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

STUDY_REL = (
    BASE_REL
    + "/schema_v2_requirement_to_semantic_unit_"
      "crosswalk_evidence_resolution_study_v1"
)

AUTH_REL = (
    BASE_REL
    + "/schema_v2_requirement_to_semantic_unit_"
      "crosswalk_evidence_resolution_study_v1_"
      "review_package_authorization_v1"
)

PACKAGE_REL = (
    BASE_REL
    + "/schema_v2_requirement_to_semantic_unit_"
      "crosswalk_evidence_resolution_study_v1_"
      "review_package_v1"
)

EXPECTED_PARENT = "899dd232f5e49793472f9e8b7ac3a95185caa99d"
EXPECTED_STUDY_TREE = "6f12e8a4c2fa520fd36cced03241ea5b4666969e"

EXPECTED_A01_SHA = "c3d6e190d355ac9c6a7c08f03581f3d1edc583a0876b71756746891ebdeeaa44"
EXPECTED_D0148_SHA = "9a48f45b74351cace9b4f1b2ee06fb037a3e71b5d0f268443270aed1f961adee"

EXPECTED_MANIFEST_SHA = "d8ce65985f33ced593f379f11eefa9b681fde6a10693c0bbc1a6a9fa347bb3e7"
EXPECTED_PAIR_SHA = "389615002582964b97aa6eb717ceb520067cef78b18cf482cf257fe9b36f2515"
EXPECTED_ROLLUP_SHA = "77bded52d6a5883e7a27cd786bea981256d0dac8b22cfe4b945d30628dbbc070"
EXPECTED_PROV_SHA = "0935a8bb7c02e9a31b419a56d9cd3ee391b1051603804b7ce2d3c4a8d9d58a69"
EXPECTED_ACCOUNT_SHA = "aa676f9482837936ecb4ea2901b811ed5c6fc8f2f8fdc35f06f7f4eac59c06d2"
EXPECTED_SAFE_VERIFIER_SHA = "f3df50284eefc06c5db625607a3399451acbe0c8f1f5069496f1d4ac02f3d9d2"
EXPECTED_STUDY_SUMS_SHA = "8d8e79bc543e71ebe7310e64c96c16a4c078e01ee0124b5817c844c12aaf6b75"

EXPECTED_D0147_A02_OUTPUT_SHA = "f5a4e0f183ae8c86b34660aada18826a2aa24b80e8680f377311b5a8f92b2518"
EXPECTED_D0147_A02_CONSUMPTION_SHA = "2a2da4b046286211e4d744d0bdc2b56f133008e266bc012a5d5e4b1b26eb9ab0"

PASS_MARKER = (
    "REQUIREMENT_TO_SEMANTIC_UNIT_CROSSWALK_"
    "EVIDENCE_RESOLUTION_STUDY_V1_REVIEW_PACKAGE_"
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
        "STOP|CURRENT_HEAD_IS_NOT_IMMEDIATE_SUCCESSOR_OF_DECISION0148"
    )

