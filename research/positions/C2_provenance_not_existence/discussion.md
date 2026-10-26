# Discussion — Candidate 2: "Registries must gate on provenance, not existence"

> **Full-paper framing (position = the paper's stance, not a position-track submission).**
> This document plans a FULL experimental paper: an implementable security experiment that
> (1) simulates the slopsquatting registration race, seeded from the confirmed name-recurrence
> statistics of arXiv:2607.12340; (2) implements a trust-tiered install-time provenance gate;
> and (3) measures its security/usability operating points against the four published defense
> baselines. The "existence is attacker-satisfiable by construction; provenance is not"
> argument is the paper's Introduction stance, now backed by a measured demonstration.
> Auto-research-discussion format: 6 stages, each with an internal critic → refine pass.
> Sources: `position_paper_pipeline_2026-08.md` (Candidate 3 + novelty ledger row 2 + venue
> runway).

---

## Stage 1 — Problem definition

**Input (what is wrong, who holds it).** Agent-facing registries — package indexes (npm,
PyPI), MCP server registries, and skill marketplaces — and the defenses proposed for them
gate trust on *existence-class predicates*: does the name exist, is the package old enough,
is it popular/downloaded enough, does a real artifact resolve. The defense literature
endorses this: the slopsquatting systematic review (rs.3.rs-8007192) explicitly endorses
*existence validation*; arXiv:2607.12340 itself lists name reservations and RAG-grounding
(check the name against a real index) as its closing recommendations. Who holds the belief:
registry operators, agent framework designers auto-installing recommended tools/packages,
and the security researchers proposing existence/grounding as the fix.

**Output (what the paper delivers and argues).** Because LLMs hallucinate plausible names at
stable, predictable rates (36.0/36.9/43.1% across settings; 5,669 distinct hallucinated
names; recurrence predictable enough to pre-register — arXiv:2607.12340), *the attacker
chooses when to make any existence/age/popularity predicate true* by registering the
predicted name in advance. Existence-keyed defenses therefore fail **by construction, not by
implementation** — the attacker satisfies the predicate on schedule. The paper demonstrates
this empirically (simulate the race; show each existence-class defense is defeated by
pre-registration) and shows the alternative — an install-time gate keyed on *publisher
provenance* (identity/signature/attestation), which the attacker cannot satisfy without
compromising a trusted identity — holding at a better security/usability operating point
than the published RAG-grounding defense. The stance: registries must move the trust
decision from existence to provenance, generalized across all three registry classes as one
ecosystem-design principle.

**Critic:** "Existence is attacker-satisfiable" is close to a definitional truth — an
attacker who registers a name trivially makes it exist. A reviewer can say the paper's
central claim is a tautology dressed as a finding, and that a *simulation* seeded from one
paper's statistics proves nothing an argument couldn't state in a paragraph. Where is the
experimental content?

**Refined:** The experimental content is not "existence can be satisfied" (granted) but the
*quantified economics and operating-point comparison* that turn the tautology into an
engineering verdict: (a) how cheaply, and with what lead time, can an attacker satisfy each
*graded* existence predicate (not just existence, but age ≥ N days, downloads ≥ K, "not
flagged") given the published recurrence distribution — i.e., a registration-cost-per-
predicate-class table; (b) what security/usability point does a trust-tiered provenance gate
achieve versus the four published baselines on the *same* simulated attack, especially
versus RAG-grounding's known 40.8%→3.2% hallucination-block at ~16% recall cost. The paper's
claim is comparative and measured: provenance dominates existence-class defenses on the
security/usability frontier under a realistic, literature-seeded attacker — that is not a
paragraph, it is a benchmark.

---

## Stage 2 — Motivation

**Why now.** (a) The enabling measurement just landed: arXiv:2607.12340 gives stable
cross-setting hallucination rates AND a recurrence structure — the exact quantity an
attacker needs to pre-register, and the exact quantity a simulation needs to seed a
realistic adversary. (b) The registry classes are proliferating faster than their trust
models: MCP server registries and skill marketplaces are being stood up now with
existence-only or no gating (trend scan §2.1–2.2: MCP/A2A governance-gap papers 2606.31498,
2607.02116 show protocol-layer trust is unspecified). (c) Short half-life (pipeline ledger
row 2): the security cluster is publishing monthly, so an implemented, measured
demonstration beats an argument to print and holds its ground longer than a position would.

**Binding evidence (only what the pipeline doc lists; [READ] unless noted):**
- [READ] **arXiv:2607.12340** — the anchor and the adversary seed. 36.0/36.9/43.1%
  hallucination rates across settings; 5,669 distinct hallucinated names; self-audit only
  51–53% accurate; RAG defense cuts hallucination 40.8%→3.2% but costs ~16% recall. This
  single paper supplies: the attacker's name distribution (to seed the race), and three of
  the four defense baselines with their published operating points.
- [corpus] **trend scan §2.1–2.2 (MCP/A2A governance-gap: arXiv:2606.31498, 2607.02116)** —
  independent evidence that protocol-layer trust is unspecified across the newer registry
  classes; motivates the three-class generalization.
- [established, needs citation sweep] **npm/PyPI typosquatting + provenance precedent** —
  the existence→signature→publisher-trust progression OS package managers already made
  (Sigstore, npm provenance attestations, PyPI trusted publishing). Well-established;
  citation sweep required before drafting.
- [NEEDS VERIFICATION] Newer datum from the pipeline sweep: package-level hallucination
  compressed to 4.6–6.1% in the 2026 frontier cohort (arXiv:2605.17062) yet remains
  adversary-economical — verify before using; it *strengthens* the position (lower rate,
  same attack economics) so it must be handled honestly, not omitted.

**Critic:** The entire adversary is seeded from ONE paper's statistics. If arXiv:2607.12340's
recurrence numbers are specific to its models/prompts/time, the simulated attacker is a
model of one lab's measurement, not of the ecosystem — and the frontier-cohort datum
(4.6–6.1%) suggests the rate is already moving, so a simulation frozen at 36–43% may model a
threat that is receding.

**Refined:** Turn the rate-sensitivity into a designed axis instead of a hidden assumption.
The simulation sweeps the hallucination/recurrence rate across the published range —
36–43% (2607.12340) down to 4.6–6.1% (2605.17062, once verified) — and reports the
security/usability frontier as a *function* of that rate. The position's core claim is
rate-robust by construction: even at 4.6% with predictable recurrence, the attacker still
chooses when to satisfy existence predicates, so existence-keyed defenses still fail *in
kind*; what changes with rate is only the attack's yield, which the sweep quantifies. This
converts "seeded from one paper" from a threat-to-validity into a reported robustness
result, and pre-empts the "the rate is dropping" reviewer.

---

## Stage 3 — Related work positioning

Named occupants from the novelty ledger (row 2), each concede-and-claim:

1. **Trustworthy MCP Registry (Future Internet 18(5):243, Sigstore-based).**
   *Concede:* they own a concrete cryptographic-provenance *architecture* for MCP registries
   — Sigstore-style signing/attestation, engineered and specified; we do not claim to invent
   provenance mechanism, and we cite them as the reference implementation of the "how."
   *Claim:* they are MCP-only and offer no *impossibility argument* for the alternative and
   no *comparative measurement* — they build provenance because it seems good, not because
   they show existence fails by construction; our delta is (a) the defeated-by-construction
   demonstration that makes provenance *non-optional*, (b) the generalization across all
   three registry classes as one principle, and (c) the head-to-head operating-point
   comparison against existence/RAG/self-audit baselines they never run.

2. **Slopsquatting systematic review (rs.3.rs-8007192) — a DIRECT FOIL.**
   *Concede:* they own the comprehensive threat cataloguing of the slopsquatting phenomenon
   and list provenance attestations as one mitigation among many.
   *Claim:* they *also endorse existence validation* as a defense — which our experiment
   shows is attacker-satisfiable by construction; the delta is a measured refutation of a
   recommendation a systematic review currently makes, i.e., we don't add provenance to a
   list, we remove existence from it with data.

3. **arXiv:2607.12340 (the anchor) — occupant of "name reservations as closing
   recommendation."**
   *Concede:* they own the phenomenon measurement and propose name reservations + RAG
   grounding as defenses; our entire adversary and three baselines come from their numbers,
   fully credited.
   *Claim:* name reservation is itself an existence-class defense (reserve the name so the
   attacker can't) — a race the defender loses whenever the attacker predicts and registers
   first, which their own recurrence statistics show is feasible; the delta is showing their
   recommended defense is defeated by the very recurrence they measured, and that provenance
   is the gate that does not depend on winning the reservation race.

(Cited context, per the pipeline sweep: threat taxonomies arXiv:2604.02837; MCP/A2A
governance-gap papers as evidence the trust layer is unspecified.)

**Critic:** Conceding the Future Internet paper "owns provenance architecture" risks
conceding away the paper's engineering novelty — if they already built the Sigstore-based
gate, our "trust-tiered install-time gate" may be their gate re-implemented, and the paper
reduces to "we ran their gate against a simulated attack," which is thin for a security
research track. Also, foiling a *preprint* systematic review (rs.3.rs-8007192, a Research
Square preprint) may look like attacking an un-vetted target.

**Refined:** Sharpen what our gate adds over the Future Internet architecture: not the
signing mechanism (theirs, cited) but the *trust-tiering policy and its measured operating
points* — a graded gate (untrusted / signed / attested-publisher / reputation-established)
with an explicit security-usability tradeoff curve, evaluated across three registry classes,
which a single-tier MCP-only Sigstore gate does not provide. The contribution is the
*evaluation and the policy design*, not the crypto. On the foil: cite the systematic review
as *representative* of the existence-validation endorsement (which also appears in
2607.12340's own recommendations and in operator practice), so the refutation targets a live
position held in multiple venues, not one preprint — the argument stands even if that
specific preprint never passes review.

---

## Stage 4 — Sub-problems (argumentative sub-claims, each with evidence and weakest point)

**SC1. LLM name-hallucination is stable and predictably recurrent — the attacker has a
targetable, pre-registerable name distribution.**
- *Evidence:* 2607.12340's 36–43% rates, 5,669 distinct names, recurrence structure; the
  frontier-cohort 4.6–6.1% datum showing the phenomenon persists at lower rates.
- *Weakest point:* recurrence measured in a research setting may not equal what an attacker
  can predict in the wild (model/version drift changes the name distribution). Handle by
  the rate/recurrence sweep (Stage 2 refinement) and by reporting attacker yield as a
  function of prediction accuracy, not assuming perfect prediction.

**SC2. Every existence-class predicate (existence, age, popularity, not-flagged) is
attacker-satisfiable on schedule; grounding/existence defenses fail by construction.**
- *Evidence:* the simulation — attacker pre-registers predicted names, ages them, seeds
  minimal downloads; measures the fraction of hallucinated-name install requests that pass
  each existence-class check. RAG-grounding's published 40.8%→3.2% is the defender's best
  existence-keyed number and still (a) doesn't touch squatting (a grounded name that the
  attacker registered *is* real) and (b) costs ~16% recall.
- *Weakest point:* "by construction" is definitional for bare existence but *graded*
  predicates (age ≥ 90 days, downloads ≥ 10k) impose real attacker cost — the paper must
  show that cost is *low*, not zero, or the claim overstates. This is exactly what the
  registration-cost-per-predicate-class table (Stage 6) quantifies; if some predicate is
  genuinely expensive to satisfy, report it honestly (it becomes a partial existence-side
  defense, narrowing but not refuting the claim).

**SC3. A provenance-keyed install-time gate raises attacker cost to "compromise a trusted
identity," a qualitatively different and higher bar the recurrence distribution does not
help with.**
- *Evidence:* the trust-tiered gate implementation + its operating point on the same
  simulated attack; the OS-package-manager precedent (Sigstore, npm provenance, PyPI
  trusted publishing) as existence proof the transition is deployable.
- *Weakest point:* provenance has its own failure modes (compromised signing keys,
  self-attested "publishers," typosquatted publisher identities, cold-start for legitimate
  new publishers) — the gate is not magic. Address by measuring usability cost (legitimate
  install-request block rate at each tier) and by scoping the claim to "raises the bar
  from free to identity-compromise," not "unbreakable."

**SC4. The principle generalizes across package indexes, MCP registries, and skill
marketplaces as one ecosystem-design rule.**
- *Evidence:* the simulation instantiated with real metadata from all three registry classes
  (npm/PyPI package metadata; MCP server registry entries; a skill-marketplace schema);
  same attacker, same gate, three substrates.
- *Weakest point:* the three classes differ (packages have download counts and version
  history; MCP servers and skills are newer, sparser, less instrumented), so a gate tuned on
  npm may not transfer. Report per-class operating points rather than one pooled number; the
  generalization claim is "the existence-fails/provenance-holds *structure* recurs," not
  "the same threshold works everywhere."

**Critic:** The whole thing rests on a simulation, and simulations prove what you build into
them — a reviewer's default suspicion. If the adversary and the gate are both authored by us,
"provenance wins" is a foregone conclusion, not a finding. The registry-simulation approach
needs an external validity anchor or it reads as a rigged demo.

**Refined:** Anchor every simulation parameter to a published or observable source and make
the adversary *strong*, not a strawman: (a) attacker name distribution seeded from
2607.12340's actual recurrence data (not invented); (b) predicate costs (registration fee,
aging time, download-faking cost) taken from real npm/PyPI/MCP registry mechanics, cited;
(c) the existence-side defenses implemented at their *published best* operating points
(RAG-grounding at 3.2% block / 16% recall loss — the literature's own numbers), so we are
beating the defense as its authors tuned it, not a weakened version; (d) an adversary
sensitivity sweep (prediction accuracy, budget) so the result is a frontier, not a point.
Where possible, validate one simulation parameter against real registry data (e.g., actual
median package age / download distributions) to show the simulated substrate matches reality.
The finding is credible precisely because the attacker is seeded from measured recurrence and
the baselines are set at their published strength.

---

## Stage 5 — Paper architecture (section skeleton + load-bearing figure/table per section)

Full-paper skeleton (security or SE research track); stance in §1, measured artifacts carry
each section:

- **§1 Introduction — the stance.** Existence is attacker-controlled; provenance is not;
  existence-keyed defenses fail by construction; we demonstrate it and measure the
  provenance alternative across three registry classes. Contributions: (C1) a
  literature-seeded slopsquatting-race simulator; (C2) a registration-cost-per-predicate-
  class analysis proving existence predicates are cheaply satisfiable; (C3) a trust-tiered
  provenance gate with measured security/usability operating points beating four published
  baselines; (C4) the three-registry-class generalization.
  *Artifact:* the **attacker timeline/logic figure** — a horizontal timeline showing the
  attacker satisfying each existence predicate in turn (predict name → register [existence
  ✓] → age [age ✓] → seed downloads [popularity ✓] → stay unflagged [not-flagged ✓]),
  with the provenance gate drawn as the one check that no timeline step satisfies. This
  figure is the position stated as a mechanism.

- **§2 Background & related work.** The three concede-and-claim positionings (Stage 3) +
  the OS-package-manager existence→signature→publisher progression + the MCP/A2A
  governance-gap context.
  *Artifact:* the existence→signature→provenance progression diagram, with each prior work
  (Future Internet MCP registry, 2607.12340 recommendations, systematic review) placed on
  it — showing the field is stalled at existence while OS package managers already moved.

- **§3 Threat model & the attacker-satisfiability argument.** Formalize the existence-class
  predicates; state the defeated-by-construction claim; derive the attacker's pre-
  registration strategy from 2607.12340's recurrence data.
  *Artifact (a load-bearing table):* **predicate-satisfiability / registration-cost-per-
  predicate-class** — rows = predicate classes (existence, age≥N, downloads≥K, not-flagged,
  RAG-grounded/real); columns = attacker cost to satisfy (fee, lead time, effort), lead-time
  required, and whether the recurrence distribution makes it pre-registerable. This is SC2's
  quantification and the answer to the "it's a tautology" critic.

- **§4 The provenance gate.** Trust-tier design (untrusted / signed / attested-publisher /
  reputation-established); install-time decision logic; what each tier costs a legitimate
  publisher (cold-start) and an attacker (identity compromise).
  *Artifact:* the trust-tier decision-flow diagram + the per-tier attacker-cost vs
  legitimate-publisher-friction summary.

- **§5 Experimental setup.** The simulator: three registry substrates seeded with real
  npm/PyPI/MCP metadata; adversary seeded from 2607.12340 recurrence; four baselines at
  published operating points (existence check; RAG-grounding 40.8%→3.2% / ~16% recall;
  self-audit 51–53%; name-reservation) + the provenance gate; metrics; rate/recurrence sweep.

- **§6 Results.** Security (fraction of malicious hallucinated-name installs blocked) ×
  usability (legitimate-install friction / recall loss) for each defense, per registry
  class, across the hallucination-rate sweep.
  *Artifact (headline figure):* the **security/usability operating-point frontier** — each
  defense a point/curve; RAG-grounding at its published (3.2% hallucination, 16% recall
  loss) location; the provenance gate's tiers as a curve dominating the existence-side
  cluster. The single plot that makes "provenance dominates" visible.

- **§7 Discussion + threats.** Provenance failure modes (key compromise, self-attestation,
  publisher typosquatting, cold-start); external validity of the simulation; deployment path
  for operators; the generalization's per-class caveats.

**Critic:** §3's registration-cost table and §5's baselines share a hidden dependency: the
RAG-grounding baseline's published numbers (40.8%→3.2%, 16% recall) were measured on
2607.12340's *own* task, not on our simulated registry-install task — dropping their operating
point onto our frontier plot compares numbers from two different measurement setups, which a
sharp security reviewer will flag as apples-to-oranges.

**Refined:** Re-implement RAG-grounding *inside our simulator* rather than importing its
number as a plotted point, and report both: our re-measured operating point (same task as all
other defenses — the fair comparison) AND a clearly-labeled annotation of the paper's
originally-published number for context. If our re-implementation reproduces ~3.2% block at
~16% recall on comparable inputs, that is a validation of our simulator; if it diverges,
that divergence is itself reportable and we explain it. Every defense must be measured on the
*same* simulated attack for the frontier plot to be honest; published numbers appear only as
annotations, never as plotted competitors.

---

## Stage 6 — Experiment specification (implementable; no trust-annotated snapshot needed)

The key feasibility point (per the course correction): **no trust-annotated registry snapshot
is required** — the registry is *simulated* and seeded with real npm/PyPI/MCP metadata, and
the adversary is seeded from arXiv:2607.12340's published recurrence statistics.

**Component 1 — adversary model (seeded, buildable now):** ingest 2607.12340's hallucinated-
name statistics (rates 36–43%; the 5,669-name set / recurrence structure to the extent
published; supplement with the paper's released artifact if available); build a name-
predictor that samples the names an attacker would pre-register, parameterized by prediction
accuracy (swept). Output: a stream of (hallucinated name, would-be-installed-by-agent)
events with attacker pre-registration decisions.

**Component 2 — simulated registries (three substrates):** populate three registry models
with *real metadata* — npm + PyPI (public metadata dumps: names, ages, download counts,
version history) and MCP server registry entries / a skill-marketplace schema (from public
MCP registry listings). The attacker injects pre-registered malicious entries that satisfy
graded existence predicates (register early → age → seed minimal downloads).

**Component 3 — defenses under test (all re-implemented in-simulator at published strength):**
1. Existence check (name resolves).
2. RAG-grounding (name present in a real index) — re-implemented; validate against the
   paper's 40.8%→3.2% / ~16% recall as a simulator sanity check.
3. Self-audit (LLM re-checks its own recommendation) — at the published 51–53% accuracy.
4. Name-reservation (defender pre-reserves predicted names) — a race against the attacker.
5. **The trust-tiered provenance gate** (untrusted / signed / attested-publisher /
   reputation-established) — install-time decision.

**Component 4 — measurement:** for each defense × registry class × hallucination-rate:
- Security: fraction of malicious pre-registered installs blocked (attack success rate).
- Usability: legitimate-install friction — false-block rate on genuine packages / recall
  loss (RAG's ~16% is the reference); cold-start penalty for new legitimate publishers under
  the provenance gate.
- The **predicate-satisfiability table**: attacker cost (fee, lead time, effort) to satisfy
  each existence predicate class, from real registry mechanics.
- Sweep hallucination/recurrence rate 4.6%–43% (SC-robustness).

**Falsification conditions (printed in the paper):**
1. If some graded existence predicate (e.g., a strict age + real-download + not-flagged
   composite) blocks the seeded attacker at low usability cost comparable to the provenance
   gate → the "existence fails by construction" claim is materially weakened (existence, when
   graded and composed, is a viable defense); report it — it would be an important negative.
2. If the provenance gate's legitimate-publisher friction (cold-start block rate) is so high
   it dominates the security gain → provenance is not a usable improvement as designed; the
   frontier claim fails.
3. If the result flips under the low-rate sweep (4.6%) — attacker yield collapses so far that
   existence checks suffice → the "now" urgency and the rate-robustness claim both weaken.
4. If real registry metadata shows median package age / download bars an attacker cannot
   feasibly clear within a realistic lead time → the pre-registration attack is impractical,
   softening SC2.

**Anticipated reviewer attacks → responses:**
- *"Tautology — of course a registered name exists."* → The finding is the quantified cost
  frontier and the head-to-head beat of RAG-grounding at its published operating point, not
  the existence truism (Stage 1 refinement); §3's cost table is the content.
- *"Rigged simulation."* → Adversary seeded from published recurrence, baselines at published
  best, adversary-strength sweep, one simulator parameter validated against real registry
  data (Stage 4 refinement).
- *"The Future Internet paper already built provenance for MCP."* → Concede the crypto; our
  delta is the impossibility demonstration, the trust-tier operating-point evaluation, and
  the three-class generalization (Stage 3 refinement).
- *"Hallucination rates are dropping (4.6–6.1%), so the threat is receding."* → The sweep
  shows the structure survives at low rates; even at 4.6% the attacker still chooses when to
  satisfy existence predicates (Stage 2 refinement).
- *"Provenance has its own failures (key compromise, self-attestation)."* → Conceded and
  measured (§7); the claim is "raises the bar from free to identity-compromise," not
  unbreakable (SC3).

**Critic:** The plan quietly assumes 2607.12340 released enough of its 5,669-name set /
recurrence structure to seed a realistic predictor. If the paper only reports aggregate rates
(36–43%) without the per-name recurrence data, the adversary's pre-registration accuracy has
to be *assumed*, which reintroduces exactly the "authored to win" problem the simulation was
supposed to escape.

**Refined:** Make adversary realism a graded, reported axis rather than a single assumed
value: (a) first attempt to obtain the actual name/recurrence artifact from 2607.12340
(check its release); (b) if only aggregate rates are public, parameterize attacker
prediction accuracy explicitly and report results across the full 0→1 range, so readers see
the security/usability frontier as a function of how good the attacker's prediction is — the
position holds as long as prediction accuracy is *non-negligible*, which the published
recurrence existence (names recur at all) already establishes; (c) optionally, reproduce a
small recurrence measurement directly (prompt current models for package/tool
recommendations, measure hallucinated-name recurrence across runs) to ground the predictor
in fresh first-party data — a cheap, days-scale addition that also refreshes the possibly-
receding rate. Never report a single attacker-accuracy number as if measured when it is
assumed.

---

## Venue plan (full research track, not position track)

| Window (verify exact dates at M1) | Venue | Fit |
|---|---|---|
| ~Aug/Sep 2026 cycles | **USENIX Security 2027 / IEEE S&P 2027 cycles** | Best fit for the measured security experiment (threat model + defense evaluation + attacker economics) |
| ~Sep 2026 (NDSS 2027 fall cycle) | **NDSS 2027** | Strong fit; systems-security audience for registry/supply-chain work |
| ~Mar–Apr 2027 (ICSE 2028 research track) | **ICSE 2028 / FSE 2027** | Fit if framed as software-supply-chain security (npm/PyPI provenance lineage) |
| ~2027 | **ACM CCS 2027** | Fallback top-tier security venue |
| Rolling | ACM TOPS / IEEE TDSC journals | Safety-net rolling submission |

Strategy: this is the shortest-time-to-build candidate (single primary source already
[READ], no human subjects, no trust-annotated dataset needed — everything is simulated +
seeded), but shortest half-life (pipeline ledger row 2: security cluster publishing monthly).
Build and submit to the **nearest reachable security-conference cycle** with the simulation
complete; do not sit on it. The position-track outlets (ICSE NIER / CACM) from the earlier
plan are dropped per the full-paper decision; the stance survives as §1.

## Time-to-draft / time-to-build estimate

Pipeline verdict: shortest time-to-build of the candidates. Estimate: **~5–7 working weeks**
(simulator + registries ~2 wks; defense re-implementations + adversary seeding ~1.5 wks;
measurement + sweeps ~1 wk; writing ~2 wks). Three milestones (working back from a target
security-conference cycle, exact deadline set at M1):

- **M1 — by Sep 15, 2026: adversary + substrates seeded, threat model frozen.** Obtain
  2607.12340's recurrence artifact (or fix the attacker-accuracy sweep plan); ingest real
  npm/PyPI/MCP metadata into the three registry models; write the §3 threat model and the
  predicate-satisfiability table's cost columns from real registry mechanics; complete the
  npm/PyPI provenance-precedent citation sweep; re-sweep novelty (short half-life — check for
  new provenance/slopsquatting papers).
- **M2 — by Oct 20, 2026: all five defenses measured.** RAG-grounding re-implemented and
  validated against the published 3.2%/16% point; self-audit, existence, name-reservation,
  and the trust-tiered provenance gate implemented; security/usability frontier produced per
  registry class across the rate sweep; falsification conditions checked.
- **M3 — by Nov 30, 2026: full draft submission-ready.** All sections per Stage 5 skeleton
  with the attacker-timeline figure, predicate-cost table, and operating-point frontier
  final; threats/failure-modes section; cold read + internal critic pass; second novelty
  re-sweep; submit to the nearest security cycle.

---

## Hypothesis statement (falsifiable, one sentence)

A trust-tiered install-time provenance gate blocks a literature-seeded slopsquatting adversary
at a strictly better security/usability operating point than every existence-class defense —
existence check, RAG-grounding (published 40.8%→3.2% at ~16% recall), self-audit (51–53%),
and name-reservation — across simulated package, MCP, and skill registries and across
hallucination rates from 4.6% to 43%, because the attacker can satisfy every existence
predicate on schedule but cannot satisfy publisher provenance without compromising a trusted
identity.

## Implementation checklist (build order)

1. Obtain arXiv:2607.12340's recurrence/name artifact (or fix the attacker-accuracy sweep
   fallback); optionally run a fresh first-party recurrence measurement.
2. Ingest real npm + PyPI public metadata (names, ages, download counts, versions) and MCP
   registry / skill-marketplace listings into three registry substrate models.
3. Build the adversary: name-predictor (parameterized accuracy) + pre-registration strategy
   (register → age → seed downloads → stay unflagged).
4. Build the predicate-satisfiability cost model from real registry mechanics (fees, aging,
   download-faking cost) → §3 table.
5. Re-implement the four existence-class baselines in-simulator; validate RAG-grounding
   against the published 3.2%/16% point.
6. Implement the trust-tiered provenance gate (untrusted / signed / attested-publisher /
   reputation-established) with install-time decision logic.
7. Measurement harness: security (malicious-install block rate) × usability (legit friction /
   recall / cold-start) per defense × registry class × hallucination-rate sweep.
8. Produce the operating-point frontier plot, predicate-cost table, attacker-timeline figure.
9. Paper build per Stage 5 skeleton; threats/failure-modes section.

## Verification criteria

- **Publishes (positive):** the provenance gate dominates all four existence-class defenses
  on the security/usability frontier for at least the package-registry substrate, robust
  across the hallucination-rate sweep, with the predicate-cost table showing every existence
  predicate cheaply/predictably satisfiable → full security-track paper (attacker economics +
  measured defense comparison + three-class principle).
- **Publishes (partial/negative but informative):** a composed graded-existence defense holds
  at low cost, OR provenance dominates on packages but not on sparse MCP/skill substrates →
  a scoped paper on *where* existence suffices and where provenance is required (refines the
  principle rather than proving it universally — still a contribution).
- **Kills it:** real registry metadata shows the pre-registration attack is infeasible within
  realistic lead times (age/download bars uncrossable), OR the frontier flips so existence
  checks match provenance at equal usability across all substrates → the "by construction"
  claim is empirically false; retire to the narrower argument that provenance is *a* good
  defense rather than a necessary one.
