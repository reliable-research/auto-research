# Pengsida Stage Review — B4.6

> Skill: `pengsida-stage-reviewer`. Applied **after** `research-taste-auditor` (🟢) and **before** final `paper_draft.md` was locked, per the pipeline order in `discussion_trace.md`. Stages 1–4 below are checked against the confirmed stage outputs in `discussion_trace.md` (mapping: discussion Stages 1+2 → reviewer Stage 1; discussion Stage 3 → reviewer Stage 2; discussion Stage 5 → reviewer Stage 3; discussion Stage 6 → reviewer Stage 4). The Stage 5 Writing review runs against the first assembled `paper_draft.md` and is appended at the end. Three REVISE findings fired against the confirmed outputs and were applied before/into assembly (see "Fixes applied"); the draft you now see already reflects them. Date: 2026-08-15.

## Archetype classification

**Analysis / Finding** (secondary: resource — the annotated-ledger traces and replay harness are natural release artifacts, but the paper's value does not rest on the artifact). Per `archetypes.md`'s tells: the core question is "how large is a phenomenon and what structure does it have" — verification-induced cost share, cache damage, frontier shape, avoidable headroom — with no pipeline pitted against baselines to win; the ledger, cache simulator, value profiler, and two-tier evaluation are the *analytical apparatus* that makes the phenomenon observable. This matches Stage 1's explicit `study_type: empirical` and the seed's [证据] label. Stage 3 ("Method") and Stage 4 ("Experiments") below therefore use the **Analysis/Finding** column: apparatus licensing, and falsification rather than ablation.

---

## Stage 1 — Problem + Motivation

**STAGE 1 VERDICT: PASS**

**Why, quoting the draft:** The problem clears the "so what" test before any apparatus appears — "today's serving stacks price generation while treating verification as opaque tool time" is a root-asymmetry framing (the cost model mislabels a first-order driver), not a patch, and the stakes are two-sided and concrete: "if the verification-induced share … is substantial, the field's serving optimizations are tuned against a workload model that mislabels a first-order cost driver; if it is small, the seed's premise fails and *that* bound is the finding." The refusal to pre-commit to the flattering outcome is exactly what makes the motivation credible. The minimum-viability check (stage-1 checklist item 6) is also satisfiable in a day: run the conservative-only ledger on a few hundred TraceLab sessions and ask the binary question "is the conservative dollar share ≥ 0.05?" — a cheap kill-test for the whole premise, and Phase B's walking skeleton is exactly this. Importance is current, not abandoned: the occupancy sweep documents four papers entering the adjacent speculation/verification-overlap space since 2026-06, which is a live field with a genuinely unclaimed slice, and the risk clock (1–2 quarters) is stated rather than hidden.

**Note for Stage 2:** passing here obliges Related Work to establish that the two existing characterizations (TraceLab; Copilot-scale) really do lack the verification dimension — checked next, and it is where the one soft spot lives.

---

## Stage 2 — Related Work

**STAGE 2 VERDICT: REVISE** *(fired, fixed — see "Fixes applied")*

**Why, quoting the draft:** Nearest-neighbor honesty is exemplary — the confirmed output names Cost-Aware Speculative Execution (arXiv:2606.07846) as "**the nearest neighbor, per the seed card itself**, and treated as such rather than buried," concedes the shared dollar-denominated objective, and states the three-part delta (trace-grounding, verify-as-decision-object, cache modeling) verbatim from the seed's novelty ledger. The threads a subfield reviewer expects (characterization, agent-aware caching, speculation, queueing, serving canon, test-time verification) are all present. But the load-bearing limitation of the *closest thread* rests on evidence the review itself admits is second-hand: `lim_tracelab_no_verification_semantics` is evidenced by "the 2026-08-13 occupancy sweep's finding that both existing characterizations lack the verification dimension (泛特征无验证维度)" — a corpus-scan assertion, tagged `[scan]`, about a paper whose full text was never read in this environment. Per the Stage-2 bar, "if a reviewer could reply 'but paper X already does this,' the section fails" — and nothing in the current record would let the authors answer that reply about TraceLab's own paper with first-hand evidence. The gap is probably real (two independent scan entries agree), but *probably* is not the standard for the limitation the entire novelty position leans on.

**THE ONE FIX (applied):** make first-hand confirmation a blocking gate, not an assumption: Phase B's bundle-validation gate (A1 in the experiment spec) now requires reading the TraceLab paper against its released artifact and confirming it reports no verification-attributed cost share, no retry attribution, and no cache-interaction analysis — with the pre-committed consequence that if any of the three exists, the paper repositions per guidance.md situation 6 (concede-and-differentiate at source, Phase A re-check) *before* any measurement is trusted. The paper draft's Related Work also carries the nearest-neighbor delta sentence in prose, not only in the structured output.

**Secondary fix (applied):** the draft prose must preserve the engagement-tier honesty of the confirmed output (which papers were verified via the arXiv API vs known from scan records) in its Threats to Validity, rather than flattening all citations to equal confidence.

---

## Stage 3 — "Method" (Analysis/Finding variant: the analytical apparatus)

**STAGE 3 VERDICT: REVISE** *(fired, fixed — see "Fixes applied")*

**Why, quoting the draft:** Most inferential steps are licensed exactly where they need to be. The attribution interval is justified by a bias-direction argument ("an attribution scheme whose bias direction is *known by construction* on each side"), the cache counterfactual by a determinism argument ("cache behavior is a deterministic function of the token sequence given a policy — re-rendering is a valid intervention on the cache even though it would be an invalid intervention on the agent"), and the value profiler was already forced by the discussion loop's own critic to carry a positivity gate with a pre-committed INCONCLUSIVE downgrade. No orphan components: each of the four instruments traces to a named sub-problem. But the apparatus's single most quoted claim — Tier-A reschedules are evaluated by exact replay because "outcomes are identical by construction" — is licensed only *within the replay*. As a claim about deployable headroom it silently assumes the agent's behavior is insensitive to the wall-clock consequences of rescheduling: an agent scaffold with step timeouts, retry-on-slow logic, or wall-clock-dependent prompt content could behave differently under a schedule that batches or defers verification execution, even though the token sequence it *would have seen* is byte-identical. The invariance predicate as confirmed ("agent-visible sequence preserved") does not name this channel, so the one hinge the headroom claim hangs on is stated one condition short of true.

**THE ONE FIX (applied):** the invariance predicate is scoped explicitly: Tier-A exactness holds for the recorded sessions under the stated cost model, and its deployment reading additionally assumes no wall-clock-dependent agent behavior (timeouts, latency-conditioned prompts) — checked descriptively by reporting the incidence of timeout/latency-conditioned constructs in the trace corpus, and stated as a scope condition on the Tier-A headroom claim in the Methodology and Threats sections of the draft.

---

## Stage 4 — "Experiments" (Analysis/Finding variant: falsification, not correlation)

**STAGE 4 VERDICT: REVISE** *(fired, fixed — see "Fixes applied")*

**Why, quoting the draft:** The falsification discipline is genuinely present, not implied: every hypothesis carries an explicit falsification direction with a floor ("falsified if even the liberal bound falls below 0.10"; "falsified if the ratio is at most 1.1 under either policy"; "falsified (degenerate frontier) if cost and stratified value are proportional within a factor of 1.5"), the placebo is checked before any hypothesis is scored ("non-null placebo invalidates the attribution pipeline before any hypothesis is scored"), and the strongest alternative for each finding has a named control (volume-matched filler for the cache claim; shuffled-step-type relabeling for the attribution claim; the positivity gate for the frontier's scheduling-habit confound; the oracle/frozen predictor pair for the speculation claim). The discussion loop's own Stage-6 critic already caught the two classic kills (an undecidable non-inferiority margin; a beats-baseline phrasing in an empirical study) and the fixes are in the confirmed output. What remains is a promised-denomination gap: Stage 1's output contract says the decomposition covers "tokens, latency, dollars," and the motivation argues latency matters to operators — but every hypothesis and every RQ metric in the confirmed Stage 6 output is dollar-denominated; latency has no reporting slot anywhere in the plan. An estimand promised in the problem definition with no cell in the experiment plan is exactly the "uncovered claim" this stage exists to catch — small, but real.

**THE ONE FIX (applied):** `rq_cost_share`'s metrics now include the latency-denominated share (verification-execution wall-time plus attributable retry-generation time, over session wall-time) reported descriptively alongside the dollar interval, and the headline hypothesis verdicts are explicitly scoped to the dollar denomination (the only one with a pre-registered floor). No new hypothesis is added — latency is reported, not tested, and the scope note says so.

---

## Fixes applied (Stages 2–4)

1. **Stage 2 fix** — Phase-B gate A1 upgraded from "re-verify TraceLab corpus facts" to "read the TraceLab paper first-hand and confirm the absence of verification-attributed analysis, with pre-committed repositioning (guidance.md situation 6) if the confirmation fails"; nearest-neighbor delta sentence carried into draft prose; engagement-tier honesty carried into Threats. *Files:* `experiment_design.md` (gate A1), `paper_draft.md` (Related Work opening; Threats).
2. **Stage 3 fix** — Tier-A invariance predicate scoped with the wall-clock/no-latency-dependence condition, plus a descriptive incidence check in the corpus; stated wherever the exactness claim appears. *Files:* `experiment_design.md` (Tier-A protocol), `paper_draft.md` (Methodology: Two-Tier Headroom Evaluation; Threats).
3. **Stage 4 fix** — latency-share added to `rq_cost_share` metrics as a descriptive readout; headline verdicts scoped to dollars. *Files:* `experiment_design.md` (RQ1), `paper_draft.md` (Experiments RQ1; Metrics).

The confirmed outputs in `discussion_trace.md` are preserved as the historical record; the fixes are folded forward into the assembly artifacts, which is where they bind.

---

## Stage 5 — Writing (Introduction / Abstract / Conclusion), against the first assembled `paper_draft.md`

**STAGE 5 VERDICT: REVISE → fixed** *(two findings; both applied to `paper_draft.md` and mirrored into `paper_draft.tex` before compilation)*

**Why, quoting the first-assembly draft:** The reverse-outline test *almost* passes: the Introduction's paragraph-leading sentences walk problem → gap → prior work → difficulties → design → evaluation without needing sentence 2 of any paragraph. Two genuine breaks:

1. **Abstract asserted an accomplished fact.** The first-assembly abstract read "We find that verification is a first-class cost object: its induced share …" — accomplished-fact phrasing for a study whose every Result slot is an explicit placeholder. This is the same defect B5.5's Phase-G review caught, and it had crept back in here at assembly time. **Fix (applied):** rephrased to the pre-registered form — "We pre-register interval estimates … and test whether verification clears a first-class-cost bar (conservative share ≥ 0.15)" — so the abstract asserts the design and its falsification bars, never an unmeasured outcome.
2. **The contribution sentence was split across two bullets.** The quotable one-sentence contribution ("verification steps are priced by serving stacks as opaque tool time, yet they are the workload's most cost-heterogeneous, most cache-hostile, and most reschedulable step class — and both halves of that claim are measurable from public traces") existed only implicitly, smeared across the first and third contribution bullets. Per the Stage-5 bar ("one quotable sentence must carry it — for a finding paper the characterization *is* the contribution"), the Introduction's design paragraph now leads with that sentence verbatim, and the abstract's gap move uses its first half.

Checked and passing without a finding: falsification-condition lines present in all seven RQ subsections (the B5.5 Stage-4 lesson was applied at assembly time, not retro-fixed); Conclusion names a real forward-looking limitation (the value profiler's ordering claim is the apparatus's weakest identification, pointing at instrumented-scaffold experiments as the next step) rather than recapping the abstract; no internal stage IDs (`sp_*`, `m_*`, `rq_*`, H-numbers) leak into prose — verified by direct grep over the draft.
