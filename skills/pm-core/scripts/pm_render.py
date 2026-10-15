#!/usr/bin/env python3
"""OpenPM view renderer.

Renders the workspace as static HTML pages for visual review. Open a page
with `lavish-axi <page>` to comment on it and edit it (see the pm-view skill).

  <out>/index.html                        all clients
  <out>/<client>/index.html               one client: roadmap + its projects
  <out>/<client>/<initiative>.html        one project: plan, milestones, tasks, dependencies

<out> defaults to <workspace>/.lavish. The markdown is the source of truth:
pages are regenerated and never edited by hand. Standard library only.
"""
from __future__ import annotations

import argparse
import datetime as dt
import html
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pm_scan  # noqa: E402

BOARD = ["todo", "doing", "blocked", "done"]
ESTIMATES = ["30m", "1h", "2h", "4h"]
CDN = """<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/daisyui@5.5.19/daisyui.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/daisyui@5.5.19/themes.css">
<script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4.2.4/dist/index.global.js"></script>"""
CSS = """*, *::before, *::after { box-sizing: border-box; }
html, body { background: var(--color-base-100); color: var(--color-base-content); }
:where(.grid, .flex) > * { min-width: 0; }
:where(p, h1, h2, h3, h4, li, td, th, .badge) { overflow-wrap: anywhere; }
.md h1 { font-size: 1.5rem; font-weight: 700; margin: 0 0 .75rem; }
.md h2 { font-size: 1.15rem; font-weight: 700; margin: 1.25rem 0 .5rem; }
.md h3 { font-size: 1rem; font-weight: 600; margin: 1rem 0 .4rem; }
.md p, .md ul, .md ol, .md blockquote, .md table, .md pre { margin: 0 0 .75rem; }
.md ul { list-style: disc; padding-left: 1.25rem; }
.md ol { list-style: decimal; padding-left: 1.25rem; }
.md blockquote { border-left: 3px solid var(--color-primary); padding-left: .75rem; opacity: .85; }
.md code { font-family: ui-monospace, monospace; font-size: .85em; }
.md table { width: 100%; border-collapse: collapse; font-size: .875rem; }
.md th, .md td { border: 1px solid var(--color-base-300); padding: .35rem .5rem; text-align: left; vertical-align: top; }
.md a { text-decoration: underline; }
.mermaid { background: var(--color-base-200); border-radius: .75rem; padding: 1rem; }"""
MERMAID = """<script type="module">
  import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11.15.0/dist/mermaid.esm.min.mjs";
  const dark = getComputedStyle(document.documentElement).colorScheme.includes("dark");
  mermaid.initialize({ startOnLoad: false, theme: dark ? "dark" : "default", securityLevel: "strict" });
  const run = () => mermaid.run({ nodes: [...document.querySelectorAll(".mermaid")] });
  if (document.readyState === "complete") run(); else window.addEventListener("load", run, { once: true });
</script>"""
EDIT_JS = """<script>
function openpmQueueEdits(form) {
  const items = [];
  form.querySelectorAll("tr[data-id]").forEach((tr) => {
    const changes = {};
    tr.querySelectorAll("[data-field]").forEach((el) => {
      if (el.value.trim() !== el.dataset.orig) changes[el.dataset.field] = el.value.trim();
    });
    if (Object.keys(changes).length) items.push({ id: tr.dataset.id, label: tr.dataset.label,
      file: tr.dataset.file, line: Number(tr.dataset.line), changes });
  });
  const status = form.querySelector("[data-openpm-status]");
  if (!items.length) { status.textContent = "No changes yet."; return; }
  const prompt = "Apply these task edits to the workspace markdown (edit each task block in place), " +
    "run pm_scan.py --lint, re-render, and return a one-line receipt per ID. Account for every submitted ID.";
  if (window.lavish && window.lavish.queuePrompt) {
    window.lavish.queuePrompt(prompt, { tag: "tracked-batch", element: form, queueKey: "task-edits",
      text: "Edit " + items.length + " task(s): " + items.map((i) => i.id).join(", "), data: { items } });
    status.textContent = "Queued " + items.length + " edit(s). Send to Agent when ready.";
  } else {
    const pre = form.querySelector("[data-openpm-fallback]");
    pre.hidden = false;
    pre.textContent = prompt + "\\n" + JSON.stringify(items, null, 2);
    status.textContent = "Lavish not running. Copy this into the chat.";
  }
}
</script>"""


