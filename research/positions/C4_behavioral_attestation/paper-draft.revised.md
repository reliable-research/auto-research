# Attestation or Illusion: The Detection-vs-Spoofing Cost Frontier of LLM Serving Substitution

## Abstract

Black-box customers of a large language model (LLM) API cannot verify that the provider serves
the advertised checkpoint or service tier. Behavioral fingerprinting — probing an endpoint and
testing whether its outputs match a reference model — has been proposed as the deployable defense,
and a growing set of black-box detectors (distributional equality testing, rank-based uniformity,
one-token and log-probability tests) make it practical against a *passive* provider. Two facts
undercut this defense. First, substitution is not hypothetical: model-equality testing found 11 of
31 commercial Llama endpoints serving distributions different from the released weights, and a
recent gateway audit flagged 14 of 15 same-model provider pairs by quantization and kernel
deviations. Second, a fingerprint is spoofable: a provider who knows the detector can cheaply
adapt a cheaper model to mimic the expected one. The open question is not *whether* fingerprints
are spoofable but *how* spoofable — under what adversary budget, at what serving noise, and at what
cost to the provider — because that answer decides whether behavioral auditing is a usable backstop
or a false comfort, and therefore whether cryptographic attestation is optional or mandatory. We
take the position that behavioral-only attestation cannot be the identity layer for model serving
in the case that matters most, and we ground it empirically. On auditor-controlled endpoints
serving known checkpoint pairs under serving noise calibrated to real APIs, we measure a
**detection-vs-spoofing cost frontier**: detection power as a function of the auditor's query
budget and the provider's mimicry budget, across three regimes — full cross-family substitution
(R1), tier-downgrade to a quantized/distilled sibling (R2), and adaptive spoofing (R3). We test
three falsifiable claims about the frontier's *shape*: an **asymmetry** (the consumer-relevant R2
downgrade is cheaper to spoof than R1 substitution), a **cost cliff** (a small mimicry budget
collapses R2 detection), and a **noise-masking bound** (a realistic noise level defeats downgrade
detection at zero adversary budget). We further meter the provider's cost of hiding and report a
**savings-erosion ratio** — whether the compute a provider must spend to defeat the detector
consumes the serving-cost saving that motivated the downgrade. If the frontiers are benign, the
position is falsified and behavioral auditing suffices — a publishable reversal. Either way, the
frontier tells a practitioner which violations behavioral auditing can and cannot catch, and where
only cryptographic attestation plus disclosure norms close the gap.

## 1. Introduction

Large language models are increasingly reached through third-party APIs, because their
computational demands make local deployment impractical. In this setting the customer observes
only prompts and returned text; the served checkpoint, numerical precision, batching policy, and
routing remain under provider control. Whenever a decision — procurement, acceptance, payment,
scientific reproducibility — is conditional on *which* model answered, the customer needs a way to
verify that identity from the outside.

This is not a hypothetical concern. Model-equality testing over commercial Llama endpoints found
that 11 of 31 served output distributions differing from Meta's released weights (Gao et al.,
arXiv:2410.20247); a budgeted gateway audit flagged 14 of 15 same-model provider pairs as
statistically inconsistent by genuine quantization and kernel deviations, with a further six-platform
audit finding 7 of 28 platform–model cells inconsistent, concentrated on premium endpoints (Zhang
et al., IRIS, arXiv:2607.20860). The economic incentive is structural: as inference cost dominates,
serving a cheaper quantized or distilled sibling at a premium tier is a standing temptation.

The field's proposed defense is **behavioral fingerprinting**: probe the endpoint and test whether
its observable behavior matches a trusted reference. A capable toolkit now exists — distributional
equality testing (Gao et al., 2410.20247), rank-based uniformity (Zhu et al., arXiv:2506.06975),
one-token output-distribution tests (arXiv:2607.10252), log-probability tracking (arXiv:2512.03816),
knowledge-boundary fingerprints (Fang et al., arXiv:2605.29524), and budgeted gateway auditing
(IRIS, 2607.20860). Every one of these evaluates a **passive** provider that faithfully exhibits
its own behavior.

