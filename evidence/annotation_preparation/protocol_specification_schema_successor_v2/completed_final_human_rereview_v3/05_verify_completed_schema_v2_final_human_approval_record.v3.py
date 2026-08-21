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
    return hashlib.sha256(
        p.read_bytes()
    ).hexdigest()

here = Path(__file__).resolve().parent
repo = here

while repo != repo.parent and not (repo / ".git").exists():
    repo = repo.parent

review = (
    here /
    "01_completed_schema_v2_rr09_final_human_rereview.APPROVED.v3.md"
)

handoff = (
    here /
    "02_rr09_final_handoff_manifest.v1.json"
)

proof = (
    here /
    "03_postcommit_v3_noninterference_proof"
)

recordp = (
    here /
    "04_completed_schema_v2_final_human_approval_record.v3.json"
)

pkg3 = (
    repo /
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2/"
    "review_package_v3"
)

v2 = (
    repo /
    "config/schemas/protocol_specification.v2.schema.json"
)

v1 = (
    repo /
    "config/schemas/protocol_specification.schema.json"
)

zlibp = (
    repo /
    "config/protocol_specifications/zlib.json"
)

pcapp = (
    repo /
    "config/protocol_specifications/libpcap.json"
)

curlp = (
    repo /
    "config/protocol_specifications/curl.json"
)

REVIEW_SHA = "d1ff72158d11886f5685ec65cd4da8023d0cf066d8f08e6fb57836e033bd0cee"
HANDOFF_SHA = "8eeec0ef1ead99fd7939e7c0f952047b05c4ca7e380a6ea27dcd6d1ac142d91a"

POST_MANIFEST_SHA = "106b80dc1baf94af95ef8af213d3ccebfbfc24d395c7ef2219889954cdd7f0de"
POST_SUMS_SHA = "54e5de95c7a4ae74942d34a517088d25a7dc5eb813a800035fc11bdc2fe27aec"

V2_SHA = "c6ebb5ef2214c4168283f9009d1f7ce6e88d2ff928853fe6a57ed1f7521c6956"
V1_SHA = "7eb17eeb8f49b37420d0d1d71539cf0d7cb08241ecf133e7b4139fd130718b34"
ZLIB_SHA = "f4c94c1c151b893e2e4f1fae7d43b1196432cbcceaa7f9428968d45f2f77b7b1"
PCAP_SHA = "b2877713a3d8c38ecf135544f4cab7a2230e39b4ed73e18a7965497b3901ef73"

PKG3_COMMIT = "3b07d7e661a94f664dd37b5fd54f85231a5c70ff"
PKG3_TREE = "1393d344b39d79714d400112ed5d454fcf2a9d2f"
PKG3_PARENT = "a48cab96025afa717c731a787104846272287856"

PKG3_MANIFEST_SHA = "a60c44547acd42842b236e5e50560c2e2fc34edd3a2c3ce0ab8a52b788ac3ec9"
PKG3_SUMS_SHA = "1daf9cacc46757ad974ce442ec147035871cbc0c253a0150ffaa54caa1415c5f"

if sha(review) != REVIEW_SHA:
    fail("FINAL_REVIEW_SHA")

if review.stat().st_size != 4384:
    fail("FINAL_REVIEW_SIZE")

if sha(handoff) != HANDOFF_SHA:
    fail("HANDOFF_MANIFEST_SHA")

if sha(
    proof /
    "00_postcommit_proof_manifest.v1.json"
) != POST_MANIFEST_SHA:
    fail("POSTPROOF_MANIFEST_SHA")

if sha(
    proof /
    "97_postcommit_v3_noninterference_proof.v1.SHA256SUMS"
) != POST_SUMS_SHA:
    fail("POSTPROOF_SUMS_SHA")

if sha(v2) != V2_SHA:
    fail("SCHEMA_V2_SHA")

if v2.stat().st_size != 43030:
    fail("SCHEMA_V2_SIZE")

if sha(v1) != V1_SHA:
    fail("SCHEMA_V1_SHA")

if sha(zlibp) != ZLIB_SHA:
    fail("ZLIB_SHA")

if sha(pcapp) != PCAP_SHA:
    fail("LIBPCAP_SHA")

if sha(
    pkg3 /
    "17_corrective_review_package_manifest.v3.json"
) != PKG3_MANIFEST_SHA:
    fail("PKG3_MANIFEST_SHA")

if sha(
    pkg3 /
    "18_corrective_review_package.v3.SHA256SUMS"
) != PKG3_SUMS_SHA:
    fail("PKG3_SUMS_SHA")

tree = subprocess.check_output(
    [
        "git",
        "-C",
        str(repo),
        "rev-parse",
        PKG3_COMMIT + "^{tree}"
    ],
    text=True
).strip()

if tree != PKG3_TREE:
    fail("PKG3_TREE")

parent = subprocess.check_output(
    [
        "git",
        "-C",
        str(repo),
        "show",
        "-s",
        "--format=%P",
        PKG3_COMMIT
    ],
    text=True
).strip()

if parent != PKG3_PARENT:
    fail("PKG3_PARENT")

subprocess.check_call(
    [
        "python3",
        str(
            proof /
            "99_verify_postcommit_v3_noninterference_proof.v1.py"
        )
    ],
    stdout=subprocess.DEVNULL
)

text = (
    review.read_text(encoding="utf-8")
    .replace("\r\n", "\n")
    .replace("\r", "\n")
)

