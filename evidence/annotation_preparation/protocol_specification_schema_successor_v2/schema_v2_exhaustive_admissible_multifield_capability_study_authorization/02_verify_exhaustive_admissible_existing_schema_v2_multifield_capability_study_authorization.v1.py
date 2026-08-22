#!/usr/bin/env python3

import json
from pathlib import Path

REPO = Path(
    "/openbayes/home/semanticverify-fuzz-research"
)

HERE = Path(__file__).resolve().parent

AUTH = HERE / \
    "01_exhaustive_admissible_existing_schema_v2_multifield_capability_study_authorization.v1.json"

TARGET = (
    REPO
    / "evidence/annotation_preparation/protocol_specification_schema_successor_v2"
    / "schema_v2_exhaustive_admissible_multifield_capability_study_v1"
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
] != "PRE_CAPABILITY_STUDY_AUTHORING_ONLY":
    fail("AUTHORIZATION_TYPE")

if a[
    "status"
] != "AUTHORIZED_TO_AUTHOR_EXHAUSTIVE_ADMISSIBLE_EXISTING_SCHEMA_V2_MULTIFIELD_CAPABILITY_STUDY_V1_ONLY":
    fail("STATUS")

human = a[
    "human_review_basis"
]

if human[
    "corrective_assessment_v2_human_approved"
] is not True:
    fail("V2_HUMAN_APPROVAL")

if human[
    "human_approved_current_outcome"
] != "FURTHER_EVIDENCE_REQUIRED":
    fail("HUMAN_APPROVED_CURRENT_OUTCOME")

if human[
    "schema_successor_required_human_approved"
] is not False:
    fail("SUCCESSOR_REQUIRED_APPROVAL")

if human[
    "no_successor_required_with_proven_v2_mapping_human_approved"
] is not False:
    fail("NO_SUCCESSOR_APPROVAL")

study = a[
    "authorized_study"
]

if study[
    "must_be_machine_checkable"
] is not True:
    fail("MACHINE_CHECK_REQUIREMENT")

if study[
    "must_not_presuppose_outcome"
] is not True:
    fail("OUTCOME_NEUTRALITY")

reqs = a[
    "mandatory_exact_v4_losslessness_requirements"
]

if len(reqs) != 17:
    fail("LOSSLESSNESS_REQUIREMENT_COUNT")

containers = a[
    "mandatory_v4_semantic_containers"
]

if len(containers) != 10:
    fail("SEMANTIC_CONTAINER_COUNT")

scope = a[
    "mandatory_rule_and_exit_scope"
]

if scope["rule_record_count"] != 64:
    fail("RULE_COUNT")

if scope["exit_obligation_count"] != 3:
    fail("EXIT_OBLIGATION_COUNT")

if scope["rules_with_enforcement_count"] != 64:
    fail("ENFORCEMENT_COVERAGE")

if scope["distinct_enforcement_value_count"] != 15:
    fail("ENFORCEMENT_VALUE_COUNT")

if scope["representation_policy_field_count"] != 10:
    fail("REPRESENTATION_POLICY_FIELD_COUNT")

if len(
    scope[
        "known_unresolved_representation_policy_assertions"
    ]
) != 3:
    fail("UNRESOLVED_POLICY_COUNT")

carrier = a[
    "existing_schema_v2_carrier_scope"
]

if carrier[
    "must_examine_multi_field_compositions"
] is not True:
    fail("MULTIFIELD_COMPOSITION_REQUIREMENT")

if carrier[
    "must_not_limit_search_to_same_named_properties"
] is not True:
    fail("SAME_NAMED_ONLY_PROHIBITION")

if set(
    carrier[
        "minimum_carrier_families"
    ]
) != {
    "resource_model",
    "events",
    "semantic_policy",
    "semantic_rules",
    "exit_obligations",
    "semantic_accounting",
    "provenance",
}:
    fail("CARRIER_FAMILY_SET")

admiss = a[
    "admissibility_contract"
]

required_true = (
    "schema_v2_validity_required",
    "native_structured_schema_v2_carriers_required",
    "semantically_related_carriers_only",
    "deterministic_forward_encoding_required",
    "deterministic_exact_reverse_reconstruction_required",
    "all_required_v4_semantics_must_be_recoverable",
    "field_level_accounting_required",
    "forward_accounting_required",
    "reverse_accounting_required",
    "unknown_first_class_must_be_preserved",
    "four_verdict_contract_must_be_preserved",
    "normative_strength_must_not_be_silently_strengthened_or_weakened",
    "resource_centered_semantics_must_be_preserved",
    "synthetic_protocol_events_must_not_be_invented",
    "ownership_membership_path_return_and_set_valued_semantics_must_be_preserved",
)

