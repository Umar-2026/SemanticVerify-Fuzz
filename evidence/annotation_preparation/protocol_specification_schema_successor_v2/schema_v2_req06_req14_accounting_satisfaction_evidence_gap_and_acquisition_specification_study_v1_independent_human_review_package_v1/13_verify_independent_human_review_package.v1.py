#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

P01 = HERE / "01_independent_human_review_package_manifest.v1.json"
P02 = HERE / "02_accounting_satisfaction_evidence_gap_assessment.EXACT_COPY.v1.json"
P03 = HERE / "03_future_accounting_evidence_acquisition_specification.EXACT_COPY.v1.json"
P04 = HERE / "04_machine_checkable_accounting_satisfaction_criteria.EXACT_COPY.v1.json"
P05 = HERE / "05_study_source_binding.EXACT_COPY.v1.json"
P06 = HERE / "06_study_boundary.EXACT_COPY.v1.md"
P07 = HERE / "07_independent_human_review_contract.EXACT_COPY.v1.json"
P08 = HERE / "08_reviewer_instructions.v1.md"
P09 = HERE / "09_blank_independent_human_review_form.v1.md"
P10 = HERE / "10_decision0204_a02_consumption_record.v1.json"
P11 = HERE / "11_decision0204_a02_execution_output.EXACT_COPY.v1.txt"
P12 = HERE / "12_decision0204_a02_consumption_sentinel.EXACT_COPY.v1.json"

EXPECTED_EXACT_SHA = {
    P02:
        "6dd6540f0655c1ac064460560d2429fa62762ac4e6bb52e671283ff227f0b2a9",
    P03:
        "c4c77261ef19d929112ca56247d223ad7a04d9f6661dcc08860ff4a77dfabc83",
    P04:
        "e74e58463659531a393c24a6a8de616f4efa9b688d13a24b67e876f4d0ca8436",
    P05:
        "ec0e753dfc694ff8764d2452bceddf820cf3740f55b02c218bc661db7e75cf72",
    P06:
        "451e1648c6f5eeea38bcb485839c5bb03e3eba6cc378d3fd49970317dc10f963",
    P07:
        "8ad3ea2208ddc9bced6e709072eb6082fa0b269485fceaa842666375237b4ba1",
}


def stop(code, detail=""):
    print(
        "STOP|" + code
        + (("|" + detail) if detail else "")
    )
    raise SystemExit(1)


for path in (
    P01, P02, P03, P04, P05, P06, P07,
    P08, P09, P10, P11, P12
):
    if not path.is_file():
        stop("PACKAGE_ARTIFACT_MISSING", str(path))

for path, expected in EXPECTED_EXACT_SHA.items():
    actual = hashlib.sha256(path.read_bytes()).hexdigest()

    if actual != expected:
        stop("EXACT_COPY_SHA_MISMATCH", path.name)

manifest = json.loads(
    P01.read_text(encoding="utf-8")
)

if manifest.get("package_status") != (
    "BLANK_AWAITING_INDEPENDENT_HUMAN_REVIEW"
):
    stop("PACKAGE_STATUS_INVALID")

subject = manifest.get("review_subject", {})

if subject.get("status") != "AUTHOR_CANDIDATE":
    stop("REVIEW_SUBJECT_STATUS_INVALID")

if subject.get("result") != (
    "EVIDENCE_GAP_CONFIRMED_ACQUISITION_SPECIFICATION_READY"
):
    stop("REVIEW_SUBJECT_RESULT_INVALID")

review_contract = manifest.get("review_contract", {})

if review_contract.get("review_item_count") != 9:
    stop("REVIEW_ITEM_COUNT_INVALID")

expected_ids = [
    "ASER01",
    "ASER02",
    "ASER03",
    "ASER04",
    "ASER05",
    "ASER06",
    "ASER07",
    "ASER08",
    "ASER09",
]

if review_contract.get("review_item_ids") != expected_ids:
    stop("REVIEW_ITEM_ID_SEQUENCE_INVALID")

if set(
    review_contract.get("allowed_item_decisions", [])
) != {
    "PASS",
    "REVISION_REQUIRED",
}:
    stop("ITEM_DECISION_VOCABULARY_INVALID")

if set(
    review_contract.get("allowed_overall_decisions", [])
) != {
    "APPROVE_BOUNDED_EVIDENCE_GAP_AND_ACQUISITION_SPECIFICATION_STUDY",
    "REVISION_REQUIRED",
}:
    stop("OVERALL_DECISION_VOCABULARY_INVALID")

blank_state = manifest.get("blank_human_state", {})

