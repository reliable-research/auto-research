# Auto-Research-Discussion Run — B4.4 (autoclaude-style, repo-driven from digest.md + paper.md)

> Mode: **autoclaude** (self-play, Claude as student+teacher). Source: `../digest.md` (N0–N12) + `../paper.md` (Steps 0–9), both pre-existing reverse-digest artifacts for seed **B4.4**.
>
> Full Stage 1-6 discussion trace moved to `discussion_trace.md`; see `experiment_design.md` for the standalone Stage 6 spec.

---

## Phase Log (goal.md §2 pipeline)

> Everything above this line is the `auto-research-discussion` 6-stage brainstorm log (a
> different, earlier process that produced/validated `paper.md`). This section is the run-state
> log goal.md §0 expects `pipeline.md` to hold — resumability lives here: on restart, read the
> latest row per phase and resume at the first phase whose gate is not `passed`.

| Phase | Date | Gate result | Inputs touched | Notes / pointer |
|---|---|---|---|---|
| Reference cache upgrade (goal.md §1, pre-Phase-A) | 2026-07-04 | passed | `discussion/reference_candidates.jsonl` (rewritten to canonical schema), `discussion/refs_n3_digests/*.md` (new, 10 stub digests) | 150 harvested candidates (110 arXiv + 40 ACL-2023) triaged to canonical schema: 7 selected, 143 rejected. Cache was missing all 10 of digest.md N3's citation keys entirely (harvest never included the paper's own closest prior work) — added as 10 further `selected` records with corpus-grounded stub digests. Final cache: 160 records, 17 selected / 143 rejected / 0 pending. Detail: `discussion/stage_review.md` "Phase A (re-run)" §2. |
| A — Bundle validation | 2026-07-04 | **REVISE-then-PASS** (fixes applied same run) | `paper.md` (5 edits: R1 estimand sentence added to Step 5; A1–A5 `Consequence` clauses added; R3 confound-naming list added; H1 effect floor + non-inferiority margin added to Step 6; power/thin-cell INCONCLUSIVE subsection added to Step 6), `discussion/reference_candidates.jsonl`, `discussion/stage_review.md` | Checklist items 2 (reference-cache integrity), 5 (H*/A* machinery), 6 (method-rigor audit, incl. Part 2 A2 evidence standard) fired REVISE; all fixed directly in `paper.md`/the cache per goal.md's instruction to fix static-document REVISE findings immediately. Items 1, 3, 4, 7, 8 PASS. No STOP. Full findings: `discussion/stage_review.md` § "Phase A (re-run)". |
| B — Walking skeleton | — | not started | — | Blocked on real experiment compute, which does not exist in this environment; out of scope for this run per task instructions. Bundle is otherwise clear to proceed whenever compute is available. |
| C — Full-scale execution | — | not started | — | Downstream of B; no compute in this environment. |
| D — Verdict lookup & splice | — | **skipped (no results to look up)** | — | Requires `results/*.json` from Phase C, which does not exist. Per this run's explicit scope (A validate → B/C skip → D skip → E prose → F LaTeX → G review → H taste → I compile), Phase E below elevates the pre-registered spec itself (splicing Phase A's `paper.md` fixes into the pre-existing draft), not verdict-selected result sentences — no `verdicts.json`/`claim_map.md` exist, and none of Phases E–I below assert a result as fact anywhere (checked explicitly in Phase G item 4). |

**Note on phase ordering vs. existing artifacts:** `discussion/paper_draft.md`/`.tex`/`.pdf` already
existed in this folder at the start of this run (timestamped 14:08–14:14, i.e. *before* the same-day
Phase A re-run above, which ran ~19:19–19:27 and made 5 edits to `paper.md`). The draft therefore
predated Phase A's fixes (missing estimand sentence, H1 effect floor, thin-cell INCONCLUSIVE rules)
and had zero `\cite`/`refs.bib` infrastructure. This run treated the pre-existing draft as **stale
pending those fixes**, per the same convention documented in `topics/B5.4_.../discussion/pipeline.md`,
and folded the fixes in below rather than re-deciding any claim.

