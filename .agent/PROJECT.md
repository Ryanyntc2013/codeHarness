# Project: codeHarness V1

## Goal
Validate a reusable DeepSeek Harness workflow where a cloud Main Agent plans/reviews, Codex executes bounded coding tasks, deterministic verification independently produces evidence, and the workflow stops cleanly for humans/blockers.

## Included
- DSH Web UI
- OpenAI Main Agent provider
- official DSH Codex subagent
- project state machine
- deterministic verifier
- reusable target-project bootstrap

## Deferred
- automatic UART/SWD/logic-analyzer/USB actions
- Cursor ACP executor
- dynamic multi-model routing
- remote message broker
- unattended physical hardware operations
