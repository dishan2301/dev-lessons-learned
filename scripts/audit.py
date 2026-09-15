#!/usr/bin/env python3
"""Diagnostic audit for known-fixes.md and error-log.md.

Usage:
    python scripts/audit.py

Read-only and always exits 0 — this is a report for a human to act on, not a
CI gate (use check_known_fixes.py / check_secrets.py for that). Catches the
failure modes that a row-count check can't:

  - stale rows (not re-confirmed in a while)
  - near-duplicate rows (same issue described twice, possibly diverging)
  - low-confidence promotions (promoted on a single occurrence)
  - recurrence (an issue category/stack that came back after already being
    marked as a known fix — a sign the fix isn't holding)

No dependencies beyond the standard library.
"""
import difflib
import re
from datetime import date, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
KNOWN_FIXES_FILE = REPO_ROOT / "known-fixes.md"
ERROR_LOG_FILE = REPO_ROOT / "error-log.md"

STALE_AFTER_DAYS = 120
SIMILARITY_THRESHOLD = 0.75
KNOWN_FIXES_CHAR_GUIDELINE = 6000


def parse_known_fixes_rows(text: str):
    rows = []
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|") or "---" in line:
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if cells and cells[0].lower() == "category":
            continue  # header row
        if any("_example_" in c for c in cells):
            continue  # placeholder row
        if len(cells) >= 6:
            rows.append({
                "category": cells[0],
                "stack": cells[1],
                "issue": cells[2],
                "fix": cells[3],
                "confirmed": cells[4],
                "last_confirmed": cells[5],
            })
    return rows


def parse_error_log_entries(text: str):
    """Parse '- **Key:** value' lines into dicts, one dict per '---'-separated block."""
    entries = []
    current = {}
    for line in text.splitlines():
        m = re.match(r"-\s+\*\*(.+?):\*\*\s*(.*)", line.strip())
        if m:
            current[m.group(1).strip().lower()] = m.group(2).strip()
        elif line.strip() == "---" and current:
            entries.append(current)
            current = {}
    if current:
        entries.append(current)
    # Drop the blank entry template itself (it has no real Issue field —
    # the Category line's placeholder text made a blanket "any field set"
    # check insufficient).
    entries = [e for e in entries if e.get("issue", "").strip()]
    return entries


def check_staleness(rows):
    print("\n--- Staleness (Known Fixes not re-confirmed recently) ---")
    today = date.today()
    found = False
    for row in rows:
        raw = row["last_confirmed"]
        try:
            d = datetime.strptime(raw, "%Y-%m-%d").date()
        except ValueError:
            print(f"  ? unparseable date '{raw}' — {row['issue'][:60]}")
            continue
        age = (today - d).days
        if age > STALE_AFTER_DAYS:
            found = True
            print(f"  STALE ({age}d old): [{row['category']}/{row['stack']}] {row['issue'][:60]}")
    if not found:
        print("  None.")


def check_duplicates(rows):
    print("\n--- Near-duplicate rows (Known Fixes) ---")
    found = False
    for i in range(len(rows)):
        for j in range(i + 1, len(rows)):
            ratio = difflib.SequenceMatcher(None, rows[i]["issue"], rows[j]["issue"]).ratio()
            if ratio > SIMILARITY_THRESHOLD:
                found = True
                print(f"  {ratio:.0%} similar:")
                print(f"    - {rows[i]['issue'][:70]}")
                print(f"    - {rows[j]['issue'][:70]}")
    if not found:
        print("  None.")


def check_low_confidence(rows):
    print("\n--- Low-confidence promotions (confirmed < 2 times) ---")
    found = False
    for row in rows:
        try:
            count = int(row["confirmed"])
        except ValueError:
            count = 0
        if count < 2:
            found = True
            print(f"  confirmed {count}x: [{row['category']}/{row['stack']}] {row['issue'][:60]}")
    if not found:
        print("  None — all rows confirmed 2+ times.")
    else:
        print("  (Fine if genuinely a one-shot general rule; otherwise re-verify.)")


def check_recurrence(known_fixes_rows, log_entries):
    print("\n--- Recurrence (issue came back after being marked known) ---")
    promoted_keys = {(r["category"].lower(), r["stack"].lower()) for r in known_fixes_rows}
    found = False
    for entry in log_entries:
        key = (entry.get("category", "").lower(), entry.get("stack/tool", "").lower())
        already_promoted_this_entry = entry.get("promoted to known fixes? (y/n)", "").upper() == "Y"
        if key in promoted_keys and not already_promoted_this_entry:
            found = True
            print(f"  {entry.get('project', '?')}: {key[0]}/{key[1]} hit again — "
                  f"check whether the known fix actually applies or is stale")
    if not found:
        print("  None detected.")


def check_size(text: str):
    print("\n--- known-fixes.md size ---")
    chars = len(text)
    print(f"  {chars} characters (guideline ~{KNOWN_FIXES_CHAR_GUIDELINE})")
    if chars > KNOWN_FIXES_CHAR_GUIDELINE:
        print("  Over guideline — this loads into every session. Consider splitting by domain.")


def main() -> None:
    kf_text = KNOWN_FIXES_FILE.read_text(encoding="utf-8") if KNOWN_FIXES_FILE.exists() else ""
    log_text = ERROR_LOG_FILE.read_text(encoding="utf-8") if ERROR_LOG_FILE.exists() else ""

    rows = parse_known_fixes_rows(kf_text)
    entries = parse_error_log_entries(log_text)

    print(f"known-fixes.md: {len(rows)} row(s)  |  error-log.md: {len(entries)} entrie(s)")

    check_staleness(rows)
    check_duplicates(rows)
    check_low_confidence(rows)
    check_recurrence(rows, entries)
    check_size(kf_text)

    print("\nDiagnostic only — nothing was changed. Act on what's relevant.")


if __name__ == "__main__":
    main()
