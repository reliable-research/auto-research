# C4 Draft Review — "Attestation or Illusion: Detection-vs-Spoofing Economics of LLM Serving Substitution"

**Reviewed:** 2026-08-15. **Inputs:** `paper_autodiscussion/completed_jobs_dirs/ZC4 ...--c7c69990/` (research-report.md, experiment-spec.md, paper-draft.md) vs `positions/C4_behavioral_attestation/discussion.md`.
**Citation sweep:** WebSearch unavailable was anticipated; verification done via arXiv API (`export.arxiv.org/api/query`) — narrower sweep than a full literature search, noted in §4.

---

## 1. Architecture of the proposed work (~10 lines)

The draft proposes a three-module measurement framework. (1) A **blinded, episode-randomized
replay bench**: auditor-controlled endpoints serve known checkpoint pairs (expected c⁰ vs
substituted/downgraded c¹) behind one shared serving stack, with sealed labels crossed against
nuisance profiles (temperature, batching, quantization, load) calibrated from "candidate-stable"
windows of real commercial APIs via change-point tests. (2) A **constrained empirical
double-oracle game**: a sequential likelihood-ratio auditor with information-gain query selection
alternates held-out best responses against a detector-aware adversary grammar (PEFT of the
downgrade checkpoint, decoding calibration, best-of-k reranking, rewriting, selective escalation
to the true model). (3) A **shared metered resource ledger** (queries, tokens, accelerator-seconds,
energy, latency-constrained capacity, person-hours) that converts the game into detection–spoofing
budget curves and a **savings-erosion ratio** E = (C_M − C_D)/(C_T − C_D), testing whether hiding a
downgrade consumes the savings that motivated it. Six RQs: harness-artifact validity, label
leakage, frontier convergence, adaptivity value, ledger accuracy, economic break-even.

## 2. Novelty ledger

| # | Claim in draft | Nearest prior (verified) | Delta | Stance |
|---|---|---|---|---|
| N1 | Two-sided detection-vs-spoofing **budget frontier** (auditor budget × adversary budget × sophistication) | 2606.16100 (GhostPrint: spoofing exists, fixed operating points); 2504.04715 (detection unreliable → TEE) | They give existence proofs / single points; frontier over joint budgets is unclaimed | **Holds** — this is C4's mandated delta and it survives |
| N2 | **Savings-erosion economics**: does mimicry cost consume downgrade savings (E ⋛ 1)? | 2606.16100 reports "low fine-tuning cost" qualitatively; no prior charges provider-side capacity/latency/energy | Genuinely unclaimed; the strongest new element the draft adds over discussion.md | **Holds** |
| N3 | Ground-truth-by-construction bench with **calibrated serving noise** | 2410.20247 (MET) uses real APIs w/o ground truth; 2504.04715 controlled pairs w/o calibrated-noise crossing | Crossing sealed identity × calibrated nuisance is new as an evaluation design | **Holds, but oversold** as "blinded/preregistered" apparatus (§5) |
| N4 | Sequential information-gain auditing beats fixed-query fingerprints | 2506.06975 (RUT), 2607.10252 (one-token), 2512.03816 (logprob tracking), IRIS 2607.20860, KBF 2605.29524 | Adaptivity-vs-fixed at matched ledger cost not measured before, but this is a detector contribution — exactly the "another detector paper" drift discussion.md warned against | **Weakened** — keep as instrument, not headline |
| N5 | Artifact/leakage validity protocol for substitution benches | none direct | Methodological hygiene, not a research claim | Hold as gates, not RQs |

## 3. Consistency vs discussion.md — silent scope changes

**Does the economics delta survive?** Partially. The ledger + erosion ratio (N2) actually
*sharpens* the economics beyond discussion.md (cost-of-hiding F5 promoted to a first-class
module — good). But the paper drifted in four silent ways:

