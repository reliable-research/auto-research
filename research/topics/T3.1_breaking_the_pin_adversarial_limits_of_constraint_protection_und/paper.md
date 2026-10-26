# Breaking the Pin: Adversarial Limits of Constraint Protection under Context Compaction — Pre-Registered Paper Specification

> Generated from digest.md + README.md. Status: specification, no experiments run.
> All numbers below are **pre-committed thresholds**, not measured results. Every N9 result cell remains empty until the sweep is executed.
> ID conventions inherited from digest.md: challenges `C1–C5`, mechanisms `M1–M5`, research questions `RQ1/RQ2/RQ_INF_3`, contributions `CO1–CO3`, threats `t1–t6`, claims `Claim1–Claim5`.

---

## Step 0 — Core Asymmetry (升维)

**Invariant sentence.**
> Under a fixed-budget lossy compaction channel replayed across a session, a pinned constraint survives only if it re-wins the retention-budget competition at *every* compaction event, whereas an adversary need only make it lose *once* — and can amortize an unbounded, offline optimization budget to engineer that single loss against a defender who pays only a bounded per-event budget.

This is a **durability asymmetry** (an all-quantifier defender vs. an exists-quantifier attacker over a sequence of lossy-channel events) compounded by a **cost asymmetry** (amortizable offline attack budget vs. non-amortizable per-turn defense budget). It states the *structure of the game*, not the phenomenon "pinning fails" (that is the observation, Claim1), and it is not a bridge between literatures.

**判据 test (domain-noun deletion).** Delete `compaction channel`, `pinned constraint`, `retention-budget competition`, `compaction event`:
> "Under a fixed-budget lossy ___ , a ___ survives only if it re-wins the ___ at *every* ___, whereas an adversary need only make it lose *once* — and can amortize an offline budget to engineer that loss against a defender who pays only a bounded per-event budget."

Result: the schema is **empty**. "A ___ survives only if it re-wins the ___" carries no truth value once you remove that the channel is *lossy under a fixed budget* (what forces the competition), that the object must survive *verbatim* (what makes losing-once catastrophic), and that the event is *repeated* (what creates the all-vs-exists split). Nothing generic survives deletion → grounded, not a bridge. (Contrast the forbidden "pinning and adversarial optimization were never connected; we connect them," which *does* survive deletion as a generic — rejected.)

---

## Step 2 — Archetype

**Primary: Measurement / boundary-characterization study** (digest N12 = `empirical`; README label `[边界]`).
**Secondary: Protocol/instrument artifact** (reusable defense-variant × attack-strength matrix + two-tier oracle, CO3) — instrumental, not headline.

Downstream consequences:
- **(a) Abstract contribution slot:** *a measured boundary and a price* (BT50/BT90 curves + attacker/defender cost ratio; CO1, CO2) — **not** a proposed defense. C1 is pre-declared only partially addressable; the seed asks for no mitigation.
- **(b) Intro logic = "what becomes computable," not "beat a number."** "Pinning fails" is given (Claim1); the missing quantity is the *shape and price* of failure — a cost-per-unit-robustness curve that ranks pinning variants. No incumbent number to beat; the deliverable is the first map of a region.
- **(c) Evidence standard:** judged on **estimand identifiability under noise**, not a leaderboard. Every rate carries a Wilson CI, every boundary a bootstrap CI, every cross-condition claim a pre-registered test with multiplicity correction and a pre-committed falsifier. A sharp negative (an unbreakable-in-range variant) is a *stronger* result, not a failure.

---

## Step 3 — Taste self-audit

- **Bridge?** Naive framing "prompt-injection × memory-compaction, never combined" would be a bridge — **risk present**. **Fix (skeleton-level):** the load-bearing object is the Step-0 *durability asymmetry*, a property inside the compaction game that would exist even if only one literature had named it. The paper measures a price curve implied by that asymmetry; it does not derive value from joining fields. PASS after fix.
- **Synthesis?** Reuses GCG/SlotGCG/ChatInject attacks and Wilson/bootstrap stats. **PASS:** novelty is the *strength-normalized, cost-instrumented, oracle-verified measurement design* (M2+M4+M5) plus the commensurability construction (C2/C4) that puts heterogeneous defenses on one axis — a new *estimand*, not a new attack.
- **Verbs?** Draft contained "combine/leverage/integrate" — **FAIL → fixed.** Operative verb set: **measure, locate, sweep, gate, price, falsify, isolate, normalize.**
- **Abstract-opening rule:** forbidden "X is increasingly used… however… we introduce" rejected; opener leads with the asymmetry mechanism and a measure/price verb (see Abstract v0). PASS.

