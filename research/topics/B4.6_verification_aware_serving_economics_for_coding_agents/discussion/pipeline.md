# Auto-Research-Discussion Run — B4.6 (autoclaude-style, seeded from README.md only)

> Full Stage 1–6 discussion trace lives in `discussion_trace.md`; the standalone Stage 6 protocol is `experiment_design.md`. This file is the phase/gate log per goal.md §2, distinct from the per-stage discussion log. Run date: 2026-08-15.

## Input contract status (goal.md §0)

**Degraded input, by instruction:** only `../README.md` exists (39-line Chinese topic card, [证据] label, sourced from `trend_scan_2026-08.md` §2.5 + §6 occupancy sweep). goal.md's degraded-input rule would construct `digest.md` and `paper.md` first; **this run was explicitly instructed not to fabricate either**, and instead derived the formal problem definition, assumptions, and RQs-with-fallbacks inside the discussion stages at full critic strength. Recorded as a sanctioned deviation, not an oversight. Sibling material (B4.5, B4.2 discussions) was skimmed for family-interface scope discipline only; B4.6's delta from both is stated in the seed brief and enforced by the Stage 1–3 critics (different estimand: serving-stack when/where/granularity at \$/resolved-task, including the cache-interaction term neither sibling models).

## Phase Log

| Phase | Load | Gate result | Date | Pointer |
|---|---|---|---|---|
| Stage 1–6 discussion loop | `auto-research-discussion` (autoclaude/self-play; SKILL.md + autoclaude_mode.md + stages.md + discussion_loop.md + mined_review_checks.md + paper_assembly.md read first) | **PASS** — 6 critic rounds + 6 refiner passes; majors fired in Stages 1 (method_leak + evaluability), 2 (partial_output_coverage), 3 (over-promoted deep tier / engagement honesty), 5 (positivity/identification gap), 6 (under-powered non-inferiority + tier_violation phrasing); Stage 4 fired a structural overlap minor (merge). All resolved in-stage; no cap hit; no backup. Cross-stage consistency check run with a **literal hypothesis↔RQ recount: 7 = 7** (6 mechanism + 1 framing; 0 outcome-tier under `study_type: empirical`). | 2026-08-15 | `discussion_trace.md` |
| Taste audit | `research-taste-auditor` on confirmed Stage 2 + Stage 5 | **PASS — 🟢, no flag fired** (Evidence Gap × Empirical Mapping; diagnostics 0/3/1; verbs bound/attribute/replay/stratify/partition). The two plausible failure readings (two-communities sentence as Bridge; "first-class scheduling unit" as integrate-move) were explicitly tested and rejected — no flag was manufactured, and the one residual generic clause is scored honestly (`boilerplate=1`) with a named re-audit trigger (drift back to beats-baseline framing). | 2026-08-15 | `taste_audit.md` |
| Stage review | `pengsida-stage-reviewer` (archetype classified first: **Analysis/Finding**, secondary resource) | **REVISE ×3 → fixed, then Writing REVISE ×2 → fixed.** Stage 1 (Problem+Motivation) PASS. Stage 2 (Related Work) REVISE: the load-bearing TraceLab limitation rested on corpus-scan hearsay → first-hand confirmation made blocking gate A1 with pre-committed repositioning. Stage 3 (Method/apparatus) REVISE: Tier-A "exact by construction" stated one condition short of true → wall-clock/no-latency-dependence scope condition added. Stage 4 (Experiments) REVISE: latency promised as a denomination but had no reporting slot → descriptive latency readout added to RQ1, headline verdicts scoped to dollars. Stage 5 (Writing, against first assembled draft) REVISE: accomplished-fact abstract sentence hedged to pre-registered form; quotable contribution sentence consolidated into the Introduction's design paragraph. All five fixes folded into `experiment_design.md` / `paper_draft.md` / `.tex`. | 2026-08-15 | `stage_review.md` |
| B/C (walking skeleton / full-scale run) | none — external compute | **SKIPPED (environment)** — no compute in this environment (same environment-driven shortcut recorded for B5.5/B5.4). The draft carries the pre-registered spec only; every RQ subsection ends in an explicit `[placeholder — fill in after experiments are run]`; **no fabricated numbers anywhere** — all quantitative values are design targets with stated rationales (floors, margins, power arithmetic). | 2026-08-15 | `experiment_design.md` gates A1–A4, B0 |
| D (verdict lookup & splice) | none | **SKIPPED (no results)** — no `results/*.json`; `verdicts.json`/`claim_map.md` not produced. Re-open at Phase B once compute exists; nothing in E/F should change except splicing real numbers. | 2026-08-15 | — |
| Reference cache + bibliography (goal.md §1/§8) | `curl` against the arXiv export API | **PASS** — `reference_candidates.jsonl` built with 21 `selected` records (relevance: 1 method-twin, 4 adjacent, 3 baseline-substrate, 13 background/contrast). **15 entries verified via the arXiv export API on 2026-08-15** (ids + titles + authors match); **6 entries are 2026 papers grounded in `trend_scan_2026-08.md`/the topic README** — for these, titles are rendered only as recorded locally, and the 4 whose full titles are not cached carry explicit `title_status` markers (`descriptive-not-cached` / `system-name-only` / `as-recorded-in-scan`) that `gen_refs_bib.py` converts into bibtex notes, so no descriptive title can be mistaken for a verbatim one. **Zero fabricated titles/authors; zero fabricated citations.** `refs.bib` is script-generated (`gen_refs_bib.py`), never hand-typed. | 2026-08-15 | `reference_candidates.jsonl`, `gen_refs_bib.py`, `refs.bib` |
| E/F (prose + LaTeX) | `paper_assembly.md` contract | **PASS** — `paper_draft.md` assembled per the contract: Title/Abstract/Conclusion drafted together; flowing-prose Introduction ending in a 4-item Contributions list; Problem Definition with formal notation ($s, K, \rho_{cons}, \rho_{lib}, C_{p,\Theta}, \Delta(\pi), \iota$); Method Overview + one Methodology subsection per named module (Verification Cost Ledger; Cache-Counterfactual Replay; Per-Class Value Profiler; Two-Tier Headroom Evaluation); Experiments with Setup + one subsection per RQ, each carrying an explicit **Falsification condition** line; thematic Related Work opening with the explicit nearest-neighbor sentence (Cost-Aware Speculative Execution + three-part delta). Internal-ID leak check by grep: clean. `paper_draft.tex` hand-written (no pandoc); `\usepackage[dvipsnames]{xcolor}`; no raw unicode symbols in the body; 21 real `\citep`/`\citet` keys wired (zero-\cite hard gate satisfied). | 2026-08-15 | `paper_draft.md`, `paper_draft.tex` |
| I (compile) | `pdflatex` + `bibtex` | **PASS** — pdflatex → bibtex → pdflatex ×2: exit 0 every pass; **0 "! " errors; 0 undefined citations/references; 0 overfull/underfull boxes** (one 5.9pt overfull found and fixed by rephrasing the class-set notation, mirrored into the .md); `pdftotext -layout paper_draft.pdf - | grep -c "�"` → **0**; **13 pages**. Aux files (`.aux`/`.log`/`.out`) deleted; `.tex`/`.pdf`/`.bbl` kept. | 2026-08-15 | `paper_draft.pdf` |

