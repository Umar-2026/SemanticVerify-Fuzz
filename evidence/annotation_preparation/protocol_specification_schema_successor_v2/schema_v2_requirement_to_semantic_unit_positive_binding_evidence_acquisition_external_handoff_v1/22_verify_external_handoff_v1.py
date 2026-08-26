#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parent

MANIFEST = ROOT / "01_external_handoff_manifest.v1.json"
PACKET = ROOT / "04_blank_positive_binding_evidence_packet.EXACT_COPY.v1.md"
CHECKSUMS = ROOT / "23_external_handoff_v1.SHA256SUMS"
A02_OUTPUT = ROOT / "20_decision0178_a02_final_output.EXACT_COPY.v1.txt"
CONSUMPTION = ROOT / "21_decision0178_a02_consumption_record.v1.json"


def stop(msg):
    print("STOP|" + msg)
    sys.exit(1)


def sha256_file(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


files = sorted(p for p in ROOT.iterdir() if p.is_file())

if len(files) != 23:
    stop("HANDOFF_FILE_COUNT_INVALID")

entries = []

for line in CHECKSUMS.read_text(encoding="utf-8").splitlines():
    if not line.strip():
        continue

    m = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)

    if not m:
        stop("CHECKSUM_FORMAT_INVALID")

    entries.append((m.group(1), m.group(2)))

if len(entries) != 22:
    stop("CHECKSUM_ENTRY_COUNT_INVALID")

expected_names = {
    p.name for p in files
    if p.name != CHECKSUMS.name
}

if {name for _, name in entries} != expected_names:
    stop("CHECKSUM_NAME_SET_INVALID")

for expected, name in entries:
    p = ROOT / name

    if not p.is_file():
        stop("CHECKSUM_TARGET_MISSING|" + name)

    if sha256_file(p) != expected:
        stop("CHECKSUM_MISMATCH|" + name)

obj = json.loads(MANIFEST.read_text(encoding="utf-8"))

if obj.get("artifact") != (
    "external_human_positive_binding_evidence_acquisition_handoff_v1"
):
    stop("MANIFEST_ARTIFACT_INVALID")

if obj.get("status") != (
    "HANDOFF_AUTHORED_AWAITING_EXTERNAL_HUMAN_EVIDENCE_ACQUISITION"
):
    stop("HANDOFF_STATUS_INVALID")

source = obj.get("source_package", {})

if source.get("status") != (
    "AUTHOR_CANDIDATE_BLANK_AWAITING_EXTERNAL_HUMAN_EVIDENCE_ACQUISITION"
):
    stop("SOURCE_PACKAGE_STATUS_INVALID")

if source.get("requirement_count") != 17:
    stop("REQUIREMENT_COUNT_INVALID")

if source.get("semantic_unit_count") != 109:
    stop("SEMANTIC_UNIT_COUNT_INVALID")

if source.get("pair_universe_count") != 1853:
    stop("PAIR_UNIVERSE_INVALID")

if source.get("current_unresolved_binding_count") != 1853:
    stop("UNRESOLVED_BINDING_COUNT_INVALID")

copy_hashes = obj.get("exact_copy_sha256", {})

for name, expected in copy_hashes.items():
    p = ROOT / name

    if not p.is_file():
        stop("EXACT_COPY_MISSING|" + name)

    if sha256_file(p) != expected:
        stop("EXACT_COPY_HASH_MISMATCH|" + name)

packet = PACKET.read_text(encoding="utf-8")

if len(re.findall(r"^## Requirement \d{2}$", packet, re.MULTILINE)) != 17:
    stop("PACKET_REQUIREMENT_SECTION_COUNT_INVALID")

for field in [
    "Evidence state:",
    "Proposed semantic-unit IDs:",
    "Positive-binding rationale:",
    "Reviewer notes:",
]:
    if len(re.findall(
        rf"^{re.escape(field)}[ \t]*$",
        packet,
        re.MULTILINE,
    )) != 17:
        stop("PACKET_FIELD_NOT_BLANK|" + field)

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

contract = obj.get("human_evidence_contract", {})

if contract.get("required_reviewer_role") != "Spec-Technical-Reviewer-1":
    stop("REVIEWER_ROLE_INVALID")

if contract.get("allowed_evidence_states") != [
    "POSITIVE_BINDING_PROPOSED",
    "UNRESOLVED_NO_POSITIVE_BINDING_PROPOSED",
]:
    stop("ALLOWED_EVIDENCE_STATES_INVALID")

for key in [
    "negative_binding_judgment_allowed",
    "not_supported_binding_allowed",
    "mapping_impossibility_judgment_allowed",
    "reviewer_identity_prefilled",
    "reviewer_binding_proposals_prefilled",
    "reviewer_rationale_prefilled",
    "reviewer_attestation_prefilled",
]:
    if contract.get(key) is not False:
        stop("HUMAN_CONTRACT_BOUNDARY_INVALID|" + key)

a02 = obj.get("decision0178_a02", {})

