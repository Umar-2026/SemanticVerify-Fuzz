#!/usr/bin/env python3

import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent

PKG = HERE / "review_package_v1_exact"
AUTH = HERE / "decision0114_authorization_exact"

PACKET = (
    PKG
    / "20_SUCR01_SUCR08_reviewer_packet.MANUAL_REVIEW_COPY.v1.md"
)

PKG_MANIFEST = (
    PKG
    / "21_review_package_manifest.v1.json"
)

PKG_SAFE = (
    PKG
    / "22_verify_semantic_unit_carrier_study_review_package.v1.py"
)

PKG_SUMS = (
    PKG
    / "23_review_package.v1.SHA256SUMS"
)

DEC0113 = (
    HERE
    / "01_decision0113_review_package_checkpoint.EXACT_COPY.v1.md"
)

DEC0114 = (
    HERE
    / "02_decision0114_external_handoff_authorization.EXACT_COPY.v1.md"
)

A02_OUT = (
    HERE
    / "03_decision0114_a02_final_output.EXACT_COPY.v1.txt"
)

CONSUMPTION = (
    HERE
    / "04_decision0114_a02_consumption_record.v1.json"
)

SOURCE_BIND = (
    HERE
    / "05_source_binding_manifest.v1.json"
)

MANIFEST = (
    HERE
    / "06_external_handoff_manifest.v1.json"
)

SUMS = (
    HERE
    / "08_external_review_handoff.v1.SHA256SUMS"
)

