# Cross-Domain Round-Trip: Software Engineering (SE)

After tuning the encode→decode loop on 28 AI award papers (`roundtrip-recovery.md`), the same
loop was run on **software-engineering best papers** (ICSE/FSE/ASE/ISSTA/OOPSLA/PLDI venues) to
test generalization under distribution shift. SE papers stress the encoder differently: they
pair tools with empirical evaluations, introduce benchmarks/datasets routinely, and open with
background before burying the contribution — so they exposed encoder failure modes the AI corpus
never triggered.

Historical calibration from the source snapshot; the machine-specific cross-domain harness is available in the [original source](https://github.com/skill-stability/possible_autoresearch/tree/97cdf786bad3141c8883c7639690da867a44ded5/.claude/skills/pengsida-paper-writer/scripts). These results were not rerun by this merge. Results: `references/corpus/roundtrip_se_results.json`. Six SE abstracts:
`assets/corpus-sample-se/`.

## A data-quality lesson first (honest note)

The initial SE catalog was built from arXiv IDs recalled from memory. An ID↔title↔abstract
audit found **19 of 25 IDs were wrong** (collisions: a "DocTer fuzzing" entry whose abstract was
actually about causal-inference overfitting, etc.). This is exactly the failure that
search-before-asserting is meant to prevent. The fix was to verify every paper by matching its
title against its fetched abstract and discard mismatches, leaving a clean 13-paper SE set with
hand-checked reference labels. **Lesson baked into both skills: never trust an unverified arXiv
ID; confirm the abstract matches the title before using a paper as evidence.**

## Recovery on the clean cross-domain corpus (n = 41)

| Subset | content_recall | node_coverage | type_correct | overall |
|---|---|---|---|---|
| AI (28) | 0.949 | 0.951 | 0.714 | 0.871 |
| SE (13) | 0.960 | 0.971 | 0.462 | 0.797 |
| **Combined (41)** | **0.952** | **0.957** | **0.634** | **0.848** |

Content recall and node coverage **transferred cleanly** to SE (even slightly higher — SE
abstracts are well-structured). The whole gap is in **contribution-type classification**, which
fell from 0.71 (AI) to 0.46 (SE) before fixes and is the only term that did not generalize.

## SE-specific encoder failures and fixes

1. **"essential to study fine-tuned models" ≠ building a model.** `builds_a_model` matched the
   bare token "fine-tune", so SWE-bench (a benchmark that *evaluates* fine-tuned LMs) was vetoed
   out of the benchmark class and tagged `system`. → tightened to first-person build language
   ("we fine-tune our", "we train a", "we release a model"); a benchmark/study that merely
   evaluates fine-tuned models no longer counts as building one. SWE-bench now classifies
   correctly as `benchmark`.
2. **Benchmark framed as "a rich testbed for evaluating … we introduce X".** SE benchmark papers
   often describe the contribution as a testbed/assessment-gap filler rather than literally "a
   benchmark consisting of". → added a signal for `testbed/benchmark for evaluating` +
   `to fill this gap` + `we introduce <name>`.
3. **SE tool papers describe their EVALUATION with study words.** "case study", "we evaluate",
   "we find that" routinely appear in a system paper's evaluation. The empirical rule was
   demoted to fire only when the study is the *primary frame* (headline study intent, or no
   build claim at all) — incidental evaluation language no longer flips a tool to `empirical`.

Net effect: SE type 0.385 → 0.462, SE overall 0.772 → 0.797, **with zero regression on the AI
subset** (held at 0.871) — the fixes are genuine generalizations, not AI-corpus overfitting.

## The irreducible SE gap (honest ceiling)

The 7 remaining SE type errors split into two kinds, neither fixable by keyword rules:

- **Genuinely debatable reference labels.** A paper titled "LLMs Fail at Completing Code with
  Potential Bugs" *introduces a benchmark to make an empirical point* — `benchmark` and
  `empirical` are both defensible. The N12 enum itself notes these overlaps.
- **Buried contribution.** PyTy and METAL open with two sentences of background and state the
  system only deep in the abstract; mid-abstract "we evaluate" fires before the system intro is
  seen. Reliable classification here needs full-text or genuine reasoning about which
  contribution the evaluation validates — what the production LLM extractor does and what a
  heuristic cannot.

So the skills now record a sharper rule, applied in both AI and SE: **set N12 by what the
paper's results actually validate (N9), not by the opening verb or a mid-abstract study word;
when a study introduces a benchmark/dataset to make its point, tag the artifact only if releasing
it is the headline, else tag the finding.**

## How this evolved the bundles

- **paper-digest**: the encoder generalizes across AI+SE now; `builds_a_model`, the benchmark
  testbed signal, and the headline-gated empirical rule are documented in its node schema.
- **pengsida-paper-writer**: gained the cross-domain harness (`scripts/roundtrip_se.py`), the SE
  corpus catalog and sample abstracts, and this findings file. The SE evidence reinforces the
  archetype guidance — SE's tool+evaluation pairing is the clearest real-world example of why
  "what the results validate" must override "the opening verb" when picking an archetype.

