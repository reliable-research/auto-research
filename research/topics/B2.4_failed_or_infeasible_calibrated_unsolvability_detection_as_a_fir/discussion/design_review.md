# Design Review (adversarial, 2026-07-04)

Reviewer stance: skeptical senior PC member; the recorded "Phase A (re-run) PASS" in
`discussion/stage_review.md` was NOT trusted — every claim relied on below was re-verified
against file contents on disk (`README.md`, `digest.md`, `paper.md`,
`discussion/reference_candidates.jsonl` (158 records), `discussion/refs/`,
`discussion/pipeline.md`, `discussion/stage_review.md`, `discussion/taste_audit.md`,
`discussion/paper_draft.md`).

**Staleness note (stated once):** `discussion/paper_draft.md` / `.tex` / `.pdf` are dated
2026-07-04 13:38–13:41, *before* the Phase-A fixes applied to `paper.md`/`digest.md` at
~19:26 (estimand line, PG-gates, H1 alpha/aggregation, R7 subsection, κ strengthening).
The draft's 6-RQ structure also does not match `paper.md`'s 3-RQ/4-H structure. Findings
below are scored against `paper.md` (the spec of record), not the stale draft.

## Verdict summary

| Dimension | Score | One-line reason |
|---|---|---|
| 1. Feasibility & scale | FIXABLE | Data sources real/public, costs estimated and small; but "config-not-code" scale-up is overstated (each new domain needs a new oracle + operator code), and the AgenTracer-style trained-tracer baseline has an unstated availability/training-data dependency |
| 2. Soundness | FIXABLE | Strong H/A machinery, but B0 is NOT null-by-construction (no placebo arm exists at all, and B0's expected non-null result mechanically collides with goal.md §5 step 1); H3 has an uncorrected 5×4 selection; the leakage probe — the load-bearing validity instrument — has no R2 plan of its own; benchmark-memorization confound unnamed |
| 3. Novelty & pre-emption | FIXABLE | Estimand (third-party attribution FBR/CoR + calibration boundary vs certified unsolvability) is genuinely un-pre-empted in the cache; but the harvest never covered the "infeasible-task agent benchmark" axis (WebArena-unachievable / OSWorld-infeasible / BFCL-irrelevance style), which is the nearest reviewer-known precedent family |
| 4. Hypothesis→fallback robustness | FIXABLE | Every H has floor + verbatim fallback; but wrong-direction H2 (CoR>FBR) has no pre-committed wording, the all-domains-fail-H4 corner leaves the paper with no pivot (F-G1 explicitly "requires H4 to pass"), and the F3×B-alt combination rule has an undefined middle zone |
| 5. Method scope & RQ design | FIXABLE | A2 mandatory shapes mostly present (grid, rival arm, mechanism analysis) — except the placebo arm; missing RQs a reviewer will demand: base-rate/prompt-prior rival, memorization/contamination arm, adversarially-trained leakage probe |
| 6. Prior-work reliability | PARTIALLY RELIABLE | Cache integrity fix is real and verified on disk; but Phase-A items 5/6/9 were partially rubber-stamped (H3's missing alpha/correction slot, no R2 plan for the probe or oracle, per-cell power only at headline level, B0 checked for *presence* not for placebo *function*) |

**Overall: NEEDS-REVISION** (see end for the 3 highest-leverage fixes).

---

## Findings (ranked most-severe first)

### F-1 [BROKEN] There is no null-by-construction placebo arm, and the design's "B0" contradicts goal.md's mechanical verdict procedure

Evidence: `paper.md` Step 6 Mandatory baselines defines B0 as "the **label-space-restricted
attributor** that can only output {success, agent_failure} ... Expected `FBR ≈ 1.0` on
unsolvable members by construction." guidance.md §3.3 requires B0 to do "**Two jobs in one
arm**: (a) the current-practice arm ... (b) a **null-by-construction placebo** (shuffle
labels/years/assignments) **whose effect must be null**." The spec implements job (a) only.
Worse, goal.md §5 step 1 is mechanical: "**Placebo first.** B0 non-null → run invalid ...
Never score RQs from an invalid run." This design's B0 is *expected to be maximally
non-null* — a literal execution of Phase D would invalidate every run, or (more likely)
the executor would silently skip the placebo gate, which is exactly the failure the gate
exists to prevent. And since attribution baselines in the Who&When formulation are handed
*failed* trajectories, B0's FBR = 1.0 is tautological — it is an argument dressed as an
arm, providing zero pipeline-artifact detection.

Think-hard check requested by the review brief: would B0 "actually come out null if the
pipeline is clean"? No — it cannot come out null under any pipeline state, clean or
broken. It therefore detects nothing.

**Fix (cheap, concrete):** add a true placebo arm B0-p: (i) shuffle oracle labels within
domain and require measured FBR−CoR gap ≈ 0 and AUROC(c) ≈ 0.5 (CI covering 0.5); and/or
(ii) run the full battery on sham pairs (a semantically inert mutation applied to a
solvable task, both members solvable) and require the "directional bias" to vanish.
Rename the current B0 to a design-argument control (B-def) and rewire Phase D step 1 to
gate on B0-p. Pre-commit: B0-p non-null → run invalid (situation 1).

### F-2 [FIXABLE] Benchmark-memorization is an unnamed rival that the leakage audit cannot catch

Evidence: the domains are "Spider 1.0 ... BIRD ... BFCL v3 ... τ-bench ... Terminal-Bench"
(`digest.md` N8 datasets) — all famous, all plausibly in every attributor/agent backbone's
training data. A mutation that "drop[s] the schema column ... the reference solution
requires" (`digest.md` M1) is detectable by *diffing against the memorized original*: an
LLM judge that recognizes the Spider `concert_singer` DB and notices a missing column can
flag "unsolvable" (or "anomalous") with no feasibility reasoning at all. The M6 text-only
probe does not control for this: probe AUROC < 0.60 with one probe model says nothing
about what a backbone that memorized the source benchmark can detect, and the direction of
the artifact (suppressing FBR, inflating apparent discrimination AUROC) directly
contaminates H1–H3. No R3 one-liner names this confound; `paper.md`'s R3 list covers
harness, wording, and circularity confounds only. A2's kill list ("year/condition
confounded with composition") and A3's ("no contamination analysis") both apply.

**Fix:** add a contamination arm: (i) schema/tool/entity renaming (surface-anonymized
variants) with pre-committed interpretation — if FBR/AUROC shift materially under renaming,
the memorization rival wins for that domain; (ii) require the text-only probe family to
include the same backbone family as the strongest attributor.

### F-3 [FIXABLE] The strongest rival to "directional bias = label-space/prompt design" may not be B-alt's information-limit, but base-rate prior mismatch — untested

Evidence: `paper.md` names B-alt's rival as "the traces on unsolvable tasks simply contain
no recoverable feasibility signal." But a boring explanation for `FBR − CoR ≥ 0.10` exists
that B-alt does not touch: a rational judge calibrated to deployment reality (where nearly
all tasks are solvable) *should* be reluctant to emit `unsolvable` under a 50/50 benchmark
prior — the "bias" would then be prior mismatch, curable by one prompt sentence stating
the base rate, not evidence that "unsolvable must become a first-class ... attribution
outcome" (Step 5 estimand's decision). The declared prompt-search protocol (`paper.md`
Reporting protocol: "≥3 paraphrased variants") covers wording, not base-rate disclosure —
paraphrases will share the missing prior. A reviewer's first question will be "did you
just measure an uninformed prior?"

**Fix:** add a budget-matched B-alt2 arm: identical judge prompt + explicit base-rate
disclosure (and/or explicit permission emphasis), with pre-committed downgrade wording:
"if disclosure alone closes ≥ half the FBR−CoR gap, the finding downgrades from
structural label-space bias to prior/prompt miscalibration; Claims 4 and 7 fall, Claims
1–3 and 5 survive."

### F-4 [FIXABLE] Fallback space has three uncovered corners

Evidence, walking each corner (full simulation in the next section):
1. **Wrong-direction H2** (CoR − FBR ≥ 0.10, i.e., systems over-refuse): H2's fallback
   text — "attribution systems are *symmetrically* miscalibrated on the feasibility axis
   (both directions non-trivial)" (`paper.md` RQ1 Fallback) — is factually wrong wording
   for a significant reverse gap, and guidance situation 4 ("Effect in the WRONG direction
   ... report it at full prominence") has no pre-committed sentence here.
2. **H4 fails everywhere**: F-G1 "(Requires H4 to pass so the instrument itself is valid)"
   (`paper.md` Global fallback). If every domain's operators leak irreparably, H1–H3 rates
   are invalid, F1/F2/F3 wordings (all built on measured rates) are unusable, and F-G1 is
   barred. H4's own fallback only covers per-domain narrowing ("narrowing the headline to
   passing domains"). The all-fail corner leaves the paper with only an implicit
   "leak-free injection is infeasible" story — publishable as S9 only with a power/effort
   argument that is nowhere pre-registered (how many repair iterations, how strong a
   probe, before "infeasible" is licensed?).
3. **F3 × B-alt middle zone**: B-alt branches at probe "cannot exceed AUROC 0.60" (rival
   wins) vs "clears 0.65" (rival ruled out) — probe AUROC ∈ [0.60, 0.65) has no
   pre-committed interpretation, and F3's text ("trace-level evidence is provably
   insufficient ... information-theoretic ceiling reached") is licensed *only* by the
   probe failing, but F3 as written fires on H3 failing alone; the F3/B-alt combination
   rule is not written down, violating §3.1's "write the fallback-combination rules too."

**Fix:** (1) add a verbatim wrong-direction sentence for H2 (over-refusal finding at full
prominence); (2) add a second global pivot F-G2 for the H4-all-fail corner ("mechanically
leak-free unsolvability injection is harder than assumed; we characterize which operator
families leak and why" — with a minimum-probe-strength and repair-budget pre-commitment
that makes the negative result credible); (3) write the explicit F3×B-alt truth table
including the [0.60, 0.65) zone (pre-declare INCONCLUSIVE for the mechanism claim).

### F-5 [FIXABLE] H3 is an uncorrected best-of-20 selection

Evidence: H3 requires "For **≥1** baseline in **each** of the ≥4 domains, `AUROC(c, ...)
≥ 0.65` with 95% bootstrap CI lower bound `> 0.50`" (`paper.md` RQ1). Per domain this is a
max over 5 baselines — 20 baseline×domain tests total — with no multiplicity control
(contrast H2, which carries "Holm–Bonferroni-corrected across the 5 baselines"). Under the
null, the chance that the best of 5 independent-ish AUROCs has a CI clearing 0.50 in a
given domain is far above 0.05. H3 as pre-registered can pass by selection noise.

**Fix:** either pre-specify the single baseline whose AUROC is tested per domain (e.g.,
the H2-winning strategy, chosen on a disjoint split), or Bonferroni/Holm-correct the
per-domain CI level across the 5 candidate baselines (CI level 1−α/5).

### F-6 [FIXABLE] The load-bearing validity instrument — the text-only leakage probe — has no R2 validation plan and no strength requirement

Evidence: `digest.md` M6(b): "a classifier (LLM prompted with the task text alone ...)
should perform near chance." No probe model is named, no requirement that it be the
strongest available reader, no calibration/validation of the probe itself. Yet H4 (a
*hard gate* on every headline number) passes exactly when this probe is weak — a weak
probe rubber-stamps leaky pairs. goal.md §8: "asserted numbers without protocol are
treated as absent"; guidance Part 6 item 6 requires "the 5-step R2 plan with an acceptance
threshold" for *every* instrument. `stage_review.md` item 6 claims this item fixed, but
the fix only added κ≥0.70 to the *human audit*; the probe (and the oracle M2, which gets
only the falsification-style PG-1 check) received no R2 treatment. Same gap class: PG-1's
detection ("run the strongest available agent + a bounded exhaustive/tool-search on every
`t⁻`") is a one-sided, low-power test precisely in the domain where static no-substitute
certification is weakest — Terminal-Bench, where "no substitute" over an open shell action
space is not statically decidable in general (a deleted file can be regenerated, fetched,
or reconstructed).

**Fix:** (i) name the probe protocol: strongest available backbone + a *trained*
discriminator fine-tuned on a disjoint calibration slice of pairs (the honest adversary),
freeze both before scale (R2 step ⑤); (ii) for M2, restrict Terminal-Bench operators to a
closed sub-language where no-substitute is decidable (e.g., resources outside any
reachable recovery path), or demote Terminal-Bench to an exploratory domain outside
headline claims.

### F-7 [FIXABLE] "Config-not-code" scale-up is overstated; per-domain oracle/operator construction is real code

Evidence: Step 9 pass criterion: "scaling to 600 pairs × 4 domains × 3 agents × 5
baselines is a *config change* (add source tasks, operator types, backbones, baseline
adapters), not a code change to the harness (M3), oracle interface (M2), or scorer (M5)."
But M2 itself says the oracle is "schema-graph reachability for SQL; tool-signature
coverage for function calling; environment-state assertion for τ-bench / Terminal-Bench"
— three different static-analysis engines. The skeleton exercises only "Spider, single
missing-column operator" (Step 9). Adding τ-bench/Terminal-Bench means writing new oracle
backends and operator libraries — engineering, not configuration. goal.md §8's gate
("scale-up is config, not code") will either fail honestly at Phase B or be gamed by
classifying new oracle backends as "operator types."

**Fix:** re-scope the skeleton's config-not-code claim to *within-domain* scaling, and
pre-register a per-domain "oracle bring-up" milestone (each new domain must pass PG-1/
PG-2/PG-5 at 20-pair scale before contributing) — this is the honest version of the same
gate and matches how A2's freeze-before-scale discipline is supposed to work.

### F-8 [FIXABLE] AgenTracer-style trained-tracer baseline: availability and training-data circularity unstated

Evidence: the baseline battery includes "an AgenTracer-style trained tracer where its
label space is extended with 'unsolvable'" (`digest.md` M4b). AgenTracer is an OpenReview
submission (cache record has `pdf_path: null`, `id_resolves: false` — no artifact
verified); reproducing its RL-trained tracer requires its counterfactual-replay
supervision pipeline (expensive API replay per trajectory) plus new `unsolvable`-labeled
training data — which can only come from this paper's own pairs, requiring a
train/eval split that is nowhere pre-registered (leakage risk into H2/H3), or from
nothing. The "<100 GPU-hours" feasibility line (`digest.md` N6 feasibility) prices the
fine-tune but not the supervision generation. guidance Part 5: "a baseline you can't run
gets a stated reason in the paper, not silence" — there is no pre-committed
can't-run wording, and A4/PG-4 only covers label-space incompatibility, not
non-reproducibility.

**Fix:** pre-register (i) the pair-level train/eval split for any trained component
(tracer and B-alt probe share this need — B-alt's "trained/calibrated on the oracle
label" also has no split protocol in `paper.md`, only in the stale draft's RQ4
"held-out instances" wording); (ii) the fallback: "if the tracer cannot be reproduced
within budget X, the battery is 4 baselines and every '≥3 of 5' vote rule becomes
'≥3 of 4', stated in the paper with the reason."

### F-9 [FIXABLE] FBR vs CoR compares asymmetric conditioning populations; the analysis plan's power claim mis-counts the CoR denominator

Evidence: `FBR = P(ŷ=agent_failure | y=unsolvable)` conditions on *all* unsolvable
members; `CoR = P(ŷ=unsolvable | y=solvable ∧ π did not succeed)` conditions only on
*failed* solvable members (Step 5 table). Two consequences: (a) the failed-solvable set's
composition depends on agent competence (A3 allows success up to 0.90) — the hardest
solvable tasks dominate it, and their traces most resemble unsolvable ones, inflating CoR
in a competence-dependent way; this composition confound has no R3 one-liner. (b) the
power statement "with n ≈ 1,800 per class, power > 0.9 for a 10-pp gap" (`digest.md`
analysis plan) is wrong for the CoR class: at a 0.90 success rate, failed-solvable n can
be ~180 pooled (per-domain far less), not 1,800. Guidance Part 6 item 9 ("power stated
per cell") is met only nominally — the INCONCLUSIVE rule exists, but the headline power
computation itself rests on a mis-stated n.

**Fix:** recompute power with CoR's n as a function of the A3-allowed success-rate range
(worst case 0.90); if per-domain CoR cells can drop below the powered minimum, either
tighten A3's upper bound (e.g., 0.85) or pre-declare the per-domain directional test
INCONCLUSIVE when failed-solvable n < n_min; add an R3 line naming the composition
confound and (ideally) report CoR stratified by t⁺-difficulty.

### F-10 [FIXABLE] Pre-emption sweep never covered the "infeasible-task agent benchmark" axis

Evidence: the 158-record cache (verified on disk) contains no entry for the family of
agent benchmarks that already include infeasible/unachievable tasks scored by whether the
agent declares impossibility — the WebArena "unachievable task" split, OSWorld's
infeasible-task subset, and BFCL v3's irrelevance-detection split (the latter acknowledged
only in a `digest.md` dataset parenthetical: "its existing irrelevance-detection split is
the closest natural precedent" — and never confronted in `paper.md` or the Related Work
plan). My keyword sweep of all 158 records (`infeasib|unsolvab|unanswerab|abstain|refus|
impossib|OSWorld|irrelevance`) confirms the harvest angles were attribution- and
QA-abstention-shaped; the *agent-benchmark-with-infeasible-split* angle was never queried.
guidance Part 5: "the harvest was inadequate, not the field empty. Re-harvest from new
angles ... before claiming novelty." The claimed contribution "the first
construction-guaranteed instrument" (F-G1 pivoted abstract) and "we produce the first
number" (Step 2b) are exactly the sentences this precedent family threatens. The
differentiation likely survives (third-party post-hoc attribution over traces + matched
pairs + calibration boundary ≠ first-party task-time detection on unmatched instances),
but it must be established, not assumed.

**Fix:** re-harvest with the missing angles ("infeasible tasks benchmark", "unachievable
tasks web agents", "irrelevance detection tool calling", "impossible task refusal
agent"); add the strongest hits as `contrast`/`baseline` entries; add a
concede-and-differentiate paragraph and soften "first" claims to the estimand actually
un-pre-empted (third-party attribution FBR/CoR + calibration boundary).

### F-11 [NOTE] Digest promises a cross-domain threshold-transfer analysis that paper.md never pre-registers

Evidence: `digest.md` N8 RQ1 answered_by_experiment ends "...and cross-domain threshold
transfer"; N10 t2's mitigation promises "an explicit held-out-domain threshold transfer
analysis and state its result even if negative." `paper.md` Step 6 contains no such
hypothesis, metric, or analysis line. Not claim-map-orphaned (no claim depends on it),
but a digest→spec dangling promise a reviewer of the pre-registration would catch.

**Fix:** either add it to RQ1's secondary analyses with a pre-committed reporting
sentence, or delete the promise from N10 t2 at the next permitted digest edit.

### F-12 [NOTE] Minor bookkeeping defects in the audit trail

- `stage_review.md` Phase A header: "158 records post-upgrade: 150 harvested + 9
  backfilled" — arithmetic is 150 + 8 new + 1 merge; `pipeline.md`'s phase log states it
  correctly ("150 harvested + 8 backfilled ... KnowCapable merged").
- `stage_review.md` gate result says "Two REVISE-level findings fired (checklist items 2,
  5, 6 ...)" — three items are listed.
- goal.md §0 resumability requires "input-file hashes per phase"; `pipeline.md` concedes
  "recorded qualitatively, not as literal hashes." Honest, but the contract is unmet.
- digest N3 keys (`[AgenTracer, OpenReview:l05DseqvuD]`) and cache keys (`AgenTracer05D`)
  match only via `ids`, not string-for-string; tolerable but the goal.md §1 consumption
  rule ("N3 cites only `selected` keys") is satisfied by resolution, not by key equality.

---

## Failure-space simulation (per-H walk-through)

Setup: H1 (pilot FBR ≥ 0.20, CI-LB > 0.05), H2 (FBR−CoR ≥ 0.10 for ≥3/5 baselines,
Holm-corrected), H3 (AUROC ≥ 0.65 CI-LB > 0.50 for ≥1 baseline per domain + non-1:1
risk–coverage), H4 (leakage gate, hard). Controls: B0 (definitional, see F-1), B-alt
(oracle-calibrated ceiling probe). Global pivot F-G1 fires on H1 ∧ H2 both failing,
conditional on H4 passing.

| Outcome | Pre-committed path | Survives review? |
|---|---|---|
| H1 fails (FBR small) alone | F1: "off-the-shelf ... already separates ... at rate X untuned; the open problem is the residual tail / the harder domains," headline re-targeted to worst baseline/domain | Yes, honest per-domain measurement paper — provided H4 passed and the per-domain reporting was powered (it is, per domain) |
| H1 ∧ H2 fail | F-G1 benchmark pivot; pivoted abstract written verbatim in `paper.md` | Yes — a valid instrument + a "systems already handle it" negative result is an A3-shaped paper; requires H4 (see corner 2) |
| H2 fails, both rates non-trivial | F2 "symmetrically miscalibrated" | Yes |
| H2 fails **wrong direction** (CoR−FBR ≥ 0.10) | **UNCOVERED** — F2's "symmetrically miscalibrated (both directions non-trivial)" is the wrong sentence for a significant reverse gap; situation 4 demands full-prominence reporting with re-derived implications | No pre-committed wording exists (F-4.1) |
| H3 fails + B-alt probe fails | F3 information-ceiling claim + rival-wins branch | Yes — arguably the most interesting outcome; power statement makes the null credible |
| H3 fails + B-alt probe succeeds | Design-gap claim per B-alt's second branch — but F3's verbatim text contradicts it ("provably insufficient") if applied blindly at Phase D splice time | Combination rule not written (F-4.3); Phase D is supposed to be mechanical, and here it has two conflicting sentences to splice |
| B-alt probe AUROC ∈ [0.60, 0.65) | **UNCOVERED** middle zone | No pre-declared INCONCLUSIVE (F-4.3) |
| H4 fails one domain | Withhold domain, narrow headline, report operator-family leak finding | Yes |
| H4 fails **all domains** | **UNCOVERED** — F-G1 barred ("requires H4 to pass"), F1–F3 unusable (rates invalid), only a non-pre-registered "injection is infeasible" story remains | This is the one outcome that leaves the paper with nothing pre-committed (F-4.2) |
| B0 FBR not ≈ 1.0 | "the whole framing is revisited" — no verbatim wording, and given B0's tautological construction this outcome is near-impossible, which is itself the problem (F-1) | The arm cannot fail, so it cannot detect anything |
| Placebo non-null (pipeline artifact) | **NO ARM EXISTS** to detect it | goal.md §5 step 1 has nothing to check (F-1) |

Bottom line: the mixed and clean-failure regions are well covered (better than typical);
the uncovered set is {wrong-direction H2, all-domains-H4-fail, F3×B-alt splice conflict,
absent placebo}. All four are cheap to close now and expensive to improvise later.

## Missing RQs / reviewer questions the design cannot currently answer

1. **"Is the 'bias' just an uninformed prior?"** — no base-rate-disclosure arm (F-3). The
   single most likely first-round reviewer question, and currently unanswerable.
2. **"Did the attributor recognize the mutated benchmark?"** — no memorization/
   contamination arm; famous-source mutation-diffing is undetectable by the current M6
   (F-2).
3. **"How strong is your leakage detector?"** — H4's gate is only as good as an
   unspecified prompted probe; a trained adversarial probe is the honest test (F-6).
4. **"Can humans do it?"** — no human-discrimination reference on a trace sample; without
   it, AUROC 0.65 has no anchor (is that near-ceiling or far below?). B-alt bounds
   trained-machine ceiling, not the human-analyst ceiling that debugging practice
   actually cares about (the estimand's stated decision consumer).
5. **"Does the calibration boundary transfer?"** — promised in digest N10 t2, absent from
   the spec (F-11).
6. **"Is your Terminal-Bench oracle actually sound?"** — static no-substitute
   certification over an open shell action space needs an argument, not just PG-1's
   low-power falsification search (F-6/F-7).

## Reliability audit of prior Phase A PASS

Independently re-verified (items chosen as most likely rubber-stamped: §3 items 4, 5, 6,
plus item 2's file-level claims):

**What held:**
- **Item 2 (reference-cache integrity)** — the described fix is real: 158 records on
  disk, 12 `selected`, 0 `pending`; all 12 selected records' `digest_path` resolve
  (verified programmatically), the 4 with local corpus PDFs and WhoWhen/MAST's
  `discussion/refs/*.pdf` all exist; the 6 OpenReview-only entries honestly carry
  `pdf_path: null` / `id_resolves: false` and the limitation is disclosed rather than
  hidden. Spot-checked 3 records (AgenTracer05D, WhoWhen0212, KnowCapable4661): `why`
  fields are specific to B2.4's constructs (B0 operationalization, label-space delta,
  M4c protocol) — no cross-topic contamination; the backfilled AgenTracer digest
  (`refs/l05DseqvuD.digest.md`) is transparently provenance-labeled ("built from the
  corpus's own proposal text ... not invented"). Sampled 5 random `rejected` records:
  rejection reasons are topic-appropriate, not boilerplate.
- **Item 1 (digest self-verification)** — spot-re-checked V-04's cross-reference claims
  (N4.affects_works ⊆ N3 keys; N8 mechanism/challenge/contribution sets): consistent.
- **Item 4 (claim–evidence orphans)** — re-walked all 7 claims: each traces to an H-id or
  a Step-5 definition; H1–H4 all have verbatim fallbacks. Holds *as stated* — but see
  the caveat below on what "fallback coverage" missed.

**What was rubber-stamped:**
- **Item 5 (seven-slot completeness)** — the recorded fix added alpha/aggregation to H1
  only. **H3 still has no explicit alpha/correction slot**, and its "≥1 of 5 per domain"
  aggregation is an uncorrected selection (F-5). "All seven slots ... now complete per
  #5" (`stage_review.md` item 6) is not supported by `paper.md`'s actual H3 text.
- **Item 5/§3.3 (B0 presence)** — "B0 + B-alt + F-G1 were already present and complete"
  checked *presence of a paragraph named B0*, not the §3.3(b) placebo *function*; the
  design has no null-by-construction arm at all, and its B0 semantics collides with
  goal.md §5 step 1 (F-1). This is the most consequential rubber-stamp.
- **Item 6 (R2 for every instrument)** — the fix added κ≥0.70 to the human audit only.
  The text-only probe (the H4 gate's instrument) and the oracle M2 have no R2 plan —
  no grounding, no calibration set, no acceptance threshold on the *instrument itself*
  (F-6). "Every instrument has the 5-step R2 plan" is asserted, not met.
- **Item 6/9 (power per cell)** — the INCONCLUSIVE rule was added, but the headline power
  computation itself mis-counts CoR's denominator (F-9); "power > 0.9" was accepted
  without re-derivation.
- **Fallback coverage** — item 4's "no claim is both unsupported and uncovered" missed
  the wrong-direction-H2 and all-domains-H4-fail corners (F-4), because coverage was
  checked per-H, not by simulating the joint failure space.

**Verdict on the prior PASS: partially reliable.** File-integrity and bookkeeping claims
check out on disk; the substantive method-rigor items (5, 6, 9, and §3.3 compliance) were
verified at the level of "a paragraph with the right heading exists," not at the level of
"the paragraph does the job the guidance assigns it."

## Overall: NEEDS-REVISION

The core idea is strong and un-pre-empted on its actual estimand, the taste audit's 🟢 is
defensible, the cost envelope is realistic for a small team, and the fallback machinery is
better than typical. But the spec as written would fail its own runbook at Phase D step 1
(no placebo to check), can pass H3 by selection noise, and gates all validity on an
unvalidated probe — these are exactly the defects that are cheap now and fatal after
compute is spent.

**Three highest-leverage fixes:**
1. **Restore the placebo function (F-1):** add a shuffled-label / sham-pair B0-p arm with
   a null-by-construction expected result, rename the current B0 to a design-argument
   control, and rewire the Phase D step-1 gate to B0-p. Without this the run has no
   pipeline-artifact detector and the goal.md verdict procedure is unexecutable.
2. **Add the two cheap rival arms (F-2, F-3) and harden the leakage probe (F-6):**
   base-rate-disclosure variant, schema-renaming contamination variant, and a named +
   trained text-only probe with an R2 plan — these three convert the paper's headline
   from "attackable in one reviewer sentence" to "pre-answered."
3. **Close the fallback corners (F-4, F-5):** verbatim wrong-direction H2 wording,
   an F-G2 pivot for the H4-all-fail corner with a pre-committed
   probe-strength/repair-budget standard, the F3×B-alt combination table (incl. the
   [0.60, 0.65) INCONCLUSIVE zone), and a multiplicity-corrected H3.

---

## Fixes applied (2026-07-04)

Direct edits authorized by the coordinator; applied to `paper.md` and `digest.md` only
(no results or validation numbers fabricated — all new numerals are pre-registered
design thresholds).

1. [F-1] `paper.md` Step 6: renamed "Mandatory baselines" → "Mandatory control arms"; added **B0-p** null-by-construction placebo (sham inert-mutation pairs + shuffled-label check; pre-committed null criterion: sham-gap 95% CI containing 0 and shuffled-label AUROC CI containing 0.5, per domain) as the explicit Phase D step-1 gate; relabeled the old B0 as **B0-a** current-practice arm with an explicit "not the placebo gate" note.
2. [F-1] `paper.md` A4: both "B0" references updated to "B0-a"; Claim–Evidence Map rows 6–7 updated to "B-alt1" (row 7 now names the three-branch rule and B-alt2/B-alt3 survival).
3. [F-1] `paper.md` Step 9: skeleton now includes 5 sham pairs for B0-p, computes the B0-p null criterion end-to-end, and runs the probe positive-control check; cost line updated (≈50 runs, $5–25).
4. [F-2] `paper.md` Step 6: added **B-alt2** memorization/contamination arm (surface-anonymized 20% pair subset per domain, oracle labels re-verified after renaming; pre-committed shift floors FBR ≥ 10 pp / AUROC ≥ 0.10 with CI excluding 0; downgrade wording: anonymized-variant rates become that domain's headline).
5. [F-3] `paper.md` Step 6: added **B-alt3** base-rate prior-disclosure arm (one added sentence disclosing the 50/50 prior; pre-committed downgrade wording if disclosure closes ≥ 50% of the FBR−CoR gap: Claims 4/7 downgrade, Claims 1–3/5 stand, recommendation shifts to feasibility-prior calibration).
6. [F-2/F-3/F-9] `paper.md` Step 5 R3 list: three new confound one-liners — surface anonymization vs memorized-diff, base-rate disclosure vs uninformed prior, CoR stratified by t⁺ difficulty vs asymmetric conditioning populations; fourth bullet updated to "B-alt1".
7. [F-6] `paper.md` Step 5: new "Instrument validation (R2)" subsection with full 5-step plans and acceptance thresholds for the **leakage probe** (named: strongest battery backbone prompted + trained discriminator on a disjoint 30% split; positive-control power requirement AUROC ≥ 0.90 on deliberately leaky pairs; freeze before scale; memorization blindness stated honestly) and the **oracle** (grounded in source verifiers; closed decidable operator sub-language for open-action domains like Terminal-Bench; ≥2-rater substitute-derivation audit at κ ≥ 0.70 on 10% of t⁻; repair-by-condition; hash-freeze).
8. [F-5] `paper.md` H3: explicit Alpha/multiplicity slot added — Bonferroni-corrected 99% CIs correcting the best-of-5-baselines selection within each domain (AURC separation at the same corrected level); an uncorrected-only pass does not count.
9. [F-9] `paper.md` RQ1 Verification: replaced the mis-counted "≥1,800 per class, power > 0.9" statement with honest CoR-denominator arithmetic (failed-solvable n ∈ ≈[180, 1,530] under A3; power > 0.9 only for n ≳ 400 under the conservative p≈0.5 bound; ≈0.8 at the A3 worst case, lower under Holm) plus a pre-declared realized-power rule: baselines below 0.8 realized power after Holm are INCONCLUSIVE and excluded from the "≥3 of 5" denominator with the exclusion stated.
10. [F-4.1] `paper.md` RQ1 Fallback: verbatim wrong-direction H2 wording added (CoR − FBR ≥ 0.10, Holm-corrected, ≥3/5 baselines → over-refusal finding reported at full prominence per guidance situation 4; headline shifts to H3 with the threshold adjustment reversed in sign).
11. [F-4.3/F-8-partial] `paper.md` B-alt1: pre-registered 30%/70% pair-level train/eval split protocol added, plus the three-branch decision rule with the [0.60, 0.65) / CI-straddling zone pre-declared INCONCLUSIVE; RQ1's H3 fallback made explicitly conditional on the B-alt1 branch ("never combine H3-failure wording with a B-alt1 branch it contradicts").
12. [F-4.2] `paper.md`: **F-G2** construct-validity pivot added for the H4-all-fail corner (licensed by the probe's positive-control power check; pivoted abstract written verbatim; one-repair-iteration budget fixed; leakage prevalence per operator family × domain becomes the finding; headline flips to CO1′).
13. [F-6] `digest.md` N6 M2/M6: mirrored the oracle R2 audit clause (κ ≥ 0.70 rater substitute-derivation check, closed decidable sub-language, hash-freeze) and the named two-reader probe with positive-control requirement and stated memorization blindness.
14. [F-1/F-5/F-9] `digest.md` N8 analysis plan: placebo-first sentence added (B0-p before any hypothesis, per goal.md §5 step 1); the "n ≈ 1,800 per class, power > 0.9" claim replaced with the corrected CoR arithmetic and realized-power INCONCLUSIVE rule; H3's Bonferroni-corrected 99% CI level recorded.
15. [F-2] `digest.md` N10: threat **t6** added (benchmark memorization / mutation-detection-by-memorized-diff) with the B-alt2 mitigation; N10 absence-comment updated (t1–t6) and self-verification V-10/V-11 count corrected (6 items, construct×3).

**Not fixed by these edits (needs human decision or compute):** F-7 (config-not-code
re-scoping of the skeleton pass criterion — left pending an executor decision on
per-domain oracle bring-up milestones), F-8's baseline-unavailability clause (the B-alt1
split now exists, but the "battery shrinks to 4 with stated reason if the
AgenTracer-style tracer cannot be reproduced" wording was not added), F-10 (re-harvest of
the infeasible-task-benchmark axis — requires a new harvest run), F-11 (cross-domain
threshold-transfer promise — still dangling between digest N10 t2 and paper.md), and the
stale `paper_draft.*` (now two revisions behind `paper.md`; regenerate at Phase E).
