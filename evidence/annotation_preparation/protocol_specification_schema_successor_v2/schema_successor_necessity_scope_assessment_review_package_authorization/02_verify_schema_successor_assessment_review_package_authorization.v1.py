#!/usr/bin/env python3

import json
import subprocess
from pathlib import Path

REPO = Path(
    "/openbayes/home/semanticverify-fuzz-research"
)

HERE = Path(__file__).resolve().parent

AUTH = HERE / \
    "01_schema_successor_assessment_review_package_authorization.v1.json"

ASSESS_DIR = (
    REPO
    / "evidence/annotation_preparation/protocol_specification_schema_successor_v2"
    / "schema_successor_necessity_scope_assessment_v1"
)

ASSESS_VERIFY = ASSESS_DIR / \
    "03_verify_schema_successor_necessity_scope_assessment.v1.py"

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
] != "PRE_REVIEW_PACKAGE_AUTHORING_ONLY":
    fail("AUTHORIZATION_TYPE")

if a[
    "status"
] != "AUTHORIZED_TO_AUTHOR_INDEPENDENT_HUMAN_TECHNICAL_REVIEW_PACKAGE_FOR_ASSESSMENT_V1_ONLY":
    fail("STATUS")

subprocess.run(
    [
        "python3",
        str(ASSESS_VERIFY),
    ],
    check=True,
    stdout=subprocess.DEVNULL,
)

subject = a[
    "review_subject"
]

if subject[
    "assessment_status"
] != "AUTHOR_ASSESSMENT_CANDIDATE_AWAITING_INDEPENDENT_HUMAN_TECHNICAL_REVIEW":
    fail("ASSESSMENT_STATUS")

candidate = a[
    "author_candidate_conclusion"
]

if candidate[
    "selected_outcome"
] != "SCHEMA_SUCCESSOR_REQUIRED":
    fail("AUTHOR_CANDIDATE_CONCLUSION")

if candidate[
    "reviewer_must_independently_evaluate"
] is not True:
    fail("INDEPENDENT_REVIEW_REQUIREMENT")

if candidate[
    "author_conclusion_must_not_be_treated_as_human_approval"
] is not True:
    fail("AUTHOR_CONCLUSION_BOUNDARY")

required_items = a[
    "mandatory_review_items"
]

if set(required_items) != {
    "SR01",
    "SR02",
    "SR03",
    "SR04",
    "SR05",
    "SR06",
    "SR07",
    "SR08",
}:
    fail("MANDATORY_REVIEW_ITEM_SET")

if len(required_items) != 8:
    fail("MANDATORY_REVIEW_ITEM_COUNT")

if set(
    a["allowed_item_decisions"]
) != {
    "PASS",
    "REVISION_REQUIRED",
    "FAIL",
}:
    fail("ITEM_DECISION_SET")

if set(
    a["allowed_overall_decisions"]
) != {
    "APPROVE_SCHEMA_SUCCESSOR_NECESSITY_SCOPE_ASSESSMENT",
    "REVISION_REQUIRED",
    "FAIL",
}:
    fail("OVERALL_DECISION_SET")

requirements = a[
    "review_requirements"
]

if requirements[
    "independent_human_technical_reviewer_required"
] is not True:
    fail("HUMAN_REVIEW_REQUIRED")

if requirements[
    "synthetic_reviewer_decision_allowed"
] is not False:
    fail("SYNTHETIC_REVIEW_ALLOWED")

if requirements[
    "reviewer_packet_must_be_initially_blank"
] is not True:
    fail("INITIAL_BLANK_REQUIRED")

if requirements[
    "initial_blank_state_verifier_maximum_successful_runs"
] != 1:
    fail("BLANK_VERIFIER_RUN_COUNT")

target = REPO / a[
    "authorized_review_package"
]["target_path"]

if target.exists():
    fail("REVIEW_PACKAGE_ALREADY_EXISTS")

for key, value in a[
    "explicit_non_authorizations"
].items():
    if value is not False:
        fail("NONAUTH|" + key)

for key, value in a[
    "retired_verifier_constraints"
].items():
    if value is not False:
        fail("RETIRED_VERIFIER|" + key)

for forbidden in (
    "config/protocol_specifications/curl.json",
    "config/annotation/curl_positive_v4_to_v2_mapping_contract.v1.json",
    "config/schemas/protocol_specification.v3.schema.json",
):
    if (
        REPO /
        forbidden
    ).exists():
        fail(
            "FORBIDDEN_ARTIFACT|"
            + forbidden
        )

print("IMMUTABLE_ASSESSMENT_V1_BINDING=PASS")
print("ASSESSMENT_STATUS=AUTHOR_CANDIDATE")
print("AUTHOR_CANDIDATE_CONCLUSION=SCHEMA_SUCCESSOR_REQUIRED")
print("AUTHOR_CANDIDATE_CONCLUSION_IS_HUMAN_APPROVAL=NO")
print("MANDATORY_REVIEW_ITEM_COUNT=8")
print("SR01_TO_SR08_DEFINED=YES")
print("INDEPENDENT_HUMAN_TECHNICAL_REVIEW_REQUIRED=YES")
print("SYNTHETIC_REVIEWER_DECISION_ALLOWED=NO")
print("ASSESSMENT_MODIFICATION_AUTHORIZED=NO")
print("SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO")
print("SCHEMA_VERSION_PRESELECTED=NO")
print("POSITIVE_MAPPING_AUTHORIZED=NO")
print("CURL_JSON_CREATED=NO")
print("DECISION_0075_ASSESSMENT_REVIEW_PACKAGE_AUTHORIZATION=PASS")
print("IMPORTANT=THIS_VERIFIER_IS_PRE_REVIEW_PACKAGE_AUTHORING_ONLY")
