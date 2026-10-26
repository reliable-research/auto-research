# ZW3 — Which Prover Teaches Software? Mathematical Proof versus Program Verification as Post-Training Supervision

> ## 📌 SUBMITTED-INPUT ARTIFACT — largely faithful
>
> This is the `idea_text` sent to the AutoDiscussion room, preserved verbatim for provenance.
> Of the four seeds it is the **closest to the delivered design**. Two supersessions, marked inline:
> the budget-matching rule (four reported normalizations → one common feasible intersection) and the
> arm set (the delivered study adds a matched non-formal SFT control `N`, and two curriculum
> controls this seed does not name). Everything else, including the whole verified evidence state
> and the attribution trap, propagated intact. *(sixth review pass, 2026-08-23)*


Room: `e6e06795-9b93-4a37-9905-8c6278293099` · submitted 2026-08-21 · **second-stage study**
Sources: `hyp3/idea1.md` §Two prover branches, `hyp1/idea.md` Table A, `hyp2/idea3.md` §4

## The conflation this paper attacks

Both branches get called "prover training," but they manipulate different semantic objects:

| | Mathematical theorem proving | Formal program verification |
|---|---|---|
| Semantic object | propositions, hypotheses, lemmas, tactic states | states, transitions, pre/postconditions, invariants, frame conditions, VCs |
| Systems | Lean, Isabelle, Rocq/Coq, HOL, Metamath | Dafny, Verus, Frama-C/WP, Boogie/Z3, CBMC, Liquid Haskell |
| Natural process state | open goals + tactic state | parse/type errors, individual VCs, initiation, preservation, postcondition, countermodels |
| Core failure mode | search explosion, autoformalization mismatch | weak/misaligned specification, vacuity, solver limits |

**Hypothesis:** at matched post-training budget, program-verification supervision transfers more
strongly to software-engineering tasks than mathematical-proof supervision, because it explicitly
represents *mutation and state-transition* semantics. Mathematical proof instead buys long-chain
deductive consistency and decomposition.

## Design: a transfer matrix, not a leaderboard

Two training branches × two evaluation families:

|  | Formal math eval (miniF2F-style) | Software eval (code gen, execution reasoning, invariants, semantic equivalence, repair) |
|---|---|---|
| Math-proof arm | **positive control** | transfer question |
| Program-proof arm | cross-branch transfer | **main hypothesis** |

Plus a **curriculum arm** (math-proof → program-proof) testing whether general deduction is a useful
prerequisite or an expensive detour.

> **EXTENDED 2026-08-23 (6th pass) — the delivered arm set is larger.** `paper-draft.revised.md`:36
> trains four conditions `{M, V, C, N}`, where `N` is a **matched non-formal SFT control** that this
> design section omits (the seed mentions it only in its final falsification bullet) and which is
> load-bearing: without it, "formal supervision buys nothing at this scale" is untestable. Curriculum
> order is additionally separated from composition by **Dafny→Lean** and **interleaved** arms at
> equal source quotas — controls this seed does not specify. RQ2's replay-exposure regimes
> (`natural` vs `flattened`) are likewise absent here; see `experiment-spec.md`:43.

**Matching is the methodological contribution and it is genuinely hard.** A Lean corpus and a Dafny
corpus differ in per-example length and acceptance rate, so match by *all four* of: training tokens,
optimizer steps, sampled trajectories, and accepted-trajectory count — and ~~report every
normalization~~. Reporting only the flattering one is the failure mode.

> **STRENGTHENED 2026-08-23 (6th pass).** The delivered design does not report four normalizations
> side by side — it **caps every arm at the common feasible budget intersection**, the largest
> budget simultaneously satisfiable on all four axes (`paper-draft.revised.md`:18). That removes the
> mismatch rather than displaying it, so no normalization can be selectively reported. The four axes
> themselves are unchanged and are enforced by the Budget and Replay Ledger.

**The positive control is a validity gate, not a courtesy.** The math arm *should* win on
mathematical benchmarks; if it does not, the math arm was undertrained and the entire comparison is
void. State this before running, not after.

## Evidence state going in

- The math branch is far more mature as RL (**VERIFIED 2026-08-21**). AlphaProof — Hubert et al.,
  *"Olympiad-level formal mathematical reasoning with reinforcement learning"*, **Nature 651(8106),
  607–613 (2026)**, DOI 10.1038/s41586-025-09833-y, online 2025-11-12; **no arXiv version exists** —
  is genuinely an MDP over Lean states, not an output filter: *"the state s_t is the logical state of
  the Lean prover… The agent interacts by proposing an action a_t, a Lean tactic… reward r_t = −1 for
  each tactic applied."* Compute: *"approximately 80,000 tensor processing unit (TPU) days"* in the
  main RL phase (do not conflate with its per-problem *inference* budgets quoted in TPU-hours);
  autoformalization produced *"around 80 million formal Lean problems"* from ~1M natural-language ones.
- **ATTRIBUTION TRAP — get this right or a reviewer will.** The 28/42 silver-range score belongs to
  the **combined AlphaProof + AlphaGeometry 2 system**, with AlphaProof contributing the three
  non-geometry solutions (P1, P2, P6) and AlphaGeometry 2 solving P4. Never write "AlphaProof scored
  28/42" or "AlphaProof alone reached silver."
- DeepSeek-Prover-V1.5 (Xin et al., arXiv:2408.08152, **ICLR 2025**): 63.5% miniF2F and 25.3%
  ProofNet are **RL + RMaxTS at large search budgets** — 32×6400 = 204,800 generations (with a
  CoT/non-CoT mixture strategy) and 4×6400 = 25,600 respectively. The honest budget-matched
  counterpart is **51.6% pass@128** single-pass. Quoting 63.5% next to our small-model numbers
  without the budget would be misleading.
