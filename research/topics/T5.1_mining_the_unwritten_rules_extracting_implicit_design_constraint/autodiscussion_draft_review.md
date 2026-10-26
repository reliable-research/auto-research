# Review of Autodiscussion Draft Package — T5.1 (Mining Implicit Design Constraints from Review History)

Reviewed: 2026-08-13. Inputs: `paper-draft.md` (99 KB), `experiment-spec.md` (41 KB), `research-report.md` (211 KB) in
`/data/wangjian/wj_code/paper_autodiscussion/completed_jobs_dirs/ZT5.1 Mining Implicit Design Constraints from Review History--1f4b556b/`,
audited against `discussion.md` (2026-08-13 revision) in this topic directory. Room closed with 3 unresolved MAJOR critiques (inferred in §6).

---

## 1. Architecture of the draft (~10 lines)

The draft proposes a three-module empirical framework. **Module 1 (Mine Auditable Constraint Cards)** links each review
comment to the revision hunk that resolved it, LLM-encodes the pair as a structured proposition (trigger + required
postcondition), clusters propositions by human-judged bidirectional entailment, requires breadth (≥3 PRs, ≥2 reviewers,
≥2 context cells), assigns least-general path-glob scopes, an operational checkability class (machine-static /
machine-dynamic / human-judgment) with executable "certificates," and a repository-tooling probe marking already-enforced
norms. **Module 2 (Measure Matched Patch Violations)** applies pre-PR-active cards to first-reviewable green-test agent
patches and propensity-matched human patches, with blinded double annotation, blinding-integrity audits, certificate
secondary audits, objection-coverage audits, and architectural stratification. **Module 3 (Link Violations to Merging)**
fits hierarchical five-way disposition models (merge / technical closure / administrative closure / withdrawal /
unclassified), trajectory reconstruction with "necessity replay" of reviewer repairs, and repository-held-out incremental
prediction. The evaluation enumerates 21 RQs over five cohort corpora (up to 40 repos, 14,000 patches, 24,000
double-coded applications). The methodological core is faithful to discussion.md's idea; the evaluation superstructure is not.

## 2. Novelty ledger

Verified with WebSearch on 2026-08-13 (queries: mining code review comments design rules; implicit coding conventions
LLM unwritten rules; agent patches pass tests violate repository conventions; "Many SWE-bench" would not be merged;
"All Smoke, No Alarm"; "Is Agent Code Less Maintainable"; PR review history mining constraint catalog 2026).

| # | Claim | Nearest prior | Delta | Stance |
|---|-------|--------------|-------|--------|
| C1 | Recurrent review-comment→resolving-hunk pairs can be mined into validated, scoped, provenance-bearing per-repo constraint cards | **arXiv 2604.05955, "Does Pass Rate Tell the Whole Story? Evaluating Design Constraint Compliance in LLM-based Issue Resolution" (Apr 2026)** — mines and validates 1,787 design constraints from real-world PRs across 6 SWE-bench-aligned repos; LLM-based compliance verification | 2604.05955 mines *per-issue* constraints (aligned to specific SWE-bench tasks) and validates via LLM; T5.1 mines *repo-level recurrent* catalogs from change-inducing review dialogue with behavioral evidence (author complied), recurrence thresholds (≥3 threads/≥2 reviewers/≥2 authors), human-audited precision with κ, and an unwrittenness measurement against the repo's lint/doc surface. **The draft does not cite this paper — a reviewer who knows it kills the current framing.** Delta survives but must be stated defensively. | **NOVELTY AT RISK — reframe required, not fatal** |
| C2 | Green-test agent patches violate mined constraints at a higher rate than matched human patches, and violations predict merge outcomes | (a) 2604.05955: "fewer than half of functionally correct patches satisfy design requirements" — but no agent-vs-human contrast, no per-repo catalogs, no merge-outcome linkage (verified via abstract fetch); (b) METR, *Many SWE-bench-Passing PRs Would Not Be Merged into Main* (2026-03-10): maintainer decisions ~24 pp below grader — motivation, no mechanism; (c) All Smoke No Alarm (2606.18168): oracle strength → merge OR=1.28, tests only | Agent-vs-matched-human contrast on *mined per-repo* constraints + held-out merge-outcome correlation is unclaimed territory; (a) has neither contrast nor outcome linkage; (b)(c) have outcomes but no constraint instrument | **NOVEL (defensible)** |
| C3 | Artifact-level design conformance is distinct from trace-level procedural compliance | AgentLTL (2607.02599), MANTRA (2605.06334) — verify *trace-level* compliance of agent execution against procedural specs; RepoComplianceBench (2607.26819) — compliance with *written* contribution rules (AGENTS.md/CONTRIBUTING) | T5.1 checks *artifact-level* (patch text) conformance to *unwritten* norms mined from review dialogue; the draft **never states this boundary** although discussion.md mandates it (ZV9/procedural-cluster routing rule) | **NOVEL but boundary paragraph missing from draft** |
| C4 | Rule induction from review *dialogue* rather than code alone | NATURALIZE (FSE 2014), Getafix (OOPSLA 2019), MUDetect (ESEC/FSE 2019) — induce rules from code/edits, not reviewer rationale | Review dialogue carries norms with no code-regularity signature (layering, error-handling policy); draft omits this entire prior line, weakening its own positioning | NOVEL, but related-work group (c) of discussion.md was dropped |

