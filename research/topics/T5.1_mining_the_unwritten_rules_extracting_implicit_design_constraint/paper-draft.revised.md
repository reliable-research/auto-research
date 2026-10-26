# Mining the Unwritten Rules: Extracting Implicit Design Constraints from Code Review History and Measuring Their Violation by Green-Test Agent Patches

**Target venue:** FSE 2027 (submission 2026-10-02). **Status:** revised full draft (2026-08-13), supersedes the autodiscussion package draft; experiment frame restored to the audited discussion.md plan.

## Abstract

Coding agents now routinely produce patches that pass a repository's full test suite yet fail human review: METR reports that roughly half of test-passing SWE-bench Verified agent PRs would not be merged by maintainers. The gap between "tests pass" and "humans accept" is where a repository's *unwritten* design constraints live — error-handling norms, layering rules, and API conventions that reviewers enforce in practice but that no test, linter, or document encodes. We present the first instrument that (i) mines these constraints from PR review history, using *change-inducing* review comments — an in-line comment whose anchored lines a later commit modifies as requested — as behavioral evidence of enforcement; (ii) consolidates recurrent evidence (≥3 threads, ≥2 reviewers, ≥2 authors) into validated, versioned **constraint cards** with scope, trigger, checkability class, support counts, and evidence links, whose extraction precision is established by dual human audit (κ reported) rather than LLM self-grading; (iii) measures each card's *unwrittenness* against the repository's own lint configuration and documentation; and (iv) measures per-category violation rates of green-test agent patches versus matched human gold patches on identical SWE-bench Verified tasks, so every violation found is by construction invisible to the test oracle. A budgeted outcome-linkage analysis tests whether mechanically checkable violations predict first-round review verdicts on held-out human PRs. Unlike concurrent work that validates per-issue design constraints with LLM judges (arXiv 2604.05955), our catalogs are repository-level, recurrence-filtered, human-audited, and linked to both an agent-versus-human contrast and real review outcomes; unlike procedural-compliance verification over agent execution traces (AgentLTL, MANTRA), we check the *artifact* — the patch text — against norms that were never written down. The card artifact is released as the input contract for downstream automated-checker evaluation.

**Keywords:** code review mining, implicit conventions, coding agents, SWE-bench, acceptance gap, empirical software engineering.

## 1 Introduction

The current generation of coding agents has largely saturated the test oracle: frontier systems produce green-test patches for a large fraction of SWE-bench-style tasks. Production evidence says the *acceptance* oracle disagrees. In a study where active maintainers of three SWE-bench Verified repositories reviewed 296 agent-generated PRs, maintainer merge decisions ran ~24 percentage points below the automated grader's scores — roughly half of test-passing PRs would not be merged into main [METR 2026]. Field studies of in-the-wild agent PRs report the same direction: 45.1% of merged agent PRs required revisions, including revisions for project-specific standards [Watanabe et al. 2025], and agent-authored test patches carry weak or absent oracle signals in 80.2% of cases, with oracle strength independently predicting merge [Banik et al. 2026].

We measure one candidate mechanism of this acceptance gap — implicit-constraint violation — and quantify its share, not the whole gap. A **design constraint** for repository R is a recurring, prescriptive expectation about how code in R should be written that reviewers demonstrably enforce but that no machine-checkable or documented artifact of R encodes. Review history is the uniquely good substrate for recovering such constraints: it already exists at scale (mature OSS projects carry 10⁴–10⁵ anchored review comments with revisions and verdicts); it is *behaviorally validated* — a change-inducing comment records an expectation the author actually complied with, stronger evidence than any stated preference in surveys, interviews, or agent-rule files; and it is produced by the same oracle that defines the acceptance gap, so mined constraints are merge-relevant by construction.

Concurrent work confirms the problem is real but leaves the instrument unbuilt. *Does Pass Rate Tell the Whole Story?* [arXiv 2604.05955] validates 1,787 design constraints for 495 issues in six SWE-bench-aligned repositories and finds that fewer than half of functionally correct patches are design-satisfying — but its constraints are per-issue, validated by an LLM verifier, and it measures neither an agent-versus-human contrast nor any link to real merge outcomes. Compliance benchmarks for *written* contribution rules [RepoComplianceBench, arXiv 2607.26819] and trace-level procedural verification of agent runs [AgentLTL, arXiv 2607.02599; MANTRA, arXiv 2605.06334] address the complementary cases where the rules are already explicit or the object of compliance is the execution process rather than the produced artifact. What is missing is exactly what maintainers enforce and benchmarks omit: repository-level catalogs of *unwritten*, recurrently enforced design constraints, with validated extraction, and a quantitative account of how often green-test agent patches violate them relative to matched human work.

