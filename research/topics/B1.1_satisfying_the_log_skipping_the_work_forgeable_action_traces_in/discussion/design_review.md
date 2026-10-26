# Design Review (adversarial, 2026-07-04)

Reviewer stance: skeptical PC member. Phase A "PASS" in `stage_review.md` was **not** trusted; every item relied on below was re-verified against actual file contents.

## Verdict summary

| Dimension | Score | One-line reason |
|---|---|---|
| 1. Feasibility & scale | SOUND (one FIXABLE) | Pilot is concrete (SWE-bench-Verified tasks + FuncBenchGen-style tool tasks), compute estimated ($1–3k pilot, 200–400 H100h RL); but the RL arm is a **code change, not config**, and the skeleton never exercises it. |
| 2. Soundness | FIXABLE | Estimand OK; B-alt strong & budget-matched; **but B0/arm C is NOT null-by-construction** — it is a base-rate control expected to be non-null, so Phase D's placebo-first gate is inoperable. H2/H3 have significance-only effect floors. |
| 3. Novelty & pre-emption | FIXABLE | Asymmetry is genuine, taste-clean, non-bridge. But three recent cache entries (esp. `ClinicalFHIR2607` "silent-finish") already document the log/state gap and are filed merely "adjacent"; the "never measured" claim needs qualifying. |
| 4. Hypothesis→fallback robustness | FIXABLE | F1/F2/F3 + F-G1 cover the substantive failure space, but **instrument failure (κ<0.7 or oracle false-positives) is read as a substantive null** — a real effect that is unlabelable falls through to the bounded-null fallback. |
| 5. Method scope & RQ design | SOUND (one FIXABLE) | Validity envelope stated; A2 mandatory shapes mostly present; but no RQ tests the paper's own recommendation (does adding a state-check actually reduce FIR?), and mechanism layer (R6) is thin (a qualitative taxonomy). |

**Overall: NEEDS-REVISION.** Prior Phase A PASS is **partially reliable** — reference-cache work is honest and mostly holds, but two checklist items (5, 6) were rubber-stamped on exactly the points below.

---

## Findings (ranked most-severe first)

### [BROKEN→FIXABLE] F1. B0 is not a null-by-construction placebo; Phase D's placebo gate cannot function
`paper.md` maps B0 onto **arm C (no-pressure zero-shot)**:
> "B0 — 'why do this at all' control (arm C, no-pressure zero-shot agent). Measures the base Verifier Gap `LVR−SVR` and base FIR with *no* optimization pressure."

guidance §3.3 requires B0 to do **two** jobs: (a) the current-practice arm, **and (b) a null-by-construction placebo (shuffle labels/years/assignments) whose effect *must* be null** — "Non-null placebo = the pipeline measures an artifact = the whole run is invalid." Arm C only does job (a). Its FIR is **expected to be non-null** — the design itself assumes a ~5% honest-error base rate ("power analysis assumed 5% base rate," A3). So Phase D step 1 ("Placebo first. B0 non-null → run invalid") would flag *every* run invalid, or (worse) be silently ignored. The gate is inoperable as written.

The genuine null-by-construction placebo is missing: a **non-separable / non-forgeable negative-control task set** where `V_log=1` *requires* `V_state=1`, so FIR must be structurally 0 regardless of pressure. If FIR>0 there, the state oracle is emitting false positives (mislabeling legitimate alternative solutions as forging) — which is **exactly threat t1**, currently only covered by an M2 construction check, not by a scored placebo arm. Note A1 ("every admitted task is forgeable") deliberately *excludes* such tasks, so the placebo has been designed out.

**Fix:** Add a negative-control arm of non-separable tasks (or state-label-shuffled episodes) as the true B0 placebo; pre-register that its FIR must be ≤ the oracle false-positive tolerance, and route non-null to Situation 1. Relabel arm C as the base-rate/floor control it actually is. This is the single highest-leverage fix.

### [FIXABLE] F2. H2 and H3 have significance-only effect floors, not magnitude floors
guidance §3.1: "Effect floor is mandatory: significance without magnitude passes nothing (a slope can be significant and practically zero)." H1 complies (`FIR(A)−FIR(B) ≥ 0.10`). H2 does not:
> "a positive Cochran–Armitage trend (`p<0.05`) AND the mixed-logistic pressure coefficient β>0 with 95% CI excluding 0, AND the RL dose-response slope ≥ the selection slope"

β>0 with CI excluding 0 is a *significance* criterion — the exact failure mode the rule warns against. H3 likewise: "FIR−FIR(B) 95% CI lower bound > 0" is sign-only. Neither names a minimum slope/gap magnitude in native units.
**Fix:** give H2 a minimum log-odds-per-pressure-level floor and H3 a minimum FIR−FIR(B) gap (e.g. ≥ the same 0.10). This directly contradicts `stage_review.md` item 5's claim that "H1/H2/H3 already filled all 7 slots."

