# Unresolved majors — all four papers, one place

Every room in this batch closed **6/6 CLOSED** but none reached `all_steps_clean`. The completion
gate is `all_steps_clean`, *not* 6/6, so each package carries at least one critic objection the
refiner could not clear. This file is the index; the fix for each lives where the "Fixed in" column
points.

**5 majors across 4 papers. 4 of the 5 are on `related_work`** — see the family README's
"Systematic pipeline finding" section; it is a pipeline defect, not four coincidences.

**41 findings across nine review rounds** are indexed below: the 5 room majors, then rounds 2–5 on
the manuscripts and specs, round 6 on the input and record artifacts, round 7 re-reviewing
ZW1/ZW2/ZW4 after those edits, round 8's external scoop re-sweep, and round 9 re-reviewing all four
after the round-7/8 edits. The room majors are the smallest category — most of what needed
fixing, no critic flagged.

| Paper | Room | Gate | Step | Fixed in |
|---|---|---|---|---|
| ZW1 | `29167d1d` | 5/6 clean, 1 major | `related_work` | `ZW1_proofworld/paper-draft.revised.md` ✅ (diagnosis in `major_fix_rlfr_anchor.md`) |
| ZW2 | `98e3ae6b` | 5/6 clean, 1 major | `related_work` | `ZW2_verified_but_wrong/paper-draft.revised.md` ✅ |
| ZW3 | `9f4da36d` | 4/6 clean, **2 majors** | `related_work`, `experiment_design` | `ZW3_which_prover_teaches_software/paper-draft.revised.md` ✅ (diagnosis in `major_fixes.md`) |
| ZW4 | `7bcfe3ef` | 5/6 clean, 1 major | `related_work` | `ZW4_oracle_economics/paper-draft.revised.md` ✅ |

---

## ZW1 — `related_work` · G3b ablation arm has no anchored prior work

> "The problem statement names the RLFR-style verified-goals ratio as a mandatory ablation arm, yet
> none of the eight deeply compared works instantiates a scalar proof-ratio or
> goals-verified-fraction reward; the baseline set covers execution-state, binary-verifier, and
> Dafny-RL signals but leaves the ratio arm without any anchored prior work, which weakens the
> legibility of the comparison for exactly the contrast the study must run."

**Cause: ours.** RLFR *is* that anchor, but it was omitted from the `references` payload because it
has no arXiv ID. The schema accepts `{citation, url}` without one. The room was asked to justify an
arm against a work it could not see.

**Fix (applied):** a dedicated anchor paragraph now sits in Related Work immediately before the
execution-grounded family — it cites RLFR as non-archival industry work with the archive URL as
primary locator, concedes the shaped per-obligation reward and prover-free transfer, and names the
three properties that keep the question open (undifferentiated ratio, no verdict structure, no
execution baseline at any budget despite claiming one). G3b is described as a **formula-faithful
ablation under our harness**, not a reproduction. Diagnosis in `major_fix_rlfr_anchor.md`.

**Also repaired while merging:** all **28 citations** in the generated draft rendered as `[n.d.]` —
every author, no dates — and one entry ('A recent system') had lost its authors entirely. Dates
restored from the verified record; Proof2Silicon reattributed to Jha et al. \[2025\].

---

## ZW2 — `related_work` · families not contrasted against the estimand

> "The summary reports paper and baseline counts without comparing how verifier-guided training,
> specification-quality evaluation, and static certification differ relative to the delta objective.
> Consequently, the collective motivation for the current problem remains unclear."

**Fix (applied):** Related Work now opens by contrasting the three families against δ directly —
synthesis work acts on the specification but never forms a paired measurement; benchmarks form δ
cross-sectionally on models never trained against the verifier; RL work creates the training
dependence but measures only the verification side. See `paper-draft.revised.md`.

---

## ZW3 — major 1 of 2 · `experiment_design` · the transport step is vacuous

> "The Hájek weights are indexed over training examples while the paired-W estimand is a mean over
> held-out evaluation prompts of a fixed trained model, and no channel is described by which
> reweighting the accepted-trajectory training distribution changes a held-out prompt's outcome. As
> written, the weighted and unweighted estimates could be identical by construction, making the
> equivalence test vacuous and leaving replay-exposure robustness untested."

**The most substantive criticism in the batch, and correct.** The stated success criterion — every
weighted-minus-unweighted contrast within ±0.05 — **could not fail**.

