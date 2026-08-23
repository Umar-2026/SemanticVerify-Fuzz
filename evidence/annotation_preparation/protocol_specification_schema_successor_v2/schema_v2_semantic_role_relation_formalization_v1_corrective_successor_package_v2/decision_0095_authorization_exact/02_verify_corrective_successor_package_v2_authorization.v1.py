#!/usr/bin/env python3

import hashlib
import json
from collections import Counter
from pathlib import Path

REPO = Path(
    "/openbayes/home/semanticverify-fuzz-research"
)

HERE = Path(__file__).resolve().parent

AUTH = (
    HERE
    / "01_corrective_successor_package_v2_authorization.v1.json"
)

BASE = (
    REPO
    / "evidence/annotation_preparation/protocol_specification_schema_successor_v2"
)

UNIT = (
    BASE
    / "schema_v2_exhaustive_admissible_multifield_capability_study_v1"
    / "02_v4_semantic_unit_inventory.v1.json"
)

CARRIER = (
    BASE
    / "schema_v2_exhaustive_admissible_multifield_capability_study_v1"
    / "03_schema_v2_carrier_inventory.v1.json"
)

MATRIX = (
    BASE
    / "schema_v2_exhaustive_admissible_multifield_capability_study_v1"
    / "04_candidate_multifield_composition_matrix.v1.json"
)

FORM = (
    BASE
    / "schema_v2_semantic_role_relation_formalization_v1"
)

RELATION = (
    FORM
    / "02_v4_field_class_to_schema_v2_property_path_relation.v1.json"
)

REPORT = (
    FORM
    / "04_schema_v2_semantic_role_relation_formalization.v1.md"
)

COMPLETED = (
    BASE
    / "schema_v2_semantic_role_relation_formalization_v1_completed_human_review_v1"
    / "02_completed_srr01_srr08_human_review_record.v1.json"
)

SUCCESSOR = (
    BASE
    / "schema_v2_semantic_role_relation_formalization_v1_corrective_successor_package_v2"
)

EXPECTED_SHA = {
    UNIT:
        "2b39f5625658e41aeb906a1db8a4a472d9265dc3654572e60374827f0ce7fa7d",

    CARRIER:
        "0f32fb87e1396da8c37e3f74c41059560338346ae54f29df0c2d38d72deb1d6d",

    MATRIX:
        "c064cfa8c7143b537dc3bb54b8af353f56bafba3e415e7ccdb2c17efaff30d45",

    RELATION:
        "239e6492faca3bb6da0c79abdb980470e2ea76690fc1f081562ccdbf7f303a32",

    REPORT:
        "7b71d98c63afabc6d3b5eaf72f07e0ee2e4a6707520d80032a9d51b9540878d4",

    COMPLETED:
        "d6b0d58c6adf3ba6b5b2ad848b4ef5469c213e8b37b0bd66284ed2b437b6b106",
}

def fail(msg):
    print(
        "FAIL|" + msg
    )
    raise SystemExit(1)

def sha(path):
    if not path.is_file():
        fail(
            "MISSING|" + str(path)
        )

    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()

for path, expected in EXPECTED_SHA.items():
    actual = sha(path)

    if actual != expected:
        fail(
            "SHA|"
            + str(path)
            + "|ACTUAL="
            + actual
        )

if SUCCESSOR.exists():
    fail(
        "SUCCESSOR_PACKAGE_ALREADY_EXISTS"
    )

a = json.loads(
    AUTH.read_text(
        encoding="utf-8"
    )
)

if a[
    "status"
] != "AUTHORIZED_FOR_EVIDENCE_ONLY_CORRECTIVE_SUCCESSOR_PACKAGE_V2_AUTHORING":
    fail(
        "AUTHORIZATION_STATUS"
    )

if a[
    "authorization_type"
] != "PRE_CORRECTIVE_SUCCESSOR_PACKAGE_AUTHORING_ONLY":
    fail(
        "AUTHORIZATION_TYPE"
    )

review = a[
    "source_human_review"
]

if review[
    "overall_decision"
] != "REVISION_REQUIRED":
    fail(
        "SOURCE_REVIEW_OVERALL"
    )

if review[
    "focused_revision_items"
] != [
    "SRR02",
    "SRR04",
    "SRR05",
    "SRR08",
]:
    fail(
        "FOCUSED_REVISION_ITEMS"
    )

if review[
    "carried_forward_pass_items"
] != [
    "SRR01",
    "SRR03",
    "SRR06",
    "SRR07",
]:
    fail(
        "CARRIED_FORWARD_PASS_ITEMS"
    )

completed = json.loads(
    COMPLETED.read_text(
        encoding="utf-8"
    )
)

if completed[
    "completed_review"
][
    "overall_decision"
] != "REVISION_REQUIRED":
    fail(
        "COMPLETED_REVIEW_OVERALL"
    )

expected_decisions = {
    "SRR01": "PASS",
    "SRR02": "REVISION_REQUIRED",
    "SRR03": "PASS",
    "SRR04": "REVISION_REQUIRED",
    "SRR05": "REVISION_REQUIRED",
    "SRR06": "PASS",
    "SRR07": "PASS",
    "SRR08": "REVISION_REQUIRED",
}

if completed[
    "completed_review"
][
    "decisions"
] != expected_decisions:
    fail(
        "COMPLETED_REVIEW_DECISIONS"
    )

unit = json.loads(
    UNIT.read_text(
        encoding="utf-8"
    )
)

