#!/usr/bin/env python3

from pathlib import Path
from collections import Counter, defaultdict
import hashlib
import json
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent

P01 = ROOT / "01_package_manifest.v1.json"
P02 = ROOT / "02_211_candidate_pair_inventory.v1.json"
P03 = ROOT / "03_blank_technical_adjudication_packet.v1.md"
P04 = ROOT / "04_technical_adjudicator_instructions.v1.md"
P05 = ROOT / "05_governed_source_evidence_bindings.v1.json"
P06 = ROOT / "06_decision0183_a02_consumption_record.v1.json"
P07 = ROOT / "07_decision0183_a02_output.EXACT_COPY.v1.txt"
P08 = ROOT / "08_decision0183_a02_reservation_sentinel.EXACT_COPY.v1.json"
P10 = ROOT / "10_bounded_technical_adjudication_package_v1.SHA256SUMS"

R02_SOURCE = (
    BASE
    / "schema_v2_requirement_to_semantic_unit_completed_human_"
      "positive_binding_evidence_record_v1"
    / "02_completed_human_positive_binding_evidence_packet.EXACT_COPY.v1.md"
)

MATRIX = (
    BASE
    / "schema_v2_requirement_to_semantic_unit_crosswalk_"
      "evidence_resolution_study_v1"
    / "04_requirement_semantic_unit_pair_matrix.v1.json"
)

REQ_PROV = (
    BASE
    / "schema_v2_v4_losslessness_requirement_provenance_"
      "binding_resolution_study_v1"
    / "01_17_requirement_provenance_binding_matrix.v1.json"
)

UNIT_INV = (
    BASE
    / "schema_v2_requirement_to_semantic_unit_positive_binding_"
      "evidence_acquisition_package_v1"
    / "06_semantic_unit_inventory.EXACT_COPY.v1.json"
)

UNIT_TRACE = (
    BASE
    / "schema_v2_semantic_role_relation_formalization_v1"
    / "03_v4_semantic_unit_context_and_leaf_traceability.v1.json"
)

EXPECTED_PACKET_SHA = "effd2848702219741e3814d2dc283284c92ab07f49980cd799fde351ecb8b685"
EXPECTED_MATRIX_SHA = "389615002582964b97aa6eb717ceb520067cef78b18cf482cf257fe9b36f2515"
EXPECTED_REQ_PROV_SHA = "a03a1c0d5e43a83d74534ed772503f46b3118cec9351f4324ac03ebeb51ae4ac"
EXPECTED_UNIT_INV_SHA = "2b39f5625658e41aeb906a1db8a4a472d9265dc3654572e60374827f0ce7fa7d"
EXPECTED_UNIT_TRACE_SHA = "6b4b30c958bc1e1dd0896fe086205e3ff58063583b2042bba962c8c59ba46bd4"
EXPECTED_A02_SHA = "924b9c1d38edf43cb59b308b091d9bbeebd63ef416f1feb1c5042c1865b6d333"


def stop(label):
    print("SAFE_TECHNICAL_ADJUDICATION_PACKAGE_VERIFIER_RESULT=FAIL")
    print("FAILURE=" + label)
    raise SystemExit(184)


def sha256(path):
    h = hashlib.sha256()

    with path.open("rb") as f:
        for chunk in iter(
            lambda: f.read(1024 * 1024),
            b"",
        ):
            h.update(chunk)

    return h.hexdigest()


for path in [
    P01, P02, P03, P04, P05, P06,
    P07, P08, P10,
    R02_SOURCE, MATRIX, REQ_PROV,
    UNIT_INV, UNIT_TRACE,
]:
    if not path.is_file():
        stop("REQUIRED_FILE_MISSING|" + str(path))


if sha256(R02_SOURCE) != EXPECTED_PACKET_SHA:
    stop("RECORDED_PACKET_HASH_INVALID")

if sha256(MATRIX) != EXPECTED_MATRIX_SHA:
    stop("PAIR_MATRIX_HASH_INVALID")

if sha256(REQ_PROV) != EXPECTED_REQ_PROV_SHA:
    stop("REQUIREMENT_PROVENANCE_HASH_INVALID")

if sha256(UNIT_INV) != EXPECTED_UNIT_INV_SHA:
    stop("UNIT_INVENTORY_HASH_INVALID")

if sha256(UNIT_TRACE) != EXPECTED_UNIT_TRACE_SHA:
    stop("UNIT_TRACEABILITY_HASH_INVALID")


manifest = json.loads(
    P01.read_text(encoding="utf-8")
)

inventory = json.loads(
    P02.read_text(encoding="utf-8")
)

source_bindings = json.loads(
    P05.read_text(encoding="utf-8")
)

consumption = json.loads(
    P06.read_text(encoding="utf-8")
)


if manifest.get("decision") != "Decision0184":
    stop("MANIFEST_DECISION_INVALID")

if manifest.get("package_status") != (
    "AUTHOR_CANDIDATE_BLANK_AWAITING_"
    "EXTERNAL_HUMAN_TECHNICAL_ADJUDICATION"
):
    stop("PACKAGE_STATUS_INVALID")

