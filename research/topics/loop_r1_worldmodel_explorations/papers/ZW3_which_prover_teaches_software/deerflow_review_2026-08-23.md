# deerflow_review — ZW3

- **Skills used**: `.claude/skills/academic-paper-review/SKILL.md` (review procedure + output template) and `.claude/skills/deep-research/SKILL.md` (literature-context web-research methodology)
- **Review date**: 2026-08-23
- **Reviewer**: deer-flow academic-paper-review skill (Claude agent)
- **Inputs reviewed**: `paper-draft.revised.md` (current manuscript, read in full including revision log), `experiment-spec.md` (current spec, read in full), `seed.md` (context only)
- **Review status**: findings-only; no files outside this review were modified. The package is a pre-registration-style draft with **no collected results** — the Statistical Rigor row assesses the *planned* analysis and Reproducibility is rated on the spec's completeness, per the review instructions.

## Search log

All queries executed 2026-08-23 with WebSearch; fetches with WebFetch. No query returned zero results, but relevance varied as noted.

| # | Tool | Query / URL | Status |
|---|------|-------------|--------|
| 1 | WebSearch | `formal methods training data for code LLMs state of the art 2026` | Hit — RLVR trend context; TLA-Prover; DeepSeek-Prover synthetic-Lean background |
| 2 | WebSearch | `Lean vs Dafny post-training transfer software engineering tasks LLM` | Hit (high value) — vericoding benchmark (arXiv:2509.22908, 82% Dafny vs 27% Lean model-union success); office-work→SWE transfer (arXiv:2608.01604); miniF2F-Dafny |
| 3 | WebSearch | `theorem prover corpora fine-tuning code generation transfer 2026` | Hit — PACT/GPT-f/DeepSeek-Prover lineage; nothing on prover→general-code transfer with controls |
| 4 | WebSearch | `budget-matched controlled comparison training data sources LLM post-training compute-matched` | Hit (weak relevance) — compute-matched pretraining protocols (constant-token vs compute-matched); no post-training source-comparison twin |
| 5 | WebSearch | `cross-domain transfer matrix RLVR math code reasoning post-training asymmetric transfer` | Hit (high value) — Guru (arXiv:2506.14965); Transfer-Aware Curriculum (arXiv:2606.25178); rlvr-generalizability (ICLR 2026); asymmetric-transfer + pretraining-exposure findings |
| 6 | WebSearch | `paired win-minus-loss effect size heterogeneous benchmarks evaluation LLM` | Hit (weak relevance) — win-rate variants and Cliff's-δ practice; confirms the paired W estimand is standard ordinal practice, no direct twin |
| 7 | WebSearch | `formal verification fine-tuning limitations criticism does not improve code generation` | Hit — catastrophic-forgetting and spec-generation-difficulty critiques; no controlled negative result on formal→code transfer |
| 8 | WebSearch | `curriculum order effects supervised fine-tuning math before code staged training LLM` | Hit — Reasoning Curriculum (arXiv:2510.26143, math-first bootstrapping); anti-curriculum task-dependence; "fine-tuning on code corpus does not consistently improve" |
| 9 | WebSearch | `arXiv August 2026 formal supervision theorem proving software engineering transfer study` | Hit — Process-Verified RL for Lean (2606.20068); Goedel-Code-Prover; seL4 industrial proving; all within-formal, no transfer-out design |
| 10 | WebSearch | `"Lean" "Dafny" fine-tuning comparison same checkpoint transfer code benchmarks matched budget study` | Hit — Verina, ATLAS, BRIDGE, vericoding: benchmarks and per-language systems only. **No method twin found**: no shared-checkpoint budget-matched Lean-vs-Dafny transfer study surfaced |
| 11 | WebSearch | `preregistered positive control gate machine learning experiment design confirmatory analysis` | Hit — preregistration-in-ML literature (PNAS preregistration revolution; registered models); confirms gate design is imported from RCT practice, rare in ML |
| 12 | WebFetch | `https://arxiv.org/abs/2509.22908` (vericoding benchmark) | Hit — 12,504 problems; 27% Lean / 44% Verus / 82% Dafny off-the-shelf; no fine-tuning |
| 13 | WebFetch | `https://arxiv.org/abs/2506.14965` (Guru, cross-domain RLVR) | Hit — 6 domains, 92K examples, 7B/32B; pretraining-exposed domains benefit from cross-domain RL, others need in-domain training; no budget-axis matching |
| 14 | WebFetch | `https://arxiv.org/html/2608.01604v1` (office-work→SWE) | Hit — +5.8pp SWE-Bench Pro from non-SWE agent training at 122B; explicitly no domain-matched counterfactual, no budget matching |

