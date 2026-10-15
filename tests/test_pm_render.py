"""Tests for skills/pm-core/scripts/pm_render.py (stdlib unittest).

Run: python3 -m unittest discover -s tests -v
"""
import datetime as dt
import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXAMPLE = ROOT / "examples" / "pm-workspace"

spec = importlib.util.spec_from_file_location("pm_render", ROOT / "skills/pm-core/scripts/pm_render.py")
pm_render = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pm_render)


class TestPmRender(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.out_dir = Path(self.tmp.name)
        self.today = dt.date(2026, 10, 12)

    def tearDown(self):
        self.tmp.cleanup()

    def test_render_writes_expected_files(self):
        written = pm_render.render(EXAMPLE, self.out_dir, self.today)
        rel_paths = {p.relative_to(self.out_dir).as_posix() for p in written}
        expected = {
            "index.html",
            "acme-retail/index.html",
            "acme-retail/001-revenue-mart.html",
            "globex/index.html",
            "globex/000-ops.html",
        }
        self.assertEqual(rel_paths, expected)
        for p in written:
            self.assertTrue(p.is_file())
            self.assertGreater(p.stat().st_size, 500)

    def test_render_is_deterministic(self):
        pm_render.render(EXAMPLE, self.out_dir / "run1", self.today)
        pm_render.render(EXAMPLE, self.out_dir / "run2", self.today)
        for p1 in (self.out_dir / "run1").rglob("*.html"):
            p2 = self.out_dir / "run2" / p1.relative_to(self.out_dir / "run1")
            self.assertTrue(p2.exists())
            self.assertEqual(p1.read_text(), p2.read_text(), f"Mismatch in {p1.name}")

    def test_project_page_structure(self):
        pm_render.render(EXAMPLE, self.out_dir, self.today, only_client="acme-retail")
        proj_html = (self.out_dir / "acme-retail" / "001-revenue-mart.html").read_text()

        # Sections and tabs
        self.assertIn('id="plan"', proj_html)
        self.assertIn('id="milestones"', proj_html)
        self.assertIn('id="board"', proj_html)
        self.assertIn('id="dependencies"', proj_html)
        self.assertIn('id="quick-edit"', proj_html)

        # Stable task card IDs and metadata attributes
        self.assertIn('id="ACME-001-01"', proj_html)
        self.assertIn('id="ACME-001-04"', proj_html)
        self.assertIn('data-file="clients/acme-retail/initiatives/001-revenue-mart/tasks.md"', proj_html)
        self.assertIn('data-line=', proj_html)

        # Badges and critical path
        self.assertIn("critical path", proj_html)
        self.assertIn("tier 2", proj_html)

        # Mermaid dependency graph
        self.assertIn('<div class="mermaid">', proj_html)
        self.assertIn("t_ACME_001_04 --> t_ACME_001_05", proj_html)

        # Quick edit form with Lavish question attribute
        self.assertIn('data-lavish-question="task-edits"', proj_html)
        self.assertIn('data-id="ACME-001-04"', proj_html)

    def test_client_page_structure(self):
        pm_render.render(EXAMPLE, self.out_dir, self.today, only_client="acme-retail")
        client_html = (self.out_dir / "acme-retail" / "index.html").read_text()

        self.assertIn("Acme Retail", client_html)
        self.assertIn("ACME", client_html)
        self.assertIn('id="projects"', client_html)
        self.assertIn('id="roadmap"', client_html)
        self.assertIn('href="001-revenue-mart.html"', client_html)
        self.assertIn("badge-warning", client_html)  # health is yellow

    def test_index_page_structure(self):
        pm_render.render(EXAMPLE, self.out_dir, self.today)
        index_html = (self.out_dir / "index.html").read_text()

        self.assertIn('href="acme-retail/index.html"', index_html)
        self.assertIn('href="globex/index.html"', index_html)
        self.assertIn("Acme Retail", index_html)
        self.assertIn("Globex", index_html)


if __name__ == "__main__":
    unittest.main()
