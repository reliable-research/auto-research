# ZW1 — Obligation-Level Credit Assignment: Verifier-Checked Verification Conditions as an RL Reward for Code Models

> ## 📌 SUBMITTED-INPUT ARTIFACT — NOT THE DELIVERED DESIGN
>
> This is the `idea_text` sent to the AutoDiscussion room, preserved verbatim for provenance.
> **It is two design generations behind `paper-draft.revised.md`.** Superseded in three places, each
> marked inline below: the six-arm G0–G5 table and the three-phase staging (delivered design is
> four arms A1–A4, single phase, 0.6B only); `countermodel-guided repair` as a training objective
> (withdrawn with the multi-turn claim); and the tool-off endpoint list, which names benchmarks the
> delivered design does not run. Corrections carrying novelty or citation content — the
> GraphAlignCoder and RLFR blocks — **did** propagate and are still authoritative.
> *(sixth review pass, 2026-08-23)*


*(Retitled from "ProofWorld: Verification-Condition Transitions as Semantic Process Supervision" —
see the novelty collapse below.)*

Rooms: ~~`687d0e9e`~~ (stalled r15) → ~~`91a3c142`~~ → ~~`fdb5f013`~~ → **`0843dd6e-df4e-44b8-9bf1-5f57d591200a`**
Sources: `hyp3/idea2.md` (ProofWorld formulation), `hyp2/idea3.md` (final direction), `hyp1/idea.md` §Recommended experiment

## ⚠️ NOVELTY COLLAPSE — 2026-08-21 scoop sweep

Three works published in the last eight months occupy parts of the original framing. The claim had
to be narrowed, and the concessions must appear in the paper rather than being discovered by a
reviewer. **GraphAlignCoder was subsequently read in full (v1; v2/v3 return 404) — every claim in the
row below is quoted or token-counted from the paper, and it corrected one error in our first
narrowed seed.**

| Work | What it takes | What it leaves |
|---|---|---|
| **GraphAlignCoder**, arXiv:2608.11394, **2026-08-11** (ten days before the sweep) | Formal obligations as *training-time structure* for a code LLM, evaluated **prover-off** on Python: *"At inference, θ₂ receives the ordinary programming input and emits one Python solution, with no implementation graph or proof-flow graph."* Solved counts 50/175 LiveCodeBench v6, 23/148 BCB-Hard, 363/1140 BCB-Full | **No RL of any kind** — `L_inject = L_code + L_concept + L_obligation`, token-level teacher-forced NLL; standalone "RL" occurs 0×, "reward" occurs **once, metaphorically**. Obligations are **GPT-5.2-authored text the model predicts**, filtered by an unstated criterion. Lean checks a **template-instantiated auxiliary theorem, not the Python program**; the only link is a role-name **set intersection** `A_i = C_i^I ∩ C_i^F`. **No program verifier** (Dafny 2× — background + bibliography; Verus/Frama-C 0×). **No verdicts** (refuted/countermodel/SMT/Z3 all 0×). **No dense-execution baseline** (only CodeRL, terminal pass/fail; "unit test" 0×). **No budget matching** ("budget" 0×). No limitations section, no seeds, no variance, no significance test |

> **Correction to our first narrowed seed.** It said GraphAlignCoder's obligation types were "informal
> … with no named taxonomy." **That is wrong.** Its taxonomy *is* fixed and named —
> `{boundary, invariant, progress, return}` — it simply differs from ours and carries no verdicts.
> Misdescribing a competitor is exactly the kind of error that discredits a related-work section, so
> the room was resubmitted (`0843dd6e`) with the corrected reading. The real differentiator is
> stronger than the one we had claimed: **their obligations are LLM-authored and Lean-checked against
> a synthetic theorem, so no soundness relation to the generated program exists at all**, whereas ours
> are verification conditions the verifier emits *about the candidate program*.

