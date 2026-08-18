#!/usr/bin/env python3

import hashlib
import json
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


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


auth = here / "01_v2_successor_authorization.v1.json"

decision = (
    repo
    / "documentation"
    / "decisions"
    / "0029-curl-technical-working-draft-v2-successor-authorization.md"
)

v1 = (
    repo
    / "config"
    / "annotation"
    / "curl_technical_protocol_working_draft.v1.json"
)

review = (
    repo
    / "evidence"
    / "annotation_preparation"
    / "curl_technical_protocol_working_draft_v1"
    / "completed_human_review_v1"
    / "01_completed_human_technical_review.v1.md"
)

v3 = (
    repo
    / "config"
    / "annotation"
    / "curl_v3_authoring_scope.v3.json"
)

scenario = (
    repo
    / "config"
    / "generation"
    / "scenario_bindings.80.v10.json"
)

expected_v1 = (
    "80498e0c4e021700e2a2c09654a852e67b16df86d61fbb28857d14a12fed44c6"
)

expected_review = (
    "e253340d540a06cd24af501c569154869ac0324d677995b7266349ba097973cc"
)

expected_v3 = (
    "ede7e1422b9553f73377432474deb282852b619a5b004cd7c4d00033c0a37abb"
)

expected_scenario = (
    "a7ab361e6e2d41d9051e48bc7626f0be37c1df9ec35f788a9a019b010054a2db"
)

for path, wanted, label in (
    (v1, expected_v1, "V1"),
    (review, expected_review, "COMPLETED_REVIEW"),
    (v3, expected_v3, "V3_SCOPE"),
    (scenario, expected_scenario, "SCENARIO"),
):
    if not path.is_file():
        fail(label + "_MISSING")

    if sha(path) != wanted:
        fail(label + "_SHA256")


record = json.loads(auth.read_text(encoding="utf-8"))

if record["status"] != "AUTHORIZED_FOR_SOURCE_ONLY_V2_SUCCESSOR_AUTHORING":
    fail("AUTHORIZATION_STATUS")

if (
    record["authorization_basis"]["overall_human_review_decision"]
    != "REVISION_REQUIRED"
):
    fail("HUMAN_REVIEW_DECISION_BINDING")

if (
    record["successor_identity"]["authorized_path"]
    != "config/annotation/curl_technical_protocol_working_draft.v2.json"
):
    fail("V2_AUTHORIZED_PATH")

if (
    record["successor_identity"]["predecessor_must_remain_immutable"]
    is not True
):
    fail("V1_IMMUTABILITY")

required_rr = {
    f"TS-RR{i:02d}"
    for i in range(5, 15)
}

observed_rr = set(
    record["required_human_review_corrections"].keys()
)

if observed_rr != required_rr:
    fail(
        "SUCCESSOR_REQUIREMENT_SET|"
        + repr(sorted(observed_rr))
    )

if (
    record["frozen_invariants"]["api_surface_function_count"]
    != 12
):
    fail("API_SURFACE_COUNT")

for key in (
    "api_surface_changes_authorized",
    "pinned_curl_revision_changes_authorized",
    "scenario_manifest_changes_authorized",
    "approved_source_evidence_class_changes_authorized",
    "generated_driver_evidence_authorized",
):
    if record["frozen_invariants"][key] is not False:
        fail("FROZEN_INVARIANT_CHANGED|" + key)

if record["authorization"]["v2_successor_authoring_authorized"] is not True:
    fail("V2_AUTHORING_NOT_AUTHORIZED")

if record["authorization"]["v2_author_checkpoint_authorized"] is not True:
    fail("V2_AUTHOR_CHECKPOINT_NOT_AUTHORIZED")

for key in (
    "v1_in_place_edit_authorized",
    "canonical_curl_specification_authorized",
    "generated_driver_inspection_authorized",
    "selected_sample_membership_inspection_authorized",
    "gold_annotation_authorized",
    "analyzer_implementation_authorized",
    "baseline_execution_authorized",
    "repair_authorized",
):
    if record["authorization"][key] is not False:
        fail("BLOCKED_BOUNDARY_CHANGED|" + key)

if not decision.is_file():
    fail("DECISION_0029_MISSING")

dtext = decision.read_text(encoding="utf-8")

for required in (
    expected_v1,
    expected_review,
    "REVISION_REQUIRED",
    "curl_technical_protocol_working_draft.v2.json",
    "CREATE_CURL_TECHNICAL_WORKING_DRAFT_V2_SUCCESSOR_AUTHOR_CHECKPOINT",
):
    if required not in dtext:
        fail("DECISION_0029_BINDING|" + required)

print("V1_WORKING_DRAFT_SHA256_BINDING=PASS")
print("COMPLETED_HUMAN_REVIEW_SHA256_BINDING=PASS")
print("FROZEN_V3_SCOPE_SHA256_BINDING=PASS")
print("SCENARIO_MANIFEST_SHA256_BINDING=PASS")
print("TS_RR05_TO_TS_RR14_SUCCESSOR_REQUIREMENTS=PASS")
print("EXACT_TWELVE_FUNCTION_SURFACE_FROZEN=YES")
print("V1_IN_PLACE_EDIT_AUTHORIZED=NO")
print("V2_SUCCESSOR_AUTHORING_AUTHORIZED=YES")
print("V2_AUTHOR_CHECKPOINT_AUTHORIZED=YES")
print("CANONICAL_CURL_SPECIFICATION_AUTHORIZED=NO")
print("GENERATED_DRIVER_INSPECTION_AUTHORIZED=NO")
print("SELECTED_SAMPLE_MEMBERSHIP_INSPECTION_AUTHORIZED=NO")
print("GOLD_ANNOTATION_AUTHORIZED=NO")
print("ANALYZER_IMPLEMENTATION_AUTHORIZED=NO")
print("BASELINE_EXECUTION_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
print("CURL_TECHNICAL_V2_SUCCESSOR_AUTHORIZATION_VERIFICATION=PASS")
