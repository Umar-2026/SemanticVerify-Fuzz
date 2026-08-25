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

RECORD_REL = (
    BASE_REL
    + "/schema_v2_requirement_to_semantic_unit_crosswalk_"
      "evidence_resolution_study_v1_cwxr07_lifecycle_evidence_"
      "corrective_successor_v1_completed_human_review_record_v1"
)

AUTH_REL = (
    BASE_REL
    + "/schema_v2_requirement_to_semantic_unit_crosswalk_"
      "evidence_resolution_study_v1_cwxr07_s2_"
      "narrowed_corrective_successor_authorization_v1"
)

SUCCESSOR_REL = (
    BASE_REL
    + "/schema_v2_requirement_to_semantic_unit_crosswalk_"
      "evidence_resolution_study_v1_cwxr07_s2_"
      "narrowed_corrective_successor_v1"
)

EXPECTED_PARENT = "76bb99ad11f8fcaa8273bf23644624b6b1399c2b"
EXPECTED_A01_SHA = "62c6b2120b5864fd0c598db74012db28297604400f30c4e7f4613fc2bdc1e0b1"
EXPECTED_D0163_SHA = "438ce389f518a332c4ffd686219c4f7c2ba79db10eddaacc9033a54064a34d24"

EXPECTED_RECORD_TREE = "265da19aca751d98515ddcf7724180d6ebfd2f6e"
EXPECTED_MANIFEST_SHA = "86fff2558098bacc193192b83ecf2d13b029c7792df0f48c921bb4344ead1c17"
EXPECTED_RETURNED_SHA = "f5647d3532212830fc5f8100ec26aeac6ab38a626e9fc091473154567ff2f467"
EXPECTED_SAFE_VERIFIER_SHA = "97d03d33d8e1ee80fa4b175980a45f426192cf1da745cac44c540bafe81253be"
EXPECTED_CHECKSUM_SHA = "b9135ba8bb4a915121804aa806469dc58bac5b7a678ec535c7a875346989124e"

