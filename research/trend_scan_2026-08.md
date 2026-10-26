# Cross-Corpus Trend Scan — 2026-08

Source: refreshed local caches/indices in `acl_corpus` (ACL Anthology 2024–2026,
4,935 papers), `arxiv_corpus` (rolling 6-month agent/LLM/reasoning arXiv miner,
refreshed 2026-08-10, 1,545 recent vs 1,111 prior-window papers), `SE_corpus`
(ICSE/FSE best/distinguished papers 2021–2025, 63 digests), and a status check
on two in-progress side projects (`openview_corpus/TasteGap`, `secondbrain/VaultGym`).
Compared against this repo's existing thesis in `README.md`/`goal.md`, which was
built from the older, general (non-agent-specific) `openview_corpus/ideas.jsonl`
11,683-idea corpus.

## 1. Cross-corpus convergence — signals independently confirmed by 2+ sources

These are the highest-confidence trends because three differently-scoped,
independently-built corpora agree:

- **RL-with-verifiable-rewards (RLVR) is a discrete, brand-new category, not just
  a rising tag.** ACL: 0 papers in 2024, 1 in 2025, 66 in 2026. This matches and
  sharpens this repo's own thesis (`README.md`'s claim that verifier/reward-hacking
  was 14.1% of 2025 LLM proposals) — the newer signal shows it crystallizing into
  a named subfield in the last ~8 months, not just a rising share. arXiv shows
  GRPO/RLVR as already "crowded/mature" (flat 4.5% vs 3.3%, but off a higher base) —
  i.e. the topic went from emerging to competitive within one arXiv 6-month window.
- **RAG/retrieval is fading, being displaced by "agent memory" framing.** arXiv:
  RAG keyword-rate 2.8% vs 6.0% prior window (ratio 0.47); ACL: RAG share
  plateaus 2025→2026 (6.6%→6.4%) after rising 2024→2025. Confirms this repo's own
  flag of RAG/evidence as a "largest crowded area" — the fresh signal says it's
  past its peak, with authors reframing the same substrate as agent memory instead.
- **Prompting/context-engineering framing is fading.** ACL: prompt/prompting
  share falls 19.2%→13.3% (2024→2026). arXiv: the term "context engineering"
  (5 hits in the prior window) is entirely absent from the recent window. Both
  independently suggest the field is re-labeling prompting-era work as
  agent/RL-training work rather than continuing to publish it as prompting.
- **LLM-agent reliability/failure-attribution is becoming its own object of study,
  not just a subplot inside agent papers.** SE_corpus: hallucination-detection,
  data-quality-for-eval, and "can LLMs replace annotators" appear for the first
  time as SE best-paper topics in 2025 (0 before). arXiv: agent trajectory failure
  attribution is both rising and already the single largest tag (53.8% of recent
  papers touch it in some form). This directly validates this repo's #1 and #2
  near-term priorities (planning/execution failure attribution; verifier/test-oracle
  adequacy) as still the right bet, not a stale read.
- **"Reasoning" and "agent" are now near-universal framings, not niche tags.**
  ACL: reasoning 17.6%→39.4% of all papers (2024→2026); agent/agentic 5.9%→20.4%.
  This is less a specific research opportunity than a base-rate warning: any new
  topic sketch that just says "reasoning agent X" now competes in the single most
  crowded framing in the corpus and needs a sharper hook to stand out.

## 2. New clusters not yet represented in the 47-topic map

These showed up in the fresh scans with little or no baseline in the prior
window, and don't cleanly map onto any existing B1–B6/T3/T5 topic:

1. **Agent interoperability protocol governance (MCP/A2A/ACP).** arXiv, zero
   baseline in the prior 6 months: *"Governance Gaps in Agent Interoperability
   Protocols: What MCP, A2A, and ACP Cannot Express"* (2606.31498),
   *ContextNest: Verifiable Context Governance* (2607.02116). This is the
   concrete, mechanically-checkable version of the "capability-controlled
   runtime" route this repo's own README already names as a candidate direction
   but never turned into a B/T topic — tool visibility vs. authority, except now
   grounded in real, versioned, testable protocol specs instead of a generic
   framing. Ground truth is mechanical: does an agent's behavior violate what
   the protocol spec can/cannot express.

2. **Hallucinated skill/tool recommendation.** arXiv, no prior-window analog:
   *"Skills That Don't Exist: A Large-Scale Study of Hallucinated Skill
   Recommendation in LLM Agents"* (2607.12340). This reframes hallucination as
   an agent recommending a non-existent tool/skill mid-task — a distinct,
   narrowly falsifiable failure mode (tool exists in the registry or it doesn't)
   that fits this repo's own selection filter (mechanical truth, binding
   constraint, no incumbent lockout) about as cleanly as any B1/B2 topic
   currently in the map.

