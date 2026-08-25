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
    + "/schema_v2_requirement_to_semantic_unit_crosswalk_"
      "evidence_resolution_study_v1_cwxr07_lifecycle_evidence_"
      "corrective_successor_v1_review_package_v1"
)

AUTH160_REL = (
    BASE_REL
    + "/schema_v2_requirement_to_semantic_unit_crosswalk_"
      "evidence_resolution_study_v1_cwxr07_lifecycle_evidence_"
      "corrective_successor_v1_external_handoff_authorization_v1"
)

HANDOFF_REL = (
    BASE_REL
    + "/schema_v2_requirement_to_semantic_unit_crosswalk_"
      "evidence_resolution_study_v1_cwxr07_lifecycle_evidence_"
      "corrective_successor_v1_external_handoff_v1"
)

COMPLETED_REL = (
    BASE_REL
    + "/schema_v2_requirement_to_semantic_unit_crosswalk_"
      "evidence_resolution_study_v1_completed_human_review_record_v1"
)

EXPECTED_PARENT = "54facedc1756ab12b9b41924b8ed86f100ac7af4"
EXPECTED_A01_SHA = "8dd3f6c496afc0958a3ea20f673acaec9c78a0ee4b6edb5daad386660076f532"
EXPECTED_D0159_SHA = "e6d264a7e34415e47713175770504baba1f24ccf473e2ee28335843831ebc43c"

EXPECTED_PACKAGE_TREE = "bf898f97443395d16d9a7313c5125b9fcaeb7443"
EXPECTED_PACKAGE_MANIFEST_SHA = "77f6e68e6e320517e17e9d93d562af15436367225167ff6e5aed1f5a060b2737"
EXPECTED_BLANK_PACKET_SHA = "e48090854cb7ab71a057963e831f08fdeaf52b179398495c5ffbae34113a39e6"
EXPECTED_PACKAGE_VERIFIER_SHA = "ede6fd42bfad4c4292df6442d5e1ddc50d1c58fe56ca052385535b50e6b626ad"
EXPECTED_PACKAGE_CHECKSUM_SHA = "4c3535e16bcf72c00c4b622dfd1be7b17f752200e94ae50a84e0202d45c830c1"
EXPECTED_ORIGINAL_REVIEW_SHA = "2b1727b97d97409b36f4cfcd921e1857157afcef43b41998abaf152a67ce5e91"

EXTERNAL_ZIP = Path("/openbayes/home/46_CWXR07_S1_independent_human_review_handoff.v1.zip")
EXTERNAL_REVIEW_COPY = Path("/openbayes/home/46_CWXR07_S1_reviewer_packet.MANUAL_REVIEW_COPY.v1.md")

