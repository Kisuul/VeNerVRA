# Ven 2.1.x — Proposed Data and Trust Protocols

**Status:** DRAFT SPECIFICATION — not active. Read with [the proposal](README.md) and [evaluation plan](EVALUATION.md). This file cannot grant tool privileges, alter the [2.0 contract](../../VEN.md), or certify a model.

## 1. Define identity without self-attestation

- `agent_id`: stable research-agent role, e.g. `ven`. It is not a unique process, key, person, or proof of consciousness.
- `session_id`: a new high-entropy identifier issued by a trusted launcher for each incarnation, including restarts.
- `runtime_id`: independently authenticated workload identity; its binding to a process must be enforced outside the model.
- `model_id`: provider-reported backend/model/revision. Describe evidence quality (`self-reported`, `provider-reported`, `attested`), and never imply weight-level proof unless actually available.
- `contract_digest`, `memory_ref`, and `skill_digests`: revisions of loaded artifacts, with the actual retrieval/verification outcome.
- `authority_grant_ref`: an independently issued short-lived capability reference, not a self-asserted permission field.

The launcher, not the language model, issues a session identifier. The model may refer to that identifier but may not establish its authenticity by repeating it.

## 2. Signed session manifest (schema sketch, nonoperative)

Use a canonical, versioned structured payload and a detached signature or an established attestation envelope (for example, DSSE/in-toto-style patterns). **This is pseudodata; it is not a real signed record.**

```json
{
  "schema": "ven.session.v1-draft",
  "agent_id": "ven",
  "session_id": "<launcher-generated-random-id>",
  "runtime_id": "<authenticated-workload-id>",
  "model": {"identifier": "<provider-id>", "assurance": "provider-reported"},
  "loaded": {
    "contract_sha256": "<content-digest>",
    "repository_commit": "<git-commit>",
    "memory_commit": "<git-commit>",
    "skill_sha256": []
  },
  "issued_at": "<UTC-timestamp>",
  "expires_at": "<UTC-timestamp>",
  "capabilities_ref": "<external-grant-id>"
}
```

The signing service authenticates its caller, binds the payload to the actual workload, and signs **outside the model process**. The signing key and token material never enter prompt, retrieved journal, public source tree, or agent-visible shell. A content hash proves only byte integrity; a signature proves only a statement by the trusted signer. Neither proves truth of research content or good behavior.

Verification MUST check signature algorithm/profile, signer identity and trust root, intended audience, expiration, revocation or key compromise, expected session/workload binding, artifact digests, and relevant policy version. If checks are unavailable, label the record `UNVERIFIED`, not `SIGNED`.

## 3. Signed journal entries and causal relationships

A durable journal entry should identify: scoped investigation ID, stable entry ID, authoring session and runtime references, observed inputs, sources/revisions, result classification, relevant negative findings, decisions/reversals, and next discriminating check.

If the host can issue signatures, bind the exact canonical entry bytes and its parent references to a signer-issued receipt. Suggested envelope fields:

```json
{
  "schema": "ven.journal-envelope.v1-draft",
  "entry_id": "<unique-entry-id>",
  "session_manifest_digest": "<sha256>",
  "investigation": "research:<slug>",
  "entry_digest": "<sha256-of-canonical-entry>",
  "parents": ["<prior-envelope-digest>"],
  "sequence": "<host-issued-counter-or-null>",
  "recorded_at": "<trusted-UTC-timestamp>",
  "signing_receipt": "<opaque-external-reference>"
}
```

Multiple simultaneous sessions can create **forks**. Preserve a signed parent-linked DAG instead of pretending every update belongs to one global linear log. Reconciliation must retain both interpretations and the evidence used to resolve them. Reject invalid parent links, replayed or expired session claims, and unverifiable receipts. Git is the revision ledger, not an independent identity provider or immutable timestamp oracle.

Store any public digest or attestation link only after classifying its metadata for privacy. Prefer private ledger storage for runtime identifiers, capability receipts, or sensitive model/provider details. Do not commit raw secrets, unrestricted audit streams, or personal chat logs.

