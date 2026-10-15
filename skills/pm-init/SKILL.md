---
name: pm-init
description: >-
  Set up private OpenPM workspace (profile, folders, git) or add new
  client. Trigger on pm-init, "set up OpenPM", "add a client", or
  workspace not found.
---

# pm-init

Read [pm-core](../pm-core/SKILL.md) first.

## Mode A: create workspace (workspace missing)

1. Ask target path. Default: `~/pm-workspace`. Confirm path.
2. Create folder tree per [workspace.md](../pm-core/references/workspace.md): `clients/`, `journal/daily/`, `journal/weekly/`, `sprints/`, `conversations/`.
3. Copy [workspace-AGENTS.md](../pm-core/templates/workspace-AGENTS.md) to `AGENTS.md` at workspace root.
4. **Profile interview.** Ask in **single** message. Blank values keep template defaults:
   role, timezone, working hours, weekly capacity, focus hours, sprint length, weekly review day, delegation contacts, update tone, language(s).
   Write answers to `me.md` using [me.md](../pm-core/templates/me.md).
5. Persist path:
   `mkdir -p ~/.config/openpm && echo "<path>" > ~/.config/openpm/workspace`.
6. `git init`. Create `.gitignore` ignoring `.DS_Store` and `.lavish/`. First commit.
7. Offer (never auto-run) private GitHub repo push:
   `gh repo create <name> --private --source . --push`. Warn: contains client data.
8. Run Mode B for first client.

## Mode B: add client

1. Ask: client name, short uppercase code (suggest one), contract type, meeting cadence, stakeholders (name, role, priority), stack, constraints, sensitive items. Or accept pasted email/notes/SOW and parse fields.
2. Create `clients/<slug>/` with `client.md`, `roadmap.md`, `decisions.md` (from templates), plus `inbox/`, `initiatives/`, `updates/`.
3. Save raw input: `inbox/<YYYY-MM-DD>-onboarding.md`.
4. Populate known facts. Leave `<placeholders>` for gaps. List missing items for user. Never invent data.
5. Next step: suggest `pm-intake` on first request.

## Done when
- `python3 ../pm-core/scripts/pm_scan.py --lint` runs without "No OpenPM workspace found".
- Client folder exists; `client.md` contains `code`.
