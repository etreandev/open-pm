---
name: pm-intake
description: >-
  Turns raw client input (emails, meeting transcripts, notes, tickets, SOWs)
  into a requirement brief with open questions, a Ladder of Laziness verdict,
  and a play-back message the user can send to confirm alignment. Use when the
  user runs pm-intake, pastes a client request, or says "the client wants…".
---

# pm-intake: understand the ask and align with the client

Read [pm-core](../pm-core/SKILL.md), then
[ladder-of-laziness.md](../pm-core/references/ladder-of-laziness.md).

**Goal:** to make sure the user and the client mean the same thing before any
planning starts. Every hour spent here saves a day later.

## Steps

1. **Identify the client.** If it's ambiguous, ask. If the client is new,
   run `pm-init` Mode B first.
2. **Save the raw input** exactly as given to
   `clients/<slug>/inbox/<YYYY-MM-DD>-<slug>.md`, with a one-line header that
   says where it came from.
3. **Check if it's new or a change.** Read `roadmap.md` and the existing
   initiatives.
   - If it changes an existing initiative: add it to that brief or spec's
     `## Change log`, flag the effect on scope and dates, and stop here. If
     the change is big, suggest `pm-spec` to revise.
   - If it's new: create `initiatives/<next NNN>-<slug>/brief.md` from
     [brief.md](../pm-core/templates/brief.md).
4. **Separate what you know from what you're guessing.** Every fact needs a
   source. Anything without a source goes under assumptions.
5. **Find the underlying need.** Ask "what decision does this enable, who
   makes it, and how often?" If the input doesn't answer that, it becomes the
   top open question.
6. **Climb the ladder** from rung 1. Fill in the table. You can stop early
   with a recommendation. Use "unknown" honestly.
7. **Rank the open questions** by how much the answer would change the plan.
   Keep at most 7. Phrase them so they can be pasted straight into a message.
   Prefer closed or multiple-choice questions, which busy clients answer
   faster.
8. **Write the play-back message** (section 9) in the user's voice and the
   client's language. Use the format from `client.md` / `me.md`: *what I
   understood → what I'm unsure about → what I propose → please confirm by
   <date>*.
9. **Show the user, in chat, only this:**
   - A 2-line summary of the need.
   - The ladder verdict.
   - The top 3 questions.
   - The play-back draft.
   - The path to the brief.
10. Leave the brief at `status: draft`. When the user says the client
    confirmed, set `status: validated` and fill in `validated:`. Then suggest
    `pm-spec`.

## Lead tasks
If the user needs to send the play-back, chase answers, or get access, add
those as `owner: me` tasks to `initiatives/<NNN>-<slug>/tasks.md`, with
`story: S0` and `milestone: M0` (discovery). That way `pm-daily` will surface
them.

## Don't
- Don't propose solutions or architecture here. That belongs in `pm-spec`, and
  the user decides.
- Don't treat silence as confirmation.