**Contributions.**
1. **A validated mining instrument.** A pipeline from PR review threads to per-repository constraint-card catalogs, with every LLM stage anchored by human-verified samples: dual-annotated card precision on n=300 (two-bar gate: ≥0.5 continue / ≥0.7 publishable, Wilson CIs, κ), cluster-purity audit, an independent human recall proxy on held-out threads, and a non-LLM keyword/directive baseline bounding the LLM's added value.
2. **The unwrittenness measurement.** A two-level operational test — `linter-expressible` (coverable by an existing configured rule or a ≤20-line custom semgrep/ruff rule) and `doc-mentioned` (a doc sentence states the rule at comparable specificity) — quantifying what fraction of enforced norms are written down nowhere.
3. **The violation study.** Applicability-normalized violation rates per category (error handling / architectural convention / API convention / other) for 300–500 green-test agent patches from ≥3 agent systems versus matched human gold patches on identical SWE-bench Verified tasks (within-task McNemar pairs, Holm–Bonferroni), with tiered adjudication (mechanical / static / agreement-gated LLM judge with per-category κ ≥ 0.6 / human) and blinded annotation with a measured blinding-integrity bound.
4. **Outcome linkage.** On held-out human PRs from a disjoint window, mechanical-tier violations regressed against first-round review verdicts with size and author-experience covariates — testing within our own data whether mined constraints predict acceptance.
5. **A consumable artifact.** Versioned constraint cards (statement, scope, trigger, checkability, support, evidence links, written-status, examples, human-verified flag), smoke-tested end-to-end as the input contract for downstream automated-checker evaluation.

## 2 Related Work

**(a) Empirical foundations of code review.** Bacchelli & Bird [ICSE 2013] established that convention enforcement and knowledge transfer, not just defect finding, dominate modern review outcomes; Sadowski et al. [ICSE-SEIP 2018] document review as norm enforcement at Google scale; Bosu et al. [MSR 2015] taxonomize comment usefulness. These works establish the phenomenon but produce human-readable taxonomies, not machine-applicable per-repo rule inventories checkable against unseen patches.

**(b) Automating review activities.** CodeReviewer [Li et al., ESEC/FSE 2022] and the LLM review line learn diff→comment mappings; convention knowledge stays latent in weights, no persistent auditable artifact is distilled, and defect-focused variants explicitly deprioritize convention comments as "nitpicks" — the exact slice we target. Surveys of code-review benchmarks [Khan et al. 2026] confirm no benchmark evaluates recovered *norm inventories*.

**(c) Convention and rule induction from code history.** NATURALIZE [Allamanis et al., FSE 2014] learns surface conventions from code; Getafix [Bader et al., OOPSLA 2019] learns fix patterns from edits; MUDetect/MUBench mine API-misuse patterns; classic spec mining (Ammons et al.; Daikon) infers invariants from runs. All induce rules from *code or edits alone* and therefore cannot capture norms whose only evidence is a reviewer's stated rationale (layering rules, "never catch bare Exception at this boundary"); none measures agent compliance. LintCFG [Zhang et al. 2026] compiles *stated* coding standards into linter configs — it presupposes the rules are written down, which is precisely what our unwrittenness measurement shows is often false.

