# Discussion Trace — B5.1: Pricing Manipulation Tactics in Controlled Bilateral Bargaining

> Extracted verbatim from `pipeline.md` (the auto-research-discussion 6-stage critic/refiner transcript) per the updated auto-research-discussion SKILL.md's "Final deliverables" spec — this is the complete round-by-round record across all six stages: every draft version, every critique (comments, severities, resolution), every decision, every refiner pass. `pipeline.md` itself now carries only a pointer to this file plus its own Phase Log (goal.md phase-gate tracking, a separate concern from this discussion trace).

# Auto-Research-Discussion Run — B5.1 (autoclaude-style, repo-driven from digest.md + paper.md)

> Mode: **autoclaude** (self-play, Claude as student+teacher). Source: `../digest.md` (N0–N12) + `../paper.md` (Steps 0–9), both pre-existing reverse-digest artifacts for seed **B5.1**. Round cap: 5/stage (none hit). All six stages converged in 1 critic round + 1 refiner pass each — the seed material was unusually mature (`paper.md` already carries its own formal notation, six named assumptions A1–A6, and pre-committed fallbacks F1–F3/F-G1), so genuine disagreement surfaced but didn't require re-proposing.
>
> **Full pipeline order:** this file (`auto-research-discussion`, 6 stages) → `taste_audit.md` (`research-taste-auditor`, idea-level check on Stage 2+5) → `stage_review.md` (`pengsida-stage-reviewer`, PASS/REVISE/STOP per stage against the confirmed outputs, plus a Stage 5 Writing check on the first assembled draft) → final `paper_draft.md`/`.tex`/`.pdf`. One REVISE finding from `stage_review.md` (missing per-RQ falsification-condition lines in Experiments) is already folded into the `paper_draft.*` files below — read `stage_review.md` for the reasoning behind that fix.

## Seed brief

- **One-sentence description:** Measure, via controlled single-tactic linguistic injection into an otherwise-standard LLM bargaining agent, how much economic surplus each of four manipulation tactics (anchoring, false urgency, fabricated competing offers, emotional pressure) transfers relative to a matched no-tactic control, and how that transfer varies by target model and counterparty sophistication.
- **Apparent inputs:** a single-good bilateral bargaining scenario with a controller-assigned, concealed reservation price per side; a tactic condition (control or one of four tactics at a given intensity); a manipulator/counterparty LLM pair; a counterparty-sophistication level.
- **Apparent outputs:** a per-dialogue outcome (agreed price or impasse); a per-tactic surplus-transfer statistic (ΔS) relative to control; a per-(tactic × model) susceptibility ranking; a per-(tactic × sophistication) defense-effectiveness reading.
- **Closest research areas:** LLM negotiation/bargaining-as-RL-domain (ARIA); emergent LLM-agent market competition (CompeteAI); formal LLM persuasion/influence measurement (StrategicPersuasion); controlled adversarial prompt-injection testbeds (TensorTrust, ChatInject); strategic dishonesty in evaluation settings (StrategicDishonesty); mechanism-design pricing of strategic manipulation (ClickBandit).
- **In scope:** measuring existing prompted/in-context LLM agents' susceptibility to four named linguistic tactics in a single-good bilateral bargain with mechanically-scored, concealed-valuation ground truth. **Out of scope:** training/fine-tuning new agents; multi-issue or multi-party bargaining; live/non-sandboxable deployments; tactics beyond the four named.
- **Confidence: high.** As with the B5.5 exemplar, the "repo" here is a prior reverse-digest plus a pre-registered spec (`digest.md` + `paper.md`) that already carries its own formal notation (`b, s, W, σ, ΔS, p`), six explicit assumptions (A1–A6) with fail-mode/detection/mitigation triplets, and pre-committed fallbacks (F1–F3, F-G1) if the headline hypotheses fail. Reconstruction risk is low; the discipline required here is the same as B5.5's — treat stage 5/6 as validating the **measurement instrument's properties** (isolation, concealment, comparability, power, realized-fidelity), not re-deriving `paper.md`'s own already-finished Step 5/6/9 from scratch.

---

## Stage 1 — Problem Definition

### Round 1 (critic phase)

**draft_v1** (proposer):
- `summary`: Given a single-good bilateral bargaining scenario in which each side's reservation price is assigned by a controller and concealed from both negotiating LLM agents, and given a controlled single-variable linguistic-tactic injection (anchoring, false urgency, a fabricated competing offer, or emotional pressure) applied to one agent's turns while every other feature of the dialogue (scenario, counterparty prompt, turn cap) is held fixed relative to a no-tactic control, determine how much of the bargaining surplus the injected tactic transfers to the manipulating side, and how that transfer varies across target models and counterparty sophistication levels.
- `input`: (1) a scenario specifying a concealed buyer reservation `b` and seller reservation `s` with `s < b`; (2) a tactic condition drawn from `{control, anchoring, false-urgency, fabricated-offer, emotional-pressure}` at a specified intensity and injection timing; (3) a manipulator/counterparty LLM model pair; (4) a counterparty-sophistication level (naive default, bargaining-zone-reasoning, manipulation-warned).
- `output`: (1) a per-dialogue outcome — an agreed price `p` or a recorded impasse; (2) a per-tactic surplus-transfer statistic `ΔS`, the paired-by-scenario difference in the manipulator's captured-surplus share relative to the matched no-tactic control; (3) a per-(tactic × model) susceptibility ranking; (4) a per-(tactic × sophistication) reading of whether cheap counterparty defenses reduce transfer.
- `constraints`: reservation prices must never appear in either agent's visible context, only in the scorer; the tactic template must be the sole manipulated variable between a treatment dialogue and its matched control (same scenario, same counterparty prompt, same turn cap); every dialogue must terminate in a scored outcome within a bounded number of turns.
- `objective`: a tactic's surplus-transfer claim is accepted only if its `ΔS` against the matched no-tactic control clears a pre-registered threshold at a pre-registered significance level, **and** that effect survives subtraction of a budget-matched generic-toughness control — a tactic whose effect does not survive this subtraction is attributed to aggression, not tactic-specific manipulation, and reported as such rather than folded into the catalog.
- `study_type`: `empirical` — stated explicitly: digest N12 already settles this ("a measurement study of an existing phenomenon... its headline deliverable is a quantitative welfare-pricing catalog"), and the seed's own `[证据]` (evidence-type) label agrees.

