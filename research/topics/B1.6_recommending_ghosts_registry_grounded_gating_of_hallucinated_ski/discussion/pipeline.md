# Auto-Research-Discussion Run — B1.6 (autoclaude self-play, seed = README.md + digest.md)

> Topic: **B1.6 — Recommending Ghosts: Registry-Grounded Gating of Hallucinated Skill/Tool
> Calls in Live Agent Trajectories.** Full Stage 1–6 discussion trace lives in
> `discussion_trace.md`; this file holds the phase/gate log (goal.md pipeline state).
> There was **no pre-registered `paper.md`** for this topic — the formal problem definition,
> assumptions, and RQ-with-fallback machinery were derived during the stages (see
> `discussion_trace.md`), so the critic rounds were run at full strength per the task brief.

## Inputs

| File | Role | Status at start |
|---|---|---|
| `../README.md` | topic card (CN frontmatter + asymmetry statement + minimal experiment) | present |
| `../digest.md` | N0–N12 reverse-digest, 857 lines; base paper (arXiv:2607.12340) read in full (Freshness note 2026-08-13); N3 grounded in `topics/corpus/ideas.jsonl` | present |
| `../paper.md` | pre-registered spec | **absent** (derived in-stage, not fabricated) |
| `discussion/reference_candidates.jsonl` | reference cache | **absent** (topic's N3 was built against `topics/corpus/ideas.jsonl` directly; see Reference-grounding note below) |

## Phase Log

| Phase | Load | Gate result | Date | Pointer |
|---|---|---|---|---|
| Stage 1–6 discussion loop | `auto-research-discussion` (autoclaude self-play) | **PASS** — 6 stages, each 1 genuine critic round + 1 refiner pass; genuine `[major]` in Stages 1/2/3/5/6, `[minor]` in Stage 4; no stage closed over an open major; round cap (5) never hit | 2026-08-15 | `discussion_trace.md` |
| Cross-stage consistency check | (inlined in the loop) | **PASS** — 7 hypotheses = 7 mechanism-tier RQs (explicit recount); reference integrity, ID stability, output coverage, `study_type=empirical` → 0 outcome-tier RQs all verified | 2026-08-15 | `discussion_trace.md` § "Cross-stage consistency check" |
| Taste audit (Stage 2 Motivation + Stage 5 Method) | `research-taste-auditor` | **🟢 PASS** — Failure-Risk/Empirical-Mapping, not Bridge/Synthesis; diagnostics 0/3/1; verbs relocate/replace/decouple/measure (human-heavy); no flag manufactured | 2026-08-15 | `taste_audit.md` |
| Stage review (archetype = Analysis/Finding) | `pengsida-stage-reviewer` | **PASS with 3 REVISE applied** — S1 Problem+Motivation PASS; S2 Related Work REVISE→fixed (nearest-neighbor sentence); S3 Method REVISE→fixed (human-review verdict undefined on both axes); S4 Experiments REVISE→fixed (per-RQ falsification lines + replication gate surfaced); S5 Writing PASS | 2026-08-15 | `stage_review.md` |
| Assembly (paper_assembly.md) | (inlined) | **PASS** — Title/Abstract/Conclusion together; flowing-prose Intro → Contributions; formal Problem Definition; Method Overview + one subsection per module; Experiments Setup + one subsection per RQ with explicit Falsification condition; thematic Related Work with nearest-neighbor sentence; no internal stage IDs in prose | 2026-08-15 | `paper_draft.md` |
| References (refs.bib + \cite wiring) | (inlined) | **PASS** — 9 citations, all grounded: 8 OpenReview corpus works (`paper_id`s re-verified in `topics/corpus/ideas.jsonl`) + the fully-read method-twin arXiv:2607.12340; real `\citep`/`\citet` keys wired into Intro, Method, Setup, Related Work; zero `\cite` would be a goal.md §8 hard-gate violation — not the case here | 2026-08-15 | `refs.bib`, `paper_draft.tex` |
| LaTeX compile | `pdflatex` ×2 (+ bibtex) | **PASS** — exit 0, zero `! ` errors, `pdftotext ... | grep -c "�"` = 0; `.aux/.log/.out/.blg` removed, `.tex`+`.pdf`(+`.bbl`) kept | 2026-08-15 | `paper_draft.pdf` |

## Reference-grounding note (goal.md §1 / §3 item 2)

This topic's digest **N3 was built against `topics/corpus/ideas.jsonl`** (the 11,683-record
OpenReview corpus) plus one fully-read non-corpus arXiv method-twin — there is no separate
`discussion/reference_candidates.jsonl` harvest, so citations are grounded directly against
those two sources rather than a jsonl cache:

- **8 OpenReview corpus works** — `paper_id`s `dHng2O0Jjr` (ToolLLM), `yVQcr4qjD6` (Robust
  Function-Calling via Function Masking), `l05DseqvuD` (AgenTracer), `2H03gm4Rq6`
  (Self-Evolving Agent Benchmarks), `hSyW5go0v8` (Self-RAG), `d94x0gWTUX` (Tool-Augmented
  Reward Modeling), `Ur00BNk1v2` (GenArtist), `KznJt9Fhjc` (ToolACE-MT) — all eight verified
  present in `topics/corpus/ideas.jsonl` with matching real titles (spot-checked 8/8 by
  `paper_id` grep + JSON parse); `refs.bib` uses the corpus `paper_title` and `paper_url`
  verbatim.
- **1 method-twin** — arXiv:2607.12340, "Skills That Don't Exist: A Large-Scale Study of
  Hallucinated Skill Recommendation in LLM Agents" (Yuan et al.). This is the topic's seed
  baseline, grounded fleet-wide in the repo (`../README.md`, `../../trend_scan_2026-08.md`,
  digest N3/N4 Freshness note "full text read 2026-08-13", and the `positions/C2_provenance_
  not_existence/` folder). **Verification caveat:** the live `export.arxiv.org` API in this
  sandbox returned no entry for the ID, and WebSearch quota was exhausted, so the ID could not
  be independently re-confirmed here; it is cited under the repo's established mined-corpus
  convention (the same convention under which sibling topic B5.5 cites its 2026-dated
  corpus arXiv IDs), because it is the topic's declared, digest-grounded method-twin and the
  paper cannot be positioned without it. **No additional external anchors were invented** —
  fewer real citations beat any confabulated one (goal.md §8).

## Definition-of-done status (goal.md §10)

All deliverables produced: `pipeline.md`, `discussion_trace.md`, `taste_audit.md`,
`stage_review.md`, `paper_draft.md`, `refs.bib`, `paper_draft.tex`, `paper_draft.pdf`.
Every RQ subsection ends in an explicit `[placeholder — fill in after experiments are run]`
Result — **no fabricated numbers**; all quantities in the draft are pre-registered design
targets with stated rationale (sample size, effect floors, α/correction). The abstract and
contributions assert only pre-registered *tests*, never accomplished results — consistent with
`study_type: empirical` and the fact that no experiment has been run in this environment.

## Post-draft audit + revision (2026-08-15, later same day)

`novelty-auditor` (defensive) + `se-paper-reviewer` pass recorded in `review_2026-08.md`.
Key updates: (1) the earlier verification caveat is **resolved** — the live arXiv API now
returns arXiv:2607.12340 (Yuan et al., published 2026-07-14, cs.SE/cs.CR); every number the
draft attributes to it matches the real abstract. (2) Two [major] findings fired and were
fixed in `paper_draft.md`/`.tex`/`refs.bib` (recompiled clean): uncited design-level mechanism
twins (ETDI arXiv:2506.01333; Zero-Trust Tool Registry arXiv:2504.19951) → concede-and-claim
added to Intro contribution 1 + a new Related Work thread; missing package-hallucination /
slopsquatting lineage (Spracklen arXiv:2406.10279 et seq., six works) → cited in Intro +
Related Work. (3) Two [moderate] fixes: RQ4 re-registered as a separately-sized TOST
equivalence cell (2-pt margin ≈ 3,000 episodes/arm at a ~90% base rate — design arithmetic,
not data); RQ7's standalone-arm install semantics pinned (scripted out-of-loop installer).
(4) Two [minor]: RQ3 marked as an instrument-integrity check; this note. All eight new
citations verified via the arXiv API on 2026-08-15. Overall novelty stance: 🟢 on the
measurement/instrument rows, 🟡 on the mechanism row (now conceded); decay risk high — run
the pilot soon. Chinese mirror `paper_draft.zh.md` + `B1.6_paper_draft_zh.pdf` produced from
the post-revision draft.

**Environment-gated (not deliverable defects):** Phases B/C/D (walking skeleton / full-scale
run / verdict lookup) require compute that does not exist in this environment, so
`results/*.json`, `verdicts.json`, and `claim_map.md` are not produced and no claim has moved
past its pre-registered wording. Re-open at Phase B once compute is available; nothing in the
assembled draft should change except splicing in real numbers per goal.md §6.
