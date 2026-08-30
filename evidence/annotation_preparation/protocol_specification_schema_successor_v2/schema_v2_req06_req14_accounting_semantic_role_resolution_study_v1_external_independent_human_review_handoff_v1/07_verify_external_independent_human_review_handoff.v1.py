#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

H01 = HERE / "01_external_independent_human_review_handoff_manifest.v1.json"
H02 = HERE / "02_review_package_source_binding.v1.json"
H03 = HERE / "03_decision0196_a02_consumption_record.v1.json"
H04 = HERE / "04_decision0196_a02_execution_output.EXACT_COPY.v1.txt"
H05 = HERE / "05_decision0196_a02_consumption_sentinel.EXACT_COPY.v1.json"
H06 = HERE / "06_external_handoff_boundary_and_return_instructions.v1.md"

PACKAGE_DIR = ROOT / (
    "schema_v2_req06_req14_accounting_semantic_role_resolution_"
    "study_v1_independent_human_review_package_v1"
)

P01 = PACKAGE_DIR / "01_independent_human_review_package_manifest.v1.json"
P06 = PACKAGE_DIR / "06_blank_independent_human_review_form.v1.md"

EXPECTED = {
    P01:
        "5eda213520d4d4032d932ed3c03fe0fe8dd7a0d34eb6e89191bf624e4dec3da2",
    P06:
        "c1ccf931d1d34ddacf80bcba47bf0d9adf1d109db5926a7c9ad8e068ad9e7faa",
}


def stop(code, detail=""):
    print("STOP|" + code + (("|" + detail) if detail else ""))
    raise SystemExit(1)


for path in (H01, H02, H03, H04, H05, H06, P01, P06):
    if not path.is_file():
        stop("REQUIRED_HANDOFF_ARTIFACT_MISSING", str(path))

for path, expected_sha in EXPECTED.items():
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != expected_sha:
        stop("BOUND_PACKAGE_SHA_MISMATCH", str(path))

manifest = json.loads(H01.read_text(encoding="utf-8"))
binding = json.loads(H02.read_text(encoding="utf-8"))
consumption = json.loads(H03.read_text(encoding="utf-8"))
sentinel = json.loads(H05.read_text(encoding="utf-8"))
package = json.loads(P01.read_text(encoding="utf-8"))

if manifest.get("status") != (
    "EXTERNAL_HANDOFF_AUTHORED_AWAITING_INDEPENDENT_HUMAN_REVIEW_RETURN"
):
    stop("HANDOFF_STATUS_INVALID")

if manifest.get("authorizing_decision") != "0196":
    stop("HANDOFF_AUTHORIZATION_BINDING_INVALID")

if manifest.get("authoring_decision") != "0197":
    stop("HANDOFF_AUTHORING_DECISION_INVALID")

if manifest.get("next_boundary") != (
    "AWAIT_EXTERNAL_INDEPENDENT_HUMAN_REVIEW_RETURN"
):
    stop("HANDOFF_NEXT_BOUNDARY_INVALID")

if package.get("status") != (
    "BLANK_AWAITING_INDEPENDENT_HUMAN_REVIEW"
):
    stop("SOURCE_PACKAGE_STATUS_CHANGED")

external = manifest.get("external_artifacts", {})
editable = external.get("editable_review_form", {})
zip_record = external.get("zip", {})

if editable.get("initial_sha256") != (
    "c1ccf931d1d34ddacf80bcba47bf0d9adf1d109db5926a7c9ad8e068ad9e7faa"
):
    stop("EDITABLE_INITIAL_SHA_BINDING_INVALID")

if editable.get("initial_human_fields_blank") is not True:
    stop("EDITABLE_INITIAL_BLANK_STATE_INVALID")

if not isinstance(zip_record.get("sha256"), str) or len(zip_record["sha256"]) != 64:
    stop("EXTERNAL_ZIP_SHA_RECORD_INVALID")

source_binding = binding.get(
    "external_editable_review_form",
    {}
)

if source_binding.get(
    "initially_byte_identical_to_repository_blank_form"
) is not True:
    stop("EDITABLE_SOURCE_BYTE_IDENTITY_NOT_RECORDED")

if source_binding.get("initial_sha256") != (
    "c1ccf931d1d34ddacf80bcba47bf0d9adf1d109db5926a7c9ad8e068ad9e7faa"
):
    stop("EDITABLE_SOURCE_SHA_INVALID")

