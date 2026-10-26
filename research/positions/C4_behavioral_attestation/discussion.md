# C4 — "Model serving needs verifiable identity attestation" — Structured Research Discussion

> **Full-paper framing (position = the paper's stance, not a position-track submission).**
> This document develops C4 as a FULL experimental paper for a security/ML research track.
> The stance — model serving needs verifiable identity attestation, a "TLS certificate for
> model serving," and behavioral-only fingerprinting cannot be that layer because it is
> spoofable — is the paper's framing. The contribution is an implementable black-box
> detection experiment with ground truth by construction: an external auditor probes API
> endpoints WE control that serve known checkpoint pairs, measuring detection under
> realistic serving noise AND under a spoofing-aware adversary, i.e., mapping the
> detection-vs-spoofing-cost frontier — the unclaimed empirical gap. Composes with topic
> B3.3 (probe-set machinery).

**Thesis (stance).** Benchmark results and served behavior are decoupling: vendors can and
documentedly do serve checkpoints differing from what was evaluated (LMArena Llama-4
special variant #2→#32 on retest; undisclosed tier-dependent behavior changes). Behavioral
fingerprints are spoofable by a motivated provider (arXiv:2606.16100), and TEEs alone don't
create disclosure norms (arXiv:2504.04715). The field needs verifiable model-identity
attestation as a protocol/norm layer — but whether black-box behavioral auditing can serve
even as a *detection* backstop under realistic noise and an adaptive adversary is an open
empirical question this paper answers.

**Contribution shape (full paper).** (C1) A controlled testbed: auditor-controlled API
endpoints serving known checkpoint pairs (genuine vs substituted/downgraded), instrumented
with realistic serving noise (temperature, batching/kernel nondeterminism, quantization,
load-dependent routing). (C2) Detection results: can an external black-box auditor detect
substitution/tier-downgrade under that noise, and at what query cost / statistical power?
(C3) The core novelty — a **detection-vs-spoofing-cost frontier**: against a spoofing-aware
adversary who mimics the genuine model's fingerprint (per 2606.16100), how does detection
power trade off against the adversary's mimicry cost? (C4) The implication argued from the
frontier: where behavioral detection is cheap to defeat, only cryptographic/TEE-backed
attestation with disclosure norms closes the gap — the "TLS for model serving" conclusion,
now empirically grounded rather than asserted.

**Sources:** `position_paper_pipeline_2026-08.md` (Candidate 4, novelty ledger; delta over
2504.04715 + 2604.27789 must be argued), `industry_signal_scan_2026-08.md` §3, B3 family
(B3.1/B3.3 probe-set machinery).

**Discussion protocol:** 6 stages; each carries one critic pass and one refined resolution.
Tags: [VERIFIED] = arXiv ID located in the sweep / read earlier; [NEEDS-VERIFICATION] =
channel-relayed incident, primary source not yet located.

---

## Stage 0 — Primary-source verification gate

Both motivating incidents are relayed; both need primary verification before appearing in
the draft. Unlike C3, the *experiment's* ground truth does NOT depend on these figures (it
is constructed in our own testbed), so the incidents motivate rather than substantiate —
but a security-venue reviewer will still reject relayed anecdotes.

| # | Claimed incident | Claimed source | Where to look | Status |
|---|---|---|---|---|
| V1 | Llama-4 Maverick ranked #2 at launch, fell to #32 when LMArena retested the released checkpoint (implying a separately-tuned submission variant) | LMArena's own statements / blog (relayed via `bestpartners`, P8FhX97Pb6g) | lmarena.ai blog + X/Twitter statements; Meta's Llama-4 release notes; contemporaneous coverage naming the "experimental chat version" | [NEEDS-VERIFICATION] |
| V2 | A safety tier covertly altered outputs without disclosure until developer backlash | Anthropic 319-page system card (relayed via `whycallqq`, P2MAa3jpmZw) | the specific system-card passage; developer-forum threads that forced disclosure | [NEEDS-VERIFICATION] |

**Verified mechanism-layer literature (located in sweep; full read before citing):**
- [VERIFIED] arXiv:2606.16100 — behavioral fingerprints are SPOOFABLE by a cheating
  provider; the tier-downgrade scenario directly. This is the paper's pivot: it turns a
  detection paper into a detection-vs-spoofing-cost paper.
- [VERIFIED] arXiv:2504.04715 — model-substitution auditing; concludes "TEE attestation is
  the only viable path." The main foil for the TEE-conclusion delta.
- [VERIFIED] arXiv:2604.27789 — governance of silent model updates. The foil for the
  disclosure-norms delta.
- [VERIFIED] arXiv:2506.06975 — rank-based API auditing.
- [VERIFIED] arXiv:2607.10252 — one-token fingerprinting.
- [VERIFIED] arXiv:2512.03816 — logprob tracking for change detection.

**Decision rule.** If V1/V2 verify → they open §1 as documented real-world incidents; if
not → the paper opens on the *decoupling risk* argued from the verified mechanism
literature (2504.04715 already documents substitution auditing as a live concern), and the
incidents move to a hedged "reported" footnote or are cut. The experiment is unaffected
either way — this is the framing's strength over C3.

**Critic:** Because the experiment is self-contained, Stage 0 is tempting to skip — but
that inverts the real risk: the paper's *whole reason to exist* is that substitution
happens in the wild, and if neither incident survives verification, the motivation reduces
to "this could happen," which a security reviewer will call a solution in search of a
problem. The gate is under-weighted, not over-weighted. Also the verified literature list
mixes foils (2504.04715, 2604.27789) with tools (2506.06975, 2607.10252) without saying
which our testbed will *use* vs *argue against* — a reviewer needs that separation early.

**Refined:** Stage 0 keeps a hard motivation sub-gate: at least one of V1/V2 must verify,
OR a substitute documented incident must be found (the auditing literature 2504.04715 /
2604.27789 cite real cases — mine their references for a citable, primary-verified
substitution/undisclosed-change incident), else the paper is reframed from "detection of a
known-occurring harm" to "feasibility bound for an emerging harm" (weaker but honest, and
the frontier result still stands). The verified list is split by role in this doc: **foils**
= 2504.04715 (TEE-only conclusion), 2604.27789 (governance). **Reusable detection
tooling** = 2506.06975 (rank-based), 2607.10252 (one-token), 2512.03816 (logprob) — these
become the auditor's detector bank in Stage 6, cited as building blocks, not competitors.
**Adversary model source** = 2606.16100 (spoofability). This role table is fixed at M1.

