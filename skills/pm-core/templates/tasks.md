---
initiative: <NNN>-<slug>
client: <client-slug>
spec: ./spec.md
updated: <YYYY-MM-DD>
total_estimate: <Nh>
critical_path: [<ID>, <ID>, ...]
---

# Tasks - <initiative name>

<!-- Format: see pm-core/references/workspace.md. Keep keys exact; pm_scan.py parses them. -->

## M1 - <milestone name>

### <CODE>-<NNN>-01 <verb-first title>
- status: todo
- owner: me
- type: decision
- estimate: 30m
- story: S1
- milestone: M1
- done_when: <binary, verifiable by someone else>

### <CODE>-<NNN>-02 <verb-first title>
- status: todo
- owner: agent
- type: build
- estimate: 2h
- depends_on: <CODE>-<NNN>-01
- story: S1
- milestone: M1
- done_when: <...>
