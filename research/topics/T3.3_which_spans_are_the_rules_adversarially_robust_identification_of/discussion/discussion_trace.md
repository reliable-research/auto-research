# Discussion Trace — T3.3 (auto-research-discussion, Stages 1–6)

> Extracted verbatim from `discussion/pipeline.md` per the `auto-research-discussion` skill's Final Deliverables spec (a completed run produces three separate artifacts: `paper_draft.md`, `experiment_design.md`, `discussion_trace.md`). This file is the complete round-by-round record across all six stages — every draft version, every critique (comments, severities, resolution), every decision, every refiner pass — moved here unchanged from the original run log. It is the audit trail behind the confirmed stage outputs that fed `paper.md` and `paper_draft.md`/`.tex`/`.pdf`.
>
> The goal.md §2 pipeline-state Phase Log (resumability tracking, added after this trace was produced) remains in `discussion/pipeline.md`, not here — that section tracks a different, later-added process (reference-cache upgrade + Phase A bundle validation), not the six-stage discussion itself.

> Mode: **autoclaude** (self-play, Claude as student+teacher). Source: `../digest.md` (N0–N12) + `../paper.md` (Steps 0–9), both pre-existing reverse-digest artifacts for seed **T3.3**. Round cap: 5/stage (none hit). All six stages converged in 1 critic round + 1 refiner pass each — the seed material was unusually mature (paper.md already carries its own asymmetry check, taste self-audit, formal notation, and pre-registered fallbacks), so genuine disagreement surfaced but didn't require re-proposing.
>
> **Full pipeline order (updated):** this file (`auto-research-discussion`, 6 stages) → `taste_audit.md` (`research-taste-auditor`, idea-level check on Stage 2+5) → `stage_review.md` (`pengsida-stage-reviewer`, PASS/REVISE/STOP per stage against the confirmed outputs, plus a Stage 5 Writing check on the first assembled draft) → final `paper_draft.md`/`.tex`/`.pdf`. Two structural requirements that B5.5's own pipeline caught as REVISE findings after the fact — a nearest-neighbor sentence in Related Work, and per-RQ falsification conditions in Experiments — are treated as mandatory from the first assembly pass here (see the task brief), so `stage_review.md` had to look elsewhere for genuine findings; read that file for what it actually found.

## Seed brief

- **One-sentence description:** Measure whether identifying which spans in an LLM agent's context are governance constraints (the precondition for memory-pinning) survives adversarial paraphrasing that disguises constraints as chit-chat (evasion) or disguises chit-chat as constraints (spoofing).
- **Apparent inputs:** a raw agent context window mixing constraint and non-constraint spans; a constructed paired corpus (GovSpan-Adv) of constraint/non-constraint spans with validated bidirectional adversarial rewrites; five identifier families under test.
- **Apparent outputs:** a per-span pin/no-pin decision with confidence; per-direction error rates (miss-pin / false-pin) under original vs. adversarial phrasing; a robustness-gap Δ and its decomposition into genuine identifier failure vs. contested ground truth.
- **Closest research areas:** instruction/data separation and role-based authority (ASIDE, Instruction Hierarchy); adversarial prompt injection and attack/defense benchmarking (ChatInject, TensorTrust); sequential harmfulness monitoring under benign-looking disguise (SeqMonitor); long-horizon preference retention (PrefEval); revisitable agent memory (MemoryCallback); fixed-taxonomy guardrail classification (R2-Guard); cooperative constraint mining (RECAST).
- **In scope:** measuring existing/adapted identifier families' span-level identification reliability under a validated, bidirectional register-disguise attack, in isolated-pair and in-context-transcript form. **Out of scope:** designing a new, better identifier as the paper's contribution; downstream pinning-budget mechanics; live/non-sandboxable deployments; non-English governance-constraint corpora.
- **Confidence: high.** As with the B5.5 exemplar, the "repo" here is itself a prior reverse-digest + pre-registered spec (`digest.md` + `paper.md`), already cross-referenced (N-node ↔ M-component ↔ RQ ids) and already carrying its own asymmetry/taste check (`paper.md` Step 0/3) and pre-committed fallbacks (Step 6). Reconstruction risk is low; the discipline this run adds is (a) genuine critic pushback rather than restating what `paper.md` already settled, and (b) reformatting the staged design into this skill's stage-1..6 schema, which surfaces a few structural questions `paper.md`'s own format doesn't force (e.g., explicit sub-problem/method traceability, tiered RQ accounting).

---

## Stage 1 — Problem Definition

### Round 1 (critic phase)

**draft_v1** (proposer):
- `summary`: Given a context window containing a mixture of governance-constraint spans (rules the agent must keep obeying) and ordinary conversational spans, and given that either type of span can be adversarially paraphrased — a constraint disguised in casual register (evasion) or chit-chat disguised in imperative register (spoofing) — determine whether an identifier can still correctly decide, per span, whether it must be pinned, and at what reliability relative to its performance on non-adversarial phrasing.
- `input`: (1) a raw agent context window / multi-turn transcript mixing constraint and non-constraint spans; (2) a constructed set of constraint/non-constraint span pairs with validated ground-truth labels; (3) validity-gated adversarial rewrites of each pair (Evade: constraint → casual register, force preserved; Spoof: chit-chat → imperative register, no force introduced).
- `output`: (1) a per-span pin/no-pin decision with confidence; (2) per-direction error rates (miss-pin rate, false-pin rate) on original vs. adversarial phrasing, per identifier family; (3) a robustness gap Δ = error(adversarial) − error(original).
- `constraints`: ground-truth labels must be validated (inter-annotator agreement reported) before any identifier is evaluated; adversarial rewrites must be gated for validity (the rewrite must actually preserve or withhold binding force, not merely appear to).
- `objective`: an identifier is judged adversarially robust for a given direction if its error rate under validity-gated adversarial phrasing is not significantly higher than under original phrasing.
- `study_type`: `empirical` — stated explicitly: digest N12 already classifies this as a measurement study ("we measure whether a presupposed capability survives an adversary"), not a new-identifier-as-contribution paper.

