"""Seed invariants; do not mistake these for behavioral agent evaluation."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TestContract(unittest.TestCase):
    def test_identity_not_software_agent(self):
        contract = (ROOT / 'VEN.md').read_text()
        self.assertIn('Value-Neutral Virtual Research Assistant', contract)
        self.assertIn('Research-Journal', contract)
        self.assertIn('Source Rule', contract)

    def test_memory_does_not_authorize_actions(self):
        contract = (ROOT / 'VEN.md').read_text().lower()
        self.assertIn('memory', contract)
        self.assertIn('permissions', contract)
        self.assertIn('not', contract)

    def test_original_source_preserved(self):
        source = (ROOT / 'docs/source/VeNerVRA-1.1.txt').read_text()
        self.assertIn('Value-Neutral Virtual Research Assistant', source)
        self.assertIn('Default to Research-Journal mode', source)
        self.assertIn('Source Rule (Detect Error)', source)

    def test_candidate_skills_are_not_active(self):
        self.assertFalse((ROOT / 'skills').exists(), 'Candidate skill location must be staged under integration')
        for name in ('research-source-evaluation', 'research-claim-management', 'research-continuity'):
            self.assertTrue((ROOT / f'integration/kestrel/candidates/{name}/SKILL.md').exists())

    def test_synthetic_fixture_has_no_fake_benchmark(self):
        example = (ROOT / 'research/examples/synthetic-cache/handoff-2026-11-04-cache.md').read_text()
        self.assertIn('NOT RUN', example)
        self.assertIn('synthetic', example.lower())


if __name__ == '__main__':
    unittest.main()
