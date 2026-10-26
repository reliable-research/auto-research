# Is Corpus-Level Estimation Strategy-Proof? The Economics of Evasion at Population Scale — Pre-Registered Paper Specification

> Generated from digest.md + README.md. Status: specification, no experiments run. All numeric thresholds below are PRE-REGISTERED decision criteria, not results.

---

## Step 0 — Core Asymmetry (升维)

**Asymmetry sentence.** A budget-bounded paraphrase adversary pays a fixed per-document cost to flip a single-document AI-text detector's verdict, but to move a corpus-level AI-prevalence *proportion* by a fixed margin it must spend that same per-document cost on a fixed *fraction* of the corpus — so one unit of evasion technology is scale-invariant against a per-document label and scale-taxed against a population proportion.

**判据 (deletion test).** Delete the domain nouns:
> "A budget-bounded ___ pays a fixed per-unit cost to flip a single ___, but to move an aggregate ___ by a fixed margin it must spend that cost on a fixed fraction of the ___ — so one unit of ___ is scale-invariant against a single ___ and scale-taxed against an aggregate."

This does **not** survive as a valid generic statement: it is *false* in general. Aggregates are not universally fraction-limited — a mean is dominated by concentrated outliers, so a rival adversary with economies of scale or an outlier-sensitive statistic could move an aggregate at O(1) cost. The sentence is only true given the *specific* domain facts: (i) paraphrase evasion has a bounded, quality-preserving, roughly fixed per-document cost (the presupposed single-document result, N1 constraint / A2), and (ii) the estimator is a proportion whose value no single document can dominate (mixture-MLE, A4). Remove those nouns and the claim is not generically valid — it is wrong. Passes: not a bridge.

---

## Step 2 — Archetype

**Primary archetype:** counterintuitive empirical measurement — "is X strategy-proof? surprisingly, the cost of evasion *grows* with scale" (consistent with digest N12 = `empirical`). **Secondary:** conceptual framework (CO1: a cost–accuracy game formalizing evasion economics for aggregate estimation).

**Downstream consequences:**
- **(a) Abstract contribution slot:** a *measured scaling law* — the exponent β of minimum-evasion-budget vs. corpus size N — plus the binary verdict "corpus-level estimation is / is not more strategy-proof than single-document detection under matched budget."
- **(b) Intro logic:** "what becomes measurable" (the price of evasion as a function of population scale), NOT "beat a detector's number." The intro leads with the asymmetry, then poses the falsifiable question of whether single-document pessimism transfers.
- **(c) Evidence standard:** a direction + a sign-of-slope with CI, robust across ≥2 cost models and against a capability-matched adaptive adversary. A single-N accuracy win is insufficient; the load-bearing evidence is the *scaling* behavior and its survival under the strongest rival adversary.

---

## Step 3 — Taste self-audit

- **Bridge check.** Risk: framing as "single-document detection and corpus-level estimation were never connected; we connect them." FAIL if left there. **Fix (skeleton change):** the object is not a connection but an *asymmetry in evasion economics* — we isolate and measure how one adversary currency buys different amounts of bias against two target quantities. The deliverable is β and a strategy-proofness verdict, not a bridge.
- **Synthesis check.** Risk: method = MonitorAIScale estimator (M2) + AdaptiveWMAttack adversary (M3) glued together. FAIL if the contribution is the combination. **Fix:** the estimator and adversary are *instruments*; the contribution is the measured cost-vs-N curve and the isolation of scale-driven robustness from estimator-design robustness (RQ_INF_2) and from attack weakness (B-alt).
- **Verb check.** Banned family (integrate/unify/leverage) not used as load-bearing verbs. Load-bearing verbs: *formalize* (the cost–accuracy game), *isolate* (scale vs. design), *measure* (β), *gate* (evasion by budget). PASS.
- **Abstract-opening rule:** mechanism/asymmetry first; no "X is increasingly used… however… we introduce." Enforced in Abstract v0.

---

## Step 5 — Formal Problem Definition

**Estimand (guidance.md R1).** The minimum adversary rewrite budget $B_{\min}(\varepsilon,N)$ required to bias a corpus-level AI-prevalence estimate by margin $\varepsilon$, as a function of corpus size $N$ (and the fitted scaling exponent $\beta$ of $B_{\min}$ on $N$); unit of analysis is one corpus per (N, allocation-strategy, estimator, seed) cell; reference population is semi-synthetic RAID/HC3-derived corpora with experimenter-controlled ground-truth $\alpha$; the decision this feeds is whether population-scale AI-content auditing can be trusted as evasion-resistant where per-document detection is known to be evadable.

