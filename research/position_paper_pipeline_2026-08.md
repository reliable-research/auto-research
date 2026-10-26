# Position-Paper Pipeline — 2026-08

Mission (standing, per 2026-08-13 instruction): the main job of this repo's scanning layer is
to find topics that lead the future and package each with enough direction that it can be
**paper-driven quickly — position paper first**, full experimental paper second. A position
paper needs: (1) a sharp, falsifiable-in-principle thesis, (2) evidence that already exists
(no new experiments), (3) an argument space not already occupied in print, (4) a venue with an
open window.

Sources: `trend_scan_2026-08.md` (ACL 4,935 papers 2024–2026; arXiv rolling 6-month agent
miner; SE best-paper digests), `industry_signal_scan_2026-08.md` (5 YouTube channels, ASR;
Part 1 anchored + Part 2 unanchored passes), plus the primary sources already read in full
during B1.6/H1.1 construction. Novelty verdicts below come from a live web sweep (2026-08-13)
for existing position/perspective papers claiming each argument.

Grounding discipline (unchanged): every evidence item below marked [READ] was fetched and
read in full during this repo's earlier topic-sketch work; items marked [RELAY] are still
channel-relayed and must be primary-source-verified before appearing in a submitted draft.

---

## Candidate 1 — "Skill-formation debt is real; the fix must live inside the assistant"

