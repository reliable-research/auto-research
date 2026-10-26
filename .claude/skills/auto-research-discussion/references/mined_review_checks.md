# Mined reviewer checks (adversarial second pass)

These checks were **mined from real reviewer comments on actual paper submissions** — the reference platform ran a comment-mining pipeline over human peer reviews, clustered recurring concerns, and converted them into reusable checklist items. They answer a different question than the base rubric in `stages.md`:

- The **base rubric** asks: *is this stage's artifact internally well-formed?* (fields aligned, no method leak, hypotheses falsifiable...)
- The **mined checks** ask: *what will a reviewer eventually attack?* — and therefore, what should the design already have an answer for?

Many of these are phrased against a finished manuscript ("have you reported...?"), because that's where the reviewer comments came from. At the design stage, read each one as *anticipatory*: the confirmed stage output doesn't need to contain the full answer, but it shouldn't be structured in a way that makes the answer impossible later. "Have you reported inter-annotator agreement?" at stage 6 means: does the experiment plan include an annotation-quality step at all, or will that hole only surface at rebuttal time?

## When to run this pass — and when not to

**Do not run these on round 1.** The base rubric comes first; piling 20+ mined checks onto a first draft violates the don't-pile-on principle and buries the structural issues that matter most. Run the mined pass when:

