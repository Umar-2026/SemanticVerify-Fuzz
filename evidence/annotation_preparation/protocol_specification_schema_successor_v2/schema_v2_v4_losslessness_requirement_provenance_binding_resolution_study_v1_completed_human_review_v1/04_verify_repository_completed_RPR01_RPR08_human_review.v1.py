#!/usr/bin/env python3

import hashlib
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]

BASE_REL = (
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2"
)

HANDOFF_REL = (
    BASE_REL
    + "/schema_v2_v4_losslessness_requirement_provenance_binding_resolution_study_v1_external_handoff_corrective_v1"
)

RECORD_REL = (
    BASE_REL
    + "/schema_v2_v4_losslessness_requirement_provenance_binding_resolution_study_v1_completed_human_review_v1"
)

REVIEW = (
    HERE
    / "01_completed_RPR01_RPR08_human_review.EXACT_COPY.v1.md"
)

MANIFEST = (
    HERE
    / "02_completed_human_review_manifest.v1.json"
)

DEC0133 = (
    HERE
    / "03_decision0133.EXACT_COPY.md"
)

SUMS = (
    HERE
    / "05_completed_human_review_v1.SHA256SUMS"
)

EXPECTED_REVIEW_SHA = (
    "f133c13bdaeb71055bd839663332c921"
    "556dc516544e19e655f204032d33af71"
)

EXPECTED_REVIEW_SIZE = 7251

EXPECTED_HANDOFF_TREE = (
    "050d80d79457a88265a42f4a795a5735f1171291"
)

EXPECTED_DEC0133_SHA = (
    "c444997de152ff46ad1b8d4b0720f8b8"
    "4dc926aed37231506e96f8f6cabf93c3"
)

def fail(msg):
    print("FAIL|" + msg)
    raise SystemExit(1)

def sha(path):
    if not path.is_file():
        fail("MISSING|" + str(path))

    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()

if sha(REVIEW) != EXPECTED_REVIEW_SHA:
    fail("COMPLETED_REVIEW_SHA")

if REVIEW.stat().st_size != EXPECTED_REVIEW_SIZE:
    fail("COMPLETED_REVIEW_SIZE")

if sha(DEC0133) != EXPECTED_DEC0133_SHA:
    fail("DECISION0133_EXACT_COPY")

text = REVIEW.read_text(
    encoding="utf-8"
)

lines = text.splitlines()

if sum(
    1
    for line in lines
    if line.strip() == "Decision: `PASS`"
) != 8:
    fail("RPR_PASS_COUNT")

required_lines = [
    "Overall decision: `APPROVE_V4_LOSSLESSNESS_REQUIREMENT_PROVENANCE_BINDING_RESOLUTION_STUDY_V1`",
    "Human reviewer name: Abdul Raheem Shahzad",
    "Human reviewer signature / recorded confirmation: ARS",
    "Human reviewer date: 24 / August / 2026",
    "Reviewer role: Spec-Technical-Reviewer-1",
]

for line in required_lines:
    if line not in lines:
        fail(
            "REQUIRED_REVIEW_FIELD|"
            + line
        )

manifest = json.loads(
    MANIFEST.read_text(
        encoding="utf-8"
    )
)

if (
    manifest["record_status"]
    != "COMPLETED_INDEPENDENT_HUMAN_REVIEW_RECORDED"
):
    fail("RECORD_STATUS")

packet = manifest[
    "completed_reviewer_packet"
]

for key in (
    "rpr01",
    "rpr02",
    "rpr03",
    "rpr04",
    "rpr05",
    "rpr06",
    "rpr07",
    "rpr08",
):
    if packet[key] != "PASS":
        fail(
            "RPR_DECISION|"
            + key
        )

if (
    packet["overall_decision"]
    != "APPROVE_V4_LOSSLESSNESS_REQUIREMENT_PROVENANCE_BINDING_RESOLUTION_STUDY_V1"
):
    fail("OVERALL_DECISION")

