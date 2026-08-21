#!/usr/bin/env python3

import collections
import hashlib
import json
from pathlib import Path

REPO = Path(
    "/openbayes/home/semanticverify-fuzz-research"
)

HERE = Path(__file__).resolve().parent

PROOF = HERE / \
    "01_residual_schema_v2_losslessness_insufficiency_proof.v1.json"

SUMMARY = HERE / \
    "02_residual_schema_v2_losslessness_insufficiency_proof.v1.md"

def fail(x):
    print("FAIL|" + x)
    raise SystemExit(1)

def digest(path):
    if not path.is_file():
        fail("MISSING|" + str(path))

    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()

p = json.loads(
    PROOF.read_text(
        encoding="utf-8"
    )
)

if p["status"] != \
   "AUTHOR_CANDIDATE_AWAITING_INDEPENDENT_HUMAN_TECHNICAL_REVIEW":
    fail("STATUS")

inputs = p["exact_inputs"]

for item in inputs.values():
    path = REPO / item["path"]

    if digest(path) != item["sha256"]:
        fail("INPUT_SHA|" + item["path"])

v4 = json.loads(
    (
        REPO /
        inputs["curl_technical_working_draft_v4"]["path"]
    ).read_text(
        encoding="utf-8"
    )
)

schema = json.loads(
    (
        REPO /
        inputs["active_schema_v2"]["path"]
    ).read_text(
        encoding="utf-8"
    )
)

rules = [
    x
    for family in (
        "global_runtime_rules",
        "easy_handle_rules",
        "multi_handle_rules",
        "cross_resource_rules",
    )
    for x in v4[family]
]

if len(rules) != 64:
    fail("RULE_COUNT")

if sum("enforcement" in x for x in rules) != 64:
    fail("ENFORCEMENT_COVERAGE")

enforcement_values = {
    x["enforcement"]
    for x in rules
}

if len(enforcement_values) != 15:
    fail("ENFORCEMENT_VALUE_COUNT")

raw = json.dumps(
    schema,
    sort_keys=True
).lower()

if "enforcement" in raw:
    fail("EXPLICIT_ENFORCEMENT_CARRIER")

by_verdict = collections.defaultdict(set)

for x in rules:
    by_verdict[
        x.get(
            "verdict",
            "<NO_EXPLICIT_VERDICT>"
        )
    ].add(
        x["enforcement"]
    )

if sum(
    len(v) > 1
    for v in by_verdict.values()
) != 3:
    fail("VERDICT_AMBIGUITY")

by_dv = collections.defaultdict(set)

for x in rules:
    by_dv[
        (
            x.get(
                "defect",
                "<NO_DEFECT>"
            ),
            x.get(
                "verdict",
                "<NO_EXPLICIT_VERDICT>"
            ),
        )
    ].add(
        x["enforcement"]
    )

if sum(
    len(v) > 1
    for v in by_dv.values()
) != 4:
    fail("DEFECT_VERDICT_AMBIGUITY")

expected_gaps = {
    "normative_strength_uncertainty_must_not_be_silently_strengthened":
        "normative_strength",

    "resource_centered":
        "resource_centered",

    "synthetic_protocol_events_invented":
        "synthetic_protocol_events",
}

actual_gap_fields = {
    x["field"]
    for x in p[
        "residual_gap_R2_representation_policy"
    ]["unresolved_fields"]
}

if actual_gap_fields != set(expected_gaps):
    fail("POLICY_GAP_SET")

for field, token in expected_gaps.items():
    if token in raw:
        fail(
            "POLICY_GAP_NO_LONGER_PRESENT|"
            + field
        )

r1 = p[
    "residual_gap_R1_enforcement_semantics"
]

if r1["v4_rule_record_count"] != 64:
    fail("PROOF_R1_RULE_COUNT")

if r1["rules_with_enforcement_field"] != 64:
    fail("PROOF_R1_ENFORCEMENT_COVERAGE")

if r1["distinct_enforcement_value_count"] != 15:
    fail("PROOF_R1_ENFORCEMENT_VALUES")

if r1["explicit_v2_enforcement_carrier_present"] is not False:
    fail("PROOF_R1_EXPLICIT_CARRIER")

conclusion = p["candidate_conclusion"]

if conclusion[
    "residual_schema_v2_insufficiency_under_existing_contract"
] is not True:
    fail("CANDIDATE_CONCLUSION")

if conclusion[
    "exact_positive_v4_to_v2_mapping_currently_justified"
] is not False:
    fail("POSITIVE_MAPPING_CONCLUSION")

if conclusion[
    "schema_successor_authoring_currently_authorized"
] is not False:
    fail("SCHEMA_SUCCESSOR_AUTHORIZATION")

if conclusion[
    "independent_human_technical_review_required"
] is not True:
    fail("HUMAN_REVIEW_REQUIREMENT")

for key, value in p[
    "explicit_non_claims"
].items():
    if value is not False:
        fail(
            "NONCLAIM|"
            + key
        )

if (
    REPO /
    "config/protocol_specifications/curl.json"
).exists():
    fail("CURL_JSON_EXISTS")

if (
    REPO /
    "config/annotation/curl_positive_v4_to_v2_mapping_contract.v1.json"
).exists():
    fail("POSITIVE_MAPPING_EXISTS")

if (
    REPO /
    "config/schemas/protocol_specification.v3.schema.json"
).exists():
    fail("SCHEMA_V3_EXISTS")

summary = SUMMARY.read_text(
    encoding="utf-8"
)

required_summary_strings = [
    "AUTHOR CANDIDATE",
    "15 distinct enforcement classifications",
    "A positive V4-to-V2 mapping is therefore not authorized.",
    "has **not** yet received independent human technical review",
]

for s in required_summary_strings:
    if s not in summary:
        fail(
            "SUMMARY_BINDING|"
            + s
        )

print("RULE_RECORD_TOTAL=64")
print("RULES_WITH_ENFORCEMENT_FIELD=64")
print("ENFORCEMENT_VALUE_COUNT=15")
print("V2_EXPLICIT_ENFORCEMENT_CARRIER_PRESENT=NO")
print("VERDICT_TO_ENFORCEMENT_AMBIGUOUS_COUNT=3")
print("DEFECT_PLUS_VERDICT_TO_ENFORCEMENT_AMBIGUOUS_COUNT=4")
print("UNRESOLVED_REPRESENTATION_POLICY_FIELD_COUNT=3")
print("HISTORICAL_FOUR_OBSTRUCTIONS_RECOGNIZED_AS_RESOLVED=YES")
print("RESIDUAL_SCHEMA_V2_INSUFFICIENCY_AUTHOR_CANDIDATE=YES")
print("INDEPENDENT_HUMAN_TECHNICAL_REVIEW_COMPLETED=NO")
print("SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO")
print("POSITIVE_V4_TO_V2_MAPPING_AUTHORIZED=NO")
print("CURL_JSON_CREATED=NO")
print("RESIDUAL_SCHEMA_V2_INSUFFICIENCY_PROOF_V1=PASS")
