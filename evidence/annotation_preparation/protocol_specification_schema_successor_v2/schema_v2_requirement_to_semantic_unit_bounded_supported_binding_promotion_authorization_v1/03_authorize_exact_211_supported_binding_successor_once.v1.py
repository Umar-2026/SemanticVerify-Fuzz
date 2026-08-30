#!/usr/bin/env python3

from pathlib import Path
from collections import Counter
import hashlib
import json
import re
import subprocess

D0189_COMMIT = "f4c9c31ba5ae8ac8945d0f58d96025a19fdfd65b"

ROOT = Path(
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2"
)

MATRIX = (
    ROOT
    / "schema_v2_requirement_to_semantic_unit_crosswalk_evidence_resolution_study_v1"
    / "04_requirement_semantic_unit_pair_matrix.v1.json"
)

PACKET = (
    ROOT
    / "schema_v2_requirement_to_semantic_unit_bounded_technical_adjudication_completed_human_record_v1"
    / "01_returned_human_technical_adjudication.EXACT_COPY.v1.md"
)

AUTH = (
    ROOT
    / "schema_v2_requirement_to_semantic_unit_bounded_supported_binding_promotion_authorization_v1"
)

P01 = AUTH / "01_bounded_promotion_authorization_manifest.v1.json"
P02 = AUTH / "02_exact_211_promotion_field_contract.v1.json"
P03 = AUTH / "03_authorize_exact_211_supported_binding_successor_once.v1.py"
P04 = AUTH / "04_bounded_promotion_authorization_boundary.v1.md"

DEC = Path(
    "documentation/decisions/"
    "0190-authorize-exact-211-bounded-supported-binding-promotion-successor.md"
)

EXPECTED_D0190_PATHS = {
    str(P01),
    str(P02),
    str(P03),
    str(P04),
    str(DEC),
}

MATRIX_SHA = (
    "389615002582964b97aa6eb717ceb520067cef78b18cf482cf257fe9b36f2515"
)

PACKET_SHA = (
    "ad35ddfefea1d79db79e36f24ef823407f977a682efcdf23a98a1cbc5ffd7eda"
)


def stop(code, detail=""):
    print(
        "STOP|" + code
        + (("|" + detail) if detail else "")
    )
    raise SystemExit(1)


def git(*args):
    return subprocess.check_output(
        ["git", *args],
        text=True
    ).strip()


# When this one-time verifier is consumed, HEAD must be the committed
# Decision0190 checkpoint whose parent is Decision0189.
if git("rev-parse", "HEAD^") != D0189_COMMIT:
    stop("D0190_PARENT_NOT_D0189")

if subprocess.check_output(
    ["git", "status", "--porcelain=v1", "--untracked-files=all"],
    text=True
).strip():
    stop("REPOSITORY_NOT_CLEAN_BEFORE_D0190_SUCCESSOR")

changed = {
    x
    for x in subprocess.check_output(
        [
            "git",
            "diff-tree",
            "--no-commit-id",
            "--name-only",
            "-r",
            "HEAD",
        ],
        text=True,
    ).splitlines()
    if x.strip()
}

if changed != EXPECTED_D0190_PATHS:
    stop(
        "D0190_COMMIT_SCOPE_MISMATCH",
        ",".join(sorted(changed))
    )

for path in (MATRIX, PACKET, P01, P02, P03, P04, DEC):
    if not path.is_file():
        stop(
            "REQUIRED_ARTIFACT_MISSING",
            str(path)
        )

matrix_raw = MATRIX.read_bytes()
packet_raw = PACKET.read_bytes()

if hashlib.sha256(matrix_raw).hexdigest() != MATRIX_SHA:
    stop("BASE_MATRIX_SHA_MISMATCH")

if hashlib.sha256(packet_raw).hexdigest() != PACKET_SHA:
    stop("RECORDED_HUMAN_PACKET_SHA_MISMATCH")

matrix = json.loads(
    matrix_raw.decode("utf-8")
)

packet = (
    packet_raw.decode("utf-8")
    .replace("\r\n", "\n")
    .replace("\r", "\n")
)

manifest = json.loads(
    P01.read_text(encoding="utf-8")
)

contract = json.loads(
    P02.read_text(encoding="utf-8")
)

