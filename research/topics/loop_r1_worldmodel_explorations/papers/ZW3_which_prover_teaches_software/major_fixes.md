# ZW3 — fixes for the two unresolved majors

> ## 📖 DISCHARGED FIX MEMO — the merge it asks for was completed
>
> Written 2026-08-21 while the experiment spec was still generating. **Its "merge into
> `paper-draft.revised.md` when the room syncs" instruction is discharged**: both major fixes landed,
> and Major 1's replacement design was then extended in review round 3 with the deterministic
> round-robin redistribution rule this memo does not mention (see `paper-draft.revised.md` and
> `experiment-spec.md`, which are authoritative). Kept as provenance, not as an open action.
> *(ninth review pass, 2026-08-23)*

Room `9f4da36d-840e-4a7d-8c60-860b6c8581e6` · closed 6/6, **4/6 clean, 2 unresolved majors**
Written 2026-08-21 while the experiment spec was still generating; merge into
`paper-draft.revised.md` when the room syncs.

---

## Major 1 (experiment_design) — the transport step is vacuous

**The critic's objection, verbatim:**

> "Rq-2 now specifies weight construction, but the transport step remains ill-defined: the Hájek
> weights are indexed over training examples while the paired-W estimand is a mean over held-out
> evaluation prompts of a fixed trained model, and no channel is described by which reweighting the
> accepted-trajectory training distribution changes a held-out prompt's outcome. As written, the
> weighted and unweighted estimates could be identical by construction, making the equivalence test
> vacuous and leaving replay-exposure robustness untested."

**This is correct and it is the most substantive criticism produced anywhere in this batch.** It is a
real statistical error, not a presentation complaint, and it must be fixed by changing the
experiment, not the wording.

### Root cause

The seed asked for matching on four normalizations — training tokens, optimizer steps, sampled
trajectories, **and accepted-trajectory count** — precisely because a Lean corpus and a Dafny corpus
differ in per-example length and acceptance rate. The draft addressed the accepted-trajectory
mismatch with a **post-hoc importance-weighting estimator** (Hájek weights) instead of a design
control. That cannot work:

- The weights live on **training examples**.
- The estimand is a mean over **held-out evaluation prompts** of an **already-frozen checkpoint**.
- Once the checkpoint is frozen, its held-out behaviour is a deterministic function of the weights
  that were actually used during training. Reweighting the training set afterwards changes a
  bookkeeping quantity, not the model. There is no channel from one to the other.

So the weighted and unweighted estimates coincide by construction, and the "equivalence test" tests
nothing. Worse, it would *appear* to pass — a null result manufactured by the estimator's algebra
would read as evidence of replay-exposure robustness.

### Fix A (adopt this) — match by design, upstream of the checkpoint

Subsample the larger arm's accepted trajectories down to the smaller arm's accepted count **before
training**, with the subsample drawn under a preregistered rule and a fixed seed. Then the arms are
matched on accepted-trajectory count by construction and no weighting is required or claimed. Report
all four normalizations side by side, and report which of them bind:

| Normalization | Math arm | Program arm | Binding? |
|---|---|---|---|
| Training tokens | | | |
| Optimizer steps | | | |
| Sampled trajectories | | | |
| **Accepted trajectories** | | | |

Reporting only the flattering normalization is the failure mode the seed warned about; reporting all
four makes the mismatch visible rather than corrected-away.

### Fix B (only if composition, not count, is the question) — intervene on training

If the intended question is sensitivity to the *composition* of the accepted set rather than its
size, the only valid test is to **retrain**: draw K resampled accepted sets under the alternative
composition, train K checkpoints per arm, and compare held-out means across checkpoints. Weighting
can influence a held-out outcome only through the parameters, so the intervention has to happen
before the parameters are fixed. This is expensive — budget it explicitly or drop the question.

### What to state in the paper

Replay-exposure robustness is a property of the **training pipeline**, testable only by intervening
on training. Any analysis-side reweighting of a frozen model's held-out outputs is uninformative
about it. Say this plainly; it is a methodological point worth making, since the temptation to
substitute a weighting correction for a design control is general.

---

## Major 2 (related_work) — circular limitations

**The critic's objection, verbatim:**

