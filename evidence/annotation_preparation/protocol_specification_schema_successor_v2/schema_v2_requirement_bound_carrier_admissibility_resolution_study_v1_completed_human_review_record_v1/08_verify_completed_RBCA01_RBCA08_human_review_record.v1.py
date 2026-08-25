#!/usr/bin/env python3

import hashlib
import json
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]

REVIEW = HERE / "01_completed_RBCA01_RBCA08_human_review.EXACT_COPY.v1.md"
MANIFEST = HERE / "02_completed_human_review_manifest.v1.json"
ACCOUNTING = HERE / "03_review_result_accounting.v1.json"
A02_OUT = HERE / "04_decision0143_a02_final_output.EXACT_COPY.v1.txt"
A02_CONS = HERE / "05_decision0143_a02_consumption_record.v1.json"
DEC0143 = HERE / "06_decision0143.EXACT_COPY.md"
DEC0142 = HERE / "07_decision0142.EXACT_COPY.md"
SUMS = HERE / "09_completed_human_review_record_v1.SHA256SUMS"

BASE_REL = (
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2"
)

HANDOFF_REL = (
    BASE_REL
    + "/schema_v2_requirement_bound_carrier_admissibility_resolution_study_v1_external_handoff_v1"
)

HANDOFF = REPO / HANDOFF_REL
HANDOFF_SAFE = HANDOFF / "08_verify_external_RBCA01_RBCA08_handoff.v1.py"

EXPECTED_REVIEW_SHA = (
    "9ded6b54b04c438a9a0f5ac3b7557d5ab19283c812fa5f2f6b529c92ef2e7eb1"
)

EXPECTED_REVIEW_SIZE = 8794

EXPECTED_HANDOFF_TREE = (
    "03cc454e001392c08684cb5f7b0483f10e529bb8"
)

EXPECTED_DEC0143_SHA = (
    "c85666ead800999a015135746a0081265b9f2319c4be6afb3da23023b88a02d4"
)

EXPECTED_DEC0142_SHA = (
    "6fb481f07252cf413832429564a22d3cf8b0b9aae0227663f8073b9cb0b95e4e"
)

EXPECTED_OVERALL = (
    "APPROVE_REQUIREMENT_BOUND_CARRIER_ADMISSIBILITY_RESOLUTION_STUDY_V1"
)

EXPECTED_NAME = "Abdul Raheem Shahzad"
EXPECTED_CONFIRMATION = "ARS"
EXPECTED_DATE = "24 / August / 2026"
EXPECTED_ROLE = "Spec-Technical-Reviewer-1"

def fail(msg):
    print("FAIL|" + msg)
    raise SystemExit(1)

def sha(path):
    if not path.is_file():
        fail("MISSING|" + str(path))

    return hashlib.sha256(path.read_bytes()).hexdigest()

if sha(REVIEW) != EXPECTED_REVIEW_SHA:
    fail("COMPLETED_REVIEW_SHA")

if REVIEW.stat().st_size != EXPECTED_REVIEW_SIZE:
    fail("COMPLETED_REVIEW_SIZE")

review = REVIEW.read_text(encoding="utf-8")

decisions = re.findall(
    r"^Decision:\s*`(PASS|REVISION_REQUIRED|FAIL)`\s*$",
    review,
    flags=re.MULTILINE,
)

if decisions != ["PASS"] * 8:
    fail("RBCA_DECISIONS")

overall = re.findall(
    r"^Overall decision:\s*`([^`]+)`\s*$",
    review,
    flags=re.MULTILINE,
)

if overall != [EXPECTED_OVERALL]:
    fail("OVERALL_DECISION")

def field(label):
    values = re.findall(
        rf"^{re.escape(label)}\s*(.+)$",
        review,
        flags=re.MULTILINE,
    )

    if len(values) != 1:
        fail("METADATA|" + label)

    return values[0].strip()

if field("Human reviewer name:") != EXPECTED_NAME:
    fail("REVIEWER_NAME")

if field(
    "Human reviewer signature / recorded confirmation:"
) != EXPECTED_CONFIRMATION:
    fail("REVIEWER_CONFIRMATION")

if field("Human reviewer date:") != EXPECTED_DATE:
    fail("REVIEWER_DATE")

if field("Reviewer role:") != EXPECTED_ROLE:
    fail("REVIEWER_ROLE")

for phrase in (
    "does not establish Schema-V2 losslessness",
    "resolve carrier admissibility",
    "positive mapping",
    "negative mapping impossibility",
    "whole-V4 admissible-composition exhaustiveness",
):
    if phrase not in review:
        fail("BOUNDED_NONCLAIM|" + phrase)