**Thesis.** AI coding assistance measurably erodes human skill formation, and the field's
default responses (usage bans, AI-free assessment gates) treat the symptom. Because the
erosion is carried by *identifiable interaction patterns* — not by AI use per se (3 of Shen &
Tamkin's 6 patterns preserve 65–86% quiz performance) — the correct intervention layer is the
assistant itself: real-time detection of erosion-prone patterns plus just-in-time redirection.
"Don't restrict access; instrument the interaction."

**Evidence already in hand (no new experiments needed):**
- [READ] Shen & Tamkin, arXiv:2601.20245 — n=52 RCT, 50% vs 67% quiz (d=0.738, p=0.01),
  six-pattern taxonomy splitting eroding vs preserving usage.
- [READ] Kosmyna et al., arXiv:2506.08872 — EEG, weakest connectivity + lowest ownership in
  the LLM-assisted condition (different task, instrument, population).
- [READ] Yao, arXiv:2606.06253 — observable "AI-prompt signature" in competitive-programming
  submission behavior; AI-disabled gates filter it.
- [READ] Aouad/Lykouris/Zhong, arXiv:2605.11350 — formal conditions for skill polarization
  under heterogeneous AI literacy (the "why it compounds" theory).
- [web-search-confirmed only] Cao & Huang, CSCW2 2022 — real-time reliance proxy from gaze;
  needs full read before citing.

**Argument skeleton.** §1 the effect is proven, stop re-proving it → §2 restriction-based
responses fail (Yao's data shows gates only *filter*, they don't *teach*; polarization theory
says bans widen the gap) → §3 the pattern taxonomy shows AI use is not monolithic — the
erosion is behavioral and therefore detectable → §4 the missing layer: session-time
classification + just-in-time intervention (H1.1's design as the concrete instantiation) →
§5 what the field must build/measure: precision-at-prefix-length as a standard metric,
intervention RCTs as the standard of evidence, assistant-side telemetry standards.

**Assets:** full N0–N12 digest already exists (`topics/H1.1_.../`). Time-to-draft: **short —
this is mostly a rewrite of existing material into argument form.**

**Novelty verdict (web sweep 2026-08-13): PARTIALLY CLAIMED — the specific argument is
open.** Occupied: "assistants must be redesigned to preserve learning" as *design
principles* (closest competitor: "Agents That Teach", arXiv:2607.06101, which coins
"Knowledge Debt" and proposes SHIELD — but explicitly does NOT propose detection);
deskilling-as-overlooked-safety-risk (FAccT'26 "Brainrot", arXiv:2605.03512); design-time
friction (CHI'26 AlgoGPT); metacognitive scaffolds for novices (arXiv:2602.20206).
**Unclaimed: the closed-loop claim** — real-time behavioral detection of the RCT-validated
erosion patterns as *tailoring variables for a JITAI-style loop inside the assistant*
(JITAI exists only in mHealth/education, never imported to coding assistants). Sharpest
formulation from the sweep: "skill erosion is detectable at interaction time; blanket
friction pays a constant productivity tax and restriction is unenforceable; the assistant
must classify the live pattern and intervene only at erosion-prone moments — skill
preservation as targeted runtime behavior, not a static design property." Must cite and
position against 2607.06101 explicitly.

---

## Candidate 2 — "Green tests are not acceptance" (B1.7 seed)

**Thesis.** The binding oracle gap for coding agents has moved: frontier agents now saturate
test-pass signals while failing *acceptance* — human merge decisions, static/design analysis,
post-merge defect telemetry — at rates too high to ignore. Benchmarks and RL reward design
that optimize test-pass are optimizing a defeated proxy; evaluation must move to
acceptance-layer signals that already exist in production telemetry.

**Evidence in hand:**
- [RELAY] METR: agent PRs merged at ~half the human rate despite passing the same tests.
- [RELAY] ReactBench: 8,415 runs / 51 repos; 60.8% of Fix tasks green-on-tests but fail deep
  static analysis; more reasoning effort *reduced* this score.
- [RELAY] Faros AI telemetry (4,000 teams): 31.3% of AI PRs merged with zero review; defect
  rate 9%→54% on those.
- [corpus] SE best-paper metamorphic-oracle lineage (JEST/EDEFuzz/MetaQA) as the
  methodological escape hatch when no acceptance oracle exists.
- Repo's own B1/T5 families supply the mechanism vocabulary (verifier insufficiency,
  design-constraint blindness of test suites — T5.2 is literally "why tests cannot see
  design").

**Argument skeleton.** §1 three independent production-scale measurements of the same gap →
§2 why the gap is structural, not a maturity artifact (tests encode reachable behavior, not
design intent; RL against test-pass Goodharts the proxy — connect to RLVR crystallization
trend, 0→66 ACL papers) → §3 the acceptance layer is already instrumented in industry
(merge decisions, static analysis, defect telemetry) — the field is ignoring free ground
truth → §4 concrete proposal: acceptance-calibrated evaluation + reward shaping; metamorphic
relations where acceptance signals are private → §5 predictions that would falsify the
position.

**Blocker before submission:** all three headline numbers are [RELAY] — the METR report,
ReactBench paper/repo, and Faros study must each be read in full (same discipline as
B1.6/H1.1). The web sweep could NOT independently locate papers matching the 60.8% and
31.3% figures — nearest published analogues are arXiv:2606.18168 (80.2% of agent-PR test
files carry weak/no oracle signals) and arXiv:2601.00753 (28.3% immediate merges) — so the
verification pass is not optional. Time-to-draft: **medium (hardest verification burden +
most crowded argument space of the three).**

**Novelty verdict (web sweep 2026-08-13): PARTIALLY CLAIMED — most crowded of the three,
but the prescriptive core is open.** Occupied: "test-pass is an insufficient oracle"
(Verification Horizon arXiv:2606.26300 — closest on the reward side, framed as endless
verifier co-evolution; UTBoost 2506.09289's 31% lucky passes; All-Smoke-No-Alarm
2606.18168), "benchmarks misaligned" (2606.17799), "humans missing from agent research"
(Wang et al. position, which *warns against* reducing humans to reward models — a direct
foil). **Unclaimed:** making the merge/acceptance gap itself the binding oracle gap,
grounded in PR-merge field data, with the prescription that both evaluation and RL reward
be built from a **review-adjusted acceptance oracle** (raw merge is itself noisy/hackable:
35.7% of rejections are non-agentic per 2605.22534; zero-review merges have exploding
defect rates). Delta to state against 2606.26300: "they say no silver bullet, co-evolve
verifiers; we say there is a natural terminal oracle — reviewed acceptance — and it is
already logged at platform scale."

**Decay note (2026-08-13, from the ZC3 draft review):** a method twin surfaced —
arXiv:2604.05955 already measures "green-but-design-violating" outcomes on
SWE-bench-aligned issues. Any "first measurement of the merge gap" reading is now
defeated; the surviving delta is the **cross-layer oracle-fidelity comparison** (tests vs
design checkers vs review-adjusted acceptance, field-validated on platform logs) and the
prescriptive reward-substrate claim. The pipeline draft (`positions/C3_acceptance_oracle/
autodiscussion_draft_review.md`) has the full ledger; it also failed to cite 2606.26300 —
fix before any submission.

---

## Candidate 3 — "Registries must gate on provenance, not existence" (B1.6 companion)

**Thesis.** Because LLMs hallucinate plausible tool/skill/package names at stable,
predictable rates (36–43%), and hallucinated names recur predictably enough to pre-register
(slopsquatting), *existence checking is defeated by construction* — the attacker makes the
name exist. Every agent-facing registry (MCP servers, skill marketplaces, package indexes)
must therefore move trust decisions to install-time publisher provenance, the way OS package
managers did a decade ago.

**Evidence in hand:**
- [READ] arXiv:2607.12340 — 36.0/36.9/43.1% hallucination rates across settings; 5,669
  distinct hallucinated names; self-audit only 51–53% accurate; RAG defense cuts
  hallucination 40.8%→3.2% but costs ~16% recall — i.e., the best published defense already
  trades away utility and still doesn't address squatting.
- [corpus] trend scan §2.1–2.2: MCP/A2A governance-gap papers (2606.31498, 2607.02116) as
  independent evidence that protocol-layer trust is unspecified.
- Prior ecosystem precedent: npm/PyPI typosquatting literature (needs a citation sweep, well
  established).

**Argument skeleton.** §1 hallucinated recommendation is a measured, stable phenomenon →
§2 the defense the literature proposes (existence/RAG grounding) is defeated by adversarial
registration — security argument, not an accuracy argument → §3 lesson transfer from package
managers: existence→signature→publisher-trust progression → §4 concrete gate design (B1.6's
trust-tier proposal) and the recall-loss economics vs the paper's published operating points
→ §5 governance implications for MCP/marketplace operators.

**Assets:** full B1.6 digest exists; the one primary source is already read. Time-to-draft:
**shortest of all candidates.**

**Novelty verdict (web sweep 2026-08-13): PARTIALLY CLAIMED — the most open room of all
six theses.** Occupied: MCP-specific cryptographic-provenance architecture (Future Internet
18(5):243, Sigstore-based); name reservations as a closing recommendation (2607.12340
itself); provenance attestations as one list item in a slopsquatting systematic review
(rs.3.rs-8007192 — which *also endorses existence validation*, making it a direct foil);
threat taxonomies (2604.02837). Useful new datum: package-level hallucination has
compressed to 4.6–6.1% in the 2026 frontier cohort (arXiv:2605.17062) yet remains
adversary-economical. **Unclaimed: the logical core as a position** — "existence is
attacker-controlled; provenance is not": stable, repeatable hallucination means the
attacker chooses when to make any existence/age/popularity predicate true, so
existence-keyed defenses fail *by construction, not by implementation* — generalized across
all three registry classes (package indexes, MCP registries, skill marketplaces) as one
ecosystem-design principle. **Note the interaction with the portfolio audit:** experimental
B1.6 is RETIRED (delta = implementing Yuan et al.'s stated future work; trust-annotated
registry data doesn't exist) — but that objection doesn't touch the position form, which
needs no new dataset. This is now the *only* live continuation of B1.6.

---

## Candidate 4 — "Served models need behavioral attestation" (B3.6 seed)

**Thesis.** Benchmark results and served behavior are decoupling: vendors can (and
documentedly do) serve checkpoints that differ from what was evaluated (LMArena Llama-4
special-variant, #2→#32 on retest; undisclosed tier-dependent behavior changes). Since
disclosure is voluntary and incidents keep occurring, the field needs *external behavioral
attestation* — black-box statistical fingerprinting of which model actually served a request
— as both a consumer-protection and a science-reproducibility layer.

**Evidence in hand:** both incidents [RELAY] — need primary verification (LMArena's own
statements; the system-card passage). Repo's B3 family supplies the probe-set machinery
(B3.1/B3.3 are directly reusable as the technical program).

**Argument skeleton.** §1 documented substitution incidents → §2 why this breaks science
(every eval paper silently assumes checkpoint identity) and markets (paying for tier X,
served tier Y) → §3 attestation is feasible: drift-detection literature + B3-style probe
sets → §4 proposal: attestation protocol, who runs it, incentive analysis → §5 objections
(vendor legitimate A/B testing, safety patches) and the disclosure standard that resolves
them.

Time-to-draft: **medium** (two primary verifications + probe-feasibility argument).
Positioning strength: the repo's own ocean map names external audit as the defensible
academic edge — this is that argument in position-paper form.

**Novelty verdict (web sweep 2026-08-13): PARTIALLY CLAIMED — but the best open lane of the
non-H1 candidates.** The mechanism layer is published: substitution auditing incl. "TEE
attestation is the only viable path" (arXiv:2504.04715), governance-of-silent-updates
(arXiv:2604.27789), rank-based API auditing (2506.06975), one-token fingerprinting
(2607.10252), logprob tracking (2512.03816) — and crucially, behavioral fingerprints are
shown SPOOFABLE by a cheating provider (arXiv:2606.16100, the tier-downgrade scenario
directly). **Unclaimed synthesis position:** "every LLM API response should carry a
verifiable model-identity attestation — a TLS-certificate-for-model-serving; behavioral
fingerprinting can't be the layer (spoofable), TEEs alone don't create disclosure norms;
unattested benchmark/paper results should be inadmissible." The delta over
2504.04715+2604.27789 must be argued explicitly. Consequence for B3.6: the *detection*
methods space is crowded — the open ground is the protocol/norms synthesis, and any B3.6
experimental work should target the spoofing-resistance gap, not another fingerprint.

**2026-08-15 pipeline signal — motivation gap is load-bearing.** The AutoDiscussion
critic (opus-5) could not approve C4's motivation step across two independent rooms: the
recurring major was that the problem-side evidence base is two incidents, both relayed
rather than primary-verified. We stopped chasing a clean gate (room closed 6/6 with the
major standing). Treat this as convergent with the draft review's position-deflation
finding: **the two primary verifications (LMArena's own retest statement; the
tier-behavior system-card passage) are now a hard prerequisite** — if primary sources
can't be pinned down, C4 demotes from "best open lane" to monitor tier, because the
thesis would rest entirely on secondhand incident reports.

---

## Candidate 5 (monitor tier) — weaker as standalone positions

- **"Multi-agent parallelism is an exploit amplifier"** — **TAKEN, retired as a position.**
  The web sweep found the primary source of the relayed stat: arXiv:2606.15008 (OpenClaw
  security engineering; 0.24 single-agent vs 0.86 seven-agent compromise rate, 3.58x) — and
  it already draws the design conclusion; the untrusted-by-default norm is codified in OWASP
  ASI07, Meta's "Rule of Two", arXiv:2506.08837, and the 24-author agenda arXiv:2505.02077.
  Remaining narrow openings (mandatory reported amplification-factor metric; premature-A2A-
  standardization argument) are thin — keep only as citable context for B1/B5 topics. The
  found primary source UPGRADES the industry-scan §4 item from [RELAY] to verifiable.
- **"Test-time compute has crossed into negative marginal ROI"** — **PARTIALLY CLAIMED and
  closing fast; do not build as standalone.** Overthinking/inverse-scaling is thoroughly
  published (arXiv:2604.10739 — which already proposes cost-aware evaluation; 2507.14417;
  2502.08235; survey 2503.16419; ICML 2026 "Meta Intelligence" position claims the
  allocation-as-design-principle frame). Only unclaimed sliver: mandate compute-normalized
  accuracy curves + marginal-return crossover reporting in releases ("a capability claim
  made only at unbounded test-time compute is an unsubstantiated claim") — best folded into
  B4 topics as framing, not a separate paper. Caveat from sweep: the relayed "GPT-5.6 gets
  worse at Max tier" number was NOT independently verified — do not cite without finding the
  actual release charts.
- **"Interoperability protocols cannot express governance"** — the argument already exists
  in print (2606.31498 *is* that position paper); the open move is the empirical follow-up,
  not another position.
- **H1-family expansions** (companion-app dependency as a measurable harm category;
  RLHF-label production conditions as a data-quality confound) — real, but each needs a
  primary-source verification pass before even a position draft is honest.

---

## Novelty ledger (novelty-auditor discipline, defensive mode, t_claim = now)

Category bar applied: position/synthesis — novelty must live in a **named coupling/argument
delta against a named occupant**, never in the act of taking a stance. Framing firewall
applied: each claim restated with framing verbs stripped before scoring.

| # | Claim (stripped) | Nearest prior work | Operational delta | Load-bearing? | Stance |
|---|---|---|---|---|---|
| 1 | Erosion-pattern classification at session time can serve as the tailoring variable of a JITAI-style loop inside a coding assistant | Agents That Teach (2607.06101): design principles, explicitly no detection; JITAI lit: has the loop, wrong domain, no validated tailoring variables | The coupling itself: RCT-validated pattern taxonomy (2601.20245) as JITAI tailoring variables; detectability supported by Yao 2606.06253's observable signature | Yes — the whole prescription follows from detectability | 🟢 on the coupling row; 🟡 on the "deskilling matters" row (occupied by Brainrot 2605.03512, 2607.06101) |
| 2 | Any existence/age/popularity predicate on registry names is attacker-satisfiable on schedule, so provenance must be the install-time gating contract across package indexes, MCP registries, and skill marketplaces | Trustworthy MCP Registry (Future Internet 18(5):243): provenance architecture, MCP-only, no impossibility argument; slopsquatting systematic review: endorses existence validation (direct foil); 2607.12340: name reservations as closing recommendation | The defeated-by-construction argument + the three-registry-class generalization | Yes — the argument is what makes the prescription non-optional | 🟢 on the argument row; 🟡 on the mechanism row (Sigstore-style provenance already proposed for MCP). **Short half-life** — security cluster is publishing monthly |
| 3 | Review-adjusted acceptance (merge conditioned on genuine review + post-merge survival) should replace test-pass as both headline metric and RL reward substrate | Verification Horizon (2606.26300): "users are the most faithful verifiers," co-evolution framing, no acceptance-gap data, no oracle construction; Wang et al. position: warns against humans-as-reward-models (counter-foil) | Terminal-oracle claim vs no-silver-bullet + the review-adjustment correction (raw merge is noisy per 2605.22534) + platform logs as reward substrate | Yes, but thinnest of the three — 2606.26300 is one paragraph away on the reward side | 🟡 somewhat-novel; verdict capped until the METR/ReactBench/Faros numbers are primary-verified (sweep could not locate them) |

## Venue runway (confirmed sweeps, 2026-08-13)

| Window | Venue | Fit |
|---|---|---|
| Sep 18/25, 2026 | ICLR 2027 main (no position track) | Experimental Tier-1 topics, not positions |
| Oct 12, 2026 | ARR cycle → NAACL/COLING 2027 | Only if NLP-framed |
| **Oct 23, 2026** | **ICSE 2027 NIER** (confirmed) | Best near-term slot for Candidates 2 and 3 (4+1 pp, thought-provoking reflections in scope) |
| **Oct 27 / Nov 3, 2026** | **FAccT 2027** (confirmed) | Best near-term slot for Candidate 1 (human-impact scope) |
| ~Dec 2026 | ICLR blogposts (est.) | Low-cost trial balloon for any candidate |
| ~Jan 2027 | **ICML position track** (est., pattern-stable) + FSE IVR (est.) | Flagship target for Candidate 1; FSE IVR for Candidates 2/3 |
| Rolling | CACM Opinion (≤5pp) | Candidate 2's fastest possible outlet |
| ~May 2027 | NeurIPS position (est.), AIES (est.) | Fallback windows |

Key sweep finding: the ICML-style position space around **coding agents × skill erosion ×
evaluation is unoccupied** — deskilling has empirical papers and a FAccT framing paper, but
no "Position:" paper coupling detection to intervention. Saturated spaces to avoid as
headline theses: "benchmarks are broken" (15+ occupants), generic multi-agent security,
overthinking.

## Ranked recommendation

1. **Candidate 1 — skill-formation debt / closed-loop intervention.** Rank 1 on every
   axis: all five grounding papers already [READ], the coupling row is genuinely open, the
   flagship window (ICML position, ~Jan 2027) matches, and FAccT (Nov 3) is a confirmed
   earlier shot. It is also the position-form of the portfolio's KEEP-TOP H1.1, so one
   evidence base feeds two deliverables. **Action order: draft now; FAccT abstract Oct 27.**
2. **Candidate 2 — provenance-not-existence gating.** Most open argument room and shortest
   time-to-draft (single primary source, already read), but shortest half-life. Ship to
   ICSE NIER (Oct 23) or CACM (rolling) fast; do not sit on it. Position explicitly
   against the systematic review's existence-validation endorsement and concede the MCP
   Sigstore architecture (concede-and-claim).
3. **Candidate 3 — review-adjusted acceptance oracle.** Highest strategic value (it is the
   argumentative umbrella over Tier-1 experimental topics B1.2/T5.1/T5.2) but the most
   crowded space and a hard evidence blocker: the 60.8%/31.3% figures failed independent
   location. **Gate: primary-verify METR/ReactBench/Faros first**; then ICSE NIER or FSE
   IVR (~Jan 2027), positioned against 2606.26300 by name.
4. **Candidate 4 — behavioral attestation.** Open only as the synthesis/standardization
   position ("TLS certificate for model serving"); the detection-methods space is
   occupied and fingerprints are proven spoofable. Draft after 1–3, or fold into B3.3's
   eventual paper as its discussion section.
5. **Dropped as positions:** multi-agent amplification (TAKEN — 2606.15008 + OWASP/Meta
   norms), negative test-time-compute ROI (occupied; fold the sliver into B4 framing).

Standing rule going forward (also adopted in `portfolio_2026-08.md`): **no position draft
starts without a novelty ledger against named occupants, and no relayed statistic enters a
draft without primary-source verification** — this cycle's sweeps found one relayed stat's
real source (0.24→0.86, arXiv:2606.15008) and failed to find two others (60.8%, 31.3%),
which is exactly the difference between a citable claim and a liability.
