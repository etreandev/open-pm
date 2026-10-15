---
name: pm-prioritize
description: >-
  Re-rank open work across all clients via WSJF-lite and capacity checks.
  Expose overload; propose drop/delegate/renegotiate options. Writes priorities.md.
  Trigger on pm-prioritize, overload, or focus question.
---

# pm-prioritize: stack-rank work across clients

Read [pm-core](../pm-core/SKILL.md) and [prioritization.md](../pm-core/references/prioritization.md).

## Steps

1. **Gather state:**
   `python3 ../pm-core/scripts/pm_scan.py --json`, client files `client.md` (health, contract) and `roadmap.md` (Now/Next milestones), plus briefs in `draft` or `validated` lacking tasks.
2. **Clarify (max 2 questions):** ask only if answers shift ranking (e.g., contract renewals, unlogged requests). Log incoming asks in client inbox for later `pm-intake`.
3. **Score via WSJF-lite:** score initiatives and milestones (never single tasks). Display factor matrix for user review.
4. **Capacity audit (2-week horizon):** compare committed/planned hours against focus capacity. If overloaded: lead with deficit, provide explicit levers (drop, defer, delegate with assignee, renegotiate target date and stakeholder).
5. **Fairness audit:** verify cross-client balance (max 60% capacity to single client).
6. **Write `priorities.md`** at workspace root:

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

7. **Chat output:** overload status, ranked top 5 with single-line rationale, pending decisions. After decision: update task `status`/`due`, log client impacts in `decisions.md`.

## Rules
- Never move `committed: true` dates silently. Changes require client consultation.
- When renegotiation required, state directly; suggest `pm-tough-conversation`.
