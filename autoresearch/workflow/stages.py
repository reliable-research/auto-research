"""Stage definitions and specifications for Idea-to-Paper Workflow (S1-S8)."""

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Dict


class StageId(str, Enum):
    S1 = "S1"
    S2 = "S2"
    S3 = "S3"
    S4 = "S4"
    S5 = "S5"
    S6 = "S6"
    S7 = "S7"
    S8 = "S8"


STAGE_ORDER = [
    StageId.S1,
    StageId.S2,
    StageId.S3,
    StageId.S4,
    StageId.S5,
    StageId.S6,
    StageId.S7,
    StageId.S8,
]


@dataclass
class StageDefinition:
    id: StageId
    name: str
    goal: str
    entry_criteria: str
    steps: List[str]
    minimum_deliverables: List[str]
    cards: List[str]
    not_required_now: str


STAGES: Dict[StageId, StageDefinition] = {
    StageId.S1: StageDefinition(
        id=StageId.S1,
        name="问题发现与价值判断 (Problem Discovery & Value Assessment)",
        goal="哪个未知值得投入下一项探测？",
        entry_criteria="研究方向与资源约束；原始文献、观察或可检查的理论构造。没有具体 idea 也可以进入。",
        steps=[
            "1. 先写想获得的能力或想解释的现象，不写拟采用的模块。",
            "2. 建线索表：预期、实际、条件、来源、解释、后果各一列；每条观察绑定来源位置。",
            "3. 沿五个入口找问题：预期落差、指标失真、未经验证的前提、成功/失败边界、新能力改变旧约束。",
            "4. 为每条线索写最强正常解释，做条件对齐；把仍存在的未知写成候选问题。",
            "5. 为候选写最便宜的区分性探测，比较价值、可检验性和成本，选择下一项行动。",
        ],
        minimum_deliverables=[
            "S1 问题机会卡：条件 C、预期 E、观察 O、未知 K、后果 D、反方 A、探测 T",
            "线索来源表与候选取舍记录（保留被排除候选的理由）",
            "T5 统一工作底稿 §1",
        ],
        cards=["S1-C1", "S1-C2", "S1-C3", "S1-C4", "S1-C5", "S1-C6"],
        not_required_now="完整方法、最终效果、全面创新性审计。此时只需可信线索及值得探测的未知。",
    ),
    StageId.S2: StageDefinition(
        id=StageId.S2,
        name="问题定义与研究定位 (Problem Definition & Research Positioning)",
        goal="怎样把直觉未知定义成可检验的问题合同？",
        entry_criteria="通过 S1 审核的有效问题机会卡与线索记录；或已有项目中已核实其现象来源、比较条件和重要后果的记录。",
        steps=[
            "1. 写形式化研究对象：研究单位 U、条件 C、允许信息 I、资源 B、可变对象 X、基线 R、目标 T 与衡量 M。",
            "2. 给边界实例：至少写出纳入的核心范围 G 和明确排除的非目标范围 N。",
            "3. 做近邻定位：列出最接近的已有工作，指明同条件下已解决什么、还剩什么实质差异。",
            "4. 选定主要贡献类型并确定后续审查的适用卡与替代义务。",
        ],
        minimum_deliverables=[
            "S2 问题合同卡 (U, C, I, B, X, R, T, M, G, N, K)",
            "边界实例表与近邻实质差异表",
            "T5 统一工作底稿 §2",
        ],
        cards=["S2-C1", "S2-C2", "S2-C3", "S2-C4", "S2-C5", "S2-C6"],
        not_required_now="已证明的新算法实现、大规模实验结果；此时关键在问题边界和承诺的严密性。",
    ),
    StageId.S3: StageDefinition(
        id=StageId.S3,
        name="假设与候选机制 (Hypotheses & Candidate Mechanisms)",
        goal="哪条核心假设链支撑研究，若它错了会发生什么？",
        entry_criteria="S2 问题合同、近邻定位和主要贡献类型已锁定且无阻塞 issue。",
        steps=[
            "1. 建立 T2 假设总账：分解承重假设、前提、机制与范围假设。",
            "2. 为每个核心假设写出最强竞争解释与反方理由。",
            "3. 明确区分性预测：什么可观察结果支持本假设，什么结果支持反方。",
            "4. 预定失败动作与优先次序：若某条假设被证伪，系统应如何分流。",
        ],
        minimum_deliverables=[
            "T2 假设与证据总账（核心假设已注册，反方及区分预测明确）",
            "失败分流与淘汰优先级表",
            "T5 统一工作底稿 §3",
        ],
        cards=["S3-C1", "S3-C2", "S3-C3", "S3-C4", "S3-C5", "S3-C6"],
        not_required_now="所有假设的实证确认；此时要求假设具备强可证伪性与承重逻辑链。",
    ),
    StageId.S4: StageDefinition(
        id=StageId.S4,
        name="方法、理论与实现规格 (Method, Theory & Implementation Specifications)",
        goal="拟检验的技术对象或形式命题是什么？",
        entry_criteria="S3 核心假设、承重机制与可检验预测已确立。",
        steps=[
            "1. 编写技术规格：明确输入输出、状态不变量、核心算法/推导步骤。",
            "2. 建立模块与假设的映射：说明每个设计组件分别在验证 S3 的哪条假设。",
            "3. 定位具体技术增量：相对于近邻基线，究竟哪一项构造或信息流是新引入的。",
            "4. 确保实现规格与信息/资源合法性相符，消除关键歧义。",
        ],
        minimum_deliverables=[
            "技术/理论规格说明书（无歧义接口与算法逻辑）",
            "组件—假设映射表与具体技术增量定位",
            "T5 统一工作底稿 §4",
        ],
        cards=["S4-C1", "S4-C2", "S4-C3", "S4-C4", "S4-C5", "S4-C6"],
        not_required_now="已调优的最优超参数、全套代码实现；此时重点在技术对象的严谨规格。",
    ),
    StageId.S5: StageDefinition(
        id=StageId.S5,
        name="PoC 协议与测量准备 (PoC Protocol & Measurement Preparation)",
        goal="如何用最低成本设计能区分假说的检验？",
        entry_criteria="S4 技术规格已冻结；目标机制与组件映射明确。",
        steps=[
            "1. 冻结 T3 PoC 决策合同：明确决定性假设、最小验证范围与预承诺判断规则。",
            "2. 设计对照组：主方案与基线之间只改变目标机制对应的关键因素。",
            "3. 仪器与基准校准：用已知正例、负例和退化情形验证评测仪器的可信度。",
            "4. 设定最小有意义改善门槛 δ 与不确定性度量规则。",
            "5. 规划实验执行顺序与计算/时间预算上限。",
        ],
        minimum_deliverables=[
            "T3 PoC 决策合同（含比较设计、仪器校准、意义门槛与分支动作）",
            "预算与停机规则表",
            "T5 统一工作底稿 §5",
        ],
        cards=["S5-C1", "S5-C2", "S5-C3", "S5-C4", "S5-C5", "S5-C6"],
        not_required_now="海量算力刷榜、完整消融实验；重点在测量工具的有效性与事前承诺。",
    ),
    StageId.S6: StageDefinition(
        id=StageId.S6,
        name="PoC 执行与证据判定 (PoC Execution & Evidence Adjudication)",
        goal="初始证据是否支持继续？还是否定、未决或无效？",
        entry_criteria="T3 PoC 协议已冻结且 S5 六张卡全部审核通过。",
        steps=[
            "1. 忠实执行预定协议，完整记录运行日志与关键产物（不选择性排除失败）。",
            "2. 提取测量数据，按事前定义的公式和分母计算汇总指标。",
            "3. 检查数值精度与不确定性区间是否达到 S5 协议要求。",
            "4. 判定假设状态（SUPPORTED / CONTRADICTED / INCONCLUSIVE / INVALID）并更新 T2。",
            "5. 深入分析负结果与异常点，识别是协议执行偏差还是根本机制问题。",
        ],
        minimum_deliverables=[
            "真实运行记录与可复现汇总表",
            "T2 假设台账更新（带证据 ID 索引与最新判定状态）",
            "负结果与异常案例分析记录",
            "T5 统一工作底稿 §6",
        ],
        cards=["S6-C1", "S6-C2", "S6-C3", "S6-C4", "S6-C5", "S6-C6"],
        not_required_now="所有可能领域的泛化结论；重点在 PoC 范围内证据是否扎实并忠实于协议。",
    ),
    StageId.S7: StageDefinition(
        id=StageId.S7,
        name="独立确认与证据扩展 (Independent Confirmation & Evidence Extension)",
        goal="结论是否在更强条件、更广范围和独立单位下稳健？",
        entry_criteria="S6 核心假设判定为 SUPPORTED_IN_SCOPE，且无阻塞性仪器或协议缺陷。",
        steps=[
            "1. 在独立测试集/未见场景上开展独立确认（杜绝探索集过拟合）。",
            "2. 引入强基线，在同等计算与资源预算下进行公平比较。",
            "3. 系统性探测方法失效边界与边缘案例，避免平均值掩盖致命缺陷。",
            "4. 建立从最终主张 (Claims) 到实验证据 (Evidence) 的完整闭环映射表。",
        ],
        minimum_deliverables=[
            "独立确认实验报告与公平基线对比表",
            "边界失败分析与成本-效益全景图",
            "Claim–Evidence 证据闭环表",
            "T5 统一工作底稿 §7",
        ],
        cards=["S7-C1", "S7-C2", "S7-C3", "S7-C4", "S7-C5", "S7-C6"],
        not_required_now="论文最终排版与文字润色；重点在拓展证据的厚度与反方抗辩力。",
    ),
    StageId.S8: StageDefinition(
        id=StageId.S8,
        name="论文论证与最终审查 (Paper Argumentation & Final Audit)",
        goal="论文论证是否严格对应证据？",
        entry_criteria="S7 Claim–Evidence 闭环已建立，主要主张均有对应支持证据。",
        steps=[
            "1. 撰写并整合完整的论文论证主线（引言、问题、方法、实验、讨论、局限）。",
            "2. 逐句校对核心主张，确保摘要、引言与结论的措辞不超出 S6/S7 支持范围。",
            "3. 交叉审计论文正文数字、图表、附录证明与原始运行记录的一致性。",
            "4. 完善相关工作引用与近邻对比，客观诚实地披露方法局限性与开放问题。",
        ],
        minimum_deliverables=[
            "完整统一研究手稿 (Consolidated T5 Research Draft / Paper)",
            "完整证据追溯索引与可复现清单",
            "局限性与未解决问题说明",
            "T5 统一工作底稿 §8–§10",
        ],
        cards=["S8-C1", "S8-C2", "S8-C3", "S8-C4", "S8-C5", "S8-C6"],
        not_required_now="新增大规模实验（文字或局限性问题在 S8 直接修改，证据缺陷回退 S7 或更早）。",
    ),
}


def get_stage(stage_id: StageId) -> StageDefinition:
    return STAGES[stage_id]


def get_next_stage(stage_id: StageId) -> Optional[StageId]:
    idx = STAGE_ORDER.index(stage_id)
    if idx + 1 < len(STAGE_ORDER):
        return STAGE_ORDER[idx + 1]
    return None


def get_previous_stage(stage_id: StageId) -> Optional[StageId]:
    idx = STAGE_ORDER.index(stage_id)
    if idx > 0:
        return STAGE_ORDER[idx - 1]
    return None
