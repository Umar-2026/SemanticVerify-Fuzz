#!/usr/bin/env python3

import hashlib
import json
import re
import subprocess
from pathlib import Path

from jsonschema import Draft202012Validator

def fail(x):
    print("FAIL|" + x)
    raise SystemExit(1)

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

here = Path(__file__).resolve().parent

V2_SHA = "c6ebb5ef2214c4168283f9009d1f7ce6e88d2ff928853fe6a57ed1f7521c6956"
V1_SHA = "7eb17eeb8f49b37420d0d1d71539cf0d7cb08241ecf133e7b4139fd130718b34"
REVIEW_SHA = "19e94cf48cbe9b5df537feb2abb350a80bfcef752e4da4d8bed3282077d67c98"
RECORD_SHA = "043798215fe75ceaf61650118254b1cc3d6d046c1d292a487bf6698be090b2a6"
AUTH_SHA = "89f6cfa3c722bcef7caec4b847ca5811084bf015a87c780804f9c42de2bdfc89"

Z_SHA = "f4c94c1c151b893e2e4f1fae7d43b1196432cbcceaa7f9428968d45f2f77b7b1"
Z_CONTENT = "3461269e60f3b824bef3c62335d24e9eda5552b1a939bea4c720983e39a25049"

P_SHA = "b2877713a3d8c38ecf135544f4cab7a2230e39b4ed73e18a7965497b3901ef73"
P_CONTENT = "370da6351b59f6134ae09477d8941d8ab119adad7f4230540758e09326b47c4f"

