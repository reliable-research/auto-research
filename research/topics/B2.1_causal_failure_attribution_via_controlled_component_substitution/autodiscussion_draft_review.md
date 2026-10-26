# B2.1 — Autodiscussion Draft Review (Stage 1)

**Reviewed package:** `/data/wangjian/wj_code/paper_autodiscussion/completed_jobs_dirs/ZB2.1 Causal Failure Attribution via Controlled Component Substitution--3ff5f44c/` (research-report.md, experiment-spec.md, paper-draft.md)
**Reviewed against:** `TOPIC_DIR/discussion.md` (design doc), `TOPIC_DIR/README.md` (seed)
**Date:** 2026-08-15. Room closed with 1 unresolved MAJOR, 5/6 clean passes.

---

## 1. Architecture (what the draft actually builds)

The draft proposes **"Mechanically Certified Fault Capsules"**: (a) **Proof-Carrying Fault Capsules (PFC)** — typed fault transformations (trigger predicate + deterministic transform + lineage tag) certified by a three-arm deterministic replay (clean pass / capsule-on fail with tag-to-oracle certificate / capsule-bypassed pass), 3×3 runs from identical checkpoints; (b) **Crossover Evidence Pack diagnosis** — episodes as checkpointable typed state machines; clean/faulty "component twins" swapped in both directions (fault transfer, clean repair) under five outcome-blind admissibility checks (shared keys, invariants, capability sandbox, non-target hash fixity, self-transplant hash reproduction); a blinded diagnoser picks the earliest boundary with bidirectional crossover, else abstains; (c) **backbone × replay panel** — 5 frozen backbone families × nested budgets {0,2,4,8,16} × 3 seeds × 10 decoding replicates, intention-to-diagnose scoring (abstain = error), Fleiss' κ. Six RQs: certificate reproducibility, nuisance robustness, localization uniqueness, attribution accuracy vs repair-only, budget saturation at 8, cross-backbone stability. The experiment-spec is a clean, buildable harness plan (`pcfc/` package, config-switch ablations, JSONL + content-addressed checkpoints).

## 2. Novelty ledger

| Claim | Nearest prior | Delta | Stance |
|---|---|---|---|
| Mechanically certified causal labels via toggled injection + but-for replay certificate | **Who&When Pro** (Liu et al., arXiv 2607.09996): 12,326 injected-failure trajectories with "golden labels" — *the partial scoop discussion.md predicted* | They assume injected = decisive; no bypass arm, no lineage certificate, no no-op control, no validity measurement (RQ1-style). Delta = certification-as-instrument, real but *must be stated against this paper explicitly* | **DEFENSIBLE, PERISHABLE** — the draft cites it but buries it in a list; the revised draft must make it the headline boundary |
| Injection as benchmark ground truth for attribution | **AgenTracer** (2509.03312) injection as RL training supervision; **AgentDebug** (2509.25370) counterfactual earliest-error test | Controls + released certified corpus + scoring *all* methods vs training one method | DEFENSIBLE (matches discussion.md Stage-2 refinement) |
| Outcome-blind state-closed bidirectional substitution (transfer + repair) | **DoVer** (2512.06749) repair-only hypothesis verification; **CAR** (Shah 2026) step-level do() on synthetic SCMs | Bidirectionality + admissibility-before-outcome + abstention is genuinely new protocol machinery | NOVEL but heavy; its cost must be justified against the simpler flip/no-op/identity lattice in discussion.md |
| Cross-backbone diagnosis stability (absorbed B2.3) | No prior artifact reports it | Present as RQ6, but **label-survival rate — the actual B2.3 question — is missing** | PARTIAL |
| Replay-budget scaling (absorbed B2.2) | CAR admits replay cost; no benchmark reports accuracy-per-replay | Present as RQ5 with nested budgets; k-sensitivity check from discussion.md dropped | PRESENT |
| Validity measurement of the field's substitution premise (discussion.md RQ1: flip-rate vs class-matched no-op) | Nobody | **DROPPED from the draft** — replaced by certificate-pass-rate, which measures yield, not premise validity | REGRESSION vs discussion.md |

## 3. Consistency vs discussion.md

**Absorbed axes:** B2.3 cross-backbone → **present** (RQ5/RQ6, five backbones) but semantically shifted: discussion.md's SP4 measures *label survival* ("does δ_c still flip on backbone B?" — non-transfer is the expected case) plus diagnosis stability; the draft measures only diagnosis stability of its own diagnoser and silently assumes the certified cohort transfers across backbones. B2.2 replay budget → **present** (RQ5, budgets {0,2,4,8,16}); the k-sensitivity check (k ∈ {2,4,8} on 50 trials) is dropped.

**Silent scope changes (the sibling failure signature, confirmed):**
1. **Executor became an injectable fault class.** discussion.md/README fix the executor and define K = {plan, tool, obs}; the draft's own formal definition agrees (`κ(z_i) ∈ {plan, tool, observation}`) — yet RQ1 preregisters 40 *executor* templates, macro-F1 is four-class, and executor twins are built. Internal contradiction, unflagged.
2. **The benchmark became a method paper.** discussion.md's CO3 scores an attribution-method zoo (LLM-judge ×3 strategies, frozen surface heuristic B0-b, ablation, DoVer-style, mutation-kill sibling, random/majority) against the certified corpus; the Who&When natural-failure contrast and the step-level secondary track (comparable to the 14.2% literature number) are mandatory. The draft evaluates only its own crossover diagnoser vs its own ablations (repair-only, trace-only, zero-replay). The Defects4J identity — instrument that outlives methods — is gone; Defects4J itself is never cited.
3. **The control lattice was replaced by absolute determinism.** discussion.md certifies via majority-over-k replays + class-matched no-op δ_∅^c (FlipRate ≤ 0.10) + identity tier δ_id (≤ 0.05) — "where the benchmark lives or dies" (SP2). The draft instead assumes fully deterministic execution (3/3 exact runs, hash-exact self-transplants) and drops the no-op arm entirely (nuisance variants test something else: trigger invariance).
4. **Pilot gates, scoop-check decision rule, descope ladder, powered-cell rule all absent.** Draft's certified cohort (≥24/class) violates discussion.md's own ≥80-per-cell powered-cell rule.
5. **Scale silently reshaped**: 160 templates / N=96–160 episodes vs discussion.md's ~300 certified Stage 1 → 1,500+ Stage 2; but panel cost exploded the other way (episodes × 5 backbones × 5 budgets × 3 seeds × 10 replicates ≈ 10⁵ cells).

