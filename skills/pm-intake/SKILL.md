---
name: pm-intake
description: >-
  Turn raw client input into requirement brief, open questions, Ladder of Laziness verdict,
  and play-back message. Trigger on pm-intake, pasted client request, or "the client wants…".
---

# pm-intake: understand ask, align with client

Read [pm-core](../pm-core/SKILL.md) and [ladder-of-laziness.md](../pm-core/references/ladder-of-laziness.md).

**Goal:** align user and client meaning before planning.

## Steps

1. **Identify client.** Ask if ambiguous. If new client: run `pm-init` Mode B first.
2. **Save raw input** untouched to `clients/<slug>/inbox/<YYYY-MM-DD>-<slug>.md`. Add one-line source header.
3. **Classify (new vs change).** Check `roadmap.md` and existing initiatives:
   - Modifies existing initiative: append to brief/spec `## Change log`, flag scope/date impacts, stop. Suggest `pm-spec` if major change.
   - New initiative: generate `initiatives/<next NNN>-<slug>/brief.md` from [brief.md](../pm-core/templates/brief.md).
4. **Separate facts from assumptions.** Fact needs source. No source: mark assumption.
5. **Find core need.** "What decision enabled, who decides, how often?" If unknown: top open question.
6. **Evaluate ladder.** Start rung 1. Fill table. Early exit permitted with recommendation. Mark "unknown" honestly.
7. **Rank open questions.** Sort by plan impact. Max 7 questions. Phrase for direct copy-paste. Prefer closed or multiple choice.
8. **Draft play-back message.** Section 9. User voice, client language. Structure: *understood → unsure → proposal → confirm by <date>*.
9. **Chat output (only these):**
   - 2-line need summary.
   - Ladder verdict.
   - Top 3 questions.
   - Play-back draft.
   - Brief file path.
10. Set brief `status: draft`. When user confirms client agreement: set `status: validated`, populate `validated:`, suggest `pm-spec`.

## Lead tasks
If user must send play-back, chase answers, or get access: add as `owner: me` tasks in `initiatives/<NNN>-<slug>/tasks.md` (`story: S0`, `milestone: M0`).

## Don't
- No solution/architecture proposals. Belongs in `pm-spec`. User decides.
- Never treat silence as confirmation.
