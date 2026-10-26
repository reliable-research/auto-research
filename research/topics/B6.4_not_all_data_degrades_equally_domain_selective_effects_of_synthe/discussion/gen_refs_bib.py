import json

# Manually curated bibliographic metadata for selected keys (verified via digest reads / title-match web search),
# keyed by the jsonl 'key' field. This mirrors the jsonl but supplies BibTeX-shape fields (author/year/venue)
# not stored in the jsonl schema itself. Script-generated: run this file to regenerate refs.bib from
# discussion/reference_candidates.jsonl's selected records.

META = {
    "MixRatio2023": dict(author="Garg, Anvit and Bhattacharya, Sohom and Sur, Pragya",
                          title="Preventing Model Collapse Under Overparametrization: Optimal Mixing Ratios for Interpolation Learning and Ridge Regression",
                          year="2026", eprint="2509.22341"),
    "IterStability2023": dict(author="Bertrand, Quentin and Bose, Avishek Joey and Duplessis, Alexandre and Jiralerspong, Marco and Gidel, Gauthier",
                          title="On the Stability of Iterative Retraining of Generative Models on their own Data",
                          year="2024", eprint="2310.00429", note="ICLR 2024 (spotlight)"),
    "CrossModelRecursion2023": dict(author="Vu, Hung Anh and Reeves, Galen and Wenger, Emily",
                          title="What happens when generative AI models train recursively on each others' outputs?",
                          year="2025", eprint="2505.21677"),
    "EntropyCollapse2023": dict(author="Shi, Lianghe and Wu, Meng and Zhang, Huijie and Zhang, Zekai and Tao, Molei and Qu, Qing",
                          title="A Closer Look at Model Collapse: From a Generalization-to-Memorization Perspective",
                          year="2025", eprint="2509.16499", note="NeurIPS 2025 (spotlight)"),
    "SpendWisely2023": dict(author="Yang, Pu and Feng, Yunzhen and Chen, Ziyuan and Wu, Yuhang and Li, Zhuoyuan",
                          title="Spend Wisely: Maximizing Post-Training Gains in Iterative Synthetic Data Bootstrapping",
                          year="2025", eprint="2501.18962", note="NeurIPS 2025 (spotlight)"),
    "DoReMi2023": dict(author="Xie, Sang Michael and Pham, Hieu and Dong, Xuanyi and Du, Nan and Liu, Hanxiao and Lu, Yifeng and Liang, Percy and Le, Quoc V. and Ma, Tengyu and Yu, Adams Wei",
                          title="DoReMi: Optimizing Data Mixtures Speeds Up Language Model Pretraining",
                          year="2023", eprint="2305.10429", note="NeurIPS 2023"),
    "RegMix2023": dict(author="Liu, Qian and Zheng, Xiaosen and Muennighoff, Niklas and Zeng, Guangtao and Dou, Longxu and Pang, Tianyu and Jiang, Jing and Lin, Min",
                          title="RegMix: Data Mixture as Regression for Language Model Pre-training",
                          year="2024", eprint="2407.01492", note="ICLR 2025 (spotlight)"),
    "SynthWeighting2023": dict(author="Kuo, Hsun-Yu and Liao, Yin-Hsiang and Chao, Yu-Chieh and Ma, Wei-Yun and Cheng, Pu-Jen",
                          title="Not All LLM-Generated Data Are Equal: Rethinking Data Weighting in Text Classification",
                          year="2025", eprint="2410.21526", note="ICLR 2025"),
    "TALR2023": dict(author="Lin, Jiacheng and others",
                          title="SFT Doesn't Always Hurt General Capabilities: Revisiting Domain-Specific Fine-Tuning in LLMs",
                          year="2025", eprint="2509.20758"),
    "Shumailov2024Collapse": dict(author="Shumailov, Ilia and Shumaylov, Zakhar and Zhao, Yiren and Gal, Yarin and Papernot, Nicolas and Anderson, Ross",
                          title="The Curse of Recursion: Training on Generated Data Makes Models Forget",
                          year="2024", eprint="2305.17493", note="Also published in Nature (2024)"),
    "EpidemiologyCollapse2026": dict(author="Wang, Xiangyu and others",
                          title="Epidemiology of Model Collapse: Modeling Synthetic Data Contamination via Bilayer SIR Dynamics",
                          year="2026", eprint="2606.05168"),
    "CodeRecursiveCollapse2026": dict(author="Song, Xinyuan and Cai, Zekun and Zhao, Liang",
                          title="When AI Reviews Its Own Code: Recursive Self-Training Collapse in Code LLMs",
                          year="2026", eprint="2606.28438"),
    "DemystifySynth2025": dict(author="Kang, Feiyang and Ardalani, Newsha and Kuchnik, Michael and Emad, Youssef and Elhoushi, Mostafa and Sengupta, Shubhabrata and Li, Shang-Wen and Raghavendra, Ramya and Jia, Ruoxi and Wu, Carole-Jean",
                          title="Demystifying Synthetic Data in LLM Pre-training: A Systematic Study of Scaling Laws, Benefits, and Pitfalls",
                          year="2025", eprint="2510.01631"),
    "VerifierEscape2025": dict(author="Yi, Bingji and Liu, Qiyuan and Cheng, Yuwei and Xu, Haifeng",
                          title="Escaping Model Collapse via Synthetic Data Verification: Near-term Improvements and Long-term Convergence",
                          year="2025", eprint="2510.16657"),
}

def bibtex_entry(key, rec):
    m = META.get(key, {})
    title = m.get("title", rec.get("title", ""))
    author = m.get("author", "")
    year = m.get("year", str(rec.get("year", "")))
    eprint = m.get("eprint") or (rec.get("ids", {}) or {}).get("arxiv")
    note = m.get("note", "")
    lines = [f"@article{{{key},"]
    if author:
        lines.append(f"  author = {{{author}}},")
    lines.append(f"  title = {{{title}}},")
    lines.append(f"  year = {{{year}}},")
    if eprint:
        lines.append(f"  eprint = {{{eprint}}},")
        lines.append(f"  archivePrefix = {{arXiv}},")
        lines.append(f"  url = {{https://arxiv.org/abs/{eprint}}},")
    elif rec.get("url"):
        lines.append(f"  url = {{{rec['url']}}},")
    if note:
        lines.append(f"  note = {{{note}}},")
    lines.append("}")
    return "\n".join(lines)

def main():
    entries = []
    with open("discussion/reference_candidates.jsonl") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            if r.get("verdict") == "selected":
                entries.append(bibtex_entry(r["key"], r))
    with open("discussion/refs.bib", "w") as f:
        f.write("% Auto-generated from discussion/reference_candidates.jsonl's `selected` records.\n")
        f.write("% Regenerate via: python3 /path/to/gen_refs_bib.py (see discussion/pipeline.md Phase F log)\n\n")
        f.write("\n\n".join(entries) + "\n")
    print(f"Wrote {len(entries)} entries to discussion/refs.bib")

if __name__ == "__main__":
    main()
