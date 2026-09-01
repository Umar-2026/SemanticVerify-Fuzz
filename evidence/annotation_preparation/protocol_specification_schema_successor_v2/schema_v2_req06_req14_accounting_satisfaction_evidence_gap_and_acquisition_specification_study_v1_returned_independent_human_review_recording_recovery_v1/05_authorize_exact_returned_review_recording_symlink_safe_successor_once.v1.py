#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import re
import subprocess

REPO = Path("/openbayes/home/semanticverify-fuzz-research")

EXPECTED_PARENT = (
    "0c28264942b874570066482a986517fbf01bc338"
)

RETURNED = Path(
    "/openbayes/home/"
    "50_req06_req14_accounting_gap_study_Nadeem_"
    "independent_human_review_form.MANUAL_REVIEW_COPY.v1.md"
)

RETURNED_SHA = (
    "39155e0b54cf5372b4b289df50ba4f55730f575fe1b3a2af61b16fa498025412"
)

FAILED_OUTPUT_SHA = (
    "d853a667d047df4be9f7d4d75c2c1eb256e20730996cc8dda8263ebb7e76252b"
)

ROOT = (
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2/"
)

RECOV = (
    ROOT
    + "schema_v2_req06_req14_accounting_satisfaction_"
    + "evidence_gap_and_acquisition_specification_study_v1_"
    + "returned_independent_human_review_recording_recovery_v1/"
)

R01 = RECOV + "01_decision0208_a02_failed_consumption_record.v1.json"
R02 = RECOV + "02_decision0208_a02_failed_execution_output.EXACT_COPY.v1.txt"
R03 = RECOV + "03_symlink_safe_recording_successor_contract.v1.json"
R04 = RECOV + "04_failed_consumption_and_successor_boundary.v1.md"
R05 = (
    RECOV
    + "05_authorize_exact_returned_review_recording_"
    + "symlink_safe_successor_once.v1.py"
)
R06 = RECOV + "06_verify_failed_consumption_and_successor_authorization.v1.py"
R07 = RECOV + "07_failed_consumption_and_successor_authorization.v1.SHA256SUMS"

DEC = (
    "documentation/decisions/"
    "0210-record-failed-d0208-a02-consumption-and-authorize-"
    "symlink-safe-returned-review-recording-successor-v1.md"
)

EXPECTED_CHANGED = sorted([
    R01,
    R02,
    R03,
    R04,
    R05,
    R06,
    R07,
    DEC,
])


def stop(code, detail=""):
    print(
        "STOP|" + code
        + (("|" + detail) if detail else "")
    )
    raise SystemExit(1)


head = subprocess.check_output(
    ["git", "-C", str(REPO), "rev-parse", "HEAD"],
    text=True
).strip()

parent = subprocess.check_output(
    ["git", "-C", str(REPO), "rev-parse", "HEAD^"],
    text=True
).strip()

if parent != EXPECTED_PARENT:
    stop("D0210_PARENT_INVALID", parent)

status = subprocess.check_output(
    [
        "git", "-C", str(REPO),
        "status", "--porcelain=v1",
        "--untracked-files=all"
    ],
    text=True
)

if status.strip():
    stop("REPOSITORY_NOT_CLEAN")

changed = subprocess.check_output(
    [
        "git", "-C", str(REPO),
        "diff-tree", "--no-commit-id",
        "--name-only", "-r", "HEAD"
    ],
    text=True
).splitlines()

if sorted(changed) != EXPECTED_CHANGED:
    stop("D0210_COMMIT_SCOPE_INVALID")

for rel in (R01, R02, R03, R04, R06, R07, DEC):
    if not (REPO / rel).is_file():
        stop("RECOVERY_ARTIFACT_MISSING", rel)

failed = (REPO / R02).read_bytes()

if hashlib.sha256(failed).hexdigest() != FAILED_OUTPUT_SHA:
    stop("FAILED_OUTPUT_SHA_INVALID")

failure = json.loads(
    (REPO / R01).read_text(encoding="utf-8")
)

if failure["retired_verifier"]["execution_attempt_count"] != 1:
    stop("OLD_A02_EXECUTION_COUNT_INVALID")

if failure["retired_verifier"]["execution_result"] != "FAIL":
    stop("OLD_A02_RESULT_INVALID")

if failure["retired_verifier"]["state"] != "PERMANENTLY_RETIRED":
    stop("OLD_A02_RETIREMENT_INVALID")

