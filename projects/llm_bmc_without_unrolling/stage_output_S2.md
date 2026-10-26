# S2 - 问题定义与研究定位 (Problem Definition & Research Positioning) 阶段交付成果（第 2 轮修订版）

**项目主题**: LLM-Generated Inductive Invariants for Sound Bounded Model Checking Without Loop Unrolling: Replacing CFG loops with Vampire-verified invariant nodes and SMT safety checking  
**主要贡献类型**: 方法 (Method)  
**当前审查轮次**: 第 2 轮（针对 [ISSUE-01] 进行精准闭环修复）  

---

## 审查修改对照说明 (Changelog for Review Issues)

*   **针对 [ISSUE-01] (卡项 S2-C2: 衡量指标 M 的 Goodhart 效应与弱不变量退化防御)**:
    *   **修改前**: 指标系统仅关注消解率与求解加速比（$r_{\text{elim}}$, $r_{\text{solve}}$），易诱发代理指标退化：系统可能通过生成平凡弱不变量（如 $Inv = \text{true}$）强行通过归纳性检查并实施循环消解，但在后续安全断言判定中引入过度抽象（Over-approximation），产生大量虚假反例（Spurious Counterexamples / False Alarms），将原本安全的程序误判为 Buggy，从而虚假刷高消解率。
    *   **修改后**:
        1. **引入防御性指标**: 在 $M$ 字段中增设“虚假反例计数/率 ($V_{\text{spurious}}$ / $R_{\text{spurious}}$)”与“有效保真消解率 ($r_{\text{valid\_elim}}$)”。明确规定：**仅当循环消解后成功完成全局安全证明（Soundly Safe）或保留真实可达反例（Real Bug），且未引入由过度抽象诱导的伪反例时，消解才被判定为有效**。若产生不可验证的反例（经原始程序有界展开或混凝土执行复现证实为伪反例），直接记为过度抽象惩罚，不得计入成功消解。
        2. **补充失效条件与有效区间分析**: 显式阐述弱不变量导致代理指标失效的机制，制定“断言导向的不变量充分性校验（Assertion-Sufficiency Filtering）”与“伪反例重试/回退协议（CEGAR-style Fallback）”，阻断任何试图通过生成平凡/弱不变量虚假刷高消解性能的退化路径。

---

## 一、S2 问题合同卡 (Problem Contract Card)