for key in (
    "reviewer_name_prefilled",
    "reviewer_role_prefilled",
    "reviewer_confirmation_prefilled",
    "review_date_prefilled",
    "independent_review_attestation_prefilled",
    "item_decisions_prefilled",
    "reviewer_notes_prefilled",
    "overall_decision_prefilled",
    "overall_notes_prefilled",
    "human_review_performed",
    "human_review_recorded",
):
    if blank_state.get(key) is not False:
        stop("BLANK_HUMAN_STATE_INVALID", key)

consumption = json.loads(
    P10.read_text(encoding="utf-8")
)

if consumption.get("execution_count") != 1:
    stop("D0204_A02_EXECUTION_COUNT_INVALID")

if consumption.get("execution_result") != "PASS":
    stop("D0204_A02_RESULT_INVALID")

if consumption.get("lifecycle_state") != "PERMANENTLY_RETIRED":
    stop("D0204_A02_RETIREMENT_INVALID")

if consumption.get("rerun_authorized") is not False:
    stop("D0204_A02_RERUN_BOUNDARY_INVALID")

if hashlib.sha256(P11.read_bytes()).hexdigest() != consumption.get(
    "execution_output_sha256"
):
    stop("D0204_A02_OUTPUT_BINDING_INVALID")

if hashlib.sha256(P12.read_bytes()).hexdigest() != consumption.get(
    "consumption_sentinel_sha256"
):
    stop("D0204_A02_SENTINEL_BINDING_INVALID")

for filename, metadata in manifest.get(
    "package_artifacts",
    {}
).items():
    path = HERE / filename

    if not path.is_file():
        stop("MANIFEST_BOUND_ARTIFACT_MISSING", filename)

    raw = path.read_bytes()

    if hashlib.sha256(raw).hexdigest() != metadata.get("sha256"):
        stop("MANIFEST_ARTIFACT_SHA_INVALID", filename)

    if len(raw) != metadata.get("size_bytes"):
        stop("MANIFEST_ARTIFACT_SIZE_INVALID", filename)

contract = json.loads(
    P07.read_text(encoding="utf-8")
)

if contract.get("review_item_count") != 9:
    stop("CONTRACT_REVIEW_ITEM_COUNT_INVALID")

items = contract.get("review_items", [])

if [x.get("id") for x in items] != expected_ids:
    stop("CONTRACT_REVIEW_ITEM_SEQUENCE_INVALID")

form = P09.read_text(
    encoding="utf-8"
)

lines = form.splitlines()

human_labels = [
    "Reviewer name:",
    "Reviewer role:",
    "Reviewer confirmation/signature:",
    "Review date:",
    "Independent-review attestation:",
]

for label in human_labels:
    matches = [
        line
        for line in lines
        if line.startswith(label)
    ]

    if len(matches) != 1:
        stop(
            "BLANK_FORM_HUMAN_FIELD_COUNT_INVALID",
            label
        )

    if matches[0][len(label):].strip():
        stop(
            "BLANK_FORM_HUMAN_FIELD_PREFILLED",
            label
        )

for item_id in expected_ids:
    count = len(
        re.findall(
            rf"^## {re.escape(item_id)}\b",
            form,
            flags=re.M
        )
    )

    if count != 1:
        stop(
            "BLANK_FORM_REVIEW_ITEM_SECTION_INVALID",
            item_id
        )

decision_lines = [
    line
    for line in lines
    if line.startswith("Review decision:")
]

if len(decision_lines) != 9:
    stop("BLANK_FORM_ITEM_DECISION_COUNT_INVALID")

if any(
    line[len("Review decision:"):].strip()
    for line in decision_lines
):
    stop("BLANK_FORM_ITEM_DECISION_PREFILLED")

notes_lines = [
    line
    for line in lines
    if line.startswith("Reviewer notes:")
]

if len(notes_lines) != 9:
    stop("BLANK_FORM_REVIEWER_NOTES_COUNT_INVALID")

if any(
    line[len("Reviewer notes:"):].strip()
    for line in notes_lines
):
    stop("BLANK_FORM_REVIEWER_NOTES_PREFILLED")

overall_decision = [
    line
    for line in lines
    if line.startswith("Overall review decision:")
]

if len(overall_decision) != 1:
    stop("BLANK_FORM_OVERALL_DECISION_COUNT_INVALID")

if overall_decision[0][
    len("Overall review decision:"):
].strip():
    stop("BLANK_FORM_OVERALL_DECISION_PREFILLED")

overall_notes = [
    line
    for line in lines
    if line.startswith("Overall reviewer notes:")
]

if len(overall_notes) != 1:
    stop("BLANK_FORM_OVERALL_NOTES_COUNT_INVALID")