- Direct math→software transfer remains weakly established. RLTPF — Leang et al., *"Theorem Prover as
  a Judge for Synthetic Data Generation"*, **ACL 2025 Long, pp. 29941–29977**, arXiv:2502.13137 —
  confirms prover-checked *intermediate reasoning steps* improving **informal** arithmetic benchmarks
  (up to ~5–6 points on individual benchmarks: +5.56 Mistral-7B/MultiArith, +6.00 Llama-2-7B/SVAMP,
  +3.55 Llama-3.1-8B/AQUA — per-model bests, not a uniform average). Mechanism evidence, not code
  evidence.
- Precedent for rewarding intermediate formal progress: Dong, Mahankali, Ma, *"Formal Theorem Proving
  by Rewarding LLMs to Decompose Proofs Hierarchically"*, arXiv:2411.01829 — novel proved lemmas make
  up 37.7% of the replay buffer; AFP pass rate 40.8%→45.5% and OOD 36.5%→39.5%.
- The transfer evidence on the *program* side is real but far weaker than the briefs imply
  (**VERIFIED 2026-08-21**). FVEL (NeurIPS 2024 D&B, arXiv:2406.14408) LoRA-fine-tunes on Isabelle
  verification data and raises SV-COMP solved counts **69→81** (Llama3-8B) and **75→84** (Mistral-7B)
  — but out of a **1,000-problem random subset**, i.e. 6.9%→8.1%, on a set where the symbolic solver
  UAutomizer solves **374**. Its authors attribute the gain to corpus correlation: *"Since FVELer
  originates from the seL4 micro-kernel operating system, the correlation of the data makes
  fine-tuning on the SV-COMP dataset effective."* On Code2Inv, Llama3-8B is **46→46**.
- The equivalence-proof transfer result is likewise a single best cell: **+13.3pp on EquiBench's
  **OJ_V subset only** (56.5→69.8), while DCE regresses −3.2 and TVM −1.6 (arXiv:2604.17010).

**This reframes the paper.** The honest motivation is not "program-proof transfer is established and
math-proof transfer is not" — it is that **neither branch has a credible transfer result for code**,
and the field has been citing weak, corpus-correlated gains as though the question were settled. No
published work runs both branches from one shared checkpoint at matched budget and evaluates both on
software tasks with the tools removed.

## Scope honesty (must survive drafting)

At 0.6B–1.7B neither arm produces a strong theorem prover. The claim is about **relative transfer at
small scale**, and the scaling caveat belongs in the abstract, not buried in limitations. A credible
negative — math supervision matching program supervision on code transfer — is equally publishable
and would undercut the "program proof is specially aligned with software" premise the whole loop_r1
program rests on.

## Sequencing

This is deliberately the **second-stage** study of the family. It runs after ZW1 shows signal,
because it introduces an entire extra formal language, dataset and curriculum confound that would
contaminate the first experiment. Every brief in the source set independently reached this ordering:
*use mathematical proving as a control or later pretraining arm, not the centerpiece of the first
PoC.*

## Falsification

- Math arm loses on math benchmarks → undertrained; comparison void, report and stop.
- Both arms transfer equally to code → the state-transition alignment story is wrong.
- Curriculum arm beats both → decomposition skill, not state semantics, is the active ingredient.
- Neither arm beats a matched non-formal SFT control on code tasks → formal supervision buys nothing
  at this scale, and that is the finding.

## 🔎 2026-08-23 pre-push scoop re-sweep (8th pass) — verdict NARROWING-NEEDED (motivation + control claim)

Fresh web audit before repository publication. The head-to-head budget-matched Lean-vs-Dafny
transfer study remains unclaimed — no twin found through 2026-08-23. Two corrections forced:

- **FM-alpaca** (Lu et al., *From Informal to Formal*, ACL 2025 Long, arXiv:2501.16207 — absent
  from this seed's evidence state, a Jan-2025 coverage gap, not a scoop): fine-tunes Llama3.1-8B on
  18k GPT-4o-distilled pairs across **five mixed formal languages** (Coq, Lean4, Dafny, ACSL, TLA+)
  and reports code transfer WITH a non-formal SFT contrast — HumanEval +62.5% relative over
  UltraChat but only +0.95–1.23% over Tulu-v3, MBPP −3.3% on the UltraChat arm. Consequences:
  (1) "neither branch has a credible code-transfer result" must be argued, not asserted — the
  argument is that the one published result is mixed-language, distilled, single-model and
  baseline-fragile, exactly the confounds this design removes; (2) the non-formal control `N` is no
  longer "never run" — claim the **budget-matched, per-branch** version, conceding FM-alpaca's
  additive mixed-corpus contrast as predecessor. Both applied to `paper-draft.revised.md`
  (motivation + related work) this pass.
- **Informal-domain analogue to cite:** arXiv:2506.14965 (cross-domain RLVR transfer matrix,
  math/code/puzzle; asymmetric math↔code transfer incl. degradation cases) — the informal-domain
  precedent for the transfer-matrix framing; no formal provers, no budget-axis matching.

Sequencing-risk signal, no overlap: arXiv:2608.01604 (2026-08-03) shows cross-domain post-training
→ SWE transfer is an active area — the "what supervision teaches software" question is heating up.
Within-formal half-claims logged: arXiv:2508.18587 (cross-proof-assistant transfer → Rocq, no
software eval); arXiv:2502.11901 (PoPilot, F* specialist, no general-code transfer). C2's four-axis
budget matching and C4's curriculum-order design remain fully unclaimed.
