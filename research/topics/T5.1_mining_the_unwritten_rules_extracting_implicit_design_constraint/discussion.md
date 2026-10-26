# Discussion: T5.1 — Mining the Unwritten Rules: Extracting Implicit Design Constraints from Code Review History

> Auto-research-discussion document, 6 stages, each with an internal critic→refine pass.
> Seed: `README.md` (code T5.1, label [证据], parent topic "T5. 设计约束合规（coding agent）").
> Scaffolding inherited from `digest.md` (reverse digest, N0–N12); this document supersedes the
> digest where the two disagree.
>
> **Audit context (binding for this document):** T5.1 is KEEP-TOP and the lead of the
> execution-oracle cluster. Target venue: **FSE 2027, submission deadline Oct 2, 2026** (~7
> weeks from today, 2026-08-13). It attacks the production-measured acceptance gap: agent PRs
> pass tests but fail human acceptance — METR reports agent-PR merge rates at roughly half the
> human rate [VERIFY: channel-relayed, locate the primary METR report before citing], and Faros
> telemetry reports 31.3% of agent PRs merged with zero review while the defect rate rises from
> 9% to 54% [VERIFY: channel-relayed, both figures need the primary Faros source]. Ground truth
> comes from historical human review verdicts (真值 = 人类评审裁决) on existing PR corpora — no
> new production deployment is required. Sibling **T5.3** (automated constraint-checker
> precision/recall vs human review) is ON HOLD and explicitly downstream: T5.1's constraint-card
> artifact is T5.3's primary input, so the card schema is a first-class deliverable here, not an
> afterthought.

---

## Stage 1 — Problem Definition

### 1.1 What is a "design constraint," operationally?

A **design constraint** for repository R is a *recurring, prescriptive, generalizable
expectation about how code in R should be written*, which is (a) enforced by human reviewers in
practice but (b) not encoded in any machine-checkable or documented artifact of R (tests, lint
configuration, type checker, CI scripts, CONTRIBUTING/style docs). "Enforced in practice" and
"not written down" are both given behavioral, checkable operationalizations:

- **Enforced in practice (the extraction signal).** A constraint candidate is evidenced by a
  *change-inducing review event*: an in-line PR review comment anchored to a diff hunk, such
  that a later commit in the same PR modifies the anchored lines in a way consistent with the
  comment's request. The comment text + anchored hunk + revision diff jointly witness that a
  reviewer expressed an expectation and the author complied. A candidate is promoted to a
  *constraint* only if semantically equivalent candidates recur in **≥ 3 distinct threads from
  ≥ 2 distinct reviewers** within the mining window. Recurrence is what separates a project
  norm from a one-off bug fix or a single reviewer's taste.
- **Not written down (the "unwritten" filter).** For each promoted constraint we check
  expressibility against R's own formalized surface: the repo's lint/style configuration
  (ruff/flake8/pylint/clang-format/eslint as applicable), type-checker configuration, and
  documented guidelines (CONTRIBUTING.md, docs/dev). Constraints expressible there are kept but
  flagged `written=true` and excluded from the headline "unwritten" claims; the paper's subject
  is the `written=false` majority [prediction, to be measured].

The three seed categories (错误处理/架构惯例/API 约定 — error handling / architectural
convention / API convention) plus an `other` escape category form the initial taxonomy;
categorization is dual-annotated and reliability-checked (Stage 5), never assumed.

### 1.2 The mining task (task 1)

- **Input:** R's historical PR review corpus: threads (in-line comments, anchored hunks),
  follow-up commits, review verdicts (APPROVED / CHANGES_REQUESTED), merge status; plus R's
  source tree and formalized-rule surface (lint configs, docs) at mining time.
- **Output:** a per-repository **constraint catalog**: a set of *constraint cards* (schema in
  Stage 4/SP4), each card carrying a normalized imperative rule statement, scope, trigger,
  category, checkability class, support counts, and evidence links to the source threads.
- **Quality measures:** extraction precision (human audit of sampled cards: is this a genuine,
  generalizable project constraint?), a recall proxy (constraints human annotators find in
  held-out threads that the pipeline recovers), and unwrittenness rate.

### 1.3 The violation-measurement task (task 2)

- **Input:** a constraint catalog for R; a set of **green-test patches** for tasks in R —
  agent-generated patches that pass the project's full test suite (e.g., resolved SWE-bench
  Verified instances from public leaderboard submissions) — and the matched human gold patches
  for the same tasks.
- **Output:** per-patch violation labels — the set of violated card ids, each with category,
  localization (file:line), adjudication tier (mechanical / static-analysis / LLM-judge /
  human), and rationale — aggregated into per-category violation rates for agents vs humans.
- **Ground truth:** human review verdicts, in two roles: (i) historically, verdicts + revision
  diffs are what the catalog is mined from; (ii) for validation, sampled violation labels are
  audited by human annotators, and (iii) on held-out *human* PRs with known outcomes, we test
  whether catalog violations predict CHANGES_REQUESTED vs APPROVED (the merge-outcome
  correlation, Stage 6).

