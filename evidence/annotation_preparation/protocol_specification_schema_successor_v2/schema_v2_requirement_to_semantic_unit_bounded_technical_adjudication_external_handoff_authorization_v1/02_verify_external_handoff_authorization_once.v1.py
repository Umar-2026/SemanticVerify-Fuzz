#!/usr/bin/env python3

from pathlib import Path
import datetime
import hashlib
import json
import os
import re
import subprocess
import sys

EXPECTED_PARENT = "a85b34b4918225812b2d4cd4a057db064c88df5e"

BASE = Path(
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2"
)

PKG_DIR = (
    BASE
    / "schema_v2_requirement_to_semantic_unit_"
      "bounded_technical_adjudication_package_v1"
)

AUTH_DIR = (
    BASE
    / "schema_v2_requirement_to_semantic_unit_"
      "bounded_technical_adjudication_external_"
      "handoff_authorization_v1"
)

P01 = PKG_DIR / "01_package_manifest.v1.json"
P02 = PKG_DIR / "02_211_candidate_pair_inventory.v1.json"
P03 = PKG_DIR / "03_blank_technical_adjudication_packet.v1.md"
P04 = PKG_DIR / "04_technical_adjudicator_instructions.v1.md"
P09 = PKG_DIR / "09_verify_bounded_technical_adjudication_package_v1.py"
P10 = PKG_DIR / "10_bounded_technical_adjudication_package_v1.SHA256SUMS"

A01 = AUTH_DIR / "01_external_handoff_authorization.v1.json"
A03 = AUTH_DIR / "03_one_time_verifier_lifecycle.v1.json"

DECISION = Path(
    "documentation/decisions/"
    "0185-authorize-external-human-technical-"
    "adjudication-handoff-v1.md"
)

EXPECTED_PKG_TREE = "ccf5fc04a9d80607767f79ed8c298a663378cb08"

EXPECTED_P01_SHA = "c5e86f8354fc296adafcb4b33fef3f1979e37bd670c545dd8f64b20c58fd354b"
EXPECTED_P02_SHA = "8f77fe6454fef755317f3d590c80326f79d504308b2638416013ca2ba77ba8b9"
EXPECTED_P03_SHA = "c135cd488c94be4aa94017c0684aa7a22993d9de923ff1ee3b5f389f40a7e6e0"
EXPECTED_P04_SHA = "e3df28a1d65067a050fcc996f8df0aa45121a1b2430f470f807b8d226f003018"
EXPECTED_P09_SHA = "3f8fff762cd971fb1c5b687b8b3e8b392e799d57879ac34825b46d23e8f15971"
EXPECTED_P10_SHA = "37ff75211e7fb4881d00189b2cf8f9ba5ad404abc36b7c44f7cc5f632df39737"

SENTINEL = Path(
    "/openbayes/home/"
    ".semanticverify-fuzz-decision0185-a02-"
    "single-execution-reservation.v1.json"
)

OUTPUT = Path(
    "/openbayes/home/"
    "decision0185_a02_single_execution_output.v1.txt"
)


def stop(message):
    print("DECISION0185_A02_RESULT=FAIL")
    print("FAILURE=" + message)
    raise SystemExit(186)


def sha256(path):
    h = hashlib.sha256()

    with path.open("rb") as f:
        for chunk in iter(
            lambda: f.read(1024 * 1024),
            b"",
        ):
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

if git(
    "status",
    "--porcelain=v1",
    "--untracked-files=all",
):
    stop("REPOSITORY_NOT_CLEAN")

head = git("rev-parse", "HEAD")
parent = git("rev-parse", "HEAD^")

if parent != EXPECTED_PARENT:
    stop("DECISION0185_PARENT_MISMATCH")

if git("rev-parse", f"HEAD:{PKG_DIR}") != EXPECTED_PKG_TREE:
    stop("PACKAGE_TREE_MISMATCH")

for path in [
    P01, P02, P03, P04, P09, P10,
    A01, A03, DECISION,
]:
    if not path.is_file():
        stop("REQUIRED_FILE_MISSING|" + str(path))

try:
    subprocess.check_output(
        [
            "git",
            "ls-files",
            "--error-unmatch",
            str(DECISION),
        ],
        text=True,
        stderr=subprocess.DEVNULL,
    )
except subprocess.CalledProcessError:
    stop("DECISION0185_NOT_TRACKED")

expected_hashes = {
    P01: EXPECTED_P01_SHA,
    P02: EXPECTED_P02_SHA,
    P03: EXPECTED_P03_SHA,
    P04: EXPECTED_P04_SHA,
    P09: EXPECTED_P09_SHA,
    P10: EXPECTED_P10_SHA,
}

for path, expected in expected_hashes.items():
    if sha256(path) != expected:
        stop("PACKAGE_FILE_HASH_MISMATCH|" + str(path))

safe_result = subprocess.run(
    ["python3", str(P09)],
    text=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
)

if safe_result.returncode != 0:
    print(safe_result.stdout, end="")
    stop("PACKAGE_SAFE_VERIFIER_FAILED")

if (
    "SAFE_TECHNICAL_ADJUDICATION_PACKAGE_VERIFIER_RESULT=PASS"
    not in safe_result.stdout
):
    stop("PACKAGE_SAFE_VERIFIER_PASS_MARKER_MISSING")

a01 = json.loads(
    A01.read_text(encoding="utf-8")
)

a03 = json.loads(
    A03.read_text(encoding="utf-8")
)

manifest = json.loads(
    P01.read_text(encoding="utf-8")
)

inventory = json.loads(
    P02.read_text(encoding="utf-8")
)

blank = P03.read_text(
    encoding="utf-8"
)