- **S1. The stance is gone (scope deflation).** discussion.md's C4 conclusion — "where behavioral
  detection is cheap to defeat, only cryptographic/TEE-backed attestation + disclosure norms close
  the gap; TLS-for-model-serving, empirically grounded" — and its decision map (RQ4/SP4, Fig 6)
  are absent. The mandated foil **2604.27789 (governance of silent updates) is never cited**; the
  2504.04715 TEE-necessity delta is reduced to one sentence. The draft ends as a neutral
  framework paper; the position that justified C4 in the portfolio has been silently dropped.
- **S2. Science RQs swapped for validity RQs (scope substitution).** discussion.md's headline
  hypotheses — R2-cheaper-than-R1 **asymmetry** (F3), **noise-masking bound** (SP3/F4), **cost
  cliff** frontier shape — do not appear. All six draft RQs test the *measurement apparatus*
  (artifact AUROC ≤ 0.60, leakage AUROC ≤ 0.55, frontier stability ≤ 0.02, adaptivity ≥ 0.10,
  ledger error ≤ 10%, erosion ≥ 1.0). Only RQ6 is a science claim. The R1/R2/R3 stratification is
  collapsed into a single label y∈{0,1}, so the paper cannot even state the asymmetry hypothesis.
- **S3. Adversary silently inflated past the fairness bound.** discussion.md scoped A3 to
  lightweight post-processing ("NOT retraining; retraining-based spoofing is future work / an
  upper bound"). The draft's grammar leads with **parameter-efficient fine-tuning** and adds
  **selective escalation to the expected model** — a strictly stronger adversary with no fairness
  principle stated, recreating the strawman/unbounded dilemma Stage 6's critic flagged. (PEFT is
  defensible given GhostPrint, but must be an explicitly labeled upper tier, not the core.)
