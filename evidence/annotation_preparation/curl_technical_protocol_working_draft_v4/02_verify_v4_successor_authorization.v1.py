#!/usr/bin/env python3

import hashlib
import json
import subprocess
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


V3_SHA = (
    "2c10317a7a1fa745d64b461bb318ac2aa1e3e23439ca261c8cd746d1ea3f8ac2"
)

V3_REVIEW_SHA = (
    "9a15b13cea29bcbcbfff349c9b9bcb113a9d9a4e01afe03727d7be8dbd87c327"
)

EXPECTED_REVIEW_COMMIT = (
    "0f6625753452944bbedeab66a77a4098a6e349a9"
)

EXPECTED_REVIEW_TREE = (
    "a822ec4504071e0edbdc8b77c0eda8ea3974cdbc"
)

v3 = (
    repo
    / "config/annotation/"
      "curl_technical_protocol_working_draft.v3.json"
)

v4 = (
    repo
    / "config/annotation/"
      "curl_technical_protocol_working_draft.v4.json"
)

review = (
    repo
    / "evidence/annotation_preparation/"
      "curl_technical_protocol_working_draft_v3/"
      "completed_human_review_v3/"
      "01_completed_human_technical_review.v3.md"
)

review_record = (
    repo
    / "evidence/annotation_preparation/"
      "curl_technical_protocol_working_draft_v3/"
      "completed_human_review_v3/"
      "02_completed_human_technical_review_record.v1.json"
)

review_verify = (
    repo
    / "evidence/annotation_preparation/"
      "curl_technical_protocol_working_draft_v3/"
      "completed_human_review_v3/"
      "03_verify_completed_human_technical_review.v1.py"
)

auth_path = here / "01_v4_successor_authorization.v1.json"

decision = (
    repo
    / "documentation/decisions/"
      "0035-curl-technical-working-draft-v4-successor-authorization.md"
)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


if sha(v3) != V3_SHA:
    fail("V3_IMMUTABILITY_SHA")

if sha(review) != V3_REVIEW_SHA:
    fail("COMPLETED_V3_REVIEW_SHA")


proc = subprocess.run(
    [sys.executable, str(review_verify)],
    cwd=str(review_verify.parent),
)

if proc.returncode != 0:
    fail("COMPLETED_V3_HUMAN_REVIEW_VERIFY")


rr = json.loads(
    review_record.read_text(encoding="utf-8")
)

if rr["review_target"]["sha256"] != V3_SHA:
    fail("REVIEW_RECORD_V3_BINDING")

if (
    rr["completed_human_review"]["sha256"]
    != V3_REVIEW_SHA
):
    fail("REVIEW_RECORD_HUMAN_REVIEW_BINDING")

if (
    rr["completed_human_review"]["overall_decision"]
    != "REVISION_REQUIRED"
):
    fail("REVIEW_RECORD_OVERALL_DECISION")


revision_items = [
    k
    for k, v in
    rr["completed_human_review"]["review_item_decisions"].items()
    if v == "REVISION_REQUIRED"
]

if revision_items != [
    "V3-RR02",
    "V3-RR12",
]:
    fail(
        "V3_REVISION_ITEM_SET|"
        + repr(revision_items)
    )


auth = json.loads(
    auth_path.read_text(encoding="utf-8")
)

if auth["authorization_type"] != \
        "IMMUTABLE_METADATA_SUCCESSOR_AUTHORING_ONLY":
    fail("AUTHORIZATION_TYPE")


pred = auth["predecessor"]

if pred["sha256"] != V3_SHA:
    fail("PREDECESSOR_SHA")

if pred["completed_human_review_commit"] != \
        EXPECTED_REVIEW_COMMIT:
    fail("PREDECESSOR_REVIEW_COMMIT")

if pred["completed_human_review_tree"] != \
        EXPECTED_REVIEW_TREE:
    fail("PREDECESSOR_REVIEW_TREE")

