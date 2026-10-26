
# guidance.md — how to construct an abstract idea into an executable, verified paper

**Who this is for.** The executing agent (possibly a smaller model) that must
turn a topic bundle (`README.md` → `digest.md` → `paper.md`) into a paper
whose every claim is verified or honestly downgraded. `goal.md` says *what
runs when*; this file says *how to construct each artifact well*, across
different idea shapes, method categories, and failure situations. When
`goal.md` says "construct X per guidance.md §N", this file is authoritative.

**Prime directive.** You are statistically biased toward one template:
framing every idea as "two things are disconnected" and every method as
"integrate/unify them." This was measured across 11,683 papers and nine
LLMs (arXiv:2607.01233): bridge framings are 47–64% of LLM ideas vs 12.1%
of human ideas; synthesis methods 22–39% vs 5.1%; extended thinking makes
the collapse *worse*. Human ideas spread across measurement, explanation,
risk, scope, artifact, and optimization moves, and favor local surgical
operations — **replace** a brittle component, **decouple** two confounded
mechanisms, **formalize** a loose structure, **measure/bound** an assumed
quantity. Whenever a construction step below offers you a choice, and your
instinct says "combine A with B," treat that instinct as the null hypothesis
to argue against, not the answer.

---

## Part 1 — Classify the idea shape first

An abstract idea arrives in one of a few recurring shapes. Identify the
shape before doing anything, because each shape has a different "first
move." Misclassifying here produces a generic paper no matter how good the
later execution is.

| Shape | Signature in the seed | First move |
|---|---|---|
| **S1. Untested assumption** | "everyone assumes X but nobody has checked" (e.g. B6.3: pre-2022 corpora assumed clean human anchors) | Turn the assumption into a measurable quantity with an error bound; the paper's deliverable is the bound + validity envelope, not a new tool |
| **S2. Anomaly / observation** | "we noticed models do Y unexpectedly" | Reproduce it under controls first (is it real?), then mechanism-hunt (why?); resist jumping to a fix |
| **S3. Capability gap** | "no method can do Z" | Verify the gap against the reference cache before believing it (most "no method exists" claims are wrong); if real, this is a method paper — see Part 2 A1 |
| **S4. Transfer** | "technique from field F should work on problem P" (e.g. MBFL → agent trajectories) | The transfer itself is not the contribution; identify what *breaks* in the transfer (the non-trivial adaptation) — if nothing breaks, the paper is thin |
| **S5. Measurement need** | "the field reports X without knowing how reliable X is" | Instrument-construction paper — Part 2 A2 with heavy emphasis on R2 validation |
| **S6. Resource need** | "no benchmark/dataset isolates property Q" | Benchmark paper — Part 2 A3; the design argument (construct validity) is the paper, not the collection effort |
| **S7. Risk / failure mode** | "practice P silently causes harm H" | Demonstrate H exists (controlled), measure prevalence, bound conditions; a risk asserted without a measured instance is a position paper, not an empirical one |
| **S8. Efficiency** | "same quality at fraction of the cost" | Fix the quality bar first, publicly, then optimize; never let the quality metric drift during optimization |
| **S9. Negative result / refutation** | "claimed effect E doesn't replicate / doesn't hold under condition C" | Highest rigor bar of all: your power analysis must show you *could* have detected E; an underpowered non-detection is nothing |

If the seed matches none of these, or matches two, write down the ambiguity
explicitly in `digest.md` N1 and resolve it before N5 — an idea that is
"both a benchmark and a method" usually means neither is developed enough.

## Part 2 — Archetype-specific method construction

The archetype decides what counts as evidence, what the experiment section
must contain, and what reviewers kill. Classify early (it goes in
`paper.md` Step 2), and let it gate everything downstream. When unsure
between two archetypes, pick the one whose evidence you can actually
produce with the available compute — an under-evidenced method paper is
worse than a well-evidenced empirical paper on the same material.

