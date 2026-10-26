# How Many Prompts Break per Upgrade? Contract Breakage Rates for Structured-Output Pipelines — Pre-Registered Paper Specification
> Generated from digest.md + README.md. Status: specification, no experiments run. All ids (C1.., M1.., RQ.., CO..) refer to digest.md.

## Step 0 — Core Asymmetry (升维)

**Asymmetry sentence.** For an LLM structured-output contract, *"the upgrade broke it"* and *"the same model flipped it on resampling"* are the **identical pass/fail measurement applied to two partitions of the same output pool**, so upgrade-induced breakage does not exist as a raw flip count — it exists only as whatever cross-version flipping exceeds the same-version noise floor.

**判据 (deletion test).** Strip the domain nouns:
> "For a [X], *'the [event] broke it'* and *'the same [source] flipped it on resampling'* are the identical measurement applied to two partitions of the same pool, so [event]-induced change exists only as excess over the same-[source] floor."

Without *contract / model / version / sampling*, the load-bearing clause — "cross-condition change and within-condition change are the **identical operation**" — becomes **false in general**: in an arbitrary domain, a cross-condition comparison and a within-condition comparison are *different* operations against *different* baselines. The sentence is only true because here the operation (draw sample → run validator) is literally the same whether the split is by version or by sample index. The nouns are therefore load-bearing → not a bridge. (Contrast the forbidden bridge "drift detection and downstream contracts were never connected, we connect them" — that survives noun-deletion as a generic truism.)

## Step 2 — Archetype

**Primary: Measurement / audit study** (quantify a phenomenon nobody has put a defensible number on; consistent with digest N12 `empirical`). **Secondary (subordinate): Dataset** — the reusable longitudinal contract library CO3, in the spirit of [LAMDA, OpenReview:1FnCrZtBNQ], but as the measurement *instrument*, not the headline (N12 rationale).

Downstream consequences:
- **(a) Abstract contribution slot** = the numbers: a noise-adjusted per-upgrade breakage rate decomposed by contract type (CO1), the structural features that predict fragility (CO2), and the avoidable fraction under two mitigations (CO4).
- **(b) Intro logic** = "what becomes measurable / prioritizable," not "beat a baseline": teams currently learn breakage reactively from production incidents (N2); this makes the rate and its predictors knowable *before* adopting a version.
- **(c) Evidence standard** = credible measurement, not SOTA: a within-version null (M6), pre-registered thresholds, multiple model families, per-type decomposition, and archived raw outputs for recomputation — NOT a leaderboard delta.

## Step 3 — Taste self-audit

- **Bridge check.** Risk: framing as "we connect endpoint-drift detection to downstream contracts." **Fails if framed that way.** Fix (skeleton-level): the opportunity is *quantifying an unmeasured quantity* (per-upgrade breakage rate + predictors), whose null model is a non-obvious construction (same-model resampling = same operation as the upgrade comparison, Step 0). The contribution is the measurement and its null, not a connection.
- **Synthesis check.** Method reuses existing machinery (AutoIF/IFEval validators, LogProbTracking canary, LAMDA longitudinal protocol, mixed-effects logistic). **Would fail if the method were sold as the contribution.** Fix: the paper claims *measurements*, not new algorithms; the only methodological novelty is the split-half within-version noise floor as the null for cross-version breakage (M6). Reused components are stated as reused.
- **Load-bearing verb check.** Abstract opens on the mechanism/asymmetry (Step 0) with verbs from the *formalize / measure / bound / isolate* family. The "X is increasingly used… however… we introduce" template is not used. Load-bearing verbs are `formalize`, `measure`, `fit`, `bound` — not `integrate/unify/leverage`.

## Step 5 — Formal Problem Definition

**Estimand (R1, guidance.md §3.4).** The noise-adjusted excess breakage rate `ΔB(v→v′) = B(v→v′) − B_null`, per contract type — the fraction of a fixed library of production-style structured-output contracts (JSON-schema, formatting-convention, few-shot-template) that pass at a model version `v` and newly fail at the next individually-addressable version `v′`, in excess of the same-version resampling noise floor — over the reference population of production-style contracts sourced from real artifacts (SchemaStore, JSONSchemaBench, IFEval, WildChat, BFCL) and pinned open-weight/closed-API version lineages (Llama, Qwen, dated gpt-4o snapshots); this quantity, together with the M5 fragility odds ratios that predict it, is the number a production engineering team needs to prioritize regression testing before adopting a new model version (N2/CO1/CO2).

