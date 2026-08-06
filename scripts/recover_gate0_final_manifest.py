#!/usr/bin/env python3
"""Recover Gate 0 final-manifest preparation after a lifecycle-guard stop.

The first preparation correctly stopped when an older Gate 0D2 verifier
rejected the legitimate IN_PROGRESS -> PASS transition.  This script changes
only affected verifier lifecycle guards, refreshes their manifest records and
the manifest hash pinned by the research lock, then reruns every Gate 0
verifier.  It performs no API calls, generation, repair, or Git commit.
"""

from __future__ import annotations

import ast
import hashlib
import json
import os
import subprocess
from pathlib import Path


ROOT = Path.cwd().resolve()
EXPECTED_HEAD = "6e0123ce9d4d8a80e7a7137613948942f6af4c93"
EXPECTED_PREPARATION_SHA256 = (
    "cccbbb556ae02c6a10b3335a3132dd1a"
    "cff5435bc5476826ee7936392eb2fc22"
)
MANIFEST_REL = "evidence/gates/gate0/gate0_final_manifest.json"
LOCK_REL = "config/research_lock.json"

EXPECTED_MODIFIED = {
    "config/research_lock.json",
    "documentation/CURRENT_STATUS.md",
    "evidence/gates/gate0/README.md",
    "scripts/verify_gate0.py",
    "scripts/verify_gate0d_live.py",
    "scripts/verify_gate0e_analysis.py",
    "scripts/verify_gate0f_generation_protocol.py",
}

EXPECTED_UNTRACKED_REQUIRED = {
    "documentation/decisions/0006-gate0-final-manifest-and-research-lock-closure.md",
    MANIFEST_REL,
    "scripts/prepare_gate0_final_manifest.py",
    "scripts/verify_gate0_final_manifest.py",
    "scripts/recover_gate0_final_manifest.py",
}


def fail(reason: str) -> None:
    print("GATE0_FINAL_MANIFEST_RECOVERY=FAIL")
    print(f"REASON={reason}")
    raise SystemExit(1)


def require(condition: bool, reason: str) -> None:
    if not condition:
        fail(reason)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        fail(f"cannot read JSON {path.relative_to(ROOT)}: {error}")


def write_json(path: Path, value: dict) -> None:
    path.write_text(
        json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def patch_gate0_lifecycle_guard(path: Path) -> bool:
    """Allow a frozen subgate verifier to run both before and after closure."""
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(path))
    matches = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not node.args:
            continue
        if not isinstance(node.func, ast.Name) or node.func.id != "require":
            continue
        condition = node.args[0]
        if not isinstance(condition, ast.Compare) or len(condition.ops) != 1:
            continue
        if not any(
            isinstance(item, ast.Constant) and item.value == "gate_0"
            for item in ast.walk(condition.left)
        ):
            continue
        comparator = condition.comparators[0]
        old_form = (
            isinstance(condition.ops[0], ast.Eq)
            and isinstance(comparator, ast.Constant)
            and comparator.value == "IN_PROGRESS"
        )
        new_form = (
            isinstance(condition.ops[0], ast.In)
            and isinstance(comparator, (ast.Set, ast.Tuple, ast.List))
            and {
                item.value
                for item in comparator.elts
                if isinstance(item, ast.Constant)
            } == {"IN_PROGRESS", "PASS"}
        )
        if old_form or new_form:
            matches.append(condition)

    require(len(matches) == 1, f"lifecycle guard count: {path.relative_to(ROOT)}")
    condition = matches[0]

    if isinstance(condition.ops[0], ast.In):
        return False

    old = ast.get_source_segment(source, condition)
    require(bool(old), f"cannot extract lifecycle guard: {path.relative_to(ROOT)}")
    require(source.count(old) == 1, f"ambiguous lifecycle source: {path.relative_to(ROOT)}")
    left = ast.unparse(condition.left)
    new = f'({left}) in {{"IN_PROGRESS", "PASS"}}'
    path.write_text(source.replace(old, new, 1), encoding="utf-8")
    return True


def run(args: list[str], *, capture: bool = False) -> subprocess.CompletedProcess:
    print("RUN=" + " ".join(args))
    result = subprocess.run(
        args,
        cwd=ROOT,
        check=False,
        text=True,
        capture_output=capture,
    )
    if not capture:
        require(result.returncode == 0, f"command failed: {' '.join(args)}")
    return result


require(ROOT.name == "semanticverify-fuzz-research", "wrong repository directory")
head = run(["git", "rev-parse", "HEAD"], capture=True)
require(head.returncode == 0, "cannot read HEAD")
require(head.stdout.strip() == EXPECTED_HEAD, "unexpected HEAD")

staged = run(["git", "diff", "--cached", "--name-only"], capture=True)
require(staged.returncode == 0, "cannot inspect index")
require(not staged.stdout.strip(), "staged changes present")

