# loop_r1 — World-Model Explorations: Proof-Derived Supervision for Code LLMs

**Source material.** `hyp1/idea.md`, `hyp2/idea{,2,3,4}.md`, `hyp3/idea{1,2}.md`,
`hyp3/idea1_prompt.md` — eight deep-research briefs (literature cutoff 2026-08-21) that all
converge on **one** research program rather than eight ideas:

> Move code-model learning from *matching outputs* → *observing behavior* → *learning what
> behavior must remain true*. Token → State → Proof.

The briefs agree on the same three findings, and those findings are the constraints every
paper below inherits:

1. **"Use a formal verifier as an RL reward" is no longer novel.** Re:Form (TMLR 2026) does
   verifier-driven RL in Dafny from ~0.5B upward with an open pipeline; a 2026 MIT thesis does
   GRPO-style Dafny RLVR independently. Any paper whose contribution is "replace unit-test
   reward with a verifier" is dead on arrival.
2. **Execution supervision is not a straw man any more.** RLEF (multi-turn execution feedback)
   and especially ExecVerify (dense stepwise execution-state rewards) mean the honest contrast
   is not `tests vs proof` but the four-way ladder
   `execution-outcome → execution-process → proof-outcome → proof-process`.
3. **The A-class experiment is missing.** No surveyed work through 2026-08-21 holds base model,
   instances, sampling budget, optimizer and inference budget fixed while varying *the semantic
   source and granularity of the reward*, and then **removes the prover at evaluation time**.

## The four papers carved out of the program

| ID | Paper | Contribution type | Depends on |
|---|---|---|---|
| **ZW1** | *ProofWorld: Verification-Condition Transitions as Semantic Process Supervision* | method + causal comparison (flagship) | — |
| **ZW2** | *Verified but Wrong: Measuring and Closing the Specification-Adequacy Gap* | measurement + audit instrument | independent; cheapest; **gates every proof-reward claim** |
| **ZW3** | *Which Prover Teaches Software? Math Proof vs Program Verification* | transfer matrix | second-stage — run after ZW1 shows signal |
| **ZW4** | *The Oracle Economics of Code RL: A Cost-Normalized Phase Diagram* | instrumentation + economics | layered on ZW1/ZW2 runs |

The split is deliberate: ZW1 owns the *method* (VC transitions as training-time credit
assignment), ZW2 owns the *failure mode* (proof accepts what the spec permits, not what the user
meant), ZW3 owns the *branch question* (which prover teaches software semantics), ZW4 owns the
*cost claim* ("fewer rollouts" ≠ cheaper once solver tail is charged). None of them can be
folded into another without losing its primary endpoint.

Per-paper seeds — claim, arms, endpoints, novelty ledger, falsification, verification debt — are
in `papers/`.

## Seeding conventions learned in this batch

1. **Always pass `references`.** Wave 1 passed none. Consequences: ZW2's retrieval pulled a
   particle-physics paper and a physical-chemistry paper into its corpus, and ZW4's original room
   died in a retry loop because discovery returned **one** candidate against a ≥3 full-text gate.
   Every room seeded with the 22-citation payload had a clean corpus and cleared discovery.
2. **Pass references that have no arXiv ID too.** The schema accepts `{citation, url}` without
   `arxiv_id`. ZW1v4's sole remaining major exists because RLFR — non-archival, deleted from the live
   web, surviving as one Wayback capture — was the anchor for a **mandatory ablation arm** and was
   omitted from the payload for lack of an ID. The critic correctly objected that "none of the eight
   deeply compared works instantiates a scalar proof-ratio … reward," leaving that arm unanchored.
   A room cannot justify an arm it cannot see.
3. **Lead the seed with documented failures, not gap arguments.** ZW1 and ZW3's originals each burned
   **15 refiner rounds** on `motivation` and never cleared it; their evidence-loaded twins cleared the
   same step in **1–2 rounds**. Same critic, same models — the difference is whether the motivation
   cites observed failures with quotes or asserts that nobody has done the study.
4. **State the staging and the gate in the seed, and expect them to be deleted anyway.** ZW4's draft
   dropped "measurement-only instrumentation layered on companion runs" and committed to ~600
   training runs. Scope inflation remains the pipeline's most reliable failure mode, exactly as in the
   previous 18-package fleet.

## Systematic pipeline finding: `related_work` fails the same way every time

Three rooms, three unresolved majors, **all on `related_work` and all the same defect**. This is a
pipeline weakness, not a per-topic accident, and it should be pre-empted in the seed on future runs.

