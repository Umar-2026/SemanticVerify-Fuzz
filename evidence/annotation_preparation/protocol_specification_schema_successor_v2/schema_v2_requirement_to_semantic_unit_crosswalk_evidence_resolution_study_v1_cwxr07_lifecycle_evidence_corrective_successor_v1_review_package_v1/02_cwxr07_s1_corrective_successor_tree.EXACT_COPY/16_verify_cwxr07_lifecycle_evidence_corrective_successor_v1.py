#!/usr/bin/env python3

import hashlib
import json
import subprocess
from pathlib import Path

REPO = Path("/openbayes/home/semanticverify-fuzz-research")

BASE_REL = (
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2"
)

SUCCESSOR_REL = (
    BASE_REL
    + "/schema_v2_requirement_to_semantic_unit_crosswalk_"
      "evidence_resolution_study_v1_cwxr07_lifecycle_evidence_"
      "corrective_successor_v1"
)

P = REPO / SUCCESSOR_REL

def sha(path):
    return hashlib.sha256(
        Path(path).read_bytes()
    ).hexdigest()

def load(name):
    return json.loads(
        (P / name).read_text(
            encoding="utf-8"
        )
    )

manifest = load(
    "01_cwxr07_s1_corrective_successor_manifest.v1.json"
)

parentage = load(
    "07_git_commit_parentage_manifest.v1.json"
)

blob = load(
    "08_a02_git_blob_identity_manifest.v1.json"
)

tree = load(
    "09_study_tree_immutability_manifest.v1.json"
)

history = load(
    "10_reviewed_repository_a02_history_manifest.v1.json"
)

contradictions = load(
    "11_repository_contradiction_search_manifest.v1.json"
)

cons156 = load(
    "15_decision0156_a02_consumption_record.v1.json"
)

assert (
    manifest["status"]
    == "AUTHOR_CANDIDATE_AWAITING_INDEPENDENT_HUMAN_REVIEW"
)

assert manifest["successor_criterion"] == "CWXR07-S1"

assert (
    manifest["original_review"]["overall_decision"]
    == "REVISION_REQUIRED"
)

assert (
    manifest["original_review"]["original_cwxr07_decision"]
    == "REVISION_REQUIRED"
)

assert manifest["original_review"]["modified"] is False
assert manifest["original_review"]["passed_items_reopened"] is False

assert parentage["decision0148_immediate_child_of_decision0147"] is True
assert parentage["decision0147_is_ancestor_of_reviewed_head"] is True
assert parentage["decision0148_is_ancestor_of_reviewed_head"] is True

assert blob["blob_identity_preserved"] is True
assert blob["byte_identity_preserved"] is True

assert tree["study_tree_identity_preserved"] is True

assert history["no_tracked_path_change_after_decision0147"] is True

assert contradictions["no_declared_contradiction_indicator_match"] is True
assert contradictions["total_contradiction_indicator_matches"] == 0

claim = manifest["claim_boundary"]

assert claim["preserved_record_integrity_assessable"] is True
assert claim["repository_internal_consistency_assessable"] is True
assert claim["git_identity_and_ancestry_assessable"] is True
assert claim["bounded_repository_contradiction_search_assessable"] is True

assert (
    claim[
        "actual_external_process_execution_count_independently_proven"
    ]
    is False
)

assert (
    claim[
        "global_no_rerun_fact_independently_proven"
    ]
    is False
)

assert (
    claim[
        "record_assertion_promoted_to_external_execution_fact"
    ]
    is False
)

recorded = manifest["preserved_record_facts"]

assert recorded["recorded_execution_count"] == 1
assert recorded["recorded_return_code"] == 0
assert recorded["recorded_pass_marker"] is True
assert recorded["recorded_lifecycle_after_execution"] == "PERMANENTLY_RETIRED"
assert recorded["recorded_rerun_authorized"] is False

assert cons156["execution_invocation_count_in_this_controlled_transaction"] == 1
assert cons156["return_code"] == 0
assert cons156["pass"] is True
assert cons156["lifecycle_after_execution"] == "PERMANENTLY_RETIRED"
assert cons156["rerun_authorized"] is False

assert cons156["historical_decision0147_a02_executed"] is False
assert cons156["decision0154_a02_rerun"] is False
assert cons156["decision0153_a02_executed"] is False
assert cons156["retired_a02_verifiers_executed"] is False

