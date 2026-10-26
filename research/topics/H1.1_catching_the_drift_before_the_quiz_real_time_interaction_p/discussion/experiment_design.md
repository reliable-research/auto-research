# Experiment Design Spec — H1.1 (standalone; Stage 6 confirmed output, 2026-08-15)

> This document is the executable protocol. It is synchronized with
> `paper_draft.md` § Experiments (same RQs, setups, expected outcomes, falsification
> conditions); if either changes, change both. `study_type: empirical` — **zero outcome-tier
> RQs**; every comparator below is a control or reference, not a competitor to beat. All numeric
> parameters are pre-registered design targets with stated rationales; **no experiment has been
> run and no result exists**.

## 0. Human-subjects, data-use, and calendar spine (read first — everything is gated on it)

Two IRB protocols, pipelined, plus one data-use agreement (DUA):

| Item | Action | Hard date |
|---|---|---|
| DUA request to base-RCT authors (Source A: the 52 session transcripts) | sent week 1; pursued, never depended on | answer deadline **2026-09-15**; unanswered → Source B auto-starts 2026-09-16 |
| Transcript-collection IRB (Source B; minimal risk, consented logging) | submitted immediately | approval expected well before 2026-10-31 (G0) |
| Live-RCT IRB (mild information asymmetry: participants know sessions are logged and an AI assistant is involved; arm and algorithmic trigger disclosed only at debrief) | submitted **2026-11-15** | approval assumed by Feb 2027 (expedited, 2–3 months [verify local IRB latency]) |
| Freeze-and-hash + OSF pre-registration (model, cutoff, pass table, nudge templates, analysis plan) | before the first live participant | gate G1 pass + IRB approval, whichever is later |

Gate calendar: **G0** 2026-10-31 (labeled offline set exists; annotator κ ≥ 0.7 on
erosive/protective); **G1** 2027-01-15 (sealed authorization gate; one pre-registered re-gate
allowed, absorbing to 2027-03-01 — CHI 2028 slack covers it); pilot Feb–May 2027; **G2**
2027-05-31 (internal replication directional + guardrails clean → scale-up); scale-up Jun–Aug
2027; CHI 2028 submission ~Sep 2027 (CSCW/AIES fallbacks). A data-free FAccT 2027 position paper
(deadline 2026-11-03) uses only the published evidence base plus this gated design as its
constructive proposal. Budget envelope: $35–50k participants + annotation, 6–8 person-months,
negligible compute.

## 1. Datasets

1. **Source A (pursued, not depended on):** the base RCT's 52 AI-arm session transcripts under
   DUA. *Justification:* maximal task/population fidelity to the published instrument; doubles
   the offline n if granted.
2. **Source B (fallback, auto-starts on DUA deadline):** fresh collection of 40–50 AI-assisted
   sessions on the reconstructed task under the transcript-collection IRB; **extends to ~60
   sessions if the DUA fails outright**, so the offline split below holds in every branch
   (marginal cost ~$3–5k over the 40–50 plan; these sessions double as the internal
   replication's first data). Every deviation of reconstructed materials from the original
   task/quiz is documented.
3. **Offline split:** all available sessions pooled and split **by developer** into a
   development set (**≥ 40 sessions**) and a sealed gate set (**≥ 20 sessions**) via an
   outcome-blind blocked hash balancing task family, experience, and source. *Rationale:* the
   prior package's 20-development/32-gate split starved the model and made the gate
   near-unpassable by construction (package review §5); ≥ 40 development sessions puts the
   expected erosive count at ~16–24 under the base paper's implied prevalence (roughly half of
   AI-arm sessions erosive — a design assumption checked at G0), enough for nested LODO
   cross-fitting plus cluster bootstrap; ≥ 20 gate sessions makes the prevalence-anchored exact
   bound passable by a genuinely useful detector (see RQ5 pass-table note).
