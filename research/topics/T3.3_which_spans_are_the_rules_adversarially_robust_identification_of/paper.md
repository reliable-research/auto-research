# Which Spans Are the Rules? Adversarially Robust Identification of Governance Constraints for Pinning — Pre-Registered Paper Specification

> Generated from digest.md + README.md. Status: specification, no experiments run.

## Step 0 — Core Asymmetry (升维)

**Asymmetry sentence:** A governance constraint's *binding (deontic) force* and its *surface register* are separable properties of the same span, so an adversary can preserve one while inverting the other — making any identifier that reads register a proxy for a target it does not actually measure.

**判据 test (delete domain nouns):** "A ____'s *X* and its *Y* are separable properties of the same ____, so an adversary can preserve one while inverting the other." → With `binding force`, `surface register`, `span`, `identifier`, `register` deleted, the sentence collapses to "an X and a Y are separable, so you can preserve one and change the other" — a generic, contentless truism about any two independent variables. It is FALSE/empty as stated without the domain nouns: the claim only bites because *register is exactly what current identifiers key on* and *force is exactly what pinning must preserve*. The specific coupling of these two named quantities is load-bearing. **Not a bridge** — it names an invariant (force ⟂ register) internal to the phenomenon, not a connection between two literatures.

---

## Step 2 — Archetype

**Primary archetype (consistent with digest N12): Empirical measurement study** — "we measure whether a presupposed capability survives an adversary."
**Secondary: Dataset/instrument** (GovSpan-Adv, CO1) built to enable the measurement, not as the center of gravity.

What this changes downstream:
- **(a) Abstract contribution slot:** the headline is a *measured robustness gap* (false-pin/miss-pin rates under adversarial vs. original phrasing, with a direction asymmetry), NOT a new method that beats a number. The dataset is the instrument, named second.
- **(b) Intro logic:** "what becomes possible / what we learn" — we make an *unexamined precondition of pinning* (that constraints can be identified at all) into a measurable, falsifiable quantity. The intro leads with the force⟂register asymmetry, then shows every prior literature assumes identification away (N4).
- **(c) Evidence standard:** pre-registered paired hypothesis tests with correction, hard binary thresholds, and a boundary-audit decomposition that separates identifier failure from contested ground truth. A negative result (identification IS robust) is publishable via the pre-committed fallbacks.

---

## Step 3 — Taste self-audit

- **Is the opportunity a Bridge?** Check: the framing is NOT "pinning and adversarial robustness were never connected." It is "pinning silently assumes an identification step; we test whether that step holds." PASS — the object is an internal invariant (Step 0), not a seam between fields.
- **Is the method mere Synthesis?** Check: GovSpan-Adv + five identifiers could look like "combine TensorTrust prompts with LMSYS chat." But the load-bearing act is the *validity-gated bidirectional rewrite* (M2) that isolates force from register — a construction no prior work performs. PASS.
- **Load-bearing verbs from integrate/unify/leverage family?** Check: draft verbs were "leverage existing corpora." REWRITE → the verbs are **isolate** (force from register), **measure** (two error directions), **decompose** (identifier failure vs. contested label). PASS after fix.
- **Abstract-opening rule:** the abstract opens with the mechanism/asymmetry ("binding force and surface register are separable"), uses verbs from the gate/formalize/isolate/measure family, and does NOT use "X is increasingly used… however… we introduce." PASS (see Abstract v0).

---

## Step 5 — Formal Problem Definition

**Estimand** (guidance.md §3.4 R1 — added at Phase A re-run, see `discussion/stage_review.md`): the robustness gap $\Delta = \text{err}(\text{adversarial}) - \text{err}(\text{original})$ in per-span governance-constraint identification error, measured separately for miss-pin and false-pin, per identifier family; unit of analysis = one constraint/non-constraint span pair (original phrasing paired with its validity-gated adversarial rewrite); reference population = governance-constraint and ordinary conversational spans plausible in LLM-agent deployments, approximated by TensorTrust defense prompts + agent-policy rules (constraint pool) and LMSYS-Chat-1M (non-constraint/filler pool); decision it feeds = whether current constraint-identification practice is reliable enough that memory-pinning's upstream precondition can be treated as solved, or must be scoped/pivoted per the fallback ladder below.

