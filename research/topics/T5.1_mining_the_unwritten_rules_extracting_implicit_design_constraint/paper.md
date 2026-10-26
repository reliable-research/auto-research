# Mining the Unwritten Rules: Extracting Implicit Design Constraints from Code Review History — Pre-Registered Paper Specification
> Generated from digest.md + README.md. Status: specification, no experiments run.

## Step 0 — Core Asymmetry (升维)

**Asymmetry sentence:** The requirements a maintainer enforces on a patch are decided in review dialogue but never encoded in the test suite, so the signal that determines mergeability is orthogonal to the signal a passing test measures — a patch can carry maximal behavioral evidence and zero compliance evidence at once.

**判据 test (delete the domain nouns):**
> "The ___ a ___ enforces on a ___ are decided in ___ but never encoded in the ___, so the signal that determines ___ is orthogonal to the signal a passing ___ measures."

Stripped of *maintainer / patch / review dialogue / test suite / mergeability*, the sentence collapses to "some signal is orthogonal to some other signal" — an empty generic claim. The load is carried entirely by the domain-specific fact that convention enforcement lives in review history while correctness lives in tests, and that these two channels do not overlap. It is therefore an asymmetry, not a bridge. (Grounds digest C3; the orthogonality is what the whole study exploits.)

---

## Step 2 — Archetype

**Primary archetype:** *New measurement instrument + empirical characterization of a previously unmeasured quantity* (consistent with digest N12 `value="empirical"`). The headline is not a system's performance but two measurements: (i) can the quantity be extracted at all (RQ1), and (ii) what does its distribution look like for agents vs. humans (RQ2).

**Secondary archetype:** *Released dataset/artifact* (digest CO3: per-repo catalogs + violation-labeled patch set).

Downstream consequences:
- **(a) Abstract contribution slot:** a validated instrument for mining a per-repo constraint catalog with measured precision/recall, plus the first category-wise agent-vs-human violation distribution over test-passing patches — not a new model or SOTA number.
- **(b) Intro logic:** "what becomes possible" — measuring design-constraint compliance where only test-pass rate was measurable before. NOT "we beat baseline X by N points."
- **(c) Evidence standard:** human-validated ground truth throughout (annotator precision/recall for the catalog; judge-vs-human κ gate before any automated violation label counts). A finding is credible only if the instrument that produced it passed its own validity gate.

---

## Step 3 — Taste self-audit

- **Is the opportunity a Bridge?** Check: the value is not "connect review-mining and agent-eval." It is measuring an orthogonal, currently-unmeasured compliance signal (Step 0). PASS — not a bridge.
- **Is the method mere Synthesis?** The pipeline reuses embeddings/clustering/LLM-judging, but the load-bearing novelty is the *change-inducing filter as a behavioral definition of "enforced expectation"* (M1) plus a human-gated compliance oracle (M5). PASS — the mechanism is a new operationalization, not a toolchain assembly.
- **Load-bearing verbs from integrate/unify/leverage family?** Original framing leaned on "mine/leverage review history." Corrected to gate/formalize/isolate/measure family: we *formalize* an implicit constraint as a change-inducing, multi-thread-supported rule; *isolate* compliance from correctness; *measure* the violation distribution. PASS after correction.
- **Abstract-opening rule:** forbidden template ("X is increasingly used… however… we introduce") is avoided; v0 below opens on the orthogonality mechanism.

No skeleton change needed beyond swapping the verb family; the idea already rests on an asymmetry.

---

## Step 5 — Formal Problem Definition

**Estimand (R1, one sentence per linked quantity, guidance.md §3.4).** (i) For RQ1: the precision and recall of a mined implicit-design-constraint catalog against human-annotated review threads, unit of analysis = one catalog entry (precision) or one held-out thread (recall proxy), reference population = the 5 pilot repositories' review history, feeding the decision of whether automated catalog mining is trustworthy enough to apply at scale at all. (ii) For RQ2: the category-wise rate at which test-passing patches violate the (RQ1-validated) catalog, unit of analysis = one (patch, category) pair, reference population = test-passing SWE-bench-Verified agent patches (≥3 systems) and their matched human-gold patches in the same repos, feeding the decision of whether test-suite success is a sufficient certification signal for autonomously-opened agent PRs.