required_manifest = {
    "decision": "0190",
    "authorization_status":
        "AUTHORIZED_FOR_SINGLE_FUTURE_BOUNDED_PROMOTION_SUCCESSOR_TRANSACTION",
    "pair_universe_count": 1853,
    "promotion_candidate_count": 211,
    "noncandidate_count": 1642,
    "authorized_post_promotion_supported_binding_count": 211,
    "authorized_post_promotion_not_supported_binding_count": 0,
    "authorized_post_promotion_unresolved_binding_count": 1642,
    "promotion_from": "UNRESOLVED_BINDING",
    "promotion_to": "SUPPORTED_BINDING",
    "original_matrix_in_place_modification_authorized": False,
    "successor_classification_artifact_authorized": True,
    "noncandidate_pair_reclassification_authorized": False,
    "not_supported_binding_creation_authorized": False,
    "automatic_promotion_authorized": False,
    "operational_mapping_authorized": False,
    "schema_mapping_inference_authorized": False,
    "analyzer_execution_authorized": False,
    "baseline_execution_authorized": False,
    "repair_authorized": False,
    "promotion_performed_in_decision0190": False,
    "supported_binding_created_in_decision0190": False,
    "one_time_successor_authorization_verifier_rerun_authorized": False,
}

for key, expected in required_manifest.items():
    observed = manifest.get(key)

    if observed != expected:
        stop(
            "D0190_MANIFEST_CONTRACT_MISMATCH",
            f"{key}={observed!r}"
        )

transform = contract.get(
    "candidate_pair_transformation",
    {}
)

if transform.get("classification") != {
    "from": "UNRESOLVED_BINDING",
    "to": "SUPPORTED_BINDING",
}:
    stop("CLASSIFICATION_TRANSFORMATION_INVALID")

if transform.get("positive_binding_claimed") is not True:
    stop("POSITIVE_BINDING_CLAIM_NOT_ENABLED")

if transform.get("human_semantic_judgment_used") is not True:
    stop("HUMAN_SEMANTIC_JUDGMENT_FLAG_NOT_ENABLED")

for key in (
    "operational_mapping_authority",
    "schema_mapping_inferred",
    "negative_binding_exclusion_claimed",
    "carrier_admissibility_inferred",
    "field_class_relation_promoted",
    "historical_18639_pair_reclassified",
    "historical_carrier_pair_state_promoted",
    "lexical_similarity_promoted",
    "open_string_capacity_promoted",
):
    if transform.get(key) is not False:
        stop(
            "UNAUTHORIZED_PROMOTION_SIDE_EFFECT",
            key
        )

if not str(
    transform.get("classification_basis", "")
).strip():
    stop("CLASSIFICATION_BASIS_BLANK")

if not str(
    transform.get("evidence_gap", "")
).strip():
    stop("EVIDENCE_GAP_BLANK")

pairs = matrix.get("pairs")

if not isinstance(pairs, list) or len(pairs) != 1853:
    stop("BASE_PAIR_UNIVERSE_INVALID")

if Counter(
    rec.get("classification")
    for rec in pairs
) != Counter({"UNRESOLVED_BINDING": 1853}):
    stop("BASE_CLASSIFICATION_STATE_CHANGED")

pair_re = re.compile(
    r"(?m)^## Candidate Pair ([0-9]{3})[ \t]*$"
)

matches = list(pair_re.finditer(packet))

expected_ordinals = [
    f"{i:03d}"
    for i in range(1, 212)
]

if [m.group(1) for m in matches] != expected_ordinals:
    stop("RECORDED_PACKET_PAIR_SEQUENCE_INVALID")

candidates = []

for i, m in enumerate(matches):
    end = (
        matches[i + 1].start()
        if i + 1 < len(matches)
        else len(packet)
    )

    block = packet[m.start():end]
    ordinal = m.group(1)

    def one(pattern, label):
        x = re.search(
            pattern,
            block,
            re.MULTILINE
        )

        if not x:
            stop(
                "PACKET_FIELD_MISSING",
                ordinal + ":" + label
            )

        return x.group(1)

    req = one(
        r'^Requirement ID \(exact\):[ \t]*"([^"]+)"[ \t]*$',
        "requirement_id"
    )

    unit = one(
        r'^Semantic-unit ID \(exact\):[ \t]*"([^"]+)"[ \t]*$',
        "semantic_unit_id"
    )

    reviewer = one(
        r'^Recorded reviewer evidence state:[ \t]*`([^`]+)`[ \t]*$',
        "reviewer_state"
    )

    technical = one(
        r'^Technical adjudication state:[ \t]*\n'
        r'[ \t]*([A-Z0-9_-]+)[ \t]*$',
        "technical_state"
    )

    if reviewer != "POSITIVE_BINDING_PROPOSED":
        stop(
            "REVIEWER_EVIDENCE_NOT_POSITIVE",
            ordinal
        )

    if (
        technical
        != "TECHNICAL_SUPPORT_CONFIRMED_PROMOTION_CANDIDATE"
    ):
        stop(
            "TECHNICAL_PROMOTION_CANDIDATE_NOT_CONFIRMED",
            ordinal
        )

    candidates.append((req, unit))