if pred["completed_human_review_sha256"] != \
        V3_REVIEW_SHA:
    fail("PREDECESSOR_REVIEW_SHA")

if pred["overall_decision"] != "REVISION_REQUIRED":
    fail("PREDECESSOR_REVIEW_DECISION")

if pred["immutable"] is not True:
    fail("PREDECESSOR_IMMUTABILITY")


succ = auth["authorized_successor"]

if succ["path"] != \
        "config/annotation/curl_technical_protocol_working_draft.v4.json":
    fail("SUCCESSOR_PATH")

if succ["schema_id"] != \
        "curl.technical-protocol-working-draft.v4":
    fail("SUCCESSOR_SCHEMA")

if succ["authoring_authorized"] is not True:
    fail("SUCCESSOR_AUTHORING")

if succ["predecessor_in_place_edit_authorized"] is not False:
    fail("PREDECESSOR_IN_PLACE_EDIT")

if succ["protocol_rule_semantic_change_authorized"] is not False:
    fail("PROTOCOL_RULE_CHANGE_AUTHORIZATION")

if succ["canonicalization_authorized"] is not False:
    fail("CANONICALIZATION_AUTHORIZATION")


basis = auth["review_basis"]

if basis["revision_required_items"] != [
    "V3-RR02",
    "V3-RR12",
]:
    fail("REVIEW_BASIS_REVISION_SET")

if len(basis["pass_items_to_preserve"]) != 10:
    fail("PASS_PRESERVATION_COUNT")

if (
    basis["accepted_protocol_rule_semantics_must_be_preserved"]
    is not True
):
    fail("PROTOCOL_SEMANTICS_PRESERVATION")


if len(auth["required_v4_draft_corrections"]) != 6:
    fail("V4_DRAFT_CORRECTION_COUNT")

if [
    x["id"]
    for x in auth["required_v4_draft_corrections"]
] != [
    "V4-C01",
    "V4-C02",
    "V4-C03",
    "V4-C04",
    "V4-C05",
    "V4-C06",
]:
    fail("V4_DRAFT_CORRECTION_IDS")


if len(auth["required_downstream_review_package_corrections"]) != 2:
    fail("V4_PACKAGE_CORRECTION_COUNT")

if [
    x["id"]
    for x in auth["required_downstream_review_package_corrections"]
] != [
    "V4-P01",
    "V4-P02",
]:
    fail("V4_PACKAGE_CORRECTION_IDS")


preserve = auth["must_preserve_exactly"]

for key in (
    "protocol_rule_semantics_from_v3",
    "easy_handle_rules_semantics",
    "multi_handle_rules_semantics",
    "global_runtime_rules_semantics",
    "cross_resource_rules_semantics",
    "exit_obligations_semantics",
    "defect_taxonomy_semantics",
    "return_condition_policy_semantics",
    "verdict_semantics",
):
    if preserve.get(key) is not True:
        fail("PRESERVATION_BOUNDARY|" + key)


if preserve["frozen_api_surface_function_count"] != 12:
    fail("API_SURFACE_COUNT")

if preserve["approved_source_evidence_class"] != \
        "PREAPPROVED_SOURCE_ONLY":
    fail("SOURCE_EVIDENCE_CLASS")

if preserve["approved_source_file_count"] != 21:
    fail("SOURCE_FILE_COUNT")

if preserve["machine_verdicts"] != [
    "VALID",
    "VIOLATION-MUST",
    "VIOLATION-MAY",
    "UNKNOWN",
]:
    fail("MACHINE_VERDICT_SET")

if preserve["synthetic_protocol_events_may_be_invented"] is not False:
    fail("SYNTHETIC_EVENT_BOUNDARY")


expected_prohibited = [
    "generated_driver_source",
    "selected_sample_membership",
    "raw_model_responses",
    "generated_driver_compiler_log_semantic_content",
    "gold_labels",
    "analyzer_output",
    "baseline_output",
    "llm_review_output",
    "repair_output",
]

