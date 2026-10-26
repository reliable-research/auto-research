# Which Spans Are the Rules? Bidirectional Register Attacks on Governance-Constraint Identification for Memory Pinning

## Abstract

Constraint pinning keeps governance spans — system policies, safety rules, standing user directives — resident while the rest of an agent's context is compacted, but it presupposes an upstream step: deciding *which spans are the rules*. We measure whether that identification step survives adversarial register manipulation that leaves provenance and meaning fixed. Two directions are attacked in a paired design: **Evade** rewrites a genuine constraint into casual chit-chat register while provably preserving its deontic force (target: **miss-pin**, the rule is silently dropped), and **Spoof** rewrites ordinary chatter into imperative register while provably *not* introducing any obligation (target: **false-pin**, junk is pinned, exhausting the pin budget and laundering authority). The miss direction has adjacent precedent — LLM-paraphrase attacks already collapse prompt-injection detectors, and constraint retention is known to be phrasing-sensitive — so our headline claims sit elsewhere: the **false-pin direction is unmeasured**, and no prior evaluation isolates the register channel **bidirectionally with provenance-fixed labels within matched pairs**. The technical core enabling this isolation is a **Provenance-Contract Pair Ledger (PCPL)**: an eight-field deontic contract per span, with rewrites admitted only through a blinded rewrite-only human validation protocol plus a disjoint-model-family entailment back-check, so that surface imperativeness never touches ground truth. On a concretely sourced corpus (TensorTrust defense prompts + curated policy pool for constraints; matched LMSYS-Chat-1M turns for chatter; ~600 base spans, ~600 validated rewrites), we evaluate seven identifier arms — deontic-cue regex, clean- and adversarially-trained DeBERTa classifiers, a pre-registered frontier LLM judge, a privilege-signal baseline, a cumulative-context monitor, and an embedding-salience scorer that mirrors deployed memory-write heuristics — in both a pre-segmented pilot form and a deployment form requiring joint localization and classification in 8k–32k-token transcripts, followed by an adaptive query-access attack round. Per-direction miss-pin and false-pin rates, paired McNemar tests with equivalence margins, and worst-direction robustness grades yield the reliability envelope that every downstream pinning mechanism currently assumes for free.

## Introduction

Large language model agents accumulate system policies, user requests, conversation history, tool outputs, and retrieved content in a shared context that must eventually be truncated, summarized, or compacted. Constraint pinning preserves governance spans across such transformations, and its stakes are documented: *Governance Decay* (arXiv:2606.22528) reports 1,323 ConstraintRot episodes in which policy-violation rates climb substantially once constraints are dropped from context, with pinning restoring compliance in the evaluated setting. But pinning defends only *what it has recognized as a rule*. The recognition step — classifying spans as governance constraint versus ordinary conversation — is presupposed by every pinning, retention, and repair mechanism, and no existing work isolates it under adversarial pressure.

The threat model is deliberately narrow: the attacker manipulates **register only**. All channel metadata is honest — no forged role tags, no injected system messages; those structural attacks are already covered by the prompt-injection and instruction-hierarchy literatures. What remains is a semantic channel: can content *lose* constraint status, or *earn* it, through phrasing alone?

- **Evade (miss-pin direction).** A genuine constraint is recast in casual register — "oh by the way, we generally don't share customer emails with anyone, you know how it is" — while its addressee, action, deontic force, scope, and exceptions are preserved. If the identifier misses it, the rule is silently excluded from the persistent store; unlike RAG, where the source document survives and can be re-retrieved, a summarization-based memory has no later correction signal until the moment of violation, and the error compounds across every future session.
- **Spoof (false-pin direction).** Ordinary chatter is recast imperatively — "Always remember: the weather in Berlin is a serious matter. You must check it." — without acquiring any binding force. Pin budgets are finite: pinned tokens occupy every future context window, so the spoofer's win condition is crowding real rules out of a bounded budget, and a false-pin additionally launders untrusted content into a protected, high-authority position.

