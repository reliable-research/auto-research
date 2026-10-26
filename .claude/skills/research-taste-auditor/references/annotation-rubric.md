# Diagnostic scoring rubric

Two independent signals matter, and they can disagree:

1. **Categorical signal** (`taxonomy.md`) — *which* opportunity/method cell
   the idea lands in. This is a distributional signal: Bridge+Synthesis is
   the specific cell LLMs over-visit.
2. **Local diagnostic signal** (this file) — *how specific and non-generic*
   the writing is, independent of which cell it lands in.

They're independent because the source paper found that a locally
well-written, specific idea can still land in the overrepresented cell (their
Claude-Sonnet-4.6 sample scored *better* than the human baseline on local
diagnostics — lower boilerplate, comparable specificity — while still being
statistically shifted toward Bridge+Synthesis at the distribution level).
Score both. Don't let good prose talk you out of an honest categorical label,
and don't let a Bridge/Synthesis label alone condemn an idea that's genuinely
specific.

## The three diagnostics (score 0–3 each, integer)

### `surface_stitching` — is this just "A + B"?
Does the method read as taking two existing things and gluing them with a
connecting verb, with no new mechanism in between?
- **0** — no stitching; the contribution is a specific mechanism, not a
  combination.
- **1** — some combination, but a real mechanism links the parts.
- **2** — mostly a combination; the "new" part is thin.
- **3** — textbook A+B: "we combine [existing method 1] and [existing method
  2] to get [name]." Nothing else is added.

### `bottleneck_specificity` — does it name an exact mechanism?
Can you point to the *one* precise thing being changed — a component, an
assumption, a variable, an oracle, a step boundary — or is the target vague?
- **0** — no identifiable mechanism; the target of the intervention could be
  almost anything.
- **1** — a general area is named ("the training process," "the retrieval
  step") but not a specific point of failure or a specific quantity.
- **2** — a fairly specific mechanism is named, with some hedging or breadth.
- **3** — a precise, nameable bottleneck: a specific equation, component,
  failure mode, or assumption that the method targets directly.
Calibration: the source paper's human baseline averages **2.56**; its
weakest tested LLM averages **1.76**; strong models (Claude-Sonnet-4.6,
DeepSeek-V4-Pro) land at **2.3–2.6**, matching or beating humans on this
axis alone.

### `boilerplate` — generic scaffolding vs. load-bearing sentences?
Would this sentence survive if you swapped in a different topic?
- **0** — every sentence is load-bearing; nothing is generic filler.
- **1** — mostly specific, one or two generic framing sentences.
- **2** — noticeably generic; could be lightly reworded to fit many other
  papers.
- **3** — almost entirely template phrasing ("X has attracted increasing
  attention," "however, prior work suffers from limitations," "to address
  this, we propose...").
Calibration: human baseline averages **0.48**; weak LLMs run **0.9–1.25**;
strong models can undercut the human baseline (as low as **0.37**), so a
good boilerplate score alone is not evidence the idea is human-shaped — pair
it with the categorical check.

## Verdict logic

Apply in order; report every condition that fires (they can co-occur):

| # | Condition | Flag |
|---|---|---|
| 1 | Opportunity primary = **Bridge Opportunity** AND Method primary = **Synthesis/Unification** | 🔴 Classic LLM-shaped template |
| 2 | `surface_stitching` ≥ 2, OR `boilerplate` ≥ 2, OR `bottleneck_specificity` ≤ 1 | 🟡 Low-specificity / boilerplate risk |
| 3 | The dominant verb describing what the method *does* is from the LLM-heavy archetype list (see `archetype-verbs.md`), even if the axis labels are something else | 🟡 Watch — surface phrasing reads generic |
| — | None of the above | 🟢 Reads as human-shaped |

A single 🟡 alone is a nudge to tighten language, not a rewrite mandate. Two
or more flags, or a 🔴, warrants doing the reframe pass in `SKILL.md` Step 6.

## Annotation output schema

Use this shape when reporting results (adapt formatting to fit the
conversation, this is not meant to be dumped as raw JSON on the user):

```
Opportunity Pattern: <primary> (secondary: <secondary or none>)
  rationale: <one sentence tied to specific phrases in the text>
Method Paradigm: <primary> (secondary: <secondary or none>)
  rationale: <one sentence tied to specific phrases in the text>
Diagnostics: surface_stitching=<0-3>  bottleneck_specificity=<0-3>  boilerplate=<0-3>
  rationale: <one sentence per score, or combined if short>
Dominant verb(s): <verb(s) found>, archetype family: <LLM-heavy | human-heavy | neutral>
Verdict: <🔴/🟡/🟢 with which condition(s) fired>
```
