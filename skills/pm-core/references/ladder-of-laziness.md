# The Ladder of Laziness (PM edition)

Adapted from [Ponytail](https://github.com/DietrichGebert/ponytail)'s 7-rung ladder.
Ponytail applies it to code. OpenPM applies it earlier, to **requirements**,
before any ticket exists. The cheapest work is the work you talk the client
out of, as long as their real problem still gets solved.

Climb from rung 1. **Stop at the first rung that solves the underlying need.**
Write the verdict in the brief like this: `ladder: rung N — <one-line reason>`.

| # | Rung | Question | Typical data-team example |
|:-:|:-----|:---------|:--------------------------|
| 1 | **Does it need to exist?** | What decision or outcome does this serve? Who acts on it, and how often? | "A daily dashboard" that someone looks at once a quarter → a quarterly export |
| 2 | **Already exists?** | Does an existing report, table, model, query, or past initiative already answer it? | The KPI is already in the finance mart under a different name |
| 3 | **Process, not software?** | Would a conversation, a doc, a definition, or a manual step solve it? | Two teams disagree on "active customer" → a definitions doc and one meeting, not a new pipeline |
| 4 | **Configuration / native feature?** | Can a setting in the BI tool, warehouse, dbt, or orchestrator do it? | Scheduled email from the BI tool instead of a custom alerting service |
| 5 | **Extend what exists?** | Can we add a column, filter, model, or parameter to something that already exists? | Add a `region` dimension to the existing model |
| 6 | **Smallest new thing** | What is the minimum that proves value? (one-off analysis, notebook, MVP) | One-off analysis to check the hypothesis before building a pipeline |
| 7 | **Full build** | Only now do a full spec and breakdown. | New ingestion + modelling + serving layer |

## Rules

- **Lazy, not negligent.** No rung may skip security, privacy/PII handling,
  data-quality checks, or access controls. These are guardrails, not scope.
- Rungs 1 and 3 usually mean **the user has to talk to the client**. Draft the
  message. Don't decide for them.
- If you don't have enough context to rule out a rung (for example, you can't
  see the client's existing reports), write that down as an open question.
  Don't assume the rung fails.
- New dependencies, tools, or infrastructure need an explicit written
  justification in the spec.