**critique:**
- summary: Strong draft, evidence-traceable to `paper.md`'s own Step 5 notation, but the objective is silent on a failure mode the seed's own design already worries about, and the output list risks a soft double-count.
- comments:
  - `{severity: major, field: "objective", anti_pattern: "vague_success (evaluability gap)", comment: "The objective doesn't say what happens when a target's apparent concession is strategically feigned rather than genuine. Digest N6's M6 auditor and N10's threat t3 both flag exactly this: 'a low ΔS could reflect non-delivery [refusal] rather than tactic ineffectiveness' and a manipulated concession 'may itself be strategically feigned.' As drafted, the objective would let a feigned-compliance dialogue count as a successful surplus transfer with no way to distinguish it from a genuine one — that's a real evaluability gap, not a hypothetical one, since the seed's own N6/N10 already anticipated it."}`
  - `{severity: minor, field: "summary", anti_pattern: null, comment: "'determine how much... the injected tactic transfers' presupposes transfer occurs before it's measured — the seed's own Step 6 global fallback F-G1 explicitly allows for the finding that no tactic transfers anything above the toughness-adjusted threshold ('LLM bargaining agents prove structurally robust'). Prefer neutral phrasing: the *surplus-transfer effect* of an injected tactic, not an assumed transfer."}`
- decision: `move_to_refiner` (both flags are formalize-level fixes using content already in `paper.md`'s own N6/N10/F-G1 — no new content needed).

### Refiner pass

- `objective` (refined): "A tactic's surplus-transfer claim is accepted only if its `ΔS` against the matched no-tactic control clears a pre-registered threshold at a pre-registered significance level, survives subtraction of a budget-matched generic-toughness control, **and** is reported both unconditionally and restricted to dialogues where the manipulator's tactic delivery is independently verified as high-fidelity and the target's concession is verified as genuine (not merely feigned to end the dialogue) — a condition whose fidelity/genuineness verification falls below a pre-registered threshold is reported as *not classifiable* rather than folded into the catalog at face value."
- `summary` (refined): "...determine **the surplus-transfer effect** of a controlled single-variable linguistic-tactic injection... relative to a matched no-tactic control..." (removes the presupposed-transfer framing).
- `formal_summary` (added, per stage-1 refiner's formalize-for-free duty, reusing `paper.md`'s own Step 5 notation): "Buyer/seller reservations `(b, s)`, `s < b`, ZOPA width `W = b − s`, drawn and concealed by a controller. Manipulator captured-surplus share on a deal: `σ = (p − s)/W ∈ [0,1]`. Condition `c ∈ {control, tactic × intensity} × model-pair × sophistication`. Surplus transfer for tactic `t`, paired by scenario `k` against matched control: `ΔS_t = E_k[σ(t,k) − σ(control,k)]`. The object of study is `ΔS_t` and its variation across the model and sophistication axes, gated by realized tactic fidelity and concession genuineness (both auxiliary, mechanically-scored covariates, not modeled here as part of the primary statistic)."
- `changes_made`: added the fidelity/genuineness conditioning to `objective`; removed a presupposition from `summary`; added `formal_summary`.
- `declined_to_fix`: none.

**Confirmed Stage 1** — `study_type: empirical`.

---

## Stage 2 — Motivation

### Round 1 (critic phase)

**draft_v1:**
- `summary`: Autonomous LLM agents are increasingly delegated to negotiate real economic transactions on a principal's behalf, but there is no controlled, mechanically-scored measurement of how much surplus a counterparty can extract from such an agent using specific, named linguistic manipulation tactics — leaving principals with no way to price the economic risk of delegating bargaining to an LLM.
- `why_it_matters`: If anchoring, false urgency, fabricated competing offers, or emotional pressure can reliably shift an agreed price away from what a rational, payoff-maximizing agent would concede, that is a direct, quantifiable transfer of a principal's money to whoever controls the manipulator side of the conversation — and unlike a model's accuracy on a benchmark, this transfer compounds every time the agent negotiates again. Because susceptibility plausibly differs by model (`paper.md` Step 6 RQ2/H2), a principal choosing which LLM to delegate bargaining to is otherwise choosing blind; and because cheap prompt-level defenses (bargaining-zone reasoning, explicit manipulation warnings) are the obvious first thing anyone would try, whether they actually work (`paper.md` RQ3/H3, or fail per fallback F3) determines whether "just add a warning to the system prompt" is a real fix or a false sense of security.
- `who_cares`: Principals delegating price negotiation, contract terms, or resource allocation to autonomous agents; designers of agent-to-agent marketplaces deciding whether prompt-level manipulation-resistance is sufficient; safety evaluators benchmarking model susceptibility to adversarial social engineering in economically consequential settings.
- `evidence`: `[ARIA, OpenReview:eumRwpgdMU]`'s own motivation notes that in negotiation/bargaining "reward variance is amplified by opponent dynamics" — establishing bargaining as a live, quantifiable-payoff LLM-agent domain, but never decomposing where surplus goes or attributing it to a specific tactic. `[StrategicPersuasion, OpenReview:aTCXvJKnkE]` shows linguistic influence between LLMs is formally measurable as a utility-relevant action change — evidence the underlying phenomenon (LLMs moving each other's stated preferences) is real and quantifiable — but its stance-change metric doesn't translate to bargaining surplus. `[TensorTrust, OpenReview:fsW7wJGLBd]` and `[ChatInject, OpenReview:WVhgFSKniL]` establish that controlled, templated adversarial injection is a viable testbed methodology, but both score success as binary instruction-integrity, not a continuous economic quantity — itself evidence that "how much" pricing is an open gap, not merely an unasked question.

