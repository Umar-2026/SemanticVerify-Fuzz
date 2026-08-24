#!/usr/bin/env python3

import hashlib
import json
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]

BASE_REL = (
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2"
)

EXACT = (
    HERE
    / "01_completed_SUCR01_C_focused_rereview.EXACT_COPY.v1.md"
)

RECORD = (
    HERE
    / "02_completed_focused_rereview_record.v1.json"
)

SUMS = (
    HERE
    / "04_completed_focused_rereview.v1.SHA256SUMS"
)

HANDOFF_REL = (
    BASE_REL
    + "/schema_v2_sucr01_focused_independent_rereview_package_and_external_handoff_v1"
)

HANDOFF = (
    REPO
    / HANDOFF_REL
)

H05 = (
    HANDOFF
    / "05_SUCR01_C_focused_rereview_packet.MANUAL_REVIEW_COPY.v1.md"
)

H06 = (
    HANDOFF
    / "06_focused_rereview_source_binding_manifest.v1.json"
)

H07 = (
    HANDOFF
    / "07_focused_rereview_handoff_manifest.v1.json"
)

H08 = (
    HANDOFF
    / "08_verify_focused_sucr01_rereview_handoff.v1.py"
)

H09 = (
    HANDOFF
    / "09_focused_sucr01_rereview_handoff.v1.SHA256SUMS"
)

DEC0120 = (
    REPO
    / "documentation/decisions/"
      "0120-record-focused-independent-sucr01-rereview-package-and-external-handoff-v1.md"
)

EXPECTED = {
    EXACT:
        "6cb5ce2104150229809c6a870623e47161d4b2415bb97e6222ec98d2e0b45736",

    H05:
        "ae189cf4bc861213a888772ad26cf3937bec7c92a11c0e48c4ff917b9e625376",

    H06:
        "bd997dbeaf19036cdb084ed7fa4f908810704bf10e768351dc8302740a4786ae",

    H07:
        "9f30cb2393f1439850ac2865db62d2be674ac6d8dda529c6145a5c2f8d4a71af",

    H08:
        "63415068e07910977094a95bb03477444f4fb8d335847bbfc569622010988396",

    H09:
        "91f94c1004aa4fc53abf7aea9e9e32ca384f6def6d2424e31b81faf0c0701a16",

    DEC0120:
        "c1a01d8db83d9902dfe0df7014aeda2dc248f64597ef381bfb74fa8d287981f6",
}

def fail(msg):
    print(
        "FAIL|" + msg
    )
    raise SystemExit(1)

def sha(path):

    if not path.is_file():
        fail(
            "MISSING|" + str(path)
        )

    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()

for path, expected in EXPECTED.items():

    if sha(path) != expected:
        fail(
            "SOURCE_BINDING|"
            + str(path)
        )

p = subprocess.run(
    [
        "git",
        "-C",
        str(REPO),
        "rev-parse",
        "HEAD:" + HANDOFF_REL,
    ],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    check=False,
)

if p.returncode != 0:
    fail(
        "HANDOFF_GIT_TREE_READ"
    )

if p.stdout.strip() != \
        "184f3931575d2565422cec4965878553421108d8":
    fail(
        "HANDOFF_GIT_TREE"
    )

b = EXACT.read_bytes()

if len(b) != 4916:
    fail(
        "COMPLETED_REVIEW_SIZE"
    )

if b.count(b"\r\n") != 75:
    fail(
        "COMPLETED_REVIEW_CRLF"
    )

if len(b.splitlines()) != 76:
    fail(
        "COMPLETED_REVIEW_LINES"
    )

text = b.decode("utf-8")

m = re.search(
    r"^Decision:\s*`([^`]+)`\s*$",
    text,
    flags=re.MULTILINE,
)

if not m or m.group(1).strip() != \
        "PASS":
    fail(
        "SUCR01_C_DECISION"
    )

expected_overall = (
    "APPROVE_SUCR01_CORRECTIVE_PORTABLE_SOURCE_EVIDENCE_SUCCESSOR_PACKAGE_V2"
)

m = re.search(
    r"^Overall decision:\s*`([^`]+)`\s*$",
    text,
    flags=re.MULTILINE,
)

if not m:
    fail(
        "FOCUSED_OVERALL_DECISION_MISSING"
    )

if m.group(1).strip() != \
        expected_overall:
    fail(
        "FOCUSED_OVERALL_DECISION"
    )

record = json.loads(
    RECORD.read_text(
        encoding="utf-8"
    )
)

if record[
    "status"
] != "FOCUSED_SUCR01_C_PASS_RECORDED_WITHOUT_REVIEW_CHAIN_CLOSURE":
    fail(
        "RECORD_STATUS"
    )

focused = record[
    "completed_focused_review"
]

if focused[
    "criterion"
] != "SUCR01-C":
    fail(
        "FOCUSED_CRITERION"
    )

