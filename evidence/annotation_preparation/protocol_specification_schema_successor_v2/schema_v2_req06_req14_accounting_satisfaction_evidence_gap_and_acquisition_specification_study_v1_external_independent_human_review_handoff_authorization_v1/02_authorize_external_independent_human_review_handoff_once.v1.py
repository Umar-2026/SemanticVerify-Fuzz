#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import subprocess

D0205_COMMIT = (
    "1db96673ba363b81e34c29d646d1d38fa22c0254"
)

ROOT = Path(
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2"
)

PACKAGE_DIR = ROOT / (
    "schema_v2_req06_req14_accounting_satisfaction_"
    "evidence_gap_and_acquisition_specification_study_v1_"
    "independent_human_review_package_v1"
)

P01 = PACKAGE_DIR / "01_independent_human_review_package_manifest.v1.json"
P09 = PACKAGE_DIR / "09_blank_independent_human_review_form.v1.md"
P13 = PACKAGE_DIR / "13_verify_independent_human_review_package.v1.py"
P14 = PACKAGE_DIR / "14_independent_human_review_package.v1.SHA256SUMS"

AUTH_DIR = ROOT / (
    "schema_v2_req06_req14_accounting_satisfaction_"
    "evidence_gap_and_acquisition_specification_study_v1_"
    "external_independent_human_review_handoff_authorization_v1"
)

A01 = AUTH_DIR / "01_external_independent_human_review_handoff_authorization.v1.json"
A02 = AUTH_DIR / "02_authorize_external_independent_human_review_handoff_once.v1.py"
A03 = AUTH_DIR / "03_external_independent_human_review_handoff_contract.v1.json"
A04 = AUTH_DIR / "04_external_independent_human_review_handoff_authorization_boundary.v1.md"

DEC = Path(
    "documentation/decisions/"
    "0206-authorize-external-independent-human-review-handoff-for-req06-req14-"
    "accounting-satisfaction-evidence-gap-and-acquisition-specification-study-v1.md"
)

FUTURE_HANDOFF_DIR = ROOT / (
    "schema_v2_req06_req14_accounting_satisfaction_"
    "evidence_gap_and_acquisition_specification_study_v1_"
    "external_independent_human_review_handoff_v1"
)

EXT_ZIP = Path(
    "/openbayes/home/"
    "50_req06_req14_accounting_gap_study_independent_human_review_handoff.v1.zip"
)

EXT_EDITABLE = Path(
    "/openbayes/home/"
    "50_req06_req14_accounting_gap_study_independent_human_review_form."
    "MANUAL_REVIEW_COPY.v1.md"
)

EXPECTED_D0206_PATHS = {
    str(A01),
    str(A02),
    str(A03),
    str(A04),
    str(DEC),
}

EXPECTED_PACKAGE_SHA = {
    P01:
        "9964f0ba5ce9a78a4b21f77d29f59ba42a2e03c1c589e0aa4fc4ba4e70696e86",
    P09:
        "718483ff141ee7787cf2d3d9d2e64f75a33e8ef2643e78df35de73f5e6da402a",
    P13:
        "ebf93b9089332f52372ba0e3fd32d91cb18253976b9232ff786e20948e444dc6",
    P14:
        "a5599dee0a634e262dc9a28ae666afb9d346c9be8d5c24cf73d26a318c18e658",
}


def stop(code, detail=""):
    print(
        "STOP|" + code
        + (("|" + detail) if detail else "")
    )
    raise SystemExit(1)


def git(*args):
    return subprocess.check_output(
        ["git", *args],
        text=True
    ).strip()


if git("rev-parse", "HEAD^") != D0205_COMMIT:
    stop("D0206_PARENT_NOT_D0205")

if subprocess.check_output(
    [
        "git",
        "status",
        "--porcelain=v1",
        "--untracked-files=all",
    ],
    text=True
).strip():
    stop("REPOSITORY_NOT_CLEAN_BEFORE_EXTERNAL_HANDOFF")

changed = {
    p
    for p in subprocess.check_output(
        [
            "git",
            "diff-tree",
            "--no-commit-id",
            "--name-only",
            "-r",
            "HEAD",
        ],
        text=True
    ).splitlines()
    if p.strip()
}

