# Digest: Recommending Ghosts: Registry-Grounded Gating of Hallucinated Skill/Tool Calls in Live Agent Trajectories

> **REVERSE-DIGEST NOTICE.** No paper exists yet. This is speculative scaffolding for research
> planning, built from a seed idea (topic code B1.6) as if a paper answering the seed's core
> question had already been written. Every field below is tagged inline:
> **[GIVEN]** = verbatim/near-verbatim from the seed README; **[HYPOTHESIS]** = reasoned
> elaboration / prediction, not a fact; **[PLACEHOLDER]** = genuinely unknowable until the work
> is actually done (never invented); **[GROUNDED:corpus]** = a REAL paper retrieved from the
> local OpenReview corpus (`topics/corpus/ideas.jsonl`), with its approach_summary grounded in
> that paper's own motivation/method text; **[GROUNDED:arxiv-mined]** = a REAL, very recent arXiv
> paper found via `arxiv_corpus`'s mined 6-month priority report — its existence, arXiv id, and
> the numbers shown in its mined method table are real, but this digest has **not read its full
> text**, only a scraped summary table, so any claim about what it does or does not cover beyond
> that table is marked UNVERIFIED and must be checked before the real paper is written. Do not
> cite any [HYPOTHESIS] or [PLACEHOLDER] content as if it were a real finding, and do not cite
> the [GROUNDED:arxiv-mined] paper's *scope* beyond what its mined table actually shows.

---

## Freshness note — UPDATED, full paper now read (2026-08-13)

**Verdict: the topic survives, but is substantially reframed. Read on before using anything
below this note.**

The real paper is **Weifeng Yuan, Wenbo Guo, Feng Dong, Haoyu Wang, Yang Liu, "Skills That Don't
Exist: A Large-Scale Study of Hallucinated Skill Recommendation in LLM Agents"**
(arXiv:2607.12340). It is not a general reliability study — it is a **supply-chain security
paper**. Its own framing: agents that hallucinate a plausible-but-nonexistent skill name create
an exploitable *attack precondition*, because an adversary can observe which fake names agents
reliably produce, pre-register real (malicious) skills under those exact names on open registries
that "rarely verify publishers," and wait for a victim's agent to recommend-and-auto-install the
trap. This is squatting, not noise.

**What the paper actually measures (confirmed by reading it, not inferring from a table):**
- **RQ1 Prevalence**: 15,000 prompts × 12 configurations (4 standalone LLMs incl. Claude Sonnet
  4.6, GPT-5.4-mini, GLM-4.5-Air, Claude Opus 4.7, plus open-weight models; 8 agent harnesses
  incl. Claude Code, OpenClaw, OpenCode, Codex). Hallucination rate averages 36.0%
  (standalone) / 36.9% (agents), rising to 43.1% on real developer questions; **every single
  configuration hallucinates**; 5,669 distinct hallucinated names were produced in total.
- **RQ2 Targetability**: the same fake names recur across prompts and models — i.e., they are
  *predictable*, which is what makes pre-registration-then-wait a viable, low-effort attack.
- **RQ3 Detectability**: neither the generating model itself nor a same-/cross-model judge can
  tell real from hallucinated names better than chance (51%/53% balanced accuracy — a coin
  flip); edit-distance filters also fail.
- **RQ4 Mitigation** (four defenses, all applied at the **recommendation** step, i.e. constraining
  what the LLM is allowed to say): retrieval-grounding cuts hallucination 40.8% → 3.2% but
  collapses usefulness to ~16% correct-skill recommendation; self-refinement only reaches 33.2%
  (mostly by refusing to answer); cross-model voting eliminates 92.8% of hallucinations but keeps
  only 44.8% of real skills. **Every tested defense buys security by destroying usability** — the
  paper's own headline tension.
- A single **proof-of-concept** confirms the attack is executable end-to-end (a benign placeholder
  skill was pre-registered under a name Claude Code reliably hallucinates, and the agent found and
  auto-installed it in a sandbox) — but this is one demo, not a systematic study.

**What the paper explicitly does NOT do (confirmed, not inferred):**
- No multi-step/multi-turn trajectory study with a downstream task outcome — only the one
  install-path demo above.
- No detection-timing/lag measurement and no recovery-cost measurement of any kind.
- No systematic false-positive/near-miss study: the paper's own limitations section states
  "our recall analysis covers only the four open weight models used for mitigation, so we defer
  the full false-negative study across all 12 configurations" — an explicit, self-acknowledged
  gap, not this digest's inference.
