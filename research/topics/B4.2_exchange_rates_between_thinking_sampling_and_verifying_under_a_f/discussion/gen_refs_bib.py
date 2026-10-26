import json, re

# author lists gathered by direct extraction (arXiv PDFs read in this session, or arxiv_miner_cache digests)
AUTHORS = {
    "ComputeAccuracy251224776": ["Ákos Prucs", "Nara Csutora", "Mátyás Antal", "Márk Marosi"],
    "UnderstandingAnd251224574": ["Zhenyu Zhang", "Xiaoxia Wu", "Zhongzhu Zhou", "Qingyang Wu", "Yineng Zhang", "Pragaash Ponnusamy", "Harikaran Subbaraj", "Jue Wang", "Shuaiwen Leon Song", "Ben Athiwaratkun"],
    "ScalingUnverifiable251222650": ["Shuyu Gan", "James Mooney", "Pan Hao", "Renxiang Wang", "Mingyi Hong", "Qianwen Wang", "Dongyeop Kang"],
    "TheReward251223067": ["Fady Rezk", "Yuangang Pan", "Chuan-Sheng Foo", "Xun Xu", "Nancy F. Chen", "Henry Gouk", "Timothy Hospedales"],
    "SweRm251221919": ["Kashun Shum", "Binyuan Hui", "Jiawei Chen", "Lei Zhang", "X. W.", "Jiaxi Yang", "Yuzhen Huang", "Junyang Lin", "Junxian He"],
    "CostTrade251222364": ["Saurabh Deochake", "Debajyoti Mukhopadhyay"],
    "SnellTTC4FWA": ["Charlie Snell", "Jaehoon Lee", "Kelvin Xu", "Aviral Kumar"],
    "VerifierFreeSubbeee": ["Amrith Setlur", "Nived Rajaraman", "Sergey Levine", "Aviral Kumar"],
    "PlanBudgctsp": ["Junhong Lin", "Xinyue Zeng", "Jie Zhu", "Song Wang", "Julian Shun", "Jun Wu", "Dawei Zhou"],
    "CoTLength6QDF": ["Yuyang Wu", "Yifei Wang", "Ziyu Ye", "Tianqi Du", "Stefanie Jegelka", "Yisen Wang"],
    "AsymVerifhxL4": ["Weihao Zeng", "Keqing He", "Chuqiao Kuang", "Xiaoguang Li", "Junxian He"],
    "OTVerifyBBDh": ["Arpan Mukherjee", "Marcello Bullo", "Debabrota Basu", "Deniz Gündüz"],
    "BestOfMaja6CV": ["Qiwei Di", "Kaixuan Ji", "Xuheng Li", "Heyang Zhao", "Quanquan Gu"],
    "RerankLawsrhCg": ["António Farinhas", "Haau-Sing Li", "André F. T. Martins"],
    "BrownMonkeys240721787": ["Bradley Brown", "Jordan Juravsky", "Ryan Ehrlich", "Ronald Clark", "Quoc V. Le", "Christopher Ré", "Azalia Mirhoseini"],
    # added 2026-08-21 review pass — author lists taken from the live arXiv API response (batched id_list query), never from memory
    "SpecExec260607846": ["Faisal Fareed"],
    "InferEcon260713080": ["Sheng-Wei Peng", "Yi-Hsun Lin", "Yi-Pei Lee"],
}

# real publication years (corrected from the jsonl's placeholder "OpenReview (under review) 2026" venue tags,
# now that this session fetched and read the actual arXiv preprints)
REAL_YEAR = {
    "SnellTTC4FWA": 2024, "VerifierFreeSubbeee": 2025, "PlanBudgctsp": 2025,
    "CoTLength6QDF": 2025, "AsymVerifhxL4": 2025, "OTVerifyBBDh": 2025,
    "BestOfMaja6CV": 2025, "RerankLawsrhCg": 2024, "BrownMonkeys240721787": 2024,
    "SpecExec260607846": 2026, "InferEcon260713080": 2026,
}

def bibtex_author_string(names):
    return " and ".join(names)

def make_entry(r):
    key = r["key"]
    title = r["title"]
    arxiv = r.get("ids", {}).get("arxiv")
    year = REAL_YEAR.get(key, r.get("year"))
    authors = AUTHORS.get(key)
    author_field = bibtex_author_string(authors) if authors else "Unknown"
    lines = [f"@misc{{{key},"]
    lines.append(f"  title        = {{{title}}},")
    lines.append(f"  author       = {{{author_field}}},")
    lines.append(f"  year         = {{{year}}},")
    if arxiv:
        lines.append(f"  eprint       = {{{arxiv}}},")
        lines.append("  archivePrefix = {arXiv},")
        lines.append(f"  url          = {{https://arxiv.org/abs/{arxiv}}},")
    else:
        lines.append(f"  url          = {{{r.get('url','')}}},")
    lines.append("}")
    return "\n".join(lines)

entries = []
with open("reference_candidates.jsonl") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        r = json.loads(line)
        if r.get("verdict") == "selected":
            entries.append(make_entry(r))

with open("refs.bib", "w") as f:
    f.write("% Auto-generated from reference_candidates.jsonl's selected records — do not hand-edit.\n")
    f.write("% Regenerate via discussion/gen_refs_bib.py whenever the jsonl's selected set changes.\n\n")
    f.write("\n\n".join(entries) + "\n")

print(f"Wrote {len(entries)} entries to refs.bib")
