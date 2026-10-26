# S2 阶段交付物：问题定义与研究定位 (Problem Definition & Research Positioning)

**项目主题**: Using Large Language Models to automatically generate loop invariants to avoid loop unrolling in Bounded Model Checking  
**主要贡献类型**: 方法 (Method)  
**当前审查轮次**: 第 3 轮  
**执行角色**: Builder (研究执行者)

---

## 1. S2 问题合同卡 (Problem Contract Card: U, C, I, B, X, R, T, M, G, N, K)

| 维度标号 | 维度名称 | 形式化定义与严格说明 | 经验证据/基底约束 (Grounding) |
| :--- | :--- | :--- | :--- |
| **U** | **研究单位 (Unit of Analysis)** | 单一过程内带有安全性断言后置规约的 C 语言循环结构 $P = \langle \text{Init}, \text{Loop}(G, B), \text{Post} \rangle$。其中 $\text{Init}$ 为循环前驱初始化语句，$G$ 为循环守卫条件，$B$ 为循环体转移关系，$\text{Post}$ 为需验证的安全性质断言。 | SV-COMP Loops 子集及 Code2Inv 基准程序规范，程序控制流无过程间递归，以一阶逻辑（FOL）及标量变量操作为主。 |
| **C** | **约束条件 (Condition)** | 循环上界未确定（Unbounded）或展开上界 $k \ge 10^3$（导致传统 BMC 展开无法在指定时限内完成完全证明）；程序所涉及的数据类型处于 SMT-LIB 常用理论支持范围内（主干为线性整型/实型算术 QF_LIA / QF_NRA）。 | 满足 CL-02 与 CL-04 确立的“展开代价大于断言合成开销”分界，且求解器底层一阶理论可判定。 |
| **I** | **允许信息 (Allowed Information)** | 允许输入：(1) 循环前驱代码、循环体源码与后置断言；(2) 由 SMT 求解器检查产生的符号验证结果（SAT/UNSAT）及其反例状态转移二元组 $(s, s')$；(3) 循环的静态变量依赖图与类型定义。严禁包含：人工手写的谓词模板集、预先注入的真值不变量或作弊式内联标注。 | 严格保持全自动化（Push-button）验证设置，LLM 仅接触自然源码语义及形式化工具暴露的标准验证反馈。 |
| **B** | **资源预算 (Resource Budget)** | 单个循环程序的总验证计算预算：SMT 求解超时上限 $T_{\text{SMT}} \le 60\text{s}$；LLM 交互上限 $N_{\text{iter}} \le 5$ 轮；总端到端耗时 $T_{\text{total}} \le 180\text{s}$；Token 消耗上限 $\le 1.6 \times 10^4$ tokens。 | 确保与常规 BMC 实用超时（如 CBMC 默认 3~5 分钟上限）相比具备工程净收益。 |
| **X** | **可变对象 (Variable Object)** | **弱归纳断言强化与闭环验证协议（Inductive Strengthening Protocol）**：包含 (1) 面向 LLM 的“真值语义提议 + 结构化归纳强化项推导”提示范式；(2) 结合 SMT 反例核的局部弱归纳补全算法；(3) 循环不变量向 BMC 工具注入替换展开的切断机制。 | 核心可调整的创新算法架构（Method Contribution 核心）。 |
| **R** | **基线参考 (Reference Baselines)** | (1) **R1（原生 BMC 展开）**：CBMC 原生有界展开（无不变量介入）；<br>(2) **R2（经典模板合成）**：Houdini / ICE 经典自动合成；<br>(3) **R3（直接问答基线）**：Vanilla LLM 零样本/单轮直接生成不变量；<br>(4) **R4（前沿基线）**：Lemur (OOPSLA 2024) 纯反例 CEGIS 交互机制。 | 覆盖无模型传统解法、经典形式化合成器、朴素 LLM 解法及目前已知最强相关 SOTA。 |
| **T** | **目标承诺 (Target)** | 在相同计算预算下，使合成的不变量满足归纳充分性（$\text{Init} \implies Inv \land Inv \land G \land B \implies Inv' \land Inv \land \neg G \implies \text{Post}$），使得验证工具无需循环展开即可完成安全性证明；将单轮/少轮归纳闭合成功率显著提升，规避展开超时。 | 突破 CL-01 的“真但不归纳”断裂，实现“无展开证明完成”。 |
| **M** | **衡量指标 (Metrics)** | (1) **全归纳证明成功率 (Inductive Success Rate, ISR)**：无需展开即完成安全证明的基准程序比例；<br>(2) **端到端证明耗时 (End-to-End Proof Time, EPT)**：从源码输入到 SMT 宣布 UNSAT 的整体耗时；<br>(3) **收敛轮次分布 (Convergence Iterations, CI)**：成功用例中消耗的 LLM 交互轮次；<br>(4) **展开替代收益比 (Unrolling Speedup Factor, USF)**：相比于可展开完成用例的 BMC 耗时加速比。 | 形式化判定无歧义，由求解器输出 UNSAT 判定绝对客观。 |
| **G** | **纳入核心范围 (In-Scope, General)** | 见下文边界实例表（核心为整数算术、固定结构多变量循环、含安全性质断言的 C 源码）。 | 算法设计与评测的第一承诺区间。 |
| **N** | **排除非目标范围 (Out-of-Scope, Neglected)** | 见下文边界实例表（排除动态堆分配、非平凡指针别名、并发交织、深度过程间递归等）。 | 避免问题合同无限膨胀导致不可行。 |
| **K** | **后验验证卡 (Verification Protocol)** | 验证结果必须由独立 SMT 求解器（Z3 4.12+）以及形式化工具（CBMC `--apply-loop-invariants`）双重校验 UNSAT；且必须通过健全性消解（Mutation Check）——故意注入 Bug 时不变量生成机制绝不能证明错误程序安全。 | 防范 LLM 幻觉产生假阳性（Soundness Bug）。 |

---

## 2. 边界实例表 (Scope Boundary Table)

| 类别 | 实例代码/结构简述 | 纳入/排除状态 | 理由与依据 |
| :--- | :--- | :--- | :--- |
| **G1 (核心标量多变量循环)** | `int x=0, y=0; while(x<N){ x++; y+=2; } assert(y==2*x);` | **纳入 (G)** | 典型的线性整数算术（LIA），依赖多变量同步归纳步，传统 BMC 大 $N$ 展开爆炸，LLM 易提议 $y=2x$ 且易归纳闭合。 |
| **G2 (带条件分支的循环)** | `while(i<n){ if(c) { a++; } else { b++; } i++; } assert(a+b==i);` | **纳入 (G)** | 涉及路径分支合并，单步转换关系包含析取逻辑，极度考验弱归纳强化项的构造能力。 |
| **G3 (嵌套循环内层切断)** | `for(int i=0; i<M; i++){ for(int j=0; j<N; j++){ ... } }` | **纳入 (G)** | 针对内层或外层循环分别建立独立切断规约，展开深度呈乘积级爆炸，必须依靠不变量切断。 |
| **N1 (复杂动态内存/堆指针)** | `struct Node *p = head; while(p){ p = p->next; }` | **排除 (N)** | 涉及分离逻辑（Separation Logic）或复杂堆不变量图理论，不在一阶 SMT-LIB 标量理论范畴内，属于专用形状分析（Shape Analysis）领域。 |
| **N2 (非终止或活性验证)** | 验证循环“最终一定会退出”（Liveness / Termination） | **排除 (N)** | 本课题合同严格限定于**安全性证明（Safety Verification）**，活性证明需要构造秩函数（Ranking Function），证明义务与归纳不变式不同。 |
| **N3 (并发多线程交织循环)** | `pthread_create(...)` 共享内存多线程竞态循环 | **排除 (N)** | 状态空间由线程调度交织主导，Owicki-Gries 断言体系极其复杂，超出单过程 BMC 循环切断问题域。 |
| **N4 (黑盒函数/汇编/内联系统调用)** | 循环体内调用外部未建模系统 API 或汇编指令 | **排除 (N)** | 缺少完整语义转移关系，SMT 求解器无法给出确定性符号转换公式（Transition Relation）。 |

---

## 3. 近邻工作定位与实质差异表 (Related Work & Substantial Delta)

| 维度对比 | 经典 Houdini / ICE 学习器 (CAV'01, CAV'14) | Vanilla LLM 直接合成 (Pei et al. FSE'23) | Lemur: SMT 反例驱动 CEGIS (Yao et al. OOPSLA'24) | **本项工作方法合同 (Our Method Contract)** |
| :--- | :--- | :--- | :--- | :--- |
| **语义假设依赖** | 强依赖人工/启发式预设的有限谓词模板格（Template Lattice）。 | 依赖模型预训练语言先验，无形式化后处理。 | 依赖模型理解原始 Concrete Counterexamples 并自主修正。 | **基于 LLM 语义先验 + 符号核驱动的自封闭弱归纳强化协议**。 |
| **主要失败模式** | 模板爆炸或超出预设谓词表达能力（OutOfMemory / Inexpressible）。 | 提出语义真实但不具备归纳保持性的断言（Consecution Failure）。 | 面对非线性或多变量反例时，模型诱发“打补丁式特判（Case-split）”，陷入振荡。 | 将“真值不变性提议”与“归纳强化项封闭”解耦，阻止反例将模型带偏为局部特判。 |
| **与 BMC 工具整合** | 独立运行的合成器，极少直接嵌入 BMC 前端管线。 | 离线生成断言，缺乏与 BMC 工具状态切断机制的闭环结合。 | 作为通用程序验证后端，未针对 BMC 循环展开替代代价做定量权衡。 | **专为 BMC 展开规避设计**：无缝注入 CBMC/SMT `--apply-loop-invariants` 机制。 |
| **核心实质差异 (Delta)** | 从“受限模板搜索”跃迁至“开箱即用（Unconstrained）的开放域代码语义先验”。 | 从“单轮直觉押题（盲目）”跃迁为“有形式化保证的自洽强化生成”。 | 从“被动接受具体反例打补丁”跃迁为“通过符号核与结构化强化机制主动约束归纳超平面”。 | **彻底解决 CL-01 的弱归纳断裂，在极低交互开销下实现无展开的完全归纳证明。** |

---

## 4. 选定主要贡献类型与后续审查承诺 (Contribution Type & Review Commitments)

* **选定主要贡献类型**: **方法 (Method)**
* **方法类贡献的后续审查义务 (Method Replacement Commitments)**:
  1. **无魔法假定 (No Magic Assumptions)**：方法描述中绝不假设 LLM 具备“天然能生成封闭归纳式”的能力，必须给出确定性的算法/交互步骤（Prompt 协议 + 形式化辅助过滤 + 归纳补全），使任何具有代码理解能力的通用 LLM 均可复现该过程。
  2. **基线公平对比 (Fair Baselines)**：严格在统一的算力与时间预算下对比（相同的基准用例集、相同的 Z3/CBMC 求解器版本、可控且透明的 LLM Token/轮次预算）。
  3. **健全性兜底 (Soundness Guarantee)**：生成的断言必须保证经过 SMT 归纳三段论（Init, Step, Post）的绝对检验；验证工具绝不盲目信任 LLM 答案。
  4. **失败归因义务 (Failure Attribution)**：在无法成功合成的边界用例中，清晰给出是由于 SMT 一阶理论不可判定（如高度非线性）、LLM 上下文截断、还是变量关系超出归纳表达范围。

---

## 5. T5 统一工作底稿 §2 更新（增量纳入）

```markdown
## 2 问题定义与研究定位（S2 交付物：第 3 轮完整版）

### 2.1 形式化问题合同 (Formal Problem Contract)
本研究形式化定义为在有限资源预算 $B$ 内，求解一个能够切断有界模型检验（BMC）循环展开的归纳循环不变量合成问题。
* **输入元组**: $\langle P, C, I \rangle$
  * $P = \langle \text{Init}, \text{Loop}(G, B), \text{Post} \rangle$ 为带安全断言规约的 C 循环代码片段；
  * $C$: 展开深度 $k \ge 10^3$ 或上界未确定，且变量理论属于一阶可判定理论（QF_LIA/QF_NRA）；
  * $I$: 允许程序静态 AST、源码上下文、类型信息及 SMT 返回的符号判定（SAT/UNSAT/Counterexamples）。
* **可变对象 $X$**:
  * 提出两阶段弱归纳强化方法（Two-stage Weak-Inductive Strengthening Protocol），由 LLM 提议全局不变性质候选项 $Inv_{\text{cand}}$，结合轻量符号反馈与强化规则生成自封闭归纳项 $Inv_{\text{ind}}$。
* **求解目标 $T$ 与验证 $K$**:
  * 产出有效不变量 $Inv$，使 SMT 求解器证明满足：
    1. $\text{Init} \implies Inv$ (Initiation)
    2. $Inv \land G \land B \implies Inv'$ (Consecution)
    3. $Inv \land \neg G \implies \text{Post}$ (Safety)
  * BMC 工具直接借此切断展开完成全证明（UNSAT），规避状态爆炸。
* **衡量基准 $\langle R, M \rangle$**:
  * 对比 CBMC 原生展开 (R1)、经典 Houdini/ICE (R2)、Vanilla LLM 提示 (R3)、Lemur CEGIS (R4)；
  * 以全归纳证明成功率 (ISR)、端到端耗时 (EPT)、交互轮次 (CI) 为统一指标。

### 2.2 边界约束与不变量范围 (Scope & Boundaries)
* **核心纳入 (G)**: 线性及简单非线性整数算术、复合标量控制变量依赖、带内部路径分支的单循环与规则嵌套循环。
* **明确排除 (N)**: 排除复杂堆内存指针形状分析（Shape Analysis）、多线程竞态条件并发循环、终止性/活性性质验证、黑盒外部系统调用。

### 2.3 与近邻工作的实质差异 (Substantial Delta)
本工作针对文献中揭示的“LLM 易生成 True 断言但极难直接生成自封闭 Inductive 断言”这一根本痛点（CL-01），拒绝走“盲目增加 CEGIS 反例轮次导致特判振荡”的老路，确立“LLM 提议全局语义 + 符号核引导结构归纳强化”的方法路线，形成轻量、高归纳闭合率的 BMC 展开切断方法。
```
