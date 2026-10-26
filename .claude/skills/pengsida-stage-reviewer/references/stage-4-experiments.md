# Stage 4 Reviewer — Experiments / Ablations (and its archetype variants)

> **Read the archetype line from the manager first.** The default below is the
> method/exploratory bar. For theory, finding, position, or resource papers, jump
> to "Archetype variants" at the end. `archetypes.md` has the full table.
>
> **The one question this stage asks, in every archetype:** *is the claimed cause
> isolated from its strongest alternative explanation?* Method isolates by
> ablation; theory by discharging theorem hypotheses; finding by falsification;
> position by counterargument rebuttal; resource by leakage/quality control. Name
> the alternative explicitly, then check whether the paper rules it out.

You are reviewing whether the evidence *actually supports the claims*, and — for
exploratory work — whether experiments follow minimum viability. Source: Prof.
Peng Sida's "探索性实验应遵循最小可行性" and the claim→evidence discipline.

## The bar this stage must clear

Two different bars depending on what's in hand:

- **Exploratory experiment (early):** Does it follow *minimum viability* — the
  smallest experiment that cleanly answers one binary feasibility question with an
  explicit, pre-stated success criterion?
- **Confirmatory experiments (paper-stage):** Does every claim in the Method map
  to a result that supports it, with the right baselines and ablations to rule out
  alternative explanations?

## Minimum-viability checklist (for exploratory experiments)

1. **Binary success criterion, set in advance.** Is "what would count as success?"
   stated as yes/no and measurable *before* running? Fuzzy criteria are the #1
   minimum-viability failure ("不确定/数据模糊" means the design was
   under-specified).
2. **Stripped to the core.** Has every non-essential factor been removed so the
   experiment tests *only* the core hypothesis? "If I had one day, what's the
   simplest test?" Over-built early experiments waste the resource they're meant
   to save.
3. **Decision-ready.** Does the result lead to one of three clean actions —
   succeed (scale it up), fail (pivot, and that's a *win* because it was cheap), or
   ambiguous (redesign the test)? An experiment that can't trigger a decision
   isn't minimum-viable.

## Confirmatory checklist (for paper-stage experiments — quote the draft)

1. **Claim coverage.** Does *every* claim made in Method have a result behind it?
   List any claim with no supporting experiment — those are the dangerous ones.
2. **Right baselines.** Are the compared methods the ones a reviewer expects,
   including the nearest competitor from Stage 2? A missing obvious baseline reads
   as evasion.
3. **Ablations isolate the contribution.** Does an ablation turn off *each* claimed
   mechanism, so the improvement is attributed to the right cause and not to
   confounds? Three new pieces and one aggregate number proves nothing about which
   piece matters.
4. **Failure-case evidence.** Are the cases the Method said it fixes actually shown
   fixed (ideally the same figure the Method pointed at)?
5. **Honest reporting.** Are losses, settings, and negative results reported, or
   only the flattering cut? Cherry-picked tables get caught.
6. **The result answers the question.** Does the headline number speak to the
   Stage-1 problem, or to a proxy that's easier to win?

## Failure modes to call out by name

- **Fuzzy criterion.** No pre-stated yes/no bar; the experiment can't decide.
- **Over-engineered probe.** A heavy system built before the idea was validated
  cheaply.
- **Uncovered claim.** Method asserts a mechanism; no experiment touches it.
- **Aggregate-only.** One combined improvement, no per-component ablation →
  causation unproven.
- **Missing the obvious baseline / nearest competitor.**
- **Proxy win.** Beats a metric that isn't the motivated problem.

## Verdict format

```
STAGE 4 VERDICT: PASS | REVISE | STOP
WHY (1–2 sentences, quoting the draft):
THE ONE FIX (most important):
[prioritized secondary fixes — especially: each uncovered claim, each missing
ablation, and (exploratory) whether the success criterion is binary and
pre-stated]
```

- **STOP** = (exploratory) the experiment can't make a decision and needs
  redesign; or (paper-stage) the central claim has no evidence and the result
  doesn't survive an obvious confound.
- **REVISE** = the spine is there but an ablation, baseline, or claim-link is
  missing.
- **PASS** = every Method claim is evidenced, confounds are ablated away, and the
  result speaks to the real problem. The paper is ready for the writing stage.

---

## Archetype variants (apply instead of the method bar above when relevant)

Each variant is the *same* question — is the claimed cause isolated from its
strongest alternative — instantiated for a different kind of evidence.

**Theory / method-with-proof** (e.g. SEDD). Evidence = proofs + corroboration.
- **Hypotheses discharged.** For each theorem the contribution leans on, are its
  stated assumptions actually satisfied in the setting where it's applied? An
  unstated gap between "the theorem assumes X" and "the experiments violate X" is
  the theory analogue of an uncovered claim.
- **Empirical corroboration.** Do the experiments test a *consequence* the theory
  predicts (not just "the method scores well")? SEDD's score-entropy theory
  predicts better likelihood/perplexity and annealing-free generation — and those
  are exactly what's measured. Check the experiments target a theory-implied
  prediction.
- **The alternative to rule out:** "the gain comes from engineering, not the
  theorem." An ablation isolating the theoretically-motivated component (the new
  loss) from architecture/scale is what rules it out.
- STOP = the headline theorem's hypotheses are violated in practice and nothing
  bridges the gap.

**Analysis / finding** (e.g. diffusion-generalization). Evidence = falsification.
- **Is the finding falsification-tested, not merely correlated?** The strongest
  finding papers construct a case where, *if the claim were false*, the result
  would differ. The exemplar trains on classes where the claimed basis (GAHB) is
  *suboptimal* and shows the bias persists — that's a falsification design, not a
  correlation. Demand at least one such test.
- **The alternative to rule out:** "the characterization just reflects the data,
  not an inductive bias." The adversarial-construction test rules it out.
- PASS = the finding survives a genuine attempt to break it.

**Position / critique** (e.g. DP and diversity papers). Evidence = argument
survives its strongest counterargument, and recommendations are actionable.
- **Counterargument rebuttal is mandatory and is the core of this stage.** Does
  the paper state the *strongest* objection to its thesis and answer it? The DP
  paper pre-empts "but the data is public" (distinguishing available from
  consented-for-use) and "this is just a public-education problem" (showing a
  technical residue remains). A position paper that only argues *for* itself and
  never confronts the best case *against* fails Stage 4 outright.
- **Are the concerns load-bearing?** Each numbered concern must actually support
  the thesis, not be an associated grievance.
- **Constructive positions** (diversity paper): is the recommendation
  *operationalized and demonstrated*? The diversity paper validates measurement
  theory on a real case study (Segment Anything). A recommendation with no worked
  application is a weaker pass.
- **The alternative to rule out:** the steelman of the opposing position.
- STOP = the thesis collapses under an obvious counterargument the paper never
  addresses.

**Resource / dataset / foundation.** Evidence = the artifact is sound and
characterized.
- **Coverage and quality controls.** Is what the dataset claims to cover actually
  covered, and are quality/label-noise controls reported?
- **Leakage / contamination.** For benchmarks, is train/test (or
  pretraining/eval) contamination checked and ruled out? This is the resource
  analogue of confound isolation.
- **Honest baseline characterization**, not SOTA-chasing: do baseline numbers
  show the artifact is *useful and hard*, rather than that the authors' own model
  wins?
- STOP = undisclosed leakage, or coverage that doesn't match the stated purpose.

In all variants the secondary checks from the method bar still apply where
meaningful: honest reporting (no cherry-picking), and "does the headline result
speak to the Stage-1 problem rather than an easier proxy?"
