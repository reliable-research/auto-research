# AGENT.md

Autonomous Multi-Agent System Specification & Operating Manual for **AutoResearch Codeless** (`Idea_to_Paper_Codeless_Workflow_v4`).

---

## 1. System Architecture: The Multi-Agent Triad

The research workflow is driven by a decentralized, check-and-balance triad of specialized autonomous agents:

```
                  ┌──────────────────────────────┐
                  │    Workflow Orchestrator     │
                  │   (Coordinates 7-Step Loop)  │
                  └──────────────┬───────────────┘
                                 │
         ┌───────────────────────┼───────────────────────┐
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Builder Agent  │────▶│  Critic Agent   │────▶│Controller Agent │
│ (Executor/Author│     │ (Hostile Auditor│     │ (Budget & State │
│  Drafts T5/Out) │     │  48 Card Matrix)│     │  Transition Mgt)│
└─────────────────┘     └─────────────────┘     └─────────────────┘
         ▲                                               │
         │                Decision Actions:              │
         │          - CONTINUE (Advance Stage)           │
         │          - REFINE_INLOOP (Retry Stage) ───────┤
         │          - ROLLBACK (Revert to S_root) ───────┘
         └───────────────────────────────────────────────┘
```

### 1.1 Builder Agent (研究执行者)
- **Primary Mission**: Executes research tasks for the current stage (S1–S8), synthesizes raw intellectual output, resolves outstanding issues from previous audit rounds, and updates the unified research draft (`05_T5_UNIFIED_RESEARCH_DRAFT.md`).
- **Operating Rules**:
  1. Ground all claims, formulas, numbers, and observations in verifiable protocols.
  2. Adhere strictly to the stage's **Minimum Deliverables** and obey the stage's **What is NOT required now** constraints to avoid premature over-engineering.
  3. When in a refinement loop (`REFINE_INLOOP`), make targeted, minimal surgical repairs addressing the specific `acceptance_criteria` of each blocking issue without generating unrequested speculative text.
  4. Synchronize all incremental stage achievements into the single source of truth: the unified working draft (T5).

### 1.2 Critic Agent (严苛审核者)
- **Primary Mission**: Serves as a hostile peer reviewer / Program Committee (PC) member auditing stage deliverables strictly against the stage's 6 designated review cards (from the 48-card catalog).
- **Audit Protocol**:
  1. Inspect specific designated sections (`where_to_check`) using formal verification logic (`how_to_check`).
  2. Output structured JSON strictly adhering to schema:
     ```json
     {
       "card_evaluations": {
         "S1-C1": {"status": "MET|GAP|CONFLICT|N/A", "reason": "...", "location": "..."},
         ...
       },
       "issues": [
         {
           "issue_id": "ISSUE-01",
           "card_id": "S1-C5",
           "severity": "BLOCKING",
           "location": "Section 4.2",
           "actual_content": "...",
           "problem": "...",
           "impact": "...",
           "owner_stage": "S1",
           "minimal_fix": "...",
           "acceptance_criteria": "...",
           "suggested_route": "REFINE_INLOOP|ROLLBACK"
         }
       ]
     }
     ```
  3. **Root-Cause Ownership Principle**: Identify the true upstream origin of an error. For example, if S6 experimental results contradict S3 hypotheses, the issue is assigned to `owner_stage: S3`, triggering an upstream rollback rather than a superficial local patch in S6.
  4. **Strict No-Preference Rule**: The Critic must NEVER raise blocking issues based on subjective prose style or personal aesthetic taste. Every issue must be grounded in an explicit card violation.

### 1.3 Controller Agent (决策与仲裁者)
- **Primary Mission**: Arbitrates transitions based on Critic audit results and the project's state machine rules.
- **State Transition Rules**:
  - `CONTINUE`: Triggered only when all 6 cards of the current stage are `MET` (or justified `N/A`). Advances the pointer to `S_{n+1}`.
  - `REFINE_INLOOP`: Triggered when blocking issues exist whose `owner_stage` equals current stage $S_n$, provided `current_round < max_refine_rounds` (default: 3).
  - `ROLLBACK`: Triggered when an issue identifies a root cause in an upstream stage $S_{\text{root}} < S_n$, or when in-loop refinement budget is exhausted without convergence. Cascades invalidation of all deliverables between $S_{\text{root}}$ and $S_n$.
  - `PAUSE`: Triggered when execution budget/token limits are reached, or unresolvable contradictions require human researcher intervention.

---

