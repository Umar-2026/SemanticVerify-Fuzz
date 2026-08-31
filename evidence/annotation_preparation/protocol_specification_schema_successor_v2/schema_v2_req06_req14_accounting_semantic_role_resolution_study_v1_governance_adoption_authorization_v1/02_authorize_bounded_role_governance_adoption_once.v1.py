#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import subprocess

D0199_COMMIT = (
    "e97b83518790e9715c55dfe8348f8b31088a23f6"
)

ROOT = Path(
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2"
)

PACKAGE_DIR = ROOT / (
    "schema_v2_req06_req14_accounting_semantic_role_resolution_"
    "study_v1_independent_human_review_package_v1"
)

P02 = PACKAGE_DIR / (
    "02_req06_req14_accounting_semantic_role_resolution_study."
    "EXACT_COPY.v1.json"
)

P03 = PACKAGE_DIR / (
    "03_req06_req14_accounting_role_evidence_anchor_matrix."
    "EXACT_COPY.v1.json"
)

RECORD_DIR = ROOT / (
    "schema_v2_req06_req14_accounting_semantic_role_resolution_"
    "study_v1_returned_independent_human_review_record_v1"
)

R01 = RECORD_DIR / (
    "01_returned_independent_human_review.EXACT_COPY.v1.md"
)

R02 = RECORD_DIR / (
    "02_returned_independent_human_review_record_manifest.v1.json"
)

R07 = RECORD_DIR / (
    "07_verify_returned_independent_human_review_record.v1.py"
)

R08 = RECORD_DIR / (
    "08_returned_independent_human_review_record.v1.SHA256SUMS"
)

AUTH_DIR = ROOT / (
    "schema_v2_req06_req14_accounting_semantic_role_resolution_"
    "study_v1_governance_adoption_authorization_v1"
)

A01 = AUTH_DIR / (
    "01_bounded_role_governance_adoption_authorization.v1.json"
)

A02 = AUTH_DIR / (
    "02_authorize_bounded_role_governance_adoption_once.v1.py"
)

A03 = AUTH_DIR / (
    "03_bounded_role_governance_adoption_contract.v1.json"
)

A04 = AUTH_DIR / (
    "04_bounded_role_governance_adoption_authorization_boundary.v1.md"
)

DEC = Path(
    "documentation/decisions/"
    "0200-authorize-governance-adoption-of-recorded-req06-req14-"
    "bounded-role-study-review-v1.md"
)

EXPECTED_PATHS = {
    str(A01),
    str(A02),
    str(A03),
    str(A04),
    str(DEC),
}

