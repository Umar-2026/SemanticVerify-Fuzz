#!/usr/bin/env python3

import hashlib
import json
from pathlib import Path

REPO = Path(
    "/openbayes/home/semanticverify-fuzz-research"
)

HERE = Path(__file__).resolve().parent

AUTH = HERE / \
    "01_residual_schema_v2_insufficiency_review_package_authorization.v1.json"

def fail(x):
    print("FAIL|" + x)
    raise SystemExit(1)

def digest(path):
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
   "PRE_REVIEW_PACKAGE_AUTHORING_ONLY":
    fail("AUTHORIZATION_TYPE")

if r["status"] != \
   "AUTHORIZED_TO_AUTHOR_EXACT_INDEPENDENT_HUMAN_TECHNICAL_REVIEW_PACKAGE_ONLY":
    fail("STATUS")

checkpoint = r[
    "immutable_author_checkpoint"
]

for key in (
    "proof_json",
    "proof_md",
    "decision_0068",
):
    info = checkpoint[key]

    if digest(
        REPO / info["path"]
    ) != info["sha256"]:
        fail(
            "CHECKPOINT_SHA|"
            + key
        )

items = r[
    "mandatory_review_items"
]

expected_ids = [
    "RI01",
    "RI02",
    "RI03",
    "RI04",
    "RI05",
    "RI06",
    "RI07",
    "RI08",
]

if [
    x["review_item_id"]
    for x in items
] != expected_ids:
    fail("REVIEW_ITEM_SET")

if r[
    "allowed_item_decisions"
] != [
    "PASS",
    "REVISION_REQUIRED",
    "FAIL",
]:
    fail("ITEM_DECISIONS")

if r[
    "allowed_overall_decisions"
] != [
    "APPROVE_RESIDUAL_SCHEMA_V2_INSUFFICIENCY_PROOF",
    "REVISION_REQUIRED",
    "FAIL",
]:
    fail("OVERALL_DECISIONS")

target = REPO / r[
    "review_package_target"
]["path"]

if target.exists():
    fail("REVIEW_PACKAGE_ALREADY_EXISTS")

for forbidden in (
    "config/protocol_specifications/curl.json",
    "config/annotation/curl_positive_v4_to_v2_mapping_contract.v1.json",
    "config/schemas/protocol_specification.v3.schema.json",
):
    if (
        REPO /
        forbidden
    ).exists():
        fail(
            "FORBIDDEN_ARTIFACT_EXISTS|"
            + forbidden
        )

for key, value in r[
    "explicit_non_authorizations"
].items():
    if value is not False:
        fail(
            "NONAUTH|"
            + key
        )

retired = r[
    "retired_verifier_constraints"
]

for key, value in retired.items():
    if value is not False:
        fail(
            "RETIRED_VERIFIER_STATE|"
            + key
        )

print("IMMUTABLE_PROOF_V1_BINDING=PASS")
print("MANDATORY_REVIEW_ITEM_COUNT=8")
print("RI01_TO_RI08_DEFINED=YES")
print("INDEPENDENT_HUMAN_TECHNICAL_REVIEW_REQUIRED=YES")
print("SYNTHETIC_REVIEWER_DECISION_ALLOWED=NO")
print("PROOF_V1_MODIFICATION_AUTHORIZED=NO")
print("SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO")
print("POSITIVE_MAPPING_AUTHORIZED=NO")
print("CURL_JSON_CREATED=NO")
print("DECISION_0069_REVIEW_PACKAGE_AUTHORIZATION=PASS")
print("IMPORTANT=THIS_VERIFIER_IS_PRE_REVIEW_PACKAGE_AUTHORING_ONLY")