**critique:**
- summary: The draft is evidence-traceable and correctly scoped, but the objective has the same evaluability gap the digest itself already names, and `input` conflates two distinct things without saying which is primary at this stage.
- comments:
  - `{severity: major, field: "objective", anti_pattern: "vague_success (evaluability gap)", comment: "Digest N1's own constraints field says the study 'assumes a labeled, paired ground truth exists for evaluation purposes, not that real-world constraint-hood is always cleanly separable' (C4), and paper.md Step 5 formally defines a 'contested' case as one where blind re-annotators disagree with the gold label. The objective as drafted treats every error as an identifier failure. A success/failure criterion that doesn't name the contested-label case as a first-class possibility isn't fully evaluable as written — a robustness gap could be measured and misattributed entirely to identifier weakness when a fraction of it is genuinely unresolvable ground truth."}`
  - `{severity: minor, field: "input", anti_pattern: null, comment: "Item (1) (a raw deployment context window) and item (2) (a constructed paired corpus) are two different objects — a live transcript is unsegmented and unlabeled; the constructed corpus is pre-segmented and labeled by design. The pilot stage (per digest N6/M1) deliberately uses only the constructed, pre-segmented form and defers the raw-transcript form to Stage 2 of the methodology (M6). The problem statement should say which is being defined here, or that both are in scope with the pre-segmented form as the object of the pilot-stage objective specifically."}`
- decision: `move_to_refiner` (both flags are formalize-level fixes using content already in the digest and paper.md — no new content needed).

### Refiner pass

