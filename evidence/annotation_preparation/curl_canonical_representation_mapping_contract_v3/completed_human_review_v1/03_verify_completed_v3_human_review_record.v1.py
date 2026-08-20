#!/usr/bin/env python3
import hashlib
import json
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

review = here / "01_completed_v3_human_review.REVISION_REQUIRED.v1.md"
recordp = here / "02_completed_v3_human_review_record.v1.json"
v3p = repo / "config/annotation/curl_canonical_representation_mapping_contract.v3.json"
curlp = repo / "config/protocol_specifications/curl.json"

REVIEW_SHA = "96afd2a552443ecbdb321f8087612a0771838216272cb8fd43d14f8b8e203b14"
V3_SHA = "ef401d5d04656f67ce4148c5cc6848368a9d68449f1296c64189d1422eebdb97"

if sha(review) != REVIEW_SHA:
    fail("REVIEW_SHA")

if review.stat().st_size != 19684:
    fail("REVIEW_SIZE")

if sha(v3p) != V3_SHA:
    fail("V3_SHA")

if v3p.stat().st_size != 24750:
    fail("V3_SIZE")

r = json.loads(recordp.read_text(encoding="utf-8"))

if r["status"] != "COMPLETED_HUMAN_REVIEW_RECORDED_REVISION_REQUIRED":
    fail("STATUS")

h = r["exact_human_review"]

if h["decision_counts"] != {
    "PASS": 9,
    "REVISION_REQUIRED": 1,
    "FAIL": 0
}:
    fail("COUNTS")

if h["overall_decision"] != "REVISION_REQUIRED":
    fail("OVERALL")

for i in range(1, 10):
    key = f"V3-RR{i:02d}"
    if h["item_decisions"][key] != "PASS":
        fail("EXPECTED_PASS|" + key)

if h["item_decisions"]["V3-RR10"] != "REVISION_REQUIRED":
    fail("RR10")

if h["human_reviewer_name"] != "Abdul Raheem Shahzad":
    fail("NAME")

if h["human_reviewer_confirmation"] != "ARS":
    fail("CONFIRMATION")

if h["human_reviewer_date"] != "20 / August / 2026":
    fail("DATE")

if h["synthetic_or_assistant_generated"] is not False:
    fail("SYNTHETIC")

rr10 = r["review_findings"]["V3-RR10"]

if rr10["defect"] != "STALE_INTERNAL_INDEPENDENT_REVIEW_TARGET":
    fail("RR10_DEFECT")

if rr10["actual_value"] != "Exact immutable V2 schema-insufficiency proof.":
    fail("RR10_VALUE")

if rr10["v3_in_place_edit_authorized"] is not False:
    fail("RR10_INPLACE")

t = r["technical_interpretation"]

if t["v2_rr01_problem_resolved_in_v3"] is not True:
    fail("V2_RR01_RESOLUTION")

if t["v2_rr08_problem_resolved_in_v3"] is not True:
    fail("V2_RR08_RESOLUTION")

if t["schema_insufficiency_conclusion_rejected"] is not False:
    fail("CONCLUSION")

if t["exact_v3_approved"] is not False:
    fail("V3_APPROVAL")

if t["exact_v3_revision_required"] is not True:
    fail("V3_REVISION")

if t["canonical_schema_successor_authorized"] is not False:
    fail("SCHEMA_SUCCESSOR")

if t["curl_json_materialization_authorized"] is not False:
    fail("CURL_AUTH")

for key, value in r["evidence_quarantine"].items():
    if value is not False:
        fail("QUARANTINE|" + key)

if curlp.exists():
    fail("CURL_JSON_EXISTS")

print("EXACT_COMPLETED_V3_HUMAN_REVIEW_SHA256=PASS")
print("HUMAN_REVIEW_ITEM_COUNTS=9_PASS_1_REVISION_REQUIRED_0_FAIL")
print("OVERALL_TECHNICAL_REVIEW_DECISION=REVISION_REQUIRED")
print("V3_RR01_TO_V3_RR09=PASS")
print("V3_RR10=REVISION_REQUIRED")
print("V2_RR01_PORTABILITY_PROBLEM_RESOLVED_IN_V3=YES")
print("V2_RR08_ACCOUNTING_PROBLEM_RESOLVED_IN_V3=YES")
print("SCOPED_SCHEMA_INSUFFICIENCY_CONCLUSION_REJECTED=NO")
print("V3_RR10_STALE_REVIEW_TARGET_RECORDED=YES")
print("EXACT_V3_APPROVED=NO")
print("EXACT_V3_IMMUTABLE=YES")
print("CANONICAL_SCHEMA_SUCCESSOR_AUTHORIZED=NO")
print("CURL_JSON_CREATED=NO")
print("COMPLETED_V3_HUMAN_REVIEW_RECORD_VERIFICATION=PASS")
