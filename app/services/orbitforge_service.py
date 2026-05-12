from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from statistics import mean
from typing import Any


def _clamp(value: float, low: int = 0, high: int = 100) -> int:
    return max(low, min(high, round(value)))


@dataclass(slots=True)
class OrbitForgeService:
    source_path: Path

    def load(self) -> dict[str, Any]:
        return json.loads(self.source_path.read_text(encoding="utf-8"))

    def assets(self) -> list[dict[str, Any]]:
        data = self.load()
        events_by_asset: dict[str, list[dict[str, Any]]] = {}
        for event in data["events"]:
            events_by_asset.setdefault(event["asset_id"], []).append(event)

        enriched: list[dict[str, Any]] = []
        for asset in data["assets"]:
            history = events_by_asset.get(asset["asset_id"], [])
            critical_events = sum(1 for event in history if event["severity"] == "critical")
            conjunctions = sum(1 for event in history if event["event_type"] == "conjunction-alert")
            governance_risk = _clamp(
                max(0, 2.8 - asset["collision_distance_km"]) * 24
                + max(0, 60 - asset["fuel_margin_pct"]) * 0.9
                + max(0, 85 - asset["crosslink_health"]) * 1.1
                + (14 if not asset["override_ready"] else 0)
                + critical_events * 16
                + conjunctions * 14
                + min(asset["last_maneuver_hours"], 36) * 0.6
            )
            status = "contain" if governance_risk >= 76 else "watch" if governance_risk >= 48 else "clear"
            next_action = (
                "Pause autonomous maneuver expansion, require human signoff, and preserve the full maneuver chain for replay."
                if status == "contain"
                else "Hold the asset inside a tighter envelope and monitor crosslink and conjunction state before the next task handoff."
                if status == "watch"
                else "Continue autonomous operations with governance telemetry attached to the mission record."
            )
            enriched.append(
                {
                    "assetId": asset["asset_id"],
                    "name": asset["name"],
                    "class": asset["class"],
                    "orbitBand": asset["orbit_band"],
                    "task": asset["task"],
                    "fuelMarginPct": asset["fuel_margin_pct"],
                    "collisionDistanceKm": asset["collision_distance_km"],
                    "crosslinkHealth": asset["crosslink_health"],
                    "overrideReady": asset["override_ready"],
                    "policyEnvelope": asset["policy_envelope"],
                    "governanceRisk": governance_risk,
                    "status": status,
                    "nextAction": next_action,
                }
            )
        return sorted(enriched, key=lambda item: (-item["governanceRisk"], item["name"]))

    def events(self) -> list[dict[str, Any]]:
        data = self.load()
        severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        assets = {asset["assetId"]: asset for asset in self.assets()}
        enriched: list[dict[str, Any]] = []
        for event in data["events"]:
            provenance_score = _clamp(
                (30 if event["override_applied"] else 12)
                + len(event["handoff_chain"]) * 12
                + (20 if event["resolution_state"] in {"maneuver-authorized", "replanned"} else 8)
                + (22 if event["severity"] == "critical" else 14 if event["severity"] == "high" else 7)
            )
            enriched.append(
                {
                    "eventId": event["event_id"],
                    "timestamp": event["timestamp"],
                    "assetId": event["asset_id"],
                    "assetName": assets.get(event["asset_id"], {}).get("name", event["asset_id"]),
                    "orbitBand": event["orbit_band"],
                    "severity": event["severity"],
                    "eventType": event["event_type"],
                    "policyTriggered": event["policy_triggered"],
                    "handoffChain": event["handoff_chain"],
                    "overrideApplied": event["override_applied"],
                    "resolutionState": event["resolution_state"],
                    "distanceKm": event["distance_km"],
                    "provenanceScore": provenance_score,
                }
            )
        return sorted(enriched, key=lambda item: (severity_order[item["severity"]], item["timestamp"]))

    def summary(self) -> dict[str, Any]:
        data = self.load()
        assets = self.assets()
        events = self.events()
        contain = [asset for asset in assets if asset["status"] == "contain"]
        high_events = [event for event in events if event["severity"] in {"critical", "high"}]
        avg_risk = mean(asset["governanceRisk"] for asset in assets)
        avg_provenance = mean(event["provenanceScore"] for event in events)
        return {
            "mission": data["mission"],
            "theater": data["theater"],
            "assetCount": len(assets),
            "containCount": len(contain),
            "highSeverityEventCount": len(high_events),
            "averageGovernanceRisk": round(avg_risk, 1),
            "averageProvenanceScore": round(avg_provenance, 1),
            "leadRecommendation": (
                "Keep the tug agent and debris-watch node inside tighter conjunction rules, then preserve every maneuver and handoff branch so orbital investigations can replay the decision chain without ambiguity."
            ),
        }

    def asset(self, asset_id: str) -> dict[str, Any] | None:
        for asset in self.assets():
            if asset["assetId"] == asset_id:
                return asset
        return None

    def event(self, event_id: str) -> dict[str, Any] | None:
        for event in self.events():
            if event["eventId"] == event_id:
                return event
        return None

    def sample_payload(self) -> dict[str, Any]:
        assets = self.assets()
        events = self.events()
        return {
            "dashboard": self.summary(),
            "assets": [
                {
                    "assetId": asset["assetId"],
                    "name": asset["name"],
                    "governanceRisk": asset["governanceRisk"],
                    "status": asset["status"],
                    "nextAction": asset["nextAction"],
                }
                for asset in assets[:3]
            ],
            "events": [
                {
                    "eventId": event["eventId"],
                    "severity": event["severity"],
                    "eventType": event["eventType"],
                    "resolutionState": event["resolutionState"],
                    "provenanceScore": event["provenanceScore"],
                }
                for event in events[:3]
            ],
        }


def build_service(root: Path | None = None) -> OrbitForgeService:
    base = root or Path(__file__).resolve().parents[2]
    return OrbitForgeService(base / "app" / "data" / "sample_orbit.json")
