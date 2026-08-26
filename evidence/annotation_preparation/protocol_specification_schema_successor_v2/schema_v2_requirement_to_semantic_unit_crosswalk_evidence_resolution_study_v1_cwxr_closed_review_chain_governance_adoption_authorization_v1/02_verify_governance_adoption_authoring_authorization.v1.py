#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import os
import re
import subprocess
import sys

ROOT = Path("/openbayes/home/semanticverify-fuzz-research").resolve()

EXPECTED_DECISION0173_COMMIT = (
    "dc803658410240de51c6ccf2d21d8ff219030927"
)

BASE = Path(
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2"
)

CLOSURE_DIR = BASE / (
    "schema_v2_requirement_to_semantic_unit_crosswalk_evidence_resolution_study_v1_"
    "cwxr_review_chain_closure_assessment_v1"
)

STUDY_DIR = BASE / (
    "schema_v2_requirement_to_semantic_unit_crosswalk_evidence_resolution_study_v1"
)

AUTH_DIR = BASE / (
    "schema_v2_requirement_to_semantic_unit_crosswalk_evidence_resolution_study_v1_"
    "cwxr_closed_review_chain_governance_adoption_authorization_v1"
)

A01 = ROOT / AUTH_DIR / "01_governance_adoption_authorization.v1.json"
A02 = ROOT / AUTH_DIR / "02_verify_governance_adoption_authoring_authorization.v1.py"
A03 = ROOT / AUTH_DIR / "03_governance_adoption_authorization.v1.SHA256SUMS"

C01 = ROOT / CLOSURE_DIR / "01_review_chain_closure_assessment.v1.json"
STUDY_MANIFEST = ROOT / STUDY_DIR / "01_study_manifest.v1.json"

DEC0174 = ROOT / (
    "documentation/decisions/"
    "0174-authorize-governance-adoption-of-closed-cwxr-review-chain-and-bounded-study-v1-outcome.md"
)


def stop(msg):
    print("STOP|" + msg)
    sys.exit(174)


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


def contains_value(value, target):
    if isinstance(value, dict):
        return any(contains_value(v, target) for v in value.values())
    if isinstance(value, list):
        return any(contains_value(v, target) for v in value)
    return value == target


# Decision-0174 must be the direct child of Decision-0173.
if git("rev-parse", "HEAD^") != EXPECTED_DECISION0173_COMMIT:
    stop("DECISION0174_PARENT_NOT_DECISION0173")

if git("status", "--porcelain=v1", "--untracked-files=all") != "":
    stop("REPOSITORY_NOT_CLEAN")

if not DEC0174.is_file():
    stop("DECISION0174_FILE_MISSING")

for p in (A01, A02, A03, C01, STUDY_MANIFEST):
    if not p.is_file():
        stop("REQUIRED_ARTIFACT_MISSING|" + p.name)

auth = json.loads(A01.read_text(encoding="utf-8"))

if auth.get("artifact") != (
    "cwxr_closed_review_chain_governance_adoption_authorization_v1"
):
    stop("AUTHORIZATION_ARTIFACT_INVALID")

if auth.get("status") != "AUTHORIZED_NOT_ADOPTED":
    stop("AUTHORIZATION_STATUS_INVALID")

if auth.get("source_review_chain", {}).get("review_chain_closed") is not True:
    stop("SOURCE_REVIEW_CHAIN_NOT_CLOSED")

if auth.get("source_review_chain", {}).get("closure_outcome") != (
    "PASS_CLOSED_WITH_BOUNDED_CWXR07_S2_SUCCESSOR"
):
    stop("SOURCE_CLOSURE_OUTCOME_INVALID")

if auth.get("source_review_chain", {}).get(
    "original_cwxr07_decision"
) != "REVISION_REQUIRED":
    stop("ORIGINAL_CWXR07_HISTORY_INVALID")

if auth.get("source_review_chain", {}).get(
    "original_overall_review"
) != "REVISION_REQUIRED":
    stop("ORIGINAL_OVERALL_HISTORY_INVALID")

if auth.get("source_review_chain", {}).get(
    "historical_cwxr07_s1_decision"
) != "REVISION_REQUIRED":
    stop("HISTORICAL_S1_INVALID")

if auth.get("source_review_chain", {}).get(
    "cwxr07_s2_decision"
) != "PASS":
    stop("S2_DECISION_INVALID")

if auth.get("bounded_study_v1_outcome") != "FURTHER_EVIDENCE_REQUIRED":
    stop("BOUNDED_STUDY_OUTCOME_INVALID")

