# Agent instructions for the OpenPM repo

This file is for agents working **on** OpenPM itself. Agents *using* OpenPM
should start at [skills/pm-core/SKILL.md](skills/pm-core/SKILL.md).

## Rules
- **Markdown first.** New behaviour is a change to a `SKILL.md`, a reference,
  or a template. Add code only when a result has to be deterministic (for
  example, ranking or linting). Follow the Ladder of Laziness for the repo
  too.
- **Scripts:** use only the Python 3 standard library, with no dependencies.
  Keep them in `skills/<skill>/scripts/`, and cover them in `tests/`.
- **Shared rules live in `pm-core`.** Other skills link to it with relative
  paths (`../pm-core/...`). Don't duplicate rules across skills.
- **Keep SKILL.md files short.** Put the bulk in `references/` (progressive
  disclosure).
- **The task format is a contract.** If you change keys in
  `references/workspace.md`, update `pm_scan.py`, the templates, the example
  workspace, and the tests in the same change.
- **No real client data,** ever. `examples/` is fictional.
- Files are in English. Skills tell the agent to reply in the user's language.

## Checks before you commit
```bash
python3 -m unittest discover -s tests -v
python3 skills/pm-core/scripts/pm_scan.py --workspace examples/pm-workspace --lint
```
