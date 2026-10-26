# ZW4 — AutoDiscussion draft review

> ## 📖 DATED REVIEW RECORD — its Fix-3 arm mapping is wrong
>
> Written 2026-08-21. Fixes 1 and 2 were applied and hold. **Fix 3 assigns Re:Form to both the
> binary- and structured-proof arms; that conflation was corrected in review round 1** and is marked
> inline. *(sixth review pass, 2026-08-23)*


Room `7bcfe3ef-ae2b-4f78-9bda-dc939d0c4838` (twin; original `2a72d422` died in a retry loop) · closed
6/6, **5/6 clean**, 1 unresolved major (related_work) · reviewed 2026-08-21
Artifacts: `completed_jobs_dirs/ZW4 The Oracle Economics…--7bcfe3ef/` — `research-report.md` (796 L),
`paper-draft.md` (282 L), `experiment-spec.md` (158 L)
Retitled by the pipeline: **"Cost-Aware Phase Diagrams for Proof and Execution Oracles in Code
Reinforcement Learning."**

**Verdict: adopt with one structural fix.** The measurement design is better than the seed's. The
scope is roughly 100× the seed's and must be cut back before this is runnable.

## The reference payload worked — this is the headline process result

ZW2 (submitted with **no** `references`) pulled a particle-physics paper and a physical-chemistry
paper into its related-work corpus. ZW4 was the first completed room submitted **with** the 22
verified citations, and its corpus is **100% seeded references, zero off-topic contamination**.
Re:Form carries the corrected title; AlphaProof is cited as *Nature* 651(8106):607–613 with the note
that no arXiv version exists. Seeding references fixes the retrieval-contamination bug outright.

One residual defect: Proof2Silicon is credited to **"(unknown authors)"** despite the seeded entry
naming Jha, Wan & Chen — the pipeline drops author lists on some entries. Same class of bug as ZW2's
"(unknown authors)" for Gao/Schulman/Hilton.

## Where the draft beats the seed

1. **Censoring is handled properly.** Timeouts are retained as **right-censored** observations with a
   Kaplan–Meier estimator restricted to the pre-cap region and *never imputed*. The seed only said
   "report the complete timeout distribution"; this is the statistically correct version of that.
2. **Specification quality becomes an observed property, not a label.** The seed used
   human-authored-vs-model-generated as a proxy. The draft calibrates quality tiers before training
   against two independent criteria — defect-detection on held-out semantic mutants, plus blind
   expert ratings — so "quality" is measured rather than assumed from provenance.
3. **Three well-chosen measurement baselines**: source-only quality labels, naive job-wall-time
   accounting, and a mean-latency stall model. For a measurement paper these are exactly right — each
   is a way the field currently gets this wrong, and each is falsifiable.
4. **The event-sourced ledger** records process-tree CPU, reserved GPU, wall latency, obligation
   identity, retries, caching, parallelism, termination cause and timeout cap **per call** — enough to
   separate consumed resources from wall-clock stalls, which the seed hand-waved.
5. **Cross-fitted attainable-capability envelopes** with ties preserved as sets, and unsupported
   crossovers reported as **intervals between adjacent observed budgets** rather than interpolated.
   That is the honest treatment of a discrete budget grid.

## Fix 1 (mandatory) — scope inflation, the known fleet failure mode

The draft specifies **"at least 120 cells and 20,000 paired held-out task-seed outcomes per cell and
oracle."** With five oracles that is ~600 training runs, at candidate budgets of 50k/200k/500k per
arm. This is not fundable and not runnable.

The seed's framing was explicitly the opposite:

> "This runs as measurement-only instrumentation layered on the training runs of the companion
> experiments, and it is the paper that keeps the surrounding program from over-claiming efficiency."

**That framing is gone from the draft.** ZW4's entire value proposition was that it is *cheap* —
instrumentation over ZW1's and ZW2's runs, not a standalone factorial. Restore it: the primary
deliverable is the ledger + envelope machinery validated on the companion experiments' arms, with the
full factorial as a clearly-labelled aspiration.

