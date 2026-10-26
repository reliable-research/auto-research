# Readability

This file is about the prose-level decisions that determine whether a reader gets through your paper or bounces. The four concepts below come from hzwer's WritingAIPaper handbook and are the most useful diagnostic frame I've seen for revising scientific writing.

## Four diagnostic dimensions

When a section reads badly, it's almost always failing on one of these:

1. **Logical strength** — does each sentence follow from the previous one?
2. **Defensibility** — could a hostile reader poke a hole in this?
3. **Confusion time** — how often does the reader stop and reread?
4. **Information density** — is each sentence pulling its weight?

Diagnose first, then fix. "This paragraph is bad" is unhelpful; "this paragraph has weak logical structure and three undefined terms" tells you what to do.

## Logical strength: don't fake structure with connectives

Connectives ("therefore," "thus," "to this end," "first… second… last but not least") should *follow* the logic. They shouldn't *create* it. When the underlying argument is muddled, no amount of connective insertion fixes it.

**Anti-pattern 1: connective without antecedent.**

> *"We argue that problem A is critical. To this end, we propose method B."*

"To this end" refers to which end? The previous sentence stated a position, not a goal. The connective is grammatically wrong. Fix by either making the goal explicit ("We aim to address problem A. To this end, we propose method B.") or dropping the connective entirely.

**Anti-pattern 2: imposing order on un-ordered items.**

> *"The system comprises three modules. First of all, Module A is.... Second, Module B is.... Last but not least, Module C is...."*

Unless A→B→C reflects a real dependency, the connectives are lying. They suggest the modules have an order, when really they're just three things. Better:

> *"The system comprises three modules: A, B, and C. Module A handles..."*

When reviewing a draft, scan for connectives. For each one, ask: does this connective accurately describe the relationship between these two ideas? If not, replace or delete.

## Defensibility: read your paper as a hostile reviewer would

Every assertive claim is a target. When you write "Problem A is a pain point in this field and has not been solved yet," ask the reader's questions for them: Why is this a pain point? How serious are the consequences? Has it really not been solved, or are you unaware of work that solved it?

The fix is references and evidence:

> *"It is reported that problem A results in [degradations] [1, 2, 3] and [downstream errors] [4, 5], which are critical to [system performance] because [reason] [6, 7, 8]."*

For results, distinguish between direct evidence and indirect:

- **Direct evidence — make it prominent:** "The performance improves, which is attributed to the fact that XXX..."
- **Indirect evidence — soften the language:** "The improvement may be explained by the fact that XXX..."

When in doubt, hedge accurately rather than overclaim. Reviewers can spot overclaiming, and they punish it harder than honest hedging. "Our method achieves competitive results" is fine when true; "our method achieves state-of-the-art results" had better actually be true.

## Confusion time: minimize "wait, what?" moments

Confusion time is the cumulative seconds a reader spends decoding sentences. Lower is better.

**Tactic 1: explain a concept the moment you introduce it.**

> *"We propose XXX, which is implemented with a two-layer multilayer perceptron (MLP)."*

Don't introduce a name without saying what it is, then make the reader read three more pages to find out. Inline definitions cost almost nothing; deferred definitions cost a lot.

**Tactic 2: resolve relative pronoun ambiguity.**

If a long sentence has multiple possible antecedents for "it," "this," or "they," break the sentence up. Many readers are non-native English speakers; clever sentence structures don't earn extra points and sometimes lose them.

> *Bad:* "We use the encoder, which feeds the classifier, which produces the output, which is then evaluated."
>
> *Better:* "The encoder feeds the classifier. The classifier produces the output. We evaluate this output against the ground truth."

**Tactic 3: topic sentences at the start of paragraphs.**

Readers skim. Make the first sentence of each paragraph carry that paragraph's main claim, so a skimmer who only reads first sentences still gets the argument. The body of the paragraph then defends and elaborates the claim.

This is one of the highest-leverage edits available — going through a draft and rewriting weak topic sentences often does more for clarity than any other single pass.

## Information density: get to the point

Low information density makes readers' eyes glaze over and undermines the perception of expertise.

**Tactic 1: cut the meandering opening.**

The first sentence of a section should not be a history lesson. Sections that start with "Since the beginning of artificial intelligence research..." are wasting the reader's first impression. Start where the paper's contribution starts.

**Tactic 2: balance prose and visuals.**

Don't over-describe a chart in prose; let the chart do its job. Don't under-describe a chart; the reader needs to know what to look at. A common failure mode is a giant figure with two key numbers highlighted, surrounded by paragraphs of text that don't reference the figure at all. Caption thoroughly; refer in prose; don't repeat.

**Tactic 3: keep important explanations close to charts.**

If you want to emphasize a result in Table 5, put the analysis sentence on the same page as Table 5, with "Table 5" appearing both before and after that sentence. Why? Readers using PDF search ("Table 5") need to land somewhere meaningful. And readers scrolling visually need the analysis adjacent to the figure they're looking at.

This sometimes means breaking nice paragraph structure, and that's fine. Clear placement beats elegant flow when the alternative is a reader who can't connect the analysis to the data.

## Charts must be self-explanatory

The ideal: each chart can be understood without the body text. The caption should state both the theme and the key conclusion. Abbreviations in the chart need to be defined in the caption (or, less ideally, the legend).

Don't expect readers to figure out from a complex table who should be compared with whom. If your point is "method A is better than B and C," the table layout should make that immediately visible — typically by putting A, B, C in adjacent rows or columns and bolding A's winning numbers. If the design forces you to repeat a baseline twice for clarity, do that. Inelegant tables don't get rejected; unclear tables do.

## A revision checklist for readability

Before submitting, do a pass with each of these questions:

- Does every connective accurately describe the relationship it's announcing?
- For every assertive claim, can I point to the citation or experimental evidence backing it?
- For every term, do I define it the moment I introduce it?
- For every paragraph, does the first sentence carry the main claim?
- For every long sentence, can a non-native reader parse it without rereading?
- For every figure and table, can someone understand it from the caption alone?
- For every chart referenced in prose, is the analysis on the same page as the chart?
