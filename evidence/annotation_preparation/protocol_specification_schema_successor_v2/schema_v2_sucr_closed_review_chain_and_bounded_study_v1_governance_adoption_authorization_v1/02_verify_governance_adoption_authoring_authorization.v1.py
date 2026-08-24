#!/usr/bin/env python3

import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]

BASE = (
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2"
)

AUTH = (
    HERE
    / "01_governance_adoption_authorization.v1.json"
)

CLOSURE_REL = (
    BASE
    + "/schema_v2_sucr_review_chain_closure_assessment_v1"
)

CLOSURE = (
    REPO
    / CLOSURE_REL
    / "01_review_chain_closure_assessment.v1.json"
)

FUTURE = (
    REPO
    / BASE
    / "schema_v2_sucr_closed_review_chain_and_bounded_study_v1_governance_adoption_v1"
)

def fail(msg):
    print("FAIL|" + msg)
    raise SystemExit(1)

def git_object(rel):
    p = subprocess.run(
        [
            "git",
            "-C",
            str(REPO),
            "rev-parse",
            "HEAD:" + rel,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )

    if p.returncode != 0:
        fail(
            "GIT_OBJECT|" + rel
        )

    return p.stdout.strip()

p = subprocess.run(
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

if p.returncode != 0:
    fail("GIT_STATUS")

if p.stdout.strip():
    fail(
        "REPOSITORY_NOT_CLEAN"
    )

if FUTURE.exists():
    fail(
        "GOVERNANCE_ADOPTION_ALREADY_EXISTS"
    )

if git_object(
    CLOSURE_REL
) != "18d6b1b77994d6827b878a498e1556487921fda7":
    fail(
        "CLOSURE_ASSESSMENT_TREE"
    )

a = json.loads(
    AUTH.read_text(
        encoding="utf-8"
    )
)

if a[
    "status"
] != "AUTHORIZED_FOR_GOVERNANCE_ADOPTION_AUTHORING_ONLY":
    fail(
        "AUTHORIZATION_STATUS"
    )

review = a[
    "review_chain_state"
]

if review[
    "closure_assessment_outcome"
] != "PASS_CLOSED":
    fail(
        "REVIEW_CHAIN_OUTCOME"
    )

if review[
    "review_chain_closed"
] is not True:
    fail(
        "REVIEW_CHAIN_NOT_CLOSED"
    )

study = a[
    "study_state_before_governance_adoption"
]

if study[
    "artifact_status"
] != "AUTHOR_CANDIDATE":
    fail(
        "STUDY_ARTIFACT_STATUS"
    )

if study[
    "bounded_technical_outcome"
] != "FURTHER_EVIDENCE_REQUIRED":
    fail(
        "BOUNDED_TECHNICAL_OUTCOME"
    )

if study[
    "governance_adopted"
] is not False:
    fail(
        "GOVERNANCE_ALREADY_ADOPTED"
    )

contract = a[
    "governance_adoption_contract"
]

if contract[
    "authorized_governance_status"
] != "APPROVED_WITH_BOUNDED_TECHNICAL_OUTCOME":
    fail(
        "AUTHORIZED_GOVERNANCE_STATUS"
    )

if contract[
    "adopted_bounded_technical_outcome"
] != "FURTHER_EVIDENCE_REQUIRED":
    fail(
        "AUTHORIZED_BOUNDED_OUTCOME"
    )

for key, value in contract.items():

    if key in (
        "authorized_governance_status",
        "adopted_bounded_technical_outcome",
    ):
        continue

    if value is not True:
        fail(
            "GOVERNANCE_CONTRACT|"
            + key
        )

pre = a[
    "pre_adoption_state"
]

if pre[
    "governance_adoption_authorized"
] is not True:
    fail(
        "GOVERNANCE_NOT_AUTHORIZED"
    )

if pre[
    "governance_adoption_authored"
] is not False:
    fail(
        "PREMATURE_GOVERNANCE_ADOPTION"
    )

if pre[
    "study_governance_adopted"
] is not False:
    fail(
        "STUDY_ALREADY_ADOPTED"
    )

for key, value in a[
    "technical_nonclaims"
].items():

    if value is not False:
        fail(
            "UNEXPECTED_PERMISSION|"
            + key
        )

life = a[
    "authorization_verifier_lifecycle"
]

if life[
    "initial_state"
] != "ACTIVE_UNCONSUMED":
    fail(
        "A02_INITIAL_STATE"
    )

if life[
    "may_execute_exactly_once_immediately_before_governance_adoption_authoring"
] is not True:
    fail(
        "A02_LIFECYCLE"
    )

closure = json.loads(
    CLOSURE.read_text(
        encoding="utf-8"
    )
)

if closure[
    "assessment_outcome"
] != "PASS_CLOSED":
    fail(
        "SOURCE_CLOSURE_OUTCOME"
    )

if closure[
    "closure_result"
][
    "review_chain_closed"
] is not True:
    fail(
        "SOURCE_REVIEW_CHAIN_STATE"
    )

if closure[
    "study_state_after_closure"
][
    "bounded_technical_outcome"
] != "FURTHER_EVIDENCE_REQUIRED":
    fail(
        "SOURCE_BOUNDED_OUTCOME"
    )

if closure[
    "study_state_after_closure"
][
    "governance_adopted"
] is not False:
    fail(
        "SOURCE_PREMATURE_ADOPTION"
    )

print("CLOSED_SUCR_REVIEW_CHAIN_BINDING=PASS")
print("REVIEW_CHAIN_CLOSURE_OUTCOME=PASS_CLOSED")
print("REVIEW_CHAIN_CLOSED=YES")

print("STUDY_ARTIFACT_STATUS=AUTHOR_CANDIDATE")
print("BOUNDED_TECHNICAL_OUTCOME=FURTHER_EVIDENCE_REQUIRED")
print("STUDY_GOVERNANCE_ADOPTED=NO")

print("AUTHORIZED_GOVERNANCE_STATUS=APPROVED_WITH_BOUNDED_TECHNICAL_OUTCOME")
print("AUTHORIZED_ADOPTED_TECHNICAL_OUTCOME=FURTHER_EVIDENCE_REQUIRED")

print("GOVERNANCE_ADOPTION_AUTHORIZED=YES")
print("GOVERNANCE_ADOPTION_AUTHORED=NO")

print("OPERATIONAL_MAPPING_AUTHORIZED=NO")
print("SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO")
print("CURL_JSON_AUTHORIZED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")

print("RETIRED_A02_VERIFIERS_EXECUTED=NO")

print("GOVERNANCE_ADOPTION_AUTHORING_AUTHORIZATION=PASS")
print("VERIFIER_LIFECYCLE=ONE_FINAL_RUN_IMMEDIATELY_BEFORE_GOVERNANCE_ADOPTION_AUTHORING_THEN_PERMANENT_RETIREMENT")
