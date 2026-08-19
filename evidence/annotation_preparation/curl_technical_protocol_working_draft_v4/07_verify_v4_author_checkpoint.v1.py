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


V3_SHA = "2c10317a7a1fa745d64b461bb318ac2aa1e3e23439ca261c8cd746d1ea3f8ac2"

v3p = repo / "config/annotation/curl_technical_protocol_working_draft.v3.json"
v4p = repo / "config/annotation/curl_technical_protocol_working_draft.v4.json"

authp = here / "01_v4_successor_authorization.v1.json"
resolutionp = here / "04_v4_successor_author_resolution.v1.json"
tracep = here / "05_v4_metadata_successor_traceability.v1.json"
checkpointp = here / "06_v4_author_checkpoint.v1.json"

decisionp = (
    repo
    / "documentation/decisions/"
      "0036-curl-technical-working-draft-v4-author-checkpoint.md"
)


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


if sha(v3p) != V3_SHA:
    fail("V3_IMMUTABILITY")


cp = json.loads(checkpointp.read_text(encoding="utf-8"))

v4_sha = cp["final_checkpoint_identity"]["sha256"]
v4_size = cp["final_checkpoint_identity"]["size_bytes"]

if sha(v4p) != v4_sha:
    fail("V4_SHA")

if v4p.stat().st_size != v4_size:
    fail("V4_SIZE")


auth = json.loads(authp.read_text(encoding="utf-8"))

if auth["authorization_type"] != \
        "IMMUTABLE_METADATA_SUCCESSOR_AUTHORING_ONLY":
    fail("AUTH_TYPE")

if auth["authorized_successor"]["authoring_authorized"] is not True:
    fail("AUTH_SUCCESSOR_AUTHORING")

if auth["authorized_successor"][
    "predecessor_in_place_edit_authorized"
] is not False:
    fail("AUTH_IN_PLACE_EDIT")

if auth["authorized_successor"][
    "protocol_rule_semantic_change_authorized"
] is not False:
    fail("AUTH_PROTOCOL_CHANGE")

if auth["authorized_successor"]["canonicalization_authorized"] is not False:
    fail("AUTH_CANONICALIZATION")


v3 = json.loads(v3p.read_text(encoding="utf-8"))
v4 = json.loads(v4p.read_text(encoding="utf-8"))

if v4["schema_id"] != "curl.technical-protocol-working-draft.v4":
    fail("V4_SCHEMA")

if v4["status"] != \
        "SOURCE_ONLY_TECHNICAL_WORKING_DRAFT_V4_AUTHOR_CHECKPOINT":
    fail("V4_STATUS")

if v4["next_required_boundary"] != \
        "BUILD_INDEPENDENT_CURL_TECHNICAL_WORKING_DRAFT_V4_REVIEW_PACKAGE":
    fail("V4_NEXT_BOUNDARY")


