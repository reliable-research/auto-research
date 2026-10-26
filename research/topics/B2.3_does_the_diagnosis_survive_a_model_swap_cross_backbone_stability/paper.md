# Does the Diagnosis Survive a Model Swap? Cross-Backbone Stability of Failure Attribution — Pre-Registered Paper Specification

> Generated from digest.md + README.md. Status: specification, no experiments run. All thresholds below are pre-registered decision rules, not results.

## Step 0 — Core Asymmetry (升维)

**The asymmetry**: Programmatic fault injection holds the *cause* of an agent failure invariant across backbones, but nothing holds its *evidence* invariant — the injected layer is fixed by construction while the trace that any attribution procedure must read is a function of the executing backbone — so every plan/tool/execution label silently asserts an invariance class (task-property) that its measurement pipeline never possessed.

**判据 test (domain-noun deletion)**: delete "fault injection", "agent failure", "backbone", "injected layer", "trace", "attribution label":
> "X holds the cause of Y invariant across Z, but nothing holds its evidence invariant — the \_\_ is fixed by construction while the \_\_ that any procedure must read is a function of Z — so every \_\_ silently asserts an invariance class its measurement never possessed."

Without the nouns the sentence has no truth value: there is no generic reason "evidence" should vary with Z when "cause" does not. The claim's entire force is the specific empirical fact that LLM backbones transform identical injected causes into divergent observable failure signatures (digest C2) read by backbone-sensitive judges (C1, C5). It is not a bridge ("attribution and backbone-swapping were never connected") — it names a mismatch between what a label *claims to be invariant to* and what its computation *is actually a function of*.

## Step 1 — Estimand (guidance.md R1)

**One-sentence estimand**: the chance-corrected cross-backbone agreement (Fleiss' κ on the failing intersection $\mathcal{I}$, or Krippendorff's α when $\Omega$ is low) of the plan/tool/execution attribution label assigned by a fixed judge to the same injected-fault cell, over the population of (task, fault-layer) cells drawn from GAIA/WebArena-style agent benchmarks executed by a fixed set of LLM backbones — feeding the decision of whether single-backbone failure-attribution claims may be reported as task properties or must be re-scoped as (task, backbone)-pair properties (CO4).

