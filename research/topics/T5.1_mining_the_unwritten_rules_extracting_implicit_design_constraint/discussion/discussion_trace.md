# Auto-Research-Discussion Run — T5.1 (autoclaude-style, repo-driven from digest.md + paper.md)

> Mode: **autoclaude** (self-play, Claude as student+teacher). Source: `../digest.md` (N0–N12) + `../paper.md` (Steps 0–9), both pre-existing reverse-digest artifacts for seed **T5.1**. Round cap: 5/stage (none hit). All six stages converged in 1 critic round + 1 refiner pass each — the seed material was unusually mature (paper.md already carries formal notation, assumptions A1–A7, RQ hypotheses with pre-committed fallbacks, a walking skeleton, and an abstract v0), so genuine disagreement surfaced without needing a full re-proposal.
>
> **Full pipeline order (updated):** this file (`auto-research-discussion`, 6 stages) → `taste_audit.md` (`research-taste-auditor`, idea-level check on Stage 2+5) → `stage_review.md` (`pengsida-stage-reviewer`, PASS/REVISE/STOP per stage against the confirmed outputs, plus a Stage 5 Writing check on the first assembled draft) → final `paper_draft.md`/`.tex`/`.pdf`. Any REVISE findings from `stage_review.md` are folded into the `paper_draft.*` files below before they are called final — read `stage_review.md` for the reasoning behind each fix.

## Seed brief

- **One-sentence description:** Mine a per-repository, categorized catalog of implicit design constraints from historical pull-request code-review discussions, and measure how often test-passing coding-agent patches violate that catalog, by category, relative to matched human gold patches.
- **Apparent inputs:** historical PR review threads (in-line comments anchored to diff hunks, verdicts, follow-up commits) for a set of high-review-volume repositories; test-passing coding-agent patches for issues in those same repositories (public SWE-bench leaderboard submissions) plus their matched human gold patches.
- **Apparent outputs:** a categorized implicit-constraint catalog per repository (error handling / architectural convention / API convention), each entry with a support count and evidence links; per-patch violation labels (rule id, category, localization, rationale); a category-wise violation-rate distribution comparing agent and human patches.
- **Closest research areas:** LLM-based automated code review (DefectCR); coding-agent benchmarks graded purely by tests (SWE-bench, SWE-Lancer); constraint-heavy agentic code generation with curated documentation (FHE-Coder); latent-rubric learned critics (RLAC); repo-context-aware code editing (Coeditor); foundational empirical code-review studies (Bacchelli & Bird 2013; Bosu et al. 2015; CodeReviewer).
- **In scope:** mining and validating a constraint catalog from real review history, and measuring violation rates on test-passing agent vs. human patches in the same repositories. **Out of scope:** training or fine-tuning agents to comply with the catalog; characterizing violations in test-*failing* patches; feeding the catalog back into agent generation loops (explicitly deferred to future work, digest N10 t6).
- **Confidence: high.** As with the reference exemplar, the "repo" here is itself a prior reverse-digest plus a pre-registered spec (`digest.md` + `paper.md`) that already cross-references N-node ↔ M-component ↔ RQ ids and already ran its own informal asymmetry/taste self-check (`paper.md` Step 0/Step 3). Reconstruction risk is low; the discipline required is not inventing new content but **formalizing what's already there into the six-stage schema**, and using the critic/refiner loop to surface real precision gaps the seed's own hypothesis-tagging didn't force it to resolve (see Stage 1 below).

---

## Stage 1 — Problem Definition

### Round 1 (critic phase)

**draft_v1** (proposer):
- `summary`: Given historical pull-request review threads for a repository — in-line comments anchored to diff hunks, reviewer verdicts, and follow-up commits — and given test-passing patches produced by coding agents for issues in that repository together with the matched human-authored gold patch for each issue, determine (1) whether a categorized catalog of implicit design constraints (error-handling conventions, architectural conventions, API-usage conventions) can be systematically extracted from the review threads, and (2) at what rate and in which categories the test-passing agent patches violate that catalog relative to the matched human patches.
- `formal_summary`: Repository $r$ has review threads $T_r=\{t\}$, each an in-line comment $c_t$ anchored to diff hunk $h_t$ with PR verdict $v_t$ and follow-up commits $F_t$. A mined catalog $K_r=\{k\}$, $k=(\text{stmt}_k,\text{scope}_k,\text{cat}_k,\text{supp}_k,\text{ev}_k)$, $\text{cat}_k\in\{\text{EH},\text{ARCH},\text{API},\text{other}\}$. A patch $p$ (agent $p^a$ or human gold $p^g$) touches files $\text{files}(p)$; a judge $J(p,k)\in\{\text{violated},\text{compliant},\text{n/a}\}$. Determine (i) the extraction precision/recall of $K_r$ against human annotation, and (ii) the category-wise distribution of $J(p^a,k)=\text{violated}$ vs. $J(p^g,k)=\text{violated}$.
- `input`: (1) PR review threads with anchored diff hunks, verdicts, and follow-up commits, for a set of high-review-volume repositories; (2) test-passing coding-agent patches for issues in those repositories, from at least three distinct agent systems; (3) the matched human gold patch for each such issue.
- `output`: (1) a per-repository categorized constraint catalog with support counts and evidence links; (2) extraction precision and recall estimates for that catalog against human annotation; (3) per-patch violation labels (rule id, category, localization); (4) a category-wise violation-rate distribution contrasting agent and human-gold patches.
- `constraints`: ground truth = human review verdicts and human annotation; only test-passing patches are in scope (test-failing patches are out of scope by design, not by oversight); the catalog and the violation judge must each be validated before their outputs are used to support a comparative claim.
- `objective`: extraction is judged against human-annotated precision/recall on held-out threads; the violation-rate comparison between agent and human-gold patches is judged only once the compliance judge itself clears a stated agreement threshold against blind human annotation on a held-out sample of (patch, rule) pairs.
- `study_type`: `empirical` — stated explicitly, matching digest N12's `value: "empirical"`: both research questions are measurement claims (extraction feasibility; a violation-rate distribution of an already-existing phenomenon), not a system whose performance is the headline.