**Citation verification**: all arXiv ids cited in this review were verified in one batched export-API request (`id_list=2509.22908,2608.01604,2506.14965,2501.16207,2510.26143`); all five resolved with matching titles. No citation debt.

---

# Paper Review: Budget-Matched Formal Supervision: Comparing Lean Proofs and Dafny Verification for Software Transfer

## Paper Metadata
- **Authors**: Not stated (AutoDiscussion pipeline output, room `9f4da36d`; loop_r1 project, package ZW3)
- **Venue**: None — internal pre-registration-style draft plus experiment spec (registered-report format)
- **Year**: 2026 (drafted 2026-08-21, revised 2026-08-23)
- **Domain**: ML for code / formal methods; LLM post-training; experimental methodology
- **Paper Type**: Empirical study **design** (pre-registration; no collected results)

## Executive Summary

The manuscript proposes a controlled comparison of two families of formal post-training supervision — Lean mathematical-proof data and Dafny-style program-verification data — measured by their transfer to five software capability families (code generation, execution reasoning, invariant inference, semantic equivalence, repair) from a single shared 0.6B–1.7B checkpoint. The methodological core is (i) a four-axis budget-matching scheme that caps every arm at the largest budget simultaneously feasible in loss-bearing tokens, optimizer updates, sampled candidates, and validator-accepted trajectories; (ii) a paired win-minus-loss transfer matrix that avoids assuming commensurate units across heterogeneous benchmarks; (iii) a preregistered formal-mathematics positive-control gate that stops confirmatory analysis if Lean training fails to improve Lean theorem proving; and (iv) a curriculum-order design (Lean→Dafny vs Dafny→Lean vs interleaved, with segmented single-source controls) that separates presentation order from source composition. Six RQs with explicit numeric success criteria are specified, and the companion experiment spec decomposes the harness into modules, configs, tests, and manifests.

The design attacks a genuine and — per this review's independent literature sweep — still-unclaimed gap: no published work trains both formal branches from one shared checkpoint at matched budget and evaluates both on software tasks. The evidence audit in the introduction and related work is unusually honest (deflated verified readings of FVEL, DeepSeek-Prover-V1.5, AlphaProof; an explicit concession to FM-alpaca, arXiv:2501.16207, as the mixed-corpus predecessor), and the documented replacement of a vacuous RQ2 estimator with a falsifiable training-time intervention shows real methodological self-correction. The main shortfalls are on the feasibility and interpretation side: the plan implies on the order of 300+ training runs with no compute estimate or power analysis; the common-feasible-intersection rule risks pinning all arms to an undertrained regime set by the worst-yield arm (making a positive-control-gate failure — which voids the whole confirmatory study — quite likely at 0.6B, where even frontier models verify only ~27% of Lean tasks off-the-shelf); a pretraining-familiarity confound between branches is unaddressed; and several preregistration-critical numbers (the RQ2 equivalence margin, the non-formal corpus identity, decoding budgets) are left symbolic. As a registered-report-style design contribution the work is above the bar with revisions; it is not yet an executable preregistration.

## Summary of Contributions

1. A four-axis budget-matching design (tokens, updates, sampled candidates, accepted trajectories) that caps all training arms at their common feasible intersection, with a Budget and Replay Ledger for verification.
2. A validity-gated transfer matrix of paired win-minus-loss effects across formal mathematics and five software families, with a preregistered Lean positive-control gate and stopping rule.
3. A curriculum-order isolation design using equal source quotas and matched Lean→Dafny / Dafny→Lean / interleaved arms, with segmented single-source controls for the segmentation confound.
4. A small-scale evaluation plan (six RQs with numeric success criteria) distinguishing formal-supervision transfer from generic supervised post-training and from the base checkpoint, packaged as an implementable harness spec.

## Claims Ledger