| Room | Critic's objection (quoted) |
|---|---|
| ZW2 | "reports paper and baseline counts without comparing how verifier-guided training, specification-quality evaluation, and static certification differ **relative to the delta objective**" |
| ZW3t | "All eight limitation descriptions are **near-identical restatements of the study's own research question**… problem-relative but undifferentiated and **borderline circular**" |
| ZW4t | "All eight works are marked `is_potential_baseline=false`… rejecting every work as a baseline without justification **leaves the study with no stated path from literature to experimental arms**" |

Two distinct bugs:

1. **Circular limitations.** The step writes each work's limitation as *"they did not do our study."*
   Eight entries, one sentence, restated. A limitation must be that work's **own** evidential gap,
   independent of our question — the ZW3t critic supplies the pattern: *"Re:Form evaluates only
   within-Dafny generalization without cross-domain software tasks, LORIS is inference-time-only with
   no training signal, DeepSeek-Prover-V1.5 never evaluates on any code task."*
2. **Blanket baseline rejection.** The step marks every retrieved work `is_potential_baseline=false`
   with no rationale, which is indefensible when Re:Form *is* the program-verification arm's recipe
   and ExecVerify *is* the execution-oracle arm.

**Seed-level mitigation for future runs:** state explicitly which retrieved works are expected to
supply experimental arms, and require that each related-work entry give a gap that would still be a
gap if our paper did not exist.

## AutoDiscussion runs (submitted 2026-08-21)

Six-step pipeline (`problem_statement → motivation → related_work → sub_problems →
method_design → experiment_design`), each step critic/refiner-looped. Models from
`.env.production` defaults: generate/refiner/thread = `codex:gpt-5.6-sol`, critic/review/judge =
`claude-code:claude-opus-5`. Completion gate is `all_steps_clean`, **not** `6/6 CLOSED`.

| Job | Room ID |
|---|---|
| ZW1 | `687d0e9e-c9ac-40e4-a384-a1d7e11791db` |
| ZW2 | `98e3ae6b-50e4-4a0c-8763-675d94a6ebcc` |
| ZW3 | `e6e06795-9b93-4a37-9905-8c6278293099` |
| ZW4 | `2a72d422-03b2-4a39-bf1a-8b65aa8b47af` |