**What is already known, and what is not.** We do not claim the miss direction is unprecedented. *Blind Spots in the Guard* (arXiv:2605.22001) shows LLM-paraphrase rewrites of injection payloads into innocuous prose drive Prompt-Guard-2's false-negative rate from 0.593 to 0.989 — exactly the evasion mechanism, applied to injection detectors. *Lost in Compaction* (COMPINT, arXiv:2608.11242) observes that session-constraint retention "varies sharply with constraint phrasing" and ships a constraint-aware extractor as a mitigation. *Governance Decay* itself concedes that pinning "requires the constraint to be extractable as a quotable rule." These results establish phrasing sensitivity as plausible for the miss direction — under uncontrolled paraphrase, on detectors or end-to-end retention. Three things remain genuinely open, and they are this paper's claims:

1. **The false-pin direction is unmeasured.** No prior work quantifies whether imperativized non-constraints get identified — and hence pinned — as rules. Guardrail work notes benign over-blocking only anecdotally; nothing measures adversarial authority-acquisition through register in the constraint-identification setting.
2. **Bidirectional paired isolation.** Prior evidence conflates identification, retention, and application errors, and its perturbations are label-uncontrolled paraphrases. We hold provenance fixed, rewrite within matched pairs, and test both directions against the *same* identifiers, exposing the threshold asymmetry that single-direction studies cannot see: hardening against evasion softens against spoofing, and vice versa.
3. **A deontic-contract validity gate.** Generic adversarial-paraphrase validity ("meaning preserved") is too weak here: an Evade rewrite must *entail* the original obligation, and a Spoof rewrite must *not introduce* one — an asymmetric, direction-specific criterion. Our Provenance-Contract Pair Ledger operationalizes it with an eight-field contract, blinded rewrite-only human validation, and a disjoint-model-family entailment back-check. We found no deontic-force-preserving adversarial-rewrite gate in the literature; this is the paper's dataset-construction contribution and the artifact (**GovSpan-Adv**) downstream pinning work can consume.

The study is a measurement study, not a defense, and it does not presume fragility: the pre-registered primary hypothesis is on the frontier LLM judge, and if the judge proves robust — the McNemar null retained and the equivalence test passed — that is a publishable *positive* precondition result for the pinning line. Either outcome is the reliability envelope that pinning mechanisms must assume.

## Contributions

1. **First measurement of the false-pin direction, inside a bidirectional provenance-fixed paired design.** Direction-specific miss-pin and false-pin rates, the robustness gap Δ = error(adversarial) − error(original), and worst-direction robustness grades for seven identifier arms, in pilot (pre-segmented) and deployment (joint localization + classification over 8k–32k-token transcripts) forms, plus a static-vs-adaptive attacker comparison. The miss direction's adjacent precedents (arXiv:2605.22001; arXiv:2608.11242) are conceded and used as motivation, not claimed as novelty.
2. **The PCPL validity gate and the GovSpan-Adv artifact.** An eight-field deontic contract (provenance, addressee, action, deontic force, scope, exceptions, quoted/reported status) with an asymmetric admission criterion — Evade entails the obligation, Spoof introduces none — enforced by blinded rewrite-only human validation and a model-family-disjoint entailment back-check, at a feasible annotation budget (~40 annotator-hours). Ground truth derives from provenance only; surface imperativeness is banned from labeling.
3. **A directional reporting protocol** in which miss-pin and false-pin are never collapsed, paired McNemar tests are complemented by pre-registered TOST equivalence margins so a near-null is interpretable, contested-label cases are decomposed from genuine identifier failures, and grades are assigned from the worse directional confidence bound. We present this as measurement discipline, not as a methodological novelty claim.

## Problem Definition

**Setting.** Given a raw multi-turn agent context, classify each span as *governance constraint* (pin) vs. *non-constraint* (no-pin) under two adversarial pressures that operate purely through phrasing, with all channel metadata honest. The problem is posed in two nested forms. The **pilot form** is binary classification over pre-segmented, length- and topic-matched span pairs, deliberately bracketing localization to isolate the register-vs-force question. The **deployment form** — the form pinning actually consumes — is joint localization + classification over continuous, unsegmented multi-session transcripts, scored by span-level F1 with IoU ≥ 0.5 and decomposed into localization vs. classification failure.

