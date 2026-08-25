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
    + "/schema_v2_requirement_to_semantic_unit_crosswalk_"
      "evidence_resolution_study_v1_cwxr07_lifecycle_evidence_"
      "corrective_successor_v1_external_handoff_v1"
)

AUTH162_REL = (
    BASE_REL
    + "/schema_v2_requirement_to_semantic_unit_crosswalk_"
      "evidence_resolution_study_v1_cwxr07_lifecycle_evidence_"
      "corrective_successor_v1_completed_human_review_"
      "recording_authorization_v1"
)

RECORD_REL = (
    BASE_REL
    + "/schema_v2_requirement_to_semantic_unit_crosswalk_"
      "evidence_resolution_study_v1_cwxr07_lifecycle_evidence_"
      "corrective_successor_v1_completed_human_review_record_v1"
)

EXPECTED_PARENT = "43222ebd72b36f40f48509bc11594303a4b5064a"
EXPECTED_A01_SHA = "64db63e5714113358b82c3649eccbb4c71938a22b641644520d7231b384d881d"
EXPECTED_D0161_SHA = "37d54f33b7d9997b4a18b2d4102769a05b348466254ad6db1eaf16738f1852f9"

EXPECTED_HANDOFF_TREE = "672ce477e011238bbbb57f16f354fe3952f33ecd"
EXPECTED_HANDOFF_MANIFEST_SHA = "def8bbc01056e819fe1edfc6b78e7c73947406fe5458ce7d065d355cb24bc390"
EXPECTED_HANDOFF_CHECKSUM_SHA = "b9eb241bbd8cfe4ab9f7d18fd923451a970e7cc7cf8383199ece16423815545a"

RETURNED = Path("/openbayes/home/46_CWXR07_S1_manually_reviewer_packet.MANUAL_REVIEW_COPY.v1.md")
EXPECTED_RETURNED_SHA = "f5647d3532212830fc5f8100ec26aeac6ab38a626e9fc091473154567ff2f467"
EXPECTED_RETURNED_SIZE = 4138

ORIGINAL_EDITABLE = Path("/openbayes/home/46_CWXR07_S1_reviewer_packet.MANUAL_REVIEW_COPY.v1.md")
EXPECTED_ORIGINAL_EDITABLE_SHA = "e48090854cb7ab71a057963e831f08fdeaf52b179398495c5ffbae34113a39e6"

EXTERNAL_ZIP = Path("/openbayes/home/46_CWXR07_S1_independent_human_review_handoff.v1.zip")
EXPECTED_EXTERNAL_ZIP_SHA = "5db52465a62fea2f9526d4c3c3e01bdf4decd14ca56a80fb3819bb1e0746f4d7"

