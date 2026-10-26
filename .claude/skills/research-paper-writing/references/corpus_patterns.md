# Patterns from the Award-Paper Corpus

This file is grounded in a regression-test corpus of 10 award-winning papers from top AI/ML venues 2023–2025 (NeurIPS, ICML, ICLR, ACL, CVPR). Their abstracts and introductions are stored as `.md` excerpts in the corpus; the patterns below are extracted from how these papers *actually* frame their work — not how textbooks say they should.

When applying this skill to a paper-writing task, treat these as concrete templates to adapt rather than abstract advice.

## The corpus

| Short ID | Title | Venue | Award |
|---|---|---|---|
| `var` | Visual Autoregressive Modeling | NeurIPS 2024 | Best Paper |
| `dpo` | Direct Preference Optimization | NeurIPS 2023 | Outstanding RU |
| `emergent-mirage` | Are Emergent Abilities of LLMs a Mirage? | NeurIPS 2023 | Outstanding |
| `vit-registers` | Vision Transformers Need Registers | ICLR 2024 | Outstanding |
| `stealing-llm` | Stealing Part of a Production Language Model | ICML 2024 | Best Paper |
| `privacy-audit` | Privacy Auditing with One (1) Training Run | NeurIPS 2023 | Outstanding |
| `scaling-data` | Scaling Data-Constrained Language Models | NeurIPS 2023 | Outstanding RU |
| `impossible-lms` | Mission: Impossible Language Models | ACL 2024 | Best Paper |
| `train-worst-plan-best` | Train for the Worst, Plan for the Best | ICML 2025 | Outstanding |
| `diffusion-no-memorize` | Why Diffusion Models Don't Memorize | NeurIPS 2025 | Best Paper |

## Pattern 1: Five repeatable opening templates

Award abstracts cluster into a small number of opening templates. Pick one.

### Template A — "We present/introduce + named artifact"

The most common high-confidence opener. Used when the contribution has a clean named output (algorithm, architecture, system, attack).

> *VAR:* "We present Visual AutoRegressive modeling (VAR), a new generation paradigm that redefines the autoregressive learning on images as coarse-to-fine 'next-scale prediction'..."

> *Privacy-Audit:* "We propose a scheme for auditing differentially private machine learning systems with a single training run."

The artifact is named in the first sentence and typically also in the title. The first sentence reframes the contribution in one phrase — *"redefines AR learning as next-scale prediction"*, *"single training run"*. That phrase is the t-shirt slogan; everything else is elaboration.

### Template B — "Problem framing → existing approach → its limit → our approach"

Used when the contribution is methodological (a better way of doing something already being done).

> *DPO:* "While LMs learn broad world knowledge..., achieving precise control of their behavior is difficult... Existing methods... use RLHF. However, RLHF is a complex and often unstable procedure... In this paper we introduce a new parameterization..."

The structure is: capability gap → standard fix → flaw in standard fix → our fix. The flaw in the standard fix is what justifies the paper's existence. If you can't articulate this flaw cleanly in one sentence, you don't yet have a paper, you have a hobby.

### Template C — "They claim X. However, there is very little evidence. Here, we..."

The refutation/critical-analysis opener. High-impact, hard to pull off without solid evidence.

> *Emergent-Mirage:* "Recent work claims that large language models display emergent abilities... Here, we present an alternative explanation: that... emergent abilities appear due to the researcher's choice of metric rather than due to fundamental changes in model behavior..."

> *Impossible-LMs:* "Chomsky and others have very directly claimed that LLMs are equally capable of learning languages that are possible and impossible... However, there is very little published experimental evidence to support such a claim. Here, we develop..."

The "However" pivot is the structural hinge. The opening establishes a target claim with citations, then the paper occupies the niche by providing the missing evidence. Note that both papers are very precise about *what* they're refuting — not "people are wrong about LLMs" but a specific named claim by specific named authors.

### Template D — "Trend/setup → research question → concrete experiment scope"

Used when the contribution is empirical mapping of a regime nobody has charted.

> *Scaling-Data:* "The current trend of scaling language models involves increasing both parameter count and training dataset size. Extrapolating this trend suggests that training dataset size may soon be limited... Motivated by this limit, we investigate scaling language models in data-constrained regimes. Specifically, we run a large set of experiments... ranging up to 900 billion training tokens and 9 billion parameter models."

