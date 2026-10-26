---
code: B7.2
title_cn: "投毒半衰期：记忆管理策略下的存活分析"
label: "[证据]"
parent_topic: "B7. Agent 记忆/技能生命周期经济学"
source: "../../trend_scan_2026-08.md §2.4 + 2026-08-13 occupancy sweep"
---

# B7.2 投毒半衰期：记忆管理策略下的存活分析

标签：[证据]

父 Topic：B7. Agent 记忆/技能生命周期经济学（2026-08-13 新增家族）

**B7.2 长驻 agent 记忆中毒的 hazard 曲线** [证据]
> Poison Half-Life: Survival Analysis of Agent Memory Poisoning Under Memory-Management Policies

核心问题：把每条注入的毒化声明当作存活分析的受试对象，测其在持续良性流量与记忆管理动态（摘要、整合/反思、驱逐/TTL、去重）下的中和时间。可证伪核心假设：**提升效用的记忆管理策略（激进整合/摘要）会延长而非缩短毒化半衰期** —— 因为 laundering（2605.16746：对抗内容以检测器不可见形式挺过摘要）把可检测的毒转化为不可见的持久影响；即 MemSecBench 当作"修复"处理的 Forget 阶段，在现实策略下实为放大阶段。

最小实验：复用已发表攻击与防御作 treatment（Memory Sandbox 2605.08442、A-MemGuard 2510.02373、MemLineage 2605.14421、trust-decay 2601.05504），在 (记忆策略 × 防御) 网格上跑长时段良性交互流，间隔性机械验收探针测毒化声明是否仍被采纳；输出 censoring-aware 半衰期估计量与 per-cell hazard 曲线。若半衰期对记忆策略不变，假设被干净证伪。无需新攻击，纯防御/测量。

## 证据基础（2026-08-13 扫描）

- 核心占位已发生：MemSecBench (2607.27080, 2026-07) 已做 Write–Execute–Forget 检查点式持久性基准（84.2% persistence）；2605.08442 已做 6 防御 × 21 模型的分层评测（发现注入-执行解耦）。"检查点持久性 + 防御对比"的直接组合有 incremental-benchmark 被拒风险。
- 本角度的差量：**连续/纵向 hazard 估计量**（非固定检查点二值）、laundering-放大假设（连接 2605.16746 与 2607.27080 两条尚未被连接的发现）、把记忆策略本身当处理变量。
- 备选（若被质疑）：多 agent 共享记忆中的毒化**传染再生数** —— Byzantine 防御线 (2605.09076, 2608.04366) 只建防御，无人把传播动力学当估计量。

## 新颖性台账

| 声明 | 最近邻 | 差量 | 立场 |
|---|---|---|---|
| 毒化声明的存活/半衰期估计量 | MemSecBench 2607.27080（固定检查点二值） | 连续时间 + censoring-aware 存活分析 | novel |
| 整合/摘要放大毒化持久性 | State Contamination 2605.16746（单通路机制发现） | 升级为跨策略量化假设并可证伪 | novel |
| 已发表防御在纵向协议下头对头 | 2605.08442（短程分层评测） | 时间维 + 策略×防御交互 | somewhat-novel |

风险时钟：该子领域 2026 年 Q2 起每月 3–5 篇；OWASP ASI06 已收录 memory poisoning。半衰期角度目前无人占据，但 MemSecBench 团队是天然的快速跟进者。建议以安全场馆节奏推进（USENIX Sec '27 cycle / CCS）。

审稿场景：USENIX Security / CCS（测量+防御评测）或 ICLR safety track。
