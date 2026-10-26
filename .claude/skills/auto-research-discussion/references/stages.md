# Stages reference

Six stages in fixed order. For each stage below: what it is, the field schema, the rubric the critic checks against, the critic's own don't-drift boundaries, and the anti-patterns to flag. This file is synced against the field schemas and checklist registry of the reference platform (a real multi-tenant research-mentorship tool this skill's workflow is modeled on) — the schema and rubric text below are drawn directly from its live templates, not reconstructed from memory.

When you generate a stage's output, fill in the field schema. When you critique it, walk the rubric *and* respect the critic's boundaries (issues that belong to a later stage aren't yours to raise yet). When deciding severity, anti-pattern matches are `[major]` by default.

---

## Stage 1: Problem Definition

**Goal.** State *what* problem the paper solves, with no commitment to *how*.

**Fields.**
```
{
  "summary": "1-3 sentences, the concrete problem definition — not just a topic",
  "formal_summary": "OPTIONAL, AI-suggested: a symbolic/mathematical restatement of the same problem, using lightweight notation (short variable names for key inputs/outputs). Only include if it clarifies rather than adds new assumptions.",
  "input": "what is given at the start — the data, materials, or information available",
  "output": "what must be decided, predicted, or produced — state ALL important outputs, not just the main one",
  "constraints": "real problem-setting assumptions or boundaries — not hidden method ideas, not motivation",
  "objective": "what defines a good solution — evaluable, not aspirational",
  "study_type": "technical | empirical | theory — see below"
}
```

**`study_type` matters more than it looks.** This single field gates what stage 6 is allowed to do:
- `technical` — you're proposing a new method/system/algorithm. Stage 6 *must* include at least one outcome-tier research question (beats-baseline comparison on a macro metric). Default if you don't specify.
- `empirical` — the contribution is measuring or characterizing a phenomenon; the measurement *is* the result. Stage 6 must **not** frame anything as "our procedure beats baseline X" — baselines are optional sanity checks at best.
- `theory` — you're proving a property or deriving a bound. Same restriction as empirical: no beats-baseline framing.

If the user doesn't state `study_type` explicitly, infer it from the `output`/`objective` wording and say so out loud (don't silently guess): language like "prove / theorem / bound" → `theory`; "algorithm / system / detector / classifier / framework that / tool that" → `technical`; "measure / characterize / empirical / observe / quantify / report" → `empirical`. Default to `technical` if genuinely ambiguous — it's the safer failure mode (it asks for a comparison you can drop later, rather than silently exempting the paper from one it needed).

**Rubric.**
- Does `summary` define the problem itself, not a method, model, system, or experiment plan?
- Is `summary` a concrete problem definition, not just a broad topic statement?
- Are `input` and `output` each clearly and independently specified — and if there are multiple important outputs, is each one explicit (not just the main task, partially specified)?
- Are `constraints` real boundaries/assumptions, not a disguised method choice or a motivation statement that wandered in?
- Is `objective` clear, reasonable, and evaluable — not vague or purely aspirational?
- Are `input`, `output`, `constraints`, and `objective` mutually consistent with each other and with `summary`?
- Is there scope confusion, ambiguity, or a missing assumption that would make the problem hard to interpret?
- Does the artifact stay out of later-stage territory — no method design, no experiment design, no prior-work comparison leaking in here?
- If `formal_summary` is present, does it genuinely restate the *same* problem more formally, rather than sneaking in new assumptions or a hidden method choice?
- Is `objective` compatible with the stated `constraints` and `output`, especially when multiple goals are named together?

**Anti-patterns to flag.**
- **`method_leak`** *(major)* — `summary` (or `constraints`) names a technique, architecture, or algorithm. "We solve X *using transformers*" is a method leak. Cut the method; keep the problem.
- **`later_stage_content`** *(major)* — the artifact prematurely introduces method design, experiment design, or related-work comparison. Those belong to stages 3, 5, 6 respectively.
- **`scope_creep`** *(major)* — the statement promises more than one paper's worth of work.
- **`vague_success`** *(minor)* — `objective` reads as "improve performance" with no reference task or metric.
- **`buzzword_substitution`** *(minor)* — a trendy term ("foundation model," "agentic") standing in for a concrete problem description.
- **`fields_misaligned`** *(major)* — `input`/`output`/`constraints`/`objective` don't actually cohere with `summary` or with each other.
- **`formal_summary_drift`** *(major)* — `formal_summary` describes a subtly different problem than `summary`, usually by baking in a method choice under the guise of notation.

**Critic boundaries at this stage — don't drift into:**
- Judging novelty or comparing against prior work. That's stage 3's job; a problem statement isn't supposed to be original, just clear.
- Raising anything that isn't actionable for clarifying the problem definition itself.
- Treating "the artifact names a specific model/tool/solution strategy as part of the problem" as a minor wording nit — that's always `[major]`.

**Refiner behavior at this stage.** The refiner's job is to *formalize*, not redesign: tighten consistency across fields, and — this is a specific, real behavior worth keeping — if the content already supports it, propose or sharpen a `formal_summary` using lightweight notation (assign short variable names to key inputs/outputs) even if the user didn't ask for one. Don't stop at light polishing if the same content could be said more precisely with simple notation. But never introduce a new assumption to get there, and never expand scope.

**Good vs weak.**
- *Good:* "Given a noisy lecture transcript and the speaker's slides, produce a chapter-segmented summary that preserves all numerical claims. Success: ROUGE-L ≥ 0.5 on the EduSum benchmark and zero numerical errors on a 100-clip audit." `study_type: technical`.
- *Weak (method_leak):* "We use retrieval-augmented LLMs to summarize lectures."

---

## Stage 2: Motivation

**Goal.** Justify *why* the problem matters, tied specifically to the outputs and objective confirmed in stage 1 — not to the topic in the abstract.

**Fields.**
```
{
  "summary": "short high-level statement of why this problem matters",
  "why_it_matters": "why solving this would be valuable — the substantive argument",
  "who_cares": "OPTIONAL but strongly encouraged — who is affected or would benefit",
  "evidence": "OPTIONAL but strongly encouraged — concrete signals, examples, incidents, or prior findings backing the importance claim"
}
```

Note what's *not* a field here: there's no `output_coverage[]` array to fill in by hand. Coverage of every stage-1 output/objective by the motivation is something the critic checks holistically against `why_it_matters` — you don't need (and shouldn't force) one bullet per output field. If stage 1 promised chapter segmentation *and* numerical-claim preservation, both need to show up somewhere in the reasoning, in prose, not as a checklist the writer fills mechanically.

