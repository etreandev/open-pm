---
name: pm-weekly
description: >-
  Run cross-client weekly review: planned vs done, slips, client health, wins,
  lessons, next week outcomes, relationship follow-ups, and update drafts.
  Trigger on pm-weekly or weekly review day.
---

# pm-weekly: cross-client weekly review

Read [pm-core](../pm-core/SKILL.md), [prioritization.md](../pm-core/references/prioritization.md), and [style.md](../pm-core/references/style.md) (terse chat output).

## Steps

1. **Ingest weekly inputs:** current `journal/daily/*`, `pm_scan.py --json --all` output, `git -C <workspace> log --since="7 days ago" --oneline`, client `client.md`/`roadmap.md` files, `priorities.md`.
2. **Scoreboard:** planned vs delivered; committed deadlines preserved vs missed. If slipped date wasn't communicated to client: prioritize immediate outreach.
3. **Assess client health:** suggest green/yellow/red per client with single-line reason based on slips, blockers, sentiment, update cadence. Obtain user confirmation; record in `client.md` health log.
4. **Wins and retros:** translate wins to business value (for client updates). For failures: identify root causes and specific process adjustment. Flag repeat estimation errors.
5. **Target next week:** check capacity vs demand. Max 2 milestone-linked outcomes per client. If capacity exceeded: apply overload levers from `prioritization.md`.
6. **Stakeholder follow-ups:** identify stale contacts (> 2 weeks), champions to acknowledge, skeptics needing alignment, or networking goals from `me.md`.
7. **Draft updates:** run `pm-update` for clients due on cadence; save to `updates/`.
8. **Artifact:** save `journal/weekly/<YYYY-Www>.md` via [weekly.md](../pm-core/templates/weekly.md).
9. **Chat output (max 2 screens):** scoreboard, health table, next week outcomes, required decisions, drafted update links.
10. Trigger suggestions: `pm-roadmap all` if milestones shifted; `pm-tough-conversation` if client marked red.
