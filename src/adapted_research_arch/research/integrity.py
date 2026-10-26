"""Deterministic integrity audit: non-LLM checks the Critic cannot argue past.

The Critic is a language model auditing a language model. It reliably catches
*internal* incoherence but cannot catch a claim that is coherent and false --
a log file that does not exist, a cohort size that changed between stages, a
measurement that was never taken. Those checks are mechanical, so they run
mechanically here, and their findings are forced into the card matrix by the
Controller regardless of what the Critic concluded.

Every finding is emitted in the same shape as a Critic issue so the existing
decision engine consumes it unchanged.
"""

import re
import subprocess
from collections import Counter
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from .stages import StageId

# Stages whose deliverables assert measured results. S1-S5 are design stages:
# they are allowed (indeed required) to describe artifacts that do not exist yet.
EVIDENCE_STAGES = {StageId.S6, StageId.S7, StageId.S8}

# A Builder running without instruments marks every unmeasured quantity with this.
TBD_MARKER = re.compile(r"\[TBD-MEASURE:[A-Za-z0-9_.\-]+\]")

# Artifact references: fenced paths with an extension, and file:// URLs.
_ARTIFACT_EXT = (
    "log|out|err|json|jsonl|csv|tsv|txt|md|xml|html|pdf|dat|trace|"
    "smt|smt2|cnf|c|sh|py|yaml|yml|sqlite|db"
)
# Artifact citations are detected fail-CLOSED: anything path-shaped is checked,
# whatever its extension. An allowlist of extensions is the wrong shape for an
# audit -- a citation to `results/` or `run.manifest` or `bench.tar.gz` would
# pass clean while pointing at nothing, which is the exact failure this layer
# exists to stop. False positives cost a clarifying issue; false negatives cost
# a fabricated citation shipping in a manuscript.
_BACKTICKED = re.compile(r"`([^`\n]{3,200})`")
# Line anchors ("...trace.log#L18-L92") and URL fragments are not part of the path.
_FRAGMENT = re.compile(r"#.*$")
_PATH_EXTENSION = re.compile(r"\.[A-Za-z0-9]{1,8}$")

_FILE_URL = re.compile(r"file://(/[^\s)\]\"']{3,300})")

# A git commit hash presented as provenance.
_GIT_SHA = re.compile(r"(?:commit|SHA|sha|hash|Hash|哈希|提交)[^\n`]{0,40}?`?\b([0-9a-f]{7,40})\b`?")

# Quantitative result claims.
_PERCENT = re.compile(r"(?<![\d.])(\d{1,3}(?:\.\d{1,2})?)\s*%")
_FRACTION = re.compile(r"(?<![\d/.])(\d{1,6})\s*/\s*(\d{1,6})(?![\d/.])")
_SPEEDUP = re.compile(r"(?<![\d.])(\d{1,4}(?:\.\d{1,2})?)\s*(?:[xX](?![A-Za-z])|×)")

# Cohort declarations ("120 个基准用例", "133 programs", "N=40").
_COHORT_CN = re.compile(r"(\d{1,6})\s*(?:个|例|条|组|份)\s*(?:典型)?(?:基准|测试|评测|样例|用例|程序|任务|benchmark)?")
_COHORT_EN = re.compile(r"(\d{1,6})\s+(?:benchmarks?|programs?|cases?|tasks?|samples?|instances?)\b")
_COHORT_N = re.compile(r"\bN\s*(?:=|＝)\s*(\d{1,6})\b")

# Protocol parameters that a frozen S5 contract pins and S6 must honour.
_TIMEOUT = re.compile(
    r"(?:timeout|time limit|超时|时限|限时|时间限制|限制)[^\n]{0,30}?(\d{1,5}(?:\.\d+)?)\s*(?:s\b|秒|sec)",
    re.I,
)
_TEMPERATURE = re.compile(r"(?:temperature|Temp|温度)\s*(?:=|＝|:|：)?\s*(\d(?:\.\d+)?)", re.I)
_REPEATS = re.compile(r"重复\s*(\d{1,3})\s*次|(\d{1,3})\s*(?:次)?重复|repeat(?:ed)?\s*(\d{1,3})\s*times", re.I)

