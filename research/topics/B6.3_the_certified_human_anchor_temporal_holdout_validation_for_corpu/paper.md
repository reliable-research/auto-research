# The Certified-Human Anchor: Temporal Holdout Validation for Corpus-Level AI-Content Estimators — Pre-Registered Paper Specification

> Generated from digest.md + README.md. Status: specification, no experiments run.
> All ids (C1.., M1.., RQ1.., CO1..) refer to digest.md. No result below is real.

## Step 0 — Core Asymmetry (升维)

**The asymmetry:** *An anchor corpus's purity and its validity come apart under time: a pre-2022 human anchor whose every document is genuinely human-authored can still license a false error bound, because "certified human" is a time-stamped property of documents while the false-positive guarantee it backs is a property of the detector–distribution pair at a temporal distance from the certification date — so the guarantee decays with temporal distance even when not one label is wrong.*

**判据 (deletion test).** Delete the domain nouns: "An ___'s purity and its validity come apart under ___: a ___ whose every ___ is genuinely ___ can still license a false ___, because ___ is a property of ___ while the guarantee is a property of ___ at a ___ distance." — the residue is unevaluable: without *human authorship certified at a 2022 cutoff* vs. *detector FPR measured at a temporal distance from that cutoff*, there is no stated quantity that decays, no distance to decay along, and no sense in which purity and validity are distinct observables. The sentence has no generic truth value once the nouns are removed, so it is not a bridge ("A and B were never connected" does not appear anywhere in it; it names one object whose two properties are forced apart by one mechanism).

## Step 2 — Archetype

**Primary:** `empirical` (measurement study), per digest N12 — the deliverable is a measured FPR-drift magnitude and a validity envelope for a load-bearing methodological convention, propagated into the bias of a real prevalence estimator ([MonitorAIScale, OpenReview:bX3J7ho18S]).
**Secondary:** methodological audit / cautionary recommendation (CO4), subordinate to the measurement.

Downstream consequences:
- **(a) Abstract contribution slot:** a measured quantity + an envelope — "FPR drift of X pp per year of temporal distance; the pre-2022 anchor's implied bound holds only within window/genre/domain E" — not a new detector, dataset headline, or theorem.
- **(b) Intro logic:** "what becomes possible" — after this paper, any corpus-level AI-prevalence estimate can (and should) report an anchor-conditional error bound instead of asserting anchor validity. Not "we beat a number"; there is no leaderboard.
- **(c) Evidence standard for Results:** pre-registered trend statistics with placebo and confound-matched controls (Step 6), reported effect sizes with CIs, and explicit power per year-bucket. A negative (flat-drift) result is publishable under F-G1; a SOTA comparison is not required and will not be claimed.

## Step 3 — Taste Self-Audit

- **Bridge check:** FAIL if the opportunity is "temporal evaluation (LAMDA) meets AI-text detection". The Step-0 sentence does not connect two fields; it states that one object (the anchor) has two properties (purity, validity) that a single mechanism (temporal drift) forces apart. **PASS** as framed above.
- **Synthesis check:** FAIL if the method is "apply existing detectors to year-stratified data". The method's non-synthetic core is the *estimand*: the anchor-conditional FPR bound as a function of temporal distance, and its propagation into prevalence-estimator bias (M6) — a quantity no cited work defines or measures (digest N3 absence_comment). The detectors are instruments, not the contribution. **PASS**, conditional on the paper claiming the estimand + envelope, never the battery.
- **Verb check:** load-bearing verbs are *measure, bound, isolate, propagate, certify, decay* — none from the integrate/unify/leverage family. **PASS.**
- **Abstract-opening rule:** mechanism/asymmetry first (see Abstract v0); the "X is increasingly used… however… we introduce" template is not used. **PASS.**

No framing fix required; the idea skeleton stands as in digest N1/N12.

## Step 5 — Formal Problem Definition

**Estimand (R1).** The false-positive rate of a corpus-level AI-content estimator, evaluated on certified pre-2022 human text, as a function of temporal distance Δ between the document's publication year and the 2022 certification cutoff; unit of analysis = one (detector, year-bucket) cell; reference population = hard-timestamped human documents from a single continuously-archived source; the estimate feeds a go/no-go decision — whether a researcher may draw the estimator's human reference from a given historical year without an unstated bias.