h = re.search(
    r"^###\s+SV2-RR09-FINAL-CORRECTIVE\b[^\n]*$",
    text,
    re.M
)

if not h:
    fail("RR09_HEADING")

tail = text[h.end():]

nxt = re.search(
    r"^##\s+New overall technical review decision\b",
    tail,
    re.M
)

if nxt is None:
    fail("OVERALL_SECTION")

section = tail[:nxt.start()]

vals = re.findall(
    r"^Decision:[ \t]*(PASS|REVISION_REQUIRED|FAIL)[ \t]*$",
    section,
    re.M
)

if vals != ["PASS"]:
    fail("RR09_DECISION")

overall = re.findall(
    r"^Overall decision:[ \t]*"
    r"(APPROVE_PROTOCOL_SPECIFICATION_SCHEMA_V2_CANDIDATE|"
    r"REVISION_REQUIRED|FAIL)"
    r"[ \t]*$",
    text,
    re.M
)

if overall != [
    "APPROVE_PROTOCOL_SPECIFICATION_SCHEMA_V2_CANDIDATE"
]:
    fail("OVERALL_DECISION")

if "10 PASS / 0 REVISION_REQUIRED / 0 FAIL" not in text:
    fail("FINAL_COUNTS")

record = json.loads(
    recordp.read_text(
        encoding="utf-8"
    )
)

if record["status"] != \
   "FINAL_HUMAN_TECHNICAL_REVIEW_APPROVED_SCHEMA_V2_CANDIDATE":
    fail("RECORD_STATUS")

candidate = record[
    "schema_v2_candidate"
]

if candidate[
    "human_technical_review_approved"
] is not True:
    fail("CANDIDATE_APPROVAL")

if candidate[
    "content_change_required"
] is not False:
    fail("CONTENT_CHANGE")

if candidate[
    "must_remain_immutable"
] is not True:
    fail("CANDIDATE_IMMUTABILITY")

if candidate[
    "activated"
] is not False:
    fail("CANDIDATE_ACTIVATED")

final = record[
    "final_human_review"
]

if final["sha256"] != REVIEW_SHA:
    fail("RECORD_REVIEW_SHA")

if final[
    "sv2_rr09_final_corrective"
] != "PASS":
    fail("RECORD_RR09")

if final[
    "overall_decision"
] != "APPROVE_PROTOCOL_SPECIFICATION_SCHEMA_V2_CANDIDATE":
    fail("RECORD_OVERALL")

if final[
    "final_counts"
] != {
    "PASS": 10,
    "REVISION_REQUIRED": 0,
    "FAIL": 0
}:
    fail("RECORD_COUNTS")

items = record[
    "final_review_item_state"
]

if set(items.keys()) != {
    f"SV2-RR{i:02d}"
    for i in range(1, 11)
}:
    fail("REVIEW_ITEM_SET")

for key, value in items.items():
    if key in {
        "SV2-RR02",
        "SV2-RR09"
    }:
        if value != "PASS_CLOSED":
            fail("CLOSED_ITEM|" + key)
    elif value != "PASS":
        fail("PASS_ITEM|" + key)

g = record[
    "governance_interpretation"
]

if g[
    "schema_v2_candidate_human_approved"
] is not True:
    fail("GOV_APPROVED")

if g[
    "all_ten_schema_v2_review_items_pass"
] is not True:
    fail("GOV_ALL_PASS")

false_fields = (
    "schema_v2_candidate_rejected",
    "schema_v2_content_change_required",
    "schema_v2_activation_authorized_by_this_record",
    "schema_v2_activated",
    "decision_0019_superseded",
    "v2_hash_contract_activated",
    "positive_v4_to_v2_mapping_defined",
    "positive_v4_to_v2_mapping_authorized",
    "curl_json_created",
    "analyzer_implementation_authorized",
    "analyzer_execution_authorized",
    "baseline_execution_authorized",
    "repair_authorized",
)

for key in false_fields:
    if g[key] is not False:
        fail("NONAUTH|" + key)

if record[
    "next_boundary"
] != "AUTHORIZE_SCHEMA_V2_ACTIVATION_GOVERNANCE":
    fail("NEXT_BOUNDARY")

if curlp.exists():
    fail("CURL_JSON_EXISTS")

print("EXACT_FINAL_SCHEMA_V2_HUMAN_APPROVAL=PASS")
print("FINAL_SCHEMA_V2_REVIEW_COUNTS=10_PASS_0_REVISION_REQUIRED_0_FAIL")
print("SV2_RR02_STATUS=PASS_CLOSED")
print("SV2_RR09_STATUS=PASS_CLOSED")
print("SCHEMA_V2_CANDIDATE_HUMAN_APPROVED=YES")
print("SCHEMA_V2_CANDIDATE_CONTENT_CHANGE_REQUIRED=NO")
print("SCHEMA_V2_CANDIDATE_IMMUTABLE=YES")
print("SCHEMA_V2_ACTIVATED=NO")
print("DECISION_0019_SUPERSEDED=NO")
print("V2_HASH_CONTRACT_ACTIVATED=NO")
print("POSITIVE_V4_TO_V2_MAPPING_DEFINED=NO")
print("CURL_JSON_CREATED=NO")
print("FINAL_SCHEMA_V2_HUMAN_APPROVAL_RECORD_VERIFICATION=PASS")
