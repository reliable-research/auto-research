# Discussion loop reference

How to actually run a single stage's critic/refiner cycle. Read this once per conversation; the SKILL.md gives you the high-level summary, this file is the operational detail.

## Correcting the skill's own origin story

Earlier drafts of this skill described "the original system" as three separate AI models (proposer, critic, refiner) plus a human supervisor, all looping together until convergence. Having gone back to the actual reference platform, that's not quite right, and it's worth being precise about the difference, because it changes how the refiner should behave:

- **The proposer is the student — a human, not a model.** The platform's AI only ever plays critic and refiner. Claude drafting v1 for the user (the default in this skill) is a *convenience this skill adds*, standing in for work a human would normally do by hand. That's fine, but it means: when the user supplies their own draft, treat it the way the real system treats a student submission — something to critique and polish, not something to second-guess the framing of.
- **Critic and refiner are sequential phases, not an interleaved loop.** In the real system, only the **critic** phase repeats (bounded by a round cap, student decides each round whether to revise-and-recritique or move on). The **refiner** runs *once* per critic phase, and is deliberately conservative — see below.
- **Closing a stage is either automatic or requires a human supervisor's approval** (`step_approval_mode`, default `supervised`). There's no AI "decider" role weighing severity thresholds — a human always makes the close/no-close call, or it's automatic by room policy.

This skill still runs a fuller critique-refine-critique-refine convergence cycle than the reference platform does, by design — Claude has to self-supervise without a separate human in every seat, so giving it room to iterate past a single critic-then-refiner pass is a reasonable, disclosed enhancement. Just don't describe it to the user as a literal mirror of the reference system. It isn't. It's a deliberate superset built for a context where no second human is available to play supervisor.

## The roles you play

