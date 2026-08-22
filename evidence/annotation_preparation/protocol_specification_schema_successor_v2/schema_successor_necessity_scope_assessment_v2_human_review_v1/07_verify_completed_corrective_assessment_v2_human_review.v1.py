#!/usr/bin/env python3

import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent

REVIEW = HERE / \
    "01_completed_corrective_assessment_v2_human_review.EXACT_COPY.v1.md"

EXT_RECORD = HERE / \
    "02_external_completed_human_review_record.EXACT_COPY.v1.json"

EXT_SUMS = HERE / \
    "03_external_completed_human_review_checksums.EXACT_COPY.v1.SHA256SUMS"

HANDOFF_MANIFEST = HERE / \
    "04_external_handoff_manifest.EXACT_COPY.v1.json"

CONSUMED = HERE / \
    "05_initial_blank_verifier_consumption_marker.EXACT_COPY.v1"

RECORD = HERE / \
    "06_completed_corrective_assessment_v2_human_review_record.v1.json"

EXPECTED = {
    REVIEW:
        "fdb770d807d08946656fb70caa336de9f88d39b47bf3bf5963e8a32503f1ea9c",

    EXT_RECORD:
        "c71a4d2d1e9853b7dedd0390aa0aa6462db74e4a73c7f24dca17658257aaac31",

    EXT_SUMS:
        "0665e5dc5f714aa0c9885d7a6be53f51f11da906bfbf56c3f3d717dfd2db5efe",

    HANDOFF_MANIFEST:
        "f16e614be98ea9e2b38a7b2cd787f2fb0a51ff02cc0cc8189681bce5b31c1c74",

    CONSUMED:
        "cca3d2c5a1f292875663918e3cd1dac8ca76e9fde8fd6d8f69eb55ca4ff8dfd4",
}

def fail(msg):
    print("FAIL|" + msg)
    raise SystemExit(1)

def sha(path):
    if not path.is_file():
        fail("MISSING|" + path.name)

    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()

for path, expected in EXPECTED.items():
    if sha(path) != expected:
        fail(
            "SHA|"
            + path.name
        )

text = REVIEW.read_text(
    encoding="utf-8"
)

decisions = re.findall(
    r"^Decision \(PASS / REVISION_REQUIRED / FAIL\):\s*(\S+)\s*$",
    text,
    flags=re.MULTILINE,
)

if decisions != ["PASS"] * 8:
    fail("CVR_DECISIONS")

overall = re.findall(
    r"^Overall decision "
    r"\(APPROVE_CORRECTIVE_SCHEMA_SUCCESSOR_NECESSITY_SCOPE_ASSESSMENT_V2 / "
    r"REVISION_REQUIRED / FAIL\):\s*(\S+)\s*$",
    text,
    flags=re.MULTILINE,
)

if overall != [
    "APPROVE_CORRECTIVE_SCHEMA_SUCCESSOR_NECESSITY_SCOPE_ASSESSMENT_V2"
]:
    fail("OVERALL_DECISION")

required_cvr01 = (
    "Before reviewer editing, the manual-review copy was "
    "byte-identical to the blank draft, as established by the "
    "one-time initial blank-state verification and its consumption marker."
)

if required_cvr01 not in text:
    fail("CVR01_TEMPORAL_CORRECTION")

if (
    "The manual-review copy remains byte-identical to the blank draft."
    in text
):
    fail("STALE_CVR01_CLAIM")

expected_identity = {
    "Reviewer role":
        "Spec-Reviewer-1",

    "Human reviewer name":
        "Abdul Raheem Shahzad",

    "Human reviewer signature / recorded confirmation":
        "ARS",

    "Human reviewer date":
        "22 / August / 2026",
}

for field, expected in expected_identity.items():

    values = re.findall(
        r"^"
        + re.escape(field)
        + r":\s*(.*?)\s*$",
        text,
        flags=re.MULTILINE,
    )

    if values != [expected]:
        fail(
            "IDENTITY|"
            + field
        )

