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

PACKAGE_REL = (
    BASE_REL
    + "/schema_v2_requirement_bound_carrier_admissibility_resolution_study_v1_review_package_v1"
)

THIS_AUTH_REL = (
    BASE_REL
    + "/schema_v2_requirement_bound_carrier_admissibility_resolution_study_v1_external_handoff_authorization_v1"
)

PACKAGE = REPO / PACKAGE_REL

PACKAGE_SAFE = (
    PACKAGE
    / "10_verify_requirement_bound_carrier_study_review_package.v1.py"
)

PACKET = (
    PACKAGE
    / "03_RBCA01_RBCA08_reviewer_packet.BLANK.v1.md"
)

BUNDLE = (
    PACKAGE
    / "08_sealed_repository_checkpoint.bundle"
)

AUTH = (
    HERE
    / "01_external_independent_human_review_handoff_authorization.v1.json"
)

EXPECTED_DECISION0140 = (
    "cbce1a415bdca9ff8b32d47b5268a37504de35cc"
)

EXPECTED_PACKAGE_TREE = (
    "94a907e55c8473f434d8675a7b5e46c63aad7533"
)

EXPECTED_BLANK_SHA = (
    "4b0df835c5bfd59f2d023204f5a1a2ede11a293d7168f862413777ccd846210b"
)

EXPECTED_BLANK_SIZE = 4134

EXPECTED_BUNDLE_SHA = (
    "a5f9f0ced2ea7e057da8faaede9d58ce5428d420967c9b6715044f873ab27741"
)

EXPECTED_BUNDLE_CHECKPOINT = (
    "c9cf1bf0c9a3b59714e08f966f9c98acbd309fd7"
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

def sha(path):
    import hashlib

    if not path.is_file():
        fail(
            "MISSING|"
            + str(path)
        )

    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()

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

if current_head == EXPECTED_DECISION0140:
    fail(
        "EXTERNAL_HANDOFF_AUTHORIZATION_NOT_COMMITTED"
    )

if current_parent != EXPECTED_DECISION0140:
    fail(
        "CURRENT_HEAD_IS_NOT_IMMEDIATE_SUCCESSOR_OF_DECISION0140"
    )

if (
    git(
        "rev-parse",
        "HEAD:" + PACKAGE_REL,
    )
    != EXPECTED_PACKAGE_TREE
):
    fail(
        "REVIEW_PACKAGE_GIT_TREE"
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
    != "PRE_EXTERNAL_INDEPENDENT_HUMAN_REVIEW_HANDOFF_AUTHORING_ONLY"
):
    fail(
        "AUTHORIZATION_TYPE"
    )

if (
    auth["status"]
    != "AUTHORIZED_NOT_YET_HANDED_OFF"
):
    fail(
        "AUTHORIZATION_STATUS"
    )

subject = auth[
    "handoff_subject"
]

if subject["review_items"] != [
    "RBCA01",
    "RBCA02",
    "RBCA03",
    "RBCA04",
    "RBCA05",
    "RBCA06",
    "RBCA07",
    "RBCA08",
]:
    fail(
        "REVIEW_ITEMS"
    )

if subject["required_reviewer_role"] != "Spec-Technical-Reviewer-1":
    fail(
        "REVIEWER_ROLE"
    )

if subject["study_outcome_under_review"] != "FURTHER_EVIDENCE_REQUIRED":
    fail(
        "STUDY_OUTCOME"
    )

if subject["unresolved_count"] != 17:
    fail(
        "UNRESOLVED_COUNT"
    )

if subject["human_review_performed"] is not False:
    fail(
        "HUMAN_REVIEW_ALREADY_PERFORMED"
    )

if subject["reviewer_decision_present"] is not False:
    fail(
        "REVIEWER_DECISION_ALREADY_PRESENT"
    )

if subject["reviewer_decision_synthesized"] is not False:
    fail(
        "REVIEWER_DECISION_SYNTHESIZED"
    )

if sha(PACKET) != EXPECTED_BLANK_SHA:
    fail(
        "BLANK_PACKET_SHA"
    )

if PACKET.stat().st_size != EXPECTED_BLANK_SIZE:
    fail(
        "BLANK_PACKET_SIZE"
    )

text = PACKET.read_text(
    encoding="utf-8"
)

if text.count(
    "Decision: `[PASS / REVISION_REQUIRED / FAIL]`"
) != 8:
    fail(
        "BLANK_PACKET_DECISION_COUNT"
    )

for forbidden in (
    "Decision: `PASS`",
    "Decision: `REVISION_REQUIRED`",
    "Decision: `FAIL`",
    "Overall decision: `APPROVE_REQUIREMENT_BOUND_CARRIER_ADMISSIBILITY_RESOLUTION_STUDY_V1`",
):
    if forbidden in text:
        fail(
            "PREFILLED_DECISION"
        )

if sha(BUNDLE) != EXPECTED_BUNDLE_SHA:
    fail(
        "SEALED_BUNDLE_SHA"
    )

p = subprocess.run(
    [
        "git",
        "bundle",
        "list-heads",
        str(BUNDLE),
    ],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    check=False,
)

if p.returncode != 0:
    fail(
        "SEALED_BUNDLE_LIST_HEADS"
    )

if EXPECTED_BUNDLE_CHECKPOINT not in p.stdout:
    fail(
        "SEALED_BUNDLE_CHECKPOINT"
    )

bundle_policy = auth[
    "sealed_bundle_semantics"
]

if (
    bundle_policy["checkpoint_commit"]
    != EXPECTED_BUNDLE_CHECKPOINT
):
    fail(
        "BUNDLE_POLICY_CHECKPOINT"
    )

if (
    bundle_policy["checkpoint_role"]
    != "DECISION_0139_PRE_REVIEW_PACKAGE_CHECKPOINT"
):
    fail(
        "BUNDLE_POLICY_ROLE"
    )

if bundle_policy["bundle_is_decision_0140_checkpoint"] is not False:
    fail(
        "BUNDLE_POLICY_FALSE_CLAIM"
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
        str(PACKAGE_SAFE),
    ],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    check=False,
)

