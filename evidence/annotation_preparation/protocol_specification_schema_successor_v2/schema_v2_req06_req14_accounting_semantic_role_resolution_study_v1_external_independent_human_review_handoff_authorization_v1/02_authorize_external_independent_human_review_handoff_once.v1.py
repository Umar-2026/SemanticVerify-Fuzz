#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import subprocess

D0195_COMMIT = "a70ddd50d068bc91c69c99888b6db499cd8645ef"

ROOT = Path(
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2"
)

PACKAGE_DIR = ROOT / (
    "schema_v2_req06_req14_accounting_semantic_role_resolution_"
    "study_v1_independent_human_review_package_v1"
)

P01 = PACKAGE_DIR / "01_independent_human_review_package_manifest.v1.json"
P06 = PACKAGE_DIR / "06_blank_independent_human_review_form.v1.md"
P07 = PACKAGE_DIR / "07_decision0194_a02_consumption_record.v1.json"
P10 = PACKAGE_DIR / "10_verify_independent_human_review_package.v1.py"
P11 = PACKAGE_DIR / "11_independent_human_review_package.v1.SHA256SUMS"

AUTH_DIR = ROOT / (
    "schema_v2_req06_req14_accounting_semantic_role_resolution_study_v1_"
    "external_independent_human_review_handoff_authorization_v1"
)

A01 = AUTH_DIR / "01_external_independent_human_review_handoff_authorization.v1.json"
A02 = AUTH_DIR / "02_authorize_external_independent_human_review_handoff_once.v1.py"
A03 = AUTH_DIR / "03_external_independent_human_review_handoff_contract.v1.json"
A04 = AUTH_DIR / "04_external_independent_human_review_handoff_authorization_boundary.v1.md"

DEC = Path(
    "documentation/decisions/"
    "0196-authorize-external-independent-human-review-handoff-for-"
    "req06-req14-accounting-role-study-v1.md"
)

EXPECTED_D0196_PATHS = {
    str(A01),
    str(A02),
    str(A03),
    str(A04),
    str(DEC),
}

EXPECTED_SHA = {
    P01:
        "5eda213520d4d4032d932ed3c03fe0fe8dd7a0d34eb6e89191bf624e4dec3da2",
    P06:
        "c1ccf931d1d34ddacf80bcba47bf0d9adf1d109db5926a7c9ad8e068ad9e7faa",
    P07:
        "473d0d979ebe1f78366c1b3e6daa6afe5e0b61fe5086347c5915509c4408d0ab",
    P10:
        "e4d51877bbba92ddd475de3de7c941b5e52265da68a8aab887c37161ad251de3",
    P11:
        "ea49975a5f265911b737cc2b887b358ac97f37efd282386502dd29fc3fd28b06",
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


if git("rev-parse", "HEAD^") != D0195_COMMIT:
    stop("D0196_PARENT_NOT_D0195")

if subprocess.check_output(
    ["git", "status", "--porcelain=v1", "--untracked-files=all"],
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
        text=True,
    ).splitlines()
    if p.strip()
}

if changed != EXPECTED_D0196_PATHS:
    stop(
        "D0196_COMMIT_SCOPE_MISMATCH",
        ",".join(sorted(changed))
    )

for path, expected_sha in EXPECTED_SHA.items():
    if not path.is_file():
        stop("BOUND_PACKAGE_ARTIFACT_MISSING", str(path))

    actual = hashlib.sha256(path.read_bytes()).hexdigest()

    if actual != expected_sha:
        stop("BOUND_PACKAGE_ARTIFACT_SHA_MISMATCH", str(path))

for path in (A01, A02, A03, A04, DEC):
    if not path.is_file():
        stop("D0196_ARTIFACT_MISSING", str(path))

manifest = json.loads(P01.read_text(encoding="utf-8"))
consumption = json.loads(P07.read_text(encoding="utf-8"))
authorization = json.loads(A01.read_text(encoding="utf-8"))
contract = json.loads(A03.read_text(encoding="utf-8"))

if manifest.get("status") != (
    "BLANK_AWAITING_INDEPENDENT_HUMAN_REVIEW"
):
    stop("REVIEW_PACKAGE_STATUS_CHANGED")

if authorization.get("decision") != "0196":
    stop("D0196_AUTHORIZATION_DECISION_INVALID")

if authorization.get("status") != (
    "AUTHORIZED_TO_AUTHOR_EXTERNAL_INDEPENDENT_HUMAN_REVIEW_HANDOFF_ONLY"
):
    stop("D0196_AUTHORIZATION_STATUS_INVALID")

handoff = authorization.get(
    "authorized_handoff_activity",
    {}
)

for key in (
    "author_internal_handoff_record",
    "create_external_zip_from_exact_review_package",
    "create_external_editable_blank_review_form_copy",
    "preserve_blank_review_form_content_initially",
    "report_external_zip_sha256",
    "report_external_editable_copy_initial_sha256",
):
    if handoff.get(key) is not True:
        stop("AUTHORIZED_HANDOFF_ACTIVITY_MISSING", key)

