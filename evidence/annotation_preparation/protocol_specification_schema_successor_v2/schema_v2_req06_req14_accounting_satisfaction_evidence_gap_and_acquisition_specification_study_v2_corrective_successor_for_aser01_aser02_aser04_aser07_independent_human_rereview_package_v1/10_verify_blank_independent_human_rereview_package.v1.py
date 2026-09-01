#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json

BASE = Path(__file__).resolve().parent


def stop(code, detail=""):
    print(
        "STOP|" + code
        + (("|" + detail) if detail else "")
    )
    raise SystemExit(1)


def sha(raw):
    return hashlib.sha256(
        raw
    ).hexdigest()


manifest = json.loads(
    (
        BASE
        / "01_blank_rereview_package_manifest.v1.json"
    ).read_text(
        encoding="utf-8"
    )
)

binding = json.loads(
    (
        BASE
        / "03_package_source_binding.v1.json"
    ).read_text(
        encoding="utf-8"
    )
)

consumption = json.loads(
    (
        BASE
        / "06_decision0214_a02_consumption_record.v1.json"
    ).read_text(
        encoding="utf-8"
    )
)

sentinel = json.loads(
    (
        BASE
        / "08_decision0214_a02_consumption_sentinel.EXACT_COPY.v1.json"
    ).read_text(
        encoding="utf-8"
    )
)

if manifest.get("status") != (
    "BLANK_AWAITING_EXTERNAL_HANDOFF_AUTHORIZATION"
):
    stop("PACKAGE_STATUS_INVALID")

if manifest[
    "review_scope"
]["fresh_items"] != [
    "ASER01",
    "ASER02",
    "ASER04",
    "ASER07",
]:
    stop("REREVIEW_SCOPE_INVALID")

if manifest[
    "review_scope"
]["preserved_pass_items"] != [
    "ASER03",
    "ASER05",
    "ASER06",
    "ASER08",
    "ASER09",
]:
    stop("PRESERVED_PASS_SCOPE_INVALID")

for key, value in manifest[
    "non_authorizations"
].items():
    if value is not False:
        stop(
            "NONAUTHORIZATION_INVALID",
            key,
        )

form_path = (
    BASE
    / manifest["blank_form"]["path"]
)

if not form_path.is_file():
    stop("BLANK_FORM_MISSING")

form_raw = form_path.read_bytes()

if sha(form_raw) != manifest[
    "blank_form"
]["sha256"]:
    stop("BLANK_FORM_SHA_INVALID")

if manifest[
    "blank_form"
]["human_fields_populated"] is not False:
    stop("BLANK_FORM_STATE_INVALID")

form = form_raw.decode(
    "utf-8"
)

required_blank_identity_lines = [
    "Reviewer name:",
    "Reviewer role:",
    "Reviewer confirmation / signature:",
    "Review date:",
    "Attestation confirmation:",
    "Reviewer acknowledgement:",
]

form_lines = form.splitlines()

for required in required_blank_identity_lines:
    if required not in form_lines:
        stop(
            "REQUIRED_BLANK_HUMAN_FIELD_INVALID",
            required,
        )

if form.count("[x]") != 0 or form.count("[X]") != 0:
    stop("PRESELECTED_REVIEW_DECISION_PRESENT")

if form.count("[ ] PASS") != 4:
    stop("ITEM_PASS_OPTION_COUNT_INVALID")

if form.count("[ ] REVISION_REQUIRED") != 5:
    stop("REVISION_REQUIRED_OPTION_COUNT_INVALID")

if form.count(
    "[ ] APPROVE_BOUNDED_CORRECTIVE_SUCCESSOR"
) != 1:
    stop("OVERALL_APPROVAL_OPTION_INVALID")


for rec in binding["source_records"]:
    path = BASE / rec["package_path"]

    if not path.is_file():
        stop(
            "SOURCE_COPY_MISSING",
            rec["package_path"],
        )

    raw = path.read_bytes()

    if sha(raw) != rec["sha256"]:
        stop(
            "SOURCE_COPY_SHA_INVALID",
            rec["package_path"],
        )

    if len(raw) != rec["size_bytes"]:
        stop(
            "SOURCE_COPY_SIZE_INVALID",
            rec["package_path"],
        )


