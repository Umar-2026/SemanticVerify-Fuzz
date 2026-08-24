#!/usr/bin/env python3

import hashlib
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent

MATRIX = HERE / \
    "01_semantic_unit_carrier_admissibility_matrix.v1.json"

REQ = HERE / \
    "02_losslessness_requirement_binding_assessment.v1.json"

COH = HERE / \
    "03_cross_unit_coherence_constraint_inventory.v1.json"

ACC = HERE / \
    "04_machine_readable_accounting.v1.json"

A02_OUTPUT = HERE / \
    "06_decision0110_a02_final_output.EXACT_COPY.v1.txt"

CONSUMPTION = HERE / \
    "07_decision0110_a02_consumption_record.v1.json"

SUMS = HERE / \
    "09_semantic_unit_carrier_admissibility_and_requirement_binding_study.v1.SHA256SUMS"

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

matrix = json.loads(
    MATRIX.read_text(
        encoding="utf-8"
    )
)

if matrix["status"] != \
        "AUTHOR_CANDIDATE":
    fail("MATRIX_STATUS")

if matrix[
    "semantic_unit_source"
][
    "semantic_unit_count"
] != 109:
    fail("SEMANTIC_UNIT_COUNT")

if matrix[
    "schema_v2_property_path_count"
] != 171:
    fail("PROPERTY_PATH_COUNT")

if matrix[
    "cartesian_pair_count"
] != 18639:
    fail("CARTESIAN_PAIR_COUNT")

rows = matrix["rows"]

if len(rows) != 18639:
    fail(
        "MATRIX_ROW_COUNT|"
        + str(len(rows))
    )

pairs = [
    (
        row["semantic_unit_id"],
        row["schema_v2_property_path"],
    )
    for row in rows
]

if len(set(pairs)) != 18639:
    fail(
        "MATRIX_PAIR_UNIQUENESS"
    )

units = {
    x[0]
    for x in pairs
}

paths = {
    x[1]
    for x in pairs
}

if len(units) != 109:
    fail(
        "MATRIX_UNIT_DOMAIN"
    )

if len(paths) != 171:
    fail(
        "MATRIX_PATH_DOMAIN"
    )

expected_pairs = {
    (
        unit,
        path,
    )
    for unit in units
    for path in paths
}

if set(pairs) != expected_pairs:
    fail(
        "MATRIX_CARTESIAN_COVERAGE"
    )

counts = Counter(
    row["classification"]
    for row in rows
)

if counts != Counter({
    "UNRESOLVED":
        18639,
}):
    fail(
        "MATRIX_CLASSIFICATION_COUNTS|"
        + repr(dict(counts))
    )

for row in rows:
    if row[
        "losslessness_witness"
    ] is not False:
        fail(
            "PREMATURE_LOSSLESSNESS_WITNESS"
        )

    if row[
        "operational_mapping_authority"
    ] is not False:
        fail(
            "PREMATURE_OPERATIONAL_MAPPING"
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
    "unique_authoritative_17_item_inventory_bound"
] is not False:
    fail(
        "PREMATURE_REQUIREMENT_INVENTORY"
    )

records = req["records"]

if len(records) != 17:
    fail(
        "REQUIREMENT_RECORD_COUNT"
    )

if [
    x["requirement_index"]
    for x in records
] != list(range(1, 18)):
    fail(
        "REQUIREMENT_INDEX_DOMAIN"
    )

for rec in records:
    if rec[
        "binding_status"
    ] != "UNRESOLVED_SOURCE_BINDING":
        fail(
            "UNEXPECTED_REQUIREMENT_BINDING"
        )

    if rec["requirement_text"] is not None:
        fail(
            "INVENTED_REQUIREMENT_TEXT"
        )

    if rec[
        "requirement_text_invented"
    ] is not False:
        fail(
            "REQUIREMENT_INVENTION_FLAG"
        )

    if rec[
        "requirement_text_reconstructed_from_memory"
    ] is not False:
        fail(
            "REQUIREMENT_MEMORY_RECONSTRUCTION"
        )

coh = json.loads(
    COH.read_text(
        encoding="utf-8"
    )
)

if coh[
    "accepted_explicit_cross_unit_constraint_count"
] != 0:
    fail(
        "UNSUPPORTED_CROSS_UNIT_CONSTRAINT"
    )

if coh[
    "accepted_explicit_cross_unit_constraints"
] != []:
    fail(
        "UNSUPPORTED_CROSS_UNIT_LIST"
    )

if coh[
    "complete_cross_unit_constraint_inventory_proven"
] is not False:
    fail(
        "PREMATURE_COHERENCE_COMPLETENESS"
    )

if coh[
    "whole_v4_composition_enumeration_performed"
] is not False:
    fail(
        "PREMATURE_COMPOSITION_ENUMERATION"
    )

acc = json.loads(
    ACC.read_text(
        encoding="utf-8"
    )
)

if acc["status"] != \
        "AUTHOR_CANDIDATE":
    fail(
        "ACCOUNTING_STATUS"
    )

if acc["global_outcome"] != \
        "FURTHER_EVIDENCE_REQUIRED":
    fail(
        "GLOBAL_OUTCOME"
    )

uc = acc[
    "semantic_unit_carrier_domain"
]

if uc[
    "pair_count_observed"
] != 18639:
    fail(
        "ACCOUNTING_PAIR_COUNT"
    )