**Notation.**
- Sources s ∈ S (single continuously-archived source per experiment, per N6 feasibility); year-buckets y ∈ Y = {y_min, …, 2021}; certification epoch y* = 2022 (cutoff date 2022-11-30). Temporal distance Δ(y) = y* − y.
- Anchor slice A_y = {d : source(d)=s, archival timestamp t(d) in year y, t(d) < cutoff}; |A_y| = n_y.
- Detectors D_k, k ∈ {1..K} (M2 battery), each with decision threshold τ_k fixed once on a held-out calibration split C ⊂ A_2021 at nominal FPR ν = 1% (see A4).
- Per-bucket empirical FPR: **FPR_k(y) = (1/n_y) Σ_{d∈A_y} 1[D_k(d) > τ_k]** (digest N8 metric 1).
- Drift model (M3): mixed-effects logistic regression logit P(flag_k(d)) = α_k + β_k·Δ(y(d)) + u_{s(d)}; β_k is the drift slope (metric 2). Trend corroboration: Mann-Kendall on {FPR_k(y)}.
- Validity envelope (M4): **E_k(ε, δ) = { y : UCB_{1−δ}(FPR_k(y)) ≤ ν + ε }**, with Clopper–Pearson upper bounds; pre-registered ε = 1 pp, δ = 0.05 (metric 4 made concrete).
- Prevalence-estimator bias (M6): for fixed target corpus T and mixture estimator π̂(T; H) with human reference H, **b(y) = π̂(T; A_y) − π̂(T; A_2021)** (metric 5).

**Adjective/verb → definition → measurement:**

| Load-bearing term (from digest Claims) | Formal definition | Measured by |
|---|---|---|
| "certified human" (Claim 1) | t(d) < 2022-11-30 per hard archival timestamp of source s | metadata filter + purity spot-check (A1) |
| "bounded, not zero, error guarantee" (Claim 1) | Clopper–Pearson 95% interval on pooled anchor FPR excludes 0 and its year-conditional UCB is not uniform in y | H1 |
| "drift" / "measurable confound" (Claim 2) | β_k > 0 with pre-registered significance and effect-size floor (H2) | M3 regression + Mann-Kendall |
| "independent of actual AI content" (Claim 2) | slope persists on buckets with y ≤ 2018 (pre-LLM) and under synthetic-drift injection on a fixed sample | B-alt arm, H2b |
| "boundary condition / validity envelope" (Claim 3) | E_k(1 pp, 0.05) as defined above | M4 over pilot + scale-up grid |
| "directional bias" downstream (Claim 4) | b(y) with sign and permutation-test CI | H3 |
| "temporally distant" | Δ(y) ≥ 8 years | corpus design (M1) |

Deleted adjectives: "silently", "uncharacterized" (rhetoric, no measurement); they may appear only in motivation prose, never in claims.

## Assumptions (A1..A6)

