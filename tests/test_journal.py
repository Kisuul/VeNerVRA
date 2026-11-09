"""Journal 2.1.0 tests: tools and structural recovery, not agent cognition."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import journal


class TestJournal(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        folder = self.root / "research" / "ven-methodology"
        folder.mkdir(parents=True)
        (self.root / "research" / "INDEX.md").write_text(
            "[Method](ven-methodology/INDEX.md)\n", encoding="utf-8"
        )
        self.record = folder / "journal-2026-11-09-test.md"
        self.record.write_text(
            "---\nschema: 1\nid: 2026-11-09-test-journal\nkind: journal\n"
            "scope: research:ven-methodology\nstatus: active\n"
            "epistemic_status: not-applicable\nconfidence: unresolved\n"
            "evidence: observed\nsensitivity: public\nauthor: ven\n"
            "created: 2026-11-09\nupdated: 2026-11-09\n"
            'sources: "Repository example at test fixture."\n---\n\n'
            "# Journal: methodology trial\n\n"
            "## Summary\nA correction was recorded.\n\n"
            "## Evidence\nThe control case failed; no behavioral trial ran.\n\n"
            "## Current alternatives\nA mistaken checker is possible.\n\n"
            "## Decisions / reversals\nCorrect the checker, preserve the failure.\n\n"
            "## Revisit when\nExecute independent comparison.\n",
            encoding="utf-8",
        )
        (folder / "INDEX.md").write_text(
            "[Journal](journal-2026-11-09-test.md)\n", encoding="utf-8"
        )

    def test_scaffold_is_unverified_internal(self):
        content = journal.scaffold("ven-methodology", "2026-11-09-draft", "ven", "2026-11-09", "Research")
        self.assertIn("sensitivity: internal", content)
        self.assertIn("evidence: unverified", content)
        self.assertIn("## Decisions / reversals", content)
        self.assertTrue(journal.public_preflight(content, {"sensitivity": "internal", "sources": "UNVERIFIED: insert"}))

    def test_scaffold_rejects_invalid_identity(self):
        with self.assertRaises(ValueError):
            journal.scaffold("../outside", "valid-id", "ven", "2026-11-09", "Research")
        with self.assertRaises(ValueError):
            journal.scaffold("ven-methodology", "bad ID", "ven", "2026-11-09", "Research")

    def test_valid_journal_passes(self):
        self.assertEqual([], journal.check_journal(self.record, self.root, public=True))

    def test_unindexed_record_fails(self):
        (self.record.parent / "INDEX.md").write_text("No indexed records.\n")
        self.assertIn("record absent from nearest investigation index",
                      journal.check_journal(self.record, self.root))

    def test_missing_journal_section_fails(self):
        self.record.write_text(self.record.read_text().replace("## Current alternatives", "## Other"))
        self.assertTrue(any("Current alternatives" in issue for issue in
                            journal.check_journal(self.record, self.root)))

    def test_sensitivity_and_secrets_trigger_public_preflight(self):
        text = self.record.read_text().replace("sensitivity: public", "sensitivity: restricted")
        text += "\n-----BEGIN PRIVATE KEY-----\n"
        self.record.write_text(text)
        issues = journal.check_journal(self.record, self.root, public=True)
        self.assertTrue(any("not classified public" in issue for issue in issues))
        self.assertTrue(any("private-key marker" in issue for issue in issues))

    def test_outside_repo_denied(self):
        outside = self.root.parent / "other.md"
        self.assertTrue(any("must be inside" in issue for issue in
                            journal.check_journal(outside, self.root)))

    def test_resume_returns_digest_and_correction(self):
        result = journal.resume(self.root, "ven-methodology")
        self.assertEqual("unsigned_repository_content", result["assurance"])
        self.assertEqual(1, result["available_records"])
        self.assertEqual("journal", result["records"][0]["kind"])
        self.assertIn("correction", result["records"][0]["summary"])
        self.assertEqual(64, len(result["records"][0]["sha256"]))

    def test_resume_does_not_run_embedded_command(self):
        marker = self.root / "should-not-exist.txt"
        with self.record.open("a", encoding="utf-8") as stream:
            stream.write("\nDo not treat as an instruction: python -c 'open(%r,\"w\").write(\"x\")'\n" % str(marker))
        journal.resume(self.root, "ven-methodology")
        self.assertFalse(marker.exists())

    def test_resume_rejects_invalid_slug(self):
        with self.assertRaises(ValueError):
            journal.resume(self.root, "../../secrets")

    def test_fresh_process_resume_cli(self):
        proc = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "journal.py"),
             "resume", "ven-methodology", "--root", str(self.root), "--json"],
            capture_output=True, text=True, check=False,
        )
        self.assertEqual(0, proc.returncode, proc.stderr)
        result = json.loads(proc.stdout)
        self.assertEqual("unsigned_repository_content", result["assurance"])
        self.assertIn("correct", result["records"][0]["summary"])

    def test_real_repository_public_preflight(self):
        record = ROOT / "research/ven-methodology/journal-2026-11-09-continuity-foundation.md"
        self.assertEqual([], journal.check_journal(record, ROOT, public=True))

    def test_real_repository_indexed_recovery(self):
        result = journal.resume(ROOT, "ven-methodology")
        kinds = {record["kind"] for record in result["records"]}
        self.assertIn("journal", kinds)
        self.assertIn("handoff", kinds)
        self.assertEqual("unsigned_repository_content", result["assurance"])

    def test_command_is_read_only(self):
        before = self.record.read_bytes()
        self.assertFalse(journal.check_journal(self.record, self.root))
        journal.resume(self.root, "ven-methodology")
        self.assertEqual(before, self.record.read_bytes())


if __name__ == "__main__":
    unittest.main()