# ---------- helpers ----------

def esc(s) -> str:
    return html.escape(str(s if s is not None else ""), quote=True)


def slugify(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def split_frontmatter(text: str) -> tuple[dict, str]:
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            meta = {}
            for line in text[3:end].splitlines():
                m = re.match(r"^([A-Za-z_]+):\s*(.*?)(\s+#.*)?$", line)
                if m:
                    meta[m.group(1)] = m.group(2).strip()
            return meta, text[end + 4:].lstrip("\n")
    return {}, text


def doc_title(text: str, prefix: str) -> str | None:
    m = re.search(rf"^#\s+{prefix}\s*-\s*(.+)$", text, re.M)
    return m.group(1).strip() if m else None


# ---------- mini markdown ----------

def inline(s: str) -> str:
    s = html.escape(s, quote=False)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", s)
    return re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)",
                  lambda m: f'<a href="{m.group(2).replace(chr(34), "&quot;")}">{m.group(1)}</a>', s)


def _table(rows: list[str]) -> str:
    cells = [[c.strip() for c in r.strip("|").split("|")] for r in rows
             if not re.fullmatch(r"\|[\s:|-]+\|?", r)]
    if not cells:
        return ""
    head = "".join(f"<th>{inline(c)}</th>" for c in cells[0])
    body = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in cells[1:])
    return f'<div class="overflow-x-auto"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


def _checkbox(s: str) -> str:
    m = re.match(r"^\[([ xX])\]\s*(.*)$", s)
    return (("☑ " if m.group(1).strip() else "☐ ") + inline(m.group(2))) if m else inline(s)


LIST_RE = re.compile(r"^\s*([-*]|\d+\.)\s+")


def md_to_html(text: str, heading=None) -> str:
    """Small, safe markdown subset: headings, lists, tables, quotes, code, paragraphs.

    heading(level, text) -> (id or None, extra html after the heading).
    """
    lines = re.sub(r"<!--.*?-->", "", text, flags=re.S).splitlines()
    out, para, i = [], [], 0

    def flush():
        if para:
            out.append(f"<p>{inline(' '.join(para))}</p>")
            para.clear()

    while i < len(lines):
        s = lines[i].strip()
        if not s:
            flush(); i += 1; continue
        if s.startswith("```"):
            flush(); j, buf = i + 1, []
            while j < len(lines) and not lines[j].strip().startswith("```"):
                buf.append(lines[j]); j += 1
            out.append(f"<pre><code>{esc(chr(10).join(buf))}</code></pre>")
            i = j + 1; continue
        m = re.match(r"^(#{1,6})\s+(.*)$", s)
        if m:
            flush()
            level, title = len(m.group(1)), m.group(2).strip()
            hid, extra = heading(level, title) if heading else (None, "")
            idattr = f' id="{esc(hid)}"' if hid else ""
            out.append(f"<h{level}{idattr}>{inline(title)}</h{level}>{extra}")
            i += 1; continue
        if s.startswith("|"):
            flush(); rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(lines[i].strip()); i += 1
            out.append(_table(rows)); continue
        if LIST_RE.match(s):
            flush(); ordered, items = s[0].isdigit(), []
            while i < len(lines) and LIST_RE.match(lines[i]):
                items.append(LIST_RE.sub("", lines[i], count=1)); i += 1
                while (i < len(lines) and lines[i].startswith("  ") and lines[i].strip()
                       and not LIST_RE.match(lines[i])):
                    items[-1] += " " + lines[i].strip(); i += 1
            tag = "ol" if ordered else "ul"
            out.append(f"<{tag}>" + "".join(f"<li>{_checkbox(it)}</li>" for it in items) + f"</{tag}>")
            continue
        if s.startswith(">"):
            flush(); buf = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                buf.append(lines[i].strip()[1:].strip()); i += 1
            out.append(f"<blockquote>{inline(' '.join(buf))}</blockquote>"); continue
        if re.fullmatch(r"-{3,}|\*{3,}", s):
            flush(); out.append("<hr>"); i += 1; continue
        para.append(s); i += 1
    flush()
    return "\n".join(out)


# ---------- workspace model ----------