for key in required_true:
    if admiss[key] is not True:
        fail("ADMISSIBILITY_REQUIRED_TRUE|" + key)

required_false = (
    "opaque_blob_packing_allowed",
    "free_text_as_hidden_semantic_storage_allowed",
    "external_lookup_required_for_reverse_reconstruction_allowed",
    "unrelated_field_repurposing_allowed",
    "semantic_accounting_as_substitute_for_semantic_storage_allowed",
    "lossy_normalization_allowed",
    "silent_semantic_strengthening_allowed",
    "silent_semantic_weakening_allowed",
)

for key in required_false:
    if admiss[key] is not False:
        fail("ADMISSIBILITY_REQUIRED_FALSE|" + key)

outcomes = set(
    a[
        "permitted_study_outcomes"
    ]
)

if outcomes != {
    "PROVEN_ADMISSIBLE_EXISTING_SCHEMA_V2_MAPPING_PATH_AVAILABLE",
    "PROVEN_NO_ADMISSIBLE_EXISTING_SCHEMA_V2_MAPPING_PATH_UNDER_REVIEWED_CONSTRAINTS",
    "FURTHER_EVIDENCE_REQUIRED",
}:
    fail("OUTCOME_SET")

gov = a[
    "outcome_governance"
]

for key in (
    "study_result_is_author_candidate_only",
    "independent_human_technical_review_required_before_governance_use",
    "positive_result_does_not_authorize_positive_mapping_contract",
    "negative_result_does_not_authorize_schema_successor",
    "further_evidence_result_does_not_authorize_schema_successor",
    "no_outcome_authorizes_curl_json",
    "no_outcome_authorizes_analyzer",
):
    if gov[key] is not True:
        fail("OUTCOME_GOVERNANCE|" + key)

allowed = a[
    "allowed_analysis_artifacts"
]

if allowed[
    "analysis_only_mapping_witness"
] is not True:
    fail("ANALYSIS_WITNESS_REQUIRED")

if allowed[
    "operational_positive_mapping_contract"
] is not False:
    fail("OPERATIONAL_MAPPING_NOT_ALLOWED")

if allowed[
    "canonical_curl_json"
] is not False:
    fail("CANONICAL_CURL_NOT_ALLOWED")

if TARGET.exists():
    fail("CAPABILITY_STUDY_ALREADY_EXISTS")

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

print("CORRECTIVE_ASSESSMENT_V2_HUMAN_APPROVED=YES")
print("FURTHER_EVIDENCE_REQUIRED_HUMAN_APPROVED=YES")
print("SCHEMA_SUCCESSOR_REQUIRED_HUMAN_APPROVED=NO")

print("EXHAUSTIVE_V2_CAPABILITY_STUDY_AUTHORING_AUTHORIZED=YES")
print("EXHAUSTIVE_V2_CAPABILITY_STUDY_AUTHORED=NO")

print("LOSSLESSNESS_REQUIREMENT_COUNT=17")
print("V4_SEMANTIC_CONTAINER_COUNT=10")
print("V4_RULE_RECORD_COUNT=64")
print("V4_EXIT_OBLIGATION_COUNT=3")
print("DISTINCT_ENFORCEMENT_VALUE_COUNT=15")
print("UNRESOLVED_REPRESENTATION_POLICY_ASSERTION_COUNT=3")

print("ALL_SEMANTICALLY_RELATED_SCHEMA_V2_CARRIERS_MUST_BE_EXAMINED=YES")
print("MULTIFIELD_COMPOSITIONS_MUST_BE_EXAMINED=YES")
print("SAME_NAMED_PROPERTY_ONLY_REASONING_ALLOWED=NO")

print("DETERMINISTIC_FORWARD_ENCODING_REQUIRED=YES")
print("DETERMINISTIC_EXACT_REVERSE_RECONSTRUCTION_REQUIRED=YES")
print("COLLISION_ANALYSIS_REQUIRED=YES")
print("SEMANTIC_NONINTERFERENCE_REQUIRED=YES")

print("ANALYSIS_ONLY_MAPPING_WITNESS_ALLOWED=YES")
print("OPERATIONAL_POSITIVE_MAPPING_CONTRACT_AUTHORIZED=NO")

print("SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO")
print("SCHEMA_VERSION_PRESELECTED=NO")
print("SCHEMA_V3_CREATED=NO")
print("POSITIVE_MAPPING_AUTHORIZED=NO")
print("CURL_JSON_CREATED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")

print("DECISION_0083_CAPABILITY_STUDY_AUTHORIZATION=PASS")
print("IMPORTANT=THIS_VERIFIER_IS_PRE_CAPABILITY_STUDY_AUTHORING_ONLY")
