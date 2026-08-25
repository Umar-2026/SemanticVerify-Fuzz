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

AUTH154_REL = (
    BASE_REL
    + "/schema_v2_requirement_to_semantic_unit_"
      "crosswalk_evidence_resolution_study_v1_completed_"
      "human_review_recording_corrective_successor_authorization_v1"
)

AUTH153_REL = (
    BASE_REL
    + "/schema_v2_requirement_to_semantic_unit_"
      "crosswalk_evidence_resolution_study_v1_completed_"
      "human_review_recording_authorization_v1"
)

COMPLETED_REL = (
    BASE_REL
    + "/schema_v2_requirement_to_semantic_unit_"
      "crosswalk_evidence_resolution_study_v1_completed_"
      "human_review_record_v1"
)

EXPECTED_PARENT = "75ffaf3214ffbe4345d7290829c334b4a559ac07"
EXPECTED_HANDOFF_TREE = "ffa411b05857c7d77db70223f39887104f76afd8"

EXPECTED_A01_SHA = "6a2a6f86608740412a2c61ee7850f1e132d2849d82b518188175d2036d31553d"
EXPECTED_D0153_SHA = "717da5bafedf3dd5f6c91e375b5ed66b43fb2d572a0b7ed54cc7288e9b50560f"

DEFECTIVE_A02_SHA = "873bf03323b26cfbaa2a6223b3f0e461d1c38f5edfa701408a88d70b21c18522"

RETURNED = Path("/openbayes/home/41_CWXR01_CWXR08_manually_reviewer_packet.MANUAL_REVIEW_COPY.v1.md")
EXPECTED_RETURNED_SHA = "2b1727b97d97409b36f4cfcd921e1857157afcef43b41998abaf152a67ce5e91"
EXPECTED_RETURNED_SIZE = 7703

HANDOFF_VERIFIER = Path("/openbayes/home/semanticverify-fuzz-research/evidence/annotation_preparation/protocol_specification_schema_successor_v2/schema_v2_requirement_to_semantic_unit_crosswalk_evidence_resolution_study_v1_external_handoff_v1/08_verify_external_CWXR01_CWXR08_handoff.v1.py")
EXPECTED_HANDOFF_VERIFIER_SHA = "c29a6cca9298d0bba6814e830b54c2b5184b9b471ed0a71b46a0663a6eb4b8db"

PASS_MARKER = (
    "REQUIREMENT_TO_SEMANTIC_UNIT_CROSSWALK_"
    "EVIDENCE_RESOLUTION_STUDY_V1_COMPLETED_"
    "HUMAN_REVIEW_RECORDING_CORRECTIVE_SUCCESSOR_AUTHORIZATION=PASS"
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
        "STOP|CURRENT_HEAD_IS_NOT_IMMEDIATE_SUCCESSOR_OF_DECISION0153"
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

auth154 = REPO / AUTH154_REL
auth153 = REPO / AUTH153_REL
completed = REPO / COMPLETED_REL

if completed.exists():
    raise SystemExit(
        "STOP|COMPLETED_HUMAN_REVIEW_RECORD_ALREADY_EXISTS"
    )

a01 = auth154 / "01_corrective_successor_recording_authorization.v1.json"
a03 = auth154 / "03_corrective_successor_recording_authorization.v1.SHA256SUMS"

if sha(a01) != EXPECTED_A01_SHA:
    raise SystemExit(
        "STOP|CORRECTIVE_SUCCESSOR_A01_SHA_MISMATCH"
    )

subprocess.check_call(
    ["sha256sum", "-c", a03.name],
    cwd=auth154,
    stdout=subprocess.DEVNULL,
)

d0153 = (
    REPO
    / "documentation/decisions/"
      "0153-authorize-recording-completed-cwxr01-cwxr08-"
      "human-review-with-revision-required-outcome.md"
)

if sha(d0153) != EXPECTED_D0153_SHA:
    raise SystemExit(
        "STOP|DECISION0153_SHA_MISMATCH"
    )

defective_a02 = (
    auth153
    / "02_verify_completed_human_review_recording_authorization.v1.py"
)

if sha(defective_a02) != DEFECTIVE_A02_SHA:
    raise SystemExit(
        "STOP|DEFECTIVE_DECISION0153_A02_SHA_MISMATCH"
    )

defective_src = defective_a02.read_text(encoding="utf-8")

if "`?([A-Z_]+)`?" in defective_src:
    raise SystemExit(
        "STOP|DECISION0153_A02_EXPECTED_DEFECT_NOT_PRESENT"
    )

if r'^Overall decision:\s*?\s*$' not in defective_src:
    raise SystemExit(
        "STOP|DECISION0153_A02_CORRUPTED_REGEX_NOT_FOUND"
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

text = RETURNED.read_text(encoding="utf-8")

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
    pattern = rf"^{item} decision:\s*`?([A-Z_]+)`?\s*$"

    found = re.findall(
        pattern,
        text,
        flags=re.MULTILINE,
    )

    if found != [value]:
        raise SystemExit(
            "STOP|RETURNED_REVIEW_DECISION_MISMATCH|"
            + item
        )

overall = re.findall(
    r"^Overall decision:\s*`?([A-Z_]+)`?\s*$",
    text,
    flags=re.MULTILINE,
)

if overall != ["REVISION_REQUIRED"]:
    raise SystemExit(
        "STOP|OVERALL_REVIEW_DECISION_MISMATCH"
    )

identity = {
    "Reviewer name:": "Abdul Raheem Shahzad",
    "Reviewer role:": "Spec-Technical-Reviewer-1",
    "Reviewer confirmation/signature:": "ARS",
    "Review date:": "25 / August / 2026",
}

lines = text.splitlines()

for prefix, expected_value in identity.items():
    values = [
        line[len(prefix):].strip()
        for line in lines
        if line.startswith(prefix)
    ]

    if values != [expected_value]:
        raise SystemExit(
            "STOP|REVIEWER_IDENTITY_MISMATCH|"
            + prefix
        )

if sha(HANDOFF_VERIFIER) != EXPECTED_HANDOFF_VERIFIER_SHA:
    raise SystemExit(
        "STOP|HANDOFF_VERIFIER_SHA_MISMATCH"
    )

safe_output = subprocess.check_output(
    ["python3", str(HANDOFF_VERIFIER)],
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
print("CURRENT_HEAD_PARENT_DECISION0153_BINDING=PASS")
print("EXTERNAL_HANDOFF_TREE_BINDING=PASS")

print("DECISION_0153_A02_DEFECT_CONFIRMED=YES")
print("DECISION_0153_A02_EXECUTED_BY_THIS_VERIFIER=NO")
print("DECISION_0153_A02_SUPERSEDED=YES")

print("RETURNED_REVIEW_PACKET_BYTE_BINDING=PASS")
print("COMPLETED_HUMAN_REVIEW_OCCURRED=YES")

print("PASS_ITEM_COUNT=7")
print("REVISION_REQUIRED_ITEM_COUNT=1")
print("FAIL_ITEM_COUNT=0")

print("CWXR07=REVISION_REQUIRED")
print("OVERALL_DECISION=REVISION_REQUIRED")

print("GOVERNANCE_ADOPTION_AUTHORIZED=NO")
print("CORRECTIVE_ACTION_REQUIRED_AFTER_RECORDING=YES")
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