if overall_notes[0][
    len("Overall reviewer notes:"):
].strip():
    stop("BLANK_FORM_OVERALL_NOTES_PREFILLED")

gov = manifest.get("governance_state", {})

false_keys = (
    "study_governance_adopted",
    "actual_accounting_evidence_acquisition_authorized",
    "actual_accounting_evidence_acquisition_performed",
    "concrete_accounting_instance_created",
    "source_unit_to_schema_carrier_mapping_created",
    "accounting_satisfaction_determination_authorized",
    "accounting_satisfaction_established",
    "pair_reclassification_performed",
    "supported_binding_created",
    "not_supported_binding_created",
    "schema_v2_losslessness_proven",
    "operational_mapping_authorized",
    "analyzer_authorized",
    "baseline_authorized",
    "repair_authorized",
)

for key in false_keys:
    if gov.get(key) is not False:
        stop("PACKAGE_GOVERNANCE_BOUNDARY_INVALID", key)

if gov.get("supported_binding_count") != 211:
    stop("SUPPORTED_BINDING_COUNT_INVALID")

if gov.get("unresolved_binding_count") != 1642:
    stop("UNRESOLVED_BINDING_COUNT_INVALID")

if gov.get("not_supported_binding_count") != 0:
    stop("NOT_SUPPORTED_BINDING_COUNT_INVALID")

if gov.get("req06_req14_unresolved_pair_count") != 218:
    stop("REQ06_REQ14_UNRESOLVED_PAIR_COUNT_INVALID")

instructions = P08.read_text(
    encoding="utf-8"
)

for phrase in (
    "genuine independent human reviewer",
    "must not be the author",
    "No reviewer identity or role has been preassigned",
    "non-establishment / not-evaluated markers",
    "does not itself",
):
    if phrase not in instructions:
        stop("REVIEWER_INSTRUCTIONS_BOUNDARY_MISSING", phrase)

print(
    "REQ06_REQ14_ACCOUNTING_GAP_STUDY_INDEPENDENT_HUMAN_REVIEW_PACKAGE_VERIFIER=PASS"
)

print(
    "PACKAGE_STATUS=BLANK_AWAITING_INDEPENDENT_HUMAN_REVIEW"
)

print("REVIEW_SUBJECT_STATUS=AUTHOR_CANDIDATE")

print(
    "REVIEW_SUBJECT_RESULT="
    "EVIDENCE_GAP_CONFIRMED_ACQUISITION_SPECIFICATION_READY"
)

print("REVIEW_ITEM_COUNT=9")

print("REVIEWER_NAME_PREFILLED=NO")
print("REVIEWER_ROLE_PREFILLED=NO")
print("REVIEWER_CONFIRMATION_PREFILLED=NO")
print("REVIEW_DATE_PREFILLED=NO")
print("INDEPENDENCE_ATTESTATION_PREFILLED=NO")
print("ITEM_DECISIONS_PREFILLED=NO")
print("REVIEWER_NOTES_PREFILLED=NO")
print("OVERALL_DECISION_PREFILLED=NO")
print("OVERALL_NOTES_PREFILLED=NO")

print("HUMAN_REVIEW_PERFORMED=NO")
print("HUMAN_REVIEW_RECORDED=NO")
print("STUDY_GOVERNANCE_ADOPTED=NO")

print("ACTUAL_ACCOUNTING_EVIDENCE_ACQUISITION_AUTHORIZED=NO")
print("ACTUAL_ACCOUNTING_EVIDENCE_ACQUISITION_PERFORMED=NO")
print("CONCRETE_ACCOUNTING_INSTANCE_CREATED=NO")
print("SOURCE_UNIT_TO_SCHEMA_CARRIER_MAPPING_CREATED=NO")
print("ACCOUNTING_SATISFACTION_DETERMINATION_AUTHORIZED=NO")
print("ACCOUNTING_SATISFACTION_ESTABLISHED=NO")

print("PAIR_RECLASSIFICATION_PERFORMED=NO")
print("SUPPORTED_BINDING_COUNT=211")
print("UNRESOLVED_BINDING_COUNT=1642")
print("NOT_SUPPORTED_BINDING_COUNT=0")
print("REQ06_REQ14_UNRESOLVED_PAIR_COUNT=218")

print("SCHEMA_V2_LOSSLESSNESS_PROVEN=NO")
print("OPERATIONAL_MAPPING_AUTHORIZED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")

print("DECISION0204_A02_EXECUTION_COUNT=1")
print("DECISION0204_A02_RESULT=PASS")
print("DECISION0204_A02_STATE=PERMANENTLY_RETIRED")
print("DECISION0204_A02_RERUN_AUTHORIZED=NO")