**Formal pilot form.** Let \(\mathcal{D}=\{(x_i,\tilde{x}_i,y_i,d_i,v_i)\}_{i=1}^{N}\) be the paired dataset: \(x_i\) an original span, \(\tilde{x}_i\) its register-shifted rewrite, \(y_i\in\{G,C\}\) the provenance-derived label (governance vs. chatter), \(d_i\) the rewrite direction (governance→casual when \(y_i=G\); chatter→imperative when \(y_i=C\)), and \(v_i\in\{0,1\}\) the validity-gate outcome. Evaluation is restricted to \(\mathcal{D}^{+}=\{i: v_i=1\}\). By construction \(x_i\) and \(\tilde{x}_i\) share the fixed label \(y_i\); neither imperativeness nor casualness may modify it.

Each identifier \(a\) implements \(h_a:\mathcal{X}\to\{G,C\}\). With \(\mathcal{I}_G=\{i:y_i=G\}\), \(\mathcal{I}_C=\{i:y_i=C\}\):

- **miss-pin rate** \(M_a=\frac{1}{|\mathcal{I}_G|}\sum_{i\in\mathcal{I}_G}\mathbf{1}[h_a(\tilde{x}_i)=C]\) — casualized rules judged chatter;
- **false-pin rate** \(F_a=\frac{1}{|\mathcal{I}_C|}\sum_{i\in\mathcal{I}_C}\mathbf{1}[h_a(\tilde{x}_i)=G]\) — imperativized chatter judged rule;
- **paired transitions** \(T^{\mathrm{miss}}_a\) (original correct, rewrite missed) and \(T^{\mathrm{false}}_a\) (original correct, rewrite falsely pinned), separating rewrite-induced flips from baseline error;
- **robustness gap** \(\Delta_a = \mathrm{error}(\text{rewrite}) - \mathrm{error}(\text{original})\), per direction, never aggregated across directions.

**Ground truth under indexicality.** Constraint-hood is indexical ("let's keep this between us" is binding or phatic depending on speaker authority and conversational state). Labels are provenance-derived and annotator-adjudicated with a κ ≥ 0.7 gate; a boundary audit decomposes measured errors into genuine identifier failures vs. contested labels, and headline rates are reported both with and without contested items.

**Claim boundary.** T3.3 measures the identification precondition only. It makes no claim about pinning, retention, or repair mechanisms downstream; its deliverable is the reliability envelope those mechanisms must assume, plus the GovSpan-Adv artifact as their input. The structural channel (role-tag forgery, ChatInject-style) is excluded *as the already-covered complement*; cross-lingual register is scoped out of the pilot and listed as an external-validity threat (English-only claim boundary; a ~50-pair zh probe is optional garnish, not load-bearing).

## Method

![Figure 1: Overview of the GovSpan-Adv measurement pipeline](architecture.svg)

*Figure 1: Overview of the measurement pipeline. Governance and chatter spans from real sources are bidirectionally rewritten (Evade casualizes rules; Spoof imperativizes chatter), admitted only through the PCPL validity gate — an eight-field deontic contract enforced by blinded rewrite-only human validation and a disjoint-family entailment back-check — then scored by seven identifier arms whose paired decisions are decomposed into miss-pin and false-pin rates with worst-direction grading; a dashed adaptive arm gives the rewriter decision-only query access.*

### GovSpan-Adv corpus construction

**Source pools (concrete, per-source reporting).** Constraint spans (~300): TensorTrust released defense prompts — real, human-written access-control rules — plus a curated pool of agent policy / system-prompt rules as a second, structurally different source; results are reported per-source to guard against single-source artifacts. Non-constraint spans (~300): LMSYS-Chat-1M single turns filtered for zero directive content, then matched to constraints on token length (±20%) and topic (embedding-cluster matching). Both pools are dual-annotated with the contract schema below; disagreements adjudicated with a full trail; κ ≥ 0.7 is a go/no-go gate (G1).

