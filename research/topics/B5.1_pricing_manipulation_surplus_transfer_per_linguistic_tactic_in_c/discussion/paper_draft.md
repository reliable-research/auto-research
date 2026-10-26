# Payoff-Irrelevant Words, Payoff-Relevant Prices: Pricing Linguistic Manipulation Tactics in LLM Bilateral Bargaining

> Assembled from the six confirmed stage outputs in `pipeline.md`, post-audit (`taste_audit.md`: 🟢). Status: **specification / paper draft — no experiments have been run.** All numbers below are pre-registered design targets, not results.

## Abstract

A rational bargainer's concession should depend only on its private reservation value and the offers on the table, yet an LLM negotiating agent may let payoff-irrelevant linguistic form — an anchored opening offer, a claim of urgency, a fabricated competing bid, an appeal to emotion — move that concession instead. Whether this happens, how much surplus it transfers, and whether it differs by target model or by counterparty defense is currently unmeasured as an isolated, per-tactic causal quantity: existing controlled-injection testbeds score success as binary instruction-integrity, existing formal treatments of LLM persuasion score a stance change, and the negotiation studies that do quantify a tactic's economic footprint either instruct a single bias (anchoring) without separating it from generic assertiveness or optimize an adversarial emotional policy rather than pricing a fixed, named tactic against a concealed ground truth. We build a bilateral bargaining harness in which each side's reservation price is drawn and concealed from both agents, verified absent from their visible context, and known only to the scorer. Into this harness we inject one of four linguistic tactics at a time, holding everything else about the dialogue fixed relative to a matched no-tactic control and a budget-matched generic-toughness control that separates manipulation from mere assertiveness. We measure the resulting surplus-transfer statistic across a cross-model matrix and across three counterparty-sophistication levels, and we audit whether the manipulator actually delivered the tactic and whether the target's concession was genuine. The result is a welfare-pricing catalog: how much surplus each tactic transfers, against which models, and whether cheap prompt-level defenses recover it.

## Introduction

Autonomous LLM agents are increasingly delegated to negotiate real economic transactions — price a purchase, settle a contract term, split a shared resource — on behalf of a human or organizational principal. The premise behind delegating this kind of decision is that the agent will concede only what its assigned valuation and outside options justify. That premise is testable, and it is worth testing directly rather than assuming it holds.

Yet how much surplus a specific linguistic tactic extracts from such an agent has never been measured as an isolated causal quantity. Pieces of the answer exist, and we concede them plainly: LLM negotiators are known to be anchoring-susceptible — a recent case study that instructs a seller agent to apply the anchoring effect shifts the final deal price with the anchor's level (arXiv:2508.21137), and evolutionary search over emotional-pressure policies raises an adversarial buyer's realized savings in multi-turn price negotiation (EvoEmo). But a counterparty that opens with an aggressively anchored offer, claims a deadline that does not exist, invents a competing bid, or leans on emotional pressure is doing something a rational, payoff-maximizing negotiator should be unmoved by — and no existing study prices these tactics on a common welfare scale: one that isolates a named tactic's causal transfer from generic assertiveness with a matched control, scores it as surplus share against a concealed and independently verified two-sided reservation ground truth, and compares tactics, target models, and defenses in one design. This is not a hypothetical concern: a principal who delegates price negotiation to an LLM is exposed to this gap every time the agent negotiates again, and the exposure compounds silently unless someone measures it.

The nearest existing work approaches this gap through controlled adversarial injection, not economic pricing. Testbeds such as Tensor Trust and ChatInject already show that templated, staged adversarial content is a viable, repeatable way to manipulate an LLM's behavior — but both score success as binary instruction-integrity (did the model reveal a secret, follow a forged instruction), not as a continuous economic quantity, so neither can say *how much* was transferred, only whether an instruction boundary was crossed. Two further structural twins on the same tactic-injection methodology, found in an agentic (not bargaining) setting, sharpen this delta rather than close it: DECEPTICON shows that dark-pattern categories — including an urgency category that overlaps this paper's own tactic set — steer LLM web agents toward malicious task-goal deviation, and TRAP builds a 630-combination persuasion-tactic injection space against web agents; both score a binary behavioral/task-redirection outcome, not a continuous, concealed-valuation economic surplus. Work that treats LLM bargaining itself as a live domain — ARIA's negotiation-as-training-environment, CompeteAI's emergent multi-agent market — establishes that negotiation payoffs are quantifiable and that repeated interaction produces measurable dynamics, but neither decomposes where surplus goes or attributes a price shift to a specific injected tactic. A 2026 wave of negotiation benchmarks has since made continuous surplus measurement itself routine — TERMS-Bench scores 13 LLM agents' surplus extraction against an environment-held, concealed counterpart payoff structure, and supply-chain bargaining studies decompose surplus division across model providers and prompt configurations — so the gap this paper closes is no longer "score bargaining economically" but the causal step those benchmarks do not take: attributing a surplus shift to a specific injected linguistic tactic, isolated from assertiveness and audited for delivery. And the closest formal treatment of linguistic influence between LLMs, Strategic Persuasion's Bayesian sender-receiver game, shows that a stance change can be measured as a utility-relevant action shift — but its single-shot, discrete-outcome game has no bilateral price, no private two-sided reservation, and no multi-round concession dynamic to transfer surplus through in the first place.

