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

review = here / "01_completed_v2_human_review.REVISION_REQUIRED.v1.md"
recordp = here / "02_completed_v2_human_review_record.v1.json"
v2 = repo / "config/annotation/curl_canonical_representation_mapping_contract.v2.json"
curl = repo / "config/protocol_specifications/curl.json"

REVIEW_SHA = "d688196db67da6cf9e359046ab612e78117fc54c9166122a9523729270df50d5"
V2_SHA = "f2badbc07895e8baff078a0ce617ceb6ff02d39c7634a9e38b3b8a46a18d811c"

if sha(review) != REVIEW_SHA:
    fail("REVIEW_SHA")

if review.stat().st_size != 25643:
    fail("REVIEW_SIZE")

if sha(v2) != V2_SHA:
    fail("V2_SHA")

r = json.loads(recordp.read_text(encoding="utf-8"))

if r["status"] != "COMPLETED_HUMAN_REVIEW_RECORDED_REVISION_REQUIRED":
    fail("STATUS")

h = r["exact_human_review"]

if h["decision_counts"] != {
    "PASS": 8,
    "REVISION_REQUIRED": 2,
    "FAIL": 0
}:
    fail("COUNTS")

if h["overall_decision"] != "REVISION_REQUIRED":
    fail("OVERALL")

if h["item_decisions"]["V2-RR01"] != "REVISION_REQUIRED":
    fail("RR01")

if h["item_decisions"]["V2-RR08"] != "REVISION_REQUIRED":
    fail("RR08")

if h["human_reviewer_name"] != "Abdul Raheem Shahzad":
    fail("NAME")

if h["human_reviewer_confirmation"] != "ARS":
    fail("CONFIRMATION")

if h["human_reviewer_date"] != "20 / August / 2026":
    fail("DATE")

if h["synthetic_or_assistant_generated"] is not False:
    fail("SYNTHETIC")

if r["review_findings"]["rr01"]["local_repository_followup_verification"] != "PASS":
    fail("RR01_LOCAL_FOLLOWUP")

if r["review_findings"]["rr01"]["local_followup_changes_human_decision"] is not False:
    fail("RR01_DECISION_MUTATION")

if r["review_findings"]["rr08"]["v2_in_place_edit_authorized"] is not False:
    fail("RR08_IN_PLACE_EDIT")

t = r["technical_interpretation"]

if t["schema_insufficiency_conclusion_rejected"] is not False:
    fail("CONCLUSION_INTERPRETATION")

if t["exact_v2_approved"] is not False:
    fail("V2_APPROVAL")

if t["exact_v2_revision_required"] is not True:
    fail("V2_REVISION")

if t["canonical_schema_successor_authorized"] is not False:
    fail("SCHEMA_SUCCESSOR")

if t["curl_json_materialization_authorized"] is not False:
    fail("MATERIALIZATION")

for k, v in r["evidence_quarantine"].items():
    if v is not False:
        fail("QUARANTINE|" + k)

if curl.exists():
    fail("CURL_JSON_EXISTS")

print("EXACT_COMPLETED_V2_HUMAN_REVIEW_SHA256=PASS")
print("HUMAN_REVIEW_ITEM_COUNTS=8_PASS_2_REVISION_REQUIRED_0_FAIL")
print("OVERALL_TECHNICAL_REVIEW_DECISION=REVISION_REQUIRED")
print("RR01_LOCAL_GIT_FOLLOWUP=PASS")
print("RR01_HUMAN_DECISION_CHANGED=NO")
print("RR08_SUCCESSOR_CORRECTION_REQUIRED=YES")
print("EXACT_V2_APPROVED=NO")
print("EXACT_V2_IMMUTABLE=YES")
print("CANONICAL_SCHEMA_SUCCESSOR_AUTHORIZED=NO")
print("CURL_JSON_CREATED=NO")
print("COMPLETED_V2_HUMAN_REVIEW_RECORD_VERIFICATION=PASS")
