# Design Review (adversarial, 2026-07-04)

> Reviewer stance: skeptical senior PC member. The recorded "Phase A (re-run) PASS" in
> `stage_review.md` was NOT trusted; every item relied on below was re-verified against file
> contents on disk. Files reviewed: `README.md`, `digest.md`, `paper.md`,
> `discussion/reference_candidates.jsonl` (159 records re-parsed), `discussion/stage_review.md`,
> `discussion/pipeline.md`, `discussion/paper_draft.md` (+ `.tex`/`.pdf` noted),
> `discussion/taste_audit.md`, plus `topics/goal.md` and `topics/guidance.md`.
>
> Staleness note (stated once, per instructions): `paper_draft.md`/`.tex`/`.pdf` (mtime
> 13:37–13:40) predate the Phase-A fixes applied to `paper.md` (mtime 19:09) — the draft
> contains none of the estimand, Aggregation lines, A8/PG-4, or per-layer power statement.
> This is expected staleness and is not re-penalized below, but the *content divergence*
> between the two registrations is (Finding 3).

## Verdict summary

| Dimension | Score | One-line reason |
|---|---|---|
| 1. Feasibility & scale | FIXABLE | Datasets real (ALFWorld, GAIA, Who&When) and costs estimated (<$200 pilot, ~$1–3k scale), but the replayable natural-failure slice is largely imaginary, cached-web GAIA replay is underestimated, and the walking skeleton omits the group-testing primitive it later claims scales "config-not-code". |
| 2. Soundness | FIXABLE (borderline BROKEN on B0) | Estimand, R2 plan (A8), paired tests, Holm correction all present — but the designated B0 is *not* null-by-construction, and the injected-fault corpus makes the headline monotonicity invariant near-true by construction. |
| 3. Novelty & pre-emption | FIXABLE | Differentiation from AgenTracer/DoVer/Who&When is a genuinely different estimand (budget-accuracy curve, not attribution accuracy), but the harvest never ran topic-targeted arXiv angles and the load-bearing method-twins have no digests, so pre-emption is not confidently excluded. |
| 4. Hypothesis→fallback robustness | FIXABLE | All four H* are binary with effect floors and verbatim fallbacks + a real pivoted abstract (F-G1), but fallback triggers don't cover the full negation of each H*, H3's conjunctive criterion is unreachable at its own stated power, and F1/F-G1 both depend on violation-rate variance the corpus is engineered to suppress. |
| 5. Method scope & RQ design | FIXABLE | Validity envelope stated and most A2 reviewer-kills pre-empted, but the A2-mandatory placebo arm is missing in its true form, M5d (the strongest practical rival) is wired into no hypothesis, and length-scaling of the Θ(log n / n) claim has no RQ. |
| 6. Prior-work reliability | PARTIALLY RELIABLE | Cache paths and OpenReview ids all resolve as claimed and rejections are honest, but Phase A items 2, 4, 5 were declared PASS in states that do not actually satisfy goal.md §3's own wording. |

**Overall: NEEDS-REVISION** (see end for the 3 highest-leverage fixes).

---

## Findings (ranked most-severe first)

### F1. [BROKEN] B0 is not null-by-construction; Phase D step 1 will either misfire or be vacuous

`paper.md` "Mandatory baselines": *"**B0 'why do this at all' control** — **zero-replay log-only LLM judge** (Who&When all-at-once + step-by-step, M5c). ... Its (expected) budget-independent accuracy floor is what makes the problem worth posing."*

guidance.md §3.3 gives B0 **two** jobs: (a) the current-practice arm, and (b) *"a null-by-construction placebo (shuffle labels/years/assignments) whose effect must be null. **Non-null placebo = the pipeline measures an artifact = the whole run is invalid.**"* The zero-replay judge satisfies (a) only. It is **not** null by construction: Who&When's own results (cited in digest N4 L1) show log-only judging is *weak, not at chance* — it will land measurably above chance. Now walk goal.md §5 step 1: *"Placebo first. B0 non-null → run invalid; ... stop."* Applied literally, an above-chance judge invalidates every run forever; applied charitably (nobody applies it), the run has **no artifact detector at all**. Think about what a real placebo would catch here: if M2's programmatic corruption leaves a conspicuous textual artifact at step d, a judge — or even the replay pipeline via verifier quirks — can "localize" the injection artifact rather than a decisive failure. No arm in the design would reveal this.

