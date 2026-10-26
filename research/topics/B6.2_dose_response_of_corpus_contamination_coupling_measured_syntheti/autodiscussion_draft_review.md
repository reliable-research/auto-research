# Review: B6.2 Auto-Generated Draft Package ("Shared Data-Budget Dose Modeling...")

Reviewed: `paper-draft.md`, `experiment-spec.md`, `research-report.md` in
`/data/wangjian/wj_code/paper_autodiscussion/completed_jobs_dirs/ZB6.2 The Privacy-Capability Scissors Dose-Response of Synthetic Contamination with Rarity Displacement--9cf96679/`
against `discussion.md` / `README.md` in this topic dir. Date: 2026-08-15.
Citation sweep: WebSearch quota exhausted; verification done via arXiv API (`export.arxiv.org/api/query`) — a **narrower sweep** than intended; 2025–26 near-twin coverage is best-effort only.

## 1. Architecture of the draft (~10 lines)

- Preregistered, fixed-token-budget training panel: GPT-2-style 124M/355M models trained **from scratch** at dose grid G = {0, 5, 10, 20, 35, 50, 70}% synthetic, paired seeds.
- 20 scenarios = 5 corpora (Wikipedia, arXiv, StackExchange, GitHub, Gutenberg) × 2 model sizes × 2 detector-separability regimes; 40 paired seeds/scenario → **800 trajectories, 5,600 base runs**, plus a matched replacement factorial on top.
- Rarity factor (absorbed B6.4): rare-targeted / common-targeted / proportional replacement masks at matched ρ, with duplication-matched human-resampling controls; feasible-dose set D_R and ρ* = max D_R; effects identified by paired contrasts + difference-in-differences.
- Privacy outcome: calibrated reconstruction probability of **single-exposure rare sentinels**, with a checksum-verifiable latent reconstruction event R and a blinded score-stratified gold-label audit.
- Joint Bayesian dose model: four **disjoint** curve-family supports (flat / linear / convex / change-point) with 0.10-SD separation bands and an `unclassified` outcome when a calibration gate (LODO RMSE ≤ 0.15, 90% PPI coverage ∈ [0.85, 0.95]) fails.
- Forensic module: detector decisions modeled as misclassified observations of latent reconstruction events; uncertainty propagated through curve fits; validated on 2,000/2,400 semi-synthetic replays (RQ5/RQ6) vs a plug-in confusion-matrix baseline.
- Six RQs: endpoint effects at ρ=0.50 (RQ1), calibrated family classification (RQ2), rarity-specific privacy (RQ3) and diversity (RQ4) effects at ρ*, interval calibration (RQ5), family recovery (RQ6).

## 2. Novelty ledger

| # | Claim | Nearest prior | Delta | Stance |
|---|-------|---------------|-------|--------|
| N1 | Within-generation dose-response of synthetic fraction with statistical shape adjudication (flat/linear/convex/change-point) | Shumailov et al. 2305.17493 (generations as dose); Gerstgrasser et al. 2404.01413 (2 discrete regimes); Dohmatob et al. 2402.07712 + Strong Model Collapse 2410.04840 (theory: even tiny fractions harm, no safe threshold); Kazdan et al. 2410.16713 (mixture proportions, recursive) | First empirical LM-scale *controlled within-generation fraction grid* with preregistered family classification | Plausibly novel, but the draft **never cites the Dohmatob line**, whose theory directly predicts the answer ("no safe dose") — must be engaged as the adverse prior |
| N2 | Rarity displacement as a designed factor: contamination raises memorization/privacy risk of *surviving rare human data* | Carlini 2202.07646 (memorization ∝ duplication/scale); Kandpal et al. 2202.06539 & Lee et al. 2107.06499 (dedup↔privacy); Morris et al. 2505.24832 (~3.6 bits/param capacity, rarity-driven memorization) | Treatment = displacement of rarity strata; outcome = memorization of residual human data; duplication controlled by matched resampling | Novel coupling — the paper's best card. But the draft **omits Morris et al.**, the very result that motivated the topic refresh; the "shared data budget" hypothesis floats without its mechanism |
| N3 | Forensic detector uncertainty propagated through dose-response inference | Liang et al. 2403.07183 (corpus-level AI-text prevalence estimation); MIA calibration line (Duan et al. 2402.07841) | Measurement-error model inside the dose fit | Novel-ish, but the draft silently **retargeted** the instrument: discussion.md's M6 propagates error in the *contamination dose estimate* ρ̂ (the policy-relevant case: curators only have detectors); the draft propagates error in *reconstruction-event detection*, a different and less-motivated channel |
| N4 | Disjoint-support Bayesian family classification with `unclassified` | Standard segmented-regression/model-selection (Davies test, AICc) | Packaging: separation bands + calibration gate prevent forced labels | Supporting methodology, not a headline claim; keep |

