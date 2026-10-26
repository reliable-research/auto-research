# deerflow_review — ZW1_proofworld

- **Skills used**: `.claude/skills/academic-paper-review/SKILL.md` (review procedure + output template) and `.claude/skills/deep-research/SKILL.md` (literature-context web methodology) — the two deer-flow review skills.
- **Review date**: 2026-08-23
- **Reviewer**: deer-flow academic-paper-review skill (Claude agent)
- **Artifacts reviewed**: `paper-draft.revised.md` (current manuscript, read in full including revision log) and `experiment-spec.md` (current spec, read in full). No other package files consulted; no existing file edited.
- **Adaptation note**: this is a pre-registration-style draft with no collected results. The "Statistical Rigor" row assesses the *planned* analysis; "Reproducibility" is rated on the completeness of the experiment spec.

## Search log

Every web query issued during the literature-context phase (deep-research skill), with hit/empty status:

| # | Query | Angle | Status |
|---|-------|-------|--------|
| 1 | `reinforcement learning formal verification reward code generation state of the art 2026` | state of the art 2026 | HIT (LLM-VeriOpt CGO 2026; RLFR/Haladir; arXiv 2605.30914; RLVR surveys) |
| 2 | `Dafny reinforcement learning LLM verifier reward Re:Form` | direct competitor / anchor | HIT (Re:Form arXiv 2507.16331, TMLR 05/2026; DafnyPro; PREFACE GLSVLSI 2025) |
| 3 | `typed proof obligation verdict fine-grained verifier feedback reward RL code model` | method-twin mechanism nouns | HIT (Process-Verified RL via Lean arXiv 2606.20068; Proof-Verifier OpenReview; verifier-engineering survey) |
| 4 | `verified code generation benchmark hidden tests pass@1 Dafny specification hacking evaluation` | benchmark / estimand | HIT (VERINA 2505.23135; CLEVER 2505.13938; DafnyBench; AxDafny 2606.32007; VeriScale) |
| 5 | `reward hacking weakened specification formal verifier RL limitations criticism` | limitations / criticism | HIT (RLVR reward-hacking literature; noisy-verifier RL 2510.00915; verifier-fuzzing 2606.01066) |
| 6 | `verifier reward reinforcement learning code August 2026` | recent-work August 2026 | HIT (awesome-RLVR list with ICLR/ICML 2026 additions; imperfect-verifier papers) |
| 7 | `dense execution state reward stepwise execution trace reinforcement learning code LLM 2026` | primary-baseline family (A2 twin) | HIT (StepCodeReasoner 2605.11922; ExecVerify 2603.11226; CodeRL+; StepCoder/PSGPO) |
| 8 | `RLFR Haladir "verified goals" Dafny formally-defined rewards` | GR-arm anchor verification | HIT (Haladir RLFR page indexed; YC W26; LinkedIn announcement) |

No query returned empty. WebFetch was used on the 3 most relevant hits:

- `https://www.haladir.com/research/rlfr` — the URL now serves unrelated logistics-AI content with **no RLFR material**, consistent with the manuscript's claim that the RLFR report was removed from the live web and survives only as a web-archive capture (the search index still shows the old title).
- `https://arxiv.org/abs/2507.16331` (Re:Form) — confirmed TMLR 05/2026, verifier-feedback RL on Dafny, DafnyComp benchmark; abstract does not describe typed-obligation rewards or matched execution-reward baselines.
- `https://arxiv.org/abs/2606.20068` (Process-Verified RL via Lean) — tactic-level dense verifier feedback with first-error credit assignment, Lean theorem proving; compares against outcome-only baselines but not against matched execution supervision, and not in a code-generation/tool-off setting.

**arXiv verification**: all ids cited in this review were verified in ONE batched request (`id_list=2507.16331,2606.20068,2605.30914,2505.23135,2505.13938,2603.11226,2605.11922,2608.11394`); all 8 resolved with matching titles. No citation debt.

---

# Paper Review: Typed Verifier Verdicts for Matched Reinforcement Learning of Tool-Free Dafny Programs

## Paper Metadata
- **Authors**: Not stated in manuscript (AutoDiscussion pipeline output, room `29167d1d`; ZW1 package of the loop_r1 portfolio)
- **Venue**: None (pre-registration-style draft; no target venue named)
- **Year**: 2026 (draft dated by revision log, 2026-08-21 through 2026-08-23)
- **Domain**: Machine learning for code generation; RL with verifiable rewards; formal verification (Dafny)
- **Paper Type**: Empirical study design / pre-registered experimental protocol (no collected results)

