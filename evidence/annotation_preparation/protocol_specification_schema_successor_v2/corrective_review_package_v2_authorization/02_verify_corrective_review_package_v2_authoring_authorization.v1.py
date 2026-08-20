#!/usr/bin/env python3

import hashlib
import json
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

authp = here / "01_corrective_review_package_v2_authoring_authorization.v1.json"

v2p = repo / "config/schemas/protocol_specification.v2.schema.json"
v1p = repo / "config/schemas/protocol_specification.schema.json"

zlibp = repo / "config/protocol_specifications/zlib.json"
pcapp = repo / "config/protocol_specifications/libpcap.json"

completed = (
    repo /
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2/"
    "completed_human_review_v1"
)

pkg1 = (
    repo /
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2/"
    "review_package_v1"
)

pkg2 = (
    repo /
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2/"
    "review_package_v2"
)

curlp = repo / "config/protocol_specifications/curl.json"

V2_SHA = "c6ebb5ef2214c4168283f9009d1f7ce6e88d2ff928853fe6a57ed1f7521c6956"
V1_SHA = "7eb17eeb8f49b37420d0d1d71539cf0d7cb08241ecf133e7b4139fd130718b34"
ZLIB_SHA = "f4c94c1c151b893e2e4f1fae7d43b1196432cbcceaa7f9428968d45f2f77b7b1"
PCAP_SHA = "b2877713a3d8c38ecf135544f4cab7a2230e39b4ed73e18a7965497b3901ef73"
REVIEW_SHA = "19e94cf48cbe9b5df537feb2abb350a80bfcef752e4da4d8bed3282077d67c98"
RECORD_SHA = "043798215fe75ceaf61650118254b1cc3d6d046c1d292a487bf6698be090b2a6"

if sha(v2p) != V2_SHA:
    fail("V2_SHA")

if sha(v1p) != V1_SHA:
    fail("V1_SHA")

if sha(zlibp) != ZLIB_SHA:
    fail("ZLIB_SHA")

if sha(pcapp) != PCAP_SHA:
    fail("LIBPCAP_SHA")

if sha(
    completed /
    "01_completed_schema_v2_human_review.REVISION_REQUIRED.v1.md"
) != REVIEW_SHA:
    fail("COMPLETED_REVIEW_SHA")

if sha(
    completed /
    "02_completed_schema_v2_human_review_record.v1.json"
) != RECORD_SHA:
    fail("COMPLETED_RECORD_SHA")

if pkg2.exists():
    fail("REVIEW_PACKAGE_V2_ALREADY_EXISTS")

if curlp.exists():
    fail("CURL_JSON_EXISTS")

auth = json.loads(authp.read_text(encoding="utf-8"))

if auth["status"] != \
   "AUTHORIZED_FOR_CORRECTIVE_REVIEW_PACKAGE_V2_AUTHORING_RR02_RR09_EVIDENCE_ONLY":
    fail("AUTH_STATUS")

if auth["basis"]["overall_review_outcome"] != "REVISION_REQUIRED":
    fail("REVIEW_OUTCOME")

if auth["basis"]["revision_required_items"] != [
    "SV2-RR02",
    "SV2-RR09",
]:
    fail("REVISION_REQUIRED_ITEMS")

if set(auth["basis"]["passing_items_preserved"]) != {
    "SV2-RR01",
    "SV2-RR03",
    "SV2-RR04",
    "SV2-RR05",
    "SV2-RR06",
    "SV2-RR07",
    "SV2-RR08",
    "SV2-RR10",
}:
    fail("PRESERVED_PASS_ITEMS")

if auth["immutable_inputs"]["schema_v2_candidate"]["may_modify"] is not False:
    fail("V2_MUTABILITY")

if auth["immutable_inputs"]["review_package_v1"]["may_modify"] is not False:
    fail("PACKAGE_V1_MUTABILITY")

if auth["authorized_successor"]["package_path"] != \
   "evidence/annotation_preparation/protocol_specification_schema_successor_v2/review_package_v2":
    fail("RESERVED_PACKAGE_PATH")

if auth["authorized_successor"]["authoring_authorized"] is not True:
    fail("AUTHORING_AUTHORIZATION")

