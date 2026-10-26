# Discussion — B3.3 静默变更率 / "Undocumented by Design? Measuring Silent Behavioral Change against Vendor Changelogs"

> Auto-research-discussion document (6 stages, each with an internal critic→refine pass).
> Status: **KEEP-TOP**, external-audit cluster. Target: **ICLR 2027** (abstract **Sep 18, 2026**, paper **Sep 25, 2026** — TIGHT; see Stage 6).
> Sources: `README.md` (seed, [GIVEN]), `digest.md` (reverse digest, C1–C4 / M1–M5 / CO1–CO3 / RQ1–RQ3 ids reused here), `paper.md` (pre-registered spec), `discussion/` (July working folder: `discussion_trace.md`, `experiment_design.md`, `paper_draft.tex`).
> Tag conventions: **[VERIFY]** = channel-relayed or unconfirmed claim, must be independently verified before appearing in any submitted text; **[GIVEN]** = from the seed README.

---

## Stage 1 — Problem definition (precise estimand)

**Core question [GIVEN]:** Of the behavioral changes that can be measured empirically across versions of a deployed LLM API, what fraction never appears in the vendor's changelog? In which behavioral categories do silent changes concentrate?

**Estimand (v1).** For a version transition `t → t+1` of a target system, with a fixed, pre-registered probe suite `P` (categories `𝒞`: factual QA, refusal/safety, instruction-following/formatting, reasoning/math, tool-calling, latency/cost) and the vendor's disclosure text `L_{t→t+1}` parsed into claim set `𝒦`:

- A probe `p` shows a **detected diff** (`D(p)=1`) iff a two-sample distance between the N-sample response sets at `t` and `t+1` exceeds the same-version resampling null (permutation p-value < α, Holm-corrected across probes) **and** passes an effect-size floor (|Cliff's δ| ≥ 0.33).
- A detected diff is **documented** (`Doc(p)=1`) iff some claim `k ∈ 𝒦` entails it at score ≥ τ (τ calibrated on human labels); otherwise **silent**.
- **Undocumented-change rate:** `ρ = Σ_p Silent(p) / Σ_p D(p)`, reported overall and per category `ρ_c`, with bootstrap CIs.

This is an **accountability metric**, not a change-detection metric: the unit of measurement is the *gap between measured behavior change and the vendor's own record of it*. It requires two arms that no prior work combines — a **longitudinal probe arm** (behavioral diffing) and a **changelog-parsing arm** (claim extraction + entailment alignment).

**Critic:**
1. `ρ` as stated is not one number — it is a function `ρ(P, α, δ-floor, τ)` of the probe suite and three analyst-chosen thresholds. Two labs with different suites would report different "silent-change rates" for the same transition; the estimand must own this conditionality explicitly or it will be attacked as unfalsifiable.
2. The denominator choice (detected diffs) makes `ρ` undefined when no diffs are detected, and unstable when few are. What is reported for a transition with 3 detected diffs?
3. "Documented" is doing enormous work. Vendors write blanket entries ("improved model quality and safety"). Under a lenient entailment threshold, one vague sentence documents *everything* and `ρ ≈ 0` by construction; under a strict one, almost nothing is documented and `ρ ≈ 1` by construction. A single τ hides a whole spectrum.
4. Ground-truth incompleteness (digest C3): with no independent list of "all actual changes," `ρ` is only partially identified. The direction of the bound must be stated correctly: `ρ` is the silent fraction *among diffs the suite can see*, which is neither an upper nor a lower bound on the true silent fraction unless a coverage assumption is stated.
5. Per-probe counting overweights categories with many probes; correlated probes (same benchmark, near-duplicate prompts) violate the independence the bootstrap assumes.

**Refined:**
- **Estimand (v2, pre-registered):** `ρ_c(T; P, θ)` — for transition `T`, probe suite `P` (frozen and versioned before any post-`t+1` measurement), and a *pre-registered analysis configuration* `θ = (α=0.05 Holm, |δ|≥0.33, τ ∈ {τ_strict, τ_lenient})`. **Headline result is reported as a strict/lenient interval, never a point:** documentation is scored on a 3-level specificity scale — **S2 specific** (claim names the behavior or category), **S1 vague/blanket** (claim could cover it only under generous reading), **S0 absent**. `ρ_strict` counts only S2 as documented; `ρ_lenient` counts S1∨S2. The gap `ρ_strict − ρ_lenient` is itself a finding (how much disclosure is blanket boilerplate).
- **Denominator:** report `(Σ D(p), ρ)` jointly; transitions with `Σ D(p) < 10` are reported descriptively (diff list + labels) and excluded from pooled rates. Also report the unconditional companion `σ = Σ Silent(p) / |P|` (silent diffs per probe), which is defined for every transition.
- **Identification statement (verbatim in the paper):** `ρ` estimates the silent fraction *of suite-visible changes*; it says nothing about invisible changes. The claim defended is "at least this much measured change went undisclosed," a well-defined lower bound on the *count* (not the rate) of undisclosed changes.
- **Correlation:** cluster bootstrap at the probe-family level (probes sharing a template/benchmark = one cluster); category rates weighted by pre-registered category weights, not raw probe counts.

---

## Stage 2 — Motivation (why now, binding constraint)

**Why now.**
1. **Incident pressure.** Channel-relayed motivating incidents: (a) Llama 4's LMArena entry reportedly dropped from **#2 to #32 upon retest** after the arena variant was found to differ from the released model **[VERIFY — channel-relayed; the publicly reported version is that Meta submitted an experimental chat-tuned variant to LMArena distinct from the released weights; confirm details and final rank against LMArena's own statement before citing]**; (b) reports of **undisclosed tier-dependent behavior changes** (same model alias behaving differently across account tiers / load conditions) **[VERIFY — channel-relayed, no citable source yet; if unverifiable by submission, drop or replace with documented incidents]**. Both are instances of the same structural fact: the party that controls the change is the sole author of the record of the change (`paper.md` Step 0 asymmetry).
2. **Regulatory pull.** EU AI Act GPAI obligations and the technical-AI-governance literature ([TAIG, OpenReview:Be2B6f0ps1]) demand *ongoing monitoring* and post-market documentation; no instrument currently measures whether vendor disclosure keeps pace with actual behavioral change.
3. **The field just built the ingredients.** 2024–2026 produced API change-detection (logprob tracking, arXiv:2512.03816), model-equality testing (arXiv:2506.06975), substitution audits (arXiv:2504.04715), and fingerprint-spoofing attacks (arXiv:2606.16100) — everyone can now detect *that* something changed; nobody has measured *what fraction of change is disclosed*. The niche is open and will not stay open long.

