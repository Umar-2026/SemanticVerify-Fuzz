#!/usr/bin/env python3

from pathlib import Path
from collections import Counter
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

BASE = (
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

CONTRACT = AUTH / "02_exact_211_promotion_field_contract.v1.json"
P03 = AUTH / "03_authorize_exact_211_supported_binding_successor_once.v1.py"

S01 = HERE / "01_bounded_supported_binding_successor_matrix.v1.json"
S02 = HERE / "02_promotion_execution_manifest.v1.json"
S03 = HERE / "03_decision0190_p03_consumption_record.v1.json"
S04 = HERE / "04_decision0190_p03_execution_output.EXACT_COPY.v1.txt"
S05 = HERE / "05_decision0190_p03_consumption_sentinel.EXACT_COPY.v1.json"

EXPECTED_BASE_SHA = (
    "389615002582964b97aa6eb717ceb520067cef78b18cf482cf257fe9b36f2515"
)
EXPECTED_PACKET_SHA = (
    "ad35ddfefea1d79db79e36f24ef823407f977a682efcdf23a98a1cbc5ffd7eda"
)
EXPECTED_CONTRACT_SHA = (
    "4b64bbcc990654d0b86981b684e4f295c988993e0c397ec6f20ac98b9a51ea81"
)
EXPECTED_P03_SHA = (
    "08796576e58def2345db40129e0b9e4e1a95006d7ebaff3c2de9d16712aa2c60"
)


def stop(code, detail=""):
    print("STOP|" + code + (("|" + detail) if detail else ""))
    raise SystemExit(1)


for path in (BASE, PACKET, CONTRACT, P03, S01, S02, S03, S04, S05):
    if not path.is_file():
        stop("REQUIRED_ARTIFACT_MISSING", str(path))

if hashlib.sha256(BASE.read_bytes()).hexdigest() != EXPECTED_BASE_SHA:
    stop("BASE_MATRIX_SHA_MISMATCH")

if hashlib.sha256(PACKET.read_bytes()).hexdigest() != EXPECTED_PACKET_SHA:
    stop("HUMAN_PACKET_SHA_MISMATCH")

if hashlib.sha256(CONTRACT.read_bytes()).hexdigest() != EXPECTED_CONTRACT_SHA:
    stop("PROMOTION_CONTRACT_SHA_MISMATCH")

if hashlib.sha256(P03.read_bytes()).hexdigest() != EXPECTED_P03_SHA:
    stop("P03_SHA_MISMATCH")

base = json.loads(BASE.read_text(encoding="utf-8"))
successor = json.loads(S01.read_text(encoding="utf-8"))
contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
execution = json.loads(S02.read_text(encoding="utf-8"))
consumption = json.loads(S03.read_text(encoding="utf-8"))
sentinel = json.loads(S05.read_text(encoding="utf-8"))

packet = (
    PACKET.read_bytes()
    .decode("utf-8")
    .replace("\r\n", "\n")
    .replace("\r", "\n")
)

if hashlib.sha256(S01.read_bytes()).hexdigest() != execution["successor_matrix_sha256"]:
    stop("SUCCESSOR_MATRIX_SHA_BINDING_INVALID")

if S01.stat().st_size != execution["successor_matrix_size_bytes"]:
    stop("SUCCESSOR_MATRIX_SIZE_BINDING_INVALID")

if consumption.get("execution_count") != 1:
    stop("P03_EXECUTION_COUNT_INVALID")

if consumption.get("execution_result") != "PASS":
    stop("P03_RESULT_NOT_PASS")

if consumption.get("lifecycle_state") != "PERMANENTLY_RETIRED":
    stop("P03_NOT_PERMANENTLY_RETIRED")

if consumption.get("rerun_authorized") is not False:
    stop("P03_RERUN_BOUNDARY_INVALID")

if consumption.get("verifier_sha256") != EXPECTED_P03_SHA:
    stop("P03_CONSUMPTION_SHA_BINDING_INVALID")

if consumption.get("decision0187_a02_rerun") is not False:
    stop("DECISION0187_A02_RERUN_FLAG_INVALID")

if consumption.get("decision0188_crlf_safe_successor_rerun") is not False:
    stop("D0188_SUCCESSOR_RERUN_FLAG_INVALID")

output_raw = S04.read_bytes()

if hashlib.sha256(output_raw).hexdigest() != consumption[
    "execution_output_sha256"
]:
    stop("P03_OUTPUT_SHA_BINDING_INVALID")

output_text = output_raw.decode("utf-8")

for marker in (
    "DECISION0190_BOUNDED_PROMOTION_AUTHORIZATION_VERIFIER=PASS",
    "EXACT_PROMOTION_PAIR_COUNT=211",
    "NONCANDIDATE_PAIR_COUNT=1642",
    "PROMOTION_TO=SUPPORTED_BINDING",
    "AUTHORIZED_POST_SUPPORTED_BINDING_COUNT=211",
    "AUTHORIZED_POST_UNRESOLVED_BINDING_COUNT=1642",
    "AUTHORIZED_POST_NOT_SUPPORTED_BINDING_COUNT=0",
    "PROMOTION_SUCCESSOR_AUTHORIZED=YES",
    "SUCCESSOR_AUTHORIZATION_EXECUTION_COUNT_FOR_THIS_RUN=1",
    "SUCCESSOR_AUTHORIZATION_RERUN_AUTHORIZED=NO",
):
    if marker not in output_text:
        stop("P03_OUTPUT_MARKER_MISSING", marker)

sentinel_raw = S05.read_bytes()

if hashlib.sha256(sentinel_raw).hexdigest() != consumption[
    "consumption_sentinel_sha256"
]:
    stop("P03_SENTINEL_SHA_BINDING_INVALID")

if sentinel.get("verifier_sha256") != EXPECTED_P03_SHA:
    stop("P03_SENTINEL_VERIFIER_SHA_INVALID")

if sentinel.get("authorized_execution_count") != 1:
    stop("P03_SENTINEL_EXECUTION_COUNT_INVALID")

if sentinel.get("rerun_authorized") is not False:
    stop("P03_SENTINEL_RERUN_BOUNDARY_INVALID")

if successor.get("artifact") != (
    "requirement_to_semantic_unit_crosswalk_"
    "bounded_supported_binding_successor_v1"
):
    stop("SUCCESSOR_ARTIFACT_ID_INVALID")

if successor.get("status") != "GOVERNED_BOUNDED_SUCCESSOR":
    stop("SUCCESSOR_STATUS_INVALID")

if successor.get("allowed_pair_classifications") != base.get(
    "allowed_pair_classifications"
):
    stop("ALLOWED_CLASSIFICATIONS_CHANGED")

if successor.get("pair_domain") != base.get("pair_domain"):
    stop("PAIR_DOMAIN_CHANGED")

if successor.get("historical_18639_pair_matrix") != base.get(
    "historical_18639_pair_matrix"
):
    stop("HISTORICAL_METADATA_CHANGED")

if successor.get("pair_promotion_policy") != contract.get("successor_policy"):
    stop("SUCCESSOR_PROMOTION_POLICY_INVALID")

if len(base["pairs"]) != 1853 or len(successor["pairs"]) != 1853:
    stop("PAIR_UNIVERSE_COUNT_INVALID")

pair_re = re.compile(
    r"(?m)^## Candidate Pair ([0-9]{3})[ \t]*$"
)

matches = list(pair_re.finditer(packet))

if [m.group(1) for m in matches] != [
    f"{i:03d}" for i in range(1, 212)
]:
    stop("PACKET_SEQUENCE_INVALID")

candidate_pairs = []

for i, m in enumerate(matches):
    end = matches[i + 1].start() if i + 1 < len(matches) else len(packet)
    block = packet[m.start():end]

    req = re.search(
        r'^Requirement ID \(exact\):[ \t]*"([^"]+)"[ \t]*$',
        block,
        re.MULTILINE
    )
    unit = re.search(
        r'^Semantic-unit ID \(exact\):[ \t]*"([^"]+)"[ \t]*$',
        block,
        re.MULTILINE
    )

    if not req or not unit:
        stop("PACKET_IDENTITY_MISSING", m.group(1))

    candidate_pairs.append((req.group(1), unit.group(1)))

candidate_set = set(candidate_pairs)

if len(candidate_set) != 211:
    stop("CANDIDATE_SET_NOT_211")

base_index = {
    (r["requirement_id"], r["semantic_unit_id"]): r
    for r in base["pairs"]
}

succ_index = {
    (r["requirement_id"], r["semantic_unit_id"]): r
    for r in successor["pairs"]
}

if len(base_index) != 1853 or len(succ_index) != 1853:
    stop("PAIR_IDENTITIES_NOT_UNIQUE")

if set(base_index) != set(succ_index):
    stop("PAIR_IDENTITY_UNIVERSE_CHANGED")

transform = contract["candidate_pair_transformation"]

allowed_changed = {
    "classification",
    "classification_basis",
    "evidence_gap",
    "positive_binding_claimed",
    "human_semantic_judgment_used",
}

candidate_changed = 0
noncandidate_changed = 0

for key in base_index:
    before = base_index[key]
    after = succ_index[key]

    if key not in candidate_set:
        if before != after:
            noncandidate_changed += 1
        continue

    changed = {
        k
        for k in set(before) | set(after)
        if before.get(k) != after.get(k)
    }

    if changed != allowed_changed:
        stop(
            "PROMOTED_PAIR_CHANGED_FIELD_SET_INVALID",
            repr((key, sorted(changed)))
        )

    if before["classification"] != "UNRESOLVED_BINDING":
        stop("PROMOTED_PAIR_BASE_PRESTATE_INVALID", repr(key))

    if after["classification"] != "SUPPORTED_BINDING":
        stop("PROMOTED_PAIR_SUCCESSOR_STATE_INVALID", repr(key))

    if after["classification_basis"] != transform["classification_basis"]:
        stop("PROMOTED_PAIR_BASIS_INVALID", repr(key))

    if after["evidence_gap"] != transform["evidence_gap"]:
        stop("PROMOTED_PAIR_EVIDENCE_GAP_INVALID", repr(key))

    if after["positive_binding_claimed"] is not True:
        stop("PROMOTED_PAIR_POSITIVE_FLAG_INVALID", repr(key))

    if after["human_semantic_judgment_used"] is not True:
        stop("PROMOTED_PAIR_HUMAN_FLAG_INVALID", repr(key))

    for field in (
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
        if after[field] is not False:
            stop("UNAUTHORIZED_PROMOTED_PAIR_FLAG_TRUE", field)

    candidate_changed += 1

if candidate_changed != 211:
    stop("PROMOTED_PAIR_COUNT_NOT_211", str(candidate_changed))

if noncandidate_changed != 0:
    stop("NONCANDIDATE_RECORD_CHANGE_DETECTED", str(noncandidate_changed))

states = Counter(
    r["classification"]
    for r in successor["pairs"]
)

if states.get("SUPPORTED_BINDING", 0) != 211:
    stop("SUPPORTED_BINDING_COUNT_INVALID")

if states.get("UNRESOLVED_BINDING", 0) != 1642:
    stop("UNRESOLVED_BINDING_COUNT_INVALID")

if states.get("NOT_SUPPORTED_BINDING", 0) != 0:
    stop("NOT_SUPPORTED_BINDING_COUNT_INVALID")

if execution.get("supported_binding_count") != 211:
    stop("EXECUTION_MANIFEST_SUPPORTED_COUNT_INVALID")

if execution.get("unresolved_binding_count") != 1642:
    stop("EXECUTION_MANIFEST_UNRESOLVED_COUNT_INVALID")

if execution.get("not_supported_binding_count") != 0:
    stop("EXECUTION_MANIFEST_NOT_SUPPORTED_COUNT_INVALID")

if execution.get("noncandidate_pair_records_changed") != 0:
    stop("EXECUTION_MANIFEST_NONCANDIDATE_CHANGE_INVALID")

for key in (
    "operational_mapping_created",
    "schema_mapping_inferred",
    "negative_binding_created",
    "original_pair_matrix_modified",
    "analyzer_authorized",
    "baseline_authorized",
    "repair_authorized",
):
    if execution.get(key) is not False:
        stop("EXECUTION_MANIFEST_BOUNDARY_INVALID", key)

print("BOUNDED_SUPPORTED_BINDING_SUCCESSOR_VERIFIER=PASS")
print("BASE_MATRIX_SHA256=" + EXPECTED_BASE_SHA)
print("BASE_MATRIX_MODIFIED=NO")
print("SUCCESSOR_PAIR_UNIVERSE_COUNT=1853")
print("SUPPORTED_BINDING_COUNT=211")
print("UNRESOLVED_BINDING_COUNT=1642")
print("NOT_SUPPORTED_BINDING_COUNT=0")
print("EXACT_PROMOTED_PAIR_COUNT=211")
print("NONCANDIDATE_PAIR_RECORDS_CHANGED=0")
print("POSITIVE_BINDING_CLAIMED_FOR_PROMOTED_PAIRS=YES")
print("HUMAN_SEMANTIC_JUDGMENT_USED_FOR_PROMOTED_PAIRS=YES")
print("OPERATIONAL_MAPPING_CREATED=NO")
print("SCHEMA_MAPPING_INFERRED=NO")
print("DECISION0190_P03_EXECUTION_COUNT=1")
print("DECISION0190_P03_RESULT=PASS")
print("DECISION0190_P03_STATE=PERMANENTLY_RETIRED")
print("DECISION0190_P03_RERUN_AUTHORIZED=NO")
print("DECISION0187_A02_RERUN=NO")
print("D0188_CRLF_SAFE_SUCCESSOR_RERUN=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
