# Review: T3.2 Autodiscussion Draft Package (Why Soft Policies Rot Faster)

Reviewed: 2026-08-13. Inputs: `research-report.md`, `experiment-spec.md`, `paper-draft.md` in
`paper_autodiscussion/completed_jobs_dirs/ZT3.2...--2c804c8e/`, against `discussion.md` + `README.md` in this topic dir.
Context: room closed with 3 unresolved MAJOR critiques (weakest-gate cohort); sibling failure signature checked explicitly
(confabulated citations / silent scope inflation / missed 2026 neighbors).

---

## 1. Architecture of the proposed study (~10 lines)

1. **Predicate-Matched Constraint Bank (PMCB):** same-predicate soft/hard pairs (identical predicate + choice set, differ only in preferred-vs-mandatory wording) carry the headline asymmetry; distinct-predicate pairs carry cue-removal / prior tests. Matched on length (≤2 tokens), specificity, opportunity count, canonical difficulty (5-pt caliper), solo-presentation drift stability.
2. **Five arms per item:** injected / frozen-token null (class cue only: "preference"/"rule") / cue-free (no cue at all) / solo-stability / canonical-difficulty. Core identity `G_raw = G_null + G_lift` splits raw class gap into cue-inclusive class support vs visible-instruction lift.
3. **Cue-free prior-affirmation tower (H4a–H4c):** first-probe equivalence positive control → late-probe joint-arm divergence (solo vs joint decomposition, interaction term I) → category-coherence mixed model (predicate as random effect) → normative-specificity vs decorrelated placebo partition (ρ_dec ≤ 0.30, margin δ_spec). Outcomes include UNTESTABLE / UNSCREENED statuses.
4. **Factorial salience–framing decomposition:** position × repetition (1/2/4) × imperative/descriptive mood; hierarchical logistic trajectories; closed-form 3-player Shapley allocation of ΔG_lift into salience / framing / residual.
5. **Counterfactual compaction replay:** frozen histories re-probed at matched checkpoints under growth / oldest-first truncation / unconstrained summarization / verbatim-preserving summarization / null-token ablation, at equal token budget, constraint-age ladder {1,4,8,12}; deletion test only as a secondary bound vs both null and cue-free baselines.
6. **13 RQs + deterministic attribution ledger** (S1 prior / S2 visible-text / S3 mixed / S4 bounded-partial / S5 cue-dependent-majority / informative-null / uninformative), all scoring by frozen rule-based parsers (judge/human labels only in one-time parser validation).
7. Scale as specced: 240 held-out + 120 calibration pairs × up to 5 arms × 8 probes × 12 sessions × 2 grids × 5 operators — order 10⁵–10⁶ generations, single frozen model snapshot.

## 2. Novelty ledger (top claims verified by 2025–2026 web search)

| # | Claim | Nearest prior | Delta | Stance |
|---|-------|---------------|-------|--------|
| N1 | First **mechanism attribution** (salience vs framing vs alignment prior) of the soft/hard constraint-decay asymmetry on length/specificity-equated pairs | **Governance Decay** (arXiv:2606.22528, Jun 2026): 8.3× soft-vs-hard compaction decay, ConstraintRot, Constraint Pinning — measures + mitigates, does **not** attribute. **Omission/Commission** (arXiv:2604.20911, Apr 2026, Gamage): omission-vs-commission asymmetry + a *partial* mechanism decomposition (schema-semantic vs token-volume dilution, 62–100% semantic) | Factorial framing manipulation, cue-free no-injection prior tests, and class pairs equated for surface form remain unclaimed; but "no one decomposes mechanism at all" is **overclaimed** — 2604.20911 already separates two dilution mechanisms | **SUPPORTED, NARROWED** — must position against 2604.20911's decomposition explicitly |
| N1b | Salience (position/repetition) as decay mechanism | **Lost in Compaction** (arXiv:2608.11242, Aug 2026, PSU): CompInt shows session-constraint retention through compactors is ~17% and *systematically sensitive to SC phrasing and injection location* | 2608.11242 measures **survival of the constraint text through the compactor**; T3.2 measures **behavioral decay with class contrast and no-injection baselines**. Delta real but the "phrasing/position matter under compaction" headline is now published | **PARTIALLY PREEMPTED** on the salience-as-survival axis; draft cites neither this nor 2512.17920 (constraint compliance under compression benchmark) |
| N2 | Separating **growth-only decay from compaction-induced loss** via counterfactual replay of matched histories at equal budget (verbatim-preserving vs unconstrained summarization) | Governance Decay (compaction only, no growth-only arm); Omission/Commission (growth/dilution only, no compaction); 2512.17920 (compression, single-shot) | No found work runs both regimes on identical frozen histories with operator as the only difference | **SUPPORTED** — this is the strongest, cleanest novel contribution |
| N3 | Behavioral, text-independent **alignment-prior** test (cue-free divergence + coherence + specificity screens) | Shallow-alignment line: Qi et al. 2406.05946; SSAH 2410.10862 (ICLR 2026) — weight-level characterization, never behavioral class-support under cue removal; refusal-geometry work (e.g. 2606.22686) is representation-level | Behavioral cue-free bounding is new, but the design itself concedes it cannot point-identify (predicate-identity confound); every affirmation path can exit as UNTESTABLE/UNSCREENED | **NOVEL BUT FRAGILE** — over-engineered relative to the evidential yield it can deliver |

