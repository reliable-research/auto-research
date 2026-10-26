# The Privacy-Capability Scissors: Dose-Response of Synthetic Corpus Contamination with Rarity Displacement

## Abstract

Web-scale training corpora increasingly contain machine-generated text, yet the two literatures that should tell curators what to do about it do not connect: model-collapse studies vary *generations* of recursive training at extreme doses, and memorization studies measure privacy risk of a corpus *as given*. Neither answers the question every curator faces — at a measured synthetic fraction $\rho$, how much harm, of what kind, and is there a practically safe region? We propose a controlled continued-pretraining study that treats the within-generation synthetic fraction as a *dose* ($\rho \in \{0, 0.5, 1, 2, 5, 10, 20, 35, 50, 75, 100\}\%$, log-spaced at the low end) and, crucially, treats *which rarity stratum of human data the synthetic text displaces* as a second designed factor. Our organizing hypothesis is that contamination and memorization consume a shared budget: under a fixed memorization capacity (~3.6 bits/parameter; Morris et al., 2025), entropy-poor synthetic text that displaces rare human data both degrades capability/tail coverage *and* makes the surviving rare examples rarer — hence more heavily memorized and more extractable. This predicts the **privacy-capability scissors**: at fixed dose, rare-targeted displacement lowers rare-token recall while raising canary exposure and membership-inference AUC on residual rare-stratum data. The design uses frozen pre-ChatGPT backbones (Pythia-410M/1.4B), a provenance-clean pre-2022 human pool, matched displacement arms with duplication-matched resampling controls, per-stratum canaries at controlled duplication {1, 4, 16}, and a preregistered curve-family adjudication (flat / linear / convex / change-point, with disjoint supports, an explicit *unclassified* outcome, and an equivalence test for a "statistically harmless" low-dose region). A forensic coupling analysis re-estimates all curves on detector-estimated doses $\hat{\rho}$ and reports how detector error shifts the threshold verdict. Total budget ≈ 1.1–1.3k A100-hours (~75 runs), gated by preregistered pilot checks. The deliverable is a transferable measurement protocol and a shape-of-harm verdict, not a single magic threshold.

## 1. Introduction

Post-2022 web corpora are measurably contaminated with LLM-generated text (Liang et al., 2024), and provenance filtering is failing faster than detection is improving. Two mature literatures surround this fact without answering the operative question. The model-collapse line shows that *recursive* training on generated data loses distributional tails (Shumailov et al., 2023/Nature 2024) and that the outcome depends strongly on the training regime: collapse can be avoided when real and synthetic data *accumulate* rather than replace one another (Gerstgrasser et al., 2024), while theory in solvable regression settings predicts that even small synthetic fractions change scaling behavior and that no strictly safe dose exists (Dohmatob et al., 2024a; 2024b). The memorization line shows that language models memorize their training data in proportion to duplication, model scale, and example rarity (Carlini et al., 2021; 2022), that deduplication mitigates privacy risk (Lee et al., 2021; Kandpal et al., 2022), and — in the result that motivates this paper — that models have an approximately fixed memorization capacity of ~3.6 bits per parameter which rare/atypical data disproportionately fills (Morris et al., 2025).

Neither line delivers a *within-generation dose-response curve*: the functional relationship between a measured synthetic fraction $\rho$ and downstream harm, at fixed compute, fixed token budget, and fixed provenance. Detection work (e.g., corpus-level prevalence estimation; Liang et al., 2024) tells a curator *how much* synthetic text is present; nothing tells them *how much is harmful*, whether harm is monotone or thresholded, or how detector noise distorts that verdict. And no existing work couples contamination dose to the *privacy* of the human data that survives in the mixture.

