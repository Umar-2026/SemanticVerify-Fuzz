#!/usr/bin/env python3

import hashlib
import json
from pathlib import Path


def fail(msg):
    print("FAIL|" + msg)
    raise SystemExit(1)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_sha(value):
    data = json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")

    return hashlib.sha256(data).hexdigest()


here = Path(__file__).resolve().parent

repo = here
while repo != repo.parent and not (repo / ".git").exists():
    repo = repo.parent

if not (repo / ".git").exists():
    fail("REPOSITORY_ROOT_NOT_FOUND")


v2p = (
    repo
    / "config/annotation/"
      "curl_canonical_representation_mapping_contract.v2.json"
)

v4p = (
    repo
    / "config/annotation/"
      "curl_technical_protocol_working_draft.v4.json"
)

schemap = (
    repo
    / "config/schemas/"
      "protocol_specification.schema.json"
)

authp = (
    here
    / "01_v2_successor_authorization.v1.json"
)

checkpointp = (
    here
    / "04_v2_schema_insufficiency_author_checkpoint.v1.json"
)

decisionp = (
    repo
    / "documentation/decisions/"
      "0042-curl-canonical-mapping-contract-v2-schema-insufficiency-author-checkpoint.md"
)

curlp = (
    repo
    / "config/protocol_specifications/curl.json"
)


V4_SHA = (
    "e17ae2ea5a70bdd790c946eb4b89ca37368d749cd7463159e69514d88a50cea8"
)

SCHEMA_SHA = (
    "7eb17eeb8f49b37420d0d1d71539cf0d7cb08241ecf133e7b4139fd130718b34"
)

AUTH_SHA = (
    "5d3771c4748731642f3068722e986e65479a9b85d1087737e2faeb2dc76b073b"
)


if not v2p.is_file():
    fail("V2_MISSING")

if sha(v4p) != V4_SHA:
    fail("V4_SHA")

if sha(schemap) != SCHEMA_SHA:
    fail("SCHEMA_SHA")

if sha(authp) != AUTH_SHA:
    fail("AUTH_SHA")


v2 = json.loads(
    v2p.read_text(encoding="utf-8")
)

v4 = json.loads(
    v4p.read_text(encoding="utf-8")
)

schema = json.loads(
    schemap.read_text(encoding="utf-8")
)

auth = json.loads(
    authp.read_text(encoding="utf-8")
)

checkpoint = json.loads(
    checkpointp.read_text(encoding="utf-8")
)


if v2["contract_version"] != "V2":
    fail("CONTRACT_VERSION")

if v2["contract_kind"] != \
        "FORMAL_FROZEN_SCHEMA_INSUFFICIENCY_PROOF":
    fail("CONTRACT_KIND")

if v2["status"] != \
        "AUTHOR_CHECKPOINT_INDEPENDENT_REVIEW_REQUIRED":
    fail("CONTRACT_STATUS")

expected_outcome = (
    "FROZEN_SCHEMA_INSUFFICICIENCY_DEMONSTRATED_"
    "SCHEMA_SUCCESSOR_REQUIRED"
)

if v2["author_outcome"] != expected_outcome:
    fail("AUTHOR_OUTCOME")


inventory = v2["frozen_inventory"]

if inventory["semantic_container_count"] != 10:
    fail("SEMANTIC_CONTAINER_COUNT")

if inventory["api_surface_function_count"] != 12:
    fail("API_FUNCTION_COUNT")

if inventory["resource_component_count"] != 5:
    fail("RESOURCE_COMPONENT_COUNT")

if inventory["global_runtime_rule_count"] != 10:
    fail("GLOBAL_RULE_COUNT")

if inventory["easy_handle_rule_count"] != 21:
    fail("EASY_RULE_COUNT")

if inventory["multi_handle_rule_count"] != 29:
    fail("MULTI_RULE_COUNT")

if inventory["cross_resource_rule_count"] != 4:
    fail("CROSS_RULE_COUNT")

if inventory["total_rule_record_count"] != 64:
    fail("TOTAL_RULE_COUNT")

if inventory["exit_obligation_count"] != 3:
    fail("EXIT_OBLIGATION_COUNT")

if inventory["allowed_machine_verdicts"] != [
    "VALID",
    "VIOLATION-MUST",
    "VIOLATION-MAY",
    "UNKNOWN",
]:
    fail("FOUR_VERDICT_CONTRACT")


