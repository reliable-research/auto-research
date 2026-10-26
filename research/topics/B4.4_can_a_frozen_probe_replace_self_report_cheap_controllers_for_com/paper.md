# Can a Frozen Probe Replace Self-Report? Cheap Controllers for Compute Allocation — Pre-Registered Paper Specification

> Generated from digest.md + README.md. Status: specification, no experiments run.
> All ids (C.., M.., CO.., RQ.., t..) refer to digest.md nodes N1–N12.

---

## Step 0 — Core Asymmetry (升维)

**Asymmetry sentence:**
> A compute-allocation controller is paid for out of the very budget it allocates, so a controller that reads its routing signal from a frozen prefill hidden state the query has *already* produced enjoys a structural budget advantage over one that must burn fresh generation — an extra self-report call, or k extra self-consistency samples — to manufacture the same decision.

**判据 (deletion test).** Remove the domain nouns:
> A ___ is paid for out of the very ___ it allocates, so a ___ that reads its ___ from a ___ the ___ has *already* produced enjoys a structural ___ advantage over one that must burn fresh ___ to manufacture the same ___.

This collapses to "a thing is paid out of the budget it allocates, so a thing that reuses what already exists beats one that must spend fresh" — which is empty/tautological without "prefill hidden state", "self-report call", "self-consistency samples", "routing signal". The claim only carries content because the signal-acquisition cost of *these specific controllers* is charged against the *same* dollar meter they route. It is NOT a bridge ("A and B were never connected") — it names an invariant (signal cost is subtracted from allocation budget) that produces a testable ordering among controllers.

---

## Step 2 — Archetype

**Primary archetype:** *Empirical measurement / controlled comparison* (digest N12 `value = empirical`). No new controller mechanism is proposed; the object is a matched-budget three-way comparison (CO1).
**Secondary:** *Instrument* — the precompute-then-simulate accuracy-per-dollar harness (CO3, N11) is the reusable artifact enabling zero-model-cost re-evaluation of new controllers.

Downstream consequences:
- **(a) Abstract contribution slot:** the *measurement result* — whether a near-zero-cost frozen probe matches/exceeds self-report and training-free signals at matched realized budget, with each controller charged its own signal cost.
- **(b) Intro logic:** "what becomes possible" — if a probe reading already-computed features matches self-report, the controller stops being a budget line item (N2). NOT "beat a number".
- **(c) Evidence standard:** paired per-query correctness under identical cached two-tier outputs, budget points pre-registered, controllers compared at *equal realized spend* including their own signal cost; ground truth is controller-independent (programmatic exact-match).

---

## Step 3 — Taste self-audit

- **Is the opportunity a Bridge?** Risk: "connect probing to compute allocation." Rejected — the antecedents ([DiffAdapt 644FH1vVIl], [AdaptiveThinking 2i6Rp0gCq6]) already probe hidden states for allocation. The content is the *asymmetry in signal cost under a shared budget* (Step 0), not a connection. PASS after sharpening.
- **Is the method mere Synthesis?** Risk: "combine entropy + probe + self-report into an ensemble." Rejected — the design does not fuse them; it *isolates and prices* each as a competing controller under one meter (M4/M5). PASS.
- **Load-bearing verbs from integrate/unify/leverage family?** Original draft abstract (N0) opened "This paper asks whether… can serve as…". Corrected below to gate/price/measure verbs. PASS after fix.

**Corrected framing (skeleton, not prose):** the paper *prices* three controller families against a single dollar meter and *measures* which allocation frontier survives when each signal's acquisition cost is subtracted from the budget it spends. Abstract opens on the cost-accounting asymmetry, not "X is increasingly used… however… we introduce" (forbidden template avoided).

---

## Step 5 — Formal Problem Definition

