# goal.md — drive an idea bundle to paper_draft.tex / paper_draft.pdf

**This file is an executable runbook.** It says *what runs when*, with exact
file contracts and binary gates. **How to construct anything well — idea
classification, archetype-specific method design, hypothesis/assumption/
fallback engineering, rigor recipes, and what to do when things go sideways —
lives in `guidance.md`, which sits next to this file and is authoritative for
every construction step.** State lives on disk in `discussion/` so a run can
stop at any gate and resume without re-doing prior phases.

---

## 0. Input contract

One topic = one folder (reference example: `B4.1_the_regret_of_stopping...`):

```
<topic_dir>/
  README.md      # topic card: YAML frontmatter (code, title_cn, label,
                 # parent_topic, source) + 核心问题 (core question)
                 # + 最小实验 (minimal experiment)
  digest.md      # reverse-digest: paper-digest's N0–N12 schema run FORWARD
                 # from the seed. Tags: [GIVEN]/[HYPOTHESIS]/
                 # [GROUNDED:corpus]/[PLACEHOLDER]. N3 grounded against real
                 # reference records. Ends with Claims + self-verification.
  paper.md       # pre-registered spec: taste audit, archetype (guidance.md
                 # Part 2), formal problem definition (estimand + notation +
                 # term→definition→measurement table), assumptions ledger
                 # (A* per guidance.md §3.2), pre-registered experiments
                 # (E*/H* per §3.1), control arms (B0/B-alt per §3.3),
                 # fallbacks (F*, global pivot F-G*), walking skeleton,
                 # Claim–Evidence Map, Abstract v0.
  discussion/    # THE WORKING DIRECTORY:
    reference_candidates.jsonl   # local reference cache — §1
    pipeline.md                  # run state + phase log
    stage_review.md              # Phase A/G reviewer outputs
    taste_audit.md               # taste audits (initial + final)
    paper_draft.md               # Phase E prose
    paper_draft.tex              # Phase F output
    paper_draft.pdf              # Phase I output
    B_pilot/  results/  verdicts.json  claim_map.md   # created when needed
```

**Degraded inputs** — construct the missing artifact before Phase A, never
improvise past the gap:
- Only `README.md` → classify the idea shape (guidance.md Part 1), then
  build `digest.md` with `paper-digest` in reverse-digest mode (§9); build
  `reference_candidates.jsonl` first if absent (§1); N9 stays
  `[PLACEHOLDER]`.
- `README.md` + `digest.md` → build `paper.md` **per guidance.md Parts 2–3
  end-to-end** (archetype first, then hypothesis/assumption/fallback
  machinery, then the Part 6 self-check), with `research-taste-auditor` run
  on the motivation+method pair first (→ `taste_audit.md`).
- Raw clue only → `auto-research-discussion` brainstorm mode to produce a
  README-shaped topic card, then the two steps above.

**Resumability:** on start, read `discussion/pipeline.md`; resume at the
first phase whose gate is not `passed`. Never re-run a passed phase unless
its inputs changed (record input-file hashes per phase in `pipeline.md`).

---

## 1. `reference_candidates.jsonl` — the local reference cache

Local-first related-work substrate: recent published + arXiv papers
harvested once, cached, digested. One JSON object per line; minimum fields
(tolerate extras, backfill on first touch):

```json
{"key": "TasteGap2607",
 "title": "...",
 "ids": {"arxiv": "2607.01233", "openreview": null, "doi": null},
 "venue": "arXiv", "year": 2026,
 "url": "https://arxiv.org/abs/2607.01233",
 "pdf_path": "refs/2607.01233.pdf",
 "digest_path": "refs/2607.01233.digest.md",
 "relevance": "baseline|method-twin|adjacent|contrast|background",
 "verdict": "selected|rejected|pending",
 "why": "one sentence: why in/out",
 "verified": {"id_resolves": true, "checked": "2026-07-04"}}
```

**Lifecycle:** ① **Harvest** from ≥4–5 query angles derived from the core
question (arXiv / OpenReview / Semantic Scholar; Scholar Gateway when
available); append as `pending`; cache PDFs where licensing permits.
② **Digest** every potentially load-bearing candidate
(`baseline`/`method-twin`/`contrast`) with `paper-digest` in **extraction**
mode → `digest_path`; its N1 + own stated limitations ground the topic
digest's N3/N4. `background` entries (incl. the 2–3 per-archetype
structural exemplars required by guidance.md Part 5) may get lighter
digests. ③ **Select** — set `verdict` + `why`; rejections stay in the file.
④ **Consume** — N3 cites only `selected` keys; Phase E prose and Phase F
`refs.bib` are generated from this file (scripted), never hand-typed.

**Staleness:** before Phase E, one freshness sweep (hits newer than the
latest `verified.checked`, same angles). A new `method-twin` → guidance.md
Part 4 situation 6: `paper.md` repositioning + Phase A re-check, never a
silent prose patch.

