#!/usr/bin/env python3

import hashlib
import json
import re
import subprocess
from pathlib import Path

REPO = Path("/openbayes/home/semanticverify-fuzz-research")

BASE_REL = (
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2"
)

HANDOFF_REL = (
    BASE_REL
    + "/schema_v2_requirement_to_semantic_unit_"
      "crosswalk_evidence_resolution_study_v1_external_handoff_v1"
)

AUTH_REL = (
    BASE_REL
    + "/schema_v2_requirement_to_semantic_unit_"
      "crosswalk_evidence_resolution_study_v1_"
      "completed_human_review_recording_authorization_v1"
)

COMPLETED_REL = (
    BASE_REL
    + "/schema_v2_requirement_to_semantic_unit_"
      "crosswalk_evidence_resolution_study_v1_"
      "completed_human_review_record_v1"
)

EXPECTED_PARENT = "4b5b9310e618e33fbd05a1667819d1f63be6003d"
EXPECTED_HANDOFF_TREE = "ffa411b05857c7d77db70223f39887104f76afd8"

EXPECTED_A01_SHA = "a12d8b0ab485d314a7b6348a5bab98c6dfa4b4dfd3ef0449e79dfe173c779cc0"
EXPECTED_D0152_SHA = "9b016ab8990b85d7b360b29e3a12a11fae05221d3662bf8c7096a323e574be57"

RETURNED = Path(
    "/openbayes/home/41_CWXR01_CWXR08_manually_reviewer_packet.MANUAL_REVIEW_COPY.v1.md"
)

EXPECTED_RETURNED_SHA = "2b1727b97d97409b36f4cfcd921e1857157afcef43b41998abaf152a67ce5e91"
EXPECTED_RETURNED_SIZE = 7703

PASS_MARKER = (
    "REQUIREMENT_TO_SEMANTIC_UNIT_CROSSWALK_"
    "EVIDENCE_RESOLUTION_STUDY_V1_COMPLETED_"
    "HUMAN_REVIEW_RECORDING_AUTHORIZATION=PASS"
)

def run(*args):
    return subprocess.check_output(
        args,
        cwd=REPO,
        text=True,
    ).strip()

def sha(path):
    return hashlib.sha256(
        Path(path).read_bytes()
    ).hexdigest()

head = run("git", "rev-parse", "HEAD")
parent = run("git", "rev-parse", "HEAD^")

if parent != EXPECTED_PARENT:
    raise SystemExit(
        "STOP|CURRENT_HEAD_IS_NOT_IMMEDIATE_SUCCESSOR_OF_DECISION0152"
    )

if run(
    "git",
    "rev-parse",
    f"HEAD:{HANDOFF_REL}",
) != EXPECTED_HANDOFF_TREE:
    raise SystemExit(
        "STOP|EXTERNAL_HANDOFF_TREE_CHANGED"
    )

status = run(
    "git",
    "status",
    "--porcelain=v1",
    "--untracked-files=all",
)

if status:
    raise SystemExit(
        "STOP|REPOSITORY_NOT_CLEAN"
    )

auth = REPO / AUTH_REL
completed = REPO / COMPLETED_REL

if completed.exists():
    raise SystemExit(
        "STOP|COMPLETED_HUMAN_REVIEW_RECORD_ALREADY_EXISTS"
    )

a01 = (
    auth
    / "01_completed_human_review_recording_authorization.v1.json"
)

a03 = (
    auth
    / "03_completed_human_review_recording_authorization.v1.SHA256SUMS"
)

if sha(a01) != EXPECTED_A01_SHA:
    raise SystemExit(
        "STOP|A01_SHA_MISMATCH"
    )

subprocess.check_call(
    [
        "sha256sum",
        "-c",
        a03.name,
    ],
    cwd=auth,
    stdout=subprocess.DEVNULL,
)

d0152 = (
    REPO
    / "documentation/decisions/"
      "0152-record-external-independent-human-review-"
      "handoff-for-cwxr01-cwxr08.md"
)

if sha(d0152) != EXPECTED_D0152_SHA:
    raise SystemExit(
        "STOP|DECISION0152_SHA_MISMATCH"
    )

if not RETURNED.is_file():
    raise SystemExit(
        "STOP|RETURNED_REVIEW_PACKET_MISSING"
    )

if sha(RETURNED) != EXPECTED_RETURNED_SHA:
    raise SystemExit(
        "STOP|RETURNED_REVIEW_PACKET_SHA_MISMATCH"
    )