| 字段 | 形式化定义与约束 | 详细说明与操作定义 |
| :--- | :--- | :--- |
| **研究单位 (Unit, U)** | $P = \langle CFG, L, \Phi_{\text{init}}, \Phi_{\text{safe}} \rangle$ | 包含非平凡循环结构 $L = \{l_1, \dots, l_m\}$ 的单过程或可内联过程 C 语言程序实例及其控制流图（CFG），具备明确的初始状态条件 $\Phi_{\text{init}}$ 和安全断言集合 $\Phi_{\text{safe}}$。 |
| **前置条件 (Condition, C)** | $C := C_{\text{CFG}} \wedge C_{\text{Loop}} \wedge C_{\text{Sound}}$ | (1) 循环 $l \in L$ 的循环边界符号化、未知或上界超大（$k > 10^4$），使标准有界展开在计算预算内无法完整覆盖；(2) 不依赖特定循环模板即可表达归纳性质；(3) 验证要求数学意义上的绝对稳健性（Sound Safety），不允许任何真实违反被漏报，且要求可判定的终止性。 |
| **允许信息 (Information, I)** | $I := \{ \text{AST}(P), \text{CFG}(P), \Phi_{\text{init}}, \Phi_{\text{safe}}, \text{Trace}_{\le k_{\text{small}}} \}$ | 允许使用程序静态源码、抽象语法树、CFG、初始/后置谓词规范，以及小界限探索（$k \le 3$）所得的前缀路径约束与有限状态抽样数据。**严格禁止**：预先注入的人工标注循环不变量或特定程序的定制启发参数。 |
| **计算资源 (Budget, B)** | $B := \langle T_{\text{total}}, T_{\text{inv\_check}}, Mem, \text{Call}_{\text{ext}} \rangle$ | 每个程序实例验证总时限 $T_{\text{total}} \le 300\text{s}$；单个循环不变量归纳充分性验证时限 $T_{\text{inv\_check}} \le 15\text{s}$；物理内存上限 $Mem \le 16\text{GB}$；外部启发式生成器（如 LLM/采样器）交互轮次上限 $\text{Call}_{\text{ext}} \le 5$。 |
| **可变对象 (Variable Object, X)** | $X = \langle \mathcal{G}_{\text{prompt}}, \mathcal{V}_{\text{sound}}, \mathcal{T}_{\text{replace}} \rangle$ | 求解器架构与管线配置：(1) 上游候选不变量抽取机制 $\mathcal{G}_{\text{prompt}}$；(2) 符号稳健判定与归纳充分性校验引擎 $\mathcal{V}_{\text{sound}}$（一阶饱和证明与 SMT 组合）；(3) CFG 循环结构至 Havoc-Assume-Assert 不变量抽象节点的拓扑重写规则 $\mathcal{T}_{\text{replace}}$ 与反例回退调度策略。 |
| **参照基线 (Baseline, R)** | $R := \{ R_{\text{BMC}}, R_{\text{InvGen}}, R_{\text{AutoLLM}} \}$ | $R_{\text{BMC}}$: 工业级标准展开 BMC（如 CBMC 5.95 默认展开模式）；<br>$R_{\text{InvGen}}$: 经典确定性不变量生成工具（如 LoopInvGen、基于 Houdini/IC3 的静态分析器）；<br>$R_{\text{AutoLLM}}$: 无归纳证明闭环的直接 LLM 预测生成与 SMT 过滤 baseline（直接提示+一轮 SMT 验证）。 |
| **核心目标 (Target, T)** | $T := \text{SoundlyProve}(P) \vee \text{WitnessBug}(P)$ | 在预算 $B$ 内，消除因循环展开导致的组合爆炸：在不引入虚假反例的前提下，将目标程序中的可消解循环稳健地替换为静态抽象节点，对 Safe 程序输出具备严格数学证据的全局安全证明（UNSAT），对 Buggy 程序报告确定性违反反例（SAT）。 |
| **衡量体系 (Metric, M)** *(针对 ISSUE-01 修订)* | $\mathcal{M} = \langle r_{\text{valid\_elim}}, r_{\text{solve}}, V_{\text{spurious}}, T_{\text{overhead}}, S_{\text{sound}} \rangle$ | **核心有效性指标**: <br>1. **有效保真消解率 ($r_{\text{valid\_elim}}$)**: 成功消解循环数占循环总数的比例，**附加约束**: 仅当消解后能得出明确结论（严格证明 Safe 或确认真实可达 Bug）且未诱发伪反例时，计入分子；<br>2. **验证求解成功率与加速比 ($r_{\text{solve}}, S_{\text{speedup}}$)**: 在基线超时（Timeout）的大界限/符号循环实例上的求解闭环率与时延加速；<br>**防御性与稳健性指标**: <br>3. **虚假反例/假报警数 ($V_{\text{spurious}}$)**: 因过度抽象（弱不变量）在后续断言处诱发的无法在真实程序中复现的假反例绝对数量（严格要求 $V_{\text{spurious}} = 0$）；<br>4. **稳健性维持标志 ($S_{\text{sound}} \in \{0, 1\}$)**: 严禁将存在 Bug 的程序误报为 Safe（漏报率必须绝对为 0）；<br>5. **验证辅助开销 ($T_{\text{overhead}}$)**: 归纳检验与节点重写耗时占总验证时间的比例。 |
| **纳入核心范围 (Scope-In, G)** | 见下文边界实例表（$G$ 集合） | 确定包含确定性/非确定性分支、标量整数/位向量算术、线性与分段非线性约束、单重及简单非嵌套/串联循环。 |
| **排除非目标范围 (Scope-Out, N)** | 见下文边界实例表（$N$ 集合） | 涉及并发死锁竞态（Concurrency）、递归函数调用未内联、复杂动态堆内存与指针别名重组、外部非语义黑盒系统调用。 |
| **核心未知 (Unknown, K)** | $K$ (已消除方案预占) | 在符号模型检测中，如何以低于循环展开组合复杂度的计算代价，判定由外部非受限启发源给出的候选不变量的归纳充分性，并建立将控制流图循环结构消解为健全等价静态抽象节点的语义规约与误差边界？ |

---

### 指标有效区间、失效条件与 Goodhart 防御机制分析

