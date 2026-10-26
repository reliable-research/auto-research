# H1.1 Draft-Package Review — "Catching the Drift Before the Quiz"

Reviewer: Claude (Fable 5), 2026-08-14. Package: `paper_autodiscussion/completed_jobs_dirs/ZH1.1 ...--531488a0/` (research-report.md, experiment-spec.md, paper-draft.md) vs design doc `topics/H1.1_.../discussion.md` (2026-08-13). Context: room closed with **2 unresolved MAJOR critiques**; experiment-spec was **regenerated after a FAILED attempt**. Citation sweep: **narrower than normal** — WebSearch quota exhausted mid-review; all arXiv IDs verified via the arXiv export API; ACM DL citations could not be re-verified (403).

---

## 1. Architecture of the package (~10 lines)

The package proposes a three-stage, gate-serialized program. **Stage A (offline):** from query-stream prefixes of the Shen & Tamkin 52-developer RCT (arXiv:2601.20245), a session-weighted elastic-net logistic "landmark" model R_k produces a calibrated prognostic risk of the session terminating in an erosive delegation pattern, using only cumulative prefix features (solution-request counts, explanation/testing requests, user diagnostic detail, query count/length/timing); nested leave-one-developer-out cross-fitting + 9,999-replicate cluster bootstrap evaluate precision (RQ1) and Brier improvement over prevalence-only baselines at 10/20/30-min checkpoints (RQ2). **Stage B (gate):** model, cutoff c, and τ=0.70 are frozen and hashed; a sealed 32-session gate set is scored once at half-session; the live study opens only if the exact one-sided 95% Clopper–Pearson lower bound on alert precision ≥ 0.70 (RQ3). **Stage C (live, gate-conditional):** three concurrent AI arms — unnotified / placebo-trigger / active comprehension nudge — with the classifier running silently in all arms, pre-notification risk freezing, matched placebo, blinded original-rubric quiz grading, MI(50)+Rubin, MNAR tipping points (RQ4–RQ5); the source-RCT hand-code condition survives only as a **nonconcurrent descriptive anchor**. The experiment-spec renders Stages A–B as a fully implementable pipeline (sealing mechanism, pass-table pre-enumeration, sizing simulator) with the live analysis scaffolded.

## 2. Novelty ledger

| # | Claim | Nearest prior | Delta | Stance |
|---|-------|--------------|-------|--------|
| N1 | First prefix-only, individual-session **prognostic** risk score for skill-eroding AI-interaction patterns | Shen & Tamkin 2601.20245 (hindsight labels on complete sessions); Yao 2606.06253 (retrospective, cohort-level "AI-prompt signature") | Prefix-time, per-session, leakage-controlled prognosis vs. post-hoc description | **SUPPORT** — genuine, provided the ITS/knowledge-tracing lane is cited to preempt "knowledge tracing rediscovered" (currently **not cited** — see §3) |
| N2 | Sealed-set exact-binomial precision gate as *ethical authorization* for the live study | Standard preregistration; JITAI micro-randomized-trial design discipline (Klasnja et al.) | Formalizing go/no-go as a frozen pass-table with an exact bound is careful methodology, not new statistics | **SUPPORT as methodological contribution**; do not oversell |
| N3 | Placebo-controlled one-shot comprehension nudge isolating content from notification reactivity | Buçinca et al. cognitive forcing functions (untargeted, decision-accuracy outcome); JITAI placebo arms | Risk-*triggered*, skill-formation outcome, matched placebo | **SUPPORT** with scoping — but the draft never cites either prior lane |
| N4 | (Implicit) first closed JITAI-style loop whose sensed state is an AI-interaction pattern and whose distal outcome is skill formation | Nahum-Shani et al. 2018 JITAI framework | The domain+sensor transplant is the novelty, per discussion.md's own scoping | **SUPPORT only if JITAI is credited** — the package silently drops the credit discussion.md mandated, re-creating the overclaim its critic explicitly warned against |

## 3. Consistency vs discussion.md — silent scope changes

