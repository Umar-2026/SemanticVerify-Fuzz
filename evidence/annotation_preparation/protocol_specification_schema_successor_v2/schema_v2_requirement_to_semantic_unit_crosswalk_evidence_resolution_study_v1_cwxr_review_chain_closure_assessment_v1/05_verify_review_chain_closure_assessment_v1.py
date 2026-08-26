#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parent

C01 = ROOT / "01_review_chain_closure_assessment.v1.json"
C02 = ROOT / "02_review_chain_closure_assessment_report.v1.md"
C03 = ROOT / "03_decision0172_a02_final_output.EXACT_COPY.v1.txt"
C04 = ROOT / "04_decision0172_a02_consumption_record.v1.json"
C05 = ROOT / "05_verify_review_chain_closure_assessment_v1.py"
C06 = ROOT / "06_review_chain_closure_assessment_v1.SHA256SUMS"


def stop(msg):
    print("STOP|" + msg)
    sys.exit(1)


def sha256_file(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


for p in (C01, C02, C03, C04, C05, C06):
    if not p.is_file():
        stop("CLOSURE_ARTIFACT_MISSING|" + p.name)

entries = []

for line in C06.read_text(encoding="utf-8").splitlines():
    if not line.strip():
        continue

    m = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)

    if not m:
        stop("CHECKSUM_FORMAT_INVALID")

    entries.append((m.group(1), m.group(2)))

expected_names = {
    "01_review_chain_closure_assessment.v1.json",
    "02_review_chain_closure_assessment_report.v1.md",
    "03_decision0172_a02_final_output.EXACT_COPY.v1.txt",
    "04_decision0172_a02_consumption_record.v1.json",
    "05_verify_review_chain_closure_assessment_v1.py",
}

if len(entries) != 5:
    stop("CHECKSUM_ENTRY_COUNT_INVALID")

if {name for _, name in entries} != expected_names:
    stop("CHECKSUM_NAME_SET_INVALID")

for expected, name in entries:
    path = ROOT / name

    if not path.is_file():
        stop("CHECKSUM_TARGET_MISSING|" + name)

    if sha256_file(path) != expected:
        stop("CHECKSUM_MISMATCH|" + name)


assessment = json.loads(C01.read_text(encoding="utf-8"))

if assessment.get("artifact") != "cwxr_review_chain_closure_assessment_v1":
    stop("ASSESSMENT_ARTIFACT_INVALID")

if assessment.get("status") != (
    "PASS_CLOSED_WITH_BOUNDED_CWXR07_S2_SUCCESSOR"
):
    stop("ASSESSMENT_STATUS_INVALID")

original = assessment.get("historical_original_review", {})

expected_original = {
    "CWXR01": "PASS",
    "CWXR02": "PASS",
    "CWXR03": "PASS",
    "CWXR04": "PASS",
    "CWXR05": "PASS",
    "CWXR06": "PASS",
    "CWXR07": "REVISION_REQUIRED",
    "CWXR08": "PASS",
    "overall": "REVISION_REQUIRED",
}

for key, value in expected_original.items():
    if original.get(key) != value:
        stop("ORIGINAL_REVIEW_HISTORY_INVALID|" + key)

if original.get("modified") is not False:
    stop("ORIGINAL_REVIEW_MODIFIED")

if original.get("reopened") is not False:
    stop("ORIGINAL_REVIEW_REOPENED")

s1 = assessment.get("historical_cwxr07_s1", {})

if s1.get("decision") != "REVISION_REQUIRED":
    stop("S1_DECISION_INVALID")

if s1.get("modified") is not False:
    stop("S1_MODIFIED")

if s1.get("upgraded") is not False:
    stop("S1_UPGRADED")

s2 = assessment.get("cwxr07_s2", {})

if s2.get("decision") != "PASS":
    stop("S2_DECISION_INVALID")

if s2.get("separate_corrective_successor") is not True:
    stop("S2_NOT_SEPARATE_SUCCESSOR")

if s2.get("retroactively_changes_s1") is not False:
    stop("S2_RETROACTIVELY_CHANGES_S1")

if s2.get("retroactively_changes_original_review") is not False:
    stop("S2_RETROACTIVELY_CHANGES_ORIGINAL")

reason = assessment.get("closure_reasoning", {})

if reason.get(
    "original_cwxr07_deficiency_resolved_on_original_s1_scope"
) is not False:
    stop("ORIGINAL_S1_SCOPE_IMPROPERLY_DECLARED_RESOLVED")

if reason.get("historical_s1_deficiency_erased") is not False:
    stop("S1_HISTORY_IMPROPERLY_ERASED")

