---
name: pm-breakdown
description: >-
  Breaks an approved spec into atomic, traceable tasks (build tasks plus the
  user's lead tasks: comms, decisions, resources), with dependencies, critical
  path, and estimates checked against capacity, and adds the milestones to the
  client roadmap. Use when the user runs pm-breakdown or asks to split work
  into tasks or tickets.
---

# pm-breakdown: turn the spec into atomic tasks

Read [pm-core](../pm-core/SKILL.md), then
[planning-standards.md](../pm-core/references/planning-standards.md)
(atomic task rules) and the task format in
[workspace.md](../pm-core/references/workspace.md).

## Preconditions
- `spec.md` has `status: approved`, and the approach is decided. Otherwise,
  follow the gate rule.

## Steps

1. **Milestones first.** Group the stories into 1–4 milestones. Each one must
   deliver usable value on its own: "After M1, <who> can <do what>…". Avoid a
   plumbing-only first milestone. If one is truly needed, keep it short and
   explain why.
2. **Lead tasks** (`owner: me`): one for every client dependency in the spec,
   every open decision, every access or resource request, and every message
   the user has to send (kickoff, data request, demo, sign-off).
3. **Spikes** for every unknown baseline or unclear estimate: timeboxed to
   2h or less, with `done_when: answer to "<question>" written in spec.md`.
4. **Build and review tasks:** split each story until every task meets all 6
   atomic rules. Write verb-first titles. Each `done_when` must be checkable
   by someone else. Default owner: `agent` for well-specified build work that a
   coding agent can do, `me` for judgement-heavy work, or a named person.
5. **Dependencies:** add `depends_on` only where the order is really forced.
   Calculate the **critical path** (the longest chain by hours) and write it
   in the frontmatter.
6. **Dates:** add `due` only to real deadlines. Set `committed: true` only for
   dates the user has actually promised.
7. Write everything to `tasks.md` (from
   [tasks.md](../pm-core/templates/tasks.md)), grouped by milestone. Number
   tasks in a sensible execution order.
8. **Validate:** run `python3 ../pm-core/scripts/pm_scan.py --lint` and fix
   every problem it reports in this initiative.
9. **Capacity check:** compare total hours, and the user's own hours, with
   `me.md` capacity, using
   [prioritization.md](../pm-core/references/prioritization.md). Give a
   realistic finish date for each milestone. If the client expects something
   sooner, say so plainly and offer `pm-tough-conversation`.
10. **Roadmap:** add or update the milestones in `roadmap.md` (Now / Next),
    then run the narrative checks (no orphan tasks or milestones).
11. In chat, show: the milestones with their dates, task counts and hours by
    owner, the critical path, the user's lead tasks for this week, and any
    capacity warning. Nothing else.

## Delegating to a coding agent
If a task has `owner: agent`, its block should contain everything a coding
agent with no other context needs: which files or models to touch, which
inputs, and the `done_when` check. Link the spec section with a `notes:` field
if needed. Following the original OpenPM idea, the coding agent should read
only the task and the spec, not the PM conversation.
