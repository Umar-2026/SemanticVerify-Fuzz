#!/usr/bin/env python3

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

def load(name):
    return json.loads((HERE / name).read_text(encoding="utf-8"))

def fail(msg):
    print("FAIL|" + msg)
    raise SystemExit(1)

assessment = load("01_requirement_bound_carrier_admissibility_assessment.v1.json")
domain = load("02_carrier_domain_accounting.v1.json")
gap = load("03_requirement_semantic_binding_gap.v1.json")
account = load("04_machine_readable_accounting.v1.json")
cons = load("07_decision0137_a02_consumption_record.v1.json")

if assessment["status"] != "AUTHOR_CANDIDATE":
    fail("STATUS")

if assessment["global_outcome"] != "FURTHER_EVIDENCE_REQUIRED":
    fail("OUTCOME")

if len(assessment["records"]) != 17:
    fail("REQUIREMENT_RECORD_COUNT")

if len({r["requirement_id"] for r in assessment["records"]}) != 17:
    fail("REQUIREMENT_ID_UNIQUENESS")

for r in assessment["records"]:
    if r["carrier_classification"] != "UNRESOLVED":
        fail("CARRIER_CLASSIFICATION")
    if r["exact_carrier_witness"] is not None:
        fail("EXACT_WITNESS")
    if r["composite_carrier_witness"] != []:
        fail("COMPOSITE_WITNESS")
    if r["negative_requirement_specific_exhaustiveness_proven"] is not False:
        fail("NEGATIVE_EXHAUSTIVENESS")
    if r["historical_pair_reclassification_performed"] is not False:
        fail("PAIR_RECLASSIFICATION")

if domain["semantic_unit_count"] != 109:
    fail("UNIT_COUNT")

if domain["schema_v2_property_path_count"] != 171:
    fail("PATH_COUNT")

if domain["historical_pair_count"] != 18639:
    fail("PAIR_COUNT")

if domain["historical_pair_direct_requirement_binding_rows"] != 0:
    fail("DIRECT_REQUIREMENT_BINDING")

if domain["requirement_level_results"]["UNRESOLVED"] != 17:
    fail("UNRESOLVED_COUNT")

if gap["finding"] != "NO_AUTHORIZED_REQUIREMENT_TO_SEMANTIC_UNIT_CROSSWALK_IDENTIFIED":
    fail("BINDING_GAP")

if account["global_outcome"] != "FURTHER_EVIDENCE_REQUIRED":
    fail("ACCOUNT_OUTCOME")

if account["requirement_to_semantic_unit_crosswalk_identified"] is not False:
    fail("CROSSWALK_STATE")

if account["technical_nonclaims"]["carrier_admissibility_resolved"] is not False:
    fail("CARRIER_RESOLUTION_STATE")

for key in (
    "schema_v2_losslessness_proven",
    "positive_mapping_proven",
    "negative_mapping_impossibility_proven",
    "whole_v4_exhaustiveness_proven",
):
    if account["technical_nonclaims"][key] is not False:
        fail("TECHNICAL_NONCLAIM|" + key)

for key, value in account["governance_non_authorizations"].items():
    if value is not False:
        fail("NONAUTHORIZATION|" + key)

if cons["final_run_result"] != "PASS":
    fail("A02_RESULT")

if cons["verifier_state_after_run"] != "PERMANENTLY_RETIRED":
    fail("A02_STATE")

if cons["rerun_authorized"] is not False:
    fail("A02_RERUN_POLICY")

if cons["must_never_be_rerun"] is not True:
    fail("A02_RETIREMENT_POLICY")

a02_out = HERE / "06_decision0137_a02_final_output.EXACT_COPY.v1.txt"

if hashlib.sha256(a02_out.read_bytes()).hexdigest() != cons["final_output_sha256"]:
    fail("A02_OUTPUT_SHA")

if "REQUIREMENT_BOUND_CARRIER_ADMISSIBILITY_RESOLUTION_STUDY_V1_AUTHORIZATION=PASS" not in a02_out.read_text(encoding="utf-8"):
    fail("A02_PASS_MARKER")

sums = HERE / "09_requirement_bound_carrier_admissibility_resolution_study.v1.SHA256SUMS"

if sums.exists():
    for line in sums.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        digest, rel = line.split(None, 1)
        rel = rel.strip().lstrip("*")
        actual = hashlib.sha256((HERE / rel).read_bytes()).hexdigest()
        if actual != digest:
            fail("CHECKSUM|" + rel)

print("REQUIREMENT_BOUND_CARRIER_ADMISSIBILITY_RESOLUTION_STUDY_V1=PASS")
print("STUDY_STATUS=AUTHOR_CANDIDATE")
print("REQUIREMENT_COUNT=17")
print("SEMANTIC_UNIT_COUNT=109")
print("SCHEMA_V2_PROPERTY_PATH_COUNT=171")
print("HISTORICAL_PAIR_COUNT=18639")
print("REQUIREMENT_TO_SEMANTIC_UNIT_CROSSWALK_IDENTIFIED=NO")
print("ADMISSIBLE_EXACT_COUNT=0")
print("ADMISSIBLE_COMPOSITE_COUNT=0")
print("NO_ADMISSIBLE_CARRIER_PROVEN_COUNT=0")
print("UNRESOLVED_COUNT=17")
print("STUDY_OUTCOME=FURTHER_EVIDENCE_REQUIRED")
print("HISTORICAL_PAIR_STATE_MODIFIED=NO")
print("CARRIER_ADMISSIBILITY_RESOLVED=NO")
print("POSITIVE_MAPPING_PROVEN=NO")
print("NEGATIVE_MAPPING_IMPOSSIBILITY_PROVEN=NO")
print("WHOLE_V4_EXHAUSTIVENESS_PROVEN=NO")
print("OPERATIONAL_MAPPING_AUTHORIZED=NO")
print("SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO")
print("CURL_JSON_AUTHORIZED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
print("DECISION_0137_A02_STATE=PERMANENTLY_RETIRED")
print("DECISION_0137_A02_EXECUTED_BY_SAFE_VERIFIER=NO")
print("INDEPENDENT_HUMAN_REVIEW_REQUIRED=YES")
