#!/usr/bin/env python3

from pathlib import Path
from collections import Counter
import hashlib
import json
import subprocess

D0191_COMMIT = "119df8756fdb483d969b5a1b6b8ab2c7bba2d165"

ROOT = Path(
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2"
)

AUTH = ROOT / (
    "schema_v2_req06_req14_accounting_"
    "semantic_role_resolution_study_v1_authorization"
)

A01 = AUTH / "01_accounting_semantic_role_resolution_study_authorization.v1.json"
A02 = AUTH / "02_authorize_accounting_semantic_role_resolution_study_once.v1.py"
A03 = AUTH / "03_accounting_semantic_role_resolution_study_contract.v1.json"
A04 = AUTH / "04_accounting_semantic_role_resolution_authorization_boundary.v1.md"

DEC = Path(
    "documentation/decisions/"
    "0192-authorize-req06-req14-accounting-semantic-role-resolution-study-v1.md"
)

SUCCESSOR = ROOT / (
    "schema_v2_requirement_to_semantic_unit_bounded_"
    "supported_binding_promotion_successor_v1/"
    "01_bounded_supported_binding_successor_matrix.v1.json"
)

SCHEMA = Path("config/schemas/protocol_specification.v2.schema.json")

DESIGN = ROOT / "04_schema_v2_successor_design_record.v1.json"

RESIDUAL = ROOT / (
    "schema_v2_residual_losslessness_insufficiency_review_package_v2/"
    "03_residual_insufficiency_proof_v1.EXACT_COPY.json"
)

CARRIER = ROOT / (
    "schema_v2_requirement_bound_carrier_admissibility_"
    "resolution_study_v1/"
    "01_requirement_bound_carrier_admissibility_assessment.v1.json"
)

ADOPTION = ROOT / (
    "schema_v2_requirement_bound_carrier_admissibility_"
    "resolution_study_v1_bounded_governance_adoption_v1/"
    "01_bounded_governance_adoption_manifest.v1.json"
)

EXPECTED = {
    SUCCESSOR:
        "c74240135454c6746b0829306d60c5a818c67d06a4148116de0f21891669a940",
    SCHEMA:
        "c6ebb5ef2214c4168283f9009d1f7ce6e88d2ff928853fe6a57ed1f7521c6956",
    DESIGN:
        "eb0367a18ca2474084a90b0aaf44b769b2ac2855f270b0d94814b35590749e90",
    RESIDUAL:
        "400f6806217f50b79d17ec77e41683d9077f64e07c63e5421c8b1922b49aaff0",
    CARRIER:
        "2c9ca9125aa89dd77f7f74950f7285657fcaee7dbd17ce0dca01012ad716263c",
    ADOPTION:
        "d133548d4c3b7eef2436faabece406b3bfb815bab12c0a5c119c84258e84169a",
}

