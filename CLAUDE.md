# CLAUDE.md

AutoResearch Codeless (`autoresearch_codeless`) — An autonomous AI-driven academic research pipeline implementing the **Idea_to_Paper_Codeless_Workflow_v4** methodology, natively powered by **Google Antigravity (`agy`)** and **Gemini** LLMs.

---

## 1. Project Overview

This repository automates the transition from raw research idea to peer-review-ready academic paper across 8 structured stages (S1–S8) governed by 48 review cards. It uses a 3-agent check-and-balance architecture (**Builder**, **Critic**, **Controller**), persistent state management, and 6 standardized markdown deliverables (T0–T5).

- **LLM Integration**: Mappings to local Google Antigravity credentials (`~/.gemini/antigravity-cli/antigravity-oauth-token`) and the `agy` CLI (`~/.local/bin/agy`), calling models such as `gemini-3.8-flash-low`, `gemini-3.8-flash-high`, and `gemini-3.1-pro-high`.
- **Workflow Standard**: Faithfully executes `Idea_to_Paper_Codeless_Workflow_v4/` rules, decision maps, and card criteria.

---

## 2. Essential Commands

### Environment & Verification
```bash
# Editable installation
pip install -e . --no-deps --break-system-packages

# Check environment, agy binary, and OAuth credential connectivity
autoresearch doctor
# (Alternative alias: idea2paper doctor)

# Run full test suite (20 unit & integration tests)
pytest -v tests/

# Run standalone smoke test (end-to-end component verification)
python3 smoke_test.py
```

### Research CLI Operations
```bash
# List all 8 stages and 48 review cards
autoresearch stages

# Initialize a new research workspace in projects/<project_name>
autoresearch init <project_name> --topic "<idea_description>" --archetype "方法 (Method)"

# Execute a single research step (Builder -> Critic -> Controller)
autoresearch step <project_name> [--model gemini-3.8-flash-high]

# Run pipeline autonomously from a start stage until a target stage
autoresearch run <project_name> --stage S1 --until S8 [--model gemini-3.8-flash-low]

# Inspect live project state, card audit matrix, and active issues
autoresearch status <project_name>

# Trigger manual rollback to a previous root-cause stage
autoresearch rollback <project_name> --to S2 --reason "Refined formal problem scope"

# Re-run the deterministic integrity audit over an existing project (no LLM involved).
# Works on runs produced before the audit existed.
autoresearch verify <project_name> [--evidence-mode SIMULATED|MEASURED]

# Run a stage with an explicit evidence mode, and optionally seed reference material
autoresearch step <project_name> --evidence-mode MEASURED --reference paper_text.txt
```

### Pre-configured Pipeline Scripts
```bash
# 1. Paper Reproduction Pipeline (seeds the ASE 2024 paper text via --reference)
python3 run_paper_pipeline.py

# 2. Zero-Cheat Blind Pipeline (1-sentence naive input, discovering invariants from scratch)
python3 run_blind_pipeline.py

# 3. Specific Idea Pipeline (grounded research proposal without leaking paper solution tricks)
python3 run_specific_idea_pipeline.py
```

---

## 3. Repository & Code Architecture

```
auoreseaerch_codeless/
├── autoresearch/                      # Core Python Package
│   ├── config.py                      # Global configuration, model paths, defaults
│   ├── llm/                           # LLM Interface & Antigravity Mapping
│   │   ├── base.py                    # BaseLLMClient interface
│   │   ├── credentials.py             # OAuth token parser & environment exporter
│   │   ├── agy_client.py              # Subprocess client for /home/wangjian/.local/bin/agy
│   │   └── factory.py                 # Client factory
│   ├── workflow/                      # Academic Workflow Engine
│   │   ├── stages.py                  # S1-S8 stage definitions, steps, and deliverables
│   │   ├── cards.py                   # 48 review cards (S1-C1 to S8-C6) definitions
│   │   ├── state.py                   # ProjectState dataclass & JSON serialization
│   │   ├── decision_engine.py         # Controller decision logic (CONTINUE, REFINE, ROLLBACK, PAUSE)
│   │   ├── integrity.py               # Deterministic, non-LLM evidence audit (see §6)
│   │   └── templates.py               # T0-T5 markdown document manager & synchronizer
│   ├── execution/                     # Real measurement (the only source of MEASURED numbers)
│   │   └── runner.py                  # Protocol runner: artifacts, provenance, derived summaries
│   ├── agents/                        # Multi-Agent Triad
│   │   ├── builder.py                 # BuilderAgent: executes research tasks & drafts T5
│   │   ├── critic.py                  # CriticAgent: card auditor producing JSON verdicts & Issues
│   │   ├── controller.py              # ControllerAgent: transition & budget controller
│   │   └── coordinator.py             # WorkflowOrchestrator: 7-step loop runner
│   ├── cli/                           # CLI Entrypoints
│   │   └── main.py                    # argparse CLI implementation
│   └── utils/                         # Formatting & Terminal Display
│       └── logger.py                  # Rich console formatting, banners, tables
├── Idea_to_Paper_Codeless_Workflow_v4/ # Upstream specification documents & diagrams
├── projects/                          # Individual research project workspaces
│   ├── llm_bmc_without_unrolling/     # Paper reproduction project
│   ├── blind_llm_loop_invariants/     # Naive blind run project
│   └── specific_idea_llm_loop_invariants/ # Grounded specific idea project
└── tests/                             # Comprehensive test suite
```

---

## 4. Coding Standards & Conventions

