---
name: pm-sprint
description: >-
  Plan sprint (client goals, capacity, committed vs stretch, not-now list)
  or run review (outcomes, carry-over, retro). Trigger on pm-sprint,
  "plan sprint", "sprint review", or "retro".
---

# pm-sprint: plan and review sprint

Read [pm-core](../pm-core/SKILL.md) and [prioritization.md](../pm-core/references/prioritization.md). Sprint cadence sourced from `me.md` (default 14 days).

## Plan mode (default when no active sprint)

1. **Gather context:** `pm_scan.py --json`, `priorities.md` (require `pm-prioritize` if > 7 days old), roadmap milestones, previous sprint review.
2. **Capacity audit:** prompt for PTO, holidays, on-call, delegate bandwidth. Compute focus hours per person.
3. **Set sprint goals:** exactly one outcome goal per active client, advancing specific milestone. Paused clients get zero.
4. **Allocate work:**
   - **Committed:** fill to 80% focus capacity. Priority order. Unblocking lead tasks first. Respect dependencies.
   - **Stretch:** fill remaining 80–100% capacity.
5. **Explicitly not this sprint:** record deferred high-temptation items with rationale.
6. **Pre-flight lint:** execute `pm_scan.py --lint`. Oversized or vague tasks forbidden in committed scope until decomposed.
7. **Write artifact:** `sprints/<from-date>-<name>.md` from [sprint.md](../pm-core/templates/sprint.md) (`status: active`).
8. **Chat output:** goals, committed hours vs capacity, not-now items, top risks.

## Review mode (trigger: "review", "retro", or sprint end date passed)

1. Compare committed tasks against terminal status.
2. Complete Review section: terminal state per item (user selects carry-over or drop), goal achievement, estimate variance. Identify blown estimates.
3. **Retro:** max 3 bullets each for Keep / Change / Try. One actionable workflow change. If estimates drifted: calculate variance multiplier for next cycle.
4. Mark `status: reviewed`. Offer `pm-update` drafts. Launch Plan mode for subsequent sprint.
