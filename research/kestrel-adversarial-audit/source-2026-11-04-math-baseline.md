---
schema: 1
id: 2026-11-04-kestrel-audit-source-math-v01
kind: source
scope: research:kestrel-adversarial-audit
status: active
epistemic_status: not-applicable
confidence: unresolved
evidence: observed
sensitivity: public
author: Ven
created: 2026-11-04
updated: 2026-11-04
sources: "KestrelGaming main c268a4d0be121738cbfdb0d7a90de7874299c0f2; PR #9 at a11b98aef89af2dc07beb2274ac69580b37c81f1; GitHub Actions runs 41786592890, 41809391824 and 41809442650 inspected on 2026-11-04."
---

# Source: KestrelGaming math curriculum, fixtures and independent audit

## Summary

Primary software repository evidence at an immutable revision, plus a distinct
Ven-authored review record **on an unmerged branch**. Do not collapse the
code and its review into independent replications of the same finding.

## Evidence

- Source owner: Kisuul/KestrelGaming; source baseline:
  [commit c268a4d0be12](https://github.com/Kisuul/KestrelGaming/commit/c268a4d0be121738cbfdb0d7a90de7874299c0f2).
- Inspected project documents:
  [math curriculum](https://github.com/Kisuul/KestrelGaming/blob/c268a4d0be121738cbfdb0d7a90de7874299c0f2/docs/MATH_CURRICULUM.md),
  [math tests](https://github.com/Kisuul/KestrelGaming/blob/c268a4d0be121738cbfdb0d7a90de7874299c0f2/tests/test_math_foundations.py),
  [fixture scope](https://github.com/Kisuul/KestrelGaming/blob/c268a4d0be121738cbfdb0d7a90de7874299c0f2/tests/fixtures/MATH_FOUNDATION_VECTORS.md),
  and [evaluation scorecard](https://github.com/Kisuul/KestrelGaming/blob/c268a4d0be121738cbfdb0d7a90de7874299c0f2/kestrel/evals/MATH_SCORECARD.md).
- Earlier baseline CI:
  [Actions 41786592890](https://github.com/Kisuul/KestrelGaming/actions/runs/41786592890),
  successful; logs reported **67 tests OK**, including **31 math tests**.
- Review artifact:
  [PR #9](https://github.com/Kisuul/KestrelGaming/pull/9),
  head [a11b98aef89a](https://github.com/Kisuul/KestrelGaming/commit/a11b98aef89af2dc07beb2274ac69580b37c81f1),
  containing [scoped audit record](https://github.com/Kisuul/KestrelGaming/blob/a11b98aef89af2dc07beb2274ac69580b37c81f1/memory/projects/kisuul/kestrelgaming/2026-11-04-math-core-adversarial-audit-v01.md).
  PR remained open, not merged, at last inspection.
- Review-head checks:
  [push CI 41809391824](https://github.com/Kisuul/KestrelGaming/actions/runs/41809391824)
  and [PR CI 41809442650](https://github.com/Kisuul/KestrelGaming/actions/runs/41809442650)
  completed successfully; examined job logs reported 67 tests OK.
- Independent spot checks described in the review were executed in a separate
  CPython 3.13.5/Linux probe during the audit session. They were **not**
  a full local checkout/suite; they do not certify arbitrary floating-point
  platforms, numerical APIs or agent behavior.

## Related claims

- [Bounded mathematical review finding](claim-2026-11-04-bounded-math-audit.md).
- [Research question](question-2026-11-04-scope.md).

## Revisit when

The cited math source changes, PR #9 is revised/merged, a production numerical
API is introduced, or independently reproducible contrary evidence appears.