**Notation.** Repository $r$ has review threads $T_r=\{t\}$, each thread an in-line comment $c_t$ anchored to a diff hunk $h_t$ with a PR verdict $v_t\in\{\text{APPROVED},\text{CHANGES\_REQUESTED}\}$ and follow-up commits $F_t$. A mined catalog $K_r=\{k\}$; each entry $k=(\text{stmt}_k,\text{scope}_k,\text{cat}_k,\text{supp}_k,\text{ev}_k)$ with category $\text{cat}_k\in\{\text{EH},\text{ARCH},\text{API},\text{other}\}$. A patch $p$ (agent $p^a$ or human gold $p^g$) touches files $\text{files}(p)$. Judge $J(p,k)\in\{\text{violated},\text{compliant},\text{n/a}\}$.

| Adjective/verb (from digest Claims) | Formal definition | Measured by |
|---|---|---|
| "change-inducing" (comment) | $\exists f\in F_t$ posted after $c_t$ that edits lines overlapping $h_t$ | Deterministic diff/timestamp check in M1 |
| "implicit / unwritten" (constraint) | $k$ not expressible as any rule in the ruff∪pylint∪import-linter inventory $\mathcal{L}$: $\text{lintmap}(k)=\varnothing$ | Linter-expressibility rate (M3 / RQ1 metric) |
| "systematically extractable" | catalog-entry precision $\Pr[k\text{ genuine}]$ estimable with Wilson 95% CI whose lower bound clears the pilot gate | M5(a) dual annotation, n=300 |
| "genuine project constraint" | $\ge 3$ distinct threads and $\ge 2$ distinct reviewers support $k$ (supp$_k\ge3$) AND both annotators label it genuine | M3 support threshold + M5(a) |
| "violates" (patch violates $k$) | $J(p,k)=\text{violated}$ AND $J$ validated at κ≥0.6 vs. humans | M4 judge + M5(b) gate |
| "test-passing" (patch) | patch is in SWE-bench Verified fail-to-pass resolved set | SWE-bench harness (external) |
| "higher rate than human" | $\text{viol}_c(p^a) > \text{viol}_c(p^g)$ on matched pairs, McNemar-significant | RQ2 |
| "category-wise violation rate" | $\text{viol}_c=\frac{1}{|P|}\sum_p \mathbb{1}[\exists k: \text{cat}_k=c \wedge J(p,k)=\text{violated}]$ | RQ2 metric |

Every load-bearing adjective in the digest Claims list now has a computable definition or is dropped.

---

## Assumptions (A1..An)

> Each A\* below fills all five guidance.md §3.2 slots (assumption, failure_mode, detection, gate, consequence); `gate: PG-j` names the walking-skeleton pilot-gate check that clears it before scale-up (Step 9), or the later phase that does if no pilot check applies.

- **A1 (review channel carries constraints).** A non-trivial fraction of change-inducing review comments encode generalizable, project-level design rules (not only one-off bug fixes). *Fail mode:* comments are overwhelmingly one-off. *Detection:* pilot gate — extraction precision <0.5 on the n=100 candidate sample (digest N6 feasibility risk). *Gate:* PG-1 (pilot, before any RQ1 scale-up). *Consequence:* fails → RQ1 blocked wholesale; triggers Global fallback F-G1 (below) rather than a partial degrade, since every downstream catalog entry depends on this channel existing.
- **A2 (change-inducing ≈ enforced).** A later commit editing the anchored hunk is a valid behavioral proxy for "the reviewer's expectation was enforced." *Fail mode:* follow-up edits are cosmetic/unrelated. *Detection:* M5(a) precision + manual audit of a change-inducing sample during pilot. *Gate:* PG-2 (pilot, folded into the same n=100 audit as A1). *Consequence:* fails → RQ1(i)'s precision denominator is contaminated; restrict scope to manually-audited-clean threads only, narrowing RQ1's claimed repo coverage rather than blocking it outright.
- **A3 (compliance ⟂ tests).** Test-passing status carries no information about convention compliance (Step 0). *Fail mode:* tests already catch conventions, so B-alt zero-shot judge finds nothing. *Detection:* nonzero validated violation rate on test-passing patches in the walking skeleton. *Gate:* PG-3 (walking-skeleton pass criterion, Step 9). *Consequence:* fails → the paper's central asymmetry premise (Step 0) is empty; this is the placebo-style "why do this at all" failure and routes to Global fallback F-G1, not a degraded RQ2.
- **A4 (LLM judge alignable to humans).** An LLM judge can reach κ≥0.6 vs. dual human annotation on (patch, rule) pairs. *Fail mode:* κ<0.6. *Detection:* RQ2 judge-validity gate (n=400), pre-committed to block scaled labeling. *Gate:* PG-4 for a mini version (walking-skeleton arm 3, human confirmation of ~20 flagged violations); full gate at RQ2 scale before any category-wise number is reported. *Consequence:* fails → automated violation labels are not used at scale; fall back to the reduced manually-labeled sample only, and RQ2's claim narrows to that sample's size (CO2/CO4 degrade to a smaller-n, still-reported finding, never silently dropped).
- **A5 (matched human gold exists & is a fair reference).** Each agent patch has a human gold patch for the same issue (SWE-bench pairing). *Fail mode:* gold patches themselves violate at ceiling. *Detection:* B0 reference distribution in RQ2. *Gate:* checked at RQ2 (not pilot-gated; B0 is evaluated before any H\* is scored per goal.md §5 step 1). *Consequence:* gold patches at or near ceiling → B0 is non-null in effect (Part 4 situation 1 logic): CO4 is empty by construction and the run does not license an agent-vs-human gap claim regardless of RQ2's other numbers.
- **A6 (sufficient review volume).** Each pilot repo yields enough change-inducing threads (target ≥~2,000 sampled) for supp≥3 entries to exist. *Fail mode:* thin catalogs. *Detection:* walking-skeleton catalog-size check before full RQ2. *Gate:* PG-5 (skeleton pass criterion: ≥10 supp≥3 entries in the mini-catalog, Step 9). *Consequence:* fails for a specific repo → drop that repo from the pilot set rather than lowering the supp≥3 admission threshold; report per-repo catalog sizes so the drop is visible, not silent.
- **A7 (agent patches available, ≥3 systems).** Public SWE-bench leaderboard "experiments" repo supplies test-passing patches from ≥3 agent systems in the pilot repos. *Fail mode:* too few. *Detection:* skeleton data-availability check. *Gate:* PG-6 (skeleton, before the RQ2 sample is finalized). *Consequence:* fails → narrow RQ2's claim to however many agent systems are actually available (named explicitly), never silently substitute a single-system comparison for the pre-registered ≥3-system design.