**Binding constraint being attacked:** downstream integrators, auditors, and regulators currently have to *trust changelogs as complete records*, and there is no published number for how incomplete they are. Vendors will structurally never produce this number themselves [GIVEN: "结论直接服务问责，厂商结构性不会自己做"].

**Critic:**
1. Both headline incidents are unverified relays. The Llama 4/LMArena case is arguably a *disclosed-after-the-fact* discrepancy (Meta acknowledged the experimental variant), which makes it an awkward poster child for *silent* change — a careful reviewer will notice.
2. "Regulation demands it" is a weak motivation if no regulator is named as a consumer of `ρ`; the paper needs a concrete user story.
3. "Why now" must also answer "why is this a *measurement* paper and not a blog post": the motivation should lean on the estimand's non-obviousness (partial identification, instrument calibration), not just on outrage.

**Refined:**
- Use the incidents only as *illustrations of the asymmetry*, each with a verified citation or not at all; the Llama 4 case is reframed honestly: "even when a discrepancy is eventually disclosed, disclosure was reactive, externally forced, and absent from any changelog — the record was corrected only because an external measurement existed" **[VERIFY the sequence of events before using even this framing]**. The tier-dependent claim is used only if a citable source (news report, vendor admission, published measurement) is found; otherwise cut.
- Concrete user stories, one per audience: (i) an enterprise integrator deciding whether a regression in production traces to a vendor update; (ii) a safety auditor asking whether refusal-behavior changes are disclosed at the same rate as capability changes; (iii) a standards body (e.g., post-market monitoring under the AI Act) needing a measurable definition of "documentation fidelity." The paper's deliverable for all three is the same instrument + number.
- The motivation paragraph closes on the methodological claim: turning "changelogs are incomplete" from an anecdote into a **calibrated, partially-identified, reproducible estimate** is the contribution; that is what makes it ICLR material rather than journalism.