if len(candidates) != 211 or len(set(candidates)) != 211:
    stop("EXACT_211_CANDIDATE_SET_INVALID")

matrix_index = {
    (
        rec.get("requirement_id"),
        rec.get("semantic_unit_id")
    ): rec
    for rec in pairs
}

if len(matrix_index) != 1853:
    stop("BASE_MATRIX_PAIR_IDENTITIES_NOT_UNIQUE")

for key in candidates:
    rec = matrix_index.get(key)

    if rec is None:
        stop(
            "CANDIDATE_MISSING_FROM_MATRIX",
            repr(key)
        )

    if rec.get("classification") != "UNRESOLVED_BINDING":
        stop(
            "CANDIDATE_PRESTATE_CHANGED",
            repr(key)
        )

candidate_set = set(candidates)

noncandidate = [
    rec
    for rec in pairs
    if (
        rec.get("requirement_id"),
        rec.get("semantic_unit_id")
    ) not in candidate_set
]

if len(noncandidate) != 1642:
    stop("NONCANDIDATE_COUNT_NOT_1642")

decision = DEC.read_text(encoding="utf-8")

for marker in (
    "PROMOTION_SUCCESSOR_AUTHORIZED=YES",
    "PROMOTION_PERFORMED=NO",
    "SUPPORTED_BINDING_CREATED=NO",
    "NOT_SUPPORTED_BINDING_CREATED=NO",
    "ORIGINAL_MATRIX_IN_PLACE_MODIFICATION_AUTHORIZED=NO",
    "NONCANDIDATE_PAIR_RECLASSIFICATION_AUTHORIZED=NO",
    "OPERATIONAL_MAPPING_AUTHORIZED=NO",
    "ANALYZER_AUTHORIZED=NO",
    "BASELINE_AUTHORIZED=NO",
    "REPAIR_AUTHORIZED=NO",
):
    if marker not in decision:
        stop(
            "DECISION0190_MARKER_MISSING",
            marker
        )

print("DECISION0190_BOUNDED_PROMOTION_AUTHORIZATION_VERIFIER=PASS")
print("BASE_PAIR_UNIVERSE_COUNT=1853")
print("EXACT_PROMOTION_PAIR_COUNT=211")
print("NONCANDIDATE_PAIR_COUNT=1642")
print("PROMOTION_FROM=UNRESOLVED_BINDING")
print("PROMOTION_TO=SUPPORTED_BINDING")
print("AUTHORIZED_POST_SUPPORTED_BINDING_COUNT=211")
print("AUTHORIZED_POST_UNRESOLVED_BINDING_COUNT=1642")
print("AUTHORIZED_POST_NOT_SUPPORTED_BINDING_COUNT=0")
print("POSITIVE_BINDING_CLAIMED_FOR_PROMOTED_PAIRS=YES")
print("HUMAN_SEMANTIC_JUDGMENT_USED_FOR_PROMOTED_PAIRS=YES")
print("OPERATIONAL_MAPPING_CREATED=NO")
print("SCHEMA_MAPPING_INFERRED=NO")
print("NONCANDIDATE_RECLASSIFICATION=NO")
print("NOT_SUPPORTED_BINDING_CREATION=NO")
print("PROMOTION_SUCCESSOR_AUTHORIZED=YES")
print("PROMOTION_PERFORMED_BY_THIS_VERIFIER=NO")
print("SUCCESSOR_AUTHORIZATION_EXECUTION_COUNT_FOR_THIS_RUN=1")
print("SUCCESSOR_AUTHORIZATION_RERUN_AUTHORIZED=NO")
