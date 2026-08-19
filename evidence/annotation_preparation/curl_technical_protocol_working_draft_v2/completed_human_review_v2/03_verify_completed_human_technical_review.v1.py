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


V2_SHA = (
    "63c17bbd0a09365fad9d3f0445fdc2115a8a0e945f622a39c745f31e1baf3d31"
)

REVIEW_SHA = (
    "597699068c3ba7bf480204c67d88d940f400c7425442a081a18198908b1e029e"
)

REVIEW_SIZE = 37832

review = here / "01_completed_human_technical_review.v2.md"
record_path = here / "02_completed_human_technical_review_record.v1.json"

v2 = (
    repo
    / "config/annotation/"
      "curl_technical_protocol_working_draft.v2.json"
)

decision = (
    repo
    / "documentation/decisions/"
      "0031-curl-technical-working-draft-v2-human-review-revision-required.md"
)

pkg = (
    repo
    / "evidence/annotation_preparation/"
      "curl_technical_protocol_working_draft_v2/"
      "review_package_v2"
)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


if sha(v2) != V2_SHA:
    fail("V2_IMMUTABILITY_SHA256")

if sha(review) != REVIEW_SHA:
    fail("COMPLETED_HUMAN_REVIEW_SHA256")

if review.stat().st_size != REVIEW_SIZE:
    fail("COMPLETED_HUMAN_REVIEW_SIZE")

if len([p for p in pkg.rglob("*") if p.is_file()]) != 40:
    fail("IMMUTABLE_REVIEW_PACKAGE_FILE_COUNT")

pkg_verify = pkg / "15_verify_review_package.v1.py"

cp = subprocess.run(
    [sys.executable, str(pkg_verify)],
    cwd=str(pkg),
)

if cp.returncode != 0:
    fail("IMMUTABLE_REVIEW_PACKAGE_INTERNAL_VERIFY")


raw = review.read_text(encoding="utf-8")
text = raw.replace("\\_", "_")

expected = {
    "V2-RR01": "PASS",
    "V2-RR02": "PASS",
    "V2-RR03": "PASS",
    "V2-RR04": "PASS",
    "V2-RR05": "REVISION_REQUIRED",
    "V2-RR06": "REVISION_REQUIRED",
    "V2-RR07": "PASS",
    "V2-RR08": "PASS",
    "V2-RR09": "REVISION_REQUIRED",
    "V2-RR10": "REVISION_REQUIRED",
    "V2-RR11": "PASS",
    "V2-RR12": "REVISION_REQUIRED",
}

if V2_SHA not in text:
    fail("HUMAN_REVIEW_V2_SHA_BINDING")

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
        r"^###\s+V2-RR\d{2}\b[^\n]*$|"
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

    observed[rr] = ds[0]

    if ds[0] != wanted:
        fail(
            "REVIEW_DECISION_MISMATCH|"
            + rr + "|EXPECTED=" + wanted
            + "|OBSERVED=" + ds[0]
        )


overall = re.findall(
    r"^Overall decision:[ \t]*"
    r"(APPROVE_EXACT_WORKING_DRAFT_V2_FOR_CANONICALIZATION|"
    r"REVISION_REQUIRED|FAIL)[ \t]*$",
    text,
    re.M,
)

if overall != ["REVISION_REQUIRED"]:
    fail("OVERALL_REVIEW_DECISION|" + repr(overall))


identity_checks = {
    "Reviewer role ID":
        "Spec-Technical-Reviewer-1",

    "Human reviewer name":
        "Abdul Raheem Shahzad",

    "Human reviewer signature / recorded confirmation":
        "ARS",

    "Human reviewer date":
        "19 / August / 2026",
}

