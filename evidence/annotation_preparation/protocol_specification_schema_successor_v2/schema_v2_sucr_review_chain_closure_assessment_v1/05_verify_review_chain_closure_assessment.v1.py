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

ASSESS = (
    HERE
    / "01_review_chain_closure_assessment.v1.json"
)

A02_OUT = (
    HERE
    / "03_decision0122_a02_final_output.EXACT_COPY.v1.txt"
)

CONSUMPTION = (
    HERE
    / "04_decision0122_a02_consumption_record.v1.json"
)

SUMS = (
    HERE
    / "06_review_chain_closure_assessment.v1.SHA256SUMS"
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
        fail("MISSING|" + str(path))
    return hashlib.sha256(path.read_bytes()).hexdigest()

def git_object(rel):
    p = subprocess.run(
        [
            "git", "-C", str(REPO),
            "rev-parse", "HEAD:" + rel,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )

    if p.returncode != 0:
        fail("GIT_OBJECT|" + rel)

    return p.stdout.strip()

if git_object(ORIGINAL_REL) != \
        "e8178b937ab376faca698d35cc57d6e3785fbbb5":
    fail("ORIGINAL_REVIEW_TREE")

if git_object(FOCUSED_REL) != \
        "170c04d5dedf3a900edcf9d2a7ebc92b298b48a9":
    fail("FOCUSED_REVIEW_TREE")

if git_object(CORRECTIVE_REL) != \
        "dd34182886703f72fc5bfa4df899ad2bccbf4744":
    fail("CORRECTIVE_PACKAGE_TREE")

x = json.loads(
    ASSESS.read_text(encoding="utf-8")
)

if x["status"] != "COMPLETED":
    fail("ASSESSMENT_STATUS")

if x["assessment_outcome"] != "PASS_CLOSED":
    fail("ASSESSMENT_OUTCOME")

hist = x["historical_review_findings"]

if hist["SUCR01"] != "REVISION_REQUIRED":
    fail("HISTORICAL_SUCR01")

for rid in (
    "SUCR02", "SUCR03", "SUCR04", "SUCR05",
    "SUCR06", "SUCR07", "SUCR08",
):
    if hist[rid] != "PASS":
        fail("HISTORICAL_PASS|" + rid)

if hist["historical_overall"] != "REVISION_REQUIRED":
    fail("HISTORICAL_OVERALL")

if hist["historical_findings_rewritten"] is not False:
    fail("HISTORICAL_REWRITE")

orig = x["original_sucr01_corrective_requirement"]

if orig["scope"] != \
        "SOURCE_EVIDENCE_PORTABILITY_AND_RESOLVABILITY":
    fail("ORIGINAL_CORRECTIVE_SCOPE")

focused = x["focused_corrective_findings"]

if focused["criterion"] != "SUCR01-C":
    fail("FOCUSED_CRITERION")

if focused["scope"] != \
        "SOURCE_EVIDENCE_PORTABILITY_AND_RESOLVABILITY":
    fail("FOCUSED_SCOPE")

if focused["item_decision"] != "PASS":
    fail("FOCUSED_DECISION")

if focused["overall_decision"] != \
        "APPROVE_SUCR01_CORRECTIVE_PORTABLE_SOURCE_EVIDENCE_SUCCESSOR_PACKAGE_V2":
    fail("FOCUSED_OVERALL")

pred = x["closure_predicates"]

for key, value in pred.items():
    if value is not True:
        fail("CLOSURE_PREDICATE|" + key)

result = x["closure_result"]

if result["review_chain_closed"] is not True:
    fail("REVIEW_CHAIN_NOT_CLOSED")

if result["historical_sucr01_remains"] != \
        "REVISION_REQUIRED":
    fail("HISTORICAL_SUCR01_RESULT")

if result["historical_overall_remains"] != \
        "REVISION_REQUIRED":
    fail("HISTORICAL_OVERALL_RESULT")

study = x["study_state_after_closure"]

if study["status"] != "AUTHOR_CANDIDATE":
    fail("STUDY_STATUS")

if study["bounded_technical_outcome"] != \
        "FURTHER_EVIDENCE_REQUIRED":
    fail("BOUNDED_OUTCOME")

if study["governance_adopted"] is not False:
    fail("PREMATURE_GOVERNANCE_ADOPTION")

for key, value in x["technical_nonclaims"].items():
    if value is not False:
        fail("UNEXPECTED_PERMISSION|" + key)

cons = json.loads(
    CONSUMPTION.read_text(encoding="utf-8")
)

if cons["final_run_result"] != "PASS":
    fail("A02_RESULT")

if cons["verifier_state_after_run"] != \
        "PERMANENTLY_RETIRED":
    fail("A02_STATE")

if cons["must_never_be_rerun"] is not True:
    fail("A02_RETIREMENT")

if sha(A02_OUT) != cons["final_output_sha256"]:
    fail("A02_OUTPUT_SHA")

if (
    "REVIEW_CHAIN_CLOSURE_ASSESSMENT_AUTHORING_AUTHORIZATION=PASS"
    not in A02_OUT.read_text(encoding="utf-8")
):
    fail("A02_PASS_MARKER")

if SUMS.is_file():
    lines = [
        line for line in
        SUMS.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    if len(lines) != 5:
        fail(
            "CHECKSUM_ENTRY_COUNT|"
            + str(len(lines))
        )

    for line in lines:
        digest, rel = line.split(None, 1)
        rel = rel.strip().lstrip("*")
        target = HERE / rel

        if sha(target) != digest:
            fail("CHECKSUM|" + rel)

print("REVIEW_CHAIN_CLOSURE_ASSESSMENT=PASS")
print("REVIEW_CHAIN_CLOSURE_ASSESSMENT_OUTCOME=PASS_CLOSED")

print("ORIGINAL_SUCR01_DECISION_REMAINS=REVISION_REQUIRED")
print("SUCR02_SUCR08_ORIGINAL_PASS_FINDINGS_PRESERVED=YES")
print("ORIGINAL_OVERALL_REVIEW_REMAINS=REVISION_REQUIRED")

print("FOCUSED_SUCR01_C_DECISION=PASS")
print("FOCUSED_CORRECTIVE_OVERALL_APPROVAL=PASS")
print("CORRECTIVE_SCOPE_MATCH=YES")

print("REVIEW_CHAIN_CLOSED=YES")

print("STUDY_STATUS=AUTHOR_CANDIDATE")
print("GLOBAL_OUTCOME=FURTHER_EVIDENCE_REQUIRED")
print("STUDY_GOVERNANCE_ADOPTED=NO")

print("POSITIVE_EXISTING_V2_MAPPING_PROVEN=NO")
print("NEGATIVE_EXISTING_V2_MAPPING_IMPOSSIBILITY_PROVEN=NO")
print("WHOLE_V4_ADMISSIBLE_COMPOSITION_EXHAUSTIVENESS_PROVEN=NO")

print("OPERATIONAL_MAPPING_AUTHORIZED=NO")
print("SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO")
print("CURL_JSON_AUTHORIZED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")

print("DECISION_0122_A02_STATE=PERMANENTLY_RETIRED")
print("DECISION_0122_A02_EXECUTED_BY_SAFE_VERIFIER=NO")
print("RETIRED_A02_VERIFIERS_EXECUTED=NO")

print("SUCR_REVIEW_CHAIN_CLOSURE_ASSESSMENT_V1=PASS")