**Fix:** split B0 into B0a (judge = current-practice arm, expected weak-but-nonzero; premise-collapse routes to F-G1 per §3.3 job (a)) and B0b, a genuine null arm — e.g. (i) sham-injection trajectories: apply the same textual perturbation machinery at a step whose corruption does *not* flip the outcome (round-trip verified), where every localizer's "decisive step" prediction must be at chance; and/or (ii) run the full strategy suite on *successful* trajectories where no d exists. Pre-commit "B0b at chance" as the run-validity gate that Phase D step 1 actually checks.

### F2. [BROKEN] The injected-fault corpus makes the headline invariant (near-monotone g(k)) close to true *by construction*, and the one slice where it can genuinely break is probably not replayable

The asymmetry statement (Step 0) and Claim 1 rest on measuring where state-inheritance monotonicity holds vs. breaks (A3, C2: *"the sharpest risk (non-monotone recovery) is measured, not solved"*). But consider the mechanics of M2: faults are **exogenous** perturbations injected into one step of a *successful* trajectory (*"perturb one step of a successful trajectory ... keep the trajectory only if the perturbed run fails and a replay from the injected step with the original action succeeds"*). For k ≤ d, `replay(k, seed)` re-samples steps k..n fresh — the injected corruption is not regenerated, because the *policy never produced it in the first place*; the trajectory was selected to succeed under the policy. So g(k)=1 for k≤d up to baseline task-failure noise, and g(k)=0 for k>d exactly (corrupted state inherited). Natural failures are the opposite regime: the model's own propensity produced the mistake, so a fresh re-sample at k ≤ d frequently *regenerates* the same mistake — that is where non-monotonicity and "recovery" genuinely live. The M2 keep-filter (*"replay from the injected step with the original action succeeds"*) additionally *selects for* monotone-profile trajectories. Net effect: the monotonicity-violation rate — the paper's load-bearing mechanism covariate, F1's regressor, and F-G1's pivot deliverable — is measured on a corpus engineered to suppress it.

The designed escape hatch is the natural-failure slice (A6), but see F5: Who&When logs re-hosted "where re-executable" will mostly not be re-executable, so replay-based strategies (and hence violation-rate measurement) cannot run on exactly the slice where the invariant is at risk. The claims survive as *injected-corpus* claims (A4 correctly restricts licensing), but then Claim 1 / Claim 7 ("the risk is measured") are close to tautological.