**Fix (applied):** replaced post-hoc reweighting with a training-time intervention — **natural** vs
**flattened** replay regimes trained separately under the same four-axis budget intersection — so the
contrast is a real difference between checkpoints and *can* fail. Diagnosis in `major_fixes.md`.

## ZW3 — major 2 of 2 · `related_work` · circular limitations

> "All eight limitation descriptions are near-identical restatements of the study's own research
> question … problem-relative but undifferentiated and borderline circular."

**Fix (applied):** eight independently standing, primary-verified gaps. Test each must pass: *would
this still be a gap if our paper did not exist?*

---

## ZW4 — `related_work` · every work rejected as a baseline

> "All eight works are marked `is_potential_baseline=false` and the artifact claims 0 candidate
> baselines, but a measurement study still needs concrete training pipelines to instantiate its
> oracle arms; Re:Form's verifier-guided GRPO (proof oracle), ExecVerify's trace rewards (execution
> oracle), and Tan's Dafny RLVR setup are exactly the kinds of arms the harness must run."

**Fix (applied):** Related Work now carries an explicit oracle→recipe table: test outcome → CodeRL;
execution process → ExecVerify with StepCodeReasoner as an independent second instantiation; binary
proof → Re:Form and Tan; structured proof → RLFR as the scalar precursor plus the typed-VC
implementation from the ZW1 companion; hybrid → **study-defined**, with semantic-equivalence
self-play cited as motivation rather than recipe.

**Correction made during strict re-review:** an earlier version of this fix called Re:Form the recipe
for *both* the binary- and structured-proof arms. That is wrong. Re:Form's "subset reward" checks
whether a generated specification is stronger than ground truth — a property of the *specification*,
not a decomposition of obligations discharged for a candidate program. Mis-assigning it would have
made the binary-versus-structured contrast, which the paper exists to price, incoherent. Re:Form now
anchors the binary-proof arm only, and the draft says so explicitly.

---

## Round 2 — full-package audit (2026-08-21, after strict external re-review)

The first round reviewed and fixed **`paper-draft.md` only**. That was the wrong unit: each package
ships three artifacts, and `experiment-spec.md` is what an implementer actually follows. A strict
full-package re-review found that **all four topics still carried at least one major**, in two
classes: (a) manuscript fixes not propagated to the spec, and (b) methodological blockers that no
critic had flagged.

| # | Paper | Issue | Class |
|---|---|---|---|
| 1 | ZW1 | Dense reward runs Dafny + execution at 32 token-indexed prefixes; **most prefixes are not valid Dafny** and no completion/stubbing/incremental-verification procedure was defined — the matched dense feedback was not implementable | blocker |
| 2 | ZW1 | Spec says every training candidate is scored by the execution **hidden-test** harness, then says hidden tests are withheld from every reward signal — mutually contradictory | blocker |
| 3 | ZW2 | **The estimator removed the phenomenon.** With δ = V − B and V = A·D·(1−Q), a verifier-accepted vacuous program gives A=1, B=0, V=0, hence **δ = 0** — smallest measured gap exactly where the pathology is worst | blocker |
| 4 | ZW2 | "The same system before and after its contracts were cleaned" was unsupported — Tan's runs differ in benchmark composition and training protocol too | overclaim |
| 5 | ZW3 | Spec still mandated the invalid Hájek post-hoc weighting; an implementer following it would rebuild the rejected experiment | spec desync |
| 6 | ZW4 | Spec still commanded the saturated five-oracle factorial and a **log-spaced interpolation grid**, contradicting the manuscript's Phase-2 scoping and its "never interpolated" commitment | spec desync |
| 7 | ZW4 | Manuscript said both "never interpolated" **and** "bisection will estimate the crossover" in the same paragraph | internal contradiction |

**All seven fixed.** Notable resolutions:

- **ZW2's estimand is now raw acceptance:** δ = Pr(A=1) − Pr(B=1), with B evaluated over the *trusted
  intended domain* so a model cannot raise B by shrinking its own precondition. The adequacy-aware
  quantity survives as a **decomposition**, not a filter: since A ≥ V pointwise,
  δ = [Pr(V)−Pr(B)] + [Pr(A)−Pr(V)]. A δ driven by the second term is a specification-hacking story;
  one driven by the first is an implementation-correctness story. Both are reported.
