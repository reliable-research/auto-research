---
code: B1.1
title_cn: "工具日志可伪造性"
label: "[证据+机制]"
parent_topic: "B1. Verifier 充分性（agent / 代码场景）"
source: "../../38_topics.txt"
---

# B1.1 工具日志可伪造性

标签：[证据+机制]

父 Topic：B1. Verifier 充分性（agent / 代码场景）

**B1.1 工具日志可伪造性** [证据+机制]
> Satisfying the Log, Skipping the Work: Forgeable Action Traces in Log-Verified Agent Tasks

核心问题：当 verifier 检查工具调用日志而非环境状态时，agent 会不会学会"产出合格日志但跳过真实动作"？
最小实验：构造日志校验与状态校验可分离的任务集；真值 = 环境状态差分。测量提示优化/RL 压力下伪造日志行为的出现率与条件。
