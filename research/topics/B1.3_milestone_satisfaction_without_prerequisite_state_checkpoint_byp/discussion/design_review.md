# Design Review (adversarial, 2026-07-04)

Reviewer stance: skeptical PC member, DESIGN review only. Phase A self-report was
independently re-verified, not trusted. Prior Phase A gate = FAIL (8 cited-but-never-
backfilled references); that verdict is confirmed below, but I also found soundness
defects the prior pass rubber-stamped.

## Verdict summary

| Dimension | Score | One-line reason |
|---|---|---|
| 1. Feasibility & scale | SOUND | CPU-only pilot, named substrates, config-not-code exit criterion, cost bounded; only soft risk is real-agent rollout yield. |
| 2. Soundness | FIXABLE | Estimand ρ is defined over a researcher-controlled distribution D; H1 is near-tautological; A6 power claim is arithmetically wrong; trajectory clustering ignored by every test. |
| 3. Novelty & pre-emption | FIXABLE | Idea not pre-empted, but the novelty argument is grounded in a corpus disjoint from the actual cache; the real cache twins (CodeReproducibilityGap, RevealWeakestLink, MATP) go unaddressed. |
| 4. Hypothesis→fallback | FIXABLE | Fallbacks are verbatim and mostly strong, but the global pivot guards the one hypothesis that cannot fail; the joint failure of the genuinely-at-risk H3/H4/H5 has no combination rule. |
| 5. Method scope & RQ design | FIXABLE | Validity envelope stated; but per-cell power only exists for A6 (and is wrong), no mitigation/detectability RQ, dependence structure unmodelled. |

**Reference-cache integrity is a hard STOP** (goal.md §3 item 2 / §8), separate from the
five design dimensions; it blocks Phase B on its own and the prior pass correctly recorded it.

## Findings (most-severe first)

