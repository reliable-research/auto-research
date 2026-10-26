# Design Review (adversarial, 2026-07-04)

Reviewer stance: skeptical PC member; the recorded "Phase A (re-run) PASS" in
`discussion/stage_review.md` was **not** trusted — every item relied on below was re-verified
against actual file contents (`paper.md`, `digest.md`, `reference_candidates.jsonl`,
`pipeline.md`, `paper_draft.md`) and against on-disk paths.

Staleness note (stated once, per instructions): `paper_draft.md`/`.tex`/`.pdf` were written
2026-07-04 13:30; `paper.md` and `digest.md` carry Phase A fixes from 19:12–19:13. The draft
therefore predates the estimand, PG-* gate ids, R2/κ protocol, and power/thin-cell paragraph,
and is not penalized again below — but anything that exists **only** in the draft (notably the
contamination control) is treated as absent from the pre-registered spec, because Phase B/C
execute `paper.md`, not the draft.

## Verdict summary

| Dimension | Score | One-line reason |
|---|---|---|
| 1. Feasibility & scale | FIXABLE | GAIA/Who&When are real and named, costs estimated ($20–90 skeleton, low-$k full run), skeleton concrete and config-not-code stated — but temperature-0 replay reproducibility on live-tool GAIA-style tasks is the load-bearing bet, and its hard-failure path (PG-1) has no fallback beyond "redesign scaffold". |
| 2. Soundness | FIXABLE | Estimand present, A5 has a real 5-step κ≥0.7 R2 plan — but the shared (non-class-matched) no-op arm confounds per-class comparisons, trial dependence on ~200 base tasks is ignored by every test, and two instruments (δ_∅ generator, B0-b error-signal detector) have no validation plan at all. |
| 3. Novelty & pre-emption | FIXABLE | AgenTracer twin conceded honestly and differentiation is real (per-class certification + matched no-op control + released benchmark ≠ single-action injection for tracer training), but all 9 load-bearing references have `digest_path: null` and `id_resolves: false` — the pre-emption check is shallower than the recorded PASS claims. |
| 4. Hypothesis→fallback robustness | FIXABLE | Per-H verbatim fallbacks + pre-written F-G1 pivot abstract are genuinely good — but the plausibly-modal outcome (B0-b near ceiling ⇒ "no benchmark needed") has no routing, fallback-combination rules are absent, and H3's fallback promises an unbudgeted harder tier that violates the paper's own single-fault invariant. |
| 5. Method scope & RQ design | FIXABLE | Validity envelope stated in the estimand; A3 archetype shapes mostly present (headroom E3, IAA A5, baseline sweep E2) — but two A3 reviewer kills (contamination analysis, maintenance/versioning) are unaddressed in the binding spec, and corpus longevity under backbone-model deprecation is never confronted. |

**Overall: NEEDS-REVISION** (details and the 3 highest-leverage fixes at the end).

## Findings (ranked most-severe first)

### F1 [BROKEN] The plausibly-modal outcome — trivial heuristic near ceiling — has no pre-committed routing, and the two fallbacks that border it contradict each other

Evidence: `paper.md` B0-b: *"if this trivial heuristic already matches ground truth at ≥ 0.90,
attribution is symptom-reading and no benchmark is needed."* That sentence names a
premise-collapse outcome (guidance.md §3.3 B0 job (a): such an outcome *"must route to the
global pivot, not be buried"*) — but F-G1's trigger is only *"H1 fails on all classes"*.
If H1 passes and B0-b ≈ 0.95: H2 auto-fails (nothing can beat 0.95 by 0.10) and H3 fails
(best Acc > 0.90). H2's pre-committed fallback then reads *"current attribution methods do not
exceed a trivial surface heuristic … indicating those labels reward symptom-matching rather
than causal localization"* — which is factually wrong in that world (all methods, including the
heuristic, are *accurate*; the certified faults are simply easy). H3's fallback ("benchmark is a
competence certificate; we release a harder tier") is the right story, but see F4. No
combination rule says which wording wins.

