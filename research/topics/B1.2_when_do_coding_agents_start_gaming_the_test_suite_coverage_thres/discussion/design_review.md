# Design Review (adversarial, 2026-07-04)

> Reviewer stance: skeptical senior PC member. Independent re-verification of the
> self-reported "Phase A (re-run) PASS" in `stage_review.md`; no file other than this
> one was modified. Files read in full: `goal.md`, `guidance.md`, topic `README.md`,
> `digest.md`, `paper.md`, `discussion/reference_candidates.jsonl` (parsed: 16
> selected / 142 rejected / 0 pending / 0 malformed), `discussion/stage_review.md`,
> `discussion/pipeline.md`, `discussion/taste_audit.md`, `discussion/paper_draft.md`
> (spot-checked). Staleness note (said once): `paper_draft.pdf` (13:30) is stale
> relative to `paper_draft.tex`/`.md` (19:16) and to today's `paper.md` (19:13);
> `pipeline.md` itself flags the whole `paper_draft.*` set as a "Phase-E-shaped draft
> of the *plan*", produced ahead of Phases B–D — honestly disclosed, not penalized
> further below.

## Verdict summary

| Dimension | Score | One-line reason |
|---|---|---|
| 1. Feasibility & scale | **FIXABLE** | Real, obtainable data (SWE-bench Verified, Defects4J+Major matrices) and an estimable budget, but the "scale-up is config-not-code" claim is false for the Java track and 2 of 3 agent families, and the named mitigation for the biggest cost risk (EvalPlus surrogate) does not apply to the chosen Python track. |
| 2. Soundness | **FIXABLE** | Estimand, R2 protocol, and B-alt are genuinely strong; but B0 is not null-by-construction (no placebo arm exists at all), colliding with goal.md §5's "placebo first" invalidation rule, and H2 has no effect floor. |
| 3. Novelty & pre-emption | **FIXABLE** | Differentiation vs the cached twins (ResamplingLimits, Regression Accumulation, RepoRescue) is real and non-cosmetic, but the classical APR test-suite-overfitting literature — the most dangerous twin family — was never harvested; the "≈0 hits" claim rests on the wrong corpus. |
| 4. Hypothesis→fallback robustness | **FIXABLE** | Every H\* has a verbatim, specific fallback and F-G1 is pre-worded; gaps: the wrong-direction (inverted-curve) outcome has no matching wording, and no explicit combination rule covers contradictory arms (B-alt vs H4). |
| 5. Method scope & RQ design | **FIXABLE** | Archetype A2's mandatory shapes are mostly present (grid, rival arm, mechanism layer) except the placebo; the estimand's decision claim overreaches to RLVR training that no experiment touches; two RQs a real reviewer will demand are missing. |

**Overall: NEEDS-REVISION** (see final section for the 3 highest-leverage fixes).

---

## Findings (ranked most-severe first)

### F1 [BROKEN] — B0 is not a null-by-construction placebo; no placebo arm exists anywhere in the design

Evidence (`paper.md`, Mandatory baselines): *"**B0 — 'why do this at all' control: the
full-adequacy arm.** Agents run against $ms \approx 1.0$ ... if the gap is already
≥10 pp here, degrading adequacy explains nothing (H1 criterion (iii) encodes this)."*

guidance.md §3.3 assigns B0 **two** jobs: (a) the current-practice arm AND (b) *"a
null-by-construction placebo (shuffle labels/years/assignments) whose effect must be
null. **Non-null placebo = the pipeline measures an artifact = the whole run is
invalid.**"* The full-adequacy arm is only job (a). Think hard about whether this B0
would come out null if the pipeline is clean: **it plausibly would not, for a boring
construct reason** — killing 100% of mutants does not imply passing hidden tests
(mutation operators cannot represent missing-logic faults, and SWE-bench's
fail-to-pass tests probe issue-specific behavior no mutant of the pre-fix program
encodes), so $G(1.0) > 10$ pp is a live outcome even with zero gaming and zero
pipeline artifact. `paper.md` itself knows this — it pre-commits an H1(iii) fallback
(*"mutation score is an insufficient sufficiency criterion"*) that treats a non-null
B0 as a **publishable finding**. But goal.md §5 step 1 is mechanical: *"Placebo
first. B0 non-null → run invalid; ... stop."* At Phase D, the verdict-lookup
procedure would **invalidate the entire run** on exactly the outcome the spec wants
to publish. The arm labeled B0 carries invalidation semantics the design does not
intend, and the semantics the pipeline *needs* (artifact detection) are carried by
nothing. `paper.md`'s A2 row even says a broad oracle failure is *"a
placebo-adjacent failure"* — a tacit admission that no actual placebo exists.

