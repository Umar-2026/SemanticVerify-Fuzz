#!/usr/bin/env python3

import json
from pathlib import Path

REPO = Path(
    "/openbayes/home/semanticverify-fuzz-research"
)

HERE = Path(__file__).resolve().parent

AUTH = HERE / \
    "01_semantic_role_relation_formalization_v1_review_package_authorization.v1.json"

PACKAGE = (
    REPO
    / "evidence/annotation_preparation/protocol_specification_schema_successor_v2"
    / "schema_v2_semantic_role_relation_formalization_v1_review_package_v1"
)

FORM = (
    REPO
    / "evidence/annotation_preparation/protocol_specification_schema_successor_v2"
    / "schema_v2_semantic_role_relation_formalization_v1"
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
    "status"
] != "AUTHORIZED_TO_AUTHOR_INDEPENDENT_HUMAN_TECHNICAL_REVIEW_PACKAGE_V1_ONLY":
    fail("STATUS")

if a[
    "authorization_type"
] != "PRE_REVIEW_PACKAGE_AUTHORING_ONLY":
    fail("AUTHORIZATION_TYPE")

basis = a[
    "governance_basis"
]

if basis[
    "decision_0090_commit"
] != "55cdd77baf2cf9a44789dcc2625edb617dae4011":
    fail("DECISION_0090_COMMIT")

if basis[
    "formalization_status"
] != "AUTHOR_CANDIDATE":
    fail("FORMALIZATION_STATUS")

if basis[
    "formalization_selected_outcome"
] != "PARTIAL_RELATION_FURTHER_EVIDENCE_REQUIRED":
    fail("FORMALIZATION_OUTCOME")

if basis[
    "formalization_selected_outcome_human_approved"
] is not False:
    fail("HUMAN_APPROVAL_PREEXISTS")

if basis[
    "independent_human_technical_review_required"
] is not True:
    fail("HUMAN_REVIEW_REQUIREMENT")

items = a[
    "mandatory_review_items"
]

expected_ids = {
    "SRR01",
    "SRR02",
    "SRR03",
    "SRR04",
    "SRR05",
    "SRR06",
    "SRR07",
    "SRR08",
}

if set(items) != expected_ids:
    fail("MANDATORY_REVIEW_ITEMS")

if a[
    "allowed_item_decisions"
] != [
    "PASS",
    "REVISION_REQUIRED",
    "FAIL",
]:
    fail("ITEM_DECISIONS")

if a[
    "allowed_overall_decisions"
] != [
    "APPROVE_SCHEMA_V2_SEMANTIC_ROLE_RELATION_FORMALIZATION_V1",
    "REVISION_REQUIRED",
    "FAIL",
]:
    fail("OVERALL_DECISIONS")

r = a[
    "review_requirements"
]

required_true = (
    "independent_human_technical_review_required",
    "reviewer_name_must_be_human_supplied",
    "reviewer_confirmation_must_be_human_supplied",
    "reviewer_date_must_be_human_supplied",
    "all_SRR01_through_SRR08_require_explicit_decision",
    "all_PASS_required_for_approval",
    "reviewer_must_not_be_prepopulated_by_authoring_step",
    "human_decision_must_not_be_synthesized",
)

for key in required_true:
    if r[key] is not True:
        fail(
            "REVIEW_REQUIREMENT|" + key
        )

if r[
    "reviewer_role_required"
] != "Spec-Technical-Reviewer-1":
    fail("REVIEWER_ROLE")

bounded = a[
    "approval_if_eventually_granted_is_bounded"
]

if bounded[
    "formalization_v1_may_be_human_approved"
] is not True:
    fail("BOUNDED_STUDY_APPROVAL")

if bounded[
    "PARTIAL_RELATION_FURTHER_EVIDENCE_REQUIRED_may_be_human_approved"
] is not True:
    fail("BOUNDED_OUTCOME_APPROVAL")

