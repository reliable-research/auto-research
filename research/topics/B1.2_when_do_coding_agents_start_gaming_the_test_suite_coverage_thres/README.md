---
code: B1.2
title_cn: "可见测试过拟合的出现边界"
label: "[边界]"
parent_topic: "B1. Verifier 充分性（agent / 代码场景）"
source: "../../38_topics.txt"
---

# B1.2 可见测试过拟合的出现边界

标签：[边界]

父 Topic：B1. Verifier 充分性（agent / 代码场景）

**B1.2 可见测试过拟合的出现边界** [边界]
> When Do Coding Agents Start Gaming the Test Suite? Coverage Thresholds for Visible-Test Overfitting

核心问题：可见测试覆盖度降到什么程度时，agent 的"过可见测试但挂隐藏组合测试"行为开始出现？
最小实验：系统性控制可见测试套件的变异体杀伤率（mutation score），测 visible-pass 与 held-out-pass 的缺口随充分性变化的曲线。真值 = 隐藏测试与变异体。这是经典 mutation testing 充分性理论对 agent 评价面的直接迁移，全语料中该框架命中≈0。
