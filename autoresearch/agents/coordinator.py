"""Workflow Orchestrator: runs the 7-step loop across S1-S8 research stages."""

from pathlib import Path
from typing import Optional, Dict, Any

from autoresearch.config import Config
from autoresearch.llm.factory import create_llm_client
from autoresearch.workflow.stages import StageId, get_stage, STAGE_ORDER
from autoresearch.workflow.state import ProjectState
from autoresearch.workflow.templates import TemplateManager
from autoresearch.workflow.decision_engine import ActionType, TransitionDecision
from autoresearch.workflow.integrity import (
    audit_stage,
    extract_stage_evidence,
    summarize_for_prompt,
)
from autoresearch.agents.builder import BuilderAgent
from autoresearch.agents.critic import CriticAgent
from autoresearch.agents.controller import ControllerAgent
from autoresearch.utils.logger import (
    print_banner,
    print_info,
    print_success,
    print_warning,
    print_error,
    print_table,
)


class WorkflowOrchestrator:
    """End-to-end orchestrator for Idea-to-Paper Codeless Workflow."""

    def __init__(
        self,
        project_name: str,
        topic: Optional[str] = None,
        contribution_type: str = "方法 (Method)",
        config: Optional[Config] = None,
    ):
        self.config = config or Config()
        self.project_name = project_name
        self.workspace = self.config.workspace_dir / project_name
        self.workspace.mkdir(parents=True, exist_ok=True)

        self.tm = TemplateManager(self.workspace)
        self.llm = create_llm_client(self.config)

        self.builder = BuilderAgent(
            self.llm,
            evidence_mode=self.config.evidence_mode,
            draft_context_chars=self.config.draft_context_chars,
            reference_material=self._load_reference_material(),
            reference_material_chars=self.config.reference_material_chars,
        )
        self.critic = CriticAgent(self.llm)
        self.controller = ControllerAgent(self.tm)

        # Load or initialize project state
        state_file = self.workspace / "project_state.json"
        if state_file.exists():
            self.state = ProjectState.load(self.workspace)
            if topic:
                self.state.topic = topic
            if contribution_type:
                self.state.contribution_type = contribution_type
        else:
            default_topic = topic or "Automated Reasoning & Verification with LLMs"
            self.state = ProjectState(
                project_id=f"proj_{project_name}",
                name=project_name,
                topic=default_topic,
                contribution_type=contribution_type,
                current_stage=StageId.S1,
                current_round=1,
                max_rounds=self.config.max_refine_rounds + 1,
            )
            self.state.save(self.workspace)
            self.tm.initialize_all(
                project_name=project_name,
                topic=default_topic,
                archetype=contribution_type,
            )

    def _load_reference_material(self) -> str:
        """Read the reference paper, if one was configured. Never fatal."""
        path = self.config.reference_material_path
        if not path:
            return ""
        path = Path(path)
        if not path.exists():
            print_warning(f"[Reference] Configured reference material not found: {path}")
            return ""
        text = path.read_text(encoding="utf-8", errors="replace")
        print_info(f"[Reference] Loaded {len(text)} chars of reference material from {path.name}")
        return text

    def execute_current_stage_step(self) -> TransitionDecision:
        """Execute one complete Builder -> Critic -> Controller cycle for the current stage."""
        stage = get_stage(self.state.current_stage)
        stage_idx = STAGE_ORDER.index(stage.id) + 1
        # Stamp the governing mode so a later audit uses the same rules.
        self.state.evidence_mode = self.config.evidence_mode

        print_banner(
            f"Stage {stage.id.value}: {stage.name}",
            f"Topic: {self.state.topic} | Round {self.state.current_round}/{self.state.max_rounds}",
        )

        # 1. Read current working draft
        t5_draft = ""
        if self.tm.t5_path.exists():
            t5_draft = self.tm.t5_path.read_text(encoding="utf-8")

        # 2. Builder execution, anchored to what upstream stages already registered
        carried_facts = summarize_for_prompt(self.state.evidence_ledger, self.state.frozen_protocol)
        print_info(f"[Builder] Generating deliverables for {stage.id.value} (Round {self.state.current_round})...")
        stage_output = self.builder.build_stage(
            stage=stage,
            project_state=self.state,
            unified_draft=t5_draft,
            issues=self.state.active_issues,
            round_num=self.state.current_round,
            carried_facts=carried_facts,
        )

        # Save stage output file
        stage_file = self.workspace / f"stage_output_{stage.id.value}.md"
        stage_file.write_text(stage_output, encoding="utf-8")
        self.state.stage_outputs[stage.id.value] = stage_output

        # Update section in T5
        self.tm.update_t5_section(stage_idx, stage_output)
        print_success(f"[Builder] Deliverable saved to {stage_file.name} and synced to T5 draft.")

        # 3. Deterministic integrity audit. Runs before the Critic so its findings
        #    inform the review, and is re-applied after it so they cannot be argued away.
        findings = audit_stage(
            stage_id=stage.id,
            stage_output=stage_output,
            workspace=self.workspace,
            prior_evidence=self.state.evidence_ledger,
            frozen_protocol=self.state.frozen_protocol or None,
            evidence_mode=self.config.evidence_mode,
        )
        finding_dicts = [f.to_issue() for f in findings]
        if finding_dicts:
            print_error(f"[Integrity] {len(finding_dicts)} machine-verified violation(s) in {stage.id.value}:")
            for f in finding_dicts:
                print_warning(f"  - [{f['check']}] {f['card_id']}: {f['problem'][:120]}")
        else:
            print_success(f"[Integrity] {stage.id.value} passed all deterministic evidence checks.")

        # 4. Critic review
        print_info(f"[Critic] Auditing deliverable against 6 review cards in {stage.id.value}...")
        critic_results = self.critic.review_stage(
            stage=stage,
            stage_output=stage_output,
            project_state=self.state,
            round_num=self.state.current_round,
            carried_facts=carried_facts,
            integrity_findings=finding_dicts,
        )

        # Display Critic Card Statuses in table
        headers = ["Card ID", "Status", "Inspection Location", "Reason"]
        rows = []
        for cid, info in critic_results["cards"].items():
            rows.append([
                cid,
                info.get("status", "GAP"),
                info.get("evidence_location", "")[:25],
                info.get("reason", "")[:50],
            ])
        print_table(headers, rows, title=f"Critic Review Card Matrix ({stage.id.value})")

        # 5. Controller decision (integrity findings override the review verdict)
        decision = self.controller.evaluate_and_route(
            stage=stage,
            critic_results=critic_results,
            project_state=self.state,
            integrity_findings=finding_dicts,
        )

        # 6. Register what this stage asserted, so later stages are checked against
        #    it rather than only against themselves.
        self._register_evidence(stage.id, stage_output, decision)

        # 7. Persist updated state
        self.state.save(self.workspace)

        # Report decision
        if decision.action == ActionType.CONTINUE:
            print_success(f"[Controller] Decision: CONTINUE -> Next: {decision.target_stage.value if decision.target_stage else 'FINISHED'}")
            print_info(f"Reason: {decision.reason}")
        elif decision.action == ActionType.REFINE_INLOOP:
            print_warning(f"[Controller] Decision: REFINE_INLOOP (Remaining issues: {len(decision.blocking_issues)})")
            print_info(f"Reason: {decision.reason}")
        elif decision.action == ActionType.ROLLBACK:
            print_error(f"[Controller] Decision: ROLLBACK -> Returning to {decision.target_stage.value}")
            print_warning(f"Invalidated Objects: {', '.join(decision.invalidated_objects)}")
        elif decision.action == ActionType.PAUSE:
            print_warning(f"[Controller] Decision: PAUSE (Budget exhausted).")
            print_info(f"Reason: {decision.reason}")

        return decision

    def _register_evidence(self, stage_id: StageId, stage_output: str, decision) -> None:
        """Record this stage's asserted facts; freeze the S5 contract on exit from S5."""
        evidence = extract_stage_evidence(stage_id, stage_output)
        self.state.evidence_ledger[stage_id.value] = evidence.to_dict()

        if stage_id == StageId.S5 and decision.action == ActionType.CONTINUE:
            # The protocol becomes immutable the moment S5 is signed off. Anything
            # S6 does differently is drift, not a design choice.
            self.state.frozen_protocol = {
                "frozen_at_stage": StageId.S5.value,
                "primary_cohort": evidence.primary_cohort,
                "cohorts": evidence.cohorts,
                "timeouts": evidence.timeouts,
                "temperatures": evidence.temperatures,
                "repeats": evidence.repeats,
            }
            self.tm.write_t3_contract(self.state.frozen_protocol, stage_output)
            print_success(
                f"[Protocol] S5 contract frozen into T3: N={evidence.primary_cohort}, "
                f"timeout={evidence.timeouts}, temp={evidence.temperatures}, repeats={evidence.repeats}"
            )

        self.tm.write_t2_ledger(self.state.evidence_ledger, self.state.integrity_findings)

    def run_stage_to_completion(self, stage_id: Optional[StageId] = None) -> TransitionDecision:
        """Run refine cycles for the specified stage until it transitions (CONTINUE, ROLLBACK, or PAUSE)."""
        target_stage = stage_id or self.state.current_stage
        self.state.current_stage = target_stage

        while True:
            decision = self.execute_current_stage_step()
            if decision.action != ActionType.REFINE_INLOOP:
                return decision

    def run_pipeline(
        self,
        start_stage: Optional[StageId] = None,
        stop_stage: Optional[StageId] = None,
    ):
        """Run the automated pipeline across multiple stages."""
        if start_stage:
            self.state.current_stage = start_stage

        end_stage = stop_stage or StageId.S8

        print_banner(
            f"Starting Idea-to-Paper Research Pipeline",
            f"Project: {self.project_name} | Target: {end_stage.value}",
        )

        while True:
            curr = self.state.current_stage
            decision = self.execute_current_stage_step()

            if decision.action == ActionType.PAUSE:
                print_error(f"Pipeline PAUSED at {curr.value}: {decision.reason}")
                break

            if decision.action == ActionType.CONTINUE:
                if curr == end_stage or decision.target_stage is None:
                    print_banner("Research Pipeline Complete!", f"Deliverable ready in {self.workspace}")
                    break

            # If REFINE_INLOOP or ROLLBACK, the loop naturally continues at the updated self.state.current_stage