**Rubric.**
- Is the motivation genuinely connected to the *confirmed* problem statement (not a generic version of the topic)?
- Does it actually justify the key outputs and objective from stage 1 — not just the general topic?
- Is any important output or objective left unmotivated or only weakly justified?
- If stage 1 requires a nontrivial output (explanation, interpretability, some secondary deliverable), does the motivation explain why *that* matters in practice, not just the headline output?
- Are importance claims specific and credible — backed by stakeholders or evidence, not "this is important because AI"?
- Is there supporting evidence (signal, example, observation)? At this stage you're checking that it *exists and is specific*, not fact-checking it deeply.
- Does the motivation argue for *why now* — what changed that makes this tractable or urgent — rather than a timeless appeal to the topic's general importance?
- Is the motivation about why the *problem* matters, not why a particular method/model/trendy technique is exciting? ("Transformers are having a moment" is not motivation.)

**Anti-patterns to flag.**
- **`partial_output_coverage`** *(major)* — the motivation justifies some outputs/objectives but ignores others. This is the dominant motivation failure the reference platform's checklist was built around — check it explicitly, don't just eyeball it.
- **`generic_appeal`** *(minor)* — "AI is becoming more important" or "this aligns with current trends." Replace with stake-specific reasoning.
- **`unsourced_pain`** *(minor)* — claims something is a problem ("doctors waste hours on X") with no data point behind it. Acceptable to flag rather than block — note it as something to firm up before the paper draft.
- **`method_hype`** *(major)* — the justification is really about a technique being attractive, not about the problem mattering.
- **`unsupported_impact`** *(minor → major if egregious)* — overstating downstream impact with no evidence or stakeholder grounding to carry it.

