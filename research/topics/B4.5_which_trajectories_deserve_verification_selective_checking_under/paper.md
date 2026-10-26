# Which Trajectories Deserve Verification? Selective Checking under a Verifier-Call Budget — Pre-Registered Paper Specification

> Generated from digest.md + README.md. Status: specification, no experiments run.
> All ids (C1–C4, M1–M5, CO1–CO4, RQ1/RQ_INF_1/RQ_INF_2, Claims 1–5, t1–t5) refer to digest.md.

## Step 0 — Core Asymmetry (升维)

**The asymmetry:** Because every candidate trajectory *and* every verifier-free uncertainty signal over it are drawn from the same model distribution, the trajectories whose verification would change the final answer most — unanimous-but-wrong sample pools — are exactly the trajectories that any agreement-based ranking scores as *least* worth verifying; a trusted verifier call has uniform price but its marginal information is anti-correlated with the only free estimate of that information.

**判据 (deletion test).** Delete the domain nouns: *"Because every candidate and its quality signal come from the same source, the items whose checking would change the outcome most are exactly the ones every ranking scores as least worth checking."* This generic statement is **false**: in ordinary selective inspection (manufacturing QA, active learning with an independent feature model, medical triage), the checking signal is *not* produced by the error source, so high-value targets are not systematically ranked last — uncertainty sampling generically works. The sentence is only true when the signal generator and the error generator are the same sampled LLM (mode share is computed from the very samples whose collective failure it must detect). The claim collapses without the domain nouns, so it is an asymmetry, not a bridge. (Grounded in digest C1 and Claim 4.)

## Step 2 — Archetype

**Primary:** `empirical` — a measurement/characterization study (digest N12): the deliverables are budget–accuracy curves, signal-AUROC tables, and matched-budget policy comparisons; the built components (M1–M5) are instruments, not the contribution object. **Secondary:** conceptual formalization (CO1: budget-constrained trajectory selection with a *trusted* verifier as the complementary corner to verifier-imperfection theory `[ROC-n-reroll, OpenReview:3Gy5mmyuxn]` and to topic B1.5).

Downstream consequences:
- **(a) Abstract contribution slot:** a measured quantity — "what fraction of the full-verification gain is recovered at what fraction of calls, and which verifier-free signal buys it" — not a new method claiming SOTA.
- **(b) Intro logic:** "what becomes possible": pipeline designers can *price* verification before deploying it — decide how many verifier calls a sampling pipeline needs, and where to aim them, from signals that cost nothing extra. Not "we beat baseline X by Y points".
- **(c) Evidence standard for Results:** pre-registered directional hypotheses with hard thresholds, paired matched-budget comparisons on identical frozen trajectory pools, corrected significance tests, and per-signal (never generic "uncertainty") claims. A negative result under this standard is a publishable characterization (see F-G1), which a SOTA-method archetype would not survive.

## Step 3 — Taste self-audit

- **Is the opportunity a Bridge?** Risk exists: "budget allocation exists for generation, we bring it to verification" is a bridge. **Fixed framing:** the opportunity is the Step-0 asymmetry — uniform call price vs. anti-correlated marginal value under a self-generated signal. The paper measures how much that asymmetry actually costs and how much of it cheap signals can still exploit. PASS after fix.
- **Is the method mere Synthesis?** No: M1–M5 are deliberately minimal instruments (digest N12 rationale); the method *is* the measurement design (oracle-verifier isolation in Stage 1, verifier-realism sweep in Stage 2). The oracle-first staging is a designed identification strategy, not a component mashup. PASS.
- **Load-bearing verbs check:** the framing verbs are **meter** (verifier calls as the explicit scarce resource), **isolate** (oracle verifier separates allocation quality from verifier quality), **measure** (signal AUROC, budget-recovery fraction), **rank/eliminate** (policy and aggregator mechanics). No integrate/unify/leverage/combine in load-bearing positions. PASS.
- **Abstract-opening rule:** Abstract v0 (below) opens with the metered-resource asymmetry, not with "LLMs are increasingly used… however… we introduce". PASS.

## Step 5 — Formal Problem Definition

