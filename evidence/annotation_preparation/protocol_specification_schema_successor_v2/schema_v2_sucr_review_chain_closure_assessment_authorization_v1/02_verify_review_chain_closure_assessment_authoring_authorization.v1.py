#!/usr/bin/env python3

import hashlib
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]

BASE_REL = (
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2"
)

AUTH = (
    HERE
    / "01_review_chain_closure_assessment_authorization.v1.json"
)

ORIGINAL = (
    REPO
    / BASE_REL
    / "schema_v2_semantic_unit_carrier_admissibility_and_requirement_binding_study_v1_completed_human_review_v1"
)

FOCUSED = (
    REPO
    / BASE_REL
    / "schema_v2_sucr01_focused_rereview_v1_completed_human_review_v1"
)

CORRECTIVE_REL = (
    BASE_REL
    + "/schema_v2_sucr01_corrective_portable_source_evidence_successor_package_v2"
)

ORIGINAL_REL = (
    BASE_REL
    + "/schema_v2_semantic_unit_carrier_admissibility_and_requirement_binding_study_v1_completed_human_review_v1"
)

FOCUSED_REL = (
    BASE_REL
    + "/schema_v2_sucr01_focused_rereview_v1_completed_human_review_v1"
)

FUTURE = (
    REPO
    / BASE_REL
    / "schema_v2_sucr_review_chain_closure_assessment_v1"
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
        "CLOSURE_ASSESSMENT_ALREADY_EXISTS"
    )

if git_object(
    ORIGINAL_REL
) != "e8178b937ab376faca698d35cc57d6e3785fbbb5":
    fail(
        "ORIGINAL_REVIEW_TREE"
    )

if git_object(
    FOCUSED_REL
) != "170c04d5dedf3a900edcf9d2a7ebc92b298b48a9":
    fail(
        "FOCUSED_REVIEW_TREE"
    )

if git_object(
    CORRECTIVE_REL
) != "dd34182886703f72fc5bfa4df899ad2bccbf4744":
    fail(
        "CORRECTIVE_PACKAGE_TREE"
    )

a = json.loads(
    AUTH.read_text(
        encoding="utf-8"
    )
)

if a[
    "status"
] != "AUTHORIZED_FOR_REVIEW_CHAIN_CLOSURE_ASSESSMENT_AUTHORING_ONLY":
    fail(
        "AUTHORIZATION_STATUS"
    )

historical = a[
    "historical_review_state"
]

if historical[
    "SUCR01"
] != "REVISION_REQUIRED":
    fail(
        "HISTORICAL_SUCR01"
    )

for rid in (
    "SUCR02",
    "SUCR03",
    "SUCR04",
    "SUCR05",
    "SUCR06",
    "SUCR07",
    "SUCR08",
):
    if historical[rid] != "PASS":
        fail(
            "HISTORICAL_PASS|"
            + rid
        )

if historical[
    "overall"
] != "REVISION_REQUIRED":
    fail(
        "HISTORICAL_OVERALL"
    )

focused = a[
    "corrective_review_state"
]

if focused[
    "criterion"
] != "SUCR01-C":
    fail(
        "FOCUSED_CRITERION"
    )

if focused[
    "scope"
] != "SOURCE_EVIDENCE_PORTABILITY_AND_RESOLVABILITY":
    fail(
        "FOCUSED_SCOPE"
    )

if focused[
    "item_decision"
] != "PASS":
    fail(
        "FOCUSED_ITEM_DECISION"
    )

if focused[
    "overall_decision"
] != "APPROVE_SUCR01_CORRECTIVE_PORTABLE_SOURCE_EVIDENCE_SUCCESSOR_PACKAGE_V2":
    fail(
        "FOCUSED_OVERALL_DECISION"
    )

contract = a[
    "closure_assessment_contract"
]