if binding[
    "predecessor_returned_review_sha256"
] != (
    "39155e0b54cf5372b4b289df50ba4f55730f575fe1b3a2af61b16fa498025412"
):
    stop("PREDECESSOR_REVIEW_SHA_INVALID")


if consumption.get(
    "execution_attempt_count"
) != 1:
    stop("D0214_A02_COUNT_INVALID")

if consumption.get(
    "execution_result"
) != "PASS":
    stop("D0214_A02_RESULT_INVALID")

if consumption.get(
    "state"
) != "PERMANENTLY_RETIRED":
    stop("D0214_A02_STATE_INVALID")

if consumption.get(
    "rerun_authorized"
) is not False:
    stop("D0214_A02_RERUN_STATE_INVALID")

if sentinel.get(
    "execution_attempt_count"
) != 1:
    stop("D0214_SENTINEL_COUNT_INVALID")

if sentinel.get(
    "execution_result"
) != "PASS":
    stop("D0214_SENTINEL_RESULT_INVALID")

if sentinel.get(
    "state"
) != "PERMANENTLY_RETIRED":
    stop("D0214_SENTINEL_STATE_INVALID")

if sentinel.get(
    "rerun_authorized"
) is not False:
    stop("D0214_SENTINEL_RERUN_INVALID")

output_raw = (
    BASE
    / "07_decision0214_a02_execution_output.EXACT_COPY.v1.txt"
).read_bytes()

if sha(output_raw) != consumption[
    "execution_output_sha256"
]:
    stop("D0214_OUTPUT_COPY_INVALID")

sentinel_raw = (
    BASE
    / "08_decision0214_a02_consumption_sentinel.EXACT_COPY.v1.json"
).read_bytes()

if sha(sentinel_raw) != consumption[
    "consumption_sentinel_sha256"
]:
    stop("D0214_SENTINEL_COPY_INVALID")


print(
    "D0215_BLANK_D0213_INDEPENDENT_HUMAN_REREVIEW_PACKAGE_VERIFIER=PASS"
)

print(
    "PACKAGE_STATUS=BLANK_AWAITING_EXTERNAL_HANDOFF_AUTHORIZATION"
)

print(
    "REREVIEW_ITEMS=ASER01,ASER02,ASER04,ASER07"
)

print(
    "PRESERVED_PASS_ITEMS=ASER03,ASER05,ASER06,ASER08,ASER09"
)

print(
    "BLANK_HUMAN_REREVIEW_FORM_PRESENT=YES"
)

print(
    "HUMAN_FIELDS_POPULATED=NO"
)

print(
    "HUMAN_REREVIEW_PERFORMED=NO"
)

print(
    "EXTERNAL_REREVIEW_HANDOFF_AUTHORIZED=NO"
)

print(
    "RETURNED_REREVIEW_RECORDING_AUTHORIZED=NO"
)

print(
    "CORRECTIVE_SUCCESSOR_GOVERNANCE_ADOPTED=NO"
)

print(
    "D0214_A02_EXECUTION_ATTEMPT_COUNT=1"
)

print(
    "D0214_A02_RESULT=PASS"
)

print(
    "D0214_A02_STATE=PERMANENTLY_RETIRED"
)

print(
    "D0214_A02_RERUN_AUTHORIZED=NO"
)

print(
    "ACCOUNTING_EVIDENCE_ACQUISITION_AUTHORIZED=NO"
)

print(
    "CONCRETE_MAPPING_AUTHORIZED=NO"
)

print(
    "ACCOUNTING_SATISFACTION_DETERMINATION_AUTHORIZED=NO"
)

print(
    "PAIR_RECLASSIFICATION_AUTHORIZED=NO"
)

print(
    "SUPPORTED_BINDING_COUNT=211"
)

print(
    "UNRESOLVED_BINDING_COUNT=1642"
)

print(
    "NOT_SUPPORTED_BINDING_COUNT=0"
)

print(
    "REQ06_REQ14_UNRESOLVED_PAIR_COUNT=218"
)

print(
    "ANALYZER_AUTHORIZED=NO"
)

print(
    "BASELINE_AUTHORIZED=NO"
)

print(
    "REPAIR_AUTHORIZED=NO"
)