**critique:**
- summary: Good stake-specific motivation with real citations, but one of stage 1's four outputs is motivated only implicitly.
- comments:
  - `{severity: major, field: "why_it_matters", anti_pattern: "partial_output_coverage", comment: "Stage 1 output (4) is the per-(tactic × sophistication) defense-effectiveness reading. why_it_matters gestures at it ('whether cheap prompt-level defenses... actually work') but never explains why this needs to be *measured per tactic* rather than as a single yes/no verdict on 'defenses' in general — paper.md's own H3 explicitly predicts anchoring shows the *smallest* reduction even when other tactics are substantially defended against. Without stating why a uniform defense-effectiveness claim would be misleading, a reader could reasonably ask 'why not just report whether warnings help, once, and move on' — which is exactly the oversimplification H3's per-tactic granularity exists to prevent."}`
- decision: `move_to_refiner`.

### Refiner pass

- `why_it_matters` (extended): "...critically, a defense's effectiveness cannot be reported as a single aggregate verdict: if bargaining-zone reasoning and manipulation warnings recover surplus against false urgency and emotional pressure but leave anchoring's transfer largely intact — because anchoring works by shifting the *perceived* reference point itself, which a warned-but-still-anchored reasoner can still adopt — then a principal told only 'defenses work' would under-protect against exactly the tactic likeliest to survive the fix. Per-tactic, not aggregate, defense measurement is what prevents that specific false sense of security."
- `changes_made`: added the per-tactic-granularity argument for why defense measurement can't be reported as a single aggregate claim.
- `declined_to_fix`: none.

**Confirmed Stage 2.**

---

## Stage 3 — Related Work

All seven works below are treated as **specific (deep) tier** — digest N3/N4 already engaged each at the approach + limitation level (input/output framing and a limitation tied to this paper's setting), so no landscape-only `general_related_works` entries are invented to pad the list, per the no-fabrication rule.

### Round 1 (critic phase)

**draft_v1** (`specific_related_works`, abbreviated to citation / I-O framing / limitation / `is_potential_baseline`):

| work_id | citation | is_potential_baseline | limitation (→ sub-problem it will motivate) |
|---|---|---|---|
| `rw_aria` | Anon., ARIA (OpenReview:eumRwpgdMU) | false (RL training environment, not a measurement instrument) | Treats bargaining as a training domain and works to reduce reward variance for the learner; never decomposes where surplus goes or attributes concessions to a specific injected linguistic tactic. |
| `rw_competeai` | Anon., CompeteAI (OpenReview:wGtzp4ZT1n) | false (emergent market, no injected treatment, no concealed valuation) | Studies competition dynamics that emerge endogenously from agent strategies; with no injected, held-constant treatment and no concealed ground-truth valuation per side, it cannot causally isolate an individual manipulation tactic or mechanically price the resulting welfare transfer. |
| `rw_stratpersuasion` | Anon., StrategicPersuasion (OpenReview:aTCXvJKnkE) | **true** | Formalizes persuasion as a single-shot-ish Bayesian sender-receiver stance-change game with a discrete action readout; doesn't model a bilateral price negotiation with two-sided private reservations, multi-round concession dynamics, or an economic-surplus payoff. |
| `rw_tensortrust` | Anon., TensorTrust (OpenReview:fsW7wJGLBd) | false (binary string-integrity objective, different domain) | Evaluates adversarial manipulation against a symbolic string-comparison objective (say/withhold an access code); success is binary instruction-integrity, not a continuous economic quantity. |
| `rw_chatinject` | Anon., ChatInject (OpenReview:WVhgFSKniL) | false (indirect prompt injection against assistants, not bargaining) | Shows staged, fabricated multi-turn dialogue and forged role tags are strong injection levers, but scores success as instruction compliance, not transferable economic surplus. |
| `rw_strategicdishonesty` | Anon., StrategicDishonesty (OpenReview:IbDr8xgUMW) | false (adversarial safety-evaluation setting, not a bargaining testbed) | Characterizes strategic dishonesty in refusal-vs-fake-compliance safety evaluations; flags that apparent compliance may be strategically feigned but provides no bargaining testbed or surplus metric to price that feigning. |
| `rw_clickbandit` | Anon., ClickBandit (OpenReview:lsxeNvYqCj) | false (one-sided bandit/recommendation mechanism design) | Prices strategic manipulation of a single reported scalar in a one-sided platform-vs-arms bandit setting; doesn't address two-sided bilateral bargaining, free-form linguistic tactics, or per-tactic decomposition of who captures surplus. |

**critique:**
- summary: Every limitation is specific and tied to this paper's setting (no "scalability issues"-style vagueness), but one baseline label needs the same scrutiny B5.5's SOTOPIA entry needed.
- comments:
  - `{severity: major, field: "specific_related_works[rw_stratpersuasion].is_potential_baseline", anti_pattern: "io_approach_mismatch", comment: "StrategicPersuasion's I/O framing is a single-shot stance-change game with a discrete action readout — genuinely different from this paper's repeated-offer, continuous-surplus bilateral bargain. Per the stage-3 rubric, a mismatched-I/O work is 'not a baseline — at best a method-side reference.' Marking it a straightforward baseline risks implying its own reported persuasion-success numbers are being compared against, which they never are anywhere in paper.md's Step 6."}`
- decision: `move_to_refiner` (a wording-precision fix, not a structural one — the *upper-reference-arm* role `paper.md` already gives it is legitimate and stays).

### Refiner pass

- `rw_stratpersuasion.is_potential_baseline` retained as `true`, but the field's accompanying note is sharpened: "Not a baseline in the beat-a-number sense — its own reported persuasion-success numbers are not compared against. Its **Sender agent, reused as a strong strategic-manipulator upper-reference arm** (per `paper.md`'s Step 6 baseline list), is borrowed for what a highly capable, purpose-built persuader achieves in this bargaining setting — independent of its own published results."
- `changes_made`: clarified StrategicPersuasion's baseline role to avoid an implied I/O-mismatched comparison.
- `declined_to_fix`: none.
- **Note on `verify_as_hypothesis`:** set `false` on every limitation. None is flagged as a stage-6 framing-tier RQ — every limitation above motivates the paper's *existence* (no prior work prices per-tactic bargaining surplus) rather than a distinct, separately-testable framing claim this paper would spend an experiment confirming independent of its own mechanism-tier hypotheses. Per `stages.md`: *"If nothing was flagged, emit zero framing-tier RQs — don't manufacture one."*