## Executive Summary

The paper proposes a pre-registered, seed-blocked, four-arm randomized "policy fork" experiment to answer a genuinely well-isolated causal question: does retaining *typed* proof-obligation identities (initialization / preservation / postcondition / safety / termination) and *distinct solver verdicts* (proved / refuted / unknown / timeout / invalid) in an RL reward improve tool-off (no verifier at inference) hidden-test correctness of Dafny code models, beyond (a) an equally dense execution-state reward, (b) a binary verifier reward, and (c) an RLFR-style verified-goals ratio? All four rewards are constructed from synchronized dual-oracle observations of the same candidates, with the simpler rewards obtained by deterministic coarsening, frozen calibration to unit RMS, and per-candidate matched snapshot boundaries — a design that squarely targets the confound (reward density vs. reward semantics) that the existing literature leaves open. The evaluation plan is unusually defensive: sealed hidden tests disjoint from reward-visible tests, semantics-preserving perturbations, weakened-specification stress tasks, an AST comparator for specification hacking, a reward-pipeline audit (RQ3) with a usable-packet feasibility gate, and a non-circular predictive probe (RQ4).

The manuscript's strongest qualities are the cleanliness of the estimand, the mechanism-level care in the prefix-completion design (rejecting `assume false` stubs on vacuity grounds, per-obligation determinacy from dependency footprints), and an exemplary concede-and-claim treatment of the closest prior work — the unrefereed, now-delisted RLFR report — whose reward it adopts as the GR ablation arm rather than claiming the graded proof reward as novel. Its main shortfalls are feasibility-side: the "equally dense" execution baseline (A2) — the arm the headline contrast depends on — is left materially under-specified with no A2-side density gate symmetric to RQ3c; the statistical plan rests a two-way cluster bootstrap on only 8 checkpoint clusters with no power analysis for the 0.02 pass@1 threshold; and the data/compute requirements (≥32 RL runs plus 8 scalarization variants; ~24,000+ curated Dafny tasks with hidden metamorphic tests and spec ASTs, all "supplied by the user") are far beyond any existing Dafny resource, with no construction pipeline in scope. As a study design, this is a strong, honest, and falsifiable protocol; as an executable plan, it is at real risk of being unrunnable at the stated scale. There are also residual internal inconsistencies from the fixed-K→variable-k_c revision (RQ4 still says "the 32 typed reward packets") and an unfinished Related Work apparatus.

## Summary of Contributions

1. A randomized, seed-blocked four-arm policy-fork design with dual-oracle scoring and exact budget matching to identify reward-*representation* effects despite on-policy divergence.
2. Synchronized typed obligation–verdict rewards plus deterministic binary and verified-goals-ratio coarsenings that hold reward timing, source events, and calibrated scale constant across arms.
3. A tool-off behavioral evaluation combining sealed hidden tests, semantics-preserving perturbations, controlled specification weakening, and post-hoc verifier/AST diagnostics to separate behavioral correctness from verifier acceptance.
4. An empirical protocol (six RQs with preregistered, checkable success criteria) for whether structured verifier feedback adds training and predictive value beyond dense execution supervision and scalar proof completion.

## Claims Ledger

