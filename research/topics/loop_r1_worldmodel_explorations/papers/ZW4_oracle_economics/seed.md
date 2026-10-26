# ZW4 — The Oracle Economics of Code RL: A Cost-Normalized Phase Diagram of Execution versus Proof Supervision

> ## 📌 SUBMITTED-INPUT ARTIFACT — CONTAINS ONE UNCORRECTED FACTUAL ERROR
>
> This is the `idea_text` sent to the AutoDiscussion room, preserved verbatim for provenance.
> **It attributes a GPU-hours figure to Re:Form that Re:Form does not report** — the one third-party
> attribution error left anywhere in this family, surviving here behind an unresolved `[VERIFY]`
> marker while being corrected everywhere else. Both `[VERIFY]` markers are now resolved inline.
> The scope is also superseded: the axes below describe the saturated factorial that the manuscript
> demotes to an aspirational Phase 3. *(sixth review pass, 2026-08-23)*


Room: `2a72d422-03b2-4a39-bf1a-8b65aa8b47af` · submitted 2026-08-21
Sources: `hyp2/idea4.md` §Compute and solver budget, `hyp1/idea.md` §compute matching, `hyp3/idea2.md` §12 Efficiency

## The unaudited claim

The efficiency argument for proof supervision is always some version of *"a proof covers all
executions, so we need fewer rollouts."* Fewer program executions is not the same as cheaper. SMT
cost has a **heavy tail**, and honest accounting charges GPU time, solver CPU time, execution time,
verifier calls, test-harness calls and wall-clock against the same budget line.

**The product of this paper is a phase diagram, not a winner:** for which program families,
specification qualities and budget regimes does each oracle — test outcome, execution process, binary
proof, structured proof, hybrid — deliver the most capability per unit cost.

## Method

1. **Instrument every oracle call** in a shared code-RL harness. Record the full per-obligation
   solver latency *distribution*, not its mean.
2. **Fixed per-obligation resource/time limits**, and report the **complete timeout distribution**.
   Never silently raise solver effort until an arm looks better — given how verifier budgets are
   reported today, this alone is a methodological contribution.
3. **Report every capability result twice**: under equal *model-compute* budget and under equal
   *end-to-end cost* budget. These orderings can disagree, and that disagreement is the result.
4. **Leave prices as free variables:** `C = H_gpu·p_gpu + H_cpu·p_cpu`, with a dated price-sheet
   appendix. The scientific claim is the **ordering and its robustness to price perturbation** —
   does it survive a 3× shift in the GPU:CPU price ratio? — not a dollar figure that expires.

## Axes of the diagram

- **Program family:** straight-line · linear loops · polynomial/nonlinear arithmetic · arrays and
  aliasing · recursion.
