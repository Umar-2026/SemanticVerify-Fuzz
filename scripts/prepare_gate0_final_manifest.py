#!/usr/bin/env python3
"""Prepare the final Gate 0 manifest and close the research-lock gate.

Preparation only: no API calls, no primary generation, no repair work, and no
Git commit.  Gate 0 closure does not authorize generation; Gate 1 must freeze
the prompts, scenario bindings, source locks, price evidence, and execution
authorization first.
"""

from __future__ import annotations

import datetime
import ast
import hashlib
import json
import os
import re
import stat
import subprocess
import sys
from pathlib import Path


ROOT = Path.cwd().resolve()
EXPECTED_HEAD = "6e0123ce9d4d8a80e7a7137613948942f6af4c93"
EXPECTED_TREE = "3c56b668e17c70593fd9d872d17cfa1dda25d7ae"
SELF_REL = "scripts/prepare_gate0_final_manifest.py"
MANIFEST_REL = "evidence/gates/gate0/gate0_final_manifest.json"
VERIFIER_REL = "scripts/verify_gate0_final_manifest.py"
DECISION_REL = (
    "documentation/decisions/"
    "0006-gate0-final-manifest-and-research-lock-closure.md"
)
LOCK_REL = "config/research_lock.json"
STATUS_REL = "documentation/CURRENT_STATUS.md"
README_REL = "evidence/gates/gate0/README.md"
OVERALL_VERIFIER_REL = "scripts/verify_gate0.py"
GATE0F_VERIFIER_REL = "scripts/verify_gate0f_generation_protocol.py"

EXPECTED_BASE_HASHES = {
    "config/research_lock.json": (
        "0616953ded51dcebc6e43056262bc8773"
        "1b88a6204f9fa0c669050e9e8684f07"
    ),
    "config/model_targets.json": (
        "c6171d0f398c422cfcb056ec1293a42c"
        "43de831e12320b28cb1762660fba1e38"
    ),
    "config/statistical_analysis_registration.json": (
        "c7537ce5d082de904cc7aef4d617c9ff"
        "6612b30fdb4740b0667c9eb84ca5b2d4"
    ),
    "config/generation_execution_protocol.json": (
        "aae67d6d5d6cf063f92d117efce75b51"
        "d015466decf3a17ea4822c8f2e1e38de"
    ),
    "evidence/gates/gate0/environment_qualification.json": (
        "e4dd7a2f5e6bd4ebf0105c721a740e41"
        "ca16c5d4f4dc00177e3a75fb2d7d32c6"
    ),
    "evidence/gates/gate0/gate0ab_checkpoint.json": (
        "4421a85db1c439a3bd2045ecd527be30"
        "c5734ed674e8a760117ce19c06e2c29e"
    ),
    "evidence/gates/gate0/proposal_provenance.json": (
        "0d10d9ef545413223f90ce3ea2745e42"
        "77a2026ad605713eaa8f9cf83737fea7"
    ),
    "evidence/gates/gate0/model_documentation_qualification.json": (
        "8806bf34fb395a36422fdce0c0d3a715"
        "bd465b4ce18c915a218b06e24d913a41"
    ),
    "evidence/gates/gate0/model_targets_prequalification.json": (
        "d8d048bba349e45a3c2267567c37a3d"
        "771011d50ceac885fb8a953149a5cc401"
    ),
    "evidence/gates/gate0/model_live_qualification.json": (
        "f0b22b51684605677d4bfbfa4b187227"
        "c67093fc4c79792412797e28cb30f5c4"
    ),
    "evidence/gates/gate0/statistical_analysis_registration_pre_simulation.json": (
        "8a26244a7be384ce58d1a11f736505499"
        "8fd92d4c5b496e07d7b3dfa3d2a7144"
    ),
    "evidence/gates/gate0/statistical_power_curve.json": (
        "bb746da67ccdae2eeda232aba36c53ba"
        "53ec3d7830fdd726bb4f450aa2ab9b58"
    ),
    "evidence/gates/gate0/secret_scan.json": (
        "96a24dfc31d5611345b64d731cd292e3"
        "4f677d1df189b6baaec88fe35f46e4e8"
    ),
}

