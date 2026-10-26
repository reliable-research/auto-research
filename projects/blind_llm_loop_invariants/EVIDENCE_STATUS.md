# EVIDENCE STATUS: UNVALIDATED

**Audited**: 2026-09-15 05:35:22 by `autoresearch verify` (deterministic; no LLM involved)

> Produced before the integrity layer existed. The pipeline had no tool execution of any kind, so no number in `05_T5_UNIFIED_RESEARCH_DRAFT.md` was measured. **Do not cite any figure from this workspace.** The method narrative and problem framing may still be useful; the evidence layer is not.

**Artifact citations**: 22 cited, **22 resolve to nothing** (100%).

## 5 machine-verified violations

| Stage | Check | Card | Problem |
| --- | --- | --- | --- |
| S6 | `ARTIFACT_MISSING` | S6-C1 | 16 file path(s) are cited as raw evidence but do not exist on disk. An evidence citation that cannot be opened is not evidence. |
| S6 | `GIT_SHA_UNRESOLVABLE` | S6-C1 | A commit hash is presented as provenance but does not resolve in this repository (or the workspace is not a git repository). |
| S7 | `COHORT_DRIFT` | S8-C3 | The evaluation cohort changed from N=30 (S6) to N=60 (S7) with no recorded protocol amendment. |
| S8 | `ARTIFACT_MISSING` | S6-C1 | 6 file path(s) are cited as raw evidence but do not exist on disk. An evidence citation that cannot be opened is not evidence. |
| S8 | `COHORT_DRIFT` | S8-C3 | The evaluation cohort changed from N=30 (S6) to N=133 (S8) with no recorded protocol amendment. |

## Registered cohort per stage

| Stage | Primary N | Timeouts (s) | Quantitative claims |
| --- | --- | --- | --- |
| S1 | 20 | - | 12 |
| S2 | - | - | 1 |
| S3 | 3 | - | 4 |
| S4 | - | [5.0] | 1 |
| S5 | 30 | [30.0] | 4 |
| S6 | 30 | - | 33 |
| S7 | 60 | [120.0] | 67 |
| S8 | 133 | [3.4, 60.0, 180.0] | 53 |

## To make this project citable

1. `autoresearch rollback <project> S5 --reason "protocol never executed"`
2. Write `protocol.json`, then `autoresearch measure <project>`.
3. Re-run S6-S8 with `--evidence-mode MEASURED`.
4. Confirm `autoresearch verify <project>` reports 0 violations.
