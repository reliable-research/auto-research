---
code: B2.1
title_cn: "受控替换归因协议"
label: "[证据]"
parent_topic: "B2. 失败归因（plan / tool / execution）"
source: "../../38_topics.txt"
---

# B2.1 受控替换归因协议

标签：[证据]

父 Topic：B2. 失败归因（plan / tool / execution）

**B2.1 受控替换归因协议** [证据]
> Causal Failure Attribution via Controlled Component Substitution in Tool-Use Agents

核心问题：固定 executor 换 plan、固定 plan 换工具条件，失败是否随被替换组件转移？归因结论可否被替换实验机械验证？
最小实验：注入已知故障（坏 plan 步、断工具、污染观测）作 ground-truth 标签，测各归因方法的准确率。这是给 agent 领域造一个"Defects4J"——已知故障标注库本身就是贡献。