EXPECTED = {
    PACKET:
        "38f1021657d06716ac28709ec98be6d9d992a4c451b41569b0f60c651f68a8db",

    PKG_MANIFEST:
        "c954de9c57039be17f7b7d4f6c15d023ff39d5d658d3b6194889f95189ab65aa",

    PKG_SAFE:
        "a1ab5a2ba3e2dba2f48a0d48a5f7f0ae8ed97b7ddffbd824236ac6371efc33e2",

    PKG_SUMS:
        "576051b93ab71a8b5500b91acb42677b9a72133727ba2e5608145b2a7e9dd78a",

    DEC0113:
        "93ed7e5538a717bc9eae242b9a215eba99d7e144e459672e474eb1dee8104fd2",

    DEC0114:
        "5b3d960a839b874017247943cd77f662dd4ee252f48bd34e268df862aa8d1c25",

    AUTH / "01_external_independent_human_review_handoff_authorization.v1.json":
        "b5fe549a6607f7d70f1fa194e7d9049a8af2d5cbb95d7a447ab8a5fa83690bfa",

    AUTH / "02_verify_external_handoff_authoring_authorization.v1.py":
        "3139be91d0a6618e928c803ccc81b330a440e4c5ee63a90f95f0cccf6a751fd4",

    AUTH / "03_external_handoff_authorization.v1.SHA256SUMS":
        "bcff1b20ec210aa03ca79590f62169b8f1098b55028010eebe7c6538bcad77c0",
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

if len([
    p
    for p in PKG.rglob("*")
    if p.is_file()
]) != 23:
    fail(
        "REVIEW_PACKAGE_FILE_COUNT"
    )

if len([
    p
    for p in AUTH.rglob("*")
    if p.is_file()
]) != 3:
    fail(
        "AUTH_FILE_COUNT"
    )

text = PACKET.read_text(
    encoding="utf-8"
)

if (
    "Package state: `BLANK — AWAITING INDEPENDENT HUMAN REVIEW`"
    not in text
):
    fail(
        "PACKET_NOT_BLANK"
    )

for rid in (
    "SUCR01",
    "SUCR02",
    "SUCR03",
    "SUCR04",
    "SUCR05",
    "SUCR06",
    "SUCR07",
    "SUCR08",
):

    if text.count(
        f"## {rid} —"
    ) != 1:
        fail(
            "REVIEW_ITEM|"
            + rid
        )

if re.search(
    r"^Decision:\s*`?(PASS|REVISION_REQUIRED|FAIL)`?\s*$",
    text,
    flags=re.MULTILINE,
):
    fail(
        "PREPOPULATED_ITEM_DECISION"
    )

if re.search(
    r"^Overall decision:\s*`?(APPROVE_|REVISION_REQUIRED|FAIL)",
    text,
    flags=re.MULTILINE,
):
    fail(
        "PREPOPULATED_OVERALL_DECISION"
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
        "A02_FINAL_RESULT"
    )

if cons[
    "verifier_state_after_run"
] != "PERMANENTLY_RETIRED":
    fail(
        "A02_STATE"
    )

if cons[
    "rerun_authorized"
] is not False:
    fail(
        "A02_RERUN_AUTHORIZED"
    )

if cons[
    "must_never_be_rerun"
] is not True:
    fail(
        "A02_RETIREMENT_GUARD"
    )

if sha(A02_OUT) != \
        cons["final_output_sha256"]:
    fail(
        "A02_OUTPUT_SHA"
    )

if A02_OUT.stat().st_size != \
        cons["final_output_size_bytes"]:
    fail(
        "A02_OUTPUT_SIZE"
    )

if (
    "EXTERNAL_HANDOFF_AUTHORING_AUTHORIZATION=PASS"
    not in A02_OUT.read_text(
        encoding="utf-8"
    )
):
    fail(
        "A02_PASS_MARKER"
    )

source = json.loads(
    SOURCE_BIND.read_text(
        encoding="utf-8"
    )
)

if source[
    "source_checkpoint"
][
    "review_package_v1_git_tree"
] != "e3d3c93a723b9d4c085a81ec0d0be11df852601a":
    fail(
        "BOUND_REVIEW_PACKAGE_TREE"
    )

manifest = json.loads(
    MANIFEST.read_text(
        encoding="utf-8"
    )
)

if manifest[
    "state"
] != "BLANK_READY_FOR_EXTERNAL_INDEPENDENT_HUMAN_REVIEW":
    fail(
        "HANDOFF_STATE"
    )

if manifest[
    "required_reviewer_role"
] != "Spec-Technical-Reviewer-1":
    fail(
        "REVIEWER_ROLE"
    )

if manifest[
    "review_items"
] != [
    "SUCR01",
    "SUCR02",
    "SUCR03",
    "SUCR04",
    "SUCR05",
    "SUCR06",
    "SUCR07",
    "SUCR08",
]:
    fail(
        "REVIEW_ITEMS"
    )

human = manifest[
    "human_review_state"
]

for key, value in human.items():

    if value is not False:
        fail(
            "HUMAN_REVIEW_PREPOPULATION|"
            + key
        )

for key, value in manifest[
    "technical_nonclaims"
].items():

    if value is not False:
        fail(
            "UNEXPECTED_TECHNICAL_PERMISSION|"
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

    if len(lines) != 33:
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

print("INTERNAL_EXTERNAL_REVIEW_HANDOFF_SOURCE_BINDINGS=PASS")
print("REVIEW_PACKAGE_V1_EXACT_COPY=PASS")
print("DECISION_0114_AUTHORIZATION_EXACT_COPY=PASS")

print("REVIEW_PACKAGE_STATE=BLANK_READY_FOR_EXTERNAL_INDEPENDENT_HUMAN_REVIEW")
print("REVIEW_ITEMS=SUCR01,SUCR02,SUCR03,SUCR04,SUCR05,SUCR06,SUCR07,SUCR08")
print("REQUIRED_REVIEWER_ROLE=Spec-Technical-Reviewer-1")

print("ITEM_DECISIONS_PREPOPULATED=NO")
print("REVIEWER_NOTES_PREPOPULATED=NO")
print("OVERALL_DECISION_PREPOPULATED=NO")
print("REVIEWER_IDENTITY_PREPOPULATED=NO")
print("HUMAN_REVIEW_DECISION_EXISTS=NO")

print("STUDY_STATUS=AUTHOR_CANDIDATE")
print("GLOBAL_OUTCOME=FURTHER_EVIDENCE_REQUIRED")
print("STUDY_GOVERNANCE_ADOPTED=NO")

print("DECISION_0114_A02_STATE=PERMANENTLY_RETIRED")
print("DECISION_0114_A02_EXECUTED_BY_SAFE_VERIFIER=NO")
print("DECISION_0112_A02_EXECUTED_BY_SAFE_VERIFIER=NO")
print("DECISION_0110_A02_EXECUTED_BY_SAFE_VERIFIER=NO")

print("OPERATIONAL_MAPPING_AUTHORIZED=NO")
print("SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO")
print("CURL_JSON_AUTHORIZED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")

print("EXTERNAL_REVIEW_HANDOFF_V1=PASS")
