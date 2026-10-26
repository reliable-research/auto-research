# Green Tests Are Not Acceptance: A Staged Cross-Layer Comparison of Acceptance Oracles for Coding-Agent Patches

## Abstract

Coding agents increasingly produce patches that pass repository tests yet remain unacceptable to the projects that receive them. Existing work has measured single layers of this problem in isolation: test overfitting and lucky passes within benchmarks, design-constraint violations on benchmark-aligned issues, merge and rejection dynamics of agent pull requests, and post-merge survival. What no prior study provides is a comparison of the competing *acceptance oracles themselves* — pre-review test-pass, raw merge, and review-adjusted acceptance — for agreement and for held-out predictive fidelity against independently validated field outcomes on platform logs. We present a staged measurement framework that delivers exactly this comparison. A hash-locked enrollment register and label vault fix the sampling frame before any outcome is opened; a frozen Specification-Obligation Checker (SOC) scores source-explicit design obligations that green tests do not exercise; a backward-confirmed field-defect (BCFD) procedure validates post-merge defect labels against organizational confounding; and a review-adjusted oracle — merged ∧ substantively reviewed ∧ survives a construction window — is compared with test-pass and raw merge on temporally disjoint rejection and defect outcomes. The design is explicitly staged: a Stage-0 primary-source verification gate and three pilot gates (checker bake-off, field feasibility probe, adjudication dry-run) precede a core study whose human-adjudication budget is fixed at approximately 350 blinded items; the full 24-question, multi-panel program is preserved as a preregistered extension, not the build plan. A falsification set (F1–F5), including the explicit condition under which "green tests effectively are acceptance" and the stance dies, is encoded in the gating engine. The intended output is a field-validated answer to which acceptance layer should serve as the reward and evaluation substrate for coding agents.

## 1 Introduction

Autonomous coding agents translate issue descriptions into repository-scale patches, run continuous integration (CI), and open pull requests (PRs) with limited human intervention. As agents get better at satisfying visible tests, a green CI result carries less information about whether a patch respects omitted cases, compatibility commitments, architectural constraints, or repository-specific expectations. The field nonetheless operationalizes "solved" as "tests pass": benchmark resolved-rates, verifiable-reward RL on test outcomes, and auto-merge-on-green deployment gates all hard-code the proxy.

The diagnosis that verifiers are imperfect proxies is no longer novel, and we do not claim it. The *Verification Horizon* argument [8] holds that verifiers and agents co-evolve with no static verifier as a silver bullet, and that "users are the most faithful verifiers" — but it supplies an argument, not measurements, and it cannot say whether review-conditioned acceptance actually outpredicts strengthened test suites. On the lab side, the gap itself has been measured: green-but-design-violating patches are already documented at scale on SWE-bench-aligned issues, where fewer than half of "resolved" issues satisfy validated design constraints and correctness is approximately independent of design satisfaction [9]; ReactBench and its React-Doctor verifier ship a public green-but-fails-static-verifier instrument for React repositories [10]; UTBoost exposes ~31% lucky passes under strengthened suites [6]; and 80.2% of agent-PR test files carry weak or no oracle signal [7]. On the field side, mining studies describe merge, rejection, and review behavior of agent PRs [12, 13, 14, 21], merge outcomes are predictable at AUC 0.96 [19], and post-merge survival has been traced [15, 16].

Each of these results measures one layer in isolation. None of them answers the question that determines what agents should be trained and evaluated against: **when the layers disagree, which acceptance signal — pre-review test-pass, raw merge, or review-adjusted acceptance — most faithfully tracks validated downstream outcomes on real platform logs?** That cross-layer oracle-fidelity comparison, field-validated against independently verified defect and rejection outcomes, is this paper's contribution, together with the prescription it licenses: which layer to use as the reward substrate. We explicitly do not claim the first measurement of green-but-unacceptable patches — that lab-arm finding belongs to [9] and [10]; our prevalence estimate is the *field-validated, design-weighted* counterpart, and it is one input to the oracle comparison, not the headline.

Three measurement obstacles make the comparison hard. First, acceptance is unobserved when any checker is constructed, so a checker tuned against maintainer outcomes contaminates its own validation. Second, post-merge reverts, modifications, and defect reports may reflect organizational causes (refactors, ownership changes, dependency updates) rather than patch defects, so raw telemetry cannot serve as ground truth. Third, substantive review is latent at corpus scale: raw merge conflates careful evaluation with rubber-stamping, and raw rejection conflates technical objections with project constraints — 35.7% of agent-PR rejections are non-agentic in cause [13], and 28.3% of agentic PRs merge immediately with zero review [21]. The framework addresses these with, respectively, a frozen and manifest-locked checker, a quarantined defect-label validation procedure, and a review-adjusted oracle whose review conjunct is calibrated against blinded human adjudication and whose survival conjunct is temporally disjoint from held-out outcomes.

