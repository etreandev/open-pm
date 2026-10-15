---
name: pm-daily
description: >-
  Builds the user's one-screen plan for today (top 3, lead work only they can
  do, what to delegate, risks) from all clients, or runs the end-of-day
  shutdown to record progress and carry-overs. Use when the user runs
  pm-daily, says "plan my day", "what's next", or "wrap up the day".
---

# pm-daily: today, on one screen

Read [pm-core](../pm-core/SKILL.md) and [style.md](../pm-core/references/style.md)
(terse chat output). The ranking rules are the triage tiers in
[prioritization.md](../pm-core/references/prioritization.md), and they are
already built into the scanner.

## Morning mode (default)

1. Run `python3 ../pm-core/scripts/pm_scan.py` (ranked, all clients). Also
   read `priorities.md` if it is less than 7 days old, yesterday's
   `journal/daily/` file (its carry-overs), and `me.md`.
2. Ask **one** question: "What meetings or fixed blocks do you have today,
   and is anything new or on fire?" Skip it if the user already told you.
3. Calculate the available focus hours: working hours minus meetings, times
   `focus_ratio`.
4. Build the plan using [daily.md](../pm-core/templates/daily.md):
   - **Top 3:** take them from the highest tiers that fit in the available
     hours. Make one of them a lead task when one exists. For each, give the
     tier reason in a few words.
   - **Lead work:** messages to send, decisions to make, resources to chase,
     and the people waiting on the user. Point out which tasks each one
     unblocks.
   - **Delegate:** actionable `owner: agent` tasks, and the context each one
     needs.
   - **Watch list:** committed dates due within 2 days, blocked items older
     than 3 days, and meetings that need prep. Offer `pm-tough-conversation`
     for any meeting that is hard.
5. Write `journal/daily/<YYYY-MM-DD>.md`, then show it in chat. It must fit on
   one screen. If it doesn't, cut it.

## Shutdown mode ("wrap up", "end of day", "shutdown")

1. Ask: "What got done? Anything new I should capture?" Accept any form.
   IDs, plain sentences, or a brain-dump all work.
2. Update the task `status` lines in place, set `blocked_by` where it applies,
   and save new information to the right client's `inbox/`.
3. Fill in the Shutdown section of today's journal: done, carry over (with the
   reason), and tomorrow's first move.
4. If a committed date is now at risk, say so plainly and suggest the user
   warn the client **today**. Offer to draft the message.

## Rules
- Plan for 3 items, not 10. If the user insists on more, list them under
  "If time allows".
- Don't schedule more work than the available focus hours.
