# Not All Data Degrades Equally: Domain-Selective Effects of Synthetic Contamination — Pre-Registered Paper Specification

> Generated from digest.md + README.md (topic B6.4). Status: specification, no experiments run.
> All ids (C1–C4, M1–M6, CO1–CO4, RQ1/RQ_INF_2/RQ_INF_3, Claims 1–6, t1–t5) refer to digest.md.

## Step 0 — Core Asymmetry (升维)

**The asymmetry**: *Damage per contaminated token is not a constant of the corpus but an increasing function of the training domain's correctness strictness: domains whose ground truth is mechanically verifiable (code executes, math answers check) convert subtly-wrong synthetic content into corrupted supervision signal, while style-tolerant domains (prose, dialogue) absorb the same synthetic dose as benign stylistic variation.*

This is an invariant claim about *where* harm concentrates, not the phenomenon ("synthetic data hurts") and not a bridge ("collapse work and mixture work were never crossed").

**判据 (deletion test)**: delete the domain nouns:
> "Damage per contaminated token is an increasing function of the ______'s ______ strictness: ______ whose ground truth is ______ convert wrong ______ into corrupted signal, while ______-tolerant ______ absorb the same dose as benign variation."

Without "domain", "correctness", "code/math executes/checks", "prose/dialogue" the sentence has no computable subject: there is no axis on which damage could increase, and "converts wrong X into corrupted signal" is unfalsifiable filler. It does **not** survive as a valid generic statement → not a bridge. (Contrast the FORBIDDEN bridge version: "collapse theory has no domain axis and mixture work assumes clean shards; we connect them" — that sentence survives noun deletion as a generic connect-A-and-B template.)

## Step 2 — Archetype

**Primary**: `empirical` (measurement/evidence paper), per digest N12 — the deliverable is a controlled measurement of a domain × ratio interaction and a replicated vulnerability ranking, matching the seed's gap-type label [证据].
**Secondary**: `methodological protocol` (CO3) — the token-accounted single-domain contamination protocol is reusable scaffolding, subordinate to the measurement.