This is not a corner case: the certification gate *selects* faults severe enough to flip
outcomes under k=4 replays, i.e. biases the corpus toward loud faults (an error-returning tool
stub is glaringly visible in the trajectory text), which is exactly the regime where a
last-step-before-error-signal heuristic thrives.

Fix: add a pre-registered branch "B0-b ≥ 0.90 on the certified tier" with its own verbatim
wording (severity-tiered corpus + the harder tier becomes the headline artifact, budgeted now),
and a one-line rule for which of H2/H3's wordings leads in each joint outcome.

### F2 [BROKEN] The recorded Phase A PASS on checklist item 2 is contradicted by the cache file itself

Evidence: goal.md §3 item 2 requires *"load-bearing entries have resolvable `digest_path`;
spot-check 2–3 ids by fetching."* goal.md §1 lifecycle ②: *"Digest every potentially
load-bearing candidate (`baseline`/`method-twin`/`contrast`)."* In
`reference_candidates.jsonl`, **all nine** load-bearing records the paper actually argues
against (WhoAndWhen2025 baseline, DoVer2025 + AgenTracer2025 + SelfEvolveBench2025
method-twins, CRM2025/FAPO2025 baselines, Defects4J2014 + the contrasts) carry
`"digest_path": null` and `"verified": {"id_resolves": false}`. `stage_review.md` admits this
(*"flagged honestly rather than fabricating a path"*) and records **"PASS after fix"** anyway —
an explicit requirement self-waived. Honesty about the gap does not convert a failed gate into
a passed one.

Independent re-verification (this review): the 8 OpenReview ids do exist in
`topics/corpus/ideas.jsonl` with matching titles (GazlTYxZss, mrEK16Jy6h, l05DseqvuD spot-checked),
so the records are not fabricated — but no external fetch and no per-paper digest was ever done,
which matters for novelty: the AgenTracer differentiation rests entirely on a proposal-extract
reading, not on the paper's actual method section.

Fix: digest the 4–5 genuinely load-bearing entries (WhoAndWhen, DoVer, AgenTracer,
SelfEvolveBench minimum) in extraction mode, set `digest_path`, fetch-verify ids, and only then
re-record item 2 as PASS.

### F3 [BROKEN] The contamination control credited by Phase A item 6 does not exist in the pre-registered spec

Evidence: `grep -in "contaminat" paper.md` → zero hits. The control exists only in the stale
`paper_draft.md` (line 89, "Contamination control" paragraph). `stage_review.md` item 6
nevertheless credits *"the pre-existing contamination control from the Stage 4 fix above"* as
satisfying the confound check, and its item-10 A3 evidence-standard claim leans on it. Since
Phase B/C execute `paper.md` (goal.md phase table: Phase B "Reads: `paper.md`"), a control that
lives only in prose the pipeline will later overwrite from `claim_map.md` is not pre-registered.
Memorized-solution familiarity is a named A3 reviewer kill ("no contamination analysis") and a
genuine rival explanation for LLM-judge accuracy on public GAIA tasks.

Fix: port the held-out/paraphrased-subset contamination arm into `paper.md` (as a B-alt-2 arm or
an E2 sub-analysis with its own pre-committed downgrade wording), with its cell size and power
noted.

### F4 [FIXABLE] H3's fallback paper would not survive review as written

Evidence: `paper.md` E3 fallback: *"we release a harder tier (multi-step-removed faults,
compound-candidate distractors) constructed under the same labeling invariant."* Two problems:
(a) nothing budgets this tier — it appears in no cost estimate, no experiment, no skeleton arm,
so at verdict time it is a promise, exactly the "future work for category (a) evidence" that
guidance.md situation 14 bans; (b) "compound-candidate distractors" is in direct tension with
A5's single-component label-unambiguity assumption and Step 5's labeling invariant ("single
injected fault"), so "same labeling invariant" is unsubstantiated. If H3 fails (methods near
ceiling), the paper's headline becomes this tier — i.e. the weakest-specified artifact becomes
the contribution.

