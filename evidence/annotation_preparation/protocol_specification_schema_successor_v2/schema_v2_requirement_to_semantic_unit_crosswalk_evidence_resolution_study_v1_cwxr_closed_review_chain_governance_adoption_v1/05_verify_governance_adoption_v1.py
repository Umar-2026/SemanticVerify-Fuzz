#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parent

G01 = ROOT / "01_governance_adoption.v1.json"
G02 = ROOT / "02_governance_adoption_report.v1.md"
G03 = ROOT / "03_decision0174_a02_final_output.EXACT_COPY.v1.txt"
G04 = ROOT / "04_decision0174_a02_consumption_record.v1.json"
G05 = ROOT / "05_verify_governance_adoption_v1.py"
G06 = ROOT / "06_governance_adoption_v1.SHA256SUMS"


def stop(msg):
    print("STOP|" + msg)
    sys.exit(1)


def sha256_file(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


for p in (G01, G02, G03, G04, G05, G06):
    if not p.is_file():
        stop("GOVERNANCE_ARTIFACT_MISSING|" + p.name)

entries = []

for line in G06.read_text(encoding="utf-8").splitlines():
    if not line.strip():
        continue

    m = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)

    if not m:
        stop("CHECKSUM_FORMAT_INVALID")

    entries.append((m.group(1), m.group(2)))

expected_names = {
    "01_governance_adoption.v1.json",
    "02_governance_adoption_report.v1.md",
    "03_decision0174_a02_final_output.EXACT_COPY.v1.txt",
    "04_decision0174_a02_consumption_record.v1.json",
    "05_verify_governance_adoption_v1.py",
}

if len(entries) != 5:
    stop("CHECKSUM_ENTRY_COUNT_INVALID")

if {name for _, name in entries} != expected_names:
    stop("CHECKSUM_NAME_SET_INVALID")

for expected, name in entries:
    p = ROOT / name

    if not p.is_file():
        stop("CHECKSUM_TARGET_MISSING|" + name)

    if sha256_file(p) != expected:
        stop("CHECKSUM_MISMATCH|" + name)


obj = json.loads(G01.read_text(encoding="utf-8"))

if obj.get("artifact") != \
        "cwxr_closed_review_chain_governance_adoption_v1":
    stop("ARTIFACT_ID_INVALID")

if obj.get("governance_status") != \
        "APPROVED_WITH_BOUNDED_TECHNICAL_OUTCOME":
    stop("GOVERNANCE_STATUS_INVALID")

if obj.get("adopted_bounded_technical_outcome") != \
        "FURTHER_EVIDENCE_REQUIRED":
    stop("BOUNDED_OUTCOME_INVALID")

chain = obj.get("adopted_review_chain", {})

if chain.get("review_chain_closed") is not True:
    stop("REVIEW_CHAIN_NOT_CLOSED")

if chain.get("closure_outcome") != \
        "PASS_CLOSED_WITH_BOUNDED_CWXR07_S2_SUCCESSOR":
    stop("CLOSURE_OUTCOME_INVALID")

for item in [
    "CWXR01", "CWXR02", "CWXR03", "CWXR04",
    "CWXR05", "CWXR06", "CWXR08"
]:
    if chain.get(item) != "PASS":
        stop("HISTORICAL_PASS_INVALID|" + item)

if chain.get("original_CWXR07") != "REVISION_REQUIRED":
    stop("ORIGINAL_CWXR07_INVALID")

if chain.get("original_overall_review") != "REVISION_REQUIRED":
    stop("ORIGINAL_OVERALL_INVALID")

if chain.get("historical_CWXR07_S1") != "REVISION_REQUIRED":
    stop("S1_HISTORY_INVALID")

if chain.get("CWXR07_S2") != "PASS":
    stop("S2_DECISION_INVALID")

if chain.get("CWXR07_S2_is_separate_bounded_successor") is not True:
    stop("S2_SUCCESSOR_BOUNDARY_INVALID")

if chain.get("historical_decisions_rewritten") is not False:
    stop("HISTORICAL_REVIEW_REWRITTEN")

if chain.get("historical_decisions_upgraded") is not False:
    stop("HISTORICAL_REVIEW_UPGRADED")

study = obj.get("adopted_study_v1", {})

if study.get("artifact_status") != "AUTHOR_CANDIDATE":
    stop("STUDY_STATUS_INVALID")

if study.get("artifact_modified") is not False:
    stop("STUDY_ARTIFACT_MODIFIED")

if study.get("requirement_count") != 17:
    stop("REQUIREMENT_COUNT_INVALID")

if study.get("semantic_unit_count") != 109:
    stop("SEMANTIC_UNIT_COUNT_INVALID")

if study.get("pair_universe_count") != 1853:
    stop("PAIR_UNIVERSE_COUNT_INVALID")

if study.get("supported_binding_count") != 0:
    stop("SUPPORTED_BINDING_COUNT_INVALID")

if study.get("not_supported_binding_count") != 0:
    stop("NOT_SUPPORTED_BINDING_COUNT_INVALID")

if study.get("unresolved_binding_count") != 1853:
    stop("UNRESOLVED_BINDING_COUNT_INVALID")

if study.get("unresolved_requirement_count") != 17:
    stop("UNRESOLVED_REQUIREMENT_COUNT_INVALID")

if study.get("bounded_technical_outcome") != "FURTHER_EVIDENCE_REQUIRED":
    stop("STUDY_BOUNDED_OUTCOME_INVALID")

bounded = obj.get("bounded_interpretation", {})

for key, value in bounded.items():
    if value is not False:
        stop("BOUNDED_NONCLAIM_VIOLATED|" + key)

