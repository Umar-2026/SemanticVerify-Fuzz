#!/usr/bin/env python3

import hashlib
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]

BASE_REL = (
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2"
)

RECORD_REL = (
    BASE_REL
    + "/schema_v2_requirement_bound_carrier_admissibility_resolution_study_v1_completed_human_review_record_v1"
)

THIS_AUTH_REL = (
    BASE_REL
    + "/schema_v2_requirement_bound_carrier_admissibility_resolution_study_v1_bounded_governance_adoption_authorization_v1"
)

RECORD = REPO / RECORD_REL

RECORD_SAFE = (
    RECORD
    / "08_verify_completed_RBCA01_RBCA08_human_review_record.v1.py"
)

MANIFEST = (
    RECORD
    / "02_completed_human_review_manifest.v1.json"
)

ACCOUNTING = (
    RECORD
    / "03_review_result_accounting.v1.json"
)

AUTH = (
    HERE
    / "01_bounded_governance_adoption_authorization.v1.json"
)

EXPECTED_DECISION0144 = (
    "e82a13b9ecb1ca611b3eb00be62cc7d203314de7"
)

EXPECTED_RECORD_TREE = (
    "1b42cb3de3eb699c9e8a80387787250c6355d23b"
)

EXPECTED_REVIEW_SHA = (
    "9ded6b54b04c438a9a0f5ac3b7557d5ab19283c812fa5f2f6b529c92ef2e7eb1"
)

EXPECTED_OVERALL = (
    "APPROVE_REQUIREMENT_BOUND_CARRIER_ADMISSIBILITY_RESOLUTION_STUDY_V1"
)

def fail(msg):
    print("FAIL|" + msg)
    raise SystemExit(1)

