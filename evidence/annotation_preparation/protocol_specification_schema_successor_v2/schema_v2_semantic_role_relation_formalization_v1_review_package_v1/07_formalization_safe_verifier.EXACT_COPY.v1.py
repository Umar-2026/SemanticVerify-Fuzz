#!/usr/bin/env python3

import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]

SUMMARY = HERE / \
    "01_schema_v2_semantic_role_relation_formalization.v1.json"

RELATION = HERE / \
    "02_v4_field_class_to_schema_v2_property_path_relation.v1.json"

TRACE = HERE / \
    "03_v4_semantic_unit_context_and_leaf_traceability.v1.json"

CONSUMED = HERE / \
    "05_pre_formalization_authorization_verifier_consumed.v1"

AUTH = (
    REPO
    / "evidence/annotation_preparation/protocol_specification_schema_successor_v2"
    / "schema_v2_semantic_role_relation_formalization_v1_authorization"
    / "01_semantic_role_relation_formalization_v1_authorization.json"
)

STUDY = (
    REPO
    / "evidence/annotation_preparation/protocol_specification_schema_successor_v2"
    / "schema_v2_exhaustive_admissible_multifield_capability_study_v1"
)

UNIT_INV = STUDY / \
    "02_v4_semantic_unit_inventory.v1.json"

CARRIER_INV = STUDY / \
    "03_schema_v2_carrier_inventory.v1.json"

MATRIX = STUDY / \
    "04_candidate_multifield_composition_matrix.v1.json"

EXPECTED = {
    AUTH:
        "d2e6199f18f9b352992f0a2ee22190e1d173fcf52ae79f9b7c59883c1e4b6594",

    UNIT_INV:
        "2b39f5625658e41aeb906a1db8a4a472d9265dc3654572e60374827f0ce7fa7d",

    CARRIER_INV:
        "0f32fb87e1396da8c37e3f74c41059560338346ae54f29df0c2d38d72deb1d6d",

    MATRIX:
        "c064cfa8c7143b537dc3bb54b8af353f56bafba3e415e7ccdb2c17efaff30d45",
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
            "INPUT_SHA|" + str(path)
        )

summary = json.loads(
    SUMMARY.read_text(
        encoding="utf-8"
    )
)

relation = json.loads(
    RELATION.read_text(
        encoding="utf-8"
    )
)

trace = json.loads(
    TRACE.read_text(
        encoding="utf-8"
    )
)

unit_inv = json.loads(
    UNIT_INV.read_text(
        encoding="utf-8"
    )
)

carrier_inv = json.loads(
    CARRIER_INV.read_text(
        encoding="utf-8"
    )
)

matrix = json.loads(
    MATRIX.read_text(
        encoding="utf-8"
    )
)

# ------------------------------------------------------------
# Reviewed source domains
# ------------------------------------------------------------

if len(unit_inv["leaf_fields"]) != 531:
    fail("SOURCE_LEAF_COUNT")

if len(unit_inv["semantic_units"]) != 109:
    fail("SOURCE_UNIT_COUNT")

if len(matrix["field_class_analysis"]) != 57:
    fail("SOURCE_MATRIX_FIELD_CLASS_COUNT")

if len(matrix["unit_analysis"]) != 109:
    fail("SOURCE_MATRIX_UNIT_COUNT")

if len(carrier_inv["property_paths"]) != 171:
    fail("SOURCE_CARRIER_COUNT")

if carrier_inv["distinct_property_name_count"] != 123:
    fail("SOURCE_PROPERTY_NAME_COUNT")

if carrier_inv["open_unconstrained_string_path_count"] != 59:
    fail("SOURCE_OPEN_STRING_COUNT")

matrix_classes = [
    row["v4_field_class"]
    for row in matrix["field_class_analysis"]
]

carrier_paths = [
    row["path"]
    for row in carrier_inv["property_paths"]
]

if len(set(matrix_classes)) != 57:
    fail("MATRIX_FIELD_CLASS_UNIQUENESS")

if len(set(carrier_paths)) != 171:
    fail("CARRIER_PATH_UNIQUENESS")

unit_fc_union = set()

for unit in unit_inv["semantic_units"]:
    unit_fc_union.update(
        unit.get(
            "field_classes",
            []
        )
    )

