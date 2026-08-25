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

HANDOFF_REL = (
    BASE_REL
    + "/schema_v2_requirement_bound_carrier_admissibility_resolution_study_v1_external_handoff_v1"
)

THIS_AUTH_REL = (
    BASE_REL
    + "/schema_v2_requirement_bound_carrier_admissibility_resolution_study_v1_completed_human_review_recording_authorization_v1"
)

HANDOFF = REPO / HANDOFF_REL

HANDOFF_SAFE = (
    HANDOFF
    / "08_verify_external_RBCA01_RBCA08_handoff.v1.py"
)

BLANK = (
    HANDOFF
    / "03_RBCA01_RBCA08_reviewer_packet.INITIAL_BLANK_EXACT_COPY.v1.md"
)

RETURNED = Path(
    "/openbayes/home/36_manually_RBCA01_RBCA08_reviewer_packet.MANUAL_REVIEW_COPY.v1.md"
)

AUTH = (
    HERE
    / "01_completed_human_review_recording_authorization.v1.json"
)

EXPECTED_DECISION0142 = (
    "8e7cc325bbea4042bef8403b7f6e853c52456f38"
)

EXPECTED_HANDOFF_TREE = (
    "03cc454e001392c08684cb5f7b0483f10e529bb8"
)

EXPECTED_RETURNED_SHA = (
    "9ded6b54b04c438a9a0f5ac3b7557d5ab19283c812fa5f2f6b529c92ef2e7eb1"
)

EXPECTED_RETURNED_SIZE = 8794

EXPECTED_OVERALL = (
    "APPROVE_REQUIREMENT_BOUND_CARRIER_ADMISSIBILITY_RESOLUTION_STUDY_V1"
)

EXPECTED_NAME = "Abdul Raheem Shahzad"
EXPECTED_CONFIRMATION = "ARS"
EXPECTED_DATE = "24 / August / 2026"
EXPECTED_ROLE = "Spec-Technical-Reviewer-1"

def fail(msg):
    print("FAIL|" + msg)
    raise SystemExit(1)

def sha(path):
    if not path.is_file():
        fail(
            "MISSING|"
            + str(path)
        )

    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()