---

## Stage 3 — Related work (positioning + boundary statements)

**Nearest published prior (from the Aug-2026 sweep) and the boundary against each:**

1. **arXiv:2504.04715 — model-substitution auditing** (are you getting the model you pay for; concludes verification is hard black-box and points to TEEs). *Boundary:* answers "is the served model the one promised?" — a **binary identity** question, with a trust-anchor (TEE) recommendation. B3.3 answers "of the changes that occur, what fraction is disclosed?" — a **rate over disclosure**, requiring a changelog-parsing arm 2504.04715 does not have. We inherit its threat model (vendors can misrepresent) as motivation, not its method.
2. **arXiv:2512.03816 — logprob tracking of API changes** (cheap continuous change detection on deployed endpoints; corpus twin [LogProbTracking, OpenReview:hFxivbAgVP]). *Boundary:* produces a **change signal** with no behavior-category attribution and no alignment to disclosure text; it cannot label any change documented or silent. We reuse it as (a) the boundary-detection component of our version-pair acquisition (M2) and (b) the change-detection-only baseline. **[VERIFY on the full text: confirm 2512.03816 does not itself compare detected changes to vendor announcements; if it does even informally, our delta narrows to the calibrated entailment arm + category taxonomy + the ρ estimand, and the related-work text must say so.]**
3. **arXiv:2506.06975 — rank-based uniformity test** (model-equality testing vs a trusted reference; corpus twin [RankUniformity, OpenReview:PSIe9mmF7a]). *Boundary:* requires a trusted local reference distribution and answers same/different; no disclosure arm, no taxonomy. Used as a secondary detector for open-weight pairs where a reference exists.
4. **arXiv:2606.16100 — fingerprint spoofing** (a vendor aware of fingerprint-based audits can spoof them). *Boundary:* an **attack on the detection arm**, not a competing measurement. It justifies two of our design choices: (i) broad *behavioral* probe batteries are harder to spoof than narrow statistical fingerprints; (ii) our headline claims rest on transitions where change is not adversarially concealed (open-weight pairs, publicly dated snapshots). We explicitly scope out the fully adversarial vendor and cite 2606.16100 as the reason the adversarial version of this audit is a separate problem.
5. **Chen, Zaharia & Zou 2023 (arXiv:2307.09009)** — the canonical two-snapshot drift study. *Boundary:* demonstrates drift exists; never cross-references OpenAI's changelog, computes no documented/silent rate, no instrument calibration. B3.3 is "Chen et al. with a disclosure arm, a null-calibrated detector, and an accountability estimand."
6. **Corpus support (from digest N3):** [FairBetting, OpenReview:EEVpt3dJQj] (anytime-valid sequential tests — reused statistical machinery for the prospective arm), [RobustAudit, OpenReview:AiaVCVDuxF] (audit-facing vs user-facing serving — threat model), [SafeHarbor, OpenReview:dLojMSgSFW] (legal exposure of ToS-constrained probing — limitations section), [TAIG, OpenReview:Be2B6f0ps1] (governance demand), [LAMDA, OpenReview:1FnCrZtBNQ] (longitudinal-measurement hygiene).
7. **SE literature on release-note/changelog quality** (mining studies of changelog completeness in traditional software, e.g., work on automatic release-note generation and what fraction of code changes surface in notes) — the closest *conceptual* precedent for "documentation fidelity as a measurable quantity." **[VERIFY — I believe such studies exist (e.g., ARENA release-note generation, Moreno et al.; changelog mining work); a targeted search is required before naming them in the paper.]**

**Critic:**
1. The list is detector-heavy; the *entailment/alignment* side has its own literature (NLI for claim verification, specification-mining, compliance checking of documentation vs behavior) that is currently unrepresented — a reviewer from the NLP side will ask what alignment method we build on.
2. Item 2's [VERIFY] is the single biggest novelty risk in the paper and is buried mid-list. It should be a named action item with an owner and a date, not a footnote.
3. "We scope out the adversarial vendor" needs one more sentence of justification or reviewers will call the whole audit defeatable-by-design.

