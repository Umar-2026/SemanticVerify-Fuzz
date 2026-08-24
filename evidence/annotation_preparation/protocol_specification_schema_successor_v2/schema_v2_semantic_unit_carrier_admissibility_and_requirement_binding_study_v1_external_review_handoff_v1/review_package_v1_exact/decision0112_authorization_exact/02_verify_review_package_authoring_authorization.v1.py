#!/usr/bin/env python3

import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]

BASE_REL = (
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2"
)

STUDY = (
    REPO
    / BASE_REL
    / "schema_v2_semantic_unit_carrier_admissibility_"
      "and_requirement_binding_study_v1"
)

MATRIX = (
    STUDY
    / "01_semantic_unit_carrier_admissibility_matrix.v1.json"
)

REQ = (
    STUDY
    / "02_losslessness_requirement_binding_assessment.v1.json"
)

COH = (
    STUDY
    / "03_cross_unit_coherence_constraint_inventory.v1.json"
)

ACC = (
    STUDY
    / "04_machine_readable_accounting.v1.json"
)

SAFE = (
    STUDY
    / "08_verify_semantic_unit_carrier_admissibility_and_requirement_binding_study.v1.py"
)

SUMS = (
    STUDY
    / "09_semantic_unit_carrier_admissibility_and_requirement_binding_study.v1.SHA256SUMS"
)

AUTH = (
    HERE
    / "01_review_package_authorization.v1.json"
)

FUTURE_PKG = (
    REPO
    / BASE_REL
    / "schema_v2_semantic_unit_carrier_admissibility_"
      "and_requirement_binding_study_v1_review_package_v1"
)

EXPECTED = {
    MATRIX:
        "44a6e8169f8515921a980cb727e106281f47bbe1a6bc9672e16146bab2832a12",

    REQ:
        "c8c6fd120f7046ac7e747124821796d1a3686be3dcf6ea40e712b96cdd851ee5",

    COH:
        "2b831650ec9d4af78f0a836150e79068846d1c70401251951593f9c9e341eb23",

    ACC:
        "f271db56cdd680f85a14d8fe3d4a4b1e820b1bb5276215bd2ca8cb7486e307db",

    SAFE:
        "4b8c99000699589bc100fd558b7e64fcb70d40139294eb78faafbb4f10584dde",

    SUMS:
        "4a3120241af95c90f935a01c750c88a5d6eda15c513f15b9b377b25b39710795",
}

def fail(msg):
    print("FAIL|" + msg)
    raise SystemExit(1)

def sha(path):
    if not path.is_file():
        fail(
            "MISSING|" + str(path)
        )

    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()

for path, expected in EXPECTED.items():
    if sha(path) != expected:
        fail(
            "SOURCE_BINDING|" + str(path)
        )

proc = subprocess.run(
    [
        "git",
        "-C",
        str(REPO),
        "status",
        "--porcelain=v1",
        "--untracked-files=all",
    ],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    check=False,
)

if proc.returncode != 0:
    fail(
        "GIT_STATUS"
    )

if proc.stdout.strip():
    fail(
        "REPOSITORY_NOT_CLEAN"
    )

if FUTURE_PKG.exists():
    fail(
        "REVIEW_PACKAGE_ALREADY_EXISTS"
    )

matrix = json.loads(
    MATRIX.read_text(
        encoding="utf-8"
    )
)

rows = matrix["rows"]

if len(rows) != 18639:
    fail(
        "MATRIX_ROW_COUNT"
    )

pairs = {
    (
        x["semantic_unit_id"],
        x["schema_v2_property_path"],
    )
    for x in rows
}

if len(pairs) != 18639:
    fail(
        "PAIR_UNIQUENESS"
    )

if len({
    x[0] for x in pairs
}) != 109:
    fail(
        "SEMANTIC_UNIT_COUNT"
    )

if len({
    x[1] for x in pairs
}) != 171:
    fail(
        "PROPERTY_PATH_COUNT"
    )

counts = Counter(
    x["classification"]
    for x in rows
)

if counts != Counter({
    "UNRESOLVED": 18639,
}):
    fail(
        "UNIT_CLASSIFICATION_COUNTS"
    )

req = json.loads(
    REQ.read_text(
        encoding="utf-8"
    )
)

if req[
    "requirement_count_in_scope"
] != 17:
    fail(
        "REQUIREMENT_COUNT"
    )

if req[
    "binding_status_counts"
][
    "BOUND_TO_UNIQUE_AUTHORITATIVE_SOURCE_ITEM"
] != 0:
    fail(
        "BOUND_REQUIREMENTS"
    )

if req[
    "binding_status_counts"
][
    "UNRESOLVED_SOURCE_BINDING"
] != 17:
    fail(
        "UNRESOLVED_REQUIREMENTS"
    )

coh = json.loads(
    COH.read_text(
        encoding="utf-8"
    )
)

if coh[
    "screening_hit_count"
] != 2:
    fail(
        "COHERENCE_SCREENING_HITS"
    )