## Definition-of-done status (goal.md §10) after this pass

All items met **except** those gated on Phase B/C/D compute (no `results/`, `verdicts.json`, or `claim_map.md`; correctly, no claim in the draft has moved past its pre-registered wording — the Abstract/Contributions read as pre-registered tests per the Writing-stage fix). Every citation resolves through a `selected` cache record via a real `\cite`; the taste audit is 🟢 with a named currency trigger; the stage review's five REVISE findings are applied, not pending.

**Open to-dos for a future pass:**
1. Re-open at Phase B: gates A1 (TraceLab first-hand confirmation — this is also the standing novelty re-check), A2 (labeling audit), A3 (simulator calibration), A4 (kill-test), then B0 placebo before any hypothesis.
2. Freshness sweep before any submission: the seed's own risk clock says the speculation/verification-overlap subfield is filling at ~4 papers/quarter; a new method-twin triggers guidance.md situation 6 repositioning, not a silent related-work patch.
3. If compute arrives and the global premise fails (RQ1 liberal bound < 0.10), the pre-committed pivot applies: the paper becomes the certified-small-share negative result at full prominence — wording already fixed in RQ1's falsification condition.

**2026-08-15 — post-run citation-metadata repair (supervisor pass).** arXiv rate
limits blocked live verification during the build; a follow-up batched API query
resolved all 12 previously-unverified IDs. Every ID was real; 5 entries carried
scan-shorthand titles and were updated to the published title/author metadata
(refs.bib + paper_draft.md references list), and the PDF was recompiled clean
(exit 0, zero undefined citations, mojibake check 0).

**2026-08-21 — per-topic review pass (novelty-auditor DEFENSIVE + se-paper-reviewer).**
Output: `review_2026-08.md`. Claim ledger 4 rows: 🟢 on the two estimand claims
(verification-cost interval vs TraceLab 2606.30560/Copilot-scale 2608.00101; cache-content
attribution vs KVFlow/Irminsul), 🟡 on the per-class profiles (vs Dai 2504.07347, theory-only)
and the speculation tier (vs CostAwareSpec 2606.07846 + SpecBox 2607.23933, conceded in draft).
Frequently-missed B1/B2-cluster works (EvilGenie, SpecBench, ImpossibleBench, Hardening,
SWE-Marathon, Who&When Pro, CHIEF) dismissed as non-neighbors with reasons; B4.5/B1.5/B4.1–B4.4
boundaries confirmed distinct. Findings: 2 moderate (F1 live-arm model/decoding/cost-reporting
gap; F2 stale md-mirror + TraceLab-Anonymous metadata), 3 minor. Fixes applied to
paper_draft.md/.tex (Run-provenance-and-study-cost paragraph; External-Validity update +
predictor-transfer sentence; References sync) and refs.bib (TraceLab authors via live batched
arXiv API query 2026-08-21; five provenance notes). Recompiled clean: exit 0, zero "! ",
zero undefined, mojibake 0, 13 pages; aux deleted. Citation debt: none. Hazard noted:
reference_candidates.jsonl is pre-repair — sync before any gen_refs_bib.py regeneration.
Chinese translation `paper_draft.zh.md` + `B4.6_paper_draft_zh.pdf` built this pass.

**2026-08-21 — reference-cache sync (supervisor pass).** Defused the hazard flagged in `review_2026-08.md`: `reference_candidates.jsonl` still carried pre-repair metadata (Anonymous authors / shorthand titles), so any `gen_refs_bib.py` rerun would have clobbered the 2026-08-15 citation repair and the 2026-08-21 TraceLab fix. All 21 records synced to the repaired `refs.bib` metadata (authors stored as lists, per the generator's expected schema); regeneration verified byte-equivalent in content; recompiled clean.
