#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import os
import re
import subprocess
import sys

ROOT = Path("/openbayes/home/semanticverify-fuzz-research").resolve()

EXPECTED_PARENT = "4765b028fd8e559944247a1a040117ead67df3c1"

BASE = Path(
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2"
)

ORIGINAL_DIR = BASE / (
    "schema_v2_requirement_to_semantic_unit_crosswalk_evidence_resolution_study_v1_"
    "completed_human_review_record_v1"
)

ORIGINAL_PACKET = ORIGINAL_DIR / (
    "02_CWXR01_CWXR08_returned_reviewer_packet.EXACT_COPY.v1.md"
)

EXPECTED_ORIGINAL_TREE = "b4bb9b57ae25f90c5dc2506a90ade02e810c4388"

S1_DIR = BASE / (
    "schema_v2_requirement_to_semantic_unit_crosswalk_evidence_resolution_study_v1_"
    "cwxr07_lifecycle_evidence_corrective_successor_v1_completed_human_review_record_v1"
)

EXPECTED_S1_TREE = "265da19aca751d98515ddcf7724180d6ebfd2f6e"

S2_SUCCESSOR_DIR = BASE / (
    "schema_v2_requirement_to_semantic_unit_crosswalk_evidence_resolution_study_v1_"
    "cwxr07_s2_narrowed_corrective_successor_v1"
)

EXPECTED_S2_SUCCESSOR_TREE = "e3e8b53823c6c1e132eba5c56a97f726a801f753"

S2_REVIEW_DIR = BASE / (
    "schema_v2_requirement_to_semantic_unit_crosswalk_evidence_resolution_study_v1_"
    "cwxr07_s2_narrowed_corrective_successor_v1_completed_human_review_record_v1"
)

EXPECTED_S2_REVIEW_TREE = "b15036b779a21f0489d1d007f3af8b05b53750f6"

AUTH_DIR = BASE / (
    "schema_v2_requirement_to_semantic_unit_crosswalk_evidence_resolution_study_v1_"
    "cwxr_review_chain_closure_assessment_authorization_v1"
)

A01 = ROOT / AUTH_DIR / "01_review_chain_closure_assessment_authorization.v1.json"
A02 = ROOT / AUTH_DIR / "02_verify_review_chain_closure_assessment_authoring_authorization.v1.py"
A03 = ROOT / AUTH_DIR / "03_review_chain_closure_assessment_authorization.v1.SHA256SUMS"

DEC0172 = ROOT / (
    "documentation/decisions/"
    "0172-authorize-cwxr-review-chain-closure-assessment-after-cwxr07-s2-pass.md"
)


def stop(msg):
    print("STOP|" + msg)
    sys.exit(172)


def git(*args):
    env = os.environ.copy()
    env["GIT_OPTIONAL_LOCKS"] = "0"
    return subprocess.check_output(
        ["git", *args],
        cwd=ROOT,
        env=env,
        text=True,
    ).strip()


