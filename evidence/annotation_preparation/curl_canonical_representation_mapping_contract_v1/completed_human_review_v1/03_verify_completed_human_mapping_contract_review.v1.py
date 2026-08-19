#!/usr/bin/env python3

import hashlib
import json
import re
from pathlib import Path


def fail(msg):
    print("FAIL|" + msg)
    raise SystemExit(1)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


here = Path(__file__).resolve().parent

repo = here
while repo != repo.parent and not (repo / ".git").exists():
    repo = repo.parent

if not (repo / ".git").exists():
    fail("REPOSITORY_ROOT_NOT_FOUND")


reviewp = (
    here
    / "01_completed_human_mapping_contract_review.v1.md"
)

recordp = (
    here
    / "02_completed_human_mapping_contract_review_record.v1.json"
)

contractp = (
    repo
    / "config/annotation/"
      "curl_canonical_representation_mapping_contract.v1.json"
)

v4p = (
    repo
    / "config/annotation/"
      "curl_technical_protocol_working_draft.v4.json"
)

schemap = (
    repo
    / "config/schemas/"
      "protocol_specification.schema.json"
)

decisionp = (
    repo
    / "documentation/decisions/"
      "0040-curl-canonical-mapping-contract-v1-human-review-approved.md"
)

curlp = (
    repo
    / "config/protocol_specifications/curl.json"
)


REVIEW_SHA = (
    "a19d4a6132be417798b027794045227949ea40265e11714543e85ef1c325ad73"
)

CONTRACT_SHA = (
    "31d606f98f2c819291103ba7403214206ccde1d8e5e0e9103f0659c227622257"
)

V4_SHA = (
    "e17ae2ea5a70bdd790c946eb4b89ca37368d749cd7463159e69514d88a50cea8"
)

SCHEMA_SHA = (
    "7eb17eeb8f49b37420d0d1d71539cf0d7cb08241ecf133e7b4139fd130718b34"
)


if sha(reviewp) != REVIEW_SHA:
    fail("COMPLETED_REVIEW_SHA")

if reviewp.stat().st_size != 24169:
    fail("COMPLETED_REVIEW_SIZE")

if sha(contractp) != CONTRACT_SHA:
    fail("MAPPING_CONTRACT_SHA")

if contractp.stat().st_size != 10879:
    fail("MAPPING_CONTRACT_SIZE")

if sha(v4p) != V4_SHA:
    fail("APPROVED_V4_SHA")

if v4p.stat().st_size != 41033:
    fail("APPROVED_V4_SIZE")

if sha(schemap) != SCHEMA_SHA:
    fail("FROZEN_SCHEMA_SHA")


text = (
    reviewp.read_text(encoding="utf-8")
    .replace("\r\n", "\n")
    .replace("\r", "\n")
    .replace("\\#", "#")
    .replace("\\_", "_")
)

for i in range(1, 11):
    rr = f"CMR-RR{i:02d}"

    heads = list(
        re.finditer(
            rf"^###\s+{re.escape(rr)}\b[^\n]*$",
            text,
            re.M,
        )
    )

    if len(heads) != 1:
        fail(
            f"REVIEW_HEADING_COUNT|{rr}|{len(heads)}"
        )

    tail = text[heads[0].end():]

    nxt = re.search(
        r"^###\s+CMR-RR\d{2}\b[^\n]*$|"
        r"^##\s+Overall technical review decision\b",
        tail,
        re.M,
    )

    section = tail[:nxt.start()] if nxt else tail

    values = re.findall(
        r"^Decision:[ \t]*(.*?)[ \t]*$",
        section,
        re.M,
    )

    if len(values) != 1:
        fail(
            f"DECISION_COUNT|{rr}|{len(values)}"
        )

    if values[0].strip() != "PASS":
        fail(
            f"ITEM_NOT_PASS|{rr}|{values[0].strip()}"
        )


overall = re.findall(
    r"^Overall decision:[ \t]*(.*?)[ \t]*$",
    text,
    re.M,
)

if len(overall) != 1:
    fail("OVERALL_DECISION_COUNT")

if overall[0].strip() != \
        "APPROVE_MAPPING_BLOCKER_CONTRACT":
    fail("OVERALL_DECISION")


required_identity = {
    "Human reviewer name":
        "Abdul Raheem Shahzad",

    "Human reviewer signature / recorded confirmation":
        "ARS",

    "Human reviewer date":
        "19 / August / 2026",
}

for label, expected in required_identity.items():
    pattern = (
        "^"
        + re.escape(label)
        + r":[ \t]*(.*?)[ \t]*$"
    )

    vals = re.findall(
        pattern,
        text,
        re.M,
    )

    if len(vals) != 1:
        fail(
            "IDENTITY_FIELD_COUNT|"
            + label
        )

    if vals[0].strip() != expected:
        fail(
            "IDENTITY_VALUE|"
            + label
        )


if (
    "Reviewer role ID: `Spec-Technical-Reviewer-1`"
    not in text
):
    fail("REVIEWER_ROLE_ID")


