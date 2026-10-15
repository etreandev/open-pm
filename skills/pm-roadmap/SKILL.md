---
name: pm-roadmap
description: >-
  Builds or reviews a client's narrative roadmap (Now / Next / Later, plus Not
  doing) and checks that tasks, milestones, specs, and recent client updates
  tell one consistent story. Use when the user runs pm-roadmap, asks "where are
  we with <client>", or needs a quarter or roadmap view for a client.
---

# pm-roadmap: one consistent story per client

Read [pm-core](../pm-core/SKILL.md), then the "Narrative consistency" section
of [planning-standards.md](../pm-core/references/planning-standards.md) and
[style.md](../pm-core/references/style.md) (one-line capability statements).

## Steps

1. Pick the client. Ask if it's unclear, or use `all` for a short portfolio
   view.
2. Read `roadmap.md`, all `initiatives/*/spec.md`, the `brief.md` files with
   no spec yet, the latest file in `updates/`, and run
   `python3 ../pm-core/scripts/pm_scan.py --client <slug> --json --all`.
3. **Run the checks**, then list the findings in order of severity:
   - Tasks with no milestone, or milestones with no open or done tasks.
   - Milestones whose remaining hours don't fit before their target date
     (use capacity from `me.md`).
   - Milestones that only deliver plumbing (no capability the client can see).
   - Contradictions: the last update promised X, but the roadmap or tasks say Y.
   - Briefs waiting more than 7 days for validation (alignment debt).
   - SHOULD items that silently became tasks (scope creep).
4. **Update `roadmap.md`:** set the status of each milestone (on track, at
   risk, or late), move items between Now, Next, and Later, and rewrite "The
   story in one paragraph" if it changed. Add a dated `## Change log` line.
   Don't change targets or commitments without asking the user.
5. In chat, show: the story paragraph, the milestone table (name, target,
   status, remaining hours), and the top findings, each with a proposed fix.

## Portfolio view (`all`)
Show one row per client: health, current milestone, its status, next
committed date, hours left this month, and the biggest risk. End with the one
client that needs the most attention and why.
