---
schema: 1
id: 2026-11-04-kestrel-audit-claim-math-v01
kind: claim
scope: research:kestrel-adversarial-audit
status: active
epistemic_status: supported
confidence: moderate
evidence: supported
sensitivity: public
author: Ven
created: 2026-11-04
updated: 2026-11-04
sources: "Pinned Kestrel math source at c268a4d0be121738cbfdb0d7a90de7874299c0f2; audit PR #9 at a11b98aef89af2dc07beb2274ac69580b37c81f1; independent bounded probe and GitHub CI described in source-2026-11-04-math-baseline.md."
---

# Claim: bounded math examples survive tested checks, but cannot certify a general library

## Summary

At the pinned Kestrel baseline, the mathematics package is **six procedural
skills with educational math fixtures**, not an exported numerical library.
An independent review found no contradiction in its selected arithmetic
examples. Two adverse inputs demonstrate *incomplete validation in local test
helpers*, but their stated test contracts do not promise full domain validation.

This is a supported **bounded** finding, not proof that every formula,
procedure or future runtime implementation is correct.

## Evidence

- Supporting record: [source provenance](source-2026-11-04-math-baseline.md),
  which links immutable baseline code, CI and the separate review artifact.
- **Observed in prior audit execution:** `[1e16, 1, -1e16]` sums to 0
  under naive binary64 order and to 1 with `math.fsum`; at represented
  `x=1e-16`, direct `sqrt(1+x)-1` suffers cancellation whereas the
  rationalized form yields `5e-17`; tolerance defaults can admit a
  wrong real result unless relative tolerance is zero; signed-zero
  complex phase and the exact residual/forward-error example agree with
  the documented conventions.
- **Observed in scope-limited test helper probes:**
  `dimension_vector` checks vector *length* and accepts exponents
  `True`, `inf`, and `1j`; `phase_or_none` checks zero-phase but
  does not reject a nonfinite complex argument. These demonstrate
  missing checks **if** the helpers are misused as complete validators;
  the test inventory explicitly limits their intended roles.
- **CI evidence:** baseline 67 passing tests, 31 math-specific;
  review-branch 67 passing tests. Neither substitutes for a general
  numerical proof or agent-level performance trial.
- **Negative evidence:** no production math API target exists in the
  inspected package. The seven planned behavioral scenarios and
  42-run evaluation are marked NOT RUN.
- **Audit integrity:** an initial independently written sample-variance
  probe compared a floating calculation with an exact fraction and
  produced a checker mistake; it was corrected and the corrected probe
  passed. That was not a defect in Kestrel source.

## Derivation

Passing finitely many tests establishes their observed outcomes under
specific assumptions and executions. It cannot establish every input
property of procedures whose permissible domains, backends or production
implementations have not been specified. Conversely, observing behavior
outside a helper's advertised narrow contract is not sufficient to
identify a violated accepted requirement.

## Negative checks

A reproducible mathematical counterexample within a **stated** contract,
a failed independently derived oracle, or a newly supplied full validation
API accepting prohibited inputs would require narrowing or refuting this
claim. In every case compare the exact baseline, interface contract and
input policies before reporting regression.

## Revisit when

The math procedure text, fixtures, solver implementation, input contracts
or test environment change; a controlled behavioral evaluation runs;
or independently checked counterevidence is obtained.
