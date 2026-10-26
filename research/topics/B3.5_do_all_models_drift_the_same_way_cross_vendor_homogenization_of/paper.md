# Do All Models Drift the Same Way? Cross-Vendor Homogenization of Behavioral Change — Pre-Registered Paper Specification

> Generated from digest.md + README.md. Status: specification, no experiments run.
> All thresholds below are pre-registered and hard-coded before any data collection.

## Step 0 — Core Asymmetry (升维)

**Asymmetry sentence:**

> Because every LLM vendor is pulled toward the same trivial attractor — higher capability — raw agreement in how their models change is uninformative; the invariant is that under genuinely independent pipelines the *capability-orthogonal* components of inter-version drift (refusal posture, sycophancy, stance) are **exchangeable across vendors**, so excess drift-vector correlation on those components is a one-way signature that independent development cannot produce but shared training inputs / alignment recipes cannot fully suppress.

**判据 (deletion test).** Delete the domain nouns:

> "Because every ___ is pulled toward the same trivial attractor, raw agreement in how ___ change is uninformative; under independent ___ the orthogonal components of ___ are exchangeable, so excess correlation is a one-way signature of shared ___."

Without the domain nouns the sentence is **empty and, read generically, false**: the generic claim "correlation implies sharing" fails in general *precisely because* common attractors exist — the sentence only becomes true once "capability" names the attractor to be projected out and "refusal/sycophancy/stance" name the components on which exchangeability is the correct independence null (digest C2, C5). It is not a bridge: it does not connect two fields, it states which component of an observable is invariant under the independence hypothesis.

## Step 2 — Archetype

**Primary: `empirical` (measurement study)** — consistent with digest N12 (rationale mirrors the ArtificialHivemind classification: the probe battery M1 is instrumental, not terminal). **Secondary: `technical_artifact`** (CO1: reusable battery + drift protocol), which is also the pre-committed pivot target (see F-G1).

Downstream consequences:
- **(a) Abstract contribution slot:** an empirical answer — the measured cross-vendor drift-correlation matrix and diversity trend (CO2, CO3) — not a new method or benchmark; the battery appears only as the instrument.
- **(b) Intro logic:** "what becomes possible": for the first time the *independence assumption* behind multi-vendor redundancy becomes auditable as a number (drift-synchrony vs. an exchangeability null), rather than "we beat baseline X". No SOTA claim exists or is needed.
- **(c) Evidence standard for results:** effect sizes with permutation-null CIs, robustness across both time alignments and across axes (RQ3), and explicit power disclosure for small vendor-n (digest t5). A significant p-value on one alignment scheme or one axis does NOT meet the standard.

## Step 3 — Taste self-audit

| Check | Verdict | Note |
|---|---|---|
| Is the opportunity a Bridge ("drift studies ∧ cross-vendor comparison were never connected")? | **PASS after fix** | The framing is not "connect longitudinal drift with cross-model similarity"; it is "isolate the component of drift on which independence is testable" (Step 0). The bridge version is forbidden and not used. |
| Is the method mere Synthesis (CAPA + Vendi + IFEval glued together)? | **PASS with guard** | The load-bearing element is not the instrument list but the **exchangeability null + capability-residualization** (M4 + B-alt), which none of the borrowed instruments contains. Instruments are cited as commodity parts. |
| Load-bearing verbs from integrate/unify/leverage family? | **PASS** | Verbs used: *isolate, measure, test, gate, residualize, falsify*. "Leverage/unify/integrate" do not appear in any claim. |
| Abstract-opening rule | **PASS** | Abstract v0 opens with the attractor/exchangeability mechanism; the "LLMs are increasingly used… however… we introduce" template is not used. |

No skeleton change was required beyond making residualization (B-alt) first-class rather than a robustness afterthought.

## Step 5 — Formal Problem Definition

**Estimand (R1, guidance.md §3.4).** The quantity of interest is the mean pairwise Pearson/cosine correlation ρ̄ between per-vendor capability-residualized drift vectors, computed over the set of dated flagship-model version releases from N accessible vendors during the studied calendar window, together with the calendar-time trend slope β of a cross-vendor behavioral-diversity index D(τ) over the same window; the unit of analysis is one vendor-pair-drift-step (for ρ̄) and one calendar time bin (for D(τ)); the reference population is deployed flagship LLM releases from the accessible vendor set, not all possible LLMs; the decision this feeds is whether "multi-vendor redundancy" can still be treated as an independence-based risk hedge (Claim 1).

