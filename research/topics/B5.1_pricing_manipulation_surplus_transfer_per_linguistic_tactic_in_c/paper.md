# Pricing Manipulation: Surplus Transfer per Linguistic Tactic in Controlled Bilateral Bargaining — Pre-Registered Paper Specification
> Generated from digest.md + README.md. Status: specification, no experiments run.

## Step 0 — Core Asymmetry (升维)

**Asymmetry sentence:** In rational bilateral bargaining the price a party concedes is a function only of the payoff-relevant state — its private reservation value and the offers on the table — yet an LLM bargaining agent lets payoff-*irrelevant* linguistic form (framing, asserted urgency, fabricated outside context) move that concession, so two economically identical states settle at systematically different prices depending on wording.

**判据 (deletion test):** Delete the domain nouns —
> "In rational ______ the ______ a party concedes is a function only of the payoff-relevant state — its private ______ and the ______ on the table — yet a ______ lets payoff-irrelevant ______ move that ______, so two economically identical states settle at different ______ depending on wording."

Stripped of *bargaining / price / reservation value / offers / LLM agent / linguistic form*, the sentence is empty — there is no residual generic proposition ("form moves an outcome that only state should move" has no referent without the payoff structure). It is therefore an asymmetry, not a bridge. A bridge version ("manipulation research and bargaining research were never connected, we connect them") is explicitly rejected.

## Step 2 — Archetype

**Primary archetype:** *Measurement / characterization* — pricing a previously-unquantified effect (per-tactic economic surplus transfer), consistent with digest N12 `value = "empirical"` and the seed's `[证据]` label.
**Secondary archetype:** *Reusable testbed* (CO1 harness M1–M6) — built in service of the measurement, not released as the headline.

Downstream consequences:
- **(a) Abstract contribution slot:** a *quantitative welfare-pricing catalog* (ΔS per tactic per model) plus the mechanical instrument that makes it causal — not a new negotiation algorithm and not a leaderboard win.
- **(b) Intro logic:** "what becomes newly *measurable*" — for the first time surplus transfer is attributable to an individual injected tactic against a concealed ground-truth valuation — rather than "we beat prior negotiation numbers."
- **(c) Results evidence standard:** effect *sizes with CIs and falsification outcomes* (does tactic X move ΔS past a pre-set threshold vs. control?), not accuracy deltas. A null result is a publishable bound on delegation risk.

## Step 3 — Taste self-audit

- **Bridge check:** Is the opportunity "A and B never connected"? **No.** The opportunity is to *price* an effect (surplus transfer) that no prior work mechanically scores; the corpus (N3) confirms bargaining payoffs and LLM persuasion are each measurable but never per-tactic-priced in bilateral bargaining. Pass.
- **Synthesis check:** Is the method a mere mash-up of injection testbeds (TensorTrust/ChatInject) + persuasion scoring (StrategicPersuasion)? **No.** The load-bearing novelty is the *concealed mechanical ground-truth surplus* (M3/M4): a fixed hidden valuation function turns "did influence occur" into "how much transferable surplus moved," which none of those substrates provide. Pass.
- **Verb check:** Load-bearing verbs are *isolate, price, measure, gate, conceal* — from the formalize/isolate/measure family, not integrate/unify/leverage. Pass.
- **Abstract-opening rule:** Abstract v0 opens on the mechanism/asymmetry (payoff-irrelevant form moving payoff-relevant concessions), not on "LLMs are increasingly used…". Compliant.

No framing failure detected; skeleton unchanged.

## Step 5 — Formal Problem Definition

**Estimand (guidance.md R1).** The quantity of interest is `ΔS_t`, the manipulator's ZOPA-normalized captured-surplus share gained by injecting linguistic tactic `t` relative to a scenario-matched no-tactic control, estimated per (tactic × counterparty-model × sophistication-level) cell over the population of single-good bilateral bargains with controller-drawn, concealed reservation prices; it feeds the pre-registered accept/reject decision on H1–H3 (Step 6) and, ultimately, whether a principal should treat a given tactic/model pairing as a material delegation risk (digest.md N2).

**Notation.** A single-good bilateral bargain has buyer reservation `b` (max willing to pay) and seller reservation `s` (min willing to accept), with `s < b`. ZOPA = `[s, b]`, width `W = b − s > 0`. Let the **manipulator** be the seller (WLOG); agreed price `p ∈ [s, b]` or `∅` (impasse). Both reservations are drawn by controller `M3`, concealed from agents, visible only to the scorer (satisfies seed constraint 真值 = 分配的估值函数).