---

## Stage 1 — Problem definition

**The wrong practice/belief.** The field treats a served model's identity as given: eval
papers assume the checkpoint they benchmarked is the checkpoint served; consumers assume
the tier they pay for is the tier they receive; and where auditing is discussed, the
implicit belief is that *either* behavioral fingerprinting suffices to catch substitution
*or* that TEE attestation (2504.04715) fully resolves it. Both halves are incomplete:
fingerprints are spoofable (2606.16100), and TEEs attest execution without creating
disclosure *norms* (2604.27789) or covering the behavioral-equivalence question a consumer
actually cares about.

**Who holds it.** Benchmark/eval authors (checkpoint-identity assumed silently); API
consumers and downstream product builders (tier/version assumed); the auditing sub-field
that has proposed detection methods (2506.06975, 2607.10252, 2512.03816) without measuring
them against an *adaptive* spoofing adversary; standards/governance discussions treating
either TEEs or fingerprints as the answer.

**The measurement problem (method-free).** Given only black-box query access to a served
API endpoint: (a) can an external auditor reliably detect that the served model differs
from a claimed reference checkpoint (full substitution) or has been tier-downgraded
(partial capability reduction), *under realistic serving nondeterminism*? (b) how does that
detection power degrade against a *spoofing-aware* provider who actively mimics the
reference model's observable fingerprint while still serving the cheaper/different model?
(c) what is the resulting **frontier** — detection power (or query cost to reach a target
power) as a function of the adversary's spoofing budget — and where on that frontier does
behavioral-only auditing become uneconomical, marking the region where cryptographic
attestation is the only remaining option?

**Formal objects.** Endpoints E serve model m ∈ {reference m0, substitute m1, downgraded
m0*}; noise process N (temperature τ, batch nondeterminism, quantization q, routing);
auditor issues n queries via a detector d ∈ D, outputs decision + confidence; adversary
spends budget b on a mimicry policy π_b (project m1's outputs toward m0's fingerprint);
detection power = P(correct reject | m≠m0) at fixed false-positive rate α, as a surface
over (n, b, N). The deliverable object is this surface / its frontier.