**For every archetype: harvest 2–3 recent top-venue exemplars of the same
archetype into `reference_candidates.jsonl` (relevance: "background"),
digest them, and imitate their evidence *structure* (not their content).**
Do not rely on your memory of what such papers look like — memory of paper
structure is exactly where a smaller model confabulates. The one exemplar
already vetted in this pipeline is arXiv:2607.01233 for A2.

### A1. Method / technique paper
- **Contribution:** a new procedure that does something better/cheaper/
  newly-possible, on a task with existing baselines.
- **Evidence standard:** main comparison vs the *strongest* baselines from
  the cache (not convenient weak ones), plus an ablation per component —
  every M\* in the method must have a row showing what dies without it. A
  component with no ablation is decoration; delete it from the method.
- **Mandatory experiment shape:** main table (method vs baselines, ≥2
  datasets/settings), ablation table (one row per component), sensitivity
  analysis on the 1–2 hyperparameters the method introduces, cost/overhead
  reporting.
- **Hypothesis style:** superiority with an effect-size floor ("≥ X points
  over best baseline, p<α with correction, on ≥ k of n settings") — never
  bare "outperforms."
- **Fallback ladder:** loses to baselines overall → is there a *regime*
  where it wins (data scale, budget, distribution shift)? Then the paper
  narrows to that regime honestly. No regime → pivot to analysis: why the
  intuitive method fails is publishable if the diagnosis is mechanistic
  (S9 discipline applies).
- **Reviewer kills to pre-empt:** missing strong baseline (the cache's
  `method-twin`/`baseline` entries are the checklist); tuned-on-test;
  single-dataset claims; ablation-free components.

### A2. Empirical / measurement study
- **Contribution:** a measured quantity the field was assuming, plus the
  conditions under which it holds (a validity envelope). Exemplars:
  2607.01233; the B6.3 bundle.
- **Evidence standard:** validated instrument (R2 below) + controlled
  comparison (R3) + pre-registered trend/effect tests with effect-size
  floors (R4) + rival-explanation ablations (R5) + ≥1 mechanism analysis
  (R6).
- **Mandatory experiment shape:** the measurement grid (units × conditions),
  a placebo arm whose effect must be null, a rival-explanation arm, and a
  power statement per cell (under-powered cells pre-declared inconclusive).
- **Hypothesis style:** existence + magnitude + direction, all three
  binary-checkable ("slope β>0, p<α, odds ratio ≥ 1.05/year, for ≥2/3
  instruments").
- **Fallback ladder:** effect absent → the pre-committed flat-result
  wording is *itself* a finding if the field assumed otherwise (robustness
  certification — the F-G1 pivot pattern: the measured null becomes the
  license the field lacked). Effect present but rival explains it → the
  downgrade wording: phenomenon confirmed, mechanism reattributed.
- **Reviewer kills:** unvalidated LLM-judge; year/condition confounded with
  composition; "we manually verified" without protocol; claims generalized
  beyond the measured envelope.

### A3. Benchmark / dataset / resource
- **Contribution:** an instrument the community can reuse; the paper *is*
  the design argument.
- **Evidence standard:** construct validity (does the benchmark measure the
  named property and not a proxy? show discriminant cases), contamination
  analysis (train-set overlap, memorization probes), difficulty headroom
  (frontier systems must not saturate it at release), inter-annotator
  agreement for any labels (R2), and a baseline sweep demonstrating the
  benchmark *separates* systems that should differ.
- **Hypothesis style:** about the instrument, not about any system:
  "benchmark scores correlate ≥ρ with the gold property on the validation
  slice; frontier systems score ≤X% (headroom); label κ ≥ 0.7."
- **Fallback ladder:** frontier systems saturate it → tighten the hard
  slice or reposition as a diagnostic (which capabilities saturate first)
  rather than a leaderboard. Labels don't reach agreement → the property
  may be ill-defined; that discovery redirects to an A2 paper about the
  property's ambiguity.
- **Reviewer kills:** no contamination analysis; labels by a single
  unvalidated pass; benchmark distinguishable from the property it claims
  to measure; no maintenance/versioning statement.

### A4. Analysis / understanding
- **Contribution:** a mechanism explanation for a known phenomenon —
  *why*, not *that*.
- **Evidence standard:** at least two independent lines of evidence
  converging on the mechanism (e.g. behavioral + representational;
  intervention + correlation), and a **counterfactual test**: manipulate
  the proposed cause, observe the predicted change. Correlational-only
  mechanism claims are the archetype's classic failure.
- **Hypothesis style:** "intervening on M changes outcome O in direction D
  by ≥δ; ablating the alternative mechanism M' does not."
- **Fallback ladder:** intervention doesn't move O → the mechanism story is
  wrong; report the correlation honestly as descriptive and say the causal
  test failed. Both mechanisms move O → the paper becomes about their
  interaction/decomposition.
- **Reviewer kills:** mechanism inferred from attention maps / embeddings
  alone; no intervention; cherry-picked qualitative examples standing in
  for quantitative coverage.

### A5. Theory
- **Contribution:** a theorem/bound plus its relevance.
- **Evidence standard:** proofs checked line-by-line (state every
  assumption as a numbered condition), tightness discussion (is the bound
  vacuous in realistic regimes? compute it numerically for real parameter
  values), and a small empirical sanity check that the predicted behavior
  appears where the theory says it should.
- **Fallback ladder:** bound is vacuous in practice → either strengthen
  under added assumptions (state them, discuss their realism) or reframe
  as an impossibility/lower-bound result if that's what it actually shows.
- **Reviewer kills:** assumptions that exclude every real system;
  asymptotic claims sold as practical; theorem–experiment mismatch (theory
  about one quantity, experiments about another).

### A6. Tool / system
- **Contribution:** an artifact that works, with design decisions defended.
- **Evidence standard:** end-to-end evaluation on real tasks (not
  synthetic-only), comparison against existing tools' workflows,
  performance/robustness envelope, and — the part usually missing — a
  user-cost accounting (setup, latency, failure recovery).
- **Fallback ladder:** loses on benchmarks but wins on a workflow property
  (auditability, determinism, integration cost) → make THAT the claim and
  measure it directly.
- **Reviewer kills:** demo-grade evaluation; no failure-mode analysis; the
  system works only in the authors' environment.

### A7. Position / critique
- **Contribution:** an argument that changes what the field should do.
- **Evidence standard:** every empirical premise cited to a `selected`
  cache record; the strongest counter-position steel-manned and answered;
  at least one concrete, falsifiable recommendation (what experiment would
  settle the disagreement).
- **Reviewer kills:** attacking a straw man; premises from memory;
  recommendations no one could act on.

## Part 3 — Hypothesis, assumption, and fallback engineering

This is the machinery `paper.md` must contain, in full, before any
experiment runs. Templates below; the B6.3 bundle is the worked instance.

### 3.1 Hypothesis template (every H\* must fill every slot)

```
H<k> (binary): <quantified statement with direction and magnitude>
  applies_if:   [A1, A4, ...]        # assumptions it depends on
  metric:       <named metric, formula in Step 5>
  test:         <exact statistical test + correction>
  alpha:        <e.g. 0.05, Bonferroni over m tests → per-test 0.0167>
  effect_floor: <minimum magnitude that counts, in native units>
  aggregation:  <pre-registered vote rule, e.g. "≥2 of 3 instruments">
  fallback F<k>: <pre-committed VERBATIM sentence used if H<k> fails>
```

Rules:
- **Binary means binary**: a person with the results JSON and no context
  must be able to return PASS/FAIL. "Improves substantially" fails this.
- **Effect floor is mandatory**: significance without magnitude passes
  nothing (a slope can be significant and practically zero).
- **The fallback sentence is written NOW**, before results, at the same
  specificity as the main claim — because after results exist, every
  incentive pushes toward spin. If a hypothesis fails and its fallback is
  *itself* a publishable finding (the field assumed the opposite), say so
  in the fallback text (see A2's flat-result pattern).
- **Write the fallback-combination rules too**: "F1 combines with F2 into
  the global pivot F-G1 if H1(ii) also fails" — never invent combination
  logic at verdict time.

### 3.2 Assumption ledger template (every A\* must fill every slot)

```
A<j>: <the assumption, stated as a checkable proposition>
  failure_mode: <what the world looks like if it's false>
  detection:    <the concrete check that would reveal the failure>
  gate:         <PG-j if checked in the pilot; else the phase that checks it>
  consequence:  <what happens to which H* if it fails — degrade, restrict
                 scope, or block>
```

Worked instances from B6.3 to imitate: anchor-purity floor (A1: spot-check
1–2k docs, if impurity ≥1% report bounds as FPR±impurity AND require the
pre-LLM sub-range to agree); no-threshold-leakage (A4: enforced by pipeline
*order* — thresholds hashed before evaluation — a design-time detection,
the strongest kind); power (A6: named test, named power ≥0.9, named
minimum n per cell, and a pre-declared rule that thin cells are
INCONCLUSIVE, never null).

**Assumption verification is an activity, not a paragraph**: each A\* with
`gate: PG-*` runs inside the walking skeleton and its pass/fail is recorded
in `B_pilot/` before scale-up. An assumption that has no detection method
is not an assumption — it's a hope; either find a detection or restate the
claim so it doesn't depend on it.

### 3.3 The three-arm control structure (always present)

1. **B0 — placebo / "why do this at all".** Two jobs in one arm: (a) the
   current-practice arm whose asserted guarantee your study tests (if
   current practice is never violated, your premise collapses — that
   outcome must route to the global pivot, not be buried); (b) a
   null-by-construction placebo (shuffle labels/years/assignments) whose
   effect must be null. **Non-null placebo = the pipeline measures an
   artifact = the whole run is invalid.** Checked before any H\* is scored.
2. **B-alt — strongest rival explanation.** Name the 1–2 most plausible
   non-your-mechanism explanations for the expected result (composition
   drift, leakage, prompt wording, context compression...). Design a
   budget-matched arm that isolates each. Pre-commit the **downgrade
   wording**: what the claim becomes if the effect survives the rival vs
   dies ("the anchor's FPR is non-stationary either way, but the mechanism
   is composition change, not style change — Claims 1/3/4 hold, Claim 2
   falls"). Note the downgrade is per-claim, not per-paper.
3. **F-G\* — global archetype pivot.** If the central hypothesis *family*
   fails, the paper doesn't die — it changes archetype along a
   pre-committed line (measurement-of-erosion → robustness-certification;
   method-superiority → mechanistic-failure-analysis; benchmark-headroom →
   saturation-diagnostic). Write the pivoted abstract NOW. The pivot can
   flip which contribution (CO\*) is the headline.

### 3.4 Rigor recipes (apply to whichever archetype)

- **R1 Estimand first**: one sentence — quantity, unit of analysis,
  reference population, decision it feeds — before any component list.
  (2607.01233's estimand: distributional distance between LLM-idea and
  human-idea label distributions on a fixed taxonomy under shared
  literature context; unit = one idea per source paper.)
- **R2 Instrument validation sequence** (any taxonomy, rubric, LLM-judge,
  classifier, mutation set, detector): ① ground categories in cited
  external sources (2607.01233: NSF/NIH/AHRQ/DARPA program criteria) →
  ② draft wide, refine on a held-out calibration set with *named*
  merge/split/remove operations (11+9 elements → 7+7 on 150 held-out
  papers) → ③ validate the automated annotator against ≥2 independent
  human raters on the held-out set, κ ≥ 0.7 required (theirs: 0.84/0.81/
  0.93) → ④ inspect the confusion structure — disagreements must be
  adjacent categories, not systematic collapse → ⑤ freeze (hash) before
  scale. Asserted validation numbers without the protocol are treated as
  absent.
- **R3 Confound-removal one-liners**: for every design constraint write
  "constraint X removes confound Y" (2607.01233: shared reconstructed
  literature context removes topic-choice and knowledge-access confounds).
  Unnamed-Y constraints are decoration; obvious-Y without an X means the
  design is broken.
- **R4 Metrics**: standard bounded measures with formulas (they used TVD +
  JSD + normalized entropy — a distance *and* a concentration measure,
  which answer different questions); one plain-language magnitude gloss
  per headline number ("TVD 0.348 ⇒ over a third of the mass would have
  to move").
- **R5 Rival→ablation pairing**: each named rival gets one budget-matched
  ablation with the interpretation pre-committed. Their three: full-paper
  context (rival: compression artifact — gap didn't shrink), neutral
  prompt wording (rival: prompt-induced — pattern survived), thinking
  mode (rival: reasoning fixes it — it got *worse*, and they published
  that).
- **R6 Mechanism layer**: after the headline, ≥1 analysis explaining *why*:
  archetype clustering with per-family log-odds (integrate: 34.2% of model
  operations vs 2.35% human, log-odds 3.07; replace: 0.9% vs 9.1%),
  embedding geometry (two different model families closer to each other,
  cos 0.83, than either to the human idea for the same paper — a shared
  template, not random narrowness), or enrichment ranking with minimum
  support.
- **R7 Reporting**: exact parameters + seeds; an explicit no-hyperparameter-
  search statement (or the search protocol); human-audit protocol with n
  and rater count; prompts verbatim in an appendix; a Limitations section
  that **bounds the setting of the claim** ("evidence about current LLM
  ideation under a controlled literature-grounded setting" — names the
  envelope) rather than generic caveats; refuting results reported at full
  prominence.
- **R8 Honest scale**: matched-set construction rule stated (rows dropped
  when any source lacks valid output; final n reported with per-domain
  split); per-cell counts in every table; validation subset disjoint from
  evaluation; headline n never includes dropped rows.

## Part 4 — Situation handbook (when things go sideways)

Diverse inputs produce diverse failures. Each situation below has one
correct move; do not improvise alternatives.

| # | Situation | The move |
|---|---|---|
| 1 | **Placebo arm non-null** | The run is invalid — an artifact is being measured. Do NOT score any hypothesis "to see." Diagnose the pipeline (ordering leak? threshold leak? composition artifact?), fix, re-run from the walking skeleton. |
| 2 | **Central hypothesis fails, cleanly** | Use the pre-committed F\*/F-G\* wording verbatim. If the field assumed the effect existed, the null IS the finding (robustness certification) — but only at the measured envelope, with the power statement making the null credible. Never quietly reframe as if the null was the goal all along without the pivot machinery. |
| 3 | **Effect exists but B-alt kills the mechanism** | Apply the downgrade wording: the phenomenon stands, the causal story changes. Check the claim map for which claims survive — usually the practical recommendation survives even when the mechanism claim falls. |
| 4 | **Effect in the WRONG direction** | Stronger than a null — report it at full prominence (2607.01233's thinking-mode result is the template). Re-derive what the direction implies; often it upgrades the paper's interest. Never bury it in an appendix. |
| 5 | **Under-powered cells** | Pre-declared INCONCLUSIVE, never null, never dropped silently. If the *central* test is under-powered, the honest options are: collect more (if config-only), narrow the claim to powered cells, or stop. |
| 6 | **Method-twin discovered mid-run** (freshness sweep or reviewer) | Concede-and-differentiate, at source: what machinery is genuinely shared (concede it explicitly — trying to hide a shared estimator is the detectable sin), and what remains yours (new response variable, finer granularity, different estimand, new regime). This is a `paper.md` repositioning + Phase A re-check, never a silent related-work paragraph. |
| 7 | **Instrument fails κ validation** | Do not scale it. Options in order: refine categories on the held-out set (named merge/split ops) and re-validate; simplify the construct (fewer, coarser labels often agree); or accept that the property is ill-defined — which may itself redirect the paper (A3→A2 pattern). |
| 8 | **Walking skeleton needs a code change to scale** | The skeleton failed even if pilot numbers looked fine. Fix, re-run the skeleton, only then scale. Config-not-code is the gate. |
| 9 | **Two arms give contradictory results** | Check assumption ledger first (which A\* differs between arms?); usually one arm violates an assumption the other satisfies. If genuinely contradictory under shared assumptions, the paper's claim narrows to the conditions of agreement and the contradiction is reported as a finding. |
| 10 | **Compute budget insufficient for the pre-registered grid** | Shrink along pre-declared axes only (fewer conditions, not smaller n per cell — n protects power); record the shrink in `pipeline.md`; re-check which H\* remain adequately powered and pre-declare the rest INCONCLUSIVE before running. |
| 11 | **Results are too good** (e.g. Top-1 = 1.00) | Treat as a bug signal before a celebration: check for leakage (A4-type), label contamination, degenerate task difficulty. If it survives, add a hardness analysis showing the ceiling isn't an artifact (harder slice, adversarial cases) — reviewers apply exactly this skepticism. |
| 12 | **Idea pre-empted entirely** (exact study exists) | Stop the paper; do not "differentiate" cosmetically. Salvage: replication-with-extension (new regime/population), or the residual gap the existing paper names in its own limitations (its digest's N10 is the mine). |
| 13 | **Claims drifted above evidence during writing** | The `claim_map.md` grep (goal.md's stale-claim gate) exists for this; fix the sentence to the licensed wording, don't fix the map to the sentence. |
| 14 | **Reviewer persona demands an experiment you can't run** | Distinguish: (a) evidence the claim NEEDS → narrow the claim; (b) robustness nice-to-have → add to limitations with a named concrete protocol someone could run; (c) misunderstanding → fix the writing that caused it. Never promise "future work" for category (a). |
| 15 | **The abstract idea is really two papers** | Split at the estimand: if two deliverables need different instruments or different evidence standards (a bound AND a new method), pick the one the compute supports and demote the other to one paragraph of future work. Two half-evidenced contributions reject as one. |

## Part 5 — Using references to construct, not just to cite

- **Structural exemplars**: per archetype, digest 2–3 recent top-venue
  papers of the same archetype (`relevance: background`) and imitate the
  *shape* of their evidence — table structure, ablation granularity,
  threat taxonomy. Never imitate content, never cite from memory.
- **The method-twin as a design input**: the closest prior work's digest
  (N6 components, N10 limitations) tells you which components you can
  inherit (concede) and where the genuine gap is (its own stated
  limitations are the most defensible motivation you can have — the prior
  authors conceded them for you).
- **Baseline selection is a cache query**: baselines = the `selected`
  entries tagged `baseline`, strongest first; a baseline you can't run gets
  a stated reason in the paper, not silence.
- **When the cache is thin** (fewer than ~5 selected entries): the harvest
  was inadequate, not the field empty. Re-harvest from new angles (method
  names, metric names, dataset names, the assumption's name) before
  claiming novelty.

## Part 6 — Quality bar self-check (run before handing to Phase A)

1. Estimand in one sentence? (R1)
2. Verb check passed — no undefended integrate/unify framing? (Prime
   directive; deletion test on the asymmetry sentence)
3. Every H\* has all seven template slots including a verbatim fallback?
4. Every A\* has a detection method and a gate?
5. B0 + B-alt + F-G\* all present with pre-committed wording?
6. Every instrument has the 5-step R2 plan with an acceptance threshold?
7. Every design constraint names its confound? (R3)
8. ≥1 mechanism analysis budgeted? (R6)
9. Power stated per cell; thin cells pre-declared INCONCLUSIVE?
10. Archetype named, and the evidence standard in Part 2 for that
    archetype is met by the experiment plan — not by intention?

Any "no" → fix before Phase A, citing the section number here.