- No end-to-end malicious-payload or user-behavior study ("Measuring whether real users install
  such recommendations requires a controlled user study" — stated as future work).
- The paper's own stated needed fix is ecosystem-level and unbuilt: "registry-level name
  reservations and verified recommendation pipelines."

**The one important correction this reading forces on the original topic sketch:** a bare
*existence* check (does this name appear in the registry?) is **not a valid defense against the
paper's own attack model**, because the whole point of squatting is that the attacker *does*
register the hallucinated name — so by the time a victim's agent recommends it, "exists in the
registry" is true and a naive existence gate would wave the malicious skill straight through.
The only mechanism that survives contact with the paper's threat model is a **publisher-trust /
provenance gate** (does this skill come from a verified or previously-trusted publisher, not
merely "does a skill by this name exist somewhere") — which is exactly what the paper's own
closing sentence calls for ("verified recommendation pipelines") but never builds or tests. This
digest is revised throughout to gate on **trust tier**, not bare existence, and to place the gate
at **install/execution time**, a different intervention point than all four of the paper's own
recommendation-time defenses — which is also why it might sidestep the security/usability
collapse the paper documents: it doesn't need to touch what the LLM is allowed to say at all, so
a correctly-named real skill from an unverified publisher is a separate signal from a
hallucinated name, and both can be distinguished from a verified-publisher skill without
constraining recommendation diversity.

---

## N0 Metadata

- **title** [GIVEN]: "Recommending Ghosts: Registry-Grounded Gating of Hallucinated Skill/Tool
  Calls in Live Agent Trajectories" (seed README, English gloss line under B1.6)
- **authors** [PLACEHOLDER]: `["Anonymous"]` — no paper, no authors exist yet.
- **abstract** [HYPOTHESIS] (drafted, not real — synthesized from the seed's core question +
  minimal experiment; explicitly a draft):
  > "Recent large-scale measurements show LLM agents recommend or invoke tools and skills that do
  > not exist at rates from roughly 6% to 51%, depending on model and harness. We ask a
  > downstream question that a single-shot measurement cannot answer: in a live, multi-step agent
  > trajectory, can a cheap pre-execution check against the agent's real tool/skill registry
  > intercept a hallucinated recommendation before it derails the task, and does *when* it is
  > caught matter? We embed single-turn hallucination-prone recommendation moments inside longer
  > agent trajectories, instrument a registry-existence gate that runs before each tool
  > invocation, and compare gate-on and gate-off arms on downstream task success, the number of
  > steps consumed before a hallucination is caught (by the gate or by organic task failure), the
  > recovery cost once caught, and the gate's false-positive rate against real-but-unfamiliar
  > tool names. We report whether registry grounding is a cheap, sufficient first line of defense
  > or whether it merely shifts the failure mode toward more plausible near-miss names."
- **doi** [PLACEHOLDER]: `null`
- **arxiv_id** [PLACEHOLDER]: `null`
- **num_pages** [PLACEHOLDER]: `null`
- **research_area** [HYPOTHESIS]: `"AI/ML"` primary lens (agent evaluation/intervention
  methodology); secondary case for `"SE"` given the tool/API-registry framing (matches
  2607.12340's own cs.SE categorization) and for `"Security"` given the near-miss/typosquatting
  angle in C4 below.

**Status:** PARTIAL — `authors`/`abstract` are placeholder/hypothesis only.
**absence_comment:** {"what_missing": "No actual paper, author list, or printed abstract exists for this topic yet.", "why_matters": "Any bibliographic claim made from this digest would be fabricated if presented as fact.", "implication": "Treat N0 purely as a planning placeholder; re-derive it from the real paper once written, and only after the Freshness note's required check of arXiv:2607.12340 has been done."}

---

## N1 Problem Formulation

- **objective** [HYPOTHESIS] (built from the core question, revised post-reading): "measure,
  inside constructed multi-step agent trajectories that embed a skill-name-hallucination moment
  modeled on the confirmed 36-43% prevalence and high name-recurrence [HallucSkills,
  arXiv:2607.12340] reports, whether an install/execution-time **publisher-trust gate** (not a
  bare existence check, which the squatting threat model defeats by construction) reduces
  successful-compromise rate and downstream task disruption relative to no gate and relative to
  the paper's own recommendation-time defenses, as a function of how early in the trajectory the
  untrusted skill is caught — producing a detection-timing-to-outcome curve plus a
  security/usability tradeoff point directly comparable to the paper's own reported RAG (3.2%
  hallucination / ~16% recall) and voting (7.2% hallucination / 44.8% recall) operating points."
  - Self-check: kind of task = intervention evaluation at a different pipeline stage than an
    already-published paper's four tested defenses; domain = LLM agents that install/invoke
    skills from open, publisher-unverified registries; outcome shape = a security/usability
    Pareto point plus a detection-timing-to-cost curve. All three dimensions land, and the
    comparison to real, already-published operating points gives this topic a concrete bar to
    clear or miss.
- **inputs** [HYPOTHESIS]:
  1. A registry snapshot annotated with **publisher-trust tier** (verified publisher,
     known/previously-seen publisher, unknown/anonymous publisher) — not merely a name-existence
     list, because existence alone is satisfied by a squatted malicious skill.
  2. A multi-step agent trajectory harness in which a skill-recommendation-and-install decision
     (modeled on [HallucSkills, arXiv:2607.12340]'s own two settings: standalone-LLM
     recommendation, and agent-harness recommend-then-install) is one step inside a longer task
     with its own real downstream outcome.
  3. A trust-tier gate: a function from (recommended skill name, registry-with-trust-tier
     snapshot) to {install-allowed, install-blocked, human-review-flagged}.
  4. A realistic adversary model built directly from the paper's own RQ2 finding: since
     hallucinated names *recur* across prompts/models, an attacker can plausibly pre-register a
     subset of the paper's own reported 5,669 hallucinated names (or names elicited the same way)
     under an unverified publisher identity — the squatted-skill simulation should use this
     recurrence property, not arbitrary malicious names, to stay faithful to the demonstrated
     attack.
  5. A set of legitimate-but-unverified-publisher probes (real, useful skills published by
     first-time/independent authors) to measure the trust gate's usability cost — the paper's own
     finding that every tested defense collapses usefulness makes this the central risk to test.
- **outputs** [HYPOTHESIS]:
  1. Per-episode labels: was the recommended name a hallucination (per the paper's own
     conservative registry+GitHub matching definition), was it squatted (present under an
     unverified publisher) or absent entirely, gate verdict, ground-truth task/security outcome.
  2. Detection-lag: the step index at which an untrusted/squatted install is first caught (by the
     gate, immediately; or, gate-off, by whatever the trajectory's organic failure signal is —
     which may never fire, since a successfully installed malicious skill can silently look like
     task success, unlike the pure-noise hallucinations the base paper studies).
  3. Security/usability operating point: compromise-block rate vs. legitimate-unverified-publisher
     rejection rate, reported so it can be plotted against the paper's own four reported points.
  4. Recovery cost: extra steps/tokens/tool-calls needed to complete the task after a blocked or
     caught install, gate-on vs. gate-off.
- **constraints** [GIVEN/CONFIRMED] (revised from the seed after reading the full paper): the
  confirmed 36.0%-43.1% average hallucination-rate range and the confirmed name-recurrence
  property (RQ2) must be used as the basis for constructing a realistic squatting simulation,
  rather than an arbitrary or worst-case adversary; the gate must be evaluated against the
  confirmed fact that self-model and cross-model auditing are coin-flip-level (RQ3) — i.e., the
  gate cannot rely on asking any LLM whether a name "looks real," only on registry/provenance
  metadata; ground truth for "was this a successful compromise" is a static, pre-committed
  trust-tier snapshot plus environment execution state, not a model judgment.

**Status:** PARTIAL (objective/inputs/outputs inferred; constraints now confirmed against the
full paper rather than a scraped table).
**absence_comment:** {"what_missing": "There is no written Problem Formulation section to extract from — this is reconstructed from the seed plus a fully-read real paper.", "why_matters": "A reviewer could still reasonably scope the trajectory harness differently, or argue the install-time trust-gate idea is itself an obvious enough extension of the paper's closing sentence that it needs a stronger differentiator before being paper-shaped.", "implication": "Treat inputs/outputs/objective as the most conservative reading consistent with the now-confirmed paper; the remaining open risk is novelty margin, not factual accuracy about what the base paper covers."}

---

## N2 Motivation

**motivations:**
- **motivation_text** [GROUNDED:arxiv-read]: "A just-published security study [HallucSkills,
  arXiv:2607.12340] establishes, at large scale (15,000 prompts, 12 configurations), that every
  tested LLM/agent configuration hallucinates skill names (36.0%-43.1% average rate), that these
  names recur predictably enough to be reliable attack targets (RQ2), that neither the model
  itself nor a cross-model judge can flag them better than chance (RQ3, 51-53% balanced
  accuracy), and that every one of its four tested defenses — all applied at the recommendation
  step — buys a hallucination-rate reduction only by destroying usefulness (best case: 3.2%
  hallucination but only ~16% correct-skill recall). The paper's own words frame the fix as
  needing 'ecosystem-wide structural changes: registry-level name reservations and verified
  recommendation pipelines' — and explicitly stops short of building or testing either. This is
  not a gap this digest infers; it is the paper's own stated closing position."
- **motivation_text** [HYPOTHESIS, building on the confirmed gap]: "The paper's four defenses
  share one structural property worth questioning: all of them intervene on what the LLM is
  allowed to *say* (retrieval-constrained generation, self-refinement, cross-model voting), which
  is exactly why they collapse recall — a real, useful, but training-distribution-atypical skill
  name looks the same to these filters as a hallucinated one. A defense placed one step later, at
  *install/execution time*, does not need to touch the recommendation distribution at all: it
  only needs to know whether the specific name about to be installed comes from a verified
  publisher. This reframes the problem from 'stop the model from saying fake names' (recall-costly
  by the paper's own numbers) to 'stop the agent from acting on an unverified name regardless of
  who said it or why' — a different point in the pipeline that the paper never evaluates."
- **motivation_text** [HYPOTHESIS]: "A **bare existence check is not this defense**, because the
  paper's own threat model is squatting: an attacker who observes a recurring hallucinated name
  (RQ2) can pre-register it, at which point 'does this name exist in the registry' becomes true
  for the malicious skill. The gate must check *publisher trust tier*, not name existence — which
  is a materially different verifier design than the seed's original 'registry-grounding' framing
  assumed, and is the central correction this topic's freshness check produced (see the
  Freshness note)."
- **motivation_text** [HYPOTHESIS]: "The tool-use literature already treats grounding proposed
  actions in real, executable resources as a standard fix for brittleness: [ToolLLM,
  OpenReview:dHng2O0Jjr] trains on real, executable API interactions because simulated tool
  environments do not transfer; [Themis, OpenReview:d94x0gWTUX] has a reward model invoke real
  tools mid-evaluation rather than trust an internally generated judgment. But neither treats
  *provenance of the proposed resource* as something to verify — they assume the tool set is
  fixed, known, and trustworthy by construction, which is exactly the assumption
  [HallucSkills, arXiv:2607.12340] shows is false for open skill registries. [FuncMasking,
  OpenReview:yVQcr4qjD6]'s finding — that models shortcut on names rather than grounding in
  semantics — is a second, independent reason to distrust any gate built on name-similarity
  rather than a hard provenance signal."
  - source: HYPOTHESIS (stakes framing) anchored to the now fully-read real paper and real corpus
    papers; location: `{seed_locator: "README core question + minimal experiment, revised"}`.