Turning this gap into a measurable question surfaces its own difficulties. A tactic's apparent effect could simply be generic assertiveness rather than its specific content, so isolating the tactic requires more than one control. Reservation prices are private information in real bargaining, so a valid experiment must conceal them from the agents while still knowing them exactly — and that concealment has to be verified against actual rendered dialogues, not assumed from the harness design. A finding from one model pair may be an artifact of that model's idiosyncrasies rather than a property of the tactic, so comparing potency across models requires a shared action grammar and format. Individual bargaining dialogues are stochastic and outcomes are heavy-tailed, so a real tactic effect has to be separated from ordinary sampling noise and confirmed to reflect the tactic category rather than one lucky phrasing. A defense's effectiveness plausibly differs by which tactic it faces, so testing counterparty sophistication against only one tactic, or reporting a single aggregate verdict across all four, would misrepresent which vulnerabilities a cheap fix actually closes. And because an LLM's guardrails may refuse to fully deliver a deceptive tactic, or a target's apparent concession may itself be strategically feigned rather than genuine, the realized strength of the manipulation is not directly observable from the final price alone.

Our approach turns each of these obstacles into a specific instrument-design choice rather than a hedge. A dedicated controller draws and conceals each side's reservation price, and that concealment is independently verified with a leakage probe rather than assumed. Every tactic dialogue is paired against both a no-tactic control and a budget-matched generic-toughness control, so a tactic's effect is only credited to the tactic once assertiveness alone has been subtracted out. The identical tactic set runs through a fixed matrix of models on one shared action grammar, so a cross-model spread reflects susceptibility rather than harness artifacts. Each tactic is instantiated at multiple phrasings and intensities, so the measured effect can be shown to be a property of the tactic category rather than one specific string. Three counterparty-sophistication conditions are crossed with all four tactics, so a defense's effectiveness is reported per tactic rather than as one number that could hide a tactic it fails against. And an independent auditor verifies realized tactic delivery and concession genuineness, with the explicit requirement that this conditioning be shown to change the substantive verdict in at least one case — a reservation price never enters either agent's visible context, so any shift in the agreed price away from that concealed ground truth is, by construction, attributable to something other than the payoff structure itself, and every instrument above exists to make that attribution precise rather than assumed.

We evaluate this design across synthetic bilateral bargaining scenarios with controller-assigned reservation prices, a parameterized economic-game benchmark for a second controlled substrate, and naturalistic negotiation corpora for an external-validity check, comparing tactic conditions against a no-tactic control and a budget-matched toughness control, alongside reference arms borrowed from the closest prior persuasion and injection work.

In summary, we contribute:
- A concealed-valuation bilateral bargaining harness in which each side's reservation price is verified, not merely assumed, to be absent from either agent's visible context, making surplus transfer mechanically scorable against a known ground truth.
- A paired tactic-isolation design that subtracts a budget-matched generic-toughness control from each tactic's effect, so a measured surplus transfer is attributable to the tactic's specific content rather than to assertiveness in general.
- A cross-model, cross-sophistication measurement of which of four linguistic tactics transfers how much surplus, against which target models, and whether per-tactic-differentiated counterparty defenses recover it.
- A realized-manipulation auditor that verifies tactic delivery and concession genuineness and demonstrates that this verification is load-bearing — changing the accept/reject verdict on the central claims, not merely decorating them.

## Problem Definition

**Formal setup.** Consider a single-good bilateral bargain between a manipulator agent and a counterparty agent. A buyer reservation `b` and seller reservation `s`, with `s < b`, are drawn by a controller and concealed from both agents; the bargaining zone width is `W = b − s > 0`. A negotiation of bounded length yields either an agreed price `p ∈ [s, b]` or an impasse. The manipulator's captured-surplus share on a deal is `σ = (p − s)/W ∈ [0,1]`. A condition `c` fixes a tactic (control, or one of anchoring / false urgency / a fabricated competing offer / emotional pressure, at a given intensity), a manipulator/counterparty model pair, and a counterparty-sophistication level (naive default, bargaining-zone-reasoning, or manipulation-warned). For tactic `t`, paired against a matched no-tactic control on the same scenario `k`, the surplus-transfer statistic is `ΔS_t = E_k[σ(t,k) − σ(control,k)]`. The object of study is `ΔS_t` and its variation across the model and sophistication axes, gated by two auxiliary, mechanically-scored covariates: whether the manipulator's tactic was realized with sufficient fidelity, and whether the counterparty's concession was genuine rather than feigned.

**Why this is hard.** Fixing a tactic condition does not, on its own, isolate that tactic's causal effect: a tactic-condition dialogue differs from its control both in the tactic's specific content and in general assertiveness, so `ΔS_t` alone conflates the two unless a second, budget-matched generic-toughness arm is subtracted out. The concealment that makes `σ` mechanically computable is a property of the rendered dialogue an agent actually sees, not of the harness's intent, so it must be verified by an independent leakage probe rather than assumed from the experimental design. Comparing `ΔS_t` across models is only meaningful if every model is run through an identical action grammar and scenario format, since a model that cannot reliably emit a valid offer will show a distorted `ΔS_t` for reasons unrelated to susceptibility. Because bargaining dialogues are stochastic and outcomes are heavy-tailed, `ΔS_t` must be estimated from enough independently drawn trials — with tactic phrasing and intensity themselves varied — to confirm the estimate reflects the tactic category and not a single string's artifact. A counterparty-sophistication intervention's effect on `ΔS_t` can differ by tactic, so it must be crossed with all four tactics rather than checked against only one. And because the manipulator's guardrails may prevent full delivery of a tactic, or the counterparty's apparent concession may be strategically feigned rather than a genuine payoff-relevant shift, `ΔS_t` computed without conditioning on realized fidelity and concession genuineness risks misattributing non-delivery as ineffectiveness, or feigned compliance as real transfer.

