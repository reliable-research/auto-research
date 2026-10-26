# Discussion Trace — B6.4 (Auto-Research-Discussion, Stages 1-6)

> Complete round-by-round record of the `auto-research-discussion` six-stage critic/refiner loop for this topic, extracted verbatim from `pipeline.md` (formerly its "## Seed brief" through "## Cross-stage consistency check" sections) per the skill's updated "Final deliverables" spec (three separate artifacts: `paper_draft.md`, `experiment_design.md`, `discussion_trace.md`). No content below was regenerated or altered — this is a move, not a re-run. `pipeline.md` itself now retains only the Phase Log / goal.md phase-gate bookkeeping and a pointer back here.

> Mode: **autoclaude** (self-play, Claude as student+teacher). Source: `../digest.md` (N0-N12) + `../paper.md` (Steps 0-9), both pre-existing reverse-digest artifacts for seed **B6.4**. Round cap: 5/stage (none hit). All six stages converged in 1 critic round + 1 refiner pass each — the seed material was unusually mature (`paper.md` already runs its own asymmetry derivation, taste self-audit, formal notation, assumptions ledger, and five pre-registered experiments with fallbacks), so genuine disagreement surfaced but didn't require re-proposing.
>
> **Full pipeline order:** this file (`auto-research-discussion`, 6 stages) → `taste_audit.md` (`research-taste-auditor`, idea-level check on Stage 2+5) → `stage_review.md` (`pengsida-stage-reviewer`, PASS/REVISE/STOP per stage against the confirmed outputs, plus a Stage 5 Writing check on the first assembled draft) → final `paper_draft.md`/`.tex`/`.pdf`. Two REVISE findings from `stage_review.md` (a dataset validity gap in the Experiments dataset table, and a missing explicit falsification-condition line format in the assembled draft) are already folded into the `paper_draft.*` files — read `stage_review.md` for the reasoning behind those fixes.

---

## Seed brief

- **One-sentence description:** Measure whether synthetic-text contamination injected into exactly one content domain (code, prose, mathematics, or dialogue) of a continued-pretraining corpus damages downstream capability more or less than the same dose injected into another domain, and rank domains by fragility.
- **Apparent inputs:** a domain-partitioned clean pretraining corpus (four shards); one or more in-domain synthetic-text generators; a sweep of single-domain contamination ratios; a domain-matched capability evaluation suite.
- **Apparent outputs:** a domain × ratio matrix of capability deltas relative to a clean control; a cross-domain vulnerability ranking with uncertainty; a generator-robustness / degeneracy-robustness verdict qualifying how intrinsic that ranking is.
- **Closest research areas:** model-collapse / recursive-training theory (MixRatio, IterStability, CrossModelRecursion, EntropyCollapse — all single global real/synthetic mixing-ratio framings); data-mixture optimization (DoReMi, RegMix — domain axis causally live but always assumed clean); synthetic-data reweighting at fine-tuning scale (SynthWeighting); domain-specific SFT capability retention (TALR).
- **In scope:** controlled single-domain contamination of a continued-pretraining corpus at up to ~3B model scale, measured via existing benchmarks. **Out of scope:** training a new mitigation method as the primary contribution; production-scale pretraining; domains beyond the four tested; non-text modalities.
- **Confidence: high.** As with a prior-reverse-digest seed, the "repo" here is itself a prior reverse-digest (`digest.md`) plus a pre-registered spec (`paper.md`) that already derived its own core asymmetry (Step 0), ran its own bridge/synthesis self-audit (Step 3), stated formal notation (Step 5) and assumptions (A1–A7), and pre-registered five experiments with fallbacks (Step 6, E1–E5). Reconstruction risk is low; the risk is redundancy with `paper.md`'s own Step 6, so stages 5/6 below are framed as re-deriving the same measurement apparatus **from the digest's N5 challenges upward**, independently checking that it lands on the same five hypotheses `paper.md` already committed to — not copying them uncritically.

---

## Stage 1 — Problem Definition

### Round 1 (critic phase)

**draft_v1** (proposer):
- `summary`: Given a domain-partitioned clean continued-pretraining corpus (code, mathematics, prose, dialogue shards) and one or more in-domain synthetic-text generators, and given a sweep of contamination ratios applied to exactly one domain shard at a time while all other shards and total token count stay fixed, determine whether the resulting downstream capability damage is uniform across domains or varies systematically with domain identity, and if it varies, produce a replicated cross-domain vulnerability ranking.
- `input`: (1) four domain shards from public per-domain sources, held clean except for the manipulated cell; (2) one or more contamination generators producing in-domain synthetic documents; (3) a ratio sweep applied to one domain at a time; (4) a domain-matched capability evaluation suite plus per-domain held-out validation loss.
- `output`: (1) a domain × ratio matrix of normalized capability deltas relative to a clean-control model; (2) a cross-domain vulnerability ranking of per-domain degradation slopes with uncertainty; (3) a robustness verdict on that ranking — whether it survives a second, independently-sourced contamination generator and a degeneracy-matched real-text control.
- `constraints`: only one domain shard is contaminated per training run; total token count and per-domain mixture proportions are held byte-identical across cells; the same base model, optimizer state, and training schedule are reused across all cells.
- `objective`: a vulnerability ranking is accepted as intrinsic to domain identity only if the domain × ratio interaction is statistically significant, the ranking is directionally consistent under two independent capability normalizations, it replicates across two independently-sourced contamination generators, and the damage exceeds a degeneracy-matched real-text control.
- `study_type`: `empirical` — stated explicitly, not silently inferred: digest N12 already classifies this as `empirical` ("a controlled measurement of an existing phenomenon... not the introduction of a new system, dataset, or benchmark"), and the seed's own core question ("哪类数据最脆弱") is a ranking/characterization question, not a proposed fix.

