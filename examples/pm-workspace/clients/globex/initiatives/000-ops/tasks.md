# Tasks - Ops (ad-hoc)

## M0 - Keep the lights on

### GLBX-000-01 Send outage RCA to Bob
- status: todo
- owner: me
- type: comms
- estimate: 30m
- due: 2026-10-12
- committed: true
- story: S0
- milestone: M0
- done_when: RCA email sent with impact, root cause, prevention actions and dates

### GLBX-000-02 Lower freshness alert threshold to 2h
- status: blocked
- owner: agent
- type: build
- estimate: 1h
- blocked_by: waiting on Airflow admin rights from Globex IT
- story: S0
- milestone: M0
- done_when: alert fires in staging when the dashboard source is more than 2h stale
