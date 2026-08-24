#!/usr/bin/env python3

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]

BASE_REL = (
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2"
)

ASSESSMENT = (
    HERE
    / "01_governance_adoption_assessment.v1.json"
)

SUMS = (
    HERE
    / "03_governance_adoption.v1.SHA256SUMS"
)

REVIEW = (
    REPO
    / BASE_REL
    / "schema_v2_relation_informed_exhaustive_"
      "admissible_composition_study_v1_completed_human_review_v1"
)

C01 = (
    REVIEW
    / "01_completed_RIAC01_RIAC08_human_review.EXACT_COPY.v1.md"
)

C02 = (
    REVIEW
    / "02_completed_human_review_record.v1.json"
)

C03 = (
    REVIEW
    / "03_verify_repository_completed_RIAC01_RIAC08_human_review.v1.py"
)

C04 = (
    REVIEW
    / "04_completed_human_review.v1.SHA256SUMS"
)

STUDY = (
    REPO
    / BASE_REL
    / "schema_v2_relation_informed_exhaustive_"
      "admissible_composition_study_v1/"
      "01_relation_informed_exhaustive_admissible_composition_study.v1.json"
)

DEC0108 = (
    REPO
    / "documentation/decisions/"
      "0108-record-completed-independent-human-review-for-relation-informed-study-v1.md"
)

EXPECTED = {
    C01:
        "7730e555a2d85b96dae1c75d20ef23da7670831feb3f398eaac600c64d323d98",

    C02:
        "177768f2975908470097e36234a5a6a1bc4843a33b77968b4f0a2429b6f9722e",

    C03:
        "f139f41399b61727876a6970efa5ae4eb3bfa72b8b0fa74b172eeaf8ba8b420d",

    C04:
        "9b4b04d8bd50f0cfae61009ef1e22ad98b8ca731f0d09a2e92ec60793948d65c",

    STUDY:
        "a8d28b09e78e1466eb5bb0991289879b28b10abd1dd1f9197d138ca723718f6f",

    DEC0108:
        "2ef3a1a1d8b73827bbc0c9d419e2db92aaa50cf402bd95a9c907a216ff84fe70",
}

def fail(msg):
    print("FAIL|" + msg)
    raise SystemExit(1)

def sha(path):
    if not path.is_file():
        fail(
            "MISSING|" + str(path)
        )

    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()

for path, expected in EXPECTED.items():
    if sha(path) != expected:
        fail(
            "SOURCE_BINDING|" + str(path)
        )

review = json.loads(
    C02.read_text(
        encoding="utf-8"
    )
)

expected_items = {
    "RIAC01": "PASS",
    "RIAC02": "PASS",
    "RIAC03": "PASS",
    "RIAC04": "PASS",
    "RIAC05": "PASS",
    "RIAC06": "PASS",
    "RIAC07": "PASS",
    "RIAC08": "PASS",
}

if review["item_decisions"] != expected_items:
    fail(
        "HUMAN_REVIEW_ITEM_DECISIONS"
    )

expected_overall = (
    "APPROVE_RELATION_INFORMED_EXHAUSTIVE_"
    "ADMISSIBLE_COMPOSITION_STUDY_V1"
)

if review["overall_review_decision"] != \
        expected_overall:
    fail(
        "HUMAN_REVIEW_OVERALL_DECISION"
    )

study = json.loads(
    STUDY.read_text(
        encoding="utf-8"
    )
)

if study["status"] != "AUTHOR_CANDIDATE":
    fail(
        "SOURCE_STUDY_STATUS"
    )

if study["global_outcome"] != \
        "FURTHER_EVIDENCE_REQUIRED":
    fail(
        "SOURCE_STUDY_OUTCOME"
    )

assessment = json.loads(
    ASSESSMENT.read_text(
        encoding="utf-8"
    )
)

if assessment["status"] != \
        "GOVERNANCE_ADOPTED_WITH_BOUNDED_TECHNICAL_OUTCOME":
    fail(
        "ADOPTION_STATUS"
    )

g = assessment["governance_adoption"]

if g[
    "completed_human_review_adopted"
] is not True:
    fail(
        "HUMAN_REVIEW_NOT_ADOPTED"
    )

if g[
    "reviewed_bounded_study_outcome_adopted"
] is not True:
    fail(
        "BOUNDED_OUTCOME_NOT_ADOPTED"
    )

if g[
    "study_governance_approved"
] is not True:
    fail(
        "STUDY_GOVERNANCE_NOT_APPROVED"
    )

if g[
    "governance_status"
] != "APPROVED_WITH_BOUNDED_TECHNICAL_OUTCOME":
    fail(
        "GOVERNANCE_STATUS"
    )

