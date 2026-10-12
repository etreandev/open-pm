---
name: pm-prioritize
description: >-
  Re-ranks all open work across every client using WSJF-lite and a capacity
  check, exposes overload, and proposes what to drop, delegate, or renegotiate.
  Writes priorities.md. Use when the user runs pm-prioritize, feels overloaded,
  gets a new urgent request, or asks "what should I focus on".
---

# pm-prioritize: what matters most, across all clients

Read [pm-core](../pm-core/SKILL.md), then
[prioritization.md](../pm-core/references/prioritization.md).

## Steps

1. **Collect the state:**
   `python3 ../pm-core/scripts/pm_scan.py --json`, plus every client's
   `client.md` (health, contract) and `roadmap.md` (Now and Next milestones),
   plus any briefs still in `draft` or `validated` that have no tasks yet.
2. **Ask at most 2 questions**, and only if the answer would change the
   ranking. For example: "Is the Acme renewal this month?" or "Any new
   requests not yet captured?" Capture new requests with `pm-intake` later; a
   one-liner in the inbox is enough for now.
3. **Score initiatives and milestones** (not individual tasks) with
   WSJF-lite. Show the factor table, so the user can argue with a single
   factor.
4. **Capacity check** for the next 2 weeks: compare committed and planned
   hours with available focus hours. If it's over, lead with that and give
   concrete options: drop, defer, delegate (to whom), or renegotiate (which
   date, with whom).
5. **Fairness check** across clients (the 60% rule).
6. **Write `priorities.md`** at the workspace root, overwriting the old one:

   ```markdown
   ---
   updated: YYYY-MM-DD
   horizon: 2 weeks
   available_focus_hours: N
   planned_hours: N
   ---
   # Priorities
   ## Ranked
   1. <client> · <initiative/milestone> · score X · <one-line why>
   ## Overload decisions needed
   - <option> → <consequence>
   ## Deliberately not now
   - <item> · <why> · <revisit date>
   ```

7. In chat, show: the overload status, the ranked top 5 with a one-line reason
   each, and the decisions you need from the user. Once the user decides,
   update the task `status` and `due` values and record any decision that
   affects a client in that client's `decisions.md`.

## Rules
- Don't silently change `committed` dates. Committed dates move only after the
  user has talked to the client.
- If renegotiation is the right answer, say so directly and offer
  `pm-tough-conversation`.
