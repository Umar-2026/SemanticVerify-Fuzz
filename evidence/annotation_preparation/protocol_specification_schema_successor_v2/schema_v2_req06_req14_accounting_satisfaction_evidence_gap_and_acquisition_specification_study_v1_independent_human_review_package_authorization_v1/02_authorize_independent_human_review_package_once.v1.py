#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import subprocess

D0203_COMMIT = (
    "70437180754f8248a5cc06d0af3e59c2c343520c"
)

ROOT = Path(
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2"
)

STUDY_DIR = ROOT / (
    "schema_v2_req06_req14_accounting_satisfaction_"
    "evidence_gap_and_acquisition_specification_study_v1"
)

S01 = STUDY_DIR / (
    "01_accounting_satisfaction_evidence_gap_assessment.v1.json"
)

S02 = STUDY_DIR / (
    "02_future_accounting_evidence_acquisition_specification.v1.json"
)

S03 = STUDY_DIR / (
    "03_machine_checkable_accounting_satisfaction_criteria.v1.json"
)

S04 = STUDY_DIR / (
    "04_study_source_binding.v1.json"
)

S05 = STUDY_DIR / (
    "05_decision0202_a02_consumption_record.v1.json"
)

S06 = STUDY_DIR / (
    "06_decision0202_a02_execution_output.EXACT_COPY.v1.txt"
)

S07 = STUDY_DIR / (
    "07_decision0202_a02_consumption_sentinel.EXACT_COPY.v1.json"
)

S08 = STUDY_DIR / (
    "08_study_boundary.v1.md"
)

S09 = STUDY_DIR / (
    "09_verify_accounting_satisfaction_evidence_gap_and_"
    "acquisition_specification_study.v1.py"
)

S10 = STUDY_DIR / (
    "10_accounting_satisfaction_evidence_gap_and_"
    "acquisition_specification_study.v1.SHA256SUMS"
)

D0203 = Path(
    "documentation/decisions/"
    "0203-author-req06-req14-accounting-satisfaction-"
    "evidence-gap-and-acquisition-specification-study-v1.md"
)

AUTH_DIR = ROOT / (
    "schema_v2_req06_req14_accounting_satisfaction_"
    "evidence_gap_and_acquisition_specification_study_v1_"
    "independent_human_review_package_authorization_v1"
)

A01 = AUTH_DIR / (
    "01_independent_human_review_package_authorization.v1.json"
)

A02 = AUTH_DIR / (
    "02_authorize_independent_human_review_package_once.v1.py"
)

A03 = AUTH_DIR / (
    "03_independent_human_review_package_contract.v1.json"
)

A04 = AUTH_DIR / (
    "04_independent_human_review_package_authorization_boundary.v1.md"
)

DEC = Path(
    "documentation/decisions/"
    "0204-authorize-independent-human-review-package-for-req06-req14-"
    "accounting-satisfaction-evidence-gap-and-acquisition-specification-"
    "study-v1.md"
)

FUTURE_PACKAGE_DIR = ROOT / (
    "schema_v2_req06_req14_accounting_satisfaction_"
    "evidence_gap_and_acquisition_specification_study_v1_"
    "independent_human_review_package_v1"
)

EXPECTED_D0204_PATHS = {
    str(A01),
    str(A02),
    str(A03),
    str(A04),
    str(DEC),
}

EXPECTED_SOURCE_SHA = {
    S01:
        "6dd6540f0655c1ac064460560d2429fa62762ac4e6bb52e671283ff227f0b2a9",
    S02:
        "c4c77261ef19d929112ca56247d223ad7a04d9f6661dcc08860ff4a77dfabc83",
    S03:
        "e74e58463659531a393c24a6a8de616f4efa9b688d13a24b67e876f4d0ca8436",
    S04:
        "ec0e753dfc694ff8764d2452bceddf820cf3740f55b02c218bc661db7e75cf72",
    S05:
        "b392b256a707b59e643b53322c684d9e1dc76be023e0f62700f282a0d915174d",
    S06:
        "dc2f03f4a0afa97f6c5a43cf6cc28eed7d65e43c2dbc31e2e98ce218cd3b8136",
    S07:
        "6718c7bbeec9ecdc411c7f53ff3de2db8aadc973647d2d26220b4f7072037486",
    S08:
        "451e1648c6f5eeea38bcb485839c5bb03e3eba6cc378d3fd49970317dc10f963",
    S09:
        "50c97680a709fefe0dd68b96ea06146df8f0bff92387bd6b704a360811642d2a",
    S10:
        "99223bf924883efbda6821dee0ab2afb86119517b8cc3eee844ca5e475841598",
    D0203:
        "4d0a29bea5a1f76035f9f2aa2ea0dbe88ef2b6f19eb469885a28bbca2bdbea9c",
}

