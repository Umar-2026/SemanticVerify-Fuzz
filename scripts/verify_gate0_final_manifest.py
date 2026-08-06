#!/usr/bin/env python3
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
