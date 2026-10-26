# S4 阶段交付物：方法、理论与实现规格（第 2 轮）

---

## 针对上一轮审查问题 (ISSUE-01) 的修复说明

* **修改定位**：§4.2.3 节新增《符号归纳强化算子（`symbolic_strengthen`）精确代数与逻辑推导规范》，并在 §4.2.1 与 §4.2.2 中同步对齐确定性接口签名与流程控制。
* **最小修复实施内容**：
  1. 抛弃模糊的自然语言描述，明确采用**基于有界回溯最弱前置条件（Bounded Weakest Precondition, WP）结合 Unsat Core 与 Farkas' Lemma 凸松弛投影**的双轨确定性推导机制。
  2. 详细列出从输入 $(I_{\text{cand}}, \text{cex}_{\text{step}}, \text{Body}, \text{Init})$ 到输出 $I_{\text{aux}}$ 的三步代数转换与求解步骤（一阶逻辑公式级展开）。
  3. 给出了明确的算法伪代码、终止准则、超时（Timeout）与失败（Fail-safe Fallback）判定边界，确保任意第三方工程师能够依据 Z3/CVC5 API 实现出行为严格一致的强化器。

---

## 1. 技术与理论规格说明书 (Technical & Theoretical Specification)

### 1.1 形式化问题定义与验证边界