**Status:** PARTIAL — motivation now anchored to a fully-read real paper rather than a scraped
table; the pipeline-stage/install-time argument and the trust-tier correction are this digest's
reasoning, not the base paper's own stated framing (it does not propose or evaluate either).
**absence_comment:** {"what_missing": "No paper-level Motivation section exists for this unwritten topic; the base paper's own motivation/findings are now grounded, but the argument for *why an install-time trust gate specifically* is the right next step is this digest's inference.", "why_matters": "A reviewer could argue that a provenance/trust-tier gate is such a direct reading of the base paper's own closing sentence that it needs sharper differentiation (e.g., a specific mechanism design or a specific measured tradeoff) to count as a distinct contribution rather than 'building what they said should exist'.", "implication": "The strongest version of this topic should lead with the concrete, comparable-to-published-numbers security/usability tradeoff (N8's RQ1) rather than the trust-tier idea alone, since the idea itself is a fairly direct implication of the base paper."}

---

## N3 Related Works

Search protocol actually run for this revision: (1) located the real mined arXiv entry for
"Skills That Don't Exist" (arXiv:2607.12340) inside `arxiv_corpus/arxiv_ideaseed_6m_priority.md`,
then fetched and read the full paper (abstract page + full HTML text) on 2026-08-13 — see the
Freshness note for what changed once the full text (not just the mined table) was available;
(2) a keyword-scored search over `topics/corpus/ideas.jsonl` (11,683 OpenReview records,
`domain=="ml"` subset), matching five term groups — tool-existence-hallucination language,
tool/function-call language, multi-step agent-trajectory language, retrieval/grounding language,
and verifier/gate/registry language — which surfaced 685 candidates scoring ≥2 group-matches;
(3) the top ~15 candidates by match count were read in full (motivation + method text) before
selection. Nine works are retained below: one real, fully-read, non-corpus arXiv paper (the
central empirical baseline, whose threat model this topic now directly targets) and eight
[GROUNDED:corpus] OpenReview papers.

**works:**

1. **citation_key**: `[HallucSkills, Yuan et al., arXiv:2607.12340]` — [GROUNDED:arxiv-read; full
   text read 2026-08-13]
   **approach_summary**: "Frames LLM/agent skill-name hallucination as a supply-chain attack
   precondition: an adversary can pre-register real (malicious) skills under names agents
   reliably hallucinate, then wait for a victim's agent to recommend-and-install the trap. Runs
   the first large-scale measurement (15,000 prompts, 12 configurations: 4 standalone LLMs + 8
   agent harnesses) across four RQs — prevalence (36.0%-43.1% hallucination rate, every
   configuration affected), targetability (hallucinated names recur predictably across
   prompts/models), detectability (self- and cross-model auditing is coin-flip-level, 51-53%
   balanced accuracy; edit-distance filters also fail), and mitigation (four recommendation-time
   defenses — retrieval grounding, self-refinement, cross-model voting, and their combination —
   each trading hallucination reduction for severe usability loss, e.g. retrieval grounding:
   40.8%→3.2% hallucination but only ~16% correct-skill recall). Includes one benign
   proof-of-concept confirming the full attack path (hallucination → pre-registration →
   recommend-and-auto-install) executes in a sandboxed Claude Code instance."
   **paper_url**: https://arxiv.org/abs/2607.12340
2. **citation_key**: `[ToolLLM, OpenReview:dHng2O0Jjr]` — [GROUNDED:corpus]
   **approach_summary**: "Trains open-source LLMs on a large-scale, executable, real-world
   RESTful-API dataset (16,000+ APIs) with explicit multi-step solution-path annotation and a
   depth-first multi-path decision process designed to mitigate error propagation from an early
   mistake — motivated by prior tool-use benchmarks' reliance on small, synthetic, single-tool
   scenarios that fail to generalize to realistic multi-step interaction."
   **paper_url**: https://openreview.net/forum?id=dHng2O0Jjr
3. **citation_key**: `[FuncMasking, OpenReview:yVQcr4qjD6]` — [GROUNDED:corpus]
   **approach_summary**: "Shows on-device function-calling models over-rely on function/parameter
   *names* as shortcuts rather than grounding selection in semantic descriptions, causing sharp
   accuracy collapse under naming-distribution shift; fixes this via name/parameter masking plus
   an irrelevance-augmented dataset that trains the model to abstain when no real function
   applies."
   **paper_url**: https://openreview.net/forum?id=yVQcr4qjD6
4. **citation_key**: `[AgenTracer, OpenReview:l05DseqvuD]` — [GROUNDED:corpus]
   **approach_summary**: "Localizes the earliest decisive error step in a failed multi-agent
   trajectory via counterfactual replay — substituting a minimally corrected action at each step
   and finding the earliest substitution that flips the outcome to success — then trains a
   reinforcement-learned tracer on this synthetically generated supervision to predict the
   responsible agent/step at scale, motivated by the data-scarcity and weak-judge limits of prior
   failure-attribution work."
   **paper_url**: https://openreview.net/forum?id=l05DseqvuD
5. **citation_key**: `[SelfEvolvingAgentBench, OpenReview:2H03gm4Rq6]` — [GROUNDED:corpus]
   **approach_summary**: "Builds harder agent-benchmark tasks by having an agent explore an
   environment at test time, treating a successful, reproducible trajectory as evidence a task is
   solvable, then converting that trajectory into a new verification-guaranteed benchmark item —
   a trajectory-centered construction method motivated by static benchmarks saturating as
   capability improves."
   **paper_url**: https://openreview.net/forum?id=2H03gm4Rq6
6. **citation_key**: `[SelfRAG, OpenReview:hSyW5go0v8]` — [GROUNDED:corpus]
   **approach_summary**: "Trains a single LM to emit learned reflection tokens that decide
   on-demand whether retrieval is needed and then critique whether generated claims are actually
   supported by the retrieved evidence, internalizing retrieval-control and self-verification
   end-to-end rather than relying on external confidence estimators or post-hoc verification
   passes."
   **paper_url**: https://openreview.net/forum?id=hSyW5go0v8
7. **citation_key**: `[Themis, OpenReview:d94x0gWTUX]` — [GROUNDED:corpus]
   **approach_summary**: "Proposes a tool-augmented reward model (Themis) that follows a
   ReAct-style thought-action-observation trajectory and invokes real external tools (search,
   calculator, code interpreter) before producing a scalar preference score, motivated by static
   reward models failing in exactly the regimes where the base policy fails (unverified facts,
   arithmetic, code)."
   **paper_url**: https://openreview.net/forum?id=d94x0gWTUX
8. **citation_key**: `[GenArtist, OpenReview:Ur00BNk1v2]` — [GROUNDED:corpus]
   **approach_summary**: "Separates reasoning/verification from execution in a multimodal-LLM
   image-generation-and-editing agent: actions are organized into a tree with sibling
   alternatives, each node is verified, and the agent backtracks to an alternative when a
   verification check fails, rather than continuing down a linear pipeline after an error."
   **paper_url**: https://openreview.net/forum?id=Ur00BNk1v2
9. **citation_key**: `[ToolACE-MT, OpenReview:KznJt9Fhjc]` — [GROUNDED:corpus]
   **approach_summary**: "Synthesizes multi-turn tool-use dialogue data via a non-autoregressive
   pipeline — coarse trajectory skeleton, iterative masked refinement, then an explicit offline
   verification stage — replacing costly online multi-agent simulation while retaining a
   dedicated quality/verification safeguard over the generated tool-call trajectories."
   **paper_url**: https://openreview.net/forum?id=KznJt9Fhjc

