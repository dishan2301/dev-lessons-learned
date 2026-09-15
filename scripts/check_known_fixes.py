#!/usr/bin/env python3
"""Fail if known-fixes.md has grown past the row limit.

Usage:
    python scripts/check_known_fixes.py

Exits non-zero (for CI) if the table has more than MAX_ROWS real rows.
The "_example_" row is not counted.

No dependencies beyond the standard library.
"""
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
KNOWN_FIXES_FILE = REPO_ROOT / "known-fixes.md"
MAX_ROWS = 40


def main() -> int:
    if not KNOWN_FIXES_FILE.exists():
        print(f"ERROR: {KNOWN_FIXES_FILE} not found.")
        return 1

    lines = KNOWN_FIXES_FILE.read_text(encoding="utf-8").splitlines()

    table_lines = [
        line for line in lines
        if line.strip().startswith("|") and "---" not in line
    ]

    # First matching line is the header row; drop it.
    data_rows = table_lines[1:] if table_lines else []

    # Don't count the placeholder example row.
    real_rows = [row for row in data_rows if "_example_" not in row]

    count = len(real_rows)
    print(f"known-fixes.md: {count} row(s) (limit {MAX_ROWS})")

    if count > MAX_ROWS:
        print(
            f"\nOver the limit. Split a domain out into its own "
            f"known-fixes-<domain>.md file and link it from a row here "
            f"instead of inlining it."
        )
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