4. **Live pilot dataset:** four-arm RCT, **n = 120 (30/arm), 144 recruited** (20%
   over-recruitment for attrition/screening failure), Prolific/Upwork, 1+ yr Python, no Trio
   experience, screening quiz with embedded Trio-familiarity trap questions; compensation
   $100–150 per 2–2.5 h session (~$16–18k participant cost at pilot scale).

## 2. Baselines / comparators (controls and references only)

- **Fold-train prevalence-only predictor** — the sanity reference every probabilistic claim is
  measured against (RQ2/RQ3/RQ4). Not a competitor: the study measures enrichment over it.
- **Human prefix ceiling** — upper reference for achievable prefix-time performance (RQ1).
- **Hand-code arm (H)** — the published control arm, reproduced for internal replication (RQ7).
- **Unnotified-AI arm (U)** — the published treatment arm, reproduced; reference for guardrails
  and reactivity contrasts.
- **Placebo-trigger arm (P)** — identical trigger policy/timing/length/presentation,
  content-free text; isolates notification reactivity from nudge content (RQ8).

## 3. Shared instruments

- **Feature extraction:** tier-1 deterministic log features; tier-2 LLM intent tags (frozen
  prompt; 15% human audit; κ ≥ 0.75 acceptance; failure → deterministic-only feature set is the
  declared instrument).
- **Labels:** two annotators, published six-pattern protocol; erosive/protective binary primary
  (κ ≥ 0.7 required, adjudicated); six-way descriptive only.
- **Risk model:** session-weighted elastic-net logistic landmark model, Platt calibration,
  nested leave-one-developer-out (LODO) cross-fitting; cutoff selected on fold-train only.
- **Trigger:** first crossing of frozen cutoff after floor k ≥ 3; ≤ 1 alert/session; risk
  frozen pre-notification.
- **Inference:** cluster bootstrap over developers with the full pipeline re-run per replicate
  (B = 2,000; the prior spec's 9,999 was compute theater at this n); exact Clopper–Pearson for
  the sealed gate; Holm correction within RQ families; MI(50) + Rubin + MNAR tipping points for
  live-trial missingness.

## 4. Research questions

### RQ1 (mechanism) — How early are erosive patterns humanly visible? (the ceiling)

- **Target hypothesis (H3, verbatim):** "At a prefix length no greater than half the median
  session length, human annotators labeling prefixes blind to session endings identify
  erosive-terminal sessions with precision exceeding the erosive-label prevalence by at least
  0.10."
- **Setup:** 30 development-session prefixes at k ∈ {1, 3, 5, 10}, labeled by the protocol
  annotators blind to endings; agreement with terminal labels per k.
- **Sample-size rationale:** 30 sessions × 4 prefix lengths = 120 prefix judgments per
  annotator; sized for a ±0.15 CI half-width on per-k precision at the implied base rate — a
  characterization target, not a hypothesis-testing one, since the ceiling is reported whatever
  it is.
- **Statistical test:** one-sided binomial test of precision > prevalence + 0.10 at the
  half-median-session k; per-k curves descriptive.
- **Expected outcome:** ceiling clears the margin at half-session but not at k = 1 (patterns
  become visible somewhere between the first query and mid-session).
- **Falsification condition:** refuted if the half-session human precision bound fails to clear
  prevalence + 0.10 — meaning the patterns are not humanly visible early and the real-time
  premise is bounded away; the ceiling is then the headline finding and the classifier RQs are
  reported as characterization only.
- **Metrics:** human precision/recall vs. terminal labels per k; inter-annotator κ on prefixes.

### RQ2 (mechanism) — Prefix-time detection precision

- **Target hypothesis (H1, verbatim):** "At a prefix length no greater than half the median
  session length, the cluster-bootstrap one-sided 90% lower confidence bound on the risk
  model's alert precision for erosive-terminal sessions, under nested leave-one-developer-out
  cross-fitting, exceeds the development-set erosive-label prevalence by at least 0.10."
- **Setup:** development set only; nested LODO; precision/recall at k ∈ {1,3,5,10} and elapsed
  10/20/30 min; cluster bootstrap (developers resampled, pipeline re-run).
- **Sample-size rationale:** ≥ 40 sessions / ~16–24 erosive (design assumption checked at G0)
  is the minimum at which the bootstrap lower bound can clear a +0.10 margin for a detector with
  true precision ≈ prevalence + 0.25; below that n the margin was shown unreachable
  (package-review feasibility analysis) — hence the dual-source plan.
- **Statistical test:** cluster-bootstrap one-sided 90% LB vs. prevalence + 0.10.
- **Expected outcome:** margin cleared at half-median session; not at k = 1.
- **Falsification condition:** refuted if the LB fails the margin at every k ≤ half-median
  session — the detector adds nothing a base-rate guess doesn't; G1 then fails regardless of the
  gate set (pre-registered no-go before sealing).
- **Metrics:** precision, recall, alert count, enrichment over prevalence, per k and per time
  checkpoint; gap to the RQ1 ceiling.

### RQ3 (mechanism) — Probabilistic prognosis quality

- **Target hypothesis (H2, verbatim):** "At each locked elapsed-time checkpoint (10, 20, and
  30 minutes), the risk model's session-weighted Brier score improves on the fold-train
  prevalence-only predictor by a relative margin whose cluster-bootstrap one-sided 90% lower
  bound exceeds 0.10, Holm-adjusted across the three checkpoints."
