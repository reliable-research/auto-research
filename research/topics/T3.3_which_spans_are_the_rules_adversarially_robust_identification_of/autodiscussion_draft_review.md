# Review: T3.3 Autodiscussion Draft Package

Reviewed 2026-08-13. Inputs: `research-report.md`, `experiment-spec.md`, `paper-draft.md` (job `ZT3.3--72b10a6c`), vs. `discussion.md` + `README.md` in this folder. All web checks against 2025–2026 literature; sources listed at end.

## 1. Architecture

The draft proposes a **measurement harness**, not a defense, in three stages:

1. **PCPL (Provenance-Contract Pair Ledger).** Real governance spans (system-prompt policies, defense rules) and chatter spans, each annotated with an 8-field semantic contract (provenance, addressee, action, deontic force, scope, exceptions, quoted/reported status). Ground truth `is_rule` derives **only** from provenance. Bidirectional register rewrites — casualized-rule and imperativized-chatter — are admitted only if two blinded validators confirm all contract fields preserved AND a separate register-manipulation check confirms the intended register shift.
2. **Masked paired evaluation.** Seven identifier families score each original/rewrite independently (pair metadata masked); frozen per-family `NormalizationAdapter`s (calibrated on disjoint, provenance-balanced data) map heterogeneous outputs to binary rule/chatter decisions; a completeness validator enforces the full Cartesian record set.
3. **Directional paired-error analysis.** Estimands: miss-pin rate P(rewrite→chatter | true rule, casualize direction), false-pin rate P(rewrite→rule | true chatter, imperativize direction), paired rewrite-minus-original error diff; macro/micro aggregation; pair-clustered family-stratified bootstrap CIs; robustness grade A–D by the **worse** directional 95% upper bound (UNGRADED if <100 pairs/direction).

Datasets: D1 audit corpus (1,200 gated/ungated rewrites), D2 calibration/eval corpus (400+400 per family), D3 synthetic benchmark with known rates (24 configs × 200 seeds × 10k pairs/direction), D4 grade-stress corpus (300 pairs/cell). Baselines are all **self-ablations of the harness**: ungated admission, pooled threshold, unbalanced calibration, direction-collapsed estimator, unpaired bootstrap. Six RQs with numeric PASS/FAIL criteria (violation ≤5%, α ≥0.80, macro-F1 ≥0.80, stability ≥95%, |rate error| ≤0.02, grade stability ≥90%).

**Load-bearing design choices:** (a) provenance-only ground truth with imperativeness banned from labeling; (b) the two-check admission gate (semantic contract vs. register manipulation kept separate); (c) never collapsing the two directions; (d) worst-direction grading. Choice (b) is the single biggest validity risk (as discussion.md already identified), and choice "seven identifier families" is load-bearing but the families are **never named** anywhere in the three artifacts — they exist only as "7 concrete family stubs" left to the implementer.

**Critical structural flaw:** the experiment-spec states outright it is "a measurement/validation study of the harness itself … not a leaderboard of identifiers." All six RQs validate the instrument (gate validity, annotator agreement, calibration accuracy/stability, estimator recovery on synthetic data, grade stability). **No RQ measures the actual scientific question** — whether real identifiers' miss-pin/false-pin rates degrade under register rewrites. The headline experiment of the topic (README: "测识别器的错保率与漏保率") has no hypothesis, no success criterion, and no driver in the spec.

## 2. Novelty ledger

Mechanism scored under the framing verbs ("audit", "isolate", "characterize"): the operative mechanism is *label-preserving bidirectional register-rewrite attack on a binary rule-vs-chatter span classifier, with a deontic-contract validity gate and paired directional error decomposition*.

