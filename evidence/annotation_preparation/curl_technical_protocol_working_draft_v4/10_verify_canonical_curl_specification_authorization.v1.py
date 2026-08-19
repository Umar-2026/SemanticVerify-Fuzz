#!/usr/bin/env python3

import hashlib
import json
import sys
from pathlib import Path


def fail(msg):
    print("FAIL|" + msg)
    raise SystemExit(1)


here = Path(__file__).resolve().parent

repo = here
while repo != repo.parent and not (repo / ".git").exists():
    repo = repo.parent

if not (repo / ".git").exists():
    fail("REPOSITORY_ROOT_NOT_FOUND")


V4_SHA = (
    "e17ae2ea5a70bdd790c946eb4b89ca37368d749cd7463159e69514d88a50cea8"
)

REVIEW_SHA = (
    "074814c04922f7cbc5fa41ef460cbde74dcb32529c09ef5752cf1d0f511f2aed"
)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


v4p = (
    repo
    / "config/annotation/"
      "curl_technical_protocol_working_draft.v4.json"
)

reviewp = (
    repo
    / "evidence/annotation_preparation/"
      "curl_technical_protocol_working_draft_v4/"
      "completed_human_review_v4/"
      "01_completed_human_technical_review.v4.md"
)

recordp = (
    repo
    / "evidence/annotation_preparation/"
      "curl_technical_protocol_working_draft_v4/"
      "completed_human_review_v4/"
      "02_completed_human_technical_review_record.v1.json"
)

authp = here / "09_canonical_curl_specification_authorization.v1.json"

decisionp = (
    repo
    / "documentation/decisions/"
      "0038-authorize-canonical-curl-specification-from-approved-v4.md"
)

canonicalp = (
    repo
    / "config/protocol_specifications/curl.json"
)

zlibp = (
    repo
    / "config/protocol_specifications/zlib.json"
)

libpcapp = (
    repo
    / "config/protocol_specifications/libpcap.json"
)


if sha(v4p) != V4_SHA:
    fail("APPROVED_V4_IMMUTABILITY_SHA")

if v4p.stat().st_size != 41033:
    fail("APPROVED_V4_IMMUTABILITY_SIZE")

if sha(reviewp) != REVIEW_SHA:
    fail("COMPLETED_HUMAN_REVIEW_SHA")

if reviewp.stat().st_size != 24722:
    fail("COMPLETED_HUMAN_REVIEW_SIZE")


completed = json.loads(
    recordp.read_text(encoding="utf-8")
)

if completed["review_target"]["sha256"] != V4_SHA:
    fail("COMPLETED_RECORD_V4_SHA")

if completed["completed_human_review"]["decision_counts"] != {
    "PASS": 12,
    "REVISION_REQUIRED": 0,
    "FAIL": 0,
}:
    fail("COMPLETED_RECORD_DECISION_COUNTS")

if completed["completed_human_review"]["overall_decision"] != \
        "APPROVE_EXACT_WORKING_DRAFT_V4_FOR_CANONICALIZATION":
    fail("COMPLETED_RECORD_OVERALL_DECISION")

effect = completed["technical_effect"]

if effect[
    "exact_v4_technically_adequate_for_later_canonicalization_authorization"
] is not True:
    fail("COMPLETED_RECORD_TECHNICAL_ELIGIBILITY")

if effect[
    "human_review_itself_authorizes_canonicalization"
] is not False:
    fail("HUMAN_REVIEW_SELF_AUTHORIZATION")

if effect[
    "separate_canonicalization_authorization_required"
] is not True:
    fail("SEPARATE_AUTHORIZATION_REQUIREMENT")


auth = json.loads(
    authp.read_text(encoding="utf-8")
)

if auth["authorization_type"] != \
        "CANONICAL_SPECIFICATION_MATERIALIZATION_FROM_EXACT_APPROVED_V4":
    fail("AUTHORIZATION_TYPE")

if auth["authorization_stage"] != "PRE_MATERIALIZATION":
    fail("AUTHORIZATION_STAGE")

source = auth["exact_approved_source"]

if source["sha256"] != V4_SHA:
    fail("AUTH_SOURCE_V4_SHA")

if source["size_bytes"] != 41033:
    fail("AUTH_SOURCE_V4_SIZE")

if source["must_remain_immutable"] is not True:
    fail("AUTH_V4_IMMUTABILITY")


human = auth["independent_human_approval"]

if human["completed_review_sha256"] != REVIEW_SHA:
    fail("AUTH_HUMAN_REVIEW_SHA")

