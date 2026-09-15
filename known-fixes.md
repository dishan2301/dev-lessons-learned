# Known Fixes

Curated, cross-project, cross-tool rules — confirmed across 2+ projects, or
obviously general the first time. Both the Claude Code skill and the Codex
AGENTS.md read this same file, so a lesson learned in either tool is available
in both.

Keep this under ~40 rows. If a domain outgrows that (e.g. deployment, a
specific API, a specific language), split it into `known-fixes-<domain>.md` in
this repo and link it from the row instead of inlining the detail.

**Promotion rule:** don't promote on a single occurrence unless it's
obviously general (e.g. an environment-wide setup step). Otherwise wait for a
2nd confirmed occurrence — a confidently-wrong row is worse than no row,
since future sessions are told to apply it "directly, don't rediscover it."

**Staleness:** update `Last Confirmed` whenever a row is re-confirmed still
true. A row that hasn't been touched in 120+ days should be re-verified, not
trusted blind — the library/API/tool it describes may have moved on.

**Never paste a real secret, token, or credential into a row** — redact it
(e.g. `API_KEY=<redacted>`). `scripts/check_secrets.py` scans for likely
secrets in CI, but treat that as a backstop, not a guarantee.

Run these any time:
```
python scripts/check_known_fixes.py   # row-count / size limit
python scripts/audit.py               # staleness, duplicates, low-confidence rows, recurrence
```
CI runs `check_known_fixes.py` and `check_secrets.py` on every push.

| Category | Stack/Tool | Issue | Fix / Rule | Confirmed | Last Confirmed |
|---|---|---|---|---|---|
| _example_ | _example_ | _example error pattern_ | _example fix, stated as a rule to follow next time_ | 1 | 2026-09-15 |