PASS_MARKER = (
    "CWXR07_S1_EXTERNAL_INDEPENDENT_HUMAN_"
    "REVIEW_HANDOFF_AUTHORING_AUTHORIZATION=PASS"
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
        "STOP|CURRENT_HEAD_IS_NOT_IMMEDIATE_SUCCESSOR_OF_DECISION0159"
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

auth = REPO / AUTH160_REL

a01 = (
    auth
    / "01_external_independent_human_review_handoff_authorization.v1.json"
)

a03 = (
    auth
    / "03_external_independent_human_review_handoff_authorization.v1.SHA256SUMS"
)

if sha(a01) != EXPECTED_A01_SHA:
    raise SystemExit(
        "STOP|DECISION0160_A01_SHA_MISMATCH"
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

d0159 = (
    REPO
    / "documentation/decisions/"
      "0159-record-cwxr07-s1-independent-human-review-package-v1.md"
)

if sha(d0159) != EXPECTED_D0159_SHA:
    raise SystemExit(
        "STOP|DECISION0159_SHA_MISMATCH"
    )

if run(
    "git",
    "rev-parse",
    f"HEAD:{PACKAGE_REL}",
) != EXPECTED_PACKAGE_TREE:
    raise SystemExit(
        "STOP|REVIEW_PACKAGE_TREE_CHANGED"
    )

package = REPO / PACKAGE_REL

manifest = package / "01_review_package_manifest.v1.json"
blank = (
    package
    / "07_CWXR07_S1_reviewer_packet.INITIAL_BLANK.EXACT_COPY.v1.md"
)
safe_verifier = (
    package
    / "10_verify_cwxr07_s1_independent_human_review_package_v1.py"
)
checksum = package / "11_review_package_v1.SHA256SUMS"

if sha(manifest) != EXPECTED_PACKAGE_MANIFEST_SHA:
    raise SystemExit(
        "STOP|PACKAGE_MANIFEST_SHA_MISMATCH"
    )

if sha(blank) != EXPECTED_BLANK_PACKET_SHA:
    raise SystemExit(
        "STOP|BLANK_REVIEWER_PACKET_SHA_MISMATCH"
    )

if sha(safe_verifier) != EXPECTED_PACKAGE_VERIFIER_SHA:
    raise SystemExit(
        "STOP|PACKAGE_SAFE_VERIFIER_SHA_MISMATCH"
    )

if sha(checksum) != EXPECTED_PACKAGE_CHECKSUM_SHA:
    raise SystemExit(
        "STOP|PACKAGE_CHECKSUM_SHA_MISMATCH"
    )

subprocess.check_call(
    [
        "sha256sum",
        "-c",
        checksum.name,
    ],
    cwd=package,
    stdout=subprocess.DEVNULL,
)

obj = json.loads(
    manifest.read_text(
        encoding="utf-8"
    )
)

if obj["review_scope"] != "CWXR07-S1_ONLY":
    raise SystemExit(
        "STOP|REVIEW_SCOPE_MISMATCH"
    )

contract = obj["review_contract"]

if contract["criterion"] != "CWXR07-S1":
    raise SystemExit(
        "STOP|SUCCESSOR_CRITERION_MISMATCH"
    )

if contract["human_review_completed"] is not False:
    raise SystemExit(
        "STOP|HUMAN_REVIEW_ALREADY_COMPLETED"
    )

if contract["reviewer_identity_recorded"] is not False:
    raise SystemExit(
        "STOP|REVIEWER_IDENTITY_ALREADY_RECORDED"
    )

if contract["item_decision_recorded"] is not False:
    raise SystemExit(
        "STOP|REVIEWER_ITEM_DECISION_ALREADY_RECORDED"
    )

claim = obj["claim_boundary"]

if (
    claim[
        "actual_external_process_execution_count_independently_proven"
    ]
    is not False
):
    raise SystemExit(
        "STOP|EXTERNAL_PROCESS_CLAIM_BOUNDARY_INVALID"
    )

if claim["global_no_rerun_fact_independently_proven"] is not False:
    raise SystemExit(
        "STOP|GLOBAL_NO_RERUN_CLAIM_BOUNDARY_INVALID"
    )

if claim["record_assertion_promoted_to_external_execution_fact"] is not False:
    raise SystemExit(
        "STOP|RECORD_PROMOTION_BOUNDARY_INVALID"
    )

original_review = (
    REPO
    / COMPLETED_REL
    / "02_CWXR01_CWXR08_returned_reviewer_packet.EXACT_COPY.v1.md"
)

if sha(original_review) != EXPECTED_ORIGINAL_REVIEW_SHA:
    raise SystemExit(
        "STOP|ORIGINAL_REVIEW_SHA_MISMATCH"
    )

future = REPO / HANDOFF_REL

if future.exists():
    raise SystemExit(
        "STOP|EXTERNAL_HANDOFF_ALREADY_EXISTS"
    )

if EXTERNAL_ZIP.exists():
    raise SystemExit(
        "STOP|EXTERNAL_ZIP_ALREADY_EXISTS"
    )

if EXTERNAL_REVIEW_COPY.exists():
    raise SystemExit(
        "STOP|EXTERNAL_REVIEW_COPY_ALREADY_EXISTS"
    )

print(PASS_MARKER)

print("CURRENT_HEAD=" + head)
print("CURRENT_HEAD_PARENT_DECISION0159_BINDING=PASS")

print("REVIEW_SCOPE=CWXR07-S1_ONLY")
print("PACKAGE_TREE_BINDING=PASS")
print("PACKAGE_CHECKSUM_CLOSURE=PASS")

print("ORIGINAL_REVIEW_STATUS=REVISION_REQUIRED")
print("ORIGINAL_CWXR07_STATUS=REVISION_REQUIRED")
print("ORIGINAL_REVIEW_MODIFIED=NO")

print("ACTUAL_PROCESS_EXECUTION_COUNT_INDEPENDENTLY_PROVEN=NO")
print("GLOBAL_NO_RERUN_FACT_INDEPENDENTLY_PROVEN=NO")
print("RECORD_ASSERTION_PROMOTED_TO_EXTERNAL_EXECUTION_FACT=NO")

print("HUMAN_REVIEW_COMPLETED=NO")
print("REVIEWER_IDENTITY_RECORDED=NO")
print("REVIEWER_DECISION_RECORDED=NO")

print("DECISION0158_A02_EXECUTED_BY_THIS_VERIFIER=NO")
print("DECISION0156_A02_EXECUTED_BY_THIS_VERIFIER=NO")
print("DECISION0154_A02_EXECUTED_BY_THIS_VERIFIER=NO")
print("DECISION0153_A02_EXECUTED_BY_THIS_VERIFIER=NO")
print("DECISION0147_A02_EXECUTED_BY_THIS_VERIFIER=NO")
print("RETIRED_A02_VERIFIERS_EXECUTED=NO")

print("GOVERNANCE_ADOPTION_AUTHORIZED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")

print(
    "VERIFIER_LIFECYCLE="
    "ONE_FINAL_RUN_IMMEDIATELY_BEFORE_EXTERNAL_"
    "INDEPENDENT_HUMAN_REVIEW_HANDOFF_AUTHORING_"
    "THEN_PERMANENT_RETIREMENT"
)