**Estimand (R1, guidance.md §3.4):** the accuracy-per-verifier-call APC(B) (and its integral, the budget-recovery curve R(b)) delivered by an allocation-plus-aggregation policy π,g at a fixed trusted-verifier-call budget B, relative to uniform-random allocation and full verification at matched B; unit of analysis is one task instance's final answer under a budget shared across the whole evaluation batch; reference population is sampled-trajectory pools (self-consistency/best-of-N/rollouts) from open 7–8B-class models on benchmarks with checkable final answers (math, code); the decision it feeds is how a deployment should size and aim a metered verifier-call budget before spending it.

**Notation.** Task instances x_1..x_m; per instance a pool T_i = {τ_i1..τ_iN} of N trajectories sampled i.i.d. from model p_θ; final answer a(τ). Trusted verifier V: τ ↦ {0,1} (correct/incorrect for its instance). Global budget B < mN. Allocation policy π selects S ⊆ ∪T_i, |S| ≤ B; aggregator g maps (T_i, V restricted to S∩T_i, signals) ↦ â_i. Acc(π,B) = (1/m)Σ 1[â_i correct]. Signals u(τ) ∈ ℝ³ = (mode share, normalized sequence log-likelihood, verbalized confidence/100), computed before any V call (M1).

**Load-bearing adjectives/verbs → computable definitions → measurement:**

| Term (from Claims) | Definition | Measured by |
|---|---|---|
| **trusted** (verifier) | oracle: V = ground-truth lookup, error 0 by construction; realistic: measured FPR and FNR ≤ 0.05 against held-out gold labels | Stage-2 verifier audit on 200 labeled trajectories per domain (A1 gate) |
| **selective / uncertainty-guided** | π ranks trajectories (or instances) by u and submits the top B; fully specified by (signal, granularity) ∈ {3 signals} × {trajectory-level, instance-level} (M2) | code, deterministic given frozen pools |
| **matched budget** | two policies compared at identical B, identical frozen pools, identical aggregator g | pipeline construction; cache hashes |
| **accuracy-per-verifier-call** | APC(B) = (Acc(B) − Acc(0)) / B | digest N8 metric |
| **budget-recovery fraction** | R(b) = (Acc(bmN) − Acc(0)) / (Acc(mN) − Acc(0)) | digest N8 metric |
| **recovers the majority** (Claim 1) | R(0.25) > 0.5 | H2 |
| **small fraction** (Claim 1) | b ≤ 0.25 | fixed budget grid b ∈ {.05,.10,.25,.50} |
| **informative** (signal) | AUROC(u_k, V-labels) with DeLong 95% CI lower bound > 0.55 | H1; digest N9 Result-1 falsification threshold |
| **confident-but-wrong** (Claim 4) | instance whose plurality answer has mode share ≥ 0.75 and is incorrect | counted per dataset; CBW mass = their fraction |
| **structurally imperfect proxy** (Claim 4) | AUROC < 1 and P(rank in top-B | confident-but-wrong) < B/(mN), i.e. the ranking under-selects CBW targets relative to chance | direct count on verified pools |
| **verification headroom** | H = Acc(full verification) − Acc(no verification) | B0 gate: problem is non-vacuous iff H ≥ 0.05 |
| **transfers** (Claim 5) | policy (signal choice + granularity + any threshold) frozen on domain D₁, evaluated on D₂, still beats uniform at b=0.25 (corrected p < 0.05) | H3 |
| **hindsight-optimal** | allocation chosen with knowledge of all V-labels to maximize Acc at budget B (computable post hoc since oracle pools are fully labeled) | M5 gap denominator |

Deleted adjectives: "wisely", "efficiently", "smart" — none appear in claims; any that creep into prose must reduce to APC or R(b).

## Assumptions (A1–A6)

Each assumption below now names an explicit **Gate** (guidance.md §3.2: "gate: PG-j if checked in the pilot; else the phase that checks it") in addition to its failure mode and detection, so pass/fail is recorded in `B_pilot/` rather than left as a paragraph:

- **A1 Verifier trust.** Oracle stage: exact by construction. Realistic stage: execution/PRM verifier FPR, FNR ≤ 0.05 on held-out gold labels. *Failure mode:* PRM threshold noisy → "trusted" premise void, topic collapses into B1.5. *Detection:* 200-trajectory verifier audit before Stage 2, with a confusion-structure inspection (are FPR/FNR errors concentrated in specific difficulty bins or problem types, or diffuse? per guidance.md R2 step ④) rather than a bare pass/fail rate. *Gate:* Stage 2 pre-flight (not checked in the Step-9 pilot, which uses the oracle verifier only); frozen before any Stage-2 budgeted run. *Consequence if failed:* Stage 2 claims (H3a) scope down to "oracle-verified allocation only," Stage-2 realism/transfer RQs (H3a/H3b) become out of scope for the affected domain, and the verifier-noise sensitivity sweep (linking to ROC-n-reroll) is reported descriptively in its place.
- **A2 Signal informativeness.** At least one M1 signal has AUROC CI-lower-bound > 0.55 against V-labels. *Failure:* proxy gap total (C1); no policy can beat uniform. *Detection:* walking-skeleton gate (Step 9). *Gate:* PG-(iii) — Step 9 pass-criterion (iii), mode-share AUROC ≥ 0.60. *Consequence if failed:* H1 fails at its first conjunct; F1/F-G1 fire.
- **A3 Model–dataset non-degeneracy.** Base accuracy in [0.30, 0.70] and mode-share IQR > 0.2 (digest N6 feasibility mitigation). *Failure:* unanimous pools everywhere → mode share constant, allocation vacuous. *Detection:* 50-instance dry-run pre-screen per model×dataset pair; failed pairs replaced (MATH-500 levels 3–5, MBPP+ as difficulty knobs), replacements logged before any budgeted run. *Gate:* PG-0 — the dry-run pre-screen, which runs before (and gates entry to) the Step-9 walking skeleton. *Consequence if failed:* the offending model×dataset pair is swapped for its named replacement before any code runs; two failed swaps in a row routes to F-G1.
- **A4 Pipeline separation.** All M1 signals computed and frozen (hashed cache) before any verifier call (digest t2). *Failure:* leakage trivializes results. *Detection:* automated audit — signal-cache write timestamps/hashes precede first V-call log entry. *Gate:* PG-(cache-order) — an automated CI check embedded in and run alongside every Step-9 skeleton pass criterion, and re-checked at every scale-up. *Consequence if failed:* the run is invalid per goal.md's non-null-placebo discipline (situation 1) — diagnose the ordering leak, fix, and re-run the skeleton before any hypothesis is scored.
- **A5 Answer checkability.** Final answers exact-matchable (math) or executable against held-out tests (code); answer parse rate ≥ 0.95 per dataset. *Failure:* unparsed answers corrupt both mode share and V-labels. *Detection:* parse-rate report in dry run; datasets below 0.95 excluded (pre-registered exclusion rule). *Gate:* PG-(i) — Step 9 pass-criterion (i), parse rate ≥ 0.95. *Consequence if failed:* the dataset is excluded (pre-registered exclusion), reported against generality claims per R8, never silently dropped.
- **A6 Cost realism.** A verifier call's marginal cost dominates signal computation: measured cost(V-call) ≥ 10 × cost(all three signals per trajectory) in tokens or wall-clock for the realistic verifiers. *Failure:* if signals cost as much as verification, "verifier-free" framing is hollow. *Detection:* per-call cost logging (M3 instrumented output); reported as accuracy-per-dollar alongside accuracy-per-call. *Gate:* Stage 2 pre-flight, alongside A1 (not applicable to the oracle-only Step-9 pilot, since oracle verification is free by construction). *Consequence if failed:* the "verifier-free signal" framing is qualified in Limitations as cost-neutral rather than cost-saving for that verifier class; APC/R(b) headline claims are re-reported as accuracy-per-dollar instead of accuracy-per-call for the affected configs.

**Power and thin-cell rule (guidance.md Part 6 item 9; Part 3.4 R8; Part 4 situation 5):** McNemar-test power at the pre-registered effect floors (2.0 accuracy points at b=0.10 for H1; 1.0 point at b=0.25 for H2b) is computed per config *before* any hypothesis test, using each config's own n (500 for GSM8K/MATH-500/MBPP+-subsample; 164 for HumanEval+, its full size — the one cell smaller than the 500-instance design target). Any RQ×config cell whose pre-registered effect floor is not attainable at power ≥ 0.80 given that cell's n is pre-declared **INCONCLUSIVE** for that cell — not scored PASS or FAIL, not counted toward the "≥k of n configs" aggregation vote in H1–H3, and never silently dropped from the reported grid (R8). If HumanEval+ is under-powered for a given RQ's effect floor, that RQ's aggregation vote is evaluated over the remaining 3 configs with the INCONCLUSIVE cell reported alongside, not folded into a smaller implicit denominator without comment.

