#!/usr/bin/env python3

from pathlib import Path
from collections import Counter, defaultdict
import datetime
import hashlib
import json
import os
import re
import subprocess
import sys

EXPECTED_PARENT = "63689901dd1e1a51c7462049eb208baefa7f0ea5"

BASE = Path(
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2"
)

AUTH_DIR = (
    BASE
    / "schema_v2_requirement_to_semantic_unit_recorded_"
      "positive_binding_technical_adjudication_package_authorization_v1"
)

A01 = AUTH_DIR / "01_technical_adjudication_package_authorization.v1.json"
A03 = AUTH_DIR / "03_one_time_verifier_lifecycle.v1.json"

DECISION = Path(
    "documentation/decisions/"
    "0183-authorize-bounded-technical-adjudication-package-"
    "for-recorded-positive-binding-evidence-v1.md"
)

R02 = (
    BASE
    / "schema_v2_requirement_to_semantic_unit_completed_human_"
      "positive_binding_evidence_record_v1"
    / "02_completed_human_positive_binding_evidence_packet.EXACT_COPY.v1.md"
)

MATRIX = (
    BASE
    / "schema_v2_requirement_to_semantic_unit_crosswalk_"
      "evidence_resolution_study_v1"
    / "04_requirement_semantic_unit_pair_matrix.v1.json"
)

EXPECTED_R02_SHA = (
    "effd2848702219741e3814d2dc283284"
    "c92ab07f49980cd799fde351ecb8b685"
)

EXPECTED_R02_SIZE = 20425

EXPECTED_MATRIX_SHA = (
    "389615002582964b97aa6eb717ceb5200"
    "67cef78b18cf482cf257fe9b36f2515"
)

SENTINEL = Path(
    "/openbayes/home/"
    ".semanticverify-fuzz-decision0183-a02-single-execution-reservation.v1.json"
)

OUTPUT = Path(
    "/openbayes/home/"
    "decision0183_a02_single_execution_output.v1.txt"
)


def stop(message):
    print("DECISION0183_A02_RESULT=FAIL")
    print("FAILURE=" + message)
    raise SystemExit(184)


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def git(*args):
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
    stop("DECISION0183_PARENT_MISMATCH")

for path in [A01, A03, DECISION, R02, MATRIX]:
    if not path.is_file():
        stop("REQUIRED_FILE_MISSING|" + str(path))

try:
    subprocess.check_output(
        ["git", "ls-files", "--error-unmatch", str(DECISION)],
        text=True,
        stderr=subprocess.DEVNULL,
    )
except subprocess.CalledProcessError:
    stop("DECISION0183_NOT_TRACKED")

if sha256(R02) != EXPECTED_R02_SHA:
    stop("RECORDED_PACKET_HASH_MISMATCH")

if R02.stat().st_size != EXPECTED_R02_SIZE:
    stop("RECORDED_PACKET_SIZE_MISMATCH")

if sha256(MATRIX) != EXPECTED_MATRIX_SHA:
    stop("PAIR_MATRIX_HASH_MISMATCH")

a01 = json.loads(A01.read_text(encoding="utf-8"))
a03 = json.loads(A03.read_text(encoding="utf-8"))

if a01.get("decision") != "Decision0183":
    stop("A01_DECISION_BINDING_INVALID")

if a01.get("authorization_status") != \
        "AUTHORIZED_FOR_SEPARATE_NEXT_TRANSACTION":
    stop("A01_AUTHORIZATION_STATUS_INVALID")

if a01.get("authorization_scope") != \
        "AUTHOR_NEUTRAL_BOUNDED_TECHNICAL_ADJUDICATION_PACKAGE_FOR_EXACTLY_211_RECORDED_POSITIVE_BINDING_PROPOSALS":
    stop("A01_SCOPE_INVALID")

scope = a01.get("bounded_scope", {})

expected_scope = {
    "recorded_positive_requirement_count": 15,
    "recorded_unresolved_requirement_count": 2,
    "candidate_positive_pair_count": 211,
    "candidate_pairs_present_in_governed_universe": 211,
    "candidate_pairs_currently_unresolved": 211,
    "candidate_pairs_already_supported": 0,
    "candidate_pairs_already_not_supported": 0,
}

