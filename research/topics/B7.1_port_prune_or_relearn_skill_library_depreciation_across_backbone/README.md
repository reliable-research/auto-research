---
code: B7.1
title_cn: "换骨干后的技能库折旧：移植、裁剪还是重学"
label: "[证据]"
parent_topic: "B7. Agent 记忆/技能生命周期经济学"
source: "../../trend_scan_2026-08.md §2.3 + 2026-08-13 occupancy sweep"
---

# B7.1 换骨干后的技能库折旧：移植、裁剪还是重学

标签：[证据]

父 Topic：B7. Agent 记忆/技能生命周期经济学（2026-08-13 新增家族）

**B7.1 技能库跨模型代际折旧** [证据]
> Port, Prune, or Relearn: Skill-Library Depreciation Across Backbone Upgrades

核心问题：在弱骨干下学到的技能库，换到强骨干后是否从资产变成负债（强模型+旧库 < 强模型裸跑，且差距超出可解释的能力差）？基于逐技能折旧测量的 retire/refresh 策略，能否在同等成功率下以更低总 token 成本击败"永不退役"和"全量重学"两个基线？

最小实验：固定一条任务流（如 MBPP+/SWE-bench 子集 + ALFWorld），在 2–3 个真实模型代际上重放（例如 GPT-4 级 → GPT-5 级，或 sonnet-4 → opus-5）；每个技能记账（获取成本、每次复用的边际收益、负迁移事件），拟合逐技能折旧曲线；用折旧估计驱动 retire/refresh 策略，对比 never-retire / full-relearn / no-library 三基线的 (总成本, 成功率) 前沿。真值全程机械（执行结果 + token 计费）。

## 证据基础（2026-08-13 扫描）

- 技能库 staleness/rot 的**诊断**已被占据：Library Drift (2605.19576, 无界积累→低于无库基线, +0.0pp vs 人工 +16.2pp)、Skill Drift Is Contract Violation (2605.10990, 880 对退化基准)、SkillOps (2605.13716)。但它们全部只测环境/代码库漂移轴，**无一测模型代际轴**。
- 经济学框架有概念无实验：Token Economics (2605.09104) 把技能当资本品但没有逐技能回本曲线；2606.09421 只做单次调用成本，摘要明示不做摊销。
- 跨模型只有快照式迁移精度：AFTER (2606.23127) 报 73.1% cross-model accuracy，但没有成本记账、没有"迁移决策"。
- 两篇 survey（2607.10113, 2606.11435）点名 lifecycle/metric 缺口而未测量 —— 社区已看见问题，窗口正在收窄。

## 新颖性台账

| 声明 | 最近邻 | 差量 | 立场 |
|---|---|---|---|
| 模型代际是技能库 staleness 的独立轴 | Library Drift 2605.19576（环境轴） | 换轴：backbone 版本作为处理变量 | novel |
| 逐技能折旧曲线 + 回本视界估计量 | Token Economics 2605.09104（概念框架） | 从 framing 到 measured estimand | novel |
| retire/refresh 策略击败两基线 | SkillsVote 2605.18401（治理机制无经济学） | 用折旧测量驱动决策并给成本前沿 | somewhat-novel |

风险时钟：诊断文献 5 篇/季度的速度在填充；每次大模型发版都是别人也能用的自然实验。建议 6 个月内出首个代际重放结果。占位判定：原"技能库经济学"核心已 TAKEN，本角度是扫描确认的最锐利幸存角。

审稿场景：ICLR/ICML（agent+eval track）或 FSE/ICSE（若以编码技能库为主载体）。
