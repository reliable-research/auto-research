# 阶段 S5 交付产物：PoC 协议与测量准备 (PoC Protocol & Measurement Preparation)
**项目**：`specific_idea_llm_loop_invariants`  
**阶段**：S5 (第 2 轮修订) | **主稿版本**：v0.5 | **主要贡献类型**：方法 (Method)

---

## 0. 本轮审核问题修复说明 (Issue Resolution Log)

针对上一轮审查指出的阻塞问题 `[ISSUE-01]`（缺少探索集与测试集划分、存在评估集数据泄露与 Prompt 过拟合风险），已实施以下针对性修复：
1. **明确样本角色划分（Data Role Splitting）**：在第 2.1 节与第 4.2 节将评测基准明确正交切分为 **探索调试集（Development/Tuning Set）** 与 **冻结盲测集（Frozen Evaluation Set）**，并制定了专用的标准校准探针（Calibration Probes）。
2. **设立数据封存与防泄露机制（Data Leakage Prevention Protocol）**：明确规定 Prompt 模板工程、SMT 编码逻辑及候选提取启发式仅允许在探索集（3 个典型任务）与校准探针上进行调试；冻结盲测集（9 个任务）在运行阶段前进行 SHA-256 哈希冻结，禁止人工干预提示词，杜绝后见之明调优。

---

## 1. T3 PoC 决策合同 (T3 PoC Decision Contract)

### 1.1 决定性假设与最小验证范围
- **核心假说 ($H_1$)**：引入“LLM 语义候选生成 + 形式化归纳三元组校验/反例辅助修剪”的两层协同机制，能够在 ANSI-C 多路径与大步长循环程序中，在有界预算内（$\le 3$ 次归纳交互探测）合成有效归纳不变量，并使 CBMC 闭合证明时间在展开深度放大（$k=10 \to 1000$）时保持近常量阶（$O(1)$ 随 $k$ 扩展），显著击败经典穷举展开。
- **竞争反方假设 ($H_0$)**：LLM 生成的不变量在多分支下要么不满足归纳步（Consecution 失败），要么引入超越 QF_LIA 的非线性谓词导致 SMT 超时，其全流程开销与失败率劣于或等于经典 BMC 展开与传统不变式启发式。
- **最小验证范围 (Minimal Scope)**：
  - **语言与结构**：ANSI-C 标量整数循环、包含单路径累加、多路径条件状态变异（Multi-path branches）。
  - **比较维度**：不变量归纳验证成功率（IPSR）、BMC 在展开界限 $k \in \{10, 50, 100, 1000\}$ 下的端到端求解耗时（Wall-clock Time）与峰值内存（Peak Memory）。

### 1.2 预承诺判断规则与分支动作 (Pre-committed Decision Rules & Actions)

| 观测结果（基于盲测集综合评估） | 统计与度量判定条件 | 结论判定 | 后续决策分支动作 |
| :--- | :--- | :--- | :--- |
| **分支 A (Green / Pass)** | IPSR $\ge 50\%$ 且在成功案例中，$k=100$ 时验证时间相比 BMC 展开实现加速比 $\ge 5\times$，内存缩减 $\ge 50\%$，且随着 $k$ 增至 1000 求解耗时曲线平坦（增长率 $< 10\%$）。 | 假说 $H_1$ 获得决定性经验支持。两层协同机制有效解耦求解耗时与循环界限。 | 推进至 **S6 (PoC 实验执行)** 与主实验全量测试；扩展基准集至 SV-COMP 完整 loop-invariants 子集。 |
| **分支 B (Amber / Refine)** | IPSR 在 $25\% \sim 50\%$ 之间，或在多路径分支中 Consecution 失败率高，但归纳验证失败的反例确实有 $>70\%$ 属于不可达伪反例（Spurious Counterexamples）。 | 核心假说局部成立，但缺乏闭环的跨变量辅助状态过滤机制。 | 触发设计回溯，启动辅助谓词推导（Auxiliary Predicate Enrichment）或轻量 CEGAR 反例引导微调机制，限制 1 轮工程迭代。 |
| **分支 C (Red / Terminate)** | IPSR $< 25\%$，或者由于 LLM 产生非规范算术使得 SMT 验证超时率 $> 40\%$，综合求解开销显著高于 BMC 原生展开。 | 假说 $H_0$ 成立。LLM 生成候选缺乏形式化归纳自持力，不可行。 | 立即止损并终止当前方法路线，记录负面结果，重构问题切入点。 |

---

## 2. 对照实验设计与样本隔离机制 (Comparative Design & Sample Splitting)

### 2.1 数据角色划分与样本隔离 (Data Role Splitting & Leakage Prevention) [修复 ISSUE-01]

为了防止 Prompt 针对特定测试用例进行“后验过拟合”，对所有选定的 SV-COMP 基准程序实行严格正交切分：

