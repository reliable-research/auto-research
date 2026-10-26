# Why Tests Cannot See Design: A Structural Account of What Test Suites Fail to Express — Pre-Registered Paper Specification

> Generated from digest.md + README.md. Status: specification, no experiments run. All ids (C.., M.., CO.., RQ.., L.., t..) refer to digest.md.

## Step 0 — Core Asymmetry (升维)

**Asymmetry sentence.** A test verdict is (in practice, almost entirely) a function of a program's input/output behavior and is therefore near-constant on each functional-equivalence class — while design conventions (naming, layering/cross-cutting boundaries, event ordering) vary *within* those classes, so every behavior-preserving convention violation sits on the far side of an expressiveness boundary that adding more functional tests cannot cross.

This is not a tautology: real tests do leak structure-sensitivity (literal-identifier assertions, mock call-order verification, reflection), which is exactly why the boundary's location must be *measured*, not proved (cf. digest N8 metric "incidental-kill fraction").

**判据 (deletion test).** Delete the domain nouns: "A ___ verdict is a function of ___ and is therefore near-constant on each ___-equivalence class — while ___ vary within those classes, so every ___-preserving ___ sits beyond a boundary that adding more ___ cannot cross." The residue is an empty schema: it asserts nothing until you commit to (a) the empirical fact that *test suites specifically* are near-pure behavior-observers, and (b) the empirical fact that *naming/layering/temporal conventions specifically* are realizable behavior-preservingly. Both are contestable domain facts (tests could be heavily structure-coupled; conventions could be behavior-entangled), so the noun-free version is not a valid generic statement — the sentence is an asymmetry, not a bridge.

## Step 2 — Archetype

**Primary: empirical (measurement/characterization study)** — consistent with digest N12 (`value: "empirical"`). **Secondary: technical artifact** (the certified design-mutant corpus + dual-oracle pipeline, CO2).

Downstream consequences:
- (a) **Abstract contribution slot**: the per-category blind-spot *profile* (CO3) — which design-property classes systematically survive, by how much, versus the same suite's functional mutation score. Not "a new tool", not "a new benchmark".
- (b) **Intro logic**: "what becomes possible" — a mechanical, auditable answer to "can a green test suite gate a coding agent's change for design compliance?", replacing impressionistic claims that "tests miss design" with a measured boundary. Not "we beat prior kill rates".
- (c) **Evidence standard for Results**: pre-registered statistical contrasts (mixed-effects survival models across ≥12 systems, audited oracles, hard thresholds below), with negative/partial outcomes publishable via pre-committed fallbacks. No leaderboard numbers; effect sizes with CIs.

## Step 3 — Taste self-audit

