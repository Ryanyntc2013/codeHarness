# codeHarness repository instructions

This repository is the reusable harness layer. Keep DeepSeek Harness external; do not vendor or fork upstream DSH unless a documented blocker requires it.

## Engineering rules

1. Prefer configuration, presets and project-side tools over DSH core changes.
2. Treat `.agent/STATE.json` as the workflow state of record.
3. Never accept an agent's claim that tests passed as evidence; run `.agent/tools/verify.py`.
4. Physical hardware actions are human-gated in V1.
5. Keep the worktree clean at task handoff when the project policy requires it.
6. Preserve evidence under `.agent/evidence/`; generated evidence is git-ignored.
7. Never commit credentials.
8. Separate upstream DSH/Codex integration failures from product-code failures.

Read `CODEHARNESS.md` for the Main Agent workflow.
