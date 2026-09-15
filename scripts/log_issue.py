#!/usr/bin/env python3
"""Append a new entry to error-log.md interactively.

Usage:
    python scripts/log_issue.py

No dependencies beyond the standard library.
"""
import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
LOG_FILE = REPO_ROOT / "error-log.md"

CATEGORIES = [
    "env-setup",
    "dependency",
    "api",
    "deployment",
    "logic-bug",
    "security",
    "other",
]


def ask(prompt: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    value = input(f"{prompt}{suffix}: ").strip()
    return value or default


def main() -> None:
    print("New error-log entry (Ctrl+C to cancel)\n")

    date = ask("Date", datetime.date.today().isoformat())
    project = ask("Project")
    stack = ask("Stack/Tool")

    print(f"Category options: {', '.join(CATEGORIES)}")
    category = ask("Category", "other")

    issue = ask("Issue")
    root_cause = ask("Root cause")
    fix = ask("Fix")
    generalizes = ask("Generalizes across projects? (Y/N)", "N")
    promoted = "N"  # always starts unpromoted; promotion is a deliberate, separate step

    entry = f"""
## {date} — {project}

- **Date:** {date}
- **Project:** {project}
- **Stack/Tool:** {stack}
- **Category:** {category}
- **Issue:** {issue}
- **Root cause:** {root_cause}
- **Fix:** {fix}
- **Generalizes across projects? (Y/N):** {generalizes}
- **Promoted to Known Fixes? (Y/N):** {promoted}

---
"""

    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(entry)

    print(f"\nAppended to {LOG_FILE}")
    if generalizes.strip().upper() == "Y":
        print(
            "You marked this as generalizable — consider adding a row to "
            "known-fixes.md now instead of waiting for a cleanup pass."
        )


if __name__ == "__main__":
    main()
