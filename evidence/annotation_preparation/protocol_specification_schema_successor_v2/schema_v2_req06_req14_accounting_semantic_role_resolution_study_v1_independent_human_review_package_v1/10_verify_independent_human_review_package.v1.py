#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent

P01 = HERE / "01_independent_human_review_package_manifest.v1.json"
P02 = HERE / "02_req06_req14_accounting_semantic_role_resolution_study.EXACT_COPY.v1.json"
P03 = HERE / "03_req06_req14_accounting_role_evidence_anchor_matrix.EXACT_COPY.v1.json"
P04 = HERE / "04_independent_human_review_contract.EXACT_COPY.v1.json"
P05 = HERE / "05_independent_human_reviewer_instructions.v1.md"
P06 = HERE / "06_blank_independent_human_review_form.v1.md"
P07 = HERE / "07_decision0194_a02_consumption_record.v1.json"
P08 = HERE / "08_decision0194_a02_execution_output.EXACT_COPY.v1.txt"
P09 = HERE / "09_decision0194_a02_consumption_sentinel.EXACT_COPY.v1.json"

EXPECTED = {
    P02:
        "22c51d0d77f3faa086cb426788d057da15c5002a29b4ba68cd3177935aa80381",
    P03:
        "a153d0979f4bda119928fb29fd8043088115793f164e268c6d0def6fe1203601",
    P04:
        "1d71a5afb82d7ea7ad5fb882a904879409f0ace0b4c71b0201cf59ea82fd0ac1",
}


def stop(code, detail=""):
    print("STOP|" + code + (("|" + detail) if detail else ""))
    raise SystemExit(1)


for path in (
    P01, P02, P03, P04, P05,
    P06, P07, P08, P09
):
    if not path.is_file():
        stop("PACKAGE_ARTIFACT_MISSING", str(path))

for path, expected_sha in EXPECTED.items():
    actual = hashlib.sha256(path.read_bytes()).hexdigest()

    if actual != expected_sha:
        stop("EXACT_COPY_SHA_MISMATCH", str(path))

manifest = json.loads(
    P01.read_text(encoding="utf-8")
)
study = json.loads(
    P02.read_text(encoding="utf-8")
)
evidence = json.loads(
    P03.read_text(encoding="utf-8")
)
contract = json.loads(
    P04.read_text(encoding="utf-8")
)
consumption = json.loads(
    P07.read_text(encoding="utf-8")
)
sentinel = json.loads(
    P09.read_text(encoding="utf-8")
)

if manifest.get("status") != (
    "BLANK_AWAITING_INDEPENDENT_HUMAN_REVIEW"
):
    stop("PACKAGE_STATUS_INVALID")

if study.get("status") != "AUTHOR_CANDIDATE":
    stop("STUDY_STATUS_CHANGED")

if study.get(
    "global_author_candidate_result", {}
).get("governance_adopted") is not False:
    stop("STUDY_PREMATURELY_ADOPTED")

if evidence.get("status") != (
    "AUTHOR_CANDIDATE_SUPPORTING_EVIDENCE"
):
    stop("EVIDENCE_STATUS_CHANGED")

items = contract.get("required_review_items")

if not isinstance(items, list) or len(items) != 6:
    stop("REVIEW_CONTRACT_ITEM_COUNT_INVALID")

if [x.get("review_item_id") for x in items] != [
    "ASRR01",
    "ASRR02",
    "ASRR03",
    "ASRR04",
    "ASRR05",
    "ASRR06",
]:
    stop("REVIEW_CONTRACT_ITEM_SEQUENCE_INVALID")

human_state = manifest.get(
    "human_field_state",
    {}
)

for key in (
    "reviewer_identity_prefilled",
    "reviewer_role_prefilled",
    "review_item_decisions_prefilled",
    "reviewer_notes_prefilled",
    "overall_decision_prefilled",
    "reviewer_confirmation_prefilled",
    "review_date_prefilled",
    "attestation_prefilled",
):
    if human_state.get(key) is not False:
        stop("MANIFEST_HUMAN_FIELD_PREPOPULATED", key)

review_state = manifest.get(
    "review_state",
    {}
)

for key in (
    "human_review_performed",
    "human_review_recorded",
    "role_governance_adopted",
):
    if review_state.get(key) is not False:
        stop("REVIEW_STATE_PREMATURE", key)

technical = manifest.get(
    "technical_state",
    {}
)

for key in (
    "pair_reclassification_performed",
    "supported_binding_created",
    "not_supported_binding_created",
    "accounting_satisfaction_established",
    "operational_mapping_created",
    "schema_v2_losslessness_proven",
    "analyzer_authorized",
    "baseline_authorized",
    "repair_authorized",
):
    if technical.get(key) is not False:
        stop("PACKAGE_TECHNICAL_BOUNDARY_INVALID", key)

if consumption.get("execution_count") != 1:
    stop("D0194_A02_EXECUTION_COUNT_INVALID")

if consumption.get("execution_result") != "PASS":
    stop("D0194_A02_RESULT_INVALID")

if consumption.get(
    "lifecycle_state"
) != "PERMANENTLY_RETIRED":
    stop("D0194_A02_NOT_RETIRED")