**critique:**
- summary: The problem is concretely scoped and traceable to the seed, but the `objective` bundles four logically distinct acceptance conditions into one all-or-nothing bar without saying what a partial result means.
- comments:
  - `{severity: major, field: "objective", anti_pattern: "vague_success (evaluability gap)", comment: "As drafted, 'accepted as intrinsic to domain identity only if [interaction significant] AND [directionally consistent] AND [generator-replicated] AND [exceeds degeneracy control]' collapses paper.md's own Claim-Evidence Map — which keeps Claim 1 (domain-selectivity), Claim 2 (directional ranking), and Claim 5 (generator/degeneracy robustness) as separately gradable claims with their own fallbacks (FB1, FB2, FB4, FB5) — into a single binary. If the interaction is significant and the ranking replicates across generators but does NOT clear the degeneracy-matched bar, is that 'domain-selective damage exists, ranking is real, but its syntheticness-specificity is unresolved' or a flat rejection of the whole objective? The draft doesn't say, and paper.md's own design clearly intends these to be gradable, separately reportable outcomes."}`
  - `{severity: minor, field: "output", anti_pattern: null, comment: "Output (3) is described as a single 'robustness verdict' but actually bundles two logically distinct checks (generator robustness and degeneracy robustness) that the digest's own N5 treats as separate challenges (C4 vs C1) — worth flagging for stage 4 to keep distinct, even if output-level phrasing stays combined for brevity."}`
- decision: `move_to_refiner` (both flags are formalize-level fixes using content paper.md already worked out — the Claim-Evidence Map already gives the right structure — no new content needed).

### Refiner pass

- `objective` (refined): "A vulnerability ranking's claims are graded, not binary: (i) *domain-selectivity exists* is established if the domain × ratio interaction is significant; (ii) *the specific ranking direction* is established, conditional on (i), if a pre-registered strict-versus-tolerant contrast holds under both capability normalizations; (iii) *the ranking is intrinsic to domain rather than to measurement artifact* is established, conditional on (i)+(ii), only if it replicates across two independently-sourced generators and exceeds a degeneracy-matched control. Each condition is reported and falsifiable on its own terms — failing (iii) alone does not retract (i)/(ii), it only narrows how strongly the ranking can be interpreted as domain-intrinsic."
- `formal_summary` (added, per stage-1 refiner's formalize-for-free duty, reusing `paper.md` Step 5's own notation): "Base corpus D = ⋃_{d∈𝔻} D_d, 𝔻 = {code, math, prose, dialogue}. Generator G produces in-domain synthetic documents. Contamination operator κ(D,d,r) replaces exactly an r-fraction of shard D_d's tokens with G-synthetic text, holding every other shard byte-identical and total token count fixed. θ(d,r,s): a model continued-pretrained on κ(D,d,r) with seed s, fixed schedule. S_d(·): domain-d capability metric of a checkpoint. Δ_d(r) = normalized capability delta of θ(d,r,s) relative to θ(d,0,s). β_d: OLS slope of Δ_d on r. Determine whether the domain × ratio interaction on {Δ_d(r)} is significant, and if so, whether the resulting ordering of {β_d} is directionally consistent, generator-stable, and degeneracy-robust."
- `changes_made`: split the single accept/reject objective into three separately gradable, ordered conditions; added a notation-reusing `formal_summary`.
- `declined_to_fix`: none.

**Confirmed Stage 1** — `study_type: empirical`.

---

## Stage 2 — Motivation

### Round 1 (critic phase)