def git(*args):
    p = subprocess.run(
        ["git", "-C", str(REPO), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )

    if p.returncode != 0:
        fail(
            "GIT|"
            + " ".join(args)
            + "|"
            + p.stderr.strip()
        )

    return p.stdout.strip()

current_head = git(
    "rev-parse",
    "HEAD",
)

current_parent = git(
    "show",
    "-s",
    "--format=%P",
    "HEAD",
)

if current_head == EXPECTED_DECISION0144:
    fail(
        "BOUNDED_GOVERNANCE_ADOPTION_AUTHORIZATION_NOT_COMMITTED"
    )

if current_parent != EXPECTED_DECISION0144:
    fail(
        "CURRENT_HEAD_IS_NOT_IMMEDIATE_SUCCESSOR_OF_DECISION0144"
    )

if (
    git(
        "rev-parse",
        "HEAD:" + RECORD_REL,
    )
    != EXPECTED_RECORD_TREE
):
    fail(
        "COMPLETED_REVIEW_RECORD_GIT_TREE"
    )

git(
    "cat-file",
    "-e",
    "HEAD:" + THIS_AUTH_REL,
)

if git(
    "status",
    "--porcelain=v1",
    "--untracked-files=all",
):
    fail(
        "REPOSITORY_NOT_CLEAN"
    )

auth = json.loads(
    AUTH.read_text(encoding="utf-8")
)

if auth["authorization_type"] != \
    "PRE_BOUNDED_GOVERNANCE_ADOPTION_ONLY":
    fail("AUTHORIZATION_TYPE")

if auth["status"] != \
    "AUTHORIZED_NOT_YET_ADOPTED":
    fail("AUTHORIZATION_STATUS")

review = auth["completed_human_review_binding"]

if review["completed_review_packet_sha256"] != EXPECTED_REVIEW_SHA:
    fail("REVIEW_PACKET_SHA")

if review["human_review_completed"] is not True:
    fail("HUMAN_REVIEW_COMPLETED")

if review["human_review_recorded_in_repository"] is not True:
    fail("HUMAN_REVIEW_RECORDED")

for key in (
    "RBCA01","RBCA02","RBCA03","RBCA04",
    "RBCA05","RBCA06","RBCA07","RBCA08",
):
    if review[key] != "PASS":
        fail("REVIEW_RESULT|" + key)

if review["pass_count"] != 8:
    fail("PASS_COUNT")

if review["revision_required_count"] != 0:
    fail("REVISION_COUNT")

if review["fail_count"] != 0:
    fail("FAIL_COUNT")

if review["overall_review_decision"] != EXPECTED_OVERALL:
    fail("OVERALL_DECISION")

if review["reviewer_decision_synthesized"] is not False:
    fail("REVIEWER_DECISION_SYNTHESIS")

if review["reviewer_identity_synthesized"] is not False:
    fail("REVIEWER_IDENTITY_SYNTHESIS")

bounded = auth[
    "bounded_result_authorized_for_governance_adoption"
]

if bounded["study_result"] != "FURTHER_EVIDENCE_REQUIRED":
    fail("BOUNDED_RESULT")

if bounded["requirement_count"] != 17:
    fail("REQUIREMENT_COUNT")

if bounded["semantic_unit_count"] != 109:
    fail("SEMANTIC_UNIT_COUNT")

if bounded["schema_v2_property_path_count"] != 171:
    fail("SCHEMA_PATH_COUNT")

if bounded["historical_carrier_pair_count"] != 18639:
    fail("PAIR_COUNT")

if bounded["requirement_to_semantic_unit_crosswalk_identified"] is not False:
    fail("CROSSWALK_STATE")

if bounded["admissible_exact_count"] != 0:
    fail("ADMISSIBLE_EXACT")

if bounded["admissible_composite_count"] != 0:
    fail("ADMISSIBLE_COMPOSITE")

if bounded["no_admissible_carrier_proven_count"] != 0:
    fail("NO_ADMISSIBLE_CARRIER_COUNT")

if bounded["unresolved_count"] != 17:
    fail("UNRESOLVED_COUNT")

for key in (
    "schema_v2_losslessness_proven",
    "carrier_admissibility_resolved",
    "positive_mapping_proven",
    "negative_mapping_impossibility_proven",
    "whole_v4_exhaustiveness_proven",
):
    if bounded[key] is not False:
        fail("UNEXPECTED_TECHNICAL_CLAIM|" + key)

for key, value in auth["explicit_non_authorizations"].items():
    if value is not False:
        fail("UNEXPECTED_OPERATIONAL_AUTHORIZATION|" + key)

for key, value in auth["retired_verifier_policy"].items():
    if value is not False:
        fail("RETIRED_A02_RERUN_ALLOWED|" + key)

manifest = json.loads(
    MANIFEST.read_text(encoding="utf-8")
)

gov = manifest["governance_state"]

if gov["human_review_completed"] is not True:
    fail("MANIFEST_HUMAN_REVIEW_COMPLETED")

if gov["human_review_recorded_in_repository"] is not True:
    fail("MANIFEST_HUMAN_REVIEW_RECORDED")

if gov["study_governance_adopted"] is not False:
    fail("STUDY_ALREADY_GOVERNANCE_ADOPTED")

if gov["study_governance_adoption_authorized"] is not False:
    fail("PREVIOUS_GOVERNANCE_ADOPTION_AUTHORIZATION")

technical = manifest["reviewed_technical_result"]

if technical["author_candidate_outcome"] != "FURTHER_EVIDENCE_REQUIRED":
    fail("MANIFEST_TECHNICAL_OUTCOME")

if technical["unresolved_count"] != 17:
    fail("MANIFEST_UNRESOLVED_COUNT")

accounting = json.loads(
    ACCOUNTING.read_text(encoding="utf-8")
)

if accounting["approved_bounded_technical_outcome"] != \
    "FURTHER_EVIDENCE_REQUIRED":
    fail("ACCOUNTING_TECHNICAL_OUTCOME")

if accounting["study_governance_adopted"] is not False:
    fail("ACCOUNTING_GOVERNANCE_ADOPTED")

p = subprocess.run(
    ["python3", str(RECORD_SAFE)],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    check=False,
)

if p.returncode != 0:
    fail(
        "COMPLETED_REVIEW_RECORD_SAFE_VERIFIER|"
        + p.stdout
        + p.stderr
    )

for marker in (
    "COMPLETED_RBCA01_RBCA08_HUMAN_REVIEW_RECORD_V1=PASS",
    "HUMAN_REVIEW_COMPLETED=YES",
    "HUMAN_REVIEW_RECORDED_IN_REPOSITORY=YES",
    "RBCA01_RBCA08_PASS_COUNT=8",
    "OVERALL_REVIEW_DECISION="
    + EXPECTED_OVERALL,
    "REVIEWED_TECHNICAL_OUTCOME=FURTHER_EVIDENCE_REQUIRED",
    "UNRESOLVED_COUNT=17",
    "CARRIER_ADMISSIBILITY_RESOLVED=NO",
    "POSITIVE_MAPPING_PROVEN=NO",
    "NEGATIVE_MAPPING_IMPOSSIBILITY_PROVEN=NO",
    "WHOLE_V4_EXHAUSTIVENESS_PROVEN=NO",
    "STUDY_GOVERNANCE_ADOPTED=NO",
    "STUDY_GOVERNANCE_ADOPTION_AUTHORIZED=NO",
    "DECISION_0143_A02_STATE=PERMANENTLY_RETIRED",
    "RETIRED_A02_VERIFIERS_EXECUTED=NO",
):
    if marker not in p.stdout:
        fail(
            "COMPLETED_REVIEW_SAFE_MARKER|"
            + marker
        )

print(
    "BOUNDED_GOVERNANCE_ADOPTION_AUTHORIZATION=PASS"
)

print(
    "CURRENT_CHECKPOINT_ROLE="
    "IMMEDIATE_SUCCESSOR_OF_DECISION0144"
)

print(
    "CURRENT_HEAD_PARENT_DECISION0144_BINDING=PASS"
)

print(
    "HUMAN_REVIEW_COMPLETED=YES"
)

print(
    "HUMAN_REVIEW_RECORDED_IN_REPOSITORY=YES"
)

print(
    "RBCA01_RBCA08_PASS_COUNT=8"
)

print(
    "OVERALL_REVIEW_DECISION="
    + EXPECTED_OVERALL
)

print(
    "BOUNDED_TECHNICAL_OUTCOME=FURTHER_EVIDENCE_REQUIRED"
)

print(
    "REQUIREMENT_TO_SEMANTIC_UNIT_CROSSWALK_IDENTIFIED=NO"
)

print(
    "ADMISSIBLE_EXACT_COUNT=0"
)

print(
    "ADMISSIBLE_COMPOSITE_COUNT=0"
)

print(
    "NO_ADMISSIBLE_CARRIER_PROVEN_COUNT=0"
)

print(
    "UNRESOLVED_COUNT=17"
)

print(
    "STUDY_GOVERNANCE_ADOPTED=NO"
)

print(
    "CARRIER_ADMISSIBILITY_RESOLVED=NO"
)

print(
    "POSITIVE_MAPPING_PROVEN=NO"
)

print(
    "NEGATIVE_MAPPING_IMPOSSIBILITY_PROVEN=NO"
)

print(
    "WHOLE_V4_EXHAUSTIVENESS_PROVEN=NO"
)

print(
    "OPERATIONAL_MAPPING_AUTHORIZED=NO"
)

print(
    "SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO"
)

print(
    "CURL_JSON_AUTHORIZED=NO"
)

print(
    "ANALYZER_AUTHORIZED=NO"
)

print(
    "BASELINE_AUTHORIZED=NO"
)

print(
    "REPAIR_AUTHORIZED=NO"
)

print(
    "RETIRED_A02_VERIFIERS_EXECUTED=NO"
)

print(
    "VERIFIER_LIFECYCLE="
    "ONE_FINAL_RUN_IMMEDIATELY_BEFORE_BOUNDED_GOVERNANCE_ADOPTION_AUTHORING_THEN_PERMANENT_RETIREMENT"
)
