#!/usr/bin/env python3

import hashlib
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]

SUBJECT = HERE / "study_v1_exact"
AUTH = HERE / "decision0128_authorization_exact"
PORTABLE = HERE / "portable_sources"

SUBJECT_MANIFEST = HERE / "01_review_subject_manifest.v1.json"
SOURCE_MANIFEST = HERE / "02_source_binding_manifest.v1.json"
REVIEWER_PACKET = HERE / "03_RPR01_RPR08_reviewer_packet.BLANK.v1.md"
A02_OUT = HERE / "04_decision0128_a02_final_output.EXACT_COPY.v1.txt"
A02_CONS = HERE / "05_decision0128_a02_consumption_record.v1.json"
BUNDLE = HERE / "06_repository_checkpoint.bundle"
BUNDLE_MANIFEST = HERE / "07_repository_checkpoint_bundle_manifest.v1.json"
SUMS = HERE / "10_review_package_v1.SHA256SUMS"

EXPECTED_HEAD = "7f13e5569c5d25c9c104a9b1dd68516471b6017a"
EXPECTED_STUDY_TREE = "ee85980dcff85b5be3f21995f578b3b78cf39aa2"
EXPECTED_AUTH_TREE = "4b188e43c8367baf983c3ad6ccd3838bb9d2b269"

def fail(msg):
    print("FAIL|" + msg)
    raise SystemExit(1)

def sha(path):
    if not path.is_file():
        fail("MISSING|" + str(path))
    return hashlib.sha256(path.read_bytes()).hexdigest()

subject_manifest = json.loads(
    SUBJECT_MANIFEST.read_text(encoding="utf-8")
)

checkpoint = subject_manifest["decision_0128_checkpoint"]

if checkpoint["commit"] != EXPECTED_HEAD:
    fail("CHECKPOINT_COMMIT")

if checkpoint["study_git_tree"] != EXPECTED_STUDY_TREE:
    fail("STUDY_TREE_BINDING")

if checkpoint["authorization_git_tree"] != EXPECTED_AUTH_TREE:
    fail("AUTH_TREE_BINDING")

if subject_manifest["reviewer_decision_present"] is not False:
    fail("REVIEWER_DECISION_PRESENT")

if subject_manifest["reviewer_decision_synthesized"] is not False:
    fail("REVIEWER_DECISION_SYNTHESIZED")

if subject_manifest["required_reviewer_role"] != "Spec-Technical-Reviewer-1":
    fail("REVIEWER_ROLE")

if subject_manifest["review_items"] != [
    "RPR01",
    "RPR02",
    "RPR03",
    "RPR04",
    "RPR05",
    "RPR06",
    "RPR07",
    "RPR08",
]:
    fail("REVIEW_ITEMS")

for entry in subject_manifest["review_subject"]["study_files"]:
    path = HERE / entry["package_relative_path"]

    if sha(path) != entry["sha256"]:
        fail(
            "STUDY_EXACT_COPY|"
            + entry["package_relative_path"]
        )

source_manifest = json.loads(
    SOURCE_MANIFEST.read_text(encoding="utf-8")
)

if source_manifest["source_count"] != 7:
    fail("SOURCE_COUNT")

if source_manifest["all_sources_portable"] is not True:
    fail("SOURCE_PORTABILITY")

for entry in source_manifest["records"]:
    portable = HERE / entry["portable_package_relative_path"]

    if sha(portable) != entry["source_sha256"]:
        fail(
            "PORTABLE_SOURCE_SHA|"
            + entry["original_repo_relative_path"]
        )

    if entry["byte_exact_portable_copy"] is not True:
        fail("BYTE_EXACT_FLAG")

    if entry["independently_resolvable_from_package"] is not True:
        fail("RESOLVABILITY_FLAG")

packet = REVIEWER_PACKET.read_text(
    encoding="utf-8"
)

