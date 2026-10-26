# Archetype verbs: what the method's main verb gives away

The source paper's mechanism analysis (Section 4.5) rewrote thousands of
motivation/method pairs into one-sentence archetypes, clustered them, and
counted the main verb of each. The split below is sharp enough to use as a
fast surface check before doing the full two-axis classification.

## LLM-heavy verbs (found disproportionately in model outputs)

| Verb | Model share of that operation | Human share |
|---|---|---|
| integrate | 34.2% of all model operations (only 2.35% of human ones) | 2.35% |
| unify | 8.2% | 1.9% |
| design (as in "design a framework that...") | 1.5% | 0.3% |
| merge | elevated (log-odds 1.37 vs. human) | — |
| adapt | elevated (log-odds 1.36 vs. human) | — |

Other words that function the same way even though the paper didn't track
them as a named cluster: *combine, leverage, bring together, bridge,
reconcile, synergize, jointly consider, holistically address*.

These verbs aren't individually forbidden — they just correlate strongly
with the generic "connect A and B" template. If one of these is the *main*
verb of the method sentence (the thing the reader remembers), treat it as a
flag.

## Human-heavy verbs (found disproportionately in published human ideas)

| Verb | Human share of that operation | Model share |
|---|---|---|
| replace | 9.13% of human operations | 0.92% |
| decouple | 2.33% | 0.21% |
| formalize | human-majority cluster | minority |
| separate | human-majority cluster | minority |
| reinterpret | human-majority cluster | minority |

Two clusters were almost entirely absent from LLM outputs: **replace**
(83.3% human-authored) and **decouple** (85.4% human-authored). Papers built
around these verbs also scored *higher* on bottleneck specificity (2.61,
2.70) and *lower* on boilerplate (0.60, 0.51) than integrate/unify-led
papers — the verb choice and the specificity finding reinforce each other.

Other words in the same family: *isolate, disentangle, localize, swap out,
strip out, ablate, invert, recast, expose*.

## Why this happens (for context, not required reading during an audit)

The paper's concept-enrichment analysis found LLM-favored ideas cluster
around a handful of high-frequency technical motifs (multi-omics
integration, diffusion policy, multimodal generation, in-context learning,
test-time adaptation) and then apply a safe connecting verb to whichever
motif is nearby. Human-favored ideas instead named a narrower, more local
target — a trajectory, a ligand interaction, a tokenization choice, an
equivariance property — and did something specific to *that* thing. The
practical takeaway: specificity of the *target*, not just the verb, is what
separates the two populations. A precise verb applied to a vague target
doesn't fix the problem.

## Reframing patterns

When a 🔴 or multiple 🟡 flags fire, don't just swap the verb — find the
actual target first, then verbalize the operation on it.

**Generic bridge/synthesis framing:**
> "Prior work on [A] and [B] has developed largely in isolation. We
> integrate ideas from both to propose [method]."

**Reframe toward a nameable mechanism (pick whichever actually fits):**
> "[Prior approach] treats [specific component/assumption/quantity] as
> [fixed/binary/unobserved]. We replace it with [specific alternative],
> which resolves [specific failure mode] without requiring [the
> costly/trained thing prior work needed]."

**Cross-domain transfer is not automatically a Bridge/Synthesis idea.**
Transferring a technique from field A into field B is extremely common and
often legitimate (it's the user's own recurring move: SE fault-localization
theory into LLM-agent trajectories). The question is whether the write-up
names the *specific property* of the source technique being repurposed and
the *specific limitation* it resolves in the target domain — vs. describing
the move as "connecting the two literatures." Same underlying contribution,
two different framings:

- Bridge/Synthesis framing (flagged): "MBFL and agent trajectory analysis
  have not been connected; we bridge fault-localization theory and
  long-horizon agents."
- Mechanism framing (not flagged): "Existing step-credit signals for agent
  trajectories are correlational, expensive, or require a trained tracer. We
  replace [the specific weak signal] with a directional mutation-kill
  statistic that requires no training and bounds replay cost to
  m·K·N·L_tail."

Same technique, same lineage — but the second version leads with a specific
insufficiency and a specific operation, which is what pushes the label off
Bridge/Synthesis and onto Evidence Gap / Empirical Mapping (or
Failure-Risk / Robustification, depending on which specific weakness is
being targeted).