---

## Step 5 — Formal Problem Definition

**Notation.** Trajectory `T` = turns `τ_1..τ_T`. Compaction event `κ`: lossy map compressing history into `≤ B` tokens; `E(T)=(e_1..e_m)`, `m≥1`. Pinned constraint `c` (predicate the agent must satisfy for the rest of the session); suite `C`. Defense variant `d ∈ D = {d_0, d_reinj, d_kcopy, d_cksum, d_slot}` (M1: control, verbatim re-injection, redundant k-copy, checksum-verified, structural slot). Attack family `a ∈ A = {a_wb, a_bb}` (white-box gradient à la SlotGCG/GCG; black-box template-role forgery à la ChatInject). Normalized strength `s ∈ [0,1]`. Trial seed `ω`. Break-through indicator `V(c,T;d,a,s,ω) ∈ {0,1}`.

**Objective (formal restatement of N1).** For each `(d,a,model g)` estimate the break-through rate
`p_{d,a,g}(s) = Pr_{c,T,ω}[V=1]`, and derive (i) boundary scalar BT50, (ii) cost ratio R at BT50, (iii) cross-condition ordering stability.

**PHASE-A FIX — citation-cache provenance caveat (goal.md §3 checklist item 2).** "SlotGCG/GCG" and "ChatInject" above name attack *families*, not verified cache records: digest.md N3's ten related-work citations (ChatInject, ThreatSnapshots, SlotGCG, TAO-Attack, GuidedBench, TensorTrust, COMI, InfoChannel, LightMem, GCG) were grounded via a general OpenReview corpus search (`topics/corpus/ideas.jsonl`) that is **separate from this topic's formal harvest** in `discussion/reference_candidates.jsonl`; none of their OpenReview IDs resolve against that cache. Per goal.md's hard gate ("citations only via `selected` cache keys"), these names must be treated as **provisional/unverified** until a targeted re-harvest resolves their exact records — they are retained here only as informal, memory-free-text shorthand for attack *mechanisms* (gradient suffix search; template-role forgery), not as citable sources. The now-canonical cache (Task 1 of this run) does contain cache-verified, `selected` entries covering adjacent ground and usable today: `AgenticSTS2026` (method-twin: bounded, ablatable memory contract for long-horizon agents), `ForensicTrajSig2026` (adjacent: agent memory-poisoning detection), `FoldAct2025` (adjacent: benign context-folding mechanism), `TRAP2026` (adjacent: current agent prompt-injection benchmark), `GoExploreRedTeam2026` (adjacent: automated attack-search methodology), `GCGDiffusion2026` (adjacent: GCG-family generality), `TrustworthyAgenticAI2025` (contrast: a non-pinning defense paradigm), `RecursiveLM2026` (adjacent: grounds the B-alt "context rot" rival explanation), and three background structural exemplars (`JailbreakVsFilters2025`, `PackKV2026`, `ClawAgentSecurity2026`). Phase E prose must cite from this cache-verified set for anything not re-harvested; the informal SlotGCG/ChatInject/GCG mechanism names may remain in the Notation gloss only as unattributed method labels until re-harvested.

Every load-bearing adjective/verb from the Claims list → definition → measurement:

| Adjective/verb (Claim) | Definition | Measured by |
|---|---|---|
| "break-through" (Claim1,2) | `V=1`: constraint `c` violated *after* a compaction event, given it was present pre-compaction (attribution gate) | two-tier oracle M3 |
| "break-through rate" (Claim1,2) | `p̂ = (1/N)Σ_ω V` per cell `(d,a,g,s)` | M3, Wilson 95% CI |
| "findable, finite boundary" (Claim2) | logistic `p=σ(β_0+β_1 s)`; `BT50 = −β_0/β_1`; findable iff BT50∈[0,1] and its bootstrap 95% CI ⊂ [0,1] | M5 fit + bootstrap |
| "unbreakable-in-range" (RQ1 falsifier) | `max_s p̂_{d,a,g}(s) < 0.05` across the whole grid | M3/M5 |
| "commensurable strength axis" (C2) | `s = (log ρ_a − log ρ_a^min)/(log ρ_a^max − log ρ_a^min)`, `ρ_a` = raw attack budget per family (M2), bounds fixed pre-run | M2 |
| "cost ratio" R (Claim3) | `R_{d,a,g} = AC_{d,a,g}(BT50)/DC_d`; AC = fwd+bwd passes / tokens to reach BT50 in token-equivalent; DC = extra tokens/turn × compaction-relevant turns | M4, ≥2 currencies |
| "differs meaningfully across variants" (Claim3) | Holm-corrected Wilcoxon on `log R` rejects equality for ≥1 pair (α=0.05) AND max/min variant R ≥ `θ_R = 2×` | M4/M5 |
| "ranking model/attack-agnostic" (Claim4) | mean pairwise Kendall's `τ ≥ τ* = 0.6` (permutation p<0.05) of variant orderings across (g,a) | M5 |

