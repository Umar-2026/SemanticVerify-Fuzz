#!/usr/bin/env python3

import hashlib
import json
import sys
from pathlib import Path


def fail(msg):
    print("FAIL|" + msg)
    raise SystemExit(1)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_hash(obj):
    return hashlib.sha256(
        json.dumps(
            obj,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode("utf-8")
    ).hexdigest()


here = Path(__file__).resolve().parent

repo = here
while repo != repo.parent and not (repo / ".git").exists():
    repo = repo.parent

if not (repo / ".git").exists():
    fail("REPOSITORY_ROOT_NOT_FOUND")


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

contractp = (
    repo
    / "config/annotation/"
      "curl_canonical_representation_mapping_contract.v1.json"
)

checkpointp = (
    here
    / "01_mapping_contract_author_checkpoint.v1.json"
)

decisionp = (
    repo
    / "documentation/decisions/"
      "0039-curl-canonical-representation-mapping-contract-v1-"
      "author-checkpoint.md"
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


if sha(v4p) != V4_SHA:
    fail("APPROVED_V4_SHA")

if v4p.stat().st_size != 41033:
    fail("APPROVED_V4_SIZE")

if sha(schemap) != SCHEMA_SHA:
    fail("FROZEN_SCHEMA_SHA")


v4 = json.loads(
    v4p.read_text(encoding="utf-8")
)

schema = json.loads(
    schemap.read_text(encoding="utf-8")
)

contract = json.loads(
    contractp.read_text(encoding="utf-8")
)

checkpoint = json.loads(
    checkpointp.read_text(encoding="utf-8")
)


if contract["status"] != \
        "AUTHOR_CHECKPOINT_REVIEW_REQUIRED":
    fail("CONTRACT_STATUS")

if contract["contract_kind"] != \
        "NEGATIVE_FEASIBILITY_AND_REPRESENTATION_REVIEW_GATE":
    fail("CONTRACT_KIND")

if contract["exact_approved_v4_binding"]["sha256"] != V4_SHA:
    fail("CONTRACT_V4_SHA")

if contract["frozen_canonical_schema_binding"]["sha256"] != SCHEMA_SHA:
    fail("CONTRACT_SCHEMA_SHA")


semantic_containers = [
    "api_surface",
    "resources",
    "return_condition_policy",
    "verdict_semantics",
    "defect_taxonomy",
    "global_runtime_rules",
    "easy_handle_rules",
    "multi_handle_rules",
    "cross_resource_rules",
    "exit_obligations",
]

inventory = contract[
    "approved_v4_semantic_inventory"
]

if inventory[
    "protocol_semantic_containers"
] != semantic_containers:
    fail("SEMANTIC_CONTAINER_ORDER_OR_SET")

if inventory[
    "protocol_semantic_container_count"
] != 10:
    fail("SEMANTIC_CONTAINER_COUNT")

for key in semantic_containers:
    observed = canonical_hash(v4[key])

    expected = inventory[
        "protocol_semantic_container_sha256"
    ][key]

    if observed != expected:
        fail(
            "SEMANTIC_CONTAINER_HASH|"
            + key
        )


expected_counts = {
    "global_runtime_rules": 10,
    "easy_handle_rules": 21,
    "multi_handle_rules": 29,
    "cross_resource_rules": 4,
}

if inventory["rule_family_counts"] != expected_counts:
    fail("RULE_FAMILY_COUNTS")

if inventory["total_rule_record_count"] != 64:
    fail("TOTAL_RULE_COUNT")

if inventory["exit_obligation_record_count"] != 3:
    fail("EXIT_OBLIGATION_COUNT")

if inventory["api_surface_function_count"] != 12:
    fail("API_SURFACE_COUNT")

if inventory["resource_component_count"] != 5:
    fail("RESOURCE_COMPONENT_COUNT")


core = (
    set(schema["required"])
    - {
        "freeze_date",
        "content_sha256",
    }
)

if len(core) != 15:
    fail("PREFREEZE_CORE_COUNT")

candidate_paths = []


def walk(obj, path="$"):
    if isinstance(obj, dict):
        if set(obj) == core:
            candidate_paths.append(path)

        for key, value in obj.items():
            walk(
                value,
                path + "." + str(key),
            )

    elif isinstance(obj, list):
        for i, value in enumerate(obj):
            walk(
                value,
                f"{path}[{i}]",
            )


walk(v4)

if candidate_paths:
    fail(
        "REFERENCE_STYLE_CANDIDATE_PRESENT|"
        + repr(candidate_paths)
    )


gap = contract["observed_schema_gap"]

if gap[
    "reference_style_canonical_candidate_present"
] is not False:
    fail("CONTRACT_CANDIDATE_STATUS")

if gap[
    "fsm_construction_required_for_current_schema"
] is not True:
    fail("FSM_CONSTRUCTION_GAP")

if gap[
    "canonical_obligation_projection_required_for_current_schema"
] is not True:
    fail("OBLIGATION_PROJECTION_GAP")

if gap[
    "canonical_provenance_projection_required_for_current_schema"
] is not True:
    fail("PROVENANCE_PROJECTION_GAP")


resolution = contract[
    "current_mapping_resolution"
]

if resolution[
    "lossless_v4_to_frozen_schema_mapping_proven"
] is not False:
    fail("LOSSLESS_MAPPING_STATUS")

if resolution[
    "canonical_materialization_safe"
] is not False:
    fail("MATERIALIZATION_SAFETY")

if resolution[
    "curl_json_may_be_created_under_this_contract_before_review"
] is not False:
    fail("CURL_JSON_PRE_REVIEW_POLICY")

if resolution[
    "positive_mapping_algorithm_defined"
] is not False:
    fail("POSITIVE_MAPPING_STATUS")

if resolution[
    "synthetic_event_mapping_defined"
] is not False:
    fail("SYNTHETIC_EVENT_MAPPING_STATUS")


review = contract["human_review"]

if review["required"] is not True:
    fail("HUMAN_REVIEW_REQUIRED")

if review["review_status"] != "PENDING":
    fail("HUMAN_REVIEW_STATUS")

if review["review_item_decisions"] != {}:
    fail("SYNTHETIC_REVIEW_DECISIONS_PRESENT")

if review["overall_decision"] is not None:
    fail("SYNTHETIC_OVERALL_DECISION_PRESENT")

if review[
    "assistant_generated_or_synthetic_human_approval_permitted"
] is not False:
    fail("SYNTHETIC_APPROVAL_POLICY")


if len(
    contract["independent_review_requirements"]
) != 10:
    fail("REVIEW_REQUIREMENT_COUNT")

expected_rr = {
    f"CMR-RR{i:02d}"
    for i in range(1, 11)
}

observed_rr = {
    x["review_id"]
    for x in contract[
        "independent_review_requirements"
    ]
}

if observed_rr != expected_rr:
    fail("REVIEW_REQUIREMENT_IDS")


for key, value in contract[
    "prohibited_evidence_used"
].items():
    if value is not False:
        fail("PROHIBITED_EVIDENCE|" + key)


for key, value in contract[
    "downstream_non_authorizations"
].items():
    if value is not False:
        fail("DOWNSTREAM_AUTHORIZATION|" + key)


if contract["next_boundary"] != \
        "BUILD_INDEPENDENT_CURL_CANONICAL_REPRESENTATION_MAPPING_" \
        "CONTRACT_V1_REVIEW_PACKAGE":
    fail("NEXT_BOUNDARY")


if checkpoint["contract"]["sha256"] != sha(contractp):
    fail("CHECKPOINT_CONTRACT_SHA")

if checkpoint["contract"]["size_bytes"] != contractp.stat().st_size:
    fail("CHECKPOINT_CONTRACT_SIZE")

if checkpoint[
    "author_result"
]["lossless_mapping_proven"] is not False:
    fail("CHECKPOINT_MAPPING_STATUS")

if checkpoint[
    "author_result"
]["canonical_materialization_safe"] is not False:
    fail("CHECKPOINT_MATERIALIZATION_STATUS")

if checkpoint[
    "author_result"
]["human_review_completed"] is not False:
    fail("CHECKPOINT_HUMAN_REVIEW_STATUS")


if not decisionp.is_file():
    fail("DECISION_0039_MISSING")

dt = decisionp.read_text(encoding="utf-8")

for marker in (
    V4_SHA,
    SCHEMA_SHA,
    "LOSSLESS_V4_TO_FROZEN_SCHEMA_MAPPING_PROVEN=NO",
    "CANONICAL_MATERIALIZATION_SAFE=NO",
    "POSITIVE_MAPPING_ALGORITHM_AUTHORED=NO",
    "curl.json CREATED=NO",
    "No assistant-generated or synthetic human approval is permitted.",
    "BUILD_INDEPENDENT_CURL_CANONICAL_REPRESENTATION_MAPPING_CONTRACT_V1_REVIEW_PACKAGE",
):
    if marker not in dt:
        fail("DECISION_0039_BINDING|" + marker)


# Author-checkpoint-stage assertion.
if curlp.exists():
    fail("CURL_JSON_PREMATURELY_EXISTS")


print("APPROVED_V4_IMMUTABILITY=PASS")
print("FROZEN_CANONICAL_SCHEMA_BINDING=PASS")
print("PROTOCOL_SEMANTIC_CONTAINERS=10_OF_10_BOUND")
print("API_SURFACE_FUNCTION_COUNT=12")
print("RESOURCE_COMPONENT_COUNT=5")
print("GLOBAL_RUNTIME_RULE_COUNT=10")
print("EASY_HANDLE_RULE_COUNT=21")
print("MULTI_HANDLE_RULE_COUNT=29")
print("CROSS_RESOURCE_RULE_COUNT=4")
print("TOTAL_RULE_RECORD_COUNT=64")
print("EXIT_OBLIGATION_RECORD_COUNT=3")
print("REFERENCE_STYLE_CANONICAL_CANDIDATE_PRESENT=NO")
print("LOSSLESS_V4_TO_FROZEN_SCHEMA_MAPPING_PROVEN=NO")
print("POSITIVE_MAPPING_ALGORITHM_AUTHORED=NO")
print("CANONICAL_MATERIALIZATION_SAFE=NO")
print("HUMAN_REVIEW_REQUIRED=YES")
print("HUMAN_REVIEW_COMPLETED=NO")
print("SYNTHETIC_HUMAN_APPROVAL_PRESENT=NO")
print("CURL_JSON_CREATED=NO")
print("ANALYZER_IMPLEMENTATION_AUTHORIZED=NO")
print("BASELINE_EXECUTION_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
print("CURL_CANONICAL_REPRESENTATION_MAPPING_CONTRACT_V1_AUTHOR_CHECKPOINT=PASS")
