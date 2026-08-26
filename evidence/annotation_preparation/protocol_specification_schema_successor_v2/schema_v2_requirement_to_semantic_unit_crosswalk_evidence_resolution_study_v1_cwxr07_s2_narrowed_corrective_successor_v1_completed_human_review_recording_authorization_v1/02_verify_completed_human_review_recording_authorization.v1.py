#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import os
import re
import subprocess
import sys

ROOT = Path("/openbayes/home/semanticverify-fuzz-research").resolve()

RETURNED = Path(
    "/openbayes/home/"
    "50_CWXR07_S2_Manually_reviewer_packet.MANUAL_REVIEW_COPY.v1.md"
)

ORIGINAL_BLANK = Path(
    "/openbayes/home/"
    "50_CWXR07_S2_reviewer_packet.MANUAL_REVIEW_COPY.v1.md"
)

EXPECTED_RETURNED_SHA = (
    "ad86241de11df01b65dd309097757e2f90c09f4ad08754dea680227fefde4da5"
)
EXPECTED_RETURNED_SIZE = 2803

EXPECTED_BLANK_SHA = (
    "ad5333e4687a285f7fb87ce1ab427e25b4d00c8fa513b1f9ee1ae116c0fad5a2"
)
EXPECTED_BLANK_SIZE = 1555

EXPECTED_DECISION0169_COMMIT = (
    "71e0469d4e971c283874d06fb48d3ec8fed1c164"
)

HANDOFF_DIR_REL = (
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2/"
    "schema_v2_requirement_to_semantic_unit_crosswalk_evidence_resolution_study_v1_"
    "cwxr07_s2_narrowed_corrective_successor_v1_external_handoff_v1"
)

EXPECTED_HANDOFF_TREE = (
    "122f65c1130d2e9b0f5e4cba67cea5f18a98369c"
)

AUTH_DIR_REL = (
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2/"
    "schema_v2_requirement_to_semantic_unit_crosswalk_evidence_resolution_study_v1_"
    "cwxr07_s2_narrowed_corrective_successor_v1_"
    "completed_human_review_recording_authorization_v1"
)

A01 = ROOT / AUTH_DIR_REL / "01_completed_human_review_recording_authorization.v1.json"
A02 = ROOT / AUTH_DIR_REL / "02_verify_completed_human_review_recording_authorization.v1.py"
A03 = ROOT / AUTH_DIR_REL / "03_completed_human_review_recording_authorization.v1.SHA256SUMS"

DEC0170_REL = (
    "documentation/decisions/"
    "0170-authorize-recording-of-genuine-cwxr07-s2-pass-human-review.md"
)


def stop(msg):
    print("STOP|" + msg)
    sys.exit(170)