## Step 6 — Pre-Registered Experiments

Shared design constants (frozen before Stage 1): pilot = 2 models (Qwen2.5-7B-Instruct, Llama-3.1-8B-Instruct) × 2 datasets (GSM8K-500 fixed subsample, MATH-500), N = 16, budget grid b ∈ {.05,.10,.25,.50}, 5 seeds on primary configuration, oracle verifier. Stage 2 adds HumanEval+, MBPP+, N = 64, execution/PRM verifiers, M5. Statistics: per-budget paired McNemar + 10,000-resample paired bootstrap CI on identical pools; Holm–Bonferroni within each declared family; AUROC via DeLong (digest N8 analysis plan). "Config" below = one model×dataset pair; pilot has 4.

### E1 (RQ1 — which trajectories deserve the calls; C1; CO1, CO2)
- **Assumption:** A2, A3, A4, A5.
- **Hypothesis H1 (binary):** (i) mode share attains AUROC ≥ 0.65 with DeLong 95% CI lower bound > 0.55 on ≥ 3 of 4 pilot configs; AND (ii) the best single-signal M2 policy beats uniform-random allocation at b = 0.10 by ≥ 2.0 accuracy points with Holm-corrected McNemar p < 0.05 on ≥ 3 of 4 configs. Both (i) and (ii) must hold.
- **Metric:** signal AUROC per u_k; Δacc(b) = Acc_selective(b) − Acc_uniform(b); APC(b).
- **Verification:** family = {4 configs × 3 signals} for AUROC (DeLong CIs, Holm); family = {4 configs} for Δacc(0.10) (McNemar + bootstrap CI, Holm, α = 0.05). Sample size 500 instances/config (power adequate for a 2-point paired difference at base accuracy 30–70%).
- **Fallback F1 (pre-committed wording):** "Verifier-free uncertainty signals, though nonzero predictors of trajectory correctness, cannot be converted into a verifier-call allocation that beats blind spending at small budgets; we quantify the confident-but-wrong mass (Step-5 definition) that caps every signal-ranked policy, giving the first measured ceiling on selective verification in trajectory pools." (Claims 1 drops; Claim 4 becomes the headline.)

### E2 (RQ_INF_1 — budget–accuracy curve + aggregation; C1, C4; CO2, CO3, CO4)
- **Assumption:** A2–A5, plus B0 headroom gate (H ≥ 0.05 per config).
- **Hypothesis H2 (binary):** (i) budget-recovery fraction R(0.25) ≥ 0.50 with 95% bootstrap CI lower bound > 0.25 (strictly better than spend-proportional recovery) on ≥ 3 of 4 configs; AND (ii) selective > uniform (corrected p < 0.05) at every b ∈ {.05,.10,.25,.50} on ≥ 2 of 4 configs. — **H2b (aggregation, separable):** elimination-aware M4 beats the naive rule by ≥ 1.0 accuracy point at b = 0.25 on ≥ 3 of 4 configs (paired bootstrap CI excluding 0).
- **Metric:** R(b); AUBC over b ∈ [0,1]; Δacc(b); M4-vs-naive Δacc at matched budget.
- **Verification:** curves from 5 seeds with seed-level dispersion; per-budget McNemar + bootstrap, Holm over the 4-budget × 4-config family; H2b tested in its own 4-config family.
- **Fallback F2 (pre-committed wording):** "Selective allocation's recovery is only proportional to spend — the budget–accuracy curve is statistically indistinguishable from the diagonal — showing that in these regimes verifier-call *placement* is irrelevant and only verifier-call *volume* matters; practitioners can size verification budgets by volume alone." If only H2b fails: "aggregation is not a separate design axis at these budgets; verified-incorrect eliminations carry negligible marginal information over the raw vote" (CO4 withdrawn, selection claims unaffected).

