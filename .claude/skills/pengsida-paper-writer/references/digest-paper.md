# Digest a Paper (N1–N12)

Before reconstructing, comparing, or reviewing a paper, decompose it into a structured
argument chain. This schema is adapted from a paper-knowledge-extraction service and was
validated by digesting real award papers (`digest-examples.md`, `comparison.md`). Use it to
turn an unstructured PDF/abstract into checkable parts, then map every claim you write back
to a node.

## The nodes

- **N0 metadata** — title, authors, venue, field.
- **N1 problem / objective** — the task: inputs, outputs, constraints, objective. The
  objective must be a full predicate (verb + object + qualifier) such that a reader can
  infer the task KIND, DOMAIN, and OUTCOME shape. Reject bare verbs ("evaluate", "detect").
- **N2 motivation** — why the problem matters (not prior-work failure).
- **N3 related works** — 5–10 representative prior works: what they DO.
- **N4 prior limitations** — what prior works FAIL to do (claims, grounded in N3 keys).
- **N5 challenges** — problem-inherent difficulty any solution must overcome (NOT prior
  failure). Keep N4 and N5 distinct — see `introduction.md`.
- **N6 methodology** — overview + key_components (M1, M2, …) + challenge_arguments mapping
  each N5 challenge to the components (M-ids) that address it; list unaddressed challenges.
- **N7 contributions** — core claims (CO1, …) with per-contribution type
  (technical_artifact / empirical_finding / conceptual_framework / dataset / tool /
  theoretical_result) and is_testable.
- **N8 research questions** — RQs linking challenges, contributions, mechanisms.
- **N9 results** — findings, each tied to an RQ where possible.
- **N10 threats / self-limitations**.
- **N11 artifacts** — released code / data / model / demo URLs (has_code/has_data/has_model).
- **N12 contribution type (whole paper)** — exactly one of:
  `empirical | theoretical | system | tool | survey | position | dataset | benchmark |
  case_study | replication | experience_report | unknown`, with a rationale citing specific
  paper content (no circular "it's a tool because it has a tool").

## How the skill uses a digest

1. **Reconstruct**: from N1/N5/N6/N7 pick the archetype (`paper-archetypes.md`), then draft
   the Abstract/Introduction so each sentence maps to a node (N1→task, N4/N5→challenge,
   N6→insight/method, N7→contribution, N9→results).
2. **Compare two papers**: digest both, then align node-by-node (`comparison.md`). Look for
   shared framing moves (e.g. dissolve-a-constraint) and divergent contribution shapes.
3. **Review**: a claim in the Abstract/Introduction with no supporting node (especially no
   N9 result) is an unsupported claim — flag it. N6 unaddressed_challenges and N10 threats
   are reviewer ammunition; pre-empt them.

## Relationship between N12 and the skill's archetypes

The skill's five archetypes map onto the digest's 11-value N12 enum:

- method/pipeline ↔ `system`
- efficiency/frontier ↔ `system`/`tool` with an efficiency headline (the digest captures the
  efficiency angle in N9 results, not N12)
- analysis/position ↔ `empirical` / `case_study` / `position` / `replication`
- resource/foundation ↔ `dataset` / `benchmark` / `tool`
- theory ↔ `theoretical`
- (`survey` and `experience_report` are digest categories the skill folds into
  analysis/position when they arise.)

Use N12 when you want the precise CfP-style filing; use the archetype when you want the
writing template. They agree on the contribution's nature; the archetype just adds the
how-to-write layer.

## Automating the digest

`scripts/digest_paper.py` produces an N1–N12 skeleton from a paper's text (heuristic
extraction; refine by hand against the node definitions above). For a production-grade
extractor, the uploaded `paper-knowledge-service` runs an LLM single-agent pass over the
parsed PDF — this skill's script is a lightweight stand-in for drafting and teaching.