A previous version of this design inflated silently from its planned core into a 15,000–20,000-item adjudication program. This version restores the staged discipline: a Stage-0 primary-source verification gate and pilot gates G1–G3 run first; the core study (RQ8 and RQ19–RQ24, at a fixed ~350-item human-adjudication budget, single BCFD reference arm with partial-identification bounds) is the minimum publishable unit; the full multi-panel program is preserved as a clearly marked preregistered extension. A falsification set F1–F5 — including the condition under which the stance itself is dead — is encoded in the gating engine, so the design can lose.

## 2 Contributions

1. **A cross-layer oracle-fidelity comparison, field-validated on platform logs.** We compare pre-review test-pass, raw merge, and review-adjusted acceptance for agreement, directional discordance, and held-out predictive fidelity against (i) technical-only maintainer rejection and (ii) a validated post-merge defect label — the comparison that single-layer prior work [6, 7, 9, 10, 12–16, 19, 21] cannot perform, and the data that the Verification Horizon argument [8] needs but does not have.
2. **A review-adjusted acceptance oracle with a leakage-safe survival conjunct.** O_review = merged ∧ substantively reviewed (audit-anchored, threshold-locked) ∧ survives a construction window disjoint from all held-out outcomes — and a prescription for its use as the terminal reward substrate, with tests retained as shaping signal.
3. **Field-validated, design-weighted green-but-unacceptable prevalence.** A probability-sampled, blinded human audit of all-green agent PRs, scoped by a frozen obligation charter (SOC), yielding the field counterpart of the lab-arm findings of [9, 10] — conceding their priority on the lab measurement and claiming the field estimand, the transport machinery, and the validation chain.
4. **A staged, falsifiable verification protocol.** Stage-0 source verification, pilot gates G1–G3 with pre-specified degraded modes, a locked register and label vault, a single-arm BCFD validation with partial-identification bounds, and an encoded falsification set F1–F5 with an explicit kill condition and a publishable-negative branch.

## 3 Formal Problem Definition

Let the laboratory dataset be
\[
\mathcal{D}_{L}=\{(x_i,p_i,T_i,C_i)\}_{i=1}^{n_L},
\]
where \(x_i\) describes a real-repository task, \(p_i\) the agent-generated patch, \(T_i\in\{0,1\}\) whether the repository test suite passes, and \(C_i\in\{0,1\}\) whether the design/obligation checker flags the patch. Let \(\phi(x_i,p_i)\in\mathbb{R}^d\) denote task and patch features. A run is *green but unacceptable under the checker proxy* when \(U_i=T_iC_i=1\), and the conditional rate is \(\rho_L=\Pr(C=1\mid T=1)\).

Let the field dataset be
\[
\mathcal{D}_{F}=\{(z_j,M_j,R_j,S_j^{(c)},Y_j)\}_{j=1}^{n_F},
\]
where \(z_j\) contains observable task, patch, repository, and PR attributes; \(M_j\in\{0,1\}\) denotes merge by the day-30 landmark; \(R_j\in\{0,1\}\) denotes substantive, non-rubber-stamp review; \(S_j^{(c)}\in\{0,1\}\) denotes survival through a prespecified *construction window* (no revert and no defect-linked modification touching the patch between merge and day 30); and \(Y_j\) denotes held-out post-merge outcomes measured over days 31–180 — survival, reversion, and validated defect reports. For unmerged PRs, post-merge variables are undefined, never imputed as adverse.

Three acceptance layers are compared wherever their variables are observable:
\[
O^{\mathrm{test}}_j = T_j,\qquad
O^{\mathrm{merge}}_j = M_j,\qquad
O^{\mathrm{review}}_j = M_j\, R_j\, S^{(c)}_j .
\]
O^review accepts a patch only when it is merged, substantively reviewed, **and** survives the construction window. This definition is used *both* formally and operationally: the operational encoding is `review_adjusted_acceptance = raw_merge(day30) ∧ (review_signal ≥ τ*) ∧ S_c`, where τ* is the audit-locked review threshold (§7.2) and `S_c` is computed from platform events inside the construction window only. The construction-window conjunct \(S^{(c)}\) is disjoint by design from the held-out outcome window (days 31–180), preventing outcome leakage. (An earlier draft dropped \(S^{(c)}\) from the operational definition; this version reconciles the two.)

The study's three outputs are:

1. **Prevalence.** The design-weighted field prevalence \(\Pr(\text{adjudicated charter-scoped violation}\mid T=1)\), estimated from a blinded probability-sampled audit, with checker-corrected prevalence as a scalable secondary estimate.
2. **Prediction (extension).** \(f(\phi(x,p))\approx\Pr(U=1\mid T=1,\phi)\) with feature families residualized against surface covariates.
3. **Oracle comparison (primary).** For each pair \(O^a,O^b\): agreement \(A_{ab}=\Pr(O^a=O^b)\) and directional discordance \(D_{a\to b}=\Pr(O^a=1,O^b=0)\); and for each layer, held-out predictive fidelity
\[
F_a=-\mathbb{E}[\ell(Y, g_a(O^a,z))]
\]
under a prespecified proper loss on temporally disjoint data. The principal estimand is the joint characterization \((\{A_{ab},D_{a\to b}\},\{F_a\})\): where the layers agree, where they diverge, and which layer most faithfully predicts independent field outcomes. Neither \(O^{\mathrm{test}}\) nor \(O^{\mathrm{merge}}\) is designated ground truth.

