#!/usr/bin/env python3

import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]

REVIEW = (
    HERE
    / "01_completed_RIAC01_RIAC08_human_review.EXACT_COPY.v1.md"
)

RECORD = (
    HERE
    / "02_completed_human_review_record.v1.json"
)

SUMS = (
    HERE
    / "04_completed_human_review.v1.SHA256SUMS"
)

BASE_REL = (
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2"
)

HANDOFF = (
    REPO
    / BASE_REL
    / "schema_v2_relation_informed_exhaustive_"
      "admissible_composition_study_v1_external_review_handoff_v1"
)

HANDOFF_SAFE = (
    HANDOFF
    / "07_verify_external_independent_review_handoff.v1.py"
)

HANDOFF_MANIFEST = (
    HANDOFF
    / "08_external_review_handoff_manifest.v1.json"
)

HANDOFF_SUMS = (
    HANDOFF
    / "09_external_review_handoff.v1.SHA256SUMS"
)

DEC0107 = (
    REPO
    / "documentation/decisions/"
      "0107-record-external-independent-review-handoff-v1-author-checkpoint.md"
)

STUDY = (
    REPO
    / BASE_REL
    / "schema_v2_relation_informed_exhaustive_"
      "admissible_composition_study_v1/"
      "01_relation_informed_exhaustive_admissible_composition_study.v1.json"
)

EXPECTED = {
    REVIEW:
        "7730e555a2d85b96dae1c75d20ef23da7670831feb3f398eaac600c64d323d98",

    HANDOFF_SAFE:
        "9afd2ba0dd832df8a50beb1f342f724754becec3a89bdc7eedabe60867851bc3",

    HANDOFF_MANIFEST:
        "22b0fb98b6845ef35aa6a874c613212744553e048f3074e281b9c03870fbf985",

    HANDOFF_SUMS:
        "da45b6167b06156323340fd62e47323a8913f45c48289fcc22a4443bbedfcc48",

    DEC0107:
        "7a9610926c46ed3c9178363c70e6be9aa51ffe11429de1b9e38ac914c1b341af",

    STUDY:
        "a8d28b09e78e1466eb5bb0991289879b28b10abd1dd1f9197d138ca723718f6f",
}

def fail(msg):
    print("FAIL|" + msg)
    raise SystemExit(1)

def sha(path):
    if not path.is_file():
        fail("MISSING|" + str(path))

    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()

for path, expected in EXPECTED.items():
    if sha(path) != expected:
        fail(
            "SOURCE_BINDING|" + str(path)
        )

raw = REVIEW.read_bytes()

if len(raw) != 9240:
    fail("REVIEW_SIZE")

if raw.count(b"\r\n") != 84:
    fail("REVIEW_CRLF_COUNT")

text = raw.decode("utf-8")

if "Package state: `COMPLETED — INDEPENDENT HUMAN REVIEW RECORDED`" not in text:
    fail("REVIEW_COMPLETION_STATE")