**Oracle procedure for V (M3).** (1) Hard constraints (forbidden tool call fired; numeric/format rule broken): deterministic programmatic check from execution log. (2) Soft constraints: GuidedEval-style rubric LLM-judge; `V=1` iff checklist completion > preset threshold. (3) Attribution gate: violation must occur at/after `e_1` with the constraint present pre-compaction. Oracle validity gated at G0 (below).

**R2 instrument-validation sequence for the soft-constraint judge** (guidance.md §3.4 R2; PHASE-A FIX — the prior draft stated only step③ below, with an acceptance bar under guidance's required minimum): ① ground the checklist categories (entity/action items) in the pinned constraint's own written specification, not invented ad hoc — each checklist item must trace to a clause of the constraint `c` as authored. ② Draft the rubric wide on a held-out calibration slice of ~50 constraint-violation cases disjoint from the ~200-case audit set below, then refine with named merge/split/remove operations until items stop changing case verdicts. ③ Validate the frozen rubric against ≥2 independent human raters on a ~200-case held-out audit set; **acceptance threshold raised to Cohen's κ ≥ 0.7** (guidance.md §3.4 R2 states κ ≥ 0.7 is required, not ≥0.6 — the prior draft's G0 threshold of 0.6 undershot this and is corrected here). ④ Inspect the confusion structure: disagreements between judge and human raters must fall on adjacent checklist categories, not a systematic collapse onto one label; a systematic-collapse pattern blocks freezing even if aggregate κ clears 0.7. ⑤ Freeze (hash) the rubric and its prompt before any scale-up cell is scored.

---

## Assumptions (A1..A6)

