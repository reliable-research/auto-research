#!/usr/bin/env python3
"""Generate refs.bib from reference_candidates.jsonl's `selected` records.

Per goal.md Phase F: "refs.bib script-generated from the jsonl; ... hand-typing
either is banned." Re-run this script whenever reference_candidates.jsonl changes.
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
JSONL = HERE / "reference_candidates.jsonl"
OUT = HERE / "refs.bib"


def bibkey(key: str) -> str:
    return re.sub(r"[^A-Za-z0-9]", "", key)


def guess_venue(rec: dict) -> str:
    venue = (rec.get("venue") or "").strip()
    if not venue or venue.startswith("OpenReview (venue/year"):
        return "arXiv preprint"
    return venue


# Authors confirmed by directly reading the paper (PDF) during this pass, per
# goal.md's no-fabrication rule. Records without a confirmed PDF (still
# verified.id_resolves=false in the jsonl) are left author-less rather than
# guessed.
KNOWN_AUTHORS = {
    "Tam2024LetMeSpeak": "Zhi Rui Tam and Cheng-Kuang Wu and Yi-Lin Tsai and Chieh-Yen Lin and Hung-yi Lee and Yun-Nung Chen",
    "ChatGPTDrift2307": "Lingjiao Chen and Matei Zaharia and James Zou",
    "LogProbTracking": "Timoth{\\'e}e Chauvin and Erwan Le Merrer and Fran{\\c c}ois Ta{\\\"i}ani and Gilles Tredan",
    "DSPy": "Omar Khattab and Arnav Singhvi and Paridhi Maheshwari and Zhiyuan Zhang and Keshav Santhanam and Sri Vardhamanan and Saiful Haq and Ashutosh Sharma and Thomas T. Joshi and Hanna Moazam and Heather Miller and Matei Zaharia and Christopher Potts",
    "RECAST": "Zhengkang Guo and Wenhao Liu and Mingchen Xie and Jingwen Xu and Zisu Huang and Muzhao Tian and Jianhan Xu and Yuanzhe Shen and Qi Qian and Muling Wu and Xiaohua Wang and Changze Lv and HeDa Wang and Hu Yao and Xiaoqing Zheng and Xuanjing Huang",
    "AutoIF": "Guanting Dong and Keming Lu and Chengpeng Li and Tingyu Xia and Bowen Yu and Chang Zhou and Jingren Zhou",
}


def main() -> None:
    records = []
    with JSONL.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            d = json.loads(line)
            if d.get("verdict") == "selected":
                records.append(d)

    records.sort(key=lambda d: d["key"])

    entries = []
    for d in records:
        key = bibkey(d["key"])
        title = d.get("title", "").replace("{", "").replace("}", "")
        venue = guess_venue(d)
        year = d.get("year") or "n.d."
        url = d.get("url", "")
        arxiv = (d.get("ids") or {}).get("arxiv")
        note_bits = []
        if arxiv:
            note_bits.append(f"arXiv:{arxiv}")
        openreview = (d.get("ids") or {}).get("openreview")
        if openreview and not arxiv:
            note_bits.append(f"OpenReview:{openreview}")
        note = "; ".join(note_bits)

        fields = []
        author = KNOWN_AUTHORS.get(d["key"])
        if author:
            fields.append(f'  author = {{{author}}}')
        fields += [
            f'  title = {{{title}}}',
            f'  year = {{{year}}}',
            f'  howpublished = {{{venue}}}',
            f'  url = {{{url}}}',
        ]
        if note:
            fields.append(f'  note = {{{note}}}')

        entry = f"@misc{{{key},\n" + ",\n".join(fields) + "\n}\n"
        entries.append(entry)

    OUT.write_text("\n".join(entries))
    print(f"wrote {len(entries)} entries to {OUT}")


if __name__ == "__main__":
    main()
