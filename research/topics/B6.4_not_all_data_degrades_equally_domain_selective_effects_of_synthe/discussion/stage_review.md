# Pengsida Stage Review — B6.4

> Skill: `pengsida-stage-reviewer`. Applied **after** `research-taste-auditor` (🟢) and **before** final `paper_draft.md` was locked in — per the pipeline order: `auto-research-discussion` → `research-taste-auditor` → `pengsida-stage-reviewer` → assemble/finalize `paper_draft.md`. Stages 1–4 below were checked against the confirmed `pipeline.md` stage outputs; Stage 5 was checked against the first assembled draft of `paper_draft.md`. Three REVISE findings fired and were applied — one directly into `pipeline.md`'s Stage 5 method description, two into the assembled `paper_draft.md`/`.tex` files (see "Fixes applied" at the end).

## Archetype classification

**Analysis / Finding.** Per `archetypes.md`'s tells: the core question is "we ask whether/how much a phenomenon (domain-selective contamination damage) occurs" with no new pipeline proposed as a fix for anything — the measurement apparatus (dual-normalization scorer, degeneracy-matched control, staged dose-response/scale design, cross-generator replication) is the *analytical instrument* that makes the phenomenon observable and its ranking trustworthy, not a method being pitted against baselines to win. This matches digest N12's own explicit `empirical` classification ("a controlled measurement of an existing phenomenon... not the introduction of a new system, dataset, or benchmark as the primary deliverable") and Stage 1's `study_type: empirical`. Stage 3 ("Method") and Stage 4 ("Experiments") below use the **Analysis/Finding** column of the archetype table, not the default method-paper bar.

---

## Stage 1 — Problem + Motivation

**STAGE 1 VERDICT: PASS**

**Why:** The problem clears the "so what" test before any method appears — the post-audit-tightened motivation states "no existing framework can currently tell a practitioner whether this asymmetry is real," and the stakes are stated concretely (a global, domain-uniform filtering policy over-protects tolerant domains and under-protects fragile ones), not a generic AI-importance appeal. The framing attacks the root cause (the asymmetry itself) rather than patching two literatures together — the taste audit's Section 6 already confirms the `summary` field was tightened specifically to keep this first-principles framing honest.

**Note on feasibility evidence (checklist item 6, not a blocking issue):** the stage-1 rubric asks whether an exploratory claim has, or could have, a minimum-viable experiment with a binary, pre-stated success criterion answerable in about a day. It does — `paper.md`'s own Step 9 "Walking Skeleton" (3 arms: clean control, code@100%, prose@100%; one seed each; ≈20–25 A100-hours, ≈1 day on a 4-GPU node; four binary pass criteria including "code-arm code-metric delta and prose-arm prose-metric delta each estimable... and ≥1 of the two exceeds 2× its SE"). This satisfies the checklist item, but it lives in `paper.md` and was not referenced anywhere in the confirmed Stage 1/2 pipeline outputs. **Recommendation (not a REVISE):** surface the walking skeleton explicitly in the assembled paper's Experimental Setup as the pilot-stage design, so a reader sees the feasibility evidence rather than having to trust the claim on faith. Applied below in `paper_draft.md`'s Experimental Setup.

**Note for Stage 2:** Passing here means Related Work must now establish that no one has already closed this exact gap — checked next.

---

## Stage 2 — Related Work

**STAGE 2 VERDICT: REVISE** *(fired, fixed — see below)*

**Why, quoting the draft:** The ten-work table in `pipeline.md`'s Stage 3 is genuinely specific per limitation (e.g. "DoReMi... assumes every domain shard is clean — the domain axis is causally live in its own results, yet contamination is never crossed with it" — not a generic "scalability issues" complaint), which clears the citation-dump failure mode. But the section never states, in one place, which prior work (or pair of works) is the *closest* — a reader sees ten parallel limitation entries and has to infer for themselves which one the paper is really positioned against. Per the Stage 2 bar: "hiding the method-twin is the fastest way to a desk reject... reviewers find it anyway; confront it first." `paper.md`'s own Claim-Evidence Map already does this implicitly (Claim 3 is explicitly grounded in exactly four works: MixRatio, IterStability, DoReMi, RegMix), but that ranking never surfaced as an explicit nearest-neighbor sentence in the related-work material itself.