**Notation.** A contract `c = (T, D, A)`: prompt template `T`, input distribution `D`, deterministic acceptance predicate `A: output → {0,1}` (M1, M2). A lineage `L = (v_0, v_1, …, v_k)` of individually addressable versions (M3). For `(c, v)`, draw `n = 20` i.i.d. samples `{o_i}` from `v` under fixed decoding; `A` yields pass probability `p̂(c,v) = (1/n) Σ_i A(o_i)`.

| Adjective / verb (from Claims / N7) | Formal definition | How measured |
|---|---|---|
| **passes at v** | `p̂(c,v) ≥ 0.9` | 20-sample validator run (M2, M4) |
| **fails at v** | `p̂(c,v) ≤ 0.5` (band `(0.5,0.9)` = indeterminate, excluded from primary stat, swept in sensitivity) | same |
| **breaks (v→v′)** | `pass@v ∧ fail@v′` | set membership over paired runs |
| **breakage rate B(v→v′)** | `|{c: pass@v ∧ fail@v′}| / |{c: pass@v}|` | M4 |
| **fix rate F / net regression** | `F = |{fail@v ∧ pass@v′}|/|{fail@v}|`; net `= B − F` | M4 |
| **noise floor B_null(v)** | split 20 samples into two disjoint 10-sample halves `h1,h2`; run M4 between halves as pseudo-versions | M6 |
| **excess / noise-adjusted breakage ΔB** | `ΔB = B(v→v′) − B_null` | M6 vs M4 |
| **fragile / fragility predictor** | feature `f` with mixed-effects logistic odds ratio `OR(f) ` whose 95% CI excludes 1 after BH correction, sign consistent across families | M5 |
| **avoidable breakage** | `B_unmitigated − B_mitigated` on *identical* contracts, paired | M2/M3/M4, RQ3 |
| **production-style contract** | sourced from real artifacts (SchemaStore, JSONSchemaBench, IFEval-style rules, WildChat-mined templates, BFCL), not authored ad hoc | M1 provenance tag |

Every load-bearing adjective in the Claims resolves to a computable quantity above; none is left undefined.

## Assumptions (A1..A6)

