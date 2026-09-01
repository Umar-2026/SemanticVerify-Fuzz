#!/usr/bin/env python3

from pathlib import Path
import json
import subprocess

REPO = Path(
    "/openbayes/home/semanticverify-fuzz-research"
)

EXPECTED_PARENT = (
    "53d0ced3daa2aa1b3dc6464ac77a3793704905b8"
)

EXPECTED_PACKAGE_TREE = (
    "bb5427cc37ba328de88212d9cb1fab921cb8f026"
)

ROOT = (
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2/"
)

PACKAGE_DIR = (
    ROOT
    + "schema_v2_req06_req14_accounting_satisfaction_"
    + "evidence_gap_and_acquisition_specification_study_v2_"
    + "corrective_successor_for_aser01_aser02_aser04_aser07_"
    + "independent_human_rereview_package_v1"
)

AUTH_DIR = (
    PACKAGE_DIR
    + "_external_handoff_authorization_v1"
)

A01 = (
    AUTH_DIR
    + "/01_external_independent_human_rereview_handoff_authorization.v1.json"
)

A02 = (
    AUTH_DIR
    + "/02_authorize_external_independent_human_rereview_handoff_once.v1.py"
)

A03 = (
    AUTH_DIR
    + "/03_external_handoff_scope_contract.v1.json"
)

A04 = (
    AUTH_DIR
    + "/04_external_handoff_authorization_boundary.v1.md"
)

DEC = (
    "documentation/decisions/"
    "0216-authorize-external-independent-human-rereview-handoff-"
    "for-d0213-corrective-successor.md"
)

EXPECTED_CHANGED = sorted([
    A01,
    A02,
    A03,
    A04,
    DEC,
])

EXPECTED_ZIP = (
    "/openbayes/home/"
    "50_req06_req14_accounting_gap_corrective_successor_"
    "independent_human_rereview_handoff.v1.zip"
)

EXPECTED_FORM = (
    "/openbayes/home/"
    "50_req06_req14_accounting_gap_corrective_successor_"
    "independent_human_rereview_form.MANUAL_REVIEW_COPY.v1.md"
)


def stop(code, detail=""):
    print(
        "STOP|"
        + code
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
        "D0216_PARENT_INVALID",
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
    stop("D0216_COMMIT_SCOPE_INVALID")

package_tree = subprocess.check_output(
    [
        "git",
        "-C",
        str(REPO),
        "rev-parse",
        f"{EXPECTED_PARENT}:{PACKAGE_DIR}",
    ],
    text=True,
).strip()

if package_tree != EXPECTED_PACKAGE_TREE:
    stop(
        "D0215_PACKAGE_TREE_INVALID",
        package_tree,
    )

authorization = json.loads(
    (
        REPO
        / A01
    ).read_text(
        encoding="utf-8"
    )
)

contract = json.loads(
    (
        REPO
        / A03
    ).read_text(
        encoding="utf-8"
    )
)

if authorization.get("decision") != "0216":
    stop("AUTHORIZATION_DECISION_INVALID")

if authorization.get(
    "authorization_status"
) != (
    "AUTHORIZED_TO_CREATE_EXTERNAL_INDEPENDENT_HUMAN_REREVIEW_HANDOFF_ONLY"
):
    stop("AUTHORIZATION_STATUS_INVALID")

scope = authorization.get(
    "review_scope",
    {},
)

if scope.get(
    "fresh_human_rereview_items"
) != [
    "ASER01",
    "ASER02",
    "ASER04",
    "ASER07",
]:
    stop("REREVIEW_SCOPE_INVALID")

if scope.get(
    "preserved_pass_items"
) != [
    "ASER03",
    "ASER05",
    "ASER06",
    "ASER08",
    "ASER09",
]:
    stop("PRESERVED_PASS_SCOPE_INVALID")

if scope.get(
    "preserved_pass_items_reopened"
) is not False:
    stop("PRESERVED_PASS_REOPENING_INVALID")

outputs = authorization.get(
    "authorized_external_outputs",
    {},
)

if outputs.get(
    "handoff_zip",
    {},
).get("path") != EXPECTED_ZIP:
    stop("HANDOFF_ZIP_TARGET_INVALID")

if outputs.get(
    "manual_review_copy",
    {},
).get("path") != EXPECTED_FORM:
    stop("MANUAL_FORM_TARGET_INVALID")

for name in (
    "handoff_zip",
    "manual_review_copy",
):
    if outputs.get(
        name,
        {},
    ).get(
        "must_not_overwrite_existing_target"
    ) is not True:
        stop(
            "NO_OVERWRITE_RULE_INVALID",
            name,
        )

rules = authorization.get(
    "handoff_construction_rules",
    {},
)

for key in (
    "zip_source_must_be_exact_committed_decision0215_package",
    "working_tree_substitution_for_package_source_forbidden",
    "manual_copy_source_must_be_exact_committed_blank_form",
    "human_fields_must_remain_blank_during_handoff_creation",
    "human_decisions_must_not_be_synthesized",
    "reviewer_identity_must_not_be_synthesized",
    "reviewer_notes_must_not_be_synthesized",
    "reviewer_signature_or_confirmation_must_not_be_synthesized",
    "review_date_must_not_be_synthesized",
    "independence_attestation_completion_must_not_be_synthesized",
    "existing_external_targets_must_not_be_overwritten",
):
    if rules.get(key) is not True:
        stop(
            "HANDOFF_RULE_INVALID",
            key,
        )

for key, value in authorization.get(
    "explicit_nonauthorization",
    {},
).items():
    if value is not False:
        stop(
            "NONAUTHORIZATION_INVALID",
            key,
        )

requirements = contract.get(
    "required_handoff_properties",
    {},
)

for key in (
    "committed_source_bytes_only",
    "zip_integrity_binding_required",
    "manual_form_initial_exact_copy_required",
    "manual_form_blank_at_creation_required",
    "safe_rerunnable_handoff_verifier_required",
    "checksum_closure_required",
    "existing_external_targets_must_not_be_overwritten",
):
    if requirements.get(key) is not True:
        stop(
            "HANDOFF_CONTRACT_REQUIREMENT_INVALID",
            key,
        )

print(
    "DECISION0216_EXTERNAL_INDEPENDENT_HUMAN_REREVIEW_HANDOFF_AUTHORIZATION_VERIFIER=PASS"
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
    "SOURCE_D0215_PACKAGE_TREE="
    + package_tree
)

print(
    "EXTERNAL_HANDOFF_CREATION_AUTHORIZED=YES"
)

print(
    "EXTERNAL_HANDOFF_CREATED_BY_THIS_VERIFIER=NO"
)

print(
    "MANUAL_REVIEW_COPY_CREATION_AUTHORIZED=YES"
)

print(
    "HUMAN_REREVIEW_PERFORMED=NO"
)

print(
    "HUMAN_FIELDS_POPULATED=NO"
)

print(
    "HUMAN_FIELDS_SYNTHESIZED=NO"
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
