# Dose-Response of Corpus Contamination: Coupling Measured Synthetic Fractions to Downstream Degradation — Pre-Registered Paper Specification

> Generated from digest.md + README.md (topic B6.2). Status: **specification, no experiments run.**
> All ids (C*, M*, RQ*, CO*, t*, Claim-*) refer to digest.md. Nothing below is a result.

## Step 0 — Core Asymmetry (升维)

**The statistical signature that makes LLM-generated text detectable — its excess proximity to the generator's learned distribution, i.e. its missing distributional tails — is the same signature through which it degrades a model trained on it; so forensic detection and training harm are two noisy measurements of one underlying quantity, and noise on the forensic side attenuates the estimated harm slope in only one direction: toward permissiveness.**

判据 test (delete domain nouns): *"The signature that makes a contaminant detectable is the same signature through which it causes harm; detection and harm measure one quantity, and measurement noise biases thresholds toward permissiveness."* — This is **false as a generic statement**: for almost every contaminant (lead in water, doped athletes, plagiarized text) detectability and harm arise from unrelated properties, and there is no reason detection noise should bias in one direction. The sentence only becomes true when the domain nouns return: synthetic text's closeness to the generator's distribution simultaneously (a) removes tail mass from the training signal (the collapse mechanism of [Shumailov et al., 2024], [CloserLookCollapse, OpenReview:6xCcjYa97j]) and (b) raises detector recoverability scores ([DandR, OpenReview:FiMZSxo4DO]); and errors-in-variables on the dose axis specifically *flattens* the fitted dose-response slope (Claim-4). Not a bridge: the sentence asserts a shared-cause invariant and a signed bias, not "forensics and collapse were never connected, we connect them."

## Step 2 — Archetype

**Primary: `empirical`** (measurement study; per digest N12 — the headline is measured dose-response curves plus a statistically adjudicated threshold-vs-monotonic verdict). **Secondary: instrument/protocol** (CO1 harness + CO4 metric-and-adjudication battery are enabling artifacts, not the claim).

Downstream consequences:
- **(a) Abstract contribution slot:** a measured functional law + a signed bias result ("detector noise makes contamination look safer"), *not* a new system, dataset, or SOTA number.
- **(b) Intro logic:** "what becomes possible" — corpus curators currently get a descriptive contamination estimate; a dose-response law turns that estimate into an actionable tolerance (Claim-6). No "beat a number" framing exists to fall back on.
- **(c) Evidence standard for results:** pre-registered statistics with seed-level uncertainty — equivalence tests (TOST) for any "harmless" claim, model comparison (AICc) for shape claims, multiplicity correction (Holm–Bonferroni) across the battery. Point estimates without a shape-adjudication verdict do not count as evidence.

## Step 3 — Taste self-audit

- **Is the opportunity a Bridge?** The seed's own phrasing ("把取证接到 model collapse 上") *is* bridge-shaped. **FAIL → fixed at the idea level:** the coupling is licensed by the Step-0 shared-cause invariant (harm and detectability are driven by the same distributional property), so the paper's opportunity is stated as *measuring one quantity two ways and quantifying the signed disagreement*, not as connecting two fields. The forensics module (M6) is an errors-in-variables analysis of the dose axis, not a field-marriage.
- **Is the method mere Synthesis?** Components (CPT harness, lm-eval, curve fitting, off-the-shelf detectors) are standard parts — acceptable for the `empirical` archetype, where the contribution is the *measurement design* (confound isolation C1, equivalence margins C4, paired continuous/discontinuous metrics C2), and the claim is the measured law. **PASS**, conditional on the claims never being "we built a pipeline."
- **Load-bearing verbs:** measure, isolate, adjudicate, bound, quantify, certify (equivalence). No integrate/unify/leverage in any claim. **PASS.**
- **Abstract-opening rule:** Abstract v0 (below) opens with the mechanism/asymmetry sentence; the "X is increasingly used… however… we introduce" template — which the digest's own N0 draft abstract uses — is **discarded**. **FIXED.**

## Step 5 — Formal Problem Definition

**Estimand (guidance.md R1, §3.4):** the standardized causal effect of a training corpus's
synthetic-text fraction ρ on downstream model quality, Δm(ρ) = (mean_s m(θ(ρ,s)) − mean_s
m(θ(0,s))) / SD₀(m); unit of analysis = one continued-pretraining run (backbone × dose ×
seed); reference population = fixed pre-ChatGPT-backbone continued-pretraining under an
academic-cluster compute budget (not from-scratch production pretraining, per C5); the
decision it feeds = whether a corpus curator may certify a dose ρ as statistically harmless
or must treat degradation as monotonic from the first synthetic token.