3. **Self-evolving skill-library agents.** arXiv, rising 1.56x (24.3% vs 15.6%
   of papers touch skill-library/discovery/evolution framing): *ASPIRE*
   (2607.00272), *Learning Globally Reusable Skills for Coding Agents*
   (2608.06153). Adjacent to but distinct from B2 (failure attribution) and T5
   (design-constraint compliance) — this is about skill acquisition/reuse
   economics, not diagnosis. No existing topic in the map targets it directly.

4. **Multi-agent adversarial robustness — memory poisoning, Byzantine-tolerant
   collaborative RAG, connectivity attacks.** arXiv, small but essentially zero
   baseline: *Forensic Trajectory Signatures for Agent Memory Poisoning
   Detection* (2606.30566), *Combating Knowledge Corruption in Agent Systems*
   (2608.04366). This is a genuinely different angle from B5's economic
   bargaining/manipulation family — it's adversarial-input robustness with a
   cleaner ground truth (does a poisoned claim get accepted despite a defense
   mechanism) rather than surplus-transfer economics.

5. **Coding-agent serving economics.** arXiv, rising 2.6x: *TraceLab:
   Characterizing Coding Agent Workloads for LLM Serving* (2606.30560),
   *Inference Economics of Enterprise Coding Agents* (2607.13080). This is the
   systems/cost side of B4's budget-aware test-time-compute family — currently
   B4 frames budget as a verification-allocation problem; this cluster frames it
   as a serving-infrastructure problem, which is a different (and possibly more
   defensible, since it needs real traces rather than a clean lab setup) angle.

## 3. SE-specific corroboration and one reusable methodological pattern

- SE best-paper topics confirm the pivot toward LLM-centric SE research
  specifically in 2025: LLM-for-code-gen (0→3), LLM-for-proof-synthesis (0→2),
  LLM-agents-for-SE (0→1), and LLM-reliability-as-object-of-study (0→3) all
  appear for the first time in 2025, while non-LLM neural ML4SE tools (TOGA-style,
  BERT-traceability, KG-embedding) and human-factors/community studies both
  collapse to near-zero after being steady 2021–2024.
- Recurring reviewer-rewarded pattern worth reusing directly: **metamorphic/
  differential relations as an oracle substitute when ground truth doesn't
  exist** — used across `JEST` (2021), `EDEFuzz` (2024), and `MetaQA` (2025,
  hallucination detection via metamorphic relations). Any new B1-family topic
  proposing a verifier for agent/coding tasks without a clean execution oracle
  should consider a metamorphic-relation design instead of an LLM-judge design —
  it's the specific pattern SE program committees have repeatedly rewarded.

## 4. Two side projects that are further along than their own docs admit

- **TasteGap→ICML expansion** (`openview_corpus/`): `ICML_EXPANSION_PLAN.md` is
  dated Jul 13 and describes Phase 1 as not yet run, but the substrate rebuild,
  idea generation (516 items via gpt-5.4-mini), and taste labeling (2,208 items)
  actually completed Jul 14 with 0 errors, and a further enrichment pass touched
  `ml_venue_papers_2023_2025_enriched.jsonl` as recently as Aug 10 — three weeks
  after the plan's own last audit. **Next action**: read the labeling output
  against the original taxonomy to check whether NLP/Security show the same
  bridge+synthesis skew as ML/Nature-Communications did, then update the plan
  doc to reflect actual completion before deciding on the causal (Phase 3) or
  mitigation (Phase 4) axis. This is directly relevant to this repo's own
  "execution-grounded ideation" route in the README.
- **VaultGym** (`secondbrain/`): a working experiment harness (hooks, ledger,
  synthetic stream generator, 3 policy arms, 19 passing smoke tests) with a live
  pilot that ran three arms through checkpoint t_005, but all activity is dated
  Jul 4–5 — over five weeks stale with uncommitted changes sitting in the working
  tree. **Next action**: verify the hook/CLI assumptions in `revised_v1.md` §5
  against the installed Claude Code version, then extend the live3 pilot from
  t_005 to the full t={5,15,25} exit criteria — that's the single gate between
  the already-built harness and a reportable result.

## 5. Bottom line — where the near-term opening actually is