- **Is the opportunity a Bridge?** Risk: "mutation testing meets architecture conformance — never connected before, we connect them" (the seed's own phrase "mutation testing 框架的又一处直接迁移" invites this). **FAIL as stated → fixed framing**: the opportunity is the *asymmetry of Step 0* — test verdicts are near-constant on behavior-equivalence classes; design conventions cut within them. Mutation is merely the *measuring instrument* for locating that boundary; the transfer is not the contribution, the measured boundary is. Idea skeleton changed accordingly: the paper's object is the boundary, not the pipeline.
- **Is the method mere Synthesis?** Risk: the pipeline composes existing tools (PIT/pitest, Checkstyle, ArchUnit, EvoSuite). **PASS after check**: the load-bearing novel object is the **design mutant** — certified functionally-equivalent AND certified convention-violating by two *mutually independent* oracles (M2+M3) — a variant no existing framework can even represent (L1: an all-pass matrix row; L7: outside the equivalent-mutant model). The admission rule, not the tool glue, carries the method.
- **Load-bearing verbs**: audit of the draft framing found "extend mutation-testing theory", "leverage existing checkers". **FAIL → replaced**: we *isolate* design conformance from functional behavior (dual-oracle admission), *measure* the suite's kill response, *formalize* the blind spot as a conditional-kill-probability gap, *gate* claims behind audited oracle precision.
- **Abstract-opening rule**: mechanism/asymmetry first; no "X is increasingly used… however… we introduce". Enforced in Abstract v0 below.

## Step 5 — Formal Problem Definition

**Estimand (guidance.md §3.4 R1).** The quantity: per-category Design-Mutant Survival Rate `DMSR_c` contrasted against the same suite's functional survival rate `FSR`, and the same contrast's response to a matched convention-neutral control and a capability-matched suite augmentation. Unit of analysis: one admitted design mutant `m`, nested in (category `c` × subject system). Reference population: mature open-source Java/Python systems shipping machine-readable convention configs (Checkstyle/ArchUnit/flake8/import-linter) with `FMS ≥ 0.40` (A1). Decision it feeds: whether "a green test suite certifies design compliance" is a licensed inference for gating coding-agent changes, per category and overall.

**Notation.** Program `P`; test suite `T` (unmodified, pre-existing); mutant `m` (a program variant of `P`); category `c ∈ {NAM (naming), LAY (layering/cross-cutting), TMP (temporal/ordering)}` (M1); rule set `R_P` = the project's shipped machine-readable conventions (Checkstyle/ArchUnit/trace rules, M3); differential corpus `X_diff` of `N_diff` inputs generated independently of `T` (M2).

- `K_T(m) ∈ {0,1}`: kill — 1 iff any test in `T` fails on `m` (temporal kill criterion extended per M4 to trace-order assertions).
- `EQ_B(m) = 1` iff `∀x ∈ X_diff: obs(P,x) = obs(m,x)` — **bounded functional equivalence** under budget `B = N_diff` (M2). Pre-registered budget: `N_diff ≥ 10,000` generated inputs per subject system, generator disjoint from `T` (EvoSuite/randoop/fuzzing).
- `V(m) ∈ {0,1}`: violation — 1 iff the M3 checker flags `m` against a rule in `R_P`.
- **Admitted design mutant set** `D_c = {m : op(m) ∈ c, EQ_B(m)=1, V(m)=1}`.
- **Matched neutral set** `N_c = {m : op(m) ∈ c, EQ_B(m)=1, V(m)=0}` (same operator families, matched locality; see B-alt).
- `DMSR_c = |{m ∈ D_c : K_T(m)=0}| / |D_c|` (per-category Design-Mutant Survival Rate, digest N8).
- `FMS` = functional mutation score of `T` under default PIT/mutmut operators; `FSR = 1 − FMS` (functional survival rate).
- `IKF_c` = incidental-kill fraction: killed `m ∈ D_c` whose failing assertion references a literal identifier/value rather than behavior (digest N8).

**Adjective → definition → measurement:**

| Load-bearing word (from Claims) | Formal definition | Measured by |
|---|---|---|
| "functionally equivalent" | `EQ_B(m)=1` at `N_diff ≥ 10,000`, budget reported | M2 differential runs; equivalence-mislabel audit on survivors (A3) |
| "design-violating" | `V(m)=1` with audited checker precision ≥ 0.90 | M3 + stratified human audit, n ≥ 300 (A4) |
| "blind spot" (category-level) | `DMSR_c ≥ 0.50` AND `DMSR_c − FSR ≥ 0.25` (pooled) | M5 profile vs B0 arm |
| "structural" (vs quantity-limited) | DMSR drop after capability-matched suite augmentation `< 0.10` absolute | RQ_INF_2 arm (E3) |
| "systematic" (cross-category structure) | category fixed effect significant; ordering gap ≥ 0.15 | E2 mixed-effects model |
| "mechanical evidence" | per-mutant `(EQ_B, V, K_T)` triple, fully scripted, no human in the verdict loop | released harness (M4), N11 plan |
| "incidental(ly caught)" | kill trace matches literal-identifier/value assertion pattern | `IKF_c` classifier + audit subsample |
| "non-local" | operator edits ≥ 2 modules or crosses a declared `R_P` boundary | static diff footprint of `op(m)` |

Deleted adjectives (no computable quantity, so banned from claims): "principled", "faithful", "realistic".

**Confound-removal one-liners (guidance.md §3.4 R3):** (i) `X_diff` generated independently of `T` (EvoSuite/randoop/fuzzing, never `T`'s own generator) removes the circularity confound of certifying equivalence using inputs the suite already exercises; (ii) the matched neutral set `N_c` (same operator family and locality footprint as `D_c`, differing only in `V(m)`) removes the generic-equivalent-mutant confound, isolating whether kill probability responds to violation status specifically rather than to equivalence/undecidability per se; (iii) the capability-matched augmentation gate (A6: added suite must raise `FMS` by ≥10 points) removes the weak-augmentation confound, so a null result in E3 cannot be attributed to an under-strength augmentation arm.

## Assumptions (A1..A6)

- **A1 (corpus)**: ≥ 12 mature open-source systems (Java + Python) exist that ship machine-readable convention configs (Checkstyle/ArchUnit; flake8/import-linter) *and* have suites with `FMS ≥ 0.40`. *Failure*: too few qualifying projects → underpowered E1/E2. *Detection*: project-mining pilot gate before any mutant generation; abort-to-pilot-scope if < 12 found (scale-up shrinks, claims scoped per t3).
- **A2 (yield)**: operators (M1) yield ≥ 150 admitted mutants per category per system after M2+M3 filtering. *Failure*: dual-oracle admission too strict, cells underpowered (t4). *Detection*: walking-skeleton yield metric (Step 9); if yield < 50% of candidates, operators are revised before scale-up, never after unblinding.
- **A3 (equivalence oracle)**: bounded equivalence `EQ_B` mislabels < 5% of admitted mutants (true behavioral differences missed by `X_diff`). *Failure*: survival biased upward (digest feasibility risk; t2). *Detection*: manual audit of 100 randomly sampled *surviving* mutants + restriction to structurally-guaranteed operator families (pure renames, verified-commutative swaps, call-multiset-preserving relocations). *Gate (added per guidance.md §3.2, was missing)*: if the audit finds mislabel rate ≥ 5% on any subject system, admitted design mutants for that system are re-filtered to the structurally-guaranteed operator subfamilies only and `DMSR` is recomputed; if the restricted subfamily still exceeds 5% mislabeling, that system's H1/H2 results are demoted to exploratory — the same treatment A4 applies to a failed checker-precision gate, so the two dual-oracle halves (equivalence, violation) are gated symmetrically.
- **A4 (violation oracle)**: M3 checker precision ≥ 0.90 against human audit (C1, C4). *Failure*: "blind spot" partly measures checker noise. *Detection (hardened to the full guidance.md §3.4 R2 sequence, was a single-rater precision number)*: (①) each category's checker rules are grounded in the project's own shipped, externally-documented convention source (Checkstyle/ArchUnit/import-linter config — not invented ad hoc); (②) rule thresholds are drafted wide and refined on a held-out calibration subsample (named merge/split/remove operations logged) before the audit sample is drawn; (③) validate against **two independent human raters** on the stratified sample (n ≥ 300 across categories), requiring **κ ≥ 0.7** in addition to the ≥ 0.90 precision figure; (④) inspect the confusion structure — disagreements must be adjacent-rule confusions, not a systematic collapse onto one category, else the rule set is too coarse; (⑤) freeze the checker (hash the rule set) before scale-up. *Gate*: if precision < 0.90 **or** κ < 0.7 **or** confusion is systematic (not adjacent-only) for a category, that category's results are demoted to exploratory.
- **A5 (determinism)**: suite verdicts are stable — 3× rerun agreement ≥ 98% per system. *Failure*: flaky kills corrupt `K_T`. *Detection*: walking-skeleton rerun check; flaky tests quarantined and reported.
- **A6 (augmentation arm)**: a discrimination-optimized generated test set (UTRL-style or EvoSuite) can be produced that raises `FMS` by ≥ 10 points on each subject — otherwise the RQ_INF_2 arm is not capability-matched and is invalid. *Failure*: E3 unrunnable as designed. *Detection*: augmentation pilot on skeleton system; pre-committed substitution: EvoSuite-generated suite replaces the LLM generator if the LLM arm misses the +10 FMS bar.

## Step 6 — Pre-Registered Experiments

Design constants (all pre-registered): pilot n=2 systems; scale-up n=12 systems × 3 categories; ≥ 150 admitted mutants/category/system (A2); `N_diff ≥ 10,000`; α = 0.05; Holm correction within each hypothesis family; mixed-effects logistic model `kill ~ mutant_type + category + (1|system)` as the primary inference engine (digest N8 analysis plan, hardened).

**Power statement (added per guidance.md §3.2/§3.4 R2, Part 6 item 9, was missing).** At the pre-registered minimum of 150 admitted mutants per category per system, a per-system two-proportion test (H1's per-system contrast) has power ≥ 0.90 at α = 0.05 to detect the pre-registered effect floor `DMSR_c − FSR ≥ 0.25`; this is the n=150 threshold's justification, not an arbitrary round number. **Thin-cell rule**: any (category × system) cell that ends below 150 admitted mutants after M2+M3 filtering (A2's yield risk) is pre-declared **INCONCLUSIVE** for that cell's contribution to H1/H2 — never scored as a null and never silently dropped from the denominator; INCONCLUSIVE cells are excluded from the "≥ 9 of 12 systems" vote in H1 and reported separately with the observed n and the shortfall reason.

### E1 — RQ1 (blind spot exists)
- **Assumption**: A1, A2, A3, A4, A5.
- **Hypothesis H1 (binary)**: pooled `DMSR ≥ 0.50` AND per-system `DMSR − FSR ≥ 0.25` in ≥ 9 of 12 systems AND the mutant-type effect (design vs functional) in the mixed-effects model is significant at α = 0.05. All three conjuncts required; else H1 fails.
- **Metric**: `DMSR_c` and `FSR` as defined in Step 5; pooled DMSR = admitted-mutant-weighted mean across categories/systems.
- **Verification**: two-proportion contrast per system (design survival vs functional survival), pooled via mixed-effects logistic model with system random intercept; report odds ratio with 95% CI; Holm across the 12 per-system tests.
- **Fallback FB1 (pre-committed wording)**: "Existing test suites kill behavior-preserving design violations at a rate statistically indistinguishable from functional mutants (ΔDMSR−FSR < 0.25, OR CI spanning 1); we report the first certified design-mutant corpus showing that test suites encode substantially more design intent — largely via incidental structural coupling (IKF = measured value) — than the design-blindness folklore assumes." (Negative result; feeds F-G1 if E2/E3 also fail.)

### E2 — RQ_INF_1 (category structure)
- **Assumption**: A1, A2, A4 (per-category gate).
- **Hypothesis H2 (binary)**: category fixed effect significant (likelihood-ratio test, α = 0.05) AND pooled `DMSR_TMP ≥ DMSR_NAM + 0.15` AND pooled `DMSR_LAY ≥ DMSR_NAM + 0.15` (pre-registered ordering from digest N8: temporal ≈ cross-cutting > naming). Holm correction across the two pairwise ordering contrasts.
- **Metric**: per-category `DMSR_c` with 95% CIs; `IKF_NAM` reported alongside (predicted mechanism for low naming survival).
- **Verification**: LRT on the category term of the mixed-effects model; pairwise contrasts on model estimates, Holm-corrected; effect sizes as absolute DMSR differences with bootstrap CIs (10,000 resamples, system-level blocks).
- **Fallback FB2 (pre-committed wording)**: "Survival is uniformly high (or uniformly low) across naming, layering, and temporal categories (category LRT p ≥ 0.05): test blindness to design is undifferentiated rather than structured by non-locality/temporality; the C2/C3 non-locality account is not supported and the blind spot is better modeled as a single behavior-equivalence effect."

### E3 — RQ_INF_2 (structural, not quantity-limited)
- **Assumption**: A5, A6 (validity gate: augmented suite must raise FMS by ≥ 10 points, else arm invalid and E3 reported as unexecutable-as-designed with the A6 substitution).
- **Hypothesis H3 (binary)**: for TMP and LAY, absolute DMSR reduction after augmentation `< 0.10` AND paired McNemar p ≥ 0.05 (i.e. no significant per-mutant kill change), on ≥ 4 subject systems. (NAM is exploratory in E3: a drop via literal assertions is predicted and does not count against H3.)
- **Metric**: `ΔDMSR_c = DMSR_c(T) − DMSR_c(T ∪ T_gen)` per category; McNemar discordant-pair counts.
- **Verification**: paired McNemar per category per system on per-mutant kill verdicts before/after augmentation; Holm across categories; augmentation capability check (ΔFMS ≥ +0.10) reported first as the arm-validity gate.
- **Fallback FB3 (pre-committed wording)**: "Discrimination-optimized functional tests significantly reduce non-local design-mutant survival (McNemar p < 0.05, ΔDMSR ≥ 0.10): the blind spot is a *quantity/strength* limit, not a structural expressiveness limit — design compliance can be partially bought with more functional tests, and we quantify the exchange rate (ΔDMSR per added test / per ΔFMS point)."

### Mandatory baselines

- **B0 — "why do this at all" control**: the **default functional mutation arm** — the identical unmodified suite run against default PIT/mutmut mutants on the same systems, yielding `FMS`/`FSR`. This is the no-mechanism arm: if suites also failed to kill ordinary functional mutants (`FMS < 0.40`), surviving design mutants would show only that the suite is weak, not that design is a *distinct* blind spot. B0 gates admission of every system (A1) and supplies the contrast term in H1.
- **B-alt — strongest-alternative-explanation control**: the **matched convention-neutral equivalent-mutant arm** `N_c` — same operator families, same locality footprint, `EQ_B = 1`, but `V = 0` (e.g. convention-*conforming* renames; order swaps that break no declared rule; relocations within a layer). **Rival explanation being isolated**: "design mutants survive merely because they are behavior-preserving — the equivalent-mutant effect — and any kills that do occur are incidental structural coupling, so the study measures behavior-preservation, not design-specific (in)visibility." Pre-registered check: `|P(K_T=1 | m ∈ D_c) − P(K_T=1 | m ∈ N_c)| < 0.05` per category supports the structural account (kill probability carries no information about violation status); a gap ≥ 0.05 with sign toward killing violators would show suites partially *do* sense conventions, quantified via `IKF_c` decomposition.

### Global fallback F-G1

If the central hypothesis family (H1 ∧ H2) fails — suites kill design mutants like functional ones, with no category structure — the archetype pivots from *empirical characterization of a blind spot* to *technical artifact / measurement instrument* (secondary archetype promoted). Pivoted abstract sentence, pre-committed: "We formalize and release the design-mutation score — a dual-oracle-certified adequacy criterion over behavior-preserving convention violations — and show, contrary to the folklore that tests cannot see design, that mature suites detect a measurable fraction of design violations through quantifiable structural coupling, giving the first calibrated instrument for design-conformance-aware gating of coding-agent changes."

## Step 9 — Walking Skeleton

**One binary question**: *Can the dual-oracle admission pipeline (M2+M3) produce certified design mutants at usable yield with deterministic kill verdicts on one real system?*

- **System**: 1 mature Java project shipping both a Checkstyle config and ArchUnit rules (candidate pool: Defects4J projects + ArchUnit's own example ecosystem; pick the first that meets FMS ≥ 0.40).
- **Arms (3)**: (1) NAM design mutants, 30 candidates → target ≥ 15 admitted; (2) B0 functional PIT default run; (3) B-alt neutral mutants, 30 candidates → ≥ 15 admitted. (LAY/TMP operators, Python, and E3 augmentation are explicitly *excluded* from the skeleton.)
- **Deterministic metrics only**: admission yield (admitted/candidates), per-mutant `K_T` verdicts, 3× rerun agreement, FMS, wall-clock per mutant. No statistics, no CIs.
- **Expected cost**: ≤ 1 machine-day on a commodity multicore (≈ 60 mutant × suite runs + 1 PIT run + `N_diff`-scaled differential pass at reduced budget 1,000 inputs); zero GPU; ≤ $10 API if any LLM assist is used.
- **Pass criterion (explicit)**: yield ≥ 50% on both mutant arms AND rerun agreement ≥ 98% AND FMS ≥ 0.40 AND every admitted mutant carries a complete machine-readable `(EQ_B, V, K_T)` triple. **Skeleton passed ⇒ scaling is a config change**: adding systems, the LAY/TMP operator families, the Python ecosystem, and the E3 arm must require only entries in the project/operator config lists, not harness code changes — this property is itself checked by adding a second system via config-only diff before declaring the skeleton done.

## Claim–Evidence Map

| # | Abstract-level claim (from digest Claims) | Traces to | Status |
|---|---|---|---|
| 1 | Test suites structurally fail to express certain design-property classes; demonstrable mechanically via functionally-equivalent convention-violating mutants (Claim 1, CO1/CO2) | H1 + Step 5 defs of "functionally equivalent", "design-violating", "mechanical evidence" | needs-experiment (E1); fallback-covered (FB1) |
| 2 | Design-mutant survival exceeds functional-mutant survival and differs by category, non-local > naming (Claim 2, CO3) | H1, H2 | needs-experiment (E1, E2); fallback-covered (FB1, FB2) |
| 3 | The blind spot is structural, not quantity-limited: discrimination-optimized tests don't remove it (Claim 3) | H3 + Step 5 def of "structural" | needs-experiment (E3); fallback-covered (FB3) |
| 4 | Survival is design-specific, not a generic equivalent-mutant artifact | B-alt conditional-kill check + IKF decomposition | needs-experiment (B-alt arm) |
| 5 | The dual-oracle admission procedure yields auditable per-mutant evidence (CO2) | Step 5 defs + A3/A4 audit gates + skeleton pass criterion | supported-by-design (gated by A4 audit) |
| 6 | Adequacy theory extended from functional to design conformance (Claim 5) | Framing only; carried by claims 1–4 | supported-by-design (conditional on H1 or F-G1 pivot) |
| 7 | No numeric result exists yet (Claim 4) | This document's status line | supported-by-design |

## Abstract v0 (draft, mechanism-first)

> **[DRAFT — BEFORE RESULTS. No numbers below are real; brackets are pre-registered slots.]**
>
> A test verdict is near-constant on each functional-equivalence class of programs, yet design conventions — naming, layering, event ordering — vary within those classes: behavior-preserving convention violations are therefore candidates for a structural blind spot no added functional test can close. We formalize this boundary and measure it. A dual-oracle procedure isolates *design mutants* — certified functionally equivalent by differential execution independent of the suite, and certified convention-violating by rule checkers independent of both — then gates them through 12 mature open-source suites. We report per-category design-mutant survival against the same suites' functional mutation scores, a convention-neutral matched control separating design-blindness from the generic equivalent-mutant effect, and an augmentation arm testing whether discrimination-optimized generated tests shrink the gap ([DMSR], [ΔDMSR], [category ordering] to be filled). The result is a mechanical account of which design properties a green test suite cannot certify — the precondition for using tests to gate coding-agent changes.
