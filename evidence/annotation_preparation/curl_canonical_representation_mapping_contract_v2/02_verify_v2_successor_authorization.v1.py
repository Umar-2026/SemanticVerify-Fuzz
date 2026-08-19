#!/usr/bin/env python3

import hashlib
import json
from pathlib import Path


def fail(msg):
    print("FAIL|" + msg)
    raise SystemExit(1)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


here = Path(__file__).resolve().parent

repo = here
while repo != repo.parent and not (repo / ".git").exists():
    repo = repo.parent

if not (repo / ".git").exists():
    fail("REPOSITORY_ROOT_NOT_FOUND")


authp = here / "01_v2_successor_authorization.v1.json"

v1p = (
    repo
    / "config/annotation/"
      "curl_canonical_representation_mapping_contract.v1.json"
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

reviewp = (
    repo
    / "evidence/annotation_preparation/"
      "curl_canonical_representation_mapping_contract_v1/"
      "completed_human_review_v1/"
      "01_completed_human_mapping_contract_review.v1.md"
)

recordp = (
    repo
    / "evidence/annotation_preparation/"
      "curl_canonical_representation_mapping_contract_v1/"
      "completed_human_review_v1/"
      "02_completed_human_mapping_contract_review_record.v1.json"
)

decisionp = (
    repo
    / "documentation/decisions/"
      "0041-authorize-curl-canonical-representation-mapping-contract-v2-successor.md"
)

v2p = (
    repo
    / "config/annotation/"
      "curl_canonical_representation_mapping_contract.v2.json"
)

curlp = (
    repo
    / "config/protocol_specifications/curl.json"
)


V1_SHA = (
    "31d606f98f2c819291103ba7403214206ccde1d8e5e0e9103f0659c227622257"
)

V4_SHA = (
    "e17ae2ea5a70bdd790c946eb4b89ca37368d749cd7463159e69514d88a50cea8"
)

SCHEMA_SHA = (
    "7eb17eeb8f49b37420d0d1d71539cf0d7cb08241ecf133e7b4139fd130718b34"
)

REVIEW_SHA = (
    "a19d4a6132be417798b027794045227949ea40265e11714543e85ef1c325ad73"
)

RECORD_SHA = (
    "b7a8572b3893d83e411c4d79a56682c9b3a47345ed25396df5dcc4556d8a161d"
)


if sha(v1p) != V1_SHA:
    fail("V1_SHA")

if v1p.stat().st_size != 10879:
    fail("V1_SIZE")

if sha(v4p) != V4_SHA:
    fail("V4_SHA")

if v4p.stat().st_size != 41033:
    fail("V4_SIZE")

if sha(schemap) != SCHEMA_SHA:
    fail("SCHEMA_SHA")

if sha(reviewp) != REVIEW_SHA:
    fail("HUMAN_REVIEW_SHA")

if sha(recordp) != RECORD_SHA:
    fail("HUMAN_REVIEW_RECORD_SHA")


record = json.loads(
    recordp.read_text(encoding="utf-8")
)

if record["exact_human_review"]["decision_counts"] != {
    "PASS": 10,
    "REVISION_REQUIRED": 0,
    "FAIL": 0,
}:
    fail("HUMAN_REVIEW_COUNTS")

if record["exact_human_review"]["overall_decision"] != \
        "APPROVE_MAPPING_BLOCKER_CONTRACT":
    fail("HUMAN_REVIEW_DECISION")

if record["human_review_effect"][
    "mapping_blocker_contract_v1_approved"
] is not True:
    fail("V1_BLOCKER_APPROVAL")

if record["human_review_effect"][
    "lossless_v4_to_frozen_schema_mapping_proven"
] is not False:
    fail("V1_LOSSLESS_STATUS")


auth = json.loads(
    authp.read_text(encoding="utf-8")
)

if auth["status"] != \
        "AUTHORIZED_FOR_V2_MAPPING_CONTRACT_AUTHORING_ONLY":
    fail("AUTH_STATUS")

if auth["authorized_v2_target"]["path"] != \
        "config/annotation/curl_canonical_representation_mapping_contract.v2.json":
    fail("V2_TARGET")

if auth["authorized_v2_target"][
    "authoring_authorized"
] is not True:
    fail("V2_AUTHORING_AUTHORIZATION")

if auth["authorized_v2_target"][
    "approval_by_authoring"
] is not False:
    fail("V2_APPROVAL_BY_AUTHORING")

if auth["authorized_v2_target"][
    "canonical_materialization_by_authoring"
] is not False:
    fail("V2_MATERIALIZATION_BY_AUTHORING")


boundary = auth["representation_design_boundary"]

required_true = (
    "candidate_representation_decisions_may_be_authored",
    "representational_event_ids_for_existing_v4_semantics_authorized",
)

for key in required_true:
    if boundary[key] is not True:
        fail("REQUIRED_TRUE|" + key)


required_false = (
    "candidate_representation_decisions_are_approved_by_authoring",
    "candidate_mapping_may_be_called_lossless_before_independent_review",
    "new_protocol_semantics_authorized",
    "new_api_function_authorized",
    "new_defect_category_authorized",
    "new_machine_verdict_authorized",
    "new_source_evidence_authorized",
    "new_evidence_class_authorized",
    "semantic_protocol_event_invention_authorized",
    "rule_strengthening_authorized",
    "rule_weakening_authorized",
    "rule_merging_with_semantic_loss_authorized",
    "rule_splitting_with_new_semantics_authorized",
    "opaque_payload_packing_authorized",
    "protocol_rule_addition_authorized",
    "protocol_rule_removal_authorized",
    "protocol_rule_semantic_change_authorized",
    "api_surface_change_authorized",
    "defect_taxonomy_change_authorized",
    "machine_verdict_contract_change_authorized",
    "source_evidence_change_authorized",
)

for key in required_false:
    if boundary[key] is not False:
        fail("REQUIRED_FALSE|" + key)


account = auth["v2_required_semantic_accounting"]

if account["approved_v4_semantic_container_count"] != 10:
    fail("SEMANTIC_CONTAINER_COUNT")

if account["frozen_api_surface_function_count"] != 12:
    fail("API_SURFACE_COUNT")

if account["resource_component_count"] != 5:
    fail("RESOURCE_COMPONENT_COUNT")

if account["global_runtime_rule_count"] != 10:
    fail("GLOBAL_RULE_COUNT")

if account["easy_handle_rule_count"] != 21:
    fail("EASY_RULE_COUNT")

if account["multi_handle_rule_count"] != 29:
    fail("MULTI_RULE_COUNT")

if account["cross_resource_rule_count"] != 4:
    fail("CROSS_RULE_COUNT")

if account["total_rule_record_count"] != 64:
    fail("TOTAL_RULE_COUNT")

if account["exit_obligation_count"] != 3:
    fail("EXIT_OBLIGATION_COUNT")

if account["allowed_machine_verdicts"] != [
    "VALID",
    "VIOLATION-MUST",
    "VIOLATION-MAY",
    "UNKNOWN",
]:
    fail("FOUR_VERDICT_CONTRACT")


review_req = auth["independent_review_requirement"]

if review_req["required"] is not True:
    fail("INDEPENDENT_REVIEW_REQUIRED")

if review_req[
    "positive_mapping_may_be_used_before_review"
] is not False:
    fail("PRE_REVIEW_MAPPING_USE")

if review_req[
    "curl_json_may_be_materialized_before_review"
] is not False:
    fail("PRE_REVIEW_MATERIALIZATION")


for key, value in auth[
    "prohibited_evidence"
].items():
    if value is not True:
        fail("PROHIBITED_EVIDENCE_POLICY|" + key)


for key, value in auth[
    "downstream_non_authorizations"
].items():
    if value is not False:
        fail("DOWNSTREAM_AUTHORIZATION|" + key)


if auth["next_boundary"] != \
        "AUTHOR_CURL_CANONICAL_REPRESENTATION_MAPPING_CONTRACT_V2":
    fail("NEXT_BOUNDARY")


if not decisionp.is_file():
    fail("DECISION_0041_MISSING")

decision = decisionp.read_text(
    encoding="utf-8"
)

for marker in (
    V1_SHA,
    REVIEW_SHA,
    RECORD_SHA,
    V4_SHA,
    SCHEMA_SHA,
    "10 PASS / 0 REVISION_REQUIRED / 0 FAIL",
    "APPROVE_MAPPING_BLOCKER_CONTRACT",
    "AUTHOR_CURL_CANONICAL_REPRESENTATION_MAPPING_CONTRACT_V2",
):
    if marker not in decision:
        fail(
            "DECISION_0041_BINDING|"
            + marker
        )


# This verifier is intentionally PRE-V2-AUTHORING only.
if v2p.exists():
    fail("V2_MAPPING_CONTRACT_ALREADY_AUTHORED")

if curlp.exists():
    fail("CURL_JSON_PREMATURELY_EXISTS")


print("EXACT_V1_MAPPING_CONTRACT_BINDING=PASS")
print("COMPLETED_V1_HUMAN_REVIEW_BINDING=PASS")
print("V1_HUMAN_REVIEW_DECISION=10_PASS_0_REVISION_REQUIRED_0_FAIL")
print("V1_OVERALL_DECISION=APPROVE_MAPPING_BLOCKER_CONTRACT")
print("APPROVED_V4_BINDING=PASS")
print("FROZEN_CANONICAL_SCHEMA_BINDING=PASS")
print("V2_MAPPING_CONTRACT_AUTHORING_AUTHORIZED=YES")
print("V2_CANDIDATE_REPRESENTATION_DESIGN_AUTHORIZED=YES")
print("V2_MAPPING_APPROVED=NO")
print("CANONICAL_SCHEMA_SUCCESSOR_AUTHORIZED=NO")
print("CURL_JSON_MATERIALIZATION_AUTHORIZED=NO")
print("PROTOCOL_RULE_SEMANTIC_CHANGE_AUTHORIZED=NO")
print("PROTOCOL_RULE_ADDITION_AUTHORIZED=NO")
print("PROTOCOL_RULE_REMOVAL_AUTHORIZED=NO")
print("SEMANTIC_PROTOCOL_EVENT_INVENTION_AUTHORIZED=NO")
print("REPRESENTATIONAL_EVENT_IDS_FOR_EXISTING_V4_SEMANTICS_AUTHORIZED=YES")
print("INDEPENDENT_V2_TECHNICAL_REVIEW_REQUIRED=YES")
print("ANALYZER_IMPLEMENTATION_AUTHORIZED=NO")
print("BASELINE_EXECUTION_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
print("CURL_CANONICAL_MAPPING_CONTRACT_V2_SUCCESSOR_AUTHORIZATION=PASS")