manifest = json.loads(
    MANIFEST.read_text(encoding="utf-8")
)

if (
    manifest["record_status"]
    != "COMPLETED_HUMAN_REVIEW_RECORDED_PENDING_SEPARATE_GOVERNANCE_ADOPTION"
):
    fail("RECORD_STATUS")

packet = manifest["completed_human_review_packet"]

if packet["sha256"] != EXPECTED_REVIEW_SHA:
    fail("MANIFEST_REVIEW_SHA")

if packet["byte_exact_to_validated_return"] is not True:
    fail("BYTE_EXACT_STATE")

if packet["human_review_completed"] is not True:
    fail("HUMAN_REVIEW_COMPLETED_STATE")

if packet["human_review_recorded_in_repository"] is not True:
    fail("HUMAN_REVIEW_RECORDED_STATE")

if packet["reviewer_decision_synthesized"] is not False:
    fail("DECISION_SYNTHESIS")

if packet["reviewer_identity_synthesized"] is not False:
    fail("IDENTITY_SYNTHESIS")

if packet["reviewer_notes_rewritten"] is not False:
    fail("NOTES_REWRITE")

result = manifest["human_review_result"]

for key in (
    "RBCA01","RBCA02","RBCA03","RBCA04",
    "RBCA05","RBCA06","RBCA07","RBCA08",
):
    if result[key] != "PASS":
        fail("MANIFEST_ITEM_RESULT|" + key)

if result["pass_count"] != 8:
    fail("PASS_COUNT")

if result["revision_required_count"] != 0:
    fail("REVISION_COUNT")

if result["fail_count"] != 0:
    fail("FAIL_COUNT")

if result["overall_review_decision"] != EXPECTED_OVERALL:
    fail("MANIFEST_OVERALL")

if result["reviewer_name"] != EXPECTED_NAME:
    fail("MANIFEST_REVIEWER_NAME")

if result["reviewer_confirmation"] != EXPECTED_CONFIRMATION:
    fail("MANIFEST_CONFIRMATION")

if result["reviewer_date"] != EXPECTED_DATE:
    fail("MANIFEST_DATE")

if result["reviewer_role"] != EXPECTED_ROLE:
    fail("MANIFEST_ROLE")

technical = manifest["reviewed_technical_result"]

if technical["author_candidate_outcome"] != "FURTHER_EVIDENCE_REQUIRED":
    fail("TECHNICAL_OUTCOME")

if technical["unresolved_count"] != 17:
    fail("UNRESOLVED_COUNT")

if technical["admissible_exact_count"] != 0:
    fail("ADMISSIBLE_EXACT")

if technical["admissible_composite_count"] != 0:
    fail("ADMISSIBLE_COMPOSITE")

if technical["no_admissible_carrier_proven_count"] != 0:
    fail("NEGATIVE_CARRIER_COUNT")

governance = manifest["governance_state"]

if governance["human_review_completed"] is not True:
    fail("GOV_HUMAN_REVIEW_COMPLETED")

if governance["human_review_recorded_in_repository"] is not True:
    fail("GOV_HUMAN_REVIEW_RECORDED")

if governance["study_governance_adopted"] is not False:
    fail("GOVERNANCE_ADOPTED")

if governance["study_governance_adoption_authorized"] is not False:
    fail("GOVERNANCE_ADOPTION_AUTHORIZED")

for key, value in manifest["technical_nonclaims"].items():
    if value is not False:
        fail("UNEXPECTED_TECHNICAL_CLAIM|" + key)

for key, value in manifest["explicit_non_authorizations"].items():
    if value is not False:
        fail("UNEXPECTED_AUTHORIZATION|" + key)

accounting = json.loads(
    ACCOUNTING.read_text(encoding="utf-8")
)

if accounting["source_completed_review_sha256"] != EXPECTED_REVIEW_SHA:
    fail("ACCOUNTING_REVIEW_SHA")

if accounting["pass_count"] != 8:
    fail("ACCOUNTING_PASS_COUNT")

if accounting["revision_required_count"] != 0:
    fail("ACCOUNTING_REVISION_COUNT")

if accounting["fail_count"] != 0:
    fail("ACCOUNTING_FAIL_COUNT")

if accounting["overall_review_decision"] != EXPECTED_OVERALL:
    fail("ACCOUNTING_OVERALL")

if accounting["study_governance_adopted"] is not False:
    fail("ACCOUNTING_GOV_ADOPTION")

if accounting["study_governance_adoption_authorized"] is not False:
    fail("ACCOUNTING_GOV_AUTHORIZATION")

cons = json.loads(
    A02_CONS.read_text(encoding="utf-8")
)

