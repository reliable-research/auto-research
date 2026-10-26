# Pengsida Stage Review — T3.3

> Skill: `pengsida-stage-reviewer`. Applied **after** `research-taste-auditor` (🟢) and **before** final `paper_draft.md` was locked in — per the pipeline order: `auto-research-discussion` → `research-taste-auditor` → `pengsida-stage-reviewer` → assemble/finalize `paper_draft.md`. Stages 1–4 below were checked against the confirmed `pipeline.md` stage outputs *as realized in the first assembled* `paper_draft.md`; Stage 5 was checked against that same first assembled draft's Introduction/Abstract/Conclusion prose. One REVISE finding fired and was applied (see "Fixes applied" at the end); the draft you now see in `paper_draft.md`/`.tex`/`.pdf` already reflects it. Two structural requirements that fired as REVISE in the B5.5 exemplar's own review — a nearest-neighbor sentence in Related Work and per-RQ falsification conditions in Experiments — were treated as mandatory from the first assembly pass for this topic (per the task brief), so both were already present when this review ran; they are not re-reported as findings here because they were never absent to find.

## Archetype classification

**Analysis / Finding.** Per `archetypes.md`'s tells: the core question is "we ask whether/how often a phenomenon (adversarially fragile identification) occurs" with no new identifier proposed as a fix — GovSpan-Adv, the paired metrics protocol, the localization harness, and the boundary audit are the *analytical apparatus* that makes the phenomenon observable and its alternative explanations rule-out-able, not a method being pitted against baselines to win. This matches digest N12's own `empirical` classification and Stage 1's `study_type: empirical`. Stage 3 ("Method") and Stage 4 ("Experiments") below use the **Analysis/Finding** column of the archetype table, not the default method-paper bar.

---

## Stage 1 — Problem + Motivation

**STAGE 1 VERDICT: PASS**

**Why:** The problem clears the "so what" test before any method appears. Quoting the draft: "Current treatments of 'which text is binding' typically assign that status by channel position... known in advance of any content ever arriving" — a first-principles framing of the root gap (identification-by-position, not identification-by-content), not a patch. The stakes are concrete and non-generic: "an adversary who preserves a rule's binding force while flattening its register... can defeat identification without ever touching the pinning mechanism itself." The Einstein ratio holds and then some — method language ("Our approach turns each of these obstacles...") doesn't appear until paragraph 5 of 6; paragraphs 1–4 are pure problem, gap, prior-work insufficiency, and inherent difficulty.

**Note for Stage 2:** Passing here means Related Work must now establish that no one has already closed this exact gap — checked next.

---

## Stage 2 — Related Work

**STAGE 2 VERDICT: PASS**

**Why, quoting the draft:** The four thematic paragraphs are genuinely threaded, each closing on a problem-tied limitation rather than a generic one — e.g., "MemoryCallback... assumes salience can eventually be reassessed — an assumption a disguised constraint engineered to look unimportant at write time defeats by construction." The nearest-neighbor test is cleared explicitly and up front, not left for the reader to infer: "ASIDE offers the closest existing formulation of 'which text is executable and binding versus merely conversational data'... SeqMonitor offers the closest existing treatment of evasion via benign-looking surface form... Neither work measures span-level constraint-identification error under a validated, bidirectional register-disguise attack, which is precisely the gap this paper is built to close." No cited work already solves the stated problem (checked against each closing sentence), so Stage 1 is not undermined retroactively.

**Note for Stage 3:** Passing here means the Method (analytical apparatus) must now actually target this exact gap — checked next.

---

## Stage 3 — "Method" (Analysis/Finding variant: the analytical apparatus)

**STAGE 3 VERDICT: PASS**