for key, expected_hash in (
    v2["approved_v4_semantic_container_hashes"].items()
):
    if canonical_sha(v4[key]) != expected_hash:
        fail(
            "SEMANTIC_CONTAINER_HASH|"
            + key
        )


witnesses = {
    x["obstruction_id"]: x
    for x in v2[
        "structural_obstruction_witnesses"
    ]
}

required_witnesses = {
    "V2-O1-MEMBERSHIP-RELATION",
    "V2-O2-FOUR-VERDICT-AND-JOIN-POLICY",
    "V2-O3-PATH-AND-SET-VALUED-REASONING",
    "V2-O4-STRUCTURED-RULE-PAYLOAD",
}

if set(witnesses) != required_witnesses:
    fail("OBSTRUCTION_WITNESS_SET")


if (
    v4["resources"]["EASY_MULTI_MEMBERSHIP"]["relation"]
    != "easy_handle -> zero_or_one_multi_handle"
):
    fail("MEMBERSHIP_RELATION")


if (
    witnesses[
        "V2-O1-MEMBERSHIP-RELATION"
    ]["frozen_schema_facts"][
        "explicit_membership_property_present"
    ]
    is not False
):
    fail("MEMBERSHIP_CARRIER_FACT")


if (
    witnesses[
        "V2-O2-FOUR-VERDICT-AND-JOIN-POLICY"
    ]["frozen_schema_facts"][
        "explicit_machine_verdict_property_present"
    ]
    is not False
):
    fail("VERDICT_CARRIER_FACT")


if (
    witnesses[
        "V2-O3-PATH-AND-SET-VALUED-REASONING"
    ]["frozen_schema_facts"][
        "explicit_path_sensitive_property_present"
    ]
    is not False
):
    fail("PATH_CARRIER_FACT")


structured = witnesses[
    "V2-O4-STRUCTURED-RULE-PAYLOAD"
]

if structured[
    "structured_value_occurrence_count"
] != 12:
    fail("STRUCTURED_VALUE_COUNT")

if structured[
    "frozen_schema_facts"
][
    "canonical_obligation_object_typed_field_count"
] != 0:
    fail("OBLIGATION_OBJECT_CARRIER_COUNT")


proof = v2[
    "formal_insufficiency_argument"
]

if proof[
    "positive_mapping_candidate_authored"
] is not False:
    fail("POSITIVE_MAPPING_CANDIDATE")

if proof[
    "lossless_mapping_to_existing_frozen_schema_demonstrated"
] is not False:
    fail("LOSSLESS_MAPPING_STATUS")

if proof[
    "frozen_schema_insufficiency_demonstrated_under_current_contract"
] is not True:
    fail("INSUFFICIENCY_AUTHOR_CONCLUSION")

if proof[
    "schema_successor_required"
] is not True:
    fail("SCHEMA_SUCCESSOR_REQUIRED")

if proof[
    "schema_successor_authorized_by_this_contract"
] is not False:
    fail("SCHEMA_SUCCESSOR_AUTHORIZATION")


if v2[
    "positive_mapping_algorithm_defined"
] is not False:
    fail("POSITIVE_MAPPING_DEFINED")

if v2[
    "positive_mapping_algorithm_approved"
] is not False:
    fail("POSITIVE_MAPPING_APPROVED")

if v2[
    "lossless_v4_to_frozen_schema_mapping_proven"
] is not False:
    fail("LOSSLESS_V4_MAPPING_PROVEN")

if v2[
    "canonical_materialization_safe"
] is not False:
    fail("MATERIALIZATION_SAFE")

if v2[
    "curl_json_creation_authorized"
] is not False:
    fail("CURL_JSON_AUTHORIZED")

if v2[
    "curl_json_created"
] is not False:
    fail("CURL_JSON_CREATED_RECORD")

if v2[
    "canonical_schema_successor_required"
] is not True:
    fail("SCHEMA_SUCCESSOR_REQUIRED_TOP")

if v2[
    "canonical_schema_successor_authorized"
] is not False:
    fail("SCHEMA_SUCCESSOR_AUTHORIZED_TOP")


if schema.get("additionalProperties") is not False:
    fail("SCHEMA_NOT_CLOSED")