if manifest.get("bounded_pair_count") != 211:
    stop("MANIFEST_PAIR_COUNT_INVALID")

if manifest.get("adjudicator_identity_prefilled") is not False:
    stop("ADJUDICATOR_IDENTITY_BOUNDARY_INVALID")

if manifest.get("adjudication_outcomes_prefilled") is not False:
    stop("ADJUDICATION_OUTCOME_BOUNDARY_INVALID")

if manifest.get(
    "author_or_model_additional_pair_selection"
) is not False:
    stop("PAIR_SELECTION_BOUNDARY_INVALID")

if manifest.get(
    "candidate_pair_ranking_performed"
) is not False:
    stop("PAIR_RANKING_BOUNDARY_INVALID")


a02 = manifest.get("decision0183_a02", {})

if a02.get("verifier_sha256") != EXPECTED_A02_SHA:
    stop("A02_HASH_BINDING_INVALID")

if a02.get("execution_count") != 1:
    stop("A02_EXECUTION_COUNT_INVALID")

if a02.get("state") != "PERMANENTLY_RETIRED":
    stop("A02_RETIREMENT_INVALID")

if a02.get("rerun_authorized") is not False:
    stop("A02_RERUN_BOUNDARY_INVALID")


if consumption.get("execution_count_after") != 1:
    stop("CONSUMPTION_COUNT_INVALID")

if consumption.get("execution_result") != "PASS":
    stop("CONSUMPTION_RESULT_INVALID")

if consumption.get("state_after_execution") != "PERMANENTLY_RETIRED":
    stop("CONSUMPTION_RETIREMENT_INVALID")

if consumption.get("rerun_authorized") is not False:
    stop("CONSUMPTION_RERUN_BOUNDARY_INVALID")


output_lines = set(
    P07.read_text(
        encoding="utf-8"
    ).splitlines()
)

for line in [
    "DECISION0183_A02_RESULT=PASS",
    "BOUNDED_TECHNICAL_ADJUDICATION_PAIR_SCOPE=211",
    "BOUNDED_SCOPE_PAIRS_CURRENTLY_UNRESOLVED=211",
    "TECHNICAL_ADJUDICATION_PERFORMED=NO",
    "PAIR_RECLASSIFICATION_PERFORMED=NO",
    "ONE_TIME_VERIFIER_STATE=PERMANENTLY_RETIRED",
    "RERUN_AUTHORIZED=NO",
]:
    if line not in output_lines:
        stop("A02_OUTPUT_MARKER_MISSING|" + line)


records = inventory.get("records", [])

if inventory.get("pair_count") != 211:
    stop("INVENTORY_PAIR_COUNT_INVALID")

if len(records) != 211:
    stop("INVENTORY_RECORD_COUNT_INVALID")


pair_keys = []

for expected_ordinal, record in enumerate(
    records,
    start=1,
):
    if record.get("pair_ordinal") != expected_ordinal:
        stop("PAIR_ORDINAL_INVALID")

    req = record.get("requirement_id")
    unit = record.get("semantic_unit_id")

    if not isinstance(req, str):
        stop("REQUIREMENT_ID_INVALID")

    if not isinstance(unit, str):
        stop("SEMANTIC_UNIT_ID_INVALID")

    pair_keys.append((req, unit))

    if record.get("governed_pair_prestate") != "UNRESOLVED_BINDING":
        stop("PAIR_PRESTATE_INVALID")

    if record.get("recorded_reviewer_evidence_state") != "POSITIVE_BINDING_PROPOSED":
        stop("REVIEWER_EVIDENCE_STATE_INVALID")

    if not record.get(
        "recorded_reviewer_rationale"
    ):
        stop("REVIEWER_RATIONALE_MISSING")

    if record.get(
        "technical_adjudication_state"
    ) != "":
        stop("ADJUDICATION_STATE_PREFILLED")

    if record.get(
        "technical_adjudication_rationale"
    ) != "":
        stop("ADJUDICATION_RATIONALE_PREFILLED")

    if record.get(
        "technical_adjudicator_notes"
    ) != "":
        stop("ADJUDICATOR_NOTES_PREFILLED")


if len(set(pair_keys)) != 211:
    stop("PAIR_KEYS_NOT_UNIQUE")


source_packet = R02_SOURCE.read_text(
    encoding="utf-8"
)

heading_rx = re.compile(
    r"(?m)^## Requirement (\d{2})$"
)

matches = list(
    heading_rx.finditer(source_packet)
)

human_marker = source_packet.find(
    "# Human evidence-reviewer completion"
)

expected_records = []

ordinal = 0