## 3. Consistency vs discussion.md — silent scope changes (the known failure signature, confirmed)

Zero confabulated citations (see §4) **but severe silent scope inflation** — the exact pattern found in sibling reviews:

1. **Budgets inflated 10–100×.** discussion.md: 5 SWE-bench Verified repos, 300–500 agent patches, n=300 card audit,
   n=400 judge-validation pairs, ~90 annotator-hours, low-hundreds USD. Draft: ≥20–40 repos, 1,200 held-out cards (RQ1),
   4,000 matched patches / 2,000 pairs (RQ3/RQ7), **14,000 patches / 7,000 provenance-verified pairs (RQ8/RQ13)**,
   6,000 double-coded applications (RQ9), a **24,000-application double-coded pool** (RQ14/16), 12,000-patch disposition
   cohort (RQ17), 5,000 trajectory-complete patches with per-violation "necessity replay" (RQ19–21). Double-coding
   24,000 applications alone is on the order of 2,000+ annotator-hours — ~25× the committed budget.
2. **Pilots and gates dropped.** G1 (100-card precision gate, ~Aug 28), G2 (per-category judge κ ≥ 0.6), G3, the
   descope ladder with trigger dates, the two-bar precision semantics (0.5 continue / 0.7 publishable), and the entire
   W1–W7 milestone plan to Oct 2 are all absent. The draft's "gates" are estimand-qualification gates, not
   schedule-feasibility gates.
3. **Measurement substrate silently swapped.** discussion.md: green-test patches = public SWE-bench Verified leaderboard
   submissions + matched human gold patches (data that exists today). Draft: in-the-wild agent PRs with immutable
   authorship provenance, CI-verified test status on the exact index revision, reconstructible pre-review revisions, at
   7,000 pairs — a dataset that does not exist and cannot be built in 7 weeks; it also reintroduces the task-selection
   confounds the within-task SWE-bench design was chosen to avoid.
4. **Headline claims dropped:** the unwrittenness rate (linter-expressible ∧ doc-mentioned test) survives only as a
   diluted "tooling probe" (config-only, no doc-mention test); the three-category taxonomy (error handling /
   architectural convention / API convention) — the seed question of README.md — is gone; the keyword/directive
   non-LLM extraction baseline is replaced by LLM-only ablations; the constraint-card schema as **T5.3's input
   contract** (checkability stratification, `check_hint`, smoke-test) is never mentioned; the ZV9/procedural-compliance
   boundary paragraph mandated by Stage 3 is absent.
