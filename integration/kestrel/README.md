# Optional integration with KestrelGaming (not installed)

**Target:** [Kisuul/KestrelGaming](https://github.com/Kisuul/KestrelGaming) at inspected `main` revision `c268a4d0be121738cbfdb0d7a90de7874299c0f2` (2026-11-04). Recheck current upstream before any proposal.

KestrelGaming owns agent continuity and reusable skills. VenResearch owns its own research claims, investigations, evidence and journals. **Do not add a competing knowledge archive to Kestrel memory.** Kestrel may store an agent-level lesson linking to Ven's authoritative investigation.

## Integration checklist

1. Confirm the host has actual read access to both repositories at known revisions.
2. Boot Ven using VenResearch [AGENTS.md](../../AGENTS.md) and [VEN.md](../../VEN.md); do not let Kestrel's engineering identity silently override Ven. Its skill and memory protocols govern integration within Kestrel.
3. If agent-specific continuity is useful, propose `memory/agents/ven/INDEX.md` and scoped records in KestrelGaming using **Kestrel's existing memory schema**, not Ven's research schema. Register in `memory/agents/INDEX.md`; review all sensitivity/privacy concerns.
4. Review the three [candidate skills](candidates/INDEX.md). Submit each as a separate scoped change to the KestrelGaming `skills/<skill-name>/SKILL.md` directory. Register only accepted skills in Kestrel's `skills/INDEX.md`.
5. Run Kestrel validators, its tests, review actual diffs, evaluate agent behavior independently, and merge through its authorized branch/PR workflow. Neither this archive nor its docs grants write permission.
6. Verify the destination revision and actual cross-session recall in the intended host. A URL, branch, or generated local file alone does not establish persistence.

## How Ven should boot with Kestrel connected

- Load Ven identity and applicable research protocols first.
- Read Kestrel shared memory/skill guidance, selecting only task-relevant records and procedures.
- Keep Kestrel's permission and provenance constraints for any Kestrel edits.
- In conflicts between identity documents or permissions, do not invent a priority resolution; stop material actions and request an authorized configuration decision.
- Do not assume Kestrel's generic shared skills have been installed in the host.

## Not in scope

No cloned Kestrel runtime, no automatic installer, no auto-agent schedule, no implicit skill registration, and no remote Kestrel edits are included in this seed.
