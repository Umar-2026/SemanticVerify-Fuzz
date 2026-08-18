#!/usr/bin/env python3

import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]

V3 = REPO / "config/annotation/curl_v3_authoring_scope.v3.json"

FREEZE = (
    REPO /
    "evidence/annotation_preparation/"
    "curl_v3_authoring_scope_successor/"
    "scope_freeze_v3/"
    "01_scope_freeze_record.v3.json"
)

D26 = (
    REPO /
    "documentation/decisions/"
    "0026-curl-v3-post-freeze-technical-working-draft-authorization.md"
)

RECORD = HERE / "01_working_draft_authorization.v1.json"

V3_SHA = "ede7e1422b9553f73377432474deb282852b619a5b004cd7c4d00033c0a37abb"
V3_COMMIT = "7de6fc01797ae68cbd64406b850a3198f71cc702"
V3_TREE = "c5f96b844e5803cccd04c9f64a55754dc6c77e20"
V3_PATH = "config/annotation/curl_v3_authoring_scope.v3.json"
V3_BLOB = "931c24cc46c99f23ee352455d3e8c93e57e63401"


def fail(msg):
    print("FAIL|" + msg)
    raise SystemExit(1)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


if sha(V3) != V3_SHA:
    fail("V3_SHA256_MISMATCH")

tree = subprocess.check_output(
    ["git", "-C", str(REPO), "rev-parse", V3_COMMIT + "^{tree}"],
    text=True,
).strip()

if tree != V3_TREE:
    fail("V3_TREE_MISMATCH")

blob = subprocess.check_output(
    ["git", "-C", str(REPO), "rev-parse", V3_COMMIT + ":" + V3_PATH],
    text=True,
).strip()

if blob != V3_BLOB:
    fail("V3_BLOB_MISMATCH")

freeze = json.loads(FREEZE.read_text(encoding="utf-8"))

freeze_state = freeze.get("authorization_state_after_freeze", {})

if freeze.get("status") != "FROZEN":
    fail("FREEZE_STATUS")

if freeze_state.get("v3_scope_frozen") is not True:
    fail("V3_SCOPE_NOT_FROZEN")

if freeze_state.get("technical_working_draft_authorized") is not False:
    fail("FREEZE_RECORD_MUST_PRECEDE_SEPARATE_DRAFT_AUTHORIZATION")

record = json.loads(RECORD.read_text(encoding="utf-8"))

if record.get("status") != "TECHNICAL_WORKING_DRAFT_AUTHORIZED":
    fail("AUTHORIZATION_STATUS")

state = record.get("authorization_state", {})

if state.get("v3_scope_freeze_authorized") is not True:
    fail("FREEZE_NOT_AUTHORIZED")

if state.get("v3_scope_frozen") is not True:
    fail("SCOPE_NOT_FROZEN")

if state.get("technical_working_draft_authorized") is not True:
    fail("WORKING_DRAFT_NOT_AUTHORIZED")

for key in (
    "canonical_specification_authorized",
    "generated_driver_inspection_authorized",
    "gold_annotation_authorized",
    "analyzer_implementation_authorized",
    "baseline_execution_authorized",
    "repair_authorized",
):
    if state.get(key) is not False:
        fail("UNEXPECTED_DOWNSTREAM_AUTHORIZATION|" + key)

if (
    record.get(
        "technical_specification_review_required_before_canonicalization"
    )
    is not True
):
    fail("TECHNICAL_REVIEW_REQUIREMENT")

decision = record.get("authorization_decision", {})

if sha(D26) != decision.get("sha256"):
    fail("DECISION_0026_SHA256")

print("EXACT_FROZEN_V3_BINDING=PASS")
print("COMPLETED_SCOPE_FREEZE_PREREQUISITE=PASS")
print("SEPARATE_POST_FREEZE_AUTHORIZATION_BOUNDARY=PASS")
print("TECHNICAL_WORKING_DRAFT_AUTHORIZED=YES")
print("CANONICAL_CURL_SPECIFICATION_AUTHORIZED=NO")
print("GENERATED_DRIVER_INSPECTION_AUTHORIZED=NO")
print("GOLD_ANNOTATION_AUTHORIZED=NO")
print("ANALYZER_IMPLEMENTATION_AUTHORIZED=NO")
print("BASELINE_EXECUTION_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
print("TECHNICAL_SPEC_INDEPENDENT_REVIEW_REQUIRED=YES")
print("CURL_V3_WORKING_DRAFT_AUTHORIZATION_VERIFICATION=PASS")