*(Added at Phase A re-run per guidance.md Part 6 item 1 / Part 3.4 R1 — the quantity, unit of analysis [one (task, fault, backbone) cell], reference population [GAIA/WebArena-style fault-injection cells], and the decision it feeds [CO4's re-scoping guidance] were previously scattered across Steps 0/2/5 but never stated as one sentence.)*

## Step 2 — Archetype

**Primary**: `empirical` (measurement study), per digest N12 — the deliverable is a measured quantity (cross-backbone agreement of attribution labels) about existing systems, in the pattern of Emergent-Abilities-Mirage / LLMs-Get-Lost.
**Secondary**: `conceptual_framework` (CO1) — the measurement protocol (fault suite + factorial + censoring metrics) is a reusable instrument, subordinate to the finding.

Downstream consequences:
- **(a) Abstract contribution slot**: a number with an interpretation rule — "κ = \_\_ overall, decomposed into agent/judge/style shares" — not a method or a benchmark. The suite appears only as the instrument that made the number credible.
- **(b) Intro logic**: not "what becomes possible" and not "we beat X"; the intro must establish that a widely-consumed quantity (failure-attribution labels: Who&When, AgenTracer, MAST) has an unmeasured validity dimension, and that either measurement outcome changes how that quantity may be reported (seed: 结论无论正反都有信息量).
- **(c) Evidence standard for Results**: pre-registered thresholds decided *before* data (this document), chance-corrected statistics with clustered uncertainty, censoring reported beside every agreement number, and the judge-vs-agent confound decomposed rather than assumed away. A single headline κ without the overlap rate and variance decomposition fails the standard (digest Claims 2–3).

## Step 3 — Taste self-audit

| Check | Verdict | Note |
|---|---|---|
| Is the opportunity a Bridge? | PASS (not a bridge) | The claim is not "attribution research meets multi-backbone evaluation"; it is that attribution labels assert an invariance their pipeline never had (Step 0). The contradiction (seed label [矛盾]) is internal to the attribution enterprise itself. |
| Is the method mere Synthesis? | PASS | The design is not "AgenTracer's injectors + Who&When's judges combined". The load-bearing methodological objects are new *measurement obligations*: the failure-overlap (censoring) rate as a first-class quantity (C3/M5), and the judge×agent factorial that converts a confound into an estimated variance share (C1/M6). Injectors and judge protocols are reused as instruments, credited as such. |
| Load-bearing verbs | PASS after audit | Verbs used in claims: *measure, hold fixed, decompose, isolate, gate, report-beside*. No integrate/unify/leverage in any claim sentence. One occurrence of "unifies" existed only in describing AgenTracer's own method (citation summary) — permitted. |
| Abstract-opening rule | ENFORCED | Abstract v0 (below) opens with the mechanism/asymmetry ("Fault injection fixes the cause… nothing fixes the evidence"), not with "LLM agents are increasingly used… however… we introduce". |

No framing fix required; the digest's skeleton already centers the asymmetry.

## Step 5 — Formal Problem Definition

**Notation.**
- Task set $T$; fault layers $L = \{\text{plan}, \text{tool}, \text{exec}\}$; injectors $\iota_\ell$ per layer (M1). A **cell** is $c = (t, \ell) \in T \times L$ with injection record $r_c = \{task\_id, layer, step\_idx, payload\}$; ground-truth layer $\ell^*(c) = \ell$.
- Backbone set $B$ ($|B|=K$); seeds $s$. Running cell $c$ under backbone $b$ (fixed scaffold, M2) yields trace $\tau(c,b,s)$ and failure flag $F(c,b,s) \in \{0,1\}$ from the task's programmatic checker.
- Judge set $J$; attribution procedure $A_j: \tau \mapsto L$ under frozen prompt + codebook (M3). Normalizer $\nu$ (M4); $A_j(\nu(\tau))$ is the normalized-arm label.
- **Failing intersection** $\mathcal{I} = \{c : \forall b \in B,\ F(c,b)=1\}$ (at T=0, seed 0).

**Adjective/verb → definition → measurement** (every load-bearing term from the digest Claims):

| Term (claim source) | Formal definition | Measured by |
|---|---|---|
| **stable** (Claim 4) | Fleiss' κ over $\{A_j(\tau(c,b))\}_{b \in B}$, $c \in \mathcal{I}$, satisfies κ ≥ 0.8 (95% task-cluster-bootstrap CI entirely ≥ 0.8) | M5; 10,000 task-level resamples |
| **model-specific** (Claim 4, seed) | κ < 0.6 with CI entirely < 0.6; 0.6 ≤ κ < 0.8 (or CI straddling) = "partially stable" | M5 |
| **agreement** (RQ1) | pairwise: $\frac{1}{|\mathcal{I}|}\sum_{c \in \mathcal{I}} \mathbb{1}[A_j(\tau(c,b_1)) = A_j(\tau(c,b_2))]$; K-way: Fleiss' κ on $\mathcal{I}$, Krippendorff's α on all failing (possibly partial) cells | M5 |
| **censored / overlap** (Claim 3) | failure-overlap rate $\Omega = |\mathcal{I}| / |T \times L|$; per-backbone recovery rate $1 - \Pr_c[F(c,b)=1]$ | M5, first-class reported quantity |
| **accurate** (RQ_INF_1) | $\text{Acc}(b) = \Pr_{c \in \mathcal{I}}[A_j(\tau(c,b)) = \ell^*(c)]$ | M5 vs M1 record |
| **agree-wrong mass** (RQ_INF_1) | $\Pr_{c \in \mathcal{I}}[\text{all } b \text{ agree} \wedge \text{label} \neq \ell^*(c)]$ | joint distribution table |
| **separable / apportioned** (Claim 2) | variance shares from cross-classified mixed model: match $\sim (1|\text{task}) + (1|\text{agent\_bb}) + (1|\text{judge\_bb}) + \text{interactions}$; share = component variance / total random-effect variance | M6, LRT + bootstrap CIs |
| **surface-style-driven** (C5) | style-share $= \frac{D_{\text{raw}} - D_{\text{norm}}}{D_{\text{raw}}}$, where $D$ = mean pairwise cross-backbone disagreement, raw vs $\nu$-normalized traces | M4 ablation |
| **valid judge** (M3) | Cohen's κ(judge, adjudicated-human) ≥ 0.7 on the 200-trace human-codebook subset | M3(b) gate |
| **informative either way** (Claim 4) | the pre-registered κ bands above partition all outcomes; each band maps to a distinct publishable claim (H1 / F-1 / F-G1 below) | this document |

Deleted adjectives (no computable referent, removed from all claims): "highly" (model-specific), "materially" (different claim) — replaced by the κ bands and by CO4's re-scoping rule respectively.

## Assumptions (A1–A7)

| id | Assumption | How it could fail | Detection / gate |
|---|---|---|---|
| A1 | Each injector produces a fault whose ground-truth layer is well-defined and single-layered by construction (M1 record is the truth). | Injected fault genuinely spans layers (C4); record ambiguous. | Skeleton: manual audit of all 36 skeleton injections; Stage-1 gate: human–human codebook κ ≥ 0.7 on injected-trace subset. |
| A2 | Injected faults are lethal enough that the failing intersection is large: $\Omega \geq 0.6$ in Stage 2. | Strong backbones absorb faults (C3); $\mathcal{I}$ too small to power κ. | Pilot measures per-fault lethality; iterate payloads toward irrecoverable-by-design faults. Hard gate: pilot $\Omega \geq 0.5$ before Stage 2; else α-on-partial-cells becomes primary (pre-committed). |
| A3 | One scaffold runs byte-identically across all backbones (tool-calling API compatibility, T=0 support). | A backbone lacks function-calling parity; silent prompt truncation. | Skeleton clean-run: all backbones complete ≥ 90% of no-injection tasks without harness errors. |
| A4 | The frozen LLM judge is a valid instrument for the codebook. | Judge noise / preference-leakage-style relatedness bias (t2). | Gate: judge-vs-human κ ≥ 0.7 on 200-trace subset; vendor-disjoint judges in M6; fail → human-coded subset becomes primary data (pre-committed, smaller N). |
| A5 | At T=0, within-backbone label variation is small, so cross-backbone disagreement is attributable to the backbone, not sampling noise. | Provider-side nondeterminism; judge nondeterminism. | B0 test–retest arm (below): within-backbone label agreement ≥ 0.9; else all analyses model the noise floor explicitly. |
| A6 | All backbones can solve the base tasks fault-free (prompt-fit, t6); failures in injected runs are caused by the injection. | Scaffold suits some backbones better; baseline failures contaminate cells. | Headline analysis restricted to tasks with clean-run success under all backbones; clean-run success reported per backbone as a fit covariate. |
| A7 | Base benchmarks (GAIA L1–2, WebArena-style tasks) are locally runnable with deterministic success checkers. | Environment drift; flaky checkers. | Skeleton: checker determinism verified by double-running; flaky tasks excluded before any injection. |

## Instrument validation (guidance.md R2) — the M3 attribution codebook

*(Added at Phase A re-run: A1/A4 already state the acceptance threshold — κ ≥ 0.7 — but guidance.md Part 6 item 6 requires the full 5-step R2 sequence with an acceptance threshold, not the threshold alone. Steps ① and ③ already existed implicitly; ②④⑤ did not and are added here.)*

1. **Ground categories in cited external sources**: the plan/tool/execution boundary and its earliest-causally-decisive-layer tie-break are not invented for this study — they are inherited from Who&When's decisive-error definition (agent–step pairs whose correction flips the outcome) and MAST's plan/tool/execution-adjacent taxonomy (concede-and-differentiate per stage_review.md Stage 3), both externally published and independently reviewed.
2. **Draft wide, refine on a held-out calibration set with named operations**: the walking skeleton's 36 injection records (Step 9) are the held-out calibration set. During the skeleton, any injection that two human coders cannot agree is single-layer (A1) triggers one of two named operations on the codebook before Stage 1 scale-up: **split** the ambiguous layer definition (add a sub-rule distinguishing the two readings) or **merge** it into the adjacent layer under the tie-break rule — whichever keeps the tie-break rule shortest. The specific split/merge applied (if any) is logged in `B_pilot/`.
3. **Validate against ≥2 independent human raters, κ ≥ 0.7 required**: A1's Stage-1 gate and A4's 200-trace subset gate (two human annotators, Cohen's κ ≥ 0.7 before adjudication) — already specified above.
4. **Inspect the confusion structure**: on the same 200-trace human-codebook subset, report the full 3×3 (plan/tool/execution) human-vs-judge confusion matrix, not just the scalar κ. Acceptance requires off-diagonal mass to concentrate in *adjacent* category pairs consistent with genuinely layer-spanning failures (e.g., plan↔tool cascades) — a systematic collapse onto one category (e.g., >50% of all disagreements labeled "execution" regardless of true layer) fails validation and blocks scale-up, routing to situation 7 (guidance.md Part 4): simplify the codebook or accept the property is ill-defined.
5. **Freeze before scale**: once the skeleton's pass criterion (Step 9) is met and the confusion-matrix check in ④ passes, the codebook text and tie-break rule are hashed and frozen; Stage 1 and Stage 2 run against the frozen hash only. Any post-hoc codebook edit after freezing invalidates the run (same discipline as A2's threshold-hashing).

## Aggregation rule (guidance.md §3.1 "aggregation" slot — applies to H1, H1b, H2, H3a, H3b, H4a, H4b)

*(Added at Phase A re-run: Part 6 item 3 requires every H\* to fill all seven template slots including a pre-registered vote rule; Step 6 below stated statement/metric/test/alpha/effect_floor/fallback but never an aggregation rule across the study's two base-task families.)*

The Stage-2 suite draws cells from two base-task families (GAIA-derived and WebArena-derived) plus the Who&When organic-failure complement (Stage 6 dataset table). For every hypothesis in Step 6, the **primary** verdict is computed on the pooled Stage-2 grid (all families combined). As a pre-registered secondary check, the identical band/threshold decision is recomputed independently within each of the two synthetic-fault families (GAIA-only cells; WebArena-only cells). **Aggregation vote rule**: a hypothesis counts as *family-robust* only if the pooled verdict agrees with at least 1 of the 2 family-specific verdicts (≥1 of 2, mirroring the "≥2 of 3 instruments" pattern at this study's smaller family count); if both family-specific verdicts disagree with the pooled verdict, the claim is downgraded from a general statement to a family-conditional one ("stability holds on GAIA-style cells but not WebArena-style cells," or vice versa) rather than reported as the pooled number alone. The Who&When organic-failure complement is never pooled into the primary vote (it answers RQ1's synthetic-vs-organic generalization question on its own, per the Stage 6 dataset justification) but is reported alongside as a third, non-voting data point.

## Power / INCONCLUSIVE pre-declaration (guidance.md Part 6 item 9; situation 5)

*(Added at Phase A re-run: only H1/H1b's power was stated, and only in aggregate; H2/H3a/H3b/H4a/H4b had no stated power, and no cell was pre-declared INCONCLUSIVE if under-powered.)*

- **H1/H1b** (unchanged): >0.9 power to detect κ differences of 0.10 between layers at α = 0.05, computed from pilot-estimated base rates (digest N8).
- **H2** (agree-wrong mass): power computed from the pilot's estimated $|\mathcal{I}|$ and the pre-registered effect floor (≥0.05 mass, CI lower bound >0.02); a (backbone-pair × layer) cell with fewer than 20 jointly-failing tasks is pre-declared **INCONCLUSIVE** for that cell's contribution to the mass estimate, never treated as evidence of a zero effect.
- **H3a/H3b** (judge/style variance shares): power depends on the number of judge×agent×trace observations feeding the mixed-effects model; any (judge_backbone × agent_backbone) cell with fewer than 15 failing traces is pre-declared INCONCLUSIVE and excluded from the variance-share point estimate (but retained in the denominator reported for transparency), never silently dropped.
- **H4a/H4b** (family/capability structure): *(Rule restated 2026-07-04 per design_review.md F1 — the previous per-family formulation, "a family with fewer than 3 same-family backbones is INCONCLUSIVE," contradicted the pre-registered 2-per-family grid and would have emptied H4a by construction. Resolution chosen: reword at the **pair level** so H4a is answerable under the existing grid — no grid extension, no added cost.)* H4a's permutation test operates on backbone **pairs pooled across families**, not on per-family estimates: the within-family arm requires ≥3 within-family pairs *in total* (satisfied by 3–4 families × 1 within-family pair each under the 2-per-family grid) and the cross-family arm requires ≥6 pairs. If either pooled arm falls below its minimum, H4a as a whole is pre-declared **INCONCLUSIVE** (reported descriptively per pair, never as evidence of "unstructured"). Per-family within-family agreement is reported as descriptive rows only; no per-family inferential claim is made at n=1 pair per family.
- **General rule** (situation 5): an INCONCLUSIVE cell is never counted toward a "null" or "stable" verdict, never dropped from the reported n, and always listed in the results table with its cell count so a reader can audit which comparisons were adequately powered.

## Step 6 — Pre-Registered Experiments

Judge for all headline numbers: the pre-registered primary judge (frozen prompt, T=0), validated per A4. All CIs: 10,000 task-level cluster bootstrap resamples. Multiple comparisons within each H-family: Holm correction, α = 0.05.

### E1 (RQ1) — Does the label survive the swap?
- **Assumption**: A1, A2, A3, A5, A6.
- **Hypothesis H1**: Fleiss' κ across K ≥ 6 backbones on $\mathcal{I}$ has a 95% CI entirely below 0.8 (attribution is *not* fully stable). **H1b** (layer structure): κ_exec − κ_plan ≥ 0.10 with Holm-corrected p < 0.05.
- **Metric**: Fleiss' κ on $\mathcal{I}$; Krippendorff's α on all failing cells; pairwise agreement per backbone pair; all per layer. $\Omega$ reported beside every number (Claim 3).
- **Verification**: Stage-2 grid (≈900 cells × 6–8 backbones × 3 seeds; >0.9 power for κ differences of 0.1 at α=0.05 under pilot base rates, per digest N8). Band decision: κ ≥ 0.8 stable / < 0.6 model-specific / else partial.
- **Fallback F-1** (if CI entirely ≥ 0.8): claim as pre-worded — *"On controlled single-layer faults, plan/tool/execution attribution is backbone-invariant (κ = \_\_, CI \_\_): the diagnosis is a task property, and single-backbone attribution benchmarks measure something transferable — a certification prior work assumed but never ran."* (Feeds F-G1.) If CI straddles: report "partially stable" band with per-layer decomposition as the primary result; the claim becomes the layer-ordering finding H1b.
- **Fallback F-1b** *(added 2026-07-04 per design_review.md F5a — H1b previously had no verbatim fallback of its own)*: if H1 passes but H1b fails with no ordering (|κ_exec − κ_plan| < 0.10 or Holm p ≥ 0.05): *"Attribution instability is layer-uniform: execution-layer faults are no easier to diagnose consistently than plan-layer faults (κ_exec − κ_plan = \_\_, CI \_\_), so the 'mechanical legibility' account of attribution difficulty fails, and CO4's re-scoping guidance cannot be relaxed for any layer."* If the ordering **reverses** (κ_plan − κ_exec ≥ 0.10, Holm p < 0.05), report at full prominence per guidance.md situation 4: *"Contrary to the mechanical-legibility prediction, plan-layer attributions are the ones that survive the swap while execution-layer attributions are backbone-specific (κ_plan − κ_exec = \_\_): consistency tracks interpretive layers, not mechanically legible ones — inverting which attribution claims need per-backbone re-validation."*

### E2 (RQ_INF_1) — Stable but wrong?
- **Assumption**: A1, A4.
- **Hypothesis H2**: agree-wrong mass ≥ 0.05 of $\mathcal{I}$, with 95% CI lower bound > 0.02 (consistency ≠ correctness; digest N9 refutation threshold).
- **Metric**: joint distribution over $\mathcal{I}$: {agree-correct, agree-wrong, disagree}, per layer; Acc(b) per backbone vs M1 record.
- **Verification**: exact binomial-style bootstrap CI on the agree-wrong proportion, clustered by task; per-layer breakdown Holm-corrected.
- **Fallback F-2** (if mass < 0.05): *"Whenever backbones agree, they agree with the injected ground truth (agree-wrong < 5%): cross-backbone consensus is a cheap correctness certificate for attribution labels, and majority-vote-across-backbones is a valid pseudo-oracle."* (Upgrades the majority-vote baseline to a contribution.)

### E3 (RQ_INF_2) — Who moves the label: agent, judge, or style?
- **Assumption**: A4, A5.
- **Hypothesis H3a**: judge-backbone variance share > 0.20 of total random-effect variance, LRT p < 0.05. **H3b**: style-share ≥ 0.10 (normalization removes ≥10% of raw cross-backbone disagreement), CI lower bound > 0.
- **Metric**: variance shares from the M6 cross-classified mixed model (3 vendor-disjoint judges × K agents over identical traces); style-share per Step 5.
- **Verification**: model fitted on Stage-2 factorial (~90k judge calls, raw + normalized arms); bootstrap CIs on shares; human-codebook subset (200 traces) anchors judge validity.
- **Fallback F-3** (if both fail): *"Judges are interchangeable and style-blind in this regime (judge share ≈ 0, style-share ≈ 0): the instability measured in E1 is genuinely agent-behavioral — the same fault manifests differently, and no better judge will fix it."* (This *strengthens* E1's interpretation; pre-committed as the alternative mechanism claim.)
- **Mixed outcomes (pre-committed, added 2026-07-04 per design_review.md F5b)**: if H3a passes and H3b fails: *"Instability is judge-driven but not a surface-form artifact (judge share = \_\_, style-share ≈ 0): vendor-disjoint judges disagree about the substance of the same trace, so the codebook — not trace formatting — is where attribution pipelines leak backbone dependence."* If H3a fails and H3b passes: *"Judges are interchangeable but uniformly style-sensitive (judge share ≈ 0, style-share = \_\_): style normalization is a necessary preprocessing step for any attribution pipeline, even one that never swaps its judge."*

### E4 (RQ_INF_3) — Family structure and capability-skewed censoring.
- **Assumption**: A2, A3, A6.
- **Hypothesis H4a**: mean within-family pairwise agreement exceeds cross-family by ≥ 0.10 absolute, Holm p < 0.05. **H4b**: backbone fault-recovery rate correlates with clean-run capability, Spearman ρ ≥ 0.5, p < 0.05 (censoring is capability-skewed).
- **Metric**: pairwise agreement split within/cross-family; per-backbone recovery rate vs clean-run success rate.
- **Verification**: Stage-2 grid crossing family × capability tier (two sizes per family where available); permutation test on the family split respecting task clustering.
- **Confound (R3), named** *(added 2026-07-04 per design_review.md F2)*: under the 2-sizes-per-family grid, every within-family pair is by construction a **cross-tier** pair, so a naive within-vs-cross-family contrast confounds family with tier composition. **Constraint that removes it**: H4a's family contrast is restricted to *cross-tier pairs on both sides* — (within-family, cross-tier) pairs vs (cross-family, cross-tier) pairs — which removes the tier-composition confound; the tier effect is estimated by the orthogonal contrast (cross-family, same-tier) vs (cross-family, cross-tier) pairs and reported beside H4a. Both contrasts use the same task-clustered permutation scheme; pair counts per arm are reported in the results table per the INCONCLUSIVE rule above.
- **Fallback F-4** (if unstructured): *"Attribution instability is idiosyncratic rather than family- or capability-structured: knowing a backbone's vendor or tier does not predict whether its diagnosis will transfer, so per-backbone re-validation cannot be amortized across a family."* (Sharpens CO4's re-scoping guidance.)
- **Mixed outcomes (pre-committed, added 2026-07-04 per design_review.md F5b)**: if H4a passes and H4b fails: *"Agreement is family-structured but censoring is not capability-skewed (within−cross gap = \_\_; ρ = \_\_): re-validation can be amortized within a vendor family, and the failing intersection is not systematically biased toward weak backbones."* If H4a fails and H4b passes: *"Agreement is family-blind but the analyzable failure set is capability-skewed (ρ = \_\_): family membership buys no transfer, and every reported agreement number over-represents the faults that strong backbones cannot absorb — the censoring caveat, not the family caveat, is the one practitioners must carry."* An INCONCLUSIVE H4a (pair-count minimum unmet) is never spliced into F-4's "unstructured" wording — it is reported as INCONCLUSIVE per the Power section's general rule.

### Mandatory baselines

- **B0 — "why do this at all" control: same-backbone test–retest.** Re-run every pilot cell under the *identical* backbone (T=0 re-execution + 3 seeds at T=0.7) and re-judge; also compute the chance floor via label-marginal-preserving permutation (digest baselines). **Justification logic**: cross-backbone disagreement is only a phenomenon if it exceeds the within-backbone noise floor and the chance floor. Pre-registered gate: cross-backbone disagreement > within-backbone disagreement + 0.05 absolute; else the topic's premise fails and F-G1 does not even apply (the honest claim is "attribution labels are noisy, full stop" — pre-committed wording under B0-fail).
- **B-alt — strongest-alternative-explanation control.** **Rival explanation**: "the labels differ not because backbones fail differently, but because the *judge* reads backbone-flavored surface style differently" (C1 + C5; the Preference-Leakage/BiasScope worry). **Budget-matched arm**: identical judging budget spent on (i) M4 style-normalized + neutrally-paraphrased traces and (ii) the vendor-disjoint judge swap (M6), plus the human-codebook subset as the style-immune anchor. If disagreement on normalized traces judged by humans collapses to the B0 floor, the rival explanation wins — and that outcome is exactly fallback F-3's mirror: *"cross-backbone attribution instability is a judging artifact, not an agent property; style normalization is a necessary preprocessing step for any attribution pipeline."*

### Global fallback F-G1

If the central hypothesis family (H1, H3, H4) fails jointly — agreement uniformly high, unstructured, judge-independent — the archetype pivots from *measurement-of-instability* to *certification-protocol* (empirical → conceptual_framework/benchmark lean). Pivoted abstract sentence, pre-committed: *"We pre-registered and ran the first cross-backbone invariance certification for LLM-agent failure attribution and found the diagnosis survives the model swap (κ = \_\_ across N families); we release the fault-injection certification suite so any future attribution benchmark can earn the same stamp."*

### Extreme-censoring fallback F-C0 (Ω → 0; added 2026-07-04 per design_review.md F5c)

Previously uncovered outcome: pilot payload iteration fails to secure overlap — Stage-2 $\Omega < 0.2$ **and** mean pairwise failure overlap < 0.2, so neither Fleiss' κ on $\mathcal{I}$ nor Krippendorff's α on partial cells is estimable at pre-registered power. Pre-committed pivot: the censoring structure itself becomes the headline finding, routed through Claim 3 and H4b. Verbatim: *"Cross-backbone attribution stability is not merely unmeasured but unmeasurable at fault-injection granularity: backbones do not even fail on the same injected faults (Ω = \_\_; mean pairwise overlap = \_\_), so every single-backbone attribution benchmark samples a backbone-specific failure distribution before any judge is consulted. The feasibility bound — which faults transfer at all, and how recovery skews with capability (ρ = \_\_) — is the deliverable, and CO4's re-scoping guidance applies a fortiori: there is no shared failure set on which a backbone-general diagnosis could even be defined."* Under F-C0, H1/H1b/H2/H3 are reported INCONCLUSIVE (not null), H4b is promoted to the primary hypothesis, and the archetype stays `empirical` (a measured feasibility bound, not a certification).

### Fallback-combination rules (guidance.md §3.1; added 2026-07-04 per design_review.md F5b)

Pre-committed at specification time — never invented at verdict time:
1. **B0-fail dominates everything**: if the B0 premise gate fails, no F-\* or F-G1 is used; the only licensed claim is the pre-committed "attribution labels are noisy, full stop" wording (Mandatory baselines).
2. **F-C0 pre-empts E1–E3 fallbacks**: if the Ω → 0 condition fires, F-1/F-1b/F-2/F-3 wordings are not spliced (their hypotheses are INCONCLUSIVE, not failed); F-C0 + H4b carry the paper.
3. **F-G1 fires only on joint failure**: H1 fails (F-1 direction) **and** H3a+H3b both fail (F-3) **and** H4a+H4b both fail or are INCONCLUSIVE (F-4). Any single-H fallback outside this conjunction is spliced locally per its own pre-committed sentence; mixed H3/H4 outcomes use their mixed wordings above and do **not** count toward F-G1's conjunction.
4. **B-alt-wins composes with F-1, not F-G1**: if the rival explanation wins (disagreement collapses to the B0 floor on human-judged normalized traces), the judging-artifact wording (B-alt block) replaces the E1 mechanism gloss but the certification claim F-1/F-G1 is *not* triggered by it — an artifact-driven high κ is not an invariance certificate.

## Step 9 — Walking Skeleton

**One binary question**: *does an injected fault produce a judgeable, overlapping failure under two different-family backbones, end to end, with the ground-truth record intact?*

- **Arms (2)**: backbone-1 = one closed-weight family model; backbone-2 = one open-weight family model (frozen checkpoint). Primary frozen judge, T=0, **plus** *(amended 2026-07-04 per design_review.md F3 — the skeleton previously exercised neither M4 nor M6, making the "config-not-code" claim false)* one vendor-disjoint secondary judge over the same failing traces (the minimal M6 factorial path, deterministic label counts only — no mixed-model fitting yet), and one pass of the deterministic M4 normalizer ν with the primary judge re-run on normalized traces (the M4 code path; the paraphrase arm stays Stage-2-only and is the one declared exception to config-only scale-up).
- **Task set**: 12 base tasks (8 GAIA L1, 4 WebArena-style tool tasks), each verified deterministic (A7) and clean-run-solvable by both backbones (A3/A6) → 12 × 3 injectors = 36 cells, 72 agent runs.
- **Deterministic metrics only**: harness completion rate, checker determinism (double-run), per-cell failure flags, failure-overlap count, judge label parse rate, raw pairwise agreement count, accuracy-vs-record count. No κ, no CIs, no mixed models.
- **Expected cost**: 72 agent runs (~10–40 steps) + ≤ 216 judge calls (primary raw + primary normalized + secondary raw, ≤ 72 each); < $25 API, ≤ 1 day wall-clock including the manual audit of all 36 injection records (A1).
- **Pass criterion (explicit)**: (i) 100% harness completion, 0 checker flakes; (ii) failure-overlap ≥ 50% of cells (18/36); (iii) judge returns a parseable layer label for 100% of failing traces; (iv) manual audit confirms ≥ 33/36 injection records are unambiguous single-layer faults; (v) *(added 2026-07-04)* the secondary-judge and normalized-arm passes each return a parseable label for 100% of failing traces, and ν is verified idempotent (ν(ν(τ)) = ν(τ)) on all skeleton traces — i.e., every Stage-2 code path (M4 normalizer, multi-judge fan-out) already runs end to end. **Skeleton passed ⇒ pilot (Stage 1: 60 tasks × 3 injectors × 4 backbones) and Stage 2 are config changes (more tasks, more backbones, more judges, plus the pre-declared paraphrase-arm exception), not code changes.** Any failed criterion maps to its assumption gate (A7/A3, A2, A4, A1, A4/M4 respectively) and blocks scaling.

## Claim–Evidence Map

| # | Abstract-level claim (from digest Claims) | Traces to | Status |
|---|---|---|---|
| 1 | Cross-backbone generalizability of failure attribution is an untested assumption in the attribution line (Who&When, AgenTracer, MAST) and untouched by the judge-reliability line. | digest N3/N4; Step 0 asymmetry | supported-by-design (literature-grounded; **grounding currently weak** — see harvest caveat below) |
| 2 | Instability has two separable sources (agent vs judge) and only a factorial + normalization can apportion them. | H3a/H3b; M4/M6 definition (Step 5 "separable", "style-share") | needs-experiment (E3); fallback-covered (F-3, both directions publishable) |
| 3 | Censoring is first-order: agreement numbers are uninterpretable without the overlap rate. | Ω definition (Step 5); A2 gate; H4b | needs-experiment (E1/E4 report Ω beside every κ); supported-by-design as a protocol obligation |
| 4 | The measured agreement is informative either way (κ bands partition all outcomes). | H1 + F-1 + F-G1; κ-band definitions | fallback-covered by construction |
| 5 | If model-specific, single-backbone attribution claims must be re-scoped as (task, backbone)-pair properties; the released suite makes re-validation cheap. | H1 (model-specific band) + H4 (F-4 sharpens); CO4 | needs-experiment (conditional claim); fallback-covered (F-4) |
| — | Stable-but-wrong consensus exists (or consensus certifies correctness). | H2 / F-2 | needs-experiment (E2); fallback-covered |

Every claim traces to an H-id or a Step-5 definition; no claim depends on an undefined adjective.

**Harvest caveat on Claim 1 (non-pre-emption; added 2026-07-04 per design_review.md F4)**: Claim 1's "untested assumption" status rests on (a) the 2025-snapshot OpenReview corpus (`topics/corpus/ideas.jsonl`) and (b) a 150-candidate arXiv harvest of which 147 hits proved off-topic — i.e., the harvest angles never targeted this topic, so absence-of-a-twin has only been checked against a weak search. Claim 1 may not be asserted as established in any Phase E prose until the pre-registered re-harvest (guidance.md Part 5 / situation 6 discipline) runs on these named angles and returns no method-twin: **"cross-backbone failure attribution stability"**, **"LLM judge agreement on agent trajectories/traces"**, **"fault injection agent evaluation across models"**, **"plan tool execution error taxonomy cross-model"**, **"backbone swap agent diagnosis reproducibility"**. A twin found → repositioning + Phase A re-check, never a silent related-work patch.

## Abstract v0 (draft, mechanism-first — DRAFT BEFORE RESULTS; blanks are pre-registered slots)

> Fault injection fixes the *cause* of an LLM-agent failure across backbones; nothing fixes its *evidence*. Plan/tool/execution attribution labels are therefore reported as task properties while being computed from backbone-dependent traces, often by backbone-dependent judges. We isolate this gap: an identical fault-injection suite (GAIA/WebArena base tasks; single-layer injectors with machine-readable ground truth) is executed under 6–8 backbones spanning family and capability tier, every failing trace is labeled by a fixed pre-registered procedure, and agreement is measured with chance-corrected statistics gated on the failure-overlap rate — the censoring quantity that stronger backbones distort by recovering from faults. A judge×agent factorial with style-normalized traces decomposes label variance into agent, judge, and surface-style shares. Pre-registered bands (κ ≥ 0.8 stable; κ < 0.6 model-specific) make either outcome a finding: diagnosis as task property, or diagnosis as backbone artifact. [κ = \_\_; shares = \_\_.]

(148 words. Opens on the asymmetry; verbs: fix, isolate, execute, label, measure, gate, decompose; no "increasingly used… however… we introduce".)
