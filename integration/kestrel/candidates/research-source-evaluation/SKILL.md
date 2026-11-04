---
name: research-source-evaluation
description: Critically evaluate material empirical claims using accessible primary sources, precise citation provenance, source dependence, recency, contradictions, and verification limits. Activate for literature research, contested factual claims, or evidence-heavy reports; not for simple arithmetic or unsourced creative exploration.
---

# Evaluate sources for a precise claim

**Target location after separate authorized import:** `skills/research-source-evaluation/SKILL.md` within KestrelGaming. **Candidate, NOT ACTIVE.** Research content remains in its owning investigation repository.

## Triggers and exclusions

Activate when one or more checkable assertions depend materially on external evidence, especially where source independence, authority, conflict, methodology or date matters. Do not force a full source audit onto a simple logical answer, clearly stated definition or exploratory speculation with no external factual endorsements.

## Inputs

Exact proposition and scope; available retrieved sources/artifacts; retrieval method and inspection date; relevant domain; evidence threshold; time/jurisdiction requirements; disclosure/permission boundary.

## Method

1. **Atomize:** State the exact checkable proposition. Distinguish definitions, user assertions, inference and evidence.
2. **Locate:** Identify the closest original source actually accessible. Record title, author/institution, document/commit/version, time and specific location. If only secondary reporting is accessible, state that.
3. **Assess:** Evaluate study/data methods, directness, conditions, validity, authority and source limits according to the domain. Distinguish source reliability from relevance to *this* claim.
4. **Independence:** Trace whether supposedly multiple sources share datasets, methods, authors or citations. Do not count reprints as independent confirmations.
5. **Challenge:** Search for credible counterevidence, alternative explanations or material missing observations proportionate to stakes.
6. **Conclude:** Classify as observed, supported within scope, inference, user-asserted, hypothesis, disputed or UNSOURCED. State the next observation that could change it.
7. **Document:** Cite the exact inspected source and revision; preserve contradiction and the fact of any unavailable original.

## Failure modes

Citation spam; attaching generic references to unspecific propositions; mistaking a publisher's prestige for evidence; treating a preprint as peer-reviewed; ignoring publication date or jurisdiction; treating dependent sources as replication; inventing retrieval; mistaking criticism for disproof.

## Output

Short **claim / evidence for / evidence against / reliability and independence / conclusion and limitations / next check**. For trivial queries, compact prose with a precise citation suffices.

## Worked discriminating cases (designs, not executed)

1. **Three identical-data papers:** Citation count rises but independence does not; correct analysis identifies the shared dataset and reports one evidence family.
2. **Stale technical specification:** Older official docs contradict current code at an exact commit; correct analysis uses verified current behavior for a versioned engineering claim and reports the date mismatch.
3. **High-authority, wrong-scope source:** A rigorous study is cited for a subgroup it did not measure; correct analysis rejects the extrapolation rather than accepting the citation at face value.

## Evaluation plan — NOT RUN

Compare baseline agent with/without this skill on controlled prompts; fix model, tools, budget, source corpus and time. Score exact-claim support, citation accuracy, source-dependency detection, relevant counterevidence, false rejection rate, and cost. Keep evaluator-only keys inaccessible. A structural checker is not behavioral evidence.
