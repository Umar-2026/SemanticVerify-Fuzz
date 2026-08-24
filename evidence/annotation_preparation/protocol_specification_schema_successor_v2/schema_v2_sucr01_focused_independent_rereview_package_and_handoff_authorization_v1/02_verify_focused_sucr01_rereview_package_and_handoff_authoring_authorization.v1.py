#!/usr/bin/env python3

import hashlib
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]

BASE_REL = Path(
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2"
)

AUTH = (
    HERE
    / "01_focused_sucr01_rereview_package_and_handoff_authorization.v1.json"
)

CORRECTIVE = (
    REPO
    / BASE_REL
    / "schema_v2_sucr01_corrective_portable_source_evidence_successor_package_v2"
)

CORRECTIVE_MANIFEST = (
    CORRECTIVE
    / "07_corrective_successor_package_v2_manifest.json"
)

CORRECTIVE_SAFE = (
    CORRECTIVE
    / "09_verify_sucr01_corrective_portable_source_evidence_successor_package_v2.py"
)

CORRECTIVE_SUMS = (
    CORRECTIVE
    / "10_sucr01_corrective_portable_source_evidence_successor_package_v2.SHA256SUMS"
)

FUTURE = (
    REPO
    / BASE_REL
    / "schema_v2_sucr01_focused_independent_rereview_package_and_external_handoff_v1"
)

EXPECTED_HEAD = (
    "DECISION0119_COMMIT_PLACEHOLDER"
)

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

def git_status():
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

    return p.stdout.strip()

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
            "GIT_OBJECT|"
            + rel
        )

    return p.stdout.strip()

if git_status():
    fail(
        "REPOSITORY_NOT_CLEAN"
    )

if FUTURE.exists():
    fail(
        "FOCUSED_REREVIEW_PACKAGE_ALREADY_EXISTS"
    )

if git_object(
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2/"
    "schema_v2_sucr01_corrective_portable_source_evidence_successor_package_v2"
) != "dd34182886703f72fc5bfa4df899ad2bccbf4744":
    fail(
        "CORRECTIVE_PACKAGE_GIT_TREE"
    )

if sha(
    CORRECTIVE_SAFE
) != "ec8ff4ae3c5fd4ec24b2317fe0c5956437e023241c5d3b689fbd7e7437a912fa":
    fail(
        "CORRECTIVE_SAFE_VERIFIER_SHA"
    )

if sha(
    CORRECTIVE_SUMS
) != "9ee621a5bc5972fde01ea5641a903fa21c4514263ea1e33ec5a90353175f9cc5":
    fail(
        "CORRECTIVE_CHECKSUM_SHA"
    )

a = json.loads(
    AUTH.read_text(
        encoding="utf-8"
    )
)

if a[
    "status"
] != "AUTHORIZED_FOR_FOCUSED_SUCR01_REREVIEW_PACKAGE_AND_EXTERNAL_HANDOFF_AUTHORING_ONLY":
    fail(
        "AUTHORIZATION_STATUS"
    )

contract = a[
    "focused_rereview_contract"
]

if contract[
    "criterion_id"
] != "SUCR01-C":
    fail(
        "FOCUSED_CRITERION"
    )

if contract[
    "criterion_scope"
] != "SOURCE_EVIDENCE_PORTABILITY_AND_RESOLVABILITY":
    fail(
        "FOCUSED_SCOPE"
    )

if contract[
    "required_reviewer_role"
] != "Spec-Technical-Reviewer-1":
    fail(
        "REVIEWER_ROLE"
    )

if contract[
    "allowed_item_decisions"
] != [
    "PASS",
    "REVISION_REQUIRED",
    "FAIL",
]:
    fail(
        "ITEM_DECISIONS"
    )

if contract[
    "allowed_overall_decisions"
] != [
    "APPROVE_SUCR01_CORRECTIVE_PORTABLE_SOURCE_EVIDENCE_SUCCESSOR_PACKAGE_V2",
    "REVISION_REQUIRED",
    "FAIL",
]:
    fail(
        "OVERALL_DECISIONS"
    )

for key in (
    "sucr02_through_sucr08_are_not_reopened",
    "sucr02_through_sucr08_original_pass_findings_are_carried_forward",
    "reviewer_must_review_corrective_evidence_independently",
    "reviewer_must_not_modify_evidence_package",
    "no_author_synthesized_decision",
    "focused_pass_does_not_itself_close_review_chain",
    "focused_pass_requires_later_separate_review_chain_closure_assessment",
):
    if contract[key] is not True:
        fail(
            "REVIEW_CONTRACT|"
            + key
        )

