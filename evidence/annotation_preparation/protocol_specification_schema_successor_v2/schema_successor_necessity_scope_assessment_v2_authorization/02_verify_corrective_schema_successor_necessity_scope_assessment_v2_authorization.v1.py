#!/usr/bin/env python3

import json
from pathlib import Path

REPO = Path(
    "/openbayes/home/semanticverify-fuzz-research"
)

HERE = Path(__file__).resolve().parent

AUTH = HERE / \
    "01_corrective_schema_successor_necessity_scope_assessment_v2_authorization.v1.json"

TARGET = (
    REPO
    / "evidence/annotation_preparation/protocol_specification_schema_successor_v2"
    / "schema_successor_necessity_scope_assessment_v2"
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
] != "PRE_CORRECTIVE_ASSESSMENT_V2_AUTHORING_ONLY":
    fail("AUTHORIZATION_TYPE")

if a[
    "status"
] != "AUTHORIZED_TO_AUTHOR_CORRECTIVE_SCHEMA_SUCCESSOR_NECESSITY_SCOPE_ASSESSMENT_V2_ONLY":
    fail("STATUS")

pred = a[
    "predecessor_assessment"
]

if pred[
    "human_approved"
] is not False:
    fail("PREDECESSOR_APPROVAL_STATE")

if pred[
    "must_remain_immutable"
] is not True:
    fail("PREDECESSOR_IMMUTABILITY")

review = a[
    "completed_human_review"
]

if review[
    "overall_decision"
] != "REVISION_REQUIRED":
    fail("OVERALL_REVIEW_DECISION")

expected_items = {
    "SR01": "PASS",
    "SR02": "REVISION_REQUIRED",
    "SR03": "PASS",
    "SR04": "PASS",
    "SR05": "PASS",
    "SR06": "PASS",
    "SR07": "REVISION_REQUIRED",
    "SR08": "REVISION_REQUIRED",
}

if review[
    "item_decisions"
] != expected_items:
    fail("ITEM_DECISIONS")

if review[
    "schema_successor_required_human_approved"
] is not False:
    fail("SUCCESSOR_REQUIRED_APPROVAL")

corrective = a[
    "mandatory_corrective_items"
]

if set(corrective) != {
    "CV2_SR02",
    "CV2_SR07",
    "CV2_SR08",
}:
    fail("CORRECTIVE_ITEM_SET")

if corrective[
    "CV2_SR02"
]["current_evidence_supported_outcome"] != "FURTHER_EVIDENCE_REQUIRED":
    fail("SR02_SUPPORTED_OUTCOME")

if corrective[
    "CV2_SR02"
]["stronger_SCHEMA_SUCCESSOR_REQUIRED_outcome_allowed_without_new_exhaustive_capability_argument"] is not False:
    fail("SR02_STRONGER_OUTCOME_BOUNDARY")

if corrective[
    "CV2_SR07"
]["curl_json_materialization_must_remain_after_activation_and_separate_authorization"] is not True:
    fail("SR07_CURL_BOUNDARY")

if corrective[
    "CV2_SR08"
]["required_selected_outcome_for_corrective_assessment_v2"] != "FURTHER_EVIDENCE_REQUIRED":
    fail("SR08_REQUIRED_OUTCOME")

contract = a[
    "mandatory_corrective_v2_conclusion_contract"
]

if contract[
    "selected_outcome_under_current_evidence"
] != "FURTHER_EVIDENCE_REQUIRED":
    fail("CONCLUSION_CONTRACT")

if contract[
    "schema_successor_required_may_not_be_selected_in_corrective_v2"
] is not True:
    fail("SUCCESSOR_REQUIRED_SELECTION_BOUNDARY")

if contract[
    "future_exhaustive_v2_capability_study_may_change_conclusion_only_after_separate_authorization_and_review"
] is not True:
    fail("FUTURE_CAPABILITY_STUDY_BOUNDARY")

sequence = a[
    "mandatory_future_governance_order_if_successor_later_becomes_supported"
]

mapping_index = next(
    (
        i
        for i, item in enumerate(sequence)
        if "positive curl V4-to-successor mapping" in item
    ),
    None,
)

activation_index = next(
    (
        i
        for i, item in enumerate(sequence)
        if item == "Execute successor activation."
    ),
    None,
)

if mapping_index is None or activation_index is None:
    fail("GOVERNANCE_SEQUENCE_REQUIRED_STAGES")

if mapping_index >= activation_index:
    fail("MAPPING_MUST_PRECEDE_ACTIVATION")

if TARGET.exists():
    fail("CORRECTIVE_ASSESSMENT_V2_ALREADY_EXISTS")

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

print("ASSESSMENT_V1_HUMAN_DECISION=REVISION_REQUIRED")
print("ASSESSMENT_V1_HUMAN_APPROVED=NO")
print("SCHEMA_SUCCESSOR_REQUIRED_HUMAN_APPROVED=NO")

print("CORRECTIVE_ITEM_COUNT=3")
print("CORRECTIVE_SR02_REQUIRED=YES")
print("CORRECTIVE_SR07_REQUIRED=YES")
print("CORRECTIVE_SR08_REQUIRED=YES")

print("CORRECTIVE_V2_REQUIRED_SELECTED_OUTCOME=FURTHER_EVIDENCE_REQUIRED")
print("SCHEMA_SUCCESSOR_REQUIRED_SELECTION_ALLOWED_IN_CORRECTIVE_V2=NO")

print("POSITIVE_MAPPING_AND_ROUNDTRIP_REVIEW_MUST_PRECEDE_SUCCESSOR_ACTIVATION=YES")

print("HISTORICAL_SR01_SR03_SR04_SR05_SR06_PASS_RESULTS_PRESERVED=YES")
print("HISTORICAL_PASS_RESULTS_AUTOMATICALLY_APPROVE_V2=NO")

print("CORRECTIVE_ASSESSMENT_V2_AUTHORING_AUTHORIZED=YES")
print("EXHAUSTIVE_V2_CAPABILITY_STUDY_AUTHORIZED=NO")
print("SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO")
print("SCHEMA_VERSION_PRESELECTED=NO")
print("POSITIVE_MAPPING_AUTHORIZED=NO")
print("CURL_JSON_CREATED=NO")

print("DECISION_0078_CORRECTIVE_ASSESSMENT_V2_AUTHORIZATION=PASS")
print("IMPORTANT=THIS_VERIFIER_IS_PRE_CORRECTIVE_ASSESSMENT_V2_AUTHORING_ONLY")