The trend statement gives the paper urgency (this thing is going to happen). The experimental scope (900B tokens, 9B params, 400 runs) signals seriousness — the reader knows this is not a toy study.

### Template E — "Question → answer with one striking number"

Used for results that have a memorable headline.

> *Stealing-LLM:* "In this paper we ask: how much information can an adversary learn about a production language model by making queries to its API?... For under $20 USD, our attack extracts the entire projection matrix of OpenAI's ada and babbage language models."

The dollar figure ($20) is the headline. The reader will remember the number and look up the paper.

## Pattern 2: Numbers in the abstract are non-negotiable

Every paper in this corpus (except Privacy-Audit, which is unusually short) drops at least one concrete number into the abstract:

- VAR: "FID from 18.65 to 1.73", "20× faster inference"
- DPO: (no specific numbers in abstract — uses qualitative claims; this is unusual)
- Stealing-LLM: "$20 USD", "1024 and 2048", "$2,000"
- Scaling-Data: "900 billion training tokens and 9 billion parameter models", "up to 4 epochs"
- Train-Worst-Plan-Best: "<7% to ≈90%", "7× as many parameters"
- Diffusion-No-Memorize: linear scaling τmem with n

The number does work the prose can't: it's a memorable hook, an honesty signal, and a pre-commitment that the body will deliver.

DPO's abstract is interesting — it stays qualitative ("matches or improves response quality") because the paper's value is the method, not the size of the gain. When in doubt, include numbers; only skip them when the paper is genuinely method-first and the numbers are confirmatory.

## Pattern 3: The "named artifact" rule

Almost every contribution-driven paper in the corpus introduces a named artifact:

- **VAR** (the model)
- **DPO** (the algorithm)
- **Register tokens** (ViT-Registers)
- The unnamed "single-run audit scheme" (Privacy-Audit) — note this paper's relative obscurity vs. DPO; named things travel better
- **τgen and τmem** (Diffusion-No-Memorize) — even theoretical papers benefit from named quantities

When helping with a paper, push for a name. "Our method" is what unconfident first drafts say. Award papers say "DPO" or "Visual AutoRegressive (VAR) modeling" or "register tokens."

