---
code: T3.4
title_cn: "规模化 pinning 的开销边界"
label: "[资源]"
parent_topic: "T3. Memory 约束保持（窄环，4 条）"
source: "../../38_topics.txt"
---

# T3.4 规模化 pinning 的开销边界

标签：[资源]

父 Topic：T3. Memory 约束保持（窄环，4 条）

**T3.4 规模化 pinning 的开销边界** [资源]
> Pinning at Scale: Token Overhead versus Violation Trade-offs under Hundreds of Constraints

核心问题：约束从个位数增长到数百条时，全量 pinning 的 token 开销何时反噬任务性能？选择性 pinning 的选择策略是什么？
最小实验：约束数量扫描下测违规率-开销-任务成功率三方权衡。

---
