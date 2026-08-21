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

reviewp = (
    here /
    "01_completed_schema_v2_corrective_human_rereview."
    "REVISION_REQUIRED.v2.md"
)

recordp = (
    here /
    "02_completed_schema_v2_corrective_human_rereview_record.v2.json"
)

v2p = repo / "config/schemas/protocol_specification.v2.schema.json"
v1p = repo / "config/schemas/protocol_specification.schema.json"

zlibp = repo / "config/protocol_specifications/zlib.json"
pcapp = repo / "config/protocol_specifications/libpcap.json"

pkg2 = (
    repo /
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2/"
    "review_package_v2"
)

curlp = repo / "config/protocol_specifications/curl.json"

REVIEW_SHA = "80852675eeb63508644e20caa4b7c6fdd5d73cd361bd9b072474e12521c3ac40"
V2_SHA = "c6ebb5ef2214c4168283f9009d1f7ce6e88d2ff928853fe6a57ed1f7521c6956"
V1_SHA = "7eb17eeb8f49b37420d0d1d71539cf0d7cb08241ecf133e7b4139fd130718b34"
ZLIB_SHA = "f4c94c1c151b893e2e4f1fae7d43b1196432cbcceaa7f9428968d45f2f77b7b1"
PCAP_SHA = "b2877713a3d8c38ecf135544f4cab7a2230e39b4ed73e18a7965497b3901ef73"

PKG2_MANIFEST_SHA = "68902be116599ff915b8efadcb58b4fbb3107d4abf35d330d723c42f69922bd4"
PKG2_SUMS_SHA = "de583d227d8869bafda83219bab02c02ca718129d9209626e39dc1ed4f52fdcf"

PKG2_COMMIT = "75dd1d9c5a3d01d72b76f9d76e8abb56113187e5"
PKG2_TREE = "d2bc2301cea0ef87aeae7b37278ba1d5440aae57"
PKG2_PARENT = "bf6cf53d54c105353906f02c6fa117668b635eae"

if sha(reviewp) != REVIEW_SHA:
    fail("REVIEW_SHA")

if reviewp.stat().st_size != 5413:
    fail("REVIEW_SIZE")

if sha(v2p) != V2_SHA:
    fail("V2_SHA")

if v2p.stat().st_size != 43030:
    fail("V2_SIZE")

if sha(v1p) != V1_SHA:
    fail("V1_SHA")

if sha(zlibp) != ZLIB_SHA:
    fail("ZLIB_SHA")

if sha(pcapp) != PCAP_SHA:
    fail("LIBPCAP_SHA")

if sha(pkg2 / "14_corrective_review_package_manifest.v2.json") != \
   PKG2_MANIFEST_SHA:
    fail("PKG2_MANIFEST_SHA")

if sha(pkg2 / "16_corrective_review_package.v2.SHA256SUMS") != \
   PKG2_SUMS_SHA:
    fail("PKG2_SUMS_SHA")

actual_tree = subprocess.check_output(
    [
        "git",
        "-C",
        str(repo),
        "rev-parse",
        PKG2_COMMIT + "^{tree}",
    ],
    text=True
).strip()

if actual_tree != PKG2_TREE:
    fail("PKG2_TREE")

actual_parent = subprocess.check_output(
    [
        "git",
        "-C",
        str(repo),
        "show",
        "-s",
        "--format=%P",
        PKG2_COMMIT,
    ],
    text=True
).strip()

if actual_parent != PKG2_PARENT:
    fail("PKG2_PARENT")

record = json.loads(
    recordp.read_text(encoding="utf-8")
)

if record["status"] != \
   "COMPLETED_CORRECTIVE_HUMAN_REREVIEW_RECORDED_REVISION_REQUIRED":
    fail("RECORD_STATUS")

cr = record["completed_corrective_human_rereview"]

if cr["sha256"] != REVIEW_SHA:
    fail("RECORD_REVIEW_SHA")

if cr["size_bytes"] != 5413:
    fail("RECORD_REVIEW_SIZE")

if cr["corrective_decisions"] != {
    "SV2-RR02-CORRECTIVE":
        "PASS",

    "SV2-RR09-CORRECTIVE":
        "REVISION_REQUIRED",
}:
    fail("CORRECTIVE_DECISIONS")

if cr["corrective_counts"] != {
    "PASS": 1,
    "REVISION_REQUIRED": 1,
    "FAIL": 0,
}:
    fail("CORRECTIVE_COUNTS")

if cr["aggregate_counts"] != {
    "PASS": 9,
    "REVISION_REQUIRED": 1,
    "FAIL": 0,
}:
    fail("AGGREGATE_COUNTS")

