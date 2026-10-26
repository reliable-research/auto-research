# ZW3 — AutoDiscussion draft review

> ## 📖 DATED REVIEW RECORD — accurate, one detail incomplete
>
> Written 2026-08-21. No conclusion in it was later reversed. Its Major-1 replacement design was
> extended in review round 3 with a redistribution rule the text below does not mention — marked
> inline. *(sixth review pass, 2026-08-23)*


Room `9f4da36d-840e-4a7d-8c60-860b6c8581e6` (twin; original `e6e06795` stalled 15 rounds on
`motivation`) · closed 6/6, **4/6 clean, 2 unresolved majors** · reviewed 2026-08-21
Artifacts: `completed_jobs_dirs/ZW3 Which Prover Teaches Software…--9f4da36d/` — `research-report.md`
(754 L), `paper-draft.md` (324 L), `experiment-spec.md` (158 L)
Pipeline retitle: **"Budget-Matched Formal Supervision: Comparing Lean Proofs and Dafny Verification
for Software Transfer."**

**Verdict: adopt with fixes — and this is the strongest of the four drafts.** Both majors are fixed
in `paper-draft.revised.md`; the diagnosis is in `major_fixes.md` and the change list in that file's
revision log. Alone among the four packages it shows **no scope inflation**.

## What the pipeline got right

- **The verified reframing survived intact.** FVEL is reported as "modest improvements on an SV-COMP
  subset, substantially weaker performance than a specialized verifier, and no gain on Code2Inv";
  the self-play result as "gains concentrated in one semantic-equivalence setting alongside
  regressions in others." These are the corrected readings, not the briefs' inflated ones — the
  reframing after verification propagated correctly through the seed into the draft.
- **No AlphaProof misattribution.** The draft credits it with theorem-proving capability and says it
  "supplies no direct evidence of transfer to software tasks." The 28/42 trap did not fire.
- **The positive-control gate survived and was strengthened into a blinding protocol**: *"Before
  software outcomes are opened, the Lean arm must pass a preregistered formal-mathematics
  positive-control gate; otherwise, confirmatory analysis will stop and the transfer matrix will
  remain diagnostic."* Stronger than the seed, which only required declaring the gate in advance.
- **Four-axis matching became a common feasible intersection** — cap every arm at the largest budget
  simultaneously feasible across tokens, updates, sampled candidates and accepted trajectories. A
  better construction than the seed's "report all four normalizations," because it removes the
  mismatch rather than displaying it.
- **Curriculum order separated from composition** through equal source quotas across Lean→Dafny,
  Dafny→Lean and interleaved arms — a control the seed did not specify.
- **Paired win-minus-loss effects** avoid assuming commensurate units across heterogeneous benchmarks
  while preserving family-level negative transfer.

## Major 1 — RQ2's transport step was vacuous (fixed)

The most substantive criticism the critic produced anywhere in this batch, and it is correct. RQ2
proposed stabilized inverse-replay weights transported to the evaluation estimand by "reweighting
each arm's accepted-trajectory training distribution," via a Hájek estimator. The weights index
training examples; the estimand is a mean over held-out prompts of a **frozen** checkpoint. No
channel connects them, so weighted and unweighted estimates coincide identically — and the stated
success criterion (every contrast within ±0.05) **could not fail**. A null manufactured by the
estimator's algebra would have been reported as replay robustness.

Replaced with a training-time intervention: **natural** versus **flattened** replay regimes per arm
(per-example multiplicity capped at the arm's median), both held to the same four-axis budget
intersection so exposure distribution changes while exposure total does not.

> **EXTENDED in review round 3 — the cap alone is not enough.** Capping multiplicity *reduces total
> exposure* unless the freed replay slots are put back, which would silently reintroduce the budget
> confound the four-axis intersection exists to remove. `experiment-spec.md`:43 now specifies the
> **deterministic redistribution rule**: round-robin over trajectories strictly below the cap in
> canonical order (ascending current multiplicity, ties by trajectory id), repeating until all freed
> slots are placed; residual placed by continuing the same round-robin at cap+1, with the residual
> count reported. Performance-independent and seed-deterministic, and the ledger asserts exposure
> totals identical to `natural` **before** training starts. The contrast becomes a
real difference between checkpoints and **can fail**. Doubling training cost is the price; if
unaffordable, drop RQ2 and report realized multiplicity as an unaddressed threat — retaining a test
that cannot fail is not an option.

## Major 2 — circular limitations (fixed)

Fourth room in a row on this defect. All eight limitations restated the study's own question.
Replaced with independently standing, primary-verified gaps — Re:Form's OOD measured *inside* formal
verification (14.0% vs 8.3%); FVEL's authors crediting seL4 corpus correlation for a 6.9%→8.1% subset
effect with Code2Inv at 46→46; Proof2Silicon training a prompt policy over a frozen model; AlphaVerus
obtaining verified code without fine-tuning; AlphaProof's 28/42 belonging to the combined system;
DeepSeek-Prover-V1.5 never evaluating code, with search-heavy headline numbers; Dong et al.'s OOD
being *within* theorem proving; Leang et al. transferring to *informal arithmetic*. Re:Form and
DeepSeek-Prover-V1.5 are now marked arm-supplying, resolving the accompanying minor.

## Citation audit

**Zero confabulated statistics, zero off-topic works** — the seeded reference payload held, as it did
for ZW4. Remaining defect is presentational: related-work prose uses inline author-title references
rather than linked citations with venues, and the "This section requires manual completion with
proper citations" placeholder was present (now removed). Venue corrections for bib time are listed in
the revision log.