**Critic:** Four attacks. (1) *Circularity risk*: constraints are defined as "what reviewers
enforce," and violations are validated against "what reviewers demand" — is the measurement
tautological? (2) *The change-inducing filter is too generous*: most change-inducing comments
are one-off bug fixes; recurrence ≥3 threads helps, but semantic deduplication (which decides
what "recurs") is itself an LLM step, so the promotion rule launders extraction noise into
apparent recurrence. (3) *"Unwritten" is underspecified*: docs coverage is fuzzy — a
CONTRIBUTING.md sentence like "handle errors gracefully" arguably "writes down" half the
error-handling category; expressibility needs a strict operational test or the headline claim
is unfalsifiable. (4) *Verdict noise*: CHANGES_REQUESTED confounds convention violations with
scope/timing/design disagreements; using it as 真值 without decomposition overclaims. Also, the
definition should say explicitly what a constraint is *not* (personal preference, one-off fix,
temporal/runtime obligation — the ZV9 boundary belongs partly here).

**Refined:** (1) Circularity is broken structurally by **temporal and population splits**: the
catalog is mined from PRs in window W₁ (e.g., up to the SWE-bench task cutoff); violations are
measured on *agent patches for disjoint tasks*, and the merge-outcome correlation uses
*held-out human PRs* from window W₂ disjoint from W₁. Nothing the catalog is scored against was
used to build it. The claim is generalization: past review behavior predicts future acceptance
behavior — an empirical claim, not a tautology. (2) The promotion rule is tightened: recurrence
counts only clusters whose *pairwise* semantic-equivalence judgments survive a human audit on a
stratified sample (cluster-purity audit, Stage 5), and support counts require ≥2 distinct
reviewers *and* ≥2 distinct PR authors (so one author's repeated mistake corrected by one
reviewer does not fabricate a norm). (3) "Unwritten" gets a two-level operational test:
`linter-expressible` (an existing rule id in the repo's configured linters, or a writable
semgrep/ruff-custom rule of ≤ ~20 lines, covers it — mechanically checkable) and
`doc-mentioned` (an annotator can point to a specific doc sentence that states the rule at
comparable specificity — the specificity qualifier excludes "handle errors gracefully"-grade
platitudes). Headline claims use `linter-expressible=false ∧ doc-mentioned=false`. (4) We do
not use raw CHANGES_REQUESTED as constraint ground truth; the verdict enters only (a) filtered
through the change-inducing + recurrence pipeline at mining time and (b) as the *outcome*
variable in the correlation analysis, where confounding is acknowledged and partially handled
(Stage 6). Explicit non-constraints: one-off defect reports, personal preference without
recurrence, scope/process comments ("split this PR"), and **temporal/runtime obligations over
tool-call or API event sequences (deferred to the ZV9 line — boundary statement in Stage 3)**.

---

## Stage 2 — Motivation

### 2.1 The acceptance gap is the binding constraint on coding agents

The current generation of coding agents has largely saturated the *test oracle*: on
SWE-bench-style benchmarks, frontier agents produce green-test patches for a large fraction of
tasks. Yet in production the *acceptance* oracle — a human maintainer merging the PR — tells a
different story: METR reports agent-PR merge rates at roughly half the human baseline [VERIFY:
channel-relayed], and Faros telemetry indicates 31.3% of agent PRs are merged with zero human
review, with defect rates rising from 9% to 54% in that channel [VERIFY: channel-relayed; both
numbers must be traced to primary sources before any use in the paper — until verified they are
motivation-context only, never load-bearing]. Whatever the exact numbers, the direction is
consistent and production-measured: **passing tests is no longer the bottleneck; being
acceptable to the humans who own the code is.** The delta between "tests pass" and "humans
accept" is precisely the region where unwritten design constraints live — error-handling norms,
layering rules, API conventions that no test exercises. T5.1 is the evidence-producing
([证据]) lead of the execution-oracle cluster because it measures that delta directly and
produces the artifact (constraint cards) that the rest of the cluster (T5.3 checker, T5.5
compliance-utility frontier) consumes.

### 2.2 Why review history is the right truth source

Three properties make historical code review the uniquely good substrate:

1. **It already exists at scale.** Mature OSS projects carry 10⁴–10⁵ review comments with
   anchored diffs, revisions, and verdicts — no new deployment, no new labeling campaign for the
   raw signal. This is what makes an FSE-timeline empirical study feasible at all.
2. **It is behaviorally validated at the source.** A change-inducing comment is not an opinion
   about what reviewers *say* they want (surveys, interviews, agent-rule files); it is a record
   of an expectation that was *actually enforced* — the author changed the code. This is
   stronger evidence of a real norm than any stated-preference source.
3. **It is the same oracle we ultimately care about.** The acceptance gap is defined by human
   review verdicts; mining the constraints from the very process that produces those verdicts
   means the catalog is, by construction, about merge-relevant expectations — not about
   abstract code quality.

### 2.3 Why now

(a) Agent PR volume makes the acceptance gap an operational cost today, not a projection;
(b) test-oracle benchmarks are saturating, so the field needs the *next* oracle, and several
groups are circling convention-adherence qualitatively (e.g., taxonomy work like *From
Correctness to Collaboration*, arXiv:2512.23844) without a quantitative per-repo instrument —
the measurement niche is open but will not stay open past ~2027; (c) LLM extraction quality
crossed the threshold where mining semantic rules from informal dialogue is plausible, provided
extraction validity is independently established (the SP1 concern); (d) downstream demand is
concrete and internal: T5.3 is blocked on exactly this artifact.

