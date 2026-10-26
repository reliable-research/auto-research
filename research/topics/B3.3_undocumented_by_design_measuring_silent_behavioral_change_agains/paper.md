# Undocumented by Design? Measuring Silent Behavioral Change against Vendor Changelogs — Pre-Registered Paper Specification
> Generated from digest.md + README.md. Status: specification, no experiments run.

## Step 0 — Core Asymmetry (升维)

**Asymmetry sentence:** The party that controls when a deployed AI system changes is also the sole author of the record of what changed, so the completeness of that record is unverifiable from inside it — only an external measurement of behavior can bound how much change the record omits.

**判据 (deletion test):** Delete the domain nouns —
> "The party that controls when *a thing* changes is also the sole author of the record of what changed, so the completeness of that record is unverifiable from inside it — only external *measurement* can bound how much the record omits."

Stripped of "deployed AI system / changelog / behavioral probe," the sentence collapses to a generic tautology about self-reporting; it no longer names *behavioral change measured against the author's own disclosure text* and cannot generate the estimand (silent-change rate = measured diffs with no matching disclosure). It reads as empty, not as a valid generic claim → the sentence is an asymmetry, not a bridge. PASS.

(This is not "changelogs and behavior audits were never connected, so we connect them" — the load-bearing content is the *structural conflict of interest between change-controller and change-documenter*, which makes the record's incompleteness the object of measurement.)

---

## Step 2 — Archetype

**Primary archetype:** New Measurement / Instrument-and-Finding (empirical), consistent with digest **N12 = `empirical`**: the headline deliverable is the *rate and category-distribution of undocumented behavioral change* (CO1/CO3), with the probe+alignment pipeline (CO2) as instrumentation.

**Secondary:** Tool/Infrastructure (CO2), subordinate — the pipeline is a means to the measurement.

**Downstream consequences:**
- **(a) Abstract contribution slot:** a *number with a confidence interval* — "X% of statistically-detected cross-version behavioral diffs have no matching changelog entry, concentrated in categories {…}" — plus the validated instrument that produced it. Not a method-superiority claim.
- **(b) Intro logic:** "what becomes possible" — external, reproducible quantification of documentation fidelity that no first-party actor will produce (README: "厂商结构性不会自己做"). NOT "beat baseline number X."
- **(c) Evidence standard:** a measurement is credible only if the instrument's error is characterized: M3 false-positive rate on same-version null pairs must be bounded, and M4 alignment must be validated against human labels. The result section stands on *calibration of the instrument* + *effect sizes*, not on a leaderboard delta.

---

## Step 3 — Taste self-audit

- **Is the opportunity a Bridge?** Risk: "align changelog text with behavior diffs" sounds like connecting two existing things. Corrected framing: the object is not the connection but the *quantified gap* the connection exposes — the silent-change rate as a partially-identified estimand (lower bound, C3). The contribution is a measured quantity about a structural conflict of interest, not the act of aligning. PASS after reframing.
- **Is the method mere Synthesis?** The components (change detection, entailment matching, sequential testing) are reused from N3, but the *estimand* — documented-vs-silent rate per behavior category — is new and is what is defended. Synthesis of tools serving a novel measurement is acceptable for an empirical archetype. PASS.
- **Load-bearing verbs:** target verbs are *measure, bound, calibrate, isolate, attribute* — not *integrate/unify/leverage*. PASS.
- **Abstract-opening rule:** v0 below opens with the mechanism/asymmetry (change-controller = change-documenter) and uses *measure/bound/calibrate*; the "X is increasingly used… however… we introduce" template is avoided. PASS.

---

## Step 5 — Formal Problem Definition

**Notation.** Target system with versions $v_t, v_{t+1}$. Probe suite $P = \{p_1,\dots,p_M\}$, each $p_i$ a fixed (prompt, decoding-config) pair belonging to category $c(p_i) \in \mathcal{C}$ (factual QA, refusal/safety, instruction-following/formatting, reasoning/math, tool-calling, latency/cost). For probe $p$ and version $v$, draw $N$ samples $S_{p,v} = \{y_{p,v}^{(1)},\dots,y_{p,v}^{(N)}\}$. Changelog for the transition is text $L_{t\to t+1}$, parsed into claim set $\mathcal{K} = \{k_1,\dots,k_R\}$.

| Adjective/verb (from Claims/N8) | Formal definition | Measured by |
|---|---|---|
| "measurable behavioral change" (probe $p$ has a diff) | $D(p)=1$ iff two-sample distance $d(S_{p,t},S_{p,t+1})$ exceeds same-version null $d(S_{p,t},S'_{p,t})$ at permutation $p\text{-val}<\alpha$ (Holm-corrected) **and** $|\text{Cliff's }\delta| \ge 0.33$ | M3 |
| "genuine vs stochastic" (C1) | null distribution of $d$ estimated by within-version resampling of $S_{p,t}$; diff genuine iff outside null CI | M3 |
| "documented" (probe's diff is covered) | $\text{Doc}(p)=1$ iff $\exists k\in\mathcal{K}$ with entailment score $e(\text{diff}(p),k)\ge\tau$ (τ tuned on human-labeled dev subset) | M4 |
| "silent / undocumented" | $\text{Silent}(p)=1$ iff $D(p)=1 \wedge \text{Doc}(p)=0$ | M4/M5 |
| "silent-change rate" (per category $c$) | $\rho_c = \frac{\sum_{p:c(p)=c} \text{Silent}(p)}{\sum_{p:c(p)=c} D(p)}$; overall $\rho=\frac{\sum_p \text{Silent}(p)}{\sum_p D(p)}$ | M5 |
| "concentrate" (RQ2) | $\rho_c$ non-uniform across $\mathcal{C}$: reject $H_0:\rho_c$ equal $\forall c$ via chi-square / proportion test | M5 |
| "accurately reproduces" (M4 vs human) | $F1(\text{Silent}_{\text{auto}}, \text{Silent}_{\text{human}}) \ge$ threshold on held-out labeled subset | M4 validation |
| "clean version boundary" (C4) | logprob-fingerprint discontinuity $>$ within-version fingerprint variance at fixed threshold | M2 |
| "lower bound" (estimand, C3) | $\rho$ conditioned on coverage of $P$; true rate $\ge$ measured only if undetected diffs are ≥ as silent — reported as bound, not point estimate | framing |

Any adjective without a row above is deleted from claims.

---

## Assumptions (A1..An)

- **A1 (measurable-diff separability, C1):** same-version sampling noise is estimable and stationary enough that a genuine cross-version diff is separable from it. *Fail:* heavy load-dependent routing makes same-version variance non-stationary. *Detect:* pilot measures M3 false-positive rate on same-version null pairs. *Gate:* **PG-1**, checked in the walking skeleton's same-version A/A arm (Step 9); fails if FPR > α.
- **A2 (changelog exists and is parseable, C2):** the vendor publishes changelog/release-note text for the transition, parseable into discrete claims. *Fail:* no changelog, or pure marketing prose with zero behavioral claims. *Detect:* Stage-0 pilot confirms ≥1 parseable claim exists for the chosen transition before scaling. *Gate:* **PG-2**, checked in the walking skeleton before any probe run is scored.
- **A3 (entailment matching is feasible, C2):** semantic entailment between a behavioral diff description and a changelog claim is learnable to usable accuracy. *Fail:* diffs and claims live in incommensurable vocabularies. *Detect:* M4 F1 vs human labels; F1 < 0.7 flags A3 risk. *Gate:* **PG-3**, checked at RQ3 (H3(a)) — must clear before M4 labels are trusted for RQ1/RQ2's headline rate.
- **A4 (approximate version boundaries, C4):** version transitions can be pinned to release windows via timestamped polling + fingerprinting well enough to attribute a diff to a release. *Fail:* fully undated rolling deploys. *Detect:* M2 fingerprint discontinuity check; transitions without a clean discontinuity are quarantined (reported separately, not in headline). *Gate:* **PG-4**, checked in the walking skeleton's boundary-attribution arm (Step 9 / RQ_boundary).
- **A5 (probe coverage informativeness, C3):** the category-stratified probe suite covers enough behavior that the measured lower-bound rate is informative (not vacuously low). *Fail:* suite too narrow. *Detect:* ablation over probe subsets (t2 mitigation) — rate stability across subsets. *Gate:* **PG-5**, checked at scale-up (Stage 1) via the split-sample coverage-stability check, not inside the cheap pilot (probe-subset ablation needs the full Stage-1 suite to be meaningful).
- **A6 (partial identification accepted):** stakeholders accept a lower-bound estimand. *Fail:* reviewers demand the true rate. *Detect:* framed explicitly; not empirically detectable, handled in threats (t4). *Gate:* **PG-6** — a framing check only (no pilot pass/fail is possible), verified at Phase A/G review that Abstract/Results never assert the point-estimate reading.

---

## Step 6 — Pre-Registered Experiments

### RQ1 — What proportion of measured behavioral changes are undocumented? (digest N8 RQ1; CO1; M3,M4; C1,C2)

- **Assumption:** A1, A2, A3, A4.
- **Hypothesis H1:** overall silent-change rate $\rho > 0.50$ — a strict majority of statistically-detected cross-version diffs (with $|\delta|\ge0.33$) have no matching changelog claim, with the bootstrap 95% CI lower bound also $> 0.50$.
- **Metric:** $\rho = \frac{\sum_p \text{Silent}(p)}{\sum_p D(p)}$; bootstrap 95% CI over probes.
- **Verification:** per probe, $N=50$ samples/snapshot; permutation two-sample test at α=0.05 with Holm–Bonferroni across probes within a transition; effect-size floor $|\delta|\ge0.33$; bootstrap CI on $\rho$ (≥1000 resamples). Reported per-vendor, not pooled.
- **Aggregation (cross-vendor vote rule):** because $\rho$ is computed and CI'd separately per vendor (not pooled), H1 is scored **PASS** only if $\rho>0.50$ with the CI lower bound also $>0.50$ holds in **≥2 of the ≥3 tested vendors** (majority rule, mirroring H2's per-category power floor); a vendor contributing fewer than 20 detected diffs is excluded from the vote as underpowered and reported separately, never counted as a "no" vote. If exactly one vendor is tested at the Stage-0 pilot scale, H1 is provisionally scored on that single vendor and explicitly flagged **INCONCLUSIVE-pending-scale-up** rather than PASS/FAIL until Stage 1's ≥3-vendor vote is available.
- **Fallback F1:** if the cross-vendor vote fails (fewer than 2 of ≥3 vendors show CI lower bound $>0.50$), claim shifts to: "silent changes are a *material minority* — $\rho$ = [measured] (CI …), demonstrating that even under strong disclosure the undocumented fraction is non-negligible," and reframe headline around the *existence and category structure* (RQ2) rather than majority prevalence.

### RQ2 — In which categories do silent changes concentrate? (N8 RQ2; CO3; M1,M5; C2)

- **Assumption:** A1, A5.
- **Hypothesis H2:** $\rho_c$ is non-uniform across categories (chi-square rejects equality at α=0.05), AND the rank order places safety/refusal, formatting/instruction-following, and latency/cost strictly above factual-accuracy ($\rho_{\text{safety}},\rho_{\text{format}},\rho_{\text{latency}} > \rho_{\text{factual}}$, each pairwise proportion test at α=0.05 Holm-corrected).
- **Metric:** per-category $\rho_c$ with bootstrap 95% CIs; chi-square across categories; pairwise proportion tests.
- **Verification:** chi-square test of homogeneity of $\rho_c$; Holm-corrected pairwise proportion tests for the three predicted orderings; minimum 20 detected diffs per category for a category to enter the test (else pooled/reported as underpowered).
- **Fallback F2:** if uniform (chi-square not rejected) → claim "silent change is *pervasive and category-agnostic* — no behavior type is reliably documented." If non-uniform but different order (e.g., factual most silent) → report the *observed* concentration as the finding (the taxonomy is the contribution regardless of direction).

### RQ3 — Does the pipeline reproduce human labels and control false positives? (N8 RQ3; CO2; M3,M4; C1,C2)

- **Assumption:** A1, A3.
- **Hypothesis H3:** (a) M4 automatic silent/documented labeling achieves $F1 \ge 0.70$ against a human-labeled subset; AND (b) M3 false-positive rate on same-version null probe pairs $\le \alpha = 0.05$.
- **Metric:** $F1(\text{Silent}_{\text{auto}}, \text{Silent}_{\text{human}})$; M3 FPR = fraction of same-version null pairs flagged $D=1$.
- **Verification:** human-labeled subset ≥200 diff/claim pairs, two annotators + adjudication, report Cohen's κ (require κ ≥ 0.6 for label validity); M3 FPR measured on ≥200 same-version pairs; binomial CI on FPR.
- **Fallback F3:** if F1 < 0.70, report M4 as a *human-in-the-loop* aid (auto-flag + human adjudication) and present the silent-rate on the human-labeled subset only, downgrading the automatic-pipeline claim from CO2's headline to "assistive." If M3 FPR > α, recalibrate the effect-size floor upward (report the floor that restores FPR ≤ α) and re-derive rates; the corrected floor is pre-committed to be reported transparently.

### Mandatory baselines

- **B0 "why do this at all" control (no-mechanism arm):** the *assume-everything-documented* / naive-string-match baseline — align diffs to changelog by keyword/string overlap only (no semantic entailment). If a trivial string matcher already labels ≥ (1−ρ) of diffs as documented, semantic alignment adds nothing and the problem is a lookup, not an inference. This justifies M4's existence. Paired with the *same-version null arm*: run the full pipeline on two same-version snapshots — it must yield $\rho$ on essentially zero detected diffs (D≈0); a non-trivial "silent rate" here would mean the pipeline manufactures its own finding.
- **B-alt strongest-alternative-explanation control (capability/budget-matched):** the rival explanation is *"detected diffs are just sampling noise / prompt sensitivity that the vendor correctly did not document because nothing really changed."* Control arm: budget-matched — same $N=50$ samples, same probes, but comparing two *same-version* resamples (A/A test) at equal API cost. The claimed cause (real cross-version change) is isolated only if cross-version $\rho$ and diff count exceed the A/A arm by a pre-registered margin (cross-version detected-diff count ≥ 3× the A/A false-diff count). This separates "vendor silently changed behavior" from "auditor's detector is trigger-happy."

### Global fallback F-G1

If the central hypothesis family fails (H1 refuted AND H2 uniform — i.e., silent change is neither prevalent nor structured), **pivot archetype from measurement-finding to instrument/methodology**: the contribution becomes the *validated, reusable documentation-fidelity audit pipeline with characterized error rates* (CO2 promoted to headline), and the empirical result is reframed as a *calibration study establishing that vendor changelogs for the tested systems are largely faithful* — itself an accountability-relevant null. Pivoted abstract sentence: "We build and validate the first external instrument that measures documentation fidelity of versioned AI APIs against their vendor changelogs, and report its precision/recall and false-positive characteristics on N transitions across M vendors."

---

## Step 9 — Walking Skeleton

**One binary question:** On ONE vendor, ONE clean-boundary version transition, does the pipeline detect ≥1 statistically-genuine behavioral diff (D=1, |δ|≥0.33) that has NO matching changelog claim — while flagging ~0 diffs on a same-version A/A control?

- **Arms (3):** (1) cross-version pipeline; (2) same-version A/A null control; (3) B0 string-match aligner on the same diffs.
- **Smallest task set:** ~200 probes across 5–6 M1 categories (the digest Stage-0 pilot), $N=50$ samples/probe, 2 cross-version snapshots + 1 same-version resample.
- **Deterministic metrics only:** count of D=1 probes (cross vs A/A), $\rho$ on the pilot set, string-match vs entailment agreement — all computable without human labels for the go/no-go (human labels validate M4 afterward).
- **Expected cost/wall-clock:** ~200 probes × ~3 snapshots × 50 samples ≈ 30k short API calls → low-hundreds-USD, ≈1–2 days wall-clock incl. polling; no GPU training.
- **Skeleton-passed criterion:** cross-version arm yields ≥1 silent diff AND same-version A/A arm yields ≤ α·(#probes) false diffs AND M4 τ is set on a ≥20-pair dev slice. If passed, scaling to Stage 1 (3 vendors × 4 transitions × 1.5k probes) is a **config change** (probe-list size, vendor list, transition list) — no new code paths. Failure at the A/A gate = fix M3 before any scaling.
- **Assumption-gate mapping (PG-\*):** this skeleton is where the Assumptions section's pilot-checkable gates actually run: **PG-1** (A1, same-version A/A false-diff rate ≤ α) = the A/A arm above; **PG-2** (A2, ≥1 parseable changelog claim exists) = a precondition checked before Arm 1 is scored; **PG-3** (A3, M4 F1 ≥ 0.70) = checked once the ≥20-pair dev slice is labeled (may extend into early Stage 1 if the pilot's labeled subset is under-sized); **PG-4** (A4, clean fingerprint discontinuity) = required of the chosen transition before it is used at all. **PG-5** (A5, probe-subset rate stability) is *not* checked in this skeleton — it needs Stage-1 scale to be meaningful and is deferred there. **PG-6** (A6, lower-bound framing) is a writing-discipline check, not a pilot pass/fail, verified at Phase A/G review.

---

## Claim–Evidence Map

| Abstract claim | Status | Trace |
|---|---|---|
| A substantial share of measurable behavioral changes are undocumented | needs-experiment / fallback-covered | H1 (F1 fallback; cross-vendor vote rule, Step 6) |
| Silent changes concentrate non-uniformly by category | needs-experiment / fallback-covered | H2 (F2 fallback) |
| The instrument (M4 aligner, M3 detector) reproduces human labels and controls false positives — the validity precondition for the two claims above | needs-experiment / fallback-covered | H3(a) F1≥0.70 vs. human labels, H3(b) FPR≤α (F3 fallback: downgrade M4 to human-in-the-loop / recalibrate the effect-size floor, Step 6 RQ3) |
| Existing audit tools detect *that* a model changed but cannot label documented/silent | supported-by-design | N4 [LogProbTracking],[RankUniformity]; Step-5 def of Silent(p) |
| Vendors have no structural incentive to self-report; third-party audit is necessary | supported-by-design | GIVEN (README); Step-0 asymmetry |
| The measured rate is a lower bound, not the true rate | supported-by-design | Step-5 "lower bound" row; C3/A6/t4 |

Every claim traces to an H-id or a Step-5 definition.

---

## Abstract v0 (draft, mechanism-first) — DRAFT BEFORE RESULTS

The party controlling when a deployed AI system changes is also the sole author of the record of what changed, making that record's completeness unverifiable from within it. We measure the gap externally. We run a category-stratified behavioral probe suite against paired pre/post-version snapshots of LLM APIs, estimate a same-version noise floor by within-version resampling, and flag genuine diffs that exceed both a significance threshold and an effect-size floor. Each detected diff is aligned by semantic entailment to the vendor's changelog claims for that release window and labeled documented or silent; we calibrate the aligner against human labels and bound the detector's false-positive rate on same-version null pairs. We report a per-category silent-change rate (a coverage-conditioned lower bound) with bootstrap confidence intervals across multiple vendors and transitions, isolating real change from sampling noise via a budget-matched A/A control. The instrument and frozen audit trail are released.

*(≤150 words; mechanism-first; verbs measure/estimate/flag/align/calibrate/bound/isolate; no "increasingly used… however… we introduce" template.)*
