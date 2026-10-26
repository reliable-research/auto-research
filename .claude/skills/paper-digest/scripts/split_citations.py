#!/usr/bin/env python3
"""
split_citations.py — split a concatenated References section into one entry
per citation.

Direct port of the production service's `refs.py`. PDF extraction usually
returns the entire bibliography as one or a few giant text chunks; this
recovers a real ordered list so the digest's `references` output has one
entry per citation.

Handles numbered citations: `[1] author... [2] author...`. Falls back to
returning the input unchanged when no `[N]` markers are found (author-year
style is left untouched — better one ugly blob than wrong splits).

Usage:
    python3 split_citations.py refs.txt          # one citation per line
    python3 split_citations.py refs.txt --json   # JSON list
    cat refs.txt | python3 split_citations.py -  # read stdin
"""
from __future__ import annotations

import json
import re
import sys

_CITATION_MARKER = re.compile(r"\[(\d+)\]")
_FOOTER_PATTERN = re.compile(
    r",?\s*(?:Vol\.\s*\d|Article\s*\.|Publication date|"
    r"Proceedings of the \w+ ACM)",
    re.IGNORECASE,
)
_HEADING_WORDS = {"references", "bibliography", "works cited"}


def _is_heading_only(text: str) -> bool:
    return text.strip().rstrip(":.").lower() in _HEADING_WORDS


def split_citations(raw_blocks: list[str]) -> list[str]:
    """Turn raw 'References' text chunks into one entry per citation.

    Steps:
      1. Drop heading-only entries ("References", "REFERENCES", "Bibliography").
      2. Concatenate the rest so a citation split across chunks reunites.
      3. Split on `[N]` markers, keeping the marker as the chunk's prefix.
      4. Strip publication footers ("Vol. 1, No. 1, Article ...") from the
         last chunk — a typical PDF artifact.
    """
    cleaned = [t.strip() for t in raw_blocks if t and t.strip()]
    cleaned = [t for t in cleaned if not _is_heading_only(t)]
    if not cleaned:
        return []

    joined = " ".join(cleaned)
    markers = list(_CITATION_MARKER.finditer(joined))
    if not markers:
        # No [N] markers — return the original (non-heading) chunks rather
        # than guess at author-year boundaries.
        return cleaned

    citations: list[str] = []
    for i, m in enumerate(markers):
        start = m.start()
        end = markers[i + 1].start() if i + 1 < len(markers) else len(joined)
        chunk = joined[start:end].strip()
        # Trim trailing publication footer off the last citation
        if i == len(markers) - 1:
            footer = _FOOTER_PATTERN.search(chunk)
            if footer:
                chunk = chunk[: footer.start()].rstrip(" .,;")
        if chunk:
            citations.append(chunk)
    return citations


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    src = sys.argv[1]
    text = sys.stdin.read() if src == "-" else open(
        src, encoding="utf-8", errors="replace").read()
    # Treat blank-line-separated chunks as the raw blocks
    blocks = [b for b in re.split(r"\n\s*\n", text) if b.strip()]
    cites = split_citations(blocks)
    if "--json" in sys.argv:
        print(json.dumps(cites, indent=2, ensure_ascii=False))
    else:
        for c in cites:
            print(c)


if __name__ == "__main__":
    main()