5. **Genuine improvements to keep:** first-reviewable-revision (index-revision) alignment; blinding-integrity audit with
   the 0.60 balanced-accuracy upper bound; objection-coverage (differential circularity) audit; tooling-enforcement
   stratification; five-way disposition decomposition (a sharper version of discussion.md's verdict-noise concern);
   entailment-based clustering as an upgrade over embedding-only dedup.

## 4. Citation audit (load-bearing set)

| Citation (as used in draft) | Status |
|---|---|
| METR, *Many SWE-bench-Passing PRs Would Not Be Merged into Main* (2026) | **CONFIRMED** — METR research note 2026-03-10 (not arXiv); ~24 pp gap; also resolves discussion.md's [VERIFY] on the METR figure |
| Jimenez et al., SWE-bench (ICLR 2024) | **CONFIRMED** |
| Aleithan et al., SWE-Bench+ | **CONFIRMED** (arXiv 2410.06992) |
| *All Smoke, No Alarm* (2026) | **CONFIRMED** — arXiv 2606.18168, IEEE AITest 2026; 80.2% weak/no oracle; OR 1.28 |
| Patel et al., *Is Agent Code Less Maintainable Than Human Code?* | **CONFIRMED** — arXiv 2606.21804; resolve-rate drop up to 13.1% |
| Watanabe et al., *On the Use of Agentic Coding* | **CONFIRMED** (2025 arXiv; 567 Claude Code PRs, 83.8% acceptance, 45.1% revised) |
| Peralta et al., *Why Are Agentic Pull Requests Merged or Rejected?* | **CONFIRMED** — arXiv 2605.22534; 35.7% clear agentic failures |
| Sawada et al., agent-code maintenance | **CONFIRMED** — arXiv 2605.06464 |
| Li et al., CodeReviewer (ESEC/FSE 2022) | **CONFIRMED** |
| Zhang et al., *Pull Request Decision(s) Explained* | **CONFIRMED** (IST 2022/2023 line) |
| Lenarduzzi et al., code quality vs PR acceptance | **CONFIRMED** (2019/2021) |
| Allamanis et al. (NATURALIZE) | **MISFORMATTED** in research-report ("Miltiadis Allamanis et al.. Earl T..") — real paper (FSE 2014), citation string must be repaired |
| Rahman & Shihab; Chatlatanagulchai (Agent READMEs); Khan survey; Minh review-effort; Zhang LintCFG; Peng optimization; Paul smells | **PLAUSIBLE-CONFIRMED** (abstracts present in research-report; not independently re-verified; none load-bearing) |
| **NOT CITED but must be:** arXiv 2604.05955 (Does Pass Rate Tell the Whole Story), arXiv 2607.26819 (RepoComplianceBench), AgentLTL 2607.02599, MANTRA 2605.06334 | **MISSING — the 2026 nearest neighbors** |

Verdict on the confabulation axis: **zero fabricated citations**; failure mode is omission, not invention — matching the sibling signature.

## 5. Gap to implementation (FSE 2027, submission Oct 2 — 7 weeks)

- The draft as written is **unimplementable by Oct 2 by roughly an order of magnitude**: 21 RQs, five disjoint cohort
  corpora, thousands of annotator-hours, provenance-verified in-the-wild agent-PR harvesting at 7,000-pair scale,
  per-violation counterfactual "necessity replay," archived per-repo tooling execution environments. discussion.md's own
  plan (5 repos, ~90 annotator-hours, gates + descope ladder) was already labelled "tight but viable"; the draft
  multiplies every number without adding time.
- The experiment-spec concedes it: "The agent does **not** run the study (no live repos, annotators, or agent PRs are
  supplied)" — i.e., the package specifies software, not a study that can produce numbers by the deadline.
- Recoverable core within 7 weeks (= discussion.md's plan, upgraded with the draft's best mechanisms): SWE-bench
  Verified substrate, 5 repos, 300–500 patches, index-revision alignment, entailment-aware clustering, blinding audit,
  tooling-enforcement flag, G1/G2/G3 gates, descope ladder. RQ17–RQ21 (disposition/trajectory modeling) must move to
  future work; outcome linkage survives only in discussion.md's budgeted form (mechanical-tier cards over sampled
  held-out human PRs).

## 6. Verdict + top-3 fixes (and the 3 inferred unresolved MAJORs)

**Verdict: MAJOR REVISION — sound core mechanism, wrong scale, unprotected novelty.** The draft independently
reinvented several good instruments but silently discarded the feasibility scaffolding and the 2026 threat model that
made T5.1 KEEP-TOP.

Inferred unresolved MAJORs from the closed room:
- **MAJOR-1 (feasibility/scope):** evaluation plan inflated 10–100× vs the committed budget with all schedule gates and
  the descope ladder dropped; not executable before Oct 2.
- **MAJOR-2 (novelty exposure):** 2026 nearest neighbors missing — above all arXiv 2604.05955, plus
  RepoComplianceBench and the AgentLTL/MANTRA trace-vs-artifact boundary — leaving both headline claims unpositioned.
- **MAJOR-3 (estimand drift):** substrate swapped from SWE-bench-Verified matched pairs to unobtainable in-the-wild
  provenance-verified PR pairs, and the discussion.md headline deliverables (unwrittenness rate, category taxonomy,
  keyword baseline, T5.3 card contract) dropped.

Top-3 fixes (applied in `paper-draft.revised.md`):
1. **Restore the discussion.md experiment frame** (5 repos, 300–500 green SWE-bench patches + human gold, n=300 audit,
   per-category judge gate, G1–G3 + descope ladder, W1–W7 plan), keeping the draft's index-revision alignment,
   entailment clustering, blinding audit, objection-coverage audit, and tooling-enforcement stratification; demote
   disposition/trajectory modeling (RQ17–21) to future work and keep outcome linkage in its budgeted mechanical-tier form.
2. **Add the missing related-work groups and the boundary paragraph**: 2604.05955 (concede-and-differentiate: per-issue
   LLM-validated constraints vs recurrent human-audited per-repo catalogs + agent-vs-human contrast + outcome linkage),
   RepoComplianceBench (written vs unwritten rules), AgentLTL/MANTRA (trace-level procedural vs artifact-level design
   conformance), and the code-history rule-induction line (NATURALIZE/Getafix/MUDetect).
3. **Reinstate the dropped deliverables**: unwrittenness headline (linter-expressible ∧ doc-mentioned, on top of the
   draft's tooling probe), the three-category taxonomy with dual annotation, the keyword/directive baseline, and the
   versioned constraint-card schema as T5.3's smoke-tested input contract.