if uc[
    "unresolved_count"
] != 18639:
    fail(
        "ACCOUNTING_UNRESOLVED_COUNT"
    )

if uc[
    "unit_level_admissibility_resolved"
] is not False:
    fail(
        "PREMATURE_ADMISSIBILITY_RESOLUTION"
    )

rb = acc[
    "requirement_provenance_binding"
]

if rb["bound_count"] != 0:
    fail(
        "ACCOUNTING_REQUIREMENT_BOUND_COUNT"
    )

if rb[
    "unresolved_source_binding_count"
] != 17:
    fail(
        "ACCOUNTING_REQUIREMENT_UNRESOLVED_COUNT"
    )

bounded = acc[
    "bounded_findings"
]

for key in (
    "positive_existing_v2_mapping_witness_identified",
    "negative_existing_v2_mapping_impossibility_proven",
    "whole_v4_admissible_composition_exhaustiveness_established",
):
    if bounded[key] is not False:
        fail(
            "UNSUPPORTED_TECHNICAL_CLAIM|"
            + key
        )

for key, value in acc[
    "governance_nonclaims"
].items():
    if value is not False:
        fail(
            "UNEXPECTED_GOVERNANCE_PERMISSION|"
            + key
        )

cons = json.loads(
    CONSUMPTION.read_text(
        encoding="utf-8"
    )
)

if cons[
    "final_run_result"
] != "PASS":
    fail(
        "A02_FINAL_RESULT"
    )

if cons[
    "verifier_state_after_run"
] != "PERMANENTLY_RETIRED":
    fail(
        "A02_NOT_RETIRED"
    )

if cons[
    "rerun_authorized"
] is not False:
    fail(
        "A02_RERUN_AUTHORIZED"
    )

if cons[
    "must_never_be_rerun"
] is not True:
    fail(
        "A02_RERUN_GUARD"
    )

if sha(A02_OUTPUT) != \
        cons["final_output_sha256"]:
    fail(
        "A02_OUTPUT_SHA"
    )

if A02_OUTPUT.stat().st_size != \
        cons["final_output_size_bytes"]:
    fail(
        "A02_OUTPUT_SIZE"
    )

if (
    "SEMANTIC_UNIT_CARRIER_AND_REQUIREMENT_BINDING_STUDY_AUTHORING_AUTHORIZATION=PASS"
    not in A02_OUTPUT.read_text(
        encoding="utf-8"
    )
):
    fail(
        "A02_PASS_MARKER"
    )

if SUMS.is_file():
    lines = [
        line
        for line in SUMS.read_text(
            encoding="utf-8"
        ).splitlines()
        if line.strip()
    ]

    if len(lines) != 8:
        fail(
            "CHECKSUM_ENTRY_COUNT|"
            + str(len(lines))
        )

    for line in lines:
        digest, rel = line.split(
            None,
            1,
        )

        rel = rel.strip().lstrip("*")

        target = HERE / rel

        if sha(target) != digest:
            fail(
                "CHECKSUM|" + rel
            )

print("SEMANTIC_UNIT_COUNT=109")
print("SCHEMA_V2_PROPERTY_PATH_COUNT=171")
print("UNIT_CARRIER_CARTESIAN_PAIR_COUNT=18639")
print("UNIT_CARRIER_PAIR_UNIQUENESS=PASS")
print("UNIT_CARRIER_CARTESIAN_COVERAGE=PASS")

print("UNIT_CARRIER_CANDIDATE_ADMISSIBLE_COUNT=0")
print("UNIT_CARRIER_NOT_ADMISSIBLE_COUNT=0")
print("UNIT_CARRIER_UNRESOLVED_COUNT=18639")

print("LOSSLESSNESS_REQUIREMENT_COUNT_IN_SCOPE=17")
print("REQUIREMENT_BOUND_COUNT=0")
print("REQUIREMENT_UNRESOLVED_SOURCE_BINDING_COUNT=17")
print("INVENTED_REQUIREMENT_TEXT=NO")

print(
    "CROSS_UNIT_COHERENCE_SCREENING_HIT_COUNT="
    + str(coh["screening_hit_count"])
)

print("ACCEPTED_EXPLICIT_CROSS_UNIT_CONSTRAINT_COUNT=0")
print("WHOLE_V4_COMPOSITION_ENUMERATION_PERFORMED=NO")

print("GLOBAL_OUTCOME=FURTHER_EVIDENCE_REQUIRED")
print("STUDY_STATUS=AUTHOR_CANDIDATE")
print("INDEPENDENT_HUMAN_REVIEW_REQUIRED=YES")
print("STUDY_GOVERNANCE_ADOPTED=NO")

print("POSITIVE_EXISTING_V2_MAPPING_PROVEN=NO")
print("NEGATIVE_EXISTING_V2_MAPPING_IMPOSSIBILITY_PROVEN=NO")
print("WHOLE_V4_ADMISSIBLE_COMPOSITION_EXHAUSTIVENESS_PROVEN=NO")

print("OPERATIONAL_MAPPING_AUTHORIZED=NO")
print("SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO")
print("CURL_JSON_AUTHORIZED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")

print("DECISION_0110_A02_STATE=PERMANENTLY_RETIRED")
print("DECISION_0110_A02_EXECUTED_BY_SAFE_VERIFIER=NO")

print(
    "SEMANTIC_UNIT_CARRIER_ADMISSIBILITY_AND_REQUIREMENT_BINDING_STUDY_V1=PASS"
)