**Estimand (R1, guidance.md §3.4).** The quantity of interest is $\max_\pi \text{Acc}_\pi(\tau_\pi(B))$ — matched-realized-budget accuracy — compared across controller families $\pi\in\{\text{training-free}, \text{probe}, \text{self-report}\}$ at a pre-registered grid of total dollar budgets $B$, where the unit of analysis is one (query, controller, budget-point) triple and the decision the estimand feeds is whether a near-zero-marginal-cost frozen probe can replace self-report/training-free signals as a compute-allocation controller (RQ1/RQ_INF_1/RQ_INF_2 below operationalize this single estimand into three binary tests).

**Notation.** Query set $Q$; each $q\in Q$ scored by programmatic correctness $y_t(q)\in\{0,1\}$ under execution tier $t\in\{\text{cheap},\text{exp}\}$ (exact/option match). Dollar cost of tier $t$ on $q$: $c_t(q)$ (measured tokens × price, dual cost model, M5). A **controller** $\pi$ emits signal $s_\pi(q)\in\mathbb{R}$ at acquisition cost $a_\pi(q)$. A **routing policy** thresholds: route exp iff $s_\pi(q)<\tau$. Realized total cost at threshold $\tau$: $\text{Cost}_\pi(\tau)=\sum_q\big[a_\pi(q)+c_{\text{cheap}}(q)+\mathbb{1}[s_\pi(q)<\tau]\,c_{\text{exp}}(q)\big]$. Realized accuracy: $\text{Acc}_\pi(\tau)=\tfrac1{|Q|}\sum_q\big[\mathbb{1}[s_\pi(q)<\tau]\,y_{\text{exp}}(q)+\mathbb{1}[s_\pi(q)\ge\tau]\,y_{\text{cheap}}(q)\big]$.

Each load-bearing adjective/verb → definition → measurement:

| Adjective/verb | Formal definition | Measured by |
|---|---|---|
| "matched realized budget $B$" | choose $\tau_\pi(B)$ s.t. $\text{Cost}_\pi(\tau)=B$ (linear interpolation between adjacent $\tau$) | offline simulator over cached outputs (M4) |
| "near-zero marginal cost" (probe) | $a_{\text{probe}}(q)=$ (head FLOPs)·price; prefill reused, so $\le 10^{-3}\times a_{\text{self-report}}(q)$ | M5 token/latency meter |
| "decision quality" | $\text{Acc}_\pi(\tau_\pi(B))$ at matched $B$; threshold-free: $\text{AUROC}(s_\pi, y_{\text{cheap}})$ | M5 harness |
| "matches / exceeds" | $\text{Acc}_{\text{probe}}(\tau(B)) \ge \text{Acc}_{\text{self-report}}(\tau(B))$, McNemar-tested | H1 |
| "sufficient" (training-free) | TOST equivalence within ±2pp of best controller at matched $B$ | H2 |
| "transfer" | $\Delta_{\text{transfer}}=\text{Acc}_{\text{probe,in-dist}}-\text{Acc}_{\text{probe,held-out}}$ at matched $B$ | H3 |
| "accuracy-per-dollar" | $\text{Acc}_\pi(\tau)/\text{Cost}_\pi(\tau)$; and AUCC = area under $(\text{Cost},\text{Acc})$ curve normalized between all-cheap and oracle | M5 |
| "calibrated" | 15-bin ECE of probe/self-report probability vs. $y_{\text{cheap}}$ | M5 |

Any adjective without a row is deleted from claims.

---

## Assumptions (A1..A5)

**On guidance.md §3.4 R2 (instrument validation).** R2's 5-step sequence (ground categories → draft/refine → validate against ≥2 human raters, κ≥0.7 → inspect confusion → freeze) targets *subjective* instruments (rubrics, LLM-judges, taxonomies). This design has no subjective instrument: every controller's ground truth is programmatic exact/option-match correctness (A1), and the probe (M2) is validated against that objective ground truth via the AUROC>0.60 walking-skeleton gate (A4), not via inter-rater agreement. R2 is therefore not applicable rather than silently skipped; A1's parser-agreement gate (≥99% on 100 hand-checked items) is the one place a human check enters, and it validates the *scoring* function, not a judgment rubric.

