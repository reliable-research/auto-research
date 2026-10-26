# AutoResearch Codeless (Idea → Paper 自动化研究引擎)

> 基于 **Idea_to_Paper_Codeless_Workflow_v4** 设计的可执行学术研究推进系统，原生集成 **Google Antigravity (`agy`)** 与 **Gemini** 大模型，自动映射与复用本地 OAuth 凭据，实现学术研究从问题发现（S1）到论文论证（S8）的闭环自主推进。

---

## 🌟 核心特性

1. **八阶段学术推进流水线（S1–S8）**：
   - **S1**：问题发现与价值判断 (Problem Discovery & Value Assessment)
   - **S2**：问题定义与研究定位 (Problem Definition & Research Positioning)
   - **S3**：假设与候选机制 (Hypotheses & Candidate Mechanisms)
   - **S4**：方法、理论与实现规格 (Method, Theory & Implementation Specifications)
   - **S5**：PoC 协议与测量准备 (PoC Protocol & Measurement Preparation)
   - **S6**：PoC 执行与证据判定 (PoC Execution & Evidence Adjudication)
   - **S7**：独立确认与证据扩展 (Independent Confirmation & Evidence Extension)
   - **S8**：论文论证与最终审查 (Paper Argumentation & Final Audit)

2. **48 张严谨操作审查卡（每阶段 C1–C6）**：
   - 每张卡均具备“为什么查、查哪里、怎么查、何为问题、期望产物、最小修复、验收方式、失败归属”。
   - 彻底拒绝用模糊语言代替证据核验。

3. **三角色制衡机制 (Multi-Agent Triad)**：
   - **Builder (研究执行者)**：遵循阶段指引生产最小交付物，更新唯一主线底稿（T5）。
   - **Critic (审核者)**：逐卡独立审计交付产物，标记 `MET` / `GAP` / `CONFLICT` / `N/A`，开具定位精准的阻塞 Issue。
   - **Controller (决策与预算控制者)**：依据 02 决策地图判定动作：`CONTINUE`（推进）、`REFINE_INLOOP`（阶段内微调）、`ROLLBACK`（精准回溯到根因阶段）或 `PAUSE`（预算耗尽保护）。

4. **原生 agy / Gemini 凭据映射**：
   - 自动发现并读取 `~/.gemini/antigravity-cli/antigravity-oauth-token`。
   - 自动识别 CLI 执行体 `/home/wangjian/.local/bin/agy`。
   - 免配置 `GEMINI_API_KEY`，开箱即用支持 `gemini-3.8-flash-high`、`gemini-3.8-flash-medium`、`gemini-3.1-pro-high` 等模型。

5. **六大规范学术交付模板 (T0–T5)**：
   - `00_T0_PROJECT_AND_STAGE_CARD.md`：项目启动与阶段承诺卡
   - `01_T1_REVIEW_AND_REFINE.md`：审查、Issue 跟踪与修复复核记录
   - `02_T2_HYPOTHESES_AND_EVIDENCE.md`：假设总账与证据台账
   - `03_T3_POC_DECISION_CONTRACT.md`：PoC 决策合同与预承诺检验协议
   - `04_T4_ROLLBACK_AND_HANDOFF.md`：回退交接单与依赖重查清单
   - `05_T5_UNIFIED_RESEARCH_DRAFT.md`：唯一统一研究主线底稿

---

## 🚀 快速上手

### 1. 安装与凭据检查

项目已支持标准 Python 3.10+ 安装，CLI 命令 `autoresearch` 与 `idea2paper` 互为别名：

```bash
# 检查本地 agy 环境与 Gemini 凭据连通性
autoresearch doctor
```

输出示例：
```
╭───────────────────────────────────────────╮
│ AutoResearch System Health Check (Doctor) │
│ Validating agy & Gemini mapping           │
╰───────────────────────────────────────────╯
ℹ Testing Gemini model response via agy...
                               System Diagnostics                               
┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Component         ┃ Status ┃ Details                                         ┃
┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ agy CLI Binary    │ FOUND  │ /home/wangjian/.local/bin/agy                   │
│ OAuth Credentials │ VALID  │ Token: ya29.a0A... (method: consumer)           │
│ Gemini LLM Test   │ PASSED │ Successfully reached gemini-3.8-flash-low       │
└───────────────────┴────────┴─────────────────────────────────────────────────┘
✔ All system checks passed! Ready to run AutoResearch workflows.
```

### 2. 初始化一个科研项目

```bash
autoresearch init my_research --topic "Self-correcting code generation via execution-grounded test synthesis" --archetype "方法 (Method)"
```
执行后将在 `projects/my_research` 中创建全部 T0–T5 模板和 `project_state.json`。

### 3. 单步推进 (Step-by-step)

运行当前阶段的一个完整循环（Builder 产出 -> Critic 审查 -> Controller 裁决）：

