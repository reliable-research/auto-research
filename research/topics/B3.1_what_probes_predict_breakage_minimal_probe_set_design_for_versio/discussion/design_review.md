# Design Review (adversarial, 2026-07-04)

Reviewer: skeptical senior PC member. Scope: `README.md`, `digest.md`, `paper.md`, `discussion/{reference_candidates.jsonl, stage_review.md, pipeline.md, paper_draft.md}`. The recorded "Phase A (re-run) PASS" was independently re-verified, not trusted. Fixes were applied directly to `paper.md` and `digest.md` (logged at the end).

## Verdict summary

| Dimension | Score | One-line reason |
|---|---|---|
| Feasibility & scale | FIXABLE | Toy corpus concrete and obtainable; but skeleton did not exercise the riskiest components (placebo, noise-floor re-decode, collinearity path, semantic-diff κ) — now amended. |
| Soundness | FIXABLE→ (BROKEN placebo + power, both fixed) | B0 was a performance floor mislabeled as the placebo (no null-by-construction arm existed); `|P|≈20` was asserted to power a ρ=0.30 ranking claim that actually has ≈0.25 power. Both fixed. |
| Novelty & pre-emption | FIXABLE | Method-twin (BSM) genuinely differentiated; verb check clean; but the recent-only harvest missed the classical test-suite-minimization and concept-drift threads that are the direct pre-LLM analog — conceded now. |
| Hypothesis→fallback | FIXABLE | H1–H6 mostly complete; H5 was a bare failure-to-reject null (rubber-stamp risk); combination rules were implicit; forward/prospective validation absent. All added. |
| Method scope & RQ | SOUND (after fixes) | A2 mandatory shapes now all present (placebo added, power honest, mechanism = H6); envelope stated; RQ set covers the A2 kill list. |

## Findings (ranked most-severe first)

### 1. [BROKEN→FIXED] B0 is a performance floor mislabeled as the placebo; no null-by-construction arm existed
Evidence (`paper.md`, original Mandatory baselines): *"B0 — 'why do this at all' control … a **constant base-rate breakage predictor** using no probe features (predicts E[B̄]). If the full battery … fails to beat B0's AUC/Brier … the entire premise … collapses."* This is guidance.md §3.3 job (a) only. A constant predictor cannot "come out non-null by artifact," so Phase D's "placebo first / non-null ⇒ run invalid" gate (goal.md §5, guidance.md §3.3(b), situation 1) had **nothing to fire on**. This is exactly the fleet's most common defect: a no-signal comparison arm wearing the placebo label. A leaking pipeline (CV grouping leak; a per-pair nuisance — prompt length, decode temperature — shared by drift `D` and breakage `B̄`) would sail through undetected.
**Fix applied:** added **P0 — null-by-construction label-shuffle placebo** (permute the `D(p)↔B̄(p)` correspondence across pairs, re-fit the identical predictor/CV path; `π`/AUC CI must include the null over ≥1000 shuffles; non-null ⇒ run invalid, checked before any H\*). Relabeled the constant predictor as **B0 — no-signal performance floor**. Added Claim-Map row 6b, R3 confound line, and a PG-P0 gate in the skeleton.

### 2. [BROKEN→FIXED] The central ranking test is severely underpowered; `|P|≈20` was falsely asserted to suffice
Evidence (`paper.md` original A6): *"`|P| ≈ 20` pairs suffice for a ranking claim."* But `π_f = |Spearman ρ(D_f(p), B̄(p))|` and the joint fit both have effective n = **number of pairs**, not the ≈400 `(p,t)` cells (cells collapse into `B̄(p)`; the bootstrap/grouped-CV correctly resample at the pair level). Independently computed (Fisher-z, two-sided α=0.05): power to detect a true ρ=0.30 (the H1 floor) is **0.25 at n=20, 0.47 at n=40, 0.65 at n=60, 0.80 only at n≈85**. H1's real test — paired-bootstrap CI on `π_top − π_cap` lower-bound `>0`, Holm across 10 pairs — needs *more* than a single correlation. The "per-cell power floor (≥50 inputs)" the prior Phase A added protects the within-cell breakage estimate but is orthogonal to the pair-level correlation's df. **The confirmatory claim the paper's headline rests on was not powered.**
**Fix applied:** rewrote A6 with the honest arithmetic and a pre-committed power policy: `|P|<40` → H1 EXPLORATORY; `40≤|P|<60` → INCONCLUSIVE (never FAIL); confirmatory PASS/FAIL only at `|P|≥60`; corpus target raised to `|P|≥60` (config-not-code via more archived open-weight successions). Added a power gate to H1.