for key in (
    "positive_existing_v2_mapping_path_would_be_proven",
    "negative_existing_v2_mapping_impossibility_would_be_proven",
    "admissible_composition_exhaustiveness_would_be_established",
    "operational_positive_mapping_would_be_authorized",
    "schema_successor_authoring_would_be_authorized",
):
    if bounded[key] is not False:
        fail(
            "BOUNDED_OVERCLAIM|" + key
        )

for key, value in a[
    "retired_verifier_constraints"
].items():
    if value is not False:
        fail(
            "RETIRED_VERIFIER|" + key
        )

for key, value in a[
    "explicit_non_authorizations"
].items():
    if value is not False:
        fail(
            "NONAUTH|" + key
        )

if not FORM.is_dir():
    fail("FORMALIZATION_MISSING")

if PACKAGE.exists():
    fail("REVIEW_PACKAGE_ALREADY_EXISTS")

for forbidden in (
    REPO
    / "config/protocol_specifications/curl.json",

    REPO
    / "config/annotation/curl_positive_v4_to_v2_mapping_contract.v1.json",

    REPO
    / "config/annotation/curl_positive_v4_to_successor_mapping_contract.v1.json",

    REPO
    / "config/schemas/protocol_specification.v3.schema.json",
):
    if forbidden.exists():
        fail(
            "FORBIDDEN_ARTIFACT|"
            + str(forbidden)
        )

print("FORMALIZATION_V1_STATUS=AUTHOR_CANDIDATE")
print("FORMALIZATION_SELECTED_OUTCOME=PARTIAL_RELATION_FURTHER_EVIDENCE_REQUIRED")
print("FORMALIZATION_SELECTED_OUTCOME_HUMAN_APPROVED=NO")

print("SRR01_REQUIRED=YES")
print("SRR02_REQUIRED=YES")
print("SRR03_REQUIRED=YES")
print("SRR04_REQUIRED=YES")
print("SRR05_REQUIRED=YES")
print("SRR06_REQUIRED=YES")
print("SRR07_REQUIRED=YES")
print("SRR08_REQUIRED=YES")

print("INDEPENDENT_HUMAN_REVIEW_PACKAGE_V1_AUTHORIZED=YES")
print("INDEPENDENT_HUMAN_REVIEW_PACKAGE_V1_AUTHORED=NO")
print("HUMAN_REVIEW_DECISION_CREATED=NO")
print("HUMAN_REVIEWER_IDENTITY_PREPOPULATED=NO")

print("POSITIVE_EXISTING_V2_MAPPING_PATH_PROVEN=NO")
print("NEGATIVE_EXISTING_V2_MAPPING_PATH_IMPOSSIBILITY_PROVEN=NO")
print("ADMISSIBLE_COMPOSITION_EXHAUSTIVENESS_ESTABLISHED=NO")

print("EXHAUSTIVE_COMPOSITION_ENUMERATION_AUTHORIZED=NO")
print("CONSTRUCTIVE_POSITIVE_MAPPING_WITNESS_AUTHORIZED=NO")
print("OPERATIONAL_POSITIVE_MAPPING_CONTRACT_AUTHORIZED=NO")

print("SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO")
print("SCHEMA_VERSION_PRESELECTED=NO")
print("SCHEMA_V3_CREATED=NO")
print("CURL_JSON_CREATED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")

print("DECISION_0089_PRE_FORMALIZATION_VERIFIER_RERUN=NO")
print("DECISION_0087_PRE_RECORD_VERIFIER_RERUN=NO")
print("INITIAL_BLANK_CSR01_CSR08_VERIFIER_RERUN=NO")
print("DECISION_0085_PRE_REVIEW_PACKAGE_VERIFIER_RERUN=NO")
print("DECISION_0083_PRE_STUDY_VERIFIER_RERUN=NO")

print("DECISION_0091_REVIEW_PACKAGE_AUTHORIZATION=PASS")
print("IMPORTANT=THIS_VERIFIER_IS_PRE_REVIEW_PACKAGE_AUTHORING_ONLY")