if human["decision_distribution"] != {
    "PASS": 12,
    "REVISION_REQUIRED": 0,
    "FAIL": 0,
}:
    fail("AUTH_HUMAN_DECISION_COUNTS")

if human["overall_decision"] != \
        "APPROVE_EXACT_WORKING_DRAFT_V4_FOR_CANONICALIZATION":
    fail("AUTH_HUMAN_OVERALL_DECISION")


target = auth["authorized_target"]

if target["path"] != \
        "config/protocol_specifications/curl.json":
    fail("AUTHORIZED_TARGET_PATH")

if target["creation_authorized"] is not True:
    fail("CANONICAL_CREATION_AUTHORIZATION")

if target["overwrite_authorized"] is not False:
    fail("CANONICAL_OVERWRITE_AUTHORIZATION")

if target["target_must_not_preexist"] is not True:
    fail("TARGET_PREEXISTENCE_POLICY")

if target["source_v4_in_place_edit_authorized"] is not False:
    fail("V4_IN_PLACE_EDIT_POLICY")


boundary = auth["authorized_transformation_boundary"]

for key in (
    "protocol_rule_semantic_change_authorized",
    "protocol_rule_addition_authorized",
    "protocol_rule_removal_authorized",
    "api_surface_change_authorized",
    "defect_taxonomy_change_authorized",
    "machine_verdict_contract_change_authorized",
    "source_evidence_change_authorized",
    "new_evidence_class_authorized",
    "synthetic_protocol_event_authorized",
):
    if boundary[key] is not False:
        fail("UNAUTHORIZED_TRANSFORMATION|" + key)

if boundary["canonical_metadata_transformation_authorized"] is not True:
    fail("CANONICAL_METADATA_TRANSFORMATION")


preserve = auth["must_preserve_exactly"]

if preserve["protocol_semantic_container_count"] != 10:
    fail("PROTOCOL_CONTAINER_COUNT")

if len(preserve["protocol_semantic_containers"]) != 10:
    fail("PROTOCOL_CONTAINER_SET")

if preserve["easy_handle_rule_count"] != 21:
    fail("EASY_RULE_COUNT")

if preserve["multi_handle_rule_count"] != 29:
    fail("MULTI_RULE_COUNT")

if preserve["frozen_api_surface_function_count"] != 12:
    fail("API_SURFACE_COUNT")

if preserve["machine_verdicts"] != [
    "VALID",
    "VIOLATION-MUST",
    "VIOLATION-MAY",
    "UNKNOWN",
]:
    fail("MACHINE_VERDICT_CONTRACT")

if preserve["pinned_curl_commit"] != \
        "68720b4837284335b2d63cb358f8f6ce65f5bc55":
    fail("PINNED_CURL_COMMIT")

if preserve["pinned_curl_tree"] != \
        "e23d273aeb073c04aa5b073b35c9fde16979c896":
    fail("PINNED_CURL_TREE")

if preserve["approved_source_evidence_class"] != \
        "PREAPPROVED_SOURCE_ONLY":
    fail("SOURCE_EVIDENCE_CLASS")

if preserve["approved_source_file_count"] != 21:
    fail("SOURCE_FILE_COUNT")


inspection = auth["required_pre_materialization_inspection"]

if inspection["required"] is not True:
    fail("CONVENTION_INSPECTION_REQUIREMENT")

if inspection["inspection_mode"] != "READ_ONLY":
    fail("CONVENTION_INSPECTION_MODE")

if inspection[
    "materialization_before_inspection_authorized"
] is not False:
    fail("PRE_INSPECTION_MATERIALIZATION_POLICY")

if inspection["reference_specifications"] != [
    "config/protocol_specifications/zlib.json",
    "config/protocol_specifications/libpcap.json",
]:
    fail("CANONICAL_REFERENCE_SPECIFICATIONS")

if not zlibp.is_file():
    fail("ZLIB_CANONICAL_REFERENCE_MISSING")

if not libpcapp.is_file():
    fail("LIBPCAP_CANONICAL_REFERENCE_MISSING")


for key, value in auth[
    "prohibited_evidence_boundary"
].items():
    if key.endswith("_used") and value is not False:
        fail("PROHIBITED_EVIDENCE|" + key)


for key, value in auth[
    "downstream_non_authorizations"
].items():
    if value is not False:
        fail("DOWNSTREAM_NON_AUTHORIZATION|" + key)


state = auth[
    "canonicalization_state_after_this_authorization"
]