**THE ONE FIX (applied):** Add one explicit nearest-neighbor sentence naming the two works that jointly bound the gap — MixRatio (the contamination axis, with no domain decomposition) and DoReMi (the domain axis, assumed clean) — and stating the precise delta, rather than leaving the reader to rank ten parallel entries themselves.

---

## Stage 3 — "Method" (Analysis/Finding variant: the analytical apparatus)

**STAGE 3 VERDICT: REVISE** *(fired, fixed directly in `pipeline.md` — see below)*

**Why, quoting the draft:** Each construct is defined precisely before it is used — the dual-normalization scorer, the degeneracy-matched control, the staged dose-response/scale design, and the cross-generator replication test are all specified in Stage 5's methodology ahead of any claim invoking them. Most of the inferential chain is licensed: "the correctness-strictness ordering is a substantive domain-theory hypothesis being tested *with* the [normalization] instrument, not a property the instrument confers" is exactly the kind of hinge this bar looks for. But one inferential step, as first drafted, was stated more strongly than it is licensed: `m_degeneracy_isolated_syntheticness_test`'s `key_insight` originally read as if matching the synthetic and real-text arms on measured degeneracy (repetition, type-token ratio) *fully* isolates syntheticness — but digest N6 itself already concedes this is only a **partial** identification ("cannot equate latent [degeneracies]... so residual confounding remains"). Presenting a partial identification as if it were total is exactly the kind of unjustified jump this bar exists to catch — the finding could over-claim what the control arm actually rules out.

**THE ONE FIX (applied):** Added an explicit scope caveat to `m_degeneracy_isolated_syntheticness_test`'s `key_insight` in `pipeline.md`, stating the comparison rules out excess damage attributable to *measured* surface degeneracy specifically, while leaving latent, unmeasured quality defects as residual, unresolved confounding — matching digest N6's own honest concession rather than silently dropping it.

**Note for Stage 4:** the discharge test here isn't ablation (that's the method-paper bar) — it's whether the finding is falsification-tested, not merely correlational. Checked next.

---

## Stage 4 — "Experiments" (Analysis/Finding variant: falsification, not correlation)

**STAGE 4 VERDICT: REVISE** *(fired, fixed — see below)*

**Why, quoting the draft:** The one question this stage asks in every archetype — is the claimed cause isolated from its strongest alternative — is well-served structurally: RQ5 (`rq_syntheticness_vs_degeneracy`) is a genuine falsification design (does damage survive a matched-degeneracy control, not just correlate with contamination), and RQ4 (`rq_generator_robustness`) is a genuine falsification design (does the ranking survive a structurally different generator). But the first assembled draft's RQ subsections stopped at "**Expected outcome.**" without stating the converse — what result would *refute* that expectation. Per the Analysis/Finding bar: "the strongest finding papers construct a case where, if the claim were false, the result would differ... demand at least one such test," and an "Expected outcome" alone reads as a hope rather than a pre-registered, breakable claim. `paper.md`'s own Step 6 already has this discipline baked in as five explicit "Fallback" clauses (FB1–FB5) that didn't survive into the first assembled `paper_draft.md`'s RQ subsections in that exact falsification-condition form.

**THE ONE FIX (applied):** Added an explicit **Falsification condition** line to all five RQ subsections in the Experiments section (both `paper_draft.md` and `paper_draft.tex`), stating the specific observation that would refute each expected outcome — translated directly from `paper.md`'s own pre-committed FB1–FB5 fallback wording, not invented fresh.

---

## Stage 5 — Writing (Introduction / Abstract / Conclusion)

**STAGE 5 VERDICT: PASS**

**Why:** Reverse-outline test passes — reading only each Introduction paragraph's first sentence ("Synthetic text generated by large language models is no longer a rare visitor to pretraining corpora" / "Yet a specific question about this contamination remains unaddressed" / "The nearest existing work approaches this gap from two adjacent but non-overlapping angles" / "Turning this asymmetry into a measurable claim surfaces its own obstacles" / "Our approach turns each of these obstacles into a specific design choice" / "We evaluate this design across four content domains") reconstructs the whole five-move arc (problem → gap → prior work's shared limitation → why it's hard → the approach → the evaluation) without needing sentence 2 of any paragraph. One quotable contribution sentence exists and is used consistently in title, abstract, and introduction: "damage from synthetic contamination may not be a property of the corpus as a whole but of the domain it lands in." The Conclusion names a real forward-looking limitation (the tested regime's scale ceiling and the residual C1 confound between syntheticness and latent quality defects) rather than only recapping the abstract.