This paper's organizing claim is that **contamination and memorization are two faces of one budget**. Synthetic text is entropy-poor and tail-truncated relative to human text (Guo et al., 2024; Shi et al., 2025). Mixing it in (a) reduces the effective diversity of the training signal, degrading capability and tail coverage; and (b) changes what fills the fixed memorization budget: when synthetic text displaces *rare* human data, the surviving rare examples become rarer relative to the training distribution and — per the rarity-driven memorization mechanism (Morris et al., 2025; Carlini et al., 2022) — are memorized *harder*. Contamination therefore plausibly increases per-example privacy risk for residual minority data even as aggregate capability degrades. We call the predicted signature the **privacy-capability scissors**: at fixed dose, rare-targeted displacement lowers rare-token recall while raising canary exposure and membership-inference AUC on the surviving rare stratum. This is the mechanistic reason rarity must be a *designed factor* of the mixture (which stratum the synthetic tokens displace), not a covariate.

We contribute:

1. **A confound-controlled dose axis.** A continued-pretraining panel over frozen pre-ChatGPT backbones and a provenance-clean pre-2022 human pool, with exactly-known $\rho$ on a log-spaced grid from 0.5% to 100%, fixed token budget, and denser replication at low doses — so "is 3% tolerable?" is answerable in principle, and $\rho = 100\%$ anchors the collapse literature.
2. **Rarity displacement as treatment, duplication as a controlled variable.** Rare-targeted vs. common-targeted vs. proportional displacement at matched $\rho$, with matched duplication profiles and duplication-matched human-resampling controls, so displacement effects are identified separately from duplication effects (engaging Lee et al., 2021; Kandpal et al., 2022 directly).
3. **A dual outcome battery with a preregistered shape verdict.** Capability/diversity/tail metrics and a privacy battery (per-stratum canaries at duplication {1, 4, 16}, verbatim extraction, calibrated membership inference) feed a four-family curve adjudication — flat / linear / convex / change-point on disjoint supports — with an explicit *unclassified* outcome and an equivalence (TOST/ROPE) criterion, so a "statistically harmless" low-dose region is a possible finding rather than an assumption.
4. **Forensic coupling.** All curves are re-estimated on detector-estimated doses $\hat{\rho}$ (calibration curve $\hat{\rho}(\rho)$ from two black-box detectors), with the threshold shift $\Delta\rho^{*}$ and verdict flips reported; predicted direction: detector noise biases policy toward permissiveness.

The claims are scoped honestly: the estimand is dose-response *under fixed-backbone continued pretraining at ≤1.4B scale and fixed budget*, with scale transfer measured as a trend (two backbones + a from-scratch 160M regime check informed by proxy-validity results; small-proxy caveats per ICLR 2026 findings on proxy-run curation), not claimed resolved. The deliverable is the protocol, the curve family, and the direction of detector-induced bias — not one number.

## 2. Related Work

**Model collapse and recursive training.** Shumailov et al. (2023; Nature 2024) established tail loss under generational retraining; Alemohammad et al. (2024) the quality/diversity decay of self-consuming image loops; Seddik et al. (2024) a statistical characterization; Bertrand et al. (2024) stability conditions for iterative retraining; Borji (2024) a statistical reading of the phenomenon. Gerstgrasser et al. (2024) showed collapse is avoidable when data accumulate rather than replace, and Kazdan et al. (2024) mapped the intermediate regimes. Dohmatob et al. (2024a; 2024b) provide the sharpest adverse prior for our question: in solvable settings, even small synthetic fractions alter scaling laws and collapse can be "strong" — i.e., theory predicts *no safe threshold*. Shi et al. (2025) recast collapse as a generalization-to-memorization transition driven by declining data entropy. All of these vary generations or regimes; none sweeps a controlled within-generation fraction grid at LM scale and statistically adjudicates flat vs. monotone vs. thresholded harm. We also *design in* the accumulate-vs-replace debate rather than argue it: a matched accumulate arm at equal synthetic token count places the Gerstgrasser contrast on our dose axis.

**Data mixtures and synthetic data as an asset.** DoReMi (Xie et al., 2023) shows mixture proportions causally affect quality on the human-domain axis; data-mixing-law work fits proportion-to-loss functions for human mixtures; synthetic continued pretraining (Yang et al., 2024) is the benefit-framed inverse of our harm-framed axis and supplies our CPT protocol template; Chen et al. (2024) and Havrilla et al. (2024) study synthetic-data diversity/quality effects. None of these treats synthetic fraction as a harm dose with a threshold question, nor touches privacy.

