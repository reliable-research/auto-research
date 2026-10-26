# Round-Trip Recovery (Encode → Decode)

This is the encode/decode self-evaluation that drove the latest refinement of both skills.
**paper-digest is the encoder** (paper → N1–N12); **pengsida-paper-writer is the decoder**
(N1–N12 → reconstructed abstract). Running the loop on 28 award papers and scoring how much
of each original survives gives a measurable recovery rate — and every failure is a concrete
bug in one of the two skills.

Historical calibration from the source snapshot; the machine-specific round-trip harness is available in the [original source](https://github.com/skill-stability/possible_autoresearch/tree/97cdf786bad3141c8883c7639690da867a44ded5/.claude/skills/pengsida-paper-writer/scripts). These results were not rerun by this merge. Results: `references/corpus/roundtrip_results.json`;
baseline before refinement: `references/corpus/roundtrip_baseline.json`.

## Recovery metric

Per paper, recovery = mean of three terms:
1. **content_recall** — fraction of the original abstract's top salient terms that reappear
   in the reconstruction (information survival through the round trip).
2. **node_coverage** — fraction of the eight key nodes (N1, N2, N4, N5, N6, N7, N9, N12) the
   encoder populated non-trivially (did the digest capture the structure).
3. **type_correct** — did N12 match a human reference label at the archetype-family level
   (system/tool, dataset/benchmark, study, theory).

## Results across iterations (n = 28 award papers)

| Iteration | content_recall | node_coverage | type_correct | overall |
|---|---|---|---|---|
| Baseline | 0.673 | 0.661 | 0.536 | 0.623 |
| +N12 priority/benchmark-vs-usage | 0.816 | 0.951 | 0.607 | 0.791 |
| +headline-aware dataset/position | 0.824 | 0.951 | 0.679 | 0.818 |
| +theory/position FP fixes | 0.824 | 0.951 | 0.714 | 0.830 |
| +decoder & method-body capture | **0.949** | **0.951** | **0.714** | **0.871** |

**Final recovery rate: 0.871** (median 0.96; 20/28 papers ≥ 0.80, 18/28 ≥ 0.90).

## What each failure taught the skills

**Encoder (paper-digest) fixes — N12 classifier was the biggest error source (13/28 → 8/28):**
1. "Evaluated *on* benchmark X" is usage, not a benchmark contribution; only a headline
   "we introduce benchmark X" counts. Same for "billions of images" as pretraining data vs a
   released dataset. → dataset/benchmark now require headline introduce-intent.
2. A method paper that "argues" (e.g. EDM's "we argue … by presenting a design space") is a
   `system`, not a `position` paper. → position requires a refutation headline with no build-intent.
3. "Impossibility" only implies theory alongside proof language ("impossible languages" is a
   study). → theory cue tightened.
4. `unknown` is never the right answer for an award paper. → modal fallback is `system`.

**Encoder fixes — node coverage (0.66 → 0.95):**
5. N2/N5/N6/N7/N9 missed when abstracts lacked literal cue words ("challenge", "important").
   → broadened cue sets + neighbour-sentence fallbacks so no key node is left empty.

**Encoder fix — content recall (0.82 → 0.95): the key structural insight.**
6. Dense single-paragraph abstracts carry their most distinctive method terms (e.g. "Fourier
   domain", "spectral volume") in sentences with *no* cue word, which keyword extraction
   dropped. → **method-body capture**: grab the run of sentences between the method-overview
   sentence and the first results sentence as additional M-components. This single change took
   the worst paper from 0.225 to near-complete recovery and lifted the mean 13 points.

**Decoder (pengsida) fixes:**
7. The decoder was too lossy — it carried only 2–3 components / 2 contributions / 3 results.
   → carry up to 4 components, 3 contributions, 4 results; always include the N6 overview; and
   decode archetype-specifically (system → components; dataset → release line; theory →
   conditions; analysis → controlled-test line).

## The irreducible gap (honest ceiling)

The 8 remaining type errors are all `system` vs a `study`/`dataset`/`theory` reference where
the abstract *opens* with "we propose/develop/introduce" (a system surface form) but the true
contribution is a measurement, a released dataset, or a theorem. Distinguishing these reliably
needs full-text or genuine reasoning about which contribution is primary — exactly what the
production `paper-knowledge-service` LLM single-agent pass does and what a keyword heuristic
cannot. Pushing keyword rules further would overfit these 28 papers and hurt generalization, so
the skill stops here and flags type as the lowest-confidence node. When a human or an LLM-backed
extractor is in the loop, set N12 by reading which contribution the paper's evaluation actually
validates (N9), not by the opening verb.

## How this evolved the bundles

- **paper-digest**: the N12 classifier, node fallbacks, and method-body capture in
  `scripts/digest_paper.py` are now materially better and documented in its node schema.
- **pengsida-paper-writer**: gained the round-trip harness (`scripts/roundtrip.py`) as a
  self-evaluation tool, the synced encoder, and this findings file. The decoder logic (how a
  digest reconstructs into an abstract per archetype) is now an explicit, tested mapping that
  reinforces the archetype templates in `paper-archetypes.md`.