| # | Claim | Nearest named prior | Operational delta | Stance |
|---|-------|--------------------|-------------------|--------|
| C1 | Register shifts (casualizing rules / imperativizing chatter) systematically corrupt governance-span identification, undermining constraint pinning's premise | (i) **Blind Spots in the Guard** (arXiv 2605.22001): LLM-paraphrase rewrites of injections into "innocuous prose" push Prompt-Guard-2 FNR 0.593→0.989 — this is exactly the miss direction, on injection detectors. (ii) **Lost in Compaction / COMPINT** (arXiv 2608.11242, Aug 2026): session-constraint retention "varies sharply with … SC phrasing", and ships an SC-aware extractor (an identification component) with >90% retention. (iii) **Governance Decay** (arXiv 2606.22528) already names the extraction limitation ("requires the constraint to be extractable as a quotable rule"). | Miss direction is substantially pre-demonstrated for injection/guardrail detectors; phrasing-sensitivity of constraint retention is already observed (not adversarially controlled) by COMPINT. Remaining delta: **bidirectionality** (false-pin via imperativized chatter is genuinely unmeasured; guardrail lit only notes benign over-blocking anecdotally), provenance-fixed paired design, and pinning-specific framing. | **somewhat-novel** (verified, 5 queries). The false-pin half and the paired isolation are the defensible core; the miss-pin half must concede 2605.22001 and 2608.11242 or a reviewer will produce the twin. Neither appears in the draft's related work. |
| C2 | Provenance-contract validity gate (PCPL): 8-field deontic contract + dual blinded validation + separate register-manipulation check makes rewrite validity independent of imperativeness | Adversarial-paraphrase validity constraints (TextFooler lineage; **Agentic Adversarial Rewriting**, arXiv 2604.23483, requires "semantic equivalence + linguistic coherence"); annotation-side: obligation/permission/prohibition tagging from legal NLP (ContractNLI/LexGLUE family) — no adversarial variant found | Generic attack validity = meaning preservation; PCPL's direction-specific asymmetric contract (Evade must *entail* the obligation; Spoof must *not introduce* one) plus provenance-derived labels is a stronger, task-specific criterion. Search found no deontic-force-preserving adversarial-rewrite gate. | **somewhat-novel** (verified, 3 queries). It is an annotation methodology, not a mechanism — novel as dataset-construction contribution (GovSpan-Adv style), not as a method. |
| C3 | Directional miss-pin/false-pin decomposition + worst-direction A–D robustness grading with pair-clustered bootstrap | Standard paired FN/FP decomposition; McNemar-style transition analysis is textbook; letter-grading with arbitrary cutoffs (0.05/0.10/0.20) is packaging | Bookkeeping discipline (direction never collapsed) is good practice, not a contribution; the RQ5/RQ6 "estimator validates on synthetic data" exercise verifies arithmetic | **not-novel** as method; acceptable as reporting protocol. Should not be listed as a headline contribution (it currently is, contribution 3). |
| C4 | Per-family frozen normalization adapters beat a pooled threshold for cross-family comparability (RQ3/RQ4) | Ordinary per-model threshold calibration (Platt/isotonic per system) — universal practice in detector benchmarking | None beyond applying standard calibration hygiene | **not-novel**; fine as infrastructure, should not consume 2 of 6 RQs. |

## 3. Consistency vs discussion.md

**Agreements.** Core problem framing identical (register channel isolated from structural forgery; miss-pin/false-pin as the two directional rates; provenance/annotation-based ground truth; validity gate named as the biggest risk; measurement study, not a defense; "surface imperativeness is not ground truth" is preserved faithfully).

**Improvements over discussion.md.** (a) The 8-field contract schema is more explicit than discussion.md's "obligation entailed / not introduced" gate — quoted/reported status is a genuinely good addition. (b) The completeness validator and frozen-before-eval calibration discipline are stronger engineering hygiene. (c) Synthetic estimator validation (RQ5) is a reasonable addition discussion.md lacks. (d) Register-manipulation check as a separate gate (manipulation-check ≠ validity-check) is cleanly articulated.

**Contradictions / silent scope changes (serious).**
1. **The deployment form is silently deleted.** discussion.md Stage 1 refined explicitly puts *both* forms in scope: pilot (pre-segmented pairs) **and** joint localization+classification over 8k–32k unsegmented transcripts (span F1, IoU ≥0.5, depth-stratified — SP3). The draft package contains only pre-segmented spans; localization is gone without acknowledgment. This deletes the half of the problem "deployed pinning actually consumes."
2. **The adaptive attacker (SP4) is gone.** No query-access round, no static-vs-adaptive Δ. discussion.md made this a named sub-problem.
3. **Identifier families are abstracted away.** discussion.md names 7 concrete arms (regex deontic heuristic, DeBERTa, adversarially-trained DeBERTa b′, LLM-judge as pre-registered primary, ASIDE-style privilege baseline, SeqMonitor-style monitor, embedding salience scorer — the deployed-practice baseline). The draft keeps the count "seven" but drops all identities, including the b′ adversarial-training arm the critic demanded ("without it the paper reads 'we didn't try the standard fix'") and the LLM-judge prompt-paraphrase variance control.
4. **The blinded-validation refinement is regressed.** discussion.md's SP2 critic flagged that validators comparing source and rewrite side-by-side inflates agreement; the refined protocol requires the annotator to see **the rewrite alone** and independently state whether it carries an obligation. The draft's gate has validators "compare the source and rewrite against every contract field" — precisely the unblinded protocol the critic rejected. The disjoint-model-family NLI back-check (anti-circularity) is also dropped.
5. **Concrete data sources dropped.** TensorTrust defense prompts + curated policy pool + LMSYS-Chat-1M matched chatter (with per-source breakdown) → replaced by "Inputs You Must Provide." The GovSpan-Adv artifact — the audit's stated justification for the topic ("the artifact is a direct input to the Tier-1 line either way") — no longer exists as a deliverable.
6. **Contested-label / boundary audit (SP1, SP5) gone.** The [边界] label's whole point — indexical constraint-hood, κ ≥0.7 gate, headline rates with/without contested items — is absent. The draft treats labels as crisp, exactly what the Stage-1 critic called ill-posed.
7. **Statistical plan swapped.** McNemar + Holm, TOST equivalence margin (making a near-null interpretable), power discussion → replaced by threshold-attainment PASS/FAIL tests on the harness itself. The falsifiable stance ("robust judge is a publishable positive result") is lost.
8. **Cost/timeline discipline dropped.** discussion.md: ~40 annotator-hours, <8 GPU-h, $500–1,000, G1–G3 go/no-go gates, ICLR 2027 feasibility call. The draft: 3 experts × 1,200 rewrites × 8 fields + 4 validators × 800 + frozen expert labels for 400+400 items × 7 families (≈5,600 labels) — thousands of annotator-hours, no gates, no venue plan.

