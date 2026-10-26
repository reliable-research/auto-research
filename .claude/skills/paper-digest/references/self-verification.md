# Self-verification checklist

The production service runs four circuit-breaker validators (V-01, V-02, V-04, V-08) plus
three lighter node-specific checks (V-10, V-11, V-12) on the extractor's output *before* a
human ever sees it. Here, nothing runs after you — so run this checklist yourself against
your own draft digest before you output it. Fix violations in place; don't output a digest
that fails any of the "must" items below.

Treat this as a final pass over a completed draft, not a per-field interruption while
you're still reading the paper — extract first, then verify the whole thing at once.

## V-01 — Locator integrity
**Every item with `source="extracted"` and `status="FOUND"` has a non-null locator**
(`page` + `section_title`, ideally + `quote`). If you wrote something down as extracted but
can't point to where, either find the locator or downgrade the item to `inferred`/lower
status honestly.

## V-02 — Absence comment shape
**Every item with `status != "FOUND"` has a full 3-part `absence_comment`**
(`what_missing`, `why_matters`, `implication`), each a real sentence — not "N/A", not a
single word, not left blank. A one-line comment is a violation, not a shortcut.

## V-04 — ID consistency
Walk every cross-reference and confirm it resolves:
- [ ] `N4.limitations[].affects_works` values all appear in `N3.works[].citation_key`
- [ ] `N6.challenge_arguments[].challenge_id` values all appear in `N5.challenges[].id`
- [ ] `N6.challenge_arguments[].mechanism_components` values all appear in
      `N6.key_components[].id`
- [ ] `N6.unaddressed_challenges` is a subset of `N5.challenges[].id`
- [ ] `N8.research_questions[].addresses_challenges` values all appear in `N5.challenges[].id`
- [ ] `N8.research_questions[].tests_contributions` values all appear in `N7.contributions[].id`
- [ ] `N8.research_questions[].evaluates_mechanisms` values all appear in `N6.key_components[].id`
- [ ] `N9.results[].rq_id` values all appear in `N8.research_questions[].id`

A dangling id (referencing `C4` when only `C1`–`C3` exist) is a hard error — either the id
was mistyped or the referenced node/item was never actually created. Fix the source, not
the reference.

## V-08 — Confidence doesn't inflate under inference
The production resolver auto-downgrades any structural gap that touches an `inferred` node
so it can't be reported with `extracted`-level certainty. You don't have a separate gap
detector, but the underlying principle still applies: if `N6.unaddressed_challenges` or a
similar downstream claim rests on an `N5`/`N6`/`N8` item you marked `source="inferred"`,
say so plainly in the surrounding text rather than presenting it with the same confidence
as an extracted, citation-backed claim.

## V-10 — N10 self-consistency
`status="FOUND"` implies `threats` is non-empty. If you set FOUND with an empty list,
that's a bug — either populate it or the status should be PARTIAL/NOT_FOUND.

## V-11 — N11 self-consistency
- `status="FOUND"` implies `artifacts` is non-empty.
- `has_code` is true **iff** at least one artifact has `type="code_repo"` — recompute it
  from the actual list, don't just assert it.
- Same check for `has_data` ↔ `type="dataset"` and `has_model` ↔ `type="model"`.

## V-12 — N12 rationale quality
`rationale` is at least a real sentence (not "it's a tool because it's a tool") and cites
something concrete from the paper — a component name, an evaluation design choice, what
N9's results actually validate. Circular rationale is a rejection, not a style nitpick.

## General field-name spot check (EX-12)
Before finalizing, scan your draft for these specific known failure modes:
- `objective` (not `problem_statement`)
- `motivations` (not `motivation_items`)
- `citation_key` (not `citation`)
- `text` / `limitation_text` (not `description`, on Challenge/Limitation respectively)

If you renamed any field for readability while drafting, rename it back before output.

## Empty-node check (EX-11)
Every one of N0–N12 appears in your output, even nodes with nothing to say
(`status="NOT_FOUND"`, `absence_comment` filled in, list fields `[]`). Scan your draft for
any node you skipped entirely — that's the most common miss, especially N10/N11 when a
paper genuinely has no limitations section or releases nothing.