**critique:**
- summary: The problem is unusually well-scoped for a first draft, but `constraints` quietly folds together two epistemically different grounding sources under one label, and that conflation would let the paper's central comparison (agent vs. human violation rate) borrow more credibility than it has earned by the point it is actually measured.
- comments:
  - `{severity: major, field: "constraints", anti_pattern: "fields_misaligned", comment: "'Ground truth = human review verdicts' is only true for the catalog side of this study: the constraint catalog and its validation (precision/recall) are checked against real, historically-occurring PR verdicts and threads. But the violation labels on agent and human-gold patches (output 3/4) can never be 'human review verdicts' in that same sense — an agent's SWE-bench submission patch was never actually reviewed by a human on GitHub, so there is no verdict to consult. What stands in for ground truth there is a *constructed* compliance oracle: blind human annotators judging (patch, rule) pairs post hoc, whose agreement with the automated judge is itself only estimated at a stated threshold (digest A4, paper.md's kappa gate). Stating both under one 'ground truth = verdicts' line overstates the epistemic status of the RQ2-style comparison relative to what the design actually delivers — a reader could reasonably (and wrongly) assume agent patches were held to the same real-world review process the catalog was mined from."}`
  - `{severity: minor, field: "output", anti_pattern: null, comment: "Output (2), the precision/recall estimates, is itself a first-class deliverable this paper stakes claims on (digest CO1) — worth keeping explicit here rather than folding it silently into 'the catalog,' which the draft already does correctly; flagging only to make sure the refiner doesn't compress it back out."}`
