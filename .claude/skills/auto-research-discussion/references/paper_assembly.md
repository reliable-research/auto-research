# Paper assembly reference

Once all six stages have confirmed outputs, this skill produces a paper draft. Read this file before generating the draft. The section-by-section guidance below is drawn from the reference platform's actual paper-generation prompts — it's considerably more prescriptive than a generic section-mapping table, and that prescriptiveness is the point: most of it exists to suppress specific tells of AI-assembled papers (internal ID labels leaking into prose, mechanical "First,...Second,...Third" enumeration, `[CITE]` placeholders, module-by-module abstract/conclusion recaps).

## The one rule that matters most: no internal labels in prose

Every section below draws on structured IDs — `sp_1`, `m_2`, `rw_3`, `lim_greedy_decoding`, UUIDs. **None of these may appear in the rendered prose, ever.** Refer to sub-problems, methods, and related works by their *substantive* name or role ("the confused-deputy threat model," "the dual-ledger metric," "capability-based defenses"), never by their internal ID or ordinal position ("Sub-Problem 2," "M1," "the second module"). This is the single most common tell that a paper draft was assembled mechanically rather than written, and it's worth a dedicated pass over the draft specifically to check for stray IDs before showing it to the user.

Closely related: avoid `[CITE]` or `[TODO]` placeholders. If `related_works[].citation` has a real bibliographic string, use it inline directly ("capability-based defenses such as Author et al. [Year]"). If a citation is genuinely missing, fall back to a generic reference ("a recent system [Year]") rather than inventing an author name — never invent one.

## Section-by-section guidance

### Title, Abstract, Conclusion — generate together

These three are tightly coupled and worth drafting as one pass, not three independent ones.

- **Title**: 10-15 words, concrete about the mechanism, not just the domain. Avoid vague adjectives ("novel," "effective," "advanced"). Should hint at the method's actual core idea, not just restate the problem.
- **Abstract**: 150-200 words, one paragraph, four moves — (a) the problem and its real-world importance, from stage 2; (b) the gap in existing work, from stage 3's limitations; (c) the method, described by role and core insight, not by internal labels; (d) the evaluation plan (datasets/baselines from stage 6), present tense, **no fabricated numbers or outcomes** — the experiments haven't been run yet.
- **Conclusion**: 150-200 words. Restate the problem broadly; summarize the approach *as an integrated whole*, not module-by-module (no "the first module... the second module..."); state expected impact based on the evaluation plan; 1-2 sentences of concrete future work drawn from unresolved minor flags. **The conclusion must not simply repeat the abstract** — it reflects on significance and points forward, not a recap at the same altitude.

### Introduction — flowing prose, not subsection-per-topic

Write 4-6 paragraphs of continuous prose. **No subsection headings** ("Background," "Existing Work," "Our Approach," etc.) — the only acceptable heading is an optional final "Contributions" bullet list. Weave these elements in, roughly in this order, with natural transitions rather than labeled breaks:

1. Open with the research domain in accessible terms — what's happening in practice, why this setting is common now. Draw from stage 2 (`why_it_matters`, `evidence`). No formal I/O definitions yet.
2. Pivot to the gap: the specific problem and its significance, from stage 1's `summary`. Make the pivot feel like a natural observation ("Yet a central question remains unanswered"), not a section break.
3. Survey existing approaches and their shared limitation in 1-2 paragraphs, naming prior work by its substantive identity using the citation field directly inline. When enumerating multiple clusters of prior work, prefer naming each by its substantive identity over ordinal position; if you must use ordinal connectors, vary them ("a first difficulty... another challenge... finally...") rather than mechanically repeating "First,... Second,... Third."
4. State the technical challenges as part of the gap discussion, from each sub-problem's `technical_challenge` — again by substantive name, not `sp_1`/`sp_2`.
5. Introduce the method as **one coherent idea**, not as N separate answers to N separate challenges. Lead with the central insight, then trace how the pieces support it in one paragraph. Name modules by role, not by ID.
6. Preview the evaluation in 1-2 sentences — datasets and baselines from stage 6, present/future tense, no fabricated numbers.
7. End with contributions: either a bulleted list (3-5 items, each starting with an action verb — "We propose...", "We show...") derived from each method's `key_insight`, or a closing "In summary, we contribute..." paragraph.

