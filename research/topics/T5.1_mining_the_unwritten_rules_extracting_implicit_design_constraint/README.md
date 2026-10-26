---
code: T5.1
title_cn: "从评审历史挖掘隐式约束"
label: "[证据]"
parent_topic: "T5. 设计约束合规（coding agent）"
source: "../../38_topics.txt"
---

# T5.1 从评审历史挖掘隐式约束

标签：[证据]

父 Topic：T5. 设计约束合规（coding agent）

**T5.1 从评审历史挖掘隐式约束** [证据]
> Mining the Unwritten Rules: Extracting Implicit Design Constraints from Code Review History

核心问题：PR 评审意见中能否系统抽取隐式设计约束？agent 在通过测试的前提下最常违反哪些类别（错误处理/架构惯例/API 约定）？
最小实验：评审语料 → 约束目录 → 对 agent patch 的违规分布统计。真值 = 人类评审裁决。
