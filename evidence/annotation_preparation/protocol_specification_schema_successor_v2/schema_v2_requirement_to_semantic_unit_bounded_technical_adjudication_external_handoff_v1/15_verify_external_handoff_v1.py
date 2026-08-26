#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent

H01 = ROOT / "01_external_handoff_manifest.v1.json"
H02 = ROOT / "02_blank_technical_adjudication_packet.EXACT_COPY.v1.md"
H03 = ROOT / "03_technical_adjudicator_instructions.EXACT_COPY.v1.md"
H04 = ROOT / "04_211_candidate_pair_inventory.EXACT_COPY.v1.json"
H05 = ROOT / "05_package_manifest.EXACT_COPY.v1.json"
H06 = ROOT / "06_governed_source_evidence_bindings.EXACT_COPY.v1.json"
H07 = ROOT / "07_recorded_positive_binding_human_evidence.EXACT_COPY.v1.md"
H08 = ROOT / "08_governed_pair_matrix.EXACT_COPY.v1.json"
H09 = ROOT / "09_requirement_provenance.EXACT_COPY.v1.json"
H10 = ROOT / "10_semantic_unit_inventory.EXACT_COPY.v1.json"
H11 = ROOT / "11_semantic_unit_traceability.EXACT_COPY.v1.json"
H12 = ROOT / "12_decision0185_a02_consumption_record.v1.json"
H13 = ROOT / "13_decision0185_a02_output.EXACT_COPY.v1.txt"
H14 = ROOT / "14_decision0185_a02_reservation_sentinel.EXACT_COPY.v1.json"
H16 = ROOT / "16_external_handoff_v1.SHA256SUMS"

PKG_DIR = (
    BASE
    / "schema_v2_requirement_to_semantic_unit_bounded_technical_adjudication_package_v1"
)

P01 = PKG_DIR / "01_package_manifest.v1.json"
P02 = PKG_DIR / "02_211_candidate_pair_inventory.v1.json"
P03 = PKG_DIR / "03_blank_technical_adjudication_packet.v1.md"
P04 = PKG_DIR / "04_technical_adjudicator_instructions.v1.md"
P05 = PKG_DIR / "05_governed_source_evidence_bindings.v1.json"

RECORDED_HUMAN = (
    BASE
    / "schema_v2_requirement_to_semantic_unit_completed_human_positive_binding_evidence_record_v1"
    / "02_completed_human_positive_binding_evidence_packet.EXACT_COPY.v1.md"
)

MATRIX = (
    BASE
    / "schema_v2_requirement_to_semantic_unit_crosswalk_evidence_resolution_study_v1"
    / "04_requirement_semantic_unit_pair_matrix.v1.json"
)

REQ_PROV = (
    BASE
    / "schema_v2_v4_losslessness_requirement_provenance_binding_resolution_study_v1"
    / "01_17_requirement_provenance_binding_matrix.v1.json"
)

UNIT_INV = (
    BASE
    / "schema_v2_requirement_to_semantic_unit_positive_binding_evidence_acquisition_package_v1"
    / "06_semantic_unit_inventory.EXACT_COPY.v1.json"
)

UNIT_TRACE = (
    BASE
    / "schema_v2_semantic_role_relation_formalization_v1"
    / "03_v4_semantic_unit_context_and_leaf_traceability.v1.json"
)

EXPECTED_A02_SHA = "ffd8dd3b4beea31fcac8903c70f902f26038e200d82c0fdb4a829d9d40d46324"


def stop(label):
    print("SAFE_EXTERNAL_HANDOFF_VERIFIER_RESULT=FAIL")
    print("FAILURE=" + label)
    raise SystemExit(186)


def sha256(path):
    h = hashlib.sha256()

    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)

    return h.hexdigest()


for path in [
    H01, H02, H03, H04, H05, H06,
    H07, H08, H09, H10, H11, H12,
    H13, H14, H16,
    P01, P02, P03, P04, P05,
    RECORDED_HUMAN, MATRIX, REQ_PROV,
    UNIT_INV, UNIT_TRACE,
]:
    if not path.is_file():
        stop("REQUIRED_FILE_MISSING|" + str(path))


exact_copy_pairs = [
    (H02, P03),
    (H03, P04),
    (H04, P02),
    (H05, P01),
    (H06, P05),
    (H07, RECORDED_HUMAN),
    (H08, MATRIX),
    (H09, REQ_PROV),
    (H10, UNIT_INV),
    (H11, UNIT_TRACE),
]

for handoff_copy, source in exact_copy_pairs:
    if sha256(handoff_copy) != sha256(source):
        stop("EXACT_COPY_HASH_MISMATCH|" + handoff_copy.name)

    if handoff_copy.read_bytes() != source.read_bytes():
        stop("EXACT_COPY_BYTES_MISMATCH|" + handoff_copy.name)


manifest = json.loads(H01.read_text(encoding="utf-8"))
inventory = json.loads(H04.read_text(encoding="utf-8"))
consumption = json.loads(H12.read_text(encoding="utf-8"))
sentinel = json.loads(H14.read_text(encoding="utf-8"))

if manifest.get("decision") != "Decision0186":
    stop("MANIFEST_DECISION_INVALID")

if manifest.get("handoff_status") != \
        "HANDOFF_AUTHORED_AWAITING_EXTERNAL_HUMAN_TECHNICAL_ADJUDICATION":
    stop("HANDOFF_STATUS_INVALID")

if manifest.get("bounded_pair_count") != 211:
    stop("MANIFEST_PAIR_COUNT_INVALID")

if manifest.get(
    "authorized_external_human_editable_surface_count"
) != 1:
    stop("EDITABLE_SURFACE_COUNT_INVALID")