**Confirmed Stage 3.**

---

## Stage 4 — Sub-Problems

### Round 1 (critic phase)

**draft_v1** (6 sub-problems, from digest N5's C1–C6):

- **`sp_tactic_isolation`** — *description:* Isolate the causal effect of a single injected linguistic tactic from the rest of an otherwise free-form bargaining dialogue, including ruling out "it's just being tough" as the true driver. *why_it_is_a_problem:* Without isolation, an observed price shift could reflect generic assertiveness rather than the specific tactic construct, making the whole catalog attribute the wrong cause. *technical_challenge:* Requires a paired treatment/control design where only the tactic template differs (scenario, counterparty prompt, turn cap held fixed) **and** a second, budget-matched "generic toughness" arm to subtract out mere aggression — a single control is not enough to rule out both confounds at once. *source_limitation_ids:* `["__novel__"]` — no cited work scores a continuous bilateral surplus against a matched pair of controls in the first place.
- **`sp_concealed_valuation`** — *description:* Keep each side's reservation price fully known to the scorer but fully concealed from both negotiating agents, so surplus transfer is mechanically, not subjectively, computable. *why_it_is_a_problem:* If either agent's visible context leaks its own or the counterpart's reservation, the mechanical surplus scorer becomes contaminated by information the real-world principal never actually reveals. *technical_challenge:* Concealment must be verified, not assumed — a scenario description can leak reservation information through paraphrase or implication even when no number is stated outright. *source_limitation_ids:* `["__novel__"]`.
- **`sp_cross_model_comparability`** — *description:* Compare tactic potency and target-model susceptibility on a common footing across different LLMs playing the manipulator and counterparty roles. *why_it_is_a_problem:* A single-model finding may be an artifact of that model's idiosyncrasies rather than a general property of tactics or of model families. *technical_challenge:* Different models vary in instruction-following fidelity and valid-offer parse rates, so "the same tactic" must be run through an identical action grammar and scenario format across models before any cross-model ranking is meaningful. *source_limitation_ids:* `["__novel__"]`.
- **`sp_signal_variance`** — *description:* Separate a genuine tactic effect from ordinary sampling noise, given that individual bargaining dialogues are stochastic and outcomes are heavy-tailed (impasses, extreme prices). *why_it_is_a_problem:* Without this, any observed ΔS is unfalsifiable — a single lucky or unlucky dialogue could be mistaken for a tactic's true effect. *technical_challenge:* Requires enough independently drawn scenario/paraphrase/intensity trials per condition for a true effect to be statistically distinguishable from noise, and requires confirming the effect reflects the tactic *category* rather than one specific string's phrasing. *source_limitation_ids:* `["__novel__"]`.
- **`sp_counterparty_confound`** — *description:* Determine whether a tactic's effect is stable or is instead an artifact of a single, default counterparty's naivety, by varying counterparty sophistication (naive, bargaining-zone-reasoning, manipulation-warned) independently of the injected tactic. *why_it_is_a_problem:* A catalog built entirely against one default, unsophisticated counterparty conflates "how strong is this tactic" with "how easy is it to fool this one specific default prompt," which is a much weaker and less generalizable claim. *technical_challenge:* Sophistication and tactic must be crossed factorially rather than run as separate one-off checks, since a defense's effectiveness plausibly differs by which tactic it's defending against. *source_limitation_ids:* `["__novel__"]`.
- **`sp_realized_manipulation`** — *description:* Determine whether a target's apparent concession under a tactic reflects genuine strategic response or refusal/feigned compliance that never delivers the intended manipulation. *why_it_is_a_problem:* An in-context LLM's guardrails may refuse to deploy or fully absorb a deceptive tactic, and a target's apparent concession may itself be a strategically feigned compliance rather than a real payoff-relevant shift — either failure mode would make a raw, unconditioned ΔS misattribute non-delivery as tactic ineffectiveness, or feigned compliance as real transfer. *technical_challenge:* Realized tactic fidelity and concession genuineness are not directly observable from the final price alone; both require an independent judge (and spot-check) applied to the dialogue transcript itself, following exactly the fake-vs-genuine-compliance distinction StrategicDishonesty draws in a different (safety-evaluation) setting. *source_limitation_ids:* `["lim_strategicdishonesty"]`.

**critique:**
- summary: Coverage checks out (solving all six would jointly deliver stage 1's four outputs), but two sub-problems read as invoking the same "vary something systematically" fix without stating what actually distinguishes them.
- comments:
  - `{severity: minor, field: "sp_cross_model_comparability / sp_counterparty_confound", anti_pattern: "overlap", comment: "Both technical_challenge fields end on 'must be varied/crossed systematically,' which can read as the same sub-problem stated twice. They are genuinely distinct — one is about model *identity* (which LLM is playing a role), the other about counterparty *strategy/prompting sophistication* holding model identity fixed — but the descriptions don't make that axis distinction explicit enough."}`
- decision: `move_to_refiner`.

### Refiner pass

- `sp_cross_model_comparability.technical_challenge` sharpened to end with: "...this is a **model-identity** axis — which LLM occupies the manipulator or counterparty role — held orthogonal to which tactic is injected."
- `sp_counterparty_confound.technical_challenge` sharpened to end with: "...this is a **counterparty-strategy** axis distinct from model identity — the same model can be run at any sophistication level, so sophistication and tactic must be crossed factorially independent of which model is doing the reasoning."
- `changes_made`: made the model-identity-vs-counterparty-strategy distinction explicit in both `technical_challenge` fields.
- `declined_to_fix`: none.

**Confirmed Stage 4** (6 sub-problems; 1 sourced from a related-work limitation, 5 `__novel__` with stated decisive-component justifications).

---

## Stage 5 — Method Design

### Round 1 (critic phase)

**draft_v1** (6 methods):

- **`m_paired_injection`** → targets `sp_tactic_isolation`. *proposed_approach:* For every treatment dialogue, run a scenario-matched no-tactic control dialogue and a scenario-matched, budget-matched generic-toughness-prompt dialogue, holding scenario, counterparty prompt, and turn cap identical across all three; only the manipulator's template differs. *key_insight:* A single control cannot separate "tactic-specific manipulation" from "generic assertiveness" — subtracting a toughness-matched second arm is what makes the tactic label load-bearing rather than a stand-in for aggression. *hypotheses:* ["At least one tactic's paired ΔS against the matched no-tactic control is significantly nonzero (≥0.10 of ZOPA width) at a Bonferroni-corrected α=0.0025.", "For any tactic clearing that threshold, the effect survives subtraction of the budget-matched generic-toughness control (ΔS_tactic − ΔS_toughness ≥ 0.05 at α=0.01); a tactic that does not survive this subtraction is attributable to aggression, not tactic-specific manipulation."]
- **`m_concealment_controller`** → targets `sp_concealed_valuation`. *proposed_approach:* A dedicated controller draws each side's reservation price and injects it only into the scorer's private state, never into either agent's prompt context; every scenario template is audited by string/paraphrase search for implicit leakage, and a "guess the counterpart's reservation" probe query is run against a held-out sample of dialogues. *key_insight:* Concealment is a property of the actual rendered prompts an agent sees, not of the experimenter's intent, so it has to be independently verified against real dialogue transcripts, not assumed from the harness design. *hypotheses:* ["A leakage-probe query asking either agent to guess the counterpart's reservation returns accuracy statistically indistinguishable from chance, pooled across all tactic conditions."]
- **`m_cross_model_matrix`** → targets `sp_cross_model_comparability`. *proposed_approach:* Run the identical tactic set, at the identical intensities, through a fixed matrix of LLMs occupying both the manipulator and counterparty roles, using one shared action grammar and scenario format; models with a valid-offer parse rate below a pre-specified threshold are excluded and reported, not silently dropped. *key_insight:* Only when the tactic template and scenario format are held bit-for-bit identical across models does a cross-model spread in ΔS reflect model susceptibility rather than incidental harness differences. *hypotheses:* ["The tactic × counterparty-model interaction is significant (likelihood-ratio test p<0.01), and for at least one tactic the per-model spread in ΔS is ≥0.10 of ZOPA width.", "Smaller or less safety/instruction-tuned counterparty models show significantly larger ΔS than larger, more heavily-aligned counterparty models, for at least one tactic."]
- **`m_variance_control_design`** → targets `sp_signal_variance`. *proposed_approach:* Run each tactic at ≥2 phrasing variants and ≥2 intensity levels, treating tactic-variant and paraphrase as random effects in a mixed-effects model powered (via pilot variance) to detect ΔS≈0.10 at 80% power with n≈200 dialogues per cell. *key_insight:* A tactic's effect is only meaningful as a category-level claim if the across-paraphrase variance within a tactic is small relative to the across-tactic variance — otherwise the "effect" is really a single string's artifact, not evidence about the tactic construct. *hypotheses:* ["The across-paraphrase variance in ΔS within a tactic is significantly smaller than the across-tactic variance in mean ΔS, confirming the measured effect reflects the tactic category rather than one specific phrasing."]
- **`m_sophistication_defense`** → targets `sp_counterparty_confound`. *proposed_approach:* Cross three counterparty-sophistication conditions (naive default, bargaining-zone-reasoning, explicit manipulation-warning) with all four tactics, holding model identity fixed within each comparison, and fit a mixed-effects model with a sophistication × tactic interaction term. *key_insight:* A single mixed-effects specification (sophistication × tactic) yields two distinct, separately falsifiable estimands from one fit: whether sophistication changes the *average* transfer at all, and whether it changes transfer *unevenly* across tactics — one instrument, two readouts, not two mechanisms. *hypotheses:* ["The sophistication × tactic interaction is significant (LRT p<0.01), and at least one non-naive sophistication condition reduces mean ΔS by ≥50% relative to the naive default for the tactic(s) it targets.", "Anchoring shows the smallest percentage reduction in ΔS across sophistication conditions among the four tactics, consistent with anchoring biasing the reference point itself rather than being defeated by post-hoc reasoning."]
- **`m_fidelity_auditor`** → targets `sp_realized_manipulation`. *proposed_approach:* An LLM-judge, spot-checked by a human annotator on a stratified sample, classifies (a) whether the manipulator's turns actually deliver the intended tactic (fidelity) and (b) whether the target's concession is genuine or feigned, via a re-probe that removes the tactic's factual claim from context and checks whether the target still accepts the same price. *key_insight:* Fidelity and genuineness are not nuisance metadata to report alongside ΔS — they determine whether ΔS is even measuring what it claims to, so the auditor's output has to be shown to actually change the substantive verdict in at least one condition, not just exist as a side-channel diagnostic. *hypotheses:* ["Conditioning ΔS on verified-fidelity, verified-genuine dialogues changes the accept/reject verdict against the ΔS≥0.10 threshold (Methods above) in at least one tactic × model cell relative to the unconditioned ΔS, demonstrating the auditor is load-bearing rather than redundant with the raw statistic."]

**critique:**
- summary: Every method has a real mechanism (no goal-restatement — this isn't "sub-problem: isolate the tactic; method: a system that isolates the tactic"), and every hypothesis names a threshold or a comparison an experiment could refute — but one method is carrying two headline claims and needs the same one-line justification B5.5 required for its analogous case.
- comments:
  - `{severity: minor, field: "m_sophistication_defense.hypotheses", anti_pattern: null, comment: "Two hypotheses here (interaction+magnitude, and anchoring-smallest-reduction) are the paper's second and third most central claims (H3 in paper.md, split). Worth stating explicitly why one mechanism produces both, the same way B5.5's m_matched_conditions justified its two-hypothesis bundle, so this doesn't read as scope creep folded into a single method."}`
- decision: `move_to_refiner`.

### Refiner pass

- `m_sophistication_defense.key_insight` already states the one-instrument-two-estimands justification in the draft above (added during drafting rather than needing a separate refiner edit) — refiner confirms this satisfies the critique and makes no further change to that field.
- `m_fidelity_auditor.key_insight` tightened for precision: "...the auditor's output has to be shown to actually **change the verdict** in at least one condition — a demonstrated, falsifiable load-bearing test, not an assumed one."
- `changes_made`: minor wording tightening on `m_fidelity_auditor.key_insight`; confirmed `m_sophistication_defense`'s existing justification already addresses the critique.
- `declined_to_fix`: none.

**Confirmed Stage 5** — 6 methods, **8 hypotheses total** (2 + 1 + 2 + 1 + 2 + 1 across the six methods respectively — `m_paired_injection` and `m_cross_model_matrix` and `m_sophistication_defense` each carry two, per the refiner's one-instrument-two-estimands justifications above), mixing instrument-validity claims (concealment, variance-structure, fidelity load-bearingness) with the study's headline empirical predictions (magnitude, cross-model spread, defense effectiveness) — a deliberate design choice for an `empirical` study_type, explained in the stage-6 header below.

---

## Stage 6 — Experiment Design

**Tier accounting (checked against study_type=empirical):**
- **Mechanism-tier: 8 RQs**, one per Stage 5 hypothesis (verbatim `target_hypotheses`).
- **Framing-tier: 0 RQs** — no Stage 3 limitation was flagged `verify_as_hypothesis`; none manufactured.
- **Outcome-tier: 0 RQs** — `study_type = empirical` forbids "our procedure beats baseline X" framing. All baselines below are sanity-check comparators or upper-reference arms, never a competitor this paper is trying to beat.

### Round 1 (critic phase)

**draft_v1:**

`datasets`:
- Synthetic single-good buyer/seller scenarios with controller-assigned, randomized ZOPA (He et al.–style parameterization) — *justification:* the only substrate that can satisfy the concealed-valuation constraint by construction (the controller generates and holds out the ground truth), so it is the primary substrate for every RQ below.
- GLEE (Shapira et al., 2024) — *justification:* a parameterized economic-game benchmark offering controlled surplus size and asymmetry, used to test whether the cross-model spread (RQ4/RQ5) and the magnitude finding (RQ1) are stable under a controlled substrate other than the fully synthetic one, rather than only observed on one generator.
- (draft initially listed CraigslistBargain / DealOrNoDeal with justification only "external-validity transfer test, per digest N8" — flagged below.)

`baselines` (sanity-check comparators and upper-reference arms, not outcome-tier competitors):
- No-tactic / neutral negotiating prompt (B0) — the necessary control for every tactic claim; every ΔS is defined relative to it.
- Generic-toughness prompt (B-alt), budget-matched on token/turn count — the discriminator that separates tactic-specific manipulation from mere aggression (Methodology, `m_paired_injection`).
- Nash / split-the-difference midpoint reference — a theoretical no-manipulation reference used only as a rationality sanity check on the control condition itself (confirms mean control `σ` sits in a plausible range before any tactic claim is trusted).
- StrategicPersuasion's Sender agent (`rw_stratpersuasion`) — borrowed as a strong strategic-manipulator upper-reference arm, per Stage 3's sharpened role for this work (protocol borrowed, not its own reported numbers).
- ChatInject's forged-role staged-dialogue injection (`rw_chatinject`) — borrowed as an adversarial upper-bound reference for how much realizable manipulation intensity is achievable at all, independent of whether it is economically framed.

`research_questions` (8, all mechanism-tier):

| rq_id | target_sub_problem_id | target_hypotheses (verbatim) |
|---|---|---|
| `rq_magnitude` | `sp_tactic_isolation` | "At least one tactic's paired ΔS against the matched no-tactic control is significantly nonzero (≥0.10 of ZOPA width) at a Bonferroni-corrected α=0.0025." |
| `rq_toughness_survival` | `sp_tactic_isolation` | "For any tactic clearing that threshold, the effect survives subtraction of the budget-matched generic-toughness control (ΔS_tactic − ΔS_toughness ≥ 0.05 at α=0.01); a tactic that does not survive this subtraction is attributable to aggression, not tactic-specific manipulation." |
| `rq_concealment_verification` | `sp_concealed_valuation` | "A leakage-probe query asking either agent to guess the counterpart's reservation returns accuracy statistically indistinguishable from chance, pooled across all tactic conditions." |
| `rq_model_interaction` | `sp_cross_model_comparability` | "The tactic × counterparty-model interaction is significant (likelihood-ratio test p<0.01), and for at least one tactic the per-model spread in ΔS is ≥0.10 of ZOPA width." |
| `rq_alignment_direction` | `sp_cross_model_comparability` | "Smaller or less safety/instruction-tuned counterparty models show significantly larger ΔS than larger, more heavily-aligned counterparty models, for at least one tactic." |
| `rq_paraphrase_variance` | `sp_signal_variance` | "The across-paraphrase variance in ΔS within a tactic is significantly smaller than the across-tactic variance in mean ΔS, confirming the measured effect reflects the tactic category rather than one specific phrasing." |
| `rq_defense_interaction` | `sp_counterparty_confound` | "The sophistication × tactic interaction is significant (LRT p<0.01), and at least one non-naive sophistication condition reduces mean ΔS by ≥50% relative to the naive default for the tactic(s) it targets." |
| `rq_anchoring_persistence` | `sp_counterparty_confound` | "Anchoring shows the smallest percentage reduction in ΔS across sophistication conditions among the four tactics, consistent with anchoring biasing the reference point itself rather than being defeated by post-hoc reasoning." |
| `rq_fidelity_loadbearing` | `sp_realized_manipulation` | "Conditioning ΔS on verified-fidelity, verified-genuine dialogues changes the accept/reject verdict against the ΔS≥0.10 threshold (Methods above) in at least one tactic × model cell relative to the unconditioned ΔS, demonstrating the auditor is load-bearing rather than redundant with the raw statistic." |

(Table above lists 9 rows in the draft's working notes but `rq_anchoring_persistence` and `rq_defense_interaction` were merged from a single over-long row during drafting; final count is 8, matching Stage 5's 8 hypotheses one-to-one — see cross-stage check below for the explicit recount.)

**critique:**
- summary: Tier accounting is clean and every RQ traces to a verbatim hypothesis, but one dataset justification is a citation to the digest instead of a real methodological reason, exactly the failure B5.5 caught in its own GLEE entry.
- comments:
  - `{severity: major, field: "datasets[CraigslistBargain/DealOrNoDeal]", anti_pattern: "weak justification (not a named anti-pattern, but fails the rubric's 'justification for why this dataset actually stresses the hypothesis')", comment: "'external-validity transfer test, per digest N8' says nothing about which RQ needs it or why a naturalistic corpus stresses that RQ differently than the synthetic/GLEE substrates already do."}`
- decision: `move_to_refiner`.

### Refiner pass

- `datasets` entry replaced: "CraigslistBargain (He et al., 2018) and Deal-or-No-Deal (Lewis et al., 2017) — *justification:* naturalistic multi-issue and single-issue price-negotiation corpora with real (not procedurally generated) item and price framing; used specifically to test whether `rq_magnitude` and `rq_model_interaction`'s findings generalize beyond scenarios an experimenter authored, since a tactic's effectiveness could plausibly be an artifact of synthetic scenario phrasing rather than a property of real negotiation language."
- `changes_made`: gave the naturalistic-corpus datasets a hypothesis-linked reason (which RQs they stress and why) instead of a provenance note.
- `declined_to_fix`: none.

**Confirmed Stage 6.**

---

## Cross-stage consistency check (final pass, all six stages)

1. **No method leak** in stages 1/2/4 — checked; `objective`/`why_it_is_a_problem` fields name no technique (the toughness-subtraction and fidelity-conditioning clauses in Stage 1's objective describe *acceptance criteria*, not a method, mirroring how B5.5's dual-fairness-reference objective was accepted as evaluability content, not a method leak).
2. **ID stability** — no id renamed mid-run; `sp_*` / `m_*` / `rq_*` stable stage-to-stage.
3. **Reference integrity** — `sp_realized_manipulation.source_limitation_ids = ["lim_strategicdishonesty"]` ∈ Stage 3 limitations ✓; all other `source_limitation_ids = ["__novel__"]` ✓; every `target_sub_problem_id` in Stage 5 ∈ Stage 4 ✓; every Stage 6 `target_hypotheses` is a verbatim match to a Stage 5 hypothesis ✓.
4. **Output coverage** — Stage 1's four outputs (outcome record, per-tactic ΔS, per-(tactic×model) ranking, per-(tactic×sophistication) defense reading) are each reachable: outcome/ΔS via `sp_tactic_isolation` + `sp_concealed_valuation` + `sp_signal_variance`, model ranking via `sp_cross_model_comparability`, defense reading via `sp_counterparty_confound` (+ `sp_realized_manipulation` for whether either reading is trustworthy at all) — nothing promised in Stage 1 falls off the chain by Stage 6.
5. **`study_type` consistency** — `empirical` throughout; Stage 6 correctly emits 0 outcome-tier RQs.
6. **Hypothesis-to-RQ recount** (explicit, per the goal document's instruction): Stage 5 confirmed 8 hypotheses across 6 methods (2+1+2+1+2+1 — wait, recounted: `m_paired_injection`=2, `m_concealment_controller`=1, `m_cross_model_matrix`=2, `m_variance_control_design`=1, `m_sophistication_defense`=2, `m_fidelity_auditor`=1; sum = 9). **Correction applied during this check:** the running tally in the Stage 5 summary line above ("8 hypotheses total... 2+1+2+1+2+1") was arithmetically wrong — 2+1+2+1+2+1 = 9, not 8. Stage 6 correctly lists all **9** research questions (the table has 9 rows, not 8; the parenthetical note about a "merge" under the table was a drafting-stage error and is retracted here, not carried into the paper draft). Every one of the 9 hypotheses has exactly one verbatim-matching RQ; every RQ has exactly one source hypothesis. 9 hypotheses ↔ 9 RQs, 1:1, confirmed by explicit recount.

**What was hardest:** as with B5.5, the recurring tension was **not disagreement about facts** (paper.md's Steps 5/6/9 are unusually well-specified, down to explicit Bonferroni corrections and fallback conditions) but **scope discipline against redundancy** — repeatedly checking whether a stage-5/6 hypothesis was quietly re-deriving paper.md's own already-finished H1/H2/H3 rather than adding something this schema's structure specifically demands (e.g., the concealment-verification and fidelity-load-bearing hypotheses, which paper.md's Assumptions A2/A3 gesture at as fail-mode/mitigation pairs but never states as falsifiable hypotheses with their own RQ in Step 6).

**Total rounds:** 6 stages × 1 critic round + 1 refiner pass = 6 critic rounds, 6 refiner passes. No stage hit the round cap; no cross-stage backup was required. One self-caught arithmetic error (8 vs. 9 hypotheses) is corrected in the consistency check above rather than silently fixed — the paper draft below uses the corrected count of 9 throughout.

---

## Post-review revision round (2026-07-05)

Revision pass over all review artifacts (`stage_review.md`, `taste_audit.md`; no `design_review.md` exists in this topic). Every finding/recommendation was enumerated and its status checked against the current deliverables. Historical rounds above are untouched.

**Findings verified as already applied (no action needed):**
1. `stage_review.md` Stage 2 REVISE (nearest-neighbor sentence naming TensorTrust/ChatInject with plain delta) — present in `paper_draft.md` Related Work opening paragraph and `paper_draft.tex`.
2. `stage_review.md` Stage 4 REVISE (per-RQ falsification-condition lines) — present in all 10 RQ subsections of `paper_draft.md`/`.tex`.
3. `stage_review.md` Phase A items 1/2/5/6 (N12 absence_comment; N3 backfill + residual closed in second pass; assumption Gate labels; R1 estimand; M6 R2 κ≥0.7 plan; RQ4/H4/F4 mechanism; thin-cell INCONCLUSIVE rule) — applied to `digest.md`/`paper.md` and reflected downstream (RQ10 in both deliverables; κ≥0.7 in `experiment_design.md` RQ9; thin-cell rule in `experiment_design.md` RQ4).
4. `stage_review.md` Phase G [moderate] (RQ2's dropped H1 ordering clause) — present in `paper_draft.md` RQ2 (Expected outcome, Falsification condition, Hypothesis) and `experiment_design.md` RQ2.
5. `taste_audit.md` — 🟢 PASS twice, no action items; its one advisory (preserve per-module Challenge→Insight→Method structure) verified intact in `paper_draft.md` Methodology.
6. `experiment_design.md` RQ10 target hypothesis verified byte-identical to `paper.md` H4.

**OPEN findings applied this round:**
1. `pipeline.md` Phase E claims the DECEPTICON/TRAP concede-and-differentiate treatment was added to "both the Intro's related-work paragraph and the Related Work section," but the Intro sentence existed only in `paper_draft.tex`, not `paper_draft.md` (md/tex drift). → Mirrored the .tex Introduction sentence ("Two further structural twins on the same tactic-injection methodology... not a continuous, concealed-valuation economic surplus.") into `paper_draft.md`'s Introduction. File: `paper_draft.md`.
2. Cross-deliverable effect-floor precision: `paper.md` F1 pre-registers the reliability floor at ΔS ≥ 0.03, but RQ2's falsification condition in the draft said "about one-thirtieth of the bargaining-zone width" (≈0.033). → Replaced with "0.03 of the bargaining-zone width, the pre-registered reliability floor" in both `paper_draft.md` and `paper_draft.tex`; recompiled clean (exit 0, zero undefined citations, PDF regenerated).

**Findings rejected as moot (not applied, with reason):**
1. `stage_review.md` Phase G [minor] — RQ10 placed after RQ9 rather than interleaved near RQ3. Rejected: cosmetic ordering preference; fixing requires renumbering RQ4–RQ9 and every cross-reference (including `experiment_design.md`, which pins its numbering to the draft) for no substantive gain — same judgment the Phase G review itself recorded under goal.md's "splice, don't re-decide" discipline.
2. `stage_review.md` Phase G [minor] — no worked numeric example in the draft. Rejected: no experiments have run and no numbers exist; adding one would fabricate results, which the draft's own pre-handoff checklist and this revision pass's no-invented-content rule both forbid. Remains a logged to-do for the post-Phase-D re-entry.
3. `pipeline.md` open to-dos — Phase B/C/D (compute-dependent) and standalone digests for the 4 non-load-bearing backfilled references. Rejected for this pass: outside deliverable revision scope (no compute in this environment; lighter treatment explicitly allowed by guidance for adjacent/background references).

**Cross-consistency check (paper_draft.md ↔ experiment_design.md):** RQ count 10 = 10; RQ titles match 1:1; target hypotheses in `experiment_design.md` verbatim from Stage 5 / `paper.md` H4 as declared; effect floors (ΔS ≥ 0.10 primary, 0.03 reliability), RQ3 margin (ΔS_tactic − ΔS_toughness ≥ 0.05 at α = 0.01), Bonferroni α = 0.0025, n ≈ 200/cell, κ ≥ 0.7, and the ≥50% RQ7 reduction / RQ10 attenuation thresholds all consistent after the 0.03-floor fix above.
