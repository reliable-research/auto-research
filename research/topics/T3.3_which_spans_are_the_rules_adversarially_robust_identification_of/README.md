---
code: T3.3
title_cn: "约束识别问题"
label: "[边界]"
parent_topic: "T3. Memory 约束保持（窄环，4 条）"
source: "../../38_topics.txt"
---

# T3.3 约束识别问题

标签：[边界]

父 Topic：T3. Memory 约束保持（窄环，4 条）

**T3.3 约束识别问题** [边界]
> Which Spans Are the Rules? Adversarially Robust Identification of Governance Constraints for Pinning

核心问题：pinning 的前提是先认出哪些上下文片段是治理约束——对抗性措辞（把约束伪装成闲聊、把闲聊伪装成约束）下识别可靠吗？
最小实验：对抗改写的约束/非约束配对集，测识别器的错保率与漏保率。
