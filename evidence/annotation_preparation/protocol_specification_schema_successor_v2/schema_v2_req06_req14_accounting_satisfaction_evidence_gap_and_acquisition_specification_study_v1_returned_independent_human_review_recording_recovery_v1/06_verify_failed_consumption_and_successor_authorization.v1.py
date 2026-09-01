#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent

R01 = ROOT / "01_decision0208_a02_failed_consumption_record.v1.json"
R02 = ROOT / "02_decision0208_a02_failed_execution_output.EXACT_COPY.v1.txt"
R03 = ROOT / "03_symlink_safe_recording_successor_contract.v1.json"
R04 = ROOT / "04_failed_consumption_and_successor_boundary.v1.md"
R05 = ROOT / "05_authorize_exact_returned_review_recording_symlink_safe_successor_once.v1.py"

FAILED_SHA = (
    "d853a667d047df4be9f7d4d75c2c1eb256e20730996cc8dda8263ebb7e76252b"
)


def stop(code):
    print("STOP|" + code)
    raise SystemExit(1)


for p in (R01, R02, R03, R04, R05):
    if not p.is_file():
        stop("RECOVERY_ARTIFACT_MISSING")

if hashlib.sha256(R02.read_bytes()).hexdigest() != FAILED_SHA:
    stop("FAILED_OUTPUT_SHA_INVALID")

record = json.loads(R01.read_text(encoding="utf-8"))

if record["retired_verifier"]["execution_attempt_count"] != 1:
    stop("OLD_A02_COUNT_INVALID")

if record["retired_verifier"]["execution_result"] != "FAIL":
    stop("OLD_A02_RESULT_INVALID")

if record["retired_verifier"]["state"] != "PERMANENTLY_RETIRED":
    stop("OLD_A02_STATE_INVALID")

if record["retired_verifier"]["rerun_authorized"] is not False:
    stop("OLD_A02_RERUN_INVALID")

if record["failure_classification"]["class"] != (
    "PATH_ALIAS_CANONICALIZATION_DEFECT"
):
    stop("FAILURE_CLASS_INVALID")

contract = json.loads(R03.read_text(encoding="utf-8"))

life = contract["one_time_successor_lifecycle"]

if life["authorized_execution_count"] != 1:
    stop("SUCCESSOR_COUNT_INVALID")

if life["executed_by_decision0210"] is not False:
    stop("SUCCESSOR_EXECUTION_STATE_INVALID")

if life["rerun_after_first_attempt_authorized"] is not False:
    stop("SUCCESSOR_RERUN_INVALID")

boundary = R04.read_text(encoding="utf-8")

for marker in (
    "`DECISION0208_A02_EXECUTION_ATTEMPT_COUNT=1`",
    "`DECISION0208_A02_RESULT=FAIL`",
    "`DECISION0208_A02_STATE=PERMANENTLY_RETIRED`",
    "`DECISION0208_A02_RERUN_AUTHORIZED=NO`",
    "`RETURNED_REVIEW_RECORDED=NO`",
):
    if marker not in boundary:
        stop("BOUNDARY_MARKER_MISSING")

print(
    "D0210_FAILED_D0208_A02_CONSUMPTION_AND_SYMLINK_SAFE_SUCCESSOR_RECORD_VERIFIER=PASS"
)

print("DECISION0208_A02_EXECUTION_ATTEMPT_COUNT=1")
print("DECISION0208_A02_RESULT=FAIL")
print("DECISION0208_A02_STATE=PERMANENTLY_RETIRED")
print("DECISION0208_A02_RERUN_AUTHORIZED=NO")

print("FAILURE_CLASS=PATH_ALIAS_CANONICALIZATION_DEFECT")

print("SYMLINK_SAFE_SUCCESSOR_AUTHORIZED=YES")
print("SYMLINK_SAFE_SUCCESSOR_EXECUTED=NO")
print("SYMLINK_SAFE_SUCCESSOR_AUTHORIZED_EXECUTION_COUNT=1")

print("RETURNED_REVIEW_RECORDED=NO")
print("CORRECTIVE_STUDY_SUCCESSOR_AUTHORIZED=NO")
print("STUDY_GOVERNANCE_ADOPTED=NO")

print("ACCOUNTING_EVIDENCE_ACQUISITION_AUTHORIZED=NO")
print("CONCRETE_MAPPING_AUTHORIZED=NO")
print("ACCOUNTING_SATISFACTION_DETERMINATION_AUTHORIZED=NO")
print("PAIR_RECLASSIFICATION_AUTHORIZED=NO")

print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
