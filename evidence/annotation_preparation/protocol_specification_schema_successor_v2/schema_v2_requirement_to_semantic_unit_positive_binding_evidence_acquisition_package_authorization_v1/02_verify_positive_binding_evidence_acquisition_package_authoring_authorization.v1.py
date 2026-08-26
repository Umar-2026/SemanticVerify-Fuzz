#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import os
import re
import subprocess
import sys

ROOT = Path("/openbayes/home/semanticverify-fuzz-research").resolve()

EXPECTED_DECISION0175_COMMIT = (
    "930cdb7a90a4da2be8a4aef1adbeba57d7b2d4d3"
)

BASE = Path(
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2"
)

AUTH_DIR = BASE / (
    "schema_v2_requirement_to_semantic_unit_"
    "positive_binding_evidence_acquisition_package_authorization_v1"
)

A01 = ROOT / AUTH_DIR / (
    "01_positive_binding_evidence_acquisition_package_authorization.v1.json"
)
A02 = ROOT / AUTH_DIR / (
    "02_verify_positive_binding_evidence_acquisition_package_authoring_"
    "authorization.v1.py"
)
A03 = ROOT / AUTH_DIR / (
    "03_positive_binding_evidence_acquisition_package_authorization.v1.SHA256SUMS"
)

ADOPT_DIR = BASE / (
    "schema_v2_requirement_to_semantic_unit_crosswalk_evidence_resolution_study_v1_"
    "cwxr_closed_review_chain_governance_adoption_v1"
)

G01 = ROOT / ADOPT_DIR / "01_governance_adoption.v1.json"

STUDY_DIR = BASE / (
    "schema_v2_requirement_to_semantic_unit_crosswalk_evidence_resolution_study_v1"
)

PAIR_MATRIX = ROOT / STUDY_DIR / "04_requirement_semantic_unit_pair_matrix.v1.json"

REQ_SRC = ROOT / BASE / (
    "schema_v2_v4_losslessness_requirement_provenance_binding_resolution_study_v1/"
    "01_17_requirement_provenance_binding_matrix.v1.json"
)

UNIT_INV = ROOT / BASE / (
    "schema_v2_exhaustive_admissible_multifield_capability_study_v1/"
    "02_v4_semantic_unit_inventory.v1.json"
)

TRACE_SRC = ROOT / BASE / (
    "schema_v2_semantic_role_relation_formalization_v1/"
    "03_v4_semantic_unit_context_and_leaf_traceability.v1.json"
)

DEC0176 = ROOT / (
    "documentation/decisions/"
    "0176-authorize-positive-requirement-to-semantic-unit-binding-"
    "evidence-acquisition-package-v1.md"
)


def stop(msg):
    print("STOP|" + msg)
    sys.exit(176)


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


if git("rev-parse", "HEAD^") != EXPECTED_DECISION0175_COMMIT:
    stop("DECISION0176_PARENT_NOT_DECISION0175")

if git("status", "--porcelain=v1", "--untracked-files=all") != "":
    stop("REPOSITORY_NOT_CLEAN")

if not DEC0176.is_file():
    stop("DECISION0176_FILE_MISSING")

for p in (A01, A02, A03, G01, PAIR_MATRIX, REQ_SRC, UNIT_INV, TRACE_SRC):
    if not p.is_file():
        stop("REQUIRED_FILE_MISSING|" + p.name)

auth = json.loads(A01.read_text(encoding="utf-8"))
gov = json.loads(G01.read_text(encoding="utf-8"))
pairs = json.loads(PAIR_MATRIX.read_text(encoding="utf-8"))
req = json.loads(REQ_SRC.read_text(encoding="utf-8"))
inv = json.loads(UNIT_INV.read_text(encoding="utf-8"))
trace = json.loads(TRACE_SRC.read_text(encoding="utf-8"))

if auth.get("artifact") != (
    "requirement_to_semantic_unit_positive_binding_"
    "evidence_acquisition_package_authorization_v1"
):
    stop("AUTHORIZATION_ARTIFACT_INVALID")

if auth.get("status") != "AUTHORIZED_NOT_AUTHORED":
    stop("AUTHORIZATION_STATUS_INVALID")

if auth.get("package_authoring_authorized") is not True:
    stop("PACKAGE_AUTHORING_NOT_AUTHORIZED")

if auth.get("package_authored") is not False:
    stop("PACKAGE_ALREADY_AUTHORED")

if auth.get("human_review_executed") is not False:
    stop("HUMAN_REVIEW_PREMATURELY_EXECUTED")

if auth.get("human_review_result_recorded") is not False:
    stop("HUMAN_RESULT_PREMATURELY_RECORDED")

if auth.get("pair_reclassification_authorized") is not False:
    stop("PAIR_RECLASSIFICATION_BOUNDARY_INVALID")

