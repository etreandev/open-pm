# Prioritization

There are two tools for two time scales. Both have to be explainable in one
sentence per item. If you can't explain a ranking, it's wrong.

## 1. Triage tiers (today / this week)

Used by `pm-daily` and as the default sort order of `pm_scan.py`. Go top-down.
Inside a tier, sort by due date, then smallest estimate.

| Tier | Rule | Why |
|:-:|:--|:--|
| 0 | **Committed and overdue or due today**; production or data incidents | Trust is the scarcest resource |
| 1 | Committed and due within 2 days | Same, with a little slack |
| 2 | **Unblocks others**: open tasks depend on it | One hour of yours frees many hours of theirs |
| 3 | **Lead tasks** (`owner: me`, type `comms`/`decision`/`resource`/`network`) | Only the user can do these, and they're usually the bottleneck |
| 4 | Already `doing` | Finish before you start something new (limit work in progress) |
| 5 | Due within 7 days | |
| 6 | Everything else that is actionable | |
| — | Waiting (dependencies not done) or `blocked` | Not actionable. Show the blocker and who can clear it |

## 2. WSJF-lite (backlog / sprint / roadmap)

Used by `pm-prioritize` and `pm-sprint` to rank **initiatives or stories**,
not individual tasks.

```
score = (Value + Time-criticality + Risk-reduction) / Size
```

Score each factor 1, 3, or 5. Use the extremes only when you can name the reason.

- **Value**: how much it moves a success metric the client cares about.
- **Time-criticality**: what it costs to wait (deadlines, seasonality, a
  dependent team waiting, a contract milestone).
- **Risk-reduction**: does it resolve a big unknown, or enable other work?
  Early spikes score high here.
- **Size**: total estimate (1 = ≤1 day, 3 = ≤1 week, 5 = more than 1 week).

Show the table with the factor scores, so the user can disagree with a factor
instead of arguing with the result.

## 3. Capacity check (always)

- Read `capacity_hours_per_week` and `focus_ratio` from `me.md`. The default
  focus ratio is 0.6, because meetings and interruptions are real.
- Available hours = capacity × focus ratio.
- If committed hours exceed available hours, **say so first** and propose
  options:
  1. Drop or defer (name exactly what).
  2. Delegate (to an agent or a person; name who).
  3. **Renegotiate** a date or scope with the client. Offer to run
     `pm-tough-conversation` to prepare.
- Never quietly hide overload by squeezing the estimates.

## Multi-client fairness

If one client takes more than 60% of the available hours in a week, point it
out. Ask the user whether that matches the contract or what's commercially
important. Don't fix it on your own.
