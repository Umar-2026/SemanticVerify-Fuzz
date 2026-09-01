#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parent

R01 = ROOT / "01_returned_independent_human_review.EXACT_COPY.v1.md"
R02 = ROOT / "02_returned_review_source_binding.v1.json"
R03 = ROOT / "03_decision0210_successor_consumption_record.v1.json"
R04 = ROOT / "04_decision0210_successor_execution_output.EXACT_COPY.v1.txt"
R05 = ROOT / "05_decision0210_successor_consumption_sentinel.EXACT_COPY.v1.json"
R06 = ROOT / "06_returned_review_record_boundary.v1.md"

RETURN_SHA = (
    "39155e0b54cf5372b4b289df50ba4f55730f575fe1b3a2af61b16fa498025412"
)

SUCCESSOR_SHA = (
    "5daf813882132beb325840aad00856a00acabafbdd0f9d5a2eba6c53eb2379d1"
)

expected = {
    "ASER01": "REVISION_REQUIRED",
    "ASER02": "REVISION_REQUIRED",
    "ASER03": "PASS",
    "ASER04": "REVISION_REQUIRED",
    "ASER05": "PASS",
    "ASER06": "PASS",
    "ASER07": "REVISION_REQUIRED",
    "ASER08": "PASS",
    "ASER09": "PASS",
}


def stop(code, detail=""):
    print(
        "STOP|" + code +
        (("|" + detail) if detail else "")
    )
    raise SystemExit(1)


for p in (R01, R02, R03, R04, R05, R06):
    if not p.is_file():
        stop("RECORD_ARTIFACT_MISSING", p.name)

b = R01.read_bytes()

if hashlib.sha256(b).hexdigest() != RETURN_SHA:
    stop("RETURNED_REVIEW_SHA_INVALID")

if len(b) != 12281:
    stop("RETURNED_REVIEW_SIZE_INVALID")

if b.count(b"\r\n") != 140:
    stop("RETURNED_REVIEW_CRLF_INVALID")

text = b.decode("utf-8-sig")
text = text.replace("\r\n", "\n").replace("\r", "\n")

for item, wanted in expected.items():
    m = re.search(
        rf"^## {item}\s+—.*?"
        rf"^Review decision:\s*`(PASS|REVISION_REQUIRED)`",
        text,
        re.M | re.S
    )

    if not m:
        stop(item + "_DECISION_NOT_FOUND")

    if m.group(1) != wanted:
        stop(item + "_DECISION_INVALID")

overall = re.search(
    r"^Overall review decision:\s*"
    r"`(APPROVE_BOUNDED_EVIDENCE_GAP_AND_ACQUISITION_SPECIFICATION_STUDY|REVISION_REQUIRED)`",
    text,
    re.M
)

if not overall or overall.group(1) != "REVISION_REQUIRED":
    stop("OVERALL_REVIEW_DECISION_INVALID")

binding = json.loads(R02.read_text(encoding="utf-8"))
consumption = json.loads(R03.read_text(encoding="utf-8"))
sentinel = json.loads(R05.read_text(encoding="utf-8"))

if binding["authorization"]["symlink_safe_successor_sha256"] != SUCCESSOR_SHA:
    stop("SUCCESSOR_SHA_BINDING_INVALID")

if binding["repository_exact_copy"]["sha256"] != RETURN_SHA:
    stop("RETURN_SHA_BINDING_INVALID")

facts = binding["returned_packet_facts"]

if facts["overall_review_decision"] != "REVISION_REQUIRED":
    stop("PACKET_OVERALL_DECISION_INVALID")

if facts["identity_or_authorship_independently_verified"] is not False:
    stop("IDENTITY_VERIFICATION_CLAIM_INVALID")

if consumption["execution_attempt_count"] != 1:
    stop("SUCCESSOR_EXECUTION_COUNT_INVALID")

if consumption["execution_result"] != "PASS":
    stop("SUCCESSOR_RESULT_INVALID")

if consumption["state"] != "PERMANENTLY_RETIRED":
    stop("SUCCESSOR_STATE_INVALID")

if consumption["rerun_authorized"] is not False:
    stop("SUCCESSOR_RERUN_BOUNDARY_INVALID")

