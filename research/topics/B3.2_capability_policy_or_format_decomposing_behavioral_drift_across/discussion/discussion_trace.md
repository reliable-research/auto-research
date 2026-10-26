# Auto-Research-Discussion Run — B3.2 (autoclaude-style, repo-driven from digest.md + paper.md)

> Mode: **autoclaude** (self-play, Claude as student+teacher). Source: `../digest.md` (N0–N12) + `../paper.md` (Steps 0–9), both pre-existing reverse-digest artifacts for seed **B3.2**. Round cap: 5/stage (none hit). All six stages converged in 1 critic round + 1 refiner pass each — the seed material was unusually mature (paper.md already carries a pre-registered statistical plan with gating order, fallbacks, and a walking skeleton), so genuine disagreement surfaced but didn't require re-proposing.
>
> **Full pipeline order:** this file (`auto-research-discussion`, 6 stages) → `taste_audit.md` (`research-taste-auditor`, idea-level check on Stage 2+5) → `stage_review.md` (`pengsida-stage-reviewer`, PASS/REVISE/STOP per stage against the confirmed outputs, plus a Stage 5 Writing check on the first assembled draft) → final `paper_draft.md`/`.tex`/`.pdf`. Two REVISE findings from `stage_review.md` (a missing nearest-neighbor sentence in Related Work, and missing per-RQ falsification conditions in Experiments) are already folded into the `paper_draft.*` files below — read `stage_review.md` for the reasoning behind those two fixes.

## Seed brief

- **One-sentence description:** Decompose the observed behavioral change between a pair of same-provider LLM versions into capability, policy, and format components, and test whether the resulting attribution structure recurs across vendors or is vendor-specific.
- **Apparent inputs:** same-provider LLM version pairs (commercial snapshot-pinned endpoints and open-weight release pairs); constructed control pairs whose dominant change axis is known by construction; repeated sampling per item per version.
- **Apparent outputs:** a per-pair axis-share attribution (capability / policy / format / leakage / noise-floor); a calibration accuracy report on control pairs; a cross-vendor structural comparison.
- **Closest research areas:** longitudinal LLM behavioral auditing ([ChatGPTBehavior, arXiv:2307.09009]); refusal/policy measurement and over-refusal diagnosis (RefusalIndex, ContrastiveOverRefusal); judge-bias/format-confound literature (WildBench); model-pair attribution instruments requiring internal access (FewTokensDeep, DiffInterpretation, MoreRLHFMoreTrust); downstream breakage from undifferentiated version drift (CARLoRA).
- **In scope:** measuring/attributing drift for already-shipped model pairs via black-box behavioral probes, calibrated against constructed control pairs. **Out of scope:** training new models to reduce drift; any attribution method requiring logits, weights, or training data for the commercial pairs of primary interest; live/streaming monitoring systems.
- **Confidence: high.** Like the B5.5 exemplar, the "repo" here is itself a prior reverse-digest plus a pre-registered spec (`digest.md` + `paper.md`) that already cross-references N-nodes ↔ M-components ↔ RQ ids and already carries its own asymmetry/taste self-audit (`paper.md` Step 0/3). Reconstruction risk is low; the risk is *redundancy* with `paper.md`'s own Steps 5/6, so stages 5/6 below are framed as re-deriving the same design from this schema's own discipline (method-leak-free problem/motivation, sub-problems traced to specific limitations, hypotheses stated independently of the eventual RQ list) rather than copy-pasting `paper.md`'s notation wholesale.

---

## Stage 1 — Problem Definition

### Round 1 (critic phase)

**draft_v1** (proposer):
- `summary`: Given a pair of LLM versions from the same provider, both accessible only through their ordinary input/output interface, determine how much of the observed behavioral difference between the two versions is attributable to a change in capability, a change in alignment/policy, or a change in output format/style preference — and determine whether the resulting attribution profile is shared across different providers or specific to each one.
- `input`: (1) a set of same-provider LLM version pairs, each queryable only through its ordinary text interface; (2) for at least a subset of pairs, an independently known dominant cause of change, constructed so that ground truth is available; (3) repeated queries to each version under identical conditions, used to characterize within-version behavioral variability.
- `output`: (1) for each real version pair, an attribution of the observed behavioral difference across the three candidate sources; (2) an estimate of how reliably the attribution procedure recovers the correct dominant source when the true source is known by construction; (3) a comparison of whether the attribution profile is common across providers or differs from one to the next.
- `constraints`: the version pairs of primary interest are accessible only via ordinary text input/output — no model internals, training data, or vendor documentation of what changed is available; there is no ground truth for which source caused a given real pair's difference, so validity must be established indirectly, via pairs where the cause is known by construction.
- `objective`: an attribution is accepted as informative only if the underlying procedure demonstrably recovers the correct dominant source, on pairs of independently known cause, at a rate clearly above chance; if it does not, no claim about real pairs' attribution — or about cross-provider structure — is warranted.
- `study_type`: `empirical` — stated explicitly, not silently inferred: the seed's own core question ("多少来自能力变化、多少来自对齐/政策调整、多少只是格式偏好漂移") and digest N12 already settle this as a measurement/attribution study, not a proposed fix to drift itself.

