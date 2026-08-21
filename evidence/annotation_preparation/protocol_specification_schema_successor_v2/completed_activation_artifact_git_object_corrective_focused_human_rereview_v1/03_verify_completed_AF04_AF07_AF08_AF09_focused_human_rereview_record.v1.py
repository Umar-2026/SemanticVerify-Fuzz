#!/usr/bin/env python3

import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent

REVIEW = HERE / \
    "01_completed_AF04_AF07_AF08_AF09_focused_human_rereview.v1.md"

RECORD = HERE / \
    "02_completed_AF04_AF07_AF08_AF09_focused_human_rereview_record.v1.json"

EXPECTED_SHA = \
    "1f531a54bce1c6f7a8aeeb9531a834fbf55bdc30b4242439bc48de79222fc170"

EXPECTED_SIZE = 4438

def fail(x):
    print("FAIL|" + x)
    raise SystemExit(1)

raw = REVIEW.read_bytes()

if hashlib.sha256(raw).hexdigest() != EXPECTED_SHA:
    fail("REVIEW_SHA")

if len(raw) != EXPECTED_SIZE:
    fail("REVIEW_SIZE")

text = raw.decode(
    "utf-8"
).replace(
    "\r\n", "\n"
).replace(
    "\r", "\n"
)

normalized = (
    text
    .replace("\\#", "#")
    .replace("\\_", "_")
)

for rid in (
    "AF04",
    "AF07",
    "AF08",
    "AF09",
):
    heading = re.search(
        r"^##\s+"
        + rid
        + r"\b.*$",
        normalized,
        re.M
    )

    if not heading:
        fail("MISSING_ITEM|" + rid)

    tail = normalized[heading.end():]

    nxt = re.search(
        r"^##\s+",
        tail,
        re.M
    )

    section = (
        tail[:nxt.start()]
        if nxt
        else tail
    )

    vals = re.findall(
        r"^Decision:[ \t]*(.*?)[ \t]*$",
        section,
        re.M
    )

    if vals != ["PASS"]:
        fail("ITEM_DECISION|" + rid)

overall = re.findall(
    r"^Overall decision:[ \t]*(.*?)[ \t]*$",
    normalized,
    re.M
)

if overall != [
    "APPROVE_AF04_AF07_AF08_AF09_CORRECTIVE_EVIDENCE"
]:
    fail("OVERALL_DECISION")

record = json.loads(
    RECORD.read_text(
        encoding="utf-8"
    )
)

if record["status"] != \
   "AF01_TO_AF10_HUMAN_REVIEW_COMPLETE_10_PASS_RECORD_ONLY_NOT_ACTIVATED":
    fail("STATUS")

if record[
    "completed_review"
]["sha256"] != EXPECTED_SHA:
    fail("RECORD_SHA")

if record[
    "completed_review"
]["item_decisions"] != {
    "AF04": "PASS",
    "AF07": "PASS",
    "AF08": "PASS",
    "AF09": "PASS",
}:
    fail("RECORDED_ITEM_DECISIONS")

if record[
    "completed_review"
]["overall_decision"] != \
   "APPROVE_AF04_AF07_AF08_AF09_CORRECTIVE_EVIDENCE":
    fail("RECORDED_OVERALL")

if record[
    "aggregate_AF01_to_AF10_state"
] != {
    "PASS": 10,
    "REVISION_REQUIRED": 0,
    "FAIL": 0,
}:
    fail("AGGREGATE_STATE")

effects = record["approval_effect"]

if effects[
    "corrective_evidence_human_approved"
] is not True:
    fail("APPROVAL_FLAG")

for key, value in effects.items():
    if key == "corrective_evidence_human_approved":
        continue

    if value is not False:
        fail("PROHIBITED_EFFECT|" + key)

retired = record[
    "retired_verifier_constraints"
]

if retired[
    "focused_initial_blank_verifier_rerun"
] is not False:
    fail("INITIAL_BLANK_RERUN")

if retired[
    "decision_0063_prepackage_authorization_verifier_rerun"
] is not False:
    fail("DEC0063_AUTH_RERUN")

print("ESCAPED_MARKDOWN_NORMALIZATION=PASS")
print("AF04=PASS")
print("AF07=PASS")
print("AF08=PASS")
print("AF09=PASS")
print(
    "FOCUSED_OVERALL="
    "APPROVE_AF04_AF07_AF08_AF09_CORRECTIVE_EVIDENCE"
)
print("AF01_TO_AF10_PASS_COUNT=10")
print("AF01_TO_AF10_REVISION_REQUIRED_COUNT=0")
print("AF01_TO_AF10_FAIL_COUNT=0")
print("CORRECTIVE_EVIDENCE_HUMAN_APPROVED=YES")
print("SCHEMA_V2_ACTIVATED=NO")
print("INITIAL_BLANK_VERIFIER_RERUN=NO")
print("DECISION_0063_PREPACKAGE_AUTHORIZATION_VERIFIER_RERUN=NO")
print("COMPLETED_FOCUSED_HUMAN_REVIEW_RECORD=PASS")
