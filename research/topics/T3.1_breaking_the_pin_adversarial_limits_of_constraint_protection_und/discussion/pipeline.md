# Auto-Research-Discussion Run — T3.1 (autoclaude-style, repo-driven from digest.md + paper.md)

> Full Stage 1-6 discussion trace moved to `discussion_trace.md`; see `experiment_design.md` for the standalone Stage 6 spec.

---

## Phase Log (goal.md §2 pipeline state)

> This section tracks goal.md's own phase gates (A → B → C → D → E → F → G →
> H → I), distinct from the `auto-research-discussion` stage log above. Added
> in the 2026-07-04 session that upgraded `reference_candidates.jsonl` to the
> canonical schema and re-ran the Phase A checklist.

| Phase | Date | Gate result | Notes | Pointer |
|---|---|---|---|---|
| A | 2026-07-04 | **PASS** (2 REVISE items found and fixed in this run; 0 STOP) | Task 1: `reference_candidates.jsonl` upgraded from ad hoc harvest schema to goal.md §1 canonical schema; all 150 candidates individually digested and adjudicated — **12 selected / 138 rejected, 0 pending**. Task 2: full goal.md §3 checklist re-run. REVISE #1 — digest.md N3's ten related-work keys don't resolve against the cache (grounded via a different, general OpenReview corpus); fixed with provenance caveats in `digest.md` N3 and `paper.md` Step 5, cross-linking the 12 newly-verified cache entries; residual risk noted for `paper_draft.md`/`.tex`'s existing citations of the same 10 keys (out of this session's fix scope). REVISE #2 — oracle (M3) instrument validation plan incomplete and under-thresholded (κ≥0.6 vs guidance.md §3.4 R2's required κ≥0.7, missing R2 steps ①②④); fixed directly in `paper.md` Step 5 / assumption A1 / global gate G0. Also fixed: `digest.md` N12 missing `Status` line (tag-discipline, goal.md §3 items 1/3). | `discussion/stage_review.md` → "## Phase A (re-run)" |
| Review-revision pass | 2026-07-05 | **PASS** (1 OPEN finding applied, 1 .md/.tex desync fixed; 1 rejected-as-moot) | `paper_draft.md`, `paper_draft.tex`, `paper_draft.pdf`, `discussion_trace.md`, `pipeline.md` | Folded Phase-A item-2 residual risk (added citation-provenance caveat to draft Related Work in `.md`+`.tex`) and synced `.tex` RQ3 to κ≥0.7 with full R2 setup; recompiled PDF (13pp); cross-deliverable RQ counts/effect floors verified consistent. |
| B–I | — | not started | No real experiment compute exists in this environment; per this session's explicit scope, Phase B/C/D/E/F/G/H/I were not attempted. `discussion/paper_draft.md/.tex/.pdf` already exist on disk from a prior session's run of Phases E–I, but their Phase-A-relative validity is now contingent on resolving the reference-cache-integrity residual risk logged above before they are next touched. | — |

## 2026-08-21 — Per-topic review pass (resumed after interruption)

- **Review**: `review_2026-08.md` (drafted 2026-08-15, t_audit=2026-08-15; novelty-auditor DEFENSIVE + se-paper-reviewer) found complete: claim ledger C1–C5, verdict *somewhat-novel / novel-at-margin* (nearest neighbor **Governance Decay 2606.22528**, uncited — F1 [major]), findings F1 [major], F2–F4 [moderate], F5–F6 [minor], T3.2/T3.3/T3.4 estimand boundaries confirmed distinct. The interrupted session had written the review but **not** applied any revision.
- **Revisions applied** (this session) to `paper_draft.md` + mirrored in `paper_draft.tex`: F1 — Governance Decay named and conceded in Abstract, Intro ¶2–¶3, Contributions, Related Work (new lead paragraph), Conclusion; F2 — oracle claim narrowed to the before/after-compaction persistence gate (IH-Benchmark 2607.25987 conceded); F3 — cost claim narrowed to the attacker/defender ratio at the break boundary (GD defender cost + Security–Fidelity 2606.30783 conceded); F4 — "Attack-arm scope" added to Experimental Setup + third Conclusion limitation (gradient arm open-weight-only). [minor] F5/F6 logged, not revised beyond the caveat rewrite F1 required.
- **Citation debt discharged**: arXiv API recovered; one batched `id_list` request verified all 5 records (exact title matches); appended as `selected` to `reference_candidates.jsonl` (150→155), `verified.checked=2026-08-21`. Provenance caveat in the draft narrowed to the 8 still-provisional mechanism names.
- **Recompile**: pdflatex ×2, exit 0, zero errors/undefined refs (draft has no formal bibliography — prose name + arXiv-id citations); `paper_draft.pdf` 14 pp; .aux/.log/.out removed.
- **Chinese version**: `paper_draft.zh.md` translated from the post-revision draft; `T3.1_paper_draft_zh.pdf` built via md2pdf.
- Phase B–I status unchanged (no experiments run; draft remains a pre-registered specification).

**Resume point:** per goal.md's resumability rule, the next session should
resume by resolving the item-2 residual risk (either re-harvest targeting the
ten unresolved OpenReview IDs, or rewrite `paper_draft.md`/`.tex`'s Related
Work from the 12 cache-verified entries) before treating Phase E/F/G/H/I as
still valid, since goal.md §8's `stale_claim_after_verdict` / citation-only-
via-`selected`-keys hard gates were not clean at the time those phases were
last run.
