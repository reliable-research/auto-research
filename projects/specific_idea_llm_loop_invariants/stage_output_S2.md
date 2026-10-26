# 阶段 S2 交付产物：问题定义与研究定位 (Problem Definition & Research Positioning)
**项目**：`specific_idea_llm_loop_invariants`  
**阶段**：S2 (第 3 轮审查交付) | **主稿版本**：v0.4 | **主要贡献类型**：方法 (Method)

---

## 1. S2 问题合同卡 (Problem Contract Card: U-C-I-B-X-R-T-M-G-N-K)

| 合同要素 | 要素定义 | 本课题具体实例化承诺 |
| :--- | :--- | :--- |
| **研究单位 (U)** | 实验与验证的不可分割基本对象 | 包含单个或级联循环、且循环体存在多路径条件分支与线性整数算术（LIA）的规范 ANSI-C 源代码函数。 |
| **测试条件 (C)** | 触发核心瓶颈的外部运行环境与输入特征 | 循环展开上界 $k \ge 50$（或动态不可确定上界），目标断言位于循环后置（Safety Check），BMC 直接展开耗时 $\ge 30\text{s}$ 或出现内存超限（OOM）。 |
| **允许信息 (I)** | 算法/生成器在运行期允许消费的输入源 | 目标 C 程序的静态抽象语法树（AST）、控制流图（CFG）、循环体代码、前置/后置规约，以及 SMT-LIB2 求解器返回的反例赋值模型（Counterexample Trace/Model）。**严禁**使用外部测试用例的动态执行轨迹作弊引入预置不变量。 |
| **资源约束 (B)** | 评估或运行必须遵守的算力/时间/通信预算 | 单个程序候选生成与归纳验证总超时（Timeout）设为 $300\text{s}$；SMT 单步求解超时设为 $10\text{s}$；LLM 交互上限不超过 5 轮查询（Refinement Steps $\le 5$），调用温度 $T=0$。 |
| **可变对象 (X)** | 本课题研究设计中可被自由修改与优化的变量 | **两层协同架构实现**：(1) LLM 语义提议层的提示词模式与程序切片抽象策略；(2) 辅助状态谓词推导与反例清洗过滤机制；(3) 形式化归纳三元组（Initiation, Consecution, Safety）验证与多轮反馈精化协议。 |
| **对照基线 (R)** | 用于衡量实质改进的已有方法基准 | 1. **纯有界展开基线**：原生 CBMC (v5.95) 纯展开模式（Unrolling with incremental $k$）；<br>2. **经典不变式合成工具**：Daikon（动态推断）、Houdini（模板筛选）、LoopInvGen / Code2Inv（经典反例引导合成）；<br>3. **朴素 LLM 辅助基线**：直接单轮/多轮 Prompting（如 GPT-4o / Claude-3.5-Sonnet 直接输出 `__CPROVER_loop_invariant`）。 |
| **目标期望 (T)** | 方法成功成立的判别终点 | 在不进行大步长循环展开的前提下，生成出能够经一阶逻辑 SMT 严格自持证明的归纳不变量 $I$，使得 BMC 仅需验证三元组（Initiation, Consecution, Safety）即闭合安全性证明。 |
| **度量指标 (M)** | 评估目标达成程度的定量度量集合 | 1. **归纳证明成功率 (IPSR)**：经 SMT 证明完全闭合的基准测试用例占比；<br>2. **验证加速比 (Speedup)**：相对于基线 R 在 $k=10, 50, 100, 1000$ 时的求解墙钟时间比率（Wall-clock Time Ratio）；<br>3. **内存缩减率 (Memory Reduction)**：BMC 求解峰值内存（Peak RSS）降低百分比；<br>4. **平均收敛轮次 (Avg. Iterations)**：从候选提出到归纳闭合所需的 LLM 反馈精化轮次。 |
| **核心范围 (G)** | 明确承诺解决的程序与逻辑域边界 | 属于量词自由线性整数算术（QF_LIA）理论体系内的 ANSI-C 程序：包含标量累加、双/多变量耦合递推、多路径 `if-else` 分支的单层及级联循环。 |
| **排除范围 (N)** | 明确界定不作为本阶段目标的外围场景 | 包含非线性算术除法/乘方（QF_NIA）、复杂指针算术与堆内存动态重分配、递归调用、并发多线程交互数据竞争。 |
| **关键未知 (K)** | 本研究试图解答的深层科学/工程未知 | 为什么 LLM 能够准确捕捉程序宏观业务语义，却系统性缺失归纳封闭所需的低级不可达伪反例隔离谓词？如何以最小形式化开销自动推导出该“辅助缝合约束（Auxiliary Constraint）”？ |

