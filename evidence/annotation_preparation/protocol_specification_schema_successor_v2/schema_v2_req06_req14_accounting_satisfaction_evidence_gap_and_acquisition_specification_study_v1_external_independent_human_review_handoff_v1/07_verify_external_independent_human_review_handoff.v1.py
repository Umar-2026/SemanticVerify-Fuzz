#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

PACKAGE_DIR = ROOT / (
    "schema_v2_req06_req14_accounting_satisfaction_"
    "evidence_gap_and_acquisition_specification_study_v1_"
    "independent_human_review_package_v1"
)

H01 = HERE / "01_external_independent_human_review_handoff_manifest.v1.json"
H02 = HERE / "02_review_package_source_binding.v1.json"
H03 = HERE / "03_decision0206_a02_consumption_record.v1.json"
H04 = HERE / "04_decision0206_a02_execution_output.EXACT_COPY.v1.txt"
H05 = HERE / "05_decision0206_a02_consumption_sentinel.EXACT_COPY.v1.json"
H06 = HERE / "06_external_handoff_boundary_and_return_instructions.v1.md"

P09 = PACKAGE_DIR / "09_blank_independent_human_review_form.v1.md"

EXPECTED_BLANK_SHA = (
    "718483ff141ee7787cf2d3d9d2e64f75a33e8ef2643e78df35de73f5e6da402a"
)


def stop(code, detail=""):
    print(
        "STOP|" + code
        + (("|" + detail) if detail else "")
    )
    raise SystemExit(1)


for path in (H01, H02, H03, H04, H05, H06, P09):
    if not path.is_file():
        stop("REQUIRED_ARTIFACT_MISSING", str(path))

manifest = json.loads(
    H01.read_text(encoding="utf-8")
)

binding = json.loads(
    H02.read_text(encoding="utf-8")
)

consumption = json.loads(
    H03.read_text(encoding="utf-8")
)

if manifest.get("handoff_status") != (
    "EXTERNAL_HANDOFF_AUTHORED_AWAITING_INDEPENDENT_HUMAN_REVIEW_RETURN"
):
    stop("HANDOFF_STATUS_INVALID")

subject = manifest.get("review_subject", {})

if subject.get("status") != "AUTHOR_CANDIDATE":
    stop("REVIEW_SUBJECT_STATUS_INVALID")

if subject.get("result") != (
    "EVIDENCE_GAP_CONFIRMED_ACQUISITION_SPECIFICATION_READY"
):
    stop("REVIEW_SUBJECT_RESULT_INVALID")

if subject.get("review_item_count") != 9:
    stop("REVIEW_ITEM_COUNT_INVALID")

source = manifest.get("source_package", {})

if source.get("review_package_tree") != (
    "07777d8b68eec2537f530f9f10c6c295de8524aa"
):
    stop("SOURCE_PACKAGE_TREE_INVALID")

if source.get("blank_review_form_sha256") != EXPECTED_BLANK_SHA:
    stop("SOURCE_BLANK_FORM_SHA_INVALID")

external_zip = manifest.get("external_zip", {})

if not str(external_zip.get("sha256", "")).strip():
    stop("EXTERNAL_ZIP_SHA_NOT_RECORDED")

if external_zip.get("entry_count") != 14:
    stop("EXTERNAL_ZIP_ENTRY_COUNT_INVALID")

if external_zip.get(
    "all_entries_verified_byte_identical_to_repository_sources"
) is not True:
    stop("EXTERNAL_ZIP_BYTE_IDENTITY_RECORD_INVALID")

editable = manifest.get(
    "external_editable_review_form",
    {}
)

if editable.get("initial_sha256") != EXPECTED_BLANK_SHA:
    stop("EXTERNAL_EDITABLE_INITIAL_SHA_INVALID")

if editable.get(
    "initial_bytes_equal_immutable_blank_form"
) is not True:
    stop("EXTERNAL_EDITABLE_INITIAL_IDENTITY_INVALID")

if editable.get(
    "repository_blank_form_remains_immutable"
) is not True:
    stop("REPOSITORY_BLANK_IMMUTABILITY_INVALID")

if hashlib.sha256(P09.read_bytes()).hexdigest() != EXPECTED_BLANK_SHA:
    stop("REPOSITORY_BLANK_FORM_CHANGED")

files = binding.get("files", [])

if len(files) != 14:
    stop("SOURCE_BINDING_FILE_COUNT_INVALID")

seen = set()

for item in files:
    name = item.get("name")
    expected = item.get("sha256")

    if not name or not expected:
        stop("SOURCE_BINDING_ITEM_INVALID")

    if name in seen:
        stop("SOURCE_BINDING_DUPLICATE", name)

    seen.add(name)

    path = PACKAGE_DIR / name

    if not path.is_file():
        stop("SOURCE_PACKAGE_FILE_MISSING", name)

    actual = hashlib.sha256(path.read_bytes()).hexdigest()

    if actual != expected:
        stop("SOURCE_PACKAGE_FILE_SHA_MISMATCH", name)

