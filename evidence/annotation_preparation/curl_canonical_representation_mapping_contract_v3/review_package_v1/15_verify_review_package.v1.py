#!/usr/bin/env python3
import hashlib, json, re
from pathlib import Path

here = Path(__file__).resolve().parent

def die(x):
    print("FAIL|" + x)
    raise SystemExit(1)

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

V3_SHA = "ef401d5d04656f67ce4148c5cc6848368a9d68449f1296c64189d1422eebdb97"
V2_SHA = "f2badbc07895e8baff078a0ce617ceb6ff02d39c7634a9e38b3b8a46a18d811c"
V4_SHA = "e17ae2ea5a70bdd790c946eb4b89ca37368d749cd7463159e69514d88a50cea8"
SCHEMA_SHA = "7eb17eeb8f49b37420d0d1d71539cf0d7cb08241ecf133e7b4139fd130718b34"

if sha(here / "03_exact_v3_mapping_contract.v3.json") != V3_SHA:
    die("V3_SHA")

if (here / "03_exact_v3_mapping_contract.v3.json").stat().st_size != 24750:
    die("V3_SIZE")

if sha(here / "10_exact_v2_mapping_contract.v2.json") != V2_SHA:
    die("V2_SHA")

if sha(here / "06_exact_approved_curl_v4.json") != V4_SHA:
    die("V4_SHA")

if sha(here / "07_frozen_canonical_schema.json") != SCHEMA_SHA:
    die("SCHEMA_SHA")

v3 = json.loads(
    (here / "03_exact_v3_mapping_contract.v3.json").read_text(encoding="utf-8")
)

if v3["contract_version"] != "V3":
    die("VERSION")

if v3["positive_mapping_algorithm_approved"] is not False:
    die("POSITIVE_MAPPING")

if v3["canonical_schema_successor_authorized"] is not False:
    die("SCHEMA_SUCCESSOR")

if v3["curl_json_created"] is not False:
    die("CURL_JSON")

loss = v3["formal_insufficiency_argument"]["required_losslessness_contract"]

for key in (
    "ownership_sensitive_semantics_preserved",
    "return_sensitive_semantics_preserved",
    "complete_exact_v4_representation_policy_preserved",
    "complete_exact_v4_representation_policy_machine_checkably_bound",
):
    if loss.get(key) is not True:
        die("CORRECTIVE_BOUNDARY|" + key)

manifest = json.loads(
    (here / "14_review_package_manifest.v1.json").read_text(encoding="utf-8")
)

for x in manifest["package_members"]:
    p = here / x["path"]
    if not p.is_file():
        die("MEMBER_MISSING|" + x["path"])
    if sha(p) != x["sha256"]:
        die("MEMBER_SHA|" + x["path"])
    if p.stat().st_size != x["size_bytes"]:
        die("MEMBER_SIZE|" + x["path"])

review = (
    here / "02_v3_corrected_schema_insufficiency_reviewer_packet.BLANK.v1.md"
).read_text(encoding="utf-8")

for i in range(1, 11):
    rr = f"V3-RR{i:02d}"
    m = re.search(
        rf"^###\s+{re.escape(rr)}\b.*?^Decision:[ \t]*(.*)$",
        review,
        re.M | re.S
    )
    if not m:
        die("REVIEW_ITEM|" + rr)
    if m.group(1).splitlines()[0].strip():
        die("DECISION_NOT_BLANK|" + rr)

for label in (
    "Overall decision:",
    "Human reviewer name:",
    "Human reviewer signature / recorded confirmation:",
    "Human reviewer date:",
):
    vals = re.findall(
        "^" + re.escape(label) + r"[ \t]*(.*)$",
        review,
        re.M
    )
    if len(vals) != 1 or vals[0].strip():
        die("BLANK_FIELD|" + label)

print("EXACT_V3_REVIEW_TARGET_SHA256=PASS")
print("EXACT_V3_REVIEW_TARGET_SIZE=PASS")
print("V3_RR08_CORRECTION_BOUNDARY=PASS")
print("PORTABLE_GIT_OBJECT_EVIDENCE_INCLUDED=YES")
print("V3_RR01_TO_V3_RR10_DECISIONS=BLANK")
print("OVERALL_TECHNICAL_REVIEW_DECISION=BLANK")
print("SYNTHETIC_HUMAN_APPROVAL_PRESENT=NO")
print("CANONICAL_SCHEMA_SUCCESSOR_AUTHORIZED=NO")
print("CURL_JSON_CREATED=NO")
print("V3_INDEPENDENT_REVIEW_PACKAGE_VERIFICATION=PASS")
