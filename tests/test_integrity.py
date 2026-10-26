"""Integrity audit tests, anchored on the real fabrications found in projects/.

Each test names the concrete failure it would have blocked in the
``llm_bmc_without_unrolling`` run, so a regression here is legible as
"the harness could fabricate X again".
"""
import json
import tempfile
from pathlib import Path
from adapted_research_arch.research.integrity import audit_stage, extract_artifact_refs, extract_numeric_claims, extract_stage_evidence, summarize_for_prompt
from adapted_research_arch.research.stages import StageId

def _checks(findings):
    return {f.check for f in findings}
import unittest

class IntegrityTests(unittest.TestCase):

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.workspace = Path(self.temporary.name)

    def test_missing_artifact_is_blocked(self):
        workspace = self.workspace
        'The real S6 cited 40 logs under artifacts/poc_runs/. None existed.'
        text = '| R-001 | `loop-lit/gj2007.c` | PASS | `artifacts/poc_runs/R-001_gj2007.log` |\n| R-002 | `loop-lit/hhk2008.c` | PASS | `artifacts/poc_runs/R-002_hhk2008.log` |\n'
        findings = audit_stage(StageId.S6, text, workspace, {}, evidence_mode='MEASURED')
        assert 'ARTIFACT_MISSING' in _checks(findings)
        assert findings[0].severity == 'BLOCKING'
        assert findings[0].card_id == 'S6-C1'

    def test_existing_artifact_passes(self):
        workspace = self.workspace
        (workspace / 'artifacts' / 'poc_runs').mkdir(parents=True)
        (workspace / 'artifacts' / 'poc_runs' / 'R-001.log').write_text('UNSAT\n')
        text = '| R-001 | PASS | `artifacts/poc_runs/R-001.log` |'
        findings = audit_stage(StageId.S6, text, workspace, {}, evidence_mode='MEASURED')
        assert 'ARTIFACT_MISSING' not in _checks(findings)

    def test_stdout_style_extensions_are_checked(self):
        workspace = self.workspace
        'A cited .out/.err/.jsonl slipped through: it was not in the extension list.'
        for ext in ('out', 'err', 'jsonl', 'dat', 'trace'):
            findings = audit_stage(StageId.S6, f'原始输出见 `artifacts/poc_runs/R-001.{ext}`', workspace, {}, evidence_mode='MEASURED')
            assert 'ARTIFACT_MISSING' in _checks(findings), f'.{ext} citation must be checked'

    def test_no_slash_identifiers_are_not_artifact_citations(self):
        workspace = self.workspace
        for token in ['v5.95.0', '4.12.2', 'Vampire4.8', 'z3.Solver', 'Config.evidence_mode']:
            with self.subTest(token=token):
                'Fail-closed path detection must not read a method section as a citation.\n\n    Without a directory component, a version string or attribute reference is\n    path-shaped but names no file. Flagging them would block legitimate drafts,\n    and an integrity check that cries wolf gets switched off.\n    '
                findings = audit_stage(StageId.S6, f'实现细节参见 `{token}`。', workspace, {}, evidence_mode='MEASURED')
                assert 'ARTIFACT_MISSING' not in _checks(findings)

    def test_real_filenames_are_still_caught(self):
        workspace = self.workspace
        for token in ['two_indices.c', 'bm08.log', 'requirements-freeze.txt', 'data/v1.0/out.csv', 'benchmarks/set.tar.gz']:
            with self.subTest(token=token):
                'The tightening must not reopen the hole it was narrowing.'
                findings = audit_stage(StageId.S6, f'原始证据见 `{token}`。', workspace, {}, evidence_mode='MEASURED')
                assert 'ARTIFACT_MISSING' in _checks(findings)

    def test_file_url_citation_is_checked(self):
        workspace = self.workspace
        'The specific_idea run cited file:///...antigravity-cli/scratch/.../bm04.log.'
        text = '详见 [日志](file:///nonexistent/scratch/poc_logs/bm04.log)'
        findings = audit_stage(StageId.S6, text, workspace, {}, evidence_mode='MEASURED')
        assert 'ARTIFACT_MISSING' in _checks(findings)

    def test_planned_artifacts_are_exempt(self):
        workspace = self.workspace
        text = '运行后将生成 `artifacts/poc_runs/run.log`，计划由 S6 执行填充。'
        findings = audit_stage(StageId.S6, text, workspace, {}, evidence_mode='MEASURED')
        assert 'ARTIFACT_MISSING' not in _checks(findings)

    def test_design_stages_are_not_artifact_audited(self):
        workspace = self.workspace
        text = '协议产物写入 `artifacts/poc_runs/planned.log`'
        assert audit_stage(StageId.S4, text, workspace, {}, evidence_mode='MEASURED') == []

    def test_fake_git_sha_is_blocked(self):
        workspace = self.workspace
        'The real S6 claimed commit a9f4c2b98e... in a directory that is not a repo.'
        text = 'Git Commit SHA: `a9f4c2b98e10d21a88c7b80a133f92d6e4086b97`'
        findings = audit_stage(StageId.S6, text, workspace, {}, evidence_mode='MEASURED')
        assert 'GIT_SHA_UNRESOLVABLE' in _checks(findings)

    def test_simulated_mode_blocks_fabricated_numbers(self):
        workspace = self.workspace
        'The exact abstract sentence the old pipeline shipped.'
        text = '相较于标准 BMC 方案，本方法将平均求解超时率从 58.3%（70/120）显著压降至 5.0%（6/120），加速比中位数 31.6×。'
        findings = audit_stage(StageId.S6, text, workspace, {}, evidence_mode='SIMULATED')
        assert 'FABRICATED_MEASUREMENT' in _checks(findings)

    def test_simulated_mode_allows_tbd_placeholders(self):
        workspace = self.workspace
        text = '超时率: [TBD-MEASURE:timeout_rate_baseline] vs [TBD-MEASURE:timeout_rate_ours]，由 scripts/run_bmc.py 产出后填入。'
        findings = audit_stage(StageId.S6, text, workspace, {}, evidence_mode='SIMULATED')
        assert 'FABRICATED_MEASUREMENT' not in _checks(findings)

    def test_simulated_mode_allows_declared_thresholds(self):
        workspace = self.workspace
        'Commitments are not observations: a frozen delta may stay numeric.'
        text = '预承诺意义门槛 δ: 加速比 ≥ 2.0×，求解率提升不低于 30%。\n预算上限: 单例超时 60 秒。'
        findings = audit_stage(StageId.S6, text, workspace, {}, evidence_mode='SIMULATED')
        assert 'FABRICATED_MEASUREMENT' not in _checks(findings)

    def test_measured_mode_permits_numbers_with_real_artifacts(self):
        workspace = self.workspace
        (workspace / 'eval').mkdir()
        (workspace / 'eval' / 'results.csv').write_text('id,status\n1,PASS\n')
        text = '求解率 95.0%（114/120），原始数据见 `eval/results.csv`。'
        findings = audit_stage(StageId.S6, text, workspace, {}, evidence_mode='MEASURED')
        assert _checks(findings) == set()

    def test_preregistration_drift_is_blocked(self):
        workspace = self.workspace
        'S5 froze 30 eval cases at T=0.0; S6 ran 40 at T=0.2 and was passed as MET.'
        frozen = {'primary_cohort': 30, 'timeouts': [30.0], 'temperatures': [0.0], 'repeats': [3]}
        text = '本轮共评测 40 个基准用例。Temperature=0.2，单例 Timeout 60 秒。\n通过 [TBD-MEASURE:pass_rate]。'
        findings = audit_stage(StageId.S6, text, workspace, {}, frozen_protocol=frozen, evidence_mode='SIMULATED')
        assert 'PREREGISTRATION_DRIFT' in _checks(findings)
        drift = next((f for f in findings if f.check == 'PREREGISTRATION_DRIFT'))
        assert 'cohort size' in drift.actual_content
        assert 'temperature' in drift.actual_content.lower()
        assert 'repetitions' in drift.actual_content

    def test_protocol_adherence_passes(self):
        workspace = self.workspace
        frozen = {'primary_cohort': 30, 'timeouts': [60.0], 'temperatures': [0.0], 'repeats': [3]}
        text = '评测 30 个基准用例，Temperature=0.0，Timeout 60 秒，重复 3 次取中位数。'
        findings = audit_stage(StageId.S6, text, workspace, {}, frozen_protocol=frozen, evidence_mode='SIMULATED')
        assert 'PREREGISTRATION_DRIFT' not in _checks(findings)

    def test_cohort_drift_between_s6_and_s8_is_blocked(self):
        workspace = self.workspace
        'S6 ran 40, S7 claimed 240, S8 manuscript claimed 120 -- all passed S8-C3 as MET.'
        s6_text = '全局汇总 40 例：通过 30/40，超时 5/40。'
        ledger = {StageId.S6.value: extract_stage_evidence(StageId.S6, s6_text).to_dict()}
        s8_text = '在 120 个基准上，求解率 95.0%（114/120），安全证明 80/98。'
        findings = audit_stage(StageId.S8, s8_text, workspace, ledger, evidence_mode='MEASURED')
        assert 'COHORT_DRIFT' in _checks(findings)
        drift = next((f for f in findings if f.check == 'COHORT_DRIFT'))
        assert '40' in drift.actual_content and '120' in drift.actual_content

    def test_consistent_cohort_passes(self):
        workspace = self.workspace
        s6_text = '全局汇总 120 例：通过 80/120，超时 6/120。'
        ledger = {StageId.S6.value: extract_stage_evidence(StageId.S6, s6_text).to_dict()}
        s8_text = '在 120 个基准上，安全证明 80/120，超时 6/120。'
        findings = audit_stage(StageId.S8, s8_text, workspace, ledger, evidence_mode='MEASURED')
        assert 'COHORT_DRIFT' not in _checks(findings)

    def test_environment_drift_is_blocked(self):
        workspace = self.workspace
        'S6 ran at 60s, S7 silently switched to 300s while comparing baselines.'
        s6_text = '单例超时 60 秒。通过 30/40。'
        ledger = {StageId.S6.value: extract_stage_evidence(StageId.S6, s6_text).to_dict()}
        s7_text = '每题限制 300 秒。求解 30/40。'
        findings = audit_stage(StageId.S7, s7_text, workspace, ledger, evidence_mode='MEASURED')
        assert 'ENVIRONMENT_DRIFT' in _checks(findings)

    def test_extract_numeric_claims_distinguishes_kinds(self):
        claims = extract_numeric_claims('求解率 95.0%，通过 114/120，加速 31.6×。')
        kinds = {c.kind for c in claims}
        assert kinds == {'percent', 'fraction', 'speedup'}
        frac = next((c for c in claims if c.kind == 'fraction'))
        assert (frac.numerator, frac.denominator) == (114, 120)

    def test_extract_numeric_claims_ignores_dates_and_versions(self):
        claims = extract_numeric_claims('CBMC v5.95.0 于 2024 年发布，Z3 4.12.2。')
        assert claims == []

    def test_year_ranges_are_not_read_as_fractions(self):
        """"SV-COMP 2023/2024" was being registered as a cohort of 2024."""
        assert extract_numeric_claims('参考 SV-COMP 2023/2024 竞赛报告。') == []
        ev = extract_stage_evidence(StageId.S1, '参考 SV-COMP 2023/2024 竞赛报告。')
        assert ev.primary_cohort != 2024

    def test_primary_cohort_is_the_dominant_denominator(self):
        ev = extract_stage_evidence(StageId.S6, '通过 80/120，超时 6/120，缺陷 16/22。')
        assert ev.primary_cohort == 120
        assert ev.denominators == [22, 120]

    def test_extract_artifact_refs_finds_both_forms(self):
        refs = extract_artifact_refs('见 `a/b.log` 与 [x](file:///tmp/c.json)')
        assert {r for _, r in refs} == {'a/b.log', '/tmp/c.json'}

    def test_summarize_for_prompt_renders_constraints(self):
        out = summarize_for_prompt({'S6': {'primary_cohort': 120, 'denominators': [22, 120], 'timeouts': [60.0], 'claim_count': 9}}, {'primary_cohort': 120, 'timeouts': [60.0]})
        assert 'S5 Frozen Contract' in out
        assert 'N=120' in out
        assert '硬约束' in out

    def test_summarize_for_prompt_handles_empty(self):
        assert '尚无已登记' in summarize_for_prompt({}, None)

    def test_finding_serializes_as_issue(self):
        workspace = self.workspace
        text = '求解率 95.0%（114/120）。'
        finding = audit_stage(StageId.S6, text, workspace, {}, evidence_mode='SIMULATED')[0]
        issue = finding.to_issue()
        for key in ('issue_id', 'card_id', 'severity', 'location', 'problem', 'owner_stage', 'minimal_fix', 'acceptance_criteria'):
            assert issue[key], f'{key} must be populated for the decision engine'
        assert issue['machine_verified'] is True
        json.dumps(issue, ensure_ascii=False)

    def test_pathshaped_citation_is_checked_whatever_its_extension(self):
        workspace = self.workspace
        for cited in ['benchmarks/svcomp_selected_120.manifest', 'benchmarks/loop_invariants.tar.gz', 'artifacts/poc_runs/', 'results/', 'experiments/poc/runs/run_20260914/traces/m1_smt2/', 'logs/m1_traces/c2i_12_trace.log#L18-L92']:
            with self.subTest(cited=cited):
                'All of these appear in the real drafts and pointed at nothing.'
                findings = audit_stage(StageId.S6, f'原始证据见 `{cited}`。', workspace, {}, evidence_mode='MEASURED')
                assert 'ARTIFACT_MISSING' in _checks(findings), f'{cited} slipped through'

    def test_non_path_tokens_are_not_flagged(self):
        workspace = self.workspace
        for token in ['Qwen/Qwen2.5-Coder-32B-Instruct', 'N/A', '.jsonl', '.trace', 'python3 run.py --spec a.c']:
            with self.subTest(token=token):
                findings = audit_stage(StageId.S6, f'配置: `{token}`。通过 [TBD-MEASURE:x]。', workspace, {}, evidence_mode='MEASURED')
                assert 'ARTIFACT_MISSING' not in _checks(findings), f'{token} falsely flagged'

    def test_existing_directory_citation_passes(self):
        workspace = self.workspace
        (workspace / 'artifacts' / 'poc_runs').mkdir(parents=True)
        findings = audit_stage(StageId.S6, '日志目录 `artifacts/poc_runs/`。', workspace, {}, evidence_mode='MEASURED')
        assert 'ARTIFACT_MISSING' not in _checks(findings)

    def test_the_two_modes_agree_on_protocol_invariants(self):
        workspace = self.workspace
        'Drift checks are the pre-register/verify core and must not depend on mode.\n\n    Provenance vs fabrication checks legitimately differ between modes; cohort and\n    environment drift must fire identically, or the two sides disagree on whether\n    a pre-registration was honoured.\n    '
        s6 = '全局汇总 40 例：通过 30/40。单例超时 60 秒。'
        ledger = {StageId.S6.value: extract_stage_evidence(StageId.S6, s6).to_dict()}
        s8 = '在 120 个基准上，安全证明 80/120。每题限制 300 秒。'
        invariants = {'COHORT_DRIFT', 'ENVIRONMENT_DRIFT'}
        measured = _checks(audit_stage(StageId.S8, s8, workspace, ledger, evidence_mode='MEASURED'))
        simulated = _checks(audit_stage(StageId.S8, s8, workspace, ledger, evidence_mode='SIMULATED'))
        assert invariants <= measured, f'MEASURED missed {invariants - measured}'
        assert invariants <= simulated, f'SIMULATED missed {invariants - simulated}'
        assert measured & invariants == simulated & invariants
