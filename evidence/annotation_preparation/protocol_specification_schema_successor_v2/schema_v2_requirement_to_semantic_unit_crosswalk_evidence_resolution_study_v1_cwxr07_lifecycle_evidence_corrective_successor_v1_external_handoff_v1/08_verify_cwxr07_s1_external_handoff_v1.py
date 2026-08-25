#!/usr/bin/env python3

import hashlib
import json
from pathlib import Path

H = Path(__file__).resolve().parent
COPY = H / "02_review_package.EXACT_COPY"

def sha(path):
    return hashlib.sha256(
        Path(path).read_bytes()
    ).hexdigest()

def load(path):
    return json.loads(
        Path(path).read_text(encoding="utf-8")
    )

manifest = load(
    H / "01_external_handoff_manifest.v1.json"
)

assert manifest["status"] == "HANDED_OFF_AWAITING_INDEPENDENT_HUMAN_REVIEW"
assert manifest["review_scope"] == "CWXR07-S1_ONLY"

assert (
    manifest["claim_boundary"][
        "actual_external_process_execution_count_independently_proven"
    ]
    is False
)

assert (
    manifest["claim_boundary"][
        "global_no_rerun_fact_independently_proven"
    ]
    is False
)

assert (
    manifest["claim_boundary"][
        "record_assertion_promoted_to_external_execution_fact"
    ]
    is False
)

human = manifest["human_review_state"]

assert human["completed"] is False
assert human["reviewer_identity_recorded"] is False
assert human["item_decision_recorded"] is False
assert human["overall_decision_recorded"] is False

original = manifest["original_review_boundary"]

assert original["overall_decision"] == "REVISION_REQUIRED"
assert original["original_cwxr07_decision"] == "REVISION_REQUIRED"
assert original["original_review_modified"] is False
assert original["passed_items_reopened"] is False

life = manifest["decision0160_a02_lifecycle"]

assert life["executed"] is True
assert life["execution_count_in_handoff_transaction"] == 1
assert life["pass"] is True
assert life["lifecycle_after_execution"] == "PERMANENTLY_RETIRED"
assert life["rerun_authorized"] is False

src = manifest["source_review_package"]

assert (
    sha(COPY / "01_review_package_manifest.v1.json")
    == src["manifest_sha256"]
)

assert (
    sha(COPY / "06_reviewer_instructions.v1.md")
    == src["reviewer_instructions_sha256"]
)

assert (
    sha(
        COPY
        / "07_CWXR07_S1_reviewer_packet.INITIAL_BLANK.EXACT_COPY.v1.md"
    )
    == src["blank_reviewer_packet_sha256"]
)

assert (
    sha(COPY / "10_verify_cwxr07_s1_independent_human_review_package_v1.py")
    == src["repeat_safe_verifier_sha256"]
)

assert (
    sha(COPY / "11_review_package_v1.SHA256SUMS")
    == src["checksum_sha256"]
)

package_sums = COPY / "11_review_package_v1.SHA256SUMS"

rows = [
    line.strip()
    for line in package_sums.read_text(
        encoding="utf-8"
    ).splitlines()
    if line.strip()
]

assert len(rows) == 26

for row in rows:
    digest, name = row.split(None, 1)
    name = name.strip().lstrip("*")

    path = COPY / name

    assert path.is_file()
    assert sha(path) == digest

instructions = (
    H / "04_external_reviewer_instructions.v1.md"
).read_text(encoding="utf-8")

required = [
    "Review exactly:",
    "`CWXR07-S1`",
    "A PASS does **not** certify that an independently observed external process executed historical Decision-0147 A02 exactly once.",
    "A PASS does **not** certify a global no-rerun fact outside the reviewed repository evidence.",
    "`APPROVE_CWXR07_S1_CORRECTIVE_SUCCESSOR_V1`",
    "`Spec-Technical-Reviewer-1`",
]

for marker in required:
    assert marker in instructions, marker

blank = H / "05_CWXR07_S1_reviewer_packet.INITIAL_BLANK.EXACT_COPY.v1.md"

assert (
    sha(blank)
    == manifest["external_artifacts"][
        "editable_manual_review_copy_initial_sha256"
    ]
)

cons = load(
    H / "07_decision0160_a02_consumption_record.v1.json"
)

assert cons["decision"] == "0160"
assert cons["execution_invocation_count_in_this_controlled_transaction"] == 1
assert cons["return_code"] == 0
assert cons["pass"] is True
assert cons["lifecycle_after_execution"] == "PERMANENTLY_RETIRED"
assert cons["rerun_authorized"] is False
assert cons["retired_a02_verifiers_executed"] is False
assert cons["human_review_completed"] is False
assert cons["governance_adoption_authorized"] is False

sums = H / "09_external_handoff_v1.SHA256SUMS"

sum_rows = [
    line.strip()
    for line in sums.read_text(
        encoding="utf-8"
    ).splitlines()
    if line.strip()
]

expected_files = {
    p.relative_to(H).as_posix()
    for p in H.rglob("*")
    if p.is_file()
    and p.name != sums.name
}

actual_files = set()

for row in sum_rows:
    digest, name = row.split(None, 1)
    name = name.strip().lstrip("*")

    path = H / name

    assert path.is_file()
    assert sha(path) == digest

    actual_files.add(name)

assert actual_files == expected_files
assert len(expected_files) == 34

print("CWXR07_S1_EXTERNAL_INDEPENDENT_HUMAN_REVIEW_HANDOFF_V1=PASS")
print("HANDOFF_SCOPE=CWXR07-S1_ONLY")
print("HANDOFF_FILE_COUNT=35")
print("HANDOFF_CHECKSUM_ENTRY_COUNT=34")
print("SOURCE_REVIEW_PACKAGE_EXACT_COPY_FILE_COUNT=27")

print("ORIGINAL_REVIEW_STATUS=REVISION_REQUIRED")
print("ORIGINAL_CWXR07_STATUS=REVISION_REQUIRED")
print("ORIGINAL_REVIEW_MODIFIED=NO")

print("ACTUAL_PROCESS_EXECUTION_COUNT_INDEPENDENTLY_PROVEN=NO")
print("GLOBAL_NO_RERUN_FACT_INDEPENDENTLY_PROVEN=NO")
print("RECORD_ASSERTION_PROMOTED_TO_EXTERNAL_EXECUTION_FACT=NO")

print("DECISION0160_A02_STATE=PERMANENTLY_RETIRED")
print("DECISION0160_A02_RERUN_AUTHORIZED=NO")

print("HUMAN_REVIEW_COMPLETED=NO")
print("REVIEWER_IDENTITY_RECORDED=NO")
print("REVIEWER_DECISION_RECORDED=NO")

print("GOVERNANCE_ADOPTION_AUTHORIZED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