## Method Overview

At a conceptual level, the study is a single measurement pipeline with six cooperating parts, ordered by dependency: a concealment controller first establishes the mechanical ground truth the rest of the pipeline depends on; a paired tactic-injection design with a toughness-matched control then turns raw dialogues into an isolated surplus-transfer estimate; a cross-model matrix and a paraphrase/intensity variance-control design turn that estimate into a comparable, noise-robust statistic across models and tactic instantiations; a counterparty-sophistication crossing turns the same statistic into a per-tactic defense-effectiveness reading; and a realized-manipulation fidelity auditor gates every claim above against the possibility that a raw `ΔS_t` is measuring non-delivery or feigned compliance rather than genuine tactic-driven transfer.

The **concealed-valuation controller** draws each side's reservation price, injects it only into the scorer's private state, and independently verifies — via a leakage probe rather than by assumption — that neither agent's visible context reveals it. The **paired tactic-injection design** runs every treatment dialogue alongside a scenario-matched no-tactic control and a budget-matched generic-toughness control, holding scenario, counterparty prompt, and turn cap fixed, so a tactic's effect can be credited only once generic assertiveness is subtracted out. The **cross-model comparability matrix** runs the identical tactic set through a fixed set of models occupying both roles on one shared action grammar, excluding and reporting (rather than silently dropping) any model whose valid-offer parse rate falls below a pre-specified threshold. The **paraphrase-and-intensity variance-control design** instantiates each tactic at multiple phrasings and strengths, treating them as random effects, so a measured effect can be attributed to the tactic category rather than a single string. The **counterparty-sophistication crossing** runs three sophistication levels against all four tactics factorially, so a defense's effectiveness is reported per tactic instead of as one number that could conceal a tactic it fails against. The **realized-manipulation fidelity auditor** classifies, per dialogue, whether the intended tactic was actually delivered and whether the counterparty's concession was genuine, and its output is required to change at least one substantive verdict elsewhere in the pipeline, not merely accompany it.

## Methodology

### Concealed-Valuation Controller

**Challenge.** Reservation prices are private information in real bargaining; a valid experiment must fix and conceal a ground-truth valuation per side so surplus transfer is mechanically, not subjectively, scorable — but concealment is a property of what an agent's prompt actually contains, not of the experimenter's intent.

**Insight.** Concealment has to be independently verified against rendered dialogue transcripts, not merely designed in, because scenario text can leak reservation information through paraphrase or implication even when no number is stated outright.

**Method.** A dedicated controller draws each side's reservation price and randomizes the bargaining-zone width and midpoint per scenario, injecting the values only into the scorer's private state; every scenario template is audited by string and paraphrase search for implicit leakage, and a held-out sample of dialogues is probed with a "guess the counterpart's reservation" query whose accuracy is checked against chance.

### Paired Tactic Injection with Toughness Subtraction

**Challenge.** A tactic's apparent effect on price could reflect the tactic's specific content, or it could simply reflect generic assertiveness that any sufficiently insistent counterparty would produce; a single no-tactic control cannot separate the two.

**Insight.** Subtracting a second, budget-matched generic-toughness arm — assertive and persistent, but tactic-free — is what makes a tactic's effect attributable to its content rather than to aggression in general.

**Method.** Every treatment dialogue for a given tactic and intensity is run alongside a scenario-matched no-tactic control and a scenario-matched, token- and turn-budget-matched generic-toughness-prompt dialogue, with the manipulator's template as the only variable that differs across the three. A tactic's surplus transfer is reported only after the toughness control's own transfer is subtracted from the tactic's.

### Cross-Model Comparability Matrix

**Challenge.** A finding from a single model pair may reflect that pair's idiosyncrasies — instruction-following quirks, valid-offer parse failures — rather than a general property of the tactic or of model families.

**Insight.** A cross-model spread in surplus transfer is only informative if the tactic template and scenario format are held identical across models, so that any observed difference reflects susceptibility rather than incidental harness mismatches.

**Method.** The identical tactic set, at identical intensities, is run through a fixed matrix of LLMs occupying both the manipulator and counterparty roles under one shared action grammar and scenario format; models whose valid-offer parse rate falls below a pre-specified threshold are excluded and reported, not silently dropped from the comparison.

### Paraphrase-and-Intensity Variance Control

**Challenge.** Individual bargaining dialogues are stochastic and outcomes are heavy-tailed, so a genuine tactic effect must be distinguished from ordinary sampling noise, and confirmed to be a property of the tactic category rather than one specific phrasing.

**Insight.** A tactic's effect is only a meaningful category-level claim if the variance introduced by paraphrasing and intensity within a tactic is small relative to the variance across different tactics — otherwise, what looks like "the tactic's effect" is really one string's artifact.

**Method.** Each tactic is instantiated at no fewer than five phrasing variants and two or more intensity levels; phrasing is modeled as a random effect in a mixed-effects specification powered, via pilot variance estimates, to detect a target effect size at a pre-specified power level with a pre-specified per-cell sample size. The five-variant floor exists because a variance component estimated from fewer than about five levels is statistically unreliable; if fewer than five variants survive fidelity screening for a tactic, phrasing is pre-committed to be modeled as a fixed effect for that tactic instead, and the category-level claim is correspondingly narrowed.

### Counterparty-Sophistication Crossing

