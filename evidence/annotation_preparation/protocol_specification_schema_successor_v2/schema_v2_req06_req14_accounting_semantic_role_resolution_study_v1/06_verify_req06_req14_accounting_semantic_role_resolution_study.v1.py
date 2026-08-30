#!/usr/bin/env python3

from pathlib import Path
from collections import Counter
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
REPO = ROOT.parents[2]

STUDY = HERE / "01_req06_req14_accounting_semantic_role_resolution_study.v1.json"
EVIDENCE = HERE / "02_req06_req14_accounting_role_evidence_anchor_matrix.v1.json"
CONSUMPTION = HERE / "03_decision0192_a02_consumption_record.v1.json"
OUTPUT = HERE / "04_decision0192_a02_execution_output.EXACT_COPY.v1.txt"
SENTINEL = HERE / "05_decision0192_a02_consumption_sentinel.EXACT_COPY.v1.json"

SUCCESSOR = ROOT / (
    "schema_v2_requirement_to_semantic_unit_bounded_"
    "supported_binding_promotion_successor_v1/"
    "01_bounded_supported_binding_successor_matrix.v1.json"
)

SCHEMA = REPO / "config/schemas/protocol_specification.v2.schema.json"
DESIGN = ROOT / "04_schema_v2_successor_design_record.v1.json"
RESIDUAL = ROOT / (
    "schema_v2_residual_losslessness_insufficiency_review_package_v2/"
    "03_residual_insufficiency_proof_v1.EXACT_COPY.json"
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
}


def stop(code, detail=""):
    print(
        "STOP|" + code
        + (("|" + detail) if detail else "")
    )
    raise SystemExit(1)


for path in (
    STUDY,
    EVIDENCE,
    CONSUMPTION,
    OUTPUT,
    SENTINEL,
    *EXPECTED.keys(),
):
    if not path.is_file():
        stop("REQUIRED_ARTIFACT_MISSING", str(path))

for path, expected_sha in EXPECTED.items():
    actual = hashlib.sha256(path.read_bytes()).hexdigest()

    if actual != expected_sha:
        stop("BOUND_ARTIFACT_SHA_MISMATCH", str(path))

study = json.loads(STUDY.read_text(encoding="utf-8"))
evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))
consumption = json.loads(CONSUMPTION.read_text(encoding="utf-8"))
successor = json.loads(SUCCESSOR.read_text(encoding="utf-8"))
schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
design = json.loads(DESIGN.read_text(encoding="utf-8"))
residual = json.loads(RESIDUAL.read_text(encoding="utf-8"))
sentinel = json.loads(SENTINEL.read_text(encoding="utf-8"))

if study.get("status") != "AUTHOR_CANDIDATE":
    stop("STUDY_STATUS_INVALID")

if study.get("authorization_decision") != "0192":
    stop("STUDY_AUTHORIZATION_BINDING_INVALID")

if study.get("target_requirement_count") != 2:
    stop("TARGET_REQUIREMENT_COUNT_INVALID")

if study.get("target_pair_count") != 218:
    stop("TARGET_PAIR_COUNT_INVALID")

results = study.get("results")

if not isinstance(results, list) or len(results) != 2:
    stop("ROLE_RESULT_COUNT_INVALID")

expected_targets = [
    ("forward_accounting_required", 6),
    ("reverse_accounting_required", 14),
]

if [
    (
        x.get("requirement_id"),
        x.get("requirement_ordinal")
    )
    for x in results
] != expected_targets:
    stop("ROLE_RESULT_TARGETS_INVALID")

