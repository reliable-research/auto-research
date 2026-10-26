---
name: paper-digest
description: >-
  Decompose a research paper PDF into a structured N0-N12 knowledge digest: metadata,
  problem, motivation, related work, prior limitations, challenges, methodology
  (challenge-to-mechanism map), contributions, research questions, results, threats,
  artifacts, whole-paper contribution-type, and a claims list. Ported from a production
  single-agent LLM extraction service: every item carries status
  (FOUND/PARTIAL/NOT_FOUND), source (extracted/inferred), a page+section locator, a
  3-part absence_comment when missing, and resolvable cross-node ids. Use when the user
  uploads/links a paper and wants its novelty, methods, contributions, or structure
  extracted, or asks to "digest", "break down", "summarize the contributions of",
  "extract the method", "classify", or "compare" papers, or wants structured output over
  a loose summary. Hand off to pengsida-paper-writer to reconstruct/compare, or
  se-paper-reviewer / pengsida-stage-reviewer to review. Trigger on paper uploads, arXiv
  links, "digest this paper".
---

# Paper Digest

Turn an unstructured paper into a checkable N0–N12 argument chain with full evidence
discipline — every node anchored to where it came from, every cross-reference resolvable,
every gap explained rather than papered over. This is the extraction front-end; for writing
or comparing papers from a digest, use `pengsida-paper-writer`; to review, use
`se-paper-reviewer` or `pengsida-stage-reviewer`.

## Provenance

This skill ports the node semantics, extraction rules (EX-01..EX-12), and schema of a
production paper-knowledge-extraction service (`PDF → MinerU parse → single-agent LLM
extract → structured KB`). In that service, an LLM sees the whole parsed paper in one call
and emits one JSON object, then a separate resolver/validator pass checks it. Here, **you
are that single agent, and there is no separate pass after you** — you read the PDF
directly (no block-indexed parser, no database), so building an honest locator and keeping
every cross-node id consistent is your job, done in the same reasoning pass as the
extraction itself.

## Workflow

1. **Get the paper.** PDF uploaded → read it directly, page by page, or via
   `/mnt/skills/public/pdf-reading/SKILL.md` for a long one. arXiv link → fetch full
   text/HTML if available, else the abstract page.
2. **Track page + section as you read.** For every page, note the section heading it falls
   under (`UNKNOWN_SECTION` if genuinely unclear — never guess one). This is what you'll
   anchor every extracted item to; see the `locator` shape in
   `references/node-schema.md#common-shapes`.
3. **Extract N0–N12 in order** against `references/node-schema.md` — the full per-node
   semantics, "what belongs here vs. the adjacent node" tables, and exact field names.
   Read it before drafting; it's the source of truth, not this file. Assign ids as you go
   (`C1,C2,…` challenges, `M1,M2,…` method components, `CO1,CO2,…` contributions,
   `RQ1,RQ2,…` or `RQ_INF_1,…` research questions) and keep them stable once assigned —
   later nodes reference earlier ones.
4. **Bibliography (optional, mechanical).** If the user wants the full citation list,
   capture the References-section text and split it with `scripts/split_citations.py`
   (one entry per `[N]` citation; author–year styles stay unsplit by design). This is a
   separate pass, not part of N3 — see the References section of the node schema.
5. **Self-verify** the completed draft against `references/self-verification.md` before
   output. Nothing else will catch a dangling id, a missing locator, or a one-line absence
   comment — that check is yours alone in this setup.
6. **Output** — markdown by default (below); switch to strict JSON when the user wants
   machine-readable output or plans to feed it into `paper-knowledge-service`-style tooling.

If one node proves intractable (corrupted page, unparseable table), degrade gracefully
rather than abandoning the digest: extract everything else, set that node's status
honestly, and say in one line which node degraded and why — same contract as the
production extractor's `parse_errors`. Metadata precedence and multi-paper dedup rules are
in the node schema's "Operational rules" section: user-supplied venue/year/area is never
overwritten, suspiciously short titles get re-checked against page 1, and batch digests
dedup on normalized titles (preprint vs camera-ready).

## The nodes

| Node | Captures |
|---|---|
| N0 | Bibliographic metadata: title, authors, abstract, DOI, arXiv id, pages, area |
| N1 | Problem/objective: inputs, outputs, constraints, a full-predicate objective |
| N2 | Motivation — why the problem matters (not prior-work failure) |
| N3 | 5–10 representative related works — what they DO |
| N4 | What those works FAIL to do, grounded in N3's citation keys |
| N5 | Problem-inherent challenges (not prior-work failure — see N4 vs N5 test) |
| N6 | Method overview + key_components (M-ids) + challenge→mechanism arguments + gaps |
| N7 | Contributions (CO-ids), each with a fine-grained type and testability |
| N8 | Research questions linking challenges, contributions, mechanisms; eval setup |
| N9 | Results per RQ, with result type and evidence strength |
| N10 | Author-acknowledged threats/limitations, categorized |
| N11 | Released artifacts (code/data/model/demo), with has_code/has_data/has_model |
| N12 | Whole-paper contribution-type classification (one enum, grounded rationale) |

Plus a top-level **claims** list — reviewer-relevant assertions collected across all nodes.

Full semantics, status rules, node-vs-node distinctions, and exact field names for every
row above live in `references/node-schema.md`.

## Core extraction discipline

The full rules are EX-01..EX-12 in `references/node-schema.md#extraction-rules`. The ones
that most commonly get skipped:

- **No hallucination, limited inference.** Unsupported → `status="NOT_FOUND"` + a real
  3-part `absence_comment`, not a shrug.
