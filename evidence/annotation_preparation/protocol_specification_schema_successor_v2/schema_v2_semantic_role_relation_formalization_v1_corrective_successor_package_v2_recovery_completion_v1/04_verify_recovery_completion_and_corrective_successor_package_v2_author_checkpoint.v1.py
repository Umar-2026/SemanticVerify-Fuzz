#!/usr/bin/env python3

import hashlib
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(
    "/openbayes/home/semanticverify-fuzz-research"
)

HERE = Path(__file__).resolve().parent

BASE = (
    REPO
    / "evidence/annotation_preparation/protocol_specification_schema_successor_v2"
)

SUCCESSOR = (
    BASE
    / "schema_v2_semantic_role_relation_formalization_v1_corrective_successor_package_v2"
)

REC_AUTH = (
    BASE
    / "schema_v2_semantic_role_relation_formalization_v1_corrective_successor_package_v2_recovery_authorization"
)

C01 = (
    HERE
    / "01_final_recovery_authorization_verifier_output.EXACT_RECONSTRUCTED.v1.txt"
)

C02 = (
    HERE
    / "02_recovery_completion_record.v1.json"
)

C03 = (
    HERE
    / "03_post_recovery_safe_successor_verifier_output.v1.txt"
)

C05 = (
    HERE
    / "05_recovery_completion_and_author_checkpoint.v1.SHA256SUMS"
)

SAFE = (
    SUCCESSOR
    / "05_verify_corrective_successor_package_v2.py"
)

SUMS = (
    SUCCESSOR
    / "07_corrective_successor_package_v2.SHA256SUMS"
)

R01 = (
    REC_AUTH
    / "01_partial_successor_package_pre_recovery_inventory.v1.SHA256SUMS"
)

R03 = (
    REC_AUTH
    / "03_verify_post_final_authorization_run_recovery_authorization.v1.py"
)

AUTH0095_VERIFIER = (
    BASE
    / "schema_v2_semantic_role_relation_formalization_v1_corrective_successor_package_v2_authorization"
    / "02_verify_corrective_successor_package_v2_authorization.v1.py"
)

EXPECTED = {
    C01:
        "3ffce5cec14ed4bee20d13a0d2242db1a4a6e2d1264fa521a13bf0b7480238ee",

    SAFE:
        "2c053a69dd183faa896364a61e5a2c337876c59735313c421e2acb63cd13a63a",

    SUMS:
        "a6dc0402138a5c59a59202795d3616e67439b20ff5df4a0c1ccf27caa3eb7f95",

    R01:
        "7696e37f1f19b0fe5731eaea55e48d762467d7c1397ab234e76c7610315ba2c7",

    R03:
        "180c58974f894788884d75f9e0ae8964e4d2a9df5ff418e52b1856c282a920e4",

    AUTH0095_VERIFIER:
        "4c4a1feca0496055035e57389f0c581542e97ac72a46d10137f657208743093b",
}

def fail(msg):
    print(
        "FAIL|" + msg
    )
    raise SystemExit(1)

def sha(path):
    if not path.is_file():
        fail(
            "MISSING|" + str(path)
        )

    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()

for path, expected in EXPECTED.items():
    actual = sha(path)

    if actual != expected:
        fail(
            "SHA|"
            + str(path)
            + "|ACTUAL="
            + actual
        )

if C01.stat().st_size != 899:
    fail(
        "FINAL_RECOVERY_OUTPUT_SIZE"
    )

record = json.loads(
    C02.read_text(
        encoding="utf-8"
    )
)

if record["status"] != "RECOVERY_COMPLETE_AUTHOR_CHECKPOINT_READY":
    fail(
        "RECOVERY_COMPLETION_STATUS"
    )

d96 = record[
    "decision_0096_recovery_authorization"
]

if d96["final_allowed_run_completed"] is not True:
    fail(
        "DECISION0096_FINAL_RUN"
    )

if d96["final_allowed_run_result"] != "PASS":
    fail(
        "DECISION0096_FINAL_RESULT"
    )

if d96[
    "final_allowed_output_sha256"
] != EXPECTED[C01]:
    fail(
        "DECISION0096_FINAL_OUTPUT_BINDING"
    )