- **Proposer** — drafts v1 of the stage's structured output. Uses the user's seed and the prior confirmed outputs as input. If the user supplied their own draft, that *is* v1 — don't redraft it from scratch. Aim for a real attempt, not a strawman; the loop converges faster from an honest first draft.
- **Critic** — evaluates the current draft against the rubric in `references/stages.md` for the current stage *and* the cross-stage consistency rules, while respecting that stage's declared critic boundaries (each stage in `stages.md` lists what the critic must *not* drift into). Output is a `summary` string plus a list of `comments`, each tagged `[major]` or `[minor]` and referencing the field it's about.
- **Refiner** — produces the next version of the draft. Unlike a general-purpose editor, the reference platform's refiner is written to be *narrow on purpose*: polish wording, tighten internal consistency, formalize where the content already supports it — and explicitly avoid inventing new content, adding components that weren't there, or redesigning the argument. If a `[major]` issue needs more than that to fix — a genuinely new sub-problem, a new method, a new baseline — that's a proposer-level change, not a refiner-level one. Say so, and re-propose rather than quietly having "the refiner" do it.
- **Decider** — in the reference platform this is literally the human student (accept the critic's point and revise, or ignore and move on) and, for closing the stage, a human supervisor (or automatic room policy). In this skill, that's the user — ask, don't assume, when severity is genuinely ambiguous. Autoclaude mode is the one exception, where Claude plays this role too (see `autoclaude_mode.md`).

You don't need to label these roles in the visible output every round — that gets noisy. Internally, route your own reasoning through them; externally, what the user sees is "round N: <summary of what changed>, <critic flags>, <decision>."

## Round-by-round structure

Two distinct phases per stage, not one repeating loop:

**Phase A — Critic loop (can repeat, bounded).**
```
ROUND <N>  [critic phase]
  draft_vN: { ... structured output for the stage ... }
  critique:
    summary: "<1-2 sentences on the overall state of the draft>"
    comments:
      - { severity: major|minor, field: "<which field>", anti_pattern: "<name from stages.md or null>", comment: "<what's wrong and why>" }
  decision: revise_and_recritique | move_to_refiner
```
At each round, the decision to loop again or move on belongs to whoever is playing the student in this conversation — usually the user, in stage-by-stage mode; Claude itself in autoclaude mode. Don't auto-loop past the round cap regardless of severity (see stop rules).

**Phase B — Refiner pass (runs once, after the critic phase concludes).**
```
REFINER PASS
  refined_draft: { ... }
  changes_made: "<what was tightened/formalized, one line>"
  declined_to_fix: [ "<any [major] issue the refiner correctly left alone because fixing it would mean inventing new content>" ]
```
The refiner pass happens exactly once per critic-phase conclusion. If `declined_to_fix` is non-empty, surface those to the user explicitly — they need a fresh proposer pass, not more polish.

Show the user a compact version of each: round N → "what changed this round" → critic's `summary` → list of major flags (one line each) → decision. Save the full structured detail for if they ask.

## Stop rules for the critic phase

**The prime rule: a stage does not close over an open `[major]`.** When a critique returns any `[major]` comment, the default next action is always one more round — revise the draft to resolve each `[major]`, then re-critique — not moving on. `[minor]` comments never force another round; batch them into the refiner pass or carry them as notes. This asymmetry is the point of the severity system: majors are structural and block, minors are polish and don't.

Apply in order:

1. **Resolution round (automatic)** if the latest critique contains any `[major]`: revise targeting each `[major]` specifically, re-critique, repeat while majors remain and the round cap isn't hit. Each resolution round's critique must explicitly state, per previous `[major]`, whether it is now *resolved*, *still open*, or *transformed* into a different issue — don't let majors silently evaporate between rounds.
2. **Move to refiner** when a critique returns zero `[major]` flags (any number of minors is fine).
3. **User override** — the user may still say `ignore_and_submit` with majors open. Honor it, but (a) warn once, concretely: name each open `[major]` and what it will cost downstream ("this uncovered hypothesis means stage 6 can't generate its RQ"); (b) record the open majors in the stage's confirmed output as `known_open_majors: [...]` so they carry forward visibly into the trace and later stages rather than vanishing. In **autoclaude mode there is no override** — Claude is playing the student, and a student who waves through their own majors defeats the self-play; majors always get a resolution round, up to the cap.
4. **Escalate to the user** if:
   - The round cap (default **5**, matching the reference platform's `max_critic_rounds` default; raisable to 50 on request) is hit and `[major]` issues still remain — the rubric or the seed idea has a gap that more iteration alone won't fix. Present the surviving majors and ask: revise the seed, back up a stage, raise the cap, or accept with `known_open_majors`.
   - The same `[major]` flag repeats across three consecutive rounds with no real change — the loop is stuck, usually because an earlier stage has a problem worth revisiting.
   - A cross-stage consistency check is failing because a *prior confirmed* stage is wrong, not the current one. Surface this immediately and offer to back up (see below) — don't silently patch around it.
5. Once the critic phase ends (by any of the above), always run **exactly one** refiner pass before presenting the result — even if the critique came back clean. This matches the reference system's behavior of always finishing with a refiner pass; the difference here is there's only ever one, and it's conservative by design. If the refiner's `declined_to_fix` list contains anything that was a `[major]`, the stage is *not* actually resolved — go back to rule 1 (a proposer-level revision), don't present a confirmed output with a declined major.

## Convergence check (for this skill's extended loop)

If the user opts to keep revising past what the reference platform would (i.e., wants another full critique-refine-critique cycle rather than accepting after one refiner pass), a round produced "no substantive change" if:
- All `[major]` flags from the previous round are still present, and
- The diff between vN-1 and vN is below ~10% of fields changed.

Two such rounds in a row → treat as stuck, escalate rather than continue.

## Critic behavior

- **Severity is anchored, not discretionary.** Anti-pattern matches from `stages.md` are `[major]` by default. Don't soften them because the rest of the draft is good.
- **Be specific.** "This section is unclear" is useless. Name the field and the anti-pattern: "`objective` doesn't reference a metric — vague_success."
- **Don't pile on.** Group minor stylistic comments into one line rather than listing twelve. The loop exists to fix structural issues, not to gold-plate prose.
- **Cross-stage flags first.** Uncovered hypotheses, orphan sub-problems (checking for the `__novel__` exception first), missing limitation references — these are almost always `[major]` and worth surfacing before line-level nits.
- **Respect the stage's declared boundaries.** Don't critique method quality in stage 2, or novelty in stage 1 — that's not this stage's job, and raising it just adds noise the student has to mentally file away for later.
- **Escalate to the mined-checks pass when warranted.** `references/mined_review_checks.md` holds an adversarial second layer, mined from real reviewer comments, keyed by stage. Run it (selectively — 3-6 checks, not all of them) when the user asks for a hard/reviewer-level review, when a nontrivial draft passes the base rubric on the first critique (a clean round 1 is a signal the critic under-fired, especially in autoclaude self-play), or on stages 5-6 for competitive-venue targets. Never on round 1 by default.

## Refiner behavior

- **Default to conservative.** The reference platform's actual refiner guidance is explicit about this per stage — phrases like "avoid heavily rewriting," "avoid inventing," "avoid substantially redesigning" appear for every single stage. Mirror that instinct: your job is to make the existing content clearer and more internally consistent, not to make it better by adding things the student didn't put there.
- **Preserve stable IDs.** If `lim_decoder_greedy` is referenced from stage 4, don't silently rename it to `lim_greedy_decoding` between rounds. Rename only on a decisive, disclosed change.
- **Don't drop content** the critic didn't ask to drop. If round 2 had five sub-problems and the critic only flagged one, round 3 should still have five (or four, if one was explicitly merged on a critic note).
- **Formalize where it's free.** In stage 1 especially, if the content already supports a more precise notational version, produce it — that's genuinely part of the refiner's job, not scope creep.
- **Surface, don't silently ignore, disagreement.** If a critic comment misreads the draft, say so explicitly (`defenses: [...]`) rather than quietly not applying it.

## What to show the user during the loop

Default presentation per round (compact):

```
**Round N — <decision>**
- *Changes this round:* one line
- *Critic summary:* one line
- *Major flags:* `[anti_pattern_name]` field — one-line description, with per-flag resolution status vs. the previous round (resolved / still open / transformed)
                 (omit this line if no major flags)
- *Minor flags:* count only ("3 minor flags")
```

After the loop ends, present:
- The final confirmed output, fully rendered
- A 1-2 line "what was hardest" note (which anti-patterns kept showing up — useful for the user to know about their own thinking)
- The total round count, whether the refiner declined to fix anything (and why), and any `known_open_majors` accepted by user override

**Keep the full trace regardless of what's shown.** The compact format is a *presentation* choice, not a retention choice: the complete round-by-round record — every draft version, every critique with all its comments and severities, every decision, every refiner pass with its `changes_made`/`declined_to_fix` — is one of the pipeline's three final deliverables (see SKILL.md "Final deliverables"). In a file-tool environment, append each round to a trace file as you go rather than reconstructing it at the end; in pure chat, be prepared to render the full trace on request at any point.

If the user asked to see "every round in full," skip the compact format and dump everything. Otherwise stick to compact.

## When to back up to a prior stage

If during stage N the cross-stage checks reveal that stage M (M < N) has a real problem, surface this immediately and offer to back up:

> The critic flagged that `sp_grounding` has no clean source limitation and doesn't qualify as a novel decisive component either — the closest candidate (`lim_decoder`) was too vague to cleanly target. We could either (a) tighten `lim_decoder` in stage 3, or (b) drop `sp_grounding`, or (c) mark it `["__novel__"]` if you can articulate why it's a decisive component no prior work addresses. Want to revise stage 3, or is (c) accurate?

Don't silently fix prior stages — the user signed off on them. Always ask.