**Critic:** (1) The two production figures are channel-relayed and one of them (Faros
9%→54%) is on a *zero-review* channel — which, note, is a channel where review-derived
constraints were *not* enforced; citing it as evidence that constraint violations block
acceptance is actually citing evidence about what happens when review is absent. Do not let the
narrative depend on either figure. (2) The acceptance gap has multiple causes — trust in
authorship, PR scope/churn, provenance bias against bots, missing context — and constraint
violations are only one slice; the motivation must not imply constraints explain the whole
merge-rate delta. (3) "Review history is the right truth source" needs a concession: review
records are biased toward what reviewers *notice* and *bother to write*; silent norms enforced
by author self-selection never appear. (4) "Why now" point (b) asserts a closing niche without
evidence.

**Refined:** (1) The paper's introduction uses the production figures only as [VERIFY]-gated
context ("production telemetry suggests…"), and the Faros zero-review figure is reframed
correctly: it bounds the *cost of absent review* (what agents do when unreviewed), which
motivates having a machine-checkable proxy for review — i.e., it motivates the *artifact*, not
the violation measurement. The load-bearing motivation is internal and verifiable: the
merge-outcome correlation (Stage 6) tests, within our own data, whether catalog violations
predict negative verdicts. If that correlation is null, the paper honestly reports that mined
constraints do not explain acceptance — still a publishable [证据] result given the measurement
is validated. (2) Scoping sentence added to the motivation: "We measure one candidate mechanism
of the acceptance gap — implicit-constraint violation — and quantify its share, not the whole
gap." The correlation analysis is what converts "one slice" from hand-waving into an estimated
effect size. (3) Concede the visibility bias as a scope limitation (mined catalog =
*reviewer-surfaced* norms, a lower bound on the norm inventory) and note it biases the
violation measurement *conservatively* — agents are checked only against norms reviewers
demonstrably enforce. (4) Soften (b) to the observable facts: the taxonomy-level neighbors
exist and are qualitative; no published work provides per-repo, quantitative,
violation-rate-on-green-patches measurement [VERIFY via the Stage-3 fresh literature sweep
before submission].

---

## Stage 3 — Related Work

