# /deerflow_review — review existing research drafts with the deer-flow research skills

**Goal:** for each target draft, produce a peer-review-quality structured review grounded in fresh
web research, using the two skills ported from `bytedance/deer-flow` (`skills/public/`, cloned
2026-08-23) into `.claude/skills/`:

- `deep-research` — systematic multi-angle web research methodology (broad exploration → deep dive
  → diversity/validation → synthesis check; never single-search, always current-year temporal
  qualifiers, fetch key sources in full).
- `academic-paper-review` — top-venue structured review: metadata → deep reading → claims ledger
  (claim/evidence/strength) → literature-context search → methodology assessment table (soundness,
  novelty, reproducibility, experimental design, statistical rigor, scalability, 1–5) →
  strengths/weaknesses with section references → questions for authors → literature positioning →
  Accept…Reject recommendation + contribution level + actionable suggestions.

**Targets** (default; args can override): the four active loop_r1 manuscripts
`research/topics/loop_r1_worldmodel_explorations/papers/ZW{1..4}_*/paper-draft.revised.md` (read
`experiment-spec.md` alongside; both are the CURRENT artifacts per `papers/README.md`).
For `research/topics/<CODE>_<slug>/` topics, the draft is `discussion/paper_draft.md`.

**Procedure per draft** (one self-contained background agent per draft, run in parallel):

1. Read the draft in full, byte one to end (Phase 1 of `academic-paper-review`); build the claims
   ledger.
2. Run the `deep-research` methodology for literature context: ≥5 targeted searches across angles
   (state of the art <current year>, method-twin nouns, benchmark/estimand, limitations/criticism,
   recent 2026 work), fetching the most relevant sources.
3. Verify any arXiv ids in ONE batched request
   (`curl -sL "https://export.arxiv.org/api/query?id_list=<id1>,<id2>,..."`) — never per-id loops
   (rate-ban); on 429 mark unverified, do not retry.
4. Write the full `academic-paper-review` output template to
   `<draft-folder>/deerflow_review_<YYYY-MM-DD>.md`, with a header naming both skills, the audit
   date, and every search run (including empty ones).
5. Never edit the draft itself; reviews are findings-only. Do not fabricate citations; unverifiable
   candidates go under "Citation debt (supervisor verify)".

**Supervisor duties:** verify each review file landed on disk and is complete (template sections
present, non-aspirational); summarize verdicts per draft; log nothing into frozen topic-root files.