**Fix (cheap, config/analysis-only):** (1) rename the full-adequacy arm to `B-ref`
(current-practice reference; its non-null outcome routes to H1(iii)'s fallback, as
already pre-worded); (2) add a true B0 with two null-by-construction checks that
need **zero new agent runs**: (i) permutation placebo — shuffle adequacy-level
labels across sub-suites within instance and re-fit M4; the ms fixed effect must be
null; (ii) gold-patch pass-through — $g_i$ run through the full scoring pipeline at
every adequacy level must show $G_{gold}(s) = 0$ for all $s$ (this also subsumes
G-S2). Wire both into Phase D step 1.

### F2 [BROKEN as claimed / FIXABLE by repositioning] — Pre-emption risk from the classical APR test-suite-overfitting literature was never assessed

Evidence: the README's novelty premise — *"这是经典 mutation testing 充分性理论对
agent 评价面的直接迁移，全语料中该框架命中≈0"* — and Claim 8 (*"No prior work
sweeps adequacy against agent behavior"*) are grounded solely in an OpenReview/arXiv
-recent corpus. `digest.md` N3's own absence_comment concedes: *"A full review would
additionally want classical mutation-testing literature (PIT/Major,
DeMillo/Offutt-style adequacy theory) and EvalPlus, which lie outside this
OpenReview corpus."* I parsed all 158 cache records: **zero** entries from the
2015–2019 automated-program-repair overfitting literature. That literature is the
real method-twin family: Smith et al. (FSE'15, "Is the cure worse than the
disease?") measured patch overfitting against held-out test suites **as a function
of training-suite coverage/quality** — the same estimand shape, pre-LLM; Qi et al.
(ISSTA'15) established plausible-vs-correct patch gaps; DiffTGen (Xin & Reiss,
ISSTA'17) detects overfitting patches by **differential test generation against the
reference patch** — which is literally M5's mechanism; PATCH-SIM (Xiong et al.,
ICSE'18) classifies patch correctness without oracles. guidance.md Part 5: *"When
the cache is thin ... the harvest was inadequate, not the field empty. Re-harvest
from new angles (method names, metric names ...) before claiming novelty."* The
differentiation is probably survivable (LLM agents under iterative optimization
pressure; mutation-kill adequacy as a *controlled, size/coverage-matched swept
variable*; an onset estimand — none of which Smith et al. did), but right now the
paper walks into an SE reviewer's single most predictable kill ("this is the APR
overfitting literature with an LLM swap") with no concession paragraph, and M5 is
presented as a new mechanism when its core move has a named prior tool.

**Fix:** targeted re-harvest with the angles "test-suite overfitting", "patch
overfitting", "overfitting automated program repair", "patch correctness
assessment"; add the 3–4 canonical papers as `selected` method-twins;
concede-and-differentiate per guidance.md Part 4 situation 6 (repositioning in
`paper.md`, not a silent related-work paragraph); reposition M5 as an
agent-setting adaptation of DiffTGen-style differential testing, with the *new*
part named (metamorphic neighborhood of the visible sub-suite's inputs +
adequacy-conditioned trend). Re-check Claim 8's wording — it survives only in its
narrow form ("adequacy as a *swept, matched* variable against *agents*").

### F3 [FIXABLE] — "Scale-up is a config change, zero new code paths" is false as scoped

Evidence (`paper.md` Step 9): skeleton = *"One agent (Agentless + one fixed model),
one track (SWE-bench Verified Python subset; Defects4J deferred to Stage 1)"*, then:
*"All four ⇒ Stage 0/1 scaling is a config change (instances, levels, agents, k) —
zero new code paths."* Stage 1 adds a Java track (Defects4J, Major kill matrices,
JVM build/test execution, a different mutation toolchain than mutmut/cosmic-ray) and
two agent families (SWE-agent, OpenHands) whose harness adapters the skeleton never
exercises. Those are code paths by any definition; guidance.md Part 4 situation 8:
*"The skeleton failed even if pilot numbers looked fine."* The gate as written will
be silently violated at Phase C.

**Fix (choose one, pre-commit now):** (a) extend the skeleton with 2 Defects4J
instances and a 1-instance smoke run per agent family (adds ~10–20 episodes, still
≤2 days); or (b) pre-commit Stage 1 to the Python track + Agentless-compatible
adapters only and demote Defects4J/extra families to a pre-registered extension
with its own mini-skeleton gate.

### F4 [FIXABLE] — M5's input-generation machinery is undefined at repository scale, and the pre-committed cost mitigation doesn't fit the chosen benchmark

Evidence: Step 5 defines gaming via *"differential testing of $p$ vs $g_i$ on
$N=200$ generated inputs ... (b) disagreement on ≥30% of inputs in the metamorphic
neighborhood of $T_v$'s inputs"*, labeled "Automated". For SWE-bench repo-level
patches, "inputs" are not vectors to a function — they are pytest invocations
against arbitrary repository APIs; no generator (fuzzer? property-based? Pynguin?)
is named, and generating 200 valid inputs per patched entity across ~150
heterogeneous repos is itself a research-grade engineering effort. Separately,
`digest.md` N6's mitigation for *"the biggest feasibility risk"* — *"reuse
EvalPlus's precomputed 80×-augmented tests as a ready-made held-out oracle and
mutant surrogate"* on the Python track — is incompatible with that track as chosen:
EvalPlus artifacts exist for HumanEval/MBPP function-level problems, not SWE-bench
Verified repositories. So the Python track carries both fresh whole-repo mutation
costs ("hours of CPU" in Step 9 is optimistic for repo-scale suites × hundreds of
mutants × 150 instances) and an unspecified M5 input generator, while the mitigation
text points at an artifact that cannot be used there.

**Fix:** name the input-generation tool per track (e.g., EvoSuite for Defects4J;
Hypothesis/Pynguin-based generation scoped to the patched function(s) for Python),
make "M5 generator produces ≥N valid inputs on ≥80% of pilot patches" a skeleton
gate; either add a function-level EvalPlus track where the surrogate actually
applies, or delete the EvalPlus mitigation and re-estimate mutation preprocessing
cost honestly for SWE-bench.

### F5 [FIXABLE] — H2 has no effect floor (a mandatory §3.1 slot), despite the recorded PASS on checklist item 5

Evidence (`paper.md` E2): *"H2 (monotone growth) holds iff the fitted $G(s)$ is
non-increasing in $s$ with a trend test $p<0.05$ (Holm)."* guidance.md §3.1:
*"**Effect floor is mandatory**: significance without magnitude passes nothing (a
slope can be significant and practically zero)."* With ~36,000 episodes, a 1-pp
total drift across the sweep could clear $p<0.05$; "monotone growth" would then be
claimed for a practically flat curve. H1 (10 pp), H3 (0.15 ms-units), H4 (15 pp)
all have floors; H2 alone does not. `stage_review.md` item 5/6 asserted *"every H\*
has all 7 §3.1 slots in substance (… effect_floor …)"* — not true for H2.