if scope != expected_scope:
    stop("A01_BOUNDED_SCOPE_INVALID")

allowed = a01.get("allowed_future_adjudication_states", [])

if allowed != [
    "TECHNICAL_SUPPORT_CONFIRMED_PROMOTION_CANDIDATE",
    "TECHNICAL_SUPPORT_NOT_ESTABLISHED",
    "TECHNICAL_ADJUDICATION_UNRESOLVED",
]:
    stop("A01_ALLOWED_ADJUDICATION_STATES_INVALID")

if a03.get("state") != "ACTIVE_UNCONSUMED":
    stop("A03_NOT_ACTIVE_UNCONSUMED")

if a03.get("execution_count") != 0:
    stop("A03_EXECUTION_COUNT_INVALID")

if a03.get("authorized_execution_transaction") != "Decision0184":
    stop("A03_EXECUTION_TRANSACTION_INVALID")

if a03.get("rerun_authorized") is not False:
    stop("A03_RERUN_BOUNDARY_INVALID")

matrix_obj = json.loads(MATRIX.read_text(encoding="utf-8"))

req_ids = set()
unit_ids = set()

def find_domain(node):
    if isinstance(node, dict):
        for k, v in node.items():
            if k == "requirement_id" and isinstance(v, str):
                req_ids.add(v)

            if (
                isinstance(k, str)
                and "semantic" in k.lower()
                and "unit" in k.lower()
                and "id" in k.lower()
                and isinstance(v, str)
            ):
                unit_ids.add(v)

            find_domain(v)

    elif isinstance(node, list):
        for v in node:
            find_domain(v)

find_domain(matrix_obj)

recognized = {
    "UNRESOLVED_BINDING",
    "SUPPORTED_BINDING",
    "NOT_SUPPORTED_BINDING",
}

def scalar_strings(node):
    out = []

    if isinstance(node, dict):
        for v in node.values():
            out.extend(scalar_strings(v))

    elif isinstance(node, list):
        for v in node:
            out.extend(scalar_strings(v))

    elif isinstance(node, str):
        out.append(node)

    return out

pairs = defaultdict(set)

def walk(node):
    if isinstance(node, dict):
        vals = scalar_strings(node)

        req_here = {x for x in vals if x in req_ids}
        unit_here = {x for x in vals if x in unit_ids}
        state_here = {x for x in vals if x in recognized}

        if (
            len(req_here) == 1
            and len(unit_here) == 1
            and len(state_here) >= 1
        ):
            pair = (
                next(iter(req_here)),
                next(iter(unit_here)),
            )
            pairs[pair].update(state_here)

        for v in node.values():
            walk(v)

    elif isinstance(node, list):
        for v in node:
            walk(v)

walk(matrix_obj)

if len(pairs) != 1853:
    stop("PAIR_UNIVERSE_COUNT_INVALID")

state_counts = Counter()

for states in pairs.values():
    if len(states) == 1:
        state_counts[next(iter(states))] += 1
    else:
        state_counts["MULTIPLE"] += 1

if state_counts["UNRESOLVED_BINDING"] != 1853:
    stop("PAIR_UNIVERSE_NOT_ALL_UNRESOLVED")

if (
    state_counts["SUPPORTED_BINDING"] != 0
    or state_counts["NOT_SUPPORTED_BINDING"] != 0
    or state_counts["MULTIPLE"] != 0
):
    stop("PAIR_UNIVERSE_STATE_INVALID")

packet = R02.read_text(encoding="utf-8")

heading_rx = re.compile(r"(?m)^## Requirement (\d{2})$")
matches = list(heading_rx.finditer(packet))
human_marker = packet.find("# Human evidence-reviewer completion")

if len(matches) != 17 or human_marker < 0:
    stop("RECORDED_PACKET_STRUCTURE_INVALID")

candidate_pairs = []
positive_requirements = 0
unresolved_requirements = 0