> **Their own ablation is worth citing neutrally.** Consolidation-only reaches **49/175** on
> LiveCodeBench v6 against the full method's **50/175** — the entire Lean and graph-alignment
> apparatus buys **one task out of 175** — and the BCB-Full margin over CodeRL is 363 vs 359, four
> tasks out of 1,140. Report the numbers; let the reader conclude.
| **RLFR**, The Haladir Team, **2026-01-06**, *non-archival, unrefereed, and now DELETED from the live web* (HTTP 404; one Wayback capture: `web.archive.org/web/20260108115201/…`) | **⚠️ The closest prior work.** Offline single-turn GRPO on a 17,521-program Dafny corpus from Re:Form's Python2Dafny data (8×B200, 2,460 steps). Reward is **shaped and per-proof-obligation** — `R_k = verified_goals_k / total_goals_k` — explicitly motivated *against* binary: *"Unlike unit test-based verification which provides binary pass/fail signals, this process yields fine-grained feedback through partial proof completion."* Reports prover-free Dafny→Python transfer: HCT 22.0 vs 18.3 base pass@1 on LiveCodeBench 2406-2409 | **Ran no execution-supervision baseline at any budget** — every non-RLFR number is copied from published tables — yet asserts it "establishes that RLFR outperforms standard execution-based baselines," which its own experiments do not support. Reward is an **undifferentiated ratio**: obligations untyped, so a failed loop invariant is indistinguishable from a failed postcondition. Its weighted per-category variant "was not implemented for this report." **No verdict structure** — timeout, unknown and refutation collapse into one not-discharged count. Offline single-turn, so no progress signal. No spec-hacking measurement. No models, code, or data released |

> **⚠️ MAJOR CORRECTION — 2026-08-21, and it forced a fourth resubmission (`29167d1d`).** Both our
> first and second narrowed seeds described RLFR's reward as **binary**. **It is not.** It is a shaped
> per-proof-obligation ratio — i.e. RLFR already occupies the "structured beats binary" position that
> the second seed claimed for us. Publishing that mischaracterization would have inflated our novelty
> against the one paper closest to us, in exactly the direction that flatters us. Two further
> provenance corrections: the Wayback snapshot id circulating in our notes (`20260417194155`) **does
> not exist** — an exact-match CDX query returns exactly one capture ever, `20260108115201` — and the
> live URL does **not** redirect to a marketing page, it returns **HTTP 404** (the post was removed;
> the July 2026 site bundle contains zero occurrences of "rlfr"). Also, the transfer quote as it
> reached us was a **misquote** that dropped "quite" and "some level of," both omissions strengthening
> the claim relative to what the authors wrote.

> **🔎 2026-08-23 pre-push re-sweep (8th pass) — verdict CLEAR; one correction to the correction.**
> A fresh web audit found no method twin through 2026-08-23: GraphAlignCoder is still v1-only with
> no follow-ups; RLFR has not resurfaced; no new work uses typed per-obligation verifier verdicts
> as a training reward, and none runs the matched proof-vs-execution comparison. New non-scooping
> neighbors to cite: **VeRPO** (arXiv:2601.03525, dense *test-based* partial credit — independent
> evidence that reward density is a live confounder, strengthening the A3/A4 coarsening controls);
> **SpecRL** (arXiv:2604.05820, inverse task — specs from tests); **TCPO** (arXiv:2608.01667,
> turn-level credit for multi-turn verifier RL — confirms withdrawing the multi-turn claim was
> prudent, that space is being occupied); **The Verification Horizon** (arXiv:2606.26300,
> motivation). Provenance: the Wayback claim in the block above is **over-broad** — snapshot
> `20260417194155` exists for `haladir.com/research/rlfr` (readable, corroborates the single-turn/
> no-execution-baseline reading; multi-turn is its "Next Steps") while `20260108115201` is the
> `/blog/rlfr` JS shell holding the formula; cite both per the superseding rule in
> `major_fix_rlfr_anchor.md`. Also flag: OpenReview/TMLR titles Re:Form "…Reducing Human
> **Priors**…" while arXiv v4 says "Annotations" — check at camera-ready.