**Fix:** add a fault mode the policy *can* regenerate — e.g. propensity-sampled faults: at step d, sample the policy at high temperature until it emits a genuinely wrong action, and inject *that* (the model's own error mode), so replay from k ≤ d has a realistic chance of re-committing it; report the violation rate separately per fault mode. Alternatively, pre-commit in `paper.md` that Claim 1/Claim 7 are licensed only as "for exogenous single-step faults" and delete the "sharpest risk is measured" framing from the abstract.

### F3. [FIXABLE] Two divergent pre-registrations coexist: paper.md's 4 H* vs. pipeline/paper_draft's 7 RQs with materially different criteria

`paper.md` Step 6 registers H1–H4 (RQ1, RQ_INF_1..3). `pipeline.md` Stage 6 + `paper_draft.md` register **seven** RQs (`rq_position_dependent_savings` ... `rq_structure_vs_uniform_and_judge`) with their own falsification conditions — and at least one materially disagrees with the spec: draft RQ2 scopes the 90%/25% claim *"on trajectories whose empirical g(k) profile is monotone"*, while paper.md H1 scores it on the **pooled** n=300 corpus with a ≥3-of-4 strata rule and *no* monotone-subset restriction. `rq_position_dependent_savings` (late-decisive-step quartile effect) exists in no paper.md hypothesis at all. goal.md Phase C requires *"one results file per RQ"* and Phase D scores *"each H\* against its exact pre-registered binary criterion"* — at execution time a weaker model has two conflicting answer keys, which is exactly the ambiguity pre-registration exists to remove (and a spin opportunity: pick whichever registration passed).

**Fix:** declare `paper.md` Step 6 the sole registration of record in both `pipeline.md` and the draft; either promote the two extra draft hypotheses (position-quartile effect; monotonicity-predictor stratification) into paper.md as H5/H6 with full seven-slot templates, or demote them to descriptive analyses. Regenerate `paper_draft.*` after (it is stale anyway).

### F4. [FIXABLE] Fallback triggers do not cover the negation of their hypotheses — a mid-zone failure leaves no pre-committed sentence

guidance.md §3.1: the fallback is *"the pre-committed VERBATIM sentence used if H<k> fails"* — i.e., it must fire on **any** FAIL. But paper.md writes conditional triggers narrower than ¬H:

- H1 fails iff NOT(≥90% accuracy at ≤25% cost); its fallback fires *"IF H1 fails (structured needs ≥50% of exhaustive budget to come within 5 pts...)"*. A result of 90% accuracy at 35% cost fails H1 but does not meet the stated trigger. What sentence gets spliced? Undefined.
- H2's fallback text — *"index structure yields no advantage over uniform replay"* — is written for the extreme case. If structured beats uniform by a significant 8 pts (< the 15-pt floor), H2 FAILs but the fallback sentence is *factually false* as written. The pre-committed wording would then misreport the result, and Phase E is forbidden from re-deciding.
- H4 is a conjunction (r=3 stabilization AND crossover exists) with fallbacks only for "insensitive to r" and "no crossover" — the mixed outcome (crossover exists, but r=3 does *not* stabilize) has no combination rule, violating §3.1's *"write the fallback-combination rules too."*

**Fix:** restate each F\* as the sentence used on *any* FAIL, with bracketed variants for the pre-enumerated sub-cases (floor-missed-but-direction-held / no-effect / wrong-direction), and add the H4 partial-conjunct rule. This is a wording exercise, an afternoon of work, and it is precisely what saves the paper at Phase D.

### F5. [FIXABLE] The natural-failure slice is presented as available but is mostly not constructible as specified

digest N6/N8 and paper.md A6/A8 lean on *"a natural-failure evaluation slice on human-annotated Who&When logs (re-hosted in the replay harness where re-executable)"*. Who&When's logs come from third-party multi-agent scaffolds (live-web GAIA-style tasks); re-executing an arbitrary logged trajectory suffix requires reconstructing that scaffold, its tool endpoints, and its environment state at every step boundary — none of which the logs contain. The honest expectation is that the *replay-based* strategies (bisection, group testing, uniform, exhaustive) can run on few or none of these logs; only the zero-replay judge runs everywhere. Additionally M4's group intervention (*"replace all steps of a group with recorded-correct actions where available"*) has no recorded-correct actions on natural failures at all. Yet H3/RQ_INF_2's fallback machinery, A6's paired-slice comparison, and A8's PG-4 (κ ≥ 0.7 relabeling gate) all presume the slice exists in usable, replayable form. The budget also never itemizes the re-hosting engineering (the feasibility section budgets 20–30 annotator-hours, zero engineering-days).

**Fix:** pre-commit the degraded form now: "the natural slice supports zero-replay judging and layer-label transfer only; replay-based strategies are evaluated on injected faults only" — and rewrite A6's consequence and Claim 8 accordingly. If a replayable natural slice is truly wanted, name a concrete source that is replayable (e.g. natural failures harvested *within this paper's own harness* on ALFWorld/cached-GAIA runs — the harness makes its own failures replayable by construction; this is the cheap, defensible version).

### F6. [FIXABLE] H3's conjunctive PASS is nearly unreachable at its own stated power — a pre-registered own-goal

