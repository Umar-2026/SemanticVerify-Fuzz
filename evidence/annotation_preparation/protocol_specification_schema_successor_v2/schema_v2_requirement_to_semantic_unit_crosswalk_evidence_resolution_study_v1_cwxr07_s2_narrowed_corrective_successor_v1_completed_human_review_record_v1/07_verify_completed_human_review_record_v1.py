#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import re
import sys

RECORD = Path(__file__).resolve().parent

EXPECTED = {
    "01_completed_human_review_manifest.v1.json":
        "edaf11cf9f172b5681cb70c39f300602657cb44157fc5caa637d3a755f07c8ad",
    "02_returned_human_review.EXACT_COPY.v1.md":
        "ad86241de11df01b65dd309097757e2f90c09f4ad08754dea680227fefde4da5",
    "03_decision0169.EXACT_COPY.v1.md":
        "7e8bf5908cfebf7b2f0ca37e8ae8e879277715686668b9013a00e44d5568ce64",
    "04_external_handoff_manifest.EXACT_COPY.v1.json":
        "1f533706e27c6b2ff4fbe7b410e089298422a80f5cc40a484313a067d5298c4a",
    "05_decision0170_a02_final_output.EXACT_COPY.v1.txt":
        "e808f3348602dd8411bea84368d36f7e9d6767989f7e42d84a6170b13e1d2e1c",
    "06_decision0170_a02_consumption_record.v1.json":
        "c677c4dda4adc5465d6905842d9621cf7d3f62a0891d124e8de2c28fd26e7715",
}

EXPECTED_A02_SHA = "2ca68fcecc6627f3048cb4a277e36181e2c6c5efc4655e3abe2e59dea132b03f"
EXPECTED_RETURNED_SHA = "ad86241de11df01b65dd309097757e2f90c09f4ad08754dea680227fefde4da5"


def stop(message):
    print("STOP|" + message)
    sys.exit(1)


def sha256_file(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


for name, expected in EXPECTED.items():
    path = RECORD / name
    if not path.is_file():
        stop("COMPLETED_REVIEW_FILE_MISSING|" + name)

    actual = sha256_file(path)
    if actual != expected:
        stop("COMPLETED_REVIEW_FILE_HASH_MISMATCH|" + name)


sumfile = RECORD / "08_completed_human_review_record_v1.SHA256SUMS"

if not sumfile.is_file():
    stop("COMPLETED_REVIEW_CHECKSUM_FILE_MISSING")

entries = []

for line in sumfile.read_text(encoding="utf-8").splitlines():
    if not line.strip():
        continue

    m = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)

    if not m:
        stop("COMPLETED_REVIEW_CHECKSUM_FORMAT_INVALID")

    entries.append((m.group(1), m.group(2)))

if len(entries) != 7:
    stop("COMPLETED_REVIEW_CHECKSUM_ENTRY_COUNT_INVALID")

expected_names = {
    "01_completed_human_review_manifest.v1.json",
    "02_returned_human_review.EXACT_COPY.v1.md",
    "03_decision0169.EXACT_COPY.v1.md",
    "04_external_handoff_manifest.EXACT_COPY.v1.json",
    "05_decision0170_a02_final_output.EXACT_COPY.v1.txt",
    "06_decision0170_a02_consumption_record.v1.json",
    "07_verify_completed_human_review_record_v1.py",
}

actual_names = {name for _, name in entries}

if actual_names != expected_names:
    stop("COMPLETED_REVIEW_CHECKSUM_NAME_SET_INVALID")

for expected, name in entries:
    path = RECORD / name

    if not path.is_file():
        stop("COMPLETED_REVIEW_CHECKSUM_TARGET_MISSING|" + name)

    if sha256_file(path) != expected:
        stop("COMPLETED_REVIEW_CHECKSUM_MISMATCH|" + name)


manifest = json.loads(
    (RECORD / "01_completed_human_review_manifest.v1.json")
    .read_text(encoding="utf-8")
)

if manifest.get("artifact") != "cwxr07_s2_completed_human_review_record_v1":
    stop("MANIFEST_ARTIFACT_INVALID")

if manifest.get("status") != "GENUINE_EXTERNAL_HUMAN_REVIEW_RECORDED":
    stop("MANIFEST_STATUS_INVALID")

if manifest.get("review_scope") != "CWXR07-S2_ONLY":
    stop("MANIFEST_REVIEW_SCOPE_INVALID")

if manifest.get("review_decision") != "PASS":
    stop("MANIFEST_REVIEW_DECISION_INVALID")

if manifest.get("cwxr07_s2_bounded_pass_recorded") is not True:
    stop("MANIFEST_BOUNDED_PASS_NOT_RECORDED")

if manifest.get("historical_cwxr07_s1_decision") != "REVISION_REQUIRED":
    stop("MANIFEST_HISTORICAL_S1_INVALID")

if manifest.get("historical_cwxr07_s1_modified") is not False:
    stop("MANIFEST_HISTORICAL_S1_MODIFIED")

if manifest.get("historical_cwxr07_s1_upgraded") is not False:
    stop("MANIFEST_HISTORICAL_S1_UPGRADED")

