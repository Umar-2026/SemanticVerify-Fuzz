#!/usr/bin/env python3

import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]

REVIEW = (
    HERE
    / "01_completed_srr01_srr08_human_review.EXACT_COPY.v1.md"
)

RECORD = (
    HERE
    / "02_completed_srr01_srr08_human_review_record.v1.json"
)

PKG = (
    REPO
    / "evidence/annotation_preparation/protocol_specification_schema_successor_v2"
    / "schema_v2_semantic_role_relation_formalization_v1_review_package_v1"
)

EXPECTED_REVIEW_SHA = \
    "4504b8fd74e8bd699fcdb4b600f72f706d429cee7126bc432bfe7adb1b9ba9f1"

EXPECTED_BLANK_SHA = \
    "84aa233232268866aaf9a5b8db673ed1c42e0519c7231162dece7f53a7c4ad3b"

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

if sha(REVIEW) != EXPECTED_REVIEW_SHA:
    fail(
        "COMPLETED_REVIEW_SHA"
    )

if sha(
    PKG
    / "15_semantic_role_relation_formalization_v1_reviewer_packet.BLANK.v1.md"
) != EXPECTED_BLANK_SHA:
    fail(
        "IMMUTABLE_BLANK_PACKET_SHA"
    )

text = REVIEW.read_text(
    encoding="utf-8"
)

expected = {
    "SRR01": "PASS",
    "SRR02": "REVISION_REQUIRED",
    "SRR03": "PASS",
    "SRR04": "REVISION_REQUIRED",
    "SRR05": "REVISION_REQUIRED",
    "SRR06": "PASS",
    "SRR07": "PASS",
    "SRR08": "REVISION_REQUIRED",
}