**Refined:**
- Add an alignment-methods paragraph: changelog claims → diff alignment is instantiated as NLI/entailment scoring (off-the-shelf NLI model or LLM-judge with human calibration), positioned against claim-verification / fact-checking pipelines **[VERIFY exact citations at writing time]**; the novelty claimed is the estimand and calibration protocol, *not* a new NLI method — stated explicitly to deflect "the matcher is off-the-shelf" as a criticism.
- **Action item (blocking, week 1):** full-text read of arXiv:2512.03816 and arXiv:2504.04715 for any documented-vs-announced analysis; update the delta statement in `related work` and the novelty claim in the abstract accordingly. Owner: paper lead. Due before the pilot go/no-go.
- Adversarial scoping sentence: "A vendor that actively conceals change from auditors defeats any black-box audit (2606.16100); our estimand is meaningful for the *non-adversarial but under-documenting* vendor, which the incident record suggests is the common case — and a measured non-adversarial ρ is the prerequisite for arguing the adversarial case matters."

---

## Stage 4 — Sub-problems (each with the hard part named)

**SP1 — Genuine diff vs stochasticity (detector calibration).** Build a two-sample detector over N-sample response sets whose false-positive rate on *same-version* pairs is empirically ≤ α. **Hard part:** API nondeterminism is not iid noise — load-dependent routing, batching effects, and infra changes (tokenizer, sampling kernel) shift distributions *within* a "version"; the null must be estimated from same-version resamples spread across days/loads, or infra noise is miscounted as behavioral change (silent-rate inflation).

**SP2 — Changelog claim extraction + entailment alignment.** Parse unstructured release notes into discrete claims; score claim-vs-diff entailment; calibrate against human labels. **Hard part:** the mapping is many-to-many at wildly variable granularity ("safety improvements" vs "fixed over-refusal on medical dosage questions"); the strict/lenient specificity scale (Stage 1) must be *reliably annotatable* — if human κ < 0.6 on S0/S1/S2, the headline metric has no floor to stand on.

**SP3 — Version-pair acquisition.** Assemble transitions where (a) both endpoints are queryable and (b) a disclosure text exists. **Hard part:** the ideal object (the same API alias before/after a silent update) is *ephemeral* — you cannot re-query the past. Every acquisition strategy trades off realism vs availability: open-weight pairs are perfectly re-queryable but their "changelog" is a model card; concurrently-served dated API snapshots are realistic but the vendor chose to date them (biasing toward *more* documented transitions); prospective alias monitoring is unbiased but cannot be scheduled — vendors ship on their own clock, which collides with our deadline (Stage 6).

**SP4 — Uncertainty for a partially-identified estimand.** Report `ρ` with honest uncertainty: cluster bootstrap over probe families, sensitivity analysis over (α, δ-floor, τ), and the strict/lenient interval. **Hard part:** the largest uncertainty term — probe-suite coverage — is not statistical and cannot be bootstrapped; the paper must make the conditional nature of `ρ` impossible to misquote (press will want "X% of changes are secret"; the instrument only supports "X% of *detected* changes were undisclosed").

**SP5 — Attribution to a release window.** Pin each detected diff to a specific transition so it can be aligned to the right changelog entries. **Hard part:** rolling deploys and A/B routing mean the "boundary" can be a mixture state lasting days; logprob-fingerprint discontinuity detection (M2, following 2512.03816) gives boundaries only up to fingerprint sensitivity — and 2606.16100 shows fingerprints are the weakest link.

**Critic:**
1. SP3 is the schedule-critical sub-problem and the only one with a calendar dependency; it should be ranked first for de-risking, not third.
2. SP1's "spread same-version resamples across days" quietly assumes no silent update happens *during* the null-estimation window — circular. Needs an explicit guard.
3. Five sub-problems, but SP5 is arguably a sub-case of SP3 for the prospective arm only; for the retrospective arms (open-weight, dated snapshots) attribution is trivial. Collapsing would sharpen the doc.

