# Research Taste Audit — B1.6

> Skill: `research-taste-auditor` (Chen, Zhao & Cohan, arXiv:2607.01233). Run once,
> on the core idea (Motivation + Method) confirmed at Stage 2 / Stage 5 of the
> autoclaude discussion-loop run, **before** final paper assembly — per the skill's
> own guidance ("cheaper to catch before drafting than after"). This topic had **no
> pre-registered `paper.md`** self-audit to lean on (unlike B5.5), so this pass is the
> first idea-level taste check the idea receives, and is run at full strength.

## 1. Extracted idea

**Motivation** (Stage 2, confirmed): "A just-published security study establishes that
LLM agents hallucinate skill names at scale, that the names recur predictably enough to
be squatted, that no model can flag them better than chance, and that every one of its
four recommendation-time defenses buys a lower hallucination rate only by destroying
usefulness. All four share one structural property: they intervene on the recommendation
distribution — what the model is allowed to *say* — which is exactly why they collapse
recall, because a real but training-atypical skill name looks identical to a hallucinated
one to a filter on the model's output. An install-time provenance gate does not touch
that distribution at all; and a bare *existence* check cannot substitute, because the
attack is squatting — once the attacker registers the hallucinated name, 'the name
exists' is true for the malicious skill."

**Method** (Stage 5, summary-level): "Insert a gate immediately before install that keys
*only* on publisher-trust-tier provenance metadata — no name lookup, no name-similarity
heuristic, no LLM judgment — and measure, in a multi-step trajectory that embeds a
recommend-then-install decision, the (compromise-block, legitimate-reject) operating
point, how it moves as the check is delayed, and the recovery cost; a bare-existence gate
serves as the placebo, and the recurrence-seeded squatting set is confined to offline
adversary/ground-truth construction, never read by the gate."

## 2. Taxonomy labels

**Opportunity Pattern:** primary **Failure / Risk Gap** (secondary: **Evidence Gap**)
- rationale: the load-bearing motivation clause is "every one of its four defenses buys a
  lower hallucination rate only by *destroying usefulness*" and "a bare existence check
  *cannot substitute* because the attack is squatting" — the existing defenses are brittle
  / unsafe (Failure-Risk), and the install-time intervention point is *unmeasured*
  (Evidence Gap). There is no "two literatures have developed in isolation" clause anywhere.
- Explicitly **not** Bridge Opportunity: the idea does not connect two disconnected fields;
  it relocates a checkpoint within *one* pipeline (recommendation → install) and swaps one
  signal for another (name-existence → publisher-provenance). The tool-use references
  (ToolLLM, Self-RAG) are cited as *contrast* — mechanisms that assume the tool set is
  trustworthy — not as a literature to be fused with security work.

**Method Paradigm:** primary **Empirical Mapping** (secondary: **Robustification**)
- rationale: "measure ... the operating point, how it moves as the check is delayed, and
  the recovery cost" is characterization/measurement instrumentation — the harness + gate
  are the instrument, the operating point + timing curve are the result (digest N12
  `empirical`). The secondary Robustification reading is licensed because the intervention
  *does* reduce a documented failure (squatted installs); but the paper's claim is the
  *measurement* of that reduction and its usability cost, not "we built a more robust
  system," which is why Empirical Mapping is primary.
- Explicitly **not** Synthesis/Unification: nothing is integrated, unified, or reconciled;
  a single mechanism is placed at a specific point and its effect is measured.

## 3. Diagnostics

- `surface_stitching` = **0** — not an "A + B" glue. There is exactly one mechanism (a
  provenance-tier check) placed at one point (pre-install). The Stage-5 critic round
  actively *removed* the one place where a second signal (name-recurrence matching) had
  been fused into the gate, precisely to keep the mechanism single and clean. No pair of
  pre-existing methods is being combined.
- `bottleneck_specificity` = **3** — the target is exact and nameable at every step: the
  precise *intervention point* being moved (recommendation-time → install/execution-time),
  the precise *signal* being swapped (name-existence, which squatting defeats → publisher-
  trust-tier provenance), and the precise *quantity* measured (the (block, reject) operating
  point + detection-lag-to-cost curve). Meets/exceeds the human baseline (2.56) and the
  strongest tested models (2.3–2.6).
- `boilerplate` = **1** — mostly load-bearing; the one soft clause is "keeping delegated
  agent transactions safe" governance framing, which is slightly generic but still ties to
  a specific claim (install-time vs recommendation-time intervention) rather than being
  swappable filler.

## 4. Dominant verb(s)

Method sentence's main operations: **relocate** (the checkpoint), **replace** (existence
with provenance), **measure** (the operating point / timing). `replace` is the single most
human-heavy verb in the archetype data (83.3% human-authored, log-odds strongly negative
for models); `decouple`/`isolate` also appear (the offline recurrence set is *decoupled*
from the online gate's inputs, and the delayed-gate control *isolates* timing). `measure`
is a neutral Empirical-Mapping verb. No instance of *integrate / unify / merge / adapt /
combine / leverage / bridge* appears in a claim position anywhere in the extracted idea.
Archetype family: **human-heavy / neutral**.

## 5. Verdict

| # | Condition | Fired? |
|---|---|---|
| 1 | Opportunity = Bridge Opportunity AND Method = Synthesis/Unification | **No** (Failure-Risk / Empirical-Mapping) |
| 2 | surface_stitching ≥ 2, OR boilerplate ≥ 2, OR bottleneck_specificity ≤ 1 | **No** (0 / 1 / 3) |
| 3 | Dominant verb from the LLM-heavy archetype list | **No** (relocate / replace / decouple / measure) |

**Verdict: 🟢 Reads as human-shaped.** No condition fires — a clean pass on all three
independent checks, not merely an absence of the worst-case flag.

## 6. Interpretation (honest, not a rubber stamp)

This is a genuine 🟢, and it is worth naming *why* it clears the bar so cleanly, because
the topic sits one step from a framing that *would* have flagged. A lazier write-up of the
same underlying idea — "supply-chain security and agent tool-use have been studied
separately; we bridge them with a trust-aware install pipeline" — would land squarely in
the Bridge+Synthesis cell (🔴). The idea escapes that not by luck but because two
construction decisions, both made during the discussion loop, pushed it off the template:

1. The **Stage-1 objective reframe** turned "our gate *beats* the four published defenses"
   (an outcome-tier, method-competition framing that drifts toward "we built a better
   system") into "measure where the install-time operating point *lands* relative to the
   published frontier" (Empirical Mapping). The verb moved from *beat/build* to *measure*.
2. The **Stage-5 gate correction** stripped the name-recurrence signal out of the gate's
   verdict path, leaving a single provenance predicate. That is what drove
   `surface_stitching` to 0 — had the gate fused provenance + name-similarity, this would
   have read as an "A + B" combination (🟡 at least).

Neither decision was cosmetic; both were forced by evidence-grounded `[major]` flags in
the trace. The auditor's role here is independent confirmation, from a taxonomy the
discussion loop did not use, that those two moves left the idea in the human-shaped region.
No reframe is required; no flag is manufactured.

**One caveat carried forward (not a taste flag, a novelty-margin note):** digest N2/N10
t1 flag that a provenance gate is a fairly direct reading of the base paper's own closing
call for "verified recommendation pipelines." That is a *novelty* concern (does the
mechanism add enough over the base paper's own sentence), addressed by leading the paper
with the measured operating point + timing curve rather than the gate idea — not a *taste*
concern (the idea is not Bridge+Synthesis-shaped). The two are distinct; this audit speaks
only to the second, and the taste verdict stands 🟢.