**Notation.** Corpus $D_N = \{d_1,\dots,d_N\}$; each $d_i$ has a latent label $y_i \in \{\text{human}, \text{AI}\}$. True prevalence $\alpha = \tfrac1N\sum_i \mathbb{1}[y_i=\text{AI}]$. A corpus-level estimator $E$ returns $\hat\alpha = E(D_N)$. A single-document detector $g$ returns a score $g(d_i)$; AUROC of $g$ over $D_N$ is $\mathrm{AUROC}(g;D_N)$. An adversary $\mathcal{A}$ transforms $D_N \to D_N'$ by paraphrasing, spending budget $B(\mathcal{A}) = \sum_i c(d_i, d_i')$ under a cost model $c$ (per-token, or per-document-touched × strength). Clean error $e_0(N) = \mathbb{E}|E(D_N) - \alpha|$; attacked error $e_B(N) = \mathbb{E}|E(D_N') - \alpha|$. Bias margin $\varepsilon = |E(D_N') - E(D_N)|$.

| adjective/verb (from Claims) | definition (computable) | measurement |
|---|---|---|
| **strategy-proof (at scale)** | $\beta > 0$, where $\beta$ = OLS slope of $\log B_{\min}(\varepsilon,N)$ on $\log N$ | M5 log-log regression, bootstrap CI |
| **robust (estimator)** | $e_B(N) \le 2\,e_0(N)$ at fixed budget $B$ | M2 vs. ground-truth $\alpha$ |
| **uneconomical evasion** | cost-per-unit-bias $c^*(N)=B_{\min}(\varepsilon,N)/\varepsilon$ strictly increasing in $N$ | M4 best-response search across M5 sweep |
| **fragile (single-document)** | $\mathrm{AUROC}(g;D_N') \le 0.60$ under the same budget $B$ | M1 pre/post paraphrase |
| **budget-bounded** | $B(\mathcal{A}) \le B$, a pre-set scalar in a declared cost model $c$ | M3 accounting |
| **bias / margin ε** | $\varepsilon = |E(D_N') - E(D_N)|$; target $\varepsilon = 0.10$ | M4 |
| **minimum budget to bias ε** | $B_{\min}(\varepsilon,N) = \min\{B(\mathcal{A}) : |E(D_N')-E(D_N)| \ge \varepsilon\}$ | M4 greedy/grid search vs. surrogate |

Any adjective without a row is deleted from the claims.

---

## Assumptions (A1..A6)

- **A1 — Ground-truth controllability.** Semi-synthetic corpora have a known, experimenter-set $\alpha$. *Fail:* generation leaks a trivial artifact making α recoverable regardless of estimator. *Detect:* pilot/walking-skeleton no-adversary arm — clean estimator must recover α within CI **and** a shuffled-label control must NOT. *Gate:* PG-1, checked inside the walking skeleton (Step 9, no-adversary + shuffled-label arms), before any scale-up. *Consequence:* if it fails, no H\* is scorable (there is no trustworthy ground truth to measure error against) — this is a placebo-style invalidation that blocks RQ1, RQ_INF_1, and RQ_INF_2 alike until the corpus-construction procedure is fixed and re-piloted.
- **A2 — Single-document fragility premise (N1 constraint).** A DetectGPT/Fast-DetectGPT-style $g$ collapses to $\mathrm{AUROC}\le 0.60$ under the adversary's paraphrase. *Fail:* $g$ stays robust → no contrast to measure. *Detect:* walking-skeleton M1 arm; if AUROC stays >0.60, swap generator/detector before scaling. *Gate:* PG-2, checked inside the walking skeleton (Step 9, M1 arm), before any scale-up. *Consequence:* if it fails, RQ1 loses its fragility contrast (nothing to be "more strategy-proof than") and is blocked — not degraded, blocked — until a generator/detector pair that actually collapses under the budget is substituted.
- **A3 — Fixed, scale-free per-document paraphrase cost (C2).** The cost to meaningfully rewrite one document is bounded and does not fall with N. *Fail:* adversary has economies of scale. *Detect:* report ≥2 cost models (per-token, per-document-touched); the β sign must be invariant (threat t2). *Gate:* Phase C (full-scale run) — this cannot be checked in the cheap single-cost-model pilot; it is only observable once both cost models are swept across the full N grid. *Consequence:* if the β sign disagrees between cost models, RQ_INF_1 downgrades from its main PASS wording to the pre-committed "cost-model-dependent, unresolved" wording (Step 6 RQ_INF_1 fallback) rather than being scored a clean PASS or FAIL.
- **A4 — Estimator consistency (A of M2).** $e_0(N)$ is (near-)unbiased and non-increasing in N under no attack. *Fail:* estimator biased/inconsistent. *Detect:* pilot no-adversary sweep across N; require $e_0$ to shrink or plateau, not grow. *Gate:* PG-4, checked inside the walking skeleton (Step 9 pilot no-adversary sweep) and re-verified at full scale in Phase C. *Consequence:* if it fails, $e_0(N)$ is not a meaningful baseline, which invalidates the $e_B(N)\le 2\,e_0(N)$ criterion in RQ1 and the matched-baseline ratio in RQ_INF_2 — both are blocked until a consistent estimator variant is substituted.
- **A5 — Adversary knowledge bound (C4 scope).** Adversary is budget-bounded and non-omniscient (not white-box on the exact aggregation statistic). *Fail:* realistic adversaries are white-box. *Detect:* out-of-scope by declaration; B-alt tests an *adaptive surrogate* adversary as the strongest in-scope proxy and reports it as a lower bound on evasion difficulty. *Gate:* by declaration — there is no empirical gate for the excluded white-box regime itself; the closest in-scope proxy (the adaptive/coordinated adversary) is checked via B-alt in Phase C. *Consequence:* does not block any H\*, but restricts every claim's scope to the declared threat model — the abstract and conclusion must state the budget-bounded, non-omniscient envelope explicitly rather than let a reader generalize to a fully adaptive attacker.
- **A6 — Imperfect coordination within budget (C1).** Per-document paraphrase perturbations cannot be made perfectly directional-and-cheap across the whole corpus simultaneously. *Fail:* cheap perfect coordination. *Detect:* this is exactly what RQ1/RQ_INF_1 measure; the adaptive-coordinated adversary arm is the direct test. *Gate:* Phase C (the RQ1/RQ_INF_1 main experiments, adaptive-coordinated adversary arm) — not checkable in the pilot, which only runs the non-adaptive adversary. *Consequence:* if it fails (coordination turns out to be cheap), RQ1 and RQ_INF_1 both fall to their pre-committed fallback wording ("aggregation confers no strategy-proofness at the tested scales" / β≤0 wording) rather than the main PASS wording.

---

## Step 6 — Pre-Registered Experiments

Shared grid: $N \in \{10^2,10^3,10^4,10^5\}$; 5 seeds per (N, strategy, estimator) cell; $\varepsilon=0.10$; cost models $c \in \{\text{per-token}, \text{per-document-touched}\}$; generators: ≥3 families (GPT-, Llama-, Claude-class) from RAID; base corpora RAID + HC3.

**Design constraints and the confound each removes (guidance.md R3).**
- Matched-prompt HC3 pairing for the human/AI portions of every semi-synthetic corpus removes the *topic confound* (an estimator could otherwise recover $\alpha$ by exploiting topic rather than authorship signal).
- The shuffled-label negative control (A1) removes the *trivial-recoverability confound* (a construction artifact making $\alpha$ recoverable regardless of what the estimator does).
- Reporting $\hat\beta$ under both declared cost models (A3) removes the *cost-model-artifact confound* (a scaling conclusion that only holds under one arbitrary bookkeeping convention).
- The adaptive/coordinated adversary arm (B-alt, A6) removes the *weak-attacker confound* (an apparent robustness that only survives against a non-adaptive, independent-perturbation attacker).
- The naive per-document-average estimator control (RQ_INF_2) removes the *generic-averaging confound* (an apparent estimator-design advantage that is really just a property of averaging over many documents).

**Power statement (guidance.md R8 / Part 2 A2 evidence standard).** 5 seeds × ≥3 generators per (N, strategy, estimator) cell is the pre-registered minimum designed to detect the stated effect floors (e.g. $\hat\beta\ge 0.5$ for RQ_INF_1, a $\ge 2\times$ ratio for RQ_INF_2) at power $\ge 0.8$ under a conservative assumed effect size; achieved power is checked post-hoc from the realized bootstrap CI width. Any cell whose post-hoc power falls below 0.8 (CI too wide to distinguish the effect floor from the null at $\alpha=0.05$) is pre-declared **INCONCLUSIVE**, never scored as a null result and never silently dropped from the reported grid (guidance.md Part 4 situation 5).

### RQ1 (digest N8 RQ1) — Is corpus-level estimation as fragile as single-document detection, or does evasion become uneconomical at scale?
- **Assumption:** A1, A2, A4, A6.
- **Hypothesis (binary):** At $N=10^5$ under a fixed total budget $B$ that drives $\mathrm{AUROC}(g)\le 0.60$, the corpus estimator satisfies $e_B(10^5) \le 0.05$ **and** $e_B(10^5) \le 2\,e_0(10^5)$, while the paired single-document detector satisfies $\mathrm{AUROC}(g;D')\le 0.60$. (Robust estimate + collapsed detector at matched budget.)
- **Metric:** $e_B(N)=\mathbb{E}|\hat\alpha-\alpha|$; $\mathrm{AUROC}(g;D')$ (digest N8 metrics).
- **Verification:** bootstrap 95% CI on $e_B$ (5 seeds × ≥3 generators); criterion met iff the CI upper bound $\le 0.05$ and the AUROC CI upper bound $\le 0.60$. Holm correction across generators.
- **Aggregation:** vote across generator families — criterion must hold on $\ge 2$ of the $\ge 3$ tested generator families (Holm-corrected per-family test at per-test $\alpha=0.05/3$); a single-generator pass does not qualify as PASS.
- **Fallback:** IF $e_B(10^5) > 2\,e_0(10^5)$ → claim *"Corpus-level estimation inherits single-document fragility; aggregation confers no strategy-proofness at the tested scales."* (Publishable negative; feeds F-G1.)

### RQ_INF_1 (digest N8) — Minimum budget to bias by ε, and its scaling exponent β vs. N.
- **Assumption:** A3, A6.
- **Hypothesis (binary):** The fitted log-log slope $\hat\beta \ge 0.5$ with bootstrap 95% CI lower bound $> 0$, under *both* cost models. (Budget-to-bias grows at least as $\sqrt{N}$; evasion strictly more expensive at scale.)
- **Metric:** $B_{\min}(\varepsilon,N)$ from M4 best-response search; $\hat\beta$ = OLS slope of $\log B_{\min}$ on $\log N$ (digest N8 metric; N8 analysis plan).
- **Verification:** pre-registered one-sided test $H_0: \beta\le 0$ vs. $H_1:\beta>0$ at $\alpha=0.05$; bootstrap 95% CI on $\hat\beta$ over seeds; require CI lower bound $>0$ AND point estimate $\ge 0.5$ in both cost models.
- **Fallback:** IF $0 < \hat\beta < 0.5$ but CI excludes 0 → weaker claim *"Evasion cost grows sublinearly with corpus size — cheaper than proportional but not free."* IF CI includes 0 or $\hat\beta\le 0$ → *"Aggregate-estimate evasion cost does not grow with scale"* (refutes central claim; F-G1).

### RQ_INF_2 (digest N8) — Is robustness a property of aggregation *design* or of corpus-level estimation per se?
- **Assumption:** A1, A4.
- **Hypothesis (binary):** At matched N and B, the naive per-document-average estimator's error exceeds each dedicated estimator's by $\ge 2\times$: $e_B^{\text{naive}} \ge 2\,e_B^{\text{MLE}}$ and $e_B^{\text{naive}} \ge 2\,e_B^{\text{DUCI}}$.
- **Metric:** $e_B(N)$ for {mixture-MLE, debias-aggregate, naive-average} at matched (N,B).
- **Verification:** paired bootstrap on the ratio $e_B^{\text{naive}}/e_B^{\text{dedicated}}$ per seed; criterion iff 95% CI lower bound $\ge 2$.
- **Fallback:** IF naive-average is equally robust ($e_B^{\text{naive}} \le 1.25\,e_B^{\text{dedicated}}$) → claim *"Robustness is a generic consequence of averaging over a large population, not of the specific estimator design"* — reframes CO3, still supports the scale thesis (threat t3).

### Mandatory baselines
- **B0 — "why do this at all" control:** *population-scale single-document detection* = mean of per-document $g$ verdicts, no distributional estimator, no calibration. This is what a practitioner does absent our framing. Expected to inherit single-document fragility ($e_B$ large, tracking AUROC collapse). If B0 is *already* strategy-proof, the whole distributional-estimator apparatus is unjustified and the paper has no problem to solve.
- **B-alt — strongest-alternative-explanation control:** a *budget- and capability-matched adaptive/coordinated adversary* (DPO-tuned paraphraser à la AdaptiveWMAttack, optimizing a surrogate of $\hat\alpha$), run at identical budget to the non-adaptive DIPPER-style adversary. **Rival explanation it kills:** "the observed corpus-level robustness is an artifact of a *weak, non-adaptive* adversary; a competent budget-matched attacker evades just as cheaply, so robustness is not scale-driven." If $\hat\beta>0$ and the RQ1 criterion survive against the adaptive adversary at matched budget, the claimed cause (scale economics) is isolated from attack weakness.

### Global fallback F-G1
IF the central hypothesis family fails (RQ1 fallback fires AND RQ_INF_1 gives $\hat\beta\le 0$): **pivot archetype from "counterintuitive positive measurement" to "boundary-characterization / cautionary map."** Pivoted abstract sentence: *"We show that corpus-level AI-prevalence estimates inherit single-document evasion fragility, and we map the budget, coordination, and estimator regimes in which population-scale auditing gives practitioners a false sense of security."*

---

## Step 9 — Walking Skeleton

**One binary question:** at a single corpus size, does the distributional estimator resist a fixed-budget adversary while the single-document detector collapses under the *same* attack?

- **Arms (3):** (1) M1 single-document detector on $D$ and paraphrased $D'$; (2) M2 mixture-MLE estimator on clean $D$; (3) M2 on adversary-perturbed $D'$ (non-adaptive DIPPER paraphraser, fixed budget).
- **Task set:** one $N=10^3$ corpus, one generator family, one domain (HC3), known $\alpha=0.5$, 3 seeds.
- **Metrics (deterministic):** $e_B=|\hat\alpha-\alpha|$, $e_0$, $\mathrm{AUROC}(g)$ before/after.
- **Cost:** paraphrasing $10^3$ docs on a local 7B ≈ a few GPU-hours; estimator fits = CPU-minutes. Total < 1 day, < \$50-class.
- **Skeleton passed iff:** clean M2 recovers $\alpha$ within 0.03; M1 AUROC drops to $\le 0.60$ under paraphrase (A2 holds); M2-under-attack error is measurable and strictly below the B0 naive-collapse level. **Scaling criterion:** passing means the full grid (N-sweep, seeds, generators, cost models, adaptive adversary) is reachable by changing config lists only — no new estimator/adversary code paths.

---

## Claim–Evidence Map

| Claim (final abstract will make) | Trace | Status |
|---|---|---|
| Evasion of a per-document label is scale-invariant; evasion of a population proportion is scale-taxed (the asymmetry). | Step 5 def of $B_{\min}$, β; RQ_INF_1 (H: β≥0.5) | needs-experiment |
| Corpus-level estimator stays accurate under fixed budget while the paired detector collapses. | RQ1 (H: $e_B\le0.05 \wedge \le 2e_0$, AUROC≤0.60) | needs-experiment |
| Minimum evasion budget grows with corpus size (β>0). | RQ_INF_1 | needs-experiment; fallback-covered (sublinear / null) |
| Robustness is (partly) aggregation design, testable vs. naive average. | RQ_INF_2 | needs-experiment; fallback-covered (generic-averaging reframe) |
| The claim is conditional on a budget-bounded, non-omniscient adversary. | A5, B-alt, C4 scope | supported-by-design (scope declaration) |
| Trivial single-document-at-scale approach is fragile (problem is real). | B0 | needs-experiment (design-justifying control) |
| Result robust to cost-model choice. | A3, threat t2 (β sign invariant across 2 cost models) | supported-by-design |

Every claim traces to an H-id (RQ1 / RQ_INF_1 / RQ_INF_2) or a Step-5 definition. No claim rests on an unmeasured adjective.

---

## Abstract v0 (draft — BEFORE results)

> *Draft, mechanism-first; no experiments run.*

A budget-bounded paraphrase adversary that flips a single-document AI-text detector at a fixed per-document cost must spend that same cost on a fixed *fraction* of a corpus to move an aggregate prevalence estimate — so identical evasion technology is scale-invariant against a per-document label yet scale-taxed against a population proportion. We formalize this as a cost–accuracy game between a budget-bounded paraphraser and a corpus-level distributional prevalence estimator, and measure the exponent β by which the minimum budget to bias the aggregate estimate by a fixed margin scales with corpus size N. We isolate scale-driven robustness from estimator-design robustness (a naive-averaging control) and from attack weakness (a capability-matched adaptive adversary), and gate every conclusion on a pre-registered one-sided test that the scaling exponent exceeds zero across two distinct adversary cost models. The threat model is explicitly budget-bounded and non-omniscient.

*(~150 words.)*