if manifest.get("study_governance_adopted") is not False:
    stop("MANIFEST_GOVERNANCE_ALREADY_ADOPTED")

if manifest.get("governance_adoption_authorized") is not False:
    stop("MANIFEST_GOVERNANCE_AUTHORIZATION_INVALID")

if manifest.get("analyzer_authorized") is not False:
    stop("MANIFEST_ANALYZER_BOUNDARY_INVALID")

if manifest.get("baseline_authorized") is not False:
    stop("MANIFEST_BASELINE_BOUNDARY_INVALID")

if manifest.get("repair_authorized") is not False:
    stop("MANIFEST_REPAIR_BOUNDARY_INVALID")


review_path = RECORD / "02_returned_human_review.EXACT_COPY.v1.md"

if sha256_file(review_path) != EXPECTED_RETURNED_SHA:
    stop("RETURNED_REVIEW_EXACT_COPY_BINDING_INVALID")

review = review_path.read_text(encoding="utf-8")

required_exact = [
    "CWXR07-S2 decision: PASS",
    "Reviewer name: Abdul Raheem Shahzad",
    "Reviewer role: Spec-Technical-Reviewer-1",
    "Reviewer confirmation/signature: ARS",
    "Review date: 25 / August / 2026",
]

for value in required_exact:
    if review.count(value) != 1:
        stop("RETURNED_REVIEW_REQUIRED_FIELD_INVALID|" + value)

att = re.search(
    r"^Reviewer attestation:[ \t]*(.+)$",
    review,
    re.MULTILINE,
)

if not att:
    stop("REVIEWER_ATTESTATION_MISSING")

if not re.search(
    r"reviewed\s+only\s+CWXR07-S2",
    att.group(1),
    re.I,
):
    stop("REVIEWER_ATTESTATION_SCOPE_INVALID")

if not re.search(
    r"CWXR07-S1\s+remains\s+REVISION_REQUIRED",
    review,
    re.I,
):
    stop("HISTORICAL_S1_BOUNDARY_NOT_PRESERVED")


consumption = json.loads(
    (RECORD / "06_decision0170_a02_consumption_record.v1.json")
    .read_text(encoding="utf-8")
)

if consumption.get("artifact") != "decision0170_a02_consumption_record_v1":
    stop("CONSUMPTION_ARTIFACT_INVALID")

if consumption.get("a02_sha256") != EXPECTED_A02_SHA:
    stop("CONSUMPTION_A02_BINDING_INVALID")

if consumption.get("execution_count_in_decision0171_transaction") != 1:
    stop("CONSUMPTION_EXECUTION_COUNT_INVALID")

if consumption.get("return_code") != 0:
    stop("CONSUMPTION_RETURN_CODE_INVALID")

if consumption.get("pass_marker_present") is not True:
    stop("CONSUMPTION_PASS_MARKER_INVALID")

if consumption.get("lifecycle_after_execution") != "PERMANENTLY_RETIRED":
    stop("CONSUMPTION_LIFECYCLE_INVALID")

if consumption.get("rerun_authorized") is not False:
    stop("CONSUMPTION_RERUN_BOUNDARY_INVALID")

if consumption.get("other_a02_executed_in_this_transaction") is not False:
    stop("CONSUMPTION_OTHER_A02_BOUNDARY_INVALID")

if consumption.get("global_no_rerun_fact_independently_certified") is not False:
    stop("CONSUMPTION_GLOBAL_CLAIM_INVALID")


a02_output = (
    RECORD /
    "05_decision0170_a02_final_output.EXACT_COPY.v1.txt"
).read_text(encoding="utf-8")

if "DECISION0170_A02_RESULT=PASS" not in a02_output.splitlines():
    stop("A02_FINAL_OUTPUT_PASS_MARKER_MISSING")


print("CWXR07_S2_COMPLETED_HUMAN_REVIEW_RECORD_V1=PASS")
print("REVIEW_SCOPE=CWXR07-S2_ONLY")
print("CWXR07_S2_DECISION=PASS")
print("GENUINE_EXTERNAL_HUMAN_REVIEW_RECORDED=YES")
print("HUMAN_REVIEW_STRUCTURALLY_COMPLETE=YES")
print("REVIEWER_NAME=Abdul Raheem Shahzad")
print("REVIEWER_ROLE=Spec-Technical-Reviewer-1")
print("REVIEWER_CONFIRMATION=ARS")
print("REVIEWER_ATTESTATION_PRESENT=YES")
print("HISTORICAL_CWXR07_S1_DECISION=REVISION_REQUIRED")
print("HISTORICAL_CWXR07_S1_MODIFIED=NO")
print("HISTORICAL_CWXR07_S1_UPGRADED=NO")
print("CWXR07_S2_BOUNDED_PASS_RECORDED=YES")
print("EXCLUDED_FACTS_INDEPENDENTLY_CERTIFIED=NO")
print("DECISION0170_A02_STATE=PERMANENTLY_RETIRED")
print("DECISION0170_A02_RERUN_AUTHORIZED=NO")
print("STUDY_GOVERNANCE_ADOPTED=NO")
print("GOVERNANCE_ADOPTION_AUTHORIZED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
print("COMPLETED_HUMAN_REVIEW_SAFE_VERIFICATION=PASS")
