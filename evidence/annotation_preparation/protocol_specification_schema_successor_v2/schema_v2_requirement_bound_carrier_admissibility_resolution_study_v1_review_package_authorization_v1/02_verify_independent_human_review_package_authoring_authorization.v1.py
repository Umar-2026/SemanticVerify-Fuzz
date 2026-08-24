#!/usr/bin/env python3

import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]

BASE_REL = (
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2"
)

STUDY_REL = (
    BASE_REL
    + "/schema_v2_requirement_bound_carrier_admissibility_resolution_study_v1"
)

THIS_AUTH_REL = (
    BASE_REL
    + "/schema_v2_requirement_bound_carrier_admissibility_resolution_study_v1_review_package_authorization_v1"
)

STUDY = REPO / STUDY_REL

STUDY_SAFE = (
    STUDY
    / "08_verify_requirement_bound_carrier_admissibility_resolution_study.v1.py"
)

AUTH = (
    HERE
    / "01_independent_human_review_package_authorization.v1.json"
)

EXPECTED_DECISION0138 = (
    "27f3176e76d375297264b006a66f96e915fbf4b6"
)

EXPECTED_STUDY_TREE = (
    "ea4806ec69f51d2a81a2d1d3cc3663e8706dcaa3"
)

def fail(msg):
    print("FAIL|" + msg)
    raise SystemExit(1)

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

if current_head == EXPECTED_DECISION0138:
    fail(
        "REVIEW_PACKAGE_AUTHORIZATION_NOT_COMMITTED"
    )

if current_parent != EXPECTED_DECISION0138:
    fail(
        "CURRENT_HEAD_IS_NOT_IMMEDIATE_SUCCESSOR_OF_DECISION0138"
    )

if (
    git(
        "rev-parse",
        "HEAD:" + STUDY_REL,
    )
    != EXPECTED_STUDY_TREE
):
    fail(
        "STUDY_V1_GIT_TREE"
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
    != "PRE_INDEPENDENT_HUMAN_REVIEW_PACKAGE_AUTHORING_ONLY"
):
    fail(
        "AUTHORIZATION_TYPE"
    )

if (
    auth["status"]
    != "AUTHORIZED_NOT_YET_PACKAGED"
):
    fail(
        "AUTHORIZATION_STATUS"
    )

subject = auth[
    "review_subject"
]

if subject["status"] != "AUTHOR_CANDIDATE":
    fail(
        "SUBJECT_STATUS"
    )

if (
    subject["author_candidate_outcome"]
    != "FURTHER_EVIDENCE_REQUIRED"
):
    fail(
        "SUBJECT_OUTCOME"
    )

if subject["requirement_count"] != 17:
    fail(
        "REQUIREMENT_COUNT"
    )

if subject["semantic_unit_count"] != 109:
    fail(
        "SEMANTIC_UNIT_COUNT"
    )

if subject["schema_v2_property_path_count"] != 171:
    fail(
        "SCHEMA_PATH_COUNT"
    )

if subject["historical_pair_count"] != 18639:
    fail(
        "PAIR_COUNT"
    )

if subject["admissible_exact_count"] != 0:
    fail(
        "ADMISSIBLE_EXACT_COUNT"
    )

if subject["admissible_composite_count"] != 0:
    fail(
        "ADMISSIBLE_COMPOSITE_COUNT"
    )

if subject["no_admissible_carrier_proven_count"] != 0:
    fail(
        "NO_ADMISSIBLE_CARRIER_PROVEN_COUNT"
    )

if subject["unresolved_count"] != 17:
    fail(
        "UNRESOLVED_COUNT"
    )

if (
    subject[
        "requirement_to_semantic_unit_crosswalk_identified"
    ]
    is not False
):
    fail(
        "CROSSWALK_STATE"
    )

if subject["historical_pair_state_modified"] is not False:
    fail(
        "PAIR_STATE"
    )

if (
    sorted(auth["review_criteria"].keys())
    != [
        "RBCA01",
        "RBCA02",
        "RBCA03",
        "RBCA04",
        "RBCA05",
        "RBCA06",
        "RBCA07",
        "RBCA08",
    ]
):
    fail(
        "REVIEW_CRITERIA"
    )

if auth["required_reviewer_role"] != "Spec-Technical-Reviewer-1":
    fail(
        "REVIEWER_ROLE"
    )

if auth["reviewer_decision_synthesis_authorized"] is not False:
    fail(
        "REVIEW_DECISION_SYNTHESIS"
    )

if auth["human_reviewer_identity_synthesis_authorized"] is not False:
    fail(
        "REVIEWER_IDENTITY_SYNTHESIS"
    )

if auth["review_notes_synthesis_authorized"] is not False:
    fail(
        "REVIEW_NOTES_SYNTHESIS"
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
    ["python3", str(STUDY_SAFE)],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    check=False,
)

if p.returncode != 0:
    fail(
        "STUDY_SAFE_VERIFIER|"
        + p.stdout
        + p.stderr
    )

required_markers = [
    "REQUIREMENT_BOUND_CARRIER_ADMISSIBILITY_RESOLUTION_STUDY_V1=PASS",
    "STUDY_STATUS=AUTHOR_CANDIDATE",
    "UNRESOLVED_COUNT=17",
    "STUDY_OUTCOME=FURTHER_EVIDENCE_REQUIRED",
    "HISTORICAL_PAIR_STATE_MODIFIED=NO",
    "CARRIER_ADMISSIBILITY_RESOLVED=NO",
    "POSITIVE_MAPPING_PROVEN=NO",
    "NEGATIVE_MAPPING_IMPOSSIBILITY_PROVEN=NO",
    "WHOLE_V4_EXHAUSTIVENESS_PROVEN=NO",
    "DECISION_0137_A02_STATE=PERMANENTLY_RETIRED",
    "DECISION_0137_A02_EXECUTED_BY_SAFE_VERIFIER=NO",
    "INDEPENDENT_HUMAN_REVIEW_REQUIRED=YES",
]

for marker in required_markers:
    if marker not in p.stdout:
        fail(
            "STUDY_SAFE_MARKER|"
            + marker
        )

print(
    "INDEPENDENT_HUMAN_REVIEW_PACKAGE_AUTHORING_AUTHORIZATION=PASS"
)

print(
    "CURRENT_CHECKPOINT_ROLE="
    "IMMEDIATE_SUCCESSOR_OF_DECISION0138"
)

print(
    "CURRENT_HEAD_PARENT_DECISION0138_BINDING=PASS"
)

print(
    "REVIEW_SUBJECT_STATUS="
    "AUTHOR_CANDIDATE"
)

print(
    "REVIEW_SUBJECT_OUTCOME="
    "FURTHER_EVIDENCE_REQUIRED"
)

print(
    "REVIEW_ITEMS="
    "RBCA01|RBCA02|RBCA03|RBCA04|RBCA05|RBCA06|RBCA07|RBCA08"
)

print(
    "REQUIRED_REVIEWER_ROLE="
    "Spec-Technical-Reviewer-1"
)

print(
    "REVIEWER_DECISION_SYNTHESIS_AUTHORIZED=NO"
)

print(
    "REVIEWER_IDENTITY_SYNTHESIS_AUTHORIZED=NO"
)

print(
    "STUDY_GOVERNANCE_ADOPTION_AUTHORIZED=NO"
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
    "ONE_FINAL_RUN_IMMEDIATELY_BEFORE_INDEPENDENT_HUMAN_REVIEW_PACKAGE_AUTHORING_THEN_PERMANENT_RETIREMENT"
)