- **A1 (scorable ground truth).** Every eval query has automatic controller-independent correctness (C1). *Fails if* benchmark answers are ambiguous/free-form. *Detected by:* pilot gate (PG-1) — parser agreement ≥99% on 100 hand-checked GSM8K/MMLU-Pro items before scale-up. *Consequence if it fails:* the programmatic-correctness premise underlying every H1–H3 test is void (ground truth itself is unreliable) — the run does not proceed past the walking skeleton; the benchmark is swapped for one with unambiguous exact-match answers or the ambiguous subset is dropped and re-gated before any budget sweep.
- **A2 (offline-simulation exactness).** Both tiers + all signals precomputed once per query make any routing policy exactly reconstructible (N6 overview). *Fails if* tiers are stochastic and not cached per-sample. *Detected by:* pilot gate (PG-2) — re-running 50 cached queries live must reproduce Acc within ±0 (deterministic decode) / within sampling CI (k-sample tiers). *Consequence if it fails:* every downstream matched-budget number (H1, H2, H3 all read from the same offline simulator) is suspect, since it would mean the cached replay does not match live behavior — restrict scope to per-sample-cached signals only (drop any non-cacheable controller variant) and re-run the walking skeleton before scale-up.
- **A3 (cost commensurability).** All signal-acquisition costs are meterable in the same dollar unit (C2, M5). *Fails if* self-hosted marginal cost is undefinable. *Detected by:* dual-cost-model gate (PG-3) — dual cost model (API list price vs GPU-seconds); flag any controller ranking whose *sign flips* between models (t1). *Consequence if it fails:* H1/H2's matched-budget verdicts are reported *per cost model* rather than as one number, and any claim whose sign flips between the two cost models is downgraded to "cost-model-dependent" in the Claim–Evidence Map rather than stated as a main finding (degrades H1/H2, does not block them).
- **A4 (probe has non-trivial signal on the frozen backbone).** Prefill hidden states separate cheap-tier correctness (Claim 1, [DiffAdapt], [AdaptiveThinking]). *Fails if* AUROC(probe)≈0.5. *Detected by:* walking-skeleton gate (PG-4, "Gate A4" in Step 9) — probe AUROC vs cheap-tier correctness must exceed 0.60 on GSM8K dev before any budget sweep. *Consequence if it fails:* blocks — H1 and RQ_INF_2/H3 cannot be run at all (a non-informative probe has no matched-budget comparison to make), and the study stops at the walking skeleton per goal.md's skeleton-pass gate; only H2 (training-free sufficiency) remains answerable, reframed as "is training-free sufficient given no viable probe."
- **A5 (no train/eval leakage).** Probe train queries are disjoint & de-duplicated from eval (t3). *Fails if* near-duplicates inflate probe. *Detected by:* n-gram/embedding dedup gate (PG-5); cross-task transfer (RQ_INF_2) reported as primary, not appendix. *Consequence if it fails:* restricts scope — any in-distribution probe advantage (H1) is reported alongside the cross-task/cross-backbone transfer numbers (H3) as the primary evidence instead of the in-distribution number alone, since leakage would selectively inflate only the in-distribution comparison.

**Design constraints → confounds removed (R3, guidance.md §3.4):**
- Dual cost model (API list price + GPU-seconds, M5) removes the *cost-model-choice confound* — without both, a controller ranking could reflect which billing convention was picked rather than which controller allocates compute better (A3).
- Charging each controller its own signal-acquisition cost inside the same threshold sweep (M4/M5) removes the *free-signal confound* — without it, a cheaper-signal controller could win purely by leaving more of a nominal shared budget for expensive-tier generation, independent of decision quality (this is exactly what the B-alt cost-free AUROC contrast is built to detect).
- Disjoint, de-duplicated probe train/eval splits (A5) remove the *leakage confound* — without it, apparent probe superiority in H1 could be memorization of near-duplicate training queries rather than genuine difficulty separability.
- Precomputing both tiers once and replaying offline (A2) removes the *re-sampling-noise confound* — without it, apparent differences between controllers at the same nominal budget could reflect independent sampling noise in re-generated tiers rather than the routing policy itself.
- Two prompt-tuned self-report variants with the stronger reported as headline (t2) remove the *strawman-baseline confound* — without it, an apparent probe advantage over self-report could be an artifact of an arbitrarily weak elicitation choice rather than a genuine decision-quality gap.

