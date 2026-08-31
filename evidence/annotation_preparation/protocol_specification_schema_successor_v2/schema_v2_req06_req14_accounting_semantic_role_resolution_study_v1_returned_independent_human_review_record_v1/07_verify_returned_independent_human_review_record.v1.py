#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent

R01 = HERE / "01_returned_independent_human_review.EXACT_COPY.v1.md"
R02 = HERE / "02_returned_independent_human_review_record_manifest.v1.json"
R03 = HERE / "03_decision0198_a02_consumption_record.v1.json"
R04 = HERE / "04_decision0198_a02_execution_output.EXACT_COPY.v1.txt"
R05 = HERE / "05_decision0198_a02_consumption_sentinel.EXACT_COPY.v1.json"
R06 = HERE / "06_returned_independent_human_review_recording_boundary.v1.md"

REVIEW_SHA = (
    "a3a9f38ed79b3fa450d6799677b986b690a02f235ef21acf93cb5b75d2423309"
)
REVIEW_SIZE = 9578

OUTPUT_SHA = (
    "8aae1836a07f67f4c39fca1212f6f596c145977f55a03f679cdc7556fe8a3705"
)

SENTINEL_SHA = (
    "3d33683cd6c1a0701ab5331cca8e05486e23faf825c05b63762e11c2e81e624b"
)

A02_SHA = (
    "e75ad34e85d7050ef27c41f285e08e01fc7e74685de3dda2ec7eb905b63264a4"
)


def stop(code, detail=""):
    print("STOP|" + code + (("|" + detail) if detail else ""))
    raise SystemExit(1)


def clean(value):
    value = value.strip()

    if (
        len(value) >= 2
        and value.startswith("`")
        and value.endswith("`")
    ):
        return value[1:-1].strip()

    return value


def next_value(lines, label):
    hits = [
        i for i, line in enumerate(lines)
        if line.startswith(label)
    ]

    if len(hits) != 1:
        stop("FIELD_COUNT_INVALID", label)

    i = hits[0]
    inline = clean(lines[i][len(label):])

    if inline:
        return inline

    j = i + 1

    while j < len(lines) and not lines[j].strip():
        j += 1

    if j >= len(lines):
        stop("FIELD_BLANK", label)

    value = clean(lines[j])

    if not value or value.startswith("#") or value == "---":
        stop("FIELD_BLANK", label)

    return value


for path in (R01, R02, R03, R04, R05, R06):
    if not path.is_file():
        stop("REQUIRED_RECORD_ARTIFACT_MISSING", str(path))

raw = R01.read_bytes()

if hashlib.sha256(raw).hexdigest() != REVIEW_SHA:
    stop("RECORDED_REVIEW_SHA_MISMATCH")

if len(raw) != REVIEW_SIZE:
    stop("RECORDED_REVIEW_SIZE_MISMATCH")

if raw.count(b"\r\n") == 0:
    stop("RECORDED_REVIEW_CRLF_NOT_PRESERVED")

if raw.count(b"\n") != raw.count(b"\r\n"):
    stop("RECORDED_REVIEW_LINE_ENDINGS_CHANGED")

if raw.count(b"\r") != raw.count(b"\r\n"):
    stop("RECORDED_REVIEW_LINE_ENDINGS_CHANGED")

manifest = json.loads(R02.read_text(encoding="utf-8"))
consumption = json.loads(R03.read_text(encoding="utf-8"))
sentinel = json.loads(R05.read_text(encoding="utf-8"))

if manifest.get("status") != (
    "RETURNED_INDEPENDENT_HUMAN_REVIEW_RECORDED_AWAITING_SEPARATE_GOVERNANCE_ADOPTION_DECISION"
):
    stop("RECORD_STATUS_INVALID")

recovery = manifest.get("recording_recovery", {})

if recovery.get("prior_attempt_a02_consumed") is not True:
    stop("RECOVERY_A02_CONSUMPTION_STATE_INVALID")

if recovery.get("prior_attempt_a02_result") != "PASS":
    stop("RECOVERY_A02_RESULT_INVALID")

if recovery.get("prior_attempt_commit_created") is not False:
    stop("RECOVERY_PRIOR_COMMIT_STATE_INVALID")

if recovery.get("a02_rerun_performed") is not False:
    stop("RECOVERY_ILLEGAL_A02_RERUN_RECORDED")

exact = manifest.get("exact_returned_review", {})

if exact.get("sha256") != REVIEW_SHA:
    stop("MANIFEST_REVIEW_SHA_INVALID")

if exact.get("size_bytes") != REVIEW_SIZE:
    stop("MANIFEST_REVIEW_SIZE_INVALID")

if exact.get("line_ending") != "CRLF":
    stop("MANIFEST_LINE_ENDING_INVALID")

