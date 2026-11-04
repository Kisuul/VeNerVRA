"""Read-only validator regression tests; NOT agent-behavior experiments."""
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import validate_seed as validator


class TestValidator(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'seed'
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        self.sample = self.root / 'research/examples/synthetic-cache'

    def issues(self):
        return validator.validate_repo(self.root)

    def test_clean_seed_passes(self):
        self.assertEqual([], self.issues())

    def test_missing_contract_fails(self):
        (self.root / 'VEN.md').unlink()
        self.assertTrue(any('VEN.md' in issue for issue in self.issues()))

    def test_invalid_status_fails(self):
        p = self.sample / 'hypothesis-2026-11-04-cache.md'
        p.write_text(p.read_text().replace('status: draft', 'status: certified', 1))
        self.assertTrue(any('unsupported status' in issue for issue in self.issues()))

    def test_duplicate_id_fails(self):
        p = self.sample / 'hypothesis-2026-11-04-cache.md'
        p.write_text(p.read_text().replace('2026-11-04-cache-speed-hypothesis', '2026-11-04-cache-question', 1))
        self.assertTrue(any('duplicate id' in issue for issue in self.issues()))

    def test_unindexed_record_fails(self):
        original = self.sample / 'hypothesis-2026-11-04-cache.md'
        new = self.sample / 'hypothesis-second.md'
        new.write_text(original.read_text().replace('2026-11-04-cache-speed-hypothesis', '2026-11-04-different-hypothesis', 1))
        self.assertTrue(any('record missing from nearest INDEX.md' in issue for issue in self.issues()))

    def test_wrong_scope_fails(self):
        p = self.sample / 'question-2026-11-04-cache.md'
        p.write_text(p.read_text().replace('scope: research:synthetic-cache', 'scope: research:someone-else'))
        self.assertTrue(any('scope must be' in issue for issue in self.issues()))

    def test_updated_before_created_fails(self):
        p = self.sample / 'question-2026-11-04-cache.md'
        p.write_text(p.read_text().replace('updated: 2026-11-04', 'updated: 2025-11-04'))
        self.assertTrue(any('earlier than created' in issue for issue in self.issues()))

    def test_broken_local_link_fails(self):
        p = self.root / 'README.md'
        p.write_text(p.read_text() + '\n[broken](not-a-real-file.md)\n')
        self.assertTrue(any('broken link' in issue for issue in self.issues()))

    def test_missing_revisit_section_fails(self):
        p = self.sample / 'handoff-2026-11-04-cache.md'
        p.write_text(p.read_text().replace('## Revisit when', '## Absent heading'))
        self.assertTrue(any('missing ## Revisit when' in issue for issue in self.issues()))

    def test_claim_requires_epistemic_status(self):
        p = self.sample / 'hypothesis-2026-11-04-cache.md'
        p.write_text(p.read_text().replace('epistemic_status: proposed', 'epistemic_status: not-applicable'))
        self.assertTrue(any('claim or hypothesis cannot' in issue for issue in self.issues()))

    def test_superseded_requires_link(self):
        p = self.sample / 'hypothesis-2026-11-04-cache.md'
        p.write_text(p.read_text().replace('status: draft', 'status: superseded', 1))
        self.assertTrue(any('superseded record missing' in issue for issue in self.issues()))

    def test_no_escape_from_repo(self):
        p = self.root / 'README.md'
        p.write_text(p.read_text() + '\n[bad](../../private.txt)\n')
        self.assertTrue(any('escapes repository' in issue for issue in self.issues()))


if __name__ == '__main__':
    unittest.main()