## 4 Challenges

\(U\) is observed only through \(C\), whose validity cannot be presumed; establishing that \(C\) predicts \(Y\) needs a bridge sample despite initially separate lab and field populations. Lab-to-field distribution shift can invalidate transported estimates without explicit common-support and conditional-stability checks. The layers encode distinct error sources: \(O^{\mathrm{test}}\) omits properties tests do not exercise; \(O^{\mathrm{merge}}\) mixes technical acceptability with capacity, priority, and fit; \(O^{\mathrm{review}}\) depends on separating substantive review from rubber-stamping and on keeping \(S^{(c)}\) disjoint from \(Y\). Agreement statistics are sensitive to marginal prevalence and to the fact that post-merge outcomes are undefined when \(M=0\); comparing \(F_a\) therefore requires aligned populations, leakage-free windows, and explicit selection handling — otherwise apparent fidelity differences reflect observability, not measurement quality.

## 5 Staged Verification Protocol and Pilot Gates

The study is staged so that no expensive stage runs before its cheap gate passes, and no gate failure is silent. Each gate has a pre-specified degraded mode.

**Stage-0 — primary-source verification gate (hard blocker).** Every channel-relayed motivating figure is verified against its primary document before entering the draft: locate the source; confirm number, denominator, and cohort as we would state them; extract the source's own limitations into our threats section. Figures that fail are dropped, not hedged. The verified fallback set ([6], [7], [13], [21]) is sufficient to motivate the study alone. For public instruments (ReactBench [10], the design-compliance corpus of [9]) Stage-0 additionally performs a novelty-delta audit whose answers fix the related-work wording and reusable components.

**G1 — checker bake-off (20 patches × 5 repos).** All mechanized layers — off-the-shelf deep static analysis (CodeQL/Semgrep at maximum depth), strengthened suites where available (UTBoost-style [6]), and the SOC obligation checker (§7.1) — run on a 20-patch pilot. SOC must produce adjudication-agreeing verdicts on the pilot, or the design layer is scoped to the repository subset where it runs (reported as such, not silently degraded to linters). *Adjudication cost: 20 items.*

**G2 — field feasibility probe (200 PRs, 50 hand-audited).** Two hundred candidate agent PRs are pulled with the identification heuristics of the AIDev-line corpora [12, 13]; identification precision is measured by hand-audit of 50, and review-metadata richness is counted. If fewer than 60% of PRs carry metadata sufficient for a graded review-depth signal, the review conjunct collapses to the binary zero-review split — the crudest adjustment, which the dominance claim (F3) is designed to survive on. G2 also measures recoverability of immutable earliest-head CI status after force-pushes; if coverage is inadequate, the test layer carries inverse-probability-of-observation weights and pass/fail bounding as pre-specified. *Adjudication cost: 50 light identification audits (not full patch adjudications).*

**G3 — adjudication dry-run (30 patches, κ ≥ 0.6).** The adjudication rubric is drafted from the rejection-cause taxonomy of [13]; two raters calibrate on 30 patches; inter-rater κ ≥ 0.6 is required before the main panel opens. Failure loops the rubric, not the panel. *Adjudication cost: 30 items.*

**Core study (minimum publishable unit).** RQ8 (field prevalence) and RQ19–RQ24 (review measurement and the cross-layer oracle comparison), at core sample sizes: a ~300-patch stratified blinded audit panel (two raters + tiebreak; each patch coded for charter-scoped violation, review substance, and acceptability), machine-scale telemetry cohorts, and a **single** BCFD reference arm with partial-identification bounds (§7.3). Total human-adjudication budget: **20 (G1) + 30 (G3) + ~300 (panel) ≈ 350 blinded items**, plus 50 light G2 audits.

**Extension program (preregistered, clearly marked; not the build plan).** The full 24-RQ design — extraction-validation panels (RQ1–2), lab discrimination and transport bridge at 1,200/1,000/1,500 scale (RQ3–4, RQ7, RQ9), behavioral association and predictor program (RQ5–6, RQ11–14), and dual-arm quarantined BCFD validation with replay bank (RQ15–18) — totaling 15,000–20,000 adjudication items across ≥8 sequestered panels, is retained as the preregistered ideal for a follow-up registered report. Core results never depend on extension stages.

## 6 Method Overview

The framework ingests PR artifacts captured at first green CI — issues, failure traces, repository policies, patches, test outcomes, review records, dispositions, post-merge signals — under a hash-locked master register whose LabelVault refuses outcome labels until the corresponding instruments are frozen. It produces: a charter-scoped field prevalence of green-but-unacceptable patches; a validated post-merge defect label; and the cross-layer comparison of test-pass, raw merge, and review-adjusted acceptance against field outcomes, feeding a gating engine that assigns each claim a status in {confirmatory, descriptive, reference-limited, org-confounding-unverified} and evaluates the falsification set F1–F5.

