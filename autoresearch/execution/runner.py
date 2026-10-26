"""Execute a declared protocol and write artifacts an auditor can actually open.

This is the other half of the integrity layer. ``integrity.py`` stops the Builder
from asserting numbers it never measured; this module is how numbers get measured
at all, so MEASURED mode has something honest to cite.

Three properties matter more than features here:

1. **It never invents.** A missing binary produces ``TOOL_MISSING``, not a plausible
   result. An unresolvable git HEAD produces ``None``, not a hash-shaped string.
2. **Aggregates are arithmetic, not prose.** :func:`summarize` computes every headline
   number from the run records, so S6's summary table is derived rather than written.
3. **Artifacts land where citations point.** Each run writes a real ``.log`` and
   ``.json`` under the workspace, so ``ARTIFACT_MISSING`` stops firing for honest runs.

The runner is tool-agnostic: a spec is just an argv, so the same machinery drives
CBMC, a solver, a training script, or a shell one-liner.
"""

import hashlib
import json
import platform
import shutil
import statistics
import subprocess
import sys
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence

# Terminal statuses a run may end in. TOOL_MISSING and ERROR are kept distinct
# from FAIL because "the instrument was not there" is not evidence about the
# hypothesis -- conflating them is how a broken harness reads as a negative result.
STATUS_PASS = "PASS"
STATUS_FAIL = "FAIL"
STATUS_TIMEOUT = "TIMEOUT"
STATUS_ERROR = "ERROR"
STATUS_TOOL_MISSING = "TOOL_MISSING"

# Statuses that mean the instrument did not produce a reading at all.
INVALID_STATUSES = {STATUS_ERROR, STATUS_TOOL_MISSING}


@dataclass
class RunSpec:
    """One unit of work: an argv to execute under a time limit."""

    run_id: str
    command: Sequence[str]
    label: str = ""
    group: str = "default"
    timeout_s: float = 60.0
    # Files whose content hash is recorded, so a result is tied to its exact input.
    inputs: List[str] = field(default_factory=list)
    cwd: Optional[str] = None


@dataclass
class RunRecord:
    """What actually happened, with enough provenance to replay it."""

    run_id: str
    label: str
    group: str
    command: List[str]
    timeout_s: float
    status: str
    exit_code: Optional[int]
    wall_time_s: float
    stdout_path: str
    stderr_path: str
    input_hashes: Dict[str, str]
    started_at: str
    finished_at: str
    note: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _sha256(path: Path) -> Optional[str]:
    try:
        h = hashlib.sha256()
        with path.open("rb") as fh:
            for chunk in iter(lambda: fh.read(65536), b""):
                h.update(chunk)
        return h.hexdigest()
    except OSError:
        return None


def _git_commit(workspace: Path) -> Optional[str]:
    """Return the real HEAD commit, or None. Never returns a placeholder."""
    try:
        res = subprocess.run(
            ["git", "-C", str(workspace), "rev-parse", "HEAD"],
            capture_output=True, text=True, timeout=10,
        )
        return res.stdout.strip() if res.returncode == 0 else None
    except (OSError, subprocess.SubprocessError):
        return None


def _tool_version(binary: str) -> Optional[str]:
    """Best-effort version string for a tool, or None if it cannot be determined."""
    if not shutil.which(binary):
        return None
    for flag in ("--version", "-version", "-V"):
        try:
            res = subprocess.run([binary, flag], capture_output=True, text=True, timeout=15)
            out = (res.stdout or res.stderr).strip()
            if out:
                return out.splitlines()[0][:200]
        except (OSError, subprocess.SubprocessError):
            continue
    return None


def environment_fingerprint(workspace: Path, tools: Sequence[str] = ()) -> Dict[str, Any]:
    """Record the environment as it actually is.

    Every field may legitimately be None. A None git commit is the correct answer
    for a non-repository, and is strictly better than a hash-shaped invention: the
    integrity audit flags fabricated provenance, not absent provenance.
    """
    return {
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "git_commit": _git_commit(workspace),
        "platform": platform.platform(),
        "processor": platform.processor() or None,
        "python": sys.version.split()[0],
        "tool_versions": {t: _tool_version(t) for t in tools},
    }


