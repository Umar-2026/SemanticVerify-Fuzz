#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent

R01 = HERE / "01_failed_decision0187_a02_execution_output.EXACT_COPY.v1.txt"
R02 = HERE / "02_failed_decision0187_a02_consumption_sentinel.EXACT_COPY.v1.json"
R03 = HERE / "03_failed_a02_root_cause_record.v1.json"
R04 = HERE / "04_authorize_crlf_safe_recording_successor_once.v1.py"
R05 = HERE / "05_recovery_and_successor_authorization_boundary.v1.md"

RETURNED = Path(
    "/openbayes/home/"
    "50_bounded_technical_adjudication_Nadeem_packet."
    "MANUAL_ADJUDICATION_COPY.v1.md"
)

EXPECTED_OUTPUT_SHA = (
    "04df80cb3dd19ee1ac4ef6ce4404853807f09de89584f5281ac16fdbab9d46d0"
)
EXPECTED_SENTINEL_SHA = (
    "dec976a852031b016d75763fe0d764c7430e82eac808db3035981da5d819bce1"
)
EXPECTED_PACKET_SHA = (
    "ad35ddfefea1d79db79e36f24ef823407f977a682efcdf23a98a1cbc5ffd7eda"
)


def stop(code):
    print("STOP|" + code)
    raise SystemExit(1)


for p in (R01, R02, R03, R04, R05):
    if not p.is_file():
        stop("RECOVERY_ARTIFACT_MISSING")

if hashlib.sha256(R01.read_bytes()).hexdigest() != EXPECTED_OUTPUT_SHA:
    stop("FAILED_OUTPUT_COPY_SHA_MISMATCH")

if hashlib.sha256(R02.read_bytes()).hexdigest() != EXPECTED_SENTINEL_SHA:
    stop("FAILED_SENTINEL_COPY_SHA_MISMATCH")

if R01.read_text(encoding="utf-8").strip() != (
    "STOP|PAIR_SEQUENCE_INVALID|count=0 unique=0"
):
    stop("FAILED_OUTPUT_CONTENT_MISMATCH")

root = json.loads(R03.read_text(encoding="utf-8"))

if root["original_verifier_execution_count"] != 1:
    stop("ORIGINAL_EXECUTION_COUNT_INVALID")

if root["original_verifier_execution_result"] != "FAIL":
    stop("ORIGINAL_EXECUTION_RESULT_INVALID")

if root["original_verifier_lifecycle_state"] != "PERMANENTLY_RETIRED":
    stop("ORIGINAL_VERIFIER_NOT_RETIRED")

if root["original_verifier_rerun_authorized"] is not False:
    stop("ORIGINAL_VERIFIER_RERUN_BOUNDARY_INVALID")

if root["root_cause"] != "CRLF_SENSITIVE_D0187_A02_REGEX":
    stop("ROOT_CAUSE_RECORD_INVALID")

if root["original_regex_raw_match_count"] != 0:
    stop("RAW_MATCH_COUNT_INVALID")

if root["normalized_newline_match_count"] != 211:
    stop("NORMALIZED_MATCH_COUNT_INVALID")

if root["crlf_tolerant_regex_match_count"] != 211:
    stop("CRLF_TOLERANT_MATCH_COUNT_INVALID")

if root["returned_packet_structural_invalidity_caused_failure"] is not False:
    stop("INVALID_PACKET_CAUSE_FLAG_INVALID")

raw = RETURNED.read_bytes()

if hashlib.sha256(raw).hexdigest() != EXPECTED_PACKET_SHA:
    stop("RETURNED_PACKET_SHA_MISMATCH")

if len(raw) != 316649:
    stop("RETURNED_PACKET_SIZE_MISMATCH")

if raw.count(b"\r\n") != 4034:
    stop("RETURNED_PACKET_CRLF_COUNT_MISMATCH")

text = raw.decode("utf-8")

sensitive = re.findall(
    r"(?m)^## Candidate Pair ([0-9]{3})[ \t]*$",
    text
)

normalized = re.findall(
    r"(?m)^## Candidate Pair ([0-9]{3})[ \t]*$",
    text.replace("\r\n", "\n").replace("\r", "\n")
)

expected = [f"{i:03d}" for i in range(1, 212)]

if sensitive:
    stop("SENSITIVE_PATTERN_UNEXPECTEDLY_MATCHED")

if normalized != expected:
    stop("NORMALIZED_SEQUENCE_INVALID")

boundary = R05.read_text(encoding="utf-8")

for marker in (
    "PERMANENTLY_RETIRED",
    "Decision0187 A02 MUST NOT be executed again.",
    "successor verifier executed: NO",
    "`SUPPORTED_BINDING` created: NO",
    "analyzer implementation/execution authorized: NO",
    "baseline execution authorized: NO",
    "repair authorized: NO",
):
    if marker not in boundary:
        stop("RECOVERY_BOUNDARY_MARKER_MISSING")

print("D0188_RECOVERY_RECORD_VERIFIER=PASS")
print("D0187_A02_EXECUTION_COUNT=1")
print("D0187_A02_RESULT=FAIL")
print("D0187_A02_STATE=PERMANENTLY_RETIRED")
print("D0187_A02_RERUN_AUTHORIZED=NO")
print("ROOT_CAUSE=CRLF_SENSITIVE_D0187_A02_REGEX")
print("RETURNED_PACKET_STRUCTURAL_INVALIDITY_CAUSED_FAILURE=NO")
print("NORMALIZED_PAIR_COUNT=211")
print("SUCCESSOR_AUTHORED=YES")
print("SUCCESSOR_EXECUTED=NO")
print("PAIR_RECLASSIFICATION_PERFORMED=NO")
print("SUPPORTED_BINDING_CREATED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