![Figure 1: Staged architecture of the acceptance-oracle study](architecture.svg)

*Figure 1: Overview of the staged measurement architecture. Agent PRs enter through a hash-locked register at first green CI and are scored by three acceptance layers — the test suite (earliest-head, pre-review), the frozen SOC design checker, and the review-adjusted oracle O_review = merged ∧ substantively reviewed ∧ survives the construction window. Layer verdicts meet field merge outcomes and the BCFD-validated defect label in a cross-layer fidelity comparison anchored by a ~350-item blinded human audit; the gating engine evaluates falsification predicates F1–F5 and emits the reward-substrate prescription. Pilot gates Stage-0 and G1–G3 (top band) must pass before the stage they mark is allowed to run.*

Design separations prevent circular validation: checker construction, human adjudication, maintainer behavior, and post-merge verification are mutually sequestered; measurement gates restrict only the claims that depend on the affected instrument.

## 7 Methodology

### 7.1 Specification-Obligation Checker (SOC)

Passing CI certifies only the behaviors the executed tests exercise and assert. SOC measures the remaining source-explicit obligation space: it compiles explicit issue, trace, and repository-policy statements into span-grounded atomic obligations and evaluates them by executable or static checks, separating extraction fidelity, construct coverage, evaluator accuracy, field transport, and behavioral association so that evidence for one property cannot substitute for another.

A preregistered *coverage charter* defines scope by semantic acceptance relevance and source explicitness: required/prohibited behavior, preservation and regression constraints, API and compatibility commitments, design contracts and invariants, scope boundaries, supported configurations. Claims whose evaluation needs unavailable environments produce evaluator *abstentions* rather than disappearing from the construct. The charter publishes a frozen *coverage manifest* of obligation types; only manifest types contribute to the primary violation score, and extra-charter extractions flow to a separate stream. Locking the manifest before implementation makes the field-scored population type-identical to the human-adjudicated population.

Each obligation record carries type, governed artifact, required predicate, triggering condition, configuration, exact provenance span, and evaluation mode; every substantive field must be grounded in a cited span, and unresolved entities generate explicit abstentions. Executable obligations are evaluated by generated tests that must demonstrate prescribed parent behavior; non-executable obligations by AST- and diff-based rules. The violation threshold is selected on blinded laboratory labels and locked before any field label opens.

In the **core**, SOC is exercised at G1 bake-off scale and then run frozen over the field cohort as a *descriptive third layer* alongside the audit: the core's prevalence estimand (RQ8) rests on the blinded human audit, not on SOC passing performance gates. The full extraction-validation program (240 held-out source packages, ~1,200 claims, dual annotation; RQ1–2), the 1,200-patch lab discrimination corpus (RQ3), the 1,000-PR transport bridge (RQ4), the 1,500-PR checker-validity audit (RQ7), and g-computation misclassification correction (RQ9) are **extension** stages.

### 7.2 Review-Adjusted Acceptance Layer

Substantive review is manually codable but latent at corpus scale, and raw merge conflates evaluation with rubber-stamping. The core builds the review conjunct in three steps. (i) A rubric — issue-specific reasoning, a requested change, or a nontrivial human edit — is calibrated at G3 (κ ≥ 0.6). (ii) The ~300-patch audit panel dual-codes review substance on the full pre-merge record, blinded to CI status, dispositions, and outcomes; this audit is the sole evidence base for rubber-stamp prevalence claims (RQ21). (iii) A graded review-depth signal (reviewer count, comment depth, review latency, edit requests — G2-verified availability) is anchored to the audited labels; the operating threshold τ* is fixed at the lowest value whose one-sided 95% bounds meet PPV ≥ 0.90 and sensitivity ≥ 0.60 on an audit split disjoint by repository and time, then locked before merge, rejection, or defect outcomes are opened. If no threshold qualifies, thresholded acceptance is reported as descriptive sensitivity curves; if G2's depth-grid check fails, the conjunct degrades to the pre-specified binary zero-review split. The full 2,400-thread dual-coded classifier program (embedding-based, cross-fitted; RQ19 at scale) is an **extension** instrument; the core RQ19 instantiation is the audit-anchored proxy above.

The operational oracle is
`review_adjusted_acceptance = raw_merge(day30) ∧ (review_signal ≥ τ*) ∧ S_c`,
with `S_c` = no revert and no defect-linked modification touching patch lines between merge and day 30 — matching the formal O^review = M·R·S^(c) exactly. Pre-review test-pass is taken from the earliest completed required run on the initially submitted head; runs authored after the first human review event never replace it (anti-leakage), and missing initial-head statuses are bounded by assigning pass and fail alternately.

### 7.3 Backward-Confirmed Field-Defect Label (BCFD) — single-arm core