### E3 (RQ_INF_2 — realism, transfer, sequential policy; C2, C3; CO1, CO3)
- **Assumption:** A1 (realistic-verifier audit), A2, A3, A6.
- **Hypothesis H3 (binary, three separable sub-claims):**
  - **H3a (verifier realism):** under execution (code) and PRM (math) verifiers, Δacc(0.25) retains ≥ 50% of its oracle-verifier magnitude and remains significant (corrected p < 0.05) on ≥ 2 of 4 Stage-2 configs; on code with execution verification (near-ground-truth), Δacc(0.25) > 0 with p < 0.05.
  - **H3b (transfer):** the policy frozen on math beats uniform on code at b = 0.25 (corrected p < 0.05), and vice versa, in ≥ 3 of 4 transfer directions×model cells.
  - **H3c (sequential):** M5 closes ≥ 20% of the static-M2-to-hindsight-optimal accuracy gap at b ≤ 0.10, with bootstrap CI excluding 0, on ≥ 2 of 4 configs.
- **Metric:** Δacc(b) under each verifier; transferred-policy Δacc; gap closure = (Acc_M5 − Acc_M2)/(Acc_hindsight − Acc_M2); accuracy-per-dollar (A6 logging).
- **Verification:** same paired machinery; three separate Holm families (realism / transfer / sequential), declared here; verifier-noise sensitivity sweep linking to `[ROC-n-reroll, OpenReview:3Gy5mmyuxn]` reported descriptively (no hypothesis).
- **Fallback F3 (pre-committed wording):** per failed sub-claim — H3a: "selective gains are an oracle artifact: realistic verifier noise erases placement advantage, locating this topic's practical value strictly at the verifier-quality frontier"; H3b: "signal informativeness is domain-bound; a verification budget policy must be re-fit per domain (C2 answered negatively, with the AUROC-shift decomposition as the explanation)"; H3c: "static ranking is within X% of hindsight-optimal already — the online character of C3 is immaterial at these pool sizes" (X reported as measured).

### Mandatory baselines

