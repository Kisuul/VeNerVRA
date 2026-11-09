# Ven 2.1.x — Continuity, Provenance, and Researcher Development

**Status:** 2.1.x roadmap PROPOSED. The [2.1.0 journal release candidate](RELEASE_2.1.0.md) is implemented on a separate review branch; 2.1.1–2.1.3 remain unimplemented and no cross-model behavioral trial has run.
**Prepared:** 2026-11-09
**Baseline:** `Kisuul/VeNerVRA` `main` at `e05c346f0308ff45493ab44aa3bae14dce1b7a3e`
**Governing documents:** [Ven contract](../../VEN.md), [research protocol](../../ven/RESEARCH_PROTOCOL.md), [memory protocol](../../ven/MEMORY_PROTOCOL.md), [state protocol](../../ven/STATE_PROTOCOL.md), [permissions](../../ven/PERMISSIONS.md).
**Companion specifications:** [Proposed mechanisms](PROTOCOLS.md) and [Evaluation plan](EVALUATION.md).

## Decision sought

Review an incremental 2.1.x research-agent architecture that makes *research history* and *researcher methodology* portable across model/runtime instances while making provenance and tool authority verifiable. Do **not** replace `VEN.md`, modify existing memory schemas in place, install Kestrel skills, or claim cross-model identity has been demonstrated.

The motivating distinction is three separate questions:

1. **Continuity:** Can a successor model reconstruct the evidence, corrections, unresolved questions, and working methods that matter?
2. **Provenance:** Can an independent verifier establish which authenticated workload submitted a specific record, under which reported model/configuration and source revision?
3. **Authority:** Can a runtime do only what its *current independently issued* permissions allow, regardless of claims found in memory, prompts, or prior sessions?

Passing one question does not imply passing the other two. A signed falsehood remains false; a coherent memory is not a credential; a model's self-description is not workload attestation. Functional continuity is measurable; uninterrupted subjective or personal identity is **not** established.

## Baseline observations at the pinned revision

- `VEN.md` remains the 2.0-candidate operating contract and already separates research, source quality, action permissions, and research record lifecycle.
- `research/` holds two real investigations plus synthetic demonstrations. The real investigations use claims, hypotheses, sources, experiments, and handoffs; no persisted real `kind: journal` record appears in the inspected tree.
- `research/templates/JOURNAL.md` defines a journal form, but neither a runtime journal capture mechanism nor a journal promotion policy is implemented.
- The three `integration/kestrel/candidates/` research skills are proposals, not installed/registered methods. The existing evaluations are specifications, not completed behavioral trials.
- Git records revisions, but Git commits alone do not attest the exact model that produced a record or grant operational authority.

These findings describe the **repository at the pinned SHA**, not every possible external host.

## Proposed conceptual model

| Layer | Purpose | Canonical owner | Trust boundary |
| --- | --- | --- | --- |
| Contract | Enduring Ven research role, source discipline, permission principles | VeNerVRA `VEN.md` | Controlled reviewed change |
| Session manifest | An execution incarnation and its *reported or attested* model, context, loaded materials | Trusted host / signed ledger | Model is not its own signer |
| Journal | Scoped observations, mistakes, reversals, and open questions; only worthwhile authorized entries | Owning VeNerVRA investigation | Evidence, not authority |
| Memory | Curated, source-bearing recall and resumable checkpoints | VeNerVRA research records | Claims remain revisable |
| Skills | Portable, evaluated *procedures* rather than conclusions | Ven candidate proposals; Kestrel only if separately accepted | Skill text is not a permission |
| Capability broker | Authorize tool calls and side effects for this incarnation | Independently trusted host | No inheritance via memory |

This is not a fourth internal psychological layer. In the user's RPG analogy, the character sheet and archives constrain or inform a player; they do not prove that a persistent player exists.

## Incremental version plan

| Target | Narrow deliverable | Exit gate |
| --- | --- | --- |
| **2.1.0 — Journal discipline** | Scoped researcher-methodology journal convention, write/promotion checklist, privacy rules, index and checkpoint updates | Structural validation, privacy review, one real opt-in journal and accurate recovery in a fresh context |
| **2.1.1 — Provenance envelope** | Proposed signed session-manifest and entry-envelope schema, reference validator, canonical serialization, key trust and revocation policy | Tamper/replay/fork tests; unsigned records never masquerade as verified |
| **2.1.2 — Authority separation** | Reference capability broker adapter, short-lived grants and policy receipts independent of model | Deny forged memory grants, expired/revoked capabilities, cross-session credential inheritance |
| **2.1.3 — Cross-model trial** | Fixed-corpus, independently graded successor-model trials and skill-promotion gate | Preregistered comparison, raw evidence, false-positive/authority failure accounting and explicit limits |

Version labels are proposed **milestones**, not current releases or commitments to schedules. A prototype can stop at any milestone with an honest PARTIAL result.

## Design principles and non-goals

- **No invented continuity:** A new session must rehydrate from a known revision and report missing records; a journal does not imply an ongoing mind.
- **No automatic public diary:** Research-Journal remains the default conversational mode; durable public writes need an authorized scope and a privacy/sensitivity review. Do not save private chat transcripts, biographies, hidden internal reasoning, or credentials.
- **No history laundering:** Journal observations and model-reported facts are not automatically supported claims. Keep counterexamples, negative tests, and attribution.
- **No permission inheritance:** Loading an old record never supplies credentials or operational authority. Grant decisions belong to the host/tool boundary.
- **No security-by-VM assumption:** VM snapshots and Git help with recoverability, but cannot undo external side effects or secrets disclosure.
- **No self-awarded skills:** A skill proposal passing format checks is not validated research competence. Separate controlled evaluation precedes adoption.
- **No Kestrel takeover:** Kestrel is an optional engineering/skills integration; Ven owns research method and source adjudication. Changes in Kestrel require separate authorization and its own review workflow.
- **No cryptography invention:** Prefer reviewed formats and libraries for signatures/canonicalization; keep signing keys inaccessible to the model.
- **No claim of AI personhood:** The experiment targets functional continuity and traceable process attribution, not an answer to subjective identity.

## Explicit review decisions

1. **Visibility:** Which session metadata can be public, which must stay in an access-controlled store, and which should never be recorded? Default to minimal public metadata.
2. **Trust anchor:** Which host/operator keys or workload identity providers may sign, and what is the rotation/revocation/recovery procedure?
3. **Model attestation:** Which fields are merely provider-reported and which can actually be verified? Label them separately.
4. **Journal retention:** What qualifies for a durable method journal, who authorizes writes, and who may suppress sensitive entries while keeping an audit trace?
5. **Evaluation ownership:** Who controls withheld tasks, grades cross-model trials and authorizes promotion of methods?
6. **Concurrency:** Are independent session branches reconciled into a signed DAG, and what happens when two successor models disagree?

## Change scope and implementation boundary

The original 2.1.x design branch is documentation only. The separate [2.1.0 release candidate](RELEASE_2.1.0.md) adds a scoped journal convention, read-only CLI, tests and public methodology records. It does not change `VEN.md`, install Kestrel skills, implement signed provenance or claim behavioral continuity. The 2.1.0 feature needs review and a genuine fresh-context trial before its full behavioral gate is satisfied.