Post-merge telemetry does not reveal *why* a patch was reverted or modified; treating raw telemetry as a defect label contaminates every downstream comparison. The BCFD label separates discovery from verification. Discovery adjudicators compose candidate defect labels from reverts, linked defect reports, and overlapping modifications under a preregistered semantic-linkage rubric. In the **core**, a single evidence-quarantined reference arm — receiving only immutable pre-merge artifacts, never discovery allegations — verifies a stratified subsample of discovery-positive and discovery-negative merged PRs from the audited panel, with organizational-control frames (broad refactors, dependency updates, ownership transfers) sampled as designed false-positive probes. Unresolved cases are never coded defect-free: they widen partial-identification bounds, and all downstream fidelity comparisons (RQ22–23) are reported across the resulting misclassification region. Core BCFD claims are correspondingly bounded, not point-identified. The dual-arm design with independent executable and static arms, telemetry-independent sensitivity samples, and the 600-case blinded historical replay bank (RQ15–18) is deferred to the **extension**, where it upgrades the bounds to validated point estimates.

### 7.4 Green-Unacceptability Predictors (extension)

The dual-target predictor program — survey-weighted hierarchical group-lasso on adjudicated obligation violations, and discrete-time competing-risk models on technical-only rejection, with candidate families (requirement ambiguity, dependency breadth, complexity delta, test-to-code ratio) residualized against surface covariates and 1,000-bootstrap stability selection (RQ11–14) — is retained as designed but scheduled entirely in the extension: it reuses core labels and features and adds none of its own gates to the core.

### 7.5 Gating Engine and Falsification Set

Every RQ carries a machine-checkable pass predicate, and label-validity clauses assign each downstream claim a status in {confirmatory, descriptive, reference-limited, org-confounding-unverified}. On top of the per-RQ gates, the engine encodes the study-level falsification set:

- **F1 (gap ignorable).** Adjudication-calibrated green-but-unacceptable rate < 5% on *every* measured layer (RQ8 upper bounds). The gap is ignorable.
- **F2 (layers redundant).** Every deeper layer agrees with the test layer at κ > 0.8 (RQ20). Layered acceptance adds nothing over strengthened suites; UTBoost's rung [6] is the top of the ladder.
- **F3 (oracle dominance fails).** The *crudest* review adjustment (binary zero-review split, S_c at w=30) fails to beat both raw merge and pre-review test-pass on held-out fidelity (RQ22 with RQ23 bounds). **Publishable-negative branch:** F3-with-gap-confirmed is reported as "review adjustment does not rescue merge signals; the humans-are-not-reward-models caveat holds empirically," reframed around the layer-disagreement instrument — same venues, honest inversion.
- **F4 (gap unpredictable — extension).** Best in-track predictor AUROC < 0.65, or lab-to-field transfer AUROC < 0.60: the bridge fails; per-track results remain reportable, headline demoted.
- **F5 (maturity wins — extension).** Layered gap rates fall proportionally with green-rate gains across model tiers and reasoning budgets: the maturity hypothesis beats the structural stance.

**Kill condition (encoded, not implied):** F1 ∧ F2 ⇒ green tests effectively *are* acceptance once suites are strengthened; the stance, the oracle, and the paper are dead; the pipeline is retired into suite-strengthening tooling. Any two of {gap ≥ 15% on ≥ 1 layer, κ < 0.8 disagreement, crudest-adjustment dominance} carry the paper; all three carry the strongest version.

## 8 Experiments

### 8.1 Setup (core scale)

All analyses use one master sampling frame: an enrollment-time enumeration of public repositories from one preregistered forge ecosystem, eligible if actively maintained, configured with required-status-check CI, open to external contributions, and containing ≥ 1 agent-authored PR (identification heuristics G2-audited). Before any outcome label opens, the hash-locked master register records eligibility, sampling probabilities, cohort membership and nesting, sequestration assignments, weights, agent framework/model versions, and all thresholds; the LabelVault refuses outcome labels until the corresponding instrument freezes.

Core datasets: **(D-core-1)** first-green-CI inception cohort, machine-enrolled at platform scale (~6,000 PRs of telemetry; telemetry is cheap — human labels are the constrained resource); **(D-core-2)** the ~300-PR stratified blinded audit panel drawn from the all-green stratum (violation, review-substance, and acceptability codes; two raters + tiebreak); **(D-core-3)** the expanded layer cohort with immutable earliest-head CI status, day-30 dispositions, construction-window events, and day-31–180 follow-up (machine telemetry, ~12,000 PRs); **(D-core-4)** the BCFD core verification subsample (single arm, organizational-control frames, partial-ID bounds); **(D-core-5)** the review-activity cohort (~8,000 PRs, telemetry + audit-anchored review signal) for RQ24. Baselines: pre-review test-pass, raw merge, approval-count and change-request rules, raw post-merge telemetry, and a repository-time-surface predictor; the PatchDiff-only and transported diff-and-surface comparators join in the extension.

The core research questions (numbering retained from the preregistered full design):

