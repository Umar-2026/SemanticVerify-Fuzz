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


V2_SHA = (
    "63c17bbd0a09365fad9d3f0445fdc2115a8a0e945f622a39c745f31e1baf3d31"
)

REVIEW_SHA = (
    "597699068c3ba7bf480204c67d88d940f400c7425442a081a18198908b1e029e"
)

EXPECTED_REVIEW_COMMIT = (
    "96b5ff417206fa2f1fe9e8e5c9d499561d4e6d7b"
)

EXPECTED_REVIEW_TREE = (
    "6c8304aa228019c2a1d5cfe2cc4af856843ba6cd"
)

v2 = (
    repo
    / "config/annotation/"
      "curl_technical_protocol_working_draft.v2.json"
)

v3 = (
    repo
    / "config/annotation/"
      "curl_technical_protocol_working_draft.v3.json"
)

review = (
    repo
    / "evidence/annotation_preparation/"
      "curl_technical_protocol_working_draft_v2/"
      "completed_human_review_v2/"
      "01_completed_human_technical_review.v2.md"
)

review_record = (
    repo
    / "evidence/annotation_preparation/"
      "curl_technical_protocol_working_draft_v2/"
      "completed_human_review_v2/"
      "02_completed_human_technical_review_record.v1.json"
)

review_verify = (
    repo
    / "evidence/annotation_preparation/"
      "curl_technical_protocol_working_draft_v2/"
      "completed_human_review_v2/"
      "03_verify_completed_human_technical_review.v1.py"
)

auth_path = here / "01_v3_successor_authorization.v1.json"

decision = (
    repo
    / "documentation/decisions/"
      "0032-curl-technical-working-draft-v3-successor-authorization.md"
)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


if sha(v2) != V2_SHA:
    fail("V2_SHA256")

if sha(review) != REVIEW_SHA:
    fail("COMPLETED_REVIEW_SHA256")


cp = subprocess.run(
    [sys.executable, str(review_verify)],
    cwd=str(review_verify.parent),
)

if cp.returncode != 0:
    fail("COMPLETED_V2_HUMAN_REVIEW_VERIFY")


rr = json.loads(
    review_record.read_text(encoding="utf-8")
)

if (
    rr["completed_human_review"]["overall_decision"]
    != "REVISION_REQUIRED"
):
    fail("PREDECESSOR_OVERALL_DECISION")

if (
    rr["review_target"]["working_draft_sha256"]
    != V2_SHA
):
    fail("PREDECESSOR_V2_SHA_BINDING")


expected_revision_items = {
    "V2-RR05",
    "V2-RR06",
    "V2-RR09",
    "V2-RR10",
    "V2-RR12",
}

actual_revision_items = {
    k
    for k, v in
    rr["completed_human_review"]["review_item_decisions"].items()
    if v == "REVISION_REQUIRED"
}

if actual_revision_items != expected_revision_items:
    fail(
        "REVISION_REQUIRED_ITEM_SET|"
        + repr(sorted(actual_revision_items))
    )


auth = json.loads(
    auth_path.read_text(encoding="utf-8")
)

if (
    auth["authorization_type"]
    != "IMMUTABLE_SUCCESSOR_AUTHORING_ONLY"
):
    fail("AUTHORIZATION_TYPE")

if (
    auth["predecessor"]["sha256"]
    != V2_SHA
):
    fail("AUTHORIZATION_PREDECESSOR_SHA")

if (
    auth["predecessor"]["completed_human_review_commit"]
    != EXPECTED_REVIEW_COMMIT
):
    fail("AUTHORIZATION_REVIEW_COMMIT")

if (
    auth["predecessor"]["completed_human_review_tree"]
    != EXPECTED_REVIEW_TREE
):
    fail("AUTHORIZATION_REVIEW_TREE")

if (
    auth["predecessor"]["completed_human_review_sha256"]
    != REVIEW_SHA
):
    fail("AUTHORIZATION_REVIEW_SHA")

if (
    auth["predecessor"]["overall_decision"]
    != "REVISION_REQUIRED"
):
    fail("AUTHORIZATION_PREDECESSOR_DECISION")


successor = auth["authorized_successor"]

if successor["path"] != (
    "config/annotation/curl_technical_protocol_working_draft.v3.json"
):
    fail("SUCCESSOR_PATH")

if successor["schema_id"] != (
    "curl.technical-protocol-working-draft.v3"
):
    fail("SUCCESSOR_SCHEMA")

if successor["authoring_authorized"] is not True:
    fail("SUCCESSOR_AUTHORING_AUTHORIZATION")

if successor["predecessor_in_place_edit_authorized"] is not False:
    fail("V2_IN_PLACE_EDIT_BOUNDARY")

if successor["canonicalization_authorized"] is not False:
    fail("CANONICALIZATION_BOUNDARY")


expected_sources = [
    "V2-RR05",
    "V2-RR06",
    "V2-RR09",
    "V2-RR10",
    "V2-RR12",
]

if auth["authorized_correction_sources"] != expected_sources:
    fail("AUTHORIZED_CORRECTION_SOURCE_SET")