```bash
autoresearch step my_research --model gemini-3.8-flash-high
```

### 4. 自动流水线运行 (Full Pipeline)

从当前阶段连续推进，遇阻自动 Refine，严重前提失效自动 Rollback，直至指定阶段：

```bash
autoresearch run my_research --stage S1 --until S8 --model gemini-3.8-flash-high
```

### 5. 查看项目状态与审查卡矩阵

```bash
autoresearch status my_research
```

### 6. 手动回退 (Manual Rollback)

当发现根本性前提失效时，触发精准回退：

```bash
autoresearch rollback my_research S2 --reason "核心研究单位与边界需要重新界定"
```

---

## 📂 项目结构

```
auoreseaerch_codeless/
├── autoresearch/                         # 核心 Python 实现包
│   ├── config.py                         # 路径、默认模型与预算配置
│   ├── llm/
│   │   ├── base.py                       # 抽象 LLM 接口与响应数据结构
│   │   ├── credentials.py                # agy 本地 OAuth Token 解析与环境映射器
│   │   ├── agy_client.py                 # 基于 agy 子进程的 Gemini 稳定客户端
│   │   └── factory.py                    # 客户端构建工厂
│   ├── workflow/
│   │   ├── stages.py                     # S1–S8 阶段目标、交付要求与进出准则
│   │   ├── cards.py                      # 48 张审查卡元数据与判定标准
│   │   ├── decision_engine.py            # 02 决策地图引擎（CONTINUE/REFINE/ROLLBACK）
│   │   ├── state.py                      # ProjectState 状态机与持久化
│   │   └── templates.py                  # T0–T5 Markdown 生成器与更新器
│   ├── agents/
│   │   ├── builder.py                    # BuilderAgent (研究执行者)
│   │   ├── critic.py                     # CriticAgent (审核者)
│   │   ├── controller.py                 # ControllerAgent (决策控制者)
│   │   └── coordinator.py                # WorkflowOrchestrator 整体流转协调器
│   ├── cli/
│   │   └── main.py                       # 终端交互式命令行
│   └── utils/
│       ├── json_utils.py                 # 健壮的 LLM JSON 提取与修复工具
│       └── logger.py                     # Rich 彩色终端输出
├── Idea_to_Paper_Codeless_Workflow_v4/   # 原始 v4 规范文档、离线图表与手册
├── tests/                                # 单元与集成测试套件 (14+ 项自动化测试)
├── pyproject.toml                        # 构建与依赖配置
└── setup.py                              # 标准打包入口
```

---

## 💡 Python API 编程式调用

除命令行外，您可以在任意 Python 脚本中进行二次开发与编程式调度：

```python
from autoresearch import WorkflowOrchestrator, Config, StageId

# 1. 自定义配置与模型选择
config = Config(
    model="gemini-3.8-flash-high",
    max_refine_rounds=2,
)

# 2. 实例化流水线调度器
orchestrator = WorkflowOrchestrator(
    project_name="automated_reasoning",
    topic="Self-supervised consistency checking for theorem proving",
    config=config,
)

# 3. 执行单阶段或全流程
decision = orchestrator.execute_current_stage_step()
print(f"Action: {decision.action}, Target: {decision.target_stage}")

# 4. 连续推进至 S8
orchestrator.run_pipeline(start_stage=StageId.S1, stop_stage=StageId.S8)
```

---

## 🛡️ 决策与回退原则

本系统严格落实 `02_DECISION_AND_ROLLBACK_MAP.md` 的单一归属原则：

| 失效对象 | 归属与回退目标 | 到该阶段修什么 |
| :--- | :--- | :--- |
| **现象入口或重要后果** | **S1** | 来源核查、现象比较、价值后果与下一项探测 |
| **研究单位、目标、信息、范围或主要贡献** | **S2** | 问题合同、边界实例与最强近邻定位 |
| **承重假设、解释或区分预测** | **S3** | 假设依赖、最强反方与区分性预测 |
| **技术对象、构造、方法身份或核心推导** | **S4** | 算法规格、组件映射、接口与具体技术增量 |
| **测量、对照、样本/独立单位或判定协议** | **S5** | 验证设计、对照组、仪器校准与意义门槛 |
| **实际执行、汇总或已有证据判定** | **S6** | 运行记录、全量汇总与假设经验状态 |
| **独立确认、扩展、边界或论文证据范围** | **S7** | 独立测试集、公平强基线对比与证据闭环 |
| **文字、引用位置、论证组织** | **S8** | 表达、相关工作引用与最终局限性审计 |

当发生回退时，系统自动生成 `04_T4_ROLLBACK_AND_HANDOFF.md`，将依赖该前提的所有下游产物打上 `NEEDS_RECHECK` 标签，保障学术因果链条的绝对闭环。