- **A1 (validator construct validity).** `A` accepts exactly what a real downstream parser would accept. *Failure:* too strict inflates B, too lenient deflates it. *Detection (R2 instrument-validation sequence, guidance.md §3.4):* ① the three tiers are grounded in cited external precedent (AutoIF's executable-verification discipline, IFEval's rule set) rather than invented; ② validators unit-tested and refined against a held-out calibration set of hand-built positive/negative example outputs, with the strict/lenient boundary (e.g., trailing prose around a JSON block) as a named, swept design constant; ③ acceptance threshold is validator-vs-hand-label agreement ≥ 0.95 on that calibration set; ④ disagreements are inspected for confusion structure (must cluster on the pre-registered indeterminate band `(0.5, 0.9)`, not scatter — a systematic collapse would itself fail the gate); ⑤ frozen before any measurement run. *Gate:* PG-1 (walking skeleton; pass criterion (i) in Step 9). *Consequence:* if validator agreement < 0.95, or disagreements do not cluster on the indeterminate band, the skeleton fails outright and every downstream H\* is blocked — no RQ is scored on an uncalibrated validator.
- **A2 (noise floor is a valid null).** Within-version split-half resampling captures the same-source flip confound that cross-version comparison must exceed. *Failure:* if serving nondeterminism is non-exchangeable across time, split-half underestimates the floor. *Detection:* interleave the two halves in collection order; compare split-half B_null to a temporal-half B_null; skeleton computes both. *Gate:* PG-2 (walking skeleton; pass criterion (ii)). *Consequence:* if split-half and temporal-half B_null diverge materially, RQ1/RQ2/RQ3 all degrade to the temporal-half floor as the conservative null (Part 4 situation 1 discipline — an invalid null blocks scoring, it is not silently averaged away).
- **A3 (version addressability & stability).** Each `v` is individually re-queryable and stable during its collection window. *Failure:* silent within-snapshot change on closed endpoints. *Detection:* LogProbTracking-style first-token top-k logprob canary beside every batch (M3); affected batches re-collected; primary claims anchored on open-weight checkpoints where A3 holds by construction (N6 feasibility). *Gate:* continuous, every collection batch (M3), not a one-time pilot check. *Consequence:* a canary-flagged closed-API batch is re-collected before scoring; if re-collection is impossible (snapshot deprecated), that transition is dropped from the closed-API secondary arm and never promoted to a primary (open-weight) claim — RQ1/RQ3 headline numbers restrict to open-weight lineages only.
- **A4 (contract representativeness).** The library proxies real production contract mix. *Failure:* skewed genre mix biases the pooled rate. *Detection:* report B per source/genre, never pooled-only (t3); provenance recorded per contract. *Gate:* Stage-2 library-construction freeze (M1), before any version is queried. *Consequence:* RQ1's pooled ΔB is always reported alongside its per-genre decomposition; a pooled claim without the per-genre breakdown is not licensed even if the pooled number is significant.
- **A5 (statistical power).** Enough independent transitions × contract diversity for the RQ2 feature model. *Failure:* underpowered ORs. *Detection:* a-priori power analysis (N8: ~3000 contracts × ≥10 transitions → ≥0.8 power for OR=1.3); pilot gate checks realized pass@v counts against the power assumption before scale-up. *Gate:* PG-5, pre-scale-up (between Stage 1 pilot and Stage 2). *Consequence:* any (transition × contract-type) cell realized below the powered-n target is pre-declared **INCONCLUSIVE** and excluded from RQ2's headline tally rather than folded into a null (guidance.md Part 4 situation 5; see the pre-declaration paragraph opening Step 6 below).
- **A6 (feature measurability & decorrelation).** The 7-feature M1 vector is mechanically computable and depth/constraint-count are decorrelated by stratified sampling. *Failure:* collinearity makes ORs uninterpretable. *Detection:* report VIFs; stratified joint-grid sampling of schemas (M1); drop/merge features with VIF > 5 pre-registered. *Gate:* Stage-2 model-fitting time, before Wald tests are read (M5). *Consequence:* any feature with VIF > 5 is dropped/merged per the pre-registered rule *before* RQ2 is scored, never post-hoc after seeing which features look significant.

### Confound Ledger (R3, guidance.md §3.4)

Every design constraint above exists to remove one named confound, stated explicitly rather than left implicit in the Assumptions' *Detection* clauses:

- Temperature-0 primary arm + n = 20 samples per (contract, version) removes confound: ordinary sampling/serving stochasticity being misattributed to the version change (A2).
- The split-half noise floor computed by the identical M4 pipeline (not a separately-modeled or externally-sourced null) removes confound: using two different measurement procedures for the cross-version and within-version arms, which would make "excess over noise" incomparable by construction (A2).
- The LogProbTracking-style canary running beside every collection batch removes confound: silent within-snapshot serving changes on closed endpoints being attributed to the named version transition instead of to an uncontrolled mid-collection change (A3).
- Anchoring primary claims on open-weight lineages (vs. closed dated snapshots) removes confound: closed-API deprecation or silent drift making a specific "version N → N+1" comparison irreproducible after the fact (A3, t5).
- Stratified joint-grid sampling of schemas across the feature space (M1) removes confound: schema nesting depth and constraint count being naturally correlated, which would make per-feature odds ratios in RQ2 uninterpretable (A6).
- Benjamini–Hochberg correction across every (transition × contract-type) cell removes confound: multiple-comparison inflation manufacturing a "significant" fragility feature or breakage transition by chance (A5, RQ1/RQ2 Verification).
- Grouped 5-fold CV and leave-one-family-out evaluation by contract family (M5) removes confound: near-duplicate contracts straddling train/test folds inflating the fragility model's apparent predictive AUC (A5/A6).

## Step 6 — Pre-Registered Experiments

**Power / INCONCLUSIVE pre-declaration (guidance.md Part 4 situation 5; Part 6 item 9).** Before any test is scored: any (transition × contract-type) cell whose realized sample falls short of the power target for its hypothesis's effect floor — RQ1: powered to distinguish `B = 5%` from `B_null = 1%`; RQ2: powered for `OR = 1.3` at ≥0.8 — is pre-declared **INCONCLUSIVE**, reported separately, and excluded from the headline PASS/FAIL tally. An INCONCLUSIVE cell is never folded into a null verdict (that would silently misreport "no effect" where the honest statement is "underpowered to tell"), never silently dropped from the reported table, and never used to inflate the denominator of a per-type or pooled rate. If the *central* test (the pooled RQ1 test across open-weight transitions) is itself underpowered at realized scale, the options are, in order: collect more transitions (config-only extension), narrow the claim to the powered cells only, or stop before Phase B/C scale-up — never silently report the underpowered pooled estimate as if it were conclusive.

