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

V2_SHA = "c6ebb5ef2214c4168283f9009d1f7ce6e88d2ff928853fe6a57ed1f7521c6956"
ZLIB_SHA = "f4c94c1c151b893e2e4f1fae7d43b1196432cbcceaa7f9428968d45f2f77b7b1"
PCAP_SHA = "b2877713a3d8c38ecf135544f4cab7a2230e39b4ed73e18a7965497b3901ef73"
REREVIEW_SHA = "80852675eeb63508644e20caa4b7c6fdd5d73cd361bd9b072474e12521c3ac40"
REREVIEW_RECORD_SHA = "01486959b88c17e4f4259d8fd3d6b45177081b6d85aeb83784b6c221b7b514c9"
AUTH_SHA = "720ee16cc35082ef347799f0b24a64b1ef3b7234086104eb471b78c1e568162e"
PKG2_MANIFEST_SHA = "68902be116599ff915b8efadcb58b4fbb3107d4abf35d330d723c42f69922bd4"
PKG2_SUMS_SHA = "de583d227d8869bafda83219bab02c02ca718129d9209626e39dc1ed4f52fdcf"

checks = {
    "03_exact_unchanged_protocol_specification_schema_v2_candidate.json":
        V2_SHA,
    "04_exact_frozen_zlib_canonical_specification.json":
        ZLIB_SHA,
    "05_exact_frozen_libpcap_canonical_specification.json":
        PCAP_SHA,
    "06_prior_completed_corrective_rereview.REVISION_REQUIRED.v2.md":
        REREVIEW_SHA,
    "07_prior_corrective_rereview_record.v2.json":
        REREVIEW_RECORD_SHA,
    "10_review_package_v3_authorization.v1.json":
        AUTH_SHA,
    "12_review_package_v2_manifest.v2.json":
        PKG2_MANIFEST_SHA,
    "13_review_package_v2_checksum_manifest.v2.SHA256SUMS":
        PKG2_SUMS_SHA,
}

for rel, expected in checks.items():
    p = here / rel
    if not p.exists():
        fail("MISSING|" + rel)
    if sha(p) != expected:
        fail("SHA|" + rel)

if (
    here /
    "03_exact_unchanged_protocol_specification_schema_v2_candidate.json"
).stat().st_size != 43030:
    fail("SCHEMA_V2_SIZE")

subprocess.check_call(
    [
        "python3",
        str(
            here /
            "14_package_v2_checkpoint_parent_git_proof/"
            "99_verify_package_v2_checkpoint_parent_proof.v1.py"
        )
    ]
)

binding = json.loads(
    (here / "01_package_binding.v3.json")
    .read_text(encoding="utf-8")
)

if binding["scope"] != "SV2-RR09-EVIDENCE-ONLY":
    fail("SCOPE")

if binding["schema_v2"]["changed"] is not False:
    fail("SCHEMA_V2_CHANGED")

if binding["review_package_v2"]["changed_or_patched"] is not False:
    fail("PACKAGE_V2_PATCHED")

if binding["prior_review_state"]["sv2_rr02"] != "PASS_CLOSED":
    fail("RR02_STATUS")

if binding["prior_review_state"]["sv2_rr09"] != \
   "REVISION_REQUIRED_OPEN":
    fail("RR09_STATUS")

if binding["postcommit_v3_noninterference_handoff_proof_required"] is not True:
    fail("POSTCOMMIT_PROOF_REQUIREMENT")

if binding["postcommit_proof_must_not_modify_package_v3"] is not True:
    fail("POSTCOMMIT_PACKAGE_MUTABILITY")

if binding["schema_v2_activated"] is not False:
    fail("SCHEMA_ACTIVATED")

if binding["positive_v4_to_v2_mapping_defined"] is not False:
    fail("POSITIVE_MAPPING")

if binding["curl_json_created"] is not False:
    fail("CURL_JSON")

if binding["synthetic_human_decision"] is not False:
    fail("SYNTHETIC_DECISION")

packet = (
    here / "02_rr09_reviewer_packet.BLANK.v3.md"
).read_text(
    encoding="utf-8"
).replace(
    "\r\n", "\n"
).replace(
    "\r", "\n"
)

h = re.search(
    r"^###\s+SV2-RR09-FINAL-CORRECTIVE\b[^\n]*$",
    packet,
    re.M
)

if not h:
    fail("RR09_HEADING")

tail = packet[h.end():]

nxt = re.search(
    r"^##\s+New overall technical review decision\b",
    tail,
    re.M
)

section = tail[:nxt.start()] if nxt else tail

vals = re.findall(
    r"^Decision:[ \t]*(.*?)[ \t]*$",
    section,
    re.M
)

if len(vals) != 1 or vals[0].strip():
    fail("RR09_DECISION_NOT_BLANK")

overall = re.findall(
    r"^Overall decision:[ \t]*(.*?)[ \t]*$",
    packet,
    re.M
)

if len(overall) != 1 or overall[0].strip():
    fail("OVERALL_NOT_BLANK")

for label in (
    "Human reviewer name",
    "Human reviewer signature / recorded confirmation",
    "Human reviewer date",
):
    vals = re.findall(
        "^" + re.escape(label)
        + r":[ \t]*(.*?)[ \t]*$",
        packet,
        re.M
    )
    if len(vals) != 1 or vals[0].strip():
        fail("IDENTITY_NOT_BLANK|" + label)

manifest = json.loads(
    (here / "17_corrective_review_package_manifest.v3.json")
    .read_text(encoding="utf-8")
)

if manifest["scope"] != "SV2-RR09-EVIDENCE-ONLY":
    fail("MANIFEST_SCOPE")

if manifest["schema_v2_changed"] is not False:
    fail("MANIFEST_SCHEMA_CHANGED")

if manifest["human_decisions_initially_blank"] is not True:
    fail("MANIFEST_HUMAN_STATE")

if manifest["postcommit_v3_noninterference_handoff_proof_required"] is not True:
    fail("MANIFEST_POSTCOMMIT_PROOF")

for item in manifest["files"]:
    p = here / item["path"]
    if sha(p) != item["sha256"]:
        fail("MANIFEST_FILE_SHA|" + item["path"])
    if p.stat().st_size != item["size_bytes"]:
        fail("MANIFEST_FILE_SIZE|" + item["path"])

print("EXACT_UNCHANGED_SCHEMA_V2_CANDIDATE=PASS")
print("EXACT_FROZEN_ZLIB_CANONICAL_SPECIFICATION=PASS")
print("EXACT_FROZEN_LIBPCAP_CANONICAL_SPECIFICATION=PASS")
print("PRIOR_RR02_PASS_CLOSED_BINDING=PASS")
print("PRIOR_RR09_REVISION_REQUIRED_BINDING=PASS")
print("PACKAGE_V2_CHECKPOINT_PARENT_RR09_EVIDENCE=PASS")
print("SV2_RR09_REVIEW_DECISION_INITIAL_STATE=BLANK")
print("OVERALL_REVIEW_DECISION_INITIAL_STATE=BLANK")
print("REVIEWER_IDENTITY_INITIAL_STATE=BLANK")
print("POSTCOMMIT_V3_NONINTERFERENCE_HANDOFF_PROOF_REQUIRED=YES")
print("SYNTHETIC_HUMAN_DECISION=NO")
print("SCHEMA_V2_ACTIVATED=NO")
print("POSITIVE_V4_TO_V2_MAPPING_DEFINED=NO")
print("CURL_JSON_CREATED=NO")
print("SELF_CONTAINED_CORRECTIVE_REVIEW_PACKAGE_V3_VERIFICATION=PASS")
