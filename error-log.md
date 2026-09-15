# Error Log (raw, append-only)

## Scope

This log is for errors the AI hits **while building, coding, testing, or
deploying** — build/compile failures, failed tests, a wrong assumption about
a library/API/framework, dependency or version conflicts, deployment
failures, a logic bug it introduced, tool or environment problems.

It is **not** for user-side mistakes — a wrong URL you handed it, an
ambiguous or incomplete instruction, a typo in a prompt. Those aren't durable
code patterns worth a "known fix" row. The fix for that class of thing is
behavioral, not a lookup table — see "Getting the Most Out of Codex" in
`codex/AGENTS.md`: verify unfamiliar input before building on it, rather than
silently trusting it.

One entry per issue. Never edit or delete a past entry — this is a log, not a
scratchpad. Reviewed periodically (by you or the AI) and promoted into
`known-fixes.md` once a pattern is confirmed.

**Never paste a real secret, token, credential, or internal hostname into an
entry** — redact it (e.g. `API_KEY=<redacted>`). `scripts/check_secrets.py`
scans for likely secrets in CI, but treat that as a backstop, not a
guarantee — it catches recognizable patterns, not everything.

Add entries either by hand, by asking the AI to log it, or via:
`python scripts/log_issue.py`

---

## Entry template (copy this block for each new issue)

- **Date:**
- **Project:**
- **Stack/Tool:**
- **Category:** (env-setup / dependency / api / deployment / logic-bug / security / other)
- **Issue:**
- **Root cause:**
- **Fix:**
- **Generalizes across projects? (Y/N):**
- **Promoted to Known Fixes? (Y/N):**

---