---

## Fixes applied

1. **Stage 3 fix** — added an explicit partial-identification caveat to `m_degeneracy_isolated_syntheticness_test`'s `key_insight` directly in `pipeline.md` (Stage 5), so the confirmed method output does not silently overclaim what the degeneracy-matched control rules out.
2. **Stage 2 fix** — added an explicit nearest-neighbor sentence to the Related Work section's opening paragraph in `paper_draft.md`/`.tex`, naming MixRatio and DoReMi as the two works that jointly bound the gap and stating the delta plainly.
3. **Stage 4 fix** — added a **Falsification condition** line to each of the five RQ subsections in the Experiments section of `paper_draft.md`/`.tex`, translated from `paper.md`'s own pre-committed FB1–FB5 fallback wording.

All three fixes are reflected in the current `pipeline.md`/`paper_draft.md`/`.tex`/`.pdf` — this file records the review that produced them, not a pending to-do list.

---

## Phase A (re-run) — 2026-07-04

> Scope: goal.md §3's Phase A validation checklist (8 items), run fresh against `README.md`/`digest.md`/`paper.md` plus the just-upgraded `discussion/reference_candidates.jsonl` (goal.md §1 canonical schema). This is an independent gate check, separate from the pre-draft `pengsida-stage-reviewer` pass above (which reviewed the auto-research-discussion stages, not the goal.md §3 checklist). No Phase B/C compute exists in this environment; this run stops at the Phase A gate per instruction.

### 1. Digest self-verification