def parse_roadmap(text: str) -> tuple[list[dict], dict]:
    """Return (sections, milestones). Sections: [{title, body}], milestones keyed by id."""
    _, body = split_frontmatter(text)
    sections, milestones, current = [], {}, None
    for line in body.splitlines():
        if line.startswith("## "):
            current = {"title": line[3:].strip(), "body": []}
            sections.append(current)
        elif current is not None:
            current["body"].append(line)
    for sec in sections:
        ms = None
        for line in sec["body"]:
            m = re.match(r"^###\s+(M\d+)\s*-\s*(.*)$", line)
            if m:
                parts = [p.strip() for p in m.group(2).split("·")]
                ms = {"id": m.group(1), "name": parts[0], "section": sec["title"], "target": "",
                      "initiative": "", "after": "", "status": "", "metrics": ""}
                for p in parts[1:]:
                    key, _, val = p.partition(" ")
                    if key in ("target", "initiative"):
                        ms[key] = val.strip()
                milestones[ms["id"]] = ms
                continue
            if ms and line.startswith("- "):
                item = line[2:].strip()
                if item.startswith("**"):
                    ms["after"] = item.strip("*").strip()
                elif item.lower().startswith("status:"):
                    ms["status"] = item.split(":", 1)[1].strip()
                elif item.lower().startswith("success metric"):
                    ms["metrics"] = item.split(":", 1)[1].strip()
        sec["body"] = "\n".join(sec["body"]).strip()
    return sections, milestones


def milestone_names(tasks_text: str) -> dict:
    return {m.group(1): m.group(2).strip()
            for m in re.finditer(r"^##\s+(M\d+)\s*-\s*(.+)$", tasks_text, re.M)}


def progress(tasks: list[dict]) -> dict:
    live = [t for t in tasks if t["status"] != "dropped"]
    done = [t for t in live if t["status"] == "done"]
    open_ = [t for t in live if t["status"] in pm_scan.OPEN]
    pct = round(100 * len(done) / len(live)) if live else 0
    return {"total": len(live), "done": len(done), "pct": pct,
            "open_hours": sum(t["hours"] or 0 for t in open_),
            "blocked": sum(1 for t in live if t["status"] == "blocked")}


def load_model(ws: Path, today: dt.date) -> tuple[list[dict], list[dict]]:
    tasks = pm_scan.load(ws)
    pm_scan.enrich(tasks, today)
    clients = []
    for cdir in sorted(p for p in (ws / "clients").glob("*") if p.is_dir()):
        meta, _ = split_frontmatter(read(cdir / "client.md"))
        sections, milestones = parse_roadmap(read(cdir / "roadmap.md"))
        projects = []
        for idir in sorted(p for p in (cdir / "initiatives").glob("*") if p.is_dir()):
            spec, brief, tasks_md = (read(idir / f) for f in ("spec.md", "brief.md", "tasks.md"))
            plan_kind = "spec" if spec else ("brief" if brief else "")
            plan_meta, plan_body = split_frontmatter(spec or brief)
            title = (doc_title(spec, "Spec") or doc_title(brief, "Brief")
                     or doc_title(tasks_md, "Tasks") or idir.name)
            ptasks = [t for t in tasks if t["client"] == cdir.name and t["initiative"] == idir.name]
            tmeta, _ = split_frontmatter(tasks_md)
            crit = [c.strip() for c in tmeta.get("critical_path", "").strip("[]").split(",") if c.strip()]
            projects.append({"slug": idir.name, "title": title, "plan_kind": plan_kind,
                             "plan_status": plan_meta.get("status", ""), "plan_body": plan_body,
                             "tasks": ptasks, "critical": crit, "ms_names": milestone_names(tasks_md),
                             "tasks_file": f"clients/{cdir.name}/initiatives/{idir.name}/tasks.md"})
        clients.append({"slug": cdir.name, "name": meta.get("client", cdir.name), "meta": meta,
                        "sections": sections, "milestones": milestones, "projects": projects,
                        "tasks": [t for t in tasks if t["client"] == cdir.name]})
    return tasks, clients


# ---------- components ----------

