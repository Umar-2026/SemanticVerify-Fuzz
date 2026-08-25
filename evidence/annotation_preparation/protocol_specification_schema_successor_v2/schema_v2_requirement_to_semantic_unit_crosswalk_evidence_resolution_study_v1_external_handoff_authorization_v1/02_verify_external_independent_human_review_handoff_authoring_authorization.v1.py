#!/usr/bin/env python3

import hashlib
import json
import subprocess
from pathlib import Path

REPO = Path("/openbayes/home/semanticverify-fuzz-research")

BASE_REL = (
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2"
)

PACKAGE_REL = (
    BASE_REL
    + "/schema_v2_requirement_to_semantic_unit_"
      "crosswalk_evidence_resolution_study_v1_review_package_v1"
)

AUTH_REL = (
    BASE_REL
    + "/schema_v2_requirement_to_semantic_unit_"
      "crosswalk_evidence_resolution_study_v1_"
      "external_handoff_authorization_v1"
)

HANDOFF_REL = (
    BASE_REL
    + "/schema_v2_requirement_to_semantic_unit_"
      "crosswalk_evidence_resolution_study_v1_external_handoff_v1"
)

EXPECTED_PARENT = "2218a21de85bcb9db259732c2cbb63b84bfa7438"
EXPECTED_PACKAGE_TREE = "0da42326cac4898131a01a8528dd21b3d530ef13"

EXPECTED_A01_SHA = "67193b6c0e9652425808318a8dad2c4af4ac7acbf595c8c7478986fe10012ac7"
EXPECTED_D0150_SHA = "2dbdc6c5cb8fbe0887fce73c65274ff913eab75f118fda3d88a7e817cdeae898"

EXPECTED_PACKAGE_MANIFEST_SHA = "f835275cd80fd52a8cd926cf410e635a5de86a968becce105a3719a8e77a6f2a"
EXPECTED_BLANK_PACKET_SHA = "3e777294a87314a54658a0ce4156ab1324d7bb314529c3907ee47119e2234fdd"
EXPECTED_PACKAGE_VERIFIER_SHA = "8cc5e7e29354fb9b41edeb4d0c7dadab4edf1f01aed6ea20580574a64bdf0402"
EXPECTED_PACKAGE_SUMS_SHA = "de8738227ea1b66c596f414df04ade6309e3b11d936d2f9a00ee6fd7de70f15d"

EXTERNAL_ZIP = Path("/openbayes/home/41_CWXR01_CWXR08_independent_human_review_handoff.v1.zip")
EXTERNAL_EDITABLE_PACKET = Path("/openbayes/home/41_CWXR01_CWXR08_reviewer_packet.MANUAL_REVIEW_COPY.v1.md")

PASS_MARKER = (
    "REQUIREMENT_TO_SEMANTIC_UNIT_CROSSWALK_"
    "EVIDENCE_RESOLUTION_STUDY_V1_EXTERNAL_"
    "INDEPENDENT_HUMAN_REVIEW_HANDOFF_"
    "AUTHORING_AUTHORIZATION=PASS"
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
        "STOP|CURRENT_HEAD_IS_NOT_IMMEDIATE_SUCCESSOR_OF_DECISION0150"
    )

