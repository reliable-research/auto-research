# Capability, Policy, or Format? Decomposing Behavioral Drift across LLM Version Pairs — Pre-Registered Paper Specification

> Generated from digest.md + README.md. Status: specification, no experiments run.
> All ids (C1.., M1.., CO.., RQ..) refer to digest.md. Nothing here contradicts the digest; where the digest gives a statistical plan, this spec hardens it into binary pre-registered criteria.

## Step 0 — Core Asymmetry (升维)

**The sentence.** In black-box LLM auditing, the model's output text is simultaneously the sole measurement channel and itself an object of vendor change: capability and policy updates alter *what the model computes*, while format updates alter *the channel every score must pass through* — so an un-instrumented audit can misread format drift as capability or policy drift, but never the reverse, and drift decomposition becomes identifiable exactly by exploiting this one-directional confounding (freeze the channel with format-invariant scoring; what remains is content change).

**判据 (deletion test).** Delete the domain nouns (LLM, output text, capability, policy, format):

> "In black-box auditing, *something* is simultaneously the sole measurement channel and itself an object of change: some updates alter what is computed, while others alter the channel — so audits can misread one kind of drift as another, but never the reverse."

Without the domain nouns this is FALSE as a generic statement: in general measurement systems, channel confounds and content confounds run in *both* directions, and "never the reverse" has no support. The asymmetry holds only because LLM text is the carrier of every black-box measurement while task content does not contaminate surface-feature scores (a wrong answer does not change markdown density; added markdown fences do change executability checks — the documented incident in [ChatGPTBehavior, arXiv:2307.09009], digest N4). The sentence is not a bridge: it states a directionality of confounding, not a connection between two fields.

## Step 2 — Archetype

**Primary: `empirical`** (measurement/attribution finding), per digest N12. **Secondary: technical artifact** — the calibrated decomposition instrument (CO2) and the released battery + cached corpus (CO4) are supporting deliverables, not the headline.

Downstream consequences:
- **(a) Abstract contribution slot**: a *measured finding* — per-pair axis shares with leakage/noise accounting (RQ1) and the cross-vendor structure verdict (RQ_INF_1) — plus one instrument claim: calibration accuracy on control pairs (RQ_INF_2).
- **(b) Intro logic**: "what becomes possible" — axis-resolved drift reports let integrators triage (format → fix parsers; capability → re-benchmark; policy → re-review compliance) instead of full requalification (digest N2, [CARLoRA]). NOT "we beat a number": there is no leaderboard here.
- **(c) Evidence standard for results**: calibration-gated attribution. No real-pair decomposition may be interpreted unless the blind control-pair recovery gate (H3) passes first; all attributions carry bootstrap CIs, permutation-based nulls, and an explicit leakage share; cross-vendor claims are graded (W with CI), never binary prose.

## Step 3 — Taste self-audit

| Check | Verdict | Evidence |
|---|---|---|
| Is the opportunity a Bridge ("drift auditing meets variance decomposition")? | **PASS (not a bridge)** | The framing is an identifiability asymmetry (Step 0): format acts on the measurement channel, content changes do not act on format scores. The decomposition is a *consequence* of the asymmetry, not a stapling of two fields. |
| Is the method mere Synthesis (existing benchmarks + a mixed model)? | **PASS after sharpening** | The load-bearing mechanism is NOT the mixed model; it is (i) orthogonality turned from an assumption into a *measured bound* — explicit leakage term (M4) + blind dominant-axis recovery on constructed control pairs with axis known by construction (M6) — and (ii) the null-pair placebo arm (B-alt below), which no prior drift audit runs. Benchmarks are commodity inputs. |
| Load-bearing verbs from integrate/unify/leverage family? | **PASS** | The claims use: *decompose, isolate, freeze, calibrate, bound, gate, recover, falsify*. No "leverage/unify/integrate/combine" anywhere in Claims 1–5 (digest) or Abstract v0. |
| Abstract opening rule ("X is increasingly used… however… we introduce" FORBIDDEN) | **PASS** | Abstract v0 opens with the misattribution mechanism (one-directional confounding), first verb family: *misread / isolate / calibrate*. |

