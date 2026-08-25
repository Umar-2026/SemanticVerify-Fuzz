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

SUCCESSOR_REL = (
    BASE_REL
    + "/schema_v2_requirement_to_semantic_unit_crosswalk_"
      "evidence_resolution_study_v1_cwxr07_lifecycle_evidence_"
      "corrective_successor_v1"
)

AUTH158_REL = (
    SUCCESSOR_REL
    + "_review_package_authorization_v1"
)

COMPLETED_REL = (
    BASE_REL
    + "/schema_v2_requirement_to_semantic_unit_crosswalk_"
      "evidence_resolution_study_v1_completed_human_review_record_v1"
)

PACKAGE_REL = (
    SUCCESSOR_REL
    + "_review_package_v1"
)

EXPECTED_PARENT = "b0ae57379667f068c947ab3286a97ed9678590a3"
EXPECTED_A01_SHA = "efe7e2e356cf983448b94256a1e57952a68ef0c046a0c4be1ca5ee8336dc2c7c"
EXPECTED_D0157_SHA = "3b4f770bce1b137a40b8d1155fd481d734144e6ad3148f629c9c8e7c56b35def"

EXPECTED_SUCCESSOR_TREE = "5fdde69a9f860dcf53f94118f7fc0e0d8506f878"
EXPECTED_SUCCESSOR_MANIFEST_SHA = "05a89d827f168e3603a775e15d476f0a9c0078839326e3d5aba2f9dc19fb7ed7"
EXPECTED_SUCCESSOR_VERIFIER_SHA = "3001186e41f4558e2b0162410d103d534c3ae3dd16dcb5a83cbd7e9d1a1c4a42"
EXPECTED_SUCCESSOR_CHECKSUM_SHA = "2714f239950ed64a82a3da236f56e91a04599b0c080cf52c0b5fc04bbc499602"
EXPECTED_ORIGINAL_REVIEW_SHA = "2b1727b97d97409b36f4cfcd921e1857157afcef43b41998abaf152a67ce5e91"

