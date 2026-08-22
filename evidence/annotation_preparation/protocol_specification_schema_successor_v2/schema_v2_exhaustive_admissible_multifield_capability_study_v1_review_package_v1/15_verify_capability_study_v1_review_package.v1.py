#!/usr/bin/env python3

import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent

FILES = {
    "study":
        HERE / "01_capability_study_v1.EXACT_COPY.json",

    "units":
        HERE / "02_v4_semantic_unit_inventory.EXACT_COPY.json",

    "carriers":
        HERE / "03_schema_v2_carrier_inventory.EXACT_COPY.json",

    "matrix":
        HERE / "04_candidate_multifield_composition_matrix.EXACT_COPY.json",

    "study_md":
        HERE / "05_capability_study_v1.EXACT_COPY.md",

    "study_sums":
        HERE / "06_capability_study_v1_checksums.EXACT_COPY.SHA256SUMS",

    "study_consumed":
        HERE / "07_pre_study_authorization_verifier_consumed.EXACT_COPY.v1",

    "decision_0084":
        HERE / "08_decision_0084_author_checkpoint.EXACT_COPY.md",

    "authorization":
        HERE / "09_decision_0085_review_package_authorization.EXACT_COPY.json",

    "decision_0085":
        HERE / "10_decision_0085.EXACT_COPY.md",

    "predecessor_review":
        HERE / "11_predecessor_completed_corrective_v2_human_review_record.EXACT_COPY.json",

    "evidence":
        HERE / "12_capability_study_v1_review_evidence.v1.json",

    "packet":
        HERE / "13_capability_study_v1_reviewer_packet.REVIEW_DRAFT.v1.md",

    "pre_package_consumed":
        HERE / "14_pre_review_package_authorization_verifier_consumed.v1",

    "manifest":
        HERE / "16_capability_study_v1_review_package_manifest.v1.json",
}

EXPECTED = {
    "study":
        "9bf685bcd5d8286938f4e221bffd2cc1acc8b5da961d3b0e14f1b10a6a43b78b",

    "units":
        "2b39f5625658e41aeb906a1db8a4a472d9265dc3654572e60374827f0ce7fa7d",

    "carriers":
        "0f32fb87e1396da8c37e3f74c41059560338346ae54f29df0c2d38d72deb1d6d",

    "matrix":
        "c064cfa8c7143b537dc3bb54b8af353f56bafba3e415e7ccdb2c17efaff30d45",

    "study_md":
        "7976e9d079a1df6ef20f183f37a290398a6214079a5b08674aa9ea68b25c600c",

    "study_sums":
        "68d2a28fb99b3fbb4df2e93ddd7569efb97a35367e08ec823afd9e89fc5848b2",

    "study_consumed":
        "0dc3641be811e2d1ce1aa859fabd4ab78edf9d8e1832440f72fa1e58835a8d51",

    "decision_0084":
        "d0d9a3885d0479f19673a114ead2f54df42351739d79bef8434b586b79f82dc7",

    "authorization":
        "638d103b5045508a7567e48efd7638530b7b952bd67d9bf55d136ed8ebb6bb49",

    "decision_0085":
        "06cf32adac408ccaf4d0747572dee9b265afa116510c38ea9e1f30bb6b562b39",

    "predecessor_review":
        "d6d1142315f3830abfd2f5d33ca4fff120d1c814d07f80b1b4eb6c96ae0378c1",
}

def fail(msg):
    print("FAIL|" + msg)
    raise SystemExit(1)

def sha(path):
    if not path.is_file():
        fail("MISSING|" + str(path))

    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()

for key, expected in EXPECTED.items():
    if sha(FILES[key]) != expected:
        fail("EXACT_COPY_SHA|" + key)

study = json.loads(
    FILES["study"].read_text(
        encoding="utf-8"
    )
)

units = json.loads(
    FILES["units"].read_text(
        encoding="utf-8"
    )
)

carriers = json.loads(
    FILES["carriers"].read_text(
        encoding="utf-8"
    )
)

matrix = json.loads(
    FILES["matrix"].read_text(
        encoding="utf-8"
    )
)

auth = json.loads(
    FILES["authorization"].read_text(
        encoding="utf-8"
    )
)

