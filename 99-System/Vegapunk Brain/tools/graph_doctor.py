#!/usr/bin/env python3
"""Compile-check Vegapunk Brain Python tools without executing graph writes."""

from __future__ import annotations

import py_compile
import sys
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parent
    errors: list[str] = []
    for path in sorted(root.glob("*.py")):
        try:
            py_compile.compile(str(path), doraise=True)
        except py_compile.PyCompileError as exc:
            errors.append(f"{path}: {exc.msg}")
    if errors:
        print("Vegapunk Brain tool doctor failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Vegapunk Brain tool doctor passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
