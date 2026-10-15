---
name: pm-spec
description: >-
  Write spec from validated brief: objective, metrics, MUST/SHOULD/OUT scope,
  approach trade-offs, stories with acceptance criteria, pre-mortem. Trigger
  on pm-spec or scope definition.
---

# pm-spec: define success and scope (user decides approach)

Read [pm-core](../pm-core/SKILL.md) and [planning-standards.md](../pm-core/references/planning-standards.md).

## Preconditions
- `brief.md` has `status: validated`. Missing: follow gate rule (warn once; record `gate_skipped` if forced).

## Steps

1. Read brief, `client.md`, `roadmap.md`, `decisions.md`. Create `spec.md` adjacent to brief from [spec.md](../pm-core/templates/spec.md).
2. **Objective:** ≤ 3 lines, client terms.
3. **Success metrics:** minimum one outcome, one output, one guardrail. Include baseline (or `unknown` + spike task), target, measurement method. No outcome metric: stop; provide question for client.
4. **Scope:** MUST stays minimal viable core. Move other client requests to SHOULD or OUT with rationale. Mirror OUT items into `roadmap.md` `Not doing`.
5. **Approach options:** present 2–3 real options, including ladder lazy option. Document pros, cons, effort, rung. Recommend one in single line. **Prompt user to decide.** Block until answered.
6. **Record decision:** prepend entry to `decisions.md` from [decisions.md](../pm-core/templates/decisions.md); link in `spec.md` frontmatter.
7. **Reuse audit:** enumerate existing reusable assets. Justify any new dependency or infrastructure.
8. **Stories:** 3–7 items. Client capability format with acceptance criteria. Data work requires explicit thresholds (freshness, completeness, reconciliation, uniqueness).
9. **Pre-mortem:** list ≥ 5 failure modes (access lag, source quality, metric drift, stakeholder churn, cost/rate limits, non-adoption). Provide early signal and mitigation per risk.
10. **Client dependencies:** list required inputs with deadlines. Feed into lead tasks for `pm-breakdown`.
11. **Chat output:** metrics table, MUST/OUT lists, options with recommendation, top 3 risks. Request approach decision and scope approval in single prompt.
12. Approval: set `status: approved`. If scope diverged from play-back, draft note for client. Suggest `pm-breakdown`.
