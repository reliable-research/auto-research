# T0 项目与阶段启动卡

| 字段 | 填写 |
| --- | --- |
| 项目 / 日期 / 版本 | specific_idea_llm_loop_invariants / 2026-09-14 / v1.0 |
| 长期问题及其重要后果 | LLM-Assisted Inductive Invariant Generation for Bypassing Loop Unrolling in Bounded Model Checking (BMC)

[Problem Background & Bottleneck]
Bounded Model Checking (BMC, e.g., CBMC) for C software suffers from severe state-space explosion when unrolling loops with large, variable, or unbounded iteration counts (k >= 50). Classical invariant generation tools (such as Houdini, ICE, or Daikon) rely on rigid syntactic predicate templates or abstract interpretation, which frequently fail or time out on programs with multiple loop branches and linear/non-linear arithmetic.

[The LLM Bottleneck & Core Hypothesis]
Directly prompting LLMs to synthesize formal invariants fails because LLMs frequently hallucinate or generate "true but non-inductive" candidate predicates—assertions that hold along standard execution traces but fail the inductive step (consecution: I /\ Guard /\ Body => I') due to missing auxiliary state constraints.
We hypothesize that a synergistic, two-tiered framework can resolve this:
1. Semantic Proposal Tier: Leverage LLM's high-level program reasoning to inspect loop conditions, state mutations, and post-conditions to propose candidate invariants and auxiliary relations.
2. Formal Inductive Verification Tier: Formally verify the candidate assertions against the inductive triplet (Initiation, Consecution, Safety) via automated deduction.
3. Proof Integration: Incorporate sound inductive invariants back into BMC to achieve complete unbounded verification in constant solver time, eliminating the loop unrolling bottleneck.

[Evaluation Dimensions & Scope]
- Scope: ANSI-C programs containing integer arithmetic loops with scalar and multi-path branches.
- Evaluation Metrics: Inductive proof success rate (IPSR), verification speedup and memory footprint reduction against standard BMC loop unrolling across increasing bounds (k = 10, 50, 100, 1000).
- Soundness & Failure Analysis: Categorization of non-inductive failure modes and exploration of automated refinement strategies when candidates fail the consecution check.
 |
| 当前最具体未知 | 待 S1 机会探测明确 |
| 主要贡献类型及次要义务 | 方法 (Method) |
| 当前阶段及进入依据 | S1 / 初始进入 |
| 上游输入版本和证据位置 | 无（项目起点） |
| 本轮完成后要作出的决定 | 决定哪个未知值得投入下一项探测 |
| 本阶段适用必需卡 | S1-C1 至 S1-C6 |
| 当前到期义务 | 交付问题机会卡、线索表与 T5 §1 |
| 已登记的后续义务 | S2 问题合同、S3 假设注册、S5 PoC 协议 |
| 本轮最小产物 | 机会卡、线索来源表、候选取舍记录 |
| 工作预算与单位 | 最大 3 轮审查 |
| 最大复审轮数 / 已用轮数 | 3 / 0 |
| 执行 / 审核 / 决策职能 | Builder / Critic / Controller (Gemini via agy) |
| 首项具体工作 | 梳理初始观察与预期落差，建立候选线索表 |
