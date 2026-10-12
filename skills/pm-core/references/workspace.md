# Workspace

All PM state lives in one private **PM workspace** (a git repo), kept separate
from the OpenPM tool repo. That way `pm-daily` can see every client at once,
and no client data ends up in the public tool repo.

## Locating the workspace (check in this order)

1. The environment variable `$OPENPM_WORKSPACE`.
2. The first line of `~/.config/openpm/workspace` (a path).
3. `~/pm-workspace`, if it exists.
4. If none of these exist, ask the user, then offer to run `pm-init`.

## Layout

```
pm-workspace/
├── AGENTS.md                    # tells any agent this is an OpenPM workspace
├── me.md                        # the user's role, capacity, working hours, preferences
├── priorities.md                # latest ranked list, written by pm-prioritize
├── clients/
│   └── <client-slug>/
│       ├── client.md            # stakeholders, goals, constraints, cadence, health
│       ├── roadmap.md           # narrative roadmap: Now / Next / Later + milestones
│       ├── decisions.md         # decision log (newest first)
│       ├── inbox/               # raw inputs: YYYY-MM-DD-<slug>.md (emails, transcripts, notes)
│       ├── initiatives/
│       │   └── <NNN>-<slug>/
│       │       ├── brief.md     # pm-intake
│       │       ├── spec.md      # pm-spec
│       │       └── tasks.md     # pm-breakdown
│       └── updates/             # YYYY-MM-DD-<audience>.md, drafted by pm-update
├── journal/
│   ├── daily/YYYY-MM-DD.md
│   └── weekly/YYYY-Www.md
├── sprints/YYYY-MM-DD-<name>.md # sprint plan + review
└── conversations/YYYY-MM-DD-<slug>.md   # pm-tough-conversation prep
```

- Every client has a short uppercase `code` in `client.md` (e.g. `ACME`).
- Initiatives are numbered per client: `001`, `002`, …
- Every document starts with YAML frontmatter that includes a `status`.

## Document statuses

| Document | Statuses |
| :--- | :--- |
| brief.md | `draft` → `validated` (client confirmed) · `parked` · `rejected` |
| spec.md | `draft` → `approved` → `done` · `parked` |
| client.md `health` | `green` · `yellow` · `red` |

## Task format (in `tasks.md`)

One `###` block per task. `pm_scan.py` parses these blocks, so keep the keys
exactly as shown.

```markdown
### ACME-001-03 Build stg_orders model
- status: todo            # todo | doing | blocked | done | dropped
- owner: me               # me | agent | <person name>
- type: build             # build | spike | comms | decision | resource | network | review
- estimate: 2h            # 30m | 1h | 2h | 4h  (anything bigger must be split)
- due: 2026-10-15         # optional, ISO date
- committed: false        # true = a date promised to someone; missing it costs trust
- depends_on: ACME-001-01, ACME-001-02   # optional
- blocked_by: waiting on warehouse access from client IT   # required if status is blocked
- story: S1               # the story in spec.md this task serves
- milestone: M1           # the milestone in roadmap.md this task moves forward
- done_when: dbt build passes for stg_orders; row count within 0.5% of source
```

- ID: `<CLIENT_CODE>-<initiative NNN>-<task NN>`.
- When status changes, edit the line in place. Don't rewrite the whole file.
- Small ad-hoc tasks that don't belong to an initiative go in
  `clients/<slug>/initiatives/000-ops/tasks.md` (create it on first use).
- Personal or cross-client tasks use client slug `_internal` with code `INT`.

## Scanner

`scripts/pm_scan.py` is standard-library Python and needs no install. Run it
with `--help` to see the flags. Common calls:

```bash
python3 scripts/pm_scan.py                     # open tasks, all clients, ranked by urgency
python3 scripts/pm_scan.py --owner me          # only the user's tasks
python3 scripts/pm_scan.py --due-within 7      # due in the next 7 days (incl. overdue)
python3 scripts/pm_scan.py --lint              # format problems: missing done_when, estimate > 4h, ...
python3 scripts/pm_scan.py --json              # machine-readable output
```

Trust the scanner's numbers (hours, counts, overdue items) over your own
reading of the files.