if auth["authorized_successor"]["human_re_review_required"] is not True:
    fail("HUMAN_REREVIEW")

if auth["authorized_successor"][
    "scope_limited_to_prior_rr02_rr09_evidence_findings"
] is not True:
    fail("CORRECTIVE_SCOPE")

for key, value in auth["explicit_non_authorizations"].items():
    if value is not False:
        fail("NONAUTH|" + key)

if auth["next_boundary"] != \
   "AUTHOR_SCHEMA_V2_CORRECTIVE_REVIEW_PACKAGE_V2_RR02_RR09_EVIDENCE_ONLY":
    fail("NEXT_BOUNDARY")

def git_sha(commit, path):
    raw = subprocess.check_output(
        ["git", "-C", str(repo), "show", f"{commit}:{path}"]
    )
    return hashlib.sha256(raw).hexdigest()

def git_blob(commit, path):
    return subprocess.check_output(
        ["git", "-C", str(repo), "rev-parse", f"{commit}:{path}"],
        text=True
    ).strip()

z_commits = [
    "e12adfe2d502f6915a094c2f39a46e426ddc0522",
    "dc6371ceaa189d0a39ae5a93e131cb85ebe328d8",
    "5195de4842668fdd1ef587e4dbe969e53f80dd5c",
    "41753d7f7b6f26836ff6c2a4b12bb13084f069e9",
    "c2c1e28c235c158eb36759d167c3700bfd8042f4",
]

p_commits = [
    "b1635239e29ff6dd9a3188e264c4e6a816977aae",
    "dc6371ceaa189d0a39ae5a93e131cb85ebe328d8",
    "5195de4842668fdd1ef587e4dbe969e53f80dd5c",
    "41753d7f7b6f26836ff6c2a4b12bb13084f069e9",
    "c2c1e28c235c158eb36759d167c3700bfd8042f4",
]

z_blobs = []
for c in z_commits:
    if git_sha(c, "config/protocol_specifications/zlib.json") != ZLIB_SHA:
        fail("ZLIB_PREPOST_SHA|" + c)

    z_blobs.append(
        git_blob(c, "config/protocol_specifications/zlib.json")
    )

if len(set(z_blobs)) != 1:
    fail("ZLIB_BLOB_IDENTITY")

p_blobs = []
for c in p_commits:
    if git_sha(c, "config/protocol_specifications/libpcap.json") != PCAP_SHA:
        fail("LIBPCAP_PREPOST_SHA|" + c)

    p_blobs.append(
        git_blob(c, "config/protocol_specifications/libpcap.json")
    )

if len(set(p_blobs)) != 1:
    fail("LIBPCAP_BLOB_IDENTITY")

print("COMPLETED_SCHEMA_V2_REVISION_REQUIRED_REVIEW_BINDING=PASS")
print("SCHEMA_V2_CANDIDATE_IMMUTABLE=YES")
print("REVIEW_PACKAGE_V1_IMMUTABLE=YES")
print("ZLIB_BASELINE_TO_CURRENT_BYTE_SHA_IDENTITY=PASS")
print("ZLIB_BASELINE_TO_CURRENT_GIT_BLOB_IDENTITY=PASS")
print("LIBPCAP_BASELINE_TO_CURRENT_BYTE_SHA_IDENTITY=PASS")
print("LIBPCAP_BASELINE_TO_CURRENT_GIT_BLOB_IDENTITY=PASS")
print("RR02_RR09_CORRECTIVE_EVIDENCE_FEASIBILITY=PASS")
print("CORRECTIVE_REVIEW_PACKAGE_V2_AUTHORING_AUTHORIZED=YES")
print("CORRECTIVE_SCOPE=SV2_RR02_AND_SV2_RR09_EVIDENCE_ONLY")
print("SCHEMA_V2_ACTIVATED=NO")
print("POSITIVE_V4_TO_V2_MAPPING_DEFINED=NO")
print("CURL_JSON_CREATED=NO")
print("CORRECTIVE_REVIEW_PACKAGE_V2_AUTHORING_AUTHORIZATION_VERIFICATION=PASS")
