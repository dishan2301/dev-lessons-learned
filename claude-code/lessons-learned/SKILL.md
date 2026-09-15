---
name: lessons-learned
description: Global, cross-project, cross-tool error and issue memory. Use this whenever starting real coding/dev work in ANY project, and — most importantly — the instant an error, exception, failed build, unexpected bug, or "stuck" moment happens, even if not explicitly asked to check it. Also consult before wrapping up a coding session. Exists so the same mistake is never solved twice, whether it was first hit here or in Codex.
---

# Lessons Learned — Cross-Project, Cross-Tool Error Memory

This skill shares its memory with the Codex `AGENTS.md` version of the same
system — both read and write the exact same two files, so a lesson learned in
either tool is available in both:

- `$LESSONS_LEARNED_HOME/known-fixes.md` — curated, confirmed rules. **Always
  read this in full the moment this skill triggers** — it is short by design,
  treat reading it as mandatory, not optional context.
- `$LESSONS_LEARNED_HOME/error-log.md` — raw, append-only.

`LESSONS_LEARNED_HOME` defaults to `~/dev-lessons-learned` if unset. Run
`scripts/install.sh` after cloning — it sets this up and tells you what to
export if the repo lives somewhere else.

**Scope:** this log is for errors *you* hit while building, coding, testing,
or deploying — build/compile failures, failed tests, a wrong assumption
about a library/API, dependency conflicts, a logic bug you introduced,
tool/environment problems. It is not for the user's input being wrong (a bad
URL, an ambiguous instruction) — that's covered by the checklist below
instead of a "known fix" row.

## Getting the Most Out of This

Do this every session — it prevents most of the errors this file exists to
stop, before they happen:

1. **Verify before assuming.** Don't build on an unverified URL, library
   version, API signature, or file path. Check it before writing code
   against it.
2. **Small, verifiable steps.** Test independently as you go rather than
   writing a large chunk and hoping it holds together.
3. **Prove it before calling it done.** Run the build, run the tests, run
   the actual command.
4. **Diagnose before re-guessing.** On failure, read the actual error output
   and find the root cause before trying another fix.
5. **Flag, don't silently guess.** If a URL, credential, or requirement
   looks wrong or missing, say so instead of building on an unverified
   assumption.

## Workflow

1. **Starting a task:** read `known-fixes.md` in full. Apply anything relevant
   directly — don't rediscover it.
2. **The moment something breaks:** fix it, then append an entry to
   `error-log.md` (template inside it) — project, stack, what broke, root
   cause, the fix.
3. **Promote carefully:** don't promote on one occurrence unless it's
   obviously general — otherwise wait for a 2nd confirmed hit. Update the
   `Confirmed` and `Last Confirmed` columns when you do. A confidently-wrong
   row is worse than none.
4. **Periodic cleanup:** when asked, or when `error-log.md` is getting long,
   review newer entries and promote anything recurring or clearly general.
   Run:
   ```
   python $LESSONS_LEARNED_HOME/scripts/check_known_fixes.py
   python $LESSONS_LEARNED_HOME/scripts/audit.py
   ```
   before finishing — `audit.py` flags stale rows, near-duplicates,
   low-confidence promotions, and issues that recurred after already being
   marked fixed.

## Ground rules

- `known-fixes.md` only holds rules that hold regardless of project *or*
  tool. One-off, project-specific quirks stay in `error-log.md` only.
- Never delete or rewrite a past `error-log.md` entry.
- Install this folder at `~/.claude/skills/lessons-learned/` (Claude Code's
  "personal" skill location) so it loads in every project on this machine.
