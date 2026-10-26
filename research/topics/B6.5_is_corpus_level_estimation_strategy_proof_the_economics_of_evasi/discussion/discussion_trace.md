# Discussion Trace — B6.5

> Extracted verbatim from `pipeline.md`'s "## Seed brief" through "## Cross-stage consistency check" sections (the complete round-by-round record of all six `auto-research-discussion` stages). `pipeline.md` now retains only the Phase Log (goal.md phase-gate tracking) and a pointer to this file. See `experiment_design.md` for the standalone Stage 6 spec, and `../paper_draft.md` / `paper_draft.md`/`.tex` for the assembled paper built from these confirmed stage outputs.

---

# Auto-Research-Discussion Run — B6.5 (autoclaude-style, repo-driven from digest.md + paper.md)

> Mode: **autoclaude** (self-play, Claude as student+teacher). Source: `../digest.md` (N0–N12) + `../paper.md` (Steps 0–9), both pre-existing reverse-digest artifacts for seed **B6.5**. Round cap: 5/stage (none hit). All six stages converged in 1 critic round + 1 refiner pass each — the seed material was unusually mature (paper.md already carries formal notation, six pre-registered assumptions A1–A6, and per-RQ fallback clauses), so genuine disagreement surfaced but didn't require re-proposing.
>
> **Full pipeline order (updated):** this file (`auto-research-discussion`, 6 stages) → `taste_audit.md` (`research-taste-auditor`, idea-level check on Stage 2+5) → `stage_review.md` (`pengsida-stage-reviewer`, PASS/REVISE/STOP per stage against the confirmed outputs, plus a Stage 5 Writing check on the first assembled draft) → final `paper_draft.md`/`.tex`/`.pdf`. Two REVISE findings from `stage_review.md` (a missing nearest-neighbor sentence in Related Work, and missing per-RQ falsification conditions in Experiments) are already folded into the `paper_draft.*` files below — read `stage_review.md` for the reasoning behind those two fixes.

## Seed brief

