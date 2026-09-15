# Lessons Learned — Cross-Project, Cross-Tool Error Memory

Applies to every project on this machine, not just the current repo. Shares
its memory with the Claude Code `lessons-learned` skill — both read and write
the exact same two files, so a lesson learned in either tool is available in
both:

- `$LESSONS_LEARNED_HOME/known-fixes.md` — curated, confirmed rules.
- `$LESSONS_LEARNED_HOME/error-log.md` — raw, append-only.

`LESSONS_LEARNED_HOME` defaults to `~/dev-lessons-learned` if the environment
variable isn't set. Run `scripts/install.sh` after cloning — it sets this up
and tells you what to export if you put the repo somewhere else.

**Scope:** this log is for errors *you* (Codex) hit while building, coding,
testing, or deploying — build/compile failures, failed tests, a wrong
assumption about a library/API, dependency conflicts, a logic bug you
introduced, tool/environment problems. It is not for the user's input being
wrong (a bad URL, an ambiguous instruction) — that's covered by the checklist
below instead, not by a "known fix" row.

## Getting the Most Out of Codex

Do this every session — it prevents most of the errors this file exists to
stop, before they happen:

1. **Verify before assuming.** Don't build on an unverified URL, library
   version, API signature, or file path — whether it came from the user or
   from your own memory. Check it (fetch it, read the actual dependency file
   or library source) before writing code against it.
2. **Small, verifiable steps.** Break work into steps you can test
   independently rather than writing a large chunk and hoping it holds
   together.
3. **Prove it before calling it done.** Run the build, run the tests, run
   the actual command. Don't declare a task finished because the code looks
   right.
4. **Diagnose before re-guessing.** On failure, read the actual error output
   and find the root cause before trying another fix. Don't cycle through
   guesses — log the failure in `error-log.md` if the first guess is wrong,
   rather than repeating the same class of mistake blind.
5. **Flag, don't silently guess.** If a URL, credential, or requirement
   looks wrong, incomplete, or missing, say so instead of building on top of
   an unverified assumption.

## Workflow

1. **Before starting real work,** read `known-fixes.md` for anything relevant
   to the current stack. Apply it directly.
2. **The moment something breaks:** fix it, then append an entry to
   `error-log.md` — project, stack, what broke, root cause, the fix.
3. **Promote carefully:** don't promote on one occurrence unless it's
   obviously general — otherwise wait for a 2nd confirmed hit. Update the
   `Confirmed` and `Last Confirmed` columns in `known-fixes.md` when you do.
   A confidently-wrong row is worse than none.
4. **Periodic cleanup:** when asked, or when `error-log.md` is getting long,
   promote recurring entries and run:
   ```
   python $LESSONS_LEARNED_HOME/scripts/check_known_fixes.py
   python $LESSONS_LEARNED_HOME/scripts/audit.py
   ```
   `audit.py` flags stale rows, near-duplicates, low-confidence promotions,
   and issues that recurred after already being marked fixed.

Note: this file is guidance Codex reads at the start of a session, not an
enforced rule engine — it still needs to actually be applied each time, not
just logged.