if exact.get("exact_byte_identity_preserved") is not True:
    stop("MANIFEST_BYTE_IDENTITY_INVALID")

if exact.get("line_endings_normalized") is not False:
    stop("MANIFEST_NORMALIZATION_STATE_INVALID")

facts = manifest.get("packet_recorded_review_facts", {})

if facts.get("reviewer_name") != "Muhammad Nadeem Nadir":
    stop("REVIEWER_NAME_INVALID")

if facts.get("reviewer_role") != "Spec-Technical-Adjudicator-1":
    stop("REVIEWER_ROLE_INVALID")

if facts.get("reviewer_confirmation") != "MN_Lodhi":
    stop("REVIEWER_CONFIRMATION_INVALID")

if facts.get("review_date") != "31 / August / 2026":
    stop("REVIEW_DATE_INVALID")

expected_decisions = {
    "ASRR01": "PASS",
    "ASRR02": "PASS",
    "ASRR03": "PASS",
    "ASRR04": "PASS",
    "ASRR05": "PASS",
    "ASRR06": "PASS",
}

if facts.get("review_item_decisions") != expected_decisions:
    stop("ITEM_DECISIONS_INVALID")

if facts.get("pass_count") != 6:
    stop("PASS_COUNT_INVALID")

if facts.get("revision_required_count") != 0:
    stop("REVISION_COUNT_INVALID")

if facts.get("overall_review_decision") != "APPROVE_BOUNDED_ROLE_STUDY":
    stop("OVERALL_DECISION_INVALID")

epi = manifest.get("epistemic_boundary", {})

if epi.get("human_identity_independently_verified") is not False:
    stop("IDENTITY_BOUNDARY_INVALID")

if epi.get(
    "human_authorship_beyond_returned_artifact_independently_proven"
) is not False:
    stop("AUTHORSHIP_BOUNDARY_INVALID")

gov = manifest.get("governance_state", {})

for key in (
    "role_governance_adopted",
    "req06_role_governance_adopted",
    "req14_role_governance_adopted",
    "accounting_satisfaction_established",
    "pair_reclassification_performed",
    "supported_binding_created",
    "not_supported_binding_created",
    "operational_mapping_authorized",
    "schema_v2_losslessness_proven",
    "analyzer_authorized",
    "baseline_authorized",
    "repair_authorized",
):
    if gov.get(key) is not False:
        stop("GOVERNANCE_BOUNDARY_INVALID", key)

if gov.get("supported_binding_count") != 211:
    stop("SUPPORTED_COUNT_INVALID")

if gov.get("unresolved_binding_count") != 1642:
    stop("UNRESOLVED_COUNT_INVALID")

if gov.get("not_supported_binding_count") != 0:
    stop("NOT_SUPPORTED_COUNT_INVALID")

if gov.get("req06_req14_unresolved_pair_count") != 218:
    stop("REQ06_REQ14_UNRESOLVED_COUNT_INVALID")

if consumption.get("verifier_sha256") != A02_SHA:
    stop("D0198_A02_SHA_INVALID")

if consumption.get("execution_count") != 1:
    stop("D0198_A02_EXECUTION_COUNT_INVALID")

if consumption.get("execution_result") != "PASS":
    stop("D0198_A02_RESULT_INVALID")

if consumption.get("lifecycle_state") != "PERMANENTLY_RETIRED":
    stop("D0198_A02_RETIREMENT_INVALID")

if consumption.get("rerun_authorized") is not False:
    stop("D0198_A02_RERUN_BOUNDARY_INVALID")

if consumption.get("rerun_performed_by_recovery") is not False:
    stop("D0198_A02_RECOVERY_RERUN_INVALID")

output_raw = R04.read_bytes()

if hashlib.sha256(output_raw).hexdigest() != OUTPUT_SHA:
    stop("D0198_A02_OUTPUT_SHA_INVALID")

if consumption.get("execution_output_sha256") != OUTPUT_SHA:
    stop("D0198_A02_OUTPUT_BINDING_INVALID")

sentinel_raw = R05.read_bytes()

if hashlib.sha256(sentinel_raw).hexdigest() != SENTINEL_SHA:
    stop("D0198_A02_SENTINEL_SHA_INVALID")

if consumption.get("consumption_sentinel_sha256") != SENTINEL_SHA:
    stop("D0198_A02_SENTINEL_BINDING_INVALID")

if sentinel.get("verifier_sha256") != A02_SHA:
    stop("SENTINEL_VERIFIER_SHA_INVALID")

if sentinel.get("rerun_authorized") is not False:
    stop("SENTINEL_RERUN_INVALID")

review_text = raw.decode("utf-8")
review_lines = review_text.splitlines()

