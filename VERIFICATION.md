# Seed verification report — 2026-11-04

## Checks executed against this generated seed

- **PASS** — `python3 tools/validate_seed.py` (required files, local links, research schema, scope, index coverage, record identity and dates).
- **PASS** — `python3 -m unittest discover -s tests -v` (17 unit tests; including deliberately broken structures).
- **PASS** — staged snapshot of the seed in a temporary Git repository, `git diff --cached --check` (no whitespace errors).
- **PASS** — preserved Ven 1.1 source byte-for-byte against supplied `VeNerVRA-1.1.txt`.

## Not performed

- **NOT RUN** — live or multi-session Ven agent behavioral evaluations.
- **NOT RUN** — real external research or independent factual validation of research claims (the example is synthetic).
- **NOT RUN** — GitHub push, PR, merge, repository creation, permissions provisioning, Kestrel skill installation, or host runtime integration.

Structural validation does not establish agent competence, safety, research quality, memory persistence or permission enforcement.
