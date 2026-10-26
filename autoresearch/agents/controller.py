"""Controller Agent: governs transitions, budgets, rollbacks, and handoffs."""

from typing import Dict, List, Any, Optional

from autoresearch.workflow.stages import StageDefinition, StageId, get_stage
from autoresearch.workflow.cards import CardStatus
from autoresearch.workflow.decision_engine import (
    DecisionAdjudicator,
    DecisionIssue,
    TransitionDecision,
    ActionType,
)
from autoresearch.workflow.state import ProjectState
from autoresearch.workflow.templates import TemplateManager


class ControllerAgent:
    """Decision controller enforcing workflow invariants, budget limits, and rollback paths."""

    def __init__(self, template_manager: TemplateManager):
        self.tm = template_manager

    def evaluate_and_route(
        self,
        stage: StageDefinition,
        critic_results: Dict[str, Any],
        project_state: ProjectState,
        integrity_findings: Optional[List[Dict[str, Any]]] = None,
    ) -> TransitionDecision:
        """Run decision rules against Critic's findings and update workflow state.

        Machine-verified integrity findings are merged in AFTER the Critic and take
        precedence over it: a card the deterministic audit failed cannot be MET,
        whatever the language model concluded.
        """
        cards_dict = critic_results.get("cards", {})
        raw_issues = list(critic_results.get("issues", []))
        integrity_findings = integrity_findings or []

        forced: List[str] = []
        for finding in integrity_findings:
            cid = finding.get("card_id", "")
            # Attribute the finding to a card this stage actually owns, so it lands
            # in the matrix rather than being silently dropped.
            if cid not in stage.cards:
                cid = stage.cards[0] if stage.cards else cid
                finding = {**finding, "card_id": cid}
            entry = cards_dict.setdefault(cid, {})
            entry["name"] = entry.get("name", cid)
            if entry.get("status") != CardStatus.CONFLICT.value:
                forced.append(f"{cid}:{entry.get('status', 'NOT_REVIEWED')}->CONFLICT")
            entry["status"] = CardStatus.CONFLICT.value
            entry["evidence_location"] = finding.get("location", entry.get("evidence_location", ""))
            entry["reason"] = (
                f"[MACHINE-VERIFIED {finding.get('check')}] {finding.get('problem')} "
                f"(deterministic audit; not overridable by review judgement)"
            )
            if not any(i.get("issue_id") == finding.get("issue_id") for i in raw_issues):
                raw_issues.append(finding)

        if forced:
            critic_results["integrity_overrides"] = forced
        card_statuses: Dict[str, CardStatus] = {}

        for cid, info in cards_dict.items():
            st_str = info.get("status", "GAP")
            try:
                card_statuses[cid] = CardStatus(st_str)
            except ValueError:
                card_statuses[cid] = CardStatus.GAP

        decision_issues: List[DecisionIssue] = []

        for iss in raw_issues:
            try:
                owner = StageId(iss.get("owner_stage", stage.id.value))
            except ValueError:
                owner = stage.id

            decision_issues.append(
                DecisionIssue(
                    issue_id=iss.get("issue_id", "ISSUE"),
                    card_id=iss.get("card_id", ""),
                    severity=iss.get("severity", "BLOCKING"),
                    location=iss.get("location", ""),
                    problem=iss.get("problem", ""),
                    owner_stage=owner,
                    minimal_fix=iss.get("minimal_fix", ""),
                    acceptance_criteria=iss.get("acceptance_criteria", ""),
                )
            )

        # Adjudicate action
        decision = DecisionAdjudicator.adjudicate(
            current_stage=stage.id,
            card_statuses=card_statuses,
            issues=decision_issues,
            current_round=project_state.current_round,
            max_rounds=project_state.max_rounds,
        )

        # Persist the card matrix so the audit has history, not just prose in T1.
        for cid, info in cards_dict.items():
            project_state.card_statuses[f"{stage.id.value}:{cid}"] = info.get("status", "NOT_REVIEWED")
        if integrity_findings:
            project_state.integrity_findings[stage.id.value] = integrity_findings
        else:
            project_state.integrity_findings.pop(stage.id.value, None)

        # Update T1 documentation
        self.tm.update_t1(
            stage=stage.id,
            round_num=project_state.current_round,
            card_results=cards_dict,
            issues=raw_issues,
            decision=decision,
        )

        # Handle specific transitions
        if decision.action == ActionType.ROLLBACK and decision.target_stage:
            self.tm.update_t4_rollback(
                current_stage=stage.id,
                target_stage=decision.target_stage,
                reason=decision.reason,
                invalidated_objects=decision.invalidated_objects,
                affected_stages=decision.affected_stages,
            )
            # Update state
            project_state.current_stage = decision.target_stage
            project_state.current_round = 1
            project_state.active_issues = [
                iss for iss in raw_issues if iss.get("severity") == "BLOCKING"
            ]

        elif decision.action == ActionType.REFINE_INLOOP:
            project_state.current_round += 1
            project_state.active_issues = [
                iss for iss in raw_issues if iss.get("severity") == "BLOCKING"
            ]

        elif decision.action == ActionType.CONTINUE:
            # Advance stage
            project_state.resolved_issues.extend(project_state.active_issues)
            project_state.active_issues = []
            project_state.current_round = 1
            if decision.target_stage:
                project_state.current_stage = decision.target_stage

        # Log event in project state
        project_state.log_event(
            event_type=f"STAGE_DECISION_{decision.action.value}",
            details={
                "action": decision.action.value,
                "target_stage": decision.target_stage.value if decision.target_stage else None,
                "reason": decision.reason,
                "blocking_issues_count": len(decision.blocking_issues),
            },
        )

        return decision
