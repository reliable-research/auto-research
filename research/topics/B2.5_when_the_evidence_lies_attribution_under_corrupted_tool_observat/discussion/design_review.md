# Design Review (adversarial, 2026-07-04)

> Reviewer stance: skeptical PC member, design-only review of the pre-registered spec.
> Files reviewed: `README.md`, `digest.md`, `paper.md`, `discussion/reference_candidates.jsonl`,
> `discussion/stage_review.md`, `discussion/pipeline.md`, `discussion/paper_draft.md`,
> `discussion/taste_audit.md`, plus on-disk verification of cache paths and independent power
> calculations. The recorded "Phase A (re-run) PASS" in `stage_review.md` was NOT trusted;
> checklist items 2, 4, 5, and 6 were independently re-verified (see Reliability audit).

**Staleness note (stated once):** `paper_draft.md`/`.tex`/`.pdf` (mtime 13:40–13:42) predate
today's `paper.md` edits (mtime 19:18 — estimand sentence, assumption-consequence column,
confound ledger) and use a different experiment articulation (7 RQs incl. instrument-validation
RQs vs. `paper.md`'s E1–E3/H1–H3). Findings below are against `paper.md` as the binding spec;
the draft is cited only where it contains material `paper.md` should have absorbed.

---

## Verdict summary

| Dimension | Score | One-line reason |
|---|---|---|
| 1. Feasibility & scale | FIXABLE | Datasets are real and costs estimated, but "scale-up is a config change" is not credible for 3 heterogeneous frameworks the skeleton never touches; Who&When log replay is a live risk. |
| 2. Soundness | FIXABLE (one BROKEN element) | Estimand and stats machinery mostly solid, but B0 is not null-by-construction (goal.md §5 step 1 is inoperable as written), the plausibility screen has no R2 validation, and H2 is underpowered at its own pre-declared minimum (~51% power). |
| 3. Novelty & pre-emption | FIXABLE | Differentiation from method-twins (Who&When, AgenTracer) is real — new response variable and fault universe; no bridge framing — but the harvest that certifies non-pre-emption demonstrably missed all 8 core works, so its recall cannot be trusted. |
| 4. Hypothesis→fallback robustness | FIXABLE | F1/F2/F3/F-G1 are verbatim and mostly strong, but the failure space has holes: incompetent-on-overt-errors branch, H2b has no fallback, significantly negative Δ, and license-makes-it-worse are all uncovered. |
| 5. Method scope & RQ design | FIXABLE | Validity envelope stated; A2 kill-list mostly pre-empted; but the A2-mandatory placebo arm is missing, and the human-annotator arm exists in M3 with no RQ/H attached. |

**Overall: NEEDS-REVISION** (salvageable pre-compute; no fatal conceptual flaw found).

---

## Findings (ranked most-severe first)

### F-1 [BROKEN] B0 is not null-by-construction; Phase D's "placebo first" gate is inoperable as written

Evidence — `paper.md`, Mandatory baselines:

> "**B0 — 'why do this at all' control: the overt-error arm + a constant-guess attributor.**"

guidance.md §3.3 requires B0 to include "(b) a null-by-construction placebo (shuffle
labels/years/assignments) whose effect must be null. **Non-null placebo = the pipeline measures
an artifact = the whole run is invalid.**" Neither of B2.5's two B0 components has a null
prediction: the overt-error arm is *part of the estimand itself* (Δ_A's subtrahend — it is
expected to show strongly non-null attribution accuracy), and the always-predict-plan attributor
is a floor baseline, not a placebo. goal.md §5 step 1 ("Placebo first. B0 non-null → run
invalid... B0 checked first") is mechanically unexecutable: there is no defined observable whose
non-nullness would invalidate the run. A pipeline artifact (injection metadata leaking into the
serialized trajectory, replay side-effects, selection effects from 3–5× over-generation) could
manufacture a spurious Δ > 0 and **nothing in the design would catch it** — the exact failure
Phase D's step 1 exists to prevent, in a paper whose entire thesis is "pipelines silently trust
corrupted evidence." The irony should be motivating.

**Fix (concrete):** add two cheap placebo components with pre-committed null criteria:
(a) *sham-injection arm* — run verified genuine-plan-failure (or matched) trajectories through
the identical injection→replay→serialization machinery with the identity mutation (o′_t = o_t);
each method's attribution distribution on sham-processed vs. untouched twins must be
statistically indistinguishable (equivalence margin pre-set, e.g. ≤3 pp); (b) *label-shuffle
analysis placebo* — recompute Δ_A after permuting the D_sem/D_overt arm labels within matched
task-step pairs; the permuted Δ must be centered on 0. Wire both into goal.md §5 step 1 as the
operational meaning of "B0 null."

### F-2 [FIXABLE] The plausibility screen is an unvalidated LLM-judge instrument — the A2 archetype's #1 reviewer kill

Evidence — `paper.md` Step 5 defines "subtle" as:

> "screen model (≠ any judge model, per A7) answers 'not self-evidently wrong in context' with
> confidence ≥ 0.8; 'borderline' = [0.5, 0.8)"

guidance.md A2 reviewer kills: "**unvalidated LLM-judge**"; Part 6 item 6: "Every instrument has
the 5-step R2 plan with an acceptance threshold." The screen gates M1 admission (gate iii),
stratifies the M5 grid, and defines the construct "subtle" — it is load-bearing — yet `paper.md`
contains no R2 sequence for it: no external grounding, no calibration set, no ≥2 human raters,
no κ/agreement threshold, no freeze-hash. A7 covers only model-family disjointness, which is a
different threat. Notably, `paper_draft.md` RQ1 ("Does the automated legality screen approximate
human undetectability?... At least 90% of gate-passing corruptions are independently rated
plausible-in-context") **already contains most of this validation experiment — but it never made
it back into `paper.md`** as a gated PG-* instrument check, so the binding spec would scale an
unvalidated screen (violating goal.md §8: "No instrument runs at scale without passing R2").

**Fix:** promote draft-RQ1 into `paper.md` as a walking-skeleton gate G5: 2 human raters ×
stratified sample of gate-passing + gate-rejected candidates, agreement threshold (e.g., ≥90%
pass-rated-plausible AND rater κ ≥ 0.7), confusion-structure inspection, then freeze the screen
prompt+threshold by hash. Add a sensitivity analysis over the 0.8 confidence threshold.

### F-3 [FIXABLE] "Scale-up is a config change" is asserted, not designed — the skeleton de-risks 1 of 3 frameworks

Evidence — `paper.md` Step 9: skeleton = "10 AgentDojo tasks... single-agent ReAct-style
framework, one backbone," followed by:

> "**Skeleton passed ⇒ scale-up (3 frameworks, 5 operators, 5 methods, n≥300/arm, M5 grid, trust
> probe) is a config change — more tasks, more operators, more methods in the same harness — not
> a code change.**"

The estimand's population spans "single-agent (AgentDojo), long-horizon (GAIA), and logged
multi-agent (Who&When) trajectories." Adding GAIA (different tool stack, no fixed harness) and
especially a Who&When-logged multi-agent system requires new environment adapters, tool-state
reconstruction for replay, and framework-specific injection interception — code by any
definition, and precisely guidance.md situation 8 ("the skeleton failed even if pilot numbers
looked fine"). Worse, A2's replay-determinism gate (G2 ≥90% twin agreement) is only ever
exercised on AgentDojo; replaying *logged* trajectories of someone else's multi-agent system
against live tool state is the setting where G2 is most likely to fail, and the design finds
that out only after full pilot investment.

**Fix:** either (a) narrow the estimand population to AgentDojo + GAIA and demote Who&When logs
to the plan-failure control source only (they are already M6(b)'s source — no replay of full
multi-agent runs needed for that if A6's audit is per-tool-call), or (b) extend the skeleton
with a 3–5-trajectory injection+replay smoke test per additional framework before declaring
config-not-code.

### F-4 [FIXABLE] H2 is underpowered at its own pre-declared minimum; "power stated per cell" holds only for H1

Evidence — `paper.md` E2: "conditional on E1 producing ≥50 misattributed cases per method (else
E2 reported descriptively)" and "π_plan ≥ 0.65 with exact binomial p < .05 against 0.5."
Independent calculation: exact binomial, n=50, two-sided α=.05 (critical k=33) gives **power
≈ 0.51** at true π=0.65. So at the pre-declared minimum, a genuinely present skew of exactly the
hypothesized size fails H2 about half the time, and the pre-committed F2 ("blame scatters...
directionally diffuse") would then be published as a *false* finding. H3 likewise has no power
statement (McNemar power for a 5 pp reduction depends on the discordant-pair rate, never
estimated); guidance Part 6 item 9 requires "power stated per cell," and the Phase A pass cited
sample-size minima (≥50, ≥15/cell) as if they were power statements.

**Fix:** raise the E2 conditional threshold to ≥120–150 misattributed cases per method (power
≈0.8–0.9 at π=0.65), or lower α-spend via a one-sided pre-registration, and pre-declare the
50–120 band INCONCLUSIVE (not F2). Add a discordant-rate assumption + power statement for H3;
pre-declare the corresponding INCONCLUSIVE band.

### F-5 [FIXABLE] Uncovered failure branches: incompetent-on-overt, H2b, negative Δ, license-backfires

Simulated failure walk (details in next section) finds four outcomes with no pre-committed
sentence:

1. **Methods incompetent on overt errors** — H1's own clause "m_A(D_overt) ≤ 40% for those
   methods (they must be competent on overt errors, else the gap is uninterpretable)"
   (`paper.md` E1) names the condition but pre-commits nothing for its failure. If most methods
   flunk overt errors, H1 cannot pass, F1's wording ("localize... as reliably as overt errors")
   is false, and F-G1's pivot abstract ("localize such corruptions about as well as overt
   errors") is equally unusable. This is guidance §3.3's B0-job-(a) premise-collapse branch with
   no route to the pivot.
2. **H2b fails while H2 passes** — Claim 4 is marked "fallback-covered (F2)" but F2's wording
   covers only directional diffuseness, not "no corruption-type factor predicts direction."
3. **Δ significantly negative** (methods *better* on semantic corruption) — F1 covers only
   "within ±10 pp, n.s."; situation 4 (wrong direction, report at full prominence) has no
   pre-committed wording.
4. **Trust license *increases* misattribution on D_sem** — F3 covers "n.s." and
   "reduction-with-FPR-inflation," not a significant wrong-direction effect.

**Fix:** add F0 ("attribution methods cannot reliably localize even overt tool faults — the
attribution layer is broadly unreliable and the schema-validity distinction is moot; the paper
becomes a competence audit anchored on the constant-attributor floor"), an F2b for
type-independence, and one wrong-direction sentence each for Δ<0 and δ>0, plus explicit
fallback-combination rules (guidance §3.1: "write the fallback-combination rules too" — the spec
has only "(Feeds F-G1)" on F1).

### F-6 [FIXABLE] The headline Δ contrast carries an unnamed confound: fault-to-manifestation distance

Evidence — the Confound-removal ledger (`paper.md`) matches D_sem/D_overt on task and step
locus, but an overt error (exception/timeout) typically truncates or visibly derails the
trajectory at step t, while a schema-valid corruption lets the agent run on, producing a longer,
more entangled post-fault suffix. Attribution difficulty plausibly grows with the distance
between fault and failure manifestation *regardless of channel* — a boring partial explanation
for Δ > 0 that step-locus matching does not remove. The B-alt agent-side arm does control this
for the mechanism claim (agent-side wrong values propagate silently too), but B-alt is only
scored for "the methods passing H1," so the headline H1 number itself remains exposed. R3 says
"obvious-Y without an X means the design is broken"; here Y is identified and X is missing.

**Fix:** add the confound to the ledger with a named constraint: report Δ_A stratified by
post-fault suffix length (or failure-manifestation lag), and/or include suffix length as a fixed
effect in the E2 mixed model; pre-commit the interpretation if Δ collapses within
suffix-length strata.

### F-7 [FIXABLE] Novelty is certified by a harvest with demonstrably poor recall

Evidence — `stage_review.md` Phase A item 2: "The 150-item harvest (110 arXiv + 40
ACL-anthology, both weak-recall keyword pulls) hit zero overlap with these 8 titles/ids." A
sweep that misses Who&When and AgenTracer — the paper's own method-twins — cannot support the
digest's Claim 1 ("The specific condition... is unoccupied in the searched corpus"). The
differentiation itself is genuine (new response variable: attribution correctness, not attack
success; new fault universe: observations, not actions; the `why` fields on both method-twin
records concede shared machinery correctly), and no bridge/integrate framing survives into a
claim (verb audit independently confirmed). But situation-12 risk (an exact
"attribution-under-corrupted-observations" study existing unfound) is currently unbounded.

**Fix:** re-harvest with angles derived from the method names this spec itself uses
("counterfactual replay attribution," "observation corruption agent," "fault injection tool
output," "blame assignment corrupted evidence," Who&When/AgenTracer *citing* papers) before
Phase B; goal.md §1's freshness sweep before Phase E is too late for a pre-emption discovery.

### F-8 [FIXABLE] The human-annotator arm exists in the method but no hypothesis consumes it

Evidence — `digest.md` M3: "a human-annotator reference on a stratified 10% subsample." No H*,
RQ, fallback, or claim touches it. This is the single most reviewer-attractive question the
design already pays for: *are humans fooled too?* If yes, Who&When's human-annotated ground
truth (and MAST's whole taxonomy, per N4 item 7) is contaminated in exactly the way the paper
theorizes — a much bigger implication than any per-method Δ; if no, humans become the repair
upper bound that the trust-license probe should be compared against. Leaving it unregistered
invites post-hoc cherry-picking of whichever human result is convenient.

**Fix:** pre-register H4 (descriptive floor acceptable): human misattribution rate on D_sem with
CI, compared against both the best automated method and the overt-error control, with
pre-committed wording for both directions.

### F-9 [NOTE] MAST is `selected` (relevance: contrast) with `digest_path: null` and content asserted from memory

Evidence — cache record `MAST_250313657`: `"digest_path": null`, `"pdf_path": null`,
`verified.id_resolves: false`; its own `why` concedes it is "selected provisionally with a
verification flag." goal.md §3 item 2 requires load-bearing entries (contrast is in the
digest-mandatory class per §1 lifecycle ②) to have a resolvable `digest_path`. `digest.md` N4
item 7 builds a limitation claim on it. The stage review flagged this honestly but still stamped
item 2 PASS. Do not let this reach Phase E prose; also all 8 core records have
`id_resolves: false` (no cached PDFs) — the flagged pre-E re-harvest is genuinely blocking, not
advisory.

### F-10 [NOTE] Phase-order deviation: Phase E/F/I artifacts exist with no Phase B/C/D behind them

`paper_draft.md`, `paper_draft.tex`, and a compiled `paper_draft.pdf` exist although `B_pilot/`,
`results/`, `verdicts.json`, and `claim_map.md` do not — goal.md's contract has Phase E consume
`claim_map.md`. Spot-grep found no fabricated result numbers (the draft frames everything as
"Expected outcome"/"Falsification condition" with targets, not findings), so this is a process
deviation, not data fabrication — but a compiled PDF of an unrun study is exactly the artifact
most likely to leak imagined results downstream. Mark the three files as pre-execution scaffolds
in `pipeline.md`, and note the two-way divergence: the draft's 7-RQ structure (incl. its
superior instrument-validation RQ1/RQ2/RQ7) vs. `paper.md`'s 3-H structure must be reconciled in
one direction before Phase B.

### F-11 [NOTE] Estimand is one sentence only by punctuation

`paper.md` Step 5's estimand does contain all four R1 elements (quantity: Δ-trust gap; unit:
per-method over verified replay-decisive tool-caused failures; population: three named
trajectory sources; decision: routing corrective effort), which satisfies R1's letter — but at
~95 words with two nested clauses it will not survive as the paper's one-sentence anchor.
Cosmetic; tighten during Phase E.

---

## Failure-space simulation (per-H walk-through)

**H1 fails, cleanly (Δ within ±10 pp, methods competent on overt):** F1 fires — verbatim,
specific, and the F-G1 pivot to a certification-benchmark paper is pre-written. Would the pivot
paper survive review? Mostly: the suite (Claim 2) survives independently of H1, and F-G1's
"isolating which corruption types still evade which method class" gives it content. Gap: as an
A3 paper it would face the A3 kill list (contamination analysis, headroom, maintenance
statement) — none budgeted. Survivable but thin; pre-declare the A3 evidence add-ons in F-G1.

**H1 fails because methods flunk overt errors (m_A(D_overt) > 40%):** UNCOVERED — see F-5(1).
This is the branch most likely to actually occur if the Who&When judges are as weak on real
logs as their own paper reports (their all-at-once accuracy is low). Highest-priority fallback
gap.

**H1 passes for exactly 3/5 methods after an A5 baseline drop (denominator 4):** the "≥3 of 5"
aggregation with a shrunk denominator is noted in A5's consequence ("weakens the evidential
weight") but the binary rule for 4 or 3 remaining methods is not restated — is it ≥3 of 4? ≥2 of
3? Pre-commit the majority rule as a fraction, not an absolute count.

**H2 fails / underpowered:** F2 fires — but at n=50 the test has ~51% power (F-4), so F2 would
frequently misreport a true skew as "directionally diffuse." F2's wording is otherwise good
(names the alternative geometry as "a distinct and reportable failure geometry"). H2b failure:
uncovered (F-5(2)).

**H3 fails (no reduction):** F3 fires — genuinely strong fallback: the C3
counterfactual-deficit interpretation is itself the more interesting finding ("cheap prompt
fixes are ruled out"), and the second branch (reduction + FPR inflation: "trust is a dial, not a
switch") is pre-written. Wrong-direction (license increases misattribution): uncovered
(F-5(4)). A6 failure path (control set contaminated/thin → FPR clause INCONCLUSIVE) is properly
pre-declared.

**B-alt kills the mechanism (agent-side ≈ tool-side):** covered — "F3-style capability wording
takes over the mechanism claim"; Claims 3/4 survive as phenomenon claims, Claim 5 falls;
matches guidance situation 3.

**All-fail (H1+H2+H3 all fail):** F-G1 covers it *if* the suite construction succeeded
(skeleton G1/G2 passed). If G1 or G2 fails, A1/A2 block pre-scale — the paper dies cheaply at
the skeleton, which is acceptable and correctly designed.

**Is there any outcome that leaves the paper with nothing?** One: the incompetent-on-overt
branch combined with a saturating constant-attributor floor (judges ≈ always-plan on
everything). No pre-committed wording exists, F-G1 is unusable, and the honest residual — "the
attribution layer is broadly unreliable" — is publishable but unregistered, so it would have to
be improvised at verdict time, which is exactly what pre-registration forbids. Add F0 (F-5).

---

## Missing RQs / reviewer questions the design cannot currently answer

1. **Are human annotators fooled too?** (F-8) — the design collects the data and never asks.
   Direct implication for the validity of Who&When's own labels and MAST's taxonomy.
2. **Does the gap close with judge capability?** t3 crosses model *family* but no capability
   axis (weak vs. frontier judge). A reviewer will ask "is this just a weak-judge artifact that
   GPT-next fixes?" One extra judge tier per framework answers it.
3. **Detection vs. attribution decomposition:** does the judge ever *flag* the corrupted
   observation as suspicious yet still blame the plan? Separates "never noticed" (C1) from
   "noticed but overrode" — cheap to log from judge rationales, sharpens the C2-vs-C3 mechanism
   story beyond the single trust-license bit.
4. **Sensitivity to the plausibility-screen threshold (0.8/0.5 cutpoints)** — currently a magic
   constant defining the "subtle" construct (F-2).
5. **What would B0-null even look like?** (F-1) — currently unanswerable, and it is the first
   question goal.md §5 asks.
6. **Δ stratified by fault-to-manifestation distance** (F-6) — the referee's first rival
   explanation for the headline number.

---

## Reliability audit of prior Phase A PASS

Independently re-verified items 2, 4, 5, 6 (the ones most likely rubber-stamped), plus record
spot-checks:

- **Item 1 (digest self-verification): HELD.** Spot re-checks of N4→N3 `affects_works`, N6→N5,
  N8 cross-refs, and the N12 `absence_comment` (now present) all confirm the recorded state.
- **Item 2 (cache integrity): PARTIALLY RUBBER-STAMPED.** The review deserves credit for
  *finding* the major gap (8 load-bearing works absent from the cache) and fixing it same-day.
  But it then stamped PASS while: all 8 added records carry `verified.id_resolves: false`;
  MAST (`selected`, load-bearing `contrast` class) has `digest_path: null` with content
  self-described as from memory; and the mandated live fetch spot-check of the new records was
  "blocked by OpenReview's bot-verification gate... inconclusive." Under goal.md §3 item 2's
  binary wording ("load-bearing entries have resolvable digest_path; spot-check 2–3 ids by
  fetching"), this is REVISE-with-blocking-action-item, not PASS-with-residual. The three
  spot-checks it did run (pdftotext on 2606.30449, 2512.22894, one rejected record) were real —
  I re-verified all three `selected` harvest records' `digest_path`/`pdf_path` resolve on disk,
  and all 10 non-MAST `digest_path`s resolve (7 manual digests exist in
  `discussion/refs_manual/`).
- **Item 4 (claim–evidence orphans): MOSTLY HELD, one miss.** All 6 claims trace to an H-id or
  design definition. Miss: Claim 4 is marked "fallback-covered (F2)" but its H2b half
  (type-dependence) has no covering fallback — F2's wording addresses direction only.
- **Item 5 (seven-slot completeness): RUBBER-STAMPED for H2b.** The recorded claim
  "H1/H2/H2b/H3 each fill guidance.md §3.1's seven slots" is false for H2b: it has no
  effect_floor (any LRT-significant predictor counts, no magnitude) and no verbatim fallback.
  H1/H2/H3 do genuinely fill all slots (verified slot-by-slot), and the A1–A7 consequence
  column the review added is real and well-differentiated (block/degrade/restrict-scope).
- **Item 6 (Part 6 self-check): RUBBER-STAMPED on two sub-items.** The recorded audit lists
  items 2, 4, 5, 8, 9, 10 and fixes for 1 and 7 — **Part 6 item 6 (every instrument has a
  5-step R2 plan with acceptance threshold) was never checked at all**, and it fails in fact:
  the plausibility screen has no R2 plan (F-2). Item 9 ("power stated per cell") was passed by
  citing sample-size minima (≥50 cases, ≥15/cell) that are not power statements; the ≥50
  minimum yields ~51% power for H2's own criterion (F-4). Item 5's "placebo (B0)... present"
  also passed a B0 that contains no null-by-construction arm (F-1) — the Part 2 A2 evidence
  standard ("a placebo arm whose effect must be null") is not met by the plan.
- **Reference spot-checks (cross-topic contamination): CLEAN.** Sampled `2601_00042`,
  `2606_30449`, `2512_22894` and the 8 core records: every `why` is specific to B2.5's
  attribution-under-corruption estimand (no imported rationale from another topic); the two
  method-twin `why`s correctly concede shared machinery (Who&When's judge protocol,
  AgenTracer's replay) and state the delta. 147 rejected records retained in-file per the
  lifecycle rule; no `pending` verdicts.

**Net:** the prior PASS is *partially* reliable — its cross-reference and tag-discipline checks
were real work and its cache-gap discovery was genuine, but the gate decision itself was
generous: at least three sub-checks (R2-per-instrument, power-per-cell, placebo presence) were
stamped without being performed against the actual standard, and each hides a substantive
design defect found above.

---

## Overall: NEEDS-REVISION

The core idea survives adversarial reading: the asymmetry is genuine and directional, the
twin-replay ground truth is the right construction, B-alt is the correct strongest rival with a
budget-matched arm, and the taste audit's clean verdict is deserved. The defects are all in the
verification machinery the pipeline itself claims to enforce — which is repairable now, before
compute.

**Three highest-leverage fixes:**

1. **Make B0 a real placebo (F-1):** add the sham-injection arm and label-shuffle analysis
   placebo with pre-committed null/equivalence criteria, so goal.md §5's "placebo first" gate
   has an operational meaning and a pipeline artifact cannot masquerade as the headline Δ.
2. **Close the two biggest fallback holes (F-5):** pre-commit F0 for the
   methods-incompetent-on-overt-errors branch (the single outcome that currently leaves the
   paper with nothing) and give H2b an effect floor + fallback; add the two wrong-direction
   sentences and explicit fallback-combination rules.
3. **Validate the instruments and the power they feed (F-2, F-4, F-3):** promote the draft's
   screen-validation RQ into `paper.md` as a skeleton gate with an R2 acceptance threshold;
   raise E2's conditional minimum to a powered n (~120–150) with the 50–120 band INCONCLUSIVE;
   and either narrow the estimand's framework population or extend the skeleton with
   per-framework smoke tests so "config-not-code" is demonstrated rather than asserted.

---

## Fixes applied (2026-07-04)

Direct edits authorized post-review; one line per edit. No results or validation numbers were
fabricated — all thresholds below are pre-registered acceptance targets; the only computed
numbers are power calculations (exact binomial, reproducible).

1. `paper.md` Mandatory baselines — added **B0-placebo** with two null-by-construction components: (i) sham-injection arm (identity mutation through the full injection→replay→serialization machinery, TOST equivalence margin ±3 pp per layer share) and (ii) label-shuffle analysis placebo (1,000 within-pair permutations, permuted Δ centered on 0), frozen with skeleton thresholds and wired as the Phase D step-1 check before any H\* verdict (closes F-1).
2. `paper.md` B0 bullet — added the explicit statement that neither overt arm nor constant attributor carries a null prediction, routing the placebo job to B0-placebo and the premise-collapse outcome to F0 (closes F-1's inoperable-gate half).
3. `paper.md` E1 — added **Fallback F0** (verbatim, premise-collapse branch): fires at m_A(D_overt) > 40% for ≥3 of 5 methods; the overt-error failure rate becomes the headline (competence audit anchored on the constant-attributor floor, suite released as the entry bar); H1 unscoreable, F1/F-G1 explicitly marked unusable; combination rule: F0 pre-empts F1/F-G1, E2/E3 verdicts INCONCLUSIVE (closes F-5(1)).
4. `paper.md` F-G1 — added a **Scope of F-G1** paragraph restricting it to the robust-and-competent cell and deferring the premise-collapse cell to F0 (completes F-5(1)).
5. `paper.md` E2 — replaced the ≥50-case conditional with an **honest power statement** (~0.51 power at n=50 for π_plan=0.65; ~0.89 at n=120, critical count 72/120) and pre-declared bands: ≥120 scored, 50–119 INCONCLUSIVE (F2 does not fire), <50 descriptive (closes F-4).
6. `paper.md` E2 — added **Fallback F2b** (verbatim, H2b type-dependence failure) with the F2×F2b four-cell combination note (closes F-5(2) and the item-4/5 H2b orphan).
7. `paper.md` — added new section **"Instrument validation: the plausibility screen (guidance.md R2, 5 steps)"**: grounding in the cache's corruption literature, held-out calibration set (50 pass + 50 reject) with named merge/split ops, 2 independent human raters with acceptance κ ≥ 0.7 / ≥90% gate-passing plausible / <60% gate-rejected, confusion-structure inspection confined to the borderline band, freeze-by-hash before scale plus a 0.7/0.9 cutpoint sensitivity analysis; situation-7 failure path pre-declared (closes F-2, promoted from stale paper_draft.md RQ1 into the binding spec).
8. `paper.md` Step 9 — extended the walking skeleton with **framework reach** (1 full injection→replay cycle on GAIA; 1 twin-replay determinism attempt on a Who&When-logged trajectory — the known likely breaker, now exercised), gate **G5** (screen R2 validation inside the skeleton) and gate **G6** with a pre-committed narrowing rule: Who&When replay failure narrows the estimand population to AgentDojo + GAIA and demotes Who&When to a stated stretch arm / M6(b) control source, recorded in pipeline.md before scaling; pass criterion updated four→six gates, cost updated to include smoke runs + ~200 rater judgments (closes F-3).
9. `paper.md` Step 5 estimand — added the parenthetical binding the population to the G6 narrowing rule (envelope honesty for F-3).
10. `paper.md` Claim–Evidence Map — rows 3/4/6 updated: row 3 gains B0-placebo validity gating + F0 branch, row 4 splits fallback coverage into F2 (direction) / F2b (type), row 6 gains F0 coverage for the failure branch (map consistency with edits 1–6).
11. `digest.md` N6 M1 — added the screen-validation clause referencing paper.md's R2 plan (κ ≥ 0.7, freeze-by-hash) so the digest no longer describes an unvalidated instrument.
12. `digest.md` N6 M6 — "Three controls" → "Four controls": added (d) the sham-injection placebo as a null-by-construction validity arm referencing paper.md B0-placebo.
13. `digest.md` N8 analysis plan — RQ_INF_1 updated to the ≥120-case scoring threshold with the honest power figures (~0.89 at 120, ~0.51 at 50) and the pre-declared INCONCLUSIVE/descriptive bands, aligned with paper.md E2.

**Not fixed here (needs human, network, or compute):** F-7 re-harvest with method-name angles + PDF caching for the 8 core records and primary-source verification of MAST (needs live fetch; OpenReview was bot-gated in this environment); F-9's `id_resolves: false` flags (same); F-6 fault-to-manifestation-distance stratification and F-8's human-annotator hypothesis H4 (design additions beyond the authorized fix list — recommend before Phase B); F-10 reconciliation of the stale 7-RQ paper_draft.\* with the revised paper.md (Phase E rerun); F-11 estimand sentence tightening (cosmetic, Phase E). Taste-audit currency: today's edits do not touch the Step-0 asymmetry statement or Step-5 definitions' substance, so goal.md §3 item 8's re-audit trigger does not fire.