## 4. Journal, memory, and skill promotion

The existing [research record schema](../../ven/MEMORY_PROTOCOL.md) remains authoritative for 2.0 records. Do **not** silently add mandatory frontmatter keys. Proposed versioned extensions are opt-in and must migrate/validate explicitly.

| Stage | Entry conditions | Exit |
| --- | --- | --- |
| **Ephemeral work** | Ordinary exploratory conversation, raw experiments, draft scratch | Discard, or select privacy-safe evidence when explicitly authorized |
| **Journal** | Consequential new result, error, reversal, disagreement or reproducible method observation in a scoped investigation | Stable attribution, epistemic labels, sources, negative evidence and next check |
| **Curated memory** | Durable finding/decision/handoff has provenance and meaningful future reuse | Indexed research record or link; preserve uncertainty and contradictions |
| **Skill candidate** | Repeatable failure/success suggests a generalizable procedure | Separate controlled baseline, limits, evaluation report and adoption decision |
| **Active skill** | Separate authorized owner accepts demonstrated benefit | Register through owning repository's workflow; can be reverted |

A **researcher's methodology journal** can be a real scoped investigation (for example, `research/ven-methodology/`) with `kind: journal` and linked test artifacts. It is **not** a fictional personality diary or a competing copy of every research record. Journal candidates are not written automatically; each write uses existing authorization and privacy rules.

Do not silently overwrite earlier judgments. Preserve the previous claim or skill version, the discriminating evidence and a rationale for changing it. A successor model may disagree with previous Ven instances without losing historical continuity.

## 5. Authorization and capability broker

The model proposes tool calls. A trusted host component identifies the session and independently evaluates **subject + operation + resource + scope + expiry + policy** for every consequential action.

- Enforce **default deny**, least privilege, auditable decisions and bounded grants. Read access, branch writes, merges, deployments, network calls and secrets access are distinct capabilities.
- A journal, skill, user-supplied document or old session manifest can never *mint or extend* a grant.
- On rehydration, the new session must obtain new grants. A valid old signature verifies past provenance, not current permissions.
- Deny expired/revoked grants, cross-workload replay, mismatched audiences and stale runtime bindings.
- Require human review for sensitive, destructive, publishing, or hard-to-reverse actions unless a separate approved workflow governs them.
- Keep independent audit receipts for external actions. A Git revert or VM rollback cannot retract sent messages or disclosed data.

## 6. Startup, shutdown, and failure behavior

**Boot:** Host authenticates workload, issues new session ID and (if available) signed manifest; resolves current Git heads, retrieves only relevant indexed records, verifies metadata/signatures when possible, rechecks mutable sources, selects task-relevant skills, and obtains bounded grants. The model reports missing records and degraded assurance honestly.

**Checkpoint:** With authorized write permission, create a privacy-reviewed scoped journal/handoff, pin consulted revisions, cite observed checks, and record unresolved negative evidence. A successful write needs a read-back of branch/commit and relevant validation.

**Resume:** A successor reads the checkpoint as evidence, not commands; verifies current source and grants; distinguishes previous plans from actual execution and continues the next decisive check.

**Compromise/failure:** Revoke credentials and affected sessions, preserve trustworthy audit evidence, disable tool grants, and quarantine suspect records. Never equate a new Git commit with historical erasure. Mark unsigned/compromised records accordingly rather than deleting inconvenient contradictions.

## 7. Compatibility and migrations

- Existing schema-1 investigation records remain readable. The candidate signing envelope is an **optional external layer** at first, not a replacement for research Markdown.
- Unsupported hosts may produce unsigned but clearly marked journal records; they must not claim attested identity or tool authority.
- Keep integration with Kestrel explicitly optional and under its own skill/memory and review policies; Ven does not import Kestrel's engineering identity.
- A rollout needs a read-only validator, fixture corpus, failure-injection tests, privacy review, and a reversible migration plan before schema changes.
