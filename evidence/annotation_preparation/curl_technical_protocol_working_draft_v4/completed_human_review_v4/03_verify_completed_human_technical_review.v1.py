#!/usr/bin/env python3

import hashlib
import json
import re
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


V4_SHA = (
    "e17ae2ea5a70bdd790c946eb4b89ca37368d749cd7463159e69514d88a50cea8"
)

V3_SHA = (
    "2c10317a7a1fa745d64b461bb318ac2aa1e3e23439ca261c8cd746d1ea3f8ac2"
)

REVIEW_SHA = (
    "074814c04922f7cbc5fa41ef460cbde74dcb32529c09ef5752cf1d0f511f2aed"
)

PACKAGE_SUMS_SHA = (
    "5d5d19a0f151767b59ebb88fb1f9d573c1ca96df5318585e01bde6fa218f639f"
)

v4p = (
    repo
    / "config/annotation/"
      "curl_technical_protocol_working_draft.v4.json"
)

v3p = (
    repo
    / "config/annotation/"
      "curl_technical_protocol_working_draft.v3.json"
)

reviewp = here / "01_completed_human_technical_review.v4.md"
recordp = here / "02_completed_human_technical_review_record.v1.json"

pkg = (
    repo
    / "evidence/annotation_preparation/"
      "curl_technical_protocol_working_draft_v4/"
      "review_package_v4"
)

pkg_sums = pkg / "19_review_package.v4.SHA256SUMS"

decisionp = (
    repo
    / "documentation/decisions/"
      "0037-curl-technical-working-draft-v4-human-review-approved.md"
)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


if sha(v4p) != V4_SHA:
    fail("V4_IMMUTABILITY_SHA")

if v4p.stat().st_size != 41033:
    fail("V4_IMMUTABILITY_SIZE")

if sha(v3p) != V3_SHA:
    fail("V3_IMMUTABILITY_SHA")

if sha(reviewp) != REVIEW_SHA:
    fail("COMPLETED_V4_REVIEW_SHA")

if reviewp.stat().st_size != 24722:
    fail("COMPLETED_V4_REVIEW_SIZE")

if sha(pkg_sums) != PACKAGE_SUMS_SHA:
    fail("IMMUTABLE_REVIEW_PACKAGE_SUMS_SHA")


text = (
    reviewp.read_text(encoding="utf-8")
    .replace("\\_", "_")
    .replace("\r\n", "\n")
    .replace("\r", "\n")
)

observed = {}

for i in range(1, 13):
    rr = f"V4-RR{i:02d}"

    heads = list(
        re.finditer(
            rf"^###\s+{re.escape(rr)}\b[^\n]*$",
            text,
            re.M,
        )
    )

    if len(heads) != 1:
        fail(
            "REVIEW_HEADING_COUNT|"
            + rr
            + "|"
            + str(len(heads))
        )

    tail = text[heads[0].end():]

    nxt = re.search(
        r"^###\s+V4-RR\d{2}\b[^\n]*$|"
        r"^##\s+Overall technical review decision\b",
        tail,
        re.M,
    )

    section = tail[:nxt.start()] if nxt else tail

    decisions = re.findall(
        r"^Decision:[ \t]*"
        r"(PASS|REVISION_REQUIRED|FAIL)[ \t]*$",
        section,
        re.M,
    )

    if decisions != ["PASS"]:
        fail(
            "REVIEW_DECISION|"
            + rr
            + "|"
            + repr(decisions)
        )

    observed[rr] = "PASS"


overall = re.findall(
    r"^Overall decision:[ \t]*"
    r"(APPROVE_EXACT_WORKING_DRAFT_V4_FOR_CANONICALIZATION|"
    r"REVISION_REQUIRED|FAIL)[ \t]*$",
    text,
    re.M,
)

if overall != [
    "APPROVE_EXACT_WORKING_DRAFT_V4_FOR_CANONICALIZATION"
]:
    fail("OVERALL_REVIEW_DECISION|" + repr(overall))


identity = {
    "role": (
        r"^Reviewer role ID:[ \t]*`?([^`\n]+?)`?[ \t]*$",
        "Spec-Technical-Reviewer-1",
    ),
    "name": (
        r"^Human reviewer name:[ \t]*(.+?)[ \t]*$",
        "Abdul Raheem Shahzad",
    ),
    "confirmation": (
        r"^Human reviewer signature / recorded confirmation:"
        r"[ \t]*(.+?)[ \t]*$",
        "ARS",
    ),
    "date": (
        r"^Human reviewer date:[ \t]*(.+?)[ \t]*$",
        "19 / August / 2026",
    ),
}

for field, (pattern, wanted) in identity.items():
    vals = re.findall(pattern, text, re.M)

    if len(vals) != 1 or vals[0].strip() != wanted:
        fail(
            "REVIEWER_IDENTITY|"
            + field
            + "|"
            + repr(vals)
        )


record = json.loads(
    recordp.read_text(encoding="utf-8")
)

if record["review_target"]["sha256"] != V4_SHA:
    fail("RECORD_V4_SHA")

if record["review_target"]["size_bytes"] != 41033:
    fail("RECORD_V4_SIZE")

if record["review_target"]["author_checkpoint_commit"] != \
        "b98d76536376b21fc6f2e85a060e960e1681453c":
    fail("RECORD_AUTHOR_CHECKPOINT_COMMIT")

