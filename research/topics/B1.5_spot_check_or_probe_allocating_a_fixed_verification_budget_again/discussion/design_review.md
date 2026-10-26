# Design Review (adversarial, 2026-07-04)

> Reviewer stance: skeptical PC member, design-only (no results exist). The recorded
> "Phase A (re-run)" outcome in `stage_review.md` was independently re-verified against
> file contents, not trusted. Files reviewed: `README.md`, `digest.md`, `paper.md`,
> `discussion/reference_candidates.jsonl`, `discussion/stage_review.md`,
> `discussion/pipeline.md`, `discussion/taste_audit.md`, `discussion/paper_draft.md`.
>
> Staleness note (stated once, per instruction): `paper_draft.md`/`.tex`/`.pdf` predate
> the 2026-07-04 Phase A edits to `paper.md` — the R1 estimand sentence and the thin-cell
> INCONCLUSIVE rule are absent from the draft (`grep -c estimand paper_draft.md` = 0,
> `grep -c INCONCLUSIVE paper_draft.md` = 0). `pipeline.md` itself discloses this. Not
> penalized further below.

## Verdict summary

| Dimension | Score | One-line reason |
|---|---|---|
| 1. Feasibility & scale | FIXABLE | Datasets real (APPS/BigCodeBench/EvalPlus), skeleton cheap and concrete; but A1's "≥20 naturally occurring reward-hack episodes" has no named source, the allocation-aware machinery is absent from the skeleton (scale-up is NOT config-only for Stage 2), and both `baseline` cache entries lack local PDFs/digests. |
| 2. Soundness | FIXABLE | Estimand and effect floors are genuinely present; but the R2 instrument-validation waiver is wrong (the probe/covering-array generators are unvalidated instruments), B0(ii) is a filter re-check rather than a placebo, H2 has a winner-selection multiplicity hole, and power ignores task clustering. |
| 3. Novelty & pre-emption | FIXABLE | No direct method-twin found; differentiation vs ControlTax/AIControl is a real estimand change (composition vs size/threshold); but the harvest was a generic corpus scan, and the security-games resource-allocation and metamorphic-testing literatures — the two most dangerous reviewer angles — are unengaged. |
| 4. Hypothesis→fallback robustness | FIXABLE | F1/F2/F3 and F-G1 are verbatim, specific, and mostly publishable; but H3b has no fallback in the spec, fallback-COMBINATION rules (guidance §3.1) are missing, H3-failure is confounded with a weak awareness implementation, and wrong-direction wording is absent. |
| 5. Method scope & RQ design | FIXABLE | Validity envelope stated and honest (implanted-shortcut regime, Python); A2's mandatory shapes are mostly present, but the R6 mechanism analysis is double-counted with the B-alt rival arm, and several reviewer-mandatory RQs (attack-mix sensitivity, equilibrium/optimal-π question, awareness dose) are missing. |
| 6. Prior-work reliability (Phase A audit) | PARTIALLY RELIABLE | Items 1–3 and the cache backfill check out honestly (including honest `id_resolves: false`); items 4, 5, and 6 each contain a rubber-stamped sub-claim contradicted by file contents. |

**Overall: NEEDS-REVISION** (see end for the 3 highest-leverage fixes).

---

## Findings (ranked most-severe first)

### F1. [BROKEN → must fix before B] The R2 waiver is wrong: the verification-flavor library is an unvalidated instrument, and its failure modes produce boring non-results the design cannot distinguish from findings.

Evidence: `stage_review.md` Phase A item 6 waives R2 entirely — "R2's 5-step
instrument-validation plan does not apply here … ground truth is constructed (M5:
implanted witnesses), not produced by an LLM-judge/rubric/classifier, so there is no
R2-eligible instrument in this design." But guidance.md R2 explicitly covers "any
taxonomy, rubric, LLM-judge, classifier, **mutation set, detector**". `paper.md` M2's
P flavor is a mutation set — "*invariance probe* = one metamorphic transformation per
call (semantics-preserving input reformatting, value scaling, argument reordering …)"
— and the H flavor is a generated detector ("pairwise (t=2) covering-array generation
over each task's input-parameter domains, judged against the reference solution").
Neither has a soundness validation step or acceptance threshold anywhere in `paper.md`:

- If a "semantics-preserving" transform is not actually semantics-preserving for a
  given task (value scaling changes the correct answer; reformatting hits a parser),
  P flags **genuine** solutions → FA(P) inflates → under the pre-registered guard "a
  flavor whose FA exceeds 10% at any B is disqualified from being declared winner"
  (paper.md E1), P is disqualified for an instrument bug, not a real property.
- If covering-array inputs fall outside a task's valid input domain (very plausible on
  BigCodeBench free-form arguments), r_τ itself misbehaves and H's comparisons flag
  genuine code → same boring disqualification path for H.