The existing near-term ranking in `README.md` (planning/execution failure
attribution, then verifier/test-oracle adequacy) holds up under fresh signal and
should stay rank 1–2. The clearest **new** addition the fresh scan surfaces is
**hallucinated skill/tool recommendation** (§2.2) — it satisfies the repo's own
three-part filter (mechanical truth via registry lookup, binding constraint
because it breaks execution, no incumbent lockout because the literature is a
single paper old) better than most already-mapped topics, and it slots naturally
next to B1/B2 as a new sub-topic rather than requiring a new family. Agent
protocol governance (§2.1) is the second-strongest new candidate but needs a
concrete protocol version and spec to anchor mechanical ground truth before it's
paper-shaped.

## 6. 2026-08-13 update — occupancy sweeps on the §2 clusters, and two fresh signals

Four parallel literature sweeps (each 7–8 targeted searches over ~Mar–Aug 2026)
pressure-tested the §2 clusters that had not yet been converted into topics.
Headline: **every original cluster core is now CROWDED or TAKEN — the six-month
lag between "cluster appears in a corpus scan" and "cluster is occupied" has
effectively collapsed to one quarter.** Each sweep, however, surfaced a sharper
successor angle; the four survivors were promoted into the topic map (B7.1,
B7.2, B8.1, B4.6 — see `portfolio_2026-08.md` §Tier-2 addendum).

| §2 cluster | Verdict on original angle | Occupier / nearest twin | Promoted survivor |
|---|---|---|---|
| Protocol governance (§2.1) | CROWDED; runtime-conformance seam narrow, months-scale clock | AgentRFC 2603.23801 (spec→TLA+ conformance), 2606.28679 (visibility-vs-authority at framework level), HCP 2606.29073 | **B8.1** spec-drift differential conformance across MCP/A2A versions (divergence windows, authority→visibility downgrades; wire-level ground truth) |
| Skill-library economics (§2.3) | CROWDED, diagnostics core TAKEN (5 papers May–Jul + 2 surveys naming the payback gap) | Library Drift 2605.19576; Skill-Drift-as-Contract-Violation 2605.10990 (880-pair benchmark) | **B7.1** skill-library depreciation across backbone upgrades — port/prune/relearn decision with per-skill depreciation curves (strongest of the four) |
| Memory poisoning (§2.4) | CROWDED, core TAKEN | MemSecBench 2607.27080 (checkpoint persistence + repair); 2605.08442 (6 defenses × 21 models) | **B7.2** poison half-life survival analysis; hypothesis: utility-improving consolidation *increases* half-life via laundering (2605.16746) |
| Serving economics (§2.5) | Characterization TAKEN twice (public + production scale); scheduling/KV each 5+ papers deep | TraceLab 2606.30560 (public traces); Copilot-scale 2608.00101; Cost-Aware Speculative Execution 2606.07846 | **B4.6** verification-aware serving economics on public TraceLab traces ($/resolved-task at matched resolve rate) |

Two additional signals from the general fresh sweep (not from the four agents):

- **Procedural-compliance verification is crystallizing as a cluster**: AgentLTL
  (2607.02599, FO-LTL deterministic compliance scores over traces, gate + dense
  reward), MANTRA (2605.06334, SMT-validated compliance benchmarks), COVENANT
  (2607.25400, workflow compilation for aligned execution). **Not a scoop of
  T5.1/T5.2** — those verify the *artifact* (does the patch violate mined design
  constraints while passing tests); this cluster verifies the *trace* (did the
  tool-call sequence follow procedural rules). Different estimand, but real decay
  pressure on the "tests-pass-isn't-enough" stance: T5 positioning should now
  concede this cluster by name and claim the artifact-level estimand explicitly.
  Also context for C3 (acceptance oracle): the trace side of its stance is being
  colonized; the artifact/acceptance side remains open.
- **Memory staleness/forgetting is a named subfield now**: Memora/FAMA
  (2604.20006, metric penalizing reliance on invalidated memory), control-plane
  forgetting study (2606.15903, 13 configurations), TOKI bitemporal
  contradiction algebra (2606.06240), typed-memory provenance-role work
  (2605.25869). Conversational/fact memory staleness is occupied; the
  *procedural/skill* staleness axis is what B7.1 claims, and the *adversarial*
  persistence axis is what B7.2 claims — both deliberately avoid the occupied
  center.

Process note: §5's six-month-old advice ("protocol governance needs a concrete
spec anchor before it's paper-shaped") aged badly in five weeks — by the time an
anchor existed, three groups had built on it. The operational lesson for this
repo: convert corpus-scan clusters into scoop-checked topics within **one
window**, or log them as monitored, never as "later".
