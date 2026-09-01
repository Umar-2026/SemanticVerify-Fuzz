#!/usr/bin/env python3

from pathlib import Path
import json
import subprocess

REPO = Path(
    "/openbayes/home/semanticverify-fuzz-research"
)

EXPECTED_PARENT = (
    "18d744c0825ce436f28e17f1256cac525523e5c4"
)

ROOT = (
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2/"
)

AUTH = (
    ROOT
    + "schema_v2_req06_req14_accounting_satisfaction_"
    + "evidence_gap_and_acquisition_specification_study_v2_"
    + "corrective_successor_for_aser01_aser02_aser04_aser07_"
    + "independent_human_rereview_package_authorization_v1/"
)

A01 = (
    AUTH
    + "01_independent_human_rereview_package_authorization.v1.json"
)

A02 = (
    AUTH
    + "02_authorize_independent_human_rereview_package_once.v1.py"
)

A03 = (
    AUTH
    + "03_independent_human_rereview_scope_contract.v1.json"
)

A04 = (
    AUTH
    + "04_independent_human_rereview_package_authorization_boundary.v1.md"
)

DEC = (
    "documentation/decisions/"
    "0214-authorize-independent-human-rereview-package-for-"
    "d0213-corrective-successor.md"
)

EXPECTED_CHANGED = sorted([
    A01,
    A02,
    A03,
    A04,
    DEC,
])


def stop(code, detail=""):
    print(
        "STOP|" + code
        + (("|" + detail) if detail else "")
    )
    raise SystemExit(1)


head = subprocess.check_output(
    [
        "git",
        "-C",
        str(REPO),
        "rev-parse",
        "HEAD",
    ],
    text=True,
).strip()

parent = subprocess.check_output(
    [
        "git",
        "-C",
        str(REPO),
        "rev-parse",
        "HEAD^",
    ],
    text=True,
).strip()

if parent != EXPECTED_PARENT:
    stop(
        "D0214_PARENT_INVALID",
        parent,
    )

status = subprocess.check_output(
    [
        "git",
        "-C",
        str(REPO),
        "status",
        "--porcelain=v1",
        "--untracked-files=all",
    ],
    text=True,
)

if status.strip():
    stop("REPOSITORY_NOT_CLEAN")

changed = subprocess.check_output(
    [
        "git",
        "-C",
        str(REPO),
        "diff-tree",
        "--no-commit-id",
        "--name-only",
        "-r",
        "HEAD",
    ],
    text=True,
).splitlines()

if sorted(changed) != EXPECTED_CHANGED:
    stop("D0214_COMMIT_SCOPE_INVALID")

authorization = json.loads(
    (REPO / A01).read_text(
        encoding="utf-8"
    )
)

contract = json.loads(
    (REPO / A03).read_text(
        encoding="utf-8"
    )
)

if authorization.get("decision") != "0214":
    stop("AUTHORIZATION_DECISION_INVALID")

if authorization.get(
    "authorization_status"
) != (
    "AUTHORIZED_TO_AUTHOR_BLANK_INDEPENDENT_HUMAN_REREVIEW_PACKAGE_ONLY"
):
    stop("AUTHORIZATION_STATUS_INVALID")

scope = authorization.get(
    "rereview_scope",
    {},
)

if scope.get(
    "corrective_items_requiring_new_human_judgment"
) != [
    "ASER01",
    "ASER02",
    "ASER04",
    "ASER07",
]:
    stop("REREVIEW_SCOPE_INVALID")

if scope.get(
    "preserved_predecessor_pass_items"
) != [
    "ASER03",
    "ASER05",
    "ASER06",
    "ASER08",
    "ASER09",
]:
    stop("PRESERVED_PASS_SCOPE_INVALID")

if scope.get(
    "preserved_pass_items_are_not_reopened"
) is not True:
    stop("PASS_NONREOPENING_RULE_INVALID")

non = authorization.get(
    "explicit_nonauthorization",
    {},
)

for key, value in non.items():
    if value is not False:
        stop(
            "NONAUTHORIZATION_INVALID",
            key,
        )

human_fields = authorization.get(
    "human_fields_must_remain_blank_until_external_review",
    [],
)

required_human_fields = {
    "reviewer_name",
    "reviewer_role",
    "reviewer_confirmation_or_signature",
    "review_date",
    "independence_attestation",
    "ASER01_decision",
    "ASER01_notes",
    "ASER02_decision",
    "ASER02_notes",
    "ASER04_decision",
    "ASER04_notes",
    "ASER07_decision",
    "ASER07_notes",
    "overall_rereview_decision",
    "overall_rereview_notes",
}

if set(human_fields) != required_human_fields:
    stop("BLANK_HUMAN_FIELD_SET_INVALID")

if contract.get(
    "required_rereview_items"
) != [
    "ASER01",
    "ASER02",
    "ASER04",
    "ASER07",
]:
    stop("CONTRACT_REREVIEW_ITEMS_INVALID")

if contract.get(
    "preserved_pass_items"
) != [
    "ASER03",
    "ASER05",
    "ASER06",
    "ASER08",
    "ASER09",
]:
    stop("CONTRACT_PASS_ITEMS_INVALID")

package = contract.get(
    "package_requirements",
    {},
)

for key in (
    "blank_before_external_handoff",
    "exact_source_binding",
    "checksum_closure",
    "safe_rerunnable_package_verification",
    "independent_human_completion_required",
    "no_synthetic_human_fields",
):
    if package.get(key) is not True:
        stop(
            "PACKAGE_REQUIREMENT_INVALID",
            key,
        )

print(
    "DECISION0214_INDEPENDENT_HUMAN_REREVIEW_PACKAGE_AUTHORIZATION_VERIFIER=PASS"
)

print(
    "AUTHORIZATION_COMMIT="
    + head
)

print(
    "AUTHORIZATION_PARENT="
    + parent
)

print(
    "REREVIEW_ITEMS=ASER01,ASER02,ASER04,ASER07"
)

print(
    "PRESERVED_PASS_ITEMS=ASER03,ASER05,ASER06,ASER08,ASER09"
)

print(
    "BLANK_INDEPENDENT_HUMAN_REREVIEW_PACKAGE_AUTHORING_AUTHORIZED=YES"
)

print(
    "BLANK_INDEPENDENT_HUMAN_REREVIEW_PACKAGE_AUTHORED_BY_THIS_VERIFIER=NO"
)

print(
    "HUMAN_REREVIEW_PERFORMED=NO"
)

print(
    "HUMAN_FIELDS_SYNTHESIZED=NO"
)

print(
    "EXTERNAL_REREVIEW_HANDOFF_AUTHORIZED=NO"
)

print(
    "RETURNED_REREVIEW_RECORDING_AUTHORIZED=NO"
)

print(
    "CORRECTIVE_SUCCESSOR_GOVERNANCE_ADOPTION_AUTHORIZED=NO"
)

print(
    "ACCOUNTING_EVIDENCE_ACQUISITION_AUTHORIZED=NO"
)

print(
    "CONCRETE_MAPPING_AUTHORIZED=NO"
)

print(
    "ACCOUNTING_SATISFACTION_DETERMINATION_AUTHORIZED=NO"
)

print(
    "PAIR_RECLASSIFICATION_AUTHORIZED=NO"
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
    "AUTHORIZATION_EXECUTION_ATTEMPT_COUNT_FOR_THIS_RUN=1"
)

print(
    "AUTHORIZATION_RERUN_AFTER_FIRST_ATTEMPT_AUTHORIZED=NO"
)
