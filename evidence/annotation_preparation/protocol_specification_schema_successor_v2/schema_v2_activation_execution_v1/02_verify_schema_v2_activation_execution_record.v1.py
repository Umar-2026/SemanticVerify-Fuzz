#!/usr/bin/env python3

import hashlib
import json
from pathlib import Path

REPO = Path(
    "/openbayes/home/semanticverify-fuzz-research"
)

HERE = Path(__file__).resolve().parent

RECORD = HERE / \
    "01_schema_v2_activation_execution_record.v1.json"

def fail(x):
    print("FAIL|" + x)
    raise SystemExit(1)

def digest(path):
    if not path.is_file():
        fail(
            "MISSING|"
            + str(path)
        )

    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()

r = json.loads(
    RECORD.read_text(
        encoding="utf-8"
    )
)

if r["status"] != "SCHEMA_V2_ACTIVE":
    fail("STATUS")

if r["activation_effect"] != {
    "active_v2_hash_contract_installed": True,
    "active_version_dispatch_installed": True,
    "decision_0019_successor_adopted": True,
    "schema_v2_activated": True,
}:
    fail("ACTIVATION_EFFECT")

hash_info = r[
    "active_v2_hash_contract"
]

hash_source = REPO / hash_info[
    "source_path"
]

hash_dest = REPO / hash_info[
    "destination_path"
]

if digest(hash_source) != hash_info[
    "source_sha256"
]:
    fail("HASH_SOURCE_SHA")

if digest(hash_dest) != hash_info[
    "destination_sha256"
]:
    fail("HASH_DEST_SHA")

if hash_source.read_bytes() != \
   hash_dest.read_bytes():
    fail("HASH_BYTE_IDENTITY")

dispatch_info = r[
    "active_version_dispatch"
]

dispatch_source = REPO / dispatch_info[
    "source_path"
]

dispatch_dest = REPO / dispatch_info[
    "destination_path"
]

if digest(dispatch_source) != dispatch_info[
    "source_sha256"
]:
    fail("DISPATCH_SOURCE_SHA")

if digest(dispatch_dest) != dispatch_info[
    "destination_sha256"
]:
    fail("DISPATCH_DEST_SHA")

if dispatch_source.read_bytes() != \
   dispatch_dest.read_bytes():
    fail("DISPATCH_BYTE_IDENTITY")

schema = REPO / r[
    "schema_v2"
]["path"]

if digest(schema) != r[
    "schema_v2"
]["sha256"]:
    fail("SCHEMA_V2_SHA")

successor = r[
    "decision_0019_successor"
]

successor_path = REPO / successor[
    "reviewed_active_form_path"
]

if digest(successor_path) != successor[
    "reviewed_active_form_sha256"
]:
    fail("SUCCESSOR_SHA")

if successor[
    "adopted_by_reference"
] is not True:
    fail("SUCCESSOR_NOT_ADOPTED")

decision = REPO / r[
    "activation_decision"
]["path"]

if digest(decision) != r[
    "activation_decision"
]["sha256"]:
    fail("DECISION_0066_SHA")

decision_text = decision.read_text(
    encoding="utf-8"
)

required_strings = [
    "Status: ACTIVE — SCHEMA V2 ACTIVATED",
    "a96f9d8b6811a9f9170a18de9ff8be6f80a3704b9e6a13c59fbb88e423bec3bb",
    "adopted by exact SHA-256-bound reference",
    "Historical Decision 0019 remains byte-immutable",
]

for text in required_strings:
    if text not in decision_text:
        fail(
            "DECISION_0066_BINDING|"
            + text
        )

immutable = r[
    "immutable_existing_artifacts"
]

checks = {
    "v1_hash_contract_sha256":
        REPO /
        "config/protocol_content_hash_canonicalization.v1.json",

    "decision_0019_sha256":
        REPO /
        "documentation/decisions/0019-canonical-library-protocol-specification-path-convention.md",

    "zlib_sha256":
        REPO /
        "config/protocol_specifications/zlib.json",

    "libpcap_sha256":
        REPO /
        "config/protocol_specifications/libpcap.json",
}

for key, path in checks.items():
    if digest(path) != immutable[key]:
        fail(
            "IMMUTABLE_ARTIFACT|"
            + key
        )

curl = REPO / \
    "config/protocol_specifications/curl.json"

if curl.exists():
    fail("CURL_JSON_EXISTS")

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

if retired[
    "decision_0065_pre_activation_verifier_final_run_completed"
] is not True:
    fail("PREACTIVATION_FINAL_RUN")

if retired[
    "decision_0065_pre_activation_verifier_must_never_run_again"
] is not True:
    fail("PREACTIVATION_RETIREMENT")

if retired[
    "historical_initial_blank_verifiers_rerun"
] is not False:
    fail("HISTORICAL_BLANK_RERUN")

if retired[
    "decision_0063_prepackage_authorization_verifier_rerun"
] is not False:
    fail("DEC0063_RERUN")

print("SCHEMA_V2_ACTIVE=YES")
print("ACTIVE_V2_HASH_CONTRACT_INSTALLED=YES")
print("ACTIVE_V2_HASH_CONTRACT_BYTE_IDENTITY=PASS")
print("ACTIVE_VERSION_DISPATCH_INSTALLED=YES")
print("ACTIVE_VERSION_DISPATCH_BYTE_IDENTITY=PASS")
print("DECISION_0019_SUCCESSOR_ADOPTED=YES")
print("HISTORICAL_DECISION_0019_IMMUTABLE=PASS")
print("V1_ZLIB_LIBPCAP_IMMUTABILITY=PASS")
print("CURL_JSON_CREATED=NO")
print("POSITIVE_V4_TO_V2_MAPPING_DEFINED=NO")
print("POSITIVE_V4_TO_V2_MAPPING_AUTHORIZED=NO")
print("ANALYZER_IMPLEMENTATION_AUTHORIZED=NO")
print("BASELINE_EXECUTION_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
print("DECISION_0065_PRE_ACTIVATION_VERIFIER_RETIRED=YES")
print("SCHEMA_V2_ACTIVATION_EXECUTION_RECORD=PASS")
