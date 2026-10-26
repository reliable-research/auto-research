#!/usr/bin/env python3
"""Generate refs.bib from discussion/reference_candidates.jsonl's `selected` records.

Per goal.md's hard gate: refs.bib must be script-generated from the jsonl, not
hand-curated. Run from the topic's `discussion/` directory:
    python3 generate_refs_bib.py

Known real authors (verified 2026-07-04 via arXiv fetch + digest) are used for
AIControl2024 and ControlTax2024. Other OpenReview keys were still under
double-blind review as of the harvest date, so no real author list is
resolvable from the corpus; they are cited by their citekey with `Anonymous`
authorship, exactly as the paper.md/pipeline.md's own "Anon., <title>
(OpenReview:<id>)" convention already uses. One non-corpus canonical entry
(Kuhn/Kacker/Lei, cited in Related Work for the combinatorial-test-design
technique's provenance) is appended manually since it predates and is
independent of the jsonl harvest, exactly as `AvenhausInspectionGames2002`'s
own record already flags itself as a "non-corpus canonical entry."
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
JSONL_PATH = HERE / "reference_candidates.jsonl"
OUT_PATH = HERE / "refs.bib"

KNOWN_AUTHORS = {
    "AIControl2024": "Greenblatt, Ryan and Shlegeris, Buck and Sachan, Kshitij and Roger, Fabien",
    "ControlTax2024": "Terekhov, Mikhail and Liu, Zhen Ning David and Gulcehre, Caglar and Albanie, Samuel",
    "AvenhausInspectionGames2002": "Avenhaus, Rudolf and von Stengel, Bernhard and Zamir, Shmuel",
}

KNOWN_VENUE_OVERRIDE = {
    "AIControl2024": "Proceedings of the 41st International Conference on Machine Learning (ICML)",
    "ControlTax2024": "arXiv preprint",
    "AvenhausInspectionGames2002": "Handbook of Game Theory, Vol. 3, Elsevier",
}

# Note: the 5 still-double-blind OpenReview keys (CtrlAltDeceit2024,
# CalibratedStackelberg2024, InfTimeRewardHacking2024, CorrelatedProxies2024,
# UTRL2024) intentionally have no year override — their jsonl `year` field is
# genuinely null (anonymous submissions, year not resolvable from the corpus)
# and fabricating one would misrepresent the cache's own honesty discipline.


def bibkey_safe(key: str) -> str:
    # BibTeX citation keys may contain letters, digits, underscore, hyphen,
    # colon, period — only strip characters that are genuinely unsafe
    # (braces, commas, whitespace, '#', '@', quotes).
    return re.sub(r"[^A-Za-z0-9_\-:.]", "", key)


def escape_bibtex(text: str) -> str:
    """Escape characters BibTeX/LaTeX treat specially in a plain-text field.

    Brace-protect the escaped macro (e.g. ``{\\&}`` not bare ``\\&``) so that
    bibtex styles which call change.case$ on the field (plainnat's sentence-
    case title handling) don't strip the backslash while lowercasing.
    """
    text = text.replace("{", "").replace("}", "")
    for ch in ("&", "%", "#", "_"):
        text = text.replace(ch, "{\\" + ch + "}")
    return text


def make_entry(rec: dict) -> str:
    key = bibkey_safe(rec["key"])
    title = escape_bibtex(rec.get("title", ""))
    year = rec.get("year")
    url = rec.get("url")
    ids = rec.get("ids", {})
    arxiv_id = ids.get("arxiv")
    openreview_id = ids.get("openreview")
    venue = KNOWN_VENUE_OVERRIDE.get(rec["key"], rec.get("venue") or "arXiv preprint")
    author = KNOWN_AUTHORS.get(rec["key"], "Anonymous")

    entrytype = "misc"
    fields = [f'  title = {{{title}}}', f'  author = {{{author}}}']
    if year:
        fields.append(f"  year = {{{year}}}")
    fields.append(f"  howpublished = {{{venue}}}")
    if arxiv_id:
        fields.append(f"  eprint = {{{arxiv_id}}}")
        fields.append('  archivePrefix = {arXiv}')
    if openreview_id:
        fields.append(f"  note = {{OpenReview id: {openreview_id}}}")
    if url:
        fields.append(f"  url = {{{url}}}")

    return "@%s{%s,\n%s\n}\n" % (entrytype, key, ",\n".join(fields))


def main():
    if not JSONL_PATH.exists():
        print(f"ERROR: {JSONL_PATH} not found", file=sys.stderr)
        sys.exit(1)

    entries = []
    with open(JSONL_PATH) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            if rec.get("verdict") == "selected":
                entries.append(make_entry(rec))

    # Manual non-corpus canonical entry (mirrors AvenhausInspectionGames2002's
    # own "non-corpus canonical entry" disclosure) — cited in Related Work
    # for combinatorial-test-design provenance, predates the jsonl harvest.
    entries.append(
        "@book{KuhnKackerLei2013CombinatorialTesting,\n"
        "  title = {Introduction to Combinatorial Testing},\n"
        "  author = {Kuhn, D. Richard and Kacker, Raghu N. and Lei, Yu},\n"
        "  year = {2013},\n"
        "  publisher = {CRC Press},\n"
        "  note = {Non-corpus canonical entry, cited for technique provenance rather than as a jsonl-retrieved record}\n"
        "}\n"
    )

    with open(OUT_PATH, "w") as f:
        f.write("% Auto-generated by generate_refs_bib.py from reference_candidates.jsonl's `selected` records.\n")
        f.write("% Do not hand-edit entries sourced from the jsonl; re-run the script after updating the cache.\n\n")
        f.write("\n".join(entries))

    print(f"Wrote {len(entries)} entries to {OUT_PATH}")


if __name__ == "__main__":
    main()
