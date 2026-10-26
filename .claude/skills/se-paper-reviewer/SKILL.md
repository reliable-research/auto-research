---
name: se-paper-reviewer
description: >
  Software-engineering-grade peer review for ICSE/FSE/ASE/ISSTA/TSE/TOSEM
  submissions, in both directions — stress-testing the user's OWN paper before
  submission, and writing referee reports / meta-reviews for OTHERS' papers.
  Runs a multi-persona panel (Meta-Reviewer + R1 methodology, R2 domain/related-work,
  R3 significance/impact, plus a Devil's Advocate) over an SE-tuned 0-100 rubric,
  applies the empirical-SE threats-to-validity taxonomy, checks artifact/open-science
  expectations, and (when the codebase is present) audits paper claims against the
  code/data. Triggers on: "review my paper", "referee report", "peer review",
  "meta-review", "what will reviewers ask", "is my contribution clear", "stress-test
  before ICSE/FSE submission", "critique this SE paper", "threats to validity",
  "is this rigorous enough", "rebuttal". Works on LaTeX source, PDF, or a digest.
  Hands off to/from paper-digest (N1-N12 intake), pengsida-paper-writer (archetype +
  rebuttal), and research-paper-writing.
metadata:
  version: "1.0.0"
  status: active
  task_type: open-ended
  related_skills:
    - paper-digest
    - pengsida-paper-writer
    - research-paper-writing
---

# SE Paper Reviewer — ICSE/FSE-grade peer review

A single skill that reviews software-engineering papers the way a competent PC
member would, in **two directions**:

- **Self-review (defensive):** stress-test the user's own draft before submission —
  surface the weaknesses a real reviewer will attack, generate the questions they
  will ask, and pre-build the rebuttal.
- **Refereeing (offensive):** produce a structured referee report or meta-review of
  someone else's SE paper, with calibrated scores and a defensible recommendation.

It is **SE-specialized**, not a general-academic reviewer. The rubric, the
threats-to-validity taxonomy, the baseline/benchmark expectations, and the
open-science checks are all tuned for empirical and systems-oriented SE venues
(ICSE, FSE/ESEC-FSE, ASE, ISSTA, TSE, TOSEM, EMSE, MSR).

---

## When NOT to use this skill

| Situation | Use instead |
|-----------|-------------|
| Need to *write* or improve a section (not review) | `pengsida-paper-writer` or `research-paper-writing` |
| Need an N1–N12 structured decomposition of a paper | `paper-digest` |
| Reviewing a pull request / code (not a paper) | a code-review skill |
| Non-SE field (bio, clinical, social science) | a general `academic-paper-reviewer` |

---

## Step 0 — Intake and routing (do this first)

1. **Identify what you were given:** LaTeX bundle (`.tex`/`.bib`), a PDF, pasted text,
   or an existing N1–N12 digest. If a codebase / repo is also present, the
   **Claim–Code Audit** (Step 4) becomes available.
2. **Decide the direction:**
   - The user says "my paper", "before I submit", "what will reviewers ask",
     "rebuttal" → **self-review mode** (defensive). End with the rebuttal kit.
   - The user says "referee report", "review this paper", "meta-review", names a
     paper that is clearly not theirs → **refereeing mode** (offensive). End with a
     recommendation + confidence.
   - Ambiguous → ask one question, then proceed.
3. **Get a digest cheaply.** If a clean N1–N12 digest isn't already available, build
   the argument skeleton first (problem → motivation → prior-limitation → challenge →
   method → contribution → RQ → result → threat → artifact). If `paper-digest` is
   installed, hand off to it; otherwise extract the skeleton inline. Reviewing
   without first reconstructing the argument chain produces shallow, surface-level
   comments — don't skip this.
4. **Fix the archetype.** SE papers are one of: **method/technique**, **empirical/analysis**,
   **tool/system**, **dataset/benchmark**, **theory/position**. The archetype changes
   what counts as sufficient evidence (see `references/se-rubric.md` → "Archetype
   adjustments"). If `pengsida-paper-writer` is available, reuse its archetype call;
   otherwise classify inline. State the archetype explicitly at the top of the review —
   most weak reviews come from judging a paper against the wrong archetype's bar.

---

## Step 1 — The review panel

Run these personas. In self-review mode they are advisory; in refereeing mode they
produce the actual report. Each persona reads the whole paper but writes only from
its angle, so the angles don't collapse into one bland summary.

| Persona | Focus | Primary rubric dimensions |
|---------|-------|---------------------------|
| **R1 — Methodology** | research design, baselines, statistics, reproducibility, threats to validity | Rigor, Reproducibility |
| **R2 — Domain / Related Work** | positioning vs prior SE work, method-twins, missing citations | Novelty, Positioning |
| **R3 — Significance** | does this matter to SE research or practice; generalizability | Significance, Soundness-of-claims |
| **Devil's Advocate** | *does not score* — only attacks: strongest counter-argument, the one experiment that would break the paper, cherry-picking, claim–evidence gaps | (challenge only) |
| **Meta-Reviewer** | synthesizes the four into one decision + revision roadmap; resolves disagreement | weighted aggregate |

Full persona briefs: `references/personas.md`.
Scoring rubric and decision mapping: `references/se-rubric.md`.
Devil's Advocate stress-test protocol: `references/devils-advocate.md`.

---

## Step 2 — Score against the SE rubric

Score each dimension 0–100 using the behavioral anchors in `references/se-rubric.md`.
The SE-tuned dimensions and weights:

| Dimension | Weight | What it measures (SE-specific) |
|-----------|--------|--------------------------------|
| Novelty & Positioning | 18% | new estimand/technique/finding vs nearest method-twin; honest delta |
| Methodological Rigor | 22% | design↔RQ alignment; baselines; ablations; statistical testing of empirical claims |
| Evidence & Soundness | 20% | claims supported by the reported results; effect sizes + significance, not just means |
| Reproducibility & Artifacts | 15% | can it be re-implemented; artifact availability; open-science badge readiness |
| Threats to Validity | 12% | construct/internal/external/conclusion threats identified AND mitigated, not just listed |
| Clarity & Presentation | 13% | RQ structure, figures, can a knowledgeable reader reproduce the method from the text |

Rules (inherited and kept):
- State which range descriptor matches, *then* fine-tune within it.
- If two dimensions conflict (great method, weak writing) do **not** average them down —
  report both honestly.
- A score is **ordinally** meaningful (75 > 65), not a guarantee of acceptance.
- Anchor to the *target venue's* bar: a 75 for ICSE ≠ a 75 for a workshop.

Decision mapping (refereeing mode): `references/se-rubric.md` → "Decision mapping".

---

## Step 3 — SE-specific checks (run all that apply)

These are the checks general reviewers miss and SE reviewers always run. Full
checklist: `references/se-checklist.md`. The high-value ones:

- **Baseline completeness.** Are the baselines the *ones a reviewer in this subarea
  would demand* (recent SOTA, not just a strawman)? Missing-baseline is the #1
  ICSE/FSE reject reason.
- **Statistical testing.** Empirical SE claims need significance tests + effect size
  (Mann–Whitney/Wilcoxon + Â₁₂/Cliff's δ for non-parametric; report p AND magnitude).
  Means-only comparisons are a rigor flag.
- **Benchmark soundness.** Standard benchmark used correctly? (e.g. Defects4J/Defects4C
  splits, no leakage, no train-on-test). Custom benchmark → is it justified and released?
- **Method-twin positioning.** Is there a recent paper with the *same estimator/technique*?
  If so, the paper must concede the shared part and claim the genuinely-new delta
  (estimand, granularity, setting). Reviewers punish papers that hide a method-twin.
- **Threats-to-validity taxonomy.** Construct / internal / external / conclusion —
  each identified *and mitigated*. A "Threats" section that only lists threats without
  mitigation scores low.
- **Open science.** Artifact availability, anonymized repo for double-blind, data/model
  release. ICSE/FSE increasingly gate on this.
- **LLM-for-SE specifics** (if applicable): model/version pinned, decoding params
  reported, contamination addressed, non-determinism handled across re-runs, cost
  reported. See `references/se-checklist.md` → "LLM-for-SE".

---

## Step 4 — Claim–Code Audit (only if the codebase/data is present)

When the repo is available, verify the paper says what the artifacts show. This is
the highest-signal check for the user's own paper and catches the exact gaps that
sink rebuttals. Protocol and report format: `references/claim-code-audit.md`. Summary:

- **Numerical audit:** every headline number in the paper traced to a result file /
  log / config; exact (not approximate) match; consistent rounding.
- **Method–code alignment:** algorithm/equations/hyperparameters in the text match the
  implementation.
- **Evaluation integrity:** no train/test leakage; metric computed as described;
  re-run a cheap result if possible and compare.
- Output: HIGH / MEDIUM / LOW issues, each with `paper says "…" (file:line)` vs
  `code/data shows "…" (file:line)` and a concrete fix. Always include a
  **Verified Claims** list — it builds confidence and shows the audit was real.

Every flagged issue must carry specific evidence (path, line, exact value).
Distinguish **verified** issues from **suspected** ones. Never approximate.

---

## Step 5 — Generate reviewer questions (self-review) / write the report (refereeing)

**Self-review mode → rebuttal kit:**
- A **weakness table** (category → issue → severity), pulling from the panel + Step 3 + Step 4.
- **Top 10 anticipated reviewer questions**, ranked by likelihood, each with:
  `Q` / `why they'd ask` / `answerable from current data? (cite Table X / needs new run Y)` /
  `draft 2–3 sentence response`.
- **Ablation/experiment triage:** which existing results to foreground; which open
  cells (if any) genuinely need a fresh run before submission vs can be deferred.
- **Specific text edits:** exact paragraphs to strengthen, framed as diffs/suggestions.
- Template: `templates/rebuttal-kit.md`.

**Refereeing mode → referee report:**
- Summary (what the paper claims, in your words — proves you read it).
- Strengths (specific, not generic).
- Weaknesses, ordered major → minor, each actionable.
- Per-dimension scores + weighted aggregate + **recommendation** (Accept / Minor /
  Major / Reject) + **reviewer confidence** (1–5).
- Questions for the authors (for the rebuttal phase).
- Template: `templates/referee-report.md`.

If responding to *received* reviews (rebuttal-writing), hand off to
`pengsida-paper-writer`'s rebuttal mode if available; otherwise use the rebuttal
structure in `references/personas.md` → "Rebuttal discipline".

---

## Operating principles (non-negotiable)

1. **Argument chain before comments.** Always reconstruct problem→…→claim before
   judging. Surface-level reviews are worthless.
2. **Right archetype, right bar.** Judge a tool paper as a tool paper, an analysis
   paper as an analysis paper. State the archetype.
3. **Evidence, not vibes.** Every weakness cites a section/table/figure/line.
   Distinguish *verified* from *suspected*.
4. **Actionable, ranked output.** Every issue carries a specific fix and a severity.
   Never deliver an undifferentiated list.
5. **Honest delta.** The most useful thing this skill does is force an honest
   statement of what is genuinely new vs the nearest prior work.
6. **Don't average away a fatal flaw.** A single invalidating problem (broken
   evaluation, hidden method-twin, unsupported headline claim) caps the recommendation
   regardless of how polished the rest is.