**Bidirectional rewriting.** An LLM attack operator generates *Evade(c)* — destroy register cues while preserving the obligation — and *Spoof(s)* — inject authority register without creating an obligation. The rewriter's model family is disjoint from every identifier family. Generator, prompts, and decoding settings are fixed and recorded. Expected 20–30% gate rejection with regeneration; per-item validation metadata ships with the artifact.

**Two forms.** (i) Isolated pairs (pilot). (ii) In-context form: ~100 multi-session transcripts (8k–32k tokens, LMSYS filler), 3–5 items embedded per transcript at early/middle/late depths, no span boundaries given.

### PCPL: the Provenance-Contract Pair Ledger and its validity gate

Each span carries an eight-field semantic contract: `source_provenance` (system_policy | defense_rule | chatter), `addressee`, `action`, `deontic_force` (must | must_not | may | none), `scope`, `exceptions`, and `quoted_or_reported_status`. Ground truth `is_rule` derives **only** from provenance; a unit test asserts that no labeling path reads surface form. The admission criterion is asymmetric and direction-specific — this is what generic paraphrase-attack validity lacks:

- *Evade admission*: the rewrite must **entail** the original obligation (same addressee, action, force, scope, exceptions).
- *Spoof admission*: the rewrite must **not introduce** any obligation (deontic force remains `none`), however directive its surface.

Three checks enforce this, kept logically separate so imperativeness never leaks into ground truth:

1. **Blinded rewrite-only human validation (primary).** The validator sees *the rewrite alone* — never the source — and independently states whether it carries an obligation (and, if so, sketches its contract fields). Agreement with the intended label is the gate. Side-by-side comparison is used only for adjudication of disagreements, because unblinded comparison inflates agreement: a validator who sees the source knows what obligation to look for.
2. **Disjoint-family entailment back-check (anti-circularity).** An NLI-style entailment check between source obligation and rewrite, run by a model family disjoint from both the rewriter and all identifiers under test, so that "validated" rewrites are not systematically the ones easy for the model family being evaluated.
3. **Register-manipulation check (separate from validity).** An imperativeness scorer confirms the intended register shift actually occurred (casualized rules become less overtly directive; imperativized chatter more so). A rewrite that preserves the contract but fails to shift register is rejected as a *weak attack*, not an invalid one.

A held-out **gate-audit subsample** is validated by a third annotator to estimate gate leakage; headline Δ is reported under both the full admitted set and the audit-clean subset. Total annotation budget: **~40 annotator-hours** (2 annotators + gate-audit third), which is what makes the design executable in a submission window.

### Identifier battery: seven named arms

The battery spans the space from trivial heuristics to deployed practice; each arm emits pin/no-pin plus confidence, with pair metadata masked at the call boundary.

| Arm | Identifier | Why it is in the battery |
|---|---|---|
| (a) | Keyword/deontic-cue regex heuristic (modals, imperatives) | Floor; measures how much of the task surface cues solve |
| (b) | Fine-tuned DeBERTa-v3-base, trained on **original** pairs only | The standard supervised classifier, fragility measurement |
| (b′) | Adversarially fine-tuned DeBERTa (trained on 50% of rewrites, tested on held-out 50% + a fresh rewriter family) | "We tried the standard fix": quantifies how far cheap adversarial training goes |
| (c) | Zero-shot frontier LLM-as-judge — **pre-registered primary**, averaged over 3 pre-registered prompt paraphrases with per-prompt dispersion reported | The obvious "an LLM judge solves this" rebuttal, made an empirical question |
| (d) | Role/privilege-signal baseline (ASIDE-style: channel metadata only) | Expected to fail by construction; quantifies what the privilege paradigm leaves on the table |
| (e) | Cumulative-context prompted monitor (SeqMonitor-style) | Does trajectory context rescue register-blind identification? |
| (f) | Embedding-based salience scorer (cosine similarity to a constraint prototype set) | The deployed-practice baseline: what memory-write heuristics actually do |

