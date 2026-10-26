# Pipeline State — B6.5

## Phase Log (goal.md pipeline)

| Phase | Gate result | Date | Notes / pointer |
|---|---|---|---|
| A — Bundle validation | **PASS** (after fixes) | 2026-07-04 | Reference cache (`discussion/reference_candidates.jsonl`) rewritten to goal.md §1's canonical schema and re-triaged (150 harvested candidates → 3 selected + 147 rejected; 7 N3-grounded records backfilled as `selected`, total 10 selected / 147 rejected). Phase A checklist re-run against `README.md`/`digest.md`/`paper.md` per goal.md §3; 4 of 8 checklist items fired REVISE and were fixed directly in `digest.md` (N12 `absence_comment`) and `paper.md` (assumption-ledger `Gate:`/`Consequence:` slots, Step 5 `Estimand` line, Step 6 confound-naming + power/INCONCLUSIVE statement, RQ1 `Aggregation` line). Full item-by-item findings and fixes: `discussion/stage_review.md`, heading "## Phase A (re-run)". |
| B/C — Walking skeleton / full-scale run | **SKIPPED (out of scope)** | 2026-07-04 | No real experiment compute exists in this environment; `paper_draft.md`/`.tex`/`.pdf` already existed from an earlier run as a pre-registered spec (Results sections carry only `[placeholder]` markers, no fabricated numbers). |
| D — Verdict lookup & splice | **SKIPPED (no results to splice)** | 2026-07-04 | No `results/` exist; `claim_map.md`/`verdicts.json` not created. All RQ "Result" fields remain explicit placeholders per goal.md §5's own precondition (never scored without `run_valid`). |
| Reference-cache integrity re-check + freshness sweep (goal.md §1/§3 item 2) | **PASS, real gap found and fixed** | 2026-07-04 | No `selected` load-bearing (`baseline`/`method-twin`) record had `digest_path: null` (all 4 already resolved from the prior Phase A backfill), so the mandatory-real-PDF-digest rule did not fire. Two targeted freshness-sweep searches on the core manipulated-variable angle found no new method-twin (guidance.md situation-6 repositioning does not apply). **Real gap found:** 3 of 10 `selected` cache records (`MultiAgentMechDesign2025`, `GumbelWatermarkSampleComplexity2026`, `ATINTER2023`) were never cited anywhere in `paper_draft.md`/`.tex` — fixed in the Phase E/F entry below. Full detail: `discussion/stage_review.md`, headings "Freshness sweep" and "Reference-cache integrity re-check". |
| E/F — Prose + LaTeX re-entry (bibliography wiring) | **REVISE → fixed** | 2026-07-04 | **[major]:** `paper_draft.tex` had zero `\cite`/`\citep` commands and no `refs.bib` — a goal.md hard-gate violation (refs.bib must be script-generated from the jsonl's `selected` records). Fixed: added `RAID2024`/`HC3_2023` dataset records to the jsonl (both arXiv ids live-verified); generated `discussion/refs.bib` (12 entries) via a script reading the jsonl's `selected` records; added `natbib` + `\bibliographystyle{plainnat}`/`\bibliography{refs}`; rewired all 5 Related Work paragraphs + the Experimental Setup Datasets paragraph with real `\citep{}` keys, adding the 3 previously-uncited works as new concede-and-differentiate/context sentences; added an explicit **Threats to Validity** section (5 categories, reusing `digest.md` N10's taxonomy + mitigations verbatim) before the Conclusion. Mirrored into `paper_draft.md`. Full detail: `discussion/stage_review.md`. |
| G — Adversarial review (`se-paper-reviewer`) | **PASS (after fixes)** | 2026-07-04 | Scope: `paper_draft.tex` + `paper.md` + reference cache; all results-dependent checks N/A (no `B_pilot/`/`results/`). The `[major]` (bibliography wiring) and one `[moderate]` (missing Threats to Validity section) both fixed directly, folded into the E/F entry above. One `[minor]` logged, not fixed (a slightly imprecise RQ2→RQ3 cross-reference label; cosmetic, no claim affected). Full detail: `discussion/stage_review.md`, heading "## Phase G". |
| H — Taste re-audit | **PASS — 🟢 reconfirmed, no drift** | 2026-07-04 | Re-ran against the final Abstract + Method Overview (unchanged text); confirmed the Phase E/F/G edits (bibliography wiring, new Related Work sentences, new Threats section) did not touch the audited framing and none of the three verdict conditions fire. Appended (not overwritten) to `discussion/taste_audit.md`. |
| I — Compile | **PASS — 0 errors** | 2026-07-04 | `latexmk -pdf -interaction=nonstopmode -halt-on-error paper_draft.tex` → exit 0, 15 pages, 0 `\cite` undefined warnings, 0 LaTeX errors (only cosmetic `Overfull \hbox` typesetting warnings, pre-existing from before this pass). `discussion/paper_draft.pdf` regenerated. |
| Review-revision pass | **PASS** | 2026-07-05 | Files touched: `paper_draft.md`, `paper_draft.tex`, `paper_draft.pdf` (recompiled, exit 0, 15 pages, 0 errors/undefined citations), `discussion_trace.md` (appended "Post-review revision round (2026-07-05)"). Applied the one open finding — Phase G `[minor]` #1, RQ2 Metrics line's imprecise RQ3 cross-reference, clarified in `.md`+`.tex` — all other review findings verified already applied; `[minor]` #2 and the OpenReview-id to-do rejected as moot/environment-blocked; cross-deliverable consistency (7 RQs, effect floors, margins) verified clean. |

**Resumability note:** Phases A and E–I are now gated `PASS` for this pass (B/C/D remain
out-of-scope in this environment, as designed — this is a spec-stage deliverable, not a results
report). Next real work requires either (a) real experiment compute to run Phase B/C, or (b)
revisiting Phase A/E if `paper.md`/`digest.md`/the reference cache change again (goal.md §0
resumability rule). **Open to-dos for a future pass:** (1) the 7 OpenReview-sourced `selected`
cache records (`MonitorAIScale`, `DetectGPT`, `AdaptiveWMAttack`, `MarkovCalib`, `DUCI`,
`AnchorPeerReview`, `UCB-S`) remain `verified.id_resolves=false` — no PDF cached locally, and a live
resolution attempt on one of them (`bX3J7ho18S`) was inconclusive (404 on `api.openreview.net`,
bot-challenge-gated on the public forum page) rather than a clean confirm/deny; (2) ~~the RQ2→RQ3
cross-reference label noted as `[minor]` in Phase G~~ — **resolved 2026-07-05** in the
Review-revision pass (see that Phase Log row and `discussion_trace.md`'s "Post-review revision
round (2026-07-05)").

---

## Per-topic review pass (2026-08-21)

Skills: `novelty-auditor` (defensive, t_audit=2026-08-15) + `se-paper-reviewer` (feasibility/staleness).
Full report: `discussion/review_2026-08.md`. Findings: 1 [major] (F1: cost construct has no external
anchor — matches `portfolio_2026-08.md`'s Tier-4 retirement rationale; conceded in-draft rather than
overturned), 3 [moderate] (F2: missing compute-budget arithmetic for the $B_{\min}$ search; F3:
citation staleness — MonitorAIScale/DetectGPT were "Anonymous/n.d." OpenReview stubs despite published
identities, and the paraphrase-attack literature 2023–26 was uncited; N1: quantification-learning
field never conceded despite the three estimator designs instantiating its standard families),
2 [minor] (not revised — no manufactured fixes). Novelty verdict: 🟢 on the estimand row
(budget-scaling exponent vs corpus size), nearest neighbors named (Liang et al. 2024 benign-only;
adaptive watermark-attack line per-text-only); B6.1 boundary confirmed (strategic evasion vs
distributional generalization); 7 frequently-missed 2025–26 agent-benchmark works API-verified and
dismissed as non-neighbors. Revisions applied to `paper_draft.md` + `.tex`: construct-threat and
Conclusion concessions (simulated cost economy), compute-amortization paragraph (paraphrase ladder +
bisection monotonicity), Related Work extended (paraphrase-attack line; new Quantification-learning
concede-and-claim paragraph). References: `reference_candidates.jsonl` +7 new `selected` records
(all arXiv-ids live-verified in one batched API request), MonitorAIScale/DetectGPT upgraded to
verified published identities; `refs.bib` regenerated via new `discussion/gen_refs_bib.py`
(19 entries); recompiled pdflatex→bibtex→pdflatex×2, exit 0, 16 pages, 0 errors/undefined citations;
aux files removed. Chinese version: `paper_draft.zh.md` + `B6.5_paper_draft_zh.pdf` built.
Citation debt (supervisor verify): Forman 2008 (DMKD) and González et al. 2017 (CSUR) — canonical
QL citations without arXiv ids, not added under the arXiv-only verification rule; the 5 remaining
OpenReview-sourced records (AdaptiveWMAttack, MarkovCalib, DUCI, AnchorPeerReview, UCB-S) stay
`id_resolves=false` (OpenReview still bot-gated from this environment).

---

> Full Stage 1-6 discussion trace moved to `discussion_trace.md`; see `experiment_design.md` for the standalone Stage 6 spec.

**2026-08-21 — citation-debt partial resolution (supervisor pass).** AdaptiveWMAttack confirmed as arXiv 2410.02440 (exact title match "Optimizing Adaptive Attacks against Watermarks for Language Models", Diaa/Aremu/Lukas) via live API; jsonl record upgraded (`id_resolves=true`, arXiv id + authors added), `refs.bib` regenerated, recompiled clean. Remaining debt unchanged: Forman 2008 / González 2017 (non-arXiv canonical QL refs) and 4 OpenReview bot-gated records (MarkovCalib, DUCI, AnchorPeerReview, UCB-S).
