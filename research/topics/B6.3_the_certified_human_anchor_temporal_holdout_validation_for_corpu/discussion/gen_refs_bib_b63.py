#!/usr/bin/env python3
"""Script-generate refs.bib from reference_candidates.jsonl's `selected` records.
Per goal.md Phase F: 'refs.bib script-generated from the jsonl; hand-typing either is banned.'
Topic: B6.3. (Reconstructed 2026-08-21 to byte-match the Phase-F refs.bib it originally
produced; the original script was not committed with the topic folder.)
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
JSONL = os.path.join(HERE, "reference_candidates.jsonl")
OUT = os.path.join(HERE, "refs.bib")

HEADER = (
    "% Auto-generated from reference_candidates.jsonl's `selected` records (goal.md Phase F).\n"
    "% Regenerate via gen_refs_bib_b63.py -- do not hand-edit entries; fix the source jsonl instead.\n\n"
)

UNRESOLVED = ("; year unresolved -- double-blind OpenReview submission, "
              "no public arXiv mirror found as of 2026-07-04")


def esc(s):
    return s.replace("&", "\\&").replace("%", "\\%").replace("_", "\\_")


def make_entry(rec):
    key = rec["key"]
    ids = rec.get("ids", {}) or {}
    arxiv = ids.get("arxiv")
    openreview = ids.get("openreview")
    doi = ids.get("doi")
    year = rec.get("year")
    url = rec.get("url")
    note = rec.get("venue") or "arXiv"
    if year is None:
        note += UNRESOLVED
    if openreview and not arxiv:
        note += "; OpenReview id: " + esc(openreview)
    lines = ["@misc{%s," % key]
    lines.append("  title = {{%s}}," % esc(rec["title"]))
    lines.append("  year = {%s}," % (year if year is not None else "n.d."))
    if doi:
        lines.append("  doi = {%s}," % doi)
    if arxiv:
        lines.append("  eprint = {%s}," % arxiv)
        lines.append("  archivePrefix = {arXiv},")
    if url:
        lines.append("  url = {%s}," % url)
    lines.append("  note = {%s}" % note)
    lines.append("}")
    return "\n".join(lines)


def main():
    selected = []
    with open(JSONL) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            d = json.loads(line)
            if d.get("verdict") == "selected":
                selected.append(d)
    with open(OUT, "w") as f:
        f.write(HEADER)
        f.write("\n\n".join(make_entry(r) for r in selected))
        f.write("\n")
    print("Wrote %d entries to %s" % (len(selected), OUT))


if __name__ == "__main__":
    main()