if auth["prohibited_evidence"] != expected_prohibited:
    fail("PROHIBITED_EVIDENCE_SET")


for key, value in auth["explicit_non_authorizations"].items():
    if value is not False:
        fail("NON_AUTHORIZATION_CHANGED|" + key)


constraints = auth["authoring_constraints"]

for key in (
    "v4_must_be_new_file",
    "v3_must_not_be_modified",
    "protocol_rule_objects_must_not_change_semantically",
    "no_new_protocol_rule",
    "no_removed_protocol_rule",
    "no_new_api_function",
    "no_new_evidence_class",
    "no_generated_driver_derived_metadata",
    "only_review_required_metadata_corrections_authorized",
    "v4_requires_separate_author_checkpoint",
    "v4_requires_new_independent_human_review",
):
    if constraints.get(key) is not True:
        fail("AUTHORING_CONSTRAINT|" + key)


if auth["next_boundary"] != \
        "INSPECT_V3_METADATA_FOR_EXACT_BOUNDED_V4_AUTHORING":
    fail("NEXT_BOUNDARY")


if not decision.is_file():
    fail("DECISION_0035_MISSING")

dtext = decision.read_text(encoding="utf-8")

for marker in (
    V3_SHA,
    V3_REVIEW_SHA,
    EXPECTED_REVIEW_COMMIT,
    "V3-RR02",
    "V3-RR12",
    "No protocol-rule semantic change is authorized",
    "platform-independent path",
    "PREAPPROVED_SOURCE_ONLY",
    "INSPECT_V3_METADATA_FOR_EXACT_BOUNDED_V4_AUTHORING",
):
    if marker not in dtext:
        fail("DECISION_0035_BINDING|" + marker)


# Authorization stage only: V4 must not yet exist.
if v4.exists():
    fail("V4_DRAFT_PREMATURELY_EXISTS")


print("V3_IMMUTABILITY_SHA256=PASS")
print("COMPLETED_V3_HUMAN_REVIEW_BINDING=PASS")
print("PREDECESSOR_DECISION=REVISION_REQUIRED")
print("AUTHORIZED_REVISION_ITEMS=V3-RR02,V3-RR12")
print("V3_PASS_ITEMS_TO_PRESERVE=10")
print("V4_DRAFT_METADATA_CORRECTIONS=6")
print("V4_REVIEW_PACKAGE_CORRECTIONS=2")
print("V3_PROTOCOL_RULE_SEMANTICS_MUST_BE_PRESERVED=YES")
print("PROTOCOL_RULE_SEMANTIC_CHANGE_AUTHORIZED=NO")
print("FROZEN_TWELVE_FUNCTION_SURFACE=PASS")
print("APPROVED_SOURCE_EVIDENCE_CLASS=PREAPPROVED_SOURCE_ONLY")
print("APPROVED_SOURCE_FILES=21")
print("FOUR_MACHINE_VERDICT_CONTRACT=PASS")
print("V3_IN_PLACE_EDIT_AUTHORIZED=NO")
print("V4_SUCCESSOR_AUTHORING_AUTHORIZED=YES")
print("V4_WORKING_DRAFT_ALREADY_CREATED=NO")
print("PLATFORM_INDEPENDENT_REVIEW_PACKAGE_VERIFIER_REQUIRED=YES")
print("CANONICAL_CURL_SPECIFICATION_AUTHORIZED=NO")
print("GENERATED_DRIVER_INSPECTION_AUTHORIZED=NO")
print("SELECTED_SAMPLE_MEMBERSHIP_INSPECTION_AUTHORIZED=NO")
print("GOLD_ANNOTATION_AUTHORIZED=NO")
print("ANALYZER_IMPLEMENTATION_AUTHORIZED=NO")
print("ANALYZER_EXECUTION_AUTHORIZED=NO")
print("BASELINE_EXECUTION_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
print("CURL_TECHNICAL_V4_SUCCESSOR_AUTHORIZATION_VERIFICATION=PASS")
