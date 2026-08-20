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
    "01_completed_schema_v2_human_review.REVISION_REQUIRED.v1.md"
)

recordp = (
    here /
    "02_completed_schema_v2_human_review_record.v1.json"
)

v2p = repo / "config/schemas/protocol_specification.v2.schema.json"
v1p = repo / "config/schemas/protocol_specification.schema.json"

pkg = (
    repo /
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2/"
    "review_package_v1"
)

curlp = repo / "config/protocol_specifications/curl.json"

REVIEW_SHA = "19e94cf48cbe9b5df537feb2abb350a80bfcef752e4da4d8bed3282077d67c98"
V2_SHA = "c6ebb5ef2214c4168283f9009d1f7ce6e88d2ff928853fe6a57ed1f7521c6956"
V1_SHA = "7eb17eeb8f49b37420d0d1d71539cf0d7cb08241ecf133e7b4139fd130718b34"
PKG_MANIFEST_SHA = "3bb3f044b4b8e3d62a84dfc621c3512cf064796ca58cd0422ad4bcde50f39ed0"
PKG_SUMS_SHA = "560858b14dec0d3c693062547eab3a00a954ba08d4413696be3e0828151cf0c3"

if sha(reviewp) != REVIEW_SHA:
    fail("REVIEW_SHA")

if reviewp.stat().st_size != 8404:
    fail("REVIEW_SIZE")

if sha(v2p) != V2_SHA:
    fail("V2_SHA")

if v2p.stat().st_size != 43030:
    fail("V2_SIZE")

if sha(v1p) != V1_SHA:
    fail("V1_SHA")

if sha(pkg / "19_review_package_manifest.v1.json") != PKG_MANIFEST_SHA:
    fail("PACKAGE_MANIFEST_SHA")

if sha(pkg / "21_review_package.v1.SHA256SUMS") != PKG_SUMS_SHA:
    fail("PACKAGE_SUMS_SHA")

record = json.loads(recordp.read_text(encoding="utf-8"))

if record["status"] != \
   "COMPLETED_HUMAN_REVIEW_RECORDED_REVISION_REQUIRED":
    fail("RECORD_STATUS")

if record["review_target"]["sha256"] != V2_SHA:
    fail("RECORD_TARGET_SHA")

if record["completed_human_review"]["sha256"] != REVIEW_SHA:
    fail("RECORD_REVIEW_SHA")

if record["completed_human_review"]["size_bytes"] != 8404:
    fail("RECORD_REVIEW_SIZE")

if record["completed_human_review"]["decision_counts"] != {
    "PASS": 8,
    "REVISION_REQUIRED": 2,
    "FAIL": 0,
}:
    fail("RECORD_COUNTS")

expected = {
    "SV2-RR01": "PASS",
    "SV2-RR02": "REVISION_REQUIRED",
    "SV2-RR03": "PASS",
    "SV2-RR04": "PASS",
    "SV2-RR05": "PASS",
    "SV2-RR06": "PASS",
    "SV2-RR07": "PASS",
    "SV2-RR08": "PASS",
    "SV2-RR09": "REVISION_REQUIRED",
    "SV2-RR10": "PASS",
}

if record["completed_human_review"]["decisions"] != expected:
    fail("RECORD_DECISION_VECTOR")

if record["completed_human_review"]["overall_decision"] != \
   "REVISION_REQUIRED":
    fail("RECORD_OVERALL")

t = record["technical_interpretation"]

if t["schema_v2_candidate_technically_approved"] is not False:
    fail("TECH_APPROVED")

if t["schema_v2_candidate_rejected"] is not False:
    fail("TECH_REJECTED")

if t["schema_v2_candidate_requires_content_change"] is not False:
    fail("TECH_CONTENT_CHANGE")

if t["revision_is_review_package_evidence_scope"] is not True:
    fail("TECH_EVIDENCE_SCOPE")

if t["schema_v2_candidate_must_remain_immutable"] is not True:
    fail("TECH_V2_IMMUTABILITY")

if t["review_package_v1_must_remain_immutable"] is not True:
    fail("TECH_PACKAGE_IMMUTABILITY")

