# Discussion Trace — B4.6 (auto-research-discussion, Stages 1–6)

> Mode: **autoclaude** (self-play, Claude as student+teacher). Seed: `../README.md` only (39-line topic card, [证据]/evidence label, sourced from `trend_scan_2026-08.md` §2.5 + the 2026-08-13 occupancy sweep in §6). **No `digest.md` and no `paper.md` exist for this topic and none were fabricated** — the seed is immature by design, so every formal definition, assumption, and RQ below is derived during the stages, and the critic rounds run at full strength against the seed rather than deferring to it. Round cap: 5/stage (none hit). Date: 2026-08-15.
>
> **Full pipeline order:** this file (`auto-research-discussion`, 6 stages) → `taste_audit.md` (`research-taste-auditor` on confirmed Stage 2 + Stage 5) → `stage_review.md` (`pengsida-stage-reviewer`, archetype-classified PASS/REVISE/STOP per stage, plus the Writing bar against the first assembled draft) → `paper_draft.md` / `refs.bib` / `paper_draft.tex` / `paper_draft.pdf`. `experiment_design.md` renders Stage 6's confirmed output as a standalone protocol.

## Seed brief

- **One-sentence description:** Measure what fraction of a coding agent's serving bill (tokens, latency, dollars) is *verification-induced* — test runs, failure-retry loops, test output fed back into context, and the prefix-cache reuse that verification output destroys — and how much of that bill is avoidable, at matched task-resolution outcomes, when verification steps are scheduled as first-class units.
- **Apparent inputs:** TraceLab public coding-agent traces (~4,300 sessions, 430K tool calls, test/build/edit steps distinguishable — per the seed card); supplementary self-run SWE-bench sessions; a serving cost model (prefix-cache policy + price vector).
- **Apparent outputs:** verification-induced cost decomposition; KV/prefix-cache invalidation attribution; per-verification-class cost/value profile (lint ≪ unit ≪ full suite); $/resolved-task headroom under counterfactual verification scheduling at matched resolve rate.
- **Closest research areas (from the seed's own evidence base):** coding-agent workload characterization (TraceLab 2606.30560; Copilot-scale 2608.00101), agent-aware KV-cache/scheduling (KVFlow; Irminsul 2605.05696; SAGA 2605.00528), cost-aware speculative execution (2606.07846; SpecBox 2607.23933), Generate/Verify queueing theory (arXiv:2504.07347).
- **In scope:** trace-grounded measurement, counterfactual replay simulation, and a bounded set of live SWE-bench re-runs. **Out of scope (explicit in the seed):** datacenter access; proposing a production scheduler as the contribution; training new verifiers or agents.
- **Family interface note (scope discipline, not paper content):** sibling B4.5 asks *which trajectories deserve verification* (agent-level precision–budget frontier); sibling B4.2 asks *what a verifier dollar buys relative to thinking/sampling dollars* (test-time allocation frontier). B4.6's estimand is different from both: *when, where, and at what granularity verification runs on the serving stack*, denominated as $/resolved-task at matched resolve rate, including the cache-interaction term neither sibling models. The critic checks at Stages 1–3 that no stage output drifts onto either sibling's estimand.
- **Confidence: medium.** The seed card is specific about data, nearest neighbors, and the falsifiable claim, but carries no formal problem definition, no assumptions ledger, and no RQ structure — all constructed below and therefore fully critic-exposed.

---

## Stage 1 — Problem Definition

### Round 1 (critic phase)

**draft_v1** (proposer):
- `summary`: Given session-level traces of coding agents in which verification steps (lint, type-check, unit test, build, full test suite) are distinguishable from generation and other tool steps, determine (a) what fraction of each session's serving cost — tokens, latency, dollars — is induced by verification, directly (executing the check, feeding its output back into context) and indirectly (failure-retry loops, prefix-cache invalidation caused by verification-output churn), and (b) how much of that cost could be removed at unchanged resolution outcomes by rescheduling verification — including speculatively continuing generation past verifications predicted to pass.
- `input`: (1) a trace corpus with per-step type labels, message content or reconstructable token counts, timestamps, and task-resolution outcomes; (2) a serving cost model mapping the session's request sequence to prefill/decode work and prefix-cache hits under a stated cache policy; (3) a price vector (dollars per input/output token, per verification-execution second).
- `output`: (1) a per-session verification-induced cost decomposition; (2) a verification-attributable prefix-cache-invalidation estimate; (3) a per-verification-class cost/value profile; (4) headroom estimates: the serving dollars removable by counterfactual verification scheduling at matched resolve rate.
- `constraints`: traces are post-hoc — the agent policy that generated them cannot be re-queried inside the corpus; any counterfactual schedule that changes what the agent observes cannot be evaluated by replay alone; dollar figures are functions of a stated price vector and cache policy.
- `objective`: decompositions and headroom estimates that a third party could recompute from the traces and the stated rules; comparisons across schedules are valid only at matched resolve rate.
- `study_type`: `empirical` — stated explicitly: the seed's own label is [证据]/evidence, its deliverable is a measured cost structure and a measured headroom, and its stage-1 phrasing ("多大比例…造成多少破坏") is measurement language. The scheduling policies are measurement probes for avoidable cost, not a proposed serving system.

**critique:**
- summary: The estimand family is right and traceable to the seed card, but the summary smuggles in a named technique, and the load-bearing phrase "matched resolve rate" is asserted without an evaluability rule — as written, the objective cannot be scored.
- comments:
  - `{severity: major, field: "summary", anti_pattern: "method_leak", comment: "'including speculatively continuing generation past verifications predicted to pass' names a specific mechanism (speculative continuation + a pass/fail predictor) inside the problem statement. The seed card does propose this technique, but it belongs to Stage 5; the problem statement should quantify avoidable cost over a *class* of admissible reschedules, defined by what they preserve, not by any named trick. Keeping it here would also quietly commit Stage 5 before Stage 3 has checked whether the nearest neighbor (2606.07846) already owns that trick."}`
  - `{severity: major, field: "objective", anti_pattern: "vague_success (evaluability gap)", comment: "'valid only at matched resolve rate' has two incompatible readings the draft never separates: for a reschedule that leaves the agent-visible token sequence byte-identical, resolve outcomes are matched *by construction* (the recorded outcomes are reused); for a reschedule that changes what the agent sees, matching is a *statistical* claim needing a pre-registered non-inferiority margin, and replay cannot certify it at all. An objective that doesn't distinguish these makes the headline headroom number unscoreable — the single most attackable point of the whole design."}`
  - `{severity: minor, field: "output", anti_pattern: null, comment: "Output (1) should say the decomposition is *interval-valued*: retry-loop attribution has no ground-truth counterfactual in an observational trace, so a point estimate would overclaim. The conservative/liberal bounding is already implicit in the seed's framing; make it explicit at the output level."}`
- decision: `move_to_refiner` — both majors are subtraction/formalization fixes on content already present (delete the technique clause; split the matching rule the constraints already gesture at), squarely within the refiner's conservative remit; no new content is required.

### Refiner pass

- `summary` (refined): "...and (b) how much of that cost could be removed at unchanged resolution outcomes by rescheduling *when, where, and at what granularity* verification steps execute, over a class of admissible reschedules partitioned by whether they preserve the agent-visible information sequence." (Named technique removed.)
- `objective` (refined): "Decompositions reported as pre-registered conservative/liberal intervals recomputable by a third party from traces and stated rules. Headroom estimates are valid under exactly one of two certificates: (i) *replay-exact* — the reschedule preserves the agent-visible token sequence byte-for-byte, so resolution outcomes are identical by construction; or (ii) *non-inferiority-gated* — the reschedule changes agent-visible information, is evaluated by live re-execution, and its headroom is reported only if the resolve-rate difference clears a pre-registered one-sided non-inferiority margin. A headroom number carrying neither certificate is not reportable."
- `output` (1) (refined): "a per-session verification-induced cost decomposition, reported as an interval under pre-registered conservative and liberal attribution rules."
- `formal_summary` (added, refiner's formalize-for-free duty): "A session s = (x_1,…,x_n) interleaves generation steps, non-verification tool steps, and verification steps; each verification step carries a class in K = {lint, type-check, unit, build, suite} and an outcome (pass/fail). A serving cost model C_{p,Θ}(s) maps s to dollars given price vector p and cache policy Θ, counting prefill (cache-miss) tokens, decode tokens, and verification-execution seconds. Estimand 1: the verification-induced share ρ(s) = [ρ_cons(s), ρ_lib(s)] under two fixed attribution rules. Estimand 2: the verification-attributable share of invalidated (re-prefilled) cache tokens. Estimand 3: per-class cost and information-value profiles over K. Estimand 4: headroom Δ(π) = C_{p,Θ}(s) − C_{p,Θ}(π(s)) over admissible reschedules π, partitioned by the invariance predicate ι(π) = 'agent-visible sequence preserved', at matched resolve rate per the objective's two certificates."
- `changes_made`: removed the method leak; split "matched resolve rate" into the two-certificate rule; made interval-valuedness explicit; added formal_summary.
- `declined_to_fix`: none.

**Confirmed Stage 1** — `study_type: empirical`.

---

## Stage 2 — Motivation

### Round 1 (critic phase)

**draft_v1:**
- `summary`: Serving cost, not capability, is becoming the binding constraint on coding-agent deployment, and today's serving stacks price generation while treating verification as opaque tool time — if a large share of a session's bill is verification-induced, both cost accounting and scheduler design are optimizing the wrong term.
- `why_it_matters`: Operators of agent-serving deployments set batching, placement, and cache policy using cost models in which a tool call is dead time and context growth is undifferentiated tokens. Verification steps break both assumptions in a specific, checkable way: their execution cost spans orders of magnitude (a lint pass versus a full test suite), their outputs are large, volatile, and re-fed into the prompt, and their failure outcomes trigger retry loops whose generation cost is causally downstream of the verification event. If the verification-induced share of a session's dollars is substantial, the field's serving optimizations are tuned against a workload model that mislabels a first-order cost driver; if it is small, the seed's premise fails and *that* bound is the finding. Either way the number is decision-relevant: it is the business case — or its refutation — for making verification a first-class scheduling unit.
- `who_cares`: serving-stack operators running vLLM/SGLang-class engines for coding agents; agent-framework maintainers choosing default verification cadence (lint-per-edit? suite-per-patch?); budget-allocation research, which currently reasons about *whether* to verify but has no serving-side account of what verification costs *where*; platform pricing teams deciding what to meter.
- `evidence`: Two workload characterizations now exist — TraceLab (public traces) and a production-scale study of Copilot traffic (3.2M users, 95T tokens, no trace release) — and per the 2026-08-13 occupancy sweep, *neither carries verification-step semantics*: no verification-attributed cost share, no retry-loop attribution, no cache-interaction analysis. Cost-Aware Speculative Execution (2606.07846) prices speculation in dollars but is not grounded in real traces and does not treat the verify decision as the scheduling object. Queueing-theoretic work (arXiv:2504.07347) already models Generate/Verify as distinct service classes — theoretical precedent that the distinction matters for scheduling — but with stylized workloads. The measurement gap is therefore real and currently open, with a stated risk clock (the speculation/verification-overlap subfield gained four papers since 2026-06).
- `why_now`: TraceLab's release is the enabling event — before it, this measurement required production access that only platform owners have (and the Copilot-scale study demonstrates owners are not releasing traces). Public availability is also the threat: anyone can run this measurement now, which is exactly why the seed card gives it a 1–2 quarter clock.

**critique:**
- summary: Stake-specific, evidence-backed, and honestly two-sided (the small-share outcome is named as a finding, not buried). But coverage of Stage 1's four outputs is incomplete in a way that matters: two of the four estimands are motivated only by association.
- comments:
  - `{severity: major, field: "why_it_matters", anti_pattern: "partial_output_coverage", comment: "Stage 1 promises four outputs. The cost-share decomposition and the headroom estimate are motivated directly. But (a) the cache-invalidation estimand gets no argument for why *reuse destruction* is a distinct harm from 'more tokens' — the reader needs the serving fact that prefill dominance makes a cache-miss token materially costlier than an appended token, otherwise invalidation looks like double-counting; and (b) the per-class cost/value profile is never motivated at all — why measure lint vs unit vs suite separately rather than pooling verification? Without that, the frontier output reads as decoration and Stage 4 will inherit an unmotivated sub-problem."}`
  - `{severity: minor, field: "summary", anti_pattern: "unsourced_pain", comment: "'Serving cost, not capability, is becoming the binding constraint' is asserted without a data point. The evidence field's own entries (an enterprise inference-economics paper exists; a production study logged 95T tokens) can carry this — wire one of them to the sentence rather than leaving it as a vibe."}`
- decision: `move_to_refiner` — the missing arguments are one sentence each and use only facts already present in the evidence field and the seed card; formalize-level.

### Refiner pass

- `why_it_matters` (extended, cache): "Cache invalidation is a distinct harm from token volume because agent serving is prefill-dominated: a token that misses the prefix cache is re-computed at full prefill cost on every subsequent request that re-reads the context, so content that *churns* — as verification output does, with volatile paths, durations, and truncated logs re-rendered between turns — can cost multiples of its own length, and a cost model that only counts appended tokens structurally understates it."
- `why_it_matters` (extended, per-class): "The per-class profile is what any scheduling decision actually consumes: 'verification' pooled into one number cannot tell an operator whether the cheap check buys most of the information (schedule it early and often, defer the suite) or almost none of it. The seed's own falsifiable claim — heterogeneous cost × heterogeneous information value — is a claim about this profile, so it must be measured per class or the scheduling question is undefined."
- `summary` (extended): "...binding constraint on coding-agent deployment — enterprise inference-economics analyses and a 95-trillion-token production characterization both exist because operators are now metering exactly this — and today's serving stacks price generation while treating verification as opaque tool time..."
- `changes_made`: added the prefill-dominance argument for the invalidation estimand; added the per-class-profile motivation; wired the binding-constraint sentence to existing evidence.
- `declined_to_fix`: none.

**Confirmed Stage 2.**

---

## Stage 3 — Related Work

**Engagement-honesty header (added after round 1 — see critique):** each work below is tagged with the depth actually reached in this environment: `[scan]` = corpus-scan record only (title/one-liner + the seed card's characterization); `[title+abstract]` = title and abstract-level metadata verified against the arXiv export API on 2026-08-15; `[known]` = well-known published work engaged from established knowledge. No paper's full text was read in this environment; comparisons are drawn accordingly and confidence-qualified.

### Round 1 (critic phase)

**draft_v1** put seven works in the specific tier: TraceLab, Copilot-scale, Cost-Aware Speculative Execution, SpecBox, the Generate/Verify queueing paper, KVFlow, and Inference Economics of Enterprise Coding Agents — each with a full comparison block.

**critique:**
- summary: The funnel was run and the seed's own novelty ledger gives real deltas, but the specific tier is over-promoted: promotion means committing to content-level engagement, and for three of the seven only a corpus-scan one-liner exists in this environment.
- comments:
  - `{severity: major, field: "specific_related_works[copilot_scale, inference_econ, specbox]", anti_pattern: "missing_comparison (comparison unsupported by actual engagement)", comment: "The stage-3 protocol says promotion commits you to read the paper's problem definition, method, and evaluation — and to 'be explicit about how deeply you actually saw the paper.' For 2608.00101 the local record is an arXiv id + scale + no-trace-release status (not even a cached title); for 2607.13080 a title only; for 2607.23933 a system name and one mechanism clause. Comparison blocks built on that are assertions wearing a protocol's clothes. Demote all three to the general tier with honest one-liners, and keep the specific tier to the four works whose role is load-bearing and whose characterization the seed card itself commits to: TraceLab (data substrate + characterization twin), Cost-Aware Speculative Execution (nearest neighbor), the queueing paper (theoretical precedent, verified via arXiv API), and KVFlow (cache-cluster representative, verified via arXiv API)."}`
  - `{severity: minor, field: "general_related_works", anti_pattern: null, comment: "The landscape tier should also carry the serving-systems canon (vLLM/PagedAttention, SGLang radix cache, disaggregation work) and the verification-in-test-time-compute line (repeated sampling, compute-optimal scaling, Reflexion-style feedback loops, execution-based checking) — these are the two communities whose cost models the motivation says mislabel verification, so their absence would read as evasion."}`
- decision: `move_to_refiner` — demotion and landscape completion drop and re-shelve existing entries; no comparison content is invented.

### Refiner pass — confirmed Stage 3 output

**`general_related_works`** (landscape tier; citation + one-line summary; no limitation analysis claimed):

| work_id | citation | engagement | one-liner |
|---|---|---|---|
| `rw_copilot_scale` | arXiv:2608.00101 (2026) | [scan] | Production-scale characterization of coding-agent serving traffic (3.2M users, 95T tokens); no trace release. |
| `rw_inference_econ` | *Inference Economics of Enterprise Coding Agents*, arXiv:2607.13080 (2026) | [scan] | Enterprise-side cost accounting for coding agents; evidences the "operators are metering this" premise. |
| `rw_specbox` | SpecBox, arXiv:2607.23933 (2026) | [scan] | Sandbox-prewarming mechanism for speculative agent execution; mechanism only, per the seed's ledger. |
| `rw_irminsul` | Irminsul, arXiv:2605.05696 (2026) | [scan] | Agent-aware KV-cache management (one of ≥5 such systems May–Jul 2026, with SAGA arXiv:2605.00528, SMetric arXiv:2607.08565, arXiv:2605.06110). |
| `rw_vllm` | Kwon et al. (2023). Efficient Memory Management for LLM Serving with PagedAttention. SOSP. | [known] | Paged KV memory; the serving substrate whose prefix caching this paper's simulator models. |
| `rw_sglang` | Zheng et al. (2023). SGLang. arXiv:2312.07104. | [title+abstract] | Radix-tree prefix cache across structured LM programs — the concrete reuse mechanism verification churn breaks. |
| `rw_distserve` | Zhong et al. (2024). DistServe. OSDI. | [known] | Prefill/decode disaggregation; establishes prefill as the dominant, separately-provisioned cost. |
| `rw_sarathi` | Agrawal et al. (2024). Sarathi-Serve. OSDI. | [known] | Chunked-prefill scheduling; throughput–latency tradeoff machinery this paper's cost model inherits. |
| `rw_mooncake` | Qin et al. (2024). Mooncake. arXiv:2407.00079. | [title+abstract] | KV-cache-centric disaggregated serving in production; evidence that cache reuse is the economic center. |
| `rw_specdecode` | Leviathan et al. (2023). Fast Inference via Speculative Decoding. ICML. | [known] | Token-level speculate-then-verify; the intra-request analogue of step-level speculative continuation. |
| `rw_monkeys` | Brown et al. (2024). Large Language Monkeys. arXiv:2407.21787. | [title+abstract] | Repeated sampling + verification as inference scaling; verification cost treated as free/afterthought. |
| `rw_snell` | Snell et al. (2024). Scaling LLM Test-Time Compute Optimally. arXiv:2408.03314. | [title+abstract] | Compute-optimal test-time allocation; budget denominated in model FLOPs, not serving dollars. |
| `rw_reflexion` | Shinn et al. (2023). Reflexion. NeurIPS. | [known] | The canonical feed-verification-output-back loop that generates retry segments. |
| `rw_codex` | Chen et al. (2021). Evaluating LLMs Trained on Code. arXiv:2107.03374. | [known] | Execution-based checking (pass@k) — the origin of tests-as-verifier for code. |
| `rw_swebench` | Jimenez et al. (2024). SWE-bench. ICLR. | [known] | Resolution-rate task substrate for the live arms. |
| `rw_sweagent` | Yang et al. (2024). SWE-agent. NeurIPS. | [known] | Agent-computer interface whose scaffolds produce the session shape studied here. |
| `rw_openhands` | Wang et al. (2024). OpenHands. arXiv:2407.16741. | [title+abstract] | Open agent platform; second scaffold for the live arms. |

**`specific_related_works`** (deep tier, 4 entries, full comparison protocol):

1. **`rw_tracelab`** — *TraceLab: Characterizing Coding Agent Workloads for LLM Serving*, arXiv:2606.30560 (2026). `[scan]`, but load-bearing as *data substrate*, so its documented corpus facts (~4,300 sessions, 430K tool calls, test/build/edit distinguishable) are taken from the seed card and re-verified against the release in Phase B before any measurement (assumption A1, Stage 6).
   - `input_output_framing`: agent traces in → aggregate workload statistics out (request sizes, tool-call mix, session shapes) for serving-system design.
   - `comparison`: `problem_alignment: related` (same substrate, different estimand: workload statistics vs verification-attributed cost, cache interaction, and counterfactual headroom) · `method_addresses: false` — characterization has no attribution rules, no cache counterfactual, no reschedule evaluation · `effectiveness: n/a` · `threat_to_motivation: medium` (the authors hold the natural follow-up; the seed's risk clock says 1–2 quarters) · `gap_type: not_considered` · `gap_we_address`: "no verification-step semantics: no verification-induced cost share, no retry attribution, no cache-invalidation analysis" · `role: related_for_context` (and data source).
   - `limitations`: `lim_tracelab_no_verification_semantics` — evidence: the 2026-08-13 occupancy sweep's finding that both existing characterizations lack the verification dimension (泛特征无验证维度, per the seed's novelty ledger). `verify_as_hypothesis: false`.
2. **`rw_costaware_spec`** — *Cost-Aware Speculative Execution*, arXiv:2606.07846 (2026). `[scan]`; **the nearest neighbor, per the seed card itself**, and treated as such rather than buried.
   - `input_output_framing`: agent workloads (not real traces) in → dollar-denominated speculative-execution policies out.
   - `comparison`: `problem_alignment: related` (dollar-priced speculation for agents, but the scheduling object is generic execution, not the verify decision) · `method_addresses: true` with adaptation — its speculation machinery could be pointed at verification steps · `effectiveness: untested` — never evaluated on real traces, and never with verification as the decision object or KV interaction modeled (the seed ledger's three deltas: 无真实 trace 落地 / 不把 verify 决策当调度对象 / 不建模 KV 破坏) · `threat_to_motivation: medium` · `hypothesis_to_verify` (set, per protocol, since effectiveness=untested): **"Speculative continuation past verifications predicted to pass yields net positive dollar savings on live coding-agent runs at non-inferior resolve rate; with an oracle pass/fail predictor the median saving is at least 15% of session serving dollars, and a frozen trace-trained predictor retains at least half of the oracle saving. The claim is falsified if oracle savings fall below 5% (speculation headroom absent regardless of predictor quality) or if the frozen predictor retains less than a quarter of oracle savings (headroom exists but is predictor-limited beyond practical reach)."** · `gap_type: not_done_well` (for our problem) · `role: motivation_threat`, answered by repositioning: the delta is trace-grounding + verify-as-decision-object + cache modeling, conceded to share the dollar-denominated objective.
   - `limitations`: `lim_costaware_no_trace_no_verify_object` (description as above; `verify_as_hypothesis: true` → Stage 6 framing-tier RQ).
3. **`rw_queueing`** — Dai, Deng, Li & Peng. *Throughput-Optimal Scheduling Algorithms for LLM Inference and AI Agents*, arXiv:2504.07347 (2025). `[title+abstract]` (verified via arXiv API 2026-08-15).
   - `input_output_framing`: stylized queueing model of LLM/agent request classes in → throughput-optimality results out.
   - `comparison`: `problem_alignment: related` (verification as a distinct service class — the theoretical precedent the seed cites as 理论先声) · `method_addresses: false` — provides no way to estimate the empirical service-class parameters (costs, values, churn) from traces; that estimation is this paper · `effectiveness: n/a` · `threat_to_motivation: low` · `gap_type: not_solved` · `gap_we_address`: "the queueing abstraction presumes exactly the per-class cost/value/cache profiles that have never been measured; this paper supplies the empirical side of that model" · `role: related_for_context`.
   - `limitations`: `lim_queueing_stylized_workloads` (`verify_as_hypothesis: false`).
4. **`rw_kvflow`** — Pan et al. *KVFlow: Efficient Prefix Caching for Accelerating LLM-Based Multi-Agent Workflows*, arXiv:2507.07400 (2025). `[title+abstract]` (verified via arXiv API 2026-08-15); representative of the ≥5-paper agent-aware cache cluster.
   - `input_output_framing`: agent-workflow structure in → workflow-aware KV eviction/prefetch policies out.
   - `comparison`: `problem_alignment: related` (optimizes agent cache reuse, but treats step *content* generically) · `method_addresses: false` for our estimand — it improves reuse without measuring which step semantics destroy it, so it cannot answer "how much invalidation is verification-attributable" · `effectiveness: n/a` · `threat_to_motivation: low` · `gap_type: not_considered` · `gap_we_address`: "cache policies are workflow-structure-aware but step-semantics-blind; the verification-output churn channel is unmeasured" · `role: related_for_context`.
   - `limitations`: `lim_kvcluster_semantics_blind` (`verify_as_hypothesis: false`).

- `changes_made` (refiner): demoted three under-engaged works to the general tier; added the serving-systems and test-time-verification canon to the landscape; carried the seed's novelty-ledger deltas into the comparison blocks verbatim rather than re-deriving softer ones; wrote the `hypothesis_to_verify` for the nearest neighbor as a complete falsifiable statement.
- `declined_to_fix`: none.

**Confirmed Stage 3** — 17 general + 4 specific; 1 limitation flagged `verify_as_hypothesis: true` (`lim_costaware_no_trace_no_verify_object`); nearest neighbor named and repositioned, not buried.

---

## Stage 4 — Sub-Problems

### Round 1 (critic phase)

**draft_v1** (5 sub-problems):

- **`sp_attribution`** — *description:* Attribute a session's tokens, latency, and dollars to verification when retry-loop generation is causally downstream of a failed verification yet interleaved with genuine forward progress. *why_it_is_a_problem:* the cost share is the paper's headline estimand; an unprincipled attribution makes it arbitrary, and the field would be right to ignore it. *technical_challenge:* the trace contains no counterfactual "same session without verification"; naive rules are biased in known directions (direct-only undercounts by ignoring induced retries; everything-after-failure overcounts by absorbing unrelated progress) — the challenge is an attribution scheme whose bias direction is *known by construction* on each side, yielding a defensible interval rather than a false point. *source_limitation_ids:* `["lim_tracelab_no_verification_semantics"]`.
- **`sp_cache_interaction`** — *description:* Quantify how much prefix-cache reuse verification output destroys, beyond what equally long non-verification content would destroy. *why_it_is_a_problem:* prefill dominance means invalidated tokens are re-paid on every subsequent turn; a verification-blind account structurally understates verification's cost, and the invalidation channel is precisely what no cache-cluster paper measures (Stage 3). *technical_challenge:* invalidation is a joint function of content churn, position in context, and volume under a specific cache policy — attributing it to verification *content* requires holding position and volume fixed counterfactually, which behavioral data alone cannot do. *source_limitation_ids:* `["lim_kvcluster_semantics_blind"]`.
- **`sp_value_heterogeneity`** — *description:* Measure, per verification class (lint/type-check/unit/build/suite), both cost and information value on a common scale, from observational traces. *why_it_is_a_problem:* the seed's falsifiable claim is that classes have heterogeneous cost × heterogeneous value; if value turns out proportional to cost, granularity-aware scheduling is pointless and the premise honestly fails — so the profile must be measured, not assumed. *technical_challenge:* "information value" is not directly observed; any proxy (does the outcome change the agent's next action? does it predict eventual resolution?) is confounded by *when* agents choose to run each class — the full suite is run at endpoints, lint after edits — so raw class comparisons measure scheduling habits, not value. *source_limitation_ids:* `["lim_queueing_stylized_workloads", "__novel__"]` — the queueing model presumes these parameters; no prior work estimates them.
- **`sp_counterfactual_validity`** — *description:* Determine which rescheduling counterfactuals can be validly evaluated from traces at all, and evaluate each in the strongest regime available to it. *why_it_is_a_problem:* the headroom estimand is only as good as its evaluation's validity; the nearest neighbor's weakness (dollar-priced speculation with no trace grounding) is exactly this hole, so inheriting it would erase the delta. *technical_challenge:* replay is exact only for reschedules that leave the agent-visible sequence untouched; anything else is off-policy and needs live re-execution — the challenge is a checkable partition criterion plus an evaluation design on each side of it. *source_limitation_ids:* `["lim_costaware_no_trace_no_verify_object"]`.
- **`sp_matched_outcomes`** — *description:* Certify "matched resolve rate" statistically for reschedules that change agent-visible information. *why_it_is_a_problem:* $/resolved-task is meaningless if resolve rate silently degrades. *technical_challenge:* non-inferiority on a binary outcome at realistic resolve rates needs careful margins and power. *source_limitation_ids:* `["lim_costaware_no_trace_no_verify_object"]`.

**critique:**
- summary: Coverage is right (jointly solving these delivers all four Stage-1 outputs), sources resolve, and nothing is method-shaped. One real structural defect: the last two sub-problems are one problem wearing two names.
- comments:
  - `{severity: minor, field: "sp_counterfactual_validity / sp_matched_outcomes", anti_pattern: "overlap", comment: "sp_matched_outcomes is the live-side half of sp_counterfactual_validity's own partition: 'evaluate each side in its strongest regime' already implies the non-inferiority certificate on the live side (and Stage 1's objective states the two-certificate rule explicitly). Two sub-problems here would force Stage 5 either to invent a redundant method or to have one method serve two sub-problems — both artifacts of the split, not of the domain. Merge, keeping the statistical-certification content as the live-side technical challenge."}`
- decision: `move_to_refiner` (merge is a re-shelving of existing content).

### Refiner pass

- Merged into **`sp_counterfactual_validity`** (4 sub-problems total), whose `technical_challenge` now ends: "…on the replay side, exactness must be argued from the invariance predicate; on the live side, matching is statistical — a pre-registered one-sided non-inferiority margin on resolve rate, with power sized honestly for a binary outcome at realistic resolve rates, and an INCONCLUSIVE label (never a silent pass) when the confidence bound straddles the margin."
- `changes_made`: merged the overlapping pair; no other content touched.
- `declined_to_fix`: none.

**Confirmed Stage 4** — 4 sub-problems; 3 sourced from Stage-3 limitations, 1 dual-sourced with a stated `__novel__` decisive-component justification.

---

## Stage 5 — Method Design

### Round 1 (critic phase)

**draft_v1** (4 methods):

- **`m_cost_ledger`** → targets `sp_attribution`. *proposed_approach:* Parse each session into typed steps; compute direct verification cost exactly (execution seconds; feedback tokens injected into context). Define a *retry segment* structurally: the contiguous step span from a failed verification of target f to the next verification attempt of the same target. Report the verification-induced dollar share as the interval [ρ_cons, ρ_lib]: conservative = direct costs only; liberal = direct + all retry-segment generation. Dollar-ize under three pre-registered price vectors (API-metered; self-host GPU-hour; latency-weighted) and both cache policies; run the identical ledger on TraceLab and on self-run SWE-bench sessions. *key_insight:* pointwise attribution is unidentifiable from observational traces, but the decision the estimand feeds — is verification a first-class cost object? — needs only an interval whose two ends have *known-direction* bias; bounding replaces the counterfactual that doesn't exist. A single ledger also yields the robustness readout for free: recomputing it across price vectors, cache policies, and corpora tests whether the verdict is an artifact of any one accounting choice — one instrument, two readouts. *hypotheses:* ["H1: On TraceLab sessions passing integrity filters, the median session's verification-induced dollar share has conservative bound at least 0.15 and liberal bound at least 0.30; the premise is falsified if even the liberal bound falls below 0.10.", "H2: Every headline verdict (H1's threshold verdict, H3's ratio verdict, H6's headroom verdict) is invariant across the three price vectors, both cache policies, and both corpora; falsified if any verdict flips under any grid cell."]
- **`m_kv_replay`** → targets `sp_cache_interaction`. *proposed_approach:* Replay each session's request sequence through a radix-tree prefix-cache simulator (SGLang-style; plus a vLLM-style block-hash policy as the second policy), counting cache-hit vs re-prefilled tokens per request. Attribute invalidation by counterfactual re-rendering: (i) a volume-matched neutral-filler variant (same lengths and positions, inert content) isolates churn from volume+position; (ii) a canonicalized variant (verification output with volatile spans — paths, timestamps, durations, truncation boundaries — rewritten to stable forms) measures how much of the verification-attributable invalidation is format-driven. *key_insight:* unlike agent behavior, cache behavior is a deterministic function of the token sequence given a policy — so counterfactual attribution that is invalid behaviorally is *exact* here; re-rendering is a valid intervention on the cache even though it would be an invalid intervention on the agent. *hypotheses:* ["H3: Verification outputs account for a share of re-prefilled (invalidated) tokens at least 1.5 times their share of context tokens, under both cache policies; falsified if the ratio is at most 1.1 under either policy.", "H4: Canonicalizing volatile spans in verification output recovers at least half of the verification-attributable invalidation; falsified if recovery is below one quarter."]
- **`m_value_profiler`** → targets `sp_value_heterogeneity`. *proposed_approach:* For each verification class, estimate: cost (execution seconds, feedback tokens — direct from the ledger) and two value proxies — action-divergence (probability the agent's next action differs between pass and fail outcomes) and terminal relevance (how much the outcome shifts the probability of eventual resolution), both estimated within strata of observable pre-step context (session phase, files touched, diff size since last check of same class). *key_insight:* observational traces cannot yield causal per-class value, but scheduling needs only the *ordering* of value-per-dollar across classes; stratification on pre-step observables is sufficient for an ordering claim and its failure is detectable (empty or non-overlapping strata). *hypotheses:* ["H5: Across verification classes, median execution cost spans at least a factor of 10 (lint to full suite) while stratified action-divergence spans at most a factor of 3 — that is, value per dollar differs by at least a factor of 3 across classes; falsified (degenerate frontier) if cost and stratified value are proportional within a factor of 1.5."]
- **`m_two_tier_replay`** → targets `sp_counterfactual_validity`. *proposed_approach:* Partition candidate reschedules by the invariance predicate ι (agent-visible sequence byte-identical). Tier A (ι holds — e.g., batching verification executions, sandbox placement/prewarming, cache-aware scheduling of re-prefill, overlapping verification execution with the decode of the same turn): evaluate by exact replay; Δ$ is exact and resolve outcomes are the recorded ones by construction. Tier B (ι broken — e.g., granularity substitution, speculative continuation past predicted-pass verifications with rollback on failure): evaluate by live SWE-bench re-execution, paired by instance and seed across arms, reporting headroom only under the non-inferiority certificate; the pass/fail predictor for speculation is trained on TraceLab, frozen before any live run, with an oracle-predictor arm bounding achievable headroom from above. *key_insight:* the agent-visibility boundary converts one ill-posed off-policy evaluation into two well-posed ones — an exact simulation and a small live experiment — and the boundary, not simulator fidelity, is what makes each headroom claim valid; the oracle/frozen pair then decomposes Tier-B headroom into "exists" vs "reachable at realistic predictor quality." *hypotheses:* ["H6: Tier-A rescheduling alone recovers at least 10% of the median session's total serving dollars at byte-identical outcomes; falsified if the recovered share is below 5%."]

**critique:**
- summary: No goal-restatement; every hypothesis carries a floor and a falsification direction; the two-readouts bundling in the ledger is justified. Two real flags: the value profiler's identification story is one assumption short of honest, and one hypothesis quietly depends on another's magnitude without saying so.
- comments:
  - `{severity: major, field: "m_value_profiler", anti_pattern: "mismatch (method does not fully answer its sub-problem's stated challenge)", comment: "sp_value_heterogeneity's technical_challenge names the confound precisely: class choice is entangled with session phase and context. The method answers with stratification but never states the condition under which stratification licenses even an ordering claim — overlap/positivity (each stratum must contain multiple classes) — nor what is reported when it fails. Without that, H5 is unfalsifiable in exactly the failure mode the sub-problem predicts: empty strata would silently produce a 'measured' frontier that is a scheduling-habit artifact. Required: a pre-registered positivity diagnostic and a pre-committed downgrade wording (frontier reported as descriptive-only, H5 scored INCONCLUSIVE) when overlap fails."}`
  - `{severity: minor, field: "m_two_tier_replay.hypotheses[H6]", anti_pattern: null, comment: "H6's floor (10% of total dollars) is not independent of H1: Tier-A recovery acts mostly on verification-induced cost, so H6's ceiling is roughly H1's liberal bound. State the coupling — 'if H1 fails at the 0.10 level, H6's floor is unreachable by construction and is scored against a re-based floor (half of the measured liberal share)' — or a single bad constant makes two hypotheses fail for one reason."}`
- decision: `move_to_refiner` — the positivity gate and the coupling clause are guard-rail additions to existing machinery, not new mechanisms; within the conservative remit.

### Refiner pass

- `m_value_profiler.proposed_approach` (extended): "…Positivity gate (pre-registered): a stratum enters the estimate only if it contains at least 30 steps from each of at least two verification classes; the profile is reported with per-stratum counts, and if fewer than half of the pre-defined strata pass the gate, the frontier is reported as *descriptive only* and H5 is scored INCONCLUSIVE rather than PASS/FAIL — the failure of overlap is itself reported as a finding about how tightly agents' verification habits are phase-locked."
- `m_two_tier_replay.hypotheses[H6]` (extended): "…If H1 is falsified at the 0.10 level, H6's absolute floor is unreachable by construction and H6 is instead scored against a re-based floor of half the measured liberal share, with the re-basing stated in the report." 
- `changes_made`: added the positivity gate + INCONCLUSIVE downgrade; made the H1→H6 coupling explicit.
- `declined_to_fix`: none.

**Confirmed Stage 5** — 4 methods, **6 mechanism-tier hypotheses** (H1, H2 | H3, H4 | H5 | H6 — the ledger and the cache replay each carry two under a one-instrument-two-readouts justification), plus the **1 framing-tier hypothesis** held at Stage 3 (`lim_costaware_no_trace_no_verify_object.hypothesis_to_verify`, the speculation-viability claim). 7 falsifiable hypotheses total feed Stage 6.

---

## Stage 6 — Experiment Design

**Tier accounting (checked against `study_type: empirical`):**
- **Mechanism-tier: 6 RQs**, one per Stage-5 hypothesis, `target_hypotheses` verbatim.
- **Framing-tier: 1 RQ**, targeting the Stage-3 `hypothesis_to_verify` on `lim_costaware_no_trace_no_verify_object`, verbatim.
- **Outcome-tier: 0 RQs** — empirical study; no reschedule is framed as "our scheduler beats X." The native schedule is the *object of measurement*; counterfactual policies are probes of avoidable cost.

### Round 1 (critic phase)

**draft_v1:**

`datasets`:
- TraceLab (arXiv:2606.30560) — *justification:* the only public corpus at session granularity with typed tool calls (test/build/edit distinguishable), ~4,300 sessions / 430K tool calls per the seed card (corpus facts re-verified against the release in Phase B, gate A1); carries RQ1–RQ5 and the predictor training for RQ7.
- Self-run SWE-bench Verified sessions (Jimenez et al., 2024) under two scaffolds (OpenHands; SWE-agent), 300 instances × 2 scaffolds × 3 seeds per arm — *justification:* live arms are the only valid evaluation regime for Tier-B reschedules (Stage 5), and running the identical ledger on self-run sessions is the cross-corpus half of H2.
- Serving cost model: SGLang-style radix cache + vLLM-style block-hash policy; three price vectors (API-metered, self-host GPU-hour amortized, latency-weighted), all frozen before measurement.

`baselines` (sanity-check comparators, not competitors): the native agent schedule (the recorded behavior — the measured object); a shuffled-step-type placebo (B0: attribution rules applied to randomly re-labeled step types must yield share ≈ token share and invalidation ratio ≈ 1 — non-null placebo invalidates the attribution pipeline before any hypothesis is scored); the volume-matched neutral-filler re-rendering (the cache-side placebo/control from Stage 5).

`research_questions` (draft): rq_cost_share (H1), rq_verdict_stability (H2), rq_cache_ratio (H3), rq_canonicalization (H4), rq_frontier (H5), rq_tier_a (H6) — v1 phrased rq_tier_a's description as "does the cost-optimal verification-aware scheduler cut $/resolved-task by ≥10% versus the agent-native policy?" — and rq_speculation (framing, Stage-3 hypothesis), with δ = 2pp non-inferiority margin on resolve rate.

**critique:**
- summary: Tier accounting and verbatim traceability check out; two design defects, one of them the kind a reviewer would kill on.
- comments:
  - `{severity: major, field: "research_questions[rq_speculation].sample_size_rationale", anti_pattern: "under-powered non-inferiority (mined-checks: stochasticity/variability)", comment: "At baseline resolve rate ≈ 0.40 with n = 900 paired runs per arm, the standard error of a between-arm resolve-rate difference is ≈ 2.2pp even before clustering by instance — a δ = 2pp one-sided non-inferiority margin is *undecidable* at this n: the CI will straddle the margin almost regardless of truth, guaranteeing INCONCLUSIVE. Either the margin widens to δ = 5pp with an instance-paired (McNemar-style discordant-pair) test, which the paired design's variance reduction makes decidable at n = 900, or n must grow ≈ 6×, which the compute note rules out. Widen the margin, state the power calculation, and pre-declare INCONCLUSIVE for a straddling CI."}`
  - `{severity: major, field: "research_questions[rq_tier_a].description", anti_pattern: "tier_violation (beats-baseline framing in an empirical study)", comment: "'does the cost-optimal scheduler cut $/resolved-task versus the agent-native policy' is outcome-tier language — procedure-beats-baseline — which study_type=empirical forbids, and it also misstates the estimand: Tier A's claim is a property of the *workload* (what share of the recorded bill is avoidable at byte-identical outcomes), for which the policy is the probe. Rephrase as headroom measurement; the falsification floor already lives in H6 and does not change."}`
- decision: `move_to_refiner` — margin/power arithmetic and description rephrasing change design parameters and wording, not the plan's structure.

### Refiner pass — confirmed Stage 6 output

- `rq_speculation.sample_size_rationale` (refined): "n = 300 instances × 3 seeds = 900 paired runs per arm, paired by (instance, seed) across arms. Non-inferiority margin widened to δ = 5pp (one-sided α = 0.05) on the paired difference, tested via the discordant-pair (McNemar-style) construction: with an expected discordance rate ≤ 0.15, power ≥ 0.8 to certify non-inferiority when the true difference is 0. A confidence bound straddling the margin is pre-declared INCONCLUSIVE — reported as such, never as a silent pass. δ = 2pp at this n is undecidable and was rejected in review."
- `rq_tier_a.description` (refined): "What share of the recorded serving bill is avoidable by agent-transparent rescheduling alone — i.e., the Tier-A headroom of the workload at byte-identical outcomes — measured by exact replay under the frozen cost model?"
- `changes_made`: widened and power-justified the non-inferiority design; reframed rq_tier_a as headroom measurement.
- `declined_to_fix`: none.

**Confirmed Stage 6** — 7 RQs (6 mechanism + 1 framing + 0 outcome):

| rq_id | tier | target_sub_problem_id | target_hypotheses (source, verbatim) |
|---|---|---|---|
| `rq_cost_share` | mechanism | `sp_attribution` | H1 (m_cost_ledger) |
| `rq_verdict_stability` | mechanism | `sp_attribution` | H2 (m_cost_ledger) |
| `rq_cache_ratio` | mechanism | `sp_cache_interaction` | H3 (m_kv_replay) |
| `rq_canonicalization` | mechanism | `sp_cache_interaction` | H4 (m_kv_replay) |
| `rq_frontier` | mechanism | `sp_value_heterogeneity` | H5 (m_value_profiler) |
| `rq_tier_a` | mechanism | `sp_counterfactual_validity` | H6 (m_two_tier_replay) |
| `rq_speculation` | framing | `sp_counterfactual_validity` | Stage-3 `hypothesis_to_verify` on `lim_costaware_no_trace_no_verify_object` |

(Per-RQ setup, sample-size rationale, statistical test, expected outcome, falsification condition, and metrics are rendered in `experiment_design.md` and mirrored in the paper draft's Experiments section; every number there is an authored design target with a stated rationale, not a fabricated fact.)

---

## Cross-stage consistency check (final pass, all six stages)

1. **No method leak in Stages 1/2/4** — checked. The one leak that existed (speculative continuation named in Stage 1 v1's summary) was caught and removed in Stage 1 round 1; Stage 4's sub-problems name no mechanism.
2. **ID stability** — no ID renamed after confirmation. The one structural change (Stage 4's merge of `sp_matched_outcomes` into `sp_counterfactual_validity`) happened *before* Stage 4 was confirmed, and the retired ID appears nowhere downstream.
3. **Reference integrity** — every `source_limitation_ids` entry ∈ Stage 3 limitations or `__novel__` ✓ (`lim_tracelab_no_verification_semantics`, `lim_kvcluster_semantics_blind`, `lim_queueing_stylized_workloads`+`__novel__`, `lim_costaware_no_trace_no_verify_object`); every Stage-5 `target_sub_problem_id` ∈ Stage 4's four ✓; every Stage-6 mechanism-tier `target_hypotheses` is a verbatim match to a Stage-5 hypothesis ✓; the framing-tier RQ's hypothesis is the verbatim Stage-3 `hypothesis_to_verify` on the one limitation flagged `verify_as_hypothesis: true` ✓.
4. **Hypothesis↔RQ recount (literal):** Stage 5 carries 6 mechanism hypotheses (m_cost_ledger: H1, H2; m_kv_replay: H3, H4; m_value_profiler: H5; m_two_tier_replay: H6). Stage 3 carries 1 flagged hypothesis_to_verify. Total falsifiable hypotheses = **7**. Stage 6 carries **7 RQs**: 6 mechanism + 1 framing. Count matches 7 = 7; no hypothesis uncovered; no RQ without a source; no outcome-tier RQ exists ✓.
5. **Output coverage** — Stage 1's four outputs each reach Stage 6: decomposition → rq_cost_share (+ rq_verdict_stability for its robustness); invalidation estimate → rq_cache_ratio + rq_canonicalization; per-class profile → rq_frontier; headroom → rq_tier_a + rq_speculation. Nothing promised in Stage 1 falls off the chain ✓.
6. **`study_type` consistency** — `empirical` throughout; Stage 6 emits 0 outcome-tier RQs, and the one beats-baseline phrasing that crept in was caught at Stage 6 round 1 ✓.

**What was hardest:** keeping the *headroom* half of the paper from quietly becoming a method paper. Three separate rounds (Stage 1's method-leak flag, Stage 5's H1→H6 coupling note, Stage 6's tier-violation flag) are all the same pressure surfacing in different stages — the seed card's own falsifiable claim is written in beats-baseline language ("$/resolved-task 降低 ≥X%（相对 agent 原生策略）"), and every stage had to re-translate that into a measurement estimand (avoidable share of the recorded bill) without weakening its falsifiability. The second recurring tension was engagement honesty in Stage 3: the occupancy-sweep one-liners are confident, but promotion to the deep tier had to track what was actually read in this environment, not what the sweep asserts.

**Total rounds:** 6 stages × 1 critic round + 1 refiner pass each = 6 critic rounds, 6 refiner passes. Majors fired in Stages 1, 2, 3, 5, 6 (Stage 4 fired a structural minor); every major was resolved within its stage's refiner pass under the formalize-level rule; no round cap hit; no cross-stage backup required.