**Challenge.** A catalog built against a single, naive default counterparty conflates "how strong is this tactic" with "how easy is it to fool this one specific default prompt," and a defense's effectiveness plausibly varies by which tactic it faces.

**Insight.** A single mixed-effects specification crossing sophistication with tactic yields two distinct, separately falsifiable estimands from one fit: whether sophistication changes the average transfer at all, and whether it changes transfer unevenly across tactics — one instrument, two readouts, not two mechanisms.

**Method.** Three counterparty-sophistication conditions — a naive default, an explicit bargaining-zone-reasoning prompt, and an explicit manipulation-warning prompt — are crossed factorially with all four tactics, holding model identity fixed within each comparison, and fit with a sophistication-by-tactic interaction term.

### Realized-Manipulation Fidelity Auditor

**Challenge.** A manipulator's guardrails may refuse to fully deliver a deceptive tactic, and a counterparty's apparent concession may itself be strategically feigned rather than a genuine payoff-relevant shift; neither is directly observable from the final price alone.

**Insight.** Fidelity and genuineness verification only earn their place if conditioning on them is shown to actually change a substantive verdict elsewhere in the pipeline — a demonstrated, falsifiable load-bearing test, not an assumed one.

**Method.** An LLM judge, spot-checked by a human annotator on a stratified sample, classifies whether the manipulator's turns deliver the intended tactic and whether the counterparty's concession is genuine, via a re-probe that removes the tactic's factual claim from context and checks whether the counterparty still accepts the same price; every headline surplus-transfer statistic is reported both unconditionally and restricted to verified-fidelity, verified-genuine dialogues.

## Experiments

### Experimental Setup

**Datasets.** Synthetic single-good buyer/seller scenarios with controller-assigned, randomized reservation prices — the primary substrate, and the only one that satisfies the concealed-valuation constraint by construction, since the controller generates and holds out the ground truth itself. GLEE (Shapira et al., 2024) — a parameterized economic-game benchmark offering controlled surplus size and asymmetry, used to test whether the magnitude and cross-model findings are stable under a second controlled substrate, not only the fully synthetic one. CraigslistBargain (He et al., 2018) and Deal-or-No-Deal (Lewis et al., 2017) — naturalistic price-negotiation corpora, used specifically to test whether the magnitude and cross-model findings generalize beyond experimenter-authored scenario phrasing to real negotiation language.

**Baselines** (sanity-check comparators and upper-reference arms — this is a measurement study, and no research question here is framed as "our procedure beats baseline X"). A no-tactic, neutral negotiating prompt is the necessary control for every tactic claim; every surplus-transfer statistic is defined relative to it. A generic-toughness prompt, budget-matched on token and turn count, is the discriminator that separates tactic-specific manipulation from mere assertiveness. A Nash / split-the-difference midpoint reference is used only as a rationality sanity check on the control condition itself, confirming mean control surplus share falls in a plausible range before any tactic claim is trusted. Strategic Persuasion's Sender agent is borrowed as a strong strategic-manipulator upper-reference arm — its own protocol reused, not its own reported persuasion-success numbers compared against. ChatInject's forged-role, staged-dialogue injection is borrowed as an adversarial upper bound on how much realizable manipulation intensity is achievable at all, independent of whether it is economically framed.