for key in (
    "must_preserve_original_review",
    "must_preserve_focused_review",
    "must_not_rewrite_historical_sucr01_revision_required",
    "must_not_rewrite_historical_overall_revision_required",
    "must_confirm_sucr02_through_sucr08_original_pass_findings",
    "must_confirm_focused_corrective_scope_matches_original_sucr01_deficiency",
    "must_confirm_focused_sucr01_c_pass",
    "must_confirm_focused_overall_corrective_approval",
    "must_confirm_no_other_original_review_item_requires_correction",
    "assessment_must_not_claim_study_governance_adoption",
    "assessment_must_not_change_bounded_technical_outcome",
    "assessment_must_not_create_operational_authority",
):
    if contract[key] is not True:
        fail(
            "CLOSURE_CONTRACT|"
            + key
        )

if contract[
    "allowed_assessment_outcomes"
] != [
    "PASS_CLOSED",
    "REMAINS_OPEN",
]:
    fail(
        "ASSESSMENT_OUTCOMES"
    )

pre = a[
    "pre_assessment_state"
]

if pre[
    "review_chain_closure_assessment_authorized"
] is not True:
    fail(
        "ASSESSMENT_AUTHORIZATION"
    )

if pre[
    "review_chain_closure_assessment_authored"
] is not False:
    fail(
        "PREMATURE_ASSESSMENT"
    )

if pre[
    "review_chain_closed"
] is not False:
    fail(
        "PREMATURE_CHAIN_CLOSURE"
    )

if pre[
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
    "may_execute_exactly_once_immediately_before_review_chain_closure_assessment_authoring"
] is not True:
    fail(
        "A02_LIFECYCLE"
    )

original_record = json.loads(
    (
        ORIGINAL
        / "02_completed_human_review_record.v1.json"
    ).read_text(
        encoding="utf-8"
    )
)

focused_record = json.loads(
    (
        FOCUSED
        / "02_completed_focused_rereview_record.v1.json"
    ).read_text(
        encoding="utf-8"
    )
)

if original_record[
    "review_interpretation"
][
    "sucr01_corrective_scope"
] != "SOURCE_EVIDENCE_PORTABILITY_AND_RESOLVABILITY":
    fail(
        "ORIGINAL_CORRECTIVE_SCOPE"
    )

if focused_record[
    "completed_focused_review"
][
    "scope"
] != "SOURCE_EVIDENCE_PORTABILITY_AND_RESOLVABILITY":
    fail(
        "FOCUSED_CORRECTIVE_SCOPE"
    )

if focused_record[
    "completed_focused_review"
][
    "item_decision"
] != "PASS":
    fail(
        "FOCUSED_PASS"
    )

print("ORIGINAL_COMPLETED_SUCR_REVIEW_BINDING=PASS")
print("FOCUSED_COMPLETED_SUCR01_C_REREVIEW_BINDING=PASS")
print("CORRECTIVE_SUCCESSOR_PACKAGE_V2_BINDING=PASS")

print("ORIGINAL_SUCR01_DECISION=REVISION_REQUIRED")
print("SUCR02_SUCR08_ORIGINAL_PASS_FINDINGS_PRESERVED=YES")
print("ORIGINAL_OVERALL_REVIEW_REMAINS=REVISION_REQUIRED")

print("FOCUSED_SUCR01_C_DECISION=PASS")
print("FOCUSED_CORRECTIVE_OVERALL_APPROVAL=PASS")
print("CORRECTIVE_SCOPE_MATCH=YES")

print("REVIEW_CHAIN_CLOSURE_ASSESSMENT_AUTHORIZED=YES")
print("REVIEW_CHAIN_CLOSURE_ASSESSMENT_AUTHORED=NO")
print("REVIEW_CHAIN_CLOSED=NO")

print("STUDY_GOVERNANCE_ADOPTED=NO")
print("GLOBAL_OUTCOME=FURTHER_EVIDENCE_REQUIRED")

print("OPERATIONAL_MAPPING_AUTHORIZED=NO")
print("SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO")
print("CURL_JSON_AUTHORIZED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")

print("RETIRED_A02_VERIFIERS_EXECUTED=NO")

print("REVIEW_CHAIN_CLOSURE_ASSESSMENT_AUTHORING_AUTHORIZATION=PASS")
print("VERIFIER_LIFECYCLE=ONE_FINAL_RUN_IMMEDIATELY_BEFORE_CLOSURE_ASSESSMENT_AUTHORING_THEN_PERMANENT_RETIREMENT")