Fix: specify the harder tier now (fault templates, injection distance definition, expected
yield, cost delta) or replace the fallback with something already budgeted (e.g. severity-tier
stratified reporting from the existing severity knob in A3/PG-3).

### F5 [FIXABLE] The no-op control is not class-matched, and δ_∅ is itself an unvalidated instrument

Evidence: E1 tests each class against *"the shared no-op arm"* (`paper.md` E1: "n ≥ 100
injection trials per class + n ≥ 100 no-op trials"; "Two-proportion z-test per class vs the
shared no-op arm"). But the substitution disturbance differs mechanically by component (editing
a plan message ≠ swapping a tool binding ≠ rewriting an observation): a shared arm confounds
"fault effect for class c" with "substitution disturbance differential between class c and
whatever mix the no-op arm used." Worse, δ_∅ is defined as *"swap a component for a semantically
equivalent good copy"* — the equivalence generator (paraphraser? alternate tool build?) is an
instrument with **no R2 validation plan and no stated construction**, violating goal.md §8
("asserted numbers without protocol are treated as absent") for the very arm every H1 comparison
is normalized against. A subtly-degraded "equivalent" copy inflates FlipRate(δ_∅), trips PG-4,
and routes to F-G1 for a harness reason, not a domain reason.

Related: the single-tier placebo conflates harness artifact with intrinsic stochasticity. F-G1's
pivoted abstract claims *"single-component injected faults do not move task outcomes above the
stochastic replay baseline"* — a domain claim — but a non-null δ_∅ cannot distinguish "agent
pipelines are chaotically sensitive" (publishable) from "our orchestrator-edit layer is leaky"
(a bug, goal.md §5 situation 1: invalid run, never a finding).

Fix: (i) stratify δ_∅ per component class and compare class-matched; (ii) add an identity-replay
placebo tier (no edit at all) below δ_∅, so intrinsic stochasticity, edit disturbance, and fault
effect are three separately estimated quantities; (iii) give the δ_∅ generator a one-paragraph
validation protocol (equivalence checked how, by whom, frozen when).

### F6 [FIXABLE] Statistical dependence and the power-at-floor conjunction are both unhandled

Evidence: Stage-2 targets *"3 fault classes × 5 templates × 200 tasks × k=4"* (`paper.md` Step 9)
— ~3,000 trials generated from ~200 base tasks. Trials sharing a base task are correlated (same
trajectory prefix, same task difficulty), yet E1's two-proportion z-test, E2's McNemar, and all
bootstrap CIs treat trials as independent; the "≥80 certified trajectories per cell" power floor
is computed on that inflated effective n. Additionally, H1's pass criterion is a conjunction —
point-estimate gap ≥ 0.20 **and** BH-corrected significance — so at a true gap of exactly 0.20
the pass probability is ≈ 0.5, not the stated ">0.9 power" (which holds for the significance
component alone at the design alternative).

Fix: cluster the bootstrap by base task (and use a cluster-robust or task-aggregated test for
E1); restate power under clustering; state power against a design alternative strictly above the
floor (e.g. true gap 0.30) or re-express the floor as a CI-lower-bound criterion.

### F7 [FIXABLE] Fallback-combination rules are absent, and two assumption failures fall outside every fallback

Evidence: guidance.md §3.1 rule 4 — *"Write the fallback-combination rules too … never invent
combination logic at verdict time"* — has no counterpart anywhere in `paper.md`; stage_review
item 5 claims the seven slots were "verified by direct inspection" but the combination-rule
requirement was never checked (see Reliability audit). Concrete uncovered outcomes:
- **A1 hard failure** (PG-1: cannot assemble ≥30 reproducibly-solved tasks even after scaffold
  redesign): blocks E1 before H1 exists; F-G1's trigger ("H1 fails on all classes") never fires;
  consequence text is only *"redesign scaffold before Stage 1"* — an engineering loop, not a
  paper. Yet "agent runs are too irreproducible for intervention-certified ground truth" is the
  same *kind* of finding F-G1 already pre-commits to.
