#!/usr/bin/env python3
"""Scan tracked markdown files for likely secrets before they get committed.

Usage:
    python scripts/check_secrets.py

Exits non-zero (for CI / pre-commit) if a likely secret is found. This is a
lightweight, regex-based heuristic — it catches recognizable patterns, not
everything, and can false-positive on long identifiers. Treat it as a
backstop, not a substitute for actually redacting secrets before writing
them into known-fixes.md or error-log.md. For stronger scanning, consider
adding a dedicated tool like gitleaks or detect-secrets alongside this.

No dependencies beyond the standard library.
"""
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCAN_FILES = ["known-fixes.md", "error-log.md"]

PATTERNS = {
    "AWS Access Key ID": re.compile(r"AKIA[0-9A-Z]{16}"),
    "Private key header": re.compile(r"-----BEGIN (RSA|EC|OPENSSH|PGP|DSA) PRIVATE KEY-----"),
    "Slack token": re.compile(r"xox[baprs]-[0-9A-Za-z-]{10,}"),
    "GitHub token": re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}"),
    "JWT-looking string": re.compile(r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}"),
    "Generic key/secret/token/password assignment": re.compile(
        r"(?i)(api[_-]?key|secret|token|password)\s*[:=]\s*['\"]?[A-Za-z0-9/+_\-]{20,}['\"]?"
    ),
}

# Lines containing these are template placeholders, not real values — skip them.
ALLOWLIST_MARKERS = ["<redacted>", "_example_", "your-", "xxxx", "placeholder"]


def scan_file(path: Path):
    hits = []
    if not path.exists():
        return hits
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if any(marker in line.lower() for marker in ALLOWLIST_MARKERS):
            continue
        for label, pattern in PATTERNS.items():
            if pattern.search(line):
                hits.append((label, lineno, line.strip()[:100]))
    return hits


def main() -> int:
    all_hits = []
    for filename in SCAN_FILES:
        path = REPO_ROOT / filename
        hits = scan_file(path)
        for label, lineno, snippet in hits:
            all_hits.append((filename, label, lineno, snippet))

    if not all_hits:
        print("No likely secrets found.")
        return 0

    print("Possible secret(s) found — review before committing/pushing:\n")
    for filename, label, lineno, snippet in all_hits:
        print(f"  {filename}:{lineno} [{label}]")
        print(f"    {snippet}")
    print(
        "\nIf these are false positives (e.g. a long non-secret identifier), "
        "add a distinguishing word to ALLOWLIST_MARKERS or edit the line. "
        "If real, redact the value before committing."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