**Memorization, duplication, and privacy.** Carlini et al. (2019; 2021; 2022) established canary exposure, training-data extraction, and the scaling of memorization with duplication, model size, and context. Zhang et al. (2023) defined counterfactual memorization. Lee et al. (2021) and Kandpal et al. (2022) showed deduplication reduces memorization and privacy risk — the reason our design controls duplication explicitly, lest rarity-displacement effects be duplication effects in disguise. Membership inference on LLM pretraining data is hard and calibration-sensitive (Duan et al., 2024); we adopt Min-K%/Min-K%++-style calibrated scores (Shi et al., 2023) against per-stratum frozen non-member splits. Morris et al. (2025) measure a fixed capacity of ~3.6 bits/parameter with rare data disproportionately memorized — the quantitative engine of our scissors prediction; our motivation degrades gracefully if the capacity number shifts, since the rarity-memorization direction is independently established (Carlini et al., 2022). No prior work manipulates contamination as the treatment and reads memorization of the *residual human data* as the outcome.

**Forensics.** Black-box AI-text detectors score documents (DandR-style recoverability; Binoculars-style perplexity contrast), and Liang et al. (2024) estimate corpus-level AI-modified fractions; detection stops at *presence*. We couple it to *harm*: the practical consumer of a dose-response curve only observes $\hat{\rho}$, so we propagate detector error into the threshold verdict.

**One-line positioning.** Prior work varies generations (collapse), regimes (accumulate/replace), or domain weights (DoReMi) and reads capability; we vary within-generation synthetic fraction × displaced-stratum rarity and read capability, diversity, and privacy harm on the residual human data — one controlled design, two coupled harm families.

## 3. Problem Definition

Let the training mixture for run $i$ be $T_i = H_i \cup S_i$ with known synthetic fraction $\rho_i = |S_i| / |T_i|$ (token-weighted), built by continued pretraining (CPT) from a frozen backbone $p_0$ whose original corpus predates ChatGPT. Each human document $x \in H_i$ carries a preregistered rarity stratum $z(x)$ — assigned by (i) rare-token density decile and (ii) topic-cluster population size — and a controlled duplication count $m_i(x)$. The displacement condition $d_i \in \{\text{rare}, \text{common}, \text{proportional}\}$ specifies which strata the synthetic tokens replace at matched $\rho$; duplication profiles are matched across conditions.

Outcomes per run: capability $C_i$, diversity/tail $V_i$, and per-stratum privacy risk $R_i(\cdot)$ (canary exposure, extraction rate, MIA AUC). The target curves, relative to the $\rho=0$ CPT control at matched duplication configuration $u$:

$$f_C(\rho, d, u) = \mathbb{E}[\,C_{0,u} - C_i \mid \rho_i = \rho, d_i = d, u_i = u\,], \qquad f_V \text{ analogous},$$

$$f_P(\rho, d, u; s) = \mathbb{E}[\,R_i(s) \mid \rho_i = \rho, d_i = d, u_i = u\,] \quad \text{for stratum } s,$$

with duplication entering only through designed contrasts. Each curve is adjudicated into a family $\kappa \in \{\text{flat}, \text{linear}, \text{convex}, \text{change-point}\}$ over *disjoint* supports, or *unclassified* if no family passes a predictive-calibration gate. Displacement effects are matched-dose contrasts against the proportional arm, $\Delta_f^{\text{disp}}(\rho, d, u) = f(\rho, d, u) - f(\rho, \text{proportional}, u)$. The scissors hypothesis is the conjunction, at fixed $\rho$: $\Delta^{\text{disp}}_{f_V}(\rho, \text{rare}) > 0$ (worse tail coverage) and $\Delta^{\text{disp}}_{f_P}(\rho, \text{rare}; \text{rare}) > 0$ (higher privacy risk on surviving rare data), with the resampling-control DiD removing the duplication-attributable share. A *statistically harmless region* is the maximal prefix of the dose grid on which TOST equivalence vs. $\rho = 0$ holds for all primary endpoints at the preregistered margin $\delta = 0.5\,\sigma_0$ ($\sigma_0$ = $\rho=0$ seed SD). All conclusions are scoped to one generation of CPT under $p_0$; the practical-inference variant replaces $\rho$ by the detector estimate $\hat{\rho} \sim q(\hat{\rho} \mid \rho)$ and must propagate that error.