Style throughout: concrete claims over hedged ones, varied sentence length, no filler ("it is worth noting that," "in this paper, we").

### Problem Definition / Preliminaries

Two parts:
1. **Formal problem definition** — precise, using notation if the content supports it (stage 1's `formal_summary` is the natural seed for this). State input, output, objective, and constraints with consistent notation.
2. **Challenges** (one paragraph) — why the *formally defined* problem is hard, grounded in the symbols just introduced (reference the input space, output requirements, constraints by name), drawing from each sub-problem's `technical_challenge` but reframed in terms of the formal structure rather than repeated verbatim from the Introduction.

### Method Overview — flowing narrative, no subsection headers

One to two paragraphs giving the reader a conceptual picture of the whole framework — input, output, high-level flow — weaving in how the pieces connect as part of the flow, not as a separate "Component Interactions" aside. Then 2-3 sentences per module: role, and which challenge it addresses, named by role, not by `m_1`/`sp_1`/UUID. No implementation detail here — that's the next section.

### Methodology — one subsection per method module

`## [Module Name]` headings, no section numbers, named by the module's actual name or a short descriptive phrase — never `M1`/`M2`. For each:
1. **Challenge** (1-2 sentences) — the specific technical challenge this module solves, from `technical_challenge`, described in plain language (don't write "Sub-Problem 1").
2. **Insight** (1-2 sentences) — the design rationale, from `key_insight`, framed as *why this design works*, not as a testable hypothesis (hypotheses belong in Experiments).
3. **Method** — the technical detail, from `proposed_approach`.

Don't repeat the Overview's high-level description here; go deeper, not wider. Don't mention hypotheses.

### Experiments

Start directly with `## Experimental Setup` — no "Note: this section presents the experimental design" framing text.
1. **Experimental Setup**: datasets, baselines, metrics, key hyperparameters, with justification for each choice.
2. **Research questions**: a short numbered list (RQ1, RQ2, ...), one sentence each.
3. **One subsection per RQ** (`## RQ1: [question title]`): state the RQ and the plain-language challenge it targets → describe the setup (what's measured, baselines compared, ablations) → state the expected outcome (falsifiable, from `expected_outcome`) → summarize the hypotheses in plain language (no internal labels) → list metrics. **Never fabricate numeric results** — this is a plan, not a report.

**Respect `study_type`.** If stage 1's `study_type` is `technical`, at least one RQ should read as an outcome-tier, beats-baseline comparison. If it's `empirical` or `theory`, do **not** frame any RQ as "our procedure beats baseline X" — frame mechanism/framing-tier RQs as validating attributes of the procedure or property itself (reproducibility, sensitivity, soundness, robustness), with baselines appearing only as sanity checks if at all.

### Related Work

Continuous prose, grouped into 2-4 thematic categories (not one paragraph per paper). For each category: one sentence naming the line of work → 2-4 sentences on the general approach of representative papers, citing them inline by their real citation string → one closing sentence naming the shared limitation that motivates this paper. No `[CITE]` placeholders, no `[TODO]`, no internal identifiers, no discussion of your own method here.

## What the draft is and isn't

The draft is a **section-structured Markdown document with placeholders for results and figures**. It's not a finished paper — it can't be, because experiments haven't run yet. It's also only one of the run's three deliverables (see SKILL.md "Final deliverables"): the **experiment design spec** ships as a separate standalone document rendered from stage 6's confirmed output, and the paper's Experiments section must stay synchronized with it — same RQs, same setups, same expected outcomes; if a late edit changes one, change both. The user will either run the experiments (from the spec, not the paper) and fill in result placeholders, or take the draft to `research-paper-writing` for prose polish and LaTeX conversion. Mark placeholders clearly:

```
## RQ2: Does retrieval-grounded decoding preserve numerical claims?

**Setup.** Datasets: EduSum-Audit (n=100, target — sized to detect a 10-point
gap at α=0.05). Baselines: vanilla GPT-4o summarizer; ROUGE-optimized BART.
Metrics: numerical-claim preservation rate (primary); ROUGE-L (guardrail).

**Expected outcome.** If H2 holds, preservation rate ≥ 0.95, ROUGE-L drop ≤ 0.02.

**Result.** *[placeholder — fill in after experiments are run]*
```

Note the distinction in that example: a target sample size *with a stated rationale* is a legitimate design choice to author yourself, not a fabrication — the line to hold is on results and citation-attributed numbers, not on the experiment's own design parameters.

## Internal structure first, then prose

Don't go straight from confirmed outputs to flowing prose. Build a structured intermediate representation first — section title, list of points, list of references to confirmed outputs — then expand each point into prose. This makes it obvious when a section can't be written yet (a method with no hypothesis means the discussion has nothing to discuss), lets the user spot structural problems before reading prose, and makes single-section regeneration easy.

If the user asks for "just the introduction" or "regenerate the method section," produce only that section, but use the same structured-first approach.

## Length targets

Default targets unless the user specifies a venue:
- Abstract: 150-200 words (this is the reference platform's actual target — tighter than you might default to)
- Introduction: 4-6 paragraphs (~700-1100 words)
- Method: 2-4 pages worth
- Experiments: 1.5-3 pages worth
- Other sections: scale to content

If the user names a venue (NeurIPS 9-page main, ICLR 9-page main, ACL long, etc.), adapt — but don't try to hit a hard page count. That's the LaTeX conversion's job.

## Honest gaps

If a stage's confirmed output is shallow — e.g., stage 6 only has one research question because the user didn't push for more — produce a draft that reflects that honestly. Don't pad. Add a clearly-marked "Further evaluation" subsection listing what *would* be tested with more time, drawn from unresolved minor flags.

## Pre-handoff checklist (mined from real reviewer comments)

Before presenting the draft, run one pass over these — each is a recurring complaint mined from actual peer reviews of submitted papers, filtered to the ones a draft (as opposed to a camera-ready) can already get right:

- **Organization and navigation** — can a reader follow the narrative without jumping between distant sections? Does each paragraph advance the argument rather than restate the previous one?
- **Terminology discipline** — every domain-specific term, label, and symbol defined at first use, then used consistently. This is where stage-output field names sneaking into prose usually get caught too.
- **Notation with worked examples** — central formal constructs get precise definitions, consistent notation, and at least one worked example or input→output walkthrough.
- **RQ framing matches outcomes** — research questions phrased to match graded/quantitative outcomes, not as binary yes/no items, and each answered in its own subsection.
- **Actionable implications** — the conclusion/discussion says something concrete about what the results mean for future research or practice, with limitations and specific next steps — not just a recap.
- **No typesetting artifacts** — no leftover placeholders, broken references, malformed markup; internal IDs already covered above but re-scan here.
- **Artifact plan stated** — if code/data release is claimed anywhere, the draft says what will be released and roughly how (README, dependencies, example traces), rather than a bare "code will be made available."

(Figure/table resolution and final proofreading belong to the LaTeX/camera-ready stage — note them for the hand-off but don't block the Markdown draft on them.)

## Hand-off

After producing the draft, tell the user:
- The next natural step is `research-paper-writing` for prose polish, LaTeX conversion, and figure work
- Or `docx` if they want a Word version
- Or coming back to this skill if a stage needs revision — cross-stage problems (an uncovered hypothesis, a `study_type`/tier mismatch) often only become visible once the draft is on the page

Keep the draft as Markdown by default. Don't try to produce LaTeX or `.docx` from inside this skill — those formats have their own conventions and dedicated skills handle them better.