**Refined:**
- Re-rank: **SP3 (acquisition) is sub-problem #1** and drives the experiment design; its retrospective arms are executable immediately (no calendar risk) and the prospective arm is a bonus case study (Stage 6).
- SP1 guard: the null window is itself monitored with the fingerprint tracker; any fingerprint discontinuity inside a null window voids that window's resamples. Same-version null pairs are drawn only from fingerprint-stable stretches.
- SP5 is folded into SP3 as "SP3b: boundary attribution for the prospective arm," leaving four top-level sub-problems (SP1 detector calibration, SP2 alignment + annotation reliability, SP3 acquisition incl. attribution, SP4 partial-identification honesty).

---

## Stage 5 — Methods (concrete design)

**M1 — Probe suite construction.**
- ~1,200–1,500 probes across 6 categories, each probe = (prompt, decoding config, response-feature extractor). Sources: stratified draws from MMLU, GSM8K, TruthfulQA (factual/reasoning); XSTest + HarmBench subsets (refusal/over-refusal); IFEval (instruction/formatting); BFCL (tool-calling); plus ~200 hand-written probes targeting behaviors changelogs actually talk about (persona/tone, formatting defaults, refusal templates, JSON-mode strictness) — mined from the changelog corpus itself so the suite has *coverage of the disclosed-change vocabulary* (this is what lets `ρ_strict < 1` be attainable).
- Per probe: N = 25–50 samples per version at the version's default decoding; response features: exact answer, refusal flag (classifier), format-compliance flags, response length, first-token top-k logprobs where the API returns them.
- Frozen + hashed before any `t+1` measurement (pre-registration artifact).