**Out of scope (leak guard):** designing the cryptographic attestation protocol itself
(that is the discussion/implication, and future work / B3.3's eventual system); the
experiment measures *when behavioral auditing fails*, which is what makes attestation
necessary — the paper argues the need, it does not build the certificate.

**Critic:** The problem definition conflates three detection tasks with very different
difficulty — full substitution (m0 vs unrelated m1), tier-downgrade (m0 vs a quantized/
smaller sibling m0*), and adaptive spoofing — and a single "frontier" cannot summarize all
three; the downgrade case is where 2606.16100's spoofability bites hardest and also where
serving noise most plausibly masks the effect, so lumping it with clean substitution will
produce an uninterpretable average. Also, "realistic serving noise" is asserted but its
*calibration* to real deployments is unspecified — if our injected noise doesn't match what
real APIs exhibit, the whole external-validity claim collapses.

**Refined:** The problem is explicitly stratified into three detection regimes, each with
its own frontier, reported separately: **R1 full substitution** (m0 vs a different-family
model), **R2 tier-downgrade** (m0 vs its quantized/distilled sibling — the
consumer-protection case and the hardest), **R3 adaptive spoofing** (R1/R2 with the
adversary spending mimicry budget). The paper's headline is the *R2 and R3 frontiers*,
since R1 is the easy case prior tools mostly solve. Noise calibration is promoted to a
first-class design requirement with its own gate (Stage 6 G1): the injected noise process
N is fit to *measured* nondeterminism from real public APIs (repeat-query variance,
temperature effects, observed batching jitter) so that "realistic" is an empirical claim
with an appendix, not an adjective. Construct scope stated: detection is of
behavioral-identity divergence, which is necessary-not-sufficient for the broader identity
question — and that gap is exactly the paper's argument for attestation.

---

## Stage 2 — Motivation: why now

**Why binding in 2026.** (1) Documented incidents: served ≠ evaluated has moved from
hypothetical to reported (LMArena Llama-4; tier-downgrade), so the harm is real, not
speculative. (2) Economic incentive is structural and growing: as inference cost dominates,
the incentive to silently serve a cheaper checkpoint at a premium tier only rises. (3) The
science-reproducibility stake: every eval/benchmark paper silently assumes checkpoint
identity — if that assumption is violable and undetectable, a large literature rests on an
unverified premise. (4) The detection sub-field has produced fingerprints (2506.06975,
2607.10252, 2512.03816) but 2606.16100 just showed them spoofable — so the field's own
proposed defense has a freshly-documented hole that nobody has *measured the size of*. That
measurement gap is the opening.

**Binding evidence, tagged:**
1. [NEEDS-VERIFICATION] Llama-4 / LMArena #2→#32 on retest. Role: cleanest documented
   substitution incident.
2. [NEEDS-VERIFICATION] tier-downgrade covert behavior change. Role: the consumer-protection
   and tier-downgrade (R2) motivating case.
3. [VERIFIED] arXiv:2606.16100 — fingerprints spoofable. Role: the pivot; kills a naive
   "just fingerprint it" paper and creates the detection-vs-cost question.
4. [VERIFIED] arXiv:2504.04715 — substitution auditing, "TEE is the only viable path."
   Role: establishes the problem is recognized AND sets the delta we must beat.
5. [VERIFIED] arXiv:2604.27789 — governance of silent updates. Role: disclosure-norm gap.
6. [VERIFIED] arXiv:2506.06975 / 2607.10252 / 2512.03816 — detection tooling. Role: the
   detector bank we build on and stress-test against the adversary.

**Critic:** The reproducibility stake (point 3) is rhetorically strong but the paper does
not measure it — it's a motivating claim the experiment never touches, which invites "then
why isn't reproducibility your dependent variable?" Point 2's economic-incentive argument
is asserted without any number (how much cheaper is the downgraded checkpoint? if the
saving is trivial, the threat model is weak). And leaning on two unverified incidents as
pillars 1–2 while pillar 4 (the spoofability result) is the actually-verified load-bearing
motive risks the same C3 problem: the vivid motives are the unverified ones.

**Refined:** Motivation is re-anchored on the verified pivot (3+4+5+6): "the field proposed
behavioral fingerprinting as the substitution defense; it was just shown spoofable; nobody
has measured how spoofable — under what adversary budget, at what serving noise — and
therefore nobody knows whether behavioral auditing is a usable backstop or a false comfort;
we measure it, and the answer determines whether cryptographic attestation is optional or
mandatory." This stands entirely on verified work. Incidents 1–2 are amplifiers gated by
Stage 0. The economic-incentive point gets a concrete anchor: cite the actual price/compute
delta between a flagship and its quantized/distilled sibling (public pricing + known
quantization speedups) to size the adversary's motive — a verifiable number, not an
assertion. The reproducibility stake is kept as an *implication* in the discussion, not
claimed as a measured result.

---

## Stage 3 — Related-work positioning

Novelty-ledger discipline: named occupant → concede-and-claim with an operational delta.
The two mandated deltas (2504.04715, 2604.27789) are argued explicitly.

**O1. arXiv:2504.04715 — substitution auditing, "TEE is the only viable path"** (mandated
delta).
*Concede:* they correctly frame served-model substitution as an auditing problem and
reach a defensible conclusion — that trusted execution is the robust guarantee. *Claim:*
they assert TEE-necessity by argument; we *measure the frontier that makes it necessary* —
exactly where behavioral auditing's power collapses against an adaptive adversary under
realistic noise. Our delta is empirical grounding for their conclusion in the R2/R3 regimes
they did not quantify, plus the part TEEs do not solve (behavioral-equivalence and
disclosure), so "TEE is necessary" becomes "TEE is necessary *here on the frontier*, and
insufficient *there* without disclosure norms" — a sharper, tested claim.

**O2. arXiv:2604.27789 — governance of silent model updates** (mandated delta).
*Concede:* they own the norm-and-governance framing: silent updates need disclosure regimes.
*Claim:* governance without a *verification substrate* is unenforceable — a disclosure norm
you cannot audit is a promise, not a control; our frontier shows precisely which violations
are externally detectable (cheap to catch, norm can be self-enforcing) versus which are not
(cheap to spoof, norm needs cryptographic backing). We supply the enforceability map their
governance proposal presupposes but does not provide.

**O3. arXiv:2606.16100 — fingerprints are spoofable.**
*Concede:* they own the qualitative result that a cheating provider can defeat behavioral
fingerprinting, including the tier-downgrade scenario. *Claim:* they demonstrate spoofability
exists; we quantify its *cost frontier* — how much mimicry budget defeats how much detection
power at what query cost under what noise — turning an existence proof into an economic
boundary that tells a defender whether to bother.

**O4. arXiv:2506.06975 (rank-based) / 2607.10252 (one-token) / 2512.03816 (logprob).**
*Concede:* they own individual black-box detection methods, each effective against a
non-adaptive provider. *Claim:* none is evaluated against a spoofing-aware adversary or
under calibrated serving noise; we assemble them into the auditor's detector bank and report
where each sits on the frontier — repositioning them from "solutions" to "measured
instruments with a known breaking point."

**O5. TEE/cryptographic attestation architectures (the hardware-attestation line
2504.04715 builds toward).**
*Concede:* cryptographic attestation is the robust endpoint and we do not out-engineer it.
*Claim:* our contribution is the *evidence that behavioral auditing cannot substitute for
it in the R2/R3 regime* plus the disclosure-norm layer TEEs omit — i.e., we motivate and
scope attestation, we do not reinvent it.

**Critic:** The whole positioning rests on "we quantify the frontier they left qualitative,"
which is only a contribution if the frontier is *non-obvious* — a reviewer can say "of
course more mimicry budget defeats more detection; you've measured a monotone curve nobody
doubted." Without a stated hypothesis about the frontier's *shape* (a threshold? a cheap
plateau where tiny budget kills detection? a regime where noise alone masks downgrade?),
the deltas read as "we put numbers on the obvious." Also O1's delta claims TEEs are
"insufficient without disclosure norms" but the experiment measures behavioral detection,
not TEE sufficiency — that half of the delta is argued, not tested, and should be labeled.