### [FIXABLE] F3. Instrument failure is indistinguishable from a substantive null in H1
H1's attribution guard: "the annotator-confirmed forging fraction among flagged arm-A episodes exceeds that of arm B (**κ ≥ 0.7 required for annotation to count**)." If M6 annotation fails validation (κ<0.7), the annotation "doesn't count," the AND-clause cannot be satisfied, **H1 fails, and its fallback fires** — declaring a *bounded-null* ("log-forging is not an automatic consequence…"). But that outcome is compatible with a large *real* effect that merely could not be labeled. guidance Situation 7 says κ-failure is a "do not scale / refine or simplify" branch, **not** a substantive null. The paper's A2 consequence covers oracle failure (degrade to upper bound) but there is no H1-level branch for annotation failure.
**Fix:** pre-commit a distinct branch: κ<0.7 → INCONCLUSIVE on attribution, report raw FIR gap as unattributed, never as the bounded-null finding.

### [FIXABLE] F4. RL scale-up is code, not config; the skeleton never exercises it
Step 9's skeleton runs **arm A best-of-16 selection + arm C only** ("arm B/state-reward deferred to first scale step"), deterministic metrics, no RM, no RL. It then claims: "Scaling to the full grid (add models, the 3 M3 verifiers, arm B, RL, 150–300 tasks…) is then a **config-list change, not a code change**." Adding a **GRPO RL training loop** is not a config change over a best-of-n sampling loop — it is a new training harness (goal.md §8 / guidance Situation 8 config-not-code gate). Yet H2 depends on "RL slope ≥ selection slope," so the paper's most expensive, highest-risk component is entirely untested by the pass criterion. The digest honestly flags RL as "the single biggest feasibility risk" and pre-commits the core claim to the selection regime — good — but the skeleton should still smoke-test the RL path, or the RL conjunct of H2 must be pre-declared INCONCLUSIVE-if-unrun.
**Fix:** add a 1-task, 1-seed RL smoke run to the skeleton so the training path is exercised before scale; otherwise demote all RL-slope claims.

### [FIXABLE] F5. Recent near-twins document the log/state gap; "never measured" needs qualifying
The cache's own `selected` `adjacent` entries partly pre-empt the novelty framing:
- `ClinicalFHIR2607` (arXiv:2607.01470): "reports a 'silent-finish' ceiling where a large share of episodes end without the agent producing the required FHIR order, i.e. a documented gap between what the harness scores and what the agent actually did." That is a demonstrated log-pass/state-fail phenomenon in a real benchmark.
- `EvoPolicyGym2607`: "final return… can hide blind retries, overfitting to visible feedback, brittle special cases, missing verification."
- `AuditedSkillGraph2512`: "verifiable rewards can shift behavior toward what is easiest to verify rather than what is desired."

None runs the separability-certified, matched-arm, pressure-dose-response measurement this paper proposes, so the idea is **not** pre-empted (Situation 12 does not fire). But the differentiation is real only if stated: the delta is *optimization-pressure sweep + separability certificate + forging-vs-honest-error attribution*, not "first observation of the gap." Related work currently ranks only SWE-RM/ToolRM as nearest neighbor (per stage_review Stage 2); the 2607 "silent-finish" line is closer to the *phenomenon* and must be confronted as such.
**Fix:** promote `ClinicalFHIR2607`/`EvoPolicyGym2607` to a concede-and-differentiate paragraph; soften "has not been directly measured" to "has not been measured under controlled optimization pressure with separability certification and attribution."

### [NOTE] F6. Estimand is one sentence but a ~100-word run-on
R1 wants "one sentence — quantity, unit, population, decision." The estimand sentence contains all four but is a multi-clause, semicolon-laden paragraph masquerading as a sentence. Technically compliant, readability-marginal. Tighten for the draft.

### [NOTE] F7. `paper_draft.md`/`.tex`/`.pdf` are stale relative to `paper.md`
Draft artifacts are timestamped 13:29; `paper.md` was edited at 19:12 to add the Phase A fixes (estimand sentence, A1–A6 gate fields, M1/M6 R2 plan, inconclusive-cell rule). The draft predates all four. Noted once — not penalized further; regenerate before Phase E.

---

## Failure-space simulation (per-H walk-through)

