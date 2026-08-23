#!/usr/bin/env python3

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(
    "/openbayes/home/semanticverify-fuzz-research"
)

HERE = Path(__file__).resolve().parent

BASE = (
    REPO
    / "evidence/annotation_preparation/protocol_specification_schema_successor_v2"
)

SUCCESSOR = (
    BASE
    / "schema_v2_semantic_role_relation_formalization_v1_corrective_successor_package_v2"
)

COMP = (
    BASE
    / "schema_v2_semantic_role_relation_formalization_v1_corrective_successor_package_v2_recovery_completion_v1"
)

HANDOFF = (
    BASE
    / "schema_v2_semantic_role_relation_formalization_v1_corrective_successor_package_v2_focused_rereview_handoff_v1"
)

AUTH = (
    HERE
    / "01_focused_rereview_handoff_authorization.v1.json"
)

SAFE = (
    SUCCESSOR
    / "05_verify_corrective_successor_package_v2.py"
)

BLANK = (
    SUCCESSOR
    / "04_focused_rereview_packet.BLANK.v2.md"
)

MANIFEST = (
    SUCCESSOR
    / "01_corrective_successor_package_v2_manifest.json"
)

C02 = (
    COMP
    / "02_recovery_completion_record.v1.json"
)

C04 = (
    COMP
    / "04_verify_recovery_completion_and_corrective_successor_package_v2_author_checkpoint.v1.py"
)

D95 = (
    BASE
    / "schema_v2_semantic_role_relation_formalization_v1_corrective_successor_package_v2_authorization"
    / "02_verify_corrective_successor_package_v2_authorization.v1.py"
)

D96 = (
    BASE
    / "schema_v2_semantic_role_relation_formalization_v1_corrective_successor_package_v2_recovery_authorization"
    / "03_verify_post_final_authorization_run_recovery_authorization.v1.py"
)

