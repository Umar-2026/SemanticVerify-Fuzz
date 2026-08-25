#!/usr/bin/env python3

import hashlib
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent

EXPECTED_BLANK_SHA = (
    "3e777294a87314a54658a0ce4156ab1324d7bb314529c3907ee47119e2234fdd"
)

EXPECTED_D0151_SHA = (
    "77402a87f4046da20685a269f373de0ad8b739d53171ca893eb309028e7f23d6"
)

EXPECTED_D0150_SHA = (
    "2dbdc6c5cb8fbe0887fce73c65274ff913eab75f118fda3d88a7e817cdeae898"
)

PASS_MARKER = (
    "REQUIREMENT_TO_SEMANTIC_UNIT_CROSSWALK_"
    "EVIDENCE_RESOLUTION_STUDY_V1_EXTERNAL_"
    "INDEPENDENT_HUMAN_REVIEW_HANDOFF_"
    "AUTHORING_AUTHORIZATION=PASS"
)

def sha(path):
    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()

def load(name):
    return json.loads(
        (HERE / name).read_text(
            encoding="utf-8"
        )
    )

manifest = load(
    "01_external_handoff_manifest.v1.json"
)

consumption = load(
    "05_decision0151_a02_consumption_record.v1.json"
)

assert (
    manifest["status"]
    == "EXTERNAL_HANDOFF_AUTHORED_AWAITING_INDEPENDENT_HUMAN_REVIEW"
)

scope = manifest["review_scope"]

assert scope["review_item_ids"] == [
    "CWXR01",
    "CWXR02",
    "CWXR03",
    "CWXR04",
    "CWXR05",
    "CWXR06",
    "CWXR07",
    "CWXR08",
]

assert (
    scope["required_reviewer_role"]
    == "Spec-Technical-Reviewer-1"
)

assert scope["per_item_allowed_decisions"] == [
    "PASS",
    "REVISION_REQUIRED",
    "FAIL",
]

assert (
    scope["overall_allowed_decisions"][0]
    == "APPROVE_REQUIREMENT_TO_SEMANTIC_UNIT_"
       "CROSSWALK_EVIDENCE_RESOLUTION_STUDY_V1"
)

review = manifest["review_state"]

assert review["independent_human_review_completed"] is False
assert review["reviewer_identity_recorded_in_repository"] is False
assert review["reviewer_decisions_recorded_in_repository"] is False
assert review["overall_review_decision_recorded_in_repository"] is False
assert review["returned_reviewer_packet_recorded"] is False

assert (
    manifest["governance_state"]
    ["study_governance_adopted"]
    is False
)

assert all(
    value is False
    for value in manifest["non_authorizations"].values()
)

assert consumption["a02_execution_count"] == 1
assert consumption["a02_return_code"] == 0
assert consumption["a02_pass_marker_present"] is True
assert (
    consumption["lifecycle_after_execution"]
    == "PERMANENTLY_RETIRED"
)
assert consumption["rerun_authorized"] is False
assert (
    consumption["decision0149_a02_executed_by_this_transaction"]
    is False
)
assert (
    consumption["decision0147_a02_executed_by_this_transaction"]
    is False
)
assert (
    consumption["retired_a02_verifier_execution_performed"]
    is False
)

a02_output = (
    HERE
    / "04_decision0151_a02_final_output.EXACT_COPY.v1.txt"
).read_text(
    encoding="utf-8"
)

assert PASS_MARKER in a02_output.splitlines()

blank = (
    HERE
    / "03_CWXR01_CWXR08_reviewer_packet.INITIAL_BLANK_EXACT_COPY.v1.md"
)

assert sha(blank) == EXPECTED_BLANK_SHA

assert (
    sha(HERE / "06_decision0151.EXACT_COPY.v1.md")
    == EXPECTED_D0151_SHA
)

