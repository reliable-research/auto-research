---
code: B4.6
title_cn: "验证感知的编码 agent 推理服务经济学"
label: "[证据]"
parent_topic: "B4. 预算感知的测试时计算与验证分配"
source: "../../trend_scan_2026-08.md §2.5 + 2026-08-13 occupancy sweep"
---

# B4.6 验证感知的编码 agent 推理服务经济学

标签：[证据]

父 Topic：B4. 预算感知的测试时计算与验证分配（2026-08-13 扩展）

**B4.6 验证步作为一等调度单元** [证据]
> Verification-Aware Serving Economics for Coding Agents

核心问题：编码 agent 会话中，多大比例的 token/延迟/美元是验证诱发的（测试运行、失败重试环、回喂的测试输出上下文），验证输出对前缀缓存复用造成多少破坏？可证伪声明：把验证步当作一等调度单元（lint ≪ 单测 ≪ 全套件的异构成本 × 异构信息价值，配合对预测通过的验证做投机续跑）的调度策略,在 trace-replay 服务仿真（vLLM/SGLang）下，同等解决率时 $/resolved-task 降低 ≥X%（相对 agent 原生策略）。

最小实验：TraceLab 公开 trace（~4,300 会话、430K 工具调用，test/build/edit 可区分）+ 自测 SWE-bench 运行做补充；(1) 测量验证诱发成本占比与 KV 失效模式；(2) 构建 cost-optimal 验证调度策略并在重放仿真中对比原生策略。无需数据中心访问 —— 这是本家族少见的小组可行角度。

## 证据基础（2026-08-13 扫描）

- 纯 workload characterization 已被双重占据：TraceLab (2606.30560, 公开 trace) + Microsoft Copilot 生产级 (2608.00101, 3.2M 用户/95T token, 不放 trace)。第三篇 characterization 没有空间。
- KV-cache-for-agents 与 agentic scheduling 各已 5+ 篇（KVFlow, Irminsul 2605.05696, SMetric 2607.08565, SAGA 2605.00528, 2605.06110 等）。
- 最近邻：Cost-Aware Speculative Execution (2606.07846) —— 美元计价的投机执行,但（a）无真实 trace 落地（b）不把 verify 决策本身当调度对象（c）不建模验证输出的 KV 破坏。SpecBox (2607.23933) 只做 sandbox 预热机制。2504.07347 的 Generate/Verify 排队论是理论先声。
- 与本家族的接口：B4.5（选择性验证）问"哪些轨迹值得验证"，B4.6 问"验证在服务栈上何时/以何粒度跑" —— 估计量不同（B4.5: 精度-预算前沿；B4.6: $/resolved-task at matched resolve rate）。

## 新颖性台账

| 声明 | 最近邻 | 差量 | 立场 |
|---|---|---|---|
| 验证诱发成本占比 + KV 破坏测量（真实 trace） | TraceLab 2606.30560（泛特征无验证维度） | 验证步语义 + 缓存交互 | novel |
| verify 决策的成本最优调度 | 2606.07846（泛投机、无 trace 落地） | 决策对象换轴 + trace-grounded | novel |
| 投机续跑过预测通过的验证 | SpecBox 2607.23933（机制无策略/经济学） | 策略层 + 美元目标函数 | somewhat-novel |

风险时钟：投机/验证重叠子领域正快速填充（2026-06 起 4 篇），但 trace-grounded 验证经济学切片仍空。TraceLab trace 公开是可行性护城河失效的信号 —— 别人同样能用，建议 1–2 个季度内出测量结果（阶段 1 可独立成文投 MLSys/EuroSys measurement track）。

审稿场景：MLSys / EuroSys / ATC（系统测量+策略）；或 ICLR（若强调策略学习）。