1. **Related-work collapse (the sibling failure signature).** discussion.md prescribed **five lanes** + a debt ledger. The package's related work contains **three distinct papers** (research-report admits "the four records contain three distinct works because Kosmyna is duplicated"): Shen & Tamkin, Kosmyna, and a silently **added** Becker et al./METR (2507.09089). Silently **dropped**: Yao 2606.06253, Aouad 2605.11350, Cao & Huang (CSCW2 2022), the entire JITAI lane, the Buçinca forcing-function lane, ITS/knowledge tracing, and — worst — the **named C1 foil Agents-That-Teach 2607.06101** (Mehra et al., verified real, July 2026, directly on-topic). Zero confabulated citations, but the 2026 neighborhood is missing exactly as the sibling signature predicts.
2. **Data plan hardened into an unacknowledged dependency.** discussion.md: pursue the base transcripts, **don't depend** — fallback is fresh collection of 40–50 sessions (auto-start date, budgeted). Package: hard-assumes DUA access to all 52 source sessions; no fallback anywhere.
3. **Internal replication dropped.** discussion.md made directional replication of the 50%/67% hand-vs-AI gap a **validity precondition** with a pre-registered interpretation tree; the package demotes hand-code to a nonconcurrent descriptive anchor and never randomizes a hand-code arm. The topic's headline selling point ("directly comparable to the published 50%/67%") silently vanishes while the abstract still leans on the 17-point framing.
4. **Threshold procedure discarded.** discussion.md M6: "the ≥70% number survives only if the base-rate math endorses it" — threshold via decision analysis (annoyance budget ≤0.3 nudges per protective session), gate via CI-vs-majority-baseline. Package: τ=0.70 hard-coded as an **LCB** requirement with no base-rate derivation.
5. **Early detection narrowed to one landmark.** discussion.md wanted k ∈ {1,3,5,10} prefix curves + a **detection-lag distribution**; the package triggers only at the half-session point and drops detection lag entirely — "catching the drift" degraded to "one checkpoint at 50% of allotted time."
6. **IRB/timeline realism: absent.** The package contains no ethics section, no IRB pipeline, no recruitment/attrition arithmetic, no calendar (discussion.md had all four, incl. IRB submission Nov 15 2026 → Feb 2027 approval, 20% over-recruitment, $35–50k envelope, FAccT-2027 data-free position deliverable). For a CHI/CSCW human-subjects submission this is disqualifying as packaged.

## 4. Citation audit (load-bearing)

| Citation | Status (2026-08-14) |
|---|---|
| Shen & Tamkin, *How AI Impacts Skill Formation*, arXiv:2601.20245 | **VERIFIED** (arXiv API; v2, pub. 2026-01-28, first author Judy Hanwen Shen). Numbers used (52 devs, 17 pts, d=0.738, 6 patterns) match digest's full read |
| Kosmyna et al., *Your Brain on ChatGPT*, arXiv:2506.08872 | **VERIFIED** (v2). Still a preprint — must be cited as convergent direction only (draft does this correctly) |
| Becker et al. (METR), *Measuring the Impact of Early-2025 AI...*, arXiv:2507.09089 | **VERIFIED** (v2, 2025-07-12). Accurately described — but silently added vs discussion.md |
| Yao, *When the Scaffold Stays On*, arXiv:2606.06253 | **VERIFIED** (v2, Song Yao, 2026-06-04). **Missing from package** — must restore |
| Aouad, Lykouris & Zhong, *Human-AI Productivity Paradoxes*, arXiv:2605.11350 | **VERIFIED** (v1, 2026-05-12). **Missing** — restore |
| Mehra et al., *Agents That Teach*, arXiv:2607.06101 | **VERIFIED** (v1, 2026-07-07). The C1 foil; subtitle "Designing Incidental Learning Back into AI-Assisted Software Development" confirms open-loop-design framing — foil holds. **Missing** — restore |
| Cao & Huang, gaze/reliance, PACMHCI CSCW2 2022 | **NOT RE-VERIFIED** (ACM DL 403; WebSearch quota exhausted). Keep discussion.md's [VERIFY] flag; cite only with caveat |
| Nahum-Shani et al. 2018 (JITAI framework); Klasnja et al. (MRT/HeartSteps) | From memory / discussion.md; **[VERIFY exact refs before submission]** |
| Buçinca et al. 2021 (cognitive forcing, *To Trust or to Think*) | From memory; **[VERIFY]** |
| Corbett & Anderson 1995 (knowledge tracing) | Canonical; low risk; [VERIFY page details] |

No confabulated citations found. The `[n.d.]` placeholders and the leftover "> This section requires manual completion with proper citations." line in paper-draft.md §Related Work must go.

## 5. Gap to implementation