**PASS, with one fix.** Re-executed the digest's own self-verification claims: N0–N12 + Claims all present (confirmed by direct read of `digest.md`); cross-node references resolve — `N4.affects_works` ⊆ N3 citation keys (all 10 checked verbatim), `N6.challenge_arguments[].challenge_id` ⊆ {C1–C4} and `mechanism_components` ⊆ {M1–M6}, `N6.unaddressed_challenges = {C1,C3}` ⊆ {C1–C4}, `N8.*.addresses_challenges/tests_contributions/evaluates_mechanisms` all resolve, `N9.results[].rq_id` ∈ {RQ1, RQ_INF_2, RQ_INF_3} with exactly one result per RQ. **Gap found:** N1 and N12 carried HYPOTHESIS-level content (inferred objective/inputs/outputs; inferred contribution-type rationale) but were the only two nodes without a formal 3-part `absence_comment`, and N1 was mislabeled `Status: FOUND` despite its content being explicitly `[HYPOTHESIS]` in the same line — a tag-discipline inconsistency with every other node (N2–N11 all use PARTIAL/NOT_FOUND + absence_comment for the same confidence level). **Fixed directly in `digest.md`**: N1's status corrected FOUND → PARTIAL with a full 3-part absence_comment added; N12 given a matching 3-part absence_comment. (guidance.md Part 6 item 3's tag-discipline check; goal.md §3 item 1.)

### 2. Reference-cache integrity

**REVISE → fixed.** The 150-candidate harvest in `reference_candidates.jsonl` (Task 1 of this run) contained **zero** of the 9 OpenReview works + 1 canonical non-corpus work that `digest.md` N3/N4 and `paper.md`'s Claims/fallback text actually cite (MixRatio, IterStability, CrossModelRecursion, EntropyCollapse, SpendWisely, DoReMi, RegMix, SynthWeighting, TALR, Shumailov et al. 2024) — the harvest was drawn from a different source (recent arXiv + ACL-2023-alphabetical scrape) than the corpus (`topics/corpus/ideas.jsonl`, 11,683 OpenReview entries) that `digest.md` N3 was actually grounded against. This is exactly the failure goal.md §3 item 2 checks for ("every N3 key is a `selected` cache record"). **Fixed**: appended all 10 N3/N4-cited works to `reference_candidates.jsonl` as `selected` records (2 `method-twin`: MixRatio, DoReMi — the two nearest-neighbor works per the Stage-2 fix above; 2 `baseline`: EntropyCollapse, SynthWeighting — both named explicitly as mitigation baselines in `paper.md` N8; 5 `adjacent`; 1 `background`/canonical). Cross-checked all 9 OpenReview forum ids against `topics/corpus/ideas.jsonl`'s own `paper_id`/`paper_title` fields — all 9 titles match `digest.md` N3 verbatim (direct-match spot-check substituting for network fetch, which is blocked by OpenReview's Cloudflare browser check in this environment — confirmed via two failed `WebFetch` attempts on `9RdhTvYbX0` and `lXuByUeHhd`). **Residual, logged limitation**: none of these 10 additions has a resolvable local `pdf_path`/`digest_path` (no PDF is cached for them in this environment; their grounding lives only in `digest.md`'s own inline N3/N4 prose, sourced from the `ideas.jsonl` proposal-corpus record, not a standalone `paper-digest` extraction). `verified.id_resolves = false` for all 10, honestly reflecting this. This does not block Phase A — `paper.md`'s claims are adequately grounded by the inline N3/N4 text — but a future pass with network/PDF access should backfill real `digest_path`s for the 2 `method-twin` + 2 `baseline` entries per goal.md §1 lifecycle step ②. No `pending` verdict anywhere in the final 160-line cache (confirmed programmatically).

### 3. Tag discipline

**PASS** (after the item-1 fix). Every assertion in `digest.md` carries one of `[GIVEN]`/`[HYPOTHESIS]`/`[GROUNDED:corpus]`/`[NON-CORPUS, canonical]`/`[PLACEHOLDER]`; no silent HYPOTHESIS→GIVEN promotion detected (Claim 4 is the only GIVEN-tagged claim, and it is a near-verbatim restatement of the seed's own "结论直接指导数据筛选优先级" line, correctly sourced). `paper.md`'s pre-registration framing (binary hypotheses, pre-committed fallbacks) does not assert anything as an observed fact.

### 4. Claim–Evidence Map completeness

**PASS.** All six claims trace to an H-id (Claims 1,2,5,6 → H1/H2/H4+H5/H3(iii)) or a supported-by-design definition (Claim 3, positioning only; Claim 4, fallback-covered via H1∧(H2 or FB2)). Every H1–H5 has a verbatim fallback (FB1–FB5); the central family (H1) has global-pivot coverage (F-G1). No orphans in either direction.

### 5. Hypothesis/assumption machinery

**REVISE → fixed.** Checked every H* against guidance.md §3.1's seven slots and every A* against §3.2's four slots.
- **Effect floor missing** on H1, H2, H3(i), H5 — each was stated as significance-only (a bootstrap CI excluding 0, or p < α), with no minimum native-unit magnitude, violating §3.1's "significance without magnitude passes nothing." **Fixed**: added explicit `effect_floor` values to H1 (≥0.10 slope difference), H2 (≥0.05 strict-vs-tolerant contrast), H3(i) (≥0.05 per-domain slope), H5 (≥0.03 beyond degeneracy control), each pinned to the existing native units (Δ_d, β_d) and cross-referenced to the pilot gate G-P1's own detectability threshold for consistency. H4's τ ≥ 0.66 already functioned as a magnitude floor — no fix needed.
- **Missing aggregation rule** on H3 — three sub-parts (i)/(ii)/(iii) were listed without saying which combination yields PASS/FAIL, violating the "binary means binary" rule. **Fixed**: added an explicit Aggregation line — H3 PASS iff (i) ∧ (iii); (ii) is descriptive only and selects which FB3 sub-clause applies.
- **Missing gate/consequence** on A2, A6, A7 — each had a `Fails if`/`Detected by` but no explicit gate phase or consequence-to-H* statement (§3.2 requires both). **Fixed**: added explicit `Gate:`/`Consequence:` text to A2 (PG-2, walking skeleton; blocks H1–H5), A6 (Stage 2; H2 fails — consequence already present, gate added), A7 (Stage 2; H4 scope-limited — consequence already present, gate added).
- **Missing instrument-validity assumption** for the one non-deterministic metric — MT-Bench's LLM-judge (dialogue domain) was covered only by threat `t5` (a mitigation note), with no assumption-ledger entry (detection + gate + consequence), violating Part 2 A2's "unvalidated LLM-judge" reviewer-kill and guidance.md R2. **Fixed**: added **A8** (dialogue judge validity) with an R2-lite validation (100-response, 2-human-rater, κ ≥ 0.7 calibration, frozen before Stage 2, gated at a new PG-3) and a concrete consequence (κ < 0.7 ⇒ dialogue's primary DV demotes to validation-loss-only). Threaded A8 into E1/E2/E3's `Assumption:` lines (all three use the dialogue judge score inside `Δ_d(r)` or `β_d`) and into E4 (β-rankings span all four domains) and E5 (conditionally, if dialogue is E2's top-ranked domain).
- B0 + B-alt + F-G1 all present and correctly structured (checked, no change).

### 6. Method-rigor audit (guidance.md Part 6 items 1–10 + Part 2 A2 evidence standard)

**REVISE → fixed**, three gaps beyond item 5's hypothesis/assumption fixes:
- **Item 1 (estimand)**: no explicit R1-style one-sentence estimand existed anywhere in `paper.md`. **Fixed**: added an **Estimand** line to Step 5 (quantity = β_d + cross-domain ordering; unit = one (domain, ratio, seed) cell; reference population = the tested ≤3B/≤2.5B regime; decision fed = curation-budget allocation).
- **Item 7 (confound-removal, R3)**: no design constraint in `paper.md` was written as an explicit "constraint X removes confound Y" one-liner (the word "confound" did not appear in `paper.md` at all, though `digest.md`'s challenges implicitly rely on the concept). **Fixed**: added a **Confound-removal** block to Step 5 naming six constraints and the specific confound each removes (global-diet shift, run-to-run variance, benchmark-construct artifact, generic degeneracy, generator-idiosyncrasy, mere-presence-of-synthetic-data).
- **Item 8 (≥1 mechanism analysis, R6)**: the design tested *that* damage is domain-selective (H1/H2) but had no analysis testing *why* — the Step-0 mechanism (verifiable-wrongness converts to corrupted signal) was asserted, not probed independently of the aggregate ranking. **Fixed**: added **M7 — Mechanism analysis**, a verifiable-error audit of the injected synthetic code/math documents (execution/exact-match check on the synthetic content itself) correlated against β_d, explicitly framed as explanatory (not a new pass/fail gate) and recorded as separable from H1/H2 in `claim_map.md`.
- **Item 9 (power/INCONCLUSIVE)**: A5 described increasing seeds under low power but never named what happens if power remains inadequate afterward — guidance.md/Part 4 situation 5 requires thin cells be pre-declared INCONCLUSIVE, never null, never silently dropped. **Fixed**: added the INCONCLUSIVE consequence and its Holm-denominator exclusion rule directly to A5.
- Items 2 (verb check), 3 (H* slots, fixed under item 5 above), 4 (A* slots, fixed under item 5), 6 (per-instrument R2 plan — MT-Bench's now closed by new A8; deterministic metrics need no such plan), 10 (archetype named + A2 evidence standard, now met given the above fixes) — all PASS.

### 7. Stage cross-check (advisory)

**Already run, still valid.** The `pengsida-stage-reviewer` pass recorded above (Stages 1–5, three REVISE findings already fixed into `paper_draft.md`/`.tex`/`pipeline.md`) covers this. Today's fixes (effect floors, aggregation, confound-removal, estimand, mechanism analysis, A8, N1/N12 absence comments) are refinements to `paper.md`/`digest.md` that strengthen but do not contradict or restructure anything that pass checked — no re-run needed; advisory, non-blocking either way.

### 8. Taste audit currency

**PASS, no re-run needed.** `taste_audit.md` is anchored on the Motivation (Stage 2) and Method (Stage 5) summary text. None of today's fixes touched the asymmetry statement (Step 0) or the term-table's existing definitions (Step 5) — they added new machinery (effect floors, an estimand line, a confound-removal list, an assumption, a mechanism-analysis component) alongside the audited text without altering it. Per goal.md §3 item 8, a re-audit is only required when the asymmetry statement or formal definition is materially edited; neither was.

### Phase A gate result: **PASS (after fixes)**

All 8 checklist items now clear. Six REVISE-level findings were fixed directly in `digest.md`/`paper.md` (items 1, 2, 5×4, 6×4 above); none required a STOP. Phase B (walking skeleton) is unblocked on paper — but per this run's scope, no Phase B/C execution occurs here (no real experiment compute exists in this environment). See `discussion/pipeline.md` for the phase-log entry.
