---
name: pm-init
description: >-
  Sets up the private OpenPM workspace (profile, folders, git) or adds a new
  client to it. Use when the user runs pm-init, says "set up OpenPM", "add a
  client", or when another pm-* skill can't find a workspace.
---

# pm-init

Read [pm-core](../pm-core/SKILL.md) first.

## Mode A: create the workspace (no workspace found)

1. Ask where to put it. The default is `~/pm-workspace`. Confirm the path.
2. Create the layout from
   [workspace.md](../pm-core/references/workspace.md): `clients/`,
   `journal/daily/`, `journal/weekly/`, `sprints/`, `conversations/`.
3. Copy [workspace-AGENTS.md](../pm-core/templates/workspace-AGENTS.md) to
   `AGENTS.md` at the workspace root.
4. **Profile interview.** Ask these in **one** message and accept short
   answers. Anything left blank keeps the template default:
   role, timezone, working hours, weekly capacity, how much of it is real focus
   time, sprint length, weekly review day, people you can delegate to, update
   tone, and language(s).
   Write the answers to `me.md` using [me.md](../pm-core/templates/me.md).
5. Save the path so every skill and the scanner can find it:
   `mkdir -p ~/.config/openpm && echo "<path>" > ~/.config/openpm/workspace`.
6. Run `git init`. Add a `.gitignore` that excludes `.DS_Store` and `.lavish/`. Make the
   first commit.
7. Offer (don't do it automatically) to push it as a **private** GitHub repo:
   `gh repo create <name> --private --source . --push`. Remind the user that
   it will contain client data.
8. Continue with Mode B for their first client.

## Mode B: add a client

1. Ask for: client name, a short uppercase code (suggest one), contract type,
   meeting cadence, stakeholders (name, role, what they care about), stack,
   constraints, and anything sensitive. Offer to take a pasted email, notes, or
   an SOW instead, and extract the answers from it.
2. Create `clients/<slug>/` with `client.md`, `roadmap.md`, `decisions.md`
   (from the templates), plus `inbox/`, `initiatives/`, and `updates/`.
3. Save any pasted raw material to `inbox/<YYYY-MM-DD>-onboarding.md`.
4. Fill in what you know. Leave `<placeholders>` for the rest, and list the
   gaps for the user. Don't make anything up.
5. Suggest the next step: "Run `pm-intake` on their first request."

## Done when
- `python3 ../pm-core/scripts/pm_scan.py --lint` runs without "No OpenPM
  workspace found".
- The client folder exists, and its `client.md` has a `code`.