- **Specification quality:** human-authored fixed vs model-generated (ties directly to ZW2's δ).
- **Budget scale:** smoke ~50k · standard ~200k · high ~500k candidate generations per arm.

> **SCOPE SUPERSEDED 2026-08-23 (6th pass).** Crossed in full, these axes are the saturated design —
> 5 oracles × 5 program families × 2 specification sources × 3 budgets, i.e. the "≥120 cells at
> 20,000 paired outcomes per cell and oracle" the draft first specified and which is on the order of
> several hundred training runs. `paper-draft.revised.md`:156–162 demotes that to **Phase 3
> (aspirational, not claimed as executable)**. The delivered study is staged: **Phase 1** validates
> the ledger and envelope machinery with no new training runs, a **gate** requires per-call
> attribution accuracy plus a censoring-aware latency model that beats mean-latency, and **Phase 2**
> draws the phase diagram over *only the cells the companion experiments actually run* — crossovers
> reported as intervals between adjacent observed budgets, unmeasured cells reported as unobserved,
> never interpolated. This restores the seed's own "Relationship to the family" framing below, which
> the first draft had lost.

**Predicted structure, to be confirmed or refuted:** execution supervision dominates at small budgets
and on programs whose semantics are cheap to sample; proof supervision dominates where the
specification is trustworthy and the input space is large enough that sampled tests are weak
evidence; the crossover moves with nonlinear arithmetic, where solver timeouts inflate the proof
arm's cost tail.

## Planning anchors — and their status

These are **first-order planning estimates derived from one paper, not measurements**, and replacing
them with measured distributions is the paper's first deliverable:

- ~~Re:Form's **reported** ~176 GPU-h (0.5B) and ~400 GPU-h (1.5B) verifier-RL runs.~~ **[VERIFY]**
  → **⚠️ RESOLVED, AND THE CLAIM WAS WRONG (2026-08-23, 6th pass).** Re:Form (arXiv:2507.16331,
  TMLR 05/2026) **reports no GPU-hours figure anywhere.** Its Table 2 gives GPU count and wall-clock
  in *separate columns* for the *subset-reward* configuration on A800-SXM4-80G — 0.5B: 16 GPUs ×
  ~11 h; 1.5B: 16 × ~25 h. The ~176/~400 numbers are **our arithmetic on those columns**, and the
  40-epoch detail attaches **only to the 3B run**. Writing "Re:Form's reported" inverts the very
  point this paper makes — that the field's most-cited compute anchor does not report the quantity
  it is used for. `paper-draft.revised.md`:14 and :345 carry the corrected form; ZW1's seed carried
  it from 2026-08-21. Cite as derived, never as reported.
- A 200k-candidate structured-VC arm with five instrumented obligation categories ≈ **1M SMT/assertion
  batch evaluations** — which at 0.2 s mean batch time is ~56 CPU-hours, but at 2.0 s is ~556.
  That 10× swing on a plausible latency range *is* the reason this paper is needed.
- Dafny's own documentation warns that individual assertions can become unexpectedly hard, time out,
  or vary widely in solver cost — hence per-batch logging and hard resource limits. ~~**[VERIFY]**~~
  → **RESOLVED 2026-08-23 (6th pass): confirmed, and stated as fact in `paper-draft.revised.md`:14.**

## Novelty ledger

No surveyed work through 2026-08-21 reports code-RL results under equal end-to-end cost with solver
CPU charged in. Re:Form reports GPU hours but not a cost-normalized comparison against an execution
oracle; ExecVerify and RLEF report capability gains without solver accounting because they have no
solver; FLOPs-matched test-time-compute studies routinely assume the verifier is free. The gap is a
*measurement discipline*, and it is cheap to claim because it is layered instrumentation rather than
a new training method.

> ### 🔎 2026-08-23 pre-push scoop re-sweep (8th pass) — verdict CLEAR, three neighbors to add
>
> Fresh web audit before repository publication. The core claim — cost-normalized multi-oracle
> comparison with solver CPU charged into an end-to-end budget — is still unoccupied. Three
> neighbors were absent from this ledger and must be cited and distinguished:
>
> - **Pareto Optimal Code Generation** (Orlanski & Roberts, arXiv:2506.10056, 2025-06-11): maps an
>   accuracy-vs-throughput frontier for code *verifiers* — the closest published "verification has a
>   compute price and the choice is a frontier" statement. **Test-time generate-then-rank, not RL
>   training**; no proof oracles, no solver CPU, no price model, no family/spec-quality axes. Cite
>   as the test-time analogue of this paper's training-time question.
> - **Quantifying Empirical Compute-Supervision Tradeoffs in RLVR** (arXiv:2605.25252, 2026-05-24):
>   varies verifier *quality* (injected noise) vs rollout compute on GSM8K, verifier priced at zero —
>   i.e. it does exactly what this ledger says the field does. Cite as motivating evidence, not
>   competitor.
> - **JURY-RL** (arXiv:2604.25419, 2026-04-28): reports per-training-step wall-clock of its Lean
>   verifier with cache amortization inside an RLVR paper. One-off wall-clock table, single oracle,
>   no capability-per-cost normalization, no latency distributions, no price parameterization —
>   confirms the gap but kills any "nobody even measures verifier wall-clock inside RL training"
>   phrasing. **Soften to: "no systematic, cost-normalized capability comparison across oracle
>   types."**
>
> Cosmetic: Re:Form v4's arXiv title is now "…Reducing Human **Priors**…" (earlier versions said
> "Annotations") — sync at camera-ready.

## Falsification

- No crossover exists — one oracle dominates everywhere at every budget → the phase diagram collapses
  to a single recommendation, which is still a usable result.
- The ordering is unstable to price perturbation → the honest report is that **oracle choice is a
  cost accident, not a scientific decision**, and every efficiency claim in the proof-supervision
  literature (including ZW1's) must be restated as price-conditional.

## Relationship to the family

Runs as measurement-only instrumentation layered on ZW1's and ZW2's training runs. It is the paper
that keeps the rest of the program from over-claiming efficiency.
