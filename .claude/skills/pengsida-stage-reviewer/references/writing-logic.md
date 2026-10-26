# Writing Logic — the "写作思路" worked example

Shared reference for Stage 2, 3, and 5 reviews. Source: Prof. Peng Sida's
"写作思路典例" and "如何使用copilot和gpt辅助英语写作". The core principle:

> **List the writing logic first — down to what every single sentence says —
> then write the English.** A paragraph is clear only when each sentence has a
> pre-assigned job.

Granularity, coarse to fine: Section → Sub-section → Paragraph → Sentence.
Refine the logic *while* writing — refining the per-sentence plan mid-draft is
the key to a clear paragraph.

Use this file to model rewrites. When a stage reviewer flags a paragraph,
reconstruct its intended sentence-by-sentence logic first, then rewrite — the
same order Prof. Peng uses.

---

## Worked example — Introduction, paragraph logic

The five-move arc (one paragraph each, message in sentence 1):

1. **Problem.** Scene reconstruction matters (AR, robotics, autonomous
   driving) → traditional MVS estimates per-image depth then fuses → it
   struggles on low-texture regions (floors, walls) because matching is
   unreliable there. *Note the move: importance → how it's done → the concrete
   failure and its reason.*
2. **Traditional planar-prior methods.** They use a planar prior to help → here
   is how (triangulation / superpixel / learned plane segmentation) → but when
   depth or plane segmentation is inaccurate, they perform poorly.
3. **Recent implicit methods.** NeRF/IDR/VolSDF/NeuS represent scenes as
   implicit fields learned by differentiable rendering → IDR uses surface
   rendering but fails in complex scenes because gradients only flow on the
   surface point → volume-rendering methods fix that → *however, our experiments
   (Sec. X) show they still fail in low-texture planar regions*, because many 3D
   shapes explain the same images there. *The limitation is shown via the
   paper's own experiment, not asserted.*
4. **Our method.** One innovation sentence: a neural representation encoding
   geometry *and* semantics for indoor reconstruction. Then "Specifically, …":
   detect floors/walls, enforce Manhattan-world geometric constraints; and
   because segmentation may be wrong, jointly optimize a semantic field so wrong
   supervision is down-weighted. *Each move answers a difficulty just named.*
5. **Experiments.** One line on the payoff.

## Worked example — sentence logic (the problem move)

The plan, before any English is written:
- Sentence 1 = "reconstruction matters, here are the applications."
- Sentence 2 = "traditional methods do per-image depth + fusion."
- Sentence 3 = "they're impressive but fail on low-texture regions, because
  matching is unreliable there."

Then, and only then, write the English for each — using an AI assistant to
phrase, then refining the *plan* if a sentence turns out to carry the wrong job.

## Worked example — Related Work thread logic

Each thread = a mini three-move story:
1. What this line of work does (one sentence + citations).
2. How representative methods do it, concretely.
3. The limitation *that matters for your problem*: "Although these methods
   improve X, when Y is inaccurate they tend to perform poorly."

A thread without a problem-tied limitation does no positioning work.

## Worked example — Method sub-section logic

Order: Problem statement → Overview (with figure) → core machinery → the
contribution mechanism → the refinement for the obvious failure case. Each
sub-section opens with *what it achieves*, then *how*. Every component is
introduced by the difficulty it resolves ("Considering that inaccurate
segmentation may mislead the optimization, we additionally …").

---

## How to use this in a review

1. Take the flagged paragraph. Write its intended one-sentence-per-line logic,
   as above. This exposes buried messages and two-message paragraphs instantly.
2. Check: does sentence 1 state the single message? Does each later sentence
   have a distinct job? Are the logical turns marked (Although / However / To
   solve this / Specifically)?
3. Rewrite topic sentence first, then the body, one paragraph at a time. Model
   the connective structure on the moves above.
