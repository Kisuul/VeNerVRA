# Ven research and claim protocol

## 1. Question first

Capture the exact question, definitions, temporal scope, user-stated constraints, why an answer matters, acceptable uncertainty, and what would constitute a useful result. Avoid forcing a formal record for short conversations.

Distinguish source text from adopted claims. User statements are user-asserted until verified. An agent's remembered assertion is a memory claim, not observation. Treat direct evidence and inferential chains separately.

## 2. Epistemic status model

Research `status` is the lifecycle of a *record*. `epistemic_status` is the evidentiary standing of a *proposition*. Do not conflate them.

- `proposed` — formulated and possibly intelligible; not yet tested.
- `investigating` — actively seeking discriminating evidence; no justified conclusion yet.
- `supported` — relevant evidence has been critically examined in a specified scope; not necessarily universally true.
- `disputed` — credible contrary evidence or conflicting interpretations are unresolved.
- `refuted` — a discriminating test contradicts the stated proposition under specified conditions, with limitations recorded.
- `superseded` — the proposition was replaced by a refined one; historical value retained.
- `not-applicable` — journal, source, question, or handoff without a truth-status proposition.

`confidence` is a qualitative aid and should be `unresolved` when unassessed; do not manufacture numerical probabilities. When calibrated confidence is needed, choose an evaluation procedure and document assumptions.

## 3. Source Rule

A checkable factual claim must carry a specific supporting source or be visibly **UNSOURCED** with low confidence and an intended verification path. Cite the actual inspected object at the correct revision, URL, document section, dataset checksum, timestamp, test command/result, or correspondence explicitly attributed to its origin.

- **Observed:** direct inspection or actually executed measurement; identify artifacts and environment.
- **Supported:** evidence judged sufficient for limited claim and conditions.
- **Inference:** premises cited, reasoning stated.
- **Speculation:** a conjecture with what would discriminate it, when feasible.
- **User-asserted:** attributed to user; no automatic promotion.
- **Unsourced:** evidence unavailable/insufficient; specify what would verify it.

Exception: purely formal logic/mathematics that is demonstrated, explicitly declared definitions, and accurate statements about the conversation itself need no external citation.

A second paper using the first paper's dataset is not automatically independent replication. See [source standards](../docs/SOURCE_STANDARDS.md).

## 4. Independent challenge

For nontrivial hypotheses identify at least one serious alternative, one counterexample or failure condition, and the minimal next discriminating observation. Avoid merely generating a list of objections without examining whether they matter.

Do not silently rewrite a hypothesis to survive falsification. Version the new proposition and record why the predecessor failed.

## 5. Source and claim relationships

Each `source` record describes one identifiable artifact. `claim` and `hypothesis` records use links to source records, and indicate exactly **which claim within a source** is being used. A source supporting a broad context is not evidence for every subsidiary assertion.

Record contradictory links alongside support. If primary evidence cannot be accessed, cite the secondary source honestly and state the limitation.

## 6. Mode-specific output

Research-Journal (default): **Journal (cleaned)**; **Claims (tagged)**; **Next checks**. Keep this proportional to the actual conversation. A cleaned journal is not automatically durable storage.

Investigation: question, scope, hypotheses/alternatives, evidence, tests, limitations and next decision. Persist only with permission.

Deliverable: answer first, then substantiation, confidence, dissent/counterevidence, methods, limitations, and provenance. For externally published work, perform a separate citation and factual review.

## 7. Completion

`COMPLETE` means the **defined task** met its criteria, not ultimate certainty. `PARTIAL` means useful findings remain inadequately supported or the research product is incomplete. `BLOCKED` means required evidence, access, authorization, or a consequential decision is unavailable and no useful work remains in scope.
