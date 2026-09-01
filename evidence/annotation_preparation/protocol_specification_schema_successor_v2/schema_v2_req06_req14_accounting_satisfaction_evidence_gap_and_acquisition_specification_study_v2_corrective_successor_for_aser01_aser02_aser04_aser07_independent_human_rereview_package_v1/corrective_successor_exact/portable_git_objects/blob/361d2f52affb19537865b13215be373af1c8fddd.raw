#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

S01 = HERE / "01_accounting_satisfaction_evidence_gap_assessment.v1.json"
S02 = HERE / "02_future_accounting_evidence_acquisition_specification.v1.json"
S03 = HERE / "03_machine_checkable_accounting_satisfaction_criteria.v1.json"
S04 = HERE / "04_study_source_binding.v1.json"
S05 = HERE / "05_decision0202_a02_consumption_record.v1.json"
S06 = HERE / "06_decision0202_a02_execution_output.EXACT_COPY.v1.txt"
S07 = HERE / "07_decision0202_a02_consumption_sentinel.EXACT_COPY.v1.json"
S08 = HERE / "08_study_boundary.v1.md"

SCHEMA = Path("config/schemas/protocol_specification.v2.schema.json")

CARRIER_ASSESS = ROOT / (
    "schema_v2_requirement_bound_carrier_admissibility_resolution_study_v1/"
    "01_requirement_bound_carrier_admissibility_assessment.v1.json"
)

CARRIER_ADOPTION = ROOT / (
    "schema_v2_requirement_bound_carrier_admissibility_resolution_study_v1_"
    "bounded_governance_adoption_v1/01_bounded_governance_adoption_manifest.v1.json"
)

CAPABILITY = ROOT / (
    "schema_v2_exhaustive_admissible_multifield_capability_study_v1/"
    "01_exhaustive_admissible_existing_schema_v2_multifield_capability_study.v1.json"
)

RELATION = ROOT / (
    "schema_v2_relation_informed_exhaustive_admissible_composition_study_v1/"
    "02_exhaustiveness_accounting.v1.json"
)

DESIGN = ROOT / "04_schema_v2_successor_design_record.v1.json"

RESIDUAL = ROOT / (
    "schema_v2_residual_losslessness_insufficiency_proof_v1/"
    "01_residual_schema_v2_losslessness_insufficiency_proof.v1.json"
)