class ProtocolRunner:
    """Runs specs, writes artifacts, and refuses to report what it did not observe."""

    def __init__(self, workspace: Path, artifacts_subdir: str = "artifacts/poc_runs"):
        self.workspace = Path(workspace)
        self.artifacts_subdir = artifacts_subdir
        self.artifacts_dir = self.workspace / artifacts_subdir
        self.artifacts_dir.mkdir(parents=True, exist_ok=True)

    def _rel(self, path: Path) -> str:
        """Path as a citation relative to the workspace, matching what S6 will print."""
        try:
            return str(path.relative_to(self.workspace))
        except ValueError:
            return str(path)

    def run_one(
        self,
        spec: RunSpec,
        classifier: Optional[Callable[[Optional[int], str, str], str]] = None,
    ) -> RunRecord:
        """Execute one spec, always producing a record and its artifacts."""
        classify = classifier or default_classifier
        stdout_path = self.artifacts_dir / f"{spec.run_id}.log"
        stderr_path = self.artifacts_dir / f"{spec.run_id}.err.log"

        input_hashes: Dict[str, str] = {}
        for rel in spec.inputs:
            p = Path(rel)
            p = p if p.is_absolute() else self.workspace / p
            digest = _sha256(p)
            if digest:
                input_hashes[str(rel)] = digest

        argv = list(spec.command)
        started = datetime.now(timezone.utc)
        t0 = time.monotonic()

        if not argv:
            status, exit_code, out, err, note = STATUS_ERROR, None, "", "", "empty command"
        elif not shutil.which(argv[0]) and not Path(argv[0]).exists():
            # The instrument is absent. This is not a failed experiment.
            status, exit_code, out, err = STATUS_TOOL_MISSING, None, "", ""
            note = f"executable not found: {argv[0]}"
        else:
            note = ""
            try:
                proc = subprocess.run(
                    argv,
                    capture_output=True,
                    text=True,
                    timeout=spec.timeout_s,
                    cwd=spec.cwd or str(self.workspace),
                )
                out, err, exit_code = proc.stdout, proc.stderr, proc.returncode
                status = classify(exit_code, out, err)
            except subprocess.TimeoutExpired as e:
                out = e.stdout.decode() if isinstance(e.stdout, bytes) else (e.stdout or "")
                err = e.stderr.decode() if isinstance(e.stderr, bytes) else (e.stderr or "")
                status, exit_code = STATUS_TIMEOUT, None
                note = f"exceeded timeout of {spec.timeout_s}s"
            except (OSError, subprocess.SubprocessError) as e:
                out, err, exit_code, status = "", str(e), None, STATUS_ERROR
                note = f"execution error: {type(e).__name__}"

        wall = time.monotonic() - t0
        finished = datetime.now(timezone.utc)

        stdout_path.write_text(out or "", encoding="utf-8")
        stderr_path.write_text(err or "", encoding="utf-8")

        record = RunRecord(
            run_id=spec.run_id,
            label=spec.label or spec.run_id,
            group=spec.group,
            command=argv,
            timeout_s=spec.timeout_s,
            status=status,
            exit_code=exit_code,
            # Wall time is meaningless when nothing ran; do not report a duration
            # that would later be averaged into a performance claim.
            wall_time_s=round(wall, 4) if status not in INVALID_STATUSES else 0.0,
            stdout_path=self._rel(stdout_path),
            stderr_path=self._rel(stderr_path),
            input_hashes=input_hashes,
            started_at=started.isoformat(),
            finished_at=finished.isoformat(),
            note=note,
        )
        (self.artifacts_dir / f"{spec.run_id}.json").write_text(
            json.dumps(record.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8"
        )
        return record

    def run_all(
        self,
        specs: Sequence[RunSpec],
        classifier: Optional[Callable[[Optional[int], str, str], str]] = None,
        tools: Sequence[str] = (),
        progress: Optional[Callable[[RunRecord], None]] = None,
    ) -> Dict[str, Any]:
        """Execute every spec and write manifest.json + results.json.

        Returns the manifest. ``results.json`` holds the derived summary that S6
        should quote verbatim rather than restate in its own words.
        """
        records: List[RunRecord] = []
        for spec in specs:
            record = self.run_one(spec, classifier)
            records.append(record)
            if progress:
                progress(record)

        manifest = {
            "environment": environment_fingerprint(self.workspace, tools),
            "run_count": len(records),
            "artifacts_dir": self.artifacts_subdir,
            "records": [r.to_dict() for r in records],
        }
        (self.artifacts_dir / "manifest.json").write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
        )

        summary = summarize(records)
        (self.artifacts_dir / "results.json").write_text(
            json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        manifest["summary"] = summary
        return manifest


def default_classifier(exit_code: Optional[int], stdout: str, stderr: str) -> str:
    """Exit code 0 means PASS. Override for tools with richer exit conventions."""
    return STATUS_PASS if exit_code == 0 else STATUS_FAIL


def _group_stats(records: Sequence[RunRecord]) -> Dict[str, Any]:
    total = len(records)
    counts: Dict[str, int] = {}
    for r in records:
        counts[r.status] = counts.get(r.status, 0) + 1

    valid = [r for r in records if r.status not in INVALID_STATUSES]
    passed = [r for r in records if r.status == STATUS_PASS]
    times = [r.wall_time_s for r in passed]
    # Cost is observed whenever the instrument ran, not only when it returned PASS.
    # A refuted property (FAIL) and an exhausted budget (TIMEOUT) are both real
    # readings of how expensive the query was, so they belong in a cost statistic;
    # ERROR and TOOL_MISSING produced no reading and stay excluded.
    valid_times = [r.wall_time_s for r in valid]

    stats: Dict[str, Any] = {
        "n": total,
        "status_counts": counts,
        # Denominators are stated explicitly so a later stage cannot quietly swap them.
        "n_valid": len(valid),
        "n_invalid": total - len(valid),
        "pass_count": len(passed),
        "pass_rate_over_valid": round(len(passed) / len(valid), 4) if valid else None,
        "pass_rate_over_all": round(len(passed) / total, 4) if total else None,
    }
    if times:
        stats["wall_time_s"] = {
            "mean": round(statistics.fmean(times), 4),
            "median": round(statistics.median(times), 4),
            "min": round(min(times), 4),
            "max": round(max(times), 4),
        }
    else:
        stats["wall_time_s"] = None

    # Reported under its own name so no reader can mistake it for the PASS-only
    # figure above; the denominator is n_valid, stated in the same dict.
    if valid_times:
        stats["wall_time_s_over_valid"] = {
            "mean": round(statistics.fmean(valid_times), 4),
            "median": round(statistics.median(valid_times), 4),
            "min": round(min(valid_times), 4),
            "max": round(max(valid_times), 4),
        }
    else:
        stats["wall_time_s_over_valid"] = None
    return stats


def summarize(records: Sequence[RunRecord]) -> Dict[str, Any]:
    """Derive every headline figure arithmetically from the run records.

    Rates are reported over two denominators on purpose. A run that errored or
    whose tool was missing produced no reading, so folding it into a failure rate
    would report a harness problem as a scientific negative.
    """
    groups: Dict[str, List[RunRecord]] = {}
    for r in records:
        groups.setdefault(r.group, []).append(r)

    return {
        "computed_at": datetime.now(timezone.utc).isoformat(),
        "derivation": "counts and rates computed from artifacts/poc_runs/*.json; not authored",
        "overall": _group_stats(records),
        "by_group": {g: _group_stats(rs) for g, rs in sorted(groups.items())},
        "run_ids": [r.run_id for r in records],
    }


def specs_from_manifest(path: Path) -> List[RunSpec]:
    """Load run specs from a JSON manifest, so the protocol is a file, not code.

    Expected shape::

        {"defaults": {"timeout_s": 60}, "runs": [{"run_id": "R-001", "command": [...]}]}
    """
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    defaults = data.get("defaults", {})
    specs: List[RunSpec] = []
    for i, entry in enumerate(data.get("runs", []), start=1):
        merged = {**defaults, **entry}
        specs.append(
            RunSpec(
                run_id=merged.get("run_id") or f"R-{i:03d}",
                command=merged["command"],
                label=merged.get("label", ""),
                group=merged.get("group", "default"),
                timeout_s=float(merged.get("timeout_s", 60.0)),
                inputs=list(merged.get("inputs", [])),
                cwd=merged.get("cwd"),
            )
        )
    return specs
