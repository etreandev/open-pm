#!/usr/bin/env python3
"""OpenPM workspace scanner.

Parses task blocks from clients/*/initiatives/*/tasks.md and prints them
ranked by the triage tiers in references/prioritization.md.

Standard library only. Run with --help for options.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
from pathlib import Path

OPEN = {"todo", "doing", "blocked"}
STATUSES = OPEN | {"done", "dropped"}
TYPES = {"build", "spike", "comms", "decision", "resource", "network", "review"}
LEAD_TYPES = {"comms", "decision", "resource", "network"}
MAX_HOURS = 4.0
TIER_LABELS = {
    0: "committed: overdue/today",
    1: "committed: due <=2d",
    2: "unblocks others",
    3: "lead task",
    4: "in progress",
    5: "due <=7d",
    6: "backlog",
}
TASK_RE = re.compile(r"^###\s+([A-Z][A-Z0-9_]*-\d{3}-\d{2,})\s+(.*)$")
FIELD_RE = re.compile(r"^\s*-\s+([a-z_]+):\s*(.*)$")
SHORT_FIELDS = {"status", "owner", "type", "estimate", "due", "committed", "story", "milestone"}


def find_workspace(explicit: str | None) -> Path | None:
    candidates = [explicit, os.environ.get("OPENPM_WORKSPACE")]
    cfg = Path.home() / ".config" / "openpm" / "workspace"
    if cfg.is_file():
        lines = cfg.read_text().strip().splitlines()
        candidates.append(lines[0].strip() if lines else None)
    candidates.append(str(Path.home() / "pm-workspace"))
    for c in candidates:
        if c and Path(c).expanduser().is_dir():
            return Path(c).expanduser().resolve()
    return None


def parse_hours(value: str) -> float | None:
    m = re.fullmatch(r"\s*(\d+(?:\.\d+)?)\s*([mhd])\s*", value or "")
    if not m:
        return None
    n, unit = float(m.group(1)), m.group(2)
    return {"m": n / 60, "h": n, "d": n * 8}[unit]


def parse_date(value: str) -> dt.date | None:
    try:
        return dt.date.fromisoformat((value or "").strip())
    except ValueError:
        return None


def parse_tasks(path: Path, workspace: Path) -> list[dict]:
    rel = path.relative_to(workspace)
    client, initiative = rel.parts[1], rel.parts[3]
    tasks, current = [], None
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        head = TASK_RE.match(line)
        if head:
            current = {"id": head.group(1), "title": head.group(2).strip(), "client": client,
                       "initiative": initiative, "file": str(rel), "line": lineno}
            tasks.append(current)
            continue
        if line.startswith("#"):
            current = None
            continue
        field = FIELD_RE.match(line) if current else None
        if field:
            key, val = field.group(1), field.group(2).strip()
            if key in SHORT_FIELDS:
                val = re.sub(r"\s+#.*$", "", val).strip()
            current[key] = val
    return tasks


def load(workspace: Path) -> list[dict]:
    tasks = []
    for path in sorted(workspace.glob("clients/*/initiatives/*/tasks.md")):
        tasks.extend(parse_tasks(path, workspace))
    return tasks


def enrich(tasks: list[dict], today: dt.date) -> None:
    by_id = {t["id"]: t for t in tasks}
    for t in tasks:
        t["status"] = t.get("status", "todo").lower()
        t["owner"] = t.get("owner", "")
        t["hours"] = parse_hours(t.get("estimate", ""))
        t["deps"] = [d.strip() for d in t.get("depends_on", "").split(",") if d.strip()]
        t["committed"] = t.get("committed", "false").lower() in {"true", "yes"}
        due = parse_date(t.get("due", ""))
        t["due_date"] = due
        t["days_left"] = (due - today).days if due else None
        t["dependents"] = []
    for t in tasks:
        if t["status"] in OPEN:
            for d in t["deps"]:
                if d in by_id:
                    by_id[d]["dependents"].append(t["id"])
    for t in tasks:
        open_deps = [d for d in t["deps"] if by_id.get(d, {}).get("status") not in {"done", "dropped"}]
        t["waiting_on"] = open_deps
        t["actionable"] = t["status"] in {"todo", "doing"} and not open_deps
        t["tier"] = tier(t) if t["actionable"] else None


def tier(t: dict) -> int:
    days = t["days_left"]
    if t["committed"] and days is not None and days <= 0:
        return 0
    if t["committed"] and days is not None and days <= 2:
        return 1
    if t["dependents"]:
        return 2
    if t["owner"] == "me" and t.get("type") in LEAD_TYPES:
        return 3
    if t["status"] == "doing":
        return 4
    if days is not None and days <= 7:
        return 5
    return 6


def sort_key(t: dict):
    return (t["tier"] if t["tier"] is not None else 99,
            t["days_left"] if t["days_left"] is not None else 10**6,
            t["hours"] if t["hours"] is not None else 10**6, t["id"])


def lint(tasks: list[dict]) -> list[str]:
    problems, seen = [], {}
    ids = {t["id"] for t in tasks}
    for t in tasks:
        where = f'{t["file"]}:{t["line"]} {t["id"]}'
        if t["id"] in seen:
            problems.append(f"{where}: duplicate id (also {seen[t['id']]})")
        seen.setdefault(t["id"], where)
        if t["status"] not in STATUSES:
            problems.append(f"{where}: invalid status '{t['status']}'")
        if t["status"] in {"done", "dropped"}:
            continue
        if t.get("type") not in TYPES:
            problems.append(f"{where}: missing/invalid type '{t.get('type', '')}'")
        if not t["owner"]:
            problems.append(f"{where}: missing owner")
        if not t.get("done_when"):
            problems.append(f"{where}: missing done_when")
        if t["hours"] is None:
            problems.append(f"{where}: missing/unparseable estimate")
        elif t["hours"] > MAX_HOURS:
            problems.append(f"{where}: estimate {t['estimate']} > {MAX_HOURS:g}h, split it")
        if t.get("due") and t["due_date"] is None:
            problems.append(f"{where}: unparseable due date '{t['due']}'")
        if t["status"] == "blocked" and not t.get("blocked_by"):
            problems.append(f"{where}: blocked without blocked_by")
        for key in ("story", "milestone"):
            if not t.get(key):
                problems.append(f"{where}: missing {key} (narrative traceability)")
        for d in t["deps"]:
            if d not in ids:
                problems.append(f"{where}: depends_on unknown id {d}")
    return problems


def fmt_due(t: dict) -> str:
    if t["days_left"] is None:
        return ""
    d = t["days_left"]
    rel = "today" if d == 0 else (f"{-d}d late" if d < 0 else f"in {d}d")
    return f"{t['due']} ({rel}){' !' if t['committed'] else ''}"


def table(rows: list[dict], cols: list[tuple[str, str]]) -> str:
    if not rows:
        return "  (none)"
    widths = [max(len(h), *(len(str(r.get(k, ""))) for r in rows)) for k, h in cols]
    line = lambda vals: "  " + "  ".join(str(v).ljust(w) for v, w in zip(vals, widths))
    out = [line(h for _, h in cols), line("-" * w for w in widths)]
    out += [line(r.get(k, "") for k, _ in cols) for r in rows]
    return "\n".join(out)


def report(tasks: list[dict], today: dt.date) -> str:
    act = sorted((t for t in tasks if t["actionable"]), key=sort_key)
    rest = [t for t in tasks if t["status"] in OPEN and not t["actionable"]]
    for t in act + rest:
        t["tier_label"] = f'{t["tier"]} {TIER_LABELS[t["tier"]]}' if t["tier"] is not None else ""
        t["due_fmt"] = fmt_due(t)
        t["est"] = t.get("estimate", "?")
        t["why_not"] = t.get("blocked_by") or ("waiting on " + ", ".join(t["waiting_on"]))
    cols = [("tier_label", "tier"), ("id", "id"), ("title", "title"), ("owner", "owner"),
            ("type", "type"), ("est", "est"), ("due_fmt", "due (! = committed)")]
    hours = lambda ts: sum(t["hours"] or 0 for t in ts)
    by_owner, by_client = {}, {}
    for t in act + rest:
        by_owner[t["owner"] or "?"] = by_owner.get(t["owner"] or "?", 0) + (t["hours"] or 0)
        by_client[t["client"]] = by_client.get(t["client"], 0) + (t["hours"] or 0)
    week = [t for t in act + rest if t["days_left"] is not None and t["days_left"] <= 7]
    parts = [
        f"OpenPM scan - {today.isoformat()}",
        f"\nACTIONABLE ({len(act)} tasks, {hours(act):g}h)",
        table(act, cols),
        f"\nWAITING / BLOCKED ({len(rest)})",
        table(rest, [("id", "id"), ("title", "title"), ("owner", "owner"), ("why_not", "why")]),
        "\nSUMMARY",
        "  open hours by owner:  " + ", ".join(f"{k} {v:g}h" for k, v in sorted(by_owner.items())),
        "  open hours by client: " + ", ".join(f"{k} {v:g}h" for k, v in sorted(by_client.items())),
        f"  due within 7d (incl. overdue): {len(week)} tasks, {hours(week):g}h; "
        f"committed: {hours([t for t in week if t['committed']]):g}h",
    ]
    return "\n".join(parts)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--workspace", help="workspace path (default: $OPENPM_WORKSPACE, ~/.config/openpm/workspace, ~/pm-workspace)")
    p.add_argument("--owner", help="filter by owner (e.g. me)")
    p.add_argument("--client", help="filter by client slug")
    p.add_argument("--due-within", type=int, metavar="DAYS", help="only tasks due within N days (incl. overdue)")
    p.add_argument("--all", action="store_true", help="include done/dropped tasks (with --json)")
    p.add_argument("--lint", action="store_true", help="report format problems; exit 1 if any")
    p.add_argument("--json", action="store_true", help="JSON output")
    p.add_argument("--today", help="override today's date (YYYY-MM-DD), for testing")
    a = p.parse_args(argv)

    ws = find_workspace(a.workspace)
    if not ws:
        print("No OpenPM workspace found. Run the pm-init skill or set $OPENPM_WORKSPACE.", file=sys.stderr)
        return 2
    today = dt.date.fromisoformat(a.today) if a.today else dt.date.today()
    tasks = load(ws)
    enrich(tasks, today)

    if a.lint:
        problems = lint(tasks)
        print("\n".join(problems) if problems else f"OK - {len(tasks)} tasks, no problems.")
        return 1 if problems else 0

    if a.owner:
        tasks = [t for t in tasks if t["owner"] == a.owner]
    if a.client:
        tasks = [t for t in tasks if t["client"] == a.client]
    if a.due_within is not None:
        tasks = [t for t in tasks if t["days_left"] is not None and t["days_left"] <= a.due_within]
    if not a.all:
        tasks = [t for t in tasks if t["status"] in OPEN]

    if a.json:
        out = [{k: v for k, v in t.items() if k != "due_date"} for t in sorted(tasks, key=sort_key)]
        print(json.dumps({"workspace": str(ws), "today": today.isoformat(), "tasks": out}, indent=2))
    else:
        print(report(tasks, today))
    return 0


if __name__ == "__main__":
    sys.exit(main())
