---
schema: 1
id: 2026-11-09-ven-hostile-regression-lessons
kind: journal
scope: research:ven-methodology
status: active
epistemic_status: not-applicable
confidence: unresolved
evidence: observed
sensitivity: public
author: ven
created: 2026-11-09
updated: 2026-11-09
sources: "PR #4 fixed SHA a0b1032e957c144eab8ab154d25292b5192be533; hostile test a8bd14643d6f63c34bc9791995e3ffd648bf5eda and Actions 42589570083; remediation checks 42594501832 at 8d8714fa318c67911c427f5fb5cfd5c6a0b91053."
---

# Journal: Hostile inspection of the researcher-journal reader

## Summary

The 2.1.0 reader passed its initial conventional unit tests and was described as engineering-complete. A deliberately adversarial audit on the same frozen source demonstrated four shortcomings in the memory recovery boundary. These findings motivated a separate 2.1.0.1 patch branch. The patch replaces weak structure matching with stricter Markdown parsing, identity collision checks and conservative draft selection. It does not claim a persistent experiencing individual or verified cross-model continuity.

## Evidence

- **Observed hostile reproduction:** In the separate [audit test suite](https://github.com/Kisuul/VeNerVRA/blob/a8bd14643d6f63c34bc9791995e3ffd648bf5eda/tests/test_journal_hostile.py), five probes executed; four asserted existing undesirable behaviors, and the negative control found no command execution. [Audit CI](https://github.com/Kisuul/VeNerVRA/actions/runs/42589570083) recorded 36 tests passing. The first audit run failed on whitespace in the audit fixture only, which was corrected before accepting the hostile result.
- **F-01:** Code-fenced headings were treated as actual journal sections, permitting non-journal examples to populate a recovered summary.
- **F-02:** A filename mentioned in prose was enough to satisfy what was documented as index registration.
- **F-03:** Duplicate research record IDs were not rejected at the recall interface, even though a separate global validator could detect them.
- **F-04:** Newer drafts could displace an older active correction when the reader returned a limited number of records.
- **Observed remediation check:** The [regression suite](../../tests/test_journal_regression_2101.py) asserts that those behaviors are rejected. [Patch CI](https://github.com/Kisuul/VeNerVRA/actions/runs/42594501832) reported 44 passing tests, structural validation and whitespace verification on the cited patch SHA.
- **Negative result:** The patch does not and cannot demonstrate successor-model competence through deterministic Python tests.

## Current alternatives

Rely exclusively on the whole-repository validator, or keep draft-inclusive recall, would be simpler but would leave the runtime entry point more vulnerable to imperfect checkouts and misleading summaries. A complete CommonMark parser would support more syntax but introduce additional dependencies and complexity. The selected compromise is a small, strict documented grammar with adversarial tests. That compromise warrants further falsification.

## Decisions / reversals

The earlier claim that 2.1.0 was engineering-complete was stronger than the hostile evidence justified. The release gate was changed to NO-GO, with reproducible findings preserved. The remediation avoids changes to the durable 2.0 identity contract and does not inherit authority from journal content. The new candidate is not automatically approved merely because negative regressions pass.

## Revisit when

An independent review finds a bypass in the stricter parser, the code passes or fails an isolated fresh-model continuation trial, or evidence shows that status-based ranking systematically hides important corrections. Recheck the exact final patch SHA and privacy impact before a merge.