> "All eight limitation descriptions are near-identical restatements of the study's own research
> question ('they never pose the budget-matched transfer question with a math positive control'),
> which makes them problem-relative but undifferentiated and borderline circular. Each entry should
> instead surface that work's distinct evidential gap … so the limitations can independently motivate
> sub-problems rather than uniformly asserting 'this paper is not our study.'"

This is the **fourth room in a row** to take a major on `related_work` for this defect (ZW2, ZW3t,
ZW4t, and the pattern is recorded in the family README). The test each entry must pass: *would this
still be a gap if our paper did not exist?*

### Replacement limitations, each independently motivating

All figures below are primary-source verified (2026-08-21).

| Work | Gap that stands on its own |
|---|---|
| **Re:Form** (TMLR 05/2026, arXiv:2507.16331) | Evaluates generalization **only within Dafny/DafnyComp**. Its headline OOD result — 14.0% pass@1 for the 14B RL model vs 8.3% SFT-only — is out-of-domain *inside formal verification*, so it is silent on whether any capability reaches ordinary software tasks |
| **FVEL** (NeurIPS 2024 D&B, arXiv:2406.14408) | The one system that trains on verification data and measures downstream transfer, and its own authors attribute the gain to corpus correlation: *"Since FVELer originates from the seL4 micro-kernel operating system, the correlation of the data makes fine-tuning on the SV-COMP dataset effective."* The effect is 69→81 and 75→84 **out of a 1,000-problem subset** (6.9%→8.1%, 7.5%→8.4%) where the symbolic solver UAutomizer solves 374, and Code2Inv shows 46→46 — zero gain |
| **LORIS** (TOPLAS 48(2) 2026, arXiv:2605.17914) | **Inference-time only** — the strings "fine-tun"/"finetun" occur zero times and all experiments use closed commercial APIs. It provides no training signal at all, so it cannot speak to what formal supervision teaches a model |
| **DeepSeek-Prover-V1.5** (ICLR 2025, arXiv:2408.08152) | **Never evaluates on any code task.** Its 63.5% miniF2F and 25.3% ProofNet are RMaxTS results at 32×6400 and 4×6400 search budgets (204,800 and 25,600 generations); the single-pass counterpart is 51.6% pass@128. Strong evidence about proving, none about programming |
| **AlphaProof** (*Nature* 651(8106):607–613, 2026) | Demonstrates that Lean proof states work as an RL environment at ~80,000 TPU-days, but evaluates only mathematics. Its 28/42 belongs to the **combined AlphaProof + AlphaGeometry 2 system** (AlphaProof solved P1, P2, P6), and no code-transfer claim is made or tested |
| **RLTPF / Theorem Prover as a Judge** (ACL 2025 Long, arXiv:2502.13137) | Shows prover-checked intermediate reasoning improving **informal arithmetic** benchmarks (up to ~5–6 points on individual benchmarks, per-model bests). Establishes a transfer *mechanism* outside the prover's own domain, but never to code |
| **Semantic-equivalence self-play** (arXiv:2604.17010, ACL 2026 Findings) | The best proof-to-code transfer evidence available, and it is narrow: **+13.3 points on EquiBench's OJ_V subset alone** (56.5→69.8) while DCE regresses −3.2 and TVM −1.6. Its volume-controlled ablation uses ≈150 pairs, which its own Limitations section flags |
| **Hierarchical lemma-decomposition RL** (arXiv:2411.01829) | Establishes that rewarding intermediate formal progress works — novel proved lemmas form 37.7% of the replay buffer, AFP 40.8%→45.5%, OOD 36.5%→39.5% — but the OOD generalization measured is **within theorem proving**, leaving open whether decomposition skill is domain-portable |

### The framing these support

Read together, these gaps say something the draft should state directly and which is stronger than
the seed's original framing: **neither branch has a credible code-transfer result.** The program-proof
side rests on a corpus-correlated 1.2-point subset gain that its own authors disclaim; the math side
has no code evaluation at all. The field cites both as if the question were settled. That is what
makes the budget-matched two-arm comparison worth running — and it is why a credible negative
(math supervision matching program supervision on code transfer) would be equally publishable.

### Baseline flagging (accompanying minor)

The artifact marked every work `is_potential_baseline=false`. At minimum, **Re:Form is the
program-verification arm's training recipe** (Dafny RL demonstrated down to 0.5B) and
**DeepSeek-Prover-V1.5 is the math arm's**. Mark both as arm-supplying and say so.
