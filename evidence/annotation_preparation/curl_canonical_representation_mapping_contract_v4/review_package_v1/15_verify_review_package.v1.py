#!/usr/bin/env python3

import copy
import hashlib
import json
import re
from pathlib import Path

here = Path(__file__).resolve().parent

def die(x):
    print("FAIL|" + x)
    raise SystemExit(1)

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

V4_SHA = "9a44120de8947369864b75fb04680b504b91ccfa478eeaeaea20162a6d97e070"
V3_SHA = "ef401d5d04656f67ce4148c5cc6848368a9d68449f1296c64189d1422eebdb97"
TECH_V4_SHA = "e17ae2ea5a70bdd790c946eb4b89ca37368d749cd7463159e69514d88a50cea8"
SCHEMA_SHA = "7eb17eeb8f49b37420d0d1d71539cf0d7cb08241ecf133e7b4139fd130718b34"

v4p = here / "03_exact_v4_mapping_contract.v4.json"
v3p = here / "10_exact_v3_mapping_contract.v3.json"

if sha(v4p) != V4_SHA:
    die("V4_SHA")

if v4p.stat().st_size != 26601:
    die("V4_SIZE")

if sha(v3p) != V3_SHA:
    die("V3_SHA")

if sha(here / "06_exact_approved_curl_technical_v4.json") != TECH_V4_SHA:
    die("TECH_V4_SHA")

if sha(here / "07_frozen_canonical_schema.json") != SCHEMA_SHA:
    die("SCHEMA_SHA")

v4 = json.loads(v4p.read_text(encoding="utf-8"))
v3 = json.loads(v3p.read_text(encoding="utf-8"))

if v4["contract_version"] != "V4":
    die("VERSION")

if v4["independent_review_requirement"]["review_target"] != \
   "Exact immutable V4 corrective schema-insufficiency proof.":
    die("SELF_REVIEW_TARGET")

if v4["positive_mapping_algorithm_approved"] is not False:
    die("POSITIVE_MAPPING")

if v4["canonical_schema_successor_authorized"] is not False:
    die("SCHEMA_SUCCESSOR")

if v4["curl_json_created"] is not False:
    die("CURL_JSON")

allowed = {
    "schema_id",
    "contract_version",
    "contract_kind",
    "status",
    "purpose",
    "input_bindings",
    "corrective_successor_from_v3_review",
    "independent_review_requirement",
    "immutability_policy",
    "next_boundary",
}

a = copy.deepcopy(v3)
b = copy.deepcopy(v4)

for key in allowed:
    a.pop(key, None)
    b.pop(key, None)

if a != b:
    die("SUBSTANTIVE_V3_CHANGE")

r3 = copy.deepcopy(v3["independent_review_requirement"])
r4 = copy.deepcopy(v4["independent_review_requirement"])

r3.pop("review_target")
r4.pop("review_target")

if r3 != r4:
    die("REVIEW_REQUIREMENT_NON_TARGET_CHANGE")

manifest = json.loads(
    (here / "14_review_package_manifest.v1.json")
    .read_text(encoding="utf-8")
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
    here /
    "02_v4_rr10_corrected_schema_insufficiency_reviewer_packet.BLANK.v1.md"
).read_text(encoding="utf-8")

for i in range(1, 11):
    rr = f"V4-RR{i:02d}"

    head = re.search(
        rf"^###\s+{re.escape(rr)}\b[^\n]*$",
        review,
        re.M
    )

    if not head:
        die("REVIEW_ITEM|" + rr)

    tail = review[head.end():]

    nxt = re.search(
        r"^###\s+V4-RR\d{2}\b[^\n]*$|"
        r"^##\s+Overall technical review decision\b",
        tail,
        re.M
    )

    section = tail[:nxt.start()] if nxt else tail

    vals = re.findall(
        r"^Decision:[ \t]*(.*)$",
        section,
        re.M
    )

    if len(vals) != 1 or vals[0].strip():
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

print("EXACT_V4_REVIEW_TARGET_SHA256=PASS")
print("EXACT_V4_REVIEW_TARGET_SIZE=PASS")
print("V4_EXACT_SELF_REVIEW_TARGET=PASS")
print("V3_RR10_CORRECTION=PASS")
print("V3_SUBSTANTIVE_PROOF_PRESERVATION=PASS")
print("PORTABLE_GIT_OBJECT_EVIDENCE_INCLUDED=YES")
print("V4_RR01_TO_V4_RR10_DECISIONS=BLANK")
print("OVERALL_TECHNICAL_REVIEW_DECISION=BLANK")
print("HUMAN_REVIEWER_IDENTITY_FIELDS=BLANK")
print("SYNTHETIC_HUMAN_APPROVAL_PRESENT=NO")
print("CANONICAL_SCHEMA_SUCCESSOR_AUTHORIZED=NO")
print("CURL_JSON_CREATED=NO")
print("V4_INDEPENDENT_REVIEW_PACKAGE_VERIFICATION=PASS")
