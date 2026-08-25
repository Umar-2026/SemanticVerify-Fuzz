#!/usr/bin/env python3

import hashlib
import json
from pathlib import Path

P = Path(__file__).resolve().parent
COPY = P / "02_cwxr07_s1_corrective_successor_tree.EXACT_COPY"

def sha(path):
    return hashlib.sha256(
        Path(path).read_bytes()
    ).hexdigest()

def load(path):
    return json.loads(
        Path(path).read_text(
            encoding="utf-8"
        )
    )

manifest = load(
    P / "01_review_package_manifest.v1.json"
)

assert (
    manifest["status"]
    == "AUTHOR_CANDIDATE_AWAITING_EXTERNAL_HANDOFF_AND_INDEPENDENT_HUMAN_REVIEW"
)

assert manifest["review_scope"] == "CWXR07-S1_ONLY"

contract = manifest["review_contract"]

assert contract["criterion"] == "CWXR07-S1"
assert contract["item_count"] == 1

assert contract["allowed_item_decisions"] == [
    "PASS",
    "REVISION_REQUIRED",
    "FAIL",
]

assert contract["allowed_overall_decisions"] == [
    "APPROVE_CWXR07_S1_CORRECTIVE_SUCCESSOR_V1",
    "REVISION_REQUIRED",
    "FAIL",
]

assert contract["reviewer_role"] == "Spec-Technical-Reviewer-1"
assert contract["independent_human_review_required"] is True
assert contract["human_review_completed"] is False
assert contract["reviewer_identity_recorded"] is False
assert contract["item_decision_recorded"] is False
assert contract["overall_decision_recorded"] is False

original = manifest["original_review_boundary"]

assert original["overall_decision"] == "REVISION_REQUIRED"
assert original["original_cwxr07_decision"] == "REVISION_REQUIRED"
assert original["original_review_modified"] is False
assert original["passed_items_reopened"] is False

claim = manifest["claim_boundary"]

assert claim["preserved_record_integrity_reviewable"] is True
assert claim["repository_internal_consistency_reviewable"] is True
assert claim["git_identity_and_ancestry_reviewable"] is True
assert claim["bounded_repository_contradiction_search_reviewable"] is True

assert (
    claim[
        "actual_external_process_execution_count_independently_proven"
    ]
    is False
)

assert claim["global_no_rerun_fact_independently_proven"] is False
assert claim["record_assertion_promoted_to_external_execution_fact"] is False

life = manifest["decision0158_a02_lifecycle"]

assert life["executed"] is True
assert life["execution_count_in_package_authoring_transaction"] == 1
assert life["pass"] is True
assert life["lifecycle_after_execution"] == "PERMANENTLY_RETIRED"
assert life["rerun_authorized"] is False

handoff = manifest["external_handoff"]

assert handoff["authorized"] is False
assert handoff["completed"] is False
assert handoff["editable_manual_review_copy_created"] is False

assert all(
    value is False
    for value in manifest["explicit_non_authorizations"].values()
)

# ------------------------------------------------------------
# Verify package root exact copies
# ------------------------------------------------------------

bindings = manifest["exact_copy_bindings"]

assert (
    sha(P / "03_decision0157.EXACT_COPY.v1.md")
    == bindings["decision0157_sha256"]
)

assert (
    sha(P / "04_decision0156.EXACT_COPY.v1.md")
    == bindings["decision0156_sha256"]
)

assert (
    sha(P / "05_original_completed_human_review.EXACT_COPY.v1.md")
    == bindings["original_completed_review_sha256"]
)

assert (
    sha(
        P
        / "07_CWXR07_S1_reviewer_packet.INITIAL_BLANK.EXACT_COPY.v1.md"
    )
    == bindings["initial_blank_cwxr07_s1_packet_sha256"]
)

assert (
    sha(P / "08_decision0158_a02_final_output.EXACT_COPY.v1.txt")
    == bindings["decision0158_a02_output_sha256"]
)

assert (
    sha(P / "09_decision0158_a02_consumption_record.v1.json")
    == bindings["decision0158_a02_consumption_record_sha256"]
)

# ------------------------------------------------------------
# Verify copied successor internally
# ------------------------------------------------------------

successor_manifest = load(
    COPY / "01_cwxr07_s1_corrective_successor_manifest.v1.json"
)

assert successor_manifest["successor_criterion"] == "CWXR07-S1"

assert (
    successor_manifest["status"]
    == "AUTHOR_CANDIDATE_AWAITING_INDEPENDENT_HUMAN_REVIEW"
)

assert (
    sha(COPY / "01_cwxr07_s1_corrective_successor_manifest.v1.json")
    == manifest["successor_binding"]["successor_manifest_sha256"]
)

assert (
    sha(COPY / "16_verify_cwxr07_lifecycle_evidence_corrective_successor_v1.py")
    == manifest["successor_binding"]["successor_repeat_safe_verifier_sha256"]
)

assert (
    sha(COPY / "17_cwxr07_lifecycle_evidence_corrective_successor_v1.SHA256SUMS")
    == manifest["successor_binding"]["successor_checksum_sha256"]
)