if d96[
    "reconstruction_cryptographically_matches_original_tee_hash_and_size"
] is not True:
    fail(
        "RECOVERY_OUTPUT_RECONSTRUCTION"
    )

if d96[
    "recovery_authorization_verifier_permanently_retired"
] is not True:
    fail(
        "DECISION0096_RETIREMENT"
    )

if d96[
    "recovery_authorization_verifier_rerun_allowed"
] is not False:
    fail(
        "DECISION0096_RERUN"
    )

d95 = record[
    "decision_0095_authorization_verifier"
]

if d95["permanently_retired"] is not True:
    fail(
        "DECISION0095_RETIREMENT"
    )

if d95["rerun_allowed"] is not False:
    fail(
        "DECISION0095_RERUN"
    )

recovery = record[
    "authorized_recovery"
]

if recovery["result"] != "PASS":
    fail(
        "RECOVERY_RESULT"
    )

if recovery["changed_files"] != [
    "05_verify_corrective_successor_package_v2.py",
    "07_corrective_successor_package_v2.SHA256SUMS",
]:
    fail(
        "RECOVERY_CHANGED_FILES"
    )

if recovery["changed_file_count"] != 2:
    fail(
        "RECOVERY_CHANGED_COUNT"
    )

if recovery["unchanged_file_count"] != 45:
    fail(
        "RECOVERY_UNCHANGED_COUNT"
    )

if recovery[
    "unauthorized_package_file_change_count"
] != 0:
    fail(
        "RECOVERY_UNAUTHORIZED_CHANGE"
    )

# ------------------------------------------------------------
# Re-prove exact 2-file recovery delta from pre-recovery snapshot.
# ------------------------------------------------------------

pre = {}

for raw in R01.read_text(
    encoding="utf-8"
).splitlines():
    if not raw.strip():
        continue

    digest, rel = raw.split(
        None,
        1,
    )

    rel = rel.strip()

    if rel.startswith("*"):
        rel = rel[1:]

    if rel.startswith("./"):
        rel = rel[2:]

    pre[rel] = digest

if len(pre) != 47:
    fail(
        "PRE_RECOVERY_SNAPSHOT_COUNT"
    )

current_paths = {
    str(
        p.relative_to(
            SUCCESSOR
        )
    )
    for p in SUCCESSOR.rglob("*")
    if p.is_file()
}

if current_paths != set(pre):
    fail(
        "SUCCESSOR_FILE_SET"
    )

changed = []

for rel, old_sha in sorted(pre.items()):
    current_sha = sha(
        SUCCESSOR / rel
    )

    if current_sha != old_sha:
        changed.append(rel)

if changed != recovery["changed_files"]:
    fail(
        "RECOVERY_DELTA_REPRODUCTION"
    )

# ------------------------------------------------------------
# Package checksum closure.
# ------------------------------------------------------------

sum_lines = [
    line
    for line in SUMS.read_text(
        encoding="utf-8"
    ).splitlines()
    if line.strip()
]

if len(sum_lines) != 46:
    fail(
        "PACKAGE_SUM_COUNT"
    )

for raw in sum_lines:
    digest, rel = raw.split(
        None,
        1,
    )

    rel = rel.strip()

    if rel.startswith("*"):
        rel = rel[1:]

    if rel.startswith("./"):
        rel = rel[2:]

    target = SUCCESSOR / rel

    if sha(target) != digest:
        fail(
            "PACKAGE_SUM|" + rel
        )

# ------------------------------------------------------------
# Execute only the SAFE post-recovery successor verifier.
# Never execute R03 or Decision-0095 verifier.
# ------------------------------------------------------------

proc = subprocess.run(
    [
        sys.executable,
        str(SAFE),
    ],
    cwd=str(SUCCESSOR),
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    check=False,
)

if proc.returncode != 0:
    fail(
        "SAFE_SUCCESSOR_VERIFIER_RETURN_CODE|"
        + str(proc.returncode)
    )

if proc.stdout != C03.read_bytes():
    fail(
        "SAFE_SUCCESSOR_OUTPUT_BINDING"
    )