**Notation.** Vendors v ∈ V; per vendor an ordered panel of dated releases (m_{v,1}, …, m_{v,T_v}) with release dates τ_{v,t} (M2). Fixed probe battery P partitioned into K = 6 axes (M1); axis-k score s_k(m) ∈ [0,1] = mean over that axis's prompts (5 samples/prompt). A-priori axis partition: **capability-loaded** K_cap = {factuality, instruction/format compliance, reasoning} vs. **capability-neutral** K_neu = {refusal, sycophancy, political/moral stance}.

- **Drift vector** (M3): d_{v,t} = ( z_k( s_k(m_{v,t+1}) − s_k(m_{v,t}) ) )_{k=1..K}, z-normalized per axis across all vendor-steps.
- **Noise floor**: ν = 95th percentile of ||d̂|| over same-snapshot re-probe deltas d̂ (B0). "Model m **drifts**" ⇔ ||d_{v,t}|| > ν.
- **Residualized drift**: d̃_{v,t} = d_{v,t} − proj_ḡ(d_{v,t}), where ḡ = mean drift direction across all vendors (the "rising-tide" component).

Adjective → definition → measurement:

| Load-bearing term (from digest Claims) | Formal definition | Measured by |
|---|---|---|
| "correlated / synchronized drift" (Claim 2) | ρ̄ = mean over vendor pairs (u,v) of Pearson r(d_u, d_v) on aligned steps; also cosine on full vectors | M3 + M4, both alignment schemes |
| "significant" correlation | ρ̄ > 95th percentile of ≥10,000-permutation null (shuffled vendor pairings and axis labels), pairwise p's BH-corrected at q = 0.05 | M4 |
| "homogenization" (title, Claim 2) | significant ρ̄ on K_neu **and** on residualized d̃ (i.e., surviving B-alt), sign-stable across both alignments | H1 ∧ H3 |
| "diversity" (Claim 3) | D(τ) = Vendi Score over vendors' K-dim behavioral profiles at calendar bin τ; secondary: mean pairwise CAPA distance (CAPA = Chance-Adjusted Probabilistic Agreement, [GreatModelsThinkAlike]'s functional-similarity measure over full output-probability distributions, adapted here as a distance) | M5 |
| "converges" (Claim 3) | Theil–Sen slope β of D(τ) < 0 with permutation p < 0.05 and total decline ≥ 10% of window-initial D | H2 |
| "drifts" at all | ||d_{v,t}|| > ν (above noise floor) | B0 gate |
| "shared data sources / alignment recipes cause it" (seed) | **not computable from observables** (C5) → **deleted from claims**; retained only as interpretation with the stated causal limit (Claim 4 / t4) | — |
| "multi-model redundancy validity" (Claim 1) | conditional statement on (H1, H2) outcomes; no new quantity | Claim–Evidence map |

## Assumptions (A1..A6)

Each row fills guidance.md §3.2's five slots (assumption, failure_mode, detection, gate, consequence); `PG-j` gate IDs are the ones checked inside the walking skeleton (Step 9) before any scale-up.