**Notation.** Let a context window be a sequence of spans $S = (s_1, \dots, s_n)$. Each span $s_i$ has a latent ground-truth label $y_i \in \{1 (\text{constraint}), 0 (\text{non-constraint})\}$. An identifier $f_\theta$ maps a span (optionally with context) to a pin decision $\hat{y}_i = f_\theta(s_i, \text{ctx}) \in \{0,1\}$ plus a confidence $c_i \in [0,1]$. A rewrite operator transforms a span while a validity gate $V$ certifies label preservation: $\text{Evade}(s \mid y{=}1)$ preserves $y{=}1$ but shifts register to casual; $\text{Spoof}(s \mid y{=}0)$ shifts register to imperative but preserves $y{=}0$.

**Load-bearing adjectives/verbs → definitions → measurement** (from digest Claims + N8 metrics):

| Adjective/verb | Formal definition | How measured |
|---|---|---|
| "reliable / robust" identification | robustness gap $\Delta = \text{err}(\text{adversarial}) - \text{err}(\text{original})$ per direction per identifier; robust ⟺ $\Delta$ not significantly $>0$ | McNemar exact test on paired decision flips (M4) |
| "miss-pin" (漏保率) | $\text{missrate} = \text{FN}/(\text{FN}+\text{TP})$ on true constraint spans = $1-\text{recall}$ | count on Evade condition |
| "false-pin" (错保率) | $\text{fprate} = \text{FP}/(\text{FP}+\text{TN})$ on non-constraint spans | count on Spoof condition |
| "disguised but still binding" (valid rewrite) | $V(\text{Evade}(s))=1$ ⟺ NLI back-check entails original obligation AND 2 annotators confirm | rejection rate + Cohen's κ (M2) |
| "dominant" failure direction | $\text{missrate}_{\text{adv}} - \text{fprate}_{\text{adv}}$, sign and CI | 10k-bootstrap CI (RQ_INF_1) |
| "contested" (ill-posed label, C4) | fraction of errors where blind re-annotators disagree with gold or split | M5 blind re-annotation, Wilson 95% CI |
| "localize" (Stage 2) | span-level F1 with IoU ≥ 0.5 overlap credit | M6 in-context evaluation |
| "adaptive degradation" | $\Delta_{\text{adaptive}} - \Delta_{\text{static}}$ for best identifier | paired bootstrap (RQ_INF_2) |

Every adjective in the Claims has either an equation or a decision procedure above; none is left rhetorical.

---

## Assumptions (A1..An)

> **Gates added at Phase A re-run** (guidance.md §3.2: "every A\* must fill... gate"; see `discussion/stage_review.md` item 5). PG-1/PG-2 run inside the Step 9 walking skeleton (both are needed just to trust the 60-pair skeleton result); PG-3–PG-6 are deferred to the phase named, because the skeleton's 2-arm, single-identifier design cannot itself exercise a family swap, a per-source split, a downstream-transfer check, or a full-n power calculation — deferring them is a design choice, not an oversight, and each is checked before the claim that depends on it is scored (goal.md §3 item 5).

