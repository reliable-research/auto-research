---
code: B3.1
title_cn: "探针集的充分性设计"
label: "[证据]"
parent_topic: "B3. 跨版本行为漂移 / 纵向审计"
source: "../../38_topics.txt"
---

# B3.1 探针集的充分性设计

标签：[证据]

父 Topic：B3. 跨版本行为漂移 / 纵向审计

**B3.1 探针集的充分性设计** [证据]
> What Probes Predict Breakage? Minimal Probe-Set Design for Version-Drift Auditing

核心问题：哪个最小探针族（能力/拒答边界/格式偏好/校准/安全行为）对下游破坏最有预测力？
最小实验：在已发生的版本对上回溯：用各探针族的漂移量预测真实下游任务的行为变化，比较预测力。真值 = 同一输入集的跨版本输出差分。