```
Claim 1: No published work compares math-proof vs program-verification post-training from a
         shared checkpoint at matched budget with software-task evaluation.
Evidence: Verified deflated readings of FVEL, Re:Form, DeepSeek-Prover-V1.5, AlphaProof;
          explicit FM-alpaca (2501.16207) concession as mixed-corpus predecessor. This
          review's searches #2, #3, #5, #10 independently found no twin through 2026-08-23.
Strength: Strong.

Claim 2: All four budget axes must be matched; update-only matching leaves consequential
         imbalance (RQ1).
Evidence: Argument from differing sequence lengths and acceptance yields; RQ1 is designed
          to demonstrate it. No empirical evidence yet; conceptually sound.
Strength: Moderate (design-stage).

Claim 3: Paired win-minus-loss W permits comparison across heterogeneous native metrics
         without assuming commensurate units.
Evidence: Statistical argument; standard ordinal-effect practice (Cliff's δ family;
          search #6). Correct but with a tie-dominance vulnerability at small scale (W5).
Strength: Moderate.

Claim 4: The positive-control gate prevents uninterpretable software claims when the Lean
         manipulation fails.
Evidence: Design logic imported from RCT/preregistration practice (search #11); coherent
          and correctly specified as a stopping rule. Thresholds (0.10 / 0.05) are not
          power-justified.
Strength: Strong as logic; Weak as calibrated numbers.

Claim 5: Equal source quotas plus reverse-order and interleaved arms isolate temporal
         order from composition; segmented single-source controls remove the
         segmentation confound.
Evidence: Design argument; the segmented-halves control is a genuinely careful touch.
Strength: Strong (design-stage).

Claim 6: RQ2's flattened-vs-natural replay intervention is a falsifiable test of replay-
         exposure robustness, and the Hájek reweighting it replaced was vacuous.
Evidence: The vacuity argument (weights over training examples cannot alter a frozen
          checkpoint's held-out behaviour) is correct; the replacement contrast
          μ(θ_flat) − μ(θ_nat) is a real between-checkpoint difference.
Strength: Strong.
```

## Strengths