**Refined:** The positioning is re-centered on *decision-relevant frontier shape*, with
falsifiable structure the experiment can confirm or refute: the interesting, non-obvious
claims are (i) an **asymmetry** — R2 tier-downgrade is far cheaper to spoof than R1
substitution, so consumer-protection (the case people care about) is precisely the weak
case; (ii) a **noise-masking threshold** — a level of realistic serving noise above which
even zero adversary budget defeats downgrade detection at practical query counts; (iii) a
**cost cliff** — a small mimicry budget that collapses detection power sharply (a plateau),
versus graceful degradation. If the frontiers are boring (smooth, high-detection
everywhere), that is *itself* a publishable result overturning the C4 stance (behavioral
auditing suffices — attestation is optional), so the positioning is honest either way. O1's
untested half is explicitly labeled: the "TEE insufficient without disclosure" claim is
argued in discussion and scoped as such; the *tested* delta is the detection frontier.

---

## Stage 4 — Sub-problems

Each: claim → evidence → weakest point. SP2 is the mandated spoofability core.

**SP1 — Substitution/downgrade is detectable under realistic noise by a non-adaptive
auditor (RQ1: baseline detectability).** With auditor-controlled endpoints and a detector
bank (rank-based, one-token, logprob), full substitution (R1) and tier-downgrade (R2) are
detectable at practical query counts *when the provider is not actively hiding* — but
detection power for R2 degrades sharply as serving noise rises.
*Evidence:* [VERIFIED] 2506.06975/2607.10252/2512.03816 show detection works vs
non-adaptive providers; our testbed adds calibrated noise (R2 under noise is the novel
cell).
*Weakest point:* if our noise calibration is unrepresentative, R2 results don't transfer.
Mitigation: G1 noise-calibration gate (Stage 6) fits N to measured real-API variance;
sensitivity reported across a noise sweep.

**SP2 — [MANDATORY CORE] Behavioral-only attestation fails against a spoofing-aware
adversary, and the failure is cheap in the case that matters (RQ2: spoofing frontier).** A
provider who mimics the reference fingerprint (project m1/m0* outputs toward m0 on the
statistics the detector uses) collapses detection power; the mimicry budget required is
small for tier-downgrade (R2→R3), because the sibling model is already close in output
distribution, and larger for cross-family substitution. Therefore behavioral auditing
cannot be the identity layer — exactly the stance's claim, now with a measured cost.
*Evidence:* [VERIFIED] 2606.16100 (spoofability exists, tier-downgrade scenario); our
frontier quantifies its cost.
*Weakest point:* the adversary is *our* construction — a reviewer can say we built a
strawman spoofer that's too strong or too weak. Mitigation: implement multiple adversary
strategies of increasing sophistication (naive output-matching → detector-aware
distributional matching → adaptive best-response to the specific detector), report the
frontier per adversary tier, and open-source the spoofers so the strength is auditable, not
asserted.