if t["corrective_review_package_successor_required"] is not True:
    fail("TECH_SUCCESSOR_REQUIRED")

if t[
    "corrective_scope_limited_to_rr02_rr09_evidence_deficiencies"
] is not True:
    fail("TECH_CORRECTIVE_SCOPE")

for key, value in record["explicit_non_authorizations"].items():
    if value is not False:
        fail("NONAUTH|" + key)

if record["next_boundary"] != \
   "AUTHORIZE_SCHEMA_V2_CORRECTIVE_REVIEW_PACKAGE_SUCCESSOR_FOR_RR02_RR09_ONLY":
    fail("NEXT_BOUNDARY")

text = (
    reviewp.read_text(encoding="utf-8")
    .replace("\r\n", "\n")
    .replace("\r", "\n")
)

for rr, decision in expected.items():
    h = re.search(
        rf"^###\s+{rr}\b[^\n]*$",
        text,
        re.M
    )

    if not h:
        fail("REVIEW_HEADING|" + rr)

    tail = text[h.end():]

    nxt = re.search(
        r"^###\s+SV2-RR\d{2}\b[^\n]*$|"
        r"^##\s+Overall technical review decision\b",
        tail,
        re.M
    )

    section = tail[:nxt.start()] if nxt else tail

    m = re.search(
        r"^Decision:[ \t]*(PASS|REVISION_REQUIRED|FAIL)[ \t]*$",
        section,
        re.M
    )

    if not m or m.group(1) != decision:
        fail("REVIEW_DECISION|" + rr)

required_identity = {
    "Overall decision": "REVISION_REQUIRED",
    "Human reviewer role": "Spec-Technical-Reviewer-1",
    "Human reviewer name": "Abdul Raheem Shahzad",
    "Human reviewer signature / recorded confirmation": "ARS",
    "Human reviewer date": "20 / August / 2026",
}

for label, value in required_identity.items():
    m = re.search(
        "^" + re.escape(label)
        + r":[ \t]*(.*?)[ \t]*$",
        text,
        re.M
    )

    if not m or m.group(1).strip() != value:
        fail("IDENTITY|" + label)

actual_pkg_tree = subprocess.check_output(
    [
        "git",
        "-C",
        str(repo),
        "rev-parse",
        "41753d7f7b6f26836ff6c2a4b12bb13084f069e9^{tree}",
    ],
    text=True
).strip()

if actual_pkg_tree != \
   "143e16303264da0e1c97b1f68dc29c8ae64596e9":
    fail("PACKAGE_COMMIT_TREE")

if curlp.exists():
    fail("CURL_JSON_EXISTS")

print("EXACT_COMPLETED_SCHEMA_V2_HUMAN_REVIEW=PASS")
print("SCHEMA_V2_REVIEW_COUNTS=8_PASS_2_REVISION_REQUIRED_0_FAIL")
print("SCHEMA_V2_REVIEW_OUTCOME=REVISION_REQUIRED")
print("SV2_RR02_REVISION_REQUIRED=CONFIRMED")
print("SV2_RR09_REVISION_REQUIRED=CONFIRMED")
print("SCHEMA_V2_CANDIDATE_APPROVED=NO")
print("SCHEMA_V2_CANDIDATE_REJECTED=NO")
print("SCHEMA_V2_CANDIDATE_CONTENT_CHANGE_REQUIRED=NO")
print("SCHEMA_V2_CANDIDATE_MUST_REMAIN_IMMUTABLE=YES")
print("REVIEW_PACKAGE_V1_MUST_REMAIN_IMMUTABLE=YES")
print("CORRECTIVE_REVIEW_PACKAGE_SUCCESSOR_REQUIRED=YES")
print("SCHEMA_V2_ACTIVATED=NO")
print("POSITIVE_V4_TO_V2_MAPPING_DEFINED=NO")
print("CURL_JSON_CREATED=NO")
print("COMPLETED_SCHEMA_V2_HUMAN_REVIEW_RECORD_VERIFICATION=PASS")