**Critic boundaries at this stage — don't drift into:**
- Evaluating methods. There aren't any yet, and there shouldn't be.
- Accepting method-centered reasoning as a substitute for problem motivation, even if it's well-written.
- Piling on — prefer fewer, higher-signal questions over a long list of minor comments.

**Refiner behavior at this stage.** Sharpen the link between the confirmed problem and the claimed significance. If the evidence is weak, improve the *phrasing*, not the *strength of the claim* — never invent stronger support than the user gave you.

---

## Stage 3: Related Work

**Goal.** Build a literature landscape specific and strong enough to support stage 4's decomposition — and, for every closely-related paper, an explicit **problem-relative comparison** that establishes where this work is novel and where it is not. Not a bibliography — a set of exploitable, verified gaps plus a defensible novelty position.

### The selection funnel: how papers get chosen and promoted

The reference platform runs stage 3 as a wizard with distinct selection phases, and the discipline transfers directly:

1. **Scout** — gather a broad candidate pool. Search for closest prior work (favor named top venues); snowball from the strongest hits (check what they cite and what cites them). With `web_search` available, this means several searches per problem facet, not one.
2. **Triage the general tier** — keep or drop candidates on citation + abstract-level summary alone. No limitation analysis happens at this tier; keep at least ~3. These become `general_related_works` (landscape/context).
3. **Promote to the specific tier** — select the few papers (the platform caps at ~3 per pass; more is allowed here but each one costs a real analysis) that are *closest* to this problem: same or adjacent problem framing, or a plausible baseline, or a potential novelty threat. Promotion means committing to read the paper's actual content — its problem definition, claimed contribution, method, and evaluation — not just its abstract. If the user can supply the PDF, use it; otherwise fetch/read what's accessible and be explicit about how deeply you actually saw the paper.
4. **Deep-compare each promoted paper** — run the comparison protocol below. This is the step that "constructs the novelty": every specific paper gets analyzed *relative to our confirmed stage-1 problem*, and the outputs mechanically derive what threatens us, what we can exploit, and what must be verified.

### Fields.

```
{
  "summary": "short overview of the current solution landscape",
  "general_related_works": [
    // Landscape tier: kept from triage, citation + abstract-level summary only.
    // No limitations claimed at this tier — you haven't read them closely enough.
    { "work_id": "rw_<slug>", "citation": "Author et al. (Year). Title. Venue.", "summary": "1-2 line summary from the abstract" }
  ],
  "specific_related_works": [
    // Deep tier: promoted papers, read closely, each carrying a problem-relative comparison.
    {
      "work_id": "rw_<slug>",
      "citation": "Author et al. (Year). Title. Venue.",
      "summary": "content-level summary",
      "input_output_framing": "what they take in / produce",
      "approach_summary": "1-2 sentences on their method",
      "is_potential_baseline": true,
      "comparison": {           // ← the deep-compare output, one per specific paper
        "problem_alignment": "same | related | different",
        "alignment_rationale": "one line: OUR problem vs THEIR problem",
        "method_addresses": true,   // could their method, as-is or lightly adapted, solve OUR problem?
        "method_rationale": "one line: if no, why not; if yes, how it would apply",
        "effectiveness": "proven_better | untested | tried_but_weak | n/a",  // n/a only when method_addresses=false
        "threat_to_motivation": "high | medium | low | none",   // derived — see rules below
        "hypothesis_to_verify": "OPTIONAL: concrete falsifiable claim, set when effectiveness=untested",
        "gap_type": "not_solved | not_considered | not_done_well | none",
        "gap_we_address": "concrete description of what they don't solve/consider/do well — relative to OUR problem; sharp enough to seed a sub-problem; empty when gap_type=none",
        "role": "baseline | related_for_context | motivation_threat"
      },
      "limitations": [
        {
          "limitation_id": "lim_<slug>",
          "description": "the specific gap, stated so a sub-problem can target it (usually derived from comparison.gap_we_address)",
          "evidence_for_limitation": "why this limitation holds for THIS paper's setting — not a generic weakness",
          "verify_as_hypothesis": false  // true → becomes a framing-tier RQ in stage 6; default false (most limitations are taken from literature at face value)
        }
      ]
    }
  ]
}
```