**Fix:** add a floor, e.g. "and the fitted total change $\hat G(0.3)-\hat G(1.0)
\ge 5$ pp attributable to the monotone component" (or a minimum standardized slope),
pre-registered now.

### F6 [FIXABLE] — Failure-space gaps: inverted-direction wording, and no combination rule for contradictory arms

(a) If the curve is **inverted** (gap larger at *high* adequacy), H1 fails via (i),
but the pre-committed F1 wording asserts *"held-out correctness is insensitive to
visible-suite adequacy"* and F-G1's pivoted abstract says the sweep *"produces no
rise"* — both sentences are factually wrong for an inverted result. guidance.md
Part 4 situation 4 requires wrong-direction results at full prominence with their
own interpretation; no verbatim sentence exists for it. (b) §3.1: *"Write the
fallback-combination rules too … never invent combination logic at verdict time."*
The only explicit combination logic is H2–H4's conditionality on H1 and "{H1} fails
⇒ F-G1". Uncovered mixed case: **B-alt kills the mechanism (iterative slope ≤
selection-only slope) while H4 passes (gaming fraction rises with degraded
adequacy)** — one arm says "selection effect", the other says "adaptive gaming";
guidance situation 9 exists generically, but no pre-committed sentence resolves
which claim survives.

**Fix:** add one verbatim wrong-direction sentence to E1's fallback block ("if
$\hat G(0.3) - \hat G(1.0) \le -10$ pp, we report the inversion at full prominence
and …"), and one combination rule for B-alt×H4 (e.g., "if B-alt fails to isolate
and H4(ii) passes, Claim 6 falls, Claim 5 is downgraded to 'gaming-shaped patches
arise under selection alone', and the mechanism paragraph reports the tension as a
finding per situation 9").