if run("git", "rev-parse", f"HEAD:{STUDY_REL}") != EXPECTED_STUDY_TREE:
    raise SystemExit(
        "STOP|CROSSWALK_STUDY_TREE_CHANGED"
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

study = REPO / STUDY_REL
auth = REPO / AUTH_REL
package = REPO / PACKAGE_REL

if package.exists():
    raise SystemExit(
        "STOP|REVIEW_PACKAGE_ALREADY_EXISTS"
    )

a01 = auth / "01_independent_human_review_package_authorization.v1.json"
a03 = auth / "03_independent_human_review_package_authorization.v1.SHA256SUMS"

if sha(a01) != EXPECTED_A01_SHA:
    raise SystemExit(
        "STOP|A01_SHA_MISMATCH"
    )

# Authorization checksum closure must validate without executing
# any historical/retired verifier.
subprocess.check_call(
    [
        "sha256sum",
        "-c",
        a03.name,
    ],
    cwd=auth,
    stdout=subprocess.DEVNULL,
)

d0148 = (
    REPO
    / "documentation/decisions/"
      "0148-record-requirement-to-semantic-unit-crosswalk-"
      "evidence-resolution-study-v1.md"
)

if sha(d0148) != EXPECTED_D0148_SHA:
    raise SystemExit(
        "STOP|DECISION0148_SHA_MISMATCH"
    )

checks = {
    "01_study_manifest.v1.json":
        EXPECTED_MANIFEST_SHA,

    "04_requirement_semantic_unit_pair_matrix.v1.json":
        EXPECTED_PAIR_SHA,

    "05_requirement_crosswalk_rollup.v1.json":
        EXPECTED_ROLLUP_SHA,

    "06_evidence_provenance_matrix.v1.json":
        EXPECTED_PROV_SHA,

    "07_accounting_summary.v1.json":
        EXPECTED_ACCOUNT_SHA,

    "08_decision0147_a02_final_output.EXACT_COPY.v1.txt":
        EXPECTED_D0147_A02_OUTPUT_SHA,

    "09_decision0147_a02_consumption_record.v1.json":
        EXPECTED_D0147_A02_CONSUMPTION_SHA,

    "10_verify_requirement_to_semantic_unit_crosswalk_"
    "evidence_resolution_study_v1.v1.py":
        EXPECTED_SAFE_VERIFIER_SHA,

    "11_study_v1.SHA256SUMS":
        EXPECTED_STUDY_SUMS_SHA,
}

for name, expected in checks.items():
    if sha(study / name) != expected:
        raise SystemExit(
            "STOP|STUDY_ARTIFACT_SHA_MISMATCH|" + name
        )

consumption = json.loads(
    (
        study
        / "09_decision0147_a02_consumption_record.v1.json"
    ).read_text(encoding="utf-8")
)

if consumption.get("a02_execution_count") != 1:
    raise SystemExit(
        "STOP|DECISION0147_A02_EXECUTION_COUNT_NOT_ONE"
    )

if consumption.get("lifecycle_after_execution") != "PERMANENTLY_RETIRED":
    raise SystemExit(
        "STOP|DECISION0147_A02_NOT_RETIRED"
    )

if consumption.get("rerun_authorized") is not False:
    raise SystemExit(
        "STOP|DECISION0147_A02_RERUN_STATE_INVALID"
    )

safe_verifier = (
    study
    / "10_verify_requirement_to_semantic_unit_crosswalk_"
      "evidence_resolution_study_v1.v1.py"
)

safe_output = subprocess.check_output(
    ["python3", str(safe_verifier)],
    cwd=REPO,
    text=True,
)

required_safe_markers = [
    (
        "REQUIREMENT_TO_SEMANTIC_UNIT_CROSSWALK_"
        "EVIDENCE_RESOLUTION_STUDY_V1=PASS"
    ),
    "STUDY_STATUS=AUTHOR_CANDIDATE",
    "PAIR_UNIVERSE_COUNT=1853",
    "UNRESOLVED_BINDING_COUNT=1853",
    "UNRESOLVED_REQUIREMENT_COUNT=17",
    "GLOBAL_OUTCOME=FURTHER_EVIDENCE_REQUIRED",
    "INDEPENDENT_HUMAN_REVIEW_REQUIRED=YES",
    "STUDY_GOVERNANCE_ADOPTED=NO",
    "DECISION_0147_A02_STATE=PERMANENTLY_RETIRED",
]

for marker in required_safe_markers:
    if marker not in safe_output.splitlines():
        raise SystemExit(
            "STOP|SAFE_STUDY_VERIFIER_REQUIRED_MARKER_MISSING|"
            + marker
        )

print(PASS_MARKER)
print("CURRENT_HEAD=" + head)
print("CURRENT_HEAD_PARENT_DECISION0148_BINDING=PASS")
print("CROSSWALK_STUDY_V1_TREE_BINDING=PASS")
print("STUDY_STATUS=AUTHOR_CANDIDATE")
print("REQUIREMENT_COUNT=17")
print("SEMANTIC_UNIT_COUNT=109")
print("PAIR_UNIVERSE_COUNT=1853")
print("SUPPORTED_BINDING_COUNT=0")
print("NOT_SUPPORTED_BINDING_COUNT=0")
print("UNRESOLVED_BINDING_COUNT=1853")
print("UNRESOLVED_REQUIREMENT_COUNT=17")
print("GLOBAL_OUTCOME=FURTHER_EVIDENCE_REQUIRED")
print("INDEPENDENT_HUMAN_REVIEW_REQUIRED=YES")
print("INDEPENDENT_HUMAN_REVIEW_COMPLETED=NO")
print("STUDY_GOVERNANCE_ADOPTED=NO")
print("DECISION_0147_A02_STATE=PERMANENTLY_RETIRED")
print("DECISION_0147_A02_EXECUTED_BY_THIS_VERIFIER=NO")
print("RETIRED_A02_VERIFIERS_EXECUTED=NO")
print("EXTERNAL_HANDOFF_AUTHORIZED=NO")
print("GOVERNANCE_ADOPTION_AUTHORIZED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
print(
    "VERIFIER_LIFECYCLE="
    "ONE_FINAL_RUN_IMMEDIATELY_BEFORE_INDEPENDENT_HUMAN_"
    "REVIEW_PACKAGE_AUTHORING_THEN_PERMANENT_RETIREMENT"
)
