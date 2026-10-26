# Research Taste Audit — T3.4

> Skill: `research-taste-auditor` (Chen, Zhao & Cohan, arXiv:2607.01233). Run once, on the core idea (Motivation + Method) confirmed at Stage 2 / Stage 5 of the discussion-loop run, **before** final paper assembly — per the skill's own guidance ("cheaper to catch before drafting than after").

## 1. Extracted idea

**Motivation** (Stage 2, confirmed): "Pinning — repeating every standing constraint verbatim in every turn — is the default, lowest-effort engineering fix for making sure an LLM agent 'sees' safety rules, user preferences, and policy constraints, but nothing establishes whether this practice continues to work as standing constraint sets scale from a handful of rules to the hundreds now typical of production deployments... telling a deployer 'just cap the constraint count below the knee' is not actionable when the standing rule count is not the deployer's free choice — the live decision a deployer actually faces is not *how many* rules to have on the books, but *which bounded subset* needs to be resident in context at a given step."

**Method** (Stage 5, summary-level): "We build a factorial constraint-count sweep harness that deconfounds constraint count from raw prompt length and from applicability density, instrument full pinning's token overhead directly against task success to locate (or rule out) a breakpoint, evaluate a family of budget-capped, step-conditioned selective-pinning policies — including an applicability-aware classifier tested against similarity-based selectors — against a random-*k* floor, and gate every violation-rate curve behind a human-calibrated dual-mode detector."

## 2. Taxonomy labels

**Opportunity Pattern:** primary **Evidence Gap** (secondary: **Resource Bottleneck**)
- rationale: the motivation's load-bearing claim is "nothing establishes whether this practice continues to work" / "no corpus paper jointly measures violation rate, token overhead, and task success while sweeping the count of simultaneously active constraints" (digest N4) — a measurement/diagnosability absence, not a "two literatures never connected" framing. The secondary Resource Bottleneck reading is licensed by the concrete mechanism named: "the token cost of verbatim repetition grows linearly with rule count" against a fixed per-turn budget — a scaling/cost limit, not a cross-domain synthesis.
- Explicitly **not** Bridge Opportunity: there is no "X and Y have developed in isolation" clause anywhere in the motivation; `paper.md`'s own Step 0 independently arrived at the same asymmetry framing (token-price-for-presence vs. attention-budget-price-for-compliance) and its Step 3 self-audit already rejected a bridge reading, explicitly naming COMI and RECAST as "instruments, not the other side of a bridge."

**Method Paradigm:** primary **Empirical Mapping** (secondary: **Optimization/Search**)
- rationale: "we build a harness... instrument... evaluate a family of selectors... gate" is characterization/measurement instrumentation — a controlled sweep that locates (or rules out) a breakpoint, not "integrate/unify" two existing methods. The secondary Optimization/Search reading comes from the selective-pinning policy family itself: choosing which bounded subset of constraints to keep resident under a fixed token budget *k* is a genuine budget-allocation move, distinct from the measurement apparatus that evaluates it.
- Explicitly **not** Synthesis/Unification: COMI's marginal-gain scorer is reused as *one comparison arm among five* inside the sweep, not glued together with another method to form the paper's contribution — the contribution is the deconfounded measurement design and the knee-location/detector-gating apparatus around it, which is purpose-built.

## 3. Diagnostics

- `surface_stitching` = **0** — not an "A + B" combination. COMI's selector is one of five *evaluated conditions* inside a larger design, not a component glued into the paper's own claimed mechanism. The novel apparatus (factorial count⊥length⊥density deconfounding, the breakpoint test, the dual-mode detector gate) is purpose-built for this identifiability problem, not assembled from two prior methods.
- `bottleneck_specificity` = **3** — the target is exact and nameable at every step: *which* budget (per-turn token count), *which* three axes are deconfounded (count, length, density), *which* statistical test locates the breakpoint (segmented regression + Davies test), *which* five selectors and *which* one distinguishes applicability from similarity. Matches or exceeds the human baseline (2.56) and the strongest tested models (2.3–2.6).
- `boilerplate` = **1** — mostly load-bearing; the one soft clause is "production policy/safety/preference sets" in the motivation, a slightly generic descriptor of constraint types, but it is still tied to a specific claim (what kinds of constraints accumulate independent of task need) rather than being swappable filler.

## 4. Dominant verb(s)

Method sentence's main verbs: **build, deconfound, instrument, evaluate, gate**. None of these appear on the LLM-heavy list (`integrate, unify, merge, adapt, combine, leverage, bridge, reconcile`); `deconfound` and `gate` in particular are precise, mechanism-naming verbs in the same register as the human-heavy family (`isolate, separate, disentangle`) even though they are not literally on either named list. `evaluate` and `instrument` are neutral, task-specific verbs. No instance of *integrate/unify/merge/adapt/combine/leverage* appears in a claim position anywhere in the extracted idea.
Archetype family: **human-heavy / neutral**.

## 5. Verdict

| # | Condition | Fired? |
|---|---|---|
| 1 | Opportunity = Bridge Opportunity AND Method = Synthesis/Unification | **No** |
| 2 | surface_stitching ≥ 2, OR boilerplate ≥ 2, OR bottleneck_specificity ≤ 1 | **No** (0 / 1 / 3) |
| 3 | Dominant verb from the LLM-heavy archetype list | **No** (build/deconfound/instrument/evaluate/gate) |

**Verdict: 🟢 Reads as human-shaped.** No condition fires — not merely "no worst-case flag," but a clean pass on all three independent checks.

## 6. Interpretation (why this matters for "avoiding homogeneous output")

This is a genuinely useful result, not a rubber stamp: the seed material (`paper.md` Step 0/Step 3) had *already* run its own informal asymmetry/bridge/synthesis self-check before this audit even started — the reverse-digest generation process for this topic was itself designed to reject the generic bridge-then-synthesize template, and its Step 3 table explicitly checked "is the opportunity a Bridge?" (PASS) and "is the method mere Synthesis?" (PASS, after flagging COMI-reuse as a risk and resolving it the same way this audit independently did). This audit is independent confirmation using a different, externally-sourced taxonomy (not the same prompt logic that wrote `paper.md`), and it agrees.

One point worth stating plainly rather than glossing over: the Stage-5 critique in `pipeline.md` found that `m_tradeoff_tracker` carries *zero* falsifiable hypotheses, disclosed as intentional rather than patched. That gap has no bearing on this audit — a hypothesis-free descriptive component doesn't change the idea's *shape* (it's still a measurement-instrument component, not a stitched-together one) — but it is exactly the kind of thing a taste audit does *not* catch and a stage reviewer does; the two skills are checking different failure modes, which is why both run in this pipeline.

The practical implication for the other topics in this collection: this specific pass (🟢, no manufactured flag) should not be read as "every topic in the set will pass automatically" — several other seeds may lean on a real cross-domain-transfer move that gets *written up* in bridge language by default (see `archetype-verbs.md`'s cross-domain-transfer note), or may have thinner Step-0/Step-3 self-audits than this one. The auditor is cheapest to run **per topic, right after Stage 2/5 confirm**, before committing to a full paper draft — flagging early is the entire point of running it here rather than after the draft is written.