### 3. [FIXABLE→FIXED] Walking skeleton did not exercise every riskiest component (config-not-code claim was false)
Evidence (`paper.md` original Step 9): skeleton ran `ref`,`cap` only, *"fixed decoding only and does not re-sample"* (so the A2 noise-floor null — which gates every ranking claim — was never exercised), 2 families (so VIF/partial-correlation M7/H6 could not run), no shuffle placebo, and deferred the semantic-diff human-κ (the one subjective component of the ground truth) entirely to Phase C. goal.md §4 requires R2/PG-* gates to run *inside* B. Several riskiest components were first met at scale — the definition of a failed skeleton.
**Fix applied:** skeleton now runs 3 families (`ref`,`cap`,`fmt`) exercising the VIF/partial-correlation path; adds PG-P0 (placebo null), PG-noise (within-version re-decode null fires for ≥1 family), and PG-2 (mini human-κ ≥0.7 on the ~15 near-threshold semantic-diff cells). Pass criterion (iii)–(vi) now require all four; any that needs new code to scale = skeleton failed (situation 8).

### 4. [FIXABLE→FIXED] H5 was a bare failure-to-reject null — an underpowered test could rubber-stamp "attrition-unbiased"
Evidence (`paper.md` original H5): PASS = *"do not differ … (two-sample permutation test … α=0.05)."* With few attrited closed-API pairs this test is underpowered, and "p>0.05" then means "no evidence," not "no bias" — it would license treating the corpus as representative on no basis. No effect floor / equivalence margin (a genuine seven-slot gap the prior Phase A missed).
**Fix applied:** reframed H5 as a **TOST equivalence test** against ±0.5 SD, with an explicit effect floor, and an INCONCLUSIVE route when the attrited stratum is too thin to power the TOST (report all rankings both pooled and open-weight-only). Instrument/power failure now routes to INCONCLUSIVE, never a substantive "unbiased."

### 5. [FIXABLE→FIXED] Missing classical literature: test-suite minimization + concept-drift detection
Evidence: `digest.md` N3 harvested only recent arXiv/OpenReview; N4 absence_comment claims the composite is novel. But "minimal subset of cheap tests that retains fault-detection power" **is** regression test selection / test-suite minimization (Yoo & Harrold; Rothermel & Harrold), and "cheap monitor predicts expensive degradation" is concept-drift detection (Gama et al.). A reviewer will name these instantly; claiming first-mover status is a desk-reject risk.
**Fix applied:** added an `[UNVERIFIED — requires harvest]` block to `digest.md` N3 naming both threads with concede-and-differentiate deltas, and a concession paragraph in `paper.md` Step 3 (the defensible novelty is the black-box, axis-resolved, oracle-free *transposition*, not the minimality criterion itself). Marked UNVERIFIED throughout — no fabricated citations.

### 6. [FIXABLE→FIXED] Fallback-combination rules were implicit; no prospective/temporal validation
Evidence: each H had its own fallback, but guidance.md §3.1 requires explicit combination logic (H1-fail+H2-pass, H3-gates-H1, H6-undefined-under-collinearity, etc.), and the protocol is *sold* as a prospective "run once per version bump" tool while H1/H2 are estimated in-sample with random-pair CV.
**Fix applied:** added a pre-committed fallback-combination-rules block (incl. "<3 families survive H3 ⇒ suspend H2"; VIF≫10 ⇒ bundle-level attribution; F-G1 fires only on a *powered, P0-clean* substantive null), and a temporal-split forward-validation robustness check (fit on earlier pairs, evaluate `AUC(S*)`/rank-τ on the latest held-out pairs; reported, not a gate).