- **Setup:** as RQ2; Brier scores computed at the three locked wall-clock checkpoints.
  Ablations (pre-registered): regularization on/off; calibration on/off; checkpoint-by-index vs.
  by-time.
- **Sample-size rationale:** same as RQ2 (shared data and resampling scheme).
- **Statistical test:** relative Brier reduction, cluster-bootstrap one-sided 90% LB > 0.10,
  Holm over 3 checkpoints.
- **Expected outcome:** margin cleared at 20 and 30 min; 10 min inconclusive.
- **Falsification condition:** refuted if no checkpoint clears the Holm-adjusted bound — risk
  scores carry no calibrated information beyond the base rate.
- **Metrics:** session-weighted Brier per checkpoint; calibration slope/intercept; reliability
  diagrams.

### RQ4 (framing) — Can the features be thin? (zero-hardware sufficiency)

- **Target hypothesis (flagged limitation `lim_hardware_proxy`, verbatim):** "Deterministic,
  zero-hardware query-log features alone retain at least 50% of the full two-tier feature set's
  relative Brier improvement over the prevalence-only predictor at the half-session checkpoint."
- **Setup:** re-run the full RQ3 pipeline with tier-1 (deterministic) features only; compare
  relative Brier improvement against the full two-tier model at the half-session checkpoint.
- **Sample-size rationale:** shared with RQ2/RQ3.
- **Statistical test:** ratio of relative Brier improvements (deterministic-only / full), with
  cluster-bootstrap CI; retained fraction ≥ 0.5 is the pre-registered criterion.
- **Expected outcome:** deterministic-only retains ≥ 50% (the signal does not hinge on the LLM
  tagger), while the full set remains better (intents add real signal).
- **Falsification condition:** refuted if the retained fraction's CI falls below 0.5 — the
  detector's signal then depends on semantic intent tagging, and the "any logging proxy can
  deploy this" claim narrows accordingly (scope note pre-committed).
- **Metrics:** retained-fraction ratio with CI; per-tier feature importances (descriptive).

### RQ5 (mechanism) — Does the sealed gate authorize the live study?

- **Target hypothesis (H5, verbatim):** "The frozen model–cutoff pair passes the sealed gate:
  on a developer-disjoint gate set of at least 20 sessions scored exactly once at the
  half-session checkpoint, the one-sided 90% Clopper–Pearson lower bound on alert precision
  exceeds the development-set erosive-label prevalence by at least 0.10, with at least 5 alerted
  sessions and a false-positive burden of at most 0.3 alerts per protective-terminal session."