checks = {
    "03_exact_unchanged_protocol_specification_schema_v2_candidate.json":
        V2_SHA,

    "04_frozen_protocol_specification_schema_v1.json":
        V1_SHA,

    "05_prior_completed_human_review.REVISION_REQUIRED.v1.md":
        REVIEW_SHA,

    "06_prior_completed_human_review_record.v1.json":
        RECORD_SHA,

    "09_corrective_review_package_v2_authorization.v1.json":
        AUTH_SHA,

    "10_exact_frozen_zlib_canonical_specification.json":
        Z_SHA,

    "11_exact_frozen_libpcap_canonical_specification.json":
        P_SHA,
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
    fail("V2_SIZE")

v2 = json.loads(
    (
        here /
        "03_exact_unchanged_protocol_specification_schema_v2_candidate.json"
    ).read_text(encoding="utf-8")
)

Draft202012Validator.check_schema(v2)

z = json.loads(
    (
        here /
        "10_exact_frozen_zlib_canonical_specification.json"
    ).read_text(encoding="utf-8")
)

p = json.loads(
    (
        here /
        "11_exact_frozen_libpcap_canonical_specification.json"
    ).read_text(encoding="utf-8")
)

if z.get("content_sha256") != Z_CONTENT:
    fail("ZLIB_CONTENT_SHA")

if p.get("content_sha256") != P_CONTENT:
    fail("LIBPCAP_CONTENT_SHA")

if z.get("schema_version") != "1.0.0":
    fail("ZLIB_SCHEMA_VERSION")

if p.get("schema_version") != "1.0.0":
    fail("LIBPCAP_SCHEMA_VERSION")

comparison = json.loads(
    (
        here /
        "12_zlib_libpcap_prepost_comparison_manifest.v1.json"
    ).read_text(encoding="utf-8")
)

if comparison["zlib"]["expected_file_sha256"] != Z_SHA:
    fail("COMPARISON_ZLIB_SHA")

if comparison["libpcap"]["expected_file_sha256"] != P_SHA:
    fail("COMPARISON_LIBPCAP_SHA")

claims = comparison["claims"]

for key in (
    "zlib_byte_identity_from_own_freeze_through_corrective_authorization",
    "zlib_git_blob_identity_from_own_freeze_through_corrective_authorization",
    "libpcap_byte_identity_from_own_freeze_through_corrective_authorization",
    "libpcap_git_blob_identity_from_own_freeze_through_corrective_authorization",
    "later_governance_parent_checkpoint_pairs_preserve_both_artifacts",
):
    if claims[key] is not True:
        fail("COMPARISON_CLAIM|" + key)

if claims["schema_v2_candidate_modified"] is not False:
    fail("SCHEMA_V2_MODIFIED")

subprocess.check_call(
    [
        "python3",
        str(
            here /
            "13_zlib_libpcap_prepost_git_proof/"
            "99_verify_portable_zlib_libpcap_git_proof.v1.py"
        )
    ]
)

pred = here / "12_predecessor_review_package_v1"

subprocess.check_call(
    [
        "python3",
        str(pred / "20_verify_review_package.v1.py")
    ],
    stdout=subprocess.DEVNULL,
)

with (pred / "21_review_package.v1.SHA256SUMS").open("rb"):
    pass

packet = (
    (here / "02_corrective_reviewer_packet.BLANK.v2.md")
    .read_text(encoding="utf-8")
    .replace("\r\n", "\n")
    .replace("\r", "\n")
)

for rr in (
    "SV2-RR02-CORRECTIVE",
    "SV2-RR09-CORRECTIVE",
):
    h = re.search(
        rf"^###\s+{re.escape(rr)}\b[^\n]*$",
        packet,
        re.M
    )

    if not h:
        fail("REVIEW_HEADING|" + rr)

    tail = packet[h.end():]

    nxt = re.search(
        r"^###\s+SV2-RR\d{2}-CORRECTIVE\b[^\n]*$|"
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
        fail("REVIEW_DECISION_NOT_BLANK|" + rr)

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
        fail("REVIEWER_IDENTITY_NOT_BLANK|" + label)

binding = json.loads(
    (here / "01_corrective_package_binding.v1.json")
    .read_text(encoding="utf-8")
)

if binding["schema_v2_candidate"]["modified_for_corrective_package"] is not False:
    fail("BINDING_V2_MODIFIED")

if binding["schema_v2_activated"] is not False:
    fail("BINDING_ACTIVATED")

if binding["positive_v4_to_v2_mapping_defined"] is not False:
    fail("BINDING_POSITIVE_MAPPING")

if binding["curl_json_created"] is not False:
    fail("BINDING_CURL_JSON")

if binding["synthetic_human_decision"] is not False:
    fail("BINDING_SYNTHETIC_DECISION")

manifest = json.loads(
    (here / "14_corrective_review_package_manifest.v2.json")
    .read_text(encoding="utf-8")
)

if manifest["review_target"]["schema_v2_sha256"] != V2_SHA:
    fail("MANIFEST_V2_SHA")

if manifest["review_target"][
    "schema_v2_changed_from_review_package_v1"
] is not False:
    fail("MANIFEST_V2_CHANGED")

if manifest["human_decisions_initially_blank"] is not True:
    fail("MANIFEST_HUMAN_BLANK")

if manifest["synthetic_human_decision"] is not False:
    fail("MANIFEST_SYNTHETIC")

for item in manifest["files"]:
    fp = here / item["path"]

    if sha(fp) != item["sha256"]:
        fail("MANIFEST_FILE_SHA|" + item["path"])

    if fp.stat().st_size != item["size_bytes"]:
        fail("MANIFEST_FILE_SIZE|" + item["path"])

print("EXACT_UNCHANGED_SCHEMA_V2_CANDIDATE=PASS")
print("EXACT_FROZEN_ZLIB_CANONICAL_BYTES=PASS")
print("EXACT_FROZEN_LIBPCAP_CANONICAL_BYTES=PASS")
print("ZLIB_CONTENT_HASH_BINDING=PASS")
print("LIBPCAP_CONTENT_HASH_BINDING=PASS")
print("PREDECESSOR_REVIEW_PACKAGE_V1_BINDING=PASS")
print("PRIOR_REVISION_REQUIRED_REVIEW_BINDING=PASS")
print("RR02_CORRECTIVE_EVIDENCE_PRESENT=PASS")
print("RR09_CORRECTIVE_EVIDENCE_PRESENT=PASS")
print("CORRECTIVE_REVIEW_DECISIONS_INITIAL_STATE=BLANK")
print("CORRECTIVE_OVERALL_DECISION_INITIAL_STATE=BLANK")
print("CORRECTIVE_REVIEWER_IDENTITY_INITIAL_STATE=BLANK")
print("SYNTHETIC_HUMAN_DECISION=NO")
print("SCHEMA_V2_ACTIVATED=NO")
print("POSITIVE_V4_TO_V2_MAPPING_DEFINED=NO")
print("CURL_JSON_CREATED=NO")
print("SELF_CONTAINED_CORRECTIVE_REVIEW_PACKAGE_V2_VERIFICATION=PASS")