No framing repair needed beyond the Synthesis sharpening recorded above (which is now the canonical framing: the contribution is a *calibrated instrument + finding*, not a pipeline).

## Step 5 — Formal Problem Definition

**Estimand (guidance.md R1).** The quantity of interest is the vector of axis shares `(η²_cap(P), η²_pol(P), η²_fmt(P), λ(P))` — the fraction of a same-provider LLM version pair's measured behavioral delta attributable to capability, policy, and format change respectively, plus unresolved cross-axis leakage — with `P` (one version pair) as the unit of analysis, the reference population being snapshot-pinned commercial and open-weight version pairs currently simultaneously servable across ≥3 vendors, and the decision it feeds being whether a downstream integrator should re-benchmark, re-audit for policy compliance, or merely patch a parser after a given version bump (digest N2).

**Notation.** A version pair `P = (v_old, v_new)`, same provider, both black-box (text-in/text-out only, C2). Probe batteries `a ∈ {cap, pol, fmt}` (M1, M2, M3), items `i ∈ I_a`, `k = 5` samples per item per version at fixed decoding settings. For item `i`, per-sample score `s(v, i, r)`, `r = 1..k`; per-item behavioral delta `Δ_i = mean_r s(v_new,i,r) − mean_r s(v_old,i,r)`.

- **Noise floor** `σ²_w(P)`: within-version run-to-run variance of `s(v,i,·)`, pooled over items and both versions.
- **Axis share** `η²_a(P)`: proportion of between-version variance in `{Δ_i}` attributed to battery `a` by the mixed-effects model M4 (axis fixed effect, item random effect), counted only in excess of `σ²_w(P)`.
- **Leakage share** `λ(P)`: proportion of capability/policy per-item deltas explained by cross-axis regression on that item's format-feature deltas (and policy deltas on lexical surface cues); reassigned to a reported leakage term, never absorbed (M4).
- **Format drift** `D_fmt(P)`: L2 norm of the standardized per-feature mean-difference vector over M3's features (length, markdown density, list-vs-prose rate, hedging frequency, JSON compliance, refusal boilerplate).
- **Dominant axis** `dom(P) = argmax_a η²_a(P)`; **recovery accuracy** `Acc = (1/n) Σ_controls 1[dom(P_c) = axis built into P_c]` (M6).
- **Cross-vendor agreement**: Kendall's `W` over per-vendor rank orderings of axis dominance across pairs, with a 10,000-draw permutation null (M5).

**Adjective audit** (every load-bearing adjective in digest Claims → computable quantity):

| Adjective/verb | Formal definition | Measured by |
|---|---|---|
| "orthogonal" (probes) | `λ(P) < 0.15` on control pairs AND scorer output invariant under synthetic format perturbations (≥99% unchanged scores) | M4 leakage regression + A3 perturbation audit |
| "drift" (vs noise) | axis contribution exceeds `σ²_w(P)` at permutation `p < 0.01` | M4 + E1 procedure |
| "non-negligible" (format share, Claim 3) | `η²_fmt(P) ≥ 0.10` of explained drift | E1 |
| "calibrated" (Claim 1, 4) | `Acc ≥ 8/9` blind recovery AND mean `λ < 0.15` on controls | E3 |
| "common structure" (Claim 2) | Kendall's `W ≥ 0.60` with permutation `p < 0.05` over ≥6 pairs, ≥3 vendors | E2 |
| "black-box" | only text I/O used; no logits, weights, training data at any pipeline stage (decision procedure: code audit of pipeline inputs) | design invariant |
| "separately-measurable" (Claim 1) | ≥2 axes distinguishable above noise floor in the same pair | E1 |

Deleted adjectives: "more useful" (Claim 5) is not experimentally defined here — demoted to argued motivation only (see Claim–Evidence Map).

## Assumptions (A1–A8)

