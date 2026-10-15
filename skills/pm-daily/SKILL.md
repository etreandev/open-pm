---
name: pm-daily
description: >-
  Generate single-screen daily plan (top 3, user lead tasks, delegation, risks)
  or execute end-of-day shutdown. Trigger on pm-daily, "plan my day",
  "what's next", or "wrap up the day".
---

# pm-daily: today on one screen

Read [pm-core](../pm-core/SKILL.md) and [style.md](../pm-core/references/style.md) (terse chat output). Ranking uses triage tiers in [prioritization.md](../pm-core/references/prioritization.md) (embedded in scanner).

## Morning mode (default)

1. **Scan state:** run `python3 ../pm-core/scripts/pm_scan.py`. Inspect `priorities.md` (if < 7 days old), previous `journal/daily/` carry-overs, `me.md`.
2. **Clarify (single question):** "What meetings/blocks today; anything on fire?" Skip if provided.
3. **Compute focus hours:** (working hours - meeting hours) × `focus_ratio`.
4. **Draft plan** via [daily.md](../pm-core/templates/daily.md):
   - **Top 3:** highest tiers fitting available hours. Include lead task if available. Add brief tier reason.
   - **Lead work:** user-only tasks (comms, decisions, unblocking others). Link unblocked tasks.
   - **Delegate:** actionable `owner: agent` tasks with required context.
   - **Watch list:** committed deadlines ≤ 2 days, blockers > 3 days, high-friction meetings (offer `pm-tough-conversation`).
5. **Persist and emit:** save `journal/daily/<YYYY-MM-DD>.md`. Output to chat. Must fit on single screen. Prune if exceeds.

## Shutdown mode (trigger: "wrap up", "end of day", "shutdown")

1. Prompt: "What got done? Any new inputs?" Accept raw IDs, sentences, brain-dumps.
2. Update task `status` in place. Populate `blocked_by`. Route new inputs to client `inbox/`.
3. Complete journal Shutdown section: completed, carry-overs with rationale, tomorrow's first move.
4. If committed date endangered: state immediately; advise warning client today. Offer draft.

## Rules
- Cap primary plan at 3 items. Spillover goes under "If time allows".
- Never exceed available focus hours.