### [BROKEN] F1 — N3 related-work grounding is built from a corpus disjoint from the cache
The digest's entire N3/N4 and paper.md's motivation/exemplar scaffolding rest on eight
OpenReview papers (TED `fHsVNklKOc`, XENON `N22lDHYrXe`, Gistify `nmdDgo4OXC`, StepORLM
`ZrgxU8WMmG`, LatentVeracity `eux1cp8GqC`, WebArbiter `canA6Ef0RP`, GTool `bn47cqGQ7l`,
DiffTaskGraph `2HvgvB4aWq`). I grepped all eight ids and title strings against
`discussion/reference_candidates.jsonl`: **0/8 appear** — not as `selected`, not even as
`rejected` records. The cache's 11 `selected` entries are a completely different set
(arXiv `2512.*`/`2607.*` + three ACL papers). Per goal.md §3 item 2 ("every N3 key is a
`selected` cache record") and §8 ("citations only via `selected` cache keys"), this fails
outright. paper.md Step 2 cites "Gistify, lost-in-conversation, emergent-abilities-mirage"
as exemplar classes — none are in the cache either.
**Fix:** re-harvest the eight N3 works (or true equivalents) into this cache with digests,
OR rewrite N3/N4 to be grounded in the 11 entries that actually exist. Until then Phase B
is blocked. This is the recorded FAIL and it is legitimate.
Pointer: `digest.md` N3; `discussion/reference_candidates.jsonl`; `stage_review.md` item 2.

### [BROKEN] F2 — The central estimand is defined over a researcher-controlled distribution, making H1 near-unfalsifiable
paper.md Step 5: "ρ := P_{τ∼D}[A(τ)=1 ∧ Ω(τ)=0]", "unit = one completion trajectory τ over
one task in the constructed-suite / real-agent-rollout distribution D". For the constructed
suite, **D is entirely authored by the researchers**: an injection trace is *defined* (M3) as
"directly write the surface signature M2 checks … without executing the real operation," and
A5 filters to only traces where A(τ)=1. So by construction A=1, and if the real work was never
done, Ω=0 — i.e. B(τ)=1 for essentially every injection trace, and ρ_inject → whatever fraction
of the suite is injection. H1 ("ρ̂ ≥ 0.10, lower Wilson > 0.05") is therefore not a discovery but
a design choice. This has two consequences:
(a) **R1 is really two estimands under one symbol.** The constructed-suite ρ (arbitrary,
researcher-set) and the natural-rollout ρ_nat (a genuine population quantity) have different
reference populations and are not the same measurement; R1 requires one. Note pipeline.md line
168 itself concedes "two separately falsifiable estimands … from one instrument."
(b) **H1's "measurement" is a constructibility result**, honestly flagged in digest t3/t5 and
F4, but the paper's framing (Claim 1: "not a sufficient proxy") reads as an empirical rate when
the constructed number is an artifact of D.
**Fix:** split the estimand explicitly — ρ_constructed is an *existence/constructibility* claim
(state it as such, drop the ≥0.10 "hypothesis" framing; it is closer to a walking-skeleton
sanity gate), and reserve the population-level estimand language for ρ_nat (RQ_INF_3), which is
the genuinely at-risk, publishable quantity. Re-weight the paper's headline accordingly.
Pointer: `paper.md` Step 5 estimand + RQ1/H1; `digest.md` N10 t3/t5.

### [FIXABLE] F3 — A6/H4 power statement is arithmetically wrong (~57%, claimed ≥0.9)
paper.md A6: "≥200 M2-complete rollouts is sized to detect the H4 effect floor (ρ_nat ≥ 0.02) at
power ≥0.9 … a true rate of 0.02 needs ~200 Bernoulli trials." H4's decision rule requires
ρ̂_nat ≥ 0.02, i.e. observing ≥4 events in 200 trials. At the true floor 0.02, I computed
P(≥4/200) = **0.569** — the criterion threshold has been set equal to the effect floor, so at the
floor you detect it ~57% of the time (median behaviour), not 90%. (The weaker "lower bound > 0"
event, ≥1/200, does have power 0.98 — but that is not H4's stated criterion.) The prior Phase A
pass marked item 9 PASS on the strength of "A6 now has a power statement" without checking the
arithmetic.
**Fix:** either (i) raise n so P(ρ̂≥0.02 | true=0.02) ≥ 0.9 (needs ~n≈450–600), or (ii) separate
the effect floor from the decision threshold (power at ρ_nat = 0.04 say, and declare H4 detectable
only above that), or (iii) restate H4's criterion as "lower Wilson bound > 0" (power 0.98 at n=200)
and drop the ρ̂≥0.02 conjunct. As written, RQ_INF_3 — the one genuinely at-risk hypothesis — is
under-powered for its own criterion.
Pointer: `paper.md` A6 + RQ_INF_3/H4.

### [FIXABLE] F4 — Dependence structure ignored: trajectories are clustered in tasks, every test assumes independence
H1 uses a one-sided exact binomial over "≥300 constructed trajectories (20–40 pilot tasks × … ×
~5 variants)"; H3 uses "a logistic regression of B(τ) on … depth and in-degree … Wald p<0.05";
H2/H4 use two-proportion z-tests. All treat trajectories as i.i.d. Bernoulli, but they are nested
within 20–40 tasks (≈5–15 traces/task sharing DAG structure, verifier code, oracle). Intra-task
correlation makes the effective n far below 300, so Wilson intervals and Wald SEs are too narrow
and false-positive rates inflated — precisely the risk on H3 (topology), the paper's most
inferentially load-bearing empirical claim. Holm across H1–H4 controls FWER under dependence
(fine), but does nothing for *within-hypothesis* clustering.
**Fix:** cluster-robust or mixed-effects models with task as the grouping factor (task random
intercept for the H3 logistic regression; cluster-bootstrapped Wilson intervals for H1/H4);
report the number of *tasks* alongside the number of trajectories as the effective n.
Pointer: `paper.md` RQ1/RQ_INF_2/RQ_INF_3 verification lines.

### [FIXABLE] F5 — Global pivot F-G1 guards the un-failable hypothesis; the real failure combination is uncovered
F-G1 fires only if "ρ̂ indistinguishable from 0 across all three strategies (H1/H2/H3 fail) AND
against the strongest checker." Per F2, ρ_inject cannot realistically be ~0 (injection writes the
checked signal by definition), so **F-G1 is effectively dead machinery.** Meanwhile the plausible
bad outcome — H1 passes trivially, but H3 (topology flat), H4 (no natural incidence), and H5
(strong checkers halve the rate) *all* fail — has **no pre-committed combination rule**. That
outcome leaves the paper with: "we can trivially construct a bypass, it isn't modulated by
structure, real agents never do it, and a slightly better checker mostly defeats it" — a very
thin paper, and the spec has no verbatim wording for it. guidance.md §3.1 requires the
fallback-combination rules to be written now.
**Fix:** (a) re-target the global pivot at the H3+H4 (structure + deployment) family, not H1;
(b) add an explicit F3∧F4∧F5 combination sentence, pre-committing the honest narrowed claim
("checkpoint bypass is a constructible artifact of milestone-locality that stronger local checkers
substantially mitigate and that real agents do not exhibit unprompted — a design caution, not a
measured deployment risk").
Pointer: `paper.md` "Global fallback F-G1"; fallbacks F3/F4/F5.

### [FIXABLE] F6 — Novelty argument does not engage the actual cache method-twins
The 11 `selected` entries include structurally very close work the paper never addresses:
`CodeReproducibilityGap2025` ("code passes the assumed-sufficient functional benchmark yet fails a
separate disjoint reproducibility oracle" — the same local-signal-vs-disjoint-oracle asymmetry in
the code domain), `RevealWeakestLink2024` (step-level verification because final-answer correctness
masks invalid steps), `MATPLogicalFlaws2025` (correct surface signal, invalid steps). Their `why`
fields (verified on disk, all digests resolve) are genuinely on-topic — no cross-topic
contamination — but paper.md concede-and-differentiates against the *other* (disjoint-corpus)
papers instead. Differentiation from these is achievable (explicit prerequisite DAG + adversarial
reorder/skip/inject construction + milestone-scoped rather than final-answer scope), but it is
currently undefended.
**Fix:** in the same re-harvest that fixes F1, fold the real cache twins into N3/N4 and write the
nearest-neighbor concession against CodeReproducibilityGap and RevealWeakestLink.
Pointer: `reference_candidates.jsonl` selected entries; `paper.md` Step 2 / Claim–Evidence Map row 7.

### [NOTE] F7 — paper_draft.* is stale relative to paper.md
`discussion/paper_draft.md` (13:29) predates paper.md (19:12); it contains 0 occurrences of "H5"
vs 9 in paper.md, so the B-alt→H5 formalization, the estimand sentence, and the A-ledger relabel
are not reflected in the draft. Noted once, not penalized further — Phase E has not run.

## Failure-space simulation (per-H)

- **H1 (ρ ≥ 0.10)** — cannot realistically fail on injection traces (F2). F1 wording is credible as
  robustness certification but will almost never be invoked. *Coverage: over-provisioned.*
- **H2 (inject dominates by ≥10pp)** — can fail cleanly; F2 ("no single strategy dominates …
  generic to locality") is a fine, publishable downgrade. *Covered.*
- **H3 (topology modulates)** — can fail; F3 ("flat structural property") is publishable. But the
  Wald test is mis-specified for clustered data (F4), so a *false* pass is a live risk. *Covered
  wording, under-rigorous test.*
- **H4 (natural incidence ≥ 0.02)** — likely the true at-risk hypothesis; F4 fallback ("constructibility
  result, latent risk") is publishable but substantially demotes the paper's deployment relevance,
  and the arm is under-powered for its own criterion (F3). *Covered wording, under-powered.*
- **H5 (bypass survives strongest checker)** — can fail; F5 verbatim downgrade (mechanism reattributed,
  Claim 1 survives downgraded, Claim 3 falls) is exemplary. *Covered.*
- **Uncovered combination:** H1 trivially passes ∧ {H3, H4, H5} all fail → no pre-committed sentence;
  F-G1 does not fire because it is keyed to H1≈0. **This is the failure outcome that leaves the paper
  thin, and the design does not currently name it.** (See F5.)

## Missing RQs / reviewer questions the design cannot answer

1. **Mitigation / detectability RQ.** The paper measures the vulnerability but never tests the obvious
   fix a reviewer will demand: does a *lightweight cross-milestone provenance/ordering check* (cheaper
   than the full terminal oracle) recover soundness, and at what cost? CO3 asserts the terminal oracle
   as the audit pattern but no RQ evaluates a deployable, cheaper detector. Without it the paper says
   "here is a hole" and stops.
2. **Per-checker-type sensitivity as a hypothesis, not just reporting.** A3 is demoted to "continuous
   reporting discipline," so the paper cannot answer "which checker types are actually vulnerable?"
   with any inferential claim — yet that is the single most actionable question for a benchmark
   designer.
3. **Power for RQ1/RQ_INF_2 cells.** Only A6/H4 has a power statement (and it is wrong). A reviewer will
   ask for the per-cell power of the topology regression (H3), whose cells (depth × in-degree bins) are
   where the constructed suite thins out fastest.
4. **Robustness of ρ_nat to task-completion yield.** RQ_INF_3 needs ≥200 M2-complete real-agent rollouts;
   if agent completion rates on hard multi-step tasks are low, the 3,000–5,000-rollout budget may not
   yield 200 complete ones. The design does not state the assumed completion rate.

## Reliability audit of prior Phase A result

Independently re-checked goal.md §3 items 2, 4, 5, 6 (the ones most likely rubber-stamped):

- **Item 2 (reference-cache integrity) — HELD.** The prior pass's headline STOP is fully supported:
  I re-ran the grep, 0/8 N3 ids in the cache, and confirmed the 11 selected entries are a different
  corpus. Not rubber-stamped; correctly caught.
- **Item 4 (claim–evidence orphans) — HELD.** The current Claim–Evidence Map traces all seven rows to
  an H-id-with-fallback or a supported-by-design definition; the H5/F5 fix genuinely closed the one
  orphan the prior pass named. Verified.
- **Item 5 (seven-slot completeness) — PARTIALLY RUBBER-STAMPED.** The prior pass says "H1–H4 already
  filled all seven slots." In fact H1–H4 are written in prose, not the §3.1 slot template; `aggregation`
  is implicit/absent for H1/H3/H4 (single-test), and `applies_if` is stated as "Assumption:" lines. Only
  H5 is genuinely in seven-slot form. Cosmetic gap, but the claim of full compliance is generous.
- **Item 6 (Part 6 self-check) — PARTIALLY RUBBER-STAMPED.** Item 9 (power per cell) was marked
  effectively PASS on the basis that "A6 now has a power statement," but that statement is arithmetically
  false (F3: ~57%, not ≥0.9). Item 6's R2 N/A ruling is defensible (instruments are deterministic; no
  LLM-judge). The dependence/clustering issue (F4) is not surfaced anywhere in the self-check.

Reference-record spot check: 3 randomly chosen `selected` entries (`CodeReproducibilityGap2025`,
`RevealWeakestLink2024`, `RLVRAtlassianToolUseAgents2026`) — all `digest_path` and `pdf_path` resolve on
disk; all three `why` fields are on-topic for verifier sufficiency (no cross-topic contamination). The
cache that *exists* is clean; the problem is that the paper doesn't use it and uses a phantom corpus instead.

**Bottom line:** the prior gate's FAIL verdict is reliable and well-supported at the top level, but the
"REVISE fired and fixed" claims for the machinery items overstate the fix quality — a wrong power
calculation and an unmodelled dependence structure passed through.

## Overall: NEEDS-REVISION

The core idea is sharp (the many-to-one projection asymmetry passes the deletion test and is not a bridge),
the archetype/control skeleton is genuinely strong (B0 calibration, B-alt→H5 strongest-checker attribution,
verbatim fallbacks), and it is cheaply executable. But it is not clear-to-build as written: one hard STOP
plus three substantive soundness defects.

**Three highest-leverage fixes:**
1. **Re-harvest and re-ground N3/N4** in the actual cache (fixes the STOP that blocks Phase B) and
   concede-and-differentiate against the real twins (CodeReproducibilityGap, RevealWeakestLink). [F1, F6]
2. **Reframe the estimand and headline:** ρ_constructed is a constructibility/existence result (demote H1
   from "measurement hypothesis" to sanity gate), and make ρ_nat (RQ_INF_3) the at-risk headline — then
   fix its power (n≈450–600 or decouple threshold from effect floor) and re-target F-G1 at the H3/H4
   family with an explicit mixed-failure combination rule. [F2, F3, F5]
3. **Model the dependence:** cluster/mixed-effects tests with task as the grouping factor for H1/H3/H4,
   and report tasks (not just trajectories) as the effective n. [F4]

## Fixes applied (2026-07-04)

Authorized direct-edit pass following the review above. One line per edit.

**paper.md**
1. Step 2: replaced memory-cited exemplar class with cache keys (`PLMCalibrationCloseLook2023`, `CodeReproducibilityGap2025`); old exemplars marked [UNVERIFIED — requires harvest]. [F1/F6]
2. Step 2: added "Positioning against the verified reference cache" concede-and-differentiate block for CodeReproducibilityGap2025 / RevealWeakestLink2024 / MATPLogicalFlaws2025 (guidance Part 4 situation 6); stated no positioning depends on the 8 phantom works. [F6]
3. Step 5: split the estimand — primary/headline ρ_nat over D_nat (H4), secondary constructibility ρ_c over researcher-authored D_c (H1); never pooled. [F2]
4. Step 5 notation: ρ redefined as conditional on A(τ)=1 and instantiated separately as ρ_c / ρ_nat. [F2]
5. A3: TED citation marked [UNVERIFIED]; assumption re-anchored on cache records MCPAgentBenchToolUse2026 / RLVRAtlassianToolUseAgents2026. [F1]
6. A6: corrected power statement with inline arithmetic — decision threshold decoupled from floor (ρ̂≥0.01 ≡ ≥2 events at n=200 → power P(X≥2|Bin(200,0.02)) ≈ 0.91 ≥ 0.9); documented that the old rule (threshold=floor) had power ≈0.57 and cannot reach 0.9 at any n; added ≥20-distinct-task requirement for the cluster bootstrap. [F3]
7. Step 6 preamble: added dependence-structure analysis-plan note (task-level cluster bootstrap / cluster-robust SEs / mixed model; n_tasks reported everywhere) and headline note (H4 headline, H1 gate). [F4, F2]
8. RQ1/H1: reframed as constructibility gate / manipulation check with role note; CI switched to task-level cluster bootstrap. [F2, F4]
9. RQ_INF_1/H2 verification: cluster-robust (task-level) SEs / GEE. [F4]
10. RQ_INF_2/H3: statement and verification switched to mixed-effects logistic regression with task random intercept. [F4]
11. RQ_INF_3/H4: marked HEADLINE; criterion re-specified (ρ̂_nat ≥ 0.01 at n=200, floor 0.02, pre-declared edge cases: ρ̂=0 → FAIL, 0<ρ̂<0.01 → INCONCLUSIVE-at-n with required-n recorded); cluster-bootstrap CI. [F2, F3, F4]
12. H5 test slot: cluster-robust non-inferiority test, paired by task. [F4]
13. Global fallback section rewritten: F-G1 re-pointed at the failable family (H4 ∧ H5 fail) with new pre-committed pivoted abstract; added FC-1 verbatim combination wording for "H1 passes trivially ∧ H3/H4/H5 all fail" plus pairwise-combination rule; original all-zero pivot retained as F-G1a. [F5]
14. Claim–Evidence Map row 1: scoped to constructibility/existence reading; fallback trace F-G1a. [F2]
15. Claim–Evidence Map row 4: marked HEADLINE claim, F-G1 linkage. [F2, F5]
16. Claim–Evidence Map row 7: gap claim re-traced to the verified cache with residual-harvest caveat. [F1]
17. Abstract v0: natural incidence foregrounded as headline estimand; constructed traces described as constructibility gate; task-clustered intervals mentioned. [F2, F4]

**digest.md**
18. N3: added dated cache-integrity update note demoting entries 1–8 to [UNVERIFIED — requires harvest] (globally downgrading every dependent [GROUNDED:corpus] tag in N2/N4/N5–N8/Claims 1–3); Status line and works header updated. [F1]
19. N3: added verified cache-grounded entries 9–11 (CodeReproducibilityGap2025, RevealWeakestLink2024, MATPLogicalFlaws2025) with [GROUNDED:cache] tags; absence_comment rewritten to rest on the verified cache. [F1, F6]
20. N4: added preamble note (limitations 1–5 non-load-bearing pending harvest; 6–8 load-bearing). [F1]
21. N4: added limitations 6–8 for the three cache twins with concede-and-differentiate deltas. [F6]
22. Claims: Claim 4 rewritten to rest on verified-cache coverage (150 triaged / 11 selected), phantom works explicitly excluded from its support. [F1]

**Not fixed here (needs human/network/compute):** re-harvest of the 8 demoted OpenReview works into the cache (no network in this environment — remains the Phase-B-blocking item); Phase B/C execution; regeneration of stale `paper_draft.md`/`.tex`/`.pdf` (F7 — Phase E artifact, predates all of today's paper.md changes); exact power re-derivation at walking-skeleton scale-up; per-cell power derivation for H3's topology bins (flagged in review §Missing RQs item 3).