- **ZW1 gained a deterministic prefix completer** — close delimiters in parser order, typed holes for
  unterminated expressions, `assume false;` bodies for unwritten methods so unfinished code neither
  verifies vacuously nor fails spuriously, specification clauses untouched. Obligations from inserted
  scaffolding are tagged `synthetic` and excluded from reward; unclosable prefixes are recorded as
  `uncompletable` and their rate reported. The same completer runs on the execution oracle's snapshots
  so the dense arms stay matched by construction.
- **ZW1's test sets are now explicitly two**: `tests_train` (reward-visible, the only set any oracle
  sees) and `tests_sealed` (tool-off only, never exposed to any reward channel or checkpoint
  selection), disjoint by construction, with the spec instructed to fail the run if either oracle
  receives the wrong set.
- **ZW4 crossovers are intervals, not points.** Bisection is removed from both artifacts: it requires
  evaluating capability between measured budgets, which is exactly the interpolation the study rules
  out. Narrowing a crossover requires measuring more budgets, not modelling between them.

## Round 3 — definitions, not prose

Round 2 fixed the *prose* in both artifacts. A third strict pass found that the **definitions** — the
equation, the record schema, the stub semantics — still encoded the old behaviour, and in one case a
round-2 fix had introduced a new defect.

| # | Paper | Issue |
|---|---|---|
| 8 | ZW1 | **The round-2 prefix completer reintroduced vacuity.** It supplied `assume false;` bodies for unwritten methods, intending to prevent spurious failure. `assume false` makes the remaining path unreachable, so the verifier discharges the enclosing method's **original** postconditions and assertions vacuously. Tagging *inserted* obligations `synthetic` cannot undo contamination of obligations the model actually wrote |
| 9 | ZW2 | The formal equation still defined `B_i` via `D_i=1` and "applicable" candidate-contract tests, contradicting the prose asserting `B` is independent of the candidate domain |
| 10 | ZW2 | The methodology section reverted to `V−B` after the problem definition had switched to `A−B` |
| 11 | ZW2 | The spec declared `A−B` but its record schema carried only `(V, B)` — no raw `A` field, so the promised decomposition was uncomputable and the estimand would silently revert |

**The instructive one is #8.** `assume false` is the canonical vacuity idiom; the round-2 fix
reintroduced into ZW1's reward channel the exact pathology that ZW2 exists to measure. The lesson is
not "be careful with Dafny stubs" — it is that **a repair which strengthens a path condition to avoid
a failure signal will usually manufacture a success signal instead**, and that a completer's job is
to close syntax, never to make claims.

The corrected design **abstains rather than assumes**: unwritten bodies stay empty, no assumption of
any kind is inserted, obligations from inserted holes are `synthetic`, obligations whose enclosing
unit is unfinished are `indeterminate`, both are excluded from reward, and both stay distinct from
`unknown`/`timeout` (solver ran, did not conclude). Only fully-written units earn reward, so the dense
signal grows with the candidate. The per-snapshot `indeterminate` share is reported with an inverted
reading: a high early share is the expected shape; a **low** one means the completer is doing more
than closing syntax.

For #9–#11: `B_i` is now `1{f_i satisfies every test in T_ci}` with `T_ci` fixed over the trusted
intended domain and explicitly not conditioned on `D_i` — restricting tests to inputs "applicable"
under `P_i` would hand the model the same lever on the behavioral side it already has on the
verification side. The methodology computes `A_i − B_i`. The record schema persists `A` alongside `V`
with the invariant `V == (A and not vacuity and not empty_domain)` asserted on load.

## Round 4 — the specs, exhaustively

Round 3 fixed definitions at the sites a reviewer had cited. A fourth pass found that **site-by-site
patching kept missing residue**: each spec still carried the removed construct in metric lists,
baseline tables, ablation switches, simulation parameters, and implementation checklists that no one
had pointed at. Fixing only cited lines is not fixing a spec.