### S1: A verified, still-unclaimed gap, argued with unusual evidential honesty
The introduction and related work (Introduction ¶2–3; Related Work, all four subsections) do not inflate prior transfer evidence — they deflate it with primary-source numbers: FVEL's 69→81 SV-COMP gain is reported as 6.9%→8.1% on a 1,000-problem subset with the authors' own seL4 corpus-correlation attribution and Code2Inv 46→46; DeepSeek-Prover-V1.5's 63.5% miniF2F is flagged as a 32×6400 search-budget figure against a 51.6% pass@128 counterpart; AlphaProof's 28/42 is correctly attributed to the combined system with AlphaGeometry 2; FM-alpaca's +62.5%-relative HumanEval gain is shown to collapse to ~+1% against a strong SFT baseline. This review's independent sweep (searches #2, #3, #5, #10) confirms the head-to-head budget-matched design remains unclaimed as of 2026-08-23. The resulting motivation — "neither branch has a credible code-transfer result, and the field cites both as though the question were settled" — is earned rather than asserted.

### S2: Preregistration machinery well beyond field norms
The design stack — common-feasible-intersection budget capping (Methodology §Budget-Matched Arm Comparison), a positive-control gate with an explicit stopping rule and a no-reinterpretation clause (§Validity-Gated Transfer Matrix), mutually disjoint RQ4/RQ5/RQ6 panels with frozen hash-partitioned splits (Experiments §Experimental Setup; spec §Panel split), seed-cluster-robust few-cluster inference with multiplicity adjustment, and a ledger that makes budget compliance auditable per training step — is far more disciplined than anything in the cited transfer literature (Guru, arXiv:2506.14965, matches nothing across domains; arXiv:2608.01604 concedes it has "no causal or domain-matched counterfactual"). If executed, the artifact would set a methods bar for post-training comparisons generally, not just for this question.

### S3: Documented self-correction of a vacuous test (RQ2)
The manuscript devotes a full paragraph (Experiments §RQ2) and the spec a REMOVED note (spec §M2) to explaining why the earlier Hájek inverse-replay reweighting could not fail — weights indexed over training examples have no channel to a frozen checkpoint's held-out behaviour — and replaces it with a preregistered training-time intervention (natural vs flattened replay regimes at identical four-axis totals, with a deterministic, performance-independent redistribution rule). The explicit fallback ("if the doubled training cost is not affordable, drop RQ2 and report replay as an unaddressed threat; it is not acceptable to retain a test that cannot fail") is exactly the right epistemic posture. This is the strongest single piece of methodological writing in the package.

### S4: The curriculum design controls a confound most curriculum papers ignore
Segmenting the Lean-only, Dafny-only, and non-formal controls into two consecutive halves *even when both halves use the same source* (Methodology §Staged Curriculum Comparison) means sequential-curriculum contrasts cannot be confounded by segmentation, checkpoint handling, or optimizer-state discontinuities — a control absent from the math-first curriculum literature (e.g., Reasoning Curriculum, arXiv:2510.26143). Combined with equal per-half quotas (T/2, S/2, N/2, K/2) and the uninterrupted optimizer-state policy, RQ6's order contrast is cleanly identified at the design level.

## Weaknesses

### W1: No compute accounting or power analysis for a plan of ~300+ training runs
Summing the RQs: RQ1 declares 96 runs, RQ2 another 96 (all six arms × two replay regimes × 8 seeds), RQ3 24 (2 arms × 12 seeds), RQ4 36, RQ5 48, RQ6 36 — over 300 training runs of a 0.6B–1.7B model, each preceded by sampling N candidates and running Lean-kernel/Dafny-verifier checks on all of them, plus oracle-based evaluation on panels up to 9,000 prompts (Experiments §RQ1–RQ6; spec §RQs). Neither document estimates GPU-days, verifier-CPU cost, or wall-clock; the spec's Inputs section says only "GPUs for ~96 runs (RQ1) + 12-seed arms." Worse for a preregistration: none of the numeric success thresholds (imbalance ≤0.01, gate W≥0.10, aggregate effects ≥0.05, order effects ≥0.03) or seed counts (8 vs 12) is justified by a power or minimum-detectable-effect calculation, and the RQ2 "preregistered equivalence margin" is never given a number — the single most preregistration-critical constant in RQ2 is left symbolic. **Fix**: add a compute budget table per RQ, a simulation-based power analysis under plausible tie rates, and commit the RQ2 margin (and cap-quantile) to numbers before any training run.

### W2: The common-feasible-intersection rule couples all arms to the worst arm and makes gate failure the modal outcome
Capping every arm at the largest budget feasible for *all* arms (Methodology §Budget-Matched Arm Comparison) means the accepted-trajectory quota K is set by the lowest-yield arm — almost certainly Lean at 0.6B–1.7B, where even frontier off-the-shelf models verify only ~27% of Lean tasks versus 82% for Dafny (vericoding benchmark, arXiv:2509.22908; model-union numbers, so small-model single-pass yields will be far lower). A tiny K forces extreme replay multiplicity in every arm and risks leaving the Lean arm undertrained — precisely the condition under which the RQ3 gate (W≥0.10, lower bound >0.05, on kernel-checked proof acceptance) fails and the entire confirmatory study (RQ4–RQ6, ~120 runs) is demoted to diagnostic. The manuscript treats gate failure as an honest outcome, which is right, but never estimates its probability, never uses the pilot to forecast acceptance yields, and never specifies a contingency (e.g., a larger checkpoint tier, proof-step-level rather than whole-proof supervision, or an easier theorem stratum for the gate panel). **Fix**: preregister a pilot-based feasibility gate *before* the main runs — minimum acceptable K and predicted gate pass probability — and a predeclared fallback if Lean yield at this scale is below it.

### W3: A pretraining-familiarity confound between branches is unaddressed
Budget matching equalizes exposure *during post-training* but not the checkpoint's prior exposure to each language. Lean/mathlib text is comparatively plentiful in public pretraining corpora; Dafny is rare — and the cross-domain RLVR literature the seed itself logs finds that transfer gains concentrate in domains the base model saw heavily during pretraining (Guru, arXiv:2506.14965). A Dafny-vs-Lean difference in the RQ4 matrix therefore admits two readings the design cannot separate: supervision-type semantics (the paper's hypothesis about state-transition objects) versus differential pretraining familiarity/tokenization fit. The zero-exposure anchor detects neither, since it is common to both branches. **Fix**: at minimum, discuss this threat explicitly and report base-checkpoint perplexity/zero-shot competence on each formal language as a covariate; stronger, add a syntax-familiarity control (e.g., continued pretraining on unverified Lean/Dafny text without checker supervision) so the "formal supervision" effect is separated from "seeing the language" — the design's own logic (matched non-formal SFT controls for generic supervision) extends naturally to this arm.

