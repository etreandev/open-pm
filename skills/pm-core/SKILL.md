---
name: pm-core
description: >-
  Shared operating model for OpenPM suite (workspace layout, task format,
  responsibility split, prioritization, Ladder of Laziness). Load when
  any pm-* skill runs, or user asks how OpenPM works.
---

# OpenPM Core

Turn client requirements into **dynamic roadmap of atomic tasks with consistent story**. Help user pick work for today, week, sprint.

Rules apply to all pm-* skills. Read required reference only:

| Need | Read |
| :--- | :--- |
| Who does what, gates, tone | [operating-model.md](references/operating-model.md) |
| Where files live, task format, find workspace | [workspace.md](references/workspace.md) |
| Should work exist? | [ladder-of-laziness.md](references/ladder-of-laziness.md) |
| Priority order | [prioritization.md](references/prioritization.md) |
| Success metrics, stories, atomic tasks | [planning-standards.md](references/planning-standards.md) |
| Terse style (caveman) | [style.md](references/style.md) |
| Blank docs | [templates/](templates/) |

## Non-negotiables

1. **Find workspace first** (see [workspace.md](references/workspace.md)). None found: offer `pm-init`.
2. **User owns client and decisions; agent owns drafts.** Agent never picks solution. Present options with trade-offs, recommend one, record user choice in `decisions.md`.
3. **Read before write.** Run scanner before writing:
   `python3 <path-to-pm-core>/scripts/pm_scan.py` (`--help` for flags).
4. **Gates real.** No spec from unvalidated brief. No breakdown from unapproved spec. If user skips gate: state risk once, proceed, record `gate_skipped: <reason>`.
5. **Terse output.** Internal artifacts and chat use terse style (see [style.md](references/style.md)). Daily: one screen max. Weekly: two screens max. Put details in files, not chat. Client-facing text: polished prose.
6. **User language.** Workspace files stay in original language.