| Reference-cache follow-up (goal.md §3 item 2, pre-Phase-E) | 2026-07-04 | **resolved (2 of 3 upgraded to real digests; 1 honest gap)** | `discussion/reference_candidates.jsonl`, `openview_corpus/paper_cache/pdf/arxiv_{2510.19669,2207.05221}.pdf`, `openview_corpus/paper_cache/pdf_digests_main/arxiv_{2510.19669,2207.05221}.md` | `DiffAdapt644F` (method-twin): real arXiv mirror found (2510.19669, ICLR 2026); full N0–N12 digest built from the actual 28pp PDF. `Kadavath2207` (baseline): real PDF fetched (43pp); genuine partial-read (pp.1–10) N0–N12 digest built, NOT_FOUND used honestly for unread sections rather than fabricating. `AdaptiveThink2i6` (method-twin): genuine search exhausted (no arXiv mirror exists; OpenReview PDF fetch blocked by bot-check challenge in this environment) — corpus-motivation-only stub retained, gap logged honestly in `stage_review.md` rather than fabricated. Detail: `discussion/stage_review.md` § "Reference-cache follow-up — 2026-07-04". |
| Freshness sweep (goal.md §1, pre-Phase-E) | 2026-07-04 | **passed (no new method-twin)** | — | 2 targeted searches on the paper's own manipulated-variable angle (frozen-probe-vs-self-report-vs-training-free under one matched dollar budget); no genuine same-estimand match found. No repositioning triggered. |
| E — Prose elevation (re-check/fold-in) | 2026-07-04 | **PASS (folded into F)** | `discussion/paper_draft.md`, `discussion/paper_draft.tex` | Spliced Phase A's `paper.md` fixes into the pre-existing draft: added Estimand sentence to Problem Definition; added ≥1pp effect floor + ±1pp non-inferiority margin to RQ2; added thin-cell INCONCLUSIVE pre-declarations to RQ2–RQ4 (30 discordant pairs / n=200 routed-expensive-tier queries); added a new Related Work paragraph citing 7 previously-selected-but-uncited `background`/`adjacent` cache entries; fixed one localization artifact (an untranslated bilingual seed-quote fragment) in the English-language draft only. Applied identically to `.md` and `.tex`. |
| F — LaTeX production (bibliography wiring) | 2026-07-04 | **REVISE — fixed** | `discussion/paper_draft.tex`, `discussion/refs.bib` (new) | **[major] found and fixed in this pass:** `paper_draft.tex` had zero `\cite` commands and no `refs.bib` — a goal.md hard-gate violation. Fix: `refs.bib` script-generated (`gen_refs_bib_b44.py`, scratchpad) from all 17 `selected` cache records; `\usepackage{natbib}` + `\bibliographystyle{plainnat}` + `\bibliography{refs}` added; all 17 `selected` keys wired into real `\citep{}` citations (19 instances) in Introduction/Related Work — no `selected` entry left uncited. Recompiled to confirm resolution (see Phase I row). |
| G — Adversarial review | 2026-07-04 | **REVISE-then-PASS** (`se-paper-reviewer`) | `discussion/stage_review.md` | Reviewed (results-dependent checks scoped out, no compute): (1) RQ↔`paper.md` hypothesis fidelity — PASS after the Phase E splice; (2) citation wiring — PASS, 17/17 selected keys cited, Kadavath's role correctly stated as an adopted protocol not a beat-a-number baseline; (3) notation consistency — PASS; (4) overclaim check on Abstract/Introduction/Conclusion — PASS, one `[minor]` noted (a contribution bullet reads marginally more assertive than surrounding hedged prose; not blocking). The one `[major]` (bibliography wiring, Phase F row above) was fixed in this same pass. Full findings: `discussion/stage_review.md` § "Phase G — adversarial review". |
| H — Taste re-audit | 2026-07-04 | **PASS** (`research-taste-auditor`) | `discussion/taste_audit.md` (new dated section appended, prior entry kept) | Re-audit of the final Abstract + five Methodology subsections post Phase F/G edits: verdict 🟢 unchanged, no condition fires, no regression from the estimand/effect-floor/citation splices. Diagnostics: surface_stitching=0, bottleneck_specificity=3 (sharper than the pre-draft audit), boilerplate=1. |
| I — Compile | 2026-07-04 | **PASS** | `discussion/paper_draft.tex` → `.pdf` | `latexmk -C` then `latexmk -pdf -interaction=nonstopmode -halt-on-error`, exit 0, zero errors, zero undefined-citation warnings, 14 pages (up from 13 pre-bibliography-wiring), `.bbl` has 17 `\bibitem`s matching the 17 `selected` cache records. |
| Review-revision pass | 2026-07-05 | **PASS** (1 open finding applied, 2 rejected as moot/not-requested, 8 verified already-applied) | `discussion/paper_draft.md`, `discussion/paper_draft.tex` → `.pdf` (recompiled, exit 0, zero undefined citations), `discussion/discussion_trace.md` (appended round) | Applied the sole OPEN finding — Phase G's `[minor]` on the fourth contribution bullet — by hedging it to direction-neutral deliverable-format wording; all other review findings verified already applied; cross-deliverable check (6 RQs, ≥1pp floor, −1pp/±2pp margins, thin-cell rules, n=2,000) found no mismatch. Detail: `discussion_trace.md` § "Post-review revision round (2026-07-05)". |

