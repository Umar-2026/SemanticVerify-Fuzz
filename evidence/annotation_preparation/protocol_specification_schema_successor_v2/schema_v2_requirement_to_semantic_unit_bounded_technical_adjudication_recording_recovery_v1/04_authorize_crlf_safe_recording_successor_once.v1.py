#!/usr/bin/env python3

from pathlib import Path
import hashlib
import re
import subprocess

D0187_COMMIT = "fe82467ca6719d2fa09ebda62b6fc45b281a3575"

RETURNED = Path(
    "/openbayes/home/"
    "50_bounded_technical_adjudication_Nadeem_packet."
    "MANUAL_ADJUDICATION_COPY.v1.md"
)

EXPECTED_PACKET_SHA = (
    "ad35ddfefea1d79db79e36f24ef823407f977a682efcdf23a98a1cbc5ffd7eda"
)
EXPECTED_PACKET_SIZE = 316649

REF = Path(
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2/"
    "schema_v2_requirement_to_semantic_unit_"
    "bounded_technical_adjudication_external_handoff_v1/"
    "02_blank_technical_adjudication_packet.EXACT_COPY.v1.md"
)

RECOVERY_DIR = Path(
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2/"
    "schema_v2_requirement_to_semantic_unit_"
    "bounded_technical_adjudication_recording_recovery_v1"
)