def sha256_file(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def git(*args):
    env = os.environ.copy()
    env["GIT_OPTIONAL_LOCKS"] = "0"
    return subprocess.check_output(
        ["git", *args],
        cwd=ROOT,
        env=env,
        text=True,
    ).strip()


# This verifier is valid only at the Decision-0170 checkpoint:
# Decision-0170 must be the direct child of Decision-0169.
if git("rev-parse", "HEAD^") != EXPECTED_DECISION0169_COMMIT:
    stop("DECISION0170_PARENT_NOT_DECISION0169")

if git("status", "--porcelain=v1", "--untracked-files=all") != "":
    stop("REPOSITORY_NOT_CLEAN")

if not (ROOT / DEC0170_REL).is_file():
    stop("DECISION0170_FILE_MISSING")

handoff_tree = git("rev-parse", f"HEAD:{HANDOFF_DIR_REL}")
if handoff_tree != EXPECTED_HANDOFF_TREE:
    stop("HANDOFF_TREE_CHANGED")

if not RETURNED.is_file():
    stop("RETURNED_REVIEW_MISSING")

if sha256_file(RETURNED) != EXPECTED_RETURNED_SHA:
    stop("RETURNED_REVIEW_HASH_CHANGED")

if RETURNED.stat().st_size != EXPECTED_RETURNED_SIZE:
    stop("RETURNED_REVIEW_SIZE_CHANGED")

if not ORIGINAL_BLANK.is_file():
    stop("ORIGINAL_BLANK_MISSING")

if sha256_file(ORIGINAL_BLANK) != EXPECTED_BLANK_SHA:
    stop("ORIGINAL_BLANK_HASH_CHANGED")

if ORIGINAL_BLANK.stat().st_size != EXPECTED_BLANK_SIZE:
    stop("ORIGINAL_BLANK_SIZE_CHANGED")

for p in (A01, A02, A03):
    if not p.is_file():
        stop("AUTHORIZATION_ARTIFACT_MISSING|" + p.name)

# Verify A03 closure without invoking any other verifier.
entries = []
for line in A03.read_text(encoding="utf-8").splitlines():
    if not line.strip():
        continue
    m = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
    if not m:
        stop("AUTHORIZATION_CHECKSUM_FORMAT_INVALID")
    entries.append((m.group(1), m.group(2)))

if len(entries) != 2:
    stop("AUTHORIZATION_CHECKSUM_ENTRY_COUNT_INVALID")

for expected, name in entries:
    target = A03.parent / name
    if not target.is_file():
        stop("AUTHORIZATION_CHECKSUM_TARGET_MISSING|" + name)
    if sha256_file(target) != expected:
        stop("AUTHORIZATION_CHECKSUM_MISMATCH|" + name)

auth = json.loads(A01.read_text(encoding="utf-8"))

if auth.get("artifact") != "cwxr07_s2_completed_human_review_recording_authorization_v1":
    stop("A01_ARTIFACT_ID_INVALID")

if auth.get("review_scope") != "CWXR07-S2_ONLY":
    stop("A01_SCOPE_INVALID")

if auth.get("returned_review", {}).get("sha256") != EXPECTED_RETURNED_SHA:
    stop("A01_RETURNED_REVIEW_BINDING_INVALID")

if auth.get("returned_review", {}).get("decision") != "PASS":
    stop("A01_RETURNED_DECISION_INVALID")

if auth.get("historical_cwxr07_s1_decision") != "REVISION_REQUIRED":
    stop("A01_HISTORICAL_S1_INVALID")

if auth.get("recording_verifier_sha256") != sha256_file(A02):
    stop("A01_A02_BINDING_INVALID")

if auth.get("governance_adoption_authorized") is not False:
    stop("A01_GOVERNANCE_BOUNDARY_INVALID")

if auth.get("analyzer_authorized") is not False:
    stop("A01_ANALYZER_BOUNDARY_INVALID")

if auth.get("baseline_authorized") is not False:
    stop("A01_BASELINE_BOUNDARY_INVALID")

if auth.get("repair_authorized") is not False:
    stop("A01_REPAIR_BOUNDARY_INVALID")

text = RETURNED.read_text(encoding="utf-8")

required_exact = [
    "CWXR07-S2 decision: PASS",
    "Reviewer name: Abdul Raheem Shahzad",
    "Reviewer role: Spec-Technical-Reviewer-1",
    "Reviewer confirmation/signature: ARS",
    "Review date: 25 / August / 2026",
]

for value in required_exact:
    if text.count(value) != 1:
        stop("RETURNED_REVIEW_EXACT_FIELD_BINDING_FAILED|" + value)

att_match = re.search(
    r"^Reviewer attestation:[ \t]*(.+)$",
    text,
    re.MULTILINE,
)

if not att_match:
    stop("REVIEWER_ATTESTATION_MISSING")

att = att_match.group(1)

if not re.search(r"reviewed\s+only\s+CWXR07-S2", att, re.I):
    stop("REVIEWER_ATTESTATION_SCOPE_INVALID")

if not re.search(r"CWXR07-S1\s+remains\s+REVISION_REQUIRED", text, re.I):
    stop("HISTORICAL_S1_BOUNDARY_NOT_PRESERVED")

print("CWXR07_S2_COMPLETED_REVIEW_RECORDING_AUTHORIZATION_A02=PASS")
print("REVIEW_SCOPE=CWXR07-S2_ONLY")
print("GENUINE_RETURNED_HUMAN_REVIEW_BOUND=YES")
print("CWXR07_S2_DECISION=PASS")
print("REVIEWER_NAME=Abdul Raheem Shahzad")
print("REVIEWER_ROLE=Spec-Technical-Reviewer-1")
print("REVIEWER_CONFIRMATION=ARS")
print("REVIEW_DATE=25 / August / 2026")
print("HISTORICAL_CWXR07_S1_DECISION=REVISION_REQUIRED")
print("HISTORICAL_CWXR07_S1_MODIFIED=NO")
print("REVIEWER_DECISION_SYNTHESIZED=NO")
print("REVIEWER_IDENTITY_SYNTHESIZED=NO")
print("RECORDING_AUTHORIZED=YES")
print("COMPLETED_REVIEW_RECORD_AUTHORED=NO")
print("GOVERNANCE_ADOPTION_AUTHORIZED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
print("DECISION0170_A02_RESULT=PASS")