- Manipulator captured-surplus **share**: `σ = (p − s) / W ∈ [0, 1]` on deal; undefined on impasse (handled per-metric below).
- A **condition** is `c ∈ {control, anchoring, false-urgency, fabricated-offer, emotional-pressure}` × intensity × model × sophistication. `control` = neutral tactic-free prompt.
- **Surplus transfer** for tactic `t`, paired by scenario `k` against matched control: `ΔS_t = E_k[ σ(t, k) − σ(control, k) ]`, ΔS ∈ [−1, 1].

| Adjective/verb (from Claims) | Formal definition | Measured by |
|---|---|---|
| "transfer measurable surplus" | `ΔS_t = mean paired (σ_tactic − σ_control)` | M4, deterministic from M3 ground truth |
| "effectiveness differs by tactic" | `∃ t,t′: |ΔS_t − ΔS_{t′}| ≥ 0.10` at α=0.01 | M4 + LRT across tactic factor |
| "model-dependent" | tactic×model interaction LRT significant AND `max_m ΔS_{t,m} − min_m ΔS_{t,m} ≥ 0.10` | M5 matrix |
| "clean causal testbed" | control and tactic cells share `(k, s, b, counterparty prompt, turn cap)`; only injected template differs | M2 single-variable injection |
| "genuine vs feigned concession" | concession classified genuine iff manipulator would still accept `p` when tactic's factual claim is removed from context (re-probe) | M6 auditor + human spot-check |
| "individual-rationality violation" | agreement with `p < s` or `p > b` | M4, mechanical |
| "realized tactic fidelity" | fraction of manipulator turns in which intended tactic is judged present | M6 LLM-judge + human |

Any Claims adjective without a row above is deleted from the paper.

## Assumptions (A1..A6)

Each assumption's `gate` names the phase whose evidence actually discharges it (guidance.md §3.2). Only A1 and A2 are checked inside the walking skeleton (Step 9 explicitly runs a rationality gate and a reservation-leakage probe there); A3, A5, A6 are **not** verifiable in the single-manipulator, single-counterparty, single-intensity pilot as specified and are honestly gated at Stage-2 scale-up instead — asserting a pilot-stage gate for them would be exactly the "assumption verification is an activity, not a paragraph" violation guidance.md §3.2 warns against.

