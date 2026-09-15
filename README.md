# dev-lessons-learned

A single, cross-project, cross-tool memory of every error and issue you've
hit — so the same mistake never gets solved twice, whether you're working in
Claude Code or Codex, and no matter which repo you're in.

## Why

Coding agents start every session from zero. The same dependency quirk, the
same env-setup gotcha, the same API footgun gets rediscovered in a different
project every time — or in a different tool, even on the same project. This
repo is one small piece of shared, persistent memory that both tools read
from and write to.

## How it works

Two files are the single source of truth:

| File | Purpose |
|---|---|
| [`known-fixes.md`](./known-fixes.md) | Curated, short, confirmed rules. Kept under ~40 rows on purpose — see below. |
| [`error-log.md`](./error-log.md) | Raw, append-only. Every issue lands here first. |

An issue is only promoted from the raw log into the curated table once it's
confirmed to generalize — across 2+ projects, or obviously general the first
time. This keeps `known-fixes.md` short enough to actually be read every
time, instead of turning into a second copy of the raw log.

**Scope — what belongs in the log and what doesn't:** this system is for
errors the AI itself hits while building, coding, testing, or deploying —
build failures, wrong assumptions about a library/API, dependency conflicts,
logic bugs it introduced. It is deliberately **not** for user-side mistakes
(a wrong URL you gave it, an ambiguous instruction) — those aren't durable
code patterns a "known fix" row can solve. That class of thing is handled by
the "Getting the Most Out of Codex" checklist in both `codex/AGENTS.md` and
`claude-code/lessons-learned/SKILL.md`: verify unfamiliar input before
building on it, rather than trusting it silently. That checklist also covers
the broader goal of getting the most reliable output out of a session, not
just avoiding repeat errors.

Two thin adapters point both tools at the same two files:

- `claude-code/lessons-learned/SKILL.md` — a Claude Code skill
- `codex/AGENTS.md` — Codex global instructions

Neither adapter holds its own copy of the data. A lesson logged from a Codex
session is immediately visible the next time Claude Code reads
`known-fixes.md`, and vice versa.

## Setup

1. Clone this repo to a fixed location — anywhere is fine, but pick one:
   ```
   git clone <this-repo> ~/dev-lessons-learned
   ```
2. Run the installer (safe to re-run any time, e.g. after moving the repo or
   on a new machine):
   ```
   bash scripts/install.sh
   ```
   This installs the Claude Code skill and the Codex global instructions,
   and tells you what to `export` if you didn't clone to `~/dev-lessons-learned`
   (the `LESSONS_LEARNED_HOME` environment variable overrides the default).

## Day to day

- **Starting work:** the AI reads `known-fixes.md` before diving in.
- **Something breaks:** the AI (or you) appends an entry to `error-log.md`.
  You can also do this by hand:
  ```
  python scripts/log_issue.py
  ```
- **Promoting a fix:** only promote after a 2nd confirmed occurrence, unless
  it's obviously general — a confidently-wrong row is worse than none. Record
  it with a `Confirmed` count and `Last Confirmed` date.
- **Cleanup / health check:**
  ```
  python scripts/check_known_fixes.py   # row-count / size limit — CI gate
  python scripts/check_secrets.py       # likely secrets — CI gate
  python scripts/audit.py               # staleness, duplicates, low-confidence
                                         # promotions, recurrence — diagnostic only
  ```
  CI runs the first two on every push; `audit.py` is for you to run and read.

## Known limitations (and what's done about them)

| Limitation | Mitigation |
|---|---|
| Loads into every AI session, whether relevant or not | Row cap + size guideline enforced by `check_known_fixes.py`; split by domain once it grows |
| Logging/promoting isn't enforced, just requested | `audit.py` surfaces staleness and low-confidence rows so drift is visible, but this is fundamentally a habit, not a guarantee |
| A bad promotion gets applied confidently by future sessions | 2-confirmation promotion rule; `audit.py` flags rows promoted on a single occurrence |
| Rules go stale as libraries/APIs change | `Last Confirmed` column; `audit.py` flags anything 120+ days old |
| Duplicate or contradictory rows can accumulate | `audit.py` does near-duplicate detection on the Issue text |
| Hardcoded path breaks if the repo moves or a new machine is used | `LESSONS_LEARNED_HOME` env var with a documented default, plus `scripts/install.sh` to re-set-up in one command |
| A real secret could get pasted into a log entry, especially if this repo is public | `check_secrets.py` runs in CI and fails the build on likely matches — a heuristic backstop, not a guarantee, so still redact manually |
| No way to measure whether a known fix actually prevented a repeat | `audit.py`'s recurrence check flags when an already-promoted category/stack shows up again in the raw log |

## Ground rules

- `known-fixes.md` only holds rules that hold regardless of project *or*
  tool. Project-specific one-offs stay in `error-log.md` only.
- Never edit or delete a past `error-log.md` entry — it's a log, not a
  scratchpad.
- If a domain (deployment, a specific API, a specific language) outgrows a
  handful of rows, split it into its own `known-fixes-<domain>.md` and link
  it from a row instead of inlining it.
- This is guidance the AI reads, not an enforced rule engine — it still has
  to actually apply it each time, not just log it.

## License

MIT — see [`LICENSE`](./LICENSE).
