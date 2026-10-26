---
code: B1.4
title_cn: "verifier 组合的健全性算术"
label: "[矛盾]"
parent_topic: "B1. Verifier 充分性（agent / 代码场景）"
source: "../../38_topics.txt"
---

# B1.4 verifier 组合的健全性算术

标签：[矛盾]

父 Topic：B1. Verifier 充分性（agent / 代码场景）

**B1.4 verifier 组合的健全性算术** [矛盾]
> Two Sound Checks, One Unsound Gate: Emergent Shortcuts under Verifier Composition

核心问题：两个各自健全的 verifier，其合取/析取组合是否仍健全？组合是否打开单个检查不存在的捷径？
最小实验：构造单检查无捷径、组合后有捷径的任务对（如"通过 A 的方式恰好绕开 B 的检查面"）；验证组合缺口的存在性与出现条件。反直觉结论若成立，对所有多重校验管线是普适警告。
