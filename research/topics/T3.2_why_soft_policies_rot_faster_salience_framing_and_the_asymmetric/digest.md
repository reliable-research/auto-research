# Digest: Why Soft Policies Rot Faster: Salience, Framing, and the Asymmetric Decay of In-Context Constraints

> **REVERSE-DIGEST NOTICE.** No paper exists yet. This document is speculative scaffolding
> for research planning: it projects what an N0–N12 digest *would* look like for a paper
> that answered the seed idea below. Every field is tagged inline:
> **[GIVEN]** = verbatim/near-verbatim from the seed README; **[HYPOTHESIS]** = reasoned
> elaboration/prediction, not a fact; **[PLACEHOLDER]** = genuinely unknowable until the
> work is done (never invented); **[GROUNDED:corpus]** = a real OpenReview paper from
> `topics/corpus/ideas.jsonl`, whose approach_summary is grounded in that paper's own
> motivation/method text (its *relevance framing* to this future paper is still this
> digest's judgment call). Treat all [HYPOTHESIS]/[PLACEHOLDER] content as falsifiable
> planning material, not results.

**Seed source:** `topics/T3.2_why_soft_policies_rot_faster_salience_framing_and_the_asymmetric/README.md`
Code T3.2 · label `[机制]` (mechanism) · parent topic "T3. Memory 约束保持（窄环，4 条)" [GIVEN]

---

## N0 — Metadata

- `title`: "Why Soft Policies Rot Faster: Salience, Framing, and the Asymmetric Decay of In-Context Constraints" **[GIVEN]** (verbatim from seed README line 16)
- `authors`: `["Anonymous"]` **[PLACEHOLDER]** — no paper exists, no authors can be known.
- `abstract` **[HYPOTHESIS, drafted — not a real abstract]**:
  > "Deployed LLM agents are steered by two qualitatively different kinds of in-context
  > constraints: soft organizational policies (stylistic, business-preference, or
  > operational-scope rules injected via system prompt) and hard safety norms (refusal of
  > harmful requests, reinforced during alignment training). Prior work reports that
  > adherence to soft policies decays roughly 8x faster than adherence to hard norms over
  > long-horizon interactions, but the mechanism behind this asymmetry is unknown. We ask
  > whether the gap is driven by (i) contextual salience (position and repetition of the
  > constraint), (ii) framing (the wording strength used to state it), or (iii) the
  > pretraining/alignment prior attached to the constraint's content. We build a matched
  > soft/hard constraint-pair bank and a long-horizon probe environment that injects
  > constraints into multi-turn conversations padded with realistic distractor turns,
  > orthogonally manipulating wording strength, context position, and repetition count.
  > Fitting per-condition discrete-time survival curves of constraint adherence and
  > decomposing variance in the soft/hard decay-rate gap across the three factors, we
  > attribute the asymmetry to its candidate mechanisms and derive placement/wording
  > guidance for policy authors."
- `doi`: `null` **[PLACEHOLDER]**
- `arxiv_id`: `null` **[PLACEHOLDER]**
- `num_pages`: `null` **[PLACEHOLDER]**
- `research_area`: `"AI/ML"` **[HYPOTHESIS]** — inferred from the domain (LLM agent in-context behavior); no venue exists to confirm.

**Status:** NOT_FOUND (paper doesn't exist). `absence_comment`: {`what_missing`: "No real title page, byline, or abstract exists because this is a pre-paper research idea, not a parsed document.", `why_matters`: "Any downstream consumer of this digest (e.g. a paper-writer or reviewer agent) must not treat authors/abstract/doi as real bibliographic facts.", `implication`: "Treat N0 as a planning placeholder; regenerate this digest from the real PDF once the paper is written."}

---

## N1 — Problem Formulation

- `objective` **[HYPOTHESIS]**: "Measure and mechanistically decompose the differential
  decay rate of soft organizational-policy constraints versus hard safety-norm constraints
  held in an LLM agent's context window over long-horizon multi-turn interaction, by
  orthogonally ablating contextual salience (position, repetition count), framing (wording
  strength), and pretraining/alignment prior strength (proxied via no-injection and
  base-vs-aligned compliance contrasts), in order to determine which mechanism(s) drive
  the previously reported ~8x gap in decay rate between the two constraint types."
  — Self-check: kind of task = controlled ablation/measurement study; domain = LLM agent
  in-context constraint adherence; outcome shape = attributed decay curves + a
  variance-decomposition mechanism report. All three land.
- `inputs` **[HYPOTHESIS]**, inferred from the minimal experiment ("控制措辞强度/位置/重复次数的消融"):
  1. A bank of matched soft-policy / hard-safety-norm constraint statement pairs, each
     with wording-strength variants (advisory / standard / imperative)
  2. Position-in-context and repetition-count manipulation schedules
  3. A long-horizon multi-turn conversation environment with realistic distractor turns
     and scripted, programmatically verifiable compliance probes
  4. The evaluated LLMs (including at least one open-weights base/instruct pair for the
     prior-strength proxy)
- `outputs` **[HYPOTHESIS]**:
  1. Per-turn, per-condition constraint-adherence measurements (probe pass/fail)
  2. Fitted discrete-time survival curves and decay half-lives per constraint type ×
     manipulation cell
  3. A variance decomposition attributing the soft/hard decay-rate gap to salience,
     framing, and residual (prior-linked) components, plus a probe-reactivity estimate
- `constraints` **[GIVEN]**: the seed explicitly frames the phenomenon to be explained as a
  quantified prior effect size — "组织软政策的衰减远大于硬安全规范（原论文报告约 8 倍差异)" — i.e. any
  valid study design must be able to reproduce or reference this ~8x soft/hard decay-rate
  gap as the baseline effect it is decomposing, and must keep the three candidate
  mechanisms (salience, framing, pretraining prior) separable rather than confounded.
- `text` (objective summary, **[HYPOTHESIS]**): a mechanism-attribution study of asymmetric
  in-context constraint decay.
- **Status:** PARTIAL. `source="inferred"` throughout (no explicit formulation exists in
  any real text — only the seed's one-sentence core question + minimal experiment).
  `absence_comment`: {`what_missing`: "There is no paper text to extract a formal
  problem statement from.", `why_matters`: "The objective above is reconstructed by a third
  party (this digest), not asserted by any author, so its exact scope (e.g. which agent
  domains, which model families) is undetermined.", `implication`: "Use this objective as a
  design target for the eventual study, not as a settled scope statement."}

---

## N2 — Motivation

**Node field:** `motivations`

- MotivationItem 1 **[HYPOTHESIS]**, reconstructed from parent_topic framing ("T3. Memory
  约束保持（窄环，4 条)" — narrow research loop on memory/constraint retention): "Long-running
  LLM agents are frequently governed by two tiers of in-context constraints: safety norms
  (high-stakes, heavily reinforced during RLHF/alignment training) and organizational soft
  policies (lower-stakes stylistic/business/scope preferences injected only via system
  prompt). If soft policies decay much faster than hard norms, deployed agents may silently
  drift out of intended business behavior long before any safety-visible failure occurs,
  creating an invisible governance gap that current safety-focused evaluation would not
  catch." `evidence`: [{type: "citation", text: "OffTopicEval's motivation makes the same
  deployment argument: 'an agent may be unsafe even when it never produces overtly harmful
  content, simply because it answers requests that lie outside its declared role, policies,
  or authority' — i.e. soft/operational policy adherence is a distinct, under-evaluated
  failure surface", source: "GROUNDED:corpus", location: {section: "OffTopicEval
  motivation, OpenReview:EcIyiJrajc"}}].
- MotivationItem 2 **[GIVEN]**: "组织软政策的衰减远大于硬安全规范（原论文报告约 8 倍差异)" — the seed
  itself asserts, as a given premise attributed to "the original paper," that the reported
  decay-rate gap is approximately 8x. This number is treated as a **given input premise to
  be explained**, not as an invented statistic of this future paper.
- MotivationItem 3 **[HYPOTHESIS]**: "Without knowing *which* mechanism drives the
  asymmetry, mitigation guidance is guesswork: if salience dominates, cheap placement and
  restatement fixes suffice; if the alignment prior dominates, no amount of prompt
  engineering will make soft policies as durable as safety norms, and the fix must move
  into training." `evidence`: `[]` (prospective reasoning; no citation evidence exists).
- **Status:** PARTIAL — motivation is reconstructed, not extracted; `source="inferred"` for
  items 1 and 3; item 2 source="given" (seed-level premise). `absence_comment`:
  {`what_missing`: "No author has written a Motivation/Introduction section yet.",
  `why_matters`: "A reviewer cannot yet judge whether the felt urgency ('why does an 8x gap
  matter practically') is over- or under-stated.", `implication`: "Revisit this section once
  the actual paper states its own motivating claims; do not cite this reconstruction as the
  paper's own reasoning."}

---

## N3 — Related Works

**Method:** Grounded corpus search over `topics/corpus/ideas.jsonl` (11,683 OpenReview
papers). Queries run from three keyword angles: (a) mechanism — "position bias; lost in the
middle; attention; salience; primacy; recency" and "prompt sensitivity; phrasing; wording;
paraphrase; formatting; brittleness"; (b) failure mode — "multi-turn; drift; persona;
conversation; consistency", "agent memory; long horizon; forgetting; context; constraint",
and "safety alignment; refusal; shallow; jailbreak; prior"; (c) evaluation domain —
"instruction following; long context; degradation; system prompt" and "system prompt; role;
adherence; robustness; guideline; policy". Each corpus entry's approach_summary is grounded
in the paper's own motivation/method text. One non-corpus entry ([LLMsGetLost, Laban et
al., 2025]) is retained because it is canonical for multi-turn degradation and its
existence is independently verified (arXiv:2505.06120); it is clearly marked NON-CORPUS.

| citation_key | approach_summary | source | paper_url |
|---|---|---|---|
| [SafetyFewTokensDeep, OpenReview:6Mxhg9PtDE] | "Safety Alignment Should Be Made More Than Just a Few Tokens Deep" — formalizes "shallow safety alignment": safety training mostly reshapes the first few output tokens. Instruments this with a per-token KL-divergence diagnostic between aligned and base models on harmful instructions, then deepens alignment via safety-recovery data augmentation and a token-wise constrained fine-tuning loss. Directly characterizes how the *alignment prior* encodes hard safety norms in weights. | GROUNDED:corpus | https://openreview.net/forum?id=6Mxhg9PtDE |
| [TimeToInconsistency, OpenReview:88C7vSdn0t] | Models multi-turn LLM robustness as a *time-to-event* problem: the first inconsistency in an adversarial dialogue is a survival event, conversations without failure are right-censored, and turn-level hazard functions are estimated with embedding-based semantic-drift covariates — converting multi-turn robustness from a static score into a temporally resolved risk signal. | GROUNDED:corpus | https://openreview.net/forum?id=88C7vSdn0t |
| [SinkTrack, OpenReview:Gg1aPETCL6] | Diagnoses that LLMs "hallucinate or forget earlier instructions during long-form generation" because decoding progressively favors newer tokens (recency bias, positional disadvantage), and proposes a training-free fix: cross-attentive enrichment of the BOS attention-sink token so early context stays accessible. Treats *positional salience loss* as the operative mechanism of instruction forgetting. | GROUNDED:corpus | https://openreview.net/forum?id=Gg1aPETCL6 |
| [PrefEval, OpenReview:QWunLKbBGF] | PREFEVAL benchmark: tests whether LLMs infer, remember, and proactively follow user preferences (a soft, low-stakes constraint class) across long multi-session conversations, interspersing preference disclosures and queries with long unrelated distractor spans sampled from LMSYS-Chat-1M; uses paired generation (LLM-judged) and classification tasks. | GROUNDED:corpus | https://openreview.net/forum?id=QWunLKbBGF |
| [OffTopicEval, OpenReview:EcIyiJrajc] | OFFTOPICEVAL: instantiates each LLM as 21 purpose-specific agents via system prompts specifying allowed/forbidden behaviors and refusal instructions (explicit soft operational policies), then measures the accept/refuse tradeoff on in-domain, direct out-of-domain, and adversarially "laundered" out-of-domain queries. | GROUNDED:corpus | https://openreview.net/forum?id=EcIyiJrajc |
| [SafeDialBench, OpenReview:KFjtRqVnKH] | Bilingual multi-turn safety benchmark: 3–10-turn dialogues across 22 scenarios instantiated with seven jailbreak strategies, scoring three fine-grained safety abilities including *consistency across turns* — i.e. the hard-safety-norm side of dialogue-level constraint persistence, motivated by evidence that "safety degradation is cumulative across turns". | GROUNDED:corpus | https://openreview.net/forum?id=KFjtRqVnKH |
| [ICFBench, OpenReview:hcJywRYc3n] | ICF-Bench: evaluates *in-context forgetting* — whether models can suppress revoked/outdated context — via paired NoForget/Forget dialogue instances that isolate the causal effect of forgetting interference from baseline task difficulty, across instructional forgetting, subtask revision, and dynamic preference change scenarios. Its paired-condition design is a template for causal isolation in dialogue evaluation. | GROUNDED:corpus | https://openreview.net/forum?id=hcJywRYc3n |
| [TARE, OpenReview:YEBDvqsniH] | "Beyond Magic Words": shows prompt performance "depends heavily on exact wording, even when nearby paraphrases preserve task intent," and defines *textual sharpness* — worst-case loss over a semantic neighborhood of paraphrases — optimized via black-box min-max prompt evolution. Establishes wording/framing sensitivity as a measurable, first-class robustness dimension. | GROUNDED:corpus | https://openreview.net/forum?id=YEBDvqsniH |
| [RECAST, OpenReview:90tCp2KszA] | RECAST: scalable synthesis of multi-constraint instruction data by mining constraints from instruction–response corpora, with *dual-mode verification* — rule-based programmatic checkers for deterministic constraints (word counts, keywords, structure) and LLM-based validators for qualitative ones (tone, style) — plus constraint-level RL rewards (RLVC). Its verifier taxonomy is directly reusable for labeling constraint adherence. | GROUNDED:corpus | https://openreview.net/forum?id=90tCp2KszA |
| [LLMsGetLost, Laban et al., 2025] | **NON-CORPUS (canonical, verified: arXiv:2505.06120, "LLMs Get Lost in Multi-Turn Conversation")** — large-scale sharded-conversation simulation (200k+ conversations, 15 LLMs, 6 tasks) showing an average 39% multi-turn performance drop, decomposed into minor aptitude loss vs. a 112% increase in unreliability; models that take a wrong turn "get lost and do not recover." | HYPOTHESIS (relevance framing); paper existence verified | https://arxiv.org/abs/2505.06120 |

**Status:** PARTIAL. `absence_comment`: {`what_missing`: "No paper in the searched corpus
directly compares decay rates of soft vs. hard in-context constraints within one matched
design, nor runs the salience/framing/prior ablation the seed calls for — the ten works
above cover each ingredient (soft-policy adherence, multi-turn safety persistence,
survival-style decay modeling, positional salience, wording sensitivity, alignment-prior
depth, verifiable constraint checking) separately.", `why_matters`: "The eventual paper's
novelty claim rests precisely on unifying these ingredients into one factorial
mechanism-attribution design; if a direct precedent exists outside this corpus, the claim
weakens.", `implication`: "Before submission, re-run the positioning search on an
arXiv-native tool (Semantic Scholar) for exact-match precedents on 'constraint decay
asymmetry' and 'system prompt adherence over turns'; the works above are the grounded
positioning base until then."}

---

## N4 — Prior Limitations

**Node fields:** `limitations`, `grounding_check=true` **[HYPOTHESIS]** (every limitation
below cites at least one N3 citation_key, exact string form).

| limitation_text | affects_works | limitation_type | source |
|---|---|---|---|
| Measure adherence to a *single tier* of constraint (user preferences; operational-scope policies) as an outcome, but do not compare decay rates of soft vs. hard constraint types within a matched design, and manipulate neither wording strength nor position/repetition of the constraint statement — so they can document soft-constraint failure but not attribute its mechanism. (Defensible from their own method texts: PREFEVAL varies distractor length and preference form; OFFTOPICEVAL varies query type and language — neither varies the constraint statement's framing or placement factorially.) | [PrefEval, OpenReview:QWunLKbBGF], [OffTopicEval, OpenReview:EcIyiJrajc] | other | HYPOTHESIS |
| Evaluates only the hard-safety-norm side, and only under *adversarial* pressure (seven jailbreak strategies); it does not measure benign, attack-free decay of adherence over turns, and contains no soft-policy conditions to compare against — its own motivation frames the problem as safety-dimension coverage, not constraint-type asymmetry. | [SafeDialBench, OpenReview:KFjtRqVnKH] | generalizability | HYPOTHESIS |
| Estimates turn-level hazard of first failure with *observational* semantic-drift covariates; it predicts when failure happens but never intervenes on the constraint's wording, position, or repetition, so its hazard model cannot separate salience from framing from prior — correlational decay modeling, not causal mechanism attribution. | [TimeToInconsistency, OpenReview:88C7vSdn0t] | theoretical | HYPOTHESIS |
| Presupposes that positional salience loss (recency bias, sink-anchoring) is *the* mechanism of instruction forgetting and builds a mitigation for it; it does not test whether constraint types with different alignment priors or wording strengths decay differently under the same positional disadvantage — the alternative mechanisms are never manipulated. | [SinkTrack, OpenReview:Gg1aPETCL6] | generalizability | HYPOTHESIS |
| Characterizes the alignment prior's depth (per-token KL between aligned and base models) only for hard safety refusals against adversarial exploits; it does not extend the diagnostic to in-context-injected soft policies, nor to decay across conversation turns — its unit of analysis is token depth within one response, not turn depth within a dialogue. | [SafetyFewTokensDeep, OpenReview:6Mxhg9PtDE] | other | HYPOTHESIS |
| Measures wording/paraphrase sensitivity as *point-wise* robustness of a task prompt (worst-case accuracy over a paraphrase neighborhood, single-shot); it does not study whether wording strength modulates the *longitudinal* durability of a constraint over a long interaction. | [TARE, OpenReview:YEBDvqsniH] | other | HYPOTHESIS |
| Tests suppression of *revoked or outdated* context (forgetting that should happen); the complementary failure — unintended decay of a still-valid constraint — is outside its paired NoForget/Forget design, and it does not distinguish constraint types by stakes or prior. | [ICFBench, OpenReview:hcJywRYc3n] | other | HYPOTHESIS |
| Documents multi-turn degradation and its aptitude/unreliability decomposition for *task performance* under underspecification, and RECAST documents degradation under *many simultaneous constraints*; neither stratifies degradation by constraint type (soft policy vs. safety norm) or by the constraint statement's salience/framing, so the asymmetry itself is invisible to their designs. | [LLMsGetLost, Laban et al., 2025], [RECAST, OpenReview:90tCp2KszA] | generalizability | HYPOTHESIS |

**Status:** PARTIAL (all `source="HYPOTHESIS"`, never `"extracted"`, since no author of the
future T3.2 paper has made these limitation claims; each is however defensible from the
cited paper's own motivation/method text as noted inline). `absence_comment`:
{`what_missing`: "These limitations are this digest's inference about the gap between the ten
related works above and the seed's exact question, not claims those papers' authors made about
themselves.", `why_matters`: "A reviewer should not cite these as 'paper X admits Y' — they
are third-party gap analysis.", `implication`: "Re-derive N4 from the eventual paper's own
Related Work section once written; until then use these entries as the positioning
skeleton."}

---

## N5 — Challenges

**Node fields:** `challenges`, `conflation_check=true` **[HYPOTHESIS]**.

- **C1** [HYPOTHESIS, tightly derived from the core question]: "Salience, framing, and
  alignment prior are naturally confounded in the wild: hard safety norms are typically
  stated with more imperative wording, *and* placed prominently, *and* backed by heavy
  RLHF reinforcement of their content. Any observational comparison of soft vs. hard
  constraints therefore conflates all three candidate mechanisms; only an experimental
  design that crosses wording strength with position/repetition on *content-matched*
  constraint pairs can orthogonalize them." (N4-vs-N5 test: this is about why the
  *problem* is hard regardless of any specific prior tool → N5, not N4.)
- **C2** [HYPOTHESIS]: "Decay can only be measured via behavioral compliance probes
  inserted at intervals, and the act of probing may itself refresh the constraint's
  salience (a probe that exercises the constrained behavior implicitly re-mentions its
  topic) — so the measurement instrument perturbs the very decay rate being measured,
  analogous to test–retest reactivity in longitudinal studies."
- **C3** [HYPOTHESIS]: "Constructing soft/hard constraint pairs that are *matched* on
  everything except type is intrinsically hard: the pair must share topic domain, length,
  syntactic complexity, and — critically — an unambiguous, probe-checkable compliance
  criterion, even though soft policies are naturally graded (tone, style, scope) while
  hard norms are naturally binary (refuse/comply). Unmatched pairs turn the type contrast
  into a task-difficulty contrast."
- **C4** [HYPOTHESIS]: "'Alignment/pretraining prior strength' for a given constraint is
  not directly observable — it can only be proxied (no-injection zero-shot compliance;
  base-vs-aligned compliance deltas; per-token divergence diagnostics on open weights),
  and every proxy is itself confounded with model family, scale, and training recipe, so
  the third mechanism can never be manipulated as cleanly as the first two."

**Status:** PARTIAL, `source="inferred"` for all (no paper text exists to extract these
from — they are derived from the core question's own three-way disambiguation plus the
design constraints in N1). `absence_comment`: {`what_missing`: "No author has enumerated
these challenges in prose yet.", `why_matters`: "The eventual paper may name additional or
differently-scoped challenges once real pilot data is collected.", `implication`: "Use
C1–C4 as a design checklist for the minimal experiment, not as a verified challenge list."}

---

## N6 — Methodology

### `overview` **[HYPOTHESIS]**
A controlled factorial ablation framework for attributing the soft/hard constraint
decay-rate gap. Matched soft-policy / hard-safety-norm constraint pairs are injected into
long-horizon multi-turn conversations padded with realistic distractor turns; wording
strength (framing), context position, and repetition count (salience) are manipulated
orthogonally; adherence is measured at scripted probe points with programmatic verifiers;
discrete-time survival curves are fitted per condition and the variance of the soft/hard
decay-gap is decomposed across factors, with prior strength read off a proxy battery.

**Staged plan [HYPOTHESIS]:**
- **Stage 1 — Pilot (= the seed's minimal experiment, "控制措辞强度/位置/重复次数的消融"):**
  2 models (one hosted frontier model, one open-weights instruct model), 20 matched
  constraint pairs, a 2×2×2×2 factorial (type: soft/hard × wording: advisory/imperative ×
  position: system-prompt-start/injected-at-turn-10 × repetition: 1/3), 30-turn
  conversations with probes every 5 turns, 3 seeds per cell → ~960 conversations per
  model. Success criterion: the soft/hard decay-gap replicates directionally
  (soft half-life < hard half-life) and at least one manipulation factor shows a
  detectable interaction with the gap; otherwise redesign probes before scaling.
- **Stage 2 — Scale-up:** ≥6 models across ≥3 families (including one base/instruct pair
  for M5), 40 pairs, 3-level wording and position factors, repetition {1,3,5}, horizon
  extended to 100 turns on a fractional-factorial subsample; adds the between-conversation
  probe design (M6) on the cells that pilot analysis flags as significant, and a
  mitigation-baseline arm (naive every-k-turn restatement; SinkTrack-style anchoring where
  weights are accessible).

### `key_components`
- **M1 — Matched Constraint-Pair Bank** [HYPOTHESIS]: 40 soft-policy / hard-safety-norm
  statement pairs, matched per pair on topic domain, token length (±10%), and verifier
  type; each statement authored in 3 wording-strength variants (advisory: "we prefer that
  you…"; standard; imperative: "you must never…") via templated rewrite plus human review.
  Soft policies drawn from the style of [OffTopicEval, OpenReview:EcIyiJrajc]'s
  policy-conditioned system prompts and [PrefEval, OpenReview:QWunLKbBGF]'s preference
  statements; hard norms drawn from standard harmful-request refusal categories. Wording
  variants are checked for semantic equivalence (embedding similarity threshold + human
  audit), operationalizing the manipulation-validity concern from [TARE,
  OpenReview:YEBDvqsniH]'s paraphrase-neighborhood construction.
- **M2 — Position × Repetition Controller** [HYPOTHESIS]: harness that (a) places the
  constraint statement at one of three context loci (system-prompt head; system-prompt
  tail; injected as a user turn mid-conversation), and (b) restates it verbatim 1/3/5
  times at pre-scheduled turns, holding total context token count constant across cells
  via length-matched filler — directly implementing the seed's "位置/重复次数" ablation as
  the salience factor, with position effects interpretable against the recency-bias
  account in [SinkTrack, OpenReview:Gg1aPETCL6].
- **M3 — Long-Horizon Probe Environment** [HYPOTHESIS]: a multi-turn conversation engine
  that pads the horizon with distractor turns sampled from LMSYS-Chat-1M (the padding
  protocol of [PrefEval, OpenReview:QWunLKbBGF]) and inserts scripted probes every 5
  turns. Each probe is a natural task request whose response is checkable against the
  constraint *without the probe text mentioning the constraint or its topic keywords*
  (anti-reactivity authoring rule). Compliance labeling uses the dual-mode verifier
  taxonomy of [RECAST, OpenReview:90tCp2KszA]: rule-based programmatic checkers wherever
  the constraint permits (format, lexical, refusal-trigger checks) and an LLM judge with
  a 10% human-audit sample only for irreducibly graded soft constraints.
- **M4 — Decay-Curve Fitting & Mechanism Attribution** [HYPOTHESIS]: adherence-over-turns
  modeled as a discrete-time survival process (first sustained violation = event;
  violation-free conversations right-censored), following [TimeToInconsistency,
  OpenReview:88C7vSdn0t]; per-cell decay half-life t½ derived from the fitted hazard. A
  mixed-effects complementary-log-log (discrete hazard) regression — hazard ~ turn ×
  type × wording × position × repetition + (1|constraint-pair) + (1|model) — with the
  soft/hard gap quantified as the type×turn coefficient; mechanism attribution =
  dominance analysis / partial-R² share of that gap coefficient absorbed by each
  manipulated factor and by the M5 prior covariate.
- **M5 — Prior-Strength Proxy Battery** [HYPOTHESIS]: per-constraint covariates for the
  unmanipulable third mechanism: (a) no-injection zero-shot compliance rate (does the
  model already obey the constraint with no statement present?); (b) base-vs-instruct
  compliance delta on the open-weights pair, adapting the aligned-vs-base contrast
  instrument of [SafetyFewTokensDeep, OpenReview:6Mxhg9PtDE] from token depth to
  constraint content; (c) optionally, per-token KL on the constraint-violating
  continuation for open weights. Entered as covariates in M4, never as manipulated
  factors.
- **M6 — Probe-Reactivity Control** [HYPOTHESIS]: a paired measurement design that
  quantifies C2 directly: within-conversation probing (every 5 turns, cheap) versus
  between-conversation probing (each conversation probed exactly once at a randomly
  assigned turn, so earlier probes cannot refresh salience; expensive). The difference
  between the two fitted decay curves is the reactivity estimate, used to correct or
  bound the main M4 estimates — the causal-isolation logic borrowed from [ICFBench,
  OpenReview:hcJywRYc3n]'s paired NoForget/Forget design.

### `challenge_arguments`
- {challenge_id: C1, argument_text: "[HYPOTHESIS] Orthogonally crossing wording strength
  (M1's variants) with position/repetition (M2) on content-matched pairs, while entering
  prior strength as a measured covariate (M5), breaks the natural three-way confound: each
  candidate mechanism gets its own independent source of variance in the M4 model.",
  mechanism_components: [M1, M2, M5]}
- {challenge_id: C2, argument_text: "[HYPOTHESIS] Probes are authored under an
  anti-reactivity rule (no constraint mention or topic keywords, M3), and the residual
  reactivity that authoring cannot remove is *measured* rather than assumed away, via the
  within- vs. between-conversation probing contrast (M6).", mechanism_components: [M3, M6]}
- {challenge_id: C3, argument_text: "[HYPOTHESIS] The pair bank (M1) enforces matching on
  topic, length, and verifier type, and the probe environment (M3) restricts the study to
  constraints with rule-checkable or high-agreement-judgeable compliance criteria — trading
  some ecological breadth of 'soft policy' for unambiguous, non-circular ground truth.",
  mechanism_components: [M1, M3]}
- {challenge_id: C4, argument_text: "[HYPOTHESIS] The proxy battery (M5) triangulates prior
  strength with three imperfect instruments rather than one; this is explicitly a partial
  resolution — prior strength remains a covariate, not a manipulated factor, so its
  attribution share is an upper bound on what correlational adjustment can claim.",
  mechanism_components: [M5]}

### `unaddressed_challenges`
`[C4]` **[HYPOTHESIS]** — the alignment-prior mechanism remains the weakest-instrumented of
the three candidates: M5 proxies it with correlational covariates while M1/M2 genuinely
manipulate framing and salience. Any residual-variance attribution to "prior" is therefore
a diagnosis of exclusion. Per V-08: this unaddressed-challenge claim itself rests on
inferred (not extracted) N5/N6 content, so it is presented at inferred-level confidence.

### Feasibility **[HYPOTHESIS]**
- **Pilot compute/effort:** 2 models × 16 cells × 20 pairs × 3 seeds = 1,920 conversations,
  30 turns each with 6 probes → ~60k assistant calls, ~10⁸ input tokens dominated by
  growing context; API cost class **$10²–10³**; open-weights half runs on 1×A100-80GB in
  ~3–5 days. Engineering: ~2 person-weeks (harness + verifiers). Human effort: verifier
  audit of ~1,200 sampled probe labels ≈ **40–60 annotator-hours**.
- **Scale-up compute/effort:** ~20k conversations (fractional factorial), 100-turn horizon
  → API cost class **$10³–low-10⁴**, or ~2 GPU-weeks on 8×A100 for the open-weights
  models; M6's between-conversation arm alone accounts for ~40% of the budget.
- **Single biggest feasibility risk:** the between-conversation probe design (M6)
  multiplies conversation count by the number of probe points (one conversation per probe
  turn), which is what makes clean, reactivity-free decay curves expensive. **Mitigation:**
  run within-conversation probing everywhere, and deploy the between-conversation design
  only as a calibration subsample on 4 pilot-flagged cells (2 constraint pairs × 6 probe
  turns × 10 seeds ≈ 480 extra conversations); if the measured reactivity delta is small
  and uniform, correct globally rather than redesigning.

**Status:** PARTIAL, `source="inferred"` throughout. `absence_comment`: {`what_missing`:
"No implementation exists; this is a method plan extrapolated from a one-sentence minimal
experiment.", `why_matters`: "The actual method may combine or split these components
differently once implemented (e.g. M6 may prove unaffordable and shrink to a robustness
check).", `implication`: "Use as an implementation starting point with the staged plan as
the go/no-go structure, not a finalized method description."}

---

## N7 — Contributions

| id | text | contribution_type | is_testable | has_rq | source |
|---|---|---|---|---|---|
| CO1 | "[HYPOTHESIS] A factorial ablation framework (matched constraint-pair bank + position/repetition controller + reactivity-controlled long-horizon probe environment) that decomposes the contribution of salience, framing, and alignment-prior strength to differential decay of in-context LLM constraints." | technical_artifact | true | true | HYPOTHESIS |
| CO2 | "[HYPOTHESIS] Quantified attribution of the previously reported ~8x soft/hard constraint decay-rate gap: the share of the gap's variance explained by each of the three candidate mechanisms, with survival-curve half-lives per condition." | empirical_finding | true | true | HYPOTHESIS |
| CO3 | "[HYPOTHESIS] A reusable long-horizon constraint-decay task suite (constraint pairs + probes + verifiers) that can be repurposed to test mitigation strategies (restatement schedules, placement policies, salience-anchoring interventions)." | dataset | true | true | HYPOTHESIS |
| CO4 | "[HYPOTHESIS] Actionable wording/placement/repetition guidance for policy authors, conditional on the attribution result — including the negative form: if the prior mechanism dominates, prompt-level fixes cannot close the gap and durable soft policies require training-time reinforcement." | conceptual_framework | false | true | HYPOTHESIS |

**Status:** PARTIAL, `source="inferred"` for all — these are projected claims a paper
answering the seed's core question would plausibly assert, not verified contributions.
`absence_comment`: {`what_missing`: "No paper text states these as contributions.",
`why_matters`: "A reviewer should treat these as candidate framing, subject to revision once
real findings exist.", `implication`: "Re-derive N7 from the actual Contributions/Intro
paragraph once written."}

---

## N8 — Research Questions

- **RQ1** **[GIVEN]** (near-verbatim restatement of the seed's core question, translated):
  "Is the observed asymmetry between soft-organizational-policy decay and hard-safety-norm
  decay (reported at ~8x) in LLM in-context constraint adherence driven primarily by
  salience, by wording/framing, by pretraining/alignment prior, or by some combination?"
  `rq_source`: "explicit" (given by seed). `evaluates_mechanisms`: [M1, M2, M4, M5].
  `addresses_challenges`: [C1, C4]. `tests_contributions`: [CO1, CO2].
  `answered_by_experiment`: "Stage-1 pilot factorial (type × wording × position ×
  repetition) fitted with the M4 discrete-hazard mixed model and M5 prior covariates;
  mechanism shares via dominance analysis of the type×turn gap coefficient; confirmed on
  the Stage-2 multi-model fractional factorial."
- **RQ_INF_1** **[HYPOTHESIS]**, inferred from the minimal experiment's explicit mention of
  ablating "位置/重复次数" as a route to *separating* mechanisms — the actionable converse:
  "Can experimentally boosting a soft policy's salience and framing to match a hard norm's
  typical presentation (imperative wording, prominent position, high repetition) close the
  soft/hard decay-rate gap, and by how much?" `rq_source`: "inferred".
  `evaluates_mechanisms`: [M1, M2, M3, M4]. `addresses_challenges`: [C1, C3].
  `tests_contributions`: [CO3, CO4]. `answered_by_experiment`: "Contrast of the
  'boosted soft' cell (imperative + head position + repetition 5) against the standard
  soft and standard hard cells: ratio of fitted half-lives with bootstrap CIs."
- **RQ_INF_2** **[HYPOTHESIS]**, inferred from the C2 measurement-validity problem any
  such study must settle first: "Does behavioral probing itself refresh constraint
  salience — i.e. how much of any measured decay curve is an artifact of the measurement
  schedule?" `rq_source`: "inferred". `evaluates_mechanisms`: [M3, M6].
  `addresses_challenges`: [C2]. `tests_contributions`: [CO1].
  `answered_by_experiment`: "Within- vs. between-conversation probing contrast on
  calibration cells (M6); reactivity delta = difference in fitted hazard between the two
  probing regimes at matched turns."

**datasets** `EvalEntityGroup` **[HYPOTHESIS — real, named, fit-checked sources for suite
construction; the assembled suite itself does not yet exist]**: `{names: ["LMSYS-Chat-1M
(distractor-turn padding, following PrefEval's protocol)", "PrefEval (soft
preference-constraint statements and long-context interleaving design)", "OffTopicEval-style
policy-conditioned system prompts (soft operational policies; 21-agent template)", "IFEval
(verifiable, rule-checkable instruction constraints for probe/verifier design)", "HEx-PHI
(hard-norm probe requests, harmful-instruction taxonomy)", "AdvBench (hard-norm probe
requests, secondary)"], source: "inferred"}`
**baselines** **[HYPOTHESIS]**: `{names: ["standard hard-norm condition (reference decay
curve)", "no-manipulation natural-wording soft condition (control)", "naive every-k-turn
verbatim restatement heuristic (mitigation baseline)", "SinkTrack-style training-free
context anchoring [SinkTrack, OpenReview:Gg1aPETCL6] (mechanism-informed mitigation
baseline, open-weights models only, Stage 2)"], source: "inferred"}`
**metrics** **[HYPOTHESIS]**: `{names: ["per-turn adherence rate (fraction of probes at
turn t passing the constraint's verifier)", "decay half-life t½ (turn at which fitted
survival of adherence crosses 50% of its turn-1 value)", "soft/hard hazard ratio (exp of
the type×turn coefficient in the M4 discrete-hazard model)", "mechanism share (dominance
weight / partial R² of each factor in the gap coefficient)", "probe-reactivity delta
(hazard difference, within- vs between-conversation probing)", "verifier validity
(judge–human agreement, Cohen's κ on the 10% audit sample, target ≥0.8)"], source:
"inferred"}`

**Analysis plan [HYPOTHESIS]:** Pilot sample size: 1,920 conversations (960/model), giving
per-cell n=60 conversations and ~11,500 probe outcomes per model — a design target sized
for ≥80% power to detect a hazard-ratio interaction of 1.5 at α=0.05 (to be confirmed by
simulation before running; power claim is itself a hypothesis, not a computed fact).
Primary test: likelihood-ratio tests on the mixed-effects complementary-log-log model
(M4) for the three factor×type×turn interactions; α=0.05 with Holm–Bonferroni correction
across the three mechanism factors; conversation-level random effects guard against
pseudo-replication of probe outcomes within a conversation. Expected effect direction:
soft constraints show larger hazard than hard (gap replication); wording and
position/repetition interactions each significantly *reduce* the type×turn gap
coefficient, with salience+framing jointly absorbing >50% of it; the M5 prior covariate
absorbs a smaller but nonzero share. Robustness: refit with parametric (Weibull) survival
curves; leave-one-constraint-pair-out; per-model-family subgroup fits.

**Status:** PARTIAL. `absence_comment`: {`what_missing`: "RQ_INF_1/RQ_INF_2, the eval
entity groups, and the analysis plan are inferred from a one-sentence minimal experiment
plus the grounded related work — none are stated by any author.", `why_matters`: "The real
study may re-scope RQs (e.g. add cross-model-family generalization as its own RQ) and the
power target must be verified by simulation.", `implication`: "Treat RQ1 as the fixed
anchor (it is the seed's own core question); treat RQ_INF_1/RQ_INF_2, the entity groups,
and the analysis plan as adjustable but pre-registerable scaffolding."}

---

## N9 — Results **[PLACEHOLDER — HYPOTHESIZED DIRECTION ONLY, NO REAL DATA]**

> CRITICAL: no experiment has been run. Every entry below states a predicted direction as a
> falsifiable claim, with `evidence_strength="missing"` and `rq_answered=false`. No numbers
> here are real; the only number that appears (8x) is the seed's given premise.

- **Result 1** (`rq_id`: RQ1): `result_text` (hypothesized direction): "Salience
  (position/repetition) and framing (wording strength) jointly account for the majority of
  the soft/hard decay-rate gap, with the prior-strength covariate (M5) explaining a
  smaller but nonzero residual share." `result_type`: quantitative. `evidence_strength`:
  "missing". `rq_answered`: false.
  **Falsification condition [HYPOTHESIS]:** refuted if, in the M4 dominance analysis, the
  manipulated factors' combined share of the type×turn gap coefficient is below 50% while
  the M5 prior covariate absorbs the majority — i.e. matching a soft policy's presentation
  to a hard norm's still leaves most of the gap standing, implicating the alignment prior
  as the dominant driver.
- **Result 2** (`rq_id`: RQ_INF_1): `result_text` (hypothesized direction): "The
  fully-boosted soft condition (imperative wording, head position, repetition 5)
  substantially narrows — but does not eliminate — the half-life gap with the standard
  hard condition." `result_type`: quantitative. `evidence_strength`: "missing".
  `rq_answered`: false.
  **Falsification condition [HYPOTHESIS]:** refuted in either direction: (a) if the
  boosted-soft half-life is statistically indistinguishable from standard-soft (no
  manipulation effect at all — salience/framing causally inert, prior-only account wins),
  or (b) if boosted-soft fully matches standard-hard (gap closes completely — no
  prior-linked residual exists and CO4's negative guidance clause is falsified).
- **Result 3** (`rq_id`: RQ_INF_2): `result_text` (hypothesized direction): "Within-
  conversation probing yields a measurably slower fitted decay than between-conversation
  probing (probes refresh salience), but the reactivity delta is small relative to the
  soft/hard gap and approximately uniform across constraint types, permitting a global
  correction." `result_type`: quantitative. `evidence_strength`: "missing".
  `rq_answered`: false.
  **Falsification condition [HYPOTHESIS]:** refuted if the reactivity delta differs
  significantly *by constraint type* (interaction of probing regime × type) — in which
  case within-conversation decay curves are differentially biased, the main design cannot
  be globally corrected, and the study must move wholly to the expensive
  between-conversation design before any mechanism claim survives.

**Status:** NOT_FOUND (no experiment run). `absence_comment`: {`what_missing`: "No
quantitative results exist because the paper has not been written or the experiment run.",
`why_matters`: "Any number here would be fabricated and misleading if mistaken for a real
finding.", `implication`: "Use the falsification conditions above as pre-registration-style
decision rules: RQ_INF_2's check gates the validity of everything else, so run the M6
calibration cells first."}

---

## N10 — Threats / Self-Limitations **[HYPOTHESIS — anticipated by this digest, not author-stated]**

| threat_id | category | description | mitigation (planner-proposed, not author-stated) |
|---|---|---|---|
| t1 | construct | "[HYPOTHESIS] 'Adherence' for graded soft policies (tone, scope, style) is operationalized through programmatic verifiers and LLM judges; a judge may not track the policy's intent, and restricting the bank to checkable constraints narrows what 'soft policy' means in this study." | Prefer rule-checkable constraints (IFEval-style) wherever possible; for judged constraints, 10% human audit with Cohen's κ ≥ 0.8 acceptance gate and exclusion of low-agreement pairs; report results separately for rule-verified vs. judge-verified subsets. |
| t2 | internal | "[HYPOTHESIS] Wording-strength variants may inadvertently change semantic content, specificity, or task difficulty alongside framing, so the 'framing' factor could smuggle in a second manipulation." | M1's manipulation checks: embedding-similarity threshold between variants, human semantic-equivalence review, and an independent salience-rating pass; drop pairs whose variants fail equivalence. |
| t3 | internal | "[HYPOTHESIS] Probe insertion itself refreshes constraint salience (C2), inflating measured half-lives, and possibly differentially by constraint type." | Measured directly rather than assumed away: M6 within- vs. between-conversation calibration arm (RQ_INF_2); global correction if uniform, design escalation if type-dependent. |
| t4 | external | "[HYPOTHESIS] Results from 2–6 model snapshots and English-only, text-only, single-agent conversations may not generalize across model families, alignment recipes, languages, or tool-using agent settings — and the salience/framing/prior shares may themselves be model-specific." | Stage-2 coverage of ≥3 families including a base/instruct pair; per-family subgroup estimates reported alongside the pooled model; explicit scope statement excluding multi-agent/tool-use settings. |
| t5 | conclusion | "[HYPOTHESIS] A 4-factor factorial with survival-curve fitting invites many researcher degrees of freedom (link function, censoring horizon, half-life definition) and multiple-comparison inflation." | Pre-registered model specification and factor set before Stage 2; Holm–Bonferroni across the three mechanism-factor tests; Weibull refit and leave-one-pair-out reported as sensitivity analyses; all cells reported, not only significant ones. |
| t6 | reproducibility | "[HYPOTHESIS] Hosted-API models update silently; the exact decay-rate numbers may be non-reproducible even with identical prompts and seeds." | Pin dated model versions and log raw transcripts; include at least one fully open-weights model whose results anchor replication; release the suite (CO3) so drift itself is re-measurable. |

**Status:** NOT_FOUND (no author-written Threats/Limitations section exists — these are
this digest's anticipated threats with planner-proposed mitigations, not extracted
author-acknowledged ones; per the N10 extraction rule they could not populate a real
digest's N10). `absence_comment`: {`what_missing`: "No paper exists to author-state its own
threats to validity.", `why_matters`: "Per N10's rule, only author-acknowledged limitations
belong in a real digest's N10; everything above is planner-anticipated and must not be
cited as if the paper conceded it.", `implication`: "Re-derive N10 from the real paper's
own Limitations section once written; until then use this table as the pre-writing
checklist of concerns to preempt — t3 gates the design and should be resolved first."}

---

## N11 — Artifacts

**Node fields:** `artifacts: []`, `has_code: false`, `has_data: false`, `has_model: false`
— all **[PLACEHOLDER]**.

**Status:** NOT_FOUND. `absence_comment`: {`what_missing`: "No code, dataset, model, or demo
has been released because the paper and its experiments do not yet exist (the planned
releases would be the M1 pair bank, M2/M3 harness, and probe/verifier suite of CO3).",
`why_matters`: "A reviewer relying on this digest should not assume any reusable artifact is
available for inspection or replication.", `implication`: "Revisit N11 once (if) the study
is implemented and artifacts are released; until then, treat T3.2 as pure planning
scaffolding."}

---

## N12 — Contribution Type

- `value`: **`empirical`** **[HYPOTHESIS]**
- `rationale` **[HYPOTHESIS]**: "The core question is a mechanism-attribution question
  about an existing phenomenon (the ~8x soft/hard decay-rate gap the seed takes as given),
  and the projected N9 results that would validate the paper are measurement findings —
  variance shares and half-life contrasts — not a released benchmark or trained system.
  This matches the exemplar precedent directly: both 'LLMs Get Lost in Multi-Turn
  Conversation' and 'Safety Alignment Should Be Made More Than Just a Few Tokens Deep'
  are classified `empirical` even though each ships a substantial constructed apparatus
  (sharded-simulation environment; per-token diagnostic + two mitigations), because the
  apparatus exists to substantiate the central empirical claim. Here likewise the pair
  bank and probe suite (M1–M3, CO3) are instrumental to answering RQ1. Re-classification
  to `benchmark` becomes correct only if the released suite, rather than the mechanism
  finding, ends up as the headline contribution."

**Status:** PARTIAL (best-fit judgment call absent real N9 results to confirm against).
`absence_comment`: {`what_missing`: "N12 is decided from projected results, not real ones.",
`why_matters`: "If the eventual paper's main contribution shifts toward 'we release suite X'
rather than 'we found mechanism Y dominates,' the correct classification shifts from
`empirical` to `benchmark`.", `implication`: "Re-check N12 once real N9 results exist."}

---

## Claims

1. **[GIVEN]** "The decay of organizational soft policies is far greater than hard safety
   norms — the original paper reports approximately an 8x difference." `evidence`:
   [{type: "citation", text: "原论文报告约 8 倍差异", source: "GIVEN", location: {section:
   "README core question / 核心问题"}}]. This is the seed-level premise the whole study
   exists to explain; not itself a claim of the (nonexistent) T3.2 paper. Reviewer note:
   the study must first *replicate* this gap directionally (Stage-1 success criterion)
   before decomposing it — if the gap does not replicate in the matched-pair design, the
   premise, not the mechanism, is what needs investigating.
2. **[HYPOTHESIS]** "Salience, framing, and pretraining/alignment prior are the three
   candidate mechanisms sufficient to explain the soft/hard decay-rate gap; no fourth
   mechanism is required." `evidence`: [{type: "argument", text: "derived directly from the
   seed's own three-way disambiguation in the core question", source: "HYPOTHESIS",
   location: {section: "N1/N5 above"}}]. Contestable: plausible omitted mechanisms include
   constraint-interference between co-present policies, and distractor-content interference
   of the kind [ICFBench, OpenReview:hcJywRYc3n] shows can disrupt later retrieval; the M4
   residual term is where such omissions would surface.
3. **[HYPOTHESIS]** "Content-matched soft/hard constraint pairs (M1) make the type contrast
   interpretable — the pairs differ in type, not in difficulty or checkability."
   `evidence`: [{type: "argument", text: "matching on topic, length, and verifier type per
   C3", source: "HYPOTHESIS", location: {section: "N5-C3 / N6-M1 above"}}]. This is the
   construct-validity linchpin (threat t1/t2); if matching fails, every downstream
   attribution is confounded — the single highest-value target for a skeptical reviewer.
4. **[PLACEHOLDER]** "Boosting a soft policy's salience and framing to match a hard norm's
   typical presentation will substantially close (though not eliminate) the decay-rate
   gap." No evidence yet — this is the Result-1/Result-2 predicted direction in N9, with
   symmetric falsification conditions stated there; the most reviewer-contestable empirical
   claim the eventual paper would make, and the one CO4's guidance depends on.
5. **[HYPOTHESIS]** "The long-horizon probe environment (M3) can measure constraint decay
   without the probes themselves refreshing constraint salience — or at least with a
   reactivity bias that is measurable and type-uniform (M6)." `evidence`: [{type:
   "argument", text: "anti-reactivity probe authoring rule plus within-/between-conversation
   calibration contrast", source: "HYPOTHESIS", location: {section: "N6-M3/M6, N8-RQ_INF_2
   above"}}]. If false in the type-dependent way (Result 3's falsification condition), the
   entire within-conversation design is invalid — this is why RQ_INF_2 is sequenced first.