req = a[
    "focused_package_and_handoff_requirements"
]

for key, value in req.items():
    if value is not True:
        fail(
            "HANDOFF_REQUIREMENT|"
            + key
        )

state = a[
    "review_chain_state"
]

if state[
    "original_overall_review"
] != "REVISION_REQUIRED":
    fail(
        "ORIGINAL_OVERALL_REVIEW"
    )

if state[
    "focused_sucr01_rereview_completed"
] is not False:
    fail(
        "PREMATURE_FOCUSED_REVIEW"
    )

if state[
    "review_chain_closed"
] is not False:
    fail(
        "PREMATURE_CHAIN_CLOSURE"
    )

if state[
    "study_governance_adopted"
] is not False:
    fail(
        "PREMATURE_GOVERNANCE_ADOPTION"
    )

for key, value in a[
    "technical_nonclaims"
].items():
    if value is not False:
        fail(
            "UNEXPECTED_TECHNICAL_PERMISSION|"
            + key
        )

for key, value in a[
    "retired_verifier_state"
].items():
    if key == \
            "retired_verifiers_must_not_be_executed":

        if value is not True:
            fail(
                "RETIRED_VERIFIER_POLICY"
            )

    elif value != \
            "PERMANENTLY_RETIRED":

        fail(
            "RETIRED_VERIFIER_STATE|"
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
    "may_execute_exactly_once_immediately_before_focused_rereview_package_and_external_handoff_authoring"
] is not True:
    fail(
        "A02_LIFECYCLE"
    )

pkg = json.loads(
    CORRECTIVE_MANIFEST.read_text(
        encoding="utf-8"
    )
)

if pkg[
    "package_status"
] != "AUTHOR_CANDIDATE_AWAITING_FOCUSED_SUCR01_REREVIEW":
    fail(
        "CORRECTIVE_PACKAGE_STATUS"
    )

if pkg[
    "source_review_state"
][
    "SUCR01"
] != "REVISION_REQUIRED":
    fail(
        "ORIGINAL_SUCR01_STATE"
    )

if pkg[
    "source_review_state"
][
    "original_overall_review"
] != "REVISION_REQUIRED":
    fail(
        "ORIGINAL_OVERALL_STATE"
    )

for key, value in pkg[
    "review_state"
].items():
    if value is not False:
        fail(
            "PREMATURE_CORRECTIVE_REVIEW_STATE|"
            + key
        )

print("DECISION_0118_CORRECTIVE_PACKAGE_BINDING=PASS")

print("FOCUSED_CRITERION=SUCR01-C")
print("FOCUSED_SCOPE=SOURCE_EVIDENCE_PORTABILITY_AND_RESOLVABILITY")
print("REQUIRED_REVIEWER_ROLE=Spec-Technical-Reviewer-1")

print("ORIGINAL_SUCR01_DECISION=REVISION_REQUIRED")
print("SUCR02_SUCR08_ORIGINAL_PASS_FINDINGS_PRESERVED=YES")
print("ORIGINAL_OVERALL_REVIEW_REMAINS=REVISION_REQUIRED")

print("FOCUSED_SUCR01_REREVIEW_COMPLETED=NO")
print("REVIEW_CHAIN_CLOSED=NO")
print("STUDY_GOVERNANCE_ADOPTED=NO")

print("DECISION_0102_A02_STATE=PERMANENTLY_RETIRED")
print("DECISION_0104_A02_STATE=PERMANENTLY_RETIRED")
print("DECISION_0106_A02_STATE=PERMANENTLY_RETIRED")
print("DECISION_0110_A02_STATE=PERMANENTLY_RETIRED")
print("DECISION_0112_A02_STATE=PERMANENTLY_RETIRED")
print("DECISION_0114_A02_STATE=PERMANENTLY_RETIRED")
print("DECISION_0117_A02_STATE=PERMANENTLY_RETIRED")
print("RETIRED_A02_VERIFIERS_EXECUTED=NO")

print("OPERATIONAL_MAPPING_AUTHORIZED=NO")
print("SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO")
print("CURL_JSON_AUTHORIZED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")

print("FOCUSED_SUCR01_REREVIEW_PACKAGE_AND_HANDOFF_AUTHORING_AUTHORIZATION=PASS")
print("VERIFIER_LIFECYCLE=ONE_FINAL_RUN_IMMEDIATELY_BEFORE_FOCUSED_REREVIEW_PACKAGE_AND_HANDOFF_AUTHORING_THEN_PERMANENT_RETIREMENT")