if focused[
    "item_decision"
] != "PASS":
    fail(
        "RECORDED_ITEM_DECISION"
    )

if focused[
    "overall_decision"
] != expected_overall:
    fail(
        "RECORDED_OVERALL_DECISION"
    )

history = record[
    "historical_review_state"
]

if history[
    "SUCR01"
] != "REVISION_REQUIRED":
    fail(
        "HISTORICAL_SUCR01"
    )

for rid in (
    "SUCR02",
    "SUCR03",
    "SUCR04",
    "SUCR05",
    "SUCR06",
    "SUCR07",
    "SUCR08",
):

    if history[rid] != "PASS":
        fail(
            "HISTORICAL_PASS_STATE|"
            + rid
        )

if history[
    "original_overall"
] != "REVISION_REQUIRED":
    fail(
        "HISTORICAL_OVERALL"
    )

if history[
    "historical_review_modified"
] is not False:
    fail(
        "HISTORICAL_REVIEW_MODIFIED"
    )

chain = record[
    "review_chain_state"
]

if chain[
    "focused_sucr01_c_rereview_completed"
] is not True:
    fail(
        "FOCUSED_REREVIEW_COMPLETION"
    )

if chain[
    "focused_sucr01_c_pass_recorded"
] is not True:
    fail(
        "FOCUSED_PASS_RECORD"
    )

if chain[
    "review_chain_closure_assessment_authorized"
] is not False:
    fail(
        "PREMATURE_CLOSURE_AUTHORIZATION"
    )

if chain[
    "review_chain_closure_assessment_performed"
] is not False:
    fail(
        "PREMATURE_CLOSURE_ASSESSMENT"
    )

if chain[
    "review_chain_closed"
] is not False:
    fail(
        "PREMATURE_REVIEW_CHAIN_CLOSURE"
    )

if chain[
    "study_governance_adopted"
] is not False:
    fail(
        "PREMATURE_GOVERNANCE_ADOPTION"
    )

if record[
    "study_state"
][
    "status"
] != "AUTHOR_CANDIDATE":
    fail(
        "STUDY_STATUS"
    )

if record[
    "study_state"
][
    "bounded_technical_outcome"
] != "FURTHER_EVIDENCE_REQUIRED":
    fail(
        "BOUNDED_TECHNICAL_OUTCOME"
    )

for key, value in record[
    "technical_nonclaims"
].items():

    if value is not False:
        fail(
            "UNEXPECTED_TECHNICAL_PERMISSION|"
            + key
        )

for key, value in record[
    "retired_verifier_state"
].items():

    if value != \
            "PERMANENTLY_RETIRED":
        fail(
            "RETIRED_VERIFIER_STATE|"
            + key
        )

if SUMS.is_file():

    lines = [
        line
        for line in SUMS.read_text(
            encoding="utf-8"
        ).splitlines()
        if line.strip()
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
        target = HERE / rel

        if sha(target) != digest:
            fail(
                "CHECKSUM|"
                + rel
            )

print("COMPLETED_FOCUSED_SUCR01_C_EXACT_BINDING=PASS")

print("FOCUSED_SUCR01_C_DECISION=PASS")
print(
    "FOCUSED_OVERALL_DECISION="
    + expected_overall
)

print("ORIGINAL_SUCR01_REMAINS=REVISION_REQUIRED")
print("SUCR02_SUCR08_ORIGINAL_PASS_FINDINGS_PRESERVED=YES")
print("ORIGINAL_OVERALL_REVIEW_REMAINS=REVISION_REQUIRED")

print("FOCUSED_SUCR01_C_REREVIEW_COMPLETED=YES")
print("FOCUSED_SUCR01_C_PASS_RECORDED=YES")

print("REVIEW_CHAIN_CLOSURE_ASSESSMENT_AUTHORIZED=NO")
print("REVIEW_CHAIN_CLOSURE_ASSESSMENT_PERFORMED=NO")
print("REVIEW_CHAIN_CLOSED=NO")

print("STUDY_STATUS=AUTHOR_CANDIDATE")
print("GLOBAL_OUTCOME=FURTHER_EVIDENCE_REQUIRED")
print("STUDY_GOVERNANCE_ADOPTED=NO")

print("POSITIVE_EXISTING_V2_MAPPING_PROVEN=NO")
print("NEGATIVE_EXISTING_V2_MAPPING_IMPOSSIBILITY_PROVEN=NO")
print("WHOLE_V4_ADMISSIBLE_COMPOSITION_EXHAUSTIVENESS_PROVEN=NO")

print("OPERATIONAL_MAPPING_AUTHORIZED=NO")
print("SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO")
print("CURL_JSON_AUTHORIZED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")

print("RETIRED_A02_VERIFIERS_EXECUTED=NO")

print(
    "REPOSITORY_COMPLETED_FOCUSED_SUCR01_C_REREVIEW=PASS"
)
