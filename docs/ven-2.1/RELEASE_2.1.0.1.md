# Ven 2.1.0.1 — Hostile Remediation Candidate

**State:** PATCH CANDIDATE ON A REVIEW BRANCH; **NOT RELEASED, NOT MERGED**.
**Date:** 2026-11-09
**Target baseline:** 2.1.0 draft PR #4, original head a0b1032e957c144eab8ab154d25292b5192be533.
**Previous hostile review:** https://github.com/Kisuul/VeNerVRA/pull/4#issuecomment-6736122920
**Reproduction:** https://github.com/Kisuul/VeNerVRA/actions/runs/42589570083
**Fixed-behavior checks:** https://github.com/Kisuul/VeNerVRA/actions/runs/42594501832 (44 tests, structural validator and whitespace gate passed against 8d8714fa318c67911c427f5fb5cfd5c6a0b91053; recheck final documentation commit).

## Remediation matrix

| Finding | Observed 2.1.0 defect | 2.1.0.1 correction | Test |
| --- | --- | --- | --- |
| F-01 | Fenced pseudoheadings passed journal validation and became summaries | Strict level-two headings only outside code fences/indentation/comments; duplicate required sections rejected | test_f01_fenced_pseudoheadings_cannot_populate_sections; test_duplicate_summary_heading_is_rejected |
| F-02 | Filename substrings counted as index registration | Index lookup requires an actual, resolving local Markdown link; shared in the repository validator | test_f02_prose_mentions_are_not_index_registration, plus three global validator tests |
| F-03 | Recall emitted duplicate stable record IDs | Scan scoped research IDs across investigations and fail closed on collisions | test_f03_duplicate_ids_fail_closed; test_record_ids_must_be_globally_unique_across_investigations |
| F-04 | New draft displaced an older active correction under a bounded retrieval limit | Exclude drafts by default, allow explicit --include-drafts, prioritize active over disputed over draft, disclose omitted/excluded counts | test_f04_draft_does_not_displace_active_correction |
| F-05 | No independent fresh-model continuity experiment | **NOT FIXED BY UNIT TESTS**; require genuine isolated successor model, preregistered expected corrections, and independent evaluation | [Evaluation plan](EVALUATION.md) remains NOT RUN |

## Commands for reviewers

    python3 tools/validate_seed.py
    python3 -m unittest discover -s tests -v
    python3 tools/journal.py check research/ven-methodology/journal-2026-11-09-hostile-corrections.md --public-preflight
    python3 tools/journal.py resume ven-methodology --json
    python3 tools/journal.py resume ven-methodology --include-drafts --json
    git diff --check

Run the commands on a pinned checkout. Read the exact tool output and the full diff before accepting. The deterministic reader is neither a model-person identity verifier nor a secret scanner, and its limited Markdown grammar is intentional.

## Release gate

**Engineering patch evidence:** The four reproduced defects have targeted negative regression checks and pass on the patch branch; independent hostile review of the final SHA is still appropriate.

**Behavioral acceptance:** PARTIAL / NOT VERIFIED — there has not been a real fresh-model recovery test. The 2.1.0 acceptance standard is unchanged, and the engineering patch must not be described as proven model continuity.

**Deployment/authorization:** None. No signing, scheduling, tool permission brokering, credential inheritance or public journal auto-publishing was added. Original contract and Kestrel repository remain unchanged.

**Next decision:** Review the patch independently, then run a true fresh-context recovery trial with withheld grading. Keep 2.1.0.1 as a candidate until that gate is satisfied or explicitly and transparently re-scoped.
