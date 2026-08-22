#!/usr/bin/env python3

import hashlib
import json
import subprocess
from pathlib import Path

REPO = Path(
    "/openbayes/home/semanticverify-fuzz-research"
)

HERE = Path(__file__).resolve().parent

AUTH = HERE / \
    "01_schema_successor_necessity_scope_assessment_authorization.v1.json"

REREVIEW_RECORD = (
    REPO
    / "evidence/annotation_preparation/protocol_specification_schema_successor_v2"
    / "schema_v2_residual_losslessness_insufficiency_focused_ri01_rereview_v1"
)

REREVIEW_VERIFY = REREVIEW_RECORD / \
    "03_verify_completed_focused_RI01_C_human_rereview.v1.py"

def fail(msg):
    print("FAIL|" + msg)
    raise SystemExit(1)

record = json.loads(
    AUTH.read_text(
        encoding="utf-8"
    )
)

if record[
    "authorization_type"
] != "PRE_ASSESSMENT_AUTHORING_ONLY":
    fail("AUTHORIZATION_TYPE")

if record[
    "status"
] != "AUTHORIZED_TO_AUTHOR_SCHEMA_SUCCESSOR_NECESSITY_SCOPE_ASSESSMENT_V1_ONLY":
    fail("STATUS")

subprocess.run(
    [
        "python3",
        str(REREVIEW_VERIFY),
    ],
    check=True,
    stdout=subprocess.DEVNULL,
)

chain = record[
    "review_chain_state"
]

if chain[
    "historical_first_round_overall_decision"
] != "REVISION_REQUIRED":
    fail("HISTORICAL_OVERALL_DECISION")

if chain[
    "historical_first_round_overall_decision_must_not_be_rewritten"
] is not True:
    fail("HISTORICAL_DECISION_PROTECTION")

if chain[
    "RI01_corrective"
] != "PASS":
    fail("RI01_CORRECTIVE")

if chain[
    "RI02_to_RI08"
] != "PASS_CLOSED":
    fail("RI02_TO_RI08")

if chain[
    "all_RI01_to_RI08_review_items_pass_closed"
] is not True:
    fail("ALL_REVIEW_ITEMS")

if chain[
    "synthetic_overall_reviewer_approval_allowed"
] is not False:
    fail("SYNTHETIC_OVERALL_APPROVAL")

assessment = record[
    "authorized_assessment"
]

if assessment[
    "assessment_only"
] is not True:
    fail("ASSESSMENT_ONLY")

if assessment[
    "schema_successor_authoring"
] is not False:
    fail("SUCCESSOR_AUTHORING")

if assessment[
    "schema_version_name_or_number_preselected"
] is not False:
    fail("VERSION_PRESELECTED")

mandatory = record[
    "mandatory_assessment_items"
]

expected_ids = {
    "SA01",
    "SA02",
    "SA03",
    "SA04",
    "SA05",
    "SA06",
    "SA07",
    "SA08",
}

if set(mandatory) != expected_ids:
    fail("MANDATORY_ASSESSMENT_ITEM_SET")

gap = record[
    "mandatory_residual_gap_scope"
]

if gap[
    "enforcement_field_coverage"
] != "64_OF_64_V4_RULE_RECORDS":
    fail("ENFORCEMENT_COVERAGE")

if gap[
    "distinct_enforcement_values"
] != 15:
    fail("ENFORCEMENT_VALUE_COUNT")

if gap[
    "explicit_schema_v2_enforcement_carrier"
] is not False:
    fail("ENFORCEMENT_CARRIER_STATE")

if gap[
    "other_unproven_field_level_mappings_must_remain_in_scope"
] is not True:
    fail("OTHER_FIELDS_SCOPE")

if gap[
    "unit_accountability_must_not_be_treated_as_field_level_losslessness"
] is not True:
    fail("ACCOUNTING_BOUNDARY")

for key, value in record[
    "explicit_non_authorizations"
].items():
    if value is not False:
        fail("NONAUTH|" + key)

for key, value in record[
    "retired_verifier_constraints"
].items():
    if value is not False:
        fail("RETIRED_VERIFIER|" + key)

target = REPO / assessment[
    "target_path"
]

if target.exists():
    fail("ASSESSMENT_ALREADY_EXISTS")

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

print("COMPLETED_FOCUSED_RI01_REREVIEW_RECORD=PASS")
print("RI01_CORRECTIVE_DECISION=PASS")
print("RI01_CORRECTIVE_DEFICIENCY_CLOSED=YES")
print("RI02_TO_RI08_PASS_CLOSED=YES")
print("ALL_RI01_TO_RI08_REVIEW_ITEMS_NOW_PASS_CLOSED=YES")
print("HISTORICAL_FIRST_ROUND_OVERALL_DECISION=REVISION_REQUIRED")
print("SYNTHETIC_OVERALL_REVIEWER_APPROVAL_CREATED=NO")
print("SCHEMA_SUCCESSOR_NECESSITY_SCOPE_ASSESSMENT_AUTHORIZED=YES")
print("MANDATORY_ASSESSMENT_ITEM_COUNT=8")
print("SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO")
print("SCHEMA_VERSION_PRESELECTED=NO")
print("POSITIVE_MAPPING_AUTHORIZED=NO")
print("CURL_JSON_CREATED=NO")
print("DECISION_0073_SCHEMA_SUCCESSOR_ASSESSMENT_AUTHORIZATION=PASS")
print("IMPORTANT=THIS_VERIFIER_IS_PRE_ASSESSMENT_AUTHORING_ONLY")
