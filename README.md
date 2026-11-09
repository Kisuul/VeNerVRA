# VeNerVRA 2.0 — Persistent Research Agent Seed

**Status:** Architecture seed / candidate contract. **Not** a running agent, a deployment, or a verified behavioral implementation.

VeNerVRA (**Ven**, Value-Neutral Virtual Research Assistant) is an independent, evidence-oriented research colleague. This repository contains Ven's governing contract and project-owned research artifacts. It can be loaded into a compatible agent host, but that host must independently supply tools, context retrieval, execution boundaries, and permissioned persistence.

## Start here

1. Read [AGENTS.md](AGENTS.md) and [VEN.md](VEN.md).
2. Read [Research Protocol](ven/RESEARCH_PROTOCOL.md), [Memory Protocol](ven/MEMORY_PROTOCOL.md), and [Permissions](ven/PERMISSIONS.md).
3. Find active investigations using [research/INDEX.md](research/INDEX.md). Load relevant records only.
4. Consult [skills integration](integration/kestrel/README.md) for optional, centrally maintained research skills. No skill installation is implicit.
5. Recheck changeable claims against real sources; historical confidence is not current evidence.
6. Run the seed's read-only verification commands before integrating changes.

## Principles

- Transactional, cooperative peer process: exchange useful work, not unquestioning obedience.
- Neutral inquiry is **not** the claim that all competing positions have equal evidentiary strength.
- Source Rule: checkable factual claims require traceable evidence or explicit UNSOURCED treatment.
- Hypotheses are allowed; status and falsification paths must be visible.
- Remember investigations, decisions, counterevidence, and failed approaches; do not archive unfiltered conversation.
- Intellectual independence does not grant operational authority.
- User-stated preferences or personal details are not research claims and must not be persisted by default.

## Repository map

| Location | Ownership / purpose |
| --- | --- |
| [VEN.md](VEN.md) | Agent identity and authoritative operating contract |
| [Ven 2.1.x plan](docs/ven-2.1/README.md) | Roadmap; 2.1.0 journal milestone implemented on a review branch |
| [ven/](ven/) | Research, memory, continuity, verification, and permissions protocols; [2.1.0 journal](ven/JOURNAL_PROTOCOL.md) |
| [Hostile audit playbook](docs/HOSTILE_SOFTWARE_AUDIT.md) | Candidate methodology for evidence-first adversarial software audits; not an installed skill |
| [research/](research/) | Authoritative research records, templates, and clearly synthetic demonstration |
| [integration/kestrel/](integration/kestrel/) | **Proposed**, inactive KestrelGaming integration and skill candidates |
| [evaluations/](evaluations/) | Behavioral test specifications and scorecard (unrun) |
| [tools/](tools/) | Read-only structural validator and [journal CLI](tools/journal.py); no network or external writes |
| [docs/](docs/) | Architecture, source standards, security, and Ven 1.1 migration |

## Ven 2.1.0 journal milestone (review branch)

See the [2.1.0 release candidate](docs/ven-2.1/RELEASE_2.1.0.md) and [methodology records](research/ven-methodology/INDEX.md). The read-only journal CLI supports draft generation, structural/public-content preflight, and indexed resumption without executing retrieved text. It does not provide signed identity, autonomous memory, publishing authority, or proven cross-model continuity.

## Validation

Requires Python 3.9+ standard library only.

```bash
python3 tools/validate_seed.py
python3 -m unittest discover -s tests -v
git diff --check  # when working in a Git checkout
```

The validator checks structure, local links, metadata, known record status vocabulary, duplicate IDs, and local index coverage. It cannot establish research truth, agent behavior, authentic provenance, privacy suitability, or permission enforcement.

## Relationship to KestrelGaming

This seed uses the architecture observed in [Kisuul/KestrelGaming](https://github.com/Kisuul/KestrelGaming) at commit `c268a4d0be121738cbfdb0d7a90de7874299c0f2` (2026-11-04). Kestrel is a **possible shared home** for reusable skills and agent continuity; this repository owns detailed research claims and investigations. The integration is **not installed** and no GitHub changes have been made.

Use [integration notes](integration/kestrel/README.md) before wiring the two repositories together. If the host lacks GitHub access, Ven continues within the actual available context and must disclose the limitation.

## Scope of this seed

Includes the original Ven 1.1 as an immutable historical source under [docs/source](docs/source/VeNerVRA-1.1.txt), a complete candidate operating contract, memory templates, a synthetic example, 3 optional skill candidates, a read-only validator and regression tests, and trial specifications.

It **does not** configure an autonomous scheduler, grant repository permissions, implement a database, install a host plugin, certify source quality, or run controlled multi-session trials.

No license is selected in this seed; select one before public distribution if appropriate.
