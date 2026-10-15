---
name: pm-update
description: >-
  Draft client status updates converting technical milestones to business outcomes,
  with explicit asks and risks. Adapt to audience and channel. Trigger on pm-update,
  demo summary, or release notes.
---

# pm-update: communicate client impact over internal activity

Read [pm-core](../pm-core/SKILL.md).

## Steps

1. **Parameters:** client, audience, channel, time horizon. Defaults from `client.md` and `me.md`. Ask only if ambiguous.
2. **Collect data:** completed tasks (`pm_scan.py --client <slug> --json --all`), roadmap milestone states, `decisions.md` additions, open lead tasks needing client action, prior update.
3. **Translate to business value:** convert technical work to client capabilities/risk reductions (e.g., "model refactored" → "daily revenue numbers ready 4 hours earlier").
4. **Verify narrative alignment:** update must match roadmap and previous status. Highlight status degradations near top; never bury.
5. **Asks:** concrete request, explicit deadline, affected dependency.
6. **Audience tailoring:**
   - Exec: ≤ 5 lines (status, core takeaway, pending decision).
   - Sponsor: full template schema.
   - Engineering/working team: task IDs and technical specifics permitted.
7. **Artifact:** save `clients/<slug>/updates/<YYYY-MM-DD>-<audience>.md` from [update.md](../pm-core/templates/update.md) (`status: draft`). Display in chat. **User delivers message.** On send confirmation: set `status: sent`.

## Rules
- Ban technical jargon in client prose unless audience technical.
- Deliver negative developments first, coupled with mitigation path (root cause, blast radius, remedy, pending ask). Severe issues: recommend `pm-tough-conversation`.
- Never round progress percentage ("80% complete" banned). Report discrete milestone completion.
