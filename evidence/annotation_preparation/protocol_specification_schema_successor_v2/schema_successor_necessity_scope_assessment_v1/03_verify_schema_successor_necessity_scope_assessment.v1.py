#!/usr/bin/env python3

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

ASSESSMENT = HERE / \
    "01_schema_successor_necessity_scope_assessment.v1.json"

def fail(msg):
    print("FAIL|" + msg)
    raise SystemExit(1)

if not ASSESSMENT.is_file():
    fail("ASSESSMENT_MISSING")

a = json.loads(
    ASSESSMENT.read_text(
        encoding="utf-8"
    )
)

if a["status"] != \
   "AUTHOR_ASSESSMENT_CANDIDATE_AWAITING_INDEPENDENT_HUMAN_TECHNICAL_REVIEW":
    fail("STATUS")

if a[
    "claim_boundary"
]["abstract_information_theoretic_impossibility_claimed"] is not False:
    fail("OVERCLAIM_INFORMATION_THEORETIC")

if a[
    "claim_boundary"
]["claim_that_schema_v2_is_insufficient_for_the_reviewed_exact_v4_contract"] is not True:
    fail("BOUNDED_V2_INSUFFICIENCY")

basis = a["reviewed_basis"]

if basis[
    "all_RI01_to_RI08_review_items_pass_closed"
] is not True:
    fail("REVIEW_ITEMS_NOT_CLOSED")

if basis[
    "historical_first_round_overall_decision"
] != "REVISION_REQUIRED":
    fail("HISTORICAL_OVERALL_DECISION")

if basis[
    "historical_first_round_overall_decision_rewritten"
] is not False:
    fail("HISTORICAL_DECISION_REWRITTEN")

if basis[
    "focused_RI01_corrective_decision"
] != "PASS":
    fail("RI01_CORRECTIVE_STATE")

alternatives = a[
    "SA02_existing_schema_v2_alternative_assessment"
]

if alternatives[
    "proven_admissible_existing_v2_mapping_path_available"
] is not False:
    fail("UNEXPECTED_PROVEN_V2_MAPPING_PATH")

if alternatives[
    "alternative_B_derive_enforcement_from_existing_verdict_or_defect_verdict"
]["verdict_to_enforcement_ambiguous_group_count"] != 3:
    fail("VERDICT_AMBIGUITY")

if alternatives[
    "alternative_B_derive_enforcement_from_existing_verdict_or_defect_verdict"
]["defect_plus_verdict_to_enforcement_ambiguous_group_count"] != 4:
    fail("DEFECT_VERDICT_AMBIGUITY")

scope = a[
    "SA03_minimum_explicit_semantic_carrier_scope"
]

if scope[
    "must_preserve_enforcement_semantics"
]["source_rule_coverage"] != 64:
    fail("RULE_COVERAGE")

if len(
    scope[
        "must_preserve_enforcement_semantics"
    ]["distinct_source_values"]
) != 15:
    fail("ENFORCEMENT_VALUE_COUNT")

if len(
    scope[
        "must_preserve_three_representation_policy_assertions"
    ]
) != 3:
    fail("POLICY_ASSERTION_COUNT")

fields = a[
    "SA04_complete_field_level_scope"
]

if fields[
    "exit_obligation_count"
] != 3:
    fail("EXIT_OBLIGATION_COUNT")

if fields[
    "important"
].find(
    "must not be artificially narrowed"
) < 0:
    fail("FULL_FIELD_SCOPE_BOUNDARY")

accounting = a[
    "SA05_semantic_accounting_boundary"
]

if accounting[
    "semantic_accounting_alone_is_not_missing_semantic_storage"
] is not True:
    fail("ACCOUNTING_BOUNDARY")

compat = a[
    "SA06_backward_compatibility_and_migration"
]

for key in (
    "existing_zlib_schema_v1_specification_must_remain_unchanged",
    "existing_libpcap_schema_v1_specification_must_remain_unchanged",
    "active_schema_v2_artifacts_must_remain_historically_immutable",
    "successor_must_not_silently_reinterpret_existing_v1_or_v2_documents",
    "current_schema_v2_remains_active_until_separate_successor_activation",
):
    if compat[key] is not True:
        fail("BACKWARD_COMPATIBILITY|" + key)

sequence = a[
    "SA07_minimum_future_governance_sequence_if_successor_is_required"
]

if len(sequence) < 10:
    fail("GOVERNANCE_SEQUENCE_TOO_SHORT")

conclusion = a[
    "SA08_conclusion"
]

allowed = {
    "NO_SUCCESSOR_REQUIRED_WITH_PROVEN_ADMISSIBLE_V2_MAPPING_PATH",
    "SCHEMA_SUCCESSOR_REQUIRED",
    "FURTHER_EVIDENCE_REQUIRED",
}

if set(
    conclusion["allowed_outcomes"]
) != allowed:
    fail("ALLOWED_OUTCOME_SET")

if conclusion[
    "selected_outcome"
] != "SCHEMA_SUCCESSOR_REQUIRED":
    fail("ASSESSMENT_CONCLUSION")

if conclusion[
    "schema_successor_authoring_authorized_by_this_assessment"
] is not False:
    fail("SUCCESSOR_AUTHORING_AUTHORIZED")

if conclusion[
    "successor_version_number_preselected"
] is not False:
    fail("VERSION_PRESELECTED")

for key, value in a[
    "explicit_non_authorizations"
].items():
    if value is not False:
        fail("NONAUTH|" + key)

review = a[
    "human_review_state"
]

if review[
    "independent_human_technical_review_completed"
] is not False:
    fail("HUMAN_REVIEW_ALREADY_COMPLETED")

if review[
    "synthetic_reviewer_decision"
] is not False:
    fail("SYNTHETIC_REVIEW")

print("ASSESSMENT_STATUS=AUTHOR_CANDIDATE")
print("ALL_RI01_TO_RI08_REVIEW_ITEMS_PASS_CLOSED=YES")
print("PROVEN_ADMISSIBLE_EXISTING_V2_MAPPING_PATH_AVAILABLE=NO")
print("ENFORCEMENT_RULE_COVERAGE=64_OF_64")
print("DISTINCT_ENFORCEMENT_VALUES=15")
print("VERDICT_TO_ENFORCEMENT_AMBIGUOUS_GROUPS=3")
print("DEFECT_PLUS_VERDICT_TO_ENFORCEMENT_AMBIGUOUS_GROUPS=4")
print("UNRESOLVED_REPRESENTATION_POLICY_ASSERTIONS=3")
print("OTHER_RULE_AND_EXIT_FIELD_GAPS_REMAIN_IN_SCOPE=YES")
print("SEMANTIC_ACCOUNTING_ALONE_SUFFICIENT_FOR_LOSSLESSNESS=NO")
print("BACKWARD_COMPATIBILITY_REQUIREMENTS_DEFINED=YES")
print("ASSESSMENT_CONCLUSION=SCHEMA_SUCCESSOR_REQUIRED")
print("SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO")
print("SCHEMA_VERSION_PRESELECTED=NO")
print("INDEPENDENT_HUMAN_TECHNICAL_REVIEW_COMPLETED=NO")
print("SYNTHETIC_REVIEWER_DECISION=NO")
print("SCHEMA_SUCCESSOR_NECESSITY_SCOPE_ASSESSMENT_V1=PASS")
