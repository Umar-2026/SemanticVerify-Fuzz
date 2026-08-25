#!/usr/bin/env python3

import hashlib
import json
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
    R / "01_cwxr07_s2_narrowed_corrective_successor_manifest.v1.json"
)

assert (
    manifest["status"]
    == "AUTHOR_CANDIDATE_AWAITING_INDEPENDENT_HUMAN_REVIEW"
)

assert manifest["criterion_id"] == "CWXR07-S2"

s1 = manifest["historical_s1_boundary"]

assert s1["cwxr07_s1_decision"] == "REVISION_REQUIRED"
assert s1["cwxr07_s1_modified"] is False
assert s1["cwxr07_s1_upgraded"] is False
assert s1["historical_original_review_modified"] is False
assert s1["cwxr01_to_cwxr06_and_cwxr08_reopened"] is False
assert s1["exact_copy_of_completed_s1_record_included"] is True
assert s1["exact_copy_file_count"] == 8

copy_root = (
    R
    / "02_s1_completed_human_review_record.EXACT_COPY"
)

actual_copy_files = {
    p.relative_to(copy_root).as_posix(): {
        "sha256": sha(p),
        "size_bytes": p.stat().st_size,
    }
    for p in sorted(copy_root.rglob("*"))
    if p.is_file()
}

assert actual_copy_files == s1["exact_copy_source_files"]
assert len(actual_copy_files) == 8

inner_checksum = (
    copy_root
    / "08_completed_human_review_record_v1.SHA256SUMS"
)

rows = [
    row.strip()
    for row in inner_checksum.read_text(
        encoding="utf-8"
    ).splitlines()
    if row.strip()
]

assert len(rows) == 7

for row in rows:
    digest, name = row.split(None, 1)
    name = name.strip().lstrip("*")

    path = copy_root / name

    assert path.is_file()
    assert sha(path) == digest

historical_manifest = load(
    copy_root
    / "01_completed_human_review_manifest.v1.json"
)

assert historical_manifest["review_scope"] == "CWXR07-S1_ONLY"

assert (
    historical_manifest["human_review"]["cwxr07_s1_decision"]
    == "REVISION_REQUIRED"
)

assert historical_manifest["review_result"]["successor_approved"] is False
assert historical_manifest["review_result"]["revision_required"] is True

strategy = manifest["corrective_strategy"]

assert strategy["reviewer_option"] == 2

assert (
    strategy["strategy"]
    == "FURTHER_NARROW_CRITERION_TO_BYTE_INTEGRITY_AND_INTERNAL_CONSISTENCY"
)

assert strategy["sealed_git_bundle_selected"] is False
assert strategy["full_repository_snapshot_selected"] is False

assert manifest["positive_scope"] == [
    "SUPPLIED_FILE_BYTE_INTEGRITY",
    "CHECKSUM_CLOSURE_INTEGRITY",
    "PRESERVED_A02_SCRIPT_OUTPUT_CONSUMPTION_BINDING_CONSISTENCY",
    "INTERNAL_CONSISTENCY_OF_PRESERVED_REPOSITORY_RECORD_ASSERTIONS",
    "BOUNDED_CLAIM_LANGUAGE_CONSISTENCY",
]

assert manifest["explicit_excluded_independent_proof_claims"] == [
    "DECISION0147_TO_DECISION0148_GIT_PARENTAGE",
    "DECISION0148_STUDY_V1_TREE_IDENTITY",
    "TRACKED_DECISION0147_A02_PATH_HISTORY_CORRECTNESS",
    "REPOSITORY_CONTRADICTION_SEARCH_CORRECTNESS_OR_COMPLETENESS",
    "ACTUAL_EXTERNAL_PROCESS_EXACTLY_ONCE_EXECUTION",
    "GLOBAL_NO_RERUN_FACT",
]

sem = manifest["pass_semantics"]

assert sem["pass_certifies_only_s2_positive_scope"] is True
assert sem["pass_changes_s1_revision_required_to_pass"] is False
assert sem["pass_independently_proves_excluded_claims"] is False
assert sem["pass_authorizes_governance_adoption"] is False
assert sem["pass_authorizes_analyzer"] is False
assert sem["pass_authorizes_baseline"] is False
assert sem["pass_authorizes_repair"] is False

human = manifest["human_review"]

assert human["new_independent_human_review_required"] is True
assert human["human_review_completed"] is False
assert human["reviewer_identity_recorded"] is False
assert human["reviewer_decision_recorded"] is False
assert human["reviewer_identity_synthesized"] is False
assert human["reviewer_decision_synthesized"] is False
assert human["initial_blank_reviewer_packet_included"] is True

life = manifest["decision0164_a02_lifecycle"]

assert life["executed"] is True
assert life["execution_count_in_authoring_transaction"] == 1
assert life["pass"] is True
assert life["lifecycle_after_execution"] == "PERMANENTLY_RETIRED"
assert life["rerun_authorized"] is False

assert all(
    value is False
    for value in manifest["explicit_non_authorizations"].values()
)