Five groups, nearest first. Corpus grounding inherited from `digest.md` N3 (the local
OpenReview corpus is ML-skewed — one code-review paper in 11,683 — so the MSR/FSE literature
below is cited from general knowledge; every entry marked [VERIFY] must be bibliographically
confirmed via ACM DL/IEEE Xplore before submission, and a dedicated fresh sweep for 2025–2026
"agent PR review / convention compliance" work is mandatory given the topic's heat).

**(a) Empirical foundations of code review.** Bacchelli & Bird, *Expectations, Outcomes, and
Challenges of Modern Code Review* (ICSE 2013) — review's dominant outcomes include convention
enforcement and knowledge transfer, not just defects; Sadowski et al., *Modern Code Review: A
Case Study at Google* (ICSE-SEIP 2018) — reviews as norm-enforcement and education at scale;
Bosu et al., *Characteristics of Useful Code Reviews* (MSR 2015) — usefulness taxonomy of
review comments. These establish that the phenomenon (norms enforced through review) is real
and central, but produce human-readable taxonomies, not machine-applicable per-repo rule
inventories checkable against unseen patches.

**(b) Automating review activities.** Tufano et al., *Towards Automating Code Review
Activities* (ICSE 2021) and follow-ups [VERIFY exact titles/venues]; Li et al., *Automating
Code Review Activities by Large-Scale Pre-Training* (CodeReviewer, ESEC/FSE 2022); AUGER
(review-comment generation, ESEC/FSE 2022) [VERIFY]; LLaMA-Reviewer (ISSRE 2023) [VERIFY];
DefectCR-style defect-focused LLM review (OpenReview:mEV0nvHcK3). All learn diff→comment
mappings or generate findings per merge request; convention knowledge stays latent in weights,
no persistent, auditable constraint artifact is distilled, and defect-focused work explicitly
*deprioritizes* convention/style ("nitpicks") — the exact slice T5.1 targets.

**(c) Convention & rule induction from code history.** Allamanis et al., NATURALIZE (FSE 2014)
— learns naming/formatting conventions from a codebase and suggests convention-conforming
changes; Bader et al., Getafix (OOPSLA 2019) — learns recurring fix patterns from past fixes;
Rolim et al., REVISAR (learning quick-fix rules from code edits) [VERIFY venue/year]; API-misuse
detection lines: Amann et al., MUBench (MSR 2016) / MUDetect (ESEC/FSE 2019); classic spec
mining: Ammons et al. (POPL 2002), Daikon invariant detection (Ernst et al.). These induce
rules from *code or edits alone* — surface-level (naming, formatting), pattern-level (fix
templates, API call patterns), or invariant-level — but not from the *review dialogue*, so they
cannot capture norms whose evidence is a reviewer's stated rationale rather than a code
regularity (e.g., layering rules, "don't catch bare Exception at this boundary"), and none
measures agent compliance.

**(d) Agent evaluation beyond tests.** SWE-bench (ICLR 2024, OpenReview:VTF8yNQM66) — the
test-oracle benchmark whose green patches are our measurement substrate; SWE-Lancer
(OpenReview:xZXhFg43EI) — concedes unit tests under-capture full-system expectations; *From
Correctness to Collaboration* (Dong et al., arXiv:2512.23844) — the nearest thesis-level
neighbor: a 15-behavior taxonomy (incl. "Adhere to Standards and Processes") mined from
enterprise agent-rule files + interviews. Concede-and-differentiate (per digest N4.7): they
share the "correctness-only evaluation misses what matters" thesis and validate their taxonomy
against humans; but they mine *static, already-written-down* rule files and stated preferences,
cross-company and qualitative — no per-repo catalogs, no support counts, no violation *rates*
on green-test patches, no merge-outcome linkage. T5.1's deltas: dynamic review-dialogue
substrate, behavioral (change-inducing) evidence, quantitative agent-vs-human violation
measurement, and a checker-consumable card artifact.

**(e) Boundary statement vs ZV9 (Temporal Contract Mining, job `ZV9_…--1093b439`).** ZV9 mines
**temporal tool-call contracts** — behavioral obligations over *event sequences in agent
execution trajectories* (order, timing, entity association), grounded in API documentation and
business specifications of varying normative authority, checked by trace conformance with
explicit decidability states, and compiled into *runtime supervision rules*. Its intellectual
substrate is specification/process mining (LTL learning, conformance checking over uncertain
logs, declarative-constraint mining à la Rebmann et al.). T5.1 is disjoint on every axis that
matters: **substrate** (human review dialogue about code diffs vs execution/event logs),
**constraint semantics** (static properties of source code and its structure — error-handling
form, layering, API usage conventions in the code text — vs temporal ordering obligations over
runtime events), **evidence type** (change-inducing review comments + revision diffs vs trace
satisfaction/violation witnesses), **oracle** (human review verdicts vs trace conformance
semantics), and **consumer** (T5.3's static patch checker vs a runtime monitor). The shared
shape is only the abstract "mine candidate rules, then check violations." Explicit
non-collision rule, to be stated in both papers: *any T5.1 candidate whose natural statement is
a temporal obligation over runtime/tool-call events is out of T5.1 scope and routed to the ZV9
line; any ZV9 contract candidate whose evidence is review-dialogue text rather than
documentation or traces is out of ZV9 scope.* The two artifacts are complementary layers of an
agent-oversight stack (static design compliance vs runtime behavioral compliance) and neither
subsumes the other.

**Critic:** (1) Group (c) is the danger zone for a "method twin": review-comment *mining* for
rules specifically may already exist — e.g., work on extracting reviewer intents, tacit
knowledge extraction from review threads, or "review comment → static analysis rule" induction;
the current list names no such work, which means the sweep hasn't been done, not that it
doesn't exist. A reviewer who knows one such paper kills the novelty claim. (2) Too many
[VERIFY] tags for a KEEP-TOP topic seven weeks from deadline — the verification pass must be
scheduled, not aspirational. (3) The ZV9 boundary is well-drawn but currently lives only in
internal documents; if both papers submit, the boundary sentence must actually appear in the
T5.1 related-work text. (4) Missing group: LLM-judge validity literature (the audit penalizes
unvalidated LLM judges), which Stage 4/SP1 depends on — cite the judge-reliability line (e.g.,
"LLM-as-judge" bias/agreement studies [VERIFY specific works]) to show the validation design is
informed.

**Refined:** (1) Add a mandatory pre-submission **novelty sweep** (owned task, week 1, Stage 6
plan): ACM DL / IEEE Xplore / arXiv queries for {review comment mining, tacit knowledge code
review, reviewer intent classification, convention extraction review threads, static analysis
rule induction from reviews, agent PR review 2025–2026}; the sweep's negative result (or the
discovered neighbors) goes into the paper. Known partial neighbors to check first: work on
classifying review-comment intents (e.g., Turzo & Bosu on usefulness/intents [VERIFY]), and any
FSE/ICSE 2025–2026 "unwritten rules"-flavored titles. (2) Verification pass scheduled as a
concrete W1 task with a checklist over every [VERIFY] entry; entries failing verification are
dropped, not kept vaguely. (3) The boundary paragraph above is copy-ready for the paper's
related work; ZV9's draft gets the mirrored sentence (action item to the ZV9 owner). (4) Group
(f) added in the paper: LLM-judge reliability and human-agreement methodology (cite the
agreement-gated-judge design pattern; specific citations resolved in the W1 sweep) — this both
arms SP1 and pre-empts the "penalized LLM-judge" review objection.

---

## Stage 4 — Sub-problems

**SP1 — Constraint taxonomy + extraction reliability (the LLM-extraction-validity problem).**
Can an LLM pass over change-inducing comments produce constraint candidates whose precision,
recall, and categorization are *independently established* rather than assumed? The trap to
avoid — explicitly penalized in prior audits — is the unvalidated-LLM-judge pattern: LLM
extracts, LLM deduplicates, LLM categorizes, LLM checks, and no human number anchors any of it.
Design answer: every LLM stage gets a human-verified sample with pre-registered agreement
thresholds — extraction precision via dual annotation of n=300 sampled cards (Cohen's κ
reported; Wilson CIs), cluster purity via a pairwise-equivalence audit, categorization via dual
annotation with adjudication, recall proxy via independent human mining of held-out threads. A
non-LLM keyword/directive baseline (regex over should/must/never/avoid + code-element mentions)
bounds the LLM's added value. If human agreement on "is this a genuine constraint" is itself
low (κ < 0.4), that finding is reported as a result about the construct, and the taxonomy is
revised before scaling.

**SP2 — Repo selection and generalizability.** The measurement substrate (green-test agent
patches with matched human gold) exists at scale only for SWE-bench-family repos: mature,
review-heavy, Python, OSS. Pilot: 5 SWE-bench Verified repos with the highest in-line-review
volume (candidate set: django, scikit-learn, sympy, matplotlib, sphinx; confirm review-thread
counts empirically in W1 — repos with maintainer-committer cultures that review lightly are
excluded by a minimum-volume threshold, e.g., ≥2k change-inducing comments). Generalizability
is handled by honest scoping (claims indexed to "mature Python OSS"), per-repo reporting (no
pooled-only numbers), and a designed-but-deferred Stage-2 scale-up (more languages/repos)
positioned as future work + artifact extension, not squeezed before Oct 2.

**SP3 — Linking constraints to agent-patch violations while tests pass (the core
measurement).** Three linkage problems: (i) *applicability* — which cards apply to a given
patch (scope matching: path globs, module boundaries, trigger predicates on the diff); (ii)
*adjudication* — deciding violated/compliant/N-A per (patch, card) pair, tiered by
checkability: mechanical (AST/regex/semgrep rule auto-derived or hand-written from the card),
static-analysis-assisted, LLM-judge (agreement-gated, κ ≥ 0.6 vs dual human labels on n=400
pairs, judge model from a different family than any evaluated agent), or human-only; (iii)
*outcome linkage* — do violations predict real acceptance? Measured on held-out human PRs
(W₂ window): violation presence/count vs APPROVED-first-round / CHANGES_REQUESTED / time-to-merge,
with PR size and author-experience covariates. All patches in the measurement are verified
green (tests pass), so every violation found is by construction invisible to the test oracle —
that is the paper's central sentence.

**SP4 — The constraint-card artifact schema (T5.3's input contract).** T5.3 will evaluate
automated checkers against human review given *explicit* design cards; T5.1 must therefore emit
cards that are checkable objects, not prose. Schema v0 (YAML/JSONL, one card per record):

```yaml
card_id: django-EH-0007            # repo, category tag, serial
repo: django/django
statement: "Never catch bare Exception in ORM-layer code; catch the narrowest applicable subclass."
category: error_handling           # error_handling | arch_convention | api_convention | other
scope: {paths: ["django/db/**"], exclude: ["**/tests/**"]}
trigger: "diff adds an `except` clause"     # NL + optional AST predicate
checkability: static               # mechanical | static | llm | human_only
check_hint: "semgrep: except Exception: within django/db/"   # seed for T5.3's checkers
support: {threads: 5, reviewers: 3, authors: 4, window: "2019-01..2024-06"}
evidence: [{pr: 14231, comment_url: "...", revision_commit: "abc123"}, ...]
written_status: {linter_expressible: false, doc_mentioned: false}
examples: {violating_hunk: "...", conforming_hunk: "..."}    # from real revision diffs
provenance: {extractor: "model+prompt v1.3", clustered_by: "...", human_verified: true|false}
validation: {audit_round: 1, annotators: 2, verdict: genuine|spurious|ambiguous}
```

The fields T5.3 specifically needs: `statement` (imperative, self-contained), `scope` +
`trigger` (so a checker knows *when* the card applies), `checkability` + `check_hint` (so T5.3
can stratify precision/recall by automatability — its "which constraints can be automated,
which essentially need humans" question maps directly onto this field), `examples` (few-shot
material for LLM checkers and test cases for static ones), and `human_verified` (so T5.3 can
restrict to the validated subset). Schema is versioned; v0 frozen in W1 after a 30-minute
review against T5.3's README requirements.

**Critic:** (1) SP1's κ<0.4 escape hatch is honest but under-planned: what is the *procedure*
if agreement is low — codebook revision cycles cost annotator time the 7-week plan doesn't
have. (2) SP2's "5 repos, Python-only" invites the generalizability review kill; per-repo
reporting helps but the paper needs at least a cheap breadth probe. (3) SP3's outcome linkage
has a confound the current design under-handles: agent patches and held-out human PRs differ
systematically (task selection, size); and within human PRs, violations correlate with author
inexperience, which independently predicts CHANGES_REQUESTED — the correlation may be
author-effect, not constraint-effect. (4) SP4's `checkability` field is assigned by whom? If by
the extracting LLM, T5.3 inherits an unvalidated stratification variable. (5) Only measuring
violations ignores base rates: a category can look "most violated" merely because its cards are
most frequently applicable.

**Refined:** (1) Pre-commit a *single* codebook-revision cycle: pilot annotation on 50 cards →
revise codebook once → full n=300; if κ still < 0.4 on "genuine constraint," the paper pivots
its framing to "how reliably can implicit constraints even be identified?" — a legitimate
[证据] result — rather than iterating indefinitely. (2) Add a cheap breadth probe: run the
mining pipeline (only mining, no violation study) on 2 non-Python repos with heavy review
culture (e.g., a Rust and a TypeScript project) and report catalog yield + a 30-card precision
spot-check — one figure, bounds the "Python-only pipeline" objection. (3) Outcome linkage gets
covariate controls (PR size, files touched, author prior merged-PR count) in a logistic
regression, reported alongside the raw association, with the causal caveat stated; the
agent-vs-human comparison is kept *within-task* (matched pairs on identical SWE-bench tasks,
McNemar), which is immune to task-selection confounds. (4) `checkability` is dual-annotated by
humans on all cards that enter the released artifact (it is a small, low-cost label per card),
and the LLM's proposed value is recorded separately as `checkability_pred` so T5.3 can also
measure that prediction's accuracy. (5) All violation rates are reported with applicability
denominators: rate = violated / applicable per (category, patch-set), plus per-card rates in
the artifact; the headline "which category is most violated" claim uses the
applicability-normalized rate.

---

## Stage 5 — Methods

### 5.1 Mining pipeline (M1–M3)

- **M1 Review-corpus collector.** GitHub GraphQL harvest per pilot repo: PR review threads at
  (repo, PR, thread, in-line comment, anchored hunk) granularity, joined with verdicts, merge
  status, follow-up commits. Compute the *change-inducing* flag: a commit later in the PR
  modifies the anchored lines (heuristic: line-range overlap after diff-tracking through
  rebases; precision of this flag itself spot-checked on 100 threads). Restrict to a recent
  window (default: last ~5 years, per-repo tuned) to bound norm drift; record the window on
  every card.
- **M2 Constraint extractor.** LLM pass over each change-inducing comment + anchored hunk ±20
  lines context, emitting either `no_constraint` (one-off fix, question, praise, scope/process
  comment, *temporal/runtime obligation → routed out per the ZV9 boundary*) or a candidate
  record {imperative statement, scope guess, trigger, provisional category, evidence link}.
  Prompts versioned; keyword/directive regex baseline run in parallel on the same input.
- **M3 Catalog builder.** Sentence-embed candidate statements; cluster (HDBSCAN, cosine);
  LLM-merge each cluster into a canonical card; compute support (distinct threads, reviewers,
  authors); admit at threads ≥ 3 ∧ reviewers ≥ 2 ∧ authors ≥ 2, quarantine the rest (kept in
  the artifact, flagged). Assign `written_status` by (a) mapping against the repo's configured
  lint rule inventory + a "≤20-line custom rule" expressibility judgment and (b) doc search +
  annotator confirmation. Category and checkability dual-annotated.

### 5.2 Validation instruments (M5 — run *before* the violation study consumes the catalog)

1. **Card precision:** stratified n=300 cards (across repos × categories × support levels),
   two annotators, blind, verdict ∈ {genuine, spurious, ambiguous}; report κ and Wilson CI;
   pilot gate G1 uses the first 100.
2. **Cluster purity:** n=150 candidate pairs sampled within clusters; annotators judge
   same-rule/different-rule; purity < 0.8 forces re-clustering with tighter thresholds.
3. **Recall proxy:** 50–100 held-out threads (budget-dependent) independently mined by
   annotators; report fraction of annotator-found constraints recovered by the pipeline.
4. **Baseline comparison:** LLM extractor vs keyword baseline on paired thread-level detection
   (McNemar, α=0.05).

Annotators: two SE-experienced annotators (not the paper's prompt author, to avoid
self-confirmation); adjudication by discussion; all disagreement data released.

### 5.3 Violation study (M4)

- **Patch sets:** all green-test agent patches for pilot-repo tasks from the public SWE-bench
  experiments repository, ≥3 distinct agent systems (choose the 3–5 highest-volume distinct
  *scaffolds/model families* to avoid pseudo-replication of one model), plus matched human gold
  patches. Target ~300–500 agent patches after filtering.
- **Applicability:** cards matched to patches by scope globs + trigger predicates; ambiguous
  matches resolved conservatively (N-A), with the applicability matcher spot-checked (n=100
  pairs, human).
- **Tiered adjudication:** mechanical checks (semgrep/AST rules derived from `check_hint`)
  wherever `checkability ∈ {mechanical, static}` — these need no judge validation beyond rule
  review; LLM-judge for `checkability=llm` cards, **agreement-gated**: κ ≥ 0.6 vs dual human
  labels on n=400 (patch, card) pairs before any at-scale use; judge model from a different
  family than every evaluated agent; `human_only` cards adjudicated by humans on a budgeted
  subsample and reported separately. Every reported violation carries its tier, so readers can
  discount tiers they distrust.
- **Comparisons:** per-category applicability-normalized violation rates, agent vs human gold,
  matched-pair McNemar per category with Holm–Bonferroni across categories; per-repo
  stratification; chi-square for category non-uniformity.
- **Outcome linkage:** on held-out human PRs (disjoint window W₂), regress first-round outcome
  (approved vs changes-requested) on violation count with size/experience covariates.

**Critic:** (1) Deriving semgrep rules from cards is itself an error-prone step — a buggy
mechanical rule silently corrupts the "cleanest" tier; who validates the rules? (2) The
LLM-judge gate is per-pool, not per-category: κ ≥ 0.6 overall can hide κ ≈ 0.3 on architectural
cards (the hardest, and per the prediction the most violated — the headline category would rest
on the weakest judge). (3) Agent patch provenance: leaderboard submissions differ in date,
model version, scaffold; treating them as "coding agents" homogeneously invites a
which-agent-generation confound. (4) The plan's annotation total (300 cards + 150 pairs +
50–100 threads + 400 patch-card pairs + spot-checks, ×2 annotators) is ~70–90 annotator-hours —
feasible but only if annotators are secured in W1; there is no slack for recruitment slippage.
(5) Data contamination: agent models may have trained on the very review threads mined —
does that threaten the measurement? (Answer worth stating: it biases *toward* compliance,
making observed violations conservative — but say it.)

**Refined:** (1) Every mechanical rule gets a unit test built from the card's
`examples.violating_hunk` / `conforming_hunk` (must flag the former, pass the latter) plus a
10-sample human spot-check per rule; rules failing are demoted to LLM tier. (2) The judge gate
is applied **per category** (n≈130 pairs per category within the 400): any category failing
κ ≥ 0.6 has its automated labels replaced by human adjudication on a subsample, and the paper
reports that category with wider uncertainty. (3) Agent systems are reported individually
(system × category matrix), never only pooled; submission dates recorded; the paper claims a
distribution *per system generation*, noting heterogeneity. (4) W1 checklist includes annotator
commitment (2 people, ~45 h each, calendar-blocked); if only one external annotator is secured,
the second is a project member with blinding to pipeline outputs, disclosed as a threat. (5)
Add the contamination paragraph: training-data exposure to review history would push agents
*toward* compliance, so measured violation rates are a lower bound — strengthening, not
weakening, the headline claim.

---

## Stage 6 — Experiment Design

### 6.1 Datasets and scale

- **Review corpora:** 5 SWE-bench Verified repos (candidate: django, scikit-learn, sympy,
  matplotlib, sphinx; final pick by W1 volume audit, threshold ≥2k change-inducing comments in
  window). Expected order: 10k–40k change-inducing comments total through M2.
- **Patch corpora:** SWE-bench Verified tasks in those repos × green-test submissions from ≥3
  agent systems (public experiments repo) → target 300–500 agent patches + matched gold.
- **Held-out outcome set:** ~500 human PRs per repo from window W₂ (post-cutoff), with
  first-round verdicts.
- **Breadth probe:** 2 non-Python repos, mining only (SP2 refinement).

### 6.2 Metrics (all pre-registered in W1)

| Metric | Definition | Target/Gate |
|---|---|---|
| Constraint yield | admitted cards per 1k change-inducing comments, per repo | descriptive |
| Extraction precision | fraction of sampled cards dual-judged genuine (Wilson CI, κ reported) | **G1 pilot gate: ≥0.5 raw on first 100; ≥0.7 post-revision for headline** |
| Recall proxy | annotator-found constraints in held-out threads recovered by pipeline | descriptive, CI |
| Unwrittenness rate | fraction of cards linter-expressible=false ∧ doc-mentioned=false | headline claim if majority |
| Judge validity | κ(LLM judge, dual human) per category on n=400 pairs | **G2 gate: κ ≥ 0.6 per category** |
| Violation rate | applicability-normalized, per category × system, agent vs gold (McNemar, Holm–Bonferroni) | headline |
| Outcome correlation | violation count → first-round CHANGES_REQUESTED (logistic, covariates) | supporting |
| Baseline delta | LLM vs keyword extractor (McNemar) | supporting |

### 6.3 Go/no-go gates

- **G1 (end of W2, ~Aug 28):** extraction precision ≥ 0.5 on the first 100-card audit. Fail →
  one prompt/filter revision cycle (≤4 days); fail again → **pivot decision**: either reframe
  as a negative/feasibility result for a later venue, or descope to the 1–2 repos where
  precision holds. No Stage-2 spend before G1.
- **G2 (mid-W4, ~Sep 11):** judge κ ≥ 0.6 per category. Fail per-category → human adjudication
  fallback for that category (budgeted subsample).
- **G3 (end of W5, ~Sep 18):** violation study complete on ≥300 patches with ≥3 systems; if
  volume falls short, the paper reports the smaller n with CIs — no gate failure, just honesty.

### 6.4 Milestone plan, working back from FSE 2027 (submission Oct 2, 2026; today Aug 13)

| Week | Dates | Deliverables |
|---|---|---|
| W1 | Aug 13–20 | Repo volume audit + final repo pick; harvester running; card schema v0 frozen against T5.3 README; annotators calendar-committed; pre-registration doc (metrics, gates, α); novelty sweep + [VERIFY] citation checklist; intro/related-work drafting starts |
| W2 | Aug 21–28 | M2 extraction on 2 repos; 100-card audit → **G1**; codebook revision cycle if needed |
| W3 | Aug 28–Sep 4 | Full mining on 5 repos; clustering + catalog build; dual annotation (300 cards, purity pairs) running; breadth probe launched |
| W4 | Sep 4–11 | Catalog validation done (precision/recall/unwrittenness); violation checker built (mechanical rules + unit tests); judge validity sample → **G2** |
| W5 | Sep 11–18 | Violation study at scale (300–500 patches × catalog); outcome-linkage regression → **G3** |
| W6 | Sep 18–25 | Analysis freeze; figures; card artifact v1.0 frozen + handoff note to T5.3; full paper draft |
| W7 | Sep 25–Oct 1 | Internal review (se-paper-reviewer pass), threats section, artifact packaging (prompts, catalogs, labels, disagreements), submit Oct 2 |

Compute/budget: no training; ~30k–80k LLM API calls (M2+M4), low hundreds of USD; GitHub
harvest is rate-limit-bound (~days, W1–W2 background). Annotation ≈ 90 annotator-hours across
W2–W5.

**Critic:** (1) Seven weeks is the plan's dominant risk and the table pretends every step
succeeds on schedule; there is no explicit slack, and W4 stacks catalog validation, checker
construction, and judge validation simultaneously on the same two annotators. (2) The outcome-
linkage analysis needs held-out human PRs *with violations labeled* — that is another judge
pass over ~2.5k PRs' diffs, unbudgeted in the table. (3) The pilot gate G1 at ≥0.5 raw
precision is low; a catalog at 0.5 precision would be rightly savaged — the dependence of every
downstream number on the *post-threshold* 0.7 must be explicit, and if 0.7 is not reached the
violation study measures noise. (4) No explicit fallback venue if the work misses Oct 2; a
KEEP-TOP topic should not be schedule-gambled into a rushed submission. (5) The artifact
handoff to T5.3 is a one-line item; T5.3 being ON HOLD means no consumer will smoke-test the
schema before release — schema defects will be discovered after the paper is out.

**Refined:** (1) Two structural fixes: (a) the annotation-critical path is serialized
explicitly — card audit (W3) strictly before judge validation (W4), checker construction moved
to overlap W3 (it needs only the schema + early cards, not the validated catalog); (b) a
declared **descope ladder** with trigger dates: by Sep 11, if behind → drop the breadth probe;
by Sep 15 → drop outcome linkage to future work; by Sep 18 → reduce to 3 repos / 300 patches.
The headline claims (extraction validity + violation rates on green patches) are the last thing
sacrificed. (2) Outcome linkage is redesigned to fit the budget: sample 150 held-out human PRs
per verdict class per repo (not the full 2.5k), run only mechanical+static tier cards over them
(no LLM-judge pass, no new validation debt), and frame the result as "mechanically checkable
subset predicts outcomes" — smaller claim, fits W5. (3) G1 semantics clarified: 0.5 is the
*continue-investing* bar on raw candidates; the *publishable* bar is ≥0.7 on admitted
(post-threshold, post-revision) cards, checked on the full n=300 audit at W4 — if the 0.7 bar
fails, the violation study is cut and the paper becomes a rigorous feasibility/negative result
on constraint mining (still [证据], venue re-targeted). (4) Fallback venue named: FSE 2027
second cycle if one exists [VERIFY FSE 2027 cycle structure], else ISSTA 2027 / ICSE 2028 with
the extra time invested in the Stage-2 scale-up (more repos, languages) — turning the schedule
risk into a stronger paper rather than a worse one. (5) T5.3 handoff gets a concrete smoke
test inside T5.1's own W6: implement *one* trivial checker (semgrep runner over
`checkability=mechanical` cards) and verify it can parse and execute every released card
end-to-end — the minimum evidence that the schema is consumable, without unblocking T5.3 early.

