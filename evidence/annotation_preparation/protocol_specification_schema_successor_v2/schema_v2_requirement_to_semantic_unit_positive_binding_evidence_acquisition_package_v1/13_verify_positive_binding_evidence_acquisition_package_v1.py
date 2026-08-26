#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parent

FILES = {
    "manifest": ROOT / "01_package_manifest.v1.json",
    "instructions": ROOT / "02_evidence_reviewer_instructions.v1.md",
    "packet": ROOT / "03_blank_positive_binding_evidence_packet.v1.md",
    "index": ROOT / "04_semantic_unit_neutral_index.v1.md",
    "requirements": ROOT / "05_requirement_provenance.EXACT_COPY.v1.json",
    "units": ROOT / "06_semantic_unit_inventory.EXACT_COPY.v1.json",
    "trace": ROOT / "07_semantic_unit_traceability.EXACT_COPY.v1.json",
    "governance": ROOT / "08_governance_adoption.EXACT_COPY.v1.json",
    "authorization": ROOT / "09_decision0176_authorization.EXACT_COPY.v1.json",
    "decision": ROOT / "10_decision0176.EXACT_COPY.v1.md",
    "a02_output": ROOT / "11_decision0176_a02_final_output.EXACT_COPY.v1.txt",
    "consumption": ROOT / "12_decision0176_a02_consumption_record.v1.json",
    "verifier": ROOT / "13_verify_positive_binding_evidence_acquisition_package_v1.py",
    "checksums": ROOT / "14_positive_binding_evidence_acquisition_package_v1.SHA256SUMS",
}


def stop(msg):
    print("STOP|" + msg)
    sys.exit(1)


def sha256_file(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


for name, path in FILES.items():
    if not path.is_file():
        stop("PACKAGE_FILE_MISSING|" + name)

entries = []

for line in FILES["checksums"].read_text(encoding="utf-8").splitlines():
    if not line.strip():
        continue

    m = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)

    if not m:
        stop("CHECKSUM_FORMAT_INVALID")

    entries.append((m.group(1), m.group(2)))

if len(entries) != 13:
    stop("CHECKSUM_ENTRY_COUNT_INVALID")

expected_names = {
    p.name
    for key, p in FILES.items()
    if key != "checksums"
}

if {name for _, name in entries} != expected_names:
    stop("CHECKSUM_NAME_SET_INVALID")

for expected, name in entries:
    p = ROOT / name
    if sha256_file(p) != expected:
        stop("CHECKSUM_MISMATCH|" + name)

manifest = json.loads(FILES["manifest"].read_text(encoding="utf-8"))

if manifest.get("artifact") != (
    "positive_requirement_to_semantic_unit_binding_"
    "evidence_acquisition_package_v1"
):
    stop("MANIFEST_ARTIFACT_INVALID")

if manifest.get("status") != (
    "AUTHOR_CANDIDATE_BLANK_AWAITING_EXTERNAL_HUMAN_EVIDENCE_ACQUISITION"
):
    stop("PACKAGE_STATUS_INVALID")

bindings = manifest.get("source_domain_bindings", {})

if bindings.get("requirement_count") != 17:
    stop("REQUIREMENT_COUNT_INVALID")

if bindings.get("semantic_unit_count") != 109:
    stop("SEMANTIC_UNIT_COUNT_INVALID")

if bindings.get("pair_universe_count") != 1853:
    stop("PAIR_UNIVERSE_INVALID")

if bindings.get("current_unresolved_binding_count") != 1853:
    stop("UNRESOLVED_BINDING_COUNT_INVALID")

content = manifest.get("package_content", {})

copy_checks = [
    ("requirements", "requirement_provenance_exact_copy_sha256"),
    ("units", "semantic_unit_inventory_exact_copy_sha256"),
    ("trace", "semantic_unit_traceability_exact_copy_sha256"),
    ("governance", "governance_adoption_exact_copy_sha256"),
    ("authorization", "decision0176_authorization_exact_copy_sha256"),
    ("decision", "decision0176_exact_copy_sha256"),
    ("a02_output", "decision0176_a02_final_output_sha256"),
    ("consumption", "decision0176_a02_consumption_record_sha256"),
]

for file_key, manifest_key in copy_checks:
    if sha256_file(FILES[file_key]) != content.get(manifest_key):
        stop("MANIFEST_COPY_BINDING_INVALID|" + file_key)

req = json.loads(FILES["requirements"].read_text(encoding="utf-8"))
inv = json.loads(FILES["units"].read_text(encoding="utf-8"))
trace = json.loads(FILES["trace"].read_text(encoding="utf-8"))

req_records = req.get("records", [])
unit_records = inv.get("semantic_units", [])
trace_records = trace.get("semantic_unit_context_records", [])

if len(req_records) != 17:
    stop("SOURCE_REQUIREMENT_COUNT_INVALID")

if len(unit_records) != 109:
    stop("SOURCE_UNIT_COUNT_INVALID")

if len(trace_records) != 109:
    stop("SOURCE_TRACE_COUNT_INVALID")

