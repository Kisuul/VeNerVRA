# Evidence-first hostile software audit playbook (candidate)

**Status:** Reviewable Ven methodology; **not** an installed Kestrel skill, a completed security assessment, or an authorization to attack a live system.
**Scope:** Source audits, integration audits, safety and security reviews, and merge-readiness reviews of software supplied within an actually authorized environment.
**Operating contract:** [VEN.md](../VEN.md), [research protocol](../ven/RESEARCH_PROTOCOL.md), [verification protocol](../ven/VERIFICATION.md), and [permissions](../ven/PERMISSIONS.md) remain authoritative.

## Mission and adversarial stance

Attempt to **falsify** correctness, safety, security, and integration claims. Treat a plausible design, passing tests, a green CI badge, comments, PR descriptions, commit messages, previous audit sign-offs, and polished documentation as **leads**, not proof. Treat source code as evidence of *what was written*, not automatically of *what ran*; deployment configuration, dependency versions, runtime conditions, and observed execution may change the result.

**Trust reality, not the account of reality.** Be equally skeptical of findings that sound impressive. A genuine defect needs a concrete failure mechanism and appropriate evidence; a claim of safety needs scope and coverage. Never invent execution, confidence, or test results.

The auditor should not change the target merely to make it fail, and must not quietly repair it while purporting to audit the untouched baseline.

## 0. Establish authority, scope, and a frozen baseline

Before an audit, determine:

- Authorized repository/project, exact commit SHA and branch, files or PR under review, deployment target, and whether the question is a whole-system audit, regression audit, or bounded merge decision.
- Which environment is genuinely available (read-only source, test fixture, disposable local runtime, authorized staging, production). No environment access is inferred from documentation.
- Supported platforms, version constraints, compatibility promises, security/trust boundaries, expected users, and meaningful failure impact.
- Permitted actions, prohibited systems or data, and whether writing tests, creating branches, or making remote changes is authorized.

Inspect actual entrypoints, build paths, imports, dependency resolution, configuration precedence, feature flags, persistence, migrations, startup/shutdown, and cleanup. Distinguish shipped code from unreachable code and test-only substitutes. Record the baseline; avoid unrecorded changes. Do not execute unknown scripts or untrusted dependencies outside an appropriately isolated environment.

## 1. Build an execution and trust map

1. **Trace real paths:** External input or trigger -> validation -> dispatch -> state mutation -> side effect -> output and cleanup. Follow actual call sites, not just module names.
2. **Identify invariants:** What must always be true, even after error, restart, cancellation, timeout, or concurrent operations?
3. **Mark trust boundaries:** Untrusted files and repositories, package dependencies, network responses, webhooks, bot commands, identity and authorization context, generated agent instructions, and persistent memory.
4. **Inventory failure surfaces:** Initialization, partial failure, exceptions, resource leaks, ordering, reentrancy, rollback, cache invalidation, migrations, compatibility, rate limits, and unbounded work.
5. **Inspect baselines:** Compare target behavior to the previous *actual executable or source revision*. History proves a change occurred, not that a feature works or that a defect was fixed.

### Overlays: plugin/module loaders, bots, and agents

For a module loader, independently inspect discovery, filename/path normalization, manifest parsing, identity collisions, load order, dependency cycles, dynamic imports, capability boundaries, registration, unload/reload, rollback after partial initialization, cleanup of handlers/tasks, and concurrent lifecycle transitions. Check whether validation examines the actual runtime artifacts rather than a convenient but different fixture.

For bot/agent code, additionally trace user/guild/tenant authorization, command dispatch, secrets, external API failure, message size, event duplication, retry idempotence, rate-limit behavior, untrusted tool or repository text, memory provenance, and whether an agent-generated artifact can silently gain operational authority.

## 2. Challenge the strongest failure hypotheses first

Prioritize by plausible impact, exposure, and likelihood, not by the attractiveness of a finding:

- **Security and privilege:** Authentication and authorization bypass, injection, path traversal, unsafe deserialization, data exposure, secrets, untrusted dependency or prompt-injection promotion, and unauthorized side effects.
- **Correctness and contracts:** Incorrect outputs, lost updates, wrong version or schema, broken invariants, unexpected fallbacks, silent failure, and branch or loader path mismatches.
- **Reliability and lifecycle:** Timeouts, retries, races, deadlocks, partial initialization, cancellation, resource leaks, corrupted recovery, and faulty rollback.
- **Interoperability and upgrade:** Real public APIs, declared compatibility, dependency behavior, integration ordering, deployment differences, and migration of pre-existing state.
- **Test integrity and coverage:** Misconfigured runners, tests that cannot reach the production path, brittle mocks, asserted wrong values, skipped suites, fake fixtures, false-green exit codes, and changes that alter acceptance criteria.

Exercise boundaries: missing/empty/duplicate/oversized/Unicode inputs; malformed records; clock and time-zone boundaries; permission changes; out-of-order events; concurrent calls; dependency absence; power/network failures; and restart/reload paths. Favor tests that distinguish a defect from innocent alternative explanations.

## 3. Verify independently; avoid evidence laundering

