#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import os
import re
import subprocess
import sys

ROOT = Path("/openbayes/home/semanticverify-fuzz-research").resolve()

EXPECTED_DECISION0177_COMMIT = (
    "60ba1d7c907e7d5427216c25155d0528648c7c1e"
)

BASE = Path(
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2"
)

PKG_DIR = BASE / (
    "schema_v2_requirement_to_semantic_unit_"
    "positive_binding_evidence_acquisition_package_v1"
)

AUTH_DIR = BASE / (
    "schema_v2_requirement_to_semantic_unit_"
    "positive_binding_evidence_acquisition_external_handoff_authorization_v1"
)

HANDOFF_DIR = BASE / (
    "schema_v2_requirement_to_semantic_unit_"
    "positive_binding_evidence_acquisition_external_handoff_v1"
)

A01 = ROOT / AUTH_DIR / (
    "01_external_human_positive_binding_evidence_acquisition_"
    "handoff_authorization.v1.json"
)
A02 = ROOT / AUTH_DIR / (
    "02_verify_external_human_positive_binding_evidence_acquisition_"
    "handoff_authoring_authorization.v1.py"
)
A03 = ROOT / AUTH_DIR / (
    "03_external_human_positive_binding_evidence_acquisition_"
    "handoff_authorization.v1.SHA256SUMS"
)

P01 = ROOT / PKG_DIR / "01_package_manifest.v1.json"
P03 = ROOT / PKG_DIR / "03_blank_positive_binding_evidence_packet.v1.md"
P13 = ROOT / PKG_DIR / (
    "13_verify_positive_binding_evidence_acquisition_package_v1.py"
)

DEC0178 = ROOT / (
    "documentation/decisions/"
    "0178-authorize-external-human-positive-binding-"
    "evidence-acquisition-handoff-v1.md"
)

EXTERNAL_ZIP = Path(
    "/openbayes/home/"
    "50_positive_binding_evidence_acquisition_external_handoff.v1.zip"
)

EXTERNAL_PACKET = Path(
    "/openbayes/home/"
    "50_positive_binding_evidence_packet.MANUAL_REVIEW_COPY.v1.md"
)


def stop(msg):
    print("STOP|" + msg)
    sys.exit(178)


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


# At execution time HEAD must be Decision-0178 and its parent Decision-0177.
if git("rev-parse", "HEAD^") != EXPECTED_DECISION0177_COMMIT:
    stop("DECISION0178_PARENT_NOT_DECISION0177")

if git("status", "--porcelain=v1", "--untracked-files=all") != "":
    stop("REPOSITORY_NOT_CLEAN")

for p in (A01, A02, A03, P01, P03, P13, DEC0178):
    if not p.is_file():
        stop("REQUIRED_FILE_MISSING|" + p.name)

if (ROOT / HANDOFF_DIR).exists():
    stop("INTERNAL_HANDOFF_ALREADY_EXISTS")

if EXTERNAL_ZIP.exists():
    stop("EXTERNAL_ZIP_ALREADY_EXISTS")

if EXTERNAL_PACKET.exists():
    stop("EXTERNAL_PACKET_ALREADY_EXISTS")

auth = json.loads(A01.read_text(encoding="utf-8"))
manifest = json.loads(P01.read_text(encoding="utf-8"))
packet = P03.read_text(encoding="utf-8")

if auth.get("artifact") != (
    "external_human_positive_binding_evidence_acquisition_"
    "handoff_authorization_v1"
):
    stop("AUTHORIZATION_ARTIFACT_INVALID")

if auth.get("status") != "AUTHORIZED_NOT_AUTHORED":
    stop("AUTHORIZATION_STATUS_INVALID")

if auth.get("handoff_authoring_authorized") is not True:
    stop("HANDOFF_AUTHORING_NOT_AUTHORIZED")

if auth.get("handoff_authored") is not False:
    stop("HANDOFF_ALREADY_AUTHORED")

if auth.get("external_editable_copy_creation_authorized") is not True:
    stop("EXTERNAL_EDITABLE_COPY_NOT_AUTHORIZED")