- `objective` (refined): "An identifier's directional robustness is accepted or refuted only relative to a validated ground truth: a robustness gap Δ is attributed to identifier failure only for the fraction of errors that survive a blind, full-context re-annotation audit (i.e., where independent annotators agree with the original gold label); errors where blind annotators split or disagree with gold are reported separately as *contested*, not folded into the robustness verdict."
- `input` (refined): explicitly split into "(1a) the constructed, pre-segmented span-pair corpus (GovSpan-Adv) — the primary object of the Stage-1 (pilot) objective — and (1b) unsegmented multi-session transcripts with the same items embedded at controlled depths, which extends the objective to joint localization+classification at Stage 2 of the methodology, not the pilot."
- `formal_summary` (added, per stage-1 refiner's formalize-for-free duty, lifted directly from paper.md Step 5 notation): "Context window as a span sequence $S=(s_1,\dots,s_n)$; each span has latent label $y_i \in \{0,1\}$ (constraint/non-constraint). Identifier $f_\theta(s_i, \text{ctx}) \to (\hat y_i, c_i)$. Rewrite operators $\text{Evade}(s\mid y{=}1)$ and $\text{Spoof}(s\mid y{=}0)$ each certified by a validity gate $V$. Objective: characterize $\Delta = \text{err}(\text{adversarial}) - \text{err}(\text{original})$ per direction per identifier, decomposed into identifier-attributable and contested-label components."
- `changes_made`: tightened `objective`'s evaluability condition to name the contested-label case explicitly; split `input` into pilot-stage vs. scale-up objects; added `formal_summary`.
- `declined_to_fix`: none.

**Confirmed Stage 1** — `study_type: empirical`.

---

## Stage 2 — Motivation

### Round 1 (critic phase)

**draft_v1:**
- `summary`: Memory-pinning mechanisms for LLM agents can only preserve a governance constraint if the upstream step — deciding which spans are the rules — correctly recognizes it as one in the first place, and this recognition step has never been measured for adversarial robustness.
- `why_it_matters`: Existing treatments of "which text is binding" assign that status by channel position (system vs. user vs. tool) known a priori, not computed from content — so a rule delivered in an ostensibly low-privilege channel gets no special status, and filler delivered in a privileged channel is over-trusted. If an agent's memory-pinning safeguard rests on an identification step that keys on surface register, then an adversary who can preserve a rule's binding force while flattening its register into small talk defeats pinning without ever touching the pinning mechanism itself — and no prior work measures this because attack-and-defense literature reports end-behavior compromise (hijack success, extraction), never the span-level identification error that caused it.
- `who_cares`: Designers of agent memory/pinning systems who treat "detect the constraint" as a solved precondition; safety teams evaluating whether governance rules embedded in long-running agent deployments actually stay enforced; researchers deciding whether structural-authority findings (role tags, channel position) transfer to a purely semantic register-disguise threat.
- `evidence`: `[ASIDE, OpenReview:C81TnwHiRM]`'s own motivation concedes the model "must infer executability from contextual cues, which adversaries can manipulate" — its fix relocates the label (assigns it by embedding subspace) rather than computing it from content; `[ChatInject, OpenReview:WVhgFSKniL]` demonstrates the structural half of this exact spoofing threat (forged role tags), but never the semantic-register half (no structural forgery, register alone); `[MemoryCallback, OpenReview:1cymflI2Lh]`'s own motivation is that "information encountered early... may be overwritten before its relevance becomes clear" — a benign version of exactly the failure an adversary could induce deliberately.

**critique:**
- summary: Well-grounded with real citations tied to specific claims, but the motivation doesn't explain why Stage 1's *per-direction, separately-reported* error rates specifically matter, as opposed to one aggregate identification-error number.
- comments:
  - `{severity: major, field: "why_it_matters", anti_pattern: "partial_output_coverage", comment: "Stage 1 output (2) is not one error rate — it's miss-pin and false-pin reported per direction. The current why_it_matters motivates why identification failure in general is dangerous, but never explains why the two directions need to be measured and reported separately rather than pooled into one accuracy number. This matters concretely: an evader (who wants a constraint to slip through unpinned) and a spoofer (who wants filler wrongly pinned, e.g. to exhaust a fixed pin budget or launder authority) have opposite goals, and digest C3 already names the consequence — hardening against one direction by moving a decision threshold necessarily softens the other. Without stating this, a reader could reasonably ask 'why not just report overall accuracy' — a real, currently unaddressed gap."}`
- decision: `move_to_refiner`.

### Refiner pass

- `why_it_matters` (extended): "...critically, these two failure directions are not interchangeable and cannot be safely collapsed into one number: an evader benefits specifically from miss-pins (a live rule silently drops out of enforcement), while a spoofer benefits specifically from false-pins (filler content wrongly earns authority, which can exhaust a bounded pin budget or be used to launder instructions as if governance-sanctioned). Because these are opposite-direction failures, a defender who shifts an identifier's decision threshold to suppress one necessarily makes the other easier — so a single pooled accuracy number would hide exactly the tradeoff an adversary is positioned to exploit, and only per-direction reporting makes that tradeoff visible and actionable."
- `changes_made`: added the direction-asymmetry argument, tying it to Stage 1's two separate output metrics.
- `declined_to_fix`: none.

**Confirmed Stage 2.**

---

## Stage 3 — Related Work

All nine works below are treated as **specific (deep) tier** — digest N3 already engaged each one at the approach + limitation level (motivation and method text actually read for the corpus entries; no title-only landscape mentions were present in the source material, and per the no-fabrication rule, no additional landscape papers are invented here to pad a `general_related_works` list).

### Round 1 (critic phase)

**draft_v1** (`specific_related_works`, abbreviated to citation / I-O framing / limitation / `is_potential_baseline`):

| work_id | citation | is_potential_baseline | limitation (→ sub-problem it will motivate) |
|---|---|---|---|
| `rw_aside` | Anon., ASIDE (OpenReview:C81TnwHiRM) | **true** | Assigns instruction/data role by a fixed embedding-subspace rotation applied at ingestion — role is *relocated*, not computed from content, so a rule delivered in a low-privilege channel gets no special status. |
| `rw_instructionhierarchy` | Wallace et al., 2024 (arXiv:2404.13208) | false (canonical anchor, not runnable baseline) | Trains priority by channel role (system > user > tool); the paradigm ASIDE's baseline row instantiates — same content-vs-position gap, kept as the canonical statement of the paradigm this paper departs from. |
| `rw_chatinject` | Anon., ChatInject (OpenReview:WVhgFSKniL) | false (attack technique, not an identifier) | Demonstrates the *structural* half of the spoofing threat (forged role tags) but never the semantic-register half — content that earns authority through phrasing alone, no structural forgery. |
| `rw_tensortrust` | Anon., TensorTrust (OpenReview:fsW7wJGLBd) | false (corpus source, not an identifier) | Produces real human-written defense prompts (governance rules) and attack/defense benchmarks scored by string-comparison outcome, never span-level identification error. |
| `rw_seqmonitor` | Anon., SeqMonitor (OpenReview:HQuboWvFA1) | **true** | Detects accumulating harmful intent via binary halt decisions over conversation prefixes — the closest existing evasion-via-benign-surface-form treatment, but for trajectory-level harmfulness halting, not per-span constraint retention, and covers only the evasion direction. |
| `rw_prefeval` | Zhou et al., PrefEval (OpenReview:QWunLKbBGF) | false | Tests long-horizon preference retention with benign (not adversarial) distractors sampled from unrelated conversation; conflates inference/retention/application into one following-failure signal. |
| `rw_r2guard` | Anon., R2-Guard (OpenReview:CkgKSqZbuC) | false | Robust guardrail classification over a fixed, enumerable safety taxonomy — governance constraints are open-ended and cannot be pre-enumerated as categories. |
| `rw_recast` | Anon., RECAST (OpenReview:90tCp2KszA) | false (I/O mismatch — cooperative extraction, not adversarial identification) | Mines constraints from cooperative instruction data under fully-stated conditions; its verifiers check response *compliance* with known constraints, never *discovery* of a disguised one. |
| `rw_memorycallback` | Anon., MemoryCallback (OpenReview:1cymflI2Lh) | false (memory architecture, not an identifier) | Fixes benign "premature pruning" via learned callback queries assuming salience can be re-assessed later; models no adversary optimizing content to appear unimportant at write time. |

**critique:**
- summary: Grounding is solid and every limitation is specific and tied to this paper's task, but two baseline labels need scrutiny for the same reason B5.5's SOTOPIA label did.
- comments:
  - `{severity: major, field: "specific_related_works[rw_aside, rw_seqmonitor].is_potential_baseline", anti_pattern: "io_approach_mismatch", comment: "Neither ASIDE nor SeqMonitor is being run and compared against its own reported numbers — per digest N6/M3, ASIDE's position/privilege-signal mechanism is *adapted* into identifier M3d, and SeqMonitor's cumulative-context monitor is *adapted* into identifier M3e. Marking `is_potential_baseline: true` without qualification risks implying a beat-the-published-number comparison, which contradicts this paper's own `study_type: empirical` framing (no outcome-tier RQs, no 'beats baseline X' claims). Per the stage-3 rubric, if the I/O framing doesn't match (ASIDE assigns role at ingestion under non-adversarial assumptions; SeqMonitor halts trajectories, it doesn't emit per-span pin decisions), the work is 'not a baseline in the beat-a-number sense — at best a method-side reference' whose *mechanism*, not its published results, is being borrowed."}`
- decision: `move_to_refiner` (a wording-precision fix, not structural — the underlying design already only adapts the mechanism, per N6).

### Refiner pass

- `rw_aside.is_potential_baseline` and `rw_seqmonitor.is_potential_baseline` retained as `true`, but each field's accompanying note sharpened: "Not a baseline in the beat-a-number sense — [ASIDE's / SeqMonitor's] own reported results are not compared against. Its **privilege-signal mechanism** [position-derived role labels / cumulative-context halting] is adapted as one identifier family under test (M3d / M3e), independent of its published findings."
- `changes_made`: clarified both baselines' role to avoid an implied I/O-mismatched comparison against published numbers.
- `declined_to_fix`: none.
- **Note on `verify_as_hypothesis`:** set `false` on every limitation. None is flagged as a stage-6 framing-tier RQ — every limitation here is already fully absorbed into a Stage-4 sub-problem and Stage-5 method rather than needing its own standalone verification RQ. Per stages.md: *"If nothing was flagged, emit zero framing-tier RQs — don't manufacture one."*

**Confirmed Stage 3.**

---

## Stage 4 — Sub-Problems

### Round 1 (critic phase)

**draft_v1** (5 sub-problems, from digest N5's C1–C4 plus one novel confound-isolation problem):

- **`sp_force_register_decoupling`** — *description:* Determine whether an identifier's decision is actually tracking binding (deontic) force, or merely correlated surface register that can be moved independently of force. *why_it_is_a_problem:* If force and register are separable but every identifier is (implicitly) keyed on register, every measured "identification accuracy" number is a register-detection number wearing a force-detection label — the entire premise of pinning rests on a property the field has never actually isolated. *technical_challenge:* proving the decoupling requires a paraphrase that provably preserves force while moving register (and the reverse) — not just phrasing that "looks" disguised — which needs an explicit, checkable validity criterion, not a stylistic rewrite. *source_limitation_ids:* `["lim_aside_position_not_content"]` (ASIDE/Instruction-Hierarchy assign role by channel position, assuming away exactly this decoupling rather than testing it).
- **`sp_joint_localization`** — *description:* Determine whether identification degrades further when a disguised span must first be found inside a long, unsegmented transcript, not just classified once handed a pre-cut span. *why_it_is_a_problem:* Real deployments never hand an identifier pre-segmented pairs; if all measurement happens on pre-cut spans, a real component of deployed risk (boundary/localization failure) is invisible by construction. *technical_challenge:* joint boundary detection + classification is a strictly harder task than classification alone, and disentangling "found it, misclassified it" from "never found it" requires depth-stratified, overlap-credited localization metrics, not a single pass/fail flag. *source_limitation_ids:* `["__novel__"]` — no cited work evaluates governance-constraint span localization under adversarial disguise; PrefEval's distractors are unrelated conversation, not disguised look-alikes, so it doesn't stress this specific gap.
- **`sp_direction_asymmetry`** — *description:* Report and characterize the tradeoff between miss-pin and false-pin errors rather than a single pooled error rate, since the two errors serve opposite-goaled adversaries. *why_it_is_a_problem:* An operating point chosen to suppress one direction mechanically loosens the other (per Stage 2's motivation); reporting only aggregate accuracy would hide exactly the exploitable tradeoff. *technical_challenge:* this requires a paired, per-direction statistical design (not just two averages) and a threshold-swept view (AUROC) to show the tradeoff is a frontier, not a coincidence of one chosen cutoff. *source_limitation_ids:* `["lim_seqmonitor_evasion_only"]` (SeqMonitor's threat model covers evasion-style disguise only, never the spoofing direction, so its design cannot even in principle expose this asymmetry).
- **`sp_label_indexicality`** — *description:* Separate genuine identifier failure from cases where the "correct" label is itself contested once full context and speaker authority are considered. *why_it_is_a_problem:* per the `[边界]` (boundary) framing of this topic, some spans' constraint-hood is inherently ambiguous (e.g. "let's keep this between us" as binding confidentiality vs. idle phatic talk) — reporting a robustness gap without this decomposition risks attributing irreducible ground-truth ambiguity to identifier weakness, overstating the finding either way. *technical_challenge:* this requires a blind, full-context re-annotation protocol run *after* errors are observed, structurally independent from the original labeling pass, so the audit isn't contaminated by the same judgment call that produced the contested label in the first place. *source_limitation_ids:* `["__novel__"]` — R2-Guard's fixed-taxonomy design (`lim_r2guard_fixed_taxonomy`) assumes categories are enumerable and non-contested by construction, which is the closest related assumption, but no cited work treats label ambiguity itself as a measured quantity; the decisive-component justification is that no identification claim in this space is checkable without it.
- **`sp_attacker_defender_confound`** — *description:* Rule out that a measured robustness gap reflects the adversarial rewriter and the identifier sharing a model family's own self-consistent notion of register, rather than a genuine, family-independent force/register decoupling. *why_it_is_a_problem:* if the rewriter (M2) and the strongest identifier (the LLM-as-judge, M3c) come from the same model family, part of any measured Δ could be an artifact of that family's internal consistency, not evidence about identification in general — an alternative explanation the headline claim must rule out. *technical_challenge:* isolating this requires deliberately swapping the rewriter's model family and re-measuring, which is a distinct manipulation from anything the other four sub-problems require. *source_limitation_ids:* `["__novel__"]` — this is a validity threat internal to this paper's own design (paper.md's own A3/t2), not a gap in a cited work, so no `lim_*` id applies; it is a decisive component because without it the paper's central claim is confounded by construction.

**critique:**
- summary: Coverage checks out (solving all five would jointly deliver Stage 1's objective) and the novel-component justifications are real, but one sourcing choice is weaker than it looks.
- comments:
  - `{severity: major, field: "sp_label_indexicality.source_limitation_ids", anti_pattern: "weak justification (not a named anti-pattern, but fails the rubric's 'is each limitation relevant to this problem, not a content-free tie')", comment: "R2-Guard's fixed-taxonomy limitation (`lim_r2guard_fixed_taxonomy`) is about categories being *enumerable*, not about labels being *contested* — enumerability and indexicality are different properties (a taxonomy can be small and fixed yet every category still be uncontested, or open-ended yet every instance still be clearly one thing or another). Citing it as grounding implies a tighter connection than exists; this sub-problem is better stated as purely `__novel__`, since its actual justification (no cited work treats label ambiguity as a measured quantity) doesn't need R2-Guard's taxonomy point to stand on its own."}`
- decision: `move_to_refiner` (a sourcing-precision fix — the sub-problem's own justification is already strong without the strained tie).

### Refiner pass

- `sp_label_indexicality.source_limitation_ids` changed to `["__novel__"]` (dropping the strained R2-Guard tie); `why_it_is_a_problem` left unchanged since its own justification was already self-sufficient.
- `changes_made`: removed the weak limitation tie for `sp_label_indexicality`, standing it fully on its `__novel__` decisive-component justification.
- `declined_to_fix`: none.

**Confirmed Stage 4** (5 sub-problems; 3 sourced from Stage-3 limitations, 2 `__novel__` with stated decisive-component justifications).

---

## Stage 5 — Method Design

### Round 1 (critic phase)

**draft_v1** (5 methods):

- **`m_bidirectional_rewrite`** → targets `sp_force_register_decoupling`. *proposed_approach:* Two validity-gated LLM rewrite operators — Evade(constraint → casual register, force preserved) and Spoof(chit-chat → imperative register, no force introduced) — each gated by an NLI-style entailment back-check plus 2-annotator validation before use; rewriter model family kept disjoint from every identifier family. *key_insight:* the only way to test whether an identifier is keyed on register rather than force is to construct a rewrite that is *provably* force-preserving (or force-withholding) while register moves — validity gating turns "is this rewrite valid" from an assumption into a checked precondition, rather than trusting the paraphrase at face value. *hypotheses:* ["The validity gate certifies 70–80% of raw Evade/Spoof rewrites on first generation pass (rejection rate 20–30%), with post-gate inter-annotator Cohen's κ ≥ 0.7 on rewrite validity.", "For at least four of the five identifier families, identification error on validity-gated adversarial rewrites is significantly higher than on original phrasing (Holm-corrected McNemar test, per direction), with mean robustness gap Δ̄ ≥ 0.10 across families for the pre-registered primary identifier (LLM-as-judge)."]
- **`m_paired_direction_metrics`** → targets `sp_direction_asymmetry`. *proposed_approach:* Report miss-pin and false-pin as separate paired statistics per identifier per direction (McNemar exact tests, Holm-corrected across identifiers × directions); sweep the decision threshold to trace an AUROC-style frontier. *key_insight:* pooling into one aggregate accuracy hides exactly the tradeoff an adversary is positioned to exploit — only a per-direction, threshold-swept design exposes whether hardening against one error mechanically loosens the other. *hypotheses:* ["Under adversarial phrasing, miss-pin rate significantly exceeds false-pin rate: the 10k-bootstrap 95% CI on (missrate_adv − fprate_adv) lies strictly above 0.", "Sweeping an identifier's decision threshold to reduce its adversarial miss-pin rate measurably increases its adversarial false-pin rate for the same identifier — no single operating point minimizes both error directions simultaneously."]
- **`m_incontext_localization`** → targets `sp_joint_localization`. *proposed_approach:* Embed validated GovSpan-Adv items at controlled depths (early/middle/late thirds) inside long, unsegmented multi-session transcripts built from filler conversation; require identifiers to localize (span-level F1, IoU ≥ 0.5) and classify jointly, without given span boundaries; a final adaptive round gives the rewriter query access (≤20 queries/item) to the best Stage-1 identifier and re-runs Evade/Spoof. *key_insight:* an evaluation built only from pre-segmented pairs measures the classification half of the problem and brackets localization entirely; embedding at controlled depths is what turns "does context length/position matter" into a measurable, depth-stratified quantity rather than an assumption. *hypotheses:* ["In-context span-level miss-pin rate (embedded, unsegmented, IoU ≥ 0.5 overlap credit) exceeds isolated-pair miss-pin rate, with paired-bootstrap 95% CI strictly above 0.", "Δ_adaptive exceeds Δ_static for the best Stage-1 identifier, with paired-bootstrap 95% CI strictly above 0."]
- **`m_boundary_audit`** → targets `sp_label_indexicality`. *proposed_approach:* All items on which the best identifier errs, plus a matched random sample of correct items, are re-annotated blind by 2 annotators given full context; errors are partitioned into genuine identifier failure (annotators agree with gold) vs. contested-label cases (annotators split or flip). *key_insight:* aggregate error rates silently blend two different things — an identifier being wrong and a label being genuinely ambiguous — and only a blind, independently-run re-annotation pass, structurally separated from the original labeling process, can tell them apart. *hypotheses:* ["The contested-label fraction among adversarial errors has a Wilson 95% CI upper bound below 0.50 — a majority of measured adversarial fragility reflects genuine identifier failure, not contested ground truth."]
- **`m_cross_family_ablation`** → targets `sp_attacker_defender_confound`. *proposed_approach:* Enforce disjoint model families between the rewriter (M2) and every identifier under test by design; additionally re-run the full rewrite-and-measure pipeline with the rewriter's model family swapped, holding the identifier fixed, and compare the measured Δ. *key_insight:* if rewriter and identifier shared a family, part of any measured gap could reflect that family's own self-consistent notion of register rather than a family-independent force/register decoupling — swapping the family is the only manipulation that isolates the two explanations. *hypotheses:* ["Swapping the rewriter's model family changes the measured robustness gap Δ for the primary identifier by no more than 50% relative to the original-family measurement."]

**critique:**
- summary: Every method has a real, checkable mechanism (no goal-restatement) and every hypothesis names a threshold, but one method is carrying two headline claims and needs the same one-line justification B5.5's stage-5 refiner gave for its own dual-hypothesis method.
- comments:
  - `{severity: minor, field: "m_incontext_localization.hypotheses", anti_pattern: null, comment: "The localization-gap hypothesis (isolated vs. embedded) and the adaptive-attack hypothesis (static vs. adaptive Δ) are both carried by the same in-context transcript harness. Worth stating explicitly why this is one instrument with two readouts, not two mechanisms bundled under one method id — otherwise it reads as scope creep."}`
- decision: `move_to_refiner`.

### Refiner pass

- `m_incontext_localization.key_insight` extended: "...the same embedded-transcript harness yields two separately falsifiable estimands without being two mechanisms: the marginal isolated-vs-embedded gap (tests the localization hypothesis) and the static-vs-adaptive Δ contrast (tests the adaptive-degradation hypothesis) — one harness, two readouts, because both require the same controlled-depth, unsegmented-transcript infrastructure to even be measurable."
- `changes_made`: justified the two-hypotheses-one-method structure explicitly, mirroring the same fix pattern the B5.5 run applied to its own dual-hypothesis method.
- `declined_to_fix`: none.

**Confirmed Stage 5** — 5 methods, **8 hypotheses total** (2 + 2 + 2 + 1 + 1 across the five methods respectively), mixing instrument-validity claims (rewrite-gate yield, family-coupling stability) with the study's headline empirical predictions (degradation, direction dominance, threshold tradeoff, localization gap, adaptive degradation, contested fraction) — a deliberate design choice for an `empirical` study_type.

---

## Stage 6 — Experiment Design

**Tier accounting (checked against study_type=empirical):**
- **Mechanism-tier: 8 RQs**, one per Stage 5 hypothesis (verbatim `target_hypotheses`).
- **Framing-tier: 0 RQs** — no Stage 3 limitation was flagged `verify_as_hypothesis`; none manufactured.
- **Outcome-tier: 0 RQs** — `study_type = empirical` forbids "our identifier beats baseline X" framing. The two baselines below are sanity-check comparators only.

### Round 1 (critic phase)

**draft_v1:**

`datasets`:
- GovSpan-Adv (constructed) — ~300 constraint spans from TensorTrust's released defense-prompt corpus (real access-control rules) plus ~300 non-constraint spans from LMSYS-Chat-1M (real, public), length-and-topic matched; validity-gated bidirectional rewrites per M2. *justification:* both source pools are real, released assets, and TensorTrust's defense prompts are actual human-written governance rules rather than synthetic stand-ins.
- (draft initially listed a second constraint-source pool only as "agent policy / system-prompt rules" with justification "broadens beyond game-derived rules" — flagged below.)
- PrefEval (secondary transfer check) — *justification:* tests whether Stage-1 identifiers flag PrefEval's implicit preference statements as pin-worthy, bridging identification scores to an existing end-to-end retention benchmark (per A5).

`baselines` (sanity-check comparators, not outcome-tier competitors):
- Keyword/deontic-cue heuristic (M3a) run on **original, non-adversarial** phrasing only — the trivial/no-mechanism control: if this already fails on original phrasing, the problem is hard even benignly; if it succeeds on original but collapses on adversarial, that justifies studying the adversarial gap specifically.
- Cross-family rewriter ablation + length/topic-matched non-constraint control (B-alt) — isolates whether measured Δ is register-disguise fragility versus (i) attacker–defender family self-consistency or (ii) spurious length/topic distribution shift.

`research_questions` (8, all mechanism-tier):

| rq_id | target_sub_problem_id | target_hypotheses (verbatim) |
|---|---|---|
| `rq_rewrite_validity` | `sp_force_register_decoupling` | "The validity gate certifies 70–80% of raw Evade/Spoof rewrites on first generation pass (rejection rate 20–30%), with post-gate inter-annotator Cohen's κ ≥ 0.7 on rewrite validity." |
| `rq_adversarial_degradation` | `sp_force_register_decoupling` | "For at least four of the five identifier families, identification error on validity-gated adversarial rewrites is significantly higher than on original phrasing (Holm-corrected McNemar test, per direction), with mean robustness gap Δ̄ ≥ 0.10 across families for the pre-registered primary identifier (LLM-as-judge)." |
| `rq_direction_dominance` | `sp_direction_asymmetry` | "Under adversarial phrasing, miss-pin rate significantly exceeds false-pin rate: the 10k-bootstrap 95% CI on (missrate_adv − fprate_adv) lies strictly above 0." |
| `rq_threshold_tradeoff` | `sp_direction_asymmetry` | "Sweeping an identifier's decision threshold to reduce its adversarial miss-pin rate measurably increases its adversarial false-pin rate for the same identifier — no single operating point minimizes both error directions simultaneously." |
| `rq_localization_gap` | `sp_joint_localization` | "In-context span-level miss-pin rate (embedded, unsegmented, IoU ≥ 0.5 overlap credit) exceeds isolated-pair miss-pin rate, with paired-bootstrap 95% CI strictly above 0." |
| `rq_adaptive_degradation` | `sp_joint_localization` | "Δ_adaptive exceeds Δ_static for the best Stage-1 identifier, with paired-bootstrap 95% CI strictly above 0." |
| `rq_contested_fraction` | `sp_label_indexicality` | "The contested-label fraction among adversarial errors has a Wilson 95% CI upper bound below 0.50 — a majority of measured adversarial fragility reflects genuine identifier failure, not contested ground truth." |
| `rq_family_coupling_stability` | `sp_attacker_defender_confound` | "Swapping the rewriter's model family changes the measured robustness gap Δ for the primary identifier by no more than 50% relative to the original-family measurement." |

(setup/sample-size/statistical-test/expected-outcome/metrics per RQ carried into the paper draft's Experiments section below, reusing paper.md's already-designed Steps 6/9 numbers as authored design targets, not fabricated results.)

**critique:**
- summary: Tier accounting is clean and every RQ traces to a verbatim hypothesis, but one dataset entry has a placeholder justification instead of a real methodological reason.
- comments:
  - `{severity: major, field: "datasets[agent policy/system-prompt rules pool]", anti_pattern: "weak justification (fails the rubric's 'justification for why this dataset actually stresses the hypothesis')", comment: "'Broadens beyond game-derived rules' says nothing about which RQ needs a second source pool or why one game-derived corpus (TensorTrust) isn't sufficient on its own. Digest N10/t3 already names the actual reason (source-pool representativeness) but the dataset entry doesn't carry that reasoning — and no specific, named real corpus is given for this second pool, which risks reading as an unfilled placeholder rather than a design decision."}`
- decision: `move_to_refiner`.

### Refiner pass

- `datasets` entry replaced: "A second, structurally different constraint-source pool — agent/system-prompt policy documents (to be assembled from publicly documented agent-framework system prompts, e.g. released tool-use or assistant policy templates, rather than TensorTrust's game-derived defense prompts alone) — *justification:* digest N10/t3 names source-pool representativeness as a specific external-validity threat (TensorTrust is game-derived access-control rules; LMSYS-Chat-1M is public chat — neither alone represents production governance constraints like multi-sentence policies or tool-permission rules). Drawing constraint spans from two structurally different pools and reporting `rq_adversarial_degradation`'s robustness gap per-source (not just pooled) is what lets cross-source consistency of Δ serve as the generalization check A4 commits to, rather than resting the whole finding on one source's idiosyncrasies. Concrete corpus selection is deferred to implementation time and will be named explicitly once assembled — flagged here as a design commitment, not a citation."
- `changes_made`: gave the second dataset pool a hypothesis-linked, threat-linked reason instead of a generic breadth claim, and was explicit that the concrete corpus is not yet named (avoiding a fabricated citation).
- `declined_to_fix`: none.

**Confirmed Stage 6.**

---

## Cross-stage consistency check (final pass, all six stages)

1. **No method leak** in stages 1/2/4 — checked; `objective`/`why_it_is_a_problem` fields name no technique (identifiers, rewrite operators, and audits are introduced only from Stage 5 onward).
2. **ID stability** — no id renamed mid-run; `sp_*` / `m_*` / `rq_*` stable stage-to-stage (`sp_label_indexicality`'s sourcing changed in its refiner pass, but the id itself did not).
3. **Reference integrity** — `sp_force_register_decoupling.source_limitation_ids = ["lim_aside_position_not_content"]` and `sp_direction_asymmetry.source_limitation_ids = ["lim_seqmonitor_evasion_only"]` ∈ Stage 3 limitations ✓; `sp_joint_localization`/`sp_label_indexicality`/`sp_attacker_defender_confound` = `["__novel__"]` ✓; every `target_sub_problem_id` in Stage 5 ∈ Stage 4 ✓; every Stage 6 `target_hypotheses` entry is a verbatim match to a Stage 5 hypothesis ✓.
4. **Output coverage** — Stage 1's three outputs (per-span pin decision, per-direction error rates, robustness gap Δ) are each reachable: pin decision + error rates via `sp_force_register_decoupling` + `sp_direction_asymmetry` + `sp_joint_localization`, and the Δ's correct attribution (identifier failure vs. contested label) via `sp_label_indexicality` and confound-freedom via `sp_attacker_defender_confound` — nothing promised in Stage 1 falls off the chain by Stage 6.
5. **`study_type` consistency** — `empirical` throughout; Stage 6 correctly emits 0 outcome-tier RQs.

**What was hardest:** unlike a typical fresh idea, the recurring tension was **not** disagreement about facts (`paper.md`'s Steps 0/3/5/6/9 had already settled the substantive design) but making sure this schema's own discipline — verbatim hypothesis-to-RQ traceability, explicit sub-problem sourcing, tiered RQ accounting — surfaced something `paper.md`'s own format doesn't force. The two genuine findings that survived critique (the contested-label evaluability gap in Stage 1, and the R2-Guard mis-tie in Stage 4) are both cases where restating `paper.md` in this schema's stricter field discipline exposed a looseness the free-form spec had let slide.

**Total rounds:** 6 stages × 1 critic round + 1 refiner pass = 6 critic rounds, 6 refiner passes. No stage hit the round cap; no cross-stage backup was required.

---

## Post-review revision round (2026-07-05)

Revision pass over all review artifacts (`stage_review.md`, `taste_audit.md`, `pipeline.md`; no `design_review.md` exists for this topic). Every finding enumerated, its status checked against the current deliverables, and open items applied. Historical rounds above are unchanged.

1. `stage_review.md` → Stage 4 REVISE (spurious length/topic cues named in prose but never checked) → **already applied**: pre-registered KS/cosine corpus-validity verification present in `paper_draft.md` (Baselines paragraph), mirrored in `paper_draft.tex`, and backported into `paper.md` (B-alt "Corpus-validity verification"). No change needed this round.
2. `stage_review.md` → Phase A item 2 (reference-cache integrity: 9 N3 grounding papers absent from cache) → **already applied**: 9 `selected` records present in `reference_candidates.jsonl` (159 records total, 0 pending).
3. `stage_review.md` → Phase A item 2 residual (the 9 N3 records have `pdf_path`/`digest_path = null`; fetch PDFs + run `paper-digest` in a future harvest pass) → **rejected — moot for this pass**: fetching external PDFs is outside a static-document revision pass and no PDFs exist locally; already logged as a to-do in `pipeline.md`, which is the disposition Phase A itself pre-committed to.
4. `stage_review.md` → Phase A item 4 (B-alt missing pre-committed downgrade wording, per-claim scoping) → **already applied**: full both-failure-mode downgrade wording present in `paper.md` Step 6 B-alt.
5. `stage_review.md` → Phase A item 5 (A1–A6 missing explicit gates; missing thin-cell INCONCLUSIVE pre-declaration) → **already applied**: `*Gate:*` present on all six assumptions (PG-1/PG-2 in-skeleton, A3–A6 deferred to named scale-up phases); A6 carries the INCONCLUSIVE pre-declaration naming the depth-stratified cells and single-source subsets.
6. `stage_review.md` → Phase A item 6.1 (missing one-sentence estimand, R1) → **already applied**: `**Estimand**` sentence present in `paper.md` Step 5.
7. `stage_review.md` → Phase A item 6.6 (missing 5-step R2 instrument-validation plan for M1/M2) → **already applied**: full 5-step walkthrough for both instruments present in `paper.md` (Instrument validation block), with κ ≥ 0.7 acceptance criteria and the Part-4-situation-7 failure route.
8. `stage_review.md` → Phase A item 6.7 (KS/cosine verification stale — existed in draft but not in `paper.md`) → **already applied**: backport present in `paper.md` B-alt.
9. `taste_audit.md` → verdict 🟢, no conditions fired; the one soft note (`boilerplate = 1`, the "keeping governance constraints resident and enforced" clause) was explicitly scored below every flag threshold and carried no recommendation → **no action required** (nothing to apply; not counted as an open finding).
10. Cross-deliverable consistency sweep (this round) → **found & fixed**: `experiment_design.md`'s B-alt pre-committed downgrade wording said "the RQ1/RQ2/RQ3 (below) claims hold at full strength" — a mistranslation of `paper.md`'s claim family into the design doc's own 8-RQ numbering, since design-RQ1 is the validity-gate instrument check (`rq_rewrite_validity`), not a fragility claim, and the localization/adaptive and contested-fraction claims (design RQ5/RQ6/RQ7) were omitted. Changed in `experiment_design.md` to "the claims tested by RQ2/RQ3/RQ5/RQ6/RQ7 below (`paper.md`'s RQ1/RQ_INF_1/RQ_INF_2 claim family)". No hypothesis text was touched — target hypotheses remain verbatim Stage 5 → Stage 6 matches.

Verification of cross-deliverable invariants (this round): 8 RQs in both `paper_draft.md` and `experiment_design.md`; effect floor Δ̄ ≥ 0.10; n = 300 pairs/direction sized for ~8pp at power ≈ 0.8; Holm-corrected McNemar over 10 tests at α = 0.05; κ ≥ 0.7 (annotation and gate); Wilson-CI contested-fraction bound < 0.50; IoU ≥ 0.5; ≤ 20 adaptive queries/item; 50%-relative family-swap threshold; KS/cosine matching-validity test at α = 0.05 — all consistent across `paper.md`, `paper_draft.md`, and `experiment_design.md`. `paper_draft.md`/`.tex` prose required no changes this round, so no recompile was needed (`paper_draft.pdf` remains current).
