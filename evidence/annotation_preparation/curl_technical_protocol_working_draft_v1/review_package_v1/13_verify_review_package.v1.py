#!/usr/bin/env python3

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

DRAFT = ROOT / "03_curl_technical_protocol_working_draft.v1.json"
D27 = ROOT / "04_decision_0027.AUTHOR_CHECKPOINT.md"
SOURCE_MAP = ROOT / "05_source_evidence_map.v1.json"
V3 = ROOT / "07_frozen_curl_v3_authoring_scope.v3.json"
D26 = ROOT / "08_decision_0026.WORKING_DRAFT_AUTHORIZATION.md"
SOURCE_MANIFEST = ROOT / "09_approved_source_evidence_manifest.v1.json"
SOURCE_ROOT = ROOT / "10_source_evidence"
REVIEW = ROOT / "02_curl_technical_spec_reviewer_packet.v1.md"

WIT_VERIFY = (
    ROOT /
    "11_author_checkpoint_git_witness_v1" /
    "03_verify_author_checkpoint_git_witness.v1.py"
)

DRAFT_SHA = "80498e0c4e021700e2a2c09654a852e67b16df86d61fbb28857d14a12fed44c6"
D27_SHA = "2488407a4e4a5e6f0c6881e446bf9a5f9627bf3fe0187b5417c9885739adc6e6"
V3_SHA = "ede7e1422b9553f73377432474deb282852b619a5b004cd7c4d00033c0a37abb"
D26_SHA = "6d4d9e19074834cfbbacb5125f9a11e7f13651693e70333120ad6c13525f36c1"


def fail(msg):
    print("FAIL|" + msg)
    raise SystemExit(1)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


if sha(DRAFT) != DRAFT_SHA:
    fail("DRAFT_SHA")

if sha(D27) != D27_SHA:
    fail("D27_SHA")

if sha(V3) != V3_SHA:
    fail("V3_SHA")

if sha(D26) != D26_SHA:
    fail("D26_SHA")

draft = json.loads(DRAFT.read_text(encoding="utf-8"))

if draft.get("status") != "WORKING_DRAFT_NOT_CANONICAL":
    fail("DRAFT_STATUS")

if len(draft.get("api_surface", [])) != 12:
    fail("API_SURFACE_COUNT")

if draft.get("governance", {}).get(
    "canonical_specification_authorized"
) is not False:
    fail("CANONICAL_PREAUTHORIZED")

review_items = draft.get("open_independent_review_items", [])

if {x.get("id") for x in review_items} != {
    "NR01", "NR02", "NR03", "NR04", "NR05", "NR06"
}:
    fail("NR_SET")

source_manifest = json.loads(
    SOURCE_MANIFEST.read_text(encoding="utf-8")
)

files = source_manifest.get("files", [])

if len(files) != 21:
    fail("SOURCE_FILE_COUNT")

for entry in files:
    p = SOURCE_ROOT / entry["path"]

    if not p.is_file():
        fail("SOURCE_FILE_MISSING|" + entry["path"])

    if sha(p) != entry["sha256"]:
        fail("SOURCE_SHA|" + entry["path"])

cp = subprocess.run(
    [sys.executable, str(WIT_VERIFY)],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
)

if cp.returncode != 0:
    sys.stdout.write(cp.stdout.decode(errors="replace"))
    sys.stderr.write(cp.stderr.decode(errors="replace"))
    fail("AUTHOR_GIT_WITNESS")

text = (
    REVIEW.read_text(encoding="utf-8")
    .replace("\\_", "_")
)

for rr in [f"TS-RR{i:02d}" for i in range(1, 16)]:
    heading = re.search(
        rf"^### {re.escape(rr)}\b[^\n]*$",
        text,
        re.M,
    )

    if not heading:
        fail("REVIEW_ITEM_MISSING|" + rr)

    tail = text[heading.end():]

    next_heading = re.search(
        r"^### TS-RR\d{2}\b[^\n]*$|"
        r"^## Overall technical review decision\b",
        tail,
        re.M,
    )

    section = (
        tail[:next_heading.start()]
        if next_heading
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

overall = re.search(
    r"^Overall decision:[ \t]*(.*)$",
    text,
    re.M,
)

if not overall:
    fail("OVERALL_DECISION_LINE")

if overall.group(1).strip():
    fail("OVERALL_DECISION_NOT_BLANK")

for label in (
    "Human reviewer name:",
    "Human reviewer signature / recorded confirmation:",
    "Human reviewer date:",
):
    matches = [
        line for line in text.splitlines()
        if line.startswith(label)
    ]

    if len(matches) != 1:
        fail("REVIEWER_FIELD_COUNT|" + label)

    if matches[0][len(label):].strip():
        fail("REVIEWER_FIELD_NOT_BLANK|" + label)

source_map = json.loads(
    SOURCE_MAP.read_text(encoding="utf-8")
)

if source_map.get("prohibited_evidence_used") is not False:
    fail("PROHIBITED_EVIDENCE_USED")

print("EXACT_WORKING_DRAFT_V1_BINDING=PASS")
print("EXACT_FROZEN_V3_BINDING=PASS")
print("DECISION_0026_AND_0027_BINDING=PASS")
print("APPROVED_SOURCE_EVIDENCE=21_OF_21_PASS")
print("AUTHOR_CHECKPOINT_MINIMAL_GIT_WITNESS=PASS")
print("TS_RR01_TO_TS_RR15_DECISIONS=BLANK")
print("OVERALL_TECHNICAL_REVIEW_DECISION=BLANK")
print("HUMAN_REVIEWER_IDENTITY_FIELDS=BLANK")
print("CANONICAL_CURL_SPECIFICATION_AUTHORIZED=NO")
print("GENERATED_DRIVER_INSPECTION_AUTHORIZED=NO")
print("GOLD_ANNOTATION_AUTHORIZED=NO")
print("ANALYZER_IMPLEMENTATION_AUTHORIZED=NO")
print("BASELINE_EXECUTION_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
print("CURL_TECHNICAL_WORKING_DRAFT_V1_REVIEW_PACKAGE_VERIFICATION=PASS")
