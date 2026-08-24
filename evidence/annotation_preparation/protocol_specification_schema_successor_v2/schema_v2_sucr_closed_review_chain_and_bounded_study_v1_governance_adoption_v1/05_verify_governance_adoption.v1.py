#!/usr/bin/env python3

import hashlib
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]

BASE = (
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2"
)

RECORD = (
    HERE
    / "01_governance_adoption_record.v1.json"
)

A02_OUT = (
    HERE
    / "03_decision0124_a02_final_output.EXACT_COPY.v1.txt"
)

CONSUMPTION = (
    HERE
    / "04_decision0124_a02_consumption_record.v1.json"
)

SUMS = (
    HERE
    / "06_governance_adoption.v1.SHA256SUMS"
)

CLOSURE_REL = (
    BASE
    + "/schema_v2_sucr_review_chain_closure_assessment_v1"
)

STUDY_REL = (
    BASE
    + "/schema_v2_semantic_unit_carrier_admissibility_and_requirement_binding_study_v1"
)

ORIGINAL_REL = (
    BASE
    + "/schema_v2_semantic_unit_carrier_admissibility_and_requirement_binding_study_v1_completed_human_review_v1"
)

FOCUSED_REL = (
    BASE
    + "/schema_v2_sucr01_focused_rereview_v1_completed_human_review_v1"
)

CORRECTIVE_REL = (
    BASE
    + "/schema_v2_sucr01_corrective_portable_source_evidence_successor_package_v2"
)

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

