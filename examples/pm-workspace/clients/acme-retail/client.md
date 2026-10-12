---
client: Acme Retail
code: ACME
health: yellow
contract: retainer 20h/week
cadence: weekly sync Tue 10:00, async update Fri
started: 2026-09-01
---

# Acme Retail

## Why they hired us (in their words)
"Finance spends a week every month rebuilding revenue numbers in Excel."

## Their goals this quarter
- Close the month in 3 days instead of 6

## Stakeholders (people map)
| Name | Role | Cares about | Influence | Stance | Prefers | Notes |
|:--|:--|:--|:-:|:--|:--|:--|
| Maria | VP Finance (sponsor) | Close speed, audit trail | H | champion | short emails | Presents numbers to the CFO monthly |
| Ana | Sales Ops | Regional targets | M | neutral | Slack | Owns the region mapping spreadsheet |
| Tom | IT manager | Security, access | M | skeptic | tickets | Slow to grant access; burned by a past vendor |

## Constraints
- Access / security: read-only ERP replica, no PII outside the warehouse
- Tech stack: Snowflake, dbt, Looker

## Landmines & history
- A previous vendor delivered revenue numbers that didn't tie to the GL. Trust is fragile.

## Health log (newest first)
- 2026-10-09 yellow - ERP access took 2 weeks; M1 at risk
- 2026-09-01 green - kickoff