1. **Goodhart 效应退化陷阱**:
   若单纯以循环消解率（$r_{\text{elim}} = \frac{\text{消解循环数}}{\text{总循环数}}$）为优化目标，外部启发源极易生成平凡不变量（Trivial Invariant，例如 $Inv \equiv \text{true}$ 或与循环变量无关的弱约束）。此类弱不变量满足归纳基步和归纳步（$\text{true} \implies \text{true}$），能够轻松通过归纳检查。然而，将其转化为 Havoc-Assume 节点会抹除循环体对状态空间的有效约束，使循环后变量成为完全无约束的任意值（Havoc），直接导致后续合法的安全断言 $\Phi_{\text{safe}}$ 产生大量过度抽象假反例（Spurious Bug），彻底破坏验证实用价值。
2. **防御性设计与指标惩罚**:
   *   **定义有效保真消解率**:
       $$r_{\text{valid\_elim}} = \frac{\sum_{l \in L_{\text{elim}}} \mathbb{I}(\text{VerificationSucceeded}(P_{l}) \wedge \text{IsSpurious}(P_{l}) = 0)}{|L|}$$
       任何导致后续判定进入“产生伪反例”或“断言未知”状态的消解操作，即使技术上完成了节点替换，其计分亦直接归零，并触发系统回退（Fallback）。
   *   **断言充分性前置规约 (Assertion-Sufficiency Checking)**:
       在将候选不变量 $Inv$ 准入为替换节点前，不仅检验归纳性（$Inv$ 在初始条件和循环步下成立），还必须联合 SMT 执行局部充分性蕴含检验：$\text{Havoc}(P) \wedge Inv \wedge \neg \text{LoopCond} \implies \text{WeakestPrecondition}(\Phi_{\text{safe}})$。若不满足，即便 $Inv$ 是归纳的，亦标记为“过弱（Too Weak）”并不予替换，强制要求启发源基于未满足核进行强化，或回退至有界展开。

---

## 二、边界实例表 (In-Scope G vs. Out-of-Scope N)

| 类别 | 编号 | 程序模式与控制流特征 | 语言与语义特征 | 预期系统行为 (Behavior Contract) | 纳入/排除理由 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **纳入 (In-Scope, G)** | **G-01** | **大常数/未知上界单重循环**：如 `for(i=0; i<N; i++) { x += 2; } assert(x == 2*N);` | 线性整数算术 (LIA)，变量无别名，标量更新。 | 成功抽取线性归纳不变量 $x = 2i$，完成健全消解为抽象节点，一击证明安全（UNSAT），无需展开 $N$ 次。 | 核心目标场景：标准 BMC 展开爆炸的直接痛点。 |
| **纳入 (In-Scope, G)** | **G-02** | **非确定性分支条件循环**：循环体内含 `if (*) { a++; } else { b++; }`，断言 `assert(a + b == k);` | 路径敏感分支，位向量/整数，符号输入。 | 合成并归纳验证区间/关系不变量 $a+b = k$，替换后验证断言成立。 | 检验启发源与符号判定器对路径分支汇聚特征的归纳能力。 |
| **纳入 (In-Scope, G)** | **G-03** | **真实缺陷循环 (Real Buggy Loop)**：循环边界或内部计算存在 off-by-one 越界。 | 包含违反 $\Phi_{\text{safe}}$ 的可达状态。 | 系统在尝试不变量充分性检验时识别反例，或消解后保留可达反例并经原始有界路径确认，报告真实反例（SAT）。 | 验证系统对真实违反的辨识度，确保不会因虚假不变量将 Bug 覆盖。 |
| **纳入 (In-Scope, G)** | **G-04** | **多断言级联串联循环**：同一过程内前后存在两个数据依赖的顺序循环。 | 过程内数据流串联，无递归。 | 前序循环消解后输出抽象后置约束，作为后续循环的前置条件，全流程闭环证明。 | 验证抽象节点在 CFG 拓扑中的组合性（Compositionality）。 |
| **排除 (Out-of-Scope, N)** | **N-01** | **复杂动态堆与不透明指针别名**：如链表反转、红黑树动态平衡调整。 | 包含指针深层引用、动态分配（malloc/free）、堆形态逻辑（Separation Logic）。 | 显式拦截并回退到传统展开/指针分析模式，不尝试生成一阶归纳节点。 | 堆形态不变量需专用分离逻辑或高阶谓词，超出一阶饱和证明器与简单节点抽象能力范围。 |
| **排除 (Out-of-Scope, N)** | **N-02** | **非可内联多过程递归与高阶函数**：如相互递归（Mutual Recursion）程序。 | 调用栈无界，控制流图跨越多个动态过程边界。 | 拒绝作为循环单位处理，提示转入过程间摘要分析（Interprocedural Summarization）。 | 本研究形式化对象限定为过程内 CFG 循环消解。 |
| **排除 (Out-of-Scope, N)** | **N-03** | **并发多线程数据竞争与死锁**：含 `pthread_create` 及原子同步原语。 | 线程交错状态空间爆炸，弱内存模型（Weak Memory Model）。 | 明确排除，不纳入本阶段合同。 | 并发不变量（Owicki-Gries / rely-guarantee）需完全不同的并发语义与展开模型。 |
| **排除 (Out-of-Scope, N)** | **N-04** | **非语义外部黑盒调用**：循环体内包含无法符号化的闭源动态链接库调用或 I/O 操作。 | 未解释外部函数，不可符号求值。 | 识别未解释黑盒，若无法推导抽象效应则放弃消解。 | 缺乏形式语义基础，无法构建稳健归纳验证闭环。 |