Notation. Fixed backbone θ₀; mixture corpus D(ρ) of exactly T tokens with synthetic fraction ρ = (synthetic tokens)/T, ρ ∈ G = {0, 0.5, 1, 2, 5, 10, 20, 35, 50, 75, 100}% (pilot subset {0,1,5,10,25,50,100}%); θ(ρ, s) = checkpoint after CPT of θ₀ on D(ρ) with seed s ∈ {1..k}; metric battery m ∈ M (M4). SD₀(m) = seed-level standard deviation of m at ρ=0. Standardized degradation **Δm(ρ) = ( mean_s m(θ(ρ,s)) − mean_s m(θ(0,s)) ) / SD₀(m)**, signed so that Δm > 0 = worse.

| Load-bearing adjective/verb (from Claims 1–6) | Formal definition | Measured by |
|---|---|---|
| "degradation" | Δm(ρ) as above | M4 battery per checkpoint |
| "monotonic" (Claim-1) | Jonckheere–Terpstra trend test over seed-level values across G, p < 0.05 (Holm-corrected), positive direction | M5 |
| "convex" (Claim-1) | power-law family y = a + b·ρ^γ wins AICc weight ≥ 0.5 among {flat, linear, power-law, change-point} **and** fitted γ̂ > 1 with bootstrap 95% CI excluding 1 | M5 |
| "hard threshold / change-point" (Claim-1) | segmented family wins AICc weight ≥ 0.5 **and** Davies test p < 0.05 (Holm-corrected) | M5 |
| "statistically harmless" (Claim-1) | dose ρ passes TOST vs ρ=0 with margin δ = 0.5·SD₀(m), α = 0.05; **safe region ρ\*** = largest ρ∈G such that all grid doses ≤ ρ pass TOST on the primary endpoint | M5 |
| "distribution-matched" (Claim-2) | synthetic vs human pool: Jensen–Shannon divergence of doc-length histogram ≤ 0.05 **and** of embedding-topic-cluster histogram ≤ 0.05 (decision procedure: regenerate/reject until both hold) | M1 matching report |
| "contamination-free by provenance" (Claim-2) | every document's crawl/publication timestamp < 2022-01-01 (pre-ChatGPT), source corpus fixed (C4 or Pile slice); auditable base rate ρ̂₀ from detector sweep | M1 + skeleton gate S3 |
| "isolates synthetic fraction as sole variable" (Claim-2) | across arms: identical θ₀, T, hyperparameters, shuffling policy (config-hash equality); only ρ varies | M2 + M3 config hashes |
| "detector calibration error" (Claim-4) | e(ρ) = ρ̂(ρ) − ρ, where ρ̂ = mean per-document detector score mapped through a fixed calibration; report mean |e| over G | M6 |
| "too permissive / attenuation" (Claim-4) | threshold shift Δρ\* = ρ̂\* − ρ\* > 0 (in grid steps) **and** slope ratio b̂(ρ̂)/b̂(ρ) < 1 on the primary endpoint | M6 re-fit |
| "degrades earlier" (Claim-3) | onset dose ρ_onset(m) = smallest ρ∈G with Holm-significant Δm(ρ) ≠ 0; family F degrades earlier than F′ iff median ρ_onset(F) is ≥ 1 grid step below median ρ_onset(F′) | M5 |
| "stable across scale/generator" (Claim-5 scope) | the winning curve family on the primary endpoint is identical in all backbone × generator cells | RQ4 fits |

Primary endpoint (pre-registered, single): **clean held-out perplexity** = exp(mean token NLL) on the held-out human slice + WikiText-103. All other M4 metrics are secondary (Holm-corrected).

## Assumptions (A1–A6)

