#!/usr/bin/env python3

import hashlib
import json
import re
from pathlib import Path

R = Path(__file__).resolve().parent

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
    R / "01_completed_human_review_manifest.v1.json"
)

assert (
    manifest["status"]
    == "COMPLETED_HUMAN_REVIEW_RECORDED_REVISION_REQUIRED"
)

assert manifest["review_scope"] == "CWXR07-S1_ONLY"

review = manifest["human_review"]

assert review["genuine_external_human_review"] is True
assert review["structurally_complete"] is True
assert review["cwxr07_s1_decision"] == "REVISION_REQUIRED"

assert review["reviewer_name"] == "Abdul Raheem Shahzad"
assert review["reviewer_role"] == "Spec-Technical-Reviewer-1"
assert review["reviewer_confirmation"] == "ARS"
assert review["review_date"] == "25 / August / 2026"

assert review["reviewer_attestation_present"] is True
assert review["corrective_evidence_request_present"] is True

assert review["overall_successor_review_decision_field_required_by_form"] is False
assert review["overall_successor_review_decision_synthesized"] is False

result = manifest["review_result"]

assert result["successor_approved"] is False
assert result["revision_required"] is True
assert result["corrective_evidence_required"] is True
assert result["review_result_rewritten"] is False
assert result["reviewer_decision_synthesized"] is False

remediation = manifest["reviewer_requested_remediation"]

assert remediation["strategy_selected_by_author"] is False

assert (
    remediation["option_1"]
    == "CHECKSUM_BOUND_SEALED_GIT_BUNDLE_OR_EQUIVALENT_IMMUTABLE_REPOSITORY_SNAPSHOT"
)

assert (
    remediation["option_2"]
    == "FURTHER_NARROW_CWXR07_S1_TO_BYTE_INTEGRITY_AND_INTERNAL_CONSISTENCY"
)

claim = manifest["claim_boundary"]

assert claim["actual_external_process_exactly_once_certified"] is False
assert claim["global_no_rerun_fact_certified"] is False
assert claim["repository_assertion_promoted_to_external_fact"] is False
assert claim["historical_original_review_modified"] is False
assert claim["historical_cwxr07_modified"] is False
assert claim["cwxr01_to_cwxr06_and_cwxr08_reopened"] is False

life = manifest["decision0162_a02_lifecycle"]

assert life["executed"] is True
assert life["execution_count_in_recording_transaction"] == 1
assert life["pass"] is True
assert life["lifecycle_after_execution"] == "PERMANENTLY_RETIRED"
assert life["rerun_authorized"] is False

assert all(
    value is False
    for value in manifest["explicit_non_authorizations"].values()
)

returned = R / "02_returned_human_review.EXACT_COPY.v1.md"

assert sha(returned) == review["returned_packet_sha256"]
assert returned.stat().st_size == review["returned_packet_size_bytes"]

text = returned.read_text(
    encoding="utf-8"
)

m = re.search(
    r"^CWXR07-S1 decision:\s*(.+?)\s*$",
    text,
    flags=re.MULTILINE,
)

assert m
assert m.group(1).strip().strip("`") == "REVISION_REQUIRED"

required = [
    "Reviewer name: Abdul Raheem Shahzad",
    "Reviewer role: Spec-Technical-Reviewer-1",
    "Reviewer confirmation/signature: ARS",
    "Reviewer attestation:",
    "Review date: 25 / August / 2026",
    "cannot be independently reproduced",
    "sealed Git bundle",
    "Alternatively, narrow CWXR07-S1 further",
]

for marker in required:
    assert marker in text, marker

assert (
    sha(R / "03_decision0161.EXACT_COPY.v1.md")
    == manifest["source_handoff"]["decision0161_sha256"]
)

assert (
    sha(R / "04_external_handoff_manifest.EXACT_COPY.v1.json")
    == manifest["source_handoff"]["manifest_sha256"]
)

assert (
    sha(R / "05_decision0162_a02_final_output.EXACT_COPY.v1.txt")
    == life["output_sha256"]
)

assert (
    sha(R / "06_decision0162_a02_consumption_record.v1.json")
    == life["consumption_record_sha256"]
)

cons = load(
    R / "06_decision0162_a02_consumption_record.v1.json"
)

assert cons["decision"] == "0162"
assert cons["execution_invocation_count_in_this_controlled_transaction"] == 1
assert cons["return_code"] == 0
assert cons["pass"] is True
assert cons["lifecycle_after_execution"] == "PERMANENTLY_RETIRED"
assert cons["rerun_authorized"] is False
assert cons["retired_a02_verifiers_executed"] is False
assert cons["review_result_rewritten"] is False
assert cons["reviewer_decision_synthesized"] is False
assert cons["successor_approved"] is False
assert cons["corrective_evidence_authoring_authorized"] is False
assert cons["governance_adoption_authorized"] is False

sums = R / "08_completed_human_review_record_v1.SHA256SUMS"

rows = [
    line.strip()
    for line in sums.read_text(
        encoding="utf-8"
    ).splitlines()
    if line.strip()
]

expected_files = {
    p.relative_to(R).as_posix()
    for p in R.rglob("*")
    if p.is_file()
    and p.name != sums.name
}

actual_files = set()

for row in rows:
    digest, name = row.split(None, 1)
    name = name.strip().lstrip("*")

    path = R / name

    assert path.is_file()
    assert sha(path) == digest

    actual_files.add(name)

assert actual_files == expected_files
assert len(expected_files) == 7

print("CWXR07_S1_COMPLETED_HUMAN_REVIEW_RECORD_V1=PASS")
print("REVIEW_SCOPE=CWXR07-S1_ONLY")
print("CWXR07_S1_DECISION=REVISION_REQUIRED")

print("GENUINE_EXTERNAL_HUMAN_REVIEW_RECORDED=YES")
print("HUMAN_REVIEW_STRUCTURALLY_COMPLETE=YES")

print("REVIEWER_NAME=Abdul Raheem Shahzad")
print("REVIEWER_ROLE=Spec-Technical-Reviewer-1")
print("REVIEWER_CONFIRMATION=ARS")
print("REVIEWER_ATTESTATION_PRESENT=YES")

print("SUCCESSOR_APPROVED=NO")
print("CORRECTIVE_EVIDENCE_REQUIRED=YES")
print("CORRECTIVE_STRATEGY_SELECTED=NO")

print("ACTUAL_PROCESS_EXACTLY_ONCE_FACT_CERTIFIED=NO")
print("GLOBAL_NO_RERUN_FACT_CERTIFIED=NO")
print("REPOSITORY_ASSERTION_PROMOTED_TO_EXTERNAL_FACT=NO")

print("DECISION0162_A02_STATE=PERMANENTLY_RETIRED")
print("DECISION0162_A02_RERUN_AUTHORIZED=NO")

print("CORRECTIVE_EVIDENCE_AUTHORING_AUTHORIZED=NO")
print("GOVERNANCE_ADOPTION_AUTHORIZED=NO")

print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