EXPECTED_SOURCE_SHA = {
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

A02_SHA = (
    "1a2c253e07ed9416f700c906872d10f99a4a2b19f05307ed6c4bc09301681581"
)

ROLE = "CROSS_CUTTING_ACCOUNTING_COMPLETENESS_CONSTRAINT"
SAT = "FURTHER_ACCOUNTING_SATISFACTION_EVIDENCE_REQUIRED"


def stop(code, detail=""):
    print("STOP|" + code + (("|" + detail) if detail else ""))
    raise SystemExit(1)


for path in (
    S01, S02, S03, S04, S05, S06, S07, S08,
    *EXPECTED_SOURCE_SHA.keys()
):
    if not path.is_file():
        stop("REQUIRED_ARTIFACT_MISSING", str(path))

for path, expected in EXPECTED_SOURCE_SHA.items():
    actual = hashlib.sha256(path.read_bytes()).hexdigest()

    if actual != expected:
        stop("IMMUTABLE_SOURCE_SHA_MISMATCH", str(path))

gap = json.loads(S01.read_text(encoding="utf-8"))
acq = json.loads(S02.read_text(encoding="utf-8"))
criteria = json.loads(S03.read_text(encoding="utf-8"))
binding = json.loads(S04.read_text(encoding="utf-8"))
consumption = json.loads(S05.read_text(encoding="utf-8"))
sentinel = json.loads(S07.read_text(encoding="utf-8"))

if gap.get("status") != "AUTHOR_CANDIDATE":
    stop("STUDY_STATUS_INVALID")

if gap.get("study_result") != (
    "EVIDENCE_GAP_CONFIRMED_ACQUISITION_SPECIFICATION_READY"
):
    stop("STUDY_RESULT_INVALID")

scope = gap.get("governed_requirement_scope", {})

for req, key in (
    ("Req06", "forward_accounting_required"),
    ("Req14", "reverse_accounting_required"),
):
    entry = scope.get(req, {})

    if entry.get("requirement_key") != key:
        stop("REQUIREMENT_KEY_INVALID", req)

    if entry.get("governance_role") != ROLE:
        stop("GOVERNANCE_ROLE_INVALID", req)

    if entry.get("accounting_satisfaction_state") != SAT:
        stop("SATISFACTION_STATE_INVALID", req)

fixed = gap.get("fixed_findings", {})

required_fixed = {
    "active_schema_structurally_supports_forward_accounting": True,
    "active_schema_structurally_supports_reverse_accounting": True,
    "active_schema_requires_forward_complete_true": True,
    "active_schema_requires_reverse_complete_true": True,
    "schema_completeness_flags_are_not_independent_satisfaction_evidence": True,
    "bound_relation_evidence_contains_concrete_accounting_instance": False,
    "constructive_full_exact_mapping_witness_complete": False,
    "deterministic_complete_forward_encoding_proven": False,
    "deterministic_exact_reverse_reconstruction_proven": False,
    "accounting_alone_proves_semantic_encoding": False,
    "current_immutable_evidence_structurally_sufficient_for_concrete_accounting_satisfaction_assessment": False,
}

for key, expected in required_fixed.items():
    if fixed.get(key) != expected:
        stop("FIXED_FINDING_INVALID", key)

questions = gap.get("gap_questions", [])

if [q.get("id") for q in questions] != [
    "ASG01", "ASG02", "ASG03", "ASG04",
    "ASG05", "ASG06", "ASG07", "ASG08",
]:
    stop("GAP_QUESTION_SEQUENCE_INVALID")

summary = gap.get("gap_summary", {})

if summary.get("question_count") != 8:
    stop("GAP_QUESTION_COUNT_INVALID")

if summary.get("evidence_gap_confirmed") is not True:
    stop("EVIDENCE_GAP_CONFIRMATION_INVALID")

if summary.get(
    "future_acquisition_specification_can_be_defined_without_creating_actual_accounting_evidence"
) is not True:
    stop("ACQUISITION_SPECIFICATION_READINESS_INVALID")

if summary.get("accounting_satisfaction_currently_determinable") is not False:
    stop("CURRENT_SATISFACTION_DETERMINABILITY_INVALID")

nonresults = gap.get("current_nonresults", {})

for key in (
    "forward_accounting_satisfied",
    "reverse_accounting_satisfied",
    "accounting_satisfaction_established",
    "concrete_accounting_instance_created",
    "source_unit_to_schema_carrier_mapping_created",
    "pair_reclassification_performed",
    "schema_v2_losslessness_proven",
    "operational_mapping_completed",
):
    if nonresults.get(key) is not False:
        stop("CURRENT_NONRESULT_INVALID", key)

pair = gap.get("pair_state", {})

if pair.get("supported_binding_count") != 211:
    stop("SUPPORTED_BINDING_COUNT_INVALID")

if pair.get("unresolved_binding_count") != 1642:
    stop("UNRESOLVED_BINDING_COUNT_INVALID")

if pair.get("not_supported_binding_count") != 0:
    stop("NOT_SUPPORTED_BINDING_COUNT_INVALID")

if pair.get("req06_req14_unresolved_pair_count") != 218:
    stop("REQ06_REQ14_UNRESOLVED_PAIR_COUNT_INVALID")

review = gap.get("review_state", {})

if review.get("independent_human_review_required") is not True:
    stop("INDEPENDENT_REVIEW_REQUIREMENT_INVALID")

if review.get("independent_human_review_completed") is not False:
    stop("INDEPENDENT_REVIEW_COMPLETION_INVALID")

if review.get("governance_adopted") is not False:
    stop("STUDY_GOVERNANCE_STATE_INVALID")

if acq.get("status") != "AUTHOR_CANDIDATE_SPECIFICATION_ONLY":
    stop("ACQUISITION_SPEC_STATUS_INVALID")

for key in (
    "actual_acquisition_authorized",
    "actual_acquisition_performed",
    "concrete_accounting_instance_created",
):
    if acq.get(key) is not False:
        stop("ACQUISITION_BOUNDARY_INVALID", key)

artifacts = acq.get("required_future_evidence_artifacts", [])

if [x.get("id") for x in artifacts] != [
    "AEA01", "AEA02", "AEA03", "AEA04", "AEA05"
]:
    stop("ACQUISITION_ARTIFACT_SEQUENCE_INVALID")

for item in artifacts:
    if item.get("current_status") != "REQUIRED_NOT_ACQUIRED":
        stop("ACQUISITION_ARTIFACT_CURRENT_STATUS_INVALID", item.get("id", ""))

placeholders = acq.get("current_placeholders", {})

for value in placeholders.values():
    if value != "NOT_ACQUIRED":
        stop("ACQUISITION_PLACEHOLDER_INVALID")

if criteria.get("status") != "AUTHOR_CANDIDATE_CRITERIA_NOT_EVALUATED":
    stop("CRITERIA_STATUS_INVALID")

current_result = criteria.get("current_result", {})

if current_result.get("criteria_defined") is not True:
    stop("CRITERIA_DEFINED_STATE_INVALID")

if current_result.get("criteria_evaluated") is not False:
    stop("CRITERIA_EVALUATION_STATE_INVALID")

for key in (
    "forward_accounting_satisfied",
    "reverse_accounting_satisfied",
    "accounting_satisfaction_established",
):
    if current_result.get(key) is not False:
        stop("CRITERIA_CURRENT_RESULT_INVALID", key)

lossless = criteria.get("losslessness_boundary", {})

if lossless.get("accounting_satisfaction_implies_schema_v2_losslessness") is not False:
    stop("LOSSLESSNESS_BOUNDARY_INVALID")

if lossless.get(
    "accounting_satisfaction_implies_exact_semantic_reconstruction"
) is not False:
    stop("SEMANTIC_RECONSTRUCTION_BOUNDARY_INVALID")

if lossless.get("separate_semantic_losslessness_evidence_required") is not True:
    stop("SEPARATE_LOSSLESSNESS_EVIDENCE_BOUNDARY_INVALID")

if binding.get(
    "decision0202_authorization", {}
).get("a02_sha256") != A02_SHA:
    stop("SOURCE_BINDING_A02_SHA_INVALID")

if consumption.get("verifier_sha256") != A02_SHA:
    stop("A02_CONSUMPTION_VERIFIER_SHA_INVALID")

if consumption.get("execution_count") != 1:
    stop("A02_EXECUTION_COUNT_INVALID")

if consumption.get("execution_result") != "PASS":
    stop("A02_RESULT_INVALID")

if consumption.get("lifecycle_state") != "PERMANENTLY_RETIRED":
    stop("A02_RETIREMENT_INVALID")

if consumption.get("rerun_authorized") is not False:
    stop("A02_RERUN_BOUNDARY_INVALID")

output_raw = S06.read_bytes()

if hashlib.sha256(output_raw).hexdigest() != consumption.get(
    "execution_output_sha256"
):
    stop("A02_OUTPUT_BINDING_INVALID")

for marker in (
    "DECISION0202_ACCOUNTING_SATISFACTION_EVIDENCE_GAP_AND_ACQUISITION_STUDY_AUTHORIZATION_VERIFIER=PASS",
    "ACTUAL_ACCOUNTING_EVIDENCE_ACQUISITION_AUTHORIZED=NO",
    "CONCRETE_ACCOUNTING_INSTANCE_AUTHORING_AUTHORIZED=NO",
    "ACCOUNTING_SATISFACTION_DETERMINATION_AUTHORIZED=NO",
    "PAIR_RECLASSIFICATION_PERFORMED=NO",
    "AUTHORIZATION_EXECUTION_COUNT_FOR_THIS_RUN=1",
    "AUTHORIZATION_RERUN_AUTHORIZED=NO",
):
    if marker not in output_raw.decode("utf-8"):
        stop("A02_OUTPUT_REQUIRED_MARKER_MISSING", marker)

sentinel_raw = S07.read_bytes()

if hashlib.sha256(sentinel_raw).hexdigest() != consumption.get(
    "consumption_sentinel_sha256"
):
    stop("A02_SENTINEL_BINDING_INVALID")

if sentinel.get("verifier_sha256") != A02_SHA:
    stop("A02_SENTINEL_VERIFIER_SHA_INVALID")

if sentinel.get("rerun_authorized") is not False:
    stop("A02_SENTINEL_RERUN_BOUNDARY_INVALID")

boundary = S08.read_text(encoding="utf-8")

for phrase in (
    "AUTHOR_CANDIDATE",
    "EVIDENCE_GAP_CONFIRMED_ACQUISITION_SPECIFICATION_READY",
    "No concrete source-unit-to-schema-carrier mapping is created",
    "No actual accounting-evidence acquisition is performed",
    "No requirement-to-semantic-unit pair is modified or reclassified",
    "Schema-V2 losslessness remains unproven",
    "requires independent human review",
):
    if phrase not in boundary:
        stop("STUDY_BOUNDARY_REQUIRED_PHRASE_MISSING", phrase)

print(
    "REQ06_REQ14_ACCOUNTING_SATISFACTION_EVIDENCE_GAP_AND_"
    "ACQUISITION_SPECIFICATION_STUDY_VERIFIER=PASS"
)

print("STUDY_STATUS=AUTHOR_CANDIDATE")

print(
    "STUDY_RESULT="
    "EVIDENCE_GAP_CONFIRMED_ACQUISITION_SPECIFICATION_READY"
)

print("GAP_QUESTION_COUNT=8")
print("FUTURE_REQUIRED_EVIDENCE_ARTIFACT_COUNT=5")
print("MACHINE_CHECKABLE_SATISFACTION_CRITERIA_DEFINED=YES")
print("MACHINE_CHECKABLE_SATISFACTION_CRITERIA_EVALUATED=NO")

print("REQ06_GOVERNANCE_ROLE=" + ROLE)
print("REQ14_GOVERNANCE_ROLE=" + ROLE)

print("REQ06_ACCOUNTING_SATISFACTION_STATE=" + SAT)
print("REQ14_ACCOUNTING_SATISFACTION_STATE=" + SAT)

print("ACTUAL_ACCOUNTING_EVIDENCE_ACQUISITION_AUTHORIZED=NO")
print("ACTUAL_ACCOUNTING_EVIDENCE_ACQUISITION_PERFORMED=NO")
print("CONCRETE_ACCOUNTING_INSTANCE_CREATED=NO")
print("SOURCE_UNIT_TO_SCHEMA_CARRIER_MAPPING_CREATED=NO")

print("FORWARD_ACCOUNTING_SATISFIED=NO")
print("REVERSE_ACCOUNTING_SATISFIED=NO")
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

print("INDEPENDENT_HUMAN_REVIEW_REQUIRED=YES")
print("INDEPENDENT_HUMAN_REVIEW_COMPLETED=NO")
print("STUDY_GOVERNANCE_ADOPTED=NO")

print("DECISION0202_A02_EXECUTION_COUNT=1")
print("DECISION0202_A02_RESULT=PASS")
print("DECISION0202_A02_STATE=PERMANENTLY_RETIRED")
print("DECISION0202_A02_RERUN_AUTHORIZED=NO")
