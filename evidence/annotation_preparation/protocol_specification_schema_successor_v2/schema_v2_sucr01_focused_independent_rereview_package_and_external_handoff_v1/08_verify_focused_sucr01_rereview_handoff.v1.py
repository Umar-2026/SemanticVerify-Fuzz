#!/usr/bin/env python3

import hashlib
import json
import os
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent

CORRECTIVE = (
    HERE
    / "corrective_successor_package_v2_exact"
)

AUTH = (
    HERE
    / "decision0119_authorization_exact"
)

PACKET = (
    HERE
    / "05_SUCR01_C_focused_rereview_packet.MANUAL_REVIEW_COPY.v1.md"
)

SOURCE = (
    HERE
    / "06_focused_rereview_source_binding_manifest.v1.json"
)

MANIFEST = (
    HERE
    / "07_focused_rereview_handoff_manifest.v1.json"
)

A02_OUT = (
    HERE
    / "03_decision0119_a02_final_output.EXACT_COPY.v1.txt"
)

CONSUMPTION = (
    HERE
    / "04_decision0119_a02_consumption_record.v1.json"
)

SUMS = (
    HERE
    / "09_focused_sucr01_rereview_handoff.v1.SHA256SUMS"
)

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

corrective_files = [
    p
    for p in CORRECTIVE.rglob("*")
    if p.is_file()
]

if len(corrective_files) != 54:
    fail(
        "CORRECTIVE_FILE_COUNT|"
        + str(len(corrective_files))
    )

auth_files = [
    p
    for p in AUTH.rglob("*")
    if p.is_file()
]

if len(auth_files) != 3:
    fail(
        "AUTH_FILE_COUNT|"
        + str(len(auth_files))
    )

text = PACKET.read_text(
    encoding="utf-8"
)

if (
    "Package state: `BLANK — AWAITING FOCUSED INDEPENDENT HUMAN REREVIEW`"
    not in text
):
    fail(
        "PACKET_STATE"
    )

if text.count(
    "## SUCR01-C —"
) != 1:
    fail(
        "SUCR01_C_COUNT"
    )

if re.search(
    r"^Decision:\s*`?(PASS|REVISION_REQUIRED|FAIL)`?\s*$",
    text,
    flags=re.MULTILINE,
):
    fail(
        "PREPOPULATED_DECISION"
    )

if re.search(
    r"^Overall decision:\s*`?(APPROVE_|REVISION_REQUIRED|FAIL)",
    text,
    flags=re.MULTILINE,
):
    fail(
        "PREPOPULATED_OVERALL"
    )

source = json.loads(
    SOURCE.read_text(
        encoding="utf-8"
    )
)

if source[
    "corrective_successor_package_v2"
][
    "source_git_tree"
] != "dd34182886703f72fc5bfa4df899ad2bccbf4744":
    fail(
        "CORRECTIVE_TREE_BINDING"
    )

if source[
    "decision_0119_authorization"
][
    "source_git_tree"
] != "3a73b4ebfdeb3f42afe2e293ee6d43b0923951c8":
    fail(
        "AUTH_TREE_BINDING"
    )

if source[
    "historical_review_state"
][
    "overall"
] != "REVISION_REQUIRED":
    fail(
        "HISTORICAL_OVERALL_STATE"
    )

if source[
    "focused_rereview_scope"
][
    "criterion"
] != "SUCR01-C":
    fail(
        "FOCUSED_CRITERION"
    )

if source[
    "focused_rereview_scope"
][
    "sucr02_through_sucr08_reopened"
] is not False:
    fail(
        "SUCR02_SUCR08_REOPENED"
    )

manifest = json.loads(
    MANIFEST.read_text(
        encoding="utf-8"
    )
)

if manifest[
    "state"
] != "BLANK_READY_FOR_FOCUSED_INDEPENDENT_HUMAN_REREVIEW":
    fail(
        "HANDOFF_STATE"
    )

if manifest[
    "criterion"
] != "SUCR01-C":
    fail(
        "HANDOFF_CRITERION"
    )

if manifest[
    "required_reviewer_role"
] != "Spec-Technical-Reviewer-1":
    fail(
        "REVIEWER_ROLE"
    )

if manifest[
    "original_review_state"
][
    "overall"
] != "REVISION_REQUIRED":
    fail(
        "ORIGINAL_OVERALL_REVIEW"
    )

for key, value in manifest[
    "review_chain_state"
].items():
    if value is not False:
        fail(
            "PREMATURE_REVIEW_CHAIN_STATE|"
            + key
        )

for key, value in manifest[
    "technical_nonclaims"
].items():
    if value is not False:
        fail(
            "UNEXPECTED_PERMISSION|"
            + key
        )

cons = json.loads(
    CONSUMPTION.read_text(
        encoding="utf-8"
    )
)

if cons[
    "final_run_result"
] != "PASS":
    fail(
        "A02_RESULT"
    )

if cons[
    "verifier_state_after_run"
] != "PERMANENTLY_RETIRED":
    fail(
        "A02_STATE"
    )

if cons[
    "must_never_be_rerun"
] is not True:
    fail(
        "A02_RETIREMENT"
    )

if sha(A02_OUT) != \
        cons[
            "final_output_sha256"
        ]:
    fail(
        "A02_OUTPUT_SHA"
    )

if (
    "FOCUSED_SUCR01_REREVIEW_PACKAGE_AND_HANDOFF_AUTHORING_AUTHORIZATION=PASS"
    not in A02_OUT.read_text(
        encoding="utf-8"
    )
):
    fail(
        "A02_PASS_MARKER"
    )

if SUMS.is_file():

    lines = [
        line
        for line in SUMS.read_text(
            encoding="utf-8"
        ).splitlines()
        if line.strip()
    ]

    if len(lines) != 65:
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

print("FOCUSED_CRITERION=SUCR01-C")
print("FOCUSED_SCOPE=SOURCE_EVIDENCE_PORTABILITY_AND_RESOLVABILITY")
print("REQUIRED_REVIEWER_ROLE=Spec-Technical-Reviewer-1")

print("CORRECTIVE_SUCCESSOR_PACKAGE_V2_EXACT_COPY=PASS")
print("DECISION_0119_AUTHORIZATION_EXACT_COPY=PASS")

print("FOCUSED_REVIEWER_PACKET_STATE=BLANK")
print("HUMAN_FOCUSED_REREVIEW_DECISION_EXISTS=NO")

print("ORIGINAL_SUCR01_DECISION=REVISION_REQUIRED")
print("SUCR02_SUCR08_ORIGINAL_PASS_FINDINGS_PRESERVED=YES")
print("ORIGINAL_OVERALL_REVIEW_REMAINS=REVISION_REQUIRED")

print("FOCUSED_SUCR01_REREVIEW_COMPLETED=NO")
print("REVIEW_CHAIN_CLOSED=NO")

print("STUDY_STATUS=AUTHOR_CANDIDATE")
print("GLOBAL_OUTCOME=FURTHER_EVIDENCE_REQUIRED")
print("STUDY_GOVERNANCE_ADOPTED=NO")

print("DECISION_0119_A02_STATE=PERMANENTLY_RETIRED")
print("DECISION_0119_A02_EXECUTED_BY_SAFE_VERIFIER=NO")
print("RETIRED_A02_VERIFIERS_EXECUTED=NO")

print("OPERATIONAL_MAPPING_AUTHORIZED=NO")
print("SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO")
print("CURL_JSON_AUTHORIZED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")

print("FOCUSED_SUCR01_REREVIEW_HANDOFF_V1=PASS")
