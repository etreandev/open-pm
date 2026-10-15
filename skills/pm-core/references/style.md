# Terse Style (Caveman-Inspired)

OpenPM favors brevity. Extra words in internal documents waste attention,
crowd the screen, and slow down execution.

> Why use many words when few words do trick. Code, paths, and checks stay exact.

## Scope: Internal vs Client-Facing

| Artifact / Context | Style | Tone |
| :--- | :--- | :--- |
| **Tasks & breakdowns** (`tasks.md`) | Terse | Verb-first, no filler, binary verification |
| **Roadmap narrative & milestones** (`roadmap.md`) | Terse | One-line capability statements ("After Mn, who can do what") |
| **Daily & weekly chat outputs** (`pm-daily`, `pm-weekly`) | Terse | Scan-friendly tables, bullets, top 3 only |
| **Triage & quick edits** | Terse | Direct instructions and diff receipts |
| **Client play-backs** (`pm-intake`) | Normal | Professional, empathetic, clear |
| **Status updates** (`pm-update`) | Normal | Business outcome focused, polished |
| **Tough conversations** (`pm-tough-conversation`) | Normal | Thoughtful, diplomatic, script-ready |

---

## Rules for Internal Artifacts

### 1. Task titles: verb-first, ≤ 8 words
Start with an imperative verb (`Build`, `Confirm`, `Measure`, `Reconcile`, `Ask`, `Fix`).
- **Good:** `Build stg_erp__invoices` (2 words)
- **Good:** `Confirm net revenue definition with Maria` (6 words)
- **Too long:** `Reach out to Maria from Finance in order to clarify and align on what net revenue means` (16 words)

### 2. `done_when`: binary check, ≤ 25 words
One objective condition that another person or test can confirm. No filler phrases like "Ensure that..." or "Successfully...".
- **Good:** `dbt build passes for stg_erp__invoices; unique and not_null tests pass on invoice_id` (12 words)
- **Good:** `monthly totals within 0.5% of GL; differences explained in spec.md` (10 words)
- **Too long:** `Make sure that all the team members agree and that the report runs smoothly and that Maria from the finance team feels comfortable with the numbers.` (24 words, vague)

### 3. Roadmap milestones: capability format
Use the format: **"After M<n>, <who> can <do what> that they couldn't before."**
One single sentence. Focus on what is unlocked, not technical plumbing.

### 4. Drop filler, keep payload exact
- **Drop:** Greetings, pleasantries ("I would be happy to help"), preambles, recaps of what the user just said, conversational padding.
- **Never drop:** Negations (`not`, `never`, `no`, `only`), numbers, units (`h`, `m`, `d`, `%`), task IDs, file paths, and code snippets.
- **Answer first:** Deliver the conclusion, decision, or action in the very first sentence.

### 5. Know when to use full sentences
Use complete sentences when:
- Highlighting critical risks or blockers.
- Explaining irreversible actions (dropping tables, rejecting client scope, terminating contracts).
- The user is confused or asks for rationale.
