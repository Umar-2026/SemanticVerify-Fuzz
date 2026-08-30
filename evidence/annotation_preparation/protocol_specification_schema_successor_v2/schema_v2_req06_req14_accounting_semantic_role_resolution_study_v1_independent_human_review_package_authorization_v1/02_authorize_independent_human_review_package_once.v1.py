#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import subprocess

D0193_COMMIT = "bfa56e86ae24bf330a33b89cd70cb00fc5d9df4e"

ROOT = Path(
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2"
)

STUDY_DIR = ROOT / (
    "schema_v2_req06_req14_accounting_"
    "semantic_role_resolution_study_v1"
)

S01 = STUDY_DIR / (
    "01_req06_req14_accounting_semantic_role_resolution_study.v1.json"
)
S02 = STUDY_DIR / (
    "02_req06_req14_accounting_role_evidence_anchor_matrix.v1.json"
)
S03 = STUDY_DIR / "03_decision0192_a02_consumption_record.v1.json"

AUTH_DIR = ROOT / (
    "schema_v2_req06_req14_accounting_semantic_role_resolution_"
    "study_v1_independent_human_review_package_authorization_v1"
)

A01 = AUTH_DIR / "01_independent_human_review_package_authorization.v1.json"
A02 = AUTH_DIR / "02_authorize_independent_human_review_package_once.v1.py"
A03 = AUTH_DIR / "03_independent_human_review_contract.v1.json"
A04 = AUTH_DIR / "04_independent_human_review_package_authorization_boundary.v1.md"

DEC = Path(
    "documentation/decisions/"
    "0194-authorize-independent-human-review-package-for-"
    "req06-req14-accounting-semantic-role-study-v1.md"
)

EXPECTED_D0194_PATHS = {
    str(A01),
    str(A02),
    str(A03),
    str(A04),
    str(DEC),
}

