---
code: B6.2
title_cn: "污染-退化的剂量反应曲线"
label: "[机制]"
parent_topic: "B6. 污染机制层（合成语料）"
source: "../../38_topics.txt"
---

# B6.2 污染-退化的剂量反应曲线

标签：[机制]

父 Topic：B6. 污染机制层（合成语料）

**B6.2 污染-退化的剂量反应曲线** [机制]
> Dose-Response of Corpus Contamination: Coupling Measured Synthetic Fractions to Downstream Degradation

核心问题：训练语料合成占比与模型能力/多样性退化之间的函数关系是什么？存在安全阈值还是单调退化？
最小实验：受控合成比例训练小模型（冻结骨干 + 持续预训练可控成本），画剂量反应曲线。把取证接到 model collapse 上，从"测多少"走到"多少有害"。