| Id | Assumption | How it could fail | Detection (gate) |
|---|---|---|---|
| A1 | Snapshot-pinned endpoints serve a fixed model over the study window | silent server-side change mid-study | **PG-1**: both versions queried in interleaved windows; early-half vs late-half noise-floor comparison per version; flag if between-window variance > 2× within-window (t2) |
| A2 | k=5 repeats at fixed decoding estimate the within-version variance floor | heavy-tailed nondeterminism (infra) | **PG-2**: skeleton check: `σ²_w` from k=3 subset within 20% of k=5 estimate; else raise k |
| A3 | Format-robust scorers (M1) are invariant to surface form | extractor breaks on unseen formatting | **PG-3**: perturbation audit: apply synthetic transforms (fence-wrapping, verbosity padding, markdown injection) to fixed responses; scores must be unchanged on ≥99% of items — walking-skeleton gate |
| A4 | LLM judge's 3-way refusal classification (M2) tracks human judgment | judge is style-biased ([WildBench] bias evidence) | **PG-4**: 600-item human validation; gate: Cohen's κ ≥ 0.70; else fall back to keyword/regex classifier + human adjudication of disagreements. Full R2 instrument-validation sequence for this judge: ① categories grounded in the stratification's own source taxonomies (XSTest safe/unsafe, OR-Bench-Hard pseudo-harmful, SORRY-Bench harmful) rather than invented labels; ② the comply/refuse/redirect-hedge rubric is drafted wide and refined on a held-out 100-item calibration slice disjoint from the 600-item validation set, with any merge/split of the 3 labels named explicitly if confusion is high; ③ validated against ≥2 independent human raters on the 600-item held-out sample, κ ≥ 0.70 required per rater-pair; ④ confusion matrix inspected — pass requires disagreements to concentrate on adjacent categories (comply↔redirect-hedge), not a systematic refuse↔comply collapse; ⑤ rubric and thresholds hashed/frozen before the k=5, 6-pair scale-up run. |
| A5 | Constructed control pairs (M6) span the kinds of change vendors ship | vendor updates are mechanistically unlike SFT/safety-tune/template changes (C4, C2) | not directly detectable (unaddressed challenge C2); mitigated by ≥3 construction recipes per axis; scope-limited in claims (Claim 4 wording) |
| A6 | ≥6 real pairs from ≥3 vendors have both snapshots simultaneously served | deprecation mid-study (N6 top feasibility risk) | **PG-5**: day-0 availability audit; all raw outputs cached immediately at study start (CO4); open-weight anchor pairs guarantee ≥2 pairs survive |
| A7 | A near-ceiling shared-correct prompt set exists for M3 | no items where both versions ≥95% correct | **PG-6**: pre-pass gate before M3; if <300 items survive, backfill from easier pools until 500 reached |
| A8 | Each axis-pair test cell (6 pairs × 3 axes for H1; 9 control pairs for H3) has enough items/repeats for ≥0.9 power to detect the pre-registered effect floor (η²≥0.10 for format share, λ<0.15 for leakage) at α=0.01 (Holm–Bonferroni-corrected) | a cell's per-item variance is higher than the ~3,000-item/k=5 design assumed, so the realized power falls below 0.9 | **PG-7**: power recomputed per cell from the pilot's observed per-item variance (walking skeleton, n=400/k=3) before the k=5 scale-up; minimum n per cell fixed at the pilot-recomputed value (never reduced to raise a headline count); any cell whose recomputed power is <0.9 is pre-declared **INCONCLUSIVE** for H1/H2/H3 scoring — never reported as a null and never dropped silently from the per-pair denominator (mirrors the B6.3 A6 worked instance in guidance.md §3.2) |

## Step 6 — Pre-Registered Experiments

**Gating order:** E3 (calibration) must pass before E1/E2 results are interpreted; B-alt (null pairs) runs alongside E1. This ordering is pre-registered and matches digest N9 ("Result 3 gates the other two").

### E3 — Calibration on control pairs (RQ_INF_2; runs FIRST)