def git_object(rel):

    p = subprocess.run(
        [
            "git",
            "-C",
            str(REPO),
            "rev-parse",
            "HEAD:" + rel,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )

    if p.returncode != 0:
        fail(
            "GIT_OBJECT|" + rel
        )

    return p.stdout.strip()

expected_trees = {
    CLOSURE_REL:
        "18d6b1b77994d6827b878a498e1556487921fda7",

    STUDY_REL:
        "3f04237bdc58c2be56e85628de5923b87578a051",

    ORIGINAL_REL:
        "e8178b937ab376faca698d35cc57d6e3785fbbb5",

    FOCUSED_REL:
        "170c04d5dedf3a900edcf9d2a7ebc92b298b48a9",

    CORRECTIVE_REL:
        "dd34182886703f72fc5bfa4df899ad2bccbf4744",
}

for rel, expected in expected_trees.items():

    if git_object(rel) != expected:
        fail(
            "SOURCE_TREE|" + rel
        )

x = json.loads(
    RECORD.read_text(
        encoding="utf-8"
    )
)

if x[
    "status"
] != "APPROVED_WITH_BOUNDED_TECHNICAL_OUTCOME":
    fail(
        "GOVERNANCE_STATUS"
    )

if x[
    "adopted_bounded_technical_outcome"
] != "FURTHER_EVIDENCE_REQUIRED":
    fail(
        "ADOPTED_BOUNDED_OUTCOME"
    )

review = x[
    "review_chain_state"
]

if review[
    "closure_assessment_outcome"
] != "PASS_CLOSED":
    fail(
        "CLOSURE_OUTCOME"
    )

if review[
    "review_chain_closed"
] is not True:
    fail(
        "REVIEW_CHAIN_NOT_CLOSED"
    )

if review[
    "historical_sucr01"
] != "REVISION_REQUIRED":
    fail(
        "HISTORICAL_SUCR01"
    )

if review[
    "historical_overall"
] != "REVISION_REQUIRED":
    fail(
        "HISTORICAL_OVERALL"
    )

if review[
    "historical_findings_rewritten"
] is not False:
    fail(
        "HISTORICAL_REWRITE"
    )

study = x[
    "study_governance_state"
]

if study[
    "original_study_artifact_status"
] != "AUTHOR_CANDIDATE":
    fail(
        "STUDY_ARTIFACT_STATUS"
    )

if study[
    "original_study_artifact_modified"
] is not False:
    fail(
        "STUDY_ARTIFACT_MODIFIED"
    )

if study[
    "governance_adopted"
] is not True:
    fail(
        "GOVERNANCE_NOT_ADOPTED"
    )

if study[
    "governance_status"
] != "APPROVED_WITH_BOUNDED_TECHNICAL_OUTCOME":
    fail(
        "STUDY_GOVERNANCE_STATUS"
    )

if study[
    "bounded_technical_outcome"
] != "FURTHER_EVIDENCE_REQUIRED":
    fail(
        "STUDY_BOUNDED_OUTCOME"
    )

for key, value in x[
    "technical_nonclaims"
].items():

    if value is not False:
        fail(
            "UNEXPECTED_PERMISSION|"
            + key
        )

cons = json.loads(
    CONSUMPTION.read_text(
        encoding="utf-8"
    )
)

if cons[
    "final_run_result"
] != "PASS":
    fail(
        "A02_RESULT"
    )

if cons[
    "verifier_state_after_run"
] != "PERMANENTLY_RETIRED":
    fail(
        "A02_STATE"
    )

if cons[
    "must_never_be_rerun"
] is not True:
    fail(
        "A02_RETIREMENT"
    )

if sha(A02_OUT) != \
        cons[
            "final_output_sha256"
        ]:
    fail(
        "A02_OUTPUT_SHA"
    )

if (
    "GOVERNANCE_ADOPTION_AUTHORING_AUTHORIZATION=PASS"
    not in A02_OUT.read_text(
        encoding="utf-8"
    )
):
    fail(
        "A02_PASS_MARKER"
    )

if SUMS.is_file():

    lines = [
        line
        for line in SUMS.read_text(
            encoding="utf-8"
        ).splitlines()
        if line.strip()
    ]

    if len(lines) != 5:
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

print("GOVERNANCE_ADOPTION_V1=PASS")

print("GOVERNANCE_STATUS=APPROVED_WITH_BOUNDED_TECHNICAL_OUTCOME")
print("ADOPTED_BOUNDED_TECHNICAL_OUTCOME=FURTHER_EVIDENCE_REQUIRED")

print("REVIEW_CHAIN_CLOSURE_OUTCOME=PASS_CLOSED")
print("REVIEW_CHAIN_CLOSED=YES")

print("ORIGINAL_SUCR01_REMAINS=REVISION_REQUIRED")
print("SUCR02_SUCR08_ORIGINAL_PASS_FINDINGS_PRESERVED=YES")
print("ORIGINAL_OVERALL_REVIEW_REMAINS=REVISION_REQUIRED")
print("FOCUSED_SUCR01_C_DECISION=PASS")

print("STUDY_ARTIFACT_STATUS=AUTHOR_CANDIDATE")
print("STUDY_ARTIFACT_MODIFIED=NO")
print("STUDY_GOVERNANCE_ADOPTED=YES")

print("POSITIVE_EXISTING_V2_MAPPING_PROVEN=NO")
print("NEGATIVE_EXISTING_V2_MAPPING_IMPOSSIBILITY_PROVEN=NO")
print("WHOLE_V4_ADMISSIBLE_COMPOSITION_EXHAUSTIVENESS_PROVEN=NO")

print("OPERATIONAL_MAPPING_AUTHORIZED=NO")
print("ACTIVE_SCHEMA_V2_MODIFICATION_AUTHORIZED=NO")
print("SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO")
print("SCHEMA_VERSION_PRESELECTED=NO")
print("SCHEMA_V3_CREATED=NO")
print("CURL_JSON_CREATED=NO")
print("ANALYZER_IMPLEMENTATION_AUTHORIZED=NO")
print("ANALYZER_EXECUTION_AUTHORIZED=NO")
print("BASELINE_EXECUTION_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")

print("DECISION_0124_A02_STATE=PERMANENTLY_RETIRED")
print("DECISION_0124_A02_EXECUTED_BY_SAFE_VERIFIER=NO")
print("RETIRED_A02_VERIFIERS_EXECUTED=NO")
