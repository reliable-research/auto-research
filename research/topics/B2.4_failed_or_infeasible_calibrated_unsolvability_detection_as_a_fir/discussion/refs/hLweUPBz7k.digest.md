# Digest (lightweight, backfilled): From Conversation to Query Execution: Benchmarking User and Tool Interactions for EHR Database Agents

- **Title**: From Conversation to Query Execution: Benchmarking User and Tool Interactions for EHR Database Agents
- **OpenReview id**: hLweUPBz7k
- **URL**: https://openreview.net/forum?id=hLweUPBz7k
- **Source**: extracted from `topics/corpus/ideas.jsonl` (paper_id `hLweUPBz7k`), a real corpus of 11,683 OpenReview papers already used to ground `digest.md` N3/N4 for this topic. OpenReview's own paper page returns a bot-verification wall (confirmed via WebFetch during this backfill), so no local PDF could be cached; this digest is built from the corpus's own proposal text (motivation + method fields), which is itself grounded in the paper's real motivation/method sections, not invented. Lightweight digest, not a full paper-digest N0-N12 run.

## Motivation (from corpus proposal, truncated)
Current evaluation of EHR database question answering is dominated by text-to-SQL formulations that assume the user’s request is already sufficiently specified. This assumption is problematic in clinical settings. @lee2022ehrsql showed that EHR querying is inherently domain-specific, involving complex schemas, temporal conditions, and specialized terminology, while @ryu2024ehrseqsql showed that sequential context matters for EHR exploration. However, both benchmark families still primarily evaluate SQL construction from given utterances, not the prior interactive work required when the utterance is vague or uses language that does not directly match database values.

A more specific gap appears when ambiguity and agent autonomy are considered together. @dong2025practiq demonstrates that ambiguous and unanswerable questions are common and difficult, but its interaction template is scripted: clarification occurs in a predefined format and on a fixed conversational schedule. This means the benchmark does not test whether an agent can decide when to ask the user, when to inspect the database, or when to attempt a direct answer. At the same time, general agent benchmarks such as @yao2025taubench and @shim2025tooldial show the importance of evaluating joint user-tool interaction, but they do not capture the EHR-specific problem of value mismatch, where clinical brand names, abbreviations, lay terms, and database entries often diverge.

This gap matters because clinical database acc

## Method (from corpus proposal, truncated)
We propose EHR-ChatQA, an interactive benchmark for evaluating end-to-end LLM database agents in EHR settings. Instead of scoring only question-to-SQL mapping, the benchmark places an agent in a simulated environment where it must resolve query ambiguity through conversation, resolve value mismatch through tool use, and then generate executable SQL. This formulation directly targets the gap left by EHR text-to-SQL benchmarks such as @lee2022ehrsql and @ryu2024ehrseqsql and extends the user-tool-agent evaluation paradigm introduced by @yao2025taubench and @shim2025tooldial into the clinical database domain.

1. **Clinically Grounded Interactive Task Construction**: We build tasks from real EHR databases and clinically meaningful SQL queries so that interaction remains anchored to authentic medical retrieval problems, following the grounding principle established by @lee2022ehrsql. We then transform these queries into user instructions that intentionally withhold information or rephrase database values in everyday or alternate clinical language, creating controlled ambiguity and value mismatch that static text-to-SQL datasets do not test.

2. **Two Interaction Flows for Query Refinement**: We structure the benchmark around Incremental Query Refinement and Adaptive Query Refinement. The first extends the sequential setting highlighted by @ryu2024ehrseqsql by requiring the agent to preserve and update query state as users add constraints; the second goes further by requiring cond

## Limitation (as used in digest.md N4, this topic)
Treats underspecification as *resolvable* via clarification questions or database exploration; never requires the agent to certify that a request is infeasible and stop, nor provides construction-guaranteed infeasibility labels to score such a call against.

## Relevance to B2.4
Closest interactive-ambiguity benchmark; B2.4's command-line/tool-agent domains extend this paper's user-agent-tool-loop evaluation style to genuinely unsolvable (not merely ambiguous/resolvable) instances.