EXPECTED_D0192_PATHS = {
    str(A01),
    str(A02),
    str(A03),
    str(A04),
    str(DEC),
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


if git("rev-parse", "HEAD^") != D0191_COMMIT:
    stop("D0192_PARENT_NOT_D0191")

if subprocess.check_output(
    ["git", "status", "--porcelain=v1", "--untracked-files=all"],
    text=True
).strip():
    stop("REPOSITORY_NOT_CLEAN_BEFORE_D0192_SUCCESSOR")

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

if changed != EXPECTED_D0192_PATHS:
    stop(
        "D0192_COMMIT_SCOPE_MISMATCH",
        ",".join(sorted(changed))
    )

for path, expected_sha in EXPECTED.items():
    if not path.is_file():
        stop("BOUND_INPUT_MISSING", str(path))

    actual = hashlib.sha256(path.read_bytes()).hexdigest()

    if actual != expected_sha:
        stop("BOUND_INPUT_SHA_MISMATCH", str(path))

for path in (A01, A02, A03, A04, DEC):
    if not path.is_file():
        stop("D0192_ARTIFACT_MISSING", str(path))

manifest = json.loads(A01.read_text(encoding="utf-8"))
contract = json.loads(A03.read_text(encoding="utf-8"))

if manifest.get("decision") != "0192":
    stop("AUTHORIZATION_DECISION_INVALID")

if manifest.get("status") != (
    "AUTHORIZED_TO_AUTHOR_REQ06_REQ14_"
    "ACCOUNTING_SEMANTIC_ROLE_RESOLUTION_STUDY_V1_ONLY"
):
    stop("AUTHORIZATION_STATUS_INVALID")

activity = manifest.get("authorized_activity", {})

if activity.get("author_semantic_role_resolution_study_v1") is not True:
    stop("ROLE_STUDY_AUTHORING_NOT_AUTHORIZED")

for key in (
    "classify_role_in_decision0192",
    "perform_pair_reclassification",
    "create_supported_binding",
    "create_not_supported_binding",
    "claim_accounting_satisfaction",
    "create_operational_mapping",
    "modify_schema_v2",
    "authorize_schema_successor",
    "authorize_curl_json",
    "authorize_analyzer_implementation",
    "authorize_analyzer_execution",
    "authorize_baseline_execution",
    "authorize_repair",
):
    if activity.get(key) is not False:
        stop("D0192_BOUNDARY_INVALID", key)

targets = manifest.get("target_requirements", [])

if [
    (
        x.get("requirement_id"),
        x.get("requirement_ordinal"),
        x.get("current_supported_binding_count"),
        x.get("current_unresolved_binding_count"),
    )
    for x in targets
] != [
    ("forward_accounting_required", 6, 0, 109),
    ("reverse_accounting_required", 14, 0, 109),
]:
    stop("TARGET_REQUIREMENT_CONTRACT_INVALID")

allowed_roles = contract.get(
    "allowed_author_candidate_role_states"
)

if allowed_roles != [
    "CROSS_CUTTING_ACCOUNTING_COMPLETENESS_CONSTRAINT",
    "UNIT_BINDABLE_SUBSTANTIVE_REQUIREMENT",
    "ROLE_UNRESOLVED",
]:
    stop("ROLE_STATE_VOCABULARY_INVALID")

if contract.get(
    "critical_distinction", {}
).get("role_resolution_is_not_pair_promotion") is not True:
    stop("ROLE_PAIR_PROMOTION_DISTINCTION_MISSING")

if contract.get(
    "critical_distinction", {}
).get("role_resolution_is_not_accounting_satisfaction") is not True:
    stop("ROLE_SATISFACTION_DISTINCTION_MISSING")

successor = json.loads(
    SUCCESSOR.read_text(encoding="utf-8")
)

pairs = successor["pairs"]

if Counter(
    r["classification"]
    for r in pairs
) != Counter({
    "SUPPORTED_BINDING": 211,
    "UNRESOLVED_BINDING": 1642
}):
    stop("D0191_SUCCESSOR_DISTRIBUTION_CHANGED")

for req in (
    "forward_accounting_required",
    "reverse_accounting_required",
):
    rows = [
        r
        for r in pairs
        if r["requirement_id"] == req
    ]

    if len(rows) != 109:
        stop("TARGET_PAIR_COUNT_CHANGED", req)

    if any(
        r["classification"] != "UNRESOLVED_BINDING"
        for r in rows
    ):
        stop("TARGET_PAIR_RECLASSIFIED_BEFORE_ROLE_STUDY", req)

schema = json.loads(
    SCHEMA.read_text(encoding="utf-8")
)

sa = schema["properties"]["semantic_accounting"]

if not {
    "inventory",
    "forward_complete",
    "reverse_complete",
    "forward_accounting",
    "reverse_accounting",
}.issubset(set(sa["required"])):
    stop("SCHEMA_ACCOUNTING_REQUIRED_CONTRACT_CHANGED")

if sa["properties"]["forward_complete"].get("const") is not True:
    stop("SCHEMA_FORWARD_COMPLETE_CHANGED")

if sa["properties"]["reverse_complete"].get("const") is not True:
    stop("SCHEMA_REVERSE_COMPLETE_CHANGED")

design = json.loads(
    DESIGN.read_text(encoding="utf-8")
)

carriers = design["required_sensitive_semantics_carriers"]

if carriers.get("forward_accounting") != (
    "/semantic_accounting/forward_accounting"
):
    stop("FORWARD_ACCOUNTING_CARRIER_CHANGED")

if carriers.get("reverse_accounting") != (
    "/semantic_accounting/reverse_accounting"
):
    stop("REVERSE_ACCOUNTING_CARRIER_CHANGED")

residual = json.loads(
    RESIDUAL.read_text(encoding="utf-8")
)

boundary = residual["semantic_accounting_boundary"]

if boundary.get("forward_accounting_supported_by_schema") is not True:
    stop("FORWARD_ACCOUNTING_SCHEMA_SUPPORT_CHANGED")

if boundary.get("reverse_accounting_supported_by_schema") is not True:
    stop("REVERSE_ACCOUNTING_SCHEMA_SUPPORT_CHANGED")

if boundary.get("accounting_alone_proves_semantic_encoding") is not False:
    stop("ACCOUNTING_SEMANTIC_ENCODING_NONCLAIM_CHANGED")

adoption = json.loads(
    ADOPTION.read_text(encoding="utf-8")
)

if adoption["adopted_bounded_result"]["governance_result"] != (
    "FURTHER_EVIDENCE_REQUIRED"
):
    stop("HISTORICAL_ADOPTION_RESULT_CHANGED")

decision = DEC.read_text(encoding="utf-8")

for marker in (
    "ROLE_RESOLUTION_STUDY_AUTHORIZED=YES",
    "ROLE_CLASSIFICATION_PERFORMED=NO",
    "PAIR_RECLASSIFICATION_PERFORMED=NO",
    "SUPPORTED_BINDING_CREATED=NO",
    "NOT_SUPPORTED_BINDING_CREATED=NO",
    "ACCOUNTING_SATISFACTION_ESTABLISHED=NO",
    "OPERATIONAL_MAPPING_AUTHORIZED=NO",
    "ANALYZER_AUTHORIZED=NO",
    "BASELINE_AUTHORIZED=NO",
    "REPAIR_AUTHORIZED=NO",
):
    if marker not in decision:
        stop("DECISION0192_MARKER_MISSING", marker)

print("DECISION0192_ROLE_STUDY_AUTHORIZATION_VERIFIER=PASS")
print("TARGET_REQUIREMENT_COUNT=2")
print("TARGET_UNRESOLVED_PAIR_COUNT=218")
print("SEPARATE_FORWARD_ACCOUNTING_CARRIER_PRESENT=YES")
print("SEPARATE_REVERSE_ACCOUNTING_CARRIER_PRESENT=YES")
print("ACCOUNTING_ALONE_PROVES_SEMANTIC_ENCODING=NO")
print("ROLE_RESOLUTION_STUDY_AUTHORIZED=YES")
print("ROLE_CLASSIFICATION_PERFORMED_BY_THIS_VERIFIER=NO")
print("PAIR_RECLASSIFICATION_PERFORMED_BY_THIS_VERIFIER=NO")
print("SUPPORTED_BINDING_CREATED_BY_THIS_VERIFIER=NO")
print("ACCOUNTING_SATISFACTION_ESTABLISHED_BY_THIS_VERIFIER=NO")
print("AUTHORIZATION_EXECUTION_COUNT_FOR_THIS_RUN=1")
print("AUTHORIZATION_RERUN_AUTHORIZED=NO")