- **E1 reversed partial** (plan passes, tool fails): E1's fallback wording is written for one
  specific pattern (*"executable faults … but not for semantic plan corruption"*) and is false
  under the reverse pattern; situation 4 (wrong direction) demands full-prominence reporting but
  no wording exists.

Fix: one short "combination and coverage" block: extend F-G1's trigger to include unrecoverable
PG-1/PG-4 failure; write a pattern-neutral E1-partial wording ("certified for the subset of
classes clearing the margin: {list}"); state which fallback leads for each joint (H2,H3) outcome
(ties into F1).

### F8 [FIXABLE] PG-5's κ gate cannot distinguish "labels are bad" from "post-hoc human attribution is unreliable" — and the latter is the paper's own thesis

Evidence: A5's consequence: *"κ < 0.7 … re-taxonomize templates per guidance.md situation 7 and
re-validate."* But the paper's motivating premise (taste_audit.md §1, digest N2) is that
post-hoc blame — including human blame — may be symptom-matching. If that premise is right,
raters reading only trajectories could fail κ against by-construction labels *because humans
can't do post-hoc attribution*, in which case re-taxonomizing is the wrong move and the
disagreement is a headline finding, not an instrument failure. The protocol already collects
what's needed to disambiguate (inter-rater κ AND rater-vs-label κ, step ④ confusion structure)
but the pre-registered consequence doesn't branch on it.

Fix: pre-register the branch — raters agree with each other but not the label (κ_rr ≥ 0.7,
κ_rl < 0.7) ⇒ label/taxonomy problem, situation 7 applies; raters don't agree with each other
(κ_rr < 0.7) ⇒ post-hoc human attribution unreliable ⇒ report as a finding and rely on
by-construction validity + adjacency inspection instead.

### F9 [FIXABLE] H4's plan-vs-tool comparison confounds fault class with post-certification severity distribution (R3 violation)

Evidence: certification keeps only outcome-flipping faults per class, and A3/PG-3 allows a
*"template-severity knob"* per class to reach yield. Nothing constrains the surviving severity
distributions to be comparable across classes, so H4's `Acc(judge|plan) ≤ Acc(judge|tool) − 0.10`
can reflect "certified plan faults happen to be subtler than certified tool faults" rather than
class identity. No design constraint names this confound (guidance.md R3: "obvious-Y without an
X means the design is broken"), and B0-b accuracy per class — the natural severity proxy — is
reported but not used to condition H4.

Fix: pre-register H4 as severity-controlled (template-matched pairs, or condition on B0-b
per-class accuracy as a difficulty covariate), or weaken H4's wording to a descriptive
confusion-structure claim.

### F10 [FIXABLE] B0-b is specified by an undefined detector, so the "trivial floor" may not be trivial or deterministic

Evidence: B0-b = *"blame the component hosting the last step before first observable error
signal (ties → majority class)"*. "Observable error signal" has no operational definition
(regex over tool returns? HTTP codes? an LLM call?). If it requires judgment, the floor is
itself an unvalidated instrument (goal.md §8) and H2's McNemar comparisons inherit its noise;
if it's a regex, plan-corruption faults (no error string; the run just goes wrong) may emit
*no* signal, making B0-b's tie-rule dominate for the very class H4 cares about.

Fix: one table row in Step 5 — signal definition per fault class, deterministic rule, frozen
before Stage 1.

### F11 [NOTE] B-alt controls a rival for a claim that appears in no hypothesis or claim-map row

Evidence: B-alt's target is *"intervention-based methods (DoVer-style) beat post-hoc judges"* —
but no H1–H4 asserts that, and the Claim–Evidence Map has no compute-parity row; meanwhile the
Abstract v0 promises *"budget-matched … controls isolating causal access from compute."* Either
promote the intervention-vs-judge comparison to a pre-registered (secondary) hypothesis with the
existing downgrade wording as its fallback, or delete the abstract clause. Also: the second
rival's mitigation ("report each method's accuracy on the human-labeled Who&When set") is
under-specified — Who&When's agent/step labels do not map onto the plan/tool/obs component
taxonomy, and no mapping is defined, so that arm cannot currently be scored.

### F12 [NOTE] Resource longevity under backbone deprecation is never confronted

A "Defects4J for agents" built on a closed API model rots: released trajectories serve post-hoc
methods, but intervention-based baselines (and any future user's re-certification) need live
checkpoint-replay on the *same* backbone, which vendors deprecate within ~a year. Defects4J
works because the JVM is stable. This doubles as the missing A3 maintenance/versioning statement
(a named reviewer kill). Fix: pin an open-weights backbone for at least one full corpus tier, or
pre-commit a versioning policy (corpus vN per backbone, re-certification script released).

### F13 [NOTE] Minor pre-registration ambiguities

(a) H2's aggregation ("≥3 of the method families pass") doesn't adapt if PG-6 drops a family —
state the rule as a fraction of runnable families. (b) H3's "max over methods" — is B0-b in the
max? If yes, F1's scenario auto-fails H3 by definition; say so. (c) H1's BH correction across 3
classes combined with an all-three-must-pass conjunction is conservative-on-conservative; an
intersection-union test framing would be cleaner (each class at full α is valid for IUT) —
harmless as is, but the current write-up overstates the correction's necessity.

## Failure-space simulation (per-H walk-through)

- **H1 all pass** → main wording; sound.
- **H1 partial, expected pattern** (tool/obs pass, plan fails) → verbatim fallback exists; the
  fallback paper (certified executable tier + uncertified plan tier) is a genuine, reviewable
  benchmark contribution. Covered.
- **H1 partial, reversed pattern** (plan passes, tool fails) → **uncovered**: the pre-committed
  sentence is false under this pattern (F7).
- **H1 all fail** → single k↑ retry → F-G1 pivot with pre-written abstract; the pivot paper
  survives review *only if* the non-null-flip result can be shown to be domain stochasticity
  rather than harness disturbance — which the single-tier δ_∅ cannot show (F5). Partially
  covered.
- **H2 fails, B0-b low** → fallback wording ("methods don't survive mechanical verification")
  is a strong, publishable negative finding; the benchmark artifact survives independently.
  Covered — this is the design's best fallback.
- **H2 fails because B0-b is high** → **uncovered** (F1): the pre-committed wording misdescribes
  the world; no routing exists.
- **H3 fails** (methods near ceiling) → fallback promises an unbudgeted, invariant-straining
  harder tier (F4). Nominally covered, practically weak.
- **H4 fails (null)** → fallback fine, low stakes. **H4 reversed** (plan easier than tool) →
  the wording "not ordered by fault class" is false; situation-4 handling not pre-written. Minor
  gap.
- **Assumption space:** A2/A3/A4 route sensibly through PG-2/3/4 (A4 → k↑ → F-G1). **A1 hard
  failure is the one outcome that leaves the paper with nothing** as pre-registered (F7): no
  reproducible base pool ⇒ no E1 ⇒ F-G1's trigger never fires ⇒ only "redesign scaffold."
- **All-fail / mixed combos:** no fallback-combination rules exist anywhere (F7), contrary to
  guidance.md §3.1 rule 4; combination logic would be invented at verdict time, which is exactly
  what pre-registration is supposed to prevent.

Bottom line: roughly 80% of the failure space lands on a genuinely pre-committed, publishable
sentence — better than most specs — but the three uncovered cells (B0-b ceiling, A1 hard fail,
reversed partials) include what is arguably the single most likely outcome (B0-b high on a
severity-selected corpus).

## Missing RQs / reviewer questions the design cannot currently answer

1. **"Is judge accuracy driven by memorized GAIA solutions?"** — contamination arm exists only
   in the stale draft, not the executable spec (F3).
2. **"How will the community use this after your backbone is deprecated?"** — no
   maintenance/versioning statement; intervention baselines are irreproducible post-deprecation
   (F12). A3 kill-list item, unanswered.
3. **"Does anything transfer beyond one scaffold?"** — t2 promises multi-framework at Stage 2,
   but no RQ/H covers scaffold generality; all H1–H4 claims are single-scaffold and the envelope
   says so — fine — but then the "reusable community asset" claim (CO1) quietly exceeds the
   envelope: a corpus of one scaffold's trajectories certifies attribution *on that scaffold*.
   Either add a two-scaffold replication cell or bound CO1's wording.
4. **"Is your certified corpus just the easy faults?"** — severity-selection bias induced by the
   flip gate (F1/F9); needs a severity-stratified accuracy report to answer.
5. **"How exactly is a 'semantically equivalent good copy' produced and audited?"** (F5) — a
   methods-section question with no current answer.
6. **"Your κ audit assumes humans can post-hoc attribute; your intro says they can't — which is
   it?"** (F8).

## Reliability audit of prior Phase A PASS

Independently re-verified items 4, 5, 6 (the most rubber-stamp-prone) plus item 2 and the
reference spot-checks:

**What held (genuinely done, verified in the files):**
- Item 6 partial: the R1 estimand paragraph **is** in `paper.md` (line 30), quantity/unit/
  population/decision all present; PG-1…PG-6 ids **are** in `paper.md` (11 occurrences) with
  consequence clauses; the power/thin-cell INCONCLUSIVE paragraph **is** present; A5's R2
  protocol **is** the full 5-step sequence with κ ≥ 0.7 and adjacency inspection — these claimed
  fixes are real, not asserted.
- Item 4 mostly: the Claim–Evidence Map has no orphan claims and no orphan H-ids in either
  direction (5 rows ↔ H1–H4 + supported-by-design), as recorded. One soft orphan the pass
  missed: the abstract's budget-matched-control promise has no claim-map row (F11).
- Cache hygiene: 159 records, 0 `pending`, rejected entries carry individual topic-specific
  `why` strings (spot-checked); the 7 arXiv-sourced selected records' `pdf_path`/`digest_path`
  all resolve on disk (2512.24842, 2512.24145, 2607.02436, 2512.24635 verified); their `why`
  fields are genuinely about B2.1 (reproducibility risk → A1; paired-seed variance → A4/C2;
  observational-attribution foil) — **no cross-topic contamination found**.
- The 8 OpenReview ids exist in `topics/corpus/ideas.jsonl` with matching titles (GazlTYxZss,
  l05DseqvuD, mrEK16Jy6h re-fetched from the corpus by this review).

**What was rubber-stamped (recorded PASS not supported by file contents):**
- **Item 2 "PASS after fix" is false as recorded** (F2): all nine load-bearing
  baseline/method-twin/contrast records have `digest_path: null`, `id_resolves: false` — the
  checklist's own text ("load-bearing entries have resolvable digest_path; spot-check 2–3 ids by
  fetching") is unmet; the review noted the gap and passed itself anyway.
- **Item 6's confound sub-check leaned on a control that is not in the spec** (F3): "the
  pre-existing contamination control from the Stage 4 fix" exists only in `paper_draft.md`;
  `paper.md` has zero contamination content. Item 10's A3 evidence-standard claim inherits the
  same error, and the A3 versioning kill was never checked at all.
- **Item 5 checked the seven slots but not §3.1's rules**: fallback-combination rules (rule 4)
  are absent from `paper.md` and the pass never mentions them (F7); the E1-partial wording's
  pattern asymmetry was also not noticed.
- The advisory phase-state note (paper_draft.* are honest placeholders, resume point = Phase B)
  was re-verified and **is accurate** — the draft contains explicit placeholder results and no
  fabricated numbers.

Net: the Phase A re-run did real, verifiable work (it caught the PRISM memory-citation, rebuilt
a genuinely off-target cache, and added real rigor scaffolding) but its final "PASS" is
**partially reliable**: two of the eight checklist items (2 and 6) are recorded as passing
against the checklist's own literal criteria when the files show otherwise.

## Overall: NEEDS-REVISION

The core design is unusually well-constructed for a pre-registered spec — a real asymmetry
(forward-manufacturable ground truth), an honest archetype call, a concrete cheap skeleton, and
per-H fallbacks that are mostly publishable papers in their own right. What blocks it is not the
idea but three closable holes in the failure-space and spec-integrity machinery:

**Three highest-leverage fixes:**
1. **Close the B0-b-ceiling cell and write the combination rules** (F1, F4, F7): add the
   pre-registered branch for "trivial heuristic ≥ 0.90 on the certified tier" with budgeted
   harder-tier construction, a pattern-neutral E1-partial wording, F-G1 trigger extension to
   unrecoverable PG-1/PG-4 failure, and one block of fallback-combination rules. This converts
   the design's most likely embarrassing outcome into its pre-committed second paper.
2. **Move the missing controls into the binding spec and split the placebo** (F3, F5): port the
   contamination arm from the draft into `paper.md`; stratify δ_∅ per component class; add an
   identity-replay tier below it; give the δ_∅ generator and B0-b's error-signal detector
   frozen, deterministic definitions. Without this, both the headline comparison and the F-G1
   pivot are one reviewer question away from "harness artifact."
3. **Fix the statistics and finish the reference work** (F2, F6): cluster all tests/bootstraps
   by base task and restate power under clustering and above the effect floor; digest and
   fetch-verify the four genuinely load-bearing references (WhoAndWhen, DoVer, AgenTracer,
   SelfEvolveBench) so the novelty concession is grounded in the papers, not proposal extracts —
   then re-run Phase A items 2 and 6 for real.

## Fixes applied (2026-07-04)

Applied directly to `paper.md` (P) and `digest.md` (D) after coordinator authorization; one line per edit.

1. P Step-5 notation: `δ_∅` split into class-matched `δ_∅^c` (same edit pathway as `δ_c`, R3 confound named) + zero-tier identity replay `δ_id`. (F5)
2. P Step-5 table: comparison row re-keyed to `δ_∅^c`; new row defining the *heuristic-sufficiency rate* `Acc(B0-b)` as a reported quantity. (F1)
3. P A1/PG-1: single pre-registered scaffold redesign only; persistent yield < 30 routes to F-G1's new PG-1 branch — no open-ended redesign loop. (F7)
4. P A2/PG-2: crash gate re-keyed to per-class `δ_∅^c` arms. (F5)
5. P A4/PG-4: rewritten as a two-tier bound (`δ_∅^c ≤ 0.10` per class, `δ_id ≤ 0.05`) with tiered disambiguation — edit-pathway artifact ⇒ harness fix (situation 1), identity-tier failure ⇒ k↑ once then F-G1. (F5)
6. P E1: metric/test class-matched; cluster-robust inference at base-task level; honest power statement (≈0.5 pass probability at the 0.20 floor; powered against the 0.30 design alternative; pilot cluster-bootstrap power simulation with frozen thresholds, under-powered classes INCONCLUSIVE); fallback rewritten pattern-neutral with situation-4 full-prominence clause. (F5, F6, F7)
7. P E2/H2: aggregation adapts to PG-6-runnable family count (≤2 families ⇒ INCONCLUSIVE); cluster-robust paired test; fallback wording explicitly conditioned on `Acc(B0-b) < 0.90` and superseded by CR-1 above that. (F1, F6, F13a)
8. P E3/H3: B0-b excluded from the max (reported separately); cluster bootstrap over base tasks; fallback harder tier respecified as single-fault, invariant-consistent (lowest certifying severity + fault-to-failure distance ≥ 3), budgeted at ≤ 25% of Stage-2 injection budget as a config change. (F4, F13b)
9. P E4/H4: cluster-bootstrap test; severity confound named (R3) with severity-matched template pairs + per-class B0-b difficulty proxy and a pre-committed severity-effect downgrade wording; reversed ordering routed to CR-5, not the null wording. (F6, F9)
10. P B0-a: rewritten as class-matched arms + identity tier; full 5-step R2 validation plan for the δ_∅ equivalence generator (2 raters, κ ≥ 0.7, ≥ 95% equivalent, freeze-hash pre-Stage-1). (F5)
11. P B0-b: error-signal detector made frozen and deterministic (rule/regex set over logged fields, no LLM); full 5-step R2 plan (2 raters, κ ≥ 0.7 on first-error-step, per-class no-signal rate reported, freeze-hash pre-Stage-1). (F10)
12. P B-alt: Who&When contrast given an explicit agent/step→component label-space mapping with reported coverage rate. (F11 partial)
13. P B-alt-2 added: contamination/memorization control ported from the stale draft into the binding spec (≥ 30 held-out/paraphrased base tasks scored separately in E2–E4, pre-committed memorization-assisted downgrade wording). (F3)
14. P Power statement: rewritten — all E1–E4 inference cluster-robust at base-task level (~200 clusters, not ~3,000 trials); ≥80-trajectory floor demoted to necessary-only; binding check = cluster-bootstrap power simulation ≥ 0.8, frozen pre-Stage-1; INCONCLUSIVE rule extended to either failure. (F6)
15. P F-G1: triggers extended to (b) PG-4 identity-tier failure and (c) PG-1 hard failure, with the PG-1-branch headline quantity (reproducibility yield) pre-committed. (F7)
16. P New section "Fallback-combination rules (CR-1–CR-5)": CR-1 heuristic-ceiling branch with verbatim narrowing wording (heuristic-sufficiency rate as finding + residual challenge tier), CR-2 partial-certification precedence, CR-3/CR-4 reconciling H2×H3 joint outcomes, CR-5 wrong-direction wordings, explicit precedence order. (F1, F7)
17. P New section "Release, versioning, and longevity": versioned tiers keyed to scaffold+backbone, per-backbone certification, one pinned open-weights tier, re-certification script, no silent cross-backbone label reuse. (F12)
18. P Walking skeleton: 4th identity-replay arm; no-op arm class-matched (`δ_∅^tool`); cost updated (≈210 runs, $21–105); pass criterion extended with the coarse `δ_id` check; scale-up config list extended with the no-op variant list. (F5)
19. P Claim–Evidence Map row 5: fallback coverage now cites CR-1/CR-3/CR-4. (F1)
20. D N8 analysis plan: cluster-robust base-task inference + class-matched no-op, consistent with paper.md. (F6)
21. D t4: dependence-of-trials threat added to the stated threat; mitigation updated to cluster-robust tests/CIs. (F6)

### Remaining (needs human or compute — not fixable by spec edits)

- F2: digest + fetch-verify the 9 load-bearing reference records (WhoAndWhen, DoVer, AgenTracer, SelfEvolveBench at minimum) — requires running paper-digest on real PDFs/pages and setting `digest_path`/`id_resolves`; Phase A item 2 should only then be re-recorded as PASS.
- F8: PG-5 κ-gate disambiguation branch (inter-rater κ vs rater-vs-label κ) — recommended in the review but NOT applied here: it changes A5's pre-registered consequence semantics materially and deserves a human decision (it reclassifies a possible gate failure as a headline finding).
- Scaffold-generality: no RQ/H covers multi-scaffold transfer; CO1's "reusable asset" claim remains bounded to one scaffold until a second-scaffold replication cell is added (compute decision).
- paper_draft.md/.tex/.pdf remain stale relative to today's paper.md edits (both the Phase A fixes and this batch); per pipeline.md they are provisional until real B/C/D output exists, so they were intentionally not touched.
- Phase A should be re-run over the edited bundle (goal.md resumability rule: inputs of a passed phase changed).
