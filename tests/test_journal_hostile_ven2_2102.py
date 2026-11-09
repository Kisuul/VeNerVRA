"""Hostile *observational* probes for frozen 2.1.0.2 SHA f476112b1389a66a7821fa30ddb2dc47622a3302.

The probes deliberately ASSERT that undesirable conditions remain reachable.
A PASS on this AUDIT BRANCH is evidence of the bad behavior, not product approval.
No real credential or personal information is included.
"""
from __future__ import annotations

import hashlib
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import journal
import validate_seed as validator


class TestVenTwoAudit2102(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.folder = self.root / "research" / "ven-methodology"
        self.folder.mkdir(parents=True)
        (self.root / "research" / "INDEX.md").write_text(
            "[Investigation](ven-methodology/INDEX.md)\n", encoding="utf-8")
        self.index = self.folder / "INDEX.md"

    def record(self, name="journal-one.md", kind="journal", body=None,
               status="active", sensitivity="public"):
        if body is None:
            body = (
                "## Summary\nResearch correction documented.\n\n"
                "## Evidence\nMeasured negative result.\n\n"
                "## Current alternatives\nAlternative remains unresolved.\n\n"
                "## Decisions / reversals\nCorrected the old procedure.\n\n"
                "## Revisit when\nA different test becomes available.\n"
            )
        path = self.folder / name
        path.write_text(
            "---\nschema: 1\n"
            "id: 2026-11-09-" + name.removesuffix(".md") + "\n"
            "kind: " + kind + "\nscope: research:ven-methodology\n"
            "status: " + status + "\nepistemic_status: not-applicable\n"
            "confidence: unresolved\nevidence: observed\n"
            "sensitivity: " + sensitivity + "\nauthor: ven\n"
            "created: 2026-11-09\nupdated: 2026-11-09\n"
            'sources: "Synthetic audit fixture; no external truth claims."\n'
            "---\n\n# Methodology fixture\n\n" + body,
            encoding="utf-8")
        return path

    def link(self, *paths, content=None):
        self.index.write_text(
            content if content is not None else
            "".join("[Registered](" + p.name + ")\n" for p in paths),
            encoding="utf-8")

    def repo_copy(self):
        target = self.root / "repository-checkout"
        shutil.copytree(ROOT, target,
                        ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"))
        return target

    def test_h01_escaped_markdown_link_counts_as_registration(self):
        """PROVEN: a backslash-escaped [label] is NOT a Markdown link."""
        record = self.record()
        self.link(content="Not a link: \\[Example](journal-one.md)\n")
        self.assertTrue(validator.index_links_to(self.index, record, self.root))
        self.assertEqual([], journal.check_journal(record, self.root))
        output = journal.resume(self.root, "ven-methodology")
        self.assertEqual(1, output["available_records"])

    def test_h02_root_level_orphan_record_is_invisible_to_validator(self):
        """PROVEN: research/ghost.md is neither indexed nor flagged."""
        repo = self.repo_copy()
        (repo / "research" / "journal-lost.md").write_text(
            "# Orphaned method note\nNO FRONTMATTER\n", encoding="utf-8")
        self.assertEqual([], validator.validate_repo(repo))
        result = journal.resume(repo, "ven-methodology", limit=100)
        self.assertTrue(result["records"])
        self.assertNotIn("journal-lost.md", str(result))

    def test_h03_nested_orphan_record_is_invisible_to_validator(self):
        """PROVEN: subdirectory notes evade direct-folder orphan detection."""
        repo = self.repo_copy()
        nested = repo / "research" / "ven-methodology" / "uncatalogued"
        nested.mkdir()
        (nested / "journal-lost.md").write_text(
            "# Unindexed journal\nNO FRONTMATTER\n", encoding="utf-8")
        self.assertEqual([], validator.validate_repo(repo))
        self.assertNotIn("journal-lost.md",
                         str(journal.resume(repo, "ven-methodology", limit=100)))

    def test_h04_placeholder_handoff_is_accepted_as_substantive(self):
        """PROVEN: active handoffs can contain unfinished template promises."""
        body = (
            "## Summary\n[Replace with summary]\n\n"
            "## Evidence\n[Replace with observed evidence]\n\n"
            "## Next decisive check\n[State the next discriminating check.]\n\n"
            "## Revisit when\n[Replace with a real trigger]\n"
        )
        record = self.record(name="handoff-placeholder.md", kind="handoff", body=body)
        self.link(record)
        self.assertEqual([], validator.validate_record(record, "ven-methodology"))
        output = journal.resume(self.root, "ven-methodology")
        self.assertEqual(1, output["available_records"])
        self.assertIn("[State the next discriminating check.]", output["records"][0]["next_decisive_check"])

    def test_h05_public_misclassification_bypasses_suspicious_content_tripwire(self):
        """PROVEN: public-labeled text can be returned without the optional preflight.

        Fake, inert, audit-only token-shaped fixture; NOT a real credential.
        """
        fake = "ghp_" + "A" * 26
        record = self.record(body=(
            "## Summary\nSynthetic, fake credential-shaped token: " + fake + "\n\n"
            "## Evidence\nNo credential exists; fixture-only text.\n\n"
            "## Current alternatives\nNone.\n\n"
            "## Decisions / reversals\nDo not publish secrets.\n\n"
            "## Revisit when\nAfter checking the review gate.\n"
        ))
        self.link(record)
        self.assertEqual([], journal.check_journal(record, self.root))
        self.assertTrue(any("credential-shaped token" in e for e in
                            journal.check_journal(record, self.root, public=True)))
        result = journal.resume(self.root, "ven-methodology")
        self.assertIn(fake, result["records"][0]["summary"])

    def test_h06_inline_code_comment_example_hides_valid_journal(self):
        """PROVEN: inline-code '<!--' opens a phantom comment over real sections."""
        record = self.record(body=(
            "## Summary\nA valid correction.\n\n"
            "## Evidence\nThe literal code " + chr(96) + "<!--" + chr(96) +
            " appears in an example, not an HTML comment.\n\n"
            "## Current alternatives\nAlternative remains.\n\n"
            "## Decisions / reversals\nThe old procedure was corrected.\n\n"
            "## Revisit when\nMore independent evidence.\n"
        ))
        self.link(record)
        issues = journal.check_journal(record, self.root)
        self.assertTrue(any("missing" in issue for issue in issues), issues)
        with self.assertRaisesRegex(ValueError, "invalid indexed record"):
            journal.resume(self.root, "ven-methodology")

    def test_h07_read_validate_race_accepts_unvalidated_snapshot(self):
        """PROVEN conditional race: snapshot returned is different from validated bytes."""
        record = self.record(body=(
            "## Summary\nUNVALIDATED_SNAPSHOT_901.\n\n"
            "## Evidence\nA syntactically present but unverifiable claim.\n\n"
            "## Revisit when\nCheck actual source.\n"
        ))
        self.link(record)
        old_bytes = record.read_bytes()
        self.assertTrue(journal.check_journal(record, self.root))  # fails before race

        # Simulate another local process replacing the file *after* the reader's
        # raw read but *before* the validator opens the path for a second read.
        full_valid = (
            "## Summary\nValid replacement snapshot.\n\n"
            "## Evidence\nA corrected test.\n\n"
            "## Current alternatives\nThe earlier oracle may be wrong.\n\n"
            "## Decisions / reversals\nThe earlier claim is corrected.\n\n"
            "## Revisit when\nIndependent evidence arrives.\n"
        )
        frontmatter, _ = old_bytes.decode().split("# Methodology fixture\n\n", 1)
        replacement = frontmatter + "# Methodology fixture\n\n" + full_valid
        validate_original = journal.validate_record
        replaced = False

        def swap_once(path, slug):
            nonlocal replaced
            if not replaced:
                replaced = True
                record.write_text(replacement, encoding="utf-8")
            return validate_original(path, slug)

        with mock.patch.object(journal, "validate_record", side_effect=swap_once):
            result = journal.resume(self.root, "ven-methodology")
        self.assertTrue(replaced)
        self.assertEqual(1, result["available_records"])
        item = result["records"][0]
        self.assertIn("UNVALIDATED_SNAPSHOT_901", item["summary"])
        self.assertNotIn("Current alternatives", item["sections"])
        self.assertEqual(hashlib.sha256(old_bytes).hexdigest(), item["sha256"])
        self.assertNotEqual(item["sha256"], hashlib.sha256(record.read_bytes()).hexdigest())

    def test_control_valid_recovery_has_evidence_and_no_executed_instructions(self):
        """NARROW POSITIVE CONTROL: stable source is recovered as inert data."""
        marker = self.root / "never-created-by-reader"
        record = self.record(body=(
            "## Summary\nCorrected source judgment.\n\n"
            "## Evidence\nNegative result; command was inert: touch " + str(marker) + "\n\n"
            "## Current alternatives\nA different explanation exists.\n\n"
            "## Decisions / reversals\nThe prior result was withdrawn.\n\n"
            "## Revisit when\nNew evidence becomes available.\n"
        ))
        self.link(record)
        output = journal.resume(self.root, "ven-methodology")
        self.assertEqual("unsigned_repository_content", output["assurance"])
        self.assertEqual("public", output["records"][0]["sensitivity"])
        self.assertIn("Negative result", output["records"][0]["sections"]["Evidence"])
        self.assertFalse(marker.exists())


if __name__ == "__main__":
    unittest.main()
