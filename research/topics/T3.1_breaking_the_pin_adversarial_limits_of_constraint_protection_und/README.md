---
code: T3.1
title_cn: "Pinning 的对抗失效边界"
label: "[边界]"
parent_topic: "T3. Memory 约束保持（窄环，4 条）"
source: "../../38_topics.txt"
---

# T3.1 Pinning 的对抗失效边界

标签：[边界]

父 Topic：T3. Memory 约束保持（窄环，4 条）

**T3.1 Pinning 的对抗失效边界** [边界]
> Breaking the Pin: Adversarial Limits of Constraint Protection under Context Compaction

核心问题：原论文的优化注入击穿全部受测模型——pinning 类防御在对抗性 compaction 下的精确失效边界在哪里？防御-攻击的成本比是多少？
最小实验：注入优化强度扫描 × 防御变体矩阵，画击穿率曲线。