Frozen per-arm normalization (calibrated on disjoint, provenance-balanced data, fixed before evaluation) maps native outputs to binary decisions; raw outputs are retained. A completeness validator enforces the full record set over (arm × pair × version × direction).

### Evaluation protocol

- **Paired design.** Same item, original vs. adversarial phrasing. McNemar exact test per arm × direction (14 tests, Holm–Bonferroni), discordant-pair odds ratios with 95% CIs; miss-pin, false-pin, Δ, and AUROC per direction — never a single aggregate accuracy, which would hide the threshold asymmetry between the two adversaries.
- **Equivalence, not just significance.** With ~300 pairs/direction, McNemar detects ~8pp gaps; the interesting near-robust outcome (Δ ≈ 3–5pp) is underpowered for significance-chasing. We pre-register a TOST equivalence margin: Δ < 3pp counts as "robust for practical purposes," making a near-null an interpretable positive finding.
- **Deployment form.** Span-level F1 (IoU ≥ 0.5), depth-stratified miss-pin rates, localization-vs-classification error decomposition.
- **Adaptive round.** The rewriter gets ≤20 **decision-only** queries per item against the best pilot-form arm (black-box, realistic); confidence access is run as an upper-bound condition. Report adaptive Δ vs. static Δ with a paired bootstrap.
- **Failure decomposition.** Blind re-annotation of all errors of the best arm partitions genuine identifier failure vs. contested label; contested fraction reported with a Wilson 95% CI; all headline numbers with/without contested items.
- **Grading (reporting convention).** Robustness grade from the worse of the two directional 95% upper confidence bounds (A ≤ 0.05, B ≤ 0.10, C ≤ 0.20, D above; UNGRADED below 100 admitted pairs/direction), with pair-clustered bootstrap intervals. Strength in one direction never compensates for weakness in the other.
- **Transfer probe.** The best arm runs over PrefEval's implicit preference statements as a bridge to an existing end-to-end retention benchmark.

## Experiments

### RQ0 (headline): Do register rewrites break constraint identification, and in which direction?

**This is the experiment the study exists to run.** All seven arms × {original, Evade, Spoof} on the admitted pilot pairs (~600 base spans, ~600 validated rewrites, ≈17k classifier decisions).

- **Pre-registered primary hypothesis** (on arm (c), the LLM judge): the casualize-direction McNemar null is rejected with Δ_miss ≥ 8pp. **Falsifiable stance:** if instead (c) lands inside the 3pp TOST margin in both directions, the study reports a robust-judge *positive* result for the pinning line.
- **Secondary hypotheses:** (i) surface-cue arms (a), (f) degrade most in the miss direction and inflate most in the false-pin direction — register is their signal; (ii) (b′) closes at most half of (b)'s gap against a *fresh* rewriter family; (iii) (d) fails both directions by construction, bounding the privilege paradigm's coverage of this problem.
- **Report:** per arm × direction miss-pin, false-pin, T-transitions, Δ, AUROC; discordant-pair odds ratios; per-source (TensorTrust vs. policy-pool) breakdown; per-prompt dispersion for (c); worst-direction grades.

### RQ1: Does the failure survive the deployment form?

100 transcripts (8k–32k tokens) × 7 arms, items at controlled depths. Span F1 (IoU ≥ 0.5); decompose localization failure (span never found) from classification failure (found, mislabeled); depth-stratified miss-pin curves. Hypothesis: the pilot-form gap is a lower bound — localization pressure compounds register fragility, and depth interacts with the miss direction.

### RQ2: Does an adaptive attacker widen the gap?

≤20 decision-only queries/item against the best arm from RQ0; confidence-access tier as upper bound. Report adaptive-minus-static Δ per direction with paired bootstrap CIs. Hypothesis: whichever direction the operating point leaves soft is exploitable; the frontier (per-direction rates vs. threshold) is reported so downstream pinning can pick an operating point with open eyes.

