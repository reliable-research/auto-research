# ZW1 — fix for the unresolved major: the G3b ablation arm has no anchored prior work

> ## 📖 DISCHARGED FIX MEMO — the merge it asks for was completed
>
> Written 2026-08-21 while the experiment spec was still generating. **Its "merge into
> `paper-draft.revised.md` on sync" instruction is discharged** — the RLFR anchor, the
> formula-faithful-ablation wording and the reward formula all landed in the manuscript's Related
> Work. Kept as the provenance record of why that arm is anchored, not as an open action.
>
> **Arm-name key.** This memo uses the *seed's* six-arm `G0`–`G5` numbering, which the delivered
> design withdrew. `G3b` = the verified-goals-ratio arm, written \(\mathrm{GR}\) in the manuscript
> and `A4` in `experiment-spec.md`; `G4` = the typed-verdict arm, \(\mathrm{TV}\) / `A1`. The
> manuscript no longer uses `G` names anywhere. *(ninth review pass, 2026-08-23)*

Room `29167d1d-a681-490f-9361-6e7b02a89d39` · closed 6/6, **5/6 clean, 1 unresolved major**
Written 2026-08-21 while the experiment spec was generating; merge into `paper-draft.revised.md` on
sync.

## The critic's objection, verbatim

> "The problem statement names the RLFR-style verified-goals ratio as a mandatory ablation arm, yet
> none of the eight deeply compared works instantiates a scalar proof-ratio or
> goals-verified-fraction reward; the baseline set covers execution-state, binary-verifier, and
> Dafny-RL signals but leaves the ratio arm without any anchored prior work, which weakens the
> legibility of the comparison for exactly the contrast the study must run."

**The critic is right, and the cause is ours.** RLFR *is* the anchor for G3b — it is the published
instance of the scalar `verified_goals / total_goals` reward — but it was omitted from the room's
`references` payload because it **has no arXiv ID**. The API's citation schema accepts
`{citation, url}` without `arxiv_id`; we simply did not use that form. The room was therefore asked
to justify an ablation arm against a work it could not see.

**Reusable lesson, recorded in the family README:** references lacking arXiv IDs must still be
passed, or any arm depending on them will be flagged as unanchored.

## The fix: anchor G3b explicitly

### Citation form (non-archival, deleted from the live web)

> The Haladir Team. *RLFR: Reinforcement Learning from Formally-Defined Rewards for Code Generation.*
> Haladir blog, 6 January 2026. Non-archival industry report. Original URL
> `https://haladir.com/blog/rlfr` no longer available (HTTP 404 as of 21 August 2026); archived at
> `https://web.archive.org/web/20260108115201/https://www.haladir.com/blog/rlfr` (accessed
> 21 August 2026).

Conventions to follow: give the **archive URL as the primary locator**, not a "see also"; state both
the access date and the fact that the original is dead; and label it "non-archival industry report"
in the prose so a reader calibrates its evidential weight. Do **not** cite the JavaScript bundle URL
from which the text was recovered — that is retrieval method, not artifact. **Keep a local copy of
the recovered text**, since a single-capture Wayback record is fragile.

Two provenance corrections against notes circulating earlier in this project: the snapshot id
`20260417194155` **does not exist** (an exact-match CDX query returns exactly one capture ever,
`20260108115201`), and the live URL does **not** redirect to a marketing page — it returns **HTTP
404**; the post was removed, and the July 2026 site bundle contains zero occurrences of "rlfr".

> **🔎 2026-08-23 re-sweep (8th pass): the first correction above is itself over-broad.** The two
> earlier notes were each right about a *different URL*. The CDX record shows `20260417194155`
> **does exist — for `haladir.com/research/rlfr`** (8.5KB, fully human-readable), while
> `20260108115201` attaches to `haladir.com/blog/rlfr` and is a 1,168-byte JS shell whose rendered
> text is just "Haladir" — the R_k formula and the quoted sentences are recoverable only from its
> JS bundle. The `/research/rlfr` capture was retrieved in full on 2026-08-23 and independently
> corroborates the core reading (Dafny; 17,521-program Re:Form-derived corpus; GRPO on
> Qwen2.5-Coder-7B-Instruct and Qwen3-8B; single-turn; prover-free "+3.7 percentage points"
> LiveCodeBench transfer; multi-turn SMT-counterexample refinement listed verbatim under **Next
> Steps**, i.e. future work) but does **not** contain the per-obligation formula. **Citation rule
> that supersedes the one above:** cite the April `/research/rlfr` capture
> (`web.archive.org/web/20260417194155/https://www.haladir.com/research/rlfr`) as the readable
> primary locator, and the January `/blog/rlfr` capture plus the local copy for formula-level
> quotes. Scope, don't drop, the "does not exist" sentence.

