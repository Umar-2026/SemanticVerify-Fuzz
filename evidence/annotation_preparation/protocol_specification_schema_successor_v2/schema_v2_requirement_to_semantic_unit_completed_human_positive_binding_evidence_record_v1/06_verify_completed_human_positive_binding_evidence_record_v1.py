#!/usr/bin/env python3

from pathlib import Path
from collections import Counter
import hashlib
import json
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent

MANIFEST = ROOT / "01_recording_manifest.v1.json"
PACKET = ROOT / "02_completed_human_positive_binding_evidence_packet.EXACT_COPY.v1.md"
CONSUMPTION = ROOT / "03_decision0180_a02_consumption_record.v1.json"
OUTPUT = ROOT / "04_decision0180_a02_output.EXACT_COPY.v1.txt"
SENTINEL = ROOT / "05_decision0180_a02_reservation_sentinel.EXACT_COPY.v1.json"
CHECKSUMS = ROOT / "07_completed_human_positive_binding_evidence_record_v1.SHA256SUMS"

EXPECTED_PACKET_SHA = "effd2848702219741e3814d2dc283284c92ab07f49980cd799fde351ecb8b685"
EXPECTED_PACKET_SIZE = 20425

EXPECTED_A02_SHA = "51aac6bb34d5d6fd16d5198d1643e9e35a8d5d1a14f2ab73e34b4f83053527f7"

P05 = (
    ROOT.parent
    / "schema_v2_requirement_to_semantic_unit_positive_binding_evidence_acquisition_package_v1"
    / "05_requirement_provenance.EXACT_COPY.v1.json"
)

P06 = (
    ROOT.parent
    / "schema_v2_requirement_to_semantic_unit_positive_binding_evidence_acquisition_package_v1"
    / "06_semantic_unit_inventory.EXACT_COPY.v1.json"
)


def stop(label: str) -> None:
    print("SAFE_RECORD_VERIFIER_RESULT=FAIL")
    print("FAILURE=" + label)
    raise SystemExit(182)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


required = [
    MANIFEST,
    PACKET,
    CONSUMPTION,
    OUTPUT,
    SENTINEL,
    CHECKSUMS,
    P05,
    P06,
]

for path in required:
    if not path.is_file():
        stop("REQUIRED_FILE_MISSING|" + str(path))

manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
consumption = json.loads(CONSUMPTION.read_text(encoding="utf-8"))

if manifest.get("record_status") != \
        "IMMUTABLE_CANDIDATE_HUMAN_EVIDENCE_RECORDED":
    stop("RECORD_STATUS_INVALID")

if manifest.get("decision") != "Decision0181":
    stop("DECISION_BINDING_INVALID")

if sha256(PACKET) != EXPECTED_PACKET_SHA:
    stop("RECORDED_PACKET_HASH_INVALID")

if PACKET.stat().st_size != EXPECTED_PACKET_SIZE:
    stop("RECORDED_PACKET_SIZE_INVALID")

recorded = manifest.get("recorded_packet", {})

if recorded.get("sha256") != EXPECTED_PACKET_SHA:
    stop("MANIFEST_PACKET_HASH_INVALID")

if recorded.get("size_bytes") != EXPECTED_PACKET_SIZE:
    stop("MANIFEST_PACKET_SIZE_INVALID")

if recorded.get("byte_identical_to_authorized_returned_packet") is not True:
    stop("BYTE_IDENTITY_BOUNDARY_INVALID")

a02 = manifest.get("decision0180_a02_consumption", {})

if a02.get("verifier_sha256") != EXPECTED_A02_SHA:
    stop("A02_HASH_BINDING_INVALID")

if a02.get("execution_count") != 1:
    stop("A02_EXECUTION_COUNT_INVALID")

if a02.get("state_after_execution") != "PERMANENTLY_RETIRED":
    stop("A02_RETIREMENT_STATE_INVALID")

if a02.get("rerun_authorized") is not False:
    stop("A02_RERUN_BOUNDARY_INVALID")

if sha256(OUTPUT) != a02.get("output_sha256"):
    stop("A02_OUTPUT_HASH_INVALID")

if OUTPUT.stat().st_size != a02.get("output_size_bytes"):
    stop("A02_OUTPUT_SIZE_INVALID")

if sha256(SENTINEL) != a02.get("reservation_sentinel_sha256"):
    stop("A02_SENTINEL_HASH_INVALID")

if SENTINEL.stat().st_size != a02.get("reservation_sentinel_size_bytes"):
    stop("A02_SENTINEL_SIZE_INVALID")

