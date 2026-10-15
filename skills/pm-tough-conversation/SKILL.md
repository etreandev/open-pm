---
name: pm-tough-conversation
description: >-
  Prepare for difficult conversations (deadlines, incidents, scope, saying no,
  budget, feedback) with script, objection handling, rehearsal, and debrief.
  Trigger on pm-tough-conversation or dreaded conversation.
---

# pm-tough-conversation: prepare, rehearse, debrief

Read [pm-core](../pm-core/SKILL.md) and [playbooks.md](references/playbooks.md).

## Prepare

1. **Intake:** stakeholder, incident/event, timestamp, channel, user goal. Pull existing context: `client.md` (stakeholder profile, landmines), tasks, decisions, recent updates. Prompt user only for unrecorded facts.
2. Populate [conversation.md](../pm-core/templates/conversation.md); save to `conversations/<YYYY-MM-DD>-<slug>.md`:
   - **Objective:** single sentence covering outcome and relationship preservation.
   - **Facts vs stories:** isolate verifiable reality from interpretations (user and client).
   - **Their side:** incentives, perceived risk, emotional state, assumptions.
   - **What we own:** direct ownership; active voice; no over-apologizing.
   - **Opening script:** verbatim 30–60 second monologue (frame issue, own responsibility, invite collaboration).
   - **Key messages:** max 3 points.
   - **Options:** cost to us vs value to counterpart. Explicit boundary lines. Never offer unauthorized concessions. Prompt user for hard limits.
   - **Objections:** 4–6 anticipated pushbacks structured as acknowledge → answer → redirect.
   - **Inquiries and close:** verbal confirmation points and draft written recap.
3. **Chat output:** objective, opening script, 3 core messages, options/limits, 3 top objections. Offer simulation.

## Rehearse (optional, recommended)

- Role-play counterpart using profile. Challenge user realistically; avoid fast capitulation. Remain in character until user says "stop".
- Post-simulation feedback (3 points): effective arguments, defensive/unclear points, concrete line replacement.
- Optional stress test: simulate escalated hostility or senior executive escalation.

## Debrief (post-meeting)

1. Collect outcomes and explicit agreements.
2. Complete journal debrief. Convert commitments to tasks with assigned owner and `committed: true` for deadlines. Record entries in `decisions.md`; update `client.md` health/stance.
3. Draft written confirmation message.

## Rules
- Demand radical candor. Never spin, deflect, or scapegoat colleagues.
- If legal, HR, or contract exposure emerges: instruct user to escalate to manager, legal counsel, or HR.
