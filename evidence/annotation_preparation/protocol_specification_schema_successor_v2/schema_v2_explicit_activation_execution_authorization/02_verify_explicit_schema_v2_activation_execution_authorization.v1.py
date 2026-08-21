#!/usr/bin/env python3

import hashlib
import json
from pathlib import Path

REPO = Path(
    "/openbayes/home/semanticverify-fuzz-research"
)

HERE = Path(__file__).resolve().parent

AUTH = HERE / \
    "01_explicit_schema_v2_activation_execution_authorization.v1.json"

def fail(x):
    print("FAIL|" + x)
    raise SystemExit(1)

r = json.loads(
    AUTH.read_text(
        encoding="utf-8"
    )
)

if r["status"] != \
   "AUTHORIZED_FOR_EXACT_FUTURE_ACTIVATION_EXECUTION_NOT_YET_ACTIVATED":
    fail("STATUS")

if r["authorization_type"] != \
   "PRE_ACTIVATION_EXECUTION_ONLY":
    fail("AUTHORIZATION_TYPE")

approved = r["approval_chain"]

if approved != {
    "activation_artifact_finalization_AF01_to_AF10_pass_count": 10,
    "activation_artifact_finalization_fail_count": 0,
    "activation_artifact_finalization_revision_required_count": 0,
    "activation_governance_human_approved": True,
    "schema_v2_candidate_human_approved": True,
    "v2_hash_active_form_human_approved": True,
}:
    fail("APPROVAL_CHAIN")

installs = r[
    "authorized_exact_installations"
]

expected = {
    "v2_hash_contract": {
        "source_path":
            "evidence/annotation_preparation/protocol_specification_schema_successor_v2/schema_v2_hash_contract_finalization_package_v1/02_active_form_v2_hash_contract.REVIEW_CANDIDATE.json",

        "source_sha256":
            "37f035bb617f5598a0e368ba3b60b4bf1e69e4e69ce2f1053d71c0fcc96619e9",

        "destination_path":
            "config/protocol_content_hash_canonicalization.v2.json",
    },

    "version_dispatch": {
        "source_path":
            "evidence/annotation_preparation/protocol_specification_schema_successor_v2/schema_v2_activation_artifact_finalization_package_v1/02_active_form_version_dispatch.REVIEW_CANDIDATE.json",

        "source_sha256":
            "67a96c3eda8de95fa6c55342d5d33ea725e16cea8af21fcb4f3b8945b9d4eeee",

        "destination_path":
            "config/protocol_specification_schema_version_dispatch.v1.json",
    }
}

for key, e in expected.items():
    got = installs[key]

    for field, value in e.items():
        if got[field] != value:
            fail(
                "INSTALL_BINDING|"
                + key
                + "|"
                + field
            )

    if got["transformation_allowed"] is not False:
        fail("TRANSFORMATION_ALLOWED|" + key)

    if got[
        "destination_bytes_must_equal_source_bytes"
    ] is not True:
        fail("BYTE_IDENTITY|" + key)

    source = REPO / got["source_path"]

    if not source.is_file():
        fail("SOURCE_MISSING|" + key)

    if hashlib.sha256(
        source.read_bytes()
    ).hexdigest() != got["source_sha256"]:
        fail("SOURCE_SHA|" + key)

    destination = REPO / got[
        "destination_path"
    ]

    if destination.exists():
        fail(
            "ACTIVE_DESTINATION_ALREADY_EXISTS|"
            + key
        )

successor = r[
    "decision_0019_successor_adoption"
]

if successor[
    "reviewed_active_form_sha256"
] != \
   "a96f9d8b6811a9f9170a18de9ff8be6f80a3704b9e6a13c59fbb88e423bec3bb":
    fail("SUCCESSOR_SHA_BINDING")

source = REPO / successor[
    "reviewed_active_form_path"
]

if hashlib.sha256(
    source.read_bytes()
).hexdigest() != successor[
    "reviewed_active_form_sha256"
]:
    fail("SUCCESSOR_SOURCE_SHA")

if successor[
    "adoption_mode"
] != \
   "EXACT_SHA256_BOUND_ADOPTION_BY_REFERENCE_IN_EXPLICIT_ACTIVATION_DECISION":
    fail("SUCCESSOR_ADOPTION_MODE")

if successor[
    "decision_0019_must_remain_byte_immutable"
] is not True:
    fail("DECISION_0019_IMMUTABILITY")

future_decision = REPO / successor[
    "future_activation_decision_path"
]

if future_decision.exists():
    fail("FUTURE_ACTIVATION_DECISION_ALREADY_EXISTS")

if (REPO / "config/protocol_specifications/curl.json").exists():
    fail("CURL_JSON_EXISTS")

for key, value in r[
    "explicit_non_authorizations"
].items():
    if value is not False:
        fail("NONAUTH|" + key)

for key, value in r[
    "current_effect"
].items():
    if value is not False:
        fail("CURRENT_EFFECT|" + key)

print("APPROVAL_CHAIN=PASS")
print("EXACT_V2_HASH_INSTALL_BINDING=PASS")
print("EXACT_VERSION_DISPATCH_INSTALL_BINDING=PASS")
print("DECISION_0019_SUCCESSOR_SHA_BOUND_ADOPTION=PASS")
print("ACTIVE_V2_HASH_PATH_ABSENT=PASS")
print("ACTIVE_VERSION_DISPATCH_PATH_ABSENT=PASS")
print("FUTURE_ACTIVATION_DECISION_PATH_ABSENT=PASS")
print("CURL_JSON_PATH_ABSENT=PASS")
print("NO_MAPPING_ANALYZER_BASELINE_REPAIR_AUTHORIZATION=PASS")
print("SCHEMA_V2_ACTIVATED=NO")
print("EXPLICIT_SCHEMA_V2_ACTIVATION_EXECUTION_AUTHORIZATION=PASS")
print("IMPORTANT=THIS_VERIFIER_IS_PRE_ACTIVATION_EXECUTION_ONLY")