ALLOWED_ITEM = {
    "PASS",
    "REVISION_REQUIRED",
}

ALLOWED_OVERALL = {
    "APPROVE_BOUNDED_EVIDENCE_GAP_AND_ACQUISITION_SPECIFICATION_STUDY",
    "REVISION_REQUIRED",
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


if git("rev-parse", "HEAD^") != D0203_COMMIT:
    stop("D0204_PARENT_NOT_D0203")

if subprocess.check_output(
    [
        "git",
        "status",
        "--porcelain=v1",
        "--untracked-files=all",
    ],
    text=True
).strip():
    stop("REPOSITORY_NOT_CLEAN_BEFORE_PACKAGE_AUTHORING")

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

if changed != EXPECTED_D0204_PATHS:
    stop(
        "D0204_COMMIT_SCOPE_MISMATCH",
        ",".join(sorted(changed))
    )

if FUTURE_PACKAGE_DIR.exists():
    stop("REVIEW_PACKAGE_ALREADY_EXISTS")

for path in (
    *EXPECTED_SOURCE_SHA.keys(),
    A01,
    A02,
    A03,
    A04,
    DEC,
):
    if not path.is_file():
        stop(
            "REQUIRED_ARTIFACT_MISSING",
            str(path)
        )

for path, expected in EXPECTED_SOURCE_SHA.items():
    actual = hashlib.sha256(
        path.read_bytes()
    ).hexdigest()

    if actual != expected:
        stop(
            "IMMUTABLE_SOURCE_SHA_MISMATCH",
            str(path)
        )

authorization = json.loads(
    A01.read_text(encoding="utf-8")
)

contract = json.loads(
    A03.read_text(encoding="utf-8")
)

if authorization.get("decision") != "0204":
    stop("AUTHORIZATION_DECISION_INVALID")

if authorization.get("status") != (
    "AUTHORIZED_TO_AUTHOR_BLANK_INDEPENDENT_HUMAN_REVIEW_PACKAGE_ONLY"
):
    stop("AUTHORIZATION_STATUS_INVALID")

subject = authorization.get(
    "review_subject",
    {}
)

if subject.get("study_status") != "AUTHOR_CANDIDATE":
    stop("REVIEW_SUBJECT_STATUS_INVALID")

if subject.get("study_result") != (
    "EVIDENCE_GAP_CONFIRMED_ACQUISITION_SPECIFICATION_READY"
):
    stop("REVIEW_SUBJECT_RESULT_INVALID")

if subject.get("independent_human_review_required") is not True:
    stop("REVIEW_REQUIREMENT_INVALID")

if subject.get("independent_human_review_completed") is not False:
    stop("REVIEW_COMPLETION_STATE_INVALID")

if subject.get("governance_adopted") is not False:
    stop("REVIEW_SUBJECT_GOVERNANCE_STATE_INVALID")

package = authorization.get(
    "authorized_review_package",
    {}
)

if package.get("package_status") != (
    "BLANK_AWAITING_INDEPENDENT_HUMAN_REVIEW"
):
    stop("PACKAGE_STATUS_INVALID")

if package.get("review_item_count") != 9:
    stop("PACKAGE_REVIEW_ITEM_COUNT_INVALID")

for key in (
    "include_exact_gap_assessment",
    "include_exact_future_acquisition_specification",
    "include_exact_machine_checkable_satisfaction_criteria",
    "include_exact_study_source_binding",
    "include_exact_study_boundary",
    "include_review_contract",
    "include_reviewer_instructions",
    "include_blank_human_review_form",
    "include_decision0204_a02_consumption_evidence",
    "include_safe_rerunnable_package_verifier",
    "include_checksum_manifest",
):
    if package.get(key) is not True:
        stop(
            "PACKAGE_CONTENT_AUTHORIZATION_INVALID",
            key
        )

human = authorization.get(
    "human_review_form_requirements",
    {}
)

for key in (
    "reviewer_name_must_be_blank_at_package_authoring",
    "reviewer_role_must_be_blank_at_package_authoring",
    "reviewer_confirmation_must_be_blank_at_package_authoring",
    "review_date_must_be_blank_at_package_authoring",
    "independent_review_attestation_must_be_blank_at_package_authoring",
    "all_item_decisions_must_be_blank_at_package_authoring",
    "all_reviewer_notes_must_be_blank_at_package_authoring",
    "overall_review_decision_must_be_blank_at_package_authoring",
    "overall_reviewer_notes_must_be_blank_at_package_authoring",
):
    if human.get(key) is not True:
        stop(
            "BLANK_FORM_REQUIREMENT_INVALID",
            key
        )

for key in (
    "reviewer_identity_preassigned",
    "reviewer_role_preassigned",
):
    if human.get(key) is not False:
        stop(
            "HUMAN_PREFILL_BOUNDARY_INVALID",
            key
        )

vocab = authorization.get(
    "allowed_review_vocabulary",
    {}
)

if set(vocab.get("item_decisions", [])) != ALLOWED_ITEM:
    stop("ITEM_DECISION_VOCABULARY_INVALID")

if set(vocab.get("overall_decisions", [])) != ALLOWED_OVERALL:
    stop("OVERALL_DECISION_VOCABULARY_INVALID")

independence = authorization.get(
    "independence_boundary",
    {}
)

if independence.get(
    "genuine_independent_human_review_required"
) is not True:
    stop("INDEPENDENCE_REQUIREMENT_INVALID")

if independence.get(
    "reviewer_must_not_be_author_of_author_candidate_study"
) is not True:
    stop("INDEPENDENCE_AUTHOR_BOUNDARY_INVALID")

if independence.get(
    "specific_reviewer_identity_required_by_authorization"
) is not False:
    stop("SPECIFIC_REVIEWER_IDENTITY_BOUNDARY_INVALID")

if independence.get(
    "specific_reviewer_role_label_required_by_authorization"
) is not False:
    stop("SPECIFIC_REVIEWER_ROLE_BOUNDARY_INVALID")

non_auth = authorization.get(
    "explicit_non_authorizations",
    {}
)

for key in (
    "human_review_performed",
    "human_review_recorded",
    "study_governance_adopted",
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
        stop(
            "NONAUTHORIZATION_BOUNDARY_INVALID",
            key
        )

one_time = authorization.get(
    "one_time_package_authoring_verifier",
    {}
)

if one_time.get(
    "execution_authorized_in_decision0204"
) is not False:
    stop("A02_EXECUTION_PREMATURE")

if one_time.get(
    "authorized_future_execution_count"
) != 1:
    stop("A02_EXECUTION_COUNT_INVALID")

if one_time.get(
    "rerun_authorized"
) is not False:
    stop("A02_RERUN_BOUNDARY_INVALID")

if contract.get(
    "review_subject_status"
) != "AUTHOR_CANDIDATE":
    stop("CONTRACT_SUBJECT_STATUS_INVALID")

if contract.get(
    "review_subject_result"
) != (
    "EVIDENCE_GAP_CONFIRMED_ACQUISITION_SPECIFICATION_READY"
):
    stop("CONTRACT_SUBJECT_RESULT_INVALID")

if contract.get("review_item_count") != 9:
    stop("CONTRACT_REVIEW_ITEM_COUNT_INVALID")

items = contract.get("review_items", [])

expected_ids = [
    "ASER01",
    "ASER02",
    "ASER03",
    "ASER04",
    "ASER05",
    "ASER06",
    "ASER07",
    "ASER08",
    "ASER09",
]

if [item.get("id") for item in items] != expected_ids:
    stop("CONTRACT_REVIEW_ITEM_SEQUENCE_INVALID")

for item in items:
    if not str(item.get("title", "")).strip():
        stop("CONTRACT_ITEM_TITLE_BLANK", item.get("id", ""))

    if not str(item.get("question", "")).strip():
        stop("CONTRACT_ITEM_QUESTION_BLANK", item.get("id", ""))

if set(contract.get("allowed_item_decisions", [])) != ALLOWED_ITEM:
    stop("CONTRACT_ITEM_VOCABULARY_INVALID")

if set(contract.get("allowed_overall_decisions", [])) != ALLOWED_OVERALL:
    stop("CONTRACT_OVERALL_VOCABULARY_INVALID")

blank = contract.get(
    "blank_package_requirement",
    {}
)

for key in (
    "all_human_fields_blank",
    "all_item_decisions_blank",
    "all_item_notes_blank",
    "overall_decision_blank",
    "overall_notes_blank",
):
    if blank.get(key) is not True:
        stop(
            "CONTRACT_BLANK_PACKAGE_REQUIREMENT_INVALID",
            key
        )

decision = DEC.read_text(
    encoding="utf-8"
)

for marker in (
    "INDEPENDENT_HUMAN_REVIEW_PACKAGE_AUTHORIZED=YES",
    "REVIEW_SUBJECT_STATUS=AUTHOR_CANDIDATE",
    "REVIEW_ITEM_COUNT=9",
    "HUMAN_REVIEW_PERFORMED=NO",
    "HUMAN_REVIEW_RECORDED=NO",
    "STUDY_GOVERNANCE_ADOPTED=NO",
    "ACTUAL_ACCOUNTING_EVIDENCE_ACQUISITION_AUTHORIZED=NO",
    "ACCOUNTING_SATISFACTION_ESTABLISHED=NO",
    "PAIR_RECLASSIFICATION_PERFORMED=NO",
    "ANALYZER_AUTHORIZED=NO",
    "BASELINE_AUTHORIZED=NO",
    "REPAIR_AUTHORIZED=NO",
):
    if marker not in decision:
        stop(
            "DECISION0204_REQUIRED_MARKER_MISSING",
            marker
        )

print(
    "DECISION0204_INDEPENDENT_HUMAN_REVIEW_PACKAGE_AUTHORIZATION_VERIFIER=PASS"
)

print(
    "REVIEW_SUBJECT_STATUS=AUTHOR_CANDIDATE"
)

print(
    "REVIEW_SUBJECT_RESULT="
    "EVIDENCE_GAP_CONFIRMED_ACQUISITION_SPECIFICATION_READY"
)

print("REVIEW_ITEM_COUNT=9")
print("PACKAGE_AUTHORING_AUTHORIZED=YES")
print("PACKAGE_AUTHORED_BY_THIS_VERIFIER=NO")

print("REVIEWER_IDENTITY_PREASSIGNED=NO")
print("REVIEWER_ROLE_PREASSIGNED=NO")
print("HUMAN_REVIEW_PERFORMED=NO")
print("HUMAN_REVIEW_RECORDED=NO")
print("STUDY_GOVERNANCE_ADOPTED=NO")

print("ACTUAL_ACCOUNTING_EVIDENCE_ACQUISITION_AUTHORIZED=NO")
print("CONCRETE_ACCOUNTING_INSTANCE_AUTHORING_AUTHORIZED=NO")
print("SOURCE_UNIT_TO_SCHEMA_CARRIER_MAPPING_CREATION_AUTHORIZED=NO")
print("ACCOUNTING_SATISFACTION_DETERMINATION_AUTHORIZED=NO")
print("ACCOUNTING_SATISFACTION_ESTABLISHED=NO")

print("PAIR_RECLASSIFICATION_PERFORMED=NO")
print("SUPPORTED_BINDING_COUNT=211")
print("UNRESOLVED_BINDING_COUNT=1642")
print("NOT_SUPPORTED_BINDING_COUNT=0")
print("REQ06_REQ14_UNRESOLVED_PAIR_COUNT=218")

print("SCHEMA_V2_LOSSLESSNESS_PROVEN=NO")
print("OPERATIONAL_MAPPING_AUTHORIZED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")

print("AUTHORIZATION_EXECUTION_COUNT_FOR_THIS_RUN=1")
print("AUTHORIZATION_RERUN_AUTHORIZED=NO")