- **One-sentence description:** Test whether corpus-level (population-scale) distributional estimation of AI-generated-text prevalence is robust to a budget-bounded paraphrase adversary, or whether it inherits the fragility already demonstrated for single-document detectors — and, if robust, whether the adversary's minimum budget to bias the estimate grows with corpus size.
- **Apparent inputs:** semi-synthetic corpora with an experimenter-controlled ground-truth AI-generation proportion; a corpus-level prevalence estimator (mixture-MLE, or a debias-and-aggregate alternative); a budget-constrained paraphrasing adversary (non-adaptive and adaptive/coordinated variants).
- **Apparent outputs:** the corpus estimator's error under attack (paired against a collapsing single-document-detector control); the minimum adversary budget to bias the estimate by a fixed margin ε; a fitted scaling exponent β of that minimum budget against corpus size N.
- **Closest research areas:** AI-text prevalence measurement (`MonitorAIScale`); zero-shot single-document detection (`DetectGPT`); budget-bounded adaptive watermark evasion (`AdaptiveWMAttack`); debiased population-proportion estimation (`DUCI`); incentive-aware strategy-proofness under a manipulation budget (`UCB-S`).
- **In scope:** measuring an existing/simulated estimator-vs-adversary cost–accuracy game across controlled corpus scales. **Out of scope:** a fully white-box, estimator-omniscient adversary (digest N6's `unaddressed_challenges = ["C4"]`, paper.md A5); ground truth on real uncurated corpora; live production deployment.
- **Confidence: high.** As with the calibration reference, the "repo" here is itself a prior reverse-digest + pre-registered spec (`digest.md` + `paper.md`) — already internally cross-referenced (N-node ↔ M-component ↔ RQ ids) and already carrying its own asymmetry/taste check (`paper.md` Step 0 deletion test, Step 3 self-audit). Reconstruction risk is low; the risk is *redundancy* with `paper.md`'s own Step 5/6, which is why stages 5/6 below are framed as validating the **measurement instrument's isolation properties** (does the estimator's robustness survive coordination, cost-model choice, and a naive-averaging null model), not re-deriving `paper.md`'s already-finished hypotheses from scratch.

---

## Stage 1 — Problem Definition

### Round 1 (critic phase)

**draft_v1** (proposer):
- `summary`: Given a corpus of N documents with an unknown mixture of human- and AI-generated text, and given a budget-bounded paraphrasing adversary that may rewrite a subset of documents under a fixed total cost, determine whether a corpus-level distributional estimator's error in recovering the population-level AI-generation proportion stays bounded — and whether the minimum adversary budget required to bias that estimate by a fixed margin grows with corpus size — in contrast to the established fragility of single-document AI-text detectors under the same class of attack.
- `input`: (1) a corpus $D_N = \{d_1,\dots,d_N\}$, each document with a latent label $y_i \in \{\text{human}, \text{AI}\}$, unknown to the estimator but controllable by the experimenter in semi-synthetic corpora; (2) a corpus-level estimator $E$ that returns $\hat\alpha = E(D_N)$; (3) a single-document detector $g$, retained as a fragility control; (4) an adversary with a fixed total rewrite budget $B$ under a declared cost model (per-token or per-document-touched).
- `output`: (1) the corpus-level estimate $\hat\alpha$ and its error $e_B(N)$ against ground truth $\alpha$ under attack, paired against (2) the single-document detector's AUROC under the identical attack; (3) the minimum adversary budget $B_{\min}(\varepsilon, N)$ required to bias $\hat\alpha$ by margin $\varepsilon$; (4) a fitted scaling exponent $\beta$ of $B_{\min}$ against corpus size $N$.
- `constraints`: the adversary is budget-bounded and non-omniscient — not white-box on the exact aggregation statistic (out of scope by declaration, digest C4/paper.md A5); ground-truth $\alpha$ is only knowable in constructed semi-synthetic corpora, never in real uncurated ones; single-document detector fragility under paraphrasing is presupposed as an established prior result, not re-derived here.
- `objective`: a "strategy-proof at scale" verdict is accepted only if, at a matched budget $B$ that already collapses the single-document detector below a stated fragility threshold, the corpus estimator's error stays within a pre-registered bound **and** the fitted scaling exponent $\beta$'s confidence interval excludes zero, ideally exceeding a stated threshold, under at least two independently defined cost models.
- `study_type`: `empirical` — stated explicitly, not silently inferred: the seed's own core question ("单文档检测已被证明可被改写击穿；语料级分布估计是否在对抗规避下同样脆弱，还是规避成本随语料规模上升而变得不经济") is a measurement/characterization question about how evasion cost scales, matching digest N12's own `empirical` classification — not a new detection method being pitted for outcome superiority against a competitor.

**critique:**
- summary: Strong draft, evidence-traceable to the seed's own formal notation (`paper.md` Step 5 supplies $D_N$, $\alpha$, $E$, $\hat\alpha$, $g$, $B$, $e_0(N)$, $e_B(N)$, $\varepsilon$, $\beta$ almost verbatim), but the objective has a real evaluability gap once the two required checks can disagree.
- comments:
  - `{severity: major, field: "objective", anti_pattern: "vague_success (evaluability gap)", comment: "The objective doesn't say what happens when the two cost models disagree — either in the *magnitude* of β (positive but below the 'ideally exceeds a stated threshold' bar) or, worse, in its *sign*. paper.md's own Step 6 fallback for RQ_INF_1 already distinguishes three outcomes (β≥0.5 confirmed, 0<β<0.5 weaker sublinear claim, β≤0 or CI-includes-0 refuted) and threat t2 requires the *sign* to be invariant across cost models — but the stage-1 objective as drafted collapses all of that into 'ideally exceeds a stated threshold,' which is not evaluable as written. A reader can't tell from this objective alone whether a positive-but-sub-threshold β under one cost model and a null result under the other counts as pass, partial pass, or fail."}`
  - `{severity: minor, field: "summary", anti_pattern: null, comment: "The parenthetical clause bundles two logically separable claims (bounded error under attack; budget scaling with N) as though answering one automatically answers the other. They are separable and are in fact tested by different sub-problems later — worth flagging now so stage 4/5 doesn't accidentally treat them as one question."}`
- decision: `move_to_refiner` (both flags are formalize-level fixes using content already in `paper.md`'s own Step 5/6 — no new content needed).

### Refiner pass

- `objective` (refined): "A 'strategy-proof at scale' verdict is accepted only under a three-way outcome structure, not a binary pass/fail: (i) **confirmed** if, at a budget $B$ that drives the paired single-document detector's AUROC $\le 0.60$, the corpus estimator satisfies $e_B(N) \le 0.05$ and $e_B(N) \le 2\,e_0(N)$ at the largest tested $N$, **and** the fitted $\hat\beta$'s 95% CI lower bound exceeds 0 with a point estimate $\ge 0.5$ under *both* declared cost models; (ii) **weaker/sublinear** if $\hat\beta$'s CI excludes 0 but the point estimate is below 0.5 under one or both cost models — evasion is more expensive at scale but not disproportionately so; (iii) **refuted** if $\hat\beta$'s CI includes 0 or is negative under either cost model, or if the sign of $\hat\beta$ disagrees between the two cost models — the latter is reported as *cost-model-dependent, unresolved*, not resolved by reporting only the favorable cost model."
- `summary` (refined): unbundled the parenthetical into two explicitly separate clauses: "...determine (a) whether a corpus-level distributional estimator's error in recovering the population-level AI-generation proportion stays bounded under a budget-bounded adversary, and, independently, (b) whether the minimum adversary budget required to bias that estimate by a fixed margin grows with corpus size — in contrast to..."
- `formal_summary` (added, per stage-1 refiner's formalize-for-free duty, reusing `paper.md` Step 5 notation directly since the seed already supplies it): "Corpus $D_N=\{d_1,\dots,d_N\}$, latent labels $y_i\in\{\text{human,AI}\}$, true prevalence $\alpha=\frac1N\sum_i\mathbb 1[y_i=\text{AI}]$. Estimator $E$: $\hat\alpha=E(D_N)$. Detector $g$: $\mathrm{AUROC}(g;D_N)$. Adversary $\mathcal A$ transforms $D_N\to D_N'$ under cost model $c$, spending budget $B(\mathcal A)=\sum_i c(d_i,d_i')$. Clean error $e_0(N)=\mathbb E|E(D_N)-\alpha|$; attacked error $e_B(N)=\mathbb E|E(D_N')-\alpha|$; bias margin $\varepsilon=|E(D_N')-E(D_N)|$; minimum budget to bias $B_{\min}(\varepsilon,N)=\min\{B(\mathcal A):|E(D_N')-E(D_N)|\ge\varepsilon\}$; scaling exponent $\beta=$ OLS slope of $\log B_{\min}$ on $\log N$. Determine the joint behavior of $(e_B(N), \hat\beta)$ relative to $g$'s collapse under the same $B$."
- `changes_made`: tightened `objective`'s evaluability condition into an explicit three-way outcome structure; unbundled the two separable claims in `summary`; added `formal_summary` reusing the seed's own notation.
- `declined_to_fix`: none.

**Confirmed Stage 1** — `study_type: empirical`.

---

## Stage 2 — Motivation

### Round 1 (critic phase)

**draft_v1:**
- `summary`: Practitioners increasingly rely on corpus-level AI-text prevalence estimates — for data-curation auditing, platform-scale moderation, or governance reporting — precisely because they have been told instance-level detection is unreliable under adversarial paraphrasing, but whether that reframe genuinely trades away the adversary's leverage, or merely defers the same fragility to a different statistic, has not been directly measured.
- `why_it_matters`: If corpus-level estimation quietly inherits single-document fragility, then treating it as a safe fallback is actively dangerous — a decision-maker who believes an aggregate estimate is robust "because any individual verdict can be gamed but the pooled estimate can't" is trusting exactly the averaging intuition that is plausible but unverified. Conversely, if the same budget that reliably flips a single-document verdict requires disproportionately more spend to move a population-scale proportion, that is a positive, actionable result: it tells practitioners corpus-level auditing is a genuinely different (and better) instrument, not single-document detection wearing an aggregation layer.
- `who_cares`: Teams running corpus-level content-authenticity or dataset-contamination audits who need to know whether their aggregate number can be gamed by a motivated minority of paraphrased documents; designers of AI-text-prevalence monitoring pipelines (à la `MonitorAIScale`) deciding whether their instrument needs an adversarial-robustness certification before being trusted for governance decisions; researchers extending the "single-document detection is broken" result who might over-generalize it to every AI-text measurement task without checking whether the target statistic actually changes the adversary's economics.
- `evidence`: `[MonitorAIScale, OpenReview:bX3J7ho18S]`'s own motivation reframes AI-text detection as measurement precisely because instance-level detection is unstable, but validates its mixture-MLE estimator only on semi-synthetic mixtures generated by a benign, non-adversarial process — it never tests an adversary trying to move the fitted mixing coefficient. `[AdaptiveWMAttack, OpenReview:AsODat0dkE]`'s own motivation argues adaptive, budget-bounded attackers should be the default threat model for any detection-adjacent claim, not an edge case — a standard this corpus-level literature has not yet been held to. None of the seven N3 works combines a budget-bounded adversary with a corpus-level (not per-document) target statistic — itself evidence the question is open.

**critique:**
- summary: Good stake-specific motivation with real citations, but it motivates *that* robustness matters without motivating *why the scaling behavior across N*, specifically, is the load-bearing quantity.
- comments:
  - `{severity: major, field: "why_it_matters", anti_pattern: "partial_output_coverage", comment: "Stage 1 output (4) is a scaling exponent β — a claim about how cost behaves *across corpus sizes*, not merely whether robustness holds at one practically-relevant N. why_it_matters argues why robustness-or-fragility matters but never explains why measuring the *scaling law* is necessary, as opposed to simply confirming robustness once at whatever corpus size a practitioner cares about. A reader could reasonably ask: 'if you can show robustness holds at N=10^5 already, why do I need the exponent β at all?' — that question is real and currently unaddressed."}`
- decision: `move_to_refiner`.

### Refiner pass

- `why_it_matters` (extended): "...critically, a single-N confirmation cannot distinguish 'robust regardless of scale' from 'coincidentally robust at this one tested size' — two claims with very different practical implications for whether the result transfers to a corpus a practitioner hasn't directly tested. Real deployments span orders of magnitude (a platform's daily upload queue vs. a regulator's full historical audit corpus), so what a decision-maker actually needs is a transferable safety-margin *function* of corpus size, not a point estimate at one size. A fitted exponent β with a confidence interval is exactly that function — and it is also the only form in which the seed's counterintuitive claim ('evasion becomes uneconomical at scale,' not merely 'evasion happens not to work today') is falsifiable at all: a claim about a *trend* requires measuring more than one point on the curve."
- `changes_made`: added the scaling-law-vs-single-point argument, tying it to both practical transferability and to what actually makes the seed's claim falsifiable.
- `declined_to_fix`: none.

**Confirmed Stage 2.**

---

## Stage 3 — Related Work

All seven works below are treated as **specific (deep) tier** — digest N3/N4 already engaged each one at the approach + limitation level (no title-only landscape mentions were present in the source material, and per the no-fabrication rule, no additional landscape papers are invented here to pad a `general_related_works` list).

### Round 1 (critic phase)

**draft_v1** (`specific_related_works`, abbreviated to citation / role / `is_potential_baseline` / limitation → sub-problem it will motivate):

| work_id | citation | role in this paper | is_potential_baseline | limitation |
|---|---|---|---|---|
| `rw_monitoraiscale` | Anon., MonitorAIScale (OpenReview:bX3J7ho18S) | instantiated as the primary corpus estimator (M2) | **true** | `lim_monitoraiscale_nonadversarial`: "Validated only on semi-synthetic mixtures generated under a benign, non-adversarial process; never models an adversary who paraphrases specifically to shift the fitted mixing coefficient." |
| `rw_detectgpt` | Anon., DetectGPT (OpenReview:UiAyIILXRd) | instantiated as the single-document fragility control (M1) | **true** | `lim_detectgpt_paraphrase_fragility`: "Produces per-document curvature verdicts that degrade under paraphrasing; offers no aggregate-estimate quantity and no notion of whether averaging over a corpus restores what per-document detection loses." |
| `rw_adaptivewmattack` | Anon., AdaptiveWMAttack (OpenReview:AsODat0dkE) | protocol adapted for the adaptive/coordinated adversary (M3) | false (protocol borrowed, not a corpus-estimation competitor) | `lim_adaptivewmattack_perdocument`: "Defines its evasion objective and budget *per text* against a per-text watermark verifier; never asks whether the same per-document budget suffices to move a population-level statistic." |
| `rw_markovcalib` | Anon., MarkovCalib (OpenReview:Lzwkeg2o2z) | context only — token-score aggregation for passage-level decisions | false | `lim_markovcalib_benign_noise`: "Improves passage-level aggregation of token scores under benign sampling noise (a Markov smoothness prior), assumes noise is incidental rather than adversarially coordinated, and still targets a per-passage decision rather than a corpus proportion." |
| `rw_duci` | Anon., DUCI (OpenReview:EUSkm2sVJ6) | instantiated as the debias-and-aggregate alternate estimator | **true** | `lim_duci_stationarity`: "Assumes per-record measurement-error rates (TPR/FPR) are stationary and estimable from reference models; an adversary who deliberately shifts per-record signals to bias the aggregate violates that stationarity assumption." |
| `rw_anchorpeerreview` | Anon., AnchorPeerReview (OpenReview:HyZwf1rt4s) | context only — instance-level detector benchmark | false | `lim_anchorpeerreview_no_robustness_analysis`: "Builds an instance-level detector benchmarked at low FPR and merely cites prior population-level LLM-prevalence estimates as motivation; never analyzes the robustness of those population estimates to strategic evasion." |
| `rw_ucbs` | Anon., UCB-S (OpenReview:lsxeNvYqCj) | conceptual anchor for the "strategy-proof under a manipulation budget" vocabulary | false (different domain — bandit allocation, not text estimation) | `lim_ucbs_no_text_bridge`: "Develops strategy-proofness for bandit *allocation* under a manipulation budget with a payment-free screening mechanism; provides the vocabulary but has no existing bridge to text-corpus distributional prevalence estimation." |

**critique:**
- summary: Grounding is solid and every limitation is specific (not "scalability issues"-style vagueness), but the `is_potential_baseline: true` labels on three works risk implying they're beat-a-number competitors when in fact all three are instruments this paper directly instantiates.
- comments:
  - `{severity: major, field: "specific_related_works[rw_monitoraiscale, rw_detectgpt, rw_duci].is_potential_baseline", anti_pattern: "io_approach_mismatch (inverted)", comment: "Per the stage-3 rubric, a 'baseline' is something the paper's result is compared *against* to show an improvement. But MonitorAIScale's estimator and DUCI's estimator are literally instantiated *as* this paper's own M2 (primary and alternate), and DetectGPT is instantiated as M1, the paired fragility control whose collapse is the point of comparison, not a rival being beaten. Marking all three `true` without qualification risks the same mis-signal the calibration reference (B5.5) flagged for SOTOPIA: implying these papers' own reported numbers are what gets compared against, which they are not — this is an *empirical measurement* study (study_type=empirical), so nothing here is framed as 'beats baseline X' at all."}`
- decision: `move_to_refiner` (a wording-precision fix, not structural — the works are still legitimately instantiated as components/controls).

### Refiner pass

- `is_potential_baseline` notes sharpened for all three: "Not a baseline in the beat-a-number sense — none of `[MonitorAIScale]`, `[DetectGPT]`, or `[DUCI]`'s own reported numbers are compared against. `[MonitorAIScale]` and `[DUCI]` are instantiated as this paper's own estimator options (M2 primary/alternate); `[DetectGPT]` is instantiated as the paired fragility control (M1) whose known collapse under the *same* attack budget is itself part of the evidence, not a competitor's score to beat. Retained as `is_potential_baseline: true` only in the loose sense that their *protocols* are directly run inside this paper's own pipeline, distinct from `rw_adaptivewmattack`'s protocol-only borrowing and `rw_ucbs`'s vocabulary-only anchoring."
- `changes_made`: clarified that "potential baseline" here means "instantiated instrument/control," never "external number to beat" — consistent with `study_type: empirical` forbidding outcome-tier framing everywhere downstream.
- `declined_to_fix`: none.
- **Note on `verify_as_hypothesis`:** set `false` on every limitation. None is flagged as a stage-6 framing-tier RQ — the closest candidates (`lim_duci_stationarity`, `lim_anchorpeerreview_no_robustness_analysis`) restate this paper's own core question rather than adding a distinct framing check, and are already covered end-to-end as mechanism-tier RQs in Stage 6 via `sp_debiasing_under_adversarial_shift`. Per `stages.md`: *"If nothing was flagged, emit zero framing-tier RQs — don't manufacture one."*

**Confirmed Stage 3.**

---

## Stage 4 — Sub-Problems

### Round 1 (critic phase)

**draft_v1** (5 sub-problems, from digest N5's C1–C3 plus digest N4's DUCI limitation and a novel confound-isolation problem):

- **`sp_coordinated_evasion`** — *description:* Determine whether the corpus estimator's presumed noise-averaging robustness survives an adversary that coordinates rewrites directionally across the corpus, rather than paraphrasing each document independently. *why_it_is_a_problem:* the entire strategy-proofness claim rests on an unstated assumption that per-document perturbations behave like independent noise that cancels under aggregation; if a correlated adversary defeats it, the seed's central claim collapses regardless of what happens under a weaker attacker. *technical_challenge:* constructing a genuinely directional (not merely stronger) rewrite allocation, and training it against a non-differentiable corpus estimator without gradient access. *source_limitation_ids:* `["lim_monitoraiscale_nonadversarial"]`.
- **`sp_cost_model_ambiguity`** — *description:* Define an adversary cost model (tokens rewritten, fraction of documents touched, or paraphrase-compute spend) precise enough that the strategy-proofness conclusion isn't an artifact of one arbitrary bookkeeping choice. *why_it_is_a_problem:* different cost models imply different optimal attacks (uniform-light rewriting vs. concentrated-heavy rewriting of a subset), so a conclusion that only holds under one convention is a property of the convention, not of the estimator. *technical_challenge:* no canonical cost model exists in this literature; the same scaling question must be re-asked under at least two non-nested conventions and the qualitative conclusion checked for sign agreement. *source_limitation_ids:* `["__novel__"]`.
- **`sp_ground_truth_construction`** — *description:* Construct evaluation corpora with a known, controllable ground-truth AI-generation proportion, since no real uncurated corpus has verifiable ground truth for what fraction is AI-generated. *why_it_is_a_problem:* without controllable ground truth, no error metric $e_B(N)$ is even computable, and a construction that leaks a trivial shortcut (e.g., topic correlates with label) would make any estimator "work" for the wrong reason. *technical_challenge:* building semi-synthetic corpora that are hard enough to be informative while still admitting a verifiable ground-truth $\alpha$, and ruling out the trivial-artifact failure mode rather than merely asserting it away. *source_limitation_ids:* `["__novel__"]`.
- **`sp_debiasing_under_adversarial_shift`** — *description:* Determine whether a debias-and-aggregate estimator's correction — which assumes stationary per-record detector error rates — still holds when an adversary deliberately shifts those error rates by paraphrasing. *why_it_is_a_problem:* a debiasing correction computed once from clean reference data is only valid if the adversary doesn't change the very error rates it corrects for; if it can, the debiased estimate silently inherits a stale correction, a distinct failure mode from a likelihood-based estimator's. *technical_challenge:* isolating a stationarity-violation failure specifically, rather than conflating it with the coordinated-evasion question already covered by `sp_coordinated_evasion`. *source_limitation_ids:* `["lim_duci_stationarity"]`.
- **`sp_design_vs_scale_confound`** — *description:* Isolate whether any observed adversarial robustness stems from the corpus-level estimator's specific aggregation design (mixture-MLE or debias-aggregate) or is a generic property of averaging over many documents that a naive mean-of-per-document-scores estimator would also exhibit. *why_it_is_a_problem:* without this, the paper's claim that a *dedicated* estimator matters is confounded with the trivial fact that any large-N average has lower variance than a single document. *technical_challenge:* constructing a "no design" null model (the naive average) that is a fair comparator rather than a strawman, and running it under identical attack conditions. *source_limitation_ids:* `["__novel__"]`.

**critique:**
- summary: Coverage checks out (solving all five would jointly deliver stage 1's objective); one pair of sub-problems risks reading as the same underlying question twice.
- comments:
  - `{severity: minor, field: "sp_coordinated_evasion / sp_design_vs_scale_confound", anti_pattern: "overlap", comment: "Both ultimately ask 'is the observed robustness real or an artifact?' which can read as the same sub-problem restated. They are genuinely distinct — one is about *attacker capability* (can a smarter, coordinated adversary defeat the robustness that holds against an independent one?), the other about *estimator internals* (even against a fixed, weak attacker, does the specific aggregation design matter versus generic averaging?) — but the descriptions don't make that axis distinction explicit enough."}`
- decision: `move_to_refiner`.

### Refiner pass

- `sp_coordinated_evasion.technical_challenge` sharpened to end with: "...this is an **attacker-capability** axis — does robustness generalize beyond the (weaker) independent-perturbation threat model — distinct from whether the estimator's design is doing anything at all."
- `sp_design_vs_scale_confound.technical_challenge` sharpened to end with: "...this is an **estimator-internals** axis, orthogonal to attacker capability: it is asked even holding the attacker fixed at its weakest (non-adaptive) setting, and asks only whether the specific aggregation machinery — not just aggregation itself — is responsible for the result."
- `changes_made`: made the attacker-capability-vs-estimator-internals distinction explicit in both `technical_challenge` fields.
- `declined_to_fix`: none.

**Confirmed Stage 4** (5 sub-problems; 2 sourced from related-work limitations, 3 `__novel__` with stated decisive-component justifications).

---

## Stage 5 — Method Design

### Round 1 (critic phase)

**draft_v1** (5 methods):

- **`m_coordinated_adversary_arm`** → targets `sp_coordinated_evasion`. *proposed_approach:* Alongside the non-adaptive fixed-budget paraphraser (independent per-document rewrites), build a coordinated/adaptive adversary (DPO-tuned against a surrogate estimator, à la `[AdaptiveWMAttack]`) that optimizes its budget allocation specifically to shift $\hat\alpha$ in one direction, and compare its bias-per-budget efficiency against the non-adaptive one at matched budget. *key_insight:* independent per-document noise cancels under aggregation by construction, but a directionally coordinated adversary specifically breaks that cancellation — so the adaptive-vs-non-adaptive contrast isolates whether the estimator's apparent robustness depends on the (unrealistic) assumption of an uncoordinated attacker. *hypotheses:* ["The adaptive/coordinated adversary requires no less budget than the non-adaptive adversary to bias $\hat\alpha$ by margin $\varepsilon=0.10$ at matched corpus size — budget-matched coordination does not defeat the aggregation-based robustness advantage.", "If the adaptive adversary requires strictly less budget than the non-adaptive one to achieve the same bias margin, the fitted scaling exponent $\beta$ will still have a 95% CI lower bound $>0$ under the adaptive adversary — coordination narrows but does not eliminate the scale-taxed cost structure."]
- **`m_cost_model_invariance`** → targets `sp_cost_model_ambiguity`. *proposed_approach:* Define and report the adversary's budget under two independent, non-nested cost models (per-token rewritten; per-document-touched × rewrite strength), running the full minimum-budget-to-bias search separately under each, and require the qualitative scaling conclusion (the sign of $\beta$) to agree across both rather than reporting only the more favorable one. *key_insight:* different cost models imply different optimal attack allocations (uniform-light vs. concentrated-heavy), so a conclusion holding under only one bookkeeping convention would be an artifact of that convention, not a property of the estimator. *hypotheses:* ["The fitted scaling exponent $\beta$ has a 95% CI lower bound $>0$ under both the per-token and the per-document-touched cost models, not only under whichever model happens to be reported."]
- **`m_semisynthetic_ground_truth_design`** → targets `sp_ground_truth_construction`. *proposed_approach:* Build semi-synthetic corpora from real human/AI text pairs (RAID, HC3) with an experimenter-set ground-truth AI proportion $\alpha$, validated by a walking-skeleton check that (i) the clean (no-adversary) estimator recovers $\alpha$ within a pre-registered tolerance and (ii) a shuffled-label control fails to recover $\alpha$ — ruling out a trivial artifact making $\alpha$ recoverable regardless of the estimator. *key_insight:* a ground-truth check that only confirms the estimator "works" is insufficient; the shuffled-label negative control is what rules out the possibility that the construction procedure itself, not the estimator, produces an accurate $\hat\alpha$. *hypotheses:* ["The clean corpus-level estimator recovers the experimenter-set $\alpha$ within a pre-registered tolerance across all tested corpus sizes, while a shuffled-label control's estimate deviates from $\alpha$ by significantly more than that tolerance.", "Under a fixed adversary budget $B$ that drives the paired single-document detector's AUROC to $\le 0.60$, the corpus-level (mixture-MLE) estimator's error $e_B(N)$ remains $\le 0.05$ and $\le 2\,e_0(N)$ at $N=10^5$ — establishing that corpus-level estimation resists the same budget that defeats single-document detection."]
- **`m_naive_debias_control`** → targets `sp_debiasing_under_adversarial_shift`. *proposed_approach:* Alongside the primary mixture-MLE estimator, run a debias-and-aggregate estimator (`[DUCI]`-style) that corrects per-document detector scores using reference TPR/FPR rates, and test both under an adversary whose paraphrasing specifically shifts the per-document error rates the debiasing step assumes are stationary. *key_insight:* a debiasing correction computed once from clean reference data is only valid if the adversary doesn't change the error rates it's built on — a distinct failure mode from the mixture-MLE estimator's likelihood-based approach. *hypotheses:* ["Under the fixed-budget adversary, the debias-and-aggregate estimator's error grows relative to its no-adversary baseline by more than the mixture-MLE estimator's does, at matched budget and corpus size — indicating the stationarity assumption is the more fragile of the two estimator designs."]
- **`m_naive_average_control`** → targets `sp_design_vs_scale_confound`. *proposed_approach:* Alongside the two dedicated corpus estimators, run a naive baseline that simply averages the single-document detector's per-document scores into a corpus-level proportion estimate, with no calibration or distributional modeling, and compare all three estimators' error under identical attack conditions at matched $(N,B)$. *key_insight:* if the naive average is just as robust as the dedicated estimators, the observed "corpus-level robustness" is a generic consequence of averaging over many documents, not evidence that a specifically designed estimator does anything — so this comparison is what makes the estimator-design contribution non-vacuous. *hypotheses:* ["At matched N and B, the naive per-document-average estimator's error exceeds each dedicated estimator's (mixture-MLE, debias-aggregate) by at least 2×, with the ratio's 95% CI lower bound $\ge 2$ — indicating the robustness benefit is attributable to estimator design, not generic averaging."]

**critique:**
- summary: Every method has a real mechanism (no goal-restatement), every hypothesis is falsifiable with a stated threshold — but two methods each carry two headline claims and need a one-line justification for why that's one mechanism, not two, mirroring a pattern the calibration reference also had to justify.
- comments:
  - `{severity: minor, field: "m_coordinated_adversary_arm.hypotheses", anti_pattern: null, comment: "Two hypotheses (budget parity, and scaling persistence under a stronger attacker) are related but logically separable claims bundled into one method. Worth stating explicitly why one experimental arm produces both readouts."}`
  - `{severity: minor, field: "m_semisynthetic_ground_truth_design.hypotheses", anti_pattern: null, comment: "Two hypotheses here (ground-truth/shuffle-control validity, and the headline robustness-under-attack finding) are doing different jobs — one validates the measurement instrument, the other is the paper's central empirical claim (digest RQ1). Bundling them under 'ground truth construction' risks burying the headline claim inside what reads like an instrument-validity method."}`
- decision: `move_to_refiner`.

### Refiner pass

- `m_coordinated_adversary_arm.key_insight` extended: "...a single adversary-construction pipeline (train the coordinated adversary against a surrogate, then run it at the same declared budgets as the non-adaptive adversary) yields two distinct, separately falsifiable readouts from one comparison: whether coordination reduces the required budget at all (tests attacker-capability sensitivity), and, independently, whether the scale-taxation property survives even if it does (tests whether the headline scaling claim is robust to the strongest attacker considered) — one experimental arm, two readouts, not two mechanisms."
- `m_semisynthetic_ground_truth_design.key_insight` extended: "...the same semi-synthetic construction underwrites two separately falsifiable readouts: whether the construction itself is trustworthy (clean recovery + shuffled-label negative control — an instrument-validity claim that must hold before anything else is interpretable) and, built on that validated instrument, whether the estimator is robust under the fixed-budget attack that already defeats the paired single-document detector (the paper's headline empirical claim). The second claim is uninterpretable without the first, which is why they share one method rather than being split across two."
- `changes_made`: justified both two-hypotheses-one-method structures explicitly.
- `declined_to_fix`: none.

**Confirmed Stage 5** — 5 methods, **7 hypotheses total** (2 + 1 + 2 + 1 + 1 across the five methods respectively — `m_coordinated_adversary_arm` and `m_semisynthetic_ground_truth_design` each carry two, per the refiner's one-instrument-two-readouts justification above), mixing instrument-validity claims with the study's headline empirical predictions — a deliberate design choice for an `empirical` study_type, explained in the stage-6 header below.

---

## Stage 6 — Experiment Design

**Tier accounting (checked against study_type=empirical):**
- **Mechanism-tier: 7 RQs**, one per Stage 5 hypothesis (verbatim `target_hypotheses`).
- **Framing-tier: 0 RQs** — no Stage 3 limitation was flagged `verify_as_hypothesis`; none manufactured.
- **Outcome-tier: 0 RQs** — `study_type = empirical` forbids "our procedure beats baseline X" framing. The naive-average and debias-vs-MLE comparisons are diagnostic isolations (is robustness generic or design-specific?), never framed as "our estimator beats a competitor."

### Round 1 (critic phase)

**draft_v1:**

`datasets`:
- RAID (Dugan et al., 2024) — *justification:* large multi-domain, multi-generator machine-generated-text benchmark including adversarial/paraphrase variants; supplies the $\ge 3$ generator families (GPT-, Llama-, Claude-class) needed so the scaling result isn't an artifact of one generator.
- (draft initially listed HC3 with justification only "digest mentions it as a paired human/LLM corpus source" — flagged below.)
- Semi-synthetic mixed corpora with experimenter-controlled ground-truth AI proportion, built from the above — *justification:* the only way to make $e_B(N)$ computable at all (no real corpus has verifiable ground truth), mirroring `[MonitorAIScale]`'s own semi-synthetic validation protocol.

`baselines` (sanity-check comparators, not outcome-tier competitors):
- B0 — population-scale single-document mean (no distributional modeling, no calibration): the "why do this at all" control; if B0 is already strategy-proof, the entire estimator apparatus is unjustified.
- B-alt — a budget- and capability-matched adaptive/coordinated adversary (the same instrument as `m_coordinated_adversary_arm`), run at identical budget to the non-adaptive adversary: the "strongest-alternative-explanation" control ruling out "the observed robustness is just an artifact of a weak, non-adaptive attacker."

`research_questions` (7, all mechanism-tier):

| rq_id | target_sub_problem_id | target_hypotheses (verbatim) |
|---|---|---|
| `rq_coordination_budget_parity` | `sp_coordinated_evasion` | "The adaptive/coordinated adversary requires no less budget than the non-adaptive adversary to bias $\hat\alpha$ by margin $\varepsilon=0.10$ at matched corpus size — budget-matched coordination does not defeat the aggregation-based robustness advantage." |
| `rq_coordination_scaling_persists` | `sp_coordinated_evasion` | "If the adaptive adversary requires strictly less budget than the non-adaptive one to achieve the same bias margin, the fitted scaling exponent $\beta$ will still have a 95% CI lower bound $>0$ under the adaptive adversary — coordination narrows but does not eliminate the scale-taxed cost structure." |
| `rq_cost_model_sign_invariance` | `sp_cost_model_ambiguity` | "The fitted scaling exponent $\beta$ has a 95% CI lower bound $>0$ under both the per-token and the per-document-touched cost models, not only under whichever model happens to be reported." |
| `rq_ground_truth_recovery_validity` | `sp_ground_truth_construction` | "The clean corpus-level estimator recovers the experimenter-set $\alpha$ within a pre-registered tolerance across all tested corpus sizes, while a shuffled-label control's estimate deviates from $\alpha$ by significantly more than that tolerance." |
| `rq_base_robustness_under_attack` | `sp_ground_truth_construction` | "Under a fixed adversary budget $B$ that drives the paired single-document detector's AUROC to $\le 0.60$, the corpus-level (mixture-MLE) estimator's error $e_B(N)$ remains $\le 0.05$ and $\le 2\,e_0(N)$ at $N=10^5$." |
| `rq_debias_fragility_under_shift` | `sp_debiasing_under_adversarial_shift` | "Under the fixed-budget adversary, the debias-and-aggregate estimator's error grows relative to its no-adversary baseline by more than the mixture-MLE estimator's does, at matched budget and corpus size." |
| `rq_naive_average_vs_dedicated` | `sp_design_vs_scale_confound` | "At matched N and B, the naive per-document-average estimator's error exceeds each dedicated estimator's (mixture-MLE, debias-aggregate) by at least 2×, with the ratio's 95% CI lower bound $\ge 2$." |

(setup/sample-size/statistical-test/expected-outcome/metrics per RQ carried into the paper draft's Experiments section below, reusing `paper.md`'s already-designed Step-6/Step-9 numbers and fallback clauses as authored design targets, not fabricated results.)

**critique:**
- summary: Tier accounting is clean and every RQ traces to a verbatim hypothesis, but one dataset justification is a citation to the digest instead of a real methodological reason.
- comments:
  - `{severity: major, field: "datasets[HC3]", anti_pattern: "weak justification (not a named anti-pattern, but fails the rubric's 'justification for why this dataset actually stresses the hypothesis')", comment: "'digest mentions it' is not a justification — it says nothing about which RQ needs HC3 specifically, as opposed to any other paired human/LLM corpus."}`
- decision: `move_to_refiner`.

### Refiner pass

- `datasets` entry replaced: "HC3 (Human ChatGPT Comparison Corpus, Guo et al., 2023) — *justification:* provides matched human/LLM answers to the *same prompts*, giving the tightest available control for constructing controllable-$\alpha$ semi-synthetic corpora with minimal topical confound between the human and AI portions. This directly stresses `rq_ground_truth_recovery_validity`'s shuffled-label control: if human and AI text differed systematically in topic (as they might from unpaired sources), an estimator could recover $\alpha$ by exploiting topic rather than authorship signal, and the shuffled-label check alone might not catch a *topic-correlated* shortcut. HC3's matched-prompt pairing is what makes that specific failure mode a real risk worth ruling out, rather than one simulated away by construction."
- `changes_made`: gave HC3's inclusion a hypothesis-linked reason (stresses the shuffled-label control's ability to catch a topic-confound shortcut) instead of a provenance note.
- `declined_to_fix`: none.

**Confirmed Stage 6.**

---

## Cross-stage consistency check (final pass, all six stages)

1. **No method leak** in stages 1/2/4 — checked; `objective`/`why_it_is_a_problem` fields name no technique.
2. **ID stability** — no id renamed mid-run; `sp_*` / `m_*` / `rq_*` stable stage-to-stage.
3. **Reference integrity** — `sp_coordinated_evasion.source_limitation_ids = ["lim_monitoraiscale_nonadversarial"]` ∈ Stage 3 limitations ✓; `sp_debiasing_under_adversarial_shift.source_limitation_ids = ["lim_duci_stationarity"]` ∈ Stage 3 ✓; all other `source_limitation_ids = ["__novel__"]` ✓; every `target_sub_problem_id` in Stage 5 ∈ Stage 4 ✓; every Stage 6 `target_hypotheses` is a verbatim match to a Stage 5 hypothesis ✓.
4. **Output coverage** — Stage 1's four outputs ($\hat\alpha$/$e_B(N)$, paired AUROC control, $B_{\min}(\varepsilon,N)$, scaling exponent $\beta$) are each reachable: (1)+(2) via `sp_ground_truth_construction`'s `rq_base_robustness_under_attack`; (3)+(4) via `sp_coordinated_evasion` and `sp_cost_model_ambiguity`'s RQs — nothing promised in Stage 1 falls off the chain by Stage 6.
5. **`study_type` consistency** — `empirical` throughout; Stage 6 correctly emits 0 outcome-tier RQs.

**What was hardest:** the recurring tension was **not disagreement about facts** (the seed material — especially `paper.md`'s pre-registered assumptions A1–A6 and fallback clauses — is unusually well-specified) but **deciding whether a paper.md-declared control (B0, B-alt) deserved its own sub-problem/method or should remain a bystander baseline**. Resolved by promoting both into full methods with their own falsifiable hypotheses (`m_naive_average_control` for B0, folded into `m_coordinated_adversary_arm` for B-alt) rather than leaving them as unexamined sanity checks — since the whole point of `rq_naive_average_vs_dedicated` and `rq_coordination_scaling_persists` is to test them directly, not merely report their numbers.

**Total rounds:** 6 stages × 1 critic round + 1 refiner pass = 6 critic rounds, 6 refiner passes. No stage hit the round cap; no cross-stage backup was required.

---

## Post-review revision round (2026-07-05)

Revision pass over the three review artifacts (`stage_review.md`, `taste_audit.md`; no
`design_review.md` exists for this topic). Every finding in those files was enumerated and
statused against the current deliverables. This section records the disposition of each; it
appends to — and does not rewrite — the historical rounds above.

**Findings already applied and logged during the original pipeline run** (verified still present
in the current deliverables; no re-work needed, listed for completeness):

1. `stage_review.md` Stage 2 REVISE → nearest-neighbor sentence opening Related Work — applied in
   `paper_draft.md`/`.tex` (pipeline Phase E/F era; confirmed present).
2. `stage_review.md` Stage 4 REVISE → explicit **Falsification condition** line in all seven RQ
   subsections — applied; 7/7 present in both `paper_draft.md` and `paper_draft.tex`.
3. `stage_review.md` Phase A items 1, 2, 5, 6 (digest N12 `absence_comment`; reference-cache
   backfill; RQ1 Aggregation line + A1–A6 `Gate:`/`Consequence:` slots; Estimand line,
   confound-naming list, power/INCONCLUSIVE statement) — applied in `digest.md`/`paper.md`/
   `reference_candidates.jsonl`; logged in `pipeline.md` Phase A row.
4. `stage_review.md` reference-cache re-check gap (3 `selected` works uncited) + Phase E/F
   `[major]` (zero `\cite`/no `refs.bib`) + Phase G `[moderate]` (missing Threats to Validity
   section) — all applied; logged in `pipeline.md` Phase E/F and G rows.

**Finding applied in this revision round:**

5. `stage_review.md` Phase G `[minor]` #1 (the only logged-not-fixed item): RQ2's **Metrics** line
   cross-referenced "the non-adaptive-adversary $\hat\beta$ from RQ3" imprecisely — RQ3 is the
   cost-model-invariance RQ, and the base non-adaptive $\hat\beta$ is computed inside RQ3's
   corpus-size sweep rather than being RQ3's own question. **What changed:** the Metrics line now
   reads "...compared against the base non-adaptive-adversary $\hat\beta$ fitted at the primary
   cost model inside RQ3's corpus-size sweep (RQ3's question is cost-model invariance; its sweep
   is where the base non-adaptive scaling exponent is computed)." **Files:** `paper_draft.md`
   (RQ2 Metrics line) and mirrored into `paper_draft.tex`; `paper_draft.pdf` recompiled via
   `latexmk -pdf` (exit 0, 15 pages, 0 errors, 0 undefined citations). No claim, number, or
   hypothesis text was altered — wording clarification only. `experiment_design.md`'s RQ2 lines
   never contained the imprecise cross-reference, so it needed no edit.

**Findings rejected as moot (not applied, with reasons):**

6. `stage_review.md` Phase G `[minor]` #2 (no numbered `\label`/`\ref` cross-references anywhere
   in the LaTeX) — rejected: the review itself classifies this as "consistent throughout, not a
   defect"; introducing numbered refs now would be new content, not a fix.
7. `pipeline.md` open to-do (1): 7 OpenReview-sourced `selected` cache records remain
   `verified.id_resolves=false` — rejected as environment-blocked, not a deliverable edit: no PDF
   is cached locally and live resolution is bot-challenge-gated/404 (recorded in
   `stage_review.md`'s integrity re-check); the honest `false` flag stays.
8. `taste_audit.md` — no action items: verdict 🟢 in both the original audit and the Phase H
   re-audit ("reconfirmed, no drift"); §6's takeaway is guidance for *future* topics, not a change
   request for this one.

**Cross-deliverable consistency check (this round):** RQ count 7 = 7 = 7 across
`paper_draft.md`, `paper_draft.tex`, `experiment_design.md`; effect floors ($\hat\beta \ge 0.5$,
$\ge 2\times$ naive-average ratio) and margins ($\varepsilon = 0.10$, attacked error $\le 0.05$
and $\le 2\,e_0(N)$ at $N = 10^5$, paired-detector AUROC $\le 0.60$) match across
`paper.md`, `paper_draft.md`, and `experiment_design.md`; the seven **Target hypothesis** blocks
in `experiment_design.md` remain verbatim Stage 5 text (untouched this round). No mismatch found;
nothing needed fixing.
