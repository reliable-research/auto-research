# Portfolio System — 2026-08 audit and reorganization

Purpose: per the 2026-08-13 directive, the topic map is now managed as a **portfolio system**,
not a flat list. Every topic carries a status; outdated/unfeasible ones are retired (folders
kept on disk as design notes — nothing deleted); the survivors are organized into execution
tiers with explicit sequencing. Companion doc: `position_paper_pipeline_2026-08.md` (the
fast, no-new-experiments track).

Audit method: three parallel reviews (B1/B2/T5, B3/B4/T3, B5/B6/H1) judged every topic
README against the 2026-08 evidence base (`trend_scan_2026-08.md`,
`industry_signal_scan_2026-08.md`, live web novelty sweeps) and the repo's own selection
filter (mechanical truth / binding constraint / no incumbent lockout), with the FSE 2027
(Oct 2, 2026) / ICLR 2027 (~late Sep 2026) windows as the feasibility clock.

Verdict scale: **KEEP-TOP** (lead bet: aligned with field direction + feasible in 3-6
months) · **KEEP** (sound, not a lead) · **HOLD** (premature by sequencing or crowding —
monitor, don't build) · **RETIRE** (outdated by field movement, argument occupied, or truth
source inaccessible).

Tally over 41 topics: 9 KEEP-TOP · 11 KEEP · 10 HOLD · 11 RETIRE.
2026-08-13 addendum: +4 sweep-verified Tier-2 topics (B7.1, B7.2, B8.1, B4.6 — see Tier-2
addendum below), bringing the map to 45 folders / 24 active.

---

## Tier 1 — Active leads (KEEP-TOP, 9)

The portfolio's bets. One shared pattern selected them: **ground truth that is executable or
historical-human** (mutants, state diffs, injected faults, past review verdicts, RCT quiz
scores) — never an LLM judge.

### Execution-oracle cluster (targets FSE 2027, Oct 2)
- **B1.2** — mutation-score-controlled boundary of visible-test overfitting. Best
  single fit to every 2026-08 fact: executable ground truth, mutation/differential design
  (the style SE PCs reward), and it mechanizes the production-measured green-tests-fail gap.
- **T5.2** — design-violating but functionally-equivalent mutants that test suites cannot
  kill. Turns ReactBench's 60.8% green-but-fails-static-analysis observation into a
  systematic account of *why*; existing mutation + static-analysis tooling.
