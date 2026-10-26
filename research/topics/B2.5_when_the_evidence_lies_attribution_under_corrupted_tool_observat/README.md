---
code: B2.5
title_cn: "观测污染的归因盲区"
label: "[机制]"
parent_topic: "B2. 失败归因（plan / tool / execution）"
source: "../../38_topics.txt"
---

# B2.5 观测污染的归因盲区

标签：[机制]

父 Topic：B2. 失败归因（plan / tool / execution）

**B2.5 观测污染的归因盲区** [机制]
> When the Evidence Lies: Attribution under Corrupted Tool Observations

核心问题：失败源于工具返回了错误但格式合法的观测时，归因方法是否系统性地把责任错记到 plan 或 execution 层？为什么？
最小实验：注入语义错误但语法合法的工具输出，测主流归因思路的错记率与错记方向。

---

## B3. 跨版本行为漂移 / 纵向审计