if obj.get("governance_adoption_authorized") is not True:
    stop("GOVERNANCE_AUTHORIZATION_INVALID")

if obj.get("governance_adoption_authored") is not True:
    stop("GOVERNANCE_NOT_AUTHORED")

if obj.get("study_governance_adopted") is not True:
    stop("STUDY_NOT_GOVERNANCE_ADOPTED")

if obj.get("review_chain_governance_adopted") is not True:
    stop("CHAIN_NOT_GOVERNANCE_ADOPTED")

if obj.get("study_artifact_status") != "AUTHOR_CANDIDATE":
    stop("TOP_LEVEL_STUDY_STATUS_INVALID")

if obj.get("study_artifact_modified") is not False:
    stop("TOP_LEVEL_STUDY_MODIFIED")

for key in [
    "pair_reclassification_authorized",
    "historical_pair_reclassification_authorized",
    "operational_mapping_authorized",
    "schema_v2_modification_authorized",
    "schema_successor_authoring_authorized",
    "curl_json_authorized",
    "analyzer_implementation_authorized",
    "analyzer_execution_authorized",
    "baseline_execution_authorized",
    "repair_implementation_authorized",
    "repair_execution_authorized",
]:
    if obj.get(key) is not False:
        stop("OPERATIONAL_BOUNDARY_VIOLATED|" + key)

a02 = obj.get("decision0174_a02", {})

if a02.get("execution_count_in_decision0175_transaction") != 1:
    stop("A02_EXECUTION_COUNT_INVALID")

if a02.get("state") != "PERMANENTLY_RETIRED":
    stop("A02_STATE_INVALID")

if a02.get("rerun_authorized") is not False:
    stop("A02_RERUN_INVALID")

consumption = json.loads(G04.read_text(encoding="utf-8"))

if consumption.get("execution_count_in_decision0175_transaction") != 1:
    stop("CONSUMPTION_EXECUTION_COUNT_INVALID")

if consumption.get("return_code") != 0:
    stop("CONSUMPTION_RETURN_CODE_INVALID")

if consumption.get("pass_marker_present") is not True:
    stop("CONSUMPTION_PASS_MARKER_INVALID")

if consumption.get("lifecycle_after_execution") != "PERMANENTLY_RETIRED":
    stop("CONSUMPTION_STATE_INVALID")

if consumption.get("rerun_authorized") is not False:
    stop("CONSUMPTION_RERUN_INVALID")

if consumption.get("other_a02_executed_in_this_transaction") is not False:
    stop("OTHER_A02_EXECUTED")

if consumption.get(
    "global_no_rerun_fact_independently_certified"
) is not False:
    stop("GLOBAL_NO_RERUN_OVERCLAIM")

output = G03.read_text(encoding="utf-8").splitlines()

if "DECISION0174_A02_RESULT=PASS" not in output:
    stop("A02_PASS_MARKER_MISSING")

print("CWXR_CLOSED_CHAIN_GOVERNANCE_ADOPTION_V1=PASS")
print("GOVERNANCE_STATUS=APPROVED_WITH_BOUNDED_TECHNICAL_OUTCOME")
print("ADOPTED_BOUNDED_TECHNICAL_OUTCOME=FURTHER_EVIDENCE_REQUIRED")
print("REVIEW_CHAIN_CLOSED=YES")
print("CLOSURE_OUTCOME=PASS_CLOSED_WITH_BOUNDED_CWXR07_S2_SUCCESSOR")
print("CWXR01_TO_CWXR06_AND_CWXR08_ORIGINAL_PASS_FINDINGS_PRESERVED=YES")
print("ORIGINAL_CWXR07_REMAINS=REVISION_REQUIRED")
print("ORIGINAL_OVERALL_REVIEW_REMAINS=REVISION_REQUIRED")
print("HISTORICAL_CWXR07_S1_REMAINS=REVISION_REQUIRED")
print("CWXR07_S2=PASS")
print("CWXR07_S2_IS_SEPARATE_BOUNDED_SUCCESSOR=YES")
print("STUDY_ARTIFACT_STATUS=AUTHOR_CANDIDATE")
print("STUDY_ARTIFACT_MODIFIED=NO")
print("STUDY_GOVERNANCE_ADOPTED=YES")
print("REVIEW_CHAIN_GOVERNANCE_ADOPTED=YES")
print("SUPPORTED_BINDING_COUNT=0")
print("NOT_SUPPORTED_BINDING_COUNT=0")
print("UNRESOLVED_BINDING_COUNT=1853")
print("UNRESOLVED_REQUIREMENT_COUNT=17")
print("EXCLUDED_STRONGER_FACTS_INDEPENDENTLY_CERTIFIED=NO")
print("DECISION0174_A02_STATE=PERMANENTLY_RETIRED")
print("DECISION0174_A02_RERUN_AUTHORIZED=NO")
print("PAIR_RECLASSIFICATION_AUTHORIZED=NO")
print("OPERATIONAL_MAPPING_AUTHORIZED=NO")
print("SCHEMA_V2_MODIFICATION_AUTHORIZED=NO")
print("SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO")
print("CURL_JSON_AUTHORIZED=NO")
print("ANALYZER_IMPLEMENTATION_AUTHORIZED=NO")
print("ANALYZER_EXECUTION_AUTHORIZED=NO")
print("BASELINE_EXECUTION_AUTHORIZED=NO")
print("REPAIR_IMPLEMENTATION_AUTHORIZED=NO")
print("REPAIR_EXECUTION_AUTHORIZED=NO")
print("GOVERNANCE_ADOPTION_SAFE_VERIFICATION=PASS")