**What ZW1 is now**, after RLFR: the contribution is no longer "per-obligation reward" — that is
taken. It is **(1)** the matched head-to-head against dense execution-state supervision, *which RLFR
claims but never ran*; **(2)** typed obligations with a **verdict lattice**, asking whether knowing
*which* obligation failed and whether it was *disproved* versus merely *undecided* beats RLFR's scalar
ratio; ~~**(3)** multi-turn progress against RLFR's offline single-turn setup.~~ **WITHDRAWN 2026-08-21 (5th pass):** never instantiated — the delivered design is single-generation like RLFR's, with progress measured between syntactic-completion boundaries inside one generation rather than across repair turns. Claiming it would assert a capability the design does not have. ZW1 rests on (1) and (2). A **mandatory ablation**
collapsing our typed vector to RLFR's `verified_goals/total_goals` is now in the seed — without it a
reviewer correctly says we reimplemented RLFR with extra steps.
| **Process-Verified RL for Theorem Proving via Lean**, arXiv:2606.20068 | *Our exact motivating argument*: RLVR "has relied on a single binary verification signal" while proof assistants "offer rich, fine-grained structured feedback"; implements tactic-level verified rewards | **Lean mathematics only** — no code generation, no program verifier, no obligation-level decomposition, no tool-off transfer; budgets explicitly not comparable |

**Claims now forbidden:** first use of a verifier as an RL reward (Re:Form) · first use of
formal-obligation structure as training-time supervision for a code LLM (GraphAlignCoder) · first
demonstration that Dafny post-training survives prover removal (RLFR) · first argument that
structured beats binary formal feedback (2606.20068).

**The narrowed claim, which is genuinely untouched:** per-obligation, **verifier-checked verdicts
emitted by a deductive program verifier about the candidate program itself**, used as an **RL reward
providing credit assignment over a verdict-valued obligation set**, benchmarked head-to-head against
equally dense **execution-state supervision at matched budget**. Supporting negative: an arXiv
full-index query for `"verification condition"` AND `"reward"` returns **zero results, ever**.

The differentiator is **not** that our taxonomy is named — theirs is too. It is that (a) supervised
imitation of obligation *text* cannot express partial credit over an obligation set that the model's
**own generated program** induces, (b) our supervision is **sound by construction** rather than
aligned by name overlap, and (c) the **verdict lattice** distinguishes *disproved* from *undecided* —
meaningless as a text prediction target, load-bearing as a reward.

**Tool-off evaluation is now inherited, not claimed.** GraphAlignCoder owns it as a headline first
with numbers on the board. The paper adopts it as a shared protocol, cites them for it, and competes
on where the evaluation *goes* — unseen loop schemas, invariant repair without countermodels,
predicting which VC fails, semantic equivalence, Defects4C repair, and the perturbation battery.

Two consequences for the design. First, the **transfer suite** is the contribution on the tool-off
axis, not the bare transfer claim — RLFR already has that — so evaluation must go where RLFR's did
not (unseen loop schemas, invariant repair without countermodels, predicting which VC fails,
semantic equivalence, Defects4C repair, plus the perturbation battery). Second, a **new and valuable
falsification** exists: since GraphAlignCoder got prover-off gains from obligation structure via
plain SFT, if RL credit assignment over verifier-checked obligations cannot beat SFT on serialized
obligation text at matched budget, then the reward channel is *not* where obligation structure does
its work — a finding that would redirect the field.

## Problem-side evidence (VERIFIED 2026-08-21 — this is the motivation, not the gap argument)

The failure this paper addresses is **documented today**: the formal-feedback systems that work
best deliberately keep the verifier *outside* the model, so their gains are scaffolding that
evaporates when the tool is removed.

- **Proof2Silicon / PREFACE** (Jha, Wan, Chen; arXiv:2509.06239): PPO trains a *small language model
  that writes prompts*; the target LLM is **frozen**. Verbatim: *"iteratively repairs the prompts
  provided to **frozen LLMs**… without costly fine-tuning."* The verified-code gain provably lives
  outside the model's parameters.
- **LORIS** (Li, Yan, Liu, Di, Zhang; **ACM TOPLAS 48(2), Art. 8, May 2026**, arXiv:2605.17914): uses
  exactly our signal — *"our method focuses the LLM on a single failed VC from 𝕍ℂ_fail at a time"* —
  but entirely at inference, against closed APIs (gpt-4.1, gpt-4.1-mini, Claude-3.7-Sonnet). The
  strings "fine-tun"/"finetun" occur **zero times** in the paper. The structured VC signal exists and
  has never been used to update parameters. **Our novelty claim is safe.**
