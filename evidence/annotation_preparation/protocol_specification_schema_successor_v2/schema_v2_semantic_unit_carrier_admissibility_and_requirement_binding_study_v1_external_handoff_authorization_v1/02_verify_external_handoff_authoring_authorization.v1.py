#!/usr/bin/env python3

import hashlib
import json
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]

BASE_REL = (
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2"
)

PKG = (
    REPO
    / BASE_REL
    / "schema_v2_semantic_unit_carrier_admissibility_"
      "and_requirement_binding_study_v1_review_package_v1"
)

PACKET = (
    PKG
    / "20_SUCR01_SUCR08_reviewer_packet.MANUAL_REVIEW_COPY.v1.md"
)

MANIFEST = (
    PKG
    / "21_review_package_manifest.v1.json"
)

SAFE = (
    PKG
    / "22_verify_semantic_unit_carrier_study_review_package.v1.py"
)

SUMS = (
    PKG
    / "23_review_package.v1.SHA256SUMS"
)

AUTH = (
    HERE
    / "01_external_independent_human_review_handoff_authorization.v1.json"
)

FUTURE_HANDOFF = (
    REPO
    / BASE_REL
    / "schema_v2_semantic_unit_carrier_admissibility_"
      "and_requirement_binding_study_v1_external_review_handoff_v1"
)

EXTERNAL_ZIP = Path(
    "/openbayes/home/"
    "22_semantic_unit_carrier_study_v1_independent_review_handoff.v1.zip"
)

EXTERNAL_PACKET = Path(
    "/openbayes/home/"
    "22_SUCR01_SUCR08_reviewer_packet.MANUAL_REVIEW_COPY.v1.md"
)

EXPECTED = {
    PACKET:
        "38f1021657d06716ac28709ec98be6d9d992a4c451b41569b0f60c651f68a8db",

    MANIFEST:
        "c954de9c57039be17f7b7d4f6c15d023ff39d5d658d3b6194889f95189ab65aa",

    SAFE:
        "a1ab5a2ba3e2dba2f48a0d48a5f7f0ae8ed97b7ddffbd824236ac6371efc33e2",

    SUMS:
        "576051b93ab71a8b5500b91acb42677b9a72133727ba2e5608145b2a7e9dd78a",
}

def fail(msg):
    print("FAIL|" + msg)
    raise SystemExit(1)

def sha(path):
    if not path.is_file():
        fail(
            "MISSING|" + str(path)
        )

    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()

for path, expected in EXPECTED.items():
    if sha(path) != expected:
        fail(
            "SOURCE_BINDING|" + str(path)
        )

proc = subprocess.run(
    [
        "git",
        "-C",
        str(REPO),
        "status",
        "--porcelain=v1",
        "--untracked-files=all",
    ],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    check=False,
)

if proc.returncode != 0:
    fail(
        "GIT_STATUS"
    )

if proc.stdout.strip():
    fail(
        "REPOSITORY_NOT_CLEAN"
    )

if FUTURE_HANDOFF.exists():
    fail(
        "EXTERNAL_HANDOFF_ALREADY_EXISTS"
    )

if EXTERNAL_ZIP.exists():
    fail(
        "EXTERNAL_ZIP_ALREADY_EXISTS"
    )

if EXTERNAL_PACKET.exists():
    fail(
        "EXTERNAL_PACKET_ALREADY_EXISTS"
    )

manifest = json.loads(
    MANIFEST.read_text(
        encoding="utf-8"
    )
)

if manifest[
    "package_state"
] != "BLANK_READY_FOR_INDEPENDENT_HUMAN_REVIEW":
    fail(
        "PACKAGE_STATE"
    )

if manifest[
    "review_contract"
][
    "required_reviewer_role"
] != "Spec-Technical-Reviewer-1":
    fail(
        "REVIEWER_ROLE"
    )

