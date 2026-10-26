"""Template rendering and file manager for T0-T5 research artifacts."""

from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

from autoresearch.workflow.stages import StageId
from autoresearch.workflow.cards import CardDefinition, CardStatus


class TemplateManager:
    """Generates and updates the standard T0-T5 Markdown files in a project workspace."""

    def __init__(self, workspace_path: Path):
        self.workspace = workspace_path
        self.workspace.mkdir(parents=True, exist_ok=True)
        self.t0_path = self.workspace / "00_T0_PROJECT_AND_STAGE_CARD.md"
        self.t1_path = self.workspace / "01_T1_REVIEW_AND_REFINE.md"
        self.t2_path = self.workspace / "02_T2_HYPOTHESES_AND_EVIDENCE.md"
        self.t3_path = self.workspace / "03_T3_POC_DECISION_CONTRACT.md"
        self.t4_path = self.workspace / "04_T4_ROLLBACK_AND_HANDOFF.md"
        self.t5_path = self.workspace / "05_T5_UNIFIED_RESEARCH_DRAFT.md"

    def initialize_all(self, project_name: str, topic: str, archetype: str = "方法 (Method)"):
        """Initialize empty T0-T5 templates if they do not already exist."""
        now_str = datetime.now().strftime("%Y-%m-%d")
        
        # T0
        if not self.t0_path.exists():
            t0_content = f"""# T0 项目与阶段启动卡

| 字段 | 填写 |
| --- | --- |
| 项目 / 日期 / 版本 | {project_name} / {now_str} / v1.0 |
| 长期问题及其重要后果 | {topic} |
| 当前最具体未知 | 待 S1 机会探测明确 |
| 主要贡献类型及次要义务 | {archetype} |
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
"""
            self.t0_path.write_text(t0_content, encoding="utf-8")

        # T1
        if not self.t1_path.exists():
            self.t1_path.write_text(
                "# T1 审查与修复记录\n\n尚无审核记录。执行 `autoresearch review` 或 `run` 自动生成。\n",
                encoding="utf-8",
            )

        # T2
        if not self.t2_path.exists():
            t2_content = """# T2 假设与证据台账

## 假设注册：一条可独立判定的主张一行

| H ID | 主张及范围 | 类型 | 核心/辅助 | 依赖 | 最强反方 | 区分预测/证明义务 |
| --- | --- | --- | --- | --- | --- | --- |

| H ID | 支持条件 | 反驳条件 | 未决条件 | 失败影响 | 需修改对象及归属阶段 |
| --- | --- | --- | --- | --- | --- |

## 证据索引

| E ID | 来源类型 | 原始位置/运行 ID | 对象与版本 | 实际观察 | 有效性 | 可支持范围 |
| --- | --- | --- | --- | --- | --- | --- |

## 假设判定

| H ID | 证据 ID | 当前状态 | 适用条件 | 仍未排除的解释 | 状态变化理由 |
| --- | --- | --- | --- | --- | --- |

## 论文主张映射

| Claim ID / 原句 | 核心或扩展 | 需要哪些 H | 支持证据与范围 | 当前缺口 | 保留/收紧/撤回 |
| --- | --- | --- | --- | --- | --- |
"""
            self.t2_path.write_text(t2_content, encoding="utf-8")

        # T3
        if not self.t3_path.exists():
            t3_content = """# T3 PoC 决策合同

## 本轮只需要决定什么
待 S5 阶段生成与冻结。

## 比较设计
待完善。

## 仪器与数据
待校准。

## 如何衡量和决定
待定义。
"""
            self.t3_path.write_text(t3_content, encoding="utf-8")

        # T4
        if not self.t4_path.exists():
            t4_content = "# T4 回退、复核与交接单\n\n当前处于正常推进流程，无回退记录。\n"
            self.t4_path.write_text(t4_content, encoding="utf-8")

        # T5
        if not self.t5_path.exists():
            t5_content = f"""# 01_UNIFIED_RESEARCH_DRAFT：研究主线模板

项目：{project_name}；当前阶段：S1；主稿版本：v0.1；主要贡献类型：{archetype}。

## 1 问题与重要后果（S1）
[待生成]

## 2 问题定义与定位（S2）
[待进入 S2]

## 3 核心假设及依赖（S3）
[待进入 S3]

## 4 方法、分析或形式对象（S4）
[待进入 S4]

## 5 最小验证及决定规则（S5）
[待进入 S5]

## 6 当前 PoC 证据与决定（S6）
[待进入 S6]

## 7 论文证据范围（S7）
[待进入 S7]

## 8 当前可保留的结论与论文论证（S8）
[待进入 S8]

## 9 开放问题与下一项行动
[待更新]

## 10 版本与证据变更
| 日期/版本 | 改变了什么 | 为什么 | 依赖影响 | 尚需复核 |
| --- | --- | --- | --- | --- |
| {now_str}/v0.1 | 项目初始化 | 建立工作底稿 | 无 | 全流程 |
"""
            self.t5_path.write_text(t5_content, encoding="utf-8")

    def update_t1(
        self,
        stage: StageId,
        round_num: int,
        card_results: Dict[str, Dict[str, Any]],
        issues: List[Dict[str, Any]],
        decision: Any,
    ):
        """Write out a complete T1 Review and Refine record."""
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        lines = [
            f"# T1 审查与修复记录",
            f"\n阶段：{stage.value}　审核日期：{now_str}　复审轮次：第 {round_num} 轮\n",
            "## 逐卡判定\n",
            "| 卡 ID | 审查项目 | 状态 | 证据位置 | 评估与理由 |",
            "| --- | --- | --- | --- | --- |",
        ]

        for card_id, res in card_results.items():
            name = res.get("name", card_id)
            status = res.get("status", "NOT_REVIEWED")
            loc = res.get("evidence_location", "产物正文")
            reason = res.get("reason", "").replace("\n", " ")
            lines.append(f"| {card_id} | {name} | **{status}** | {loc} | {reason} |")

        lines.append("\n## 阻塞问题与发现 (Issues)\n")
        if not issues:
            lines.append("本轮无阻塞 Issue，所有适用卡项符合标准。\n")
        else:
            for idx, issue in enumerate(issues, 1):
                lines.extend([
                    f"### Issue #{idx}: [{issue.get('issue_id', f'ISSUE-{idx}')}] {issue.get('problem', '')}",
                    "",
                    f"- **关联卡 ID**: {issue.get('card_id', '')}",
                    f"- **严重度**: {issue.get('severity', 'BLOCKING')}",
                    f"- **具体位置**: {issue.get('location', '')}",
                    f"- **问题实际内容**: {issue.get('actual_content', '')}",
                    f"- **为什么是问题**: {issue.get('impact', '')}",
                    f"- **归属阶段**: {issue.get('owner_stage', stage.value)}",
                    f"- **最小修复**: {issue.get('minimal_fix', '')}",
                    f"- **验收方式**: {issue.get('acceptance_criteria', '')}",
                    f"- **建议动作**: {issue.get('suggested_route', 'REFINE_INLOOP')}",
                    "",
                ])

        lines.extend([
            "## 本轮结论与决策",
            "",
            f"- **转移动作**: **{decision.action.value}**",
            f"- **目标阶段**: {decision.target_stage.value if decision.target_stage else '完成'}",
            f"- **决策理由**: {decision.reason}",
            "",
        ])

        self.t1_path.write_text("\n".join(lines), encoding="utf-8")

    def write_t3_contract(
        self,
        frozen_protocol: Dict[str, Any],
        stage_output: str = "",
    ):
        """Write the S5 PoC decision contract as a real, dated artifact.

        T3 existed only as an unfilled template before, so the pre-registration
        that S6-C2 adjudicates against was never actually recorded anywhere.
        """
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        lines = [
            "# T3 PoC 决策合同 (FROZEN)",
            "",
            f"**冻结时间**: {now_str}",
            f"**冻结阶段**: {frozen_protocol.get('frozen_at_stage', 'S5')}",
            "",
            "> 本合同在任何测量发生之前冻结。S6 执行参数与下表不一致即构成 "
            "`PREREGISTRATION_DRIFT`，必须回退 S5 并留下书面修订，不得就地改写。",
            "",
            "## 冻结参数",
            "",
            "| 参数 | 冻结值 |",
            "| --- | --- |",
            f"| 评测集规模 N | {frozen_protocol.get('primary_cohort') or '未登记'} |",
            f"| 登记的分组规模 | {frozen_protocol.get('cohorts') or '未登记'} |",
            f"| 单例超时 (s) | {frozen_protocol.get('timeouts') or '未登记'} |",
            f"| 解码温度 | {frozen_protocol.get('temperatures') or '未登记'} |",
            f"| 重复次数 | {frozen_protocol.get('repeats') or '未登记'} |",
            "",
            "## S5 协议全文",
            "",
            stage_output or "（S5 阶段产物未提供）",
            "",
        ]
        self.t3_path.write_text("\n".join(lines), encoding="utf-8")

    def write_t2_ledger(
        self,
        evidence_ledger: Dict[str, Any],
        integrity_findings: Dict[str, Any],
    ):
        """Write the cumulative evidence ledger that T2 was supposed to hold."""
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        lines = [
            "# T2 假设与证据台账",
            "",
            f"**更新时间**: {now_str}",
            "",
            "## 各阶段已登记的量化事实",
            "",
            "| 阶段 | 主分母 N | 已登记分母 | 超时 (s) | 温度 | 量化断言数 | 待测占位数 |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ]
        for stage_key in sorted(evidence_ledger):
            ev = evidence_ledger[stage_key]
            lines.append(
                f"| {stage_key} | {ev.get('primary_cohort') or '-'} | {ev.get('denominators') or '-'} "
                f"| {ev.get('timeouts') or '-'} | {ev.get('temperatures') or '-'} "
                f"| {ev.get('claim_count', 0)} | {ev.get('tbd_count', 0)} |"
            )

        lines.extend(["", "## 确定性审计未决违规", ""])
        if not integrity_findings:
            lines.append("当前无未决的机器验证违规。")
        else:
            lines.append("| 阶段 | 检查 | 卡项 | 问题 |")
            lines.append("| --- | --- | --- | --- |")
            for stage_key in sorted(integrity_findings):
                for f in integrity_findings[stage_key]:
                    problem = str(f.get("problem", "")).replace("|", "/")[:160]
                    lines.append(
                        f"| {stage_key} | {f.get('check')} | {f.get('card_id')} | {problem} |"
                    )
        lines.append("")
        self.t2_path.write_text("\n".join(lines), encoding="utf-8")

    def update_t4_rollback(
        self,
        current_stage: StageId,
        target_stage: StageId,
        reason: str,
        invalidated_objects: List[str],
        affected_stages: List[StageId],
    ):
        """Write a T4 rollback record."""
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        lines = [
            "# T4 回退、复核与交接单",
            "",
            f"**记录时间**: {now_str}",
            "",
            "## 动作与理由",
            "",
            f"| 字段 | 填写 |",
            f"| --- | --- |",
            f"| 当前阶段及版本 | {current_stage.value} |",
            f"| 动作 | **ROLLBACK** |",
            f"| 明确目标阶段 | **{target_stage.value}** |",
            f"| 项目状态 | ACTIVE (ROLLING BACK) |",
            f"| 触发原因与依据 | {reason} |",
            f"| 实际失效的对象 | {', '.join(invalidated_objects)} |",
            f"| 为什么由该阶段负责 | 该对象在 {target_stage.value} 首次定义与承诺，修改必须从根源重新闭环 |",
            "",
            "## 依赖影响与标记 NEEDS_RECHECK",
            "",
            "| 上游变更 | 受影响阶段 | 标记 | 处理要求 |",
            "| --- | --- | --- | --- |",
        ]

        for s in affected_stages:
            lines.append(f"| 上游核心前提改变 | {s.value} | NEEDS_RECHECK | 需在目标阶段修复后，顺次重新复核各阶段卡项 |")

        lines.extend([
            "",
            "## 修复指南",
            f"1. 切换至阶段 **{target_stage.value}** 重新开展 Builder 工作，专门修复失效的前提对象；",
            f"2. 保留不依赖该前提的原始有效数据，仅对因果链条断裂的结论做纠偏；",
            f"3. 修复完毕后经 Critic 审查通过，再按顺序返回当前阶段。",
            "",
        ])

        self.t4_path.write_text("\n".join(lines), encoding="utf-8")

    def update_t5_section(self, section_number: int, content: str):
        """Update a specific section in T5 unified research draft."""
        if not self.t5_path.exists():
            return
        current_t5 = self.t5_path.read_text(encoding="utf-8")
        
        # Section header patterns e.g. ## 1 问题与重要后果（S1）
        pattern_header = f"## {section_number} "
        next_header = f"## {section_number + 1} "

        pos_start = current_t5.find(pattern_header)
        if pos_start == -1:
            # Append if not found
            self.t5_path.write_text(current_t5 + f"\n\n## {section_number} 阶段产物\n\n{content}\n", encoding="utf-8")
            return

        end_of_header_line = current_t5.find("\n", pos_start)
        pos_next = current_t5.find(next_header, end_of_header_line)
        if pos_next == -1:
            # Last section
            new_t5 = current_t5[:end_of_header_line] + f"\n\n{content}\n"
        else:
            new_t5 = current_t5[:end_of_header_line] + f"\n\n{content}\n\n" + current_t5[pos_next:]

        self.t5_path.write_text(new_t5, encoding="utf-8")