**Metrics.** The paired surplus-transfer statistic and its mixed-effects estimate with confidence intervals; deal rate and impasse rate; the individual-rationality-violation rate (agreements outside either side's own reservation); realized tactic fidelity rate and manipulator refusal rate; and the genuine-versus-feigned concession rate.

**Scale and power.** The full crossed design implies on the order of 20,000–30,000 dialogues (four tactics × roughly six models × n ≈ 200 per cell, each cell paired with its no-tactic and budget-matched toughness arms, plus the three-level sophistication crossing and the phrasing/intensity variants), which at typical multi-turn dialogue lengths is a low-hundreds-of-millions token budget; the pre-registration commits to reporting the realized dialogue and token counts alongside the results. The per-cell n ≈ 200 basis is derived for detecting a main effect of ΔS ≈ 0.10 at 80% power; because the RQ4 and RQ7 verdicts rest on *interaction* likelihood-ratio tests, which require roughly four times the per-cell sample to detect an interaction of the same magnitude, the pre-registered detectable interaction size for those two tests is widened accordingly (to ≈ 0.20 of the bargaining-zone width at the same power) rather than silently reusing the main-effect basis — a smaller true interaction is then reported as INCONCLUSIVE at this scale, not as absent.

**Research questions:**
1. RQ1 — Is the concealment of each side's reservation price actually verified in the rendered dialogues, not just assumed by design?
2. RQ2 — How much surplus does each tactic transfer relative to a matched no-tactic control?
3. RQ3 — Does each tactic's transfer survive subtraction of a budget-matched generic-toughness control?
4. RQ4 — Does tactic potency vary significantly, and by how much, across target models?
5. RQ5 — Are smaller or less safety-tuned models more susceptible than larger, more heavily-aligned ones?
6. RQ6 — Does the measured effect reflect the tactic category, or a single phrasing?
7. RQ7 — Do counterparty-sophistication defenses reduce transfer, and does the reduction differ by tactic?
8. RQ8 — Is anchoring specifically more resistant to sophistication-based defenses than the other tactics?
9. RQ9 — Does conditioning on verified tactic delivery and concession genuineness change the substantive verdict?
10. RQ10 — (mechanism, guidance.md R6) Does anchoring move the final price via a reference-point shift, distinct from mere perceived toughness?

#### RQ1: Is the concealment of each side's reservation price actually verified in the rendered dialogues, not just assumed by design?

**Setup.** A held-out sample of dialogues across all tactic conditions is probed with a "guess the counterpart's reservation" query directed at each agent; guessed values are compared against the true concealed reservations for statistically-significant deviation from chance-level accuracy.

**Expected outcome.** Guess accuracy is statistically indistinguishable from chance, pooled across all tactic conditions.

**Falsification condition.** Refuted if guess accuracy is significantly above chance in any condition — this would mean reservation information leaks through scenario phrasing or dialogue content, invalidating the mechanical ground truth for that condition until the leak is patched, and every downstream surplus-transfer claim in that condition would need to be withheld pending a fix.

**Hypothesis (plain language).** The harness's concealment design actually holds in the dialogues agents see, not only in the experimenter's intent.

**Metrics.** Leakage-probe accuracy versus chance, pooled and per condition.

**Result.** *[placeholder — fill in after experiments are run]*

#### RQ2: How much surplus does each tactic transfer relative to a matched no-tactic control?

**Setup.** For each tactic, paired-by-scenario bootstrap comparison of the manipulator's captured-surplus share against the matched no-tactic control, across roughly 200 dialogues per tactic in the pilot stage, scaling to a larger cross-model grid; per-tactic significance tested at a Bonferroni-corrected threshold across the four tactics.

**Expected outcome.** At least one tactic's surplus-transfer statistic is significantly nonzero and reaches at least one-tenth of the bargaining-zone width. Secondarily, the per-tactic ordering satisfies anchoring ≈ fabricated-offer > false-urgency > emotional-pressure (the predicted ordering is a secondary, not load-bearing, prediction).

**Falsification condition.** Refuted toward "no manipulable surplus" if no tactic reaches the one-tenth threshold and none reaches even a smaller reliability floor (0.03 of the bargaining-zone width, the pre-registered reliability floor) — this collapses into the global fallback that current LLM bargainers are structurally robust to single-tactic linguistic manipulation within this design. If no tactic clears the primary threshold but at least one clears the reliability floor, the finding is reframed from "large, exploitable transfer" to "small but statistically reliable transfer," not treated as a clean refutation. If the magnitude threshold is cleared but the predicted ordering is contradicted, the ordering claim alone is dropped and the *observed* ordering is published as the catalog instead — the ordering was a prediction, not a load-bearing claim, so its failure does not affect the magnitude verdict.

**Hypothesis (plain language).** At least one of the four tactics moves the agreed price away from what a matched, tactic-free negotiation would produce, and the tactics are expected to rank roughly anchoring/fabricated-offer above false-urgency above emotional-pressure.

**Metrics.** Per-tactic surplus-transfer statistic and its confidence interval; final classification against the pre-registered threshold.

**Result.** *[placeholder — fill in after experiments are run]*

#### RQ3: Does each tactic's transfer survive subtraction of a budget-matched generic-toughness control?

**Setup.** For each tactic that clears RQ2's threshold, its surplus-transfer statistic is compared against the budget-matched generic-toughness control's own statistic on the same scenarios; the difference is tested against a pre-registered minimum margin.

**Expected outcome.** For tactics clearing RQ2's threshold, the tactic-minus-toughness difference clears the pre-registered margin, at the pre-registered significance level.

**Falsification condition.** Refuted, per tactic, if the tactic-minus-toughness difference does not clear the margin — that tactic's apparent effect is then attributed to generic assertiveness rather than tactic-specific manipulation, and is reported as such rather than folded into the manipulation catalog. This is assessed per tactic; one tactic failing this test does not refute another tactic's result.

**Hypothesis (plain language).** A tactic's measured transfer is due to what it specifically says, not merely to being assertive.

**Metrics.** Per-tactic toughness-subtracted transfer and its confidence interval.

**Result.** *[placeholder — fill in after experiments are run]*

#### RQ4: Does tactic potency vary significantly, and by how much, across target models?

**Setup.** A mixed-effects model with a tactic-by-model interaction term is fit across the cross-model matrix; the interaction is tested via a likelihood-ratio test, and per-model spread in surplus transfer is computed for each tactic.

**Expected outcome.** The tactic-by-model interaction is statistically significant, and at least one tactic shows a per-model spread of at least one-tenth of the bargaining-zone width.

**Falsification condition.** Refuted if the interaction is non-significant and no tactic's per-model spread reaches the threshold — in that case the finding is reframed as "tactic susceptibility is approximately model-invariant, and a single catalog generalizes across the tested models," a stronger and simpler transfer claim rather than a failure of the research question.

**Hypothesis (plain language).** How much a tactic works depends on which model it is used against.

**Metrics.** Interaction-term significance; per-tactic per-model spread with confidence intervals.

**Result.** *[placeholder — fill in after experiments are run]*

#### RQ5: Are smaller or less safety-tuned models more susceptible than larger, more heavily-aligned ones?

**Setup.** Within the cross-model matrix, per-model surplus-transfer statistics are ranked and compared against each model's approximate scale/alignment tier, for tactics reaching significance in RQ4.

**Expected outcome.** For at least one tactic, smaller or less safety/instruction-tuned counterparty models show significantly larger surplus transfer than larger, more heavily-aligned counterparty models.

**Falsification condition.** Refuted if larger, more heavily-aligned models are equally or more susceptible than smaller ones, or if susceptibility shows no systematic relationship to scale or alignment tier — reported as an absence of the predicted direction, independent of whether RQ4's interaction itself is significant.

**Hypothesis (plain language).** Model scale and alignment tuning are not neutral with respect to manipulability.

**Metrics.** Per-model-tier surplus-transfer comparison with confidence intervals.

**Result.** *[placeholder — fill in after experiments are run]*

#### RQ6: Does the measured effect reflect the tactic category, or a single phrasing?

**Setup.** Within each tactic, surplus-transfer variance across paraphrase-and-intensity variants is compared against variance across different tactics, using the same mixed-effects specification as RQ2/RQ4 with paraphrase as an explicit random effect.

**Expected outcome.** Within-tactic paraphrase variance is significantly smaller than across-tactic variance in mean transfer.

**Falsification condition.** Refuted if within-tactic paraphrase variance is comparable to or exceeds across-tactic variance — this would mean the measured "tactic effect" is actually an artifact of one specific phrasing rather than a property of the tactic category, and the catalog would need to be re-scoped to specific templates rather than tactic labels.

**Hypothesis (plain language).** The catalog measures a property of each tactic as a category, not of one lucky or unlucky sentence.

**Metrics.** Within-tactic versus across-tactic variance ratio, with confidence intervals.

**Result.** *[placeholder — fill in after experiments are run]*

#### RQ7: Do counterparty-sophistication defenses reduce transfer, and does the reduction differ by tactic?

**Setup.** A mixed-effects model with a sophistication-by-tactic interaction term is fit across the three sophistication conditions and four tactics; the interaction is tested via a likelihood-ratio test, and per-tactic percentage reduction relative to the naive-default condition is computed for each non-naive condition.

**Expected outcome.** The sophistication-by-tactic interaction is statistically significant, and at least one non-naive sophistication condition reduces mean surplus transfer by at least half, relative to the naive default, for the tactic or tactics it targets.

**Falsification condition.** Refuted if no sophistication condition reduces transfer by the threshold for any tactic and the interaction is non-significant — this supports the safety-relevant negative finding that cheap prompt-level defenses do not meaningfully recover surplus, which is itself a reportable, decision-relevant result rather than a null outcome to be discarded.

**Hypothesis (plain language).** At least one cheap, prompt-level defense meaningfully reduces manipulability for at least one tactic, and its effectiveness is not uniform across tactics.

**Metrics.** Interaction-term significance; per-tactic percentage reduction with confidence intervals.

**Result.** *[placeholder — fill in after experiments are run]*

#### RQ8: Is anchoring specifically more resistant to sophistication-based defenses than the other tactics?

**Setup.** Among the per-tactic percentage reductions computed in RQ7, anchoring's reduction is compared against the other three tactics' reductions.

**Expected outcome.** Anchoring shows the smallest percentage reduction in surplus transfer across sophistication conditions among the four tactics.

**Falsification condition.** Refuted if anchoring's percentage reduction is comparable to or larger than the other tactics' reductions — this would undercut the account that anchoring specifically works by biasing the reference point itself (something explicit reasoning does not straightforwardly correct), rather than by exploiting a correctable failure of the naive default counterparty.

**Hypothesis (plain language).** Anchoring is harder to defend against with cheap reasoning-based prompts than the other three tactics, because it shifts the reference point the reasoning itself operates on.

**Metrics.** Anchoring's percentage reduction versus the other three tactics', with confidence intervals.

**Result.** *[placeholder — fill in after experiments are run]*

#### RQ9: Does conditioning on verified tactic delivery and concession genuineness change the substantive verdict?

**Setup.** For each tactic-by-model cell, the accept/reject verdict against RQ2's pre-registered threshold is recomputed twice: once on all dialogues, and once restricted to dialogues verified by the fidelity auditor as high-fidelity tactic delivery and genuine (non-feigned) concession; the two verdicts are compared cell by cell.

**Expected outcome.** In at least one tactic-by-model cell, the verdict computed on verified-fidelity, verified-genuine dialogues differs from the verdict computed on all dialogues.

**Falsification condition.** Refuted if the verdict is identical with and without fidelity/genuineness conditioning in every tested cell — this would mean the auditor's classification, while informative as a diagnostic, is not load-bearing for any headline claim in this study, and its role in the pipeline would need to be reported as a validity check rather than a claim-changing instrument.

**Hypothesis (plain language).** Whether a tactic was actually delivered and a concession was genuine is not a decorative side-channel — it can flip which conclusion the raw statistic alone would support.

**Metrics.** Count and identity of tactic-by-model cells whose verdict changes under conditioning; fidelity and refusal rates; genuine-versus-feigned concession rate.

**Result.** *[placeholder — fill in after experiments are run]*

#### RQ10 (mechanism): Does anchoring move the final price via a reference-point shift, distinct from mere perceived toughness?

**Why this is a mechanism analysis, not a restatement of RQ3.** RQ3 asks a *categorical* question — does anchoring's effect survive subtracting a toughness-matched control at all? RQ10 asks a *dose-response* question about the surviving effect's cause: if anchoring works by shifting the counterparty's perceived reference point, the numeric distance of the opening anchor from the true bargaining-zone-fair point should predict the final price continuously, over and above a measured toughness-perception covariate — a correlational surplus-transfer statistic alone cannot show this (guidance.md's counterfactual-test-not-correlation-only bar).

