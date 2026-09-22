#!/usr/bin/env python3
from __future__ import annotations
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

AGENT_DIR = Path(__file__).resolve().parents[1]
ROOT = AGENT_DIR.parent
CONFIG_PATH = AGENT_DIR / "config.json"
EVIDENCE_DIR = AGENT_DIR / "evidence"
MAX_CAPTURE = 80000

def tail(value: str) -> str:
    return value if len(value) <= MAX_CAPTURE else "[truncated]\n" + value[-MAX_CAPTURE:]

def run(cmd: str, timeout: int) -> dict[str, Any]:
    started = datetime.now(timezone.utc)
    try:
        proc = subprocess.run(cmd, cwd=ROOT, shell=True, text=True, capture_output=True, timeout=timeout)
        return {"command": cmd, "returncode": proc.returncode, "passed": proc.returncode == 0,
                "stdout": tail(proc.stdout), "stderr": tail(proc.stderr),
                "started_at": started.isoformat(), "finished_at": datetime.now(timezone.utc).isoformat()}
    except subprocess.TimeoutExpired as exc:
        return {"command": cmd, "returncode": None, "passed": False, "timed_out": True,
                "stdout": tail(exc.stdout or ""), "stderr": tail(exc.stderr or ""),
                "started_at": started.isoformat(), "finished_at": datetime.now(timezone.utc).isoformat()}

def git_snapshot(timeout: int) -> dict[str, Any]:
    out = {}
    for name, cmd in {"head":"git rev-parse HEAD","status":"git status --porcelain","diff_stat":"git diff --stat"}.items():
        r = run(cmd, timeout)
        out[name] = {"returncode": r["returncode"], "stdout": r["stdout"].strip(), "stderr": r["stderr"].strip()}
    return out

def main() -> int:
    cfg = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    verify_cfg = cfg.get("verification", {})
    timeout = int(verify_cfg.get("timeout_seconds", 180))
    commands = list(verify_cfg.get("commands", []))
    before = git_snapshot(timeout)
    results = [run(cmd, timeout) for cmd in commands]
    after = git_snapshot(timeout)
    passed = all(item["passed"] for item in results)
    evidence = {"schema_version":1,"passed":passed,"generated_at":datetime.now(timezone.utc).isoformat(),
                "workspace":str(ROOT),"git_before":before,"commands":results,"git_after":after}
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = EVIDENCE_DIR / f"verify-{stamp}.json"
    path.write_text(json.dumps(evidence, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"passed": passed, "evidence": str(path)}, ensure_ascii=False))
    return 0 if passed else 1

if __name__ == "__main__":
    sys.exit(main())
