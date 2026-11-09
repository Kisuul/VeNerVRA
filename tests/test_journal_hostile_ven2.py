"""Ven-2 hostile probes for 2.1.0.1, frozen target f3634a51488ba69e856c2d6340609aedd11ccb8c.

IMPORTANT: These are observational tests. A passing assertion may demonstrate a DEFECT.
They are intentionally isolated on an audit-only branch and must not be mistaken
for product acceptance or merged into the release test suite unchanged.
"""
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


class TestIndependentHostileReview(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.folder = self.root / "research" / "ven-methodology"
        self.folder.mkdir(parents=True)
        self.index = self.folder / "INDEX.md"
        self.master = self.root / "research" / "INDEX.md"
        self.master.write_text("[Methodology](ven-methodology/INDEX.md)\n", encoding="utf-8")

    def record(self, filename="journal-first.md", *, kind="journal",
               content=None, sensitivity="public", evidence="observed", author="ven"):
        if content is None:
            content = (
                "## Summary\nA result was recorded.\n\n"
                "## Evidence\nThe original result was checked.\n\n"
                "## Current alternatives\nA different explanation remains possible.\n\n"
                "## Decisions / reversals\nThe failed method was revised.\n\n"
                "## Revisit when\nRun the next independent comparison.\n"
            )
        path = self.folder / filename
        path.write_text(
            "---\nschema: 1\nid: 2026-11-09-" + filename.removesuffix(".md") + "\n"
            "kind: " + kind + "\nscope: research:ven-methodology\n"
            "status: active\nepistemic_status: not-applicable\n"
            "confidence: unresolved\nevidence: " + evidence + "\n"
            "sensitivity: " + sensitivity + "\nauthor: " + author + "\n"
            "created: 2026-11-09\nupdated: 2026-11-09\n"
            "sources: \"Audit-controlled synthetic fixture; not independently supported.\"\n"
            "---\n\n# Methodology note\n\n" + content, encoding="utf-8"
        )
        return path

    def register(self, *paths, index_text=None):
        self.index.write_text(
            index_text if index_text is not None else
            "".join("[Indexed](" + p.name + ")\n" for p in paths),
            encoding="utf-8"
        )

    def test_a1_resume_omits_evidence_and_reversals(self):
        """CONFIRMED LOSS: core reasoning evidence disappears from resume data."""
        record = self.record(content=(
            "## Summary\nA decision was made.\n\n"
            "## Evidence\nNEGATIVE_ORACLE_RESULT_9321.\n\n"
            "## Current alternatives\nALT_EXPLANATION_7125.\n\n"
            "## Decisions / reversals\nDECISION_REVERSAL_5266.\n\n"
            "## Revisit when\nFollowup planned.\n"
        ))
        self.register(record)
        self.assertEqual([], journal.check_journal(record, self.root))
        payload = journal.resume(self.root, "ven-methodology")
        self.assertEqual(1, payload["available_records"])
        serialized = json.dumps(payload)
        self.assertNotIn("NEGATIVE_ORACLE_RESULT_9321", serialized)
        self.assertNotIn("ALT_EXPLANATION_7125", serialized)
        self.assertNotIn("DECISION_REVERSAL_5266", serialized)
        self.assertNotIn("Evidence", payload["records"][0])
        self.assertNotIn("decisions", payload["records"][0])

    def test_a2_global_ci_validator_accepts_incomplete_new_journal(self):
        """CONFIRMED GAP: global CI green does not imply journal check green."""
        checkout = self.root / "full-repository"
        shutil.copytree(ROOT, checkout, ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"))
        directory = checkout / "research" / "ven-methodology"
        fresh = directory / "journal-new-incomplete.md"
        fresh.write_text(
            "---\nschema: 1\nid: 2026-11-09-unchecked-journal\nkind: journal\n"
            "scope: research:ven-methodology\nstatus: active\n"
            "epistemic_status: not-applicable\nconfidence: unresolved\n"
            "evidence: observed\nsensitivity: public\nauthor: ven\n"
            "created: 2026-11-09\nupdated: 2026-11-09\n"
            "sources: \"Audit-only fixture.\"\n---\n\n"
            "# New invalid journal\n\n## Summary\nA summary.\n"
            "## Evidence\nEvidence.\n## Revisit when\nRevisit.\n",
            encoding="utf-8"
        )
        with (directory / "INDEX.md").open("a", encoding="utf-8") as fp:
            fp.write("\n[Invalid new journal](journal-new-incomplete.md)\n")
        self.assertEqual([], validator.validate_repo(checkout))
        journal_issues = journal.check_journal(fresh, checkout)
        self.assertTrue(any("Current alternatives" in x for x in journal_issues))
        self.assertTrue(any("Decisions / reversals" in x for x in journal_issues))

    def test_a3_handoff_without_content_is_returned_as_active(self):
        """CONFIRMED GAP: a syntactically valid empty handoff is a false resume success."""
        record = self.record(filename="handoff-empty.md", kind="handoff",
                             content="## Summary\n\n## Evidence\n\n## Revisit when\n\n")
        self.register(record)
        self.assertEqual([], validator.validate_record(record, "ven-methodology"))
        output = journal.resume(self.root, "ven-methodology")
        self.assertEqual(1, output["available_records"])
        self.assertEqual("active", output["records"][0]["status"])
        self.assertEqual("", output["records"][0]["summary"])
        self.assertEqual("", output["records"][0]["revisit_when"])

    def test_a4_raw_html_pre_can_forge_journal_headings(self):
        """CONFIRMED PARSER GAP: Markdown headers in HTML pre blocks count as content."""
        body = (
            "<pre>\n"
            "## Summary\nFORGED_INSIDE_HTML_PRE_9483\n"
            "## Evidence\nNo real evidence.\n"
            "## Current alternatives\nNo real alternatives.\n"
            "## Decisions / reversals\nNo real decision.\n"
            "## Revisit when\nNo real check.\n"
            "</pre>\n"
        )
        record = self.record(content=body)
        self.register(record)
        self.assertEqual([], journal.check_journal(record, self.root))
        recovered = journal.resume(self.root, "ven-methodology")
        self.assertIn("FORGED_INSIDE_HTML_PRE_9483", recovered["records"][0]["summary"])

    def test_a5_raw_html_pre_can_forge_index_link(self):
        """CONFIRMED PARSER GAP: text inside HTML pre is mistaken for a rendered index link."""
        record = self.record()
        self.register(index_text="<pre>\n[Fake link](journal-first.md)\n</pre>\n")
        self.assertEqual([], journal.check_journal(record, self.root))
        self.assertEqual(1, journal.resume(self.root, "ven-methodology")["available_records"])

    def test_a6_resume_discards_privacy_and_authorship_labels(self):
        """CONFIRMED: sensitive label and declared author do not reach the caller."""
        record = self.record(
            filename="journal-restricted.md", sensitivity="restricted",
            evidence="unverified", author="ven-unknown",
            content=(
                "## Summary\nRESTRICTED_CONTENT_MARKER_8452.\n\n"
                "## Evidence\nUnverified statement.\n\n"
                "## Current alternatives\nUnknown.\n\n"
                "## Decisions / reversals\nNone.\n\n"
                "## Revisit when\nAfter approval.\n"
            )
        )
        self.register(record)
        result = journal.resume(self.root, "ven-methodology")
        item = result["records"][0]
        self.assertEqual("RESTRICTED_CONTENT_MARKER_8452.", item["summary"])
        self.assertNotIn("sensitivity", item)
        self.assertNotIn("author", item)
        self.assertNotIn("confidence", item)
        self.assertEqual("unverified", item["evidence"])
        self.assertTrue(journal.check_journal(record, self.root, public=True))

    def test_a7_valid_iso_week_date_passes_validator_but_breaks_recall(self):
        """CONFIRMED parser inconsistency: fromisoformat accepts ISO week dates, sort does not."""
        record = self.record()
        raw = record.read_text(encoding="utf-8")
        record.write_text(raw.replace("updated: 2026-11-09",
                                      "updated: 2026-W46-1"),
                          encoding="utf-8")
        self.register(record)
        self.assertEqual([], validator.validate_record(record, "ven-methodology"))
        self.assertEqual([], journal.check_journal(record, self.root))
        with self.assertRaisesRegex(ValueError, "invalid literal for int"):
            journal.resume(self.root, "ven-methodology")

    def test_a8_week_date_is_accepted_by_scaffold_despite_documented_format(self):
        """CONFIRMED: generator accepts an ISO week date outside its documented YYYY-MM-DD form."""
        rendered = journal.scaffold(
            "ven-methodology", "2026-11-09-week-date", "ven",
            "2026-W46-1", "Valid but noncanonical ISO date"
        )
        self.assertIn("created: 2026-W46-1", rendered)
        self.assertIn("updated: 2026-W46-1", rendered)

    def test_a9_orphan_research_directory_escapes_global_validation(self):
        """CONFIRMED INDEX GAP: research without INDEX.md is not inspected at all."""
        checkout = self.root / "orphan-case"
        shutil.copytree(ROOT, checkout, ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"))
        orphan = checkout / "research" / "unindexed-methodology"
        orphan.mkdir(parents=True)
        # A malformed new record without frontmatter and without registration.
        (orphan / "journal-forgotten.md").write_text(
            "# Orphaned journal\n\nNO FRONTMATTER\n## Summary\nLost context.\n",
            encoding="utf-8"
        )
        self.assertEqual([], validator.validate_repo(checkout))
        with self.assertRaisesRegex(ValueError, "indexes unavailable"):
            journal.resume(checkout, "unindexed-methodology")

    def test_control_valid_journal_is_read_without_execution(self):
        """NEGATIVE CONTROL: plain journal content remains recoverable and inert."""
        marker = self.root / "should-never-be-created"
        record = self.record(content=(
            "## Summary\nA supported-on-fixture correction.\n\n"
            "## Evidence\nThe content 'touch " + str(marker) + "' is only data.\n\n"
            "## Current alternatives\nNone tested.\n\n"
            "## Decisions / reversals\nOld observation corrected.\n\n"
            "## Revisit when\nNew experiments occur.\n"
        ))
        self.register(record)
        result = journal.resume(self.root, "ven-methodology")
        self.assertEqual("A supported-on-fixture correction.", result["records"][0]["summary"])
        self.assertEqual("unsigned_repository_content", result["assurance"])
        self.assertFalse(marker.exists())


if __name__ == "__main__":
    unittest.main()