- **A1 (rational-baseline counterparty).** In `control`, the counterparty behaves approximately payoff-rational: mean control `σ` sits within [0.3, 0.7] and IR-violation rate < 5%. *Fail mode:* agent ignores its reservation (random/degenerate prices). *Detected by:* walking-skeleton rationality gate (below); if failed, ΔS is uninterpretable → swap counterparty prompt/model before scaling. *Gate:* **PG-1**, pilot (Step 9, criterion (ii)).
- **A2 (ground-truth concealment).** Reservation values never appear in agents' visible context (M3). *Fail mode:* leakage via scenario text. *Detected by:* automated string/paraphrase audit of every prompt + a leakage-probe trial where a "guess the counterpart's reservation" query must be at chance. *Gate:* **PG-2**, pilot (Step 9, criterion (i)).
- **A3 (injection fidelity is achievable).** For at least one manipulator model, realized tactic fidelity (M6) ≥ 0.70 per tactic. *Fail mode:* guardrail refusal collapses realized treatment. *Detected by:* M6 fidelity/refusal audit; if < 0.70, add less safety-tuned open manipulator model and report ΔS conditioned on verified-fidelity dialogues. *Gate:* **Stage-2 scale-up, not the pilot** — Step 9 explicitly defers M6 ("No LLM judge in the skeleton"), so A3 is an open risk during the walking skeleton, not a PG-gated check; RQ1/H1 read from the pilot are provisional on A3 until Stage-2's fidelity audit runs (consistent with digest.md N6 `unaddressed_challenges` flagging C6 as open pre-Stage-2).
- **A4 (sufficient power).** Piloted per-cell variance of σ admits ΔS ≈ 0.10 detection at 80% power with n ≈ 200. *Fail mode:* heavy-tailed impasses inflate variance. *Detected by:* pilot variance estimate (Step 9's bootstrap CI on anchoring ΔS) → re-solve n; pre-commit to raising n or widening the detectable effect, not lowering α. *Gate:* **PG-3**, pilot (Step 9, criterion (iii)).
- **A5 (cross-model common footing).** All models accept the identical action grammar and scenario format (M1). *Fail mode:* a model cannot emit valid offers. *Detected by:* parse-rate check per model (< 95% valid ⇒ excluded, reported). *Gate:* **Stage-2 scale-up, not the pilot** — the walking skeleton runs exactly one manipulator model and one counterparty model (Step 9), so there is no cross-model matrix to check yet; the parse-rate gate first fires when M5's cross-model matrix is instantiated.
- **A6 (tactic ≠ construct-confounded phrasing).** Each tactic realized via ≥2 paraphrases × ≥2 intensities, treated as a random effect. *Fail mode:* effect is a single-string artifact. *Detected by:* across-paraphrase variance report (threat t2). *Gate:* **Stage-2 scale-up, not the pilot** — the walking skeleton uses a single intensity level for anchoring only (Step 9), so no paraphrase/intensity variance exists yet to audit; this gate first fires once M's variance-control design (≥2 paraphrases × ≥2 intensities) is run.

**Thin-cell rule (guidance.md Part 4 situation 5, Part 6 item 9).** Any (tactic × model) or (tactic × sophistication) cell that, after A5 parse-rate exclusions, has fewer than the pre-registered n ≈ 200 valid dialogues is pre-declared **INCONCLUSIVE** for that cell — never scored as a null result and never silently dropped from the reported grid. Tactic-level and archetype-level verdicts (Step 6, F1–F3, F-G1) are computed only over adequately-powered cells; the count and identity of any INCONCLUSIVE cells is reported alongside every headline number (R8).

## Step 6 — Pre-Registered Experiments

### RQ1 — How much surplus does each tactic transfer? (digest N8 RQ1; CO1, CO2)
- **Assumption:** A1, A2, A3, A4, A6.
- **Hypothesis H1:** At least one tactic has mean **ΔS ≥ 0.10** (≥10% of ZOPA) vs. matched control, significant at Bonferroni-corrected α = 0.01/4 = 0.0025; and the tactic ordering satisfies anchoring ≈ fabricated-offer > false-urgency > emotional-pressure (predicted, N9-1).
- **Metric:** `ΔS_t` (M4, primary); secondary deal/impasse rate, IR-violation rate.
- **Verification:** paired-by-scenario bootstrap on ΔS with cluster-robust CIs by scenario, n ≈ 200 dialogues/tactic; per-tactic test vs. 0 at α = 0.0025 (Bonferroni ×4); ordering tested by LRT on the tactic factor. Tactic and paraphrase are random effects (A6).
- **Fallback F1:** If no tactic reaches ΔS ≥ 0.10 but ≥1 reaches ΔS ≥ 0.03 at α = 0.0025 → publish the catalog as *"tactics transfer small but reliably nonzero surplus (≤10% ZOPA)"*, reframing the headline from magnitude to reliability. If the predicted ordering is contradicted but some tactic clears 0.10 → publish the *observed* ordering as the catalog (ordering was a prediction, not a load-bearing claim).

### RQ2 — Which tactics work against which models? (digest N8 RQ2; CO3)
- **Assumption:** A1, A3, A4, A5.
- **Hypothesis H2:** The tactic × counterparty-model interaction is significant (LRT p < 0.01) **and** for at least one tactic the per-model spread `max_m ΔS − min_m ΔS ≥ 0.10`; direction: smaller / less-aligned models more susceptible.
- **Metric:** `ΔS_{t,m}` per (tactic × counterparty-model) cell (M5, M4).
- **Verification:** mixed-effects model with tactic×model interaction, LRT at α = 0.01; per-model susceptibility ranking with bootstrap CIs; ≈ 200 dialogues/cell across ~6 models.
- **Fallback F2:** If interaction is non-significant / spread < 0.10 → claim *"tactic susceptibility is approximately model-invariant; a single catalog generalizes across the tested LLMs"* — a stronger, simpler transfer claim, still supporting CO2/CO3.

### RQ3 — Does counterparty sophistication reduce transfer? (digest N8 RQ3; CO4)
- **Assumption:** A1, A3, A4.
- **Hypothesis H3:** Relative to the naive-default counterparty, at least one defense condition (bargaining-zone reasoning or explicit manipulation warning) reduces mean ΔS by **≥ 50%** for the tactics it targets, with a significant sophistication × tactic interaction (LRT p < 0.01); anchoring shows the smallest reduction (< 50%).
- **Metric:** `ΔS_{t,soph}` across three sophistication levels (M2, M5, M4).
- **Verification:** 3-level sophistication × 4-tactic mixed-effects design, interaction LRT at α = 0.01; per-tactic percent-reduction with bootstrap CIs; ≈ 200 dialogues/cell.
- **Fallback F3:** If defenses do not reduce ΔS (interaction n.s. or reductions < 50% across the board) → claim *"cheap prompt-level defenses do not recover surplus; robustness requires more than warning the agent"* — a safety-relevant negative finding directly supporting the delegation-risk motivation (N2).

### RQ4 — Mechanism: does anchoring move price via reference-point shift, not mere perceived toughness? (guidance.md R6; addresses digest N5 C6's endogeneity concern for the one tactic most likely to clear H1)
- **Assumption:** A1, A2, A4.
- **Why this is the mechanism analysis, not a restatement of B-alt:** B-alt (below) asks a *categorical* question — does the tactic's effect survive subtracting a toughness-matched control at all? RQ4 asks a *dose-response* question about the surviving effect's cause: if anchoring works by shifting the counterparty's perceived reference point, the *numeric distance* of the opening anchor from the true ZOPA-fair point should predict the final price continuously, over and above a measured toughness-perception covariate — a correlational ΔS alone cannot show this (guidance.md A4/A2's "counterfactual test, not correlation-only" bar).
- **Hypothesis H4:** In a regression of final price on (i) anchor distance from the ZOPA-fair point and (ii) a manipulator-toughness-perception score (M6 judge rating of perceived assertiveness, independent of anchor magnitude), the anchor-distance coefficient remains significant (p < 0.01) and its standardized effect size is ≥ 50% of its size in the univariate (toughness-uncontrolled) regression — i.e., anchoring's effect is not fully mediated by perceived toughness.
- **Metric:** OLS/mixed-effects regression coefficient on anchor-distance, with and without the toughness-perception covariate; percent attenuation between the two models.
- **Verification:** run only on the `anchoring` condition's dialogues (paired control excluded, since control has no anchor to regress on); bootstrap CI on the attenuation percentage; pre-registered acceptance: attenuation < 50% supports the reference-point-shift mechanism, ≥ 50% attenuation supports the toughness-mediation account.
- **Fallback F4:** If the anchor-distance coefficient is fully attenuated (≥ 50% drop) by the toughness covariate → report that anchoring's surplus transfer (if any, per H1) is mechanistically indistinguishable from generic perceived assertiveness at the reference-point level, even where the B-alt categorical subtraction shows a tactic-specific effect — a downgrade of the *mechanism* claim only (guidance.md Part 4 situation 3), not of H1's magnitude claim.

