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

AUTH156_REL = (
    BASE_REL
    + "/schema_v2_requirement_to_semantic_unit_crosswalk_"
      "evidence_resolution_study_v1_cwxr07_lifecycle_evidence_"
      "corrective_successor_authorization_v1"
)

COMPLETED_REL = (
    BASE_REL
    + "/schema_v2_requirement_to_semantic_unit_crosswalk_"
      "evidence_resolution_study_v1_completed_human_review_record_v1"
)

STUDY_REL = (
    BASE_REL
    + "/schema_v2_requirement_to_semantic_unit_crosswalk_"
      "evidence_resolution_study_v1"
)

AUTH147_REL = (
    BASE_REL
    + "/schema_v2_requirement_to_semantic_unit_crosswalk_"
      "evidence_resolution_study_v1_authorization_v1"
)

A02_147_REL = (
    AUTH147_REL
    + "/02_verify_requirement_to_semantic_unit_crosswalk_"
      "evidence_resolution_study_v1_authoring_authorization.v1.py"
)

EXPECTED_PARENT = "1326a8584c31f941aca3fc946119f73114a08d62"
EXPECTED_A01_SHA = "74716d3a5b10dd7453e941ce38864afb0e69c2e3e73dbf2b1a40c36a4b1bedd9"
EXPECTED_D0155_SHA = "482168f8fb728293fcc17ee71d1a62e38003c01e53491afe5b9c3ef8ac0f56f9"
EXPECTED_COMPLETED_TREE = "b4bb9b57ae25f90c5dc2506a90ade02e810c4388"
EXPECTED_REVIEW_SHA = "2b1727b97d97409b36f4cfcd921e1857157afcef43b41998abaf152a67ce5e91"

D0147 = "f083884cf9b4e44505a4481fb15d9748c530c65b"
D0148 = "899dd232f5e49793472f9e8b7ac3a95185caa99d"

EXPECTED_HISTORICAL_A02_SHA = "e013514045bcaf08b741cde13c54a51760de37a6217129e5f74602f6a49356d2"
EXPECTED_STUDY_TREE = "6f12e8a4c2fa520fd36cced03241ea5b4666969e"
EXPECTED_OUTPUT_SHA = "f5a4e0f183ae8c86b34660aada18826a2aa24b80e8680f377311b5a8f92b2518"
EXPECTED_CONSUMPTION_SHA = "2a2da4b046286211e4d744d0bdc2b56f133008e266bc012a5d5e4b1b26eb9ab0"

