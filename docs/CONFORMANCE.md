# Conformance report

## Release result

Version 0.1 implements the local runtime, shared CLI/protocol surface, ten fixture agent packages, four workflows, trust and policy controls, evidence promotion, reviewed memory, and verification tooling. The standard-library conformance suite contains 32 tests and runs without credentials or network access.

## Architecture acceptance mapping

**1 — Resume after process failure.** A running attempt without a terminal event is reconciled to `interrupted`; completed stages come from the verified event ledger and are skipped. Tested by the resume/reconciliation conformance case.

**2 — Provenance-preserving isolated fork.** Thread rows retain parent and fork boundary; each thread receives a distinct writable state directory. Tested by the thread-fork conformance case.

**3 — Changed package loses trust.** Trust records pin the complete package digest. A mismatch becomes `changed` and routing rejects it. Tested by the changed-agent conformance case.

**4 — No unresolved promotion.** Claim state remains `draft` when a locator fails; promotion checks resolution and independent evaluation. Tested by the unresolved-claim conformance case.

**5 — Numeric result provenance.** Numeric claims require `numeric` evidence resolving to a content-addressed output locator; the attempt pins the producing package digest. Tested by the numeric-provenance conformance case.

**6 — Evaluation firewall.** Agent memory queries expose reviewed train/development records only, and marked dependency records are recursively redacted. Tested by the reviewed-memory firewall case.

**7 — Approval and budget.** Policy combines stage/package risk, project maximums, digest-bound approval, wall timeout, and declared usage checks. Tested by the approval and over-budget cases.

**8 — Failed evaluation remains inspectable.** Output and attempt artifacts are stored before gates run; gate failure marks the attempt without deleting workspace or artifacts. Tested by the failed-evaluator case.

**9 — Writer cannot treat drafts as facts.** Audit requires `reviewDecision=pass`; writer context contains promoted claims only and output must reverse-link their IDs. Tested by the writer-context case.

**10 — Advanced method has a matched control.** Strategy comparison requires a simple-control family, identical metric contract digest, and artifacts for both results. Tested by the optimizer-control case.

**11 — Scientific boundary outcomes survive.** Negative, inconclusive, saturated, and floored results complete normally and become durable run outcomes. Tested by the boundary-outcomes case.

**12 — More than one client shares a project.** CLI and initialized JSON protocol dispatcher call the same engine and observe the same event cursor and run state. Tested by the client-interoperability and event-cursor cases.

Additional conformance checks execute and verify all four workflows; detect event, artifact, and stage-result tampering; enforce run-scoped artifact access and idempotent request consistency; preserve malformed-agent failures; and keep the stdio protocol alive after malformed input.

## Deliberate boundaries

The local subprocess adapter uses copied attempt workspaces and post-execution source mutation detection. It automatically adds a Bubblewrap write/network boundary when its namespace and mount probe succeeds and can fail closed with `ARA_OS_SANDBOX=required`. Bubblewrap still exposes the host read-only and cannot enforce hostname allowlists; stronger confidentiality and network policy require a hardened container, VM, or deployment proxy. The runtime reports the active boundary through `server/diagnostics` and `ara doctor`.

The included agent packages are deterministic fixtures. Real model intelligence, scientific data connectors, scheduler jobs, and remote tools enter through versioned adapters and must still pass the same state, policy, evidence, and evaluation mechanisms.

Phases 7–10 remain deferred: scheduler/container orchestration, broad advanced search, publication rendering and external publishing, and distributed deployment.