- Conversely, silently *weak* transforms (identity-like) make P detect nothing — which
  the design would read as "H1 partially fails / composition is second-order" (F1's
  fallback wording) when the truth is "P was broken." Nothing detects this: A5 checks
  only *constructibility* ("constructible for ≥90% of sampled APPS/BigCodeBench
  tasks"), not correctness, and the FA guard only catches the over-flagging direction.

This is exactly the class of pipeline artifact B0 is supposed to catch, and B0 does not
(see F4). **Fix (cheap, config-level):** add an R2-style gate per targeted flavor,
frozen before attacks per A6: (i) *soundness*: r_τ passes 100% of generated probes and
covering-array checks on every retained task (drop failing probes/tasks, report the
rate); (ii) *positive control*: on scripted attacks whose witness is by construction in
the flavor's detection class (family (c) for P, family (b) trigger-on-pairwise for H),
the flavor must detect ≥ a stated floor at B=∞ (all checks). Both belong in the
walking skeleton as PG-* gates with thresholds.

### F2. [BROKEN → must fix before B] The walking skeleton never exercises the P flavor or the allocation-aware condition, so "scale-up is a config change" is false for the two riskiest pieces of machinery.

Evidence: `paper.md` Step 9 — "**Arms (3):** pure R, pure H, visible-test-replay
B0(ii). Budget B = 4 only … 1 attack family (scripted hard-coding …)" and then
"**Passed ⇒ scaling is a config change** … all registry entries in the harness, zero
new code paths." But Stage 2's aware condition requires an entirely new interaction
loop — Step 5 defines aware as "attack policy conditions on the verifier's past check
outcomes and/or a descriptor of π" — i.e., a feedback channel from verifier to attacker
across episodes that no skeleton arm exercises. That is a new code path by any honest
reading of goal.md's "Scale-up must be a config change, not a code change — otherwise
the skeleton failed." Likewise P (the metamorphic flavor, the instrument most likely to
be unsound per F1) is never piloted; G2's cost-ratio gate (A3) is only ever measured
between R and H. H3 — one of the paper's three headline hypotheses — rests entirely on
machinery that first runs at full scale. **Fix:** add to the skeleton (a) a pure-P arm
over the same 20 tasks with a scripted family-(c) attack, and (b) a minimal aware arm
using a scripted **oracle-aware** attacker that is *told* π and redistributes
deterministically (this doubles as the manipulation check in F5). Both keep the
skeleton in the "<2h, ≈$0" envelope.

### F3. [FIXABLE] The strongest rival explanation is not B-alt's novelty rival — it is the built-in duality between the attack-family taxonomy and the flavor taxonomy, and no arm or analysis tests it.

Evidence: the three attack families in M1 — "(a) hard-coded special-casing of visible
test inputs, (b) implanted input-conditional backdoors (wrong output on a rare trigger
predicate), (c) invariance-breaking implementations" — map almost one-to-one onto the
three flavors' detection classes, which digest C2 itself states: "a random spot-check
detects only shortcuts on sampled inputs, an invariance probe detects only
invariance-violating shortcuts, a hidden combinatorial test detects only
compositional/edge-case shortcuts." With that duality, the pooled MR ordering (H1) and
the mixture result (H2) are largely determined by the experimenter-chosen family mix:
weight family (c) at 1/3 and P is guaranteed a large detection share by construction.
B-alt ("targeted flavors win only because their inputs are novel") does not touch this
rival; t3's per-family breakdown reports it but no pre-registered analysis quantifies
it, and the estimand's "population of (task, attack-family) episodes" quietly makes the
experimenter's mix the population. A measurement-study reviewer (A2 kill list:
"condition confounded with composition") will lead with this. **Fix (reanalysis-only,
pre-registrable now):** pre-register a family-mix sensitivity analysis — recompute the
H1/H2 winners under reweighted family mixes (e.g., each family at {10,33,80}% of mass)
and pre-commit the wording: the recommendation is claimed only where the winner is
mix-stable, otherwise stated per-family. A1's natural-episode audit then anchors which
mixes are realistic.