if binding.get(
    "external_zip", {}
).get(
    "contents_byte_identical_to_repository_review_package"
) is not True:
    stop("ZIP_SOURCE_IDENTITY_NOT_RECORDED")

human = manifest.get("human_review_state", {})

for key in (
    "reviewer_identity_supplied",
    "reviewer_role_supplied",
    "review_item_decisions_supplied",
    "reviewer_notes_supplied",
    "overall_decision_supplied",
    "reviewer_confirmation_supplied",
    "review_date_supplied",
    "attestation_supplied",
    "human_review_performed",
    "human_review_recorded",
):
    if human.get(key) is not False:
        stop("HANDOFF_HUMAN_STATE_PREMATURE", key)

governance = manifest.get("governance_state", {})

for key in (
    "role_governance_adopted",
    "accounting_satisfaction_established",
    "pair_reclassification_performed",
    "supported_binding_created",
    "not_supported_binding_created",
    "operational_mapping_authorized",
    "analyzer_authorized",
    "baseline_authorized",
    "repair_authorized",
):
    if governance.get(key) is not False:
        stop("HANDOFF_GOVERNANCE_BOUNDARY_INVALID", key)

if consumption.get("execution_count") != 1:
    stop("D0196_A02_EXECUTION_COUNT_INVALID")

if consumption.get("execution_result") != "PASS":
    stop("D0196_A02_RESULT_INVALID")

if consumption.get("lifecycle_state") != "PERMANENTLY_RETIRED":
    stop("D0196_A02_NOT_RETIRED")

if consumption.get("rerun_authorized") is not False:
    stop("D0196_A02_RERUN_BOUNDARY_INVALID")

if consumption.get("verifier_sha256") != (
    "ab7e1fcafcc5c799acd769fd6bce012123d967cf61d7ff5e888fc6e0d86be7be"
):
    stop("D0196_A02_SHA_BINDING_INVALID")

output_raw = H04.read_bytes()

if hashlib.sha256(output_raw).hexdigest() != consumption.get(
    "execution_output_sha256"
):
    stop("D0196_A02_OUTPUT_BINDING_INVALID")

for marker in (
    "DECISION0196_EXTERNAL_HANDOFF_AUTHORIZATION_VERIFIER=PASS",
    "EXTERNAL_INDEPENDENT_HUMAN_REVIEW_HANDOFF_AUTHORIZED=YES",
    "HUMAN_REVIEW_PERFORMED_BY_THIS_VERIFIER=NO",
    "HUMAN_REVIEW_RECORDED_BY_THIS_VERIFIER=NO",
    "AUTHORIZATION_EXECUTION_COUNT_FOR_THIS_RUN=1",
    "AUTHORIZATION_RERUN_AUTHORIZED=NO",
):
    if marker not in output_raw.decode("utf-8"):
        stop("D0196_A02_OUTPUT_MARKER_MISSING", marker)

sentinel_raw = H05.read_bytes()

if hashlib.sha256(sentinel_raw).hexdigest() != consumption.get(
    "consumption_sentinel_sha256"
):
    stop("D0196_A02_SENTINEL_BINDING_INVALID")

if sentinel.get("rerun_authorized") is not False:
    stop("D0196_A02_SENTINEL_RERUN_INVALID")

print("REQ06_REQ14_EXTERNAL_INDEPENDENT_HUMAN_REVIEW_HANDOFF_VERIFIER=PASS")
print("HANDOFF_STATUS=EXTERNAL_HANDOFF_AUTHORED_AWAITING_INDEPENDENT_HUMAN_REVIEW_RETURN")
print("REVIEW_ITEM_COUNT=6")
print("EXTERNAL_ZIP_RECORDED=YES")
print("EXTERNAL_EDITABLE_INITIAL_SHA_BOUND_TO_BLANK_FORM=YES")
print("REPOSITORY_BLANK_FORM_IMMUTABLE=YES")
print("HUMAN_REVIEW_PERFORMED=NO")
print("HUMAN_REVIEW_RECORDED=NO")
print("ROLE_GOVERNANCE_ADOPTED=NO")
print("PAIR_RECLASSIFICATION_PERFORMED=NO")
print("ACCOUNTING_SATISFACTION_ESTABLISHED=NO")
print("DECISION0196_A02_EXECUTION_COUNT=1")
print("DECISION0196_A02_RESULT=PASS")
print("DECISION0196_A02_STATE=PERMANENTLY_RETIRED")
print("DECISION0196_A02_RERUN_AUTHORIZED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
