# Discussion: B3.1 探针集的充分性设计 — What Probes Predict Breakage? Minimal Probe-Set Design for Version-Drift Auditing

> **Document type:** structured research discussion (auto-research-discussion style: 6 stages, each with an internal critic → refine pass).
> **Topic status from portfolio audit:** KEEP, **Tier-2 (support)**. Explicit audit note: B3.1's truth source — downstream breakage data (真值 = 同一输入集的跨版本输出差分) — is exactly the asset B3.4 must build anyway, and B3.3 must build the behavior-diff side. Therefore B3.1's **strongest form is MERGED with or FOLLOWING B3.3/B3.4** (the Tier-1 leads). This discussion is deliberately designed so that the probe-selection methodology is a **pluggable module** consumable by B3.3/B3.4's papers, with a standalone framing held as fallback.
> **Hard constraint (inherited from parent topic B3 跨版本行为漂移 / 纵向审计):** black-box / external-audit only. No weights, no gradients, no vendor cooperation; logprobs treated as optionally available at best, never required.

---

## Stage 1 — Problem Definition

**Setting.** A provider ships a version pair (v_old → v_new). An external auditor can query both versions (open-weight checkpoints, or dated API snapshots while both are still served) but sees only inputs and outputs. Downstream integrators have pipelines — prompt templates, parsers, JSON-schema contracts, tool-call fillers, moderation wrappers — tuned against v_old.

