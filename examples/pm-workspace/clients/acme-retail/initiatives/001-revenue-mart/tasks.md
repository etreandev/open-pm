---
initiative: 001-revenue-mart
client: acme-retail
spec: ./spec.md
updated: 2026-10-09
total_estimate: 15h
critical_path: [ACME-001-04, ACME-001-05, ACME-001-06, ACME-001-09]
---

# Tasks - Revenue mart

## M1 - Trusted daily revenue for Finance

### ACME-001-01 Confirm "net revenue" definition with Maria
- status: done
- owner: me
- type: decision
- estimate: 30m
- story: S1
- milestone: M1
- done_when: definition written in spec.md and confirmed by Maria in writing

### ACME-001-02 Get read access to ERP replica from Tom
- status: done
- owner: me
- type: resource
- estimate: 30m
- story: S1
- milestone: M1
- done_when: service account can SELECT from erp.invoices

### ACME-001-03 Measure current month-close duration (baseline)
- status: todo
- owner: me
- type: spike
- estimate: 1h
- story: S1
- milestone: M1
- done_when: answer to "how many hours does the revenue close step take today?" written in spec.md

### ACME-001-04 Build stg_erp__invoices
- status: doing
- owner: agent
- type: build
- estimate: 2h
- depends_on: ACME-001-02
- story: S1
- milestone: M1
- done_when: dbt build passes for stg_erp__invoices; unique + not_null tests on invoice_id

### ACME-001-05 Build fct_revenue_daily
- status: todo
- owner: agent
- type: build
- estimate: 4h
- due: 2026-10-16
- depends_on: ACME-001-04
- story: S1
- milestone: M1
- done_when: dbt build passes; one row per day per entity; net revenue uses the D1 definition

### ACME-001-06 Reconcile fct_revenue_daily vs GL for Jul-Sep
- status: todo
- owner: me
- type: review
- estimate: 2h
- due: 2026-10-17
- committed: true
- depends_on: ACME-001-05
- story: S1
- milestone: M1
- done_when: monthly totals within 0.5% of GL; differences explained in spec.md

### ACME-001-09 Demo M1 to Finance
- status: todo
- owner: me
- type: comms
- estimate: 1h
- due: 2026-10-20
- committed: true
- depends_on: ACME-001-06
- story: S1
- milestone: M1
- done_when: Maria confirms FP&A can use the mart for the October close

## M2 - Revenue by region

### ACME-001-07 Ask Ana for the region mapping spreadsheet
- status: todo
- owner: me
- type: comms
- estimate: 30m
- story: S2
- milestone: M2
- done_when: mapping file saved to inbox/ with an owner and update frequency

### ACME-001-08 Add region dimension to fct_revenue_daily
- status: todo
- owner: agent
- type: build
- estimate: 2h
- depends_on: ACME-001-07
- story: S2
- milestone: M2
- done_when: every row has a region; unmapped rows < 1% and listed