- **Setup:** freeze-and-hash (model, cutoff c, feature spec, exclusion rules, fully enumerated
  (alerts a, true-positives t) pass table) → score the sealed set **once**, in a single pass
  that evaluates the half-session criterion and logs each session's per-query risk trajectory
  (RQ6 reads those logs; sealed data is never re-scored) → apply the pre-enumerated decision.
  Zero alerts = no-go. One re-gate permitted after pre-registered narrowing to
  delegation-pattern-only detection; second failure retires the real-time premise as scoped.
- **Sample-size rationale / pass-table note:** at n = 20 gate sessions and prevalence ≈ 0.5,
  the criterion is passable at, e.g., a = 9, t = 8 (CP 90% LB ≈ 0.632 > 0.60) or a = 10, t = 9
  (≈ 0.663); a = 8, t = 8 also passes (0.750); a = 8, t = 7 fails (0.594). Reachable by a
  genuinely enriched detector, unreachable by a lucky constant guess; contrast the prior fixed
  τ = 0.70 LCB rule, which required ~90–100% observed precision.
- **Statistical test:** exact one-sided 90% Clopper–Pearson bound (pre-enumerated).
- **Expected outcome:** gate passes on the first attempt.
- **Falsification condition:** the gate is itself the falsification instrument: a fail (twice,
  including the one re-gate) refutes the deployable-detector claim at this n and scope; the
  pre-committed failure product is the RQ1–RQ4 characterization paper.
- **Metrics:** alert count, true positives, precision, CP LB, false-positive burden.

### RQ6 (mechanism) — Does the alert come early enough to matter? (lead time)

- **Target hypothesis (H4, verbatim):** "Among gate-set sessions correctly alerted under the
  frozen cutoff, the median first alert fires with at least 40% of the session's eventual query
  count still ahead."
- **Setup:** first-crossing times (floor k ≥ 3) read from the per-query risk trajectories
  logged during the gate set's single scoring pass (no re-scoring of sealed data); lead time =
  fraction of eventual query count remaining at first true alert.
- **Sample-size rationale:** bounded by RQ5's alert count (≥ 5 by the gate's own criterion);
  reported as a distribution with a sign-test on the median. The 40% floor is an authored design
  target: an alert with most of the session already spent cannot support a just-in-time
  intervention, and 40%-remaining leaves the nudge roughly the second half of the working
  session to act on.
- **Statistical test:** one-sided sign test, median lead time ≥ 0.40.
- **Expected outcome:** median lead time ≥ 0.40 among true alerts.
- **Falsification condition:** refuted if the median true alert fires with < 40% of the session
  remaining — detection would be real but too late, and the intervention claim is bounded by
  timing, not accuracy (reported as such; the live trial's detection-lag endpoint re-checks this
  in vivo).
- **Metrics:** lead-time distribution (query-index and wall-clock), per-arm in the live trial.

### RQ7 (mechanism) — Does the published hand-vs-AI gap internally replicate?

- **Target hypothesis (H7, verbatim):** "In the live trial, the unnotified-AI arm's mean quiz
  score is lower than the hand-code arm's — directionally replicating the published 17-point
  gap — with a one-sided test significant at α = 0.05."
- **Setup:** arms H vs. U from the four-arm RCT; blinded original-rubric grading (2 graders,
  κ reported); ANCOVA with baseline covariates (experience, screening score); MI(50) + Rubin;
  MNAR tipping-point sensitivity.
- **Sample-size rationale:** n = 30/arm gives ~80% power at α = .05 (one-sided) for the
  published d = 0.738 — the one contrast the pilot is confirmatorily powered for, by design.