**(d) Design-constraint compliance of agent patches — the nearest neighbors.** *Does Pass Rate Tell the Whole Story?* [arXiv 2604.05955] is the closest concurrent work: it mines and validates design constraints from real-world pull requests (1,787 constraints, 6 repos aligned with SWE-bench Verified/Pro) and shows functional correctness has negligible association with design satisfaction. We concede the shared thesis and differ on every axis of the instrument: their constraints are indexed to individual issues and validated by an LLM-based verifier; ours are repository-level norms admitted only on recurrence across ≥3 threads, ≥2 reviewers, and ≥2 authors, validated by dual human audit with pre-registered agreement thresholds; they measure agent compliance in isolation, we measure agents *against matched human gold on identical tasks* and additionally link violations to *real first-round review outcomes*; and only we measure unwrittenness against the repository's own lint/doc surface. RepoComplianceBench [arXiv 2607.26819] evaluates agent compliance with *written* contribution rules (CONTRIBUTING/AGENTS files); our subject is the complement — norms written down nowhere. The taxonomy-level neighbor *From Correctness to Collaboration* [arXiv 2512.23844] mines static, already-written rule files and interviews qualitatively, with no per-repo catalogs, support counts, violation rates, or outcome linkage.

**(e) Boundary: artifact-level design conformance vs trace-level procedural compliance.** A concurrent cluster verifies that agent *executions* comply with procedural specifications: AgentLTL [arXiv 2607.02599] checks temporal-logic obligations over agent traces, and MANTRA [arXiv 2605.06334] enforces trace-level workflow compliance. That line answers "did the agent *behave* according to the process rules?" over event sequences at runtime. We answer "does the produced *artifact* — the patch text — conform to the repository's design norms?", a static property of source code checked after the fact, mined from human review dialogue rather than specifications or traces, and consumed by a static patch checker rather than a runtime monitor. The routing rule is explicit: any candidate whose natural statement is a temporal obligation over runtime or tool-call events is out of scope here and belongs to the trace-compliance line; any trace-line candidate whose evidence is review-dialogue text belongs here. The two are complementary layers of an agent-oversight stack; neither subsumes the other.

**(f) Agent-PR field studies and LLM-judge validity.** Watanabe et al. [2025] (567 Claude Code PRs: 83.8% acceptance, 45.1% revised), Peralta et al. [arXiv 2605.22534] (only 35.7% of agentic-PR rejections are clear agent failures — workflow confounds matter), Patel et al. [arXiv 2606.21804] (agent-on-agent maintainability drop up to 13.1%, unexplained by conventional metrics), and Banik et al. [arXiv 2606.18168] motivate the acceptance gap but stop at coarse categories. Because our pipeline uses LLM stages, we adopt the agreement-gated-judge design from the LLM-as-judge reliability literature: no LLM label enters a headline number without a human-anchored κ gate.

## 3 Problem Definition

**Design constraint (operational).** For repository R, a constraint is evidenced by *change-inducing review events*: an in-line PR comment anchored to a diff hunk such that a later commit in the same PR modifies the anchored lines consistently with the comment's request. A candidate is promoted to a constraint only if semantically equivalent candidates recur in **≥3 distinct threads from ≥2 distinct reviewers and ≥2 distinct PR authors** within the mining window — recurrence separates a project norm from a one-off fix or one reviewer's taste. Explicit non-constraints: one-off defect reports, personal preference without recurrence, scope/process comments, and temporal/runtime obligations (routed to the trace-compliance line per §2e).

**Unwritten (operational).** A promoted constraint is *unwritten* iff `linter-expressible = false` (no existing configured rule id covers it, and no ≤20-line custom semgrep/ruff rule can) **and** `doc-mentioned = false` (no annotator can point to a doc sentence stating the rule at comparable specificity — excluding "handle errors gracefully"-grade platitudes). Headline unwrittenness claims use this conjunction; written-but-enforced cards are kept and flagged.

**Task 1 (mining).** Input: R's PR review corpus (threads, anchored hunks, follow-up commits, verdicts, merge status) plus R's formalized-rule surface (lint configs, docs). Output: a per-repository **constraint catalog** of cards (schema §4.4). Quality: human-audited precision, an independent recall proxy, unwrittenness rate.

**Task 2 (violation measurement).** Input: R's catalog; green-test agent patches for R's SWE-bench Verified tasks (public leaderboard submissions, ≥3 distinct scaffold/model families) and the matched human gold patches for the *same tasks*. Output: per-patch violation labels (card id, category, file:line, adjudication tier, rationale), aggregated into applicability-normalized per-category rates, agent vs human. Because every measured patch is verified green, every violation found is invisible to the test oracle — the paper's central sentence.