for i, match in enumerate(matches):
    start = match.end()

    end = (
        matches[i + 1].start()
        if i + 1 < len(matches)
        else human_marker
    )

    body = source_packet[start:end]

    id_match = re.search(
        r'(?m)^Requirement ID \(exact\): (.+)$',
        body,
    )

    state_match = re.search(
        r'(?m)^Evidence state:\s*`?([^`\n]+)`?\s*$',
        body,
    )

    rationale_match = re.search(
        r'(?m)^Positive-binding rationale:\s*(.*)$',
        body,
    )

    notes_match = re.search(
        r'(?m)^Reviewer notes:\s*(.*)$',
        body,
    )

    requirement_id = json.loads(
        id_match.group(1)
    )

    state = state_match.group(1).strip()

    if state != "POSITIVE_BINDING_PROPOSED":
        continue

    p_start = body.find(
        "Proposed semantic-unit IDs:"
    )

    r_start = body.find(
        "Positive-binding rationale:"
    )

    proposal_region = body[
        p_start
        + len("Proposed semantic-unit IDs:"):
        r_start
    ].strip()

    units = re.findall(
        r'(?m)^-\s+`([^`]+)`\s*$',
        proposal_region,
    )

    for unit in units:
        ordinal += 1

        expected_records.append(
            (
                ordinal,
                match.group(1),
                requirement_id,
                unit,
                rationale_match.group(1).strip(),
                notes_match.group(1).strip(),
            )
        )


if len(expected_records) != 211:
    stop("SOURCE_EXPECTED_RECORD_COUNT_INVALID")


for record, expected in zip(
    records,
    expected_records,
):
    (
        ordinal,
        section,
        req,
        unit,
        rationale,
        notes,
    ) = expected

    if record.get("pair_ordinal") != ordinal:
        stop("SOURCE_PAIR_ORDINAL_MISMATCH")

    if record.get(
        "source_requirement_section"
    ) != section:
        stop("SOURCE_SECTION_MISMATCH")

    if record.get("requirement_id") != req:
        stop("SOURCE_REQUIREMENT_ID_MISMATCH")

    if record.get("semantic_unit_id") != unit:
        stop("SOURCE_SEMANTIC_UNIT_ID_MISMATCH")

    if record.get(
        "recorded_reviewer_rationale"
    ) != rationale:
        stop("SOURCE_RATIONALE_MISMATCH")

    if record.get(
        "recorded_reviewer_notes"
    ) != notes:
        stop("SOURCE_REVIEWER_NOTES_MISMATCH")


blank = P03.read_text(
    encoding="utf-8"
)

pair_headings = re.findall(
    r"(?m)^## Candidate Pair (\d{3})$",
    blank,
)

if len(pair_headings) != 211:
    stop("BLANK_PACKET_PAIR_SECTION_COUNT_INVALID")

if pair_headings != [
    f"{i:03d}"
    for i in range(1, 212)
]:
    stop("BLANK_PACKET_PAIR_ORDER_INVALID")


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
        stop(
            "BLANK_FIELD_COUNT_INVALID|"
            + label
        )

    if any(
        line.strip() != label
        for line in lines
    ):
        stop(
            "BLANK_FIELD_PREFILLED|"
            + label
        )


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

    if len(lines) != 1:
        stop(
            "HUMAN_FIELD_COUNT_INVALID|"
            + label
        )

    if lines[0].strip() != label:
        stop(
            "HUMAN_FIELD_PREFILLED|"
            + label
        )


bounded = manifest.get(
    "bounded_interpretation",
    {},
)

required_false = [
    "human_technical_adjudication_performed",
    "pair_reclassification_performed",
    "pair_reclassification_authorized",
    "automatic_promotion_authorized",
    "supported_binding_created",
    "not_supported_binding_created",
    "negative_proof_created",
    "operational_mapping_authorized",
    "schema_v2_modification_authorized",
    "analyzer_execution_authorized",
    "baseline_execution_authorized",
    "repair_execution_authorized",
]

for key in required_false:
    if bounded.get(key) is not False:
        stop(
            "BOUNDED_INTERPRETATION_INVALID|"
            + key
        )


checksum_result = subprocess.run(
    [
        "sha256sum",
        "-c",
        P10.name,
    ],
    cwd=ROOT,
    text=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
)

if checksum_result.returncode != 0:
    print(
        checksum_result.stdout,
        end="",
    )

    stop("CHECKSUM_CLOSURE_INVALID")


print(
    "SAFE_TECHNICAL_ADJUDICATION_PACKAGE_VERIFIER_RESULT=PASS"
)
print("PACKAGE_PAIR_COUNT=211")
print("PACKAGE_UNIQUE_PAIR_COUNT=211")
print("PACKAGE_PAIR_PRESTATE_UNRESOLVED_COUNT=211")
print("ADJUDICATION_STATES_PREFILLED=0")
print("ADJUDICATION_RATIONALES_PREFILLED=0")
print("ADJUDICATOR_NOTES_PREFILLED=0")
print("ADJUDICATOR_IDENTITY_PREFILLED=NO")
print("HUMAN_TECHNICAL_ADJUDICATION_PERFORMED=NO")
print("PAIR_RECLASSIFICATION_PERFORMED=NO")
print("SUPPORTED_BINDING_CREATED=NO")
print("NOT_SUPPORTED_BINDING_CREATED=NO")
print("DECISION0183_A02_EXECUTION_COUNT=1")
print("DECISION0183_A02_STATE=PERMANENTLY_RETIRED")
print("DECISION0183_A02_RERUN_AUTHORIZED=NO")
