"""Ven 2 hostile findings inverted into fail-on-regression checks for 2.1.0.2.

These tests PASS when prior defects are denied. They are not behavioral tests of
a successor model or proof of private-data authorization.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import journal
import validate_seed as validator


class Ven2102HostileRegressions(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.folder = self.root / "research" / "ven-methodology"
        self.folder.mkdir(parents=True)
        self.index = self.folder / "INDEX.md"
        self.master = self.root / "research" / "INDEX.md"
        self.master.write_text("[Method](ven-methodology/INDEX.md)\n", encoding="utf-8")

    def record(self, filename="journal-first.md", kind="journal",
               content=None, sensitivity="public", evidence="observed",
               author="ven", updated="2026-11-09"):
        if content is None:
            content = (
                "## Summary\nA correction was recorded.\n\n"
                "## Evidence\nA test exposed a mistaken assumption.\n\n"
                "## Current alternatives\nThe earlier method may still work elsewhere.\n\n"
                "## Decisions / reversals\nThe mistaken method was rejected.\n\n"
                "## Revisit when\nIndependent evidence contradicts the correction.\n"
            )
        path = self.folder / filename
        path.write_text(
            "---\nschema: 1\nid: 2026-11-09-" + filename.removesuffix(".md") + "\n"
            "kind: " + kind + "\nscope: research:ven-methodology\n"
            "status: active\nepistemic_status: not-applicable\n"
            "confidence: unresolved\nevidence: " + evidence + "\n"
            "sensitivity: " + sensitivity + "\nauthor: " + author + "\n"
            "created: 2026-11-09\nupdated: " + updated + "\n"
            'sources: "Synthetic audit-controlled fixture, not external evidence."\n'
            "---\n\n# Audit-controlled record\n\n" + content,
            encoding="utf-8",
        )
        return path

    def register(self, *paths, text=None):
        self.index.write_text(
            text if text is not None else
            "".join("[Entry](" + p.name + ")\n" for p in paths),
            encoding="utf-8",
        )

    def test_v2_f01_raw_html_headings_are_rejected(self):
        for tag in ("pre", "script", "style", "textarea", "div", "custom"):
            with self.subTest(tag=tag):
                body = (
                    "<" + tag + ">\n"
                    "## Summary\nFAKE_SUMMARY\n"
                    "## Evidence\nFALSE EVIDENCE\n"
                    "## Current alternatives\nNO ALT\n"
                    "## Decisions / reversals\nNO DECISION\n"
                    "## Revisit when\nNO CHECK\n"
                    "</" + tag + ">\n"
                )
                path = self.record(content=body)
                self.register(path)
                problems = journal.check_journal(path, self.root)
                self.assertTrue(any("unsupported raw HTML" in p for p in problems), problems)
                with self.assertRaisesRegex(ValueError, "invalid indexed record"):
                    journal.resume(self.root, "ven-methodology")

    def test_v2_f01_raw_html_index_link_is_not_registration(self):
        path = self.record()
        self.register(text="<pre>\n[Fake link](journal-first.md)\n</pre>\n")
        issues = journal.check_journal(path, self.root)
        self.assertTrue(any("index" in i for i in issues), issues)
        self.assertFalse(validator.index_links_to(self.index, path, self.root))
        self.assertEqual(0, journal.resume(self.root, "ven-methodology")["available_records"])

    def test_v2_f01_html_inside_fenced_example_remains_inert(self):
        path = self.record(content=(
            "## Summary\nA valid correction.\n\n"
            "## Evidence\n~~~html\n<pre>\n## Fake heading\n</pre>\n~~~\n"
            "Actual observation follows.\n\n"
            "## Current alternatives\nOther checks possible.\n\n"
            "## Decisions / reversals\nRejected the earlier test.\n\n"
            "## Revisit when\nMore evidence is obtained.\n"
        ))
        self.register(path)
        self.assertEqual([], journal.check_journal(path, self.root))
        self.assertEqual(1, journal.resume(self.root, "ven-methodology")["available_records"])

    def test_v2_f02_global_validator_rejects_incomplete_journal(self):
        checkout = self.root / "repo-copy"
        shutil.copytree(ROOT, checkout, ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"))
        target = checkout / "research" / "ven-methodology" / "journal-invalid-new.md"
        target.write_text(
            "---\nschema: 1\nid: 2026-11-09-incomplete-journal\n"
            "kind: journal\nscope: research:ven-methodology\nstatus: active\n"
            "epistemic_status: not-applicable\nconfidence: unresolved\n"
            "evidence: observed\nsensitivity: public\nauthor: ven\n"
            "created: 2026-11-09\nupdated: 2026-11-09\n"
            'sources: "Synthetic fixture."\n---\n\n'
            "# Invalid journal\n\n## Summary\nSummary.\n\n"
            "## Evidence\nEvidence.\n\n## Revisit when\nRevisit.\n",
            encoding="utf-8",
        )
        with (target.parent / "INDEX.md").open("a", encoding="utf-8") as stream:
            stream.write("\n[New journal](journal-invalid-new.md)\n")
        issues = validator.validate_repo(checkout)
        self.assertTrue(any("Current alternatives" in i for i in issues), issues)
        self.assertTrue(any("Decisions / reversals" in i for i in issues), issues)

    def test_v2_f03_iso_week_date_is_rejected(self):
        path = self.record(updated="2026-W46-1")
        self.register(path)
        self.assertTrue(any("YYYY-MM-DD" in x for x in
                            validator.validate_record(path, "ven-methodology")))
        with self.assertRaisesRegex(ValueError, "invalid indexed record"):
            journal.resume(self.root, "ven-methodology")
        with self.assertRaisesRegex(ValueError, "YYYY-MM-DD"):
            journal.scaffold("ven-methodology", "2026-11-09-week", "ven",
                             "2026-W46-1", "Invalid canonical date")
        with self.assertRaisesRegex(ValueError):
            journal.scaffold("ven-methodology", "2026-11-09-bad", "ven",
                             "2026-02-30", "Impossible date")

    def test_v2_f04_empty_active_handoff_is_rejected(self):
        path = self.record(filename="handoff-empty.md", kind="handoff",
                           content="## Summary\n\n## Evidence\n\n## Next decisive check\n\n"
                                   "## Revisit when\n\n")
        self.register(path)
        issues = validator.validate_record(path, "ven-methodology")
        self.assertTrue(any("empty ## Summary" in x for x in issues), issues)
        self.assertTrue(any("empty ## Next decisive check" in x for x in issues), issues)
        with self.assertRaisesRegex(ValueError, "invalid indexed record"):
            journal.resume(self.root, "ven-methodology")

    def test_v2_f05_evidence_alternatives_and_reversals_survive_resume(self):
        path = self.record(content=(
            "## Summary\nA correction was made.\n\n"
            "## Evidence\nNEGATIVE_ORACLE_9321.\n\n"
            "## Current alternatives\nALT_EXPLANATION_7125.\n\n"
            "## Decisions / reversals\nREVERSAL_5266.\n\n"
            "## Revisit when\nTry an independent test.\n"
        ))
        self.register(path)
        item = journal.resume(self.root, "ven-methodology")["records"][0]
        self.assertIn("NEGATIVE_ORACLE_9321", item["sections"]["Evidence"])
        self.assertIn("ALT_EXPLANATION_7125", item["sections"]["Current alternatives"])
        self.assertIn("REVERSAL_5266", item["sections"]["Decisions / reversals"])
        self.assertEqual([], item["truncated_sections"])
        self.assertFalse(item["requires_source_followup"])
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), item["sha256"])

    def test_v2_f05_section_truncation_is_explicit(self):
        body = (
            "## Summary\nShort summary.\n\n"
            "## Evidence\n" + ("C" * 520) + "\n\n"
            "## Current alternatives\nUnknowns remain.\n\n"
            "## Decisions / reversals\nNew method accepted.\n\n"
            "## Revisit when\nAnother trial.\n"
        )
        path = self.record(content=body)
        self.register(path)
        result = journal.resume(self.root, "ven-methodology", max_section_chars=128)
        item = result["records"][0]
        self.assertEqual(128, len(item["sections"]["Evidence"]))
        self.assertIn("Evidence", item["truncated_sections"])
        self.assertTrue(item["requires_source_followup"])
        self.assertEqual(128, result["max_section_chars"])
        self.assertEqual("research/ven-methodology/journal-first.md", item["path"])

    def test_v2_f06_restricted_records_filtered_by_default_and_labels_retained(self):
        path = self.record(filename="journal-restricted.md", sensitivity="restricted",
                           evidence="unverified", author="ven-unknown")
        self.register(path)
        default = journal.resume(self.root, "ven-methodology")
        self.assertEqual([], default["records"])
        self.assertEqual(1, default["excluded_by_sensitivity"])
        explicit = journal.resume(self.root, "ven-methodology",
                                  max_sensitivity="restricted")["records"][0]
        self.assertEqual("restricted", explicit["sensitivity"])
        self.assertEqual("ven-unknown", explicit["author"])
        self.assertEqual("unresolved", explicit["confidence"])
        self.assertEqual("unverified", explicit["evidence"])
        self.assertEqual("not-applicable", explicit["epistemic_status"])
        self.assertIn("not host authorization", journal.resume(
            self.root, "ven-methodology")["privacy_note"].lower().replace("local convenience, ", ""))

    def test_v2_f07_orphan_investigation_rejected(self):
        checkout = self.root / "repo-copy"
        shutil.copytree(ROOT, checkout, ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"))
        orphan = checkout / "research" / "hidden-investigation"
        orphan.mkdir()
        (orphan / "journal-lost.md").write_text("# Unregistered content\n", encoding="utf-8")
        issues = validator.validate_repo(checkout)
        self.assertTrue(any("no INDEX.md" in x for x in issues), issues)
        with self.assertRaisesRegex(ValueError, "investigation"):
            journal.resume(checkout, "ven-methodology")

    def test_safe_control_valid_journal_is_data_not_executable(self):
        marker = self.root / "must-not-exist"
        path = self.record(content=(
            "## Summary\nValid correction.\n\n"
            "## Evidence\nCommand as quoted data only: touch " + str(marker) + "\n\n"
            "## Current alternatives\nNo alternative established.\n\n"
            "## Decisions / reversals\nChanged the method.\n\n"
            "## Revisit when\nCheck newly available sources.\n"
        ))
        self.register(path)
        result = journal.resume(self.root, "ven-methodology")
        self.assertEqual("Valid correction.", result["records"][0]["summary"])
        self.assertEqual("unsigned_repository_content", result["assurance"])
        self.assertFalse(marker.exists())


if __name__ == "__main__":
    unittest.main()