- **AlphaVerus** (Aggarwal, Parno, Welleck; arXiv:2412.06176): *"enables a LLaMA-3.1-70B model to
  generate verified code without human intervention or model finetuning"* — stochastic few-shot
  exemplars, not learning.
- **The one system that does train on verification data reports weak transfer.** FVEL (NeurIPS 2024
  D&B, arXiv:2406.14408) fine-tunes via LoRA SFT and improves SV-COMP solved counts 69→81 (Llama3-8B)
  and 75→84 (Mistral-7B) — but **out of a 1,000-problem random subset**, i.e. 6.9%→8.1%, while the
  symbolic solver UAutomizer solves 374 on the same set. Its authors attribute the gain to corpus
  correlation, not general capability: *"Since FVELer originates from the seL4 micro-kernel operating
  system, the correlation of the data makes fine-tuning on the SV-COMP dataset effective."* On
  Code2Inv, Llama3-8B goes 46→46 — zero gain.

So: three leading formal-feedback systems avoid touching model parameters *by design*, and the one
that touches them reports a gain its own authors explain away as dataset correlation. That is the
present-day concern — not a hypothetical one — and it is what makes the tool-off endpoint the point
of this paper rather than a robustness check.

## Central claim

A deductive program verifier is not an accept/reject oracle — it is a **symbolic state-transition
environment**. Training on its internal transitions teaches program semantics that survive the
verifier's removal.

Proof state: `Z = {O_init, O_preserve, O_exit/post, O_safety, O_termination}`, each obligation
carrying a categorical verdict `z_j ∈ {proved, refuted-with-countermodel, unknown, timeout,
invalid}`. A model action `a_t` (proposed invariant, annotation, code edit) induces `Z_t → Z_{t+1}`.
Learn the transition structure — proof-state prediction, transition prediction, ~~countermodel-guided
repair~~ — instead of the single bit `1[verified]`.

> **SUPERSEDED 2026-08-23 (6th pass).** `countermodel-guided repair` is a *repair* objective: it
> presupposes the model acts on a countermodel and re-submits, i.e. the multi-turn setting withdrawn
> above. The delivered design has no repair turns, and its sealed evaluation **disables countermodel
> access** (`paper-draft.revised.md`, abstract). Reward is computed from the verdict-vector *delta*
> between consecutive syntactic-completion snapshots inside one generation. The `μ·(R_VC^(t) −
> R_VC^(t−1))` progress term below survives, but `t` indexes snapshots, not turns.

## Reward design (preregistered, not tuned post-hoc)

```
R_proof = Σ_j w_j·V(z_j) / Σ_j w_j   +   λ·1[∀j: z_j = proved]   +   μ·(R_VC^(t) − R_VC^(t−1))
```

Non-negotiable design rules, each of which is a reviewer attack surface if violated:

- **Timeout ≠ counterexample.** A solver timeout is its own verdict class, never scored as refutation.
- **Weights are preregistered** (simple normalized weights, or a monotone aggregation learned on a
  disjoint dev split), and the paper reports the raw obligation *vector* plus several fixed
  scalarizations. Hand-picking a weighted scalar after seeing test performance converts the
  contribution from "formal supervision" into "reward engineering."
- **Never reward raw VC count** or "number of verifier messages that disappeared."

## Arms and the primary contrast

| Arm | Signal |
|---|---|
| G0 | shared code SFT only (frozen baseline) |
| G1 | final test/execution outcome reward |
| G2 | dense execution-state supervision (ExecVerify-style: next statement, variable value/type) — see the reward caveat below |
| G3 | binary verifier result |
| **G4** | **structured VC state + transition supervision (proposed)** |
| G5 | hybrid VC + execution |

**Primary causal comparison is G4 vs G2** — proof-process against *equally dense* execution-process
supervision. The easy G1-vs-G3 contrast (unit tests vs binary verifier) is not the paper.

