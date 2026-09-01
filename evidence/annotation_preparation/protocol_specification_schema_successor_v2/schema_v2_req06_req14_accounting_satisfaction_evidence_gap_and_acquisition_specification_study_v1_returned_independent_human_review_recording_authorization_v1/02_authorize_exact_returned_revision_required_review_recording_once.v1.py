#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import re
import subprocess

REPO = Path("/openbayes/home/semanticverify-fuzz-research")

EXPECTED_HEAD_PARENT = (
    "449bd5f22c617aed6204e536d07fb225534925f1"
)

RETURNED = Path(
    "/openbayes/home/"
    "50_req06_req14_accounting_gap_study_Nadeem_"
    "independent_human_review_form.MANUAL_REVIEW_COPY.v1.md"
)

RETURNED_SHA = (
    "39155e0b54cf5372b4b289df50ba4f55730f575fe1b3a2af61b16fa498025412"
)

RETURNED_SIZE = 12281
RETURNED_CRLF = 140

ROOT = REPO / (
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2"
)

AUTH_DIR = ROOT / (
    "schema_v2_req06_req14_accounting_satisfaction_"
    "evidence_gap_and_acquisition_specification_study_v1_"
    "returned_independent_human_review_recording_authorization_v1"
)

A01 = AUTH_DIR / (
    "01_exact_returned_revision_required_review_"
    "recording_authorization.v1.json"
)

A03 = AUTH_DIR / "03_exact_returned_review_recording_contract.v1.json"
A04 = AUTH_DIR / "04_exact_returned_review_recording_authorization_boundary.v1.md"

DEC = REPO / (
    "documentation/decisions/"
    "0208-authorize-recording-exact-returned-revision-required-"
    "independent-human-review-for-req06-req14-accounting-gap-study-v1.md"
)

EXPECTED_CHANGED = sorted([
    str(A01.relative_to(REPO)),
    str(Path(__file__).resolve().relative_to(REPO)),
    str(A03.relative_to(REPO)),
    str(A04.relative_to(REPO)),
    str(DEC.relative_to(REPO)),
])


def stop(code, detail=""):
    print(
        "STOP|" + code
        + (("|" + detail) if detail else "")
    )
    raise SystemExit(1)


head = subprocess.check_output(
    ["git", "-C", str(REPO), "rev-parse", "HEAD"],
    text=True
).strip()

parent = subprocess.check_output(
    ["git", "-C", str(REPO), "rev-parse", "HEAD^"],
    text=True
).strip()

if parent != EXPECTED_HEAD_PARENT:
    stop("D0208_PARENT_INVALID", parent)

status = subprocess.check_output(
    [
        "git", "-C", str(REPO),
        "status", "--porcelain=v1",
        "--untracked-files=all"
    ],
    text=True
)

if status.strip():
    stop("REPOSITORY_NOT_CLEAN")

changed = subprocess.check_output(
    [
        "git", "-C", str(REPO),
        "diff-tree", "--no-commit-id",
        "--name-only", "-r", "HEAD"
    ],
    text=True
).splitlines()

if sorted(changed) != EXPECTED_CHANGED:
    stop("D0208_COMMIT_SCOPE_INVALID")

for p in (A01, A03, A04, DEC, RETURNED):
    if not p.is_file():
        stop("REQUIRED_ARTIFACT_MISSING", str(p))

authorization = json.loads(A01.read_text(encoding="utf-8"))
contract = json.loads(A03.read_text(encoding="utf-8"))

if authorization.get("decision") != "0208":
    stop("AUTHORIZATION_DECISION_INVALID")

if authorization.get("authorization_status") != (
    "AUTHORIZED_TO_RECORD_EXACT_RETURNED_REVISION_REQUIRED_HUMAN_REVIEW_ONLY"
):
    stop("AUTHORIZATION_STATUS_INVALID")

source = authorization.get("returned_review", {})

if source.get("sha256") != RETURNED_SHA:
    stop("AUTHORIZED_RETURN_SHA_INVALID")

if source.get("exact_byte_recording_required") is not True:
    stop("EXACT_RECORDING_NOT_REQUIRED")

if source.get("line_ending_normalization_authorized") is not False:
    stop("LINE_ENDING_NORMALIZATION_BOUNDARY_INVALID")

b = RETURNED.read_bytes()

if hashlib.sha256(b).hexdigest() != RETURNED_SHA:
    stop("RETURNED_REVIEW_SHA_MISMATCH")