---

## Summary

- **Core claim:** Implicit design constraints can be mined from PR review history into
  validated per-repo catalogs (precision established by human audit, not LLM self-grading), and
  green-test agent patches violate them at a measurably higher rate than matched human gold
  patches — direct, quantified evidence that the test oracle misses the acceptance-relevant
  norms behind the production merge-rate gap (METR/Faros figures kept [VERIFY]-gated,
  motivation-only).
- **Artifact:** versioned **constraint cards** (statement, scope, trigger, checkability class,
  support, evidence links, human-verified flag, violating/conforming examples) + violation-
  labeled agent/human patch sets — schema explicitly designed and smoke-tested as T5.3's input
  contract (checkability stratification maps onto T5.3's "what can be automated vs needs
  humans" question).
- **Novelty vs nearest prior:** review-automation work (CodeReviewer, DefectCR-line) leaves
  convention knowledge latent in weights and deprioritizes it as "nitpicks"; convention/rule
  induction (NATURALIZE, Getafix, MUDetect) mines code/edits, not review *dialogue*; the
  nearest thesis-neighbor (*From Correctness to Collaboration*) mines static rule files and
  interviews, qualitatively, with no per-repo catalogs or violation rates; ZV9 is explicitly
  disjoint (temporal runtime contracts from trajectories/API docs vs static design constraints
  from review dialogue — mutual routing rule written into both papers). A W1 novelty sweep is
  mandatory to confirm no unlisted review-comment→rule-induction twin exists.
- **Biggest risk:** extraction-validity collapse — most change-inducing comments may be one-off
  fixes, so admitted-card precision could miss the 0.7 publishable bar, invalidating the
  violation study; mitigated by the change-inducing filter, ≥3-thread/≥2-reviewer/≥2-author
  promotion rule, a two-bar gate (G1 continue-bar 0.5 at ~Aug 28; publishable-bar 0.7 at W4),
  and a pre-committed pivot to a rigorous feasibility/negative result if it fails.
- **Timeline feasibility:** tight but viable — 7 weeks to Oct 2 with no training, ~low-hundreds
  USD API spend, ~90 annotator-hours; feasibility rests on the W1 checklist (annotators
  committed, corpus volumes confirmed, schema frozen) and an explicit descope ladder (breadth
  probe → outcome linkage → repo/patch count) that protects the two headline claims; named
  fallback (FSE second cycle [VERIFY] / ISSTA 2027) converts a slip into the Stage-2 scale-up
  rather than a rushed submission.