PASS_MARKER = (
    "GENUINE_CWXR07_S1_REVISION_REQUIRED_"
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
        "STOP|CURRENT_HEAD_IS_NOT_IMMEDIATE_SUCCESSOR_OF_DECISION0161"
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

auth = REPO / AUTH162_REL

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
        "STOP|DECISION0162_A01_SHA_MISMATCH"
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

d0161 = (
    REPO
    / "documentation/decisions/"
      "0161-record-external-independent-human-review-handoff-"
      "for-cwxr07-s1-corrective-successor-v1.md"
)

if sha(d0161) != EXPECTED_D0161_SHA:
    raise SystemExit(
        "STOP|DECISION0161_SHA_MISMATCH"
    )

if run(
    "git",
    "rev-parse",
    f"HEAD:{HANDOFF_REL}",
) != EXPECTED_HANDOFF_TREE:
    raise SystemExit(
        "STOP|HANDOFF_TREE_CHANGED"
    )

handoff = REPO / HANDOFF_REL

manifest = handoff / "01_external_handoff_manifest.v1.json"
checksum = handoff / "09_external_handoff_v1.SHA256SUMS"

if sha(manifest) != EXPECTED_HANDOFF_MANIFEST_SHA:
    raise SystemExit(
        "STOP|HANDOFF_MANIFEST_SHA_MISMATCH"
    )

if sha(checksum) != EXPECTED_HANDOFF_CHECKSUM_SHA:
    raise SystemExit(
        "STOP|HANDOFF_CHECKSUM_SHA_MISMATCH"
    )

subprocess.check_call(
    [
        "sha256sum",
        "-c",
        checksum.name,
    ],
    cwd=handoff,
    stdout=subprocess.DEVNULL,
)

if not RETURNED.is_file():
    raise SystemExit(
        "STOP|RETURNED_REVIEW_PACKET_NOT_FOUND"
    )

if sha(RETURNED) != EXPECTED_RETURNED_SHA:
    raise SystemExit(
        "STOP|RETURNED_REVIEW_PACKET_SHA_MISMATCH"
    )

if RETURNED.stat().st_size != EXPECTED_RETURNED_SIZE:
    raise SystemExit(
        "STOP|RETURNED_REVIEW_PACKET_SIZE_MISMATCH"
    )

if sha(ORIGINAL_EDITABLE) != EXPECTED_ORIGINAL_EDITABLE_SHA:
    raise SystemExit(
        "STOP|ORIGINAL_EDITABLE_BLANK_CHANGED"
    )

if sha(EXTERNAL_ZIP) != EXPECTED_EXTERNAL_ZIP_SHA:
    raise SystemExit(
        "STOP|EXTERNAL_ZIP_CHANGED"
    )

text = RETURNED.read_text(
    encoding="utf-8"
)

decision = re.search(
    r"^CWXR07-S1 decision:\s*(.+?)\s*$",
    text,
    flags=re.MULTILINE,
)

if not decision:
    raise SystemExit(
        "STOP|CWXR07_S1_DECISION_MISSING"
    )

decision_value = (
    decision.group(1)
    .strip()
    .strip("`")
)

if decision_value != "REVISION_REQUIRED":
    raise SystemExit(
        "STOP|CWXR07_S1_DECISION_NOT_REVISION_REQUIRED"
    )

required = [
    "# CWXR07-S1 Independent Reviewer Packet — Completed Review",
    "Reviewer name: Abdul Raheem Shahzad",
    "Reviewer role: Spec-Technical-Reviewer-1",
    "Reviewer confirmation/signature: ARS",
    "Reviewer attestation:",
    "Review date: 25 / August / 2026",
    "cannot be independently reproduced",
    "sealed Git bundle",
    "Alternatively, narrow CWXR07-S1 further",
    "does **not** certify that an independently observed external process executed A02 exactly once",
]

for marker in required:
    if marker not in text:
        raise SystemExit(
            "STOP|RETURNED_REVIEW_REQUIRED_MARKER_MISSING|"
            + marker
        )

future = REPO / RECORD_REL

if future.exists():
    raise SystemExit(
        "STOP|COMPLETED_HUMAN_REVIEW_RECORD_ALREADY_EXISTS"
    )

print(PASS_MARKER)

print("CURRENT_HEAD=" + head)
print("CURRENT_HEAD_PARENT_DECISION0161_BINDING=PASS")

print("REVIEW_SCOPE=CWXR07-S1_ONLY")
print("CWXR07_S1_DECISION=REVISION_REQUIRED")

print("REVIEWER_NAME=Abdul Raheem Shahzad")
print("REVIEWER_ROLE=Spec-Technical-Reviewer-1")
print("REVIEWER_CONFIRMATION_PRESENT=YES")
print("REVIEWER_ATTESTATION_PRESENT=YES")
print("REVIEW_DATE=25 / August / 2026")

print("RETURNED_REVIEW_PACKET_SHA_BINDING=PASS")
print("ORIGINAL_EDITABLE_BLANK_PRESERVED=YES")
print("EXTERNAL_ZIP_PRESERVED=YES")

print("OVERALL_SUCCESSOR_REVIEW_DECISION_SYNTHESIZED=NO")

print("SUCCESSOR_APPROVED=NO")
print("CORRECTIVE_EVIDENCE_REQUIRED=YES")

print("ACTUAL_PROCESS_EXACTLY_ONCE_FACT_CERTIFIED=NO")
print("GLOBAL_NO_RERUN_FACT_CERTIFIED=NO")
print("REPOSITORY_ASSERTION_PROMOTED_TO_EXTERNAL_FACT=NO")

print("DECISION0160_A02_EXECUTED_BY_THIS_VERIFIER=NO")
print("DECISION0158_A02_EXECUTED_BY_THIS_VERIFIER=NO")
print("DECISION0156_A02_EXECUTED_BY_THIS_VERIFIER=NO")
print("DECISION0154_A02_EXECUTED_BY_THIS_VERIFIER=NO")
print("DECISION0153_A02_EXECUTED_BY_THIS_VERIFIER=NO")
print("DECISION0147_A02_EXECUTED_BY_THIS_VERIFIER=NO")
print("RETIRED_A02_VERIFIERS_EXECUTED=NO")

print("GOVERNANCE_ADOPTION_AUTHORIZED=NO")
print("CORRECTIVE_EVIDENCE_AUTHORING_AUTHORIZED=NO")

print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")

print(
    "VERIFIER_LIFECYCLE="
    "ONE_FINAL_RUN_IMMEDIATELY_BEFORE_RECORDING_GENUINE_"
    "CWXR07_S1_REVISION_REQUIRED_HUMAN_REVIEW_"
    "THEN_PERMANENT_RETIREMENT"
)