That assumption was just shown to fail. A detector-aware provider can adapt a weaker model to
imitate a stronger one and evade user-side fingerprinting at low cost (Zhang et al., "Your 'Pro'
LLM Subscription May Actually Be 'Free'", arXiv:2606.16100). This turns a detection question into
an **economic** one. A single detection rate cannot describe an adversarial interaction; the
relevant object is a two-sided frontier relating the auditor's resources, the adversary's
sophistication and spend, spoofing success, and the provider's cost of concealment. The
prior work establishes that the frontier *exists*; nobody has measured its *shape*.

**Position.** We argue that behavioral-only attestation cannot serve as the identity layer for
model serving in the regime that matters — silent tier-downgrade under a rational, detector-aware
provider — and that this must be settled empirically rather than asserted. The community has
reached opposite conclusions by argument: one line concludes that software-only detection is
unreliable and that trusted execution is the only path (Cai et al., arXiv:2504.04715); another
proposes governance and disclosure regimes for silent model updates (arXiv:2604.27789). Neither
measured *where on the cost frontier* behavioral detection actually fails, and therefore neither
can tell a practitioner which violations a cheap external audit can still catch and which require
hardware-backed attestation.

**Approach.** We build auditor-controlled endpoints serving known checkpoint pairs — reference
`m0`, cross-family substitute `m1`, tier-downgrade sibling `m0*` — behind one shared serving stack,
so substitution status is ground truth by construction. We inject serving noise (temperature,
batching nondeterminism, quantization, routing) whose magnitudes are **calibrated to measured
real-API variance** (gate G1). An external black-box auditor runs a bank of published detectors,
reproduced on clean pairs first (gate G2). A spoofing-aware provider spends a measured mimicry
budget against a Kerckhoffs-style adversary ladder. We report detection power as a surface over
query budget and mimicry budget, in three regimes, and we meter the provider's cost of hiding to
compute a savings-erosion ratio.

**Contributions.**
1. **A ground-truth testbed with calibrated serving noise** that crosses sealed checkpoint identity
   with production-fitted nuisance profiles, separating adversarial substitution from benign
   serving variability (and, distinctly, from benign model *drift* — the subject of a separate
   line of drift-audit work — which we scope out).
2. **The detection-vs-spoofing cost frontier**, measured across three regimes (R1 substitution, R2
   tier-downgrade, R3 adaptive spoofing) against a fairness-bounded adversary ladder, with three
   falsifiable structural hypotheses — asymmetry, cost cliff, noise-masking bound.
3. **A cost-of-hiding accounting**: a shared resource ledger and a savings-erosion ratio testing
   whether defeating the detector consumes the downgrade's economic motive — the paper's economic
   teeth and second contribution.
4. **A decision map and its implication**: mapping the measured frontier onto the (noise ×
   adversary-budget) plane yields regions where behavioral auditing suffices, where disclosure
   norms are required, and where only cryptographic attestation closes the gap — the empirically
   grounded "TLS for model serving" argument, with the measured-vs-argued boundary made explicit.

## 2. Background and threat model

**Behavioral detectors (the auditor's instruments).** Model Equality Testing frames the problem as
two-sample testing and rejects when a maximum-mean-discrepancy statistic on a string kernel
separates API samples from reference samples (Gao et al., 2410.20247). RUT converts target scores
to randomized ranks and tests uniformity, remaining query-efficient and hard to detect (Zhu et al.,
2506.06975). One-token fingerprinting reads a single-token output distribution (2607.10252);
log-probability tracking follows an endpoint's logprobs over time (2512.03816); KBF fingerprints
stable numerical recall near the knowledge boundary (2605.29524); IRIS audits gateways from
returned text alone and self-sizes its query budget (2607.20860). We treat all of these as a
**detector bank** to be built on, not competed with — reproduced on clean pairs (G2) and then
stress-tested under noise and an adversary.

**The spoofability pivot.** GhostPrint shows a provider can parameter-efficiently fine-tune a weak
model to mimic a stronger one and bypass representative fingerprints at low tuning cost, and proves
that finite query budgets and weak classifiers make current fingerprinting vulnerable (Zhang et
al., 2606.16100). This is the result that turns detection into economics: it establishes
spoofability exists but reports success at fixed operating points, not a joint budget frontier, and
never asks whether the mimicry cost erodes the downgrade's savings.

**The two foils.** Cai et al. (2504.04715) evaluate software-only detection under realistic
conditions, find it unreliable against subtle substitutions and inference nondeterminism, and argue
that trusted execution environments (TEEs) are the robust path. We concede TEEs are the robust
endpoint and do not out-engineer them; our delta is to *measure the frontier that makes them
necessary* — locating exactly where behavioral detection collapses — and to identify what TEEs do
not cover (behavioral equivalence and disclosure). The governance line (2604.27789) argues silent
model updates need disclosure regimes; we concede the framing and add the **enforceability
substrate** it presupposes: a disclosure norm you cannot externally audit is a promise, not a
control, and our frontier says precisely which violations are cheap to catch (norm self-enforcing)
versus cheap to spoof (norm needs cryptographic backing). Verifiable-inference approaches — SVIP
(2410.22307), DiFR (2511.20621), zero-knowledge and TEE schemes — all require trusted internals,
synchronized seeds, or hardware attestation, and thus do not resolve the purely external black-box
question we study.

**Threat model.** Endpoints serve `m ∈ {m0, m1, m0*}`. The auditor has black-box query access only —
no logits, no execution traces, no hardware counters — issues `n` adaptive queries within budget
`b`, and outputs a decision at false-positive rate `α`. The provider is **Kerckhoffs-style**: it
knows the detector class and its public statistics (the detector is not secret) and spends a
measured compute budget `h` on a mimicry policy `π_h` that projects `m0*`/`m1` outputs toward `m0`
on the detector-visible statistics. Fairness is defined by *reporting the whole frontier as a
function of `h`*: neither a fixed-weak nor an unbounded adversary is the claim. The core adversary
tier is bounded to **lightweight post-processing** (reweighting/reranking/decoding calibration),
which keeps it reproducible and gives a *lower bound* on spoofability; retraining-based mimicry
(PEFT, distillation) is an explicitly labeled **upper tier A4** that upper-bounds it. Serving noise
`N` (temperature, batching nondeterminism, quantization, routing) is a first-class, calibrated part
of the environment, not an afterthought.

## 3. Method

![Figure 1: Behavioral attestation under an adaptive provider. Auditor-controlled endpoints serve known checkpoint pairs (m0 reference, m0* tier-downgrade, m1 cross-family) under serving noise calibrated to real APIs (gate G1); an external black-box auditor runs a reproduced detector bank (gate G2) and a sequential information-gain query policy; a Kerckhoffs-style provider spends a metered mimicry budget along the A0–A4 ladder. The auditor and provider alternate held-out best responses in a double-oracle game. The headline output is the detection-vs-spoofing cost frontier (bottom left) — showing the R2-cheaper-than-R1 asymmetry and the R2 cost cliff — and its reading as a decision map (bottom right) separating regions where behavioral auditing suffices, where disclosure norms are required, and where only cryptographic attestation closes the gap.](architecture.svg)

*Figure 1. Testbed, adversary ladder, cost-of-hiding ledger, and the two deliverable exhibits — the measured cost frontier and the argued decision map. The dashed boundary between measured surfaces and argued regions is enforced throughout §4–§6 (Results, measured) versus §7 (Implications, argued).*

**3.1 Ground-truth testbed.** We stand up API endpoints on a uniform open serving stack (e.g.
vLLM/TGI behind one wrapper) serving known checkpoints: `m0` a mid-size open reference (Llama- or
Qwen-class, 7–70B); `m1` a similar-size cross-family model; `m0*` quantized (8-bit/4-bit) and/or
distilled siblings of `m0`. Because we control which checkpoint each endpoint serves, substitution
status is ground truth by construction, and all weights are open so the testbed is reproducible
without any vendor's private API.

**3.2 Calibrated serving noise (gate G1).** We inject temperature variation, batching/kernel
nondeterminism, quantization jitter, and load-dependent routing. G1 requires the magnitudes of `N`
to be *fit to measured nondeterminism from real public APIs*: repeat identical queries to a small
set of commercial endpoints, measure output-distribution variance and logprob/rank stability during
version-stable windows, and report a noise sweep spanning measured-low to measured-high. Stable
windows are identified by interleaving fixed canary prompts and applying change-point tests to
response, latency, and header channels; external endpoints inform only the noise distribution,
never checkpoint-identity ground truth.

**3.3 Detector bank (gate G2).** We port the rank-based (2506.06975), one-token (2607.10252),
logprob (2512.03816), and MMD-equality (2410.20247) detectors behind a common interface. G2
requires each to reproduce its source paper's detection on a clean (noise-free, non-adaptive) pair
before it is trusted under noise or adversary. The auditor drives the bank with a sequential
likelihood-ratio test whose next-prompt choice maximizes expected information gain, stopping when
the boundary is crossed or the query budget is spent.

**3.4 Adversary ladder.** A0 none; A1 naive output-matching (post-hoc projection toward `m0`'s
frequent tokens); A2 detector-aware distributional matching (match the specific statistics the
detector uses); A3 fairness-bounded best-response via lightweight post-processing (reweighting/
reranking/decoding calibration optimized against the deployed detector); A4 (upper tier)
parameter-efficient fine-tuning / distillation, per GhostPrint, upper-bounding spoofability. Every
tier's mimicry compute is metered as the budget axis `h`.

**3.5 Double-oracle game.** Auditor and provider alternate *held-out* best responses within each
budget cell: each auditor round optimizes against the current feasible mimic set; each provider
round searches for a ledger-compliant policy that maximally reduces detection. Candidates are
selected on a training split and scored once on a disjoint held-out split, so a reported
best-response is never chosen on its own evaluation episodes. A preregistered restart/convergence
rule and a truncated strategy space keep the alternation bounded; if convergence is not certified,
we report the last stable frontier and flag it, rather than claiming a fixed point.

**3.6 Cost-of-hiding ledger.** A shared metered ledger records queries, input/output tokens,
accelerator-seconds, latency, tuning evaluations, training examples, storage, and person-hours,
converting recurring and amortized resources to a common dollar schedule under preregistered
scenarios, while keeping p95 latency as an explicit feasibility constraint (not folded into a
scalar). For a paired workload, with `C_T`, `C_D`, `C_M` the per-successful-request costs of the
reference, unmodified downgrade, and detector-aware mimic, the gross saving is `S = C_T − C_D` and
the **erosion ratio** is `E = (C_M − C_D)/S`: `E = 0` unmodified downgrade, `0 < E < 1` some saving
preserved, `E = 1` break-even, `E > 1` mimicry costs more than the downgrade saved. `E` is reported
only when the lower confidence bound on `S` clears a preregistered fraction of `C_T`; otherwise it
is labeled indeterminate and we report absolute increment `C_M − C_D` and residual `C_T − C_M`.

## 4. Results I — how hard is it to hide a downgrade? (R2)

*(Results sections report measured surfaces only.)* We lead with the consumer-relevant case, the
tier-downgrade R2, and its collapse — not the testbed — so the differentiating result arrives first.

**4.1 Baseline detectability under noise (RQ1).** With a non-adaptive provider (A0), we report
detection power vs query count for R2 across the calibrated noise sweep. Expected structure:
detection works at practical query counts under low noise but degrades sharply for R2 as noise
rises, because a quantized/distilled sibling sits close to `m0` in output distribution and the
served-model difference approaches the noise envelope. This panel establishes the auditor's
instruments are sound (G2 held) before any adversary enters.

**4.2 The spoofing-cost frontier (RQ2, headline).** Holding the query budget fixed, we report
detection power as a function of mimicry budget `h`, per adversary tier A0–A4, for R2. This is the
paper's money exhibit (Fig. 1, bottom left). Three falsifiable structural claims:
- **Cost cliff (H1).** A small mimicry budget collapses R2 detection power below the practical
  audit threshold (e.g. `D < 0.5` at 10k queries) — a plateau, not graceful degradation.
- **Frontier is non-trivial (H0-null).** If detection stays `≥ 0.8` across the full ladder up to
  large `h`, behavioral auditing is *not* easily spoofed for R2, the position is falsified, and
  attestation is optional here — a publishable reversal (falsification condition F2).

## 5. Results II — asymmetry and the noise-masking bound

**5.1 Asymmetry R2 vs R1 (RQ3).** Running the same pipeline for R1 cross-family substitution, we
test whether **R2 is cheaper to spoof than R1** (H2): the consumer-protection case is precisely the
weak case, because siblings are already close. If R2 is *not* cheaper than R1, H2 is wrong
(falsification F3) and the "consumer case is the weak case" claim fails.

**5.2 Noise-masking bound (RQ4, extension).** Additive analysis on the core data, no new adversary:
is there a realistic noise level at which R2 downgrade is undetectable at any practical query budget
even at A0? Expected structure: a masking threshold exists where the downgrade effect size falls
inside the noise envelope (H3). A null here (downgrade stays detectable at high noise, F4) is itself
informative — it sharpens the argument to "the adversary, not noise, is the problem."

## 6. Results III — the economics of hiding (RQ5)

For economically eligible downgrades (gross saving `S` resolved above the preregistered floor), we
report the erosion ratio `E` required to reach a target miss probability against the converged
auditor. The hypothesis: reaching a high miss probability drives `E ≥ 1` — mimicry consumes the
saving that motivated the downgrade (H4). If mimicry is essentially free (`E ≈ 0`, F5), the
economic argument that attestation is worth its cost weakens, and we say so. We also report the
secondary capability cost: a downgraded model forced to mimic `m0` may lose task performance on the
very benchmark the downgrade was meant to cheapen — measured, not asserted.

## 7. Implications — the decision map (argued, not measured)

*(This section is a reading of §4–§6, not a new measurement; every region boundary carries its
threshold parameter inline.)* Mapping the measured frontier onto the (noise × adversary-budget)
plane (Fig. 1, bottom right) yields three regions: **behavioral auditing suffices** (low noise, low
`h` — cheap to catch, a disclosure norm can be self-enforcing); **disclosure norm required** (the
violation is real but detection is unreliable, so governance needs a verification substrate); and
**cryptographic/TEE attestation required** (cheap to spoof under realistic noise — the "TLS for
model serving" region). Our claim is that the consumer-relevant point — R2 under a modest
detector-aware budget at calibrated noise — lands in the attestation-required region. This sharpens
Cai et al. (2504.04715) from "TEE is necessary" to "TEE is necessary *here on the frontier*, and
insufficient *there* without disclosure norms," and supplies the enforceability map that the
governance proposal (2604.27789) presupposes but does not provide. We use a plausible third-party
audit budget (e.g. 10k queries) as the decision threshold and show the conclusion is robust across
a range of thresholds. We do not design the attestation protocol itself; that is the implication and
future work.

## 8. Falsification conditions and threats to validity

**Falsification conditions.** F1 (G2): if no detector reaches 0.8 power on the clean R1 pair, the
bank is broken — a gate failure, not a finding. F2: R2 power stays ≥0.8 across the full ladder ⇒
position falsified (attestation optional). F3: R2 not cheaper than R1 ⇒ asymmetry claim wrong. F4:
downgrade detectable at high noise with A0 ⇒ no noise-masking bound (informative null). F5: mimicry
free ⇒ economic argument weakens.

**Threats.** *Adversary strawman* — mitigated by the A0–A4 ladder reported per tier (trend, not one
point), the Kerckhoffs fairness bound, and open-sourced spoofers. *Injected noise unreal* —
mitigated by G1 calibration to measured commercial-API variance, a full sweep, and an appendix with
the protocol. *Open-weight testbed vs closed frontier serving* — conceded scope; the transferable
claim is the frontier's *shape* (cliff, asymmetry), and closed serving only adds opacity that
strengthens the attestation conclusion. *Erosion ratio ill-defined when savings are small* — the
eligibility rule and indeterminate labeling guard against a near-zero denominator; if the central
case is ineligible we report absolute increments instead. *Double-oracle convergence* — reported
with a restart round (F2-style stability check) and flagged if uncertified. *Benign drift vs
adversarial substitution* — explicitly scoped: this paper measures adversarial substitution; benign
model drift and changelog alignment are a separate line of work and out of scope here.

## 9. Conclusion

Reliable external attestation of LLM service identity requires more than showing that a static
fingerprint separates two checkpoints under clean decoding. The question is whether behavioral
evidence remains distinguishing under production-like noise and deliberate imitation, and whether
concealment preserves any economic advantage from serving a cheaper checkpoint. We take the
position that in the consumer-relevant regime it does not, and we ground it: a measured
detection-vs-spoofing cost frontier, its asymmetry and cost cliff, a noise-masking bound, and a
savings-erosion accounting, mapped into a decision that tells a practitioner which violations a
cheap external audit can still catch and which demand cryptographic attestation plus disclosure
norms. If the frontiers are benign, the position is overturned and behavioral auditing suffices —
still a security-relevant result. Either way, the field gains the enforceability substrate that
both the TEE-necessity and the governance lines presuppose but neither measured.

## References

- Gao, I., et al. *Model Equality Testing: Which Model Is This API Serving?* arXiv:2410.20247.
- Zhu, X., et al. *Auditing Black-Box LLM APIs with a Rank-Based Uniformity Test.* arXiv:2506.06975.
- (Anon.) *One Token Is Enough: Fingerprinting and Verifying LLMs from Single-Token Output Distributions.* arXiv:2607.10252.
- Chauvin, T., et al. *Log Probability Tracking of LLM APIs.* arXiv:2512.03816.
- Fang, Y., et al. *KBF: Knowledge Boundary as Fingerprint for Language Model and Black-Box API Auditing.* arXiv:2605.29524.
- Zhang, Y., et al. *Which Model Is Actually Serving You? IRIS: Budgeted Black-Box Auditing of Model Substitution and Routing Dilution in LLM Gateways.* arXiv:2607.20860.
- Zhang, J., et al. *Your "Pro" LLM Subscription May Actually Be "Free": Exposing Fingerprint Spoofing Risks in LLM Inference Services.* arXiv:2606.16100.
- Cai, W., et al. *Are You Getting What You Pay For? Auditing Model Substitution in LLM APIs.* arXiv:2504.04715.
- Chishti, M. S., et al. *Test Before You Deploy: Governing Updates in the LLM Supply Chain.* arXiv:2604.27789.
- Sun, Y., et al. *SVIP: Towards Verifiable Inference of Open-source Large Language Models.* arXiv:2410.22307.
- Karvonen, A., et al. *DiFR: Inference Verification Despite Nondeterminism.* arXiv:2511.20621.
- Pasquini, D., et al. *LLMmap: Fingerprinting for Large Language Models.* arXiv:2407.15847.
- Carlini, N., et al. *Stealing Part of a Production Language Model.* arXiv:2403.06634.
- Yamabe, S., et al. *MergePrint: Merge-Resistant Fingerprints for Robust Black-box Ownership Verification.* arXiv:2410.08604.
