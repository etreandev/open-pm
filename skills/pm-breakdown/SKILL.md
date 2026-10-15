---
name: pm-breakdown
description: >-
  Break approved spec into atomic tasks (build + lead), dependencies,
  critical path, capacity check, and roadmap milestones. Trigger on
  pm-breakdown or request to split work into tasks/tickets.
---

# pm-breakdown: turn spec into atomic tasks

Read [pm-core](../pm-core/SKILL.md), [planning-standards.md](../pm-core/references/planning-standards.md) (atomic rules), [style.md](../pm-core/references/style.md) (terse: title ≤ 8 words, `done_when` ≤ 25 words), and [workspace.md](../pm-core/references/workspace.md) (task schema).

## Preconditions
- `spec.md` has `status: approved` and decided approach. Otherwise: apply gate rule.

## Steps

1. **Milestones first.** Group stories into 1–4 milestones. Deliver isolated usable capability: "After M1, <who> can <do what>…". No plumbing-only first milestone unless strictly necessary with documented reason.
2. **Lead tasks** (`owner: me`): create task per client dependency, decision, access/resource request, and outreach (kickoff, data request, demo, sign-off).
3. **Spikes:** unknown baselines or fuzzy estimates get spike ≤ 2h, with `done_when: answer to "<question>" written in spec.md`.
4. **Build and review tasks:** decompose stories until all 6 atomic rules pass. Verb-first titles. Binary `done_when` verifiable by third party. Owner defaults: `agent` for deterministic build tasks, `me` for judgement, or named individual.
5. **Dependencies:** declare `depends_on` only for strict sequence constraints. Calculate critical path (longest chain by hours); record in frontmatter.
6. **Dates:** set `due` only on hard deadlines. Set `committed: true` only on explicit promises.
7. Save `tasks.md` from [tasks.md](../pm-core/templates/tasks.md), grouped by milestone, numbered in execution order.
8. **Validate:** run `python3 ../pm-core/scripts/pm_scan.py --lint`; clear all errors.
9. **Capacity check:** check total/user hours against `me.md` via [prioritization.md](../pm-core/references/prioritization.md). Provide realistic completion dates. If client expects earlier delivery: flag mismatch, offer `pm-tough-conversation`.
10. **Roadmap:** sync milestones to `roadmap.md` (Now / Next). Run narrative checks (no orphan tasks or milestones).
11. **Chat output (only these):** milestones with dates, task counts and hours by owner, critical path, lead tasks for week, capacity warnings.

## Delegating to coding agent
For `owner: agent`, task must be self-contained: target files/models, inputs, binary `done_when`. Link spec section in `notes:` if needed. Coding agent reads only task and spec, never PM conversation.