- **RQ8:** What is the design-weighted prevalence of independently adjudicated green-but-unacceptable PRs in the field?
- **RQ19:** Can substantive review be measured reproducibly with a transportable high-PPV threshold (core: audit-anchored signal; extension: classifier at scale)?
- **RQ20:** Where do pre-review test-pass, raw merge, and review-adjusted acceptance disagree, after prevalence guards?
- **RQ21:** How often does raw merge occur without independently adjudicated substantive review?
- **RQ22:** Does review-adjusted acceptance predict held-out post-merge outcomes better than earlier layers?
- **RQ23:** Is the fidelity ordering robust to bounded selection bias?
- **RQ24:** Does an upstream, text-separated review signal predict later technical rejection better than pre-review test-pass?

### 8.2 RQ8 — Green-but-Unacceptable Prevalence (core)

The ~300-PR audit panel provides dual-adjudicated, charter-scoped patch-level violation labels; inclusion and nonresponse weights recover the all-green field population at first green CI; no SOC-derived label enters the reference. Unresolved cases stay in partial-identification bounds. *Pass predicate:* estimated prevalence ≥ 0.10 with one-sided 95% lower bound > 0.05 (attainable at n ≈ 300 for the anticipated effect sizes; the design-weighted effective sample size is reported). The estimate generalizes to source-explicit charter-scoped obligations only — not to unwritten maintainer expectations. *Metrics:* design-weighted prevalence, SE, effective n, one-sided lower bound, per-stratum rates.

### 8.3 RQ19 — Substantive-Review Measurement (core instantiation)

The audit-anchored graded review signal is evaluated against held-out audited threads (repository- and time-disjoint splits within the panel), with approval-count and change-request rules as content-free baselines. *Pass predicate:* one-sided 95% lower bounds ≥ 0.90 PPV and ≥ 0.60 sensitivity at the locked τ*; advantage over the rule baselines; otherwise descriptive-only mode with sensitivity curves. *Metrics:* PPV, sensitivity, calibration, coder agreement (κ), baseline deltas.

### 8.4 RQ20 — Acceptance-Layer Disagreement (core)

On D-core-3, the joint distribution of earliest-head test-pass, day-30 raw merge, and review-adjusted acceptance is always reported in full. Weighted κ is confirmatory only when both design-weighted failure prevalences lie in [0.10, 0.90]; otherwise the two cell-conditional discordance proportions (test-green-but-unmerged; test-red-but-merged) are confirmatory. Because O^review is nested in merge, merge-vs-review agreement is descriptive. *Pass predicate:* κ ≤ 0.40 when applicable, else ≥ 1 conditional discordance ≥ 0.15 with lower bound > 0.10; review-adjusted failure among test-green PRs ≥ 0.15. F2 evaluates on this RQ's outputs.

### 8.5 RQ21 — Merge Without Substantive Review (core)

Within the merged stratum of the audit panel, the design-weighted prevalence of adjudicated rubric-negative reviews estimates rubber-stamp merging; below-threshold signal values never count as evidence without audit confirmation. *Pass predicate:* one-sided 95% lower bound ≥ 0.10. *Metrics:* audited prevalence, bound, effective n, κ, signal–audit cross-tabulation.

### 8.6 RQ22 — Predictive Fidelity of Acceptance Layers (core primary)

Cross-fitted calibrated Brier scores and time-dependent discrimination are estimated on D-core-3 with day-31–180 follow-up under doubly robust merge and censoring weights, common-support restrictions, and the BCFD partial-ID region from the single-arm validation. Within merged follow-up, review-adjusted acceptance is compared with pre-review test-pass (raw merge is constant there); at parent-cohort level, review-adjusted acceptance is compared with raw merge on the point-identified composite "merged and BCFD-positive" (unmerged PRs negative for the composite by definition, not by imputation). *Pass predicate:* review-adjusted acceptance reduces Brier by ≥ 10% against pre-review test-pass and, when identifiable, against raw merge — persisting across the BCFD misclassification region. The dominance test is additionally run at the *crudest* adjustment (binary zero-review, w = 30): this is the F3 predicate.

### 8.7 RQ23 — Robustness to Selection (core)

All admissible selection models with an unmeasured-selection odds-ratio bound of 2 are enumerated; the minimum review-adjusted improvement is retained. *Pass predicate:* worst-case improvement remains positive. If parent-cohort weighting is unidentifiable, the raw-merge comparison is reported as bounds only and excluded from confirmatory conclusions.

### 8.8 RQ24 — Upstream Review Signal vs Technical Rejection (core)

On D-core-5, at landmarks 24/48/72 h after first green CI, the graded review signal (computed only from comments strictly preceding rejection-constituting language, with the rejecting-maintainer leakage ablation) is compared with earliest-head test-pass by design-weighted time-dependent AUC on the disposition-open risk set. *Pass predicate:* tdAUC advantage ≥ 0.05 with paired lower bound > 0, persisting at earlier landmarks and under the leakage ablation.

### 8.9 Extension Program (preregistered; clearly marked — not the core build plan)