## 4. Method

![Figure 1: Overview of the dose-response pipeline: provenance-clean pool construction and rarity stratification, contamination dose grid with displacement arms and canary lacing, frozen-backbone paired-seed CPT runs, dual capability/privacy probe batteries, four-family curve adjudication with equivalence testing, and forensic dose-estimate coupling — gated by preregistered pilot checks G0–G3.](architecture.svg)

*Figure 1: Overview of the dose-response pipeline: provenance-clean pool construction and rarity stratification, contamination dose grid with displacement arms and canary lacing, frozen-backbone paired-seed CPT runs, dual capability/privacy probe batteries, four-family curve adjudication with equivalence testing, and forensic dose-estimate coupling — gated by preregistered pilot checks G0–G3.*

### 4.1 Corpus construction: pools, strata, doses, canaries

**Pools.** Human pool = a fixed pre-2022 C4/Pile slice (provenance-clean by date; residual contamination bounded in §6), stratified into rarity strata by (i) bottom-decile-frequency token density and (ii) topic-cluster size (minority-domain proxy), pre-registered before any run. Synthetic pool = Llama-3.1-8B-Instruct regenerations/continuations of a *disjoint* slice, rejection-filtered to match length/topic marginals; a second generator (Qwen2.5-7B-Instruct) serves the robustness arm.

**Dose grid.** $\rho \in \{0, 0.5, 1, 2, 5, 10, 20, 35, 50, 75, 100\}\%$ at fixed total token budget; log-spacing below 5% because the threshold question lives there; $\rho = 100\%$ anchors the collapse endpoint. Pilot subset $\{0, 1, 5, 10, 25, 50, 100\}\%$.

**Displacement factor (absorbed B6.4).** At $\rho \in \{5, 25, 50\}\%$, synthetic tokens replace (a) rare-stratum, (b) common-stratum, or (c) proportionally sampled human documents. Matched-pair displacement (each displaced rare document matched to a retained common document on length/quality proxies) keeps the factor orthogonal to length, topic, and quality; duplication profiles are matched across (a)–(c); the factor is capped at $\rho \le 50\%$ (beyond that the residual rare pool degenerates), and the achieved stratum-exhaustion fraction is reported per cell. A **duplication-matched human-resampling control** mirrors each displacement arm with human-only filler reproducing the synthetic arm's multiplicity histogram, enabling difference-in-differences that separate rarity displacement from duplication (Lee et al., 2021; Kandpal et al., 2022).

**Canary lacing.** Per-stratum canaries (register-matched to their stratum) at controlled duplication {1, 4, 16}, identical sets across all arms, total canary mass < 0.01% of tokens — so canary rarity is defined relative to the *surviving* human distribution, which is the treatment.

### 4.2 Training protocol

Frozen-backbone continued pretraining: identical starting checkpoint (Pythia-410M primary; Pythia-1.4B scale arm — both Pile-trained, pre-ChatGPT), identical hyperparameters, fixed budget (1B tokens pilot / 2B scale-up), paired seeds shared across doses (2 pilot / 3 scale-up), with *denser replication at $\rho \le 5\%$* (unbalanced by design, preregistered — this buys low-dose power where the seed-noise floor threatens identifiability). Controls: $\rho=0$ CPT control (primary reference), no-CPT frozen backbone (anchors CPT drift), **accumulate-regime arm** at matched synthetic token count at three doses (placing the Gerstgrasser contrast on the dose axis). Config hashes, loss curves, and mixture manifests logged per run.

### 4.3 Outcome batteries

