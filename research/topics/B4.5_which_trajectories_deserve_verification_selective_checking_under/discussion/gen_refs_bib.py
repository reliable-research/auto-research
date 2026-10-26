#!/usr/bin/env python3
"""Script-generate refs.bib from reference_candidates.jsonl's `selected` records.
Per goal.md Phase F: 'refs.bib script-generated from the jsonl; hand-typing banned.'
Run: python3 gen_refs_bib.py
"""
import json
import re

SRC = "reference_candidates.jsonl"
OUT = "refs.bib"


def bibtex_escape(s):
    if s is None:
        return ""
    return s.replace("&", r"\&").replace("_", r"\_").replace("%", r"\%")


def guess_entrytype(rec):
    venue = (rec.get("venue") or "").lower()
    if venue in ("acl",):
        return "inproceedings"
    if venue in ("iclr", "neurips", "icml", "acl (nips wksp)"):
        return "inproceedings"
    if "wksp" in venue or "workshop" in venue:
        return "inproceedings"
    if venue == "openreview":
        return "misc"
    return "article"  # default: arXiv preprint


def build_entry(rec):
    key = rec["key"]
    title = bibtex_escape(rec.get("title", ""))
    year = rec.get("year", "")
    venue = rec.get("venue", "") or ""
    ids = rec.get("ids", {}) or {}
    url = rec.get("url", "") or ""
    arxiv = ids.get("arxiv")
    openreview = ids.get("openreview")
    doi = ids.get("doi")

    etype = guess_entrytype(rec)
    fields = []
    authors = rec.get("authors")
    if authors:
        if isinstance(authors, list):
            authors = " and ".join(authors)
        fields.append(("author", f"{{{authors}}}"))
    fields.append(("title", f"{{{title}}}"))
    fields.append(("year", f"{{{year}}}"))
    if etype == "inproceedings":
        fields.append(("booktitle", f"{{{venue}}}"))
    elif etype == "misc":
        fields.append(("howpublished", "{OpenReview}"))
    else:
        fields.append(("journal", f"{{{venue}}}" if venue and venue != "OpenReview" else "{arXiv preprint}"))
    if arxiv:
        fields.append(("eprint", f"{{{arxiv}}}"))
        fields.append(("archivePrefix", "{arXiv}"))
    if rec.get("note"):
        fields.append(("note", f"{{{rec['note']}}}"))
    elif openreview:
        fields.append(("note", f"{{OpenReview id: {openreview}}}"))
    if doi:
        fields.append(("doi", f"{{{doi}}}"))
    if url:
        fields.append(("url", f"{{{url}}}"))

    lines = [f"@{etype}{{{key},"]
    for k, v in fields:
        lines.append(f"  {k} = {v},")
    lines[-1] = lines[-1].rstrip(",")
    lines.append("}")
    return "\n".join(lines)


def main():
    entries = []
    with open(SRC) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            if rec.get("verdict") == "selected":
                entries.append(rec)

    entries.sort(key=lambda r: r["key"])

    with open(OUT, "w") as f:
        f.write("% Auto-generated from reference_candidates.jsonl's `selected` records.\n")
        f.write("% Do not hand-edit -- regenerate via gen_refs_bib.py (goal.md Phase F discipline).\n\n")
        for rec in entries:
            f.write(build_entry(rec))
            f.write("\n\n")

    print(f"Wrote {len(entries)} entries to {OUT}")


if __name__ == "__main__":
    main()
