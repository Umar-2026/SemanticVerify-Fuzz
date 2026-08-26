#!/usr/bin/env python3

from pathlib import Path
import datetime
import hashlib
import json
import os
import subprocess
import sys

EXPECTED_PARENT = "0eebed428ea37cd0a555a4f885dc4c8da3f3c37c"

RETURNED_PACKET = Path(
    "/openbayes/home/"
    "50_positive_binding_evidence_manually_packet."
    "MANUAL_REVIEW_COPY.v1.md"
)
EXPECTED_RETURNED_SHA = (
    "effd2848702219741e3814d2dc283284c92ab07f49980cd799fde351ecb8b685"
)
EXPECTED_RETURNED_SIZE = 20425

ZIP_PATH = Path(
    "/openbayes/home/"
    "50_positive_binding_evidence_acquisition_external_handoff.v1.zip"
)
EXPECTED_ZIP_SHA = (
    "e300b1cde69bf17cada5412ae5a169b1c0d201c71ae6879a778b9731ddfb5488"
)
EXPECTED_ZIP_SIZE = 96863

DECISION_PATH = Path(
    "documentation/decisions/"
    "0180-authorize-recording-completed-human-positive-binding-"
    "evidence-packet-v1.md"
)

AUTH_DIR = Path(
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2/"
    "schema_v2_requirement_to_semantic_unit_completed_human_"
    "positive_binding_evidence_recording_authorization_v1"
)

A01 = AUTH_DIR / "01_recording_authorization.v1.json"
A03 = AUTH_DIR / "03_one_time_verifier_lifecycle.v1.json"

SENTINEL = Path(
    "/openbayes/home/"
    ".semanticverify-fuzz-decision0180-a02-single-execution-reservation.v1.json"
)

OUTPUT = Path(
    "/openbayes/home/"
    "decision0180_a02_single_execution_output.v1.txt"
)


def stop(message: str, code: int = 181) -> None:
    print("DECISION0180_A02_RESULT=FAIL")
    print("FAILURE=" + message)
    raise SystemExit(code)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def git(*args: str) -> str:
    return subprocess.check_output(
        ["git", *args],
        text=True,
    ).strip()


if SENTINEL.exists():
    stop("ONE_TIME_VERIFIER_ALREADY_CONSUMED")

if OUTPUT.exists():
    stop("PRIOR_OUTPUT_ALREADY_EXISTS")

if git("status", "--porcelain=v1", "--untracked-files=all"):
    stop("REPOSITORY_NOT_CLEAN")

head = git("rev-parse", "HEAD")
parent = git("rev-parse", "HEAD^")

if parent != EXPECTED_PARENT:
    stop("DECISION0180_PARENT_MISMATCH")

if not DECISION_PATH.is_file():
    stop("DECISION0180_FILE_MISSING")

try:
    tracked = subprocess.check_output(
        ["git", "ls-files", "--error-unmatch", str(DECISION_PATH)],
        text=True,
        stderr=subprocess.DEVNULL,
    ).strip()
except subprocess.CalledProcessError:
    stop("DECISION0180_FILE_NOT_TRACKED")

if not tracked:
    stop("DECISION0180_FILE_NOT_TRACKED")

if not RETURNED_PACKET.is_file():
    stop("RETURNED_PACKET_MISSING")

if sha256(RETURNED_PACKET) != EXPECTED_RETURNED_SHA:
    stop("RETURNED_PACKET_HASH_MISMATCH")

if RETURNED_PACKET.stat().st_size != EXPECTED_RETURNED_SIZE:
    stop("RETURNED_PACKET_SIZE_MISMATCH")

if not ZIP_PATH.is_file():
    stop("EXTERNAL_ZIP_MISSING")

if sha256(ZIP_PATH) != EXPECTED_ZIP_SHA:
    stop("EXTERNAL_ZIP_HASH_MISMATCH")

if ZIP_PATH.stat().st_size != EXPECTED_ZIP_SIZE:
    stop("EXTERNAL_ZIP_SIZE_MISMATCH")

if not A01.is_file() or not A03.is_file():
    stop("AUTHORIZATION_ARTIFACT_MISSING")

a01 = json.loads(A01.read_text(encoding="utf-8"))
a03 = json.loads(A03.read_text(encoding="utf-8"))

if a01.get("decision") != "Decision0180":
    stop("A01_DECISION_BINDING_INVALID")

if a01.get("authorization_status") != \
        "AUTHORIZED_FOR_SEPARATE_NEXT_TRANSACTION":
    stop("A01_AUTHORIZATION_STATUS_INVALID")