- The user explicitly asks for a "hard review," "reviewer-level review," or "what will reviewers say"
- A stage passed the base rubric suspiciously easily (clean first critique on a nontrivial draft — the classic sign the critic wasn't looking hard enough, especially in autoclaude self-play)
- The stage is 5 or 6 and the user is targeting a competitive venue — these two stages carry the most mined checks because they're where real reviews concentrate
- Autoclaude mode, as the "what would a cold reader flag first?" self-prompt made concrete

When you do run it, **don't walk all items mechanically.** Scan the stage's list, pick the 3-6 checks most likely to bite *this specific paper*, and raise only those. A mined check that clearly doesn't apply (no annotation → skip annotation-quality checks) costs credibility to raise.

**Severity calibration:** mined checks default to `[minor]` at the design stage — they're anticipatory, not structural. Promote to `[major]` only when the design actively forecloses the answer (e.g., the experiment plan has literally no external baseline and the paper is `study_type: technical`, so "overreliance on internal comparisons" isn't a future risk, it's a present defect).

## Expertise tiers

Each check carries the expertise level of the reviewers whose comments it was mined from:

- **[gen]** general research quality — any competent reviewer raises these; the platform curated 13 of them into its always-on active set, marked ⭐ below. Prioritize these.
- **[res]** research-expert — methodology-literate reviewers (statistics, ablation discipline, reproducibility norms). Heaviest in stages 5-6.
- **[dom]** domain-expert — reviewers deep in the specific subfield (SE/ML in the source data). Apply when the user's target venue has that depth; skip for early-stage drafts.

---

## Stage 1: Problem Definition

- **[dom] Limited scope or generalizability** — if the problem scope is narrow, is the choice justified, with an argument for how findings would generalize to broader settings? (At stage 1 this means: is a narrow scope a *stated, defended* constraint rather than an unexamined default?)

Stage 1 draws only one mined check — real reviewer complaints rarely target the problem statement directly; they target its downstream consequences. If the base rubric passed, move on.

## Stage 2: Motivation

- ⭐ **[gen] Unclear problem definition, objectives, key concepts** — are the core problem, boundaries, goals, and the mapping from evaluation criteria to claimed outcomes all explicit, with motivating examples?
- ⭐ **[gen] Insufficient evidence for effectiveness/generalizability** — are practical-importance claims backed by something checkable (data points, practitioner evidence, prior findings) rather than assertion?
- ⭐ **[gen] Practical applicability unclear** — is there a concrete story for how practitioners would adopt this, integrate it into a workflow, and get value even from imperfect outputs?
- ⭐ **[gen] Venue fit and community relevance** — do the framing, background, and citation set match the intended research community, with domain-relevant implications?
- ⭐ **[gen] Limited novelty or insight** — is there a stated reason this goes beyond straightforward application of known techniques?
- **[dom] Weak motivation / real-world significance** — is the prevalence, importance, or actionability of the motivating problem demonstrated — are the targeted failures ones practitioners actually care about?
- **[dom] Overclaiming or weak novelty** — are new contributions clearly distinguished from reapplications of known techniques, with prior art cited rather than elided?
- **[dom] Limited generalizability or coverage** — is there any evidence (or at least an argument) that the approach generalizes beyond the specific frameworks/benchmarks named?
- **[res] Inadequate engagement with prior work** — are claims about prior approaches' limitations backed by citations, not just asserted? (Overlaps stage 3 — raise here only if the *motivation itself* leans on an unsupported claim about prior work.)

## Stage 3: Related Work

- **[dom] Poor organization and positioning** — is related work organized into meaningful categories/taxonomy with a clear statement of where this work sits in the conceptual lineage — or is it a flat list?
- **[dom] Incomplete literature and tool coverage** — are relevant recent work, domain-specific literature, practical tools, and alternative approaches all represented? (For LLM-adjacent topics the "recent" bar moves fast — a search-backed pass matters here.)
- **[dom] Unclear or overstated novelty** — is it explicit which aspects are novel vs. derivative, with concrete evidence for the novel claims?
- **[dom] Insufficient novelty or differentiation** — is the approach explicitly compared to existing literature, showing which elements are genuinely new?
- **[dom] Failure to adapt or evaluate prior methods** — if prior approaches "don't apply," was a reasonable adaptation attempted or their limitation quantified, rather than dismissing them outright? Reviewers punish hand-waved incompatibility.
- **[dom] Insufficient comparative analysis planned** — do the flagged baselines (`is_potential_baseline`) actually cover closely related *and contemporary* methods, so the eventual comparison is informative?
- **[dom] Incremental engineering / integration of existing components** — if the contribution composes existing models or workflows, is there a case that the integration yields substantially different capabilities, not modest adjustments? This is one of the most common kill-shots in SE/ML reviews — confront it at stage 3, not at rebuttal.
- **[dom] Empirical observation without methodological advance** — if the contribution is primarily analysis or benchmarking, does it also contribute a framework, methodology, or tool that enables follow-up work? (Directly relevant to `study_type: empirical` papers.)
- **[dom] Inadequate methodological justification vs. best practices** — are key design/statistical choices positioned relative to what prior work established as accepted practice?
- **[dom] New taxonomies need reproducibility detail** — if this work introduces new taxonomies, labels, or reporting practices, note now that full construction detail (versions, selection criteria) will be owed later.

## Stage 4: Sub-Problems

No stage-4-specific mined checks exist in the source pool — real reviewers don't see decompositions, they see their consequences. The relevant adversarial question at stage 4 is borrowed from stages 3 and 5: *does each sub-problem survive the "incremental integration" and "goal restatement" attacks it will face once it becomes a method?* If a sub-problem's only conceivable method is "wire together two existing tools," the incremental-engineering complaint is already loaded.

## Stage 5: Method Design

⭐ Curated tier first:
- ⭐ **[gen] Ambiguous scope, assumptions, labels** — are task, objectives, success criteria, scope, threat/adversary model, key assumptions, and label/annotation provenance all explicit?
- ⭐ **[gen] Insufficient methodological/implementation detail** — is enough procedural detail specified (algorithms, prompts, parameters, resources) that reproduction is *plannable*?
- ⭐ **[gen] Undefined terms and inconsistent terminology** — is every domain-specific term/symbol defined at first use and used consistently?
- ⭐ **[gen] Unclear metrics and reported outputs** — are outputs, metrics, and evaluation semantics operationally defined (what exactly is computed, what a probability means)?
- ⭐ **[gen] High manual or engineering effort** — is required human labor (labeling, triage, domain adaptation) quantified and its practicality defended?

Research-expert tier — the methodology attacks:
- **[res] Missing rationale for design choices** — is every load-bearing choice (architecture, thresholds, operators, windowing, tooling) justified with a principled argument or comparison to alternatives? (This generalizes the base rubric's `unmotivated_design_choice` to reviewer strength.)
- **[res] Missing theoretical justification / guarantees** — is there any formal analysis, identifiability argument, or principled modeling assumption for *why* the approach should work — and are soundness/correctness limits stated?
- **[res] Unjustified modeling assumptions** — are threat models, attacker behavior, causal structure, or perturbation bounds stated and defended for applicability?
- **[res] Brittle search/decision procedures** — if the method makes early single-shot decisions (search, generation, selection), is sensitivity to those decisions acknowledged, with recovery/mitigation?
- **[res] Pipeline incoherence** — are all pipeline stages actually consistent with each other (specifications match dynamic behavior, selection strategies coherent)?
- **[res] Representation vs. usage mismatch** — if a formal/structured representation is proposed, do downstream components actually *use* its semantic properties, or is it just a data container? (A distinctly sharp check for skills/agent-artifact papers.)
- **[res] Insufficient failure-mode analysis** — is there a plan for systematically characterizing error types (FP/FN, hallucination, overfitting) and handling indeterminate cases?
- **[res] Unvalidated auxiliary artifacts** — if the method relies on constructed labels, measures, or pretrained-tool outputs, is their fidelity going to be validated/calibrated, and their influence on results quantified?
- **[res] No end-to-end concrete example** — can the design show one input→output trace demonstrating how the high-level specification becomes concrete behavior?
- **[res] Temporal/context fragmentation** — if the method windows, segments, or truncates context, is the cost to long-range dependencies examined or at least justified?
- **[res] Misaligned objectives and metrics** — are scoring functions, fitness objectives, and diversity metrics actually aligned with the target property, or just convenient to compute?

Domain-expert tier:
- **[dom] Missing assumptions/threats-to-validity analysis** — are preconditions, theoretical limits, and any privileged/unrealistic experimental conditions stated and analyzed?
- **[dom] Reliance on weak observable signals** — how does the method behave when its required signals are missing, ambiguous, or unreliable?
- **[dom] Limited cross-domain generalizability** — is applicability beyond the evaluated domain/dataset/architecture justified, with a statement of what generalizing would require?

## Stage 6: Experiment Design

This is where mined checks concentrate (30 of 85) — real reviews live here. Grouped by attack surface:

⭐ Curated tier:
- ⭐ **[gen] Under-specified procedures and human intervention** — full workflows: hyperparameters, exact run configurations, compute budgets, resampling procedures, and the extent of any human-in-the-loop steps.
- ⭐ **[gen] Incomplete/unjustified evaluation** — protocols, success criteria, benchmark-selection rationale, all reported metrics and model entries, plus runtime/cost for interpretability.
- ⭐ **[gen] Unclear real-world harm or practical impact** — if the work identifies failures/bugs, is there evidence they're consequential in realistic practice, not just detectable in contrived cases?

**Baselines** (the single most-attacked surface):
- **[dom] Unjustified baseline selection** — why was each baseline included *or excluded*, and how does each comparison help interpret the claims?
- **[dom] Omitted baseline coverage** — recent SOTA, simple heuristic baselines, alternative methodological categories, relevant model-family variants — informative comparisons need all four kinds represented or their absence defended.
- **[res] Conceptually misaligned baselines** — same task formulation, assumptions, and capabilities as the method — or an explained mismatch.
- **[res] Baseline configuration fairness** — baseline implementations, prompts, hyperparameters, seeds, and tooling matched to the method's conditions and documented.
- **[dom] Overreliance on internal comparisons** — at least one *independent external* baseline, not only self-ablations.
- **[res] Comparative evaluation under identical conditions** — rerun prior work under your reproducible conditions rather than comparing against heterogeneous cited numbers.
- **[res] Fairness of resource accounting** — matched compute/time budgets, test access, guidance; resource differences reported or normalized.

**Statistical rigor:**
- **[res] Stochasticity and variability** — repeated runs, seed control, variance measures, confidence intervals, effect sizes, hypothesis tests. (Directly aligned with this skill's `statistical_test` / `sample_size_rationale` fields — those exist because of this class of comment.)
- **[res] Metrics definition and thresholding** — metrics, aggregation rules, and operating thresholds defined consistently; conversions and composite scores justified.
- **[res] Unclear metric reporting** — operational definitions, computation procedures, counts of unknown/unclassified cases, uncertainty quantification.
- **[res] Unsupported causal claims** — if any RQ makes a causal claim, are identifiability conditions stated, with controls separating causation from correlation?

**Data:**
- **[res] Dataset provenance, sampling, and label quality** — sources, initial pools, sampling/filtering, deduplication, synthetic-generation procedures, annotator instructions, conflict resolution, inter-annotator agreement.
- **[res] Labeling bias** — annotation procedures validated to reduce systematic bias.
- **[res] Contamination and leakage** — checked and reported overlap between evaluation data and models/resources (training-set leakage, memorized artifacts). Increasingly a default reviewer question for anything LLM-based.
- **[res] Limited scope / external validity** — breadth of models, datasets, benchmarks justified against the generality of the claims; narrow scope explicitly bounded.
- **[dom] Limited generalization / real-world evaluation** — OOD transfer, cross-domain performance, end-to-end impact beyond intermediate metrics.

**Analysis depth:**
- **[res] Ablation and component isolation** — systematic ablations, controlled variants, per-component attribution (including transfer-to-baseline tests), so effects attach to specific modules.
- **[res] Robustness / sensitivity / adversarial evaluation** — sensitivity to hyperparameters, inputs, and design choices; adaptive or adversarial settings where the claim invites them.
- **[res] Failure-mode analysis with qualitative examples** — aggregate scores supplemented by representative examples, per-case error breakdowns, root-cause triage.

**Practicality:**
- **[res] Scalability and cost analysis** — runtime, throughput, latency, memory, monetary/API cost, or at least a trade-off discussion.
- **[res] Demonstrated practical benefit** — evidence the improvement is *meaningful and actionable*, not just statistically detectable.
- **[res] Reproducibility package** — code, prompts, decoding settings, seeds, splits, exact protocols, baseline implementations planned for release.

---

## Cross-cutting writing checks → paper assembly

Eleven mined checks target manuscript quality rather than any design stage (section organization, notation consistency with worked examples, figure/table quality, proofreading, typesetting artifacts, artifact accessibility/READMEs, actionable-implications discussion, and **RQ framing that matches graded outcomes rather than binary yes/no**). These belong to the paper-assembly step, not the stage loop — `paper_assembly.md` carries them as a pre-handoff checklist. The RQ-binary-framing check is worth one early glance at stage 6 too: if an RQ's `expected_outcome` is graded but its `description` is phrased yes/no, fix the phrasing now.