## 4. Citation audit

Sampled 13 across the three artifacts, prioritizing load-bearing and 2026-dated ones. **Zero confabulations found** — atypical for this pipeline and worth noting.

| Citation (as cited) | arXiv/venue | Verdict |
|---|---|---|
| Governance Decay / ConstraintRot (motivation anchor: 1,323 episodes, 0%→30%, 59% worst, pinning→0%) | 2606.22528 | **CONFIRMED**; attributed numbers match the abstract. The "38% when constraints dropped" figure was not independently verified — spot-check before use. |
| BIPIA, Yi et al. ("Atacks" [sic]) | 2312.14197 | **CONFIRMED** (real; fix the title typo, which is propagated verbatim into the paper draft's intro). Attributed claim (inability to distinguish information from instructions) accurate. |
| Spotlighting, Hines et al. | 2403.14720 | **CONFIRMED**; attribution accurate. |
| AgentVigil, Zhun Wang et al. | ACL Findings-EMNLP 2025 / arXiv 2505.05849 | **CONFIRMED** (real; originally circulated as AgentXploit). |
| StepJack, Zhan et al. | 2608.06477 | **CONFIRMED** (Aug 2026, 480 examples, 6 CUAs); attribution accurate. |
| IHEval, Zhihan Zhang et al. (3,538 examples, 9 tasks, 48% conflict accuracy) | 2502.08745, NAACL 2025 | **CONFIRMED**; numbers match. |
| XIH-Bench / Language Boundary Effect, Moon et al. | 2607.23545 | **CONFIRMED**; title, six languages, findings all match. |
| ManyIH / ManyIH-Bench, Jingyu Zhang et al. (853 tasks, 12 levels, ~40%) | 2604.09443 | **CONFIRMED**; numbers match. |
| Where Instruction Hierarchy Breaks, "G. Edward Suh & Sanjay Kariyappa" | 2606.07808 | **CONFIRMED** exists; Kariyappa is an author but full author list/order not verified — check before camera-ready. Attributed 3-stage decomposition accurate. |
| Instructional Segment Embedding, Tong Wu et al. | 2410.09102, ICLR 2025 | **CONFIRMED**; attribution accurate. |
| V-Steer, Siqi Zeng et al. | 2607.26228, COLM 2026 | **CONFIRMED**; authors match (Zeng, Lee, Zhao, Hockenmaier). |
| SyRuP, Seoyeon Kim et al. | 2607.23991 | **CONFIRMED** exists; author attribution unverified. |
| IH-Challenge, "Chuan Guo et al." (OpenAI, HF dataset) | 2603.10521 | **CONFIRMED** exists incl. HF dataset; author attribution unverified. |
| Control Illusion (research-report significance only) | 2502.15851 | **CONFIRMED** (real, known). |

Caveat: the paper-draft's Related Work ends with "> This section requires manual completion with proper citations" — the pipeline itself flags the section unfinished. More important than any confabulation: the related work is **missing the two nearest twins** (2605.22001 paraphrase-evasion of injection detectors; 2608.11242 phrasing-sensitive constraint retention) and everything discussion.md Stage 3 demanded (TensorTrust, ChatInject, ASIDE, SeqMonitor, PrefEval, MemoryCallback, R2-Guard, deontic/speech-act NLP, TextFooler-lineage paraphrase attacks).

## 5. Gap to implementation

- **All data is externalized.** D1 and D2 — real governance corpora with per-span 8-field contract annotations, plus register rewrites — are listed under "Inputs You Must Provide." The harness is runnable only against data no one has built; the spec never says where spans come from (discussion.md's TensorTrust/LMSYS recipe would fill this).
- **All identifiers are stubs.** Seven families must satisfy an `Identifier.score` protocol; none is specified. Without named identifiers, the load-bearing claim "seven heterogeneous families" is unimplementable and the per-family macro-F1 ≥0.80 criterion is untestable.
- **Human annotation is the real cost and is unbudgeted.** RQ1: 3 experts × 1,200 rewrites × 8 fields (28,800 field judgments). RQ2: 4 validators × 800. RQ3/4: ≈5,600 frozen expert labels across 7 families. This is order thousands of annotator-hours vs. discussion.md's ~40; no recruitment, payment, or IRB plan. This alone breaks any 2026 submission timeline.
- **The RQ set never runs the actual experiment.** Even fully implemented and PASSing all six RQs, no miss-pin/false-pin number for any real identifier is produced. A "headline RQ0" driver (real identifiers × admitted pairs → grades) is missing from the implementation plan, drivers, and report module.
- **Underspecified dependencies** (acknowledged in "Open Decisions"): register-manipulation checker model, adapter functional forms per family, within-pair correlation in the synthetic generator, bootstrap CI method. Reasonable to defer, but each is on the critical path.
- **Compute is fine** (CPU-bound bootstraps; RQ5's 24×200×20k synthetic sweep is cheap). Code skeleton (14 tasks, module list, tests, CLI) is genuinely implementable in ~1–2 weeks; it is the science around it that is missing.
- **Timeline realism:** no venue plan in the artifacts. discussion.md's ICLR 2027 (Sep 2026) call was already "tight" for the *smaller* design; the draft's annotation volume makes it infeasible unless scaled back to discussion.md's numbers.

## 6. Verdict

**Adopt-with-fixes** — with the caveat that the fix to the experiment plan is closer to a partial redo. The problem framing, PCPL contract idea, provenance-only ground truth, and directional-error discipline are sound and faithful to the topic; the citation base is clean (13/13 confirmed, unusual for this pipeline); but the draft has quietly transformed a sharp adversarial measurement study into a self-validating harness spec that never measures anything, while deleting the deployment form, the adaptive attacker, the named identifiers, the concrete data recipe, and the blinded-gate refinement that discussion.md's critic loop had already fought for. Priority fixes: **(1)** Add the missing headline experiment — RQ0: named identifier families (restore discussion.md's a/b/b′/c/d/e/f roster) evaluated on a concretely sourced PCPL (TensorTrust + policy pool + LMSYS chatter), reporting per-direction miss-pin/false-pin, Δ vs. original, McNemar + TOST — and demote RQ3/RQ4/RQ6 to appendix sanity checks; **(2)** restore the blinded rewrite-only validation protocol and disjoint-family entailment back-check, and cut annotation volumes to discussion.md's feasible scale (~600 spans, ~40 annotator-hours) so a 2026–27 submission is possible; **(3)** rewrite Related Work to concede the two 2026 near-twins (arXiv 2605.22001 paraphrase evasion of injection detectors; arXiv 2608.11242 phrasing-sensitive constraint retention) plus the deontic-NLP and adversarial-paraphrase literatures, and reposition the contribution on the genuinely open parts: the false-pin direction, the bidirectional paired isolation, and the deontic-contract validity gate.

---

### Verification sources

- StepJack: https://arxiv.org/abs/2608.06477
- Where Instruction Hierarchy Breaks: https://arxiv.org/abs/2606.07808
- XIH-Bench: https://arxiv.org/html/2607.23545v1
- ManyIH: https://arxiv.org/abs/2604.09443 ; https://jhu-clsp.github.io/ManyIH/
- V-Steer: https://arxiv.org/abs/2607.26228 ; https://github.com/cindy2000sh/v-steer
- SyRuP: https://arxiv.org/html/2607.23991v1
- IH-Challenge: https://arxiv.org/abs/2603.10521 ; https://huggingface.co/datasets/openai/ih-challenge ; https://openai.com/index/instruction-hierarchy-challenge/
- Governance Decay / ConstraintRot: https://arxiv.org/abs/2606.22528
- Lost in Compaction / COMPINT: https://arxiv.org/abs/2608.11242
- Blind Spots in the Guard (paraphrase evasion of injection detectors): https://arxiv.org/pdf/2605.22001
- Confidently Wrong (detector calibration under attack shift): https://arxiv.org/pdf/2606.22659
- Agentic Adversarial Rewriting: https://arxiv.org/pdf/2604.23483