```
Claim 1: No existing work isolates whether obligation typing + solver-verdict structure adds
         information beyond reward density, binary acceptance, or a verified-goals ratio under
         matched training conditions.
Evidence: Related-work survey (Intro ¶3–4; Related Work); corroborated by this review's
         literature phase — Re:Form (2507.16331), Tan (2605.30914), Process-Verified RL
         (2606.20068), ExecVerify (2603.11226), StepCodeReasoner (2605.11922) each occupy one
         side of the contrast; none runs the matched four-arm comparison.
Strength: Strong (as a gap claim; survives the search).

Claim 2: The seed-blocked four-arm fork with dual-oracle scoring identifies reward-representation
         effects despite post-initialization on-policy divergence.
Evidence: Design argument only (Methodology "Matched Causal Reward Comparison"); hierarchical
         model + two-way cluster bootstrap over task×checkpoint. No data.
Strength: Moderate (logic sound; inference validity depends on 8-cluster bootstrap, see W3).

Claim 3: Deterministic coarsenings from synchronized observations + frozen unit-RMS calibration
         hold reward timing and scale constant, leaving semantic resolution as the only
         cross-arm difference.
Evidence: Construction (M2) + planned RQ3 audit with equivalence bounds [0.95, 1.05].
Strength: Moderate (auditable by design, but A2's density matching is asserted, not
         constructed — see W1).

Claim 4: The prefix-completion procedure (no assumptions inserted; synthetic/indeterminate
         labels; per-obligation dependency-footprint determinacy; boundary snapshots) makes a
         dense proof signal feasible without vacuity contamination.
Evidence: Mechanism reasoning (Methodology "Typed-Verdict Reward Construction"; spec Open
         Decision 5) + the RQ3c usable-packet gate as an empirical check. No pilot data.
Strength: Weak-to-Moderate (thoughtful, but feasibility is explicitly unproven — the gate
         exists because the authors cannot yet show the signal is deliverable).

Claim 5: Tool-off evaluation with sealed tests, perturbations, weakened specs, and AST
         diagnostics separates behavioral correctness from verifier acceptance.
Evidence: Design (Tool-Off Behavioral Validation; spec M3; D1–D3 schemas).
Strength: Moderate (sound plan; hinges on user-supplied hidden tests being non-leaking
         and adequate).

Claim 6: Novelty is claimed only for typing + verdict structure + the matched execution
         baseline — not for graded per-obligation proof rewards or prover-free transfer,
         which are conceded to the RLFR report; GR is a formula-faithful ablation, not a
         reproduction.
Evidence: Dedicated anchor paragraph in Related Work; verified this review: the RLFR page
         is indeed no longer live (URL now serves unrelated content).
Strength: Strong (as a positioning claim; the concession is accurate and verifiable).
```

## Strengths

### S1: A cleanly isolated causal estimand that the literature verifiably leaves open
The primary estimand Δ_TV,EX (Formal Problem Definition) — typed-verdict minus dense execution-state pass@1 under shared checkpoints, data, budgets, optimizer, verifier, and harness — is precisely the contrast missing from the field. The review's literature phase confirms the paper's gap claim: Re:Form (arXiv 2507.16331, TMLR 05/2026) and Tan (arXiv 2605.30914) optimize aggregate verifier outcomes without matched execution baselines; Process-Verified RL via Lean (arXiv 2606.20068) shows tactic-level dense verifier feedback beats *outcome-only* baselines but in theorem proving, not tool-off code behavior, and never against execution supervision; ExecVerify (2603.11226) and StepCodeReasoner (2605.11922) sit on the execution side with no verifier arm. The deterministic-coarsening construction (M2) — binary and ratio rewards derived from the *same* synchronized snapshots as the typed reward — is an elegant way to make "reward density" and "reward timing" non-explanations by construction rather than by post-hoc argument.

### S2: Exemplary intellectual honesty in positioning against the RLFR precursor
The "scalar proof-obligation precursor" paragraph (Related Work) is a model of concede-and-claim: it concedes the graded per-obligation reward and prover-free transfer to an unrefereed industry report, adopts that reward verbatim as the GR arm, explicitly *withdraws* a previously claimed multi-turn distinction ("it was never instantiated here"), documents the source's evidential defects (no code/models, mismatched LiveCodeBench windows, now HTTP-404), and scopes GR as a "formula-faithful ablation under our harness" rather than a reproduction. This review independently confirmed the source's disappearance (the URL now serves unrelated content). Turning the strongest potential scoop into the mandatory ablation arm (RQ2) converts a novelty threat into the paper's sharpest experiment.

### S3: Mechanism-level care in the dense-signal construction, with a preregistered feasibility gate
The prefix-completion design (Methodology "Typed-Verdict Reward Construction"; spec Open Decision 5) shows real understanding of Dafny/Boogie failure modes: it rejects `assume false` stubs on vacuity grounds (correctly noting that tagging inserted scaffolding cannot undo contamination of *original* obligations), distinguishes `synthetic`/`indeterminate` from `unknown`/`timeout`, computes determinacy per-obligation from the VC's dependency footprint rather than whole-method completeness, and places snapshots at syntactic-completion boundaries rather than token offsets. Most importantly, RQ3c's usable-packet-rate gate preregisters the honest failure mode — "typed verdicts were never delivered" vs. "typed verdicts do not help" — so a feasibility failure is reported as such instead of masquerading as a null result. This is rare rigor for a dense-reward proposal.