The name should ideally:
1. Appear in the title
2. Be sayable in conversation ("we use DPO for this," not "we use the new parameterization of the reward model")
3. Encode the key idea ("register tokens" tells you what they do; "auxiliary tokens" wouldn't)

## Pattern 4: How introductions open

Looking at the first paragraph of each paper's introduction:

**Wide-context opener** (VAR, Diffusion-No-Memorize, ViT-Registers): start with the broader field/method, then narrow. Three to five sentences before the contribution sentence.

> *VAR:* "The advent of GPT series and more autoregressive (AR) large language models (LLMs) has heralded a new epoch in the field of artificial intelligence. These models exhibit promising intelligence in generality and versatility... At the core of these models is a self-supervised learning strategy – predicting the next token..."

**Definitional opener** (Privacy-Audit, Emergent-Mirage): start with a precise definition or formal statement of the object being studied.

> *Privacy-Audit:* "Differential privacy (DP) provides a quantifiable privacy guarantee by ensuring that no person's data significantly affects the probability of any outcome. Formally, a randomized algorithm M satisfies (ε, δ)-DP if..." [includes the equation immediately]

**Problem-first opener** (DPO, Impossible-LMs): start with the problem the paper exists to solve.

> *DPO:* "Large unsupervised language models trained on very large datasets acquire surprising capabilities. However, these models are trained on data generated by humans with a wide variety of goals, priorities, and skillsets. Some of these goals and skillsets may not be desirable to imitate..."

The choice depends on how much background the reader needs. If you can assume readers know the area, use problem-first. If the paper introduces a less-familiar setting, use wide-context. For theoretical papers, definitional often works.

## Pattern 5: Two-sided structures for trade-off papers

When a paper's contribution involves trading off two competing forces, an explicit two-sided structure works well:

> *Train-Worst-Plan-Best abstract:* "MDMs trade off complexity at training time with flexibility at inference time. At training time, they must learn to solve an exponentially large number of infilling problems, but at inference time, they can decode tokens in essentially arbitrary order. **In this work, we closely examine these two competing effects. On the training front, we theoretically and empirically demonstrate... On the inference front, we show that...**"

The "On X front... On Y front..." parallelism is doing real work. It tells the reader: there are two pieces, and we'll address both. It also doubles as a section roadmap.

If your paper has two distinct contributions, force them into parallel sentence structure. If they don't fit a parallel structure, you may have one contribution and one side-effect, or two papers smashed together.

## Pattern 6: How to write a "first ever" or "first time" claim

Several award papers use "first time" claims. They work when scoped tightly:

- VAR: "VAR, **for the first time**, makes GPT-style AR models surpass diffusion transformers in image generation"
- Stealing-LLM: "We introduce **the first** model-stealing attack that extracts precise, nontrivial information from black-box production language models"
- Stealing-LLM (later): "**for the first time**, that these black-box models have a hidden dimension of 1024 and 2048"

Note the scoping: "first time **for X-shaped paradigm** to **achieve Y**." Without scoping, "first time" claims read as overconfidence and invite reviewer attacks. With scoping, they're checkable and defensible.

When helping a user with a "first" claim, push them to scope it: first to do *what*, in *which* setting, against *which* baselines? If they can't scope it, downgrade to "we show that..." or "to our knowledge..."

## Pattern 7: Promised properties as a list

DPO and ViT-Registers both list properties of their contribution as a comma-separated tail:

> *DPO:* "the resulting algorithm... is **stable, performant, and computationally lightweight**, eliminating the need for sampling from the LM during fine-tuning..."

> *ViT-Registers:* "this solution **fixes that problem entirely** for both supervised and self-supervised models, **sets a new state of the art** for self-supervised visual models on dense visual prediction tasks, **enables object discovery methods** with larger models, and most importantly **leads to smoother feature maps and attention maps**..."

The list pattern works because each property is a separate claim the paper has to defend in the body. A reader who likes any one property has reason to keep reading. Limit to 3-5 properties; more starts to look like a sales brochure.

## Pattern 8: Code/model release as a reputation signal

Papers in this corpus often include the code/model release in the abstract itself:

- VAR: "We have released all models and codes to promote the exploration..."
- Scaling-Data: "Models and datasets from our 400 training runs are freely available at https://..."

This is partly community service, partly reputation signaling. A paper that releases artifacts is implicitly saying "we did the work, here's the proof." For empirical papers especially, including the release in the abstract is now expected at top venues.

## Pattern 9: The "implication for future work" closing

Several papers close their abstract with implications:

- Stealing-LLM: "...discuss the implications of possible future work that could extend our attack."
- Impossible-LMs: "...we hope our approach opens up a productive line of inquiry..."

This is fine — but only after the contribution is fully stated. Don't open or center the abstract on what *might* be possible; close on it.

## Anti-patterns observed by their absence

Things these abstracts **don't** do, that weak abstracts often do:

- They don't open with "Recently, deep learning has revolutionized..."
- They don't say "we apply [method] to [task]" without further claim of why this matters
- They don't conclude with "extensive experiments demonstrate the effectiveness of our method" as the only result statement — they give specific numbers
- They don't promise "novel" or "groundbreaking" — they show novelty by what they describe, never by saying the word
- They don't list every related-work citation in the abstract — they save that for related work

Keep this list in mind during revision. If a draft abstract reads like any of these patterns, push back hard.

## Practical takeaways for using this skill

When helping a user write or revise an abstract or introduction:

1. **Identify which template (A-E) fits their paper.** If none does, the contribution probably isn't sharp enough yet — flag this back.
2. **Push for a name.** What's the t-shirt-slogan name for the contribution?
3. **Push for a number.** What's the headline numerical result?
4. **For "first" claims, scope tightly.** First to do *what* under *which* conditions?
5. **For lists of properties, keep to 3-5.** And every one must be defendable in the body.
6. **For two-sided contributions, force parallel structure.** "On X... On Y..."
7. **For critical/refutation papers, name the target claim precisely.** Cite who said it and where.
8. **End the abstract on something concrete.** A number, a release, a scoped implication. Not a hand-wave.
