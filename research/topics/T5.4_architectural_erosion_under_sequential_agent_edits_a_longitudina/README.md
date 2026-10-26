---
code: T5.4
title_cn: "多轮编辑下的架构侵蚀"
label: "[证据+机制]"
parent_topic: "T5. 设计约束合规（coding agent）"
source: "../../38_topics.txt"
---

# T5.4 多轮编辑下的架构侵蚀

标签：[证据+机制]

父 Topic：T5. 设计约束合规（coding agent）

**T5.4 多轮编辑下的架构侵蚀** [证据+机制]
> Architectural Erosion under Sequential Agent Edits: A Longitudinal Measurement

核心问题：连续多个任务的 agent patch 会不会渐进侵蚀架构（每步都过测试，累计却腐蚀分层/依赖结构）？侵蚀速率与什么有关？
最小实验：同一 repo 上串行执行任务序列，逐步测架构度量（循环依赖、分层违规、复杂度）漂移。真值 = 静态分析度量。
