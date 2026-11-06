---
schema: 1
id: 2026-11-04-kestrel-audit-hypothesis-blind-v01
kind: hypothesis
scope: research:kestrel-adversarial-audit
status: draft
epistemic_status: proposed
confidence: unresolved
evidence: hypothesis
sensitivity: public
author: Ven
created: 2026-11-04
updated: 2026-11-04
sources: "User-proposed blind-audit possibility during 2026-11-04 discussion; Kestrel issue #7 and VEN.md independently inspected. No controlled comparison executed."
---

# Hypothesis: blind-first auditing can reveal defects hidden by design anchoring

## Summary

**UNTESTED proposal.** On a suitable set of code-review tasks, an auditor
who first receives public observable requirements and code—but **not**
internal design rationale, author explanations or previous review findings—
may discover additional genuine defects missed by a reviewer who reads all
design rationale before starting. The blind-first auditor then receives
the relevant context and adjudicates the frozen initial findings.

Blindness concerns **internal explanations**, not the public contract
required to judge correct behavior, the permitted tool boundary, or safety
requirements. An issue inferred without an identified accepted contract
is initially a hypothesis, not a confirmed defect.

## Evidence

- Origin: user's observation in the research conversation, framed as a
  plausible mechanism rather than an established scientific outcome.
- [Kestrel's adversarial review proposal](source-2026-11-04-p0-skill.md)
  already calls for false-positive controls, independent oracle cases,
  evidence precision and baseline attribution.
- [The math review](claim-2026-11-04-bounded-math-audit.md) demonstrated
  a **useful caution**, not this causal effect: an apparent invalid-input
  bug was reclassified as an intentionally limited test-local helper once
  the actual fixture contract was considered. It supports preserving
  provisional findings and then checking the governing contract.
- No blinded comparative trial, validated human study, or measured gain
  was performed. Do not cite this record as evidence that blind-first
  audits actually outperform design-informed audits.

## Competing hypotheses

- **Context improves specificity:** Seeing accepted design documents
  before review reduces wasted effort and false positives, catching
  contract-specific defects a blind reviewer misses.
- **Independent falsification is sufficient:** An informed reviewer
  instructed to challenge assumptions performs comparably without
  procedural blinding.
- **Extra review effort explains any gain:** Apparent benefit comes from
  two passes or more tokens rather than information order.
- **Hindsight contamination:** Later exposure to design rationales
  silently changes the account of what the blind pass initially found.

## Predicted observations

At comparable total review cost, blind-first + contextual adjudication
should discover more **independently confirmed** defects that
design-informed review initially misses, while retaining acceptable
precision, correct baseline attribution, no fabricated execution claims,
and no unauthorized source modification. If the advantage is confined
to more provisional accusations later rejected, the hypothesis fails
its intended practical objective.

## Discriminating / falsification test

Use the [planned controlled trial](experiment-2026-11-04-blind-first-trial.md).
Randomize task and arm assignments with unseen vulnerable/clean examples,
fixed contracts and budgets; seal the blind first-pass findings before
revealing design; score against independent withheld expected outcomes.
Compare defect detection, false positives, baseline attribution,
reproduction fidelity and cost. A controlled null result or a substantial
precision/cost penalty would count against adoption as a default method.

## Revisit when

A secure harness and independent evaluator are available, first-pass
artifacts are preserved, task set or design exposure conditions change,
or a controlled comparison contradicts the proposed advantage.
