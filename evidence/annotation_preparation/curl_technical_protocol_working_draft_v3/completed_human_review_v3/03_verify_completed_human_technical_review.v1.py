#!/usr/bin/env python3

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path


def fail(msg):
    print("FAIL|" + msg)
    raise SystemExit(1)


here = Path(__file__).resolve().parent

repo = here
while repo != repo.parent and not (repo / ".git").exists():
    repo = repo.parent

if not (repo / ".git").exists():
    fail("REPOSITORY_ROOT_NOT_FOUND")


V3_SHA = (
    "2c10317a7a1fa745d64b461bb318ac2aa1e3e23439ca261c8cd746d1ea3f8ac2"
)

V3_SIZE = 41330

V2_SHA = (
    "63c17bbd0a09365fad9d3f0445fdc2115a8a0e945f622a39c745f31e1baf3d31"
)

REVIEW_SHA = (
    "9a15b13cea29bcbcbfff349c9b9bcb113a9d9a4e01afe03727d7be8dbd87c327"
)

REVIEW_SIZE = 22983

PKG_SUMS_SHA = (
    "44be6f0141ffa6132f840876db4ae256753946e37ff1bafbd575b353ea79fa08"
)

v3 = (
    repo
    / "config/annotation/"
      "curl_technical_protocol_working_draft.v3.json"
)

v2 = (
    repo
    / "config/annotation/"
      "curl_technical_protocol_working_draft.v2.json"
)

review = here / "01_completed_human_technical_review.v3.md"
record_path = here / "02_completed_human_technical_review_record.v1.json"

pkg = (
    repo
    / "evidence/annotation_preparation/"
      "curl_technical_protocol_working_draft_v3/"
      "review_package_v3"
)

decision = (
    repo
    / "documentation/decisions/"
      "0034-curl-technical-working-draft-v3-human-review-revision-required.md"
)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


if sha(v3) != V3_SHA:
    fail("V3_IMMUTABILITY_SHA256")

if v3.stat().st_size != V3_SIZE:
    fail("V3_IMMUTABILITY_SIZE")

if sha(v2) != V2_SHA:
    fail("V2_IMMUTABILITY_SHA256")

if sha(review) != REVIEW_SHA:
    fail("COMPLETED_HUMAN_REVIEW_SHA256")

if review.stat().st_size != REVIEW_SIZE:
    fail("COMPLETED_HUMAN_REVIEW_SIZE")

if sha(pkg / "19_review_package.v3.SHA256SUMS") != PKG_SUMS_SHA:
    fail("IMMUTABLE_REVIEW_PACKAGE_SUMS_SHA")


proc = subprocess.run(
    [
        sys.executable,
        str(pkg / "18_verify_review_package.v3.py"),
    ],
    cwd=str(pkg),
)

if proc.returncode != 0:
    fail("IMMUTABLE_V3_REVIEW_PACKAGE_VERIFY")


raw = review.read_text(encoding="utf-8")
text = raw.replace("\\_", "_")

expected = {
    "V3-RR01": "PASS",
    "V3-RR02": "REVISION_REQUIRED",
    "V3-RR03": "PASS",
    "V3-RR04": "PASS",
    "V3-RR05": "PASS",
    "V3-RR06": "PASS",
    "V3-RR07": "PASS",
    "V3-RR08": "PASS",
    "V3-RR09": "PASS",
    "V3-RR10": "PASS",
    "V3-RR11": "PASS",
    "V3-RR12": "REVISION_REQUIRED",
}

if V3_SHA not in text:
    fail("HUMAN_REVIEW_V3_SHA_BINDING")

observed = {}

for rr, wanted in expected.items():
    hs = list(
        re.finditer(
            rf"^###\s+{re.escape(rr)}\b[^\n]*$",
            text,
            re.M,
        )
    )

    if len(hs) != 1:
        fail(
            "REVIEW_HEADING_COUNT|"
            + rr + "|" + str(len(hs))
        )

    tail = text[hs[0].end():]

    nxt = re.search(
        r"^###\s+V3-RR\d{2}\b[^\n]*$|"
        r"^##\s+Overall technical review decision\b",
        tail,
        re.M,
    )

    section = tail[:nxt.start()] if nxt else tail

    ds = re.findall(
        r"^Decision:[ \t]*(PASS|REVISION_REQUIRED|FAIL)[ \t]*$",
        section,
        re.M,
    )

    if len(ds) != 1:
        fail(
            "REVIEW_DECISION_COUNT|"
            + rr + "|" + str(len(ds))
        )

    if ds[0] != wanted:
        fail(
            "REVIEW_DECISION_MISMATCH|"
            + rr + "|EXPECTED=" + wanted
            + "|OBSERVED=" + ds[0]
        )

    observed[rr] = ds[0]


overall = re.findall(
    r"^Overall decision:[ \t]*"
    r"(APPROVE_EXACT_WORKING_DRAFT_V3_FOR_CANONICALIZATION|"
    r"REVISION_REQUIRED|FAIL)[ \t]*$",
    text,
    re.M,
)

if overall != ["REVISION_REQUIRED"]:
    fail("OVERALL_REVIEW_DECISION|" + repr(overall))


for label, pattern, wanted in (
    (
        "ROLE",
        r"^Reviewer role ID:[ \t]*`?([^`\n]+?)`?[ \t]*$",
        "Spec-Technical-Reviewer-1",
    ),
    (
        "NAME",
        r"^Human reviewer name:[ \t]*(.+?)[ \t]*$",
        "Abdul Raheem Shahzad",
    ),
    (
        "CONFIRMATION",
        r"^Human reviewer signature / recorded confirmation:[ \t]*(.+?)[ \t]*$",
        "ARS",
    ),
    (
        "DATE",
        r"^Human reviewer date:[ \t]*(.+?)[ \t]*$",
        "19 / August / 2026",
    ),
):
    vals = re.findall(pattern, text, re.M)

    if len(vals) != 1 or vals[0].strip() != wanted:
        fail(
            "REVIEWER_IDENTITY|"
            + label + "|" + repr(vals)
        )