| ID | Assumption | How it could fail (failure_mode) | Detection | Gate | Consequence if it fails |
|---|---|---|---|---|---|
| A1 | Pinned snapshots/checkpoints are immutable during the study | Silent server-side updates behind a stable API string (t2) | Same-snapshot test–retest axis-score reliability r ≥ 0.9 | **PG-1** (skeleton) | Endpoint flagged as silent-update, excluded or split; affected vendor-steps dropped from H1/H3 pairwise sets, headline n reduced accordingly (R8) |
| A2 | Automated axis scorers are valid | Refusal/sycophancy/stance judges disagree with humans | κ ≥ 0.7 vs. human labels on ~500 items (~40–80 annotator-hours, N6 feasibility) | **PG-2** (pre-scale, per guidance.md §3.4 R2 step③) | Failing axis re-instrumented (named merge/split ops) and re-validated, or dropped from K_neu/K_cap; H1/H3 recomputed on the reduced axis set, not silently kept |
| A3 | A usable version panel exists: ≥ 4 vendors × ≥ 3 dated versions | Retired closed-vendor snapshots (N6's biggest feasibility risk) | Stage-1 panel audit before any probing | **PG-3** (pre-skeleton) | Panel re-anchored on open-weight vendors (Llama/Mistral/Qwen/DeepSeek); closed vendors marked partial-coverage in every table, not silently merged with full-coverage vendors |
| A4 | Models measurably drift at all | Version steps within probe noise | ≥ 2/3 of vendor-steps exceed noise floor ν | **PG-4** (skeleton pass condition) | Skeleton fails → stop and report the noise-floor null itself (Situation 1-style) before any Stage-2 spend; H1/H2/H3 are not scored on an unvalidated instrument |
| A5 | The a-priori K_cap/K_neu partition is meaningful | Capability axes don't rise; "neutral" axes carry capability signal | K_cap drift positive for ≥ 2/3 of vendor-steps | **PG-5** (skeleton) | Partition dropped; analysis restricted to the residualization-only test (d̃) so H1/H3 do not depend on an unvalidated axis split |
| A6 | 5 samples/prompt give stable axis scores | High decoding variance swamps deltas | Bootstrap CI half-width of s_k ≤ 0.05 on skeleton data | **PG-6** (skeleton) | Sample count raised (config-only change, Step 9 discipline); H2's diversity-index cells stay pre-declared INCONCLUSIVE until CI half-width is met |

### Instrument validation plan for M1 (R2, guidance.md §3.4 — the 5-step sequence)

The six-axis probe battery (M1) is the one instrument every H* depends on, so it gets the full R2 sequence, not only the κ threshold in A2:
① **Ground categories externally**: each axis is anchored to a pre-existing, cited instrument rather than invented ad hoc — refusal (borderline-safety set + keyword/classifier detector lineage), instruction/format compliance (IFEval), factuality (TruthfulQA/SimpleQA), sycophancy (Anthropic sycophancy-eval-style opinion-flip probes), political/moral stance (GlobalOpinionQA-style battery), reasoning (fixed multi-step items) — no axis is defined without an external citation.
② **Draft wide, refine on a held-out calibration set**: pilot the ~150-prompt Stage-1 battery on a calibration slice disjoint from the Stage-2 evaluation slice; named merge/split/remove operations are logged if an axis's prompts show bimodal or degenerate scores (e.g., a sycophancy sub-probe collapsing to ceiling is split out or removed, not averaged in silently).
③ **Validate against ≥2 independent human raters**: κ ≥ 0.7 per axis on ~500 held-out items (A2/PG-2), with the two raters' identities and instructions reported (R7).
④ **Inspect confusion structure**: for any axis with κ < 0.9, the human-vs-scorer disagreement cases are inspected; disagreements must cluster on adjacent labels/borderline items, not show systematic one-directional collapse (e.g., the refusal detector always over-calling compliance) — a systematic-collapse pattern triggers re-instrumentation (Situation 7), not a lowered threshold.
⑤ **Freeze before scale**: once all six axes pass ③–④, the scorer code, prompts, and thresholds are hashed before Stage-2 data collection begins — no scorer or threshold changes after this point (mirrors the digest A4 no-threshold-leakage discipline).

### Mechanism analysis (R6, guidance.md §3.4 — required by the A2 evidence standard)

Beyond the headline correlation/diversity tests (which establish *that* drift correlates or diversity trends, not *why*), one mechanism-layer analysis is pre-registered: **per-axis log-odds decomposition**. For each of the 6 axes, compute the axis's share of the total cross-vendor drift-vector correlation signal (its individual pairwise ρ contribution relative to the aggregate ρ̄_neu) and report it as a log-odds ratio against a uniform-contribution null (each axis contributing 1/6). This answers the mechanistic question RQ1/RQ3 alone cannot: *if* homogenization is detected, is it concentrated on a specific alignment-recipe-sensitive axis (e.g., refusal posture, plausibly shared via common safety playbooks) versus spread evenly across capability-neutral axes (consistent with a more diffuse shared-data-pool mechanism, per [MultiEntityRecursion])? A concentrated log-odds signature and a diffuse one license different sentences in the Discussion even when H1 and H3 both pass — this decomposition is what turns a bare "correlation exceeds the null" result into a claim about *which* shared mechanism is more consistent with the data, without over-claiming unobservable causal attribution (C5 stays undisturbed: this is a descriptive decomposition of the measured signal, not a causal-mechanism identification).

### Power statement and INCONCLUSIVE pre-declaration (Part 6 item 9, guidance.md §3.4 R2 step 5 / Situation 5)

Per-cell power is explicitly bounded by the small accessible vendor set (N6 feasibility; N10-t5): with 6 vendors there are ≤15 vendor pairs, and per-axis breakdowns (E3) further thin each cell. The following rule is pre-registered, not decided at verdict time: **a pairwise or per-axis cell is declared INCONCLUSIVE (never scored PASS, FAIL, or silently dropped) whenever its bootstrap-over-prompts CI half-width exceeds 0.15 in native ρ units, or whenever fewer than 4 vendor pairs are available for a per-axis estimate.** INCONCLUSIVE cells are excluded from the aggregate ρ̄_neu vote count in H1/H3's "≥50%"/"≥3 of 6 axes" thresholds (the aggregation is renormalized over powered cells only, and the count of excluded cells is reported alongside every headline number, R8). If the *central* aggregate test (H1's ρ̄_neu itself) is underpowered by this rule, the paper does not report a null — it reports INCONCLUSIVE and narrows the claim to the powered subset, per Situation 5.

