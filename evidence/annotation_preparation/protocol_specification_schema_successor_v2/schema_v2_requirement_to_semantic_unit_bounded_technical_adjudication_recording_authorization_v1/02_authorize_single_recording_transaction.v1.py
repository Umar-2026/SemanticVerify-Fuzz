#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys

EXPECTED_PARENT = "fdc69cfded4fa8363846c48569418ea8a7c25978"

RETURNED = Path(
    "/openbayes/home/"
    "50_bounded_technical_adjudication_Nadeem_packet."
    "MANUAL_ADJUDICATION_COPY.v1.md"
)

EXPECTED_SHA = (
    "ad35ddfefea1d79db79e36f24ef823407f977a682efcdf23a98a1cbc5ffd7eda"
)
EXPECTED_SIZE = 316649

AUTH_DIR = Path(
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2/"
    "schema_v2_requirement_to_semantic_unit_"
    "bounded_technical_adjudication_recording_authorization_v1"
)

A01 = AUTH_DIR / "01_recording_authorization_manifest.v1.json"
A02 = AUTH_DIR / "02_authorize_single_recording_transaction.v1.py"
A03 = AUTH_DIR / "03_recording_authorization_boundary.v1.md"

DECISION = Path(
    "documentation/decisions/"
    "0187-authorize-recording-returned-human-technical-adjudication-evidence.md"
)

EXPECTED_CHANGED_PATHS = {
    str(A01),
    str(A02),
    str(A03),
    str(DECISION),
}

ALLOWED_STATES = {
    "TECHNICAL_SUPPORT_CONFIRMED_PROMOTION_CANDIDATE",
    "TECHNICAL_SUPPORT_NOT_ESTABLISHED",
    "TECHNICAL_ADJUDICATION_UNRESOLVED",
}


def stop(code, detail=""):
    if detail:
        print(f"STOP|{code}|{detail}")
    else:
        print(f"STOP|{code}")
    raise SystemExit(1)


def git(*args):
    return subprocess.check_output(
        ["git", *args],
        text=True
    ).strip()


if git("rev-parse", "HEAD^") != EXPECTED_PARENT:
    stop("DECISION0187_PARENT_MISMATCH")

if subprocess.check_output(
    ["git", "status", "--porcelain=v1", "--untracked-files=all"],
    text=True
).strip():
    stop("REPOSITORY_NOT_CLEAN_BEFORE_A02")

changed = set(
    x for x in subprocess.check_output(
        ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD"],
        text=True
    ).splitlines()
    if x.strip()
)

if changed != EXPECTED_CHANGED_PATHS:
    stop(
        "DECISION0187_COMMIT_SCOPE_MISMATCH",
        "observed=" + ",".join(sorted(changed))
    )

for p in (A01, A02, A03, DECISION):
    if not p.is_file():
        stop("AUTHORIZATION_ARTIFACT_MISSING", str(p))

manifest = json.loads(A01.read_text(encoding="utf-8"))

required_manifest_values = {
    "decision": "0187",
    "authorization_status":
        "AUTHORIZED_FOR_SINGLE_FUTURE_RECORDING_TRANSACTION",
    "authorized_operation":
        "RECORD_BYTE_EXACT_RETURNED_HUMAN_TECHNICAL_ADJUDICATION_EVIDENCE_ONLY",
    "source_sha256": EXPECTED_SHA,
    "source_size_bytes": EXPECTED_SIZE,
    "candidate_pair_count": 211,
    "technical_support_confirmed_promotion_candidate_count": 211,
    "technical_support_not_established_count": 0,
    "technical_adjudication_unresolved_count": 0,
    "required_human_role": "Spec-Technical-Adjudicator-1",
    "recording_completed": False,
    "pair_reclassification_authorized": False,
    "automatic_promotion_authorized": False,
    "supported_binding_creation_authorized": False,
    "not_supported_binding_creation_authorized": False,
    "analyzer_implementation_authorized": False,
    "analyzer_execution_authorized": False,
    "baseline_execution_authorized": False,
    "repair_authorized": False,
    "one_time_authorization_verifier_rerun_authorized": False,
}

for key, expected in required_manifest_values.items():
    if manifest.get(key) != expected:
        stop(
            "AUTHORIZATION_MANIFEST_VALUE_MISMATCH",
            f"{key}={manifest.get(key)!r}"
        )

if not RETURNED.is_file():
    stop("RETURNED_PACKET_MISSING")

raw = RETURNED.read_bytes()

if hashlib.sha256(raw).hexdigest() != EXPECTED_SHA:
    stop("RETURNED_PACKET_SHA_MISMATCH")

if len(raw) != EXPECTED_SIZE:
    stop("RETURNED_PACKET_SIZE_MISMATCH")

text = raw.decode("utf-8")

pairs = re.findall(
    r"(?m)^## Candidate Pair ([0-9]{3})[ \t]*$",
    text
)

expected_pairs = [f"{i:03d}" for i in range(1, 212)]

if pairs != expected_pairs:
    stop(
        "PAIR_SEQUENCE_INVALID",
        f"count={len(pairs)} unique={len(set(pairs))}"
    )

