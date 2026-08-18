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

V2_SHA = (
    "63c17bbd0a09365fad9d3f0445fdc2115a8a0e945f622a39c745f31e1baf3d31"
)

V1_REVIEW_SHA = (
    "e253340d540a06cd24af501c569154869ac0324d677995b7266349ba097973cc"
)

V3_SHA = (
    "ede7e1422b9553f73377432474deb282852b619a5b004cd7c4d00033c0a37abb"
)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


v2 = here / "03_curl_technical_protocol_working_draft.v2.json"
packet = here / "02_curl_technical_v2_reviewer_packet.v1.md"
review = here / "08_completed_v1_human_technical_review.md"
v3 = here / "09_frozen_curl_v3_authoring_scope.v3.json"
source_root = here / "12_source_evidence"
manifest_path = here / "14_review_package_manifest.v1.json"

if sha(v2) != V2_SHA:
    fail("EXACT_V2_SHA256")

if sha(review) != V1_REVIEW_SHA:
    fail("V1_COMPLETED_REVIEW_SHA256")

if sha(v3) != V3_SHA:
    fail("FROZEN_V3_SHA256")

data = json.loads(v2.read_text(encoding="utf-8"))

expected_api = {
    "curl_global_init",
    "curl_global_cleanup",
    "curl_easy_init",
    "curl_easy_setopt",
    "curl_easy_perform",
    "curl_easy_reset",
    "curl_easy_cleanup",
    "curl_multi_init",
    "curl_multi_add_handle",
    "curl_multi_perform",
    "curl_multi_remove_handle",
    "curl_multi_cleanup",
}

if len(data["api_surface"]) != 12:
    fail("V2_API_SURFACE_COUNT")

if set(data["api_surface"]) != expected_api:
    fail("V2_API_SURFACE_SET")

manifest = json.loads(
    manifest_path.read_text(encoding="utf-8")
)

if manifest["review_target"]["working_draft_sha256"] != V2_SHA:
    fail("PACKAGE_MANIFEST_V2_SHA")

if manifest["approved_source_evidence_file_count"] != 21:
    fail("SOURCE_MANIFEST_COUNT")

source_files = [
    p for p in source_root.rglob("*")
    if p.is_file()
]

if len(source_files) != 21:
    fail(
        "SOURCE_EVIDENCE_FILE_COUNT|"
        + str(len(source_files))
    )

expected_sources = {
    item["path"]: item["sha256"]
    for item in manifest["approved_source_evidence"]
}

observed_sources = {}

for p in source_files:
    rel = p.relative_to(source_root).as_posix()
    observed_sources[rel] = sha(p)

if observed_sources != expected_sources:
    fail("APPROVED_SOURCE_EVIDENCE_HASH_SET")

text = (
    packet.read_text(encoding="utf-8")
    .replace("\\_", "_")
)

for rr in [f"V2-RR{i:02d}" for i in range(1, 13)]:
    heading = re.search(
        rf"^### {re.escape(rr)}\b[^\n]*$",
        text,
        re.M,
    )

    if not heading:
        fail("REVIEW_ITEM_MISSING|" + rr)

    tail = text[heading.end():]

    nxt = re.search(
        r"^### V2-RR\d{2}\b[^\n]*$|"
        r"^## Overall technical review decision\b",
        tail,
        re.M,
    )

    section = (
        tail[:nxt.start()]
        if nxt
        else tail
    )

    decisions = re.findall(
        r"^Decision:[ \t]*(.*)$",
        section,
        re.M,
    )

    if len(decisions) != 1:
        fail(
            "REVIEW_DECISION_LINE_COUNT|"
            + rr + "|" + str(len(decisions))
        )

    if decisions[0].strip():
        fail("REVIEW_DECISION_NOT_BLANK|" + rr)

overall = re.findall(
    r"^Overall decision:[ \t]*(.*)$",
    text,
    re.M,
)

if len(overall) != 1:
    fail(
        "OVERALL_DECISION_LINE_COUNT|"
        + str(len(overall))
    )

if overall[0].strip():
    fail("OVERALL_DECISION_NOT_BLANK")

role = re.findall(
    r"^Reviewer role ID:[ \t]*`([^`]+)`[ \t]*$",
    text,
    re.M,
)

if role != ["Spec-Technical-Reviewer-1"]:
    fail("REVIEWER_ROLE_ID")

for label in (
    "Human reviewer name:",
    "Human reviewer signature / recorded confirmation:",
    "Human reviewer date:",
):
    vals = [
        line[len(label):].strip()
        for line in text.splitlines()
        if line.startswith(label)
    ]

    if len(vals) != 1:
        fail(
            "REVIEWER_FIELD_COUNT|"
            + label + "|" + str(len(vals))
        )

    if vals[0]:
        fail("REVIEWER_FIELD_NOT_BLANK|" + label)

witness_verify = (
    here
    / "13_author_checkpoint_git_witness_v2"
    / "03_verify_author_checkpoint_git_witness.v2.py"
)

cp = subprocess.run(
    [sys.executable, str(witness_verify)],
    cwd=str(witness_verify.parent),
)

if cp.returncode != 0:
    fail("AUTHOR_CHECKPOINT_GIT_WITNESS")

bad_terms = (
    "generated_driver",
    "gold_label",
    "analyzer_output",
    "baseline_output",
    "repair_output",
    "raw_model_response",
)

for p in here.rglob("*"):
    if not p.is_file():
        continue

    lower = p.name.lower()

    if any(term in lower for term in bad_terms):
        fail(
            "PROHIBITED_EVIDENCE_FILENAME|"
            + p.relative_to(here).as_posix()
        )

print("EXACT_WORKING_DRAFT_V2_BINDING=PASS")
print("EXACT_TWELVE_FUNCTION_API_SURFACE=PASS")
print("V1_COMPLETED_HUMAN_REVIEW_BINDING=PASS")
print("EXACT_FROZEN_V3_BINDING=PASS")
print("APPROVED_SOURCE_EVIDENCE=21_OF_21_PASS")
print("AUTHOR_CHECKPOINT_MINIMAL_GIT_WITNESS=PASS")
print("V2_RR01_TO_V2_RR12_DECISIONS=BLANK")
print("OVERALL_TECHNICAL_REVIEW_DECISION=BLANK")
print("HUMAN_REVIEWER_IDENTITY_FIELDS=BLANK")
print("CANONICAL_CURL_SPECIFICATION_AUTHORIZED=NO")
print("GENERATED_DRIVER_INSPECTION_AUTHORIZED=NO")
print("SELECTED_SAMPLE_MEMBERSHIP_INSPECTION_AUTHORIZED=NO")
print("GOLD_ANNOTATION_AUTHORIZED=NO")
print("ANALYZER_IMPLEMENTATION_AUTHORIZED=NO")
print("BASELINE_EXECUTION_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
print("CURL_TECHNICAL_WORKING_DRAFT_V2_REVIEW_PACKAGE_VERIFICATION=PASS")
