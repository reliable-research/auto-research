# C3 — "Green tests are not acceptance" — Structured Research Discussion

> **Full-paper framing (position = the paper's stance, not a position-track submission).**
> This document develops C3 as a FULL experimental measurement paper for an FSE/ICSE
> research track. The stance — green tests are not acceptance; evaluation and reward
> should be built on a review-adjusted acceptance oracle — is the paper's framing and
> motivation; the contribution is a measurement pipeline, a quantified/predicted gap,
> and an empirical evaluation of oracle variants. Everything below is implementable now.

**Thesis (stance).** Frontier coding agents saturate test-pass signals while failing
*acceptance* — human merge decisions conditioned on genuine review, static/design
analysis, post-merge survival. Test-pass is a defeated proxy; the replacement is a
**review-adjusted acceptance oracle** (`accepted := merged ∧ genuinely-reviewed ∧
survives(w)` — or, where merge outcomes are unavailable, its mechanized approximation
via deep static + design-constraint analysis).

**Contribution shape (full paper).** (C1) A ReactBench-style measurement pipeline: run
coding agents on real-repo tasks, take green-test outcomes, and cross-check them against
deep static analysis, design-constraint checkers, and — where available — real PR merge
outcomes. (C2) Quantification AND prediction of the test-pass-vs-acceptance gap: which
task/patch features predict green-but-unacceptable. (C3) An empirical evaluation of the
review-adjusted acceptance oracle against raw merge and raw test-pass as predictors of
ground-truth quality (post-merge survival / adjudicated acceptability).

**Sources:** `position_paper_pipeline_2026-08.md` (candidate "Green tests are not
acceptance", novelty ledger row 3), `industry_signal_scan_2026-08.md` §1, B1/T5 digests
(verifier insufficiency; T5.2 "why tests cannot see design" supplies the
design-constraint checkers).

**Discussion protocol:** 6 stages; each carries one critic pass (strongest objection)
and one refined resolution. Stage 0 is a hard gate. Tags: [VERIFIED] = arXiv ID
independently located in the 2026-08-13 web sweep or read in full earlier;
[NEEDS-VERIFICATION] = channel-relayed, primary source not yet located/read.

---

## Stage 0 — Primary-source verification gate (HARD BLOCKER)

**All three headline motivating figures are channel-relayed, and the 2026-08-13 sweep
FAILED to locate two of them (60.8%, 31.3%).** Per the repo's standing rule, no relayed
statistic enters a draft without primary-source verification. For the full-paper framing
this gate matters twice: the figures motivate the study, and the ReactBench artifact (if
it exists publicly) is a candidate baseline/pipeline component to build on or differ from.

**Documents to locate and read in full:**

| # | Claimed figure | Claimed source | Where to look | Status |
|---|---|---|---|---|
| V1 | Agent PRs merged at ~half the human rate despite passing the same tests | **METR RE-bench PR-merge data** (relayed via `bestpartners`, kb6e0udcGVA) | metr.org reports/blog; RE-bench paper + appendices; METR GitHub; the analysis may live in a separate METR "AI PRs in the wild" report rather than RE-bench itself | [NEEDS-VERIFICATION] |
| V2 | 60.8% of Fix tasks green-on-tests but fail deep static analysis (React-Doctor); 8,415 runs / 51 repos; more reasoning effort *reduced* the score | **ReactBench paper/repo** (relayed via `whycallqq`, duBYfrZ7Yoo) | arXiv full-text "ReactBench"+"React-Doctor"; GitHub search; the tool name is the distinctive key. If found, also assess artifact reusability for our pipeline | [NEEDS-VERIFICATION] |
| V3 | 31.3% of AI PRs merged with zero review; defect rate 9%→54% on those | **Faros AI telemetry report** (4,000 teams; relayed via `whycallqq`, j5x5SLW0xGQ) | faros.ai blog/whitepapers; press citing Faros; the 4,000-team cohort is the search key | [NEEDS-VERIFICATION] |

**Verified fallback set (located in sweep; full read before citing):**
- [VERIFIED] arXiv:2606.18168 ("All Smoke, No Alarm") — 80.2% of agent-PR test files
  carry weak/no oracle signals.
- [VERIFIED] arXiv:2601.00753 — 28.3% of agentic PRs merged immediately (zero-review
  analogue); its PR corpus is also a candidate dataset for RQ3.
- [VERIFIED] arXiv:2605.22534 — 35.7% of agent-PR rejections are non-agentic in cause;
  load-bearing for the review-adjustment design, already verified.
- [VERIFIED] arXiv:2506.09289 (UTBoost) — ~31% lucky passes under strengthened suites.

**Decision rule.** Verification outcome changes the *introduction and baselines*, not the
study: if V2's ReactBench exists publicly, we position as generalization + prediction +
oracle-evaluation beyond it (and reuse what's reusable); if it does not, our pipeline is
the first public instrument of this kind and the relayed figures are dropped (not hedged).
V1/V3 verify → motivation leads with them; fail → verified set leads.

**Critic:** The gate treats verification as retrieval, but the risky outcome is *partial*
verification — a Faros number with a self-selected cohort, a METR gap holding only in one
PR-size band, or a ReactBench that measures something subtly different (e.g., lint density,
not "deep static analysis"). A located-but-mismatched source that we cite anyway is worse
than an unlocated one. Also, for the full-paper framing there is a new failure mode the
position framing didn't have: if ReactBench exists AND already does prediction, C2's
novelty shrinks — the gate must check that, not just the number.

**Refined:** Three-check pass per item: (1) locate primary document; (2) confirm number,
denominator, and cohort match the claim as we would state it — if not, restate to match
the source and re-check the restated claim still motivates the study; (3) extract the
source's own limitations into our threats section. Plus, for V2 only, a fourth check:
a novelty-delta audit of the located artifact (does it do feature-level prediction? does
it evaluate oracle variants? does it touch merge outcomes?) — the answers set C2/C3's
claimed deltas. The fallback set gets the same three-check pass (its [VERIFIED] tag
certifies sweep-level location, not full read); reads are logged in `sources/` notes in
this directory. No number enters the draft with fewer than all checks passed.

---

## Stage 1 — Problem definition

**The wrong practice/belief.** The field operationalizes "the agent solved the task" as
"the repository's tests pass": benchmark resolved-rates, RLVR reward on test outcomes
(0→66 papers in the ACL corpus trend), and auto-merge-on-green deployment gates. The
implicit belief: test-pass is a sufficient acceptance proxy whose residual error is a
maturity artifact that better models will shrink.

**Who holds it.** Benchmark builders (leaderboards define progress by resolved-rate);
RL/post-training teams (test outcomes as the verifiable reward substrate); engineering
orgs adopting agent auto-merge; implicitly, every paper whose headline claim is a
resolved-rate.

**The measurement problem (method-free statement).** For coding-agent patches that pass
the repository's tests: (a) *how often* and *by which mechanisms* are they nonetheless
unacceptable (design violations, deep static defects, human rejection, post-merge
failure)? (b) *what predicts it* — which task and patch features separate
green-and-acceptable from green-but-unacceptable? (c) *which oracle* — raw test-pass,
raw merge, or review-adjusted acceptance — best tracks ground-truth acceptability?

**Formal objects.** Task instance t (repo, issue, test suite); agent patch p with
green(p) = 1; acceptance layers A = {deep static verdict, design-constraint verdict,
merge outcome, review-adjusted merge outcome, survival(w)}. Gap rate
G_A = P(¬acceptable_A | green) per layer; predictor f: features(t,p) → P(gap);
oracle quality = agreement of each candidate oracle with a held-out ground-truth
adjudication.

**What replaces the belief if the stance holds.** Resolved-rate claims require an
acceptance-calibration statement; reward design moves to acceptance-grounded terminal
signals with tests as shaping. (This prescription is the discussion section, not a
contribution claim — the contributions are the pipeline, the quantified/predicted gap,
and the oracle evaluation.)

**Critic:** The problem statement mixes two studies with different ground truths and
pretends they are one: (a)/(b) use mechanized checkers as the acceptance proxy on tasks
*we run agents on*, while (c) needs real merge/review outcomes, which only exist for
PRs *actually submitted to real projects* — you cannot ethically or practically get
merge outcomes for 8,000 lab-run patches. As stated, "acceptance" quietly changes
referent between RQ1/RQ2 and RQ3, which a reviewer will call construct-validity
laundering. Also `acceptable` is undefined independent of the oracles being compared —
circularity risk in (c).

**Refined:** The design is made explicitly **two-track with a bridge**, and the problem
statement now says so. **Track L (lab):** agents run on real-repo tasks; acceptance
layers are mechanized (deep static + design-constraint checkers) plus a sampled human
adjudication panel — this powers RQ1/RQ2 at scale. **Track F (field):** mined corpora of
real agent PRs with merge/review/survival telemetry (2601.00753 / 2605.22534 corpora +
fresh GitHub mining) — this powers RQ3, where ground truth is post-merge survival and
sampled human adjudication, never the compared oracles themselves (circularity broken:
oracles are compared on their agreement with survival + adjudication, not with each
other). **Bridge:** the RQ2 predictor is trained on Track L features and validated on
Track F (do the same features predict rejection/short survival in the field?) — the
bridge result is what licenses treating the two referents as one construct. Construct
scope is stated: "acceptance" = the family of post-green quality verdicts, with each
result labeled by layer.

---

## Stage 2 — Motivation: why now

**Why this is binding in 2026.** (1) Saturation: frontier agents clear test thresholds
routinely, so the proxy's residual error is now the dominant error term. (2) Exposure at
scale: agent PRs enter real repos at platform scale — acceptance telemetry exists as a
population signal for the first time. (3) RLVR crystallization: verifiable-reward RL went
0→66 papers in the ACL corpus; the field is hard-coding the proxy into training loops
*now*. (4) No public instrument exists that measures the gap across layers, predicts it,
or evaluates replacement oracles — the measurements that do exist are single-layer.

**Binding evidence, tagged:**
1. [NEEDS-VERIFICATION] METR RE-bench PR-merge data: agent PRs merged at ~half human
   rate despite same tests. Role: cleanest eval-layer gap statement.
2. [NEEDS-VERIFICATION] ReactBench: 60.8% green-but-fail-deep-static; reasoning effort
   *reduced* the score. Role: gap is mechanized-detectable and worsens with the field's
   favorite lever — the sharpest "structural, not maturity" datum if it verifies; also
   the direct methodological ancestor of Track L.
3. [NEEDS-VERIFICATION] Faros telemetry: 31.3% zero-review merges; defect 9%→54%.
   Role: raw merge is corrupted — motivates review-adjustment (RQ3).
4. [VERIFIED] arXiv:2606.18168 — 80.2% weak/no-oracle test files in agent PRs. Role:
   green is often not even green.
5. [VERIFIED] arXiv:2601.00753 — 28.3% immediate merges. Role: verified zero-review
   analogue; candidate Track F corpus.
6. [VERIFIED] arXiv:2605.22534 — 35.7% non-agentic rejections. Role: raw rejection is
   noisy too — the second jaw of review-adjustment.
7. [VERIFIED] arXiv:2506.09289 (UTBoost) — ~31% lucky passes. Role: within-benchmark
   confirmation of the same shape.
8. [VERIFIED, corpus] RLVR 0→66 trend; T5.2 mechanism (tests cannot encode design
   intent). Role: urgency + the structural mechanism our checkers operationalize.

**Critic:** The motivation's three most vivid numbers are the three unverified ones, and
the "no public instrument exists" claim (point 4) is exactly what Stage 0 might refute
(if ReactBench is public, an instrument exists for one layer/one framework). Claiming it
before the gate closes is writing a check the gate may bounce. The RLVR-urgency point
also overreaches: many RLVR pipelines reward purpose-built verifiers, not repo suites.

**Refined:** Motivation made load-bearing on verified items only: 4+5+6+7 establish
"the oracle is weak, the field signal exists but is noisy in both directions, and no
work measures across layers or evaluates corrected oracles" — sufficient alone. Items
1–3 are amplifiers with disclosed status, included iff they pass Stage 0. Point 4 is
restated conditionally and resolved by the gate: "no *cross-layer, predictive,
oracle-evaluating* instrument exists" — a claim that survives even if ReactBench is
public (single-layer, single-framework, descriptive), with the V2 novelty-delta audit
supplying the precise wording. The RLVR claim is scoped: "wherever the reward verifier
is a test suite — a documented and growing instance — the Goodhart argument applies."

---

## Stage 3 — Related-work positioning

Novelty-ledger discipline: for each named occupant, one concede-and-claim sentence;
deltas must be operational (what we measure that they don't).

**O1. Verification Horizon, arXiv:2606.26300** (closest on the reward side).
*Concede:* they own the diagnosis that verifiers and agents co-evolve with no static
silver bullet, and their "users are the most faithful verifiers" gestures at our layer.
*Claim:* they present an argument with no acceptance-gap data and no oracle
construction; we contribute the measurements and the empirical oracle comparison their
argument needs — including the datum their framing cannot supply: whether reviewed
acceptance actually outpredicts strengthened test suites (RQ3).

**O2. Wang et al., humans-are-not-reward-models caveat** (counter-foil).
*Concede:* individual human judgments are noisy, inconsistent, costly — correct, and our
own evidence (35.7% non-agentic rejections, zero-review merges) *confirms* it for raw
merge signals. *Claim:* review-adjusted acceptance uses already-produced organizational
artifacts, aggregated and survival-conditioned, and RQ3 empirically tests whether the
adjustment rescues the signal — we convert their caveat from an objection into a
measurable design requirement and report whether it is met.

**O3. All-Smoke-No-Alarm, arXiv:2606.18168.**
*Concede:* they own the finding that agent-PR test files are weak-oracled (80.2%).
*Claim:* they audit the tests agents write; we measure what green tests *miss* across
acceptance layers on agent patches, predict it, and evaluate replacement oracles.

**O4. UTBoost, arXiv:2506.09289.**
*Concede:* they own within-suite repair (strengthened tests expose ~31% lucky passes).
*Claim:* suite-strengthening is one rung of the ladder; we measure the rungs above it
(design constraints, review-adjusted merge, survival) and test whether they contain
signal that strengthened suites still miss.

**O5. ReactBench (if it verifies at Stage 0).**
*Concede:* methodological priority on green-vs-deep-static measurement at scale for
React. *Claim:* we generalize beyond one framework, add design-constraint and field
(merge/survival) layers, add feature-level *prediction* of the gap, and add the oracle
evaluation; exact delta wording fixed by the Stage 0 novelty-delta audit.

**O6. Mining studies, arXiv:2601.00753 / arXiv:2605.22534.**
*Concede:* they own the field measurements (28.3% immediate merges; 35.7% non-agentic
rejections). *Claim:* they report the noise descriptively; we use it constructively —
their corpora become Track F, and the noise rates become the design parameters of the
review adjustment we then evaluate.

**O7. Benchmark-misalignment cluster (arXiv:2606.17799 et al., ~15 occupants).**
*Concede:* "benchmarks misalign with practice" is thoroughly taken; we do not lead with
it. *Claim:* we deliver what the cluster lacks — an instrument, a predictor, and an
oracle comparison; complaint → measurement.

**Critic:** Two soft spots. First, the O5 concede-and-claim is written before Stage 0
resolves what ReactBench even is — if it turns out to include multi-framework or
predictive components, three of our four claimed deltas evaporate and the related-work
section as drafted overpromises; the positioning cannot be finalized on a relay. Second,
against O3/O4/O6 the individual deltas are each incremental ("they did X on tests, we do
X on more layers") — a reviewer can say the paper is a conjunction of small extensions.
The positioning lacks the one sentence that makes the whole more than its parts.

**Refined:** O5 positioning is explicitly gated: the related-work paragraph for
ReactBench carries two pre-written variants (exists-public vs. unverifiable), selected at
M1 by the Stage 0 fourth check; deltas that the audit kills are deleted, not weakened.
The conjunction objection is answered by promoting the *cross-layer design itself* to the
headline delta, stated once and reused everywhere: prior work measures single layers in
isolation (tests: O3/O4; field outcomes: O6; static: O5); no prior work can therefore
answer the question that matters — *whether the layers agree, which layer's disagreement
predicts real-world rejection/failure, and which oracle to trust* — and answering it
requires exactly the two-track + bridge design of Stage 1. The contribution is the
comparative measurement, not the union of per-layer measurements.

---

## Stage 4 — Sub-problems

Each: claim → evidence → weakest point. These are the paper's RQ-level joints; SP2 is
the mandated review-adjustment core.

**SP1 — The gap is real, large, and layered (RQ1: quantify).** Green patches fail deeper
acceptance layers at substantial, layer-specific rates; the layers disagree with each
other (a patch can pass strengthened tests yet violate design constraints, and vice
versa), so no single mechanized layer subsumes the others.
*Evidence:* [VERIFIED] 2606.18168, 2506.09289 (test layer); [VERIFIED] 2601.00753,
2605.22534 (field layer); [NEEDS-VERIFICATION] ReactBench (static layer);
T5.2 checkers make the design layer measurable.
*Weakest point:* mechanized checkers have false positives — "fails deep static analysis"
may overstate unacceptability. Mitigation: the sampled human-adjudication panel
calibrates each checker's verdict against human judgment; gap rates are reported both
raw and adjudication-calibrated.

**SP2 — [MANDATORY CORE] Raw merge is a noisy and hackable oracle; review adjustment
measurably fixes it (RQ3: oracle evaluation).** Raw merge as metric or reward imports
false accepts (zero-review merges: [VERIFIED] 28.3% immediate per 2601.00753;
[NEEDS-VERIFICATION] Faros 9%→54% defect rate on zero-review) and false rejects
(non-agentic rejections: [VERIFIED] 35.7% per 2605.22534). It is also hackable as a
reward: optimizing merge probability favors small, innocuous, review-evading changes.
Claim to test: the review-adjusted oracle (`merged ∧ genuinely-reviewed ∧ survives(w)`)
agrees with ground truth (survival + adjudication) strictly better than raw merge and
raw test-pass, and re-ranks agents relative to test-pass rankings.
*Weakest point:* "genuinely-reviewed" is operationally fuzzy (rubber-stamp approvals sit
above zero-review) and survival windows import their own noise (late defects,
non-quality reverts). Mitigation: treat the adjustment as a parameterized family
(review-depth threshold × window w), report oracle quality across the grid, and test
the dominance claim at the *crudest* setting — if even crude adjustment beats raw
signals, the position holds without resolving the fuzziness.

**SP3 — The gap is predictable from task/patch features (RQ2: predict).** Features —
task type (fix/feature/refactor), patch size and locality, files-touched centrality,
test-delta character (per 2606.18168's weak-oracle taxonomy), dependency footprint,
model/agent framework, reasoning budget — predict green-but-unacceptable well above
base rate; the predictor transfers from Track L to Track F (the bridge).
*Evidence:* feature families are all extractable with existing tooling; 2605.22534's
rejection-cause taxonomy supplies field labels; no prior work attempts this
(prediction is the clearest open cell in the ledger, pending the V2 audit).
*Weakest point:* transfer may fail — lab checker-verdicts and field merge-outcomes are
different constructs (Stage 1 critic). A failed bridge does not kill the paper (per-track
predictors are still contributions) but it kills the strongest headline; the design must
pre-register both outcomes as reportable.

**SP4 — The gap does not shrink with capability or reasoning effort (dose-response;
tests the "structural, not maturity" stance).** Across model tiers and reasoning budgets,
green rates rise but layered gap rates G_A do not fall — or fall much more slowly — and
(if the relayed ReactBench signal is real) some layers *worsen* with reasoning effort.
*Evidence:* [NEEDS-VERIFICATION] ReactBench's reasoning-effort datum; the T5.2 mechanism
argument (tests can't encode intent) predicts flat G_design; our Track L runs measure it
directly across {model tier} × {reasoning budget}.
*Weakest point:* a clean dose-response needs enough budget levels and runs per cell —
compute-expensive; and a null (gap shrinks with capability) partially undercuts the
stance. Mitigation: SP4 is framed as a genuine test, not a confirmation — either
outcome is publishable (see Stage 6 verification criteria), and the cell grid is sized
to the compute we have (2 tiers × 3 budgets minimum).

**Critic:** The set has a scope-creep problem and a hidden dependency chain. Four RQs ×
two tracks × an adjudication panel × a parameter grid is a 12-month study wearing a
6-month plan's clothes; SP3's bridge depends on SP1's calibrated checkers AND SP2's
field labels, so a slip anywhere lands on the headline claim. Nothing in the set is
staged as a minimum publishable core vs. extensions. Also, SP2's "hackable as reward"
limb has no experiment behind it anywhere in the design — it's asserted, not measured,
and a reviewer will notice the one unmeasured claim in a measurement paper.

**Refined:** The sub-problems are re-staged as core vs. extension. **Core (minimum
publishable unit): SP1 + SP2** — the cross-layer gap quantification (Track L + Track F
descriptive) and the oracle evaluation on Track F; this alone is a full paper (first
cross-layer measurement + first empirical oracle comparison). **Extension 1: SP3**
(prediction + bridge) — started only once core data exists, since it reuses core
features/labels. **Extension 2: SP4** (dose-response) — a Track L re-run grid, purely
additive compute. The dependency chain is thereby linearized: core needs no bridge and
no grid. SP2's reward-hackability limb is explicitly downgraded from claim to
*motivated conjecture* stated in discussion (measuring RL reward-hacking would need
training runs — out of scope, honestly labeled, and named as future work connecting to
B1.2/T5.1); the paper's measured claims are confined to oracle quality, not training
dynamics.

---

## Stage 5 — Argument architecture (paper skeleton)

Target form: FSE/ICSE research-track full paper (~11 pp + refs). Each section names its
load-bearing exhibit.

- **§1 Introduction.** Stance-first: green ≠ accepted; the field optimizes a defeated
  proxy; we build the instrument, measure the gap across layers, predict it, and
  evaluate the corrected oracle. Contributions C1–C3 + artifact.
  *Load-bearing exhibit:* **Figure 1 — the oracle ladder** (test-pass → strengthened
  suites → deep static → design constraints → raw merge → review-adjusted acceptance),
  each rung annotated with the prior work that defeats the rung below (UTBoost,
  All-Smoke-No-Alarm, mining studies) and the rungs this paper measures — related-work
  positioning rendered spatially.
- **§2 Background & motivating evidence.** The verified evidence matrix; RLVR context;
  Stage-0-gated relays if admitted.
  *Load-bearing exhibit:* **Table 1 — evidence matrix**: study × layer × population ×
  figure × what it defeats (verification status carried in the artifact).
- **§3 Study design.** Two-track + bridge design; task/repo selection; agent matrix;
  acceptance layers and checkers; adjudication protocol; oracle family definition;
  threats-by-design.
  *Load-bearing exhibit:* **Figure 2 — pipeline diagram**: tasks → agents → green filter
  → layer checkers / field telemetry → adjudication → metrics; the artifact's map.
- **§4 RQ1 results: the layered gap.** Gap rates G_A per layer, per task type, per
  agent; layer-agreement analysis (the headline "layers disagree" matrix).
  *Load-bearing exhibit:* **Figure 3 — layer-agreement heatmap** (pairwise agreement
  among test/static/design/merge verdicts on the same patches) + gap-rate table with
  adjudication-calibrated columns. This is the paper's money figure: if layers agreed,
  the whole stance collapses — visible at a glance that they don't.
- **§5 RQ3 results: oracle evaluation.** Oracle-vs-ground-truth agreement (raw
  test-pass vs raw merge vs review-adjusted grid); agent re-ranking under each oracle
  (Kendall τ vs test-pass ranking).
  *Load-bearing exhibit:* **Table 2 — oracle quality table**: precision/recall/AUROC
  against survival+adjudication ground truth, with the crudest-adjustment row bolded
  (the dominance claim), plus the re-ranking τ column.
- **§6 RQ2 results: prediction + bridge (extension).** Feature importance;
  Track L→F transfer AUROC.
  *Load-bearing exhibit:* **Figure 4 — predictor performance + transfer bars**, with
  the feature-importance panel naming the top green-but-unacceptable predictors.
- **§7 RQ4 results: dose-response (extension).** G_A vs model tier × reasoning budget.
  *Load-bearing exhibit:* **Figure 5 — dose-response curves**: green rate rising, gap
  rates flat/rising per layer — the "structural, not maturity" visual.
- **§8 Discussion.** Implications for benchmark reporting (acceptance-calibration
  statements), reward design (terminal vs shaping; the downgraded hackability
  conjecture), Wang-et-al. constraint satisfied; connection to B1.2/T5.1/T5.2.
- **§9 Threats.** Checker false positives (calibrated), construct drift between tracks
  (bridge as the test), repo/framework selection, single-window survival.
- **§10 Related work.** Stage 3 occupants with the cross-layer headline delta.

**Critic:** The skeleton buries the paper's most decisive result: §5 (oracle evaluation)
is the novelty ledger's open cell and the stance's empirical payoff, but it sits after a
long §4 and reads as one result among four — reviewers skimming §4's descriptive gap
rates may pattern-match to "yet another gap-measurement paper" (O7's crowded cluster)
before reaching the oracle comparison. Also five figures + two tables exceeds a typical
11-page budget once §3's design section takes its necessary space, and extensions
(§6–§7) are laid out as if guaranteed, contradicting Stage 4's core-vs-extension
staging.

**Refined:** §4 and §5 are merged into a single results arc titled by the question
("What should replace green tests?"): 4.1 the layers disagree (heatmap), 4.2 which
signal tracks ground truth (oracle table) — so the descriptive gap is immediately cashed
out as the oracle comparison, and the intro's contribution ordering leads with C3 (oracle
evaluation) over C1 (pipeline). Exhibit budget: Fig 1 (ladder) absorbs Table 1's content
as annotations (as in the earlier framing); Fig 2 compressed to half-column; core
exhibits = ladder, pipeline, heatmap, oracle table; Figs 4–5 marked [extension] in the
plan and included as sections 5–6 only if Stage 4's extensions land by the freeze
milestone — the skeleton carries an explicit fallback pagination for the core-only
paper. This also de-risks the "yet another gap paper" read: the paper's title and intro
lead with the oracle question, not the gap.

---

## Stage 6 — Validation plan (concrete implementable experiment spec)

### Datasets & materials (build order within each)

**Track L (lab runs):**
- **Tasks/repos:** start from SWE-bench-Verified-style real-repo fix tasks for
  comparability, then extend with fresh issues mined from active OSS repos (target:
  ≥40 repos, ≥2 language/framework ecosystems — Python + TypeScript/React — to escape
  the single-framework ceiling; ≥800 tasks core, more if compute allows).
- **Agents:** 2–3 open scaffolds (e.g., SWE-agent/OpenHands-class) × 2–3 model tiers;
  reasoning-budget knob exposed for SP4.
- **Acceptance-layer checkers:** (i) strengthened-suite layer via UTBoost-style test
  augmentation where available; (ii) deep static layer: CodeQL + Semgrep + ecosystem
  linters at max depth (and React-Doctor if V2 verifies and releases it); (iii) design-
  constraint layer: T5.2's checker family (architecture-rule and design-intent checks —
  dependency direction, layering, API-contract conformance) — this layer is the repo's
  differentiating asset; (iv) adjudication panel: stratified sample (~300 patches,
  2 raters + tiebreak, rubric published) calibrating every mechanized layer.

**Track F (field corpora):**
- 2601.00753's agentic-PR corpus and 2605.22534's rejection corpus (availability checked
  at M1; both verified to exist as papers), plus fresh mining of agent-authored PRs
  (agent-bot author heuristics per those papers) with: review metadata (reviewer count,
  comment depth, time-to-merge), merge outcome, and survival signals (reverts,
  defect-linked issues touching the patch within w ∈ {30, 90} days).

### Metrics
- **RQ1:** gap rate G_A per layer (raw + adjudication-calibrated), with 95% CIs
  (cluster-bootstrapped by repo); pairwise layer agreement (Cohen's κ) — the heatmap.
- **RQ3:** oracle quality = AUROC / precision / recall of each oracle (test-pass, raw
  merge, review-adjusted grid: review-depth ∈ {any, ≥1 substantive comment, ≥2
  reviewers} × w ∈ {30, 90}) against ground truth (survival ∧ adjudication on the
  sampled stratum); agent re-ranking Kendall τ vs test-pass ranking.
- **RQ2:** predictor AUROC (gradient-boosted trees + logistic baseline, repo-held-out
  CV); Track L→F transfer AUROC; feature importances.
- **RQ4:** slope of G_A across model tier and reasoning budget (2 tiers × 3 budgets
  minimum, ≥100 tasks per cell), with green-rate curves for contrast.

### Falsification conditions
- **F1 (gap):** if adjudication-calibrated G_A < ~5% on every layer, the gap is
  ignorable and the stance dies (see kill criteria).
- **F2 (layer disagreement):** if all mechanized layers agree at κ > 0.8 with the test
  layer, "layered acceptance" adds nothing over strengthened suites — UTBoost wins.
- **F3 (oracle):** if the crudest review-adjusted oracle does not beat raw merge AND
  raw test-pass against ground truth, SP2's dominance claim is false.
- **F4 (prediction):** if the best predictor's AUROC < 0.65 in-track, the gap is
  unpredictable noise; if it transfers at < 0.6, the bridge fails (reportable but
  demotes the headline).
- **F5 (dose-response):** if G_A falls proportionally with green-rate gains across
  tiers, the maturity hypothesis wins over the structural stance.

### Anticipated reviewer attacks & responses
- **A1: "Checker verdicts aren't 'unacceptable' — static analyzers whine."** The
  adjudication panel calibrates every layer; all headline rates reported
  adjudication-calibrated; raw rates in appendix.
- **A2: "ReactBench already did this."** Stage-0 gated positioning: if it verifies, our
  deltas are cross-layer + field track + prediction + oracle evaluation (whichever
  survive the novelty-delta audit); if not, no public instrument exists — either
  branch pre-drafted.
- **A3: "Lab checkers and field merges are different constructs."** Conceded by design —
  the two-track + bridge architecture exists precisely to test construct transfer
  rather than assume it; results labeled by layer throughout.
- **A4: "Wang et al.: humans aren't reward models."** RQ3 is the empirical answer: we
  measure whether review-adjustment rescues organizational judgment as a signal, and
  the crudest-adjustment dominance test quantifies it; their caveat is our design
  requirement, and our F3 can vindicate them.
- **A5: "Survival ground truth is confounded (reverts for non-quality reasons)."**
  Ground truth is survival ∧ adjudication on the sampled stratum, never survival alone;
  window sensitivity (30 vs 90d) reported.
- **A6: "Compute/scale too small for the agent matrix."** Core claims (RQ1/RQ3) are
  powered by patch counts, not cell counts; the cell grid matters only for RQ4, which
  is an explicitly staged extension.

**Critic:** The spec still hides its two most failure-prone dependencies. First, the
design-constraint checker layer "T5.2's checker family" is a repo asset that exists as
topic-sketch machinery, not as a hardened tool — if it isn't runnable across 40 repos,
layer (iii) silently degrades to off-the-shelf linters and the paper loses its most
differentiated layer. Second, Track F's fresh mining assumes agent-authored PRs are
identifiable and their review metadata is rich enough for the review-depth grid; both
corpora papers note identification heuristics are lossy. Neither risk has a scheduled
early check, and the adjudication panel (300 patches × 2 raters) has no stated source
of raters or rubric-validation step — the single most attackable methods paragraph.

**Refined:** Three de-risking gates added to the build order, all before the data freeze:
**G1 (M1): checker bake-off** — run all three mechanized layers on a 20-patch pilot
across 5 repos; T5.2's design checkers must produce adjudication-agreeing verdicts on
the pilot or the design layer is scoped to the repo subset where they run (reported as
such, not silently degraded). **G2 (M1): Track F feasibility probe** — pull 200
candidate agent PRs via the corpora's heuristics, measure identification precision by
hand-audit of 50, and count how many carry review metadata sufficient for the depth
grid; if < 60%, the review-depth grid collapses to the binary zero-review split (the
crudest adjustment — which SP2's dominance claim was already designed to survive on).
**G3 (M2): adjudication dry run** — rubric drafted from 2605.22534's rejection-cause
taxonomy, two raters calibrate on 30 patches, κ ≥ 0.6 required before the full panel;
raters = project members + recruited SE-grad annotators, budgeted. Each gate has a
degraded-mode outcome specified in advance, so no failure is silent.

---

## Venue plan

1. **Primary: FSE 2027 research track** (full paper; check exact deadline at M1 — FSE
   full-paper deadlines have run ~Mar for the following year) — best fit for a
   measurement + instrument + oracle-evaluation paper with a strong artifact.
2. **Alternate: ICSE 2028 research track (~Mar–Apr 2027 deadline)** if the extension
   RQs (prediction, dose-response) are worth the extra months — the fuller paper at the
   later venue.
3. **Early stake (optional, compatible):** the *stance + design + pilot numbers* as an
   ICSE 2027 NIER 4-pager (Oct 23, 2026) purely to timestamp the framing against the
   monthly-publishing occupant space, without the full results; the full paper remains
   the deliverable. Decide at M1 based on pilot-gate results.
4. **Artifact:** pipeline + checker configs + adjudication rubric + corpora scripts as
   an FSE/ICSE artifact submission (availability + reusability badges).

## Time-to-draft estimate (3 milestones)

- **M1 — Gates closed, pilot done (target: +4 weeks, ~Sep 10, 2026).** Stage 0
  three-check (+V2 novelty-delta) pass complete; fallback sources full-read into
  `sources/`; G1 checker bake-off and G2 field-feasibility probe done with
  degraded-mode decisions recorded; task/repo list frozen; NIER-timestamp decision made.
- **M2 — Core data frozen (target: +12 weeks, ~Nov 5, 2026).** Track L core runs
  (≥800 tasks × agent matrix) executed and layer-checked; Track F corpus assembled with
  review/survival fields; G3 adjudication panel complete; RQ1 heatmap and RQ3 oracle
  table computed on frozen data; go/no-go on extensions (RQ2 bridge, RQ4 grid) with
  remaining compute.
- **M3 — Full draft + artifact (target: +20 weeks, ~Jan 2027).** Extensions landed or
  cut per M2 decision; paper drafted to the Stage 5 refined skeleton;
  se-paper-reviewer + novelty-auditor passes (defensive, against O1/O5 by name);
  artifact packaged; submission-ready ahead of the FSE 2027 window.

---

## Closing block

**One-sentence falsifiable hypothesis.** For frontier coding agents on real-repository
tasks, test-green patches fail deeper acceptance layers (deep static, design-constraint,
reviewed-merge, post-merge survival) at rates that adjudication confirms are
substantial (≥15% on at least one layer), are predictable from task/patch features
(AUROC ≥ 0.65), and are better tracked by a review-adjusted acceptance oracle than by
raw merge or raw test-pass (higher AUROC against survival-plus-adjudication ground
truth, even at the crudest adjustment) — and these gap rates do not shrink
proportionally with model capability or reasoning budget.

**Implementation checklist (build order).**
1. Stage 0 verification sweep: V1 METR / V2 ReactBench (+novelty-delta audit) / V3
   Faros; full-read the four verified fallbacks; log `sources/` notes.
2. G1 checker bake-off: CodeQL/Semgrep/linters + T5.2 design checkers on 20-patch ×
   5-repo pilot; record degraded-mode decision for the design layer.
3. G2 Track F feasibility probe: 200 candidate agent PRs, hand-audit 50, count
   review-metadata coverage; fix the review-depth grid (full vs binary).
4. Freeze task/repo list (≥40 repos, 2 ecosystems, ≥800 core tasks) and agent × model
   matrix; build the run harness (agents → patches → green filter → layer checkers).
5. Execute Track L core runs; assemble Track F corpus (corpora + fresh mining with
   review/survival fields).
6. G3 adjudication: rubric from the 2605.22534 taxonomy, 30-patch calibration
   (κ ≥ 0.6), then the ~300-patch stratified panel.
7. Compute RQ1 (gap rates + layer-agreement heatmap) and RQ3 (oracle-quality table +
   re-ranking τ) on frozen data.
8. Extensions per M2 go/no-go: RQ2 predictor + Track L→F bridge; RQ4 tier × budget
   dose-response grid.
9. Write to the Stage 5 refined skeleton; internal review passes; package artifact;
   submit.

**Verification criteria — what publishes vs. what kills it.**
- **Publishes (headline):** adjudication-calibrated gap ≥15% on ≥1 layer; layer
  disagreement (κ < 0.8 between test layer and at least one deeper layer); crudest
  review-adjusted oracle beats both raw merge and raw test-pass on ground-truth AUROC.
  Any two of the three carry a full paper; all three plus a surviving bridge or
  dose-response result carry the strongest version.
- **Publishes (inverted, still a paper):** oracle result *fails* (F3) with the gap
  confirmed — an honest "review adjustment does not rescue merge signals; Wang et al.'s
  caveat holds empirically" is a publishable negative at the same venues, reframed
  around the layer-disagreement instrument.
- **Kills it:** F1 + F2 together — calibrated gaps < ~5% everywhere AND layers agree
  with strengthened suites (κ > 0.8): then green tests effectively are acceptance once
  suites are strengthened, UTBoost's rung is the top of the ladder, and the stance,
  the oracle, and the paper are dead; retire C3 and fold the pipeline into T5-family
  tooling.