evidence = json.loads(
    FILES["evidence"].read_text(
        encoding="utf-8"
    )
)

manifest = json.loads(
    FILES["manifest"].read_text(
        encoding="utf-8"
    )
)

if study["status"] != "AUTHOR_CANDIDATE":
    fail("STUDY_STATUS")

if study["selected_outcome"] != "FURTHER_EVIDENCE_REQUIRED":
    fail("STUDY_OUTCOME")

if study["selected_outcome_human_approved"] is not False:
    fail("STUDY_HUMAN_APPROVAL")

if units["semantic_unit_count"] != 109:
    fail("SEMANTIC_UNIT_COUNT")

if units["leaf_field_count"] != 531:
    fail("LEAF_FIELD_COUNT")

if carriers["property_path_count"] != 171:
    fail("PROPERTY_PATH_COUNT")

if carriers["distinct_property_name_count"] != 123:
    fail("PROPERTY_NAME_COUNT")

if carriers["open_unconstrained_string_path_count"] != 59:
    fail("OPEN_STRING_COUNT")

if matrix["field_class_count"] != 57:
    fail("FIELD_CLASS_COUNT")

if matrix["unit_analysis_count"] != 109:
    fail("UNIT_ANALYSIS_COUNT")

if matrix[
    "all_admissible_semantically_related_compositions_machine_enumerated"
] is not False:
    fail("COMPOSITION_EXHAUSTIVENESS")

if auth["status"] != \
   "AUTHORIZED_TO_AUTHOR_CAPABILITY_STUDY_V1_INDEPENDENT_HUMAN_TECHNICAL_REVIEW_PACKAGE_V1_ONLY":
    fail("AUTH_STATUS")

if list(auth["mandatory_review_items"]) != [
    "CSR01",
    "CSR02",
    "CSR03",
    "CSR04",
    "CSR05",
    "CSR06",
    "CSR07",
    "CSR08",
]:
    fail("CSR_ITEM_SET")

machine = evidence[
    "machine_checked_capability_state"
]

for key in (
    "positive_existing_v2_mapping_path_proven",
    "complete_constructive_witness_available",
    "deterministic_complete_forward_encoding_proven",
    "deterministic_exact_reverse_reconstruction_proven",
    "complete_mapping_collision_freedom_proven",
    "complete_mapping_semantic_noninterference_proven",
    "negative_existing_v2_mapping_impossibility_proven",
    "negative_exhaustive_elimination_complete",
    "all_admissible_compositions_machine_enumerated",
    "semantic_role_relation_formalization_complete",
    "admissible_composition_exhaustiveness_established",
):
    if machine[key] is not False:
        fail("CAPABILITY_STATE|" + key)

packet = FILES["packet"].read_text(
    encoding="utf-8"
)

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
    if packet.count("### " + rid + " ") != 1:
        fail("PACKET_ITEM|" + rid)

decisions = re.findall(
    r"^Decision \(PASS / REVISION_REQUIRED / FAIL\):(.*)$",
    packet,
    flags=re.MULTILINE,
)

if len(decisions) != 8:
    fail("ITEM_DECISION_COUNT")

if any(x.strip() for x in decisions):
    fail("ITEM_DECISION_NOT_BLANK")

overall = re.findall(
    r"^Overall decision "
    r"\(APPROVE_SCHEMA_V2_CAPABILITY_STUDY_V1 / "
    r"REVISION_REQUIRED / FAIL\):(.*)$",
    packet,
    flags=re.MULTILINE,
)

if len(overall) != 1:
    fail("OVERALL_DECISION_COUNT")

if overall[0].strip():
    fail("OVERALL_DECISION_NOT_BLANK")

for field in (
    "Reviewer role:",
    "Human reviewer name:",
    "Human reviewer signature / recorded confirmation:",
    "Human reviewer date:",
):
    lines = [
        line
        for line in packet.splitlines()
        if line.startswith(field)
    ]

    if len(lines) != 1:
        fail("IDENTITY_FIELD_COUNT|" + field)

    if lines[0][len(field):].strip():
        fail("IDENTITY_FIELD_NOT_BLANK|" + field)

consumed = FILES[
    "pre_package_consumed"
].read_text(
    encoding="utf-8"
).splitlines()

