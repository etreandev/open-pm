# Review Loop

This reference describes how `pm-view` translates visual reviewer feedback from Lavish Editor
into workspace markdown changes.

## Markdown is the Source of Truth

The HTML artifacts in `.lavish/` are generated views. Never manually edit the HTML files.
All changes are applied to the markdown files in `clients/` and re-rendered.

```
Visual browser (Lavish)
  │ (annotations, quick edit batch, whiteboard edits)
  ▼
lavish-axi poll
  │
  ▼
Agent edits workspace markdown in place
  │
  ▼
pm_scan.py --lint
  │
  ▼
pm_render.py (re-renders .lavish/)
  │
  ▼
Browser live-reloads automatically
```

---

## Feedback Types and Handling

### 1. Quick Edit Batches (`tag: "tracked-batch"`)
Submitted from the "Quick edit" table on project pages.
- The payload contains `data.items`, where each item has `{ id, file, line, changes }`.
- `changes` maps task field names (`status`, `owner`, `estimate`, `due`, `note`) to new values.
- Edit the corresponding task block in `tasks.md` in place.
  - If `status` changes to `blocked` and a note is provided, set `- blocked_by: <note>`.
  - If `status` changes from `blocked` to `todo` or `doing`, remove or clear `blocked_by`.
- Return an item-by-item receipt acknowledging every submitted ID.

### 2. Task Card Annotations (`id="<CODE>-<NNN>-<NN>"`)
When the user comments on a task card:
- **Estimate change:** e.g. "make this 1h" → update `- estimate: 1h`. If > 4h, split into atomic tasks.
- **Owner reassignment:** e.g. "delegate to Sam" → update `- owner: Sam`.
- **Done when clarification:** e.g. "done when staging model passes all tests" → update `- done_when: ...`. Keep ≤ 25 words per [style.md](../../pm-core/references/style.md).
- **Add dependency:** e.g. "depends on 01" → update `- depends_on: ...`.
- **Drop / Cancel:** update `- status: dropped`.

### 3. Milestone Annotations (`id="M<n>"`)
When the user comments on a milestone card:
- Updates target date, status (`on track`, `at risk`, `late`), or the "After Mn" capability line in `roadmap.md`.
- Add a dated entry to `## Change log` in `roadmap.md` explaining what changed.

### 4. Whiteboard / Dependency Edits (`tag: "whiteboard"`)
When the user edits the Mermaid dependency graph whiteboard:
- Read the edit summary in the prompt.
- Added edge `A --> B`: add `A` to `B`'s `depends_on` list in `tasks.md`.
- Removed edge `A --> B`: remove `A` from `B`'s `depends_on` list.
- Check for dependency cycles before writing.

### 5. Plan / Spec Annotations (`id="plan"`, `id="S<n>"`)
- Scope modifications or metric adjustments in an approved spec:
  - Do NOT modify approved specs silently.
  - Record the change in the spec's `## Change log`.
  - If changing MUST scope or approach, verify Gate 2 approval with the user.

---

## Session Lifecycle

1. Start review:
   ```bash
   lavish-axi <path-to-html>
   ```
2. Wait for feedback in the foreground:
   ```bash
   lavish-axi poll <path-to-html>
   ```
3. When feedback arrives, apply edits, run lint:
   ```bash
   python3 skills/pm-core/scripts/pm_scan.py --lint
   ```
4. Re-render:
   ```bash
   python3 skills/pm-core/scripts/pm_render.py --workspace <ws> --out <ws>/.lavish
   ```
5. Reply and wait for next round:
   ```bash
   lavish-axi poll <path-to-html> --agent-reply "<Concise receipt of changes>"
   ```
6. Exit when:
   - Poll returns `ended` or `browser_disconnected`.
   - User says "done", "looks good", or asks to proceed to execution.
