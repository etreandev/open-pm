---
name: pm-update
description: >-
  Drafts a client or stakeholder status update that translates technical
  progress into business outcomes, with explicit asks and risks, adapted to
  the audience (sponsor, working team, exec) and channel (email, Slack,
  talking points). Use when the user runs pm-update or asks to write a status
  update, a demo summary, or release notes for a client.
---

# pm-update: say what changed for them, not what we did

Read [pm-core](../pm-core/SKILL.md).

## Steps

1. Identify the client, audience, channel, and period. Use the defaults from
   `client.md` (cadence, stakeholder preferences) and `me.md` (tone,
   language). Ask only if one is ambiguous.
2. Collect: tasks done in the period (`pm_scan.py --client <slug> --json
   --all`), roadmap milestone status, `decisions.md` entries in the period,
   open lead tasks that need something from the client, and the previous
   update (for continuity).
3. **Translate.** Every item answers "what can they do now, or what risk is
   gone?" For example, "Optimized the incremental model" becomes "The daily
   revenue report is now ready by 7am instead of 11am."
4. **Consistency check:** this update must not contradict the roadmap or the
   previous update. If the status changed (for example, a milestone is now at
   risk), say so near the top. Don't bury it.
5. **Asks:** each one is specific, has a date, and says what it unblocks.
6. **Adapt to the audience:**
   - Exec: 5 lines max. Status, headline, decision needed.
   - Sponsor: use the full template.
   - Working team: more detail is fine. You can mention task IDs.
7. Save to `clients/<slug>/updates/<YYYY-MM-DD>-<audience>.md` from
   [update.md](../pm-core/templates/update.md) with `status: draft`, and show
   the draft in chat. **The user sends it.** When they confirm it's sent, set
   `status: sent`.

## Rules
- No jargon in client-facing text unless the audience is technical.
- Bad news goes first and comes with a plan: what happened, impact, what we're
  doing, and what we need. If it's serious, suggest `pm-tough-conversation`
  before sending.
- Don't round up progress. "80% done" is not allowed. Say which milestones
  are done and which aren't.