EXPECTED = {
    SAFE:
        "2c053a69dd183faa896364a61e5a2c337876c59735313c421e2acb63cd13a63a",

    BLANK:
        "60185126f93d5a113722545108c4b798563b6088f9b92945ccb7cd16840db75e",

    MANIFEST:
        "f1773106a7b97eda909fc7baccdc311942a77e484d7a7243cb72003842bfb05e",

    C02:
        "3885824812d292d29849c4212f11b7918a93969bca6ce7440cabe215629752e6",

    C04:
        "4b27a4016abfa20fac6f7df54c3ebececdc26c1b6d4d29abcf8a071c36b6cf9a",

    D95:
        "4c4a1feca0496055035e57389f0c581542e97ac72a46d10137f657208743093b",

    D96:
        "180c58974f894788884d75f9e0ae8964e4d2a9df5ff418e52b1856c282a920e4",
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
    actual = sha(path)

    if actual != expected:
        fail(
            "SHA|"
            + str(path)
            + "|ACTUAL="
            + actual
        )

if HANDOFF.exists():
    fail(
        "HANDOFF_ALREADY_EXISTS"
    )

# ------------------------------------------------------------
# Execute only current SAFE author-checkpoint verifiers.
# ------------------------------------------------------------

for verifier in (
    SAFE,
    C04,
):
    proc = subprocess.run(
        [
            sys.executable,
            str(verifier),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )

    if proc.returncode != 0:
        fail(
            "SAFE_VERIFIER|"
            + verifier.name
            + "|RC="
            + str(proc.returncode)
        )

# ------------------------------------------------------------
# Review state.
# ------------------------------------------------------------

manifest = json.loads(
    MANIFEST.read_text(
        encoding="utf-8"
    )
)

completion = json.loads(
    C02.read_text(
        encoding="utf-8"
    )
)

if manifest[
    "status"
] != "AUTHOR_CANDIDATE_AWAITING_FOCUSED_INDEPENDENT_HUMAN_REREVIEW":
    fail(
        "PACKAGE_STATUS"
    )

if manifest[
    "formalization_v1_approved"
] is not False:
    fail(
        "FORMALIZATION_APPROVAL"
    )

state = manifest[
    "human_review_state"
]

if state[
    "focused_rereview_packet"
] != "BLANK":
    fail(
        "FOCUSED_PACKET_STATE"
    )

if state[
    "focused_human_decision_exists"
] is not False:
    fail(
        "FOCUSED_DECISION_EXISTS"
    )

if state[
    "focused_human_approval_exists"
] is not False:
    fail(
        "FOCUSED_APPROVAL_EXISTS"
    )

review = completion[
    "review_state"
]

if review[
    "original_overall_human_review"
] != "REVISION_REQUIRED":
    fail(
        "ORIGINAL_OVERALL_REVIEW"
    )

if review[
    "carried_forward_pass_items"
] != [
    "SRR01",
    "SRR03",
    "SRR06",
    "SRR07",
]:
    fail(
        "CARRIED_FORWARD_PASS_ITEMS"
    )

if review[
    "focused_items_awaiting_rereview"
] != [
    "SRR02-C",
    "SRR04-C",
    "SRR05-C",
    "SRR08-C",
]:
    fail(
        "FOCUSED_ITEM_SET"
    )

# ------------------------------------------------------------
# Blank reviewer packet.
# ------------------------------------------------------------

text = BLANK.read_text(
    encoding="utf-8"
)

for rid in (
    "SRR02-C",
    "SRR04-C",
    "SRR05-C",
    "SRR08-C",
):
    section = re.search(
        rf"^## {re.escape(rid)}\b"
        rf"(?P<body>.*?)"
        rf"(?=^## SRR\d{{2}}-C\b|^# Overall focused decision\b)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )

    if not section:
        fail(
            "MISSING_ITEM|" + rid
        )

    if not re.search(
        r"^Decision \(PASS / REVISION_REQUIRED / FAIL\):[ \t]*$",
        section.group("body"),
        flags=re.MULTILINE,
    ):
        fail(
            "ITEM_DECISION_NOT_BLANK|" + rid
        )

if not re.search(
    r"^Overall decision "
    r"\(APPROVE_CORRECTIVE_SUCCESSOR_PACKAGE_V2 / "
    r"REVISION_REQUIRED / FAIL\):[ \t]*$",
    text,
    flags=re.MULTILINE,
):
    fail(
        "OVERALL_DECISION_NOT_BLANK"
    )

for prefix in (
    "Human reviewer name:",
    "Human reviewer signature / recorded confirmation:",
    "Human reviewer date:",
):
    vals = [
        line[len(prefix):].strip()
        for line in text.splitlines()
        if line.startswith(prefix)
    ]

    if vals != [""]:
        fail(
            "REVIEWER_FIELD_NOT_BLANK|"
            + prefix
        )

# ------------------------------------------------------------
# Authorization contract.
# ------------------------------------------------------------

auth = json.loads(
    AUTH.read_text(
        encoding="utf-8"
    )
)

if auth[
    "status"
] != "AUTHORIZED_FOR_EXTERNAL_FOCUSED_REREVIEW_HANDOFF_AUTHORING_ONLY":
    fail(
        "AUTH_STATUS"
    )

if auth[
    "source_review_state"
][
    "focused_rereview_items"
] != [
    "SRR02-C",
    "SRR04-C",
    "SRR05-C",
    "SRR08-C",
]:
    fail(
        "AUTH_FOCUSED_ITEMS"
    )

if auth[
    "source_review_state"
][
    "carried_forward_pass_items"
] != [
    "SRR01",
    "SRR03",
    "SRR06",
    "SRR07",
]:
    fail(
        "AUTH_CARRIED_FORWARD"
    )

if auth[
    "focused_rereview_contract"
][
    "reviewer_role"
] != "Spec-Technical-Reviewer-1":
    fail(
        "AUTH_REVIEWER_ROLE"
    )

for key, value in auth[
    "immutability"
].items():
    if value is not True:
        fail(
            "IMMUTABILITY|" + key
        )

for key, value in auth[
    "explicit_non_authorizations"
].items():
    if value is not False:
        fail(
            "NONAUTH|" + key
        )

print("CORRECTIVE_SUCCESSOR_PACKAGE_V2_AUTHOR_CHECKPOINT=PASS")
print("RECOVERY_COMPLETION_AUTHOR_CHECKPOINT=PASS")

print("DECISION_0095_AUTHORIZATION_VERIFIER_EXECUTED=NO")
print("DECISION_0096_RECOVERY_AUTHORIZATION_VERIFIER_EXECUTED=NO")
print("BOTH_RETIRED_GOVERNANCE_VERIFIERS_REMAIN_RETIRED=YES")

print("ORIGINAL_OVERALL_HUMAN_REVIEW=REVISION_REQUIRED")
print("CARRIED_FORWARD_PASS_ITEMS=SRR01,SRR03,SRR06,SRR07")
print("FOCUSED_REREVIEW_ITEMS=SRR02-C,SRR04-C,SRR05-C,SRR08-C")

print("FOCUSED_REREVIEW_PACKET=BLANK")
print("FOCUSED_HUMAN_DECISION_EXISTS=NO")
print("FOCUSED_HUMAN_APPROVAL_EXISTS=NO")
print("FOCUSED_REVIEWER_IDENTITY_PREPOPULATED=NO")
print("FORMALIZATION_V1_APPROVED=NO")

print("OPERATIONAL_POSITIVE_MAPPING_AUTHORIZED=NO")
print("SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO")
print("CURL_JSON_AUTHORIZED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")

print("DECISION_0098_FOCUSED_REREVIEW_HANDOFF_AUTHORIZATION=PASS")
print("IMPORTANT=THIS_VERIFIER_IS_PRE_HANDOFF_AUTHORING_ONLY")
