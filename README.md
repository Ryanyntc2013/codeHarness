# codeHarness

A lightweight hardware-R&D agent harness built on top of DeepSeek Harness (DSH).

## V1 goal

Run this loop locally:

```text
DSH Main Agent (cloud model: OpenAI)
        |
        v
Codex subagent (local executor)
        |
        v
workspace edits / build / test / git
        |
        v
deterministic verifier
        |
        v
DSH Main Agent review
        |
        +--> ACCEPT -> next task
        +--> REWORK -> delegate again
        +--> NEEDS_HUMAN -> stop for operator
        +--> BLOCKED -> stop with evidence
```

V1 intentionally does **not** automate physical hardware actions. UART/SWD/logic-analyzer/USB adapters are reserved for later phases.

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for Windows deployment and [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for the design.

## Version baseline

- DeepSeek Harness: `0.1.6-alpha.2`
- Node.js: **24.2+**, Node 26 recommended
- Python: 3.11+
- Codex authentication/configuration: managed by native Codex/DSH subagent integration

DSH is currently a developer preview. This repository keeps DSH itself external and puts our behavior in presets, project instructions, scripts and state files so upstream can be upgraded without maintaining a fork.