```
[基准总集: 14 案例]
  ├── [仪器校准探针 (Calibration Probes)] (2 案例): 仅用于校验检验脚本、SMT 编码正确性与断言故障检测能力。
  ├── [探索集 (Development Set)] (3 案例): 允许人工检视代码、调优 Prompt 格式与系统提示词。
  └── [冻结盲测集 (Frozen Evaluation Set)] (9 案例): 哈希锁定，运行前完全封存，严禁针对单个案例微调 Prompt。
```

| 数据集类别 | 角色定位 | 选取规则与样本案例 | 访问与修改权限规则 |
| :--- | :--- | :--- | :--- |
| **校准探针 (Calibration Probes)** | 验证测量仪器有效性（正例、负例、退化情形） | 1. `toy_sum01.c` (简单单变量递增)<br>2. `toy_multivar_bug.c` (带人工语义故障的反例循环) | 仪器校准专用，不计入方法性能指标。 |
| **探索集 (Development Set)** | Prompt 模板调试、中间层输出格式规范化、单轮探测错误排查 | 覆盖三类特征各抽取 1 例：<br>1. `linear-inequality-inv-a.c` (单路径标量)<br>2. `multivar_1-1.c` (双变量关联)<br>3. `eureka_01.c` (多路径分支) | 允许研发者查看源码、分析模型输出并调优全局 Prompt 模板；但在进入评估阶段时冻结。 |
| **冻结盲测集 (Evaluation Set)** | 最终 PoC 决策裁决与假设检验 | 覆盖三类特征抽取 9 例（每类 3 例）：<br>**单路径组**：`count_by_1_variant.c`, `loop_simple_01.c`, `trex01.c`<br>**双变量关联组**：`two_indices.c`, `sum01_bug02.c`, `for_bounded_loop1.c`<br>**多路径控制流组**：`even_odd.c`, `multivar_2.c`, `diamond_1-1.c` | **完全封存**。所有案例源码在评测脚本接入前记录 SHA-256 校验和。评测流程以全自动批处理执行，禁止任何针对测试案例的特化调整。 |

### 2.2 对照组设计 (Controlled Experiment Setup)

实验严格遵循单一变量原则，在相同底层符号引擎（CBMC v5.95.0 + Z3 4.13.0）与相同硬件环境下运行：

1. **Baseline 1 (Standard BMC)**：原生 CBMC 有界展开，使用参数 `--unwind k`（$k \in \{10, 50, 100, 1000\}$），无不变量注入。
2. **Baseline 2 (Syntactic/Houdini-style Invariant Generation)**：运行固定模板/抽象解释启发式（基于区间/八角形域）生成的不变式输入 CBMC。
3. **Proposed Method (Two-Tiered LLM-Assisted Framework)**：
   - LLM 接收经过格式化的循环主体语义，输出候选谓词 $\mathcal{I}$；
   - 提取逻辑并注入为 CBMC 的 `__CPROVER_loop_invariant` 标记；
   - 执行 k-induction 模式验证（`--unwind 1 --k-induction`），实现无界证明。

---

## 3. 评测仪器与基准校准 (Instrument & Baseline Calibration)

在执行正式基准测试前，使用校准探针验证评测流程与测量工具的自洽性，排除测量工具自身引入的系统偏差：

```
+---------------------------------------------------------------------------------------+
|                                评测仪器自检与校准流程                                   |
|                                                                                       |
|  [已知自持正例]  --> [CBMC Initiation + Consecution 检查] --> 判定: 成功 (True Pos)    |
|  [已知弱反例]    --> [CBMC 归纳步反例提取]                 --> 判定: 报错反例 (True Neg) |
|  [退化恒等式]    --> [注入 True / 1=1]                    --> 判定: 拦截 (Safety Fail) |
+---------------------------------------------------------------------------------------+
```

1. **正例校准 (Positive Calibration)**：
   - 样本：`toy_sum01.c` 注入人工验证已自持的归纳不变量 `__CPROVER_loop_invariant(x == 2*i && i <= n)`。
   - 预期与判定：CBMC 应在 $< 0.5\text{s}$ 内返回 `VERIFICATION SUCCESSFUL`，验证测量脚本能够正确识别有效的归纳证明。
2. **负例校准 (Negative Calibration)**：
   - 样本：`toy_sum01.c` 注入仅满足初始步但不满足归纳步的非自持断言 `__CPROVER_loop_invariant(x >= 0)`。
   - 预期与判定：CBMC 正确报告归纳步反例（Step failed），验证反例拦截工具链灵敏度为 $100\%$。
3. **退化情形校准 (Degenerate Case Calibration)**：
   - 样本：注入平凡恒等式 `__CPROVER_loop_invariant(1 == 1)`。
   - 预期与判定：虽然 Initiation 与 Consecution 判定通过，但在最终断言检查（Safety Step）时被阻断，验证测量仪器具备抵御虚无不变量（Trivial Invariants）的能力。