**Why:** Each construct is defined precisely *before* it is used — $y_i$, $f_\theta$, $\text{Evade}$, $\text{Spoof}$, and the validity gate $V$ are all given in Problem Definition ahead of any claim that invokes them, so no construct is "named after the fact." The inferential hinge for each of the five modules is stated explicitly rather than asserted by fiat: the cross-family ablation's Insight states directly why a family swap — and only a family swap — separates "genuine, family-independent effect" from "shared-family artifact," and the boundary audit's Insight states directly why blind, independently-run re-annotation is what separates identifier error from contested ground truth. No orphan components: all five Methodology subsections trace to a named sub-problem from `pipeline.md` with no leftover machinery, and the two adapted identifier families (ASIDE's privilege signal, SeqMonitor's cumulative-context monitor) are correctly kept out of Methodology and described only as systems under test in Experimental Setup — they are not, and are not written up as, part of this paper's own contributed apparatus, which is what keeps this section from reading as an unmarked synthesis of two prior methods.

**Note for Stage 4:** the discharge test here isn't ablation in the method-paper sense — it's whether each claimed cause is isolated from its strongest alternative, falsification-style, not merely correlational. Checked next.

---

## Stage 4 — "Experiments" (Analysis/Finding variant: falsification, not correlation)

**STAGE 4 VERDICT: REVISE** *(fired, fixed — see below)*

**Why, quoting the first assembled draft:** Most of the RQ set is well-isolated — RQ8's cross-family ablation is a genuine falsification design (swap the rewriter's family, see if the verdict survives), and RQ2 through RQ7 each carry an explicit falsification condition that would actually flip the corresponding claim. But the first assembled draft's Experimental Setup asserted a second, distinct confound-control by construction alone, without ever stating how it would be checked: "A cross-family rewriter ablation plus a length-and-topic-matched non-constraint control isolates whether any measured gap is register-disguise fragility rather than attacker-defender family self-consistency **or spurious distributional cues**." The family-coupling half of that sentence is discharged by RQ8; the "spurious distributional cues" half was never discharged by anything — no test anywhere in the draft would catch an identifier that is actually keying on span length or topic (which happen to correlate with the constraint/non-constraint label) rather than on force or register at all. Per the Analysis/Finding bar, this is exactly the class of un-ruled-out alternative explanation Stage 4 exists to catch: "is the claimed cause isolated from its strongest alternative?" — here, a real alternative (surface-statistic exploitation, not register-disguise fragility) was named in prose but never actually isolated by a check.

**THE ONE FIX (applied):** Since the underlying design already intends to *prevent* this confound by matching span length and topic at corpus-construction time (not by comparing an unmatched arm), the fix is not a new research question — that would inflate the tier accounting beyond what Stage 6 already committed to — but a stated, pre-registered **verification** that the matching construction actually worked, analogous in role to the annotation-quality κ already reported for labels: a two-sample distributional test (Kolmogorov–Smirnov on length; cosine-similarity distribution on topic embeddings) confirming no significant length/topic gap remains between the matched pools, reported as a corpus-validity statistic before any identifier is run. This closes the gap between what the prose claimed ("isolates... spurious distributional cues") and what the design actually checked (nothing, previously).

---

## Stage 5 — Writing (Introduction / Abstract / Conclusion)

**STAGE 5 VERDICT: PASS**

**Why:** Reverse-outline test passes cleanly — reading only each Introduction paragraph's first sentence ("Large language model agents are increasingly trusted to operate over long-running, multi-session interactions..." / "Yet that upstream step has quietly been assumed rather than tested." / "The nearest existing work approaches this gap from either side without closing it." / "Turning this gap into a measurable question surfaces genuine difficulties of its own." / "Our approach turns each of these obstacles into a specific design choice." / "We evaluate this design on GovSpan-Adv...") reconstructs the full five-move arc (problem → gap → prior work's shared insufficiency → why it's hard → the approach → the evaluation) without needing sentence two of any paragraph. One quotable contribution sentence exists and is used consistently across title and abstract: the title's "Force Is Not Register" and the abstract's "an adversary who preserves a rule's binding force while flattening its register... can defeat identification without ever touching the pinning mechanism itself." The Conclusion names two real forward-looking limitations (identification-only scope; the contested-label boundary as a target for a richer formalization, not a solved problem) rather than only recapping the abstract at the same altitude.

---

## Fixes applied