---

## 三、近邻工作定位与实质差异表 (Related Work & Substantial Differences)

| 近邻方法与代表工作 | 同等前置条件下的已解决能力 | 留存的实质差异与本质瓶颈 | 本研究的核心边界与突破点 ($X \to \Delta$) |
| :--- | :--- | :--- | :--- |
| **1. 传统 BMC 循环展开**<br>(CBMC, EBMC; Clarke et al.) | 对已知小界限展开能快速生成路径约束，利用 SMT 极其高效地发现浅层 Bug。 | 必须展开循环体；对未知上界无法提供全局 Sound 保证；展开界限 $k$ 增大时公式呈组合爆炸，必定超时。 | **消除展开依赖**：将循环结构替换为归纳抽象节点，将“时序展开求解”转换为“单步静态安全性判定”，突破界限爆炸限制。 |
| **2. 经典逻辑/插值不变量生成**<br>(LoopInvGen, Daikon, IC3/PDR, Houdini) | 严格保证输出不变量的正确性与归纳性，在特定约束逻辑（如简单单调循环）下高度确定。 | 严重依赖预设谓词模板与强约束逻辑碎片；非线性算术与非平凡分支容易发散（Divergence）或超时；合成能力脆弱。 | **解耦生成与验证**：引入非受限启发源进行全局模式识别跳跃，同时依靠一阶饱和证明器实施严格数学把关，突破模板表达力瓶颈。 |
| **3. 神经/LLM 不变量合成**<br>(CodeInv, Yao et al., Pei et al.) | 语义模式理解极强，能够直接跨越模板输出结构复杂的候选不变量公式。 | **缺乏形式化闭环保证**：产物常伴随弱归纳、伪不变量甚至语法逻辑错误；直接用于验证会破坏 Soundness，引发假反例或漏报。 | **闭环稳健消解与防御体系**：建立一阶定理证明过滤 + 断言充分性校验 + CFG 健全节点重写，在指标体系与协议上彻底杜绝弱不变量引发的虚假消解与假反例。 |
| **4. CEGAR 循环抽象与摘要**<br>(CPAchecker, Blast, SLAM) | 利用谓词抽象构建状态空间图，依据反例逐步细化抽象谓词。 | 抽象细化迭代（Spurious Counterexample refinement）开销极其沉重，复杂关系谓词发现效率低下。 | **一击式节点等价抽象**：利用外部启发提供高质量初始归纳猜想，单次完成节点收敛，失败即快速判定并受控回退，避免陷入多轮发散细化。 |

---

## 四、主要贡献类型与审查适用卡判定

### 1. 选定主要贡献类型
*   **选定类型**: **方法 (Method)**
*   **定义与定位**: 提出一种在控制流图上将非平凡循环稳健重写为一阶归纳不变量抽象节点的模型检测方法，构建“外部启发生成 - 一阶饱和证明稳健过滤 - 断言充分性防御 - CFG 节点消解 - SMT 终极安全求解”的全闭环管线。

### 2. 后续阶段审查适用卡与替代义务映射