for rid in (
    "RIAC01",
    "RIAC02",
    "RIAC03",
    "RIAC04",
    "RIAC05",
    "RIAC06",
    "RIAC07",
    "RIAC08",
):
    section = re.search(
        rf"^## {rid} — .*?"
        rf"(?=^## RIAC\d{{2}} —|^# Overall review decision)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )

    if not section:
        fail(
            "REVIEW_SECTION|" + rid
        )

    decision = re.search(
        r"^Decision:\s*`([^`]+)`\s*$",
        section.group(0),
        flags=re.MULTILINE,
    )

    if not decision:
        fail(
            "REVIEW_DECISION_MISSING|" + rid
        )

    if decision.group(1) != "PASS":
        fail(
            "REVIEW_DECISION_NOT_PASS|"
            + rid
        )

overall = re.search(
    r"^Overall decision:\s*`([^`]+)`\s*$",
    text,
    flags=re.MULTILINE,
)

expected_overall = (
    "APPROVE_RELATION_INFORMED_EXHAUSTIVE_"
    "ADMISSIBLE_COMPOSITION_STUDY_V1"
)

if not overall or overall.group(1) != expected_overall:
    fail(
        "OVERALL_REVIEW_DECISION"
    )

record = json.loads(
    RECORD.read_text(
        encoding="utf-8"
    )
)

if record["status"] != \
        "COMPLETED_HUMAN_REVIEW_RECORDED_NOT_GOVERNANCE_ADOPTED":
    fail(
        "RECORD_STATUS"
    )

for rid in (
    "RIAC01",
    "RIAC02",
    "RIAC03",
    "RIAC04",
    "RIAC05",
    "RIAC06",
    "RIAC07",
    "RIAC08",
):
    if record["item_decisions"][rid] != "PASS":
        fail(
            "RECORD_ITEM_DECISION|" + rid
        )

if record["overall_review_decision"] != \
        expected_overall:
    fail(
        "RECORD_OVERALL_DECISION"
    )

reviewer = record["reviewer"]

if reviewer != {
    "date": "23 / August / 2026",
    "name": "Abdul Raheem Shahzad",
    "recorded_confirmation": "ARS",
    "role": "Spec-Technical-Reviewer-1",
}:
    fail(
        "REVIEWER_BINDING"
    )

interp = record["review_interpretation"]

if interp[
    "independent_human_review_completed"
] is not True:
    fail(
        "HUMAN_REVIEW_COMPLETION"
    )

if interp[
    "all_eight_review_items_passed"
] is not True:
    fail(
        "ALL_ITEMS_PASS"
    )

if interp[
    "overall_human_review_approval_recorded"
] is not True:
    fail(
        "OVERALL_APPROVAL_RECORD"
    )

if interp[
    "study_governance_adopted"
] is not False:
    fail(
        "PREMATURE_GOVERNANCE_ADOPTION"
    )

if interp[
    "technical_outcome_changed_by_review"
] is not False:
    fail(
        "TECHNICAL_OUTCOME_MUTATED"
    )

study = json.loads(
    STUDY.read_text(
        encoding="utf-8"
    )
)

if study["status"] != "AUTHOR_CANDIDATE":
    fail(
        "STUDY_STATUS"
    )

if study["global_outcome"] != \
        "FURTHER_EVIDENCE_REQUIRED":
    fail(
        "STUDY_GLOBAL_OUTCOME"
    )

for key, value in record[
    "bounded_nonclaims"
].items():
    if value is not False:
        fail(
            "BOUNDED_NONCLAIM|" + key
        )

for key, value in record[
    "retired_verifier_state"
].items():
    if key == \
            "retired_verifiers_executed_during_review_recording":
        if value is not False:
            fail(
                "RETIRED_VERIFIER_EXECUTION"
            )
    else:
        if value != "PERMANENTLY_RETIRED":
            fail(
                "RETIRED_VERIFIER_STATE|" + key
            )

if SUMS.is_file():
    lines = [
        x
        for x in SUMS.read_text(
            encoding="utf-8"
        ).splitlines()
        if x.strip()
    ]

    if len(lines) != 3:
        fail(
            "CHECKSUM_ENTRY_COUNT|"
            + str(len(lines))
        )

    for line in lines:
        digest, rel = line.split(
            None,
            1,
        )

        rel = rel.strip().lstrip("*")
        path = HERE / rel

        if sha(path) != digest:
            fail(
                "CHECKSUM|" + rel
            )

print("COMPLETED_HUMAN_REVIEW_EXACT_BINDING=PASS")
print("RIAC01_DECISION=PASS")
print("RIAC02_DECISION=PASS")
print("RIAC03_DECISION=PASS")
print("RIAC04_DECISION=PASS")
print("RIAC05_DECISION=PASS")
print("RIAC06_DECISION=PASS")
print("RIAC07_DECISION=PASS")
print("RIAC08_DECISION=PASS")

print(
    "OVERALL_REVIEW_DECISION="
    + expected_overall
)

print("HUMAN_REVIEWER=Abdul Raheem Shahzad")
print("HUMAN_REVIEWER_CONFIRMATION=ARS")
print("HUMAN_REVIEWER_DATE=23 / August / 2026")
print("HUMAN_REVIEWER_ROLE=Spec-Technical-Reviewer-1")

print("INDEPENDENT_HUMAN_REVIEW_COMPLETED=YES")
print("OVERALL_HUMAN_REVIEW_APPROVAL_RECORDED=YES")

print("STUDY_STATUS=AUTHOR_CANDIDATE")
print("GLOBAL_OUTCOME=FURTHER_EVIDENCE_REQUIRED")
print("STUDY_GOVERNANCE_ADOPTED=NO")

print("POSITIVE_EXISTING_V2_MAPPING_PROVEN=NO")
print("NEGATIVE_EXISTING_V2_MAPPING_IMPOSSIBILITY_PROVEN=NO")
print("WHOLE_V4_ADMISSIBLE_COMPOSITION_EXHAUSTIVENESS_PROVEN=NO")

print("OPERATIONAL_POSITIVE_MAPPING_AUTHORIZED=NO")
print("SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO")
print("CURL_JSON_AUTHORIZED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")

print("RETIRED_A02_VERIFIERS_EXECUTED=NO")
print("REPOSITORY_COMPLETED_RIAC01_RIAC08_HUMAN_REVIEW=PASS")
