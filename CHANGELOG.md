# Changelog

All notable changes to this project are documented here.

## [1.0.0] - 2026-05-12

### Released
- Released **orbitforge** publicly as a reviewable operating system for autonomous systems governance.
- Packaged the current implementation, documentation, validation flow, and proof surfaces into a repo that can be reviewed by technical and operating stakeholders.
- Clarified the core problem the project is addressing: collision provenance gaps, override ambiguity, and weak safety review paths across autonomous fleets.

### Why this mattered
- Existing approaches in mission dashboards, telemetry products, and simulation tooling were useful for parts of the workflow.
- They still left out a control plane for incident reasoning, policy review, and human accountability under pressure.
- This release made the repo read like an operational capability rather than a narrow technical demo.

## [0.1.0] - 2026-02-19

### Shipped
- Cut the first coherent internal version of **orbitforge** with stable domain objects, review surfaces, and decision outputs.
- Established the first reviewable version of the architecture described as: Governance and provenance control plane for satellite and orbital-agent swarms handling debris, comms, and autonomous space operations.
- Focused the repo around actionability instead of passive reporting.

## [Prototype] - 2025-05-19

### Built
- Built the first runnable prototype for the repo's main workflow and decision model.
- Validated the concept against pressure points such as collision provenance gaps, override ambiguity, and weak autonomous-system audit trails.
- Used the prototype phase to test whether the project could drive action, not just present information.

## [Design Phase] - 2025-09-09

### Designed
- Defined the system around operator-first and decision-legible outputs.
- Chose interfaces and examples that made sense for robotics, aerospace, operations, and safety teams.
- Avoided reducing the project to a generic dashboard, CRUD app, or fashionable wrapper around the stack.

## [Idea Origin] - 2025-02-09

### Observed
- The original idea surfaced while looking at how teams were handling collision provenance gaps, override ambiguity, and weak safety review paths across autonomous fleets.
- The recurring pattern was that teams had data and tools, but still lacked a usable operating layer for the hardest decisions.

## [Background Signals] - 2022-08-09

### Context
- Earlier platform, governance, and operator-tooling work made one pattern hard to ignore: the systems that create the most drag are often the ones with partial controls and weak operational coherence, not the ones with no controls at all.
- That pattern shaped the thinking behind this repo well before the public version existed.