---

## Step 6 — Pre-Registered Experiments

### RQ1 (digest N8) — Probe vs. self-report at matched budget
- **Assumption:** A1, A2, A3, A4.
- **Hypothesis H1:** On BOTH Stage-1 benchmarks (GSM8K, MMLU-Pro), at all 5 pre-registered budget points $B\in\{$ all-cheap+10%, 25%, 50%, 75%, 90% toward all-expensive $\}$, probe is **non-inferior** to the *strongest* self-report variant (McNemar does not reject in self-report's favor, BH-corrected α=0.05, AND the paired-bootstrap 95% CI on the accuracy gap does not exclude −1pp in self-report's favor — i.e. any loss is within a 1pp practical-equivalence margin) AND **strictly superior** (McNemar rejects in probe's favor, BH α=0.05, **AND the paired-bootstrap 95% CI on the accuracy gap excludes 0 with a point estimate ≥1pp — the effect floor below which a "win" is not counted**) at ≥2 of the 5 points on each benchmark. *(Effect floor of ≥1pp added per guidance.md §3.1: "significance without magnitude passes nothing" — a statistically-significant-but-sub-1pp McNemar rejection does not count toward the ≥2-of-5 superiority tally.)*
- **Metric:** $\text{Acc}_\pi(\tau_\pi(B))$ (matched-budget accuracy); secondary accuracy-per-dollar & AUCC (N8 metrics).
- **Verification:** paired McNemar on per-query correctness at each of 5×2=10 budget×benchmark cells; Benjamini–Hochberg across all 10; n=2,000 paired queries/benchmark → power ≈0.8 for ~3pp gap (N8 analysis_plan). 10,000× paired bootstrap 95% CI for AUCC differences and for the ≥1pp effect-floor check above.
- **Fallback (if H1 fails):** claim becomes *"large-model self-report retains a matched-budget accuracy edge of X pp that its elicitation cost does not erase at budgets below B\*; the probe is the accuracy-per-dollar choice only above B\*"* — a cost-crossover characterization (report the crossover budget, still a publishable frontier result via CO1/CO3).

### RQ_INF_1 (digest N8) — Are training-free signals sufficient?
- **Assumption:** A1, A2, A3.
- **Hypothesis H2:** Neither training-free controller (logit/predictive entropy M1a; self-consistency k=8 M1b) is **equivalent** to the best controller: TOST equivalence within ±2pp **fails** for each at ≥3 of 5 budget points on both benchmarks, AND probe's matched-budget accuracy exceeds each training-free controller by >2pp with paired-bootstrap 95% CI excluding 0 at ≥3 of 5 points (once self-consistency's k−1 extra samples are charged).
- **Metric:** matched-budget accuracy, accuracy-per-dollar, signal AUROC (N8).
- **Verification:** TOST (±2pp) per cell; BH across cells; 10,000× paired bootstrap for the >2pp margin.
- **Fallback (if H2 fails, i.e. a training-free signal IS equivalent):** claim becomes *"training-free self-consistency already suffices — the seed's 'training-free 信号够不够?' answers YES; the probe's marginal value is ≤2pp and does not justify its training pipeline"* — a negative-for-probe, positive-for-practice result (still answers RQ_INF_1).

