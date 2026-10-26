# Auto-Research-Discussion Run — T3.2 (autoclaude-style, repo-driven from digest.md + paper.md)

> Mode: **autoclaude** (self-play, Claude as student+teacher). Source: `../digest.md` (N0–N12) + `../paper.md` (Steps 0–9), both pre-existing reverse-digest artifacts for seed **T3.2**. Round cap: 5/stage (none hit). All six stages converged in 1 critic round + 1 refiner pass each — the seed material was unusually mature (paper.md already ran its own asymmetry/taste self-audit at Step 0/3 and a full pre-registration through Step 9), so genuine disagreement surfaced quickly but didn't require re-proposing from scratch.
>
> **Full pipeline order (updated):** this file (`auto-research-discussion`, 6 stages) → `taste_audit.md` (`research-taste-auditor`, idea-level check on Stage 2+5) → `stage_review.md` (`pengsida-stage-reviewer`, PASS/REVISE/STOP per stage against the confirmed outputs, plus a Stage 5 Writing check on the first assembled draft) → final `paper_draft.md`/`.tex`/`.pdf`. One REVISE finding from `stage_review.md` (a missing nearest-neighbor sentence in Related Work) and one REVISE finding on the Experiments section (the reactivity-calibration RQ's gating role was buried inside its own subsection rather than stated up front) are already folded into the `paper_draft.*` files below — read `stage_review.md` for the reasoning behind those two fixes.

> Full Stage 1-6 discussion trace moved to `discussion_trace.md`; see `experiment_design.md` for the standalone Stage 6 spec.

---

## Phase Log (goal.md §2 pipeline)

> This section tracks the `goal.md` A→I phase pipeline itself (distinct from the `auto-research-discussion` 6-stage log, now in `discussion_trace.md`, which produced `paper_draft.*`). Per `goal.md`'s resumability rule: on resume, read this log and start at the first phase whose gate is not `passed`.

| Phase | Gate result | Date | Inputs (this run) | Notes |
|---|---|---|---|---|
| A | **passed** (after 3 REVISE-fixes) | 2026-07-04 | `README.md`, `digest.md`, `paper.md`, `reference_candidates.jsonl` (upgraded to canonical schema this same pass) | Full checklist run + fixes recorded in `discussion/stage_review.md` under "## Phase A (re-run)". Reference cache upgraded from the flat 150-item harvest schema to `goal.md` §1's canonical schema (`key`/`ids`/`venue`/`year`/`url`/`relevance`/`verdict`/`why`/`verified`) in the same pass: 5 of the original 150 harvested candidates selected (all `relevance: adjacent`), 145 rejected with paper-specific reasons; 10 additional cache records added for `digest.md` N3's already-cited works (closing the "every N3 key is a selected cache record" integrity gap those 150 didn't cover) — 160 total records, 15 selected. Three REVISE findings fixed directly in `paper.md`: (1) added an explicit R1 estimand sentence to Step 5; (2) restructured the Assumptions table (A1–A8) into five explicit guidance.md §3.2 slots incl. named `PG-*` gates and consequences, plus a full 5-step R2 instrument-validation subsection for the M3 verifier; (3) added a pre-declared per-cell thin-cell/INCONCLUSIVE rule to Step 6. No STOP condition fired. |
| B–I | not started | — | — | No real experiment compute exists in this environment; per this run's scope, execution stops at the Phase A gate. Resume at Phase B (walking skeleton) once compute is available — re-hash `paper.md`/`digest.md` inputs first per the resumability rule, since Phase A made edits to `paper.md` this pass. |
| Review-revision pass | 2026-07-05 | passed | `paper_draft.tex`, `paper_draft.pdf`, `discussion_trace.md`, `pipeline.md` | Folded review findings: 7 verified already applied, 3 rejected as advisory, 1 fixed (B-alt baseline mirrored from `paper_draft.md`/`experiment_design.md` into `.tex`, PDF recompiled clean); RQ counts, hypotheses, effect floors, and margins verified consistent across deliverables. |

---

## Per-topic review pass — 2026-08-21

`review_2026-08.md` written (novelty-auditor DEFENSIVE t_audit=2026-08-15 + se-paper-reviewer):
claim ledger 5 rows (verdict 🟢, carried by the identifiability formulation and the type-gap
decomposition estimand; no twin found), findings F1 [major] + F2/F3 [moderate] + F4–F7 [minor].
Revisions applied to `paper_draft.md` + `paper_draft.tex`: F1 premise re-hedged
(abstract/intro/conclusion — the "8×" figure downgraded to an unverified, replication-first
premise; source listed as citation debt), F2 concede-and-claim for Prompt Design at Scale
(arXiv:2607.19257, verified live 2026-08-21; record appended to `reference_candidates.jsonl`,
now 161 records / 16 selected), F3 RQ6 power arithmetic + group-sequential escalation rule.
The pass was interrupted after the md/tex edits; completed on resume the same day: PDF
recompiled (pdflatex ×2, exit 0, no errors, no bibtex — prose-named references), aux/log/out
cleaned, `paper_draft.zh.md` + `T3.2_paper_draft_zh.pdf` regenerated from the post-revision
draft. Citation debt (supervisor verify): the unnamed "原论文" behind the ~8× figure — see
`review_2026-08.md` §6.
