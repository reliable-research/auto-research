---
code: B8.1
title_cn: "规范漂移：agent 互操作协议的差分一致性测量"
label: "[证据]"
parent_topic: "B8. Agent 协议治理与一致性"
source: "../../trend_scan_2026-08.md §2.1 + 2026-08-13 occupancy sweep"
---

# B8.1 规范漂移：agent 互操作协议的差分一致性测量

标签：[证据]

父 Topic：B8. Agent 协议治理与一致性（2026-08-13 新增家族）

**B8.1 跨规范版本的差分一致性** [证据]
> Spec-Drift: Differential Conformance Testing Across Agent-Protocol Versions (MCP / A2A)

核心问题：MCP 规范快速迭代（2026-07-28 RC；A2A 1.0.1 扩展 2026-05）。可证伪声明：对规范版本 N→N+1 的每条 normative-clause 差量，已部署的 server/client 存在可测量的**发散窗口** —— 行为既不符合 N 也不符合 N+1，且窗口内可表达的 authority 约束静默降级为 visibility-only。真值机械：clause diff → 生成一致性探针 → 对真实部署 server 做 wire-level pass/fail。

最小实验：取 MCP 两个相邻规范版本，diff 出 normative 条款集；为每条生成探针（复用 2605.22333 已证明可发表的 deployed-measurement 方法学）；扫描公开 remote MCP server 目录，按（版本合规矩阵 × 时间）报告发散窗口分布与 authority→visibility 降级案例。

备选主叙事（若差分角度受阻）：**运行时行为违规按规范可表达性分类** —— 每条观察到的违规被机械标注为"可表达但未强制"vs"规范不可表达"，把 Governance Gaps (2606.31498) *论证出的* gap matrix 变成*测量出的*。此角度处于 AgentRFC 与 2606.28679 之间的窄缝，被 AgentRFC 完整版吸收的风险较高。

## 证据基础（2026-08-13 扫描）

- AgentRFC (2603.23801)：spec→typed IR→TLA+ 模型检查→SDK 反例重放，已占"规范侧一致性检查"；但 artifact 因 coordinated disclosure 未公开，完整评估被推迟 —— 公开可复现 artifact 本身是差量之一。
- Capability Gates Are Not Authorization (2606.28679)：在框架层占据 visibility-vs-authority 概念轴，但完全不触协议规范。
- HCP (2606.29073)：8 条安全不变式 + 10 攻击基准，但主张替换执行层而非测量既有规范的缺口。
- 无人做纵向/差分一致性；2605.22333（remote MCP server 认证测量）证明对真实部署做测量研究可发表。
- 环境信号：NSA/CISA 2026-06 发布 MCP 安全 CSI —— 政策侧需求真实存在。

## 新颖性台账

| 声明 | 最近邻 | 差量 | 立场 |
|---|---|---|---|
| 跨版本差分一致性 + 发散窗口估计量 | AgentRFC 2603.23801（单版本、规范侧） | 纵向轴 + 部署侧 wire-level 测量 | novel |
| authority 约束在版本迁移中降级为 visibility | 2606.28679（框架层静态审计） | 协议 wire 对象 + 时间维 | novel |
| 测量版 gap matrix | Governance Gaps 2606.31498（论证式） | argued → measured | somewhat-novel |

风险时钟：**月级而非年级**。AgentRFC 完整版可能吸收邻缝；HCP 的 metadata non-authority 不变式与 authority 轴部分重叠。规范本身在动 —— 既是机会（差分角度只在规范快速迭代期存在）也是保质期。若 3 个月内不能出首个 clause-diff 探针管线，建议降级持有。

审稿场景：USENIX Security / NDSS（测量研究）或 FSE/ICSE（一致性测试框架）。
