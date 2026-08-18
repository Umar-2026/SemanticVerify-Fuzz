#!/usr/bin/env python3

import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]

V3 = REPO / "config/annotation/curl_v3_authoring_scope.v3.json"

D25 = (
    REPO /
    "documentation/decisions/"
    "0025-curl-v3-exact-source-only-authoring-scope-freeze.md"
)

RECORD = HERE / "01_scope_freeze_record.v3.json"

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
    [
        "git",
        "-C",
        str(REPO),
        "rev-parse",
        V3_COMMIT + ":" + V3_PATH,
    ],
    text=True,
).strip()

if blob != V3_BLOB:
    fail("V3_BLOB_MISMATCH")

blob_bytes = subprocess.check_output(
    ["git", "-C", str(REPO), "cat-file", "blob", V3_BLOB]
)

if hashlib.sha256(blob_bytes).hexdigest() != V3_SHA:
    fail("V3_COMMITTED_CONTENT_SHA_MISMATCH")

record = json.loads(RECORD.read_text(encoding="utf-8"))

if record.get("status") != "FROZEN":
    fail("FREEZE_STATUS")

scope = record.get("exact_frozen_scope", {})

expected_scope = {
    "path": V3_PATH,
    "sha256": V3_SHA,
    "author_checkpoint_commit": V3_COMMIT,
    "author_checkpoint_tree": V3_TREE,
    "git_blob": V3_BLOB,
    "bytes_modified_by_freeze": False,
    "edit_in_place_allowed_after_freeze": False,
}

if scope != expected_scope:
    fail("EXACT_FROZEN_SCOPE_RECORD")

approval = record.get("human_freeze_authorization", {})

if approval.get("RR01-R1") != "PASS":
    fail("RR01_R1")
if approval.get("RR01-R2") != "PASS":
    fail("RR01_R2")
if approval.get("RR01-R3") != "PASS":
    fail("RR01_R3")
if approval.get("RR01-R4") != "PASS":
    fail("RR01_R4")

if (
    approval.get("overall")
    != "APPROVE_EXACT_V3_SCOPE_FOR_FREEZE"
):
    fail("OVERALL_HUMAN_APPROVAL")

state = record.get("authorization_state_after_freeze", {})

if state.get("v3_scope_freeze_authorized") is not True:
    fail("FREEZE_AUTHORIZED")

if state.get("v3_scope_frozen") is not True:
    fail("SCOPE_NOT_FROZEN")

for key in (
    "technical_working_draft_authorized",
    "canonical_specification_authorized",
    "generated_driver_inspection_authorized",
    "gold_annotation_authorized",
    "analyzer_implementation_authorized",
    "baseline_execution_authorized",
    "repair_authorized",
):
    if state.get(key) is not False:
        fail("UNEXPECTED_DOWNSTREAM_AUTHORIZATION|" + key)

if record.get("technical_working_draft_authorization_is_automatic") is not False:
    fail("TECHNICAL_DRAFT_AUTO_AUTHORIZATION")

decision = record.get("governance_decision", {})

if sha(D25) != decision.get("sha256"):
    fail("DECISION_0025_SHA256")

print("EXACT_V3_SCOPE_BYTE_IDENTITY=PASS")
print("V3_COMMIT_TREE_PATH_BLOB_SHA_CHAIN=PASS")
print("REAL_HUMAN_FREEZE_AUTHORIZATION_BINDING=PASS")
print("DECISION_0025_BINDING=PASS")
print("V3_SCOPE_FREEZE_AUTHORIZED=YES")
print("V3_SCOPE_FROZEN=YES")
print("TECHNICAL_WORKING_DRAFT_AUTHORIZED=NO")
print("CANONICAL_CURL_SPECIFICATION_AUTHORIZED=NO")
print("GENERATED_DRIVER_INSPECTION_AUTHORIZED=NO")
print("GOLD_ANNOTATION_AUTHORIZED=NO")
print("ANALYZER_IMPLEMENTATION_AUTHORIZED=NO")
print("BASELINE_EXECUTION_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
print("EXACT_CURL_V3_SCOPE_FREEZE_VERIFICATION=PASS")
