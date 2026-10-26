# Design Review (adversarial, 2026-07-04)

> Reviewer role: skeptical PC member, design-only pass over the pre-registered spec.
> Files read in full: `goal.md`, `guidance.md`, `README.md`, `digest.md`, `paper.md`,
> `discussion/reference_candidates.jsonl` (158 records), `discussion/stage_review.md`,
> `discussion/pipeline.md`, `discussion/taste_audit.md`, `discussion/paper_draft.md` (spot-checked).
> The recorded "Phase A (re-run) → clear to proceed" verdict was NOT trusted; every item
> relied on below was independently re-verified against file contents.
>
> **Staleness note (recorded once):** `discussion/paper_draft.md` reflects the Stage-4
> falsification-condition fix (six "Falsification condition" lines present) but does NOT
> contain the Phase-A-re-run additions made to `paper.md` (thin-cell INCONCLUSIVE policy:
> zero matches; R1 estimand line; A* Gate/Consequence fields). It is stale relative to
> today's `paper.md` and is not penalized further below.

---

## Verdict summary

| Dimension | Score | One-line reason |
|---|---|---|
| 1. Feasibility & scale | **FIXABLE** | Real datasets + cheap skeleton, but the LLM-call estimate is off by 10× and two baseline arms (UTRL-style, SWE-RM-style) require training runs the spec elsewhere says don't exist. |
| 2. Soundness | **BROKEN** | H1/E1 as pre-registered ("certified shortcut-free **over the same space**", variants "**sharing GT**") is logically unsatisfiable — the central existence experiment is guaranteed to return FAIL by pure Boolean algebra; also B0 is not null-by-construction. |
| 3. Novelty & pre-emption | **FIXABLE** | Differentiation from all `selected` twins is real and the asymmetry is genuinely non-obvious, but pre-emption was checked only against a 2025-12→2026-07 arXiv/OpenReview window — the classical ensembles-of-weak-defenses / N-version-diversity literature was never harvested. |
| 4. Hypothesis→fallback robustness | **FIXABLE** | Every H* has a verbatim fallback, but the combination space has holes (H1-fails-OR-only uncovered; H1-fail∧H2-pass routes to an F-G1 whose pivoted abstract would then be factually false; H3a/H3b mixed outcome uncovered), and — given finding S-1 — the design deterministically lands in F-G1 asserting a wrong conclusion. |
| 5. Method scope & RQ design | **FIXABLE** | Envelope stated, A2 kill list mostly pre-empted, mechanism analysis budgeted; missing: placebo arm, attacker-generality ablation, B_cert-sensitivity analysis, and above all a definition of what actually differs between task variants. |
| 6. Prior Phase A PASS reliability | **partially reliable** | Real gaps were genuinely found and fixed (estimand, R2 for M4, thin cells, cache backfill honestly flagged), but item 5 was declared fixed while A6 still lacks its failure_mode slot, Part 6 item 5 (B0 placebo) was passed without a placebo existing, and "clear to proceed to Phase B" contradicts goal.md §3's one-failure-blocks rule given the openly unresolved item-2 residual. |

**Overall: NEEDS-REVISION** (one BROKEN finding with a concrete repair path; everything else is repair-in-place).

---

## Findings (ranked most-severe first)

### S-1 [BROKEN] — H1 as pre-registered is logically unsatisfiable; the pilot cannot produce the headline result

**Evidence.** `paper.md` Step 5 Notation (line 32): "Task variants per M1: tuple ⟨T, t_A, t_B, t_∧, t_∨⟩ **sharing GT**." `paper.md` E1/H1 (line 62): "composed gate accepts a GT-failing candidate over the fully enumerated space while both single-verifier variants are certified shortcut-free **over the same space**."

**The problem.** Take the literal reading: one enumerated candidate space S, one shared GT, the same verifiers A and B across variants.
- **AND:** (A∧B)(c)=accept ⇒ A(c)=accept. If GT(c)=0, then c is a shortcut against A alone over S — contradicting Sound(A, t_A, exhaustive)=1. So no AND-emergent shortcut can exist.
- **OR:** (A∨B)(c)=accept ⇒ A(c)=accept ∨ B(c)=accept; either branch contradicts the corresponding exhaustive single-gate certificate. So no OR-emergent shortcut can exist.

