---
name: pm-view
description: >-
  Opens a visual review of a project, client roadmap, or all clients in the
  browser via Lavish Editor. Renders plan, milestones, task board, and
  dependency graph. Lets you comment and edit directly, translates feedback
  into markdown edits in place, and re-renders.
---

# pm-view: visual review and editing

Read [pm-core](../pm-core/SKILL.md) and [style.md](../pm-core/references/style.md) first.

## When to run
- The user runs `pm-view`, says "show the plan visually", "open the task board", or "let me review this in the browser".
- After running `pm-breakdown` or `pm-roadmap` when the user wants visual feedback before executing.

## Workflow

1. **Pick the target:**
   - Single project: `clients/<slug>/initiatives/<NNN>-<slug>` (default if working in an initiative).
   - Single client: `clients/<slug>` (groups all projects and shows narrative roadmap).
   - Portfolio: all clients (`index.html`).
2. **Render pages:**
   `python3 <pm-core>/scripts/pm_render.py --workspace <ws> --out <ws>/.lavish`
3. **Open in Lavish:**
   `lavish-axi <target-page.html>`
4. **Review loop:**
   Run `lavish-axi poll <target-page.html>` in the foreground to receive annotations, quick edits, or diagram changes.
   Translate feedback to markdown edits in place (see [review-loop.md](references/review-loop.md)).
5. **Lint and re-render:**
   Run `python3 <pm-core>/scripts/pm_scan.py --lint` and re-render. Repeat until the user ends the review session.

## Detail
Read [review-loop.md](references/review-loop.md) for feedback mapping, gate preservation, and receipt contracts.