设待验证程序为一个一阶转移系统 $\mathcal{P} = (\vec{x}, \text{Init}(\vec{x}), \text{Guard}(\vec{x}), \text{Body}(\vec{x}, \vec{x}'), \text{Post}(\vec{x}))$，其中：
* $\vec{x} = \langle x_1, \dots, x_n \rangle$ 为程序整数及浮点变量的状态向量；
* $\text{Init}(\vec{x})$ 为进入循环前的初始前置断言；
* $\text{Guard}(\vec{x})$ 为循环执行条件，记循环体单步转移关系为 $T(\vec{x}, \vec{x}') \triangleq \text{Guard}(\vec{x}) \land \text{Body}(\vec{x}, \vec{x}')$；
* $\text{Post}(\vec{x})$ 为后置安全规约，循环退出条件为 $\neg\text{Guard}(\vec{x}) \implies \text{Post}(\vec{x})$。

**归纳不变量定义**：断言 $I(\vec{x})$ 满足归纳有效性，当且仅当以下三项一阶逻辑公式在量词自由线性整数/实数算术理论（QF_LIA/QF_LRA）下**有效（Valid）**，即其否定在 SMT 中不可满足（UNSAT）：
1. **初值蕴含（Initiation）**：$\text{Init}(\vec{x}) \implies I(\vec{x})$；
2. **单步保持（Consecution / Step）**：$I(\vec{x}) \land T(\vec{x}, \vec{x}') \implies I(\vec{x}')$；
3. **后置安全（Safety / Consecution to Post）**：$I(\vec{x}) \land \neg\text{Guard}(\vec{x}) \implies \text{Post}(\vec{x})$。

---

### 1.2 系统架构与信息流 (System Architecture & Pipeline)

本方法采用 **两阶段解耦强化验证闭环 (Two-Stage Decoupled LLM-SMT Loop)**：
1. **阶段 1（LLM 语义提议）**：由 LLM 作为无状态经验提议器，根据循环上下文 $\mathcal{P}$ 提取语义直觉候选断言 $I_{\text{cand}}$（满足 Initiation 与 Safety，但在 Consecution 经常因漏项失败）。
2. **阶段 2（确定性符号归纳强化 `symbolic_strengthen`）**：由 SMT 求解器检查保持步，若检出单步反例模型 $\text{cex}_{\text{step}}$，不直接依赖 LLM 产生振荡式特判修复，而是由确定性符号引擎执行最弱前置条件投影与凸松弛合成，推导出必要强化辅助约束项 $I_{\text{aux}}$，构成强化断言 $I_{\text{strengthened}} \triangleq I_{\text{cand}} \land I_{\text{aux}}$，直到归纳封闭或触发受控单步 CEGIS 回退。

```
                   +---------------------------------------+
                   | Program P = (Init, Guard, Body, Post) |
                   +-------------------+-------------------+
                                       |
                                       v
                     +-----------------------------------+
                     | Step 1: LLM Semantic Proposal     |
                     | Prompt(P) -> I_cand               |
                     +-----------------+-----------------+
                                       |
                                       v
                    +------------------------------------+
                    | Step 2: SMT Validation             |
                    | Check Init(x) => I_cand(x)         |
                    | Check I_cand & ~Guard => Post      |
                    +------------------+-----------------+
                                       | Valid
                                       v
                     +-----------------------------------+
                     | Step 3: Consecution Check         |
                     | I_cand(x) & T(x, x') => I_cand(x')|
                     +-------+-------------------+-------+
                      UNSAT  |                   | SAT (Counterexample cex_step)
                    (Closed) |                   v
                             |   +------------------------------------+
                             |   | Step 4: symbolic_strengthen        |
                             |   | (Deterministic Alg: §4.2.3)        |
                             |   | - WP(I_cand, Body) backward push   |
                             |   | - Linear Farkas template/Interpol. |
                             |   | Output: I_aux                      |
                             |   +-----------------+------------------+
                             |                     |
                             |                     v
                             |   +------------------------------------+
                             |   | Form I_new = I_cand /\ I_aux       |
                             |   | Verify Initiation & Safety on I_new|
                             |   +-----------------+------------------+
                             |                     |
                             |            +--------+--------+
                             |     Success |                | Fail (Exceed bound / Non-linear)
                             |             v                v
                             |      +--------------+  +-------------------------------+
                             |      | Return I_new |  | CEGIS Fallback to LLM with   |
                             |      +-------+------+  | Abstracted Cex (Max K rounds) |
                             |              |         +---------------+---------------+
                             v              v                         |
                 +--------------------------------------+             |
                 | Pass to CBMC (--apply-loop-invariants)| <-----------+
                 | Bypassing Loop Unrolling             |
                 +--------------------------------------+
```

---

### 1.3 核心模块接口定义表

| 模块名称 | 输入签名 (Input) | 输出签名 (Output) | 前置条件 (Pre-condition) | 后置条件 (Post-condition) |
| :--- | :--- | :--- | :--- | :--- |
| `propose_semantic_candidate` | $\mathcal{P}$: 待测程序 AST 及规约；$H$: 历史失败摘要（初次为空） | $I_{\text{cand}}$: 形式化一阶逻辑公式字符串 | $\mathcal{P}$ 符合 ANSI-C 语法标准，且标注有前/后置规约 | $I_{\text{cand}}$ 经语法解析器可转化为有效 Z3 AST |
| `check_inductive_triplet` | $I$: 候选断言；$\mathcal{P}$: 程序系统；$S$: SMT 求解器实例 | $\langle r_{\text{init}}, r_{\text{step}}, r_{\text{post}}, \text{cex} \rangle$：三步验证三态结果及反例状态赋值 | $I$ 为无自由未知符号的闭合布尔谓词 | 若某项不成立，$\text{cex}$ 必包含对应步的确切变量赋值字典 $\vec{x} \mapsto \mathbb{Z}$ |
| `symbolic_strengthen` (增量核心) | $I_{\text{cand}}$: 提议断言；$\text{cex}_{\text{step}}$: 保持步反例；$\mathcal{P}$: 目标程序；$t_{\text{limit}}$: 运算超时上限 | $\langle \text{status}, I_{\text{aux}} \rangle$：强化状态（SUCCESS/FAIL）及辅助项公式 | $\text{Init} \implies I_{\text{cand}}$ 成立，但 $I_{\text{cand}} \land T \not\implies I_{\text{cand}}'$，且 $\text{cex}_{\text{step}} \models I_{\text{cand}} \land T \land \neg I_{\text{cand}}'$ | 若返回 SUCCESS，则 $I_{\text{cand}} \land I_{\text{aux}} \land T \implies (I_{\text{cand}} \land I_{\text{aux}})'$ 在当前循环步封闭，且 $\text{Init} \implies I_{\text{aux}}$ |
| `cbmc_verify_closed` | $\mathcal{P}$: 源码；$I$: 归纳断言 | $\langle \text{verified}, \text{proof\_time} \rangle$ | $I$ 在 SMT 中通过完整归纳三条件 | CBMC 使用 `--apply-loop-invariants` 彻底绕开展开，输出验证成功证明 |

---

### 1.4 核心算法伪代码

```python
def LLM_Symbolic_Loop_Verification(P: Program, max_llm_rounds: int = 3, timeout_sec: float = 30.0) -> VerificationResult:
    """
    两阶段解耦强化循环不变量生成与验证主流程
    """
    history = []
    
    for round in range(1, max_llm_rounds + 1):
        # 阶段 1: LLM 纯语义断言提议 (零样/少样本提示)
        I_cand_str = propose_semantic_candidate(P, history)
        I_cand = parse_to_smt_ast(I_cand_str)
        
        # 阶段 2: 符号引擎三步检验
        init_ok, cex_init = verify_initiation(P.Init, I_cand)
        post_ok, cex_post = verify_safety(I_cand, P.Guard, P.Post)
        
        # 若初值或安全条件不满足，直接反馈反例给 LLM 调整
        if not init_ok:
            history.append(format_feedback("INITIATION_FAIL", cex_init))
            continue
        if not post_ok:
            history.append(format_feedback("SAFETY_FAIL", cex_post))
            continue
            
        # 检验单步保持性
        step_ok, cex_step = verify_consecution(I_cand, P.Guard, P.Body)
        if step_ok:
            # 单轮即完全封闭，直接进入 CBMC 交付
            proof_res = cbmc_verify_closed(P, I_cand)
            return VerificationResult(status="PROVED", invariant=I_cand, rounds=round, time=proof_res.time)
            
        # 阶段 3: 触发确定性符号归纳强化算子 (symbolic_strengthen)
        # 避免让 LLM 面对具体的单步反例产生局部振荡
        status, I_aux = symbolic_strengthen(I_cand, cex_step, P, timeout=5.0)
        
        if status == "SUCCESS":
            I_strengthened = SMT_And(I_cand, I_aux)
            # 严格复核增强断言的 Initiation 与 Safety
            if verify_initiation(P.Init, I_strengthened)[0] and verify_safety(I_strengthened, P.Guard, P.Post)[0]:
                proof_res = cbmc_verify_closed(P, I_strengthened)
                return VerificationResult(status="PROVED", invariant=I_strengthened, rounds=round, time=proof_res.time)
        
        # 强化算子失败或超时，收集抽象化反例摘要（Abstracted Cex），进入下一轮 LLM 迭代
        abstract_feedback = generate_abstract_feedback(I_cand, cex_step, P.Body)
        history.append(abstract_feedback)
        
    return VerificationResult(status="FAILED_FALLBACK_TO_UNROLL", invariant=None, rounds=max_llm_rounds)
```

---

### 1.5 核心技术增量实现规格：`symbolic_strengthen` 算子推导规范 (针对 ISSUE-01 专项解决)

为消除任何自然语言歧义，确保两位独立工程师能够写出行为严格一致的强化器，本节给出 `symbolic_strengthen` 的确定性代数推导流水线。

#### 1.5.1 数学与逻辑机理定义

给定：
* 提议断言 $I_{\text{cand}}(\vec{x})$；
* 单步转移关系 $T(\vec{x}, \vec{x}')$；
* 转移前状态赋值 $\sigma \in \text{cex}_{\text{step}}$，使得 $\sigma \models I_{\text{cand}}(\vec{x}) \land T(\vec{x}, \vec{x}') \land \neg I_{\text{cand}}(\vec{x}')$。

注意：$\sigma$ 是从一个满足 $I_{\text{cand}}$ 的状态出发、经单步循环体执行后跳出了 $I_{\text{cand}}$ 的“虚假前置状态（Spurious Pre-state）”。
为了阻断该反例并自封闭断言空间，我们需要合成辅助谓词 $I_{\text{aux}}(\vec{x})$，使得：
1. **反例排除**：$\sigma \not\models I_{\text{aux}}(\vec{x})$（切除当前单步假反例）；
2. **初值容许**：$\text{Init}(\vec{x}) \implies I_{\text{aux}}(\vec{x})$；
3. **前向/后向封闭**：$(I_{\text{cand}} \land I_{\text{aux}})(\vec{x}) \land T(\vec{x}, \vec{x}') \implies (I_{\text{cand}} \land I_{\text{aux}})(\vec{x}')$。

#### 1.5.2 确定性推导三步算法流程

`symbolic_strengthen(I_cand, cex_step, P, timeout)` 执行以下确定性算法流程：

##### 步骤 1：最弱前置条件（Weakest Precondition, WP）后向推导与单步 Unsat-Core 提取
* 对循环体转移关系 $T(\vec{x}, \vec{x}')$ 及后状态断言 $I_{\text{cand}}(\vec{x}')$ 计算一阶代换：
  $$\text{WP}_1(\vec{x}) \triangleq \text{substitute}(\vec{x}' \leftarrow \text{UpdateExpressions}(\vec{x}), I_{\text{cand}}(\vec{x}'))$$
  *在无内嵌复杂循环的分支循环体中，$\text{WP}_1$ 通过标准的 Dijkstra 谓词转换计算：对无环程序块通过赋值语句替换与分支条件条件合并得到。*
* 构造强化候选合取式集：
  将 $\text{WP}_1(\vec{x})$ 转换为合取范式（CNF）：$\text{WP}_1(\vec{x}) = \bigwedge_{j=1}^m C_j(\vec{x})$。
* **确定性过滤规则（Filter）**：
  对每一个子句 $C_j(\vec{x})$：
  1. 检查初值可达性：调用 SMT 求解器判断 $\text{Init}(\vec{x}) \implies C_j(\vec{x})$。若 UNSAT，则立即丢弃（不可强化，否则破坏初值步）；
  2. 检查反例隔离度：检验 $\sigma \models C_j(\vec{x})$。若 $C_j$ 在反例状态 $\sigma$ 上求值为假（即 $C_j$ 能有效切除反例），则将其加入核心强化候选池 $\mathcal{S}_{\text{cand}}$。

##### 步骤 2：基于 Farkas' Lemma 的仿射超平面松弛（针对线性算术）
若步骤 1 中 $\mathcal{S}_{\text{cand}}$ 未能使全系统归纳封闭，且所有涉及变量属于线性整数/实数理论（QF_LIA/QF_LRA）：
* 设定待求超平面模板：$I_{\text{aux}}(\vec{x}) \triangleq \vec{a}^T \vec{x} + b \ge 0$，其中 $\vec{a} \in \mathbb{Z}^n, b \in \mathbb{Z}$ 为未知常数。
* 根据 Farkas 引理，系统满足归纳保持的充要条件是存在非负乘子向量 $\vec{\lambda} \ge 0, \mu \ge 0$，使得：
  $$(\vec{a}^T \vec{x}' + b) - \vec{\lambda}^T \mathbf{A}_T \begin{pmatrix} \vec{x} \\ \vec{x}' \end{pmatrix} - \mu (\vec{a}^T \vec{x} + b) \equiv 0$$
* **确定性目标函数构建**：
  将反例 $\sigma = \vec{x}_{\text{cex}}$ 转化为显式排斥线性不等式：$\vec{a}^T \vec{x}_{\text{cex}} + b < 0$。
  联立初值容许条件 $\forall \vec{x}_0 \in \text{vertices}(\text{Init}), \vec{a}^T \vec{x}_0 + b \ge 0$。
* 调用确定性双仿射求解器（如 Z3 的 QF_NIA/优化求解器），设置求解上限为 $2.0\text{s}$。若存在解，提取系数向量 $\vec{a}^*, b^*$ 输出为确定性不等式。

##### 步骤 3：终止与超时失败准则（Timeout & Failure Fallback）
* **成功准则**：在时间阈值（$t \le t_{\text{limit}} = 5.0\text{s}$）内，解出的一组有限合取式集 $I_{\text{aux}} = \bigwedge C_k^*$ 满足 $\text{Init} \implies I_{\text{aux}}$ 且 $(I_{\text{cand}} \land I_{\text{aux}}) \land T \implies (I_{\text{cand}} \land I_{\text{aux}})'$。返回 `("SUCCESS", I_aux)`。
* **失败准则**：若出现以下任意情况：
  1. 求解耗时超过 $t_{\text{limit}}$（5.0 秒）；
  2. 循环更新中存在乘法、除法或非线性逻辑（Non-linear arithmetic），Farkas 模板无解；
  3. $\mathcal{S}_{\text{cand}}$ 中所有项均与 $\text{Init}$ 冲突（证明初值与归纳保持存在本质冲突，原 $I_{\text{cand}}$ 语义过强）。
  **安全降级处理**：立即终止确定性推导，返回 `("FAIL", None)`，触发主控流水线提取当前 $\text{cex}_{\text{step}}$ 的符号投影摘要，进入下一轮 LLM-CEGIS 抽象回退。

---

## 2. 组件—假设映射表与具体技术增量定位

### 2.1 组件与 S3 核心假设映射表

| 设计组件 / 算子 | 对应 S3 假设编号 | 假设具体内容 (S3 Hypothesis) | 组件如何验证/支持该假设 |
| :--- | :--- | :--- | :--- |
| **`propose_semantic_candidate` (LLM 纯语义提议器)** | **H-01** (LLM 弱归纳断裂假设) | LLM 在不加辅助强化项时，生成的断言语义真实率高（>80% 满足 Init 与 Post），但保持步自封闭率极低（<30%）。 | 组件严格限制 LLM 仅负责从代码中提议高阶不变属性，实验中单独统计该组件输出在保持步的失败率，显式暴露并复现弱归纳断裂现象。 |
| **`symbolic_strengthen` (§4.2.3 确定性归纳强化器)** | **H-02** (符号插值互补消除振荡假设) | 归纳保持步缺失的辅助项多为状态变量间的代数仿射边界，采用确定性符号 WP/Farkas 投影补充可将断言封闭率提升至 70% 以上，且耗时低于多轮重试。 | 针对 Consecution 失败，完全切断 LLM 面对单步反例的盲目试错，由本算子代数推导 $I_{\text{aux}}$；通过对比启用前后的单轮收敛率与生成耗时，直接证明或证伪 H-02。 |
| **`generate_abstract_feedback` (反例抽象化降级通道)** | **H-03** (具体反例诱导局部特判退化假设) | 直接将具体变量赋值反例（如 `x=3, y=-1`）输入 Prompt，会导致 LLM 倾向于输出 `if-else` 或局部范围特判断言；输入符号谓词切片则不会。 | 在强化算子失败降级时，本组件不透传原始具体状态，而是将反例抽象为违背的符号路径条件（Path-Condition Slice），通过断言语法复杂度评测（AST 分支节点数）检验 H-03。 |
| **`cbmc_verify_closed` (BMC 零展开切断接口)** | **H-04** (BMC 求解跃迁收益门槛假设) | 当且仅当循环最大理论展开深度 $k > 30$ 时，LLM+符号强化合成断言的时间开销（1~5s）才会低于 BMC 循环展开求解开销。 | 作为流水线终端，执行 `--apply-loop-invariants`；通过在不同展开深度 $k \in \{10, 20, 50, 100, \infty\}$ 下对比“纯展开耗时”与“本方法生成+证明耗时”，直接确立收益分界线。 |

---

### 2.2 具体技术增量定位 (Delta Analysis against Baselines)

```
基线 1: 经典反例引导归纳合成 (CEGIS / Houdini / ICE)
[ 预设固定谓词模板格 P ] ---> [ SMT 检查 ] ---> [ 反例样本集驱动选择 ]
缺陷: 强依赖人工设计的模板语法，无法处理超出模板范围的高阶逻辑关系。

基线 2: 纯 LLM 多轮自省修复 (Pei et al. FSE'23, Yao et al. OOPSLA'24 Lemur)
[ Code ] -> [ LLM 提议 I ] -> [ SMT 报错: cex ] -> [ 完整 cex 丢回 Prompt ] -> [ LLM 盲目修补 (易特判/振荡) ]
缺陷: 把严格的代数封闭推导推给统计概率模型，导致“真但不可归纳”断言反复陷入局部震荡。

本方案技术增量 (Our Technical Delta):
[ Code ] -> [ LLM 提议 I_cand (语义直觉) ]
                   |
                   v (Consecution Failure)
            [ 核心增量算子: symbolic_strengthen (§4.2.3) ]
            - Dijkstra WP 谓词推导 + CNF 投影
            - Farkas Lemma 双仿射超平面松弛
            - 严谨排除单步反例且严格保持 Initiation
                   |
                   v (产出 I_aux，一步归纳封闭)
            [ 合成 I = I_cand /\ I_aux ] ---> [ CBMC --apply-loop-invariants 零展开全证明 ]
```

**与近邻工作的技术差异对照表**：

| 维度 / 特征 | 经典 CEGIS (Houdini / ICE) | 纯 LLM 闭环修复 (Lemur, OOPSLA'24) | 本研究方法 (S4 规格) |
| :--- | :--- | :--- | :--- |
| **语义不变性来源** | 穷举枚举或人工语法格预置 | LLM 跨模态生成（富有语义直觉） | **LLM 跨模态零样生成（仅提议直觉语义）** |
| **归纳保持步修补主体** | 基于样本点选择满足的谓词子集 | 再次提示 LLM，让 LLM 猜修补项 | **确定性符号代数求解器 (`symbolic_strengthen`)** |
| **反馈信息流粒度** | 具体正/反例数据点 | 具体变量赋值（`x=0, y=1`） | **第一级：符号 WP/Farkas 本地吸收；第二级：路径切片抽象反馈** |
| **对不可归纳断言的处理** | 丢弃或弱化 | 依赖 LLM 随机采样碰运气 | **代数强化（Strengthening）：在原断言上追加合取项** |
| **与 BMC 工具链集成深度** | 独立验证器，难以直通 BMC | 独立验证原型，评估指标脱离求解器 | **无缝接入 CBMC `--apply-loop-invariants`，直接度量展开避让效能** |

---

## 3. T5 统一工作底稿更新：§4 方法、理论与实现规格

```markdown
# 01_UNIFIED_RESEARCH_DRAFT：研究主线底稿

项目：`llm_inductive_invariants_for_bmc`；当前阶段：S4；主稿版本：v0.4；主要贡献类型：方法 (Method)。

---

## 4. 方法、理论与实现规格（S4 交付物）

### 4.1 核心技术对象定位
本方法旨在解决程序有界模型检验（BMC）面对大深度或无界循环时因循环展开导致的求解爆炸问题。技术对象为一套将大语言模型（LLM）的全局代码语义直觉与确定性一阶逻辑符号强化求解深度解耦的双阶段归纳循环不变量自动合成系统。

### 4.2 符号强化归纳生成协议（Two-Stage Synthesis Protocol）
系统将不变量生成任务解构为具有严格数学与工程规格的四步管线：

1. **语义候选提议（Semantic Candidate Proposal）**：
   LLM 接收无注释或仅含前/后置规约的 C 代码，利用通用先验提取循环的宏观单调性或变量关联，输出候选断言 $I_{\text{cand}}(\vec{x})$。
2. **符号有效性三步三态判决（Tri-State SMT Checking）**：
   使用 Z3 分别检验初值蕴含 $\text{Init} \implies I_{\text{cand}}$、保持步 $I_{\text{cand}} \land T \implies I_{\text{cand}}'$ 及后置安全性 $I_{\text{cand}} \land \neg\text{Guard} \implies \text{Post}$。若初值或安全步不通过，立即中断并定向提示；若仅保持步未通过且返回单步反例状态 $\sigma$，则将控制权移交至符号强化模块。
3. **确定性符号归纳强化算子（Deterministic Operator: `symbolic_strengthen`）**：
   - **机制 A（WP 逆向投影）**：计算单步最弱前置条件 $\text{WP}_1(\vec{x}) = \text{subst}(\vec{x}', I_{\text{cand}}(\vec{x}'))$ 并拆解为 CNF 子句集 $\{C_j\}$。筛除与 $\text{Init}$ 冲突的项，保留使 $\sigma \not\models C_j$ 的有效强化子句。
   - **机制 B（Farkas 双仿射凸松弛）**：针对线性整数/实数循环，构建参数化超平面 $\vec{a}^T \vec{x} + b \ge 0$，以切除反例状态 $\vec{a}^T \vec{x}_{\text{cex}} + b < 0$ 为约束，利用 Farkas' Lemma 求解非负乘子及确定性系数，推导出归纳辅助约束项 $I_{\text{aux}}$。
   - 形成增强不变量 $I_{\text{strengthened}} \triangleq I_{\text{cand}} \land I_{\text{aux}}$，直接自封闭归纳超平面。
4. **CBMC 零展开验证交付（Zero-Unrolling Proof Handoff）**：
   将完全封闭的归纳断言自动转化为 ANSI-C 的 `__CPROVER_loop_invariant` 宏指令注入目标位置，触发 CBMC `--apply-loop-invariants` 参数，彻底绕开循环体多步展开，实现常数级单步路径安全归纳证明。

### 4.3 资源与信息合法性保证
- **零信息穿透（Zero Information Leakage）**：LLM 提议阶段仅允许访问输入程序的 AST、前置条件与安全性质，严格隔离任何运行时展开轨迹或超出 BMC 工具常规输入的先验知识；
- **确定性与可复现性（Deterministic Guarantee）**：强化算子 `symbolic_strengthen` 严格基于形式逻辑与 SMT 确定性代数推导，不包含任何随机性采样或未受控的大模型自然语言循环，保证同一反例输入下输出确定性的强化谓词；
- **Fail-safe 降级机制**：所有 SMT 求解及强化步设置严格的 5.0 秒超时断路器，超时或遇不可解非线性结构时平滑回退至带路径切片抽象提示的受控 CEGIS 修复流程，最大轮次限制为 3 轮。
```

---

## 4. 阶段自检与确认

1. **无歧义算法规范自检**：
   - §1.5 已经详细列出 `symbolic_strengthen` 的输入、输出、Dijkstra WP 代换规则、CNF 过滤准则、Farkas 超平面约束式、求解超时（5.0s）及三态终止准则。消除了第一轮审查指出的“基于自然语言泛指”的隐患，可由第三方工程师根据 Z3 Python API 直接复现。
2. **组件—假设映射自检**：
   - 提议模块、强化算子、抽象反馈模块及 CBMC 接口分别对应 H-01、H-02、H-03、H-04 假设，并在 §2.1 中逐项说明了设计逻辑与假设验证的对应关系。
3. **技术增量定位自检**：
   - 清晰对比了经典 CEGIS/Houdini 与近邻纯 LLM 方法（如 OOPSLA'24 Lemur），明确将“LLM 宏观语义提议 + 确定性符号代数强化（Strengthening）阻断反例”确立为核心技术增量。