record = json.loads(
    recordp.read_text(encoding="utf-8")
)

if record["status"] != \
        "COMPLETED_HUMAN_REVIEW_RECORDED":
    fail("RECORD_STATUS")

hr = record["exact_human_review"]

if hr["sha256"] != REVIEW_SHA:
    fail("RECORD_REVIEW_SHA")

if hr["size_bytes"] != 24169:
    fail("RECORD_REVIEW_SIZE")

if hr["decision_counts"] != {
    "PASS": 10,
    "REVISION_REQUIRED": 0,
    "FAIL": 0,
}:
    fail("RECORD_DECISION_COUNTS")

if hr["overall_decision"] != \
        "APPROVE_MAPPING_BLOCKER_CONTRACT":
    fail("RECORD_OVERALL_DECISION")

if hr["human_reviewer_name"] != \
        "Abdul Raheem Shahzad":
    fail("RECORD_REVIEWER_NAME")

if hr["human_reviewer_confirmation"] != "ARS":
    fail("RECORD_REVIEWER_CONFIRMATION")

if hr["human_reviewer_date"] != \
        "19 / August / 2026":
    fail("RECORD_REVIEWER_DATE")

if hr["assistant_generated_or_synthetic"] is not False:
    fail("SYNTHETIC_REVIEW_FLAG")


effect = record["human_review_effect"]

expected_false = (
    "lossless_v4_to_frozen_schema_mapping_proven",
    "positive_mapping_algorithm_approved",
    "canonical_schema_successor_approved",
    "canonical_materialization_safe",
    "curl_json_authorized_by_this_review",
    "curl_json_created",
)

if effect[
    "mapping_blocker_contract_v1_approved"
] is not True:
    fail("BLOCKER_CONTRACT_APPROVAL_STATUS")

for key in expected_false:
    if effect[key] is not False:
        fail("REVIEW_EFFECT|" + key)


for key, value in record[
    "evidence_quarantine"
].items():
    if value is not False:
        fail("EVIDENCE_QUARANTINE|" + key)


for key, value in record[
    "downstream_non_authorizations"
].items():
    if value is not False:
        fail("DOWNSTREAM_AUTHORIZATION|" + key)


if record["next_boundary"] != \
        "AUTHORIZE_CURL_CANONICAL_REPRESENTATION_MAPPING_CONTRACT_V2_SUCCESSOR":
    fail("NEXT_BOUNDARY")


if not decisionp.is_file():
    fail("DECISION_0040_MISSING")

decision = decisionp.read_text(
    encoding="utf-8"
)

for marker in (
    REVIEW_SHA,
    CONTRACT_SHA,
    V4_SHA,
    SCHEMA_SHA,
    "10 PASS / 0 REVISION_REQUIRED / 0 FAIL",
    "APPROVE_MAPPING_BLOCKER_CONTRACT",
    "LOSSLESS_V4_TO_FROZEN_SCHEMA_MAPPING_PROVEN=NO",
    "POSITIVE_MAPPING_ALGORITHM_APPROVED=NO",
    "CANONICAL_SCHEMA_SUCCESSOR_APPROVED=NO",
    "CANONICAL_MATERIALIZATION_SAFE=NO",
    "CURL_JSON_CREATED=NO",
    "AUTHORIZE_CURL_CANONICAL_REPRESENTATION_MAPPING_CONTRACT_V2_SUCCESSOR",
):
    if marker not in decision:
        fail(
            "DECISION_0040_BINDING|"
            + marker
        )


if curlp.exists():
    fail("CURL_JSON_PREMATURELY_EXISTS")


print("EXACT_COMPLETED_HUMAN_REVIEW_SHA256=PASS")
print("EXACT_COMPLETED_HUMAN_REVIEW_SIZE=PASS")
print("CMR_RR01_TO_CMR_RR10=10_PASS")
print("OVERALL_TECHNICAL_REVIEW_DECISION=APPROVE_MAPPING_BLOCKER_CONTRACT")
print("HUMAN_REVIEWER_NAME=Abdul Raheem Shahzad")
print("HUMAN_REVIEWER_CONFIRMATION=ARS")
print("HUMAN_REVIEWER_DATE=19 / August / 2026")
print("SYNTHETIC_HUMAN_APPROVAL_PRESENT=NO")
print("MAPPING_BLOCKER_CONTRACT_V1_APPROVED=YES")
print("LOSSLESS_V4_TO_FROZEN_SCHEMA_MAPPING_PROVEN=NO")
print("POSITIVE_MAPPING_ALGORITHM_APPROVED=NO")
print("CANONICAL_SCHEMA_SUCCESSOR_APPROVED=NO")
print("CANONICAL_MATERIALIZATION_SAFE=NO")
print("CURL_JSON_CREATED=NO")
print("ANALYZER_IMPLEMENTATION_AUTHORIZED=NO")
print("BASELINE_EXECUTION_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
print("COMPLETED_HUMAN_MAPPING_CONTRACT_V1_REVIEW_RECORD=PASS")