paper.md RQ_INF_2: PASS requires the ≥10-pt structured advantage *"in **all 3 of 3** layers"*, with stated per-layer power of *"~65–70% ... at α=0.017"*. Even if H3 is true in every layer, P(all three per-layer tests clear) ≈ 0.65–0.70³ ≈ **0.27–0.34**. The INCONCLUSIVE-not-FAIL rule protects against wrongly declaring FAIL, but the design still buys a hypothesis whose most likely outcome under its own truth is "not confirmed" — wasted confirmatory budget. guidance.md Part 4 situation 5 offers the honest options; none was taken.

**Fix:** either (a) power the layers properly (raise per-layer n above ~150, shrinking another pre-declared axis per situation 10), or (b) re-register H3 as "pooled layer-interaction effect + descriptive per-layer margins", or (c) lower the conjunctive bar to 2-of-3 adequately-powered layers with the third reported descriptively. Choose now, not at verdict time.

### F7. [FIXABLE] H4's noise regime is likely empty in the environments chosen — and PG-2 pushes it emptier

H4 requires *"a single-replay flip rate p ≥ 15% above which group testing's accuracy-per-replay-unit exceeds vote-multiplied bisection's"*, with the CI required to *"exclude 'no crossover'."* But the environments were selected precisely to minimize stochasticity (A2: ALFWorld deterministic simulator, GAIA with cached web, all prefix tool calls cache-served, ≥95% reproduction gate). Where is the population of trajectories with p ≥ 15% supposed to come from? The design manipulates temperature (0.7) but never registers a mechanism guaranteeing support across the p-axis; if observed p concentrates near 0 (likely on ALFWorld), the crossover is not *false* but *untestable*, and neither fallback branch ("oracle near-deterministic" / "no crossover") cleanly matches "insufficient support on the p-axis to locate a crossover." Also note H4's verification block is the only one with **no stated α or multiplicity handling** (*"paired accuracy comparison across r (Wilcoxon); locate crossover with bootstrap CI"*) — the seven-slot check in stage_review item 5 passed this without the alpha slot actually being filled.

**Fix:** register a temperature/noise *sweep* as the p-manipulation (e.g. τ ∈ {0.3, 0.7, 1.0} on a subset), pre-declare "insufficient p-support" as a third, INCONCLUSIVE-style outcome for the crossover conjunct, and add α + correction to H4's verification.

### F8. [FIXABLE] The walking skeleton violates its own config-not-code gate for group testing — and B0 is not in the skeleton

paper.md Step 9: arms are *"bisection ..., uniform sampling ..., exhaustive scan ... No group testing, no judge"*, yet the scale-up criterion claims *"adding ... the group-testing arm ... is data-config expansion of the **same** `replay(k, seed)` loop"*. It is not: M4's group test is a *different oracle primitive* — *"test groups via multi-step interventions (replace all steps of a group with recorded-correct actions ..., else re-sample)"* — never exercised by the skeleton. Per guidance.md situation 8, needing new code at scale-up means the skeleton failed. Same for M5c/M5d (judge, hypothesis-then-verify): new code paths. And since B0 (however F1 resolves it) anchors run validity, a skeleton that never runs it validates nothing about the placebo path.

**Fix:** add one minimal group-testing arm (even 2 groups, contiguous) and one B0 arm to the 20-trajectory skeleton; the cost delta is small against the stated <$200 envelope.

### F9. [FIXABLE] The strongest *practical* rival (M5d, LLM-hypothesis-then-verify) is in the arm list but wired into no hypothesis or fallback

B-alt (budget-matched uniform) correctly isolates *index structure* — good, and its confound one-liner is explicit. But the rival a practitioner-facing reviewer will raise is different: "an LLM prior over *where* the fault is, plus a couple of verification replays (DoVer-style), beats blind bisection at small budgets — so your provisioning curve (CO4) recommends the wrong strategy." M5d exists in digest N6 and pipeline Stage 6's baseline list, but **no H\***, no fallback, and no claim references it; paper.md's Step 6 never mentions M5d. If M5d dominates at B ≤ 8, H1/H2 can both PASS while the paper's practical recommendation is wrong — an outcome the pre-registration cannot even express.

