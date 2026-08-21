#!/usr/bin/env python3

import hashlib
import json
import re
import subprocess
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

review = here / "01_completed_hash_contract_finalization_human_review.APPROVED.v1.md"
handoff = here / "02_hash_finalization_handoff_manifest.v1.json"
proof = here / "03_postcommit_package_noninterference_proof"
recordp = here / "04_completed_hash_contract_finalization_human_approval_record.v1.json"

package = (
    repo /
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2/"
    "schema_v2_hash_contract_finalization_package_v1"
)

active_form = package / "02_active_form_v2_hash_contract.REVIEW_CANDIDATE.json"

active_path = repo / "config/protocol_content_hash_canonicalization.v2.json"
curl_json = repo / "config/protocol_specifications/curl.json"

if sha(review) != \
   "c1e0284dc6ca14dc1194c7afc7e280ac52f908eabe24c4f9567651f24717da67":
    fail("REVIEW_SHA")

if review.stat().st_size != 5952:
    fail("REVIEW_SIZE")

if sha(handoff) != \
   "1466dc7845612e386596968abe4b7c475a9d38d8136ff6e93a7fe8ff1bc80a3d":
    fail("HANDOFF_SHA")

if sha(
    proof / "00_postcommit_noninterference_manifest.v1.json"
) != "7ca1e62e058053b5251c345b778f3e8f57008cb62171abbee8f02e59703b9b5a":
    fail("POSTPROOF_MANIFEST")

if sha(
    proof /
    "97_postcommit_hash_finalization_package_noninterference.v1.SHA256SUMS"
) != "ef196eb76b24564035fdbd90a7843658c8b6955af8b1eb1175d3b028c69be8f8":
    fail("POSTPROOF_SUMS")

subprocess.check_call(
    [
        "python3",
        str(
            proof /
            "99_verify_postcommit_hash_finalization_package_noninterference.v1.py"
        )
    ],
    stdout=subprocess.DEVNULL
)

if sha(
    package /
    "18_schema_v2_hash_contract_finalization_package_manifest.v1.json"
) != "b5c3ea2758b16f911947bc902e709b9026b9733e004d1e49b1389ff301c18f13":
    fail("PACKAGE_MANIFEST")

if sha(
    package /
    "19_schema_v2_hash_contract_finalization_package.v1.SHA256SUMS"
) != "e8adcd3725a3623b05879bed89c176155794e71085f97615b0b054577cc42b37":
    fail("PACKAGE_SUMS")

if sha(active_form) != \
   "37f035bb617f5598a0e368ba3b60b4bf1e69e4e69ce2f1053d71c0fcc96619e9":
    fail("ACTIVE_FORM_SHA")

if active_form.stat().st_size != 3154:
    fail("ACTIVE_FORM_SIZE")

text = review.read_text(
    encoding="utf-8"
).replace("\r\n", "\n").replace("\r", "\n")

for i in range(1, 9):
    rid = f"HF{i:02d}"

    h = re.search(
        r"^##\s+" + re.escape(rid) + r"\b[^\n]*$",
        text,
        re.M
    )

    if not h:
        fail("HF|" + rid)

    tail = text[h.end():]
    nxt = re.search(r"^##\s+", tail, re.M)
    section = tail[:nxt.start()] if nxt else tail

    vals = re.findall(
        r"^Decision:[ \t]*(PASS|REVISION_REQUIRED|FAIL)[ \t]*$",
        section,
        re.M
    )

    if vals != ["PASS"]:
        fail("HF_DECISION|" + rid)

overall = re.findall(
    r"^Overall decision:[ \t]*"
    r"(APPROVE_SCHEMA_V2_HASH_CONTRACT_ACTIVE_FORM|REVISION_REQUIRED|FAIL)"
    r"[ \t]*$",
    text,
    re.M
)

if overall != ["APPROVE_SCHEMA_V2_HASH_CONTRACT_ACTIVE_FORM"]:
    fail("OVERALL")

r = json.loads(recordp.read_text(encoding="utf-8"))

if r["status"] != \
   "SCHEMA_V2_HASH_CONTRACT_ACTIVE_FORM_HUMAN_APPROVED_NOT_INSTALLED_NOT_ACTIVATED":
    fail("STATUS")

hr = r["completed_human_review"]

if hr["final_counts"] != {
    "PASS": 8,
    "REVISION_REQUIRED": 0,
    "FAIL": 0,
}:
    fail("COUNTS")

if hr["overall_decision"] != \
   "APPROVE_SCHEMA_V2_HASH_CONTRACT_ACTIVE_FORM":
    fail("RECORD_OVERALL")

for i in range(1, 9):
    if hr[f"HF{i:02d}"] != "PASS":
        fail("RECORD_HF")

af = r["approved_active_form"]

if af["sha256"] != \
   "37f035bb617f5598a0e368ba3b60b4bf1e69e4e69ce2f1053d71c0fcc96619e9":
    fail("RECORD_ACTIVE_FORM_SHA")

if af["size_bytes"] != 3154:
    fail("RECORD_ACTIVE_FORM_SIZE")

if af["canonical_json_sha256"] != \
   "8f90f681c8942471ee05afc8d1fbb12d8208858163bc7f59695c26a82d48c4f6":
    fail("RECORD_CANONICAL_SHA")

if af["exact_delta_count"] != 3:
    fail("DELTA_COUNT")

if af["human_approved"] is not True:
    fail("HUMAN_APPROVED")

if af["installed_at_active_path"] is not False:
    fail("PREMATURE_INSTALL")

g = r["governance_interpretation"]

required_false = (
    "active_v2_hash_contract_created",
    "active_v2_hash_contract_installation_authorized_by_this_record",
    "schema_v2_activated",
    "schema_v2_activation_authorized_by_this_record",
    "decision_0019_superseded",
    "decision_0019_successor_adopted",
    "version_dispatch_policy_activated",
    "positive_v4_to_v2_mapping_defined",
    "positive_v4_to_v2_mapping_authorized",
    "curl_json_created",
    "analyzer_implementation_authorized",
    "analyzer_execution_authorized",
    "baseline_execution_authorized",
    "repair_authorized",
)

if g["hash_contract_active_form_human_approved"] is not True:
    fail("APPROVAL_INTERPRETATION")

for key in required_false:
    if g[key] is not False:
        fail("NONAUTH|" + key)

if active_path.exists():
    fail("ACTIVE_V2_HASH_EXISTS")

if curl_json.exists():
    fail("CURL_JSON_EXISTS")

if r["next_boundary"] != \
   "PREFLIGHT_SCHEMA_V2_ACTIVATION_AFTER_HASH_FINALIZATION_HUMAN_APPROVAL":
    fail("NEXT_BOUNDARY")

print("EXACT_COMPLETED_HASH_FINALIZATION_HUMAN_APPROVAL=PASS")
print("HF01_TO_HF08_FINAL_COUNTS=8_PASS_0_REVISION_REQUIRED_0_FAIL")
print("HASH_FINALIZATION_ACTIVE_FORM_HUMAN_APPROVED=YES")
print("ACTIVE_V2_HASH_CONTRACT_CREATED=NO")
print("SCHEMA_V2_ACTIVATED=NO")
print("POSITIVE_V4_TO_V2_MAPPING_DEFINED=NO")
print("CURL_JSON_CREATED=NO")
print("COMPLETED_HASH_FINALIZATION_HUMAN_APPROVAL_RECORD_VERIFICATION=PASS")