**Capability/diversity/tail.** Clean held-out perplexity on the human validation slice (preregistered primary endpoint) + WikiText-103; lm-eval-harness few-shot (LAMBADA, HellaSwag, ARC-E, PIQA); distinct-2/3, Self-BLEU, mean pairwise embedding distance over 5k continuations of held-out human prompts; rare-token recall and tail-decile perplexity; generation NN differential entropy. Every discontinuous metric is paired with a continuous counterpart; threshold verdicts never rest on a discontinuous metric alone.

**Memorization/privacy (absorbed axis).** (i) Canary exposure (secret-sharer protocol; Carlini et al., 2019) per stratum × duplication × dose × displacement arm — the *primary* privacy endpoint because it is exposure-controlled by construction; (ii) verbatim extraction: greedy + sampled continuation of 50-token prefixes of training rare-stratum documents, ≥50-token match (constants per Carlini et al., 2021/2022); (iii) calibrated MIA: Min-K%++ AUC per stratum against per-stratum member/non-member splits *frozen before any training run*, non-members drawn from the same provenance-clean slice (calibration caveats per Duan et al., 2024). A **manipulation check** — realized rarity histograms of the surviving corpus per arm — is a required figure preceding any scissors claim.

### 4.4 Curve fitting and adjudication

Per metric, standardized by $\sigma_0$: four candidate families on **disjoint supports** — flat (exactly constant); linear (endpoint displacement ≥ 0.10 $\sigma_0$); convex/monotone (spline or quadratic with curvature ≥ 0.10 $\sigma_0$ from the chord); segmented one-knot (kink displacement ≥ 0.10 $\sigma_0$, knot with ≥ 2 doses on each side). Parameters inside the separation bands ⇒ **unclassified**, never a forced label; family probabilities are interpreted only if a leave-one-dose-out calibration gate passes (pooled RMSE ≤ 0.15 $\sigma_0$; 90% predictive-interval coverage ∈ [0.85, 0.95]). Complementary frequentist battery (preregistered): AICc comparison, Davies change-point test, Jonckheere–Terpstra monotone trend, **TOST equivalence vs. $\rho=0$** with margin $\delta = 0.5\,\sigma_0$ defining the statistically-harmless region, Holm–Bonferroni across the battery; mixed-effects dose × displacement × scale models for the factorial questions. Thresholds and priors are frozen in a hashed preregistration file before non-zero-dose outcomes are unblinded.

### 4.5 Forensic coupling

Two black-box detectors (DandR-style recoverability score; Binoculars-style perplexity-contrast score) sweep fixed document samples from every mixture, yielding the calibration curve $\hat{\rho}(\rho)$ per detector. All §4.4 models are re-fit on $\hat{\rho}$; we report the threshold shift $\Delta\rho^{*}$, equivalence-region shift, and any family-verdict flips. Predicted direction (falsifiable): regression-toward-the-mean in $\hat{\rho}$ flattens the low-dose curve and biases policy toward permissiveness. Detector error is propagated (errors-in-variables within the Bayesian fit), not plugged in.

## 5. Experimental Design

**Sparse run matrix (~75 runs, not a full factorial).**

| Arm | Design | Runs |
|---|---|---|
| A: dose curve | 11 doses × proportional × Pythia-410M × generator-1 × 3 seeds (pilot: 7 × 2) | 33 |
| B: displacement | {rare, common} × $\rho \in \{5, 25, 50\}\%$ × 3 seeds (+ resampling controls) | 18 |
| C: scale trend | Pythia-1.4B × $\rho \in \{0, 5, 25, 50, 100\}\%$ × 2 seeds | 10 |
| D: generator-2 | Qwen2.5-7B × $\rho \in \{5, 25, 50\}\%$ × 2 seeds | 6 |
| E: controls | no-CPT, accumulate × 3 doses, extra $\rho=0$ seeds | ≈8 |
| F: regime check | 160M from-scratch, 3-point sub-grid | ≈6 |