**Partial mitigation already in the spec, and it is a good instinct:** *"No real data/model ships:
implement synthetic task/spec generators and mock oracle latencies so the pipeline and all six reports
are executable end-to-end; swap in real components later."* So the buildable artifact is a harness
validated on synthetic latencies. Keep that, and make it the paper's stated Phase 1 rather than a
footnote in Open Decisions.

## Fix 2 — the planning anchors that justified the paper are missing

The seed's core motivating arithmetic barely survives. Nearly absent from both draft and spec:

- Re:Form's Table 2 breakdown (0.5B: 16 A800-SXM4-80G GPUs × 11 h; 1.5B: 16 × 25 h), and the
  correction that **the paper reports no GPU-hours figure at all** — 176/400 is our arithmetic, and
  the 40-epoch detail attaches only to the 3B run.
- The **10× swing**: a 200k-candidate structured-VC arm with five instrumented obligation categories
  is ~1M SMT batch evaluations, which is ~56 CPU-hours at 0.2 s mean batch time but **~556 at 2.0 s**.

That swing *is* the argument for the paper. Without it the introduction asserts that solver cost has
a heavy tail rather than showing why the uncertainty is decision-relevant. Reinstate both, with the
"our arithmetic" caveat intact.

## Fix 3 — the residual major (related_work), quoted

> "All eight works are marked `is_potential_baseline=false` and the artifact claims 0 candidate
> baselines, but a measurement study still needs concrete training pipelines to instantiate its oracle
> arms; Re:Form's verifier-guided GRPO (proof oracle), ExecVerify's trace rewards (execution oracle),
> and Tan's Dafny RLVR setup are exactly the kinds of arms the harness must run."

The critic is right and names the fix. ~~Re:Form **is** the binary/structured-proof arm's recipe,~~
ExecVerify **is** the execution-process arm's, Tan's setup **is** a second proof-arm instantiation.
Mark them as arm-supplying baselines.

> **⚠️ CORRECTED in review round 1 — Re:Form does not supply the structured-proof arm.** Its
> "subset reward" is easily mistaken for structured supervision but is a verifier-acceptance reward;
> making it the recipe for both proof arms would collapse the very contrast the phase diagram
> measures. The delivered mapping (`paper-draft.revised.md`:285–291) is: **test outcome** → CodeRL ·
> **execution process** → ExecVerify, with StepCodeReasoner as an independent second instantiation ·
> **binary proof** → Re:Form *and* Tan · **structured proof** → RLFR as the scalar
> proof-obligation precursor, plus the typed verification-condition implementation from the
> companion study (ZW1) · **hybrid** → explicitly study-defined, no external recipe. See the family README — this is the third room in a row to take
a major on `related_work` for the same underlying defect.

The accompanying minor is also worth taking: every limitation is a near-identical restatement of
"they never measure oracle latency/timeouts/GPU-CPU cost," repeated eight times. Each entry should
instead name which oracle type in our taxonomy the work instantiates and which paper-specific
efficiency claim we would test — e.g. Re:Form's scalability framing, RLEF's "order of magnitude fewer
samples" claim, LORIS's token-cost reporting.

## Citation audit

**Zero confabulated statistics and zero off-topic works.** All 22 retrieved citations trace to the
seeded set. The formatting defect from ZW2 persists in the draft's prose — citations render inline as
`Hung Le et al.. CodeRL: …` with doubled periods and no venue, year, or identifier — while the
research report carries cleaner entries. Needs a bib pass, same as ZW2.

Cross-check against the verified record before drafting: RLEF is **ICML 2025, PMLR
267:19034–19055** (cite the 6-author camera-ready list, not arXiv v2's 7), ORPS must appear under its
**ICML title** *"Reasoning Through Execution…"*, μCODE is **ICML 2025 Spotlight**, and CodeRL is
**NeurIPS 2022** on a CodeT5 backbone — worth noting since GraphAlignCoder's use of "the reported
CodeRL baseline" on BigCodeBench cannot be the original model.