- **A1 (rewrite validity, from t1/M2).** Evade preserves obligation and Spoof introduces none. *Fails if:* the validity gate passes rewrites that silently flip the true label. *Detected by:* the M2 dual gate (NLI entailment back-check + 2-annotator validation, κ reported) run BEFORE any identifier; pilot gate rejects the corpus if post-gate annotator κ < 0.7 on rewrite validity. *Gate:* **PG-1**, checked inside the Step 9 walking skeleton (the 60-pair skeleton corpus must itself pass this gate before its McNemar result is trusted).
- **A2 (label separability at construction, from C4/t5).** A majority of base spans have an uncontested constraint/non-constraint label. *Fails if:* base-corpus annotator κ < 0.7. *Detected by:* M1 annotation stage before rewriting; contested items routed to adjudication or dropped. *Gate:* **PG-2**, checked inside the Step 9 walking skeleton (the 30+30 base spans are drawn from the same annotated M1 pool).
- **A3 (attacker–defender independence, from t2).** The rewriter model family is disjoint from every identifier family. *Fails if:* measured Δ is an artifact of shared self-consistency. *Detected by:* cross-family ablation — swap rewriter family, re-measure Δ for the primary identifier; flag if Δ moves > 50% relative. *Gate:* deferred to **RQ1 scale-up (n=300)** — the walking skeleton runs a single identifier family and cannot exercise a family swap; the skeleton-passed criterion is provisional on this gate until the scale-up ablation runs.
- **A4 (source-pool representativeness, from t3).** TensorTrust defense prompts + agent policy rules + LMSYS-Chat-1M chat approximate deployment governance constraints well enough for direction-level conclusions. *Fails if:* per-source Δ diverges qualitatively. *Detected by:* results reported per-source; cross-source Δ consistency is the generalization check. *Gate:* deferred to **RQ_INF_2 scale-up** — the skeleton's 60-pair subset is not pre-registered to be per-source-balanced, so a per-source split is only meaningful at n=300.
- **A5 (identification is separable from downstream pinning, from t6).** A span-level identification score is a meaningful stage to measure in isolation. *Fails if:* identification score has no relation to end-to-end retention. *Detected by:* PrefEval transfer check (do Stage-1 identifiers flag PrefEval's implicit preferences as pin-worthy?). *Gate:* deferred to **post-RQ1 (Discussion/Limitations)** — the transfer check is a scope-bounding measurement, not a pass/fail gate on any H\*, and does not block scale-up.
- **A6 (statistical power).** n=300 pairs/direction detects an ~8pp paired shift at power ≈ 0.8. *Fails if:* true effect < 8pp. *Detected by:* the analysis plan pre-commits n and power; effect sizes with CIs reported regardless of significance. *Gate:* deferred to **RQ1/RQ_INF_1/RQ_INF_2 scale-up (n=300)** — the walking skeleton's n=60 is explicitly under-powered by design (Step 9 is a detectability check, not the powered test); per guidance.md §3.2 and Part 4 situation 5, **any cell below the n=300 pre-registered target (in particular the Stage-2 depth-stratified cells — early/middle/late thirds of ~100 transcripts — and any single-source subset under A4) is pre-declared INCONCLUSIVE, never scored as null or dropped**, and is reported as such alongside its point estimate and CI.

**Instrument validation (guidance.md §3.4 R2 — added at Phase A re-run).** Two constructs in this design are instruments in R2's sense (a taxonomy/label a human or model applies, not a raw physical measurement) and each gets the 5-step sequence before scale, not just a single κ number:
1. *M1's constraint/non-constraint label.* ① Categories grounded in two external sources already named in N6/M1 — real TensorTrust defense-prompt rules and real agent policy/system-prompt rules (not invented examples). ② Draft wide on a held-out calibration slice of ~50 pairs, with named merge/split/remove operations logged if any span type proves systematically ambiguous. ③ Validate against 2 independent annotators, κ ≥ 0.7 required (already stated in M1). ④ Inspect the confusion structure: disagreements must cluster on boundary-adjacent cases (formal-register chit-chat, soft suggestions), not collapse across the whole label; this inspection is what M5's boundary/ambiguity audit reuses at scale. ⑤ Freeze the label schema (hash it) before any rewriting begins.
2. *M2's validity gate $V$ (NLI entailment back-check + 2-annotator confirmation).* ① Grounded in the formal definition of validity in Step 5 ("disguised but still binding"). ② Draft-wide on a held-out set of ~30 candidate rewrites, logging the expected 20–30% rejection rate as the calibration outcome, not an incidental byproduct. ③ Validate the NLI back-check against the same 2 annotators, κ ≥ 0.7 required on the gate's own accept/reject decision (distinct from A1's κ on the rewrite's *label*). ④ Inspect confusion structure of gate disagreements (annotator-vs-NLI splits should cluster on genuinely borderline obligation strength, not a systematic NLI bias toward one direction). ⑤ Freeze the gate's prompt/threshold before any identifier (M3) is run.
Both thresholds (κ ≥ 0.7) are acceptance criteria in R2's sense: falling short routes to guidance.md Part 4 situation 7 (refine categories, re-validate, or — if the property is genuinely ill-posed — redirect toward the C4/M5 contested-label finding), not to scaling on an unvalidated instrument.

---

## Step 6 — Pre-Registered Experiments

### RQ1 (digest N8, seed-given central question)
*Is identification reliable under adversarial phrasing that disguises constraints as chit-chat and chit-chat as constraints?*
- **Assumption:** A1, A2, A3, A6.
- **Hypothesis (binary):** For the pre-registered primary identifier LLM-as-judge (M3c), the Holm-corrected McNemar test on paired original-vs-adversarial decisions is significant (p < 0.05) with adversarial error rate higher, AND the mean robustness gap $\bar\Delta \geq 0.10$ (≥10 percentage points) across the five identifier families. Non-primary identifiers reported as confirmatory.
- **Metric:** miss-pin rate, false-pin rate, $\Delta$ per direction per identifier (M4).
- **Verification:** McNemar exact test, one per identifier × direction (10 tests), α=0.05 Holm–Bonferroni; discordant-pair odds ratios + 95% CIs. Primary hypothesis = M3c; others exploratory.
- **Fallback:** IF M3c shows no significant gap OR $\bar\Delta < 0.10$: pivot claim to "current identification is *more robust to register disguise than to structural forgery* — we quantify the surprisingly small semantic-register attack surface and localize residual fragility to identifier family M3a (surface-cue heuristic)." Publishable as a robustness-audit negative result.

### RQ_INF_1 (digest N8, inferred — direction asymmetry + C4 decomposition)
*Which failure mode dominates, and how much fragility is contested ground truth?*
- **Assumption:** A1, A2, A3.
- **Hypothesis (binary):** Under adversarial phrasing, the 10k-bootstrap 95% CI on $(\text{missrate}_{\text{adv}} - \text{fprate}_{\text{adv}})$ lies strictly above 0 (miss-pin dominates), AND the M5 contested-label fraction has Wilson 95% CI upper bound < 0.50 (fragility is majority genuine identifier failure).
- **Metric:** miss-pin − false-pin rate difference; contested-label fraction (M5).
- **Verification:** 10k-resample bootstrap CI on the rate difference; Wilson 95% CI on contested fraction from blind re-annotation of all errors + matched correct sample.
- **Fallback:** IF the CI includes 0 or is negative: claim "spoofing (false-pin / authority laundering) is at least as dangerous as evasion," re-centering the threat model. IF contested fraction ≥ 0.50: claim "adversarial 'fragility' is majority a ground-truth well-posedness problem (C4) — 'perfect identification' is ill-posed; we deliver the contested-case taxonomy (CO3) as the primary contribution."

### RQ_INF_2 (digest N8, inferred — Stage-2 localization + adaptive attack)
*Does identification degrade further under in-context localization and an adaptive attacker?*
- **Assumption:** A1, A3, A4, A6.
- **Hypothesis (binary):** In-context miss-pin rate exceeds isolated-pair miss-pin rate with paired-bootstrap 95% CI strictly above 0, AND $\Delta_{\text{adaptive}} > \Delta_{\text{static}}$ with paired-bootstrap 95% CI above 0 for the best Stage-1 identifier.
- **Metric:** span-level F1 (IoU ≥ 0.5), depth-stratified miss-pin; adaptive-Δ vs. static-Δ.
- **Verification:** paired bootstrap on (in-context − isolated) miss-pin and on (adaptive − static) Δ; depth-stratified reporting (early/middle/late thirds).
- **Fallback:** IF in-context miss-pin is indistinguishable from isolated OR adaptive Δ ≤ static Δ: claim "the cheap isolated-pair pilot already upper-bounds deployed risk — a positive methodological finding that Stage-1 measurement suffices," reducing future evaluation cost.

### Mandatory baselines
- **B0 "why do this at all" control — the trivial/no-mechanism arm:** the **keyword/deontic-cue heuristic (M3a)** run on *original (non-adversarial)* phrasing. This is the "no adversary, surface cues only" arm. If M3a already fails on original phrasing (high error with no attack), the problem is trivially motivated (identification is hard even benignly); if M3a succeeds on original but collapses on adversarial, it justifies studying the adversarial gap specifically. Establishes that the problem exists and is non-vacuous.
- **B-alt strongest-alternative-explanation control — capability/budget-matched:** the **cross-family rewriter ablation (A3/t2)** plus a **length-and-topic-matched non-constraint control**. *Rival explanation:* "the measured Δ is not register-disguise fragility but (i) attacker–defender family self-consistency, or (ii) mere distribution shift / spurious length-topic cues from the rewrite." B-alt isolates the claimed cause by (i) swapping the rewriter to a disjoint family and re-measuring Δ, and (ii) matching non-constraint spans to constraint spans on token length (±20%) and embedding-cluster topic so the identifier cannot exploit surface statistics.
  - **Corpus-validity verification for (ii)** (added at Phase A re-run — this check was already required in `discussion/stage_review.md`'s Stage 4 fix to `paper_draft.md`, backported here so the pre-registration and the draft agree, per goal.md's stale-claim discipline): before any identifier is run, the length/topic matching construction is itself verified, not merely asserted — a two-sample Kolmogorov–Smirnov test on the token-length distributions of the matched constraint and non-constraint pools, and a two-sample test on the cosine-similarity distribution of their topic embeddings, both against a pre-registered non-significance threshold (α = 0.05, no significant residual gap). This is reported as a corpus-validity statistic alongside annotation κ, analogous in role.
  - **Pre-committed downgrade wording (guidance.md §3.3 item 2 — added at Phase A re-run; this was the missing half of B-alt's pre-registration):** *If Δ survives both checks* (family swap AND the KS/cosine matching-validity test), register-disguise is the isolated cause and Claims 1–4 (the RQ1/RQ_INF_1/RQ_INF_2 claims in the Claim–Evidence Map) hold at full strength. *If Δ does not survive the family-swap check* (moves > 50% relative per A3): downgrade to "the measured gap reflects attacker–defender family self-consistency, not register-disguise fragility per se — the phenomenon of degraded identification under paraphrase stands, but the mechanism claim (force/register decoupling specifically) is unsupported; only the cross-family-robust residual, if any, is reported as the register-disguise finding." *If the KS/cosine test finds a significant residual length/topic gap* (matching failed): downgrade to "the measured Δ is confounded with surface-statistic exploitation and cannot be attributed to register-disguise without re-matching the corpus; Claims 1–2 are reported as unsupported pending a re-matched corpus, not as refuted." Per guidance.md §3.3, this downgrade is scored **per-claim**, not per-paper: a family-coupling failure does not by itself invalidate RQ_INF_2's localization/adaptive-attack finding, which is independent of B-alt's isolated-cause claim.

### Global fallback F-G1
If the entire central hypothesis family (RQ1 + RQ_INF_1) fails — identification is adversarially robust and no direction dominates — pivot archetype from *empirical fragility measurement* to *dataset/benchmark + positive robustness certificate*.
**Pivoted abstract (one sentence):** "We release GovSpan-Adv, a validity-gated bidirectional-rewrite benchmark for governance-constraint identification, and report the counterintuitive finding that current LLM-judge identifiers are robust to semantic register disguise — bounding the register attack surface and redirecting defensive effort toward structural forgery and downstream pinning."

---

## Step 9 — Walking Skeleton

**One binary question:** *Does validated register disguise move LLM-judge identification error at all?* (the atomic core of RQ1).

- **Arms (2):** (1) M3c LLM-as-judge on **original** phrasing; (2) same identifier on **Evade+Spoof adversarial** phrasing of the *same items*.
- **Smallest task set:** 30 constraint + 30 non-constraint base spans (subset of M1), each with one validated Evade/Spoof rewrite passing the M2 gate. 120 decisions total.
- **Deterministic metrics only:** miss-pin rate, false-pin rate, and paired McNemar on the 60 paired items. No annotation-audit, no depth stratification, no adaptive round.
- **Expected wall-clock/cost:** ~1 day; < $20 API (60 rewrites + 60 validations + 120 judge calls); no GPU (skip DeBERTa fine-tune at skeleton stage).
- **Skeleton-passed criterion:** McNemar p < 0.05 with adversarial error higher on this 60-pair subset → the effect is real and detectable; **scaling to n=300, five identifiers, two stages is a config change (loop bounds + identifier list + transcript embedding), not a code change.** If p ≥ 0.05 at n=60 but effect direction is correct, scaling to n=300 is justified by A6's power calc; if effect direction is *reversed*, trigger F-G1 before spending on full scale.

---

## Claim–Evidence Map

| Claim (final abstract) | Traces to | Status |
|---|---|---|
| Force and register are separable (asymmetry) | Step 0 / C1 / M2 definition | supported-by-design (construction of M2 operationalizes it) |
| Adversarial register disguise degrades identification (Δ ≥ 0.10) | H-RQ1 | needs-experiment; fallback-covered (RQ1 fallback) |
| Miss-pin dominates false-pin | H-RQ_INF_1 (direction) | needs-experiment; fallback-covered |
| A minority of fragility is contested ground truth (< 50%) | H-RQ_INF_1 (contested), Step 5 "contested" | needs-experiment; fallback-covered |
| Isolated pilot underestimates deployed risk | H-RQ_INF_2 | needs-experiment; fallback-covered |
| GovSpan-Adv is a validity-gated paired instrument | A1/M2, Step 5 "valid rewrite" def | supported-by-design |
| Register-disguise is the isolated cause (not family coupling / surface stats) | B-alt, A3 | needs-experiment |

Every claim traces to an H-id or a Step-5 definition.

---

## Abstract v0 (draft, mechanism-first) — DRAFT BEFORE RESULTS

A governance constraint's binding force and its surface register are separable: a paraphrase can flatten an imperative rule into casual chit-chat while keeping the obligation, or inflate idle talk into authoritative-sounding text carrying no obligation. Memory-pinning for LLM agents silently assumes the upstream step — deciding which spans are the rules — is reliable, yet that step keys on exactly the register an adversary can move. We isolate force from register with GovSpan-Adv, a paired corpus of constraint and length-/topic-matched non-constraint spans (from real TensorTrust defense prompts and LMSYS-Chat-1M logs) carrying validity-gated bidirectional adversarial rewrites, and measure five identifier families' miss-pin (漏保率) and false-pin (错保率) rates under adversarial versus original phrasing, in isolation and embedded in long transcripts. We report the robustness gap, its direction asymmetry, and a blind boundary audit separating identifier failure from contested ground truth. *(Draft — study not yet run.)*

<!-- word count ~150 -->