for item in (
    "RPR01",
    "RPR02",
    "RPR03",
    "RPR04",
    "RPR05",
    "RPR06",
    "RPR07",
    "RPR08",
):
    if item not in packet:
        fail("REVIEW_PACKET_ITEM|" + item)

if (
    "APPROVE_V4_LOSSLESSNESS_REQUIREMENT_PROVENANCE_BINDING_RESOLUTION_STUDY_V1"
    not in packet
):
    fail("OVERALL_DECISION_TEMPLATE")

if "AWAITING INDEPENDENT HUMAN REVIEW" not in packet:
    fail("PACKET_NOT_BLANK_STATE")

cons = json.loads(
    A02_CONS.read_text(encoding="utf-8")
)

if cons["final_run_result"] != "PASS":
    fail("A02_RESULT")

if cons["verifier_state_after_run"] != "PERMANENTLY_RETIRED":
    fail("A02_STATE")

if cons["must_never_be_rerun"] is not True:
    fail("A02_RETIREMENT")

if sha(A02_OUT) != cons["final_output_sha256"]:
    fail("A02_OUTPUT_SHA")

if (
    "INDEPENDENT_HUMAN_REVIEW_PACKAGE_AUTHORING_AUTHORIZATION=PASS"
    not in A02_OUT.read_text(encoding="utf-8")
):
    fail("A02_PASS_MARKER")

bundle_manifest = json.loads(
    BUNDLE_MANIFEST.read_text(encoding="utf-8")
)

if bundle_manifest["checkpoint_commit"] != EXPECTED_HEAD:
    fail("BUNDLE_CHECKPOINT")

if sha(BUNDLE) != bundle_manifest["bundle_sha256"]:
    fail("BUNDLE_SHA")

p = subprocess.run(
    [
        "git",
        "-C",
        str(REPO),
        "bundle",
        "verify",
        str(BUNDLE),
    ],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    check=False,
)

if p.returncode != 0:
    fail(
        "BUNDLE_VERIFY|"
        + p.stdout
        + p.stderr
    )

if SUMS.is_file():
    for line in SUMS.read_text(
        encoding="utf-8"
    ).splitlines():

        if not line.strip():
            continue

        digest, rel = line.split(None, 1)
        rel = rel.strip().lstrip("*")

        if sha(HERE / rel) != digest:
            fail("CHECKSUM|" + rel)

print("INDEPENDENT_HUMAN_REVIEW_PACKAGE_V1=PASS")
print("PACKAGE_STATUS=AUTHOR_CANDIDATE_AWAITING_INDEPENDENT_HUMAN_REVIEW")
print("REVIEW_ITEMS=RPR01|RPR02|RPR03|RPR04|RPR05|RPR06|RPR07|RPR08")
print("REQUIRED_REVIEWER_ROLE=Spec-Technical-Reviewer-1")
print("REVIEWER_DECISION_PRESENT=NO")
print("REVIEWER_DECISION_SYNTHESIZED=NO")
print("PORTABLE_SOURCE_COUNT=7")
print("PORTABLE_SOURCE_RESOLVABILITY=PASS")
print("SEALED_REPOSITORY_CHECKPOINT_BUNDLE=PASS")
print("STUDY_OUTCOME_UNDER_REVIEW=REQUIREMENT_PROVENANCE_RESOLVED")
print("STUDY_GOVERNANCE_ADOPTED=NO")
print("POSITIVE_MAPPING_PROVEN=NO")
print("NEGATIVE_MAPPING_IMPOSSIBILITY_PROVEN=NO")
print("WHOLE_V4_EXHAUSTIVENESS_PROVEN=NO")
print("OPERATIONAL_MAPPING_AUTHORIZED=NO")
print("SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO")
print("CURL_JSON_AUTHORIZED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
print("DECISION_0128_A02_STATE=PERMANENTLY_RETIRED")
print("DECISION_0128_A02_EXECUTED_BY_SAFE_VERIFIER=NO")
print("DECISION_0126_A02_STATE=PERMANENTLY_RETIRED")
print("RETIRED_A02_VERIFIERS_EXECUTED=NO")