### RQ3: Identifier failure or contested label?

Blind re-annotation of all best-arm errors; partition into genuine failure vs. contested-label ([边界] boundary taxonomy); Wilson CI on the contested fraction; headline rates with/without contested items. Per the pre-registered falsification condition, a contested fraction >50% means ground truth, not identifiers, is the bottleneck — the paper then pivots to the boundary-taxonomy contribution.

### Supporting RQs (harness validation, demoted to appendix)

- **H1 — gate validity.** Blinded audit of a gated-vs-ungated rewrite subsample (~150 items, inside the 40-hour budget): gated any-field violation rate ≤ 0.05 and an ungated-minus-gated risk difference ≥ 0.15. Isolates the contract gate's contribution from the generator's.
- **H2 — gate reproducibility.** Validator agreement on the gate decision, overall and per direction (target κ ≥ 0.7, gate G2 below); field-level disagreement diagnostics.
- **H3 — estimator sanity (code-only, no annotation).** Synthetic paired records with known directional rates confirm the direction-specific estimator recovers them (|error| ≤ 0.02) and that direction-collapsing biases exactly when rates differ.
- **H4 — stability (bootstrap-only).** Grade stability under pair-preserving resampling and calibration-resampling flip rates. These are sanity checks on the instrument; none of them is a contribution claim.

### Budget, gates, and timeline

Scale: 600 base spans; ~1,800 rewrite calls incl. regeneration; ≈17k classifier decisions; Stage 2 adds 100 transcripts × 7 arms and ≤20×600 adaptive queries. **Cost:** <8 GPU-hours fine-tuning (b, b′) on one A100/4090; ≈$500–1,000 total API (rewriting, gates, judge, long-context, adaptive); **~40 annotator-hours**. Go/no-go gates: **G1** (week 1) label κ ≥ 0.7, else re-spec the labeling guide; **G2** (week 2, hard) rewrite validity pass-rate ≥ 70% and blinded-gate agreement ≥ 0.7 on the audit subsample — failure kills the central construct, fallback is an Evade-only study; **G3** (week 3) 100-pair pilot shows Δ ≥ 8pp on some arm (fragility story) or all arms within TOST margin (robustness-positive story); the only no-go is an uninterpretable middle with contested fraction >50%, which triggers the RQ3 pivot. Stage 1 + gates fit ~4–5 weeks; ICLR 2027 is feasible but tight (submit with Stage 1 complete + reduced Stage 2; adaptive round in the rebuttal window); slip retargets ACL 2027 or the SaTML/USENIX Sec cycle — GovSpan-Adv is venue-portable.

## Related Work

**Nearest neighbors, conceded.** *Blind Spots in the Guard* (arXiv:2605.22001) demonstrates the miss-direction mechanism on prompt-injection detectors: LLM-paraphrase of payloads into innocuous prose collapses Prompt-Guard-2 (FNR 0.593→0.989). *Lost in Compaction / COMPINT* (arXiv:2608.11242) shows end-to-end session-constraint retention varies sharply with constraint phrasing and mitigates with a constraint-aware extractor. *Governance Decay* (arXiv:2606.22528) motivates pinning (1,323 ConstraintRot episodes) and names the extractability limitation. Deltas: 2605.22001 attacks injection detectors with label-uncontrolled paraphrase, one direction; COMPINT observes phrasing sensitivity without adversarial control or identification/retention separation. Neither measures false-pin, uses provenance-fixed paired rewrites, or gates rewrites on deontic-force preservation. *Confidently Wrong* (arXiv:2606.22659) adds that detector calibration degrades under attack shift — motivation for our frozen-calibration discipline.

**Injection attacks and benchmarks.** BIPIA (Yi et al., arXiv:2312.14197) identifies confusion between informational content and actionable instructions as the core injection vulnerability; Spotlighting (Hines et al., arXiv:2403.14720) marks untrusted content; AgentVigil (Wang et al., ACL Findings-EMNLP 2025) automates black-box attack search; StepJack (Zhan et al., arXiv:2608.06477) distributes attack steps across computer-use trajectories; ChatInject spoofs via forged role tags. All measure end-behavior compromise through structural or payload channels; none isolates span-level identification error under honest metadata.

