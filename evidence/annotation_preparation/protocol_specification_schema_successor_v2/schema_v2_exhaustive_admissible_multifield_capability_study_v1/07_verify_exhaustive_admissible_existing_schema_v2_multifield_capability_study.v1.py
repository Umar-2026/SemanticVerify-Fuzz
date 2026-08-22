#!/usr/bin/env python3

import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(
    "/openbayes/home/semanticverify-fuzz-research"
)

BASE = (
    REPO
    / "evidence/annotation_preparation/protocol_specification_schema_successor_v2"
)

HERE = Path(__file__).resolve().parent

S01 = HERE / \
    "01_exhaustive_admissible_existing_schema_v2_multifield_capability_study.v1.json"

S02 = HERE / \
    "02_v4_semantic_unit_inventory.v1.json"

S03 = HERE / \
    "03_schema_v2_carrier_inventory.v1.json"

S04 = HERE / \
    "04_candidate_multifield_composition_matrix.v1.json"

S05 = HERE / \
    "05_exhaustive_admissible_existing_schema_v2_multifield_capability_study.v1.md"

S06 = HERE / \
    "06_pre_study_authorization_verifier_consumed.v1"

SCHEMA = REPO / \
    "config/schemas/protocol_specification.v2.schema.json"

V4 = REPO / \
    "config/annotation/curl_technical_protocol_working_draft.v4.json"

AUTH = (
    BASE
    / "schema_v2_exhaustive_admissible_multifield_capability_study_authorization"
    / "01_exhaustive_admissible_existing_schema_v2_multifield_capability_study_authorization.v1.json"
)

PROOF = (
    BASE
    / "schema_v2_residual_losslessness_insufficiency_proof_v1"
    / "01_residual_schema_v2_losslessness_insufficiency_proof.v1.json"
)

REVIEW = (
    BASE
    / "schema_successor_necessity_scope_assessment_v2_human_review_v1"
    / "06_completed_corrective_assessment_v2_human_review_record.v1.json"
)

EXPECTED = {
    SCHEMA:
        "c6ebb5ef2214c4168283f9009d1f7ce6e88d2ff928853fe6a57ed1f7521c6956",

    V4:
        "e17ae2ea5a70bdd790c946eb4b89ca37368d749cd7463159e69514d88a50cea8",

    AUTH:
        "a8ca219ee246c99c5d3c6ef2771eda7ec4fad2532358baf0cd592c1b00e6eab3",

    PROOF:
        "400f6806217f50b79d17ec77e41683d9077f64e07c63e5421c8b1922b49aaff0",

    REVIEW:
        "d6d1142315f3830abfd2f5d33ca4fff120d1c814d07f80b1b4eb6c96ae0378c1",
}


def fail(msg):
    print("FAIL|" + msg)
    raise SystemExit(1)


def sha(path):
    if not path.is_file():
        fail("MISSING|" + str(path))

    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()


for path, expected in EXPECTED.items():
    if sha(path) != expected:
        fail(
            "IMMUTABLE_INPUT_SHA|"
            + str(path)
        )

for required in (
    S01, S02, S03, S04, S05, S06,
):
    if not required.is_file():
        fail(
            "STUDY_ARTIFACT_MISSING|"
            + required.name
        )

study = json.loads(
    S01.read_text(
        encoding="utf-8"
    )
)

units = json.loads(
    S02.read_text(
        encoding="utf-8"
    )
)

carriers = json.loads(
    S03.read_text(
        encoding="utf-8"
    )
)

matrix = json.loads(
    S04.read_text(
        encoding="utf-8"
    )
)

v4 = json.loads(
    V4.read_text(
        encoding="utf-8"
    )
)

if study["status"] != "AUTHOR_CANDIDATE":
    fail("STATUS")

if study[
    "selected_outcome"
] != "FURTHER_EVIDENCE_REQUIRED":
    fail("SELECTED_OUTCOME")

if study[
    "selected_outcome_human_approved"
] is not False:
    fail("SELECTED_OUTCOME_HUMAN_APPROVAL")

if len(
    study[
        "mandatory_losslessness_requirements"
    ]
) != 17:
    fail("LOSSLESSNESS_REQUIREMENT_COUNT")

inv = study["inventory_results"]

expected_counts = {
    "v4_semantic_container_count": 10,
    "v4_semantic_unit_count": 109,
    "v4_field_class_count": 57,
    "v4_rule_count": 64,
    "v4_exit_obligation_count": 3,
    "v4_representation_policy_field_count": 10,
    "rules_with_enforcement_count": 64,
    "distinct_enforcement_value_count": 15,
    "schema_v2_property_path_count": 171,
    "schema_v2_distinct_property_name_count": 123,
    "same_named_v4_field_to_schema_property_count": 2,
}

for key, expected in expected_counts.items():
    if inv[key] != expected:
        fail(
            f"COUNT|{key}|ACTUAL={inv[key]}"
        )

if inv[
    "current_rule_only_verdict_to_enforcement_ambiguity_group_count"
] != 2:
    fail("VERDICT_ENFORCEMENT_AMBIGUITY_COUNT")

