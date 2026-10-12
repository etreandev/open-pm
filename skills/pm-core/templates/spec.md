---
initiative: <NNN>-<slug>
client: <client-slug>
status: draft            # draft | approved | done | parked
brief: ./brief.md
approved: <YYYY-MM-DD, by the user>
decision: <D<n> in decisions.md>
---

# Spec - <initiative name>

## 1. Objective
<What the client gets and why it matters. Max 3 lines.>

## 2. Success metrics
| Kind | Metric | Baseline | Target | How measured |
|:--|:--|:--|:--|:--|
| Outcome | | | | |
| Output | | | | |
| Guardrail | | | | |

## 3. Scope
- **MUST:** <the minimum that makes this valuable>
- **SHOULD:** <valuable, can slip to the next cycle without breaking the story>
- **OUT OF SCOPE:** <things mentioned or tempting that will NOT be done now, and why>

## 4. Approach options (the user decides)
| Option | How | Pros | Cons | Effort | Ladder rung |
|:--|:--|:--|:--|:--|:-:|
| A | | | | | |
| B | | | | | |

**Agent recommendation:** <A/B, why>
**User decision:** <filled when decided, mirror to decisions.md>

## 5. Reuse (Ponytail check)
- Existing assets to reuse: <tables, models, dashboards, functions, docs>
- New dependencies / tools / infra: <none | name + justification>

## 6. Stories
### S1: As <role>, I want <capability> so that <outcome>.
- Given <...>, when <...>, then <...>
- <data check>: <threshold>

## 7. Risks & pre-mortem
> "It's 6 weeks from now and this failed. Why?"
| Risk | Likelihood | Impact | Mitigation / early signal | Owner |
|:--|:-:|:-:|:--|:--|

## 8. Dependencies on the client
- <access, data, people, decisions we need from them, by when>

## Gate 2
- [ ] Approach chosen by the user
- [ ] Scope approved by the user (and by the client if it changes what was played back)

## Change log
- <YYYY-MM-DD> <change, why, who agreed>
