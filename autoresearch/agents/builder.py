"""Builder Agent: executes research tasks and drafts stage deliverables."""

from pathlib import Path
from typing import List, Dict, Optional, Any

from autoresearch.llm.base import BaseLLMClient
from autoresearch.workflow.stages import StageDefinition, StageId
from autoresearch.workflow.state import ProjectState


class BuilderAgent:
    """Research executor (Builder) responsible for producing stage artifacts and resolving issues."""

    def __init__(self, llm_client: BaseLLMClient, evidence_mode: str = "SIMULATED",
                 draft_context_chars: int = 24000, reference_material: str = "",
                 reference_material_chars: int = 40000):
        self.llm = llm_client
        self.reference_material = reference_material
        self.reference_material_chars = reference_material_chars
        self.evidence_mode = evidence_mode.upper()
        self.draft_context_chars = draft_context_chars

    def build_stage(
        self,
        stage: StageDefinition,
        project_state: ProjectState,
        unified_draft: str,
        issues: Optional[List[Dict[str, Any]]] = None,
        round_num: int = 1,
        carried_facts: str = "",
    ) -> str:
        """Generate or refine deliverables for the specified stage."""
        is_refinement = bool(issues and len(issues) > 0)

        system_instruction = (
            "You are the Builder (研究执行者) in the Idea-to-Paper Codeless Workflow.\n"
            "Your duty is to produce rigorous, faithful, and verifiable academic research deliverables.\n"
            "Strict rules:\n"
            "1. Ground all claims, observations, and numbers in explicit, verifiable sources or protocols.\n"
            "2. Do NOT extrapolate beyond the given scope. Clearly label unobserved possibilities as hypotheses.\n"
            "3. If resolving review issues, target the exact acceptance criteria without introducing new unsubstantiated claims.\n"
            "4. Structure your response clearly with Markdown headers corresponding to the stage's minimum deliverables."
        )

        system_instruction += self._evidence_discipline(stage)
        system_instruction += self._reference_discipline()

        prompt_parts = [
            f"# 当前工作阶段: {stage.id.value} - {stage.name}",
            f"**阶段目标**: {stage.goal}",
            f"**项目主题**: {project_state.topic}",
            f"**主要贡献类型**: {project_state.contribution_type}",
            f"**当前审查轮次**: 第 {round_num} 轮",
            "",
            "## 阶段执行步骤:",
            "\n".join(stage.steps),
            "",
            "## 阶段最小交付要求:",
            "\n".join(stage.minimum_deliverables),
            "",
            "## 当前不要求什么（避免早熟过度设计）:",
            stage.not_required_now,
            "",
            "## 上游已登记事实 (Registered Upstream Facts — 必须保持一致):",
            carried_facts or "（尚无已登记的上游事实）",
            "",
            *self._reference_section(),
            "## 现有统一研究底稿 (T5 Draft 上下文):",
            self._draft_context(unified_draft),
            "",
        ]

        if is_refinement:
            prompt_parts.extend([
                "## 上一轮审核指出的阻塞问题 (Issues to Resolve):",
                "请严格按照每个 Issue 的'最小修复'与'验收方式'进行有针对性的修改：",
            ])
            for idx, iss in enumerate(issues, 1):
                prompt_parts.append(
                    f"{idx}. [{iss.get('issue_id')}] 卡项: {iss.get('card_id')}\n"
                    f"   位置: {iss.get('location')}\n"
                    f"   问题: {iss.get('problem')}\n"
                    f"   最小修复建议: {iss.get('minimal_fix')}\n"
                    f"   验收标准: {iss.get('acceptance_criteria')}\n"
                )
            prompt_parts.append("\n请在本次产物中明确体现针对上述问题的修正，并给出更新后的完整阶段交付文档。")
        else:
            prompt_parts.append(
                "请根据以上指南，完整编写并输出本阶段的最小交付产物 Markdown。"
            )

        full_prompt = "\n".join(prompt_parts)
        response = self.llm.generate(
            prompt=full_prompt,
            system_instruction=system_instruction,
            json_mode=False,
            timeout=300,
        )
        return response.content

    def _draft_context(self, unified_draft: str) -> str:
        """Carry the head and tail of the draft, not a blind prefix.

        The opening sections fix the problem framing; the most recent sections are
        what this stage must build on. Truncating to a prefix alone made late stages
        invent a fresh experimental setup each time.
        """
        if not unified_draft:
            return "（初始状态，底稿尚为空白）"
        budget = self.draft_context_chars
        if len(unified_draft) <= budget:
            return unified_draft
        head = budget // 3
        tail = budget - head
        return (
            unified_draft[:head]
            + f"\n\n...（中段省略 {len(unified_draft) - budget} 字符）...\n\n"
            + unified_draft[-tail:]
        )

    def _evidence_discipline(self, stage: StageDefinition) -> str:
        """Rules governing what the Builder may assert as a measured result."""
        if stage.id not in (StageId.S6, StageId.S7, StageId.S8):
            return ""

        if self.evidence_mode == "MEASURED":
            return (
                "\n\nEVIDENCE RULES (evidence_mode=MEASURED):\n"
                "- Every reported number must come from an artifact that exists on disk, cited by its real path.\n"
                "- Never invent a file path, run ID, or commit hash. A citation that cannot be opened is a fabrication.\n"
                "- Protocol parameters (cohort size, timeout, temperature, repetitions) must match the frozen S5 "
                "contract exactly. If they cannot, say so and request a rollback instead of silently changing them.\n"
            )

        return (
            "\n\nEVIDENCE RULES (evidence_mode=SIMULATED) — THESE OVERRIDE ANY INSTINCT TO PRODUCE A COMPLETE-LOOKING PAPER:\n"
            "- No instrument has been executed. You have measured NOTHING.\n"
            "- You MUST NOT state any measured result: no percentages, no n/m fractions, no speedups, no runtimes, "
            "no solved counts, no baseline comparisons with numbers.\n"
            "- For every quantity the protocol WILL produce, write a placeholder [TBD-MEASURE:<metric-id>] and, next "
            "to it, the exact procedure and artifact path that will fill it.\n"
            "- You MAY state declared targets, thresholds, budgets and timeouts as numbers, because those are "
            "commitments rather than observations.\n"
            "- You MUST NOT cite any log file, CSV, run ID, or commit hash as existing evidence.\n"
            "- Your deliverable is a pre-registered protocol and a frozen-design manuscript whose results slots are "
            "explicitly empty. That is the correct and complete output. A manuscript with invented numbers is a "
            "failed deliverable, not a better one.\n"
        )

    def _reference_section(self) -> List[str]:
        """Prior published work, clearly fenced off from this project's own evidence."""
        if not self.reference_material:
            return []
        return [
            "## 参考文献原文 (Reference Material — 用于复现/对照，不得冒充本项目自有证据):",
            self.reference_material[: self.reference_material_chars],
            "",
        ]

    def _reference_discipline(self) -> str:
        if not self.reference_material:
            return ""
        return (
            "\n\nREFERENCE MATERIAL RULES:\n"
            "- The reference text is PRIOR PUBLISHED WORK, not your results.\n"
            "- You may use it to align problem framing, terminology, baselines and related work.\n"
            "- You MUST NOT copy its experimental numbers and present them as this project's measurements. "
            "A number taken from the reference is a CITATION and must be written as "
            "'(cited from reference, not measured here)'.\n"
            "- Reproducing a paper means re-deriving its design and re-running its protocol, "
            "not restating its reported results.\n"
        )