> **SUPERSEDED 2026-08-23 (6th pass) — the delivered study has four arms, not six.**
> `experiment-spec.md` §M1 trains **A1 typed-verdict** (= G4), **A2 dense execution-state** (= G2,
> the primary contrast baseline), **A3 binary verifier** (= G3), and **A4 RLFR-style
> verified-goals-ratio** — an arm this seed does not contain, added as the mandatory scalar-collapse
> ablation demanded by the RLFR correction above. **G0** (SFT-only), **G1** (test-outcome) and
> **G5** (hybrid) are not implemented; `hybrid` occurs zero times in the draft and spec. The primary
> comparison A1-vs-A2 is unchanged and correct.

**G2 must be reproduced honestly (VERIFIED 2026-08-21).** ExecVerify's reward is *not* stepwise-only:
Stage I mixes the white-box term with a terminal I/O-correctness term at α = 0.5
(`R = 2·((1−α)·R^(I→O) + α·R_white)`, ≤10 sampled white-box questions per instance), and Stage II
switches to a unit-test pass-fraction reward. A "pure stepwise" G2 would be a straw man; replicate
the two-stage structure or state the deviation explicitly.

**Do not repeat the briefs' misquote of ExecVerify.** Its headline is **5.9% *relative*** pass@1 gain
(cross-benchmark average 53.9 → 57.1, i.e. **+3.2 percentage points**) over a pure unit-test-GRPO
baseline on the same 7B backbone — the paper itself is internally inconsistent ("5.9%" vs "5.9
points") and no table cell supports 5.9 pp. Its execution-reasoning result is solid and worth citing
straight: average 60.8 → 80.8, above Qwen2.5-Coder-32B-Instruct's 77.9 (one 32B comparator, so
"competitive with 32B models" plural is loose).

**Paired-oracle protocol.** Every sampled candidate is scored by *both* the fixed test harness and
the fixed verifier before arm-specific rewards are computed, so reward source is the manipulated
variable. Honest caveat that must appear in the draft: after the first parameter update, on-policy
arms diverge — "identical candidates" holds only at the seeding stage, and matched sampled-token
budgeting carries the rest of the comparison.

## Primary endpoint: tool-OFF

Verified-solve-rate with the prover present is the *secondary* endpoint; Re:Form and several
inference-time systems already make a higher verifier acceptance rate unsurprising. The primary
endpoint removes the prover:

unseen loop schemas · invariant selection and repair without countermodel feedback · predicting
which VC will fail · execution reasoning · semantic equivalence · ordinary code generation ·
Defects4C-style C/C++ repair.

Robustness battery (the memorization test): variable renaming, dead-code insertion, equivalent loop
rewrites, reordered independent statements, changed constants, unseen invariant templates,
Dafny→C/Python translation. A model that memorized Dafny invariant boilerplate collapses here; a
model that learned induction over program state degrades gracefully.

## ~~Staging (the gate structure must not be deleted in drafting)~~

> **SUPERSEDED 2026-08-23 (6th pass) — this section did not survive drafting, and the heading's
> instruction was not followed.** The delivered study is **single-phase at 0.6B**: `1.7B`,
> `Defects4C`, `SWE-EVO` and `RoadmapBench` each occur **zero times** in `paper-draft.revised.md`
> and `experiment-spec.md`. G2 is in the primary contrast from the first update rather than deferred
> to Phase 2, so the Phase-1 gate below ("proceed only if G4 beats G3") has no delivered analogue.
> The gate that *is* delivered is different in kind: RQ3(c)'s **usable-packet-rate gate**, which
> decides whether the dense comparison is interpretable at all. The transfer ladder below is
> aspiration, not design; treat the endpoint list in "Primary endpoint: tool-OFF" the same way —
> the delivered tool-off evaluation is the Matched hidden-test suite plus the perturbation battery.

- **Phase 1 (0.6B):** G0 / G1 / G3 / G4 only, on a single-function Dafny corpus — linear and
  polynomial loops, branches, arrays, given pre/postconditions, known valid invariants, executable
  reference implementations. Question answered: *does VC decomposition add anything beyond final
  proof acceptance?*