if next_value(review_lines, "Reviewer name:") != "Muhammad Nadeem Nadir":
    stop("EXACT_REVIEW_NAME_INVALID")

if next_value(review_lines, "Reviewer role:") != "Spec-Technical-Adjudicator-1":
    stop("EXACT_REVIEW_ROLE_INVALID")

if next_value(
    review_lines,
    "Reviewer confirmation/signature:"
) != "MN_Lodhi":
    stop("EXACT_REVIEW_CONFIRMATION_INVALID")

if next_value(review_lines, "Review date:") != "31 / August / 2026":
    stop("EXACT_REVIEW_DATE_INVALID")

for item in (
    "ASRR01",
    "ASRR02",
    "ASRR03",
    "ASRR04",
    "ASRR05",
    "ASRR06",
):
    match = re.search(
        rf"^## {item} .*?(?=^## |\Z)",
        review_text,
        re.MULTILINE | re.DOTALL
    )

    if not match:
        stop("EXACT_REVIEW_ITEM_MISSING", item)

    section = match.group(0).splitlines()

    if next_value(section, "Review decision:") != "PASS":
        stop("EXACT_REVIEW_ITEM_NOT_PASS", item)

    if not next_value(section, "Reviewer notes:"):
        stop("EXACT_REVIEW_ITEM_NOTES_BLANK", item)

if next_value(
    review_lines,
    "Overall review decision:"
) != "APPROVE_BOUNDED_ROLE_STUDY":
    stop("EXACT_REVIEW_OVERALL_DECISION_INVALID")

if not next_value(review_lines, "Overall reviewer notes:"):
    stop("EXACT_REVIEW_OVERALL_NOTES_BLANK")

if manifest.get("next_boundary") != (
    "SEPARATELY_AUTHORIZE_GOVERNANCE_ADOPTION_OF_RECORDED_BOUNDED_ROLE_STUDY_REVIEW"
):
    stop("NEXT_BOUNDARY_INVALID")

print("REQ06_REQ14_RETURNED_INDEPENDENT_HUMAN_REVIEW_RECORD_VERIFIER=PASS")
print("RECORD_STATUS=RETURNED_INDEPENDENT_HUMAN_REVIEW_RECORDED_AWAITING_SEPARATE_GOVERNANCE_ADOPTION_DECISION")
print("EXACT_RETURNED_REVIEW_SHA256=" + REVIEW_SHA)
print("EXACT_RETURNED_REVIEW_SIZE=9578")
print("EXACT_RETURNED_REVIEW_LINE_ENDING=CRLF")
print("EXACT_BYTE_IDENTITY_PRESERVED=YES")
print("RETURNED_REVIEW_RECORDED=YES")
print("PACKET_RECORDED_REVIEWER_NAME=Muhammad Nadeem Nadir")
print("PACKET_RECORDED_REVIEWER_ROLE=Spec-Technical-Adjudicator-1")
print("PACKET_RECORDED_REVIEWER_CONFIRMATION=MN_Lodhi")
print("PACKET_RECORDED_REVIEW_DATE=31 / August / 2026")
print("PACKET_RECORDED_INDEPENDENCE_ATTESTATION=YES")
print("HUMAN_IDENTITY_INDEPENDENTLY_VERIFIED=NO")
print("HUMAN_AUTHORSHIP_BEYOND_RETURNED_ARTIFACT_INDEPENDENTLY_PROVEN=NO")
print("REVIEW_ITEM_COUNT=6")
print("REVIEW_ITEM_PASS_COUNT=6")
print("REVIEW_ITEM_REVISION_REQUIRED_COUNT=0")
print("OVERALL_REVIEW_DECISION=APPROVE_BOUNDED_ROLE_STUDY")
print("DECISION0198_A02_EXECUTION_COUNT=1")
print("DECISION0198_A02_RESULT=PASS")
print("DECISION0198_A02_STATE=PERMANENTLY_RETIRED")
print("DECISION0198_A02_RERUN_AUTHORIZED=NO")
print("DECISION0198_A02_RERUN_PERFORMED_BY_RECOVERY=NO")
print("ROLE_GOVERNANCE_ADOPTED=NO")
print("REQ06_ROLE_GOVERNANCE_ADOPTED=NO")
print("REQ14_ROLE_GOVERNANCE_ADOPTED=NO")
print("ACCOUNTING_SATISFACTION_ESTABLISHED=NO")
print("PAIR_RECLASSIFICATION_PERFORMED=NO")
print("SUPPORTED_BINDING_COUNT=211")
print("UNRESOLVED_BINDING_COUNT=1642")
print("NOT_SUPPORTED_BINDING_COUNT=0")
print("REQ06_REQ14_UNRESOLVED_PAIR_COUNT=218")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