### W4: The non-formal control N and the Dafny corpus are construct-underspecified for a load-bearing role
Every entry of the transfer matrix is defined relative to θ_N (Problem Definition, T^{(r)}_{a,j} = μ_j(θ_a) − μ_j(θ_N)), yet neither document says what D_N *is*: code instruction data? general chat? math prose? Each choice changes what "formal supervision beats non-formal supervision" means — a code-heavy N makes the software contrasts conservative, a chat-heavy N makes them nearly vacuous (this is exactly the UltraChat-vs-Tulu baseline fragility the paper criticizes in FM-alpaca). Its "predefined task-appropriate validator" is similarly unnamed. The Dafny arm has the same problem at lower severity: "Dafny-style records encoding states, transitions, contracts, invariants, frame conditions, and verification conditions" (Problem Definition) is a format description, not a corpus identity, and the paper itself concedes acceptance "has [non-]identical meaning across these validation regimes" while still treating K-equality as a matching axis — an interpretive tension that should be surfaced as a stated limitation rather than a parenthesis. **Fix**: pin corpus identities, sources, and validator definitions in the spec manifests (the manifest machinery already exists); preregister at least two N variants (code-flavored, general) or justify the single choice.

### W5: Tie dominance threatens the W estimand's power at this model scale
With binary oracles (kernel acceptance, test pass) and 0.6B–1.7B models, most panel prompts will likely fail under *both* the arm and the control, so w_p = 0 dominates and W is an average over a small informative minority. The success thresholds (gate W≥0.10; RQ4/RQ5 ≥0.05; RQ6 ≥0.03) are on the raw tie-inclusive scale, so their meaning depends entirely on the unknown non-tie rate — W = 0.05 could be 5% of prompts decided one way or 50% of a 10%-informative panel. The design never reports or conditions on the tie rate, and the bootstrap will produce wide intervals when informative prompts are scarce, further inflating gate-failure risk (compounding W2). **Fix**: preregister the expected non-tie rate from the pilot, report W alongside the conditional win rate among non-ties, and consider difficulty-stratified panels (as the strata machinery for training acceptance already does) so a band of tractable prompts carries the contrast.

### W6: Related work misses the benchmark evidence closest to its own feasibility question
The related work covers four literatures well but omits: (i) the vericoding benchmark (arXiv:2509.22908) — the largest direct Lean-vs-Dafny-vs-Verus tractability comparison, whose 27%/82% gap is both a feasibility warning (W2) and a potential confound (W3) for this design; (ii) the cross-domain RLVR transfer literature in the *body* of the paper — Guru (arXiv:2506.14965) is logged in the seed ledger and revision note but never appears in Related Work despite being the closest informal-domain precedent for the transfer-matrix framing; (iii) math-first curriculum precedent (Reasoning Curriculum, arXiv:2510.26143) directly relevant to RQ5/RQ6's Lean→Dafny hypothesis; (iv) the August-2026 signal the seed itself flags (arXiv:2608.01604) showing cross-domain post-training→SWE transfer with a competing behavioral mechanism (goal-directed execution) that could explain formal→software transfer without any state-semantics story. None of these scoops the contribution, but all four shape its interpretation. Additionally the manuscript still has no bib apparatus (inline author-title references only; acknowledged in the revision log as outstanding).

## Methodology Assessment

