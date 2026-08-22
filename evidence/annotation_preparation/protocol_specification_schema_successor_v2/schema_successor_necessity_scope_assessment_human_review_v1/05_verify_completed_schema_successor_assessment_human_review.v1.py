#!/usr/bin/env python3

import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent

REVIEW = HERE / \
    "01_completed_schema_successor_assessment_human_review.EXACT_COPY.v1.md"

HANDOFF = HERE / \
    "02_external_handoff_manifest.EXACT_COPY.v1.json"

CONSUMED = HERE / \
    "03_initial_blank_verifier_consumption_marker.EXACT_COPY.v1"

RECORD = HERE / \
    "04_completed_schema_successor_assessment_human_review_record.v1.json"

EXPECTED_REVIEW_SHA = \
    "e81cf41aa331e371541cb3b3c8b9392e66ccedbf8b87a3e9ed3943dee8a5fd22"

EXPECTED_REVIEW_SIZE = 9949

EXPECTED_HANDOFF_SHA = \
    "d3945fd47149975c414d3c27bdc289b9f14d0ed91f0634bbe5a796ff9aa37978"

EXPECTED_CONSUMED_SHA = \
    "0d6827542b2d9dfad86dc46aba8dbfbe4aea5c93ee0a60091c00a8054ce578e0"

def fail(msg):
    print("FAIL|" + msg)
    raise SystemExit(1)

def sha(path):
    if not path.is_file():
        fail("MISSING|" + path.name)

    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()

if sha(REVIEW) != EXPECTED_REVIEW_SHA:
    fail("REVIEW_SHA")

if REVIEW.stat().st_size != EXPECTED_REVIEW_SIZE:
    fail("REVIEW_SIZE")

if sha(HANDOFF) != EXPECTED_HANDOFF_SHA:
    fail("HANDOFF_SHA")

if sha(CONSUMED) != EXPECTED_CONSUMED_SHA:
    fail("CONSUMPTION_MARKER_SHA")

review_text = REVIEW.read_text(
    encoding="utf-8"
)

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

for rid, expected_decision in expected.items():
    m = re.search(
        rf"^### {rid}\b.*?"
        rf"^Decision \(PASS / REVISION_REQUIRED / FAIL\):\s*"
        rf"(PASS|REVISION_REQUIRED|FAIL)\s*$",
        review_text,
        flags=re.MULTILINE | re.DOTALL,
    )

    if not m or m.group(1) != expected_decision:
        fail(
            "ITEM_DECISION|"
            + rid
        )

overall = re.search(
    r"^Overall decision "
    r"\(APPROVE_SCHEMA_SUCCESSOR_NECESSITY_SCOPE_ASSESSMENT / "
    r"REVISION_REQUIRED / FAIL\):\s*"
    r"(APPROVE_SCHEMA_SUCCESSOR_NECESSITY_SCOPE_ASSESSMENT|"
    r"REVISION_REQUIRED|FAIL)\s*$",
    review_text,
    flags=re.MULTILINE,
)

if not overall or overall.group(1) != "REVISION_REQUIRED":
    fail("OVERALL_DECISION")

record = json.loads(
    RECORD.read_text(
        encoding="utf-8"
    )
)

if record[
    "completed_review"
]["overall_decision"] != "REVISION_REQUIRED":
    fail("RECORD_OVERALL")

if record[
    "review_subject"
]["author_candidate_conclusion_human_approved"] is not False:
    fail("AUTHOR_CONCLUSION_APPROVAL_STATE")

if record[
    "review_interpretation"
]["assessment_v1_human_approved"] is not False:
    fail("ASSESSMENT_APPROVAL_STATE")

if record[
    "review_interpretation"
]["schema_successor_required_human_approved"] is not False:
    fail("SUCCESSOR_REQUIRED_APPROVAL_STATE")

if record[
    "review_interpretation"
]["current_supported_position"] != \
   "FURTHER_EVIDENCE_REQUIRED_UNLESS_EXHAUSTIVE_ADMISSIBLE_V2_CAPABILITY_ARGUMENT_IS_ESTABLISHED":
    fail("SUPPORTED_POSITION")

if record[
    "review_interpretation"
]["assessment_v1_must_remain_immutable"] is not True:
    fail("ASSESSMENT_V1_IMMUTABILITY")

if record[
    "review_interpretation"
]["corrective_successor_required_for_revision"] is not True:
    fail("CORRECTIVE_SUCCESSOR_BOUNDARY")

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

print("COMPLETED_ASSESSMENT_HUMAN_REVIEW_EXACT_BYTES=PASS")
print("SR01=PASS")
print("SR02=REVISION_REQUIRED")
print("SR03=PASS")
print("SR04=PASS")
print("SR05=PASS")
print("SR06=PASS")
print("SR07=REVISION_REQUIRED")
print("SR08=REVISION_REQUIRED")
print("OVERALL_ASSESSMENT_HUMAN_DECISION=REVISION_REQUIRED")

print("ASSESSMENT_V1_HUMAN_APPROVED=NO")
print("SCHEMA_SUCCESSOR_REQUIRED_HUMAN_APPROVED=NO")

print("CURRENT_SUPPORTED_POSITION=FURTHER_EVIDENCE_REQUIRED_UNLESS_EXHAUSTIVE_ADMISSIBLE_V2_CAPABILITY_ARGUMENT_IS_ESTABLISHED")

print("ASSESSMENT_V1_MODIFICATION_AUTHORIZED=NO")
print("CORRECTIVE_ASSESSMENT_V2_AUTHORING_AUTHORIZED=NO")
print("SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO")
print("POSITIVE_MAPPING_AUTHORIZED=NO")
print("CURL_JSON_CREATED=NO")

print("COMPLETED_ASSESSMENT_V1_HUMAN_REVIEW_RECORD=PASS")
