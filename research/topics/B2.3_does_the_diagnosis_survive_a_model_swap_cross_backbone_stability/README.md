---
code: B2.3
title_cn: "归因的跨模型稳定性"
label: "[矛盾]"
parent_topic: "B2. 失败归因（plan / tool / execution）"
source: "../../38_topics.txt"
---

# B2.3 归因的跨模型稳定性

标签：[矛盾]

父 Topic：B2. 失败归因（plan / tool / execution）

**B2.3 归因的跨模型稳定性** [矛盾]
> Does the Diagnosis Survive a Model Swap? Cross-Backbone Stability of Failure Attribution

核心问题：同一任务失败，换底层 LLM 后归因是否落到同一层？若归因高度模型特异，"诊断"就不是任务性质而是模型性质。
最小实验：同一故障注入任务集跑多个模型家族，测归因标签的跨模型一致率。结论无论正反都有信息量。