def page(title: str, crumbs: list[tuple[str, str | None]], body: str, extra: str = "") -> str:
    nav = "".join(f'<li><a href="{esc(h)}">{esc(t)}</a></li>' if h else f"<li>{esc(t)}</li>"
                  for t, h in crumbs)
    return f"""<!doctype html>
<html lang="en" data-theme="luxury">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
{CDN}
<style>{CSS}</style>
</head>
<body class="bg-base-100 text-base-content min-h-screen">
<main class="mx-auto max-w-7xl p-4 lg:p-8 space-y-8">
<nav class="breadcrumbs text-sm"><ul>{nav}</ul></nav>
{body}
<footer class="text-xs opacity-60 border-t border-base-300 pt-4">Generated by OpenPM <code>pm_render.py</code> from the workspace markdown. Don't edit this page: comment on it, and the agent edits the markdown and re-renders.</footer>
</main>
{extra}
</body>
</html>
"""


def badge(text: str, kind: str = "") -> str:
    return f'<span class="badge badge-sm {kind}">{esc(text)}</span>' if text else ""


def health_badge(h: str) -> str:
    return badge(h or "unknown", {"green": "badge-success", "yellow": "badge-warning",
                                   "red": "badge-error"}.get(h, "badge-ghost"))


def ms_status_badge(s: str) -> str:
    low = s.lower()
    kind = ("badge-error" if low.startswith("late") else "badge-warning" if low.startswith("at risk")
            else "badge-success" if low.startswith("on track") else "badge-ghost")
    return badge(s.split(" - ")[0] if s else "", kind)


def bar(p: dict) -> str:
    return (f'<div class="flex items-center gap-2 text-xs"><progress class="progress progress-primary w-full" '
            f'value="{p["pct"]}" max="100"></progress><span class="whitespace-nowrap">{p["done"]}/{p["total"]} done'
            f' · {p["open_hours"]:g}h left</span></div>')


def stats(items: list[tuple[str, str, str]]) -> str:
    cells = "".join(f'<div class="stat"><div class="stat-title">{esc(t)}</div>'
                    f'<div class="stat-value text-2xl">{esc(v)}</div><div class="stat-desc">{esc(d)}</div></div>'
                    for t, v, d in items)
    return f'<div class="stats stats-vertical md:stats-horizontal bg-base-200 w-full">{cells}</div>'


def task_card(t: dict, critical: set) -> str:
    due = pm_scan.fmt_due(t) if t["days_left"] is not None else ""
    lead = t["owner"] == "me" and t.get("type") in pm_scan.LEAD_TYPES
    badges = "".join([
        badge(t.get("milestone", ""), "badge-outline"),
        badge(t["owner"], "badge-accent" if lead else "badge-ghost"),
        badge(t.get("type", ""), "badge-ghost"),
        badge(t.get("estimate", ""), "badge-ghost"),
        badge(due, "badge-error" if t["committed"] else "badge-warning") if due else "",
        badge("critical path", "badge-primary") if t["id"] in critical else "",
        badge(f'tier {t["tier"]}', "badge-info") if t["tier"] is not None else "",
    ])
    why = t.get("blocked_by") or (("waiting on " + ", ".join(t["waiting_on"]))
                                  if t["waiting_on"] and t["status"] in pm_scan.OPEN else "")
    dim = " opacity-60" if t["status"] in {"done", "dropped"} else ""
    strike = " line-through" if t["status"] == "dropped" else ""
    return f"""<article id="{esc(t['id'])}" data-file="{esc(t['file'])}" data-line="{t['line']}" class="card card-border card-sm bg-base-200{dim}">
<div class="card-body gap-2">
<div class="font-mono text-xs opacity-70">{esc(t['id'])}</div>
<h3 class="card-title text-base{strike}">{esc(t['title'])}</h3>
<div class="flex flex-wrap gap-1">{badges}</div>
{f'<p class="text-sm"><span class="font-semibold">Done when:</span> {esc(t.get("done_when", ""))}</p>' if t.get("done_when") else ""}
{f'<p class="text-sm text-warning">⛔ {esc(why)}</p>' if why else ""}
</div>
</article>"""