for result in results:
    if result.get("author_candidate_role") != (
        "CROSS_CUTTING_ACCOUNTING_COMPLETENESS_CONSTRAINT"
    ):
        stop(
            "AUTHOR_CANDIDATE_ROLE_INVALID",
            result.get("requirement_id", "")
        )

    if result.get("accounting_satisfaction_state") != (
        "FURTHER_ACCOUNTING_SATISFACTION_EVIDENCE_REQUIRED"
    ):
        stop(
            "ACCOUNTING_SATISFACTION_STATE_INVALID",
            result.get("requirement_id", "")
        )

    pair_state = result.get("current_pair_state", {})

    if pair_state != {
        "supported_binding_count": 0,
        "unresolved_binding_count": 109,
        "not_supported_binding_count": 0
    }:
        stop(
            "TARGET_PAIR_STATE_INVALID",
            result.get("requirement_id", "")
        )

    for key in (
        "pair_reclassification_performed",
        "supported_binding_created",
        "not_supported_binding_created",
        "accounting_satisfaction_established",
        "operational_mapping_created",
        "schema_v2_losslessness_proven",
        "schema_mapping_inferred",
        "analyzer_authorized",
        "baseline_authorized",
        "repair_authorized",
    ):
        if result.get(key) is not False:
            stop(
                "STUDY_RESULT_BOUNDARY_INVALID",
                result.get("requirement_id", "")
                + ":"
                + key
            )

global_result = study.get(
    "global_author_candidate_result",
    {}
)

if global_result.get("req06_role") != (
    "CROSS_CUTTING_ACCOUNTING_COMPLETENESS_CONSTRAINT"
):
    stop("GLOBAL_REQ06_ROLE_INVALID")

if global_result.get("req14_role") != (
    "CROSS_CUTTING_ACCOUNTING_COMPLETENESS_CONSTRAINT"
):
    stop("GLOBAL_REQ14_ROLE_INVALID")

if global_result.get(
    "pair_promotion_needed_to_express_role"
) is not False:
    stop("PAIR_PROMOTION_ROLE_FLAG_INVALID")

if global_result.get(
    "req06_req14_pair_records_remain_unresolved"
) is not True:
    stop("TARGET_PAIR_UNRESOLVED_FLAG_INVALID")

if global_result.get(
    "accounting_satisfaction_established"
) is not False:
    stop("GLOBAL_ACCOUNTING_SATISFACTION_INVALID")

if global_result.get(
    "independent_human_review_required"
) is not True:
    stop("HUMAN_REVIEW_REQUIREMENT_MISSING")

if global_result.get("governance_adopted") is not False:
    stop("STUDY_PREMATURELY_GOVERNANCE_ADOPTED")

pairs = successor.get("pairs")

if Counter(
    r.get("classification")
    for r in pairs
) != Counter({
    "SUPPORTED_BINDING": 211,
    "UNRESOLVED_BINDING": 1642
}):
    stop("SUCCESSOR_PAIR_DISTRIBUTION_CHANGED")

for req in (
    "forward_accounting_required",
    "reverse_accounting_required",
):
    rows = [
        r
        for r in pairs
        if r.get("requirement_id") == req
    ]

    if len(rows) != 109:
        stop("TARGET_PAIR_COUNT_CHANGED", req)

    if any(
        r.get("classification") != "UNRESOLVED_BINDING"
        for r in rows
    ):
        stop("TARGET_PAIR_RECLASSIFIED", req)

sa = schema["properties"]["semantic_accounting"]

if sa["properties"]["forward_complete"].get("const") is not True:
    stop("FORWARD_COMPLETE_CHANGED")

if sa["properties"]["reverse_complete"].get("const") is not True:
    stop("REVERSE_COMPLETE_CHANGED")

carriers = design["required_sensitive_semantics_carriers"]

if carriers.get("forward_accounting") != (
    "/semantic_accounting/forward_accounting"
):
    stop("FORWARD_CARRIER_CHANGED")

if carriers.get("reverse_accounting") != (
    "/semantic_accounting/reverse_accounting"
):
    stop("REVERSE_CARRIER_CHANGED")

boundary = residual["semantic_accounting_boundary"]

if boundary.get("accounting_alone_proves_semantic_encoding") is not False:
    stop("ACCOUNTING_ENCODING_NONCLAIM_CHANGED")

if consumption.get("execution_count") != 1:
    stop("D0192_A02_EXECUTION_COUNT_INVALID")

if consumption.get("execution_result") != "PASS":
    stop("D0192_A02_RESULT_INVALID")

if consumption.get("lifecycle_state") != "PERMANENTLY_RETIRED":
    stop("D0192_A02_NOT_RETIRED")