PASS_MARKER = (
    "CWXR07_S1_INDEPENDENT_HUMAN_REVIEW_"
    "PACKAGE_AUTHORING_AUTHORIZATION=PASS"
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
        "STOP|CURRENT_HEAD_IS_NOT_IMMEDIATE_SUCCESSOR_OF_DECISION0157"
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

auth = REPO / AUTH158_REL

a01 = (
    auth
    / "01_independent_human_review_package_authorization.v1.json"
)

a03 = (
    auth
    / "03_independent_human_review_package_authorization.v1.SHA256SUMS"
)

if sha(a01) != EXPECTED_A01_SHA:
    raise SystemExit(
        "STOP|DECISION0158_A01_SHA_MISMATCH"
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

d0157 = (
    REPO
    / "documentation/decisions/"
      "0157-record-cwxr07-lifecycle-evidence-"
      "corrective-successor-v1.md"
)

if sha(d0157) != EXPECTED_D0157_SHA:
    raise SystemExit(
        "STOP|DECISION0157_SHA_MISMATCH"
    )

if run(
    "git",
    "rev-parse",
    f"HEAD:{SUCCESSOR_REL}",
) != EXPECTED_SUCCESSOR_TREE:
    raise SystemExit(
        "STOP|SUCCESSOR_TREE_CHANGED"
    )

successor = REPO / SUCCESSOR_REL

manifest = (
    successor
    / "01_cwxr07_s1_corrective_successor_manifest.v1.json"
)

safe_verifier = (
    successor
    / "16_verify_cwxr07_lifecycle_evidence_corrective_successor_v1.py"
)

checksum = (
    successor
    / "17_cwxr07_lifecycle_evidence_corrective_successor_v1.SHA256SUMS"
)

if sha(manifest) != EXPECTED_SUCCESSOR_MANIFEST_SHA:
    raise SystemExit(
        "STOP|SUCCESSOR_MANIFEST_SHA_MISMATCH"
    )

if sha(safe_verifier) != EXPECTED_SUCCESSOR_VERIFIER_SHA:
    raise SystemExit(
        "STOP|SUCCESSOR_SAFE_VERIFIER_SHA_MISMATCH"
    )

if sha(checksum) != EXPECTED_SUCCESSOR_CHECKSUM_SHA:
    raise SystemExit(
        "STOP|SUCCESSOR_CHECKSUM_SHA_MISMATCH"
    )

subprocess.check_call(
    [
        "sha256sum",
        "-c",
        checksum.name,
    ],
    cwd=successor,
    stdout=subprocess.DEVNULL,
)

obj = json.loads(
    manifest.read_text(
        encoding="utf-8"
    )
)

if obj["successor_criterion"] != "CWXR07-S1":
    raise SystemExit(
        "STOP|SUCCESSOR_CRITERION_MISMATCH"
    )

if (
    obj["status"]
    != "AUTHOR_CANDIDATE_AWAITING_INDEPENDENT_HUMAN_REVIEW"
):
    raise SystemExit(
        "STOP|SUCCESSOR_STATUS_MISMATCH"
    )

if obj["original_review"]["overall_decision"] != "REVISION_REQUIRED":
    raise SystemExit(
        "STOP|ORIGINAL_REVIEW_STATUS_MISMATCH"
    )

if obj["original_review"]["original_cwxr07_decision"] != "REVISION_REQUIRED":
    raise SystemExit(
        "STOP|ORIGINAL_CWXR07_STATUS_MISMATCH"
    )

claim = obj["claim_boundary"]

if (
    claim[
        "actual_external_process_execution_count_independently_proven"
    ]
    is not False
):
    raise SystemExit(
        "STOP|EXTERNAL_EXECUTION_COUNT_BOUNDARY_INVALID"
    )

if claim["global_no_rerun_fact_independently_proven"] is not False:
    raise SystemExit(
        "STOP|GLOBAL_NO_RERUN_BOUNDARY_INVALID"
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
        "STOP|ORIGINAL_COMPLETED_REVIEW_SHA_MISMATCH"
    )

packet = (
    successor
    / "13_CWXR07_S1_reviewer_packet.INITIAL_BLANK.v1.md"
)

packet_text = packet.read_text(
    encoding="utf-8"
)

required = [
    "Review only `CWXR07-S1`.",
    "Do not reopen CWXR01–CWXR06 or CWXR08.",
    "A PASS on CWXR07-S1 does **not** certify",
    "CWXR07-S1 decision:",
]

for marker in required:
    if marker not in packet_text:
        raise SystemExit(
            "STOP|REVIEW_PACKET_BOUNDARY_MARKER_MISSING"
        )

future = REPO / PACKAGE_REL

if future.exists():
    raise SystemExit(
        "STOP|REVIEW_PACKAGE_ALREADY_EXISTS"
    )

print(PASS_MARKER)

print("CURRENT_HEAD=" + head)
print("CURRENT_HEAD_PARENT_DECISION0157_BINDING=PASS")

print("SUCCESSOR_CRITERION=CWXR07-S1")
print("SUCCESSOR_STATUS=AUTHOR_CANDIDATE_AWAITING_INDEPENDENT_HUMAN_REVIEW")
print("SUCCESSOR_TREE_BINDING=PASS")
print("SUCCESSOR_CHECKSUM_CLOSURE=PASS")

print("ORIGINAL_REVIEW_STATUS=REVISION_REQUIRED")
print("ORIGINAL_CWXR07_STATUS=REVISION_REQUIRED")
print("ORIGINAL_REVIEW_MODIFIED=NO")

print("ACTUAL_PROCESS_EXECUTION_COUNT_INDEPENDENTLY_PROVEN=NO")
print("GLOBAL_NO_RERUN_FACT_INDEPENDENTLY_PROVEN=NO")
print("RECORD_ASSERTION_PROMOTED_TO_EXTERNAL_EXECUTION_FACT=NO")

print("DECISION0156_A02_EXECUTED_BY_THIS_VERIFIER=NO")
print("DECISION0154_A02_EXECUTED_BY_THIS_VERIFIER=NO")
print("DECISION0153_A02_EXECUTED_BY_THIS_VERIFIER=NO")
print("DECISION0147_A02_EXECUTED_BY_THIS_VERIFIER=NO")
print("RETIRED_A02_VERIFIERS_EXECUTED=NO")

print("EXTERNAL_HANDOFF_AUTHORIZED=NO")
print("HUMAN_REVIEW_COMPLETED=NO")
print("GOVERNANCE_ADOPTION_AUTHORIZED=NO")

print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")

print(
    "VERIFIER_LIFECYCLE="
    "ONE_FINAL_RUN_IMMEDIATELY_BEFORE_CWXR07_S1_"
    "INDEPENDENT_HUMAN_REVIEW_PACKAGE_AUTHORING_"
    "THEN_PERMANENT_RETIREMENT"
)
