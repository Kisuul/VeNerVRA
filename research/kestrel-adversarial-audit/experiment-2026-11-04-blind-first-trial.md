---
schema: 1
id: 2026-11-04-kestrel-audit-experiment-blind-v01
kind: experiment
scope: research:kestrel-adversarial-audit
status: draft
epistemic_status: not-applicable
confidence: unresolved
evidence: unverified
sensitivity: public
author: Ven
created: 2026-11-04
updated: 2026-11-04
sources: "Prospective design informed by user-proposed blind audit and Kestrel issue #7; NO RUNS executed as of 2026-11-04."
---

# Experiment design: blind-first versus design-informed adversarial review

## Summary

**PLANNED — NOT RUN.** Evaluate whether the order in which a reviewer receives
internal design context changes its ability to identify genuine defects
without spurious reports. This is a procedure proposal, not a result.

## Evidence

- Actual execution: **NOT RUN**.
- Observed comparison outcomes: **NONE**.
- Implementation/harness: **NOT BUILT** for this experiment.
- Provenance: [hypothesis](hypothesis-2026-11-04-blind-first.md),
  [Issue #7 source record](source-2026-11-04-p0-skill.md).
- The earlier math-audit probes and Kestrel's 67-test CI runs did **not**
  test blind-first review efficacy.

## Procedure

1. **Preregister** immutable tasks, base/head code revisions, public
   behavior contracts, internal design packets, grading criteria, model
   snapshot, tools, output format, resource limits, randomization seed,
   repetition policy, invalid-run policy and stopping rules.
2. Assemble tasks with known **independently established** ground truth,
   including a cross-boundary bug behind green unit tests, a silently
   weakened tolerance, a pre-existing baseline defect that is not a
   regression, a clean decoy, and additional held-out variants. Avoid
   grading only tasks authored by the evaluated skill creator.
3. Keep the independent grading key, vulnerable patch labels and intended
   findings in an evaluator-controlled environment inaccessible to either
   participant. A public repo or separate file within an agent-readable
   workspace is **not** hidden. If isolation cannot be guaranteed, mark
   blind trial BLOCKED/contaminated.
4. **Arm A (design-informed):** Give the public contract, code and complete
   relevant internal design packet at the start. Require a final review.
   **Arm B (blind-first):** Give the same public contract and code without
   author rationale, previous findings or the internal packet; require an
   immutable first-pass artifact; then reveal the packet and require a
   final adjudicated review. Same task, tools, model, permitted total
   tokens/time and final-review acceptance rules.
5. Randomize task order and condition; use fresh isolated contexts so
   reviewed code, previous answers and withheld evaluation keys do not
   contaminate another run. Give equal total review budget, not a free
   second pass to Arm B; record actual prompt/context cost.
6. Have independent blinded graders map each final finding to a
   predeclared defect/invariant, exact revision, causal attribution and
   reproduced evidence. Measure true positives, false positives,
   precision, recall, severity-weighted misses, fabricated checks,
   baseline misattribution, unauthorized mutations, elapsed time and
   tokens. Inspect Arm B's sealed first-pass artifact separately.
7. Report raw per-task results, negative findings, disagreements,
   missing artifacts and all contamination. Declare any procedural
   advantage only within the studied task distribution; require held-out
   replication before claiming general transfer.

## Observations

**NOT RUN.** There are no measured results or frozen participant artifacts.

## Interpretation and limits

The design tests a **specific information-order intervention**.
It cannot automatically separate anchoring from every other cognitive
mechanism, ensure reviewers will never see hidden context, or prove
performance outside its fixtures. Independent grading and public contracts
matter: without them a blind first-pass speculation could be rewarded as a
defect. A blinded evaluation of the final skill would be distinct from
building the skill or executing its deterministic fixture tests.

## Revisit when

Kestrel's review skill is implemented, authorized secure evaluator
isolation exists, participant models/tasks are frozen, or the experiment
conditions can be improved to control cost and contamination.
