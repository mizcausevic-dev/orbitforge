from __future__ import annotations

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.services.orbitforge_service import build_service


class OrbitForgeServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.service = build_service(ROOT)

    def test_summary_shape(self) -> None:
        summary = self.service.summary()
        self.assertEqual(summary["mission"], "Northstar Orbital Operations Mesh")
        self.assertGreater(summary["assetCount"], 0)

    def test_critical_event_lookup(self) -> None:
        event = self.service.event("orb-9001")
        self.assertIsNotNone(event)
        self.assertEqual(event["severity"], "critical")

    def test_tug_agent_is_not_clear(self) -> None:
        asset = self.service.asset("sat-415")
        self.assertIsNotNone(asset)
        self.assertIn(asset["status"], {"watch", "contain"})


if __name__ == "__main__":
    unittest.main()