successor_sums = (
    COPY
    / "17_cwxr07_lifecycle_evidence_corrective_successor_v1.SHA256SUMS"
)

rows = [
    row.strip()
    for row in successor_sums.read_text(
        encoding="utf-8"
    ).splitlines()
    if row.strip()
]

assert len(rows) == 16

for row in rows:
    digest, name = row.split(None, 1)
    name = name.strip().lstrip("*")

    path = COPY / name

    assert path.is_file()
    assert sha(path) == digest

# ------------------------------------------------------------
# Verify claim/instruction boundaries
# ------------------------------------------------------------

bounded = (
    COPY / "12_cwxr07_s1_bounded_claim_statement.v1.md"
).read_text(encoding="utf-8")

assert "CWXR07-S1" in bounded

assert (
    "actual external process executed Decision-0147 A02 exactly once"
    in bounded
)

assert (
    "no rerun could have occurred outside the preserved repository evidence"
    in bounded
)

instructions = (
    P / "06_reviewer_instructions.v1.md"
).read_text(encoding="utf-8")

required_instructions = [
    "Review exactly one successor criterion:",
    "`CWXR07-S1`",
    "Do not reopen CWXR01–CWXR06 or CWXR08.",
    "A PASS does **not** certify that an independently observed external process executed Decision-0147 A02 exactly once.",
    "A PASS does **not** certify a global no-rerun fact outside the reviewed repository evidence.",
    "`APPROVE_CWXR07_S1_CORRECTIVE_SUCCESSOR_V1`",
    "`Spec-Technical-Reviewer-1`",
]

for marker in required_instructions:
    assert marker in instructions, marker

packet = (
    P
    / "07_CWXR07_S1_reviewer_packet.INITIAL_BLANK.EXACT_COPY.v1.md"
).read_text(encoding="utf-8")

assert "Review only `CWXR07-S1`." in packet
assert "CWXR07-S1 decision:" in packet

original_review = (
    P / "05_original_completed_human_review.EXACT_COPY.v1.md"
).read_text(encoding="utf-8")

assert "CWXR07 decision: `REVISION_REQUIRED`" in original_review
assert "Overall decision: `REVISION_REQUIRED`" in original_review

cons = load(
    P / "09_decision0158_a02_consumption_record.v1.json"
)

assert cons["decision"] == "0158"
assert cons["execution_invocation_count_in_this_controlled_transaction"] == 1
assert cons["return_code"] == 0
assert cons["pass"] is True
assert cons["lifecycle_after_execution"] == "PERMANENTLY_RETIRED"
assert cons["rerun_authorized"] is False
assert cons["retired_a02_verifiers_executed"] is False
assert cons["human_review_completed"] is False
assert cons["external_handoff_authorized"] is False
assert cons["governance_adoption_authorized"] is False

# ------------------------------------------------------------
# Verify full package checksum closure
# ------------------------------------------------------------

package_sums = P / "11_review_package_v1.SHA256SUMS"

sum_rows = [
    row.strip()
    for row in package_sums.read_text(
        encoding="utf-8"
    ).splitlines()
    if row.strip()
]

expected_files = {
    path.relative_to(P).as_posix()
    for path in P.rglob("*")
    if path.is_file()
    and path.name != package_sums.name
}

actual_files = set()

for row in sum_rows:
    digest, name = row.split(None, 1)
    name = name.strip().lstrip("*")

    path = P / name

    assert path.is_file()
    assert sha(path) == digest

    actual_files.add(name)

assert actual_files == expected_files

assert len(expected_files) == 26

print("CWXR07_S1_INDEPENDENT_HUMAN_REVIEW_PACKAGE_V1=PASS")
print("REVIEW_SCOPE=CWXR07-S1_ONLY")
print("PACKAGE_FILE_COUNT=27")
print("PACKAGE_CHECKSUM_ENTRY_COUNT=26")
print("SUCCESSOR_EXACT_COPY_FILE_COUNT=17")

print("ORIGINAL_REVIEW_STATUS=REVISION_REQUIRED")
print("ORIGINAL_CWXR07_STATUS=REVISION_REQUIRED")
print("ORIGINAL_REVIEW_MODIFIED=NO")

print("ACTUAL_PROCESS_EXECUTION_COUNT_INDEPENDENTLY_PROVEN=NO")
print("GLOBAL_NO_RERUN_FACT_INDEPENDENTLY_PROVEN=NO")
print("RECORD_ASSERTION_PROMOTED_TO_EXTERNAL_EXECUTION_FACT=NO")

print("DECISION0158_A02_STATE=PERMANENTLY_RETIRED")
print("DECISION0158_A02_RERUN_AUTHORIZED=NO")

print("HUMAN_REVIEW_COMPLETED=NO")
print("REVIEWER_IDENTITY_RECORDED=NO")
print("REVIEWER_DECISION_RECORDED=NO")

print("EXTERNAL_HANDOFF_AUTHORIZED=NO")
print("GOVERNANCE_ADOPTION_AUTHORIZED=NO")

print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
