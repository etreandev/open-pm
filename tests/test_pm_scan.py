"""Tests for skills/pm-core/scripts/pm_scan.py (stdlib unittest).

Run: python3 -m unittest discover -s tests -v
"""
import importlib.util
import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXAMPLE = ROOT / "examples" / "pm-workspace"
spec = importlib.util.spec_from_file_location("pm_scan", ROOT / "skills/pm-core/scripts/pm_scan.py")
pm_scan = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pm_scan)


def run(*args):
    buf = io.StringIO()
    with redirect_stdout(buf):
        code = pm_scan.main(["--workspace", str(EXAMPLE), "--today", "2026-10-12", *args])
    return code, buf.getvalue()


class ExampleWorkspace(unittest.TestCase):
    def test_lint_is_clean(self):
        code, out = run("--lint")
        self.assertEqual(code, 0, out)

    def test_triage_order(self):
        _, out = run("--json")
        tasks = json.loads(out)["tasks"]
        actionable = [t["id"] for t in tasks if t["actionable"]]
        # tier 0 committed today, then tier 2 (unblocks others) smallest first, then backlog
        self.assertEqual(actionable, ["GLBX-000-01", "ACME-001-07", "ACME-001-04", "ACME-001-03"])
        tiers = {t["id"]: t["tier"] for t in tasks}
        self.assertEqual(tiers["GLBX-000-01"], 0)
        self.assertEqual(tiers["ACME-001-07"], 2)
        self.assertEqual(tiers["ACME-001-03"], 6)

    def test_waiting_and_blocked_not_actionable(self):
        _, out = run("--json")
        by_id = {t["id"]: t for t in json.loads(out)["tasks"]}
        self.assertEqual(by_id["ACME-001-05"]["waiting_on"], ["ACME-001-04"])
        self.assertFalse(by_id["ACME-001-05"]["actionable"])
        self.assertFalse(by_id["GLBX-000-02"]["actionable"])
        self.assertNotIn("ACME-001-01", by_id)  # done tasks hidden by default

    def test_filters(self):
        _, out = run("--json", "--owner", "me", "--due-within", "7")
        ids = {t["id"] for t in json.loads(out)["tasks"]}
        self.assertEqual(ids, {"GLBX-000-01", "ACME-001-06"})

    def test_text_report(self):
        code, out = run()
        self.assertEqual(code, 0)
        self.assertIn("ACTIONABLE (4 tasks", out)
        self.assertIn("waiting on Airflow admin rights", out)


class Lint(unittest.TestCase):
    def test_reports_problems(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp, "clients", "x", "initiatives", "001-a")
            d.mkdir(parents=True)
            (d / "tasks.md").write_text(
                "### X-001-01 Too big\n- status: todo\n- owner: me\n- type: build\n- estimate: 2d\n"
                "- depends_on: X-001-99\n\n"
                "### X-001-02 Blocked\n- status: blocked\n- owner: me\n- type: build\n- estimate: 1h\n"
                "- story: S1\n- milestone: M1\n- done_when: ok\n"
            )
            buf = io.StringIO()
            with redirect_stdout(buf):
                code = pm_scan.main(["--workspace", tmp, "--lint"])
            out = buf.getvalue()
        self.assertEqual(code, 1)
        for expected in ("split it", "missing done_when", "unknown id X-001-99",
                         "missing story", "blocked without blocked_by"):
            self.assertIn(expected, out)

    def test_estimates(self):
        self.assertEqual(pm_scan.parse_hours("30m"), 0.5)
        self.assertEqual(pm_scan.parse_hours("1.5h"), 1.5)
        self.assertEqual(pm_scan.parse_hours("1d"), 8)
        self.assertIsNone(pm_scan.parse_hours("soon"))

    def test_brevity_warnings(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp, "clients", "x", "initiatives", "001-a")
            d.mkdir(parents=True)
            long_title = "This is a very long task title that exceeds eight words"
            long_dw = " ".join(["word"] * 26)
            (d / "tasks.md").write_text(
                f"### X-001-01 {long_title}\n- status: todo\n- owner: me\n- type: build\n- estimate: 1h\n"
                f"- story: S1\n- milestone: M1\n- done_when: {long_dw}\n"
            )
            buf = io.StringIO()
            with redirect_stdout(buf):
                code = pm_scan.main(["--workspace", tmp, "--lint"])
            out = buf.getvalue()
        self.assertEqual(code, 0)
        self.assertIn("WARN:", out)
        self.assertIn("words (> 8, be terse)", out)
        self.assertIn("words (> 25, be terse)", out)
        self.assertIn("OK - 1 tasks, no problems (2 warning(s)).", out)


if __name__ == "__main__":
    unittest.main()