if (
    b"CORRECTIVE_SUCCESSOR_PACKAGE_V2=PASS"
    not in proc.stdout
):
    fail(
        "SAFE_SUCCESSOR_PASS_MARKER"
    )

safe_state = record[
    "post_recovery_safe_verification"
]

if sha(C03) != safe_state["output_sha256"]:
    fail(
        "SAFE_OUTPUT_RECORD_SHA"
    )

if C03.stat().st_size != safe_state["output_size_bytes"]:
    fail(
        "SAFE_OUTPUT_RECORD_SIZE"
    )

package = record[
    "corrective_successor_package_v2"
]

if package["file_count"] != 47:
    fail(
        "PACKAGE_FILE_COUNT"
    )

if package[
    "status"
] != "AUTHOR_CANDIDATE_AWAITING_FOCUSED_INDEPENDENT_HUMAN_REREVIEW":
    fail(
        "PACKAGE_STATUS"
    )

review = record[
    "review_state"
]

if review[
    "original_overall_human_review"
] != "REVISION_REQUIRED":
    fail(
        "ORIGINAL_REVIEW_STATE"
    )

if review[
    "focused_rereview_packet"
] != "BLANK":
    fail(
        "FOCUSED_PACKET_STATE"
    )

if review[
    "focused_human_decision_exists"
] is not False:
    fail(
        "FOCUSED_DECISION"
    )

if review[
    "focused_human_approval_exists"
] is not False:
    fail(
        "FOCUSED_APPROVAL"
    )

if review[
    "formalization_v1_approved"
] is not False:
    fail(
        "FORMALIZATION_APPROVAL"
    )

for key, value in record[
    "bounded_nonclaims"
].items():
    if value is not False:
        fail(
            "NONCLAIM|" + key
        )

# ------------------------------------------------------------
# Completion evidence checksum closure.
# ------------------------------------------------------------

if C05.is_file():
    lines = [
        line
        for line in C05.read_text(
            encoding="utf-8"
        ).splitlines()
        if line.strip()
    ]

    if len(lines) != 4:
        fail(
            "COMPLETION_SUM_COUNT"
        )

    for raw in lines:
        digest, rel = raw.split(
            None,
            1,
        )

        rel = rel.strip()

        if rel.startswith("*"):
            rel = rel[1:]

        target = HERE / rel

        if sha(target) != digest:
            fail(
                "COMPLETION_SUM|" + rel
            )

print("FINAL_DECISION_0096_RECOVERY_OUTPUT_EXACT_BINDING=PASS")
print("DECISION_0095_VERIFIER_EXECUTED=NO")
print("DECISION_0096_RECOVERY_VERIFIER_EXECUTED=NO")
print("BOTH_PRE_MUTATION_GOVERNANCE_VERIFIERS_PERMANENTLY_RETIRED=YES")

print("RECOVERY_CHANGED_FILE_COUNT=2")
print("RECOVERY_UNCHANGED_FILE_COUNT=45")
print("RECOVERY_UNAUTHORIZED_CHANGE_COUNT=0")

print("CORRECTIVE_SUCCESSOR_PACKAGE_V2_FILE_COUNT=47")
print("CORRECTIVE_SUCCESSOR_PACKAGE_V2_SAFE_VERIFIER=PASS")
print("CORRECTIVE_SUCCESSOR_PACKAGE_V2_STATUS=AUTHOR_CANDIDATE_AWAITING_FOCUSED_INDEPENDENT_HUMAN_REREVIEW")

print("ORIGINAL_OVERALL_HUMAN_REVIEW=REVISION_REQUIRED")
print("FOCUSED_REREVIEW_PACKET=BLANK")
print("FOCUSED_HUMAN_DECISION_EXISTS=NO")
print("FOCUSED_HUMAN_APPROVAL_EXISTS=NO")
print("FORMALIZATION_V1_APPROVED=NO")

print("OPERATIONAL_POSITIVE_MAPPING_AUTHORIZED=NO")
print("SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO")
print("CURL_JSON_AUTHORIZED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")

print("DECISION_0097_RECOVERY_COMPLETION_AND_AUTHOR_CHECKPOINT_VERIFICATION=PASS")
