# Ven 2.1.0.2 — Research continuity hardening candidate

**Status:** IMPLEMENTED ON A REVIEW BRANCH. NOT MERGED. NOT RELEASED.
**Date:** 2026-11-09
**Baseline:** 2.1.0.1 PR #5 SHA f3634a51488ba69e856c2d6340609aedd11ccb8c.
**Original hostile source:** [Ven 2's frozen audit](https://github.com/Kisuul/VeNerVRA/blob/6f982e057d05aee440b65561551272b59cbf8f89/docs/audits/VEN_2_1_0_1_HOSTILE_2026_11_09.md).
**Implementation:** [journal reader](../../tools/journal.py), [shared validator](../../tools/validate_seed.py), [inverted regression tests](../../tests/test_journal_regression_2102.py).
**Governing contract:** [VEN.md](../../VEN.md) remains unchanged.

## Remediation of Ven 2's findings

| Audit finding | Correction | Evidence category |
| --- | --- | --- |
| V2-F01: Raw HTML masquerades as Markdown headings and links | Reject raw HTML outside code/comment contexts in journals, handoffs and research indexes, including split opening tags; reject ambiguous multiline index code | Negative regression tests |
| V2-F02: Global CI misses journal-specific requirements | Shared validator enforces all five required journal sections and rejects empty or duplicate sections; global CI runs this validator on all registered records | Negative regression test using full repository copy |
| V2-F03: ISO week date crashes sort | Require real canonical YYYY-MM-DD dates in metadata and scaffolding; preserve date sort for validated records | Invalid-format and impossible-date tests |
| V2-F04: Empty active handoff accepted | Active/disputed handoff requires substantive Summary, Evidence, Next decisive check, and Revisit when | Negative regression test |
| V2-F05: Evidence and revisions lost in resume API | JSON recall includes bounded section text for evidence, alternatives, reversals and next actions; declares truncation and source follow-up | Fidelity and truncation tests |
| V2-F06: Authorship and sensitivity stripped | Include author, confidence, epistemic status and sensitivity in each entry; public-only by default and explicit maximum sensitivity | Private/label tests |
| V2-F07: Orphan research directories invisible | Global validator and resume reject unindexed real research directories containing Markdown | Orphan regression test |
| V2-F08: No fresh-model behavioral trial | **NOT RESOLVED** by deterministic Python; [trial protocol](FRESH_CONTEXT_GATE.md) defined, run NOT EXECUTED | Unmet release gate |

## Risk and honest limitations

This is a **strict, deliberately limited Markdown dialect** rather than a general Markdown renderer. It fails closed on raw HTML in structured journal/handoff/index material and requires index links resolvable within the repository. It is not a formal CommonMark validator or HTML sanitizer.

Metadata classification is **self-declared**: inclusion flags are not security authorization or verified authorship. The host must independently enforce actual access restrictions. Existing public Git history remains public; filter defaults cannot undo disclosures. SHA-256 pins bytes, not a signing key, a provider's model weights, or the truth of a claim.

The reader still selects records by status, type and date, not measured relevance. The output announces omitted records and truncated sections; a consumer must fetch and inspect the full referenced files when necessary. Journal sources and successful CI do not prove an agent's judgment transferred across models.

## Executable verification

From a frozen checkout of the final candidate commit, review complete diff then run:

    python3 tools/validate_seed.py
    python3 -m unittest discover -s tests -v
    python3 tools/journal.py check research/ven-methodology/journal-2026-11-09-2102-audit-corrections.md --public-preflight
    python3 tools/journal.py resume ven-methodology --json
    python3 tools/journal.py resume ven-methodology --max-sensitivity public --max-section-chars 4096 --json
    git diff --check

CI tests automatically execute positive controls, inverted hostile regressions, and real-repository record retrieval. The installed source contract remains 2.0-candidate; no signing keys, capability grants, production integrations, model weight changes, external deployment, or autonomous journaling have been implemented.

## Gate

**Engineering scope:** Submit for an adversarial independent re-review after final CI and remote read-back. A suite passing at one SHA does not certify a different SHA.

**Behavioral continuity:** **NOT RUN / NOT VERIFIED.** The release is a candidate until a newly initialized model context, with no inherited chat, recovers earlier evidence/corrections under independently graded criteria. This requirement is inherited, not silently removed.

**Do not advance to 2.1.1** as a verified continuation system solely on structural CI. Release approval remains a separate explicit decision.