if packet["human_review_completed"] is not True:
    fail("HUMAN_REVIEW_STATE")

if packet["reviewer_decision_synthesized"] is not False:
    fail("SYNTHETIC_REVIEW_STATE")

if (
    manifest["approved_scope"]
    != "REQUIREMENT_IDENTITY_AND_SOURCE_PROVENANCE_ONLY"
):
    fail("APPROVAL_SCOPE")

review_interp = manifest[
    "review_interpretation"
]

if (
    review_interp["requirement_provenance_result_approved"]
    is not True
):
    fail("PROVENANCE_APPROVAL_STATE")

for key in (
    "schema_v2_losslessness_proven",
    "carrier_admissibility_proven",
    "positive_mapping_proven",
    "negative_mapping_impossibility_proven",
    "whole_v4_exhaustiveness_proven",
):
    if review_interp[key] is not False:
        fail(
            "UNEXPECTED_TECHNICAL_CLAIM|"
            + key
        )

gov = manifest[
    "governance_state"
]

if gov["completed_human_review_recorded"] is not True:
    fail("COMPLETED_REVIEW_GOV_STATE")

if gov["study_governance_adopted"] is not False:
    fail("PREMATURE_GOVERNANCE_ADOPTION")

if (
    gov["governance_adoption_authorized_by_this_record"]
    is not False
):
    fail("PREMATURE_GOVERNANCE_AUTHORIZATION")

for key, value in manifest[
    "explicit_non_authorizations"
].items():
    if value is not False:
        fail(
            "UNEXPECTED_AUTHORIZATION|"
            + key
        )

for key, value in manifest[
    "retired_verifier_policy"
].items():
    if value is not False:
        fail(
            "RETIRED_VERIFIER_RERUN_ALLOWED|"
            + key
        )

# Repository binding when executed from repository.
p = subprocess.run(
    [
        "git",
        "-C",
        str(REPO),
        "rev-parse",
        "HEAD:" + HANDOFF_REL,
    ],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    check=False,
)

if p.returncode == 0:
    if p.stdout.strip() != EXPECTED_HANDOFF_TREE:
        fail("HANDOFF_GIT_TREE")

if SUMS.is_file():
    for line in SUMS.read_text(
        encoding="utf-8"
    ).splitlines():

        if not line.strip():
            continue

        digest, rel = line.split(
            None,
            1,
        )

        rel = rel.strip().lstrip("*")

        if sha(HERE / rel) != digest:
            fail(
                "CHECKSUM|"
                + rel
            )

print("COMPLETED_RPR01_RPR08_HUMAN_REVIEW_RECORD_V1=PASS")
print("HUMAN_REVIEW_COMPLETED=YES")
print("RPR01_RPR08_PASS_COUNT=8")
print(
    "OVERALL_REVIEW_DECISION="
    "APPROVE_V4_LOSSLESSNESS_REQUIREMENT_PROVENANCE_BINDING_RESOLUTION_STUDY_V1"
)
print(
    "APPROVAL_SCOPE="
    "REQUIREMENT_IDENTITY_AND_SOURCE_PROVENANCE_ONLY"
)
print("REVIEWER_DECISION_SYNTHESIZED=NO")
print("STUDY_GOVERNANCE_ADOPTED=NO")
print("GOVERNANCE_ADOPTION_AUTHORIZED_BY_THIS_RECORD=NO")
print("POSITIVE_MAPPING_PROVEN=NO")
print("NEGATIVE_MAPPING_IMPOSSIBILITY_PROVEN=NO")
print("WHOLE_V4_EXHAUSTIVENESS_PROVEN=NO")
print("OPERATIONAL_MAPPING_AUTHORIZED=NO")
print("SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO")
print("CURL_JSON_AUTHORIZED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
print("RETIRED_A02_VERIFIERS_EXECUTED=NO")
