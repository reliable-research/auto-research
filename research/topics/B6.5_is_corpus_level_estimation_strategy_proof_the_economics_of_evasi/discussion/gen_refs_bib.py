import json
import os

# Script-generated refs.bib from discussion/reference_candidates.jsonl's `selected` records
# (goal.md Phase F hard gate: never hand-edit refs.bib; edit the jsonl and re-run this script).
#
# META supplies BibTeX-shape fields (author/year/venue/eprint) not stored in the jsonl schema.
# Records absent from META fall back to the jsonl fields; OpenReview-only records (no arXiv id,
# unresolved) are emitted in the original Anonymous/n.d. form so unverified identities are never
# fabricated.

META = {
    "MonitorAIScale": dict(
        author="Weixin Liang and Zachary Izzo and Yaohui Zhang and Haley Lepp and Hancheng Cao and Xuandong Zhao and Lingjiao Chen and Haotian Ye and Sheng Liu and Zhi Huang and Daniel A. McFarland and James Y. Zou",
        title="Monitoring AI-Modified Content at Scale: A Case Study on the Impact of ChatGPT on AI Conference Peer Reviews",
        year="2024", eprint="2403.07183", note="ICML 2024"),
    "DetectGPT": dict(
        author="Eric Mitchell and Yoonho Lee and Alexander Khazatsky and Christopher D. Manning and Chelsea Finn",
        title="DetectGPT: Zero-Shot Machine-Generated Text Detection using Probability Curvature",
        year="2023", eprint="2301.11305", note="ICML 2023"),
    "RAID2024": dict(
        author="Liam Dugan and Alyssa Hwang and Filip Trhlik and Josh Magnus Ludan and Andrew Zhu and Hainiu Xu and Daphne Ippolito and Chris Callison-Burch",
        title="RAID: A Shared Benchmark for Robust Evaluation of Machine-Generated Text Detectors",
        year="2024", eprint="2405.07940", note="ACL 2024"),
    "HC3_2023": dict(
        author="Biyang Guo and Xin Zhang and Ziyuan Wang and Minqi Jiang and Jinran Nie and Yuxuan Ding and Jianwei Yue and Yupeng Wu",
        title="How Close is ChatGPT to Human Experts? Comparison Corpus, Evaluation, and Detection",
        year="2023", eprint="2301.07597"),
    "MultiAgentMechDesign2025": dict(
        author="Qiushi Han and David Simchi-Levi and Renfei Tan and Zishuo Zhao",
        title="Multi-agent Adaptive Mechanism Design",
        year="2025", eprint="2512.21794"),
    "GumbelWatermarkSampleComplexity2026": dict(
        author="Shuwen Chai and Qiaosen Wang",
        title="Sample Complexities of Estimating Gumbel-Max Watermark Proportions with and without Reduction to Pivotal Statistics",
        year="2026", eprint="2607.00224"),
    "ATINTER2023": dict(
        author="Ashim Gupta and Carter Wood Blum and Temma Choji and Yingjie Fei and Shalin Shah and Alakananda Vempala and Vivek Srikumar",
        title="Don't Retrain, Just Rewrite: Countering Adversarial Perturbations by Rewriting Text",
        year="2023", venue="ACL 2023"),
    # --- Added 2026-08-21 review pass (all arXiv ids live-verified in one batched API request) ---
    "KrishnaParaphrase2023": dict(
        author="Kalpesh Krishna and Yixiao Song and Marzena Karpinska and John Wieting and Mohit Iyyer",
        title="Paraphrasing Evades Detectors of AI-generated Text, but Retrieval is an Effective Defense",
        year="2023", eprint="2303.13408", note="NeurIPS 2023"),
    "Sadasivan2023": dict(
        author="Vinu Sankar Sadasivan and Aounon Kumar and Sriram Balasubramanian and Wenxiao Wang and Soheil Feizi",
        title="Can AI-Generated Text be Reliably Detected?",
        year="2023", eprint="2303.11156"),
    "AdvParaphrase2025": dict(
        author="Yize Cheng and Vinu Sankar Sadasivan and Mehrdad Saberi and Shoumik Saha and Soheil Feizi",
        title="Adversarial Paraphrasing: A Universal Attack for Humanizing AI-Generated Text",
        year="2025", eprint="2506.07001", note="NeurIPS 2025"),
    "PADBen2025": dict(
        author="Yiwei Zha and Rui Min and Shanu Sushmita",
        title="PADBen: A Comprehensive Benchmark for Evaluating AI Text Detectors Against Paraphrase Attacks",
        year="2025", eprint="2511.00416"),
    "MASH2026": dict(
        author="Yongtong Gu and Songze Li and Xia Hu",
        title="MASH: Evading Black-Box AI-Generated Text Detectors via Style Humanization",
        year="2026", eprint="2601.08564"),
    "QuantShift2023": dict(
        author="Pablo Gonz\\'alez and Alejandro Moreo and Fabrizio Sebastiani",
        title="Binary Quantification and Dataset Shift: An Experimental Investigation",
        year="2023", eprint="2310.04565", note="Data Mining and Knowledge Discovery, 2024"),
    "QuantifierVariance2021": dict(
        author="Dirk Tasche",
        title="Minimising Quantifier Variance under Prior Probability Shift",
        year="2021", eprint="2107.08209"),
}


def bibtex_entry(key, rec):
    m = META.get(key, {})
    key = key.replace("-", "").replace("_", "")  # bib-safe key (matches \citep usage in the .tex)
    title = m.get("title", rec.get("title", ""))
    author = m.get("author", "")
    year = m.get("year") or (str(rec.get("year")) if rec.get("year") else "n.d.")
    eprint = m.get("eprint") or (rec.get("ids", {}) or {}).get("arxiv")
    venue = m.get("venue", "")
    note = m.get("note", "")
    lines = [f"@misc{{{key},"]
    if author:
        lines.append(f"  author = {{{author}}},")
    else:
        lines.append("  author = {Anonymous},")
    lines.append(f"  title = {{{{{title}}}}},")
    lines.append(f"  year = {{{year}}},")
    if eprint:
        lines.append("  howpublished = {arXiv},")
        lines.append(f"  url = {{https://arxiv.org/abs/{eprint}}},")
        lines.append(f"  eprint = {{{eprint}}},")
        lines.append("  archivePrefix = {arXiv},")
    elif venue:
        lines.append(f"  howpublished = {{{venue}}},")
    else:
        orid = (rec.get("ids", {}) or {}).get("openreview")
        lines.append(f"  howpublished = {{OpenReview, id={orid}}},")
        lines.append("  note = {Under double-blind review; author list withheld},")
        if rec.get("url"):
            lines.append(f"  url = {{{rec['url']}}},")
    if note:
        lines.append(f"  note = {{{note}}},")
    # drop trailing comma on last field line
    lines[-1] = lines[-1].rstrip(",")
    lines.append("}")
    return "\n".join(lines)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    jsonl = os.path.join(here, "reference_candidates.jsonl")
    out = os.path.join(here, "refs.bib")
    entries = []
    with open(jsonl) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            if rec.get("verdict") != "selected":
                continue
            entries.append(bibtex_entry(rec["key"], rec))
    header = (
        "% Auto-generated by gen_refs_bib.py from discussion/reference_candidates.jsonl's `selected` records.\n"
        "% Do not hand-edit -- re-run the script after the jsonl changes (goal.md Phase F hard gate).\n"
    )
    with open(out, "w") as f:
        f.write(header + "\n" + "\n\n".join(entries) + "\n")
    print(f"Wrote {len(entries)} entries to {out}")


if __name__ == "__main__":
    main()
