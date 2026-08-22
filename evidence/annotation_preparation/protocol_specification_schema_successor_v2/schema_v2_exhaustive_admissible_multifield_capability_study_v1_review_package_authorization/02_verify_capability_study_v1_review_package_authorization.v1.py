#!/usr/bin/env python3

import json
from pathlib import Path

REPO = Path(
    "/openbayes/home/semanticverify-fuzz-research"
)

HERE = Path(__file__).resolve().parent

AUTH = HERE / \
    "01_capability_study_v1_review_package_authorization.v1.json"

PACKAGE = (
    REPO
    / "evidence/annotation_preparation/protocol_specification_schema_successor_v2"
    / "schema_v2_exhaustive_admissible_multifield_capability_study_v1_review_package_v1"
)

STUDY = (
    REPO
    / "evidence/annotation_preparation/protocol_specification_schema_successor_v2"
    / "schema_v2_exhaustive_admissible_multifield_capability_study_v1"
    / "01_exhaustive_admissible_existing_schema_v2_multifield_capability_study.v1.json"
)

def fail(msg):
    print("FAIL|" + msg)
    raise SystemExit(1)

a = json.loads(
    AUTH.read_text(
        encoding="utf-8"
    )
)

study = json.loads(
    STUDY.read_text(
        encoding="utf-8"
    )
)

if a[
    "authorization_type"
] != "PRE_REVIEW_PACKAGE_AUTHORING_ONLY":
    fail("AUTHORIZATION_TYPE")

if a[
    "status"
] != "AUTHORIZED_TO_AUTHOR_CAPABILITY_STUDY_V1_INDEPENDENT_HUMAN_TECHNICAL_REVIEW_PACKAGE_V1_ONLY":
    fail("STATUS")

subject = a[
    "review_subject"
]

if subject[
    "study_status"
] != "AUTHOR_CANDIDATE":
    fail("STUDY_STATUS")

if subject[
    "selected_outcome"
] != "FURTHER_EVIDENCE_REQUIRED":
    fail("SELECTED_OUTCOME")

if subject[
    "selected_outcome_human_approved"
] is not False:
    fail("SELECTED_OUTCOME_ALREADY_HUMAN_APPROVED")

if study[
    "selected_outcome"
] != "FURTHER_EVIDENCE_REQUIRED":
    fail("BOUND_STUDY_SELECTED_OUTCOME")

if study[
    "selected_outcome_human_approved"
] is not False:
    fail("BOUND_STUDY_HUMAN_APPROVAL_STATE")

items = a[
    "mandatory_review_items"
]

if list(items.keys()) != [
    "CSR01",
    "CSR02",
    "CSR03",
    "CSR04",
    "CSR05",
    "CSR06",
    "CSR07",
    "CSR08",
]:
    fail("CSR01_TO_CSR08_SET")

if a[
    "allowed_item_decisions"
] != [
    "PASS",
    "REVISION_REQUIRED",
    "FAIL",
]:
    fail("ITEM_DECISION_SET")

if a[
    "allowed_overall_decisions"
] != [
    "APPROVE_SCHEMA_V2_CAPABILITY_STUDY_V1",
    "REVISION_REQUIRED",
    "FAIL",
]:
    fail("OVERALL_DECISION_SET")

human = a[
    "human_review_requirements"
]

required_true = (
    "independent_human_technical_review_required",
    "initial_reviewer_packet_must_be_blank",
    "external_writable_manual_review_copy_required",
    "one_time_initial_blank_state_verifier_required",
    "initial_blank_state_verifier_must_never_run_after_reviewer_edit",
)

for key in required_true:
    if human[key] is not True:
        fail(
            "HUMAN_REVIEW_REQUIREMENT|"
            + key
        )

if human[
    "synthetic_reviewer_decision_allowed"
] is not False:
    fail("SYNTHETIC_REVIEWER_DECISION")

if human[
    "one_time_initial_blank_state_verifier_max_successful_run_count"
] != 1:
    fail("INITIAL_BLANK_MAX_RUN_COUNT")

interp = a[
    "review_interpretation_constraints"
]

if interp[
    "approval_would_human_approve_capability_study_v1"
] is not True:
    fail("APPROVAL_INTERPRETATION_STUDY")

if interp[
    "approval_would_human_approve_selected_outcome_further_evidence_required"
] is not True:
    fail("APPROVAL_INTERPRETATION_OUTCOME")

for key in (
    "approval_would_prove_positive_existing_v2_mapping",
    "approval_would_prove_negative_existing_v2_mapping_impossibility",
    "approval_would_establish_admissible_composition_exhaustiveness",
    "approval_would_authorize_positive_mapping_contract",
    "approval_would_authorize_schema_successor",
):
    if interp[key] is not False:
        fail(
            "APPROVAL_OVERCLAIM|"
            + key
        )

if PACKAGE.exists():
    fail("REVIEW_PACKAGE_ALREADY_EXISTS")

for key, value in a[
    "explicit_non_authorizations"
].items():
    if value is not False:
        fail(
            "NONAUTH|"
            + key
        )

for key, value in a[
    "retired_verifier_constraints"
].items():
    if value is not False:
        fail(
            "RETIRED_VERIFIER|"
            + key
        )

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

print("CAPABILITY_STUDY_V1_STATUS=AUTHOR_CANDIDATE")
print("CAPABILITY_STUDY_V1_SELECTED_OUTCOME=FURTHER_EVIDENCE_REQUIRED")
print("CAPABILITY_STUDY_V1_SELECTED_OUTCOME_HUMAN_APPROVED=NO")

print("CSR01_TO_CSR08_DEFINED=YES")
print("MANDATORY_REVIEW_ITEM_COUNT=8")
print("INDEPENDENT_HUMAN_TECHNICAL_REVIEW_REQUIRED=YES")
print("SYNTHETIC_REVIEWER_DECISION_ALLOWED=NO")

print("POSITIVE_EXISTING_V2_MAPPING_PATH_PROVEN=NO")
print("NEGATIVE_EXISTING_V2_MAPPING_PATH_IMPOSSIBILITY_PROVEN=NO")
print("ADMISSIBLE_COMPOSITION_EXHAUSTIVENESS_ESTABLISHED=NO")

print("CAPABILITY_STUDY_V1_REVIEW_PACKAGE_AUTHORING_AUTHORIZED=YES")
print("CAPABILITY_STUDY_V1_REVIEW_PACKAGE_AUTHORED=NO")

print("OPERATIONAL_POSITIVE_MAPPING_CONTRACT_AUTHORIZED=NO")
print("SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO")
print("SCHEMA_VERSION_PRESELECTED=NO")
print("SCHEMA_V3_CREATED=NO")
print("CURL_JSON_CREATED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")

print("DECISION_0083_PRE_STUDY_VERIFIER_RERUN=NO")

print("DECISION_0085_REVIEW_PACKAGE_AUTHORIZATION=PASS")
print("IMPORTANT=THIS_VERIFIER_IS_PRE_CAPABILITY_STUDY_V1_REVIEW_PACKAGE_AUTHORING_ONLY")