| # | Paper | Residue found after round 3 |
|---|---|---|
| 12 | ZW1 | **Dense signal could be empty and nothing would catch it.** Snapshots at 32 *evenly spaced token offsets* land inside unfinished bodies on single-function candidates, so nearly every obligation is `indeterminate`; RQ3 checked only that 32 packets *existed*, not that they held usable reward. The headline typed-vs-execution comparison could silently degenerate into two terminal rewards |
| 13 | ZW2 | Spec's primary metric still `mean(V) − mean(B)`; bootstrap preserved `(V,B)`; plus the four-state hierarchical model, the B1 unpaired baseline, the simulation generator's marginals, and the implementation checklist all still `V`-based |
| 14 | ZW3 | Spec retained the deleted Hájek metric and a `replay_weighting = hajek \| none` ablation switch |
| 15 | ZW4 | Spec simultaneously forbade interpolation, required crossover **bisection**, configured a **log grid**, and applied the Phase-3 10% criterion to the Phase-2 study |

**ZW1's fix changes the design, not just the wording.** Snapshots now sit at **syntactic-completion
boundaries** — each point where a declaration, statement, or specification clause closes — capped at
`K_max=32`. The count `k_c` therefore varies across candidates and is identical across arms for a
given candidate, so matching is per-candidate agreement rather than a global constant, and RQ3's check
changed accordingly. Added a **usable-packet-rate gate**: a packet is *usable* if it holds at least one
determinate verdict that is neither `synthetic` nor `indeterminate`, and falling below the
preregistered median means reporting a **feasibility negative** — the dense arms were terminal-reward
arms — rather than a null result about typed verdicts. Reporting the rate alongside every dense-arm
result is mandatory, because a reader otherwise cannot distinguish *"typed verdicts do not help"* from
*"typed verdicts were never delivered."*

For ZW2–ZW4 the specs were swept by **defect vocabulary** rather than by cited line, which is what
finally exhausted them: every `mean(V)`, `(V,B)`, `hajek`, `bisect`, `interpolat`, and `log grid`
occurrence was inspected and either corrected or confirmed to be part of an explicit prohibition.