if auth[
    "representation_design_boundary"
][
    "opaque_payload_packing_authorized"
] is not False:
    fail("OPAQUE_PACKING_AUTH")


if auth[
    "representation_design_boundary"
][
    "semantic_protocol_event_invention_authorized"
] is not False:
    fail("SYNTHETIC_EVENT_AUTH")


for key, value in v2[
    "evidence_quarantine"
].items():
    if value is not False:
        fail(
            "EVIDENCE_QUARANTINE|"
            + key
        )


for key, value in v2[
    "downstream_non_authorizations"
].items():
    if value is not False:
        fail(
            "DOWNSTREAM_NONAUTH|"
            + key
        )


if checkpoint[
    "exact_v2_contract"
]["sha256"] != sha(v2p):
    fail("CHECKPOINT_V2_SHA")

if checkpoint[
    "exact_v2_contract"
]["size_bytes"] != v2p.stat().st_size:
    fail("CHECKPOINT_V2_SIZE")

if checkpoint[
    "exact_v2_contract"
]["author_outcome"] != expected_outcome:
    fail("CHECKPOINT_AUTHOR_OUTCOME")


if not decisionp.is_file():
    fail("DECISION_0042_MISSING")

decision = decisionp.read_text(
    encoding="utf-8"
)

for marker in (
    sha(v2p),
    V4_SHA,
    SCHEMA_SHA,
    AUTH_SHA,
    expected_outcome,
    "CREATE_INDEPENDENT_REVIEW_PACKAGE_FOR_"
    "CURL_MAPPING_CONTRACT_V2_SCHEMA_INSUFFICIENCY_PROOF",
):
    if marker not in decision:
        fail(
            "DECISION_0042_BINDING|"
            + marker
        )


if curlp.exists():
    fail("CURL_JSON_PREMATURELY_EXISTS")


print("EXACT_V2_CONTRACT_SHA256=" + sha(v2p))
print("EXACT_V2_CONTRACT_SIZE=" + str(v2p.stat().st_size))
print("V2_CONTRACT_KIND=FORMAL_FROZEN_SCHEMA_INSUFFICIENCY_PROOF")
print("APPROVED_V4_SEMANTIC_CONTAINERS=10_OF_10_BOUND")
print("API_SURFACE_FUNCTION_COUNT=12")
print("RESOURCE_COMPONENT_COUNT=5")
print("TOTAL_RULE_RECORD_COUNT=64")
print("EXIT_OBLIGATION_COUNT=3")
print("FOUR_VERDICT_CONTRACT=PASS")
print("STRUCTURAL_OBSTRUCTION_WITNESSES=4")
print("MEMBERSHIP_RELATION_EXPLICIT_CARRIER=NO")
print("FOUR_VERDICT_JOIN_POLICY_EXPLICIT_CARRIER=NO")
print("PATH_SET_VALUED_POLICY_EXPLICIT_CARRIER=NO")
print("STRUCTURED_RULE_VALUE_OCCURRENCES=12")
print("CANONICAL_OBLIGATION_OBJECT_TYPED_CARRIERS=0")
print("OPAQUE_PAYLOAD_PACKING_AUTHORIZED=NO")
print("SEMANTIC_PROTOCOL_EVENT_INVENTION_AUTHORIZED=NO")
print("POSITIVE_MAPPING_ALGORITHM_DEFINED=NO")
print("LOSSLESS_V4_TO_FROZEN_SCHEMA_MAPPING_PROVEN=NO")
print("V2_AUTHOR_CONCLUSION_FROZEN_SCHEMA_INSUFFICIENT=YES")
print("CANONICAL_SCHEMA_SUCCESSOR_REQUIRED=YES")
print("CANONICAL_SCHEMA_SUCCESSOR_AUTHORIZED=NO")
print("CANONICAL_MATERIALIZATION_SAFE=NO")
print("CURL_JSON_CREATED=NO")
print("INDEPENDENT_V2_TECHNICAL_REVIEW_REQUIRED=YES")
print("ANALYZER_IMPLEMENTATION_AUTHORIZED=NO")
print("BASELINE_EXECUTION_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
print("V2_SCHEMA_INSUFFICIENCY_AUTHOR_CHECKPOINT_VERIFICATION=PASS")
