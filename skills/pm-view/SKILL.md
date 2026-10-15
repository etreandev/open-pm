---
name: pm-view
description: >-
  Open visual review of project, client roadmap, or all clients in browser
  via Lavish Editor. Renders plan, milestones, task board, dependency graph.
  Translate feedback to markdown edits in place and re-render.
---

# pm-view: visual review and editing

Read [pm-core](../pm-core/SKILL.md) and [style.md](../pm-core/references/style.md) first.

## Trigger
- User runs `pm-view`, requests visual plan, task board, or browser review.
- After `pm-breakdown` or `pm-roadmap` for visual confirmation.

## Workflow

1. **Scope target:**
   - Single project: `clients/<slug>/initiatives/<NNN>-<slug>` (default if in initiative).
   - Single client: `clients/<slug>` (all projects + narrative roadmap).
   - Portfolio: all clients (`index.html`).
2. **Render HTML:**
   `python3 <pm-core>/scripts/pm_render.py --workspace <ws> --out <ws>/.lavish`
3. **Launch in Lavish:**
   `lavish-axi <target-page.html>`
4. **Review cycle:**
   Run `lavish-axi poll <target-page.html>` in foreground for annotations, quick edits, diagram adjustments.
   Map feedback directly to markdown edits in place (see [review-loop.md](references/review-loop.md)).
5. **Lint and re-render:**
   Run `python3 <pm-core>/scripts/pm_scan.py --lint` and re-render. Loop until user terminates session.

## Detail
Read [review-loop.md](references/review-loop.md) for feedback mapping, gate invariants, and receipt schemas.
