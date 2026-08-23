#!/usr/bin/env python3

import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]

FILES = {
    "02_formalization_summary.EXACT_COPY.v1.json":
        "0efc848991f0f1580542b8d6e380c55df6d2b370147f236800621b24b51ee600",

    "03_field_class_to_schema_v2_property_path_relation.EXACT_COPY.v1.json":
        "239e6492faca3bb6da0c79abdb980470e2ea76690fc1f081562ccdbf7f303a32",

    "04_semantic_unit_context_and_leaf_traceability.EXACT_COPY.v1.json":
        "6b4b30c958bc1e1dd0896fe086205e3ff58063583b2042bba962c8c59ba46bd4",

    "05_formalization_report.EXACT_COPY.v1.md":
        "7b71d98c63afabc6d3b5eaf72f07e0ee2e4a6707520d80032a9d51b9540878d4",

    "06_decision_0089_verifier_consumption_marker.EXACT_COPY.v1":
        "55005f555ec580c0e623033137930fa976412aa48dc0acaddc49e767d87bb391",

    "07_formalization_safe_verifier.EXACT_COPY.v1.py":
        "842763889dd0958a39b9403832c97d2ea83cbbf8c91bc529931323f3e62f38b0",

    "08_formalization_checksum_manifest.EXACT_COPY.v1.SHA256SUMS":
        "46cbb87c47ce4332c98a80bd769346129d7a54f5cb6aa037d62a7016025e45f6",

    "09_decision_0090.EXACT_COPY.md":
        "96c5a9719101bf384022b7d8378df1a5e60abf0cb096ea5d9cbcd03be4e2a8b4",

    "10_decision_0091_review_package_authorization.EXACT_COPY.v1.json":
        "be6f78129e16ba3738cbd460e43cac603f261b86951065615531a68d7eef88b5",

    "11_decision_0091_pre_review_package_verifier.EXACT_COPY.v1.py":
        "b221024566fb4d08f94232ae745df4b62d60084dc71b12d825a147ecbebb1b4a",

    "12_decision_0091_authorization_checksum.EXACT_COPY.v1.SHA256SUMS":
        "76dc4ddefd9395138ed287cd03b402df74f026e9c10812c96b3cd2289ad25ae2",

    "13_decision_0091.EXACT_COPY.md":
        "cf61a39592b8b906094beb263fd74b93032837999fd0605f8b9ffd1b3d384eb7",
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

for name, expected in FILES.items():
    path = HERE / name

    if sha(path) != expected:
        fail(
            "EXACT_COPY_SHA|"
            + name
        )

scope = json.loads(
    (
        HERE
        / "01_review_scope_and_evidence.v1.json"
    ).read_text(
        encoding="utf-8"
    )
)

if scope[
    "status"
] != "IMMUTABLE_BLANK_INDEPENDENT_HUMAN_TECHNICAL_REVIEW_PACKAGE":
    fail("SCOPE_STATUS")

if scope[
    "review_target"
] != "SCHEMA_V2_SEMANTIC_ROLE_RELATION_FORMALIZATION_V1":
    fail("REVIEW_TARGET")

if scope[
    "formalization_status"
] != "AUTHOR_CANDIDATE":
    fail("FORMALIZATION_STATUS")

if scope[
    "formalization_selected_outcome"
] != "PARTIAL_RELATION_FURTHER_EVIDENCE_REQUIRED":
    fail("OUTCOME")

if scope[
    "formalization_selected_outcome_human_approved"
] is not False:
    fail("PREEXISTING_HUMAN_APPROVAL")

expected_items = {
    "SRR01",
    "SRR02",
    "SRR03",
    "SRR04",
    "SRR05",
    "SRR06",
    "SRR07",
    "SRR08",
}

if set(
    scope[
        "mandatory_review_items"
    ]
) != expected_items:
    fail("REVIEW_ITEMS")

counts = scope[
    "reviewed_evidence_counts"
]

expected_counts = {
    "leaf_field_records": 531,
    "semantic_units": 109,
    "matrix_field_classes": 57,
    "schema_v2_property_paths": 171,
    "semantic_role_pairs": 9747,
    "semantically_related_pairs": 113,
    "not_semantically_related_pairs": 969,
    "unresolved_pairs": 8665,
    "lexical_only_pairs_retained_unresolved": 125,
}

if counts != expected_counts:
    fail("REVIEWED_EVIDENCE_COUNTS")

packet = (
    HERE
    / "15_semantic_role_relation_formalization_v1_reviewer_packet.BLANK.v1.md"
).read_text(
    encoding="utf-8"
)

for rid in sorted(expected_items):
    heading = "## " + rid

    if heading not in packet:
        fail(
            "PACKET_MISSING_ITEM|" + rid
        )

decision_lines = re.findall(
    r"^Decision \(PASS / REVISION_REQUIRED / FAIL\):[ \t]*(.*)$",
    packet,
    flags=re.MULTILINE,
)

if len(decision_lines) != 8:
    fail("PACKET_DECISION_LINE_COUNT")

if any(
    value.strip()
    for value in decision_lines
):
    fail("PACKET_ITEM_DECISION_NOT_BLANK")

overall = re.findall(
    r"^Overall decision "
    r"\(APPROVE_SCHEMA_V2_SEMANTIC_ROLE_RELATION_FORMALIZATION_V1 / "
    r"REVISION_REQUIRED / FAIL\):[ \t]*(.*)$",
    packet,
    flags=re.MULTILINE,
)

if len(overall) != 1:
    fail("PACKET_OVERALL_LINE")

if overall[0].strip():
    fail("PACKET_OVERALL_NOT_BLANK")

identity_patterns = {
    "Human reviewer name:":
        r"^Human reviewer name:[ \t]*(.*)$",

    "Human reviewer signature / recorded confirmation:":
        r"^Human reviewer signature / recorded confirmation:[ \t]*(.*)$",

    "Human reviewer date:":
        r"^Human reviewer date:[ \t]*(.*)$",
}

for label, pattern in identity_patterns.items():
    values = re.findall(
        pattern,
        packet,
        flags=re.MULTILINE,
    )

    if len(values) != 1:
        fail(
            "PACKET_IDENTITY_FIELD|" + label
        )

    if values[0].strip():
        fail(
            "PACKET_IDENTITY_PREPOPULATED|" + label
        )

role = re.findall(
    r"^Reviewer role:\s*(.*)$",
    packet,
    flags=re.MULTILINE,
)

if role != [
    "Spec-Technical-Reviewer-1"
]:
    fail("PACKET_REVIEWER_ROLE")

consumed = (
    HERE
    / "14_pre_review_package_authorization_verifier_consumed.v1"
).read_text(
    encoding="utf-8"
).splitlines()

for required in (
    "DECISION_0091_PRE_REVIEW_PACKAGE_AUTHORIZATION_VERIFIER_FINAL_RUN=PASS",
    "REVIEW_PACKAGE_AUTHORING_FOLLOWED_FINAL_RUN=YES",
    "PERMANENTLY_RETIRED_AFTER_REVIEW_PACKAGE_AUTHORING=YES",
    "RERUN_ALLOWED=NO",
):
    if required not in consumed:
        fail(
            "CONSUMPTION|" + required
        )

manifest = json.loads(
    (
        HERE
        / "17_semantic_role_relation_formalization_v1_review_package_manifest.v1.json"
    ).read_text(
        encoding="utf-8"
    )
)

if manifest[
    "status"
] != "IMMUTABLE_INDEPENDENT_HUMAN_TECHNICAL_REVIEW_PACKAGE_V1":
    fail("MANIFEST_STATUS")

if manifest[
    "human_review_state"
] != "BLANK_UNREVIEWED":
    fail("MANIFEST_HUMAN_REVIEW_STATE")

if manifest[
    "human_decision_created"
] is not False:
    fail("MANIFEST_HUMAN_DECISION")

if manifest[
    "reviewer_identity_prepopulated"
] is not False:
    fail("MANIFEST_REVIEWER_IDENTITY")

for key, value in manifest[
    "bounded_non_authorizations"
].items():
    if value is not False:
        fail(
            "MANIFEST_NONAUTH|" + key
        )

for forbidden in (
    REPO
    / "config/protocol_specifications/curl.json",

    REPO
    / "config/annotation/curl_positive_v4_to_v2_mapping_contract.v1.json",

    REPO
    / "config/annotation/curl_positive_v4_to_successor_mapping_contract.v1.json",

    REPO
    / "config/schemas/protocol_specification.v3.schema.json",
):
    if forbidden.exists():
        fail(
            "FORBIDDEN_ARTIFACT|"
            + str(forbidden)
        )

print("SRR01_BLANK=YES")
print("SRR02_BLANK=YES")
print("SRR03_BLANK=YES")
print("SRR04_BLANK=YES")
print("SRR05_BLANK=YES")
print("SRR06_BLANK=YES")
print("SRR07_BLANK=YES")
print("SRR08_BLANK=YES")

print("OVERALL_HUMAN_DECISION_BLANK=YES")
print("HUMAN_REVIEWER_NAME_BLANK=YES")
print("HUMAN_REVIEWER_CONFIRMATION_BLANK=YES")
print("HUMAN_REVIEWER_DATE_BLANK=YES")

print("FORMALIZATION_SELECTED_OUTCOME=PARTIAL_RELATION_FURTHER_EVIDENCE_REQUIRED")
print("FORMALIZATION_SELECTED_OUTCOME_HUMAN_APPROVED=NO")

print("SEMANTIC_ROLE_PAIR_COUNT=9747")
print("SEMANTICALLY_RELATED_PAIR_COUNT=113")
print("NOT_SEMANTICALLY_RELATED_PAIR_COUNT=969")
print("UNRESOLVED_PAIR_COUNT=8665")
print("LEXICAL_ONLY_PAIR_COUNT=125")

print("POSITIVE_EXISTING_V2_MAPPING_PATH_PROVEN=NO")
print("NEGATIVE_EXISTING_V2_MAPPING_IMPOSSIBILITY_PROVEN=NO")
print("ADMISSIBLE_COMPOSITION_EXHAUSTIVENESS_ESTABLISHED=NO")

print("DECISION_0091_PRE_REVIEW_PACKAGE_VERIFIER_PERMANENTLY_RETIRED=YES")
print("DECISION_0091_PRE_REVIEW_PACKAGE_VERIFIER_RERUN_ALLOWED=NO")

print("SCHEMA_V2_SEMANTIC_ROLE_RELATION_FORMALIZATION_V1_REVIEW_PACKAGE=PASS")
