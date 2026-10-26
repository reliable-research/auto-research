> Extracted verbatim from `pipeline.md`'s original Stage 1–6 transcript (the "## Seed brief" through "## Cross-stage consistency check" sections). This is the complete round-by-round critic/refiner record for the six-stage `auto-research-discussion` run: every draft, every critique (comments + severities + resolution), every decision, every refiner pass. See `experiment_design.md` for the standalone Stage 6 spec, and `pipeline.md` for the goal.md phase-gate (Phase Log) tracking that continued after this run.

# Auto-Research-Discussion Run — B2.3 (autoclaude-style, repo-driven from digest.md + paper.md)

> Mode: **autoclaude** (self-play, Claude as student+teacher). Source: `../digest.md` (N0–N12) + `../paper.md` (Steps 0–9), both pre-existing reverse-digest artifacts for seed **B2.3**. Round cap: 5/stage (none hit). All six stages converged in 1 critic round + 1 refiner pass each — the seed material was unusually mature (`paper.md` already carries a pre-registered asymmetry, taste self-audit, formal notation, assumptions, and fallback-worded hypotheses), so genuine disagreement surfaced but didn't require re-proposing.
>
> **Full pipeline order (updated):** this file (`auto-research-discussion`, 6 stages) → `taste_audit.md` (`research-taste-auditor`, idea-level check on Stage 2+5) → `stage_review.md` (`pengsida-stage-reviewer`, PASS/REVISE/STOP per stage against the confirmed outputs, plus a Stage 5 Writing check on the first assembled draft) → final `paper_draft.md`/`.tex`/`.pdf`. Two REVISE findings from `stage_review.md` (a missing nearest-neighbor sentence in Related Work, and missing per-RQ falsification conditions in Experiments) are already folded into the `paper_draft.*` files below — read `stage_review.md` for the reasoning behind those two fixes.

## Seed brief

- **One-sentence description:** Measure whether the plan/tool/execution failure-attribution label assigned to a fault-injected LLM-agent failure trace stays the same when the agent's underlying LLM backbone is swapped, and if not, decompose the instability into agent-backbone, judge-backbone, and surface-style sources.
- **Apparent inputs:** a fault-injection task suite built over GAIA and WebArena-style tasks, each cell carrying a machine-readable ground-truth injected layer; several LLM backbones serving as the agent's executing model under one fixed scaffold; a fixed, pre-registered attribution procedure (LLM judge + codebook, validated against a human-coded subset).
- **Apparent outputs:** per-(task, fault, backbone) attribution labels; chance-corrected cross-backbone agreement statistics overall and per layer; the failure-overlap (censoring) rate; a variance decomposition of instability into agent-backbone / judge-backbone / task / interaction components.
- **Closest research areas:** LLM-agent failure attribution (Who&When, AgenTracer, MAST); LLM-judge reliability and bias (PreferenceLeakage, BiasScope, MENLO); backbone-level security/vulnerability comparison (Breaking Agent Backbones).
- **In scope:** measuring whether an existing attribution *procedure* generalizes across backbones via controlled fault injection. **Out of scope:** designing a new attribution algorithm to fix instability; training or fine-tuning judges/agents; live/production deployments; treating organically-arising (non-injected) failures as the primary evidence source (used only as a complementary check).
- **Confidence: high.** As with the calibration exemplar, the "repo" here is itself a prior reverse-digest plus a pre-registered spec (`digest.md` + `paper.md`) that is already internally cross-referenced (N-node ↔ M-component ↔ RQ ids) and already carries its own asymmetry/taste self-audit (`paper.md` Step 0/3). Reconstruction risk is low; the residual risk is *redundancy* with `paper.md`'s own Step 6, which is why stages 5/6 below are framed to surface schema-specific content (falsifiable instrument-validity claims, explicit sub-problem/method/RQ traceability) that `paper.md` gestures at through its Assumptions/fallback wording but never states in this skill's exact structured form.

---

## Stage 1 — Problem Definition

### Round 1 (critic phase)

**draft_v1** (proposer):
- `summary`: Given a fixed suite of (task, fault-layer) cells, each carrying a machine-readable ground-truth record of a single injected failure layer (plan, tool, or execution), and given the ability to run every cell through several LLM backbones acting as the agent's executing model under one identical scaffold, determine whether the failure-attribution label a fixed procedure assigns to the resulting failure trace stays the same across backbones — and, where it does not, whether the instability traces to the backbone that produced the failure, the backbone that judged it, or surface-style differences between them.
- `input`: (1) a set of tasks paired with single-layer fault injectors and a machine-readable ground-truth record per cell; (2) a set of $K$ LLM backbones serving as the agent's executing model, run under one fixed scaffold; (3) a fixed attribution procedure (an LLM judge with a frozen prompt and codebook, plus a human-coded subset for validation) mapping an observed failure trace to a plan/tool/execution label; (4) optionally, a set of judge backbones for separating agent-side from judge-side variance.
- `output`: (1) a per-(task, fault, backbone) attribution label; (2) chance-corrected cross-backbone agreement statistics, overall and per layer; (3) the failure-overlap (censoring) rate among backbones; (4) a variance decomposition of label instability into agent-backbone, judge-backbone, task, and interaction components.
- `constraints`: every cell's ground-truth failure layer must be fixed and known at injection time even though the resulting trace is a function of which backbone executed it; agreement is only computable over cells that actually fail under more than one backbone; the plan/tool/execution boundary is a fixed codebook the study does not get to redefine per case.
- `objective`: a cross-backbone agreement statistic (Fleiss' κ over the fully-failing intersection, or Krippendorff's α when cells are missing due to recovery) is accepted as characterizing "stability" only when reported jointly with the failure-overlap rate; a stability verdict (stable / partially stable / model-specific) is well-defined only relative to pre-registered agreement bands fixed before any data is collected.
- `study_type`: `empirical` — stated explicitly: digest N12 and the seed's own core question ("同一任务失败，换底层 LLM 后归因是否落到同一层") already settle this as a measurement/characterization study, not a proposed fix to attribution.

