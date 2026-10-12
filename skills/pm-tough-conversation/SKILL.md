---
name: pm-tough-conversation
description: >-
  Prepares the user for a difficult conversation (missed deadline, incident or
  failure, angry client, scope pushback, saying no, budget, or feedback to a
  teammate) with an objective, facts vs stories, their side, an opening
  script, options, pushback responses, and an optional role-play rehearsal,
  then records the debrief. Use when the user runs pm-tough-conversation or
  dreads an upcoming conversation.
---

# pm-tough-conversation: prepare, rehearse, debrief

Read [pm-core](../pm-core/SKILL.md). For playbooks by type of conversation,
read [playbooks.md](references/playbooks.md).

## Prepare

1. **Quick intake:** who, what happened, when the conversation is, the
   channel, and what the user wants. Collect the context yourself:
   `client.md` (stakeholder row, landmines), relevant tasks, decisions, and
   recent updates. Ask only for what you can't find.
2. Fill in [conversation.md](../pm-core/templates/conversation.md) and save it
   to `conversations/<YYYY-MM-DD>-<slug>.md`:
   - **Objective:** one sentence that covers both the outcome *and* the
     relationship.
   - **Facts vs stories:** separate what is verifiable from the
     interpretations, both the user's and the client's.
   - **Their side:** what they're measured on, how they likely feel, what
     they fear, and what they believe happened.
   - **What we own:** said plainly, with no passive voice and no excessive
     apologizing.
   - **Opening:** 30–60 seconds, word for word. It should state the topic,
     own our part, and say what the user wants to achieve together.
   - **Key messages:** at most 3.
   - **Options:** list them with the cost to us and the value to them. Mark
     the user's limits. **Don't commit to anything the user hasn't
     approved.** Ask the user for their limits.
   - **Pushbacks:** the 4–6 most likely, each answered with acknowledge →
     answer → redirect.
   - **Questions to ask** and the **close** (next steps to confirm out loud),
     plus a draft follow-up message.
3. In chat, show: the objective, the opening, the 3 messages, the options and
   limits, and the 3 hardest pushbacks. Offer a rehearsal.

## Rehearse (optional, recommended)

- Play the other person realistically, using their stakeholder profile. Push
  back the way they would, and don't give in easily. Stay in character until
  the user says "stop".
- Afterwards, give 3 bullets of feedback: what landed, where the user got
  defensive or vague, and one line to rephrase.
- Offer a "harder mode" where the other person is angrier or more senior.

## Debrief (after the conversation)

1. Ask what happened and what was agreed.
2. Fill in the Debrief section. Turn every commitment into a task with an
   owner and `committed: true` when it's a date. Log any decisions, and update
   the health and stakeholder stance in `client.md`.
3. Draft the follow-up message that confirms the agreements in writing, if it
   hasn't been sent yet.

## Rules
- Coach toward honesty. Never help spin, mislead, or shift blame onto
  teammates.
- If the situation involves legal, HR, or contract liability, say that the
  user should involve the right person (their manager, legal, or HR).