if g[
    "source_study_artifact_remains_immutable"
] is not True:
    fail(
        "SOURCE_STUDY_IMMUTABILITY"
    )

if g[
    "source_study_artifact_status_remains"
] != "AUTHOR_CANDIDATE":
    fail(
        "SOURCE_STUDY_STATUS_MUTATED"
    )

if g[
    "adopted_technical_outcome"
] != "FURTHER_EVIDENCE_REQUIRED":
    fail(
        "ADOPTED_TECHNICAL_OUTCOME"
    )

if g[
    "technical_outcome_changed_by_governance_adoption"
] is not False:
    fail(
        "TECHNICAL_OUTCOME_CHANGED"
    )

bounded = assessment[
    "adopted_bounded_findings"
]

if bounded[
    "field_class_relation_domain_complete"
] is not True:
    fail(
        "RELATION_DOMAIN_COMPLETENESS"
    )

if bounded[
    "semantic_unit_inventory_complete"
] is not True:
    fail(
        "SEMANTIC_UNIT_INVENTORY_COMPLETENESS"
    )

for key in (
    "whole_v4_admissible_composition_universe_proven_complete",
    "positive_existing_v2_mapping_witness_identified",
    "negative_existing_v2_mapping_impossibility_proven",
    "whole_v4_admissible_composition_exhaustiveness_established",
):
    if bounded[key] is not False:
        fail(
            "UNSUPPORTED_BOUNDED_FINDING|" + key
        )

for key, value in assessment[
    "explicit_non_authorizations"
].items():
    if value is not False:
        fail(
            "UNEXPECTED_OPERATIONAL_AUTHORIZATION|" + key
        )

for key, value in assessment[
    "retired_verifier_state"
].items():
    if key == \
            "retired_a02_verifiers_executed_during_governance_adoption":

        if value is not False:
            fail(
                "RETIRED_A02_EXECUTED"
            )

    else:
        if value != "PERMANENTLY_RETIRED":
            fail(
                "RETIRED_A02_STATE|" + key
            )

if SUMS.is_file():
    lines = [
        line
        for line in SUMS.read_text(
            encoding="utf-8"
        ).splitlines()
        if line.strip()
    ]

    if len(lines) != 2:
        fail(
            "CHECKSUM_ENTRY_COUNT|"
            + str(len(lines))
        )

    for line in lines:
        digest, rel = line.split(
            None,
            1,
        )

        rel = rel.strip().lstrip("*")
        target = HERE / rel

        if sha(target) != digest:
            fail(
                "CHECKSUM|" + rel
            )

print("COMPLETED_HUMAN_REVIEW_BINDING=PASS")
print("RIAC01_RIAC08_ALL_PASS=YES")
print(
    "OVERALL_HUMAN_REVIEW_DECISION="
    + expected_overall
)

print("COMPLETED_HUMAN_REVIEW_GOVERNANCE_ADOPTED=YES")
print("BOUNDED_STUDY_V1_OUTCOME_GOVERNANCE_ADOPTED=YES")
print("STUDY_GOVERNANCE_APPROVED=YES")
print("GOVERNANCE_STATUS=APPROVED_WITH_BOUNDED_TECHNICAL_OUTCOME")

print("SOURCE_STUDY_ARTIFACT_STATUS=AUTHOR_CANDIDATE")
print("SOURCE_STUDY_ARTIFACT_MODIFIED=NO")
print("ADOPTED_TECHNICAL_OUTCOME=FURTHER_EVIDENCE_REQUIRED")

print("FIELD_CLASS_RELATION_DOMAIN_COMPLETE=YES")
print("SEMANTIC_UNIT_INVENTORY_COMPLETE=YES")
print("WHOLE_V4_ADMISSIBLE_COMPOSITION_UNIVERSE_PROVEN_COMPLETE=NO")

print("POSITIVE_EXISTING_V2_MAPPING_PROVEN=NO")
print("NEGATIVE_EXISTING_V2_MAPPING_IMPOSSIBILITY_PROVEN=NO")

print("OPERATIONAL_POSITIVE_MAPPING_AUTHORIZED=NO")
print("ACTIVE_SCHEMA_V2_MODIFICATION_AUTHORIZED=NO")
print("SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO")
print("SCHEMA_VERSION_PRESELECTED=NO")
print("SCHEMA_V3_CREATED=NO")
print("CURL_JSON_AUTHORIZED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")

print("RETIRED_A02_VERIFIERS_EXECUTED=NO")
print("RELATION_INFORMED_STUDY_V1_GOVERNANCE_ADOPTION=PASS")