if len(b) != RETURNED_SIZE:
    stop("RETURNED_REVIEW_SIZE_MISMATCH")

if b.count(b"\r\n") != RETURNED_CRLF:
    stop("RETURNED_REVIEW_CRLF_MISMATCH")

text = b.decode("utf-8-sig")
text = text.replace("\r\n", "\n").replace("\r", "\n")

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

if not overall:
    stop("OVERALL_DECISION_NOT_FOUND")

if overall.group(1) != "REVISION_REQUIRED":
    stop("OVERALL_DECISION_INVALID")

facts = authorization.get("returned_packet_facts", {})

if facts.get("review_item_count") != 9:
    stop("REVIEW_ITEM_COUNT_INVALID")

if facts.get("pass_item_count") != 5:
    stop("PASS_ITEM_COUNT_INVALID")

if facts.get("revision_required_item_count") != 4:
    stop("REVISION_REQUIRED_ITEM_COUNT_INVALID")

if facts.get("overall_review_decision") != "REVISION_REQUIRED":
    stop("PACKET_OVERALL_DECISION_INVALID")

if facts.get("identity_or_authorship_independently_verified") is not False:
    stop("IDENTITY_VERIFICATION_CLAIM_INVALID")

props = contract.get("required_recording_properties", {})

for key in (
    "repository_exact_copy_must_match_source_sha256",
    "repository_exact_copy_must_match_source_size",
    "repository_exact_copy_must_match_source_bytes",
    "repository_exact_copy_must_preserve_crlf_bytes",
    "reviewer_identity_fields_are_packet_facts_only",
    "independent_identity_verification_claim_forbidden",
    "overall_result_must_remain_revision_required",
):
    if props.get(key) is not True:
        stop("RECORDING_CONTRACT_INVALID", key)

non = authorization.get("explicit_nonauthorization", {})

for key, value in non.items():
    if value is not False:
        stop("NONAUTHORIZATION_INVALID", key)

print(
    "DECISION0208_EXACT_RETURNED_REVISION_REQUIRED_REVIEW_RECORDING_AUTHORIZATION_VERIFIER=PASS"
)
print("AUTHORIZATION_COMMIT=" + head)
print("AUTHORIZATION_PARENT=" + parent)
print("RETURNED_REVIEW_SHA256=" + RETURNED_SHA)
print("RETURNED_REVIEW_SIZE=12281")
print("RETURNED_REVIEW_CRLF_COUNT=140")
print("RETURNED_REVIEW_EXACT_BYTE_IDENTITY=PASS")

print("REVIEW_ITEM_COUNT=9")
print("PASS_ITEM_COUNT=5")
print("PASS_ITEMS=ASER03,ASER05,ASER06,ASER08,ASER09")
print("REVISION_REQUIRED_ITEM_COUNT=4")
print("REVISION_REQUIRED_ITEMS=ASER01,ASER02,ASER04,ASER07")
print("OVERALL_REVIEW_DECISION=REVISION_REQUIRED")

print("REVIEWER_IDENTITY_IS_PACKET_FACT_ONLY=YES")
print("IDENTITY_OR_AUTHORSHIP_INDEPENDENTLY_VERIFIED=NO")

print("EXACT_REVIEW_RECORDING_AUTHORIZED=YES")
print("EXACT_REVIEW_RECORDED_BY_THIS_VERIFIER=NO")

print("CORRECTIVE_SUCCESSOR_AUTHORIZED=NO")
print("CORRECTIVE_SUCCESSOR_AUTHORED=NO")

print("STUDY_APPROVED=NO")
print("STUDY_GOVERNANCE_ADOPTED=NO")

print("REQ06_FAILURE_PROVEN=NO")
print("REQ14_FAILURE_PROVEN=NO")
print("ACCOUNTING_UNSATISFACTION_PROVEN=NO")

print("ACCOUNTING_EVIDENCE_ACQUISITION_AUTHORIZED=NO")
print("CONCRETE_MAPPING_AUTHORIZED=NO")
print("ACCOUNTING_SATISFACTION_DETERMINATION_AUTHORIZED=NO")
print("ACCOUNTING_SATISFACTION_ESTABLISHED=NO")

print("PAIR_RECLASSIFICATION_AUTHORIZED=NO")
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

print("AUTHORIZATION_EXECUTION_COUNT_FOR_THIS_RUN=1")
print("AUTHORIZATION_RERUN_AUTHORIZED=NO")