### F4. [FIXABLE] B0 is a premise/floor check, not a placebo: its "null" is guaranteed by the same filter it tests, and no null-by-construction arm exercises the scoring pipeline.

Evidence: `paper.md` B0(ii) — "Since attacks pass T_vis by filter, its expected MR ≈ 1;
if this arm's MR is NOT ≈ 1 (> 0.9), the attack filter is broken and all runs halt."
Asked hard (per the review charge): would B0(ii) actually come out "null" if the
pipeline is clean? Yes — tautologically, because the acceptance filter already enforced
100% pass on T_vis at implantation time; the only way it goes non-null is execution
nondeterminism/flakiness. That is worth catching, and the arm legitimately serves
guidance §3.3(1)(a) ("current-practice arm whose asserted guarantee your study tests").
But §3.3(1)(b) — "a null-by-construction placebo (shuffle labels/years/assignments)
whose effect must be null" — has no counterpart: nothing shuffles y_e labels (permuted
within task, the measured 'MR difference' between policies must vanish) and nothing
validates the *genuine* side of the label. Indeed the genuine-episode pool is never
specified anywhere in `paper.md`: Step 5 defines y_e ∈ {genuine, shortcut} and the FA
guard depends on genuine episodes, but M1 only generates attacks — where genuine
episodes come from, and why a "genuine" model solution passing T_vis contains no
*spontaneous* test-special-casing (a documented LLM behavior), is an unstated
assumption with no A* entry. **Fix:** (i) add a label-permutation placebo arm scored
through the identical M4 path (must show no policy separation); (ii) specify the
genuine-episode source and add A7 (genuine-label purity) with a detection (witness-style
spot audit of n genuine episodes) and a consequence for the FA guard.

### F5. [FIXABLE] H3's failure is ambiguous between "mixed-strategy robustness is false" and "our awareness implementation was too weak to matter" — and the pre-committed fallback would overclaim in the second case.

Evidence: F3's fallback text — "Allocation-awareness taxes all defenses equally: we
measure the awareness tax … the binding variable is information leakage to the agent,
not budget composition" — and F-G1's pivot ("budget size and agent awareness, not
composition, are the binding variables") both *assert awareness effects* that are only
meaningful if the aware attacker actually redistributed shortcuts. If LLM attack
policies fail to exploit "past check outcomes and/or a descriptor of π" (A2 covers
attack *strength*, not adaptation competence — no assumption covers this), ΔMR ≈ 0 for
every policy, H3 "fails," and the pre-committed sentence publishes a mechanism claim
("taxes all defenses equally") that the data cannot support. This is the one place in
the failure space where the fallback machinery makes the paper *worse* than silence.
**Fix:** add an oracle-aware scripted attacker arm (told π exactly) as a positive
control / manipulation check, with a pre-registered gate: the blind→aware shift under
the *best pure deterministic-leaning* policy against the oracle attacker must exceed a
floor; if it doesn't, the aware condition is declared inoperative and H3 is reported
INCONCLUSIVE (not failed, not fallback-worded). This composes with F2's skeleton arm.

### F6. [FIXABLE] The fallback algebra is incomplete: no combination rules, no H3b fallback in the spec, no wrong-direction wording.

Evidence, against guidance §3.1's explicit rule "Write the fallback-combination rules
too … never invent combination logic at verdict time":
- The only combination rule in `paper.md` is F-G1's all-fail trigger ("If the central
  hypothesis family {H1, H2, H3} all fail"). Mixed outcomes are uncovered, and at least
  one is internally contradictory: **H1-fail + H2-pass** — F1 asserts "check-flavor
  composition is a second-order defender lever at budgets ≤ 8" while a passing H2
  asserts a mixture beats every vertex by ≥5pp AUC, i.e., composition is first-order.
  Which sentence goes in the abstract would be decided post hoc.