PASS_MARKER = (
    "CWXR07_LIFECYCLE_EVIDENCE_CORRECTIVE_"
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
        "STOP|CURRENT_HEAD_IS_NOT_IMMEDIATE_SUCCESSOR_OF_DECISION0155"
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

auth = REPO / AUTH156_REL

a01 = (
    auth
    / "01_cwxr07_lifecycle_evidence_"
      "corrective_successor_authorization.v1.json"
)

a03 = (
    auth
    / "03_cwxr07_lifecycle_evidence_"
      "corrective_successor_authorization.v1.SHA256SUMS"
)

if sha(a01) != EXPECTED_A01_SHA:
    raise SystemExit(
        "STOP|DECISION0156_A01_SHA_MISMATCH"
    )

subprocess.check_call(
    ["sha256sum", "-c", a03.name],
    cwd=auth,
    stdout=subprocess.DEVNULL,
)

d0155 = (
    REPO
    / "documentation/decisions/"
      "0155-record-completed-cwxr01-cwxr08-human-review-"
      "with-revision-required-outcome.md"
)

if sha(d0155) != EXPECTED_D0155_SHA:
    raise SystemExit(
        "STOP|DECISION0155_SHA_MISMATCH"
    )

if run(
    "git",
    "rev-parse",
    f"HEAD:{COMPLETED_REL}",
) != EXPECTED_COMPLETED_TREE:
    raise SystemExit(
        "STOP|COMPLETED_REVIEW_TREE_CHANGED"
    )

review = (
    REPO
    / COMPLETED_REL
    / "02_CWXR01_CWXR08_returned_reviewer_packet.EXACT_COPY.v1.md"
)

if sha(review) != EXPECTED_REVIEW_SHA:
    raise SystemExit(
        "STOP|COMPLETED_REVIEW_PACKET_SHA_MISMATCH"
    )

review_text = review.read_text(
    encoding="utf-8"
)

required_review_markers = [
    "CWXR07 decision: `REVISION_REQUIRED`",
    (
        "cannot independently establish that A02 was executed exactly once "
        "or that no rerun occurred"
    ),
    (
        "Supply independently reviewable lifecycle evidence or narrow this "
        "criterion to verification of the preserved record."
    ),
]

for marker in required_review_markers:
    if marker not in review_text:
        raise SystemExit(
            "STOP|REVIEWER_CORRECTIVE_MARKER_MISSING"
        )

if run(
    "git",
    "rev-parse",
    f"{D0148}^",
) != D0147:
    raise SystemExit(
        "STOP|D0148_PARENT_NOT_D0147"
    )

historical_script_sha = hashlib.sha256(
    subprocess.check_output(
        [
            "git",
            "show",
            f"{D0147}:{A02_147_REL}",
        ],
        cwd=REPO,
    )
).hexdigest()

if historical_script_sha != EXPECTED_HISTORICAL_A02_SHA:
    raise SystemExit(
        "STOP|HISTORICAL_D0147_A02_SHA_MISMATCH"
    )

if sha(REPO / A02_147_REL) != EXPECTED_HISTORICAL_A02_SHA:
    raise SystemExit(
        "STOP|CURRENT_D0147_A02_SHA_MISMATCH"
    )

if run(
    "git",
    "rev-parse",
    f"{D0148}:{STUDY_REL}",
) != EXPECTED_STUDY_TREE:
    raise SystemExit(
        "STOP|D0148_STUDY_TREE_MISMATCH"
    )

if run(
    "git",
    "rev-parse",
    f"HEAD:{STUDY_REL}",
) != EXPECTED_STUDY_TREE:
    raise SystemExit(
        "STOP|CURRENT_STUDY_TREE_MISMATCH"
    )

output_path = (
    REPO
    / STUDY_REL
    / "08_decision0147_a02_final_output.EXACT_COPY.v1.txt"
)

cons_path = (
    REPO
    / STUDY_REL
    / "09_decision0147_a02_consumption_record.v1.json"
)

if sha(output_path) != EXPECTED_OUTPUT_SHA:
    raise SystemExit(
        "STOP|HISTORICAL_OUTPUT_SHA_MISMATCH"
    )

if sha(cons_path) != EXPECTED_CONSUMPTION_SHA:
    raise SystemExit(
        "STOP|HISTORICAL_CONSUMPTION_SHA_MISMATCH"
    )

cons = json.loads(
    cons_path.read_text(
        encoding="utf-8"
    )
)

if cons["a02_execution_count"] != 1:
    raise SystemExit(
        "STOP|PRESERVED_RECORD_EXECUTION_COUNT_NOT_ONE"
    )

if cons["a02_return_code"] != 0:
    raise SystemExit(
        "STOP|PRESERVED_RECORD_RETURN_CODE_NOT_ZERO"
    )

if cons["a02_pass_marker_present"] is not True:
    raise SystemExit(
        "STOP|PRESERVED_RECORD_PASS_MARKER_FALSE"
    )

if cons["lifecycle_after_execution"] != "PERMANENTLY_RETIRED":
    raise SystemExit(
        "STOP|PRESERVED_RECORD_LIFECYCLE_INVALID"
    )

if cons["rerun_authorized"] is not False:
    raise SystemExit(
        "STOP|PRESERVED_RECORD_RERUN_STATE_INVALID"
    )

future = (
    REPO
    / (
        BASE_REL
        + "/schema_v2_requirement_to_semantic_unit_crosswalk_"
          "evidence_resolution_study_v1_cwxr07_lifecycle_evidence_"
          "corrective_successor_v1"
    )
)

if future.exists():
    raise SystemExit(
        "STOP|CWXR07_SUCCESSOR_ALREADY_EXISTS"
    )

print(PASS_MARKER)

print("CURRENT_HEAD=" + head)
print("CURRENT_HEAD_PARENT_DECISION0155_BINDING=PASS")

print("ORIGINAL_REVIEW_STATUS=REVISION_REQUIRED")
print("ORIGINAL_CWXR07_STATUS=REVISION_REQUIRED")

print("CORRECTIVE_STRATEGY=NARROWED_CRITERION_PLUS_ADDITIONAL_REVIEWABLE_REPOSITORY_EVIDENCE")
print("SUCCESSOR_CRITERION_ID=CWXR07-S1")

print("DECISION0147_A02_BYTE_IDENTITY=PASS")
print("DECISION0147_TO_DECISION0148_IMMEDIATE_PARENTAGE=PASS")
print("DECISION0148_STUDY_TREE_IMMUTABILITY=PASS")
print("PRESERVED_A02_OUTPUT_BINDING=PASS")
print("PRESERVED_A02_CONSUMPTION_RECORD_BINDING=PASS")

print("RECORDED_EXECUTION_COUNT=1")
print("RECORDED_RETURN_CODE=0")
print("RECORDED_LIFECYCLE=PERMANENTLY_RETIRED")
print("RECORDED_RERUN_AUTHORIZED=NO")

print("ACTUAL_PROCESS_EXECUTION_COUNT_INDEPENDENTLY_PROVEN=NO")
print("GLOBAL_NO_RERUN_FACT_INDEPENDENTLY_PROVEN=NO")
print("RECORD_ASSERTION_PROMOTED_TO_EXTERNAL_EXECUTION_FACT=NO")

print("DECISION0147_A02_EXECUTED_BY_THIS_VERIFIER=NO")
print("RETIRED_A02_VERIFIERS_EXECUTED=NO")

print("GOVERNANCE_ADOPTION_AUTHORIZED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")

print(
    "VERIFIER_LIFECYCLE="
    "ONE_FINAL_RUN_IMMEDIATELY_BEFORE_CWXR07_"
    "CORRECTIVE_SUCCESSOR_AUTHORING_THEN_PERMANENT_RETIREMENT"
)
