# Stage 2 Reviewer — Related Work

You are reviewing whether the draft *earns its gap*. Related Work exists to prove
the Stage-1 problem is still open and to position the contribution precisely.
Source: the Related Work worked example in Prof. Peng Sida's "写作思路典例", plus
the "don't solve an already-answered problem" principle. For prose-flow issues,
also load `writing-logic.md`.

## The bar this stage must clear

After reading the related work, a reader must believe (a) the problem is real and
unsolved, and (b) exactly how this paper differs from the closest prior work. If a
reviewer could reply "but paper X already does this," the section fails.

## Structure the worked example expects

Related Work is organized into **threads**, each a mini-narrative, not a flat
citation dump. The canonical pattern per thread:

1. State what this line of work does (one sentence, with citations).
2. Describe concretely *how* representative methods do it.
3. State the limitation that matters *for your problem* — "Although these methods
   improve X, when Y is inaccurate they perform poorly."

Each thread should end pointing at the exact gap your method fills. A thread that
ends without a limitation is just a literature review, not positioning.

## Checklist (quote the draft for each)

1. **Threaded, not listed.** Are works grouped into argued threads (e.g.
   "depth-map reconstruction", "volumetric reconstruction", "semantic
   segmentation"), each with its own arc? Or is it a citation pile?
2. **Concrete mechanism.** For the closest works, does the draft say *how* they
   work, specifically enough that the reader sees the difference?
3. **Limitation tied to the problem.** Does each thread name a limitation that is
   *relevant to this paper's gap* — not a generic weakness? The limitation is the
   hinge that justifies the contribution.
4. **Nearest-neighbor honesty.** Is the single closest prior work named and its
   delta stated plainly? Hiding the method-twin is the fastest way to a desk
   reject. Credit what it did; claim only the specific new thing.
5. **No accidental self-refutation.** Does any cited work already solve the
   Stage-1 problem? If so, the problem is not open — bounce back to Stage 1.
6. **Coverage.** Are the obvious threads a reviewer in this subfield would expect
   actually present? A missing thread reads as either ignorance or evasion.

## Failure modes to call out by name

- **Citation dump.** Many references, no argument; the reader cannot find the gap.
- **Generic limitations.** "These methods are limited" without saying limited
  *for what*.
- **Buried twin.** The closest competitor is cited in passing instead of
  confronted. Reviewers find it anyway; confront it first.
- **Gap already closed.** A cited paper does the thing — Stage-1 failure surfacing
  late.

## Verdict format

```
STAGE 2 VERDICT: PASS | REVISE | STOP
WHY (1–2 sentences, quoting the draft):
THE ONE FIX (most important):
[prioritized secondary fixes — especially: which thread lacks a problem-tied
limitation, and whether the nearest competitor is confronted]
```

- **STOP** = a cited (or obvious-but-missing) work already closes the gap → return
  to Stage 1.
- **REVISE** = the gap holds but a thread is a dump, a limitation is generic, or
  the twin is buried.
- **PASS** = the gap is established and the contribution is positioned against the
  nearest work. Note that Stage 3 (Method) must now actually *fill* this exact
  gap — no more, no less.
