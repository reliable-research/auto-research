from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any
from uuid import uuid4

from .models import Budget, PermissionSet, Risk
from .project import Project, utc_now
from .registry import AgentPackage


class PolicyError(RuntimeError):
    """Raised when permissions, approval, or budget are insufficient."""


@dataclass(frozen=True)
class PolicyDecision:
    status: str
    permissions: PermissionSet
    budget: Budget
    reason: str | None = None


class PolicyEngine:
    def __init__(self, project: Project):
        self.project = project
        policy = project.manifest.get("policy", {})
        self.maximum_permissions = PermissionSet.from_dict(policy.get("permissions"))
        self.maximum_budget = Budget.from_dict(policy.get("budget"))

    def decide(
        self,
        *,
        run_id: str,
        stage_id: str,
        stage_risk: Risk,
        package: AgentPackage,
        control_mode: str,
    ) -> PolicyDecision:
        requested = package.manifest.permissions
        if not self.maximum_permissions.allows(requested):
            return PolicyDecision(
                status="denied",
                permissions=requested.intersect(self.maximum_permissions),
                budget=_budget_intersection(package.manifest.budget, self.maximum_budget),
                reason="agent requests permissions outside project policy",
            )
        risk = max(stage_risk, package.manifest.risk)
        budget = _budget_intersection(package.manifest.budget, self.maximum_budget)
        approval_required = _approval_required(control_mode, risk)
        if not approval_required:
            return PolicyDecision("approved", requested, budget)
        approval = self._find_approval(
            run_id=run_id,
            stage_id=stage_id,
            agent_digest=package.package_digest,
        )
        if not approval:
            return PolicyDecision(
                status="waiting_approval",
                permissions=requested,
                budget=budget,
                reason=f"{risk.name} stage requires approval in {control_mode} mode",
            )
        granted = PermissionSet.from_dict(json.loads(approval["granted_json"]))
        if not granted.allows(requested):
            return PolicyDecision(
                status="denied",
                permissions=granted,
                budget=budget,
                reason="approval did not grant the requested permission subset",
            )
        return PolicyDecision("approved", requested, budget)

    def grant(
        self,
        *,
        run_id: str,
        stage_id: str,
        package: AgentPackage,
        permissions: PermissionSet | None = None,
        scope: str = "stage",
    ) -> str:
        if scope not in {"stage", "run"}:
            raise PolicyError("approval scope must be stage or run")
        granted = permissions or package.manifest.permissions
        if not self.maximum_permissions.allows(granted):
            raise PolicyError("approval cannot exceed project policy")
        if not granted.allows(package.manifest.permissions):
            raise PolicyError("approval must satisfy the agent's required permissions")
        approval_id = "apr_" + uuid4().hex
        with self.project.connect() as connection:
            connection.execute(
                """
                INSERT INTO approvals(id, run_id, stage_id, agent_digest, granted_json, scope, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    approval_id,
                    run_id,
                    stage_id,
                    package.package_digest,
                    json.dumps(granted.to_dict(), sort_keys=True),
                    scope,
                    utc_now(),
                ),
            )
        return approval_id

    def _find_approval(self, *, run_id: str, stage_id: str, agent_digest: str) -> dict[str, Any] | None:
        with self.project.connect() as connection:
            row = connection.execute(
                """
                SELECT * FROM approvals
                WHERE run_id = ? AND agent_digest = ?
                  AND ((scope = 'stage' AND stage_id = ?) OR scope = 'run')
                ORDER BY created_at DESC LIMIT 1
                """,
                (run_id, agent_digest, stage_id),
            ).fetchone()
        return dict(row) if row else None


def _approval_required(control_mode: str, risk: Risk) -> bool:
    if control_mode == "manual":
        return True
    if risk >= Risk.R4:
        return True
    if control_mode == "copilot":
        return risk >= Risk.R2
    if control_mode == "autopilot":
        return risk > Risk.R3
    raise PolicyError(f"unknown control mode: {control_mode}")


def _budget_intersection(requested: Budget, maximum: Budget) -> Budget:
    costs = [item for item in (requested.max_cost_usd, maximum.max_cost_usd) if item > 0]
    return Budget(
        max_wall_seconds=min(requested.max_wall_seconds, maximum.max_wall_seconds),
        max_tool_calls=min(requested.max_tool_calls, maximum.max_tool_calls),
        max_sources=min(requested.max_sources, maximum.max_sources),
        max_cost_usd=min(costs) if costs else 0.0,
    )