## Step 6 — Pre-Registered Experiments

### E1 (RQ1 — is cross-vendor drift correlated beyond the independence null?)

- **Assumption:** A1, A2, A3, A4.
- **Hypothesis H1 (binary):** Under release-index alignment, mean pairwise cross-vendor drift correlation on capability-neutral axes ρ̄_neu ≥ **0.30** AND ρ̄_neu exceeds the **95th percentile** of a ≥10,000-permutation null AND ≥ **50%** of vendor pairs individually significant after BH at q = 0.05. All three or H1 fails.
- **Metric:** ρ̄_neu = mean_{u<v} Pearson r(d_u|K_neu, d_v|K_neu); cosine on full vectors reported alongside (digest N8 metrics).
- **Verification:** Permutation test (shuffle vendor pairings + axis labels, ≥10k draws); Mantel test on the full pairwise matrix; bootstrap over prompts for CIs (vendor n too small to bootstrap); BH across pairs and axes at q = 0.05 (digest analysis plan, hardened). Sample: 6 vendors × 4–6 versions × ~400 prompts × 5 samples ≈ 60k calls (N6).
- **Fallback F1 (pre-committed wording):** "Across N vendor pairs, drift-vector correlation on capability-neutral axes is statistically indistinguishable from the exchangeability null (ρ̄_neu = x, null 95th pct = y); we find **no evidence of cross-vendor behavioral homogenization beyond shared capability improvement**, which — against the prevailing monoculture concern — supports multi-vendor redundancy as a risk hedge within the studied window." (This is the digest's headline falsification, published as a positive audit result.)

### E2 (RQ2 — does cross-vendor behavioral diversity converge?)

- **Assumption:** A1, A2, A3, A6.
- **Hypothesis H2 (binary):** Theil–Sen slope of the Vendi diversity index over calendar time is **negative** with permutation p < **0.05** AND total decline over the window ≥ **10%** of the window-initial index, replicated in sign by the mean-pairwise-CAPA-distance index. Otherwise H2 fails.
- **Metric:** D(τ) = Vendi Score over vendors' per-axis behavioral profiles per calendar bin; secondary index = mean pairwise CAPA-style functional distance (digest M5, N8 metrics).
- **Verification:** Theil–Sen regression, slope sign tested by permuting time-bin labels (≥10k); bootstrap-over-prompts CIs; both indices reported, primary = Vendi (pre-registered here to prevent index shopping).
- **Fallback F2:** "The cross-vendor behavioral diversity index is flat or increasing (slope β = x, 95% CI [a, b]) over 20XX–20XX: the multi-vendor behavior space is **not measurably narrowing**, bounding how fast any monoculture dynamic can be operating at deployment scale."

### E3 (RQ3 — is the correlation an artifact of alignment scheme or a single axis?)

- **Assumption:** A1, A3, A5.
- **Hypothesis H3 (binary):** The sign of ρ̄ is **identical** under calendar-time and release-index alignment, AND the pairwise correlation is individually significant (BH q = 0.05) on ≥ **3 of 6** axes, AND remains significant after removing the single most-correlated axis. Otherwise H3 fails and any H1 positive is downgraded per F3.
- **Metric:** per-scheme, per-axis correlation estimates from M4; leave-one-axis-out ρ̄.
- **Verification:** Same permutation machinery as E1 run per scheme and per axis; agreement assessed as pre-registered sign match, not a new test (avoids garden-of-forking-paths).
- **Fallback F3:** "Cross-vendor drift correlation is **alignment- or axis-fragile** (significant only under scheme S / carried by axis k): we report it as a measurement-sensitivity finding — cross-vendor drift synchrony, if present, is not yet robustly estimable with ~6 vendors — and publish the battery and panel so the estimate tightens as vendors accumulate."
- **Granularity reconciliation note (2026-07-05, closes `discussion/stage_review.md` → Phase G finding 3):** The discussion loop's Stage 6 (`discussion/discussion_trace.md` `m_dual_alignment` / `rq_alignment_stability`; carried verbatim into `discussion/experiment_design.md` RQ4 and `discussion/paper_draft.md`/`.tex` RQ4) refined this hypothesis's first conjunct from the aggregate form stated above ("the sign of ρ̄ is identical under calendar-time and release-index alignment") to a finer per-pair form: "the sign of the mean pairwise cross-vendor drift correlation is identical under calendar-time and release-index alignment in the majority of tested vendor pairs." For scoring H3 against results, the Stage-6 per-pair form is the **operative binary criterion** for the first conjunct (sign agreement in > 50% of tested vendor pairs, each pair's sign taken from the same M4 estimator under both alignments); the aggregate-ρ̄ sign match is additionally reported as a descriptive statistic but does not by itself pass or fail the conjunct. The second and third conjuncts (≥ 3 of 6 axes individually significant at BH q = 0.05; significance surviving leave-one-axis-out) are unchanged. This note records the pre-Phase-B reconciliation the Phase G review required rather than rewriting the pre-registered H3 wording above.

### Mandatory baseline arms

- **B0 — "why do this at all" control: `B0-NoDrift` (probe-noise floor).** Re-probe every pinned snapshot twice (split-half + two-week test–retest); the distribution of same-model deltas defines ν. The study is justified only if ≥ 2/3 of true version steps have ||d_{v,t}|| > ν — i.e., *models actually drift*; otherwise "drift correlation" quantifies noise correlation and the paper's question is moot. (Digest baseline "single-vendor drift-only analysis", sharpened into a gate.)
- **B-alt — strongest-alternative-explanation control: `B-alt-RisingTide` (capability-improvement confound).** **Rival explanation (C2):** all vendors independently get better — reasoning, factuality, instruction-following rise everywhere — producing positively correlated drift with zero shared-pipeline cause. Budget-matched arm (same battery, same calls, analytic): (i) compute ρ̄ separately on K_cap and K_neu; (ii) recompute on residualized d̃ after projecting out the cross-vendor mean drift direction ḡ; (iii) CAPA contemporaneous-similarity cross-check (digest baseline 3) to show same-time similarity ≠ drift-direction similarity. The homogenization claim (H1) is only asserted if it survives (i) and (ii); if correlation lives only in K_cap / the ḡ component, the pre-committed conclusion is "correlated improvement, not homogenization."

### Global fallback F-G1

If the central family {H1, H2} fails jointly, the paper pivots archetype: `empirical finding` → `technical_artifact + audit result` (CO1 promoted to the head contribution slot). Pivoted abstract sentence, pre-committed:

> "We release a pre-registered cross-vendor drift-synchrony audit — a fixed six-axis probe battery, dated version panels, and an exchangeability-null test — and show that over 20XX–20XX, behavioral drift across N vendors is statistically indistinguishable from independent evolution once shared capability gains are removed, giving the first quantitative support for multi-vendor redundancy as a risk-hedging strategy."

## Step 9 — Walking Skeleton

**One binary question:** *does measured inter-version drift exceed the probe-noise floor, and is the drift-correlation estimator stable enough to be worth scaling?*

- **Arms (3):** (1) real drift: 3 open-weight vendor families with immutable checkpoints (Llama, Qwen, Mistral — sidesteps A3's closed-vendor risk), 3 dated versions each; (2) `B0-NoDrift` same-checkpoint re-probe; (3) shuffled-vendor permutation null (1,000 draws suffices at this scale).
- **Task set:** digest Stage-1 pilot — ~150 prompts, 3 axes only (refusal, instruction/format compliance, factuality).
- **Deterministic metrics only:** greedy decoding (1 sample); keyword+rule refusal detector, IFEval-style verifiable constraint checks, exact-match QA. **No LLM judges, no stance/sycophancy axes** in the skeleton (those wait on the A2 human-validation gate).
- **Cost:** 3 × 3 × 150 = 1,350 generations + 1,350 re-probe = **2,700 local generations ≈ 10–20 A100-hours, 1–2 days wall-clock, ~$0 API spend**.
- **Pass criterion (explicit):** A4 holds (≥ 2/3 of the 6 vendor-steps have ||d|| > ν) AND A6 holds (bootstrap CI half-width ≤ 0.05 per axis score) AND the pairwise-correlation bootstrap CI width < 0.4. **Skeleton passed ⇒ Stage 2 (6 vendors, 6 axes, 400 prompts, 5 samples, 10k permutations) is a config change — panel list, prompt list, and sample count are parameters; no new code paths.** Skeleton failed on A4 ⇒ stop: report the noise-floor result itself (drift below measurability) before spending the four-figure API budget.

## Claim–Evidence Map

| Claim (final abstract) | Traces to | Status |
|---|---|---|
| A fixed cross-vendor probe battery + drift protocol exists and is validated (CO1) | Step 5 defs; M1–M3; A2 gate | supported-by-design |
| Models drift measurably across versions | B0-NoDrift, ν definition | needs-experiment (skeleton) |
| Cross-vendor drift is/is-not correlated beyond the independence null (CO2, digest Claim 2) | H1 (+F1) | needs-experiment; fallback-covered |
| Correlation is not the rising-tide confound | B-alt-RisingTide; Step-0 asymmetry | needs-experiment (analytic arm) |
| Cross-vendor diversity converges/does not (CO3, digest Claim 3) | H2 (+F2) | needs-experiment; fallback-covered |
| Finding is robust to alignment scheme and axis choice | H3 (+F3) | needs-experiment; fallback-covered |
| Implication for multi-model redundancy (CO4, digest Claim 1) | conditional on (H1,H2); both branches pre-worded (F1/F-G1 vs. H1-positive) | fallback-covered |
| Behavioral correlation cannot establish the shared-data/recipe cause (digest Claim 4) | C5, t4; Step 5 deletion of the causal adjective | supported-by-design (stated scope limit) |

## Abstract v0 (draft, mechanism-first)

> **[DRAFT — BEFORE RESULTS; numbers are pre-registered targets, not findings.]**
> Every deployed language model is pulled toward one shared attractor — higher capability — so raw agreement in how vendors' models change across versions carries no information about shared pipelines. We isolate the component of inter-version behavioral drift on which vendor independence is actually testable: under independent development, capability-orthogonal drift directions (refusal posture, sycophancy, stance) are exchangeable across vendors. We administer a fixed six-axis probe battery to dated version panels from six vendors, extract per-vendor drift vectors, and test their cross-vendor correlation against a permutation exchangeability null, with capability gains residualized out; in parallel we measure the trend of a cross-vendor behavioral-diversity index. The outcome gates a deployment-critical question either way: excess synchrony undermines multi-vendor redundancy as a risk hedge; a null result gives it its first quantitative support.

*(≈128 words; opens with mechanism; verbs: isolate, test, measure, gate, residualize.)*