if coh[
    "accepted_explicit_cross_unit_constraint_count"
] != 0:
    fail(
        "ACCEPTED_CONSTRAINTS"
    )

acc = json.loads(
    ACC.read_text(
        encoding="utf-8"
    )
)

if acc["status"] != \
        "AUTHOR_CANDIDATE":
    fail(
        "STUDY_STATUS"
    )

if acc[
    "global_outcome"
] != "FURTHER_EVIDENCE_REQUIRED":
    fail(
        "GLOBAL_OUTCOME"
    )

auth = json.loads(
    AUTH.read_text(
        encoding="utf-8"
    )
)

if auth["status"] != \
        "AUTHORIZED_FOR_REVIEW_PACKAGE_AUTHORING_ONLY":
    fail(
        "AUTHORIZATION_STATUS"
    )

if auth[
    "required_reviewer_role"
] != "Spec-Technical-Reviewer-1":
    fail(
        "REVIEWER_ROLE"
    )

if sorted(
    auth["review_items"].keys()
) != [
    "SUCR01",
    "SUCR02",
    "SUCR03",
    "SUCR04",
    "SUCR05",
    "SUCR06",
    "SUCR07",
    "SUCR08",
]:
    fail(
        "REVIEW_ITEM_SET"
    )

if auth[
    "allowed_item_decisions"
] != [
    "PASS",
    "REVISION_REQUIRED",
    "FAIL",
]:
    fail(
        "ITEM_DECISIONS"
    )

if auth[
    "allowed_overall_decisions"
] != [
    "APPROVE_SEMANTIC_UNIT_CARRIER_ADMISSIBILITY_AND_REQUIREMENT_BINDING_STUDY_V1",
    "REVISION_REQUIRED",
    "FAIL",
]:
    fail(
        "OVERALL_DECISIONS"
    )

for key, value in auth[
    "explicit_non_authorizations"
].items():
    if value is not False:
        fail(
            "UNEXPECTED_AUTHORIZATION|"
            + key
        )

for key, value in auth[
    "retired_verifier_state"
].items():
    if key == \
            "retired_verifiers_must_not_be_executed":

        if value is not True:
            fail(
                "RETIRED_VERIFIER_POLICY"
            )

    else:
        if value != \
                "PERMANENTLY_RETIRED":
            fail(
                "RETIRED_VERIFIER_STATE|"
                + key
            )

life = auth[
    "authorization_verifier_lifecycle"
]

if life[
    "initial_state"
] != "ACTIVE_UNCONSUMED":
    fail(
        "VERIFIER_INITIAL_STATE"
    )

if life[
    "may_execute_exactly_once_immediately_before_review_package_authoring"
] is not True:
    fail(
        "VERIFIER_LIFECYCLE"
    )

print("DECISION_0111_STUDY_BINDING=PASS")
print("STUDY_STATUS=AUTHOR_CANDIDATE")
print("GLOBAL_OUTCOME=FURTHER_EVIDENCE_REQUIRED")

print("SEMANTIC_UNIT_COUNT=109")
print("SCHEMA_V2_PROPERTY_PATH_COUNT=171")
print("UNIT_CARRIER_CARTESIAN_PAIR_COUNT=18639")
print("UNIT_CARRIER_UNRESOLVED_COUNT=18639")

print("LOSSLESSNESS_REQUIREMENT_COUNT_IN_SCOPE=17")
print("REQUIREMENT_BOUND_COUNT=0")
print("REQUIREMENT_UNRESOLVED_SOURCE_BINDING_COUNT=17")

print("CROSS_UNIT_COHERENCE_SCREENING_HIT_COUNT=2")
print("ACCEPTED_EXPLICIT_CROSS_UNIT_CONSTRAINT_COUNT=0")

print("REVIEW_ITEMS=SUCR01,SUCR02,SUCR03,SUCR04,SUCR05,SUCR06,SUCR07,SUCR08")
print("REQUIRED_REVIEWER_ROLE=Spec-Technical-Reviewer-1")

print("DECISION_0102_A02_STATE=PERMANENTLY_RETIRED")
print("DECISION_0104_A02_STATE=PERMANENTLY_RETIRED")
print("DECISION_0106_A02_STATE=PERMANENTLY_RETIRED")
print("DECISION_0110_A02_STATE=PERMANENTLY_RETIRED")
print("RETIRED_A02_VERIFIERS_EXECUTED=NO")

print("HUMAN_REVIEW_DECISION_EXISTS=NO")
print("STUDY_GOVERNANCE_ADOPTED=NO")

print("OPERATIONAL_MAPPING_AUTHORIZED=NO")
print("SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO")
print("CURL_JSON_AUTHORIZED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")

print("REVIEW_PACKAGE_AUTHORING_AUTHORIZATION=PASS")
print("VERIFIER_LIFECYCLE=ONE_FINAL_RUN_IMMEDIATELY_BEFORE_REVIEW_PACKAGE_AUTHORING_THEN_PERMANENT_RETIREMENT")
