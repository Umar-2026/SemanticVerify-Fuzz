#!/usr/bin/env python3

import hashlib
import json
import subprocess
from pathlib import Path

REPO = Path(
    "/openbayes/home/semanticverify-fuzz-research"
)

HERE = Path(__file__).resolve().parent

AUTH = HERE / \
    "01_corrective_review_package_v2_authorization.v1.json"

REVIEW_RECORD = (
    REPO
    / "evidence/annotation_preparation/protocol_specification_schema_successor_v2"
    / "schema_v2_residual_losslessness_insufficiency_human_review_v1"
)

REVIEW_VERIFY = REVIEW_RECORD / \
    "03_verify_completed_residual_schema_v2_insufficiency_human_review.v1.py"

def fail(msg):
    print("FAIL|" + msg)
    raise SystemExit(1)

def sha(path):
    if not path.is_file():
        fail("MISSING|" + str(path))

    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()

r = json.loads(
    AUTH.read_text(
        encoding="utf-8"
    )
)

if r["authorization_type"] != \
   "PRE_CORRECTIVE_PACKAGE_AUTHORING_ONLY":
    fail("AUTHORIZATION_TYPE")

if r["status"] != \
   "AUTHORIZED_TO_AUTHOR_EVIDENCE_ONLY_CORRECTIVE_REVIEW_PACKAGE_V2_FOR_RI01_ONLY":
    fail("STATUS")

subprocess.run(
    [
        "python3",
        str(REVIEW_VERIFY),
    ],
    check=True,
    stdout=subprocess.DEVNULL,
)

if r[
    "human_review_basis"
]["overall_decision"] != "REVISION_REQUIRED":
    fail("OVERALL_DECISION")

if r[
    "human_review_basis"
]["RI01"] != "REVISION_REQUIRED":
    fail("RI01_DECISION")

if r[
    "human_review_basis"
]["RI02_to_RI08"] != "PASS_CLOSED":
    fail("RI02_TO_RI08")

for key in (
    "schema_v2_approval_record",
    "focused_activation_artifact_approval_record",
    "explicit_activation_authorization_record",
    "schema_v2_activation_decision",
    "activation_execution_record",
):
    item = r[
        "required_corrective_evidence"
    ][key]

    path = REPO / item["path"]

    if sha(path) != item["sha256"]:
        fail(
            "CORRECTIVE_EVIDENCE_SHA|"
            + key
        )

git = r[
    "required_corrective_evidence"
]["activation_git_provenance"]

commit = git["commit"]

object_type = subprocess.check_output(
    [
        "git",
        "-C",
        str(REPO),
        "cat-file",
        "-t",
        commit,
    ],
    text=True,
).strip()

if object_type != "commit":
    fail("ACTIVATION_COMMIT_OBJECT")

tree = subprocess.check_output(
    [
        "git",
        "-C",
        str(REPO),
        "rev-parse",
        commit + "^{tree}",
    ],
    text=True,
).strip()

if tree != git["tree"]:
    fail("ACTIVATION_TREE")

parent = subprocess.check_output(
    [
        "git",
        "-C",
        str(REPO),
        "show",
        "-s",
        "--format=%P",
        commit,
    ],
    text=True,
).strip()

if parent != git["parent"]:
    fail("ACTIVATION_PARENT")

target = REPO / r[
    "authorized_corrective_package"
]["target_path"]

if target.exists():
    fail("CORRECTIVE_PACKAGE_ALREADY_EXISTS")

if r[
    "authorized_corrective_package"
]["evidence_only"] is not True:
    fail("NOT_EVIDENCE_ONLY")

if r[
    "authorized_corrective_package"
]["RI01_focused_rereview_only"] is not True:
    fail("NOT_RI01_ONLY")

for key, value in r[
    "explicit_non_authorizations"
].items():
    if value is not False:
        fail("NONAUTH|" + key)

for key, value in r[
    "retired_verifier_constraints"
].items():
    if value is not False:
        fail("RETIRED_VERIFIER|" + key)

for forbidden in (
    "config/protocol_specifications/curl.json",
    "config/annotation/curl_positive_v4_to_v2_mapping_contract.v1.json",
    "config/schemas/protocol_specification.v3.schema.json",
):
    if (
        REPO /
        forbidden
    ).exists():
        fail(
            "FORBIDDEN_ARTIFACT|"
            + forbidden
        )

print("COMPLETED_HUMAN_REVIEW_RECORD=PASS")
print("OVERALL_HUMAN_DECISION=REVISION_REQUIRED")
print("RI01=REVISION_REQUIRED")
print("RI02_TO_RI08_PASS_CLOSED=YES")
print("CORRECTIVE_SCOPE=ACTIVATION_AND_PROVENANCE_EVIDENCE_ONLY")
print("SCHEMA_V2_APPROVAL_RECORD_BOUND=YES")
print("ACTIVATION_APPROVAL_LINEAGE_BOUND=YES")
print("DECISION_0066_ACTIVATION_RECORD_BOUND=YES")
print("ACTIVATION_EXECUTION_RECORD_BOUND=YES")
print("ACTIVATION_GIT_COMMIT_TREE_PARENT_PROVENANCE=PASS")
print("CORRECTIVE_PACKAGE_V2_AUTHORING_AUTHORIZED=YES")
print("SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO")
print("POSITIVE_MAPPING_AUTHORIZED=NO")
print("CURL_JSON_CREATED=NO")
print("DECISION_0071_CORRECTIVE_PACKAGE_V2_AUTHORIZATION=PASS")
print("IMPORTANT=THIS_VERIFIER_IS_PRE_CORRECTIVE_PACKAGE_AUTHORING_ONLY")