**Status:** PARTIAL — all eight corpus works are real with grounded approach_summaries; the
arXiv work is real with a grounded *table* but an unread full text (see Freshness note); the
mapping of all nine onto this future paper's framing is this digest's judgment.
**absence_comment:** {"what_missing": "No authored Related Work section exists. Classic non-corpus/non-mined anchors for tool-use hallucination (e.g., Gorilla, API-Bank, ToolBench's own follow-ups) are absent because they were not surfaced by this corpus's keyword search or the arXiv mining pass; a real literature search would likely find more direct precedents.", "why_matters": "The single most load-bearing related work (arXiv:2607.12340) has not been read in full; every limitation claim made against it in N4 is provisional.", "implication": "Before drafting the real paper: (1) read arXiv:2607.12340 in full, (2) run a targeted DBLP/arXiv search for 'tool hallucination detection', 'API existence verification', 'typosquatting tool names LLM agent' to find anchors this corpus-limited search could not surface."}

---

## N4 Prior Limitations

**limitations:**
1. **limitation_text** [GROUNDED:arxiv-read — confirmed against the full paper]: "[HallucSkills,
   Yuan et al., arXiv:2607.12340] measures hallucination at the level of individual recommendation
   events and validates only one end-to-end install path as a single proof-of-concept demo — not
   a systematic multi-step trajectory study with a downstream task outcome. It measures no
   detection-timing/lag and no recovery cost. All four of its tested defenses act on the
   recommendation step (constrain what the LLM says), none on the install/execution step (gate
   what the agent is allowed to act on regardless of what was said). Its own limitations section
   explicitly defers 'the full false-negative study across all 12 configurations' and states that
   measuring real user installation behavior 'requires a controlled user study' it did not run.
   These are the paper's own admitted gaps, not this digest's inference — confirmed by reading the
   full text on 2026-08-13."
   **affects_works**: ["[HallucSkills, Yuan et al., arXiv:2607.12340]"]
   **limitation_type**: "generalizability"
2. **limitation_text** [HYPOTHESIS]: "[ToolLLM, OpenReview:dHng2O0Jjr]'s depth-first multi-path
   decision process is explicitly designed to mitigate error propagation from an early mistake,
   but its evaluation targets task success on a fixed, known API set — it does not instrument or
   report *when*, within a trajectory, an erroneous (let alone hallucinated-nonexistent) tool
   choice is made, nor how that timing relates to recoverability."
   **affects_works**: ["[ToolLLM, OpenReview:dHng2O0Jjr]"]
   **limitation_type**: "generalizability"
3. **limitation_text** [HYPOTHESIS]: "[FuncMasking, OpenReview:yVQcr4qjD6] demonstrates that
   models over-rely on function names as shortcuts and trains the *policy* to abstain when no
   real function applies, but it operates entirely within a known, fixed function set — it never
   tests the harder existence question this topic requires (is the named function real at all),
   and it does not evaluate an external gate/verifier layered on top of the policy, only the
   policy's own internal robustness."
   **affects_works**: ["[FuncMasking, OpenReview:yVQcr4qjD6]"]
   **limitation_type**: "generalizability"
4. **limitation_text** [HYPOTHESIS]: "[AgenTracer, OpenReview:l05DseqvuD]'s counterfactual-replay
   attribution method is the closest precedent for measuring how an early error causally affects
   a later outcome, but it is built and evaluated for *general* multi-agent role/step errors, not
   specifically for a tool/skill-existence hallucination, and it does not evaluate a live,
   pre-execution intervention gate — it only diagnoses failures after a full trajectory has
   already run to completion or failure."
   **affects_works**: ["[AgenTracer, OpenReview:l05DseqvuD]"]
   **limitation_type**: "generalizability"
5. **limitation_text** [HYPOTHESIS]: "[SelfRAG, OpenReview:hSyW5go0v8] internalizes an on-demand
   'should I check something external' decision via learned reflection tokens, which is
   conceptually the closest existing mechanism to a registry-grounding gate — but it is built and
   evaluated for factual-claim retrieval and support-critique in generation, not for tool/skill
   *existence* verification against a discrete, versioned registry, and it requires retraining
   the base model rather than being a drop-in pre-execution check."
   **affects_works**: ["[SelfRAG, OpenReview:hSyW5go0v8]"]
   **limitation_type**: "generalizability"
6. **limitation_text** [HYPOTHESIS]: "[Themis, OpenReview:d94x0gWTUX] has a reward model invoke
   real tools to verify facts before scoring, but it assumes the tools *it* invokes are real and
   available by construction (they are the evaluator's own toolset) — it never asks whether the
   *policy being evaluated* proposed a tool that does not exist, which is the object-level
   question this topic targets."
   **affects_works**: ["[Themis, OpenReview:d94x0gWTUX]"]
   **limitation_type**: "generalizability"
7. **limitation_text** [HYPOTHESIS]: "[GenArtist, OpenReview:Ur00BNk1v2]'s tree-structured
   planning with per-node verification and backtracking is the closest existing architectural
   precedent for 'catch the failure early and recover' — but its verification checks visual/task
   quality of an image-generation step, not the existence of a proposed tool/skill against a
   registry, and its backtracking cost is not measured as a function of how early the failing
   node is detected."
   **affects_works**: ["[GenArtist, OpenReview:Ur00BNk1v2]"]
   **limitation_type**: "generalizability"
8. **limitation_text** [HYPOTHESIS]: "[ToolACE-MT, OpenReview:KznJt9Fhjc]'s offline verification
   stage checks that *synthesized training data* trajectories are well-formed and coherent before
   they are used for training — it is a data-quality gate applied once, offline, to generated
   data, not a live, per-step gate applied to a deployed agent's real-time tool proposals during
   task execution."
   **affects_works**: ["[ToolACE-MT, OpenReview:KznJt9Fhjc]"]
   **limitation_type**: "other"

**grounding_check**: `true` — every limitation cites at least one `affects_works` entry whose
string form exactly matches an N3 `citation_key`.

**Status:** PARTIAL — limitations 2-8 are this digest's inferences about what those works'
methods demonstrably do not cover; limitation 1 (against the actual method twin) is now
confirmed against the full read text, including verbatim-sourced admissions from the base
paper's own limitations section, not inferred from a scraped table.
**absence_comment:** {"what_missing": "None of works 2-8 states these limitations about itself; each is derived from what the work's method text covers versus what B1.6's core question requires. Limitation 1 is the exception — it is now grounded in the base paper's own text.", "why_matters": "With limitation 1 confirmed, the topic's remaining risk shifts from 'does the gap exist' (yes) to 'is an install-time trust gate a strong enough contribution on top of that gap, or too direct a reading of the base paper's own closing sentence' (open, see N2's absence_comment).", "implication": "Treat limitations 2-8 as still-provisional corpus-based reasoning; limitation 1 can be cited as confirmed once this topic is written up for real."}

---

## N5 Challenges

**challenges:**
- **C1** [HYPOTHESIS, revised post-reading]: "The squatting race condition: [HallucSkills,
  arXiv:2607.12340]'s own threat model means an attacker can register a hallucinated name *before*
  a defender's gate ever sees it, at which point bare existence is true for the malicious skill.
  The registry snapshot must therefore carry publisher-trust metadata (verified / known / unknown
  publisher, registration recency), not just a name list — and the simulation must model an
  adversary that pre-registers under an unverified identity, matching the paper's own
  proof-of-concept, rather than assuming trust tiers are unavailable or unforgeable."
- **C2** [HYPOTHESIS, sharpened by the confirmed RQ3 finding that self-/cross-model auditing is
  coin-flip-level]: "Because no LLM judgment can be trusted to separate real from hallucinated (or
  legitimate-but-unfamiliar from malicious) names, the trust gate must be built entirely from
  non-LLM provenance signals (publisher identity/verification status, registration age,
  cross-referencing independent registries) — reintroducing an LLM judge anywhere in the gate
  would inherit the exact 51-53%-accuracy failure the base paper already documented."