if auth.get("governance_adoption_authorized") is not True:
    stop("GOVERNANCE_ADOPTION_NOT_AUTHORIZED")

if auth.get("governance_adoption_authored") is not False:
    stop("GOVERNANCE_ADOPTION_ALREADY_AUTHORED")

if auth.get("study_governance_adopted") is not False:
    stop("STUDY_ALREADY_ADOPTED")

if auth.get("pair_reclassification_authorized") is not False:
    stop("PAIR_RECLASSIFICATION_BOUNDARY_INVALID")

if auth.get("operational_mapping_authorized") is not False:
    stop("OPERATIONAL_MAPPING_BOUNDARY_INVALID")

if auth.get("schema_v2_modification_authorized") is not False:
    stop("SCHEMA_V2_BOUNDARY_INVALID")

if auth.get("schema_successor_authoring_authorized") is not False:
    stop("SCHEMA_SUCCESSOR_BOUNDARY_INVALID")

if auth.get("curl_json_authorized") is not False:
    stop("CURL_JSON_BOUNDARY_INVALID")

if auth.get("analyzer_authorized") is not False:
    stop("ANALYZER_BOUNDARY_INVALID")

if auth.get("baseline_authorized") is not False:
    stop("BASELINE_BOUNDARY_INVALID")

if auth.get("repair_authorized") is not False:
    stop("REPAIR_BOUNDARY_INVALID")

if auth.get("pre_governance_adoption_verifier_sha256") != sha256_file(A02):
    stop("A02_BINDING_INVALID")

closure_tree = git("rev-parse", f"HEAD:{CLOSURE_DIR.as_posix()}")

if closure_tree != auth.get("source_review_chain", {}).get(
    "closure_git_tree"
):
    stop("CLOSURE_TREE_BINDING_INVALID")

study_tree = git("rev-parse", f"HEAD:{STUDY_DIR.as_posix()}")

if study_tree != auth.get("source_study_v1", {}).get("git_tree"):
    stop("STUDY_TREE_BINDING_INVALID")

if sha256_file(STUDY_MANIFEST) != auth.get(
    "source_study_v1", {}
).get("manifest_sha256"):
    stop("STUDY_MANIFEST_BINDING_INVALID")

closure = json.loads(C01.read_text(encoding="utf-8"))

if closure.get("review_chain_closed") is not True:
    stop("CLOSURE_RECORD_NOT_CLOSED")

if closure.get("closure_outcome") != (
    "PASS_CLOSED_WITH_BOUNDED_CWXR07_S2_SUCCESSOR"
):
    stop("CLOSURE_RECORD_OUTCOME_INVALID")

if closure.get("study_governance_adopted") is not False:
    stop("CLOSURE_RECORD_ALREADY_ADOPTED")

study = json.loads(STUDY_MANIFEST.read_text(encoding="utf-8"))

if not contains_value(study, "AUTHOR_CANDIDATE"):
    stop("STUDY_AUTHOR_CANDIDATE_NOT_FOUND")

if not contains_value(study, "FURTHER_EVIDENCE_REQUIRED"):
    stop("STUDY_BOUNDED_OUTCOME_NOT_FOUND")

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

print("CWXR_CLOSED_CHAIN_GOVERNANCE_ADOPTION_AUTHORIZATION_A02=PASS")
print("REVIEW_CHAIN_CLOSED=YES")
print("CLOSURE_OUTCOME=PASS_CLOSED_WITH_BOUNDED_CWXR07_S2_SUCCESSOR")
print("ORIGINAL_CWXR07_REMAINS=REVISION_REQUIRED")
print("ORIGINAL_OVERALL_REVIEW_REMAINS=REVISION_REQUIRED")
print("HISTORICAL_CWXR07_S1_REMAINS=REVISION_REQUIRED")
print("CWXR07_S2_DECISION=PASS")
print("STUDY_STATUS=AUTHOR_CANDIDATE")
print("BOUNDED_STUDY_V1_OUTCOME=FURTHER_EVIDENCE_REQUIRED")
print("GOVERNANCE_ADOPTION_AUTHORIZED=YES")
print("GOVERNANCE_ADOPTION_AUTHORED=NO")
print("STUDY_GOVERNANCE_ADOPTED=NO")
print("PAIR_RECLASSIFICATION_AUTHORIZED=NO")
print("OPERATIONAL_MAPPING_AUTHORIZED=NO")
print("SCHEMA_V2_MODIFICATION_AUTHORIZED=NO")
print("SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO")
print("CURL_JSON_AUTHORIZED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
print("DECISION0174_A02_RESULT=PASS")