### Related-work paragraph to insert

RLFR belongs in the same paragraph as Re:Form, immediately before the G3b arm is introduced:

> Closest to the reward studied here, a non-archival industry report (The Haladir Team, 2026) trains
> Qwen2.5-Coder-7B-Instruct and Qwen3-8B with offline single-turn GRPO on a 17,521-program Dafny
> corpus derived from Re:Form's Python2Dafny data, using a **shaped per-proof-obligation reward**:
> \(R_k = -1\) when the skeleton or syntax fails, \(R_k = \text{verified\_goals}_k /
> \text{total\_goals}_k\) when verification runs, and \(0\) when no goals are present. The authors
> describe it as computing "the proportion of verified proof obligations discharged, providing
> continuous gradients for partial correctness," and motivate it explicitly against binary signals:
> "Unlike unit test-based verification which provides binary pass/fail signals, this process yields
> fine-grained feedback through partial proof completion." They report prover-free transfer to
> Python, with their HCT variant reaching 22.0 pass@1 on LiveCodeBench (2406–2409) against an 18.3
> base, alongside smaller gains on HumanEval+ and MBPP+, and conclude that training purely on Dafny
> suggests "some level of generalization past the formal verification domain."
>
> We therefore do **not** claim novelty for a graded per-obligation proof reward, nor for the
> observation that Dafny post-training can survive removal of the verifier. We adopt that reward as
> **arm G3b** and ask a narrower question: whether *typing* the obligations and distinguishing
> *disproved* from *undecided* carries information beyond the proportion discharged. Three properties
> of that report make the question live rather than settled. Its reward is an **undifferentiated
> ratio**: obligations are untyped, so a failed loop invariant is indistinguishable from a failed
> postcondition, and a weighted per-category variant is defined but, in the authors' words, "was not
> implemented for this report." It carries **no verdict structure**: timeout, unknown, and refutation
> collapse into the same not-discharged count. And it runs **no execution-supervision baseline at any
> budget** — every non-RLFR number in its tables is quoted from published technical reports and the
> LiveCodeBench leaderboard — while nonetheless asserting that "this report establishes that RLFR
> outperforms standard execution-based baselines on general coding benchmarks." That comparison is
> the one this study runs.

Report the evidential caveats plainly and without editorializing: the work is unrefereed, releases no
models, code, or data, withholds its methodology pending contact with the authors, and its Table 1
compares RLFR models on LiveCodeBench 2406–2409 against external models quoted at 2407–2411 — so the
base-versus-RLFR contrast is internally consistent but the cross-model claims are not on a common
window.

### G3b arm specification

RLFR is unrefereed, is no longer available at its original URL, and releases no implementation
details, so an exact reproduction cannot be claimed. G3b is therefore a **formula-faithful ablation
under our harness**: it reuses RLFR's published reward formula and nothing else, and that limitation
is stated wherever the arm is reported. Define it as:

```
R_k = −1.0                                    if skeleton/syntax fails
      verified_goals_k / total_goals_k        if verification runs
      0.0                                     if total_goals_k = 0
```

under our own harness and the same offline single-turn GRPO configuration used for the other arms,
differing from G4 **only** in that the obligation vector is collapsed to its discharged proportion.
We do not claim to reproduce RLFR's results, only to instantiate its reward. Any other difference confounds the
ablation. G4-minus-G3b then isolates exactly two factors — obligation typing and the verdict lattice
— and if that difference is null, the honest conclusion is that RLFR's simpler published reward was
sufficient and should be preferred.

## Why this strengthens rather than weakens the paper

Anchoring G3b makes the contribution legible instead of merely narrower. The paper's claim becomes:
*a graded per-obligation proof reward already exists and already transfers prover-free; what has
never been tested is whether the structure inside that ratio matters, and whether either beats dense
execution-state supervision at matched budget — a comparison RLFR asserts without running.* That is
a smaller claim than "ProofWorld" as originally framed and a considerably more defensible one.