pair_matches = list(re.finditer(
    r"(?m)^## Candidate Pair ([0-9]{3})[ \t]*$",
    text
))

counts = {state: 0 for state in ALLOWED_STATES}

for i, match in enumerate(pair_matches):
    end = (
        pair_matches[i + 1].start()
        if i + 1 < len(pair_matches)
        else len(text)
    )
    block = text[match.start():end]
    ordinal = match.group(1)

    prestate = re.search(
        r"(?m)^Governed pair prestate:[ \t]*`([^`]+)`[ \t]*$",
        block
    )

    if not prestate or prestate.group(1) != "UNRESOLVED_BINDING":
        stop("PAIR_PRESTATE_INVALID", ordinal)

    state_match = re.search(
        r"(?m)^Technical adjudication state:[ \t]*\n"
        r"[ \t]*([A-Z0-9_-]+)[ \t]*$",
        block
    )

    if not state_match:
        stop("PAIR_STATE_MISSING", ordinal)

    state = state_match.group(1)

    if state not in ALLOWED_STATES:
        stop("PAIR_STATE_INVALID", f"{ordinal}:{state}")

    counts[state] += 1

    rationale = re.search(
        r"(?ms)^Technical adjudication rationale:[ \t]*\n"
        r"(.*?)(?=^Technical adjudicator notes:)",
        block
    )

    if not rationale or not rationale.group(1).strip():
        stop("PAIR_RATIONALE_BLANK", ordinal)

    notes = re.search(
        r"(?ms)^Technical adjudicator notes:[ \t]*\n"
        r"(.*?)(?=^---[ \t]*$|\Z)",
        block
    )

    if not notes or not notes.group(1).strip():
        stop("PAIR_NOTES_BLANK", ordinal)

if counts["TECHNICAL_SUPPORT_CONFIRMED_PROMOTION_CANDIDATE"] != 211:
    stop("CONFIRMED_PROMOTION_CANDIDATE_COUNT_NOT_211")

if counts["TECHNICAL_SUPPORT_NOT_ESTABLISHED"] != 0:
    stop("UNEXPECTED_NOT_ESTABLISHED_COUNT")

if counts["TECHNICAL_ADJUDICATION_UNRESOLVED"] != 0:
    stop("UNEXPECTED_ADJUDICATION_UNRESOLVED_COUNT")

completion_count = len(re.findall(
    r"(?m)^# Human technical-adjudicator completion[ \t]*$",
    text
))

if completion_count != 1:
    stop("HUMAN_COMPLETION_BLOCK_COUNT_INVALID", str(completion_count))


def human(prefix):
    m = re.search(
        rf"(?m)^{re.escape(prefix)}[ \t]*(.+?)[ \t]*$",
        text
    )
    if not m or not m.group(1).strip():
        stop("HUMAN_FIELD_BLANK", prefix)
    return m.group(1).strip()


human("Human technical adjudicator name:")

role = human("Human technical adjudicator role:")

human("Human technical adjudicator confirmation/signature:")
human("Human technical adjudicator date:")

attestation = human(
    "Human technical adjudicator attestation:"
)

if role != "Spec-Technical-Adjudicator-1":
    stop("HUMAN_ROLE_MISMATCH", role)

if (
    "independently reviewed all 211 candidate "
    "requirement-to-semantic-unit pairs"
    not in attestation
):
    stop("ATTESTATION_211_INDEPENDENT_REVIEW_MISSING")

decision_text = DECISION.read_text(encoding="utf-8")

required_decision_markers = (
    EXPECTED_SHA,
    "RECORDING_AUTHORIZED=YES",
    "RECORDING_COMPLETED=NO",
    "PAIR_RECLASSIFICATION_AUTHORIZED=NO",
    "AUTOMATIC_PROMOTION_AUTHORIZED=NO",
    "SUPPORTED_BINDING_CREATION_AUTHORIZED=NO",
    "ANALYZER_AUTHORIZED=NO",
    "BASELINE_AUTHORIZED=NO",
    "REPAIR_AUTHORIZED=NO",
)

for marker in required_decision_markers:
    if marker not in decision_text:
        stop("DECISION0187_MARKER_MISSING", marker)

print("DECISION0187_AUTHORIZATION_VERIFIER=PASS")
print("RETURNED_PACKET_SHA256=" + EXPECTED_SHA)
print("RETURNED_PACKET_SIZE=316649")
print("PAIR_COUNT=211")
print("CONFIRMED_PROMOTION_CANDIDATES=211")
print("NOT_ESTABLISHED=0")
print("ADJUDICATION_UNRESOLVED=0")
print("HUMAN_ROLE=Spec-Technical-Adjudicator-1")
print("RECORDING_AUTHORIZED=YES")
print("RECORDING_COMPLETED=NO")
print("PAIR_RECLASSIFICATION_AUTHORIZED=NO")
print("AUTOMATIC_PROMOTION_AUTHORIZED=NO")
print("SUPPORTED_BINDING_CREATION_AUTHORIZED=NO")
print("NOT_SUPPORTED_BINDING_CREATION_AUTHORIZED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
print("A02_EXECUTION_COUNT_FOR_THIS_RUN=1")
print("A02_RERUN_AUTHORIZED=NO")