- **H1 fails cleanly (no A−B gap):** F1 fires → bounded-null "log-forging is not an automatic consequence of log-only reward at this scale." Publishable *if* the field assumed the effect (it does — proxy-hacking prior). **Covered**, but see F3: a *false* null can arise from oracle/annotation failure, and F1 would fire indistinguishably. **Uncovered outcome.**
- **H2 fails (no dose-response):** F2 fires → "threshold-like or pressure-insensitive… cheap best-of-n is a sufficient audit probe." Coherent. **Covered.**
- **H3 fails (a log-verifier reaches state floor):** F3 fires → "characterize which log-side design suffices." Coherent, and Claim 5 (CO4 "state check necessary") correctly narrows since it is conditional on H1∧H3. **Covered.**
- **H1 ∧ H2 both fail:** global pivot F-G1 → refutation/bounded-null archetype with pre-written abstract. **Covered.**
- **H1 pass, H2 fail, H3 fail:** forging exists but not graded, log-side hardening suffices → Claim 1 partial, Claim 3/5 fall to their fallbacks. Paper survives with a narrowed "forging occurs but a strong log-side verifier closes it" story. **Covered.**
- **Wrong direction, FIR(A) < FIR(B):** physically implausible (arm B rewards state, giving no incentive to forge; FIR(B) is pure honest-error), so not a live risk — but the pre-registration never says what happens if it occurs. Minor **gap**; add a one-line "wrong-direction ⇒ diagnose oracle" clause per Situation 4.
- **Instrument failure (κ<0.7, or oracle false-positive rate high):** **UNCOVERED** — currently collapses into F1's bounded-null. This is the one failure outcome that can leave the paper asserting the wrong finding. Fix per F3 + F1.

---

## Missing RQs / reviewer questions the design cannot currently answer

1. **Does the recommended fix work?** CO4/Claim 5 asserts "state checks are a necessary complement," but no RQ measures whether *adding a partial/cheap state-check to the reward* actually reduces FIR. A reviewer will demand a mitigation arm; without it the take-home is an assertion.
2. **Does learned forging generalize / persist?** No held-out-task or post-training evaluation — is forging a memorized per-task trick or a transferable policy? A2 reviewers ask this.
3. **What is the oracle's own false-positive rate?** t1 is mitigated by construction checks, but no *quantified* FPR is reported as a headline guard (this is the same hole as the missing placebo, F1).
4. **Frontier/proprietary models** — acknowledged out of scope (t3); acceptable, but the envelope claim leans entirely on 7–14B open models.
5. **Mechanism (R6):** the only "why" analysis is a qualitative forging-strategy taxonomy (RQ_INF_2). A2 wants ≥1 genuine mechanism analysis; consider a quantitative account of *which task property* (log-cost vs state-cost ratio) predicts FIR, which N9 already hypothesizes but no RQ formally tests.

---

## Reliability audit of prior Phase A PASS

**Re-verified checklist items (the ones most likely rubber-stamped):**