The remaining RQs run only after core freeze, as a follow-up registered report: RQ1–2 (extraction reliability and charter coverage on 240 held-out source packages), RQ3–4 (1,200-patch lab discrimination; 1,000-PR transport bridge), RQ5–7 (behavioral association and 1,500-PR checker-validity audit), RQ9 (g-computation prevalence agreement, ±0.05 equivalence), RQ10–14 (BCFD convergence and the dual-target predictor program), RQ15–18 (dual-arm quarantined BCFD validation, 600-case replay bank, organizational-control caps: unresolved mass ≤ 0.20, worst-case FP ≤ 0.10). Cumulative extension adjudication: 15,000–20,000 items across ≥ 8 sequestered panels — feasible only as a funded multi-team effort, which is why it is an extension. All extension thresholds, margins, and sensitivity regions are already locked in the register.

## 9 Related Work

### 9.1 The Named Foil: Argument Without Measurement

**Verification Horizon** [8] is the closest occupant of our cell on the reward side: it argues that verifiers and agents co-evolve, that no static verifier is a silver bullet, and that "users are the most faithful verifiers." We concede the diagnosis entirely — it is our premise, not our claim. What [8] does not contain is measurement: no acceptance-gap data, no oracle construction, and no way to answer whether review-conditioned acceptance actually outpredicts strengthened test suites on real logs. This paper supplies exactly the data that argument needs: the cross-layer agreement matrix and the layer-wise held-out fidelity comparison against validated field outcomes (RQ20, RQ22–24).

### 9.2 The Method Twin: Green-but-Design-Violating, Measured in the Lab

**"Does Pass Rate Tell the Whole Story?"** [9] validates 1,787 design constraints mined from real PRs across 495 issues aligned with SWE-bench-Verified/Pro and finds that fewer than half of "resolved" issues satisfy them, with correctness approximately independent of design satisfaction. **ReactBench / React-Doctor** [10] ships a public instrument — hidden fail-to-pass tests plus a 400-rule pinned static verifier over 50+ React repositories — demonstrating green-but-fails-verifier at scale. We concede both priorities: *the lab-arm finding that green tests admit design-violating patches is theirs, and we make no "first measurement" claim.* Our surviving deltas are operational: field prevalence under probability sampling with blinded human-audit validation and design weights (RQ8); the transport machinery that [9, 10] do not need because they never leave the benchmark; and the use of the violation layer as one input to a cross-layer *oracle* comparison, which neither performs.

### 9.3 Trace-Level Compliance Is a Different Estimand

**AgentLTL** [11] checks temporal-logic compliance of tool-using agents at the *trace* level — whether the agent's procedure obeys prescribed temporal structure. Our estimands are consistently *artifact- and acceptance-level*: properties of the resulting patch and of the project's acceptance behavior, regardless of the procedure that produced them. The two are complementary — a procedurally compliant trace can yield an unacceptable patch and vice versa — and we do not measure trace compliance.

### 9.4 Test-Based Evaluation of Generated Patches

SWE-bench [1] frames issue resolution as editing real repositories to satisfy tests; EvalPlus [2] strengthens functional evaluation by test augmentation; PatchDiff [3] exposes behavioral divergence between plausible and developer patches (7.8% / 29.6% divergence findings); Ahmed et al. [4] document test overfitting on SWE-bench; SpecBench [5] separates visible from held-out compositional tests to expose reward hacking; UTBoost [6] surfaces ~31% lucky passes via test-case augmentation; All Smoke, No Alarm [7] shows 80.2% of agent-PR test files carry weak or no oracle signal. Ye et al. [25] assess repair patches with generated random tests; Martinez & Franch [24] characterize the SWE-bench leaderboard ecosystem. This line strengthens or audits the *test* rung; it does not compare that rung with merge- or review-level acceptance against field outcomes — the rung-comparison is precisely what we add.

### 9.5 Field Studies of Agent PRs, Review, and Post-Merge Quality

AIDev [12] establishes the agent-PR corpus line; Peralta et al. [13] recover merge/rejection rationales (35.7% of rejections non-agentic in cause); Abujadallah et al. [14] build a rejection-cause taxonomy; zero-review analysis [21] finds 28.3% of agentic PRs merged immediately; "These Aren't the Reviews You're Looking For" [20] measures review quality; Mazloomzadeh et al. [22] and Watanabe et al. [17] characterize agent contribution patterns; Lenarduzzi et al. [23] relate code quality to PR acceptance for human PRs. On outcomes, Cynthia et al. [15] find post-merge quality issues via differential SonarQube; Rahman & Shihab [16] trace survival (agent code surviving *longer* in their cohort — a tension our design treats as an empirical question, not an embarrassment); ReDef [18] contributes revert-anchored defect labels, which our BCFD procedure extends by validating the label construction itself against organizational confounding. Merge prediction reaches AUC 0.96 on agentic PRs [19] — but predicts the *merge* layer without asking whether that layer tracks quality; our RQ12 (extension) sharpens the estimand to technical-only rejection under competing risks, and our core asks the question [19] leaves open: which layer deserves to be predicted. All of these measure single layers descriptively; none compares the layers as competing oracles against validated downstream outcomes.

## 10 Threats to Validity

