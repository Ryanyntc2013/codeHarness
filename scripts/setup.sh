#!/usr/bin/env bash
set -euo pipefail
PROFILE="${1:-codeharness}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
node -e 'const [a,b]=process.versions.node.split(".").map(Number); if(a<24 || (a===24 && b<2)){console.error("Node 24.2+ required; Node 26 recommended"); process.exit(1)}'
python --version
npm install
DSH_HOME="${DSH_HOME:-$HOME/.dsh}"
if [[ ! -d "$DSH_HOME/profiles/$PROFILE" ]]; then
  npx dsh --profile "$PROFILE" --from-default-profile web --dump-config >/dev/null
fi
npx dsh plugin --profile "$PROFILE" add @deepseek-ai/dsh-subagent-codex || true
mkdir -p "$DSH_HOME/.agent-presets/codeharness"
cp -f dsh/preset/codeharness/* "$DSH_HOME/.agent-presets/codeharness/"
echo "Setup complete. Start with: npx dsh --profile $PROFILE"
