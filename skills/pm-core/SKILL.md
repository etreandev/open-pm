---
name: pm-core
description: >-
  Shared operating model for the OpenPM suite (workspace layout, task format,
  responsibility split, prioritization rules, Ladder of Laziness). Load this
  whenever any other pm-* skill runs, or when the user asks how OpenPM works.
---

# OpenPM Core

OpenPM turns client requirements into a **dynamic roadmap of atomic tasks that
tells a consistent story**, then helps the user decide what to do today, this
week, and this sprint.

Every pm-* skill follows these rules. Read the reference you need, not all of them.

| Need | Read |
| :--- | :--- |
| Who does what, gates, tone | [operating-model.md](references/operating-model.md) |
| Where files live, task format, finding the workspace | [workspace.md](references/workspace.md) |
| Should this work exist at all? | [ladder-of-laziness.md](references/ladder-of-laziness.md) |
| What to do first | [prioritization.md](references/prioritization.md) |
| Success metrics, stories, atomic tasks | [planning-standards.md](references/planning-standards.md) |
| Blank documents | [templates/](templates/) |

## Non-negotiables (summary)

1. **Find the workspace first** (see [workspace.md](references/workspace.md)).
   If there is none, offer to run `pm-init`.
2. **The user owns the client and the decisions; the agent owns the drafts.**
   The agent never decides the solution. It lays out options with trade-offs,
   recommends one, and records the user's decision in `decisions.md`.
3. **Read before you write.** Before you write anything, run the scanner to see
   the current state:
   `python3 <path-to-pm-core>/scripts/pm_scan.py` (add `--help` to see flags).
4. **Gates are real.** Don't write a spec from an unvalidated brief. Don't break
   down an unapproved spec. If the user wants to skip a gate, say once what the
   risk is, then do it and note `gate_skipped: <reason>` in the document.
5. **Short output.** Daily output fits on one screen. Weekly fits on two. Put
   the detail in the files, not in the chat.
6. **Write in the user's language.** Workspace files stay in the language they
   were started in.
