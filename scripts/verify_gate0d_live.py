#!/usr/bin/env python3

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REPORT = (
    ROOT
    / "evidence"
    / "gates"
    / "gate0"
    / "model_live_qualification.json"
)
SNAPSHOT = (
    ROOT
    / "evidence"
    / "gates"
    / "gate0"
    / "model_targets_prequalification.json"
)
TARGETS = ROOT / "config" / "model_targets.json"
LOCK = ROOT / "config" / "research_lock.json"

EXPECTED_REPORT_SHA256 = (
    "f0b22b51684605677d4bfbfa4b187227"
    "c67093fc4c79792412797e28cb30f5c4"
)
EXPECTED_SNAPSHOT_SHA256 = (
    "d8d048bba349e45a3c2267567c37a3d"
    "771011d50ceac885fb8a953149a5cc401"
)

def require(condition, reason):
    if not condition:
        print("GATE0D2_LIVE_MODEL_FREEZE=FAIL")
        print(f"REASON={reason}")
        raise SystemExit(1)

for path in [REPORT, SNAPSHOT, TARGETS, LOCK]:
    require(path.is_file(), f"missing file: {path.name}")

report_bytes = REPORT.read_bytes()
snapshot_bytes = SNAPSHOT.read_bytes()

require(
    hashlib.sha256(report_bytes).hexdigest()
    == EXPECTED_REPORT_SHA256,
    "live report SHA mismatch"
)
require(
    hashlib.sha256(snapshot_bytes).hexdigest()
    == EXPECTED_SNAPSHOT_SHA256,
    "prequalification target snapshot SHA mismatch"
)

report = json.loads(report_bytes)
snapshot = json.loads(snapshot_bytes)
targets = json.loads(TARGETS.read_text(encoding="utf-8"))
lock = json.loads(LOCK.read_text(encoding="utf-8"))

require(report["schema_version"] == "1.1.0", "report schema")
require(report["status"] == "PASS", "report status")
require(
    report["model_target_lock_sha256"]
    == EXPECTED_SNAPSHOT_SHA256,
    "report-to-snapshot binding"
)

require(
    snapshot["status"]["live_endpoint_qualification"]
    == "PENDING",
    "snapshot is not the prequalification lock"
)
require(
    targets["status"]["live_endpoint_qualification"]
    == "PASS",
    "current live status is not PASS"
)
require(
    targets["status"]["generation_authorized"] is False,
    "current targets authorize generation"
)

models = {
    item["model_id"]: item
    for item in targets["models"]
}

require(
    set(models)
    == {
        "deepseek-v4-flash",
        "gemini-3.1-flash-lite"
    },
    "current model targets"
)
require(
    all(
        model["live_qualification_status"] == "PASS"
        for model in models.values()
    ),
    "per-model live status"
)

deepseek = report["deepseek"]
gemini = report["gemini"]

require(
    deepseek["model_id"] == "deepseek-v4-flash",
    "DeepSeek model ID"
)
require(
    deepseek["response_model"] == "deepseek-v4-flash",
    "DeepSeek returned model"
)
require(
    deepseek["models_http_status"] == 200,
    "DeepSeek models HTTP status"
)
require(
    deepseek["generation_http_status"] == 200,
    "DeepSeek generation HTTP status"
)
require(
    deepseek["thinking_mode"] == "disabled",
    "DeepSeek thinking mode"
)
require(
    deepseek["probe_exact_match"] is True,
    "DeepSeek probe exact match"
)

require(
    gemini["model_id"] == "gemini-3.1-flash-lite",
    "Gemini model ID"
)
require(
    gemini["response_model_version"]
    == "gemini-3.1-flash-lite",
    "Gemini returned model version"
)
require(
    gemini["models_http_status"] == 200,
    "Gemini models HTTP status"
)
require(
    gemini["generation_http_status"] == 200,
    "Gemini generation HTTP status"
)
require(
    gemini["thinking_level"] == "MINIMAL",
    "Gemini thinking level"
)
require(
    gemini["probe_exact_match"] is True,
    "Gemini probe exact match"
)

secret_handling = report["secret_handling"]

require(secret_handling["values_stored"] is False, "secret stored")
require(secret_handling["values_printed"] is False, "secret printed")
require(secret_handling["values_hashed"] is False, "secret hashed")
require(
    secret_handling["failure_text_redacted"] is True,
    "failure redaction"
)

secret_patterns = [
    rb"sk-[A-Za-z0-9_-]{20,}",
    rb"AIza[A-Za-z0-9_-]{20,}",
    rb"AKIA[0-9A-Z]{16}",
    rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"
]

require(
    not any(
        re.search(pattern, report_bytes)
        for pattern in secret_patterns
    ),
    "secret-like value in report"
)

qualification = lock["model_qualification"]
current = lock["current_status"]

require(
    qualification["live_access_status"] == "PASS",
    "research-lock live status"
)
require(
    qualification["live_report_sha256"]
    == EXPECTED_REPORT_SHA256,
    "research-lock report SHA"
)
require(
    qualification["prequalification_targets_sha256"]
    == EXPECTED_SNAPSHOT_SHA256,
    "research-lock snapshot SHA"
)
require(
    qualification["generation_authorized"] is False,
    "research lock authorizes generation"
)
require(current["gate_0"] == "IN_PROGRESS", "Gate 0 closed early")
require(
    current["gate_0d2_live_model_access"] == "PASS",
    "Gate 0D2 current status"
)
require(
    lock["stage_policy"]["repair_implementation_allowed"]
    is False,
    "repair enabled"
)

require(report["generation_authorized"] is False, "report generation")
require(
    report["repair_implementation_allowed"] is False,
    "report repair"
)

print("GATE0D2_LIVE_MODEL_FREEZE=PASS")
print("DEEPSEEK_MODEL=deepseek-v4-flash")
print("DEEPSEEK_THINKING=DISABLED")
print("GEMINI_MODEL=gemini-3.1-flash-lite")
print("GEMINI_THINKING=MINIMAL")
print(f"REPORT_SHA256={EXPECTED_REPORT_SHA256}")
print(f"SNAPSHOT_SHA256={EXPECTED_SNAPSHOT_SHA256}")
print("GENERATION_AUTHORIZED=NO")
print("REPAIR_IMPLEMENTATION_ALLOWED=NO")