- **Gate:** proceed only if G4 beats G3 on a preregistered tool-free measure.
- **Phase 2:** add G2 and G5, replicate at 1.7B (same architecture/tokenizer/pretraining family).
- **Phase 3:** transfer ladder — Dafny OOD → semantic equivalence / execution reasoning → ordinary
  code generation → Defects4C repair. Repository-scale evolution (SWE-EVO, RoadmapBench) is stretch
  evaluation, not a make-or-break endpoint.

Compute planning anchor: ~64 GPU-h per 0.6B arm at 200k candidates, ~960 GPU-h for the 0.6B core
with seeds, ~145 GPU-h per 1.7B arm — extrapolated with ~30% systems margin, easily 0.5×–2× off.
**VERIFIED 2026-08-21 with a correction:** Re:Form (arXiv:2507.16331, TMLR 05/2026) never reports
GPU-hours. Its Table 2 gives GPU count × wall-clock separately for the *subset reward model* config
on A800-SXM4-80G — 0.5B: 16 GPUs × 11 h, 1.5B: 16 × 25 h — so "176 / 400 GPU-h" is our arithmetic,
not their figure, and the 40-epoch detail attaches **only to the 3B run**. Cite it as derived.

## Novelty ledger

| Prior | What it owns | Why ZW1 is not it |
|---|---|---|
| Re:Form, arXiv:2507.16331, TMLR 05/2026 ("Reducing Human **Annotations**…: A Preliminary Study on Dafny" — the briefs mistitle it "Priors") | Dafny verifier-driven RL, Qwen-2.5 0.5B–14B, ~20k Dafny functions, open pipeline; 14B RL hits 14.0% OOD pass@1 vs 8.3% SFT-only | binary/terminal verifier reward; no matched execution arm; no tool-off endpoint |
| LORIS, TOPLAS 48(2) 2026, arXiv:2605.17914 | per-VC localized feedback to repair invariants | **inference-time only** — verified: zero fine-tuning, closed-API models |
| ExecVerify, arXiv:2603.11226 (preprint, no venue) | dense execution-process reward | no formal-proof reward condition |
| RLEF, **ICML 2025, PMLR 267:19034–19055**, arXiv:2410.02089 | multi-turn execution-feedback RL, 8B+70B, ≥30× sample reduction on CodeContests | no prover comparison |
| FVEL, **NeurIPS 2024 D&B**, arXiv:2406.14408 | Isabelle verification-data LoRA SFT + SV-COMP transfer | SFT, not a reward-source comparison; and the transfer is weak (see problem-side evidence) |
| StepCodeReasoner, arXiv:2605.11922 | stepwise execution-trace RL alignment | second dense-execution comparator; no formal condition |
| ORPS — cite as *"Reasoning Through Execution: Unifying Process and Outcome Rewards for Code Generation"*, **ICML 2025, PMLR 267:72972–72994**, arXiv:2412.15118 (the v1 title differs) | execution-fused process+outcome supervision via search | search/self-critique, not a reward-source comparison |
| μCODE, **ICML 2025 Spotlight**, PMLR 267:26700–26716, arXiv:2502.20380 | multi-turn code gen via single-step rewards | execution oracle only |
| Hierarchical theorem-proving RL | rewarding intermediate lemmas | mathematical proofs, not program state |
| Proof2Silicon / PREFACE | verifier-feedback RL on a *prompt/controller* policy | target LLM stays frozen — no retained capability claim |

Claim to make: *we model deductive program verification as a symbolic state-transition environment
and use VC transitions as machine-checkable **training-time** process supervision.* Claim never to
make: *first use of a formal verifier as an RL reward.*

## Falsification

- G4 improves only while the verifier is available (→ prover is scaffolding, not learning).
- G4 cannot beat G3 (→ VC decomposition adds nothing).
- G4 loses to G2 at matched compute (→ dense execution supervision is sufficient).
- Formal acceptance rises but hidden-test correctness does not (→ see ZW2).
- Gains vanish under renaming or loop rewrites (→ Dafny template memorization).

A negative result that maps the boundary between execution and proof supervision — a phase diagram
rather than a winner — is still the paper.