if re.search(
    r"^Reviewer role ID:",
    text,
    flags=re.MULTILINE,
):
    fail("OLD_REVIEWER_ROLE_ID_LABEL")

consumed = CONSUMED.read_text(
    encoding="utf-8"
)

for line in (
    "INITIAL_BLANK_STATE_VERIFIER_SUCCESSFULLY_CONSUMED=YES",
    "SUCCESSFUL_RUN_COUNT=1",
    "MUST_NEVER_RERUN_AFTER_THIS_POINT=YES",
):
    if line not in consumed.splitlines():
        fail(
            "CONSUMPTION_MARKER|"
            + line
        )

record = json.loads(
    RECORD.read_text(
        encoding="utf-8"
    )
)

if record["status"] != \
   "COMPLETED_INDEPENDENT_HUMAN_TECHNICAL_REVIEW_APPROVED_AND_RECORDED":
    fail("STATUS")

if record[
    "review_subject"
]["human_approved_selected_outcome"] != "FURTHER_EVIDENCE_REQUIRED":
    fail("APPROVED_OUTCOME")

if record[
    "completed_human_review"
]["item_decisions"] != {
    "CVR01": "PASS",
    "CVR02": "PASS",
    "CVR03": "PASS",
    "CVR04": "PASS",
    "CVR05": "PASS",
    "CVR06": "PASS",
    "CVR07": "PASS",
    "CVR08": "PASS",
}:
    fail("RECORDED_ITEM_DECISIONS")

if record[
    "completed_human_review"
]["overall_decision"] != \
   "APPROVE_CORRECTIVE_SCHEMA_SUCCESSOR_NECESSITY_SCOPE_ASSESSMENT_V2":
    fail("RECORDED_OVERALL_DECISION")

bounded = record[
    "bounded_human_approval"
]

if bounded[
    "corrective_assessment_v2_human_approved"
] is not True:
    fail("V2_APPROVAL")

if bounded[
    "further_evidence_required_human_approved"
] is not True:
    fail("FER_APPROVAL")

if bounded[
    "schema_successor_required_human_approved"
] is not False:
    fail("SUCCESSOR_REQUIRED_APPROVAL")

if bounded[
    "no_successor_required_with_proven_v2_mapping_human_approved"
] is not False:
    fail("NO_SUCCESSOR_APPROVAL")

for key, value in record[
    "explicit_non_authorizations"
].items():
    if value is not False:
        fail(
            "NONAUTH|"
            + key
        )

print("COMPLETED_CORRECTIVE_V2_HUMAN_REVIEW_EXACT_BYTES=PASS")

for i in range(1, 9):
    print(f"CVR{i:02d}=PASS")

print("OVERALL_CORRECTIVE_V2_HUMAN_DECISION=APPROVE_CORRECTIVE_SCHEMA_SUCCESSOR_NECESSITY_SCOPE_ASSESSMENT_V2")

print("CORRECTIVE_ASSESSMENT_V2_HUMAN_APPROVED=YES")
print("FURTHER_EVIDENCE_REQUIRED_HUMAN_APPROVED=YES")

print("SCHEMA_SUCCESSOR_REQUIRED_HUMAN_APPROVED=NO")
print("NO_SUCCESSOR_REQUIRED_WITH_PROVEN_V2_MAPPING_HUMAN_APPROVED=NO")

print("INITIAL_BLANK_STATE_VERIFIER_SUCCESSFUL_RUN_COUNT=1")
print("INITIAL_BLANK_STATE_VERIFIER_RERUN=NO")

print("EXHAUSTIVE_V2_CAPABILITY_STUDY_AUTHORIZED=NO")
print("SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO")
print("SCHEMA_VERSION_PRESELECTED=NO")
print("POSITIVE_MAPPING_AUTHORIZED=NO")
print("CURL_JSON_CREATED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")

print("COMPLETED_CORRECTIVE_ASSESSMENT_V2_HUMAN_REVIEW_REPOSITORY_RECORD=PASS")