**critique:**
- summary: Strong, evidence-traceable draft — no method leak, `study_type` correctly gated — but the `objective` silently assumes the three candidate sources exhaust 100% of any observed difference, and the draft never states what a pair boundary is.
- comments:
  - `{severity: major, field: "objective", anti_pattern: "vague_success (evaluability gap)", comment: "The objective specifies a calibration bar but never says what happens to the portion of an observed difference that is neither cleanly capability, policy, nor format — nor to the portion indistinguishable from ordinary within-version noise. Digest N5's own C3/C5 and N6's M4 already treat 'leakage' and 'noise floor' as first-class, separately reported quantities, not residuals silently folded into the three named buckets. Without naming this in the objective, a reported '60% capability / 30% policy / 10% format' is not evaluable as written — a reader cannot tell whether the split exhausts the difference by construction or by finding."}`
  - `{severity: minor, field: "input/summary", anti_pattern: null, comment: "'a pair of LLM versions' is never bounded to mean two *directly adjacent* shipped snapshots. Without this, a reader could read 'pair' as spanning several intermediate releases, which would silently reintroduce multi-hop drift the digest's own feasibility section (N6) explicitly scopes out by selecting only pairs where both snapshots are currently, simultaneously served."}`
- decision: `move_to_refiner` (both flags are formalize-level fixes using content already in the digest — no new content needed).

### Refiner pass