**Anti-circularity structure.** The catalog is mined from PRs in window W₁ (up to the SWE-bench task cutoff); violations are measured on agent patches for disjoint tasks; outcome linkage uses held-out *human* PRs from disjoint window W₂. Nothing the catalog is scored against was used to build it: the claim is that past review behavior predicts future acceptance behavior — an empirical claim, not a tautology.

## 4 Method

![Figure 1: Overview — review-history mining into validated constraint cards (left), gate-guarded validation instruments (center), and the tiered violation study on green-test agent vs matched human patches with outcome linkage (right).](architecture.svg)

*Figure 1: Pipeline overview. M1 harvests review threads and computes the change-inducing flag; M2 extracts candidate constraints with an LLM (keyword baseline in parallel); M3 clusters with entailment-checked merging, applies the ≥3/≥2/≥2 recurrence rule, and assigns written-status, category, and checkability. Validation instruments (precision audit with gate G1, cluster purity, recall proxy, judge gate G2) sit between the catalog and the violation study, which adjudicates green-test agent patches vs matched human gold in four tiers and feeds the outcome-linkage regression and the released card artifact (input contract for downstream checker evaluation, T5.3).*

### 4.1 Mining pipeline (M1–M3)

**M1 — Review-corpus collector.** GitHub GraphQL harvest per repo: threads at (repo, PR, thread, in-line comment, anchored hunk) granularity, joined with verdicts, merge status, and follow-up commits. The *change-inducing* flag — a later commit in the PR modifies the anchored lines (line-range overlap after diff-tracking through rebases) — is itself spot-checked on 100 threads. Window: last ~5 years per repo, recorded on every card to bound norm drift. Patches are aligned at the **first externally reviewable revision** (index revision), so agent first-shot output is never compared against human code already repaired through review (adopted from the autodiscussion draft).

**M2 — Constraint extractor.** A frozen, versioned LLM prompt maps each change-inducing comment (+ anchored hunk ± 20 lines) to `no_constraint` (one-off fix, question, praise, process comment, temporal/runtime obligation → routed out) or a candidate record {imperative statement, scope guess, trigger, provisional category, evidence link}. A **keyword/directive regex baseline** (should/must/never/avoid + code-element mentions) runs in parallel on identical input to bound the LLM's added value (paired thread-level McNemar).

**M3 — Catalog builder.** Candidate statements are sentence-embedded and clustered (HDBSCAN, cosine); clusters are LLM-merged into canonical cards, with merges accepted only where sampled within-cluster pairs survive a human *pairwise entailment* audit (an equivalence criterion adopted from the draft: two candidates are the same rule only if satisfying either satisfies the other under the same trigger). Admission requires threads ≥ 3 ∧ reviewers ≥ 2 ∧ authors ≥ 2; sub-threshold candidates are quarantined in the artifact, flagged. `written_status` is assigned by (a) mapping against the repo's configured lint-rule inventory plus the ≤20-line expressibility judgment and (b) doc search with annotator confirmation; a **tooling-enforcement probe** additionally records whether a configured check already fails on the card's violating example and passes on its conforming example. Category and checkability are dual-annotated by humans; the LLM's proposed checkability is retained separately as `checkability_pred` so its accuracy is itself measurable downstream.

### 4.2 Validation instruments (run before the violation study consumes the catalog)

1. **Card precision:** stratified n=300 (repos × categories × support), two SE-experienced annotators (not the prompt author), blind, verdict ∈ {genuine, spurious, ambiguous}; κ and Wilson CIs; **gate G1** on the first 100 (§5.3). One pre-committed codebook-revision cycle (pilot 50 → revise once → full 300); if κ < 0.4 persists on "genuine constraint," the paper pivots to a feasibility/negative result about the construct.
2. **Cluster purity:** n=150 within-cluster pairs, same-rule/different-rule; purity < 0.8 forces re-clustering.
3. **Recall proxy:** 50–100 held-out threads independently mined by annotators; report pipeline recovery fraction.
4. **Baseline comparison:** LLM vs keyword extractor, McNemar, α = 0.05.
5. **Blinding integrity** (adopted from the draft): annotators labeling patch-card pairs guess patch authorship after each label; the study reports balanced accuracy with a 95% CI and treats an upper bound > 0.60 as a blinding failure disclosed with the affected labels.

All disagreement data are released.

### 4.3 Violation study (M4) and outcome linkage