### F7 [FIXABLE] — Claim 6 / B-alt's isolation criterion is a fifth hypothesis living outside the hypothesis machinery

Evidence: the Claim–Evidence Map row 6 traces to *"B-alt isolation criterion"*
(*"iterative arm's gap slope exceeds the selection-only arm's by ≥5 pp at
$ms \le 0.45$ ($p<0.05$)"*) — a binary, tested, fallback-carrying claim that is not
an H\*, is not in the Holm family (*"Holm-corrected across {H1, H2, H3, H4}"*), and
has no seven-slot template (no stated test statistic, no power, ambiguous phrasing —
a "slope" exceeding by "pp" mixes a derivative with a level difference). A
mechanical Phase D verdict lookup has no registered criterion id to score it under.

**Fix:** promote it to H5 with the full §3.1 template, include it in the Holm
family (m=5), and disambiguate the metric (difference in $\hat G$ at $ms \le 0.45$,
or difference of fitted slopes — pick one).

### F8 [FIXABLE] — Estimand/motivation overreach to RLVR training that no experiment touches

Evidence: Step 5's estimand feeds *"a quantitative sufficiency floor for verifier
adequacy … for teams instrumenting agent **training** or CI-gating pipelines"*, and
Step 2(b): *"verifier-sufficiency requirements for agent gating/**RLVR** can be
stated quantitatively."* Every experiment is inference-time iterative repair with a
frozen model; optimization pressure from k≤B retries within one episode is not
gradient pressure across a training run, and the two regimes are known to differ
(reward-hacking severity grows with optimization steps). This is archetype A2's
named reviewer kill: *"claims generalized beyond the measured envelope."*
`pipeline.md`'s seed brief already states *"Out of scope: training new agents or
reward models"* — the estimand contradicts the scope statement.

**Fix:** bound the decision clause to gating/evaluation-time acceptance
("budget-bounded iterative repair under a frozen policy"), and demote the RLVR
implication to one explicitly-flagged extrapolation sentence in Limitations with a
named protocol someone could run (situation 14(b)).

### F9 [NOTE] — Mutant provenance is never specified, and it is load-bearing

`paper.md` Step 5: *"mutant set $M_i$ generated by fixed operators"* — of which
program, the buggy $b_i$ or the gold-patched $g_i(b_i)$? The held-out oracle
includes *"the killing tests of excluded mutants"*, which probe correct behavior
only if mutants are of the **fixed** version (Defects4J/Major convention). If any
track mutates the buggy version, $ms$ and M3 measure different constructs across
tracks. One sentence fixes this; it must be written before Phase B.

### F10 [NOTE] — R2 step ② calibration supply is not guaranteed by the skeleton

The M5 protocol requires *"≥20 pilot $V{=}1,H{=}0$ patches from the walking
skeleton"*, but G-S4 only guarantees *"≥1 concrete $V{=}1,H{=}0$ patch archived"*
from 60 episodes. If the pilot yields 3 such patches, step ② cannot run as written.
Pre-commit the top-up rule (e.g., extend the pilot at the low-adequacy arm until 20
qualifying patches exist, capped at +100 episodes).

### F11 [NOTE] — Power is stated for the primary comparison only, not per cell

E1: *"power target: ≥0.9 to detect a 10 pp gap difference"* — good as an entry
gate, but guidance Part 6 item 9 asks for power **per cell**; only the thin-cell
INCONCLUSIVE rule (k<3) covers the rest. H3's per-family $s^*$ CIs and H4's
per-band trend have no power statement at all. Add per-H power lines at Stage-1
entry using the pilot variance.

### F12 [NOTE] — Reference-cache hygiene

Verified on disk: `2512.21919` (SWE-RM), `2607.01213` (RepoRescue), `2607.01855`
(Regression Accumulation), `acl_pang-etal-2023-reward` — all pdf_path/digest_path
resolve; `why` fields are topic-specific with no cross-topic contamination; 142
rejections each carry a specific reason; 0 pending. Honest residual (disclosed in
stage_review item 2): the 8 backfilled OpenReview works (incl. the method-twin
ResamplingLimits and the dataset-source SWEbench) have `pdf_path/digest_path =
null`. Two small defects: `verified.id_resolves=false` on those 8 conflates
"OpenReview id resolves" (it presumably does) with "locally cached" (it isn't) —
the schema field is being misused; and RepoRescue's `title` contains scraped author
-line garbage ("…Zhihao Lin1 Mingyi Zhou1…"), which will leak into a
script-generated refs.bib.

### F13 [NOTE] — Eligible-pool selection bias is unbounded

A1's pre-screen ("rich kill matrix") plus the fixed-size/coverage constraint skews
the instance pool toward heavily-tested, mutation-friendly repositories. The
consequence column handles the mechanics ("restricts scope") but the validity
envelope never names this bias; add one sentence to Limitations ("estimates
condition on repositories with suites rich enough to sample from — plausibly the
*least* gaming-prone population" — which also biases $s^*$ in a directional,
statable way).

---

## Failure-space simulation (per-H walk-through)

- **H1 fails, flat curve** (fails (i)/(ii)): F1 verbatim wording exists and routes
  to F-G1's pre-written refutation abstract. The fallback paper survives review
  **only if** the power gate held and A5's contamination sensitivity analysis ran
  (both pre-registered — good). Residual risk: F-G1's credibility depends on the
  placebo machinery that currently doesn't exist (F1 finding above): a reviewer of
  the null paper will ask "how do you know your pipeline could have detected a
  gap?" — the gold-patch/permutation placebo is exactly the answer, and it is
  missing. **Covered after F1 fix; under-defended now.**
- **H1 fails via (iii)** (gap large even at ms=1.0): pre-worded pivot to an attack
  on the adequacy construct — publishable and honest. Covered. (Note this outcome
  currently also trips goal.md §5's B0-invalidation rule — the F1 collision.)
- **H1 inverted direction**: NOT covered — no verbatim wording fits (F6a). This is
  the one outcome where the current text would force improvisation at verdict time.
- **H2 fails (non-monotone)**: covered, with the per-mutant-class breakdown
  pre-declared exploratory. Fine. (H2 passing trivially via a floor-less
  significant-but-tiny trend is the inverse risk — F5.)
- **H3 either branch**: both pre-worded ("no universal threshold" / "benchmark-
  intrinsic threshold"); A6's de-scope order (drop to 2 families) degrades H3
  gracefully and is pre-declared. Covered.
- **H4 κ<0.7**: CO3 withdrawn, annotated patch set released as a labeling
  benchmark — a real, reviewable fallback artifact. **H4(ii) fails**: honest-
  incompleteness headline pre-worded. **<100 qualifying patches**: descriptive only.
  All covered. Uncovered: H4 pass + B-alt fail contradiction (F6b).
- **All-fail**: F-G1 + CO3 withdrawal + H3's indistinguishability wording still
  compose into a coherent negative-result paper (measured null + validated
  instruments + selection-effect attribution), *provided* the placebo and power
  machinery make the null credible. No outcome leaves the paper with literally
  nothing — the genuinely uncovered cells are (a) inverted direction and (b)
  contradictory-arms, both wording-level and fixable now.

## Missing RQs / reviewer questions the design cannot currently answer

1. **"Where do real suites sit on your axis?"** The decision claim ("your suite
   must kill ≥ s\*") is only actionable if the paper reports the *empirical
   distribution of ms* for shipped SWE-bench/Defects4J suites (and ideally typical
   CI suites). This is nearly free (the kill matrices already exist) and converts
   s\* from a curiosity into a calibration. No RQ covers it.
2. **"Is the onset driven by which mutants survive, not how many?"** Mutant-class
   heterogeneity appears only inside E2's fallback as exploratory; a reviewer of
   the *main* result will ask whether s\* is stable under different operator mixes
   at the same scalar ms (the C1 challenge the digest itself raises). A small
   pre-registered robustness cell would pre-empt this.
3. **"Does this hold under a different harness/prompt?"** t5 fixes one harness —
   correct for internal validity, but a single-harness threshold estimate invites
   the "harness idiosyncrasy" kill; one pre-registered prompt-variant cell (or an
   explicit envelope clause) is needed.
4. **"Training vs inference"** (F8): as framed, a reviewer can reject the RLVR
   motivation outright; the design has no answer beyond narrowing the claim.
5. **"Is M5 just DiffTGen?"** (F2): currently unanswerable because the prior tool
   is not in the cache.

## Reliability audit of the prior Phase A PASS

Re-verified independently (items 4, 5, 6 chosen as most likely rubber-stamped, plus
items 1–2 en route):

- **Item 2 (reference-cache integrity) — held, and honestly reported.** The recorded
  REVISE correctly exposed a hard violation (N3's 9 works absent from the cache) and
  the backfill is real (I re-parsed the file: 16 selected, 0 pending). The residual
  null-path gap on 8 backfilled works is disclosed, not hidden. Spot-checked 4
  records: paths resolve, whys topic-appropriate, no cross-topic contamination.
  Minor schema misuse (`id_resolves=false` meaning "not locally cached") noted (F12).
- **Item 4 (claim–evidence map) — mostly held.** All 8 rows trace as claimed; but the
  recorded PASS missed that Claim 6's trace ("B-alt isolation criterion") is a
  tested hypothesis with no H-id, no template, and no multiplicity treatment (F7) —
  a completeness gap the checklist item exists to catch.
- **Item 5 (seven-slot completeness) — rubber-stamped in two places.** (a) The
  recorded PASS asserts every H\* has an effect floor "in substance"; **H2 has
  none** (F5). (b) "B0 + B-alt + F-G1 were already present … PASS, no fix needed
  there" — B0 as specified fails guidance §3.3's own definition (no
  null-by-construction placebo), the single deepest requirement in the section
  (F1). (c) §3.1's "write the fallback-combination rules too" was never checked;
  only H1-gating exists (F6b).
- **Item 6 (Part 6 self-check) — partially rubber-stamped.** Item 5 of Part 6
  ("B0 + B-alt + F-G\* all present") was passed incorrectly (same B0 issue); item 9
  ("power stated per cell") was passed on the strength of one primary-comparison
  power target plus the thin-cell rule — generous (F11). Items 1 (estimand), 6 (R2
  for M5), 7 (R3 confounds) genuinely hold post-fix: the Estimand sentence, the
  5-step M5 protocol with κ≥0.7, and the size/coverage-matching↔C4/t2 pairing are
  all real and verifiable in today's `paper.md`; the recorded 0.6→0.7 κ propagation
  into `paper_draft.md` is confirmed (line 174/180).
- **Item 1 (digest self-verification) — held with one gloss.** Tags, cross-refs,
  and absence_comments check out as recorded; but goal.md §0 requires the digest to
  end with "Claims + self-verification", and no self-verification section exists —
  the recorded PASS silently re-scoped the requirement (the N9 falsification-
  condition substitution is defensible; the missing terminal self-check is not
  mentioned at all).

**Net reliability: partially reliable.** The Phase A re-run did real work (the
cache backfill, the estimand, the consequence column, the R2 protocol, the thin-cell
rule are genuine improvements, all verified present), and its two REVISE findings
were honestly fixed. But it validated the *presence* of the control-arm and
hypothesis machinery, not its *construction*: the placebo requirement, H2's effect
floor, the combination rules, and Claim 6's registration were all waved through.
The PASS is trustworthy on bookkeeping, not on the deepest §3.3/§3.1 semantics.

## Overall: **NEEDS-REVISION**

Strong spec by the standards of this pipeline — a real estimand, a genuinely
non-bridge asymmetry (the taste audit's 🟢 is deserved), a budget-matched rival arm,
verbatim fallbacks, and an honest phase log. But it is not safe to spend compute on
yet. The three highest-leverage fixes:

1. **Install a real placebo and rename the current B0** (F1): permutation-of-
   adequacy-labels refit + gold-patch pass-through as the null-by-construction B0
   (analysis-only, zero new episodes); route the full-adequacy arm's non-null
   outcome to H1(iii) explicitly so Phase D's "placebo first" rule cannot
   invalidate a publishable finding.
2. **Close the APR-overfitting pre-emption hole** (F2): one targeted re-harvest
   (Smith'15 / Qi'15 / DiffTGen / PATCH-SIM), concede-and-differentiate in
   `paper.md`, reposition M5 relative to DiffTGen, and tighten Claim 8's wording —
   before this, the novelty claim is unverified against its most dangerous twins.
3. **Make the skeleton actually license the scale-up** (F3+F4): add Defects4J and
   per-agent smoke instances (or pre-commit the Python-only de-scope), name the M5
   input generator per track with a skeleton gate, and delete or relocate the
   EvalPlus mitigation that cannot apply to SWE-bench.

Secondary (cheap, do in the same edit pass): H2 effect floor (F5); inverted-
direction sentence + B-alt×H4 combination rule (F6); promote Claim 6 to H5 in the
Holm family (F7); bound the RLVR claim (F8); specify mutant provenance (F9);
R2-step-② supply rule (F10).

## Fixes applied (2026-07-04)

Authorized direct edits; surgical, style-matched; no results or validation numbers fabricated. paper.md and digest.md only.

- **F1 / paper.md (Mandatory baselines):** relabeled the full-adequacy arm B0 → **B-ref** (scored as evidence, never a validity gate); added a genuine null-by-construction **B0 placebo** with two analysis-only checks — (i) within-instance permutation of adequacy-level labels refit through M4 (shuffled-ms effect must be null), (ii) gold-patch pass-through ($\hat G_{gold}(s)=0$ at every level); made the Phase D order explicit (B0 first; B-ref and H1–H5 scored only if B0 is null), removing the collision between H1(iii)'s "finding" semantics and goal.md §5's "placebo non-null → run invalid" rule.
- **F1 / paper.md (A2 row):** "placebo-adjacent failure" reworded to "B0(ii) placebo failure (gold-patch pass-through non-null)" — the detection now names a real placebo check.
- **F5 / paper.md (E2):** added H2's mandatory effect floor in native units — fitted-curve total change $\hat G(0.3)-\hat G(1.0) \ge 5$ pp; significant-but-flat trends now fail H2.
- **F7 / paper.md (B-alt + design constants + Claim map row 6):** registered the isolation criterion as **H5** with all §3.1 template slots and a verbatim fallback F5; disambiguated the metric (band-level gap difference at $ms \le 0.45$, superseding the ambiguous "slope … by ≥5 pp" wording); extended the Holm family to {H1–H5}.
- **F6 / paper.md (new "Fallback-combination rules" section):** five pre-committed rules covering flat-curve routing, the previously uncovered **wrong-direction (inverted-curve) outcome** with its own verbatim sentence (Part 4 situation 4), H1(iii)-alone, the **H5-fail × H4-pass contradictory-arms case** (Claim 6 falls, Claim 5 downgraded to a pre-worded selection-only sentence, situation 9), and κ-failure's veto on any resurrected gaming attribution.
- **F2 / paper.md (new "Positioning vs. classical APR overfitting literature" section):** concede-and-differentiate applied now — conceded the overfitting construct and the differential-testing move (Smith'15, Qi'15, DiffTGen, PATCH-SIM; all marked **UNVERIFIED — requires harvest**); differentiated on estimand (threshold-conditioned gaming onset under controlled, size/coverage-matched adequacy, iterative LLM agents, selection control); repositioned M5 as a DiffTGen-style adaptation with its genuinely new parts named; narrowed Claim 8 / "≈0 hits" to the defensible corpus-limited form; recorded the APR harvest as the blocking pre-Phase-B residual.
- **F2 / paper.md (Claim map row 8):** claim text narrowed to "size/coverage-matched mutation adequacy against LLM-agent behavior", broad reading withdrawn, trace extended to digest N3 item 10.
- **F3 / paper.md (Step 9):** added the cross-track/cross-agent **smoke slice** (2 Defects4J instances + 1 episode per additional agent family, ≈68 episodes total) and gate **G-S5**; the config-not-code claim is now scoped to "the envelope G-S5 licensed", with a pre-committed de-scope (SWE-bench Python + Agentless-compatible) if a smoke episode fails.
- **F10 / paper.md (Step 9, G-S4):** added the calibration-supply rule — if the skeleton archives <20 $V{=}1,H{=}0$ patches, the low-adequacy arm is extended (capped +100 episodes) until R2 step ②'s ≥20 exist.
- **F4 / paper.md (Step 5 adequacy row + M5 protocol):** withdrew the inapplicable EvalPlus surrogate (function-level artifacts vs repository-level SWE-bench); replaced with mutation restricted to gold-patch-touched files; defined M5's input generation concretely per track (EvoSuite for Defects4J; Hypothesis-based, visible-test-seeded generation scoped to patched functions for SWE-bench Python) with gate **PG-M5** (≥N valid inputs on ≥80% of calibration patches, pre-declared E4 scope restriction on failure).
- **F9 / paper.md (Notation):** mutant provenance specified — operators applied to the gold-patched program $g_i(b_i)$ (Defects4J/Major convention), so excluded mutants' killing tests probe correct behavior in M3.
- **F8 / paper.md (Estimand + Step 2(b)):** decision claim bounded to evaluation/acceptance-time gating under a frozen policy; RLVR training-time extrapolation demoted to an explicitly flagged Limitations conjecture.
- **F2 / digest.md (N3):** added item 10, the `[UNVERIFIED — requires harvest]` APR method-twin block (Smith'15, Qi'15, DiffTGen, PATCH-SIM), flagged as a blocking pre-Phase-B residual; nothing citable until harvested.
- **F4 / digest.md (N6 feasibility):** corrected the biggest-risk mitigation — EvalPlus clause replaced by patch-touched-file-scoped mutmut/cosmic-ray mutation on the Python track.
- **F2 / digest.md (Claims item 3):** appended the scope caveat narrowing the "≈0 hits" absence claim to its corpus-limited, defensible form, with evidence pointer to N3 item 10.

**Not fixed here (needs human/compute/network):** the APR harvest itself and the fetch+digest of the 8 backfilled OpenReview references (no network); per-H/per-cell power statements (need the pilot's variance estimate, F11); `reference_candidates.jsonl` metadata hygiene (RepoRescue title garbage, `id_resolves` semantics, F12) — left untouched per edit scope; `paper_draft.md`/`.tex`/`.pdf` are now stale relative to today's paper.md/digest.md edits (B0/B-ref, H5, combination rules, APR positioning) and need a Phase E/F re-pass before any compile.
