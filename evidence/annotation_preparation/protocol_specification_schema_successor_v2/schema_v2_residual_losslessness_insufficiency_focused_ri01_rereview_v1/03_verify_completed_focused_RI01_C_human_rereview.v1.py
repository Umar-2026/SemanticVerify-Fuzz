#!/usr/bin/env python3

import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent

RAW = HERE / \
    "01_completed_focused_RI01_C_human_rereview.EXACT_COPY.v1.md"

RECORD = HERE / \
    "02_completed_focused_RI01_C_human_rereview_record.v1.json"

EXPECTED_SHA = \
    "ad29020ad67b43e1603e6e81a1b635c5b722b77d6a429ecdd2510b53f7c42494"

EXPECTED_SIZE = 6012

def fail(msg):
    print("FAIL|" + msg)
    raise SystemExit(1)

if not RAW.is_file():
    fail("RAW_REREVIEW_MISSING")

if hashlib.sha256(
    RAW.read_bytes()
).hexdigest() != EXPECTED_SHA:
    fail("RAW_REREVIEW_SHA")

if RAW.stat().st_size != EXPECTED_SIZE:
    fail("RAW_REREVIEW_SIZE")

text = RAW.read_text(
    encoding="utf-8"
)

decision = re.search(
    r"^Focused RI01 decision "
    r"\(PASS / REVISION_REQUIRED / FAIL\):\s*"
    r"(PASS|REVISION_REQUIRED|FAIL)\s*$",
    text,
    flags=re.MULTILINE,
)

if not decision or decision.group(1) != "PASS":
    fail("FOCUSED_RI01_DECISION")

record = json.loads(
    RECORD.read_text(
        encoding="utf-8"
    )
)

chain = record["review_chain"]

if chain[
    "historical_first_round_overall_decision"
] != "REVISION_REQUIRED":
    fail("HISTORICAL_OVERALL_DECISION")

if chain[
    "historical_first_round_decision_rewritten"
] is not False:
    fail("HISTORICAL_DECISION_REWRITTEN")

if chain[
    "RI01_corrective_decision"
] != "PASS":
    fail("RI01_CORRECTIVE_DECISION")

if chain[
    "RI01_corrective_deficiency_closed"
] is not True:
    fail("RI01_NOT_CLOSED")

if chain[
    "RI02_to_RI08"
] != "PASS_CLOSED":
    fail("RI02_TO_RI08_STATE")

if chain[
    "all_RI01_to_RI08_review_items_now_pass_closed"
] is not True:
    fail("ALL_ITEMS_NOT_CLOSED")

if chain[
    "synthetic_overall_reviewer_approval_created"
] is not False:
    fail("SYNTHETIC_OVERALL_APPROVAL")

if record[
    "reviewed_governance_conclusion"
]["residual_schema_v2_insufficiency_review_chain_complete"] is not True:
    fail("REVIEW_CHAIN_NOT_COMPLETE")

for key, value in record[
    "explicit_non_authorizations"
].items():
    if value is not False:
        fail("NONAUTH|" + key)

print("FOCUSED_RI01_C_EXACT_BYTES=PASS")
print("FOCUSED_RI01_C_HUMAN_DECISION=PASS")
print("RI01_CORRECTIVE_DEFICIENCY_CLOSED=YES")
print("RI02_TO_RI08_PASS_CLOSED=YES")
print("ALL_RI01_TO_RI08_REVIEW_ITEMS_NOW_PASS_CLOSED=YES")
print("HISTORICAL_FIRST_ROUND_OVERALL_DECISION=REVISION_REQUIRED")
print("HISTORICAL_FIRST_ROUND_DECISION_REWRITTEN=NO")
print("SYNTHETIC_OVERALL_REVIEWER_APPROVAL_CREATED=NO")
print("RESIDUAL_SCHEMA_V2_INSUFFICIENCY_REVIEW_CHAIN_COMPLETE=YES")
print("COMPLETED_FOCUSED_RI01_REREVIEW_RECORD=PASS")
