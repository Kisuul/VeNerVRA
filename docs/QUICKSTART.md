# Quickstart — local, honest research continuity

1. Extract this archive to a working directory and open [AGENTS.md](../AGENTS.md).
2. Run `python3 tools/validate_seed.py` and `python3 -m unittest discover -s tests -v`.
3. Create a new folder `research/<short-slug>/` and copy [templates](../research/templates/INDEX.md). Use `INDEX.md` to link each new record and register the investigation in [research/INDEX.md](../research/INDEX.md).
4. In your actual agent host, supply a pointer to this repository and its `AGENTS.md`; **verify the host can read it**. A URL alone does not load it.
5. Request a bounded investigation. If you also authorize persistent writing, verify exact output paths and diff, then save using the environment's permitted workflow.
6. Start a fresh context, load the checkpoint, verify external citations and the real repository revision, and continue from the recorded next test.
7. For shared research skills, use [Kestrel integration](../integration/kestrel/README.md) as a separate proposed change. Do not assume proposed candidate skills are installed.

The included synthetic example tests metadata and indexing, not agent continuity or research truth.