IMMUTABLE_INPUTS = [
    "config/toolchain_lock.json",
    "config/model_targets.json",
    "config/statistical_analysis_registration.json",
    "config/generation_execution_protocol.json",
    "provenance/proposal/SemanticVerify-Fuzz_Verification-First_Staged-Repair_Proposal.docx",
    "evidence/gates/gate0/environment_qualification.json",
    "evidence/gates/gate0/gate0ab_checkpoint.json",
    "evidence/gates/gate0/proposal_provenance.json",
    "evidence/gates/gate0/model_documentation_qualification.json",
    "evidence/gates/gate0/model_targets_prequalification.json",
    "evidence/gates/gate0/model_live_qualification.json",
    "evidence/gates/gate0/statistical_analysis_registration_pre_simulation.json",
    "evidence/gates/gate0/statistical_power_curve.json",
    "documentation/decisions/0001-verification-first-no-backflow.md",
    "documentation/decisions/0002-model-freeze-and-amendment-rule.md",
    "documentation/decisions/0003-live-model-qualification-freeze.md",
    "documentation/decisions/0004-statistical-analysis-registration-freeze.md",
    "documentation/decisions/0005-generation-window-and-transport-retry-freeze.md",
    "scripts/verify_gate0c_proposal.py",
    "scripts/verify_gate0d_documentation.py",
    "scripts/verify_gate0d_live.py",
    "scripts/verify_gate0e_analysis.py",
    "scripts/verify_gate0f_generation_protocol.py",
]


def fail(reason: str) -> None:
    print("GATE0_FINAL_MANIFEST_PREPARATION=FAIL")
    print(f"REASON={reason}")
    raise SystemExit(1)


def require(condition: bool, reason: str) -> None:
    if not condition:
        fail(reason)


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


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        fail(f"cannot read JSON {path.relative_to(ROOT)}: {error}")


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
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


require(ROOT.name == "semanticverify-fuzz-research", "wrong repository directory")
require((ROOT / ".git").exists(), "repository metadata missing")

head_result = run(["git", "rev-parse", "HEAD"], capture=True)
tree_result = run(["git", "rev-parse", "HEAD^{tree}"], capture=True)
require(head_result.returncode == 0, "cannot resolve HEAD")
require(tree_result.returncode == 0, "cannot resolve HEAD tree")
require(head_result.stdout.strip() == EXPECTED_HEAD, "unexpected HEAD")
require(tree_result.stdout.strip() == EXPECTED_TREE, "unexpected HEAD tree")

status_result = run(
    ["git", "status", "--porcelain", "--untracked-files=all"],
    capture=True,
)
require(status_result.returncode == 0, "cannot inspect worktree")
status_lines = [line for line in status_result.stdout.splitlines() if line]
require(
    status_lines in ([], [f"?? {SELF_REL}"]),
    f"unexpected pre-existing changes: {status_lines}",
)

for secret_name in ("DEEPSEEK_API_KEY", "GEMINI_API_KEY"):
    require(not os.environ.get(secret_name), f"{secret_name} must be unset")

for relative, expected in EXPECTED_BASE_HASHES.items():
    path = ROOT / relative
    require(path.is_file(), f"missing baseline file: {relative}")
    require(digest(path) == expected, f"baseline hash mismatch: {relative}")

existing_verifiers = [
    ["python3", "scripts/verify_gate0c_proposal.py"],
    ["python3", "scripts/verify_gate0d_documentation.py"],
    ["python3", "scripts/verify_gate0d_live.py"],
    ["python3", "scripts/verify_gate0e_analysis.py"],
    ["python3", "scripts/verify_gate0f_generation_protocol.py"],
    ["python3", "scripts/verify_gate0.py"],
]
for command in existing_verifiers:
    run(command)