- **A1 (corpus): the pre-2022 human pool has true ρ ≈ 0.** Fails if pre-ChatGPT machine text (GPT-2/3-era) contaminates the slice. *Detection:* skeleton gate S3 — detector sweep over the human pool; require estimated base rate ρ̂₀ ≤ 2%, else swap corpus slice. *Consequence:* if ρ̂₀ > 2%, the ρ=0 anchor used by every Δm(ρ) in E1–E4 is itself contaminated, degrading H1–H4 uniformly (all four rest on Δm defined relative to this anchor) — the study cannot proceed past the skeleton until the corpus slice is swapped and S3 re-passes; no H* may be scored against a failed A1.
- **A2 (corpus): the synthetic pool can be distribution-matched to the human pool** (length + topic, JS ≤ 0.05 both). Fails if generator style is unmatchable. *Detection:* M1 matching report is a hard gate before any training run. *Consequence:* if unmatchable, Claim-2's "isolates synthetic fraction as sole variable" is unsupported and every downstream H1–H4 result is confounded by generic distributional narrowing rather than syntheticness — B-alt's human-low-entropy arm is degraded from a confirmatory control to the *only* remaining causal check, and any claim about "syntheticness specifically" (Claim-1, Claim-3) must be downgraded to "distributionally-narrow text" per the B-alt decision rule below.
- **A3 (environment/effect size): CPT at this scale produces a detectable extreme-dose effect** — ρ=100% vs ρ=0 moves the primary endpoint by ≥ 2·SD₀-proxy. Fails if 1–2B tokens are too few to register any dose effect. *Detection:* walking-skeleton pass criterion S1; failure routes to F-G1. *Consequence:* blocks all of H1–H4 — no grid is launched (per Step 9's gate table) and the archetype pivots wholesale to the equivalence-certified negative result of F-G1.
- **A4 (agent/noise): seed noise permits low-dose resolution** — pilot power analysis shows ≥ 80% power to detect Δm = 1.0 at ρ = 5% with the planned seed count. Fails under high seed variance (feasibility risk in N6). *Detection:* Stage-1 pilot gate; pre-committed mitigation = shift budget from doses to seeds and promote continuous endpoints (per N6 Feasibility). *Consequence:* most exposed are H1(iii) (the low-dose change-point/harmless-region verdict) and H2's onset-dose ordering (E2) — both depend on resolving small effects near ρ=0. Per guidance.md Part 4 situation 5: any dose×seed cell that remains below 80% power *after* the reallocation is pre-declared **INCONCLUSIVE** for that cell (see Step 6 addendum below), never folded into a null or PASS verdict; H3/H4 are less exposed since their criteria (slope attenuation, family-identity match) do not require low-dose resolution.
- **A5 (metrics): the primary endpoint is continuous and monotone-interpretable across the grid** (C2). Fails if perplexity saturates or non-monotonically drifts with CPT itself. *Detection:* B0 no-CPT anchor + ρ=0 arm separate CPT-drift from dose effects (t3); RQ2's paired-metric contrasts test metric artifacts. *Consequence:* if the primary endpoint is not monotone-interpretable, H1's shape-adjudication (i)–(iii) and H2's onset-dose ordering both become unreliable on that endpoint; a positive RQ2 detection (metric-dependent verdict) restricts H1's claim to the surviving continuous endpoints only, and the primary-endpoint choice itself would need to move to the next-most-continuous metric in M4 before Stage 2 is scored.
- **A6 (oracle/detector): the black-box detector separates the two pure pools well enough to calibrate** — document-level AUROC ≥ 0.8 on human-pool vs synthetic-pool. Fails if the generator evades the detector, making M6/RQ3 vacuous. *Detection:* skeleton gate S2; if failed, swap in the second detector instrument (Binoculars-style) before Stage 2. *Consequence:* blocks H3/RQ3 specifically (the detector-coupling analysis) without affecting H1/H2/H4, which do not depend on the detector; if both instruments fail S2, RQ3 is dropped to future work and CO3 is not claimed.

**R2 instrument-validation mapping for the detector (A6, M6; guidance.md §3.4 R2):** ① categories
grounded in DandR's and Binoculars' own published construction (real vs. LLM-generated text,
single/paired-call recoverability scoring) — not re-derived from scratch, since both detectors
are reused off-the-shelf (digest.md N3#8). ② no held-out refinement step is needed for the same
reason (nothing is newly trained). ③ validated against the **provenance-known ground truth** of
the pure human/synthetic pools in place of independent human raters — a stronger substitute
than κ-agreement, since class labels are exact by construction rather than annotated; acceptance
threshold AUROC ≥ 0.8 (skeleton gate S2). ④ **confusion-structure check** (previously missing):
misclassified documents must cluster near the pool boundary (the length/topic overlap region
M1's matching deliberately creates), not scatter uniformly across both pools — a uniform-scatter
failure pattern would mean the detector exploits a spurious pool-specific artifact rather than
syntheticness, and routes to swapping in the second instrument before Stage 2. ⑤ freeze both
detectors' prompts/scoring thresholds before Stage 2, hashed alongside the training config
(same design-time-detection discipline as A4's threshold-hashing precedent).

## Step 6 — Pre-Registered Experiments

### E1 (RQ1) — Shape of the dose-response and existence of a safe region
- **Assumption:** A1, A2, A3, A4, A5.
- **Hypothesis H1 (binary):** On the primary endpoint over the Stage-2 grid: **(i)** JT monotone-trend p < 0.05 (Holm) with Δppl(100%) ≥ 2.0; **(ii)** the convex power-law family attains AICc weight ≥ 0.5 with γ̂ > 1 (CI excluding 1); **(iii)** Davies test p ≥ 0.05 (no change-point). H1 succeeds iff (i) ∧ (ii) ∧ (iii). Additionally report ρ\* (TOST-certified safe region, δ = 0.5·SD₀); H1 predicts ρ\* ∈ {0.5%…10%} and labels it resolution-limited, not mechanistic.
- **Metric:** Δppl(ρ) (Step-5 definition); AICc weights over the four families; Davies p; TOST verdict per dose.
- **Verification:** Stage 1 pilot (7 doses × 2 seeds, Pythia-410M, 1B tokens) estimates SD₀ and powers Stage 2; Stage 2 (11 doses × 3 seeds × 2 backbones, 2B tokens) fits mixed-effects regression (seed random effect), then M5 family comparison; α = 0.05, Holm–Bonferroni across the secondary battery; all margins fixed before Stage 2 (t5).
- **Fallback (pre-committed wording):** If (iii) fails with the change-point family winning: *"Single-generation synthetic contamination exhibits a genuine dose threshold at ρ\* = [fitted], below which degradation is equivalence-certified absent — an actionable curation tolerance stronger than the monotonic-harm default."* If (i) fails (flat family wins even at ρ=100%): route to **F-G1**.

### E2 (RQ2) — Metric-dependence of the verdict
- **Assumption:** A3, A5.
- **Hypothesis H2 (binary):** **(i)** In ≥ 2 of 3 diversity endpoints (distinct-2, Self-BLEU, embedding coverage) and ≥ 1 of 2 tail endpoints, ρ_onset is ≥ 1 grid step below ρ_onset(primary capability endpoint); **(ii)** every apparent change-point on a discontinuous few-shot metric (Davies p < 0.05) fails to replicate (Davies p ≥ 0.05) on its paired continuous metric over the same checkpoints. H2 succeeds iff (i) ∧ (ii).
- **Metric:** ρ_onset(m) per Step-5; per-family winning curve shape; paired Davies tests.
- **Verification:** same Stage-2 checkpoints re-scored on the full M4 battery; onset doses compared by pre-registered rank rule; Holm correction within each metric family.
- **Fallback:** *"The dose-response verdict is metric-invariant: capability, diversity, and tail endpoints yield statistically indistinguishable shapes and onsets — a single cheap endpoint (clean perplexity) suffices for contamination monitoring, simplifying deployment."* (Negative result on Claim-3, positive for practice.)

### E3 (RQ3) — Forensic coupling: detector error on the dose axis
- **Assumption:** A6 (plus E1's arms already run).
- **Hypothesis H3 (binary):** Re-fitting all curve families against detector-estimated ρ̂: **(i)** slope-attenuation b̂(ρ̂)/b̂(ρ) ≤ 0.8 on the primary endpoint; **(ii)** the apparent safe region widens by Δρ\* ≥ 1 grid step; **(iii)** mean calibration error is under-estimation at low dose: mean e(ρ) < 0 for ρ ≤ 10%. H3 succeeds iff at least (i) ∧ (ii).
- **Metric:** e(ρ), Δρ\*, slope ratio (Step-5); calibration curve ρ̂(ρ) with bootstrap CIs (documents resampled).
- **Verification:** two detector instruments (recoverability-style per [DandR, OpenReview:FiMZSxo4DO] + Binoculars-style) over a fixed 5k-document sample per mixture; refit M5 per instrument; report per-instrument and pooled verdicts.
- **Fallback:** *"Off-the-shelf detectors already track corpus fraction within one grid step (mean |e| = [value]), so forensic estimates can be used directly as the dose input of a harm function — coupling is practical today, without new detector development."* If detector noise instead over-alarms (Δρ\* < 0): report the signed direction as the finding; Claim-4's direction is falsified but the coupling analysis (CO3) stands.

### E4 (RQ4) — Stability across scale and generator
- **Assumption:** A2, A3.
- **Hypothesis H4 (binary):** The winning curve family on the primary endpoint is **identical in all 4 backbone × generator cells** (410M/1.4B × Llama-3.1-8B/Qwen2.5-7B on the dose sub-grid); dose-coefficient magnitude may differ (dose × scale interaction permitted and expected, p-value reported, no criterion attached).
- **Metric:** per-cell AICc-winning family; mixed-effects interaction terms (dose × scale, dose × generator).
- **Verification:** Stage-2 factorial on the dose sub-grid {0, 5, 20, 50, 100}%, 3 seeds; family identity is exact-match over 4 cells (no test needed — a categorical criterion); interactions from the pooled mixed-effects model.
- **Fallback:** *"No single dose-response law transfers across scale/generator: the functional family itself flips ([cells]), so contamination tolerances must be calibrated per training regime — C5 is elevated from threat to finding, and the released harness is the instrument for that per-regime calibration."*

### Power addendum — thin-cell INCONCLUSIVE rule (guidance.md Part 4 situation 5, Part 6 item 9)

Per A4's pilot-based power analysis (≥80% power to detect Δm = 1.0 at ρ = 5% with the planned
seed count): any dose×seed cell that, **after** the Stage-1-informed reallocation (budget shifted
from dose levels to seeds, continuous endpoints promoted to primary per N6 Feasibility), still
falls below 80% power for the pre-registered effect floor is pre-declared **INCONCLUSIVE** for
that cell. An INCONCLUSIVE cell is excluded from the AICc/Davies/TOST verdict computation for
the RQ it belongs to and reported separately in the results table — it is never folded into a
"null" (flat-family win) or a "PASS" reading. If the *primary* endpoint's central test (H1 at the
lowest dose levels) is itself underpowered even after reallocation, H1's low-dose claim narrows
to the powered cells only and the unpowered doses are named explicitly in the abstract's
envelope statement, never silently dropped from the reported grid.

### Mandatory baselines
- **B0 — "why do this at all" control: the ρ=0 clean-CPT arm + no-CPT frozen backbone** (digest N8 baselines 1–2). B0 justifies the problem's existence: if ρ=100% does not differ from ρ=0 by ≥ 2·SD₀ on any endpoint at matched budget, there is no measurable harm to dose out at this scale, and every downstream claim is void (→ F-G1). B0 also separates CPT-drift from dose effects (t3): all Δm are defined against ρ=0, never against θ₀.
- **B-alt — strongest-alternative-explanation control: the human-low-entropy arm.** *Rival explanation:* observed degradation is caused by **distributional narrowing of any kind** (low-diversity/OOD text), not by syntheticness per se (this is C1's residual after M1 matching). *Control:* budget-matched CPT arms at ρ_eff ∈ {20, 50, 100}% where the "contaminant" is **human** text from the same corpus, oversampled/duplicated until its NN differential entropy matches the synthetic pool's measured entropy. Decision rule: if the human-low-entropy dose-response is statistically indistinguishable from the synthetic one (overlapping curve fits, interaction p ≥ 0.05), the causal claim is re-scoped from "synthetic text harms" to "entropy-depleted text harms, and synthetic text is one instance" — this re-scoped wording is pre-committed. The accumulate-regime arm and the entropy-maximizing-selection arm (digest N8 baselines 3–4) are retained as secondary mitigation references, not confound controls.

### Global fallback F-G1 (archetype pivot)
If the central family {H1(i), B0 gate} fails — no detectable degradation even at ρ=100% at matched budget — the archetype pivots from `empirical finding` to `equivalence-certified negative result + instrument (CO1/CO4 promoted to headline)`. Pivoted abstract sentence, pre-committed: *"Under a pre-registered equivalence-testing protocol, single-generation synthetic contamination up to 100% of a continued-pretraining budget produces no degradation beyond δ = 0.5 SD on capability, diversity, or tail endpoints at the ≤1.4B/2B-token scale — an upper bound that localizes model-collapse harm in the multi-generation regime and a released harness for finding the budget at which harm first becomes measurable."*

## Step 9 — Walking Skeleton

One binary question before any grid: **is there any dose signal to measure, and are the two measurement instruments (provenance + detector) sound?**

- **Arms (3):** (1) ρ=0 CPT, (2) ρ=100% CPT, (3) no-CPT anchor. Pythia-410M, 200M tokens, 1 seed each, identical config hash except the mixture.
- **Smallest task set / deterministic metrics only:** clean held-out perplexity (deterministic given checkpoint); distinct-2 over 1k continuations at fixed sampling seed; detector score distributions over 1k docs from each pure pool.
- **Gates (all binary):**
  - **S1 (A3):** ppl(ρ=100%) − ppl(ρ=0) ≥ 1% relative, and larger than the ρ=0-vs-no-CPT drift direction allows to explain.
  - **S2 (A6):** detector AUROC ≥ 0.8 separating the two pure pools.
  - **S3 (A1):** estimated human-pool base rate ρ̂₀ ≤ 2%.
  - **S4 (A2):** M1 matching report passes (both JS ≤ 0.05).
- **Cost:** 2 CPT runs ≈ 2–3 A100-h; synthetic generation ≈ 250M tokens ≈ 20–25 A100-h (vLLM, 8B generator); eval + detector ≈ 5 GPU-h. **Total ≈ 30–35 A100-hours, 1–2 days wall-clock.**
- **Passed → scaling is a config change:** the harness takes (dose grid, seeds, token budget, backbone, generator) as config; Stage 1 (14 runs) and Stage 2 (66 runs + B-alt arms) reuse the identical code path. If any gate fails, no grid is launched: S1-fail → F-G1 deliberation; S2-fail → swap detector; S3-fail → swap corpus slice; S4-fail → regenerate synthetic pool.

## Claim–Evidence Map

| Abstract claim (digest Claims) | Traces to | Status |
|---|---|---|
| Degradation is monotone, convex, no hard threshold; low-dose "safe region" is resolution-limited (Claim-1) | H1 (i)(ii)(iii) + Step-5 defs of monotone/convex/threshold/harmless | needs-experiment; fallback-covered (E1 fallback, F-G1) |
| The protocol isolates synthetic fraction as sole variable at academic cost (Claim-2) | Step-5 "isolates" definition (config-hash equality) + A1/A2 gates S3/S4 + B-alt | supported-by-design (design property, verified by gates), residual confound covered by B-alt |
| Threshold verdicts are partly metric properties; diversity/tail degrade earlier (Claim-3) | H2 (i)(ii) + Step-5 ρ_onset | needs-experiment; fallback-covered (E2 fallback) |
| Detector dose error is signed toward permissiveness (Claim-4) | H3 (i)(ii)(iii) + Step-5 Δρ\*, slope ratio; Step-0 asymmetry | needs-experiment; fallback-covered (E3 fallback, direction-flip clause) |
| Quantitative curve constants are unknown until run (Claim-5) | explicit non-claim; only shape-family + stability claimed (H4) | supported-by-design (spec refuses false precision) |
| Measured fraction → actionable tolerance for curators (Claim-6) | composition of H1 (ρ\* exists as defined) + H3 (its detector-side correction) | needs-experiment; degraded gracefully by E1/E3 fallbacks |

## Abstract v0 (DRAFT — written before any results; numbers are placeholders by design)

The property that makes LLM-generated text detectable — its excess proximity to the generator's distribution, i.e. its missing tails — is the same property through which it degrades models trained on it, so contamination forensics and contamination harm measure one quantity, and forensic noise biases safety thresholds only toward permissiveness. We measure this quantity directly: from a fixed pre-ChatGPT backbone, we continue pretraining at fixed token budget across a log-spaced grid of exactly-known synthetic fractions (0–100%), score every checkpoint on a pre-registered capability/diversity/tail battery, and adjudicate flat, linear, convex, and change-point response shapes with equivalence tests at low dose. A human-text entropy-matched control isolates syntheticness from generic distributional narrowing. Re-fitting the curves against detector-estimated fractions quantifies how forensic error shifts the certified safe region — turning "how much is present" into "how much is harmful." [Results: TBD.]

*(150 words; draft-before-results; Step-3 rules enforced: asymmetry-first opening, verbs measure/isolate/adjudicate/quantify, no trend-however-introduce template.)*