**critique:**
- summary: The draft is evidence-traceable to the digest and avoids a method leak, but the objective has a real evaluability gap under its own worst-case scenario, and the summary's if-not clause is one dependency short of what the output list actually promises.
- comments:
  - `{severity: major, field: "objective", anti_pattern: "vague_success (evaluability gap)", comment: "The objective states which statistic is authoritative in the normal case but never says what happens if the failure-overlap rate is very low — digest N6's own 'single biggest feasibility risk' note and paper.md's assumption A2 both flag this as a live possibility (strong backbones simply not failing). If the fully-failing intersection is near-empty, is the whole objective unattainable, or does Krippendorff's α on partial cells become the *primary* criterion rather than a footnote? As written, a reader cannot tell whether a low-overlap outcome is a null result or a design failure — that ambiguity has to be resolved in the objective itself, not left to the analysis plan."}`
  - `{severity: minor, field: "summary", anti_pattern: null, comment: "The if-not clause names two sources of instability (backbone that produced it, backbone that judged it) plus 'surface-style differences,' but doesn't say which swap is primary. Output (4) explicitly includes a *task* variance component too — the summary's framing should make clear that 'backbone' primarily means the agent's executing backbone (the seed's own 换底层 LLM), with judge-backbone crossing introduced as a secondary decomposition arm, not a co-equal first framing."}`
- decision: `move_to_refiner` (both are formalize/scope-precision fixes using content already present in the digest and paper.md — no new content needed).

### Refiner pass

