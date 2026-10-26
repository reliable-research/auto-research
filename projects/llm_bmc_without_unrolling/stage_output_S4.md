# S4 - 方法、理论与实现规格交付成果（第 1 轮）

**项目主题**: LLM-Generated Inductive Invariants for Sound Bounded Model Checking Without Loop Unrolling: Replacing CFG loops with Vampire-verified invariant nodes and SMT safety checking  
**主要贡献类型**: 方法 (Method)  
**当前审查轮次**: 第 1 轮  
**当前工作阶段**: S4 - 方法、理论与实现规格 (Method, Theory & Implementation Specifications)

---

## 审查与设计基准说明 (Methodological Baseline & Design Rationale)

在 S3 形式命题与假设体系的基础上，本阶段完成技术对象的严谨形式化规格界定。本方法体系命名为 **$\text{LLM-VNode-BMC}$**（基于大语言模型候选引导、一阶定理证明器完备性校验与 CFG 抽象节点消解的健全有界模型检测框架）。

本设计遵循四大形式化约束：
1. **零信任外来输入 (Zero-Trust Heuristics)**：LLM 仅作为黑盒候选发生器，任何进入 CFG 重构流程的候选公式必须经由形式化双轨校验器（ATP/SMT）的完备数学证明；
2. **保健全性消解 (Soundness-Preserving Node Collapse)**：将复杂循环转换为非确定性 havoc 赋值与不变量约束的无环静态节点（Cut-Point Invariant Node），保证消解后的可达状态集为原程序可达状态集的严格过近似（Over-approximation）；
3. **分层分流与有界反馈 (Bounded Iteration with Tiered Refutation)**：采用 SMT 快速反例过滤与 Vampire 符号饱和推理分层执行，防止求解器无限发散；
4. **确定性降级机制 (Deterministic Fallback)**：若无法在时空预算内合成满足充分归纳性的不变量，严格回退至标准有界展开或区间拓扑抽象，杜绝误报安全（False Proof of Safety）。

---

## 一、技术/理论规格说明书 (Technical & Theoretical Specification)

### 1. 系统形式化输入与输出规约