### RQ_INF_2 (digest N8) — Cross-task / cross-backbone transfer
- **Assumption:** A4, A5.
- **Hypothesis H3:** A probe trained on one Stage-1 benchmark, evaluated on ≥2 of 3 held-out benchmarks (MATH-500, GPQA-Diamond, BBH), retains matched-budget accuracy ≥ the *training-free self-consistency router* at ≥3 of 5 budget points (i.e., transfer gap does not drop the probe below a no-training baseline). Cross-backbone (Llama-3.1 family): report $\Delta_{\text{transfer}}$; pre-registered expectation cross-backbone gap > cross-task gap.
- **Metric:** $\Delta_{\text{transfer}}$ and matched-budget accuracy vs self-consistency router (N8).
- **Verification:** paired bootstrap 95% CI on $\Delta_{\text{transfer}}$ per held-out benchmark; report full curves, no post-hoc point selection (t5).
- **Fallback (if H3 fails):** claim becomes *"frozen-probe controller quality is backbone/distribution-specific; the deployable recipe is per-backbone retraining on ~5k recycled self-consistency samples (cost quantified), not a transferable probe"* — reframes C3 as a costed deployment finding (CO2).

### Power and thin-cell pre-declaration (guidance.md Part 6 item 9 / Part 4 situation 5)

- **H1 (RQ1):** power ≈0.8 for a ~3pp gap at n=2,000 paired queries/benchmark (stated above, N8 analysis_plan) — the best-powered test, since it uses the full Stage-1 eval set at every budget point.
- **H2 (RQ_INF_1):** same n=2,000/benchmark and TOST ±2pp margin; power for a TOST equivalence test at this n and margin is lower than H1's difference test (TOST requires larger n than a difference test for the same margin) — cells are **pre-declared adequately powered for the ±2pp margin at n=2,000 (power ≥0.8 by construction of the margin choice)**; any cell whose realized discordant-pair count after routing falls below 30 pairs (sparse threshold sweep near the budget extremes) is **pre-declared INCONCLUSIVE, not equivalent and not non-equivalent**, and excluded from the ≥3-of-5 tally rather than counted either way.
- **H3 (RQ_INF_2):** transfer evaluation reuses the same n=2,000 held-out benchmark queries; any held-out benchmark for which the routed-expensive-tier subset (the only queries whose transfer accuracy is informative) falls below n=200 after matched-budget routing is **pre-declared INCONCLUSIVE** for that benchmark's contribution to the ≥2-of-3 held-out tally, never silently dropped and never scored as a null transfer gap.
- **General rule:** no thin cell (below the stated per-hypothesis floor) is ever reported as a PASS, a FAIL, or a null result — it is reported as INCONCLUSIVE with its realized n, per goal.md §5 step 2 and guidance.md Part 4 situation 5.

### Mandatory baselines

- **B0 "why do this at all" control — Random router at matched budget.** Routes exp on a random fraction chosen to hit each budget $B$ (no signal). Justifies the problem's existence: if no real controller beats Random on AUCC with paired-bootstrap CI excluding 0, then per-query signal is worthless and the whole comparison is void. Also anchors endpoints: all-cheap / all-expensive fixed policies and the Oracle router (routes exp iff cheap tier wrong) as the upper bound.
- **B-alt strongest-alternative-explanation control — capability-matched self-report + cost-free signal-quality head-to-head.** *Rival explanation:* "the probe wins matched-budget comparisons only because its signal is *cheaper* (the budget-accounting mechanic), not because its decisions are *better* — and/or because self-report was strawmanned." Isolated two ways: (1) self-report baseline uses BOTH variants (verbalized 0–100, P(True) [Kadavath 2022]), prompt-tuned on a dev split, same expensive model (t2), reporting the stronger as headline; (2) a **budget-independent AUROC(signal, cheap-tier correctness)** comparison that strips all cost accounting — if AUROC(probe) ≤ AUROC(self-report) yet probe wins matched-budget, the win is *purely mechanical* (cheaper signal), and the paper says so explicitly.

### Global fallback F-G1
If the central hypothesis family (H1 ∧ H2) collapses — probe neither matches self-report nor beats training-free — **pivot archetype from empirical-comparison to instrument/benchmark** (promote CO3): the paper's contribution becomes the precompute-then-simulate matched-budget harness and the finding that *no controller dominates the accuracy-per-dollar frontier; the ranking is signal-cost- and budget-regime-dependent*.
> Pivoted abstract sentence: *"We release a precompute-then-simulate harness that prices any per-query compute-allocation controller against one dollar meter, and use it to map the accuracy-per-dollar frontier — showing the best controller is budget-regime-dependent rather than universal."*

