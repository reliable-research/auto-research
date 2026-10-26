# Research Taste Audit — B8.1

> Skill: `research-taste-auditor` (Chen, Zhao & Cohan, arXiv:2607.01233). Run once
> on the core idea (Motivation + Method) as confirmed at Stage 2 / Stage 5 of the
> `auto-research-discussion` self-play run, **before** final paper assembly — per
> the skill's own guidance ("cheaper to catch before drafting than after"). The
> seed for this topic was a bare `README.md` (no `paper.md` self-audit preceded
> this), so the audit runs cold against the stage outputs, not against a prior
> asymmetry check.

## 1. Extracted idea

**Motivation** (Stage 2, confirmed): "Agent-interoperability protocols are being
adopted as the substrate for cross-vendor tool use and delegation, and they are
iterating monthly; yet whether the servers already deployed against them actually
track a spec across a revision — or fall into a window where they conform to
neither the old nor the new version — has never been measured on the wire. A
protocol revision is normally assumed to move the ecosystem cleanly from N to N+1;
if instead a measurable fraction of deployed servers sit in a divergence window,
every client negotiating with them interoperates against an unspecified behavior,
and — the sharp claim — authority constraints are the ones that degrade quietly: a
clause that in one version requires the server to *reject* an unauthorized call
can, mid-transition, degrade so the constraint is merely *advertised* while the
call still succeeds, a regression no single-version check and no static framework
audit catches because it exists only *between* versions and only on the wire."

**Method** (Stage 5, summary-level): "For each normative-clause delta between
adjacent spec versions we synthesize a matched wire-probe pair validated to
*discriminate* two pinned reference implementations before it may label any live
server 'neither'; we witness authority enforcement non-destructively by reading the
server's accept/deny decision at the authorization boundary rather than performing
the unauthorized action; we separate drift-induced divergence from generic
non-conformance with an unchanged-clause placebo plus a within-server
changed-minus-unchanged contrast; and we estimate window *width* with interval-
censored survival estimation over a fixed-cadence longitudinal sweep."

## 2. Taxonomy labels

**Opportunity Pattern:** primary **Evidence Gap** (secondary: **Failure / Risk
Gap**).
- rationale: the load-bearing clause is "has never been measured on the wire" /
  "no single-version check … catches" — a measurement/diagnosability absence, not
  a "two literatures never connected" framing. The secondary Failure/Risk reading
  is licensed by the authority-downgrade claim ("degrade so the constraint is
  merely advertised while the call still succeeds") — an existing safeguard
  (spec-conformance-as-safety-label) is unreliable across a transition.
- Explicitly **not** Bridge Opportunity: there is no "X and Y have developed in
  isolation, let us connect them" clause. The two conceptual inputs it *touches*
  (conformance testing; the visibility-vs-authority axis) are not being *bridged*
  — one is *extended* to a differential/longitudinal axis and the other is
  *operationalized* as a wire observable, with the nearest-neighbor sentence
  (Stage 3 major fix) explicitly conceding the concept to Capability-Gates/HCP and
  claiming only the measurement.

**Method Paradigm:** primary **Empirical Mapping** (secondary: **Formal
Derivation**).
- rationale: "synthesize probes … validated to discriminate references … estimate
  width with censored survival estimation" is measurement instrumentation, not
  "integrate/unify two methods." The secondary Formal Derivation reading comes
  from the two conceptual contributions that are decision-rules, not pipelines:
  the *divergence-window* estimand (a defined temporal object with a reference
  frame) and the *enforced/advertise-only/silent* three-way enforcement-status
  classification (a wire-observable operationalization of an axis previously left
  conceptual).

## 3. Diagnostics

- `surface_stitching` = **0** — not an "A + B" glue. The apparatus is purpose-built
  for one identifiability problem (does a deployed server conform to *neither*
  adjacent version, and does authority quietly stop being enforced). No pair of
  pre-existing methods is combined by a connecting verb; differential testing and
  survival analysis are *tools applied*, and the paper's novelty (matched
  reference-discrimination probes, non-destructive authority-boundary observation,
  changed-vs-unchanged placebo, interval-censored window) is new machinery between
  them, not the seam.
- `bottleneck_specificity` = **3** — the target is exact and nameable at every
  step: *which* object (a normative-clause delta), *which* verdict (N / N+1 / both
  / neither / out-of-frame relative to a defined version-bracket), *which*
  security transition (enforced → advertise-only / silent), *which* estimator
  (interval-censored survival with a stated resolution floor). Meets/exceeds the
  human baseline (2.56) and the strongest tested models (2.3–2.6).
- `boilerplate` = **1** — mostly load-bearing; the one soft clause is "adopted as
  the substrate for cross-vendor tool use and delegation," slightly generic
  adoption language, but it still ties to a specific claim (spec-conformance used
  as a *safety label*) rather than being swappable filler.

## 4. Dominant verb(s)

Method sentence's main verbs: **measure, synthesize/discriminate, witness,
separate, estimate**. `separate` is explicitly in the human-heavy cluster (with
*decouple, isolate, disentangle*); `measure`/`estimate` are neutral, task-specific
measurement verbs; `discriminate` (a probe *separating* two reference versions) is
a separation move. No instance of *integrate / unify / merge / adapt / combine /
leverage / bridge* appears in a claim position anywhere in the extracted idea — in
fact the one place a "bridge" reading could have crept in (relating conformance
testing to the authority axis) was actively *disarmed* by the Stage 3
concede-and-differentiate sentence.
Archetype family: **human-heavy / neutral**.

## 5. Verdict

| # | Condition | Fired? |
|---|---|---|
| 1 | Opportunity = Bridge Opportunity AND Method = Synthesis/Unification | **No** (Evidence Gap / Empirical Mapping) |
| 2 | surface_stitching ≥ 2, OR boilerplate ≥ 2, OR bottleneck_specificity ≤ 1 | **No** (0 / 1 / 3) |
| 3 | Dominant verb from the LLM-heavy archetype list | **No** (measure / discriminate / separate / estimate) |

**Verdict: 🟢 Reads as human-shaped.** No condition fires — a clean pass on all
three independent checks, not merely the absence of the worst-case flag.

## 6. Interpretation (honest, not a rubber stamp)

This is a genuine 🟢, and it is worth saying *why* it did not slip into the
Bridge+Synthesis cell, because the raw material had a real opportunity to. A
lazier framing of exactly this topic — "conformance testing and agent-protocol
governance have developed separately; we bridge them" — would have landed squarely
in the overrepresented LLM cell. The self-play run avoided it in two concrete
places that this audit can point at: (a) Stage 1 defined the estimand as a
*specific measured quantity* (the divergence window, with a version-bracket
reference frame and an out-of-frame category) rather than a connection between
fields; and (b) the Stage 3 critic's `unhandled_threat` major forced the authority
half to be written as *concede the concept (to Capability-Gates/HCP), claim the
measurement* — the exact reframe pattern `archetype-verbs.md` prescribes for
turning a latent bridge into an Evidence-Gap/Empirical-Mapping move. The verb audit
confirms it independently: the method's operative verbs are *measure / discriminate
/ separate / estimate*, none from the LLM-heavy list. No reframe is required; the
downstream `pengsida-stage-reviewer` and assembly can proceed on the confirmed
Stage 2 / Stage 5 idea as-is.