for key in (
    "perform_human_review",
    "prefill_reviewer_identity",
    "prefill_reviewer_role",
    "prefill_review_item_decisions",
    "prefill_reviewer_notes",
    "prefill_overall_review_decision",
    "prefill_reviewer_confirmation",
    "prefill_review_date",
    "prefill_attestation",
    "record_returned_review",
    "adopt_review_result",
):
    if handoff.get(key) is not False:
        stop("HUMAN_HANDOFF_BOUNDARY_INVALID", key)

technical = authorization.get(
    "technical_non_authorizations",
    {}
)

for key in (
    "role_governance_adoption",
    "accounting_satisfaction_establishment",
    "pair_reclassification",
    "supported_binding_creation",
    "not_supported_binding_creation",
    "operational_mapping",
    "schema_v2_modification",
    "schema_successor",
    "curl_json",
    "analyzer_implementation",
    "analyzer_execution",
    "baseline_execution",
    "repair",
):
    if technical.get(key) is not False:
        stop("TECHNICAL_NONAUTHORIZATION_INVALID", key)

if consumption.get(
    "lifecycle_state"
) != "PERMANENTLY_RETIRED":
    stop("D0194_A02_NOT_RETIRED")

if consumption.get("rerun_authorized") is not False:
    stop("D0194_A02_RERUN_BOUNDARY_INVALID")

outputs = contract.get(
    "external_handoff_outputs",
    {}
)

for key in (
    "internal_handoff_manifest_required",
    "exact_review_package_copy_or_archive_required",
    "external_zip_required",
    "external_editable_blank_review_form_required",
    "external_editable_form_initially_byte_identical_to_internal_blank_form",
    "external_zip_checksum_required",
    "external_editable_form_initial_checksum_required",
):
    if outputs.get(key) is not True:
        stop("HANDOFF_OUTPUT_CONTRACT_INVALID", key)

non_effects = contract.get(
    "handoff_non_effects",
    {}
)

for key in (
    "handoff_is_not_human_review_completion",
    "handoff_is_not_review_recording",
    "handoff_is_not_governance_adoption",
    "handoff_does_not_reclassify_pairs",
    "handoff_does_not_establish_accounting_satisfaction",
    "handoff_does_not_authorize_operational_mapping",
    "handoff_does_not_authorize_analyzer",
    "handoff_does_not_authorize_baseline",
    "handoff_does_not_authorize_repair",
):
    if non_effects.get(key) is not True:
        stop("HANDOFF_NONEFFECT_CONTRACT_INVALID", key)

decision = DEC.read_text(encoding="utf-8")

for marker in (
    "EXTERNAL_INDEPENDENT_HUMAN_REVIEW_HANDOFF_AUTHORIZED=YES",
    "EXTERNAL_HANDOFF_AUTHORED=NO",
    "EXTERNAL_ZIP_CREATED=NO",
    "EXTERNAL_EDITABLE_REVIEW_COPY_CREATED=NO",
    "HUMAN_REVIEW_PERFORMED=NO",
    "HUMAN_REVIEW_RECORDED=NO",
    "ROLE_GOVERNANCE_ADOPTED=NO",
    "PAIR_RECLASSIFICATION_PERFORMED=NO",
    "ACCOUNTING_SATISFACTION_ESTABLISHED=NO",
    "OPERATIONAL_MAPPING_AUTHORIZED=NO",
    "ANALYZER_AUTHORIZED=NO",
    "BASELINE_AUTHORIZED=NO",
    "REPAIR_AUTHORIZED=NO",
):
    if marker not in decision:
        stop("DECISION0196_MARKER_MISSING", marker)

print("DECISION0196_EXTERNAL_HANDOFF_AUTHORIZATION_VERIFIER=PASS")
print("REVIEW_PACKAGE_STATUS=BLANK_AWAITING_INDEPENDENT_HUMAN_REVIEW")
print("REVIEW_ITEM_COUNT=6")
print("EXTERNAL_INDEPENDENT_HUMAN_REVIEW_HANDOFF_AUTHORIZED=YES")
print("EXTERNAL_HANDOFF_AUTHORED_BY_THIS_VERIFIER=NO")
print("EXTERNAL_ZIP_CREATED_BY_THIS_VERIFIER=NO")
print("EXTERNAL_EDITABLE_COPY_CREATED_BY_THIS_VERIFIER=NO")
print("HUMAN_REVIEW_PERFORMED_BY_THIS_VERIFIER=NO")
print("HUMAN_REVIEW_RECORDED_BY_THIS_VERIFIER=NO")
print("ROLE_GOVERNANCE_ADOPTED=NO")
print("PAIR_RECLASSIFICATION_PERFORMED=NO")
print("ACCOUNTING_SATISFACTION_ESTABLISHED=NO")
print("AUTHORIZATION_EXECUTION_COUNT_FOR_THIS_RUN=1")
print("AUTHORIZATION_RERUN_AUTHORIZED=NO")