1. **Stage 4 fix** — the Experimental Setup's Baselines paragraph in `paper_draft.md` (and mirrored in `paper_draft.tex`) was rewritten to (a) explicitly attribute the family-coupling confound check to RQ8 by name, and (b) add a stated, pre-registered corpus-validity verification (a two-sample distributional test on span length and topic-embedding similarity) for the length/topic-matching construction, so the claim that the design "isolates... spurious distributional cues" is backed by an actual check rather than asserted by construction alone.

No other stage required a fix — Stages 1, 2, 3, and 5 passed against the draft as first assembled. This is recorded honestly: the two REVISE findings the B5.5 exemplar's own review produced were pre-empted by this task's mandatory assembly requirements (nearest-neighbor sentence, per-RQ falsification lines), so this review had to look for genuinely different problems rather than rediscovering the same two — the length/topic-matching verification gap above is the one it found.

---

## Phase A (re-run)

> Run against goal.md §3's canonical 8-item checklist (distinct from the `pengsida-stage-reviewer` 5-stage review above, which checks the auto-research-discussion pipeline's own writing stages). Inputs: `README.md`, `digest.md`, `paper.md`, and the rebuilt `discussion/reference_candidates.jsonl` (Task 1 of this run rewrote the cache into goal.md §1's canonical schema and gave every one of the 150 harvested candidates a selected/rejected verdict — see cache diff summary at the end of this section). Guidance.md is the standard applied throughout; every REVISE cites its section. Date: 2026-07-04.

### 1. Digest self-verification — **PASS**
`digest.md`'s own "Self-verification pass" (V-01 through EX-12) was re-executed by hand: all of N0–N12 + Claims are present; every non-GIVEN field carries a 3-part `absence_comment` (what_missing/why_matters/implication) — spot-checked N1, N4, N6, N9; every cross-node id (`N4.affects_works`, `N6.challenge_arguments[].challenge_id`/`mechanism_components`, `N8...addresses_challenges`/`tests_contributions`/`evaluates_mechanisms`, `N9.results[].rq_id`) resolves to a real N3/N5/N6/N7/N8 id with no dangling reference. No tag was found silently promoted from [HYPOTHESIS] to [GIVEN] anywhere in N1–N12.

### 2. Reference-cache integrity — **REVISE → FIXED (residual note)**
**Finding:** `digest.md` N3 grounds this topic against 9 real papers (ASIDE, ChatInject, TensorTrust, SeqMonitor, PrefEval, R2-Guard, RECAST, MemoryCallback, InstructionHierarchy) read from the local `openview_corpus/ideas.jsonl` corpus. **None of the 9 appeared anywhere in `reference_candidates.jsonl`** — the 150-candidate harvest was built by a separate semantic-search process over `arxiv_corpus` + `openview_corpus/paper_cache` (ACL Anthology) and never retrieved digest.md's own N3 works. Per goal.md §3 item 2 ("every N3 key is a `selected` cache record"), this was a hard fail: the cache the digest claims to be grounded in did not contain the grounding.
**Fix applied:** all 9 works were added to `reference_candidates.jsonl` as `selected` records (relevance tags: ASIDE/SeqMonitor/PrefEval/MemoryCallback = `method-twin`, ChatInject/R2-Guard/RECAST = `adjacent`, TensorTrust/InstructionHierarchy = `background`), each `why` matching digest.md N3/N4's own stated gap. Spot-check (3 of 9, guidance.md §1 "spot-check 2–3 ids"): `C81TnwHiRM` → "ASIDE: Architectural Separation of Instructions and Data in Language Models"; `WVhgFSKniL` → "ChatInject: Abusing Chat Templates for Prompt Injection in LLM Agents"; `1cymflI2Lh` → "Look Back to Reason Forward: Revisitable Memory for Long-Context LLM Agents" — all three resolved against the local `ideas.jsonl` corpus (paper_id → paper_title match), confirming digest.md's [GROUNDED:corpus] tag was honest.
**Residual, not blocking:** none of the 9 has a cached PDF or a standalone `paper-digest`-extraction file in this environment (`ideas.jsonl` carries only `paper_id`/`paper_title`/`paper_url`/`proposal`, no PDF), so `pdf_path`/`digest_path` are `null` and `verified.id_resolves = false` for all 9. Their "digest" is presently digest.md's own N3 `approach_summary` prose, not a separate extraction artifact. **Logged as a to-do in `pipeline.md`** for the next harvest pass (fetch/cache these 9 PDFs and run `paper-digest` extraction mode) rather than fixed here, since fetching external PDFs is outside a static-document Phase A pass and no PDFs exist locally to substitute. No `pending` verdicts exist anywhere in the rebuilt cache (all 159 records are `selected` or `rejected`).

### 3. Tag discipline — **PASS**
Confirmed by direct read of N1–N12: every assertion carries `[GIVEN]`, `[HYPOTHESIS]`, `[PLACEHOLDER]`, or `[GROUNDED:corpus]`; N9's results are explicitly labelled "PLACEHOLDER — hypothesized direction only" rather than presented as findings; no instance of a [HYPOTHESIS] item being treated as settled fact downstream.

### 4. Claim–Evidence Map completeness — **REVISE → FIXED**
**Finding:** the map's last row ("Register-disguise is the isolated cause... | B-alt, A3 | needs-experiment") had no fallback — guidance.md §3.3 item 2 requires B-alt to "pre-commit the downgrade wording: what the claim becomes if the effect survives the rival vs. dies." `paper.md`'s B-alt paragraph stated only the survives-both case ("If Δ survives both, register-disguise is the isolated cause") with no committed wording for either failure mode, and per-claim scoping (guidance.md: "the downgrade is per-claim, not per-paper") was absent.
**Fix applied:** added explicit downgrade wording to `paper.md`'s Mandatory-baselines/B-alt paragraph for both failure modes (family-swap fails → downgrade to a phenomenon-stands/mechanism-unsupported wording; matching-validity test fails → downgrade to a confounded/unsupported-pending-re-match wording), each naming which Claim–Evidence Map rows survive and which don't, citing guidance.md §3.3.

### 5. Hypothesis/assumption machinery — **REVISE → FIXED**
- H\* (RQ1/RQ_INF_1/RQ_INF_2): all seven guidance.md §3.1 slots are present in substance (applies_if/assumptions, metric, test, alpha, effect_floor, aggregation via named-primary-identifier, verbatim fallback) — PASS as written, just merged into prose rather than seven literal labelled bullets; no fix needed.
- A\* (A1–A6): detection methods were already present for all six, but **no A\* named an explicit gate** (guidance.md §3.2: "gate: PG-j if checked in the pilot; else the phase that checks it") — a real gap, since guidance.md is explicit that "an assumption that has no detection method is not an assumption — it's a hope," and the same is true of a detection method with no stated *when*. **Fix applied:** added `*Gate:*` to every A1–A6 in `paper.md`, mapping A1/A2 to PG-1/PG-2 inside the Step 9 walking skeleton and A3/A4/A5/A6 to the named scale-up phase that actually exercises them (family swap, per-source split, transfer check, and full-n power all require more arms/n than the 2-arm 60-pair skeleton can run) — an honest deferral, not an omission, but it now says so.
- Additionally added the missing **thin-cell INCONCLUSIVE pre-declaration** to A6 (guidance.md §3.2's worked A6 instance: "a pre-declared rule that thin cells are INCONCLUSIVE, never null"), naming the Stage-2 depth-stratified cells and any single-source subset as the cells this applies to.
- B0 + B-alt + F-G1 all present with pre-committed wording (B0/F-G1 already adequate; B-alt fixed under item 4 above).

### 6. Method-rigor audit — **REVISE → FIXED**
Guidance.md Part 6 self-check, item by item:
1. Estimand in one sentence (R1) — **missing, fixed**: added an explicit `**Estimand**` sentence to Step 5 (quantity = Δ per direction per identifier; unit = one span pair; reference population = TensorTrust/policy-rule + LMSYS-Chat-1M spans; decision = whether identification is reliable enough to treat pinning's precondition as solved).
2. Verb check (no undefended integrate/unify) — PASS, Step 3 already does this explicitly.
3. Every H\* has all seven slots incl. verbatim fallback — PASS (item 5 above).
4. Every A\* has detection + gate — **fixed** (item 5 above).
5. B0+B-alt+F-G\* pre-committed — **fixed** (item 4 above).
6. Every instrument has the 5-step R2 plan with an acceptance threshold — **missing, fixed**: added a full 5-step R2 walkthrough for M1's constraint/non-constraint label schema and M2's validity gate to `paper.md` (grounding → calibration-set draft → 2-annotator validation at κ≥0.7 → confusion-structure inspection → freeze-before-scale), naming guidance.md Part 4 situation 7 as the route if either instrument fails validation.
7. Every design constraint names its confound (R3) — **stale, backported**: the length/topic-matching confound ("removes surface-statistic exploitation as an explanation") was already named in `paper.md`'s B-alt paragraph, but the *verification* of that constraint (KS test + cosine-similarity test) existed only in `paper_draft.md`/`.tex` (added by the Stage-4 fix above) and had never been written back into `paper.md`, the nominal pre-registration source of truth. **Fixed**: backported the same two-sample-test verification into `paper.md` so the pre-registration and the draft no longer disagree about what was actually pre-committed.
8. ≥1 mechanism analysis budgeted (R6) — PASS: M5's blind boundary/ambiguity audit functions as the required "why" layer (decomposing measured fragility into identifier failure vs. contested ground truth), matching guidance.md's enrichment/decomposition pattern.
9. Power stated per cell; thin cells pre-declared INCONCLUSIVE — **missing, fixed** (item 5 above; A6 now carries the pre-declaration).
10. Archetype named + Part 2 evidence standard met — PASS-contingent-on-fixes-above: archetype = A2 empirical/measurement (Step 2), and with items 1/4/5/6/7/9 now fixed, the plan meets A2's stated bar (validated instrument + controlled comparison + pre-registered effect-floor tests + rival-explanation ablations + ≥1 mechanism analysis) on paper, not merely by intention.

### 7. Stage cross-check (advisory) — **PASS (already run)**
The `pengsida-stage-reviewer` 5-stage review above already covers N1↔Stage 1, N3/N4↔Stage 2, N6↔Stage 3, N8/E\*↔Stage 4, archetype from `paper.md`, and found/fixed one REVISE (Stage 4, now folded into item 6.7 above via the backport). No new advisory findings beyond what is already recorded there.

### 8. Taste audit currency — **PASS, no re-run needed**
`taste_audit.md`'s verdict (🟢, human-shaped) is keyed to Step 0's asymmetry sentence and Step 3's method summary. None of this Phase A pass's fixes touch either — all six fixes (estimand sentence, assumption gates, INCONCLUSIVE rule, R2 protocol, B-alt downgrade wording, KS/cosine backport) are additive rigor/completeness edits to Steps 5/6/Assumptions, not changes to the asymmetry claim or the method's verb choices. No re-audit triggered.

### Gate result: **REVISE fixes applied; Phase A now PASSES.** Phase B/C are out of scope for this run (no experiment compute available in this environment) — per goal.md, the run stops at this gate.

### Reference-cache diff summary (Task 1 of this run)
`reference_candidates.jsonl` rewritten from the flat harvest schema (topic_id/rank/score/ref_id/...) into goal.md §1's canonical schema. Of the 150 harvested candidates (110 arXiv + 40 ACL-Anthology-via-"openview"), **6 selected / 144 rejected** — every rejection carries a specific, paper-referencing one-sentence `why` (task/domain/threat-model mismatch, named against that paper's actual problem statement), not a boilerplate line. Plus **9 records added** for the N3 grounding-integrity fix above (item 2), all `selected`. Final cache: **159 records, 15 selected / 144 rejected, 0 pending.** Selected-from-150: `2607.01153` (Adversarial Pragmatics benchmark, adjacent), `2512.23684` (Multilingual Hidden Prompt Injection on Reviewing, adjacent), `2512.23128` (TRAP web-agent persuasion benchmark, adjacent), `2512.22894` (DECEPTICON dark-pattern benchmark, adjacent), `2512.23557` (Trustworthy Agentic AI provenance defense, adjacent), `2606.30306` (Always-On Agents survey, background).
