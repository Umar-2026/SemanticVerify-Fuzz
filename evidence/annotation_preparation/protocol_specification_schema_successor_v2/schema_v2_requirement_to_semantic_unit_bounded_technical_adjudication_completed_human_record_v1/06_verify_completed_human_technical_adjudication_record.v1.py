#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent

R01 = HERE / "01_returned_human_technical_adjudication.EXACT_COPY.v1.md"
R02 = HERE / "02_returned_packet_source_binding.v1.json"
R03 = HERE / "03_d0188_crlf_safe_successor_consumption_record.v1.json"
R04 = HERE / "04_d0188_crlf_safe_successor_execution_output.EXACT_COPY.v1.txt"
R05 = HERE / "05_d0188_crlf_safe_successor_consumption_sentinel.EXACT_COPY.v1.json"

REF = (
    HERE.parent
    / "schema_v2_requirement_to_semantic_unit_bounded_technical_adjudication_external_handoff_v1"
    / "02_blank_technical_adjudication_packet.EXACT_COPY.v1.md"
)

EXPECTED_PACKET_SHA = (
    "ad35ddfefea1d79db79e36f24ef823407f977a682efcdf23a98a1cbc5ffd7eda"
)

EXPECTED_SUCCESSOR_SHA = (
    "6d2048b557ddb55e47a6016cbb99b24a0c54524cc65fb693c4540a01615eaa26"
)

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


for p in (R01, R02, R03, R04, R05, REF):
    if not p.is_file():
        stop("REQUIRED_RECORD_FILE_MISSING", str(p))

raw = R01.read_bytes()

if hashlib.sha256(raw).hexdigest() != EXPECTED_PACKET_SHA:
    stop("RECORDED_PACKET_SHA_MISMATCH")

if len(raw) != 316649:
    stop("RECORDED_PACKET_SIZE_MISMATCH")

if raw.count(b"\r\n") != 4034:
    stop("RECORDED_PACKET_CRLF_COUNT_MISMATCH")

text = (
    raw.decode("utf-8")
    .replace("\r\n", "\n")
    .replace("\r", "\n")
)

ref_text = (
    REF.read_bytes().decode("utf-8")
    .replace("\r\n", "\n")
    .replace("\r", "\n")
)

pair_re = re.compile(
    r"(?m)^## Candidate Pair ([0-9]{3})[ \t]*$"
)

expected_pairs = [f"{i:03d}" for i in range(1, 212)]

pairs = pair_re.findall(text)
ref_pairs = pair_re.findall(ref_text)

if pairs != expected_pairs:
    stop(
        "PAIR_SEQUENCE_INVALID",
        f"count={len(pairs)} unique={len(set(pairs))}"
    )

if ref_pairs != expected_pairs:
    stop("REFERENCE_PAIR_SEQUENCE_INVALID")


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

for i, match in enumerate(matches):
    end = (
        matches[i + 1].start()
        if i + 1 < len(matches)
        else len(text)
    )

    block = text[match.start():end]
    ordinal = match.group(1)

    prestate = re.search(
        r"(?m)^Governed pair prestate:[ \t]*`([^`]+)`[ \t]*$",
        block
    )

    if (
        not prestate
        or prestate.group(1) != "UNRESOLVED_BINDING"
    ):
        stop("PAIR_PRESTATE_INVALID", ordinal)

    reviewer_state = re.search(
        r"(?m)^Recorded reviewer evidence state:[ \t]*`([^`]+)`[ \t]*$",
        block
    )

    if (
        not reviewer_state
        or reviewer_state.group(1) != "POSITIVE_BINDING_PROPOSED"
    ):
        stop("RECORDED_REVIEWER_STATE_INVALID", ordinal)

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
    stop("HUMAN_ATTESTATION_211_REVIEW_MISSING")

binding = json.loads(
    R02.read_text(encoding="utf-8")
)

consumption = json.loads(
    R03.read_text(encoding="utf-8")
)

sentinel = json.loads(
    R05.read_text(encoding="utf-8")
)

if binding["source_sha256"] != EXPECTED_PACKET_SHA:
    stop("SOURCE_BINDING_SHA_MISMATCH")

if binding["recorded_exact_copy_sha256"] != EXPECTED_PACKET_SHA:
    stop("RECORDED_COPY_BINDING_SHA_MISMATCH")

if binding["candidate_pair_count"] != 211:
    stop("SOURCE_BINDING_PAIR_COUNT_INVALID")

if (
    binding["technical_support_confirmed_promotion_candidate_count"]
    != 211
):
    stop("SOURCE_BINDING_CONFIRMED_COUNT_INVALID")

if binding["newline_normalization_used_for_parsing_only"] is not True:
    stop("NEWLINE_NORMALIZATION_BOUNDARY_INVALID")

if binding["raw_byte_identity_preserved"] is not True:
    stop("RAW_BYTE_IDENTITY_FLAG_INVALID")