**Fix:** either register a descriptive-but-mandatory comparison ("M5d's curve is reported on the same grid; if it dominates any structured strategy at any pre-registered budget, CO4's guidance text switches to the pre-committed hybrid wording ...") or drop M5d from every list so the paper doesn't advertise an arm it never scores.

### F10. [FIXABLE] Reference cache: load-bearing method-twins have no digests, and the harvest never ran topic-targeted angles

goal.md §3 item 2 requires *"load-bearing entries have resolvable `digest_path`"*; §1 requires digesting *"every potentially load-bearing candidate (`baseline`/`method-twin`/`contrast`)"*. Verified on disk: all 9 grounding records (WhoWhen2025, AgenTracer2025, DoVer2025, InT2025, TRIM2025, AttnRL2025, iStar2025, BAILD2025, ZellerHildebrandt2002) have `"pdf_path": null, "digest_path": null, "verified": {"id_resolves": false}` — the two `method-twin`s included. stage_review.md item 2 records this honestly (*"recorded honestly rather than papered over"*) and then declares Phase A **PASS** anyway; the gate as written is not met. Separately, the 150-record harvest was "110 arXiv recent-listing + 40 ACL-2023" — a generic pool; the targeted angles (per goal.md §1 ①: "failure attribution", "trajectory replay", "delta debugging agents", "budget-bounded localization") were only ever run against the *local OpenReview corpus* (digest N3 preamble), never against arXiv at large. Note that Who&When and AgenTracer both have public arXiv versions that would supply real PDFs and digests. Pre-emption (guidance situation 12) is therefore *probable-clear but unverified* for the last ~12 months of arXiv.

**Fix:** pull the arXiv PDFs for the three load-bearing works (Who&When, AgenTracer, DoVer minimum), digest them, fill `digest_path`; run one targeted arXiv sweep on the method-name angles before Phase B.

### F11. [NOTE] Phase E/F/I artifacts exist before Phase B — a phase-contract violation, mitigated but real

`paper_draft.md`/`.tex`/`.pdf` occupy goal.md's Phase E/F/I output slots, yet Phases B–D never ran (`pipeline.md`: "B ... not attempted"). The draft is honestly labeled (*"no experiments have been run. All numbers below are pre-registered design targets"*), so this is not claim-fabrication — but it front-loads exactly the "stale claim after verdict" risk goal.md §8 warns about: after real results, every sentence of this pre-baked prose is a spin temptation. Combined with F3 (the draft carries its own divergent RQ set), the draft should be treated as a discussion-loop artifact, not a Phase E product.

### F12. [NOTE] Claim 1 is labeled "supported-by-design" but is an empirical claim

Claim–Evidence Map row 1: *"Suffix-replay outcome is (near-)monotone ... — supported-by-design (verified via monotonicity-violation rate)"*. A claim verified by a measured rate is needs-experiment, not supported-by-design; if the violation rate comes out high, no H-id fails and no fallback fires for it — a soft claim–evidence orphan that Phase A item 4 passed. Cheap fix: give Claim 1 a numeric floor (e.g. "violation rate ≤ X% on injected corpus") tied to A3's consequence, or route it explicitly to F-G1.

---

## Failure-space simulation (per-H walk-through)

**H1 fails, extreme form** (structured needs ≥50% budget for within-5-pts): F1 fires — *"we localize the trajectory property (monotonicity-violation rate) that predicts the achievable saving."* Would the fallback paper survive review? **Only if the violation rate has variance.** Per F2, the injected corpus suppresses violations by construction; if H1 fails while violation rates sit uniformly near zero (failure caused by oracle noise or verifier flakiness instead), F1's regression has no signal and the fallback paper is empty. Uncovered corner.

**H1 fails, mid-zone** (e.g. 90% accuracy at 35% cost): no pre-committed sentence exists (F4). Uncovered.

**H2 fails, uniform matches structured**: fallback text works; combined with H1 failing → F-G1 fires, pivoted abstract exists and is genuinely written (good — this is the strongest part of the machinery). But F-G1's deliverable ("a predictor from trajectory features ... for whether budget-bounded structured replay will succeed") inherits F2's problem: predictor features need variance. F-G1 survives review only if the corpus produces heterogeneous profiles.