assert cons156["does_not_prove_historical_external_process_execution_count"] is True
assert cons156["does_not_prove_global_no_rerun_fact"] is True

assert all(
    value is False
    for value in manifest["explicit_non_authorizations"].values()
)

bounded = (
    P
    / "12_cwxr07_s1_bounded_claim_statement.v1.md"
).read_text(encoding="utf-8")

required_bounded = [
    "CWXR07-S1",
    "does **not** independently establish",
    "actual external process executed Decision-0147 A02 exactly once",
    "no rerun could have occurred outside the preserved repository evidence",
    "recorded repository assertions",
]

for marker in required_bounded:
    assert marker in bounded, marker

packet = (
    P
    / "13_CWXR07_S1_reviewer_packet.INITIAL_BLANK.v1.md"
).read_text(encoding="utf-8")

required_packet = [
    "Review only `CWXR07-S1`.",
    "Do not reopen CWXR01–CWXR06 or CWXR08.",
    "`PASS`",
    "`REVISION_REQUIRED`",
    "`FAIL`",
    "CWXR07-S1 decision:",
]

for marker in required_packet:
    assert marker in packet, marker

# Verify exact historical copies against their declared SHA values.
historical = manifest["historical_evidence"]

assert sha(P / "02_decision0147.EXACT_COPY.v1.md") == historical["decision0147_decision_sha256"]
assert sha(P / "03_decision0148.EXACT_COPY.v1.md") == historical["decision0148_decision_sha256"]
assert sha(P / "04_decision0147_a02.EXACT_COPY.v1.py") == historical["decision0147_a02_sha256"]
assert sha(P / "05_decision0147_a02_final_output.EXACT_COPY.v1.txt") == historical["preserved_a02_output_sha256"]
assert sha(P / "06_decision0147_a02_consumption_record.EXACT_COPY.v1.json") == historical["preserved_a02_consumption_record_sha256"]

# Check checksum closure.
sums = P / "17_cwxr07_lifecycle_evidence_corrective_successor_v1.SHA256SUMS"

rows = [
    line.strip()
    for line in sums.read_text(
        encoding="utf-8"
    ).splitlines()
    if line.strip()
]

expected_names = {
    p.name
    for p in P.iterdir()
    if p.is_file()
    and p.name != sums.name
}

actual_names = set()

for row in rows:
    digest, name = row.split(None, 1)
    name = name.strip().lstrip("*")
    path = P / name

    assert path.is_file()
    assert sha(path) == digest

    actual_names.add(name)

assert actual_names == expected_names

print("CWXR07_LIFECYCLE_EVIDENCE_CORRECTIVE_SUCCESSOR_V1=PASS")
print("SUCCESSOR_CRITERION=CWXR07-S1")
print("SUCCESSOR_STATUS=AUTHOR_CANDIDATE_AWAITING_INDEPENDENT_HUMAN_REVIEW")

print("DECISION0147_A02_BYTE_IDENTITY=PASS")
print("DECISION0147_TO_DECISION0148_PARENTAGE=PASS")
print("DECISION0148_STUDY_TREE_IDENTITY=PASS")
print("PRESERVED_A02_OUTPUT_BINDING=PASS")
print("PRESERVED_A02_CONSUMPTION_RECORD_BINDING=PASS")
print("TRACKED_A02_PATH_LATER_CHANGE_COUNT=0")
print("DECLARED_REPOSITORY_CONTRADICTION_INDICATOR_MATCH_COUNT=0")

print("PRESERVED_RECORD_EXECUTION_COUNT=1")
print("PRESERVED_RECORD_RETURN_CODE=0")
print("PRESERVED_RECORD_LIFECYCLE=PERMANENTLY_RETIRED")
print("PRESERVED_RECORD_RERUN_AUTHORIZED=NO")

print("ACTUAL_PROCESS_EXECUTION_COUNT_INDEPENDENTLY_PROVEN=NO")
print("GLOBAL_NO_RERUN_FACT_INDEPENDENTLY_PROVEN=NO")
print("RECORD_ASSERTION_PROMOTED_TO_EXTERNAL_EXECUTION_FACT=NO")

print("ORIGINAL_REVIEW_MODIFIED=NO")
print("ORIGINAL_CWXR07_STATUS=REVISION_REQUIRED")
print("INDEPENDENT_SUCCESSOR_HUMAN_REVIEW_REQUIRED=YES")
print("GOVERNANCE_ADOPTION_AUTHORIZED=NO")

print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