EXPECTED_D0188_PATHS = {
    str(RECOVERY_DIR / "01_failed_decision0187_a02_execution_output.EXACT_COPY.v1.txt"),
    str(RECOVERY_DIR / "02_failed_decision0187_a02_consumption_sentinel.EXACT_COPY.v1.json"),
    str(RECOVERY_DIR / "03_failed_a02_root_cause_record.v1.json"),
    str(RECOVERY_DIR / "04_authorize_crlf_safe_recording_successor_once.v1.py"),
    str(RECOVERY_DIR / "05_recovery_and_successor_authorization_boundary.v1.md"),
    str(RECOVERY_DIR / "06_verify_recovery_record.v1.py"),
    str(RECOVERY_DIR / "07_recovery_record.v1.SHA256SUMS"),
    "documentation/decisions/"
    "0188-record-failed-d0187-a02-consumption-and-authorize-crlf-safe-successor.md",
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


# When executed in the next transaction, HEAD must be Decision0188,
# whose parent must be the immutable Decision0187 authorization commit.
if git("rev-parse", "HEAD^") != D0187_COMMIT:
    stop("D0188_PARENT_IS_NOT_D0187")

if subprocess.check_output(
    ["git", "status", "--porcelain=v1", "--untracked-files=all"],
    text=True
).strip():
    stop("REPOSITORY_NOT_CLEAN_BEFORE_SUCCESSOR_EXECUTION")

changed = {
    x for x in subprocess.check_output(
        ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD"],
        text=True
    ).splitlines()
    if x.strip()
}

if changed != EXPECTED_D0188_PATHS:
    stop(
        "D0188_COMMIT_SCOPE_MISMATCH",
        "observed=" + ",".join(sorted(changed))
    )

if not RETURNED.is_file():
    stop("RETURNED_PACKET_MISSING")

raw = RETURNED.read_bytes()

if hashlib.sha256(raw).hexdigest() != EXPECTED_PACKET_SHA:
    stop("RETURNED_PACKET_SHA_MISMATCH")

if len(raw) != EXPECTED_PACKET_SIZE:
    stop("RETURNED_PACKET_SIZE_MISMATCH")

# Preserve byte-level identity above, but normalize newline representation
# only for semantic/structural parsing.
text = (
    raw.decode("utf-8")
    .replace("\r\n", "\n")
    .replace("\r", "\n")
)

if not REF.is_file():
    stop("REFERENCE_PACKET_MISSING")

ref_text = (
    REF.read_bytes().decode("utf-8")
    .replace("\r\n", "\n")
    .replace("\r", "\n")
)

pair_re = re.compile(
    r"(?m)^## Candidate Pair ([0-9]{3})[ \t]*$"
)

pairs = pair_re.findall(text)
ref_pairs = pair_re.findall(ref_text)

expected = [f"{i:03d}" for i in range(1, 212)]

if pairs != expected:
    stop(
        "RETURNED_PAIR_SEQUENCE_INVALID",
        f"count={len(pairs)} unique={len(set(pairs))}"
    )

if ref_pairs != expected:
    stop(
        "REFERENCE_PAIR_SEQUENCE_INVALID",
        f"count={len(ref_pairs)} unique={len(set(ref_pairs))}"
    )


def identities(src):
    matches = list(pair_re.finditer(src))
    result = []

    for i, m in enumerate(matches):
        end = (
            matches[i + 1].start()
            if i + 1 < len(matches)
            else len(src)
        )

        block = src[m.start():end]

        def one(pattern, label):
            mm = re.search(
                pattern,
                block,
                flags=re.MULTILINE
            )
            if not mm:
                stop(
                    "PAIR_IDENTITY_FIELD_MISSING",
                    f"{m.group(1)}:{label}"
                )
            return mm.group(1).strip()

        result.append((
            m.group(1),
            one(
                r'^Source requirement section:[ \t]*`([^`]+)`[ \t]*$',
                "source_requirement_section"
            ),
            one(
                r'^Requirement ID \(exact\):[ \t]*"([^"]+)"[ \t]*$',
                "requirement_id"
            ),
            one(
                r'^Semantic-unit ID \(exact\):[ \t]*"([^"]+)"[ \t]*$',
                "semantic_unit_id"
            ),
        ))

    return result


if identities(text) != identities(ref_text):
    stop("PAIR_IDENTITY_PRESERVATION_FAILED")

matches = list(pair_re.finditer(text))
counts = {state: 0 for state in ALLOWED_STATES}

for i, m in enumerate(matches):
    end = (
        matches[i + 1].start()
        if i + 1 < len(matches)
        else len(text)
    )

    block = text[m.start():end]
    ordinal = m.group(1)

    pre = re.search(
        r"(?m)^Governed pair prestate:[ \t]*`([^`]+)`[ \t]*$",
        block
    )

    if not pre or pre.group(1) != "UNRESOLVED_BINDING":
        stop("PAIR_PRESTATE_INVALID", ordinal)

    reviewer_state = re.search(
        r"(?m)^Recorded reviewer evidence state:[ \t]*`([^`]+)`[ \t]*$",
        block
    )

    if (
        not reviewer_state
        or reviewer_state.group(1) != "POSITIVE_BINDING_PROPOSED"
    ):
        stop("RECORDED_REVIEWER_EVIDENCE_STATE_INVALID", ordinal)

    state_m = re.search(
        r"(?m)^Technical adjudication state:[ \t]*\n"
        r"[ \t]*([A-Z0-9_-]+)[ \t]*$",
        block
    )

    if not state_m:
        stop("TECHNICAL_STATE_MISSING", ordinal)

    state = state_m.group(1)

    if state not in ALLOWED_STATES:
        stop("TECHNICAL_STATE_INVALID", f"{ordinal}:{state}")

    counts[state] += 1

    rationale = re.search(
        r"(?ms)^Technical adjudication rationale:[ \t]*\n"
        r"(.*?)(?=^Technical adjudicator notes:)",
        block
    )

    if not rationale or not rationale.group(1).strip():
        stop("RATIONALE_BLANK", ordinal)

    notes = re.search(
        r"(?ms)^Technical adjudicator notes:[ \t]*\n"
        r"(.*?)(?=^---[ \t]*$|\Z)",
        block
    )

    if not notes or not notes.group(1).strip():
        stop("NOTES_BLANK", ordinal)

if counts["TECHNICAL_SUPPORT_CONFIRMED_PROMOTION_CANDIDATE"] != 211:
    stop("CONFIRMED_PROMOTION_CANDIDATE_COUNT_NOT_211")

if counts["TECHNICAL_SUPPORT_NOT_ESTABLISHED"] != 0:
    stop("NOT_ESTABLISHED_COUNT_NOT_ZERO")

if counts["TECHNICAL_ADJUDICATION_UNRESOLVED"] != 0:
    stop("ADJUDICATION_UNRESOLVED_COUNT_NOT_ZERO")

completion_count = len(re.findall(
    r"(?m)^# Human technical-adjudicator completion[ \t]*$",
    text
))

if completion_count != 1:
    stop(
        "HUMAN_COMPLETION_BLOCK_COUNT_INVALID",
        str(completion_count)
    )


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
    stop("HUMAN_ROLE_INVALID", role)

if (
    "independently reviewed all 211 candidate "
    "requirement-to-semantic-unit pairs"
    not in attestation
):
    stop("ATTESTATION_211_INDEPENDENT_REVIEW_MISSING")

print("D0188_CRLF_SAFE_SUCCESSOR_VERIFIER=PASS")
print("RETURNED_PACKET_SHA256=" + EXPECTED_PACKET_SHA)
print("RETURNED_PACKET_SIZE=316649")
print("NEWLINE_NORMALIZATION_FOR_PARSING_ONLY=YES")
print("BYTE_IDENTITY_PRESERVED=YES")
print("PAIR_COUNT=211")
print("PAIR_SEQUENCE=001_TO_211")
print("PAIR_IDENTITY_PRESERVATION=PASS")
print("CONFIRMED_PROMOTION_CANDIDATES=211")
print("NOT_ESTABLISHED=0")
print("ADJUDICATION_UNRESOLVED=0")
print("HUMAN_COMPLETION_BLOCK_COUNT=1")
print("HUMAN_ROLE=Spec-Technical-Adjudicator-1")
print("RECORDING_SUCCESSOR_AUTHORIZED=YES")
print("PAIR_RECLASSIFICATION_AUTHORIZED=NO")
print("SUPPORTED_BINDING_CREATION_AUTHORIZED=NO")
print("NOT_SUPPORTED_BINDING_CREATION_AUTHORIZED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
print("SUCCESSOR_EXECUTION_COUNT_FOR_THIS_RUN=1")
print("SUCCESSOR_RERUN_AUTHORIZED=NO")