for i, m in enumerate(matches):
    start = m.end()
    end = matches[i + 1].start() if i + 1 < len(matches) else human_marker
    body = packet[start:end]

    id_match = re.search(
        r'(?m)^Requirement ID \(exact\): (.+)$',
        body,
    )

    state_match = re.search(
        r'(?m)^Evidence state:\s*`?([^`\n]+)`?\s*$',
        body,
    )

    if not id_match or not state_match:
        stop("RECORDED_PACKET_REQUIRED_FIELD_MISSING")

    requirement_id = json.loads(id_match.group(1))
    state = state_match.group(1).strip()

    p_start = body.find("Proposed semantic-unit IDs:")
    r_start = body.find("Positive-binding rationale:")

    if p_start < 0 or r_start <= p_start:
        stop("RECORDED_PACKET_PROPOSAL_REGION_INVALID")

    proposal_region = body[
        p_start + len("Proposed semantic-unit IDs:"):
        r_start
    ].strip()

    if state == "POSITIVE_BINDING_PROPOSED":
        positive_requirements += 1

        ids = re.findall(
            r'(?m)^-\s+`([^`]+)`\s*$',
            proposal_region,
        )

        candidate_pairs.extend(
            (requirement_id, uid)
            for uid in ids
        )

    elif state == "UNRESOLVED_NO_POSITIVE_BINDING_PROPOSED":
        unresolved_requirements += 1

    else:
        stop("RECORDED_PACKET_STATE_INVALID")

candidate_set = set(candidate_pairs)

if positive_requirements != 15:
    stop("POSITIVE_REQUIREMENT_COUNT_INVALID")

if unresolved_requirements != 2:
    stop("UNRESOLVED_REQUIREMENT_COUNT_INVALID")

if len(candidate_pairs) != 211 or len(candidate_set) != 211:
    stop("CANDIDATE_PAIR_COUNT_INVALID")

if candidate_set - set(pairs):
    stop("CANDIDATE_PAIR_OUTSIDE_GOVERNED_UNIVERSE")

for pair in candidate_set:
    if pairs[pair] != {"UNRESOLVED_BINDING"}:
        stop("CANDIDATE_PAIR_NOT_CURRENTLY_UNRESOLVED")

reservation = {
    "artifact": "decision0183_a02_single_execution_reservation_v1",
    "decision": "Decision0183",
    "execution_transaction": "Decision0184",
    "authorized_head_at_execution": head,
    "recorded_packet_sha256": EXPECTED_R02_SHA,
    "pair_matrix_sha256": EXPECTED_MATRIX_SHA,
    "bounded_candidate_pair_count": 211,
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
    "DECISION0183_A02_RESULT=PASS",
    "DECISION=Decision0183",
    "EXECUTION_TRANSACTION=Decision0184",
    f"AUTHORIZED_HEAD_AT_EXECUTION={head}",
    f"AUTHORIZED_PARENT={parent}",
    f"RECORDED_PACKET_SHA256={EXPECTED_R02_SHA}",
    f"PAIR_MATRIX_SHA256={EXPECTED_MATRIX_SHA}",
    "GOVERNED_PAIR_UNIVERSE_COUNT=1853",
    "GOVERNED_UNRESOLVED_PAIR_COUNT=1853",
    "BOUNDED_TECHNICAL_ADJUDICATION_PAIR_SCOPE=211",
    "BOUNDED_SCOPE_PAIRS_CURRENTLY_UNRESOLVED=211",
    "TECHNICAL_ADJUDICATION_PERFORMED=NO",
    "PAIR_RECLASSIFICATION_PERFORMED=NO",
    "PAIR_RECLASSIFICATION_AUTHORIZED=NO",
    "AUTOMATIC_PROMOTION_AUTHORIZED=NO",
    "NOT_SUPPORTED_BINDING_AUTHORIZED=NO",
    "OPERATIONAL_MAPPING_AUTHORIZED=NO",
    "ANALYZER_IMPLEMENTATION_AUTHORIZED=NO",
    "ANALYZER_EXECUTION_AUTHORIZED=NO",
    "BASELINE_EXECUTION_AUTHORIZED=NO",
    "REPAIR_IMPLEMENTATION_AUTHORIZED=NO",
    "REPAIR_EXECUTION_AUTHORIZED=NO",
    "ONE_TIME_VERIFIER_STATE=PERMANENTLY_RETIRED",
    "RERUN_AUTHORIZED=NO",
]

OUTPUT.write_text(
    "\n".join(lines) + "\n",
    encoding="utf-8",
)

OUTPUT.chmod(0o444)

print("\n".join(lines))