### S4: Defensive evaluation architecture against verifier gaming
The two-disjoint-test-set rule with code-level assertions (spec M0), sealed tool-off evaluation, the weakened-specification divergence metric (RQ6), and the original-spec AST comparator directly address the specification-hacking failure mode that the 2025–2026 RLVR-criticism literature (e.g., imperfect-verifier and verifier-fuzzing work, arXiv 2510.00915, 2606.01066) and benchmarks like VERINA (2505.23135) identify as the central weakness of verifier-rewarded training. Few proposals in this space plan to *measure* verifier-pass/hidden-fail divergence rather than assume verifier acceptance implies correctness.

## Weaknesses

### W1: The primary baseline A2 ("equally dense execution-state") is under-constructed, and there is no A2-side density gate
The entire headline contrast (RQ1) is TV vs. EX, yet A2's channel set is deferred to Open Decision 4 of the spec ("e.g., per-snapshot deltas in {tests-passed, assertion-checks-passed, coverage-or-branch-signal, runtime-error-flags}") and the spec itself calls the matching "a key validity threat — audit it" without defining the audit. Worse, the usable-packet gate (RQ3c) is defined *only in verifier terms* ("≥1 obligation with a determinate verdict"): there is no symmetric definition of a *usable execution packet*. On completed prefixes with empty method bodies, execution channels like tests-passed will be degenerate (an empty body passes nothing) for most early snapshots — plausibly *more* degenerate than the proof channels, since invariant-initiation obligations become determinate before any test can pass. If A2's effective density is lower than A1's, a positive Δ_TV,EX is confounded by density after all, defeating the design's stated purpose. **Fix**: preregister A2's channel set concretely; define usable-execution-packet symmetrically; make RQ3c gate both arms and report the per-snapshot usable-rate *profiles* (not just medians) side by side.

### W2: Data and compute requirements are far beyond any existing resource, with construction out of scope
The plan requires ≈24,400+ curated single-function Dafny tasks across D1–D3 (6,000 sealed with property-based *and* metamorphic hidden tests, original-spec ASTs, and four stratification labels; 2,000+2,400 disjoint audit/probe pools; 6,000 base × 6 perturbation variants; 10,000 weakenable tasks), all listed under "Inputs You Must Provide." For calibration: DafnyBench is 782 programs; Re:Form's corpus is ~17k auto-translated programs *without* hidden metamorphic tests or spec ASTs; VERINA and CLEVER are in the hundreds. Nothing at the required size and annotation richness exists, and the spec provides loaders but no construction pipeline. On compute, the plan is 4 arms × 8 checkpoints = 32 RL runs, plus RQ6's "eight typed variants will be trained" (up to 64 more runs if crossed with checkpoints — the crossing is unstated), plus up-to-K_max=32 verifier calls per candidate where incremental verification is unavailable. No token, GPU-hour, or solver-hour budget is estimated anywhere. As written, the study's feasibility is speculative. **Fix**: add a dataset-construction section (or descope D1 to ~1–2k tasks with a pilot), state the RQ6 variant×checkpoint crossing explicitly, and provide a compute budget table with the solver-cost multiplier measured on the pilot.

### W3: The planned inference rests on 8 checkpoint clusters with no power analysis
All confirmatory contrasts use a two-way cluster bootstrap over {task, checkpoint} with only **8 checkpoint-level clusters** (Experimental Setup; spec RQ table). Cluster bootstrap is known to be unreliable at fewer than ~20–30 clusters in the clustering dimension that dominates the variance — and checkpoint-level variance plausibly dominates here, since each checkpoint contributes one policy per arm. No power analysis supports the 0.02 pass@1 threshold, no minimum detectable effect is computed, and the multiplicity stance (Open Decision 10: confirmatory RQ1/RQ2, no cross-RQ correction) is recorded but not justified. If between-checkpoint heterogeneity is large, the 95% intervals will be anticonservative and a "significant" Δ ≥ 0.02 uninterpretable. **Fix**: either increase seed blocks (e.g., 16–24) with a justification of what checkpoint count powers the 0.02 threshold at the observed heterogeneity from a pilot, or preregister a few-cluster-robust method (wild cluster bootstrap / t-approximation with Satterthwaite dof) and a formal power computation.