if auth.get("negative_binding_classification_authorized") is not False:
    stop("NEGATIVE_BINDING_BOUNDARY_INVALID")

if auth.get("not_supported_binding_authorized") is not False:
    stop("NOT_SUPPORTED_BOUNDARY_INVALID")

if auth.get("operational_mapping_authorized") is not False:
    stop("OPERATIONAL_MAPPING_BOUNDARY_INVALID")

if auth.get("analyzer_implementation_authorized") is not False:
    stop("ANALYZER_IMPLEMENTATION_BOUNDARY_INVALID")

if auth.get("analyzer_execution_authorized") is not False:
    stop("ANALYZER_EXECUTION_BOUNDARY_INVALID")

if auth.get("baseline_execution_authorized") is not False:
    stop("BASELINE_BOUNDARY_INVALID")

if auth.get("repair_implementation_authorized") is not False:
    stop("REPAIR_IMPLEMENTATION_BOUNDARY_INVALID")

if auth.get("repair_execution_authorized") is not False:
    stop("REPAIR_EXECUTION_BOUNDARY_INVALID")

if auth.get("pre_package_authoring_verifier_sha256") != sha256_file(A02):
    stop("A02_BINDING_INVALID")

if gov.get("study_governance_adopted") is not True:
    stop("STUDY_NOT_GOVERNANCE_ADOPTED")

if gov.get("adopted_bounded_technical_outcome") != \
        "FURTHER_EVIDENCE_REQUIRED":
    stop("GOVERNANCE_OUTCOME_INVALID")

req_records = req.get("records", [])
unit_records = inv.get("semantic_units", [])
trace_records = trace.get("semantic_unit_context_records", [])
pair_records = pairs.get("pairs", [])

if len(req_records) != 17:
    stop("REQUIREMENT_COUNT_INVALID")

if len(unit_records) != 109:
    stop("UNIT_COUNT_INVALID")

if len(trace_records) != 109:
    stop("TRACE_COUNT_INVALID")

if len(pair_records) != 1853:
    stop("PAIR_COUNT_INVALID")

if len({r.get("requirement_id") for r in req_records}) != 17:
    stop("REQUIREMENT_IDENTITY_INVALID")

if len({r.get("unit_id") for r in unit_records}) != 109:
    stop("UNIT_IDENTITY_INVALID")

if {r.get("unit_id") for r in unit_records} != \
        {r.get("unit_id") for r in trace_records}:
    stop("UNIT_TRACEABILITY_IDENTITY_INVALID")

for row in pair_records:
    if row.get("classification") != "UNRESOLVED_BINDING":
        stop("PAIR_ALREADY_RECLASSIFIED")
    if row.get("human_semantic_judgment_used") is not False:
        stop("HUMAN_JUDGMENT_ALREADY_PROMOTED")
    if row.get("positive_binding_claimed") is not False:
        stop("POSITIVE_BINDING_ALREADY_CLAIMED")
    if row.get("negative_binding_exclusion_claimed") is not False:
        stop("NEGATIVE_BINDING_ALREADY_CLAIMED")

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

print("POSITIVE_BINDING_EVIDENCE_ACQUISITION_PACKAGE_AUTHORIZATION_A02=PASS")
print("REQUIREMENT_COUNT=17")
print("SEMANTIC_UNIT_COUNT=109")
print("CURRENT_PAIR_UNIVERSE_COUNT=1853")
print("CURRENT_UNRESOLVED_BINDING_COUNT=1853")
print("DETERMINISTIC_PROVENANCE_ONLY_CROSSWALK_SUPPORTED=NO")
print("NEW_POSITIVE_SEMANTIC_BINDING_EVIDENCE_REQUIRED=YES")
print("PACKAGE_AUTHORING_AUTHORIZED=YES")
print("PACKAGE_AUTHORED=NO")
print("HUMAN_REVIEW_EXECUTED=NO")
print("HUMAN_REVIEW_RESULT_RECORDED=NO")
print("PAIR_RECLASSIFICATION_AUTHORIZED=NO")
print("NEGATIVE_BINDING_CLASSIFICATION_AUTHORIZED=NO")
print("NOT_SUPPORTED_BINDING_AUTHORIZED=NO")
print("OPERATIONAL_MAPPING_AUTHORIZED=NO")
print("SCHEMA_V2_MODIFICATION_AUTHORIZED=NO")
print("SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO")
print("CURL_JSON_AUTHORIZED=NO")
print("ANALYZER_IMPLEMENTATION_AUTHORIZED=NO")
print("ANALYZER_EXECUTION_AUTHORIZED=NO")
print("BASELINE_EXECUTION_AUTHORIZED=NO")
print("REPAIR_IMPLEMENTATION_AUTHORIZED=NO")
print("REPAIR_EXECUTION_AUTHORIZED=NO")
print("DECISION0176_A02_RESULT=PASS")
