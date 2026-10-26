# ZW2 — AutoDiscussion draft review

> ## 📖 DATED REVIEW RECORD — one of its conclusions was later reversed
>
> Written 2026-08-21 against the room's raw output, before five adversarial review rounds.
> **Its "Fix 1" praise for the adequacy-aware estimator is wrong and was reversed in round 2** —
> marked inline. Its two mandatory fixes were applied; its `[VERIFY]` markers are resolved below.
> *(sixth review pass, 2026-08-23)*


Room `98e3ae6b-50e4-4a0c-8763-675d94a6ebcc` · closed 6/6, **5/6 clean**, 1 unresolved major
(related_work) · reviewed 2026-08-21
Artifacts: `completed_jobs_dirs/ZW2 Verified but Wrong…--98e3ae6b/` — `research-report.md` (714 L),
`paper-draft.md` (259 L), `experiment-spec.md` (217 L)

**Verdict: adopt with fixes.** The pipeline produced a *better formalization* than the seed, with
zero fabricated statistics. Two fixes are mandatory before this draft is usable; one is a corpus bug
that affects the whole first wave.

## Where the draft beats the seed

The draft retitled itself *"Tracking Dafny Specification-Adequacy Gaps with Paired Behavioral Oracles
and Semantic Audits"* and improved the estimator in three ways the seed did not specify:

1. ~~**Adequacy-aware verification indicator.** `V_i = A_i · D_i · (1 − Q_i)` where `A` is verifier
   acceptance, `D = 1[Dom(P_i) ≠ ∅]` (non-empty precondition domain) and `Q` is vacuity. A proof
   discharged over an empty domain is *recorded* but contributes zero to the verification rate. The
   seed asked for vacuity instrumentation; the draft folded it into the estimand, which is stronger.~~

   > **⚠️ REVERSED in review round 2 — this assessment was wrong.** Folding adequacy into the
   > *estimand* is weaker, not stronger: it nulls out the phenomenon. For a vacuous acceptance
   > `A=1, B=0` we get `V=0`, so the pair contributes **zero** to `V−B` — the estimator reports its
   > smallest gap exactly where spec hacking is worst. The manuscript now defines
   > `δ = Pr(A=1) − Pr(B=1)` on **raw** acceptance (`paper-draft.revised.md`:70–73) and keeps `V`
   > only for the decomposition `δ = [Pr(V)−Pr(B)] + [Pr(A)−Pr(V)]`. Points 2 and 3 below stand.
2. **Escrowed oracles.** Human-audited executable oracles plus property-based generators, fixed
   before training, excluded from reward, run with **secret seeds** — so `B` cannot leak into the
   optimization signal. Paired `(V, B)` per candidate with a nested bootstrap over tasks *and* test
   seeds preserves within-candidate dependence. This is the right answer to "how do you know the
   behavioral oracle stayed independent."
3. **Multi-label mechanism audit.** The seed's mechanism list assumed one label per candidate; the
   draft correctly makes it multi-label, since empty domains and vacuity co-occur, and adds a crossed
   mechanism calibration corpus to test identifiability.

Scope discipline held — 0.6B model, Dafny single-function corpus, existing prover infrastructure —
so this package does **not** show the fleet-wide scope-inflation failure mode.

## Fix 1 (mandatory) — the strongest evidence is missing

The draft's motivation argues from benchmarks (VERINA, CLEVER, VeriCoding) and never cites the two
measurements that make the problem concrete. Neither appears anywhere in the draft:

- Tan (arXiv:2605.30914): verified reward **2.2% → 58.1%**, then after filtering underspecified tasks
  the verified pass rate is only **9.7% → 31.1%**.
- Re:Form §3.3: *"the model exploits the reward function by omitting unverifiable clauses and
  producing trivial specifications that are easy to verify but semantically weak."*

Cause is known: ZW2 was submitted in wave 1 **with no `references` payload**, so the room never saw
the Tan thesis. Add both to the motivation — the 58.1%→31.1% collapse is the single best existing
measurement of the quantity this paper estimates properly.

## Fix 2 (mandatory) — off-topic citations contaminated the retrieved corpus

Two papers from unrelated fields were retrieved into the related-work corpus:

- Helenius & Utheim, *"Hadron-ion collisions in Pythia and the vector-meson dominance model for
  photoproduction"* — **particle physics**.
- Polanco Olsen et al., *"A new thermodynamic function for binary mixtures: the co-molar volume"* —
  **physical chemistry**.

They are real papers, wrongly retrieved. **They did not leak into `paper-draft.md` or
`experiment-spec.md`** — the pipeline's downstream filtering caught them — but they occupied
retrieval slots and sit in the research report. Also: one entry is credited to *"(unknown authors)"*
(Scaling Laws for Reward Model Overoptimization — Gao, Schulman, Hilton).

**Implication beyond this room:** every wave-1 room ran discovery with no seeded references. The
ZW1/ZW3 twins were resubmitted with 22 verified citations precisely to close this hole; ZW4 is still
running without them and should get the same audit on completion.

> **RESOLVED (stale as written).** ZW4's original room `2a72d422` died in a retry loop; its twin
> `7bcfe3ef` was resubmitted **with** the 22-reference payload and its corpus came back 100% seeded,
> zero off-topic. Seeding references fixed the retrieval bug outright.

## Fix 3 — the residual major (related_work), quoted

> "The summary reports paper and baseline counts without comparing how verifier-guided training,
> specification-quality evaluation, and static certification differ relative to the delta objective.
> Consequently, the collective motivation for the current problem remains unclear."

Fair and cheap to fix: group the related work into the three families and contrast each against δ
rather than enumerating counts. Two of the three minors are also worth taking — the CLEVER entry
contradicts itself (its summary says the benchmark *excludes* vacuity-permitting specifications while
the limitation says vacuity is *not distinguished*; the real limitation is the absence of
longitudinal, reward-conditioned measurement), and the DeepSeek-R1 entry is generic background, not
problem-specific.

## Citation audit

**Zero confabulated statistics** — the draft makes almost no numeric claims at all (only 90/95/98%,
which are design targets, not literature figures). Re:Form's retrieved abstract matches the real one
verbatim and carries the **correct** title ("Reducing Human *Annotations*"), independently confirming
the correction we made to the briefs.

Genuinely useful discoveries the seed missed, all real: **VERINA** (189 curated Lean tasks; o3 gets
72.6% code correctness, 52.3% specification soundness/completeness, 4.9% proof success), **CLEVER**,
the **VeriCoding** benchmark, **Laurel** (LLM-generated Dafny assertions), Endres et al. on
NL-intent → formal postconditions, and Lahiri on user-intent formalization for verification-aware
languages. Fold VERINA's 4.9% proof-success figure into the motivation — it independently shows how
far verified generation is from solved. ~~**[VERIFY]**~~ these six against primary sources before drafting;
they came from the room's own retrieval, not from our audited reference set.

> **RESOLVED 2026-08-23 (6th pass).** Verification was done and is recorded in the manuscript's
> revision log, not here — VERINA is **ICLR 2026 (Poster)**, not a preprint, and the o3 figures
> (72.6 / 52.3 / **4.9**) are the v3 numbers with the "one trial per task" qualifier, now cited at
> `paper-draft.revised.md`:16 and :329.

**Formatting defect:** citations render as `Author et al.. Title.` with doubled periods and no venue,
year, or identifier. Unusable as-is — needs a real bib pass.
