# Research Taste Audit — B2.2

> Skill: `research-taste-auditor` (Chen, Zhao & Cohan, arXiv:2607.01233). Run once, on the core idea (Motivation + Method) confirmed at Stage 2 / Stage 5 of the discussion-loop run, **before** final paper assembly — per the skill's own guidance ("cheaper to catch before drafting than after").

## 1. Extracted idea

**Motivation** (Stage 2, confirmed): "Counterfactual replay is the only causally verified way to attribute a long agent trajectory's failure to a specific step, but every replay re-invokes real LLM and tool calls, and current replay-based attribution systems spend that budget exhaustively — replaying one step at a time — without ever asking how few replays would have sufficed... different teams and different failures warrant different budgets, so a single recommended budget cannot serve both regimes — only a full cost-accuracy curve lets a team read off the accuracy it would get at its own budget."

**Method** (Stage 5, summary-level): "We build a checkpointed replay harness that bills every probe in position-dependent replay units, construct a replay-verified fault-injected trajectory corpus balanced across plan/tool/execution layers, localize the decisive step with bisection over checkpoint indices and noise-tolerant group testing (each de-noised by an explicit vote count), measure the monotonicity-violation rate of the replay signal as the load-bearing predictor of where bisection's shortcut holds, and characterize where group testing's redundancy overtakes vote-multiplied bisection as oracle noise and layer-crossing increase — comparing all strategies against budget-matched uniform sampling, an exhaustive per-step scan, and a zero-replay log-only judge on identical trajectories at matched budgets."

## 2. Taxonomy labels

**Opportunity Pattern:** primary **Evidence Gap** (secondary: **Resource Bottleneck**)
- rationale: the motivation's load-bearing claim is "without ever asking how few replays would have sufficed" / "no accuracy-vs-replay-budget tradeoff is characterized anywhere" — a diagnosability/measurement absence ("no benchmark for," "hard to measure" in `taxonomy.md`'s trigger language), not a "two literatures never connected" framing. The secondary Resource Bottleneck reading is licensed by the seed's own `[资源]`/Resource framing and by "every replay re-invokes real LLM and tool calls" — progress is blocked by a scarce, costly resource (replay budget), which is a distinct axis from the measurement-absence claim but co-present in the same motivation.
- Explicitly **not** Bridge Opportunity: there is no "delta debugging and LLM-agent attribution have developed in isolation" clause anywhere in the confirmed motivation. Stage 3's refiner pass went out of its way to state the opposite explicitly: "This paper does not propose bisection or group testing as new algorithms... ddmin remains the conceptual ancestor whose assumptions this paper explicitly tests, not a runnable baseline to beat" — i.e., the draft was specifically checked for, and did not fall into, a "let's connect classical search theory to agent trajectories" framing.

**Method Paradigm:** primary **Empirical Mapping** (secondary: none clearly licensed)
- rationale: "we build a harness... construct a corpus... localize... measure the monotonicity-violation rate... characterize where group testing overtakes bisection" is systematic measurement/characterization, matching `taxonomy.md`'s "we measure/characterize/quantify/localize" trigger language directly. There is no "we integrate/unify two prior methods into one" framing — bisection and group testing are each run and characterized as separate arms with distinct, falsifiable per-arm hypotheses (Stage 5), not glued into one combined mechanism. A candidate secondary label, Optimization/Search (since bisection/group testing are search strategies), was considered and rejected: the paper's own stance (Stage 3 refiner) is explicit that these are *not* proposed as an optimization contribution — they are treated as instruments under test, which keeps the method-axis label a clean, single Empirical Mapping rather than a hedge.

## 3. Diagnostics