---

## 2. 边界实例表 (Scope Boundary Cases: In-Scope vs. Out-of-Scope)

| 编号 | 类别 | 代码/问题模式特征 | 归入/排除判据 (G/N Rationale) | 理论与工具链支撑能力 |
| :---: | :---: | :--- | :--- | :--- |
| **G-1** | 核心范围 (G) | **多变量对称/交替递增多路径循环**<br>`while(i < N) { if(c) { x++; y+=2; } else { x+=2; y++; } i++; } assert(x + y == 3*i);` | 状态变量为标量整数，控制流具有交替分支路径，后置断言涉及变量间线性算术关联。属于典型 QF_LIA 域，经典抽象解释容易过度泛化，LLM 易漏掉 `x + y == 3*i` 与循环守卫的中间偶合状态。 | SMT 理论完全可判定 (QF_LIA)；CBMC 原生展开在 $N \ge 10^6$ 时超时，归纳法只需常数时间校验。 |
| **G-2** | 核心范围 (G) | **阶段式相变/标志位触发循环 (Phase-change Loop)**<br>`while(i < 100) { if(flag) x++; else { y++; if(y>10) flag=1; } i++; }` | 存在路径控制变量与布尔状态翻转，断言需要分段（Piecewise）或蕴含式不变量表达（如 `y <= 10 || flag == 1`）。 | 逻辑属于命题与线性算术组合，形式化检验可在秒级判定。 |
| **N-1** | 排除范围 (N) | **非线性多项式变换循环**<br>`while(x < N) { y = x * x; x++; } assert(y < N*N);` | 涉及非线性整数乘法（QF_NIA）。目前一阶 SMT 求解器（如 Z3/CVC5）对 NIA 不保证完全判定性，归纳检查本身可能陷入 Unknown 或不可预测超时，会污染对“不变量生成方法本身有效性”的衡量。 | 超出判定理论范畴，引入额外不可控求解瓶颈。 |
| **N-2** | 排除范围 (N) | **深度动态堆分配与链表遍历**<br>`struct Node *p = head; while(p) { p = p->next; }` | 涉及分离逻辑（Separation Logic）与堆形态分析（Shape Analysis），归纳三元组构建超出标准一阶 BMC 不变量插入语法范畴。 | 工具链需要专用形状分析器支持，偏离本课题主攻的 BMC 循环展开爆炸痛点。 |
| **N-3** | 排除范围 (N) | **非确定性并发交错 (Multi-threaded Concurrency)**<br>`pthread_create(...)` 线程内共享变量竞争循环。 | 并发不变式依赖 Owicki-Gries 或 Rely-Guarantee 关系体系，而非纯循环归纳不变量。 | 干扰归纳步检验的因果链隔离。 |

---

## 3. 近邻工作与实质差异表 (Related Work & Substantial Delta)

| 对比维度 | 经典模板/学习合成: Code2Inv (PLDI'20) / LoopInvGen (CAV'20) | 纯大模型直接驱动: LLM-Inv / Direct Prompting (Ryan et al., 2024) | 本研究方法 (Two-Tiered Co-Verification Framework) |
| :--- | :--- | :--- | :--- |
| **候选假设空间生成机制** | 依赖固定的语法模板族（Grammar Templates）或决策树/图神经网络（GNN）搜索，表达能力受限于预定义谓词算子。 | 开放式黑盒生成，利用自然语言和代码预训练先验，自由提出任意复杂算式。 | **LLM 语义提议 + 符号导向受限投影**：利用 LLM 提取复杂跨变量关系候选，自动将其规范化映射到 QF_LIA 语法范畴内。 |
| **反例处理与反馈机制** | 标准反例引导抽象精化（CEGAR/ICE）：区分正例、反例与蕴含例，利用精确数值点求解。但面对多变量组合爆炸，采样代价极高。 | 将 SMT 报错反例原始文本或变量赋值（如 `x=0, y=-1`）直接塞回 Prompt，模型极易产生震荡、忽略历史或过度保守退化。 | **伪反例可达性前向修剪 + 辅助补丁谓词隔离**：引入轻量级前置约束检验，识别“伪反例（Spurious Counterexample）”，向 LLM 提供具备程序路径语义的归纳阻碍诊断信息。 |
| **与 BMC/求解器集成深度** | 通常作为外部独立生成器运行，未能结合 BMC 内部符号执行收集的前置条件与符号路径约束。 | 仅进行表面断言生成，容易产生不可判定的复杂形式，且无法保证生成谓词满足 BMC 语法规范。 | **紧耦合闭环验证**：利用 BMC 提取初始约束与循环摘要，将检验成功的自持不变量即时作为假设前提（Assumption）注入 CBMC，彻底免除 unrolling 过程。 |
| **根本实质差异 (Substantial Delta)** | 解决了传统方法在多变量/多路径上模板组合爆炸的问题；攻克了纯 LLM 无法跨越的“轨迹真实但归纳步断裂”的幻觉缺陷。 |