- **S4. Motivation hedged into vacuum.** The draft says prior evidence "does not establish that
  commercial providers currently perform silent downgrades" — yet its own cited MET paper
  (2410.20247) *measured 11 of 31 commercial endpoints serving distributions different from
  reference weights*, and IRIS (2607.20860) flags live provider pairs. The Stage-0 substitute-
  incident rule (mine the auditing literature for primary-verified incidents) was available and
  unused. Also: no MPU/staging (24 resource cells × 20k episodes × double-oracle with PEFT inner
  loops ≈ an unbounded compute plan vs discussion.md's core = R2 + one ladder), and no
  benign-drift-vs-adversarial-substitution scope statement (B3-family separation).

## 4. Citation audit (load-bearing, verified via arXiv API)

| Citation in draft | ID | Verdict |
|---|---|---|
| Gao et al., Model Equality Testing | 2410.20247 | ✓ real (title/author match) |
| Cai et al., Are You Getting What You Pay For | 2504.04715 | ✓ real |
| Zhu et al., Rank-Based Uniformity Test | 2506.06975 | ✓ real |
| Jiahao Zhang et al., "Pro" Subscription / fingerprint spoofing (GhostPrint) | 2606.16100 | ✓ real |
| Yuewei Zhang et al., IRIS | 2607.20860 | ✓ real (ID absent from draft) |
| Fang et al., KBF | 2605.29524 | ✓ real (ID absent from draft) |
| Carlini et al., Stealing Part of a Production LM | 2403.06634 | ✓ real |
| Sun et al., SVIP | 2410.22307 | ✓ real |
| Pasquini et al., LLMmap | 2407.15847 | ✓ real (draft misattributes authors: says "Kornaropoulos & Ateniese"; Pasquini is first author) |
| Yamabe et al., MergePrint | 2410.08604 | ✓ real |
| Karvonen et al., DiFR | 2511.20621 | ✓ real |
| One-token fingerprinting | 2607.10252 | ✓ real — **known prior, missing from draft** |
| Logprob tracking | 2512.03816 | ✓ real — **known prior, missing from draft** |
| Governance of silent updates | 2604.27789 | ✓ real — **mandated foil, missing from draft** |

Zero confabulations (sibling signature confirmed). But: every reference is "[n.d.]" with no IDs,
the related-work section carries a literal "requires manual completion" placeholder, one author
misattribution (LLMmap), and three known 2025–26 neighbors from the pipeline's own ledger are
missing. RAFP / SEAL / SRAF / NanoZK / Pal et al. could not be ID-verified in this narrower sweep
(no IDs given; low load-bearing — lineage/IP subthread) — keep only with IDs located or drop.

## 5. Gap to implementation

- **No minimum publishable unit.** The full plan (12 nuisance families × 900 episodes, 60
  leakage days, 24-cell covering array × 20k episodes × double-oracle alternation with PEFT
  best-response search, 30 cost traces, 24 scenarios × 9 budgets) is a multi-quarter,
  multi-cluster program. discussion.md's M1/M2 staging and G1/G2 pilot gates were dropped.
- **Double-oracle convergence is assumed, not designed:** no restart policy, no strategy-space
  truncation argument; RQ3's ≤0.02 equivalence bound will simply fail to certify if the PEFT
  best-response search is noisy — and nothing says what happens then.
- **"Blinded/sealed/preregistered/person-hours" operational machinery is unimplementable as
  specced** for a small team (who is blinded from whom when the auditor's authors build the
  adversary?). Needs honest downgrade to "labels withheld from detector-fitting code paths."
- **Concrete checkpoints never named** (which m0 / m0* / m1, which quantizations), so effect
  sizes, GPU budget, and the noise-calibration protocol cannot be costed.
- Whole-cluster energy metering (RQ5) requires hardware access the project may not have; a
  ledger-vs-simple-proxy validation on 1–2 nodes is the realistic version.

## 6. Verdict + top-3 fixes

**Verdict: Major revision.** The core economics delta (frontier + erosion ratio) survives and is
genuinely unclaimed — the draft's ledger/erosion machinery is a real improvement over
discussion.md. But the paper silently deflated the stance (missing mandated foil 2604.27789,
missing decision map), substituted apparatus-validity RQs for the falsifiable science hypotheses
(asymmetry, cost cliff, noise-masking), inflated the adversary past the agreed fairness bound,
and shipped placeholder citations with three known neighbors missing. As written it would be
reviewed as a detector-plus-benchmark methods paper — the exact drift the design doc warned about.

1. **Restore the stance and the science headline.** Reinstate R1/R2/R3 stratification; state the
   three falsifiable frontier-shape hypotheses (R2-cheaper-than-R1 asymmetry; cost cliff vs
   graceful degradation; noise-masking bound); reinstate the decision map and the Implications
   section with the named deltas over 2504.04715 (TEE-necessity, now empirically located on the
   frontier) and 2604.27789 (enforceability substrate for governance), with the measured-vs-argued
   boundary typographically explicit.
2. **Re-stage the experiment around an MPU with gates.** Core = R2 tier-downgrade frontier under
   calibrated noise against ladder A0–A3 (A3 = Kerckhoffs-bounded lightweight post-processing);
   PEFT/GhostPrint-style tuning and selective escalation become explicitly labeled upper tier A4;
   validity RQs demoted to pilot gates G1–G4; extensions (R1, noise-masking, full covering array)
   gated at M2. Name the checkpoints.
3. **Fix the bibliography and motivation.** Real arXiv IDs throughout; add 2604.27789, 2607.10252,
   2512.03816; fix the LLMmap attribution; drop or verify RAFP/SEAL/SRAF/NanoZK; ground "why now"
   in the verified in-the-wild numbers already in hand (MET's 11/31 endpoints; IRIS's 14/15
   provider pairs) instead of the unverified V1/V2 incidents; add the benign-drift (B3-family)
   scope separation.

**Inferred unresolved majors** (would surface in external review): (a) double-oracle cost and
convergence realism; (b) whether the erosion ratio is measurable at all when gross savings are
small (the eligibility rule may exclude the central case, leaving RQ6 vacuous); (c) external
validity of self-hosted noise calibration for closed frontier-lab serving stacks; (d) adversary
fairness — any fixed grammar can be attacked as strawman; the whole-curve-per-tier reporting
must be the response and needs to be in the threat model, not the appendix.
