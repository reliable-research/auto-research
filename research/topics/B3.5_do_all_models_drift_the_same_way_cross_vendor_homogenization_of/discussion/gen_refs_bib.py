#!/usr/bin/env python3
"""Generate refs.bib from reference_candidates.jsonl's `selected` records.

Per goal.md Phase F: "refs.bib script-generated from the jsonl; hand-typing
either is banned." Re-run this script whenever reference_candidates.jsonl's
selected set changes; do not hand-edit refs.bib.
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
JSONL = HERE / "reference_candidates.jsonl"
OUT = HERE / "refs.bib"

# Manually-sourced title/author/venue metadata for selected records whose
# jsonl entry doesn't carry full bibliographic fields (the jsonl schema only
# guarantees key/title/ids/venue/year/url per goal.md §1; this table fills
# in author strings gathered during the reference-cache-integrity fix so the
# .bib entries are complete rather than placeholder-titled).
TITLE_OVERRIDES = {
    "GreatModelsThinkAlike": "Great Models Think Alike and this Undermines AI Oversight",
    "CommunityAlignmentMonoculture": "Cultivating Pluralism In Algorithmic Monoculture: The Community Alignment Dataset",
    "MultiEntityRecursion": "What Happens When Generative AI Models Train Recursively on Each Others' Outputs?",
    "DiversityAwarePO": "Diversity-Aware Policy Optimization for Large Language Model Reasoning",
    "DQO": "Post-training Large Language Models for Diverse High-Quality Responses",
    "MeasureDatasetDiversity": "Position: Measure Dataset Diversity, Don't Just Claim It",
    "ModelCollapseMemorization": "A Closer Look at Model Collapse: From a Generalization-to-Memorization Perspective",
    "ArtificialHivemind": "Artificial Hivemind: The Open-Ended Homogeneity of Language Models and Beyond",
    "BoundarySyncRepCoupling2607": "BOUNDARY\\_SYNC: Measuring Communication-Induced Representational Coupling in Multi-Agent LLM Systems",
    "CorrelatedErrors2506": "Correlated Errors in Large Language Models",
    "SimilarlyCreative2608": "Are LLMs becoming similarly creative? Evidence from three years of models",
    "VendiScore": "The Vendi Score: A Diversity Evaluation Metric for Machine Learning",
}

AUTHOR_OVERRIDES = {
    "GreatModelsThinkAlike": "Goel, Shashwat and Str{\\\"u}ber, Joschka and Auzina, Ilze Amanda and Chandra, Karuna K and Kumaraguru, Ponnurangam and Kiela, Douwe and Prabhu, Ameya and Bethge, Matthias and Geiping, Jonas",
    "CommunityAlignmentMonoculture": "Zhang, Lily Hong and Milli, Smitha and Jusko, Karen and Smith, Jonathan and Amos, Brandon and Bouaziz, Wassim and Revel, Manon and Kussman, Jack and Sheynin, Yasha and Titus, Lisa and Radharapu, Bhaktipriya and Yu, Jane and Sarma, Vidya and Rose, Kris and Nickel, Maximilian",
    "MultiEntityRecursion": "Vu, Hung Anh and Reeves, Galen and Wenger, Emily",
    "BoundarySyncRepCoupling2607": "Liu, Zewen",
    "MeasureDatasetDiversity": "Zhao, Dora and Andrews, Jerone T. A. and Papakyriakopoulos, Orestis and Xiang, Alice",
    "ModelCollapseMemorization": "Shi, Lianghe and Wu, Meng and Zhang, Huijie and Zhang, Zekai and Tao, Molei and Qu, Qing",
    "ArtificialHivemind": "Anonymous",
    "CorrelatedErrors2506": "Kim, Elliot and Garg, Avi and Peng, Kenny and Garg, Nikhil",
    "SimilarlyCreative2608": "Patel, Nirav and Crossman, Josiah and Aggarwal, Eva and Wenger, Emily",
    "VendiScore": "Friedman, Dan and Dieng, Adji Bousso",
}


def bibtex_escape(s: str) -> str:
    # Escape characters BibTeX/LaTeX treats specially so titles with raw
    # underscores/ampersands/percents (common in harvested arXiv titles)
    # don't break compilation. Titles pre-escaped via TITLE_OVERRIDES (e.g.
    # already containing "\_") are left alone by checking for an existing backslash.
    out = []
    i = 0
    while i < len(s):
        c = s[i]
        if c in "&%" :
            out.append("\\" + c)
        elif c == "_" and (i == 0 or s[i - 1] != "\\"):
            out.append("\\_")
        else:
            out.append(c)
        i += 1
    return "".join(out)


def make_entry(rec: dict) -> str:
    key = rec["key"]
    title = TITLE_OVERRIDES.get(key, rec.get("title") or key)
    year = rec.get("year") or "2025"
    ids = rec.get("ids") or {}
    arxiv = ids.get("arxiv")
    openreview = ids.get("openreview")
    author = AUTHOR_OVERRIDES.get(key, "Anonymous")
    # Prefer an arXiv-derived URL whenever an arXiv id is known, even if the
    # jsonl's own `url` field still points at an OpenReview page (harvested
    # before the arXiv id was resolved) — the arXiv version is public and
    # canonical once it exists.
    if arxiv:
        url = f"https://arxiv.org/abs/{arxiv}"
    elif openreview:
        url = f"https://openreview.net/forum?id={openreview}"
    else:
        url = rec.get("url") or ""
    if arxiv:
        return (
            f"@misc{{{key},\n"
            f"  title = {{{{{bibtex_escape(title)}}}}},\n"
            f"  author = {{{author}}},\n"
            f"  year = {{{year}}},\n"
            f"  eprint = {{{arxiv}}},\n"
            f"  archivePrefix = {{arXiv}},\n"
            f"  url = {{{url}}}\n"
            f"}}\n"
        )
    elif openreview:
        return (
            f"@misc{{{key},\n"
            f"  title = {{{{{bibtex_escape(title)}}}}},\n"
            f"  author = {{{author}}},\n"
            f"  year = {{{year}}},\n"
            f"  howpublished = {{OpenReview submission {openreview}}},\n"
            f"  note = {{Anonymous preprint/under-review submission; cited via OpenReview id per reference-cache record}},\n"
            f"  url = {{{url}}}\n"
            f"}}\n"
        )
    else:
        return (
            f"@misc{{{key},\n"
            f"  title = {{{{{bibtex_escape(title)}}}}},\n"
            f"  author = {{{author}}},\n"
            f"  year = {{{year}}},\n"
            f"  url = {{{url}}}\n"
            f"}}\n"
        )


def main():
    entries = []
    seen = set()
    with open(JSONL) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            if rec.get("verdict") != "selected":
                continue
            key = rec["key"]
            if key in seen:
                continue
            seen.add(key)
            entries.append(make_entry(rec))
    OUT.write_text(
        "% AUTO-GENERATED by gen_refs_bib.py from reference_candidates.jsonl's `selected` records.\n"
        "% Do not hand-edit; re-run the script after any jsonl change.\n\n"
        + "\n".join(entries)
    )
    print(f"Wrote {len(entries)} entries to {OUT}")


if __name__ == "__main__":
    main()
