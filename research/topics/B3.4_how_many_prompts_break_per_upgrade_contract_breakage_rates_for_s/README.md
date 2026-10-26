---
code: B3.4
title_cn: "下游契约破坏度量"
label: "[证据]"
parent_topic: "B3. 跨版本行为漂移 / 纵向审计"
source: "../../38_topics.txt"
---

# B3.4 下游契约破坏度量

标签：[证据]

父 Topic：B3. 跨版本行为漂移 / 纵向审计

**B3.4 下游契约破坏度量** [证据]
> How Many Prompts Break per Upgrade? Contract Breakage Rates for Structured-Output Pipelines

核心问题：一次版本跳变平均打断多少生产风格的 prompt 模板/结构化输出契约？什么特征的契约最脆弱？
最小实验：构造模拟生产契约库（JSON schema、格式约定、few-shot 模板），逐版本测破坏率与脆弱性预测因子。
