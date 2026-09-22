param([string]$Profile = "codeharness")
$ErrorActionPreference = "Stop"
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Write-Host "== codeHarness setup =="

if (-not (Get-Command node -ErrorAction SilentlyContinue)) { throw "Node.js not found. Install Node 24.2+; Node 26 recommended." }
$nodeVersion = (& node -p "process.versions.node").Trim()
$parts = $nodeVersion.Split(".")
$major = [int]$parts[0]; $minor = [int]$parts[1]
if (($major -lt 24) -or ($major -eq 24 -and $minor -lt 2)) { throw "Node $nodeVersion detected. Node 24.2+ required; Node 26 recommended." }
if (-not (Get-Command python -ErrorAction SilentlyContinue)) { throw "Python not found. Install Python 3.11+." }

if (-not (Get-Command pnpm -ErrorAction SilentlyContinue)) {
    Write-Host "pnpm not found; installing pnpm 11.7.0 for DSH profile/plugin management..."
    & npm install --global pnpm@11.7.0
    if ($LASTEXITCODE -ne 0) { throw "Failed to install pnpm. Install pnpm 11.7.0 manually, then rerun setup." }
}

Push-Location $RepoRoot
try {
    Write-Host "[1/4] Installing pinned DSH..."
    & npm install
    if ($LASTEXITCODE -ne 0) { throw "npm install failed." }

    $DshHome = if ($env:DSH_HOME) { $env:DSH_HOME } else { Join-Path $HOME ".dsh" }
    $ProfileDir = Join-Path $DshHome "profiles\$Profile"

    if (-not (Test-Path $ProfileDir)) {
        Write-Host "[2/4] Initializing profile '$Profile' from web..."
        & npx dsh --profile $Profile --from-default-profile web --dump-config | Out-Null
        if ($LASTEXITCODE -ne 0) { throw "DSH profile initialization failed." }
    } else { Write-Host "[2/4] Profile already exists." }

    Write-Host "[3/4] Installing official Codex subagent provider..."
    & npx dsh plugin --profile $Profile add '@deepseek-ai/dsh-subagent-codex'
    if ($LASTEXITCODE -ne 0) {
        Write-Warning "Plugin command returned non-zero. If the bundle is already installed this may be harmless; verify with: npx dsh --profile $Profile --dump-config"
    }

    Write-Host "[4/4] Installing codeHarness user preset..."
    $PresetTarget = Join-Path $DshHome ".agent-presets\codeharness"
    New-Item -ItemType Directory -Force -Path $PresetTarget | Out-Null
    Copy-Item (Join-Path $RepoRoot "dsh\preset\codeharness\*") $PresetTarget -Force

    Write-Host ""
    Write-Host "Setup complete."
    Write-Host "Next: npm run start:win"
    Write-Host "Then configure OpenAI in Settings -> Models, choose this workspace,"
    Write-Host "and create a NEW session with preset 'codeHarness'."
} finally { Pop-Location }