- **C3** [HYPOTHESIS, sharpened by the confirmed usability-collapse finding]: "Every one of the
  base paper's four defenses traded hallucination reduction for severe recall loss (best case
  ~16% correct-skill recommendation). An install-time trust gate must be shown to avoid this same
  collapse for it to be a genuine improvement rather than a relocated version of the same
  tradeoff — i.e., legitimate skills from new/independent/unverified-but-honest publishers must
  not be rejected at anywhere near the rate the base paper's recommendation-time filters reject
  real skills, or this topic has not actually solved the problem, only moved it."
- **C4** [HYPOTHESIS, derived from "拦截的时机...如何影响下游任务成功率与恢复代价", now specifically
  about compromise rather than pure noise]: "Measuring the causal effect of detection timing
  requires isolating it from confounds, and the outcome to measure is now security-relevant
  (was a squatted skill installed and, if so, did it cause detectable harm in the sandboxed
  environment), not merely a stalled trajectory — plausibly adapted from [AgenTracer,
  OpenReview:l05DseqvuD]'s counterfactual-replay logic, holding task difficulty fixed while
  varying only when the trust check runs (immediately before install vs. delayed by k steps)."
- **C5** [HYPOTHESIS, adversarial extension, now grounded in the confirmed RQ2 predictability
  finding rather than assumed]: "Since hallucinated names are confirmed to recur predictably
  across prompts and models (RQ2), an attacker's optimal strategy is already close to 'harvest
  the recurring names and register them' — the interesting open question is whether a deployed
  trust gate changes *which* names attackers bother targeting (e.g., pushes toward
  typosquat-style near-misses of verified-publisher names instead of squatting raw hallucinations)
  rather than whether hallucination itself evolves. This is a genuinely harder, longer-horizon
  question and may only be partially addressed (see `unaddressed_challenges` below)."