### W4: The treatment variable itself (obligation type × verdict) is measured by a fragile, unvalidated classifier
Dafny emits no first-class typed-obligation enum; the spec (Open Decision 3) infers types from error-message text, mapping *unmapped messages to SAFETY with a logged warning*, and distinguishes REFUTED_COUNTERMODEL from UNKNOWN by the heuristic presence of a partial Z3 model (Open Decision 7). This means the 25-channel representation — the experimental treatment — carries unquantified label noise, version-sensitive parsing (flag spellings themselves flagged as version-dependent in Open Decision 2), and a default-to-SAFETY bias that would systematically dilute exactly the type distinctions under study. If typing is noisy, a null Δ_TV,GR is ambiguous between "typing carries no information" and "typing was never measured." **Fix**: preregister a labeled-fixture validation with a minimum classifier accuracy/coverage threshold (analogous to the RQ3c gate), report the unmapped-message rate per corpus, and treat classifier accuracy as a reported precondition for interpreting RQ2/RQ4.

### W5: Residual internal inconsistencies and unfinished apparatus from the revision process
The round-9 fixed-K→variable-k_c repair is incomplete: RQ4 (Experiments) still reads "predict hidden correctness from either **the 32 typed reward packets** or the verified-goals ratio," contradicting the variable-k_c rule stated in Methodology, Experimental Setup, RQ3, and the spec's D2 schema (`typed_packets: float[k_c][25] … NOT float[32]`) — and a fixed-length probe input is not merely stylistic, since the RQ4 probe needs a defined featurization for variable-length packet sequences (padding? pooling? — currently unspecified *because* the text assumes 32). Related Work still contains the placeholder "> This section requires manual completion with proper citations."; every citation is name-year prose with no bibliography; and the section heading structure duplicates itself ("Problem Definition"/"Formal Problem Definition", "Method Overview" then "Methodology", "Experiments" then "Experimental Setup"). **Fix**: repair the RQ4 sentence and specify the variable-length featurization; complete the bib pass the revision log already flags; collapse the duplicate headings.

### W6: RQ5's directional hypothesis (typed ⇒ perturbation robustness) is under-motivated
RQ5 preregisters that typed-verdict training yields *higher* perturbed correctness than execution-state training, with a demanding compound criterion (retention ≥ 0.90 AND perturbed advantage ≥ 0.02, simultaneous bounds). No mechanism in the paper explains why obligation typing should confer robustness to identifier renaming or formatting changes — verifier obligations are computed on the candidate *program*, not the prompt surface, so the causal path from reward representation to prompt-surface invariance is left entirely implicit. A weakly motivated directional hypothesis with a strict compound bound is likely to fail without being informative. **Fix**: either articulate the mechanism (e.g., typed rewards discourage prompt-pattern shortcuts by rewarding semantics-anchored partial progress) or downgrade RQ5 to an exploratory, two-sided comparison.

## Methodology Assessment

| Criterion | Rating (1-5) | Assessment |
|-----------|:---:|------------|
| Soundness | 4 | The fork-and-coarsen design logic is correct and the vacuity analysis of `assume false` is exactly right; docked for the unconstructed A2 density matching (W1) and the noisy treatment measurement (W4), both of which threaten the causal interpretation the design exists to secure. |
| Novelty | 3 | The *question* (typed verdicts vs. matched dense execution and scalar ratio, tool-off endpoint) is verifiably unasked — closest twins (Process-Verified RL 2606.20068; RLFR) each lack the matched contrast. But the contribution is a protocol assembled from known components (GRPO-style forks, cluster bootstrap, coarsened rewards); no new algorithm, and the honest RLFR concession itself narrows the claimed delta to typing + verdict structure + baseline. |
| Reproducibility | 4 | Rated on spec completeness: unusually strong — frozen 25-channel schema, record schemas for D1–D3, per-RQ drivers, prereg.yaml with hashing, oracle-call ledger, explicit Open Decisions. Docked because the base model, optimizer hyperparameters, Dafny version, w*, and the 8 scalarizations are all deferred, and the datasets (the largest artifact) are entirely user-supplied with no construction recipe. |
| Experimental Design | 4 | Four matched arms, mandatory scalar-collapse ablation, sealed/disjoint test separation with code-level assertions, perturbation and weakened-spec stress suites, and the RQ3 pipeline audit form a strong design; docked for the asymmetric density gate (W1) and the unstated RQ6 variant×checkpoint crossing (W2). |
| Statistical Rigor | 3 | (Planned analysis.) Preregistered checkable criteria, two-way cluster bootstrap, simultaneous bounds within-RQ, and a non-circular probe (RQ4) are well above field norms for proposals; but 8 checkpoint clusters undermine bootstrap validity, there is no power analysis for the 0.02 threshold, and cross-RQ multiplicity is waved through (W3). |
| Scalability | 2 | ≥32 RL runs plus up to 8 trained scalarization variants, up to 32 verifier invocations per candidate (K× solver cost admitted to be "silent" without incremental verification), and ~24k richly annotated tasks — with no quantified compute/data budget anywhere. The oracle-call ledger and cost *reporting* commitments are good, but the study as specified is at the edge of, or beyond, plausible academic resources (W2). |