assert (
    sha(HERE / "07_decision0150.EXACT_COPY.v1.md")
    == EXPECTED_D0150_SHA
)

# Verify the exact copied review package through its own safe verifier.
review_package = (
    HERE
    / "review_package_v1_exact"
)

review_output = subprocess.check_output(
    [
        "python3",
        str(
            review_package
            / "10_verify_independent_human_review_package.v1.py"
        ),
    ],
    text=True,
)

required_review_markers = [
    (
        "REQUIREMENT_TO_SEMANTIC_UNIT_CROSSWALK_"
        "EVIDENCE_RESOLUTION_STUDY_V1_INDEPENDENT_"
        "HUMAN_REVIEW_PACKAGE=PASS"
    ),
    (
        "PACKAGE_STATUS="
        "AUTHOR_CANDIDATE_AWAITING_INDEPENDENT_HUMAN_REVIEW"
    ),
    "BLANK_REVIEWER_PACKET=PASS",
    "INDEPENDENT_HUMAN_REVIEW_COMPLETED=NO",
    "REVIEWER_IDENTITY_RECORDED=NO",
    "REVIEWER_DECISIONS_RECORDED=NO",
    "STUDY_GOVERNANCE_ADOPTED=NO",
    "DECISION_0149_A02_STATE=PERMANENTLY_RETIRED",
]

review_lines = review_output.splitlines()

for marker in required_review_markers:
    assert marker in review_lines

# Verify full handoff checksum closure.
sumfile = (
    HERE
    / "09_external_handoff_v1.SHA256SUMS"
)

checksum_entries = {}

for line in sumfile.read_text(
    encoding="utf-8"
).splitlines():

    if not line.strip():
        continue

    expected, name = line.split(
        None,
        1,
    )

    name = name.strip().lstrip("*")

    if name.startswith("./"):
        name = name[2:]

    assert name not in checksum_entries

    checksum_entries[name] = expected

actual_files = {
    str(p.relative_to(HERE))
    for p in HERE.rglob("*")
    if p.is_file()
    and p.name != "09_external_handoff_v1.SHA256SUMS"
}

assert set(checksum_entries) == actual_files

for name, expected in checksum_entries.items():
    assert sha(HERE / name) == expected

assert len(actual_files) == 37
assert len(checksum_entries) == 37

print(
    "REQUIREMENT_TO_SEMANTIC_UNIT_CROSSWALK_"
    "EVIDENCE_RESOLUTION_STUDY_V1_EXTERNAL_"
    "INDEPENDENT_HUMAN_REVIEW_HANDOFF=PASS"
)

print("HANDOFF_STATUS=AWAITING_INDEPENDENT_HUMAN_REVIEW")
print("REVIEW_ITEM_COUNT=8")
print("SOURCE_REVIEW_PACKAGE_EXACT_COPY=PASS")
print("REPOSITORY_INITIAL_BLANK_PACKET_EXACT_COPY=PASS")
print("HANDOFF_CHECKSUM_ENTRY_COUNT=37")

print("INDEPENDENT_HUMAN_REVIEW_COMPLETED=NO")
print("REVIEWER_IDENTITY_RECORDED_IN_REPOSITORY=NO")
print("REVIEWER_DECISIONS_RECORDED_IN_REPOSITORY=NO")
print("OVERALL_REVIEW_DECISION_RECORDED_IN_REPOSITORY=NO")

print("STUDY_GOVERNANCE_ADOPTED=NO")

print("DECISION_0151_A02_STATE=PERMANENTLY_RETIRED")
print("DECISION_0151_A02_RERUN_AUTHORIZED=NO")
print("DECISION_0149_A02_RERUN=NO")
print("DECISION_0147_A02_RERUN=NO")

print("PAIR_RECLASSIFICATION=NO")
print("HISTORICAL_18639_PAIR_RECLASSIFICATION=NO")
print("OPERATIONAL_MAPPING_AUTHORIZED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