### RQ1 — How many contracts break per upgrade? (digest N8 RQ1; tests CO1)
- **Assumption:** A1, A2, A3, A4.
- **Hypothesis (binary).** On the open-weight anchor lineages, for **≥ 50% of tested version transitions**, `B(v→v′)` exceeds `B_null` by a BH-corrected paired-permutation test (α = 0.05), **and** the pooled point estimate `ΔB ≥ 3 percentage points`; **and** strict-envelope types break more than templates: `ΔB_schema > ΔB_template` and `ΔB_convention > ΔB_template`.
- **Metric.** `B(v→v′)`, `F`, net regression, `ΔB = B − B_null`, per contract type (N8 metrics).
- **Verification.** Per transition: two-sided paired-permutation test of `B` vs `B_null` over contracts; Benjamini–Hochberg across all (transition × type) cells; α = 0.05. Sizing: n = 300 pilot gives > 0.9 power to separate B = 5% from B_null = 1% (N8); scale-up n ≈ 3000.
- **Fallback.** If criterion fails: report a **noise-adjusted upper bound** — "per-upgrade contract breakage is bounded below [X]% and statistically indistinguishable from within-version sampling noise across the tested lineages; structured-output contracts are more upgrade-robust than the drift-detection literature implies," which is a publishable calibration null (feeds F-G1).

### RQ2 — Which contract features are most fragile? (digest N8 RQ2; tests CO2)
- **Assumption:** A5, A6, and RQ1's phenomenon existing (else fragility is undefined).
- **Hypothesis (binary).** In the mixed-effects logistic model (M5): **at least one of {schema nesting depth, constraint density} has OR ≥ 1.3 with 95% CI excluding 1 after BH**, few-shot example count has `OR < 1` (protective), **and** leave-one-family-out predictive `ROC-AUC ≥ 0.65`.
- **Metric.** Odds ratios + 95% CIs; grouped-5-fold and leave-one-family-out AUC (N8 metrics).
- **Verification.** Pre-registered 7-feature list frozen before collection; Wald tests, BH-corrected, α = 0.05; grouped CV by contract family so near-duplicates never straddle folds; power ≥ 0.8 for OR = 1.3 at scale (N8).
- **Fallback.** If no feature is significant or out-of-family AUC ≈ 0.5: claim "**fragility is not predictable from static structural features**; upgrade regression testing cannot be prioritized by contract structure and must be treated as exhaustive" — an actionable negative result.

### RQ3 — How much breakage is avoidable? (digest N8 RQ3; tests CO4)
- **Assumption:** A1, A2, A3.
- **Hypothesis (binary).** On the open-weight chains: (a) grammar-constrained decoding removes **≥ 90% of schema-tier breakage**; (b) per-version prompt recompilation (DSPy-style) yields a **≥ 25% relative reduction in total `B(v→v′)`**, significant by paired test on identical contracts (α = 0.05).
- **Metric.** `B_mitigated` vs `B_unmitigated`, per tier, paired over identical contracts.
- **Verification.** Paired-permutation test per arm vs unmitigated, BH across arms × transitions, α = 0.05.
- **Fallback.** If no significant reduction: claim "measured breakage is **dominated by failure modes unreachable by decoding guarantees or prompt re-optimization**," reframing breakage as an inherent, non-deployment-fixable upgrade cost.

### Mandatory baselines
- **B0 — "why do this at all" / no-mechanism control.** The within-version split-half arm (M6, B_null): the exact same pipeline with **no upgrade applied**. If `B(v→v′)` is not distinguishable from B0, the phenomenon does not exist and the study's premise fails. This is the null every RQ1 claim is tested against.
- **B-alt — strongest-alternative-explanation control (budget-matched).** Rival explanation: *"contract breakage is just generic, cheaply-detectable distribution shift — a $0.01 first-token logprob detector already predicts it, so the expensive contract library adds nothing."* Arm: run the LogProbTracking-style first-token top-k logprob two-sample detector on the same (contract, version) pairs and test whether its shift signal predicts contract-level breakage (AUC). The claimed cause (contract-specific fragility) is isolated iff the cheap detector's breakage-prediction AUC is **materially below** the M5 structural model's (pre-registered gap ≥ 0.10 AUC) — i.e., breakage carries contract-specific structure the cheap signal misses. Net-regression (`B − F`) additionally controls the rival "the new version is just globally worse," not contract-specifically broken.