Worse: for Sound(A, t_A, exhaustive)=1 to hold at all over the same space and the same GT, A's finite unit-test suite must already kill *every* GT-failing candidate in S — i.e., A alone must be extensionally perfect on S, at which point composition is trivially sound. This is exactly the "extensional triviality" the paper's own Step 0 identifies and promises to escape ("the conjunction of two extensionally sound acceptors on a fixed set is trivially sound"). E1's operationalization silently collapses back into it. The digest's own worked examples confirm the incoherence: N6's "OR-gate whose weaker branch admits a degenerate solution" means that branch's single gate was never sound; N6's "AND-gate whose resource constraint forces solutions into a lookup-table region where A's finite test suite loses discrimination" means A was never sound over S. Under exhaustive enumeration, the "distribution shift" mechanism (C4, Step 0) cannot operate — enumeration checks every candidate regardless of what distribution a solver would induce.

The only escape hatches are (a) per-variant candidate spaces that differ (t_A certified over S_A ≠ S_∧), or (b) per-variant facet ground truths (Sound(A) certified against GT_A, the emergent shortcut failing the full GT). Both are plausibly what the author *meant* — the Step-0 asymmetry ("valid only relative to the facet it checks and the candidate distribution its own gate induces") points at exactly this — but **neither is defined anywhere in M1, Step 5, or E1**, and both contradict the pre-registered text ("same space", "sharing GT"). Under reading (a)/(b), the entire attribution machinery (C3's budget-matching, C4's emergence-vs-shared-blind-spot, M4's ablation triple) rests on how the variants differ, which is unspecified — a reviewer's kill would be: "your 'emergent' shortcut is just a different task; certificates were never expected to transfer."

**Consequence.** As written, the walking skeleton (Step 9) will run, mechanically answer NO, gate S-1 will loop forever on "construction restarts" (A2's consequence), or E1 will FAIL both rules and route to F-G1 — whose pivoted abstract then asserts "Boolean composition of two facet-certified verifiers preserved soundness in every constructed and benchmark condition," a tautology dressed as a finding. The pre-registration machinery would faithfully deliver a wrong paper. This is the flaw the design phase exists to catch.

**Concrete fix.** Redefine the certification relativization explicitly and pre-register it:
1. Give each single-verifier variant its **own facet ground truth** GT_A/GT_B (per-facet differential corpora) and/or its **own certification space** S_A ⊆ S_∘, with the relationship between spaces stated as part of M1's tuple definition.
2. State the **matchedness argument**: what is held constant (spec, full-task GT, DSL grammar) and what varies (facet spec shown to the certifier, facet corpus), and why that variation mirrors real practice (each deployed verifier really is certified on its own facet/distribution — cite the SWE-RM/R2-Guard practice already in the cache).
3. Turn the impossibility proof above into an **asset**: the same-space/same-GT configuration is provably null — make it the missing B0 placebo (see S-2). A run that finds an "emergent shortcut" in that configuration has a pipeline bug by theorem.

### S-2 [BROKEN→FIXABLE] — B0 is not null-by-construction; guidance §3.3 job (b) is unfilled and Phase D step 1 cannot execute

**Evidence.** `paper.md` Mandatory baselines: "**B0 — 'why do this at all' control:** the **no-composition arms** — verifier A alone and verifier B alone, each attacked on its own variant at the identical budget." guidance.md §3.3: B0 must also be "a null-by-construction placebo (shuffle labels/years/assignments) whose effect must be null. **Non-null placebo = ... the whole run is invalid.**" goal.md §5 step 1: "Placebo first. B0 non-null → run invalid."

**The problem.** The spec's B0 fills only job (a) (premise-collapse arm). There is no arm whose result is null *by construction*, so Phase D's mechanical "check B0 first, non-null invalidates the run" has nothing well-defined to check — "B0 non-null" is not even defined for the single-gate arms. Worse, at Stage 1 the single gates are *selected* to have zero attacker successes at B_cert using the very attacker later used in the H2 comparison; FAR(strictest single)≈0 is then partly a selection artifact (winner's curse), and "FAR(composed) > FAR(single)" is partially baked in. The 10× re-attack mitigates but does not remove this, because the comparison arms and the certification pass share attacker randomness.

**Concrete fix.** (i) Add a true placebo: a **self-composition arm** (A∧A′, two independently sampled instantiations of the same check, or the same-space/same-GT configuration from S-1's impossibility proof) whose emergent-gap rate must be exactly zero; non-zero ⇒ run invalid. (ii) Use **fresh, disjoint attacker randomness** (new seeds/attempt pools) for the comparison attacks vs. the certification attacks, and state it in E2's Verification.

### S-3 [FIXABLE] — Fallback-combination rules have holes, and one routing is self-contradictory

**Evidence.** E1 fallback: "If H1 fails for AND only, ... scoped to OR-style gates ... **If both fail → F-G1**." F-G1's own trigger: "If the central family fails (**H1 fails for both rules, and H2 shows no composed>single effect anywhere**)." guidance.md §3.1: "**Write the fallback-combination rules too** ... never invent combination logic at verdict time."

**The problems.**
1. **H1 fails for both rules but H2 passes** (bounded DSL too poor to express real shortcuts, yet the adversary finds them at benchmark scale — a realistic outcome): E1's rule sends this to F-G1 wholesale, but F-G1's trigger is not met, and F-G1's pre-committed pivoted abstract ("preserved soundness in every constructed **and benchmark** condition") would be factually false. The two triggers contradict; verdict-time improvisation would be forced.
2. **H1 fails for OR only** (AND succeeds): no pre-committed wording exists — only the AND-only branch is covered.
3. **H3a passes, H3b fails (or vice versa):** the E3 fallback covers only the joint failure ("If H3a/H3b fail"); `paper_draft.md` RQ6 likewise defers to "the joint fallback claim if both ... fail together." Mixed outcome uncovered.
4. **H3a wrong direction** (significantly *negative* complementarity coefficient): the fallback wording "no cheap pre-deployment warning signal was found" would be wrong — an inverted signal IS a signal, and per guidance Part 4 situation 4 it must be reported at full prominence with re-derived implications; no wording is pre-committed.

**Concrete fix.** Write the full 2×2(×2) outcome lattice for {H1-AND, H1-OR} × H2 with a verbatim sentence per cell; align E1's routing with F-G1's trigger; add wordings for the H3 mixed and wrong-direction cells.

### S-4 [FIXABLE] — F-G1's negative-result pivot does not meet the S9 rigor bar

**Evidence.** F-G1 pivoted abstract: "composition ... preserved soundness in every constructed and benchmark condition — bounding the composition risk that reward-hacking folklore attributes to multi-check gates." guidance.md S9: "your power analysis must show you *could* have detected E; an underpowered non-detection is nothing."

**The problem.** The pivot paper's evidence would be "we failed to construct counterexamples in our bounded DSL and our one attacker found nothing at N=500." The construction failure carries no coverage argument (exhaustive over *candidates*, not over *task families* — nothing bounds how representative the 5 hand-built families are), and the attack failure is attacker-specific (single fixed model/scaffold). A reviewer kills this with "you didn't look hard enough." **Fix:** pre-register what would make the null credible — an enumeration over a parameterized task-family grid (not just candidate space), ≥2 structurally different attackers, and the discovery-vs-budget curves showing saturation.

### S-5 [FIXABLE] — Feasibility arithmetic is off by 10×, and two baseline arms contradict the "no training runs" claim

**Evidence.** `digest.md` N6 feasibility (line 373): "~200 tasks × ~6 verifier-pair types × 5 gates ... × 500 attacker attempts **≈ 3×10^5 LLM calls** — mid-size API cost class (~$1k–$3k)." Actual product: 200 × 6 × 5 × 500 = **3×10^6**, before the mandatory 10× re-attacks (A3) and 3-of-3 verdict-stability judge calls (t5). Cost class is ~$10k–$30k, an order of magnitude above what was budgeted. Same file: "**No training runs required**" — yet E4's arm is "UTRL-style adversarially hardened single test suite" (UTRL *trains* a test generator via adversarial RL) and one verifier-pair type is "SWE-RM-style execution-free reward model" (a trained trajectory RM whose checkpoint availability is unverified, and whose trajectory-level design does not obviously transfer to function-synthesis tasks). The R2-Guard-style arm "presupposes the inter-check rules are known" (the paper's own N4 limitation 4) — no rules are specified for heterogeneous test×static pairs.

**Concrete fix.** Redo the budget table with the correct call count and re-attack/judge multipliers; for each of the three borrowed arms, pre-register either (a) the training budget and data, or (b) a named training-free approximation (e.g., iterative EvalPlus-style test augmentation as "hardening") with a sentence conceding the fidelity loss. Also: EvalPlus amplification exists for HumanEval/MBPP but **not** for BigCodeBench/LiveCodeBench — generating the required |D|≥10⁴ differential corpora for library-heavy BigCodeBench tasks is unbudgeted engineering; state the protocol or drop the dataset.

### S-6 [FIXABLE] — Pre-emption verified only against a 7-month, LLM-only harvest window

**Evidence.** All 158 cache records are arXiv 2512.*–2607.* or the local OpenReview corpus; the mass of wildly off-topic rejects (prosthodontics QA, travel-planning benchmarks, IoT method decoration) indicates a bulk recent-window dump filtered post hoc rather than the ≥4–5 query-angle harvest goal.md §1 prescribes. The novelty claim ("no retrieved paper studies the AND/OR soundness algebra of two individually certified verifiers") is therefore verified only within that window.

**The risk.** The closest classical work was never queried: *ensembles-of-weak-defenses* results in adversarial ML (composing defenses does not compose robustness), N-version programming / fault-diversity reliability theory (Littlewood-style failure-correlation analysis of "independently validated" components), SE test-adequacy composition, and security defense-in-depth failure analyses. The differentiation likely survives (those literatures compose *weak or statistically-characterized* components; here each component carries an individual soundness *certificate*, and the estimand is the composed gate's certified-relative false acceptance) — but that concession-and-differentiation must be *in the paper*, not discovered by Reviewer 2. **Fix:** one targeted re-harvest pass on the angles "ensemble of defenses," "N-version programming reliability," "defense in depth failure," "test suite composition adequacy" before Phase E; add the strongest hit as a `contrast` record.

### S-7 [FIXABLE] — Claim–Evidence Map: the prevalence headline (H2) has no claim row

**Evidence.** Map rows trace Claims 1→H1, 2→H3a/H3b, 4→H4; H2 appears only inside Claim 3's conditionality ("conditional on H1∧H2"). Abstract v0 promises "how often a matched adversary finds them across 200 benchmark tasks" as a headline deliverable, yet no claim row licenses a prevalence statement. Under goal.md §5.7 ("claim_map.md is the only ground truth for what the paper claims"), the paper's main quantitative result would be unlicensed at splice time. **Fix:** add a Claim row "Composed gates show higher unsound acceptance than their strictest component at matched budget, at rate X (CI)" → H2 (E2), fallback-covered.

### S-8 [FIXABLE] — Residual instrument/protocol gaps

1. **A6 lacks its failure_mode slot** — A1–A5 each carry "*Failure/Failure mode:*"; A6 (grid feasibility) jumps from the assumption to *Detection* (verified by grep: "Failure" appears in lines 51–55 only). The Phase A re-run (stage_review item 5) asserted all six "stated failure_mode and detection"; false for A6.
2. **A1's human adjudication is an instrument without an R2 plan**: "human adjudication of a 100-shortcut sample (≥90% ...)" names no rater count, no agreement threshold, no adjudication rubric — guidance R2 treats asserted validation without protocol as absent. (E3's taxonomy labeling has full R2; the *intent-violation* adjudication does not.)
3. **M4's R2 step ② may be infeasible as written**: the calibration set is "the first 20 pilot-family shortcuts," but the pilot needs only ≥1 shortcut per family in ≥3 of 5 families — there may be fewer than 20 pilot shortcuts in total. Pre-commit a fallback source (scale-up burn-in sample).
4. **H2's INCONCLUSIVE arithmetic is ambiguous**: "H2's '≥4 of 12' count is then evaluated only over the non-INCONCLUSIVE cells" — does the threshold stay at 4 when only, say, 5 cells remain scorable? State the rule (e.g., ≥⌈k/3⌉ of the k scorable cells, with a minimum k).
5. **Dependence structure of the secondary analysis**: the 1,200-cell logistic regression reuses the same 200 tasks across 6 pair types; cluster-robust (task-level) standard errors are needed and unstated. (Holm over the 12 primary McNemar comparisons is valid under dependence — no issue there.)
6. **"Task difficulty" (H3a's control covariate) has no row in the term→definition→measurement table.**

### S-9 [NOTE] — What is genuinely good here

For calibration: the Step-0 asymmetry passes the deletion test with an unusually strong argument (the generic residue is *provably false*, so the domain nouns carry the claim); the verb audit is clean (certify/attack/isolate/classify — no bridge framing, confirmed independently by `taste_audit.md`'s 0/0/3 diagnostics); the walking skeleton is genuinely cheap (1 task, CPU-only, ≤4h) with a config-not-code gate; the 10×-re-attack rival control (B-alt) is a well-designed budget-symmetry falsifier; the thin-cell INCONCLUSIVE policy and the M4 R2 protocol added in the Phase A re-run are real rigor, not paperwork. The skeleton, ironically, is also the fastest way to *discover* S-1: it would return NO on its first run.

---

## Failure-space simulation (per-H walk-through)

| Outcome | Pre-committed route | Survives review? |
|---|---|---|
| **H1 passes both rules** | Main claim (CO1) | Only if S-1 is fixed — as written this outcome is logically unreachable. |
| **H1 fails AND only** | E1 fallback verbatim (warning scoped to OR gates) | Marginal: an OR-scoped warning invites "OR-gates weakening is folklore"; needs the facet-certificate framing to stay non-trivial. Covered. |
| **H1 fails OR only** | **UNCOVERED** — no wording exists (S-3.2). | — |
| **H1 fails both, H2 passes** | **CONTRADICTORY** — E1 routes to F-G1, F-G1's trigger unmet, its pivoted abstract would be false (S-3.1). Ironically this is a *good* outcome scientifically (real-world prevalence without toy construction) with no sentence to claim it. | — |
| **H1 fails both, H2 fails** | F-G1 negative-result pivot | Weak as written — no S9 power/coverage argument (S-4). And per S-1 the unfixed design lands here *deterministically*, publishing a tautology as a finding. |
| **H2 fails, H1 holds** | E2 fallback verbatim ("tail event conditioned on pair structure") | Yes — honest and publishable alongside H1's existence certificates. Covered. |
| **H2 mostly INCONCLUSIVE (thin cells)** | Policy exists but threshold arithmetic ambiguous (S-8.4). | Partially covered. |
| **H3a passes, H3b fails (or vice versa)** | **UNCOVERED** — only joint failure has wording (S-3.3). | — |
| **H3a significant in the WRONG direction** | Fallback wording ("no signal found") would be inaccurate; situation-4 prominence handling not pre-committed (S-3.4). | — |
| **H3a/H3b both fail** | E3 fallback verbatim ("composed gates must be attacked directly to be audited") | Yes — genuinely strengthens CO2. Covered. |
| **H4 fails** | E4 fallback verbatim | Yes. Covered. |
| **H4 passes while H1/H2 fail** | Claim 4's text says it "follows from Claims 1–2"; if those fell, H4's standalone meaning is undefined. Minor uncovered corner. | — |
| **B0/placebo non-null** | Cannot fire: no null-by-construction arm exists (S-2), so Phase D step 1 is inexecutable. | — |

**Is there any outcome that leaves the paper with nothing?** Yes, and it is the *default* one: with S-1 unfixed, the run deterministically produces H1-double-FAIL, routes to F-G1, and ships a pivoted abstract whose "preserved soundness in every constructed condition" is a logical tautology, not a measurement — worse than nothing, because it is a confident wrong conclusion. With S-1/S-2/S-3 fixed, coverage is good: every remaining branch ends in a publishable, honestly-worded paper.

---

## Missing RQs / reviewer questions the design cannot currently answer

1. **"What exactly differs between t_A and t_∧, and why is that a fair comparison?"** — the single most load-bearing design element, currently undefined (S-1). No RQ or arm validates variant matchedness.
2. **"Would a different attacker find the same gaps?"** — one fixed LLM attacker; no attacker-generality ablation (≥2 structurally different attackers, e.g., LLM red-team vs. mutation/CEGIS-style search, at matched budget). Without it, every rate in H2/H3 is a property of one model's search bias.
3. **"How do emergent-gap rates depend on B_cert?"** — digest N6's mitigation promises "report emergent-gap rates as a function of B_cert," but no E* experiment or analysis-plan line carries it; the certificate-strength sensitivity curve is the paper's main defense against "budget-stamped soundness is arbitrary."
4. **"Where is your placebo?"** — the A2-archetype mandatory shapes are: measurement grid (present), rival arm (present), power per cell (present), **placebo arm whose effect must be null (absent — S-2)**.
5. **"Do real pipelines actually gate on your pair types?"** — Claim 3's "普适警告" is scoped by t3, but no arm or citation-based analysis establishes that the studied 6 pair types match deployed stacks (the cache's SWE-RM/R2-Guard/FAPO records could carry this as a design-argument paragraph; currently unassembled).
6. **"Is your OR result anything but a weak-branch tautology?"** — needs the facet-certificate framing made airtight (S-1 fix), plus an explicit argument distinguishing "composition manufactured the gap" from "you attached a weaker check and took the union."
7. Clustered-dependence handling in the H3a regression; rater protocol for the A1 adjudication (S-8.2, S-8.5).

---

## Reliability audit of prior Phase A PASS

Re-verified independently: items 4, 5, 6 (the most rubber-stamp-prone), plus item 2's reference records.

**What held:**
- **Item 1 (digest self-verification):** spot-checked — all N4 `affects_works` keys appear verbatim in N3 (9/9); N8's C/M/CO references resolve; N9 rq_ids ⊆ N8; N10/N11 carry full 3-part absence comments. PASS was earned.
- **Item 3 (tag discipline):** no untagged assertions found; Abstract v0 is explicitly marked "targets, not findings." PASS was earned.
- **Item 2 (cache integrity), partially:** the recorded REVISE was *honest work* — the 9 N3 citations genuinely were missing from the cache and were backfilled; the 8 backfilled records honestly carry `id_resolves: false`, `pdf_path/digest_path: null`. Disk check (this review): all 7 harvest-selected records' `pdf_path`/`digest_path` resolve (verified for SWERM2512, Theoria2607, Preguss2512, PatchFusion2607, CertSpecExec2606, JailbreakFilters2512, SEACertificates2607). Cross-topic contamination check on 3 selected `why` fields: Theoria2607 (Jaccard-complementarity twin), JailbreakFilters2512 (real AND-composed safety gate), Preguss2512 (assumed-safe static+deductive composition) — all three are specific to B1.4's question, not boilerplate from another topic. Clean.

**What was rubber-stamped or overstated:**
1. **Item 5 ("Fixed directly in paper.md ... every one of A1–A6"):** A6 still has **no failure_mode slot** (A1–A5 do; grep confirms). The review asserted "A1–A6 stated failure_mode and detection" — false for A6.
2. **Item 5 again — fallback-combination rules:** guidance §3.1 explicitly requires them ("write the fallback-combination rules too"); the recorded PASS never checked the combination lattice, which has three holes and one contradiction (S-3). This is precisely the check goal.md item 5 "(incl. effect floor + verbatim fallback)" was supposed to enforce in depth.
3. **Item 6 (Part 6 self-check):** Part 6 item 5 requires "B0 + B-alt + F-G* all present with pre-committed wording" — recorded as PASS, but B0's null-by-construction placebo half (guidance §3.3 job (b)) does not exist (S-2). Part 6 item 10 ("evidence standard ... met by the plan — not by intention") missed that the A2 archetype's mandatory placebo arm is absent and that E1's core criterion is unsatisfiable (S-1) — the deepest miss, though admittedly one that requires actually simulating the experiment rather than checklist-matching it.
4. **Item 4 (claim–evidence orphans):** technically PASS by the letter (every claim has an H-id or supported-by-design tag; every H has a fallback), but H2 — the paper's headline quantitative result — has no claim row (S-7); the checklist's letter was satisfied while its purpose (splice-time licensing) was not.
5. **The bottom line "GATE RESULT: REVISE (fixed in this pass) → now clear to proceed to Phase B"** overstates: goal.md §3 is a binary all-clear gate ("one failure blocks Phase B"), and item 2's residual (8 load-bearing `baseline`/`method-twin`/`contrast` records with no digests, `id_resolves: false`) is an acknowledged open failure of §3 item 2 / §1 step ②. The honest status was "Phase A not passed; pre-B TODO list," not "clear to proceed." The transparency is commendable; the verdict wording is not supported by the runbook.

**Net:** partially reliable — the re-run did real, verifiable repair work and flagged its own residuals honestly, but its PASSes on the machinery items (5, 6) were checklist-shaped rather than adversarial, and the one flaw that decides whether the paper can exist at all (S-1) sailed through.

---

## Overall: NEEDS-REVISION

Not UNSALVAGEABLE: the asymmetry is real and well-argued, the taxonomy/complementarity apparatus is genuinely novel within the verified window, the skeleton is cheap, and the S-1 repair is a definitional redesign, not a new idea. Not SOUND: as pre-registered, the central experiment cannot succeed and the pre-committed failure route publishes a tautology.

**Three highest-leverage fixes (do before any Phase B spend):**

1. **Fix S-1 — redefine certification relativity in M1/Step 5/E1.** Give single-verifier variants per-facet ground truths and/or per-variant certification spaces, pre-register the exact variant-construction rule and the matchedness argument, and re-derive H1's criterion so it is satisfiable-but-falsifiable. Then convert the current same-space/same-GT configuration into the null-by-construction placebo (which simultaneously fixes S-2 and makes Phase D step 1 executable).
2. **Fix S-3 — write the complete fallback-combination lattice** ({H1-AND, H1-OR} × H2, H3 mixed and wrong-direction cells), and reconcile E1's F-G1 routing with F-G1's trigger so the H1-fail∧H2-pass outcome — currently contradictory — gets its own (strong!) pre-committed claim sentence. Add the S9 power/coverage plan that makes F-G1's negative result survivable.
3. **Fix S-5 + S-6 — re-budget and re-harvest.** Correct the 10× LLM-call arithmetic (≈3×10⁶ calls, ~$10k–$30k class), resolve the UTRL/SWE-RM training contradiction with pre-registered training-free approximations or explicit training budgets, specify the BigCodeBench differential-corpus protocol, and run one targeted harvest pass over the classical composition-failure literatures (ensembles of weak defenses, N-version diversity, defense-in-depth) so the novelty claim is defended against the reviewer most likely to kill it.

---

## Fixes applied (2026-07-04)

Direct edits authorized by the coordinator after this review; applied to `paper.md` and `digest.md` (surgical, style-matched, no fabricated numbers). One line per edit:

1. `paper.md` Step 5 Notation — replaced "sharing GT" tuple with per-variant certification spaces S_v ⊆ S_∘ + pre-registered extension rule, named the R3 confound this removes, and reserved the provably-null same-space configuration as placebo B0-P (fixes S-1 core).
2. `paper.md` Step 5 "sound" table row — pilot Π now enumerates the variant's own space S_v; scale-up Π uses an independent certification attacker 𝒜_cert (different model/prompt/seed family from 𝒜) with the winner's-curse selection confound named per R3 (fixes S-2 selection artifact).
3. `paper.md` E1/H1 criterion — rewritten to "shortcut-free over their own exhaustively enumerated certification spaces S_A, S_B" with an explicit note that the same-space reading is impossible and serves as B0-P (fixes S-1 unsatisfiability).
4. `paper.md` E1 Metric — S → S_∘ with per-space certificates, matching the new H1 criterion.
5. `paper.md` E1 Fallback — expanded to the full pre-committed combination lattice: added the H1-fails-OR-only branch, restricted the F-G1 route to H1-both-fail ∧ H2-fail (matching F-G1's own trigger), and wrote a verbatim claim sentence for the previously contradictory H1-both-fail ∧ H2-pass cell (fixes S-3.1, S-3.2).
6. `paper.md` E2 Verification — certification now uses 𝒜_cert; comparison attacks draw randomness never used for certification selection (fixes S-2 in the sweep protocol).
7. `paper.md` E3 Fallback — added pre-committed mixed-outcome wording (exactly one of H3a/H3b holds) and wrong-direction wording (significantly negative complementarity coefficient reported at full prominence per situation 4) (fixes S-3.3, S-3.4).
8. `paper.md` E4 Metric/Verification — pre-registered training-free instantiations: UTRL-style hardening as iterative adversarial test augmentation (fidelity loss conceded in Limitations), execution-free RM as released checkpoint or prompted proxy, else A6 grid-shrink (fixes S-5 training contradiction).
9. `paper.md` Mandatory baselines — B0 split into B0-C (current-practice) and B0-P (null-by-construction placebo: same-space composition in the pilot, self-composition A∧A′ at Stage 1), evaluated FIRST per goal.md §5 step 1, nonzero ⇒ run invalid ⇒ situation 1 — guidance §3.3 job (b) now filled (fixes S-2 placebo absence).
10. `paper.md` A6 — wrote the missing *Failure mode* slot (pair types failing to instantiate at scale; RM type unavailable without training; grid below 12 comparisons or thin-cell floor) (fixes S-8.1).
11. `paper.md` Step 9 Walking Skeleton — per-variant spaces S_A/S_B/S_∨ with the manifest extension rule; added arm 4 (placebo B0-P re-certified over S_∨, must find nothing, a hit fails the skeleton); pass criterion and cost updated (≤8h; per-variant DSL bounds + extension rule in the config manifest).
12. `paper.md` Abstract v0 — added the independent certification attacker and the provably-null same-space placebo to the rival-control sentence.
13. `digest.md` N6 M1 — per-variant certification spaces + extension rule + placebo reservation, consistent with paper.md Step 5.
14. `digest.md` N6 M2 — scale-up certifier changed from "the same adversarial searcher as M3" to an independent certification searcher, with the selection confound stated.
15. `digest.md` N6 feasibility — corrected 3×10^5 → 3×10^6 attacker LLM calls (200×6×5×500), added re-attack/judge-call overhead, revised cost class to ~$10k–$30k, and stated the training-free instantiations that keep "No training runs required" true.

**Not addressed in this pass (needs human decision or compute):** H2 claim row in the Claim–Evidence Map (S-7); A1 human-adjudication R2 protocol (rater count/κ threshold) (S-8.2); M4 R2 step-② calibration-set size fallback (S-8.3); H2 INCONCLUSIVE threshold arithmetic when scorable cells < 12 (S-8.4); cluster-robust SEs for the H3a regression (S-8.5); "task difficulty" definition row (S-8.6); attacker-generality ablation and B_cert-sensitivity analysis (missing-RQ items 2–3); F-G1 S9 power/coverage plan (S-4); classical-literature re-harvest (S-6); extraction-mode digests for the 8 backfilled reference records (pre-Phase-E TODO); regeneration of stale `paper_draft.md`/`.tex`/`.pdf` to reflect today's `paper.md` changes.
