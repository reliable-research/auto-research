"""Critic Agent: performs strict, card-by-card audit of stage research deliverables."""

import json
from typing import Dict, List, Any, Optional

from autoresearch.llm.base import BaseLLMClient
from autoresearch.workflow.stages import StageDefinition, StageId
from autoresearch.workflow.cards import CardDefinition, CardStatus, CARDS
from autoresearch.workflow.state import ProjectState


class CriticAgent:
    """Rigorous academic reviewer (Critic) inspecting deliverables against the 48 review cards."""

    def __init__(self, llm_client: BaseLLMClient):
        self.llm = llm_client

    def review_stage(
        self,
        stage: StageDefinition,
        stage_output: str,
        project_state: ProjectState,
        round_num: int = 1,
        carried_facts: str = "",
        integrity_findings: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        """Perform multi-card evaluation and produce structured verdicts and issues."""
        stage_cards = [CARDS[cid] for cid in stage.cards if cid in CARDS]

        system_instruction = (
            "You are the Critic (审核者) in the Idea-to-Paper Codeless Workflow.\n"
            "Your role is to rigorously, objectively evaluate research artifacts against the stage's 6 review cards.\n"
            "CRITICAL RULES:\n"
            "1. Do NOT add blocking issues based on personal style or preferences. Rely strictly on the card definitions.\n"
            "2. Valid statuses: 'MET' (fully satisfied), 'GAP' (essential content missing), 'CONFLICT' (contradiction/invalid), 'N/A' (not applicable to this contribution archetype).\n"
            "3. If any card is 'GAP' or 'CONFLICT', you MUST generate a corresponding BLOCKING Issue with exact location, problem statement, owner stage, minimal fix, and acceptance criteria.\n"
            "4. Follow the root-cause ownership principle: determine which stage owns the root cause (S1-S8).\n"
            "5. Respond in strictly valid JSON format matching the schema provided.\n"
            "6. A deterministic pre-audit has already run. Any finding it reports is MACHINE-VERIFIED FACT: you "
            "may not mark the affected card MET, and you may not argue it away. Restate it as a BLOCKING issue "
            "with a precise location.\n"
            "7. Check the deliverable against the REGISTERED UPSTREAM FACTS, not only against itself. A number, "
            "cohort size or resource budget that contradicts an upstream fact is a CONFLICT, even if this "
            "document is internally consistent."
        )

        cards_prompt_section = []
        for c in stage_cards:
            cards_prompt_section.append(
                f"### 卡项 {c.card_id} · {c.name}\n"
                f"- **为什么查**: {c.why_check}\n"
                f"- **检查哪里**: {c.where_to_check}\n"
                f"- **怎么检查**: {c.how_to_check}\n"
                f"- **什么算有问题**: {c.what_counts_as_problem}\n"
                f"- **期望产物**: {c.expected_deliverable}\n"
                f"- **验收标准**: {c.acceptance_criteria}\n"
                f"- **默认归属阶段**: {c.target_stage.value}\n"
            )

        prompt = f"""
# 待审查阶段: {stage.id.value} - {stage.name}
**项目主题**: {project_state.topic}
**主要贡献类型**: {project_state.contribution_type}
**当前审查轮次**: 第 {round_num} 轮
**证据模式 (evidence_mode)**: {getattr(project_state, "evidence_mode", "SIMULATED")}

## 上游已登记事实 (Registered Upstream Facts):
{carried_facts or "（尚无已登记的上游事实）"}

## 确定性预审发现 (Machine-Verified Findings — 不得判为 MET):
{self._render_findings(integrity_findings)}

## 适用的 6 张审查卡与判定准则:
{"".join(cards_prompt_section)}

## 待审查的阶段产物文本:
\"\"\"
{stage_output}
\"\"\"

## 要求输出格式 (JSON Schema):
{{
  "cards": {{
    "{stage_cards[0].card_id}": {{
      "name": "{stage_cards[0].name}",
      "status": "MET" | "GAP" | "CONFLICT" | "N/A",
      "evidence_location": "引文或章节位置",
      "reason": "详细判定理由"
    }},
    ... (覆盖本阶段全部 6 张卡)
  }},
  "issues": [
    {{
      "issue_id": "ISSUE-01",
      "card_id": "{stage_cards[0].card_id}",
      "severity": "BLOCKING" | "ADVISORY",
      "location": "文件具体章节/表格/句子",
      "actual_content": "有问题的原句或内容摘要",
      "problem": "具体违反了卡项的什么规则",
      "impact": "为什么该问题影响当前或后续承诺",
      "owner_stage": "{stage.id.value}",
      "minimal_fix": "具体的最小修改动作",
      "acceptance_criteria": "审核者如何核对新证据以验收关闭",
      "suggested_route": "REFINE_INLOOP" | "ROLLBACK" | "CONTINUE"
    }}
  ]
}}
"""

        response = self.llm.generate(
            prompt=prompt,
            system_instruction=system_instruction,
            json_mode=True,
            timeout=300,
        )

        parsed = response.parsed_json or {}
        return self._normalize_review_output(stage, parsed)

    @staticmethod
    def _render_findings(findings: Optional[List[Dict[str, Any]]]) -> str:
        if not findings:
            return "（确定性预审未发现违规）"
        out = []
        for f in findings:
            out.append(
                f"- [{f.get('check')}] 卡项 {f.get('card_id')} @ {f.get('location')}\n"
                f"  事实: {f.get('problem')}\n"
                f"  影响: {f.get('impact')}"
            )
        return "\n".join(out)

    def _normalize_review_output(
        self, stage: StageDefinition, raw_dict: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Ensure all required cards have valid statuses and issues are well-structured."""
        cards_data = raw_dict.get("cards", {})
        normalized_cards = {}

        for cid in stage.cards:
            card_def = CARDS.get(cid)
            card_name = card_def.name if card_def else cid
            if cid in cards_data and isinstance(cards_data[cid], dict):
                c_item = cards_data[cid]
                raw_status = str(c_item.get("status", "NOT_REVIEWED")).upper()
                status = raw_status if raw_status in ["MET", "GAP", "CONFLICT", "N/A"] else "GAP"
                normalized_cards[cid] = {
                    "name": card_name,
                    "status": status,
                    "evidence_location": c_item.get("evidence_location", "阶段交付文档"),
                    "reason": c_item.get("reason", "无审核附注"),
                }
            else:
                # Default fallback
                normalized_cards[cid] = {
                    "name": card_name,
                    "status": "GAP",
                    "evidence_location": "缺失",
                    "reason": "未在产物中找到该卡项对应的完整检查证据",
                }

        raw_issues = raw_dict.get("issues", [])
        normalized_issues = []
        for idx, iss in enumerate(raw_issues, 1):
            if not isinstance(iss, dict):
                continue
            card_id = iss.get("card_id", stage.cards[0])
            owner_stage_str = iss.get("owner_stage", stage.id.value).upper()
            try:
                owner_stage = StageId(owner_stage_str)
            except ValueError:
                owner_stage = stage.id

            normalized_issues.append({
                "issue_id": iss.get("issue_id", f"ISS-{stage.id.value}-{idx:02d}"),
                "card_id": card_id,
                "severity": iss.get("severity", "BLOCKING").upper(),
                "location": iss.get("location", "交付产物"),
                "actual_content": iss.get("actual_content", ""),
                "problem": iss.get("problem", "存在未闭环缺口"),
                "impact": iss.get("impact", "影响阶段承诺"),
                "owner_stage": owner_stage.value,
                "minimal_fix": iss.get("minimal_fix", "根据卡项规范补充证据或修订范围"),
                "acceptance_criteria": iss.get("acceptance_criteria", "审核者复核修正后的内容与证据位置"),
                "suggested_route": iss.get("suggested_route", "REFINE_INLOOP"),
            })

        return {
            "cards": normalized_cards,
            "issues": normalized_issues,
        }