def sha256_file(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


# Decision-0172 must be direct child of Decision-0171.
if git("rev-parse", "HEAD^") != EXPECTED_PARENT:
    stop("DECISION0172_PARENT_NOT_DECISION0171")

if git("status", "--porcelain=v1", "--untracked-files=all") != "":
    stop("REPOSITORY_NOT_CLEAN")

if not DEC0172.is_file():
    stop("DECISION0172_FILE_MISSING")

bindings = [
    (ORIGINAL_DIR, EXPECTED_ORIGINAL_TREE, "ORIGINAL_REVIEW"),
    (S1_DIR, EXPECTED_S1_TREE, "S1_REVIEW"),
    (S2_SUCCESSOR_DIR, EXPECTED_S2_SUCCESSOR_TREE, "S2_SUCCESSOR"),
    (S2_REVIEW_DIR, EXPECTED_S2_REVIEW_TREE, "S2_REVIEW"),
]

for rel, expected, label in bindings:
    actual = git("rev-parse", f"HEAD:{rel.as_posix()}")
    if actual != expected:
        stop(label + "_TREE_CHANGED")

text = (ROOT / ORIGINAL_PACKET).read_text(encoding="utf-8")

expected_decisions = {
    "CWXR01": "PASS",
    "CWXR02": "PASS",
    "CWXR03": "PASS",
    "CWXR04": "PASS",
    "CWXR05": "PASS",
    "CWXR06": "PASS",
    "CWXR07": "REVISION_REQUIRED",
    "CWXR08": "PASS",
}

for item, value in expected_decisions.items():
    matches = re.findall(
        rf"^{item} decision:\s*`{re.escape(value)}`\s*$",
        text,
        re.MULTILINE,
    )
    if len(matches) != 1:
        stop("ORIGINAL_REVIEW_DECISION_INVALID|" + item)

overall = re.findall(
    r"^Overall decision:\s*`([^`]+)`\s*$",
    text,
    re.MULTILINE,
)

if overall != ["REVISION_REQUIRED"]:
    stop("ORIGINAL_OVERALL_REVIEW_INVALID")

s2_manifest = json.loads(
    (
        ROOT
        / S2_REVIEW_DIR
        / "01_completed_human_review_manifest.v1.json"
    ).read_text(encoding="utf-8")
)

if s2_manifest.get("review_scope") != "CWXR07-S2_ONLY":
    stop("S2_REVIEW_SCOPE_INVALID")

if s2_manifest.get("review_decision") != "PASS":
    stop("S2_REVIEW_DECISION_INVALID")

if s2_manifest.get("historical_cwxr07_s1_decision") != "REVISION_REQUIRED":
    stop("S2_HISTORICAL_S1_BOUNDARY_INVALID")

if s2_manifest.get("historical_cwxr07_s1_modified") is not False:
    stop("S2_HISTORICAL_S1_MODIFIED")

if s2_manifest.get("historical_cwxr07_s1_upgraded") is not False:
    stop("S2_HISTORICAL_S1_UPGRADED")

if s2_manifest.get("study_governance_adopted") is not False:
    stop("STUDY_ALREADY_GOVERNANCE_ADOPTED")

auth = json.loads(A01.read_text(encoding="utf-8"))

if auth.get("artifact") != "cwxr_review_chain_closure_assessment_authorization_v1":
    stop("AUTHORIZATION_ARTIFACT_INVALID")

if auth.get("status") != "AUTHORIZED_NOT_ASSESSED":
    stop("AUTHORIZATION_STATUS_INVALID")

if auth.get("closure_assessment_authorized") is not True:
    stop("CLOSURE_ASSESSMENT_NOT_AUTHORIZED")

if auth.get("closure_assessment_authored") is not False:
    stop("CLOSURE_ASSESSMENT_ALREADY_AUTHORED")

if auth.get("review_chain_closed") is not False:
    stop("REVIEW_CHAIN_PREMATURELY_CLOSED")

if auth.get("supported_assessment_outcome") != (
    "PASS_CLOSED_WITH_BOUNDED_CWXR07_S2_SUCCESSOR"
):
    stop("SUPPORTED_ASSESSMENT_OUTCOME_INVALID")

if auth.get("governance_adoption_authorized") is not False:
    stop("GOVERNANCE_ADOPTION_PREMATURELY_AUTHORIZED")

if auth.get("study_governance_adopted") is not False:
    stop("STUDY_PREMATURELY_ADOPTED")

if auth.get("analyzer_authorized") is not False:
    stop("ANALYZER_BOUNDARY_INVALID")

if auth.get("baseline_authorized") is not False:
    stop("BASELINE_BOUNDARY_INVALID")

if auth.get("repair_authorized") is not False:
    stop("REPAIR_BOUNDARY_INVALID")

# Validate A03 without executing any other verifier.
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

print("CWXR_REVIEW_CHAIN_CLOSURE_ASSESSMENT_AUTHORIZATION_A02=PASS")
print("ORIGINAL_CWXR07_DECISION=REVISION_REQUIRED")
print("ORIGINAL_OVERALL_REVIEW=REVISION_REQUIRED")
print("CWXR01_TO_CWXR06_AND_CWXR08_PASS_PRESERVED=YES")
print("HISTORICAL_CWXR07_S1_DECISION=REVISION_REQUIRED")
print("CWXR07_S2_DECISION=PASS")
print("CWXR07_S2_BOUNDED_SUCCESSOR=YES")
print("NO_OTHER_ORIGINAL_CWXR_ITEMS_REQUIRE_CORRECTION=YES")
print("CLOSURE_ASSESSMENT_AUTHORIZED=YES")
print("CLOSURE_ASSESSMENT_AUTHORED=NO")
print("REVIEW_CHAIN_CLOSED=NO")
print("SUPPORTED_ASSESSMENT_OUTCOME=PASS_CLOSED_WITH_BOUNDED_CWXR07_S2_SUCCESSOR")
print("STUDY_GOVERNANCE_ADOPTED=NO")
print("GOVERNANCE_ADOPTION_AUTHORIZED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
print("DECISION0172_A02_RESULT=PASS")
