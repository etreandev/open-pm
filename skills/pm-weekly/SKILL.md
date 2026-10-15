---
name: pm-weekly
description: >-
  Runs the weekly review across all clients: planned vs done, commitments kept
  or slipped, client health, wins, lessons, next week's outcomes against
  capacity, people to follow up with, and drafts of client updates. Use when
  the user runs pm-weekly, says "weekly review", or it's their weekly review
  day.
---

# pm-weekly: zoom out once a week

Read [pm-core](../pm-core/SKILL.md),
[prioritization.md](../pm-core/references/prioritization.md), and
[style.md](../pm-core/references/style.md) (terse chat output).

## Steps

1. **Collect the week's data:** this week's `journal/daily/*`, the
   `pm_scan.py --json --all` output (to compare with last week's weekly file),
   `git -C <workspace> log --since="7 days ago" --oneline` if it's a git repo,
   each client's `client.md` and `roadmap.md`, and `priorities.md`.
2. **Scoreboard:** planned vs done, committed dates kept vs slipped. For each
   slip, ask "was the client told?" If they weren't, that becomes the top
   action.
3. **Client health:** propose green, yellow, or red for each client, with a
   one-line reason. Base it on the evidence: slips, blockers, how the latest
   conversations went, and how long since the last update. Ask the user to
   confirm or override, then write it to `client.md` (`health` and the health
   log).
4. **Wins and lessons:** write wins in business language (they go into
   updates). For misses, give the root cause and one change for next week.
   Look for patterns, for example: "estimates for data-access tasks were off
   3× for two weeks in a row".
5. **Next week:** compare capacity with planned hours, and set at most 2
   outcomes per client, each tied to a milestone. If it's over capacity, run
   the overload options from prioritization.md.
6. **People:** list who to follow up with and why: stakeholders who haven't
   been contacted in more than 2 weeks, champions worth thanking, skeptics who
   need a conversation, and networking the user wanted to do (check `me.md`
   goals).
7. **Updates:** for each client where an update is due (per the cadence in
   `client.md`), draft one with `pm-update` and save it to `updates/`.
8. Write `journal/weekly/<YYYY-Www>.md` using
   [weekly.md](../pm-core/templates/weekly.md). In chat, show: the scoreboard,
   the health table, next week's outcomes, decisions needed, and links to the
   drafted updates. Two screens max.
9. Suggest `pm-roadmap all` if any milestone changed status, and
   `pm-tough-conversation` if any client is red.
