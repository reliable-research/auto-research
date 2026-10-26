# Codeless integration decisions

Source: [`codeless@4dd197d`](https://github.com/reliable-research/auto-research/tree/4dd197d18cfdbf0b1df01487a1eede1a209688e9).
Base: `main@355654554d90b270b419ceffd2cc63ea6f779b66`.

## Center idea

Turn an idea into a replayable, evidence-supported research result. Preserve one
question/scope, one frozen measurement contract, one controller, and one audit trail.
An agreement between language models cannot substitute for an observed result.

| Source component | Decision | Integrated form |
|---|---|---|
| S1–S8 definitions and 48 cards | Absorb | Native `research/stages.py` and `cards.py`, supplied on demand |
| Deterministic integrity audit | Absorb and tighten | Native evaluator gates; workspace-scoped paths and fail-closed evidence modes |
| Measurement runner | Absorb and tighten | Trusted S6 command bridge; immutable run IDs, bounded paths, log hashes, raw-record summary recomputation |
| T0–T5 templates | Absorb | Six packaged reference assets; stage/review prompts select the relevant one |
| Builder/Critic/Controller concept | Integrate responsibilities | Native build/review stages, existing `ResearchEngine`, policy, ledger, and claim promotion |
| Separate coordinator, project state, controller, and rollback engine | Omit | One authoritative native state machine; upstream revisions remain explicit new runs |
| AGY-specific client, OAuth-token discovery, rich logger, duplicate CLIs/setup | Omit | Existing provider-neutral command/model adapters and one `ara` CLI |
| Generated project runs, copied papers/text, raster diagrams, HTML portal, ad hoc pipeline scripts | Omit from product tree | Retain the original branch history; use native generated project workspaces |
| Repeated operating manuals and stage-guide copies | Consolidate | One research-loop guide, canonical Python contracts, and packaged templates |

## Evidence of integration

The tests run all original runtime conformance checks, retained codeless card/audit/runner
checks adapted to the standard library, and native end-to-end research workflows.
The offline workflows complete a simulated plan and a measured one-command experiment.
Negative observations retain their valid denominator. Separate cases reject fabricated
results, S2 scope drift, S5 protocol drift, absent instruments, log/summary tampering,
model-authored measurement certification, missing cards, and self-review.

These are software acceptance checks. No existing research-paper result, published
benchmark score, or generated Gemini manuscript was reproduced or endorsed by this merge.
The original branch is preserved, and its commit is a parent of the integration commit.

## Deliberate limits

The integration does not autonomously install a provider, inspect private OAuth files,
rewrite accepted stages on a model's rollback suggestion, or publish a manuscript.
A blocked stage retains its evidence and requires an explicit retry or revised run.
See [RESEARCH_LOOP.md](RESEARCH_LOOP.md) for the executable contracts and setup.