**H2 fails, judge ≥ structured (wrong direction)**: covered by the bracketed fallback ("replay yields no advantage over log-only judging") and would honestly be the most interesting outcome (situation 4); routing exists. Covered.

**H3 fails on one powered layer**: fallback ("layer-dependent applicability") fires; fine. **H3 true everywhere but per-layer power ~0.65**: most likely outcome is 1+ layers INCONCLUSIVE → H3 neither PASS nor FAIL → which sentence? The spec never says what splices when a conjunct is INCONCLUSIVE (F6). Uncovered.

**H4, mixed conjuncts** (crossover exists, r=3 doesn't stabilize): no combination rule (F4). **H4, empty p-support** (all observed flip rates < 15% because the environments were chosen for determinism): neither fallback branch matches (F7). Uncovered.

**All-fail**: H1+H2 → F-G1 (covered, with the F2 caveat); H3, H4 fallbacks are self-contained scoping claims (covered). **PG-2 fails on GAIA only**: strata rule "≥3 of 4" becomes arithmetic nonsense with 2 strata; no pre-committed rule for losing an environment (situation 10 covers grid-shrink generally, but the aggregation clauses hard-code 4 strata). Uncovered.

**Is there any outcome that leaves the paper with nothing?** Yes, one compound but plausible one: H1/H2 fail **and** the injected corpus shows uniformly monotone profiles **and** the natural slice proves non-replayable (F5). Then F1's regressor is flat, F-G1's predictor has no features that vary, and the natural slice can't rescue external validity. The paper's floor in that world is "structured replay fails on a corpus where its enabling invariant holds" — a genuinely confusing negative that the current pivot text cannot express. Fixing F2 (propensity faults → guaranteed violation-rate variance) closes this hole, which is why it is fix #2 below.

## Missing RQs / reviewer questions the design cannot currently answer

1. **Length scaling.** The abstract's Θ(log n / n) framing is a *scaling* claim, but n ∈ [20, 60] and length is only "a covariate to expose scaling trends" (t3) — no RQ, no test. A reviewer will ask for at least a long-trajectory stratum (n ≥ 100) or a demoted claim.
2. **Does an informed prior beat blind structure?** (F9 — M5d unwired.) The provisioning decision (CO4) is between *strategies*, and the strategy practitioners would actually try first is judge-then-verify.
3. **Injection-artifact detectability.** Can the zero-replay judge find *injected* faults more easily than natural ones because the corruption is textually conspicuous? Without B0b (F1) this confound is unmeasured, and it inflates the judge-vs-replay gap in either direction.
4. **Harness overhead accounting.** Replay units count resumed LLM calls but checkpointing itself (state snapshots per step boundary, cache infrastructure) has cost; a tool-flavored reviewer (the secondary archetype is declared "technical-artifact") will ask for the A6-style user-cost accounting guidance.md demands of artifacts.
5. **Multi-fault / diffuse failures.** A4 scopes them out of the headline honestly, but the paper has no experiment shape at all for "two injected faults" — even a 20-trajectory descriptive probe would pre-empt the obvious "single-culprit is an idealization" review (DoVer's own motivation, quoted in the digest, makes exactly this attack).
6. **Verifier reliability.** g(k) is only as good as "the task's own verifier"; a flaky GAIA verifier masquerades as oracle noise (inflating p, contaminating H4). No A\* covers verifier error separately from replay stochasticity.

## Reliability audit of prior Phase A PASS

Independently re-verified (items 2, 4, 5, 6 of goal.md §3, plus reference spot-checks):

**What held:**
- Item 1 (digest self-verification): re-walked the cross-node ids — N4 L1–L7 ↔ N3 keys, N6 args ⊆ {C1..C4}/{M1..M6}, N8 mappings, N9 rq_ids — all resolve as recorded. All nodes N0–N12 + Claims present; absence_comments present on N0/N1/N10/N11. **Genuine PASS.**
- Item 3 (tag discipline): spot-checked N2/N6/N9 — tags present, N9 uniformly `evidence_strength="missing"`. **Genuine PASS.**
- Reference records: all 6 arXiv-selected entries' `pdf_path`/`digest_path` **resolve on disk** (verified via filesystem check); the 4 spot-checked OpenReview ids (`GazlTYxZss`, `l05DseqvuD`, `mrEK16Jy6h`, `gYetLsNO8x`) **resolve in `topics/corpus/ideas.jsonl` with exactly matching titles**. Sampled 6 rejected records: `why` fields are specific, paper-content-based, and topic-appropriate — **no cross-topic contamination found**. The stage_review's claim that live OpenReview fetches were bot-walled and corpus lookup substituted is consistent with what is on disk.

**What was rubber-stamped:**
- **Item 2 declared "REVISE → fixed" but the gate is still not met**: goal.md §3 item 2 requires "load-bearing entries have resolvable `digest_path`"; all 9 grounding records — including both `method-twin`s — remain `digest_path: null`, `id_resolves: false` (verified on disk). Recording the deficiency honestly does not satisfy a binary gate. The overall "PASS" on item 2 is **not supported by file contents** (Finding F10).
- **Item 5 declared PASS with a hole**: H4's verification block has no α and no multiplicity handling across its two conjuncts (the seven-slot check credited "test/alpha" slots that are absent for H4 — F7). And "B0 + B-alt + F-G\* present per §3.3" was checked for *presence*, not construction: B0 fails §3.3's null-by-construction requirement outright (F1) — the single most consequential miss in the whole Phase A pass.
- **Item 4 declared PASS**: Claim 1's "supported-by-design" label evades the H-id/fallback requirement for what is an empirical claim (F12) — a soft orphan the completeness check should have caught.
- **Item 6 declared PASS after fixes**: Part 6 item 5 (B0 per §3.3) and item 9's deeper implication (H3's conjunctive power ≈ 0.3, F6) both slipped through; the per-layer power *statement* was added without confronting what it does to the conjunctive criterion.

**Verdict on the recorded PASS: partially reliable.** The mechanical/verifiable checks (ids, tags, file resolution, honest rejections) were real work, honestly done. The judgment-heavy checks (is B0 actually null-by-construction; do the fallback triggers cover the failure space; is the gate wording actually satisfied post-"fix") were pattern-matched on presence rather than reasoned through — exactly the imagination-vs-verification gap this review was tasked to find.

## Overall: NEEDS-REVISION

The core idea is well-shaped (genuinely non-bridge framing, real estimand, real pivot machinery, honest cost estimates) and no finding kills it — but three flaws would surface at Phase B/D and cost real compute if not fixed first.

**Three highest-leverage fixes:**
1. **Rebuild B0 (F1):** separate the zero-replay judge (current-practice arm) from a genuine null-by-construction placebo (sham-injection and/or no-fault trajectories, localization must be at chance), and make the placebo the arm Phase D step 1 actually checks. Without this the run-validity gate is broken in both directions.
2. **Fix the injected-fault construct (F2 + F5):** add propensity-sampled (policy-regenerable) faults so the monotonicity-violation rate — the mechanism covariate every fallback and the global pivot depend on — has variance by design; simultaneously pre-commit the natural slice's degraded form (judge-only) or replace it with natural failures harvested inside this paper's own replayable harness.
3. **Close the fallback/registration gaps (F3 + F4 + F6):** make paper.md the single registration of record (reconcile the 7-RQ draft), restate every F\* to fire on the *full* negation of its H\* with pre-enumerated sub-case wordings and the H4 combination rule, and re-register H3 with an achievable conjunctive criterion.

Secondary (pre-Phase-B, cheap): add group-testing + B0 arms to the walking skeleton (F8); digest the three load-bearing method-twins and run one targeted arXiv sweep (F10); add α to H4 (F7); wire or drop M5d (F9).

## Fixes applied (2026-07-04)

1. [F1] paper.md "Mandatory baselines": B0 split into B0a (zero-replay judge = current-practice arm, above-chance expected, premise-collapse routes to F-G1) and B0b (null-by-construction placebo: label-shuffle + verified sham-injection, must be at chance).
2. [F1] paper.md: Phase D rewired — goal.md §5 step 1's "placebo first" validity gate explicitly bound to B0b (not B0a), scored before any H*.
3. [F2] paper.md: "R3 confound note (injected-corpus monotonicity)" added before Step 6 — names the exogenous-injection + keep-filter → selection-toward-monotonicity confound; licenses Claim 1/Claim 7 and all violation-rate numbers as injected-corpus properties only; flags the propensity-sampled fault mode as a pre-Phase-B option to log in pipeline.md.
4. [F2] paper.md: global fallback F-G2 added (compound branch: natural slice non-replayable AND degenerate violation-rate variance → pivot to the replayability/censoring measurement, with pre-committed pivoted abstract; X% is a measured placeholder, no number fabricated).
5. [F3] paper.md Step 6: "Registration of record" paragraph added — paper.md is the sole binding spec, with the explicit rq_*↔H* mapping (rq_bisection_ceiling→H1 pooled criterion governs; rq_monotonicity_predictor / rq_position_dependent_savings demoted to descriptive analyses).
6. [F3] pipeline.md Stage 6: SUPERSEDED NOTE added declaring paper.md binding and the Stage 6 rq_* record discussion-loop history only.
7. [F4] paper.md H1: fallback F1 widened to fire on any H1 FAIL, with pre-committed sub-cases (mid-zone 25–50% cost; extreme ≥50%; degenerate-covariate → F-G1/F-G2 combination rules).
8. [F4] paper.md H2: fallback F2 widened to full negation (below-floor-advantage wording; no-advantage; judge-parity wrong-direction at full prominence) with explicit combination rules into F-G1.
9. [F6] paper.md H3: all-3-of-3 conjunctive PASS replaced by ≥2-of-adequately-powered-layers + no-significant-reversal rule, with the honest joint-power statement (≈0.65³–0.70³ ≈ 0.27–0.34 under the old rule) stated in the Aggregation slot; power sentence re-pointed at the new denominator; fallback F3 widened with under-powered and design-immaterial sub-cases.
10. [F7] paper.md H4: α=0.05 with Holm across the two conjuncts added to Verification; p-axis-support pre-condition added (insufficient noise support → INCONCLUSIVE, not FAIL); fallback F4 gains the mixed-conjunct rule (crossover-yes/r=3-no) and the untested-not-retracted branch.
11. [F4/uncovered corner] paper.md H1+H2 Aggregation: PG-2 stratum-loss rule added (lost environment → 2-of-2 same-direction, envelope narrows, shrink logged per situation 10).
12. [F8] paper.md Step 9: walking skeleton gains two smoke arms (2-group M4 group test; B0b sham-injection placebo, 5 traces each) so scale-up genuinely stays config-not-code; criterion sentence and cost estimate (<$250) updated; B0a's later addition justified as a standalone log-reader.
13. [F9] paper.md: M5d (hypothesis-then-verify) given a descriptive reporting rule — if it dominates any structured strategy at any budget point, CO4's guidance switches to the pre-committed hybrid wording.
14. [F12] paper.md Claim–Evidence Map: row 1 relabeled measured-not-assumed with injected-corpus scope + F-G2 route; row 3 traces updated to B0a/B0b; row 7 scope-bounded.
15. [F2] digest.md N10 t1: mitigation extended with the tagged [HYPOTHESIS] R3 pre-commitment and the F-G2 pivot pointer.
16. [F3/F11] pipeline.md Phase Log: new spec-revision row recording all of the above and re-stating that paper_draft.* are stale and must be regenerated at Phase E, never patched.

Not fixed here (needs human decision or compute): method-twin digests + targeted arXiv freshness sweep (F10 — needs fetch access); actually building the propensity-sampled fault mode and the natural-slice re-hosting feasibility count (F2/F5 constructive halves — need pilot compute); regenerating paper_draft.md/.tex/.pdf against the revised spec (Phase E job); length-scaling RQ and verifier-reliability assumption (reviewer-question backlog, optional pre-B additions).