for required in (
    "DECISION_0085_PRE_REVIEW_PACKAGE_AUTHORIZATION_VERIFIER_FINAL_RUN=PASS",
    "REVIEW_PACKAGE_AUTHORING_FOLLOWED_FINAL_RUN=YES",
    "PERMANENTLY_RETIRED_AFTER_REVIEW_PACKAGE_AUTHORING=YES",
    "RERUN_ALLOWED=NO",
):
    if required not in consumed:
        fail(
            "PRE_PACKAGE_VERIFIER_CONSUMPTION|"
            + required
        )

if evidence[
    "synthetic_reviewer_decision"
] is not False:
    fail("SYNTHETIC_REVIEW")

if evidence[
    "independent_human_review_completed"
] is not False:
    fail("HUMAN_REVIEW_COMPLETION_STATE")

for key, value in auth[
    "explicit_non_authorizations"
].items():
    if value is not False:
        fail("NONAUTH|" + key)

if manifest[
    "reviewer_packet_initial_state"
][
    "CSR01_to_CSR08_decisions_blank"
] is not True:
    fail("MANIFEST_ITEM_BLANK_STATE")

if manifest[
    "reviewer_packet_initial_state"
][
    "overall_decision_blank"
] is not True:
    fail("MANIFEST_OVERALL_BLANK_STATE")

if manifest[
    "reviewer_packet_initial_state"
][
    "reviewer_identity_fields_blank"
] is not True:
    fail("MANIFEST_IDENTITY_BLANK_STATE")

print("CAPABILITY_STUDY_V1_EXACT_BINDING=PASS")
print("V4_SEMANTIC_CONTAINER_COUNT=10")
print("V4_SEMANTIC_UNIT_COUNT=109")
print("V4_LEAF_FIELD_COUNT=531")
print("V4_FIELD_CLASS_COUNT=57")
print("V4_RULE_COUNT=64")
print("V4_EXIT_OBLIGATION_COUNT=3")
print("V4_REPRESENTATION_POLICY_FIELD_COUNT=10")
print("DISTINCT_ENFORCEMENT_VALUE_COUNT=15")
print("SCHEMA_V2_PROPERTY_PATH_COUNT=171")
print("SCHEMA_V2_DISTINCT_PROPERTY_NAME_COUNT=123")
print("SCHEMA_V2_OPEN_STRING_CARRIER_COUNT=59")

print("POSITIVE_EXISTING_V2_MAPPING_PATH_PROVEN=NO")
print("NEGATIVE_EXISTING_V2_MAPPING_PATH_IMPOSSIBILITY_PROVEN=NO")
print("ADMISSIBLE_COMPOSITION_EXHAUSTIVENESS_ESTABLISHED=NO")

print("CAPABILITY_STUDY_V1_SELECTED_OUTCOME=FURTHER_EVIDENCE_REQUIRED")
print("CAPABILITY_STUDY_V1_SELECTED_OUTCOME_HUMAN_APPROVED=NO")

print("CSR01_TO_CSR08_PRESENT=YES")
print("CSR01_TO_CSR08_INITIAL_DECISIONS_BLANK=YES")
print("OVERALL_CAPABILITY_STUDY_REVIEW_DECISION_INITIAL_BLANK=YES")
print("REVIEWER_IDENTITY_FIELDS_INITIAL_BLANK=YES")

print("CAPABILITY_STUDY_V1_INDEPENDENT_HUMAN_REVIEW_COMPLETED=NO")
print("SYNTHETIC_REVIEWER_DECISION=NO")

print("DECISION_0085_PRE_REVIEW_PACKAGE_VERIFIER_PERMANENTLY_RETIRED=YES")
print("DECISION_0085_PRE_REVIEW_PACKAGE_VERIFIER_RERUN_ALLOWED=NO")
print("DECISION_0083_PRE_STUDY_VERIFIER_RERUN=NO")

print("OPERATIONAL_POSITIVE_MAPPING_CONTRACT_AUTHORIZED=NO")
print("SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO")
print("SCHEMA_VERSION_PRESELECTED=NO")
print("SCHEMA_V3_CREATED=NO")
print("CURL_JSON_CREATED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")

print("SELF_CONTAINED_CAPABILITY_STUDY_V1_REVIEW_PACKAGE_V1=PASS")