def board(tasks: list[dict], critical: set) -> str:
    cols = []
    for status in BOARD:
        group = [t for t in tasks if t["status"] == status or (status == "done" and t["status"] == "dropped")]
        group.sort(key=pm_scan.sort_key if status != "done" else (lambda t: t["id"]))
        cards = "\n".join(task_card(t, critical) for t in group) or '<p class="text-sm opacity-60">None</p>'
        cols.append(f'<div id="col-{status}" class="space-y-3"><h3 class="font-semibold uppercase text-sm '
                    f'tracking-wide">{status} <span class="opacity-60">({len(group)})</span></h3>{cards}</div>')
    return f'<div class="grid gap-4 md:grid-cols-2 xl:grid-cols-4">{"".join(cols)}</div>'


def mm_label(s: str) -> str:
    return "".join({'"': "#quot;", "<": "#lt;", ">": "#gt;", "&": "#amp;"}.get(c, c) for c in s)


def dependency_graph(tasks: list[dict], critical: set, all_by_id: dict) -> str:
    live = [t for t in tasks if t["status"] != "dropped"]
    if not live:
        return ""
    nid = lambda i: "t_" + re.sub(r"\W", "_", i)
    lines, seen, extra = ["flowchart LR"], {t["id"] for t in live}, []
    for t in live:
        lines.append(f'  {nid(t["id"])}["{mm_label(t["id"] + " · " + t["title"])}"]')
    for t in live:
        for d in t["deps"]:
            if d not in seen and d not in extra:
                ext = all_by_id.get(d)
                extra.append(d)
                lines.append(f'  {nid(d)}["{mm_label(d + (" · " + ext["title"] if ext else " · unknown"))}"]:::ext')
            lines.append(f'  {nid(d)} --> {nid(t["id"])}')
    lines += ["  classDef done stroke-dasharray:4 3,opacity:0.6", "  classDef crit stroke-width:3px",
              "  classDef blocked stroke:#e5484d,stroke-width:2px", "  classDef ext stroke-dasharray:2 2"]
    for t in live:
        cls = ("done" if t["status"] == "done" else "blocked" if t["status"] == "blocked"
               else "crit" if t["id"] in critical else "")
        if cls:
            lines.append(f"  class {nid(t['id'])} {cls}")
    src = "\n".join(lines)
    return f"""<section id="dependencies" class="space-y-2">
<h2 class="text-xl font-bold">Dependencies</h2>
<p class="text-sm opacity-70">Arrows mean "must finish first". Thick border = critical path, red = blocked, dashed = done. Click the diagram to edit it as a whiteboard, then queue the feedback.</p>
<div class="mermaid">
{src}
</div>
</section>"""


def edit_form(tasks: list[dict]) -> str:
    rows = []
    for t in sorted((t for t in tasks if t["status"] in pm_scan.OPEN), key=lambda t: t["id"]):
        est = t.get("estimate", "")
        est_opts = ESTIMATES + ([est] if est and est not in ESTIMATES else [])
        status_sel = "".join(f'<option{" selected" if s == t["status"] else ""}>{s}</option>'
                             for s in ["todo", "doing", "blocked", "done", "dropped"])
        est_sel = "".join(f'<option{" selected" if e == est else ""}>{esc(e)}</option>' for e in est_opts)
        rows.append(f"""<tr data-id="{esc(t['id'])}" data-label="{esc(t['title'])}" data-file="{esc(t['file'])}" data-line="{t['line']}">
<td class="font-mono text-xs">{esc(t['id'])}</td><td>{esc(t['title'])}</td>
<td><select class="select select-sm" aria-label="status" data-field="status" data-orig="{esc(t['status'])}">{status_sel}</select></td>
<td><input class="input input-sm w-24" aria-label="owner" data-field="owner" data-orig="{esc(t['owner'])}" value="{esc(t['owner'])}"></td>
<td><select class="select select-sm" aria-label="estimate" data-field="estimate" data-orig="{esc(est)}">{est_sel}</select></td>
<td><input type="date" class="input input-sm" aria-label="due" data-field="due" data-orig="{esc(t.get('due', ''))}" value="{esc(t.get('due', ''))}"></td>
<td><input class="input input-sm" aria-label="note" placeholder="e.g. blocked by…" data-field="note" data-orig="" value=""></td>
</tr>""")
    if not rows:
        return ""
    return f"""<section id="quick-edit" class="space-y-2">
<h2 class="text-xl font-bold">Quick edit</h2>
<p class="text-sm opacity-70">Change fields, then queue them as one batch. Nothing is sent until you press Send in Lavish. For anything else, comment directly on a card.</p>
<form data-lavish-question="task-edits" onsubmit="event.preventDefault(); openpmQueueEdits(this)" class="space-y-2">
<div class="overflow-x-auto rounded-box border border-base-300"><table class="table table-sm">
<thead><tr><th>ID</th><th>Task</th><th>Status</th><th>Owner</th><th>Estimate</th><th>Due</th><th>Note</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table></div>
<div class="flex items-center gap-3"><button type="submit" class="btn btn-primary btn-sm">Queue task edits</button><span data-openpm-status role="status" aria-live="polite" class="text-sm"></span></div>
<pre data-openpm-fallback hidden class="text-xs whitespace-pre-wrap bg-base-200 p-3 rounded-box"></pre>
</form>
</section>"""