if consumption.get("execution_count_after") != 1:
    stop("CONSUMPTION_EXECUTION_COUNT_INVALID")

if consumption.get("execution_result") != "PASS":
    stop("CONSUMPTION_RESULT_INVALID")

if consumption.get("state_after_execution") != "PERMANENTLY_RETIRED":
    stop("CONSUMPTION_RETIREMENT_INVALID")

if consumption.get("rerun_authorized") is not False:
    stop("CONSUMPTION_RERUN_BOUNDARY_INVALID")

output_text = OUTPUT.read_text(encoding="utf-8")

for required_line in [
    "DECISION0180_A02_RESULT=PASS",
    "ONE_TIME_VERIFIER_STATE=PERMANENTLY_RETIRED",
    "RERUN_AUTHORIZED=NO",
    "PAIR_RECLASSIFICATION_PERFORMED=NO",
    "PAIR_RECLASSIFICATION_AUTHORIZED=NO",
]:
    if required_line not in output_text.splitlines():
        stop("A02_OUTPUT_REQUIRED_LINE_MISSING|" + required_line)

req_obj = json.loads(P05.read_text(encoding="utf-8"))
unit_obj = json.loads(P06.read_text(encoding="utf-8"))

req_records = req_obj.get("records", [])
unit_records = unit_obj.get("semantic_units", [])

if len(req_records) != 17:
    stop("REQUIREMENT_DOMAIN_COUNT_INVALID")

if len(unit_records) != 109:
    stop("SEMANTIC_UNIT_DOMAIN_COUNT_INVALID")

req_ids = [r.get("requirement_id") for r in req_records]
req_values = [r.get("canonical_value") for r in req_records]
unit_ids = {r.get("unit_id") for r in unit_records}

if len(set(req_ids)) != 17:
    stop("REQUIREMENT_ID_DOMAIN_INVALID")

if None in unit_ids or len(unit_ids) != 109:
    stop("SEMANTIC_UNIT_ID_DOMAIN_INVALID")

text = PACKET.read_text(encoding="utf-8")

if "NOT_SUPPORTED_BINDING" in text:
    stop("FORBIDDEN_NOT_SUPPORTED_BINDING_PRESENT")

heading_rx = re.compile(r"(?m)^## Requirement (\d{2})$")
matches = list(heading_rx.finditer(text))

if len(matches) != 17:
    stop("PACKET_REQUIREMENT_SECTION_COUNT_INVALID")

human_marker = text.find("# Human evidence-reviewer completion")

if human_marker < 0:
    stop("HUMAN_COMPLETION_SECTION_MISSING")

states = []
positive_pairs = []

for i, m in enumerate(matches):
    num = m.group(1)

    if num != f"{i + 1:02d}":
        stop("REQUIREMENT_SECTION_ORDER_INVALID|" + num)

    start = m.end()
    end = matches[i + 1].start() if i + 1 < len(matches) else human_marker
    body = text[start:end]

    id_match = re.search(
        r'(?m)^Requirement ID \(exact\): (.+)$',
        body,
    )

    value_match = re.search(
        r'(?m)^Canonical requirement value \(JSON\): (.+)$',
        body,
    )

    state_match = re.search(
        r'(?m)^Evidence state:\s*`?([^`\n]+)`?\s*$',
        body,
    )

    if not id_match or not value_match or not state_match:
        stop("REQUIRED_REQUIREMENT_FIELD_MISSING|" + num)

    requirement_id = json.loads(id_match.group(1))
    canonical_value = json.loads(value_match.group(1))
    state = state_match.group(1).strip()

    if requirement_id != req_ids[i]:
        stop("REQUIREMENT_ID_CHANGED|" + num)

    if canonical_value != req_values[i]:
        stop("CANONICAL_VALUE_CHANGED|" + num)

    if state not in {
        "POSITIVE_BINDING_PROPOSED",
        "UNRESOLVED_NO_POSITIVE_BINDING_PROPOSED",
    }:
        stop("INVALID_STATE|" + num)

    states.append(state)

    proposal_start = body.find("Proposed semantic-unit IDs:")
    rationale_start = body.find("Positive-binding rationale:")

    if proposal_start < 0 or rationale_start < 0:
        stop("PROPOSAL_OR_RATIONALE_FIELD_MISSING|" + num)

    proposal_region = body[
        proposal_start + len("Proposed semantic-unit IDs:"):
        rationale_start
    ].strip()

    rationale_match = re.search(
        r'(?m)^Positive-binding rationale:\s*(.*)$',
        body,
    )

    if not rationale_match:
        stop("RATIONALE_FIELD_MISSING|" + num)

    rationale = rationale_match.group(1).strip()

    if state == "POSITIVE_BINDING_PROPOSED":
        ids = re.findall(
            r'(?m)^-\s+`([^`]+)`\s*$',
            proposal_region,
        )

        if not ids:
            stop("POSITIVE_PROPOSAL_HAS_NO_IDS|" + num)

        if not rationale:
            stop("POSITIVE_RATIONALE_EMPTY|" + num)

        if len(ids) != len(set(ids)):
            stop("DUPLICATE_UNIT_WITHIN_REQUIREMENT|" + num)

        invalid = set(ids) - unit_ids

        if invalid:
            stop("UNKNOWN_UNIT_ID|" + num)

        positive_pairs.extend(
            (requirement_id, unit_id)
            for unit_id in ids
        )
    else:
        if proposal_region.strip().lower() not in {
            "",
            "none",
            "none.",
            "`none`",
            "`none.`",
        }:
            stop("UNRESOLVED_HAS_UNIT_PROPOSAL|" + num)