if a02.get("execution_count_in_decision0179_transaction") != 1:
    stop("A02_EXECUTION_COUNT_INVALID")

if a02.get("state") != "PERMANENTLY_RETIRED":
    stop("A02_STATE_INVALID")

if a02.get("rerun_authorized") is not False:
    stop("A02_RERUN_INVALID")

if a02.get("global_no_rerun_fact_independently_certified") is not False:
    stop("GLOBAL_NO_RERUN_OVERCLAIM")

if "DECISION0178_A02_RESULT=PASS" not in \
        A02_OUTPUT.read_text(encoding="utf-8").splitlines():
    stop("A02_PASS_MARKER_MISSING")

consumption = json.loads(CONSUMPTION.read_text(encoding="utf-8"))

if consumption.get("execution_count_in_decision0179_transaction") != 1:
    stop("CONSUMPTION_EXECUTION_COUNT_INVALID")

if consumption.get("return_code") != 0:
    stop("CONSUMPTION_RETURN_CODE_INVALID")

if consumption.get("pass_marker_present") is not True:
    stop("CONSUMPTION_PASS_MARKER_INVALID")

if consumption.get("lifecycle_after_execution") != "PERMANENTLY_RETIRED":
    stop("CONSUMPTION_STATE_INVALID")

if consumption.get("rerun_authorized") is not False:
    stop("CONSUMPTION_RERUN_INVALID")

if consumption.get("other_a02_executed_in_this_transaction") is not False:
    stop("OTHER_A02_EXECUTED")

delivery = obj.get("external_delivery_contract", {})

if delivery.get("editable_packet_initially_exact_internal_blank") is not True:
    stop("EDITABLE_INITIAL_BINDING_INVALID")

if delivery.get("editable_packet_is_only_human_editable_surface") is not True:
    stop("EDITABLE_SURFACE_BOUNDARY_INVALID")

if obj.get("handoff_authored") is not True:
    stop("HANDOFF_NOT_AUTHORED")

if obj.get("external_human_evidence_acquisition_authorized") is not True:
    stop("EXTERNAL_HUMAN_ACQUISITION_NOT_AUTHORIZED")

if obj.get("human_evidence_acquisition_performed") is not False:
    stop("HUMAN_EVIDENCE_PREMATURELY_PERFORMED")

if obj.get("human_evidence_result_recorded") is not False:
    stop("HUMAN_RESULT_PREMATURELY_RECORDED")

for key in [
    "pair_reclassification_authorized",
    "historical_pair_reclassification_authorized",
    "negative_binding_classification_authorized",
    "not_supported_binding_authorized",
    "operational_mapping_authorized",
    "schema_v2_modification_authorized",
    "schema_successor_authoring_authorized",
    "curl_json_authorized",
    "analyzer_implementation_authorized",
    "analyzer_execution_authorized",
    "baseline_execution_authorized",
    "repair_implementation_authorized",
    "repair_execution_authorized",
]:
    if obj.get(key) is not False:
        stop("BOUNDARY_INVALID|" + key)

print("EXTERNAL_HUMAN_POSITIVE_BINDING_EVIDENCE_ACQUISITION_HANDOFF_V1=PASS")
print("HANDOFF_STATUS=HANDOFF_AUTHORED_AWAITING_EXTERNAL_HUMAN_EVIDENCE_ACQUISITION")
print("SOURCE_PACKAGE_BLANK=YES")
print("REQUIREMENT_COUNT=17")
print("SEMANTIC_UNIT_COUNT=109")
print("PAIR_UNIVERSE_COUNT=1853")
print("CURRENT_UNRESOLVED_BINDING_COUNT=1853")
print("INTERNAL_BLANK_PACKET=PASS")
print("REVIEWER_IDENTITY_PREFILLED=NO")
print("BINDING_PROPOSALS_PREFILLED=NO")
print("NEGATIVE_BINDING_JUDGMENT_AUTHORIZED=NO")
print("NOT_SUPPORTED_BINDING_AUTHORIZED=NO")
print("DECISION0178_A02_STATE=PERMANENTLY_RETIRED")
print("DECISION0178_A02_RERUN_AUTHORIZED=NO")
print("EXTERNAL_HUMAN_EVIDENCE_ACQUISITION_AUTHORIZED=YES")
print("HUMAN_EVIDENCE_ACQUISITION_PERFORMED=NO")
print("HUMAN_EVIDENCE_RESULT_RECORDED=NO")
print("PAIR_RECLASSIFICATION_AUTHORIZED=NO")
print("OPERATIONAL_MAPPING_AUTHORIZED=NO")
print("ANALYZER_IMPLEMENTATION_AUTHORIZED=NO")
print("ANALYZER_EXECUTION_AUTHORIZED=NO")
print("BASELINE_EXECUTION_AUTHORIZED=NO")
print("REPAIR_IMPLEMENTATION_AUTHORIZED=NO")
print("REPAIR_EXECUTION_AUTHORIZED=NO")
print("INTERNAL_HANDOFF_SAFE_VERIFICATION=PASS")
