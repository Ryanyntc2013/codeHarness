#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

STATE_PATH = Path(__file__).resolve().parents[1] / "STATE.json"

ALLOWED = {
    "PLAN": {"READY_LOCAL", "NEEDS_HUMAN", "BLOCKED"},
    "READY_LOCAL": {"LOCAL_RUNNING", "NEEDS_HUMAN", "BLOCKED"},
    "LOCAL_RUNNING": {"VERIFY", "REWORK", "NEEDS_HUMAN", "BLOCKED"},
    "VERIFY": {"READY_REVIEW", "REWORK", "NEEDS_HUMAN", "BLOCKED"},
    "READY_REVIEW": {"ACCEPTED", "REWORK", "NEEDS_HUMAN", "BLOCKED"},
    "REWORK": {"READY_LOCAL", "NEEDS_HUMAN", "BLOCKED"},
    "ACCEPTED": {"PLAN"},
    "NEEDS_HUMAN": {"READY_LOCAL", "PLAN", "BLOCKED"},
    "BLOCKED": {"PLAN", "READY_LOCAL", "NEEDS_HUMAN"},
}

def load_state() -> dict[str, Any]:
    return json.loads(STATE_PATH.read_text(encoding="utf-8"))

def save_state(state: dict[str, Any]) -> None:
    state["updated_at"] = datetime.now(timezone.utc).isoformat()
    tmp = STATE_PATH.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(STATE_PATH)

def transition(target: str, reason: str) -> dict[str, Any]:
    state = load_state()
    current = state["status"]
    if target not in ALLOWED.get(current, set()):
        raise SystemExit(f"illegal transition: {current} -> {target}")
    if target == "REWORK":
        state["attempt"] = int(state.get("attempt", 0)) + 1
        limit = int(state.get("max_attempts", 3))
        if state["attempt"] > limit:
            target = "NEEDS_HUMAN"
            reason = f"automatic rework limit exceeded ({limit}); {reason}"
    elif target == "PLAN" and current == "ACCEPTED":
        state["attempt"] = 0
        state["task_id"] = None
    state["status"] = target
    state["last_reason"] = reason
    save_state(state)
    return state

def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("show")
    p = sub.add_parser("transition")
    p.add_argument("state", choices=sorted(ALLOWED))
    p.add_argument("--reason", required=True)
    args = parser.parse_args()
    result = load_state() if args.command == "show" else transition(args.state, args.reason)
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