| Criterion | Rating (1-5) | Assessment |
|-----------|:---:|------------|
| Soundness | 4 | The identification logic (shared checkpoint, four-axis matching, paired items/seeds, gate, order controls) is coherent and the RQ2 vacuity correction is exactly right; docked one point for the unaddressed pretraining-familiarity confound (W3) and the unanalyzed coupling of all arms to the worst-yield arm (W2). |
| Novelty | 4 | No method twin found through 2026-08-23 (searches #2, #5, #10): the budget-matched, per-branch, gate-protected transfer design is new, and honestly positioned as the successor to FM-alpaca's confounded mixed-corpus contrast. Individual components (ordinal paired effects, preregistration gates, curriculum controls) are imports, so not a 5. |
| Reproducibility | 4 | Rated on spec completeness: the harness decomposition (12 modules, per-RQ configs, manifests, unit tests incl. flatten-replay determinism, stubbed checkers) is unusually thorough for a plan; docked for unpinned corpus identities (W4), the symbolic RQ2 equivalence margin, and open decoding-budget/strata constants that the spec itself lists as assumptions. |
| Experimental Design | 4 | Arm set, baselines (incl. zero-exposure anchor and equal-update-only ablation), disjoint panels, and segmentation controls are comprehensive; docked for absent feasibility/pilot forecasting (W2) and tie-rate blindness in panel construction (W5). |
| Statistical Rigor | 4 | *Planned* analysis: paired ordinal estimand, item-by-seed stratified bootstrap, wild-cluster few-cluster inference, per-RQ multiplicity control, TOST equivalence, one-sided gate bounds — a strong plan; docked for no power analysis anywhere, unjustified numeric thresholds, and an unnumbered equivalence margin (W1). |
| Scalability | 2 | ~300+ training runs (doubled by RQ2's design) plus per-candidate formal checking and up to 9,000-prompt oracle evaluations, with no compute estimate; conclusions are also confined by design to 0.6B–1.7B, with scaling explicitly deferred. The spec's own escape hatch (drop RQ2) is the only cost-control lever named. |

## Questions for the Authors

1. What acceptance yield (K/N) do you expect for the Lean arm at 0.6B–1.7B, given that frontier models verify only ~27% of Lean vericoding tasks off-the-shelf? What is the minimum K below which you would declare the design infeasible rather than run it, and will the blinded pilot forecast the RQ3 gate pass probability before the ~120 confirmatory runs are committed?
2. What, concretely, is the non-formal corpus D_N and its "task-appropriate validator"? Given your own FM-alpaca critique that the transfer effect swings from +62.5% to ~+1% depending on the SFT baseline, how do you prevent the choice of N from predetermining the sign of the transfer matrix?
3. How will you distinguish supervision-type effects from pretraining-familiarity effects, given that Dafny is far rarer than Lean/mathlib in public pretraining corpora and cross-domain RLVR work (arXiv:2506.14965) finds gains concentrate in pretraining-exposed domains? Would you add an unverified-text continued-pretraining control per language?
4. What numeric equivalence margin will RQ2 use, and what is the power of the 8-seed TOST design to detect a replay effect of practically relevant size? Similarly, what analysis justifies 0.10/0.05/0.03 as the RQ3/RQ4–5/RQ6 thresholds?
5. What tie rate do you anticipate on each software family at this scale, and will you report the conditional win rate among non-ties alongside W? If ties exceed, say, 90%, is a W≥0.05 criterion even reachable with 12 seeds?
6. The formal curriculum criterion K^{(r)}_j compares θ_C only against max{θ_M, θ_V} (Problem Definition), but RQ5's success criterion additionally requires beating matched non-formal SFT. Which is the preregistered estimand, and should the formal definition be amended to include θ_N?

## Minor Issues

- Duplicated/nested headers: "## Problem Definition" immediately followed by "## Formal Problem Definition", and "## Methodology" duplicating "## Method Overview" content structure; also "## Experiments" followed directly by "## Experimental Setup". Flatten before submission.
- The budget-equality notation `B^{(r)}_{M,r}` (Problem Definition) double-indexes r; `B_{a,r}` with a superscript-free constraint would be cleaner, and the "four budget-matched comparison views" framing survives from the seed's superseded design — the delivered design trains at one common intersection, so the per-regime family {θ^{(r)}_a} is misleading (there is one θ_a per arm, not four).
- RQ2 contains a near-duplicate sentence: "This keeps loss-bearing tokens … so the regimes differ in the *distribution* of exposure and not its total" and, two sentences later, "Both regimes are held to the same four-axis budget intersection … so flattening changes the *distribution* of exposure without changing its *total*." Merge.
- W is defined twice with different formalisms (probability difference in §Validity-Gated Transfer Matrix; ±1/0 per-prompt mean in §Experimental Setup). Consistent, but state the equivalence once.
- "0.6B–1.7B" is quoted as a range while the problem definition requires a *single* shared checkpoint θ_0; say whether this is one checkpoint of unspecified size in that range or a replicated design across sizes.
- The revision log (flagged "remove before submission") and the header provenance note must be stripped; the related-work venue corrections listed there (FVEL = NeurIPS 2024 D&B, DeepSeek-Prover-V1.5 = ICLR 2025, etc.) still need to land in an actual bibliography — no refs.bib apparatus exists in the package.
- RQ2's evaluation panel includes formal math (700 of 4,200), so its formal-math prompts and RQ3's 2,500-task panel need an explicit disjointness/overlap statement; the disjointness guarantees in the spec cover only RQ4/RQ5/RQ6.
- Spec §Datasets labels D1 as "Sole input to RQ2 weights" — a leftover from the removed Hájek design that contradicts the REMOVED note in §M2; update the sentence.
- Minor scope mismatch: abstract says "post-trains a shared 0.6B–1.7B checkpoint … staged and order-controlled mixtures" — plural "mixtures" reads as more arms than the three mixed-supervision curricula actually specified.

## Literature Positioning

The paper's four-literature map (verifier-feedback theorem proving; verified program generation; formal reasoning for program properties; execution-feedback RL) is accurate, and its per-work gap statements are the strongest related-work writing this reviewer has seen from the pipeline: each gap stands independently of the proposed study (Re:Form OOD only within formal verification; FVEL's authors' own corpus-correlation attribution; Proof2Silicon/AlphaVerus/Clover not updating parameters; AlphaProof and DeepSeek-Prover-V1.5 never evaluating code), and FM-alpaca (arXiv:2501.16207) is properly conceded as the confounded predecessor rather than ignored. The independent sweep confirms the central positioning claim: benchmarks now exist comparing Lean and Dafny tractability for LLMs (vericoding, arXiv:2509.22908; Verina; miniF2F-Dafny), and cross-domain post-training transfer is an active 2026 area (Guru, arXiv:2506.14965; Transfer-Aware Curriculum; rlvr-generalizability, ICLR 2026; office-work→SWE, arXiv:2608.01604), but nobody has run the budget-matched per-branch formal comparison. What is missing (W6): the vericoding tractability gap as feasibility evidence, the cross-domain RLVR transfer-matrix literature in the body rather than only the seed ledger, math-first curriculum precedent (arXiv:2510.26143) for RQ5/RQ6, and the competing behavioral-mechanism account of cross-domain transfer (arXiv:2608.01604) as an alternative explanation the transfer matrix cannot by itself rule out. Comparisons drawn are fair — if anything the paper under-claims relative to what its design would deliver.

## Recommendations

**Overall Assessment**: Weak Accept — as a registered-report-stage design. The gap is real and verified, the identification machinery is state-setting, and the self-corrections are credible; but the preregistration is not yet executable (missing margins, corpus identities, compute plan) and the feasibility risk at the chosen scale is unquantified and plausibly fatal to the confirmatory half of the study.

**Confidence**: High — both documents were read in full; every load-bearing prior-work claim in the manuscript was spot-checked against the literature sweep and none was found inflated; the feasibility concerns rest on independently verified numbers (arXiv:2509.22908). Confidence is necessarily about the *design*, since no results exist to audit.

**Contribution Level**: Moderate (design-stage) — with a realistic path to Significant if executed with the gate passed, or even with an honest gate-failure report, since the four-axis matching methodology and the falsifiability discipline are contributions independent of the empirical outcome.

### Actionable Suggestions for Improvement
1. **Add a feasibility pre-gate before the confirmatory runs.** Use the blinded pilot to estimate per-arm acceptance yields and forecast the RQ3 gate pass probability; preregister a minimum K and a fallback (larger checkpoint tier, proof-step-level supervision, or an easier gate-panel stratum) if Lean yield at 0.6B–1.7B is below it. Publish a compute-budget table (GPU-days + verifier-CPU per RQ) alongside.
2. **Close the preregistration holes with numbers.** Commit the RQ2 equivalence margin, expected tie rates per family (reporting conditional win rate among non-ties alongside W), a simulation-based power analysis justifying 8/12 seeds and the 0.10/0.05/0.03 thresholds, and pinned identities + manifests for D_N and the Dafny corpus (ideally two preregistered N variants, code-flavored and general).
3. **Neutralize the pretraining-familiarity confound.** Report base-checkpoint competence/perplexity on Lean and Dafny as covariates and add (or at least argue away, citing arXiv:2506.14965) a continued-pretraining-on-unverified-text control per language, so branch differences can be attributed to formal supervision rather than language familiarity; fold the vericoding tractability gap (arXiv:2509.22908), the cross-domain RLVR matrix literature, and the behavioral-transfer alternative (arXiv:2608.01604) into Related Work, and complete the bib pass the revision log already schedules.