if consumption.get("rerun_authorized") is not False:
    stop("D0194_A02_RERUN_BOUNDARY_INVALID")

if consumption.get("verifier_sha256") != (
    "fa6e6fcda547381796c6b05b90e634c4581de195ac286cb6fa84e7057ed0be17"
):
    stop("D0194_A02_SHA_BINDING_INVALID")

output_raw = P08.read_bytes()

if hashlib.sha256(output_raw).hexdigest() != consumption.get(
    "execution_output_sha256"
):
    stop("D0194_A02_OUTPUT_BINDING_INVALID")

for marker in (
    "DECISION0194_REVIEW_PACKAGE_AUTHORIZATION_VERIFIER=PASS",
    "REVIEW_SUBJECT_STATUS=AUTHOR_CANDIDATE",
    "REVIEW_ITEM_COUNT=6",
    "INDEPENDENT_HUMAN_REVIEW_PACKAGE_AUTHORIZED=YES",
    "HUMAN_REVIEW_PERFORMED_BY_THIS_VERIFIER=NO",
    "REVIEWER_IDENTITY_SYNTHESIZED=NO",
    "REVIEWER_DECISION_SYNTHESIZED=NO",
    "AUTHORIZATION_EXECUTION_COUNT_FOR_THIS_RUN=1",
    "AUTHORIZATION_RERUN_AUTHORIZED=NO",
):
    if marker not in output_raw.decode("utf-8"):
        stop("D0194_A02_OUTPUT_MARKER_MISSING", marker)

sentinel_raw = P09.read_bytes()

if hashlib.sha256(sentinel_raw).hexdigest() != consumption.get(
    "consumption_sentinel_sha256"
):
    stop("D0194_A02_SENTINEL_BINDING_INVALID")

if sentinel.get("rerun_authorized") is not False:
    stop("D0194_A02_SENTINEL_RERUN_INVALID")

form_lines = P06.read_text(
    encoding="utf-8"
).splitlines()

single_blank = (
    "Reviewer name:",
    "Reviewer role:",
    "Reviewer confirmation/signature:",
    "Review date:",
    "Independent-review attestation:",
    "Overall review decision:",
    "Overall reviewer notes:",
)

for prefix in single_blank:
    hits = [
        line
        for line in form_lines
        if line.startswith(prefix)
    ]

    if len(hits) != 1:
        stop("BLANK_FORM_FIELD_COUNT_INVALID", prefix)

    if hits[0] != prefix:
        stop("BLANK_FORM_FIELD_PREPOPULATED", prefix)

review_decisions = [
    line
    for line in form_lines
    if line.startswith("Review decision:")
]

if len(review_decisions) != 6:
    stop(
        "BLANK_FORM_REVIEW_DECISION_COUNT_INVALID",
        str(len(review_decisions))
    )

if any(
    line != "Review decision:"
    for line in review_decisions
):
    stop("BLANK_FORM_REVIEW_DECISION_PREPOPULATED")

notes = [
    line
    for line in form_lines
    if line.startswith("Reviewer notes:")
]

if len(notes) != 6:
    stop(
        "BLANK_FORM_REVIEWER_NOTES_COUNT_INVALID",
        str(len(notes))
    )

if any(
    line != "Reviewer notes:"
    for line in notes
):
    stop("BLANK_FORM_REVIEWER_NOTES_PREPOPULATED")

for item in (
    "ASRR01",
    "ASRR02",
    "ASRR03",
    "ASRR04",
    "ASRR05",
    "ASRR06",
):
    count = sum(
        1
        for line in form_lines
        if line.startswith("## " + item + " ")
    )

    if count != 1:
        stop("BLANK_FORM_REVIEW_ITEM_INVALID", item)

print("REQ06_REQ14_INDEPENDENT_HUMAN_REVIEW_PACKAGE_VERIFIER=PASS")
print("PACKAGE_STATUS=BLANK_AWAITING_INDEPENDENT_HUMAN_REVIEW")
print("REVIEW_SUBJECT_STATUS=AUTHOR_CANDIDATE")
print("REVIEW_ITEM_COUNT=6")
print("REVIEWER_IDENTITY_PREFILLED=NO")
print("REVIEWER_ROLE_PREFILLED=NO")
print("REVIEWER_DECISIONS_PREFILLED=NO")
print("REVIEWER_NOTES_PREFILLED=NO")
print("REVIEWER_CONFIRMATION_PREFILLED=NO")
print("REVIEW_DATE_PREFILLED=NO")
print("REVIEW_ATTESTATION_PREFILLED=NO")
print("HUMAN_REVIEW_PERFORMED=NO")
print("HUMAN_REVIEW_RECORDED=NO")
print("ROLE_GOVERNANCE_ADOPTED=NO")
print("PAIR_RECLASSIFICATION_PERFORMED=NO")
print("ACCOUNTING_SATISFACTION_ESTABLISHED=NO")
print("DECISION0194_A02_EXECUTION_COUNT=1")
print("DECISION0194_A02_RESULT=PASS")
print("DECISION0194_A02_STATE=PERMANENTLY_RETIRED")
print("DECISION0194_A02_RERUN_AUTHORIZED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