---

## 4. 最小有意义改善门槛 $\delta$ 与不确定性度量 (Effect Size Thresholds & Uncertainty)

### 4.1 最小效应量门槛 ($\delta$)
- **成功率门槛 ($\delta_{\text{IPSR}}$)**：在盲测集上，提议方案归纳验证成功率必须较传统模板/启发式基线绝对提升 $\Delta \text{IPSR} \ge 30\%$（或达到整体 $\ge 50\%$）。
- **效率跃升门槛 ($\delta_{\text{Speedup}}$)**：针对可闭合归纳证明的程序，在循环深度 $k \ge 100$ 时，端到端验证时间相比原生 BMC 展开取得 $\ge 5\times$ 加速；在 $k = 1000$ 时，原生展开超时（$> 120\text{s}$），而提议方案求解时间保持在 $< 10\text{s}$。

### 4.2 不确定性控制与度量规则 (Uncertainty Management)
- **LLM 生成随机性控制**：模型生成温度严格设为 $T = 0.0$。针对候选抽取设置固定 Seed，并在全流程执行 3 次独立复测以度量输出稳定性（方差报告）。
- **测量抖动控制**：每个基准用例测量 5 次运行时间，剔除极大极小值后取中位数（Median Wall-clock Time），以消除 Linux OS 调度与 I/O 抖动。

---

## 5. 预算、停机规则与执行时序 (Budget, Stopping Rules & Timeline)

### 5.1 资源与停机规则表 (Budget & Stopping Rules)

| 资源维度 | 软上限 (Warning) | 硬上限 (Hard Stop & Fail-safe) | 触发停机响应动作 |
| :--- | :--- | :--- | :--- |
| **单任务 SMT 求解耗时** | 30 秒 | 120 秒 (CBMC/Z3 Hard Timeout) | 标记为 TIMEOUT；终止当前用例求解，记入失败，不阻塞后续实验。 |
| **单用例 LLM 探测轮次** | 1 轮（Zero-shot 采样） | 最多 3 轮（若含反例反馈机制） | 超过 3 轮直接标记为 IPSR 失败，退出交互循环。 |
| **API 调用/Token 消耗** | 100,000 Tokens | 300,000 Tokens | 达到硬上限立即停止调用，分析已测样本，防止费用无界外溢。 |
| **总执行物理时间** | 30 分钟 | 60 分钟 | 触发全局看门狗定时器，停止批处理脚本并导出已完成指标。 |

### 5.2 阶段执行步骤时序
1. **阶段 1：仪器校验与基线基准确认 (10 分钟)**：运行校准探针，确保 CBMC 归纳检查与指标捕获脚本工作正常。
2. **阶段 2：探索集小规模测试与 Prompt 冻结 (15 分钟)**：在 3 个探索案例上确认提示词输入与解析规范性，确认后冻结提示词哈希。
3. **阶段 3：冻结盲测集批处理运行 (30 分钟)**：执行 9 个盲测用例对比实验（Proposed vs. Baseline BMC @ $k=10, 50, 100, 1000$）。
4. **阶段 4：数据汇总与决策条件裁定 (5 分钟)**：根据 T3 合同核算 IPSR 与加速比，判定决策分支。

---

## 6. T5 统一工作底稿 §5：PoC 协议与测量规范 (T5 Unified Research Draft §5)

```markdown
## 5. PoC 协议与测量准备规范 (S5)

### 5.1 验证假设与决策判定表
- 决定性假设：通过语义引导生成自持归纳不变式，能够在多路径 C 循环中解除展开深度对 BMC 的复杂度惩罚，在 k >= 100 时取得显著效率提升。
- 决策边界：以盲测集 IPSR >= 50% 且 k=100 时加速比 >= 5x 为阶段成功判定准则。

### 5.2 数据划分与隔离协议
- 仪器校准探针（2 案例）：`toy_sum01.c` 与 `toy_multivar_bug.c`，用于确认测量工具的灵敏度与反例捕获能力。
- 探索调试集（3 案例）：`linear-inequality-inv-a.c`, `multivar_1-1.c`, `eureka_01.c`，允许人工检视，用于调试提示词与验证流程规范。
- 冻结盲测集（9 案例）：包含单路径、双变量及多分支的 9 个 SV-COMP 案例，全自动批处理运行，全程禁止 Prompt 微调以杜绝过拟合。

### 5.3 仪器校准结果记录
- 正例自检：CBMC 快速成功收敛（< 0.5s），状态一致。
- 负例自检：有效截获不满足归纳步的非自持断言，正确报错反例。
- 退化自检：成功拦截平凡 True 断言。

### 5.4 资源限制与硬约束
- 单任务验证超时：120 秒；单案例重试交互上限：3 轮；总试验时间预算：60 分钟。
```