if len(unit_fc_union) != 57:
    fail("UNIT_FIELD_CLASS_UNION_COUNT")

if unit_fc_union == set(matrix_classes):
    fail("FIELD_CLASS_DOMAIN_DISTINCTION_LOST")

# ------------------------------------------------------------
# Formalization summary
# ------------------------------------------------------------

if summary["status"] != "AUTHOR_CANDIDATE":
    fail("SUMMARY_STATUS")

if summary[
    "selected_outcome"
] != "PARTIAL_RELATION_FURTHER_EVIDENCE_REQUIRED":
    fail("SELECTED_OUTCOME")

if summary[
    "selected_outcome_human_approved"
] is not False:
    fail("HUMAN_APPROVAL")

if summary[
    "human_review_required_before_governance_use"
] is not True:
    fail("HUMAN_REVIEW_REQUIREMENT")

d = summary[
    "reviewed_domain_accounting"
]

expected_counts = {
    "v4_semantic_container_count": 10,
    "v4_semantic_unit_count": 109,
    "v4_leaf_field_count": 531,
    "v4_matrix_field_class_count": 57,
    "unit_inventory_declared_field_class_union_count": 57,
    "matrix_and_unit_inventory_57_element_domains_equal": False,
    "schema_v2_property_path_count": 171,
    "schema_v2_distinct_property_name_count": 123,
    "schema_v2_open_unconstrained_string_path_count": 59,
    "field_class_to_schema_path_pair_count": 9747,
    "semantically_related_pair_count": 113,
    "not_semantically_related_pair_count": 969,
    "unresolved_pair_count": 8665,
    "lexical_only_pair_count": 125,
    "leaf_to_unit_accounting_complete": True,
    "semantic_unit_context_record_count": 109,
    "matrix_field_class_pair_coverage_complete": True,
    "schema_v2_path_pair_coverage_complete": True,
}

for key, expected in expected_counts.items():
    if d[key] != expected:
        fail(
            "SUMMARY_COUNT|"
            + key
            + "|ACTUAL="
            + repr(d[key])
            + "|EXPECTED="
            + repr(expected)
        )

# ------------------------------------------------------------
# Reconstruct expected conservative relation from reviewed matrix
# ------------------------------------------------------------

carrier_by_path = {
    row["path"]: row
    for row in carrier_inv[
        "property_paths"
    ]
}

curated_pairs = set()
lexical_pairs = set()

for row in matrix[
    "field_class_analysis"
]:
    fc = row[
        "v4_field_class"
    ]

    for p in row.get(
        "curated_semantically_related_candidate_paths",
        [],
    ):
        curated_pairs.add(
            (fc, p)
        )

    for entry in row.get(
        "lexical_screening_candidates_only",
        [],
    ):
        for p in entry.get(
            "schema_paths",
            [],
        ):
            lexical_pairs.add(
                (fc, p)
            )

lexical_only = (
    lexical_pairs
    - curated_pairs
)

expected_classification = {}

for fc in matrix_classes:
    for path in carrier_paths:
        pair = (fc, path)

        if pair in curated_pairs:
            value = "SEMANTICALLY_RELATED"

        elif (
            carrier_by_path[path].get(
                "top_level_family"
            )
            == "semantic_accounting"
        ):
            value = "NOT_SEMANTICALLY_RELATED"

        else:
            value = "UNRESOLVED"

        expected_classification[pair] = value

if len(expected_classification) != 9747:
    fail("EXPECTED_PAIR_DOMAIN")

expected_counter = Counter(
    expected_classification.values()
)

if expected_counter != Counter({
    "SEMANTICALLY_RELATED": 113,
    "NOT_SEMANTICALLY_RELATED": 969,
    "UNRESOLVED": 8665,
}):
    fail(
        "EXPECTED_CLASSIFICATION_COUNTS|"
        + repr(expected_counter)
    )

if len(lexical_only) != 125:
    fail("EXPECTED_LEXICAL_ONLY_COUNT")

# ------------------------------------------------------------
# Verify authored relation is exactly the conservative partition
# ------------------------------------------------------------

rels = relation["relations"]

if len(rels) != 9747:
    fail("RELATION_COUNT")

seen = set()
actual_counter = Counter()
field_coverage = Counter()
path_coverage = Counter()

