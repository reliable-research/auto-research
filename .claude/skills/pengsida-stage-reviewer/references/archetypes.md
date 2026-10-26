# Paper archetypes — how the stage bars shift

Refined against an award-paper corpus (NeurIPS/ICLR/ICML/AAAI 2024 best/
outstanding papers). The stage reviewers were originally written method-shaped.
This file is the **first thing the manager fixes** before routing: identify the
archetype, because it changes what Stage 3 and Stage 4 are even *for*. Without
this step, the reviewer mis-fires — it looks for ablations in a position paper,
or for "components tracing to difficulties" in a paper whose contribution is a
theorem or a finding.

## The five archetypes

1. **Method / system.** Contribution = a new technique that works better. Stage 3
   judges the pipeline; Stage 4 judges ablations + baselines.
   *Corpus exemplars: RCML/ECML (AAAI), VAR (NeurIPS).*

2. **Theory / method-with-proof.** Contribution = a new formal object (a loss, an
   estimator, a bound) with guarantees. Stage 3 judges the *definitions and the
   theorem statements*; Stage 4 judges whether each theorem's hypotheses are
   discharged and whether the empirical results corroborate the theory.
   *Corpus exemplar: SEDD / score entropy (ICML) — Definition 3.1, Theorem 3.4,
   Proposition 3.2 carry the contribution as much as the experiments do.*

3. **Analysis / finding.** Contribution = a characterization of *why* something
   happens. There is no new pipeline. Stage 3 judges the *analytical apparatus*
   (is each inferential step licensed?); Stage 4 judges whether the finding is
   **forced by evidence** — ideally via falsification, not just correlation.
   *Corpus exemplar: "Generalization in diffusion models…" (ICLR) — the
   converge-on-disjoint-sets + adversarial-basis tests ARE the contribution.*

4. **Position / critique.** Contribution = a contested claim the field should
   accept, plus the argument for it. There is **no method and no benchmark** in
   the usual sense. Stage 3 becomes "is the **argument** sound?" and Stage 4
   becomes "is the claim **defended against its strongest counterarguments**, and
   are the recommendations actionable?"
   *Corpus exemplars: "Considerations for Differentially Private Learning…"
   (ICML) raises 3 numbered concerns and answers counterarguments inline;
   "Measure Dataset Diversity, Don't Just Claim It" (ICML) advances a posit,
   operationalizes it via measurement theory, and validates with a case study.*

5. **Resource / dataset / foundation.** Contribution = a released artifact
   (dataset, benchmark, model) whose value is its existence + design. Stage 3
   judges the construction methodology and design decisions; Stage 4 judges
   coverage, documentation, leakage/quality controls, and baseline characterization
   — not "does it beat SOTA."

A paper can be a hybrid (VAR is method + scaling-analysis; the diversity paper is
position + finding via its 135-dataset survey). When hybrid, run the dominant
archetype's bar and add the secondary one's Stage-4 check.

## How the archetype rewires each stage

| Stage | Method | Theory | Analysis/Finding | Position/Critique | Resource |
| --- | --- | --- | --- | --- | --- |
| 1 Problem | important + open + first-principles (unchanged across all) | | | | |
| 2 Related Work | threaded limitations; nearest competitor confronted (unchanged) | | | | |
| 3 "Method" | components → difficulties | definitions + theorem statements are well-posed | each analytical step is licensed | the **argument** is valid and its premises hold | construction methodology is principled |
| 4 "Experiments" | ablations isolate each mechanism + baselines | theorem hypotheses discharged + empirical corroboration | finding is **falsified-tested**, not just correlated | claim **survives its strongest counterargument**; recommendations are actionable | coverage/quality/leakage controls; honest baseline characterization |
| 5 Writing | one-message paragraphs; quotable contribution (unchanged, but the "contribution sentence" is a claim/finding/theorem, not a pipeline) | | | | |

Stages 1, 2, 5 are archetype-stable. Stages 3 and 4 are archetype-sensitive —
that is where this file does its work.

## The counterargument check (new, position-critical, useful everywhere)

The corpus's position papers share one feature the original bundle never checked:
they **state the strongest objection to their own claim and answer it**. The DP
paper raises the counterargument "maybe this is just a public-education problem,
not a technical one" and responds; it pre-empts "but the data is public" by
distinguishing *available* from *consented-for-this-use*.

This is now a first-class check:
- **Position/critique:** mandatory. A position paper that doesn't confront its
  strongest counterargument fails Stage 4, full stop.
- **Every other archetype:** a lighter version — "what is the one alternative
  explanation / strongest reviewer objection, and does the paper address it?"
  For method papers this is the ablation that rules out a confound; for findings
  it is the falsification test; for theory it is the assumption a skeptic attacks.

So the deep unity the corpus revealed: **Stage 4, across all archetypes, is one
question — is the claimed cause isolated from its strongest alternative?** Method
papers isolate by ablation, theory by discharging hypotheses, findings by
falsification, positions by counterargument rebuttal. Name the alternative; check
it's ruled out.

## How the manager uses this file

1. Before routing, classify the archetype from the abstract + contributions list
   (look for tells: "we propose a loss/estimator + Theorem" → theory; "we
   argue/posit/caution/Position:" → position; "we show that X arises from…" with
   no new pipeline → finding; "we release/introduce a dataset/benchmark" →
   resource; otherwise method).
2. State the archetype in one line before the first stage verdict.
3. When loading Stage 3 or Stage 4, tell that sub-skill which archetype applies so
   it uses the right column above.