- **C6** [HYPOTHESIS, from the empirical baseline's own heterogeneity]: "The confirmed baseline
  hallucination rate varies from 36.0% to 43.1% by prompt type and presumably more by individual
  model (the paper reports per-configuration numbers this digest has not fully enumerated). Any
  claim about gate effectiveness or the security/usability operating point must be reported per
  model/harness cell and benchmarked against the paper's own per-defense numbers, not pooled."

**conflation_check**: `true` — each challenge targets a distinct obstacle (squatting race
condition, provenance-only design constraint, usability-collapse avoidance, timing-vs-difficulty
confound for a security outcome, adversarial re-targeting, cross-model heterogeneity).

**Status:** PARTIAL — no paper text to extract from; challenges are inferred from the seed plus
the real baseline table's structure.
**absence_comment:** {"what_missing": "There is no Challenges section in a real paper; these are this digest's decomposition of the core question into problem-inherent obstacles.", "why_matters": "A different author might weight C4 (adversarial evolution) as the central contribution rather than a stretch goal.", "implication": "Treat C1-C5 as a design-review checklist for the trajectory harness and gate design, not a definitive taxonomy."}

---

## N6 Methodology

**overview** [HYPOTHESIS]: "Build a multi-step agent-trajectory harness that embeds a
skill-recommend-then-install decision — modeled on [HallucSkills, arXiv:2607.12340]'s two
settings (standalone-LLM recommendation; agent-harness recommend-then-install) and its confirmed
36.0%-43.1% hallucination rate and RQ2 name-recurrence property — inside longer tasks with a real
downstream outcome. Instrument a **publisher-trust gate** (not a bare existence check, which the
squatting threat model defeats, per C1) that runs immediately before each skill install, and
compare gate-on vs. gate-off vs. delayed-gate arms, benchmarking the resulting
security/usability operating point directly against the base paper's own four reported points."

**Staged plan.** *Pilot stage (= the seed's minimal experiment, revised):* first reproduce a
comparable hallucination rate on 1-2 of the base paper's own models/harnesses, using its own
prompt-construction method (community questions + skill-description prompts) as closely as
feasible, since a pilot that cannot reproduce the published rate cannot trust its own gate-effect
estimates. Then run ~150-300 multi-step trajectories with a real-or-simulated skill registry
carrying trust-tier metadata, across 3 arms (gate-on/off/delayed) at 1-2 models, seeding the
squatting simulation with names drawn from the recurrence pattern the base paper documents (C1),
plus a legitimate-unverified-publisher probe set (C3) to measure usability cost. Decision gate:
proceed to scale-up only if the pilot's security/usability operating point is *not* dominated by
the base paper's own four published points (i.e., this topic must beat or meaningfully
differentiate from an already-published Pareto frontier, not merely exist). *Scale-up stage:* add
the full baseline's model/harness matrix for direct comparability, and, if resources allow, a
light adversarial-retargeting arm for C5 (does a deployed gate shift attacker behavior toward
typosquats of verified names rather than raw hallucination squatting).

**key_components:**
- **M1** — name="Trust-tiered registry snapshot"; text="A skill registry snapshotted per episode,
  annotated with publisher trust tier (verified, previously-seen/known, unknown/anonymous) and
  registration recency — not merely a name-existence list, directly answering C1's squatting race
  condition: a squatted malicious skill can satisfy 'exists' but not 'verified-or-known
  publisher'." [HYPOTHESIS]
- **M2** — name="Publisher-trust gate (not an existence or name-similarity gate)"; text="A
  pre-install check keyed purely on M1's provenance metadata — no LLM judgment anywhere in the
  gate, directly enforcing C2's constraint that self-/cross-model auditing is confirmed
  coin-flip-level per [HallucSkills, arXiv:2607.12340]'s RQ3. Verdict is install-allowed
  (verified/known publisher), install-blocked (unknown publisher, name matches a documented
  hallucination-recurrence pattern), or human-review-flagged (unknown publisher, no strong
  hallucination signal — the harder middle case a real legitimate first-time publisher also falls
  into)." [HYPOTHESIS]
- **M3** — name="Multi-step recommend-then-install trajectory harness"; text="Embeds a single
  recommend-then-install decision — drawn from the base paper's own two settings — as one step
  inside a longer task with its own real, checkable downstream outcome (adapted coding tasks or
  multi-step tool-dependency tasks in the style of [ToolLLM, OpenReview:dHng2O0Jjr]'s executable
  API interactions), with the outcome now including a security dimension (was a squatted skill
  actually installed and did it execute) alongside task success." [HYPOTHESIS]
- **M4** — name="Squatting-adversary simulator, seeded from confirmed recurrence"; text="Rather
  than an arbitrary or worst-case malicious-name generator, seeds the simulated attacker's
  pre-registered names from the recurrence property [HallucSkills, arXiv:2607.12340] confirms
  (RQ2) — i.e., names a real measurement showed agents reliably hallucinate — so the adversary
  model is faithful to a demonstrated attack rather than a hypothetical one." [HYPOTHESIS]
- **M5** — name="Detection-timing instrumentation, incl. a delayed-gate control"; text="Records
  the step index at which an untrusted/squatted install is caught: immediately by M2 (gate-on
  arm), never or late via organic task/security failure (gate-off arm — which, unlike pure-noise
  hallucination, may never organically surface since a working malicious skill can look like task
  success), or artificially delayed by k steps (delayed-gate arm), adapting the
  counterfactual-replay logic of [AgenTracer, OpenReview:l05DseqvuD] to a controlled-delay design
  per C4." [HYPOTHESIS]
- **M6** — name="Security/usability operating-point accounting"; text="Per episode: compromise
  blocked/occurred, downstream task success/fail, recovery cost (extra steps/tokens after a
  blocked install), and — critically — the legitimate-unverified-publisher rejection rate from
  M1's probe set, reported as a single operating point directly plottable against the base
  paper's own four (hallucination-rate, recall) points, satisfying C3's requirement that this
  topic show it avoids, not relocates, the base paper's usability collapse." [HYPOTHESIS]

**challenge_arguments:**
- {challenge_id: "C1", argument_text: "M1's trust-tier metadata (not bare existence) and M4's
  recurrence-seeded adversary directly answer the squatting race condition: a malicious skill can
  satisfy 'exists' but not 'verified/known publisher', closing the exact hole a naive existence
  gate would leave open.", mechanism_components: ["M1", "M4"], source: HYPOTHESIS}
- {challenge_id: "C2", argument_text: "M2's gate uses only M1's provenance metadata, with no LLM
  judgment call anywhere in the verdict path, avoiding inheritance of the confirmed
  coin-flip-level self-/cross-model auditing failure.", mechanism_components: ["M1", "M2"],
  source: HYPOTHESIS}
- {challenge_id: "C3", argument_text: "M6's explicit legitimate-unverified-publisher rejection
  rate, reported alongside the compromise-block rate as one comparable operating point, is the
  direct test of whether this topic avoids the base paper's own usability-collapse pattern rather
  than assuming it does.", mechanism_components: ["M6"], source: HYPOTHESIS}
- {challenge_id: "C4", argument_text: "The delayed-gate control arm in M5 holds the trajectory
  and task difficulty fixed while varying only when the trust check runs, isolating timing's
  causal effect on M6's outcome accounting from task-difficulty confounds.",
  mechanism_components: ["M5", "M6"], source: HYPOTHESIS}
- {challenge_id: "C5", argument_text: "The optional scale-up adversarial-retargeting arm (does a
  deployed M2 gate push attackers toward typosquatting verified names instead of squatting raw
  hallucinations) is the direct, if partial, test of whether defense deployment changes attacker
  behavior rather than assuming a static adversary.", mechanism_components: ["M2", "M4"],
  source: HYPOTHESIS}
- {challenge_id: "C6", argument_text: "Reporting every M5/M6 statistic per model/harness cell
  (never pooled), and against the base paper's own per-defense numbers, keeps known
  cross-configuration heterogeneity from masking or exaggerating the gate's effect.",
  mechanism_components: ["M3", "M5", "M6"], source: HYPOTHESIS}

**unaddressed_challenges**: ["C5"] — only partially addressed: the optional adversarial-retargeting
arm is a single simulated-adversary sweep, not a live red-team or iteratively-adapting attacker,
so genuine long-horizon adversarial adaptation is out of scope for the plan as sketched here.

**Feasibility** [HYPOTHESIS — order-of-magnitude estimates]:
- *Pilot:* baseline-replication pass (1-2 models, a few hundred recommendation queries, matching
  the base paper's method loosely) plus ~150-300 trajectory episodes × 3 arms × 1-2 models ≈
  450-900+ episodes; API-cost class: low hundreds to low thousands of dollars; ~2-3 person-weeks
  for M1-M4 harness construction (the trust-tiered registry + trajectory harness + adversary
  simulator is the bulk of the engineering, and is genuinely new relative to the base paper,
  which built none of these).
- *Scale-up:* full model/harness matrix (matching the base paper's 12 configurations where
  feasible) × 3 arms ≈ low thousands of episodes; the adversarial-retargeting sweep for C5 adds a
  bounded, non-training cost; ~3-4 additional person-weeks.
- *Single biggest feasibility risk:* if the pilot's security/usability operating point does not
  clearly beat or differentiate from the base paper's own four published points, the topic has
  produced a relocated version of the same tradeoff rather than a genuine improvement — the
  staged plan's decision gate is designed to catch this before the scale-up is funded, not after.

**Status:** PARTIAL — entirely inferred method design; no methodology section exists to extract.
**absence_comment:** {"what_missing": "No implemented method exists; M1-M6 are this digest's operationalization of the seed, now revised against the fully-read base paper rather than a scraped table.", "why_matters": "The base paper explicitly did not build a trust-tiered registry, an install-time gate, or a recurrence-seeded adversary simulator — these are all genuinely new relative to it — but the actual implementation could still differ once real registry data (e.g., an actual skills marketplace's publisher-verification API) is examined.", "implication": "Use M1-M6 as the build spec; the first engineering task should be checking whether any real skill registry (the paper mentions SkillsMP, ClawHub) already exposes publisher-verification metadata, since if none do, M1 requires either building a synthetic registry or a policy argument that such metadata should exist."}

---

## N7 Contributions

- **CO1** [HYPOTHESIS]: "A multi-step agent recommend-then-install trajectory harness with a
  trust-tiered skill registry and a recurrence-seeded squatting-adversary simulator, faithful to
  [HallucSkills, arXiv:2607.12340]'s confirmed prevalence and targetability findings
  (M1+M3+M4)." contribution_type: `dataset`; is_testable: true; has_rq: true
- **CO2** [HYPOTHESIS]: "An empirical security/usability operating point for install-time
  publisher-trust gating, reported directly comparable to the base paper's own four
  recommendation-time defense operating points, plus how that point shifts with detection timing
  (immediate vs. delayed vs. never)." contribution_type: `empirical_finding`; is_testable: true;
  has_rq: true
- **CO3** [HYPOTHESIS]: "A measured legitimate-unverified-publisher rejection rate for trust-tier
  gating — the usability-cost side of the tradeoff, testing whether an install-time gate avoids
  or merely relocates the recall collapse the base paper found in all four of its own
  recommendation-time defenses." contribution_type: `empirical_finding`; is_testable: true;
  has_rq: true
- **CO4** [HYPOTHESIS]: "A methodological argument, conditional on CO2/CO3's direction, about
  whether install-time provenance verification is a better-positioned intervention point than
  recommendation-time constraint for the skill-squatting threat [HallucSkills, arXiv:2607.12340]
  documents but does not itself build or test." contribution_type: `conceptual_framework`;
  is_testable: false; has_rq: false

**Status:** PARTIAL — no paper text exists; contributions are hypothesized from the method sketch.
**absence_comment:** {"what_missing": "There is no stated contributions list to extract.", "why_matters": "The actual paper might narrow to CO2 alone if CO3/C4 prove infeasible, or drop entirely if arXiv:2607.12340 already covers this ground.", "implication": "Treat CO1-CO4 as candidate framings to validate once the Freshness-note check and real results exist."}

---

## N8 Research Questions

**research_questions:**
- **RQ1** [GIVEN, revised post-reading] (the seed's core question, now sharpened against the
  confirmed base paper): "Does an install-time publisher-trust gate achieve a security/usability
  operating point that beats or meaningfully differentiates from [HallucSkills,
  arXiv:2607.12340]'s own four recommendation-time defenses (best published point: 3.2%
  hallucination / ~16% recall via retrieval grounding; 7.2% hallucination-equivalent / 44.8%
  recall via cross-model voting), and how does the timing of interception affect downstream
  task/security outcome and recovery cost?"
  (id: "RQ1"; rq_source: "explicit"; addresses_challenges: ["C1","C2","C4","C6"];
  evaluates_mechanisms: ["M1","M2","M3","M5","M6"]; tests_contributions: ["CO1","CO2"];
  answered_by_experiment: "gate-on vs. gate-off vs. delayed-gate trajectory arms on the M3
  harness, primary endpoint = compromise-block-rate/recall operating point plotted against the
  base paper's own four points, reported per model/harness cell.")
- **RQ_INF_1** [HYPOTHESIS, inferred from the seed's evasion clause, now the usability-collapse
  test]: "Does an install-time trust gate reject legitimate skills from unverified-but-honest
  (e.g., new/independent) publishers at a rate anywhere near the ~84% rejection-of-real-skills the
  base paper's best defense (retrieval grounding) incurs, or does moving the intervention to
  install time avoid that collapse?"
  (rq_source: "inferred"; addresses_challenges: ["C3"]; evaluates_mechanisms: ["M1","M2","M6"];
  tests_contributions: ["CO3"]; answered_by_experiment: "M6's legitimate-unverified-publisher
  probe set run through M2, rejection rate compared directly to the base paper's published
  ~84%/~55% recall-loss figures.")
- **RQ_INF_2** [HYPOTHESIS, inferred from C6's heterogeneity concern and the baseline's own
  confirmed cross-configuration variance]: "Does trust-gate effectiveness and the resulting
  operating point differ between standalone-LLM recommendation and agent-harness
  recommend-then-install settings — i.e., does the base paper's own configuration-dependence
  (36.0% standalone vs. 36.9% agent average, rising to 43.1% on real developer questions) carry
  over into how much an install-time gate changes the outcome?"
  (rq_source: "inferred"; addresses_challenges: ["C6"]; evaluates_mechanisms: ["M3","M5","M6"];
  tests_contributions: ["CO2"]; answered_by_experiment: "per-setting comparison of the RQ1
  primary endpoint, matching the base paper's own standalone-vs-agent split for direct
  comparability.")

**datasets** [HYPOTHESIS — the harness is novel; the *source material* is real and named]:
{names: ["Novel multi-step recommend-then-install trajectory harness (CO1) embedding decisions
drawn from the same settings [HallucSkills, arXiv:2607.12340] uses (standalone-LLM
recommendation; agent-harness recommend-then-install, e.g. Claude Code/OpenClaw/OpenCode-style)",
"A skill registry with trust-tier metadata — either a real marketplace's publisher-verification
API if one exists (the base paper mentions SkillsMP, ClawHub) or a constructed synthetic registry
if none exposes this today", "A squatting-adversary simulator seeded from the base paper's own
confirmed recurring-hallucinated-name pattern (M4)", "A held-out legitimate-unverified-publisher
probe set (M6)"], source: HYPOTHESIS, location: null}
**baselines** [HYPOTHESIS]: {names: ["Gate-off (no intervention)", "Gate-on (M2, immediate
trust-tier check)", "Delayed-gate (M2's check artificially delayed by k steps, isolating timing
per C4)", "The base paper's own four reported operating points (retrieval grounding,
self-refinement, RAG+self-refinement, cross-model voting), used as published comparison points
rather than re-run, since re-running them is not this topic's contribution", "Oracle-always-safe
upper bound (no compromise ever occurs, for scaling the recovery-cost numbers)"], source:
HYPOTHESIS, location: null}
**metrics** [HYPOTHESIS — with definitions]: {names: ["Compromise-Block Rate = fraction of
simulated squatting-install attempts blocked, per arm and per model/harness cell",
"Legitimate-Unverified-Publisher Rejection Rate = the usability-cost counterpart, on the M6
probe set", "Detection Lag = step index at which an untrusted install is first caught (gate-on: 0
relative to the decision step; gate-off: step index of organic failure, or 'uncaught' since a
working malicious skill can look like task success)", "Recovery Cost = extra steps/tokens/
tool-calls between the untrusted install and task resolution", "Reproduced Baseline
Hallucination Rate (pilot check against the published 36.0%-43.1% range, a hard replication
gate before any arm comparison is trusted)"], source: HYPOTHESIS, location: null}

**Analysis plan** [HYPOTHESIS — pre-registerable]:
- *Sample size:* pilot ≈ 300 trajectory episodes per arm per model (900+ total per model across 3
  arms); powered to detect a 10-percentage-point compromise-block-rate difference at power ≈ 0.8,
  two-sided α = 0.05 (two-proportion test); re-estimated from the pilot's observed base rate
  before the scale-up.
- *Primary test:* Compromise-Block Rate, gate-on vs. gate-off, Fisher's exact test per
  model/harness cell, Holm-Bonferroni corrected across cells; the resulting (block-rate,
  legitimate-rejection-rate) point plotted against the base paper's own four points as the
  headline comparison, not a p-value alone. Expected direction: gate-on's point Pareto-dominates
  at least the base paper's weakest defense (self-refinement: 33.2% hallucination / recall not
  reported as favorably as retrieval grounding).
- *Timing effect (RQ1 continued):* ordinal/trend test of compromise outcome and recovery cost
  across {immediate, delayed-by-k, never-caught} detection timing, expecting monotonically worse
  outcomes as detection is delayed.
- *Usability audit (RQ_INF_1):* proportion test on M6 probe set, rejection rate compared directly
  (not just qualitatively) to the base paper's published ~84%/~55% recall-loss figures; two
  independent annotators code any disputed rejections (target Cohen's κ ≥ 0.7).
- *Setting comparison (RQ_INF_2):* pairwise contrast of the RQ1 primary endpoint between
  standalone-LLM and agent-harness settings, same correction procedure.

**Status:** PARTIAL — RQ1 is given (revised post-reading); RQ_INF_1/RQ_INF_2, datasets,
baselines, metrics, and the analysis plan are inferred design, now benchmarked against real
published numbers rather than a scraped table.
**absence_comment:** {"what_missing": "No explicit RQ list, dataset, baseline, or metric table exists in a real paper; the analysis plan is a pre-registration draft.", "why_matters": "The power analysis assumes a compromise-block base rate that has not been measured; the RQ set's novelty margin over the base paper's closing sentence is still the main open risk (see N2's absence_comment), not factual accuracy.", "implication": "Re-estimate sample sizes from the pilot's observed base rates before the scale-up; treat the base paper's own four operating points as the bar to clear, not a checkbox."}

---

## N9 Results

> **CRITICAL — no experiment has been run. Nothing below is a real result.** Each item states
> only a **hypothesized direction**, tagged [PLACEHOLDER — HYPOTHESIZED DIRECTION ONLY], with
> `evidence_strength="missing"` and `rq_answered=false`, plus an explicit falsification
> condition. No numbers are given because none exist (the only real numbers in this digest are
> the mined baseline table's, which belong to arXiv:2607.12340, not to this unwritten topic).

- **rq_id**: "RQ1"
  **result_text** [PLACEHOLDER — HYPOTHESIZED DIRECTION ONLY]: "Predicted direction: the gate-on
  arm's (compromise-block, legitimate-rejection) point Pareto-dominates the base paper's weakest
  defenses (self-refinement, RAG+self-refinement) and is competitive with but not dominated by
  its strongest (cross-model voting: 92.8% hallucination-elimination / 44.8% recall), because
  moving the check to install time avoids constraining the recommendation distribution at all.
  Detection timing predicted to matter less for pure task success than for security outcome,
  since a silently-installed malicious skill may not disrupt the visible task at all."
  **result_type**: `quantitative` (predicted); **evidence_strength**: `missing`;
  **rq_answered**: `false`
  **FALSIFICATION CONDITION**: "Refuted if the gate-on operating point is dominated by (worse on
  both axes than) any of the base paper's four published points, or if compromise-block rate is
  statistically indistinguishable between gate-on and gate-off."

- **rq_id**: "RQ_INF_1"
  **result_text** [PLACEHOLDER — HYPOTHESIZED DIRECTION ONLY]: "Predicted direction: the
  install-time trust gate's legitimate-unverified-publisher rejection rate is materially lower
  than the base paper's own worst recall-loss figure (~84% real-skill rejection under retrieval
  grounding), because it does not touch the LLM's recommendation distribution — but is not zero,
  since any real first-time/independent publisher looks identical to a squatter on provenance
  metadata alone until it accumulates trust signal."
  **result_type**: `quantitative` (predicted); **evidence_strength**: `missing`;
  **rq_answered**: `false`
  **FALSIFICATION CONDITION**: "Refuted if the install-time gate's rejection rate on legitimate
  unverified publishers is statistically indistinguishable from the base paper's own
  recommendation-time recall-loss figures (i.e., moving the intervention point bought nothing)."

- **rq_id**: "RQ_INF_2"
  **result_text** [PLACEHOLDER — HYPOTHESIZED DIRECTION ONLY]: "Predicted direction: gate benefit
  (RQ1's effect size) is larger in agent-harness recommend-then-install settings than in
  standalone-LLM recommendation settings, because only the former has a real install/execution
  step for the gate to intercept before consequence."
  **result_type**: `quantitative` (predicted); **evidence_strength**: `missing`;
  **rq_answered**: `false`
  **FALSIFICATION CONDITION**: "Refuted if the RQ1 effect size is statistically indistinguishable
  between standalone and agent-harness settings."

**Status:** NOT_FOUND (by construction — no experiment exists).
**absence_comment:** {"what_missing": "No real results exist; the paper has not been written and the experiment has not been run. The Freshness-note check HAS now been performed (full paper read 2026-08-13); what remains missing is the experiment itself, not the literature check.", "why_matters": "Presenting a direction as a finding would fabricate empirical support for a claim that is currently only a prediction.", "implication": "Re-populate N9 with real numbers only after running the pilot and scale-up; the pilot's hard gate (N6) is whether the resulting operating point differentiates from the base paper's own four published points."}

---

## N10 Threats / Self-Limitations

> Reverse-digest caveat: N10 normally holds only author-acknowledged limitations; since no author
> text exists, these are *anticipated* threats this study design must answer, written so they can
> be checked against the real paper later.

**threats:**
- **t1** [HYPOTHESIS, revised post-reading]: category=`construct`; description: "The full paper
  has now been read and confirms the trajectory/timing/install-time-gate layer is genuinely
  unstudied by it — but the *specific mechanism* proposed here (a provenance/trust gate) is close
  enough to the base paper's own closing sentence ('verified recommendation pipelines') that a
  reviewer could reasonably ask whether this is a distinct contribution or an implementation of
  an idea the base authors already had." mitigation: "Lead with the concrete, numbers-comparable
  security/usability operating point (RQ1) rather than the trust-gate idea alone; the paper's
  contribution is the *measurement* of whether this specific mechanism actually beats the
  published Pareto frontier, not the idea that provenance-checking might help."
- **t2** [HYPOTHESIS]: category=`construct`; description: "Operationalizing 'downstream task
  derailment' as a binary success/fail may miss partial degradation (task technically succeeds
  but with a worse-quality output because of the hallucinated-tool detour)." mitigation: "Record
  a secondary quality/efficiency metric (steps/tokens relative to an oracle-always-correct run)
  alongside the binary outcome, per M5."
- **t3** [HYPOTHESIS]: category=`internal`; description: "The registry-grounding gate's
  fuzzy/semantic near-miss threshold (M2) is itself a tuned parameter; results could be an
  artifact of that tuning rather than a general property of registry-grounding gates."
  mitigation: "Report results across at least two threshold settings (strict exact-match-only vs.
  the calibrated semantic band) rather than a single tuned point."
- **t4** [HYPOTHESIS]: category=`external`; description: "Findings may be specific to the tested
  model families, the specific registry sizes/domains used, and the two harness families
  (search-style, coder-agent-style); live, uncontrolled registries and frontier proprietary
  models beyond those tested are out of scope." mitigation: "Report per-model/per-harness results
  separately (no pooled-only claims, per C5); release the harness (CO1) for extension."
- **t5** [HYPOTHESIS]: category=`conclusion`; description: "Multiple condition cells (model ×
  harness × arm × delay-k) invite false positives from multiple comparisons." mitigation:
  "Pre-registered primary endpoint (RQ1's gate-on vs. gate-off contrast), Holm-Bonferroni
  correction for secondary contrasts, per N8's analysis plan."
- **t6** [HYPOTHESIS]: category=`reproducibility`; description: "The published baseline's own
  hallucination rates may not replicate exactly under this study's harness (different task
  distribution, different registry), undermining direct comparability to
  arXiv:2607.12340's numbers." mitigation: "The pilot's baseline-replication step is a hard gate
  (N6); report the reproduced rate range alongside the published one rather than assuming
  transferability."

**Status:** PARTIAL — anticipated limitations of this *kind* of study, not author-acknowledged.
**absence_comment:** {"what_missing": "There is no written Limitations/Threats-to-Validity section to extract from.", "why_matters": "N10 is supposed to hold only author-explicit self-limitations; here it necessarily holds this digest's forecasts.", "implication": "Replace wholesale with the real paper's own stated limitations once written; do not cite t1-t6 as if authors said them."}

---

## N11 Artifacts

**artifacts**: []
**has_code**: `false` [PLACEHOLDER]
**has_data**: `false` [PLACEHOLDER]
**has_model**: `false` [PLACEHOLDER]

**Status:** NOT_FOUND.
**absence_comment:** {"what_missing": "No code, dataset, or model has been released, because no paper or implementation exists yet.", "why_matters": "A reader should not assume any artifact (trajectory harness, gate implementation, near-miss probe set, registry snapshots) is available for reuse.", "implication": "Once the pilot is implemented (after the Freshness-note check), populate this node with real repo/dataset URLs; the planned releases are the CO1 harness, the M2 gate implementation, and the M6 near-miss probe set."}

---

## N12 Contribution Type

**value**: `empirical` [HYPOTHESIS]

**rationale** [HYPOTHESIS]: "RQ1 and both inferred RQs are measurement/intervention-evaluation
questions about whether, and under what conditions, a specific mechanism (a registry-grounding
gate) changes a specific downstream outcome (task success, recovery cost) — the hypothesized
outputs in N9 are success-rate deltas, a detection-lag-to-cost relationship, and a false-positive
rate, i.e., what an empirical intervention study reports. The trajectory harness and gate (M1-M6,
CO1) are built as the *instrument* for this measurement, analogous to how B1.1's dual-channel
suite supports an `empirical` classification, rather than as a leaderboard-oriented benchmark
product; the seed's own framing centers the intervention-effect question, ruling out
`benchmark`/`dataset` as the primary type. If, during execution, the harness's reuse by others
becomes the central claim (e.g., it is adopted as a standard evaluation suite), reclassify to
`benchmark`."

**Status:** FOUND (a definite single-enum classification is made, on hypothesized grounds).
No absence_comment required.

---

## Claims

1. **[HYPOTHESIS]** "An install-time publisher-trust gate, run immediately before each skill
   install in a multi-step agent trajectory, achieves a security/usability operating point that
   Pareto-dominates at least the weaker of [HallucSkills, arXiv:2607.12340]'s own four
   recommendation-time defenses, because it does not need to constrain what the LLM is allowed to
   recommend." — the central falsifiable prediction (N9/RQ1), building on but mechanistically
   distinct from the base paper's own tested defenses.
2. **[HYPOTHESIS]** "An install-time trust gate cannot be made both maximally strict and
   false-positive-free against legitimate but unverified publishers, but its rejection rate on
   real skills is materially lower than the base paper's own worst recommendation-time recall
   loss (~84%)." — the RQ_INF_1 prediction, the paper's core differentiator claim.
3. **[HYPOTHESIS]** "Gate benefit is setting-dependent, larger in agent-harness
   recommend-then-install settings (where a real install step exists to intercept) than in
   standalone-LLM recommendation settings (where there is no install step at all)." — the
   RQ_INF_2 prediction.
4. **[PLACEHOLDER]** "The actual magnitude of gate benefit, legitimate-rejection rate, and
   setting-dependence are unknown until the experiment is run — no model, dataset, or number
   currently supports any quantitative claim about this phenomenon." — flags N9 as entirely
   speculative.
5. **[CONFIRMED, 2026-08-13]** "arXiv:2607.12340 has been read in full. It confirms the
   phenomenon (36.0%-43.1% hallucination rate, every configuration affected), the attack
   (predictable-name squatting), the detection failure (self-/cross-model auditing is
   coin-flip-level), and that every one of its own four recommendation-time defenses trades
   security for severe usability loss — and it explicitly does not build or test an install-time
   provenance/trust gate, only calling for 'verified recommendation pipelines' as needed future
   work. The topic survives in the revised (trust-tier, install-time) form documented throughout
   this digest. The residual open risk is not factual (the gap is real) but a novelty-margin
   judgment call: whether building the mechanism the base paper's own closing sentence calls for
   counts as sufficiently distinct, which N2's absence_comment and t1 both flag as the thing to
   resolve by leading with the measured operating point rather than the mechanism idea alone."