- **H3b has no fallback in `paper.md`**: E3's fallback opens "If H3 fails," and H3b is
  only Holm-co-corrected with H3. Simulated failure: H3 passes, H3b fails (the
  single-channel baseline is as robust as the portfolio). The claim-map row 5 pools
  both ("Mixed/randomized allocations retain more detection power …; portfolios beat
  the single-channel baseline at matched cost | H3, H3b | … fallback-covered (E3
  fallback)") — but E3's fallback covers neither half of that outcome. Notably the
  *draft* already contains suitable wording (paper_draft.md line 140: "a
  flavor-portfolio confers no additional robustness over a well-tuned single-channel
  auditing threshold once an agent adapts …") — it just was never backported into the
  pre-registered spec, which is the file of record.
- No wrong-direction wording (guidance Part 4 situation 4): if R beats both targeted
  flavors by ≥10pp, F1's "random spot-checking … is already cost-competitive"
  *understates* a reversal that should be reported at full prominence.
**Fix:** add a short pre-committed outcome matrix to Step 6 (8 cells over
H1/H2/H3 × pass/fail plus the H3b split and the B-alt re-attribution), one sentence per
cell, resolving the F1↔H2 tension explicitly; promote the draft's RQ4 falsification
sentence to a named F3b; add one wrong-direction sentence per H.

### F7. [FIXABLE] Two statistical-design gaps: H2's "some evaluated mixed policy" invites winner's-curse selection, and the power statement ignores task clustering.

Evidence: H2 — "holds iff **some** evaluated mixed policy (10%-grid interior point or
the adaptive policy, Stage 2) has AUC* lower than EVERY pure vertex's by ≥ 0.05" — and
its verification note "mixture-vs-best-pure is the single pre-registered primary
contrast; the full simplex sweep is exploratory." These two sentences conflict: if the
winning mixture is *selected* from the same Stage-2 data on which the confirmatory CI
is computed (a ~66-point interior grid plus the adaptive policy), the mixture-vs-vertex
difference is optimistically biased and Holm on "3 pairs per budget" never sees this
selection. Separately, the power claim "≥600 shortcut episodes per (policy, budget,
condition) cell … power > 0.9 for a 10 pp miss-rate difference" treats episodes as
independent, but 600 episodes come from ~100 tasks × 3 families × ~2 seeds — with
task-level clustering (acknowledged: "task-level cluster bootstrap … is the primary
interval estimate") the design effect shrinks effective n well below 600 and the
stated power is not the power of the primary (clustered) analysis. **Fix:** (i)
pre-commit H2's confirmand: either a *pre-specified* mixture (uniform ⅓,⅓,⅓ + the
adaptive policy) as primary with grid exploratory, or select on Stage-1/odd-task halves
and confirm on disjoint even-task halves; (ii) restate power with a design-effect
assumption (assumed ICC, effective n per cell) and adjust cell sizes or the thin-cell
threshold accordingly.

### F8. [FIXABLE] Feasibility soft spot: A1's detection dataset does not exist as named, and the two `baseline` references have no local PDF/digest.

Evidence: A1's detection — "pilot audit of ≥20 naturally occurring test-special-casing
episodes from ordinary RL-for-code runs" — presumes access to RL-for-code training runs
that surface natural reward hacks. No source is named; this team's design has no RL
training anywhere, so these episodes are data that "does not actually exist" as
specified. Meanwhile the two entries the design literally reproduces as baseline arms
(H3b) carry `"pdf_path": null, "digest_path": null, "verified": {"id_resolves": false}`
(AIControl2024, ControlTax2024 in `reference_candidates.jsonl`) — honestly recorded,
and correctly logged as a pre-B blocker in stage_review.md, but as of today the
matched-budget reproduction of a protocol whose paper has never been fetched is
designed from `ideas.jsonl` summary text. **Fix:** (i) name A1's source now (published
reward-hacking example corpora / incident writeups, or pre-commit to generating them
via an unfiltered pass of the paper's own solver models and auditing passing solutions
for spontaneous special-casing — the latter is fully in-harness); (ii) keep the
existing pre-B blocker: fetch + digest AIControl and ControlTax before any H3b design
freeze.

### F9. [FIXABLE] Related-work exposure: two literatures a reviewer will raise are unengaged, and one headline prediction is quasi-known.