**draft_v1** (proposer):
- `summary`: Downstream capability damage from synthetic contamination is plausibly not a property of the corpus as a whole but of the domain it lands in — domains with mechanically verifiable correctness structure (code, mathematics) may convert a subtly wrong synthetic document into corrupted supervision, while style-tolerant domains (prose, dialogue) may absorb the same dose as benign variation — and no existing framework can currently tell a practitioner whether this asymmetry is real.
- `why_it_matters`: The load-bearing claim is not "these two literatures haven't talked to each other" but the asymmetry candidate itself: if damage concentrates by domain the way correctness-strictness predicts, a global, domain-uniform contamination-filtering policy — the only kind current theory can even express — systematically over-protects tolerant domains and under-protects fragile ones; if the asymmetry is not real (the fallback), that is itself decision-relevant, because it means a single global threshold is *sufficient* and cross-domain filtering effort is wasted. The two adjacent literatures matter only as evidence that this asymmetry is currently unmeasurable, not as the motivation itself: model-collapse theory's global mixing-ratio abstraction has no domain axis to express it with, and data-mixture optimization's domain axis is assumed clean, never contaminated.
- `who_cares`: teams doing continued pretraining or domain-adaptive fine-tuning on web-scale corpora with unknown synthetic content; synthetic-data-generation vendors deciding which domains are safe to backfill; the model-collapse theoretical literature, whose global-mixing-ratio abstraction (MixRatio, IterStability) has no domain axis to be wrong or right about.
- `evidence`: `[MixRatio, OpenReview:9RdhTvYbX0]` and `[IterStability, OpenReview:JORAfH2xFd]`'s own risk analyses are stated over one homogeneous distribution with no domain decomposition; `[DoReMi, OpenReview:lXuByUeHhd]` and `[RegMix, OpenReview:5BjQOUXq7i]`'s own results establish that per-domain composition materially shifts downstream capability — proving the domain axis is causally live — while both explicitly assume the domain shards being weighted are clean. Neither line crosses contamination with domain (digest N3's search across 11,683 corpus entries surfaced no paper that manipulates domain identity as an independent contamination variable) — itself evidence the question is open, not merely unasked.

**critique:**
- summary: The asymmetry is correctly foregrounded (not a bridge framing) and the evidence is real, but the motivation only explains why domain-selectivity itself matters, never why a practitioner should care about the *robustness* conditions (generator-replication, degeneracy-matching) that Stage 1's output (3) promises.
- comments:
  - `{severity: major, field: "why_it_matters", anti_pattern: "partial_output_coverage", comment: "Stage 1 output (3) is a robustness verdict on the ranking — whether it survives a generator swap and a degeneracy-matched control. The motivation as drafted never explains why a practitioner would care about that: if a curation team commits to one specific in-house synthetic-data generator, why does it matter whether the SAME ranking would hold under a different generator? Without an answer, a skeptical reader could reasonably say 'just measure my own generator and act on it — cross-generator robustness is an academic nicety.' This is exactly the kind of unaddressed gap the stage-2 rubric's partial_output_coverage check exists to catch."}`
- decision: `move_to_refiner`.

### Refiner pass

- `why_it_matters` (extended): "...critically, the robustness conditions are not an academic nicety but a practical necessity: synthetic-data generators are swapped and upgraded routinely as better open-weights and API models become available, so a curation policy derived from one generator's ranking is only actionable if it is a property of the *domain*, not a fingerprint of that one generator's idiosyncratic per-domain writing quality (e.g., a generator that happens to write weaker code than prose would make code look artificially fragile). A ranking that fails to replicate under a generator swap would silently invalidate every curation decision made from it the next time a team updates its synthetic-data tooling — which is precisely the failure mode the generator-robustness and degeneracy-matched checks are built to catch before, not after, a curation policy is deployed on it."
- `changes_made`: added the practical-adoption argument for why generator/degeneracy robustness matters, tied to routine generator turnover in practice.
- `declined_to_fix`: none.

**Confirmed Stage 2.**

---

## Stage 3 — Related Work

All ten works below are treated as **specific (deep) tier** — digest N3/N4 already engaged each one at the approach + limitation level; no additional landscape papers are invented here to pad a `general_related_works` list, and no author names are asserted beyond what the digest itself verified (per the no-fabrication rule, entries without a stated author list are cited as `Anon., <short title> (OpenReview:<id>)`, mirroring how the digest itself presents them).

### Round 1 (critic phase)

**draft_v1** (`specific_related_works`, abbreviated to citation / I-O framing / limitation / `is_potential_baseline`):

| work_id | citation | is_potential_baseline | limitation (→ sub-problem it will motivate) |
|---|---|---|---|
| `rw_mixratio` | Anon., MixRatio (OpenReview:9RdhTvYbX0) | false (analytical, no runnable system) | Models recursive training risk as a function of a single global real/synthetic mixing weight over one homogeneous distribution — no domain decomposition is expressible in the framework at all. |
| `rw_iterstability` | Anon., IterStability (OpenReview:JORAfH2xFd) | false (analytical) | Derives contraction conditions for iterative retraining stability as a function of the same kind of global mixing parameter — same domain-blindness as MixRatio. |
| `rw_crossmodelrecursion` | Anon., CrossModelRecursion (OpenReview:JEU4PBaX85) | false (population-level, different unit of analysis) | Models bias–variance dynamics of many models sharing a synthetic-data channel; documents aggregate tail-event loss, but never manipulates which content domain receives synthetic data. |
| `rw_entropycollapse` | Anon., EntropyCollapse (OpenReview:6xCcjYa97j) | **true** | Measures aggregate distributional entropy decline on a single data distribution (not domain-decomposed) and proposes entropy-maximizing selection as a generic mitigation — offers no domain-selectivity evidence of its own. |
| `rw_spendwisely` | Anon., SpendWisely (OpenReview:aqpHTPC63N) | false (iteration-schedule optimizer, not a comparator) | Optimizes synthetic-sample-count schedules across bootstrapping iterations for one task-homogeneous data pool; offers no guidance on staging a domain-decomposed contamination grid under fixed compute. |
| `rw_doremi` | Anon., DoReMi (OpenReview:lXuByUeHhd) | false (domain-reweighting method, not applicable as a runnable baseline here) | Proves per-domain mixture composition shifts downstream capability, but assumes every domain shard is clean — the domain axis is causally live in its own results, yet contamination is never crossed with it. |
| `rw_regmix` | Anon., RegMix (OpenReview:5BjQOUXq7i) | false (methodology reference, not a runnable competitor) | Establishes that mixture-quality *rankings* (not magnitudes) transfer across model scale for clean domains; never tested under a contamination treatment. |
| `rw_synthweighting` | Anon., SynthWeighting (OpenReview:oI5tZaWkF9) | **true** | Reweights synthetic fine-tuning examples for one task/domain at a time via distribution-mismatch correction; never compares fragility across domains or at pretraining scale. |
| `rw_talr` | Anon., TALR (OpenReview:ru93xpQFi1) | false (different setting: real, not synthetic, data) | Studies how domain-specific SFT on real curated data perturbs general capability via optimization dynamics; because its data is real and no contamination ratio is manipulated, it cannot separate "domain training shifts capability" from "synthetic contamination of a domain damages capability." |
| `rw_shumailov2024` | Shumailov et al., 2024 (Nature) | false (canonical anchor, cross-modal, no runnable baseline) | Establishes recursive-training collapse empirically and theoretically across LMs/VAEs/GMMs on single, non-decomposed distributions — the field's foundational demonstration, but silent on domain structure. |

**critique:**
- summary: Every limitation is specific and problem-tied (no "scalability issues"-style vagueness), but two of the three `is_potential_baseline: true` entries risk creating exactly the outcome-tier framing that `study_type: empirical` forbids at Stage 6.
- comments:
  - `{severity: major, field: "specific_related_works[rw_entropycollapse, rw_synthweighting].is_potential_baseline", anti_pattern: "tier_violation (anticipated)", comment: "Digest N8 already lists EntropyCollapse's entropy-maximizing selection and SynthWeighting's importance reweighting as 'baselines' without any caveat distinguishing them from outcome-tier competitors. Per stages.md, `study_type: empirical` forbids any RQ framed as 'our procedure beats baseline X' — if these two carry forward into Stage 6 as unqualified baselines, the natural next move is exactly that forbidden framing ('our contamination protocol shows more/less damage than these mitigations'), which would misrepresent a measurement study as a beats-baseline paper. The role needs to be pinned down now, before Stage 6 inherits the ambiguity."}`
- decision: `move_to_refiner` (a wording-precision fix — the two works are legitimately useful as optional mitigation-characterization arms, just not as "baselines" in the competitor sense).

### Refiner pass

- `rw_entropycollapse.is_potential_baseline` and `rw_synthweighting.is_potential_baseline` retained as `true`, but each field's accompanying note is sharpened: "Not a baseline in the beat-a-number sense — this is a measurement study and no research question is framed as outperforming either. Each is borrowed only as an optional **mitigation-characterization arm**: re-implementing its selection/reweighting heuristic on the contaminated cells shows how much of the measured domain-specific damage an existing generic mitigation already recovers, which contextualizes the ranking's practical stakes without ever claiming this paper's protocol 'beats' either method."
- `changes_made`: clarified both baseline roles to foreclose an outcome-tier framing before Stage 6.
- `declined_to_fix`: none.
- **Note on `verify_as_hypothesis`:** set `false` on every limitation. None is flagged as a Stage 6 framing-tier RQ — every limitation above restates why the *overall* problem is unaddressed (motivating Stage 4's sub-problems), not a specific claim this paper commits to independently verifying. Per stages.md: *"If nothing was flagged, emit zero framing-tier RQs — don't manufacture one."*

**Confirmed Stage 3.**

---

## Stage 4 — Sub-Problems

### Round 1 (critic phase)

**draft_v1** (4 sub-problems, from digest N5's C1–C4 — the digest's own "Conflation check" already verifies these four are problem-inherent obstacles distinct from the N4 prior-work limitations above, per its explicit N4-vs-N5 test):

- **`sp_causal_attribution`** — *description:* Determine whether measured capability damage in a contaminated cell is attributable to the injected text being machine-generated per se, or to generic textual degeneracies (repetition, reduced lexical entropy) synthetic text happens to carry alongside its syntheticness. *why_it_is_a_problem:* if the paper cannot separate the two, every downstream claim about "syntheticness causing damage" is actually an unlabeled claim about generic low-quality text — a much less interesting, less actionable finding. *technical_challenge:* within a single contamination cell, "is synthetic" and "is degenerate" change together by construction, so isolating either requires a second cell built to hold one fixed while the other varies. *source_limitation_ids:* `["__novel__"]` — no cited work manipulates domain identity as an independent contamination variable at all, let alone separates syntheticness from co-occurring degeneracy within one.
- **`sp_cross_domain_commensurability`** — *description:* Compare capability damage across four domains whose ground-truth structures are fundamentally different (code's executable pass/fail, math's checkable final answer, prose/dialogue's graded or judged scores) without letting the choice of cross-domain metric determine the ranking by construction. *why_it_is_a_problem:* comparing raw benchmark deltas directly across domains would make any "ranking" partly an artifact of which benchmark happens to be more sensitive or more compressed, not a genuine property of domain fragility. *technical_challenge:* the four domains admit no common raw unit, so a valid comparison requires normalizing every domain against its own clean-control baseline — and even that normalization choice is itself a modeling decision that could bias which domain looks most fragile. *source_limitation_ids:* `["__novel__"]` — DoReMi/RegMix optimize domain *weights*, never compare domain *fragility* under any treatment.
- **`sp_dose_response_scale`** — *description:* Characterize how damage scales with contamination ratio within each domain, and whether the resulting ranking is stable as model scale changes, without exhaustively training the full domain × ratio × scale × seed grid. *why_it_is_a_problem:* a ranking measured at one point in ratio/scale space could differ at another; reporting it without checking dose-response shape or scale-stability risks a curation recommendation that is an artifact of the specific small-scale pilot used to produce it. *technical_challenge:* the full grid is combinatorially expensive at pretraining-relevant compute, so an affordable study samples a small corner of the space and must justify why untested corners wouldn't overturn the ranking. *source_limitation_ids:* `["__novel__"]` — SpendWisely optimizes iteration schedules for a task-homogeneous pool, offering no method for staging a domain-decomposed grid under fixed compute.
- **`sp_generator_confound`** — *description:* Rule out the possibility that an observed cross-domain vulnerability ranking merely reflects one specific contamination generator's own domain-dependent writing quality, rather than a property of the domains themselves. *why_it_is_a_problem:* if the ranking is really a fingerprint of the generator used, the paper's central actionable claim would only apply to organizations using that exact generator, defeating the point of a general-purpose curation recommendation. *technical_challenge:* no single-generator study can distinguish "domain is intrinsically fragile" from "this generator happens to write this domain worse" by construction — both produce the identical observed ranking. *source_limitation_ids:* `["__novel__"]` — no cited work varies the generating model as an independent variable.

**critique:**
- summary: Coverage checks out (solving all four would jointly deliver Stage 1's graded objective), but two sub-problems read similarly enough on a first pass that a reader could conflate them.
- comments:
  - `{severity: minor, field: "sp_causal_attribution / sp_generator_confound", anti_pattern: "overlap", comment: "Both are, at a surface level, versions of 'is the damage really about domain, or about something else contaminating the signal?' They are genuinely distinct — one is a within-cell confound (syntheticness vs. degeneracy at fixed domain and ratio), the other is a cross-cell, ranking-level confound (generator identity vs. domain identity) — but the current `technical_challenge` wording doesn't state that distinction explicitly enough for a reader moving quickly through four sub-problems."}`
- decision: `move_to_refiner`.

### Refiner pass

- `sp_causal_attribution.technical_challenge` sharpened to end with: "...this is a **within-cell** confound: even holding domain and ratio fixed, is the measured damage due to the text being synthetic per se, or to incidental degeneracy synthetic text happens to carry?"
- `sp_generator_confound.technical_challenge` sharpened to end with: "...this is a **cross-cell, ranking-level** confound distinct from the within-cell syntheticness/degeneracy confound above: even if syntheticness genuinely causes damage in every cell, the relative ORDERING across domains could still be an artifact of which generator produced the contamination, not of domain identity itself — no single-generator study can tell the two apart."
- `changes_made`: made the within-cell-vs-cross-cell distinction explicit in both `technical_challenge` fields.
- `declined_to_fix`: none.

**Confirmed Stage 4** (4 sub-problems; all sourced `["__novel__"]` with stated decisive-component justifications, consistent with the digest's own N4-vs-N5 distinction between prior-tool limitations and problem-inherent obstacles).

---

## Stage 5 — Method Design

### Round 1 (critic phase)

**draft_v1** (4 methods):

- **`m_degeneracy_isolated_syntheticness_test`** → targets `sp_causal_attribution`. *proposed_approach:* For every contaminated cell, log per-document degeneracy covariates (generator perplexity, type-token ratio) during injection; build a matched control arm in which real (non-synthetic) documents from the same domain are subsampled/filtered to match the synthetic arm's measured repetition and type-token-ratio profile at equal token replacement; compare capability damage in the synthetic arm against this degeneracy-matched real-text arm. *key_insight:* degeneracy and syntheticness are perfectly confounded inside a single cell, but not confounded across two cells built to have matched degeneracy and differing syntheticness — building the second arm turns an unidentifiable within-cell confound into a between-arm comparison. This is a **partial, not total, identification**: the matched arm equates *measured* surface degeneracy (repetition, type-token ratio) between the two arms, so any excess damage in the synthetic arm beyond that match is not explained by those two covariates specifically — but it cannot equate *latent* degeneracies the logged covariates don't capture (e.g., subtle factual or logical drift), so some residual confounding between "syntheticness" and "unmeasured quality defects" remains even after the comparison. *hypotheses:* ["At full contamination, the synthetic arm's capability damage significantly exceeds the degeneracy-matched real-text arm's damage in at least half of the tested domains, including the single most vulnerable domain identified by the cross-domain ranking, one-sided bootstrap p < 0.05 after Holm correction."]
- **`m_dual_normalized_domain_ranking`** → targets `sp_cross_domain_commensurability`. *proposed_approach:* Score every domain's capability change as a delta normalized against that domain's own clean-control baseline, computed independently under the domain-native benchmark metric and a benchmark-independent held-out validation-loss metric; fit a mixed-effects model regressing the normalized delta on ratio interacted with domain, seed as random effect; report a domain-selectivity verdict and a fragility ranking only when both normalizations agree. *key_insight:* a single mixed-effects fit read two ways yields two separately falsifiable claims — the interaction term answers whether damage is domain-selective at all, while a pre-registered strict-versus-tolerant contrast on the fitted slopes answers a stronger, substantive claim about which domains are more fragile and why. *hypotheses:* ["The domain × ratio interaction term in the dual-normalized mixed-effects model is significant at Holm-corrected α = 0.05.", "The pre-registered contrast (mean slope of code and mathematics) − (mean slope of prose and dialogue) is positive with a one-sided bootstrap 95% CI excluding zero, and the same sign holds under both the benchmark-metric and validation-loss normalizations."]
- **`m_staged_dose_response_and_scale_check`** → targets `sp_dose_response_scale`. *proposed_approach:* Run a coarse two-point ratio sweep (0%, 100%) at pilot scale to establish existence and size an effect; run the full five-point ratio grid at base scale to characterize dose-response shape; replicate only the two extreme ratios at a second, larger scale, and compare the resulting per-domain ranking (not magnitude) across scales via Kendall's τ. *key_insight:* the actionable claim only requires the ranking, not the exact magnitudes, to transfer across scale — concentrating scarce large-scale compute on the two most informative ratio extremes is sufficient to test that one claim. *hypotheses:* ["Within each domain, the normalized capability delta is non-decreasing in contamination ratio (Spearman ρ ≥ 0) in at least three of four domains, and the ranking of per-domain slopes computed at the two tested model scales agrees at Kendall's τ ≥ 0.66."]
- **`m_cross_generator_replication`** → targets `sp_generator_confound`. *proposed_approach:* Independently repeat the full single-domain contamination sweep using a second contamination generator from a different model family and quality tier, holding the injection protocol fixed; compute agreement between the two generators' resulting per-domain slope rankings via Kendall's τ. *key_insight:* a ranking produced by exactly one generator is observationally indistinguishable from that generator's own idiosyncratic per-domain writing-quality profile; requiring two structurally different generators to agree is the only test that can rule out a generator-specific artifact. *hypotheses:* ["The per-domain slope ranking obtained under the two independently-sourced contamination generators agrees at Kendall's τ ≥ 0.66 (at most one adjacent transposition among the four domains)."]

**critique:**
- summary: Every method has a real mechanism (no goal-restatement) and every hypothesis names a threshold, but `m_dual_normalized_domain_ranking` carries two claims of very different strength bundled under one method without explaining why that's defensible rather than scope creep.
- comments:
  - `{severity: minor, field: "m_dual_normalized_domain_ranking.hypotheses", anti_pattern: null, comment: "Hypothesis 1 (an interaction exists) is a direct, almost mechanical consequence of building a commensurability-safe normalization — but hypothesis 2 (specifically code+math are MORE fragile than prose+dialogue, not just 'some asymmetry exists') is a much stronger, substantive scientific claim about correctness-strictness that the normalization module does not, by construction, guarantee. The current key_insight blurs this: it should say explicitly that the module makes the FIRST claim checkable but the SECOND claim is a hypothesis being tested with the instrument, not a property the instrument confers."}`
- decision: `move_to_refiner` (a justification-sharpening fix, not a redesign — the two-hypotheses-one-method structure is fine once the distinction is stated).

### Refiner pass

- `m_dual_normalized_domain_ranking.key_insight` extended: "...crucially, this instrument makes ANY cross-domain slope comparison meaningful in the first place (resolving `sp_cross_domain_commensurability` itself), but it does not by construction determine WHICH direction the comparison comes out — the correctness-strictness ordering (code, math more fragile than prose, dialogue) is a substantive domain-theory hypothesis being tested *with* this instrument, not a property the normalization confers. One measurement apparatus, two logically separable claims: that domains differ at all, and specifically how they are ordered."
- `changes_made`: made explicit the distinction between "instrument validity" (claim 1) and "substantive domain-theory claim" (claim 2) so the two-hypothesis bundling doesn't read as unexamined scope creep.
- `declined_to_fix`: none.

**Confirmed Stage 5** — 4 methods, **5 hypotheses total** (1 + 2 + 1 + 1 across the four methods respectively — `m_dual_normalized_domain_ranking` carries two, per the refiner's instrument-vs-substantive-claim justification above), matching `paper.md`'s own five pre-registered hypotheses H1–H5 in substance (independently re-derived from digest N5's challenges upward, not copied from `paper.md`'s Step 6 uncritically — see the cross-stage check below for the correspondence).

---

## Stage 6 — Experiment Design

**Tier accounting (checked against study_type=empirical):**
- **Mechanism-tier: 5 RQs**, one per Stage 5 hypothesis (verbatim `target_hypotheses`).
- **Framing-tier: 0 RQs** — no Stage 3 limitation was flagged `verify_as_hypothesis`; none manufactured.
- **Outcome-tier: 0 RQs** — `study_type = empirical` forbids "our procedure beats baseline X" framing. The mitigation-characterization arms (EntropyCollapse-style, SynthWeighting-style) from Stage 3 are sanity-check comparators only, never competitors to beat.

### Round 1 (critic phase)

**draft_v1:**

`datasets` (training shards):
- The Stack (permissive-license Python/Java subset) — code shard; justification: public, license-clean, large enough for the token budgets in N6's staged plan.
- OpenWebMath — math shard; justification: public math text at the needed scale with a natural link to GSM8K-style exact-match evaluation.
- FineWeb-Edu — prose shard; justification: public, high-quality prose at scale, natural link to LAMBADA/WikiText evaluation.
- OASST1 + UltraChat — dialogue shard; justification: public multi-turn dialogue data at the needed scale, natural link to MT-Bench evaluation.

`baselines` (sanity-check comparators, not outcome-tier competitors):
- Clean control (0% contamination, shared across domains per seed) — necessary control for every contaminated cell.
- Global-uniform contamination arm (same total synthetic-token budget spread proportionally across all four shards) — the "why do this at all" control: if concentrated single-domain injection is statistically indistinguishable from proportionally-spread injection, the domain axis adds nothing.
- Degeneracy-matched real-text arm and second-generator arm — used directly by `m_degeneracy_isolated_syntheticness_test` and `m_cross_generator_replication` above.
- Entropy-maximizing selection and importance-weighted synthetic training (mitigation-characterization arms, per Stage 3's sharpened role for `rw_entropycollapse`/`rw_synthweighting`) — optional, sanity-check only.

`research_questions` (5, all mechanism-tier):

| rq_id | target_sub_problem_id | target_hypotheses (verbatim) |
|---|---|---|
| `rq_domain_selectivity_interaction` | `sp_cross_domain_commensurability` | "The domain × ratio interaction term in the dual-normalized mixed-effects model is significant at Holm-corrected α = 0.05." |
| `rq_strictness_directional_ranking` | `sp_cross_domain_commensurability` | "The pre-registered contrast (mean slope of code and mathematics) − (mean slope of prose and dialogue) is positive with a one-sided bootstrap 95% CI excluding zero, and the same sign holds under both the benchmark-metric and validation-loss normalizations." |
| `rq_dose_response_scale_stability` | `sp_dose_response_scale` | "Within each domain, the normalized capability delta is non-decreasing in contamination ratio (Spearman ρ ≥ 0) in at least three of four domains, and the ranking of per-domain slopes computed at the two tested model scales agrees at Kendall's τ ≥ 0.66." |
| `rq_generator_robustness` | `sp_generator_confound` | "The per-domain slope ranking obtained under the two independently-sourced contamination generators agrees at Kendall's τ ≥ 0.66 (at most one adjacent transposition among the four domains)." |
| `rq_syntheticness_vs_degeneracy` | `sp_causal_attribution` | "At full contamination, the synthetic arm's capability damage significantly exceeds the degeneracy-matched real-text arm's damage in at least half of the tested domains, including the single most vulnerable domain identified by the cross-domain ranking, one-sided bootstrap p < 0.05 after Holm correction." |

(setup/sample-size/statistical-test/expected-outcome/metrics per RQ carried into the paper draft's Experiments section below, reusing `paper.md`'s already-designed E1–E5 parameters as authored design targets, not fabricated results.)

**critique:**
- summary: Tier accounting is clean and every RQ traces to a verbatim hypothesis, but the dialogue-shard dataset entry has an unstated validity problem that `paper.md`'s own Assumptions section (A1) already flags and that this draft's dataset table drops.
- comments:
  - `{severity: major, field: "datasets[OASST1 + UltraChat]", anti_pattern: "weak justification (fails the rubric's 'justification for why this dataset actually stresses the hypothesis' — here, actively undermines it)", comment: "UltraChat is itself LLM-generated. If the 'clean' dialogue baseline shard already contains a non-trivial fraction of synthetic text, every dialogue-domain contamination cell is contaminating an already-contaminated baseline — silently compressing the measurable Δ_dialogue and biasing the ranking toward 'dialogue looks robust' for a spurious reason (a ceiling effect, not genuine style-tolerance). paper.md's own Assumption A1 already identifies this exact risk and pre-registers a mitigation (an audit + a swap to a human-only corpus if the synthetic base rate exceeds 20%), but that caveat did not carry into this stage-6 dataset justification."}`
- decision: `move_to_refiner`.

### Refiner pass

- `datasets[OASST1 + UltraChat]` entry replaced: "OASST1 + UltraChat — dialogue shard, used as the 'clean' baseline **contingent on a pre-registered audit**: before any contamination run, a synthetic-text classifier is passed over the pooled shard to estimate its existing synthetic base rate. If that rate exceeds 20%, UltraChat is dropped in favor of OASST1 plus a human-only forum corpus, as a pre-committed design amendment (not a post-hoc fix), before the dialogue domain enters the ratio sweep at all. This directly guards `rq_strictness_directional_ranking` and `rq_domain_selectivity_interaction` against a ceiling-effect confound that would otherwise make the dialogue domain look artificially tolerant."
- `changes_made`: carried `paper.md`'s Assumption A1 (clean-baseline audit) forward into the dataset justification, closing the gap between the pre-registered assumptions ledger and the experiment design table.
- `declined_to_fix`: none.

**Confirmed Stage 6.**

---

## Cross-stage consistency check (final pass, all six stages)

1. **No method leak** in stages 1/2/4 — checked; `objective`/`why_it_is_a_problem` fields name no technique (the dual-normalization, degeneracy-matching, and generator-replication mechanisms first appear in Stage 5).
2. **ID stability** — no id renamed mid-run; `sp_*` / `m_*` / `rq_*` stable stage-to-stage.
3. **Reference integrity** — all four `sub_problem_id`s source `["__novel__"]` with stated justification (no lim_ id forced where the digest's own N4-vs-N5 test says none applies); every `target_sub_problem_id` in Stage 5 ∈ Stage 4 ✓; every Stage 6 `target_hypotheses` is a verbatim match to a Stage 5 hypothesis ✓.
4. **Output coverage** — Stage 1's three graded outputs (domain × ratio matrix, vulnerability ranking, robustness verdict) are each reachable: the matrix and the interaction test via `sp_cross_domain_commensurability`; the directional ranking via the same sub-problem's second hypothesis; the robustness verdict via `sp_generator_confound` (generator-replication) and `sp_causal_attribution` (degeneracy-robustness) jointly, exactly matching Stage 1's refined, ordered objective (i)-(ii)-(iii) — nothing promised in Stage 1 falls off the chain by Stage 6.
5. **`study_type` consistency** — `empirical` throughout; Stage 6 correctly emits 0 outcome-tier RQs, and the two `is_potential_baseline: true` works from Stage 3 are explicitly pinned as mitigation-characterization arms, not outcome-tier competitors.
6. **Independent re-derivation check** — Stage 5's four methods and five hypotheses were built upward from digest N5's four challenges (C1–C4), not copied from `paper.md`'s own Step 6 (E1–E5). They converge on matching substance (domain-selectivity + directional ranking ≈ H1+H2; dose-response + scale-stability ≈ H3; generator robustness ≈ H4; syntheticness-vs-degeneracy ≈ H5) — a genuine cross-check that the digest's own challenge decomposition and `paper.md`'s independently-designed experiment set agree, rather than one being a restatement of the other.

**What was hardest:** unlike a typical autoclaude run, the seed material contained almost no factual gaps to fill — the recurring tension was **scope discipline around graded claims**, not missing content. The Stage-1 critique (splitting one binary objective into three ordered, separately-falsifiable conditions) and the Stage-6 critique (surfacing that `paper.md`'s own Assumption A1 about UltraChat's synthetic base rate hadn't propagated into the dataset table) were both cases of the loop catching a place where the seed's own internal rigor (the Claim-Evidence Map; the Assumptions ledger) existed but hadn't been fully threaded through this schema's separate fields.

**Total rounds:** 6 stages × 1 critic round + 1 refiner pass = 6 critic rounds, 6 refiner passes. No stage hit the round cap; no cross-stage backup was required.

---

## Post-review revision round (2026-07-05)

> Scope: revision pass over every finding in `stage_review.md` (pre-draft stage review + Phase A re-run + Phase G adversarial review) and `taste_audit.md` (initial + Phase H re-audit). No `design_review.md` exists for this topic. Each finding was checked against the current `paper_draft.md`/`.tex`, `experiment_design.md`, `paper.md`, and `digest.md`; status recorded below. **Outcome: every actionable finding was already applied by the pass that raised it — no deliverable edit was required this round.** This section is the verification record.

**Findings verified as already applied (source → finding → where confirmed):**

1. `stage_review.md` Stage 1 (recommendation, not REVISE) → surface the walking-skeleton feasibility evidence in the assembled draft's Experimental Setup → confirmed applied: `paper_draft.md` "Feasibility check" paragraph (Experimental Setup) and `experiment_design.md` "Sample size and compute budget" walking-skeleton entry.
2. `stage_review.md` Stage 2 (REVISE) → explicit nearest-neighbor sentence naming MixRatio + DoReMi and the delta → confirmed applied: `paper_draft.md` Introduction ¶3 and Related Work ¶1; mirrored in `paper_draft.tex` (lines with `\citet{MixRatio2023}`/`\citet{DoReMi2023}`).
3. `stage_review.md` Stage 3 (REVISE) → partial-identification caveat on `m_degeneracy_isolated_syntheticness_test`'s `key_insight` → confirmed applied: this trace's Stage 5 method entry ("**partial, not total, identification**"), `paper_draft.md` Methodology "Degeneracy-Matched Syntheticness Isolation", and `experiment_design.md` RQ5 Setup.
4. `stage_review.md` Stage 4 (REVISE) → explicit **Falsification condition** line per RQ, translated from `paper.md` FB1–FB5 → confirmed applied: 5/5 in `paper_draft.md`, 5/5 in `paper_draft.tex`, and per-RQ Falsification clauses in `experiment_design.md`; Phase G item 6 independently re-verified no drift from FB1–FB5.
5. `stage_review.md` Phase A item 1 → N1 status FOUND→PARTIAL + N1/N12 3-part absence_comments → confirmed applied in `../digest.md`.
6. `stage_review.md` Phase A item 2 → reference-cache integrity (10 N3/N4-cited works appended as `selected`) → confirmed applied; the logged residual (`digest_path: null`) was separately RESOLVED per `pipeline.md`'s "Reference-cache integrity fix" row (2026-07-05).
7. `stage_review.md` Phase A item 5 → effect floors on H1 (≥0.10), H2 (≥0.05), H3(i) (≥0.05), H5 (≥0.03); H3 aggregation rule (PASS iff (i) ∧ (iii)); Gate/Consequence on A2/A6/A7; new A8 (dialogue-judge validity, κ ≥ 0.7, PG-3) → confirmed applied in `../paper.md`; floors and the H3 aggregation rule are mirrored in `experiment_design.md` (RQ1/RQ2/RQ3/RQ5) and `paper_draft.md`'s RQ expected-outcome text (0.10 / 0.05 / 0.05 / 0.03 — cross-checked identical across all three files).
8. `stage_review.md` Phase A item 6 → Estimand line, Confound-removal block, M7 mechanism analysis, A5 INCONCLUSIVE consequence → confirmed applied in `../paper.md` (M7 later propagated to the deliverables via Phase G, item 12 below).
9. `stage_review.md` Phase A items 3/4/7/8 → PASS verdicts, no action items — nothing to apply.
10. `taste_audit.md` §6 → Stage 2 `summary` field tightened to lead with the asymmetry claim → confirmed applied in this trace's Stage 2 confirmed output; honest 🟢, no further action.
11. `taste_audit.md` Phase H re-audit → 🟢, no condition fires, no action items.
12. `stage_review.md` Phase G [moderate] → M7 absent from the draft → confirmed applied: fifth Methodology subsection ("Mechanism Analysis: A Verifiable-Error Audit") + non-gating "Mechanism check" Experiments subsection in both `paper_draft.md` and `paper_draft.tex`; also carried in `experiment_design.md` ("Mechanism check (non-gating, explanatory — not a sixth RQ)").

**Findings rejected as moot / deferred (not applied, with reason):**

- `stage_review.md` Phase G [minor] (= `pipeline.md` open to-do 1): the 5 additional Related-Work citations (CAUSALM, CanSmallTraining, IterativeDeploymentImpro, EffectivenessTrainingDat, JointSelectionLarge) are absent from `paper.md`'s Claim-Evidence Map Claim 3 sourcing note → **rejected — deferred by design**: the fix targets `paper.md` (the pre-registered authority, not a revision-pass deliverable), and Phase G itself pre-committed to deferring it because any `paper.md` edit re-triggers Phase A under goal.md's resumability discipline; none of the five citations changes any claim's truth-status, and Claim 3 remains correctly sourced by its original four works. Remains logged in `pipeline.md`'s open to-dos.
- `pipeline.md` open to-dos 2 (Phase B/C compute) and 3 (full digests for 5 `adjacent` cache entries) → **rejected — moot for a revision pass**: no compute exists in this environment (to-do 2), and goal.md Phase A item 2 explicitly does not require digests for non-load-bearing `adjacent` entries (to-do 3).

**Cross-deliverable consistency check (this round):** RQ count 5 + 1 non-gating mechanism check in both `paper_draft.md` and `experiment_design.md` ✓; all five `experiment_design.md` target hypotheses byte-identical to this trace's Stage 6 table (grep -F exact-match, 5/5) ✓; effect floors 0.10/0.05/0.05/0.03 and margins (Kendall's τ ≥ 0.66, α = 0.05 Holm over 4 primary metrics, 10,000-resample bootstrap, 3 seeds/cell, 27-run pilot) identical across `paper.md`, `paper_draft.md`, and `experiment_design.md` ✓; falsification conditions faithful to FB1–FB5 in both deliverables ✓; `paper_draft.tex` carries the same 5 Falsification-condition lines and the M7 subsections as `paper_draft.md` ✓. No mismatch found; no file modified; no recompile needed (`paper_draft.pdf` from Phase I remains current).
