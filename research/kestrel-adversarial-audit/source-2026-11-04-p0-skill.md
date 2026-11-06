---
schema: 1
id: 2026-11-04-kestrel-audit-source-skill-v01
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
sources: "KestrelGaming issue #7; program PR #8 head 688f3d3a4bb82125978530c5b5b87b00f8c719bc; specialist handoff read from program branch on 2026-11-04."
---

# Source: Kestrel P0 adversarial-review proposal and handoff

## Summary

Kestrel's primary issue and draft program define the scope, ownership,
verification and evaluation security boundaries for a proposed specialist
engineering skill. These documents are design inputs, **not** an implemented
or behaviorally validated skill.

## Evidence

- [Issue #7: Adversarial Code Review & Regression Engineering](https://github.com/Kisuul/KestrelGaming/issues/7),
  open at inspection, specifies review-only boundaries, a schema for findings,
  test-integrity checks, three defect/attribution cases and a clean decoy.
- [Draft program PR #8](https://github.com/Kisuul/KestrelGaming/pull/8),
  head `688f3d3a4bb82125978530c5b5b87b00f8c719bc`, names the
  integration branch `skills/p0-engineering-foundations-2026-11-04`.
- [Program design](https://github.com/Kisuul/KestrelGaming/blob/688f3d3a4bb82125978530c5b5b87b00f8c719bc/docs/P0_ENGINEERING_SKILLS.md)
  defines selective activation, short entrypoints and independent skill evaluation.
- [Specialist handoff](https://github.com/Kisuul/KestrelGaming/blob/688f3d3a4bb82125978530c5b5b87b00f8c719bc/memory/projects/kisuul/kestrelgaming/handoffs/2026-11-04-p0-adversarial-review-agent-r01.md)
  requires a separate task branch based on the latest program branch,
  a child PR targeting that program branch, honest execution reports, and
  no self-merge.
- At inspection the proposed `skills/engineering-adversarial-review/SKILL.md`
  did **not** appear in the program-branch Git tree. Recheck before implementation.
- Withheld behavioral-evaluation answer keys must be inaccessible to
  participant agents. A public repo file named 'hidden' is not hidden.

## Related claims

- [Research question](question-2026-11-04-scope.md).
- [Blind-first hypothesis](hypothesis-2026-11-04-blind-first.md).
- [Research-to-engineering handoff](handoff-2026-11-04-skill-next.md).

## Revisit when

The specialist starts work, a child PR appears, the program branch moves,
hidden-evaluation isolation becomes available, or Issue #7 acceptance terms change.