if a01.get("authorization_scope") != \
        "RECORD_EXACT_RETURNED_PACKET_AS_IMMUTABLE_CANDIDATE_HUMAN_EVIDENCE_ONLY":
    stop("A01_SCOPE_INVALID")

summary = a01.get("validated_returned_evidence_summary", {})

expected_summary = {
    "requirement_section_count": 17,
    "semantic_unit_domain_count": 109,
    "positive_binding_proposed_requirement_count": 15,
    "unresolved_no_positive_binding_proposed_requirement_count": 2,
    "positive_requirement_unit_pair_proposal_count": 211,
    "unknown_semantic_unit_id_count": 0,
    "positive_proposal_without_rationale_count": 0,
    "invalid_evidence_state_count": 0,
    "unresolved_section_with_unit_proposal_count": 0,
    "static_prefix_preserved": True,
    "reviewer_completion_fields_present": True,
}

if summary != expected_summary:
    stop("A01_VALIDATED_SUMMARY_INVALID")

bounded = a01.get("bounded_interpretation", {})

if bounded.get("candidate_human_evidence_only") is not True:
    stop("CANDIDATE_EVIDENCE_BOUNDARY_INVALID")

if bounded.get(
    "positive_proposals_are_governed_pair_reclassifications"
) is not False:
    stop("PAIR_RECLASSIFICATION_BOUNDARY_INVALID")

if bounded.get(
    "unresolved_no_positive_binding_is_negative_proof"
) is not False:
    stop("NEGATIVE_PROOF_BOUNDARY_INVALID")

if a03.get("state") != "ACTIVE_UNCONSUMED":
    stop("A03_NOT_ACTIVE_UNCONSUMED")

if a03.get("execution_count") != 0:
    stop("A03_EXECUTION_COUNT_INVALID")

if a03.get("authorized_execution_transaction") != "Decision0181":
    stop("A03_EXECUTION_TRANSACTION_INVALID")

if a03.get("rerun_authorized") is not False:
    stop("A03_RERUN_BOUNDARY_INVALID")

reservation = {
    "artifact": "decision0180_a02_single_execution_reservation_v1",
    "decision": "Decision0180",
    "execution_transaction": "Decision0181",
    "authorized_head_at_execution": head,
    "returned_packet_sha256": EXPECTED_RETURNED_SHA,
    "state": "PERMANENTLY_RETIRED_AFTER_THIS_EXECUTION",
    "rerun_authorized": False,
    "reserved_at_utc": datetime.datetime.now(
        datetime.timezone.utc
    ).isoformat(),
}

flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL

try:
    fd = os.open(str(SENTINEL), flags, 0o444)
except FileExistsError:
    stop("ONE_TIME_RESERVATION_COLLISION")

with os.fdopen(fd, "w", encoding="utf-8") as f:
    json.dump(reservation, f, indent=2, sort_keys=True)
    f.write("\n")

lines = [
    "DECISION0180_A02_RESULT=PASS",
    "DECISION=Decision0180",
    "EXECUTION_TRANSACTION=Decision0181",
    f"AUTHORIZED_HEAD_AT_EXECUTION={head}",
    f"AUTHORIZED_PARENT={parent}",
    f"RETURNED_PACKET_SHA256={EXPECTED_RETURNED_SHA}",
    f"RETURNED_PACKET_SIZE={EXPECTED_RETURNED_SIZE}",
    "RETURNED_PACKET_IS_CANDIDATE_HUMAN_EVIDENCE_ONLY=YES",
    "PAIR_RECLASSIFICATION_PERFORMED=NO",
    "PAIR_RECLASSIFICATION_AUTHORIZED=NO",
    "OPERATIONAL_MAPPING_AUTHORIZED=NO",
    "SCHEMA_V2_MODIFICATION_AUTHORIZED=NO",
    "ANALYZER_IMPLEMENTATION_AUTHORIZED=NO",
    "ANALYZER_EXECUTION_AUTHORIZED=NO",
    "BASELINE_EXECUTION_AUTHORIZED=NO",
    "REPAIR_IMPLEMENTATION_AUTHORIZED=NO",
    "REPAIR_EXECUTION_AUTHORIZED=NO",
    "ONE_TIME_VERIFIER_STATE=PERMANENTLY_RETIRED",
    "RERUN_AUTHORIZED=NO",
]

OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
OUTPUT.chmod(0o444)

print("\n".join(lines))