**Patch sets.** All green-test agent patches for pilot-repo tasks from the public SWE-bench experiments repository, from the 3–5 highest-volume distinct scaffold/model families (avoiding pseudo-replication of one model), target 300–500 after filtering, plus matched human gold patches for the same tasks. Within-task matching makes the agent-vs-human contrast immune to task-selection confounds.

**Applicability.** Cards match patches by scope globs + trigger predicates; ambiguity resolves conservatively to N/A; the matcher is spot-checked on 100 pairs. All rates use applicability denominators: rate = violated / applicable per (category, patch set) — a category can never look "most violated" merely because its cards apply most often.

**Tiered adjudication.** (i) *Mechanical/static:* semgrep/AST rules derived from `check_hint`; every rule carries a unit test built from the card's violating/conforming example hunks (must flag the former, pass the latter) plus a 10-sample human spot-check; failing rules are demoted to the LLM tier. (ii) *LLM judge*, agreement-gated **per category**: κ ≥ 0.6 vs dual human labels on n=400 (patch, card) pairs (~130 per category) before at-scale use — **gate G2**; the judge model comes from a different family than every evaluated agent; a category failing its gate is adjudicated by humans on a budgeted subsample and reported with wider uncertainty. (iii) *Human-only* cards: budgeted subsample, reported separately. Every reported violation carries its tier.

**Comparisons.** Per-category applicability-normalized rates, agent vs human gold, matched-pair McNemar per category with Holm–Bonferroni; per-repo and per-system (system × category) matrices, never pooled-only; chi-square for category non-uniformity.

**Outcome linkage (budgeted form).** On held-out human PRs from W₂: sample 150 PRs per first-round verdict class per repo; run only mechanical/static-tier cards (no new judge-validation debt); logistic regression of first-round outcome (approved vs changes-requested) on violation count with PR size, files touched, and author prior-merged-PR covariates; causal caveats stated. The claim is deliberately modest: the *mechanically checkable subset* of mined constraints predicts outcomes.

**Contamination note.** Agent training data may include the mined review threads; exposure biases agents *toward* compliance, so measured violation rates are a lower bound — strengthening the headline claim.

### 4.4 Constraint-card artifact (the downstream input contract)

```yaml
card_id: django-EH-0007
repo: django/django
statement: "Never catch bare Exception in ORM-layer code; catch the narrowest applicable subclass."
category: error_handling            # error_handling | arch_convention | api_convention | other
scope: {paths: ["django/db/**"], exclude: ["**/tests/**"]}
trigger: "diff adds an `except` clause"
checkability: static                # mechanical | static | llm | human_only
checkability_pred: static           # LLM-proposed value, kept for meta-evaluation
check_hint: "semgrep: except Exception: within django/db/"
support: {threads: 5, reviewers: 3, authors: 4, window: "2019-01..2024-06"}
evidence: [{pr: 14231, comment_url: "...", revision_commit: "abc123"}]
written_status: {linter_expressible: false, doc_mentioned: false, tooling_enforced: false}
examples: {violating_hunk: "...", conforming_hunk: "..."}
provenance: {extractor: "model+prompt v1.3", human_verified: true}
validation: {audit_round: 1, annotators: 2, verdict: genuine}
```

Fields the downstream checker study (T5.3) requires — `statement`, `scope`+`trigger`, `checkability`+`check_hint`, `examples`, `human_verified` — are first-class. Before release, a trivial reference checker (semgrep runner over `checkability=mechanical` cards) is executed end-to-end over every released card as a schema smoke test.

## 5 Experiment Design

### 5.1 Datasets and scale

- **Review corpora:** 5 SWE-bench Verified repos (candidates: django, scikit-learn, sympy, matplotlib, sphinx; final pick by W1 volume audit, threshold ≥2k change-inducing comments). Expected 10k–40k change-inducing comments through M2.
- **Patch corpora:** SWE-bench Verified tasks in those repos × green-test submissions from ≥3 agent systems → 300–500 agent patches + matched gold.
- **Held-out outcome set:** sampled human PRs from W₂ (150 per verdict class per repo) with first-round verdicts.
- **Breadth probe:** mining-only run on 2 non-Python review-heavy repos (one Rust, one TypeScript); catalog yield + 30-card precision spot-check; bounds the "Python-only pipeline" objection.