---

## 2. Pipeline

```
[A validate bundle] → [B walking skeleton] → [C full-scale execution*]
      → [D verdict lookup & splice] → [E prose] → [F LaTeX]
      → [G adversarial review] ⇄ (revise E/F) → [H taste re-audit] → [I compile]
                    * C is the one phase no skill performs — real compute
```

| # | Phase | Load | Reads | Writes | Gate (binary) |
|---|---|---|---|---|---|
| A | Bundle validation | `pengsida-stage-reviewer`, `research-taste-auditor` | 3 input files + `reference_candidates.jsonl` | `stage_review.md` (§A), `taste_audit.md` | §3 checklist all-clear |
| B | Walking skeleton | none (execute `paper.md`'s skeleton literally) | `paper.md` | `B_pilot/` | skeleton's own pass criterion + all PG-* gates |
| C | Full-scale run | none — external compute | `B_pilot/` config, scaled | `results/*.json` | one results file per RQ + per control arm |
| D | Verdict lookup & splice | none (procedure inlined, §5) | `results/`, `paper.md` | `verdicts.json`, `claim_map.md` | every RQ has a verdict; B0 checked first |
| E | Prose elevation | `pengsida-paper-writer` | `claim_map.md`, splice choices, digest N2/N4/N6/N10, cache (+ per-paper digests) | `paper_draft.md` | reverse outline per section matches thesis; no claim outside `claim_map.md`; every citation ∈ `selected` |
| F | LaTeX production | `research-paper-writing` | `paper_draft.md`, `paper.md` notation, cache | `paper_draft.tex` + `refs.bib` + figures | notation matches spec; captions carry a conclusion; refs.bib scripted |
| G | Adversarial review | `se-paper-reviewer` | `paper_draft.tex`, `B_pilot/` + `results/`, cache | `stage_review.md` (§G) | no unresolved `[major]`; listed mitigations actually ran; no `selected` twin/baseline uncited |
| H | Taste re-audit | `research-taste-auditor` | final abstract + method | `taste_audit.md` (final) | verb/bridge/synthesis checks pass post-splice |
| I | Compile | none — `latexmk` | `paper_draft.tex` | `paper_draft.pdf` | zero errors; submission checklist pass |

---

## 3. Phase A — validation checklist

Run all; one failure blocks Phase B. Report → `stage_review.md`.

1. **Digest self-verification** — re-execute the checks `digest.md` claims:
   every cross-node reference resolves; all nodes N0–N12 + Claims present;
   every non-GIVEN item carries its 3-part absence comment.
2. **Reference-cache integrity** — every N3 key is a `selected` cache
   record; load-bearing entries have resolvable `digest_path`; spot-check
   2–3 ids by fetching; no `pending` entry cited anywhere.
3. **Tag discipline** — no untagged assertion; no silent
   `[HYPOTHESIS]`→`[GIVEN]` promotion.
4. **Claim–Evidence Map completeness** — every claim traces to an H-id or a
   supported-by-design definition; every H-id has a fallback (or global
   pivot coverage); no orphans either way.
5. **Hypothesis/assumption machinery** — every H\* fills all seven slots of
   guidance.md §3.1 (incl. effect floor + verbatim fallback); every A\*
   fills §3.2 (incl. detection + gate); B0 + B-alt + F-G\* present per
   §3.3.
6. **Method-rigor audit** — guidance.md Part 6 self-check items 1–10, plus
   the Part 2 evidence standard for the declared archetype is met by the
   plan. Any miss → REVISE citing the guidance.md section.
7. **Stage cross-check (advisory)** — `pengsida-stage-reviewer` over
   N1↔Stage 1, N3/N4↔Stage 2, N6↔Stage 3, N8/E\*↔Stage 4, archetype from
   `paper.md`. STOP blocks; REVISE items logged as pre-B fixes.
8. **Taste audit currency** — if the recorded audit predates a material
   edit to the asymmetry statement or formal definition, re-run it.

## 4. Phase B/C — execution discipline

- **B is cheap on purpose.** Frozen thresholds hashed into `B_pilot/`
  before any evaluation; deterministic metrics only; the stated arm list
  and pass criterion. **Instrument validation (guidance.md R2 steps 2–4)
  runs inside B** as PG-\* gates. Scale-up must be a config change, not a
  code change — otherwise the skeleton failed; fix and re-run B.
- **C emits one JSON per RQ and per control arm**:
  `{rq_id|arm_id, point_estimates, intervals, test_statistics, p_values,
  n_per_cell, seed/config hash}` + raw logs under `results/`. Dropped rows
  logged and excluded from every headline n (R8).
- No interpretation during B/C — that is Phase D, and it is mechanical.

## 5. Phase D — verdict lookup & splice (inlined procedure)

Interpretive decisions were made at pre-registration; this phase looks them
up. Order is strict.

1. **Placebo first.** B0 non-null → run invalid; record
   `{"run_valid": false, reason}`; stop; back to B/C (guidance.md Part 4
   situation 1). Never score RQs from an invalid run.
2. **Score each H\*** against its exact pre-registered binary criterion →
   `PASS | FAIL | INCONCLUSIVE` (INCONCLUSIVE only where pre-declared).
3. **B-alt** per contested RQ: effect dies under the rival → apply the
   pre-committed downgrade wording; record which claims survive.
4. **Select the sentence**: PASS → main; FAIL → that H's F\*; combine
   fallbacks exactly as pre-committed.
5. **Global pivot**: central family fails → F-G\* wholesale; the
   pre-committed pivoted abstract replaces Abstract v0; headline CO\* may
   flip. Wrong-direction results are reported at full prominence
   (situation 4).
6. **Emit** `verdicts.json`:
   ```json
   {"run_valid": true,
    "placebo": {"arm": "B0", "null": true, "evidence": "..."},
    "rqs": [{"rq_id": "RQ1", "hypothesis": "H1", "verdict": "PASS",
             "b_alt_survived": true, "sentence_source": "main",
             "numbers": {"...": "filled from results/"}}],
    "global_pivot": false}
   ```
   and rewrite the Claim–Evidence Map → `claim_map.md` with final `Status`
   per claim (`held | held-downgraded | fallback | pivoted`).
7. **`claim_map.md` is the only ground truth for what the paper claims.**
   Phases E–H polish around it; none may strengthen, add, or resurrect.

## 6. Phase E–F — writing discipline

- **Splice, don't re-decide**: claim sentences come from verdict-selected
  wording with numbers substituted from `results/`; `pengsida-paper-writer`
  elevates around them (one claim per paragraph, reverse-outline check).
  One plain-language magnitude gloss per headline number (R4).
- **Related Work from the cache**: per-paper digests are the source;
  `method-twin` entries get concede-and-differentiate treatment
  (guidance.md Part 5).
- Threats = anticipated threats updated with what actually happened;
  Limitations **bounds the claim's setting** (R7), no generic caveats.
- **`refs.bib` script-generated from the jsonl; results tables
  script-generated from `results/*.json`** — hand-typing either is banned.

## 7. Phase G–I — review and close

- `se-paper-reviewer` panels `paper_draft.tex` **with** `B_pilot/`,
  `results/`, and the cache present, so claims-vs-code and coverage checks
  are real; its methodology persona re-applies guidance.md Parts 2–3 as
  review criteria. `[major]` → revise E/F, re-enter G; overrides recorded
  in `stage_review.md`. Reviewer-demanded-but-unrunnable experiments →
  guidance.md Part 4 situation 14.
- `research-taste-auditor` re-audits the **final** abstract (verb check
  included) — splices can reintroduce generic framing.
- Compile with `latexmk`; zero errors; submission checklist;
  `paper_draft.pdf`; mark complete in `pipeline.md`.

## 8. Hard gates (never silently skip)

- Citations only via `selected` cache keys; refs.bib and results tables
  script-generated.
- No instrument runs at scale without passing R2 validation; asserted
  numbers without protocol are treated as absent.
- B0 evaluated before any hypothesis; non-null placebo invalidates the
  whole run.
- Skeleton pass criterion before scale-up; scale-up is config, not code.
- Freshness sweep before Phase E; new method-twin → repositioning + Phase A
  re-check.
- `stale_claim_after_verdict`: before Phase G, check Abstract/Intro/
  Conclusion against `claim_map.md` — pre-fallback wording on a
  `fallback`/`pivoted` claim is a blocking defect. Fix the sentence, never
  the map.
- If the global pivot fired: Phase E rewrites framing from the pivoted
  abstract and Phase H must re-pass.

## 9. Standing TODO (skill maintenance, not per-run)

- `paper-digest`: document the reverse-digest mode (tag scheme replacing
  FOUND/PARTIAL/NOT_FOUND; N3 grounded in the local cache; N9
  `[PLACEHOLDER]` by construction) and the `digest_path` cache convention;
  repackage via `skill-creator`.
- §5's verdict procedure should eventually live inside
  `auto-research-discussion`; until then this file is its canonical home.
- `guidance.md` could be packaged as a standalone skill
  (`empirical-method-rigor`) once proven across topics.

## 10. Definition of done

`discussion/paper_draft.pdf` compiled clean; every claim in `claim_map.md`
carries a final status; `se-paper-reviewer` and the final taste audit are
clean; every citation resolves to a `selected` cache record; every
instrument passed R2 before scale; and the abstract asserts only what
`claim_map.md` licenses — main wording where hypotheses held, pre-committed
fallback or pivot wording where they didn't, nothing stronger than either.

