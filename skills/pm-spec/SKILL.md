---
name: pm-spec
description: >-
  Writes a spec from a validated brief: objective, success metrics (outcome,
  output, guardrail), MUST/SHOULD/OUT scope, approach options for the user to
  decide, user stories with acceptance criteria, and a pre-mortem. Use when the
  user runs pm-spec or wants to define scope, metrics, or stories for an
  initiative.
---

# pm-spec: define success and scope (the user decides the approach)

Read [pm-core](../pm-core/SKILL.md), then
[planning-standards.md](../pm-core/references/planning-standards.md).

## Preconditions
- `brief.md` has `status: validated`. If it doesn't, follow the gate rule in
  pm-core (warn once, then record `gate_skipped` if the user insists).

## Steps

1. Read the brief, `client.md`, `roadmap.md`, and `decisions.md`. Create
   `spec.md` next to the brief from [spec.md](../pm-core/templates/spec.md).
2. **Objective:** 3 lines max, in the client's terms.
3. **Success metrics:** at least one outcome, one output, and one guardrail.
   Each needs a baseline (or `unknown`, plus a spike task to measure it), a
   target, and a measurement method. If no outcome metric can be defined, stop
   and send the user back to the client with the exact question.
4. **Scope:** keep MUST small enough that it still makes sense on its own.
   Everything the client mentioned that isn't MUST goes into SHOULD or OUT,
   with a reason. Copy OUT items to the `Not doing` section of `roadmap.md`.
5. **Approach options:** draft 2–3 real options, including the lazy one from
   the ladder. Give each one pros, cons, effort, and its rung. Recommend one
   and explain why in one line. **Then ask the user to decide.** Don't move on
   until they answer.
6. **Record the decision** as a new entry at the top of `decisions.md`, using
   [decisions.md](../pm-core/templates/decisions.md), and link it in the
   spec's frontmatter.
7. **Reuse check:** list existing assets to reuse. Any new tool, dependency, or
   infrastructure needs a justification.
8. **Stories:** 3–7, each a client capability with acceptance criteria. Data
   work needs explicit checks (freshness, completeness, reconciliation,
   uniqueness), each with a threshold.
9. **Pre-mortem:** ask "It's N weeks from now and this failed. Why?" Give at
   least 5 risks. Typical ones in data work: access arrives late, source data
   quality, metric definitions differ between teams, the stakeholder changes,
   rate limits or cost, nobody adopts the result. Each risk gets a mitigation
   and an early signal.
10. **Client dependencies:** list everything needed from the client, and by
    when. Each one becomes a lead task in `pm-breakdown`.
11. In chat, show: the metrics table, the MUST/OUT lists, the options with
    your recommendation, and the top 3 risks. Ask for the decision and scope
    approval in a single question.
12. When the user approves, set `status: approved`. If the scope differs from
    what the client confirmed in the play-back, draft a short note the user
    can send to the client. Then suggest `pm-breakdown`.