containers = [
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

for key in containers:
    if v3[key] != v4[key]:
        fail("PROTOCOL_CONTAINER_CHANGED|" + key)

if len(v4["easy_handle_rules"]) != 21:
    fail("EASY_RULE_COUNT")

if len(v4["multi_handle_rules"]) != 29:
    fail("MULTI_RULE_COUNT")


g = v4["governance"]

if g["working_draft_version"] != "V4":
    fail("WORKING_DRAFT_VERSION")

if g["predecessor_working_draft_version"] != "V3":
    fail("PREDECESSOR_VERSION")

if g["predecessor_sha256"] != V3_SHA:
    fail("PREDECESSOR_SHA")

if g["completed_human_review_sha256"] != \
        "9a15b13cea29bcbcbfff349c9b9bcb113a9d9a4e01afe03727d7be8dbd87c327":
    fail("REVIEW_SHA")

if g["successor_authorization_commit"] != \
        "cee5299cf80b633019ea6c98efc065b46aade1dd":
    fail("AUTH_COMMIT")

if "v1_in_place_edit_authorized" in g:
    fail("STALE_V1_FIELD")

if g["predecessor_in_place_edit_authorized"] is not False:
    fail("PREDECESSOR_EDIT_BOUNDARY")


trace = json.loads(tracep.read_text(encoding="utf-8"))

if trace["successor_binding"]["sha256"] != v4_sha:
    fail("TRACE_SHA")

if trace["successor_binding"]["status"] != \
        "SOURCE_ONLY_TECHNICAL_WORKING_DRAFT_V4_AUTHOR_CHECKPOINT":
    fail("TRACE_STATUS")

if trace["preservation_contract"]["protocol_rule_semantic_change"] is not False:
    fail("TRACE_PROTOCOL_CHANGE")

if trace["preservation_contract"][
    "accepted_v3_protocol_semantics_preserved"
] is not True:
    fail("TRACE_PROTOCOL_PRESERVATION")

for k, v in trace["evidence_boundary"].items():
    if k.endswith("_used") and v is not False:
        fail("PROHIBITED_EVIDENCE|" + k)


resolution = json.loads(
    resolutionp.read_text(encoding="utf-8")
)

if resolution["successor"]["sha256"] != v4_sha:
    fail("RESOLUTION_SHA")

if resolution["successor"]["status"] != \
        "SOURCE_ONLY_TECHNICAL_WORKING_DRAFT_V4_AUTHOR_CHECKPOINT":
    fail("RESOLUTION_STATUS")

if resolution["preservation_result"][
    "protocol_rule_semantics_preserved"
] is not True:
    fail("RESOLUTION_PROTOCOL_PRESERVATION")

if resolution["preservation_result"]["new_protocol_rule_count"] != 0:
    fail("NEW_PROTOCOL_RULE_COUNT")

if resolution["preservation_result"]["removed_protocol_rule_count"] != 0:
    fail("REMOVED_PROTOCOL_RULE_COUNT")


if cp["authorization_binding"]["pre_authoring_only_verifier_reused"] is not False:
    fail("STAGE_MISMATCHED_VERIFIER_REUSED")

if cp["protocol_preservation"]["all_protocol_containers_preserved"] is not True:
    fail("CHECKPOINT_PROTOCOL_PRESERVATION")

if cp["protocol_preservation"]["protocol_rule_semantic_change"] is not False:
    fail("CHECKPOINT_PROTOCOL_CHANGE")

if cp["downstream_review_package_requirements"][
    "V4-P01_platform_independent_source_path_comparison"
] != "PENDING":
    fail("V4_P01")

if cp["downstream_review_package_requirements"][
    "V4-P02_fresh_v4_bound_review_package"
] != "PENDING":
    fail("V4_P02")

for k, v in cp["non_authorizations"].items():
    if v is not False:
        fail("NON_AUTHORIZATION|" + k)


if not decisionp.is_file():
    fail("DECISION_0036_MISSING")

dt = decisionp.read_text(encoding="utf-8")

for marker in (
    v4_sha,
    V3_SHA,
    "V3-RR02",
    "V3-RR12",
    "pre-authoring-only V4",
    "Protocol-rule semantic change: `NONE`",
    "V4-P01 remains pending",
    "V4-P02 remains pending",
    "BUILD_INDEPENDENT_CURL_TECHNICAL_WORKING_DRAFT_V4_REVIEW_PACKAGE",
):
    if marker not in dt:
        fail("DECISION_0036_BINDING|" + marker)


print("V3_IMMUTABILITY_SHA256=PASS")
print("FINAL_V4_CHECKPOINT_SHA256=PASS")
print("FINAL_V4_CHECKPOINT_SIZE=PASS")
print("V4_SCHEMA_ID=PASS")
print("V4_STATUS=AUTHOR_CHECKPOINT")
print("STAGE_CORRECT_AUTHORIZATION_VALIDATION=PASS")
print("PRE_AUTHORING_ONLY_AUTHORIZATION_VERIFIER_REUSED=NO")
print("V4_C01_TO_V4_C06=PASS")
print("PROTOCOL_CONTAINERS_PRESERVED=10_OF_10")
print("EASY_HANDLE_RULE_COUNT=21")
print("MULTI_HANDLE_RULE_COUNT=29")
print("NEW_PROTOCOL_RULE_COUNT=0")
print("REMOVED_PROTOCOL_RULE_COUNT=0")
print("PROTOCOL_RULE_SEMANTIC_CHANGE=NONE")
print("V4_METADATA_SUCCESSOR_TRACEABILITY=PASS")
print("V4_AUTHOR_RESOLUTION=PASS")
print("V4_P01_PLATFORM_INDEPENDENT_REVIEW_VERIFIER=PENDING")
print("V4_P02_FRESH_V4_REVIEW_PACKAGE=PENDING")
print("CANONICAL_CURL_SPECIFICATION_AUTHORIZED=NO")
print("GENERATED_DRIVER_INSPECTION_AUTHORIZED=NO")
print("SELECTED_SAMPLE_MEMBERSHIP_INSPECTION_AUTHORIZED=NO")
print("GOLD_ANNOTATION_AUTHORIZED=NO")
print("ANALYZER_IMPLEMENTATION_AUTHORIZED=NO")
print("ANALYZER_EXECUTION_AUTHORIZED=NO")
print("BASELINE_EXECUTION_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
print("CURL_TECHNICAL_WORKING_DRAFT_V4_AUTHOR_CHECKPOINT_VERIFICATION=PASS")