**M2 — Version-pair acquisition (three arms).**
- **Arm R-OW (retrospective, open-weight):** 6–8 transitions with both endpoints downloadable and a vendor disclosure text (release blog + model card), e.g., Llama-3.1→3.3, Qwen-2.5→Qwen-3, DeepSeek-V3→V3.1, Mistral versioned releases, Gemma-2→3 **[VERIFY each pair's disclosure text exists and is dated before locking the list]**. Served locally (vLLM), so sampling is fully controlled and re-queryable. This arm has *perfect availability* and anchors the paper.
- **Arm R-API (retrospective, dated API snapshots):** 4–6 pairs of concurrently-served dated snapshots from ≥2 vendors (e.g., successive dated GPT / Claude / Gemini snapshots still queryable today **[VERIFY current availability and deprecation dates immediately — snapshots get retired]**), aligned to the vendor's release notes for the inter-snapshot window. Selection-bias caveat (vendor chose to date these) reported explicitly.
- **Arm P (prospective, alias monitoring):** daily fingerprint + weekly mini-suite (150 probes) against floating aliases (`-latest` style) of 2–3 vendors, started immediately; any boundary caught before the paper freeze becomes a case study. Uses anytime-valid sequential tests [FairBetting] so continuous monitoring doesn't inflate error.
- **SP3b attribution:** for Arm P, a diff is attributed to a window only if bracketed by fingerprint-stable stretches; otherwise reported as "boundary-uncertain" and excluded from ρ.

**M3 — Changelog corpus.** Scrape + archive (with Wayback snapshots for historical states) the release notes / changelogs / model cards / release blog posts of the target vendors; segment into dated claim units; annotate each claim's category and specificity (S1/S2). Corpus released as an artifact (it does not currently exist as a dataset anywhere — a secondary contribution).

**M4 — Alignment.** For each detected diff, a structured "diff card" (category, direction, effect size, example pairs) is matched against all claims in the transition window by an NLI/LLM-judge entailment scorer; τ_strict / τ_lenient calibrated on a 250-pair human-labeled dev set (2 annotators + adjudication; report κ and matcher F1 ≥ 0.7 target). Baseline: keyword/BM25 matcher (expected weak — quantifies how non-trivial alignment is).

**M5 — Metric + uncertainty.** `ρ_strict, ρ_lenient` overall and per category, per transition and pooled (transitions as random effects); cluster bootstrap (probe-family clusters) for CIs; sensitivity grid over (α ∈ {0.01, 0.05}, |δ| ∈ {0.2, 0.33, 0.5}, τ ± calibration band); detector FPR measured on same-version null pairs and reported next to every headline number.

**Critic:**
1. Arm R-OW's disclosure texts (model cards, blog posts) are a *different genre* from API changelogs — richer, marketing-flavored. Pooling `ρ` across R-OW and R-API mixes two disclosure regimes and muddies the headline.
2. N = 25–50 samples per probe per version × ~1,400 probes × ~20 endpoints is ~1.4–2.8M generations — the open-weight side is fine, but the API side at ~10–12 snapshot endpoints × 1,400 × 50 ≈ 0.7–0.85M calls could run $3–8K and hit rate limits; no budget cap was stated.
3. Hand-written probes mined from changelog vocabulary create a subtle bias: the suite is better at detecting *the kinds of things vendors disclose*, deflating ρ. The refined estimand should acknowledge suite-construction direction.
4. ToS risk (SafeHarbor): systematic probing + publishing vendor-named silent-change rates has legal exposure; unhandled.

**Refined:**
- **Never pool across arms.** Report `ρ` per arm (R-OW, R-API, P) as three disclosure regimes; the cross-regime comparison ("are API changelogs sparser than open-weight release notes?") is promoted to a named secondary finding rather than a nuisance.
- **Budget caps:** API arm capped at $4K: probes drop to N=25 samples for the API arm (power analysis on pilot data decides if 25 suffices; latency/cost category uses all calls anyway), and R-API pairs capped at 4 if needed. Open-weight arm sized to available GPUs (Stage 6).
- **Suite-direction statement:** the changelog-mined probes *raise* the detector's chance of confirming documented changes, making `ρ` conservative (biased *downward*) — the right direction for an accountability claim ("even with a suite built to find what vendors talk about, X% of detected change was undisclosed"). Stated as a design feature.
- **ToS/legal:** rate-limited polite probing, no scraping beyond public pages, findings reported at vendor-aggregate + per-category level with per-vendor detail in an appendix; cite SafeHarbor as the policy context. Legal-review pass before de-anonymized release.

---

## Stage 6 — Experiment design (arms, scale, compute, go/no-go, milestones)

**Experimental arms (maps to M2):**
| Arm | Content | Role |
|---|---|---|
| A0 Null-calibration | same-version pairs, all endpoints (fingerprint-stable windows) | detector FPR; gates everything |
| A1 R-OW | 6–8 open-weight transitions × full suite | headline ρ, fully reproducible |
| A2 R-API | 4–6 dated-snapshot pairs × suite (N=25) | realism; API-changelog regime |
| A3 P | daily fingerprints + weekly mini-suite on live aliases | case study if a boundary lands |
| A4 Alignment eval | 250-pair human-labeled set; NLI vs keyword baseline | matcher F1, κ, τ calibration |

**Scale & compute.**
- Open-weight: ~14 endpoints (7 transitions × 2) × 1,400 probes × 50 samples ≈ 1.0M generations, short outputs (≤512 tok) ⇒ ~0.5B generated tokens. On vLLM: 8B-class models trivial; 70B-class needs 4×A100/H100 nodes; estimate **600–900 A100-hours total** (dominated by 2–3 large pairs). Feasible on one 8-GPU node in ~1.5–2 weeks of wall clock, batched.
- API: ≤ $4K (Stage 5 cap). Annotation: ~60–80 annotator-hours (alignment dev set + specificity labels + adjudication).
- Storage/artifacts: raw responses + fingerprints + changelog corpus frozen and released (~tens of GB).

**Pilot (go/no-go).** By **Aug 25, 2026**: 1 open-weight transition (e.g., Qwen-2.5→3, 8B scale) + 1 API snapshot pair, 300-probe mini-suite, N=25.
**GO criteria:** (i) A0 FPR ≤ 1.5×α on ≥ 200 null probe pairs; (ii) ≥ 15 detected diffs across the two transitions (else the detector/effect-floor is mistuned or transitions are too quiet — retune once, else NO-GO); (iii) two annotators reach κ ≥ 0.6 on documented/silent with the S0–S2 scale on ≥ 50 diff–claim pairs. **NO-GO fallback:** descope to a measurement-instrument paper (detector + corpus + calibration, ρ on open-weight arm only) for a workshop, and retarget the full study.

**Milestone plan (working back from Sep 18 abstract / Sep 25 paper):**
- **Aug 13–17:** freeze probe suite v1; scrape changelog corpus; verify snapshot availability + open-weight pair disclosure texts; full-text novelty check on 2512.03816 / 2504.04715 (Stage 3 action item); start Arm P monitoring + A0 null logging (calendar-critical: nulls need multi-day spread).
- **Aug 18–25:** pilot; annotate pilot alignment set; **Aug 25 go/no-go**.
- **Aug 26–Sep 8:** full A1 + A2 runs; A4 annotation in parallel; corpus specificity labeling.
- **Sep 8–15:** analysis (ρ per arm, sensitivity grid, taxonomy), figures, draft (reuse `discussion/paper_draft.tex` skeleton).
- **Sep 16–18:** abstract + intro freeze; **Sep 18 abstract deadline**. Sep 19–25: full paper polish; **Sep 25 paper deadline**.

**Timeline verdict: feasible, but only in the descoped form.** The *retrospective* design (A1 + A2 headline, A0/A4 calibration) fits the 5 weeks with ~1 week of slack, contingent on immediate GPU access and the Aug 25 gate. The *prospective* arm cannot be guaranteed — vendors ship on their own clock; it is pre-declared as a case-study bonus, and its absence does not block submission. **Explicit infeasibility flag:** if the pilot gate slips past **Sep 1**, or A0 calibration fails twice, ICLR 2027 is off; **fallback venue: ICML 2027 (abstract ~late Jan 2027)**, which would also let Arm P mature into a real longitudinal arm — arguably a better paper; secondary fallback: NeurIPS 2027 D&B track (the changelog corpus + probe suite as the artifact).

**Critic:**
1. The plan front-loads three calendar-critical items (null logging, snapshot verification, novelty check) into 5 days that also contain suite freezing — realistically 2 of 5 will slip; there is no priority order.
2. The GO criterion "(ii) ≥ 15 detected diffs" conflates instrument failure with a *true negative* world (transitions genuinely quiet) — a NO-GO on a true "changelogs are actually complete" world would suppress a publishable negative result.
3. The Sep 8–15 analysis week assumes annotation (A4) finishes by Sep 8, but annotation starts Aug 26 at the earliest and needs 60–80 hours across two annotators — tight if annotators are the authors.
4. No compute-contention contingency: "one 8-GPU node for 2 weeks" is asserted, not reserved.

**Refined:**
- **Priority order for Aug 13–17:** (1) start A0 null logging + Arm P (calendar-critical, cannot be backfilled); (2) verify R-API snapshot availability (pairs can vanish); (3) novelty full-text check; suite freeze may slip to Aug 19 without harm.
- GO criterion (ii) reworded: *≥ 15 detected diffs OR a demonstrably calibrated detector (A0 pass) with high power on synthetic injected diffs* — a quiet-transition world with a calibrated instrument is a **publishable negative result** ("documented-change completeness is high for these pairs") and does not trigger NO-GO; only an *uncalibratable* instrument does.
- Annotation is split: specificity labeling of the changelog corpus (not diff-dependent) starts Aug 18, before the full runs; only diff–claim alignment waits for A1/A2 outputs. Third annotator budgeted for adjudication.
- GPU reservation and API budget approval are named blockers to resolve by Aug 15; if the 8-GPU node is unavailable, the 70B-class pairs drop and A1 runs at ≤14B scale (weaker but sufficient — the estimand is disclosure fidelity, not capability).

---

*End of B3.3 discussion. Design ids (C1–C4, M1–M5, CO1–CO3, RQ1–RQ3) interoperate with `digest.md` and `paper.md`; this document supersedes the July `discussion/discussion_trace.md` on scheduling and adds the Aug-2026 external-prior positioning (2504.04715, 2512.03816, 2506.06975, 2606.16100).*
