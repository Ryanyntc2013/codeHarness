#!/usr/bin/env python3
from __future__ import annotations
import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def copy_if_missing(src: Path, dst: Path, force: bool) -> None:
    if dst.exists() and not force:
        print(f"skip existing: {dst}")
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    print(f"write: {dst}")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("target", type=Path)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    target = args.target.resolve()
    target.mkdir(parents=True, exist_ok=True)
    for rel in ["CODEHARNESS.md",".agent/ACCEPTANCE.md",".agent/PROJECT.md",".agent/STATE.json",
                ".agent/config.json",".agent/tools/state.py",".agent/tools/verify.py"]:
        copy_if_missing(ROOT / rel, target / rel, args.force)
    (target / ".agent/evidence").mkdir(parents=True, exist_ok=True)
    print("\nNext: edit .agent/PROJECT.md, ACCEPTANCE.md and config.json for the target project.")

if __name__ == "__main__":
    main()
