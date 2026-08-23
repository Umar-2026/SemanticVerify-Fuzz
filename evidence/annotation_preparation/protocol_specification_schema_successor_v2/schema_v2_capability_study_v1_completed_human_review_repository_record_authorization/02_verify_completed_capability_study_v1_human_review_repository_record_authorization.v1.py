#!/usr/bin/env python3

import json
from pathlib import Path

REPO = Path(
    "/openbayes/home/semanticverify-fuzz-research"
)

HERE = Path(__file__).resolve().parent

AUTH = HERE / \
    "01_completed_capability_study_v1_human_review_repository_record_authorization.v1.json"

RECORD_DIR = (
    REPO
    / "evidence/annotation_preparation/protocol_specification_schema_successor_v2"
    / "schema_v2_capability_study_v1_completed_human_review_v1"
)

def fail(msg):
    print("FAIL|" + msg)
    raise SystemExit(1)

a = json.loads(
    AUTH.read_text(
        encoding="utf-8"
    )
)

if a[
    "authorization_type"
] != "PRE_REPOSITORY_HUMAN_REVIEW_RECORD_AUTHORING_ONLY":
    fail("AUTHORIZATION_TYPE")

if a[
    "status"
] != "AUTHORIZED_TO_RECORD_COMPLETED_CAPABILITY_STUDY_V1_HUMAN_REVIEW_IN_REPOSITORY_ONLY":
    fail("STATUS")

state = a[
    "human_review_state"
]

for rid in (
    "CSR01",
    "CSR02",
    "CSR03",
    "CSR04",
    "CSR05",
    "CSR06",
    "CSR07",
    "CSR08",
):
    if state[rid] != "PASS":
        fail(rid)

if state[
    "overall"
] != "APPROVE_SCHEMA_V2_CAPABILITY_STUDY_V1":
    fail("OVERALL")

if state[
    "capability_study_v1_human_approved"
] is not True:
    fail("STUDY_APPROVAL")

if state[
    "further_evidence_required_human_approved"
] is not True:
    fail("FER_APPROVAL")

for key in (
    "positive_existing_v2_mapping_path_proven",
    "negative_existing_v2_mapping_path_impossibility_proven",
    "admissible_composition_exhaustiveness_established",
):
    if state[key] is not False:
        fail("OVERCLAIM|" + key)

constraints = a[
    "mandatory_recording_constraints"
]

for key, value in constraints.items():
    if value is not True:
        fail("RECORDING_CONSTRAINT|" + key)

for key, value in a[
    "retired_verifier_constraints"
].items():
    if value is not False:
        fail("RETIRED_VERIFIER|" + key)

for key, value in a[
    "explicit_non_authorizations"
].items():
    if value is not False:
        fail("NONAUTH|" + key)

if RECORD_DIR.exists():
    fail("REPOSITORY_HUMAN_REVIEW_RECORD_ALREADY_EXISTS")

for forbidden in (
    REPO / "config/protocol_specifications/curl.json",
    REPO / "config/annotation/curl_positive_v4_to_v2_mapping_contract.v1.json",
    REPO / "config/annotation/curl_positive_v4_to_successor_mapping_contract.v1.json",
    REPO / "config/schemas/protocol_specification.v3.schema.json",
):
    if forbidden.exists():
        fail(
            "FORBIDDEN_ARTIFACT|"
            + str(forbidden)
        )

print("CSR01_TO_CSR08=PASS")
print("OVERALL_HUMAN_DECISION=APPROVE_SCHEMA_V2_CAPABILITY_STUDY_V1")

print("CAPABILITY_STUDY_V1_HUMAN_APPROVED=YES")
print("FURTHER_EVIDENCE_REQUIRED_HUMAN_APPROVED=YES")

print("POSITIVE_EXISTING_V2_MAPPING_PATH_PROVEN=NO")
print("NEGATIVE_EXISTING_V2_MAPPING_PATH_IMPOSSIBILITY_PROVEN=NO")
print("ADMISSIBLE_COMPOSITION_EXHAUSTIVENESS_ESTABLISHED=NO")

print("REPOSITORY_COMPLETED_HUMAN_REVIEW_RECORD_AUTHORIZED=YES")
print("REPOSITORY_COMPLETED_HUMAN_REVIEW_RECORD_AUTHORED=NO")

print("INITIAL_BLANK_CSR01_CSR08_VERIFIER_RERUN=NO")
print("DECISION_0085_PRE_REVIEW_PACKAGE_VERIFIER_RERUN=NO")
print("DECISION_0083_PRE_STUDY_VERIFIER_RERUN=NO")

print("OPERATIONAL_POSITIVE_MAPPING_CONTRACT_AUTHORIZED=NO")
print("SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO")
print("SCHEMA_VERSION_PRESELECTED=NO")
print("SCHEMA_V3_CREATED=NO")
print("CURL_JSON_CREATED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")

print("DECISION_0087_REPOSITORY_RECORD_AUTHORIZATION=PASS")
print("IMPORTANT=THIS_VERIFIER_IS_PRE_REPOSITORY_HUMAN_REVIEW_RECORD_AUTHORING_ONLY")