if consumption.get("execution_count") != 1:
    stop("D0206_A02_EXECUTION_COUNT_INVALID")

if consumption.get("execution_result") != "PASS":
    stop("D0206_A02_RESULT_INVALID")

if consumption.get("lifecycle_state") != "PERMANENTLY_RETIRED":
    stop("D0206_A02_RETIREMENT_INVALID")

if consumption.get("rerun_authorized") is not False:
    stop("D0206_A02_RERUN_BOUNDARY_INVALID")

if hashlib.sha256(H04.read_bytes()).hexdigest() != consumption.get(
    "execution_output_sha256"
):
    stop("D0206_A02_OUTPUT_BINDING_INVALID")

if hashlib.sha256(H05.read_bytes()).hexdigest() != consumption.get(
    "consumption_sentinel_sha256"
):
    stop("D0206_A02_SENTINEL_BINDING_INVALID")

human = manifest.get("human_review_state", {})

for key in (
    "reviewer_identity_preassigned",
    "reviewer_role_preassigned",
    "human_review_performed",
    "human_review_recorded",
    "returned_completed_review_received",
):
    if human.get(key) is not False:
        stop("HUMAN_REVIEW_STATE_INVALID", key)

gov = manifest.get("governance_state", {})

for key in (
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
):
    if gov.get(key) is not False:
        stop("GOVERNANCE_BOUNDARY_INVALID", key)

if gov.get("supported_binding_count") != 211:
    stop("SUPPORTED_BINDING_COUNT_INVALID")

if gov.get("unresolved_binding_count") != 1642:
    stop("UNRESOLVED_BINDING_COUNT_INVALID")

if gov.get("not_supported_binding_count") != 0:
    stop("NOT_SUPPORTED_BINDING_COUNT_INVALID")

if gov.get("req06_req14_unresolved_pair_count") != 218:
    stop("REQ06_REQ14_UNRESOLVED_PAIR_COUNT_INVALID")

boundary = H06.read_text(encoding="utf-8")

for phrase in (
    "genuine independent human reviewer",
    "separately checked before it is recorded",
    "requires a separate governance authorization",
    "does not itself constitute governance adoption",
    "must never be rerun",
):
    if phrase not in boundary:
        stop("HANDOFF_BOUNDARY_MISSING", phrase)

print(
    "REQ06_REQ14_ACCOUNTING_GAP_STUDY_EXTERNAL_INDEPENDENT_HUMAN_REVIEW_HANDOFF_VERIFIER=PASS"
)

print(
    "HANDOFF_STATUS="
    "EXTERNAL_HANDOFF_AUTHORED_AWAITING_INDEPENDENT_HUMAN_REVIEW_RETURN"
)

print("REVIEW_SUBJECT_STATUS=AUTHOR_CANDIDATE")
print("REVIEW_ITEM_COUNT=9")

print("EXTERNAL_ZIP_RECORDED=YES")
print("EXTERNAL_ZIP_ENTRY_COUNT=14")
print("EXTERNAL_ZIP_SOURCE_BINDING_VERIFIED=YES")

print("EXTERNAL_EDITABLE_INITIAL_SHA_BOUND_TO_BLANK_FORM=YES")
print("REPOSITORY_BLANK_FORM_IMMUTABLE=YES")

print("REVIEWER_IDENTITY_PREASSIGNED=NO")
print("REVIEWER_ROLE_PREASSIGNED=NO")

print("HUMAN_REVIEW_PERFORMED=NO")
print("HUMAN_REVIEW_RECORDED=NO")
print("RETURNED_COMPLETED_REVIEW_RECEIVED=NO")

print("STUDY_GOVERNANCE_ADOPTED=NO")
print("ACCOUNTING_SATISFACTION_ESTABLISHED=NO")
print("PAIR_RECLASSIFICATION_PERFORMED=NO")

print("SUPPORTED_BINDING_COUNT=211")
print("UNRESOLVED_BINDING_COUNT=1642")
print("NOT_SUPPORTED_BINDING_COUNT=0")
print("REQ06_REQ14_UNRESOLVED_PAIR_COUNT=218")

print("DECISION0206_A02_EXECUTION_COUNT=1")
print("DECISION0206_A02_RESULT=PASS")
print("DECISION0206_A02_STATE=PERMANENTLY_RETIRED")
print("DECISION0206_A02_RERUN_AUTHORIZED=NO")

print("OPERATIONAL_MAPPING_AUTHORIZED=NO")
print("SCHEMA_V2_LOSSLESSNESS_PROVEN=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