if reason.get("historical_original_revision_required_erased") is not False:
    stop("ORIGINAL_HISTORY_IMPROPERLY_ERASED")

if reason.get("chain_closed_for_governance_consideration") is not True:
    stop("CHAIN_NOT_CLOSED_FOR_GOVERNANCE_CONSIDERATION")

if assessment.get("review_chain_closed") is not True:
    stop("REVIEW_CHAIN_NOT_CLOSED")

if assessment.get("closure_outcome") != (
    "PASS_CLOSED_WITH_BOUNDED_CWXR07_S2_SUCCESSOR"
):
    stop("CLOSURE_OUTCOME_INVALID")

nonclaims = assessment.get("bounded_nonclaims", {})

for key, value in nonclaims.items():
    if value is not False:
        stop("BOUNDED_NONCLAIM_VIOLATED|" + key)

a02 = assessment.get("decision0172_a02", {})

if a02.get("execution_count_in_decision0173_transaction") != 1:
    stop("A02_EXECUTION_COUNT_INVALID")

if a02.get("state") != "PERMANENTLY_RETIRED":
    stop("A02_LIFECYCLE_INVALID")

if a02.get("rerun_authorized") is not False:
    stop("A02_RERUN_BOUNDARY_INVALID")

consumption = json.loads(C04.read_text(encoding="utf-8"))

if consumption.get("execution_count_in_decision0173_transaction") != 1:
    stop("CONSUMPTION_EXECUTION_COUNT_INVALID")

if consumption.get("return_code") != 0:
    stop("CONSUMPTION_RETURN_CODE_INVALID")

if consumption.get("pass_marker_present") is not True:
    stop("CONSUMPTION_PASS_MARKER_INVALID")

if consumption.get("lifecycle_after_execution") != "PERMANENTLY_RETIRED":
    stop("CONSUMPTION_LIFECYCLE_INVALID")

if consumption.get("rerun_authorized") is not False:
    stop("CONSUMPTION_RERUN_INVALID")

if consumption.get("other_a02_executed_in_this_transaction") is not False:
    stop("OTHER_A02_EXECUTED")

if consumption.get(
    "global_no_rerun_fact_independently_certified"
) is not False:
    stop("GLOBAL_NO_RERUN_OVERCLAIM")

a02_output = C03.read_text(encoding="utf-8").splitlines()

if "DECISION0172_A02_RESULT=PASS" not in a02_output:
    stop("DECISION0172_A02_PASS_MARKER_MISSING")

if assessment.get("study_governance_adopted") is not False:
    stop("GOVERNANCE_ALREADY_ADOPTED")

if assessment.get("governance_adoption_authorized") is not False:
    stop("GOVERNANCE_PREMATURELY_AUTHORIZED")

if assessment.get("analyzer_authorized") is not False:
    stop("ANALYZER_BOUNDARY_INVALID")

if assessment.get("baseline_authorized") is not False:
    stop("BASELINE_BOUNDARY_INVALID")

if assessment.get("repair_authorized") is not False:
    stop("REPAIR_BOUNDARY_INVALID")

print("CWXR_REVIEW_CHAIN_CLOSURE_ASSESSMENT_V1=PASS")
print("REVIEW_CHAIN_CLOSURE_ASSESSMENT_OUTCOME=PASS_CLOSED_WITH_BOUNDED_CWXR07_S2_SUCCESSOR")
print("REVIEW_CHAIN_CLOSED=YES")
print("CWXR01_TO_CWXR06_AND_CWXR08_ORIGINAL_PASS_FINDINGS_PRESERVED=YES")
print("ORIGINAL_CWXR07_DECISION_REMAINS=REVISION_REQUIRED")
print("ORIGINAL_OVERALL_REVIEW_REMAINS=REVISION_REQUIRED")
print("HISTORICAL_CWXR07_S1_DECISION_REMAINS=REVISION_REQUIRED")
print("HISTORICAL_CWXR07_S1_UPGRADED=NO")
print("CWXR07_S2_DECISION=PASS")
print("CWXR07_S2_IS_SEPARATE_BOUNDED_SUCCESSOR=YES")
print("ORIGINAL_S1_SCOPE_DECLARED_RESOLVED=NO")
print("EXCLUDED_STRONGER_FACTS_INDEPENDENTLY_CERTIFIED=NO")
print("DECISION0172_A02_STATE=PERMANENTLY_RETIRED")
print("DECISION0172_A02_RERUN_AUTHORIZED=NO")
print("STUDY_GOVERNANCE_ADOPTED=NO")
print("GOVERNANCE_ADOPTION_AUTHORIZED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
print("CLOSURE_ASSESSMENT_SAFE_VERIFICATION=PASS")