---

## Step 6 — Pre-Registered Experiments

### RQ1 — Can implicit design constraints be systematically extracted from PR review comments? (digest N8 RQ1; tests CO1; addresses C1, C2)

- **Assumption:** A1, A2, A6.
- **Hypothesis (binary):** On the 5 pilot repos, (i) catalog-entry precision Wilson-95%-CI lower bound ≥ 0.60 on the n=300 dual-annotated sample; AND (ii) LLM extractor beats the keyword/directive baseline on paired thread-level detection, McNemar p<0.05 in the LLM-favoring direction, **with a minimum paired-accuracy gap of ≥8 percentage points as the effect floor** (significance without this floor does not satisfy (ii) — guidance.md §3.1); AND (iii) linter-expressibility rate < 0.50 (i.e., a strict majority of entries are genuinely unwritten).
- **Metric:** precision = (# entries labeled genuine)/(n sampled); recall proxy = (# annotator-mined constraints recovered)/(# annotator-mined) over 100 held-out threads; linter-expressibility = $\frac{1}{|K|}\sum_k \mathbb{1}[\text{lintmap}(k)\ne\varnothing]$; LLM-vs-keyword gap = paired thread-level detection accuracy(LLM) − accuracy(keyword baseline).
- **Verification:** Wilson 95% CI on precision and recall proxy; McNemar's test α=0.05 for LLM-vs-keyword, with the ≥8-point gap checked alongside significance; Cohen's κ reported for the dual annotation (report, not gate, for precision labeling). Pilot gate (precision ≥0.5 on n=100) must pass first.
- **Fallback (pre-committed wording):** "If precision clears 0.5 but not 0.60, we claim extraction is *feasible with human-in-the-loop verification* rather than fully automated, and report the achieved precision with its CI as the operating point. If linter-expressibility ≥0.50, we narrow the claim to 'a measurable minority of mined constraints are unwritten' and report the unwritten subset as the contribution. **If the LLM extractor does not clear (ii)'s bar — McNemar p≥0.05, or p<0.05 but the paired-accuracy gap is <8 points, or the direction reverses — we report that semantic (LLM-based) extraction is not shown to add value over lexical pattern-matching at this sample size, drop the 'LLM-based' framing from CO1's method claim, and retain only whatever precision/recall the (still-gated) pipeline achieves as an operating point.**"

### RQ2 — Which implicit-constraint categories do test-passing agent patches violate most? (digest N8 RQ2; tests CO2, CO4; addresses C3, C4, C5)

- **Assumption:** A3, A4, A5, A7.
- **Hypothesis (binary):** With judge validity established, over ~500 test-passing agent patches vs. matched gold: (i) category distribution is non-uniform, chi-square goodness-of-fit p<0.05 **with Cramér's V ≥ 0.15 as the effect floor** (significance alone does not satisfy (i) — guidance.md §3.1); AND (ii) $\text{viol}_{\text{EH}}>\text{viol}_{\text{API}}$ AND $\text{viol}_{\text{ARCH}}>\text{viol}_{\text{API}}$; AND (iii) agent violation rate exceeds human-gold rate in ≥1 category, McNemar p<0.05 with Holm–Bonferroni across the 3 categories, **by at least 8 percentage points (matched-pair rate difference) in every category where (iii) is claimed to hold** (the effect floor; a significant-but-<8-point gap is reported as "detected but small," not as satisfying (iii)).
- **Metric:** $\text{viol}_c$ as defined in Step 5; agent-vs-human delta = matched-pair difference per category; Cramér's V computed from the category × (uniform-expected) contingency table.
- **Verification:** Judge-validity gate first — LLM-judge-vs-dual-human κ ≥ 0.6 on n=400 (patch, rule) pairs, else automated labels are not used (fall to manual labeling of a reduced sample). Chi-square goodness-of-fit α=0.05 with per-repo stratified sensitivity analysis (patches non-independent within repo). Matched-pair McNemar per category, Holm–Bonferroni across 3 categories, α=0.05. Wilson CIs on all rates.
- **Power (guidance.md Part 6 item 9):** patches are stratified by repo × category × arm (agent/human-gold). Any repo × category cell with fewer than 20 test-passing patches is pre-declared **INCONCLUSIVE** for that stratum and excluded from the per-repo sensitivity table — never silently pooled into a null. The pooled (non-stratified) test is treated as the primary analysis only if at least 4 of the 5 pilot repos clear the n≥20-per-category threshold; otherwise the claim is explicitly narrowed to the named repos that clear it.
- **Mechanism analysis (R6, guidance.md Part 6 item 8):** beyond the headline category-wise rate, cross-tabulate validated violations against (a) agent-system identity — does any excess concentrate in specific agent systems rather than spreading uniformly across the ≥3 systems sampled (A7)? — and (b) patch size / files-touched — does violation likelihood scale with patch size, which would point to an exposure-opportunity confound rather than a genuine per-patch compliance gap? Reported as a secondary, non-gating analysis explaining the RQ2 distribution, not another gate on CO2/CO4.
- **Fallback (pre-committed wording):** "If the category ranking (ii) fails but non-uniformity (i) holds, we report the observed ranking as the empirical finding and drop the a-priori EH/ARCH>API prediction. If agent>human (iii) fails in all categories, we report that on this sample test-passing agents and humans are statistically indistinguishable on mined-constraint compliance — a direct, publishable bound on the size of the compliance gap (refines CO4 to a null with CI rather than asserting a gap). **If (i) itself fails — chi-square cannot reject uniformity, or V<0.15 — we report that, at this sample size, violations do not detectably concentrate by category: CO2's category-ranking claim is dropped as moot (not merely narrowed), (ii) is not evaluated, and only (iii)'s agent-vs-human comparison (if it independently clears its own gate) is retained.**"

### Mandatory baselines

- **B0 — "why do this at all" control:** *matched human gold patches as the reference violation distribution.* If test-passing human patches already violate mined constraints at the same rate as agents, there is no agent-specific compliance gap to characterize and CO4 is empty — this arm justifies the problem's existence. (digest N8 baseline #4.)
- **B-alt — strongest-alternative-explanation control:** *catalog-free zero-shot LLM judge* ("does this patch violate any project convention?" with no mined catalog; operationalized as the RLAC-style per-output latent-rubric protocol, borrowed as a comparison arm only — see the added cache entry `FromCorrectnesst2512`'s sibling method-twin for the taxonomy-side analogue). Rival explanation: "any capable LLM prompted to look for convention problems finds the same violations, so the mined catalog adds nothing — the signal comes from the judge, not the mining." This arm is budget/capability-matched (same judge model, same patches) and isolates the catalog's contribution. The catalog claim survives only if catalog-guided judging materially changes the violation set vs. catalog-free judging. (digest N8 baseline #3.)
  - **Pre-committed downgrade wording (guidance.md §3.3):** if catalog-guided and catalog-free judging materially agree on which patches violate which rules (the catalog-free arm recovers substantially the same violation set), that does **not** refute RQ2's orthogonality finding — test-passing still carries no compliance information either way, so CO2/CO4 may still stand on the catalog-free judge's own numbers. It **does** refute the catalog's specific contribution: the paper's real instrument would be "a capable LLM asked to look for problems," not the mined, multi-thread-supported catalog, and CO1/CO3 downgrade to "not demonstrated" while CO2/CO4 are evaluated on the catalog-free arm's numbers instead of the catalog-guided arm's.

### Global fallback F-G1

If the central hypothesis family fails (extraction precision cannot clear 0.5 even after the pilot-gate prompt revision, OR judge validity κ<0.6 blocks all automated measurement), pivot archetype from *measurement* to *negative-result / methodological*: **"We show that implicit design constraints in PR review history resist reliable automated extraction/judging at current LLM capability, quantify exactly where the pipeline breaks (candidate identification vs. deduplication vs. judging), and release the human-annotated corpus and failure taxonomy as the contribution."**

---

## Step 9 — Walking Skeleton

**One binary question:** *Do test-passing agent patches violate at least one human-confirmed mined constraint that catalog-free judging misses?* (Simultaneously exercises A3, A4, B-alt.)

- **Arms (3):** (1) catalog-guided LLM judge; (2) catalog-free zero-shot judge (B-alt); (3) human confirmation of flagged violations.
- **Smallest task set:** 1 pilot repo (django), ~200 change-inducing threads → a mini-catalog (supp≥3), applied to ~20 test-passing agent patches from 1 agent system + their 20 matched gold patches.
- **Deterministic metrics only:** # entries with supp≥3 (integer); # patches with ≥1 catalog-guided violation; # of those also flagged by catalog-free judge; # human-confirmed. No statistical tests at skeleton stage.
- **Expected cost/wall-clock:** ~1–2k LLM calls, < 1 day wall-clock, low tens of USD; ~1 annotator-day for confirmation.
- **Skeleton-passed criterion:** mini-catalog has ≥10 supp≥3 entries AND ≥1 human-confirmed agent violation exists that the catalog-free judge missed. If met, scaling to 5 repos × 3 agents × full samples is a **config change** (repo list, sample sizes, add annotators) — no new code paths in M1–M5. If not met, trigger the relevant fallback before any grid spend.

---

## Claim–Evidence Map

| Claim the abstract will make | Traces to | Status |
|---|---|---|
| Implicit constraints are systematically extractable into a per-repo catalog, precision-verified, no formal spec needed | RQ1 H(i); Step 5 "systematically extractable" | needs-experiment |
| A majority of mined constraints are genuinely unwritten (not linter-expressible) | RQ1 H(iii); Step 5 "implicit/unwritten" | needs-experiment (fallback-covered if minority) |
| LLM mining beats a keyword-directive baseline (≥8-pt paired-accuracy floor) | RQ1 H(ii) | needs-experiment (fallback: drop 'LLM-based' framing from CO1 if floor/significance/direction fails) |
| Test-passing agents violate constraints more than matched humans (tests insufficient proxy) | RQ2 H(iii); CO4; B0 | needs-experiment (fallback: null-with-CI) |
| Violations are category-non-uniform (Cramér's V≥0.15), EH/ARCH>API | RQ2 H(i),(ii) | needs-experiment (fallback: report observed ranking if only (ii) fails; CO2 dropped as moot if (i) itself fails) |
| The mined catalog adds signal over catalog-free judging | B-alt control | needs-experiment (fallback: pre-committed downgrade wording — CO1/CO3 fall, CO2/CO4 evaluated on catalog-free numbers, if no material) |
| Compliance is orthogonal to test-pass (asymmetry) | Step 0; A3; skeleton criterion | supported-by-design |
| Released catalog + violation-labeled patch set (CO3) | artifact deliverable | supported-by-design |

---

## Abstract v0 (draft, mechanism-first) — DRAFT BEFORE RESULTS

The requirements a maintainer enforces on a patch are settled in review dialogue but never written into the test suite, so a patch can pass every test while carrying no evidence at all about whether it obeys a project's error-handling, layering, and API conventions. We formalize such an unwritten constraint as a rule that (a) demonstrably induced a code change in review and (b) recurs across ≥3 threads and ≥2 reviewers, and mine a per-repository categorized catalog from PR review history with no pre-existing specification. We gate the mined catalog on human-annotated precision and gate an LLM compliance judge on agreement with blind human labels before any automated measurement counts. Applying the validated instrument to test-passing coding-agent patches from public SWE-bench submissions and their matched human gold patches, we measure the category-wise violation distribution and isolate the catalog's contribution against a catalog-free judge, quantifying how far test success falls short of design-constraint compliance.

*(≤150 words; opens on the orthogonality mechanism; verbs formalize/mine/gate/measure/isolate; no "increasingly used… however… we introduce" template.)*
