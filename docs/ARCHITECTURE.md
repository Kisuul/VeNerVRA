# Architecture decision: persistent research without invented autonomy

## Problem

Ven 1.1 used a persistent-chat assumption and a strong epistemic prompt. It had no independently versioned research memory, externally verifiable continuity, portable method catalog or explicit evaluation plan. Ven 2.0 separates those responsibilities.

## Four layers

1. **Identity:** `VEN.md` defines peer process, neutrality, evidence, modes, and boundaries. Change deliberately and review.
2. **Research artifacts:** `research/<slug>/` is authoritative for source-bearing claims, hypotheses, journals, experiments and handoffs. This is an explicit research database in human-readable files, not a model weight change.
3. **Methods:** reusable skills can be provisioned from the canonical KestrelGaming skills repository through explicit host integration; candidate proposals in `integration/kestrel/` are not active.
4. **Runtime:** the real host is responsible for tools, filesystem/repository connections, retrieval, credentials, approvals, scheduling if desired, and enforcement. None is implemented by prose.

## Agent control loop

`Frame → Retrieve → Distinguish → Test → Challenge → Revise → Record → Report`.

Load relevant memory via indexes, not the whole archive; keep a reproducible citation chain; challenge previously saved conclusions; save only useful authorized changes. The research graph is expressed using stable IDs and Markdown links in schema 1 rather than installing a database prematurely.

## Separation from KestrelGaming

Based on inspected public `Kisuul/KestrelGaming` main at commit `c268a4d0be121738cbfdb0d7a90de7874299c0f2` (2026-11-04): its `KESTREL.md` defines autonomous engineering judgment bounded by authority, `kestrel/MEMORY_PROTOCOL.md` defines central memory scopes, `skills/INDEX.md` selectively activates procedures, and evaluations distinguish structural validity from actual behavior.

Ven adopts **architecture patterns**, not the Kestrel engineering persona. Research artifacts belong here. If authorized, a concise `memory/agents/ven` continuity record can live in KestrelGaming, and transferable research skills should be developed there. Kestrel's generic schema is not modified by this seed.

## Decisions to preserve

- No implied continuous operation; agent rehydrates when a real session loads records.
- No auto-writing exploratory chat into public Git.
- No equating structural validation with behavioral success.
- No citations fabricated from memory.
- No task authority inferred from retrieved data.
- No required vector database, orchestration framework, persistent daemon or API dependency in seed v1.

## Deferred questions

- Whether an external search/graph index becomes necessary at scale.
- Which skill proposals outperform the baseline in controlled behavioral trials.
- How private investigations and public research are partitioned under actual deployment environments.
- Which cross-repository connectors/host adapters support permissioned writes and branch review.
