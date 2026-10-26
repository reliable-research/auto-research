# EVIDENCE STATUS: UNVALIDATED

**Audited**: 2026-09-15 05:35:22 by `autoresearch verify` (deterministic; no LLM involved)

> Produced before the integrity layer existed. The pipeline had no tool execution of any kind, so no number in `05_T5_UNIFIED_RESEARCH_DRAFT.md` was measured. **Do not cite any figure from this workspace.** The method narrative and problem framing may still be useful; the evidence layer is not.

**Artifact citations**: 69 cited, **69 resolve to nothing** (100%).

## 8 machine-verified violations

| Stage | Check | Card | Problem |
| --- | --- | --- | --- |
| S6 | `ARTIFACT_MISSING` | S6-C1 | 35 file path(s) are cited as raw evidence but do not exist on disk. An evidence citation that cannot be opened is not evidence. |
| S6 | `GIT_SHA_UNRESOLVABLE` | S6-C1 | A commit hash is presented as provenance but does not resolve in this repository (or the workspace is not a git repository). |
| S6 | `PREREGISTRATION_DRIFT` | S6-C2 | The executed protocol departs from the contract frozen in S5: cohort size: frozen N=9, executed N=10; timeout: frozen [120.0], executed [60.0] |
| S7 | `COHORT_DRIFT` | S8-C3 | The evaluation cohort changed from N=10 (S6) to N=80 (S7) with no recorded protocol amendment. |
| S7 | `ENVIRONMENT_DRIFT` | S8-C3 | The per-task time budget differs from the one used in S6 with no stated justification. |
| S8 | `ARTIFACT_MISSING` | S6-C1 | 9 file path(s) are cited as raw evidence but do not exist on disk. An evidence citation that cannot be opened is not evidence. |
| S8 | `COHORT_DRIFT` | S8-C3 | The evaluation cohort changed from N=10 (S6) to N=120 (S8) with no recorded protocol amendment. |
| S8 | `ENVIRONMENT_DRIFT` | S8-C3 | The per-task time budget differs from the one used in S6 with no stated justification. |

## Registered cohort per stage

| Stage | Primary N | Timeouts (s) | Quantitative claims |
| --- | --- | --- | --- |
| S1 | 10 | - | 2 |
| S2 | - | - | 1 |
| S3 | 50 | - | 0 |
| S4 | - | [5.0] | 0 |
| S5 | 9 | [120.0] | 0 |
| S6 | 10 | [60.0] | 4 |
| S7 | 80 | [18.9, 300.0] | 77 |
| S8 | 120 | [1.84, 300.0] | 54 |

## To make this project citable

1. `autoresearch rollback <project> S5 --reason "protocol never executed"`
2. Write `protocol.json`, then `autoresearch measure <project>`.
3. Re-run S6-S8 with `--evidence-mode MEASURED`.
4. Confirm `autoresearch verify <project>` reports 0 violations.