if changed != EXPECTED_D0206_PATHS:
    stop(
        "D0206_COMMIT_SCOPE_MISMATCH",
        ",".join(sorted(changed))
    )

if FUTURE_HANDOFF_DIR.exists():
    stop("HANDOFF_RECORD_ALREADY_EXISTS")

if EXT_ZIP.exists():
    stop("EXTERNAL_ZIP_ALREADY_EXISTS")

if EXT_EDITABLE.exists():
    stop("EXTERNAL_EDITABLE_ALREADY_EXISTS")

for path in (
    P01, P09, P13, P14,
    A01, A02, A03, A04, DEC
):
    if not path.is_file():
        stop("REQUIRED_ARTIFACT_MISSING", str(path))

for path, expected in EXPECTED_PACKAGE_SHA.items():
    actual = hashlib.sha256(
        path.read_bytes()
    ).hexdigest()

    if actual != expected:
        stop("PACKAGE_SHA_MISMATCH", path.name)

subprocess.check_call(
    ["python3", str(P13)]
)

subprocess.check_call(
    [
        "sha256sum",
        "-c",
        P14.name,
    ],
    cwd=PACKAGE_DIR
)

authorization = json.loads(
    A01.read_text(encoding="utf-8")
)

contract = json.loads(
    A03.read_text(encoding="utf-8")
)

if authorization.get("decision") != "0206":
    stop("AUTHORIZATION_DECISION_INVALID")

if authorization.get("status") != (
    "AUTHORIZED_FOR_ONE_EXTERNAL_INDEPENDENT_HUMAN_REVIEW_HANDOFF_TRANSACTION_ONLY"
):
    stop("AUTHORIZATION_STATUS_INVALID")

outputs = authorization.get(
    "authorized_external_outputs",
    {}
)

if outputs.get(
    "handoff_zip_expected_internal_package_file_count"
) != 14:
    stop("ZIP_FILE_COUNT_INVALID")

if outputs.get(
    "handoff_zip_must_contain_exact_internal_review_package_files"
) is not True:
    stop("ZIP_EXACT_COPY_BOUNDARY_INVALID")

if outputs.get(
    "editable_review_form_initial_bytes_must_equal_internal_blank_form"
) is not True:
    stop("EDITABLE_FORM_COPY_BOUNDARY_INVALID")

if outputs.get(
    "editable_review_form_initial_sha256"
) != EXPECTED_PACKAGE_SHA[P09]:
    stop("EDITABLE_FORM_INITIAL_SHA_INVALID")

human = authorization.get(
    "human_boundary",
    {}
)

for key in (
    "reviewer_identity_preassigned",
    "reviewer_role_preassigned",
    "reviewer_confirmation_preassigned",
    "review_date_preassigned",
    "independence_attestation_preassigned",
    "review_decisions_preassigned",
    "reviewer_notes_preassigned",
    "human_review_performed_by_handoff_transaction",
    "human_review_recorded_by_handoff_transaction",
):
    if human.get(key) is not False:
        stop("HUMAN_BOUNDARY_INVALID", key)

non_auth = authorization.get(
    "explicit_non_authorizations",
    {}
)

for key in (
    "completed_human_review_recording",
    "study_governance_adoption",
    "actual_accounting_evidence_acquisition",
    "concrete_accounting_instance_authoring",
    "source_unit_to_schema_carrier_mapping_creation",
    "accounting_satisfaction_determination",
    "accounting_satisfaction_establishment",
    "pair_reclassification",
    "supported_binding_creation",
    "not_supported_binding_creation",
    "operational_mapping",
    "schema_v2_losslessness_proof",
    "schema_v2_modification",
    "schema_successor",
    "curl_json",
    "analyzer",
    "baseline",
    "repair",
):
    if non_auth.get(key) is not False:
        stop("NONAUTHORIZATION_BOUNDARY_INVALID", key)

one_time = authorization.get(
    "one_time_handoff_authorization_verifier",
    {}
)