**Objects.**
- A **probe battery** P partitioned into five families F = {capability, refusal-boundary (拒答边界), format-preference, calibration, safety-behavior}, each family f with a drift instrument producing a per-pair drift score d_f(v_old, v_new).
- A **downstream breakage ground truth** B: for a suite of downstream tasks/contracts T, run the same input set through both versions and measure behavior change (the seed's 真值 = 同一输入集的跨版本输出差分). In the merged design, T *is* B3.4's simulated production-contract corpus (JSON schemas, format conventions, few-shot templates) and B is B3.4's contract-breakage rate.

**Core question (RQ1, from the seed):** which probe family's drift is most predictive of downstream breakage across version pairs?

**Design question (RQ2, from the title's "minimal probe-set design"):** what is the smallest probe subset — measured in query budget, not just family count — that retains most of the full battery's predictive power?

**Robustness question (RQ3):** is measured drift signal at all, i.e., does it exceed the within-version sampling-noise floor and stay stable under paraphrase of probe items?

**Critic:** Four holes. (1) "Breakage" is underdefined: a large surface diff can be functionally harmless and a one-character diff can kill a parser; if B is raw output-diff magnitude, the whole study measures the wrong construct. (2) "Predictive" is ambiguous between *in-sample correlation across observed pairs* and *out-of-sample prediction for a new, unseen version pair* — only the latter supports the deployment story ("run the cheap probes when v_new ships, decide whether to re-test"), and the two demand different evaluation protocols. (3) Minimality is stated at the family level in the seed, but a practical audit budget is denominated in queries; a "minimal family subset" of two families could still cost 1,000 items. (4) The problem statement doesn't say what the module *is* for B3.3/B3.4 — without an explicit interface, "pluggable" is a slogan.

**Refined:** (1) Define breakage **functionally, per contract class**: B(t, pair) = change in the rate at which task t's downstream check fails (schema-validation failure, parser exception, assertion failure, tool-call inexecutability, judged answer-equivalence break), not raw edit/semantic distance; raw diff magnitude is retained only as a secondary descriptive statistic. (2) Define the headline evaluation as **out-of-sample: leave-one-version-pair-out (LOPO) prediction** of B for the held-out pair from its probe drifts; in-sample correlation is reported only as an exploratory analysis. (3) Define minimality over **query budget b**: the minimal probe set is the cheapest subset S ⊆ P (items, not only families) whose LOPO predictive performance is within a pre-registered margin ε of the full battery; the deliverable includes the full budget–retention curve, not one point. (4) State the **module contract**: input = any (version pair, breakage ground truth) collection matching a declared schema — canonically B3.4's contract corpus, alternatively B3.3's category-resolved behavior diffs; output = (i) family-level predictive ranking, (ii) selected minimal probe set with budget, (iii) a calibrated breakage-risk score for future pairs. B3.1 = the *prediction/selection layer*; B3.3/B3.4 own the ground truth.

---

## Stage 2 — Motivation

Providers ship versions that silently change behavior; the canonical longitudinal audit (Chen, Zaharia & Zou, arXiv:2307.09009) documented large per-task swings across GPT-3.5/GPT-4 snapshots. Downstream teams face a bad trade: exhaustively re-validate every pipeline on every version bump (expensive, slow), or ship blind (risky). A minimal probe set that predicts breakage converts this into a cheap triage: run ~a few hundred probes once per new version; if the predictive families are quiet, skip the full re-test; if they fire, know *which kind* of re-test to run.

Within the B3 portfolio, the motivation is explicitly that of a **multiplier for the Tier-1 leads**: B3.4 measures *how much* breaks per upgrade and which contracts are fragile; B3.3 measures *how much of the change is undocumented*. Neither answers the forward-looking operational question — *what cheap signal should an auditor watch to anticipate breakage?* B3.1 turns B3.4's retrospective breakage rates into an early-warning instrument and gives B3.3's silent-change categories a severity weighting (silent changes on high-breakage-predictive axes matter more for accountability).

**Critic:** Two attacks. (1) The obvious rejoinder: if B3.4's contract suite exists and *is* the thing you care about, why probe at all — just run the contract suite on v_new. The motivation must quantify the gap: the probe battery must be materially cheaper than the downstream suite, and — more importantly — must generalize to downstream contracts the auditor has *not* enumerated (an integrator's private pipeline is not in anyone's suite). If the probe set only predicts the specific corpus it was selected on, it is a compressed test suite, not an audit instrument. (2) "Minimal test subset preserving fault detection" is a 30-year-old SE problem (regression test selection / test-suite minimization); the motivation cannot pretend the framing is new — the delta is the black-box, non-deterministic, axis-structured behavioral setting.

**Refined:** Motivation restated on three legs. (1) **Cost asymmetry, quantified up front**: target ≥10× query-cost reduction of the selected probe set vs the full downstream suite, reported as a headline number; if the ratio is under ~3×, the probe set has no practical reason to exist and the study reports that honestly. (2) **Generalization, not compression**: the value claim is prediction for *held-out contract classes and held-out version pairs*, evaluated as such (Stage 5's cross-axis prediction matrix); predicting only the training corpus is the null hypothesis, not the goal. (3) **Honest lineage**: framed as transposing regression-test-selection's minimality logic to a setting it cannot handle — no code access, no deterministic oracle, "coverage" over behavioral axes rather than code paths — with the SE literature credited, not ignored. The portfolio positioning stays: this is the layer that makes B3.3/B3.4's data actionable.

---

## Stage 3 — Related Work

**Adjacent published audits (the sweep's three anchors — all detection, not breakage prediction):**
- **arXiv:2504.04715 — model-substitution auditing** [VERIFY exact title/authors; per our sweep: detecting whether an API silently serves a different model than advertised]. Answers "are you getting the model you paid for?" — a *binary identity/detection* question between a claimed and served model. Boundary: no downstream-breakage target, no axis-resolved probes, no minimality analysis; B3.1 starts where detection ends (change is given; what breaks?).
- **arXiv:2512.03816 — logprob-based tracking of model updates** [VERIFY]. Tracks drift via logprob signatures. Boundary: requires logprob exposure, which many production APIs restrict or perturb; B3.1 is output-behavior-only by design, and its target variable is downstream functional breakage, not distributional change per se.
- **arXiv:2506.06975 — rank-based uniformity test for behavioral shift** [VERIFY]. A statistical test for *whether* a model behind an API has changed, with error guarantees. Boundary: a yes/no shift detector on a sample of prompts; it neither ranks behavioral axes by consequence nor predicts which integrations break. B3.1 uses this class of test as a *component* (drift-vs-noise gate, Stage 5) and builds the prediction layer above it. Related: Model Equality Testing via MMD (Gao et al., arXiv:2410.20247) [VERIFY].

**Longitudinal drift evidence:** Chen, Zaharia & Zou, "How Is ChatGPT's Behavior Changing over Time?" (arXiv:2307.09009) — the canonical drift audit; blended per-task deltas, single vendor, no probe-vs-breakage predictive link.

**Single-axis instruments and machinery (local OpenReview corpus, from digest N3):** EssenceBench [OpenReview:lZlZjSxdio] (benchmark compression — minimal item subsets preserving scores/rankings, but for score fidelity at one time, not cross-version breakage prediction); BiasSimilarity-BSM [OpenReview:EveruzAsGI] (black-box cross-model behavioral similarity, one construct, no breakage link); RefusalIndex [OpenReview:9gJBhkLRat] (rate-invariant refusal-boundary metric, single time point); OffTopicEval [OpenReview:EcIyiJrajc] (policy-conditioned accept/refuse probe); B-Calibration [OpenReview:0sCyk9Tr5J] (semantic calibration for free-form generation); TARE [OpenReview:YEBDvqsniH] (paraphrase brittleness — a warning for any single-phrasing drift score); ProSafePrune [OpenReview:QkHKaPfRAB] (over-refusal as a distinct drift-prone axis); WeightDiff [OpenReview:6As4wfTB77] (white-box update interpretation — motivates why external auditors need behavioral probes).

**Classical threads (must be conceded-and-differentiated, per digest N3):** regression test selection / test-suite minimization / prioritization (Yoo & Harrold survey, ACM TOSEM ~2012; Rothermel & Harrold) [VERIFY exact citations] — same minimality *criterion*, but white-box coverage with deterministic oracles; concept-drift detection (Gama et al., ACM CSUR 2014; DDM/ADWIN) [VERIFY] — streaming single-model degradation, not version-pair axis selection.

**Gap statement:** no prior work performs an **axis-resolved, black-box comparison of probe-family drift against real downstream-breakage ground truth across LLM version pairs, with a budgeted minimality analysis**. The novelty is the composite predictive comparison + selection protocol — *not* "first minimal test subset" (false vs SE literature) and *not* "first drift detector" (false vs the three adjacents).

**Critic:** (1) Three [VERIFY] tags sit on the paper's closest published neighbors — if any of them (especially 2512.03816, which is recent and close in spirit) already correlates its drift signal with downstream task deltas, the gap statement shrinks; this must be checked against the actual PDFs before any draft, not after. (2) The most dangerous "related work" is in-portfolio: B3.4 itself. If B3.4's paper reports fragility predictors of contracts, and B3.1 reports probe predictors of breakage, reviewers of a merged paper will ask what separates the two analyses. (3) EssenceBench-style compression should be an explicit baseline, not just a citation.

**Refined:** (1) Pre-draft verification task pinned: pull all three adjacent PDFs; for each, record in one table (a) signal used, (b) access assumption, (c) target variable, (d) whether any downstream-consequence link is attempted. Kill-criterion: if any adjacent already does probe→breakage prediction, B3.1 collapses into a replication+extension and the merged-into-B3.4 form becomes mandatory rather than preferred. (2) The B3.4 boundary is drawn now: B3.4 asks *which contract features* predict that contract's fragility (contract-side predictors); B3.1 asks *which model-side probe signals* predict aggregate and per-class breakage (model-side predictors); the merged paper presents them as the two sides of one prediction problem. (3) EssenceBench-style item compression enters the experiment grid as arm A4 (Stage 6).

---

## Stage 4 — Sub-Problems

**SP1 — Instrument validity: drift vs noise vs phrasing.** Before any prediction claim, per-family drift must be shown to exceed the within-version sampling-noise floor (repeat queries under fixed and re-sampled decoding) and to be rank-stable across ≥3 paraphrase variants of the probe items (TARE's brittleness warning applied to the measuring stick itself). Output: a per-family signal-to-noise profile and a paraphrase-stability certificate.

**SP2 — Attribution under inter-family correlation.** Families co-move (safety shifts co-occur with refusal-boundary shifts). Ranking families by marginal correlation mis-attributes shared variance. Needs partial-correlation / multiple-regression / stability-selection treatment, with the honest possible outcome "a correlated bundle predicts; no single family does."

**SP3 — Small-n predictive protocol.** Version pairs are the effective sample and there will be ~15–25 at best. Designing a LOPO protocol that does not overfit — hierarchical pooling over (pair × contract-class) cells, pre-registered model class (regularized linear), permutation-based significance — is its own methodological sub-problem.

**SP4 — Budgeted minimality with a retention guarantee.** Formalize: min |S| (in queries) s.t. LOPO performance(S) ≥ performance(full) − ε. Sub-questions: family-level vs item-level selection; whether data-driven item clusters cross the hand-designed family boundaries (which would revise the taxonomy itself); stability of the selected set under bootstrap over pairs.

**SP5 — Transferability of the selected set (the pluggable-module question, made scientific).** Does a probe set selected against B3.4's contract corpus transfer to (a) held-out contract classes, (b) B3.3's silent-change categories, (c) a different vendor's pairs? This is the empirical content behind "pluggable": the module is only reusable if selection transfers.

**Critic:** (1) As first drafted, SP5 was project management ("define an interface") — the refactor into a transfer question is right, but it must include the **tautology check**: format probes predicting format-contract breakage is near-circular (probe ≈ miniature downstream task); the scientifically interesting cell is *cross-axis* prediction (do refusal probes carry signal for format breakage? does capability drift predict tool-call breakage?). Without the cross-axis matrix, the headline result risks being "things predict themselves." (2) SP3 is the load-bearing weakness: with n≈15–25 pairs, a five-predictor regression with selection on top is at serious overfitting risk; the sub-problem list should acknowledge that the *pilot* can only deliver SP1 plus directional SP2, and that SP3/SP4 conclusions need the scale-up corpus. (3) Missing sub-problem: ground-truth portability — B3.4's corpus is simulated-production; nothing checks the probe set against even one *real* third-party pipeline.

**Refined:** SP5 is restated with the **cross-axis prediction matrix as its primary deliverable** (5 probe families × contract classes; diagonal = expected/near-tautological, off-diagonal = the novel signal), and same-axis diagonal cells are excluded from the headline predictive claim. SP3 gains an explicit staging note: pilot answers SP1 (+SP2 directionally); SP3/SP4/SP5 are powered only at scale-up — the go/no-go in Stage 6 is keyed to this. A small **SP6 (stretch): external validity spot-check** is added — 1–2 real open-source downstream projects (e.g., a deployed extraction pipeline from GitHub with its own tests) run across one version pair as an out-of-corpus breakage point; explicitly best-effort, not gating.

---

## Stage 5 — Methods

**(a) Probe-family taxonomy (five families, each with a named instrument and a drift score):**
1. **Capability** — fixed battery (MMLU/GSM8K/BBH-style items) with format-robust scoring (answer extraction after normalization; code executed after fence-stripping); drift = paired per-item correctness delta aggregated with a signed magnitude.
2. **Refusal-boundary (拒答边界)** — borderline items (XSTest / OR-Bench strata); drift = refusal-rate delta + a rate-invariant RefusalIndex-style rank shift.
3. **Format-preference** — IFEval-style instructed-format items + JSON-schema tasks; drift = change in schema-validity/structural-match rates, measured across paraphrase sets.
4. **Calibration** — items with known labels; drift = change in ECE / semantic-calibration error (B-Calibration-style for free-form).
5. **Safety-behavior** — harm-adjacent + policy-conditioned out-of-scope prompts (OffTopicEval-style) + pseudo-harmful over-refusal items; drift = accept/refuse rate changes per stratum.

Every family is administered identically to both versions, k≥3 repeats, fixed decoding, with a within-version repeat arm to estimate the noise floor. All instruments are output-only (black-box constraint); logprob-based variants are excluded from the core battery.

**(b) Breakage-prediction evaluation protocol:**
- Ground truth: B3.4's contract corpus run on both versions → per (pair, contract-class) functional breakage rates (schema failure, parser exception, template break, tool-call inexecutability).
- Unit of analysis: (version-pair × contract-class) cell. Predictors: per-family drift scores. Model class: pre-registered regularized linear / logistic model, hierarchical over pairs.
- Headline evaluation: **LOPO cross-validation** — predict the held-out pair's per-class breakage from its probes; report AUC (breakage-flagging) and R² (magnitude), with bootstrap CIs over pairs and permutation nulls.
- Attribution: standardized coefficients + partial correlations + stability selection (selection frequency under bootstrap) to handle SP2.
- **Cross-axis prediction matrix** (from SP5-refined): for each probe family × contract class, LOPO predictive performance with same-axis diagonal cells reported but excluded from headline claims.

**(c) Minimality criterion:**
- Definition: S* = argmin over subsets S of query-cost(S) subject to LOPO-AUC(S) ≥ LOPO-AUC(full) − ε, with ε pre-registered (default 0.03 AUC).
- Search: greedy forward selection at the item-cluster level (clusters learned from per-item drift-profile correlation, allowed to cross family boundaries), wrapped in bootstrap-over-pairs **stability selection**; a subset only counts as selected if chosen in ≥70% of bootstrap replicates.
- Deliverable: the **budget–retention curve** (query cost vs retained AUC) with S* marked, plus the family composition of S* (does the data-driven selection respect the hand taxonomy?).

**(d) Module packaging:** the protocol in (b)+(c) is implemented against a declared ground-truth schema (pair id, contract class, breakage rate, provenance), so B3.4's corpus, B3.3's category-resolved behavior diffs, or any future corpus can be dropped in; released as code + probe bank + selection outputs.

**Critic:** (1) Greedy selection + small n = overfitting machine; stability selection helps but the honest fix is to treat the *pilot* selection as hypothesis-generating and re-validate S* frozen on later-arriving pairs (temporal holdout), which the current text doesn't demand. (2) ε = 0.03 is arbitrary; with wide bootstrap CIs at n≈20 pairs, an ε smaller than the CI width is theater. (3) The item-cluster move quietly abandons the seed's family-level question; the paper must answer *both* ("which family predicts" for science, "which items to buy" for practice) or reviewers will see a bait-and-switch. (4) The functional-breakage ground truth inherits every design choice of B3.4's corpus; if that corpus over-represents JSON contracts, format probes win by construction — a composition-sensitivity analysis is missing.

**Refined:** (1) Add a **frozen-set temporal validation**: S* is selected on pairs available at pilot time and evaluated untouched on every pair added during scale-up (new snapshots ship continuously, so the temporal holdout grows for free); this becomes the paper's most deployment-credible number. (2) ε is re-registered as max(0.03, half-width of the full battery's own bootstrap CI) — minimality claims are only made at the resolution the data supports. (3) Report structure fixed: RQ1 answered at family level (with SP2's partialling), RQ2 at item-cluster level, explicitly flagged as two granularities of one question. (4) Add **ground-truth composition sensitivity**: re-run the ranking under reweighted contract-class mixes (equal-weight, JSON-heavy, tool-call-heavy); a family ranking that survives reweighting is a finding, one that doesn't is a property of B3.4's corpus and is reported as such.

---

## Stage 6 — Experiment Design

**Arms:**
- A1: each single probe family alone (five arms) — predictive baseline per family.
- A2: full five-family battery — upper bound.
- A3: selected minimal set S* (item-cluster level, stability-selected, frozen for temporal validation).
- A4: EssenceBench-style compression *within* capability items only — tests whether generic benchmark compression already suffices (if A4 ≈ A3, the axis structure adds nothing).
- A5: random probe subsets budget-matched to S* (10 draws) — selection-value control.
- A6: raw aggregate output-diff magnitude on the probe bank ignoring family structure — "just measure total drift" baseline.
- A7 (uniformity-test gate): rank-based shift-detection in the style of arXiv:2506.06975 [VERIFY] as a binary change detector — measures how much predictive information exists *beyond* mere change detection.

**Scale:**
- *Pilot (co-scheduled with B3.4's pilot):* 4–6 open-weight version pairs with immutable checkpoints (e.g., Llama-2→3, Qwen1.5→2→2.5, Mistral v0.1→v0.2→v0.3); ~500 probe items; ground truth = B3.4 pilot corpus (~10 contract classes). ~500 probes × 2 versions × 3 repeats × 6 pairs ≈ 18k generations on top of B3.4's runs — marginal cost is small precisely because the ground truth is shared.
- *Scale-up:* 15–25 pairs adding dated API snapshots while both endpoints are live (interleaved query windows, all raw outputs cached and released); ~1,500 probe items; ~20 contract classes; ≈ 200–650k generations total (2–4 A100-class GPUs for open-weight; low-thousands-USD API stratum).

**Metrics:** LOPO AUC / R² (headline); Spearman ρ per family; partial correlations and stability-selection frequencies; ΔAUC of S* vs full battery; budget–retention curve; cross-axis matrix off-diagonal AUC; noise-floor exceedance rate; paraphrase rank-stability (Kendall's τ across paraphrase sets); frozen-set temporal-holdout AUC; cost ratio (S* query cost vs downstream-suite cost).

**Go/no-go gates (pre-registered):**
- **G1 (instrument gate, pilot):** ≥2 families show cross-version drift above the within-version noise floor on ≥70% of pilot pairs, rank-stable across paraphrases. Fail → the probes cannot measure drift reliably; stop, report instrument negative result inside B3.4's paper (one section), do not scale.
- **G2 (signal gate, pilot→scale-up):** full-battery LOPO AUC ≥ 0.70 on pilot cells (permutation p < 0.05). Fail → probes do not predict breakage; pivot to the negative-result framing ("cheap probes do not forecast contract breakage; auditors must run contract suites"), which merges into B3.4 as a finding.
- **G3 (minimality gate, scale-up):** some subset at ≤40% of full-battery query budget within ε. Fail → "no free lunch: all axes carry non-redundant signal" — still publishable, reframed as an anti-compression finding.
- **G4 (beyond-detection gate):** A2 must beat A7 by a pre-registered margin (ΔAUC ≥ 0.05); otherwise the contribution over published shift detectors is not established and standalone framing is dead regardless of other gates.

**Merge-vs-standalone decision rule (explicit, trigger-based):**
- **Default = MERGED.** If B3.4 proceeds on schedule and its scale-up corpus reaches ≥10 version pairs, B3.1 ships as the *model-side prediction + minimal-probe-set module* of B3.4's paper (B3.4 contributes breakage rates + contract-side fragility factors; B3.1 contributes probe-side prediction + budgeted selection; one shared corpus, one paper, no salami split). B3.3 additionally consumes the family ranking as severity weights for silent-change categories.
- **Standalone trigger (all three required):** (i) G1–G2 pass **and** the cross-axis matrix shows non-trivial off-diagonal prediction (the standalone-worthy scientific surprise: probes forecast breakage they don't superficially resemble); (ii) B3.4's paper is delayed beyond one submission cycle or descopes its corpus below ~8 pairs; (iii) the Stage-3 adjacency check confirms no published probe→breakage predictor. Standalone form: measurement-study framing ("which behavioral axes carry breakage signal"), with a reduced self-built downstream suite (~10 contract classes) replacing B3.4's corpus.
- **Kill/absorb trigger:** G1 or G4 fail → B3.1 reduces to at most one section + released probe bank inside B3.4; no separate paper.

**Critic:** (1) Gate thresholds (0.70 AUC, 40% budget, 0.05 margin) are round numbers without power analysis; at pilot n (≈4–6 pairs × 10 classes = 40–60 cells, heavily correlated within pair) an AUC estimate has a CI wide enough that G2 can pass/fail by luck. (2) The merged default creates an authorship/scope hazard: if B3.4's paper is already full, the probe module gets compressed into an appendix and the minimality contribution (the actual novel bit) becomes invisible. (3) The decision rule references B3.3 consumption but no experiment here produces the category-resolved output B3.3 would need. (4) Dated-API pairs may die mid-study (endpoint deprecation), which asymmetrically hits the temporal-holdout design.

**Refined:** (1) Gates re-specified with uncertainty: G2 passes only if the *lower* bootstrap CI bound of LOPO AUC exceeds 0.60 (point ≥ 0.70); pilot is explicitly labeled directional for G3 (minimality decided at scale-up only); a simulation-based power check (synthetic breakage with plausible effect sizes) is run before pilot to size the probe bank. (2) Merged-form floor negotiated up front: the merge condition includes a minimum surface for the module — the budget–retention curve and cross-axis matrix appear as main-paper figures, or B3.1 reverts to the standalone track even if B3.4 is on time; recorded in the portfolio plan now, not at write-up. (3) Add output hook for B3.3: the per-family drift scores are logged per behavior category aligned to B3.3's changelog taxonomy, so B3.3 can join tables without new runs. (4) API stratum is treated as bonus, never load-bearing: all gates and the temporal holdout are powered on open-weight pairs alone; every API response is cached and released so the analysis (not the querying) stays reproducible after deprecation.

---

## Summary Position

B3.1 is a support topic whose scientific core — *which cheap black-box signals forecast downstream breakage, and how few probes suffice* — is genuinely novel relative to shift-detection adjacents (2504.04715, 2512.03816, 2506.06975 — all "did it change?", none "what breaks?") and to SE test-minimization (white-box, deterministic oracles). Its truth source is B3.4's corpus by design, so its strongest form is the prediction/selection module inside the B3.4 paper (with hooks into B3.3), holding standalone only behind explicit triggers: surprising cross-axis predictive signal plus B3.4 slippage plus a clean adjacency check.