if inv[
    "current_rule_only_defect_verdict_to_enforcement_ambiguity_group_count"
] != 2:
    fail("DEFECT_VERDICT_ENFORCEMENT_AMBIGUITY_COUNT")

if inv["same_named_matches"] != [
    "effect",
    "rule_id",
]:
    fail("SAME_NAMED_MATCH_SET")

if units[
    "semantic_unit_count"
] != 109:
    fail("SEMANTIC_UNIT_INVENTORY_COUNT")

if len(
    units["semantic_units"]
) != 109:
    fail("SEMANTIC_UNIT_ARRAY_COUNT")

if units[
    "leaf_field_count"
] != len(
    units["leaf_fields"]
):
    fail("LEAF_FIELD_COUNT")

if carriers[
    "property_path_count"
] != 171:
    fail("CARRIER_PATH_COUNT")

if len(
    carriers["property_paths"]
) != 171:
    fail("CARRIER_PATH_ARRAY_COUNT")

if carriers[
    "distinct_property_name_count"
] != 123:
    fail("CARRIER_PROPERTY_NAME_COUNT")

if matrix[
    "field_class_count"
] != 57:
    fail("MATRIX_FIELD_CLASS_COUNT")

if len(
    matrix["field_class_analysis"]
) != 57:
    fail("MATRIX_FIELD_CLASS_ARRAY_COUNT")

if matrix[
    "unit_analysis_count"
] != 109:
    fail("MATRIX_UNIT_ANALYSIS_COUNT")

if len(
    matrix["unit_analysis"]
) != 109:
    fail("MATRIX_UNIT_ANALYSIS_ARRAY_COUNT")

if matrix[
    "all_field_classes_screened"
] is not True:
    fail("FIELD_CLASS_SCREENING")

if matrix[
    "all_semantic_units_screened"
] is not True:
    fail("UNIT_SCREENING")

if matrix[
    "all_mathematically_possible_multifield_combinations_enumerated"
] is not False:
    fail("MATHEMATICAL_COMBINATION_ENUMERATION")

if matrix[
    "all_admissible_semantically_related_compositions_machine_enumerated"
] is not False:
    fail("ADMISSIBLE_COMPOSITION_ENUMERATION")

findings = study[
    "capability_findings"
]

required_true = (
    "all_10_v4_semantic_containers_inventoried",
    "all_109_v4_semantic_units_inventoried",
    "all_v4_leaf_fields_inventoried",
    "all_57_v4_field_classes_screened",
    "all_171_schema_v2_property_paths_inventoried",
    "all_7_required_schema_v2_carrier_families_examined",
    "multi_field_compositions_examined_at_composition_class_level",
)

for key in required_true:
    if findings[key] is not True:
        fail(
            "FINDING_REQUIRED_TRUE|"
            + key
        )

required_false = (
    "same_named_property_absence_treated_as_impossibility",
    "constructive_full_exact_mapping_witness_complete",
    "deterministic_complete_forward_encoding_proven",
    "deterministic_exact_reverse_reconstruction_proven",
    "collision_freedom_for_complete_mapping_proven",
    "semantic_noninterference_for_complete_mapping_proven",
    "negative_exhaustive_elimination_complete",
    "all_admissible_semantically_related_multifield_compositions_machine_enumerated",
    "semantic_role_relation_formalization_complete",
)

for key in required_false:
    if findings[key] is not False:
        fail(
            "FINDING_REQUIRED_FALSE|"
            + key
        )

central = set(
    study[
        "unresolved_exactness_classes"
    ][
        "historically_central"
    ]
)

if not {
    "enforcement",
    "normative_strength_uncertainty_must_not_be_silently_strengthened",
    "resource_centered",
    "synthetic_protocol_events_invented",
}.issubset(central):
    fail("CENTRAL_UNRESOLVED_SET")

logic = study[
    "outcome_logic"
]

if logic[
    "positive_outcome_requirements_satisfied"
] is not False:
    fail("POSITIVE_OUTCOME_STATE")

if logic[
    "negative_outcome_requirements_satisfied"
] is not False:
    fail("NEGATIVE_OUTCOME_STATE")

if logic[
    "exhaustiveness_established"
] is not False:
    fail("EXHAUSTIVENESS_STATE")

if logic[
    "required_outcome_under_decision_0083_contract"
] != "FURTHER_EVIDENCE_REQUIRED":
    fail("OUTCOME_LOGIC")

bindings = study[
    "artifact_bindings"
]

if bindings[
    "semantic_unit_inventory_sha256"
] != sha(S02):
    fail("S02_BINDING")

if bindings[
    "schema_v2_carrier_inventory_sha256"
] != sha(S03):
    fail("S03_BINDING")

if bindings[
    "candidate_multifield_composition_matrix_sha256"
] != sha(S04):
    fail("S04_BINDING")

marker = S06.read_text(
    encoding="utf-8"
).splitlines()

