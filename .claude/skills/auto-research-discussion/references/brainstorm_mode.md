# Brainstorm mode reference

For when the user has a rough direction but no specific problem yet — "I want to work on something in X" rather than an actual seed idea. The reference platform runs this as a separate upstream workflow (a "Topic Funnel") before a candidate ever reaches stage 1. It's a genuinely different shape from the six-stage pipeline: fan out into several candidates, cheaply pressure-test each against the literature, then converge on one.

## Why this is a separate mode, not "stage 0"

The six stages (`stages.md`) all take a single confirmed problem and refine it. Brainstorming does the opposite first — it generates several *competing* candidates and kills most of them before any of the six-stage rigor gets applied to just one. Trying to fold this into stage 1 would mean running the full critic/refiner loop on ideas you're about to discard, which is wasted effort. Do the funnel first, then hand exactly one winner into stage 1 as its seed.

## The three steps

### Step 1: Direction & context

Ask the user for:
- **Direction** — the general area, one or two sentences ("automated testing for mobile apps," not a specific topic yet).
- **Context & constraints** — background, prior work they've already seen, methods they want to use or avoid, resource constraints (compute, timeline, team size).

Don't push them to sharpen this into a specific problem yet — that's what step 2 is for. If they already have a specific problem, this mode is the wrong entry point; go straight to stage 1 instead.

### Step 2: Generate and scout candidates

**Generate 4-6 candidate topics** from the direction and context. Each candidate needs:

```
{
  "candidate_id": "c_<slug>",
  "title": "short working title",
  "summary": "2-4 sentences: what this topic is about",
  "problem_seed": { ... a draft stage-1 Problem Definition, if this candidate were promoted ... },
  "motivation_seed": { ... a draft stage-2 Motivation, same idea ... }
}
```

Make the candidates genuinely different from each other — different sub-problems within the direction, different angles, different levels of ambition — not five rephrasings of the same idea. Diversity here is the entire value of doing this step at all.

**Then scout each candidate against the literature — this is the step worth doing properly.** The reference platform's actual scouting pipeline (independent of any single AI provider) does, roughly:
search a curated set of relevant top venues → deduplicate → snowball from the strongest hits via citation graphs (backward references, optionally forward citers, multiple hops, gated so only genuinely on-topic papers become new seeds) → enrich with abstracts → rank, favoring top venues → have an LLM read title+abstract (not full text, unless the user supplies a PDF) to produce a structured landscape summary and a synthesized gap list → issue a **GO/NO-GO verdict**.

You won't have that exact pipeline, but you do have `web_search` — use it, per candidate, and hold yourself to the same discipline: search for genuinely close prior work (favor papers you can name a real venue for), don't claim closer familiarity with a paper than title/abstract gives you, and be explicit when a candidate's landscape search came back thin. Then produce, per candidate:

```
{
  "novelty": "high | medium | low, with the strongest existing-work threat named",
  "feasibility": "high | medium | low, given the stated constraints",
  "verdict": "pursue | refine | reject",
  "gaps": ["what existing work misses that this candidate would address"],
  "rationale": "why this verdict, in 2-3 sentences"
}
```

Be honest about `reject` and `refine` — the entire point of this step is to kill weak candidates cheaply, before six stages of rigor get spent on them. A funnel that promotes everything isn't a funnel.

### Step 3: Compare and promote

Show the candidates side by side — title, one-line summary, novelty/feasibility, verdict, and the single strongest competing paper for each. Let the user pick one (or, if they want, ask you to combine strong elements of two).

Once they pick, **promote it**: the winning candidate's `problem_seed` and `motivation_seed` become the v1 drafts for stage 1 and stage 2 respectively — not blank slates. Tell the user which candidate you're carrying forward and move into the normal six-stage flow (`stages.md`, `discussion_loop.md`) starting at stage 1, treating the seed as v1 rather than redrafting from scratch.

## What's different from the reference platform here, on purpose

The platform's version of step 2 has the user copy a generated prompt into an external chat with deep-research capability, then paste the JSON response back in — a round trip that exists because the platform itself can't call an LLM to do open-ended research. That constraint doesn't apply here: you *are* the chat, and you have `web_search`. Do the generation and the scouting inline, in the same turn if reasonable, rather than asking the user to go elsewhere and bring back results. That's a genuine improvement this skill can make on the original design, not a corner cut.

## Failure modes to watch for

- **Fake diversity** — candidates that are the same idea with different nouns. If two candidates converge to the same `problem_seed` after drafting, merge them and generate a genuinely different fourth.
- **Verdict inflation** — calling everything `pursue` because generating a `reject` feels unhelpful. A `reject` with a well-named threat paper is more useful to the user than an optimistic `refine`.
- **Skipping the scout** — jumping straight to "which do you like best?" without checking the literature defeats the purpose; novelty claims made without a search are just guesses.
