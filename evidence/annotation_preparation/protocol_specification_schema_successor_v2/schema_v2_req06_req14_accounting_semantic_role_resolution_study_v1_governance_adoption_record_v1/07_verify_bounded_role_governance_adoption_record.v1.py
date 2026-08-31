#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent

G01 = HERE / (
    "01_bounded_role_governance_adoption_manifest.v1.json"
)

G02 = HERE / (
    "02_governance_adoption_source_binding.v1.json"
)

G03 = HERE / (
    "03_decision0200_a02_consumption_record.v1.json"
)

G04 = HERE / (
    "04_decision0200_a02_execution_output.EXACT_COPY.v1.txt"
)

G05 = HERE / (
    "05_decision0200_a02_consumption_sentinel.EXACT_COPY.v1.json"
)

G06 = HERE / (
    "06_bounded_role_governance_adoption_boundary.v1.md"
)

ROOT = HERE.parent

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

P04 = PACKAGE_DIR / (
    "04_independent_human_review_contract.EXACT_COPY.v1.json"
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

EXPECTED_SOURCE_SHA = {
    P02:
        "22c51d0d77f3faa086cb426788d057da15c5002a29b4ba68cd3177935aa80381",
    P03:
        "a153d0979f4bda119928fb29fd8043088115793f164e268c6d0def6fe1203601",
    P04:
        "1d71a5afb82d7ea7ad5fb882a904879409f0ace0b4c71b0201cf59ea82fd0ac1",
    R01:
        "a3a9f38ed79b3fa450d6799677b986b690a02f235ef21acf93cb5b75d2423309",
    R02:
        "1320dbec92e9ad18693802fe6f276185b279cc587b687d4ce5402d3a43a711c0",
}

D0200_A02_SHA = (
    "31010dc5901c886524588139755f1d2a45d6b1effe985e32265fbc9494f1afc0"
)

ROLE = (
    "CROSS_CUTTING_ACCOUNTING_COMPLETENESS_CONSTRAINT"
)

SATISFACTION = (
    "FURTHER_ACCOUNTING_SATISFACTION_EVIDENCE_REQUIRED"
)


def stop(code, detail=""):
    print(
        "STOP|" + code
        + (("|" + detail) if detail else "")
    )
    raise SystemExit(1)


for path in (
    G01,
    G02,
    G03,
    G04,
    G05,
    G06,
    P02,
    P03,
    P04,
    R01,
    R02,
):
    if not path.is_file():
        stop(
            "REQUIRED_ADOPTION_ARTIFACT_MISSING",
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

manifest = json.loads(
    G01.read_text(
        encoding="utf-8"
    )
)

binding = json.loads(
    G02.read_text(
        encoding="utf-8"
    )
)

consumption = json.loads(
    G03.read_text(
        encoding="utf-8"
    )
)

sentinel = json.loads(
    G05.read_text(
        encoding="utf-8"
    )
)

if manifest.get("status") != (
    "BOUNDED_ROLE_GOVERNANCE_ADOPTED_ACCOUNTING_SATISFACTION_EVIDENCE_STILL_REQUIRED"
):
    stop(
        "ADOPTION_STATUS_INVALID"
    )

scope = manifest.get(
    "adoption_scope",
    {}
)

if scope.get(
    "requirement_count"
) != 2:
    stop(
        "ADOPTION_REQUIREMENT_COUNT_INVALID"
    )

expected_req = {
    "Req06": "forward_accounting_required",
    "Req14": "reverse_accounting_required",
}

for req, key in expected_req.items():
    entry = scope.get(
        req,
        {}
    )

    if entry.get(
        "requirement_key"
    ) != key:
        stop(
            "ADOPTED_REQUIREMENT_KEY_INVALID",
            req
        )

    if entry.get(
        "governance_role"
    ) != ROLE:
        stop(
            "ADOPTED_ROLE_INVALID",
            req
        )

    if entry.get(
        "role_governance_adopted"
    ) is not True:
        stop(
            "ROLE_ADOPTION_STATE_INVALID",
            req
        )

    if entry.get(
        "accounting_satisfaction_state"
    ) != SATISFACTION:
        stop(
            "ACCOUNTING_SATISFACTION_STATE_INVALID",
            req
        )

review_basis = manifest.get(
    "review_basis",
    {}
)

if review_basis.get(
    "recorded_review_sha256"
) != EXPECTED_SOURCE_SHA[R01]:
    stop(
        "REVIEW_BASIS_SHA_INVALID"
    )

if review_basis.get(
    "pass_count"
) != 6:
    stop(
        "REVIEW_PASS_COUNT_INVALID"
    )

if review_basis.get(
    "revision_required_count"
) != 0:
    stop(
        "REVIEW_REVISION_COUNT_INVALID"
    )

if review_basis.get(
    "overall_review_decision"
) != "APPROVE_BOUNDED_ROLE_STUDY":
    stop(
        "REVIEW_OVERALL_DECISION_INVALID"
    )

if review_basis.get(
    "human_identity_independently_verified"
) is not False:
    stop(
        "IDENTITY_EPISTEMIC_BOUNDARY_INVALID"
    )

if review_basis.get(
    "human_authorship_beyond_returned_artifact_independently_proven"
) is not False:
    stop(
        "AUTHORSHIP_EPISTEMIC_BOUNDARY_INVALID"
    )

gov = manifest.get(
    "governance_state",
    {}
)

for key in (
    "bounded_role_study_review_governance_adopted",
    "role_governance_adopted",
    "req06_role_governance_adopted",
    "req14_role_governance_adopted",
):
    if gov.get(key) is not True:
        stop(
            "GOVERNANCE_ADOPTION_STATE_INVALID",
            key
        )

for key in (
    "accounting_satisfaction_established",
    "pair_reclassification_performed",
    "supported_binding_created",
    "not_supported_binding_created",
    "operational_mapping_authorized",
    "schema_v2_losslessness_proven",
    "schema_v2_modified",
    "schema_successor_authorized",
    "curl_json_authorized",
    "analyzer_authorized",
    "baseline_authorized",
    "repair_authorized",
):
    if gov.get(key) is not False:
        stop(
            "GOVERNANCE_NONEFFECT_INVALID",
            key
        )

if gov.get(
    "req06_accounting_satisfaction_state"
) != SATISFACTION:
    stop(
        "REQ06_SATISFACTION_STATE_INVALID"
    )

if gov.get(
    "req14_accounting_satisfaction_state"
) != SATISFACTION:
    stop(
        "REQ14_SATISFACTION_STATE_INVALID"
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

immutability = manifest.get(
    "immutability",
    {}
)

for key in (
    "author_candidate_study_modified",
    "recorded_human_review_modified",
    "requirement_to_semantic_unit_pair_matrix_modified",
):
    if immutability.get(key) is not False:
        stop(
            "IMMUTABILITY_STATE_INVALID",
            key
        )

d0200 = manifest.get(
    "decision0200_a02",
    {}
)

if d0200.get(
    "verifier_sha256"
) != D0200_A02_SHA:
    stop(
        "D0200_A02_SHA_INVALID"
    )

if d0200.get(
    "execution_count"
) != 1:
    stop(
        "D0200_A02_EXECUTION_COUNT_INVALID"
    )

if d0200.get(
    "execution_result"
) != "PASS":
    stop(
        "D0200_A02_RESULT_INVALID"
    )

if d0200.get(
    "lifecycle_state"
) != "PERMANENTLY_RETIRED":
    stop(
        "D0200_A02_RETIREMENT_STATE_INVALID"
    )

if d0200.get(
    "rerun_authorized"
) is not False:
    stop(
        "D0200_A02_RERUN_BOUNDARY_INVALID"
    )

if consumption.get(
    "verifier_sha256"
) != D0200_A02_SHA:
    stop(
        "CONSUMPTION_VERIFIER_SHA_INVALID"
    )

if consumption.get(
    "execution_count"
) != 1:
    stop(
        "CONSUMPTION_EXECUTION_COUNT_INVALID"
    )

if consumption.get(
    "execution_result"
) != "PASS":
    stop(
        "CONSUMPTION_RESULT_INVALID"
    )

if consumption.get(
    "lifecycle_state"
) != "PERMANENTLY_RETIRED":
    stop(
        "CONSUMPTION_RETIREMENT_INVALID"
    )

if consumption.get(
    "rerun_authorized"
) is not False:
    stop(
        "CONSUMPTION_RERUN_BOUNDARY_INVALID"
    )

output_raw = G04.read_bytes()

if hashlib.sha256(
    output_raw
).hexdigest() != consumption.get(
    "execution_output_sha256"
):
    stop(
        "D0200_A02_OUTPUT_BINDING_INVALID"
    )

for marker in (
    "DECISION0200_BOUNDED_ROLE_GOVERNANCE_ADOPTION_AUTHORIZATION_VERIFIER=PASS",
    "ROLE_GOVERNANCE_ADOPTION_AUTHORIZED=YES",
    "ROLE_GOVERNANCE_ADOPTED_BY_THIS_VERIFIER=NO",
    "ACCOUNTING_SATISFACTION_ESTABLISHED=NO",
    "PAIR_RECLASSIFICATION_PERFORMED=NO",
    "AUTHORIZATION_EXECUTION_COUNT_FOR_THIS_RUN=1",
    "AUTHORIZATION_RERUN_AUTHORIZED=NO",
):
    if marker not in output_raw.decode(
        "utf-8"
    ):
        stop(
            "D0200_A02_OUTPUT_MARKER_MISSING",
            marker
        )

sentinel_raw = G05.read_bytes()

if hashlib.sha256(
    sentinel_raw
).hexdigest() != consumption.get(
    "consumption_sentinel_sha256"
):
    stop(
        "D0200_A02_SENTINEL_BINDING_INVALID"
    )

if sentinel.get(
    "verifier_sha256"
) != D0200_A02_SHA:
    stop(
        "D0200_SENTINEL_VERIFIER_SHA_INVALID"
    )

if sentinel.get(
    "rerun_authorized"
) is not False:
    stop(
        "D0200_SENTINEL_RERUN_BOUNDARY_INVALID"
    )

if binding.get(
    "review_outcome",
    {}
).get(
    "overall_decision"
) != "APPROVE_BOUNDED_ROLE_STUDY":
    stop(
        "SOURCE_BINDING_REVIEW_OUTCOME_INVALID"
    )

if manifest.get(
    "next_boundary"
) != (
    "SEPARATELY_AUTHORIZE_REQ06_REQ14_ACCOUNTING_SATISFACTION_EVIDENCE_STUDY"
):
    stop(
        "NEXT_BOUNDARY_INVALID"
    )

print(
    "REQ06_REQ14_BOUNDED_ROLE_GOVERNANCE_ADOPTION_RECORD_VERIFIER=PASS"
)

print(
    "ADOPTION_STATUS="
    "BOUNDED_ROLE_GOVERNANCE_ADOPTED_"
    "ACCOUNTING_SATISFACTION_EVIDENCE_STILL_REQUIRED"
)

print(
    "BOUNDED_ROLE_STUDY_REVIEW_GOVERNANCE_ADOPTED=YES"
)

print(
    "ROLE_GOVERNANCE_ADOPTED=YES"
)

print(
    "REQ06_ROLE_GOVERNANCE_ADOPTED=YES"
)

print(
    "REQ14_ROLE_GOVERNANCE_ADOPTED=YES"
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
    "ACCOUNTING_SATISFACTION_ESTABLISHED=NO"
)

print(
    "PAIR_RECLASSIFICATION_PERFORMED=NO"
)

print(
    "SUPPORTED_BINDING_CREATED=NO"
)

print(
    "NOT_SUPPORTED_BINDING_CREATED=NO"
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
    "DECISION0200_A02_EXECUTION_COUNT=1"
)

print(
    "DECISION0200_A02_RESULT=PASS"
)

print(
    "DECISION0200_A02_STATE=PERMANENTLY_RETIRED"
)

print(
    "DECISION0200_A02_RERUN_AUTHORIZED=NO"
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