1. **Python Standards**:
   - Python 3.10+ required.
   - Use strict type annotations (`typing.Dict`, `typing.List`, `typing.Optional`, `typing.Any`).
   - Use `dataclasses` with `@dataclass` for state, cards, and configuration models.
   - All filesystem operations must use `pathlib.Path`.

2. **Antigravity CLI Subprocess Invocations**:
   - The `agy` CLI binary is invoked via `subprocess.run` with `--output-format json`.
   - **Model Effort Suffixes**: Notice that model names in `agy` already incorporate effort suffixes (e.g., `gemini-3.8-flash-low`, `gemini-3.8-flash-high`). Do NOT pass `--effort high` when the model name already specifies an effort suffix.

3. **State Machine Invariants**:
   - Never skip stages: Stages strictly progress along `STAGE_ORDER` (S1 -> S2 -> ... -> S8).
   - Card audit states: `MET` (satisfied), `GAP` (missing essential evidence), `CONFLICT` (contradiction), `N/A` (not applicable).
   - Only advance with `CONTINUE` when ALL applicable cards in the current stage are `MET`.
   - On `ROLLBACK`, invalidate and clean dependent deliverables of all subsequent stages.

4. **T0–T5 Standard Documents (Single Source of Truth)**:
   - `00_T0_PROJECT_AND_STAGE_CARD.md`: Contract and stage promises.
   - `01_T1_REVIEW_AND_REFINE.md`: Audit ledger and active issue tracking.
   - `02_T2_HYPOTHESES_AND_EVIDENCE.md`: Cumulative hypothesis ledger.
   - `03_T3_POC_DECISION_CONTRACT.md`: Pre-committed PoC criteria.
   - `04_T4_ROLLBACK_AND_HANDOFF.md`: Rollback handoff protocol.
   - `05_T5_UNIFIED_RESEARCH_DRAFT.md`: The living unified paper manuscript.

---

## 5. Guidelines for AI Assistants (Claude / Antigravity)

- **Do Not Modify Upstream Specs**: Never edit files inside `Idea_to_Paper_Codeless_Workflow_v4/`. They serve as immutable reference specifications.
- **Maintain Card Integrity**: Do not invent ad-hoc review cards. All card evaluations must map to the 48 registered card IDs (`S1-C1` through `S8-C6`).
- **Ground Claims in Real Artifacts**: When running research experiments, ensure deliverables in `stage_output_S*.md` and `05_T5_UNIFIED_RESEARCH_DRAFT.md` have real mathematical formulas, valid pseudocode, and reproducible benchmark configurations.
- **Respect Anti-Leakage Rules**: In blind or zero-cheat experiments, do not inject known answers, solver flags, or specific dataset names from published reference papers into the initial problem prompts.

---

## 6. The Evidence Contract (non-negotiable)

An earlier version of this pipeline completed all 8 stages, passed all 48 review
cards, and produced a manuscript whose every number was invented: 84 cited log
files did not exist, the commit hash resolved to nothing, and the evaluation
cohort silently changed from N=40 (S6) to N=240 (S7) to N=120 (S8). The Critic
passed it because it is a language model auditing a language model, and it was
shown only the current stage's text. Two mechanisms now prevent a repeat.

### 6.1 Evidence modes

Set via `Config.evidence_mode` or `--evidence-mode`.

| Mode | Meaning | Correct output |
| :--- | :--- | :--- |
| `SIMULATED` (default) | No instrument is wired up. Asserting ANY percentage, `n/m` fraction or speedup in S6-S8 is a BLOCKING violation. | A pre-registered protocol and a frozen-design manuscript whose result slots hold `[TBD-MEASURE:<id>]`. This is a complete deliverable, not a degraded one. |
| `MEASURED` | Numbers are permitted, but every cited artifact must resolve on disk and every protocol parameter must match the frozen S5 contract. | A manuscript whose figures trace to `artifacts/poc_runs/`. |

Declared targets, thresholds and budgets may stay numeric in both modes: a
commitment is not an observation.

### 6.2 The deterministic audit (`workflow/integrity.py`)

Runs between Builder and Critic, and is re-applied by the Controller afterwards.
A card with a machine-verified finding is forced to `CONFLICT` and **cannot be
marked MET by the Critic**. Checks:

| Check | Blocks |
| :--- | :--- |
| `ARTIFACT_MISSING` | A cited log/CSV/JSON that does not exist |
| `GIT_SHA_UNRESOLVABLE` | Provenance that resolves to no commit |
| `FABRICATED_MEASUREMENT` | Any asserted result number in `SIMULATED` mode |
| `PREREGISTRATION_DRIFT` | S6 executing a protocol that differs from the frozen S5 contract |
| `COHORT_DRIFT` | S7/S8 reporting over a different N than S6 |
| `ENVIRONMENT_DRIFT` | A resource budget silently changed between stages |

### 6.3 Rules for AI assistants working on this repo

1. **Never weaken a check to make a pipeline pass.** A blocked run is the system
   working. The fix is to measure, or to switch to `SIMULATED` and emit placeholders.
2. **Never write a number you did not compute from a file on disk.** In S6-S8 the
   only legitimate sources are `artifacts/poc_runs/results.json` and the per-run JSON.
3. **`TOOL_MISSING` and `ERROR` are not negative results.** The runner keeps them
   separate from `FAIL`, and summaries report rates over both denominators, so a
   broken harness is never reported as evidence against a hypothesis.
4. **Protocol changes go through S5.** Editing a parameter in S6 to match the data
   is the exact failure the drift check exists to catch.