| 后续阶段 | 适用审查卡项 | 贡献类型对应的特定要求 / 替代义务 (Method-specific Duties) |
| :--- | :--- | :--- |
| **S3 (技术方案设计)** | **卡项 M-Design**<br>(机制严密性卡) | 1. 必须形式化定义 CFG 节点重写操作算子 $\mathcal{T}_{\text{replace}}$ 的前置充分条件与不变性定理；<br>2. 必须给出健全性保持（Soundness Preservation）的严密数学证明草图，形式化证明为何被替换后的抽象 CFG 安全蕴含原始程序安全；<br>3. 必须明确弱不变量拦截协议的具体推演规则。 |
| **S4 (实验设计与基准)** | **卡项 M-Benchmark**<br>(实验对照公信力卡) | 1. 基准库必须从 SV-COMP (Loop / ReachSafety) 标准测试集中选择，杜绝针对自身算法的人工特供微型用例；<br>2. 对照实验必须包含与工业标准展开（CBMC）及经典合成器（LoopInvGen）的严格成对比较；<br>3. 必须报告包含 $V_{\text{spurious}}$、消解有效率 $r_{\text{valid\_elim}}$ 在内的全套防御指标，证明无作弊刷分。 |
| **S5 (实验执行与验证)** | **卡项 M-Ablation**<br>(消融与稳健性卡) | 1. **核心消融实验**: 必须包含移除一阶证明器校验、移除断言充分性过滤后的性能对比，展示假反例率的真实变化；<br>2. 必须统计分析外部启发源在不同温度/采样配置下的鲁棒性边界。 |

---

## 五、T5 统一工作底稿 §2 更新

```markdown
## 2 问题定义与研究定位（S2）

### 2.1 形式化问题合同 (Problem Contract)
本研究的形式化单位定义为包含未知或大界限循环集合 $L = \{l_1, \dots, l_m\}$ 的单过程/可内联 C 语言控制流图实例 $P = \langle CFG, L, \Phi_{\text{init}}, \Phi_{\text{safe}} \rangle$。
系统输入限定为程序结构信息与小步有界抽样前缀 $I := \{ \text{AST}(P), \text{CFG}(P), \Phi_{\text{init}}, \Phi_{\text{safe}}, \text{Trace}_{\le k_{\text{small}}} \}$，在严格时延与计算预算 $B$（单程序 $T \le 300\text{s}$，内存 $\le 16\text{GB}$）下运行。
核心优化对象为系统架构与消解算子 $X = \langle \mathcal{G}_{\text{prompt}}, \mathcal{V}_{\text{sound}}, \mathcal{T}_{\text{replace}} \rangle$。
目标 $T$ 为在不展开循环的前提下，对 $P$ 达成数学稳健的全局安全判定（Soundly Prove Safe via UNSAT）或报告不可推翻的真实反例（Witness Real Bug via SAT）。

### 2.2 防御性度量体系与 Goodhart 免疫机制
针对代理指标退化（如通过生成平凡弱不变量虚假刷高消解率，但导致后续断言过度抽象报出伪反例）的风险，本研究确立多维稳健衡量体系 $\mathcal{M} = \langle r_{\text{valid\_elim}}, r_{\text{solve}}, V_{\text{spurious}}, T_{\text{overhead}}, S_{\text{sound}} \rangle$：
- **有效保真消解率 ($r_{\text{valid\_elim}}$)**: 显式绑定后验判定结论与保真度。定义为成功消解且最终判定为 Safe（且经证明成立）或真实 Bug（经混凝土执行复现证实）的循环比例；
- **过度抽象防御与零假反例惩罚 ($V_{\text{spurious}} = 0$)**: 严禁将因不变量过弱而无法判定断言（引发假警报）的情形计入有效消解。系统内嵌断言充分性过滤：$\text{Havoc}(P) \wedge Inv \wedge \neg \text{LoopCond} \implies \text{WP}(\Phi_{\text{safe}})$，拦截平凡弱不变量；
- **稳健性绝对红线 ($S_{\text{sound}} = 1$)**: 漏报率必须恒为 0，严禁通过非稳健不变量抹除真实存在的 Bug。

### 2.3 边界实例与正交排除范围
- **纳入范围 (In-Scope, G)**: 标量算术（LIA/BV）、单重与非嵌套多分支循环、含非确定性赋值与路径汇聚的循环、存在边界越界/断言违反的真实缺陷循环。
- **排除范围 (Out-of-Scope, N)**: 动态堆指针别名深度重组（需分离逻辑支持）、非可内联相互递归、并发线程交错与同步数据竞争、不可解释的黑盒系统调用。

### 2.4 近邻实质差异定位
相较于传统展开式 BMC（CBMC），本方法消除了对循环界限的组合展开依赖，将有界验证提升为全局无界证明；相较于传统合成器（LoopInvGen/IC3），借助外部模式识别解耦搜索空间，规避逻辑模板发散；相较于黑盒神经预测（CodeInv），构建了包含一阶证明稳健把关、断言充分性防御与拓扑重写的确定性闭环，确保形式化可验证性。
```