- **Assumption:** A2, A3, A4, A7, A8.
- **Hypothesis H3 (binary):** Blind dominant-axis recovery on ≥9 constructed control pairs (3 per axis, M6) achieves **≥ 8/9 correct** (exact binomial vs p₀ = 1/3: p ≈ 0.0009) **AND** mean leakage share `λ < 0.15`. **Power/INCONCLUSIVE (A8/PG-7):** if the pilot-recomputed per-cell power for detecting `λ<0.15` is <0.9 for a given axis's 3 control pairs, that axis's contribution to Acc is reported as INCONCLUSIVE rather than scored pass/fail, and the ≥8/9 bar is then evaluated only over the powered axes with the reduced denominator stated explicitly.
- **Metric:** `Acc` and `λ` as defined in Step 5.
- **Verification:** exact binomial test against chance 1/3, α = 0.05, n = 9, one-sided; pipeline runs without axis labels (analyst-blind: decomposition code receives shuffled pair ids); leakage from M4's cross-axis regression, bootstrap CI (1,000 item resamples).
- **Fallback (pre-committed wording):** If 6–7/9: *"The instrument is partially calibrated: dominant-axis recovery exceeds chance (x/9, p = …) but not the pre-registered bar; real-pair results are therefore reported as dominant-axis calls with widened uncertainty, and per-axis percentage shares are demoted to exploratory."* If ≤ 5/9 or `λ ≥` largest axis share: instrument invalid → **F-G1**.

### E1 — Axis decomposition of real version pairs (RQ1)

- **Assumption:** A1, A2, A3, A4, A6, A8; gated by H3.
- **Hypothesis H1 (binary):** In **≥ 4 of 6** real version pairs, **≥ 2 of 3** axes exceed the noise floor (permutation p < 0.01, Holm–Bonferroni over the 6 × 3 = 18-test family) **AND** format share `η²_fmt ≥ 0.10` of explained drift in **≥ 3 of 6** pairs. **Power/INCONCLUSIVE (A8/PG-7):** any of the 18 axis-pair cells whose pilot-recomputed power is <0.9 is excluded from both the numerator and denominator of the "≥4 of 6" / "≥3 of 6" counts and reported separately as INCONCLUSIVE (never as a pass, fail, or silent drop).
- **Metric:** `η²_a(P)`, `λ(P)`, `σ²_w(P)` (Step 5; digest N8 metrics). ~3,000 items × 2 versions × 5 repeats per pair.
- **Verification:** per axis-pair cell, permutation test of axis contribution against noise floor (10,000 label permutations), α = 0.01, Holm–Bonferroni across the 18-cell family; 1,000-resample bootstrap CIs on all shares; per-pair reporting, no pooling (t4).
- **Fallback (pre-committed wording):** (i) If decomposition binds but `η²_fmt < 0.10` everywhere: *"Once scoring is made format-invariant, format drift contributes negligibly (<10%) to measured version-pair drift; the widely-feared format confound is a scoring artifact, not a behavioral axis — blended audits need format-robust extractors, not a third axis."* (still supports CO1/CO2; contradicts Claim 3 and we say so). (ii) If leakage + noise absorb the majority of drift in most pairs: the decomposition fails to bind → **F-G1**.

### E2 — Cross-vendor structure (RQ_INF_1)

- **Assumption:** A1, A5, A6; gated by H3 and by E1 binding.
- **Hypothesis H2 (binary):** Kendall's `W` over axis-dominance rank orderings across ≥ 6 pairs from ≥ 3 vendors satisfies **W ≥ 0.60 AND permutation p < 0.05** (10,000 draws); secondary consistency check: vendor-labeled clustering silhouette NOT significant vs label-permuted null.
- **Metric:** Kendall's `W`; silhouette score on the axis-share 3-simplex (M5).
- **Verification:** permutation null for W; silhouette permutation test; both reported with CIs; small-n caveat pre-registered (t4) — claim stated as graded evidence.
- **Fallback (pre-committed wording):** *"Drift structure is vendor-idiosyncratic: axis-dominance orderings do not agree across vendors (W = …, p ≥ 0.05) and/or pairs cluster by vendor; longitudinal audits therefore cannot assume a shared cross-vendor taxonomy and must be calibrated per vendor."* This is a full publishable answer to CO3 (the seed question is two-sided by construction).