if record["review_target"]["author_checkpoint_tree"] != \
        "e7243cda2f8afd9b6cceff793ab0cfa723fabbe5":
    fail("RECORD_AUTHOR_CHECKPOINT_TREE")

if record["review_target"]["review_package_commit"] != \
        "e123bd412eb316b0857365e03788b19596fb7406":
    fail("RECORD_REVIEW_PACKAGE_COMMIT")

if record["review_target"]["review_package_tree"] != \
        "1f31c28940b046427ede83bcd18cec3c6b118fda":
    fail("RECORD_REVIEW_PACKAGE_TREE")

if record["review_target"][
    "review_package_checksum_manifest_sha256"
] != PACKAGE_SUMS_SHA:
    fail("RECORD_PACKAGE_SUMS_SHA")

completed = record["completed_human_review"]

if completed["sha256"] != REVIEW_SHA:
    fail("RECORD_REVIEW_SHA")

if completed["size_bytes"] != 24722:
    fail("RECORD_REVIEW_SIZE")

if completed["decision_counts"] != {
    "PASS": 12,
    "REVISION_REQUIRED": 0,
    "FAIL": 0,
}:
    fail("RECORD_DECISION_COUNTS")

if completed["overall_decision"] != \
        "APPROVE_EXACT_WORKING_DRAFT_V4_FOR_CANONICALIZATION":
    fail("RECORD_OVERALL_DECISION")

if set(completed["review_item_decisions"]) != {
    f"V4-RR{i:02d}"
    for i in range(1, 13)
}:
    fail("RECORD_REVIEW_ITEM_SET")

if any(
    value != "PASS"
    for value in completed["review_item_decisions"].values()
):
    fail("RECORD_NON_PASS_ITEM")


effect = record["technical_effect"]

if effect[
    "exact_v4_technically_adequate_for_later_canonicalization_authorization"
] is not True:
    fail("TECHNICAL_ELIGIBILITY")

if effect[
    "human_review_itself_authorizes_canonicalization"
] is not False:
    fail("REVIEW_SELF_AUTHORIZATION")

if effect[
    "human_review_itself_creates_canonical_curl_json"
] is not False:
    fail("REVIEW_SELF_CREATION")

if effect[
    "separate_canonicalization_authorization_required"
] is not True:
    fail("SEPARATE_AUTHORIZATION_REQUIREMENT")

if effect[
    "approved_v4_must_remain_immutable"
] is not True:
    fail("APPROVED_V4_IMMUTABILITY")


if record["next_boundary"] != \
        "AUTHORIZE_CANONICAL_CURL_SPECIFICATION_FROM_APPROVED_V4":
    fail("NEXT_BOUNDARY")


for key, value in record["non_authorizations"].items():
    if value is not False:
        fail("NON_AUTHORIZATION|" + key)


if not decisionp.is_file():
    fail("DECISION_0037_MISSING")

dt = decisionp.read_text(encoding="utf-8")

for marker in (
    V4_SHA,
    REVIEW_SHA,
    "12 PASS / 0 REVISION_REQUIRED / 0 FAIL",
    "APPROVE_EXACT_WORKING_DRAFT_V4_FOR_CANONICALIZATION",
    "This human review does not itself authorize canonicalization.",
    "Canonical `curl.json` has not been created.",
    "A separate explicit canonicalization authorization is required",
    "AUTHORIZE_CANONICAL_CURL_SPECIFICATION_FROM_APPROVED_V4",
):
    if marker not in dt:
        fail("DECISION_0037_BINDING|" + marker)


print("WORKING_DRAFT_V4_IMMUTABILITY_SHA256=PASS")
print("WORKING_DRAFT_V4_IMMUTABILITY_SIZE=PASS")
print("WORKING_DRAFT_V3_IMMUTABILITY_SHA256=PASS")
print("IMMUTABLE_V4_REVIEW_PACKAGE_BINDING=PASS")
print("COMPLETED_V4_HUMAN_REVIEW_SHA256=PASS")
print("COMPLETED_V4_HUMAN_REVIEW_SIZE=PASS")
print("V4_RR01_TO_V4_RR12_COMPLETED_DECISIONS=12_OF_12_PASS")
print("REVIEW_DECISION_DISTRIBUTION=12_PASS_0_REVISION_REQUIRED_0_FAIL")
print(
    "OVERALL_TECHNICAL_REVIEW_DECISION="
    "APPROVE_EXACT_WORKING_DRAFT_V4_FOR_CANONICALIZATION"
)
print("REVIEWER_IDENTITY=PASS")
print("EXACT_V4_TECHNICALLY_ELIGIBLE_FOR_CANONICALIZATION_AUTHORIZATION=YES")
print("V4_MUST_REMAIN_IMMUTABLE=YES")
print("CANONICAL_CURL_SPECIFICATION_AUTHORIZED=NO")
print("CANONICAL_CURL_SPECIFICATION_CREATED=NO")
print("GENERATED_DRIVER_INSPECTION_AUTHORIZED=NO")
print("SELECTED_SAMPLE_MEMBERSHIP_INSPECTION_AUTHORIZED=NO")
print("GOLD_ANNOTATION_AUTHORIZED=NO")
print("ANALYZER_IMPLEMENTATION_AUTHORIZED=NO")
print("ANALYZER_EXECUTION_AUTHORIZED=NO")
print("BASELINE_EXECUTION_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
print("COMPLETED_CURL_TECHNICAL_V4_HUMAN_REVIEW_VERIFICATION=PASS")