## 2. The 8-Stage Research Lifecycle (S1–S8)

| Stage | Name | Core Goal | Minimum Deliverable | What is NOT Required Now |
| :--- | :--- | :--- | :--- | :--- |
| **S1** | **问题发现与价值判断**<br>(Problem Discovery & Value) | Identify genuine unknown, verify that solving it creates value, evaluate detection cost. | S1 Contract Card with Clues C1–C4, Unknown K, Cost T, Stakeholder D. | Formal theoretical proofs, complete code implementation, exhaustive literature surveys. |
| **S2** | **问题定义与研究定位**<br>(Problem Definition & Positioning) | Formalize research question, freeze scope, define metrics, contrast against nearest baselines. | Problem Contract (U, C, G, N, M), Target Archetype, Nearest Baseline Differential Matrix. | Full system architecture, prototype code, benchmark execution. |
| **S3** | **假设与候选机制**<br>(Hypotheses & Mechanisms) | Formulate layered causal hypotheses, specify competing explanations, define falsification lines. | T2 Hypothesis Ledger (Assumptions, Mechanisms, Extrapolations), Falsification Red-lines, Fallback Matrix. | Statistical significance tests, complete experimental runs. |
| **S4** | **方法、理论与实现规格**<br>(Method, Theory & Specs) | Design end-to-end technical specifications, unambiguous module interfaces, and theoretical foundations. | Method Architecture Diagram, Unambiguous Module Interface Signatures, Algorithmic Pseudocode. | Production UI, broad hyperparameter sweeps, cross-platform packaging. |
| **S5** | **PoC 协议与测量准备**<br>(PoC Protocol & Preparation) | Freeze minimal test protocol, lock evaluation datasets, sign pre-committed decision contract. | T3 PoC Decision Contract, Data Role Separation (Dev vs Frozen Eval), Instrumentation Protocol. | Full benchmark sweeps, final publication figures. |
| **S6** | **PoC 执行与证据判定**<br>(PoC Execution & Adjudication) | Execute frozen PoC, collect raw solver/execution traces, adjudicate hypothesis validity. | Raw Evidence Manifest (Run IDs, Git Hashes), PoC Metric Summary Table, Hypothesis Adjudication (`SUPPORTED_IN_SCOPE`). | Sweeping claims of universal generalization. |
| **S7** | **独立确认与证据扩展**<br>(Independent Confirmation & Extension) | Scale experiments across full benchmark suite, run ablation studies, explore failure boundaries. | Full Benchmark Results Matrix, Baseline Comparison Charts, Ablation Analysis, Failure Mode Taxonomy. | Camera-ready paper formatting or bibliography cleanup. |
| **S8** | **论文论证与最终审查**<br>(Paper Argumentation & Audit) | Consolidate full research manuscript, verify number consistency, audit narrative against peer-review standards. | Full Academic Research Manuscript (T5 sections 1–10), Evidence Traceability Index, Honest Limitations Section. | Future work implementations. |

---

## 3. The 48 Review Cards Reference Matrix

Each stage is protected by exactly 6 specialized operational review cards:

```
Stage S1: [S1-C1 线索源自真实问题] [S1-C2 任务条件与对照明确] [S1-C3 谁会因答案改变行动] 
          [S1-C4 未知非平凡可降解] [S1-C5 最便宜探测足以撼动] [S1-C6 取舍而非堆砌产物]
Stage S2: [S2-C1 形式化问题无歧义] [S2-C2 核心指标无古德哈特漏洞] [S2-C3 边界实例覆盖到位]
          [S2-C4 近邻工作实质差异] [S2-C5 贡献类型承诺唯一] [S2-C6 切口具体非大而全]
Stage S3: [S3-C1 承重假设分层解耦] [S3-C2 前提约束与环境依赖明确] [S3-C3 最强竞争解释在场]
          [S3-C4 证伪线与未决区间量化] [S3-C5 候选机制有因果映射] [S3-C6 失败分流动作预先承诺]
Stage S4: [S4-C1 模块接口可无歧义实现] [S4-C2 理论推导或逻辑证明闭环] [S4-C3 关键设计有消融对应]
          [S4-C4 异常与极端输入有安全出口] [S4-C5 关键超参有敏感区间界定] [S4-C6 实现与理论一一映射]
Stage S5: [S5-C1 最小闭环覆盖主因果链] [S5-C2 数据切分严禁先验泄漏] [S5-C3 观测指标抗噪声扰动]
          [S5-C4 判定阈值在执行前冻结] [S5-C5 资源预算与超时红线明确] [S5-C6 负结果分流路径畅通]
Stage S6: [S6-C1 运行记录不可篡改可追溯] [S6-C2 判定严格依据预冻结阈值] [S6-C3 负结果与异常归因到位]
          [S6-C4 假设修正仅限收缩范围] [S6-C5 证据足以支撑推进决策] [S6-C6 交接单记录关键环境细节]
Stage S7: [S7-C1 全量评测无樱桃采摘] [S7-C2 基线对比在同等资源预算下] [S7-C3 机制消融分离核心贡献]
          [S7-C4 失效用例分布与根因清晰] [S7-C5 统计功效与置信度检验充分] [S7-C6 发现具有跨域稳定性]
Stage S8: [S8-C1 论文主线解释知识增量] [S8-C2 每个主要主张有范围匹配证据] [S8-C3 数字方法证明完全一致]
          [S8-C4 相关工作与引用准确公允] [S8-C5 可复现性与局限披露完整] [S8-C6 最终关闭的是实质问题]
```