### Mechanism analysis (guidance.md R6; ≥1 required beyond the headline tests)

**M7 — Feature-level leakage attribution.** For every pair whose leakage share `λ(P)` clears a reportability threshold (`λ ≥ 0.05`), rank the M3 surface features (length, markdown density, list-vs-prose rate, hedging frequency, JSON-schema compliance, refusal-boilerplate rate) by the standardized regression coefficient magnitude from M4's cross-axis regression (Step 5), analogous to guidance.md R6's enrichment-ranking pattern. This answers *why* leakage occurs, not just *how much*: e.g., a pair whose leakage is dominated by markdown-density coefficients supports the Claim-3 mechanism (format inflating an apparent capability/policy delta) directly, while a pair dominated by hedging-frequency coefficients would instead implicate lexical policy-adjacent style rather than pure formatting — a distinction the headline `η²`/`λ` numbers alone cannot make. **Pre-registered reporting rule:** the top-2 features by coefficient magnitude are named per pair in the results table (not just the aggregate `λ`); if the top feature differs from markdown density/length in a majority of leaky pairs, Claim 3's mechanism narrows explicitly to "a specific non-length surface dimension" rather than "format" generically, and the abstract's wording is adjusted to match at splice time (Phase D).

### Mandatory baselines

- **B0 — "why do this at all" control: the blended-delta audit.** Exactly the [ChatGPTBehavior, arXiv:2307.09009] design (digest N8 baselines): one blended per-task delta per pair, no format-robust scoring, no noise floor, no decomposition. Run on the M6 *format-only* control pairs. **Pre-registered demonstration:** B0 reports a nonzero "performance change" (|delta| > its own bootstrap CI) on ≥ 2/3 format-only controls — i.e., the standard audit misattributes pure format drift as capability/policy change — while our pipeline attributes those same pairs to format. If B0 does NOT misattribute, the problem's practical motivation is weakened and Claim 3's motivation is downgraded from "documented mechanism" to "hypothetical"; we pre-commit to reporting this.
- **B-alt — strongest-alternative-explanation control: null-pair placebo.** **Rival explanation:** measured "axis shares" are artifacts of probe-battery composition, pipeline choices, and within-version nondeterminism — not model change at all (C5). **Arm:** for each vendor, one *fake pair* — the same snapshot queried in two disjoint interleaved time windows — run through the identical full pipeline at identical item/repeat budget (budget- and capability-matched by construction: it IS the same model). **Pre-registered criterion:** on every null pair, all three axis shares must be statistically indistinguishable from the noise floor (permutation p ≥ 0.01 after correction). Any null-pair axis "detection" is subtracted as a bias term and reported; ≥ 2 null-pair detections across 3 vendors invalidates E1's positive findings pending diagnosis. Additionally, the **two-way ablation** (capability+policy, no format axis; digest N8 baselines) runs on the control pairs to show the third axis is load-bearing: two-way recovery accuracy on format-only controls must be ≤ 1/3 (it has no correct label available) while three-way recovery passes H3.

### Global fallback F-G1 — archetype pivot

If the central hypothesis family fails (H3 ≤ 5/9, or E1 leakage+noise dominance), the paper pivots from `empirical finding` to `negative result / measurement critique`, keeping the same data. **Pivoted abstract sentence (pre-committed):** *"We show that capability/policy/format attribution of LLM version drift is not identifiable from black-box behavior at practical probe budgets: even on control pairs whose dominant change axis is known by construction, blind recovery fails (x/9), placing a measured lower bound on the entanglement that every published longitudinal audit implicitly claims to see through."* All raw outputs, batteries, and control recipes still release (CO4), and the calibration protocol itself remains the reusable contribution.

## Step 9 — Walking Skeleton