- **Statistical test:** one-sided ANCOVA contrast, α = 0.05.
- **Expected outcome:** directional replication (U < H).
- **Falsification condition:** refuted if U ≥ H or the contrast is non-significant; the
  pre-registered interpretation tree then reports all intervention contrasts as estimation-only
  and the replication failure itself becomes a headline finding (the base effect is fragile —
  informative either way given the base paper's prominence).
- **Metrics:** quiz score by arm; standardized gap vs. the published d = 0.738.

### RQ8 (mechanism) — Does the nudge's content help, beyond reactivity, without collateral cost?

- **Target hypothesis (H6, verbatim):** "In the live trial, the active-nudge arm's mean quiz
  score exceeds the placebo arm's, with a point estimate of at least 40% of the internally
  replicated hand-vs-AI gap, while task-completion rate and median time-on-task in the active
  arm remain within 10% of the unnotified-AI arm."
- **Setup:** primary contrast N vs. P (content beyond reactivity), intention-to-treat and
  within the pre-trigger flagged subgroup (risk frozen before notification, so the subgroup is
  defined pre-treatment in all AI arms); secondary contrasts P − U (reactivity) and N − U
  (total policy effect); guardrails (completion, time-on-task) against U; intervention-integrity
  audit on 100% of firings; detection-lag endpoint logged in all AI arms.
- **Sample-size rationale:** at 30/arm the pilot is powered only for large recovery effects, so
  it is pre-registered as **estimation plus gate**: report the CI on the N − P contrast; proceed
  to scale-up (n ≈ 120–160, micro-randomized timing per the MRT design) iff the point estimate
  ≥ 40% of the replicated gap with guardrails clean — never as a confirmatory test of small
  effects. The 40%-of-gap floor is an authored target: recovering less than ~7 of 17 points
  would not justify a deployed interruption channel under the annoyance budget.
- **Statistical test:** ANCOVA contrast N vs. P with MI + tipping-point sensitivity; guardrail
  margins as pre-registered equivalence-style checks (±10%).
- **Expected outcome:** N > P with point estimate ≥ 40% of the replicated gap; guardrails
  within margins; P − U small.
- **Falsification condition:** refuted if N ≤ P (content adds nothing beyond reactivity), or if
  guardrails fail (the nudge "works" by degrading the session — vacuous), or if the effect
  exists only outside the flagged subgroup (the trigger, not the content, is misattributed).
  Each branch's reporting language is pre-committed in the interpretation tree.
- **Metrics:** quiz score by arm (ITT + flagged subgroup); completion rate; time-on-task;
  nudge-firing integrity rate; detection lag.

## 5. Traceability

| RQ | Tier | Hypothesis | Method module | Sub-problem |
|---|---|---|---|---|
| RQ1 | mechanism | H3 | human prefix-ceiling harness | hindsight-to-prefix transfer |
| RQ2 | mechanism | H1 | prognostic risk model | hindsight-to-prefix transfer |
| RQ3 | mechanism | H2 | prognostic risk model | thin-signal sufficiency |
| RQ4 | framing | rw_reliance_gaze flagged hypothesis | prognostic risk model (tier ablation) | thin-signal sufficiency |
| RQ5 | mechanism | H5 | sealed authorization gate | small-sample authorization |
| RQ6 | mechanism | H4 | first-crossing trigger | hindsight-to-prefix transfer |
| RQ7 | mechanism | H7 | four-arm assignment | comparability/replication |
| RQ8 | mechanism | H6 | nudge + matched placebo | wrong-reason interventions |

7 method hypotheses + 1 flagged-limitation hypothesis = 8 RQs; 0 outcome-tier.

## 6. Failure products (pre-committed)

- **G1 hard-fail (gate):** "How early are erosive AI-interaction patterns visible? A
  prefix-labeling ceiling study" — CSCW note built from RQ1–RQ4.
- **G2 replication-fail:** "A pre-registered replication of AI-assisted skill-formation
  effects" — headline finding either way given the base paper's prominence.
- Both keep the human-axis topic alive rather than sunk; neither requires new data collection
  beyond what will already exist.
