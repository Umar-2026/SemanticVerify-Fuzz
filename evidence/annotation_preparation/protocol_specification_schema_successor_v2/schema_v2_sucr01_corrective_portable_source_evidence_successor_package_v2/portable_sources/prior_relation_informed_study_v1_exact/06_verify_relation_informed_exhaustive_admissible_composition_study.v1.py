#!/usr/bin/env python3

import hashlib
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]

BASE_REL = (
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2"
)

AUTH_REL = (
    BASE_REL
    + "/schema_v2_relation_informed_exhaustive_"
      "admissible_composition_study_authorization_v1"
)

AUTH = REPO / AUTH_REL

A01 = (
    AUTH
    / "01_relation_informed_exhaustive_admissible_"
      "composition_study_authorization.v1.json"
)

A02 = (
    AUTH
    / "02_verify_relation_informed_exhaustive_admissible_"
      "composition_study_authoring_authorization.v1.py"
)

A03 = (
    AUTH
    / "03_relation_informed_exhaustive_admissible_"
      "composition_study_authorization.v1.SHA256SUMS"
)

S01 = (
    HERE
    / "01_relation_informed_exhaustive_admissible_composition_study.v1.json"
)

S02 = (
    HERE
    / "02_exhaustiveness_accounting.v1.json"
)

S03 = (
    HERE
    / "03_study_report.v1.md"
)

S04 = (
    HERE
    / "04_authorization_verifier_final_output.EXACT_COPY.v1.txt"
)

S05 = (
    HERE
    / "05_authorization_verifier_consumption_record.v1.json"
)

SUMS = (
    HERE
    / "07_relation_informed_exhaustive_admissible_composition_study.v1.SHA256SUMS"
)

EXPECTED = {
    A01:
        "c0370ce7e52c7dfb74e375c1a5885119f5b086be759027dc8ae09d9db80c628d",

    A02:
        "6781df3a0b4fcf1c8bc2ce59b7f017106ce2a158d15e68cf5557781532f77af2",

    A03:
        "949938100623931a3146beefa49fdfa4c6c2cd7eeaeb9249fe19843fb629e15c",
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
            "AUTH_BINDING|" + str(path)
        )

# Authorization Git tree must remain unchanged.
proc = subprocess.run(
    [
        "git",
        "-C",
        str(REPO),
        "rev-parse",
        "HEAD:" + AUTH_REL,
    ],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    check=False,
)

if proc.returncode != 0:
    fail("AUTH_GIT_TREE_LOOKUP")

if proc.stdout.strip() != \
        "6c328a09d81fba674442c2fee07476356c2ca02d":
    fail("AUTH_GIT_TREE_CHANGED")

# IMPORTANT:
# A02 is never executed by this safe verifier.

consumption = json.loads(
    S05.read_text(
        encoding="utf-8"
    )
)

if consumption["final_run_result"] != "PASS":
    fail("A02_FINAL_RUN_RESULT")

if consumption["verifier_state_after_run"] != \
        "PERMANENTLY_RETIRED":
    fail("A02_NOT_RETIRED")

if consumption["rerun_authorized"] is not False:
    fail("A02_RERUN_AUTHORIZED")

if consumption["must_never_be_rerun"] is not True:
    fail("A02_RERUN_GUARD")

if sha(S04) != consumption["final_output_sha256"]:
    fail("A02_FINAL_OUTPUT_SHA")

if S04.stat().st_size != \
        consumption["final_output_size_bytes"]:
    fail("A02_FINAL_OUTPUT_SIZE")

output_text = S04.read_text(
    encoding="utf-8"
)

if (
    "RELATION_INFORMED_EXHAUSTIVE_ADMISSIBLE_COMPOSITION_STUDY_AUTHORING_AUTHORIZATION=PASS"
    not in output_text
):
    fail("A02_FINAL_OUTPUT_PASS_MARKER")

study = json.loads(
    S01.read_text(
        encoding="utf-8"
    )
)

if study["status"] != "AUTHOR_CANDIDATE":
    fail("STUDY_STATUS")

if study["global_outcome"] != \
        "FURTHER_EVIDENCE_REQUIRED":
    fail("GLOBAL_OUTCOME")

bindings = study["approved_input_bindings"]

if bindings["relation_pair_count"] != 9747:
    fail("RELATION_COUNT")

if bindings["matrix_field_class_count"] != 57:
    fail("MATRIX_FIELD_CLASS_COUNT")

if bindings["schema_v2_property_path_count"] != 171:
    fail("SCHEMA_PATH_COUNT")

if bindings["semantic_unit_count"] != 109:
    fail("SEMANTIC_UNIT_COUNT")

if bindings["source_leaf_record_count"] != 531:
    fail("LEAF_COUNT")

if study["relation_classification_totals"] != {
    "SEMANTICALLY_RELATED": 113,
    "NOT_SEMANTICALLY_RELATED": 969,
    "UNRESOLVED": 8665,
}:
    fail("RELATION_TOTALS")