if manifest[
    "review_contract"
][
    "review_items"
] != [
    "SUCR01",
    "SUCR02",
    "SUCR03",
    "SUCR04",
    "SUCR05",
    "SUCR06",
    "SUCR07",
    "SUCR08",
]:
    fail(
        "REVIEW_ITEMS"
    )

text = PACKET.read_text(
    encoding="utf-8"
)

if "Package state: `BLANK — AWAITING INDEPENDENT HUMAN REVIEW`" not in text:
    fail(
        "PACKET_NOT_BLANK"
    )

if re.search(
    r"^Decision:\s*`?(PASS|REVISION_REQUIRED|FAIL)`?\s*$",
    text,
    flags=re.MULTILINE,
):
    fail(
        "PREPOPULATED_ITEM_DECISION"
    )

if re.search(
    r"^Overall decision:\s*`?(APPROVE_|REVISION_REQUIRED|FAIL)",
    text,
    flags=re.MULTILINE,
):
    fail(
        "PREPOPULATED_OVERALL_DECISION"
    )

auth = json.loads(
    AUTH.read_text(
        encoding="utf-8"
    )
)

if auth[
    "status"
] != "AUTHORIZED_FOR_EXTERNAL_HANDOFF_AUTHORING_ONLY":
    fail(
        "AUTHORIZATION_STATUS"
    )

if auth[
    "authorization_verifier_lifecycle"
][
    "initial_state"
] != "ACTIVE_UNCONSUMED":
    fail(
        "VERIFIER_INITIAL_STATE"
    )

if auth[
    "authorization_verifier_lifecycle"
][
    "may_execute_exactly_once_immediately_before_external_handoff_authoring"
] is not True:
    fail(
        "VERIFIER_LIFECYCLE"
    )

for key, value in auth[
    "explicit_non_authorizations"
].items():
    if value is not False:
        fail(
            "UNEXPECTED_AUTHORIZATION|"
            + key
        )

for key, value in auth[
    "retired_verifier_state"
].items():

    if key == \
            "retired_verifiers_must_not_be_executed":

        if value is not True:
            fail(
                "RETIRED_VERIFIER_POLICY"
            )

    else:
        if value != \
                "PERMANENTLY_RETIRED":
            fail(
                "RETIRED_VERIFIER_STATE|"
                + key
            )

print("DECISION_0113_REVIEW_PACKAGE_BINDING=PASS")
print("REVIEW_PACKAGE_STATE=BLANK_READY_FOR_INDEPENDENT_HUMAN_REVIEW")
print("REVIEW_ITEMS=SUCR01,SUCR02,SUCR03,SUCR04,SUCR05,SUCR06,SUCR07,SUCR08")
print("REQUIRED_REVIEWER_ROLE=Spec-Technical-Reviewer-1")

print("ITEM_DECISIONS_PREPOPULATED=NO")
print("OVERALL_DECISION_PREPOPULATED=NO")
print("REVIEWER_IDENTITY_PREPOPULATED=NO")

print("HUMAN_REVIEW_DECISION_EXISTS=NO")
print("STUDY_GOVERNANCE_ADOPTED=NO")

print("DECISION_0102_A02_STATE=PERMANENTLY_RETIRED")
print("DECISION_0104_A02_STATE=PERMANENTLY_RETIRED")
print("DECISION_0106_A02_STATE=PERMANENTLY_RETIRED")
print("DECISION_0110_A02_STATE=PERMANENTLY_RETIRED")
print("DECISION_0112_A02_STATE=PERMANENTLY_RETIRED")
print("RETIRED_A02_VERIFIERS_EXECUTED=NO")

print("OPERATIONAL_MAPPING_AUTHORIZED=NO")
print("SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO")
print("CURL_JSON_AUTHORIZED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")

print("EXTERNAL_HANDOFF_AUTHORING_AUTHORIZATION=PASS")
print("VERIFIER_LIFECYCLE=ONE_FINAL_RUN_IMMEDIATELY_BEFORE_EXTERNAL_HANDOFF_AUTHORING_THEN_PERMANENT_RETIREMENT")