if cons["final_run_result"] != "PASS":
    fail("A02_RESULT")

if cons["verifier_state_after_run"] != "PERMANENTLY_RETIRED":
    fail("A02_STATE")

if cons["rerun_authorized"] is not False:
    fail("A02_RERUN")

if cons["must_never_be_rerun"] is not True:
    fail("A02_RETIREMENT")

if cons["previous_retired_a02_verifiers_executed"] is not False:
    fail("PREVIOUS_RETIRED_A02_EXECUTION")

if sha(A02_OUT) != cons["final_output_sha256"]:
    fail("A02_OUTPUT_SHA")

if (
    "COMPLETED_RBCA01_RBCA08_HUMAN_REVIEW_RECORDING_AUTHORIZATION=PASS"
    not in A02_OUT.read_text(encoding="utf-8")
):
    fail("A02_PASS_MARKER")

if sha(DEC0143) != EXPECTED_DEC0143_SHA:
    fail("DECISION0143_SHA")

if sha(DEC0142) != EXPECTED_DEC0142_SHA:
    fail("DECISION0142_SHA")

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

if p.returncode != 0:
    fail("HANDOFF_TREE_QUERY")

if p.stdout.strip() != EXPECTED_HANDOFF_TREE:
    fail("HANDOFF_TREE")

p = subprocess.run(
    ["python3", str(HANDOFF_SAFE)],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    check=False,
)

if p.returncode != 0:
    fail(
        "HANDOFF_SAFE_VERIFIER|"
        + p.stdout
        + p.stderr
    )

for marker in (
    "EXTERNAL_RBCA01_RBCA08_HANDOFF_V1=PASS",
    "STUDY_OUTCOME_UNDER_REVIEW=FURTHER_EVIDENCE_REQUIRED",
    "UNRESOLVED_COUNT=17",
    "STUDY_GOVERNANCE_ADOPTED=NO",
    "RETIRED_A02_VERIFIERS_EXECUTED=NO",
):
    if marker not in p.stdout:
        fail("HANDOFF_SAFE_MARKER|" + marker)

if SUMS.is_file():
    for line in SUMS.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue

        digest, rel = line.split(None, 1)
        rel = rel.strip().lstrip("*")

        if sha(HERE / rel) != digest:
            fail("CHECKSUM|" + rel)

print("COMPLETED_RBCA01_RBCA08_HUMAN_REVIEW_RECORD_V1=PASS")
print("RECORD_STATUS=COMPLETED_HUMAN_REVIEW_RECORDED_PENDING_SEPARATE_GOVERNANCE_ADOPTION")
print("HUMAN_REVIEW_COMPLETED=YES")
print("HUMAN_REVIEW_RECORDED_IN_REPOSITORY=YES")
print("COMPLETED_REVIEW_BYTE_EXACT_BINDING=PASS")
print("RBCA01_RBCA08_PASS_COUNT=8")
print("RBCA_REVISION_REQUIRED_COUNT=0")
print("RBCA_FAIL_COUNT=0")
print("OVERALL_REVIEW_DECISION=" + EXPECTED_OVERALL)
print("REVIEWER_NAME=" + EXPECTED_NAME)
print("REVIEWER_CONFIRMATION=" + EXPECTED_CONFIRMATION)
print("REVIEWER_DATE=" + EXPECTED_DATE)
print("REVIEWER_ROLE=" + EXPECTED_ROLE)
print("REVIEWER_DECISION_SYNTHESIZED=NO")
print("REVIEWER_IDENTITY_SYNTHESIZED=NO")
print("REVIEWER_NOTES_REWRITTEN=NO")
print("REVIEWED_TECHNICAL_OUTCOME=FURTHER_EVIDENCE_REQUIRED")
print("UNRESOLVED_COUNT=17")
print("CARRIER_ADMISSIBILITY_RESOLVED=NO")
print("POSITIVE_MAPPING_PROVEN=NO")
print("NEGATIVE_MAPPING_IMPOSSIBILITY_PROVEN=NO")
print("WHOLE_V4_EXHAUSTIVENESS_PROVEN=NO")
print("STUDY_GOVERNANCE_ADOPTED=NO")
print("STUDY_GOVERNANCE_ADOPTION_AUTHORIZED=NO")
print("OPERATIONAL_MAPPING_AUTHORIZED=NO")
print("SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO")
print("CURL_JSON_AUTHORIZED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
print("DECISION_0143_A02_STATE=PERMANENTLY_RETIRED")
print("DECISION_0143_A02_EXECUTED_BY_SAFE_VERIFIER=NO")
print("RETIRED_A02_VERIFIERS_EXECUTED=NO")