## 4. Citation audit (~10 load-bearing; verified via arXiv API, WebSearch not used — narrower sweep)

| Citation in draft | Verdict |
|---|---|
| Who&When, Shaokun Zhang et al. | **REAL** — arXiv 2505.00212 |
| Who&When Pro, Jiale Liu et al. | **REAL** — arXiv 2607.09996 (Jul 2026) — nearest neighbor, under-positioned |
| AgenTracer, Guibin Zhang et al. | **REAL** — arXiv 2509.03312 |
| RAFFLES, Chenyang Zhu et al. | **REAL** — arXiv 2509.06822 |
| DoVer, Ming Ma et al. | **REAL** — arXiv 2512.06749 |
| MAST, Cemri et al. | **REAL** — arXiv 2503.13657 |
| GAIA, Mialon et al. | **REAL** — arXiv 2311.12983 |
| ReAct / Toolformer / Reflexion / Plan-and-Act | **REAL** — 2210.03629 / 2302.04761 / 2303.11366 / 2503.09572 |
| AgentDebug ("Where LLM Agents Fail…", Kunlun Zhu) | **REAL** (2509.25370) — *known 2026-adjacent, NOT cited by draft* |
| TRAIL, Deshpande et al. | **REAL** (2505.08638) — *named in discussion.md, NOT cited by draft* |
| CAR (Shah), DRIFT, StepFinder, MP-Bench, "Whole Elephant", Guoqing Ma | Report-grounded (room fetched PDFs); not independently re-verified |
| Defects4J (Just et al., ISSTA 2014) | Real, framing ancestor — **absent from draft** |

Zero confabulated citations (sibling signature holds). Misses: TRAIL, AgentDebug, FAMAS, Defects4J. Related Work still contains the placeholder "> This section requires manual completion".

## 5. Gap to implementation (FSE Oct-2 realism)

- **Determinism assumption is not purchasable**: bit-exact 3/3 replays and hash-exact self-transplants across *five frozen API backbone families* is not something current LLM serving guarantees; discussion.md's stochasticity-tolerant gates (majority-of-k, FlipRate bounds) exist precisely for this. As specced, most arms would be marked "unavailable" and the paper would report mostly abstention.
- **Panel size**: ~130 episodes × 5 backbones × 5 budgets × 3 seeds × 10 replicates, each cell up to 16 replays → orders of magnitude beyond discussion.md's $2k–6k budget and the 7-week runway. 10 replicates × 3 seeds is also redundant.
- **Engineering surface**: capability sandbox + content-addressed checkpointing + typed twins over a real agent framework is a quarter of infrastructure; discussion.md's orchestrator-message-level edits (DoVer-style) reach the same interventions with a week of harness work. No walking-skeleton gate to bound the downside.
- What *is* realistic and good: config-switch ablations, JSONL artifacts, abstention-as-error scoring, preregistration file, MockPipeline smoke test.

## 6. Verdict and top-3 fixes

**Verdict: MAJOR REVISION — strong protocol core, wrong paper identity, one internal contradiction, infeasible as specced.** The PFC certificate and outcome-blind substitution machinery are genuinely sharper than anything in the 2026 neighbor set, but the draft silently pivoted from "Defects4J-for-agents benchmark that scores the field" to "our diagnoser and its ablations," dropped the control lattice that makes the labels defensible, and contradicts itself on the executor class.

**Inferred unresolved MAJOR:** the executor-class contradiction — the formal problem definition admits injected faults only in {plan, tool, observation} (consistent with discussion.md's fixed-executor premise), while the entire experimental design is four-class with 40 executor fault templates and executor twins. Both texts shipped unreconciled; this is the kind of definitional inconsistency a quality gate flags and cannot fix editorially.

**Fix 1 (contradiction + B2.3 restored):** Freeze the taxonomy at three injectable classes {plan, tool, observation}; the executor is the held-fixed substrate. Executor variation returns where it belongs: the cross-backbone axis swaps the executor backbone and reports **label survival rate** as a first-class result alongside diagnosis stability.
**Fix 2 (identity restored):** Reinstate the benchmark framing — certified corpus (CO1) + certification protocol (CO2) headline; method-zoo evaluation (CO3: LLM-judge ×3, B0-b surface-heuristic floor, DoVer-style do-then-verify, random floor, plus the bidirectional crossover diagnoser as the interventional reference) with the Who&When natural-failure contrast and the step-level secondary track; cite Defects4J, TRAIL, AgentDebug, and position sharply against Who&When Pro.
**Fix 3 (feasibility restored):** Replace absolute determinism with the k-replay majority + class-matched no-op + identity-replay control lattice (keep the bypass arm and lineage tag from the draft as additions, not replacements); shrink the panel to 3 backbones (primary + strong API + pinned open-weights) × budgets {0,2,4,8,16} × 3 seeds; reinstate the walking-skeleton go/no-go, powered-cell rule, and descope ladder with the Oct-2 milestone plan.