---

## 4. Standard Academic Deliverables (T0–T5)

Every project maintains 6 canonical markdown records in its workspace directory:

1. **`00_T0_PROJECT_AND_STAGE_CARD.md`**: Project charter, topic definition, archetype selection, and current stage commitment.
2. **`01_T1_REVIEW_AND_REFINE.md`**: Comprehensive ledger of Critic card evaluations, active blocking issues, resolved fixes, and transition reasons.
3. **`02_T2_HYPOTHESES_AND_EVIDENCE.md`**: Cumulative hypothesis ledger (Assumptions, Mechanisms, Extrapolations) tracking evidence states (`UNTESTED`, `SUPPORTED_IN_SCOPE`, `FALSIFIED`).
4. **`03_T3_POC_DECISION_CONTRACT.md`**: Frozen pre-commitment contract establishing pass/fail metric thresholds before running experiments.
5. **`04_T4_ROLLBACK_AND_HANDOFF.md`**: Formal handoff documentation executed during rollbacks, detailing discarded hypotheses and newly discovered constraints.
6. **`05_T5_UNIFIED_RESEARCH_DRAFT.md`**: The living, unified academic paper manuscript incrementally accumulated from S1 to S8.

---

## 5. Experimentation & Anti-Leakage Protocols

When utilizing LLMs for autonomous research generation, the system supports three distinct operational tiers:

### 5.1 Mode 1: Replication / Pre-Seeded
- Used to benchmark the workflow against existing published literature.
- Full or partial paper text is provided as reference context.

### 5.2 Mode 2: Zero-Cheat Blind Exploration
- A bare, one-sentence abstract premise is provided (e.g., *"Using LLMs to generate invariants to bypass loop unrolling"*).
- The system must independently discover problem definitions, inductive failure modes, and formal solvers without hints.

### 5.3 Mode 3: Grounded Specific Idea (Recommended)
- A rigorous, realistic research proposal is provided detailing:
  - Concrete target domain & failure modes (e.g., BMC state-space explosion on C integer loops with $k \ge 50$).
  - Identified theoretical bottlenecks (e.g., template rigidity vs. LLM "true but non-inductive" consecution failures).
  - General hybrid hypothesis (e.g., LLM semantic proposer + automated deductive induction checker).
  - Concrete evaluation dimensions (e.g., IPSR, runtime/memory scaling).
- **Zero-Leakage Invariants**:
  - NO naming of specific target provers (e.g., Vampire) or proprietary languages (e.g., TPTP).
  - NO leaking of internal AST rewrite hacks (e.g., CFG loop splitting/havoc).
  - NO pre-baking of cherry-picked test suite names or final evaluation numbers.

---

## 6. Execution Fail-Safes & Invariants

1. **Anti-Oscillation Guard**: If a candidate repeatedly fails formal solver checks, the Critic mandates an *Unreachable Counterexample Filter* (e.g., bounded reachability check $k=10$) rather than allowing the Builder to oscillate by guessing ad-hoc inequality patches.
2. **Anti-Hallucination Anchor**: All empirical numbers in S7 and S8 must match the exact values logged in S6 execution traces. Any discrepancy triggers an immediate `S8-C3` blocking violation.
3. **Single Source of Truth**: Intermediate thought processes in scratchpads must never supersede the checked-in state in `project_state.json` and `05_T5_UNIFIED_RESEARCH_DRAFT.md`.
