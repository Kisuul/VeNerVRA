---
schema: 1
id: 2026-11-09-ven-2101-remediation-handoff
kind: handoff
scope: research:ven-methodology
status: active
epistemic_status: not-applicable
confidence: unresolved
evidence: observed
sensitivity: public
author: ven
created: 2026-11-09
updated: 2026-11-09
sources: "2.1.0 baseline a0b1032e957c144eab8ab154d25292b5192be533; hostile run 42589570083; remediation branch test run 42594501832 at 8d8714fa318c67911c427f5fb5cfd5c6a0b91053; final head must be rechecked."
---

# Checkpoint: 2.1.0.1 hostile-remediation candidate

## Summary

- **Objective:** Fix all four reproduced journal-reader weaknesses without changing Ven's 2.0 identity contract or claiming new runtime authority.
- **Status:** PARTIAL release gate — deterministic regression evidence exists; fresh-model continuity remains NOT RUN.
- **Baseline:** PR #4 2.1.0 at a0b1032e957c144eab8ab154d25292b5192be533.
- **Patch:** fix/ven-2.1.0.1-hostile-remediation-2026-11-09; retrieve exact new head and tests before acting.
- **Relevant protocol:** [Journal protocol](../../ven/JOURNAL_PROTOCOL.md) and [release candidate](../../docs/ven-2.1/RELEASE_2.1.0.1.md).

## Evidence

- [2.1.0 hostile audit](journal-2026-11-09-hostile-corrections.md) records F-01 to F-04 and a negative control.
- [2.1.0.1 regression tests](../../tests/test_journal_regression_2101.py) invert the hostile probes into rejection assertions, also covering comments, code fences, repeated headings and cross-investigation ID collisions.
- [Patch CI](https://github.com/Kisuul/VeNerVRA/actions/runs/42594501832) passed 44 tests and structural checks at the recorded SHA, before this documentation was committed.
- **Not executed:** A new model instance with isolated context and independent evaluation of recovered evidence; cryptographic authorship; permission grants or revocation tests.
- The changed journal and handoff are sanitized public research-method notes, not transcripts or secrets, but human publication review remains necessary.

## Open decisions

Review the 2.1.0.1 patch on an exact SHA; settle whether to merge it into the 2.1.0 feature branch; choose and run a truly independent model-context recovery evaluation. Preserve the 2.1.0 audit findings even if the patch later passes.

## Next decisive check

Check CI at the final documentation commit, execute public-content preflight and reader recovery at that SHA, and independently assess F-01 through F-04 plus the unverified F-05 behavioral gate before granting release approval.

## Revisit when

The patch is re-reviewed, a future-model recovery test is run, privacy concerns surface, or new hostile fixtures falsify the current design.
