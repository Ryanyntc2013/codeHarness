# Architecture

```text
Operator -> DSH Web UI -> DSH Main Agent (cloud model)
                              |
                              v
                        subagent_codex
                              |
                              v
                     Codex one-shot executor
                              |
                       workspace changes
                              |
                              v
                    deterministic verifier
                              |
                        evidence JSON
                              |
                              v
                        Main Agent review
```

DSH owns UI, sessions, model routing, permissions and the subagent registry. codeHarness owns the engineering workflow, state and evidence contract.

## No DSH fork
DSH is developer preview, so V1 uses a user preset, the official Codex subagent provider, repository instructions and small deterministic Python tools.

## State
`.agent/STATE.json` is authoritative. `.agent/tools/state.py` validates transitions and rework limits.

## Evidence
`.agent/tools/verify.py` executes only commands listed in `.agent/config.json`, captures exit status/stdout/stderr and Git snapshots, and writes evidence under `.agent/evidence/`.

## Permissions
Physical hardware is human-gated in V1. Later UART/SWD/logic-analyzer/USB adapters should each declare explicit permissions.

## Executor replacement
Codex is V1. A future Cursor ACP provider can replace/add an executor without changing the state/evidence contract.
