#!/usr/bin/env python3

import collections
import hashlib
import json
from pathlib import Path

REPO = Path(
    "/openbayes/home/semanticverify-fuzz-research"
)

HERE = Path(__file__).resolve().parent

AUTH = HERE / \
    "01_residual_schema_v2_losslessness_insufficiency_proof_authorization.v1.json"

def fail(x):
    print("FAIL|" + x)
    raise SystemExit(1)

def sha(path):
    if not path.is_file():
        fail("MISSING|" + str(path))

    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()

r = json.loads(
    AUTH.read_text(
        encoding="utf-8"
    )
)

if r["authorization_type"] != \
   "PRE_PROOF_AUTHORING_ONLY":
    fail("AUTHORIZATION_TYPE")

if r["status"] != \
   "AUTHORIZED_TO_AUTHOR_RESIDUAL_SCHEMA_V2_INSUFFICIENCY_PROOF_AND_PREPARE_INDEPENDENT_REVIEW_ONLY":
    fail("STATUS")

for info in r["exact_inputs"].values():
    path = REPO / info["path"]

    if sha(path) != info["sha256"]:
        fail(
            "INPUT_SHA|"
            + info["path"]
        )

v4 = json.loads(
    (
        REPO /
        r["exact_inputs"]["curl_v4"]["path"]
    ).read_text(
        encoding="utf-8"
    )
)

schema = json.loads(
    (
        REPO /
        r["exact_inputs"]["active_schema_v2"]["path"]
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
    fail("ENFORCEMENT_CARRIER_NOW_PRESENT")

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
    fail("VERDICT_AMBIGUITY_COUNT")

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
    fail("DEFECT_VERDICT_AMBIGUITY_COUNT")

missing = []

for field, token in {
    "normative_strength_uncertainty_must_not_be_silently_strengthened":
        "normative_strength",

    "resource_centered":
        "resource_centered",

    "synthetic_protocol_events_invented":
        "synthetic_protocol_events",
}.items():
    if token not in raw:
        missing.append(field)

if sorted(missing) != [
    "normative_strength_uncertainty_must_not_be_silently_strengthened",
    "resource_centered",
    "synthetic_protocol_events_invented",
]:
    fail("POLICY_GAP_SET")

proof = REPO / \
    "evidence/annotation_preparation/protocol_specification_schema_successor_v2/schema_v2_residual_losslessness_insufficiency_proof_v1"

review = REPO / \
    "evidence/annotation_preparation/protocol_specification_schema_successor_v2/schema_v2_residual_losslessness_insufficiency_review_package_v1"

if proof.exists():
    fail("PROOF_ALREADY_AUTHORED")

if review.exists():
    fail("REVIEW_PACKAGE_ALREADY_AUTHORED")

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
    fail("UNAUTHORIZED_SCHEMA_V3_EXISTS")

for key, value in r[
    "explicit_non_authorizations"
].items():
    if value is not False:
        fail(
            "NONAUTH|"
            + key
        )

print("RULE_RECORD_TOTAL=64")
print("ENFORCEMENT_VALUE_COUNT=15")
print("V2_EXPLICIT_ENFORCEMENT_CARRIER_PRESENT=NO")
print("VERDICT_TO_ENFORCEMENT_AMBIGUOUS_COUNT=3")
print("DEFECT_PLUS_VERDICT_TO_ENFORCEMENT_AMBIGUOUS_COUNT=4")
print("UNRESOLVED_REPRESENTATION_POLICY_FIELD_COUNT=3")
print("CURRENT_SCHEMA_V2_SUFFICIENT_FOR_EXACT_V4_LOSSLESS_MAPPING=NO")
print("POSITIVE_MAPPING_AUTHORIZED=NO")
print("SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO")
print("CURL_JSON_CREATED=NO")
print("DECISION_0067_RESIDUAL_PROOF_AUTHORIZATION=PASS")
print("IMPORTANT=THIS_VERIFIER_IS_PRE_PROOF_AUTHORING_ONLY")