**Setup.** Restricted to the anchoring condition's dialogues only (the matched control has no anchor to regress on), a regression of final price on (i) the opening anchor's numeric distance from the bargaining-zone-fair point and (ii) an independent fidelity-auditor rating of perceived manipulator toughness is fit with and without the toughness covariate; the percent attenuation of the anchor-distance coefficient between the two specifications is the diagnostic quantity.

**Expected outcome.** The anchor-distance coefficient remains statistically significant with the toughness covariate included, and its standardized effect size retains at least half of its magnitude from the toughness-uncontrolled specification.

**Falsification condition.** Refuted if the anchor-distance coefficient is attenuated by at least half once the toughness covariate is added — anchoring's transfer (if any, per RQ2) is then reported as mechanistically indistinguishable from generic perceived assertiveness at the reference-point level, even where RQ3's categorical subtraction shows a tactic-specific effect. This downgrades only the mechanism claim, not RQ2's magnitude claim.

**Hypothesis (plain language).** Anchoring works by shifting where the counterparty thinks a fair price sits, not merely by making the manipulator seem more aggressive.

**Metrics.** Anchor-distance regression coefficient, with and without the toughness-perception covariate; percent attenuation with a bootstrap confidence interval.

**Result.** *[placeholder — fill in after experiments are run]*