if a01.get("decision") != "Decision0185":
    stop("A01_DECISION_BINDING_INVALID")

if a01.get("authorization_status") != \
        "AUTHORIZED_FOR_SEPARATE_NEXT_TRANSACTION":
    stop("A01_AUTHORIZATION_STATUS_INVALID")

if a01.get("authorization_scope") != \
        "AUTHOR_EXTERNAL_HUMAN_TECHNICAL_ADJUDICATION_HANDOFF_FOR_EXISTING_NEUTRAL_211_PAIR_PACKAGE_V1":
    stop("A01_SCOPE_INVALID")

if a03.get("state") != "ACTIVE_UNCONSUMED":
    stop("A03_NOT_ACTIVE_UNCONSUMED")

if a03.get("execution_count") != 0:
    stop("A03_EXECUTION_COUNT_INVALID")

if a03.get(
    "authorized_execution_transaction"
) != "Decision0186":
    stop("A03_EXECUTION_TRANSACTION_INVALID")

if a03.get("rerun_authorized") is not False:
    stop("A03_RERUN_BOUNDARY_INVALID")

if manifest.get("bounded_pair_count") != 211:
    stop("MANIFEST_PAIR_COUNT_INVALID")

if manifest.get("adjudicator_identity_prefilled") is not False:
    stop("MANIFEST_IDENTITY_PREFILL_INVALID")

if manifest.get("adjudication_outcomes_prefilled") is not False:
    stop("MANIFEST_OUTCOME_PREFILL_INVALID")

records = inventory.get("records", [])

if len(records) != 211:
    stop("INVENTORY_RECORD_COUNT_INVALID")

for record in records:
    if record.get("technical_adjudication_state") != "":
        stop("INVENTORY_ADJUDICATION_STATE_PREFILLED")

    if record.get(
        "technical_adjudication_rationale"
    ) != "":
        stop("INVENTORY_ADJUDICATION_RATIONALE_PREFILLED")

    if record.get(
        "technical_adjudicator_notes"
    ) != "":
        stop("INVENTORY_ADJUDICATOR_NOTES_PREFILLED")

pair_headings = re.findall(
    r"(?m)^## Candidate Pair (\d{3})$",
    blank,
)

if pair_headings != [
    f"{i:03d}"
    for i in range(1, 212)
]:
    stop("BLANK_PACKET_PAIR_STRUCTURE_INVALID")

for label in [
    "Technical adjudication state:",
    "Technical adjudication rationale:",
    "Technical adjudicator notes:",
]:
    lines = [
        line
        for line in blank.splitlines()
        if line.startswith(label)
    ]

    if len(lines) != 211:
        stop("BLANK_FIELD_COUNT_INVALID|" + label)

    if any(
        line.strip() != label
        for line in lines
    ):
        stop("BLANK_FIELD_PREFILLED|" + label)

for label in [
    "Human technical adjudicator name:",
    "Human technical adjudicator role:",
    "Human technical adjudicator confirmation/signature:",
    "Human technical adjudicator date:",
    "Human technical adjudicator attestation:",
]:
    lines = [
        line
        for line in blank.splitlines()
        if line.startswith(label)
    ]

    if len(lines) != 1:
        stop("HUMAN_FIELD_COUNT_INVALID|" + label)

    if lines[0].strip() != label:
        stop("HUMAN_FIELD_PREFILLED|" + label)

reservation = {
    "artifact": "decision0185_a02_single_execution_reservation_v1",
    "decision": "Decision0185",
    "execution_transaction": "Decision0186",
    "authorized_head_at_execution": head,
    "technical_adjudication_package_tree": EXPECTED_PKG_TREE,
    "blank_adjudication_packet_sha256": EXPECTED_P03_SHA,
    "bounded_pair_count": 211,
    "state": "PERMANENTLY_RETIRED_AFTER_THIS_EXECUTION",
    "rerun_authorized": False,
    "reserved_at_utc": datetime.datetime.now(
        datetime.timezone.utc
    ).isoformat(),
}

flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL

try:
    fd = os.open(
        str(SENTINEL),
        flags,
        0o444,
    )
except FileExistsError:
    stop("ONE_TIME_RESERVATION_COLLISION")

with os.fdopen(
    fd,
    "w",
    encoding="utf-8",
) as f:
    json.dump(
        reservation,
        f,
        indent=2,
        sort_keys=True,
    )
    f.write("\n")

lines = [
    "DECISION0185_A02_RESULT=PASS",
    "DECISION=Decision0185",
    "EXECUTION_TRANSACTION=Decision0186",
    f"AUTHORIZED_HEAD_AT_EXECUTION={head}",
    f"AUTHORIZED_PARENT={parent}",
    f"TECHNICAL_ADJUDICATION_PACKAGE_TREE={EXPECTED_PKG_TREE}",
    f"BLANK_ADJUDICATION_PACKET_SHA256={EXPECTED_P03_SHA}",
    "BOUNDED_PAIR_COUNT=211",
    "ADJUDICATION_STATES_PREFILLED=0",
    "ADJUDICATOR_IDENTITY_PREFILLED=NO",
    "EXTERNAL_HANDOFF_AUTHORING_AUTHORIZED=YES",
    "HUMAN_TECHNICAL_ADJUDICATION_PERFORMED=NO",
    "HUMAN_ADJUDICATION_RESULT_RECORDED=NO",
    "PAIR_RECLASSIFICATION_PERFORMED=NO",
    "PAIR_RECLASSIFICATION_AUTHORIZED=NO",
    "SUPPORTED_BINDING_CREATED=NO",
    "NOT_SUPPORTED_BINDING_CREATED=NO",
    "AUTOMATIC_PROMOTION_AUTHORIZED=NO",
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