## Questions for the Authors

1. **A2 density**: What is the concrete, preregistered channel set for the dense execution-state arm, and what is the definition of a *usable execution packet* on a completed prefix whose method body is empty? If A2's usable-packet rate on the pilot split is materially below A1's, does the study report RQ1 as confounded-by-density, symmetric to the RQ3c feasibility negative?
2. **RQ6 crossing and budget**: Are the eight scalarization variants trained from all 8 checkpoints (64 runs) or a subset? What total sampled-token, GPU-hour, and solver-hour budget does the full study require, and is incremental verification actually available in the pinned Dafny version?
3. **Dataset provenance**: What is the source and construction procedure for 6,000 sealed single-function Dafny tasks with property-based *and* metamorphic hidden tests, original-spec ASTs, and verdict-mix stratification labels — none of which exists in DafnyBench, DafnyComp, VERINA, or the Re:Form corpus? Is stratification by `solver_verdict_mix` even computable pre-training without running the verifier on reference solutions (and if so, with which model's candidates)?
4. **Classifier validation**: What accuracy/coverage bar must the message-text obligation-type classifier meet on labeled fixtures before RQ2/RQ4 are interpretable, and how is the unmapped→SAFETY default's dilution of type distinctions bounded?
5. **RQ4 featurization**: Given variable-length k_c packet sequences, how exactly is the typed-packet probe's input defined (padding, pooling, summary statistics)? The current text ("the 32 typed reward packets") assumes the withdrawn fixed-K design.
6. **Few-cluster inference**: Why is a two-way cluster bootstrap over 8 checkpoint clusters expected to give calibrated 95% intervals, and what does a pilot-based power computation say the minimum detectable Δ is at 8 blocks?

## Minor Issues

- RQ4 (Experiments) still asserts "the 32 typed reward packets" — a residual of the withdrawn fixed-K=32 design that the round-9 revision removed elsewhere; contradicts Methodology, RQ3, and the spec's D2 schema.
- Related Work ends with the placeholder "> This section requires manual completion with proper citations."; all citations are prose name-year with no bibliography (the revision log itself flags the `[n.d.]` repair as incomplete pending a bib pass).
- Duplicated/nested headings: "## Problem Definition" immediately followed by "## Formal Problem Definition"; "## Method Overview" then "## Methodology"; "## Experiments" then "## Experimental Setup" — collapse each pair.
- The revision log (explicitly marked "remove before submission") is present; fine for a working draft, but note the manuscript's abstract says "6,000 sealed tasks" appear only in the Experiments section, not where D1 is first invoked.
- RQ5 lists five named perturbation variants but D3 requires six ("and one more preregistered variant to reach 6" — the sixth is never named in either artifact).
- Terminology drift: the manuscript uses TV/EX/BV/GR while the spec uses A1–A4; the GR=A4 correspondence is stated once, but BV=A3 and EX=A2 are never explicitly mapped in the manuscript.
- "RLFR-style" is used before RLFR is introduced (Experimental Setup precedes the Related Work anchor for a reader; the abstract also says "verified-goals ratio" without attribution).
- The Conclusion's claim of "an integrated framework connecting structured proof evidence to independent behavioral validation" slightly overstates a design-only contribution; consider "proposes" rather than "provides a controlled account."

## Literature Positioning

The paper's map of the field is accurate and, unusually, was re-verified against the live literature during this review. Its three-family decomposition (verifier-guided program generation; execution-grounded RL; prover feedback for formal reasoning) matches the landscape: Re:Form (arXiv 2507.16331, TMLR 05/2026) and Tan (arXiv 2605.30914) are correctly characterized as optimizing aggregate verifier outcomes without matched execution baselines; ExecVerify (2603.11226) and StepCodeReasoner (2605.11922) correctly anchor the dense-execution side; and Process-Verified RL via Lean (2606.20068) is the closest mechanism twin — dense, structured verifier feedback with credit assignment — but in Lean theorem proving against outcome-only baselines, not tool-off code generation against execution supervision. The RLFR anchor treatment is the paper's positioning centerpiece and is factually right, including the delisting (confirmed: the original URL now serves unrelated content).

Gaps: (1) The benchmark line (VERINA 2505.23135, CLEVER 2505.13938, DafnyBench, and the newer agentic AxDafny) is cited for evaluation context but the paper does not engage with the practical point these make — that existing Dafny task corpora top out around 10²–10³ tasks, which directly undercuts the D1–D3 scale (W2). (2) The 2025–2026 RLVR-criticism literature on imperfect/noisy verifiers and verifier fuzzing (e.g., arXiv 2510.00915) is thematically central to RQ6 and uncited; it would strengthen the motivation for the divergence metrics. (3) Process-supervision credit-assignment work in code RL (StepCoder, PSGPO, CodeRL+) could sharpen the claim that A2 is a fair representative of "the best dense execution supervision" rather than a strawman. Comparisons planned are fair; no unfair baseline choices detected — the risk runs the other way (A2 under-specification, W1).

## Recommendations

**Overall Assessment**: Weak Accept — as a pre-registered study design. The causal question is real, verifiably open, and the protocol answering it is more rigorous and more honest than field norms; but the plan's feasibility (data, compute, cluster count) and the under-construction of the pivotal A2 baseline mean substantial revision is required before the design can credibly be executed as stated.

**Confidence**: Medium — High confidence in the literature positioning (independently re-verified, including the RLFR delisting and an 8-id arXiv batch check) and in the internal-consistency findings (direct textual evidence). Medium overall because no results exist to check, the Dafny-internals claims (verification-logger output granularity, countermodel extraction fidelity) could not be tested against a live toolchain, and compute-feasibility judgments are estimates.

**Contribution Level**: Moderate — a useful, carefully controlled protocol contribution with a genuinely novel estimand, but no new algorithm, no results, and feasibility risks that could cap its realized impact; if executed at scale with the fixes below, the study itself could reach Significant.

### Actionable Suggestions for Improvement
1. **Symmetrize the density audit (addresses W1)**: preregister A2's exact channel set, define "usable execution packet" on completed prefixes (empty bodies), extend the RQ3c gate to both dense arms, and report per-snapshot usable-rate profiles for A1 vs. A2 so a density asymmetry cannot silently confound RQ1.
2. **Right-size and power the design (addresses W2, W3)**: run the pilot split first and use it to (a) publish a compute/data budget table including the solver-cost multiplier and the RQ6 variant×checkpoint crossing, (b) compute the minimum detectable effect at 8 seed blocks and either increase blocks or adopt a few-cluster-robust inference method (wild cluster bootstrap), and (c) descope D1–D3 to a constructible size with an explicit dataset-construction pipeline (auto-formalization + metamorphic-test generation), rather than listing ~24k richly annotated tasks as a user input.
3. **Gate the treatment measurement (addresses W4)**: add a preregistered validation of the obligation-type and verdict classifiers on labeled Dafny fixtures with minimum accuracy/coverage thresholds and a reported unmapped-message rate, making classifier fidelity an interpretability precondition for RQ2/RQ4 exactly as RQ3c is for the density claim.
4. **Finish the internal-consistency pass (addresses W5)**: fix RQ4's residual "32 typed reward packets" and specify the variable-length probe featurization; remove the Related Work placeholder and complete the bibliography (the revision log's venue-correction list is a ready worklist); collapse the duplicated section headings; name the sixth RQ5 perturbation; map EX/BV/GR to A2/A3/A4 once, explicitly.
5. **Re-motivate or downgrade RQ5 (addresses W6)**: state the mechanism by which reward representation should transfer to prompt-surface robustness, or reclassify RQ5 as exploratory with a two-sided hypothesis.

---

*Reviewer disclosure of limitations: this review evaluates a pre-registration draft with no collected results; ratings for Statistical Rigor reflect the planned analysis only. Dafny toolchain behaviors asserted in the spec (verification-logger granularity, `/rlimit` determinism, countermodel extraction) were not tested against a live installation. The RLFR precursor could not be read in its archived form; its characterization was cross-checked only against the manuscript's quotations, current search-index metadata, and the confirmed absence of the report at its original URL.*