for key in (
    "pair_reclassification_performed",
    "automatic_promotion_performed",
    "supported_binding_created",
    "not_supported_binding_created",
    "analyzer_implementation_authorized",
    "analyzer_execution_authorized",
    "baseline_execution_authorized",
    "repair_authorized",
):
    if binding[key] is not False:
        stop("UNEXPECTED_TRUE_BOUNDARY", key)

if consumption["execution_count"] != 1:
    stop("SUCCESSOR_EXECUTION_COUNT_INVALID")

if consumption["execution_result"] != "PASS":
    stop("SUCCESSOR_RESULT_NOT_PASS")

if consumption["lifecycle_state"] != "PERMANENTLY_RETIRED":
    stop("SUCCESSOR_NOT_PERMANENTLY_RETIRED")

if consumption["rerun_authorized"] is not False:
    stop("SUCCESSOR_RERUN_BOUNDARY_INVALID")

if consumption["successor_sha256"] != EXPECTED_SUCCESSOR_SHA:
    stop("SUCCESSOR_SHA_BINDING_INVALID")

if consumption["decision0187_a02_rerun"] is not False:
    stop("D0187_A02_RERUN_FLAG_INVALID")

output_raw = R04.read_bytes()

if (
    hashlib.sha256(output_raw).hexdigest()
    != consumption["output_sha256"]
):
    stop("SUCCESSOR_OUTPUT_SHA_BINDING_INVALID")

output_text = output_raw.decode("utf-8")

for marker in (
    "D0188_CRLF_SAFE_SUCCESSOR_VERIFIER=PASS",
    "PAIR_COUNT=211",
    "PAIR_SEQUENCE=001_TO_211",
    "PAIR_IDENTITY_PRESERVATION=PASS",
    "CONFIRMED_PROMOTION_CANDIDATES=211",
    "RECORDING_SUCCESSOR_AUTHORIZED=YES",
    "PAIR_RECLASSIFICATION_AUTHORIZED=NO",
    "SUPPORTED_BINDING_CREATION_AUTHORIZED=NO",
    "SUCCESSOR_EXECUTION_COUNT_FOR_THIS_RUN=1",
    "SUCCESSOR_RERUN_AUTHORIZED=NO",
):
    if marker not in output_text:
        stop("SUCCESSOR_OUTPUT_MARKER_MISSING", marker)

sentinel_raw = R05.read_bytes()

if (
    hashlib.sha256(sentinel_raw).hexdigest()
    != consumption["sentinel_sha256"]
):
    stop("SUCCESSOR_SENTINEL_SHA_BINDING_INVALID")

if sentinel["successor_sha256"] != EXPECTED_SUCCESSOR_SHA:
    stop("SUCCESSOR_SENTINEL_SHA_INVALID")

if sentinel["execution_count_authorized"] != 1:
    stop("SUCCESSOR_SENTINEL_EXECUTION_COUNT_INVALID")

if sentinel["rerun_authorized"] is not False:
    stop("SUCCESSOR_SENTINEL_RERUN_BOUNDARY_INVALID")

if sentinel["retired_d0187_a02_rerun_authorized"] is not False:
    stop("D0187_A02_SENTINEL_BOUNDARY_INVALID")

print("COMPLETED_HUMAN_TECHNICAL_ADJUDICATION_RECORD_VERIFIER=PASS")
print("RECORDED_PACKET_SHA256=" + EXPECTED_PACKET_SHA)
print("RECORDED_PACKET_SIZE=316649")
print("RECORDED_PACKET_CRLF_COUNT=4034")
print("BYTE_IDENTITY_PRESERVED=YES")
print("NEWLINE_NORMALIZATION_FOR_PARSING_ONLY=YES")
print("PAIR_COUNT=211")
print("PAIR_SEQUENCE=001_TO_211")
print("PAIR_IDENTITY_PRESERVATION=PASS")
print("CONFIRMED_PROMOTION_CANDIDATES=211")
print("NOT_ESTABLISHED=0")
print("ADJUDICATION_UNRESOLVED=0")
print("HUMAN_COMPLETION_BLOCK_COUNT=1")
print("HUMAN_ROLE=Spec-Technical-Adjudicator-1")
print("D0188_SUCCESSOR_EXECUTION_COUNT=1")
print("D0188_SUCCESSOR_RESULT=PASS")
print("D0188_SUCCESSOR_STATE=PERMANENTLY_RETIRED")
print("D0188_SUCCESSOR_RERUN_AUTHORIZED=NO")
print("DECISION0187_A02_RERUN=NO")
print("PAIR_RECLASSIFICATION_PERFORMED=NO")
print("AUTOMATIC_PROMOTION_PERFORMED=NO")
print("SUPPORTED_BINDING_CREATED=NO")
print("NOT_SUPPORTED_BINDING_CREATED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