Evidence: the harvest that produced `reference_candidates.jsonl` was not query-driven
from the core question as goal.md §1 requires ("≥4–5 query angles derived from the core
question") — the 150 candidates include ~40 ACL-2023 papers on zero-pronoun
translation, NER augmentation, essay scoring etc., i.e., a pre-existing corpus scan
filtered post hoc; 130/150 rejections confirm the pool, not the search, was the
problem. Consequences: (i) the **security-games resource-allocation** line (Stackelberg
security games, randomized patrol/inspection allocation against strategic attackers —
the deployed-systems literature beyond the cited Avenhaus survey and
CalibratedStackelberg) is absent, and it is the field where "randomized/mixed
allocations survive an informed adversary better than deterministic ones" — the content
of H3 — is close to a theorem. That makes H3's *confirmation* low-novelty (its
refutation or the measured magnitude is the contribution) and the framing should say
so. (ii) **Metamorphic testing** (the P flavor is literally built from "one metamorphic
transformation per call", paper.md M2) is uncited anywhere — `grep -i metamorphic
paper_draft.md` returns nothing — the exact same kill the stage reviewer caught for
covering arrays ("isn't this just applying pairwise testing?") and fixed for H only.
The differentiation itself is real and survives: no found work varies budget
*composition* across structurally distinct executable check flavors under an
adaptive code-writing adversary; the asymmetry sentence's deletion test in Step 0 is
genuine (failures concentrate adversarially only under a pass-rate optimizer). Not
pre-empted (guidance situation 12 does not fire), but the two threads must be added
and H3 repositioned as measuring the *size* of a predicted effect.

### F10. [NOTE] R6 mechanism analysis is double-counted, and the game framing writes a check the experiments don't cash.

`stage_review.md` item 6 credits "the B-alt novelty-vs-structure ablation functions as
the required ≥1 mechanism analysis (item 8, R6)" — but B-alt is the R5
rival→ablation arm; using it as the R6 mechanism layer too leaves the "why" question
(which input regions do implanted shortcuts occupy vs which regions each flavor
covers?) unanalyzed. A cheap, pre-registrable R6: per-episode coverage-overlap analysis
between each flavor's realized check inputs and the witness region w_e (all logged
already by M4/M5). Relatedly, CO1 sells "an inspection game whose defender action is a
portfolio," yet no experiment computes anything game-theoretic — not even the
minimax-optimal π* on the measured per-family detection profiles, which is a
config-only linear program once M4's numbers exist. Either add that derived-optimum
analysis (it strengthens E2 substantially) or soften CO1's game language to
"game-motivated measurement."

### F11. [NOTE] Small spec inconsistencies to clean before B.

(i) E2's `applies_if` omits A1 and A6 although H2's external validity depends on both
(E1 lists all six); under-declared dependencies weaken the verdict-time consequence
routing. (ii) Budget sweep is written three ways: "B ∈ {1,2,4,8(,16)}" (Step 5),
"{1,2,4,8}" (E1 verification), "1–16 calls" (Abstract v0) — freeze one grid per stage.
(iii) The guidance §3.1/§3.2 field labels (`applies_if`, `gate:`, `consequence:`) are
not used literally; content is mostly present (stage_review item 5 disclosed this),
but A1/A5/A6's gates should be named PG-* entries so Phase B can check them off.

---

## Failure-space simulation (per hypothesis)

- **H1 fails (powered, right-direction null).** F1 fires: "uniform random spot-checking
  … is already cost-competitive … composition is a second-order defender lever at
  budgets ≤ 8." Verbatim, specific, and — because AI-control practice assumes targeted
  hidden tests matter — a genuine A2 flat-result finding. **Survives review only if F1
  (instrument gates) is fixed**: today a silently weak P/H produces this exact null,
  and a reviewer will refuse the "targeting buys little" conclusion without a
  positive-control demonstration that the targeted flavors *can* detect their own
  attack class. Wrong-direction variant (R strictly best by ≥10pp): no pre-committed
  wording — currently under-covered (F6).
- **H2 fails.** F2 fires ("mixing dilutes rather than hedges … identify the dominant
  flavor and commit"), conditional on the allocation-blind regime — clean, honest,
  publishable as a one-flavor recommendation. Covered. The dangerous cell is
  **H2-pass + H1-fail**, where F1's "second-order lever" sentence and H2's ≥5pp-AUC
  mixture advantage contradict; no combination rule exists (F6).
- **H3 fails.** F3 fires ("awareness taxes all defenses equally … binding variable is
  information leakage, not budget composition"). **Currently unsafe**: without a
  manipulation check the same observation is produced by an inoperative aware
  condition, and the fallback would publish an unsupported mechanism claim (F5). With
  the oracle-aware positive control added, this cell becomes safe and interesting.
- **H3-pass + H3b-fail.** Uncovered in `paper.md` (fallback exists only in the stale
  draft's RQ4 falsification line); claim-map row 5 pools both hypotheses into one
  sentence that neither main nor fallback wording would license (F6). This is the one
  concrete outcome today that leaves a headline claim with no pre-committed sentence.
- **B-alt kills the mechanism** (targeted ≈ novelty-matched control). Pre-committed
  re-attribution wording exists and is good ("held-out novelty, not targeting
  structure, is the active ingredient") — the asymmetry statement survives re-scoped to
  distributional disjointness. Covered. Interaction with H3 (does the mixed-robustness
  claim survive re-attribution?) is not specified — minor.
- **All of {H1,H2,H3} fail.** F-G1 pivots to a negative-result paper with a pre-written
  abstract — structurally correct per guidance §3.3(3), and the power machinery makes
  the null credible *per cell*. Its survival depends entirely on instrument
  credibility (F1) — a null from unvalidated probes is "nothing," per S9 discipline.
- **A2 fails (weak/refusing attackers).** Scripted-implantation floor is the
  pre-committed fallback attacker; claims then narrow to the scripted regime. Covered,
  though the narrowed wording is not pre-written (add one sentence).
- **B0 non-null / thin cells / A3 meter violation.** All three route correctly (halt;
  INCONCLUSIVE per the new thin-cell rule; pre-committed wall-clock re-indexing).
- **Is there any outcome that leaves the paper with nothing?** One: any result (pass,
  fail, or pivot) obtained with an unsound P/H instrument is uninterpretable, and the
  current design cannot detect the "silently weak instrument" direction. That is why
  F1+F2 are ranked first — they are the only holes through which the entire failure-
  space coverage drains.

## Missing RQs / reviewer questions the design cannot currently answer

1. **"Isn't the winner an artifact of your attack-family mix?"** — no pre-registered
   mix-reweighting sensitivity analysis (F3).
2. **"How do you know the aware attacker actually adapted?"** — no manipulation check /
   oracle-aware upper bound (F5).
3. **"Where do genuine episodes come from, and how pure is the genuine label?"** —
   unspecified pipeline feeding the FA guard (F4).
4. **"You formalize an inspection game — what is the optimal/minimax allocation your
   own measurements imply, and does the adaptive policy approach it?"** — no derived
   π* analysis despite it being config-only (F10).
5. **"Is the recommended composition stable across budgets B, or does the winner flip
   along the frontier?"** — the frontier contains the data but no pre-registered
   budget×composition stability test feeds the stated decision ("commit at a given
   call budget").
6. **"Does the ordering hold across attacker model families, or is it one model's
   attack style?"** — per-model breakdown implied by M1 but no pre-registered contrast.
7. **"Why t=2 covering arrays?"** — no sensitivity or justification beyond convention.
8. **"Isn't this metamorphic testing / a security game with new labels?"** — two
   missing related-work threads (F9).

## Reliability audit of prior Phase A PASS

The recorded gate is "REVISE (fixes applied; one residual pre-B action)" — not a clean
PASS — and much of it is honest work. Independently re-verified:

**Held up:**
- **Item 1 (digest self-verification):** claimed fix is real — `digest.md` now carries
  12 `absence_comment` blocks across N0–N8/N10–N12 (N9 is placeholder-by-construction);
  N0–N12 + Claims all present; M/C/RQ/CO cross-references resolve.
- **Item 2 (cache integrity):** the backfill story checks out end-to-end. All 7
  OpenReview ids resolve in `topics/corpus/ideas.jsonl` (verified by paper_id lookup);
  the 8 backfilled records honestly carry `id_resolves: false` with explanatory
  `_note`s rather than fabricated paths; no `pending` entries anywhere (158 lines, all
  selected/rejected). Spot-checked 4 harvested `selected` records beyond the review's
  own 3: SWERMExecutionfree2512.21919, CertifiedSpeculati2606.31023,
  acl_sun-etal-2023-backdooring, SafetyTestingLLMAg2607.01793 — all pdf_path and
  digest_path resolve on disk; both inspected digests match their titles/content; every
  `why` is written against THIS topic's budgeted-adversarial-verification framing (the
  contrast/background rationales are specific, e.g. SWE-RM as "replace vs ration the
  verifier") — no cross-topic contamination detected.
- **Item 3 (tag discipline):** spot-checks agree; no HYPOTHESIS→GIVEN promotion found.

**Rubber-stamped (recorded verdict not supported by file contents):**
- **Item 4 — "All 8 rows … trace to an H-id (H1/H2/H3/H3b) or to
  'supported-by-design'":** false as written. Claim-map row 6 ("The active ingredient
  is targeting structure, not mere input novelty") traces to "B-alt contrast," which is
  neither an H-id nor supported-by-design — a needs-experiment claim scored by an arm
  that has no hypothesis-template slots (no α/aggregation/applies_if). Fixable by
  promoting the B-alt criterion to a named H4 with the existing 5pp/CI rule, but the
  recorded PASS papered over it.
- **Item 5 — "H1/H2/H3/H3b each state … a verbatim fallback":** false for H3b, which
  has no fallback anywhere in `paper.md` (E3's fallback opens "If H3 fails"). The item
  also never checked guidance §3.1's mandatory fallback-**combination** rules, which
  are absent (only F-G1's all-fail trigger exists). Both are exactly the machinery
  item 5 exists to verify.
- **Item 6 — "there is no R2-eligible instrument in this design":** wrong; guidance R2
  names "mutation set, detector" and M2's metamorphic-transform and covering-array
  generators are both (finding F1). The same item credits the B-alt arm twice (as the
  R5 rival ablation and as the R6 mechanism analysis), thinning the Part 2 A2 evidence
  standard it claims is met.

**Net:** PARTIALLY reliable — file-verifiable claims (counts, paths, ids, backfills)
were done honestly and carefully; judgment calls (schema conformance of the claim map,
seven-slot completeness, R2 applicability) were graded generously in the design's
favor, and each generous grade hides a real pre-B defect.

## Overall: NEEDS-REVISION

The core design is a genuinely well-shaped A2 measurement study — real estimand, real
effect floors, honest scoping, a pre-written pivot — and nothing found here requires
new compute beyond the (still cheap) walking skeleton. But three defects would, if left
until execution, convert plausible outcomes into unpublishable or dishonest ones:

1. **Instrument-validate the targeted flavors and pilot them (F1+F2).** Add per-flavor
   R2-style gates — r_τ-soundness at 100% and a positive-control detection floor on the
   flavor's own attack class — and put a pure-P arm plus a scripted oracle-aware arm
   into the walking skeleton. This closes the only hole through which *every* branch of
   the failure space (including the F-G1 negative-result pivot) can drain.
2. **Complete the fallback algebra in `paper.md` (F6+F5).** Pre-commit the outcome
   matrix over {H1,H2,H3}×{pass,fail} plus the H3b split (backport the draft's RQ4
   falsification sentence as F3b), add wrong-direction wording, and gate F3 behind the
   oracle-aware manipulation check so an inoperative aware condition yields
   INCONCLUSIVE, not a fake mechanism claim.
3. **Defuse the attack-mix circularity and the two missing literatures (F3+F9).**
   Pre-register the family-mix reweighting sensitivity analysis with mix-stability
   wording; add metamorphic-testing and security-games-allocation threads and
   reposition H3 as measuring the magnitude of a predicted effect. Name a real source
   for A1's natural-episode audit while touching that section.

With these applied — all document/config-level — the bundle is a defensible pre-B spec.

## Fixes applied (2026-07-04)

Authorized direct edits, applied by this reviewer after the review above. One line per edit.

1. `paper.md` A1: named two concrete episode sources for the ≥20 natural reward-hack audit (in-harness unprompted solver runs + published incident reports, witness-checkable) and added a downgrade rule (scope-narrowing fires by default if <20 assemble) — closes F8(i).
2. `paper.md` Assumptions: added A7 (genuine-label purity) with failure mode, skeleton-time 100-episode audit detection, 2% impurity threshold, and consequence for the FA>10% disqualification — closes F4(ii).
3. `paper.md`: new "Instrument validation (guidance.md §3.4 R2)" section — full 5-step plan for the P mutation set and H covering-array detector with acceptance thresholds (r_τ soundness 100%; positive-control detection ≥90% on the flavor's own scripted attack class; drop-not-patch refinement; freeze per A6) — removes the wrong R2 waiver, closes F1.
4. `paper.md` Step 6 constants: power figures now explicitly cluster-adjusted (DEFF with pilot-estimated ICC, no value asserted); thin-cell rule keyed to effective n — closes F7(ii).
5. `paper.md` E1: fallback named F1; the "second-order lever" clause removed from F1 and licensed only under CR-4; wrong-direction (R strictly wins) pre-committed wording added per situation 4 — closes the F6 contradiction and wrong-direction gap for H1.
6. `paper.md` E2: H2's confirmand pre-specified (uniform 1/3-mixture and adaptive policy, Holm over 2; grid sweep exploratory, no post-hoc selection scored) — closes F7(i); assumption list extended to A1/A6 — closes F11(i).
7. `paper.md` E3: added pre-scoring manipulation check (scripted oracle-aware attacker, ≥10pp floor; failure ⇒ H3/H3b INCONCLUSIVE, never a mechanism claim); F3 conditioned on the check passing; added verbatim F3b for the H3-pass/H3b-fail split (backported from the draft's RQ4 falsification line); added the security-games concession note — closes F5 and F6's H3b hole.
8. `paper.md` B0: added arm (iii), a within-task label-permutation placebo scored through the identical evaluator (non-null ⇒ run invalid, situation 1) — closes F4(i), giving B0 a genuine null-by-construction component.
9. `paper.md` B-alt: promoted the contrast to Hypothesis H4 with all seven §3.1 slots (5pp floor, Holm, aggregation over E1-winning flavors) and verbatim fallback F4 — closes the item-4 claim-map orphan at its source.
10. `paper.md`: new pre-registered taxonomy-duality (R3) sensitivity analysis — attack-family reweighting grid {10/33/80}%, reanalysis-only, with pre-committed mix-conditional wording anchored to A1's audit — closes F3.
11. `paper.md`: new "Fallback-combination rules" block CR-1…CR-7 covering all H1×H2 cells, the H3b split, the failed-manipulation-check route, and H4's re-attribution interaction — closes F6's missing §3.1 combination rules.
12. `paper.md` F-G1: trigger amended (H3 counts as failed only with the manipulation check passed) and an INCONCLUSIVE-awareness pivoted-abstract variant pre-committed (awareness clause dropped) — closes the F5 overclaim path through the global pivot.
13. `paper.md` Step 9: skeleton extended to 5 arms (adds pure P and a scripted oracle-aware arm), 2 scripted families (a for R/H/aware, c for P's positive control), gates G5 (instrument soundness + positive controls) and G6 (aware channel operative, ≥15pp raw signal), cost re-estimated (800–1,200 runs, still <2h/$0), and the config-only claim rewritten to be true (feedback channel exercised in-skeleton; LLM attackers swap in behind the same interface) — closes F2.
14. `paper.md` Claim–Evidence Map: row 6 re-pointed from "B-alt contrast" to H4 with F4 coverage; row 5 status now names F3/F3b and the INCONCLUSIVE route — closes the rubber-stamped item-4/item-5 defects.
15. `digest.md` N3: added `[MetamorphicTesting-Survey]` and `[SecurityGames-ResourceAllocation]` rows, both explicitly **[UNVERIFIED — requires harvest]**, with concede-and-differentiate positioning for H3's mixed-strategy prediction; grounding-procedure paragraph and absence_comment updated to disclose three non-corpus entries — closes F9's document-side half (the harvest itself still requires network access).

**Not fixed here (needs human, network, or compute):** fetching + `paper-digest` extraction for the 8 backfilled N3 records (AIControl/ControlTax at minimum — pre-B blocker, already logged in stage_review.md); actually harvesting/verifying the two new [UNVERIFIED] literature threads; regenerating stale `paper_draft.md`/`.tex`/`.pdf` to pick up estimand, thin-cell rule, and all edits above (Phase E/F re-run); the derived minimax-π* analysis (F10, recommended but optional — requires Phase C data); running the extended walking skeleton (Phase B compute).