**The ONE binary question:** *Does the end-to-end pipeline, run blind on one control pair per axis, recover the dominant axis 3/3 while a null pair yields no detection?*

- **Arms (4):** (1) capability control: Qwen2.5-7B-Instruct vs same + math-SFT; (2) policy control: same base vs safety-SFT (recipe per [ContrastiveOverRefusal]-style tuning, M6); (3) format control: identical weights, style-forcing system template; (4) null pair: identical weights, identical template, two runs.
- **Smallest task set:** 400 items total — 150 capability (50 GSM8K / 50 MMLU-Pro / 50 HumanEval), 150 policy (50 per stratum: XSTest-safe / OR-Bench-Hard / SORRY-Bench), 100 format (near-ceiling pre-passed + IFEval subset); k = 3.
- **Deterministic metrics only:** execution-based accuracy, normalized exact match, regex/keyword refusal classifier (LLM judge deferred to full run; A4 validated later), format feature vector norms. No LLM-judge, no API dependency.
- **Cost:** 400 items × 2 versions × 3 repeats × 4 arms ≈ 9,600 generations + 2 short SFT runs on a 7B model. One A100 (vLLM), ≈ 15–20 GPU-hours, ≤ 2 days wall-clock, ~$0 API spend.
- **Pass criterion (explicit):** dominant-axis recovery **3/3** AND null-pair axis shares all below noise floor AND A2's k-stability check AND A3's scorer perturbation audit ≥ 99%. **Skeleton passed ⇒ scaling is a config change:** the full study only enlarges `I_a` (400 → 3,000), `k` (3 → 5), control pairs (3 → 9), and adds API endpoints and the validated judge — no new code paths, same M4/M5 analysis scripts run unchanged on the larger tables.

## Claim–Evidence Map

| Claim (digest Claims section) | Traces to | Status |
|---|---|---|
| Claim 1 — drift decomposable into three measurable sources with quantified leakage/noise bounds | H3 (calibration) + H1 (≥2 axes above floor); "measurable/calibrated/orthogonal" defined in Step 5 | needs-experiment; fallback-covered (E3/E1 fallbacks, F-G1) |
| Claim 2 — common cross-vendor structure | H2 (W ≥ 0.60, p < 0.05) | needs-experiment; fallback-covered (E2 fallback is the equally publishable idiosyncrasy finding) |
| Claim 3 — ≥10% of blended drift is format alone | H1 clause 2 (`η²_fmt ≥ 0.10` in ≥3/6 pairs) + B0 misattribution demonstration | needs-experiment; fallback-covered (E1 fallback (i) reverses it explicitly) |
| Claim 4 — attribution for commercial pairs is calibrated behavioral inference, never internally verified | supported-by-design: follows from C2 (unaddressed) + E3's calibration bound; wording pre-committed in E3/A5 | supported-by-design |
| Claim 5 — axis-resolved reports are operationally more useful than blended deltas | argued motivation only ([CARLoRA] breakage evidence); "more useful" deleted from measurable claims (Step 5) | supported-by-design (argument), explicitly NOT an experimental claim |

## Abstract v0 (draft, mechanism-first)

> **DRAFT — BEFORE RESULTS. Numbers are pre-registered targets, not findings.**

In black-box LLM auditing, output text is both the sole measurement channel and itself a target of vendor change — so audits misread format drift as capability or policy change, but never the reverse. We exploit this one-directional confounding to decompose version-pair behavioral drift into three sources: capability, policy, and format. Three probe batteries each freeze two axes by construction (format-invariant scoring; near-ceiling prompts); a mixed-effects model apportions drift with an explicit leakage term and a repeated-run noise floor; null pairs (a version against itself) bound pipeline artifacts. We calibrate the instrument on open-weight control pairs whose dominant change axis is known by construction, gating all attribution on blind recovery accuracy. Applied to version pairs from three vendors, the decomposition tests whether drift structure is industry-shared or vendor-idiosyncratic, and whether format drift — invisible to blended audits — carries a non-negligible share of what is reported as capability change.