EXPECTED_SHA = {
    S01:
        "22c51d0d77f3faa086cb426788d057da15c5002a29b4ba68cd3177935aa80381",
    S02:
        "a153d0979f4bda119928fb29fd8043088115793f164e268c6d0def6fe1203601",
    S03:
        "5b6e82be2e6c20a836f03cf3f4a396f7e5d6c6b524f03b4a00b7b7d093d7a09f",
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


if git("rev-parse", "HEAD^") != D0193_COMMIT:
    stop("D0194_PARENT_NOT_D0193")

if subprocess.check_output(
    ["git", "status", "--porcelain=v1", "--untracked-files=all"],
    text=True
).strip():
    stop("REPOSITORY_NOT_CLEAN_BEFORE_REVIEW_PACKAGE_AUTHORING")

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

if changed != EXPECTED_D0194_PATHS:
    stop(
        "D0194_COMMIT_SCOPE_MISMATCH",
        ",".join(sorted(changed))
    )

for path, expected in EXPECTED_SHA.items():
    if not path.is_file():
        stop("BOUND_STUDY_ARTIFACT_MISSING", str(path))

    actual = hashlib.sha256(path.read_bytes()).hexdigest()

    if actual != expected:
        stop("BOUND_STUDY_ARTIFACT_SHA_MISMATCH", str(path))

for path in (A01, A02, A03, A04, DEC):
    if not path.is_file():
        stop("D0194_ARTIFACT_MISSING", str(path))

authorization = json.loads(
    A01.read_text(encoding="utf-8")
)

contract = json.loads(
    A03.read_text(encoding="utf-8")
)

study = json.loads(
    S01.read_text(encoding="utf-8")
)

consumption = json.loads(
    S03.read_text(encoding="utf-8")
)

if authorization.get("decision") != "0194":
    stop("D0194_AUTHORIZATION_DECISION_INVALID")

if authorization.get("status") != (
    "AUTHORIZED_TO_AUTHOR_INDEPENDENT_HUMAN_REVIEW_PACKAGE_ONLY"
):
    stop("D0194_AUTHORIZATION_STATUS_INVALID")

package_auth = authorization.get(
    "review_package_authorization",
    {}
)

if package_auth.get("author_blank_review_package") is not True:
    stop("BLANK_REVIEW_PACKAGE_NOT_AUTHORIZED")

for key in (
    "prefill_reviewer_identity",
    "prefill_reviewer_role",
    "prefill_reviewer_decision",
    "prefill_reviewer_notes",
    "prefill_reviewer_signature_or_confirmation",
    "prefill_review_date",
    "prefill_attestation",
    "perform_human_review",
    "record_human_review",
    "adopt_review_result",
):
    if package_auth.get(key) is not False:
        stop("HUMAN_FIELD_PREFILL_OR_REVIEW_BOUNDARY_INVALID", key)

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
        stop("D0194_TECHNICAL_NONAUTHORIZATION_INVALID", key)

if study.get("status") != "AUTHOR_CANDIDATE":
    stop("STUDY_STATUS_CHANGED")

if study.get(
    "global_author_candidate_result", {}
).get("governance_adopted") is not False:
    stop("STUDY_ALREADY_GOVERNANCE_ADOPTED")

if study.get(
    "global_author_candidate_result", {}
).get("independent_human_review_required") is not True:
    stop("INDEPENDENT_REVIEW_REQUIREMENT_CHANGED")

if consumption.get("execution_count") != 1:
    stop("D0192_A02_EXECUTION_COUNT_INVALID")

if consumption.get(
    "lifecycle_state"
) != "PERMANENTLY_RETIRED":
    stop("D0192_A02_NOT_RETIRED")

if consumption.get("rerun_authorized") is not False:
    stop("D0192_A02_RERUN_BOUNDARY_INVALID")

items = contract.get("required_review_items")

if not isinstance(items, list) or len(items) != 6:
    stop("REVIEW_ITEM_COUNT_INVALID")

if [
    item.get("review_item_id")
    for item in items
] != [
    "ASRR01",
    "ASRR02",
    "ASRR03",
    "ASRR04",
    "ASRR05",
    "ASRR06",
]:
    stop("REVIEW_ITEM_SEQUENCE_INVALID")

for item in items:
    if item.get("allowed_decisions") != [
        "PASS",
        "REVISION_REQUIRED"
    ]:
        stop(
            "REVIEW_ITEM_DECISION_VOCABULARY_INVALID",
            item.get("review_item_id", "")
        )

if contract.get(
    "allowed_overall_review_decisions"
) != [
    "APPROVE_BOUNDED_ROLE_STUDY",
    "REVISION_REQUIRED"
]:
    stop("OVERALL_REVIEW_DECISION_VOCABULARY_INVALID")

independence = contract.get(
    "reviewer_independence_requirement",
    {}
)

for key in (
    "independent_human_review_required",
    "reviewer_must_not_be_the_author_of_the_author_candidate_study",
    "reviewer_identity_must_be_human_supplied",
    "reviewer_role_must_be_human_supplied",
    "reviewer_decision_must_be_human_supplied",
    "reviewer_notes_must_be_human_supplied",
    "reviewer_confirmation_must_be_human_supplied",
    "review_date_must_be_human_supplied",
    "review_attestation_must_be_human_supplied",
):
    if independence.get(key) is not True:
        stop("REVIEWER_INDEPENDENCE_CONTRACT_INVALID", key)

decision = DEC.read_text(encoding="utf-8")

for marker in (
    "INDEPENDENT_HUMAN_REVIEW_PACKAGE_AUTHORIZED=YES",
    "HUMAN_REVIEW_PACKAGE_AUTHORED=NO",
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
        stop("DECISION0194_MARKER_MISSING", marker)

print("DECISION0194_REVIEW_PACKAGE_AUTHORIZATION_VERIFIER=PASS")
print("REVIEW_SUBJECT_STATUS=AUTHOR_CANDIDATE")
print("TARGET_REQUIREMENT_COUNT=2")
print("REVIEW_ITEM_COUNT=6")
print("INDEPENDENT_HUMAN_REVIEW_PACKAGE_AUTHORIZED=YES")
print("HUMAN_REVIEW_PACKAGE_AUTHORED_BY_THIS_VERIFIER=NO")
print("HUMAN_REVIEW_PERFORMED_BY_THIS_VERIFIER=NO")
print("REVIEWER_IDENTITY_SYNTHESIZED=NO")
print("REVIEWER_DECISION_SYNTHESIZED=NO")
print("ROLE_GOVERNANCE_ADOPTED=NO")
print("PAIR_RECLASSIFICATION_PERFORMED=NO")
print("ACCOUNTING_SATISFACTION_ESTABLISHED=NO")
print("AUTHORIZATION_EXECUTION_COUNT_FOR_THIS_RUN=1")
print("AUTHORIZATION_RERUN_AUTHORIZED=NO")