for label, expected_value in identity_checks.items():

    if label == "Reviewer role ID":
        pattern = (
            r"^Reviewer role ID:[ \t]*`?"
            r"([^`\n]+?)"
            r"`?[ \t]*$"
        )
    else:
        pattern = (
            r"^"
            + re.escape(label)
            + r":[ \t]*(.+?)[ \t]*$"
        )

    vals = re.findall(
        pattern,
        text,
        re.M,
    )

    if len(vals) != 1:
        fail(
            "IDENTITY_FIELD_COUNT|"
            + label + "|" + str(len(vals))
        )

    if vals[0].strip() != expected_value:
        fail(
            "IDENTITY_FIELD_VALUE|"
            + label
            + "|EXPECTED="
            + expected_value
            + "|OBSERVED="
            + vals[0].strip()
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

if len(pass_items) != 7:
    fail("PASS_COUNT|" + str(len(pass_items)))

if len(revision_items) != 5:
    fail("REVISION_REQUIRED_COUNT|" + str(len(revision_items)))

if fail_items:
    fail("FAIL_ITEMS|" + ",".join(fail_items))


required_review_markers = [
    "Create a new immutable successor and do not edit V2 in place.",
    "successor-bound traceability record",
    "Working Draft V2 must remain immutable.",
    "This decision does not create or authorize canonical `curl.json`.",
    "No assistant-generated or synthetic human approval is permitted.",
]

for marker in required_review_markers:
    if marker not in text:
        fail("REQUIRED_REVIEW_MARKER|" + marker)


record = json.loads(
    record_path.read_text(encoding="utf-8")
)

if (
    record["review_target"]["working_draft_sha256"]
    != V2_SHA
):
    fail("RECORD_V2_SHA")

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
    "PASS": 7,
    "REVISION_REQUIRED": 5,
    "FAIL": 0,
}:
    fail("RECORD_DECISION_COUNTS")

if len(record["required_successor_corrections"]) != 8:
    fail("SUCCESSOR_CORRECTION_COUNT")


governance = record["governance"]

required_false = (
    "canonical_curl_specification_authorized",
    "generated_driver_inspection_authorized",
    "selected_sample_membership_inspection_authorized",
    "gold_annotation_authorized",
    "analyzer_implementation_authorized",
    "baseline_execution_authorized",
    "repair_authorized",
)

for key in required_false:
    if governance.get(key) is not False:
        fail("UNAUTHORIZED_BOUNDARY_CHANGED|" + key)

if governance.get("working_draft_v2_must_remain_immutable") is not True:
    fail("V2_IMMUTABILITY_GOVERNANCE")

if governance.get("new_immutable_successor_required") is not True:
    fail("SUCCESSOR_REQUIRED_GOVERNANCE")

if record.get("next_boundary") != (
    "AUTHORIZE_CURL_TECHNICAL_WORKING_DRAFT_V3_SUCCESSOR"
):
    fail("NEXT_BOUNDARY")


if not decision.is_file():
    fail("DECISION_0031_MISSING")

dtext = decision.read_text(encoding="utf-8")

for marker in (
    V2_SHA,
    REVIEW_SHA,
    "REVISION_REQUIRED",
    "Abdul Raheem Shahzad",
    "7 PASS / 5 REVISION_REQUIRED / 0 FAIL",
    "AUTHORIZE_CURL_TECHNICAL_WORKING_DRAFT_V3_SUCCESSOR",
):
    if marker not in dtext:
        fail("DECISION_0031_BINDING|" + marker)


print("WORKING_DRAFT_V2_IMMUTABILITY_SHA256=PASS")
print("COMPLETED_HUMAN_REVIEW_SHA256=PASS")
print("COMPLETED_HUMAN_REVIEW_SIZE=PASS")
print("IMMUTABLE_V2_REVIEW_PACKAGE=PASS")
print("V2_RR01_TO_V2_RR12_COMPLETED_DECISIONS=PASS")
print("REVIEW_DECISION_DISTRIBUTION=7_PASS_5_REVISION_REQUIRED_0_FAIL")
print("OVERALL_TECHNICAL_REVIEW_DECISION=REVISION_REQUIRED")
print("REVIEWER_IDENTITY=PASS")
print("SUCCESSOR_CORRECTIONS_RECORDED=8")
print("WORKING_DRAFT_V2_MUST_REMAIN_IMMUTABLE=YES")
print("NEW_IMMUTABLE_SUCCESSOR_REQUIRED=YES")
print("CANONICAL_CURL_SPECIFICATION_AUTHORIZED=NO")
print("GENERATED_DRIVER_INSPECTION_AUTHORIZED=NO")
print("SELECTED_SAMPLE_MEMBERSHIP_INSPECTION_AUTHORIZED=NO")
print("GOLD_ANNOTATION_AUTHORIZED=NO")
print("ANALYZER_IMPLEMENTATION_AUTHORIZED=NO")
print("BASELINE_EXECUTION_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
print("COMPLETED_CURL_TECHNICAL_V2_HUMAN_REVIEW_VERIFICATION=PASS")