- **A1 (anchor purity floor).** Hard-timestamped pre-cutoff sources contain < 1% mis-provenanced/AI text. *Failure mode:* mis-dated or later-revised documents (C2, t1/t3). *Detection:* 1–2k-document human spot-check (N6 feasibility), run as an R2-validated instrument since it is a human-rubric annotation task, not a pass-through metadata read: (① provenance categories — "genuinely human-authored," "later-revised/ghostwritten," "mis-dated" — are grounded in the archival source's own timestamp/version-history metadata, not invented ad hoc; ② the rubric is drafted and refined on a small held-out pilot slice of ~100 docs before the full 1–2k spot-check; ③ **two independent human annotators** label the same spot-check sample, with inter-rater agreement required at **κ ≥ 0.7** before the impurity estimate is trusted; ④ any disagreement pattern is inspected for systematic collapse (e.g., one annotator always calling "later-revised" what the other calls "pure") rather than adjacent-category noise; ⑤ the rubric and threshold are frozen before the spot-check is scaled to the full sample) — if κ < 0.7, the rubric is refined and re-validated (guidance.md Part 4 situation 7) before any impurity number is reported. If estimated impurity ≥ 1%, all FPR bounds are reported as FPR ± impurity and H2 must additionally pass on the y ≤ 2018 sub-range. **Pilot gate PG-1.**
- **A2 (timestamp accuracy).** Publication-year metadata errors are rare (< 0.5%) and non-systematic. *Failure:* archive backfills, resubmissions. *Detection:* cross-check a 200-doc sample against independent archival snapshots during the walking skeleton.
- **A3 (within-source comparability).** Within one fixed source, year-buckets are comparable after matching per-year token budgets. *Failure:* topic/length composition drifts with year (t2 — the dominant feasibility risk per N6). *Detection:* composition diagnostics (topic-cluster and length distributions per bucket) + the B-alt matched arm; if B-alt kills the slope, A3 was violated and only the composition-conditional claim survives.
- **A4 (no threshold leakage).** τ_k is fixed on calibration split C ⊂ A_2021, disjoint from all evaluation buckets, before any evaluation FPR is computed. *Failure:* threshold tuned on evaluation years → circular envelope. *Detection:* enforced by pipeline order in the walking skeleton (thresholds hashed and frozen before evaluation runs).
- **A5 (estimator reproducibility).** The mixture prevalence estimator ([MonitorAIScale]) can be re-implemented/re-run with a swapped human reference. *Failure:* method under-specified or reference format incompatible. *Detection:* walking-skeleton step; if irreproducible, H3 falls back to a re-implemented mixture estimator of the same family, declared as such.
- **A6 (power).** n_y ≈ 3,000 docs/bucket suffices: for ν = 1%, a two-proportion test detects an absolute FPR difference of 1 pp between the earliest and latest bucket with power ≥ 0.9 at α = 0.0167. *Failure:* thin old buckets (C4, t5). *Detection:* per-bucket n and CI width reported; buckets with CI half-width > 1 pp are pre-declared **inconclusive**, never null. **Pilot gate PG-2:** the chosen source must supply ≥ 3,000 docs/year for ≥ 8 pre-2022 years, else switch source before scale-up.

## Step 6 — Pre-Registered Experiments

Common design (from digest N8 analysis_plan, hardened): per genre, 8–12 year-buckets × ~3,000 documents; K = 3 instance-level detector families ([DetectGPT, OpenReview:UiAyIILXRd], [LearnToDistance, OpenReview:2ZUPeEM3FH], [DnR, OpenReview:FiMZSxo4DO]) + the mixture estimator ([MonitorAIScale, OpenReview:bX3J7ho18S]); α = 0.05 with Bonferroni across the 3 detectors (per-test α = 0.0167). All thresholds frozen per A4. Success votes: "≥ 2 of 3 detector families" is the pre-registered aggregation rule throughout.

### E1 (RQ1 — what form of bound does the anchor license?)
- **Assumption:** A1, A2, A4, A6.
- **Hypothesis H1 (binary):** (i) pooled anchor FPR is nonzero — the 95% Clopper–Pearson lower bound on FPR_k pooled over all pre-2022 buckets is > 0.25% for ≥ 2/3 detectors; AND (ii) the bound is not uniform in time — max_y UCB_0.95(FPR_k(y)) > 2ν = 2% for ≥ 2/3 detectors. H1 passes iff both (i) and (ii) hold.
- **Metric:** FPR_k(y) and its Clopper–Pearson interval; envelope E_k(1 pp, 0.05) (Step 5).
- **Verification:** exact binomial CIs per bucket; pooled CI via stratified bootstrap (10,000 resamples) to respect bucket structure; no trend test needed for H1.
- **Fallback F1 (pre-committed wording):** "On strictly certified pre-2022 human text, tested corpus-level estimators achieve a uniform false-positive bound of ≤ 2% across 8–12 years at a threshold calibrated to 1% nominal FPR; the pre-2022 anchor licenses a flat, near-nominal guarantee within the tested envelope, and we release the year-stratified benchmark (CO1) that certifies it."

### E2 (RQ2 — does human stylistic drift erode the anchor? Central hypothesis.)
- **Assumption:** A1, A2, A3, A4, A6.
- **Hypothesis H2 (binary):** for ≥ 2/3 detectors, ALL of: (a) mixed-effects slope β_k > 0 with p < 0.0167; (b) effect-size floor: odds ratio per year of temporal distance ≥ 1.05 (i.e., ≥ ~5% relative FPR growth/year); (c) Mann-Kendall trend on {FPR_k(y)} with p < 0.05, positive.
- **Hypothesis H2b (mechanism check, binary; effect floor added per guidance.md §3.1 — significance without magnitude is not a pass):** synthetic-drift injection (M5: graded lexical/syntactic perturbation of a *fixed* A_2021 sample, 5 intensity levels) produces a monotone FPR increase (Mann-Kendall p < 0.05) **of at least 1 percentage point absolute between the lowest and highest perturbation intensity** for ≥ 2/3 detectors — establishing that stylistic change alone can move FPR by a magnitude comparable to H2's real-data slope, not merely a statistically detectable but practically negligible amount, per digest N9/RQ2.
- **Metric:** β_k (log-odds per year of Δ), FPR_k(y) curve, change-point year via segmented regression (digest N8 metrics 2–3).
- **Verification:** mixed-effects logistic regression (flag ~ Δ + (1|source); single source in pilot ⇒ intercept-only random effect degenerate, then plain logistic with cluster-robust SEs by bucket), Bonferroni across detectors; Mann-Kendall as nonparametric corroboration; both must agree in sign.
- **Fallback F2 (pre-committed wording):** "Cross-year false-positive drift on certified human text is below 5% relative growth per year for the tested detector families and genres: within the 2007–2021 window, human stylistic drift does not measurably erode the pre-2022 anchor, and the anchor's validity envelope is bounded by sample coverage, not by drift." (Combines with F1 into F-G1 if H1(ii) also fails.)

### E3 (RQ3 — does anchor age bias the corpus-level estimand?)
- **Assumption:** A4, A5, A6 (+ H2 machinery, but E3 runs regardless of H2's outcome).
- **Hypothesis H3 (binary):** with target corpus T fixed (a held-out post-2022 human + synthetic mixture of known composition, and separately a real post-2022 corpus), swapping the human reference from A_2021 to the earliest bucket (Δ ≥ 8 years) shifts the estimated AI-fraction by **|b(y_min)| ≥ 2 pp absolute, in the positive direction (aged reference ⇒ higher π̂), with paired permutation test p < 0.05 (10,000 permutations over document-to-reference assignments)**.
- **Metric:** b(y) = π̂(T; A_y) − π̂(T; A_2021) across all reference buckets; monotonicity of b(y) in Δ (Mann-Kendall, secondary).
- **Verification:** permutation test per digest N8 analysis_plan; on the known-composition T, additionally report b(y) against ground-truth π (absolute bias, not just shift).
- **Fallback F3 (pre-committed wording):** "The mixture-based prevalence estimator is robust to anchor age: swapping human references across an 8–14-year span moves the estimated AI-fraction by < 2 pp on fixed targets, so anchor-temporal validity, even where per-document FPR drifts (H2), does not propagate to the corpus-level estimand at practically relevant magnitude."

### Mandatory baselines

- **B0 — "why do this at all" control: the anchor-as-asserted arm.** Current practice: calibrate on the anchor-adjacent year and assume the resulting nominal bound (ν = 1%) holds over the whole pre-2022 anchor. B0 simply reports that asserted bound alongside the measured year-conditional envelope. The problem exists iff B0's asserted bound is violated (H1(ii)) — if B0 is never violated, the paper's premise collapses into F-G1. B0 also includes a **year-shuffle placebo**: permute year labels across documents within the source and re-fit E2; the placebo slope must be null (|β| CI covering 0) or the pipeline is measuring an artifact — a hard validity gate, not a hypothesis.
- **B-alt — strongest-alternative-explanation control.** **Rival explanation:** the FPR-vs-year slope is not human stylistic drift but (r1) year-correlated composition drift within the source (topic/length/genre mix; C1(a) vs t2), or (r2) undetected AI leakage into late pre-2022 buckets (C1(b), C2). Budget-matched arm: re-run E2 on **composition-matched buckets** — resample each A_y stratified to a common topic-cluster × document-length distribution (equal per-bucket n and token budget as the main arm), and separately re-fit the slope on the **y ≤ 2018 sub-range** (pre-LLM, immune to r2). H2 is attributed to stylistic drift only if the slope survives (same sign, p < 0.0167) in BOTH matched and ≤2018 arms; otherwise the claim is downgraded to the pre-committed wording: "the pre-2022 anchor's FPR is non-stationary in calendar time, but the drift is attributable to corpus-composition change rather than writing-style change — the anchor is invalid as used either way, but the mechanism differs." (Note: this downgrade still supports Claims 1/3/4; only Claim 2 falls.)

### Global fallback F-G1 (archetype pivot)

If the central family {H1(ii), H2, H3} all fail, pivot within `empirical` from *drift-erosion measurement* to *robustness certification of the convention* (CO1 becomes the headline, CO4 flips sign). Pivoted abstract sentence, pre-committed: **"A pre-registered temporal-holdout audit across 8–12 year-stratified certified-human buckets, three detector families, and a mixture prevalence estimator finds the pre-2022 human anchor temporally stable — FPR flat within ±1 pp of nominal and prevalence estimates invariant to reference age within 2 pp — providing the first quantified license, with an explicit envelope, for the field's most common calibration assumption."**

## Step 9 — Walking Skeleton

**One binary question:** *Can this pipeline measure a between-year FPR difference at all — i.e., does it produce deterministic, threshold-frozen, per-bucket FPRs whose CIs are tight enough (half-width ≤ 2 pp) to make H2 falsifiable?*

- **Arms (3):** (1) DetectGPT-style curvature detector (single open ~1–3B LM); (2) the same detector on the year-shuffle placebo (B0 gate); (3) minimal mixture-estimator run π̂(T; A_2021) vs π̂(T; A_2008) on one small fixed target (A5 check).
- **Smallest task set:** arXiv abstracts, single source, 3 buckets {2008, 2015, 2021}, 300 docs/bucket + 300-doc calibration split from 2021 (τ frozen first, hash logged).
- **Deterministic metrics only:** FPR per bucket (exact count / 300), Clopper–Pearson intervals, placebo slope sign, b(2008) point value. No trend fitting, no significance claims.
- **Expected cost:** ≤ 1 GPU-day on one mid-size GPU + < $50 API (consistent with digest N6 feasibility: ~10^3–10^4 inferences).
- **Pass criterion (explicit):** (i) identical FPR values to 3 decimals on a full rerun (determinism); (ii) all bucket CI half-widths ≤ 2 pp at n = 300 — implying ≤ 1 pp at n = 3,000 (A6); (iii) placebo arm shows no ordering artifact; (iv) mixture estimator executes with swapped references (A5) and PG-1/PG-2 data checks pass. **Skeleton passed ⇒ scale-up to 8–12 buckets × 3,000 docs × 3 detectors × 3–4 genres is a config change (bucket list, n, detector registry), not a code change.** Any code change required for scaling = skeleton failed; fix and re-run skeleton before any grid.

## Claim–Evidence Map

| Claim (digest Claims 1–4, final-abstract candidates) | Traces to | Status |
|---|---|---|
| 1. Pre-2022 anchor licenses a bounded, not zero, guarantee, never previously made explicit | H1 (E1); "certified"/"bounded" defs (Step 5); novelty via N3 absence_comment | needs-experiment; fallback-covered (F1) |
| 2. Human stylistic drift is a measurable FPR confound independent of AI content | H2 + H2b (E2) + B-alt survival | needs-experiment; fallback-covered (F2 / B-alt downgrade wording) |
| 3. Measured drift defines an explicit validity envelope (time/genre/domain) | E_k(ε,δ) definition (Step 5, supported-by-design) + H1/H2 outcomes fill it | needs-experiment (envelope contents); supported-by-design (envelope form) |
| 4. Downstream prevalence estimates carry directional bias without a stated temporal-validity bound | H3 (E3) | needs-experiment; fallback-covered (F3) |
| Methodological recommendation (CO4: report anchor bounds, don't assume) | Holds under every branch: H-pass, B-alt downgrade, and F-G1 (where it flips to a positive license) | supported-by-design |

Every abstract claim above maps to an H-id or a Step-5 definition; no orphan claims permitted at write-up time.

## Abstract v0 (draft, mechanism-first — DRAFT BEFORE RESULTS; all quantities pending)

An anchor corpus's purity and its validity come apart in time: a pre-2022 "certified-human" reference can be label-perfect and still license a false error bound, because the false-positive guarantee it backs is a property of the detector–distribution pair at a temporal distance from the certification date, not of the labels. We formalize that gap and measure it. Using a temporal-holdout protocol over year-stratified, hard-timestamped human corpora (8–12 buckets, three detector families), we isolate false-positive-rate drift as a function of temporal distance, separate stylistic drift from composition and leakage rivals via matched resampling, pre-LLM sub-range tests, and synthetic-drift injection, and propagate the drift into the bias of a mixture-based corpus-level prevalence estimator under reference-year swaps. The output is an explicit validity envelope — time window, genre, domain — bounding when a pre-2022 anchor's guarantee holds, replacing an assumption with a reported quantity. *(≈140 words)*
