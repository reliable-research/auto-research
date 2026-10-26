# Stage 3 Reviewer — Method (and its archetype variants)

> **Read the archetype line from the manager first.** This stage is
> archetype-sensitive. The method-paper bar below is the default; if the paper is
> a theory, finding, position, or resource paper, jump to "Archetype variants" at
> the end and apply that bar instead. `archetypes.md` has the full table.

You are reviewing whether the method *actually solves the motivated problem*,
cleanly, by first principles. Source: the Method worked example in Prof. Peng
Sida's "写作思路典例" (sub-section and sentence granularity) and the
first-principles / solve-it-to-99% principles. For prose-flow issues, also load
`writing-logic.md`.

## The bar this stage must clear

A reader must be able to say, in one breath: the task, the exact technical
challenge being solved, the contribution, and *why it works*. Each design choice
must trace to a difficulty named in the motivation — no orphan machinery, no
complexity without payoff.

## Structure the worked example expects

The Method unfolds as: **Problem statement → Overview → core machinery → the
contribution mechanism → the refinement that handles the obvious failure case.**
Each sub-section is introduced by what it achieves, then how.

Crucially, the worked example narrates the method as a *chain of motivated moves*:
we do X; we observe X fails in case Z (with a figure); so we add Y to handle Z.
Every component earns its place by fixing a stated problem.

## Checklist (quote the draft for each)

1. **Challenge → mechanism mapping.** For each component, is there a sentence that
   says which difficulty it resolves? A component with no "because" is a candidate
   for deletion. List any orphan components.
2. **First-principles, not patch.** Is the design solving the root cause, or
   stitching two prior methods into something *more complex with no essential
   gain*? If the latter, this is the fatal critique — state it.
3. **One-breath summary.** Can you restate task + challenge + contribution +
   why-it-works in one sentence from the draft? If not, the method story is
   unclear; locate the missing link.
4. **Anticipated failure handling.** Does the method show awareness of where its
   own naive version breaks (e.g. "inaccurate segmentation misleads the
   optimization, as shown in Fig. 1(c)") and add the mechanism that fixes it?
5. **Notation and definitions.** Are symbols defined where introduced; are losses,
   inputs, and outputs unambiguous? A reader should be able to reimplement.
6. **Solve-to-99%.** Does the method *close* the problem, or only nudge it to
   "good enough"? Prof. Peng's self-critique is exactly the half-solved method
   that "published papers but solved nothing." If it stops at fancy-but-partial,
   say so.
7. **Overview before detail.** Is there an overview (with the figure) before the
   machinery, so the reader holds the shape before the equations?

## Failure modes to call out by name

- **Orphan component.** Machinery with no problem it answers — cut or justify.
- **Patch architecture.** A's module + B's module, more complex, no real win.
- **Unfalsifiable prose.** "We carefully design…" with no mechanism. Replace with
  the actual move and its reason.
- **Half-solution dressed as full.** Pushes a metric up but leaves the motivated
  problem standing.
- **Method that doesn't match the gap.** Solves something adjacent to, but not,
  the Stage-2 gap.

## Verdict format

```
STAGE 3 VERDICT: PASS | REVISE | STOP
WHY (1–2 sentences, quoting the draft):
THE ONE FIX (most important):
[prioritized secondary fixes — especially: every orphan component, any
patch-architecture smell, and any broken challenge→mechanism link]
```

- **STOP** = the method is a patch with no essential improvement, or it solves a
  different problem than the one motivated → rethink the approach (or revisit
  Stage 1/2).
- **REVISE** = the core idea is sound but components are unmotivated, the story
  isn't one-breath clear, or the failure case isn't handled.
- **PASS** = each piece traces to a stated difficulty and the why-it-works is
  legible. Note that Stage 4 must now *prove* each claimed mechanism actually
  causes the improvement.

---

## Archetype variants (apply instead of the method bar above when relevant)

The default bar judges a pipeline. For other archetypes, the *object* under
review changes — but the spirit is constant: **does every element earn its place,
and does the contribution survive scrutiny?**

**Theory / method-with-proof** (e.g. SEDD's score entropy). The contribution
lives in the *definitions and theorem statements*, not a pipeline.
- Is each formal object (loss, estimator, bound) *well-posed* — defined before
  use, with its domain and assumptions stated?
- Does each theorem's statement actually deliver what the intro promised (e.g.
  "naturally extends score matching to discrete spaces" → is there a consistency
  result that makes "extends" precise)?
- Are the theorem *hypotheses* reasonable, or so strong they trivialize the
  claim? (The discharge of those hypotheses is a Stage-4 matter; their
  *reasonableness* is judged here.)
- PASS = the formal apparatus is well-posed and the theorems, if true, deliver
  the contribution. STOP = the central definition is ill-posed or the headline
  theorem doesn't say what the intro claims.

**Analysis / finding** (e.g. diffusion-generalization). No new pipeline; the
"method" is the *analytical apparatus*.
- Is each inferential step *licensed* — does the chain "A, therefore B, therefore
  the finding" have no unjustified jump? (In the exemplar: denoising error bounds
  density error → denoiser convergence implies density convergence. That hinge is
  what makes everything downstream valid; check it exists.)
- Is the central construct *defined precisely* before it is observed, not named
  after the fact?
- PASS = the apparatus is principled and the finding follows from it. The
  *falsification* of the finding is Stage 4.

**Position / critique** (e.g. the DP and dataset-diversity papers). The "method"
is an **argument**.
- Are the claim's premises stated and individually defensible?
- Is the argument *valid* — do the numbered concerns actually support the thesis,
  or are they loosely associated grievances?
- Is the scope honest (does it claim more than the argument supports)?
- For constructive positions (diversity paper): is the proposed framework
  (measurement theory → reliability/validity) actually *operationalized*, or only
  gestured at? A position that recommends without operationalizing is weaker.
- PASS = the argument is valid and its premises hold. The counterargument defense
  is Stage 4.

**Resource / dataset / foundation.** The "method" is the *construction*.
- Is the construction methodology principled and reproducible?
- Are the key design decisions (what's included/excluded, how labeled, how
  split) justified against the artifact's stated purpose?
- PASS = the construction is principled and documented. Coverage/leakage/quality
  controls are Stage 4.

In every variant, the orphan-component test generalizes: an unused definition, an
inferential step that supports nothing, a concern that doesn't bear on the thesis,
or a dataset field with no purpose is the same smell as orphan machinery — flag it.