def milestone_card(mid: str, ms: dict | None, name: str, tasks: list[dict], link: str = "") -> str:
    ms = ms or {}
    p = progress(tasks)
    meta = " · ".join(x for x in [f'target {ms["target"]}' if ms.get("target") else "",
                                  ms.get("section", "")] if x)
    title = f'<a class="link" href="{esc(link)}">{esc(name)}</a>' if link else esc(name)
    return f"""<div id="{esc(mid)}" class="card card-border bg-base-200">
<div class="card-body gap-2">
<div class="flex flex-wrap items-center gap-2"><span class="font-mono text-xs opacity-70">{esc(mid)}</span>{ms_status_badge(ms.get("status", ""))}<span class="text-xs opacity-70">{esc(meta)}</span></div>
<h3 class="card-title text-base">{title}</h3>
{f'<p class="text-sm font-semibold">{esc(ms["after"])}</p>' if ms.get("after") else ""}
{f'<p class="text-xs opacity-80">Metrics: {esc(ms["metrics"])}</p>' if ms.get("metrics") else ""}
{f'<p class="text-xs opacity-80">Status: {esc(ms["status"])}</p>' if ms.get("status") else ""}
{bar(p) if p["total"] else '<p class="text-xs opacity-60">No tasks yet.</p>'}
</div></div>"""


# ---------- pages ----------

def render_project(client: dict, proj: dict, all_by_id: dict, today: dt.date) -> str:
    tasks, critical = proj["tasks"], set(proj["critical"])
    p = progress(tasks)
    nxt = next((t for t in sorted(tasks, key=pm_scan.sort_key) if t["actionable"]), None)
    committed = sorted((t for t in tasks if t["committed"] and t["status"] in pm_scan.OPEN and t["due_date"]),
                       key=lambda t: t["due_date"])
    head = f"""<header class="space-y-3">
<div class="flex flex-wrap items-center gap-2"><span class="font-mono text-sm opacity-70">{esc(client['meta'].get('code', ''))} · {esc(proj['slug'])}</span>{badge(f"{proj['plan_kind']}: {proj['plan_status']}" if proj['plan_kind'] else "no spec yet", "badge-outline")}</div>
<h1 class="text-3xl font-bold">{esc(proj['title'])}</h1>
{stats([("Progress", f"{p['pct']}%", f"{p['done']}/{p['total']} tasks done"),
        ("Open work", f"{p['open_hours']:g}h", f"{p['blocked']} blocked"),
        ("Next up", nxt["id"] if nxt else "-", nxt["title"] if nxt else "nothing actionable"),
        ("Next commitment", committed[0]["due"] if committed else "-",
         committed[0]["id"] if committed else "none open")])}
<p class="text-xs opacity-60">As of {today.isoformat()}.</p>
</header>"""

    def plan_heading(level, text):
        m = re.match(r"^(S\d+)\b", text)
        if level == 3 and m:
            return m.group(1), ""
        return (f"plan-{slugify(text)}" if level == 2 else None), ""

    if proj["plan_body"]:
        plan = (f'<section id="plan" class="card card-border bg-base-100"><div class="card-body md">'
                f'{md_to_html(proj["plan_body"], plan_heading)}</div></section>')
    else:
        plan = ('<section id="plan" role="alert" class="alert alert-info"><span>No brief or spec yet. '
                'Run pm-intake, then pm-spec.</span></section>')

    ms_ids = []
    for t in tasks:
        if t.get("milestone") and t["milestone"] not in ms_ids:
            ms_ids.append(t["milestone"])
    ms_cards = "".join(milestone_card(m, client["milestones"].get(m),
                                      (client["milestones"].get(m) or {}).get("name") or proj["ms_names"].get(m, m),
                                      [t for t in tasks if t.get("milestone") == m]) for m in ms_ids)
    body = f"""{head}
<div role="tablist" class="tabs tabs-border">
<a role="tab" class="tab" href="#plan">Plan</a><a role="tab" class="tab" href="#milestones">Milestones</a>
<a role="tab" class="tab" href="#board">Tasks</a><a role="tab" class="tab" href="#dependencies">Dependencies</a>
<a role="tab" class="tab" href="#quick-edit">Quick edit</a></div>
<section class="space-y-2"><h2 class="text-xl font-bold">Plan</h2>{plan}</section>
<section id="milestones" class="space-y-2"><h2 class="text-xl font-bold">Milestones</h2>
<div class="grid gap-4 md:grid-cols-2">{ms_cards or '<p class="text-sm opacity-60">No milestones yet.</p>'}</div></section>
<section id="board" class="space-y-2"><h2 class="text-xl font-bold">Tasks</h2>{board(tasks, critical) if tasks else '<p class="text-sm opacity-60">No tasks yet. Run pm-breakdown.</p>'}</section>
{dependency_graph(tasks, critical, all_by_id)}
{edit_form(tasks)}"""
    crumbs = [("All clients", "../index.html"), (client["name"], "index.html"), (proj["title"], None)]
    extra = (MERMAID if 'class="mermaid"' in body else "") + (EDIT_JS if "openpmQueueEdits" in body else "")
    return page(f'{proj["title"]} - {client["name"]}', crumbs, body, extra)