if run(
    "git",
    "rev-parse",
    f"HEAD:{PACKAGE_REL}",
) != EXPECTED_PACKAGE_TREE:
    raise SystemExit(
        "STOP|REVIEW_PACKAGE_TREE_CHANGED"
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

package = REPO / PACKAGE_REL
auth = REPO / AUTH_REL
handoff = REPO / HANDOFF_REL

if handoff.exists():
    raise SystemExit(
        "STOP|EXTERNAL_HANDOFF_REPOSITORY_DIR_ALREADY_EXISTS"
    )

if EXTERNAL_ZIP.exists():
    raise SystemExit(
        "STOP|EXTERNAL_HANDOFF_ZIP_ALREADY_EXISTS"
    )

if EXTERNAL_EDITABLE_PACKET.exists():
    raise SystemExit(
        "STOP|EXTERNAL_EDITABLE_PACKET_ALREADY_EXISTS"
    )

a01 = auth / "01_external_independent_human_review_handoff_authorization.v1.json"
a03 = auth / "03_external_independent_human_review_handoff_authorization.v1.SHA256SUMS"

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

d0150 = (
    REPO
    / "documentation/decisions/"
      "0150-record-independent-human-review-package-for-"
      "requirement-to-semantic-unit-crosswalk-evidence-resolution-"
      "study-v1.md"
)

if sha(d0150) != EXPECTED_D0150_SHA:
    raise SystemExit(
        "STOP|DECISION0150_SHA_MISMATCH"
    )

checks = {
    "01_review_package_manifest.v1.json":
        EXPECTED_PACKAGE_MANIFEST_SHA,

    "03_CWXR01_CWXR08_reviewer_packet.INITIAL_BLANK.v1.md":
        EXPECTED_BLANK_PACKET_SHA,

    "10_verify_independent_human_review_package.v1.py":
        EXPECTED_PACKAGE_VERIFIER_SHA,

    "11_review_package_v1.SHA256SUMS":
        EXPECTED_PACKAGE_SUMS_SHA,
}

for name, expected in checks.items():
    if sha(package / name) != expected:
        raise SystemExit(
            "STOP|REVIEW_PACKAGE_ARTIFACT_SHA_MISMATCH|" + name
        )

safe_verifier = (
    package /
    "10_verify_independent_human_review_package.v1.py"
)

safe_output = subprocess.check_output(
    ["python3", str(safe_verifier)],
    cwd=REPO,
    text=True,
)

required = [
    (
        "REQUIREMENT_TO_SEMANTIC_UNIT_CROSSWALK_"
        "EVIDENCE_RESOLUTION_STUDY_V1_INDEPENDENT_"
        "HUMAN_REVIEW_PACKAGE=PASS"
    ),
    "PACKAGE_STATUS=AUTHOR_CANDIDATE_AWAITING_INDEPENDENT_HUMAN_REVIEW",
    "BLANK_REVIEWER_PACKET=PASS",
    "INDEPENDENT_HUMAN_REVIEW_COMPLETED=NO",
    "REVIEWER_IDENTITY_RECORDED=NO",
    "REVIEWER_DECISIONS_RECORDED=NO",
    "EXTERNAL_HANDOFF_AUTHORIZED=NO",
    "STUDY_GOVERNANCE_ADOPTED=NO",
    "DECISION_0149_A02_STATE=PERMANENTLY_RETIRED",
]

lines = safe_output.splitlines()

for marker in required:
    if marker not in lines:
        raise SystemExit(
            "STOP|SAFE_REVIEW_PACKAGE_REQUIRED_MARKER_MISSING|"
            + marker
        )

blank = (
    package /
    "03_CWXR01_CWXR08_reviewer_packet.INITIAL_BLANK.v1.md"
)

if sha(blank) != EXPECTED_BLANK_PACKET_SHA:
    raise SystemExit(
        "STOP|REPOSITORY_BLANK_PACKET_CHANGED"
    )

print(PASS_MARKER)
print("CURRENT_HEAD=" + head)
print("CURRENT_HEAD_PARENT_DECISION0150_BINDING=PASS")
print("REVIEW_PACKAGE_TREE_BINDING=PASS")
print("BLANK_REVIEWER_PACKET_BYTE_BINDING=PASS")
print("REVIEW_ITEM_COUNT=8")
print("INDEPENDENT_HUMAN_REVIEW_COMPLETED=NO")
print("REVIEWER_IDENTITY_RECORDED=NO")
print("REVIEWER_DECISIONS_RECORDED=NO")
print("STUDY_GOVERNANCE_ADOPTED=NO")
print("DECISION_0149_A02_STATE=PERMANENTLY_RETIRED")
print("DECISION_0149_A02_EXECUTED_BY_THIS_VERIFIER=NO")
print("DECISION_0147_A02_EXECUTED_BY_THIS_VERIFIER=NO")
print("RETIRED_A02_VERIFIERS_EXECUTED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
print(
    "VERIFIER_LIFECYCLE="
    "ONE_FINAL_RUN_IMMEDIATELY_BEFORE_EXTERNAL_"
    "INDEPENDENT_HUMAN_REVIEW_HANDOFF_AUTHORING_"
    "THEN_PERMANENT_RETIREMENT"
)