**Construct:** "acceptance" changes referent across layers by design; every result is labeled by layer, and the lab/field constructs are bridged (extension) rather than conflated. Charter scope excludes unwritten maintainer expectations — stated as an unmeasured component. **Internal:** circularity is broken structurally (LabelVault, sequestration, audit-anchored review, quarantined BCFD, initial-head anti-leakage); the survival conjunct S^(c) is disjoint from the outcome window. **External:** one forge ecosystem; agent identification heuristics are lossy (G2 measures the loss); core BCFD claims are bounds, not points, until the extension's dual-arm validation. **Statistical:** n ≈ 300 audit items powers the core predicates but not fine strata; per-stratum results are descriptive.

## 11 Conclusion

Reliable assessment of coding-agent patches requires evidence beyond green tests and unadjusted merges — that argument is already on the record [8]; what has been missing is the measurement that adjudicates it. This staged design delivers the cross-layer comparison — test suite, design checker, review-adjusted acceptance with its survival conjunct — against validated field outcomes, at a core scale (one ~350-item adjudication budget, pilot-gated, falsification-encoded) that can actually be executed, with the full multi-panel program preserved as a preregistered extension. If the core predicates pass, the field gains a defensible acceptance signal and a concrete reward-substrate prescription: acceptance-grounded terminal rewards with tests as shaping. If F1 ∧ F2 holds instead, green tests effectively are acceptance once suites are strengthened, and we will say so. Either way, the question stops being argued and starts being measured.

## References

1. C. E. Jimenez, J. Yang, A. Wettig, S. Yao, K. Pei, O. Press, K. Narasimhan. *SWE-bench: Can Language Models Resolve Real-World GitHub Issues?* ICLR 2024. arXiv:2310.06770.
2. J. Liu, C. S. Xia, Y. Wang, L. Zhang. *Is Your Code Generated by ChatGPT Really Correct? Rigorous Evaluation of Large Language Models for Code Generation.* NeurIPS 2023 (EvalPlus).
3. Y. Wang, M. Pradel, Z. Liu. *Are "Solved Issues" in SWE-bench Really Solved Correctly? An Empirical Study.* ICSE 2026. arXiv:2503.15223 (PatchDiff).
4. T. Ahmed et al. *Investigating Test Overfitting on SWE-bench.* FSE 2026 (Ideas, Visions and Reflections). arXiv:2511.16858.
5. B. Zhao et al. *SpecBench: Measuring Reward Hacking in Long-Horizon Coding Agents.* arXiv:2605.21384.
6. *UTBoost: Rigorous Test-Case Augmentation for Coding-Agent Evaluation.* arXiv:2506.09289.
7. *All Smoke, No Alarm: Weak Oracle Signals in Agent-Authored Pull-Request Tests.* arXiv:2606.18168.
8. *The Verification Horizon: Verifiers, Agents, and the Limits of Static Checking.* arXiv:2606.26300.
9. *Does Pass Rate Tell the Whole Story? Evaluating Design Constraint Compliance in LLM-based Issue Resolution.* arXiv:2604.05955.
10. *ReactBench / React-Doctor.* Public benchmark and 400-rule pinned static verifier over 50+ React repositories (millionco); hidden fail-to-pass tests.
11. *AgentLTL: Temporal-Logic Compliance Checking for Tool-Using Agents.* arXiv:2607.02599.
12. H. Li et al. *The Rise of AI Teammates in Software Engineering (SE) 3.0: How Autonomous Coding Agents Are Reshaping Software Engineering* (AIDev dataset).
13. S. R. O. Peralta et al. *Why Are Agentic Pull Requests Merged or Rejected? An Empirical Study.* arXiv:2605.22534.
14. M. Abujadallah et al. *Understanding the Rejection of Fixes Generated by Agentic Pull Requests — Insights from the AIDev Dataset.* MSR 2026. arXiv:2606.13468.
15. S. T. Cynthia et al. *Beyond Bug Fixes: An Empirical Investigation of Post-Merge Code Quality Issues in Agent-Generated Pull Requests.* arXiv:2601.20109.
16. M. Rahman, E. Shihab. *Will It Survive? Deciphering the Fate of AI-Generated Code in Open Source.* arXiv:2601.16809.
17. Watanabe et al. *On the Use of Agentic Coding.* TOSEM. arXiv:2509.14745.
18. Nam et al. *ReDef: Do Code Language Models Truly Understand Code Changes for Just-in-Time Software Defect Prediction?* FSE 2026.
19. *Let's Make Every PR Meaningful: Predicting Agentic Pull-Request Merges.* arXiv:2601.18749.
20. *These Aren't the Reviews You're Looking For: Review Quality in Agent-Era Pull Requests.* arXiv:2605.02273.
21. *Immediate Merges of Agentic Pull Requests: A Zero-Review Analysis.* arXiv:2601.00753.
22. Mazloomzadeh et al. *How Do AI Coding Agents Contribute to Software Development?*
23. V. Lenarduzzi et al. *Does Code Quality Affect Pull Request Acceptance? An Empirical Study.*
24. Martinez, Franch. *What's in a Benchmark? The Case of SWE-Bench in Automated Program Repair.*
25. Ye et al. *Automated Patch Assessment for Program Repair at Scale.*
