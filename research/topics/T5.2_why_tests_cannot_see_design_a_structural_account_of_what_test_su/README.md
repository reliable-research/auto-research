---
code: T5.2
title_cn: "测试盲区的结构分析"
label: "[机制]"
parent_topic: "T5. 设计约束合规（coding agent）"
source: "../../38_topics.txt"
---

# T5.2 测试盲区的结构分析

标签：[机制]

父 Topic：T5. 设计约束合规（coding agent）

**T5.2 测试盲区的结构分析** [机制]
> Why Tests Cannot See Design: A Structural Account of What Test Suites Fail to Express

核心问题：测试套件结构性表达不了哪类性质（横切关注点、时序性质、命名/分层惯例）？盲区可否用变异体探测系统化刻画？
最小实验：设计约束违规型变异体（违反惯例但功能等价），测既有测试套件的杀伤率——杀不死的变异体即测试盲区的机械证据。mutation testing 框架的又一处直接迁移。