if sentinel["execution_attempt_count"] != 1:
    stop("SENTINEL_EXECUTION_COUNT_INVALID")

if sentinel["execution_result"] != "PASS":
    stop("SENTINEL_RESULT_INVALID")

if sentinel["state"] != "PERMANENTLY_RETIRED":
    stop("SENTINEL_STATE_INVALID")

if sentinel["rerun_authorized"] is not False:
    stop("SENTINEL_RERUN_INVALID")

required_pass = (
    "D0210_SYMLINK_SAFE_EXACT_RETURNED_REVIEW_"
    "RECORDING_SUCCESSOR_VERIFIER=PASS"
)

if required_pass not in R04.read_text(encoding="utf-8"):
    stop("SUCCESSOR_PASS_MARKER_MISSING")

boundary = R06.read_text(encoding="utf-8")

for marker in (
    "`RETURNED_COMPLETED_REVIEW_RECORDED=YES`",
    "`OVERALL_REVIEW_DECISION=REVISION_REQUIRED`",
    "`CORRECTIVE_RESPONSE_REQUIRED=YES`",
    "`STUDY_APPROVED=NO`",
    "`STUDY_GOVERNANCE_ADOPTED=NO`",
):
    if marker not in boundary:
        stop("BOUNDARY_MARKER_MISSING", marker)

print(
    "REQ06_REQ14_ACCOUNTING_GAP_STUDY_RETURNED_REVISION_REQUIRED_HUMAN_REVIEW_RECORD_VERIFIER=PASS"
)

print("RETURNED_COMPLETED_HUMAN_REVIEW_RECORDED=YES")
print("RETURNED_REVIEW_SHA256=" + RETURN_SHA)
print("RETURNED_REVIEW_SIZE=12281")
print("RETURNED_REVIEW_CRLF_COUNT=140")

print("PASS_ITEMS=ASER03,ASER05,ASER06,ASER08,ASER09")
print("REVISION_REQUIRED_ITEMS=ASER01,ASER02,ASER04,ASER07")
print("OVERALL_REVIEW_DECISION=REVISION_REQUIRED")

print("REVIEWER_IDENTITY_FIELDS_ARE_PACKET_FACTS_ONLY=YES")
print("IDENTITY_OR_AUTHORSHIP_INDEPENDENTLY_VERIFIED=NO")

print("DECISION0208_A02_RESULT=FAIL")
print("DECISION0208_A02_STATE=PERMANENTLY_RETIRED")
print("DECISION0208_A02_RERUN_AUTHORIZED=NO")

print("DECISION0210_R05_EXECUTION_ATTEMPT_COUNT=1")
print("DECISION0210_R05_RESULT=PASS")
print("DECISION0210_R05_STATE=PERMANENTLY_RETIRED")
print("DECISION0210_R05_RERUN_AUTHORIZED=NO")

print("CORRECTIVE_RESPONSE_REQUIRED=YES")
print("CORRECTIVE_STUDY_SUCCESSOR_AUTHORIZED=NO")
print("CORRECTIVE_STUDY_SUCCESSOR_AUTHORED=NO")

print("STUDY_APPROVED=NO")
print("STUDY_GOVERNANCE_ADOPTED=NO")

print("REQ06_FAILURE_PROVEN=NO")
print("REQ14_FAILURE_PROVEN=NO")
print("ACCOUNTING_UNSATISFACTION_PROVEN=NO")

print("ACCOUNTING_EVIDENCE_ACQUISITION_AUTHORIZED=NO")
print("ACCOUNTING_SATISFACTION_ESTABLISHED=NO")
print("PAIR_RECLASSIFICATION_PERFORMED=NO")

print("SUPPORTED_BINDING_COUNT=211")
print("UNRESOLVED_BINDING_COUNT=1642")
print("NOT_SUPPORTED_BINDING_COUNT=0")
print("REQ06_REQ14_UNRESOLVED_PAIR_COUNT=218")

print("OPERATIONAL_MAPPING_AUTHORIZED=NO")
print("SCHEMA_V2_LOSSLESSNESS_PROVEN=NO")
print("SCHEMA_V2_MODIFICATION_AUTHORIZED=NO")
print("SCHEMA_SUCCESSOR_AUTHORIZED=NO")
print("CURL_JSON_AUTHORIZED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