# Frozen subgate evidence remains unchanged.  Older subgate verifiers must
# accept the final Gate 0 lifecycle transition from IN_PROGRESS to PASS so they
# remain usable after closure.  This changes only their status guard.
lifecycle_verifiers = [
    "scripts/verify_gate0d_live.py",
    "scripts/verify_gate0e_analysis.py",
    GATE0F_VERIFIER_REL,
]
lifecycle_patched = []
for relative in lifecycle_verifiers:
    path = ROOT / relative
    if patch_gate0_lifecycle_guard(path):
        lifecycle_patched.append(relative)

require(
    "scripts/verify_gate0d_live.py" in lifecycle_patched,
    "Gate 0D2 lifecycle guard not found",
)
require(
    "scripts/verify_gate0e_analysis.py" in lifecycle_patched,
    "Gate 0E lifecycle guard not found",
)
require(
    GATE0F_VERIFIER_REL in lifecycle_patched,
    "Gate 0F lifecycle guard not found",
)

records = []
for relative in sorted(IMMUTABLE_INPUTS):
    path = ROOT / relative
    require(path.is_file(), f"immutable input missing: {relative}")
    tracked = run(["git", "ls-files", "--error-unmatch", relative], capture=True)
    require(tracked.returncode == 0, f"immutable input is not tracked: {relative}")
    records.append(
        {
            "path": relative,
            "size_bytes": path.stat().st_size,
            "sha256": digest(path),
        }
    )

records_canonical = json.dumps(
    records,
    ensure_ascii=False,
    sort_keys=True,
    separators=(",", ":"),
).encode("utf-8")
records_sha256 = hashlib.sha256(records_canonical).hexdigest()