- `surface_stitching` = **0** — not an "A + B" combination. The five methods (cost accounting, bisection+monotonicity diagnostic, vote de-noising, group-testing+layer-crossing, budget-matched comparison suite) are not two pre-existing methods glued with a connecting verb; each is a purpose-built instrument or diagnostic for one of the five sub-problems, and the "combination" of running five instruments together is the measurement design itself, not a stitched novel method.
- `bottleneck_specificity` = **3** — the target is exact and nameable at every step: *which* two search strategies (bisection vs. group testing), *which* invariant (the g(k) step-function / monotonicity-violation rate), *which* cost unit (resumed LLM calls, not probe count), *which* layer (plan-layer specifically, for the layer-crossing-design hypothesis), *which* noise parameter (vote count r, flip rate p). Matches or exceeds the human baseline (2.56) and the strongest tested models (2.3–2.6).
- `boilerplate` = **1** — mostly load-bearing; the one soft clause is "as agent trajectories grow longer, manual log inspection... becomes prohibitively expensive and inconsistent," which is a somewhat generic scaling-pain framing, but it is immediately anchored to a specific, cited claim (Who&When's own reported step-level attribution weakness) rather than left as free-floating filler.

## 4. Dominant verb(s)

Method sentence's main verbs: **build, construct, localize, measure, characterize**. `localize` is explicitly in the human-heavy archetype cluster (grouped with *isolate, disentangle*); `measure` and `characterize` are neutral, task-specific verbs typical of Empirical Mapping papers, not connecting verbs. No instance of *integrate/unify/merge/adapt/combine/leverage/bridge* appears in a claim position anywhere in the extracted idea — even where a cross-domain move is genuinely present (delta debugging → LLM-agent trajectories), the write-up leads with the specific violated assumption (cheap/deterministic/repeatable test) rather than "connecting" the two literatures, per `archetype-verbs.md`'s cross-domain-transfer distinction.
Archetype family: **human-heavy / neutral**.

## 5. Verdict

| # | Condition | Fired? |
|---|---|---|
| 1 | Opportunity = Bridge Opportunity AND Method = Synthesis/Unification | **No** |
| 2 | surface_stitching ≥ 2, OR boilerplate ≥ 2, OR bottleneck_specificity ≤ 1 | **No** (0 / 1 / 3) |
| 3 | Dominant verb from the LLM-heavy archetype list | **No** (localize/measure/characterize/build/construct) |

**Verdict: 🟢 Reads as human-shaped.** No condition fires — a clean pass on all three independent checks, not merely "no worst-case flag."

## 6. Interpretation (why this matters for "avoiding homogeneous output")

This is a genuinely useful result, not a rubber stamp: the seed material (`paper.md` Step 0/Step 3) had *already* run its own informal asymmetry/bridge/synthesis self-check before this audit even started, and its Step 3 explicitly considered and rejected both a Bridge framing ("connect delta-debugging / group testing to LLM failure attribution") and a Synthesis framing ("apply bisection + group testing + BAI to trajectories"), reframing around the state-inheritance-monotonicity invariant instead. This audit is independent confirmation using a different, externally-sourced taxonomy (not the same prompt logic that wrote `paper.md`), applied specifically to the *pipeline's own* Stage 2/5 language (drafted fresh in this run, not copy-pasted from `paper.md`) — and it agrees.

The place this idea was genuinely at the most risk of a flag is exactly the cross-domain-transfer case `archetype-verbs.md` calls out by name: taking a classical CS technique (bisection / delta debugging / group testing) into a new domain (LLM-agent trajectories) is precisely the kind of move that gets *written up* in Bridge/Synthesis language by default. The reason this idea escapes that trap is structural, not just phrasing-deep: Stage 3's refiner pass forced an explicit statement that the contribution is *not* the search algorithms themselves but the characterization of where their founding assumptions break (the monotonicity-violation rate) — which is what pushes the write-up onto Evidence Gap / Empirical Mapping instead of Bridge Opportunity / Synthesis, exactly the reframe pattern `archetype-verbs.md` describes as "leading with a specific insufficiency and a specific operation" rather than "connecting the two literatures."
