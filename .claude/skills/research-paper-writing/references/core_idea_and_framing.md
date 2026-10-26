# Core Idea and Framing

The hardest part of writing a paper is not writing — it's deciding what the paper is about. This file covers how to find and articulate the contribution, and how to set it up so a reader gets it within the first page.

> When the user is at the abstract or first-paragraph stage, also load `corpus_patterns.md` — it has empirically-grounded opening templates and concrete examples from award papers that complement the principles below.

## What kind of contribution do you have?

Almost every published paper falls into one (sometimes two) of three categories. Identifying which one your work is helps you frame the paper:

1. **Insight** — you have an explanation for a phenomenon that already exists. (e.g., "We show why dropout works as implicit ensembling.")
2. **Performance** — you can do something measurably better than prior work. (e.g., "We achieve 2.4 BLEU points over the previous SOTA on WMT En-De.")
3. **Capability** — you can do something that could not be done before. (e.g., "We demonstrate few-shot learning of a new task class with no fine-tuning.")

When the user is unclear about their contribution, ask which of these their work is. Most struggling drafts try to claim all three weakly rather than one strongly.

## Novelty is not a vibe — it's structural

Authors often worry their work "isn't novel enough." Usually the work is fine; the framing is the problem. Novelty comes from:

- **A research topic that matters** (foundational areas with broad downstream impact)
- **A solution that's elegantly simple or surprisingly effective**
- **A technique or principle that generalizes**

The ResNet paper is the canonical example: written one way it's "we used 3×3 convs and shortcuts" (not novel). Written another, it's "we identified the degradation problem in deep nets, abstracted the underlying principle of identity mappings, and validated it experimentally" (foundational). The technical work is the same. The framing is everything.

When helping a user, push them past their first description of the work toward the underlying *principle*: what did you actually discover or enable?

## Don't underestimate your own work

A common failure mode is the user describing their contribution as a list of mechanical steps. Help them surface the *why*. Ask:

- "If a researcher five years from now references this paper, what one sentence will they cite it for?"
- "What would the field be missing if your paper didn't exist?"
- "What's the simplest version of your insight that you'd put on a t-shirt?"

If they can't answer, the contribution isn't sharp enough yet — and no amount of writing will save it. The real work in this case is back at the whiteboard, not in Overleaf.

## Find the audience and write for them

The mistake newcomers make is presenting their *research process* (with all its dead ends and detours) instead of their *findings*. Researchers all understand that research is messy; nobody wants to read your messy draft of it. Save the chronology for the postscript or blog post.

Practical tactic: **make a one-slide pitch first**. Present it to a colleague who isn't familiar with the work. The questions they ask reveal what's confusing or missing. Iterate the slide before iterating the paper. If the slide is muddy, the paper will be too.

## Performance gains alone don't carry a paper

A small improvement on a benchmark is not, by itself, a contribution. Reviewers will (rightly) ask: what did we *learn*? If the answer is only "this number is higher," the paper is at risk. Numbers are evidence for a contribution; they aren't the contribution itself.

The corollary: don't hide a real insight behind benchmark tables. If your paper's actual contribution is a new way of thinking about something, lead with that, and use the numbers to back it up — not the other way around.

## Anti-pattern: optimizing for past SOTA

Kaiming He's framing is useful here: focus on the future, not on past leaderboards. Ask whether the contribution will still matter in five years, regardless of whether some specific 2026 benchmark gets beaten next year. Apply Occam's razor — simpler solutions tend to generalize. Convoluted techniques bolted on solely to win an evaluation tend not to. When a draft has six new tricks, ask which two are actually doing the work, and whether the others are just chasing decimal points.

## Three takeaways to apply when framing

1. **Clearly articulate the increment over prior work.** One or two core ideas, made explicit. Not five.
2. **New phenomena and ideas matter more than performance gains.** Lead with the discovery, support with numbers.
3. **Around the contribution statement, build a solid analytical results section.** Don't just throw tables in; explain what the numbers tell us about the contribution.