def render_client(client: dict, today: dt.date) -> str:
    meta = client["meta"]
    secs = {s["title"].lower(): s for s in client["sections"]}
    find = lambda prefix: next((s for k, s in secs.items() if k.startswith(prefix)), None)
    story = find("the story")
    by_ms_init = {}
    for proj in client["projects"]:
        for t in proj["tasks"]:
            by_ms_init.setdefault(t.get("milestone"), proj["slug"])
    cols = []
    for label in ("now", "next", "later"):
        sec = find(label)
        if not sec:
            continue
        mids = [m for m, ms in client["milestones"].items() if ms["section"] == sec["title"]]
        cards = "".join(milestone_card(m, client["milestones"][m], client["milestones"][m]["name"],
                                       [t for t in client["tasks"] if t.get("milestone") == m],
                                       f'{by_ms_init[m]}.html' if m in by_ms_init else "") for m in mids)
        rest = "\n".join(l for l in sec["body"].splitlines()
                         if not l.startswith("### ") and not (mids and l.startswith("- ")))
        cols.append(f'<div id="roadmap-{label}" class="space-y-3"><h3 class="font-semibold">{esc(sec["title"])}</h3>'
                    f'{cards}<div class="md text-sm">{md_to_html(rest)}</div></div>')
    known = ("the story", "now", "next", "later")
    others = "".join(f'<details class="collapse collapse-arrow bg-base-200" id="roadmap-{slugify(s["title"])}">'
                     f'<summary class="collapse-title font-semibold">{esc(s["title"])}</summary>'
                     f'<div class="collapse-content md text-sm">{md_to_html(s["body"])}</div></details>'
                     for s in client["sections"] if not s["title"].lower().startswith(known))
    projects = []
    for proj in client["projects"]:
        p = progress(proj["tasks"])
        status = f"{proj['plan_kind']}: {proj['plan_status']}" if proj["plan_kind"] else "no spec yet"
        projects.append(f"""<a id="project-{esc(proj['slug'])}" href="{esc(proj['slug'])}.html" class="card card-border bg-base-200 hover:bg-base-300">
<div class="card-body gap-2"><div class="flex flex-wrap gap-2 items-center"><span class="font-mono text-xs opacity-70">{esc(proj['slug'])}</span>{badge(status, "badge-outline")}</div>
<h3 class="card-title text-base">{esc(proj['title'])}</h3>{bar(p) if p['total'] else '<p class="text-xs opacity-60">No tasks yet.</p>'}</div></a>""")
    p = progress(client["tasks"])
    body = f"""<header class="space-y-3">
<div class="flex flex-wrap items-center gap-2"><span class="font-mono text-sm opacity-70">{esc(meta.get('code', ''))}</span>{health_badge(meta.get('health', ''))}<span class="text-xs opacity-70">{esc(meta.get('contract', ''))} · {esc(meta.get('cadence', ''))}</span></div>
<h1 class="text-3xl font-bold">{esc(client['name'])}</h1>
{f'<div id="story" role="note" class="alert alert-soft"><span>{inline(story["body"])}</span></div>' if story and story["body"] else ""}
<p class="text-xs opacity-60">As of {today.isoformat()} · {p['open_hours']:g}h open across {len(client['projects'])} project(s).</p>
</header>
<section id="projects" class="space-y-2"><h2 class="text-xl font-bold">Projects</h2>
<div class="grid gap-4 md:grid-cols-2 xl:grid-cols-3">{''.join(projects) or '<p class="text-sm opacity-60">No projects yet. Run pm-intake.</p>'}</div></section>
<section id="roadmap" class="space-y-2"><h2 class="text-xl font-bold">Roadmap</h2>
<div class="grid gap-4 lg:grid-cols-3">{''.join(cols) or '<p class="text-sm opacity-60">No roadmap yet. Run pm-roadmap.</p>'}</div>
{others}</section>"""
    return page(f'{client["name"]} - OpenPM', [("All clients", "../index.html"), (client["name"], None)], body)