### The comparison protocol (per promoted paper)

Walk these four questions in order — each answer constrains the next:

1. **`problem_alignment`** — is their problem the *same* as ours, *related* (adjacent framing, overlapping setting), or *different* (superficially similar topic, incompatible framing)? Justify in one line referring to both problem statements.
2. **`method_addresses`** — could their method, as-is or with minor adaptation, solve OUR problem? This is where `input_output_framing` bites: if their I/O doesn't map onto ours, the honest answer is usually no.
3. **`effectiveness`** — if it addresses our problem, how strong is their evidence? `proven_better` (they already beat alternatives on a comparable benchmark), `untested` (plausibly works, never evaluated for our setting), `tried_but_weak` (evaluated and underperformed, failure modes documented). `n/a` only when `method_addresses` is false.
4. **Derive the implications** — these are mechanical, not judgment calls:
   - `effectiveness=proven_better` **and** `alignment=same` → **`threat_to_motivation: high`**. This is a novelty crisis, not a citation: the paper must either be repositioned against (concede what's shared, claim a genuinely different response variable, granularity, or setting) or the problem itself revisited (back up to stage 1/2). Do not quietly file a high-threat paper under "related work."
   - `effectiveness=untested` → set **`hypothesis_to_verify`** — a concrete falsifiable claim about whether their method actually works in our setting. Flag the corresponding limitation `verify_as_hypothesis: true` so stage 6 generates a framing-tier RQ for it. This turns "we believe X doesn't transfer" from an assertion into a planned experiment.
   - `effectiveness=tried_but_weak` → set **`gap_we_address`** with `gap_type: not_done_well`, citing their documented failure modes as `evidence_for_limitation`.
   - `method_addresses=false` → the gap is `not_solved` (they face the dimension but sidestep it) or `not_considered` (their framing can't even pose the question). `not_considered` gaps are the strongest novelty positions but also the easiest to overclaim — check that the dimension genuinely matters for our objective, not just that they didn't mention it.
   - A paper that does our job well (`gap_type: none`) still gets kept — as `role: baseline` — but produces no limitation, and its existence must be reflected honestly in the novelty positioning.
5. **Assign `role`** — `baseline` (we will compare against it in stage 6), `related_for_context` (shapes the landscape, no direct comparison), or `motivation_threat` (its existence pressures our motivation; must be explicitly answered in the paper's positioning).

**Every `limitations[]` entry on a specific paper should trace to its `comparison`** — usually `gap_we_address` verbatim or sharpened. A limitation with no comparison behind it is an assertion, not an analysis.

**If you have live search available (web_search or similar), use it for the scout and to verify comparisons** rather than working from memory alone. Don't present search-derived summaries with more confidence than the source material supports — and say explicitly which tier of engagement each specific paper actually got (full text read / partial / abstract-plus-search).

### Rubric.
- Was the funnel actually run — a scouted pool triaged into a general tier, with deliberate promotion of the closest papers — or did the specific tier just materialize?
- Is each cited work genuinely relevant to *this* problem, not just loosely related to the same broad area?
- Does each specific work clearly state citation, input, output, and approach?
- Does each specific work carry a complete `comparison`, with the four questions answered in order and the derivations consistent (e.g., `threat_to_motivation` actually follows from `alignment` + `effectiveness`)?
- Is any `threat_to_motivation: high` paper explicitly dealt with — repositioning stated, or an escalation to revisit stage 1/2 — rather than left sitting in the list?
- Is each limitation specific, tied to a `comparison` derivation, and relevant to *this* problem's input, output, objective, or motivation?
- Does the work's `input_output_framing` actually match this paper's framing (stage 1)? If their I/O is different, they're not a baseline — at best `related_for_context`. Reframe what you cite them for, or drop them.
- Are limitations strong enough to motivate a sub-problem later, not just cosmetic weaknesses?
- Are `verify_as_hypothesis` flags used deliberately — set on gaps the paper will spend an experiment confirming (especially `effectiveness=untested` cases), not decoratively?
- Are baseline candidates (`is_potential_baseline`, `role: baseline`) reasonable and consistent with their comparisons?
- Does the general tier have at least ~3 entries with real summaries?

### Anti-patterns to flag.
- **`io_approach_mismatch`** *(major)* — citing a paper as related when its I/O formulation doesn't match yours.
- **`vague_limitation`** *(major)* — a limitation stated so generically that no sub-problem could target it concretely.
- **`missing_comparison`** *(major)* — a specific-tier paper with no `comparison`, or a comparison whose derivations don't follow the rules (e.g., `proven_better` + `same` but `threat_to_motivation: low`).
- **`unhandled_threat`** *(major)* — a `threat_to_motivation: high` paper with no repositioning and no escalation. This is the single most expensive thing to discover at review time instead of now.
- **`overclaimed_not_considered`** *(major)* — a `not_considered` gap claimed for a dimension that doesn't actually matter for the stated objective, or that the paper does implicitly handle.
- **`citation_shopping`** *(minor)* — long lists without distinguishing what the paper actually builds on vs. context.
- **`fabricated_citation`** *(major, hard rule, no exceptions)* — never invent a citation. If you don't actually know a real paper that fits, mark it `[citation needed]` and ask the user, or say plainly that a search didn't turn up a strong match. This is the one rule the reference platform treats as a safety constraint, not a quality one — it appears as a "no fabrication" rule with `critical` severity across the whole platform, not just this step.
- **`untied_limitation`** *(major)* — a limitation not clearly connected to this problem's input, output, objective, or motivation.

### Critic boundaries at this stage — don't drift into:
- Method design, or starting to argue for your own proposed solution. That's stage 5. (Repositioning against a threat paper — "we claim a different response variable" — is a *problem/framing* move and belongs here; designing the mechanism that delivers it does not.)
- Inventing missing citations or external evidence not in the provided material. If it's not there, say so — don't fill the gap with something plausible-sounding.
- Deep-auditing the general tier. The platform's critic audits `specific_related_works` only, plus a light check that the general tier exists (≥3, summaries non-empty). Mirror that: don't demand comparisons for landscape papers.

### Refiner behavior at this stage.
Make entries structurally consistent so stages 4-5 can trace limitations reliably, and check comparison-derivation consistency (alignment + effectiveness → threat level). Do not invent stronger limitations or comparisons than what's there — only clarify wording.

---

## Stage 4: Sub-Problems

**Goal.** Decompose the main problem into sub-problems, each grounded in a real gap. Still no methods.

**Fields.**
```
{
  "summary": "short overview of the main technical challenges",
  "sub_problems": [
    {
      "sub_problem_id": "sp_<slug>",
      "description": "1-2 sentences: what problem must be solved",
      "why_it_is_a_problem": "why this is a real, distinct gap worth treating on its own — NOT why it's technically hard",
      "technical_challenge": "why this sub-problem is genuinely difficult — NOT a restatement of the description",
      "source_limitation_ids": ["lim_<id>", "..."]  // or the literal sentinel ["__novel__"] — see below
    }
  ]
}
```

**The `__novel__` sentinel matters — don't over-apply the "must trace to a limitation" rule.** A sub-problem is allowed to exist without any `source_limitation_ids` from stage 3, *if* it's a genuinely novel, decisive component that your own top-down decomposition surfaced and that no prior paper addresses — set `source_limitation_ids: ["__novel__"]` for those. This is a real, intentional escape hatch in the platform this is modeled on, not a workaround. The failure mode to actually flag is a sub-problem that is *arbitrary* — neither tied to a real stage-3 limitation nor defensible as a decisive component your problem genuinely requires. Don't reflexively call every literature-untethered sub-problem an `orphan_sub_problem`; ask whether it's decisively required first.

**Rubric.**
- Does `description`, `why_it_is_a_problem`, and `technical_challenge` each do its distinct job — what must be solved / why it's a real gap / why it's hard — rather than three restatements of the same sentence?
- Is each sub-problem still method-free? "Design a retrieval module" is a method, not a sub-problem.
- Is each sub-problem specific enough to actually support later method design, rather than restating a broad goal?
- Are the sub-problems logically connected to the stage-1 problem statement — would solving them help achieve the stated outputs/objective?
- Would solving *all* sub-problems together plausibly achieve stage 1's outputs and objective? (If not, something's missing.)
- Are important stage-3 limitations adequately covered by the decomposition?
- Are the sub-problems distinct from each other, not overlapping heavily or minor rephrasings?

**Anti-patterns to flag.**
- **`method_leak`** *(major)* — a sub-problem stated as a proposed method, system, module, or solution idea. "Sub-problem 2: design a retrieval module" → reframe as "ground generated summaries in source-document evidence."
- **`orphan_sub_problem`** *(major, only if truly arbitrary)* — no `source_limitation_ids` and no defensible `["__novel__"]` claim. Either find the stage-3 limitation it targets, mark it novel-decisive with a real justification, or drop it.
- **`undercoverage`** *(major)* — the union of sub-problems doesn't cover the main problem. Literally check: "if all sub-problems were solved, would stage 1's success criteria be met?"
- **`overlap`** *(minor)* — two sub-problems bottoming out in the same underlying issue. Merge.
- **`field_confusion`** *(minor)* — `why_it_is_a_problem` is doing `technical_challenge`'s job or vice versa.

**Critic boundaries at this stage — don't drift into:**
- Suggesting specific solutions, methods, or system components as ways to address the sub-problems. Focus only on whether the decomposition is grounded, distinct, and stated as a problem.

**Refiner behavior at this stage.** Preserve the student's decomposition where possible; clarify boundaries and limitation linkage instead of inventing new structure. Don't redesign the decomposition, and don't jump into method design.

---

## Stage 5: Method Design

**Goal.** Specify concrete methods, each targeting one sub-problem, each carrying falsifiable hypotheses.

**Fields.**
```
{
  "summary": "short overview of the overall methodological direction",
  "methods": [
    {
      "method_id": "m_<slug>",
      "target_sub_problem_id": "sp_<id>",
      "proposed_approach": "concrete description of the mechanism — what you actually do",
      "key_insight": "why this method idea may work — the load-bearing 'why,' not a repeat of the approach or the goal",
      "hypotheses": ["falsifiable claim(s) about what this method achieves, stated so an experiment could refute it"]
    }
  ]
}
```

**Rubric.**
- Does every method target a real `sub_problem_id` from stage 4?
- Does it address the sub-problem's `technical_challenge` specifically, not just its high-level description?
- Is `proposed_approach` concrete enough that two competent researchers would build approximately the same system?
- Does `key_insight` actually explain *why* the method idea may work, rather than repeating the approach or the goal?
- Do `proposed_approach`, `key_insight`, and `hypotheses` form one coherent logical chain?
- Is each hypothesis a concrete, testable claim, and is it **falsifiable** — could a result clearly refute it? "Our method works well" is not falsifiable; "numerical-claim preservation rate ≥95% on EduSum-Audit vs. baseline ~60%" is.
- Are hypotheses informative enough to actually drive stage 6, not so generic they can't be validated?
- Does the full method set cohere at the room/paper level — not just each method in isolation, especially if several sub-problems are being tackled together?

**Anti-patterns to flag.**
- **`goal_restatement`** *(major)* — the "method" paraphrases the sub-problem with no new mechanism. "Sub-problem: preserve numerical claims. Method: a system that preserves numerical claims." This is the dominant failure mode at this stage — push for the actual mechanism.
- **`unfalsifiable_hypothesis`** *(major)* — can't be refuted by any conceivable experiment.
- **`weak_key_insight`** *(minor)* — `key_insight` just repeats `proposed_approach` instead of explaining the "why."
- **`uncovered_sub_problem`** *(major)* — a stage-4 sub-problem has no method targeting it.
- **`mismatch`** *(major)* — the method doesn't actually address the target sub-problem's core challenge, or claims things the mechanism doesn't support.

**Critic boundaries at this stage — don't drift into:**
- Judging experimental quality. That's stage 6.

**Refiner behavior at this stage.** Clarify mechanism and per-method hypothesis wording. Avoid substantially redesigning the method, inventing new components, or adding major new mechanism detail — and don't drift into evaluation planning.

---

## Stage 6: Experiment Design

**Goal.** Design a validation plan that can actually fail — every important hypothesis from stage 5 (and any flagged stage-3 limitation) gets a research question that could refute it, not just confirm it.

**Fields.** Note the shape: `datasets` and `baselines` are shared, top-level lists; the per-experiment unit is a `research_question`, not a flat `experiment`.

```
{
  "summary": "two-three sentence overview of the evaluation plan",
  "datasets": [{ "name": "...", "justification": "why this dataset actually stresses the hypothesis" }],
  "baselines": [{ "name": "...", "justification": "why beating this comparison would mean something" }],
  "research_questions": [
    {
      "rq_id": "rq_<slug>",
      "tier": "mechanism | framing | outcome",
      "description": "the question this RQ answers",
      "target_sub_problem_id": "sp_<id>",
      "target_hypotheses": ["VERBATIM text of the source hypothesis — exact match, not paraphrase"],
      "setup": "reproducible protocol: what's run, how",
      "sample_size_rationale": "N=X, justified (power analysis, coverage argument, etc.) — a design choice, not a fabricated fact",
      "statistical_test": "e.g. paired t-test at α=0.05, or a monotonicity/variance-bound check for measurement-style claims",
      "expected_outcome": "the falsifiable predicted result — name the threshold or sign of effect",
      "metrics": "how the expected outcome gets measured"
    }
  ]
}
```

**The tier system is the load-bearing structure here — get this right before anything else:**

- **`mechanism`** *(default, one RQ per method hypothesis)* — tests a specific hypothesis from stage 5's `methods[].hypotheses`. `target_hypotheses` must be a **verbatim, exact-match** copy of that hypothesis text — not a paraphrase. Every hypothesis stage 5 produced needs one of these.
- **`framing`** *(opt-in, only from flagged limitations)* — tests a stage-3 limitation that was marked `verify_as_hypothesis: true`. The hypothesis text comes from that paper's `comparison.hypothesis_to_verify` when present (the typical `effectiveness=untested` case), falling back to the limitation's `description`. If nothing was flagged, emit zero framing-tier RQs — don't manufacture one.
- **`outcome`** *(conditional on `study_type`)* — an end-to-end comparison against baselines on a macro metric (effectiveness/efficiency/coverage).
  - `study_type === technical` → **at least one outcome-tier RQ is required.** Zero is a major flag.
  - `study_type !== technical` (empirical/theory) → **outcome-tier RQs are forbidden.** If one appears, that's a major flag: this paper's contribution is the procedure or property itself, not "we beat baseline X." For these papers, hypotheses and RQs are about attributes of the measurement/procedure — reproducibility, non-circularity, sensitivity, monotonicity, robustness, soundness — and baselines are optional sanity checks at best (does the procedure return a trivial answer on a trivial input), not competitors to beat.

**Rigor filters — apply before accepting any research question, not just when critiquing one:**
- **No tautologies.** If an RQ would pass by construction — it only re-asserts what the method/procedure was built to do — discard it and tighten. The experiment has to be able to *fail*.
- **Baselines must be informative.** If no baseline is close enough to the method to make beating it mean something, that's a weak baseline, not a passable one — add a real comparator and justify it.
- **Don't fabricate results; do author target design parameters.** Never invent a cited number ("as reported in [X], the dataset has 9,231 entries"). Freely *author* a target sample size, threshold, or statistical test with a stated rationale — that's a design decision you're allowed and expected to make, not a fact you're claiming already holds.

**Rubric.**
- Does every important hypothesis from stage 5 get covered by at least one research question — not just loosely implied?
- Is `target_hypotheses` specific enough to show exactly what claim is being validated, and does it literally (not approximately) match its stage-5 or stage-3 source?
- Is `setup` specific enough to show how the RQ would actually be answered and the hypothesis actually tested — including sample size and statistical procedure?
- Does the setup isolate and validate the *claimed contribution*, not just report an overall performance number?
- Is `expected_outcome` a genuine falsifiable prediction that would help answer the RQ, not a hope?
- Are `metrics` concrete enough to evaluate the expected outcome?
- Do datasets and baselines have clear justifications tied to what they're supposed to stress?
- Do datasets, baselines, and research questions together tell a credible validation story for the paper's actual claims?
- Would a reviewer be able to see, from this plan alone, how each important hypothesis gets tested — not just which metrics get reported?

**Anti-patterns to flag.**
- **`question_hypothesis_mismatch`** *(major)* — the RQ's `description` and its `target_hypotheses` are about different things.
- **`uncovered_hypothesis`** *(major)* — a stage-5 hypothesis (or a flagged stage-3 limitation) with no RQ targeting it.
- **`tier_violation`** *(major)* — a technical paper with zero outcome-tier RQs, or a non-technical paper with any outcome-tier RQ.
- **`paraphrased_target`** *(major)* — `target_hypotheses` doesn't literally match the source hypothesis text.
- **`weak_baseline`** *(minor → major if egregious)* — baseline too weak for beating it to mean anything.
- **`metric_not_aligned`** *(major)* — the metric doesn't actually measure the claimed outcome.
- **`tautology`** *(major)* — the RQ would pass by construction; see rigor filters above.
- **`fabricated_number`** *(major, hard rule)* — a cited number presented as fact rather than a stated design target.

**Critic boundaries at this stage.** None declared as off-limits in the reference platform — this is the stage where the critic is meant to bear down hardest, and where a lightweight adversarial pass ("would this RQ survive a reviewer trying to break it?") pays off most.

**Refiner behavior at this stage.** Improve traceability from research questions back to sub-problems and hypotheses; strengthen internal consistency. Don't make the plan *bigger* — don't add datasets, baselines, or RQs that weren't already implied.

---

## Cross-stage consistency rules (run on every critique)

These checks are run by the critic regardless of which stage you're currently on:

1. **No method leak** in stages 1, 2, 4. Methods only appear in stage 5.
2. **ID stability** — once a `work_id`, `limitation_id`, `sub_problem_id`, `method_id`, or `rq_id` is confirmed, don't rename it. If the underlying thing changes, propose a new ID and deprecate the old.
3. **Reference integrity** — every `source_limitation_ids` in stage 4 must exist in stage 3 (or be the `["__novel__"]` sentinel); every `target_sub_problem_id` in stage 5 must exist in stage 4; every `target_hypotheses` entry in stage 6 must be a **verbatim** match to something in stage 5's `methods[].hypotheses` (mechanism tier) or a stage-3 limitation flagged `verify_as_hypothesis: true` (framing tier).
4. **Output coverage** — the chain `output (stage 1) → why_it_matters (stage 2) → sub_problems → methods.hypotheses → research_questions` shouldn't lose anything along the way. If stage 1 promises three outputs and only two are reachable through the chain by stage 6, raise it.
5. **`study_type` consistency** — stage 1's `study_type` (explicit or inferred) determines whether stage 6 needs an outcome-tier RQ (`technical`) or forbids one (`empirical`/`theory`). If `study_type` changes after stage 6 was already confirmed, that's a reason to revisit stage 6, not silently reinterpret it.

These cross-stage checks are how this skill earns its keep — they're the things a single-shot drafting skill won't do.