- **B0 — "why do this at all" control:** *uniform-random verifier-call allocation at matched budget* (the seed's stated control — the no-mechanism arm every H is tested against), gated by the *verification-headroom check*: full-verification vs. no-verification (self-consistency majority vote, `[Wang et al., 2023]`) must differ by H ≥ 0.05 accuracy on each config, else the problem is vacuous there and the config is reported as out-of-scope (pre-registered exclusion, counted against generality claims). B0 justifies the problem's existence: if blind spending matches aimed spending, or if verification buys nothing over voting, no allocation question exists.
- **B-alt — strongest-alternative-explanation control:** **rival explanation:** *"selective gains are just instance-difficulty triage — any per-instance hardness estimate would do; per-trajectory uncertainty adds nothing."* Control arm: difficulty-conditioned instance-level allocation adapted from `[Compute-Optimal-TTS, OpenReview:4FWAwZtd2n]` (allocate calls to instances ranked by base-model difficulty estimate, then verify random trajectories within), call-budget-matched and aggregator-matched. Secondary B-alt: calibrated confidence-threshold escalation adapted from `[Trust-or-Escalate, OpenReview:UHPnqSTBPO]` (per-item threshold, ignoring global budget coupling) — isolates the value of *global* budget-coupled ranking over per-item thresholding. Pre-registered comparison: M2 instance-level policy vs. B-alt at b ∈ {.10,.25}, same families/corrections; if M2 does not beat difficulty-triage, the claim demotes from "trajectory-uncertainty-guided" to "difficulty-guided" allocation (wording committed here).

### Global fallback F-G1

If the central hypothesis family {H1, H2} fails jointly (signals uninformative or placement irrelevant), the paper pivots archetype from *measurement of a working policy* to *negative-result characterization with a mechanism*: the Step-0 asymmetry becomes the finding rather than the obstacle. Pivoted abstract sentence (committed): **"We show that the verifier-free signals available to aim a metered verifier budget are systematically blind to the highest-value targets — confident-but-wrong consensus pools — and that this blindness, which we quantify as the confident-but-wrong mass across four benchmarks and two model families, caps selective verification at the value of blind spending, a measured ceiling that any future allocation policy must break by importing information from outside the sampling distribution."

## Step 9 — Walking Skeleton

**One binary question:** *on one frozen pool, does mode-share-ranked allocation beat uniform allocation at b = 0.25 under an oracle verifier?*

- **Arms (3):** (1) uniform-random @ b=0.25; (2) mode-share most-uncertain-first (instance-level) @ b=0.25; (3) full verification (anchor; also yields all V-labels for AUROC and the hindsight-optimal reference).
- **Task set:** GSM8K, fixed 100-instance subsample, Qwen2.5-7B-Instruct, N = 16, one seed, greedy M4 aggregation.
- **Deterministic metrics only:** accuracy@B per arm; mode-share AUROC (point estimate); headroom H; parse rate; A4 cache-order audit pass/fail. No significance testing at this scale.
- **Cost:** ~1,600 generations + 1,600 confidence elicitations ≈ 1–3 GPU-hours on one A100 with vLLM (or < $20 API); oracle verification free.
- **Pass criterion (all four):** (i) parse rate ≥ 0.95; (ii) headroom H ≥ 0.05; (iii) mode-share AUROC ≥ 0.60; (iv) arm-2 − arm-1 ≥ +1.0 accuracy point. **Skeleton passed ⇒ scaling is a config change, not a code change:** the full grid differs only in dataset list, model list, N, budget grid, seed count, and verifier class — every interface (pool cache → signal table → allocation → V-log → aggregator) is exercised end-to-end by the skeleton. Fail on (iii)/(iv) → invoke A2/A3 pre-screen swaps (MATH-500 L3–5) before touching any code; fail twice across swapped pairs → F-G1 path.

## Claim–Evidence Map

| Claim (digest ids) | Traces to | Status |
|---|---|---|
| Claim 1 — selective verification recovers majority of gain at small fraction of calls | H2(i)(ii); Step-5 defs of R(b), "majority", "small fraction" | needs-experiment; fallback-covered (F2) |
| Claim 2 — mirror image of B1.5: trusted verifier, scarce calls | Step-5 "trusted" def; A1; positioning vs `[ROC-n-reroll]`, `[OT-Verify]` (digest N4-L2) | supported-by-design |
| Claim 3 — no prior work meters calls to a trusted verifier over a trajectory pool | digest N3/N4 grounded corpus audit (L1–L5); no experiment needed | supported-by-design (re-run corpus search before submission, per digest N3 absence note) |
| Claim 4 — signal is structurally imperfect exactly where value is highest | Step-0 asymmetry; Step-5 CBW definition; measured in E1 (AUROC + CBW under-selection count) | needs-experiment; survives H1 failure (becomes headline under F1/F-G1) |
| Claim 5 — recovery is domain-dependent, shrinks but persists under realism/transfer | H3a, H3b | needs-experiment; fallback-covered (F3) |
| (implicit) aggregation is a distinct design axis (CO4) | H2b; Step-5 matched-budget def | needs-experiment; fallback-covered (F2-aggregation) |
| (implicit) sequential reallocation matters (C3, CO3) | H3c | needs-experiment; fallback-covered (F3-H3c) |

## Abstract v0 (draft, mechanism-first — DRAFT BEFORE RESULTS; every number below is a pre-registered target, not a finding)

A call to a trusted verifier has uniform price, but its marginal information over a pool of sampled LLM trajectories is wildly non-uniform — and the only free estimates of that information are computed from the same model whose failures they must detect, leaving the highest-value targets (unanimous-but-wrong pools) systematically under-ranked. We formalize verification under a metered call budget: given N candidate trajectories per instance and B < N×m total calls to a trusted verifier, which trajectories should be checked? We isolate allocation from verifier quality with an oracle verifier, then measure three verifier-free signals (mode share, sequence likelihood, verbalized confidence) as budget-aiming devices on math and code benchmarks, against uniform allocation, difficulty triage, and full verification at matched budgets. Pre-registered criteria: signal AUROC > 0.55 and recovery of ≥ 50% of the full-verification gain at 25% of calls.

<!-- 148 words. Opens with the asymmetry/mechanism; verbs: formalize, isolate, measure, meter; forbidden template avoided. -->