Search queries used: constraint retention context compression; instruction decay/drift long context; system prompt adherence degradation; memory compaction policy violation; salience/framing effects on instruction following; plus direct arXiv-ID verification.

## 3. Consistency vs discussion.md — silent scope changes (the sibling failure signature, confirmed)

1. **All four pilot gates dropped.** discussion.md G0 (8×-source verification + precedent search), G1 (reactivity calibration), G2 (gap-replication pivot rule), G3 (dominance stability) — none appear in spec or paper. No pilot stage at all; spec goes straight to 240 held-out pairs.
2. **Budget silently inflated 10–100×.** discussion.md commits to pilot ~4–4.6k conversations (~60k calls), scale-up ~20k conversations, envelope ≤$3k API + ≤10 A100-days. Spec: "order 10⁵–10⁶ generations", no cost estimate, no envelope, no named cuts.
3. **Probe reactivity (SP3/M6) vanished.** discussion.md: reactivity calibration "gates everything" (probes refresh the constraint's salience — the instrument perturbs the measurand). Zero mention in the 13 RQs.
4. **Multi-model design → single frozen snapshot.** discussion.md: 2 pilot + 3 scale-up models, `(1|model)` random effect, open-weights base/instruct twin. Prior-proxy battery M5 (base-vs-instruct delta, per-token KL) dropped; only the no-injection proxy survives (as the cue-free arm).
5. **Compaction operator set swapped; mitigation arms deleted.** discussion.md's `keep-top` (the audit's KEEP-TOP condition) and `summarize+pin` / every-k restatement mitigation arms are gone — the promise that "the pinning-repair crowd's remedy is evaluated inside the mechanism design" is silently unmet.
6. **Compaction-deletion natural experiment demoted** from pre-registered co-headline contrast (discussion Stage 5, critic (d)) to "secondary bound only."
7. **Survival modeling silently replaced.** Hazard models, half-lives, dominance analysis → logistic trajectories + Shapley. Defensible, but unacknowledged and the "decay half-life" outcome shape promised in discussion.md disappears.
8. **Construct drift on "hard".** discussion.md operationalizes hard = high no-injection compliance (weight-backed). Draft's headline same-predicate pairs define hard = *mandatory wording of the same predicate* — modality-only, so the headline pairs cannot carry the alignment-prior mechanism; the prior lives only in the distinct-predicate side-arm. Listed nowhere as a limitation.
9. Minor: 40-pair bank → 360 pairs; LMSYS-Chat-1M distractor padding → unspecified "neutral padding"; venue/timeline/pre-registration-freeze discipline dropped.

## 4. Citation audit (load-bearing, all checked)

| Citation (as in draft) | Status |
|---|---|
| Laban et al., LLMs Get Lost in Multi-Turn Conversation, arXiv:2505.06120 | CONFIRMED |
| Liu et al., Lost in the Middle, arXiv:2307.03172 | CONFIRMED |
| Li et al., Instruction (In)Stability, arXiv:2402.10962 (COLM 2024) | CONFIRMED |
| Zhou et al., IFEval, arXiv:2311.07911 | CONFIRMED |
| Qin et al., SysBench, arXiv:2408.10943 | CONFIRMED |
| Wu et al., LIFBench, arXiv:2411.07037 | CONFIRMED |
| He et al., Multi-IF, arXiv:2410.15553 | CONFIRMED |
| Luz de Araujo et al., Persistent Personas, arXiv:2512.12775 (EACL 2026) | CONFIRMED |
| Gamage, Omission/Commission Constraints, arXiv:2604.20911 | CONFIRMED (report lists "unknown authors" — fill in) |
| Governance Decay / ConstraintRot, arXiv:2606.22528 | CONFIRMED (authors still unlisted in draft) |
| Qi et al., Safety Alignment...Tokens Deep, arXiv:2406.05946 | CONFIRMED |
| Li & Kim, SSAH, arXiv:2410.10862 (ICLR 2026) | CONFIRMED |
| Wallace et al., Instruction Hierarchy, arXiv:2404.13208 | CONFIRMED |
| Leviathan et al., Prompt Repetition, arXiv:2512.14982 | CONFIRMED |
| Packer et al., MemGPT 2310.08560; Zhou et al. LIMA 2305.11206; Yin et al. politeness (SICon 2024) | CONFIRMED |

