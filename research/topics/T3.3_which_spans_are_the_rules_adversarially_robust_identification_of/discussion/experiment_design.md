# Experiment Design — T3.3 (standalone protocol)

> Stage 6's confirmed output (`pipeline.md`) rendered as a standalone, runnable document, per the `auto-research-discussion` skill's Final Deliverables spec. This is the protocol to execute from — it should not require opening `paper_draft.md` or `paper.md` to run. Nothing below is invented: every field is carried from `pipeline.md`'s Stage 6 confirmed output, `paper_draft.md`'s Experiments section (built from that same confirmed output), and `paper.md`'s Step 6 pre-registration. No experiments have been run — every number is a pre-registered design target, not a result. Keep this file synchronized with `paper_draft.md`'s Experiments section if either is edited later.

**Study type:** `empirical` (measurement study — no "our identifier beats baseline X" claims; see Tier accounting below).

**Tier accounting** (checked against `study_type = empirical` in Stage 6):
- Mechanism-tier: **8 RQs**, one per Stage 5 hypothesis, each a verbatim `target_hypotheses` match.
- Framing-tier: **0 RQs** — no Stage 3 related-work limitation was flagged `verify_as_hypothesis`.
- Outcome-tier: **0 RQs** — `study_type = empirical` forbids beat-a-baseline framing; the baselines below are sanity-check comparators only.

---

## Datasets

**GovSpan-Adv (constructed, primary corpus).** Approximately 300 constraint spans drawn from TensorTrust's released, human-written defense-prompt corpus (real access-control rules), plus approximately 300 non-constraint spans sampled from LMSYS-Chat-1M, length- and topic-matched to the constraint spans. Every span carries a validated ground-truth label (target inter-annotator κ ≥ 0.7) before any rewrite is applied. Validity-gated bidirectional rewrites (Evade / Spoof, per the Methodology's `m_bidirectional_rewrite`) are then generated on top of this base corpus.
- *Justification:* both source pools are real, released assets, and TensorTrust's defense prompts are actual human-written governance rules rather than synthetic stand-ins.

**Second constraint-source pool — agent/system-prompt policy documents.** A second, structurally different constraint-source pool, to be assembled from publicly documented agent-framework system prompts (e.g., released tool-use or assistant policy templates) rather than TensorTrust's game-derived defense prompts alone. Concrete corpus selection is deferred to implementation time and will be named explicitly once assembled — this is flagged as a design commitment, not a citation (per the no-fabrication rule).
- *Justification:* digest N10/t3 names source-pool representativeness as a specific external-validity threat — TensorTrust is game-derived access-control rules and LMSYS-Chat-1M is public chat; neither alone represents production governance constraints such as multi-sentence policies or tool-permission rules. Drawing constraint spans from two structurally different pools and reporting `rq_adversarial_degradation`'s robustness gap per-source (not only pooled) is what lets cross-source consistency of Δ serve as the generalization check committed to in `paper.md`'s Assumption A4, rather than resting the whole finding on one source's idiosyncrasies.

**PrefEval (secondary transfer check, not a primary experiment corpus).** Used to test whether Stage-1 identifiers flag PrefEval's implicit preference statements as pin-worthy.
- *Justification:* bridges identification scores to an existing, independently released long-horizon preference-retention benchmark, giving a first, minimal (not exhaustive) check on whether identification-stage findings say anything about downstream retention (per `paper.md`'s Assumption A5 — identification is treated as separable from downstream pinning mechanics, and this transfer check is the scope-bounding measurement for that assumption, not a pass/fail gate on any hypothesis).

## Identifier families under test

Five families, evaluated identically under both original and adversarial phrasing:
1. Keyword/deontic-cue heuristic (regex over modals, imperatives, "always/never/must") — also serves as baseline B0 (below).
2. A fine-tuned span classifier trained on original, non-adversarial pairs.
3. A zero-shot prompted LLM-as-judge (model family kept disjoint from the rewriter) — the **pre-registered primary identifier**.
4. A position/privilege-signal identifier adapting ASIDE's channel-derived role mechanism (ASIDE's own reported results are not compared against — only its mechanism is adapted).
5. A cumulative-context prompted monitor adapting SeqMonitor's trajectory-level architecture (SeqMonitor's own reported results are not compared against — only its mechanism is adapted).

