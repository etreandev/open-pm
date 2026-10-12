# Critique of the original design notes

These notes review the design documents in [archive/](archive/) (the Gemini
conversation and the four seed docs) and explain what OpenPM v1 changes and
why.

## What the originals got right (kept)

| Idea | Where it lives now |
|:--|:--|
| Spec-driven work: no work starts without a written spec | Gates 1 and 2 in [operating-model.md](../skills/pm-core/references/operating-model.md) |
| An explicit **OUT OF SCOPE** list | `spec.md` scope section, mirrored to the roadmap's "Not doing" |
| Ladder of Laziness / YAGNI | Moved earlier, to requirement time: [ladder-of-laziness.md](../skills/pm-core/references/ladder-of-laziness.md) |
| Atomic tickets with a Definition of Done | The `done_when` field plus 6 atomic rules in [planning-standards.md](../skills/pm-core/references/planning-standards.md) |
| Automated pre-mortem | Required section in `pm-spec` |
| Stakeholder Translator (role 5) | `pm-update` |
| Keep the PM context separate from the coding agent's context | `owner: agent` tasks must make sense on their own |
| Files in a `.pm/` folder that agents read | A dedicated private workspace (see below) |

## What was missing or wrong (changed)

### 1. It solved a different problem than the one you have
The originals are a **code-delivery pipeline**: requirement → spec → tickets
for a programmer. What you actually asked for has three more dimensions:

- **Time scales:** daily, weekly, sprint, prioritize. The originals had no
  notion of *when* anything happens, no capacity, and no prioritization
  model. → Added `pm-daily`, `pm-weekly`, `pm-sprint`, `pm-prioritize`, the
  triage tiers, WSJF-lite, and a mandatory capacity check.
- **People:** tough conversations, stakeholder maps, follow-ups, networking.
  These were absent. → Added `pm-tough-conversation` (prep, rehearsal,
  debrief), the stakeholder table in `client.md`, and the people section in
  `pm-weekly`.
- **Multiple clients:** a per-repo `.pm/` folder can't answer "what should I
  do today across all my clients?" → One private workspace with
  `clients/<slug>/` folders.

### 2. The Python/LangChain orchestrator broke its own Ladder of Laziness
The builder instructions asked for a Python orchestrator (LangChain, AutoGen,
or raw API calls) that runs the roles in sequence. Run that through rung 2,
"already exists?": your coding agent (Claude Code, Antigravity) **already is**
an orchestrator, with tools, file access, memory, and slash commands. Building
another one means API keys, prompt plumbing, and a UI to maintain, and it
gives you a worse chat experience. → OpenPM is **skills (markdown) plus one
small stdlib script**, used only where determinism matters (ranking and
linting).

### 3. No alignment step with the client
The flow went from "raw requirement" straight to "strict spec". It never asked
the client "did I understand you?", which is the most valuable thing a lead
does, and it's your job. → `pm-intake` produces ranked, ready-to-paste
questions and a **play-back message**. Gate 1 requires the *client* to
confirm.

### 4. The responsibility split was implicit, and the agent could decide
The Gatekeeper role was told to "define what will and won't be done". In your
model, **you** decide the solution. → Agents draft 2–3 options with
trade-offs and a recommendation, you decide, and the decision is logged in
`decisions.md`. Breakdowns also generate **lead tasks** for you (comms,
decisions, resources, networking), so your work becomes visible and gets
prioritized too.

### 5. No success metrics
The template had a "business objective" but no measurable success. → Every
spec needs **outcome, output, and guardrail** metrics, each with a baseline,
target, and measurement method. An unknown baseline becomes a spike task.

### 6. No narrative
Tickets weren't tied to anything the client would recognize. → Stories are
written as client capabilities, milestones are phrased as "After M1, <who>
can <do what>…", and every task carries `story` and `milestone`. `pm-roadmap`
checks for orphans and for contradictions with past updates.

### 7. Code-centric ticket rules didn't fit data work
"Touches 1–3 files" and "a PR that adds a table" don't describe dbt models,
pipelines, reconciliations, or analyses. Data work is also dominated by
*unknowns* (access, data quality, definitions). → Atomic rules now cover data
work, unknowns become timeboxed **spikes**, missing inputs become lead tasks,
and acceptance criteria include data checks (freshness, reconciliation,
uniqueness) with thresholds. The ladder examples are data-team examples.

### 8. Smaller issues
- **Mixed languages and garbled file names** (`t_cnica`, `especificaci_n`).
  → Files are in English, the agents reply in your language, and the
  originals are archived with clean names.
- **The ladder had 5 rungs; Ponytail has 7.** → OpenPM uses 7, adapted for
  PM work. It adds "process, not software?", which is the most common lazy
  win in data teams.
- **No state model.** Nothing defined statuses, owners, or estimates, so no
  agent could reliably answer "what's in flight?". → A strict task format
  plus `pm_scan.py --lint`.
- **Tickets "must not depend on each other".** That's unrealistic.
  → Dependencies are explicit (`depends_on`), and the critical path is
  calculated.
- **"PR rejection criteria"** belong to code review, not PM. → Deferred to
  a future `pm-review` skill.

## Open questions for you

1. **Repo map / cartographer:** the originals wanted a `CONTEXT.md` of each
   client's codebase so the ladder can check rung 2 ("already exists?"). v1
   relies on you or the agent knowing the client's assets. Is it worth adding
   a `pm-context` skill that maps a client repo or warehouse?
2. **Tracker sync:** do any clients make you use Jira or Linear? If so, which
   one first?
3. **Team mode:** v1 assumes one lead with optional delegates. Will other
   PMs share a workspace, or will each have their own?