- decision: `move_to_refiner` (the fix is a precision/formalization fix using content already in the digest and paper.md's own assumption list — no new content needed).

### Refiner pass

- `constraints` (refined): split into two explicitly distinct grounding claims: "(i) *catalog-validity ground truth* — the mined catalog's precision and recall are checked against real, historically-occurring PR review verdicts and threads (directly observed events); (ii) *violation ground truth* — because agent and human-gold patches in this study were never actually subjected to a live human review, per-patch violation labels are checked instead against a constructed compliance oracle: blind dual-human annotation of (patch, rule) pairs, with the automated judge admitted for scaled labeling only once it clears a pre-registered agreement threshold against that oracle. These are not the same kind of ground truth, and the paper's claims about (ii) are conditional on (i) and the judge-validity gate holding, not free-standing."
- `objective` (unchanged in substance, tightened for consistency with the split constraint): "Extraction is judged against human-annotated precision/recall on held-out threads (grounding type (i)); the category-wise violation-rate comparison between agent and human-gold patches is judged only once the compliance judge clears its stated agreement threshold against blind human annotation (grounding type (ii)) — a violation-rate claim reported before that gate clears is not a claim this problem definition licenses."
- `changes_made`: separated catalog-validity ground truth from violation-judgment ground truth in `constraints`; tightened `objective` to make the judge-validity gate an explicit precondition rather than an implicit one; kept `output`'s explicit listing of precision/recall as its own deliverable.
- `declined_to_fix`: none.

**Confirmed Stage 1** — `study_type: empirical`.

---

## Stage 2 — Motivation

### Round 1 (critic phase)

**draft_v1:**
- `summary`: Passing a project's automated test suite is treated, in nearly every coding-agent benchmark, as the criterion for a mergeable patch — but the actual criterion maintainers apply also includes error-handling, architectural, and API conventions that are never written into any spec, linter rule, or test, and that a project's own contributors absorb only by accumulating review feedback over time.
- `why_it_matters`: As coding agents are increasingly delegated to open pull requests autonomously, the test-passing benchmarks used to certify them (SWE-bench, SWE-Lancer) measure a signal that is, by construction, orthogonal to whether a patch respects the unwritten design norms a human reviewer would actually enforce — a patch can carry maximal behavioral evidence (every test passes) and zero compliance evidence at the same time. Automated code-review research has been moving toward defect detection and explicitly away from convention enforcement (DefectCR frames its own goal as prioritizing "defect detection over stylistic commentary"), even though foundational empirical work on human code review (Bacchelli & Bird, 2013) found that enforcing conventions and improving code, not just catching defects, is a dominant real-world outcome of review. That leaves exactly the compliance signal this paper targets without any automated, per-project measurement instrument at all.
- `who_cares`: Maintainers who review (or are asked to trust) autonomously generated pull requests; teams deciding whether a coding agent's test-passing patch is safe to merge without a full human review pass; benchmark designers deciding whether test-pass rate alone is a sufficient certification signal for agentic coding systems; SE researchers studying what code review actually enforces beyond defects.
- `evidence`: `[SWE-Lancer, OpenReview:xZXhFg43EI]`'s own motivation concedes that end-to-end tests "under-capture full-system expectations"; `[FHE-Coder, OpenReview:4F1py5vQXm]` shows that in a different constraint-heavy domain, reliable generation requires explicit constraint supply — but its constraints come from curated scheme documentation, which per-project design conventions by definition lack; `[DefectCR, OpenReview:mEV0nvHcK3]` explicitly filters out "stylistic commentary" as a design choice, showing the convention side of review is being actively engineered away from current automated tooling, not merely unaddressed; N3's own search-honesty note found only one code-review paper in an 11,683-paper ML-skewed corpus, itself evidence that this specific measurement gap is unclaimed territory in the venues that corpus samples.

**critique:**
- summary: The stakes are concrete and the citations are load-bearing, not decorative — but the motivation argues persuasively for why measuring *violations* matters and says nothing about why a *validated* catalog specifically (as opposed to any ad hoc list of conventions someone writes down) is worth the extra machinery this paper spends on it.
- comments:
  - `{severity: major, field: "why_it_matters", anti_pattern: "partial_output_coverage", comment: "Stage 1 output (2) — extraction precision/recall against human annotation — is a first-class deliverable (digest CO1), not a footnote to output (4)'s violation distribution. The current why_it_matters motivates the violation-measurement outputs (3)/(4) at length but never explains why the catalog's own validity has to be measured at all, rather than simply asserted. This is exactly the paper's own stated feasibility risk (digest N6: 'extraction precision collapse ... would invalidate everything downstream — RQ2 measures violations of rules that aren't real'): an unvalidated catalog makes every downstream violation-rate number meaningless, since a 'violation' of a spurious rule is not a violation of anything a maintainer actually enforces. Without stating this explicitly, a reader could reasonably ask why the paper doesn't just hand-write a plausible-looking convention list and skip straight to counting violations against it."}`
- decision: `move_to_refiner`.

### Refiner pass

- `why_it_matters` (extended): "...critically, none of this is informative unless the catalog itself is trustworthy: a violation-rate number computed against a spurious, hallucinated, or one-off 'rule' is not evidence about agent compliance with anything a maintainer actually enforces — it is noise wearing the shape of a finding. This is precisely why the catalog's own extraction precision and recall (output 2) has to be measured and gated before any violation distribution is reported, rather than assumed from the extraction pipeline's design alone: the validity of the instrument is a prerequisite for the credibility of the measurement, not a secondary detail to mention after the fact."
- `changes_made`: added the instrument-validity-as-prerequisite argument, closing the partial_output_coverage gap on Stage 1 output (2).
- `declined_to_fix`: none.

**Confirmed Stage 2.**

---

## Stage 3 — Related Work

All nine works below are treated as **specific (deep) tier** — digest N3/N4 already engaged each at the approach + limitation level; no title-only landscape mentions were present in the source material, and per the no-fabrication rule no additional landscape papers are invented here to pad a `general_related_works` list. (Digest N3 is explicit that the local corpus is ML-skewed and contains exactly one code-review paper; three canonical, non-corpus SE citations are retained under the stated quota and marked accordingly, matching the digest's own honesty framing.)

### Round 1 (critic phase)

**draft_v1** (`specific_related_works`, abbreviated to citation / I-O framing / limitation / `is_potential_baseline`):

| work_id | citation | is_potential_baseline | limitation (→ sub-problem it will motivate) |
|---|---|---|---|
| `rw_swebench` | SWE-bench (OpenReview:VTF8yNQM66) | false (data/protocol source, not a comparator) | Defines patch correctness solely via fail-to-pass repository tests; a patch that satisfies this definition carries no information about convention compliance. |
| `rw_swelancer` | SWE-Lancer (OpenReview:xZXhFg43EI) | false (data/protocol source) | Grades against professionally written end-to-end tests and payouts; its own motivation concedes tests under-capture full-system expectations, but it does not itself measure convention compliance. |
| `rw_defectcr` | DefectCR (OpenReview:mEV0nvHcK3) | false (I/O mismatch — live per-MR comments, not a persistent catalog) | Explicitly filters "stylistic commentary" and nitpicks to optimize for defect-oriented metrics; produces no persistent, reusable, per-project constraint artifact. |
| `rw_fhecoder` | FHE-Coder (OpenReview:4F1py5vQXm) | false (method-side reference) | Requires the constraints to already exist in curated documentation; per-project design conventions have no such documentation to retrieve from by definition. |
| `rw_rlac` | RLAC (OpenReview:dBmjnRR1bC) | **true** | Has a learned critic propose one likely-failing rubric per output rather than mining a stable, project-specific rubric inventory from historical feedback; cannot report which norm class is violated or how often. |
| `rw_coeditor` | Coeditor (OpenReview:ALVwQjZRS8) | false (method-side reference) | Captures conventions only implicitly as learned conditioning on prior diffs; when an edit breaks a norm the system cannot name the violated rule. |
| `rw_bacchelli` | Bacchelli & Bird, 2013 (ICSE) | false (foundational, canonical) | Establishes that review's dominant real-world outcomes include convention enforcement, but stops at a human-readable taxonomy, not a machine-applicable, per-repository rule set. |
| `rw_bosu` | Bosu et al., 2015 (MSR) | false (foundational, canonical) | Characterizes which comment types developers rate as useful, but produces a comment-usefulness taxonomy, not a catalog checkable against a new, unseen patch. |
| `rw_codereviewer` | CodeReviewer, Li et al., 2022 (ESEC/FSE) | false (I/O mismatch — comment generation, not catalog extraction) | Learns a diff-to-comment mapping whose convention knowledge stays latent in model weights; produces no explicit, auditable constraint artifact. |

**critique:**
- summary: Grounding is solid and every limitation is specific to this paper's gap (not "limited scalability"-style filler), but one baseline label is asserted without confronting an I/O mismatch that the rubric requires flagging.
- comments:
  - `{severity: major, field: "specific_related_works[rw_rlac].is_potential_baseline", anti_pattern: "io_approach_mismatch", comment: "RLAC trains a generator via DPO on a learned critic's per-output rubric preferences — a training-time mechanism, not an evaluation instrument applied to already-produced patches. Marking it a straightforward baseline without qualification risks implying this paper compares against RLAC's own reported numbers, which it does not and cannot (different task, different I/O). Per the stage-3 rubric, a mismatched-I/O work is 'not a baseline — at best a method-side reference,' unless the mismatch is explicitly reframed."}`
- decision: `move_to_refiner` (a wording-precision fix — the underlying *protocol* RLAC embodies is still legitimately reusable as a comparison arm, independent of its own reported results).

### Refiner pass

- `rw_rlac.is_potential_baseline` retained as `true`, but sharpened with an explicit note: "Not a baseline in the beat-a-number sense — RLAC's own reported preference-optimization results are not compared against. Its **per-output, instance-generated latent-rubric protocol** is borrowed as the experimental *catalog-free* comparison arm (a judge that proposes/checks a likely-failing rubric per patch with no mined, multi-thread-supported catalog behind it) — this isolates what a stable, historically-mined catalog adds over an on-the-fly rubric guess, independent of RLAC's own training objective or reported numbers."
- `changes_made`: clarified RLAC's baseline role to avoid an implied I/O-mismatched comparison against its own reported results.
- `declined_to_fix`: none.
- **Note on `verify_as_hypothesis`:** set `false` on every limitation. None is flagged as a stage-6 framing-tier RQ — the closest candidate (`rw_swebench`/`rw_swelancer`'s shared limitation, "test-passing carries no compliance information") restates this paper's own core question rather than being a distinct framing check, and it is already covered end-to-end as a mechanism-tier RQ in Stage 6 (the orthogonality claim). Per stages.md: *"If nothing was flagged, emit zero framing-tier RQs — don't manufacture one."*

**Confirmed Stage 3.**

---

## Stage 4 — Sub-Problems

### Round 1 (critic phase)

**draft_v1** (5 sub-problems, from digest N5's C1–C5):

- **`sp_candidate_identification`** — *description:* Distinguish review comments that state a generalizable design constraint from the large majority that do not (questions, praise, one-off bug notes). *why_it_is_a_problem:* Any catalog is only as good as its input filter — admitting noise floods the catalog with spurious entries that invalidate every downstream violation count. *technical_challenge:* No formal source of truth exists anywhere in the project (no spec, doc, or lint config) to check a candidate against, so the filter must operate on unstructured dialogue where most turns are not constraints at all. *source_limitation_ids:* `["__novel__"]` — no cited work solves comment-level constraint-vs-noise classification for this purpose; DefectCR's related move is to filter such comments *out* entirely, not to classify and retain the generalizable subset.
- **`sp_semantic_dedup`** — *description:* Collapse many differently-phrased instances of the same underlying rule into one canonical catalog entry. *why_it_is_a_problem:* Without this, a single norm inflates into many entries (or a rule stated only once looks unsupported), corrupting both the catalog's size and its support-based validity signal. *technical_challenge:* The same constraint surfaces with high lexical and contextual variability — differently phrased, partially stated ("same as above"), sometimes only implied by the requested change rather than stated — so matching must operate at the level of rule semantics, not surface text. *source_limitation_ids:* `["__novel__"]`.
- **`sp_compliance_oracle`** — *description:* Build and validate a way to judge whether a patch violates a catalog rule, independent of whether the patch passes the project's tests. *why_it_is_a_problem:* Test suites do not encode these constraints by construction, so if the oracle isn't itself independently validated, "violation" is just an assertion — exactly the paper's central asymmetry claim would otherwise go unverified. *technical_challenge:* There is no existing signal to build the oracle from (tests are silent on this by design), so the judge has to be built from scratch and its agreement with genuine human judgment has to be measured, not assumed. *source_limitation_ids:* `["rw_swebench", "rw_swelancer"]` — both define patch success exclusively via tests, which is exactly the gap this sub-problem targets.
- **`sp_category_reliability`** — *description:* Assign each catalog entry to a category (error handling / architectural convention / API convention) in a way that is reliable and reportable, not assumed. *why_it_is_a_problem:* A category-wise violation distribution (this paper's headline result) is meaningless if the categories themselves are unreliable or arbitrarily assigned. *technical_challenge:* The three categories are neither mutually exclusive nor uniform in granularity — a rule like "never raise a bare exception across a module boundary" is simultaneously error-handling and architectural — so consistent categorization is inherently ambiguous and must be measured, not assumed. *source_limitation_ids:* `["rw_bacchelli", "rw_bosu"]` — both stop at human-readable taxonomies without a reliability-checked, machine-applicable rule set.
- **`sp_groundtruth_noise`** — *description:* Produce a violation-rate finding that is not an artifact of noisy, disagreeing, or drifting human ground truth. *why_it_is_a_problem:* The designated ground truth (review verdicts, annotator judgments) is itself noisy: reviewers disagree, norms drift over a project's lifetime, and a verdict's reason is often under-articulated even when the verdict itself is clear. *technical_challenge:* This noise cannot be designed away, only bounded — aggregating across multiple reviewers/threads and restricting to a recent time window reduces but does not eliminate it, so the paper's claims must be stated at a granularity the noise can actually support. *source_limitation_ids:* `["__novel__"]`.

**critique:**
- summary: Coverage checks out (solving all five would jointly deliver Stage 1's outputs), but two sub-problems both invoke "cleaning up messy raw comment text" and the description doesn't yet make clear that they are different kinds of cleanup, not the same one twice.
- comments:
  - `{severity: minor, field: "sp_candidate_identification / sp_semantic_dedup", anti_pattern: "overlap", comment: "Both operate on the same raw material (noisy review comments) and could read as one 'clean up the data' step under two names. They are genuinely distinct — one is a classification problem (is this comment a constraint at all?), the other is an identity problem (are these two constraint-candidates the same underlying rule?) — but the descriptions don't say so explicitly enough to head off the reading that they're redundant."}`
- decision: `move_to_refiner`.

### Refiner pass

- `sp_candidate_identification.technical_challenge` sharpened to end with: "...this is a **classification** problem — deciding whether a single comment expresses a constraint at all — distinct from the separate problem of recognizing that two different constraint-expressing comments state the *same* rule."
- `sp_semantic_dedup.technical_challenge` sharpened to end with: "...this is an **identity/matching** problem that only starts once candidate identification has already decided a comment expresses *some* constraint — no amount of better classification at the candidate-identification stage removes the need to then recognize when two accepted candidates are restatements of one rule."
- `changes_made`: made the classification-vs-identity distinction explicit in both `technical_challenge` fields.
- `declined_to_fix`: none.

**Confirmed Stage 4** (5 sub-problems; 2 sourced from related-work limitations, 3 `__novel__` with stated decisive-component justifications).

---

## Stage 5 — Method Design

### Round 1 (critic phase)

**draft_v1** (5 methods):

- **`m_change_inducing_extractor`** → targets `sp_candidate_identification`. *proposed_approach:* Mine candidates only from review comments that demonstrably induced a later code change (a follow-up commit edits the lines the comment anchored to), run an LLM extraction pass over each such comment plus its diff hunk and surrounding file context, and require the extractor to positively emit a normalized rule statement or an explicit no-constraint verdict rather than passing every comment through by default. *key_insight:* "Most comments are not constraints" stops being a judgment call made comment-by-comment and becomes a behavioral, checkable filter — a comment only becomes a candidate if a human's response to it is already on record as having changed the code. *hypotheses:* ["Catalog-entry precision, estimated from a 300-entry dual-annotated sample drawn from the pilot repos, has a Wilson 95% CI lower bound of at least 0.60.", "The change-inducing LLM extractor achieves higher paired thread-level constraint-detection accuracy than a keyword/directive-pattern baseline (regex over should/must/please/avoid/never plus code-element mentions), McNemar p<0.05 in the extractor-favoring direction."]
- **`m_catalog_builder`** → targets `sp_semantic_dedup`. *proposed_approach:* Embed candidate rule statements with a sentence-embedding model, cluster them, and have an LLM merge each cluster into one canonical entry carrying a support count (distinct threads, distinct reviewers); entries with fewer than three distinct supporting threads are quarantined rather than admitted to the catalog. *key_insight:* A support threshold turns "is this a recurring norm or one reviewer's one-off phrasing" from an eyeballing judgment into a countable, pre-specified admission rule. *hypotheses:* ["At least half of admitted catalog entries (support ≥3 threads) are not mappable to any existing ruff/pylint/import-linter rule (linter-expressibility rate < 0.50), evidencing that the catalog captures genuinely unwritten content rather than already-formalized style rules."]
- **`m_compliance_judge`** → targets `sp_compliance_oracle`. *proposed_approach:* Retrieve the catalog entries applicable to a patch's touched files, run an LLM judge per (patch, rule) pair emitting violated/compliant/not-applicable with a localization and rationale, and validate that judge's output against blind dual-human annotation of a held-out sample of (patch, rule) pairs before treating its labels at scale as evidence. *key_insight:* A judge built and gated this way can detect violations on patches that already passed every test, which is exactly what would be impossible if the compliance signal were even partly recoverable from test outcomes. *hypotheses:* ["The compliance judge reaches agreement of κ ≥ 0.6 with blind dual-human annotation on a 400 (patch, rule)-pair sample.", "Among held-out test-passing patches, the validated judge confirms a nonzero rate of catalog-rule violations — demonstrating that passing every test carries no information about mined-constraint compliance."]
- **`m_category_annotation`** → targets `sp_category_reliability`. *proposed_approach:* Two annotators independently assign each catalog entry a category (error handling / architectural convention / API convention / other), adjudicate disagreements, and report Cohen's kappa; results are additionally reported at the individual catalog-entry level, not only aggregated by category, so a genuinely boundary-spanning entry's ambiguity doesn't get silently absorbed into one category's count. *key_insight:* Reporting at entry granularity as well as category granularity means a mis-assigned or genuinely ambiguous rule can be surfaced and audited rather than quietly determining which category "wins" a comparison it was never cleanly assigned to. *hypotheses:* ["Dual-annotator category labeling reaches a pre-registered Cohen's kappa threshold, with residual disagreement concentrated in entries routed to 'other' rather than spread uniformly across the three named categories."]
- **`m_stability_design`** → targets `sp_groundtruth_noise`. *proposed_approach:* Restrict mining to a recent, bounded time window per repository; aggregate support and violation evidence across multiple reviewers and threads rather than trusting any single verdict; compute the category-wise violation distribution and the agent-vs-human-gold comparison from this aggregated, time-bounded evidence base. *key_insight:* A single mixed comparison design over this aggregated evidence base yields two distinct, separately falsifiable estimands: the shape of the category-wise distribution itself, and the agent-vs-human-gold gap within it — one design, two readouts, not two separate mechanisms. *hypotheses:* ["The category-wise violation distribution is non-uniform (chi-square goodness-of-fit p<0.05), with error-handling and architectural-convention violation rates exceeding the API-convention rate.", "Test-passing agent patches violate mined constraints at a higher rate than matched human gold patches in at least one category (McNemar p<0.05, Holm-Bonferroni corrected across the three categories)."]

**critique:**
- summary: Every method traces to a real sub-problem and every hypothesis is falsifiable with a stated threshold, but one method's baseline comparison risks reading as an outcome-tier "beats a competitor" claim, which `study_type: empirical` forbids.
- comments:
  - `{severity: major, field: "m_change_inducing_extractor.hypotheses[1]", anti_pattern: "tier_violation (anticipated)", comment: "As worded, 'the extractor achieves higher accuracy than a keyword baseline' reads exactly like the outcome-tier 'our procedure beats baseline X' framing that stage 6 must forbid for an empirical study. The intent (per the seed's own framing in paper.md, and per Stage 3's treatment of the keyword baseline as a coverage/necessity check, not a competitor) is different: the comparison exists to test whether *semantic* understanding of a comment's content is doing real work, as opposed to surface pattern-matching being sufficient — a claim about what the extraction mechanism needs, not a claim that this paper's system is better than a rival system. The hypothesis wording needs to make that distinction explicit now, so stage 6 doesn't inherit an ambiguous RQ that could be misread as outcome-tier."}`
- decision: `move_to_refiner` (a framing-precision fix, not a new comparison — the mechanism and the data needed are unchanged).

### Refiner pass

- `m_change_inducing_extractor.hypotheses[1]` (refined): "The change-inducing LLM extractor achieves higher paired thread-level constraint-detection accuracy than a keyword/directive-pattern baseline (regex over should/must/please/avoid/never plus code-element mentions), McNemar p<0.05 in the extractor-favoring direction — tested as a **necessity check on the mechanism** (does recognizing a constraint require semantic understanding of what the comment and its diff hunk say, or does a naive lexical pattern already suffice), not as a claim that this paper's pipeline outperforms a rival system to be beaten."
- `changes_made`: reframed the keyword-baseline hypothesis as a mechanism-necessity check rather than a competitive comparison, to keep it unambiguously mechanism-tier once it reaches Stage 6.
- `declined_to_fix`: none.

**Confirmed Stage 5** — 5 methods, **8 hypotheses total** (2 + 1 + 2 + 1 + 2 across the five methods respectively — `m_change_inducing_extractor`, `m_compliance_judge`, and `m_stability_design` each carry two, per the refiner's one-instrument/one-design-two-readouts justifications above).

---

## Stage 6 — Experiment Design

**Tier accounting (checked against study_type=empirical):**
- **Mechanism-tier: 8 RQs**, one per Stage 5 hypothesis (verbatim `target_hypotheses`).
- **Framing-tier: 0 RQs** — no Stage 3 limitation was flagged `verify_as_hypothesis`; none manufactured.
- **Outcome-tier: 0 RQs** — `study_type = empirical` forbids "our procedure beats baseline X" framing. The keyword baseline and the catalog-free judge are sanity-check/ablation comparators embedded inside mechanism-tier RQs, never a competitor to beat.

### Round 1 (critic phase)

**draft_v1:**

`datasets`:
- SWE-bench Verified (500 human-validated repository-issue tasks) — *justification:* supplies the pilot repositories (django, scikit-learn, sympy, matplotlib, sphinx), the issue set, and the matched human gold patch for every agent patch tested in RQ7/RQ8, which is what makes a matched-pair comparison possible at all.
- Public SWE-bench leaderboard submission patches — *justification:* the source of test-passing agent patches from at least three distinct agent systems, needed so RQ7/RQ8's violation distribution is not an artifact of one agent's idiosyncratic style.
- PR review-history corpus harvested from the five pilot repositories — *justification:* the raw material RQ1–RQ4 mine and validate the catalog from; chosen to overlap exactly with the SWE-bench Verified repository set so the catalog and the patches being judged against it come from the same projects' actual norms.

`baselines` (sanity-check/necessity comparators, not outcome-tier competitors — this is a measurement study, and no research question here is framed as "our procedure beats baseline X"):
- Keyword/directive-pattern extractor — necessity check for RQ2: if a naive lexical pattern-matcher already recovered as much as the LLM extractor, semantic understanding would not be doing real work in candidate identification.
- Existing linter/architecture rule inventories (ruff, pylint, import-linter) — coverage check for RQ3: establishes what fraction of the catalog is already formalized elsewhere, which is what "unwritten" has to mean operationally.
- Catalog-free zero-shot LLM judge (the RLAC-style per-output latent-rubric protocol, borrowed per Stage 3's sharpened role) — ablation control for RQ5/RQ7/RQ8: isolates whether a stable, multi-thread-supported, mined catalog finds anything a same-model judge without that catalog would not already find on its own.
- Matched human gold patches — the necessary reference distribution for RQ8's agent-vs-human comparison, and the "why do this at all" control: if human gold patches already violate the catalog at the same rate as agent patches, there is no agent-specific compliance gap to characterize.

`research_questions` (8, all mechanism-tier):

| rq_id | target_sub_problem_id | target_hypotheses (verbatim) |
|---|---|---|
| `rq_extraction_precision` | `sp_candidate_identification` | "Catalog-entry precision, estimated from a 300-entry dual-annotated sample drawn from the pilot repos, has a Wilson 95% CI lower bound of at least 0.60." |
| `rq_semantic_vs_keyword` | `sp_candidate_identification` | "The change-inducing LLM extractor achieves higher paired thread-level constraint-detection accuracy than a keyword/directive-pattern baseline (regex over should/must/please/avoid/never plus code-element mentions), McNemar p<0.05 in the extractor-favoring direction — tested as a necessity check on the mechanism (does recognizing a constraint require semantic understanding of what the comment and its diff hunk say, or does a naive lexical pattern already suffice), not as a claim that this paper's pipeline outperforms a rival system to be beaten." |
| `rq_linter_expressibility` | `sp_semantic_dedup` | "At least half of admitted catalog entries (support ≥3 threads) are not mappable to any existing ruff/pylint/import-linter rule (linter-expressibility rate < 0.50), evidencing that the catalog captures genuinely unwritten content rather than already-formalized style rules." |
| `rq_judge_validity` | `sp_compliance_oracle` | "The compliance judge reaches agreement of κ ≥ 0.6 with blind dual-human annotation on a 400 (patch, rule)-pair sample." |
| `rq_orthogonality` | `sp_compliance_oracle` | "Among held-out test-passing patches, the validated judge confirms a nonzero rate of catalog-rule violations — demonstrating that passing every test carries no information about mined-constraint compliance." |
| `rq_category_reliability` | `sp_category_reliability` | "Dual-annotator category labeling reaches a pre-registered Cohen's kappa threshold, with residual disagreement concentrated in entries routed to 'other' rather than spread uniformly across the three named categories." |
| `rq_category_distribution` | `sp_groundtruth_noise` | "The category-wise violation distribution is non-uniform (chi-square goodness-of-fit p<0.05), with error-handling and architectural-convention violation rates exceeding the API-convention rate." |
| `rq_agent_vs_human_gap` | `sp_groundtruth_noise` | "Test-passing agent patches violate mined constraints at a higher rate than matched human gold patches in at least one category (McNemar p<0.05, Holm-Bonferroni corrected across the three categories)." |

(setup/sample-size/statistical-test/expected-outcome/metrics per RQ carried into the paper draft's Experiments section below, reusing paper.md's already-designed Step 6 numbers and pre-committed fallback wording as authored design targets, not fabricated results.)

**critique:**
- summary: Tier accounting is clean, every RQ traces to a verbatim hypothesis, and the mechanism-tier reframing from Stage 5 carried through correctly — but one baseline's justification needs to state what specifically would be learned from a null result, not just what it isolates.
- comments:
  - `{severity: minor, field: "baselines[catalog-free zero-shot LLM judge]", anti_pattern: null, comment: "The justification says what the ablation isolates but not what a null result (catalog-free judge finds the same violations as catalog-guided judging) would mean for the paper's central claim. Worth stating explicitly: a null result here would not refute the orthogonality finding (rq_orthogonality), but it would refute the *catalog's* specific contribution — i.e., it would mean the paper's real instrument is 'a capable LLM asked to look for problems,' not the mined, multi-thread-supported catalog, undercutting CO1/CO3 even if CO2/CO4 survive."}`
- decision: `move_to_refiner`.

### Refiner pass

- `baselines[catalog-free zero-shot LLM judge]` justification extended: "...if catalog-guided and catalog-free judging materially agree on which patches violate which rules, that would not refute the orthogonality finding (test-passing still carries no compliance information either way) but it would refute the catalog's own specific contribution — the paper's real instrument would be 'a capable LLM asked to look for problems' rather than the mined, multi-thread-supported catalog, which is a distinct and more damaging finding for CO1/CO3 than a null on the agent-vs-human gap (rq_agent_vs_human_gap) would be."
- `changes_made`: added the null-result interpretation to the catalog-free judge baseline's justification, distinguishing what it would and would not refute.
- `declined_to_fix`: none.

**Confirmed Stage 6.**

---

## Cross-stage consistency check (final pass, all six stages)

1. **No method leak** in stages 1/2/4 — checked; `objective`/`why_it_is_a_problem` fields name no technique (LLM, embeddings, clustering appear only from Stage 5 onward).
2. **ID stability** — no id renamed mid-run; `sp_*` / `m_*` / `rq_*` stable stage-to-stage.
3. **Reference integrity** — `sp_compliance_oracle.source_limitation_ids = ["rw_swebench", "rw_swelancer"]` ∈ Stage 3 works ✓; `sp_category_reliability.source_limitation_ids = ["rw_bacchelli", "rw_bosu"]` ∈ Stage 3 works ✓; all other `source_limitation_ids = ["__novel__"]` ✓; every `target_sub_problem_id` in Stage 5 ∈ Stage 4 ✓; every Stage 6 `target_hypotheses` entry is a verbatim match to a Stage 5 hypothesis ✓.
4. **Output coverage** — Stage 1's four outputs (catalog, precision/recall, per-patch violation labels, category-wise distribution) are each reachable: catalog and precision/recall via `sp_candidate_identification` + `sp_semantic_dedup`, violation labels via `sp_compliance_oracle`, category-wise distribution via `sp_category_reliability` + `sp_groundtruth_noise` — nothing promised in Stage 1 falls off the chain by Stage 6.
5. **`study_type` consistency** — `empirical` throughout; Stage 6 correctly emits 0 outcome-tier RQs, and the one RQ (`rq_semantic_vs_keyword`) that risked reading as outcome-tier was explicitly reframed as a mechanism-necessity check at Stage 5 and carried that framing through to Stage 6 without drifting back.

**What was hardest:** unlike a typical raw-idea run, the seed material contained almost no factual gaps to fill — the recurring difficulty was **precision discipline**: repeatedly checking whether a field was quietly claiming more certainty than the design actually delivers (Stage 1's conflated "ground truth," Stage 5's baseline comparison reading as outcome-tier). Both issues trace to the same root cause — the seed's own hypothesis-tagging in `paper.md` is honest about *what* it measures but doesn't always make explicit *why* a given comparison is licensed under an `empirical` study type rather than a competitive one, which is exactly the kind of drift this six-stage schema is built to catch.

**Total rounds:** 6 stages × 1 critic round + 1 refiner pass = 6 critic rounds, 6 refiner passes. No stage hit the round cap; no cross-stage backup was required.


---

## Post-review revision round (2026-07-05)

Revision pass over the review artifacts (`stage_review.md`, `taste_audit.md`; no `design_review.md` exists). Every finding/recommendation enumerated, status-checked against the current deliverables, and either applied or dispositioned below. Past rounds above are untouched.

1. **stage_review.md → Stage 2 REVISE (nearest-neighbor sentence naming DefectCR + RLAC)** — verified already applied: present as the opening paragraph of `paper_draft.md`/`paper_draft.tex` Related Work. No change needed.
2. **stage_review.md → Stage 4 REVISE (bound the RQ3 "unwritten" claim to the checked tool surface)** — verified already applied in `paper_draft.md`/`.tex` (Constraint Catalog Builder, RQ3 falsification condition, Conclusion limitations). No change needed.
3. **stage_review.md → Phase A item 4/5 (missing fallbacks RQ1(ii)/RQ2(i); missing effect floors ≥8-pt paired-accuracy gap, Cramér's V≥0.15, ≥8-pt matched-pair gap; power/thin-cell rule; mechanism analysis)** — was applied to `paper.md` and `paper_draft.md`, but **`paper_draft.tex` was stale**: its RQ2/RQ7/RQ8 blocks still carried the pre-fix wording (no effect floors, no "dropped as moot" branch, no thin-cell/4-of-5 rule) and the mechanism-analysis paragraph was missing entirely, as was RQ1's kappa-reported-not-gated metric line. **Applied:** mirrored all of these from `paper_draft.md` into `paper_draft.tex` (RQ2 expected outcome/falsification/metrics; RQ7 setup/expected outcome/falsification/metrics; RQ8 expected outcome/falsification/metrics; new "Mechanism analysis (secondary, non-gating)" paragraph) and recompiled (`latexmk -pdf`: clean, 13 pages).
4. **pipeline.md resumability note → re-check `paper_draft.*` against the added method-twin `2512.23844` (guidance Part 4 situation 6 concede-and-differentiate)** — was OPEN: neither draft mentioned the twin. **Applied:** added a "Human-centered agent-evaluation taxonomies" paragraph to Related Work in both `paper_draft.md` and `paper_draft.tex`, sourced strictly from digest.md N3 entry 10 / N4 limitation 7 (concede: shared correctness-isn't-enough thesis incl. "Adhere to Standards and Processes", human-validated taxonomy; differentiate: static rule-files/interviews + qualitative cross-company taxonomy vs. dynamic per-repo review-dialogue mining + quantitative per-category violation rate against matched human gold).
5. **stage_review.md → Phase A item 6 fix (R1 estimand paragraph added to paper.md Step 5)** — was OPEN in the deliverables: `experiment_design.md` (the standalone execute-from document) carried the effect floors, power rule, and mechanism plan but not the estimand. **Applied:** added an "Estimands (R1, from paper.md Step 5)" section to `experiment_design.md`, quoting paper.md's two-part estimand. Not force-fitted into `paper_draft.md`, whose Problem Definition already states the twofold object of study in prose.
6. **stage_review.md → Phase A item 6 advisory (κ≥0.6 gate vs. guidance recipe's κ≥0.7; "flagged for the next run's owner to decide explicitly")** — **decided, not silently kept:** κ≥0.6 retained (Landis–Koch "substantial" band; pre-registered consistently across digest.md/paper.md/Stage 6 hypotheses/paper_draft; raising it post-registration would break byte-identical hypothesis traceability). Decision recorded as an explicit "Threshold note" under RQ4 in `experiment_design.md`.
7. **stage_review.md → Phase A item 2 residual (5 method-twin cache entries lack local PDF/digest)** — **rejected — out of scope for a deliverable-revision pass:** this is a reference-harvest task explicitly logged in stage_review.md as "a follow-up harvest item to close before Phase E's mandatory freshness sweep," not a change to any deliverable. Left logged.
8. **pipeline.md resumability note → re-run the goal.md §1 freshness sweep** — **rejected — out of scope/environment:** a full harvest/freshness sweep is Phase E gate work, not a review finding against the deliverables; the one concrete freshness consequence already discovered (method-twin `2512.23844`) is folded in via item 4.
9. **taste_audit.md** — 🟢 verdict, all three conditions clear; no findings to apply.

**Cross-deliverable consistency re-check after the above:** 8 RQs in both `paper_draft.md/.tex` and `experiment_design.md`; effect floors match (≥8-pt paired-accuracy gap RQ2, Cramér's V≥0.15 RQ7, ≥8-pt matched-pair gap RQ8); n=300/n=100/n=400/~500-patch samples, n≥20 thin-cell rule and 4-of-5 pooling condition, α=0.05, Holm–Bonferroni across 3 categories all match; `experiment_design.md` target hypotheses remain byte-identical to `paper.md` Step 6 (untouched this pass).
