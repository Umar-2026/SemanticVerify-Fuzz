#!/usr/bin/env python3

import hashlib
import json
import re
from pathlib import Path

def fail(x):
    print("FAIL|" + x)
    raise SystemExit(1)

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

here = Path(__file__).resolve().parent
repo = here

while repo != repo.parent and not (repo / ".git").exists():
    repo = repo.parent

review = here / "01_completed_v4_human_review.APPROVED.v1.md"
recordp = here / "02_completed_v4_human_review_record.v1.json"

v4p = (
    repo /
    "config/annotation/"
    "curl_canonical_representation_mapping_contract.v4.json"
)

curlp = repo / "config/protocol_specifications/curl.json"

REVIEW_SHA = "6933bc89ab522e853640cc42f8ce3925e3fbc027a65ebc2f38bc083bf593649d"
V4_SHA = "9a44120de8947369864b75fb04680b504b91ccfa478eeaeaea20162a6d97e070"

if sha(review) != REVIEW_SHA:
    fail("REVIEW_SHA")

if review.stat().st_size != 17101:
    fail("REVIEW_SIZE")

if sha(v4p) != V4_SHA:
    fail("V4_SHA")

if v4p.stat().st_size != 26601:
    fail("V4_SIZE")

text = (
    review.read_text(encoding="utf-8")
    .replace("\r\n", "\n")
    .replace("\r", "\n")
    .replace("\\_", "_")
)

for i in range(1, 11):
    rr = f"V4-RR{i:02d}"

    heads = list(
        re.finditer(
            rf"^###\s+{re.escape(rr)}\b[^\n]*$",
            text,
            re.M
        )
    )

    if len(heads) != 1:
        fail("HEADING|" + rr)

    tail = text[heads[0].end():]

    nxt = re.search(
        r"^###\s+V4-RR\d{2}\b[^\n]*$|"
        r"^##\s+Overall technical review decision\b",
        tail,
        re.M
    )

    section = tail[:nxt.start()] if nxt else tail

    vals = re.findall(
        r"^Decision:[ \t]*(.*?)[ \t]*$",
        section,
        re.M
    )

    if len(vals) != 1 or vals[0].strip() != "PASS":
        fail("DECISION|" + rr)

overall = re.findall(
    r"^Overall decision:[ \t]*(.*?)[ \t]*$",
    text,
    re.M
)

if len(overall) != 1 or overall[0].strip() != \
   "APPROVE_V4_RR10_CORRECTED_SCHEMA_INSUFFICIENCY_PROOF":
    fail("OVERALL")

identity = {
    "Human reviewer name":
        "Abdul Raheem Shahzad",

    "Human reviewer signature / recorded confirmation":
        "ARS",

    "Human reviewer date":
        "20 / August / 2026"
}

for label, expected in identity.items():
    vals = re.findall(
        "^" + re.escape(label) + r":[ \t]*(.*?)[ \t]*$",
        text,
        re.M
    )

    if len(vals) != 1 or vals[0].strip() != expected:
        fail("IDENTITY|" + label)

r = json.loads(recordp.read_text(encoding="utf-8"))

if r["status"] != "COMPLETED_HUMAN_REVIEW_RECORDED_APPROVED":
    fail("STATUS")

h = r["exact_human_review"]

if h["decision_counts"] != {
    "PASS": 10,
    "REVISION_REQUIRED": 0,
    "FAIL": 0
}:
    fail("COUNTS")

for i in range(1, 11):
    if h["item_decisions"][f"V4-RR{i:02d}"] != "PASS":
        fail("RECORDED_ITEM_DECISION")

if h["overall_decision"] != \
   "APPROVE_V4_RR10_CORRECTED_SCHEMA_INSUFFICIENCY_PROOF":
    fail("RECORDED_OVERALL")

if h["synthetic_or_assistant_generated"] is not False:
    fail("SYNTHETIC")

if h["quarantined_evidence_used"] is not False:
    fail("QUARANTINE_REVIEW")

t = r["technical_interpretation"]

if t["exact_v4_approved"] is not True:
    fail("V4_APPROVAL")

if t[
    "scoped_frozen_schema_insufficiency_conclusion_independently_approved"
] is not True:
    fail("SCOPED_CONCLUSION")

if t["canonical_schema_successor_technically_required"] is not True:
    fail("SCHEMA_SUCCESSOR_TECHNICAL_NEED")

for key in (
    "canonical_schema_successor_authorized",
    "canonical_schema_modification_authorized",
    "positive_mapping_authorized",
    "curl_json_materialization_authorized",
    "analyzer_implementation_authorized",
    "analyzer_execution_authorized",
    "baseline_execution_authorized",
    "repair_authorized",
):
    if t[key] is not False:
        fail("UNAUTHORIZED|" + key)

for key, value in r["evidence_quarantine"].items():
    if value is not False:
        fail("QUARANTINE|" + key)

if r["next_boundary"] != \
   "AUTHORIZE_CURL_CANONICAL_SCHEMA_SUCCESSOR_AUTHORING":
    fail("NEXT_BOUNDARY")

if curlp.exists():
    fail("CURL_JSON_EXISTS")

print("EXACT_COMPLETED_V4_HUMAN_REVIEW_SHA256=PASS")
print("HUMAN_REVIEW_ITEM_COUNTS=10_PASS_0_REVISION_REQUIRED_0_FAIL")
print("OVERALL_TECHNICAL_REVIEW_DECISION=APPROVE_V4_RR10_CORRECTED_SCHEMA_INSUFFICIENCY_PROOF")
print("V4_RR01_TO_V4_RR10=PASS")
print("EXACT_V4_APPROVED=YES")
print("SCOPED_FROZEN_SCHEMA_INSUFFICIENCY_CONCLUSION_INDEPENDENTLY_APPROVED=YES")
print("CANONICAL_SCHEMA_SUCCESSOR_TECHNICALLY_REQUIRED=YES")
print("CANONICAL_SCHEMA_SUCCESSOR_AUTHORIZED=NO")
print("POSITIVE_MAPPING_AUTHORIZED=NO")
print("CURL_JSON_MATERIALIZATION_AUTHORIZED=NO")
print("ANALYZER_IMPLEMENTATION_AUTHORIZED=NO")
print("BASELINE_EXECUTION_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
print("COMPLETED_V4_HUMAN_REVIEW_RECORD_VERIFICATION=PASS")