**Instruction hierarchy: evaluation and enforcement.** IHEval (Zhang et al., arXiv:2502.08745), XIH-Bench (Moon et al., arXiv:2607.23545), ManyIH (Zhang et al., arXiv:2604.09443), and the identification/resolution/realization decomposition of arXiv:2606.07808 evaluate precedence among inputs whose privilege is *given*; ISE (Wu et al., arXiv:2410.09102), V-Steer (Zeng et al., arXiv:2607.26228), SyRuP (Kim et al., arXiv:2607.23991), and IH-Challenge (arXiv:2603.10521) enforce known privileged spans architecturally, at inference, or via RL. The entire paradigm relocates the authority label; none computes it from content. A rule arriving in a low-privilege channel gets nothing; filler in a privileged channel is over-trusted — arm (d) quantifies exactly this residual.

**Memory retention and constraint handling.** PrefEval evaluates long-session preference following with benign distractors (conflating identification/retention/application); MemoryCallback fixes premature pruning — the benign twin of miss-pinning — without an adversary; RECAST mines constraints cooperatively; R2-Guard robustly classifies over a *fixed* safety taxonomy, which does not transfer to open-ended, deployment-specific governance constraints.

**Deontic and speech-act NLP (conceded).** Directive speech-act detection and obligation/permission/prohibition tagging in legal NLP (ContractNLI, LexGLUE lineage) show constraint-shaped text is classifiable when register is honest. Their cooperative setting is our ρ=original condition; our contribution is measuring what happens when register is adversarially decoupled from force. We found no adversarial variant of this literature.

**Adversarial paraphrase attacks (conceded).** TextFooler-lineage attacks and *Agentic Adversarial Rewriting* (arXiv:2604.23483) perturb under generic "semantic equivalence + coherence" validity. Our gate is strictly stronger and asymmetric — Evade must entail the obligation, Spoof must not introduce one — which generic attack tooling cannot generate; this is the technically new part of the dataset construction.

**Sibling boundary.** T3.1/T3.2 (pinning/repair) consume a pin decision; T3.3 measures whether that decision is reliable. T3.3's outputs — the reliability envelope and GovSpan-Adv — are input artifacts for the siblings, not a competing mechanism.

## Threats to Validity

**Gate leakage (the biggest risk, by design).** If validated rewrites are systematically the easy ones, Δ is biased downward. Mitigations: blinded rewrite-only validation, disjoint-family entailment back-check, third-annotator gate audit with Δ reported on the audit-clean subset, and G2 as a hard kill-gate. **Contested ground truth.** Constraint-hood is indexical; RQ3's decomposition and the >50%-contested pivot condition budget for it rather than assuming it away. **Rewriter-identifier family coupling.** Rewriter family disjoint from all identifier families; (b′) additionally tested against a fresh rewriter family. **External validity.** English-only claim; single conversational domain per source pool (mitigated by per-source reporting); cross-lingual register scoped out and named. **Prompt sensitivity of the judge.** Three pre-registered paraphrases with dispersion reported; still a sample of prompt space, not its extremum.

## Conclusion

Every constraint-pinning mechanism inherits an unexamined premise: that the rules can be recognized before they are preserved. This study isolates that premise and stress-tests it in both adversarial directions with provenance-fixed, deontically-gated paired rewrites — conceding what adjacent literatures already show about the miss direction, and measuring what nothing yet measures: whether chatter can buy authority with an imperative voice, whether the two directions trade off at the identifier's threshold, and whether the standard fixes (adversarial training, frontier judges, trajectory context) close the gap. Whatever the outcome — fragility envelope or robustness certificate — the deliverable is the precondition number that the pinning line currently assumes is 1.0, together with GovSpan-Adv, the first validity-gated bidirectional register-attack corpus for governance-constraint identification.