if one_time.get(
    "execution_authorized_in_decision0206"
) is not False:
    stop("A02_EXECUTION_PREMATURE")

if one_time.get(
    "authorized_future_execution_count"
) != 1:
    stop("A02_EXECUTION_COUNT_INVALID")

if one_time.get("rerun_authorized") is not False:
    stop("A02_RERUN_BOUNDARY_INVALID")

zip_contract = contract.get(
    "external_zip_contract",
    {}
)

if zip_contract.get("file_count") != 14:
    stop("CONTRACT_ZIP_FILE_COUNT_INVALID")

if len(zip_contract.get("include_exact_files", [])) != 14:
    stop("CONTRACT_ZIP_FILE_LIST_INVALID")

if zip_contract.get(
    "each_zip_entry_must_be_byte_identical_to_repository_source"
) is not True:
    stop("CONTRACT_ZIP_BYTE_IDENTITY_INVALID")

editable = contract.get(
    "editable_review_form_contract",
    {}
)

if editable.get(
    "initial_copy_must_be_byte_identical"
) is not True:
    stop("CONTRACT_EDITABLE_IDENTITY_INVALID")

if editable.get(
    "repository_blank_form_remains_immutable"
) is not True:
    stop("CONTRACT_BLANK_IMMUTABILITY_INVALID")

decision = DEC.read_text(
    encoding="utf-8"
)

for marker in (
    "EXTERNAL_REVIEW_HANDOFF_AUTHORIZED=YES",
    "EXTERNAL_REVIEW_HANDOFF_CREATED=NO",
    "EXTERNAL_EDITABLE_REVIEW_FORM_CREATED=NO",
    "HUMAN_REVIEW_PERFORMED=NO",
    "HUMAN_REVIEW_RECORDED=NO",
    "STUDY_GOVERNANCE_ADOPTED=NO",
    "ACCOUNTING_SATISFACTION_ESTABLISHED=NO",
    "PAIR_RECLASSIFICATION_PERFORMED=NO",
    "ANALYZER_AUTHORIZED=NO",
    "BASELINE_AUTHORIZED=NO",
    "REPAIR_AUTHORIZED=NO",
):
    if marker not in decision:
        stop(
            "DECISION0206_REQUIRED_MARKER_MISSING",
            marker
        )

print(
    "DECISION0206_EXTERNAL_INDEPENDENT_HUMAN_REVIEW_HANDOFF_AUTHORIZATION_VERIFIER=PASS"
)

print("PACKAGE_STATUS=BLANK_AWAITING_INDEPENDENT_HUMAN_REVIEW")
print("REVIEW_SUBJECT_STATUS=AUTHOR_CANDIDATE")
print("REVIEW_ITEM_COUNT=9")

print("EXTERNAL_REVIEW_HANDOFF_AUTHORIZED=YES")
print("EXTERNAL_REVIEW_HANDOFF_CREATED_BY_THIS_VERIFIER=NO")
print("EXTERNAL_EDITABLE_REVIEW_FORM_CREATED_BY_THIS_VERIFIER=NO")

print("REVIEWER_IDENTITY_PREASSIGNED=NO")
print("REVIEWER_ROLE_PREASSIGNED=NO")
print("HUMAN_REVIEW_PERFORMED=NO")
print("HUMAN_REVIEW_RECORDED=NO")
print("STUDY_GOVERNANCE_ADOPTED=NO")

print("ACCOUNTING_SATISFACTION_ESTABLISHED=NO")
print("PAIR_RECLASSIFICATION_PERFORMED=NO")

print("SUPPORTED_BINDING_COUNT=211")
print("UNRESOLVED_BINDING_COUNT=1642")
print("NOT_SUPPORTED_BINDING_COUNT=0")
print("REQ06_REQ14_UNRESOLVED_PAIR_COUNT=218")

print("OPERATIONAL_MAPPING_AUTHORIZED=NO")
print("SCHEMA_V2_LOSSLESSNESS_PROVEN=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")

print("AUTHORIZATION_EXECUTION_COUNT_FOR_THIS_RUN=1")
print("AUTHORIZATION_RERUN_AUTHORIZED=NO")
