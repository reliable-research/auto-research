# Goal: topic → taste-checked, stage-reviewed paper draft (per topic folder)

The 45 B/T/H topic folders under `research/topics/` contain a `README.md` (one-line seed idea), a `digest.md` (reverse-engineered N0–N12 knowledge digest), and a `paper.md` (pre-registered spec: asymmetry, formal problem definition, assumptions, RQs with fallbacks). The goal is to turn that seed material into a **taste-checked, stage-reviewed paper draft** — `pipeline.md`, `taste_audit.md`, `stage_review.md`, `paper_draft.md`, `paper_draft.tex`, `paper_draft.pdf` — written into `research/topics/<TOPIC>/discussion/`.

## The pipeline (in order — do not reorder or skip a stage)

```
auto-research-discussion  →  research-taste-auditor  →  pengsida-stage-reviewer  →  assemble paper_draft.md → .tex → .pdf
   (6-stage critic/refiner)     (idea-level taste gate)     (stage-by-stage PASS/
                                                               REVISE/STOP audit)
```

1. **`auto-research-discussion`** (skill, installed at `.claude/skills/auto-research-discussion/`) — run in **autoclaude/self-play mode** (Claude plays both student and teacher) across all 6 stages: Problem Definition → Motivation → Related Work → Sub-Problems → Method Design → Experiment Design. Treat the topic's `digest.md` + `paper.md` as a **high-confidence, already-mature seed** (not a raw repo to reverse-engineer). Per stage: propose v1 → **one genuine critic round** (a real, evidence-grounded major/minor flag — no rubber-stamping, per `references/autoclaude_mode.md`'s anti-sycophancy rules) → one refiner pass → confirmed output. Respect `study_type` gating at Stage 6 (empirical/theory → zero outcome-tier RQs; technical → at least one required). Finish with a cross-stage consistency check — literally recount hypotheses vs. RQs.

2. **`research-taste-auditor`** (skill, installed at `.claude/skills/research-taste-auditor/`) — audit the confirmed Stage 2 (Motivation) + Stage 5 (Method) idea for the generic "Bridge Opportunity + Synthesis/Unification" pattern LLMs overproduce. Report the full verdict (taxonomy labels, 3 diagnostics, dominant verb, 🔴/🟡/🟢). If flagged, reframe before continuing; if clean, say so honestly rather than manufacturing a flag.

3. **`pengsida-stage-reviewer`** (skill, installed at `.claude/skills/pengsida-stage-reviewer/`) — classify the paper's **archetype** first (method / theory / analysis-finding / position / resource — this determines what "Method" and "Experiments" bars even mean; most topics here are `analysis-finding` per `study_type: empirical`). Then apply that stage's PASS/REVISE/STOP bar, quoting the draft directly, against the confirmed Stage 1+2 (Problem+Motivation), Stage 3 (Related Work), Stage 5 (Method), and Stage 6 (Experiments) outputs. Apply any REVISE fix before assembly. The Stage 5 (Writing) bar needs actual prose, so it runs against the **first assembled draft** of `paper_draft.md` — fix and re-render before calling the draft final.

4. **Assemble `paper_draft.md`** per `auto-research-discussion/references/paper_assembly.md`'s exact section rules (Title/Abstract/Conclusion together; flowing-prose Introduction ending in a Contributions list; Problem Definition with formal notation; Method Overview + one Methodology subsection per named module; Experiments with Setup + one subsection per RQ, each with an explicit **Falsification condition** line, not just an "Expected outcome"; thematic Related Work with an explicit nearest-neighbor sentence). No internal stage IDs (`sp_*`, `m_*`, `rq_*`, `C1`-`C5`, `M1`-`M6`) may leak into prose. No fabricated numbers — only pre-registered design targets with stated rationale, and `[placeholder — fill in after experiments are run]` in every Results slot.

5. **Convert to LaTeX and compile.** Hand-write `paper_draft.tex` (no `pandoc` on this machine, no sudo to install it) — `pdflatex` is available. Gotchas: `\usepackage[dvipsnames]{xcolor}` (plain `xcolor` fails on named colors); escape `_ % & # ~ ^` in prose; math mode for notation; `×/≈/≥/≤/α` → `\times/\approx/\geq/\leq/\alpha`, not raw unicode. Compile twice (`pdflatex -interaction=nonstopmode -halt-on-error`), check exit code 0 and zero `! ` errors, then `pdftotext -layout paper_draft.pdf - | grep -c "�"` must be 0. Delete `.aux`/`.log`/`.out`; keep `.tex` and `.pdf`.

## The calibration reference

`research/topics/B5.5_does_reputation_self_correct_exploitation_repeated_bargaining_dy/discussion/` is the completed exemplar — **read all 6 of its files first** before starting a new topic, to match depth, rigor, and honesty (genuine pushback, verbatim hypothesis→RQ traceability, real REVISE findings applied, not invented ones).

## Orchestration notes

- 45 B/T/H topics; process in parallel batches via the `Agent` tool (not `Workflow`, unless the user explicitly opts into multi-agent orchestration) — one topic per agent, self-contained prompt (agents have no memory of prior conversation), calibrated against the B5.5 exemplar path.
- Track batches with `TaskCreate`/`TaskUpdate`; dispatch the next batch once the current one's completions land.
- If the pipeline definition changes again (a new skill added, a step reordered), retrofit already-completed topics rather than treating their prior work as wasted — add the missing step via a lightweight follow-up agent per topic instead of redoing the whole 6-stage loop.

## Status + review-pass extension (2026-08-21)

- **Goal COMPLETE 45/45** (the count grew from 39 to 45: B1.6, B4.6, B7.1, B7.2, B8.1, H1.1 were added and built 2026-08). Every `research/topics/<T>/discussion/` has the full deliverable set.
- A follow-on **review pass** also completed for all 45 topics, adding per topic: `review_2026-08.md` (novelty-auditor DEFENSIVE mode with claim ledger + named nearest neighbors, t_audit=2026-08-15; se-paper-reviewer feasibility/power-arithmetic/staleness with [major]/[moderate]/[minor] severities), concede-and-claim revisions mirrored md↔tex where major/moderate findings fired (recompiled clean), and a Chinese version `paper_draft.zh.md` + `<T>_paper_draft_zh.pdf` (built with weasyprint via a scratchpad md2pdf.py; mojibake check `pdftotext | grep -c "�"` = 0).
- Bib discipline for any future pass: verify arXiv ids against the live export API in ONE batched `id_list` request (per-id loops get rate-banned); script-generated `refs.bib` must only be changed via `reference_candidates.jsonl` + regeneration, keeping both in sync.