- **Telemetry harness: buildable.** The spec's schema (queries with timestamps, query_type, diagnostic-detail score), features, sealing mechanism, and synthetic-data generator are concrete and implementable as written; leakage tests and determinism tests are specified. Good.
- **But the offline stage is statistically infeasible as split.** 20 development sessions (~10 erosive) must support nested LODO cross-fitting, cutoff selection, **and** 9,999 pipeline-rerunning bootstrap replicates whose Holm-adjusted lower bounds must clear precision ≥0.70 AND ≥prevalence+0.15 — unreachable at this n except by luck. The gate is worse: CP one-sided 95% LB ≥0.70 requires ≈ a=10,t=10 (LB .741) or a=20,t=18 (LB .717) — i.e., ~90–100% observed precision on 32 sessions. The gate is near-unpassable **by construction**, so the "gate-conditional" live study would de facto never open.
- **Query-type tagging:** spec assumes source annotations or a deterministic rule; discussion.md's LLM-tagger-with-κ≥0.75-audit plan is more realistic and is dropped — restore as the declared plan.
- **Recruitment/IRB:** nothing in the package; discussion.md's numbers (108 recruited for 90; $16–18k pilot; screening traps; Prolific/Upwork) must be reinstated; a 4-arm design needs ~144 recruited for 120.
- **Nudge generation quality:** spec's live intervention module has no quality gate; discussion.md's template-bank-first + fallback + 100% firing audit is dropped — restore.

## 6. Experiment-spec integrity check (regenerated after FAILED attempt)

- **Not truncated**: the spec runs through §Open Decisions/Assumptions item 9 and closes cleanly.
- **Regeneration residue**: lines 1–3 are leftover conversational preamble ("I'll analyze this research plan... Let me think through the structure...") — must be stripped.
- **Internal consistency spec↔report**: good (τ=0.70, 20/32 split, 10/20/30-min checkpoints, B=9,999, sims=10,000, MI=50 all match).
- **The real regeneration scar is in paper-draft.md**: its **Formal Problem Definition still describes the pre-regeneration design** — three arms {H, A, C} with hand-code *randomized*, Δ_CI = μ_C − μ_A, and gate G defined on the **point estimate** π̂ ≥ τ — while Methods/Experiments describe three *AI* arms + nonconcurrent hand-code and an **LCB-based** gate. research-report's problem-definition constraints carry the same fossil ("three arms ... and placebo-nudge control" = four cells in three arms). One paper, two designs.

## 7. Verdict & top-3 fixes

**Verdict: MAJOR REVISION** (strong skeleton — the sealed-gate + placebo-control machinery is genuinely better than most HCI intervention studies — but statistically infeasible as parameterized, internally inconsistent after the regeneration, and stripped of the related-work coverage and IRB/timeline realism the design doc mandated).

**Inferred unresolved MAJOR #1 — offline-stage statistical feasibility.** The 20/32 dev/gate split plus the CP-LB ≥ 0.70 gate makes both RQ1 margins and the RQ3 gate near-unpassable at the available n; the live study would never trigger. (Fix: dual-source data plan restoring the 40–50-session fallback, rebalanced developer-level split with gate ≥20 sessions, and discussion.md's M6 decision-analytic, prevalence-anchored CI gate.)

**Inferred unresolved MAJOR #2 — loss of the concurrent hand-code arm / internal replication.** Without a randomized hand-code arm the design cannot re-test the fragile n=52 base effect, forfeits the "directly comparable to 50%/67%" claim, and the formal problem definition contradicts the experiment design because this change was never propagated. (Fix: 4-arm live study — hand / unnotified-AI / placebo / active — with the pre-registered interpretation tree; rewrite the formal problem definition once, consistently.)

**Top-3 fixes applied in revision:**
1. **Repair feasibility**: dual-source data plan (DUA pursued + pre-registered fresh collection auto-start), ≥40 dev / ≥20 gate developer-disjoint split, M6 decision-analytic gate (one-sided 90% CP LB must exceed erosive prevalence + 0.10, ≥5 alerts, annoyance budget ≤0.3; τ=0.70 demoted to design target), one pre-registered re-gate.
2. **Restore the four-arm live design** with internal replication + interpretation tree; unify the formal problem definition, gate definition, and contrasts across all sections; restore per-query risk with first-crossing trigger (floor k≥3, one nudge/session) and the detection-lag endpoint.
3. **Rebuild related work to five lanes** with the verified 2026 neighbors (Yao, Aouad, Mehra-foil) + JITAI + forcing-functions + ITS lanes and a references section with verification status; add Ethics/IRB + timeline/budget section; strip regeneration residue and [n.d.] placeholders; add the architecture figure.