PASS_MARKER = (
    "CWXR07_S2_NARROWED_CORRECTIVE_"
    "SUCCESSOR_AUTHORING_AUTHORIZATION=PASS"
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
        "STOP|CURRENT_HEAD_IS_NOT_IMMEDIATE_SUCCESSOR_OF_DECISION0163"
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

a01 = auth / "01_cwxr07_s2_narrowed_corrective_successor_authorization.v1.json"
a03 = auth / "03_cwxr07_s2_narrowed_corrective_successor_authorization.v1.SHA256SUMS"

if sha(a01) != EXPECTED_A01_SHA:
    raise SystemExit(
        "STOP|DECISION0164_A01_SHA_MISMATCH"
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

d0163 = (
    REPO
    / "documentation/decisions/"
      "0163-record-genuine-cwxr07-s1-revision-required-human-review.md"
)

if sha(d0163) != EXPECTED_D0163_SHA:
    raise SystemExit(
        "STOP|DECISION0163_SHA_MISMATCH"
    )

if run(
    "git",
    "rev-parse",
    f"HEAD:{RECORD_REL}",
) != EXPECTED_RECORD_TREE:
    raise SystemExit(
        "STOP|COMPLETED_REVIEW_RECORD_TREE_CHANGED"
    )

record = REPO / RECORD_REL

manifest = record / "01_completed_human_review_manifest.v1.json"
returned = record / "02_returned_human_review.EXACT_COPY.v1.md"
safe_verifier = record / "07_verify_completed_human_review_record_v1.py"
checksum = record / "08_completed_human_review_record_v1.SHA256SUMS"

if sha(manifest) != EXPECTED_MANIFEST_SHA:
    raise SystemExit(
        "STOP|COMPLETED_REVIEW_MANIFEST_SHA_MISMATCH"
    )

if sha(returned) != EXPECTED_RETURNED_SHA:
    raise SystemExit(
        "STOP|RETURNED_REVIEW_SHA_MISMATCH"
    )

if sha(safe_verifier) != EXPECTED_SAFE_VERIFIER_SHA:
    raise SystemExit(
        "STOP|COMPLETED_REVIEW_SAFE_VERIFIER_SHA_MISMATCH"
    )

if sha(checksum) != EXPECTED_CHECKSUM_SHA:
    raise SystemExit(
        "STOP|COMPLETED_REVIEW_CHECKSUM_SHA_MISMATCH"
    )

subprocess.check_call(
    [
        "sha256sum",
        "-c",
        checksum.name,
    ],
    cwd=record,
    stdout=subprocess.DEVNULL,
)

obj = json.loads(
    manifest.read_text(
        encoding="utf-8"
    )
)

if obj["review_scope"] != "CWXR07-S1_ONLY":
    raise SystemExit(
        "STOP|HISTORICAL_REVIEW_SCOPE_CHANGED"
    )

if (
    obj["human_review"]["cwxr07_s1_decision"]
    != "REVISION_REQUIRED"
):
    raise SystemExit(
        "STOP|HISTORICAL_S1_DECISION_CHANGED"
    )

if obj["review_result"]["successor_approved"] is not False:
    raise SystemExit(
        "STOP|HISTORICAL_S1_APPROVAL_STATE_CHANGED"
    )

remediation = obj["reviewer_requested_remediation"]

if (
    remediation["option_2"]
    != "FURTHER_NARROW_CWXR07_S1_TO_BYTE_INTEGRITY_AND_INTERNAL_CONSISTENCY"
):
    raise SystemExit(
        "STOP|REVIEWER_OPTION_2_BINDING_MISSING"
    )

future = REPO / SUCCESSOR_REL

if future.exists():
    raise SystemExit(
        "STOP|CWXR07_S2_SUCCESSOR_ALREADY_EXISTS"
    )

print(PASS_MARKER)

print("CURRENT_HEAD=" + head)
print("CURRENT_HEAD_PARENT_DECISION0163_BINDING=PASS")

print("HISTORICAL_CWXR07_S1_DECISION=REVISION_REQUIRED")
print("HISTORICAL_CWXR07_S1_MODIFIED=NO")

print("SELECTED_REVIEWER_CORRECTIVE_OPTION=2")
print("NEW_SUCCESSOR_CRITERION=CWXR07-S2")

print("BYTE_INTEGRITY_REVIEW_REQUIRED=YES")
print("INTERNAL_CONSISTENCY_REVIEW_REQUIRED=YES")

print("GIT_PARENTAGE_INDEPENDENT_PROOF_REQUIRED_BY_S2=NO")
print("STUDY_TREE_IDENTITY_INDEPENDENT_PROOF_REQUIRED_BY_S2=NO")
print("TRACKED_PATH_HISTORY_INDEPENDENT_PROOF_REQUIRED_BY_S2=NO")
print("CONTRADICTION_SEARCH_CORRECTNESS_INDEPENDENT_PROOF_REQUIRED_BY_S2=NO")

print("ACTUAL_EXTERNAL_EXACTLY_ONCE_FACT_PROVEN=NO")
print("GLOBAL_NO_RERUN_FACT_PROVEN=NO")

print("SEALED_GIT_BUNDLE_AUTHORIZED=NO")
print("FULL_REPOSITORY_SNAPSHOT_AUTHORIZED=NO")

print("INDEPENDENT_SUCCESSOR_HUMAN_REVIEW_REQUIRED=YES")
print("SUCCESSOR_HUMAN_REVIEW_COMPLETED=NO")

print("GOVERNANCE_ADOPTION_AUTHORIZED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")

print(
    "VERIFIER_LIFECYCLE="
    "ONE_FINAL_RUN_IMMEDIATELY_BEFORE_CWXR07_S2_"
    "NARROWED_CORRECTIVE_SUCCESSOR_AUTHORING_"
    "THEN_PERMANENT_RETIREMENT"
)