carrier = json.loads(
    CARRIER.read_text(
        encoding="utf-8"
    )
)

matrix = json.loads(
    MATRIX.read_text(
        encoding="utf-8"
    )
)

relation = json.loads(
    RELATION.read_text(
        encoding="utf-8"
    )
)

if len(unit.get("leaf_fields", [])) != 531:
    fail("SOURCE_LEAF_COUNT")

if len(unit.get("semantic_units", [])) != 109:
    fail("SOURCE_UNIT_COUNT")

if len(carrier.get("property_paths", [])) != 171:
    fail("SOURCE_PATH_COUNT")

if len(matrix.get("field_class_analysis", [])) != 57:
    fail("SOURCE_FIELD_CLASS_COUNT")

if len(matrix.get("unit_analysis", [])) != 109:
    fail("SOURCE_UNIT_ANALYSIS_COUNT")

rows = relation.get(
    "relations",
    [],
)

if len(rows) != 9747:
    fail(
        "RELATION_ROW_COUNT"
    )

lexical = [
    row
    for row in rows
    if row.get(
        "reviewed_lexical_only_candidate"
    ) is True
]

counts = Counter(
    row.get(
        "classification"
    )
    for row in lexical
)

if len(lexical) != 125:
    fail("LEXICAL_TOTAL")

if counts.get(
    "SEMANTICALLY_RELATED",
    0,
) != 0:
    fail("LEXICAL_RELATED")

if counts.get(
    "UNRESOLVED",
    0,
) != 120:
    fail("LEXICAL_UNRESOLVED")

if counts.get(
    "NOT_SEMANTICALLY_RELATED",
    0,
) != 5:
    fail("LEXICAL_NEGATIVE")

expected_pairs = {
    (
        "EXPLICIT_GLOBAL_CLEANUP_OBLIGATION",
        "$.semantic_accounting.inventory.exit_obligation_count",
    ),
    (
        "cleanup_obligation_effect",
        "$.semantic_accounting.inventory.exit_obligation_count",
    ),
    (
        "dependent_reasoning_policy",
        "$.semantic_accounting.inventory.representation_policy_field_count",
    ),
    (
        "feasible_state_join_policy",
        "$.semantic_accounting.inventory.representation_policy_field_count",
    ),
    (
        "rule_id",
        "$.semantic_accounting.inventory.rule_count",
    ),
}

actual_pairs = {
    (
        row.get("v4_matrix_field_class"),
        row.get("schema_v2_property_path"),
    )
    for row in lexical
    if row.get(
        "classification"
    ) == "NOT_SEMANTICALLY_RELATED"
}

if actual_pairs != expected_pairs:
    fail(
        "FIVE_NEGATIVE_PAIRS"
    )

wrong_sentence = (
    "In particular, 125 lexical-screening-only pairs remain unresolved."
)

if REPORT.read_text(
    encoding="utf-8"
).count(
    wrong_sentence
) != 1:
    fail(
        "ORIGINAL_REPORT_DEFECT_BINDING"
    )

scope = a[
    "required_corrective_scope"
]

if scope[
    "SRR04"
][
    "relation_row_reclassification_authorized"
] is not False:
    fail(
        "RELATION_RECLASSIFICATION_BOUNDARY"
    )

immutability = a[
    "immutability_constraints"
]

for key, value in immutability.items():
    if value is not True:
        fail(
            "IMMUTABILITY|" + key
        )

nonclaims = a[
    "bounded_nonclaims"
]

for key, value in nonclaims.items():
    if value is not False:
        fail(
            "NONCLAIM|" + key
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

print("SOURCE_HUMAN_REVIEW_OVERALL=REVISION_REQUIRED")
print("FOCUSED_REVISION_ITEMS=SRR02,SRR04,SRR05,SRR08")
print("CARRIED_FORWARD_PASS_ITEMS=SRR01,SRR03,SRR06,SRR07")

print("SOURCE_LEAF_FIELD_COUNT=531")
print("SOURCE_SEMANTIC_UNIT_COUNT=109")
print("SOURCE_SCHEMA_V2_PROPERTY_PATH_COUNT=171")
print("SOURCE_MATRIX_FIELD_CLASS_COUNT=57")
print("SOURCE_MATRIX_UNIT_ANALYSIS_COUNT=109")

print("LEXICAL_ONLY_TOTAL=125")
print("LEXICAL_ONLY_SEMANTICALLY_RELATED=0")
print("LEXICAL_ONLY_UNRESOLVED=120")
print("LEXICAL_ONLY_NOT_SEMANTICALLY_RELATED=5")
print("SRR04_RELATION_ROW_RECLASSIFICATION_AUTHORIZED=NO")

print("ORIGINAL_FORMALIZATION_V1_IMMUTABLE=YES")
print("ORIGINAL_9747_RELATION_ROWS_IMMUTABLE=YES")
print("ORIGINAL_REVIEW_PACKAGE_V1_IMMUTABLE=YES")
print("ORIGINAL_REVISION_REQUIRED_REVIEW_IMMUTABLE=YES")

print("OPERATIONAL_POSITIVE_MAPPING_AUTHORIZED=NO")
print("SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO")
print("CURL_JSON_AUTHORIZED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")

print("DECISION_0095_CORRECTIVE_SUCCESSOR_PACKAGE_V2_AUTHORIZATION=PASS")
print("IMPORTANT=THIS_VERIFIER_IS_PRE_CORRECTIVE_SUCCESSOR_PACKAGE_AUTHORING_ONLY")