- `objective` (refined): "An attribution is accepted as informative only if (a) the procedure demonstrably recovers the correct dominant source, on pairs of independently known cause, at a rate clearly above the one-in-three chance baseline, with a stated bound on cross-source leakage; and (b) for any given real pair, the portion of the observed difference that is neither confidently attributable to a single source nor distinguishable from ordinary within-version noise is reported as its own quantity — leakage and noise floor are first-class, reportable outcomes of the procedure, never silently absorbed into the three named sources so that they appear to sum to the whole difference by fiat. If (a) fails, no claim about real pairs' attribution, or about cross-provider structure, is warranted, and that failure is itself a reportable finding about whether such attribution is possible from behavior alone."
- `input`/`summary` (refined): "a pair" is defined explicitly as two directly comparable, adjacent shipped snapshots from the same provider (not a chain spanning multiple intermediate releases), both simultaneously queryable over the study window.
- `formal_summary` (added, per stage-1 refiner's formalize-for-free duty): "Pair P = (v_old, v_new), same provider, both text-in/text-out only. Candidate sources a ∈ {cap, pol, fmt}. For each source a, an axis share η²_a(P) is estimated from repeated, identical queries to both versions; a leakage share λ(P) and a within-version noise floor σ²_w(P) are estimated and reported separately, not folded into {η²_a}. Recovery accuracy Acc is the fraction of independently-constructed pairs (known dominant axis by construction) for which the procedure's predicted dominant axis matches the true one."
- `changes_made`: tightened `objective`'s evaluability condition to name leakage/noise as first-class outputs; bounded what counts as "a pair"; added `formal_summary`.
- `declined_to_fix`: none.

**Confirmed Stage 1** — `study_type: empirical`.

---

## Stage 2 — Motivation

### Round 1 (critic phase)

**draft_v1:**
- `summary`: Providers ship new model versions frequently and users observe behavioral change, but are never told which of three very different things happened underneath — the model got smarter, its safety/alignment posture shifted, or nothing except its default formatting habits changed — and these three have completely different, and completely un-interchangeable, downstream consequences for whoever integrates the model.
- `why_it_matters`: A capability change calls for re-benchmarking task performance; a policy change calls for re-auditing safety/compliance posture; a format change calls for nothing more than fixing a brittle parser — but a single blended before/after score cannot tell these apart, so an integrator who trusts the blended number risks either wasted re-qualification effort or, worse, a missed policy regression that a spurious "it's just formatting" explanation papers over. This is not a hypothetical failure mode: the canonical longitudinal audit of ChatGPT's behavior over time found that part of an apparent capability regression in code generation was in fact caused by newly added markdown fencing breaking an executability check — a format change that got scored and reported as a capability loss (paper.md Step 0; digest N4). If today's standard longitudinal audits cannot reliably rule this out, every headline claim of the form "model X's capability degraded between snapshots" is potentially confounded by exactly the surface artifact this paper is built to separate out.
- `who_cares`: Downstream integrators deciding whether to re-benchmark, re-audit, or merely patch a parser after a version bump; researchers running longitudinal LLM audits who need to know whether their measured deltas are trustworthy; the broader research community deciding whether version-to-version change has a common cross-vendor "shape" worth standardizing an audit taxonomy around, or must remain fully vendor-specific.
- `evidence`: `[ChatGPTBehavior, arXiv:2307.09009]`'s own reported finding that a code-generation performance drop was partly attributable to markdown-fencing breaking an executability check; `[CARLoRA, OpenReview:5GimteSrgW]`'s motivation that downstream adapters silently break under undifferentiated version drift, forcing full retraining rather than a targeted fix; `[WildBench, OpenReview:MKEHCx25xp]`'s own finding that judge-based evaluation is systematically biased by surface length/style, requiring an explicit length-penalized metric — independent evidence that format-axis confounds are a documented measurement problem, not a hypothetical one.

**critique:**
- summary: Good stake-specific motivation with real, load-bearing citations, but coverage of stage 1's outputs is incomplete.
- comments:
  - `{severity: major, field: "why_it_matters", anti_pattern: "partial_output_coverage", comment: "Stage 1 output (3) is a cross-provider structural comparison — a claim about whether the taxonomy generalizes, not just about any one pair. why_it_matters fully motivates outputs (1)/(2) (the per-pair attribution and its reliability) but never explains why it is worth knowing whether the attribution structure is *shared or vendor-idiosyncratic*, as opposed to treating each vendor's audit as its own bespoke problem. A reader could reasonably ask 'why does it matter whether the structure generalizes across vendors, if each vendor's pairs are already separately attributed' — and that gap is real and currently unaddressed."}`
- decision: `move_to_refiner`.

### Refiner pass

- `why_it_matters` (extended): "...and this generalization question is itself decision-relevant, not merely descriptive curiosity: if the axis-dominance structure recurs across vendors, longitudinal-audit practice could standardize a single 'what changed' reporting taxonomy usable industry-wide, sharply cutting the cost of building a bespoke instrument per vendor from scratch. If it does not recur, that is itself a decision-relevant finding — auditors must budget for a vendor-specific instrument rather than assuming any one vendor's recipe transfers, an ambiguity practitioners currently have no evidence to resolve either way."
- `changes_made`: added the cross-provider generalization stake explicitly, tied to a concrete practical consequence (standardize vs. budget-per-vendor) rather than restating "generalization is interesting."
- `declined_to_fix`: none.

**Confirmed Stage 2.**

---

## Stage 3 — Related Work

All eight works below are treated as **specific (deep) tier** — the digest's own N3/N4 already engaged each one at the approach + limitation level (no title-only landscape mentions were present in the source material, and per the no-fabrication rule, no additional landscape papers are invented here to pad a `general_related_works` list).

### Round 1 (critic phase)

**draft_v1** (`specific_related_works`, abbreviated to citation / I-O framing / limitation / `is_potential_baseline`):

| work_id | citation | is_potential_baseline | limitation (→ sub-problem it will motivate) |
|---|---|---|---|
| `rw_chatgptbehavior` | Chen, Zaharia & Zou, "How Is ChatGPT's Behavior Changing over Time?" (arXiv:2307.09009) | **true** | Reports a single blended per-task delta between snapshots with no mechanism to attribute it to capability, policy, or format — and its own reported code-generation drop was partly a scored-as-capability format artifact (markdown fencing breaking executability); single-vendor, no cross-vendor test. |
| `rw_morerlhf` | Anon., "More RLHF, More Trust?" (OpenReview:FpiCLJrSW8) | false (needs white-box training-stage access) | Attributes behavioral change to training stages via influence-function data attribution requiring checkpoints and training data neither available nor applicable to black-box commercial version pairs; covers only trustworthiness dimensions, no capability or format axis. |
| `rw_fewtokensdeep` | Anon., "Safety Alignment Should Be Made More Than Just a Few Tokens Deep" (OpenReview:6Mxhg9PtDE) | false (needs logit access) | Per-token KL-divergence attribution requires logit access to both models in the pair, unavailable for commercial APIs; characterizes one axis (safety depth) in isolation rather than apportioning drift across competing axes. |
| `rw_refusalindex` | Anon., "Can LLMs Refuse Questions They Do Not Know?" (OpenReview:9gJBhkLRat) | **true** | Computes a within-model, single-time-point separation of refusal propensity from knowledge limitation; has no version-pair or drift framing at all. |
| `rw_contrastiveoverrefusal` | Anon., "Discern Truth from Falsehood" (OpenReview:GXcN0MuN1q) | false (representation-space, single-model fix) | Diagnoses policy/format coupling in internal representation space (requires model-internal access) and aims to fix one model's over-refusal, not to measure drift between two deployed versions. |
| `rw_wildbench` | Anon., "WildBench" (OpenReview:MKEHCx25xp) | false (single-time-point leaderboard) | Treats surface length/style as a nuisance bias to penalize away inside a ranking metric rather than a first-class, separately reported axis; produces a single-time-point leaderboard, not a paired version-to-version drift attribution. |
| `rw_diffinterpretation` | Anon., "Learning to Interpret Weight Differences in Language Models" (OpenReview:6As4wfTB77) | false (needs weight access) | Requires access to both models' weights to compute a diff; produces an open-ended natural-language description of the change rather than a share apportioned across a fixed, comparable taxonomy. |
| `rw_carlora` | Anon., "CAR-LoRA" (OpenReview:5GimteSrgW) | false | Treats version drift as an undifferentiated perturbation to train adapters robust against, rather than diagnosing what changed; offers no diagnostic signal to a downstream integrator about a specific update. |

**critique:**
- summary: Grounding is solid, every limitation is specific (not "scalability issues"-style vagueness), but one baseline label needs scrutiny.
- comments:
  - `{severity: major, field: "specific_related_works[rw_refusalindex].is_potential_baseline", anti_pattern: "io_approach_mismatch", comment: "RefusalIndex's I/O framing is a within-model, single-time-point calibration measure — genuinely different from this paper's cross-version, paired-comparison framing. Per the stage-3 rubric, a mismatched-I/O work is 'not a baseline — at best a method-side reference.' Marking it a straightforward baseline risks implying RefusalIndex's own reported numbers are being compared against, which they are not."}`
- decision: `move_to_refiner` (a wording-precision fix, not a structural one — the underlying rank-correlation *protocol* is still legitimately reusable).

### Refiner pass

- `rw_refusalindex.is_potential_baseline` retained as `true`, but the field's accompanying note is sharpened: "Not a baseline in the beat-a-number sense — RefusalIndex is computed within a single model at one time point, not across a version pair, and its own reported numbers are never compared against. Its **rank-correlation protocol for separating refusal propensity from knowledge limitation** is borrowed as a design pattern for keeping this paper's policy probe battery analytically distinct from its capability battery, independent of RefusalIndex's own published findings."
- `changes_made`: clarified RefusalIndex's baseline role to avoid an implied I/O-mismatched comparison.
- `declined_to_fix`: none.
- **Note on `verify_as_hypothesis`:** set `false` on every limitation. None is promoted to a stage-6 framing-tier RQ — the two candidate cross-vendor/calibration questions (whether structure generalizes; whether the instrument is reliable) are already the paper's own core mechanism-tier hypotheses (Stage 5/6 below), not a distinct framing check borrowed from someone else's limitation. Per stages.md: *"If nothing was flagged, emit zero framing-tier RQs — don't manufacture one."*

**Confirmed Stage 3.**

---

## Stage 4 — Sub-Problems

### Round 1 (critic phase)

**draft_v1** (4 sub-problems, from digest N5's C1, C3, C4, C5):

- **`sp_entangled_causes`** — *description:* Determine, for a given behavioral change between two versions, how to attribute it among capability, policy, and format causes when any single cause (or combination) can produce the same observed difference and no real version pair carries a known ground-truth cause. *why_it_is_a_problem:* any attribution claim is unfalsifiable without some independent check, because the true cause of a real pair's change is never directly observed. *technical_challenge:* the three causes are not orthogonal in raw behavior — a policy change can alter response length (looking like format), a capability change can alter refusal correctness (looking like policy) — so untangling requires probes engineered to hold two causes approximately fixed while measuring the third, plus an external validity check on cases where the true cause is independently known. *source_limitation_ids:* `["__novel__"]`.
- **`sp_leakage_measurement`** — *description:* Quantify, rather than assume, how much cross-contamination exists between probes nominally designed to isolate one axis, so reported axis shares are not silently biased by unacknowledged leakage. *why_it_is_a_problem:* a probe intended to isolate one axis can still be contaminated by another axis in a way invisible from the probe's own output alone. *technical_challenge:* leakage cannot be observed directly on real pairs (the true source is unknown), so it must be estimated indirectly via cross-axis regression and validated where ground truth is known. *source_limitation_ids:* `["lim_wildbench_nuisance_bias"]`.
- **`sp_noise_vs_drift`** — *description:* Separate a genuine between-version behavioral change from ordinary within-version run-to-run variability before attributing any of it to capability, policy, or format. *why_it_is_a_problem:* without this separation, sampling noise could be misclassified as drift, or a real drift could be masked, corrupting every downstream axis-share estimate. *technical_challenge:* LLM outputs are stochastic and serving infrastructure can silently shift mid-study, so isolating a stable per-version noise floor requires repeated, interleaved sampling and a way to detect infra drift contaminating the noise estimate itself. *source_limitation_ids:* `["__novel__"]`.
- **`sp_cross_vendor_comparability`** — *description:* Determine whether an attribution structure found for one vendor's version pairs is meaningfully comparable to another vendor's, given that vendors may implement conceptually similar changes (e.g., a refusal rule) through different underlying mechanisms (a policy layer vs. a system prompt vs. an output filter). *why_it_is_a_problem:* without addressing this, any finding of shared or vendor-idiosyncratic structure could just as easily be an artifact of how the axes happen to be operationalized as a real fact about the industry. *technical_challenge:* vendor-internal mechanisms are never directly observable (black-box), so commensurability itself has to be tested behaviorally — by applying an identical instrument to every vendor and checking empirically whether comparable patterns emerge, rather than assumed by definitional fiat. *source_limitation_ids:* `["__novel__"]`.

**Note on the excluded challenge (C2):** digest N5's C2 (commercial pairs are irreducibly black-box) is deliberately **not** promoted to a sub-problem here. A sub-problem is something later stages must solve; digest N6 itself already lists C2 as an `unaddressed_challenge` — no method in this pipeline resolves black-box opacity for commercial pairs, and `sp_entangled_causes`'s calibration only bounds the resulting uncertainty rather than eliminating it. Promoting C2 to a sub-problem would misleadingly imply this paper has, or needs, a fix for vendor opacity. It instead remains a first-class stated constraint (Stage 1 `constraints`) and a self-flagged limitation carried through to the Conclusion.

**critique:**
- summary: Coverage checks out (solving all four would jointly deliver stage 1's objective, modulo the explicitly excluded C2); one pair of sub-problems risks reading as the same underlying issue twice.
- comments:
  - `{severity: minor, field: "sp_entangled_causes / sp_leakage_measurement", anti_pattern: "overlap", comment: "Both invoke 'cross-axis contamination,' which can read as the same sub-problem stated twice. They are genuinely distinct — one is about whether attribution is possible *in principle* on real pairs with no ground truth (an identifiability problem, resolved only indirectly via calibration), the other is about *quantifying* imperfect probe isolation as a bounded, measured number (an instrumentation problem) — but the descriptions don't make that distinction explicit enough."}`
- decision: `move_to_refiner`.

### Refiner pass

- `sp_entangled_causes.technical_challenge` sharpened to end with: "...this is an **identifiability** problem — whether attribution is possible at all without ground truth — not a measurement-precision problem; it can only be addressed indirectly, by checking the procedure's reliability on pairs where the cause happens to be known."
- `sp_leakage_measurement.technical_challenge` sharpened to end with: "...this is a **bounded-quantification** problem distinct from identifiability — even once a procedure is judged reliable overall, the *residual* cross-contamination in any given estimate still needs its own reported number, not an assumption of zero."
- `changes_made`: made the identifiability-vs-quantification distinction explicit in both `technical_challenge` fields.
- `declined_to_fix`: none.

**Confirmed Stage 4** (4 sub-problems; 1 sourced from a related-work limitation, 3 `__novel__` with stated decisive-component justifications; C2 explicitly excluded with a recorded rationale).

---

## Stage 5 — Method Design

### Round 1 (critic phase)

**draft_v1** (4 methods):

- **`m_battery_design_and_calibration`** → targets `sp_entangled_causes`. *proposed_approach:* Build three probe batteries, each engineered so the other two axes have minimal effect on its measured quantity by construction (format-robust scoring for capability; near-ceiling-correct prompts for format; harmfulness-stratified prompts for policy). Independently, construct control pairs by deliberately modifying only one axis at a time (base model vs. domain-SFT for capability; base vs. safety-SFT for policy; identical weights with an altered system template for format), so — unlike any real vendor pair — the true dominant cause is known. Run the complete, unmodified pipeline blind (pair identities withheld from the analysis code) on these control pairs and check whether the predicted dominant axis matches the true one. *key_insight:* Entanglement can never be resolved analytically on real pairs, because no real pair carries a verifiable ground-truth cause — but a decomposition procedure's *reliability* can still be checked indirectly, on constructed pairs where the cause is known, using the exact same batteries and model later applied blind to real pairs. A pass licenses trusting the procedure on real pairs, within a stated calibration bound; a failure means no claim about real pairs is warranted, and that failure is itself the reportable finding. *hypotheses:* ["On format-only constructed control pairs (identical weights, altered template only), the capability battery's per-item correctness delta and the policy battery's refusal-rate delta are each not significantly different from their own within-version noise floor.", "Across at least 9 constructed control pairs (3 per axis), the blind decomposition procedure recovers the true dominant axis in at least 8 of 9 cases, with mean leakage share below 0.15."]
- **`m_leakage_regression`** → targets `sp_leakage_measurement`. *proposed_approach:* Regress each item's capability-battery delta on that item's format-feature deltas, and each item's policy-battery delta on lexical/surface cues, to estimate what fraction of the nominally capability or policy signal is actually explained by surface-form covariates; report this explained fraction as an explicit leakage share attached to the pair, rather than letting it silently inflate the capability or policy share. *key_insight:* Leakage is invisible from a probe's own output — an axis that leaks looks identical, from inside its own measurements, to one that doesn't — so it can only be surfaced by explicitly regressing one axis's signal on another axis's independently measured features, turning "the batteries are orthogonal" from an assumption into a reported, falsifiable number. *hypotheses:* ["The estimated cross-axis leakage share, measured via regression of capability/policy deltas on the other axes' independently measured features across the constructed control pairs, averages below 0.15 — the same threshold the calibration gate requires for the decomposition to be considered valid."]
- **`m_noise_floor_model`** → targets `sp_noise_vs_drift`. *proposed_approach:* Sample each probe item k=5 times per version at fixed decoding settings to estimate the within-version run-to-run variance for that version and item; fit a mixed-effects model with axis as fixed effect and item as random effect over the resulting per-item deltas, so an axis's estimated contribution to observed drift counts only the portion in excess of this pooled within-version variance floor; query both versions of a pair in interleaved time windows and compare early-half vs. late-half noise estimates to detect silent infra changes that would otherwise contaminate the floor itself. *key_insight:* A version-to-version delta is only evidence of drift if it exceeds what the same version alone would produce on repeated queries; treating the raw observed delta as if it were already the noise floor is exactly what would let ordinary sampling variability masquerade as a false drift finding. *hypotheses:* ["For every tested version pair, the fitted within-version noise floor is stable across interleaved query windows (early-half estimate within 20% of the late-half estimate).", "In at least 4 of 6 tested real version pairs, at least 2 of the 3 axes' contributions significantly exceed the estimated noise floor, and the format axis's share is at least 10% of explained drift in at least 3 of 6 pairs."]
- **`m_cross_vendor_agreement_test`** → targets `sp_cross_vendor_comparability`. *proposed_approach:* Summarize each version pair's decomposition as a point on the three-way simplex of axis shares; test cross-vendor structure two ways — a rank-agreement statistic (Kendall's W) over which axis dominates within each vendor's pairs, tested against a permutation null, and a clustering analysis of the simplex points to check whether pairs group by vendor identity or mix across vendors. *key_insight:* Commensurability across vendors can't be verified from vendor internals (black-box), but it can be tested behaviorally: if an identical instrument, applied identically to every vendor's pairs, produces a rank-ordering of axis dominance that agrees across vendors more than a random permutation would, that is evidence the three axes behave as a shared construct rather than three vendor-specific artifacts of how the instrument happened to be built. *hypotheses:* ["The rank-ordering of axis dominance across version pairs, grouped by vendor, agrees significantly more than chance (Kendall's W ≥ 0.60 against a permutation null, p<0.05) across at least 6 pairs from at least 3 vendors, and pairs do not cluster tightly by vendor identity on the axis-share simplex beyond what the permutation null would produce."]

**critique:**
- summary: Every method has a real mechanism (no goal-restatement), every hypothesis is falsifiable with a stated threshold — but two methods (`m_battery_design_and_calibration`, `m_noise_floor_model`) each carry two hypotheses and need a one-line justification for why that's one mechanism, not two bundled together.
- comments:
  - `{severity: minor, field: "m_battery_design_and_calibration.hypotheses / m_noise_floor_model.hypotheses", anti_pattern: null, comment: "In each case, one hypothesis is an instrument-validity precondition and the other is closer to the paper's headline empirical claim. Worth stating explicitly why each pair comes from one mechanism rather than reading as two unrelated claims stapled into a single method entry."}`
- decision: `move_to_refiner`.

### Refiner pass

- `m_battery_design_and_calibration.key_insight` extended: "...the same battery-plus-pipeline yields two separately falsifiable readouts from one design: whether the batteries are orthogonal-by-construction on format-only controls (a diagnostic precondition) and whether the full pipeline recovers the true dominant axis blind across all constructed controls (the actual calibration gate) — one instrument, two checks on it, not two mechanisms."
- `m_noise_floor_model.key_insight` extended: "...one estimated noise floor licenses two distinct, separately falsifiable readouts: whether the floor itself is stable enough to trust as a reference (a precondition on the instrument) and, once trusted, whether real-pair axis contributions actually clear it (the paper's substantive empirical finding) — the same fitted model, read two ways."
- `changes_made`: justified both two-hypotheses-one-method structures explicitly.
- `declined_to_fix`: none.

**Confirmed Stage 5** — 4 methods, **6 hypotheses total** (2 + 1 + 2 + 1 across the four methods respectively), mixing instrument-validity claims with the study's headline empirical prediction — a deliberate design choice for an `empirical` study_type, explained in the stage-6 header below.

---

## Stage 6 — Experiment Design

**Tier accounting (checked against study_type=empirical):**
- **Mechanism-tier: 6 RQs**, one per Stage 5 hypothesis (verbatim `target_hypotheses`).
- **Framing-tier: 0 RQs** — no Stage 3 limitation was flagged `verify_as_hypothesis`; none manufactured.
- **Outcome-tier: 0 RQs** — `study_type = empirical` forbids "our procedure beats baseline X" framing. Baselines below are sanity-check / misattribution-demonstration comparators only, never a competitor to beat.

### Round 1 (critic phase)

**draft_v1:**

`datasets`:
- GSM8K, MMLU-Pro, HumanEval (capability, execution/exact-match scored) — *justification:* objectively verifiable, format-robust-scorable tasks that anchor the capability battery.
- XSTest, OR-Bench-Hard-1K, SORRY-Bench (policy, harmfulness-stratified) — *justification:* the three strata (safe-but-seemingly-unsafe / pseudo-harmful / genuinely harmful) let a refusal-rate change be read against a fixed ground-truth harmfulness reference.
- IFEval (format, instructed-format compliance) — *justification:* directly measures instructed-format adherence, complementing the near-ceiling-correct prompt pool used for the rest of the format battery.
- (draft initially listed LiveCodeBench with justification only "digest mentions it as contamination-resistant" — flagged below.)

`baselines` (sanity-check/misattribution-demonstration comparators, not outcome-tier competitors):
- Blended-delta audit (the `[ChatGPTBehavior, arXiv:2307.09009]` design) — run on format-only control pairs to demonstrate whether standard practice actually misattributes pure format drift as capability/policy change.
- Null-pair placebo (the same snapshot queried twice, in disjoint interleaved windows) — the pipeline must find no axis exceeding the noise floor; any positive "detection" is a pipeline artifact, not evidence of the phenomenon.
- Two-way ablation (capability+policy decomposition with the format axis removed) — run on format-only control pairs to show the third axis is load-bearing, not decorative.

`research_questions` (6, all mechanism-tier):

| rq_id | target_sub_problem_id | target_hypotheses (verbatim) |
|---|---|---|
| `rq_orthogonality_precondition` | `sp_entangled_causes` | "On format-only constructed control pairs (identical weights, altered template only), the capability battery's per-item correctness delta and the policy battery's refusal-rate delta are each not significantly different from their own within-version noise floor." |
| `rq_calibration_recovery` | `sp_entangled_causes` | "Across at least 9 constructed control pairs (3 per axis), the blind decomposition procedure recovers the true dominant axis in at least 8 of 9 cases, with mean leakage share below 0.15." |
| `rq_leakage_bound` | `sp_leakage_measurement` | "The estimated cross-axis leakage share, measured via regression of capability/policy deltas on the other axes' independently measured features across the constructed control pairs, averages below 0.15 — the same threshold the calibration gate requires for the decomposition to be considered valid." |
| `rq_noise_floor_stability` | `sp_noise_vs_drift` | "For every tested version pair, the fitted within-version noise floor is stable across interleaved query windows (early-half estimate within 20% of the late-half estimate)." |
| `rq_axis_decomposition_finding` | `sp_noise_vs_drift` | "In at least 4 of 6 tested real version pairs, at least 2 of the 3 axes' contributions significantly exceed the estimated noise floor, and the format axis's share is at least 10% of explained drift in at least 3 of 6 pairs." |
| `rq_cross_vendor_structure` | `sp_cross_vendor_comparability` | "The rank-ordering of axis dominance across version pairs, grouped by vendor, agrees significantly more than chance (Kendall's W ≥ 0.60 against a permutation null, p<0.05) across at least 6 pairs from at least 3 vendors, and pairs do not cluster tightly by vendor identity on the axis-share simplex beyond what the permutation null would produce." |

(setup/sample-size/statistical-test/expected-outcome/metrics per RQ carried into the paper draft's Experiments section below, reusing paper.md's already-designed E1/E2/E3/B0/B-alt numbers as authored design targets, not fabricated results.)

**critique:**
- summary: Tier accounting is clean and every RQ traces to a verbatim hypothesis, but one dataset justification is a citation to the digest instead of a real methodological reason.
- comments:
  - `{severity: major, field: "datasets[LiveCodeBench]", anti_pattern: "weak justification (not a named anti-pattern, but fails the rubric's 'justification for why this dataset actually stresses the hypothesis')", comment: "'digest mentions it as contamination-resistant' says nothing about which RQ needs contamination resistance or why it matters here specifically."}`
- decision: `move_to_refiner`.

### Refiner pass

- `datasets` entry replaced: "LiveCodeBench (capability, execution-scored, rolling release) — *justification:* its rolling-release design prevents a capability battery item from having differential training-data exposure across the two versions of a pair, which would otherwise confound a measured capability-axis change with a contamination artifact uncorrelated with true capability — exactly the kind of confound `rq_axis_decomposition_finding`'s capability-share estimate needs ruled out to be interpretable."
- `changes_made`: gave LiveCodeBench's inclusion a hypothesis-linked reason instead of a provenance note.
- `declined_to_fix`: none.

**Confirmed Stage 6.**

---

## Cross-stage consistency check (final pass, all six stages)

1. **No method leak** in stages 1/2/4 — checked; `objective`/`why_it_is_a_problem` fields name no technique.
2. **ID stability** — no id renamed mid-run; `sp_*` / `m_*` / `rq_*` stable stage-to-stage.
3. **Reference integrity** — `sp_leakage_measurement.source_limitation_ids = ["lim_wildbench_nuisance_bias"]` ∈ Stage 3 limitations ✓; all other `source_limitation_ids = ["__novel__"]` ✓; every `target_sub_problem_id` in Stage 5 ∈ Stage 4 ✓; every Stage 6 `target_hypotheses` is a verbatim match to a Stage 5 hypothesis ✓.
4. **Output coverage** — Stage 1's three outputs (per-pair attribution + ambiguity/noise accounting, calibration reliability, cross-provider comparison) are each reachable: attribution/reliability via `sp_entangled_causes` + `sp_leakage_measurement` + `sp_noise_vs_drift`, cross-provider comparison via `sp_cross_vendor_comparability` — nothing promised in Stage 1 falls off the chain by Stage 6.
5. **`study_type` consistency** — `empirical` throughout; Stage 6 correctly emits 0 outcome-tier RQs; baselines are explicitly framed as sanity/misattribution-demonstration comparators, never "beats."

**What was hardest:** the recurring tension was **scope discipline around C2** — repeatedly having to check whether a stage-4/5 artifact was quietly promising to *resolve* black-box opacity (which no method here does) rather than *bound* the uncertainty it creates. The digest itself already commits to leaving C2 as an unaddressed challenge (N6), and the temptation at Stage 4 was to fold it into `sp_entangled_causes` anyway since the two are closely related; keeping them separate — one a sub-problem this paper solves, one a limitation this paper states and lives with — is exactly the kind of discipline this schema is built to enforce. A secondary tension was deciding which hypothesis carries the paper's actual headline empirical claim (that format share is non-negligible in real pairs): it was tempting to invent a fifth, freestanding method for it, but the more honest move — mirroring how the noise floor is the precondition for *any* drift claim — was recognizing it as the second, substantive readout of the same noise-floor model that also validates the floor's own stability.

**Total rounds:** 6 stages × 1 critic round + 1 refiner pass = 6 critic rounds, 6 refiner passes. No stage hit the round cap; no cross-stage backup was required.


---

## Post-review revision round (2026-07-05)

Revision pass over the completed pipeline's review artifacts (`stage_review.md`, `taste_audit.md`; no `design_review.md` exists for this topic). Every finding in those files was enumerated and statused against the current deliverables; findings already applied or logged as resolved in `pipeline.md` were left alone. Outcomes:

1. **stage_review.md → Stage 2 REVISE (nearest-neighbor sentence)** — already applied (Introduction para 3 and Related Work opening name ChatGPTBehavior as the closest prior work with the delta stated plainly). No change.
2. **stage_review.md → Stage 4 REVISE (per-RQ falsification conditions)** — already applied (all six RQ subsections carry a Falsification condition line). No change.
3. **stage_review.md → Phase A items 1/2/5/6 (digest absence-comment trailers; reference-cache backfill; A8/PG-* machinery; R1/R2/R6 method-rigor fixes)** — already applied in `digest.md`/`paper.md`; residual reference gap closed by the 2026-07-04 remediation (13/14 selected entries resolvable; CAR-LoRA logged as the honest exception). No change.
4. **stage_review.md → Phase F [major] (zero \cite / no refs.bib)** — already fixed 2026-07-04 (refs.bib script-generated, 8 citations wired, clean compile). No change.
5. **stage_review.md → Phase F/G [minor] (6 `adjacent` selected cache entries uncited; weave the most on-point into the Introduction's motivation)** — **OPEN → applied.** Added one sentence to Introduction paragraph 2 citing `HowandWhyLLMsGeneralizeA4063` (blended SFT-vs-RL accuracy deltas conceal a decomposable shift in reasoning-skill composition — the same aggregate-number-hides-separable-causes structure along a training-method axis), phrased strictly from the cache record's verified `why` field. Changed in `paper_draft.md` and `paper_draft.tex`; recompiled clean (13 pages, no undefined citations). The other 5 `adjacent` entries remain uncited by design — the review asked for "1-2 of the most on-point ones" and named only this one; force-citing the rest would be citation padding.
6. **stage_review.md → Phase G [minor] (A8/PG-7 power/INCONCLUSIVE carve-out absent from RQ5/RQ6 falsification prose)** — **OPEN → applied.** Added the carve-out to RQ5 (18-cell numerator/denominator exclusion, INCONCLUSIVE never a pass/fail/silent drop) and RQ6 (dominance ranks entering Kendall's W inherit the rule), plus RQ2 (reduced-denominator rule for the 8/9 bar) so the draft matches `experiment_design.md`'s existing carve-out blocks and `paper.md` H3/H1. Changed in `paper_draft.md` and `paper_draft.tex`; mirrored one inherited carve-out line into `experiment_design.md`'s `rq_cross_vendor_structure` block (grounded in paper.md A8's "pre-declared INCONCLUSIVE for H1/H2/H3 scoring") so draft and design stay cross-consistent. Target hypotheses left byte-identical to `paper.md`'s.
7. **taste_audit.md → phrasing-trap warning (avoid reframing as "bringing mixed-effects modeling into LLM auditing")** — **rejected as moot**: advisory only, and the current draft mentions the mixed-effects model solely as a method detail inside the noise-floor module, never as the contribution framing. No change needed.
8. **stage_review.md → Phase A residual (6 backfilled OpenReview digests unresolvable)** — logged as resolved in `pipeline.md` (2026-07-04 remediation). No change.

Cross-deliverable consistency after this round: 6 RQs in both `paper_draft.md` and `experiment_design.md`; effect floors (leakage 0.15, format share 0.10), margins (noise-floor 20%, recovery 8/9 vs 1/3, W ≥ 0.60 at p < 0.05, ≥6 pairs / ≥3 vendors, k = 5, 10,000 permutation draws) match across both and `paper.md`. Compile: `latexmk -pdf` exit 0, 13 pages, zero undefined citations.