### 5.2 Metrics (pre-registered in W1)

| Metric | Definition | Target/Gate |
|---|---|---|
| Constraint yield | admitted cards per 1k change-inducing comments, per repo | descriptive |
| Extraction precision | sampled cards dual-judged genuine (Wilson CI, κ) | **G1: ≥0.5 raw on first 100; ≥0.7 on admitted cards for headline** |
| Recall proxy | annotator-found constraints recovered by pipeline | descriptive, CI |
| Unwrittenness rate | linter-expressible=false ∧ doc-mentioned=false | headline if majority |
| Judge validity | κ(judge, dual human) per category on n=400 | **G2: κ ≥ 0.6 per category** |
| Violation rate | applicability-normalized, category × system, agent vs gold (McNemar, Holm–Bonferroni) | headline |
| Outcome correlation | mechanical-tier violations → first-round verdict (logistic, covariates) | supporting |
| Baseline delta | LLM vs keyword extractor (McNemar) | supporting |
| Blinding integrity | balanced accuracy of authorship guesses | disclose if upper CI > 0.60 |

### 5.3 Go/no-go gates and descope ladder

- **G1 (end W2, ~Aug 28):** precision ≥ 0.5 on first 100 cards. Fail → one prompt/filter revision (≤4 days); fail again → pivot to feasibility/negative result or descope to repos where precision holds. No further spend before G1.
- **G2 (mid W4, ~Sep 11):** judge κ ≥ 0.6 per category; per-category human fallback otherwise.
- **G3 (end W5, ~Sep 18):** violation study complete on ≥300 patches, ≥3 systems; shortfalls reported with CIs, not hidden.
- **Descope ladder:** behind by Sep 11 → drop breadth probe; Sep 15 → move outcome linkage to future work; Sep 18 → reduce to 3 repos / 300 patches. The two headline claims (validated extraction; violation rates on green patches) are sacrificed last. Fallback venue if Oct 2 slips: FSE second cycle if offered, else ISSTA 2027 / ICSE 2028 with the Stage-2 scale-up (more repos/languages) folded in.

### 5.4 Milestones (working back from Oct 2; today Aug 13)

| Week | Dates | Deliverables |
|---|---|---|
| W1 | Aug 13–20 | Volume audit + repo pick; harvester running; card schema v0 frozen against T5.3 requirements; annotators calendar-committed (2 × ~45 h); pre-registration (metrics, gates, α); novelty sweep + citation verification checklist; intro/related-work drafting |
| W2 | Aug 21–28 | M2 on 2 repos; 100-card audit → **G1**; codebook revision if needed |
| W3 | Aug 28–Sep 4 | Full mining on 5 repos; clustering + catalog; dual annotation (300 cards + purity pairs); checker construction starts (needs only schema + early cards); breadth probe launched |
| W4 | Sep 4–11 | Catalog validation done (precision/recall/unwrittenness); mechanical rules + unit tests done; judge sample → **G2** |
| W5 | Sep 11–18 | Violation study at scale; outcome-linkage regression → **G3** |
| W6 | Sep 18–25 | Analysis freeze; figures; card artifact v1.0 + smoke test + handoff note; full draft |
| W7 | Sep 25–Oct 1 | Internal review, threats, artifact packaging (prompts, catalogs, labels, disagreements); submit Oct 2 |

Budget: no training; ~30k–80k LLM API calls (M2 + judge), low hundreds of USD; ~90 annotator-hours across W2–W5 with the annotation-critical path serialized (card audit strictly before judge validation).

### 5.5 Deferred to future work

The autodiscussion package's disposition/trajectory program — five-way closure decomposition, reviewer-engagement necessity replay, repository-held-out incremental disposition prediction (its RQ17–RQ21) — is methodologically attractive but requires in-the-wild provenance-verified agent-PR cohorts at a scale (10⁴ patches, thousands of annotator-hours) incompatible with this cycle. We retain its analytical goal in the budgeted outcome-linkage regression and name the full program as the natural extension once the card artifact exists.

## 6 Threats to Validity

