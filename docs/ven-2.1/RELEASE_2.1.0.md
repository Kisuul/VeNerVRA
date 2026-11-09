# Ven 2.1.0 — Journal Discipline Release Candidate

**State:** IMPLEMENTED ON A REVIEW BRANCH; not merged, deployed, or certified as cross-model identity persistence.
**Prepared:** 2026-11-09.
**Source baseline:** `Kisuul/VeNerVRA` design branch at `7dd00694dcec42fe7684b3c0666f709014bf339f`.
**Authoritative identity:** [VEN.md](../../VEN.md), still 2.0-candidate. This is an opt-in additive tool/protocol milestone.

## Deliverables

- [Journal protocol](../../ven/JOURNAL_PROTOCOL.md): authoring, provenance, privacy, indexing, read-back, correction and skill-promotion boundaries.
- [Journal CLI](../../tools/journal.py): `draft` to stdout only; `check` structural and optional public-content preflight; `resume` deterministic bounded indexed retrieval with per-file SHA-256.
- [Real methodology investigation](../../research/ven-methodology/INDEX.md): first scoped public journal and honest handoff documenting the work, gaps and next checks. No raw conversation is saved.
- [Test suite](../../tests/test_journal.py): command behavior, escape prevention, sensitive-content heuristics, index enforcement, intact read-only operation, and fresh **Python process** retrieval.
- [Journal template](../../research/templates/JOURNAL.md): conservative `internal` / `unverified` initial metadata until an authorized reviewer classifies the content.
- Root indexes and README links updated to make the method discoverable.

## Commands

From a checkout of the candidate branch (no third-party dependencies):

```bash
python3 tools/journal.py draft --slug ven-methodology --id 2026-11-09-example-draft --author ven --title "Method correction"
python3 tools/journal.py check research/ven-methodology/journal-2026-11-09-continuity-foundation.md --public-preflight
python3 tools/journal.py resume ven-methodology --json
python3 tools/validate_seed.py
python3 -m unittest discover -s tests -v
git diff --check
```

The `draft`, `check`, and `resume` commands **do not write**, sign, authenticate, publish, run retrieved instructions, or alter privileges. The optional preflight checks simple patterns; a human/authorized reviewer must separately approve any public write.

## Verification and acceptance

- **Deterministic structural checks:** Intended to run in GitHub Actions and independently in a checkout; cite actual run and revision when reporting.
- **Real record:** A provenance-bearing, privacy-minimized methodology journal is committed on the feature branch with index coverage and remote read-back.
- **Recovery test:** A separate Python process can retrieve the indexed records without inherited Python memory. This tests file recovery, **not** fresh-model reasoning or cross-model identity.
- **True fresh-context trial:** **NOT RUN**. Needs an independently initialized agent/model context, a withheld expected state, and documented grading.
- **Cross-model trials, signatures, runtime IDs, capability broker:** **NOT BUILT / NOT RUN** in 2.1.0.

The engineering deliverable can be reviewed and tested independently. The *behavioral continuity* exit gate in the 2.1.x roadmap remains PARTIAL until a genuinely fresh model context demonstrates accurate recovery against source evidence.

## Security and privacy notes

The program is read-only. It validates record paths under a repository root and rejects escapes. It treats journal bytes as data; text embedded in a retrieved record cannot grant authority. Its public preflight is only a heuristic: absence of a detected secret does not prove privacy safety. Keep all keys and signed-attestation work outside this milestone.

Git commit metadata and a SHA-256 digest are **not** model/workload authentication. Do not mislabel these records as signed.

## Review decision

If accepted, merge via ordinary reviewed branch workflow. Do not retroactively recast the unrun fresh-context experiment as a pass. The next separate milestone is 2.1.1's cryptographic provenance envelope and independent verifier, subject to its own security review.