**Compute.** 410M × 1–2B tokens ≈ 5–12 A100-h/run; 1.4B ≈ 35 A100-h/run; training ≈ 900 A100-h; synthetic generation (vLLM, 8B generators, 1.5–2B tokens) ≈ 150–300 A100-h; evaluation + MIA/extraction ≈ 50 GPU-h. **Total ≈ 1.1–1.3k A100-hours** — 6–7 days wall-clock on one 8×A100 node, embarrassingly parallel. This is the audited feasibility envelope; the from-scratch multi-thousand-run alternative is out of scope by design.

**Go/no-go gates (preregistered).**
- **G0 (before any run):** novelty sweep for 2025–26 within-generation dose-sweep papers; verify the capacity/rarity citation set. A near-twin dose sweep without the rarity/privacy axis narrows us to the absorbed contribution; a twin *with* it kills the topic — check first.
- **G1 (pilot):** seed-level SD from 14 pilot runs → power analysis; the minimal detectable low-dose effect must be ≤ the TOST margin, else rebalance (more seeds/tokens at $\rho \le 5\%$, drop $\rho = 75\%$).
- **G2 (pilot):** privacy measurability — duplication-16 canary exposure at $\rho = 0$ must clear the detection floor at 410M; else the privacy axis degrades, pre-declaredly, to canaries at duplication {16, 64} and the natural-document extraction claim is dropped.
- **G3:** displacement manipulation check — realized rarity profiles must differ across arms as designed; else the rarity factor is void and the paper falls back to the pure dose-response core (still the seed's minimal experiment).

**Research questions.**
1. **RQ1 (shape):** For each primary endpoint, which family — flat / linear / convex / change-point / unclassified — best describes $f(\rho)$, and does a statistically harmless low-dose region exist under TOST at $\delta = 0.5\,\sigma_0$?
2. **RQ2 (scissors):** At matched $\rho$, does rare-targeted displacement raise canary exposure and Min-K%++ AUC on surviving rare-stratum data while lowering rare-token recall, after subtracting the duplication-matched resampling DiD?
3. **RQ3 (regime):** Does the accumulate arm at matched synthetic token count sit on, below, or off the replacement-regime dose curve (the Gerstgrasser contrast, within-generation)?
4. **RQ4 (forensics):** How far does re-estimating on $\hat{\rho}$ shift the threshold/equivalence verdict ($\Delta\rho^{*}$), and in which direction?
5. **RQ5 (transfer trend):** Do 1.4B and 160M-from-scratch arms preserve the 410M curve family and the sign of the scissors (trend claim only)?

**Falsifiers.** Scissors dies if the rare-targeted arm does not separate from proportional after DiD (G3-adjacent); the threshold story dies (informatively) if low-dose cells are TOST-inconclusive after G1 rebalancing — reported as "unanswerable at this scale," which bounds the field's proxy designs; the Dohmatob no-safe-dose prediction is *supported* if the flat family never wins at any positive dose.

## 6. Limitations and Threats

**Estimand scope.** Fixed-backbone CPT at ≤1.4B, fixed budget: not the from-scratch production curve. The 160M from-scratch check and the small-proxy validity literature (reduced-LR ranking preservation; ICLR 2026) mitigate but do not remove this; we claim trends, not transferred thresholds. **Residual contamination of the "clean" pool**: pre-2022 provenance bounds but does not zero synthetic content; any residue attenuates low-dose contrasts toward flat — we report a detector-based bound on the $\rho=0$ pool and treat the harmless-region estimate as conservative in width, not location. **Privacy floor at small scale**: memorization scales with model size; G2 pre-declares the graceful degradation path rather than discovering it at analysis time. **Generator specificity**: two generators, one family each; threshold *numbers* are scoped to generator/scale, the protocol and shape verdict are the transferable claims. **Change-point identifiability**: with 11 doses and seed noise, convex vs. segmented may be unresolvable — the unclassified outcome is the honest report, and power analysis budgets for it.

## 7. Conclusion

We reframe corpus contamination from a detection problem into a dose-response problem, and couple it — through the fixed-memorization-budget mechanism — to the privacy of the human data that survives the mixture. The design answers the curator's question at the scale a small group can execute honestly: a log-spaced within-generation dose grid with rarity displacement as a designed factor, duplication controlled, an adjudicated shape verdict with an explicit harmless-region test, an accumulate-regime anchor, and detector-error propagation into the policy verdict. If the scissors prediction holds, "how contaminated is my corpus?" becomes two questions with one answer curve: how much capability you lose, and how much more extractable your rarest human data becomes.

## References

- Alemohammad, S. et al. (2024). Self-Consuming Generative Models Go MAD. ICLR 2024.
- Bertrand, Q. et al. (2024). On the Stability of Iterative Retraining of Generative Models on Their Own Data. ICLR 2024.
- Borji, A. (2024). A Note on Shumailov et al. (2024). arXiv:2410.12954.
- Carlini, N. et al. (2019). The Secret Sharer: Evaluating and Testing Unintended Memorization in Neural Networks. USENIX Security.
- Carlini, N. et al. (2021). Extracting Training Data from Large Language Models. USENIX Security.
- Carlini, N. et al. (2022). Quantifying Memorization Across Neural Language Models. arXiv:2202.07646; ICLR 2023.
- Chen, H. et al. (2024). On the Diversity of Synthetic Data and Its Impact on Training Large Language Models. arXiv:2410.15226.
- Dohmatob, E., Feng, Y., Kempe, J. (2024a). Model Collapse Demystified: The Case of Regression. arXiv:2402.07712.
- Dohmatob, E. et al. (2024b). Strong Model Collapse. arXiv:2410.04840.
- Duan, M., Suri, A., Mireshghallah, N. et al. (2024). Do Membership Inference Attacks Work on Large Language Models? arXiv:2402.07841; COLM 2024.
- Gerstgrasser, M. et al. (2024). Is Model Collapse Inevitable? Breaking the Curse of Recursion by Accumulating Real and Synthetic Data. arXiv:2404.01413.
- Guo, Y. et al. (2024). The Curious Decline of Linguistic Diversity: Training Language Models on Synthetic Text. NAACL Findings 2024.
- Havrilla, A. et al. (2024). Surveying the Effects of Quality, Diversity, and Complexity in Synthetic Data from Large Language Models. arXiv:2412.02980.
- Kandpal, N., Wallace, E., Raffel, C. (2022). Deduplicating Training Data Mitigates Privacy Risks in Language Models. arXiv:2202.06539; ICML 2022.
- Kazdan, J. et al. (2024). Collapse or Thrive? Perils and Promises of Synthetic Data in a Self-Generating World. arXiv:2410.16713.
- Lee, K. et al. (2021). Deduplicating Training Data Makes Language Models Better. arXiv:2107.06499; ACL 2022.
- Liang, W. et al. (2024). Monitoring AI-Modified Content at Scale. arXiv:2403.07183; ICML 2024.
- Morris, J. X. et al. (2025). How Much Do Language Models Memorize? arXiv:2505.24832.
- Seddik, M. E. A. et al. (2024). How Bad Is Training on Synthetic Data? A Statistical Analysis of Language Model Collapse. arXiv:2404.05090.
- Shi, L. et al. (2025). A Closer Look at Model Collapse: From a Generalization-to-Memorization Perspective. NeurIPS 2025 (arXiv preprint).
- Shi, W. et al. (2023). Detecting Pretraining Data from Large Language Models (Min-K%). arXiv:2310.16789.
- Shumailov, I. et al. (2023/2024). The Curse of Recursion: Training on Generated Data Makes Models Forget. arXiv:2305.17493; Nature 631 (2024).
- Xie, S. M. et al. (2023). DoReMi: Optimizing Data Mixtures Speeds Up Language Model Pretraining. NeurIPS 2023.
- Yang, Z. et al. (2024). Synthetic Continued Pretraining. arXiv:2409.07431.
- Zhang, C. et al. (2023). Counterfactual Memorization in Neural Language Models. NeurIPS 2023.