Downstream consequences:
- **(a) Abstract contribution slot**: a measured interaction + a generator-replicated per-domain vulnerability ranking with uncertainty — NOT a new method, model, or benchmark.
- **(b) Intro logic**: "what becomes possible" — with a validated ranking, a fixed synthetic-data-filtering budget can be allocated to the fragile domains first (Claim 4 / CO4); the intro must not be framed as beating a number or proposing a mitigation.
- **(c) Evidence standard for Results**: pre-registered statistical criteria (mixed-model interaction test, bootstrap slope CIs, Kendall's τ replication) with all thresholds fixed here, before any run; a negative or null result under these criteria is a reportable outcome, not a failure.

## Step 3 — Taste self-audit

| Check | Verdict | Action |
|---|---|---|
| Is the opportunity a Bridge? | **Fails as drafted in digest N2-Item2** ("crossing the contamination axis with the domain axis is the natural but missing experiment" is bridge-shaped) | Fixed: the opportunity is the Step-0 asymmetry (correctness strictness governs damage-per-token). The two literatures appear only as evidence that neither can *express* the asymmetry (Claim 3), i.e. as related-work positioning, never as the contribution. |
| Is the method mere Synthesis? | Pass | The method is an isolation instrument (token-accounted single-domain replacement + degeneracy-matched control), not an assembly of existing components into a system. |
| Load-bearing verbs from integrate/unify/leverage family? | Pass after fix | Load-bearing verbs: **isolate** (single-domain replacement), **measure** (domain-matched deltas), **rank** (bootstrap slope ordering), **falsify** (cross-generator τ criterion). "Combine/cross the axes" is banned from claims. |
| Abstract-opening rule | Digest N0 draft abstract **violates** it ("Synthetic text ... is increasingly present ... Neither asks ... We run") | Rewritten in Abstract v0 below: opens with the mechanism/asymmetry, no "increasingly used… however… we introduce" template. |

## Step 5 — Formal Problem Definition

**Estimand** (guidance.md R1 — quantity, unit of analysis, reference population, decision it feeds, in one sentence): the per-domain degradation slope β_d (the marginal change in normalized capability delta Δ_d per unit increase in single-domain contamination ratio r) and the resulting cross-domain ordering of {β_d}, estimated separately for each of the four content domains (code, math, prose, dialogue); unit of analysis is one (domain, ratio, seed) continued-pretraining cell; reference population is single-domain-contaminated continued-pretraining runs in the ≤3B-parameter / ≤2.5B-token regime tested here; the estimand feeds a data-curation-budget allocation decision (which domain's synthetic-content filtering to fund first, Claim 4/CO4).

**Notation.** Base corpus `D = ⋃_{d∈𝔻} D_d`, `𝔻 = {code, math, prose, dialogue}` (shards per M1). Generator `G` (M2). Contamination operator `κ(D, d, r)`: replace exactly an `r` fraction of shard `D_d`'s tokens with `G`-synthetic in-domain documents, all other shards byte-identical (M3). Model `θ(d, r, s)`: continued-pretrain base θ₀ on `κ(D, d, r)` with seed `s`, fixed schedule. `S_d(·)`: domain-d primary metric of a checkpoint (M4). Degradation delta `Δ_d(r) = (S_d(θ(d,0)) − S_d(θ(d,r))) / S_d(θ(d,0))` (for perplexity/loss metrics, sign-flipped so larger Δ = more damage). Slope `β_d`: OLS coefficient of `Δ_d` on `r` over ratios × seeds (M5).

Every load-bearing adjective/verb in the Claims, made computable:

| Term (from Claims/N6) | Definition | Measured by |
|---|---|---|
| **controlled** (single-domain) | `κ` replaces, never adds: token count and mixture proportions identical across cells; non-target shards byte-identical (checksum) | M3 token accounting + shard checksums |
| **domain-selective** (Claim 1) | domain × ratio interaction term ≠ 0 in mixed model `Δ ~ domain × ratio + (1|seed)` | likelihood-ratio test, Holm-corrected α = 0.05 over 4 primary metrics |
| **vulnerable / fragile** (Claim 2) | larger `β_d` | OLS + 10,000-resample bootstrap 95% CI over seeds × eval items |
| **vulnerability ranking** (CO2) | descending order of `β_d` | pairwise slope-difference bootstrap CIs |
| **strict correctness structure** | decision procedure: domain has a deterministic mechanical verifier (unit-test execution; exact-match answer) → strict = {code, math}; graded/judged metric → tolerant = {prose, dialogue} | fixed by M4's metric types; binary attribute, assigned before any run |
| **stable / not a generator artifact** (Claim 5) | Kendall's τ between the two generators' rankings ≥ 0.66 (4 items: at most one adjacent transposition) | M6(a) replication |
| **attributable to syntheticness** (Claim 5) | `Δ_d^syn(r) − Δ_d^degen(r) > 0`, where the degeneracy arm matches the synthetic arm's measured repetition and type-token-ratio profile | M6(b) + M2 degeneracy logs |
| **directly guides filtering priority** (Claim 4) | curation rule: allocate filtering budget to domains in descending `β_d` order; well-defined iff the top-ranked pairwise CI excludes 0 | derived output of M5 |
| **damage / degrades** | `Δ_d(r) > 0` | M4 primary metrics + per-domain held-out validation loss (nats/token) as benchmark-independent co-primary DV |

Deleted adjectives (no computable definition, banned from claims): "silently corrupt", "catastrophic", "high-quality".

**Confound-removal (guidance.md R3 — every design constraint names its confound):**
- Token-accounted single-domain replacement, byte-identical non-target shards, fixed mixture proportions (M3) removes the confound *total-token-budget / global-diet shift*: without it, a measured Δ_d(r) could reflect a change in the overall training mixture rather than a domain-targeted effect.
- One shared clean-control model per seed, same optimizer/schedule across all cells (M3) removes the confound *run-to-run training variance*: without it, apparent domain differences could be seed/optimizer noise rather than a real domain × ratio interaction.
- Dual normalization — benchmark-Δ and validation-loss-Δ reported together (M4/M5, tests A6) removes the confound *benchmark-construct artifact*: without it, a domain could appear more "vulnerable" merely because its benchmark is more brittle (t1), not because it is more damaged.
- Degeneracy-matched real-text control arm (M6b, tests H5) removes the confound *generic surface degeneracy*: without it, damage attributed to "syntheticness" could really be repetition/low-entropy quality decay any low-quality text would cause (challenge C1).
- Cross-generator replication (M6a, tests H4) removes the confound *generator-idiosyncratic quality profile*: without it, a domain could look fragile only because this specific generator happens to write worse text in that domain (challenge C4).
- Global-uniform-contamination B0 arm (same total synthetic-token budget, spread across all shards) removes the confound *mere-presence-of-synthetic-data*: without it, a positive result could show only that any synthetic tokens hurt, not that WHERE they land matters.

## Assumptions (A1–A8)

- **A1 (clean baseline)**: the four public shards contain negligible pre-existing synthetic text. *Fails if* web-era sources (FineWeb-Edu, UltraChat is itself LLM-generated!) carry a synthetic base rate that compresses measurable deltas. *Detected by*: pre-run shard audit with an off-the-shelf synthetic-text classifier; report base rate per shard; **dialogue shard**: replace UltraChat with human-only OASST1 + a human-forum corpus if audit base rate > 20%. Gate: pilot.
- **A2 (in-domain generator)**: M2's synthetic documents are plausible in-domain members, not garbage. *Fails if* rejection sampling degenerates. *Detected by*: M2 logs (perplexity, TTR, MinHash dup-rate) + 50-doc/domain manual spot check in the walking skeleton. Gate: **PG-2**, walking skeleton (Step 9). Consequence: fails ⇒ M2 is re-prompted/swapped before the pilot proceeds; H1–H5 are all blocked (not merely degraded) until A2 passes, since a garbage generator invalidates every downstream contamination arm.
- **A3 (detectable regime)**: 1.1B-model / 0.5B-token continued pretraining sits in a regime where 100% shard contamination measurably moves domain metrics. *Fails if* effects are below seed noise (single biggest risk, digest N6 feasibility). *Detected by*: pilot gate **G-P1**: at r = 100%, ≥1 domain shows Δ ≥ 2× pooled seed SD on its primary metric; else stop and trigger F-G1.
- **A4 (above-floor metrics)**: clean-control benchmark scores exceed noise floor. *Fails if* e.g. 1.1B GSM8K ≈ 0. *Detected by*: floor gate: clean `S_d(0)` must exceed 3× its item-level bootstrap SE; pre-registered substitute if it does not: that domain's primary DV becomes held-out validation loss (already co-primary).
- **A5 (adequate power)**: 3 seeds/cell + item-level bootstrap detect the pilot-estimated effect size at α = 0.05. *Detected by*: Stage-1 power analysis before committing Stage-2 compute (t4 mitigation); if power < 0.8 for the interaction test, seeds are increased on extreme cells only, pre-registered here. Gate: Stage 1→Stage 2 transition. Consequence: if power remains < 0.8 after the seed increase (compute-bounded, extreme cells only), that domain's contribution to H1/H2/H3 is pre-declared **INCONCLUSIVE** (never scored as null, never silently dropped — guidance.md Part 4 situation 5) and excluded from the Holm-correction denominator for that metric; H1/H2/H3 are then scored on the remaining adequately-powered domains and the INCONCLUSIVE set is reported alongside every headline number (R8).
- **A6 (normalization-invariant ranking)**: the β_d ordering does not depend on choosing benchmark-Δ vs validation-loss-Δ (challenge C2). *Detected by*: dual-normalization report; disagreement in the top-ranked position → ranking reported as "inconclusive under normalization" (t1 mitigation), H2 fails. Gate: **Stage 2** (computable only once both benchmark-based and validation-loss-based Δ exist for every cell).
- **A7 (independent generators)**: the two Stage-2 generators differ in family and quality tier enough to count as replication (C4). *Detected by*: report per-domain generator perplexity/degeneracy profiles; profiles statistically indistinguishable → replication downgraded to "same-profile", H4 scope-limited. Gate: **Stage 2** (computed immediately after both generators' Stage-2 runs complete, before H4/H5 are scored).
- **A8 (dialogue judge validity)**: the frozen MT-Bench LLM-judge's single-turn 1–10 score tracks genuine dialogue-response quality rather than a self-preference or style artifact (guidance.md R2; Part 2 A2 reviewer-kill: "unvalidated LLM-judge"). *Fails if* the judge systematically prefers synthetic-styled phrasing independent of content quality (t5). *Detected by*: an **R2-lite validation** before the judge is used at scale — 100 dialogue-domain responses (spanning clean and contaminated arms) double-rated by 2 human raters on the same 1–10 rubric; require Cohen's κ ≥ 0.7 between the judge and the human-rater majority label, computed once and frozen before Stage 2. Gate: **PG-3**, walking skeleton extension (run once, before any dialogue judge score is used for H1–H3). Consequence: κ < 0.7 ⇒ the dialogue domain's primary DV is demoted to held-out validation loss only (already co-primary, per M4) and the judge score is reported descriptively but excluded from the Holm-corrected primary-metric set — dialogue is not dropped from the study, only from the judged-metric family.

## Step 6 — Pre-Registered Experiments

Design constants (from digest N6/N8, hardened): pilot = 4 domains × r ∈ {25, 100}% + shared clean control, 3 seeds, 27 runs, 1.1B model, 0.5B tokens; Stage 2 = full grid r ∈ {0,10,25,50,100}%, second generator, 3B-scale at r ∈ {0,100}%. Primary metrics per M4; co-primary DV = per-domain held-out validation loss. All tests: α = 0.05, Holm–Bonferroni over the 4 domain-matched primary metrics; bootstrap = 10,000 resamples over seeds × eval items.

### E1 — Domain-selectivity (RQ1; tests CO1; Claims 1, 3)
- **Assumption**: A1, A3, A4, A5, A8.
- **Hypothesis H1 (binary)**: the domain × ratio interaction LRT in `Δ ~ domain × ratio + (1|seed)` rejects at Holm-corrected p < 0.05, **and** ≥1 pairwise slope difference `β_d − β_d′` has a bootstrap 95% CI excluding 0 **and** a point estimate ≥ **effect_floor = 0.10** (i.e., the two domains differ by ≥10 percentage points of normalized capability delta at r = 100%, matching pilot gate G-P1's own detectability threshold of 2× pooled seed SD). All three conjuncts required (guidance.md §3.1: significance without a native-unit magnitude floor passes nothing).
- **Metric**: `Δ_d(r)` per Step 5; slopes `β_d`.
- **Verification**: linear mixed model per digest N8 analysis plan; LRT full vs no-interaction model; Holm over 4 primary metrics; pairwise contrasts via 10,000-resample bootstrap.
- **Fallback FB1** (pre-committed wording): "Within the tested regime (≤3B params, ≤2.5B tokens, ratios ≤100%), synthetic contamination behaves as a **domain-uniform capability tax**: we bound every cross-domain slope difference below δ* = [upper 95% CI], licensing a single global filtering threshold and simplifying the global-mixing-ratio abstraction of [MixRatio, OpenReview:9RdhTvYbX0] rather than complicating it."

### E2 — Directional ranking (RQ1; tests CO2; Claim 2)
- **Assumption**: A1, A3, A4, A6, A8.
- **Hypothesis H2 (binary)**: the pre-registered contrast `(β_code + β_math)/2 − (β_prose + β_dialogue)/2 > 0` with one-sided bootstrap 95% CI excluding 0 **and** a point estimate ≥ **effect_floor = 0.05** (the strict-domain average slope exceeds the tolerant-domain average slope by ≥5 percentage points of Δ per unit ratio), **and** the same sign (with the same floor) holds under the validation-loss normalization (A6).
- **Metric**: β_d under both normalizations.
- **Verification**: one-sided bootstrap test of the strict-vs-tolerant contrast; dual-normalization concordance check.
- **Fallback FB2**: "The correctness-strictness account is falsified in direction; we report the observed ranking [order] with CIs — any stable ranking, including the reverse, still yields the curation-priority rule of Claim 4, but the mechanism story is replaced by an open question about [top domain]'s fragility."

### E3 — Dose-response shape and scale stability (RQ_INF_2; tests CO1, CO3; Claim 6)
- **Assumption**: A3, A5, A8.
- **Hypothesis H3 (binary)**: (i) `β_d > 0` with 95% CI excluding 0 **and** `β_d ≥` **effect_floor = 0.05** (per-domain Δ per unit ratio) in ≥3 of 4 domains; (ii) per-domain quadratic term LRT decided at α = 0.05 (either outcome is informative; monotone non-decreasing Δ_d(r) required in every CI-significant domain, Spearman ρ ≥ 0); (iii) the 1.1B ranking and the 3B extreme-ratio ranking agree at Kendall's τ ≥ 0.66 (τ's own threshold is the floor for this conjunct).
- **Metric**: β_d, quadratic coefficient, cross-scale τ.
- **Aggregation**: H3 is scored PASS iff (i) **and** (iii) both hold — (i) establishes dose-response exists at a non-trivial floor, (iii) establishes it rank-transfers across scale; these are the two pass/fail gates. (ii) is reported descriptively for every domain regardless of its own outcome (either a linear or a threshold-shaped dose-response is informative) and determines which of FB3's sub-clauses is quoted, but does not itself gate H3 PASS/FAIL (guidance.md §3.1: binary means a reader with the results JSON and no context can return PASS/FAIL — this line resolves which of the three sub-parts are load-bearing for that verdict).
- **Verification**: per-domain OLS + LRT (linear vs quadratic), digest N8 plan; τ computed on the r = 100% orderings at both scales.
- **Fallback FB3**: "The vulnerability ranking is **scale-conditional**: it holds at 1.1B but reorders at 3B, so curation priorities derived from small-proxy contamination studies do not rank-transfer (a direct caveat to RegMix-style rank-invariance [RegMix, OpenReview:5BjQOUXq7i] under contamination)."

### E4 — Generator robustness (RQ_INF_3; tests CO2, CO3; Claim 5)
- **Assumption**: A2, A7, A8.
- **Hypothesis H4 (binary)**: Kendall's τ between the two generators' β-rankings ≥ 0.66 (at most one adjacent transposition among 4 domains).
- **Metric**: τ between generator-wise rankings (M6a).
- **Verification**: exact τ on 4 items; bootstrap CI on τ over seeds × items reported alongside.
- **Fallback FB4**: "Per-domain contamination vulnerability is **generator-conditional**: rankings from any single generator are unreliable, which itself invalidates single-generator contamination audits and makes cross-generator replication a mandatory protocol step (CO3 survives as the contribution)."

### E5 — Syntheticness beyond degeneracy (RQ_INF_3; tests CO3; Claim 5, challenge C1)
- **Assumption**: A2 (degeneracy logs must be trustworthy), A8 (if the top-ranked domain from E2 is dialogue).
- **Hypothesis H5 (binary)**: at r = 100%, `Δ_d^syn − Δ_d^degen > 0` with one-sided bootstrap p < 0.05 (Holm-corrected) **and** a point estimate ≥ **effect_floor = 0.03** (≥3 percentage points of normalized capability delta beyond the degeneracy-matched control) in ≥2 of 4 domains, **including** the top-ranked domain from E2.
- **Metric**: paired delta between synthetic arm and degeneracy-matched real-text arm (M6b), matched on M2's logged repetition + TTR profile.
- **Verification**: paired one-sided bootstrap per domain; Holm over 4 domains.
- **Fallback FB5**: "Contamination damage in this regime is explained by **surface degeneracy, not syntheticness**: cheap degeneracy detectors (repetition/TTR filters) recover the protection of expensive synthetic-text classifiers — a budget-relevant positive for curation practice."

### M7 — Mechanism analysis (guidance.md R6; explains *why*, not just *that*)

Beyond the headline slope ranking (E1/E2), one analysis is budgeted to test the Step-0 mechanism directly rather than resting on the aggregate outcome alone: a **verifiable-error audit** of the injected synthetic documents themselves. For code, run each synthetic document's associated unit tests (if authored) or a reference solution's tests where available, and record the fraction that is verifiably *incorrect* despite passing surface fluency; for mathematics, resolve each synthetic worked solution's final answer against a symbolic/numeric checker and record the fraction with a wrong answer; prose and dialogue have no analogous mechanical checker by construction (Step 5's "strict vs. tolerant" definition), so their audit is fixed at "not computable" rather than assumed zero. The mechanism prediction is: per-domain verifiable-error rate (where computable) correlates positively with β_d across seeds and ratios (Spearman ρ, reported descriptively, not gated to a PASS/FAIL threshold — this is explanatory evidence for *why* H1/H2 hold, not a substitute for them). A null or negative correlation would not overturn H1/H2 if they pass on their own pre-registered criteria, but would flag that the correctness-strictness *mechanism* story (Claim 2's causal account) is unsupported even if the *ranking* (Claim 2's descriptive claim) holds — the two are recorded as separable in `claim_map.md`.

### Mandatory baselines

- **B0 — "why do this at all" control: global-uniform contamination arm.** The same total synthetic-token budget as each (d, r) cell, spread proportionally over all four shards (digest N8 baseline 2). This is the no-mechanism arm: if concentrated single-domain injection produces per-domain damage statistically indistinguishable (bootstrap 95% CI of the difference includes 0 in all domains) from what the global synthetic ratio alone predicts, the domain axis adds nothing and the one-ratio abstraction of the collapse literature suffices — the problem does not exist. Run at the pilot stage (r-equivalent = 25% of one shard), 3 seeds.
- **B-alt — strongest-alternative-explanation control: degeneracy-matched real-text arm (M6b) + cross-generator arm (M6a).** The rival explanation IS: *"the observed ranking reflects the contamination generator's per-domain quality profile (it writes worse code than prose) plus generic surface degeneracy that any low-quality text carries — not any domain-intrinsic fragility to syntheticness."* Budget/capability matching: the degeneracy arm replaces exactly the same token count with **real** documents subsampled to match the synthetic text's measured repetition and type-token-ratio distribution; the second generator is a different family and quality tier at identical token budgets. E4 + E5 are the tests; the rival wins if H4 and H5 both fail.

### Global fallback F-G1

If the central hypothesis family fails (H1 false, or pilot gate G-P1 not passed): pivot the archetype from `empirical ranking` to `empirical bound + protocol artifact` (CO3 promoted to primary, CO2/CO4 dropped). Pivoted abstract sentence, pre-committed: *"Using a token-accounted single-domain contamination protocol with degeneracy-matched and cross-generator controls, we show that synthetic contamination up to 100% of any single domain shard acts as a domain-uniform capability tax at the 1–3B scale — bounding cross-domain vulnerability differences below δ* and licensing domain-agnostic filtering thresholds."*

## Step 9 — Walking Skeleton

**One binary question**: does 100% contamination of a single shard produce a measurable, domain-localized delta at all, through the full pipeline?

- **Arms (3)**: (1) clean control; (2) code@100%; (3) prose@100%. One seed each, 1.1B model, 0.5B-token continued pretraining, one generator.
- **Smallest task set / metrics (deterministic only — no LLM judge)**: HumanEval pass@1 (greedy, execution-based), LAMBADA last-word accuracy, and all four per-domain held-out validation losses. MT-Bench and GSM8K excluded from the skeleton.
- **Expected cost**: 3 training runs × 6–8 A100-h ≈ 20–25 A100-h, plus ~10 GPU-h synthetic generation and the A2 spot check; ≈1 day on a 4-GPU node.
- **Pass criterion (all four, binary)**: (i) shard checksums prove non-target shards byte-identical across arms (Step 5 "controlled"); (ii) M2 logs populated and 50-doc/domain spot check passes (A2); (iii) clean-arm HumanEval and LAMBADA above the A4 floor (score > 3× item-bootstrap SE); (iv) code-arm code-metric delta and prose-arm prose-metric delta each estimable with item-level bootstrap SE, and ≥1 of the two exceeds 2× its SE.
- **Skeleton passed ⇒** scaling to the pilot (27 runs) and Stage 2 changes only the config matrix (ratios, seeds, generator id, model size) — no code change. If (iv) fails at 100% contamination, A3 is dead on arrival: stop before the grid, report toward F-G1.

## Claim–Evidence Map

| Claim (digest) | Abstract will assert | Status | Traces to |
|---|---|---|---|
| Claim 1 | contamination harm is domain-selective | needs-experiment | H1 (E1); fallback FB1 |
| Claim 2 | strict-correctness domains (code, math) are more fragile | needs-experiment | H2 (E2) + Step-5 "strict" definition; fallback FB2 |
| Claim 3 | neither collapse theory nor mixture work can express the question | supported-by-design | N4 gap analysis over [MixRatio], [IterStability], [DoReMi], [RegMix]; positioning only, per Step 3 |
| Claim 4 | ranking directly guides filtering priority | fallback-covered | Step-5 priority-rule definition; well-defined iff H1∧(H2 or FB2-ranking); FB1/F-G1 give the domain-agnostic policy otherwise |
| Claim 5 | ranking is not a generator artifact; damage partly attributable to syntheticness | needs-experiment | H4 (E4), H5 (E5); fallbacks FB4, FB5 |
| Claim 6 | claims limited to the tested regime; rank-stability across scale checked | supported-by-design + needs-experiment | scope statement + H3(iii) (E3); fallback FB3 |

Every abstract-bearing claim maps to an H-id or a Step-5 definition; no claim rests on unmeasured adjectives.

## Abstract v0 (draft, mechanism-first — DRAFT BEFORE RESULTS; numbers are pre-registered criteria, not findings)

> Damage from synthetic training text may not be a property of the corpus but of the domain it lands in: domains with mechanically verifiable correctness (code, mathematics) can convert subtly wrong synthetic content into corrupted supervision, while style-tolerant domains (prose, dialogue) absorb the same dose as benign variation. We isolate this asymmetry with a token-accounted protocol that replaces a swept fraction of exactly one domain shard of a continued-pretraining corpus with in-domain synthetic text, holding token counts, mixture proportions, and training schedule fixed, and measure domain-matched capability deltas against a shared clean control. Domain-selectivity is decided by a pre-registered mixed-model interaction test; the resulting vulnerability ranking must survive a cross-generator replication (Kendall's τ ≥ 0.66) and a degeneracy-matched real-text control before we treat it as intrinsic. The ranking fixes where a finite synthetic-data-filtering budget protects the most capability.

(139 words. Opens on mechanism/asymmetry; verbs: isolate, measure, decide, survive, fix; no "increasingly used… however… we introduce".)