### 7. [NOTE] `paper_draft.{md,tex,pdf}` predate these `paper.md` edits (and the earlier H4–H6 additions)
The drafts were generated out of phase order (stage_review.md item 7 concedes this) and still describe B0 as the only control, no shuffle placebo, and `~20 pairs`. Noted once; not re-penalized. Phase E/G must re-splice the drafts against the corrected `paper.md` (placebo, power policy, H5 equivalence, classical concession).

### 8. [NOTE] B-alt and estimand are sound
B-alt (family-agnostic total-drift scalar, budget-matched) is the genuine strongest rival (update-magnitude confound) with pre-committed downgrade routing to F-G1 — correct. The R1 estimand is one sentence with quantity (`π_f`), unit (version pair), population (already-shipped LLM version pairs with a re-administrable input set), and decision (which minimal subset to run per bump). Both SOUND; no change.

## Failure-space simulation (per-H)

- **H1 (top family = ref/saf, π≥0.30, beats cap):** PASS → main claim. FAIL (cap #1) → RQ1 fallback verbatim. No family ≥0.30 → "multivariate" fallback → burden to H2. **Underpowered (|P|<60)** → now INCONCLUSIVE, not FAIL (fix #2). Covered.
- **H2 (|S*|≤2):** PASS → minimal-set claim. `|S*|=5` → "full battery is minimal" fallback. **<3 families survive H3** → H2 suspended (new combination rule). Covered.
- **H3 (≥3 families beat noise + τ≥0.70):** FAIL → instrument-limited downgrade of H1, gates H1/H2. Covered; now also exercised in skeleton (fix #3).
- **H4 (task heterogeneity ≥0.15):** FAIL → scope-narrowing fallback. H4-fail+H1-pass handled by combination rule. Covered.
- **H5 (attrition equivalence):** equivalence rejected → per-family narrowing + open-weight-only re-derivation. Underpowered → INCONCLUSIVE (fix #4). Covered.
- **H6 (raw-vs-partial rank disagreement):** no disagreement → near-orthogonality finding. **VIF≫10** → H6 undefined, bundle-level attribution (new combination rule). Covered.
- **P0 (placebo) non-null:** run invalid, re-run from skeleton — never scored (fix #1).
- **Whole family fails, P0 clean, powered:** F-G1 negative-result pivot. **Uncovered outcome closed:** F-G1 no longer fires on an artifact (P0 non-null) or an underpowered miss — both re-routed. No remaining outcome leaves the paper with nothing: worst case is a powered, clean substantive null, which F-G1 makes publishable.

## Missing RQs / reviewer questions the design cannot currently answer

- **Prospective/temporal generalization** — added as a reported robustness check (fix #6); a reviewer will still want it foregrounded once real data exists.
- **Cost/overhead accounting of the audit protocol** — motivated in prose but not an RQ with numbers; recommend a small deterministic RQ (queries/USD/wall-clock per version bump for `S*` vs. full downstream re-test) before submission. Not fixed (needs no design change, just a reporting table).
- **Per-family probe-instrument validity** — M1–M5 borrow cited instruments, but "is this output a refusal?" / over-refusal labeling is itself a judgment instrument; only the `B(p,t)` classifier gets a full R2 plan. Reviewer may ask for κ on the refusal/safety labelers. Left as a limitation to state.

## Reliability audit of prior Phase A PASS

Re-verified ≥3 checklist items independently:
- **Item 4 (claim–evidence orphans):** HELD structurally — every claim traces to an H-id / Step-5 def / control. But Claim 6 traced to B0, and B0 was not actually a placebo — so the map pointed at a mislabeled arm (finding #1). Rubber-stamped.
- **Item 5 (seven-slot completeness):** PARTIALLY rubber-stamped — H5 lacked an effect floor / equivalence margin (a null with no magnitude is not binary-checkable in the direction that matters); the prior pass declared A1–A7 and H1–H6 complete without catching this. Fixed.
- **Item 6 (Part 6 self-check, esp. item 9 power):** PARTIALLY rubber-stamped — the pass added a *cell-level* power floor and declared item 9 met, but the *central pair-level* ranking test (n=|P|) was never power-checked; "≈20 pairs suffice" is contradicted by the arithmetic (finding #2). Also item 5/§3.3 (B0+B-alt present) was checked for *presence* but not for *null-by-construction validity* of B0 (finding #1).
- **Reference records (spot-checked 3+):** the 9 corpus-harvested `selected` records (`ElicitBehaviorsMultiTurn3701`, `CausalRobust6745`, `CondGenBench0511`, …) have `digest_path`/`pdf_path` that **resolve on disk** (verified) and plausible topic-specific `why` strings. The 8 N3-backfilled records (`EssenceBench2607`, `BiasSimBSM2607`, …) resolve only to `../digest.md#N3` with `id_resolves:false` — honestly marked (not "pending"), OpenReview ids spot-confirmed against `topics/corpus/ideas.jsonl` (3/3 hits). Reference integrity: HELD.

**Net:** the Phase A PASS was reliable on digest self-verification, tag discipline, cross-node IDs, and (post-backfill) reference integrity, but **rubber-stamped the two highest-severity defects** (mislabeled placebo, unpowered central test) plus H5's missing effect floor — precisely the items the checklist's own §3.3/§3.5/item-9 language was supposed to catch.

## Overall: NEEDS-REVISION

The idea is genuinely good (a sharp axis-selectivity asymmetry, not a bridge; sound estimand; real method-twin differentiation), and the design is now internally coherent after fixes — but it entered review with two BROKEN-tier defects (no real placebo; an unpowered headline claim) that the self-reported PASS missed. It is salvageable and mostly salvaged in-place; the remaining work is compute-gated and prose re-splice, not redesign.

**Three highest-leverage fixes (all applied):**
1. Add the null-by-construction P0 label-shuffle placebo and relabel B0 as a floor (finding #1).
2. Replace the false "≈20 pairs suffice" with honest pair-level power arithmetic and a `|P|≥60` confirmatory floor / INCONCLUSIVE policy (finding #2).
3. Amend the walking skeleton so P0, the noise-floor re-decode, the ≥3-family collinearity path, and the semantic-diff κ are all exercised before scale-up (finding #3).

## Fixes applied (2026-07-04)
- `paper.md` Mandatory baselines: added P0 null-by-construction shuffle placebo; relabeled B0 as no-signal performance floor.
- `paper.md` A6: replaced "≈20 pairs suffice" with pair-level Fisher-z power arithmetic (0.25@20 … 0.80@85) and a pre-committed EXPLORATORY/INCONCLUSIVE/PASS power policy with `|P|≥60` confirmatory floor.
- `paper.md` H1: added a power gate binding the confirmatory verdict to `|P|≥60`.
- `paper.md` H5: reframed from failure-to-reject to a TOST equivalence test (±0.5 SD) with an effect floor and an INCONCLUSIVE route for the underpowered attrited stratum.
- `paper.md` Step 9 skeleton: added `fmt` as a 3rd family (VIF/partial path), PG-P0 (placebo), PG-noise (re-decode null), PG-2 (mini human-κ); rewrote the pass criterion to require all four.
- `paper.md` F-G1: constrained it to fire only on a P0-clean, adequately-powered substantive null; added an explicit fallback-combination-rules block and a temporal forward-validation robustness check.
- `paper.md` R3 ledger: added the P0 pipeline-artifact/leakage confound line.
- `paper.md` Step 3: added the classical-literature concession (test-suite minimization; concept drift), marked UNVERIFIED.
- `paper.md` Claim-Evidence Map: added row 6b (P0 placebo); relabeled row 6 (B0 floor).
- `digest.md` N3: added an `[UNVERIFIED — requires harvest]` block naming regression-test-selection/test-suite-minimization and concept-drift-detection threads with concede-and-differentiate deltas.