# A line that merely *declares a target* is not reporting a measurement.
_THRESHOLD_CONTEXT = re.compile(
    r"阈值|门槛|δ|delta|target|threshold|预算|budget|上限|限额|限制|至少|不低于|不超过|预设|预承诺|"
    r"契约|contract|冻结|frozen|判定标准|成功标准|停机|熔断|timeout|超时限|采样|seed|种子|"
    r"目标|承诺|规范|预注册|pre-?register|≥|≤|>=|<=|"
    # English threshold phrasing, which the CJK keyword list alone missed.
    r"at least|at most|no more than|no less than|minimum|maximum|required|criterion|criteria|"
    # LaTeX comparison operators: a target written as "$\ge 25/30$" is still a target.
    r"\\ge\b|\\geq\b|\\le\b|\\leq\b|\\approx\b",
    re.I,
)
# Lines describing planned/future work may reference artifacts that do not exist yet.
_PLANNED_CONTEXT = re.compile(r"计划|预计|拟|将要|将于|待生成|待执行|尚未|planned|will be|to be (?:generated|produced|run)", re.I)

# Version strings, dates and identifiers that look numeric but assert nothing.
_EXEMPT_LINE = re.compile(r"^\s*(?:\||#{1,6}\s)?\s*(?:版本|version|日期|date|引用|reference)\b", re.I)