Operating commands and the twin-room recovery rule (**a worker restart kills in-flight rooms
unrecoverably — resubmit as twins, don't wait**) are in
[`../../autodiscussion_runs_2026-08.md`](../../autodiscussion_runs_2026-08.md).

## Verification debt carried into every draft

Numbers quoted from the briefs are **relayed**, not primary-verified. These must be checked
against the source papers before they enter any submitted draft.

### ✅ VERIFIED 2026-08-21 — Re:Form and the MIT thesis

**Resolved citations (the briefs got the Re:Form title wrong — fix the bib entry):**

- Yan, Che, Huang, Xu, Li, Li, Qu, Shi, Lin, Yang, Yuan, Zhao, Qiao, Zhou, Fu.
  *"Re:Form — Reducing Human **Annotations** in Scalable Formal Software Verification with RL in
  LLMs: A Preliminary Study on Dafny."* arXiv:2507.16331 (v1 2025-07-22, v4 2026-07-03); **TMLR
  05/2026**. The briefs say "Reducing Human *Priors*" and drop the subtitle — both wrong.
- Max Tan. *"Automating Formal Verification with Reinforcement Learning and Recursive Inference."*
  M.Eng. thesis, MIT EECS, submitted 2026-05-22; arXiv:2605.30914 (2026-05-29). 140 pp.

| Claim | Verdict |
|---|---|
| Re:Form: RL reward from the Dafny verifier | CONFIRMED — but there is an SFT stage first, and the framing is *reduce*, not eliminate, human annotation |
| Re:Form: ~20,000 Dafny functions | CONFIRMED (MetaReflection 0.9k + BigCode 0.3k + Python2Dafny 16.3k) |
| Re:Form: 0.5B–14B, Qwen-2.5 | CONFIRMED (0.5B/1.5B/3B/7B/14B) |
| Re:Form: better OOD generalization after RL than SFT | CONFIRMED — 14B RL reaches 14.0% pass@1 OOD vs 8.3% SFT-only |
| Re:Form: cautions about specification hacking | CONFIRMED **in substance, not in terminology** — the paper never writes "specification hacking" or "reward hacking" |
| Tan: verified reward 2.2% → 58.1% | CONFIRMED (abstract) |
| Tan: post-filtering pass rate 9.7% → 31.1% | CONFIRMED (abstract) |
| Tan: specification hacking | CONFIRMED — the thesis *does* use the term explicitly |
| **Re:Form: "~176 / ~400 GPU-hours under a 40-epoch config"** | **PARTIALLY WRONG — do not cite as reported** |

**The compute anchor needs restating.** Re:Form never states a GPU-hours figure. Table 2 gives GPU
counts and wall-clock separately (0.5B: 16 GPUs × 11 h; 1.5B: 16 × 25 h; 3B: 32 × 20 h; 7B: 64 × 20 h;
14B: 64 × 36 h), for the **subset reward model** configuration, on A800-SXM4-80G. So 176 and 400 are
*our arithmetic*, not their numbers. Worse, the **40-epoch figure attaches only to the 3B run** —
asserting it for the 0.5B/1.5B rows is unsupported. Safe phrasing:

> Re:Form reports ~11 h on 16 A800-SXM4-80G GPUs for the 0.5B RL run and ~25 h on 16 GPUs for 1.5B
> (≈176 and ≈400 GPU-hours respectively, our arithmetic), under their subset-reward RL configuration.

**Quotable problem-side evidence** (Re:Form §3.3): *"We observe that the model exploits the reward
function by omitting unverifiable clauses and producing trivial specifications that are easy to
verify but semantically weak."* Attribute this as the *phenomenon*; "specification hacking" is Tan's
label and ours, not Re:Form's.

### ✅ VERIFIED 2026-08-21 — transfer evidence and execution baselines

**Resolved citations.** FVEL = Lin et al., *"FVEL: Interactive Formal Verification Environment with
LLMs via Theorem Proving"*, **NeurIPS 2024 D&B**, arXiv:2406.14408 · Self-play = Miceli Barone & Poon,
*"Improving LLM Code Reasoning via Semantic Equivalence Self-Play with Formal Verification"*,
arXiv:2604.17010 (**preprint, no venue**) · LORIS = Li et al., *"Guiding LLM-based Loop Invariant
Synthesis via Feedback on Local Reasoning Errors"*, **ACM TOPLAS 48(2) Art. 8, May 2026**,
arXiv:2605.17914 · AlphaVerus = Aggarwal, Parno, Welleck, arXiv:2412.06176 · Clover = Sun et al.,
**SAIV 2024**, arXiv:2310.17807 · Proof2Silicon = Jha, Wan, Chen, arXiv:2509.06239 (PREFACE is a
*separate earlier paper* by the same group, embedded as a component) · Clause2Inv = Cao et al.,
**PACMSE 2 (ISSTA 2025)** 1009–1030 · LaM4Inv = Wu et al., *"LLM Meets Bounded Model Checking"*,
**ASE 2024** 406–417 (the tool name is not in the title) · Loopy = Kamath et al., arXiv:2311.07948
(**preprint only**) · LEMUR = Wu, Barrett, Narodytska, **ICLR 2024**, arXiv:2310.04870 ·
ExecVerify = Tang et al., arXiv:2603.11226 (**preprint, no venue**) · RLEF = Gehring et al.,
**ICML 2025, PMLR 267:19034–19055**, arXiv:2410.02089 (cite the **6-author** PMLR list; arXiv v2 adds
a 7th) · StepCodeReasoner = Wang et al., arXiv:2605.11922 · ORPS → retitled at ICML: *"Reasoning
Through Execution: Unifying Process and Outcome Rewards for Code Generation"*, **ICML 2025, PMLR
267:72972–72994**, arXiv:2412.15118 · μCODE = Jain et al., **ICML 2025 Spotlight**, PMLR
267:26700–26716, arXiv:2502.20380 · CodeRL = Le et al., **NeurIPS 2022**, arXiv:2207.01780 (CodeT5
backbone — not a decoder-only LLM).

| Claim | Verdict |
|---|---|
| FVELER: 758 theories / 29,125 lemmas / 200,646 proof steps | CONFIRMED exactly |
| FVEL SV-COMP 69→81 and 75→84 | CONFIRMED — **but out of a 1,000-problem random subset** (6.9%→8.1%), floating-point excluded, while UAutomizer solves 374; authors credit seL4 corpus correlation; Code2Inv shows 46→46 |
| FVEL is SFT not RL | CONFIRMED (LoRA via LLaMA-Factory; no RL in the method) |
| Self-play ~28,000 validated Haskell functions | CONFIRMED |
| Self-play +13.3pp EquiBench | CONFIRMED — **OJ_V subset only** (56.5→69.8, DeepSeek-R1-Distill-Qwen-7B). Other categories regress: DCE −3.2, TVM −1.6. Cite as "on EquiBench's OJ_V subset" |
| Self-play PySecDB gain | CONFIRMED but small (F1 51.3→54.0) |
| Self-play: proofs not volume drive gains | **PARTIALLY** — the volume-controlled arm uses ≈150 pairs and the authors' own Limitations flag it; the next subsection says *"data volume remains critical"* |
| LORIS uses per-VC localized feedback | CONFIRMED |
| **LORIS is inference-time only** | **CONFIRMED with high confidence** — zero occurrences of "fine-tun" in the paper; closed-API models only. **Our novelty claim is safe** |
| AlphaVerus: no finetuning + spec filtering | CONFIRMED (*"without … model finetuning"*; filters *"to prevent reward hacking"*) |
| **Proof2Silicon: RL trains a prompt policy, target LLM frozen** | **CONFIRMED** (*"repairs the prompts provided to frozen LLMs … without costly fine-tuning"*; PPO trains the SLM) |
| ExecVerify: 7B competitive with 32B on execution reasoning | CONFIRMED — avg 60.8→80.8 vs Qwen2.5-Coder-32B-Instruct 77.9 (only *one* 32B comparator) |
| **ExecVerify: "+5.9 percentage points" pass@1** | **WRONG** — it is **5.9% relative** (avg 53.9→57.1, **+3.2 pp**) vs pure unit-test-GRPO on the same backbone |
| ExecVerify reward = next-statement + variable value/type | CONFIRMED **but incomplete** — Stage I mixes in a terminal I/O reward at α=0.5; Stage II uses unit-test pass fraction |
| RLEF: multi-turn, 8B+70B, order-of-magnitude fewer samples | CONFIRMED on **CodeContests** (3 samples vs 100 and vs 1,000, i.e. ≥30×) |
| CodeRL: actor–critic on unit-test feedback | CONFIRMED |

### ✅ VERIFIED 2026-08-21 — mathematical-prover branch

**Resolved citations.** AlphaProof = Hubert et al., *"Olympiad-level formal mathematical reasoning
with reinforcement learning"*, **Nature 651(8106), 607–613 (2026)**, DOI 10.1038/s41586-025-09833-y
(online 2025-11-12, print 2026-03-19) — **no arXiv version exists**, cite Nature only ·
DeepSeek-Prover-V1.5 = Xin et al., arXiv:2408.08152, **ICLR 2025** (OpenReview I4YAIwrsXa) ·
DeepSeek-Prover-V2 = Ren et al., arXiv:2504.21801 · Goedel-Prover-V2 = Lin et al., arXiv:2508.03613
(an ICLR 2026 poster page exists but the decision is **unverified** — cite arXiv) · hierarchical
lemma reward = Dong, Mahankali, Ma, arXiv:2411.01829 (the "ProD-RL" acronym is not in the v1
abstract — check the body before using it) · RLTPF = Leang, Hong, Li, Cohen, *"Theorem Prover as a
Judge for Synthetic Data Generation"*, **ACL 2025 Long 29941–29977**, arXiv:2502.13137.

| Claim | Verdict |
|---|---|
| AlphaProof: Lean states as RL states, tactics as actions (real MDP) | CONFIRMED |
| AlphaProof: ~80,000 TPU-days in the main RL phase | CONFIRMED verbatim — do **not** conflate with its per-problem *inference* TPU-hours |
| AlphaProof: ~80M formal problems from autoformalization | CONFIRMED (from ~1M natural-language problems) |
| **"AlphaProof scored 28/42"** | **MISATTRIBUTION** — 28/42 is the **combined AlphaProof + AlphaGeometry 2** system; AlphaProof solved P1/P2/P6, AlphaGeometry 2 solved P4 |
| DeepSeek-Prover-V1.5: 63.5% miniF2F / 25.3% ProofNet | CONFIRMED **but budget-dependent** — RL+RMaxTS at 32×6400 (204,800 generations, CoT/non-CoT mixture) and 4×6400. Budget-matched single-pass counterpart: **51.6% pass@128** |
| Hierarchical lemma reward improves OOD proving | CONFIRMED (AFP 40.8→45.5; OOD 36.5→39.5; novel lemmas = 37.7% of replay buffer) |
| RLTPF transfers to *informal* reasoning benchmarks | CONFIRMED (up to ~5–6 pts on individual benchmarks; per-model bests, not an average) |

### Still outstanding

- Scoop check on the four intended contributions (job running).

The briefs' own citation markers (`citeturn…`) are deep-research artifacts, not resolvable
references — every citation must be re-resolved to a real arXiv/venue ID during drafting.