for required_line in (
    "DECISION_0083_PRE_STUDY_AUTHORIZATION_VERIFIER_FINAL_RUN=PASS",
    "CAPABILITY_STUDY_AUTHORING_FOLLOWED_FINAL_RUN=YES",
    "PERMANENTLY_RETIRED_AFTER_CAPABILITY_STUDY_AUTHORING=YES",
    "RERUN_ALLOWED=NO",
):
    if required_line not in marker:
        fail(
            "PRE_STUDY_VERIFIER_CONSUMPTION_MARKER|"
            + required_line
        )

if study[
    "prohibited_evidence_accessed"
] is not False:
    fail("PROHIBITED_EVIDENCE")

for key in (
    "operational_positive_mapping_contract_created",
    "schema_successor_created",
    "schema_v3_created",
    "curl_json_created",
    "analyzer_activity_authorized",
    "baseline_activity_authorized",
    "repair_authorized",
):
    if study[key] is not False:
        fail(
            "UNAUTHORIZED_STATE|"
            + key
        )

for forbidden in (
    REPO / "config/protocol_specifications/curl.json",
    REPO / "config/annotation/curl_positive_v4_to_v2_mapping_contract.v1.json",
    REPO / "config/annotation/curl_positive_v4_to_successor_mapping_contract.v1.json",
    REPO / "config/schemas/protocol_specification.v3.schema.json",
):
    if forbidden.exists():
        fail(
            "FORBIDDEN_ARTIFACT|"
            + str(forbidden)
        )

rules = [
    rule
    for family in (
        "global_runtime_rules",
        "easy_handle_rules",
        "multi_handle_rules",
        "cross_resource_rules",
    )
    for rule in v4[family]
]

enforcement = Counter(
    str(rule["enforcement"])
    for rule in rules
)

if len(rules) != 64:
    fail("RECOMPUTED_RULE_COUNT")

if len(enforcement) != 15:
    fail("RECOMPUTED_ENFORCEMENT_COUNT")

verdict_groups = defaultdict(set)
defect_verdict_groups = defaultdict(set)

for rule in rules:
    if "verdict" in rule:
        verdict_groups[
            str(rule["verdict"])
        ].add(
            str(rule["enforcement"])
        )

    if (
        "defect" in rule
        and "verdict" in rule
    ):
        defect_verdict_groups[
            (
                json.dumps(
                    rule["defect"],
                    sort_keys=True,
                    ensure_ascii=False,
                ),
                str(rule["verdict"]),
            )
        ].add(
            str(rule["enforcement"])
        )

if sum(
    1
    for values in verdict_groups.values()
    if len(values) > 1
) != 2:
    fail("RECOMPUTED_VERDICT_AMBIGUITY")

if sum(
    1
    for values in defect_verdict_groups.values()
    if len(values) > 1
) != 2:
    fail("RECOMPUTED_DEFECT_VERDICT_AMBIGUITY")

print("CAPABILITY_STUDY_V1_EXACT_INPUT_BINDINGS=PASS")
print("V4_SEMANTIC_CONTAINER_COUNT=10")
print("V4_SEMANTIC_UNIT_COUNT=109")
print("V4_FIELD_CLASS_COUNT=57")
print("V4_RULE_COUNT=64")
print("V4_EXIT_OBLIGATION_COUNT=3")
print("V4_REPRESENTATION_POLICY_FIELD_COUNT=10")
print("DISTINCT_ENFORCEMENT_VALUE_COUNT=15")
print("SCHEMA_V2_PROPERTY_PATH_COUNT=171")
print("SCHEMA_V2_DISTINCT_PROPERTY_NAME_COUNT=123")

print("ALL_V4_SEMANTIC_UNITS_INVENTORIED=YES")
print("ALL_SCHEMA_V2_PROPERTY_PATHS_INVENTORIED=YES")
print("ALL_FIELD_CLASSES_SCREENED=YES")
print("MULTIFIELD_COMPOSITION_CLASSES_SCREENED=YES")

print("POSITIVE_EXISTING_V2_MAPPING_PATH_PROVEN=NO")
print("NEGATIVE_EXISTING_V2_MAPPING_PATH_IMPOSSIBILITY_PROVEN=NO")
print("ADMISSIBLE_COMPOSITION_EXHAUSTIVENESS_ESTABLISHED=NO")

print("CAPABILITY_STUDY_SELECTED_OUTCOME=FURTHER_EVIDENCE_REQUIRED")
print("CAPABILITY_STUDY_SELECTED_OUTCOME_HUMAN_APPROVED=NO")

print("DECISION_0083_PRE_STUDY_VERIFIER_PERMANENTLY_RETIRED=YES")
print("DECISION_0083_PRE_STUDY_VERIFIER_RERUN_ALLOWED=NO")

print("OPERATIONAL_POSITIVE_MAPPING_CONTRACT_AUTHORIZED=NO")
print("SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO")
print("SCHEMA_V3_CREATED=NO")
print("CURL_JSON_CREATED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")

print("EXHAUSTIVE_ADMISSIBLE_EXISTING_SCHEMA_V2_MULTIFIELD_CAPABILITY_STUDY_V1=PASS")
