# Discussion Trace — B8.1 (auto-research-discussion, Stages 1–6)

> Mode: **autoclaude / self-play** (Claude plays proposer, critic, and refiner;
> no human in the loop). Seed: the topic's `README.md` only (Chinese, structured
> frontmatter, ~42 lines, sourced from `trend_scan_2026-08.md` §2.1 + the
> 2026-08-13 occupancy sweep). There is **no** `digest.md` and **no** `paper.md`
> for this topic — the seed is immature, so the six stages below *derive* the
> formal problem, assumptions, and RQs-with-fallbacks from scratch rather than
> reading them off a pre-registered spec. Round cap: 5/stage (none hit). Each
> stage ran propose → **one genuine critic round** (a real, evidence-grounded
> `[major]` or `[minor]` per `autoclaude_mode.md`'s anti-sycophancy rules — no
> rubber-stamping) → one conservative refiner pass → confirmed output. Anti-
> sycophancy Rule 3 ("disagreement is a feature") was honored: every stage
> carries at least one substantive pushback with cited seed/literature evidence.
>
> **Full pipeline order:** this file (`auto-research-discussion`, 6 stages) →
> `taste_audit.md` (`research-taste-auditor`, idea-level check on the confirmed
> Stage 2 + Stage 5) → `stage_review.md` (`pengsida-stage-reviewer`,
> PASS/REVISE/STOP per stage, plus a Writing check on the first assembled draft)
> → `paper_draft.md`/`.tex`/`.pdf`. REVISE findings from `stage_review.md` are
> folded into the `paper_draft.*` files; see `stage_review.md` for the reasoning.

## Seed brief

- **One-sentence description:** For each normative-clause change between two
  adjacent agent-protocol specification versions (MCP / A2A), measure whether
  deployed servers pass through a *divergence window* — a period in which their
  wire-level behavior conforms to neither the old version nor the new one — and
  whether, inside that window, authority-bearing constraints silently degrade
  from *enforced* to *visibility-only*.
- **Apparent inputs:** two adjacent published protocol specs (their RFC-2119
  normative clauses); a longitudinally re-sampled public directory of remote
  deployed MCP servers; wire-level request/response transcripts.
- **Apparent outputs:** a per-(server, clause-delta) conformance verdict over
  time; a divergence-window prevalence and width distribution; a prevalence of
  authority→visibility downgrades; a clause-delta-type breakdown.
- **Closest research areas / vocabulary:** protocol conformance / differential
  testing (AgentRFC 2603.23801); deployed-measurement security studies (remote
  MCP-server measurement, 2605.22333); agent-protocol governance (Governance
  Gaps 2606.31498, ContextNest 2607.02116); capability/authority vs. visibility
  (Capability Gates Are Not Authorization 2606.28679; HCP 2606.29073).