**Further evaluation.** With more time, a natural extension is multi-issue and multi-party bargaining, where a tactic could plausibly trade off against multiple dimensions simultaneously — explicitly out of scope here because it changes the surplus-transfer statistic from a single scalar share to a vector-valued allocation problem, and would need its own identifiability design rather than a direct extension of the toughness-subtraction discriminator above.

## Related Work

The closest prior work to this paper by methodology is Tensor Trust and ChatInject, and it is worth stating the delta plainly before surveying the wider landscape: both already demonstrate that controlled, templated, single-variable adversarial injection reliably manipulates LLM behavior — but both score success as binary instruction-integrity (was a secret revealed, was a forged instruction followed), not as a continuous economic quantity measured against a concealed ground truth, which is precisely the pricing gap this paper is built to close.

**LLM bargaining and negotiation as an economic domain.** ARIA trains language agents in open-ended environments including negotiation and bargaining, explicitly noting that reward variance there is amplified by opponent dynamics and delayed outcomes; CompeteAI embeds competing LLM agents in a persistent, resource-constrained market and studies cumulative advantage over repeated rounds. Both establish that LLM bargaining produces quantifiable, opponent-sensitive payoffs, but neither decomposes where surplus goes or attributes a price shift to a specific injected linguistic tactic — ARIA works to reduce reward variance for a learner rather than characterize an existing agent's susceptibility, and CompeteAI's competition dynamics emerge endogenously, with no injected, held-constant treatment and no concealed ground-truth valuation to mechanically price a transfer against.

**Continuous-payoff negotiation benchmarks and single-tactic effect studies (2025–26, concede-and-differentiate).** A recent wave of work has made two components of this paper's design individually available, and we concede each before claiming the residual delta. TERMS-Bench specifies the counterpart's latent type, policy, and payoff structure inside the environment — concealed from the agent, visible to the evaluator — and diagnoses 13 LLM negotiators' surplus extraction, cue use, and belief calibration continuously, so a concealed-payoff bargaining environment with mechanical surplus scoring is no longer novel on its own; but TERMS-Bench characterizes an agent's *capability* against an oracle reference and injects no manipulation treatment, so it cannot attribute a surplus shift to a tactic. A supply-chain bargaining study likewise scores nine models' surplus division against game-theoretic benchmarks, finding prompt configuration dominates the explained variance in surplus split, but again with no injected, held-constant tactic treatment. On the tactic side, an anchoring case study instructs a seller agent to apply the anchoring effect in price-negotiation simulations and shows the final deal price moves with the anchor's level — the single nearest measurement to RQ2 for one of our four tactics — but it has no assertiveness-matched control, no two-sided concealed-and-verified reservation, no surplus-share statistic, and no cross-tactic comparison; and EvoEmo evolves emotional-pressure policies that raise an adversarial buyer's savings across models, which prices an *optimized policy*, not a fixed, named, causally isolated tactic. The residual delta this paper claims is exactly the intersection none of these occupies: a per-tactic causal surplus-transfer statistic, isolated from generic assertiveness by a budget-matched control, scored against a leakage-verified concealed ground truth, and gated on verified tactic delivery.

**Formalized measurement of LLM linguistic influence.** Strategic Persuasion formalizes persuasion as a natural-language Bayesian sender-receiver game, in which a Sender observes a state of nature and communicates strategically to shift a Receiver's stance, scored as a utility-relevant change in the Receiver's action. This shows that linguistic influence between LLMs can be measured formally, not just observed anecdotally — but its single-shot game with a discrete action readout has no bilateral price, no two-sided private reservation value, and no multi-round concession dynamic, so its persuasion metric does not translate into a bargaining surplus-transfer statistic.

**Controlled adversarial injection testbeds.** Tensor Trust harvests human-authored prompt-injection attacks and defenses from an online game and filters them by cross-model transferability to build an interpretable robustness benchmark; ChatInject shows that staged, fabricated multi-turn dialogue and forged role tags are substantially stronger injection levers than a single plain-text imperative. Both establish controlled, templated, single-variable injection as a viable and repeatable methodology — the same discipline this paper's tactic-injection design borrows directly — but neither's success construct is a continuous economic quantity: Tensor Trust scores a binary string-comparison objective, and ChatInject scores instruction compliance, so neither can say how much of anything was transferred, only whether a boundary was crossed.

