# What Probes Predict Breakage? Minimal Probe-Set Design for Version-Drift Auditing — Pre-Registered Paper Specification
> Generated from digest.md + README.md. Status: specification, no experiments run. All ids (C1.., M1.., RQ.., CO..) refer to digest.md.

## Step 0 — Core Asymmetry (升维)

**Invariant.** Whether a version update breaks a downstream integration is determined not by *how much* the model's behavior drifts but by *whether the drift lands on the specific behavioral axis that integration reads* — a parser breaks on format drift, a policy filter on refusal drift — so downstream breakage is a **sparse, axis-selective** function of drift, not a monotone function of drift size.

**判据 test (delete the domain nouns).** "Whether a ⟨X⟩ breaks a ⟨Y⟩ is determined not by how much the ⟨Z⟩ drifts but by whether the drift lands on the specific ⟨W⟩ that ⟨Y⟩ reads — so breakage is a sparse, selective function of drift, not a monotone function of drift size." → With *version update / integration / model behavior / behavioral axis / parser / format-refusal drift* removed, "the specific ⟨W⟩ that ⟨Y⟩ reads" has no referent and the sentence becomes uninterpretable/empty. The claim's content is carried entirely by the domain nouns (integrations *consume outputs* through parsers and policies that key on specific axes). It is therefore an invariant, not a bridge. ✓

---

## Step 2 — Archetype (digest N12 = `empirical`)

- **Primary archetype:** Measurement / characterization study — *"which of five observable behavioral axes actually governs downstream breakage"* — a comparative predictive-validity measurement, not a new model or a benchmark-beat.
- **Secondary archetype:** Methodological artifact — the validated **minimal probe subset** (CO1) packaged as an audit protocol (CO3).

Downstream consequences:
- **(a) Abstract contribution slot:** an empirical *ranking* of probe families by predictive power for real breakage (CO2) + the *smallest sufficient subset* (RQ_INF_1) — not a tool pitch.
- **(b) Intro logic:** "what becomes possible" — audit a version bump with a ≤2-family probe run once per version instead of a full downstream re-test — *not* "beat a number."
- **(c) Evidence standard:** correlational predictive validity across held-out retrospective version pairs, gated by (i) a within-version sampling-noise floor and (ii) paraphrase rank-stability, and isolated from a family-agnostic total-drift rival. Correlations that survive all three gates count; raw ρ alone does not.

---

## Step 3 — Taste self-audit

- **Bridge?** The opportunity is *not* "probes and breakage were never connected, we connect them." It is an asymmetry: predictive power is decoupled from drift magnitude and concentrated on a sparse axis subset. PASS.
- **Mere synthesis?** Risk: "we assemble five existing single-axis instruments." Correction (skeleton-level, not sentence-level): the deliverable is the **adjudication** — which axis *governs* breakage net of the others (partial correlation, M7) and the *minimal* subset — a measurement result the five instruments individually cannot produce. The battery is instrumental, not the contribution. PASS after reframing.
- **Load-bearing verbs from integrate/unify/leverage family?** Removed. Replaced with **formalize / measure / gate / isolate / adjudicate**.
- **Abstract-opening rule:** opens on the mechanism (axis-selective sparse breakage), not "X is increasingly used… however… we introduce." COMPLIANT (see Abstract v0).
- **Classical-thread concession (design-review addition, requires harvest — see digest.md N3 [UNVERIFIED] block):** the "minimal subset of cheap tests that retains fault-detection power" idea is not new in the abstract — it is the core of **regression test selection / test-suite minimization** (Yoo & Harrold survey; Rothermel & Harrold), and "cheap monitor predicts expensive degradation" is the core of **concept-drift detection** (Gama et al. survey). The paper must concede these explicitly rather than claim first-mover status. The **defensible** novelty is the *transposition that breaks*: these classical methods assume a deterministic pass/fail oracle and white-box coverage (test-suite min.) or a streaming label feed (concept drift); this paper has none of those — the "fault" is a probabilistic *behavioral* drift on a chosen *axis*, black-box, across two discrete version checkpoints. Axis-resolved black-box breakage prediction is the residual gap; the minimality criterion itself is inherited and credited. **[UNVERIFIED — specific citations pending harvest; never assert as verified.]**

---

## Step 5 — Formal Problem Definition

**Estimand (R1, guidance.md §3.4).** The quantity of interest is `π_f` — the predictive power of behavioral probe-family `f`'s cross-version drift for real downstream-task breakage — estimated per family (and, net of collinearity, per family conditional on the other four) over the reference population of already-shipped LLM version pairs with a shared, re-administrable downstream input set; the decision it feeds is which minimal probe subset a team should run once per version bump in place of a full downstream re-test.

**Notation.** Version pair `p = (v_old, v_new)`, `p ∈ P`. Probe families `F = {cap, ref, fmt, cal, saf}` (M1–M5), index `f`. Each family has an item set `I_f`. Downstream tasks `t ∈ T`, with input set `X_t`. Unit of analysis = cell `(p, t)`; target n ≈ 20 pairs × 20 tasks ≈ 400 (pilot ≈ 4 × 10 = 40), per digest N8 analysis plan.

