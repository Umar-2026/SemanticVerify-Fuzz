#!/usr/bin/env python3

import hashlib
import json
import re
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


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


review = here / "01_completed_human_technical_review.v1.md"
meta = here / "02_completed_human_technical_review_record.v1.json"

decision = (
    repo
    / "documentation"
    / "decisions"
    / "0028-curl-technical-working-draft-v1-human-review-revision-required.md"
)

draft = (
    repo
    / "config"
    / "annotation"
    / "curl_technical_protocol_working_draft.v1.json"
)

expected_review_sha = (
    "e253340d540a06cd24af501c569154869ac0324d677995b7266349ba097973cc"
)

expected_draft_sha = (
    "80498e0c4e021700e2a2c09654a852e67b16df86d61fbb28857d14a12fed44c6"
)

if not review.is_file():
    fail("REVIEW_FILE_MISSING")

if sha(review) != expected_review_sha:
    fail("REVIEW_FILE_SHA256")

if not draft.is_file():
    fail("WORKING_DRAFT_V1_MISSING")

if sha(draft) != expected_draft_sha:
    fail("WORKING_DRAFT_V1_SHA256")

text = review.read_text(encoding="utf-8").replace("\\_", "_")

expected = {
    "TS-RR01": "PASS",
    "TS-RR02": "PASS",
    "TS-RR03": "PASS",
    "TS-RR04": "PASS",
    "TS-RR05": "REVISION_REQUIRED",
    "TS-RR06": "REVISION_REQUIRED",
    "TS-RR07": "REVISION_REQUIRED",
    "TS-RR08": "REVISION_REQUIRED",
    "TS-RR09": "REVISION_REQUIRED",
    "TS-RR10": "REVISION_REQUIRED",
    "TS-RR11": "REVISION_REQUIRED",
    "TS-RR12": "REVISION_REQUIRED",
    "TS-RR13": "REVISION_REQUIRED",
    "TS-RR14": "REVISION_REQUIRED",
    "TS-RR15": "PASS",
}

for rr, wanted in expected.items():
    h = re.search(
        rf"^### {re.escape(rr)}\b[^\n]*$",
        text,
        re.M,
    )

    if not h:
        fail("REVIEW_ITEM_MISSING|" + rr)

    tail = text[h.end():]

    nxt = re.search(
        r"^### TS-RR\d{2}\b[^\n]*$|"
        r"^## Overall technical review decision\b",
        tail,
        re.M,
    )

    section = tail[:nxt.start()] if nxt else tail

    vals = re.findall(
        r"^Decision:[ \t]*(.*)$",
        section,
        re.M,
    )

    if len(vals) != 1:
        fail(
            "DECISION_LINE_COUNT|"
            + rr + "|" + str(len(vals))
        )

    observed = vals[0].strip().replace("\\_", "_")

    if observed != wanted:
        fail(
            "DECISION_MISMATCH|"
            + rr
            + "|OBSERVED=" + observed
            + "|EXPECTED=" + wanted
        )

overall = re.findall(
    r"^Overall decision:[ \t]*(.*)$",
    text,
    re.M,
)

if (
    len(overall) != 1
    or overall[0].strip().replace("\\_", "_")
    != "REVISION_REQUIRED"
):
    fail("OVERALL_DECISION")

role = re.findall(
    r"^Reviewer role ID:[ \t]*`([^`]+)`[ \t]*$",
    text,
    re.M,
)

if role != ["Spec-Technical-Reviewer-1"]:
    fail("REVIEWER_ROLE")

record = json.loads(meta.read_text(encoding="utf-8"))

if record["completed_review"]["sha256"] != expected_review_sha:
    fail("METADATA_REVIEW_SHA")

if (
    record["completed_review"]["overall_decision"]
    != "REVISION_REQUIRED"
):
    fail("METADATA_OVERALL_DECISION")

if record["governance_effect"]["working_draft_v1_remains_immutable"] is not True:
    fail("V1_IMMUTABILITY")

if record["governance_effect"]["working_draft_v2_successor_required"] is not True:
    fail("V2_SUCCESSOR_REQUIREMENT")

blocked = (
    "canonical_curl_specification_authorized",
    "generated_driver_inspection_authorized",
    "selected_sample_membership_inspection_authorized",
    "gold_annotation_authorized",
    "analyzer_implementation_authorized",
    "baseline_execution_authorized",
    "repair_authorized",
)

for key in blocked:
    if record["governance_effect"][key] is not False:
        fail("BLOCKED_BOUNDARY_CHANGED|" + key)

if not decision.is_file():
    fail("DECISION_0028_MISSING")

dtext = decision.read_text(encoding="utf-8")

for required in (
    expected_review_sha,
    expected_draft_sha,
    "REVISION_REQUIRED",
    "AUTHORIZE_CURL_TECHNICAL_WORKING_DRAFT_V2_SUCCESSOR",
):
    if required not in dtext:
        fail("DECISION_0028_BINDING|" + required)

print("EXACT_COMPLETED_HUMAN_REVIEW_SHA256=PASS")
print("EXACT_WORKING_DRAFT_V1_BINDING=PASS")
print("TS_RR01_TO_TS_RR15_DECISIONS=PASS")
print("OVERALL_TECHNICAL_REVIEW_DECISION=REVISION_REQUIRED")
print("REVIEWER_IDENTITY_BINDING=PASS")
print("DECISION_0028_BINDING=PASS")
print("WORKING_DRAFT_V1_IMMUTABLE=YES")
print("WORKING_DRAFT_V2_SUCCESSOR_REQUIRED=YES")
print("CANONICAL_CURL_SPECIFICATION_AUTHORIZED=NO")
print("GENERATED_DRIVER_INSPECTION_AUTHORIZED=NO")
print("SELECTED_SAMPLE_MEMBERSHIP_INSPECTION_AUTHORIZED=NO")
print("GOLD_ANNOTATION_AUTHORIZED=NO")
print("ANALYZER_IMPLEMENTATION_AUTHORIZED=NO")
print("BASELINE_EXECUTION_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
print("COMPLETED_HUMAN_TECHNICAL_REVIEW_RECORD_VERIFICATION=PASS")
