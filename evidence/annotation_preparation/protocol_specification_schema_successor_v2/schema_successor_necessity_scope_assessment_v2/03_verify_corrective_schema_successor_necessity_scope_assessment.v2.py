#!/usr/bin/env python3

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

ASSESS = HERE / \
    "01_corrective_schema_successor_necessity_scope_assessment.v2.json"

def fail(msg):
    print("FAIL|" + msg)
    raise SystemExit(1)

if not ASSESS.is_file():
    fail("ASSESSMENT_V2_MISSING")

a = json.loads(
    ASSESS.read_text(encoding="utf-8")
)

if a["status"] != \
   "AUTHOR_CORRECTIVE_ASSESSMENT_CANDIDATE_AWAITING_INDEPENDENT_HUMAN_TECHNICAL_REVIEW":
    fail("STATUS")

pred = a["predecessor"]

if pred[
    "historical_author_candidate_conclusion"
] != "SCHEMA_SUCCESSOR_REQUIRED":
    fail("HISTORICAL_V1_CONCLUSION")

if pred[
    "historical_author_candidate_conclusion_human_approved"
] is not False:
    fail("HISTORICAL_V1_APPROVAL")

if pred["human_review_overall"] != "REVISION_REQUIRED":
    fail("V1_REVIEW_OVERALL")

if pred["must_remain_immutable"] is not True:
    fail("V1_IMMUTABILITY")

if pred["modified_in_place"] is not False:
    fail("V1_EDIT_STATE")

binding = a["human_review_binding"]

expected = {
    "SR01": "PASS",
    "SR02": "REVISION_REQUIRED",
    "SR03": "PASS",
    "SR04": "PASS",
    "SR05": "PASS",
    "SR06": "PASS",
    "SR07": "REVISION_REQUIRED",
    "SR08": "REVISION_REQUIRED",
}

for key, value in expected.items():
    if binding[key] != value:
        fail("REVIEW_BINDING|" + key)

sr02 = a["CV2_SR02_correction"]["corrected_distinction"]

if sr02["proposition_A_supported"] is not True:
    fail("PROPOSITION_A")

if sr02["proposition_B_supported"] is not False:
    fail("PROPOSITION_B")

if sr02[
    "proposition_A_does_not_entail_proposition_B"
] is not True:
    fail("A_NOT_ENTAIL_B")

if a[
    "CV2_SR02_correction"
]["semantically_related_multifield_schema_v2_compositions_exhaustively_assessed"] is not False:
    fail("EXHAUSTIVE_MULTIFIELD_STATE")

if a[
    "CV2_SR02_correction"
]["exhaustive_existing_v2_capability_study_authorized_by_decision_0078"] is not False:
    fail("EXHAUSTIVE_STUDY_AUTH")

sr07 = a["CV2_SR07_correction"]

if sr07[
    "positive_mapping_authoring_precedes_successor_activation"
] is not True:
    fail("MAPPING_ORDER")

if sr07[
    "complete_roundtrip_machine_check_precedes_successor_activation"
] is not True:
    fail("ROUNDTRIP_ORDER")

if sr07[
    "independent_mapping_and_roundtrip_review_precedes_successor_activation"
] is not True:
    fail("REVIEW_ORDER")

if sr07[
    "curl_json_materialization_after_activation_and_separate_authorization"
] is not True:
    fail("CURL_ORDER")

sr08 = a["CV2_SR08_correction"]

if sr08["selected_outcome"] != "FURTHER_EVIDENCE_REQUIRED":
    fail("CORRECTED_OUTCOME")

if sr08[
    "schema_successor_required_may_be_reconsidered_only_after_separately_authorized_new_evidence"
] is not True:
    fail("FUTURE_RECONSIDERATION_BOUNDARY")

current = a["current_governance_conclusion"]

if current["selected_outcome"] != "FURTHER_EVIDENCE_REQUIRED":
    fail("CURRENT_OUTCOME")

if current[
    "schema_successor_required_human_approved"
] is not False:
    fail("SUCCESSOR_REQUIRED_APPROVAL")

if current[
    "schema_successor_authoring_justified_now"
] is not False:
    fail("SUCCESSOR_AUTHORING_JUSTIFICATION")

if current[
    "positive_existing_v2_mapping_proven"
] is not False:
    fail("POSITIVE_V2_MAPPING_STATE")

review = a["human_review_state"]

if review[
    "corrective_v2_independent_human_technical_review_completed"
] is not False:
    fail("V2_HUMAN_REVIEW_STATE")

if review["synthetic_reviewer_decision"] is not False:
    fail("SYNTHETIC_REVIEW")

for key, value in a["explicit_non_authorizations"].items():
    if value is not False:
        fail("NONAUTH|" + key)

print("CORRECTIVE_ASSESSMENT_V2_STATUS=AUTHOR_CANDIDATE")
print("PREDECESSOR_ASSESSMENT_V1_IMMUTABLE=YES")
print("PREDECESSOR_V1_HUMAN_DECISION=REVISION_REQUIRED")

print("SR02_CORRECTION=PASS")
print("NO_PROVEN_V2_MAPPING_DOES_NOT_EQUAL_NO_POSSIBLE_ADMISSIBLE_V2_MAPPING=YES")
print("EXHAUSTIVE_ADMISSIBLE_V2_MULTIFIELD_CAPABILITY_ARGUMENT_AVAILABLE=NO")

print("SR07_CORRECTION=PASS")
print("POSITIVE_MAPPING_BEFORE_SUCCESSOR_ACTIVATION=YES")
print("EXACT_ROUNDTRIP_REVIEW_BEFORE_SUCCESSOR_ACTIVATION=YES")

print("SR08_CORRECTION=PASS")
print("CORRECTIVE_ASSESSMENT_V2_SELECTED_OUTCOME=FURTHER_EVIDENCE_REQUIRED")

print("SCHEMA_SUCCESSOR_REQUIRED_HUMAN_APPROVED=NO")
print("SCHEMA_SUCCESSOR_AUTHORING_JUSTIFIED_NOW=NO")

print("HISTORICAL_SR01_SR03_SR04_SR05_SR06_PASS_RESULTS_PRESERVED=YES")
print("CORRECTIVE_V2_INDEPENDENT_HUMAN_REVIEW_COMPLETED=NO")
print("SYNTHETIC_REVIEWER_DECISION=NO")

print("EXHAUSTIVE_V2_CAPABILITY_STUDY_AUTHORIZED=NO")
print("SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO")
print("SCHEMA_VERSION_PRESELECTED=NO")
print("POSITIVE_MAPPING_AUTHORIZED=NO")
print("CURL_JSON_CREATED=NO")

print("CORRECTIVE_SCHEMA_SUCCESSOR_NECESSITY_SCOPE_ASSESSMENT_V2=PASS")