Use the strongest *available* safe evidence, recording exactly what was examined and executed:

| Evidence class | Permitted statement | Limitation |
| --- | --- | --- |
| Observed reproduction against actual revision/runtime | **CONFIRMED**, with command/input/output, environment, expected vs actual and a negative/control check where appropriate | Reproduction is scoped to the observed conditions |
| Source-level mechanism fully traced across reachable paths | **STATICALLY DEMONSTRATED**, with file/line/branch trace and concrete failing condition | No claim that an unavailable runtime was exercised |
| Failing test or tool alert independently inspected | **INDICATED**, until its oracle, reachability, setup and target are verified | A red test or scanner finding may be wrong |
| Suspicious code, missing test, or historical claim | **HYPOTHESIS / COVERAGE GAP**, with a proposed discriminating probe | Not a confirmed vulnerability |
| Inaccessible deployment, dependency, or test fixture | **NOT VERIFIED** | Never substitute an invented test execution |

For each suspected defect:
1. Specify the violated invariant, preconditions, actor, and expected versus observed result.
2. Trace the exact source-to-effect path at the inspected SHA, including configuration and error branches.
3. Construct the smallest safe reproducer in a disposable environment **if actually authorized and feasible**; preserve commands, inputs, outputs, versions, and timestamps.
4. Seek a counterexample: could the result be a false positive, intended behavior, unsupported configuration, or a mock-only artifact?
5. Recheck the original baseline and the proposed fix independently. Never weaken the oracle or silently alter acceptance criteria.
6. If a test cannot run, identify the blocked dependency and report the strongest source-only conclusion supported.

Use a read-only first pass. Do not run destructive payloads, scan third-party services, transmit secrets, or attack production without separately established authorization and safeguards. Redact private material from reports and public repositories.

## 4. Record findings without hiding uncertainty

Each finding should contain:

- **ID / concise title / affected component and revision**
- **Severity:** critical, high, medium, low, or informational, with specific impact and realistic preconditions
- **Evidence status:** CONFIRMED, STATICALLY DEMONSTRATED, INDICATED, HYPOTHESIS, COVERAGE GAP, or NOT VERIFIED
- **Exact location and path:** links or file:line references at a fixed revision, plus pertinent dependency/configuration versions
- **Failure mechanism and consequence:** actual violated invariant or attack boundary; distinguish exploitability from theoretical possibility
- **Reproducer or reasoning trace:** command and observable result if executed; source trace if not
- **Counterevidence / constraints / confidence:** what may invalidate the finding, unavailable artifacts, and scope limits
- **Remediation and regression proof:** minimal fix concept plus an independent test that would distinguish corrected behavior

Separate **severity** (consequence if true) from **confidence** (quality of evidence). Do not report a missing test as a proven functional failure. Record negative results and cleared suspicions, especially if they eliminate a previously plausible finding. Do not suppress serious observations because they lie outside the original PR diff when they affect the requested merge decision.

## 5. Merge-readiness gate

A review can be **GO**, **GO WITH EXPLICIT CONDITIONS**, **NO-GO**, or **INCONCLUSIVE**:

- **GO:** No blocking defects were found in the stated scope; applicable critical paths and regressions have adequate observed coverage. This is *not* a claim that the system has no bugs.
- **GO WITH EXPLICIT CONDITIONS:** Remaining issues are bounded, owned, and accepted under an authorized risk decision, with named follow-up checks.
- **NO-GO:** A confirmed or statically demonstrated blocker violates a required invariant, or critical acceptance evidence contradicts the change's claimed readiness.
- **INCONCLUSIVE:** Material runtime, source, dependency, security or test evidence is missing. Do not fabricate a GO from absence of observed failures.

Report the inspected SHA, changed/untouched paths, executed commands, whether tests actually ran, evidence limits, findings in descending risk, decision rationale, and the next decisive check. For a PR, distinguish *branch-only* review from merged default-branch behavior.

## 6. Audit the auditor

Before publishing: challenge at least one high-severity finding; check every cited line against the exact file revision; separate fact from conjecture; ask whether the test oracle could be faulty; look for uninspected entrypoints or hidden configuration; verify that findings were not based solely on the test suite, commit message, or prior agent summary. An authoritative tone is not evidence.

This document is a methodological candidate. It does not certify real audit performance. Behavioral evaluation requires an independent corpus with planted defects, false positives, adverse configuration, and withheld expectations; measure recall, precision, reproducibility, honest uncertainty, and cost against a baseline.

## External reference frameworks

These inform coverage and vocabulary; they do **not** replace observation of the target:

- [OWASP Application Security Verification Standard 5.0.0](https://asvs.owasp.org/) — stable web-application security requirements.
- [OWASP Web Security Testing Guide 4.2](https://owasp.org/projects/web-security-testing-guide) — stable web-application testing methodology; 5.0 is in development as of 2026-11.
- [NIST SP 800-218, Secure Software Development Framework](https://csrc.nist.gov/Projects/SSDF) — secure-development process context.
- [MITRE CWE](https://cwe.mitre.org/) — weakness classification when appropriate, never a substitute for a demonstrated mechanism.
