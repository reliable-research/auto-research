# N0–N12 Node Schema — full semantics

Source of truth for every field name, status rule, and node distinction. This is a direct
port of a production paper-knowledge-extraction service's single-agent LLM extraction
prompt (rules EX-01..EX-12 + thirteen per-node specs, reconstructed from Pydantic). Field
names below are exact — do not rename them for readability (see EX-12).

The one thing the production service had that you don't: a MinerU parser that pre-splits
the PDF into indexed blocks, and a resolver stage that runs after you to auto-compute
cross-references. You read the PDF directly, so the **locator** is adapted (see below) and
**cross-node ID consistency is done in the same pass as extraction, by you** (EX-09).

## Table of contents

1. [Common shapes](#common-shapes) — Source, FieldPresence, Locator, AbsenceComment, Claims
2. [EX-01..EX-12 — extraction rules that apply to every node](#extraction-rules)
3. [N0 — Metadata](#n0)
4. [N1 — Problem Formulation](#n1)
5. [N2 — Motivation](#n2)
6. [N3 — Related Works](#n3)
7. [N4 — Prior Limitations](#n4)
8. [N5 — Challenges](#n5)
9. [N6 — Methodology](#n6)
10. [N7 — Contributions](#n7)
11. [N8 — Research Questions](#n8)
12. [N9 — Results](#n9)
13. [N10 — Threats / Self-Limitations](#n10)
14. [N11 — Artifacts](#n11)
15. [N12 — Contribution Type](#n12)
16. References (bibliography) — separate mechanical pass
17. Operational rules from the production pipeline — graceful degradation, metadata
    precedence, multi-paper dedup

---

## Common shapes

**Source** — trust level for every content field: `"extracted"` (verbatim/near-verbatim
from the paper) or `"inferred"` (your logical conclusion, only where a node spec explicitly
allows it).

**FieldPresence (status)** — `"FOUND"` | `"PARTIAL"` | `"NOT_FOUND"`. See EX-04.

**Locator** — adapted from the production `PaperLocator`. The original shape was
`{block_index_global, page_start, section_title}`, anchored to MinerU's block index. You
don't have block indices, so use:

```json
{"page": 4, "section_title": "3.2 Coverage-Guided Fuzzing", "quote": "the mutation engine perturbs tool-call arguments"}
```

- `page` — the PDF page number the content appears on.
- `section_title` — copy the visible heading exactly. If genuinely no heading governs this
  content, use `"UNKNOWN_SECTION"` — never guess one (EX-03).
- `quote` — optional, 6–12 words verbatim from the source, close to the extracted content.
  This is what lets a human (or you, later) re-find the exact spot — it's doing the job
  `block_index_global` did in the original schema. Include it whenever you can; omit only
  when the extracted content is a synthesis of a whole paragraph with no single anchor
  phrase.

**AbsenceComment** — required whenever `status != "FOUND"`. Exactly these three keys, each
a real sentence, not a fragment:

```json
{
  "what_missing": "The paper never states an explicit research question tied to RQ2's ablation.",
  "why_matters": "Without it, a reader cannot tell what claim the ablation in Table 4 is meant to support.",
  "implication": "Treat the ablation as evidence for the closest existing RQ (RQ1) rather than inventing a new one."
}
```

**ClaimEvidence** — `{type: "argument"|"experiment"|"citation"|"observation", text, source, location}`.

**ClaimItem** — a reviewer-relevant assertion, anywhere in the paper, worth surfacing to a
reviewer: `{text, evidence: [ClaimEvidence], source, location}`. Collect these as you go —
they become the top-level `claims` list, and they're what `se-paper-reviewer` and
`pengsida-stage-reviewer` use as ready-made reviewer ammunition. Bias toward capturing more
subjective/contestable claims rather than fewer, especially anything a limitation, a
contribution, or a strong result statement rests on.

---

## Extraction rules

These twelve rules apply to every node. They are not optional flavor text — a digest that
violates them (invented content, missing locators, one-line absence comments, renamed
fields, dangling ids) is a broken digest, not a stylistic variant.

**EX-01 — No hallucination; limited inference.** Don't invent content. Unsupported field →
`status="NOT_FOUND"` + a valid 3-part `absence_comment`. Otherwise `absence_comment=null`.
Inference is allowed ONLY where a node spec explicitly permits it (e.g. N1's objective, N8's
research questions). Any inferred content is tagged `source="inferred"` and anchored to the
best available supporting locator anyway — inferred doesn't mean unanchored.

**EX-02 — Verbatim phrasing for claims.** Claims and key statements: near-verbatim. Paraphrase
only for the high-level summary fields (`overview.text`, N0-style abstracts stay verbatim
too — see N0). Never paraphrase a claim into something softer or stronger than stated.

**EX-03 — Location discipline.** Every `source="extracted"` item needs a non-null locator.
`section_title` copies the heading exactly; `"UNKNOWN_SECTION"` if genuinely unclear, never
guessed.

**EX-04 — Status meanings.**
- `FOUND` — clearly present, sufficiently supported.
- `PARTIAL` — present but incomplete, ambiguous, weakly grounded, or only partly specified.
- `NOT_FOUND` — absent from the paper.

**EX-05 — Absence comment structure.** See the AbsenceComment shape above. All three fields
required whenever status isn't FOUND; each a specific sentence, not a fragment.

**EX-06 — Schema compliance.** The target shape is fixed (below, per node). Use `null` /
`[]` where appropriate, but never add keys and never remove keys.

**EX-07 — Output format (JSON mode only).** When asked for JSON: one JSON object, no
markdown fences, no explanation, no preamble. (Markdown-mode output, the default, is
covered in SKILL.md.)

**EX-08 — Locator discipline, adapted.** You see the whole paper. Tag your internal
reading with page + section as you go (see SKILL.md step 2) so every locator you emit is
real, not reconstructed after the fact.

**EX-09 — Cross-node id consistency is your job.** No resolver runs after you — check these
yourself before you output anything (also see `references/self-verification.md`):
- `N4.limitations[].affects_works` uses the same string form as `N3.works[].citation_key`.
- `N6.challenge_arguments[].challenge_id` references an id from `N5.challenges[].id`.
- `N6.challenge_arguments[].mechanism_components` references ids from `N6.key_components[].id`.
- `N6.unaddressed_challenges` is a subset of `N5.challenges[].id`.
- `N8.research_questions[].addresses_challenges` → `N5.challenges[].id`.
- `N8.research_questions[].tests_contributions` → `N7.contributions[].id`.
- `N8.research_questions[].evaluates_mechanisms` → `N6.key_components[].id`.
- `N9.results[].rq_id` matches an id in `N8.research_questions[].id`.

**EX-10 — Strict enum for N12.** `N12_ContributionType.value` is exactly one of: `empirical,
theoretical, system, tool, survey, position, dataset, benchmark, case_study, replication,
experience_report, unknown`.

**EX-11 — Empty nodes still need a top-level key.** Nothing to populate (e.g. no Threats
section) → `status="NOT_FOUND"` + 3-part `absence_comment` + the list field set to `[]`.
Never omit the node.

**EX-12 — Field-name discipline.** JSON/field names match this spec exactly (case-sensitive).
Forbidden renames seen in practice:
- `problem_statement` → wrong; it's `objective` (or `text` for the node-level summary).
- `motivation_items` → wrong; it's `motivations`.
- `citation` → wrong; it's `citation_key`.
- `description` on Challenge/Limitation → wrong; it's `text` / `limitation_text`.

If unsure of a field name, check the per-node field listing below — it's the source of
truth.

---

<a id="n0"></a>
## N0 — Metadata

Bibliographic identity from the title page region. These fields get referenced elsewhere
(e.g. by `se-paper-reviewer`, `pengsida-paper-writer`), so get them right.

**Fields:** `title` (str|null), `authors` (list[str]), `abstract` (str|null), `doi`
(str|null), `arxiv_id` (str|null), `num_pages` (int|null), `research_area` (str|null).

- `title` — full title, verbatim, usually the first block on page 1 before the byline.
- `authors` — human names only, in paper order. Strip affiliation markers, numbers,
  daggers, asterisks.
  - Good: `["Zihao Xu", "Junchen Ding", "Yiling Lou"]`
  - Bad: `["Zihao Xu¹", "Junchen Ding¹*"]` (kept the markers), `["Zihao Xu (UNSW)"]` (kept
    the affiliation)
  - `"Anonymous Authors"` / "omitted for review" → `["Anonymous"]`.
- `abstract` — verbatim, exactly as printed, no paraphrase, no heading text included. `null`
  if there's genuinely no Abstract section.
- `doi` — no URL prefix. Good: `"10.1145/3597926.3598001"`. Bad: `"https://doi.org/10..."`.
  `null` if absent — don't guess.
- `arxiv_id` — format `YYMM.NNNNN` or `subject-class/YYMMNNN`. `null` if absent.
- `num_pages` — total page count of the PDF.
- `research_area` — pick ONE from: `SE, AI/ML, Systems, Security, DB, PL, HCI, Theory, NLP,
  CV, Networking, Other`. `null` if genuinely unclear.

**Status:** FOUND requires both `authors` and `abstract` populated. PARTIAL if only one is.
NOT_FOUND if neither (unusual — malformed PDF or a poster). DOI/arxiv_id absence never
downgrades status.

---

<a id="n1"></a>
## N1 — Problem Formulation

**Fields:** `inputs` (list[str]), `outputs` (list[str]), `constraints` (list[str]),
`objective` (str|null) — plus the NodeBase common fields (`status, source, text, location,
absence_comment`).

### What N1 is NOT
Not a general background problem statement, not motivation, not a prior-work limitation,
not a challenge list.

### What N1 captures
The task, in formulation terms: what it is, what goes in, what comes out, what constraints
a valid solution must satisfy, and what objective the method aims to achieve.

- `objective` — **given inputs/outputs/constraints, what specific GOAL does the method aim
  to achieve?** The "what does this paper try to do" answer, read in isolation.

  **Self-check before committing the objective.** Reading ONLY the objective, can a
  reviewer guess all three: (1) what KIND of task — testing / classification / synthesis /
  measurement / proof / benchmark / extraction / …; (2) what DOMAIN — LLM agents / web apps
  / OS kernels / DB queries / ICS networks / …; (3) what OUTCOME shape — a report / a
  labeled dataset / new vulnerabilities / a deployed system / a proven theorem / …? If any
  of the three is unclear, rewrite it.

  **GOOD** (full predicate, all three dimensions land):
  - "detect MAS-specific functional failures via coverage-guided fuzzing of agent task
    execution"
  - "extract a view-based access-control policy as SQL view definitions from a
    Ruby-on-Rails web app, enabling external enforcement without rewriting the app"
  - "evaluate prompt-injection defenses for LLM agents across 97 user tasks and 629
    security cases spanning email/banking/Slack/travel environments"

  **BAD — categorically rejected:** `"evaluate"`, `"benchmark"`, `"detect"`, `"generate"`
  (bare verb); `"benchmark and evaluate"` (verb conjunction, no object); `"improve
  performance"` (no domain, no object); `"build a better system"` (no domain); `"propose a
  new method"` (describes the contribution, not the task).

  If you can't construct a full predicate from the visible text, infer one from the
  abstract/title with `source="inferred"` and a 1-sentence absence_comment.

- `inputs`/`outputs` — **external only**: available BEFORE the method begins / the FINAL
  results the task aims to produce. Not intermediate artifacts one method component passes
  to another. List at most 3–5 concrete items each.

### Inference rule
Explicit formulation → `source="extracted"`. No explicit full formulation, but reliably
reconstructible from task description, method goal, notation, examples, or eval setup →
you MAY infer with `source="inferred"`, staying conservative and closely grounded. Never
turn motivation, prior limitations, or challenges into the formulation.

### Where these statements actually belong (not N1)
| Statement | Belongs to |
|---|---|
| "Existing methods are insufficient..." | N4 |
| "This problem is important because..." | N2 |
| "A major challenge is..." | N5 |

---

<a id="n2"></a>
## N2 — Motivation

**Node field:** `motivations: list[MotivationItem]`.
**MotivationItem fields:** `motivation_text` (str|null), `source`, `location`, `evidence:
list[ClaimEvidence]`.

Answers "why is this problem worth solving?" Each item is itself a claim — near-verbatim
`motivation_text`, `evidence=[]` if none present. Do NOT place prior-work failures here.

| Statement | Belongs to |
|---|---|
| "Software bugs cost the US economy $300B/year." | N2 (motivation) |
| "Existing fuzzers cannot handle stateful protocols." | N4 (prior limitation) |
| "State-space explosion makes exhaustive testing intractable." | N5 (inherent challenge) |

---

<a id="n3"></a>
## N3 — Related Works

**Node field:** `works: list[RelatedWork]`.
**RelatedWork fields:** `citation_key` (str), `approach_summary` (str), `source`, `location`.

Extract the **5–10 most representative** prior works explicitly discussed (fewer if fewer
than 5 are discussed — don't pad with loosely related works). N3 is what prior works DO;
never their limitations (that's N4).

- `citation_key` — the citation marker EXACTLY as printed (`"[12]"`, `"[Smith et al.,
  2021]"`, `"(Jones 2020)"`). N4 will reference this string, so get it exact.
- `approach_summary` — 1–2 concise sentences on what the work does.
- Prefer works discussed in Introduction / Motivation / Related Work. A bare parenthetical
  citation with no description doesn't count.

---

<a id="n4"></a>
## N4 — Prior Limitations

**Node fields:** `limitations: list[Limitation]`, `grounding_check: bool`.
**Limitation fields:** `limitation_text` (str), `affects_works` (list[str]), `source`,
`limitation_type` (enum: `scalability|precision|recall|generalizability|efficiency|
usability|theoretical|ethical|other`, optional), `location`, `evidence: list[ClaimEvidence]`.

What prior works FAIL to do, as explicitly claimed by the paper. Always `source="extracted"`
— never infer a limitation. Err toward extracting MORE subjective claims here rather than
fewer; each is a high-priority claim.

**Grounding rule (computable):** citation marker present (same string form as an
`N3.works[].citation_key`) → `affects_works=[those keys]`. No citation marker, or a general
limitation discussion not tied to specific prior work → `affects_works=[]`. Never invent a
citation. Set `grounding_check=True` **iff every** limitation has at least one entry in
`affects_works`.

**N4 vs N5 — the test:** if the statement says what a previous tool/method CANNOT do → N4.
If it's about why the problem is hard regardless of existing tools → N5.

| Statement | Belongs to |
|---|---|
| "Existing tools fail to handle multi-threaded inputs." | N4 (prior failure) |
| "Multi-threaded execution produces non-deterministic interleavings." | N5 (inherent challenge) |

---

<a id="n5"></a>
## N5 — Challenges

**Node fields:** `challenges: list[Challenge]`, `conflation_check: bool`.
**Challenge fields:** `id` (str, "C1","C2",…), `text` (str), `source`, `location`,
`evidence: list[ClaimEvidence]`.

Problem-inherent obstacles ANY valid solution must overcome — about the PROBLEM, not
weaknesses of earlier methods. Assign `id`s sequentially in the order challenges appear.
Text should be concise, close to the paper's wording. Set `conflation_check=True` iff every
challenge is genuinely distinct (no near-duplicates merged into one item).

Same N4-vs-N5 test as above applies here.

---

<a id="n6"></a>
## N6 — Methodology

**Node fields:** `overview: MethodOverview|null`, `key_components:
list[MethodKeyComponent]`, `challenge_arguments: list[ChallengeArgument]`,
`unaddressed_challenges: list[str]`.

Three parts, never merged:

**`overview`** (`{source, text, location}`) — one paragraph, what the method DOES
technically.

**`key_components`** — the method's main pieces. `{id: "M1","M2",…, name: short noun
phrase, text: brief description, source, location}`. **Assign all `key_components` ids
BEFORE populating `challenge_arguments`** — the latter's `mechanism_components` may only
reference ids that already exist here.

**`challenge_arguments`** — how the authors ARGUE the method addresses challenges (a
reported claim, not your own evaluation). `{source, challenge_id: must reference an N5 id,
argument_text: near-verbatim, mechanism_components: list of key_components ids or [] if
the argument is whole-method-level, location}`. Never invent a challenge–method link.

**`unaddressed_challenges`** — N5 ids the method does NOT address, or only partially. A
subset of `N5.challenges[].id`.

---

<a id="n7"></a>
## N7 — Contributions

**Node field:** `contributions: list[Contribution]`.
**Contribution fields:** `id` ("CO1","CO2",…), `text`, `source`, `contribution_type` (enum:
`technical_artifact|empirical_finding|conceptual_framework|dataset|tool|theoretical_result`),
`is_testable` (bool), `has_rq` (bool — true if an N8 RQ tests this contribution), `location`.

The CORE CLAIM of what the paper contributes, close to the paper's wording — not procedural
descriptions of how the method works (steps, pipelines, implementation process). Don't
invent novelty claims the paper doesn't explicitly assert.

Note: this `contribution_type` is a **per-contribution** fine-grained taxonomy, distinct
from N12 which classifies the WHOLE PAPER with a single different enum.

---

<a id="n8"></a>
## N8 — Research Questions

**Node fields:** `research_questions: list[ResearchQuestion]`, `datasets:
EvalEntityGroup|null`, `baselines: EvalEntityGroup|null`, `metrics: EvalEntityGroup|null`.

**ResearchQuestion fields:** `id` ("RQ1","RQ2",… if explicit; "RQ_INF_1",… if inferred),
`text`, `source`, `rq_source` (`"explicit"|"inferred"`, mirrors `source`),
`evaluates_mechanisms` (list of N6 `key_components` ids, `[]` if not tied to specific
components), `addresses_challenges` (list of N5 ids), `tests_contributions` (list of N7
ids), `answered_by_experiment` (short description), `location`.

**Inference rule:** RQs not explicitly stated but clearly inferable from evaluation
headings, subsection structure, or repeated evaluation goals → `source="inferred"`,
`id` prefix `RQ_INF_`. Still anchor to the best supporting locator.

**EvalEntityGroup** (`datasets`/`baselines`/`metrics`) — `{names: list[str], source,
location}`. Split multiple entities into separate list items — don't bundle "PyTorch,
TensorFlow, JAX" as one string.

---

<a id="n9"></a>
## N9 — Results

**Node field:** `results: list[Result]`.
**Result fields:** `rq_id` (must match an N8 id), `source`, `result_text` (factual: metric,
dataset, value, comparison — no evaluative language), `result_type` (enum:
`quantitative|qualitative|case_study|user_study|theoretical_proof`), `evidence_strength`
(enum: `strong` = quantitative with statistical testing, `moderate` = quantitative without
testing, `weak` = qualitative only, `missing` = claim made but no data), `rq_answered`
(bool — conclusively answered vs partial/inconclusive), `location`.

Every result links to an `rq_id`. Prefer concrete numbers when present. Qualitative-only
findings: report factually, near-verbatim, no hype or generic praise. Never hallucinate
results from future-work, discussion, or unsupported claims.

---

<a id="n10"></a>
## N10 — Threats / Self-Limitations

**Node field:** `threats: list[ThreatItem]`.
**ThreatItem fields:** `threat_id` ("t1","t2",…), `category` (enum: `internal` =
confounders in the study itself, `external` = generalisability/scope, `construct` =
operationalisation of concepts, `conclusion` = statistical/inferential validity,
`reproducibility` = replication blockers, `scope` = explicit out-of-scope statements,
`other`), `description` (verbatim/near-verbatim, ≥10 chars), `mitigation` (str|null,
author-stated only), `source`, `location`.

Only limitations the AUTHORS EXPLICITLY acknowledge (typically a Threats to
Validity/Limitations/Discussion section). Reviewer-inferred limitations don't belong here.
General-knowledge weaknesses ("LLMs hallucinate") only count if the authors themselves
invoke it as a limitation of their own work.

No threats section → `status="NOT_FOUND"` + 3-part `absence_comment` + `threats=[]`. The
comment should note the absence itself is reviewer-relevant.

---

<a id="n11"></a>
## N11 — Artifacts

**Node fields:** `artifacts: list[ArtifactItem]`, `has_code` (bool), `has_data` (bool),
`has_model` (bool).
**ArtifactItem fields:** `artifact_id` ("a1","a2",…), `type` (enum:
`code_repo|dataset|model|demo|supplement|docker_image|other`), `url` (str — `""` if
promised but no URL visible, e.g. "code will be released upon publication"; note this in
`absence_comment`), `label` (str|null, human-readable name), `accessible` (null in v1 — no
live URL probing), `location`.

`has_code`/`has_data`/`has_model` = true iff at least one artifact has that `type`.
**Strictness:** one `code_repo` artifact labeled "code + data" does NOT set `has_data=true`
unless a separate `dataset` artifact exists — use multiple artifact entries for a repo that
hosts multiple things.

Nothing released → `status="NOT_FOUND"` + `absence_comment` + `artifacts=[]` +
all three flags `false`. This is reviewer-relevant signal, not a gap to paper over.

**Status:** FOUND = every promised artifact has a concrete URL. PARTIAL = at least one has
`url=""`. NOT_FOUND = nothing mentioned.

---

<a id="n12"></a>
## N12 — Contribution Type

**Fields:** `value` (enum, see below), `rationale` (str, ≥10 chars, 1–2 sentences), `source`.

Single classification of the WHOLE paper — "which CfP category would this most naturally
be filed under?" One enum value, not a list. Distinct from N7's per-contribution taxonomy.

**Enum:** `empirical` (measurement/empirical study of an existing phenomenon), `theoretical`
(formal proof/analysis), `system` (designed+implemented a non-trivial system), `tool`
(released a usable tool — overlaps with `system`; prefer `tool` when artifact release is
central), `survey` (literature review), `position` (opinion/vision/call-to-action),
`dataset` (primary contribution is a new dataset), `benchmark` (primary contribution is a
new evaluation benchmark), `case_study` (single-case in-depth study, no broad empirical
claim), `replication` (replicates prior work), `experience_report` (industrial
experience/lessons learned), `unknown` (genuinely unclear — explain in `rationale`).

**Disambiguation hints:**
- Builds a system AND releases it as a downloadable tool → prefer `tool` (more specific).
- Releases code alongside a NEW METHOD/SYSTEM as the main contribution → `system`, not `tool`.
- Measurement study with a published dataset → `empirical` if the study is the main
  contribution, `dataset` if the dataset is.
- "We compared 10 LLMs on benchmark X" → `empirical` (it's a study).
- "We introduce benchmark X containing 1000 tasks" → `benchmark`.

**Good rationale:** "The paper introduces Flare, a coverage-guided fuzzing framework for
LLM-based MAS, and evaluates it on 16 open-source apps. The main contribution is the
released testing framework, not a measurement study." — cites specific paper content.

**Bad rationale (circular, reject):** "This paper is a tool because it introduces a tool."

Decide by what N9 (the results) actually validate, not by the opening verb of the abstract.

---

## References (bibliography) — separate mechanical pass

In the production pipeline the bibliography is NOT part of the LLM extraction — the worker
captures the raw References-section text separately and stores it on
`Extraction.references` as one entry per citation. Keep the same separation here: don't
spend extraction effort restating the bibliography inside N3 (N3 stays 5–10 *discussed*
works), and don't drop the bibliography either.

- PDF extraction usually collapses the whole bibliography into a few giant text chunks.
  `scripts/split_citations.py` recovers one entry per citation (splits on `[N]` markers,
  drops "References"/"Bibliography" heading lines, strips trailing publication footers like
  "Vol. 1, No. 1, Article ..."). No `[N]` markers (author–year style) → it deliberately
  returns the text unsplit rather than guessing boundaries.
- In markdown output, `## References` is an optional final section — include it when the
  user wants the full citation list, omit for a pure argument-chain digest.
- In JSON mode, the strict 14-key contract above is the LLM-output contract; `references:
  list[str]` may be appended as a 15th top-level key when the user wants it, mirroring how
  the production DB stores it alongside (not inside) the node blob.

---

## Operational rules from the production pipeline

**Graceful degradation (from the extractor).** In production, a Pydantic failure on one
node is recorded in `parse_errors` and extraction continues — partial extraction beats
nothing. Apply the same contract: if one node of the paper is genuinely intractable (e.g.
a corrupted page, an unparseable table the results live in), don't abandon the digest.
Extract everything else, set that node's status honestly (PARTIAL/NOT_FOUND with a real
absence_comment), and tell the user which node degraded and why, in one line.

**Metadata precedence (from the worker's N0 promotion).**
- Title: prefer the longer, more plausible title. PDF text extraction sometimes truncates
  a title to the first author's name ("Mark S." instead of "Capability Myths Demolished")
  — if what you read as the title looks like a person's name or a fragment, re-check the
  first page before committing N0.title.
- User-supplied metadata wins: if the user already told you the venue, year, or research
  area, never overwrite it with your own inference — the LLM-suggested `research_area`
  only fills a blank, exactly as in production.

**Multi-paper dedup (from `dedup.py`).** When digesting a batch, two files can be the same
paper (arXiv preprint vs camera-ready — different bytes, same title). Compare normalized
titles — lowercase, whitespace-collapsed, edge punctuation trimmed, and deliberately
nothing more aggressive: "Survey on X" and "A Survey of X" ARE different papers, so only
mechanical formatting noise gets erased. On a match, flag the duplicate and digest once
rather than producing two silently diverging digests.
