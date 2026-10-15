---
initiative: 001-revenue-mart
client: acme-retail
status: approved
brief: ./brief.md
approved: 2026-09-15, Alex
decision: D1 in decisions.md
---

# Spec - Revenue mart

## 1. Objective
Finance gets daily net revenue that ties to the GL. Month-close revenue step drops from days to hours.

## 2. Success metrics
| Kind | Metric | Baseline | Target | How measured |
|:--|:--|:--|:--|:--|
| Outcome | Revenue close step duration | unknown - ACME-001-03 | ≤ 1 day | Maria's close checklist, October close |
| Output | Mart vs GL monthly totals | n/a | within 0.5%, Jul-Sep | reconciliation query, ACME-001-06 |
| Guardrail | Nightly dbt runtime | 18 min | < 30 min | dbt run logs |

## 3. Scope
- **MUST:** daily net revenue per entity, reconciled to GL.
- **SHOULD:** region dimension for Sales Ops.
- **OUT OF SCOPE:** real-time dashboard (D1); forecasting (not assessed).

## 4. Approach options (the user decides)
| Option | How | Pros | Cons | Effort | Ladder rung |
|:--|:--|:--|:--|:--|:-:|
| A | Real-time streaming dashboard | Intraday data | Nobody acts intraday; high cost | L | 7 |
| B | Daily dbt mart on ERP replica | Solves close; reuses stack | No intraday | M | 5 |

**Agent recommendation:** B. Solves the outcome, reuses Snowflake + dbt.
**User decision:** B (D1, 2026-09-15).

## 5. Reuse (Ponytail check)
- Existing assets to reuse: ERP replica, existing dbt project, Looker.
- New dependencies / tools / infra: none.

## 6. Stories
### S1: As the FP&A analyst, I want daily net revenue that ties to the GL so that I stop rebuilding it in Excel.
- Given a closed month, when I query the mart, then totals match the GL within 0.5%
- freshness: < 2h behind source at 08:00

### S2: As Sales Ops, I want revenue by region so that I can track regional targets.
- Given the region mapping, when I filter by region, then unmapped rows < 1%

## 7. Risks & pre-mortem
> "It's 6 weeks from now and this failed. Why?"
| Risk | Likelihood | Impact | Mitigation / early signal | Owner |
|:--|:-:|:-:|:--|:--|
| Numbers don't tie to GL (repeat of past vendor) | M | H | Reconcile before demo; explain every gap | me |
| ERP access delays | H | M | Ask early; already 2 weeks late | me |

## 8. Dependencies on the client
- ERP replica read access (Tom) - done
- Region mapping spreadsheet (Ana) - before M2

## Gate 2
- [x] Approach chosen by the user
- [x] Scope approved by the user

## Change log
- 2026-09-15 approved, option B