if failure["retired_verifier"]["rerun_authorized"] is not False:
    stop("OLD_A02_RERUN_BOUNDARY_INVALID")

if failure["failure_classification"]["class"] != (
    "PATH_ALIAS_CANONICALIZATION_DEFECT"
):
    stop("FAILURE_CLASS_INVALID")

contract = json.loads(
    (REPO / R03).read_text(encoding="utf-8")
)

life = contract["one_time_successor_lifecycle"]

if life["authorized_execution_count"] != 1:
    stop("SUCCESSOR_EXECUTION_COUNT_INVALID")

if life["executed_by_decision0210"] is not False:
    stop("SUCCESSOR_PREEXECUTION_STATE_INVALID")

if life["rerun_after_first_attempt_authorized"] is not False:
    stop("SUCCESSOR_RERUN_BOUNDARY_INVALID")

b = RETURNED.read_bytes()

if hashlib.sha256(b).hexdigest() != RETURNED_SHA:
    stop("RETURNED_REVIEW_SHA_MISMATCH")

if len(b) != 12281:
    stop("RETURNED_REVIEW_SIZE_MISMATCH")

if b.count(b"\r\n") != 140:
    stop("RETURNED_REVIEW_CRLF_MISMATCH")

text = b.decode("utf-8-sig")
text = text.replace("\r\n", "\n").replace("\r", "\n")

expected = {
    "ASER01": "REVISION_REQUIRED",
    "ASER02": "REVISION_REQUIRED",
    "ASER03": "PASS",
    "ASER04": "REVISION_REQUIRED",
    "ASER05": "PASS",
    "ASER06": "PASS",
    "ASER07": "REVISION_REQUIRED",
    "ASER08": "PASS",
    "ASER09": "PASS",
}

for item, wanted in expected.items():
    m = re.search(
        rf"^## {item}\s+—.*?"
        rf"^Review decision:\s*`(PASS|REVISION_REQUIRED)`",
        text,
        re.M | re.S
    )

    if not m:
        stop(item + "_DECISION_NOT_FOUND")

    if m.group(1) != wanted:
        stop(item + "_DECISION_INVALID")

overall = re.search(
    r"^Overall review decision:\s*"
    r"`(APPROVE_BOUNDED_EVIDENCE_GAP_AND_ACQUISITION_SPECIFICATION_STUDY|REVISION_REQUIRED)`",
    text,
    re.M
)

if not overall or overall.group(1) != "REVISION_REQUIRED":
    stop("OVERALL_REVIEW_DECISION_INVALID")

print(
    "D0210_SYMLINK_SAFE_EXACT_RETURNED_REVIEW_RECORDING_SUCCESSOR_VERIFIER=PASS"
)

print("SUCCESSOR_AUTHORIZATION_COMMIT=" + head)
print("SUCCESSOR_AUTHORIZATION_PARENT=" + parent)

print("PATH_ALIAS_DEFECT_CORRECTED=YES")
print("RETIRED_D0208_A02_EXECUTED_BY_SUCCESSOR=NO")

print("RETURNED_REVIEW_SHA256=" + RETURNED_SHA)
print("RETURNED_REVIEW_SIZE=12281")
print("RETURNED_REVIEW_CRLF_COUNT=140")

print("PASS_ITEMS=ASER03,ASER05,ASER06,ASER08,ASER09")
print("REVISION_REQUIRED_ITEMS=ASER01,ASER02,ASER04,ASER07")
print("OVERALL_REVIEW_DECISION=REVISION_REQUIRED")

print("EXACT_RETURNED_REVIEW_RECORDING_AUTHORIZED=YES")
print("EXACT_RETURNED_REVIEW_RECORDED_BY_THIS_VERIFIER=NO")

print("CORRECTIVE_STUDY_SUCCESSOR_AUTHORIZED=NO")
print("STUDY_GOVERNANCE_ADOPTED=NO")
print("ACCOUNTING_EVIDENCE_ACQUISITION_AUTHORIZED=NO")
print("CONCRETE_MAPPING_AUTHORIZED=NO")
print("ACCOUNTING_SATISFACTION_DETERMINATION_AUTHORIZED=NO")
print("PAIR_RECLASSIFICATION_AUTHORIZED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")

print("SUCCESSOR_EXECUTION_ATTEMPT_COUNT_FOR_THIS_RUN=1")
print("SUCCESSOR_RERUN_AUTHORIZED=NO")
