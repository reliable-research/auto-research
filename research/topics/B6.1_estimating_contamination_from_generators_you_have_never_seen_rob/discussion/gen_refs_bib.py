#!/usr/bin/env python3
"""Script-generate refs.bib from reference_candidates.jsonl's `selected` records.
Per goal.md Phase F: 'refs.bib script-generated from the jsonl; ... hand-typing either is banned.'
Topic: B6.1
"""
import json

JSONL = "/data/wangjian/wj_code/dl_research/new_research/topics/B6.1_estimating_contamination_from_generators_you_have_never_seen_rob/discussion/reference_candidates.jsonl"
OUT = "/data/wangjian/wj_code/dl_research/new_research/topics/B6.1_estimating_contamination_from_generators_you_have_never_seen_rob/discussion/refs.bib"

# Metadata not stored in the jsonl schema (authors/year for bibtex) is supplied here,
# sourced from the real digests built during this pass (paper_cache/pdf_digests_main/*.md)
# or from the arXiv/OpenReview page itself. Keyed by jsonl `key`.
BIB_META = {
    "CanSmallTrainingRunsReli224503": {
        "author": "Jiachen T. Wang and Tong Wu and Kaifeng Lyu and James Zou and Dawn Song and Ruoxi Jia and Prateek Mittal",
        "year": 2026, "venue": "ICLR", "entrytype": "inproceedings",
        "title": "Can Small Training Runs Reliably Guide Data Curation? Rethinking Proxy-Model Practice",
    },
    "SampleComplexitiesofEsti700224": {
        "author": "Shuwen Chai and Qiaosen Wang",
        "year": 2026, "venue": "arXiv preprint", "entrytype": "misc",
        "title": "Sample Complexities of Estimating Gumbel-Max Watermark Proportions with and without Reduction to Pivotal Statistics",
    },
    "OntheEffectivenessofTrai224570": {
        "author": "Shiqi Kuang and Zhao Tian and Tao Xiao and Dong Wang",
        "year": 2026, "venue": "arXiv preprint", "entrytype": "misc",
        "title": "On the Effectiveness of Training Data Optimization for LLM-based Code Generation: An Empirical Study",
    },
    "DetectGPT2023": {
        "author": "Eric Mitchell and Yoonho Lee and Alexander Khazatsky and Christopher D. Manning and Chelsea Finn",
        "year": 2023, "venue": "ICML", "entrytype": "inproceedings",
        "title": "DetectGPT: Zero-Shot Machine-Generated Text Detection using Probability Curvature",
    },
    "LearnToDistance2023": {
        "author": "Hongyi Zhou and Jin Zhu and Kai Ye and Ying Yang and Erhan Xu and Chengchun Shi",
        "year": 2026, "venue": "ICLR", "entrytype": "inproceedings",
        "title": "Learn-to-Distance: Distance Learning for Detecting LLM-Generated Text",
    },
    "DR2023RecoveryDetect": {
        "author": "{Anonymous (OpenReview submission; no public PDF resolvable at digest time)}",
        "year": 2025, "venue": "OpenReview submission", "entrytype": "misc",
        "title": "D&R: Recovery-based AI-Generated Text Detection via a Single Black-box LLM Call",
    },
    "MarkovCalibration2023": {
        "author": "Chenwang Wu and Yiu-ming Cheung and Shuhai Zhang and Bo Han and Defu Lian",
        "year": 2026, "venue": "ICLR", "entrytype": "inproceedings",
        "title": "Beyond Raw Detection Scores: Markov-Informed Calibration for Boosting Machine-Generated Text Detection",
    },
    "KirchenbauerWatermark2023": {
        "author": "John Kirchenbauer and Jonas Geiping and Yuxin Wen and Jonathan Katz and Ian Miers and Tom Goldstein",
        "year": 2023, "venue": "ICML", "entrytype": "inproceedings",
        "title": "A Watermark for Large Language Models",
    },
    "DRCT2024DiffusionRecon": {
        "author": "Baoying Chen and Jishen Zeng and Jianquan Yang and Rui Yang",
        "year": 2024, "venue": "ICML", "entrytype": "inproceedings",
        "title": "DRCT: Diffusion Reconstruction Contrastive Training towards Universal Detection of Diffusion Generated Images",
    },
    "RecursiveMultiEntity2024": {
        "author": "Hung Anh Vu and Galen Reeves and Emily Wenger",
        "year": 2025, "venue": "arXiv preprint", "entrytype": "misc",
        "title": "What Happens When Generative AI Models Train Recursively on Each Other's Outputs?",
    },
    "IterativeRetrainStability2024": {
        "author": "Quentin Bertrand and Avishek Joey Bose and Alexandre Duplessis and Marco Jiralerspong and Gauthier Gidel",
        "year": 2023, "venue": "arXiv preprint", "entrytype": "misc",
        "title": "On the Stability of Iterative Retraining of Generative Models on Their Own Data",
    },
    "PreferenceLeakage2024": {
        "author": "Dawei Li and Renliang Sun and Yue Huang and Ming Zhong and Bohan Jiang and Jiawei Han and Xiangliang Zhang and Wei Wang and Huan Liu",
        "year": 2025, "venue": "arXiv preprint", "entrytype": "misc",
        "title": "Preference Leakage: A Contamination Problem in LLM-as-a-judge",
    },
    # --- Added 2026-08-21 by the review_2026-08.md novelty/staleness pass (findings N1, N2, N3, F1).
    # Every field below was taken from a live arXiv API response (batched id_list queries,
    # checked 2026-08-21), not from memory.
    "MonitoringAIContent2024": {
        "author": "Weixin Liang and Zachary Izzo and Yaohui Zhang and Haley Lepp and Hancheng Cao and Xuandong Zhao and Lingjiao Chen and Haotian Ye and Sheng Liu and Zhi Huang and Daniel A. McFarland and James Y. Zou",
        "year": 2024, "venue": "ICML", "entrytype": "inproceedings",
        "title": "Monitoring AI-Modified Content at Scale: A Case Study on the Impact of ChatGPT on AI Conference Peer Reviews",
    },
    "MappingLLMUse2024": {
        "author": "Weixin Liang and Yaohui Zhang and Zhengxuan Wu and Haley Lepp and Wenlong Ji and Xuandong Zhao and Hancheng Cao and Sheng Liu and Siyu He and Zhi Huang and Diyi Yang and Christopher Potts and Christopher D. Manning and James Y. Zou",
        "year": 2024, "venue": "arXiv preprint", "entrytype": "misc",
        "title": "Mapping the Increasing Use of LLMs in Scientific Papers",
    },
    "RAID2024Benchmark": {
        "author": "Liam Dugan and Alyssa Hwang and Filip Trhlik and Josh Magnus Ludan and Andrew Zhu and Hainiu Xu and Daphne Ippolito and Chris Callison-Burch",
        "year": 2024, "venue": "ACL", "entrytype": "inproceedings",
        "title": "RAID: A Shared Benchmark for Robust Evaluation of Machine-Generated Text Detectors",
    },
    "MAGE2024InTheWild": {
        "author": "Yafu Li and Qintong Li and Leyang Cui and Wei Bi and Zhilin Wang and Longyue Wang and Linyi Yang and Shuming Shi and Yue Zhang",
        "year": 2024, "venue": "ACL", "entrytype": "inproceedings",
        "title": "MAGE: Machine-generated Text Detection in the Wild",
    },
    "DipperParaphrase2023": {
        "author": "Kalpesh Krishna and Yixiao Song and Marzena Karpinska and John Wieting and Mohit Iyyer",
        "year": 2023, "venue": "NeurIPS", "entrytype": "inproceedings",
        "title": "Paraphrasing evades detectors of AI-generated text, but retrieval is an effective defense",
    },
    "ReliablyDetectable2023": {
        "author": "Vinu Sankar Sadasivan and Aounon Kumar and Sriram Balasubramanian and Wenxiao Wang and Soheil Feizi",
        "year": 2023, "venue": "Transactions on Machine Learning Research (TMLR)", "entrytype": "misc",
        "title": "Can AI-Generated Text be Reliably Detected?",
    },
    "QuantDatasetShift2023": {
        "author": "Pablo Gonz\\'alez and Alejandro Moreo and Fabrizio Sebastiani",
        "year": 2023, "venue": "arXiv preprint", "entrytype": "misc",
        "title": "Binary Quantification and Dataset Shift: An Experimental Investigation",
    },
    "QuantPriorShift2018": {
        "author": "Afonso Fernandes Vaz and Rafael Izbicki and Rafael Bassi Stern",
        "year": 2018, "venue": "arXiv preprint", "entrytype": "misc",
        "title": "Quantification under prior probability shift: the ratio estimator and its extensions",
    },
}