## 3. Consistency vs discussion.md — silent scope changes

**The rarity-displacement factor from B6.4 IS present** (rare/common/proportional masks, duplication-matched controls, RQ3/RQ4) — the absorption survived and is well-engineered. Everything else drifted, silently:

1. **Training paradigm swapped**: frozen-backbone continued pretraining (Pythia-410M/1.4B, Pile-trained pre-ChatGPT checkpoints — the audit's explicit feasibility envelope) → **from-scratch** GPT-2 124M/355M. Changes the estimand and discards the stated cost rationale.
2. **~100× compute inflation**: discussion.md commits to ≈75 runs ≈ 1.1–1.3k A100-h. The draft requires 5,600 base runs *plus* the replacement factorial (3 policies + resampling arm × 6 positive doses × 800 seed-blocks) — order 20,000+ from-scratch runs, i.e. **hundreds of thousands of A100-hours**. Never acknowledged.
3. **Low-dose region deleted**: grid {0, 0.5, 1, 2, 5, 10, 20, 35, 50, 75, 100}% → {0, 5, ..., 70}%. The seed's headline question ("is 3% tolerable? safety threshold vs monotonic") is *unanswerable* on a grid whose smallest positive dose is 5%; the TOST-equivalence "statistically harmless region" analysis and the ρ=100% collapse-anchoring endpoint are both gone.
4. **Privacy battery downgraded**: per-stratum canaries at duplication {1, 4, 16} + Min-K%++ MIA + natural-document extraction → single-exposure sentinels only. The G2 measurability gate is dropped — exactly the failure mode discussion.md pre-declared (single-exposure extraction at 124M is likely at floor, killing the absorbed axis at analysis time).
5. **Accumulate-vs-replace debate not honestly engaged**: Gerstgrasser et al. is cited descriptively, but the matched **accumulate-regime arm** from discussion.md (M3 controls) is dropped and the design is pure replacement. A reviewer armed with "collapse doesn't happen with accumulation" will ask why only the replace regime is studied; the draft has no answer in-design.
6. **Provenance requirement dropped**: discussion.md requires a pre-2022 (pre-ChatGPT) human pool so ρ is ground truth; the draft's "version-pinned" Wikipedia/StackExchange/GitHub snapshots have no temporal cutoff → the ρ=0 arm is itself contaminated, corrupting the dose axis.
7. **Rarity operationalization coarsened**: rare-token-density deciles × topic-cluster size (a strata *gradient*) → single "lowest-frequency metadata label" per corpus.
8. **Headline mechanism dropped**: the "privacy-capability scissors" prediction, its manipulation-check figure, and the title itself are gone; pilot gates G0–G3 and the venue/schedule logic are gone.

## 4. Citation audit (load-bearing)

Zero confabulated citations (sibling failure signature: confirmed absent). All checked via arXiv API:

| Citation in draft | Status |
|---|---|
| Shumailov et al., Curse of Recursion (2305.17493, Nature 2024) | OK |
| Gerstgrasser et al., Is Model Collapse Inevitable? (2404.01413) | OK |
| Alemohammad et al., Self-Consuming... MAD | OK |
| Carlini et al., Extracting Training Data (USENIX '21) | OK |
| Carlini et al., Quantifying Memorization (2202.07646) | OK |
| Zhang et al., Counterfactual Memorization | OK |
| Lee et al., Deduplicating... Better (2107.06499) | OK (cited without authors) |
| Seddik et al. (2404.05090); Bertrand et al.; Borji; Guo et al.; Chen et al.; Havrilla et al. | OK |
| Mireshghallah et al., "Do MIAs Work on LLMs?" | **Misattributed** — first author is Michael Duan (2402.07841); Mireshghallah is a co-author |
| Liang et al. [2026], Monitoring AI-Modified Content | **Wrong year** — 2403.07183, ICML 2024 |
| **Missing**: Morris et al. 2505.24832 (capacity/rarity — the topic's refresh) | Must add |
| **Missing**: Dohmatob et al. 2402.07712 + Strong Model Collapse 2410.04840 | Must add (adverse theory) |
| **Missing**: Kandpal et al. 2202.06539 (dedup mitigates privacy risk) | Must add (duplication confound counterpoint) |
| **Missing**: Kazdan et al. 2410.16713; Shi et al. Min-K% 2310.16789 | Should add |

## 5. Gap to implementation (compute realism for a small group)

- Base panel: 5,600 from-scratch runs. Even at a Chinchilla-lean ~2.5B tokens for 124M (~10–15 A100-h) and more for 355M, the base panel alone is ≈ 60–100k A100-h; the replacement factorial and resampling arms multiply this several-fold; **>200k A100-h total ≈ 100–300× the discussion.md budget** and out of reach for an academic node (8×A100 would need multiple years wall-clock).
- 40 paired seeds × 20 scenarios also implies 800 MCMC fits of a joint latent-event model plus 4,400 replay fits — weeks of CPU/GPU inference on its own.
- The blinded score-stratified gold-label audit assumes personnel/process a small group does not have; discussion.md's checksum-canary design achieves the same end mechanically.
- Detector-separability bands (AUC 0.65–0.75) may be unrealizable for modern generator/detector pairs → scenario infeasibility cascades.
- Feasible path exists and was already specified: the discussion.md sparse matrix (A)–(E): ~75 CPT runs on Pythia-410M (+10 at 1.4B, + cheap 160M from-scratch regime check) ≈ 1.1–1.3k A100-h ≈ 6–7 days on one 8×A100 node, with gates G0–G3.

## 6. Verdict + top-3 fixes

**Verdict: Major revision — sound statistical skeleton, silently inflated ~100× beyond the audited feasibility envelope, and decapitated on the seed's core question.** Keep: formal estimand, disjoint-family/`unclassified` logic, matched displacement + duplication-matched DiD, feasible-set D_R discipline, preregistration. Fix:

1. **Restore the feasible design**: frozen-backbone CPT sparse matrix (Pythia-410M primary, 1.4B scale arm, pre-2022 Pile provenance, ~75 runs + 160M from-scratch regime check), with pilot gates G0–G3 reinstated; keep the draft's Bayesian machinery on top of it (scaled-down replays).
2. **Restore the low-dose axis and the threshold verdict**: log-spaced grid {0, 0.5, 1, 2, 5, 10, 20, 35, 50, 75, 100}%, unbalanced replication at ρ ≤ 5%, and an equivalence (TOST/ROPE) criterion so "practically flat low-dose region" is a possible *finding*, not a missing cell; keep ρ=100% to anchor the collapse literature.
3. **Restore the absorbed axis's mechanism and realism**: cite and build on Morris et al. 2505.24832 (capacity/rarity) and engage Dohmatob's no-safe-dose theory + Gerstgrasser's accumulate regime (add the matched accumulate arm); reinstate per-stratum canaries at duplication {1, 4, 16} with the G2 measurability gate and Min-K%++ MIA; re-point the forensic module at dose-estimate error ρ̂ (detector→ρ̂ calibration, threshold-shift Δρ*, verdict flips); restore the scissors headline + manipulation check; fix Duan and Liang citations.

## Inferred unresolved majors

- **Privacy floor risk**: even with duplication-16 canaries, 410M CPT may show floor-level exposure — G2 exists precisely for this; the paper must pre-declare the canaries-only fallback.
- **Change-point identifiability**: with ~11 dose points and seed noise, segmented vs convex may be indistinguishable at low effect sizes; the `unclassified` outcome is the honest answer but weakens the headline — power analysis must budget for it.
- **ρ=0 self-contamination**: no pre-2022 source is perfectly synthetic-free post-hoc; residual contamination attenuates the low-dose contrast (bias toward "flat") and must be bounded.
- **Race risk**: absence claim "no within-generation dose sweep exists" rests on a narrowed (arXiv-API-only) sweep; a full G0 novelty sweep is mandatory pre-submission.