## Baselines (sanity-check comparators, not outcome-tier competitors)

**B0 — trivial/no-mechanism control.** The keyword/deontic-cue heuristic (identifier family 1 above), run only on original, non-adversarial phrasing.
- *Justification:* if B0 already fails on original phrasing, identification is hard even without an adversary (the problem is non-vacuously motivated); if it succeeds on original phrasing but collapses on adversarial phrasing, that specifically justifies studying the adversarial gap rather than a generically hard task.

**B-alt — strongest-alternative-explanation control.** Two components: (i) a cross-family rewriter ablation — swap the adversarial rewriter's model family to a disjoint alternative and re-measure Δ (this is also RQ8 below); (ii) a length-and-topic-matched non-constraint control — constraint and non-constraint spans are matched on token length (±20%) and embedding-cluster topic, verified before any identifier is run by a two-sample Kolmogorov–Smirnov test on span-length distributions and a two-sample test on the cosine-similarity distribution of topic embeddings (α = 0.05, non-significance required), reported as a corpus-validity statistic alongside annotation κ.
- *Justification:* rules out two rival explanations for any measured Δ — (i) attacker–defender model-family self-consistency, and (ii) the identifier exploiting spurious length/topic statistics rather than force or register at all — that the headline claim must rule out for the central mechanism claim (force/register decoupling) to be supported.
- *Pre-committed downgrade wording (per `paper.md` Step 6):* if Δ survives both checks, register-disguise is the isolated cause and the claims tested by RQ2/RQ3/RQ5/RQ6/RQ7 below (`paper.md`'s RQ1/RQ_INF_1/RQ_INF_2 claim family) hold at full strength. If Δ does not survive the family-swap check (moves more than 50% relative, per RQ8), the finding downgrades to "the measured gap reflects attacker–defender family self-consistency, not register-disguise fragility per se — the phenomenon of degraded identification under paraphrase stands, but the force/register-decoupling mechanism claim specifically is unsupported." If the KS/cosine matching-validity test finds a significant residual length/topic gap, the corpus-validity check itself failed and the affected claims are reported as unsupported pending a re-matched corpus, not as refuted. This downgrade is scored per-claim, not per-paper.

## Metrics (used across research questions below)

Miss-pin rate and false-pin rate per identifier per direction; the robustness gap Δ (adversarial − original error) and its AUROC-swept frontier; span-level F1 with IoU ≥ 0.5 overlap credit for the localization extension; Cohen's κ for annotation and validity-gate quality; the contested-label fraction with Wilson confidence intervals.

---

## RQ1 — `rq_rewrite_validity`

- **Tier:** Mechanism.
- **Target sub-problem:** `sp_force_register_decoupling`.
- **Target hypothesis (verbatim, Stage 5 → Stage 6):** "The validity gate certifies 70–80% of raw Evade/Spoof rewrites on first generation pass (rejection rate 20–30%), with post-gate inter-annotator Cohen's κ ≥ 0.7 on rewrite validity."
- **Setup:** Apply Evade and Spoof to the full GovSpan-Adv base corpus. Measure the fraction of raw rewrites certified on first generation pass by the entailment back-check and two-annotator validation, and the inter-annotator κ on the validation decision itself.
- **Sample-size rationale:** Full base corpus (~600 spans, ~300 per label) — no separate power calculation is specified for this RQ beyond running the gate over the full constructed corpus; this is an instrument-validation check (per `paper.md`'s R2 instrument-validation protocol), not a powered significance test.
- **Statistical test:** No null-hypothesis significance test — this is an instrument-validity check. Reported as a certification (pass) rate plus Cohen's κ inter-annotator reliability on the gate's own accept/reject decision.
- **Expected outcome:** The gate certifies 70–80% of raw rewrites on first pass (20–30% rejection and regeneration), with post-gate inter-annotator κ ≥ 0.7 on rewrite validity.
- **Falsification condition:** Refuted if post-gate κ falls below 0.7 (the validity judgment itself is not reliable enough to trust downstream measurement), or if the certified fraction is so low (e.g., below 40%) that the rewrite operators cannot produce enough valid items to power the remaining research questions, or so high (e.g., above 95%) that the gate is suspected of being too permissive to be doing real work.
- **Metrics:** Certification (pass) rate; inter-annotator κ on the validity judgment.

## RQ2 — `rq_adversarial_degradation`

- **Tier:** Mechanism.
- **Target sub-problem:** `sp_force_register_decoupling`.
- **Target hypothesis (verbatim, Stage 5 → Stage 6):** "For at least four of the five identifier families, identification error on validity-gated adversarial rewrites is significantly higher than on original phrasing (Holm-corrected McNemar test, per direction), with mean robustness gap Δ̄ ≥ 0.10 across families for the pre-registered primary identifier (LLM-as-judge)."
- **Setup:** For each of the five identifier families, compare decisions on original versus validity-gated adversarial phrasing of the same underlying items, per direction. Pilot stage: 2 backbones × 2 phrasing conditions × 300 pairs per direction.
- **Sample-size rationale:** n = 300 pairs per direction is sized to detect an approximately 8-percentage-point paired error-rate shift at power ≈ 0.8 via McNemar's test (per `paper.md` Assumption A6).
- **Statistical test:** Holm-corrected McNemar exact test on paired decision flips, one test per identifier × direction (10 tests), α = 0.05; effect sizes reported as discordant-pair odds ratios with 95% CIs.
- **Expected outcome:** For at least four of the five identifier families, adversarial error is significantly higher than original-phrasing error in at least one direction; for the pre-registered primary identifier (LLM-as-judge), the mean robustness gap Δ̄ ≥ 0.10 across the two directions.
- **Falsification condition:** Refuted for the primary identifier if the Holm-corrected McNemar test finds no significant original-versus-adversarial difference (p ≥ 0.05) or if Δ̄ < 0.10 — the central fragility claim would not hold, and the finding pivots to characterizing current identification as robust to semantic-register disguise specifically (as distinct from structural forgery), per `paper.md`'s RQ1 fallback.
- **Metrics:** Per-identifier, per-direction miss-pin/false-pin rate and Δ; McNemar p-values (Holm-corrected); discordant-pair odds ratios with 95% CIs.

## RQ3 — `rq_direction_dominance`

- **Tier:** Mechanism.
- **Target sub-problem:** `sp_direction_asymmetry`.
- **Target hypothesis (verbatim, Stage 5 → Stage 6):** "Under adversarial phrasing, miss-pin rate significantly exceeds false-pin rate: the 10k-bootstrap 95% CI on (missrate_adv − fprate_adv) lies strictly above 0."
- **Setup:** Under adversarial phrasing, compute the difference (miss-pin rate − false-pin rate) per identifier, pooled and per backbone, reusing the same paired items measured in RQ2.
- **Sample-size rationale:** Reuses RQ2's corpus (300 pairs per direction) — no separate sample beyond that pool.
- **Statistical test:** 10,000-resample bootstrap 95% CI on the (miss-pin − false-pin) rate difference.
- **Expected outcome:** The bootstrap CI on (miss-pin − false-pin) under adversarial phrasing lies strictly above 0, indicating miss-pin dominates.
- **Falsification condition:** Refuted if the CI includes 0 (no dominant direction) or lies strictly below 0 (false-pin dominates instead) — either would re-center the threat model toward spoofing (authority laundering) rather than evasion as the primary risk.
- **Metrics:** (miss-pin − false-pin) rate difference under adversarial phrasing, with bootstrap 95% CI.

## RQ4 — `rq_threshold_tradeoff`

- **Tier:** Mechanism.
- **Target sub-problem:** `sp_direction_asymmetry`.
- **Target hypothesis (verbatim, Stage 5 → Stage 6):** "Sweeping an identifier's decision threshold to reduce its adversarial miss-pin rate measurably increases its adversarial false-pin rate for the same identifier — no single operating point minimizes both error directions simultaneously."
- **Setup:** For each identifier, sweep the decision threshold over its confidence score across the full range and trace miss-pin rate and false-pin rate as a joint frontier under adversarial phrasing, reusing the same items and decisions from RQ2/RQ3.
- **Sample-size rationale:** Reuses RQ2's corpus (300 pairs per direction) — the threshold sweep is computed over the same decision set, not a new sample.
- **Statistical test:** Test whether the two rates move in opposite directions as the threshold varies (sign/slope of the local relationship across the swept range); AUROC computed as a summary statistic of the frontier.
- **Expected outcome:** Miss-pin rate and false-pin rate trace a negatively sloped frontier for every identifier family — no single threshold minimizes both simultaneously.
- **Falsification condition:** Refuted if any identifier family exhibits a threshold range where both miss-pin and false-pin rates are simultaneously at or near their respective minima (a non-negative-sloped region), which would mean the evasion/spoofing tradeoff is not fundamental to that identifier's decision structure.
- **Metrics:** Threshold-swept miss-pin/false-pin curve; sign of local slope across the curve; AUROC.

## RQ5 — `rq_localization_gap`

- **Tier:** Mechanism.
- **Target sub-problem:** `sp_joint_localization`.
- **Target hypothesis (verbatim, Stage 5 → Stage 6):** "In-context span-level miss-pin rate (embedded, unsegmented, IoU ≥ 0.5 overlap credit) exceeds isolated-pair miss-pin rate, with paired-bootstrap 95% CI strictly above 0."
- **Setup:** Embed validated GovSpan-Adv items at controlled depths (early/middle/late thirds) inside approximately 100 long transcripts (roughly 8k–32k tokens) built from unrelated filler conversation, 3–5 items per transcript, without given boundaries. Compute span-level F1 (IoU ≥ 0.5) and miss-pin rate per depth tercile; compare in-context miss-pin rate against the isolated-pair miss-pin rate from RQ2 via paired bootstrap.
- **Sample-size rationale:** ~100 transcripts × 3–5 items ≈ 300–500 embedded items, matched in scale to the isolated-pair pilot (RQ2's 300 pairs per direction) so the paired-bootstrap comparison is over comparably sized samples.
- **Statistical test:** Paired-bootstrap 95% CI on the (in-context − isolated) miss-pin rate difference.
- **Expected outcome:** In-context miss-pin rate exceeds isolated-pair miss-pin rate, with the paired-bootstrap 95% CI on the difference strictly above 0; degradation is largest at the earliest depth tercile.
- **Falsification condition:** Refuted if in-context miss-pin rate is statistically indistinguishable from isolated-pair miss-pin rate (the paired-bootstrap CI includes 0) — that would mean the cheap isolated-pair pilot already upper-bounds the deployed localization risk, a positive methodological finding in its own right (per `paper.md`'s RQ_INF_2 fallback).
- **Metrics:** Span-level F1 (IoU ≥ 0.5); depth-stratified miss-pin rate; paired-bootstrap CI on (in-context − isolated) miss-pin.

## RQ6 — `rq_adaptive_degradation`

- **Tier:** Mechanism.
- **Target sub-problem:** `sp_joint_localization`.
- **Target hypothesis (verbatim, Stage 5 → Stage 6):** "Δ_adaptive exceeds Δ_static for the best Stage-1 identifier, with paired-bootstrap 95% CI strictly above 0."
- **Setup:** Give the rewriter bounded query access (≤ 20 queries per item) to the best-performing Stage-1 identifier, and re-run Evade/Spoof adaptively against it within the same in-context transcripts used in RQ5; compare the resulting robustness gap Δ_adaptive against the static-rewrite Δ_static for the same identifier via paired bootstrap.
- **Sample-size rationale:** Reuses RQ5's embedded-item set (~300–500 items across ~100 transcripts); query budget capped at 20 queries per item.
- **Statistical test:** Paired-bootstrap 95% CI on the (Δ_adaptive − Δ_static) difference.
- **Expected outcome:** Δ_adaptive exceeds Δ_static, with a paired-bootstrap 95% CI on the difference strictly above 0.
- **Falsification condition:** Refuted if Δ_adaptive is statistically indistinguishable from or smaller than Δ_static (the CI on the difference includes or falls below 0) — that would mean query access to the identifier does not meaningfully help an attacker beyond a static, validity-gated rewrite.
- **Metrics:** Δ_adaptive vs. Δ_static; paired-bootstrap 95% CI on the difference.

## RQ7 — `rq_contested_fraction`

- **Tier:** Mechanism.
- **Target sub-problem:** `sp_label_indexicality`.
- **Target hypothesis (verbatim, Stage 5 → Stage 6):** "The contested-label fraction among adversarial errors has a Wilson 95% CI upper bound below 0.50 — a majority of measured adversarial fragility reflects genuine identifier failure, not contested ground truth."
- **Setup:** Re-annotate, blind and with full context, every item on which the identifier under audit errs (across the RQ2–RQ6 conditions) plus a matched random sample of correctly-decided items, using two independent annotators; classify each error as identifier-failure (annotators agree with gold) or contested (annotators split or disagree with gold).
- **Sample-size rationale:** Sample size is determined by the observed error count across RQ2–RQ6 (all errors are audited) plus a matched random sample of correct items of comparable size — not fixed in advance, since it depends on how many errors are actually observed.
- **Statistical test:** Wilson 95% CI on the contested fraction.
- **Expected outcome:** The contested-label fraction among adversarial errors has a Wilson 95% CI upper bound below 0.50 — a majority of measured fragility is genuine identifier failure, not label ambiguity.
- **Falsification condition:** Refuted if the Wilson CI upper bound on the contested fraction is at or above 0.50 — that would mean the measured "adversarial fragility" is majority a ground-truth well-posedness problem rather than an identifier property, and the paper's central contribution shifts from a robustness measurement to a contested-case taxonomy (per `paper.md`'s RQ_INF_1 fallback).
- **Metrics:** Contested-label fraction with Wilson 95% CI; a small taxonomy of contested cases.

## RQ8 — `rq_family_coupling_stability`

- **Tier:** Mechanism.
- **Target sub-problem:** `sp_attacker_defender_confound`.
- **Target hypothesis (verbatim, Stage 5 → Stage 6):** "Swapping the rewriter's model family changes the measured robustness gap Δ for the primary identifier by no more than 50% relative to the original-family measurement."
- **Setup:** Re-run the full rewrite-and-measure pipeline with the adversarial rewriter's model family swapped for a disjoint alternative, holding the primary identifier and all other protocol details fixed; compare the resulting Δ against the original-family measurement from RQ2. This is also the cross-family-ablation half of the B-alt baseline above.
- **Sample-size rationale:** Reuses RQ2's corpus and protocol for the primary identifier (LLM-as-judge) only, under the swapped-family rewriter.
- **Statistical test:** Relative-magnitude comparison against a pre-registered 50%-relative-change threshold (no separate null-hypothesis significance test is specified for this RQ beyond the threshold comparison itself).
- **Expected outcome:** The measured Δ for the primary identifier changes by no more than 50% relative to the original-family measurement.
- **Falsification condition:** Refuted if Δ moves by more than 50% relative under the family swap — that would indicate the originally measured gap was substantially an artifact of attacker-defender model-family self-consistency rather than a family-independent property of register disguise, triggering the B-alt pre-committed downgrade above.
- **Metrics:** Relative change in Δ under the family-swapped rewriter vs. the original-family measurement.

---

## Out of scope (explicitly bracketed, not a research question here)

A downstream, end-to-end pinning-budget study — given a fixed pin budget and the measured false-pin rates above, how often does spoofing actually exhaust the budget or crowd out a genuine constraint in practice — is explicitly out of scope. It introduces independent failure modes (budget allocation policy, retrieval behavior) that this study deliberately brackets to isolate the identification stage cleanly. The PrefEval transfer check (see Datasets) is a first, minimal bridge toward that larger question, not a substitute for it.