def render_index(clients: list[dict], today: dt.date) -> str:
    cards = []
    for c in clients:
        p = progress(c["tasks"])
        overdue = sum(1 for t in c["tasks"] if t["committed"] and t["status"] in pm_scan.OPEN
                      and t["days_left"] is not None and t["days_left"] <= 0)
        cards.append(f"""<a id="client-{esc(c['slug'])}" href="{esc(c['slug'])}/index.html" class="card card-border bg-base-200 hover:bg-base-300">
<div class="card-body gap-2"><div class="flex flex-wrap gap-2 items-center"><span class="font-mono text-xs opacity-70">{esc(c['meta'].get('code', ''))}</span>{health_badge(c['meta'].get('health', ''))}{badge(f"{overdue} committed due/overdue", "badge-error") if overdue else ""}</div>
<h2 class="card-title">{esc(c['name'])}</h2><p class="text-sm opacity-80">{len(c['projects'])} project(s)</p>{bar(p) if p['total'] else ''}</div></a>""")
    body = f"""<header><h1 class="text-3xl font-bold">Clients</h1><p class="text-xs opacity-60">As of {today.isoformat()}.</p></header>
<div class="grid gap-4 md:grid-cols-2 xl:grid-cols-3">{''.join(cards) or '<p>No clients yet. Run pm-init.</p>'}</div>"""
    return page("OpenPM - all clients", [("All clients", None)], body)


def render(ws: Path, out: Path, today: dt.date, only_client: str | None = None) -> list[Path]:
    all_tasks, clients = load_model(ws, today)
    by_id = {t["id"]: t for t in all_tasks}
    written = []

    def write(path: Path, text: str):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        written.append(path)

    write(out / "index.html", render_index(clients, today))
    for c in clients:
        if only_client and c["slug"] != only_client:
            continue
        write(out / c["slug"] / "index.html", render_client(c, today))
        for proj in c["projects"]:
            write(out / c["slug"] / f'{proj["slug"]}.html', render_project(c, proj, by_id, today))
    return written


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--workspace", help="workspace path (default: same lookup as pm_scan.py)")
    p.add_argument("--client", help="only render this client slug (the all-clients index is always written)")
    p.add_argument("--out", help="output directory (default: <workspace>/.lavish)")
    p.add_argument("--today", help="override today's date (YYYY-MM-DD), for testing")
    a = p.parse_args(argv)
    ws = pm_scan.find_workspace(a.workspace)
    if not ws:
        print("No OpenPM workspace found. Run the pm-init skill or set $OPENPM_WORKSPACE.", file=sys.stderr)
        return 2
    if a.client and not (ws / "clients" / a.client).is_dir():
        print(f"Unknown client '{a.client}'.", file=sys.stderr)
        return 2
    today = dt.date.fromisoformat(a.today) if a.today else dt.date.today()
    out = Path(a.out).expanduser().resolve() if a.out else ws / ".lavish"
    for path in render(ws, out, today, a.client):
        print(path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