corrections = auth["required_successor_corrections"]

if len(corrections) != 8:
    fail("REQUIRED_CORRECTION_COUNT")

ids = [x["id"] for x in corrections]

if ids != [
    "V3-C01",
    "V3-C02",
    "V3-C03",
    "V3-C04",
    "V3-C05",
    "V3-C06",
    "V3-C07",
    "V3-C08",
]:
    fail("REQUIRED_CORRECTION_IDS")


preserve = auth["must_preserve"]

expected_surface = [
    "curl_global_init",
    "curl_global_cleanup",
    "curl_easy_init",
    "curl_easy_setopt",
    "curl_easy_perform",
    "curl_easy_reset",
    "curl_easy_cleanup",
    "curl_multi_init",
    "curl_multi_add_handle",
    "curl_multi_perform",
    "curl_multi_remove_handle",
    "curl_multi_cleanup",
]

if preserve["frozen_api_surface"] != expected_surface:
    fail("FROZEN_API_SURFACE")

if preserve["frozen_api_surface_function_count"] != 12:
    fail("FROZEN_API_SURFACE_COUNT")

if preserve["approved_source_evidence_class"] != (
    "PREAPPROVED_SOURCE_ONLY"
):
    fail("APPROVED_SOURCE_EVIDENCE_CLASS")

if preserve["approved_source_file_count"] != 21:
    fail("APPROVED_SOURCE_FILE_COUNT")

if preserve["allowed_machine_verdicts"] != [
    "VALID",
    "VIOLATION-MUST",
    "VIOLATION-MAY",
    "UNKNOWN",
]:
    fail("MACHINE_VERDICT_SET")

if preserve["v2_immutable"] is not True:
    fail("V2_IMMUTABILITY")

if preserve["synthetic_protocol_events_may_be_invented"] is not False:
    fail("SYNTHETIC_PROTOCOL_EVENT_BOUNDARY")


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
    "only_review_required_successor_corrections_may_change_semantics",
    "no_new_api_function",
    "no_new_evidence_class",
    "no_generated_driver_derived_rule",
    "v3_must_be_a_new_file",
    "v2_must_not_be_modified",
    "v3_requires_new_author_checkpoint_before_independent_review",
):
    if constraints.get(key) is not True:
        fail("AUTHORING_CONSTRAINT|" + key)


if auth["next_boundary"] != (
    "AUTHOR_CURL_TECHNICAL_WORKING_DRAFT_V3_SUCCESSOR"
):
    fail("NEXT_BOUNDARY")


if not decision.is_file():
    fail("DECISION_0032_MISSING")

dtext = decision.read_text(encoding="utf-8")

for marker in (
    V2_SHA,
    REVIEW_SHA,
    EXPECTED_REVIEW_COMMIT,
    "REVISION_REQUIRED",
    "V2-RR05",
    "V2-RR06",
    "V2-RR09",
    "V2-RR10",
    "V2-RR12",
    "PREAPPROVED_SOURCE_ONLY",
    "AUTHOR_CURL_TECHNICAL_WORKING_DRAFT_V3_SUCCESSOR",
):
    if marker not in dtext:
        fail("DECISION_0032_BINDING|" + marker)


# This verifier is for authorization state only.
# Before V3 authoring begins, V3 must not already exist.
if v3.exists():
    fail("V3_DRAFT_PREMATURELY_EXISTS")


print("V2_IMMUTABILITY_SHA256=PASS")
print("COMPLETED_V2_HUMAN_REVIEW_BINDING=PASS")
print("PREDECESSOR_DECISION=REVISION_REQUIRED")
print("AUTHORIZED_REVISION_ITEMS=V2-RR05,V2-RR06,V2-RR09,V2-RR10,V2-RR12")
print("REQUIRED_V3_CORRECTIONS=8")
print("FROZEN_TWELVE_FUNCTION_SURFACE=PASS")
print("APPROVED_SOURCE_EVIDENCE_CLASS=PREAPPROVED_SOURCE_ONLY")
print("APPROVED_SOURCE_FILES=21")
print("FOUR_MACHINE_VERDICT_CONTRACT=PASS")
print("V2_IN_PLACE_EDIT_AUTHORIZED=NO")
print("V3_SUCCESSOR_AUTHORING_AUTHORIZED=YES")
print("V3_WORKING_DRAFT_ALREADY_CREATED=NO")
print("CANONICAL_CURL_SPECIFICATION_AUTHORIZED=NO")
print("GENERATED_DRIVER_INSPECTION_AUTHORIZED=NO")
print("SELECTED_SAMPLE_MEMBERSHIP_INSPECTION_AUTHORIZED=NO")
print("GOLD_ANNOTATION_AUTHORIZED=NO")
print("ANALYZER_IMPLEMENTATION_AUTHORIZED=NO")
print("ANALYZER_EXECUTION_AUTHORIZED=NO")
print("BASELINE_EXECUTION_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
print("CURL_TECHNICAL_V3_SUCCESSOR_AUTHORIZATION_VERIFICATION=PASS")