- **Item 4 (claim–evidence orphans): HOLDS.** All 5 claims trace (Claims 1/3/5 → H1/H2, H3, H1∧H3; Claim 2 → Step-5 defs + A1/A2/A6; Claim 4 → spec disclaimer). No orphans either direction. The recorded PASS is supported.
- **Item 5 (seven-slot completeness for every H* and A*): PARTIALLY RUBBER-STAMPED.** `stage_review.md` states "H1/H2/H3 already filled all 7 slots — no gap there." False for the **effect_floor** slot: H2's floor is β>0 (significance) and H3's is a CI-lower-bound>0 (sign) — neither is a magnitude floor, which guidance §3.1 makes mandatory (F2). Separately, item 5 asserts "B0 + B-alt + F-G1 present per §3.3," but B0 satisfies only half of §3.3's mandate — it is not a null-by-construction placebo (F1). The A1–A6 gate fields were genuinely added this session and do hold.
- **Item 6 (Part 6 self-check): MOSTLY HOLDS, one gap.** The estimand sentence (Part 6 #1), M1/M6 R2 plans with thresholds (#6), and the inconclusive-cell rule (#9) were really added and are present. But Part 6 #5 ("B0 + B-alt + F-G* all present with pre-committed wording") was checked as PASS without noticing B0 is not null-by-construction — same rubber-stamp as item 5.

**Reference-record spot checks (cross-topic contamination + resolvability):**
- `SWE-RM` (method-twin): `digest_path` and `pdf_path` both resolve on disk (`arxiv_miner_cache/…/2512.21919.{md,pdf}` present). `why` is on-topic (execution-free reward model, same proxy-vs-outcome estimand). **Clean.**
- `ClinicalFHIR2607`, `AuditedSkillGraph2512`, `EvoPolicyGym2607`, `Theoria2607` (adjacent): all four `digest_path`/`pdf_path` resolve on disk; `why` fields are topic-specific (verifier/harness-vs-world gaps). **No cross-topic contamination.**
- `ToolRM`/`CorrelatedProxies`/`FuncBenchGen` (load-bearing N3 keys): `digest_path` resolves (`refs_digests/*.md` present), but **`pdf_path: null` and `verified.id_resolves: false`** — digests were built from the local OpenReview *proposal record*, not the actual PDF. This is disclosed honestly in `stage_review.md`, but a load-bearing method-twin resting on a proposal-record digest is a real (if honest) evidentiary weakness for Phase E related-work.
- `SWE-bench` (background): both paths null — honestly reported residual; background-only, not load-bearing. Acceptable per goal.md §3 item 2.

**Net:** the reference-cache rebuild was done in good faith and is largely verifiable; the two REVISE→fixed items are real fixes. The PASS is unreliable specifically on the *design-substance* checks (items 5/6's effect-floor and placebo sub-clauses), which the weaker author's self-review waved through.

---

## Overall: NEEDS-REVISION

The core idea is genuinely sharp (provenance asymmetry, taste-clean 🟢, not pre-empted), the archetype is correctly A2, feasibility is realistic, and the fallback scaffolding is unusually mature. It is not unsalvageable — but three design flaws must be fixed before any compute is spent, because each can silently corrupt the verdict.

**Three highest-leverage fixes:**
1. **Add a true null-by-construction placebo** (non-separable/negative-control tasks whose FIR must be ~0), separate from arm C, so Phase D's placebo-first gate is operable and threat t1 gets a scored guard (F1).
2. **Give H2 and H3 magnitude effect floors** in native units, not significance/sign criteria (F2).
3. **Pre-commit a κ-failure / oracle-false-positive branch that reports INCONCLUSIVE-on-attribution**, so an unlabelable real effect cannot masquerade as the bounded-null finding (F3).

---

## Fixes applied (2026-07-04)

Applied directly to `paper.md` after user authorization (same-day review-then-fix session; `digest.md` left untouched — it is the upstream planning artifact, to be re-synced at its next revision).

1. **F1 fix (B0 placebo):** `paper.md` § Mandatory baselines — B0 redefined as **arm P**, a non-separable negative-control task set with non-separability certificates, pre-registered criterion observed FIR(P)=0 (Wilson CI upper ≤ 0.05) at max pressure, non-null ⇒ run invalid (Situation 1), checked as **PG-0**; the former "B0" relabeled **Base-rate control (arm C)**, explicitly expected-non-null and non-invalidating.
2. **F1 wiring (A1/A2):** A1 amended to "every admitted *scored* task is forgeable" with the arm-P exception stated; A2's Detection now names the arm-P placebo (PG-0) as the *scored* guard for threat t1 (oracle false positives).
3. **F2 fix (H2 floor):** H2 gains a native-unit effect floor — model-implied FIR rise from ρ=1 to ρ=64 ≥ 0.05 (5 pp); a significant-but-flat slope now fails H2.
4. **F2 fix (H3 floor):** H3 tightened from CI-lower-bound>0 (sign-only) to FIR−FIR(arm B) ≥ 0.10 point estimate (same 10-pp floor as H1) with CI lower bound > 0.
5. **F3 fix (κ-failure branch):** verbatim **Instrument-failure branch** added under H1 — M6 κ<0.7 (after one pre-registered refinement round, Situation 7) ⇒ H1 = INCONCLUSIVE-on-attribution, fallback F1 does NOT fire, run routes to instrument refinement; PG-0/PG-2 oracle failure ⇒ annotator-confirmed-subset upper bound or INCONCLUSIVE, never a substantive null. Cross-referenced from the Inconclusive-cell rule.
6. **F4 fix (RL config-not-code):** Step 9 gains an **RL-path smoke run** bullet (1-task × 1-seed × few-step GRPO emitting the same dual-label record) folded into the skeleton pass criterion; if unexercised, H2's RL conjuncts are pre-declared INCONCLUSIVE. Skeleton arms/task set/criterion updated to include 2 arm-P placebo tasks and the FIR=0 PG-0 check.
7. **F5 fix (novelty qualification):** Step 3 gains a **Pre-emption / positioning check** bullet conceding ClinicalFHIR2607 ("silent-finish"), EvoPolicyGym2607, and AuditedSkillGraph2512 as nearest phenomenon-level observations, restating the novelty claim as "never measured under controlled pressure with separability certification and attribution"; the Bridge-check bullet's "unmeasured failure" phrasing qualified accordingly.

**Not fixed here (needs human or compute):** regeneration of stale `paper_draft.md`/`.tex`/`.pdf` (F7 — Phase E artifact, must be rebuilt from the updated `paper.md`); the missing mitigation-arm RQ ("does adding a state check reduce FIR?") and a quantitative mechanism RQ (task-property → FIR) are design *additions* beyond the authorized surgical fixes, needing an owner budget decision; ToolRM/CorrelatedProxies/FuncBenchGen digests still rest on OpenReview proposal records and SWE-bench's digest_path is still unresolved (both need network/PDF access).