for row in rels:
    pair = (
        row[
            "v4_matrix_field_class"
        ],
        row[
            "schema_v2_property_path"
        ],
    )

    if pair in seen:
        fail(
            "DUPLICATE_PAIR|"
            + repr(pair)
        )

    seen.add(pair)

    if pair not in expected_classification:
        fail(
            "PAIR_OUTSIDE_REVIEWED_DOMAIN|"
            + repr(pair)
        )

    actual = row[
        "classification"
    ]

    expected = expected_classification[
        pair
    ]

    if actual != expected:
        fail(
            "PAIR_CLASSIFICATION_MISMATCH|"
            + repr(pair)
            + "|ACTUAL="
            + actual
            + "|EXPECTED="
            + expected
        )

    if (
        row[
            "reviewed_lexical_only_candidate"
        ]
        != (
            pair
            in lexical_only
        )
    ):
        fail(
            "LEXICAL_ONLY_FLAG|"
            + repr(pair)
        )

    if (
        row[
            "reviewed_curated_candidate"
        ]
        != (
            pair
            in curated_pairs
        )
    ):
        fail(
            "CURATED_FLAG|"
            + repr(pair)
        )

    actual_counter[
        actual
    ] += 1

    field_coverage[
        pair[0]
    ] += 1

    path_coverage[
        pair[1]
    ] += 1

if seen != set(
    expected_classification
):
    fail(
        "PAIR_DOMAIN_NOT_EXACT"
    )

if actual_counter != expected_counter:
    fail(
        "ACTUAL_CLASSIFICATION_COUNTS"
    )

if any(
    field_coverage[fc] != 171
    for fc in matrix_classes
):
    fail(
        "FIELD_CLASS_COVERAGE"
    )

if any(
    path_coverage[p] != 57
    for p in carrier_paths
):
    fail(
        "PATH_COVERAGE"
    )

# ------------------------------------------------------------
# Verify 531 / 109 traceability
# ------------------------------------------------------------

if trace[
    "reviewed_leaf_fields"
] != unit_inv[
    "leaf_fields"
]:
    fail(
        "LEAF_INVENTORY_NOT_EXACTLY_PRESERVED"
    )

unit_records = trace[
    "semantic_unit_context_records"
]

if len(unit_records) != 109:
    fail(
        "UNIT_TRACE_RECORD_COUNT"
    )

record_by_id = {
    row["unit_id"]: row
    for row in unit_records
}

if set(record_by_id) != {
    row["unit_id"]
    for row in unit_inv[
        "semantic_units"
    ]
}:
    fail(
        "UNIT_TRACE_DOMAIN"
    )

matrix_unit_by_id = {
    row["unit_id"]: row
    for row in matrix[
        "unit_analysis"
    ]
}

for inv in unit_inv[
    "semantic_units"
]:
    uid = inv["unit_id"]
    record = record_by_id[uid]
    ma = matrix_unit_by_id[uid]

    if record[
        "inventory_declared_field_classes"
    ] != inv.get(
        "field_classes",
        [],
    ):
        fail(
            "UNIT_INVENTORY_FIELD_CLASS_TRACE|"
            + uid
        )

    if set(
        record[
            "matrix_unit_analysis_field_classes"
        ]
    ) != set(
        ma.get(
            "field_classes",
            [],
        )
    ):
        fail(
            "UNIT_MATRIX_FIELD_CLASS_TRACE|"
            + uid
        )

    if record[
        "candidate_schema_v2_carrier_families"
    ] != ma.get(
        "candidate_schema_v2_carrier_families",
        [],
    ):
        fail(
            "UNIT_CARRIER_FAMILY_TRACE|"
            + uid
        )

# ------------------------------------------------------------
# Nonclaims
# ------------------------------------------------------------

policy = summary[
    "formalization_policy"
]

for key in (
    "raw_v4_all_scalar_leaf_walk_used_as_domain_authority",
    "two_distinct_57_element_field_class_vocabularies_conflated",
    "absence_from_prior_candidate_matrix_used_as_negative_proof",
    "lexical_only_candidates_promoted_to_related",
    "semantic_accounting_used_as_semantic_storage",
):
    if policy[key] is not False:
        fail(
            "POLICY|" + key
        )