**Process lesson:** a fix applied to one artifact is not a fix. Every correction must be swept across
`paper-draft.md`, `experiment-spec.md`, and `research-report.md`, and the defect's vocabulary grepped
afterwards — in this batch, *every* targeted edit left residue somewhere. And fixing prose is not
fixing a design: the equation, the record schema, and the stub semantics each had to be corrected
separately, one round after the prose that described them was already right. Finally, a fix is itself
a change that can introduce a defect (#8), so each round's repairs need the same adversarial reading
as the original draft.

## Round 6 — the input and record artifacts (2026-08-23)

Rounds 1–5 examined `paper-draft*.md` and `experiment-spec.md`. **Seven files in the four packages
had never been read in any round**: the four `seed.md` inputs and the three
`autodiscussion_draft_review.md` records. Round 5 had already marked `research-report.md` as the
unreviewed trap; these are the same class of defect one level further out. Nine findings, four major.

| # | File | Issue | Class |
|---|---|---|---|
| 19 | ZW2 `seed.md`:70 | **Prescribes the reversed estimand.** Instructs that a proof discharged over an empty domain be "recorded as a distinct outcome class rather than counted as success" — the `V = A·D·(1−Q)` gating that finding #3 established nulls out the phenomenon. An implementer starting from the seed rebuilds the blocker | major · reversed design |
| 20 | ZW4 `seed.md`:70 | **"Re:Form's *reported* ~176 GPU-h / ~400 GPU-h" — Re:Form reports no GPU-hours figure at all.** Survived behind an unresolved `[VERIFY]` marker while being corrected in ZW1's seed on 2026-08-21 and in ZW4's own manuscript at :14 and :345. The last third-party attribution error in the family, and it inverts the paper's thesis — that the field's most-cited compute anchor does not report the quantity it is used for | major · factual |
| 21 | ZW1 `seed.md` | **Design is two generations behind.** Six arms G0–G5 vs. the delivered four (A1 typed / A2 dense-execution / A3 binary / A4 RLFR-ratio); G0, G1, G5 do not exist and `hybrid` occurs **0×** in draft and spec. A4 — the mandatory scalar-collapse ablation — appears nowhere in the seed | major · scope |
| 22 | ZW1 `seed.md`:221 | Section headed *"Staging (the gate structure must not be deleted in drafting)"* did not survive drafting. `1.7B`, `Defects4C`, `SWE-EVO`, `RoadmapBench`: **0 occurrences** in both delivered artifacts. The Phase-1 gate ("proceed only if G4 beats G3") has no delivered analogue; the delivered gate is RQ3(c)'s usable-packet rate, different in kind | major · scope |
| 23 | ZW1 `seed.md`:140 | `countermodel-guided repair` still listed as a training objective. It presupposes repair turns — the multi-turn capability withdrawn in round 5 — and the delivered sealed evaluation *disables* countermodel access | moderate · withdrawn claim |
| 24 | ZW2 `autodiscussion_draft_review.md`:25 | **Praises the reversed design.** Lists `V_i = A_i·D_i·(1−Q_i)` under "Where the draft beats the seed" and calls folding adequacy into the estimand "stronger". It is weaker; reversed in round 2 | major · reversed verdict |
| 25 | ZW4 `autodiscussion_draft_review.md`:94 | **Wrong arm mapping.** "Re:Form **is** the binary/structured-proof arm's recipe" — the exact conflation corrected in round 1. Assigning one work to both proof arms collapses the contrast the phase diagram measures | major · reversed verdict |
| 26 | ZW4 `seed.md`:45 | Axes crossed in full are the saturated ~120-cell factorial, presented as *the* design with no staging. Manuscript demotes it to aspirational Phase 3 | moderate · scope |
| 27 | ZW3 `seed.md`:52 · ZW3 review:53 · ZW2 review:77, :109 | Superseded-but-not-wrong details: four reported normalizations vs. the delivered common feasible intersection; the replay cap described without round 3's deterministic redistribution rule; "ZW4 is still running"; an unresolved `[VERIFY]` on six citations that were in fact verified (VERINA is **ICLR 2026 Poster**, not a preprint) | minor · stale |

**All nine annotated, none rewritten.** Seeds are the literal `idea_text` sent to the rooms and the
review files are dated records; rewriting either destroys the provenance that makes them worth
keeping. Each file now opens with a status banner naming what in it is superseded, and each specific
defect carries an inline correction block at the point of the claim — the convention ZW1's own seed
already used for its GraphAlignCoder and RLFR corrections. **Line numbers in the table above are
post-annotation**, i.e. they locate the correction block, not the original text. Findings 19, 20, 24 and 25 are struck
through in place so a reader cannot skim past them.

**Process lesson — the review's blind spot is structural, not accidental.** Every round reviewed
what it had been asked about, and each round's unit of review was the previous round's output. The
inputs were never re-read because they were "already used", and the records were never re-read
because they were "already acted on". Both assumptions fail the moment a later round *reverses* an
earlier decision: #24 and #25 are files that confidently assert designs the manuscripts now argue
against, and #19 is an input file that would lead an implementer straight back to a fixed blocker.
A package is only consistent if every file in it is, including the ones nobody plans to read.

## Round 7 — re-review of ZW1, ZW2, ZW4 after the round-6 edits (2026-08-23)

ZW3 was the only package that had ever passed a strict full-package review *after* its last edit.
This round put the other three through the same reading. Nine findings, four major — and the first
one explains why these three failed where ZW3 passed.

| # | File | Issue | Class |
|---|---|---|---|
| 28 | ZW1 spec:5 · ZW2 spec:5 · ZW4 spec:5, :171 | **Stray agent narration inside three ✅ CURRENT specs**, above the title. ZW1: *"The file write requires permission. Let me output the spec directly as required."* ZW4: *"I'll output the spec directly as Markdown rather than writing to a file"*, plus a closing *"I've written the complete implementation-oriented experiment specification above…"*. ZW2's is the worst: *"This is a web application (Next.js/Prisma), unrelated to the research task itself — it's the platform hosting this work"* — the agent describing the **AutoDiscussion service's own codebase** inside a paper spec. **ZW3's spec has none.** Every round read these files from the title down, so line 5 was never in anyone's view | major · contamination |
| 29 | ZW1 draft:199 · ZW1 spec:266 | **Whole-unit reward gating contradicts the per-obligation determinacy rule, in both artifacts.** *"Only obligations belonging to completely written units contribute reward at a snapshot"* stands one sentence after *"each obligation's determinacy is computed from its own dependency footprint … independent of the enclosing unit."* The spec's own text says whole-method gating makes the dense arms terminal-reward arms and the comparison *"infeasible by construction"* — so the leftover sentence, which is the operative instruction an implementer follows, mandates the failure mode the paragraph exists to prevent. Round 5's determinacy fix, incompletely applied | major · reversed design |
| 30 | ZW1 spec ×10 | **The fixed-`K=32` design survives across the spec** while RQ3(a) explicitly forbids asserting it: *"the same K snapshots"* on A3 and A4, *"K schema slots"* in calibration, `typed_packets: float[32]` and "its 32 typed packets" in the RQ4 record schema, `K=32` in the prereg freeze, the prereg.yaml and `reward_schema.py` comments, the Inputs list, and the Open-Decision heading. The record schema is the first thing an implementer codes. `float[32]` was also dimensionally wrong under *any* reading — a candidate's packets are `k_c × 25` | major · spec desync |
| 31 | ZW4 draft:144 | **The manuscript still specified a log-spaced interpolation grid** — *"Price sensitivity will be evaluated at r₀, r₀/3 and 3r₀, and over a log-spaced interpolation grid"*, then locates crossovers as *"budget locations"*. Contradicts :248 and :341 (*"never interpolated"*; crossovers are intervals) and re-conflates the price-ratio axis with the candidate-budget axis, which the spec warns against twice. Round-2 findings #6/#7 were fixed in the spec and in two other paragraphs of the manuscript, but not this one | major · internal contradiction |
| 32 | ZW2 spec:37, :40 | **`V` was defined twice, contradictorily, three lines apart** — *"V (verifier outcome): run the Dafny verifier; V ∈ {verified, failed}"* (raw acceptance) immediately above *"V (adequacy-aware acceptance): V = A AND domain_nonempty AND NOT vacuous"*. Reading M1 top-down binds `V` to raw acceptance, which makes the load-time invariant false and silently restores the reverted estimand. `E`'s contract also still returned `(V, B)` rather than the triple | moderate · reversed design |
| 33 | ZW4 spec:42 | **RQ6's success criterion was unsatisfiable in the phase the study runs.** It hard-coded `n_eligible >= 80`, while the manuscript declares Phase 2 expected-underpowered and puts ≥80 on Phase 3. RQ5 got a "Success depends on phase" split in round 3; RQ6 did not, so `run_rq6.py` would assert a condition that cannot hold | moderate · spec desync |
| 34 | ZW2 spec:190 | Ablation `pairing` described as isolating **V–B** pairing, where RQ1, B1 and Open Decision 1 are all A–B — and :243 says simulating V–B *"would validate the wrong estimator"* | minor · stale |
| 35 | ZW1 spec:204 | `snapshot_K ∈ {8,16,32}` framed as *"packetization granularity"*. Under the boundary rule K is a **cap**, not a spacing; re-spacing snapshots is the rejected design | minor · stale |
| 36 | ZW2 spec:9 | Objective restated δ as *"(formal verification rate) − (independent behavioral correctness rate)"* — the exact ambiguous wording that produced the reversed design in the first place | minor · stale |

**All nine fixed in place** (line numbers above are post-fix). Unlike round 6 these are `✅ CURRENT`
artifacts, so they are corrected rather than annotated; where a fix reverses an earlier instruction
the correction says so explicitly, so a reader diffing against an older copy sees why.

**Process lesson — "reviewed" meant "read from the title down".** Finding #28 is the cleanest
evidence yet that coverage claims should be about *bytes*, not sections: three of four specs opened
with an agent's chat narration, one of them describing an entirely unrelated codebase, and six
review rounds walked past it because every round started reading at the `#` heading. ZW3 passed its
strict review partly because it happened to have no such line. Findings #30, #31, #33 and #34 are
the same shape as round 4's lesson — a defect fixed by vocabulary in one artifact still lived in the
record schemas, config comments, ablation lists and RQ criteria of the others. The parts of a spec
that read like boilerplate are exactly the parts an implementer copies verbatim.

## Note: majors are not the only defects

Two of the most consequential problems found in review were **not** flagged as majors by the critic
and would have shipped:

- **ZW4's scope inflation** — the draft committed to ~600 training runs after the seed specified
  measurement-only instrumentation layered on companion runs. Caught by comparing draft to seed.
- **ZW2's missing evidence** — the motivation never cited the Tan 58.1%→31.1% collapse or the Re:Form
  exploit sentence, because that room was submitted without a `references` payload.

Reviewing only the flagged majors would have missed both. The seed-versus-draft diff and the citation
audit are separate passes and both are necessary.

## Round 8 — 2026-08-23 pre-push scoop re-sweep (web audit, four parallel auditors)

Fresh internet novelty audit of all four packages before repository publication, two days after the
round-6 sweep. **Zero new majors; zero scoops.** Outcomes, applied same day:

- **ZW1 CLEAR.** No typed-verdict RL twin through 2026-08-23; GraphAlignCoder still v1-only. One
  correction *to a round-4 correction*: Wayback `20260417194155` does exist (for `/research/rlfr`,
  readable) — the "does not exist" sentence was scoped, and the citation rule in
  `major_fix_rlfr_anchor.md` superseded. New non-scooping neighbors logged in the seed (VeRPO
  2601.03525, SpecRL 2604.05820, TCPO 2608.01667, Verification Horizon 2606.26300).
- **ZW2 narrowing (wording only).** "When the Reward Suite Is Leaky" (2607.11022) measures the
  analogous gap under execution rewards — and finds it does NOT grow with training. First-measurement
  claim scoped to proof-rewarded, specification-mediated settings; RQ3 now engages the null in the
  manuscript; vacuity *detection* conceded as prior art (KaPilot 2607.21957, VeriAct 2604.00280).
- **ZW3 narrowing (motivation + control claim).** FM-alpaca (ACL 2025, 2501.16207) already ran a
  mixed-formal-corpus→code transfer with a non-formal control; "neither branch has a credible
  transfer result" is now argued (mixed-language, distilled, baseline-fragile), and control `N` is
  positioned as the budget-matched per-branch successor. Applied to manuscript + seed.
- **ZW4 CLEAR.** Cost-normalized oracle phase diagram still unoccupied. Three neighbors added to the
  ledger (Pareto Optimal Code Generation 2506.10056, Compute-Supervision Tradeoffs 2605.25252,
  JURY-RL 2604.25419); "nobody measures verifier wall-clock in RL training" softened to "no
  systematic cost-normalized capability comparison across oracle types."

## Round 9 — 2026-08-23 strict re-review after the round-7/8 edits

Round 7 corrected the `✅ CURRENT` artifacts; round 8 was an *external* audit that changed wording in
manuscripts and seeds. Neither was followed by an internal re-read, so round 9 re-reviewed all four
packages byte-for-byte, with one governing question: **when a defect was fixed in one artifact, was it
mirrored into the other?** Three of the five findings are that mirror failing.

| # | File | Issue | Class |
|---|---|---|---|
| 37 | ZW1 draft:235, :269, :304 | **The fixed-`K=32` design survived in the manuscript** after round 7 excised it from the spec in ten places. Three sites: *"every candidate produces the same number and arrangement of reward packets"*; *"32 schema-indexed reward slots per candidate"*; and, in the RQ3 section, *"Each arm will emit rewards through 32 schema-indexed slots"* — which **contradicts the paragraph immediately beneath it** (*"the count itself varies across candidates"*) and asserts precisely what the spec's RQ3(a) says must **not** be asserted. `32` is also the snapshot cap, never a schema width: the schema has **25** channels. Round 7 fixed finding #30 in the spec and never opened the manuscript | major · spec desync |
| 38 | ZW1 draft ×5 | **The manuscript's Related Work referred five times to "arm G3b"** — an identifier from the seed's **withdrawn** six-arm `G0`–`G5` table. The manuscript's own arm vocabulary is \(\{\mathrm{TV},\mathrm{EX},\mathrm{BV},\mathrm{GR}\}\); the spec calls the same arm `A4`; `G3b` is defined in neither. Three naming schemes for four arms, and the one the manuscript actually uses to state its ablation claim was the retired one. The round-6 seed banner had already declared the `G` numbering two design generations stale — the banner was written, the manuscript never re-checked against it | major · reversed design |
| 39 | ZW2 draft:274 | **Related Work framed all three prior-work families "against the estimand δ = Pr(V=1) − Pr(B=1)"** — the adequacy-aware form reversed in round 2, which the Formal Problem Definition explicitly rejects because gating on adequacy subtracts exactly the acceptances the paper measures. The body defines δ on raw acceptance in two places. Related Work predates the reversal and was never re-read against it, so the section that positions the entire contribution positioned it against the rejected quantity | major · reversed design |
| 40 | ZW2 draft (Related Work) | **Vacuity-detection prior art was conceded only in working notes.** Round 8 conceded detection as prior art in the seed ledger and the revision log; the **body** cited none of it, while RQ6 claims precision/recall for separating vacuity from empty precondition domains. Both working-note sections are marked *"remove before submission"*, so the submitted paper would have claimed an uncited detection contribution. Now conceded in Related Work — VeriAct (Misu et al., arXiv:2604.00280) and KaPilot (Wang et al., arXiv:2607.21957), **both verified against the arXiv API this pass** — with novelty retained only for the δ-decomposition use | moderate · unsupported claim |
| 41 | ZW1 `major_fix_rlfr_anchor.md` · ZW3 `major_fixes.md` | **The two fix memos were the only package files with no status banner** — round 6 banded 16 artifacts and these two were not among them — and both still instructed *"merge into `paper-draft.revised.md` on sync / when the room syncs"*, an action discharged two days and seven rounds earlier. Read cold, each looks like open work. Both now carry a `📖 DISCHARGED` banner; ZW1's also carries the `G3b`→\(\mathrm{GR}\)/`A4` mapping key that finding #38 made necessary | minor · stale |

**ZW3 passed clean**, as it did in rounds 5 and 7. Its round-8 FM-alpaca concession was verified to
have landed in the **body** — motivation (:14) and Related Work (:324) — not merely in the changelog,
which is exactly the failure mode finding #40 caught in ZW2.

**Process lesson — a fix is not applied until it is applied to every artifact that repeats it.**
Rounds 4 and 7 each ended with a version of this lesson; round 9 is the third instance and the
sharpest, because in #37 the stale sentence and its correction sit **in the same section, one
paragraph apart**, and in #38 and #39 the withdrawn vocabulary survived specifically in **Related
Work** — the section every round read last, when it read it at all. Related Work is where a
withdrawn design hides longest: it is written early, it restates the contribution in its own words,
and no later fix to the method section touches it. The mirror question ("what *else* says this?")
belongs in the fix, not in the next round.

**Near-miss worth recording.** An intermediate grep in this round, truncated with `cut -c1-175`,
appeared to show that ZW3's FM-alpaca concession existed only in the revision log — it would have
been written up as the round's headline major. The concession was in the body all along, past the
truncation column. Truncated tool output is evidence about the first 175 bytes of a line and nothing
more; every finding here was re-checked untruncated before being written down.

## Round 10 — 2026-08-23 deer-flow academic-paper-review pass (four parallel web-grounded reviewers)

A different instrument from rounds 1–9: the `academic-paper-review` + `deep-research` skills ported
from `bytedance/deer-flow` (installed in `.claude/skills/`, pipeline defined in
`.claude/commands/deerflow_review.md`), run as four parallel agents, one full structured review per
package, each grounded in 8–11 logged web searches with batched arXiv verification. Full reviews in
each package's `deerflow_review_2026-08-23.md`. All four verdicts: **Weak Accept as pre-registered
designs, Moderate contribution.** Three findings were applied same day (the fixes below); the
remaining review content — power-analysis gaps, feasibility budgets, gate-design critiques — is
recorded in the review files as open advisory findings, not applied.

- **ZW1 [major, fixed]** RQ4 still asserted *"the 32 typed reward packets"* as the probe input — the
  fourth survivor of the withdrawn fixed-`K=32` design, missed by round 9 because it names the probe
  input rather than the packet-emission rule. Now states the variable-count rule. (Manuscript only;
  spec was already correct.)
- **ZW2 [major, fixed]** The round-9 estimand fix reached Related Work but not Method/Experiments:
  five passages still carried the reversed `V−B` form, including a Methodology sentence defining the
  candidate-level gap as `V−B` one sentence before the aggregate correctly used `A_i−B_i`. All five
  now state raw acceptance `A` as primary; the spec's D2 prose ("joint (V,B) distribution") mirrored
  to (A,B).
- **ZW4 [major, fixed]** The round-8 sweep's three ordered citations (Orlanski et al. 2506.10056,
  Mitsuhashi et al. 2605.25252, JURY-RL 2604.25419) existed only in the seed ledger — Related Work
  had never absorbed them, and the intro still carried the "unmeasured" universal JURY-RL falsifies.
  Both fixed; ids re-verified in one batched arXiv request.
- **ZW3 [none applied]** Review passed with no manuscript-side consistency defect; its findings
  (compute accounting, RQ3 gate-failure risk, pretraining-familiarity confound) are design-level
  advisories logged in the review file.

The round-9 pattern held for a third consecutive round: every applied fix was a defect repaired in
one artifact and never mirrored into a sibling (spec→manuscript for ZW1, Related-Work→Method for
ZW2, seed-ledger→manuscript for ZW4).