criterion = (
    R / "05_cwxr07_s2_narrowed_criterion.v1.md"
).read_text(
    encoding="utf-8"
)

required_criterion = [
    "CWXR07-S1 remains `REVISION_REQUIRED`",
    "supplied-file byte integrity",
    "checksum-closure integrity",
    "internal consistency",
    "Decision-0147 → Decision-0148 Git parentage",
    "Decision-0148 Study V1 tree identity",
    "tracked Decision-0147 A02 path-history correctness",
    "repository contradiction-search correctness or completeness",
    "externally observed actual-process exactly-once execution fact",
    "global no-rerun fact",
    "A `PASS` on CWXR07-S2 certifies only",
    "does not convert CWXR07-S1 from `REVISION_REQUIRED` to `PASS`",
]

for marker in required_criterion:
    assert marker in criterion, marker

review_packet = (
    R / "06_CWXR07_S2_reviewer_packet.INITIAL_BLANK.v1.md"
).read_text(
    encoding="utf-8"
)

required_packet = [
    "# CWXR07-S2 Independent Reviewer Packet — Initial Blank",
    "Review only `CWXR07-S2`.",
    "CWXR07-S1 remains `REVISION_REQUIRED`",
    "`PASS`",
    "`REVISION_REQUIRED`",
    "`FAIL`",
    "CWXR07-S2 decision:",
    "Reviewer notes:",
    "Reviewer name:",
    "Reviewer role:",
    "Reviewer confirmation/signature:",
    "Reviewer attestation:",
    "Review date:",
]

for marker in required_packet:
    assert marker in review_packet, marker

cons = load(
    R / "08_decision0164_a02_consumption_record.v1.json"
)

assert cons["decision"] == "0164"
assert cons["execution_invocation_count_in_this_controlled_transaction"] == 1
assert cons["return_code"] == 0
assert cons["pass"] is True
assert cons["lifecycle_after_execution"] == "PERMANENTLY_RETIRED"
assert cons["rerun_authorized"] is False

assert cons["historical_cwxr07_s1_decision"] == "REVISION_REQUIRED"
assert cons["historical_cwxr07_s1_modified"] is False

assert cons["retired_a02_verifiers_executed"] is False
assert cons["sealed_git_bundle_authored"] is False
assert cons["full_repository_snapshot_authored"] is False
assert cons["human_review_completed"] is False
assert cons["reviewer_identity_synthesized"] is False
assert cons["reviewer_decision_synthesized"] is False
assert cons["successor_approved"] is False
assert cons["governance_adoption_authorized"] is False

sums = (
    R / "10_cwxr07_s2_narrowed_corrective_successor_v1.SHA256SUMS"
)

rows = [
    row.strip()
    for row in sums.read_text(
        encoding="utf-8"
    ).splitlines()
    if row.strip()
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
assert len(expected_files) == 16

print("CWXR07_S2_NARROWED_CORRECTIVE_SUCCESSOR_V1=PASS")

print("SUCCESSOR_CRITERION=CWXR07-S2")
print("STATUS=AUTHOR_CANDIDATE_AWAITING_INDEPENDENT_HUMAN_REVIEW")

print("HISTORICAL_CWXR07_S1_DECISION=REVISION_REQUIRED")
print("HISTORICAL_CWXR07_S1_MODIFIED=NO")
print("HISTORICAL_CWXR07_S1_UPGRADED=NO")

print("S1_COMPLETED_REVIEW_EXACT_COPY_FILE_COUNT=8")

print("BYTE_INTEGRITY_SCOPE=YES")
print("CHECKSUM_CLOSURE_SCOPE=YES")
print("INTERNAL_CONSISTENCY_SCOPE=YES")
print("BOUNDED_CLAIM_LANGUAGE_SCOPE=YES")

print("GIT_PARENTAGE_INDEPENDENT_PROOF_CLAIM=NO")
print("STUDY_TREE_IDENTITY_INDEPENDENT_PROOF_CLAIM=NO")
print("TRACKED_PATH_HISTORY_INDEPENDENT_PROOF_CLAIM=NO")
print("CONTRADICTION_SEARCH_CORRECTNESS_INDEPENDENT_PROOF_CLAIM=NO")
print("ACTUAL_EXTERNAL_EXACTLY_ONCE_FACT_CLAIM=NO")
print("GLOBAL_NO_RERUN_FACT_CLAIM=NO")

print("SEALED_GIT_BUNDLE_INCLUDED=NO")
print("FULL_REPOSITORY_SNAPSHOT_INCLUDED=NO")

print("DECISION0164_A02_STATE=PERMANENTLY_RETIRED")
print("DECISION0164_A02_RERUN_AUTHORIZED=NO")

print("INDEPENDENT_HUMAN_REVIEW_REQUIRED=YES")
print("HUMAN_REVIEW_COMPLETED=NO")
print("REVIEWER_IDENTITY_RECORDED=NO")
print("REVIEWER_DECISION_RECORDED=NO")

print("SUCCESSOR_APPROVED=NO")
print("GOVERNANCE_ADOPTION_AUTHORIZED=NO")

print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