rules = study["admissibility_rules"]

if rules[
    "matrix_and_unit_field_class_vocabularies_equated"
] is not False:
    fail("VOCABULARIES_EQUATED")

if rules["unresolved"] != \
        "NOT_AUTOMATICALLY_POSITIVE":
    fail("UNRESOLVED_POLICY")

if rules["not_semantically_related"] != \
        "EXCLUDED_FROM_ADMISSIBLE_SEMANTIC_STORAGE":
    fail("NEGATIVE_RELATION_POLICY")

units = study["per_semantic_unit_results"]

if len(units) != 109:
    fail("UNIT_RESULT_COUNT")

for row in units:
    if row["outcome"] != "UNRESOLVED":
        fail(
            "UNSUPPORTED_UNIT_OUTCOME|"
            + row["study_unit_id"]
        )

requirements = study[
    "losslessness_requirement_results"
]

if len(requirements) != 17:
    fail("REQUIREMENT_RESULT_COUNT")

technical = study["technical_nonclaims"]

for key in (
    "positive_existing_v2_mapping_witness_identified",
    "negative_existing_v2_mapping_impossibility_proven",
    "whole_v4_admissible_composition_exhaustiveness_established",
    "operational_mapping_authorized",
    "schema_successor_authoring_authorized",
):
    if technical[key] is not False:
        fail(
            "UNSUPPORTED_TECHNICAL_CLAIM|" + key
        )

accounting = study[
    "exhaustiveness_accounting"
]

if accounting[
    "field_class_relation_domain_complete"
] is not True:
    fail("FIELD_CLASS_RELATION_DOMAIN")

if accounting[
    "semantic_unit_inventory_complete"
] is not True:
    fail("SEMANTIC_UNIT_INVENTORY")

if accounting[
    "whole_v4_admissible_composition_universe_proven_complete"
] is not False:
    fail("WHOLE_V4_EXHAUSTIVENESS_OVERCLAIM")

facts = json.loads(
    S02.read_text(
        encoding="utf-8"
    )
)

if facts[
    "relation_domain"
][
    "row_count"
] != 9747:
    fail("ACCOUNTING_RELATION_COUNT")

if facts[
    "traceability_domain"
][
    "semantic_unit_count"
] != 109:
    fail("ACCOUNTING_UNIT_COUNT")

if facts[
    "traceability_domain"
][
    "matrix_and_unit_vocabularies_equated"
] is not False:
    fail("ACCOUNTING_VOCABULARY_MERGE")

# Check study checksum closure when present.
if SUMS.is_file():
    lines = [
        x
        for x in SUMS.read_text(
            encoding="utf-8"
        ).splitlines()
        if x.strip()
    ]

    if len(lines) != 6:
        fail(
            "CHECKSUM_ENTRY_COUNT|"
            + str(len(lines))
        )

    for raw in lines:
        digest, rel = raw.split(
            None,
            1,
        )

        rel = rel.strip().lstrip("*")

        target = HERE / rel

        if sha(target) != digest:
            fail("CHECKSUM|" + rel)

print("DECISION_0102_AUTHORIZATION_BINDING=PASS")
print("A02_FINAL_SUCCESSFUL_RUN_RECORDED=YES")
print("A02_STATE=PERMANENTLY_RETIRED")
print("A02_RERUN_AUTHORIZED=NO")
print("A02_EXECUTED_BY_SAFE_VERIFIER=NO")

print("FIELD_CLASS_RELATION_DOMAIN_ROWS=9747")
print("RELATION_SEMANTICALLY_RELATED=113")
print("RELATION_NOT_SEMANTICALLY_RELATED=969")
print("RELATION_UNRESOLVED=8665")

print("SEMANTIC_UNIT_COUNT=109")
print("LOSSLESSNESS_REQUIREMENT_COUNT_IN_SCOPE=17")
print("MATRIX_AND_UNIT_FIELD_CLASS_VOCABULARIES_EQUATED=NO")

print("FIELD_CLASS_RELATION_DOMAIN_COMPLETE=YES")
print("WHOLE_V4_ADMISSIBLE_COMPOSITION_UNIVERSE_PROVEN_COMPLETE=NO")

print("POSITIVE_EXISTING_V2_MAPPING_WITNESS_IDENTIFIED=NO")
print("NEGATIVE_EXISTING_V2_MAPPING_IMPOSSIBILITY_PROVEN=NO")

print("GLOBAL_OUTCOME=FURTHER_EVIDENCE_REQUIRED")
print("STUDY_STATUS=AUTHOR_CANDIDATE")

print("OPERATIONAL_POSITIVE_MAPPING_AUTHORIZED=NO")
print("SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO")
print("CURL_JSON_AUTHORIZED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")

print("RELATION_INFORMED_EXHAUSTIVE_ADMISSIBLE_COMPOSITION_STUDY_V1=PASS")