**SP3 — There exists a serving-noise regime where downgrade is undetectable at any
practical query budget even without an adversary (RQ3: noise-masking bound).** Batching
nondeterminism + temperature + quantization jitter can alone mask a genuine tier-downgrade,
because the served-model difference is within the noise envelope; this is the
"innocent-looking" failure that makes disclosure norms (not just anti-adversary detection)
necessary.
*Evidence:* preliminary — depends on measured real-API noise magnitudes vs measured
downgrade effect sizes; this is a genuine open question the experiment settles.
*Weakest point:* may not exist (noise might be smaller than downgrade effects), in which
case SP3 is a null — but a null here is informative (downgrade IS detectable absent an
adversary, sharpening the argument to "the adversary, not noise, is the problem").

**SP4 — The frontier is decision-relevant: it separates a regime where behavioral auditing
is a usable backstop from one where only cryptographic attestation + disclosure norms
suffice (RQ4: the implication).** Mapping SP1–SP3 onto the (noise × adversary-budget) plane
yields regions; the paper's claim is that the consumer-relevant region (R2 under modest
adversary budget) lands in the attestation-required zone.
*Evidence:* synthesis of SP1–SP3 results.
*Weakest point:* this is an interpretive claim layered on the measurements — a reviewer may
accept the numbers but dispute the region boundaries (what counts as "practical query
budget"?). Mitigation: report the frontier as a surface with the decision thresholds as
explicit, defensible parameters (e.g., 10k queries = a plausible third-party audit budget),
and show robustness of the conclusion across a range of thresholds.

**Critic:** Scope and dependency risk again. SP1–SP4 across three regimes × a noise sweep ×
an adversary ladder × a detector bank is a large factorial; and SP2's frontier depends on
SP1's detectors being tuned and SP3's noise being calibrated, so the mandated core sits at
the end of a dependency chain. There's no minimum-publishable core. Also SP2 and SP3 can
*interact* (an adversary who exploits noise), which the flat sub-problem list doesn't
represent — and that interaction is arguably the real threat.

**Refined:** Re-staged core vs extension. **Core (MPU): SP1 + SP2 on R2 (tier-downgrade)
only** — baseline downgrade detectability under calibrated noise, then its collapse against
the adversary ladder. R2 is the case people care about and where the stance is sharpest;
this alone is a full paper (first measured spoofing-cost frontier for tier-downgrade under
realistic serving noise). **Extension 1: R1 (full substitution)** — same pipeline, easier
regime, adds generality. **Extension 2: SP3 noise-masking bound** — additive analysis on
the core data (no new adversary). **Extension 3: SP2×SP3 interaction** — the
noise-exploiting adversary, flagged as the strongest but most compute-heavy variant. The
dependency chain is linearized: core needs the detector bank + noise calibration (both
front-loaded as G1/G2 gates) and one adversary ladder, nothing else. SP4's interpretation
is confined to whatever regimes the core+extensions actually cover, with thresholds
reported as parameters.

---

## Stage 5 — Argument architecture (paper skeleton)

Target: security/ML research-track full paper (~11–13 pp). Each section names its
load-bearing exhibit.

- **§1 Introduction.** Stance-first: served ≠ evaluated is documented; fingerprints are
  spoofable; the open question is *how* spoofable, and the answer decides whether
  cryptographic attestation is optional or mandatory. Contributions C1–C4.
  *Load-bearing exhibit:* **Figure 1 — the threat-and-defense map**: served-model identity
  attacks (substitution, tier-downgrade, adaptive spoofing) × defenses (behavioral
  fingerprinting, TEE, disclosure norms), with the cells prior work covers shaded and the
  open cell (adaptive spoofing under noise) highlighted.
- **§2 Background & incidents.** Verified incidents (Stage 0 gated); the detection tooling;
  the spoofability result; foils 2504.04715 / 2604.27789.
  *Load-bearing exhibit:* **Table 1 — prior detection methods** × (adversary-aware? noise-
  calibrated? tier-downgrade tested?) — three "no" columns that define the gap.
- **§3 Threat model & testbed.** Auditor-controlled endpoints; checkpoint pairs (m0, m1,
  m0*); noise process N and its calibration; detector bank; adversary ladder (naive →
  detector-aware → best-response).
  *Load-bearing exhibit:* **Figure 2 — testbed architecture**: our endpoints, the injected
  noise, the auditor, the adversary — the ground-truth-by-construction diagram.
- **§4 RQ1 results: baseline detectability under noise.** Detection power vs query count
  for R2 (and R1 extension) across the noise sweep, non-adaptive provider.
  *Load-bearing exhibit:* **Figure 3 — power vs queries, by noise level** (the "detection
  works, but noise hurts downgrade" panel).
- **§5 RQ2 results: the spoofing-cost frontier (headline).** Detection power vs adversary
  mimicry budget, per adversary tier, at fixed query budget and noise — the core deliverable.
  *Load-bearing exhibit:* **Figure 4 — the frontier**: detection power (or query-cost-to-
  power) as a surface/curve over adversary budget, with the "cost cliff" (if present)
  annotated; this is the paper's money figure.
- **§6 RQ3 results: noise-masking bound (extension).** Region where downgrade is
  undetectable absent any adversary.
  *Load-bearing exhibit:* **Figure 5 — effect-size vs noise-envelope overlay**.
- **§7 RQ4: the decision map & implication.** SP1–SP3 onto the (noise × budget) plane;
  the attestation-required region; the "TLS for model serving" argument grounded in the
  frontier; disclosure-norm layer TEEs omit.
  *Load-bearing exhibit:* **Figure 6 — decision map**: regions labeled {behavioral auditing
  suffices / attestation required / disclosure-norm required}, with the consumer-relevant
  point plotted.
- **§8 Discussion.** What attestation protocol the frontier implies (sketch, not build);
  connection to B3.3; the deltas over 2504.04715 (empirical grounding) and 2604.27789
  (enforceability substrate) restated.
- **§9 Threats.** Adversary-strawman risk (multiple tiers, open-sourced), noise external
  validity (calibration appendix), checkpoint-pair representativeness, single-detector-bank
  scope.
- **§10 Related work.** Stage 3 occupants.

**Critic:** Six figures is heavy, and the skeleton front-loads baseline detectability (§4)
before the headline frontier (§5) — the same burying risk as C3: reviewers hit "detection
works" and may file this under the crowded detection-methods literature (O4) before
reaching the frontier that differentiates it. Also §7's decision map presents interpretive
regions as if they were measured, and the boundary between "measured frontier" and
"argued implication" must be unmistakable or reviewers will attack the soft part as if it
were the claim.

**Refined:** §4 and §5 merge into one results arc ("How hard is it to hide a downgrade?"):
4.1 baseline (noise hurts but detection works) → 4.2 the adversary collapses it (the
frontier), so the differentiating result arrives immediately and the intro leads with the
frontier (C3) over the testbed (C1). Figure budget cut to four core + two extension: core =
threat-defense map (Fig 1), testbed (Fig 2), the frontier (the merged Fig 3+4), decision
map (Fig 6); Figs 5 and the baseline-only panel are [extension]/appendix. The
measured-vs-argued boundary is made explicit typographically: §4–§6 are "Results" (measured
surfaces only); §7 is retitled "Implications" and every region boundary carries its
threshold parameter inline, so the decision map is visibly a *reading* of the measured
frontier, not a new measurement.

---

## Stage 6 — Validation plan (concrete implementable experiment spec)

### Testbed & materials (build order)

**Endpoints (ground truth by construction):**
- Stand up controlled API endpoints (same serving stack, e.g., vLLM/TGI behind a uniform
  wrapper) serving known checkpoint pairs: **m0** reference (a mid-size open model, e.g.
  Llama/Qwen-class 7–70B), **m1** cross-family substitute (different architecture, similar
  size), **m0\*** tier-downgrade siblings (quantized 8-bit/4-bit and/or distilled smaller
  variant of m0). Ground truth = which checkpoint each endpoint serves (we know it).
- All open weights so results are reproducible; no dependence on any vendor's private API.

**Noise process N (calibrated — G1 gate):**
- Inject temperature variation, batching/kernel nondeterminism (vary batch size, GPU
  nondeterministic kernels), quantization jitter, and load-dependent routing. **G1:** fit
  the magnitudes of N to *measured* nondeterminism from real public APIs (repeat identical
  queries to 2–3 commercial endpoints, measure output-distribution variance and
  logprob/rank stability) so "realistic" is empirical. Report a noise sweep spanning
  measured-low to measured-high.

**Detector bank (build on verified tooling — G2 gate):**
- Implement/port rank-based (2506.06975), one-token (2607.10252), and logprob-tracking
  (2512.03816) detectors behind a common interface; **G2:** validate each reproduces its
  paper's detection on a clean (noise-free, non-adaptive) pair before trusting it under
  noise/adversary.

**Adversary ladder (open-sourced):**
- A0 none; A1 naive output-matching (post-hoc project m0*/m1 outputs toward m0's frequent
  tokens); A2 detector-aware distributional matching (match the specific statistics the
  detector uses — rank distributions, one-token marginals, logprob moments); A3 adaptive
  best-response (optimize mimicry against the deployed detector, at measured compute cost =
  the "spoofing budget" x-axis).

### Metrics
- Detection power = P(reject | m≠m0) at fixed FPR α=0.05, as a function of query count n,
  noise level, adversary tier/budget b. Bootstrapped CIs over query samples and over
  checkpoint-pair instances.
- Query-cost-to-power: n required to reach 0.8 power, as a function of b and noise (the
  frontier's practical axis).
- Spoofing budget b measured in adversary compute/effort (FLOPs or wall-clock for the
  mimicry policy) and, where relevant, in mimicry quality degradation (does hiding cost the
  adversary task performance? — a downgraded model forced to mimic m0 may lose the cost
  saving that motivated the downgrade — a key secondary result).

### Falsification conditions
- **F1 (baseline):** if no detector reaches 0.8 power on the clean R1 substitution pair at
  any practical n, the detector bank is broken (fix before proceeding — a G2 failure, not a
  finding).
- **F2 (spoofing, core stance):** if detection power stays ≥0.8 for R2 across the *full*
  adversary ladder up to large budget, behavioral auditing is NOT easily spoofable — the
  C4 stance is falsified and attestation is optional (a publishable reversal).
- **F3 (asymmetry):** if R2 is *not* cheaper to spoof than R1, the "consumer case is the
  weak case" claim (Stage 3 refined) is wrong.
- **F4 (noise-masking):** if downgrade stays detectable at 0.8 power even at measured-high
  noise with A0, SP3's noise bound doesn't exist (informative null).
- **F5 (adversary cost-of-hiding):** if mimicry is free (no task-performance loss to the
  adversary), the economic argument that attestation is worth its cost weakens.

### Anticipated reviewer attacks & responses
- **A1: "Your adversary is a strawman."** The ladder (A0–A3) plus open-sourced spoofers;
  the frontier is reported per tier so readers see the trend, not one point; A3 is a
  best-response, i.e., the strongest reasonable adversary, not a weak one.
- **A2: "Your injected noise isn't real serving noise."** G1 calibration to measured
  commercial-API variance; full noise sweep; appendix with the measurement protocol.
- **A3: "Open-weight testbed doesn't reflect closed frontier serving."** Conceded scope;
  the frontier's *shape* (cost cliff, asymmetry) is the transferable claim, and closed
  serving only adds noise/opacity that strengthens the attestation conclusion; stated as a
  threat with directionality argued.
- **A4: "This just confirms 2606.16100 (spoofable) and 2504.04715 (use TEEs)."** We
  quantify what they asserted: the cost frontier and the noise-masking bound neither
  measured, and the decision map that tells a practitioner *which* violations behavioral
  auditing can and cannot catch — the enforceability substrate 2604.27789's governance
  needs.
- **A5: "Detection at α=0.05 with many queries is p-hacking a difference that exists by
  construction."** The question is never "is there any difference" but "is there a
  practically-detectable difference at audit-scale query budgets under noise and
  adversary" — the frontier answers exactly that, and F2/F4 make the null publishable.

**Critic:** The A3 best-response adversary is the linchpin of the headline (F2 lives on it),
but "optimize mimicry against the deployed detector" is under-specified and potentially a
research project of its own — if A3 is weak, the frontier understates spoofability and a
reviewer will say the paper got lucky; if A3 is unbounded, it trivially wins and the
frontier is uninteresting. There's no stated principle for what makes A3 *fair*. Also the
cost-of-hiding metric (F5) is the most novel economic angle but is bolted on — it needs the
adversary's task-performance measured on a real capability benchmark, which isn't in the
materials list.

**Refined:** A3 is bounded by an explicit fairness principle stated in the threat model:
the adversary knows the detector *class and its public statistics* (Kerckhoffs-style: the
detector is not secret) but pays measured compute for the mimicry policy, and its budget b
is the x-axis — so "fair" means the frontier is reported *as a function of* the adversary's
spend, and neither a fixed-weak nor an unbounded adversary is the claim; the whole curve is.
A3's implementation is scoped to distributional-matching-via-lightweight-post-processing
(reweighting/reranking of m0*/m1 outputs toward m0's detector-visible statistics), NOT
retraining, keeping it bounded and reproducible; retraining-based spoofing is named as
future work / an upper-bound the frontier lower-bounds. The cost-of-hiding measurement is
promoted into the materials list: the adversary's served outputs are scored on a standard
capability benchmark (the same tasks the tier-downgrade was meant to cheapen), so
F5's "does hiding cost the adversary its savings?" is measured, not asserted — this becomes
the paper's economic teeth and a genuine second contribution.

---

## Venue plan

1. **Primary: a security research track** (IEEE S&P / USENIX Security / CCS; check the
   next open deadline at M1) — the ground-truth-by-construction testbed, adversary ladder,
   and cost frontier are a security-empirical contribution; the "auditing under an adaptive
   adversary" framing fits the community.
2. **Alternate: an ML venue with a measurement/benchmarks or trustworthy-ML track**
   (NeurIPS D&B / a trustworthy-ML workshop-to-track) if the ML-serving-noise and
   detector-bank angle reads better there; the frontier is model-serving-flavored.
3. **Composition with B3.3:** the probe-set machinery (B3.1/B3.3) is the detector-bank
   substrate; this paper is the adversarial-audit application of it — coordinate so B3.3's
   eventual system paper cites this as its threat-model grounding and vice versa.
4. **Fallback:** if the frontier turns out boring (F2/F4 nulls that still teach), the
   reversal ("behavioral auditing suffices for downgrade under realistic conditions") is
   itself a security-relevant result at the same venues, reframed.

## Time-to-draft estimate (3 milestones)

- **M1 — Testbed + gates green (target: +5 weeks).** Stage 0 incident verification (or
  substitute incident mined from 2504.04715/2604.27789 refs); controlled endpoints serving
  m0/m1/m0* stood up; G1 noise calibrated to measured commercial-API variance; G2 detector
  bank reproduces its source papers on clean pairs; adversary ladder A0–A2 implemented; role
  table (foils vs tooling) fixed.
- **M2 — Core frontier measured (target: +12 weeks).** R2 baseline detectability under the
  noise sweep (RQ1) and the spoofing-cost frontier against A0–A3 (RQ2) computed on frozen
  endpoints; A3 fairness-bounded best-response implemented; cost-of-hiding capability scores
  collected; go/no-go on extensions (R1, noise-masking bound, noise-exploiting adversary).
- **M3 — Full draft + artifact (target: +20 weeks).** Extensions landed or cut; decision map
  (RQ4) and implications drafted with measured-vs-argued boundary enforced; paper written to
  the Stage 5 refined skeleton; se-paper-reviewer + novelty-auditor passes (deltas over
  2504.04715 / 2604.27789 stress-tested by name); testbed + spoofers + detector bank
  open-sourced as artifact; submission-ready for the next security-track window.

---

## Closing block

**One-sentence falsifiable hypothesis.** Against an external black-box auditor using
published detection methods under serving noise calibrated to real commercial APIs, a
tier-downgrade (a quantized/distilled sibling served in place of the reference model) can
be hidden by a spoofing-aware provider at small, measurable mimicry budget — collapsing
detection power below practical thresholds at audit-scale query counts — and it is hidden
more cheaply than a full cross-family substitution, establishing an empirical frontier
where behavioral-only attestation is insufficient and cryptographic attestation plus
disclosure norms are required.

**Implementation checklist (build order).**
1. Stage 0: verify V1 (LMArena) / V2 (tier-downgrade) or mine a primary substitute
   incident from 2504.04715 / 2604.27789 references; full-read the six verified sources;
   fix the foils-vs-tooling role table.
2. Stand up controlled endpoints serving m0 (reference), m1 (cross-family), m0* (quantized/
   distilled siblings) on a uniform open serving stack; record ground-truth mapping.
3. G1: measure real commercial-API nondeterminism (repeat-query variance, logprob/rank
   stability); calibrate the injected noise process N; define the noise sweep.
4. G2: port rank-based / one-token / logprob detectors behind a common interface; verify
   each reproduces its source result on a clean pair.
5. Implement the adversary ladder A0 (none) → A1 (naive) → A2 (detector-aware
   distributional matching) → A3 (fairness-bounded best-response via lightweight
   post-processing); open-source it; measure mimicry compute = spoofing budget axis.
6. Add cost-of-hiding: score adversary outputs on a capability benchmark to measure whether
   mimicry erodes the downgrade's savings.
7. Run RQ1 (baseline detectability of R2 under noise sweep, non-adaptive) then RQ2 (spoofing
   frontier of R2 across A0–A3) on frozen endpoints; compute power, query-cost-to-power, CIs.
8. Extensions per M2 go/no-go: R1 full substitution; SP3 noise-masking bound; SP2×SP3
   noise-exploiting adversary.
9. Build the decision map (RQ4); write to the Stage 5 refined skeleton with the
   measured-vs-argued boundary enforced; internal reviews; package artifact; submit.

**Verification criteria — what publishes vs. what kills it.**
- **Publishes (headline):** a measured frontier showing R2 tier-downgrade detection power
  collapsing below a practical threshold (e.g. <0.5 at 10k queries) at small adversary
  budget under realistic noise, AND the asymmetry (R2 cheaper to spoof than R1); best
  version adds a noise-masking bound and a measured cost-of-hiding (mimicry erodes the
  adversary's savings) — the full "behavioral auditing is insufficient; attestation is
  required" argument, empirically grounded.
- **Publishes (reversal, still a paper):** if detection stays robust across the adversary
  ladder (F2) and/or downgrade is detectable even at high noise (F4), the result reverses
  the stance — "behavioral auditing suffices for the consumer-relevant case under realistic
  conditions, attestation is optional here" — a security-relevant, publishable finding that
  reframes rather than kills the paper.
- **Kills it (as framed):** if the detector bank cannot be made to work even on clean pairs
  (F1 / G2 failure) the experiment is not runnable and the paper cannot ship until fixed; and
  if the frontier is entirely uninformative (flat/obvious with no threshold, no asymmetry,
  no noise bound, no cost-of-hiding signal) the empirical contribution over 2606.16100 +
  2504.04715 evaporates — retire C4 as a standalone and fold the testbed into B3.3 as its
  threat-model evaluation section.