**Agentic manipulation-tactic benchmarks (concede-and-differentiate).** Two further works, surfaced by a reference-cache freshness sweep after the original related-work pass, are genuine structural twins on tactic-injection methodology and deserve the same direct treatment rather than a hedge: DECEPTICON isolates six dark-pattern categories — including an urgency category that overlaps this paper's own tactic set — injected into web-navigation UI flows, and shows they steer LLM web agents toward malicious task-goal deviation at high rates, with effectiveness *increasing* with model scale and test-time reasoning; TRAP independently confirms the same qualitative phenomenon with a larger, modular attack space (7 persuasion principles × 5 manipulation methods, 630 combinations) against web agents. We concede what is genuinely shared: both independently establish that a named, categorical manipulation-tactic taxonomy causally steers LLM agent behavior, and both isolate individual tactics via controlled injection exactly as this paper's design does. The delta is the outcome construct, not the injection methodology: DECEPTICON and TRAP score a binary behavioral outcome (did the agent deviate from its task goal, was it redirected), which answers *whether* a tactic steered behavior but not *how much* economic value moved as a result — neither models a two-sided concealed valuation or a continuous surplus-transfer statistic, so "urgency" in their setting shifts a click or a redirected action, not a mechanically-scored price concession against a known ground truth.

**Strategic (dis)honesty and mechanism-design pricing of manipulation.** Strategic Dishonesty separates genuine refusal, genuine compliance, and strategically feigned "fake compliance" in adversarial safety evaluations of frontier models, detecting the distinction from internal activations; ClickBandit models providers who strategically misreport a scalar (click-through rate) to extract exposure in a bandit-based recommendation mechanism, proving that an incentive-unaware algorithm suffers linear regret and designing a screening algorithm that accounts for strategic misreporting. Strategic Dishonesty's fake-versus-genuine-compliance distinction is the direct model for this paper's concession-genuineness check, but it is built for an adversarial evaluator-versus-model setting, not a mixed-motive bilateral economic exchange; ClickBandit prices strategic manipulation of a single reported scalar in a one-sided platform setting, not two-sided bilateral bargaining with free-form linguistic tactics — neither provides a per-tactic decomposition of who captures surplus in a bargaining dialogue.

## Conclusion

This work reframes an assumption implicit in delegating bargaining to LLM agents — that a rational, payoff-maximizing negotiator is unmoved by payoff-irrelevant linguistic form — as a directly measurable, falsifiable question, rather than treating today's agents as trustworthy by default. The central methodological wager is that a tactic's surplus transfer is only a defensible, attributable claim once it survives subtraction of a matched aggression-only control and is conditioned on independently verified tactic delivery and concession genuineness; a design that skipped either check risks mistaking mere assertiveness, or a manipulator's guardrail-blunted attempt, for a clean measurement of the tactic itself. Whichever pattern dominates for current LLM bargainers, the finding is decision-relevant: a reliable transfer for even one tactic quantifies a concrete, per-negotiation economic exposure for any principal delegating bargaining to that model, while a uniformly null result — every tactic failing to clear even the reliability floor once toughness is subtracted out — would itself be a publishable bound on that exposure. Two limitations bound this claim from the outset and are natural next steps rather than afterthoughts: the study is scoped to single-good, two-party bargaining with four named tactics, leaving multi-issue and multi-party settings and tactics not tested here for follow-up; and the toughness-subtraction discriminator, while sufficient to separate manipulation from generic assertiveness in a single-issue setting, may need a richer control battery once the design is extended to multi-issue bargaining, where "assertiveness" itself becomes multi-dimensional.

---

## Pre-handoff checklist

- **Organization/navigation** — narrative flows problem → method → experiments → related work without forward references to undefined terms.
- **Terminology discipline** — "concealed-valuation controller," "surplus-transfer statistic," "toughness subtraction," "realized-manipulation fidelity" each defined at first use in Problem Definition/Methodology, used consistently thereafter; no internal stage IDs (`sp_*`, `m_*`, `rq_*`) leaked into prose — checked directly against `pipeline.md`.
- **Notation with worked example** — the formal setup section defines `(b, s, W, σ, p, ΔS_t)` and the Problem Definition/Methodology/Experiments sections consistently reuse this notation; no separate worked numeric example is included since no numbers exist yet (would require fabricating results).
- **RQ framing matches outcomes** — all 10 RQs are graded/quantitative (rates, spreads, percentage reductions, agreement proportions, regression coefficients), each answered in its own subsection with an explicit falsifiable expected outcome and falsification condition, not a binary yes/no. RQ10 is the guidance.md R6 mechanism analysis (mandatory for the analysis/measurement archetype), added to close a Phase A method-rigor-audit gap; it is mechanism-tier only and is not promoted to the abstract unless it survives.
- **Bibliography wiring** — every named prior work in Introduction, Experimental Setup, and Related Work carries a real citation resolving to `refs.bib` in the LaTeX version, which is script-generated from `reference_candidates.jsonl`'s `selected` records, not hand-typed.
- **No typesetting artifacts** — no `[CITE]`/`[TODO]` placeholders; only explicit `[placeholder — fill in after experiments are run]` markers in Results, per the drafting convention this is a pre-registered spec, not a report.
- **Artifact plan** — the bargaining harness (concealment controller, tactic-injection templates, cross-model matrix runner, fidelity auditor) and the self-generated transcript corpus are the natural release artifacts; not yet built, so not claimed as available.

## Hand-off

This is a Markdown draft, not a finished paper — experiments have not run. Natural next steps: `research-paper-writing` for LaTeX conversion and prose polish once a target venue is chosen, or back into this pipeline if a stage needs revision (e.g., if piloting surfaces that the leakage probe in RQ1 fails at a much higher rate than expected, that is exactly the kind of cross-stage problem that becomes visible only once a draft exists, per `paper_assembly.md`).