**Zero confabulated citations** — matches the sibling signature. But: (a) discussion.md's own anchor set (PrefEval, SinkTrack, TimeToInconsistency, OffTopicEval, SafeDialBench, ICFBench, TARE, RECAST) was silently swapped for a different corpus; (b) **missed 2026 nearest neighbors**: Lost in Compaction (2608.11242), Separating Constraint Compliance from Semantic Accuracy under Compression (2512.17920), Prospective Memory Failures in LLMs (2603.23530), Reasoning Up the Instruction Ladder (2511.04694).

## 5. Gap to implementation

- **No code exists.** Spec demands ~20 modules: bank builder with caliper-ladder/fallback/calibration-guard logic, 5 prompt-arm constructors, 5 compaction operators with verbatim-survival audit, GLMM + TOST + closed-form Shapley, 13 RQ modules, deterministic ledger, MockClient. Realistic build: 4–8 engineer-weeks before any API call.
- **Operator must supply everything load-bearing:** predicate schemas, constraint corpus, deterministic scorers, blinded parser-validation labels (2,400 outputs), summarizer, tokenizer, model snapshot. The "harness" is scaffolding around unauthored science.
- **Compute unpriced:** 10⁵–10⁶ generations at long-context lengths is $10⁴–10⁵ API-class — vs the discussion's ≤$3k envelope. No smoke run, so the first signal on whether soft cue-free compliance even stays above floor arrives after the full spend.
- **Riskiest logic:** the freeze/fallback machinery (δ re-derivation, guard, transfer license) — most branches are untested statistical policy; a MockClient with synthetic compliance processes is specced but not built.

## 6. Verdict and top-3 fixes

**Verdict: MAJOR REVISION (design core is sound and worth keeping; package as shipped is unrunnable and mispositioned).**
The matched-pair + `G_raw = G_null + G_lift` decomposition and the counterfactual compaction replay (N2) are genuinely novel and clean. But the package exhibits the full cohort failure signature minus confabulation: silent 10–100× scope inflation, all pilot gates and the reactivity control dropped, mitigation arms deleted, and the Aug-2026 nearest neighbor missed. The H4 prior tower is baroque relative to its evidential yield.

**Fix 1 — Restore staging and honesty about scale.** Reinstate discussion.md's pilot (≈40 pairs, 2 models, growth + keep-top) with gates G0–G3 including the probe-reactivity calibration as the first gate; publish the cost envelope and named cuts; scale 240-pair full factorial down to the confirmatory subset the budget supports.
**Fix 2 — Re-anchor the alignment-prior construct.** Make hard-class membership operational (no-injection compliance) not lexical; restore base-vs-instruct triangulation on one open-weights pair; collapse H4a–c to a preregistered three-screen appendix and promote the **compaction-deletion natural experiment** back to co-headline (soft craters to no-injection floor, hard barely moves — the cleanest prior signature).
**Fix 3 — Reposition against 2026 neighbors and restore mitigation arms.** Cite and differentiate 2604.20911 (partial mechanism decomposition already exists), 2606.22528, 2608.11242, 2512.17920; restore keep-top and summarize+pin/every-k-restatement as mitigation arms so the mechanism result re-prices the pinning-repair fixes as promised.

## Inferred identity of the 3 unresolved MAJOR critiques

1. **Prior-mechanism identifiability (construct validity).** The alignment prior can never be manipulated, the headline same-predicate pairs are wording-only (cannot carry the prior), and the cue-free tower admits it cannot remove the predicate-identity confound — so the promised "mechanism attribution" can, for its most important mechanism, only ever return bounded/unscreened/untestable statuses. The critic likely demanded either a manipulable prior proxy (base-vs-instruct) or a weaker claim.
2. **Feasibility / silent scope inflation.** 10⁵–10⁶ generations, 13 RQs, ~20 modules, no pilot, no gates, no budget — vs a 6-week window and ≤$3k envelope in the design doc. The critic likely demanded a staged plan with kill criteria; it was never added.
3. **Measurement validity of the soft class + probe reactivity.** Mechanical-parser-only scoring restricts "soft policies" to format-like finite-choice predicates — the tone/business-rule constructs motivating the paper are exactly what deterministic parsers cannot score — and probing itself refreshes constraint salience with no reactivity bound anywhere in the design. The critic likely flagged that the headline construct ("soft organizational policy") and the measured construct (soft-worded finite-choice predicate) have quietly diverged.
