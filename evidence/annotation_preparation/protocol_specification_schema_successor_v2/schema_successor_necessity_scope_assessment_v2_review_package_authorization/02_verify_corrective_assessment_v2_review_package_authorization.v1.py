#!/usr/bin/env python3

import json
from pathlib import Path

REPO = Path(
    "/openbayes/home/semanticverify-fuzz-research"
)

HERE = Path(__file__).resolve().parent

AUTH = HERE / \
    "01_corrective_assessment_v2_review_package_authorization.v1.json"

TARGET = (
    REPO
    / "evidence/annotation_preparation/protocol_specification_schema_successor_v2"
    / "schema_successor_necessity_scope_assessment_v2_review_package_v1"
)

def fail(msg):
    print("FAIL|" + msg)
    raise SystemExit(1)

a = json.loads(
    AUTH.read_text(
        encoding="utf-8"
    )
)

if a[
    "authorization_type"
] != "PRE_CORRECTIVE_V2_REVIEW_PACKAGE_AUTHORING_ONLY":
    fail("AUTHORIZATION_TYPE")

if a[
    "status"
] != "AUTHORIZED_TO_AUTHOR_INDEPENDENT_HUMAN_TECHNICAL_REVIEW_PACKAGE_FOR_CORRECTIVE_ASSESSMENT_V2_ONLY":
    fail("STATUS")

subject = a[
    "review_subject"
]

if subject[
    "selected_outcome"
] != "FURTHER_EVIDENCE_REQUIRED":
    fail("SELECTED_OUTCOME")

if subject[
    "selected_outcome_is_human_approved"
] is not False:
    fail("OUTCOME_HUMAN_APPROVAL_STATE")

pred = a[
    "predecessor_review_binding"
]

if pred[
    "assessment_v1_overall_human_decision"
] != "REVISION_REQUIRED":
    fail("V1_REVIEW_DECISION")

if pred[
    "historical_pass_results_must_not_be_rewritten"
] is not True:
    fail("HISTORICAL_PASS_IMMUTABILITY")

if pred[
    "historical_pass_results_do_not_automatically_approve_v2"
] is not True:
    fail("HISTORICAL_PASS_AUTO_APPROVAL")

required = a[
    "mandatory_review_items"
]

if set(required) != {
    "CVR01",
    "CVR02",
    "CVR03",
    "CVR04",
    "CVR05",
    "CVR06",
    "CVR07",
    "CVR08",
}:
    fail("MANDATORY_REVIEW_ITEM_SET")

if len(required) != 8:
    fail("MANDATORY_REVIEW_ITEM_COUNT")

if set(
    a["allowed_item_decisions"]
) != {
    "PASS",
    "REVISION_REQUIRED",
    "FAIL",
}:
    fail("ITEM_DECISION_SET")

if set(
    a["allowed_overall_decisions"]
) != {
    "APPROVE_CORRECTIVE_SCHEMA_SUCCESSOR_NECESSITY_SCOPE_ASSESSMENT_V2",
    "REVISION_REQUIRED",
    "FAIL",
}:
    fail("OVERALL_DECISION_SET")

req = a[
    "review_requirements"
]

if req[
    "independent_human_technical_reviewer_required"
] is not True:
    fail("HUMAN_REVIEW_REQUIREMENT")

if req[
    "synthetic_reviewer_decision_allowed"
] is not False:
    fail("SYNTHETIC_REVIEW_ALLOWED")

if req[
    "initial_blank_reviewer_packet_required"
] is not True:
    fail("INITIAL_BLANK_PACKET")

if req[
    "initial_blank_verifier_maximum_successful_runs"
] != 1:
    fail("BLANK_VERIFIER_RUN_LIMIT")

if TARGET.exists():
    fail("REVIEW_PACKAGE_ALREADY_EXISTS")

for key, value in a[
    "explicit_non_authorizations"
].items():
    if value is not False:
        fail("NONAUTH|" + key)

for key, value in a[
    "retired_verifier_constraints"
].items():
    if value is not False:
        fail("RETIRED_VERIFIER|" + key)

for forbidden in (
    "config/protocol_specifications/curl.json",
    "config/annotation/curl_positive_v4_to_v2_mapping_contract.v1.json",
    "config/annotation/curl_positive_v4_to_successor_mapping_contract.v1.json",
    "config/schemas/protocol_specification.v3.schema.json",
):
    if (
        REPO /
        forbidden
    ).exists():
        fail(
            "FORBIDDEN_ARTIFACT|"
            + forbidden
        )

print("CORRECTIVE_ASSESSMENT_V2_BINDING=PASS")
print("CORRECTIVE_V2_SELECTED_OUTCOME=FURTHER_EVIDENCE_REQUIRED")
print("CORRECTIVE_V2_SELECTED_OUTCOME_HUMAN_APPROVED=NO")

print("MANDATORY_REVIEW_ITEM_COUNT=8")
print("CVR01_TO_CVR08_DEFINED=YES")

print("INDEPENDENT_HUMAN_TECHNICAL_REVIEW_REQUIRED=YES")
print("SYNTHETIC_REVIEWER_DECISION_ALLOWED=NO")

print("HISTORICAL_SR01_SR03_SR04_SR05_SR06_PASS_RESULTS_PRESERVED=YES")
print("HISTORICAL_PASS_RESULTS_AUTOMATICALLY_APPROVE_V2=NO")

print("CORRECTIVE_V2_REVIEW_PACKAGE_AUTHORING_AUTHORIZED=YES")
print("EXHAUSTIVE_V2_CAPABILITY_STUDY_AUTHORIZED=NO")
print("SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO")
print("SCHEMA_VERSION_PRESELECTED=NO")
print("POSITIVE_MAPPING_AUTHORIZED=NO")
print("CURL_JSON_CREATED=NO")

print("DECISION_0080_CORRECTIVE_V2_REVIEW_PACKAGE_AUTHORIZATION=PASS")
print("IMPORTANT=THIS_VERIFIER_IS_PRE_CORRECTIVE_V2_REVIEW_PACKAGE_AUTHORING_ONLY")