- **T5.1** — mine implicit design constraints from code-review history; which ones agent
  patches violate while passing tests. Attacks the acceptance-gap oracle problem with
  historical human review verdicts as ground truth, on data that already exists.
  **Decay note 2026-08-13:** arXiv **2604.05955** ("Does Pass Rate Tell the Whole Story?",
  1,787 mined design constraints on 6 SWE-bench repos) is now a named near-twin for BOTH
  T5.1 and C3 — the whole execution-oracle cluster must position against it
  concede-and-claim (T5.1's surviving delta: review-history provenance + unwrittenness
  taxonomy + human-anchored validation; C3's: cross-layer oracle-fidelity comparison).
  Both revised drafts already carry the positioning; do not ship any cluster paper
  without citing it.
- **B2.1** — injected-fault "Defects4J-for-agents" causal attribution benchmark. Attribution
  is the largest and fastest-crowding tag (53.8%) but the crowd uses LLM-judge labels;
  mechanical injected-fault ground truth is the durable artifact. **Hard-ship clock: run a
  scoop check, target the Oct FSE window.** (Absorbs B2.3's cross-backbone RQ as one
  experimental axis; B2.2's replay-budget RQ as an evaluation section.)
  **Scoop-check result 2026-08-15 (ZB2.1 review):** Who&When Pro (arXiv 2607.09996,
  Jul 2026) is the confirmed nearest neighbor → the partial-scoop branch of the decision
  rule fires. Headline shifts to the certification-validity claim (four-arm
  identity/no-op/fault/bypass control lattice; RQ1) with method rankings secondary;
  B2.3 reframed as label survival across backbones. A full-web scoop check
  (OpenReview/GitHub/FSE lists) is still owed before build — WebSearch quota was
  exhausted during the review.

### External-audit cluster (targets ICLR 2027, ~late Sep)
- **B3.3** — silent behavioral change rate vs vendor changelogs. The accountability paper of
  the moment given documented checkpoint-substitution incidents; black-box, public
  changelogs, fits the repo's stated defensible edge (external audit).
- **B3.4** — contract breakage rates for structured-output pipelines per version jump.
  Directly operationalizes the vendor-admitted "scaffolding goes stale, no known detection
  method" gap in SE framing; weeks of corpus work, not months.
- **B4.2** — thinking/sampling/verifying exchange rates under a fixed dollar budget. Vendor
  release charts now show one slice of this frontier publicly, proving timeliness while the
  full 3-way substitution analysis is unclaimed. Must ship before the vendor-chart attention
  pulls the crowd in.

### Mechanism cluster (window-flexible)
- **T3.2** — mechanism of the soft-policy vs hard-norm decay asymmetry. The pinning-repair
  crowd ships fixes, not explanations; cheap controlled ablations, feeds defense design.

### Human-axis cluster (CHI/CSCW/AIES clock — runs in parallel, not instead)
- **H1.1** — real-time interaction-pattern classification + just-in-time intervention
  against AI-induced skill erosion. Strongest asset in the audit: validated effect
  (d=0.738), reusable taxonomy, the source paper's own open question as the delta, empty
  niche, no incumbent incentive to publish deskilling interventions. Cannot hit Sep/Oct
  windows (IRB, recruitment) — de-risk by building the classifier offline first; the
  position-paper form (see pipeline doc) is the fast companion deliverable.

## Tier 2 — Active support (KEEP, 11 + 4 added 2026-08-13)

Sound designs, not lead bets. Build when a Tier-1 neighbor creates the substrate or a
co-author wants a well-scoped project: **B1.1** (log-vs-state forgery — mechanism half is
the value), **B1.3** (checkpoint bypass; section-sized), **B2.4** (calibrated unsolvability
as attribution outcome), **B2.5** (attribution under corrupted observations), **T5.4**
(longitudinal architectural erosion), **B3.1** (probe-set design — strongest merged into
B3.3/B3.4; per the 2026-08-14 revised draft, its Section 7 module-contract now fixes
explicit merge/standalone/kill triggers against B3.3/B3.4, incl. a main-paper-figure
merge floor — honor these when B3.3/B3.4 ship), **B3.2** (drift variance decomposition; identifiability risk is internal),
**B4.1** (stopping-rule regret; ready-made motivation from vendor charts, moves fast),
**B4.5** (selective verifier-call allocation — complements rather than collides with the
stopping-rule wave), **T3.3** (adversarially robust constraint identification — precursor
problem the repair papers assume away), **B6.2** (contamination dose-response, refreshed by
the rarity-driven memorization result — absorbs B6.4's domain/rarity factor; the only B6
build target).

### Tier-2 addendum, 2026-08-13 — four survivors from the trend-cluster occupancy sweeps

The four `trend_scan_2026-08.md` §2 clusters were pressure-tested by parallel literature
sweeps (verdicts + full comparison sets in `trend_scan_2026-08.md` §6). All four original
cores are CROWDED/TAKEN; the promoted topics are the sweep-verified successor angles:

- **B7.1** skill-library depreciation across backbone upgrades (port/prune/relearn).
  Strongest of the four: mechanical ground truth (execution + token accounting), the
  model-version staleness axis is unclaimed while the environment-drift axis is 5 papers
  deep, and every frontier-model release is a repeatable natural experiment. **Promote to
  Tier 1 on the first cross-generation replay result.**
- **B4.6** verification-aware serving economics (extends B4). Public TraceLab traces
  remove the datacenter-access barrier; measurement phase (verification-induced cost share
  + KV-damage) can ship standalone to an MLSys/EuroSys measurement track while the policy
  phase matures. Distinct estimand from B4.5 (system-level $/resolved-task vs
  trajectory-selection precision).
- **B7.2** poison half-life survival analysis. Reuses published attacks/defenses as
  treatments; the laundering-amplification hypothesis (consolidation *extends* poison
  half-life) is falsifiable in both directions and connects two unlinked 2026 findings.
  Security-venue clock (USENIX Sec '27 / CCS).
- **B8.1** spec-drift differential conformance for MCP/A2A. Sharpest framing of the
  protocol cluster, but the scoop clock is **months** (AgentRFC full version, HCP overlap)
  and the spec's own churn is both the opportunity and the shelf life. Hard gate: demote
  to Tier 3 if no clause-diff probe pipeline exists within 3 months.

Sequencing note: B7.1 and B4.6 are independent of all existing Tier-1 substrate and can
start immediately; B7.2 and B8.1 are calendar-gated bets that should not displace the
FSE/ICLR Tier-1 clocks.

## Tier 3 — Hold / monitor (10)

Premature by sequencing (independent variable is infrastructure a Tier-1 topic must build
first) or waiting for an external unlock:

| Topic | What it's waiting for |
|---|---|
| B1.5 | B1.2-style environments + shortcut-seeking agent pressure to exist |
| B2.2 | B2.1's ground-truth-labeled trajectory corpus (fold into B2.1 eval if it ships) |
| T5.3 | T5.1's constraint cards + per-patch human annotation |
| T5.5 | T5.3's working enforcement mechanism |
| B3.5 | A multi-vendor probe time series (which B3.1/B3.3 would start accumulating) |
| B4.4 | A differentiator over router/early-exit work; also cuts against the black-box edge |
| T3.1 | A stabilized set of canonical pinning defenses worth attacking |
| B5.1 | A real agent-commerce deployment incident (family re-entry point; payoff-function truth is clean) |
| B6.1 | A generator-invariant statistic worth betting on, or B6.2 needing the estimator |
| B6.4 | Nothing external — folded into B6.2 as a design note |

## Tier 4 — Retired (11)

Folders remain on disk as design notes; removed from the active index. Reason categories:
**[occupied]** argument now belongs to someone else · **[outdated]** field/reality moved ·
**[unfeasible]** truth source doesn't exist · **[vacuous]** claim doesn't survive scrutiny.

- **B1.4** [vacuous] — conjunction of sound checks is trivially sound; the behavioral
  redefinition reduces to a hand-constructed existence gadget (the contrived style SE PCs
  penalize). Salvageable core lives in B1.1/B1.2/B1.5.
- **B1.6** [occupied, as an experimental topic] — post-audit, the delta reduced to
  implementing Yuan et al.'s (arXiv:2607.12340) own stated future work, with maximal scoop
  risk and a publisher-trust-annotated registry snapshot that doesn't exist. The
  position-paper form is tracked separately in the pipeline doc (verdict pending the
  security-literature novelty sweep).
- **B2.3** [occupied-imminent] — thin cross-model consistency table in the fastest-crowding
  area; merged into B2.1 as one experimental axis.
- **B4.3** [occupied + outdated] — the overthinking flip point is now printed in vendor
  release charts on top of a dense 2025-26 literature (2604.10739, 2507.14417, 2502.08235,
  survey 2503.16419); the crowd will absorb the residual delta first.
- **T3.4** [occupied-imminent] — the obvious engineering variant of pinning the repo's own
  README already said was "being filled"; the trade-off curve is the repair-groups' natural
  next figure.
- **B5.2, B5.3, B5.4, B5.5** [outdated + unfeasible] — the B5 economic-bargaining family
  collapses: no binding constraint (no deployment incident), and the field converged on
  multi-agent *adversarial robustness* (memory poisoning / knowledge corruption:
  2606.30566, 2608.04366; amplification: 2606.15008) with cleaner ground truth — the
  argument space is being occupied under a stronger framing. B5.1 alone survives as the
  monitored re-entry point.
- **B6.3** [unfeasible-structural] — the pre-2022 "certified-human anchor" is 4+ years stale
  and certified-human post-2022 text does not exist; what remains is a calibration
  subsection inside B6.1/B6.2.
- **B6.5** [unfeasible] — evasion economics played against a simulated adversary with
  assumed budgets; no accessible truth source.

---

## The system, going forward

1. **Two clocks.** Machine-axis leads (B1.2/T5.1/T5.2/B2.1 → FSE Oct 2; B3.3/B3.4/B4.2 →
   ICLR late Sep) run on the submission clock. The human-axis lead (H1.1) runs on the
   IRB/CHI-CSCW clock in parallel. Position papers (pipeline doc) are the fast track that
   can ship from existing evidence at any window.
2. **Sequencing is explicit.** Tier-3 topics are not "weaker ideas" — they are downstream
   of Tier-1 artifacts. Building a Tier-1 topic automatically re-opens its dependents.
3. **Retirement is cheap and reversible.** A retire verdict records *why* (occupied /
   outdated / unfeasible / vacuous) so a future unlock (deployment incident, new dataset,
   scooped-paper gap) can reverse it with evidence, the way the rarity-memorization result
   just refreshed B6.2.
4. **One admission rule.** Anything new enters the portfolio only with: mechanical or
   historical-human ground truth, a binding constraint already measurable in production or
   published RCTs, no incumbent lockout — and now additionally, a **novelty sweep against
   the position/argument literature before build**, since two of this cycle's retirements
   (B1.4's neighbor space, B4.3) were arguments that had already been claimed while the
   sketch sat in the map.

---

## 2026-08-22 addendum — full-portfolio review pass folded in

All 45 topics now carry `discussion/review_2026-08.md` (novelty-auditor defensive audit,
t_audit=2026-08-15, named nearest neighbors per claim + se-paper-reviewer feasibility/
staleness), with concede-and-claim revisions applied and mirrored into the compiled drafts,
plus Chinese versions. What the pass changes about the tiering:

### Tier 1 — all nine confirmed; three sharpened
- **T5.2** — the review found and FIXED a kill-criterion tautology (the admission-side
  trace-order checker doubled as the kill monitor, which would have pinned DMSR_TMP at 0
  by construction). Instrument-separation rule now in the draft. The lead is *stronger*
  post-review.
- **T5.1** — decay item 2604.05955 confirmed real and prior (thesis twin); contribution 1
  re-scoped, 🟢 relocated to the matched agent-vs-human estimand row. Ship-soon: half-life
  short.
- **B4.2 / B3.3 / B3.4** — verdicts 🟢 on estimand rows; B3.3's long-standing 2512.03816
  [VERIFY] resolved in its favor (LogProbTracking never aligns against disclosure text).
  B4.2's dollar-metering half is commoditizing — the "ship before vendor charts pull the
  crowd" clock is now review-confirmed.

### Tier 2 — one demotion recommended, four addendum topics confirmed
- **T5.4 → recommend demote to Tier 3** [occupied-partial]: SlopCodeBench (2603.24755,
  Mar 2026) already claims "first measurement of code degradation under iterative
  extension"; review verdict downgraded to 🟡. Surviving delta (matched same-task human-gold
  counterfactual on real brownfield repos, dependency-structure estimand) is real but
  short-lived. Hold condition: a differentiation result vs SlopCodeBench, or fold the
  counterfactual arm into T5.2's cluster.
- **B2.5** — 🟢 survives but the review caught a genuine prior miss (The Misattribution Gap,
  2605.22842, *pre-freeze*): the "never been tested" universals were false. Delta restated
  on channel/threat-model/diagnosis-target. Keep, with the humility note.
- **B7.1 / B7.2 / B4.6 / B8.1** (2026-08-13 addendum topics) — all four reviews returned 🟢
  on their estimand rows. B7.2's meta-verdict: "keep, tier: run-pilot-next" (two major spec
  gaps — probe-as-intervention, horizon-truncated durability — now conceded in-draft).
  B8.1's divergence-window estimand held against AgentRFC/DCI/MCPZoo/2608.14613.

### Tier 3 — one promotion trigger satisfied
- **B4.4** — the hold condition was "a differentiator over router/early-exit work"; the
  review's concede-and-claim vs 2512.22245 + 2605.09502 is exactly that differentiator
  (matched-realized-dollar routing estimand, no method twin found). **Promotion-eligible**;
  short half-life warned — promote only with an immediate build slot.
- **B3.5** — RQ6 (diversity trend) partially scooped by 2608.19437 (posterior to t_audit;
  the Wenger cluster is moving from simulation to longitudinal measurement); the
  capability-residualized cross-vendor correlation estimand is still unclaimed. Hold stands,
  clock shortened.
- T5.3, T5.5, B1.5, B2.2, T3.1, B5.1, B6.1, B6.4 — holds confirmed; B6.1's review relocated
  its 🟢 (RAID/MAGE wrong-modality miss fixed, invariance certification recast as TOST);
  T5.3 conceded 2604.05955 with a verifier-as-measured-object delta.

### Tier 4 — three retirements review-confirmed, three tensions for the user
Confirmed with named evidence: **B4.3** (2604.10739 + 2507.14417 occupy the finding),
**B6.5** (unanchored cost construct = the retirement grounds), **B6.3** (structural; execute
the narrowed C1 now or fold into B6.1/B6.2), **B5.2–B5.5** (concurred; B5.5's headline gap
died against Fish et al. 2404.00806 — a 27-month miss — though its identifiability-criterion
row stays clean).

**User decisions (flagged, not acted on):**
1. **B1.4** — the review's repositioned verdict (🟡→🟢, novel-in-formulation-and-estimand)
   undercuts the [vacuous] retirement grounds. Re-admit, or keep retired?
2. **B2.3 ↔ B2.1 merge** — B2.3's review confirmed its estimand distinct (cross-backbone
   label survival) and logged the merge as a governance tension, contra the Tier-4
   merged-away note.
3. **B2.2** — paper.md H2 registration amendment needed before Phase B (from the batch-1
   review).
Also noted: **T3.4**'s review returned 🟢 on the joint V/O/S estimand (CogniLoad = method
twin conceded) — weak re-entry evidence against its [occupied-imminent] retirement; no
action recommended yet.

### Fleet-wide signature (unchanged from batch 1, now confirmed across all 45)
Estimands and identification designs hold almost everywhere; related work goes stale in
~4–6 weeks in monthly-publishing clusters; the recurring failure is the *unqualified
universal negative* ("never been measured") — nearly every major/moderate finding was one
counterexample against it, half of them against papers the drafts already cited or used as
instruments. Every draft now carries concede-and-claim positioning instead.