| ID | Assumption (design rests on) | How it fails | How the design detects it |
|---|---|---|---|
| A1 | A separable, reliable ground-truth oracle for "violated post-compaction" exists (N1). | rubric judge disagrees with humans on soft `c`. | **G0** 200-case audit after the full R2 sequence above (categories grounded in `c`'s spec → held-out refinement → held-out validation → confusion-structure check → freeze): judge–human Cohen's κ ≥ 0.7, else demote soft constraints to secondary. |
| A2 | Break-through rate is (near-)monotone non-decreasing in `s`. | non-monotone cells break the logistic BT50. | Spearman `ρ(s,p̂)>0`, p<0.05; if >20% cells violate, switch to isotonic estimator (F-E1). |
| A3 | Log-budget is a fair commensurability scale across families. | ordering reverses under another scale. | **E4** re-fits under linear-budget and FLOP-equiv scales; reversal → report scale-conditional. |
| A4 | Warm-started/transferable suffixes do not materially understate attack strength (t6). | defenses look stronger than they are (BT50 biased up). | **E5** calibration: \|BT50_warm − BT50_full\| ≤ 0.1 on subset, else subtract measured offset. |
| A5 | The 5 variants faithfully instantiate documented real pinning mechanisms (t1). | boundaries are artifact-specific. | each variant mapped to a cited mechanism; reported per-variant; RQ_INF_3 cross-model stability. |
| A6 | Per-cell `N` makes the boundary identifiable above sampling noise (C5). | underpowered cells misplace the curve. | **G1** power gate: widen `N` until Wilson half-width ≤ 0.1 at the steepest grid point before fitting. |

**Global gates (must pass before any Hx is adjudicated).**
- **G0 (oracle):** judge–human κ ≥ 0.7 (guidance.md §3.4 R2's required minimum; corrected from an earlier draft's 0.6), reached only after the R2 sequence's confusion-structure check clears (step ④). *Fallback:* restrict primary claims to hard constraints; soft curves → exploratory appendix.
- **G1 (power):** per-cell `N` raised until Wilson half-width ≤ 0.1 at steepest cell. *Fallback:* compute-capped cells reported "boundary-unresolved," excluded from fits (no extrapolation).

---

## Step 6 — Pre-Registered Experiments

### RQ1 — Where is the failure boundary? (CO1; C1,C2,C3,C5; M1,M2,M3,M5)
- **Assumption:** A1, A2, A6.
- **Hypothesis H1 (binary):** For **≥4 of 5** variants (per model, per attack) the logistic fit has McFadden pseudo-R² ≥ 0.3 **AND** slope `β_1 > 0` at Holm-corrected p<0.05 **AND** BT50 bootstrap 95% CI width ≤ 0.25 of the strength range; predicted resistance order `d_slot > d_cksum > d_kcopy > d_reinj > d_0`.
- **Metric:** `p_{d,a,g}(s)` (Wilson CI); BT50, BT90 (bootstrap CI); AUBC `= ∫_0^1 p ds`.
- **Verification:** per-cell logistic regression; N≥20 (Stage 1) → N≥30 (Stage 2); Holm across 5 variants; power gate G1.
- **Fallback F1:** if the logistic R² bar fails for ≥2 variants, switch to isotonic regression + threshold-crossing BT50 (nonparametric). If a variant is **unbreakable-in-range** (`max_s p̂ < 0.05`), report it as the H1 falsifier — the stronger, more interesting headline: *"At least one pinning variant resists optimization injection within practical budget; we isolate the structural property (structural slot vs. checksum) that confers it."*

### RQ2 — What is the attack/defense cost ratio? (CO2; C4; M4)
- **Assumption:** A3, A4 (and RQ1's BT50 being defined).
- **Hypothesis H2 (binary):** Holm-corrected Wilcoxon signed-rank across tasks rejects R-equality for ≥1 variant pair (α=0.05) **AND** max/min variant `R ≥ θ_R = 2×` **AND** the by-R variant ranking is identical (Kendall τ = 1) across the two cost currencies.
- **Metric:** `R_{d,a,g}` at BT50 under currencies `φ ∈ {token-equivalent, API-dollar-class}`.
- **Verification:** bootstrap 95% CIs on R (10k resamples); paired Wilcoxon on `log R`; Kendall τ across currencies.
- **Fallback F2:** if the two currencies disagree on ranking → do not report a single ratio; report currency-conditional rankings side by side and record the reversal as the pre-registered RQ2 falsifier (t4). If no pair reaches `θ_R` → conclude *"pinning cost-effectiveness is uniform — mechanism choice does not robustly change adversarial cost"* (H2 refuted, reportable negative).

### RQ_INF_3 — Is the variant ranking model/attack-agnostic? (CO1; C2,C3; M1,M2,M4,M5)
- **Assumption:** A5 (and RQ1 BT50 defined per model×family).
- **Hypothesis H3 (binary):** mean pairwise Kendall's `τ ≥ τ* = 0.6` at permutation p<0.05 for BT50 orderings (and separately by R) across the ≥4 models and both attack families.
- **Metric:** mean pairwise Kendall's τ of variant orderings.
- **Verification:** τ with permutation p-value across all model pairs and both families (Stage 2).
- **Fallback F3:** if `0 < τ < 0.6` (p<0.05) → report "weak, partial transferability" with per-model tables; if `τ ≤ 0` → H3 refuted: *"best variant is model/attack-specific; no transferable ranking exists"* (reportable negative bounding CO1's external validity).

### Mandatory baselines

- **B0 — "why do this at all" control: no-defense variant under benign compaction (null attack).** Measures natural constraint attrition from compaction alone, zero adversary. If constraints already vanish at high rate benignly, the adversarial boundary is moot; if they survive benignly, the attack is doing the work. This justifies that pinning has a job and that break-through is adversarial (directly tests A5's premise and the phenomenon's existence). *Pre-committed read:* require benign-compaction break-through Wilson upper bound < 0.20 for the study to be meaningful.
- **B-alt — strongest-alternative-explanation control: budget-matched benign-filler injection.** **Rival explanation:** break-through is generic long-context / compaction-noise instruction degradation, not the optimized injection defeating pinning. Control replaces the attacker payload with benign filler of **identical token budget, count, and insertion position**, same number of compaction events. If break-through under benign filler is statistically indistinguishable from optimized injection at matched budget (overlapping Wilson CIs), the cause is context degradation, not the attack — this isolates the claimed adversarial cause from its strongest rival.

### Global fallback F-G1 (archetype pivot)
If the central hypothesis family fails (H1 finds no identifiable boundary for any variant **and** H2 finds no cost differentiation), pivot from *boundary-characterization* to a *defense-existence / robustness-audit* archetype. Pivoted abstract sentence: *"We show that under adversarial context compaction at least one pinning mechanism resists optimization injection within any practical attacker budget, and isolate the structural property responsible — turning the question from 'where the pin fails' into 'what makes a pin hold.'"*

---

## Step 9 — Walking Skeleton

**One binary question:** *does injection strength raise post-compaction break-through, and does the structural-slot variant resist more than no-defense, on a deterministic oracle?*

- **Arms (3):** `d_0` (no-defense control), `d_reinj` (verbatim re-injection), `d_slot` (structural protected-memory slot).
- **Attack:** black-box template-role forgery (ChatInject-style) only — no gradients, no white-box access.
- **Task set:** ~10 **hard, programmatically checkable** pinned constraints (forbidden tool call fired / numeric-format rule broken). No LLM-judge.
- **Model:** one open-weight 7–14B.
- **Sweep:** 3 strength levels × 3 arms × 10 tasks × 20 trials = **1,800 rollouts**.
- **Metric:** programmatic `V` only (deterministic); break-through rate with Wilson CI.
- **Expected cost/wall-clock:** ~1.8k rollouts × ~10 calls ≈ 1.8×10⁴ model calls; single GPU, **< 1 day**, ~$0 API.
- **Skeleton-passed criterion:** break-through rises with strength for `d_0` (Wilson CIs of low vs. high strength separate) **AND** `d_slot` break-through at max strength < `d_0` (CIs non-overlapping). If passed, **scaling is a config change, not a code change**: adding models, strength levels, tasks, trials is editing config lists; adding the gradient attack and the rubric judge are two pre-stubbed modules — the `(variant × strength × task × trial)` loop and oracle interface stay fixed.

---

## Claim–Evidence Map

| Claim the final abstract will make | Traces to | Status |
|---|---|---|
| Every pinning variant has a finite, findable failure boundary within practical strength (Claim2) | H1 / BT50 def (Step 5) | needs-experiment |
| …or at least one variant is unbreakable-within-budget | F1 (RQ1 falsifier) | fallback-covered |
| Attacker/defender cost ratio differs ≥2× across variants, robust to currency (Claim3) | H2 / R def (Step 5) | needs-experiment |
| …or cost-effectiveness is undifferentiated / currency-dependent | F2 (RQ2 falsifier) | fallback-covered |
| Variant robustness ranking is model/attack-agnostic (Claim4) | H3 / Kendall τ def (Step 5) | needs-experiment |
| …or ranking is model/attack-specific | F3 (RQ_INF_3 falsifier) | fallback-covered |
| Break-through is adversarial, not benign context attrition | B0 + B-alt controls | supported-by-design |
| Existing work covers ingredients but not this boundary/cost measurement (Claim5) | digest N3/N4 | supported-by-design |
| Reusable variant×strength protocol + two-tier oracle (CO3) | M1, M3 defs (Step 5) | supported-by-design |

---

## Abstract v0 (draft, mechanism-first — DRAFT BEFORE RESULTS)

A fixed-budget lossy compaction channel, replayed across a long agent session, forces every pinned constraint to re-win a retention competition at each event, while an adversary needs it to lose only once and can amortize an offline optimization budget to force that single loss. We measure where along an injection-strength axis each pinning defense loses, and price the loss against the defense. Sweeping a normalized injection-strength parameter across five pinning-style constraint-protection variants, two attack families (gradient-optimized suffixes; template-role forgery) and multiple models, we fit break-through-rate curves to locate each variant's failure boundary (strength at 50%/90% break-through) and cost-account attacker versus defender effort in a common currency to report the cost ratio at that boundary. Budget-matched benign-filler and no-defense controls isolate the adversarial cause from generic context degradation. The result maps exactly where, and how cheaply, memory-pinning fails under adversarial compaction. *(Draft; no experiments run.)*