counts = Counter(states)

if counts["POSITIVE_BINDING_PROPOSED"] != 15:
    stop("POSITIVE_REQUIREMENT_COUNT_INVALID")

if counts["UNRESOLVED_NO_POSITIVE_BINDING_PROPOSED"] != 2:
    stop("UNRESOLVED_REQUIREMENT_COUNT_INVALID")

if len(positive_pairs) != 211:
    stop("POSITIVE_PAIR_PROPOSAL_COUNT_INVALID")

if len(positive_pairs) != len(set(positive_pairs)):
    stop("DUPLICATE_REQUIREMENT_UNIT_PAIR")

completion = text[human_marker:]

for field in [
    "Human reviewer name",
    "Human reviewer role",
    "Human reviewer confirmation/signature",
    "Human reviewer date",
    "Human reviewer attestation",
]:
    match = re.search(
        rf'(?m)^{re.escape(field)}:\s*(.+)$',
        completion,
    )

    if not match or not match.group(1).strip():
        stop("HUMAN_COMPLETION_FIELD_INVALID|" + field)

role = re.search(
    r'(?m)^Human reviewer role:\s*(.+)$',
    completion,
).group(1).strip()

if role != "Spec-Technical-Reviewer-1":
    stop("HUMAN_REVIEWER_ROLE_INVALID")

bounded = manifest.get("bounded_interpretation", {})

required_false = [
    "pair_reclassification_performed",
    "pair_reclassification_authorized",
    "technical_adjudication_performed",
    "technical_adjudication_authorized",
    "unresolved_no_positive_binding_is_negative_proof",
    "not_supported_binding_created",
    "operational_mapping_authorized",
]

for key in required_false:
    if bounded.get(key) is not False:
        stop("BOUNDED_INTERPRETATION_INVALID|" + key)

if bounded.get("candidate_human_evidence_only") is not True:
    stop("CANDIDATE_EVIDENCE_BOUNDARY_INVALID")

checksum_result = subprocess.run(
    ["sha256sum", "-c", CHECKSUMS.name],
    cwd=ROOT,
    text=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
)

if checksum_result.returncode != 0:
    print(checksum_result.stdout, end="")
    stop("CHECKSUM_CLOSURE_INVALID")

print("SAFE_RECORD_VERIFIER_RESULT=PASS")
print("RECORDED_PACKET_SHA256=" + EXPECTED_PACKET_SHA)
print("RECORDED_PACKET_SIZE=20425")
print("REQUIREMENT_SECTION_COUNT=17")
print("SEMANTIC_UNIT_DOMAIN_COUNT=109")
print("POSITIVE_BINDING_PROPOSED_REQUIREMENT_COUNT=15")
print("UNRESOLVED_NO_POSITIVE_BINDING_PROPOSED_REQUIREMENT_COUNT=2")
print("POSITIVE_REQUIREMENT_UNIT_PAIR_PROPOSAL_COUNT=211")
print("DECISION0180_A02_EXECUTION_COUNT=1")
print("DECISION0180_A02_STATE=PERMANENTLY_RETIRED")
print("DECISION0180_A02_RERUN_AUTHORIZED=NO")
print("CANDIDATE_HUMAN_EVIDENCE_ONLY=YES")
print("PAIR_RECLASSIFICATION_PERFORMED=NO")
print("TECHNICAL_ADJUDICATION_PERFORMED=NO")