- **Near-verbatim for claims**, paraphrase only for overview-level summaries.
- **Every extracted item is anchored** (page + section, ideally + a short verbatim quote).
- **Ids cross-reference and must resolve** — no `challenge_id` pointing at a `C4` that was
  never created.
- **Every node appears, even empty ones** — `NOT_FOUND` + `[]` + absence_comment, never a
  silently missing key.
- **Field names are exact** — `objective` not `problem_statement`, `citation_key` not
  `citation`, etc. (full list of known bad renames in the rules section).

## Output format

### Markdown (default)

```
# Digest: <title>

## N0 Metadata
Title / Authors / Abstract / DOI / arXiv / Pages / Area — status, source

## N1 Problem Formulation
Objective: <full predicate>
Inputs / Outputs / Constraints
Status: FOUND (p.<n>, "<section>") | Source: extracted|inferred

## N2 Motivation
- <claim> (p.<n>, "<section>")

## N3 Related Works
- [<citation_key>] <approach_summary>

## N4 Prior Limitations
- <limitation_text> (affects: [<citation_key>, …])
Grounding check: true|false

## N5 Challenges
- C1: <text> (p.<n>)
Conflation check: true|false

## N6 Methodology
Overview: <text>
Key components: M1 <name> — <text>, …
Challenge arguments: C1 ← [M1, M2]: <argument_text>
Unaddressed challenges: [C3]

## N7 Contributions
- CO1 [<contribution_type>, testable=<bool>, has_rq=<bool>]: <text>

## N8 Research Questions
- RQ1: <text> — evaluates [M1], addresses [C1], tests [CO1]
Datasets / Baselines / Metrics: <names>

## N9 Results
- RQ1 → <result_text> [<result_type>, <evidence_strength>, answered=<bool>]

## N10 Threats
- t1 [<category>]: <description> (mitigation: <text|none>)

## N11 Artifacts
- a1 [<type>]: <url|"promised, no url"> (<label>)
has_code / has_data / has_model: <bool, bool, bool>

## N12 Contribution Type
value: <enum>
rationale: <text grounded in specific paper content>

## Claims
- <claim text> — evidence: <summary>

## References  (optional — on request; via scripts/split_citations.py)
[1] <citation> …
```

For any node with `status != FOUND`, show the status and the full 3-part `absence_comment`
instead of (or alongside) the empty content — don't just leave the section blank.

### Strict JSON (on request)

One JSON object with EXACTLY these top-level keys, nothing else, no markdown fences, no
preamble (EX-06/EX-07):

```
N0_Metadata, N1_ProblemFormulation, N2_Motivation, N3_RelatedWorks, N4_PriorLimitations,
N5_Challenges, N6_Methodology, N7_Contributions, N8_ResearchQuestions, N9_Results,
N10_Threats, N11_Artifacts, N12_ContributionType, claims
```

Per-field shapes are the field listings in `references/node-schema.md` — this is the same
shape the original service's database expects, so JSON-mode output is drop-in compatible
with `paper-knowledge-service`-style downstream tooling. If the user wants the
bibliography too, append `references: list[str]` as an extra top-level key (the production
DB stores it alongside, not inside, the node blob).

## Hand-off

- **Reconstruct or write** a paper from this digest → `pengsida-paper-writer`
  (`references/digest-paper.md`, `paper-archetypes.md`).
- **Compare two papers** → digest both, then align node-by-node (`pengsida-paper-writer`'s
  `comparison.md` shows the method).
- **Review** → the `claims` list is ready-made reviewer ammunition, especially any claim
  whose evidence traces back to an `N9` result with `evidence_strength="weak"` or
  `"missing"`. `N6.unaddressed_challenges` and `N10.threats` are also direct reviewer
  ammunition — hand the whole digest to `se-paper-reviewer` or `pengsida-stage-reviewer`
  rather than re-deriving these by re-reading the paper.

## Optional fast pass for very long papers

`scripts/digest_paper.py <paper.txt>` gives a heuristic, dependency-free skeleton — mainly
useful as a quick cross-check on your own N12 call (its classifier was tuned across 28 AI +
13 SE award papers, ~71% archetype-family accuracy) or as a starting outline before the
full read on a very long paper. It only populates N0/N1/N2/N4/N5/N6/N7/N9/N11/N12 (no N3,
N8, N10, no locators, no ids beyond a flat C/M/CO numbering) — never treat its output as a
finished digest. The direct read in step 3 above is the primary path; this script is a
sanity-check aid, not a substitute for it.

## Self-evaluation (encode→decode recovery)

The N1–N12 node semantics were tuned by a round-trip test: encode a paper to N1–N12, decode
the digest back to an abstract (via the `pengsida-paper-writer` decoder), and measure how
much survives. On 28 award papers the loop recovers ~0.87 overall (content 0.95, node
coverage 0.95, contribution-type 0.71). The N12 classifier rules (headline-aware
dataset/benchmark/position; proof-gated theory; method-body capture so dense abstracts keep
their signature terms) come from fixing the failures that test surfaced. See the pengsida
bundle's `roundtrip-recovery.md`.

## Cross-domain validation (AI + SE)

Also round-trip tested on 13 verified software-engineering best papers (ICSE/FSE/ASE/
ISSTA/OOPSLA/PLDI). Combined recovery ~0.85; content and node structure transfer cleanly
across domains, and N12 gained SE-aware rules (a paper that *evaluates* fine-tuned models
isn't *building* one; testbed-style benchmark introductions; tool papers whose evaluation
uses study words stay `system`). See the pengsida bundle's `roundtrip-se.md`.
