---
code: B1.3
title_cn: "多步任务的检查点绕过"
label: "[证据]"
parent_topic: "B1. Verifier 充分性（agent / 代码场景）"
source: "../../38_topics.txt"
---

# B1.3 多步任务的检查点绕过

标签：[证据]

父 Topic：B1. Verifier 充分性（agent / 代码场景）

**B1.3 多步任务的检查点绕过** [证据]
> Milestone Satisfaction without Prerequisite State: Checkpoint Bypass in Multi-Step Agent Verification

核心问题：中间里程碑 verifier 可否在不满足前置状态的情况下被逐个满足（乱序、跳步、状态注入）？
最小实验：带依赖图的多步任务，每个里程碑独立校验；测"全部里程碑通过但端到端状态不一致"的比例。真值 = 终态一致性检查。