**Definition-of-done status (goal.md §10):** all items met for the phases this run's scope covers
(A, E, F, G, H, I) — `paper_draft.pdf` compiles clean, every citation resolves to a `selected` cache
record via real `\cite`/`refs.bib`, `se-paper-reviewer` and the final taste audit are clean. **Not yet
met, and out of scope for this environment:** "every instrument passed R2 before scale" and "every
claim carries a final status in `claim_map.md`" — both require Phase B/C real compute, which does not
exist here. Re-open this pipeline at Phase B (walking skeleton) once compute is available; at that
point Phase D's verdict lookup will need to re-splice actual result sentences into the Abstract/
Results placeholders currently marked `[placeholder — fill in after experiments are run]`.

---

## Review pass — 2026-08-21 (`review_2026-08.md`)

Per-topic review pass (novelty-auditor DEFENSIVE, t_audit=2026-08-15 + se-paper-reviewer
feasibility/staleness lens). **Findings: 0 [major], 3 [moderate], 5 [minor]** — detail in
`review_2026-08.md`. The three [moderate] fixes applied to `paper_draft.md` + `.tex`:
(1) concede-and-claim vs newly-found neighbors Radharapu et al. arXiv:2512.22245 (probes vs
verbalized confidence vs multi-generation, calibration+cost+transfer) and Yuan et al.
arXiv:2605.09502 (probe 0.95 AUROC vs uninformative verbalized confidence) — abstract sentence
softened, Related Work paragraph extended, RQ6 expected-direction conceded as pre-evidenced;
(2) both citations added to `refs.bib` after verification against the live arXiv API (one
batched id_list request); (3) RQ2's non-inferiority margin widened −1pp → −2pp (aligned with
RQ3's TOST margin) after power arithmetic showed the paired 95% CI half-width at n=2,000 is
≈1.2–2.0pp, making a −1pp margin structurally unresolvable. Supervisor-listed reward-hacking/
attribution candidates (EvilGenie, SpecBench, ImpossibleBench, Hardening-Agent-Benchmarks,
SWE-Marathon, Who&When-Pro, CHIEF) all dismissed as non-neighbors; B4.x cluster estimand check
clean (one [minor] framing-overlap note vs B4.2's verifier-cost accounting move). Recompiled
clean: exit 0, zero errors, zero undefined citations, 19 bibitems; aux files removed. Chinese
translation `paper_draft.zh.md` + `B4.4_paper_draft_zh.pdf` produced from the post-revision draft.