if p.returncode != 0:
    fail(
        "PACKAGE_SAFE_VERIFIER|"
        + p.stdout
        + p.stderr
    )

for marker in (
    "REQUIREMENT_BOUND_CARRIER_STUDY_REVIEW_PACKAGE_V1=PASS",
    "REVIEWER_PACKET_INITIAL_BLANK_STATE=PASS",
    "REVIEWER_DECISION_PRESENT=NO",
    "REVIEWER_DECISION_SYNTHESIZED=NO",
    "HUMAN_REVIEW_PERFORMED=NO",
    "PORTABLE_SOURCE_COUNT=9",
    "PORTABLE_SOURCE_RESOLVABILITY=PASS",
    "STUDY_OUTCOME_UNDER_REVIEW=FURTHER_EVIDENCE_REQUIRED",
    "UNRESOLVED_COUNT=17",
    "STUDY_GOVERNANCE_ADOPTED=NO",
    "RETIRED_A02_VERIFIERS_EXECUTED=NO",
):
    if marker not in p.stdout:
        fail(
            "PACKAGE_SAFE_MARKER|"
            + marker
        )

print(
    "EXTERNAL_INDEPENDENT_HUMAN_REVIEW_HANDOFF_AUTHORING_AUTHORIZATION=PASS"
)

print(
    "CURRENT_CHECKPOINT_ROLE="
    "IMMEDIATE_SUCCESSOR_OF_DECISION0140"
)

print(
    "CURRENT_HEAD_PARENT_DECISION0140_BINDING=PASS"
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
    "REVIEWER_PACKET_INITIAL_BLANK_STATE=PASS"
)

print(
    "HUMAN_REVIEW_PERFORMED=NO"
)

print(
    "REVIEWER_DECISION_PRESENT=NO"
)

print(
    "REVIEWER_DECISION_SYNTHESIZED=NO"
)

print(
    "EXTERNAL_ZIP_AUTHORIZED=YES"
)

print(
    "EDITABLE_EXTERNAL_REVIEWER_PACKET_AUTHORIZED=YES"
)

print(
    "STUDY_OUTCOME_UNDER_REVIEW="
    "FURTHER_EVIDENCE_REQUIRED"
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
    "ONE_FINAL_RUN_IMMEDIATELY_BEFORE_EXTERNAL_RBCA01_RBCA08_HANDOFF_AUTHORING_THEN_PERMANENT_RETIREMENT"
)
