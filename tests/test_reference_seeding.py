"""Reference material must reach the Builder, fenced off from the project's own evidence.

CLAUDE.md claimed run_paper_pipeline.py was "pre-seeded with ASE 2024 paper text",
but paper_text.txt was referenced by no code at all -- the pipeline only ever saw
the two-line TOPIC string, which is why the "reproduction" matched the real paper
on nothing. These tests pin the wiring shut.
"""

import tempfile
from pathlib import Path

import pytest

from autoresearch.agents.builder import BuilderAgent
from autoresearch.config import Config
from autoresearch.llm.base import BaseLLMClient, LLMResponse
from autoresearch.workflow.stages import StageId, get_stage
from autoresearch.workflow.state import ProjectState

REFERENCE_HEADING = "参考文献原文 (Reference Material"
NO_LAUNDERING = "不得冒充本项目自有证据"
RULES_MARKER = "REFERENCE MATERIAL RULES"


class RecordingLLM(BaseLLMClient):
    """Captures the prompt instead of calling the real agy CLI."""

    def __init__(self):
        self.prompt = None
        self.system_instruction = None

    def generate(self, prompt, system_instruction=None, json_mode=False, timeout=300, **kwargs):
        self.prompt = prompt
        self.system_instruction = system_instruction
        return LLMResponse(content="# stage output")

    def health_check(self) -> bool:
        return True


@pytest.fixture
def state():
    return ProjectState(
        project_id="proj_t", name="t", topic="invariant generation for BMC",
        contribution_type="方法 (Method)",
    )


def _build(llm, state, reference="", chars=40000):
    agent = BuilderAgent(
        llm, evidence_mode="SIMULATED", reference_material=reference,
        reference_material_chars=chars,
    )
    agent.build_stage(
        stage=get_stage(StageId.S2), project_state=state, unified_draft="", round_num=1,
    )
    return agent


def test_reference_material_reaches_the_prompt(state):
    llm = RecordingLLM()
    _build(llm, state, reference="ESBMC ibmc solves 101 of 133 code2inv programs.")
    assert "ESBMC ibmc solves 101 of 133 code2inv programs." in llm.prompt
    assert REFERENCE_HEADING in llm.prompt


def test_reference_is_fenced_against_evidence_laundering(state):
    llm = RecordingLLM()
    _build(llm, state, reference="Table 3: SeaHorn 115, ESBMC ibmc 101.")
    assert NO_LAUNDERING in llm.prompt
    assert RULES_MARKER in llm.system_instruction
    assert "CITATION" in llm.system_instruction


def test_no_reference_section_when_none_supplied(state):
    llm = RecordingLLM()
    _build(llm, state, reference="")
    assert REFERENCE_HEADING not in llm.prompt
    assert NO_LAUNDERING not in llm.prompt
    assert RULES_MARKER not in (llm.system_instruction or "")


def test_reference_material_is_truncated(state):
    llm = RecordingLLM()
    _build(llm, state, reference="X" * 5000, chars=1200)
    assert "X" * 1200 in llm.prompt
    assert "X" * 1201 not in llm.prompt


def test_missing_reference_path_does_not_raise():
    cfg = Config(reference_material_path=Path("/nonexistent/paper_text.txt"))
    assert cfg.reference_material_path == Path("/nonexistent/paper_text.txt")


def test_reference_path_is_coerced_to_path():
    with tempfile.NamedTemporaryFile(suffix=".txt") as f:
        cfg = Config(reference_material_path=f.name)
        assert isinstance(cfg.reference_material_path, Path)


def test_orchestrator_tolerates_missing_reference(tmp_path):
    """A wrong --reference must warn, not crash a running pipeline."""
    from autoresearch.agents.coordinator import WorkflowOrchestrator

    cfg = Config(
        workspace_dir=tmp_path / "projects",
        reference_material_path=tmp_path / "absent.txt",
    )
    orch = WorkflowOrchestrator.__new__(WorkflowOrchestrator)
    orch.config = cfg
    assert orch._load_reference_material() == ""


def test_orchestrator_reads_existing_reference(tmp_path):
    from autoresearch.agents.coordinator import WorkflowOrchestrator

    ref = tmp_path / "paper.txt"
    ref.write_text("LLM-Generated Invariants for Bounded Model Checking", encoding="utf-8")
    cfg = Config(workspace_dir=tmp_path / "projects", reference_material_path=ref)
    orch = WorkflowOrchestrator.__new__(WorkflowOrchestrator)
    orch.config = cfg
    assert "Bounded Model Checking" in orch._load_reference_material()


def test_paper_pipeline_seeds_the_real_paper():
    """run_paper_pipeline.py must point at a reference file that actually exists."""
    repo = Path(__file__).resolve().parent.parent
    src = (repo / "run_paper_pipeline.py").read_text(encoding="utf-8")
    assert "reference_material_path" in src, "reproduction script must seed the paper"
    assert (repo / "paper_text.txt").exists(), "seeded reference file must exist"