if {x.get("unit_id") for x in unit_records} != \
        {x.get("unit_id") for x in trace_records}:
    stop("UNIT_TRACEABILITY_IDENTITY_MISMATCH")

packet = FILES["packet"].read_text(encoding="utf-8")

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

raw_ids = re.findall(
    r"^Requirement ID \(exact\): (.+)$",
    packet,
    re.MULTILINE,
)

if len(raw_ids) != 17:
    stop("PACKET_REQUIREMENT_IDS_INVALID")

packet_ids = [json.loads(x) for x in raw_ids]
source_ids = [x.get("requirement_id") for x in req_records]

if packet_ids != source_ids:
    stop("PACKET_REQUIREMENT_ORDER_INVALID")

if "NOT_SUPPORTED_BINDING:" in packet:
    stop("NEGATIVE_CLASSIFICATION_FIELD_PRESENT")

if "Negative binding decision:" in packet:
    stop("NEGATIVE_DECISION_FIELD_PRESENT")

review_contract = manifest.get("review_contract", {})

if review_contract.get("negative_binding_judgment_allowed") is not False:
    stop("NEGATIVE_JUDGMENT_BOUNDARY_INVALID")

if review_contract.get("not_supported_binding_allowed") is not False:
    stop("NOT_SUPPORTED_BOUNDARY_INVALID")

if review_contract.get("author_candidate_preselection_present") is not False:
    stop("AUTHOR_PRESELECTION_BOUNDARY_INVALID")

if review_contract.get("model_candidate_preselection_present") is not False:
    stop("MODEL_PRESELECTION_BOUNDARY_INVALID")

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
        stop("BLANK_STATE_INVALID|" + key)

a02 = manifest.get("decision0176_a02", {})

if a02.get("execution_count_in_decision0177_transaction") != 1:
    stop("A02_EXECUTION_COUNT_INVALID")

if a02.get("state") != "PERMANENTLY_RETIRED":
    stop("A02_STATE_INVALID")

if a02.get("rerun_authorized") is not False:
    stop("A02_RERUN_INVALID")

consumption = json.loads(
    FILES["consumption"].read_text(encoding="utf-8")
)

if consumption.get("execution_count_in_decision0177_transaction") != 1:
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

if "DECISION0176_A02_RESULT=PASS" not in \
        FILES["a02_output"].read_text(encoding="utf-8").splitlines():
    stop("A02_PASS_MARKER_MISSING")

if manifest.get("external_editable_copy_created") is not False:
    stop("EXTERNAL_COPY_PREMATURELY_CREATED")

if manifest.get("external_human_evidence_acquisition_authorized") is not False:
    stop("EXTERNAL_HUMAN_ACQUISITION_PREMATURELY_AUTHORIZED")

for key in [
    "human_evidence_result_recorded",
    "pair_reclassification_authorized",
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
    if manifest.get(key) is not False:
        stop("BOUNDARY_INVALID|" + key)

print("POSITIVE_BINDING_EVIDENCE_ACQUISITION_PACKAGE_V1=PASS")
print("PACKAGE_STATUS=AUTHOR_CANDIDATE_BLANK_AWAITING_EXTERNAL_HUMAN_EVIDENCE_ACQUISITION")
print("REQUIREMENT_COUNT=17")
print("SEMANTIC_UNIT_COUNT=109")
print("PAIR_UNIVERSE_COUNT=1853")
print("CURRENT_UNRESOLVED_BINDING_COUNT=1853")
print("BLANK_EVIDENCE_PACKET=PASS")
print("HUMAN_EVIDENCE_ACQUISITION_PERFORMED=NO")
print("EVIDENCE_STATES_PREPOPULATED=NO")
print("SEMANTIC_UNIT_PROPOSALS_PREPOPULATED=NO")
print("REVIEWER_IDENTITY_PREPOPULATED=NO")
print("AUTHOR_OR_MODEL_CANDIDATE_PRESELECTION_PRESENT=NO")
print("NEGATIVE_BINDING_JUDGMENT_AUTHORIZED=NO")
print("NOT_SUPPORTED_BINDING_AUTHORIZED=NO")
print("DECISION0176_A02_STATE=PERMANENTLY_RETIRED")
print("DECISION0176_A02_RERUN_AUTHORIZED=NO")
print("EXTERNAL_EDITABLE_COPY_CREATED=NO")
print("EXTERNAL_HUMAN_EVIDENCE_ACQUISITION_AUTHORIZED=NO")
print("PAIR_RECLASSIFICATION_AUTHORIZED=NO")
print("OPERATIONAL_MAPPING_AUTHORIZED=NO")
print("ANALYZER_IMPLEMENTATION_AUTHORIZED=NO")
print("ANALYZER_EXECUTION_AUTHORIZED=NO")
print("BASELINE_EXECUTION_AUTHORIZED=NO")
print("REPAIR_IMPLEMENTATION_AUTHORIZED=NO")
print("REPAIR_EXECUTION_AUTHORIZED=NO")
print("PACKAGE_SAFE_VERIFICATION=PASS")