def git(*args):
    p = subprocess.run(
        ["git", "-C", str(REPO), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )

    if p.returncode != 0:
        fail(
            "GIT|"
            + " ".join(args)
            + "|"
            + p.stderr.strip()
        )

    return p.stdout.strip()

current_head = git(
    "rev-parse",
    "HEAD",
)

current_parent = git(
    "show",
    "-s",
    "--format=%P",
    "HEAD",
)

if current_head == EXPECTED_DECISION0142:
    fail(
        "RECORDING_AUTHORIZATION_NOT_COMMITTED"
    )

if current_parent != EXPECTED_DECISION0142:
    fail(
        "CURRENT_HEAD_IS_NOT_IMMEDIATE_SUCCESSOR_OF_DECISION0142"
    )

if (
    git(
        "rev-parse",
        "HEAD:" + HANDOFF_REL,
    )
    != EXPECTED_HANDOFF_TREE
):
    fail(
        "HANDOFF_GIT_TREE"
    )

git(
    "cat-file",
    "-e",
    "HEAD:" + THIS_AUTH_REL,
)

if git(
    "status",
    "--porcelain=v1",
    "--untracked-files=all",
):
    fail(
        "REPOSITORY_NOT_CLEAN"
    )

auth = json.loads(
    AUTH.read_text(
        encoding="utf-8"
    )
)

if (
    auth["authorization_type"]
    != "PRE_COMPLETED_HUMAN_REVIEW_RECORDING_ONLY"
):
    fail(
        "AUTHORIZATION_TYPE"
    )

if (
    auth["status"]
    != "AUTHORIZED_NOT_YET_RECORDED"
):
    fail(
        "AUTHORIZATION_STATUS"
    )

if sha(RETURNED) != EXPECTED_RETURNED_SHA:
    fail(
        "RETURNED_PACKET_SHA"
    )

if RETURNED.stat().st_size != EXPECTED_RETURNED_SIZE:
    fail(
        "RETURNED_PACKET_SIZE"
    )

review = RETURNED.read_text(
    encoding="utf-8"
)

blank = BLANK.read_text(
    encoding="utf-8"
)

headings = re.findall(
    r"^## RBCA\d{2} — .+$",
    blank,
    flags=re.MULTILINE,
)

if len(headings) != 8:
    fail(
        "BLANK_HEADING_COUNT"
    )

for heading in headings:
    if heading not in review:
        fail(
            "REVIEW_HEADING|"
            + heading
        )

decisions = re.findall(
    r"^Decision:\s*`(PASS|REVISION_REQUIRED|FAIL)`\s*$",
    review,
    flags=re.MULTILINE,
)

if decisions != ["PASS"] * 8:
    fail(
        "RBCA_DECISIONS"
    )

overall = re.findall(
    r"^Overall decision:\s*`([^`]+)`\s*$",
    review,
    flags=re.MULTILINE,
)

if overall != [EXPECTED_OVERALL]:
    fail(
        "OVERALL_DECISION"
    )

def field(label):
    matches = re.findall(
        rf"^{re.escape(label)}\s*(.+)$",
        review,
        flags=re.MULTILINE,
    )

    if len(matches) != 1:
        fail(
            "METADATA|"
            + label
        )

    return matches[0].strip()

if field("Human reviewer name:") != EXPECTED_NAME:
    fail(
        "REVIEWER_NAME"
    )

if (
    field(
        "Human reviewer signature / recorded confirmation:"
    )
    != EXPECTED_CONFIRMATION
):
    fail(
        "REVIEWER_CONFIRMATION"
    )

if field("Human reviewer date:") != EXPECTED_DATE:
    fail(
        "REVIEWER_DATE"
    )

if field("Reviewer role:") != EXPECTED_ROLE:
    fail(
        "REVIEWER_ROLE"
    )

for phrase in (
    "does not establish Schema-V2 losslessness",
    "resolve carrier admissibility",
    "positive mapping",
    "negative mapping impossibility",
    "whole-V4 admissible-composition exhaustiveness",
):
    if phrase not in review:
        fail(
            "BOUNDED_NONCLAIM|"
            + phrase
        )

for key, value in auth[
    "technical_nonclaims_preserved"
].items():
    if value is not False:
        fail(
            "UNEXPECTED_TECHNICAL_CLAIM|"
            + key
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
    "retired_verifier_policy"
].items():
    if value is not False:
        fail(
            "RETIRED_A02_RERUN_ALLOWED|"
            + key
        )

p = subprocess.run(
    [
        "python3",
        str(HANDOFF_SAFE),
    ],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    check=False,
)

if p.returncode != 0:
    fail(
        "HANDOFF_SAFE_VERIFIER|"
        + p.stdout
        + p.stderr
    )

for marker in (
    "EXTERNAL_RBCA01_RBCA08_HANDOFF_V1=PASS",
    "REVIEWER_PACKET_INITIAL_BLANK_STATE=PASS",
    "HUMAN_REVIEW_PERFORMED=NO",
    "STUDY_OUTCOME_UNDER_REVIEW=FURTHER_EVIDENCE_REQUIRED",
    "UNRESOLVED_COUNT=17",
    "STUDY_GOVERNANCE_ADOPTED=NO",
    "DECISION_0141_A02_STATE=PERMANENTLY_RETIRED",
    "DECISION_0141_A02_EXECUTED_BY_SAFE_VERIFIER=NO",
    "RETIRED_A02_VERIFIERS_EXECUTED=NO",
):
    if marker not in p.stdout:
        fail(
            "HANDOFF_SAFE_MARKER|"
            + marker
        )

print(
    "COMPLETED_RBCA01_RBCA08_HUMAN_REVIEW_RECORDING_AUTHORIZATION=PASS"
)

print(
    "CURRENT_CHECKPOINT_ROLE="
    "IMMEDIATE_SUCCESSOR_OF_DECISION0142"
)

print(
    "CURRENT_HEAD_PARENT_DECISION0142_BINDING=PASS"
)

print(
    "RETURNED_REVIEW_SHA256="
    + EXPECTED_RETURNED_SHA
)

print(
    "RETURNED_REVIEW_SIZE=8794"
)

print(
    "RBCA01_RBCA08_PASS_COUNT=8"
)

print(
    "RBCA_REVISION_REQUIRED_COUNT=0"
)

print(
    "RBCA_FAIL_COUNT=0"
)

print(
    "OVERALL_REVIEW_DECISION="
    + EXPECTED_OVERALL
)

print(
    "REVIEWER_NAME="
    + EXPECTED_NAME
)

print(
    "REVIEWER_CONFIRMATION="
    + EXPECTED_CONFIRMATION
)

print(
    "REVIEWER_DATE="
    + EXPECTED_DATE
)

print(
    "REVIEWER_ROLE="
    + EXPECTED_ROLE
)

print(
    "REVIEWER_DECISION_SYNTHESIZED=NO"
)

print(
    "REVIEWER_IDENTITY_SYNTHESIZED=NO"
)

print(
    "HUMAN_REVIEW_COMPLETED=YES"
)

print(
    "HUMAN_REVIEW_RECORDED_IN_REPOSITORY=NO"
)

print(
    "STUDY_GOVERNANCE_ADOPTED=NO"
)

print(
    "CARRIER_ADMISSIBILITY_RESOLVED=NO"
)

print(
    "POSITIVE_MAPPING_PROVEN=NO"
)

print(
    "NEGATIVE_MAPPING_IMPOSSIBILITY_PROVEN=NO"
)

print(
    "WHOLE_V4_EXHAUSTIVENESS_PROVEN=NO"
)

print(
    "OPERATIONAL_MAPPING_AUTHORIZED=NO"
)

print(
    "SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO"
)

print(
    "CURL_JSON_AUTHORIZED=NO"
)

print(
    "ANALYZER_AUTHORIZED=NO"
)

print(
    "BASELINE_AUTHORIZED=NO"
)

print(
    "REPAIR_AUTHORIZED=NO"
)

print(
    "RETIRED_A02_VERIFIERS_EXECUTED=NO"
)

print(
    "VERIFIER_LIFECYCLE="
    "ONE_FINAL_RUN_IMMEDIATELY_BEFORE_COMPLETED_RBCA01_RBCA08_HUMAN_REVIEW_RECORD_AUTHORING_THEN_PERMANENT_RETIREMENT"
)
