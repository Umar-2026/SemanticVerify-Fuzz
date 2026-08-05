#!/usr/bin/env python3

import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = (
    ROOT
    / "evidence"
    / "gates"
    / "gate0"
    / "gate0ab_checkpoint.json"
)

def require(condition, reason):
    if not condition:
        raise SystemExit(
            "GATE0AB_CHECKPOINT=FAIL\n"
            f"REASON={reason}"
        )

gate0 = subprocess.run(
    ["python3", str(ROOT / "scripts" / "verify_gate0.py")],
    text=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    check=False
)

require(gate0.returncode == 0, gate0.stdout)
require(
    "GATE0A_REPOSITORY_BOOTSTRAP=PASS" in gate0.stdout,
    "Gate 0A verifier did not pass"
)

manifest = json.loads(
    MANIFEST_PATH.read_text(encoding="utf-8")
)

require(manifest["status"] == "PASS", "manifest status")
require(
    manifest["gate_0_overall"] == "IN_PROGRESS",
    "Gate 0 must remain in progress"
)
require(
    manifest["repair_implementation_allowed"] is False,
    "repair enabled before Gate V"
)

for record in manifest["files"]:
    path = ROOT / record["path"]
    require(path.is_file(), f"missing file: {record['path']}")
    require(
        path.stat().st_size == record["size_bytes"],
        f"size mismatch: {record['path']}"
    )
    require(
        hashlib.sha256(path.read_bytes()).hexdigest()
        == record["sha256"],
        f"digest mismatch: {record['path']}"
    )

environment = json.loads(
    (
        ROOT
        / "evidence"
        / "gates"
        / "gate0"
        / "environment_qualification.json"
    ).read_text(encoding="utf-8")
)

require(environment["status"] == "PASS", "environment status")

for test_name, result in environment["tests"].items():
    require(result == "PASS", f"{test_name} did not pass")

research_lock = json.loads(
    (
        ROOT / "config" / "research_lock.json"
    ).read_text(encoding="utf-8")
)

status = research_lock["current_status"]

require(
    status["gate_0a_repository_bootstrap"] == "PASS",
    "Gate 0A status mismatch"
)
require(
    status["gate_0b_environment_qualification"] == "PASS",
    "Gate 0B status mismatch"
)
require(
    status["gate_0c_proposal_provenance"] == "PENDING",
    "proposal must still be pending"
)
require(
    status["gate_0d_model_qualification"] == "PENDING",
    "model qualification must still be pending"
)
require(
    research_lock["stage_policy"]["repair_implementation_allowed"]
    is False,
    "repair enabled"
)

name = subprocess.run(
    ["git", "-C", str(ROOT), "config", "--get", "user.name"],
    text=True,
    stdout=subprocess.PIPE,
    check=False
).stdout.strip()

email = subprocess.run(
    ["git", "-C", str(ROOT), "config", "--get", "user.email"],
    text=True,
    stdout=subprocess.PIPE,
    check=False
).stdout.strip()

require(name == "Umar-2026", "Git user.name mismatch")
require(
    email == "umar.wuhan.edu15@gmail.com",
    "Git user.email mismatch"
)

print("GATE0AB_CHECKPOINT=PASS")
print("GATE0_OVERALL=IN_PROGRESS")
print("GATE0A=PASS")
print("GATE0B=PASS")
print("GATE0C_PROPOSAL=PENDING")
print("GATE0D_MODELS=PENDING")
print("REPAIR_IMPLEMENTATION_ALLOWED=NO")
print(f"FILES_VERIFIED={len(manifest['files'])}")
print(
    "MANIFEST_SHA256="
    + hashlib.sha256(MANIFEST_PATH.read_bytes()).hexdigest()
)