EXPECTED = {
    P02:
        "22c51d0d77f3faa086cb426788d057da15c5002a29b4ba68cd3177935aa80381",
    P03:
        "a153d0979f4bda119928fb29fd8043088115793f164e268c6d0def6fe1203601",
    R01:
        "a3a9f38ed79b3fa450d6799677b986b690a02f235ef21acf93cb5b75d2423309",
    R02:
        "1320dbec92e9ad18693802fe6f276185b279cc587b687d4ce5402d3a43a711c0",
    R07:
        "c3ee6605842cf1cf10e0e6294efe505bfe82c79efb56e51ec0ab1ed385cb9426",
    R08:
        "dfa9c747ccf75eb2da6a3e11b9408d554697644e9200b3361f0b31636c0bc97f",
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


def clean(value):
    value = value.strip()

    if (
        len(value) >= 2
        and value.startswith("`")
        and value.endswith("`")
    ):
        return value[1:-1].strip()

    return value


def next_value(lines, label):
    hits = [
        i
        for i, line in enumerate(lines)
        if line.startswith(label)
    ]

    if len(hits) != 1:
        stop(
            "REVIEW_FIELD_COUNT_INVALID",
            label
        )

    i = hits[0]

    inline = clean(
        lines[i][len(label):]
    )

    if inline:
        return inline

    j = i + 1

    while (
        j < len(lines)
        and not lines[j].strip()
    ):
        j += 1

    if j >= len(lines):
        stop(
            "REVIEW_FIELD_BLANK",
            label
        )

    value = clean(lines[j])

    if (
        not value
        or value.startswith("#")
        or value == "---"
    ):
        stop(
            "REVIEW_FIELD_BLANK",
            label
        )

    return value


if git(
    "rev-parse",
    "HEAD^"
) != D0199_COMMIT:
    stop(
        "D0200_PARENT_NOT_D0199"
    )

if subprocess.check_output(
    [
        "git",
        "status",
        "--porcelain=v1",
        "--untracked-files=all",
    ],
    text=True
).strip():
    stop(
        "REPOSITORY_NOT_CLEAN_BEFORE_GOVERNANCE_ADOPTION"
    )

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

if changed != EXPECTED_PATHS:
    stop(
        "D0200_COMMIT_SCOPE_MISMATCH",
        ",".join(sorted(changed))
    )

for path in (
    P02,
    P03,
    R01,
    R02,
    R07,
    R08,
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

for path, expected_sha in EXPECTED.items():
    actual = hashlib.sha256(
        path.read_bytes()
    ).hexdigest()

    if actual != expected_sha:
        stop(
            "BOUND_SOURCE_SHA_MISMATCH",
            str(path)
        )

record = json.loads(
    R02.read_text(encoding="utf-8")
)

if record.get("status") != (
    "RETURNED_INDEPENDENT_HUMAN_REVIEW_RECORDED_AWAITING_SEPARATE_GOVERNANCE_ADOPTION_DECISION"
):
    stop(
        "RECORDED_REVIEW_STATUS_INVALID"
    )

facts = record.get(
    "packet_recorded_review_facts",
    {}
)

if facts.get("pass_count") != 6:
    stop(
        "RECORDED_PASS_COUNT_INVALID"
    )

if facts.get(
    "revision_required_count"
) != 0:
    stop(
        "RECORDED_REVISION_COUNT_INVALID"
    )

if facts.get(
    "overall_review_decision"
) != "APPROVE_BOUNDED_ROLE_STUDY":
    stop(
        "RECORDED_OVERALL_REVIEW_DECISION_INVALID"
    )

gov = record.get(
    "governance_state",
    {}
)

for key in (
    "role_governance_adopted",
    "req06_role_governance_adopted",
    "req14_role_governance_adopted",
    "accounting_satisfaction_established",
    "pair_reclassification_performed",
    "supported_binding_created",
    "not_supported_binding_created",
    "operational_mapping_authorized",
    "schema_v2_losslessness_proven",
    "analyzer_authorized",
    "baseline_authorized",
    "repair_authorized",
):
    if gov.get(key) is not False:
        stop(
            "PRE_ADOPTION_GOVERNANCE_BOUNDARY_INVALID",
            key
        )

if gov.get(
    "supported_binding_count"
) != 211:
    stop(
        "SUPPORTED_BINDING_COUNT_INVALID"
    )

if gov.get(
    "unresolved_binding_count"
) != 1642:
    stop(
        "UNRESOLVED_BINDING_COUNT_INVALID"
    )

if gov.get(
    "not_supported_binding_count"
) != 0:
    stop(
        "NOT_SUPPORTED_BINDING_COUNT_INVALID"
    )

if gov.get(
    "req06_req14_unresolved_pair_count"
) != 218:
    stop(
        "REQ06_REQ14_UNRESOLVED_PAIR_COUNT_INVALID"
    )

review_text = R01.read_text(
    encoding="utf-8"
)

review_lines = review_text.splitlines()

expected_role = (
    "CROSS_CUTTING_ACCOUNTING_COMPLETENESS_CONSTRAINT"
)

expected_satisfaction = (
    "FURTHER_ACCOUNTING_SATISFACTION_EVIDENCE_REQUIRED"
)

if next_value(
    review_lines,
    "Req06 author-candidate role:"
) != expected_role:
    stop(
        "REQ06_REVIEWED_ROLE_CHANGED"
    )

if next_value(
    review_lines,
    "Req14 author-candidate role:"
) != expected_role:
    stop(
        "REQ14_REVIEWED_ROLE_CHANGED"
    )

if next_value(
    review_lines,
    "Req06 accounting-satisfaction state:"
) != expected_satisfaction:
    stop(
        "REQ06_SATISFACTION_STATE_CHANGED"
    )

if next_value(
    review_lines,
    "Req14 accounting-satisfaction state:"
) != expected_satisfaction:
    stop(
        "REQ14_SATISFACTION_STATE_CHANGED"
    )

if next_value(
    review_lines,
    "Overall review decision:"
) != "APPROVE_BOUNDED_ROLE_STUDY":
    stop(
        "RECORDED_REVIEW_APPROVAL_CHANGED"
    )

authorization = json.loads(
    A01.read_text(encoding="utf-8")
)

contract = json.loads(
    A03.read_text(encoding="utf-8")
)

if authorization.get("decision") != "0200":
    stop(
        "D0200_AUTHORIZATION_DECISION_INVALID"
    )

if authorization.get("status") != (
    "AUTHORIZED_TO_CREATE_BOUNDED_ROLE_GOVERNANCE_ADOPTION_RECORD_ONLY"
):
    stop(
        "D0200_AUTHORIZATION_STATUS_INVALID"
    )

adoption = authorization.get(
    "authorized_governance_adoption",
    {}
)

if adoption.get(
    "requirement_count"
) != 2:
    stop(
        "AUTHORIZED_REQUIREMENT_COUNT_INVALID"
    )

requirements = adoption.get(
    "requirements",
    {}
)

for req in (
    "Req06",
    "Req14",
):
    if requirements.get(
        req,
        {}
    ).get(
        "role_to_adopt"
    ) != expected_role:
        stop(
            "AUTHORIZED_ROLE_INVALID",
            req
        )

    if requirements.get(
        req,
        {}
    ).get(
        "accounting_satisfaction_state_to_preserve"
    ) != expected_satisfaction:
        stop(
            "AUTHORIZED_SATISFACTION_STATE_INVALID",
            req
        )

for key in (
    "adopt_exact_reviewed_role_conclusions",
    "create_separate_immutable_governance_adoption_record",
    "preserve_source_study_immutability",
    "preserve_recorded_review_immutability",
):
    if adoption.get(key) is not True:
        stop(
            "AUTHORIZED_ADOPTION_ACTIVITY_INVALID",
            key
        )

prohibited = authorization.get(
    "prohibited_effects",
    {}
)

for key in (
    "modify_author_candidate_study",
    "modify_recorded_human_review",
    "establish_accounting_satisfaction",
    "modify_requirement_to_semantic_unit_pair_matrix",
    "reclassify_requirement_to_semantic_unit_pairs",
    "create_supported_binding",
    "create_not_supported_binding",
    "operational_mapping",
    "schema_v2_losslessness_proof",
    "schema_v2_modification",
    "schema_successor",
    "curl_json",
    "analyzer_implementation",
    "analyzer_execution",
    "baseline_execution",
    "repair",
):
    if prohibited.get(key) is not False:
        stop(
            "PROHIBITED_EFFECT_BOUNDARY_INVALID",
            key
        )

pair_state = contract.get(
    "pair_state_invariance",
    {}
)

if pair_state.get(
    "supported_binding_count"
) != 211:
    stop(
        "CONTRACT_SUPPORTED_COUNT_INVALID"
    )

if pair_state.get(
    "unresolved_binding_count"
) != 1642:
    stop(
        "CONTRACT_UNRESOLVED_COUNT_INVALID"
    )

if pair_state.get(
    "not_supported_binding_count"
) != 0:
    stop(
        "CONTRACT_NOT_SUPPORTED_COUNT_INVALID"
    )

if pair_state.get(
    "req06_req14_unresolved_pair_count"
) != 218:
    stop(
        "CONTRACT_REQ06_REQ14_COUNT_INVALID"
    )

decision = DEC.read_text(
    encoding="utf-8"
)

for marker in (
    "ROLE_GOVERNANCE_ADOPTION_AUTHORIZED=YES",
    "ROLE_GOVERNANCE_ADOPTED=NO",
    "REQ06_ROLE_GOVERNANCE_ADOPTED=NO",
    "REQ14_ROLE_GOVERNANCE_ADOPTED=NO",
    "ACCOUNTING_SATISFACTION_ESTABLISHED=NO",
    "PAIR_RECLASSIFICATION_PERFORMED=NO",
    "OPERATIONAL_MAPPING_AUTHORIZED=NO",
    "ANALYZER_AUTHORIZED=NO",
    "BASELINE_AUTHORIZED=NO",
    "REPAIR_AUTHORIZED=NO",
):
    if marker not in decision:
        stop(
            "DECISION0200_REQUIRED_MARKER_MISSING",
            marker
        )

print(
    "DECISION0200_BOUNDED_ROLE_GOVERNANCE_ADOPTION_"
    "AUTHORIZATION_VERIFIER=PASS"
)

print(
    "ADOPTION_TARGET_REQUIREMENT_COUNT=2"
)

print(
    "REQ06_AUTHORIZED_ROLE="
    + expected_role
)

print(
    "REQ14_AUTHORIZED_ROLE="
    + expected_role
)

print(
    "REQ06_ACCOUNTING_SATISFACTION_STATE_PRESERVED="
    + expected_satisfaction
)

print(
    "REQ14_ACCOUNTING_SATISFACTION_STATE_PRESERVED="
    + expected_satisfaction
)

print(
    "ROLE_GOVERNANCE_ADOPTION_AUTHORIZED=YES"
)

print(
    "ROLE_GOVERNANCE_ADOPTED_BY_THIS_VERIFIER=NO"
)

print(
    "ACCOUNTING_SATISFACTION_ESTABLISHED=NO"
)

print(
    "PAIR_RECLASSIFICATION_PERFORMED=NO"
)

print(
    "SUPPORTED_BINDING_COUNT=211"
)

print(
    "UNRESOLVED_BINDING_COUNT=1642"
)

print(
    "NOT_SUPPORTED_BINDING_COUNT=0"
)

print(
    "REQ06_REQ14_UNRESOLVED_PAIR_COUNT=218"
)

print(
    "OPERATIONAL_MAPPING_AUTHORIZED=NO"
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
    "AUTHORIZATION_EXECUTION_COUNT_FOR_THIS_RUN=1"
)

print(
    "AUTHORIZATION_RERUN_AUTHORIZED=NO"
)