---

## Step 9 — Walking Skeleton

Minimal closed loop answering ONE binary question: *does the probe reach non-inferiority to self-report at even a single matched budget point on one benchmark?*

- **Arms (3):** frozen probe (M2, logistic head, last-layer prefill), strongest self-report (M3a verbalized), Random router (B0).
- **Task set:** GSM8K, 500 eval queries + 1,000 train queries (probe labels recycled from k=8 cheap samples).
- **Backbone pair:** Qwen2.5-7B-Instruct (cheap) vs. Qwen2.5-72B-Instruct or GPT-4o-class (exp).
- **Metrics (deterministic only):** matched-budget accuracy at the single $B=50\%$ point; AUROC(probe, cheap correctness); realized dollar cost via M5.
- **Precompute:** both tiers + all three signals cached once (A2); routing is offline.
- **Expected cost/wall-clock:** ~500×(1 prefill+answer + 8 cheap samples + 1 exp CoT + 1 self-report) ≈ 5.5k generations; cheap tier ~5–10 A100-GPU-hours; exp+self-report API ≈ $50–120; < 1 day.
- **Gate A4:** probe AUROC > 0.60 on GSM8K dev, else stop.
- **Skeleton-passed criterion:** probe matched-budget accuracy ≥ self-report − 1pp at $B=50\%$ AND all three arms run through one shared simulator producing a $(\text{Cost},\text{Acc})$ point. **Scaling to Stages 1–2 is then a config change** (add benchmarks/backbones/budget points/thresholds to loops), *not* a code change, because every threshold/budget point is an offline replay over the cache (run count O(benchmarks×backbones), N6 feasibility).

---

## Claim–Evidence Map

| Claim the abstract will make | Trace | Status |
|---|---|---|
| Signal cost is charged from the allocated budget → probe has structural cost advantage | Step 0 asymmetry; M4/M5; Claim 4 | supported-by-design |
| First matched-realized-dollar three-way controller comparison, each charged its own signal cost | CO1; RQ1/RQ_INF_1; M5 | needs-experiment (H1, H2) |
| Frozen probe matches/exceeds self-report at matched budget | H1 (RQ1) | needs-experiment; fallback-covered (cost-crossover) |
| Training-free signals are insufficient once sampling cost is charged | H2 (RQ_INF_1) | needs-experiment; fallback-covered (training-free suffices) |
| Probe advantage's transfer behavior is characterized (not assumed) | H3 (RQ_INF_2); C3 | needs-experiment; fallback-covered (per-backbone retrain recipe) |
| Any real controller beats no-signal Random | B0 | needs-experiment |
| Probe win is decision-quality, not merely cheaper signal | B-alt (AUROC head-to-head) | needs-experiment |
| Reusable precompute-then-simulate accuracy-per-dollar harness | CO3; M5; N11 | supported-by-design |

Every claim traces to an H-id or a Step-5 definition.

---

## Abstract v0 (draft, mechanism-first) — DRAFT BEFORE RESULTS

> A per-query compute-allocation controller is paid for out of the same budget it decides how to spend: self-report costs an extra model call and self-consistency costs k extra samples, while a probe reading a frozen backbone's prefill hidden state costs almost nothing because that computation already happened. We price three controller families — training-free signals (logit entropy, self-consistency agreement), a frozen-backbone probe, and large-model self-report — against a single dollar meter, charging each its own signal-acquisition cost, and measure matched-realized-budget accuracy via a precompute-then-simulate harness that caches both execution tiers once and replays any routing policy offline. We pre-register binary criteria for whether the probe reaches non-inferiority to self-report, whether training-free signals suffice within a ±2pp equivalence margin, and how probe quality transfers across tasks and backbones. All controllers are judged only by controller-independent programmatic correctness at equal spend. *[DRAFT — synthesized from digest.md, no experiments run.]*