if state[
    "canonical_curl_specification_authorized"
] is not True:
    fail("CANONICAL_AUTHORIZATION_STATE")

if state[
    "canonical_curl_specification_created"
] is not False:
    fail("CANONICAL_CREATED_STATE")

if state[
    "canonical_curl_specification_frozen"
] is not False:
    fail("CANONICAL_FROZEN_STATE")

if state[
    "approved_v4_remains_immutable"
] is not True:
    fail("V4_IMMUTABILITY_STATE")


if auth["next_boundary"] != \
        "INSPECT_CANONICAL_SPECIFICATION_CONVENTIONS_BEFORE_CURL_MATERIALIZATION":
    fail("NEXT_BOUNDARY")


if not decisionp.is_file():
    fail("DECISION_0038_MISSING")

dt = decisionp.read_text(encoding="utf-8")

for marker in (
    V4_SHA,
    REVIEW_SHA,
    "APPROVE_EXACT_WORKING_DRAFT_V4_FOR_CANONICALIZATION",
    "config/protocol_specifications/curl.json",
    "Protocol-rule semantic change is not authorized.",
    "config/protocol_specifications/zlib.json",
    "config/protocol_specifications/libpcap.json",
    "Canonical curl specification authorization:",
    "`YES`",
    "Canonical `curl.json` created:",
    "`NO`",
    "INSPECT_CANONICAL_SPECIFICATION_CONVENTIONS_BEFORE_CURL_MATERIALIZATION",
):
    if marker not in dt:
        fail("DECISION_0038_BINDING|" + marker)


# Authorization-stage-only assertion.
# This verifier MUST NOT be reused after legitimate materialization.
if canonicalp.exists():
    fail("CANONICAL_CURL_JSON_PREMATURELY_EXISTS")


print("APPROVED_V4_IMMUTABILITY_SHA256=PASS")
print("COMPLETED_V4_HUMAN_REVIEW_BINDING=PASS")
print("HUMAN_REVIEW_DECISION=12_PASS_0_REVISION_REQUIRED_0_FAIL")
print(
    "OVERALL_TECHNICAL_REVIEW_DECISION="
    "APPROVE_EXACT_WORKING_DRAFT_V4_FOR_CANONICALIZATION"
)
print("CANONICAL_TARGET=config/protocol_specifications/curl.json")
print("CANONICAL_CURL_SPECIFICATION_CREATION_AUTHORIZED=YES")
print("CANONICAL_CURL_SPECIFICATION_CREATED=NO")
print("CANONICAL_TARGET_OVERWRITE_AUTHORIZED=NO")
print("APPROVED_V4_IN_PLACE_EDIT_AUTHORIZED=NO")
print("PROTOCOL_RULE_SEMANTIC_CHANGE_AUTHORIZED=NO")
print("PROTOCOL_RULE_ADDITION_AUTHORIZED=NO")
print("PROTOCOL_RULE_REMOVAL_AUTHORIZED=NO")
print("PROTOCOL_CONTAINERS_TO_PRESERVE=10")
print("EASY_HANDLE_RULE_COUNT_TO_PRESERVE=21")
print("MULTI_HANDLE_RULE_COUNT_TO_PRESERVE=29")
print("FROZEN_API_SURFACE_FUNCTION_COUNT_TO_PRESERVE=12")
print("FOUR_MACHINE_VERDICT_CONTRACT=PASS")
print("APPROVED_SOURCE_EVIDENCE_CLASS=PREAPPROVED_SOURCE_ONLY")
print("APPROVED_SOURCE_FILE_COUNT=21")
print("CANONICAL_CONVENTION_INSPECTION_REQUIRED=YES")
print("CANONICAL_CONVENTION_INSPECTION_MODE=READ_ONLY")
print("MATERIALIZATION_BEFORE_CONVENTION_INSPECTION_AUTHORIZED=NO")
print("PRE_MATERIALIZATION_ABSENCE_ASSERTION_EXECUTED=YES")
print("GENERATED_DRIVER_INSPECTION_AUTHORIZED=NO")
print("SELECTED_SAMPLE_MEMBERSHIP_INSPECTION_AUTHORIZED=NO")
print("GOLD_ANNOTATION_AUTHORIZED=NO")
print("ANALYZER_IMPLEMENTATION_AUTHORIZED=NO")
print("ANALYZER_EXECUTION_AUTHORIZED=NO")
print("BASELINE_EXECUTION_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
print("CANONICAL_CURL_SPECIFICATION_AUTHORIZATION_VERIFICATION=PASS")
