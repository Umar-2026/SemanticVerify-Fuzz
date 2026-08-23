#!/usr/bin/env python3

import json
from pathlib import Path

REPO = Path(
    "/openbayes/home/semanticverify-fuzz-research"
)

HERE = Path(__file__).resolve().parent

AUTH = (
    HERE
    / "01_semantic_role_relation_formalization_v1_authorization.json"
)

FORMALIZATION = (
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
] != "AUTHORIZED_TO_AUTHOR_SCHEMA_V2_SEMANTIC_ROLE_RELATION_FORMALIZATION_V1_ONLY":
    fail("STATUS")

if a[
    "authorization_type"
] != "PRE_SEMANTIC_ROLE_RELATION_FORMALIZATION_AUTHORING_ONLY":
    fail("AUTHORIZATION_TYPE")

basis = a[
    "governance_basis"
]

if basis[
    "capability_study_v1_human_approved"
] is not True:
    fail("CAPABILITY_STUDY_APPROVAL")

if basis[
    "further_evidence_required_human_approved"
] is not True:
    fail("FER_APPROVAL")

for key in (
    "positive_existing_v2_mapping_path_proven",
    "negative_existing_v2_mapping_path_impossibility_proven",
    "admissible_composition_exhaustiveness_established",
):
    if basis[key] is not False:
        fail("OVERCLAIM|" + key)

scope = a[
    "authorized_evidence_scope"
]

if scope[
    "v4_semantic_unit_count"
] != 109:
    fail("SEMANTIC_UNIT_COUNT")

if scope[
    "v4_leaf_field_count"
] != 531:
    fail("LEAF_FIELD_COUNT")

if scope[
    "v4_field_class_count"
] != 57:
    fail("FIELD_CLASS_COUNT")

if scope[
    "schema_v2_property_path_count"
] != 171:
    fail("SCHEMA_PROPERTY_PATH_COUNT")

if scope[
    "schema_v2_open_unconstrained_string_path_count"
] != 59:
    fail("OPEN_STRING_CARRIER_COUNT")

if scope[
    "human_review_required_before_governance_use"
] is not True:
    fail("HUMAN_REVIEW_REQUIREMENT")

required_classes = {
    "SEMANTICALLY_RELATED",
    "NOT_SEMANTICALLY_RELATED",
    "UNRESOLVED",
}

if set(
    scope[
        "required_pair_classifications"
    ]
) != required_classes:
    fail("PAIR_CLASSIFICATIONS")

for key, value in a[
    "admissibility_constraints"
].items():
    if value is not True:
        fail(
            "ADMISSIBILITY_CONSTRAINT|" + key
        )

for key, value in a[
    "formalization_nonclaims"
].items():
    if value is not False:
        fail(
            "FORMALIZATION_NONCLAIM|" + key
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

if FORMALIZATION.exists():
    fail(
        "SEMANTIC_ROLE_RELATION_FORMALIZATION_ALREADY_EXISTS"
    )

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

print("CAPABILITY_STUDY_V1_HUMAN_APPROVED=YES")
print("FURTHER_EVIDENCE_REQUIRED_HUMAN_APPROVED=YES")

print("POSITIVE_EXISTING_V2_MAPPING_PATH_PROVEN=NO")
print("NEGATIVE_EXISTING_V2_MAPPING_PATH_IMPOSSIBILITY_PROVEN=NO")
print("ADMISSIBLE_COMPOSITION_EXHAUSTIVENESS_ESTABLISHED=NO")

print("SEMANTIC_ROLE_RELATION_FORMALIZATION_V1_AUTHORIZED=YES")
print("SEMANTIC_ROLE_RELATION_FORMALIZATION_V1_AUTHORED=NO")

print("V4_SEMANTIC_UNIT_COUNT=109")
print("V4_LEAF_FIELD_COUNT=531")
print("V4_FIELD_CLASS_COUNT=57")
print("SCHEMA_V2_PROPERTY_PATH_COUNT=171")
print("SCHEMA_V2_OPEN_STRING_CARRIER_COUNT=59")

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

print("DECISION_0087_PRE_RECORD_VERIFIER_RERUN=NO")
print("INITIAL_BLANK_CSR01_CSR08_VERIFIER_RERUN=NO")
print("DECISION_0085_PRE_REVIEW_PACKAGE_VERIFIER_RERUN=NO")
print("DECISION_0083_PRE_STUDY_VERIFIER_RERUN=NO")

print("DECISION_0089_SEMANTIC_ROLE_RELATION_AUTHORIZATION=PASS")
print("IMPORTANT=THIS_VERIFIER_IS_PRE_SEMANTIC_ROLE_RELATION_FORMALIZATION_AUTHORING_ONLY")
