#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import subprocess

D0201_COMMIT = (
    "b76886d774aacaaee50a899aefdf9e6b5209e20d"
)

ROOT = Path(
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2"
)

ADOPTION_DIR = ROOT / (
    "schema_v2_req06_req14_accounting_semantic_role_resolution_"
    "study_v1_governance_adoption_record_v1"
)

G01 = ADOPTION_DIR / (
    "01_bounded_role_governance_adoption_manifest.v1.json"
)

SCHEMA = Path(
    "config/schemas/protocol_specification.v2.schema.json"
)

CARRIER_ASSESS = ROOT / (
    "schema_v2_requirement_bound_carrier_admissibility_resolution_"
    "study_v1/01_requirement_bound_carrier_admissibility_assessment.v1.json"
)

CARRIER_ADOPTION = ROOT / (
    "schema_v2_requirement_bound_carrier_admissibility_resolution_"
    "study_v1_bounded_governance_adoption_v1/"
    "01_bounded_governance_adoption_manifest.v1.json"
)

CAPABILITY = ROOT / (
    "schema_v2_exhaustive_admissible_multifield_capability_study_v1/"
    "01_exhaustive_admissible_existing_schema_v2_multifield_capability_study.v1.json"
)

RELATION = ROOT / (
    "schema_v2_relation_informed_exhaustive_admissible_composition_study_v1/"
    "02_exhaustiveness_accounting.v1.json"
)

DESIGN = ROOT / (
    "04_schema_v2_successor_design_record.v1.json"
)

RESIDUAL = ROOT / (
    "schema_v2_residual_losslessness_insufficiency_proof_v1/"
    "01_residual_schema_v2_losslessness_insufficiency_proof.v1.json"
)

AUTH_DIR = ROOT / (
    "schema_v2_req06_req14_accounting_satisfaction_"
    "evidence_gap_and_acquisition_study_v1_authorization"
)

A01 = AUTH_DIR / (
    "01_accounting_satisfaction_evidence_gap_and_acquisition_"
    "study_authorization.v1.json"
)

A02 = AUTH_DIR / (
    "02_authorize_accounting_satisfaction_evidence_gap_and_"
    "acquisition_study_once.v1.py"
)

A03 = AUTH_DIR / (
    "03_accounting_satisfaction_evidence_gap_and_acquisition_"
    "study_contract.v1.json"
)

A04 = AUTH_DIR / (
    "04_accounting_satisfaction_evidence_gap_and_acquisition_"
    "study_authorization_boundary.v1.md"
)

DEC = Path(
    "documentation/decisions/"
    "0202-authorize-req06-req14-accounting-satisfaction-"
    "evidence-gap-and-acquisition-study-v1.md"
)

EXPECTED_D0202_PATHS = {
    str(A01),
    str(A02),
    str(A03),
    str(A04),
    str(DEC),
}

EXPECTED_SOURCE_SHA = {
    G01:
        "5c7b3c8dd77cd427ffd74a21f6e818daa99e4d02461635d76192ac0c2c08767e",
    SCHEMA:
        "c6ebb5ef2214c4168283f9009d1f7ce6e88d2ff928853fe6a57ed1f7521c6956",
    CARRIER_ASSESS:
        "2c9ca9125aa89dd77f7f74950f7285657fcaee7dbd17ce0dca01012ad716263c",
    CARRIER_ADOPTION:
        "d133548d4c3b7eef2436faabece406b3bfb815bab12c0a5c119c84258e84169a",
    CAPABILITY:
        "9bf685bcd5d8286938f4e221bffd2cc1acc8b5da961d3b0e14f1b10a6a43b78b",
    RELATION:
        "ae56e06b6668c301167efdd7e81ba937848446215b49be52d1268c69a2c5d643",
    DESIGN:
        "eb0367a18ca2474084a90b0aaf44b769b2ac2855f270b0d94814b35590749e90",
    RESIDUAL:
        "400f6806217f50b79d17ec77e41683d9077f64e07c63e5421c8b1922b49aaff0",
}

ROLE = (
    "CROSS_CUTTING_ACCOUNTING_COMPLETENESS_CONSTRAINT"
)

SATISFACTION = (
    "FURTHER_ACCOUNTING_SATISFACTION_EVIDENCE_REQUIRED"
)

SAFE_STUDY = (
    "Req06/Req14 Accounting Satisfaction Evidence Gap "
    "and Acquisition Specification Study V1"
)


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


if git("rev-parse", "HEAD^") != D0201_COMMIT:
    stop("D0202_PARENT_NOT_D0201")

if subprocess.check_output(
    [
        "git",
        "status",
        "--porcelain=v1",
        "--untracked-files=all",
    ],
    text=True
).strip():
    stop("REPOSITORY_NOT_CLEAN_BEFORE_STUDY_AUTHORING")

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

if changed != EXPECTED_D0202_PATHS:
    stop(
        "D0202_COMMIT_SCOPE_MISMATCH",
        ",".join(sorted(changed))
    )