if manifest.get(
    "technical_adjudicator_role_contract"
) != "Spec-Technical-Adjudicator-1":
    stop("ROLE_CONTRACT_INVALID")

if len(inventory.get("records", [])) != 211:
    stop("INVENTORY_RECORD_COUNT_INVALID")

for record in inventory["records"]:
    if record.get("technical_adjudication_state") != "":
        stop("ADJUDICATION_STATE_PREFILLED")

    if record.get("technical_adjudication_rationale") != "":
        stop("ADJUDICATION_RATIONALE_PREFILLED")

    if record.get("technical_adjudicator_notes") != "":
        stop("ADJUDICATOR_NOTES_PREFILLED")


blank = H02.read_text(encoding="utf-8")

pair_sections = re.findall(
    r"(?m)^## Candidate Pair (\d{3})$",
    blank,
)

if pair_sections != [f"{i:03d}" for i in range(1, 212)]:
    stop("BLANK_PAIR_STRUCTURE_INVALID")

for label in [
    "Technical adjudication state:",
    "Technical adjudication rationale:",
    "Technical adjudicator notes:",
]:
    lines = [
        line
        for line in blank.splitlines()
        if line.startswith(label)
    ]

    if len(lines) != 211:
        stop("BLANK_FIELD_COUNT_INVALID|" + label)

    if any(line.strip() != label for line in lines):
        stop("BLANK_FIELD_PREFILLED|" + label)

for label in [
    "Human technical adjudicator name:",
    "Human technical adjudicator role:",
    "Human technical adjudicator confirmation/signature:",
    "Human technical adjudicator date:",
    "Human technical adjudicator attestation:",
]:
    lines = [
        line
        for line in blank.splitlines()
        if line.startswith(label)
    ]

    if len(lines) != 1 or lines[0].strip() != label:
        stop("HUMAN_FIELD_INVALID|" + label)


if consumption.get("execution_count_after") != 1:
    stop("A02_CONSUMPTION_COUNT_INVALID")

if consumption.get("execution_result") != "PASS":
    stop("A02_CONSUMPTION_RESULT_INVALID")

if consumption.get("state_after_execution") != "PERMANENTLY_RETIRED":
    stop("A02_RETIREMENT_STATE_INVALID")

if consumption.get("rerun_authorized") is not False:
    stop("A02_RERUN_BOUNDARY_INVALID")

if consumption.get("verifier_sha256") != EXPECTED_A02_SHA:
    stop("A02_HASH_BINDING_INVALID")


output_lines = set(H13.read_text(encoding="utf-8").splitlines())

for line in [
    "DECISION0185_A02_RESULT=PASS",
    "BOUNDED_PAIR_COUNT=211",
    "ADJUDICATION_STATES_PREFILLED=0",
    "ADJUDICATOR_IDENTITY_PREFILLED=NO",
    "HUMAN_TECHNICAL_ADJUDICATION_PERFORMED=NO",
    "PAIR_RECLASSIFICATION_PERFORMED=NO",
    "ONE_TIME_VERIFIER_STATE=PERMANENTLY_RETIRED",
    "RERUN_AUTHORIZED=NO",
]:
    if line not in output_lines:
        stop("A02_OUTPUT_MARKER_MISSING|" + line)


if sentinel.get("decision") != "Decision0185":
    stop("SENTINEL_DECISION_INVALID")

if sentinel.get("execution_transaction") != "Decision0186":
    stop("SENTINEL_TRANSACTION_INVALID")

if sentinel.get("bounded_pair_count") != 211:
    stop("SENTINEL_PAIR_COUNT_INVALID")

if sentinel.get("rerun_authorized") is not False:
    stop("SENTINEL_RERUN_BOUNDARY_INVALID")


bounded = manifest.get("bounded_interpretation", {})

for key in [
    "human_technical_adjudication_performed",
    "human_adjudication_result_recorded",
    "pair_reclassification_performed",
    "pair_reclassification_authorized",
    "supported_binding_created",
    "not_supported_binding_created",
    "automatic_promotion_authorized",
    "negative_proof_created",
    "operational_mapping_authorized",
    "schema_v2_modification_authorized",
    "analyzer_execution_authorized",
    "baseline_execution_authorized",
    "repair_execution_authorized",
]:
    if bounded.get(key) is not False:
        stop("BOUNDED_INTERPRETATION_INVALID|" + key)


checksum_result = subprocess.run(
    ["sha256sum", "-c", H16.name],
    cwd=ROOT,
    text=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
)

if checksum_result.returncode != 0:
    print(checksum_result.stdout, end="")
    stop("CHECKSUM_CLOSURE_INVALID")


print("SAFE_EXTERNAL_HANDOFF_VERIFIER_RESULT=PASS")
print("HANDOFF_PAIR_COUNT=211")
print("AUTHORIZED_EXTERNAL_EDITABLE_SURFACE_COUNT=1")
print("BLANK_PACKET_BYTE_BINDING=PASS")
print("ADJUDICATION_STATES_PREFILLED=0")
print("ADJUDICATION_RATIONALES_PREFILLED=0")
print("ADJUDICATOR_NOTES_PREFILLED=0")
print("ADJUDICATOR_IDENTITY_PREFILLED=NO")
print("DECISION0185_A02_EXECUTION_COUNT=1")
print("DECISION0185_A02_STATE=PERMANENTLY_RETIRED")
print("DECISION0185_A02_RERUN_AUTHORIZED=NO")
print("HUMAN_TECHNICAL_ADJUDICATION_PERFORMED=NO")
print("HUMAN_ADJUDICATION_RESULT_RECORDED=NO")
print("PAIR_RECLASSIFICATION_PERFORMED=NO")
print("SUPPORTED_BINDING_CREATED=NO")
print("NOT_SUPPORTED_BINDING_CREATED=NO")
