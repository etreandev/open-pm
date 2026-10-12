# Planning Standards

## Success metrics: always three kinds

Every spec defines at least one of each. If you can't, the requirement isn't
understood yet, so go back to `pm-intake`.

| Kind | Question | Example |
|:--|:--|:--|
| **Outcome** (business) | What changes for the client, and how will we know? | Finance closes the month in 3 days instead of 6 |
| **Output** (deliverable acceptance) | What exactly do we hand over, and what must be true about it? | Revenue mart reconciles to the GL within 0.5% for the last 3 closed months |
| **Guardrail** | What must not get worse? | Pipeline runtime < 30 min; warehouse cost +10% max; no PII in the BI layer |

Each metric has a **baseline** (or `unknown — task to measure`), a **target**,
and a **way to measure it**. "Improve", "faster", and "better" are not
metrics.

## Stories

```
S<n>: As <specific role at the client>, I want <capability> so that <outcome tied to a metric>.
Acceptance:
  - Given <context>, when <action>, then <observable result>
  - (data work) <check>: <threshold>   e.g. "freshness: < 2h behind source at 08:00"
```

- A story describes a capability the client gets, not a technical layer. Wrong:
  "Build staging models". Right: "As the FP&A analyst, I want daily revenue by
  region so that I stop rebuilding it in Excel".
- Keep it to 3–7 stories per spec. More than that means you should split the
  initiative.

## Atomic tasks

A task is atomic when **all** of these are true:

1. **≤ 4h** of focused work (ideally ≤ 2h). Bigger → split.
2. **One owner** and **one binary `done_when`** that someone other than the
   doer could verify.
3. **Inputs are in hand.** If it needs access, data, a decision, or a person
   that isn't available yet, that need becomes its own task with `owner: me`
   (type `resource`/`decision`/`comms`), and the build task `depends_on` it.
4. **Unknowns are spikes.** If you can't estimate it, create a `spike` with a
   timebox (≤ 2h) and the exact question it has to answer.
5. **Traceable.** Every task has a `story` and a `milestone`. If a task serves
   no story, either the spec is missing something or the task is scope creep.
   Ask which.
6. For code work, keep it to 1–3 files per task. For data work, one model,
   pipeline step, dashboard, or analysis question per task.

## Narrative consistency

The roadmap is a story the client can retell. Each milestone is phrased as
**"After M<n>, <who> can <do what> that they couldn't before."** Run these
checks when you write or revise a plan:

- No task without a milestone. No milestone without tasks.
- Milestones are in order, and each one delivers usable value on its own.
  Avoid "M1: all the plumbing".
- What the latest client update said matches the roadmap. If it doesn't,
  flag the gap.