def bib_escape(s):
    return s.replace("&", "\\&")


def make_entry(rec):
    key = rec["key"]
    meta = BIB_META.get(key)
    if meta is None:
        raise SystemExit(f"no BIB_META for {key}")
    title = bib_escape(meta["title"])
    ids = rec.get("ids", {})
    arxiv = ids.get("arxiv")
    openreview = ids.get("openreview")
    url = rec.get("url") or (f"https://arxiv.org/abs/{arxiv}" if arxiv else (f"https://openreview.net/forum?id={openreview}" if openreview else ""))
    lines = [f"@{meta['entrytype']}{{{key},"]
    lines.append(f"  title     = {{{title}}},")
    lines.append(f"  author    = {{{meta['author']}}},")
    lines.append(f"  year      = {{{meta['year']}}},")
    if meta["entrytype"] == "inproceedings":
        lines.append(f"  booktitle = {{{meta['venue']}}},")
    else:
        lines.append(f"  howpublished = {{{meta['venue']}}},")
    if arxiv:
        lines.append(f"  eprint    = {{{arxiv}}},")
        lines.append("  archivePrefix = {arXiv},")
    if url:
        lines.append(f"  url       = {{{url}}},")
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

    header = (
        "% Auto-generated by gen_refs_bib_b61.py from discussion/reference_candidates.jsonl's\n"
        "% `selected` records. Do not hand-edit -- regenerate instead (goal.md Phase F hard gate:\n"
        "% 'refs.bib script-generated from the jsonl; hand-typing either is banned').\n\n"
    )
    entries = [make_entry(r) for r in selected]
    with open(OUT, "w") as f:
        f.write(header)
        f.write("\n\n".join(entries))
        f.write("\n")
    print(f"Wrote {len(entries)} entries to {OUT}")


if __name__ == "__main__":
    main()