if consumption.get("rerun_authorized") is not False:
    stop("D0192_A02_RERUN_BOUNDARY_INVALID")

if consumption.get("verifier_sha256") != (
    "318989e9cf4c70bc2145f7e3c2718250abd429b4f7ea64ad473ce32510216a94"
):
    stop("D0192_A02_SHA_BINDING_INVALID")

output_raw = OUTPUT.read_bytes()

if hashlib.sha256(output_raw).hexdigest() != consumption.get(
    "execution_output_sha256"
):
    stop("D0192_A02_OUTPUT_BINDING_INVALID")

output_text = output_raw.decode("utf-8")

for marker in (
    "DECISION0192_ROLE_STUDY_AUTHORIZATION_VERIFIER=PASS",
    "TARGET_REQUIREMENT_COUNT=2",
    "TARGET_UNRESOLVED_PAIR_COUNT=218",
    "ROLE_RESOLUTION_STUDY_AUTHORIZED=YES",
    "AUTHORIZATION_EXECUTION_COUNT_FOR_THIS_RUN=1",
    "AUTHORIZATION_RERUN_AUTHORIZED=NO",
):
    if marker not in output_text:
        stop("D0192_A02_OUTPUT_MARKER_MISSING", marker)

sentinel_raw = SENTINEL.read_bytes()

if hashlib.sha256(sentinel_raw).hexdigest() != consumption.get(
    "consumption_sentinel_sha256"
):
    stop("D0192_A02_SENTINEL_BINDING_INVALID")

if sentinel.get("rerun_authorized") is not False:
    stop("D0192_A02_SENTINEL_RERUN_INVALID")

if evidence.get("status") != "AUTHOR_CANDIDATE_SUPPORTING_EVIDENCE":
    stop("EVIDENCE_MATRIX_STATUS_INVALID")

if evidence.get(
    "interpretation_boundary", {}
).get("anchors_authorize_pair_reclassification") is not False:
    stop("EVIDENCE_MATRIX_PAIR_BOUNDARY_INVALID")

if evidence.get(
    "interpretation_boundary", {}
).get("anchors_prove_accounting_satisfaction") is not False:
    stop("EVIDENCE_MATRIX_SATISFACTION_BOUNDARY_INVALID")

print("REQ06_REQ14_ACCOUNTING_SEMANTIC_ROLE_STUDY_VERIFIER=PASS")
print("STUDY_STATUS=AUTHOR_CANDIDATE")
print("TARGET_REQUIREMENT_COUNT=2")
print("REQ06_AUTHOR_CANDIDATE_ROLE=CROSS_CUTTING_ACCOUNTING_COMPLETENESS_CONSTRAINT")
print("REQ14_AUTHOR_CANDIDATE_ROLE=CROSS_CUTTING_ACCOUNTING_COMPLETENESS_CONSTRAINT")
print("REQ06_ACCOUNTING_SATISFACTION=FURTHER_ACCOUNTING_SATISFACTION_EVIDENCE_REQUIRED")
print("REQ14_ACCOUNTING_SATISFACTION=FURTHER_ACCOUNTING_SATISFACTION_EVIDENCE_REQUIRED")
print("TARGET_PAIR_RECORDS_RECLASSIFIED=0")
print("SUPPORTED_BINDING_CREATED=NO")
print("NOT_SUPPORTED_BINDING_CREATED=NO")
print("ACCOUNTING_SATISFACTION_ESTABLISHED=NO")
print("OPERATIONAL_MAPPING_CREATED=NO")
print("SCHEMA_V2_LOSSLESSNESS_PROVEN=NO")
print("INDEPENDENT_HUMAN_REVIEW_REQUIRED=YES")
print("GOVERNANCE_ADOPTED=NO")
print("DECISION0192_A02_EXECUTION_COUNT=1")
print("DECISION0192_A02_RESULT=PASS")
print("DECISION0192_A02_STATE=PERMANENTLY_RETIRED")
print("DECISION0192_A02_RERUN_AUTHORIZED=NO")
print("DECISION0190_P03_RERUN=NO")
print("DECISION0187_A02_RERUN=NO")
print("D0188_CRLF_SAFE_SUCCESSOR_RERUN=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
