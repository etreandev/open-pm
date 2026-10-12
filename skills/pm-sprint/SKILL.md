---
name: pm-sprint
description: >-
  Plans a sprint (goals per client, capacity, committed vs stretch, explicit
  not-now list) or reviews one (done vs committed, carry-over, estimate
  accuracy, mini-retro). Use when the user runs pm-sprint, says "plan the
  sprint", "sprint review", or "retro".
---

# pm-sprint: plan and review a sprint

Read [pm-core](../pm-core/SKILL.md) and
[prioritization.md](../pm-core/references/prioritization.md). The sprint
length comes from `me.md` (default 14 days).

## Plan mode (default if there's no active sprint)

1. Collect: `pm_scan.py --json`, `priorities.md` (run `pm-prioritize` first if
   it's more than 7 days old), the roadmap milestones, and the previous
   sprint's review.
2. Ask about the capacity for this sprint: PTO, holidays, on-call, and how
   available each delegate is. Calculate focus hours for each person.
3. Set **one sprint goal per client** (or none, if the client is paused). Each
   goal moves a milestone forward and is written as an outcome.
4. Fill **Committed** up to **80%** of the focus hours, in priority order, and
   respect dependencies. Lead tasks that unblock the goals go in first.
   Then fill **Stretch** up to 100%.
5. **Explicitly not this sprint:** list the tempting items you left out, with
   the reason. This list protects the user when someone asks later.
6. Run `pm_scan.py --lint`. Tasks that are too big or vague can't be committed
   until they're split.
7. Write `sprints/<from-date>-<name>.md` from
   [sprint.md](../pm-core/templates/sprint.md) with `status: active`. In chat,
   show: the goals, committed vs capacity, the not-now list, and the top
   risks.

## Review mode ("review", "retro", or the sprint end date has passed)

1. Compare the committed tasks with their current status.
2. Fill in the Review section: done or not done (carry over or drop, decided
   per item by the user), whether each goal was met, and estimate accuracy.
   Ask the user which tasks blew up.
3. **Retro:** at most 3 bullets each for Keep / Change / Try, based on
   evidence. Suggest one concrete process change. If estimates were off,
   suggest a correction factor to use next sprint.
4. Set `status: reviewed`. Offer to draft sprint-end client updates with
   `pm-update`, then start Plan mode for the next sprint.
