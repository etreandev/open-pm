---
name: pm-roadmap
description: >-
  Build or review client narrative roadmap (Now / Next / Later, Not doing).
  Verify task, milestone, spec, and update consistency. Trigger on pm-roadmap,
  client progress inquiry, or quarter review.
---

# pm-roadmap: coherent client narrative

Read [pm-core](../pm-core/SKILL.md), [planning-standards.md](../pm-core/references/planning-standards.md) ("Narrative consistency"), and [style.md](../pm-core/references/style.md) (single-line capability format).

## Steps

1. Select client. Clarify if ambiguous, or select `all` for portfolio review.
2. Inspect: `roadmap.md`, all `initiatives/*/spec.md`, un-specced `brief.md` files, latest update in `updates/`. Run:
   `python3 ../pm-core/scripts/pm_scan.py --client <slug> --json --all`.
3. **Audit consistency (rank by severity):**
   - Orphan tasks (no milestone) or hollow milestones (no tasks).
   - Milestones where remaining hours exceed capacity before target date (reference `me.md`).
   - Plumbing-only milestones without visible client capability.
   - Status contradictions: latest update promised X, roadmap/tasks indicate Y.
   - Alignment debt: briefs pending validation > 7 days.
   - Scope creep: SHOULD items converted to tasks without approval.
4. **Sync `roadmap.md`:** update milestone status (`on track`, `at risk`, `late`), adjust Now/Next/Later tiers, refresh "The story in one paragraph", record dated `## Change log`. Never alter target dates or commitments without user approval.
5. **Chat output:** story paragraph, milestone table (name, target, status, remaining hours), top discrepancies with proposed fixes.

## Portfolio view (`all`)
Display table: client health, active milestone, milestone status, next committed deadline, monthly hours remaining, primary risk. Highlight single client requiring immediate intervention.