#### 1.1 输入规约 (System Inputs)
系统接受一个四元组 $\mathcal{I} = \langle \mathcal{P}, \Sigma, \text{Pre}, \text{Post} \rangle$ 及超参数配置 $\Theta$：
*   **程序控制流图 $\mathcal{P} = (V_P, E_P, v_0, v_{\text{err}})$**：
    *   $V_P$：程序基本块（Basic Blocks）节点集。
    *   $E_P \subseteq V_P \times \mathcal{T} \times V_P$：带标签的有向控制转移边，其中转移关系 $\mathcal{T}(X, X')$ 为一阶无量词线性/非线性算术公式。
    *   $v_0 \in V_P$：初始入口节点；$v_{\text{err}} \in V_P$：错误捕获节点（断言违例陷阱）。
    *   $\mathcal{L} = \{L_1, L_2, \dots, L_m\}$：程序中检测到的自然循环（Natural Loops）集合，满足支配节点（Dominator）唯一性。每个循环 $L_i = (H_i, B_i, E_i)$ 由循环头（Header）$H_i$、循环体（Body nodes）$B_i$ 与回边（Back-edges）$E_i$ 唯一确定。
*   **变量集合 $\Sigma = X \cup X'$**：程序状态变量集 $X = \{x_1, \dots, x_n\}$ 及其状态后继变量集 $X'$。
*   **初始前置条件 $\text{Pre}(X)$**：$v_0$ 处的初始状态约束公式。
*   **安全后置断言 $\text{Post}(X)$**：程序各点标注的断言集合，特别是到达 $v_{\text{err}}$ 的前置条件 $\neg \text{Post}(X)$。
*   **超参数配置 $\Theta = \langle K_{\text{max\_retry}}, T_{\text{smt}}, T_{\text{vampire}}, B_{\text{fallback}} \rangle$**：
    *   $K_{\text{max\_retry}} \in \mathbb{N}^+$：LLM 纠错候选重试最大轮数（默认 $K=3$）。
    *   $T_{\text{smt}} \in \mathbb{R}^+$：SMT 求解超时阈值（默认 $5\text{s}$）。
    *   $T_{\text{vampire}} \in \mathbb{R}^+$：Vampire 证明超时阈值（默认 $30\text{s}$）。
    *   $B_{\text{fallback}} \in \mathbb{N}^+$：回退展开界限步数。

#### 1.2 输出规约 (System Outputs)
系统输出三元判定结果 $\mathcal{O} \in \{\text{SAFE}, \text{UNSAFE}(C_E), \text{UNKNOWN}(\mathcal{R})\}$：
1.  **$\text{SAFE}$**：严格数学证明。存在有效的归纳不变量集 $\mathcal{I}_{\text{inv}}$ 使得消解后的无环图 $\mathcal{P}^*$ 满足 $\mathcal{P}^* \models \text{Post}$，原系统在全局无界状态下绝无可能进入 $v_{\text{err}}$。
2.  **$\text{UNSAFE}(C_E)$**：确定性反例轨迹。$C_E = \langle s_0, e_1, s_1, \dots, v_{\text{err}} \rangle$ 为一条从初始状态可达的实际可执行路径反例（包含确定性输入赋值）。
3.  **$\text{UNKNOWN}(\mathcal{R})$**：在资源约束内无法完成充分证明，伴随结构化诊断原因 $\mathcal{R} \in \{\text{Timeout}, \text{ResourceExhausted}, \text{WeakInvariant}\}$。

---

### 2. 状态不变量与语义转换核心定义

#### 定义 1 (修改变量集 $\text{Mod}(L)$ 与非确定性赋值 $\text{Havoc}$)
对于循环 $L = (H, B, E)$，其写集合（Modified Variables）定义为在循环体所有转移关系中作为后继态出现的变量集合：
$$\text{Mod}(L) = \{ x \in X \mid \exists (u, \tau, v) \in B \times \mathcal{T} \times B,\ \tau(X, X') \implies x' \neq x \}$$
定义算子 $\text{Havoc}(\text{Mod}(L))$：取消 $\text{Mod}(L)$ 中所有变量的历史状态约束，将其重命名为全新无约束符号自由变量 $X_{\text{havoc}}$，切断其历史值依赖。

#### 定义 2 (归纳不变量三位一体判定条件 $\text{Inductive}(\text{Inv}, L)$)
候选公式 $\text{Inv}(X)$ 成为循环 $L$ 的合格归纳不变量，当且仅当以下一阶逻辑蕴含命题全称有效（Valid，即否定式为 UNSAT）：
1.  **初始化保真（Initiation / Base Step）**:
    $$\text{Valid}\left( \text{Reach}(H) \implies \text{Inv}(X) \right)$$
    其中 $\text{Reach}(H)$ 表示从程序入口 $v_0$ 沿无环前向路径到达循环头 $H$ 时的累积路径约束。
2.  **步进归纳保持（Consecution / Inductive Step）**:
    $$\text{Valid}\left( \text{Inv}(X) \land \mathcal{C}_{\text{loop}}(X) \land \mathcal{T}_L(X, X') \implies \text{Inv}(X') \right)$$
    其中 $\mathcal{C}_{\text{loop}}(X)$ 为循环进入/持续条件，$\mathcal{T}_L(X, X')$ 为循环体无环单步转移关系的析取式。
3.  **安全充分性（Safety / Sufficiency Step）**:
    $$\text{Valid}\left( \text{Inv}(X) \land \neg \mathcal{C}_{\text{loop}}(X) \land \mathcal{T}_{\text{post}}(X, X') \implies \text{Post}(X') \right)$$
    若仅满足前两项而不满足此项，则 $\text{Inv}$ 判定为“真不变量但过弱（Weak Invariant）”。

#### 定义 3 (不变节点消解操作符 $\text{Collapse}(L, \text{Inv})$)
给定满足上述定义的充分归纳不变量 $\text{Inv}(X)$，消解操作将子图 $(H, B, E)$ 替换为单一超节点 $v_{\text{node}}$，转换后拓扑重连规则为：
1.  **入边重连**：所有指向循环头 $H$ 的前向入边 $(u, \tau_{\text{in}}, H)$ 重连为 $(u, \tau_{\text{in}}, v_{\text{node}})$。
2.  **内部状态赋值与强化**：节点 $v_{\text{node}}$ 内部执行两步转换语义：
    $$\mathcal{T}_{v_{\text{node}}}(X, X') \triangleq \text{Havoc}(\text{Mod}(L)) \land \text{Inv}(X') \land \neg \mathcal{C}_{\text{loop}}(X')$$
3.  **出边重连**：所有从循环体流向外部的出口边 $(w, \tau_{\text{exit}}, v_{\text{out}})$ 重连为从 $v_{\text{node}}$ 出发，且转移前置直接接入已建立的外部状态。
4.  **死边抹除**：完全删除循环回边集 $E$ 及循环体内部节点集 $B$。

---

### 3. 系统架构与信息流 (System Architecture & Pipeline)

系统整体由四个核心模块构成解耦流水线：
```
  +------------------+       +---------------------+       +-----------------------+
  |  CFG Extractor   | ----> |  LLM Invariant      | ----> | Tiered Verifier       |
  |  & Loop Detector |       |  Generator (Engine) |       | (SMT Pre + Vampire)   |
  +------------------+       +---------------------+       +-----------------------+
          |                             ^                              |
          |                             |   Counterexample / Core      | (Validated Inv)
          |                             +------------------------------+
          |                                                            v
          | (Fallback on failure)                          +-----------------------+
          +----------------------------------------------> | Invariant Node        |
                                                           | Collapser & SMT-BMC   |
                                                           +-----------------------+
```

---

### 4. 核心算法流程伪代码

#### 算法 1：主控模型检测算法 ($\text{LLM-VNode-BMC}$)
```python
def LLM_VNode_BMC(P: Program, Pre: Formula, Post: Formula, Theta: Config) -> Result:
    """
    输入: 程序 P, 前置条件 Pre, 后置安全规约 Post, 参数 Theta
    输出: SAFE | UNSAFE(Counterexample) | UNKNOWN(Reason)
    """
    cfg = Build_Control_Flow_Graph(P)
    loops = Detect_Natural_Loops(cfg)
    
    # 拓扑最深优先遍历内层至外层循环
    for L in Post_Order_Traversal(loops):
        success, inv = Synthesize_And_Verify_Invariant(cfg, L, Post, Theta)
        if success:
            # 成功获得 Vampire 验证的归纳不变量，执行拓扑消解
            cfg = Collapse_Loop_To_Invariant_Node(cfg, L, inv)
        else:
            # 触发有界展开降级或局部回退
            if Theta.allow_fallback:
                cfg = Partial_Loop_Unroll(cfg, L, bound=Theta.B_fallback)
            else:
                return Result(UNKNOWN, reason=f"Invariant synthesis failed for loop {L.id}")
                
    # 此时 cfg 中所有成功识别的循环均消解为无环有向图 (DAG)
    # 对无环系统调用 SMT 求解器进行单次全局路径安全性证明
    smt_formula = Encode_CFG_To_SMT(cfg, Pre, Post)
    sat_status, model = SMT_Check_Satisfiability(Not(smt_formula), timeout=Theta.T_smt * 10)
    
    if sat_status == UNSAT:
        return Result(SAFE, proof_certificate="Sound Inductive Collapse")
    elif sat_status == SAT:
        trace = Reconstruct_Concrete_Trace(model, cfg)
        if Is_Feasible_Trace_On_Original_Program(trace, P):
            return Result(UNSAFE, counterexample=trace)
        else:
            # 抽象过近似引入的伪反例
            return Result(UNKNOWN, reason="Spurious counterexample due to abstraction gap")
    else:
        return Result(UNKNOWN, reason="Global SMT verification timeout")
```

#### 算法 2：分层式生成与归纳验证子例程 ($\text{Synthesize\_And\_Verify\_Invariant}$)
```python
def Synthesize_And_Verify_Invariant(cfg: CFG, L: Loop, Post: Formula, Theta: Config) -> Tuple[bool, Formula]:
    """
    分层归纳验证协议：结合 LLM 猜想、SMT 快速反例过滤与 Vampire 完备一阶归纳证明
    """
    context = Extract_Loop_Context(cfg, L, Post)
    feedback_history = []
    
    for attempt in range(1, Theta.K_max_retry + 1):
        # 1. 外部非受限启发源生成候选式 (LLM Generation)
        candidate_inv = Query_LLM_For_Invariant(context, feedback_history)
        
        # 语法与类型安全性静态检查
        if not Well_Formed(candidate_inv, cfg.variables):
            feedback_history.append({"type": "SyntaxError", "candidate": candidate_inv})
            continue
            
        # 2. Tier-1: 快速轻量级 SMT 否定反例过滤 (SMT Refutation Fast-Fail)
        smt_status, cex = SMT_Quick_Refute_Induction(cfg, L, candidate_inv, timeout=Theta.T_smt)
        if smt_status == COUNTEREXAMPLE_FOUND:
            # 捕获确定性反例（如 Base 反例或 Step 反例），转化为紧凑反馈
            feedback_history.append({
                "type": "InductionViolation",
                "candidate": candidate_inv,
                "violated_clause": cex.clause_type,  # Base or Step
                "counter_state": cex.state_assignment
            })
            continue  # 立即进入下一轮反馈重试，不浪费昂贵 ATP 算力
            
        elif smt_status == TIMEOUT:
            # SMT 无法在此界限内快速反驳，交由 Tier-2 处理
            pass

        # 3. Tier-2: Vampire 一阶归纳饱和定理证明 (Vampire Sound Inductive Check)
        tptp_problem = Encode_To_TPTP_FOF(cfg, L, candidate_inv, Post)
        vampire_status, proof_tree = Run_Vampire_ATP(
            tptp_problem, 
            timeout=Theta.T_vampire,
            options=["--mode=casc", "--induction=structural", "--symbol_elimination=on"]
        )
        
        if vampire_status == THEOREM_PROVED:
            # 证明成功，返回已确证的归纳不变量
            return True, candidate_inv
        else:
            feedback_history.append({
                "type": "VampireProofFailure",
                "candidate": candidate_inv,
                "reason": vampire_status # Unsaturated or Timeout
            })
            
    return False, None
```

#### 算法 3：CFG 循环节点消解与规约重写 ($\text{Collapse\_Loop\_To\_Invariant\_Node}$)
```python
def Collapse_Loop_To_Invariant_Node(cfg: CFG, L: Loop, inv: Formula) -> CFG:
    """
    依据 Definition 3 将循环子图物理重写为无环的不变量抽象节点
    """
    v_node = cfg.Create_Node(label=f"InvNode_{L.id}")
    
    # 提取修改变量并生成 Havoc 约束
    mod_vars = Compute_Modified_Vars(L)
    v_node.statements = [
        Havoc(mod_vars),
        Assume(inv),
        Assume(Not(L.condition))
    ]
    
    # 重构前驱入边
    for pred_edge in L.header.incoming_edges:
        if pred_edge.source not in L.body:
            cfg.Add_Edge(pred_edge.source, v_node, condition=pred_edge.condition)
            
    # 重构后继出边
    for exit_edge in L.exit_edges:
        cfg.Add_Edge(v_node, exit_edge.target, condition=exit_edge.condition)
        
    # 彻底抹除原循环体及内部边
    cfg.Remove_Subtree(L.body)
    return cfg
```

---

## 二、组件—假设映射表与具体技术增量定位

### 1. 组件与 S3 核心假设映射表 (Component-Hypothesis Mapping)

| 系统组件 (System Component) | 形式化功能与行为 | 对应 S3 形式假设 | 预期验证指标与证伪判定依据 |
| :--- | :--- | :--- | :--- |
| **Tier-1: SMT 快速反例过滤器** (`SMT_Quick_Refute`) | 在将候选式提交至一阶证明器前，通过轻量级 SMT 否定求解在 $T_{\text{smt}}$ 内剔除非归纳候选并提取反例赋值。 | **H1 (效能与反例收敛假设)**: 引入反例反馈可使候选有效率在 $K \le 3$ 轮内达到 $\ge 60\%$。 | 若经过轻量反例指导后，多轮修复通过率未显著高于无反馈重试，则证伪 H1。 |
| **Tier-2: Vampire 归纳求解器** (`Run_Vampire_ATP`) | 负责对非线性算术或复杂控制依赖的归纳步进行一阶符号饱和推理，输出机器可校验证明树（TPTP Proof）。 | **H2 (一阶定理证明器适用边界假设)**: Vampire 在位向量与非线性算术归纳证明中成功率显著超越纯启发式，且时延在控制范围内。 | 若 Vampire 超时比例 $>50\%$，或在典型整型循环上证明能力低于 Z3 插值法，则证伪 H2。 |
| **不变节点消解引擎** (`Collapse_Loop_To_InvNode`) | 将被证明的归纳式与 $\text{Havoc}(\text{Mod}(L))$ 绑定，物理切除循环回边，将 CFG 降维为 DAG。 | **H3 (无展开消解健全性定理)**: 经由归纳充分节点消解的系统在 SMT 上断言成立 $\iff$ 原程序无界安全。 | 若消解后系统判定 SAFE 但原程序存在可达违例（Soundness 破坏），直接证伪 H3。 |
| **降级兜底回退器** (`Partial_Loop_Unroll`) | 当达到最大重试轮数仍未合成合格不变量时，自适应回退至有界展开或发出保守告警。 | **H4 (资源-边界单调性假设)**: 算法消耗算力与时延不会因重试陷入无底洞，总验证开销对经典 BMC 保持可控渐近优势。 | 在大界限长循环测试集下，若总耗时反超全量展开基线，则判定未达预期效益。 |

---

### 2. 具体技术增量定位 (Novel Technological Increments)

相对于最邻近的四类工业界与学术界基准方案，本研究所提出的核心构造与信息流增量如下表所示：

```
基线 A: 工业标准 BMC (CBMC / EBMC)
[程序 CFG] ---> [暴力展开 k 步 (Unrolling)] ---> [巨型 SMT 命题] ---> 局限: 只能证明 k 步安全，易 Timeout

基线 B: 经典抽象证明器 (IC3 / PDR / Houdini)
[程序 CFG] ---> [确定性内生插值/谓词发现] ---> [归纳证明] ---> 局限: 遇非线性算术/复杂指针时谓词空间爆炸

基线 C: 现有神经符号合成器 (CodeInv / LLM+SMT 简单包装)
[LLM] ---> 抛出猜想 ---> [SMT 检验] ---> 盲目重试 ---> 局限: 无 CFG 节点消解，无法反哺 BMC 拓扑

★ 本文方案 (LLM-VNode-BMC)
[程序 CFG] ---> [LLM 提取语义生成候选] 
                     |
                     v
             [分层双轨验证 (Tier-1 SMT Cex + Tier-2 Vampire ATP Proof)]
                     | (已证明归纳充分)
                     v
             [CFG 拓扑消解: 循环抹除 -> Havoc/Assume 静态超节点替换] 
                     |
                     v
             [对无环 DAG 执行单次 Sound SMT 安全检查] ---> 实现无展开的全局无界 Sound Safety 证明
```

#### 详细增量定位剖析：
1.  **构造增量 1：拓扑“消解即抽象”算子（Topological Loop Collapsing via Havoc-Invariant Node）**
    *   *区别于现有 LLM 不变量研究*：现有基于 LLM 的不变量工作（如 CodeInv, FSE'24）仅将不变量作为文档或独立 Assertion 进行评测，或者仅作为 SMT 求解的辅助引理（Lemmas），**从未在编译器/模型检测前端对 CFG 拓扑执行剪枝与节点替代**。
    *   *增量实质*：本方法直接将已验证的不变量作为静态规约节点注入 CFG，彻底抹除了循环回边与展开因子，将传统有界展开问题形式转化为单次无环路径可达性判定。
2.  **信息流增量 2：分层过滤与语义反例重构链（Tiered SMT-Refutation to Vampire-Saturation Pipeline）**
    *   *区别于单一 SMT 校验或单一 ATP 验证*：常规方法要么受限于 SMT 处理全称量词循环归纳时的启发式实例化不完备（E-matching 脆弱），要么受限于 Vampire 面对无价值候选时漫长且无成果的饱和搜索。
    *   *增量实质*：首创“Tier-1 SMT 快速寻找反例模型指导 LLM 修正（Fast-Refute） + Tier-2 Vampire 负责无反例候选式的深度归纳有效性确证（Deep-Prove）”的级联互补信息流。

---

## 三、T5 统一工作底稿 §4 (Unified Research Draft §4)

```markdown
## 4 方法、理论与实现规格（S4）

### 4.1 技术对象全称与核心架构
本研究所构造的技术对象为 **LLM-VNode-BMC** (LLM-Guided Invariant Synthesis and Topological Node Collapse for Sound Bounded Model Checking)。该框架由四个紧密协作的形式化子系统构成：
1. **控制流抽象与循环提取器 (CFG Analyzer)**：提取目标程序自然循环 $L = (H, B, E)$，确定修改变量集 $\text{Mod}(L)$ 并构建前向到达路径。
2. **上下文感知神经候选发生器 (LLM Candidate Generator)**：提取循环源码、前置上下文与安全断言，提示外部生成形式合规的候选一阶归纳不变量 $\text{Inv}_{\text{cand}}$。
3. **分层式归纳验证机 (Tiered Verifier)**：
   - *Tier-1 (SMT Refuter)*：以微秒级时延判定基步与单步反例，向发生器回传具体违反状态；
   - *Tier-2 (Vampire ATP)*：负责全称量词与符号归纳的理论完备饱和推理，生成机器可验证证明。
4. **CFG 不变节点消解与无环求解引擎 (Topological Collapser & SMT Checker)**：基于已证不变量实施回边剪除与 $\text{Havoc}(\text{Mod}(L))$ 节点代换，对消解后的无环 DAG 进行单次 SMT 命题判定，输出全局健全的无界验证报告。

### 4.2 核心形式化推导与稳健性保证 (Soundness Proof Sketch)
**定理 1 (消解变换的保健全性，Soundness Preservation)**：
设原程序为 $\mathcal{P}$，消解后的抽象程序为 $\mathcal{P}^*$。若 $\mathcal{P}^* \models \text{Post}$，则 $\mathcal{P} \models \text{Post}$。
*证明概要*：
1. 根据 Definition 2，不变量 $\text{Inv}$ 满足初始化步与保持步。由数学归纳法可知，原程序循环头 $H$ 在任意离散步数 $k \ge 0$ 下的所有可达具体状态集 $\mathcal{S}_k(H) \subseteq \text{Inv}$。
2. 节点消解算子 $\text{Collapse}(L, \text{Inv})$ 在切断循环后，将变量集 $\text{Mod}(L)$ 执行全量非确定性 Havoc 展开，并施加 $\text{Inv}(X') \land \neg \mathcal{C}_{\text{loop}}(X')$ 过滤。因此，超节点 $v_{\text{node}}$ 的出边状态集合 $\mathcal{S}(v_{\text{node}})$ 构成了原循环所有可能退出状态集合 $\mathcal{S}_{\text{exit}}(L)$ 的严格过近似：$\mathcal{S}_{\text{exit}}(L) \subseteq \mathcal{S}(v_{\text{node}})$。
3. 拓扑替换未改变除循环体外的任何外部前向控制依赖关系。因此，无环抽象图 $\mathcal{P}^*$ 的终态可达集包含原程序 $\mathcal{P}$ 的实际可达集。由经典过近似抽象解释原理（Cousot & Cousot, 1977），若在过近似集合上无反例能进入 $v_{\text{err}}$，则原系统绝无反例可达 $v_{\text{err}}$。证毕。

### 4.3 形式化接口与数据交换格式
*   **候选生成接口 (LLM Prompt Protocol)**:
    - 输入：JSON 载荷，包含精简 C 源码片段、已推断的变量类型签名表 $\Sigma$、前置不变假设与由 Tier-1 反馈的历史反例赋值元组。
    - 输出：标准一阶 SMT-LIB 2.6 格式的谓词表达式字符串，禁止自然语言混合。
*   **一阶定理证明接口 (TPTP Exchange Standard)**:
    - 验证器统一将 CFG 转移关系与候选式转译为标准一阶逻辑 FOF (First-Order Form) 格式，提交至 Vampire 4.8 进程。
*   **消解执行与 SMT 求解接口**:
    - 消解后的无环 CFG 直接编译为单静态赋值（SSA）形式，交由 Z3/cvc5 进行单次 Incremental Check-Sat。
```

---

## 阶段验收与后续衔接说明

1.  **交付物完整性自查**：
    *   [x] 技术/理论规格说明书：输入输出、形式定义、系统流图与完整算法伪代码均已无歧义定义。
    *   [x] 组件—假设映射表：将 Tier-1、Tier-2、消解引擎和降级机制严格对应至 S3 形式假设 H1–H4。
    *   [x] 具体技术增量定位：清晰界定出“拓扑消解节点算子”与“SMT 反例过滤+Vampire 归纳验证分层信息流”两项原创技术增量。
    *   [x] T5 统一工作底稿 §4 撰写完毕，包含核心 Soundness 定理证明概要。
2.  **下一阶段 (S5 - 实验设计与基准协议)**：
    下一步将基于 S4 规格，正式确立评估基准集（SV-COMP 经典无界/大界限循环子集）、对标基线工具配置（CBMC、ESBMC、IC3/PDR、CodeInv 原生版）以及消融实验控制组。