@dataclass
class IntegrityFinding:
    """A deterministic violation, shaped like a Critic issue for the decision engine."""

    issue_id: str
    card_id: str
    severity: str
    location: str
    actual_content: str
    problem: str
    impact: str
    owner_stage: str
    minimal_fix: str
    acceptance_criteria: str
    check: str
    suggested_route: str = "REFINE_INLOOP"
    machine_verified: bool = True

    def to_issue(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class NumericClaim:
    """One quantitative assertion, with enough context to compare across stages."""

    kind: str  # "percent" | "fraction" | "speedup"
    value: float
    numerator: Optional[int]
    denominator: Optional[int]
    line_no: int
    line: str


@dataclass
class StageEvidence:
    """What a stage asserted, distilled for cross-stage comparison."""

    stage: str = ""
    cohorts: List[int] = field(default_factory=list)
    primary_cohort: Optional[int] = None
    denominators: List[int] = field(default_factory=list)
    timeouts: List[float] = field(default_factory=list)
    temperatures: List[float] = field(default_factory=list)
    repeats: List[int] = field(default_factory=list)
    artifact_refs: List[str] = field(default_factory=list)
    claim_count: int = 0
    tbd_count: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _iter_lines(text: str):
    for i, line in enumerate(text.splitlines(), start=1):
        yield i, line


def _is_exempt(line: str) -> bool:
    return bool(_THRESHOLD_CONTEXT.search(line) or _EXEMPT_LINE.match(line))


def _as_artifact_path(token: str) -> Optional[str]:
    """Return the cited path if the token names a file or directory, else None.

    Accepts anything path-shaped rather than matching an extension allowlist, and
    excludes the three things that are path-shaped but name no file: bare
    extensions being discussed as extensions (".jsonl"), identifiers that merely
    contain a slash ("Qwen/Qwen2.5-Coder-32B-Instruct", "N/A"), and shell
    fragments containing whitespace.
    """
    token = _FRAGMENT.sub("", token.strip())
    if not token or re.search(r"\s", token):
        return None
    # ".jsonl" on its own is a filename suffix under discussion, not a citation.
    if token.startswith(".") and "/" not in token:
        return None
    # A directory citation still has to resolve.
    if token.endswith("/"):
        return token if len(token) > 1 else None
    m = _PATH_EXTENSION.search(token)
    if m:
        ext = m.group(0)[1:]
        # Without a directory component, two path-shaped things name no file:
        # version strings ("v5.95.0", "4.12.2") and attribute/class references
        # ("z3.Solver", "Config.evidence_mode"). Both are common in a method
        # section. With a slash present, treat it as a path regardless.
        if "/" not in token and (ext.isdigit() or ext != ext.lower()):
            return None
        return token
    # A slash alone is not enough: model ids and "N/A" are not paths.
    return None


def extract_artifact_refs(text: str) -> List[Tuple[int, str]]:
    """Return (line_no, path) for every artifact cited as evidence."""
    refs: List[Tuple[int, str]] = []
    for line_no, line in _iter_lines(text):
        if _PLANNED_CONTEXT.search(line):
            continue
        for m in _BACKTICKED.finditer(line):
            candidate = _as_artifact_path(m.group(1))
            if candidate:
                refs.append((line_no, candidate))
        for m in _FILE_URL.finditer(line):
            refs.append((line_no, m.group(1).strip()))
    return refs


def extract_git_shas(text: str) -> List[Tuple[int, str]]:
    out: List[Tuple[int, str]] = []
    for line_no, line in _iter_lines(text):
        for m in _GIT_SHA.finditer(line):
            sha = m.group(1)
            if len(sha) >= 7 and not sha.isdigit():
                out.append((line_no, sha))
    return out


def extract_numeric_claims(text: str) -> List[NumericClaim]:
    """Extract quantitative result assertions, skipping declared targets/budgets."""
    claims: List[NumericClaim] = []
    for line_no, line in _iter_lines(text):
        if _is_exempt(line):
            continue
        stripped = TBD_MARKER.sub("", line)
        for m in _PERCENT.finditer(stripped):
            claims.append(NumericClaim("percent", float(m.group(1)), None, None, line_no, line.strip()))
        for m in _FRACTION.finditer(stripped):
            num, den = int(m.group(1)), int(m.group(2))
            # "SV-COMP 2023/2024" and "09/2024" are date ranges, not measurements.
            if 1900 <= den <= 2100:
                continue
            if den > 1 and num <= den:
                claims.append(NumericClaim("fraction", num / den, num, den, line_no, line.strip()))
        for m in _SPEEDUP.finditer(stripped):
            claims.append(NumericClaim("speedup", float(m.group(1)), None, None, line_no, line.strip()))
    return claims


def extract_stage_evidence(stage_id: StageId, text: str) -> StageEvidence:
    """Distil a stage deliverable into the facts later stages must stay consistent with."""
    ev = StageEvidence(stage=stage_id.value)

    cohorts: List[int] = []
    for pattern in (_COHORT_CN, _COHORT_EN, _COHORT_N):
        for m in pattern.finditer(text):
            val = int(m.group(1))
            if 2 <= val <= 1_000_000:
                cohorts.append(val)
    ev.cohorts = sorted(set(cohorts))

    claims = extract_numeric_claims(text)
    ev.claim_count = len(claims)
    ev.denominators = sorted({c.denominator for c in claims if c.denominator})

    # The primary cohort is the full evaluation set, not the biggest subgroup.
    # Sub-group fractions always have a denominator no larger than the total, so
    # prefer the largest denominator that the text also declares as a cohort; fall
    # back to the largest denominator, then to the largest declaration.
    corroborated = set(ev.denominators) & set(ev.cohorts)
    if corroborated:
        ev.primary_cohort = max(corroborated)
    elif ev.denominators:
        ev.primary_cohort = max(ev.denominators)
    elif cohorts:
        ev.primary_cohort = max(cohorts)

    ev.timeouts = sorted({float(m.group(1)) for m in _TIMEOUT.finditer(text)})
    ev.temperatures = sorted({float(m.group(1)) for m in _TEMPERATURE.finditer(text)})
    reps = set()
    for m in _REPEATS.finditer(text):
        for g in m.groups():
            if g:
                reps.add(int(g))
    ev.repeats = sorted(reps)
    ev.artifact_refs = [p for _, p in extract_artifact_refs(text)]
    ev.tbd_count = len(TBD_MARKER.findall(text))
    return ev


def _resolve(ref: str, workspace: Path) -> bool:
    p = Path(ref)
    if p.is_absolute():
        return p.resolve().is_relative_to(workspace.resolve()) and p.exists()
    resolved = (workspace / p).resolve()
    return resolved.is_relative_to(workspace.resolve()) and resolved.exists()


def _git_sha_exists(sha: str, workspace: Path) -> bool:
    try:
        res = subprocess.run(
            ["git", "-C", str(workspace), "cat-file", "-e", f"{sha}^{{commit}}"],
            capture_output=True,
            timeout=10,
        )
        return res.returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False


def _finding(seq: int, check: str, card_id: str, stage: StageId, **kw) -> IntegrityFinding:
    return IntegrityFinding(
        issue_id=f"INTEGRITY-{seq:02d}",
        card_id=card_id,
        severity="BLOCKING",
        owner_stage=stage.value,
        check=check,
        **kw,
    )


def audit_stage(
    stage_id: StageId,
    stage_output: str,
    workspace: Path,
    prior_evidence: Dict[str, Dict[str, Any]],
    frozen_protocol: Optional[Dict[str, Any]] = None,
    evidence_mode: str = "SIMULATED",
    known_artifacts: Optional[set[str]] = None,
) -> List[IntegrityFinding]:
    """Run every deterministic check applicable to this stage.

    ``prior_evidence`` maps stage id -> StageEvidence dict from earlier stages.
    ``frozen_protocol`` is the S5 contract that S6 execution must honour.
    """
    evidence_mode = evidence_mode.upper()
    if evidence_mode not in {"SIMULATED", "MEASURED"}:
        raise ValueError("evidence_mode must be SIMULATED or MEASURED")
    findings: List[IntegrityFinding] = []
    if stage_id not in EVIDENCE_STAGES:
        return findings

    seq = 1
    ev = extract_stage_evidence(stage_id, stage_output)
    measured = evidence_mode.upper() == "MEASURED"

    # --- Check 1: every cited artifact must resolve on disk -------------------
    # MEASURED only: see the note above about planned artifact paths.
    missing = (
        [(ln, ref) for ln, ref in extract_artifact_refs(stage_output) if ref not in (known_artifacts or set()) and not _resolve(ref, workspace)]
        if measured else []
    )
    if missing:
        shown = ", ".join(f"L{ln}:{ref}" for ln, ref in missing[:6])
        more = f" (+{len(missing) - 6} more)" if len(missing) > 6 else ""
        findings.append(_finding(
            seq, "ARTIFACT_MISSING", "S6-C1", stage_id,
            location=f"{len(missing)} artifact citation(s), e.g. {shown}{more}",
            actual_content=shown,
            problem=(
                f"{len(missing)} file path(s) are cited as raw evidence but do not exist on disk. "
                "An evidence citation that cannot be opened is not evidence."
            ),
            impact="S6-C1 requires run records to be traceable to source. Every downstream claim resting on these paths is unsupported.",
            minimal_fix=(
                "Either produce the referenced artifacts by actually running the protocol, or remove the citation "
                "and mark the corresponding quantity [TBD-MEASURE:<id>]."
            ),
            acceptance_criteria="Every path cited in an evidence table resolves under the project workspace.",
        ))
        seq += 1

    # --- Check 2: git provenance must be real --------------------------------
    bad_shas = (
        [(ln, s) for ln, s in extract_git_shas(stage_output) if not _git_sha_exists(s, workspace)]
        if measured else []
    )
    if bad_shas:
        shown = ", ".join(f"L{ln}:{s[:12]}" for ln, s in bad_shas[:4])
        findings.append(_finding(
            seq, "GIT_SHA_UNRESOLVABLE", "S6-C1", stage_id,
            location=f"commit provenance, e.g. {shown}",
            actual_content=shown,
            problem="A commit hash is presented as provenance but does not resolve in this repository (or the workspace is not a git repository).",
            impact="S6-C1 requires immutable, reproducible run provenance. An unresolvable hash makes the run unreplayable.",
            minimal_fix="Record the real commit of the code that produced the run, or drop the provenance claim and mark the run unmeasured.",
            acceptance_criteria="`git cat-file -e <sha>^{commit}` succeeds for every cited hash.",
        ))
        seq += 1

    # --- Check 3: no unmeasured numbers may be asserted as results -----------
    if evidence_mode.upper() == "SIMULATED":
        claims = extract_numeric_claims(stage_output)
        if claims:
            sample = "; ".join(f"L{c.line_no}: {c.line[:70]}" for c in claims[:4])
            findings.append(_finding(
                seq, "FABRICATED_MEASUREMENT", "S6-C2", stage_id,
                location=f"{len(claims)} quantitative result claim(s), e.g. {sample}",
                actual_content=sample,
                problem=(
                    f"evidence_mode=SIMULATED: no instrument was executed, yet {len(claims)} concrete result "
                    "quantities are asserted. Numbers that were not measured cannot be reported as results."
                ),
                impact=(
                    "Every conclusion, comparison and significance statement derived from these numbers is fabricated. "
                    "This is the failure mode that makes the whole manuscript unusable."
                ),
                minimal_fix=(
                    "Replace each measured quantity with a [TBD-MEASURE:<metric-id>] placeholder and state the "
                    "measurement procedure that will fill it. Declared thresholds and budgets may stay numeric."
                ),
                acceptance_criteria=(
                    "No percentage, fraction or speedup appears in S6-S8 outside a threshold/budget declaration "
                    "or a [TBD-MEASURE:<id>] marker."
                ),
            ))
            seq += 1

    # --- Check 4: the executed protocol must match the frozen S5 contract ----
    if stage_id == StageId.S6 and frozen_protocol:
        drift: List[str] = []
        fp_cohort = frozen_protocol.get("primary_cohort")
        if fp_cohort and ev.primary_cohort and fp_cohort != ev.primary_cohort:
            drift.append(f"cohort size: frozen N={fp_cohort}, executed N={ev.primary_cohort}")
        fp_to = frozen_protocol.get("timeouts") or []
        if fp_to and ev.timeouts and not set(fp_to) & set(ev.timeouts):
            drift.append(f"timeout: frozen {fp_to}, executed {ev.timeouts}")
        fp_temp = frozen_protocol.get("temperatures") or []
        if fp_temp and ev.temperatures and not set(fp_temp) & set(ev.temperatures):
            drift.append(f"decoding temperature: frozen {fp_temp}, executed {ev.temperatures}")
        fp_rep = frozen_protocol.get("repeats") or []
        if fp_rep and not ev.repeats:
            drift.append(f"repetitions: frozen {fp_rep}, execution reports none")
        if drift:
            findings.append(_finding(
                seq, "PREREGISTRATION_DRIFT", "S6-C2", stage_id,
                location="S6 protocol execution environment vs frozen S5 contract",
                actual_content="; ".join(drift),
                problem="The executed protocol departs from the contract frozen in S5: " + "; ".join(drift),
                impact=(
                    "S6-C2 requires adjudication strictly against pre-frozen thresholds. A protocol changed after "
                    "seeing the data cannot support any pre-registered claim."
                ),
                minimal_fix=(
                    "Re-run under the frozen parameters, or ROLLBACK to S5, amend the contract with an explicit "
                    "dated justification, and re-freeze before measuring again."
                ),
                acceptance_criteria="Every S6 protocol parameter matches the S5 contract, or a dated S5 amendment explains the change.",
            ))
            seq += 1

    # --- Check 5: cohort and environment must not drift between stages ------
    s6 = prior_evidence.get(StageId.S6.value)
    if stage_id in (StageId.S7, StageId.S8) and s6:
        s6_cohort = s6.get("primary_cohort")
        if s6_cohort and ev.primary_cohort and s6_cohort != ev.primary_cohort:
            findings.append(_finding(
                seq, "COHORT_DRIFT", "S8-C3", stage_id,
                location=f"{stage_id.value} results cohort",
                actual_content=f"S6 reported over N={s6_cohort}; {stage_id.value} reports over N={ev.primary_cohort}",
                problem=(
                    f"The evaluation cohort changed from N={s6_cohort} (S6) to N={ev.primary_cohort} "
                    f"({stage_id.value}) with no recorded protocol amendment."
                ),
                impact=(
                    "AGENT.md anti-hallucination anchor: S7/S8 numbers must trace to S6 runs. A different denominator "
                    "means these are different experiments presented as one."
                ),
                minimal_fix=(
                    "Report against the S6 cohort, or register the extension explicitly as a separate, additionally "
                    "measured cohort and keep both denominators visible in every derived statistic."
                ),
                acceptance_criteria=f"Every derived statistic names its cohort, and the S6 cohort N={s6_cohort} is reconcilable with the reported one.",
            ))
            seq += 1

        s6_to, s7_to = set(s6.get("timeouts") or []), set(ev.timeouts)
        if s6_to and s7_to and not (s6_to & s7_to):
            findings.append(_finding(
                seq, "ENVIRONMENT_DRIFT", "S8-C3", stage_id,
                location=f"{stage_id.value} resource budget",
                actual_content=f"S6 timeout {sorted(s6_to)}s vs {stage_id.value} timeout {sorted(s7_to)}s",
                problem="The per-task time budget differs from the one used in S6 with no stated justification.",
                impact="S7-C2 requires baseline comparison under equal resource budgets; changing the budget silently invalidates the comparison.",
                minimal_fix="State the budget for every reported table and justify any change, or re-report under the S6 budget.",
                acceptance_criteria="Each results table names its resource budget and any change from S6 carries a written justification.",
            ))
            seq += 1

    return findings


def summarize_for_prompt(
    prior_evidence: Dict[str, Dict[str, Any]],
    frozen_protocol: Optional[Dict[str, Any]],
) -> str:
    """Render the carried-forward facts a later stage must stay consistent with."""
    if not prior_evidence and not frozen_protocol:
        return "（尚无已登记的上游事实）"

    lines: List[str] = []
    if frozen_protocol:
        lines.append("### 冻结协议 (S5 Frozen Contract) —— 不得在未回退 S5 的情况下更改")
        for key, label in (
            ("primary_cohort", "评测集规模 N"),
            ("timeouts", "单例超时 (s)"),
            ("temperatures", "解码温度"),
            ("repeats", "重复次数"),
        ):
            val = frozen_protocol.get(key)
            if val:
                lines.append(f"- {label}: {val}")
        lines.append("")

    for stage_key in sorted(prior_evidence):
        ev = prior_evidence[stage_key]
        bits = []
        if ev.get("primary_cohort"):
            bits.append(f"主分母 N={ev['primary_cohort']}")
        if ev.get("denominators"):
            bits.append(f"已登记分母={ev['denominators']}")
        if ev.get("timeouts"):
            bits.append(f"超时={ev['timeouts']}s")
        if ev.get("temperatures"):
            bits.append(f"温度={ev['temperatures']}")
        if ev.get("claim_count") is not None:
            bits.append(f"量化断言={ev['claim_count']} 条")
        if ev.get("tbd_count"):
            bits.append(f"待测占位={ev['tbd_count']} 处")
        if bits:
            lines.append(f"- **{stage_key} 已登记事实**: " + "；".join(bits))

    lines.append("")
    lines.append(
        "**硬约束**: 本阶段引用的任何数字必须可追溯到上述已登记事实。"
        "若需改变评测集、超时或温度，必须先回退到拥有该承诺的阶段并留下书面修订，不得就地改写。"
    )
    return "\n".join(lines)