pass_items = [
    rr for rr, d in observed.items()
    if d == "PASS"
]

revision_items = [
    rr for rr, d in observed.items()
    if d == "REVISION_REQUIRED"
]

fail_items = [
    rr for rr, d in observed.items()
    if d == "FAIL"
]

if len(pass_items) != 10:
    fail("PASS_COUNT|" + str(len(pass_items)))

if revision_items != ["V3-RR02", "V3-RR12"]:
    fail("REVISION_SET|" + repr(revision_items))

if fail_items:
    fail("FAIL_ITEMS|" + repr(fail_items))


record = json.loads(
    record_path.read_text(encoding="utf-8")
)

if record["review_target"]["sha256"] != V3_SHA:
    fail("RECORD_V3_SHA")

if (
    record["completed_human_review"]["sha256"]
    != REVIEW_SHA
):
    fail("RECORD_REVIEW_SHA")

if (
    record["completed_human_review"]["size_bytes"]
    != REVIEW_SIZE
):
    fail("RECORD_REVIEW_SIZE")

if (
    record["completed_human_review"]["overall_decision"]
    != "REVISION_REQUIRED"
):
    fail("RECORD_OVERALL_DECISION")

if (
    record["completed_human_review"]["review_item_decisions"]
    != expected
):
    fail("RECORD_ITEM_DECISIONS")

if record["completed_human_review"]["decision_counts"] != {
    "PASS": 10,
    "REVISION_REQUIRED": 2,
    "FAIL": 0,
}:
    fail("RECORD_DECISION_COUNTS")

if len(record["required_successor_corrections"]) != 8:
    fail("SUCCESSOR_CORRECTION_COUNT")

if (
    record["must_preserve"]
    ["successor_protocol_rule_semantics_must_be_preserved"]
    if "successor_protocol_rule_semantics_must_be_preserved"
       in record["must_preserve"]
    else False
):
    pass

# The actual preservation flag is also recorded under accepted_protocol_semantics.
if (
    record["accepted_protocol_semantics"]
    ["successor_protocol_rule_semantics_must_be_preserved"]
    is not True
):
    fail("PROTOCOL_SEMANTICS_PRESERVATION")

for k, v in record["non_authorizations"].items():
    if v is not False:
        fail("NON_AUTHORIZATION_CHANGED|" + k)

if record["next_boundary"] != \
        "AUTHORIZE_CURL_TECHNICAL_WORKING_DRAFT_V4_SUCCESSOR":
    fail("NEXT_BOUNDARY")


if not decision.is_file():
    fail("DECISION_0034_MISSING")

dtext = decision.read_text(encoding="utf-8")

for marker in (
    V3_SHA,
    REVIEW_SHA,
    "10 PASS / 2 REVISION_REQUIRED / 0 FAIL",
    "V3-RR02",
    "V3-RR12",
    "platform-independent",
    "V3 must remain immutable",
    "AUTHORIZE_CURL_TECHNICAL_WORKING_DRAFT_V4_SUCCESSOR",
):
    if marker not in dtext:
        fail("DECISION_0034_BINDING|" + marker)


print("WORKING_DRAFT_V3_IMMUTABILITY_SHA256=PASS")
print("WORKING_DRAFT_V3_IMMUTABILITY_SIZE=PASS")
print("WORKING_DRAFT_V2_IMMUTABILITY_SHA256=PASS")
print("COMPLETED_V3_HUMAN_REVIEW_SHA256=PASS")
print("COMPLETED_V3_HUMAN_REVIEW_SIZE=PASS")
print("IMMUTABLE_V3_REVIEW_PACKAGE=PASS")
print("V3_RR01_TO_V3_RR12_COMPLETED_DECISIONS=PASS")
print("REVIEW_DECISION_DISTRIBUTION=10_PASS_2_REVISION_REQUIRED_0_FAIL")
print("OVERALL_TECHNICAL_REVIEW_DECISION=REVISION_REQUIRED")
print("REVIEWER_IDENTITY=PASS")
print("V3_RR02=REVISION_REQUIRED")
print("V3_RR12=REVISION_REQUIRED")
print("SUCCESSOR_CORRECTIONS_RECORDED=8")
print("ACCEPTED_PROTOCOL_RULE_SEMANTICS_MUST_BE_PRESERVED=YES")
print("V3_MUST_REMAIN_IMMUTABLE=YES")
print("NEW_IMMUTABLE_SUCCESSOR_REQUIRED=YES")
print("PLATFORM_INDEPENDENT_REVIEW_VERIFIER_REQUIRED=YES")
print("CANONICAL_CURL_SPECIFICATION_AUTHORIZED=NO")
print("GENERATED_DRIVER_INSPECTION_AUTHORIZED=NO")
print("SELECTED_SAMPLE_MEMBERSHIP_INSPECTION_AUTHORIZED=NO")
print("GOLD_ANNOTATION_AUTHORIZED=NO")
print("ANALYZER_IMPLEMENTATION_AUTHORIZED=NO")
print("ANALYZER_EXECUTION_AUTHORIZED=NO")
print("BASELINE_EXECUTION_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
print("COMPLETED_CURL_TECHNICAL_V3_HUMAN_REVIEW_VERIFICATION=PASS")