---

## 4. 后续审查适用卡与替代义务 (Applicable Verification Cards & Commitments)

由于本研究的主要贡献类型确立为 **方法 (Method)**，在后续开发与审查轮次中必须履行以下规范义务：

1. **适用卡类型**：
   - **T2 机制与算法设计卡 (S3 交付)**：必须清晰刻画“两层协同流水线”的形式化运行规约、LLM Prompt 模板定义、以及 SMT 反例诊断分类算法。
   - **T4 实证评估与对比基准卡 (S4 交付)**：必须在 SV-COMP `loop-invariants` 与标准基准集上完成严格的对比实验设计。
2. **形式化替代义务 (Replacement Commitments)**：
   - **严禁以工程微调替代形式化严谨性**：后续阶段不得将工作重心滑向无理论解释的“提示词魔法（Prompt Engineering）”，必须给出反例分类与辅助约束补充的形式化收敛判据。
   - **完备性与可靠性边界承诺**：必须保证经本框架证明通过的程序不变量具有 100% 的形式化可靠性（Soundness由求解器三元组保证，绝不因 LLM 幻觉产生假阴性/假阳性遗漏）。

---

## 5. T5 统一工作底稿 §2 更新 (Unified Research Draft Section 2)

```markdown
## 2 问题定义与研究定位（S2）

### 2.1 形式化问题模型 (Formal Problem Formulation)
设目标程序为一个四元组 $P = (V, \text{Init}, \mathcal{T}, \text{Safe})$，其中：
- $V$ 为有限标量整数变量集合，其状态空间为 $\mathcal{S}$；
- $\text{Init}(V)$ 为初始状态断言；
- $\mathcal{T}(V, V')$ 为由循环体条件分支及状态跃迁决定的转移关系谓词（Transition Relation）；
- $\text{Safe}(V)$ 为待验证的循环后置安全规约。

**经典 BMC 瓶颈**：标准 BMC 对循环施加展开界限 $k$，将转移公式展开为：
$$ \Phi_k = \text{Init}(V_0) \wedge \bigwedge_{i=0}^{k-1} \mathcal{T}(V_i, V_{i+1}) \wedge \neg \text{Safe}(V_k) $$
当循环上界无界或 $k \ge 50$ 时，公式规模与求解器搜索空间呈组合式爆炸。

**归纳不变量求解合同**：寻找一个由一阶线性算术公式构成的归纳不变量 $I(V)$，满足归纳证明三元组：
1. **初始步 (Initiation)**: $\forall V. \; \text{Init}(V) \implies I(V)$
2. **归纳步 (Consecution)**: $\forall V, V'. \; I(V) \wedge \mathcal{T}(V, V') \implies I(V')$
3. **安全性 (Safety)**: $\forall V. \; I(V) \implies \text{Safe}(V)$

**研究任务目标**：构建映射机制 $\mathcal{M}: P \xrightarrow{\text{LLM} \oplus \text{SMT}} I$，使得在限定时间 $B$ 内，自动合成满足三元组的有效自持不变量 $I$，使 CBMC 的验证复杂度由 $\mathcal{O}(k)$ 降维至 $\mathcal{O}(1)$ 验证步。

### 2.2 问题范围与边界实例界定
- **纳入范围 (In-Scope, G)**：ANSI-C 规范代码，循环体逻辑符合量词自由线性整数算术（QF_LIA），包含多路径 `if-else` 分支与标量状态交替依赖。
- **排除范围 (Out-of-Scope, N)**：涉及非线性算术（QF_NIA）、动态指针链表堆分配、以及并发共享内存交错程序。

### 2.3 近邻工作对比与定位
相较于经典模板枚举（Code2Inv, LoopInvGen）受制于预设多项式模板爆炸，以及纯 LLM Prompting 饱受“反例归纳步断裂与伪反例震荡”的缺陷，本课题定位为**首个结合 LLM 语义模式推测与轻量级伪反例可达性修剪的归纳闭环合成方法**，在保持 100% 形式化可靠性的同时，解决工业 BMC 深度循环求解卡死问题。
```
