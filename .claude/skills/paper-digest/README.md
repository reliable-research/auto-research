# paper-digest

Decompose a research paper PDF into a structured N0–N12 knowledge digest (metadata,
problem, motivation, related work, prior limitations, inherent challenges, methodology
with challenge→mechanism mapping, contributions, research questions, results, threats,
artifacts, a whole-paper contribution-type classification, and a claims list).

v2: every node now carries the full evidence discipline of the production service this
schema is ported from — status (FOUND/PARTIAL/NOT_FOUND), source (extracted/inferred), a
page+section locator, a 3-part absence_comment when content is missing, and cross-node ids
that must resolve (no more free-text nodes with no way to check them).

Pairs with `pengsida-paper-writer` (reconstruct/write/compare from a digest) and
`se-paper-reviewer` / `pengsida-stage-reviewer` (review using the digest's claims list and
unaddressed-challenges/threats as reviewer ammunition).

## Files
- `SKILL.md` — workflow, node overview, output formats, hand-off
- `references/node-schema.md` — full N0–N12 semantics + EX-01..EX-12 extraction rules
  (source of truth for field names and status rules)
- `references/self-verification.md` — checklist to run over your own draft before output
  (adapted from the production service's V-01/02/04/08/10/11/12 validators, which you don't
  have to run for you here)
- `scripts/digest_paper.py` — heuristic skeleton generator, optional fast pass /
  cross-check only (`python3 scripts/digest_paper.py paper.txt`)
- `scripts/split_citations.py` — bibliography splitter (port of the service's `refs.py`):
  one entry per `[N]` citation, heading/footer stripping, author–year left unsplit
  (`python3 scripts/split_citations.py refs.txt [--json]`)

## What changed from v1
v1's `node-schema.md` was a compact hand-written summary of this schema, with a heuristic
script as the primary extraction path. v2 replaces it with a direct port of the actual
production LLM extraction prompt (rules + all 13 per-node specs + schema field listings),
now uploaded by the user as `digest_paper-master`. The heuristic script is demoted to an
optional aid — a single careful LLM read against the full node spec is materially higher
fidelity than the script, which is what the production service uses an LLM for in the
first place.

Also ported from the pipeline layer (worker/extractor/refs/dedup, not just the prompt):
bibliography as a separate mechanical pass (`split_citations.py` + `references` output),
graceful per-node degradation (one broken node never kills the digest), metadata
precedence (user-supplied venue/year/area never overwritten; short/truncated titles
re-checked), and normalized-title dedup for batch digests.

## Credit
The N0–N12 schema, extraction rules (EX-01..EX-12), and field shapes are ported from a
paper-knowledge-extraction service: `PDF → MinerU parse → single-agent LLM extract →
structured KB`, with a separate resolver/validator pass. This skill adapts it into a
portable, dependency-free front-end — you're the single agent, reading the PDF directly and
self-verifying, with no parser or resolver behind you.