if RETURNED.stat().st_size != EXPECTED_RETURNED_SIZE:
    raise SystemExit(
        "STOP|RETURNED_REVIEW_PACKET_SIZE_MISMATCH"
    )

text = RETURNED.read_text(
    encoding="utf-8"
)

expected = {
    "CWXR01": "PASS",
    "CWXR02": "PASS",
    "CWXR03": "PASS",
    "CWXR04": "PASS",
    "CWXR05": "PASS",
    "CWXR06": "PASS",
    "CWXR07": "REVISION_REQUIRED",
    "CWXR08": "PASS",
}

for item, value in expected.items():

    pattern = (
        rf"^{item} decision:"
        rf"\s*?\s*$"
    )

    matches = re.findall(
        pattern,
        text,
        flags=re.MULTILINE,
    )

    if matches != [value]:
        raise SystemExit(
            "STOP|RETURNED_REVIEW_DECISION_MISMATCH|"
            + item
        )

overall = re.findall(
    r"^Overall decision:\s*?\s*$",
    text,
    flags=re.MULTILINE,
)

if overall != ["REVISION_REQUIRED"]:
    raise SystemExit(
        "STOP|OVERALL_REVIEW_DECISION_MISMATCH"
    )

identity = {
    "Reviewer name:":
        "Abdul Raheem Shahzad",

    "Reviewer role:":
        "Spec-Technical-Reviewer-1",

    "Reviewer confirmation/signature:":
        "ARS",

    "Review date:":
        "25 / August / 2026",
}

lines = text.splitlines()

for prefix, expected_value in identity.items():

    matches = [
        line[len(prefix):].strip()
        for line in lines
        if line.startswith(prefix)
    ]

    if matches != [expected_value]:
        raise SystemExit(
            "STOP|REVIEWER_IDENTITY_MISMATCH|"
            + prefix
        )

required_rationale = (
    "cannot independently establish that A02 was executed exactly once "
    "or that no rerun occurred"
)

if required_rationale not in text:
    raise SystemExit(
        "STOP|CWXR07_REVISION_RATIONALE_MISSING"
    )

handoff_verifier = (
    REPO
    / HANDOFF_REL
    / "08_verify_external_CWXR01_CWXR08_handoff.v1.py"
)

safe_output = subprocess.check_output(
    [
        "python3",
        str(handoff_verifier),
    ],
    cwd=REPO,
    text=True,
)

required_marker = (
    "REQUIREMENT_TO_SEMANTIC_UNIT_CROSSWALK_"
    "EVIDENCE_RESOLUTION_STUDY_V1_EXTERNAL_"
    "INDEPENDENT_HUMAN_REVIEW_HANDOFF=PASS"
)

if required_marker not in safe_output.splitlines():
    raise SystemExit(
        "STOP|SAFE_HANDOFF_REVERIFICATION_FAILED"
    )

print(PASS_MARKER)
print("CURRENT_HEAD=" + head)
print("CURRENT_HEAD_PARENT_DECISION0152_BINDING=PASS")
print("EXTERNAL_HANDOFF_TREE_BINDING=PASS")
print("RETURNED_REVIEW_PACKET_BYTE_BINDING=PASS")

print("COMPLETED_HUMAN_REVIEW_OCCURRED=YES")
print("PASS_ITEM_COUNT=7")
print("REVISION_REQUIRED_ITEM_COUNT=1")
print("FAIL_ITEM_COUNT=0")

print("CWXR07=REVISION_REQUIRED")
print("OVERALL_DECISION=REVISION_REQUIRED")

print("REVIEWER_NAME=Abdul Raheem Shahzad")
print("REVIEWER_ROLE=Spec-Technical-Reviewer-1")
print("REVIEWER_CONFIRMATION=ARS")
print("REVIEW_DATE=25 / August / 2026")

print("GOVERNANCE_ADOPTION_AUTHORIZED=NO")
print("CORRECTIVE_ACTION_REQUIRED=YES")
print("CORRECTIVE_SCOPE=CWXR07_ONLY")

print("DECISION_0151_A02_EXECUTED_BY_THIS_VERIFIER=NO")
print("DECISION_0149_A02_EXECUTED_BY_THIS_VERIFIER=NO")
print("DECISION_0147_A02_EXECUTED_BY_THIS_VERIFIER=NO")
print("RETIRED_A02_VERIFIERS_EXECUTED=NO")

print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")

print(
    "VERIFIER_LIFECYCLE="
    "ONE_FINAL_RUN_IMMEDIATELY_BEFORE_COMPLETED_"
    "HUMAN_REVIEW_RECORDING_THEN_PERMANENT_RETIREMENT"
)