for path in (
    G01,
    SCHEMA,
    CARRIER_ASSESS,
    CARRIER_ADOPTION,
    CAPABILITY,
    RELATION,
    DESIGN,
    RESIDUAL,
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

adoption = json.loads(
    G01.read_text(encoding="utf-8")
)

gov = adoption.get(
    "governance_state",
    {}
)

for key in (
    "role_governance_adopted",
    "req06_role_governance_adopted",
    "req14_role_governance_adopted",
):
    if gov.get(key) is not True:
        stop(
            "GOVERNED_ROLE_PRECONDITION_INVALID",
            key
        )

if gov.get(
    "accounting_satisfaction_established"
) is not False:
    stop(
        "ACCOUNTING_SATISFACTION_ALREADY_ESTABLISHED_UNEXPECTEDLY"
    )

if gov.get(
    "supported_binding_count"
) != 211:
    stop("SUPPORTED_BINDING_COUNT_INVALID")

if gov.get(
    "unresolved_binding_count"
) != 1642:
    stop("UNRESOLVED_BINDING_COUNT_INVALID")

if gov.get(
    "not_supported_binding_count"
) != 0:
    stop("NOT_SUPPORTED_BINDING_COUNT_INVALID")

if gov.get(
    "req06_req14_unresolved_pair_count"
) != 218:
    stop("REQ06_REQ14_UNRESOLVED_PAIR_COUNT_INVALID")

authorization = json.loads(
    A01.read_text(encoding="utf-8")
)

if authorization.get("decision") != "0202":
    stop("AUTHORIZATION_DECISION_INVALID")

if authorization.get("status") != (
    "AUTHORIZED_TO_AUTHOR_BOUNDED_ACCOUNTING_SATISFACTION_"
    "EVIDENCE_GAP_AND_ACQUISITION_SPECIFICATION_STUDY_ONLY"
):
    stop("AUTHORIZATION_STATUS_INVALID")

scope = authorization.get(
    "governed_requirement_scope",
    {}
)

if scope.get(
    "requirement_count"
) != 2:
    stop("AUTHORIZED_REQUIREMENT_COUNT_INVALID")

for req, key in (
    ("Req06", "forward_accounting_required"),
    ("Req14", "reverse_accounting_required"),
):
    entry = scope.get(req, {})

    if entry.get("requirement_key") != key:
        stop(
            "AUTHORIZED_REQUIREMENT_KEY_INVALID",
            req
        )

    if entry.get("governance_role") != ROLE:
        stop(
            "AUTHORIZED_GOVERNANCE_ROLE_INVALID",
            req
        )

    if entry.get(
        "current_accounting_satisfaction_state"
    ) != SATISFACTION:
        stop(
            "AUTHORIZED_SATISFACTION_STATE_INVALID",
            req
        )

finding = authorization.get(
    "current_evidence_finding",
    {}
)

required_finding = {
    "active_schema_supports_forward_accounting": True,
    "active_schema_supports_reverse_accounting": True,
    "active_schema_requires_forward_complete_true": True,
    "active_schema_requires_reverse_complete_true": True,
    "existing_relation_evidence_contains_concrete_accounting_instance": False,
    "constructive_full_exact_mapping_witness_complete": False,
    "deterministic_complete_forward_encoding_proven": False,
    "deterministic_exact_reverse_reconstruction_proven": False,
    "accounting_alone_proves_semantic_encoding": False,
    "current_immutable_evidence_structurally_sufficient_for_concrete_accounting_satisfaction_assessment": False,
}

for key, expected in required_finding.items():
    if finding.get(key) != expected:
        stop(
            "CURRENT_EVIDENCE_FINDING_INVALID",
            key
        )

study = authorization.get(
    "authorized_study",
    {}
)

if study.get("study_name") != SAFE_STUDY:
    stop("AUTHORIZED_STUDY_NAME_INVALID")

if study.get("status") != "AUTHOR_CANDIDATE":
    stop("AUTHORIZED_STUDY_STATUS_INVALID")

for key in (
    "authoring_only",
    "identify_current_evidence_gaps",
    "specify_future_evidence_acquisition_requirements",
    "define_future_machine_checkable_satisfaction_criteria",
    "bind_current_immutable_evidence",
    "independent_human_review_required_before_governance_adoption",
):
    if study.get(key) is not True:
        stop(
            "AUTHORIZED_STUDY_ACTIVITY_INVALID",
            key
        )

for key in (
    "actual_accounting_evidence_acquisition_authorized",
    "concrete_accounting_instance_authoring_authorized",
    "accounting_satisfaction_determination_authorized",
):
    if study.get(key) is not False:
        stop(
            "STUDY_BOUNDARY_INVALID",
            key
        )

prohibited = authorization.get(
    "prohibited_effects",
    {}
)

for key in (
    "establish_accounting_satisfaction",
    "create_concrete_forward_accounting_relation",
    "create_concrete_reverse_accounting_relation",
    "populate_semantic_accounting_instance",
    "create_source_unit_to_schema_carrier_mapping",
    "operational_mapping",
    "modify_requirement_to_semantic_unit_pair_matrix",
    "reclassify_requirement_to_semantic_unit_pairs",
    "create_supported_binding",
    "create_not_supported_binding",
    "prove_schema_v2_losslessness",
    "modify_schema_v2",
    "authorize_schema_successor",
    "authorize_curl_json",
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

contract = json.loads(
    A03.read_text(encoding="utf-8")
)

if contract.get(
    "study_status"
) != "AUTHOR_CANDIDATE":
    stop("CONTRACT_STUDY_STATUS_INVALID")

allowed = set(
    contract.get(
        "allowed_author_candidate_results",
        []
    )
)

if allowed != {
    "EVIDENCE_GAP_CONFIRMED_ACQUISITION_SPECIFICATION_READY",
    "EVIDENCE_GAP_REQUIRES_FURTHER_SCOPING",
}:
    stop(
        "ALLOWED_RESULT_VOCABULARY_INVALID"
    )

forbidden = set(
    contract.get(
        "forbidden_study_results",
        []
    )
)

for required in (
    "ACCOUNTING_SATISFACTION_ESTABLISHED",
    "FORWARD_ACCOUNTING_SATISFIED",
    "REVERSE_ACCOUNTING_SATISFIED",
    "SCHEMA_V2_LOSSLESSNESS_PROVEN",
    "PAIR_RECLASSIFICATION_COMPLETED",
    "OPERATIONAL_MAPPING_COMPLETED",
):
    if required not in forbidden:
        stop(
            "FORBIDDEN_RESULT_MISSING",
            required
        )

pair = contract.get(
    "pair_state_invariance",
    {}
)

if pair.get(
    "supported_binding_count"
) != 211:
    stop("CONTRACT_SUPPORTED_COUNT_INVALID")

if pair.get(
    "unresolved_binding_count"
) != 1642:
    stop("CONTRACT_UNRESOLVED_COUNT_INVALID")

if pair.get(
    "not_supported_binding_count"
) != 0:
    stop("CONTRACT_NOT_SUPPORTED_COUNT_INVALID")

if pair.get(
    "req06_req14_unresolved_pair_count"
) != 218:
    stop("CONTRACT_REQ06_REQ14_COUNT_INVALID")

if pair.get(
    "pair_reclassification_performed"
) is not False:
    stop("CONTRACT_PAIR_RECLASSIFICATION_INVALID")

decision = DEC.read_text(
    encoding="utf-8"
)

for marker in (
    "ACCOUNTING_SATISFACTION_EVIDENCE_STUDY_AUTHORIZED=YES",
    "ACCOUNTING_SATISFACTION_ESTABLISHED=NO",
    "CONCRETE_ACCOUNTING_INSTANCE_CREATED=NO",
    "PAIR_RECLASSIFICATION_PERFORMED=NO",
    "OPERATIONAL_MAPPING_AUTHORIZED=NO",
    "ANALYZER_AUTHORIZED=NO",
    "BASELINE_AUTHORIZED=NO",
    "REPAIR_AUTHORIZED=NO",
):
    if marker not in decision:
        stop(
            "DECISION0202_REQUIRED_MARKER_MISSING",
            marker
        )

print(
    "DECISION0202_ACCOUNTING_SATISFACTION_EVIDENCE_GAP_"
    "AND_ACQUISITION_STUDY_AUTHORIZATION_VERIFIER=PASS"
)

print(
    "AUTHORIZED_STUDY_TYPE="
    "BOUNDED_ACCOUNTING_SATISFACTION_EVIDENCE_GAP_"
    "AND_ACQUISITION_SPECIFICATION_STUDY"
)

print(
    "STUDY_STATUS=AUTHOR_CANDIDATE"
)

print(
    "TARGET_REQUIREMENT_COUNT=2"
)

print(
    "REQ06_GOVERNANCE_ROLE="
    + ROLE
)

print(
    "REQ14_GOVERNANCE_ROLE="
    + ROLE
)

print(
    "REQ06_ACCOUNTING_SATISFACTION_STATE="
    + SATISFACTION
)

print(
    "REQ14_ACCOUNTING_SATISFACTION_STATE="
    + SATISFACTION
)

print(
    "CURRENT_IMMUTABLE_EVIDENCE_STRUCTURALLY_SUFFICIENT_FOR_CONCRETE_ACCOUNTING_SATISFACTION_ASSESSMENT=NO"
)

print(
    "ACTUAL_ACCOUNTING_EVIDENCE_ACQUISITION_AUTHORIZED=NO"
)

print(
    "CONCRETE_ACCOUNTING_INSTANCE_AUTHORING_AUTHORIZED=NO"
)

print(
    "ACCOUNTING_SATISFACTION_DETERMINATION_AUTHORIZED=NO"
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
    "SCHEMA_V2_LOSSLESSNESS_PROVEN=NO"
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