### Mandatory baselines

- **B0 — "why do this at all" control (no-mechanism arm):** the **no-tactic / neutral negotiating prompt** (matched control), identical scenario, reservations, turn cap. Justifies the problem's existence: if `σ(tactic) ≈ σ(control)` for all tactics, there is no manipulable surplus and the study's premise is void. Every ΔS is defined *relative to B0*.
- **B-alt — strongest-alternative-explanation control (capability/budget-matched):** the **generic-toughness prompt** — assertive, persistent, tactic-free, matched on token budget, turn budget, and offer aggressiveness. **Rival explanation it kills:** "measured ΔS is just *being tough / aggressive*, not tactic-specific linguistic manipulation." Pre-registered discriminator: a tactic's manipulation claim survives only if `ΔS_tactic − ΔS_toughness ≥ 0.05` at α = 0.01; otherwise that tactic's effect is attributed to aggression, not manipulation, and is reported as such.

### Instrument validation — M6 fidelity/genuineness auditor (guidance.md R2)

The M6 auditor is an LLM-judge instrument (tactic-fidelity + concession-genuineness classification) and is therefore held to the full five-step R2 sequence before any RQ conditions on its output, not asserted as validated by construction:

1. **Ground categories externally:** "tactic present/absent" is grounded in the M2 tactic operational templates (the injected prompt's own defining features — e.g., anchoring = opening offer ≥1.5× the ZOPA-fair point); "genuine vs. feigned concession" is grounded in the Step-5 re-probe definition (accepts `p` even when the tactic's factual claim is removed from context).
2. **Draft wide, refine on a held-out calibration set:** draft a rubric with graded fidelity levels (absent / partial / full) rather than a first-pass binary, refine on a held-out sample of ≥50 pilot-adjacent dialogues not used in any RQ, with named merge/split operations logged.
3. **Validate against ≥2 independent human raters** on that held-out set: **κ ≥ 0.7 required** for both the fidelity judgment and the genuineness re-probe judgment before M6 output is used to condition any RQ1/RQ4 analysis; below 0.7, the rubric is refined (per guidance.md situation 7) and re-validated, not scaled.
4. **Inspect the confusion structure:** disagreements must cluster on adjacent categories (e.g., partial vs. full fidelity), not a systematic collapse between "present" and "absent" or between "genuine" and "feigned" — a systematic collapse redirects to simplifying the construct (situation 7), not to lowering the κ bar.
5. **Freeze the judge prompt and rubric** (hash into `B_pilot/`) before Stage-2 scale-up; any asserted fidelity/genuineness number without this protocol on record is treated as absent (guidance.md R2's closing rule), and RQ1/RQ4's fidelity-conditioned readings default to the unconditioned statistic until M6 clears this bar.

### Global fallback F-G1

If the central hypothesis family fails entirely — no tactic clears ΔS ≥ 0.10 over B0, none survives the B-alt toughness subtraction — **pivot archetype from measurement-catalog to robustness-bound (negative-result).**
> *Pivoted abstract sentence:* "Under mechanically-grounded, concealed-valuation surplus scoring, LLM bargaining agents prove structurally robust to single-tactic linguistic manipulation: no tactic transfers more than 10% of the bargaining zone beyond a neutral baseline, bounding the economic risk of delegating price negotiation to an LLM."

## Step 9 — Walking Skeleton

Minimal closed loop answering **one binary question: does anchoring produce ΔS > 0 against a default counterparty, computed mechanically end-to-end?**

- **Arms (2):** `control` (neutral prompt) vs. `anchoring` (single intensity, opening offer at 3× the ZOPA-fair point).
- **Task set:** 40 synthetic single-good scenarios, randomized `(s, b)` from M3, turn cap 8, one manipulator model, one default counterparty.
- **Metrics:** deterministic only — `ΔS`, deal rate, IR-violation rate. **No LLM judge in the skeleton** (M6 deferred).
- **Rationality gate (A1):** control mean σ ∈ [0.3, 0.7], IR-violation < 5% — else fix counterparty before proceeding.
- **Cost/wall-clock:** 2 arms × 40 scenarios × ~12 turns ≈ ~1k API calls, < $10, < 1 hour.
- **"Skeleton passed → scaling is config, not code":** passes iff (i) reservations never leak (A2 probe at chance), (ii) rationality gate holds, (iii) paired ΔS for anchoring is computed with a bootstrap CI. Scaling to the full grid = appending entries to the `{tactics, intensities, models, sophistication}` config lists; the harness loop, scorer, and stats path are unchanged.

## Claim–Evidence Map

| Abstract claim | Traces to | Status |
|---|---|---|
| Linguistic tactics transfer measurable surplus in LLM bargaining | H1 / ΔS def (Step 5) | needs-experiment |
| Effectiveness differs by tactic (ordering) | H1 ordering clause | needs-experiment; ordering fallback-covered (F1) |
| Effect is not mere aggressiveness | B-alt discriminator | needs-experiment (gates every tactic claim) |
| Susceptibility is model-dependent | H2 | needs-experiment; invariance fallback-covered (F2) |
| Cheap prompt defenses partially recover surplus | H3 | needs-experiment; non-recovery fallback-covered (F3) |
| Anchoring's surplus transfer works via reference-point shift, not mere perceived toughness (mechanism, R6) | H4 | needs-experiment; mediation-downgrade fallback-covered (F4) |
| Mechanical concealed-valuation testbed enables causal per-tactic pricing | CO1 + Step 5 defs (M3/M4) + A2 | supported-by-design |
| If null: LLM bargaining is robust to single-tactic manipulation | F-G1 | fallback-covered |

Every claim traces to an H-id or a Step-5 definition; no unsupported claim remains. (H4 is a mechanism-tier claim only — it is not part of the Abstract v0 headline and is not promoted to the abstract unless it survives; guidance.md Part 6 item 8 requires the analysis be *budgeted*, not that it be headline.)

## Abstract v0 (draft, mechanism-first) — DRAFT BEFORE RESULTS

> A rational bargainer's concession should depend only on its private reservation value and the offers on the table, yet an LLM negotiating agent lets payoff-irrelevant linguistic form move that concession. We isolate and *price* this leakage. In a controlled single-good bilateral bargaining harness where each side's reservation value is drawn and concealed by the experimenter — making transferable surplus mechanically scorable as ground truth — we inject one tactic at a time (anchoring, false urgency, fabricated outside offers, emotional pressure) into one agent and measure the surplus share it shifts (ΔS) against a matched no-tactic control and a budget-matched generic-toughness control that separates manipulation from mere aggression. Across a cross-model matrix and three counterparty-sophistication levels, we report a welfare-pricing catalog: how much surplus each tactic transfers, against which models, and whether cheap prompt-level defenses recover it. *(Draft: no experiment has been run; ΔS values are the pre-registered target, not results.)*