**Construct.** Constraints are defined by reviewer enforcement; visibility bias means the catalog captures *reviewer-surfaced* norms only — a lower bound on the norm inventory, and a conservative one: agents are checked only against norms reviewers demonstrably enforce. CHANGES_REQUESTED confounds convention violations with scope/timing disagreements; verdicts enter only through the change-inducing filter at mining time and as the outcome variable with covariates in the linkage analysis. **Internal.** LLM extraction and judging are gated by human agreement (G1, G2, per-category); mechanical rules carry unit tests; blinding integrity is measured, not assumed. Author-experience confounding in outcome linkage is covaried and causally caveated. **External.** Claims are indexed to mature Python OSS; per-repo reporting throughout; the breadth probe bounds language dependence. Agent-system heterogeneity is reported per system generation. **Contamination.** Training exposure to mined threads biases toward compliance; measured rates are lower bounds.

## 7 Conclusion

Passing tests is no longer the bottleneck for coding agents; being acceptable to the humans who own the code is. We turn the record of that acceptance process — change-inducing review comments and the revisions that satisfied them — into the first validated, repository-level catalogs of unwritten design constraints, measure how often green-test agent patches violate them relative to matched human work, and test whether those violations predict real review outcomes. The instrument, gates, and released card artifact are designed so that every headline number is anchored to a human-audited quantity, and so that automated checker evaluation can consume the catalogs directly.

## References

- Bacchelli, A., Bird, C. Expectations, Outcomes, and Challenges of Modern Code Review. ICSE 2013.
- Sadowski, C. et al. Modern Code Review: A Case Study at Google. ICSE-SEIP 2018.
- Bosu, A. et al. Characteristics of Useful Code Reviews. MSR 2015.
- Allamanis, M., Barr, E.T., Bird, C., Sutton, C. Learning Natural Coding Conventions (NATURALIZE). FSE 2014.
- Bader, J. et al. Getafix: Learning to Fix Bugs Automatically. OOPSLA 2019.
- Amann, S. et al. MUBench (MSR 2016); MUDetect (ESEC/FSE 2019).
- Li, Z. et al. Automating Code Review Activities by Large-Scale Pre-training (CodeReviewer). ESEC/FSE 2022.
- Jimenez, C.E. et al. SWE-bench: Can Language Models Resolve Real-World GitHub Issues? ICLR 2024.
- Aleithan, R. et al. SWE-Bench+: Enhanced Coding Benchmark for LLMs. arXiv:2410.06992.
- METR. Many SWE-bench-Passing PRs Would Not Be Merged into Main. METR research note, 2026-03-10.
- Anonymous. Does Pass Rate Tell the Whole Story? Evaluating Design Constraint Compliance in LLM-based Issue Resolution. arXiv:2604.05955, 2026.
- Anonymous. A First Look at Coding Agents' Compliance with AI Contribution Rules in Open-Source Communities (RepoComplianceBench). arXiv:2607.26819, 2026.
- AgentLTL: temporal-logic compliance checking of agent executions. arXiv:2607.02599, 2026.
- MANTRA: trace-level workflow compliance for coding agents. arXiv:2605.06334, 2026.
- Dong et al. From Correctness to Collaboration. arXiv:2512.23844.
- Watanabe, M. et al. On the Use of Agentic Coding: An Empirical Study of Pull Requests on GitHub. arXiv, 2025.
- Peralta, S.R.O. et al. Why Are Agentic Pull Requests Merged or Rejected? arXiv:2605.22534, 2026.
- Patel, S. et al. Is Agent Code Less Maintainable Than Human Code? arXiv:2606.21804, 2026.
- Banik, D. et al. All Smoke, No Alarm: Oracle Signals in Agent-Authored Test Code. arXiv:2606.18168, IEEE AITest 2026.
- Sawada, S. et al. To What Extent Does Agent-generated Code Require Maintenance? arXiv:2605.06464, 2026.
- Zhang, Z. et al. Still Manual? Automated Linter Configuration via DSL-Based LLM Compilation of Coding Standards (LintCFG). 2026.
- Khan, T.I. et al. A Survey of Code Review Benchmarks and Evaluation Practices. 2026.
- Zhang, X. et al. Pull Request Decisions Explained: An Empirical Overview. IST.
- Lenarduzzi, V. et al. Does Code Quality Affect Pull Request Acceptance? An Empirical Study.