manifest = {
    "schema_version": "1.0.0",
    "gate": "Gate 0 Final",
    "status": "PASS",
    "closed_at_utc": (
        datetime.datetime.now(datetime.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
    ),
    "base_checkpoint": {
        "commit": EXPECTED_HEAD,
        "tree": EXPECTED_TREE,
        "tracked_file_count": 46,
        "research_lock_pre_close_sha256": EXPECTED_BASE_HASHES[
            "config/research_lock.json"
        ],
        "secret_scan_pre_close_sha256": EXPECTED_BASE_HASHES[
            "evidence/gates/gate0/secret_scan.json"
        ],
    },
    "project": {
        "title": (
            "SemanticVerify-Fuzz: Resource-Centered, Path-Sensitive "
            "Verification and Constrained Repair of API-Protocol "
            "Violations in LLM-Generated Fuzz Drivers"
        ),
        "current_stage": "Stage A - verification",
        "contribution_count": 4,
        "research_question_count": 5,
        "model_count": 2,
        "library_count": 8,
        "scenario_count_per_library": 10,
        "attempts_per_model_library_scenario": 5,
        "total_new_attempts": 800,
    },
    "subgates": {
        "gate_0a_repository_bootstrap": "PASS",
        "gate_0b_environment_qualification": "PASS",
        "gate_0c_proposal_provenance": "PASS",
        "gate_0d1_model_documentation": "PASS",
        "gate_0d2_live_model_access": "PASS",
        "gate_0e_statistical_analysis_registration": "PASS",
        "gate_0f_generation_protocol": "PASS",
    },
    "immutable_inputs": {
        "record_count": len(records),
        "records_sha256": records_sha256,
        "records": records,
    },
    "mutable_coordination_files_excluded_from_input_hash_set": [
        "config/research_lock.json",
        "documentation/CURRENT_STATUS.md",
        "evidence/gates/gate0/README.md",
        "evidence/gates/gate0/secret_scan.json",
        "scripts/verify_gate0.py",
        MANIFEST_REL,
        VERIFIER_REL,
        SELF_REL,
        DECISION_REL,
    ],
    "freeze_contract": {
        "research_design_frozen": True,
        "silent_method_change_allowed": False,
        "status_metadata_may_advance_only_by_new_commits": True,
        "amendment_required_for_frozen_input_change": True,
        "fresh_start_no_prior_evidence_carryover": True,
        "verification_before_repair": True,
        "no_backflow": True,
    },
    "authorization": {
        "gate_0_closed": True,
        "primary_generation_authorized": False,
        "generation_blocked_by": [
            "Gate 1 specification foundation",
            "frozen system prompt and 80 scenario bindings",
            "eight library source/build locks",
            "provider price-sheet snapshots",
            "committed execution authorization",
        ],
        "held_out_driver_inspection_allowed": False,
        "repair_implementation_allowed": False,
        "repair_activation_gate": "Gate V",
    },
    "next_gate": {
        "id": "Gate 1",
        "name": "specification foundation",
        "status": "NOT_STARTED",
    },
    "secret_policy": {
        "final_commit_secret_scan_required": True,
        "secret_values_stored_printed_or_hashed": False,
    },
}

manifest_path = ROOT / MANIFEST_REL
require(not manifest_path.exists(), f"refusing to overwrite {MANIFEST_REL}")
write_json(manifest_path, manifest)
manifest_sha256 = digest(manifest_path)

verifier_source = r'''#!/usr/bin/env python3
import hashlib
import json
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "evidence/gates/gate0/gate0_final_manifest.json"
LOCK = ROOT / "config/research_lock.json"
SECRET_REPORT = ROOT / "evidence/gates/gate0/secret_scan.json"

def require(condition, reason):
    if not condition:
        print("GATE0_FINAL_MANIFEST=FAIL")
        print(f"REASON={reason}")
        raise SystemExit(1)

manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
lock = json.loads(LOCK.read_text(encoding="utf-8"))
secret_report = json.loads(SECRET_REPORT.read_text(encoding="utf-8"))

require(manifest["gate"] == "Gate 0 Final", "gate identity")
require(manifest["status"] == "PASS", "manifest status")
require(manifest["project"]["contribution_count"] == 4, "contribution count")
require(manifest["project"]["research_question_count"] == 5, "RQ count")
require(manifest["project"]["total_new_attempts"] == 800, "attempt count")

base = manifest["base_checkpoint"]
ancestor = subprocess.run(
    ["git", "merge-base", "--is-ancestor", base["commit"], "HEAD"],
    cwd=ROOT,
    check=False,
)
require(ancestor.returncode == 0, "base commit is not an ancestor of HEAD")

records = manifest["immutable_inputs"]["records"]
require(
    len(records) == manifest["immutable_inputs"]["record_count"],
    "record count",
)

canonical = json.dumps(
    records,
    ensure_ascii=False,
    sort_keys=True,
    separators=(",", ":"),
).encode("utf-8")
require(
    hashlib.sha256(canonical).hexdigest()
    == manifest["immutable_inputs"]["records_sha256"],
    "record-set digest",
)

for record in records:
    path = ROOT / record["path"]
    require(path.is_file(), f"missing immutable input: {record['path']}")
    require(path.stat().st_size == record["size_bytes"], f"size: {record['path']}")
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    require(actual == record["sha256"], f"SHA-256: {record['path']}")

require(all(value == "PASS" for value in manifest["subgates"].values()), "subgate")
freeze = manifest["freeze_contract"]
require(freeze["research_design_frozen"] is True, "research freeze")
require(freeze["silent_method_change_allowed"] is False, "silent change")
require(freeze["verification_before_repair"] is True, "stage order")
require(freeze["no_backflow"] is True, "no-backflow")

authorization = manifest["authorization"]
require(authorization["gate_0_closed"] is True, "Gate 0 closure")
require(authorization["primary_generation_authorized"] is False, "generation")
require(authorization["held_out_driver_inspection_allowed"] is False, "held-out")
require(authorization["repair_implementation_allowed"] is False, "repair")
require(authorization["repair_activation_gate"] == "Gate V", "repair gate")

manifest_sha = hashlib.sha256(MANIFEST.read_bytes()).hexdigest()
locked = lock["gate0_final_manifest"]
require(locked["status"] == "PASS", "research-lock manifest status")
require(locked["path"] == MANIFEST.relative_to(ROOT).as_posix(), "manifest path")
require(locked["sha256"] == manifest_sha, "manifest SHA in research lock")
require(locked["base_commit"] == base["commit"], "base commit in research lock")
require(locked["primary_generation_authorized"] is False, "lock generation")
require(locked["repair_implementation_allowed"] is False, "lock repair")

current = lock["current_status"]
require(current["gate_0"] == "PASS", "Gate 0 current status")
require(current["gate_0g_final_manifest"] == "PASS", "Gate 0G status")
require(current["gate_1"] == "NOT_STARTED", "Gate 1 started early")
require(lock["stage_policy"]["repair_implementation_allowed"] is False, "stage repair")
require(secret_report["status"] == "PASS", "secret scan")

for secret_name in ("DEEPSEEK_API_KEY", "GEMINI_API_KEY"):
    require(not os.environ.get(secret_name), f"{secret_name} present")

print("GATE0_FINAL_MANIFEST=PASS")
print("GATE0_OVERALL=PASS")
print(f"IMMUTABLE_INPUTS={len(records)}")
print(f"BASE_COMMIT={base['commit']}")
print(f"MANIFEST_SHA256={manifest_sha}")
print("NEXT_GATE=GATE_1_SPECIFICATION_FOUNDATION")
print("GENERATION_AUTHORIZED=NO")
print("HELD_OUT_DRIVER_INSPECTION_ALLOWED=NO")
print("REPAIR_IMPLEMENTATION_ALLOWED=NO")
'''

verifier_path = ROOT / VERIFIER_REL
require(not verifier_path.exists(), f"refusing to overwrite {VERIFIER_REL}")
verifier_path.write_text(verifier_source, encoding="utf-8")
verifier_path.chmod(verifier_path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

decision = """# Decision 0006: Gate 0 Final Manifest and Research-Lock Closure

- Status: Accepted
- Date: 2026-08-06
- Stage: Final Gate 0

## Decision

Gate 0A through Gate 0F have passed and the final manifest pins the immutable
proposal, toolchain, model, statistical, and generation-protocol evidence.
Gate 0 is therefore closed as PASS.

## Meaning of closure

Gate 0 closure freezes the registered research design. It does not authorize
primary model calls. Gate 1 must still freeze the protocol-source foundation,
one system prompt, all 80 library-specific scenario bindings, source/build
locks for the eight libraries, price-sheet snapshots, and a separate committed
execution authorization.

No held-out driver may be inspected before its proposal-defined release point.
No repair implementation, prompt, output, or feedback is permitted before the
irreversible Gate V verification freeze.

## Change control

Frozen design inputs cannot be silently edited. Any necessary change requires
a dated, committed amendment explaining its cause and effect. Status metadata
may advance only through new commits; earlier evidence remains preserved.
"""

decision_path = ROOT / DECISION_REL
require(not decision_path.exists(), f"refusing to overwrite {DECISION_REL}")
decision_path.parent.mkdir(parents=True, exist_ok=True)
decision_path.write_text(decision, encoding="utf-8")

lock_path = ROOT / LOCK_REL
lock = read_json(lock_path)
require("gate0_final_manifest" not in lock, "final manifest already locked")
current = lock["current_status"]
require(current["gate_0"] == "IN_PROGRESS", "Gate 0 was not in progress")
require(current["gate_0f_generation_protocol"] == "PASS", "Gate 0F not PASS")

# Gate 0E pins its verifier source hash in the mutable coordination lock.
# Refresh only that pin after the lifecycle-only verifier correction.
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

lock["gate0_final_manifest"] = {
    "status": "PASS",
    "path": MANIFEST_REL,
    "sha256": manifest_sha256,
    "base_commit": EXPECTED_HEAD,
    "base_tree": EXPECTED_TREE,
    "immutable_input_count": len(records),
    "immutable_records_sha256": records_sha256,
    "primary_generation_authorized": False,
    "held_out_driver_inspection_allowed": False,
    "repair_implementation_allowed": False,
    "next_gate": "Gate 1 - specification foundation",
}
current["gate_0"] = "PASS"
current["gate_0g_final_manifest"] = "PASS"
current["milestone"] = (
    "Gate 0 research lock complete; Gate 1 specification foundation pending"
)
write_json(lock_path, lock)

status_path = ROOT / STATUS_REL
status_text = status_path.read_text(encoding="utf-8")
status_text, count = re.subn(
    r"(?m)^- Current milestone:.*$",
    "- Current milestone: Gate 0 complete — research design frozen; "
    "Gate 1 specification foundation pending",
    status_text,
    count=1,
)
require(count == 1, "cannot update current milestone")
status_text, count = re.subn(
    r"(?m)^- Gate 0 overall: IN PROGRESS$",
    "- Gate 0 overall: PASS",
    status_text,
    count=1,
)
require(count == 1, "cannot close Gate 0 status")

if "Gate 0G final manifest" not in status_text:
    lines = status_text.splitlines()
    positions = [i for i, line in enumerate(lines) if line.startswith("- Gate 0F ")]
    require(len(positions) == 1, "Gate 0F status line mismatch")
    lines.insert(positions[0] + 1, "- Gate 0G final manifest and research-lock closure: PASS")
    status_text = "\n".join(lines) + "\n"

next_section = """## Next authorized work

1. Begin Gate 1 — specification foundation.
2. Freeze protocol-source provenance, the system prompt, and all 80 scenario bindings.
3. Freeze eight library source/build locks and provider price-sheet snapshots.
4. Create a separate committed execution authorization before any primary call.

Primary generation and held-out driver inspection remain unauthorized. Repair
implementation remains prohibited until Gate V.
"""
status_text, count = re.subn(
    r"## Remaining before Gate 0 closes\n.*\Z",
    next_section,
    status_text,
    count=1,
    flags=re.DOTALL,
)
require(count == 1, "cannot replace remaining Gate 0 section")
status_path.write_text(status_text.rstrip() + "\n", encoding="utf-8")

readme_path = ROOT / README_REL
readme_text = readme_path.read_text(encoding="utf-8")
if "Gate 0 final manifest and research-lock closure" not in readme_text:
    lines = readme_text.splitlines()
    positions = [i for i, line in enumerate(lines) if line.startswith("- Gate 0F ")]
    require(len(positions) == 1, "Gate 0F README line mismatch")
    lines.insert(positions[0] + 1, "- Gate 0 final manifest and research-lock closure")
    readme_text = "\n".join(lines) + "\n"

paragraphs = readme_text.split("\n\n")
matches = [
    i for i, paragraph in enumerate(paragraphs)
    if "Gate 0 remains IN PROGRESS." in paragraph
]
require(len(matches) == 1, "Gate 0 README closure paragraph mismatch")
paragraphs[matches[0]] = (
    "Final Gate 0 evidence:\n\n"
    "- `gate0_final_manifest.json`: immutable Gate 0 input manifest\n"
    "- Gate 0 status: PASS\n"
    "- Next gate: Gate 1 — specification foundation\n\n"
    "Gate 0 closure does not authorize primary generation or held-out driver "
    "inspection. Repair remains prohibited until Gate V."
)
readme_path.write_text("\n\n".join(paragraphs).rstrip() + "\n", encoding="utf-8")

overall_path = ROOT / OVERALL_VERIFIER_REL
overall_source = overall_path.read_text(encoding="utf-8")
old_gate_status = (
    'require(current["gate_0"] == "IN_PROGRESS", "Gate 0 closed too early")'
)
new_gate_status = (
    'require(current["gate_0"] == "PASS", "Gate 0 final status mismatch")'
)
require(overall_source.count(old_gate_status) == 1, "overall Gate 0 status marker")
overall_source = overall_source.replace(old_gate_status, new_gate_status, 1)

digest_marker = "digest = hashlib.sha256(LOCK_PATH.read_bytes()).hexdigest()"
require(overall_source.count(digest_marker) == 1, "overall digest marker")
final_checks = '''final_manifest_lock = lock["gate0_final_manifest"]
final_manifest_path = ROOT / final_manifest_lock["path"]

require(final_manifest_lock["status"] == "PASS", "final manifest lock status")
require(final_manifest_path.is_file(), "final manifest missing")
require(
    hashlib.sha256(final_manifest_path.read_bytes()).hexdigest()
    == final_manifest_lock["sha256"],
    "final manifest SHA mismatch"
)
final_manifest_document = json.loads(
    final_manifest_path.read_text(encoding="utf-8")
)
require(final_manifest_document["status"] == "PASS", "final manifest status")
require(
    final_manifest_document["authorization"]
    ["primary_generation_authorized"] is False,
    "generation enabled at Gate 0 closure"
)
require(
    final_manifest_document["authorization"]
    ["repair_implementation_allowed"] is False,
    "repair enabled at Gate 0 closure"
)
require(current["gate_0g_final_manifest"] == "PASS", "Gate 0G status")

'''
overall_source = overall_source.replace(digest_marker, final_checks + digest_marker, 1)
require(
    overall_source.count('print("GATE0_OVERALL=IN_PROGRESS")') == 1,
    "overall output marker",
)
overall_source = overall_source.replace(
    'print("GATE0_OVERALL=IN_PROGRESS")',
    'print("GATE0_OVERALL=PASS")',
    1,
)
overall_print_marker = 'print("GENERATION_PROTOCOL=PASS")'
require(overall_source.count(overall_print_marker) == 1, "overall protocol output")
overall_source = overall_source.replace(
    overall_print_marker,
    overall_print_marker
    + '\nprint("FINAL_GATE0_MANIFEST=PASS")'
    + '\nprint("GENERATION_AUTHORIZED=NO")',
    1,
)
overall_path.write_text(overall_source, encoding="utf-8")

for command in [
    ["python3", "scripts/verify_gate0c_proposal.py"],
    ["python3", "scripts/verify_gate0d_documentation.py"],
    ["python3", "scripts/verify_gate0d_live.py"],
    ["python3", "scripts/verify_gate0e_analysis.py"],
    ["python3", "scripts/verify_gate0f_generation_protocol.py"],
    ["python3", VERIFIER_REL],
    ["python3", "scripts/verify_gate0.py"],
    ["git", "diff", "--check"],
]:
    run(command)

print("GATE0_FINAL_MANIFEST_PREPARATION=PASS")
print("GATE0_OVERALL=PASS")
print(f"IMMUTABLE_INPUTS={len(records)}")
print(f"BASE_COMMIT={EXPECTED_HEAD}")
print(f"BASE_TREE={EXPECTED_TREE}")
print(f"MANIFEST_SHA256={manifest_sha256}")
print("NEXT_GATE=GATE_1_SPECIFICATION_FOUNDATION")
print("GENERATION_AUTHORIZED=NO")
print("HELD_OUT_DRIVER_INSPECTION_ALLOWED=NO")
print("REPAIR_IMPLEMENTATION_ALLOWED=NO")
print("STATUS=")
subprocess.run(["git", "status", "--short", "--branch"], cwd=ROOT, check=False)
