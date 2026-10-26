---
code: B3.2
title_cn: "漂移的方差分解"
label: "[机制]"
parent_topic: "B3. 跨版本行为漂移 / 纵向审计"
source: "../../38_topics.txt"
---

# B3.2 漂移的方差分解

标签：[机制]

父 Topic：B3. 跨版本行为漂移 / 纵向审计

**B3.2 漂移的方差分解** [机制]
> Capability, Policy, or Format? Decomposing Behavioral Drift across LLM Version Pairs

核心问题：一次版本升级的行为变化中，多少来自能力变化、多少来自对齐/政策调整、多少只是格式偏好漂移？
最小实验：设计三类正交探针，对多个版本对做方差分解；检验分解在厂商间是否有共同结构。