status = run(
    ["git", "status", "--porcelain", "--untracked-files=all"],
    capture=True,
)
require(status.returncode == 0, "cannot inspect worktree")
lines = status.stdout.splitlines()
modified = {line[3:] for line in lines if line.startswith(" M ")}
untracked = {line[3:] for line in lines if line.startswith("?? ")}
unexpected = [
    line
    for line in lines
    if not line.startswith(" M ") and not line.startswith("?? ")
]
require(not unexpected, f"unexpected Git states: {unexpected}")
require(modified == EXPECTED_MODIFIED, f"unexpected modified files: {sorted(modified)}")
require(
    untracked == EXPECTED_UNTRACKED_REQUIRED,
    f"unexpected untracked files: {sorted(untracked)}",
)

for secret_name in ("DEEPSEEK_API_KEY", "GEMINI_API_KEY"):
    require(not os.environ.get(secret_name), f"{secret_name} must be unset")

preparation_path = ROOT / "scripts/prepare_gate0_final_manifest.py"
require(preparation_path.is_file(), "updated preparation script missing")
require(
    digest(preparation_path) == EXPECTED_PREPARATION_SHA256,
    "updated preparation script hash mismatch",
)

manifest_path = ROOT / MANIFEST_REL
lock_path = ROOT / LOCK_REL
manifest = read_json(manifest_path)
lock = read_json(lock_path)
require(manifest["status"] == "PASS", "prepared manifest status")
require(lock["current_status"]["gate_0"] == "PASS", "prepared Gate 0 status")
require(lock["current_status"]["gate_0g_final_manifest"] == "PASS", "Gate 0G")

lifecycle_paths = [
    "scripts/verify_gate0d_live.py",
    "scripts/verify_gate0e_analysis.py",
    "scripts/verify_gate0f_generation_protocol.py",
]
patched = []
for relative in lifecycle_paths:
    path = ROOT / relative
    if patch_gate0_lifecycle_guard(path):
        patched.append(relative)

require(
    all((ROOT / relative).is_file() for relative in lifecycle_paths),
    "lifecycle verifier missing",
)

# Gate 0E verifies its own source against the mutable research-lock pin.
# Synchronize that pin after the lifecycle-only source correction.
analysis_verifier_path = ROOT / "scripts/verify_gate0e_analysis.py"
analysis_lock = lock.get("analysis_registration", {})
require(
    isinstance(analysis_lock.get("verification_script_sha256"), str),
    "analysis verifier hash pin missing",
)
analysis_lock["verification_script_sha256"] = digest(analysis_verifier_path)
if "verification_script_size_bytes" in analysis_lock:
    analysis_lock["verification_script_size_bytes"] = (
        analysis_verifier_path.stat().st_size
    )

records = manifest["immutable_inputs"]["records"]
record_by_path = {record["path"]: record for record in records}
require(len(record_by_path) == len(records), "duplicate immutable record path")

for relative in lifecycle_paths:
    if relative not in record_by_path:
        continue
    path = ROOT / relative
    record_by_path[relative]["size_bytes"] = path.stat().st_size
    record_by_path[relative]["sha256"] = digest(path)

canonical = json.dumps(
    records,
    ensure_ascii=False,
    sort_keys=True,
    separators=(",", ":"),
).encode("utf-8")
records_sha256 = hashlib.sha256(canonical).hexdigest()
manifest["immutable_inputs"]["records_sha256"] = records_sha256
write_json(manifest_path, manifest)

manifest_sha256 = digest(manifest_path)
lock["gate0_final_manifest"]["sha256"] = manifest_sha256
lock["gate0_final_manifest"]["immutable_records_sha256"] = records_sha256
write_json(lock_path, lock)

verifiers = [
    ["python3", "scripts/verify_gate0c_proposal.py"],
    ["python3", "scripts/verify_gate0d_documentation.py"],
    ["python3", "scripts/verify_gate0d_live.py"],
    ["python3", "scripts/verify_gate0e_analysis.py"],
    ["python3", "scripts/verify_gate0f_generation_protocol.py"],
    ["python3", "scripts/verify_gate0_final_manifest.py"],
    ["python3", "scripts/verify_gate0.py"],
]
for command in verifiers:
    run(command)
run(["git", "diff", "--check"])

print("GATE0_FINAL_MANIFEST_RECOVERY=PASS")
print("LIFECYCLE_PATCHED=" + ",".join(patched))
print(f"IMMUTABLE_RECORDS_SHA256={records_sha256}")
print(f"MANIFEST_SHA256={manifest_sha256}")
print(f"RESEARCH_LOCK_SHA256={digest(lock_path)}")
print("GATE0_OVERALL=PASS")
print("NEXT_GATE=GATE_1_SPECIFICATION_FOUNDATION")
print("GENERATION_AUTHORIZED=NO")
print("HELD_OUT_DRIVER_INSPECTION_ALLOWED=NO")
print("REPAIR_IMPLEMENTATION_ALLOWED=NO")
print("STATUS=")
subprocess.run(["git", "status", "--short", "--branch"], cwd=ROOT, check=False)
