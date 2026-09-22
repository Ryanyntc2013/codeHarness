# Local deployment

## Prerequisites
- Node.js 24.2+; Node 26 recommended
- Python 3.11+
- Git
- native Codex authentication available
- OpenAI API access for the DSH Main Agent

The setup scripts install pnpm 11.7.0 if it is missing because DSH profile/plugin management uses pnpm.

DSH is developer preview. This repo pins `@deepseek-ai/dsh` to `0.1.6-alpha.2`.

## Windows
```powershell
git clone https://github.com/Ryanyntc2013/codeHarness.git
cd codeHarness
powershell -ExecutionPolicy Bypass -File .\scripts\setup.ps1
.\scripts\start.ps1
```

In DSH Web UI:
1. Settings -> Models: add/select OpenAI.
2. Choose the cloned `codeHarness` directory as workspace.
3. Create a **new** session.
4. Select preset **codeHarness**.
5. Ask it to read `.agent/PROJECT.md` and run one safe smoke-test workflow.

A fresh session matters because the preset is bound at session creation.

## Preset deployment
The setup script copies `dsh/preset/codeharness/` to `$DSH_HOME/.agent-presets/codeharness/`. This avoids current developer-preview issues with custom preset roots being overwritten at runtime.

The preset follows DSH's official platform-gated shell pattern: PowerShell on Windows and bash on POSIX.

## Codex bridge
The profile installs `@deepseek-ai/dsh-subagent-codex`; the preset exposes `subagent_codex`. Each delegation is a fresh ephemeral Codex thread in the parent workspace.

### Upstream caveat
Recent DSH preview builds have open reports where a Codex child finishes but the foreground DSH call does not settle. If seen: confirm Git/workspace state, restart DSH, preserve evidence, and record it as an upstream integration incident. V1 intentionally tests the official bridge before adding a fallback adapter.

## Smoke test
```powershell
python -m unittest discover -s tests -v
python .agent\tools\verify.py
python .agent\tools\state.py show
```

Suggested first DSH prompt:
```text
Read the codeHarness workflow files. Delegate one bounded documentation-only
or test-only improvement to subagent_codex, run deterministic verification,
review the evidence, and stop after one ACCEPTED/REWORK/NEEDS_HUMAN/BLOCKED decision.
```

## Bootstrap another project
After V1 is stable:
```powershell
python tools\init_project.py D:\projects\time-sync
```

Then edit `.agent/PROJECT.md`, `.agent/ACCEPTANCE.md`, and `.agent/config.json`, and choose that project as the DSH workspace.

## Upgrade policy
Do not unpin DSH blindly. For each upgrade: change the pinned version, rerun setup, verify preset mount, verify `subagent_codex`, run smoke tests, then adopt it for active projects.