### Global fallback F-G1
If the central hypothesis family fails (RQ1 null AND RQ2 null), pivot archetype from *measurement-of-a-fragility-phenomenon* to *robustness-audit / calibration null*. Pivoted abstract sentence: **"Contrary to the prevailing assumption that provider model upgrades silently break downstream structured-output contracts, we measure per-upgrade breakage across three model families and find it statistically indistinguishable from within-version sampling noise, establishing an empirical upper bound and reframing model-version regression testing as a low-priority engineering activity."**

## Step 9 — Walking Skeleton

- **Binary question:** On a single open-weight transition, is `B(v→v′) > B_null` at p < 0.05?
- **Arms (2):** (1) cross-version `B(v→v′)`; (2) within-version split-half `B_null` (B0).
- **Task set (smallest):** 30 contracts (10 schema / 10 convention / 10 template) × one lineage, two adjacent open-weight versions (e.g. Qwen2.5 → Qwen3).
- **Deterministic metrics only:** validator pass/fail (M2), `p̂`, `B`, `B_null`, paired-permutation p-value. No human scoring.
- **Cost / wall-clock:** 30 × 2 versions × 20 samples = 1,200 local vLLM requests, < 1 GPU-hour, minutes of compute; ~1 engineering-day including validator unit tests.
- **Pass criterion → scaling is config, not code:** skeleton passes when (i) validators agree ≥ 0.95 with hand labels (A1 gate), (ii) both B and B_null compute end-to-end through the identical pipeline, (iii) the paired-permutation test emits a p-value. At that point scaling to 3,000 contracts × 3 families × ≥10 transitions changes only the contract list, version list, and family list — no new code path (validators, breakage computation, permutation test, canary all identical).

## Claim–Evidence Map

| Claim the final abstract will make | Traces to | Status |
|---|---|---|
| Per-upgrade breakage exists in excess of within-version noise | H-RQ1, Step-5 `ΔB`, B0 | needs-experiment; fallback-covered (upper-bound null) |
| Breakage decomposes by contract type (strict > template) | H-RQ1 (type clause) | needs-experiment |
| Structural features predict fragility | H-RQ2, Step-5 fragility predictor, B-alt | needs-experiment; fallback-covered (unpredictable null) |
| Breakage is only meaningful vs a reported noise floor | Step-0 asymmetry, Step-5 `B_null`, M6 | supported-by-design |
| A measurable fraction of breakage is avoidable | H-RQ3, Step-5 avoidable breakage | needs-experiment; fallback-covered (inherent-cost reframe) |
| A reusable longitudinal contract library (CO3) | M1–M3, N11 artifact commitment | supported-by-design |
| Cheap distribution-shift signals do not fully explain breakage | B-alt (AUC gap ≥ 0.10) | needs-experiment |

## Abstract v0 (draft, mechanism-first — DRAFT BEFORE RESULTS)

> A structured-output contract fixes its acceptance predicate but delegates the behavior that must satisfy it to a model version the contract owner cannot pin or observe, so whether the contract still passes after a provider upgrade is decided outside the contract. We formalize per-upgrade contract breakage as the excess of cross-version pass→fail flipping over the same model's within-version resampling noise floor — the identical pass/fail measurement applied to two partitions of the outputs — and measure it across successive versions of three model families over a library of production-style contracts (JSON-schema, formatting-convention, and few-shot-template), each carrying a deterministic validator. We fit a mixed-effects model relating contract structure (schema depth, constraint density, few-shot count) to breakage odds, isolate contract-specific fragility from cheap distribution-shift signals, and bound the avoidable fraction via constrained decoding and per-version prompt recompilation. We report noise-adjusted breakage rates by contract type and the structural features that predict fragility.

*(~150 words; opens on the Step-0 asymmetry, verbs `formalize / measure / fit / isolate / bound`; no "increasingly used… however… we introduce" template.)*