if auth.get("external_human_evidence_acquisition_authorized_after_handoff") is not True:
    stop("HUMAN_EVIDENCE_ACQUISITION_NOT_AUTHORIZED")

if auth.get("human_evidence_acquisition_performed") is not False:
    stop("HUMAN_ACQUISITION_ALREADY_PERFORMED")

if auth.get("human_evidence_result_recorded") is not False:
    stop("HUMAN_RESULT_ALREADY_RECORDED")

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

if auth.get("pre_handoff_authoring_verifier_sha256") != sha256_file(A02):
    stop("A02_BINDING_INVALID")

source = auth.get("source_package", {})

pkg_tree = git("rev-parse", f"HEAD:{PKG_DIR.as_posix()}")

if source.get("package_git_tree") != pkg_tree:
    stop("PACKAGE_TREE_BINDING_INVALID")

if source.get("package_manifest_sha256") != sha256_file(P01):
    stop("PACKAGE_MANIFEST_BINDING_INVALID")

if source.get("blank_packet_sha256") != sha256_file(P03):
    stop("BLANK_PACKET_BINDING_INVALID")

if source.get("package_safe_verifier_sha256") != sha256_file(P13):
    stop("PACKAGE_VERIFIER_BINDING_INVALID")

if manifest.get("status") != (
    "AUTHOR_CANDIDATE_BLANK_AWAITING_EXTERNAL_HUMAN_EVIDENCE_ACQUISITION"
):
    stop("SOURCE_PACKAGE_STATUS_INVALID")

blank = manifest.get("blank_state", {})

for key in [
    "human_evidence_acquisition_performed",
    "evidence_states_populated",
    "semantic_unit_proposals_populated",
    "positive_rationales_populated",
    "reviewer_notes_populated",
    "reviewer_identity_populated",
    "reviewer_attestation_populated",
]:
    if blank.get(key) is not False:
        stop("SOURCE_PACKAGE_NOT_BLANK|" + key)

for field in [
    "Human reviewer name:",
    "Human reviewer role:",
    "Human reviewer confirmation/signature:",
    "Human reviewer date:",
    "Human reviewer attestation:",
]:
    if len(re.findall(
        rf"^{re.escape(field)}[ \t]*$",
        packet,
        re.MULTILINE,
    )) != 1:
        stop("REVIEWER_FIELD_NOT_BLANK|" + field)

contract = manifest.get("review_contract", {})

if contract.get("required_reviewer_role") != "Spec-Technical-Reviewer-1":
    stop("REVIEWER_ROLE_INVALID")

if contract.get("allowed_evidence_states") != [
    "POSITIVE_BINDING_PROPOSED",
    "UNRESOLVED_NO_POSITIVE_BINDING_PROPOSED",
]:
    stop("ALLOWED_EVIDENCE_STATES_INVALID")

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

print("EXTERNAL_HUMAN_POSITIVE_BINDING_EVIDENCE_ACQUISITION_HANDOFF_AUTHORIZATION_A02=PASS")
print("SOURCE_PACKAGE_STATUS=AUTHOR_CANDIDATE_BLANK_AWAITING_EXTERNAL_HUMAN_EVIDENCE_ACQUISITION")
print("SOURCE_PACKAGE_BLANK=YES")
print("REQUIRED_REVIEWER_ROLE=Spec-Technical-Reviewer-1")
print("HANDOFF_AUTHORING_AUTHORIZED=YES")
print("HANDOFF_AUTHORED=NO")
print("EXTERNAL_EDITABLE_COPY_CREATION_AUTHORIZED=YES")
print("EXTERNAL_EDITABLE_COPY_CREATED=NO")
print("EXTERNAL_HUMAN_EVIDENCE_ACQUISITION_AUTHORIZED_AFTER_HANDOFF=YES")
print("HUMAN_EVIDENCE_ACQUISITION_PERFORMED=NO")
print("HUMAN_EVIDENCE_RESULT_RECORDED=NO")
print("REVIEWER_IDENTITY_PREFILLED=NO")
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
print("DECISION0178_A02_RESULT=PASS")
