# V1 acceptance criteria

1. DSH Web UI starts with profile `codeharness`.
2. A fresh session can select the `codeHarness` preset.
3. OpenAI can be selected as Main Agent.
4. Main Agent can call `subagent_codex` on a bounded repository task.
5. Codex can edit the workspace and return a final result.
6. `python .agent/tools/verify.py` produces machine-readable evidence.
7. Main Agent reviews evidence and chooses ACCEPTED, REWORK, NEEDS_HUMAN, or BLOCKED.
8. State transitions persist in `.agent/STATE.json`.
9. Automatic rework never exceeds the configured limit.
10. No physical hardware action occurs automatically in V1.
