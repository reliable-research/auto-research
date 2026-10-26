# Auto-Research-Discussion Run — T5.5 (autoclaude-style, repo-driven from digest.md + paper.md)

> Mode: **autoclaude** (self-play, Claude as student+teacher). Source: `../digest.md` (N0–N12) + `../paper.md` (Steps 0–9), both pre-existing reverse-digest artifacts for seed **T5.5**. Round cap: 5/stage (none hit). All six stages converged in 1 critic round + 1 refiner pass each — the seed material was unusually mature (paper.md already carries Step 0 asymmetry, Step 2 archetype, Step 3 taste self-audit, Step 5 formal definitions, Step 6 pre-registered experiments with fallbacks, and a Claim–Evidence Map), so genuine disagreement surfaced but didn't require re-proposing from scratch.
>
> **Full pipeline order (updated):** this file (`auto-research-discussion`, 6 stages) → `taste_audit.md` (`research-taste-auditor`, idea-level check on Stage 2+5) → `stage_review.md` (`pengsida-stage-reviewer`, PASS/REVISE/STOP per stage against the confirmed outputs, plus a Stage 5 Writing check on the first assembled draft) → final `paper_draft.md`/`.tex`/`.pdf`. Three REVISE findings from `stage_review.md` (a related-work coverage gap on architecture-conformance-checking tooling, an ill-conditioned mechanism-share metric in the Method, and a missing contamination/leakage check in Experiments) are already folded into the `paper_draft.*` files below — read `stage_review.md` for the reasoning behind those three fixes. A nearest-neighbor sentence and per-RQ falsification conditions were built into the stage outputs and the assembled draft from the start (not left for `stage_review.md` to catch), so `stage_review.md` was deliberately pushed to find different, genuine issues rather than re-reporting those two.

> Full Stage 1-6 discussion trace moved to `discussion_trace.md`; see `experiment_design.md` for the standalone Stage 6 spec.

---

## goal.md phase log

> Everything above this line is the `auto-research-discussion` skill's own internal
> six-stage record (a construction aid, not a goal.md phase). The entries below are the
> goal.md §2 pipeline's phase log proper, per §0's resumability contract ("on start, read
> `discussion/pipeline.md`; resume at the first phase whose gate is not `passed`").

| Phase | Date | Gate result | Notes / pointer |
|---|---|---|---|
| A (bundle validation) | 2026-07-04 | **PASS (post-fix)** | Full checklist run + findings/fixes in `discussion/stage_review.md` § "Phase A (re-run)". Two companion fixes applied to `paper.md` (estimand sentence added to Step 5; H2 effect floor + new H2c/shape-discordant criterion + fallback F2c; A1–A7 assumption ledger given explicit `PG-*` gate ids and `*Consequence:*` clauses, incl. an INCONCLUSIVE rule on A6; A1's R2 instrument-validation detection clause completed to all 5 steps). `discussion/reference_candidates.jsonl` rewritten from the ad hoc 150-row harvest schema to goal.md §1's canonical schema: all 150 harvested rows given a `selected`/`rejected` verdict (10 selected, 140 rejected, no `pending` left), plus 10 new records added for digest N3's citation keys that were entirely absent from the harvested cache (a REVISE-level integrity gap, now fixed) — 160 total records, 20 `selected`. |
| B (walking skeleton) | — | **not started** | Blocked on real experiment compute, which this environment does not have. Per this run's explicit scope, execution stops at the Phase A gate; do not treat the pre-existing `paper_draft.md`/`.tex`/`.pdf` in this directory as Phase E–I outputs produced from real B/C/D results — they were assembled by the `auto-research-discussion` construction pass above (pre-registered/hypothetical framing throughout, no fabricated numbers) and remain gated behind a real Phase B/C/D run before any of their claims can be treated as verified. |
| Review-revision pass | 2026-07-05 | **all findings closed** (6 verified already applied, 3 open items applied, 0 rejected) | `paper_draft.md`, `paper_draft.tex`, `paper_draft.pdf` (recompiled, 14 pp), `experiment_design.md`, `../digest.md`, `discussion_trace.md` | Propagated paper.md's H2 slope-ratio effect floor + A6 INCONCLUSIVE rule into both deliverables, added the taste-audit §6 primary-framing sentence, and added the digest N5/N6/N7/N12 `Status:` lines — see `discussion_trace.md` § "Post-review revision round (2026-07-05)". |

**Resume point:** Phase B, whenever real compute becomes available — start from `paper.md`'s Step 9 Walking Skeleton exactly as written (now including the PG-1..PG-6 gate ids added in the Phase A fix).

---

## Per-topic review pass — 2026-08-21

Novelty audit (defensive, t_audit=2026-08-15) + se-paper-reviewer feasibility pass: see
`review_2026-08.md`. Verdict 🟢 (estimand distinct; carried by the shape-of-frontier estimand and
the dual-criterion/shape-discordant apparatus). Four [moderate] findings fixed and mirrored into
`paper_draft.md`/`paper_draft.tex` (recompiled, exit 0): (1) Related-Work staleness — the code-specific
constraint-benchmark wave (IFEvalCode 2507.22462, MultiCodeIF 2507.00699, CIFE 2512.17387, RACE
2407.11470) does score correctness+compliance jointly, so the blanket no-oracle claim was split into
two waves with a concede-and-claim delta; (2) Intro "remains unmeasured" conceded against
SUSTAINSCORE (2601.22047, interference existence) and re-scoped to the price's schedule/shape;
(3) κ-audit arithmetic — per-rule ≥20 flagged-instance quota replaces the single 100-sample pool;
(4) sweep resolution + budget arithmetic pre-registered (≥7 ladder levels, ≥4×3 grid, ~5×10³ pilot /
~10⁵ scale-up generations as design targets). Neighbor adds in Related Work: SWE-Effi (2509.09853),
arXiv:2512.04273. All seven frequently-missed works (EvilGenie, SpecBench, ImpossibleBench,
Hardening-Agent-Benchmarks, SWE-Marathon, Who&When-Pro, CHIEF) dismissed as non-neighbors with
reasons. All new arXiv ids verified live (batched id_list, 2026-08-21). Citation debt (supervisor
verify): pre-arXiv architecture-conformance classics (reflexion models, DSM, ArchUnit/import-linter
literature) — the draft's existing `[citation needed]` marker stands. Chinese version:
`paper_draft.zh.md` → `T5.5_paper_draft_zh.pdf`.