- **In scope:** measuring *already-deployed* MCP/A2A servers against the
  published specs, on the wire, across a version transition. **Out of scope:**
  proposing a replacement protocol or execution layer; verifying a spec against
  its own formal model (that is AgentRFC's spec-side lane); training anything.
- **Confidence: medium.** The seed is a single structured README with a strong
  falsifiable claim and a named minimal experiment, but — unlike a repo with
  code — it carries no formal problem definition, no assumption ledger, and no
  RQ machinery. All of that is constructed below at full critic strength. The
  main reconstruction risk is *over-claiming the security angle* (authority
  downgrade) beyond what a wire-level probe can actually witness; the stages
  guard against this explicitly (Stage 1 minor, Stage 3 major).

---

## Stage 1 — Problem Definition

### Round 1 (critic phase)

**draft_v1** (proposer):
- `summary`: Given two adjacent published versions N and N+1 of an agent-
  interoperability protocol (MCP or A2A) and the set of normative (RFC-2119
  MUST/SHALL/SHOULD) clauses that changed between them, and given a public
  directory of deployed remote servers observed repeatedly over time, determine
  for each changed clause whether a server's wire-level behavior conforms to N,
  to N+1, to both, or to neither — and, for the "neither" verdicts, whether an
  authority constraint the clause governs has silently ceased to be enforced.
- `input`: (1) two adjacent spec versions, decomposed into a set of normative
  clauses with their requirement force (MUST / MUST NOT / SHOULD); (2) the
  clause-level diff Δ(N, N+1) = added / removed / modified clauses; (3) a public
  directory of deployed remote servers, each reachable at a wire endpoint and
  re-observable at successive times t₁ < t₂ < …; (4) for each clause, a
  conformance probe (a request/interaction whose response classifies behavior).
- `output`: (1) a per-(server, clause-delta, time) verdict ∈ {N-only,
  (N+1)-only, both, neither}; (2) a *divergence window* per (server, clause) =
  the interval over which the verdict is "neither"; (3) among authority-bearing
  clauses, a per-server *downgrade* label (enforced → advertise-only → silent);
  (4) the population-level distribution of window prevalence and width, and of
  downgrade prevalence.
- `constraints`: probes must classify behavior from the wire alone (no server
  source access); every probe must be reproducible and its verdict
  deterministic given a fixed server state; the measurement instrument must know
  each clause's intended semantics even though a deployed server need not.
- `objective`: a divergence-window / downgrade estimate is correct if its
  per-(server, clause) verdicts match the ground-truth conformance of controlled
  reference implementations pinned at N and at N+1, and if its population
  estimates carry a stated validity envelope (probe validity, directory
  coverage, temporal resolution).
- `study_type`: **empirical** — stated explicitly, not inferred: the seed's label
  is `[证据]` (evidence), its falsifiable claim is about a *measured* phenomenon
  (divergence windows exist and are measurable; authority degrades to
  visibility), and its truth mechanism is measurement ("wire-level pass/fail on
  real deployed servers"). No new protocol is proposed as a fix.

**critique** (teacher, evidence-grounded):
- summary: The problem is concrete and evidence-traceable to the README, and
  `study_type` is correctly `empirical`. But the central verdict has a real
  evaluability gap grounded in the seed's own multi-version reality, and one
  output presupposes the direction of the very thing being measured.
- comments:
  - `{severity: major, field: "output(1)/summary", anti_pattern: "fields_misaligned (evaluability gap)", comment: "The verdict 'conforms to N, N+1, both, or neither' is under-specified when the *deployed population spans more than two versions*. The README itself notes MCP is iterating fast (RC 2026-07-28) and A2A is at 1.0.1 — so at any sweep the directory contains servers pinned to N−1, N, N+1, and drafts of N+2. A server correctly pinned to N−1 would satisfy neither N nor N+1's *changed* clauses and be spuriously scored as a divergence window, inflating the headline estimand. The 'neither' verdict needs a defined reference frame: which adjacent pair (N, N+1) brackets *this* server before its clause behavior can be called a divergence rather than an ordinary older/newer-version conformance."}`
  - `{severity: minor, field: "output(3)", anti_pattern: null, comment: "'whether an authority constraint has silently ceased to be enforced' presupposes the enforced→unenforced *direction*. Whether enforcement degrades (vs. is unchanged, or even tightens N→N+1) is part of what is measured. Prefer a neutral enforcement-status classification (enforced / advertise-only / silent) whose *transition* is then read off, rather than baking the downgrade into the output definition."}`
- decision: `move_to_refiner` (both are formalize-level fixes using content the
  seed already implies — a reference-frame definition and a neutral relabeling;
  no new mechanism).

### Refiner pass

- `output(1)` and `summary` (refined): the verdict is defined **relative to the
  adjacent version pair (N, N+1) that straddles the server's observation
  window**, where N is fixed as the latest version whose publication precedes the
  server's first observed conformance and N+1 the next published version. A
  server conforming to some N−1 or N+2 on a changed clause is labeled
  **out-of-frame** (a distinct fifth category), *not* "neither" — only a server
  that was observed conforming to N (or N+1) and later conforms to neither is
  counted toward a divergence window. Version bracketing is resolved from the
  server's advertised `protocolVersion` / handshake where present (see A3).
- `output(3)` (refined): each authority-bearing clause carries a neutral
  **enforcement-status** label at each time — *enforced* (unauthorized action
  rejected on the wire), *advertise-only* (the constraint appears in a capability
  descriptor or error text but the unauthorized action still succeeds), *silent*
  (neither rejected nor advertised). A "downgrade" is then a *measured transition*
  enforced → advertise-only / silent, not a presupposed property.
- `formal_summary` (added, per the stage-1 refiner's formalize-for-free duty):
  "Versions N, N+1 with normative-clause sets C_N, C_{N+1}; clause diff Δ =
  Δ(N,N+1). For clause-delta δ ∈ Δ, matched probe pair (p_δ^N, p_δ^{N+1}).
  Server s ∈ S observed at times t₁<…<t_m. Verdict v(s,δ,t) ∈ {N, N+1, both,
  neither, out-of-frame}. Divergence window W(s,δ) = maximal interval with
  v = neither, conditional on s being in-frame for (N,N+1). For authority-
  bearing δ, enforcement status e(s,δ,t) ∈ {enforced, advertise-only, silent};
  downgrade D(s,δ) = a transition enforced→{advertise-only, silent} coincident
  with δ. Estimands: prevalence and interval-censored width of W over S; and
  prevalence of D among authority-bearing δ."
- `changes_made`: added the version-bracketing reference frame + out-of-frame
  category (closes the evaluability gap); relabeled the downgrade output as a
  neutral enforcement-status transition (removes the presupposition); added
  `formal_summary`.
- `declined_to_fix`: none.

**Confirmed Stage 1** — `study_type: empirical`.

---

## Stage 2 — Motivation

### Round 1 (critic phase)

**draft_v1:**
- `summary`: Agent-interoperability protocols are being adopted as the substrate
  for cross-vendor tool use and delegation, and they are iterating monthly; yet
  whether the servers already deployed against them actually track a spec across
  a revision — or fall into a window where they conform to neither the old nor
  the new version — has never been measured on the wire, even though a policy
  demand for exactly this assurance now exists (NSA/CISA MCP security CSI,
  2026-06).
- `why_it_matters`: A protocol revision is normally assumed to move the ecosystem
  cleanly from N to N+1. If instead a measurable fraction of deployed servers sit
  in a divergence window — passing neither version's changed normative clauses —
  then every client that negotiates with them is interoperating against an
  unspecified behavior, and any assurance argument that cites "conforms to MCP
  vX" is void for the duration of that window. Worse, the seed's sharp claim is
  that *authority* constraints are the ones that degrade quietly: a clause that
  in one version requires the server to *reject* an unauthorized tool call can,
  mid-transition, degrade so the constraint is merely *advertised* (surfaced in a
  descriptor) while the unauthorized call still succeeds — a security regression
  that no single-version conformance check and no static framework audit would
  catch, because it exists only *between* versions and only on the wire.
- `who_cares`: operators who delegate actions through MCP/A2A servers and rely on
  "spec-conformant" as a safety label; client and gateway authors who must decide
  whether to trust a server's advertised version; standards maintainers deciding
  how fast to iterate normative clauses; and the security agencies (NSA/CISA CSI)
  now issuing MCP guidance that presumes a measurable conformance baseline exists.
- `evidence`: the README's evidence base — AgentRFC (2603.23801) checks a *spec*
  against its own TLA+ model but its artifact is withheld under coordinated
  disclosure, so no deployed-side reproducible check exists; the remote-MCP-server
  measurement study (2605.22333) proves deployed-side wire measurement is
  publishable but is single-version; Governance Gaps (2606.31498) *argues* a
  gap matrix of what MCP/A2A/ACP cannot express without measuring it; Capability
  Gates Are Not Authorization (2606.28679) establishes the visibility-vs-authority
  distinction conceptually at the framework layer. The environmental signal
  (NSA/CISA MCP CSI, 2026-06) is a real, dated policy demand.

**critique:**
- summary: Stake-specific and well-evidenced, real named neighbors, correct "why
  now" (monthly iteration + CSI). But coverage of Stage 1's outputs is
  incomplete in one specific, load-bearing way.
- comments:
  - `{severity: major, field: "why_it_matters", anti_pattern: "partial_output_coverage", comment: "Stage 1's output (4) includes the *interval-censored width distribution* of the divergence window — a temporal quantity, not just a prevalence. why_it_matters motivates why divergence windows and authority downgrades *exist* and matter, but never says why their *duration* matters as opposed to a one-time snapshot of 'which servers are non-conformant right now.' A reviewer will ask: why not just audit conformance once? Without a duration argument, the whole longitudinal apparatus (repeated sweeps, survival estimation) reads as over-engineering. The real answer — a window's width is the *exposure duration* of the interop breakage / authority gap, and a snapshot cannot tell 'transiently mid-upgrade for a day' from 'persistently stuck between versions for months,' which have very different security and interop consequences at identical prevalence — needs to be in the motivation."}`
- decision: `move_to_refiner`.

### Refiner pass

- `why_it_matters` (extended): "…and the *duration* of that window is not a
  detail but the quantity that decides how much it matters: a divergence window
  is an exposure interval — the length of time a client can negotiate against an
  unspecified behavior, or an authority constraint can sit un-enforced — so two
  ecosystems with identical instantaneous non-conformance prevalence but window
  widths of a day versus a quarter carry very different real risk. A single
  conformance snapshot cannot distinguish a server transiently mid-upgrade from
  one persistently stranded between versions; only per-server tracking across
  repeated sweeps recovers the width, which is exactly why the estimand is a
  censored *duration* distribution and not a one-shot audit."
- `changes_made`: added the exposure-duration coverage argument tying Stage 1
  output (4)'s width distribution to why longitudinal measurement is necessary.
- `declined_to_fix`: none.

**Confirmed Stage 2.**

---

## Stage 3 — Related Work

The seed names its neighbors directly; all are treated as **specific (deep)
tier** — the README's evidence base already engages each at the approach +
limitation level. Per the no-fabrication rule, no landscape papers are invented
to pad a `general_related_works` list; the general tier is populated only with
the methodological anchors genuinely used (differential testing, survival
analysis, RFC-2119) which are real and well-known.

### Round 1 (critic phase)

**draft_v1** (`specific_related_works`, abbreviated to citation / I-O framing /
comparison / limitation):

| work_id | citation | is_potential_baseline | comparison + limitation (→ the sub-problem/positioning it drives) |
|---|---|---|---|
| `rw_agentrfc` | AgentRFC (2603.23801) | false | **problem_alignment: related.** spec → typed IR → TLA+ model checking → SDK counterexample replay. I/O = a *spec artifact* in, a model-checking verdict + counterexample out. Ours = a *deployed server on the wire* in, a differential conformance verdict out. `method_addresses: false` (their pipeline never contacts a deployed endpoint; it certifies the spec, not the fleet). Limitation for us: single-version, spec-side, and its artifact is withheld under coordinated disclosure — so no reproducible deployed-side check exists. |
| `rw_capgates` | Capability Gates Are Not Authorization (2606.28679) | false | **problem_alignment: related.** Establishes the visibility-vs-authority distinction at the *framework/config* layer via static audit. `method_addresses: false` for our estimand (it never touches protocol wire behavior or a version transition). Limitation: the axis is conceptual and static; whether authority actually degrades to visibility *on the wire*, *during a revision*, on *deployed* servers, is unmeasured. |
| `rw_hcp` | HCP (2606.29073) | false | **problem_alignment: different.** Proposes *replacing* the execution layer with 8 security invariants + 10 attack benchmarks. `method_addresses: false` (it prescribes a new layer; it does not measure the gaps of existing specs). Its metadata-non-authority invariant partially overlaps our authority axis but is a design proposal, not a measurement of the installed base. |
| `rw_remotemcp` | Remote-MCP-server measurement (2605.22333) | **true (method exemplar, not a beat-a-number baseline)** | **problem_alignment: related.** Deployed-side wire measurement of remote MCP servers (auth posture). I/O matches ours (deployed endpoint in, measured property out). `effectiveness: proven_better` for the *method class* (proves deployed measurement is publishable). Limitation: single-version, single-snapshot; no clause-diff, no divergence window, no longitudinal/differential axis. We borrow its deployed-measurement methodology, not its findings. |
| `rw_govgaps` | Governance Gaps (2606.31498) | false | **problem_alignment: related.** *Argues* a matrix of what MCP/A2A/ACP cannot express. `method_addresses: false` (argumentative, not instrumented). Limitation: the gap matrix is asserted, never measured against deployed behavior — our downgrade-classification turns an *argued* gap into a *measured* one. |
| `rw_contextnest` | ContextNest (2607.02116) | false | **problem_alignment: different.** Proposes verifiable context governance (a mechanism). `method_addresses: false`. Related-for-context only: it governs context provenance, not spec-version conformance. |

**critique:**
- summary: Grounding is solid and each limitation is specific. But there is an
  `unhandled_threat`: two of these papers pressure the *authority-downgrade*
  half of the contribution hard enough that leaving them as ordinary "related
  work" would be a novelty crisis at review.
- comments:
  - `{severity: major, field: "specific_related_works[rw_capgates, rw_hcp]", anti_pattern: "unhandled_threat", comment: "The README's own risk clock warns the authority→visibility angle 'sits in the narrow gap between AgentRFC and 2606.28679' and that 'HCP's metadata-non-authority invariant partially overlaps the authority axis.' Capability-Gates already owns the *concept* 'visibility ≠ authority,' and HCP already owns a *metadata-is-not-authority* invariant. If the paper presents the authority-downgrade finding as if the visibility-vs-authority distinction were novel, a reviewer who knows 2606.28679 will reject it as re-labeling. Per the stage-3 rubric a threat_to_motivation this high must be *repositioned against*, in one explicit sentence, not filed quietly. The genuine, defensible delta is not the distinction itself but its *measured, longitudinal, wire-level instantiation on deployed servers across a version transition* — which neither paper does. Concede the concept; claim the measurement."}`
  - `{severity: minor, field: "specific_related_works[rw_remotemcp].is_potential_baseline", anti_pattern: "io_approach_mismatch (mild)", comment: "Marking 2605.22333 a 'baseline' risks implying we compare against its reported auth-posture numbers, which we do not (this is empirical — nothing to beat). Its role is a *method exemplar* whose deployed-measurement protocol we extend to a differential/longitudinal axis. Sharpen the label so it doesn't read as a beat-a-number comparison."}`
- decision: `move_to_refiner` (the major is a positioning/framing move — a
  concede-and-differentiate sentence — not a redesign; the minor is a
  label-precision fix).

### Refiner pass

- Added an explicit **nearest-neighbor repositioning sentence** to be carried
  verbatim into Related Work and the Introduction: *"Capability Gates Are Not
  Authorization (2606.28679) draws the visibility-vs-authority distinction, and
  HCP (2606.29073) encodes a metadata-is-not-authority invariant — but both do so
  as static, framework-layer design claims; the contribution here is not that
  distinction but its measurement, on the wire, on deployed servers, across a
  normative-clause revision, where an authority constraint's degradation to
  visibility-only becomes an observable transition rather than a conceptual
  possibility."*
- `rw_remotemcp.is_potential_baseline` retained `true`, but role sharpened to
  **method exemplar / borrowed protocol**: "Not a beat-a-number baseline —
  2605.22333's reported findings are not compared against; its deployed-side
  wire-measurement protocol is *extended* to a clause-differential, longitudinal
  axis." (Mirrors the Stage-3 handling in B5.5 of an I/O-mismatched work.)
- **Note on `verify_as_hypothesis`:** set `false` on every limitation — no
  Stage-3 limitation is promoted to a framing-tier RQ. The closest candidate
  (Governance Gaps' *argued* matrix → our *measured* one) is not a distinct
  external hypothesis to verify but restates this paper's own core estimand,
  already covered end-to-end by mechanism-tier RQs in Stage 6. Per stages.md:
  "If nothing was flagged, emit zero framing-tier RQs."
- `changes_made`: added the concede-and-differentiate repositioning sentence for
  the two threat papers; sharpened the 2605.22333 role.
- `declined_to_fix`: none.

**Confirmed Stage 3.**

---

## Stage 4 — Sub-Problems

### Round 1 (critic phase)

**draft_v1** (4 sub-problems):

- **`sp_probe_faithfulness`** — *description:* turn each natural-language
  normative-clause delta into a wire-level probe whose pass/fail *deterministically
  separates* an N-conforming from an (N+1)-conforming server on exactly that
  clause. *why_it_is_a_problem:* if a probe's verdict tracks incidental server
  behavior rather than the clause's semantics, every downstream divergence-window
  count is an artifact of the probe, not of the ecosystem. *technical_challenge:*
  RFC-2119 clauses are prose; a matched probe pair must be *provably discriminating*
  on known-ground-truth references before it can label an unknown server "neither."
  *source_limitation_ids:* `["__novel__"]` (no cited work synthesizes wire probes
  from a clause diff).
- **`sp_drift_attribution`** — *description:* attribute a "neither" verdict to the
  version delta rather than to a generic server bug, a transient error, or plain
  non-conformance unrelated to the revision. *why_it_is_a_problem:* a single
  "neither" could be a one-off 500, a rate-limit, or a server that was simply
  always broken — none of which is a *divergence window*. *technical_challenge:*
  requires (a) a placebo of *unchanged* clauses that cannot produce a version-
  induced "neither" by construction, and (b) persistence across repeated sweeps
  to separate transient from durable. *source_limitation_ids:* `["__novel__"]`.
- **`sp_authority_classification`** — *description:* decide, from the wire, which
  clause deltas are authority-bearing and whether an authority constraint is
  *enforced*, *advertise-only*, or *silent* on a given server at a given time.
  *why_it_is_a_problem:* not every "neither" is a security downgrade; conflating
  representational changes with enforcement changes would over-claim the security
  finding. *technical_challenge:* the enforce/advertise distinction must be read
  off whether an *unauthorized* wire call is rejected vs. succeeds-while-advertised
  — operationalizing 2606.28679's static axis as a wire observable.
  *source_limitation_ids:* `["__novel__"]` (grounded in, but not solved by,
  2606.28679).
- **`sp_censored_window`** — *description:* estimate the *width* of a divergence
  window from a coarse, irregular polling schedule with servers entering and
  leaving the directory. *why_it_is_a_problem:* a naive width (first-to-last
  "neither") both under-counts (sub-cadence windows) and over-counts (churn), so
  the headline duration would be biased. *technical_challenge:* windows are
  interval-censored (entry/exit bracketed by sweeps) and right-censored (still
  diverging at last sweep, or the server disappears); an honest width needs
  survival estimation with an explicit resolution floor. *source_limitation_ids:*
  `["__novel__"]`.

**critique:**
- summary: The four sub-problems make each verdict *trustworthy*, *attributable*,
  *interpretable*, and *durationally honest* — and their union does deliver Stage
  1's outputs. But there is a genuine `undercoverage` gap that a USENIX-Security
  reviewer will raise immediately, and it is decisive for *this specific* study.
- comments:
  - `{severity: major, field: "sub_problems (coverage)", anti_pattern: "undercoverage", comment: "To measure whether an *authority* clause is enforced, a probe must attempt an *unauthorized action* and observe whether it is rejected. On a *live, third-party deployed* server this is (a) an ethics/safety problem — an unauthorized action that is *not* rejected has, by definition, just been *performed* against someone's production server — and (b) a measurement confound: a probe that mutates server state changes what later sweeps observe, corrupting the very longitudinal window estimation sp_censored_window depends on. No current sub-problem covers 'how do we witness enforcement without causing the unauthorized effect.' This is not optional polish: authority-clause measurement on live servers is *impossible* without solving it, so it is a decisive, novel sub-problem — not an assumption. Missing it would either sink the paper at ethics review or silently confound the downgrade estimand."}`
  - `{severity: minor, field: "sp_drift_attribution / sp_censored_window", anti_pattern: "overlap", comment: "Both invoke 'repeated sweeps,' which can read as one sub-problem twice. They are distinct — attribution is about *whether* a 'neither' is drift (a classification / placebo problem), estimation is about *how wide* the window is (a censored-duration problem) — but the descriptions don't make the distinction explicit."}`
- decision: `move_to_refiner` — but the major requires *adding* a sub-problem,
  which is a legitimate refiner-adjacent structural change flagged and applied
  here (the refiner adds the decisive component the critic identified, without
  redesigning the existing four).

### Refiner pass

- **Added `sp_safe_authority_probing`** (`source_limitation_ids: ["__novel__"]`)
  — *description:* witness whether an authority constraint is enforced *without*
  causing the unauthorized effect on a live third-party server. *why_it_is_a_
  problem:* authority-clause measurement is impossible on live servers otherwise —
  a non-rejected unauthorized action is a real unauthorized action, and a
  state-mutating probe confounds later sweeps. *technical_challenge:* enforcement
  must be inferred from the *rejection decision* (the server's accept/deny at the
  authorization boundary) using read-only / idempotent / dry-run request forms;
  destructive forms that *must* attempt a real mutation run only against consenting
  reference or self-hosted deployments, and any residual authority test on a live
  server is gated behind coordinated disclosure. This is a distinct measurement
  sub-problem (how to observe the accept/deny decision safely), not merely an
  ethics caveat.
- `sp_drift_attribution.technical_challenge` sharpened to end: "…this is a
  *classification/placebo* problem — separating drift-induced 'neither' from
  generic non-conformance via an unchanged-clause control — not a duration
  problem."
- `sp_censored_window.technical_challenge` sharpened to end: "…this is a
  *censored-duration* problem distinct from attribution — even once a 'neither'
  is confirmed drift-induced, its *width* is unknown without survival estimation
  over the sweep schedule; more sweeps of the same cadence do not fix the
  resolution floor, only finer cadence does."
- `changes_made`: added the decisive `sp_safe_authority_probing` sub-problem;
  made the attribution-vs-estimation distinction explicit.
- `declined_to_fix`: none.

**Confirmed Stage 4** (5 sub-problems; all `["__novel__"]` — grounded in, but not
solved by, the cited neighbors).

---

## Stage 5 — Method Design

### Round 1 (critic phase)

**draft_v1** (5 methods):

- **`m_probe_synthesis`** → targets `sp_probe_faithfulness`. *proposed_approach:*
  for each clause-delta δ, hand-author a *matched probe pair* (p_δ^N, p_δ^{N+1})
  — a wire interaction that a strictly-N-conforming server passes and a strictly-
  (N+1)-conforming server fails, and its converse — then *validate discrimination*
  against two pinned reference implementations (the official SDK/reference server
  tagged at N and at N+1): the N-reference must be classified N-only and the
  (N+1)-reference (N+1)-only. Only probes that separate the references are admitted
  to the live sweep. *key_insight:* a probe earns the right to call an unknown
  server "neither" only after it *provably* separates two known-ground-truth
  versions — differential discrimination on references is the instrument-validation
  step (guidance R2) that makes a wire "neither" meaningful rather than an
  arbitrary failed request. *hypotheses:* ["The matched probe pairs correctly
  classify the two pinned reference implementations — N-reference as N-only,
  (N+1)-reference as (N+1)-only — on ≥95% of the clause-delta set; residual
  misclassifications are attributable on inspection to genuinely ambiguous clause
  text, not probe error."]
- **`m_safe_probing`** → targets `sp_safe_authority_probing`. *proposed_approach:*
  express every authority probe in a *non-destructive* form — a read-only or
  idempotent request, or a dry-run/`checkOnly` variant, that forces the server to
  emit its accept/deny decision *at the authorization boundary* before any state
  change; any probe whose only faithful form must attempt a real mutation is run
  solely against consenting reference/self-hosted servers, never live third-party
  ones, and a harness assertion refuses to emit a state-mutating unauthorized call
  to a live endpoint. *key_insight:* enforcement is a property of the *rejection
  decision*, not of the mutation — so observing accept/deny at the boundary
  witnesses enforcement without performing the unauthorized effect, decoupling the
  measurement from the harm. *hypotheses:* ["The non-destructive protocol
  reproduces the full-interaction conformance verdict on ≥98% of reference-server
  clause deltas, and a harness-level assertion confirms zero state-mutating
  unauthorized calls are issued to any live third-party server."]
- **`m_placebo_persistence`** → targets `sp_drift_attribution`. *proposed_approach:*
  alongside changed-clause probes, run probes for a matched set of *unchanged*
  normative clauses (same requirement force, similar request shape, identical text
  in N and N+1), for which a version-induced "neither" is impossible by
  construction; count a changed-clause "neither" as a divergence window only if it
  (a) persists across ≥k consecutive sweeps and (b) exceeds the unchanged-clause
  failure baseline. *key_insight:* only spec drift can make a *changed* clause fail
  both ways while a matched *unchanged* clause of similar difficulty does not — the
  changed-vs-unchanged contrast (a within-server placebo) is the discriminating
  condition, and persistence separates durable drift from transient error.
  *hypotheses:* ["Across the swept population, the prevalence of persistent (≥k
  sweeps) 'neither' verdicts on changed clauses exceeds the matched unchanged-
  clause placebo baseline by ≥10 percentage points (paired two-proportion /
  McNemar test, Holm-corrected across clause-deltas, α=0.05).", "Servers that fail
  changed-clause probes do not fail matched unchanged-clause probes at the same
  rate — the within-server changed-minus-unchanged failure gap is > 0 — so
  'neither' is attributable to the version delta, not to generic non-conformance."]
- **`m_authority_classifier`** → targets `sp_authority_classification`.
  *proposed_approach:* pre-label each clause-delta on two axes — (i) authority-
  bearing (the clause requires the server to reject/deny an action) vs.
  representational (formatting, naming, transport); (ii) for authority-bearing
  clauses, read the wire behavior as *enforced* / *advertise-only* / *silent*; a
  *downgrade* is a transition enforced→{advertise-only, silent} coincident with the
  delta. Labels are validated by ≥2 independent annotators (κ≥0.7). *key_insight:*
  the enforce/advertise distinction is exactly 2606.28679's visibility-vs-authority
  axis, but read directly off whether an unauthorized wire call is *rejected* or
  *succeeds-while-advertised* — making "authority degraded to visibility-only" a
  wire-observable transition rather than a conceptual claim. *hypotheses:* ["Among
  authority-bearing changed clauses, a pre-registered floor (≥15%) of servers
  observed transitioning across the delta exhibit an enforced→advertise-only or
  enforced→silent downgrade coincident with the delta.", "Divergence windows and
  authority downgrades are non-uniformly distributed across clause-delta types —
  concentrated (≥2× enrichment, log-odds > 0 with a pre-registered minimum support)
  in added-MUST, strengthened-SHOULD→MUST, and retyped-authority deltas relative to
  representational deltas."]
- **`m_censored_estimator`** → targets `sp_censored_window`. *proposed_approach:*
  treat each confirmed (server, clause) window as an interval-censored duration
  (entry bracketed by the last-conforming and first-"neither" sweeps; exit by the
  last-"neither" and first-reconforming sweeps), right-censored when still diverging
  at the final sweep or the server leaves the directory; fit a Turnbull /
  Kaplan-Meier estimator and report the median width with CIs and the fraction of
  windows resolvably above the sweep-cadence floor. *key_insight:* a coarse polling
  schedule cannot be turned into an honest width by subtraction — only survival
  estimation with explicit censoring and a stated resolution floor converts the
  schedule into a defensible duration distribution. *hypotheses:* ["The interval-
  censored median divergence-window width exceeds the sweep-cadence resolution
  floor by a factor ≥2 (windows are multi-sweep durations, not single-sweep
  blips), with the estimator's lower CI above the floor."]

**critique:**
- summary: Every method has a real mechanism (no goal-restatement), every
  hypothesis is falsifiable with a stated threshold, and each targets a distinct
  Stage-4 sub-problem. One method carries two of the paper's most central claims
  and needs a one-line justification that they issue from one instrument, not two.
- comments:
  - `{severity: minor, field: "m_placebo_persistence.hypotheses / m_authority_classifier.hypotheses", anti_pattern: null, comment: "Two methods each carry two hypotheses (placebo: existence + attribution; authority: downgrade-prevalence + type-concentration). For an empirical study this is fine, but as written it can read as scope creep bundled into one method. State explicitly, per method, why one mechanism yields two separately-falsifiable readouts — e.g. the changed-vs-unchanged contrast produces *both* the existence test (changed > placebo) and the attribution test (within-server changed−unchanged gap) from the *same* paired design; and the two-axis labeling produces *both* the downgrade prevalence and its clause-type enrichment from the *same* labeled verdict stream."}`
- decision: `move_to_refiner`.

### Refiner pass

- `m_placebo_persistence.key_insight` extended: "…the same paired changed-vs-
  unchanged design yields two distinct, separately-falsifiable readouts from one
  instrument: the *population* contrast (changed-clause 'neither' prevalence minus
  placebo baseline) tests *existence* (H2), and the *within-server* contrast
  (per-server changed-minus-unchanged failure gap) tests *attribution* (H5) — one
  placebo, two estimands, not two mechanisms."
- `m_authority_classifier.key_insight` extended: "…the same two-axis labeled
  verdict stream yields two readouts: the *rate* of enforced→advertise/silent
  transitions tests *downgrade prevalence* (H4), and the *distribution* of those
  transitions (and of divergence windows) across clause-delta types tests
  *concentration* (H6) — one labeling scheme, two estimands."
- `changes_made`: justified the two-hypotheses-one-method structure explicitly for
  both methods (mirrors B5.5's one-instrument-two-estimands handling).
- `declined_to_fix`: none.

**Confirmed Stage 5** — 5 methods, **7 hypotheses total** (probe H1; safe-probing
H7; placebo H2 + H5; authority H4 + H6; estimator H3), mixing instrument-validity
claims (H1, H7) with the study's headline empirical predictions (H2–H6) — a
deliberate design for an `empirical` study_type, accounted for in Stage 6.

---

## Stage 6 — Experiment Design

**Tier accounting (checked against `study_type = empirical`):**
- **Mechanism-tier: 7 RQs**, one per Stage-5 hypothesis (verbatim
  `target_hypotheses`).
- **Framing-tier: 0 RQs** — no Stage-3 limitation was flagged
  `verify_as_hypothesis`; none manufactured.
- **Outcome-tier: 0 RQs** — `study_type = empirical` forbids "our procedure beats
  baseline X" framing. The reference implementations and the unchanged-clause
  placebo are *controls / instrument-ground-truth*, never competitors to beat.

### Round 1 (critic phase)

**draft_v1:**

`datasets` (measurement targets, not training data):
- **MCP spec pair (N, N+1)** — the two adjacent published MCP versions bracketing
  the study window (e.g. the 2026-07-28 RC and its predecessor). *justification:*
  the seed's primary target; adjacent, recently published, with a concrete
  normative-clause diff to synthesize probes from.
- **A2A spec pair (1.0.0 → 1.0.1 extension, 2026-05)** — *justification:* a
  second protocol lets the divergence-window phenomenon be tested for
  protocol-independence rather than being an MCP-specific artifact; the 1.0.1
  extension gives a smaller, cleaner clause diff as a contrast to MCP's larger one.
- **Public remote-MCP-server directory** — *justification:* the deployed
  population; re-sampled on a fixed sweep cadence to yield the longitudinal panel.
- **Two pinned reference implementations per protocol (N-ref, N+1-ref)** —
  *justification:* known-ground-truth servers for probe-discrimination validation
  (RQ1) and safe-probing equivalence (RQ7); the only "gold" conformance labels in
  the study.

`baselines` (controls / ground-truth, not outcome-tier competitors):
- **Unchanged-clause placebo** — matched normative clauses identical in N and N+1;
  their "neither" rate is the null baseline every changed-clause claim is measured
  against (guidance B0).
- **Pinned reference implementations** — provide the ground-truth verdicts the
  probes are validated against; not compared for a win.
- **Rival explanation — generic non-conformance (B-alt)** — the within-server
  changed-minus-unchanged design (RQ5) isolates drift from servers that are simply
  broadly non-conformant.

`research_questions` (7, all mechanism-tier):

| rq_id | target_sub_problem_id | target_hypotheses (verbatim) |
|---|---|---|
| `rq_probe_discrimination` | `sp_probe_faithfulness` | "The matched probe pairs correctly classify the two pinned reference implementations — N-reference as N-only, (N+1)-reference as (N+1)-only — on ≥95% of the clause-delta set; residual misclassifications are attributable on inspection to genuinely ambiguous clause text, not probe error." |
| `rq_window_existence` | `sp_drift_attribution` | "Across the swept population, the prevalence of persistent (≥k sweeps) 'neither' verdicts on changed clauses exceeds the matched unchanged-clause placebo baseline by ≥10 percentage points (paired two-proportion / McNemar test, Holm-corrected across clause-deltas, α=0.05)." |
| `rq_window_width` | `sp_censored_window` | "The interval-censored median divergence-window width exceeds the sweep-cadence resolution floor by a factor ≥2 (windows are multi-sweep durations, not single-sweep blips), with the estimator's lower CI above the floor." |
| `rq_authority_downgrade` | `sp_authority_classification` | "Among authority-bearing changed clauses, a pre-registered floor (≥15%) of servers observed transitioning across the delta exhibit an enforced→advertise-only or enforced→silent downgrade coincident with the delta." |
| `rq_drift_attribution` | `sp_drift_attribution` | "Servers that fail changed-clause probes do not fail matched unchanged-clause probes at the same rate — the within-server changed-minus-unchanged failure gap is > 0 — so 'neither' is attributable to the version delta, not to generic non-conformance." |
| `rq_clause_type_structure` | `sp_authority_classification` | "Divergence windows and authority downgrades are non-uniformly distributed across clause-delta types — concentrated (≥2× enrichment, log-odds > 0 with a pre-registered minimum support) in added-MUST, strengthened-SHOULD→MUST, and retyped-authority deltas relative to representational deltas." |
| `rq_safe_probing_equivalence` | `sp_safe_authority_probing` | "The non-destructive protocol reproduces the full-interaction conformance verdict on ≥98% of reference-server clause deltas, and a harness-level assertion confirms zero state-mutating unauthorized calls are issued to any live third-party server." |

**critique:**
- summary: Tier accounting is clean (0 outcome-tier, correct for empirical), every
  RQ traces to a verbatim Stage-5 hypothesis, and the placebo/reference controls
  are properly framed as ground-truth not competitors. But one dataset choice
  imports a hidden dependency the plan doesn't acknowledge.
- comments:
  - `{severity: major, field: "datasets[A2A spec pair]", anti_pattern: "weak justification / hidden dependency", comment: "The A2A pair is justified as a protocol-independence check, but that only works if the *same* four-module apparatus (probe synthesis, safe probing, placebo, censored estimation) actually transfers — and A2A's transport and authorization model differ enough from MCP's that the authority-enforcement observable (accept/deny at the boundary) may not be witnessable the same way. As written, the A2A pair silently assumes cross-protocol portability of the instrument, which is itself an untested claim. Either (a) scope A2A to the modules that provably transfer (divergence-window existence + width, which need only the differential probe, not necessarily the authority-downgrade observable) and say so, or (b) add a portability check as an explicit precondition. Otherwise a reviewer reads the second protocol as decorative generality."}`
- decision: `move_to_refiner`.

### Refiner pass

- `datasets` A2A entry replaced: "A2A spec pair (1.0.0 → 1.0.1 extension) —
  *justification:* used to test **protocol-independence of the divergence-window
  phenomenon** (RQ2/RQ3 — existence and width), which require only the differential
  probe and placebo, both of which transfer directly. The **authority-downgrade**
  measurement (RQ4/RQ6) is reported for A2A only if a documented precondition holds
  — that A2A exposes an accept/deny authorization boundary a non-destructive probe
  can witness (checked on the A2A reference implementations before any live sweep);
  if it does not, the downgrade estimand is reported for MCP alone and the A2A
  result is scoped to divergence-window existence/width, stated as such rather than
  silently dropped." (This makes the cross-protocol dependency explicit and turns
  the second protocol from decorative generality into a scoped, honest check.)
- `changes_made`: gave the A2A pair a portability-precondition instead of an
  unstated cross-protocol assumption.
- `declined_to_fix`: none.

**Confirmed Stage 6.**

---

## Cross-stage consistency check (final pass, all six stages)

Literal recount, per the task's requirement:

1. **No method leak** in stages 1/2/4 — checked: `summary`/`objective`/
   `why_it_is_a_problem`/`technical_challenge` name no technique (probe synthesis,
   survival estimation, etc. first appear only in Stage 5). ✓
2. **ID stability** — no id renamed mid-run; `sp_*` / `m_*` / `rq_*` stable
   stage-to-stage. ✓
3. **Reference integrity** — every Stage-4 `source_limitation_ids` is `["__novel__"]`
   (all five sub-problems are decisive novel components grounded in, but not solved
   by, the cited neighbors — legitimate `__novel__` per stages.md's sentinel rule);
   every Stage-5 `target_sub_problem_id` ∈ Stage-4 sub-problems
   (probe→faithfulness, safe→safe_authority_probing, placebo→drift_attribution,
   authority→authority_classification, estimator→censored_window) ✓; every Stage-6
   `target_hypotheses` is a **verbatim** match to a Stage-5 hypothesis ✓.
4. **Hypothesis ↔ RQ recount (literal):**
   - Stage 5 hypotheses: H1 (probe), H7 (safe), H2 (placebo-existence),
     H5 (placebo-attribution), H4 (authority-downgrade), H6 (authority-type),
     H3 (estimator) = **7 hypotheses**.
   - Stage 6 RQs: rq_probe_discrimination (H1), rq_safe_probing_equivalence (H7),
     rq_window_existence (H2), rq_drift_attribution (H5), rq_authority_downgrade
     (H4), rq_clause_type_structure (H6), rq_window_width (H3) = **7 RQs**.
   - **7 hypotheses ↔ 7 RQs, bijective. No orphan hypothesis, no orphan RQ.** ✓
5. **Output coverage** — Stage 1's four outputs each reachable: (1) per-(server,
   clause, time) verdict ← probe synthesis + safe probing; (2) divergence window
   ← placebo/persistence; (3) enforcement-status/downgrade ← authority classifier;
   (4) prevalence + width distribution ← placebo (prevalence) + censored estimator
   (width). Nothing promised in Stage 1 falls off the chain by Stage 6. ✓
6. **`study_type` consistency** — `empirical` throughout; Stage 6 emits **0
   outcome-tier RQs**, as required (empirical/theory forbid outcome-tier). ✓

**Tier-gating verification (task requirement):** study_type = empirical → zero
outcome-tier RQs required and present. All 7 RQs are mechanism-tier (instrument
validity: RQ1, RQ7; existence/prevalence/attribution: RQ2, RQ4, RQ5;
characterization: RQ3; mechanism-layer structure: RQ6). No RQ is framed as
beats-a-baseline. **Gate satisfied.**

**What was hardest:** the recurring tension was **scope discipline on the
security half** — the seed's sharp "authority silently degrades to visibility"
claim is exactly the kind of statement that is easy to *assert* and hard to
*witness on the wire without causing harm*. Two genuine majors (Stage 3's
unhandled-threat repositioning against Capability-Gates/HCP, and Stage 4's
missing safe-authority-probing sub-problem) both trace to that single pressure
point, and both were resolved by *narrowing* the claim to what a non-destructive
wire probe can actually observe (an accept/deny transition on a reference-validated
probe), rather than by inflating it.

**Total rounds:** 6 stages × 1 critic round + 1 refiner pass = 6 critic rounds,
6 refiner passes. No stage hit the round cap; no cross-stage backup was required.
Every stage carried a genuine, evidence-grounded flag (Stage 1: reference-frame
evaluability gap [major] + presupposed-direction [minor]; Stage 2:
partial_output_coverage on window *duration* [major]; Stage 3: unhandled_threat
repositioning [major] + baseline-role [minor]; Stage 4: undercoverage /
safe-authority-probing [major] + overlap [minor]; Stage 5: two-hypotheses-one-
method justification [minor]; Stage 6: hidden cross-protocol dependency [major]).