if cr["overall_decision"] != "REVISION_REQUIRED":
    fail("OVERALL")

t = record["technical_interpretation"]

expected_true = (
    "schema_v2_candidate_must_remain_immutable",
    "review_package_v2_must_remain_immutable",
    "sv2_rr02_corrective_closed",
    "corrective_review_package_v3_successor_required",
)

for key in expected_true:
    if t[key] is not True:
        fail("TECH_TRUE|" + key)

expected_false = (
    "schema_v2_candidate_approved",
    "schema_v2_candidate_rejected",
    "schema_v2_candidate_content_change_required",
    "review_package_v2_patch_in_place_allowed",
    "sv2_rr09_corrective_closed",
)

for key in expected_false:
    if t[key] is not False:
        fail("TECH_FALSE|" + key)

if t["remaining_revision_scope"] != "SV2-RR09-EVIDENCE-ONLY":
    fail("REMAINING_SCOPE")

for key, value in record["explicit_non_authorizations"].items():
    if value is not False:
        fail("NONAUTH|" + key)

if record["next_boundary"] != \
   "AUTHORIZE_SCHEMA_V2_CORRECTIVE_REVIEW_PACKAGE_V3_FOR_SV2_RR09_ONLY":
    fail("NEXT_BOUNDARY")

text = (
    reviewp.read_text(encoding="utf-8")
    .replace("\r\n", "\n")
    .replace("\r", "\n")
)

expected_decisions = {
    "SV2-RR02-CORRECTIVE": "PASS",
    "SV2-RR09-CORRECTIVE": "REVISION_REQUIRED",
}

for rr, wanted in expected_decisions.items():
    h = re.search(
        rf"^###\s+{re.escape(rr)}\b[^\n]*$",
        text,
        re.M
    )

    if not h:
        fail("HEADING|" + rr)

    tail = text[h.end():]

    nxt = re.search(
        r"^###\s+SV2-RR\d{2}-CORRECTIVE\b[^\n]*$|"
        r"^##\s+New overall technical review decision\b",
        tail,
        re.M
    )

    section = tail[:nxt.start()] if nxt else tail

    vals = re.findall(
        r"^Decision:[ \t]*(PASS|REVISION_REQUIRED|FAIL)[ \t]*$",
        section,
        re.M
    )

    if len(vals) != 1 or vals[0] != wanted:
        fail("DECISION|" + rr)

required = {
    "Overall decision":
        "REVISION_REQUIRED",

    "Human reviewer role":
        "Spec-Technical-Reviewer-1",

    "Human reviewer name":
        "Abdul Raheem Shahzad",

    "Human reviewer signature / recorded confirmation":
        "ARS",

    "Human reviewer date":
        "21 / August / 2026",
}

for label, wanted in required.items():
    vals = re.findall(
        "^" + re.escape(label)
        + r":[ \t]*(.*?)[ \t]*$",
        text,
        re.M
    )

    if len(vals) != 1 or vals[0].strip() != wanted:
        fail("FIELD|" + label)

if curlp.exists():
    fail("CURL_JSON_EXISTS")

print("EXACT_COMPLETED_SCHEMA_V2_CORRECTIVE_REREVIEW=PASS")
print("SV2_RR02_CORRECTIVE=PASS_CLOSED")
print("SV2_RR09_CORRECTIVE=REVISION_REQUIRED_OPEN")
print("CORRECTIVE_REVIEW_COUNTS=1_PASS_1_REVISION_REQUIRED_0_FAIL")
print("AGGREGATE_REVIEW_STATE=9_PASS_1_REVISION_REQUIRED_0_FAIL")
print("SCHEMA_V2_CANDIDATE_APPROVED=NO")
print("SCHEMA_V2_CANDIDATE_REJECTED=NO")
print("SCHEMA_V2_CANDIDATE_CONTENT_CHANGE_REQUIRED=NO")
print("SCHEMA_V2_CANDIDATE_MUST_REMAIN_IMMUTABLE=YES")
print("REVIEW_PACKAGE_V2_MUST_REMAIN_IMMUTABLE=YES")
print("REMAINING_CORRECTION_SCOPE=SV2_RR09_EVIDENCE_ONLY")
print("CORRECTIVE_REVIEW_PACKAGE_V3_SUCCESSOR_REQUIRED=YES")
print("SCHEMA_V2_ACTIVATED=NO")
print("POSITIVE_V4_TO_V2_MAPPING_DEFINED=NO")
print("CURL_JSON_CREATED=NO")
print("COMPLETED_SCHEMA_V2_CORRECTIVE_REREVIEW_RECORD_VERIFICATION=PASS")