for rid, expected_decision in expected.items():
    section = re.search(
        rf"^## {rid}\b(?P<body>.*?)(?=^## SRR\d{{2}}\b|^# Overall independent human decision\b)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )

    if not section:
        fail(
            "SECTION|" + rid
        )

    decision = re.search(
        r"^Decision \(PASS / REVISION_REQUIRED / FAIL\):[ \t]*"
        r"(PASS|REVISION_REQUIRED|FAIL)[ \t]*$",
        section.group("body"),
        flags=re.MULTILINE,
    )

    if not decision:
        fail(
            "DECISION|" + rid
        )

    if decision.group(1) != expected_decision:
        fail(
            "DECISION_VALUE|"
            + rid
            + "|"
            + decision.group(1)
        )

overall = re.findall(
    r"^Overall decision "
    r"\(APPROVE_SCHEMA_V2_SEMANTIC_ROLE_RELATION_FORMALIZATION_V1 / "
    r"REVISION_REQUIRED / FAIL\):[ \t]*"
    r"(APPROVE_SCHEMA_V2_SEMANTIC_ROLE_RELATION_FORMALIZATION_V1|"
    r"REVISION_REQUIRED|FAIL)[ \t]*$",
    text,
    flags=re.MULTILINE,
)

if overall != [
    "REVISION_REQUIRED"
]:
    fail(
        "OVERALL_DECISION"
    )

def exact_field(prefix):
    values = [
        line[len(prefix):].strip()
        for line in text.splitlines()
        if line.startswith(prefix)
    ]

    if len(values) != 1:
        fail(
            "FIELD|" + prefix
        )

    return values[0]

if exact_field(
    "Reviewer role:"
) != "Spec-Technical-Reviewer-1":
    fail("REVIEWER_ROLE")

if exact_field(
    "Human reviewer name:"
) != "Abdul Raheem Shahzad":
    fail("REVIEWER_NAME")

if exact_field(
    "Human reviewer signature / recorded confirmation:"
) != "ARS":
    fail("REVIEWER_CONFIRMATION")

if exact_field(
    "Human reviewer date:"
) != "23 / August / 2026":
    fail("REVIEWER_DATE")

for marker in (
    "Only 120 are UNRESOLVED; five lexical-only semantic_accounting pairs are classified NOT_SEMANTICALLY_RELATED.",
    "EXPLICIT_GLOBAL_CLEANUP_OBLIGATION",
    "cleanup_obligation_effect",
    "dependent_reasoning_policy",
    "feasible_state_join_policy",
    "rule_id",
    "original reviewed semantic-unit inventory",
    "carrier inventory",
    "candidate composition matrix",
):
    if marker not in text:
        fail(
            "REQUIRED_FINDING|" + marker
        )

record = json.loads(
    RECORD.read_text(
        encoding="utf-8"
    )
)

if record[
    "status"
] != "COMPLETED_INDEPENDENT_HUMAN_REVIEW_RECORDED":
    fail(
        "RECORD_STATUS"
    )

completed = record[
    "completed_review"
]

if completed[
    "overall_decision"
] != "REVISION_REQUIRED":
    fail(
        "RECORD_OVERALL"
    )

if completed[
    "decisions"
] != expected:
    fail(
        "RECORD_DECISIONS"
    )

if completed[
    "reviewer_name"
] != "Abdul Raheem Shahzad":
    fail(
        "RECORD_REVIEWER_NAME"
    )

if completed[
    "reviewer_confirmation"
] != "ARS":
    fail(
        "RECORD_REVIEWER_CONFIRMATION"
    )

bounded = record[
    "bounded_effect"
]

if bounded[
    "formalization_v1_approved"
] is not False:
    fail(
        "FORMALIZATION_APPROVAL"
    )

if bounded[
    "original_human_review_must_remain_immutable"
] is not True:
    fail(
        "REVIEW_IMMUTABILITY"
    )

if bounded[
    "corrective_work_requires_successor_artifacts"
] is not True:
    fail(
        "SUCCESSOR_REQUIREMENT"
    )

for key in (
    "positive_existing_v2_mapping_path_proven",
    "negative_existing_v2_mapping_impossibility_proven",
    "admissible_composition_exhaustiveness_established",
    "operational_positive_mapping_authorized",
    "schema_successor_authoring_authorized",
    "curl_json_authorized",
    "analyzer_authorized",
    "baseline_authorized",
    "repair_authorized",
):
    if bounded[key] is not False:
        fail(
            "BOUNDED_NONCLAIM|" + key
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

print("SRR01=PASS")
print("SRR02=REVISION_REQUIRED")
print("SRR03=PASS")
print("SRR04=REVISION_REQUIRED")
print("SRR05=REVISION_REQUIRED")
print("SRR06=PASS")
print("SRR07=PASS")
print("SRR08=REVISION_REQUIRED")
print("OVERALL_DECISION=REVISION_REQUIRED")

print("HUMAN_REVIEWER_NAME=Abdul Raheem Shahzad")
print("HUMAN_REVIEWER_CONFIRMATION=ARS")
print("HUMAN_REVIEWER_DATE=23 / August / 2026")

print("LEXICAL_ONLY_TOTAL=125")
print("LEXICAL_ONLY_UNRESOLVED=120")
print("LEXICAL_ONLY_NOT_SEMANTICALLY_RELATED=5")

print("EVIDENCE_PORTABILITY_DEFICIENCY=YES")
print("SELF_CONTAINED_REPRODUCIBILITY_DEFICIENCY=YES")

print("FORMALIZATION_V1_APPROVED=NO")
print("ORIGINAL_HUMAN_REVIEW_IMMUTABLE=YES")
print("ORIGINAL_REVIEW_PACKAGE_V1_IMMUTABLE=YES")
print("CORRECTIVE_WORK_REQUIRES_SUCCESSOR_ARTIFACTS=YES")

print("OPERATIONAL_POSITIVE_MAPPING_AUTHORIZED=NO")
print("SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO")
print("CURL_JSON_AUTHORIZED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")

print("REPOSITORY_COMPLETED_SRR01_SRR08_HUMAN_REVIEW=PASS")