for key, value in summary[
    "author_candidate_interpretation"
].items():
    if value is not False:
        fail(
            "OVERCLAIM|" + key
        )

# ------------------------------------------------------------
# Authorization verifier consumption
# ------------------------------------------------------------

consumed = CONSUMED.read_text(
    encoding="utf-8"
).splitlines()

for required in (
    "DECISION_0089_PRE_FORMALIZATION_AUTHORIZATION_VERIFIER_FINAL_RUN=PASS",
    "FORMALIZATION_AUTHORING_FOLLOWED_FINAL_RUN=YES",
    "PERMANENTLY_RETIRED_AFTER_FORMALIZATION_AUTHORING=YES",
    "RERUN_ALLOWED=NO",
):
    if required not in consumed:
        fail(
            "CONSUMPTION|" + required
        )

# ------------------------------------------------------------
# Forbidden boundaries
# ------------------------------------------------------------

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

print("REVIEWED_V4_LEAF_FIELD_COUNT=531")
print("REVIEWED_V4_SEMANTIC_UNIT_COUNT=109")
print("REVIEWED_MATRIX_FIELD_CLASS_COUNT=57")
print("REVIEWED_SCHEMA_V2_PROPERTY_PATH_COUNT=171")
print("REVIEWED_SCHEMA_V2_DISTINCT_PROPERTY_NAME_COUNT=123")
print("REVIEWED_SCHEMA_V2_OPEN_STRING_PATH_COUNT=59")

print("UNIT_INVENTORY_DECLARED_FIELD_CLASS_UNION_COUNT=57")
print("MATRIX_FIELD_CLASS_ANALYSIS_COUNT=57")
print("TWO_57_ELEMENT_FIELD_CLASS_DOMAINS_EQUAL=NO")
print("FIELD_CLASS_DOMAIN_EQUIVALENCE_ASSERTED=NO")

print("SEMANTIC_ROLE_PAIR_COUNT=9747")
print("SEMANTICALLY_RELATED_PAIR_COUNT=113")
print("NOT_SEMANTICALLY_RELATED_PAIR_COUNT=969")
print("UNRESOLVED_PAIR_COUNT=8665")
print("LEXICAL_ONLY_PAIR_COUNT=125")

print("FIELD_CLASS_PAIR_COVERAGE_COMPLETE=YES")
print("SCHEMA_V2_PATH_PAIR_COVERAGE_COMPLETE=YES")
print("LEAF_TO_UNIT_TRACEABILITY=PASS")
print("SEMANTIC_UNIT_CONTEXT_TRACEABILITY=PASS")

print("RAW_V4_SCALAR_WALK_USED_AS_DOMAIN_AUTHORITY=NO")
print("ABSENCE_FROM_PRIOR_MATRIX_USED_AS_NEGATIVE_PROOF=NO")
print("LEXICAL_ONLY_PAIRS_PROMOTED_TO_RELATED=NO")
print("SEMANTIC_ACCOUNTING_AS_SEMANTIC_STORAGE=NO")

print("FORMALIZATION_SELECTED_OUTCOME=PARTIAL_RELATION_FURTHER_EVIDENCE_REQUIRED")
print("FORMALIZATION_SELECTED_OUTCOME_HUMAN_APPROVED=NO")
print("FORMALIZATION_HUMAN_REVIEW_REQUIRED=YES")

print("POSITIVE_EXISTING_V2_MAPPING_PATH_PROVEN=NO")
print("NEGATIVE_EXISTING_V2_MAPPING_PATH_IMPOSSIBILITY_PROVEN=NO")
print("ADMISSIBLE_COMPOSITION_EXHAUSTIVENESS_ESTABLISHED=NO")

print("DECISION_0089_PRE_FORMALIZATION_VERIFIER_PERMANENTLY_RETIRED=YES")
print("DECISION_0089_PRE_FORMALIZATION_VERIFIER_RERUN_ALLOWED=NO")

print("OPERATIONAL_POSITIVE_MAPPING_CONTRACT_AUTHORIZED=NO")
print("SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO")
print("SCHEMA_VERSION_PRESELECTED=NO")
print("SCHEMA_V3_CREATED=NO")
print("CURL_JSON_CREATED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")

print("CORRECTED_SCHEMA_V2_SEMANTIC_ROLE_RELATION_FORMALIZATION_V1=PASS")