| adjective/verb (from Claims) | formal definition | how measured |
|---|---|---|
| **drift magnitude** `D_f(p)` | signed scalar = family-aggregated change in the family's instrument output between `v_old`,`v_new` on `I_f`; per M1–M5 (accuracy Δ; Refusal-Index & refusal-rate Δ; schema-validity/structural-match Δ; semantic-calibration/ECE Δ; accept/refuse & over-refusal Δ) | run `I_f` on both versions under fixed decoding; aggregate per-item deltas to signed magnitude (M1–M5) |
| **downstream breakage** `B(p,t) ∈ [0,1]` | `1 − FuncEquiv(v_old, v_new; X_t)` where FuncEquiv = fraction of `X_t` passing per-task functional-equivalence checks (schema validity, tool-call executability) combined with a semantic-diff threshold (M6) | run `X_t` through both versions; deterministic validators + semantic diff (the seed's 真值) |
| **predictive power** of family `f` | `π_f = |Spearman ρ( D_f(p), B̄(p) )|`, `B̄(p) = mean_t B(p,t)`; plus standardized coeff `β_f` in a multiple regression `B̄ ~ Σ_f D_f` | bootstrap over `P` (10k resamples), 95% CI (M7, N8) |
| **minimal (probe subset)** | subset `S ⊆ F` with `AUC(S) ≥ AUC(F) − δ`, `δ = 0.03`; **minimal-sufficient** `S* = argmin_{S} |S|` s.t. that holds | grouped (by pair) 5-fold CV of a breakage classifier on family-drift features (M7) |
| **robust / stable (drift)** | `D_f` **exceeds noise floor** iff `median_p |D_f(p)| > Q_{0.95}(null_f)`, `null_f` = within-version re-decoded drift; **rank-stable** iff `Kendall τ` of the family π-ranking across ≥3 paraphrase sets `≥ 0.7` | within-version re-sampling null + paraphrase resampling (RQ_INF_2, C5) |
| **sparse / axis-selective** | ∃ `S*` with `|S*| ≤ 2` achieving the minimal-sufficient criterion above | RQ_INF_1 ablation |

Any adjective without a row above is deleted from the claims.

**R3 confound-removal ledger (guidance.md §3.4).** Every design constraint below names the specific confound it removes — an unnamed-confound constraint is decoration, per R3:
- Anchoring the corpus backbone on immutably-archived open-weight checkpoints removes the **provider-side survivorship confound**: deprecated closed-API snapshots would otherwise silently shrink the sample toward whichever pairs happen to still be reachable, biasing which drift magnitudes get observed (A1).
- Running the identical 5-family probe battery and downstream suite under fixed decoding on both `v_old` and `v_new`, with a within-version re-decoded null, removes the **decoding-noise confound**: without it, apparent "drift" could be resampling variance rather than a real version-to-version change (A2).
- The **B-alt** family-agnostic total-drift arm, budget-matched to the 5-family battery, removes the **update-magnitude confound**: without it, any family's apparent predictive power could just be tracking how big the update was overall, not which axis it landed on.
- The **B0** constant base-rate predictor removes the **any-signal-at-all confound**: without it, a family could look "predictive" relative to the other families while still being no better than guessing the mean breakage rate.
- The **P0** label-shuffle placebo removes the **pipeline-artifact / leakage confound**: without it, apparent predictive power could arise from a CV grouping leak or a per-pair nuisance shared by drift and breakage (prompt length, decode temperature) rather than a real drift→breakage relationship. Its effect is null *by construction* when the pair-level correspondence is permuted; a non-null P0 invalidates the run before any H\* is scored.
- Computing `B(p,t)` per task, before pooling across the downstream suite, removes the **task-heterogeneity-averaging confound** (A5): pooling raw diffs first would let a format-sensitive task's breakage cancel against a calibration-sensitive task's non-breakage.
- Fitting `B̄ ~ Σ_f D_f` **jointly** (M7) rather than five univariate correlations removes the **family-collinearity confound** (A4, C4): a family's raw correlation with breakage would otherwise be inflated by whatever it merely shares with correlated families.

**Mechanism analysis (R6, guidance.md §3.4 — ≥1 required for the A2 archetype).** Comparing each family's raw `π_f` (Spearman ρ) against its standardized partial coefficient `β_f` from the same joint fit (M7) is this study's mechanism-layer analysis: it distinguishes a family whose predictive power is its own independent signal from one that merely rides a correlated axis (C4) — e.g. if safety-behavior's raw ρ is high but its `β_f` collapses once refusal-boundary is included, the governing mechanism is "refusal drift, with safety as a correlated proxy," not two independent causes. This is exactly RQ6/H6 below, not a separate unbudgeted analysis.

---

## Assumptions (A1..A7)

- **A1 (retrospective queryability).** For ≥ the pilot pairs, both versions are runnable on identical inputs (immutable open-weight checkpoints). *Fail:* deprecated/unpinned endpoints (C3). *Detect:* walking-skeleton gate — cannot administer `I_f` to both versions ⇒ pair dropped; corpus anchored on HuggingFace-archived open weights, closed-API as best-effort stratum (N6 feasibility). *Gate:* **PG-1**, checked in the pilot — admission to the corpus is itself gated on this check before any drift is computed. *Consequence:* an unqueryable pair is dropped (never imputed) and excluded from every headline `n` (R8); H5/RQ5 exists precisely to test whether the pairs that survive this gate are a biased subsample of the pairs that don't.
- **A2 (estimable noise floor).** Within-version decoding variance is measurable and, for ≥3 families, below cross-version drift. *Fail:* drift ⊂ noise band. *Detect:* RQ_INF_2 null distribution; if unmet, family excluded from ranking claims. *Gate:* scale-up phase (Phase C) — the skeleton runs fixed decoding only and does not re-sample, so this gate cannot fire until the re-decoded null is computed at scale. *Consequence:* a family that fails this gate is dropped from H1's ranking and from the minimal-subset search (H2), not silently kept.
- **A3 (construct validity of B).** Output-diff-with-functional-checks reflects real breakage (C2, t1). *Fail:* large harmless diffs / tiny fatal diffs dominate. *Detect:* **R2 instrument-validation sequence** (guidance.md §3.4) for the FuncEquiv-plus-semantic-diff classifier that computes `B(p,t)`: ① ground the pass/fail criteria in the downstream task's own pre-existing acceptance tests (JSON-schema files, tool-call signatures, moderation policy documents already in production use for that task, not invented ad hoc); ② draft the semantic-diff threshold wide on a held-out calibration slice of `(p,t)` cells, refine with named merge/split operations until borderline cells stop reclassifying under small threshold perturbations; ③ validate the automated call against **≥2 independent human raters** on a held-out labeled subset (40–80 annotator-hrs, N6), requiring **Cohen's/Fleiss' κ ≥ 0.7** between automated and human labels; ④ inspect the confusion structure — disagreements must cluster on genuinely ambiguous near-threshold cells, not systematically favor one task or direction; ⑤ freeze (hash) the threshold before any pair enters the scored corpus. *Gate:* **PG-2** for steps ①–② and a lightweight version of ③–④ on the skeleton's 15 cells (schema-validity/tool-call-executability only, deterministic); the full human-rater κ validation is a Phase-C-scale gate before the scored corpus is frozen. *Consequence:* if κ < 0.7, do not scale — simplify the FuncEquiv criterion (fewer, coarser pass/fail bins) and re-validate (guidance.md Part 4 situation 7); every downstream H\* (H1, H2, H4, H6) is blocked on this gate passing first, since all of them consume `B(p,t)`.
- **A4 (identifiability).** The five family-drift features are not perfectly collinear (C4). *Fail:* VIF ≫ 10, partial correlations undefined. *Detect:* VIF check + partial-correlation stability (M7); if collinear, report at the bundle level, not per-family. *Gate:* Phase C (scale-up) — VIF across 5 families needs ≥3 families in the design simultaneously; the skeleton only runs 2 (`ref`, `cap`) and cannot exercise this check. *Consequence:* if VIF ≫ 10 for any subset, H1/H6's per-family attribution is downgraded to a bundle-level statement ("this correlated group of families predicts breakage") rather than a single-family claim.
- **A5 (heterogeneous downstream).** `T` spans distinct sensitivities (format-, refusal-, calibration-sensitive tasks) (C2). *Fail:* all tasks break on one axis. *Detect:* per-task `B(p,·)` variance before pooling (M6, N8). *Gate:* **PG-3** — the skeleton already spans 5 heterogeneous downstream tasks, so per-task variance can be inspected even at pilot scale. *Consequence:* if all tasks break on one axis, H4/RQ4 (task-heterogeneity) is pre-declared FAIL and Claim 4's scope narrows to that one axis rather than being asserted as general.
- **A6 (power).** *Fail:* too few pairs / wide CIs. *Detect:* bootstrap CI width gate; if unmet ⇒ demote to Fallback wording (t3). *Gate:* Phase D (verdict lookup) — the CI-width check runs once the corpus and its bootstrap are computed.

  **Honest power arithmetic (design-review fix, 2026-07-04) — the central test operates at the PAIR level, not the cell level.** `π_f = |Spearman ρ(D_f(p), B̄(p))|` and the joint fit `B̄(p) ~ Σ_f D_f(p)` both have effective n = **number of version pairs `|P|`**, not the ≈400 `(p,t)` cells (the cells collapse into `B̄(p)`, one value per pair; the bootstrap and grouped-CV correctly resample at the pair level, so cells within a pair are *not* independent replicates). By Fisher-z, two-sided α=0.05, the power to detect a true `ρ = 0.30` (the H1 effect floor) is **≈0.25 at `|P|=20`, ≈0.47 at `|P|=40`, ≈0.65 at `|P|=60`, and only reaches 0.80 at `|P|≈85`.** H1's *actual* confirmatory test is stricter still — a paired-bootstrap CI on `π_top − π_cap` with lower bound `>0`, Holm-corrected across 10 family pairs — so it needs *more* pairs than a single correlation. **`|P|≈20` therefore does NOT power the confirmatory ranking claim; asserting it does was a Phase-A rubber-stamp.**

  **Pre-committed power policy:** (i) at `|P| < 40`, H1's paired-difference claim is reported as **EXPLORATORY** (point estimates + CIs, no confirmatory PASS/FAIL); (ii) the confirmatory H1 verdict (`π_top − π_cap` lower bound `>0`, Holm-corrected) is only scored PASS/FAIL at `|P| ≥ 60` (power ≥0.65); below that the family ranking is pre-declared **INCONCLUSIVE**, never FAIL (guidance.md Part 4 situation 5) — an underpowered non-detection is not a null. (iii) Reaching `|P| ≥ 60` is config-not-code (more archived open-weight successions: Llama-2/3/3.1/3.2, Qwen1.5/2/2.5/3, Mistral/Gemma/Phi minor bumps, plus dated-API strata), so the honest move under a thin corpus is *collect more pairs* (situation 10: shrink task conditions, never n per pair), not to claim a ranking the design cannot resolve.

  *Consequence:* **per-cell power floor (R8):** a `(p,t)` cell needs ≥50 valid downstream inputs surviving decode/attrition (out of the ~200 per task, N6) to contribute to `B(p,t)`; cells below that floor are pre-declared **INCONCLUSIVE** (never scored as null, never silently dropped — situation 5), excluded from the headline `n` and reported in a supplementary thin-cell table. The same rule applies at the family level: a family whose pair-level CI-width gate is unmet is INCONCLUSIVE for the ranking, not FAIL.
- **A7 (instrument stability).** Per-family drift is paraphrase-stable enough to preserve the ranking (C5). *Fail:* ranking reorders across paraphrase sets. *Detect:* RQ_INF_2 Kendall τ gate. *Gate:* Phase C (scale-up) — Step 9's walking skeleton explicitly excludes the paraphrase loop (adding it is the scale-up step, not new code), so this gate cannot fire at pilot scale. *Consequence:* if τ < 0.70, RQ1's ranking is downgraded to "instrument-limited: only families {…} carry rank-stable drift" (t2), and C5's construct threat is reported explicitly rather than the ranking being asserted at face value.

---

## Step 6 — Pre-Registered Experiments

### RQ1 (digest N8, GIVEN) — Which probe family is most predictive of downstream breakage?
- **Assumption:** A1, A3, A4, A5, A6.
- **Hypothesis H1 (binary):** The family with the highest bootstrap-median `π_f` is **`ref` or `saf`**, with `π_top ≥ 0.30`, AND the paired-bootstrap difference `π_top − π_cap` has a 95% CI with lower bound `> 0` (top family strictly beats capability).
- **Metric:** `π_f = |Spearman ρ(D_f, B̄)|` and standardized `β_f`; per digest N8 metrics.
- **Verification:** bootstrap over `P` (10k resamples) for each `π_f` CI; paired bootstrap/permutation test for pairwise π-differences at **α = 0.05** with **Holm correction** across the 10 family pairs; report `β_f` from `B̄ ~ Σ D_f` with VIF.
- **Aggregation:** single joint-regression estimate per family — no multi-instrument vote; `π_f`/`β_f` are the bootstrap-median over all `|P|` retrospective pairs, not an aggregate across independent instruments. Cells failing the A6 per-cell power floor are excluded before aggregation (INCONCLUSIVE, not folded in as zero).
- **Power gate (A6):** effective n = `|P|` version pairs. The confirmatory H1 verdict is scored **only at `|P| ≥ 60`** (power ≥0.65 for `ρ=0.30`); at `|P| < 40` it is EXPLORATORY, and `40 ≤ |P| < 60` is pre-declared **INCONCLUSIVE**, never FAIL. The corpus target is therefore `|P| ≥ 60` (config-not-code, per A6), not the earlier ≈20.
- **Fallback:** If `cap` ranks #1 → claim *"raw-capability drift, not policy/format drift, dominates downstream breakage"* (digest N9 Result 1 falsification path). If **no** family reaches `π ≥ 0.30` → claim *"no single axis is individually predictive; breakage is multivariate,"* handing the burden to RQ_INF_1.

### RQ_INF_1 (digest N8, inferred) — Smallest family subset retaining most predictive power?
- **Assumption:** A3, A4, A5, A6.
- **Hypothesis H2 (binary):** The minimal-sufficient subset `S*` (`AUC(S*) ≥ AUC(F) − 0.03`) has **`|S*| ≤ 2`**.
- **Metric:** `ΔAUC = AUC(F) − AUC(S)`, grouped 5-fold CV (fold = held-out version pairs) of a breakage classifier on family-drift features; forward+backward subset search over the 5 families (M7, N8).
- **Verification:** nested CV to avoid subset-selection leakage; bootstrap 95% CI on `ΔAUC(S*)`; accept only if CI upper bound `< 0.03`.
- **Aggregation:** `ΔAUC(S*)` is the grouped 5-fold-CV mean over folds (fold = held-out version pairs), itself bootstrapped for the 95% CI — no cross-instrument vote; the subset search is over the 5 families jointly, not five independent per-family tests.
- **Fallback:** If minimal `|S*| = 5` (AUC degrades ~linearly as families drop; digest N9 Result 2 falsification) → claim *"all five axes carry non-redundant breakage signal; the full battery IS the minimal set — no compression exists,"* still a publishable design verdict (rejects the 'minimal' premise honestly).

### RQ_INF_2 (digest N8, inferred) — Is the drift signal above noise and paraphrase-stable?
- **Assumption:** A2, A7.
- **Hypothesis H3 (binary):** For **≥3 of 5** families, `median_p |D_f| > Q_{0.95}(null_f)` (drift beats the within-version noise floor), AND the family π-ranking has **Kendall τ ≥ 0.70** across ≥3 paraphrase sets.
- **Metric:** drift/noise ratio vs. within-version re-decoded null; Kendall τ of rankings across paraphrase sets (M3, M6, M7).
- **Verification:** within-version null from ≥3 re-sampled decodings per item; one-sided permutation test per family at α=0.05 (Holm across families); τ computed pairwise across paraphrase sets, min reported.
- **Aggregation:** pre-registered vote rule (stated in H3 itself) — the noise-floor half passes if **≥3 of 5** families individually clear their own gate; the paraphrase half reports the **minimum** pairwise Kendall τ across all paraphrase-set comparisons (not the mean), so one unstable pairing cannot be averaged away.
- **Fallback:** If drift ⊆ noise band for a family, or ranking reorders (τ < 0.70; digest N9 Result 3 falsification) → downgrade RQ1's ranking to *"instrument-limited: only families {…} carry drift above noise,"* and flag the C5/t2 construct threat explicitly in the results.

### RQ4 (pipeline.md Stage 6 `rq_downstream_heterogeneity`, formalized here) — Does downstream breakage vary meaningfully by task sensitivity?
- **Assumption:** A5.
- **Hypothesis H4 (binary):** For at least 2 of the pre-declared task-sensitivity contrasts (format-sensitive vs. calibration-sensitive; safety-sensitive vs. capability-sensitive), the per-family drift-to-breakage correlation differs by **≥0.15** in absolute Spearman ρ, with the paired-bootstrap 95% CI on the difference excluding 0 — i.e. breakage is genuinely task-heterogeneous, not driven by one axis-agnostic factor.
- **Metric:** per-task, per-family `ρ_f(t) = Spearman ρ(D_f(p), B(p,t))` across pairs `p`, compared across the pre-declared task-sensitivity contrasts.
- **Verification:** paired bootstrap over `P` (10k resamples) for the ρ-difference CI per contrast; Holm correction across the pre-declared contrasts examined.
- **Aggregation:** restricted to the 2 pre-registered task-pair contrasts with the sharpest a-priori sensitivity difference — not a post-hoc search over all task pairs (which would inflate false positives).
- **Fallback:** If no examined contrast clears the ≥0.15 bar → claim *"breakage correlates with drift comparably across the tested task-sensitivity contrasts; any heterogeneity is smaller than this design can resolve,"* narrowing Claim 4's scope rather than asserting heterogeneity by fiat.

### RQ5 (pipeline.md Stage 6 `rq_corpus_attrition_bias`, formalized here) — Is the retained corpus biased by closed-API attrition?
- **Assumption:** A1.
- **Hypothesis H5 (binary, equivalence-framed — design-review fix 2026-07-04):** attrition does not bias the retained sample, tested as **equivalence** not as failure-to-reject. For each family, the standardized mean difference in `|D_f(p)|` between the "became-unreachable" and "fully-reachable" strata falls **within ±`Δ_eq = 0.5 SD`** (a TOST two-one-sided-test at α=0.05, Holm-corrected across the 5 families). PASS = equivalence established (both one-sided tests reject) for all 5 families; FAIL = equivalence rejected (a family's difference exceeds the margin) for ≥1 family.
- **Effect floor:** `Δ_eq = 0.5 SD` — a difference smaller than this is pre-declared "not a meaningful attrition bias"; larger triggers the narrowing fallback. (Framing a null as "p>0.05" is banned here: with few attrited closed-API pairs a plain two-sample test is underpowered and would rubber-stamp "unbiased" from no evidence.)
- **Metric:** per-family standardized mean difference in `|D_f(p)|` between the "became-unreachable" and "fully-reachable" strata.
- **Verification:** TOST equivalence test per family against ±0.5 SD; Holm correction across 5 families; α=0.05.
- **Aggregation:** pooled across every pair that experiences attrition during the study window (open-weight and closed-API strata alike).
- **INCONCLUSIVE route (instrument/power failure ≠ substantive null):** if the attrited stratum has too few pairs to power the TOST (per the A6 pair-level policy — fewer than the n needed to resolve ±0.5 SD), H5 is **INCONCLUSIVE**, and every headline ranking is reported *both* pooled and on the attrition-free open-weight-only subset (the caveat is carried, not resolved by fiat).
- **Fallback:** If equivalence is rejected for any family → not a B0/P0-style invalidation, but the claim narrows: *"the retained corpus is attrition-biased on {family}; headline rankings involving {family} are reported with this caveat and re-derived on the attrition-free open-weight-only subset as a robustness check"* (guidance.md Part 4 situation 9 — narrow to the conditions of agreement).

### RQ6 (pipeline.md Stage 6 `rq_family_collinearity_partial`, formalized here) — Does raw correlation misattribute predictive power under collinearity?
- **Assumption:** A4.
- **Hypothesis H6 (binary):** For at least 1 of the 5 families, the rank order under raw pairwise `π_f` and under the VIF-checked partial coefficient `β_f` (net of the other 4, from the same M7 fit) disagrees by **≥1 position** — collinearity is non-negligible and raw correlation alone would misattribute predictive power. This is the mechanism analysis required by R6 (see note above Assumptions).
- **Metric:** `rank(π_f)` vs. `rank(β_f)` across the 5 families, from the single joint fit shared with H1.
- **Verification:** VIF check (must be `< 10` for the partials to be trusted, per A4); the rank comparison is deterministic given the fitted values, so no separate significance test is needed for the disagreement itself — but each `β_f`'s bootstrap CI (shared with H1) determines whether a rank flip is distinguishable from noise.
- **Aggregation:** a secondary readout of the same M7 fit used for H1 — not an independent re-estimation.
- **Fallback:** If ranks never disagree (VIF-checked partials always match raw-ρ ranks) → claim *"the five families are empirically near-orthogonal in this corpus; raw correlation and partial attribution agree, so C4's identifiability concern does not bite in practice"* — a reportable finding in its own right (an assumption's failure mode not occurring is still worth stating, not silently omitted).

### Mandatory baselines and the null-by-construction placebo

**Two distinct arms are needed and were previously conflated (design-review fix, 2026-07-04): a *performance floor* (B0) and a *null-by-construction placebo* (P0). A constant base-rate predictor is a floor to beat, NOT a placebo — it cannot come out "non-null by artifact," so it cannot detect a leaking pipeline. Phase D's "placebo first" gate (goal.md §5, guidance.md Part 4 situation 1) requires an arm whose effect *must* be null if the pipeline is clean.**

- **P0 — null-by-construction placebo (label-shuffle), checked BEFORE any H\*:** randomly permute the assignment between the family-drift feature vector `D(p) = (D_cap,…,D_saf)(p)` and the breakage target `B̄(p)` **across pairs** (destroying the pair-level correspondence while preserving both marginals), then re-fit the *identical* predictor and grouped-CV pipeline used for H1/H2. Its predictive power must be null: `π_f(P0)` CI must include 0 and `AUC(P0)` 95% CI must include 0.5, over ≥1000 shuffles. **A non-null shuffled predictor = the pipeline measures an artifact** (grouping leak in the CV fold assignment, or a per-pair nuisance shared by `D` and `B̄` such as prompt length or decode temperature) **= the whole run is invalid** — record `{"run_valid": false, reason}`, diagnose, and re-run from the walking skeleton (never score any H\* "to see"). This is the genuine placebo guidance.md §3.3(b) mandates; its effect is null *by construction* when the correspondence is broken.
- **B0 — no-signal performance floor ("why do this at all", job (a) of §3.3):** a **constant base-rate breakage predictor** using *no probe features* (predicts `E[B̄]`). This is a floor the real predictors must *beat*, not a placebo: if the full battery (and every subset) fails to beat B0's AUC/Brier at α=0.05, no probe carries usable signal and the premise (a cheap probe can forecast breakage) collapses → route to F-G1. Also reported: random/uniform drift-score baseline (digest N8 baselines).
- **B-alt — strongest-alternative-explanation control (budget/capability-matched):** a **family-agnostic total-drift scalar** — raw output-diff magnitude on the *entire* probe bank ignoring family structure (digest N8 baseline), using the *same query budget* as the five-family battery. **Rival explanation it kills:** "probe drift predicts breakage only because both track *how big the update was* (one scalar), so the *which-axis* question is vacuous." H1/H2 count as isolating axis-selectivity **only if** the family-structured predictor beats this total-drift scalar's AUC (paired bootstrap, 95% CI lower bound > 0). If it does not, the axis-selectivity claim is not isolated → route to F-G1.

### Global fallback F-G1 (archetype pivot)
If the central hypothesis family fails — no family/subset beats **B0**, or the family-structured predictor never beats **B-alt** across the corpus — pivot from *empirical ranking + minimal design* to a **negative-result characterization study**: 
> *"We show that observable black-box behavioral-probe drift does not forecast downstream breakage across retrospective LLM version pairs, and characterize why — breakage is governed by integration-internal brittleness (parser/policy specifics) not recoverable from any of five measured behavioral axes — reframing version-drift auditing away from cheap external probes toward integration-level contract tests."*

**F-G1 requires a substantive null, not an artifact or an underpowered miss.** It fires only when **P0 is null** (clean pipeline) AND the corpus is adequately powered (`|P| ≥ 60`, A6). If **P0 is non-null** → run invalid, not F-G1 (situation 1). If the corpus is under-powered → INCONCLUSIVE, collect more pairs, not F-G1 (situation 5). Instrument failure (A3 κ<0.7) → fix the instrument, not F-G1 (situation 7).

### Fallback-combination rules (pre-committed, guidance.md §3.1 — never invented at verdict time)
- **H3 gates H1/H2.** If H3 fails for a family (drift ⊆ noise or rank-unstable), that family is dropped from H1's ranking and H2's subset search *before* they are scored (A2 consequence). If **fewer than 3 families survive H3**, H1 is reported as *"instrument-limited: only families {…} carry rank-stable drift above noise"* and H2's minimal-subset claim is **suspended** (a subset over <3 families is not a meaningful compression result) — report H3's outcome as the finding.
- **H1 FAIL + H2 PASS:** no single axis dominates but a ≤2-family *subset* still beats B0/B-alt → keep the minimal-subset claim (Claim 2), drop the single-axis ranking claim (Claim 1) via its RQ1 fallback wording. The paper's headline shifts from "which axis" to "which small bundle."
- **H1 PASS + H2 FAIL (`|S*|=5`):** the ranking holds but no compression exists → keep Claim 1, apply H2's fallback (full battery is minimal). Practical recommendation becomes "run the full battery; it does not compress."
- **H1 FAIL + H2 FAIL + B0 not beaten:** the whole family fails → **F-G1** (global pivot).
- **H6 undefined (VIF ≫ 10):** if partials are untrustworthy, H6 is not scored PASS/FAIL; H1's per-family attribution is downgraded to bundle-level (A4 consequence), and the mechanism-analysis claim (Claim 9) is reported as *"families are inseparably collinear in this corpus; attribution is reported at the bundle level."*
- **H4 FAIL + H1 PASS:** breakage is not resolvably task-heterogeneous but an axis still governs → Claim 1 holds, Claim 7 narrows (RQ4 fallback). No conflict.

### Forward-validation robustness check (design-review addition — the protocol's actual use is prospective)
The audit protocol is sold as *"run the minimal subset once per version bump"* — a **prospective** use, but H1/H2 are estimated in-sample with random-pair grouped CV. Pre-registered robustness: a **temporal split** — fit family ranking and `S*` on the chronologically *earlier* pairs, evaluate `AUC(S*)` and the ranking's Kendall τ on the *latest* held-out pairs. Report forward `ΔAUC(S*)` and forward rank-stability alongside the in-sample numbers. **This is a reported robustness axis, not a gate** (with few pairs the temporal fold is thin); a large in-sample-vs-forward gap is disclosed as a limitation on the "run it prospectively" claim, never hidden.

---

## Step 9 — Walking Skeleton

**One binary question:** *On the pilot, does refusal-family drift correlate with downstream breakage more strongly than capability-family drift?* (sign & ordering of `π_ref − π_cap`).

- **Arms (4):** (a) `ref` drift predictor, (b) `cap` drift predictor, (c) `fmt` drift predictor, (d) **B0** base-rate floor — plus the **P0 label-shuffle placebo** run through the identical predictor/CV path. **`fmt` is included so ≥3 families are in the design at pilot: the VIF / partial-correlation / joint-regression code path (M7, H6) is exercised by the skeleton, not first met at scale.**
- **Smallest task set:** 3 open-weight pairs with immutable checkpoints (Llama-2→Llama-3, Qwen1.5→Qwen2, Mistral v0.1→v0.2) × 5 downstream tasks (extraction-to-JSON, classification, RAG-answer, tool-call arg filling, moderation) = 15 cells. Probe items: ~100 each for `I_ref`, `I_cap`, `I_fmt`.
- **Riskiest components exercised in the skeleton (design-review fix, 2026-07-04 — goal.md §4 requires the skeleton to exercise every riskiest component and run R2/PG-* gates inside B):**
  - **PG-P0 (placebo path):** run P0 on the 15 cells; the shuffled predictor's `π`/AUC CI must include the null. A non-null shuffle at pilot = a pipeline leak caught *before* any scale-up spend.
  - **PG-noise (A2 noise-floor path):** re-decode `I_ref`/`I_cap`/`I_fmt` on the *same* version ≥3× to compute the within-version null and confirm the noise-floor gate fires for ≥1 family. The skeleton no longer runs fixed-decoding-only; the re-decode loop is exercised here, so A2 is not first met at scale.
  - **PG-2 (A3 semantic-diff κ, mini):** the semantic-diff half of `B(p,t)` — the one subjective, non-deterministic component of the ground truth — gets a *minimal* human-κ check: ≥2 raters label the ~15 near-threshold cells, requiring provisional κ ≥ 0.7 against the automated call before the pilot ordering is trusted. (The full Phase-C κ validation scales this; but the riskiest instrument is no longer entirely deferred past the skeleton.)
- **Deterministic + one re-decode loop:** schema-validity rate, tool-call executability, refusal-rate delta, capability accuracy delta, format schema-match delta, semantic-diff over fixed seed, plus the within-version re-decoded null (above).
- **Expected cost/wall-clock:** open-weight only, 2–4 A100-class GPUs, ~3–4 days (the re-decode loop + mini-κ add ~1 day); **near-zero API cost**; ~4–8 annotator-hours for PG-2.
- **Skeleton-passed criterion:** the pipeline (i) administers `I_ref`/`I_cap`/`I_fmt` to both versions, (ii) computes `D_ref`, `D_cap`, `D_fmt`, `B(p,t)` for all 15 cells with the within-version null, (iii) **PG-P0 shuffle placebo comes out null**, (iv) **PG-noise gate fires for ≥1 family**, (v) **PG-2 mini-κ ≥ 0.7**, (vi) the M7 joint fit + VIF + partial-correlation runs on the 3 families and emits `π_ref − π_cap` with a sign and per-family VIF. **Passed ⇒ scaling to `|P| ≥ 60` pairs × 20 tasks + the 2 remaining families (`cal`, `saf`) + the paraphrase loop is adding rows to the corpus/probe-bank config — not new code. If any of (iii)–(vi) requires new code to scale, the skeleton failed (situation 8): fix and re-run B.**

---

## Claim–Evidence Map

| # | Abstract claim | traces to | status |
|---|---|---|---|
| 1 | Refusal/safety drift out-predicts capability drift for breakage (digest Claim 1) | **H1** (RQ1) | needs-experiment; fallback-covered (RQ1 fallback) |
| 2 | A ≤2-family subset recovers most predictive power — a genuinely minimal probe set (Claim 2) | **H2** (RQ_INF_1) | needs-experiment; fallback-covered (RQ_INF_1 fallback) |
| 3 | Measured drift exceeds the noise floor & is paraphrase-stable (else correlations are artifacts) (Claim 3) | **H3** (RQ_INF_2) | needs-experiment; gating precondition for 1–2 |
| 4 | Breakage is defined functionally, not by surface diff (Claim 4) | **Step-5 `B(p,t)` def** + A3 | supported-by-design |
| 5 | Axis-selectivity is not just total-update-magnitude | **B-alt** control | needs-experiment; F-G1-covered |
| 6 | Any probe beats a no-probe performance floor at all | **B0** floor | needs-experiment; F-G1-covered |
| 6b | The pipeline measures a real signal, not an artifact (shuffled drift→breakage correspondence predicts nothing) | **P0** null-by-construction placebo | needs-experiment; non-null ⇒ run invalid (situation 1), checked before all H\* |
| 7 | Downstream breakage is genuinely task-heterogeneous, not axis-agnostic (pipeline.md Stage 6 `rq_downstream_heterogeneity`) | **H4** (RQ4) | needs-experiment; fallback-covered (RQ4 fallback) |
| 8 | The retained retrospective corpus is not systematically attrition-biased, licensing treating it as representative (pipeline.md Stage 6 `rq_corpus_attrition_bias`) | **H5** (RQ5) | needs-experiment; fallback-covered (per-family narrowing, not global invalidation) |
| 9 | Raw per-family correlation can misattribute predictive power without partial/collinearity-aware attribution — the R6 mechanism analysis (pipeline.md Stage 6 `rq_family_collinearity_partial`) | **H6** (RQ6) | needs-experiment; fallback-covered (RQ6 fallback) |

Every claim traces to an H-id or a Step-5 definition; no orphan claims. **Note (Phase A fix, 2026-07-04):** rows 7–9 formalize three mechanism-tier hypotheses that `pipeline.md`'s Stage 4–6 auto-research-discussion run already derived (and that `paper_draft.tex`'s six RQ subsections already assume) but that this file had left only as implicit gestures inside A1/A4/A5 — see guidance.md §3.1/§3.4 R6 and goal.md §3 checklist items 4–5. No new experiments were run; this is pre-registration catch-up, not a results claim.

---

## Abstract v0 (draft, mechanism-first — BEFORE results)

*[draft, pre-results — no numbers are observed]*

Across an LLM version update, breakage of a downstream integration is an **axis-selective** function of behavioral drift: a parser fails on format drift, a policy filter on refusal drift, and the axis that moved most need not be the axis that breaks anything. We **formalize** per-family drift magnitude over five behavioral axes — capability, refusal-boundary, format, calibration, safety — and downstream breakage as the functional-equivalence-checked cross-version output diff on a shared input set. On a retrospective corpus of already-occurred open-weight and dated-API version pairs, we **measure** which family's drift forecasts breakage and **isolate** the smallest family subset that retains that forecasting power. We **gate** every correlation against a within-version sampling-noise floor and paraphrase-set rank-stability, and separate axis-selectivity from a budget-matched family-agnostic total-drift predictor, yielding a minimal, validated version-drift audit protocol.

*(~150 words. Mechanism-first; verbs formalize/measure/isolate/gate/separate; no "increasingly used… however… we introduce.")*