- `objective` (refined): "A cross-backbone agreement statistic is accepted as characterizing 'stability' only when reported jointly with the failure-overlap rate $\Omega$ (the fraction of cells failing under every tested backbone). If $\Omega$ meets a pre-registered threshold (≥0.5 in the scale-up stage), Fleiss' κ on the fully-failing intersection is the primary stability statistic; if $\Omega$ falls short of that threshold, Krippendorff's α computed over all failing (possibly partial) cells becomes the primary statistic instead, by pre-commitment rather than post hoc convenience. A stability verdict (stable / partially stable / model-specific) is well-defined only relative to pre-registered agreement bands fixed before any data is collected, under whichever statistic is primary for that run."
- `summary` (refined): "...determine whether the failure-attribution label a fixed procedure assigns to the resulting failure trace stays the same when **the agent's executing backbone** is swapped — and, where it does not, whether the instability is better explained by the agent backbone that produced the failure, the judge backbone that diagnosed it (a secondary, crossed decomposition arm), or surface-style differences between backbones, rather than by the task itself."
- `formal_summary` (added, per stage-1 refiner's formalize-for-free duty): "Task set $T$, fault layers $L=\{\text{plan},\text{tool},\text{exec}\}$, injectors $\iota_\ell$. A cell $c=(t,\ell)\in T\times L$ carries injection record $r_c$ and ground-truth layer $\ell^*(c)=\ell$. Backbone set $B$, $|B|=K$; running $c$ under backbone $b$ (fixed scaffold) yields trace $\tau(c,b)$ and failure flag $F(c,b)\in\{0,1\}$. Judge set $J$; attribution procedure $A_j:\tau\mapsto L$ under a frozen prompt and codebook. Failing intersection $\mathcal{I}=\{c:\forall b\in B, F(c,b)=1\}$; failure-overlap rate $\Omega=|\mathcal{I}|/|T\times L|$. The object of study is the distribution of $\{A_j(\tau(c,b))\}_{b\in B}$ over $c\in\mathcal{I}$ relative to $\ell^*(c)$, and its decomposition across $B$, $J$, and $T$."
- `changes_made`: resolved the low-overlap evaluability gap with a pre-committed metric-promotion rule; scoped the summary's primary swap axis to the agent backbone, with judge-backbone crossing named as secondary; added `formal_summary`.
- `declined_to_fix`: none.

**Confirmed Stage 1** — `study_type: empirical`.

---

## Stage 2 — Motivation

### Round 1 (critic phase)

**draft_v1:**
- `summary`: Failure attribution for LLM-agent pipelines — Who&When's decisive-error judging, AgenTracer's counterfactual/injection-supervised tracer, MAST's failure taxonomy — is now a benchmarked, seemingly mature capability, but every one of these frameworks validates its labels inside one fixed execution stack, so a label that looks like a property of the failure itself (which layer broke) may actually be a property of the particular backbone that produced and judged the trace.
- `why_it_matters`: Practitioners routinely swap the underlying LLM behind an agent scaffold — for cost, latency, or a capability upgrade — while continuing to trust diagnostic tooling that was built and validated on one backbone. If attribution does not survive that swap, every downstream decision resting on a "this was a planning failure" label (which module a team patches, which benchmark result a paper cites as evidence a fix worked) is actually a claim about a (task, backbone) pair being reported as a claim about the task alone. The judge side compounds this: [PreferenceLeakage] and [BiasScope] independently show LLM judges are swayed by which model produced the content they are rating and by structured surface perturbations, so an attribution label produced by an LLM judge reading backbone-flavored agent traces inherits two previously unmeasured dependencies at once — the agent backbone and the judge backbone — exactly the tension the seed's own `[矛盾]` label names.
- `who_cares`: teams that use automated attribution to route bug fixes or justify a backbone-swap decision; benchmark and taxonomy designers (Who&When, MAST) deciding whether their released labels transfer beyond the backbone(s) used to build them; the broader LLM-judge-reliability research community, for whom this is a concrete, high-stakes instance of the general judge-validity question.
- `evidence`: [Who&When, OpenReview:GazlTYxZss]'s own motivation states manual attribution is "prohibitively expensive and inconsistent" — a claim about inconsistency that is never itself checked for backbone-dependence. [AgenTracer, OpenReview:l05DseqvuD]'s counterfactual/injection labels are defined and validated entirely by replaying failures inside one execution stack — the decisive-step definition never crosses backbones. [PreferenceLeakage, OpenReview:grIvSXVJ65] and [BiasScope, OpenReview:QGOw6AU8Lp] show judge-side instability directly, just never on agent-trace failure attribution specifically — itself evidence the question is open (digest N3's six-angle corpus search over 11,683 papers found no work combining fault injection, multi-backbone execution, and fixed attribution).

**critique:**
- summary: Stake-specific, evidence-backed, and tied to stage 1's confirmed outputs — but coverage of one specific stage-1 output is thin.
- comments:
  - `{severity: major, field: "why_it_matters", anti_pattern: "partial_output_coverage", comment: "Stage 1 output (4) is a *variance decomposition*, not just an instability number. why_it_matters motivates why instability matters and why the judge side is independently suspect, but never explains why apportioning the variance specifically has practical value, as opposed to just reporting a single low agreement number and stopping there. A reader could reasonably ask 'why decompose at all — isn't a low κ already the actionable finding?' — that gap is real and unaddressed."}`
- decision: `move_to_refiner`.

### Refiner pass

- `why_it_matters` (extended): "...critically, a single low agreement number is actionable in only one blunt way — 'don't trust attribution across backbones' — but does not tell a team *where* to intervene. Decomposing the instability turns an abandon-ship finding into an actionable one: if judge-backbone variance dominates, standardizing the judge (or using a vendor-disjoint panel) recovers most of the stability at a fraction of the cost of re-validating every agent backbone; if agent-backbone variance dominates instead, no judge fix will help, and per-backbone re-validation really is required. Reporting only the pooled instability number would collapse exactly this distinction and hand teams a diagnosis with no corresponding remedy."
- `changes_made`: added the decomposition-has-actionable-value argument, closing the partial-output-coverage gap.
- `declined_to_fix`: none.

**Confirmed Stage 2.**

---

## Stage 3 — Related Work

All entries below are treated as **specific (deep) tier** — digest N3/N4 already engaged each at the approach + limitation level; no title-only landscape mentions were introduced, and per the no-fabrication rule no additional papers are invented to pad a `general_related_works` list.

### Round 1 (critic phase)

**draft_v1** (`specific_related_works`, abbreviated to citation / I-O framing / limitation / `is_potential_baseline`):

| work_id | citation | is_potential_baseline | limitation (→ sub-problem it will motivate) |
|---|---|---|---|
| `rw_whowhen` | Anon., Who&When (OpenReview:GazlTYxZss) | **true** | Formalizes decisive-error attribution and evaluates several LLM-judge strategies, but every failure log is attributed inside one fixed system configuration — it never re-runs the same task/fault under multiple agent backbones, so it cannot say whether its labels are properties of the failure or of the backbone that produced the trace. |
| `rw_agentracer` | Anon., AgenTracer (OpenReview:l05DseqvuD) | **true** | Its fault-injection labels are correct by construction only within the execution stack that was replayed; the counterfactual definition (earliest step whose correction flips the outcome) is evaluated under one backbone's downstream behavior, so cross-backbone label stability is neither measured nor claimed. |
| `rw_breakingbackbones` | Anon., Breaking Agent Backbones (OpenReview:kga18ld70t) | false (attack-susceptibility score, not a failure-layer label) | Establishes backbone-level comparison as a first-class evaluation axis, but only for attack-susceptibility scores; its snapshot abstraction deliberately removes the multi-step downstream propagation that makes layer attribution ambiguous, so it never tests whether *qualitative diagnoses* (which layer failed) transfer across backbones. |
| `rw_preferenceleakage` | Anon., PreferenceLeakage (OpenReview:grIvSXVJ65) | false (motivates a design control, not a runnable baseline) | Shows LLM judges systematically favor outputs from a related generator, but only on pairwise preference tasks with short responses — it never measures judge disagreement on long agent traces, nor separates judge-side from agent-side variance in a trace-attribution setting. |
| `rw_biasscope` | Anon., BiasScope (OpenReview:QGOw6AU8Lp) | false (motivates a design control, not a runnable baseline) | Shows structured surface perturbations flip judge decisions, on the same short pairwise-response setting as PreferenceLeakage — the same generalizability gap to long agent traces applies. |
| `rw_menlo` | Anon., MENLO (OpenReview:QOWYX3Q2XS) | false | Documents evaluator non-invariance along the *language* axis; the backbone axis for trace-level failure attribution is untouched, and its evaluators score response quality, not failure-layer labels. |
| `rw_mast` | Cemri et al., MAST (arXiv:2503.13657) | **true** | Induces its failure taxonomy from traces of specific framework+backbone configurations and validates it via inter-annotator agreement among human/LLM annotators on the *same* traces — it never checks whether the same task, re-run under a different backbone, would be assigned the same failure category; taxonomy reliability is established across annotators, not across backbones. |

**critique:**
- summary: Grounding is solid, every limitation is specific and traces to a real stated scope — but one baseline label needs the same scrutiny B5.5's exemplar run applied to SOTOPIA.
- comments:
  - `{severity: major, field: "specific_related_works[rw_mast].is_potential_baseline", anti_pattern: "io_approach_mismatch", comment: "MAST's I/O framing is taxonomy induction from human/LLM-annotated *organic* failures, validated by inter-annotator agreement — genuinely different from this paper's fault-injection framing with a machine-readable ground-truth layer. Per the stage-3 rubric, a mismatched-I/O work is 'not a baseline — at best a method-side reference.' Marking it a straightforward baseline risks implying MAST's own reported inter-annotator numbers are being compared against, which they are not."}`
- decision: `move_to_refiner` (a wording-precision fix, not structural — MAST's category schema is still legitimately reusable as a labeling instrument).

### Refiner pass

- `rw_mast.is_potential_baseline` retained as `true`, but the field's accompanying note is sharpened: "Not a baseline in the beat-a-number sense — MAST's own reported inter-annotator agreement is not compared against. Its **plan/tool/execution-adjacent category schema** is borrowed as an instrument for this paper's codebook, independent of its own cross-annotator (not cross-backbone) validation claim."
- `changes_made`: clarified MAST's baseline role to avoid an implied I/O-mismatched comparison.
- `declined_to_fix`: none.
- **Note on `verify_as_hypothesis`:** set `false` on every limitation. None is flagged as a stage-6 framing-tier RQ — digest N8's three inferred RQs (RQ_INF_1–3) all restate mechanism-tier questions already covered end-to-end by Stage 5/6 below, not a distinct related-work-limitation check. Per stages.md: *"If nothing was flagged, emit zero framing-tier RQs — don't manufacture one."*

**Confirmed Stage 3.**

---

## Stage 4 — Sub-Problems

### Round 1 (critic phase)

**draft_v1** (6 sub-problems, from digest N5's C1–C5 plus one gap the top-down decomposition itself surfaces):

- **`sp_censoring_confound`** — *description:* Compute a cross-backbone agreement statistic whose value is not silently determined by which backbones happen to recover from an injected fault. *why_it_is_a_problem:* stronger backbones may simply not fail on a given injected fault, so the pool of "failures available to compare" itself depends on which backbones are in the comparison — an unreported censoring structure would make any agreement number vacuous. *technical_challenge:* the set of failing cells shrinks as stronger backbones recover, and this missingness is systematic (a function of backbone capability) rather than random, so simply gathering more (task, fault) cells does not fix the problem the way it would for ordinary sampling noise. *source_limitation_ids:* `["__novel__"]` — no cited work's stated scope addresses censoring; it is inherent to the cross-backbone design itself.
- **`sp_agent_judge_confound`** — *description:* Attribute an observed instability in attribution labels to the backbone that produced the failure versus the backbone that judged it, rather than reporting one conflated instability number. *why_it_is_a_problem:* without separating them, "attribution is model-specific" is ambiguous between "agents behave differently" and "judges rate differently," and these imply entirely different remedies. *technical_challenge:* whenever one fixed rater reads outputs from many different producers, any observed instability is compatible with two incompatible explanations — the producers behaved differently, or the rater is inconsistent across producers — and no amount of additional producer-side data resolves this unless the rater identity itself is also varied. *source_limitation_ids:* `["lim_preferenceleakage_biasscope"]`.
- **`sp_manifestation_divergence`** — *description:* Determine whether the same injected fault produces observably different failure signatures across backbones even before any attribution procedure is applied, and whether that divergence still maps back to the correct ground-truth layer. *why_it_is_a_problem:* if manifestation itself diverges (a tool-layer fault cascading into plan-layer symptoms in one model but staying execution-local in another), "same cause" does not guarantee "same evidence," and low agreement could reflect real behavioral divergence rather than measurement error. *technical_challenge:* an observed disagreement in the final label is compatible with two different situations — backbones producing genuinely different evidence that a correct procedure faithfully reports, or backbones producing the same evidence that gets mislabeled inconsistently — and agreement statistics alone, without reference to the injected ground truth, cannot tell these apart. *source_limitation_ids:* `["lim_whowhen_agentracer"]`.
- **`sp_taxonomy_ambiguity`** — *description:* Define a codebook boundary for plan/tool/execution that yields a determinate label even for failures that genuinely span more than one layer. *why_it_is_a_problem:* without a forced, pre-registered tie-break rule, apparent cross-backbone disagreement could reflect shifting codebook interpretation rather than backbone-driven instability, contaminating every downstream agreement statistic. *technical_challenge:* the category boundary is stipulated, not discovered from data, and different tie-break conventions can produce different apparent disagreement rates even when nothing about backbone behavior has changed, so the residual ambiguity has to be made measurable rather than assumed away by silently picking one convention. *source_limitation_ids:* `["lim_mast"]`.
- **`sp_style_confound`** — *description:* Determine how much of any observed cross-backbone disagreement is driven by surface formatting/verbosity differences between model families rather than by where the failure actually occurred. *why_it_is_a_problem:* LLM judges are a documented target of surface-level manipulation, so a judge could be latching onto backbone-characteristic phrasing rather than genuine failure location, making an agreement statistic partly a measure of stylistic similarity between backbones instead of diagnostic stability. *technical_challenge:* every trace produced by a given backbone carries that backbone's characteristic phrasing and formatting inseparably from its content, so there is no naturally occurring variation that would let a statistical control alone separate "the judge responds to backbone-identifying surface form" from "the judge responds to what actually happened." *source_limitation_ids:* `["lim_preferenceleakage_biasscope"]`.
- **`sp_family_capability_structure`** — *description:* Determine whether any residual instability, after agent/judge/style sources are accounted for, is unstructured noise across backbones or a systematic function of vendor family and capability tier. *why_it_is_a_problem:* these two possibilities carry opposite practical consequences — structured instability means re-validation costs can be amortized within a family or tier; unstructured instability means every backbone needs independent re-validation regardless of lineage — and a pooled instability number cannot distinguish between them. *technical_challenge:* family and capability tier are themselves correlated (newer, larger models often share both a vendor lineage and a capability level), so isolating which factor (if either) structures the instability requires a design that crosses the two rather than one that merely samples across backbones. *source_limitation_ids:* `["__novel__"]` — no cited work's stated scope addresses whether backbone-level instability is family- or capability-structured.

**critique:**
- summary: Coverage checks out — solving all six would jointly deliver stage 1's four outputs — but two sub-problems risk reading as the same distinction restated.
- comments:
  - `{severity: minor, field: "sp_manifestation_divergence / sp_agent_judge_confound", anti_pattern: "overlap", comment: "Both are framed around 'disentangling two possible explanations for an observed disagreement,' which can read as the same sub-problem twice. They are genuinely distinct — one is about *ground-truth accuracy* (does the label still match the injected layer), the other about *apportioning variance by rater identity* (agent vs. judge) — but the current phrasing doesn't make that distinction explicit enough to a reader skimming both."}`
- decision: `move_to_refiner`.

### Refiner pass

- `sp_manifestation_divergence.technical_challenge` sharpened to end with: "...this is a **ground-truth-accuracy** problem — whether divergent manifestations still map back to the correct injected layer — distinct from `sp_agent_judge_confound`'s **variance-apportionment** question of which rater or producer drives any observed instability in the first place."
- `changes_made`: made the accuracy-vs-apportionment distinction explicit in `sp_manifestation_divergence`'s technical_challenge.
- `declined_to_fix`: none.

**Confirmed Stage 4** (6 sub-problems; 2 sourced from a shared related-work limitation row, 1 sourced from MAST's limitation, 1 sourced from the Who&When/AgenTracer limitation row, 2 `__novel__` with stated decisive-component justifications).

---

## Stage 5 — Method Design

### Round 1 (critic phase)

**draft_v1** (6 methods):

- **`m_censoring_protocol`** → targets `sp_censoring_confound`. *proposed_approach:* Compute Fleiss' κ over the failing intersection $\mathcal{I}$ as the primary stability statistic when the failure-overlap rate $\Omega \geq 0.5$; otherwise promote Krippendorff's α (computed over all failing, possibly partial, cells) to primary status by pre-commitment. Report $\Omega$ and per-backbone recovery rate beside every agreement number. *key_insight:* censoring cannot be eliminated by design (recovery is a real backbone behavior, not noise), so the fix is a metric strategy that degrades gracefully as overlap shrinks, plus a pre-committed decision rule for which statistic is authoritative — not a hope that overlap stays high. *hypotheses:* ["Fleiss' κ across ≥6 backbones on the failing intersection has a 95% task-cluster-bootstrap CI entirely below 0.8 (attribution is not fully stable), and κ_exec − κ_plan ≥ 0.10 with Holm-corrected p < 0.05 (execution-layer faults are attributed more consistently than plan-layer faults)."]
- **`m_factorial_decomposition`** → targets `sp_agent_judge_confound`. *proposed_approach:* Cross $J=3$ vendor-disjoint judge backbones with $K=6$–8 agent backbones over the identical trace set; fit a cross-classified mixed-effects model (label match ~ (1|task) + (1|agent_backbone) + (1|judge_backbone) + interactions); read off variance shares with bootstrap CIs and likelihood-ratio tests; anchor judge validity with a 200-trace human-codebook subset (κ ≥ 0.7 gate). *key_insight:* because one fixed judge reading many agents' traces structurally confounds "which model produced the failure" with "which model is rating it," only a design that varies the judge independently of the agent — while controlling judge–agent relatedness, per PreferenceLeakage's finding — can attribute instability to a specific source rather than an ambiguous aggregate. *hypotheses:* ["Judge-backbone variance share exceeds 0.20 of total random-effect variance, with likelihood-ratio-test p < 0.05."]
- **`m_manifestation_accuracy_check`** → targets `sp_manifestation_divergence`. *proposed_approach:* For every cell in the failing intersection, cross-tabulate the joint outcome {all backbones agree and match ground truth; all backbones agree but disagree with ground truth; backbones disagree} against the injected layer, per backbone and per layer. *key_insight:* agreement alone cannot distinguish "backbones manifest and diagnose the fault identically and correctly" from "backbones manifest the fault differently but converge on the same wrong label" — only a joint agreement-vs-ground-truth tabulation exposes the agree-wrong cell, the signature attribution procedures otherwise paper over rather than resolve. *hypotheses:* ["The agree-wrong mass (all backbones agree with each other but not with the injected ground-truth layer) is at least 5% of the failing intersection, with a 95% CI lower bound above 2%."]
- **`m_style_normalization`** → targets `sp_style_confound`. *proposed_approach:* Additionally judge a style-normalized/paraphrased version of every trace (stripped model-identifying tokens, canonicalized tool-call JSON, neutral-rewriter-paraphrased reasoning text, using a rewriter model distinct from every agent and judge backbone in the study); compute the style-share as the fractional drop in mean pairwise cross-backbone disagreement between raw and normalized arms. *key_insight:* style and backbone identity are perfectly confounded in a raw trace, so isolating the style contribution requires an experimental manipulation that holds content fixed while destroying backbone-identifying surface form — a post hoc statistical control cannot separate them because there is no naturally occurring variation to condition on. *hypotheses:* ["Style-share (the fractional drop in disagreement between raw and style-normalized traces) is at least 10%, with a 95% CI lower bound above 0."]
- **`m_codebook_tiebreak_gate`** → targets `sp_taxonomy_ambiguity`. *proposed_approach:* Fix one pre-registered codebook with an explicit earliest-causally-decisive-layer tie-break; validate it with two human annotators on a 200-trace subset requiring Cohen's κ ≥ 0.7 before the codebook is used for any LLM-judge labeling; report a sensitivity re-score of the full Stage-2 grid under an alternative (latest-decisive-layer) tie-break rule alongside the primary numbers. *key_insight:* a fixed tie-break rule cannot resolve genuinely layer-spanning failures, but it can convert an otherwise-invisible source of disagreement (different judges resolving ambiguity differently) into a measured, reportable sensitivity, pinning the label definition so residual disagreement is attributable to backbone effects rather than shifting category boundaries. *hypotheses:* ["Re-scoring the Stage-2 grid under the alternative tie-break rule changes the primary stability-band verdict (stable / partially stable / model-specific) in no more than one of the tested (backbone × domain) cells, showing residual disagreement concentrates in backbone effects rather than tie-break sensitivity."]
- **`m_family_capability_test`** → targets `sp_family_capability_structure`. *proposed_approach:* Cross model family with capability tier in the backbone grid (two sizes per family where available); compare mean within-family pairwise agreement against cross-family pairwise agreement via a permutation test respecting task clustering; correlate each backbone's fault-recovery rate with its clean-run capability (Spearman ρ). *key_insight:* if instability is structured by family or tier, re-validation costs can be amortized (validate one representative per family/tier); if unstructured, every backbone requires independent re-validation regardless of lineage — a materially different practical conclusion that a pooled instability number cannot distinguish. *hypotheses:* ["Mean within-family pairwise agreement exceeds cross-family pairwise agreement by at least 0.10 absolute, Holm-corrected p < 0.05.", "Backbone fault-recovery rate correlates with clean-run capability at Spearman ρ ≥ 0.5, p < 0.05 (censoring is capability-skewed)."]

**critique:**
- summary: Every method names a real mechanism (no goal-restatement), every hypothesis states a threshold that could fail — but two methods each carry more than one headline claim and need a one-line justification for why that is one mechanism, not two.
- comments:
  - `{severity: minor, field: "m_censoring_protocol.hypotheses / m_family_capability_test.hypotheses", anti_pattern: null, comment: "m_censoring_protocol bundles the stability-band claim with a layer-ordering claim (κ_exec vs κ_plan); m_family_capability_test bundles a family-agreement claim with a capability-recovery claim. Both pairs are the paper's central claims about structure — worth stating explicitly why one instrument produces each pair, so neither reads as two methods quietly merged into one entry."}`
- decision: `move_to_refiner`.

### Refiner pass

- `m_censoring_protocol.key_insight` extended: "...the same Stage-2 grid and the same primary agreement statistic yield two separately falsifiable readouts without a second instrument: the overall stability band (is κ/α high enough to call attribution stable) and the per-layer ordering within that same fitted structure (is execution-layer agreement systematically higher than plan-layer agreement) — one measurement pass, two estimands, not two mechanisms."
- `m_family_capability_test.key_insight` extended: "...crossing family with capability tier in one backbone grid yields both readouts from the same design: the within- vs. cross-family agreement contrast and the recovery-rate-vs-capability correlation are two different slices of the identical grid, not two separate studies."
- `changes_made`: justified both two-hypotheses-one-method structures explicitly.
- `declined_to_fix`: none.

**Confirmed Stage 5** — 6 methods, **8 hypotheses total** (2 + 1 + 1 + 1 + 1 + 2 across the six methods respectively), mixing instrument-validity claims (censoring metric choice, tie-break sensitivity) with the study's headline empirical predictions (stability band, judge-variance share, agree-wrong mass, style-share, family/capability structure) — a deliberate design choice for an `empirical` study_type, carried into the tier accounting below.

---

## Stage 6 — Experiment Design

**Tier accounting (checked against study_type=empirical):**
- **Mechanism-tier: 8 RQs**, one per Stage 5 hypothesis (verbatim `target_hypotheses`).
- **Framing-tier: 0 RQs** — no Stage 3 limitation was flagged `verify_as_hypothesis`; none manufactured.
- **Outcome-tier: 0 RQs** — `study_type = empirical` forbids "our procedure beats baseline X" framing. All baselines below are sanity-check comparators or reference labelers only.

### Round 1 (critic phase)

**draft_v1:**

`datasets`:
- GAIA (levels 1–2) — *justification:* tool-use/assistant tasks with deterministic, programmatic success checkers; pilot-stage domain because a checkable single-step-tool task gives the fault-injection ground truth a clean, unambiguous referent.
- WebArena-style tasks — *justification:* reproducible web-agent tasks with richer multi-step tool interaction; scale-up domain that stress-tests whether findings generalize beyond short, deterministic GAIA-style tasks to longer-horizon tool chains.
- (draft initially listed Who&When with justification only "organic-failure complement" — flagged below.)

`baselines` (sanity-check comparators and reference labelers, not outcome-tier competitors):
- Who&When all-at-once and step-by-step LLM-judge protocols (`rw_whowhen`) — the two attribution-procedure options that bracket context-granularity effects; used as the primary attribution procedure's design space, not as a beat-a-number target.
- AgenTracer-style counterfactual-replay labeling (`rw_agentracer`) — a reference labeler on a budget-permitting subset, checking the fixed judge's labels against an independent causal-replay definition of the decisive step.
- Chance-level agreement (label-marginal-preserving permutation) — the necessary statistical floor beneath which no claim of "agreement" is meaningful.
- Majority-vote-across-backbones pseudo-consensus — a sanity baseline, promotable to a load-bearing contribution only if the agree-wrong mass (RQ_agree_wrong_mass) turns out to be negligible.
- Same-backbone test–retest (identical backbone re-run at T=0 plus 3 seeds at T=0.7) — the "why do this at all" control distinguishing cross-backbone disagreement from ordinary LLM/judge sampling noise.

`research_questions` (8, all mechanism-tier):

| rq_id | target_sub_problem_id | target_hypotheses (verbatim) |
|---|---|---|
| `rq_stability_band` | `sp_censoring_confound` | "Fleiss' κ across ≥6 backbones on the failing intersection has a 95% task-cluster-bootstrap CI entirely below 0.8 (attribution is not fully stable)..." |
| `rq_layer_ordering` | `sp_censoring_confound` | "...and κ_exec − κ_plan ≥ 0.10 with Holm-corrected p < 0.05 (execution-layer faults are attributed more consistently than plan-layer faults)." |
| `rq_judge_variance_share` | `sp_agent_judge_confound` | "Judge-backbone variance share exceeds 0.20 of total random-effect variance, with likelihood-ratio-test p < 0.05." |
| `rq_agree_wrong_mass` | `sp_manifestation_divergence` | "The agree-wrong mass (all backbones agree with each other but not with the injected ground-truth layer) is at least 5% of the failing intersection, with a 95% CI lower bound above 2%." |
| `rq_style_share` | `sp_style_confound` | "Style-share (the fractional drop in disagreement between raw and style-normalized traces) is at least 10%, with a 95% CI lower bound above 0." |
| `rq_tiebreak_sensitivity` | `sp_taxonomy_ambiguity` | "Re-scoring the Stage-2 grid under the alternative tie-break rule changes the primary stability-band verdict in no more than one of the tested (backbone × domain) cells..." |
| `rq_family_structure` | `sp_family_capability_structure` | "Mean within-family pairwise agreement exceeds cross-family pairwise agreement by at least 0.10 absolute, Holm-corrected p < 0.05." |
| `rq_capability_censoring` | `sp_family_capability_structure` | "Backbone fault-recovery rate correlates with clean-run capability at Spearman ρ ≥ 0.5, p < 0.05 (censoring is capability-skewed)." |

(setup/sample-size/statistical-test/expected-outcome/metrics per RQ carried into the paper draft's Experiments section below, reusing `paper.md`'s already-designed E1–E4 numbers and fallback wording as authored design targets, not fabricated results.)

**critique:**
- summary: Tier accounting is clean and every RQ traces to a verbatim hypothesis, but one dataset justification is a provenance note instead of a methodological reason.
- comments:
  - `{severity: major, field: "datasets[Who&When]", anti_pattern: "weak justification (fails the rubric's 'justification for why this dataset actually stresses the hypothesis')", comment: "'organic-failure complement' does not say which RQ needs it or why. Digest N8 lists Who&When's naturally-failed logs as a dataset without tying it to a specific research question — the same gap B5.5's exemplar run caught for its GLEE entry."}`
- decision: `move_to_refiner`.

### Refiner pass

- `datasets` entry replaced: "Who&When (naturally-failed multi-agent logs) — *justification:* tests whether `rq_stability_band`'s finding, established on synthetic single-layer injected faults, replicates on organically-arising, human-annotated failures where the ground-truth layer comes from expert agreement rather than injection-guaranteed construction; without it, `rq_stability_band`'s conclusion would be scoped only to synthetic-fault artifacts rather than to failure attribution generally."
- `changes_made`: gave Who&When's inclusion an RQ-linked reason instead of a provenance note.
- `declined_to_fix`: none.

**Confirmed Stage 6.**

---

## Cross-stage consistency check (final pass, all six stages)

1. **No method leak** in stages 1/2/4 — checked; `objective`/`why_it_is_a_problem`/`technical_challenge` fields name no proposed mechanism (statistical instrument names like Fleiss' κ appear only in Stage 1's evaluability criterion, analogous to B5.5's Stage-1 objective naming the Nash bargaining solution — a measurement convention, not this paper's contribution).
2. **ID stability** — no id renamed mid-run; `sp_*` / `m_*` / `rq_*` stable stage-to-stage.
3. **Reference integrity** — `sp_agent_judge_confound.source_limitation_ids` and `sp_style_confound.source_limitation_ids` both = `["lim_preferenceleakage_biasscope"]` ∈ Stage 3 ✓; `sp_manifestation_divergence.source_limitation_ids = ["lim_whowhen_agentracer"]` ∈ Stage 3 ✓; `sp_taxonomy_ambiguity.source_limitation_ids = ["lim_mast"]` ∈ Stage 3 ✓; `sp_censoring_confound` and `sp_family_capability_structure` both `["__novel__"]` ✓; every `target_sub_problem_id` in Stage 5 ∈ Stage 4 ✓; every Stage 6 `target_hypotheses` is a verbatim match to a Stage 5 hypothesis ✓.
4. **Output coverage** — Stage 1's four outputs (label, agreement statistics, censoring rate, variance decomposition) are each reachable: label + agreement via `sp_censoring_confound` + `sp_manifestation_divergence`, censoring rate via `sp_censoring_confound`, variance decomposition via `sp_agent_judge_confound` + `sp_style_confound` + `sp_family_capability_structure` — nothing promised in Stage 1 falls off the chain by Stage 6.
5. **`study_type` consistency** — `empirical` throughout; Stage 6 correctly emits 0 outcome-tier RQs.
6. **Hypothesis-vs-RQ recount** — Stage 5 confirmed 8 hypotheses across 6 methods (2+1+1+1+1+2); Stage 6 confirmed exactly 8 mechanism-tier RQs, one per hypothesis, 0 framing-tier, 0 outcome-tier. 8 = 8; no hypothesis is uncovered, no RQ is unattached.

**What was hardest:** unlike a typical raw-idea run, disagreement was not about whether the seed's core claim holds up (`paper.md`'s Step 0 asymmetry and Step 3 taste self-audit had already stress-tested that) but about **schema discipline under an unusually well-specified seed** — repeatedly checking whether a stage-4/5 sub-problem or hypothesis was quietly restating `paper.md`'s own already-finished Step 5/6 content rather than adding something this skill's structure specifically demands (e.g., the explicit accuracy-vs-apportionment distinction between `sp_manifestation_divergence` and `sp_agent_judge_confound`, and the one-instrument-two-estimands justifications in Stage 5, neither of which `paper.md` states in exactly this form even though its Assumptions/fallback wording gestures at both).

**Total rounds:** 6 stages × 1 critic round + 1 refiner pass = 6 critic rounds, 6 refiner passes. No stage hit the round cap; no cross-stage backup was required.

---

## Post-review revision round (2026-07-05)

> Scope: fold every still-OPEN finding from `stage_review.md`, `taste_audit.md`, and `design_review.md` into the three deliverables. A prior attempt at this pass was interrupted mid-run: it had already (a) split this trace and `experiment_design.md` out of `pipeline.md`, and (b) written two edits into `experiment_design.md` — the header note declaring the RQ6→SC1 demotion/renumbering and the F9 primary-protocol bullet — but had not yet renumbered the `experiment_design.md` body, touched `paper_draft.*`, or logged anything here or in `pipeline.md`. This round **completed** that partial work (same demotion decision carried through, no duplication) rather than restarting it.

### Status audit of all review findings

Already applied before this round (verified in current files, not re-applied): stage_review Stage-2 fix (nearest-neighbor sentence in Related Work), Stage-4 fix (per-RQ falsification conditions), Phase-A items 1/5/6 (digest absence_comments; aggregation rule; Estimand/R2/Power sections in `paper.md`), Phase-A item 2 + design_review F4's digest/PDF residual (resolved by the resume-session re-harvest), the freshness sweep (Claim-1 caveat resolved), Phase F bibliography wiring, Phase G aggregation/thin-cell prose fix, design_review F1/F2/F3/F5a/F5b/F5c and the F4 title corrections (all marked in `paper.md`/`reference_candidates.jsonl` on 2026-07-04). `taste_audit.md` carries no action items (🟢 twice, no regression).

### OPEN findings applied this round

1. **stage_review.md Phase G finding 2 / pipeline.md to-do — RQ6 has no H-id in `paper.md`'s Claim–Evidence Map.** Resolution: the interrupted agent's already-committed choice (the log's pre-approved second option) — **demote RQ6 to instrument-validation sensitivity check SC1**; former RQ7/RQ8 renumbered RQ6/RQ7. No H5 was fabricated in `paper.md` (no pre-registration-level construction under drafting-time incentives; `paper.md` untouched). Applied consistently in `experiment_design.md` (body now matches its header: SC1 section moved after RQ7 with a status note replacing the old "exception flag"; all cross-references renumbered) and `paper_draft.md`/`.tex` (RQ list = 7 + SC1 note; RQ6-tiebreak subsection renamed/relocated as SC1 with a demotion note; RQ7→RQ6, RQ8→RQ7; aggregation paragraph and checklist updated).
2. **design_review.md F6 — task-pool arithmetic + shrink axis.** Added "Task-pool arithmetic and pre-declared shrink axis" section to `experiment_design.md` using only the review's own numbers (GAIA L1–2 ≈140 tasks; WebArena slice sized ≥160; pessimistic 40% weak-backbone clean-run bound ⇒ ≈120-task planning bound; shrink axis = drop weakest tier first, per situation 10). The empirical residual (measured clean-run rates) stays with the skeleton, as the review itself scoped.
3. **design_review.md F7 — pipeline-level placebos.** Added judge test–retest arm and no-op injection arm to `experiment_design.md` (B0 bullet) and mirrored into `paper_draft.md`/`.tex` Baselines.
4. **design_review.md F8 — causal-divergence rival interpretation.** Added a "Pre-committed interpretation" paragraph to the Manifestation-Accuracy Check section of `paper_draft.md`/`.tex`: the re-scoping conclusion survives under either reading; only the "judges are unreliable" gloss is withdrawn in the causal-divergence case.
5. **design_review.md F9 (part 1) — primary judge protocol unnamed.** Interrupted agent had already frozen **all-at-once** as primary in `experiment_design.md`; this round mirrored the freeze into `paper_draft.md`/`.tex` Baselines.
6. **design_review.md F9 (part 2) / reviewer question 3 — partial-band decision unmapped.** Added a "Partial-band decision rule" to RQ1 in `experiment_design.md` and `paper_draft.md`/`.tex`, grounded in `paper.md` F-1's existing straddle clause: per-layer decomposition becomes primary, CO4's keep/re-validate decision is made per layer.
7. **design_review.md reviewer question 1 — scaffold generality.** Applied as the review's own alternative (b): explicit narrow-envelope concession (situation 14(b)) — scaffold-scope note in `experiment_design.md` and a fourth limitation in `paper_draft.md`/`.tex` Conclusion. No second-scaffold arm invented.
8. **design_review.md reviewer question 5 — 200-trace validation/evaluation disjointness.** Sampling rule pre-registered in `experiment_design.md` RQ3 (stratified over agent-backbone × layer, drawn from pilot failing traces, frozen pre-Stage-2, excluded from headline estimates) and mirrored into the judge-factorial Method paragraph of `paper_draft.md`/`.tex`.
9. **design_review.md F10 — lethality-iteration envelope shift.** Named as the third limitation in `paper_draft.md`/`.tex` Conclusion (payloads frozen before Stage 2 ⇒ pre-registered shift; Who&When complement only partial mitigation).
10. **design_review.md F4 residual — N3↔cache key unification.** Added explicit `n3_key` alias fields to the 7 backfilled `selected` records in `reference_candidates.jsonl` (file re-validated as well-formed JSONL, 158 lines), making the "every N3 key is a selected cache record" gate mechanically checkable.

### Rejected as moot (not applied)

- **design_review.md staleness note (draft lacks Estimand/R2/Aggregation/Power sections):** superseded — the resume session's Phase G already carried the Aggregation/INCONCLUSIVE machinery into the draft, and the note itself was explicitly "stated once, not re-penalized," with `paper.md` the spec under review.
- **Formalizing RQ6 as H5 in `paper.md`:** rejected in favor of the demotion option the same log pre-approved (see item 1) — adding a seven-slot H5 would be new pre-registration content invented at revision time, exactly what goal.md §6 warns against.
- **design_review.md F4 "fetch PDFs + digest the 7 works / run named-angle re-harvest":** moot — completed by the 2026-07-04 resume session (item-2 re-harvest RESOLVED; freshness sweep found no method-twin) before this round.

### Cross-deliverable consistency after this round

- RQ count: `paper_draft.md` = `paper_draft.tex` = `experiment_design.md` = **7 headline RQs + SC1** (was inconsistent mid-interruption: header said 7+SC1, bodies said 8).
- Target hypotheses in `experiment_design.md` remain byte-identical to `paper.md` Step 6 (H1, H1b, H3a, H2, H3b, H4a, H4b) and, for SC1, verbatim to `pipeline.md`'s Stage-5 transcript.
- Effect floors/margins/thresholds match across deliverables: κ bands 0.8/0.6; layer gap ≥0.10; judge share >0.20; agree-wrong ≥0.05 (CI LB >0.02); style-share ≥0.10; family gap ≥0.10; ρ ≥0.5; B0 +0.05; Ω gates 0.5/0.2; cell minima 20/15 tasks/traces and 3/6 pairs.
- `latexmk -pdf` rebuild: exit 0, zero errors, no undefined citations, 15 pages.
