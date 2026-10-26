"""Decision and rollback adjudication engine based on 02_DECISION_AND_ROLLBACK_MAP."""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional, Any

from autoresearch.workflow.stages import StageId, STAGE_ORDER, get_next_stage
from autoresearch.workflow.cards import CardStatus


class ActionType(str, Enum):
    CONTINUE = "CONTINUE"
    REFINE_INLOOP = "REFINE_INLOOP"
    ROLLBACK = "ROLLBACK"
    PAUSE = "PAUSE"
    CLOSE = "CLOSE"


# Root-cause owner stage mapping table
ROOT_CAUSE_MAPPING: Dict[str, StageId] = {
    "现象入口或重要后果": StageId.S1,
    "研究单位、目标、信息、范围或主要贡献": StageId.S2,
    "承重假设、解释或区分预测": StageId.S3,
    "技术对象、构造、方法身份或核心推导": StageId.S4,
    "测量、对照、样本/独立单位或判定协议": StageId.S5,
    "实际执行、汇总或已有证据判定": StageId.S6,
    "独立确认、扩展、边界或论文证据范围": StageId.S7,
    "文字、引用位置、论证组织": StageId.S8,
}


@dataclass
class DecisionIssue:
    issue_id: str
    card_id: str
    severity: str  # "BLOCKING" or "ADVISORY"
    location: str
    problem: str
    owner_stage: StageId
    minimal_fix: str
    acceptance_criteria: str


@dataclass
class TransitionDecision:
    action: ActionType
    current_stage: StageId
    target_stage: Optional[StageId]
    reason: str
    blocking_issues: List[DecisionIssue] = field(default_factory=list)
    invalidated_objects: List[str] = field(default_factory=list)
    affected_stages: List[StageId] = field(default_factory=list)


class DecisionAdjudicator:
    """Evaluates Critic review results and issues to decide whether to CONTINUE, REFINE, or ROLLBACK."""

    @staticmethod
    def adjudicate(
        current_stage: StageId,
        card_statuses: Dict[str, CardStatus],
        issues: List[DecisionIssue],
        current_round: int,
        max_rounds: int,
    ) -> TransitionDecision:
        """Adjudicate stage transition according to the strict priority rules in 02_DECISION_AND_ROLLBACK_MAP."""
        curr_idx = STAGE_ORDER.index(current_stage)
        blocking_issues = [i for i in issues if i.severity == "BLOCKING"]

        # Priority 1: Check if any blocking issue belongs to an EARLIER upstream stage
        upstream_failures: List[DecisionIssue] = []
        for issue in blocking_issues:
            owner_idx = STAGE_ORDER.index(issue.owner_stage)
            if owner_idx < curr_idx:
                upstream_failures.append(issue)

        if upstream_failures:
            # Sort to find the EARLIEST failed upstream premise
            earliest_issue = min(
                upstream_failures,
                key=lambda x: STAGE_ORDER.index(x.owner_stage),
            )
            target = earliest_issue.owner_stage
            target_idx = STAGE_ORDER.index(target)

            # Mark all downstream stages between target and current as affected
            affected = [STAGE_ORDER[i] for i in range(target_idx + 1, curr_idx + 1)]

            return TransitionDecision(
                action=ActionType.ROLLBACK,
                current_stage=current_stage,
                target_stage=target,
                reason=(
                    f"Upstream premise invalidated: Issue {earliest_issue.issue_id} "
                    f"({earliest_issue.card_id}) belongs to {target.value}. "
                    f"Problem: {earliest_issue.problem}"
                ),
                blocking_issues=upstream_failures,
                invalidated_objects=[earliest_issue.problem],
                affected_stages=affected,
            )

        # Priority 2: Check current stage blocking issues or gaps
        current_blocking = [
            i for i in blocking_issues if i.owner_stage == current_stage
        ]
        has_unresolved_gaps_or_conflicts = any(
            s in [CardStatus.GAP, CardStatus.CONFLICT] for s in card_statuses.values()
        )

        if current_blocking or has_unresolved_gaps_or_conflicts:
            # Check budget
            if current_round >= max_rounds:
                return TransitionDecision(
                    action=ActionType.PAUSE,
                    current_stage=current_stage,
                    target_stage=current_stage,
                    reason=(
                        f"Iteration budget exhausted ({current_round}/{max_rounds} rounds). "
                        f"Unresolved blocking issues remain. Pausing to avoid ungrounded progression."
                    ),
                    blocking_issues=current_blocking,
                )
            
            return TransitionDecision(
                action=ActionType.REFINE_INLOOP,
                current_stage=current_stage,
                target_stage=current_stage,
                reason=(
                    f"Stage {current_stage.value} has {len(current_blocking)} blocking issues "
                    f"requiring in-loop refinement (Round {current_round}/{max_rounds})."
                ),
                blocking_issues=current_blocking,
            )

        # Priority 3: Check if all essential cards are MET or N/A
        all_met = all(
            s in [CardStatus.MET, CardStatus.NA] for s in card_statuses.values()
        )
        if not all_met:
            # Some cards are still NOT_REVIEWED or indeterminate
            return TransitionDecision(
                action=ActionType.REFINE_INLOOP,
                current_stage=current_stage,
                target_stage=current_stage,
                reason=f"Not all required cards are MET or N/A in {current_stage.value}.",
            )

        # All passed! Advance to next stage or complete
        next_stage = get_next_stage(current_stage)
        if next_stage is None:
            return TransitionDecision(
                action=ActionType.CONTINUE,
                current_stage=current_stage,
                target_stage=None,
                reason="All S1-S8 stages successfully completed. Research paper and audit finalized.",
            )

        return TransitionDecision(
            action=ActionType.CONTINUE,
            current_stage=current_stage,
            target_stage=next_stage,
            reason=(
                f"All required review cards in {current_stage.value} MET. "
                f"Advancing to {next_stage.value}."
            ),
        )
