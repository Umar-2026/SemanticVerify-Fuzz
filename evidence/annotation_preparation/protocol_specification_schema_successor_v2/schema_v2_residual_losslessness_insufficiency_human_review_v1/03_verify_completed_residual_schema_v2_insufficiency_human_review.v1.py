#!/usr/bin/env python3

import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent

RAW = HERE / \
    "01_completed_residual_schema_v2_insufficiency_human_review.EXACT_COPY.v1.md"

RECORD = HERE / \
    "02_completed_residual_schema_v2_insufficiency_human_review_record.v1.json"

EXPECTED_SHA = \
    "c169b26960349c4829109493f946d4f7115191a830ec35a28ff7a50e6df8c74d"

EXPECTED_SIZE = 9047

def fail(msg):
    print("FAIL|" + msg)
    raise SystemExit(1)

if not RAW.is_file():
    fail("RAW_REVIEW_MISSING")

if hashlib.sha256(
    RAW.read_bytes()
).hexdigest() != EXPECTED_SHA:
    fail("RAW_REVIEW_SHA")

if RAW.stat().st_size != EXPECTED_SIZE:
    fail("RAW_REVIEW_SIZE")

text = RAW.read_text(
    encoding="utf-8"
)

expected = {
    "RI01": "REVISION_REQUIRED",
    "RI02": "PASS",
    "RI03": "PASS",
    "RI04": "PASS",
    "RI05": "PASS",
    "RI06": "PASS",
    "RI07": "PASS",
    "RI08": "PASS",
}

observed = {}

for rid in expected:
    m = re.search(
        rf"^### {rid}\b.*?"
        rf"^Decision \(PASS / REVISION_REQUIRED / FAIL\):\s*"
        rf"(PASS|REVISION_REQUIRED|FAIL)\s*$",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )

    if not m:
        fail("ITEM_DECISION|" + rid)

    observed[rid] = m.group(1)

if observed != expected:
    fail("ITEM_DECISION_SET")

overall = re.search(
    r"^Overall decision "
    r"\(APPROVE_RESIDUAL_SCHEMA_V2_INSUFFICIENCY_PROOF / "
    r"REVISION_REQUIRED / FAIL\):\s*"
    r"(APPROVE_RESIDUAL_SCHEMA_V2_INSUFFICIENCY_PROOF|"
    r"REVISION_REQUIRED|FAIL)\s*$",
    text,
    flags=re.MULTILINE,
)

if not overall or overall.group(1) != "REVISION_REQUIRED":
    fail("OVERALL_DECISION")

r = json.loads(
    RECORD.read_text(
        encoding="utf-8"
    )
)

if r["overall_decision"] != "REVISION_REQUIRED":
    fail("RECORD_OVERALL_DECISION")

if r[
    "review_interpretation"
]["RI02_to_RI08_pass_closed_for_this_review"] is not True:
    fail("RI02_TO_RI08_NOT_PASS_CLOSED")

if r[
    "review_interpretation"
]["technical_residual_insufficiency_argument_rejected"] is not False:
    fail("TECHNICAL_ARGUMENT_STATE")

if r[
    "review_interpretation"
]["corrective_scope"] != "EVIDENCE_ONLY":
    fail("CORRECTIVE_SCOPE")

for key, value in r[
    "explicit_non_authorizations"
].items():
    if value is not False:
        fail("NONAUTH|" + key)

print("COMPLETED_HUMAN_REVIEW_EXACT_BYTES=PASS")
print("RI01=REVISION_REQUIRED")
print("RI02_TO_RI08=PASS")
print("RI02_TO_RI08_PASS_CLOSED=YES")
print("OVERALL_HUMAN_DECISION=REVISION_REQUIRED")
print("CORRECTIVE_SCOPE=EVIDENCE_ONLY")
print("TECHNICAL_RESIDUAL_INSUFFICIENCY_ARGUMENT_REJECTED=NO")
print("COMPLETED_HUMAN_REVIEW_RECORD=PASS")
