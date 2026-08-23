#!/usr/bin/env python3

import hashlib
import json
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

SNAPSHOT = (
    HERE
    / "01_partial_successor_package_pre_recovery_inventory.v1.SHA256SUMS"
)

AUTH = (
    HERE
    / "02_post_final_authorization_run_recovery_authorization.v1.json"
)

SAFE = (
    SUCCESSOR
    / "05_verify_corrective_successor_package_v2.py"
)

SUMS = (
    SUCCESSOR
    / "07_corrective_successor_package_v2.SHA256SUMS"
)

CONSUMED = (
    SUCCESSOR
    / "06_decision_0095_authorization_verifier_consumed.v1.json"
)

FINAL_OUT = (
    SUCCESSOR
    / "decision_0095_authorization_exact"
    / "04_final_allowed_authorization_verifier_output.v1.txt"
)

DECISION0095_VERIFIER = (
    BASE
    / "schema_v2_semantic_role_relation_formalization_v1_corrective_successor_package_v2_authorization"
    / "02_verify_corrective_successor_package_v2_authorization.v1.py"
)

EXPECTED_DECISION0095_VERIFIER_SHA = \
    "4c4a1feca0496055035e57389f0c581542e97ac72a46d10137f657208743093b"

EXPECTED_SAFE_SHA = \
    "20324afe760f80ed7405b6987788bb6e9d969d7addfa8b4f7dd4c03bb6271ba0"

EXPECTED_SUMS_SHA = \
    "510e5ba577d2bcc2c9f094ac9d1ef613be22dc489af61910966e87c44b15c6bf"

EXPECTED_FINAL_OUT_SHA = \
    "07c8cbaf7ac1c7adf393c340d77c316c9663c4c61e3216489b19ff021e317ce5"

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

# ------------------------------------------------------------
# Decision-0095 verifier: hash only, NEVER execute.
# ------------------------------------------------------------

if sha(
    DECISION0095_VERIFIER
) != EXPECTED_DECISION0095_VERIFIER_SHA:
    fail(
        "DECISION0095_VERIFIER_SHA"
    )

# ------------------------------------------------------------
# Exact pre-recovery partial state.
# ------------------------------------------------------------

if sha(SAFE) != EXPECTED_SAFE_SHA:
    fail(
        "SAFE_PRE_RECOVERY_SHA"
    )

if sha(SUMS) != EXPECTED_SUMS_SHA:
    fail(
        "PACKAGE_SUMS_PRE_RECOVERY_SHA"
    )

if sha(FINAL_OUT) != EXPECTED_FINAL_OUT_SHA:
    fail(
        "FINAL_AUTH_OUTPUT_SHA"
    )

snapshot_lines = [
    line
    for line in SNAPSHOT.read_text(
        encoding="utf-8"
    ).splitlines()
    if line.strip()
]

if len(snapshot_lines) != 47:
    fail(
        "SNAPSHOT_ENTRY_COUNT"
    )

snapshot_paths = set()

for raw in snapshot_lines:
    parts = raw.split(
        None,
        1,
    )

    if len(parts) != 2:
        fail(
            "SNAPSHOT_LINE|" + raw
        )

    digest = parts[0]
    rel = parts[1].strip()

    if rel.startswith("*"):
        rel = rel[1:]

    if rel.startswith("./"):
        rel = rel[2:]

    target = (
        SUCCESSOR
        / rel
    )

    if not target.is_file():
        fail(
            "SNAPSHOT_FILE_MISSING|"
            + rel
        )

    actual = sha(target)

    if actual != digest:
        fail(
            "SNAPSHOT_SHA|"
            + rel
            + "|EXPECTED="
            + digest
            + "|ACTUAL="
            + actual
        )

    snapshot_paths.add(rel)

actual_paths = {
    str(
        p.relative_to(
            SUCCESSOR
        )
    )
    for p in SUCCESSOR.rglob("*")
    if p.is_file()
}

if actual_paths != snapshot_paths:
    fail(
        "PARTIAL_PACKAGE_FILE_SET_CHANGED"
    )

# ------------------------------------------------------------
# Final-run consumption evidence.
# ------------------------------------------------------------

consumed = json.loads(
    CONSUMED.read_text(
        encoding="utf-8"
    )
)

if consumed[
    "authorization_verifier_sha256"
] != EXPECTED_DECISION0095_VERIFIER_SHA:
    fail(
        "CONSUMED_VERIFIER_SHA"
    )

if consumed[
    "final_allowed_output_sha256"
] != EXPECTED_FINAL_OUT_SHA:
    fail(
        "CONSUMED_OUTPUT_SHA"
    )

if consumed[
    "final_allowed_run_result"
] != "PASS":
    fail(
        "CONSUMED_RESULT"
    )

if consumed[
    "final_allowed_run_performed"
] is not True:
    fail(
        "FINAL_RUN_FLAG"
    )

if consumed[
    "corrective_successor_package_v2_authoring_started_after_final_run"
] is not True:
    fail(
        "PACKAGE_AUTHORING_FLAG"
    )

if consumed[
    "authorization_verifier_permanently_retired"
] is not True:
    fail(
        "DECISION0095_RETIREMENT"
    )

if consumed[
    "authorization_verifier_must_never_be_rerun"
] is not True:
    fail(
        "DECISION0095_NEVER_RERUN"
    )

# ------------------------------------------------------------
# Exact diagnosed self-reference defect.
# ------------------------------------------------------------

text = SAFE.read_text(
    encoding="utf-8"
)

old = 'if "/openbayes/" in script_text:'

if text.count(old) != 1:
    fail(
        "OLD_SELF_CHECK_SITE_COUNT"
    )

literal_hits = [
    line
    for line in text.splitlines()
    if "/openbayes/" in line
]

if literal_hits != [
    old
]:
    fail(
        "OPENBAYES_LITERAL_SCOPE"
    )

new = (
    'absolute_path_prefix = "/" + "openbayes" + "/"\n\n'
    'if absolute_path_prefix in script_text:'
)

candidate = text.replace(
    old,
    new,
    1,
)

if "/openbayes/" in candidate:
    fail(
        "PROPOSED_PATCH_SELF_MATCH"
    )

# ------------------------------------------------------------
# Authorization scope.
# ------------------------------------------------------------

auth = json.loads(
    AUTH.read_text(
        encoding="utf-8"
    )
)

if auth[
    "status"
] != "AUTHORIZED_FOR_NARROW_EVIDENCE_ONLY_RECOVERY":
    fail(
        "AUTH_STATUS"
    )

if auth[
    "recovery_trigger"
] != "POST_FINAL_AUTHORIZATION_RUN_SAFE_VERIFIER_SELF_REFERENCE_FALSE_POSITIVE":
    fail(
        "AUTH_TRIGGER"
    )

allowed = auth[
    "authorized_mutations"
]

if len(allowed) != 2:
    fail(
        "AUTHORIZED_MUTATION_COUNT"
    )

if [
    x["path"]
    for x in allowed
] != [
    "05_verify_corrective_successor_package_v2.py",
    "07_corrective_successor_package_v2.SHA256SUMS",
]:
    fail(
        "AUTHORIZED_MUTATION_PATHS"
    )

for key, value in auth[
    "bounded_nonclaims"
].items():
    if value is not False:
        fail(
            "NONCLAIM|" + key
        )

print("PRE_RECOVERY_PARTIAL_PACKAGE_FILE_COUNT=47")
print("PRE_RECOVERY_PARTIAL_PACKAGE_EXACT_SNAPSHOT=PASS")

print("DECISION_0095_AUTHORIZATION_VERIFIER_EXECUTED=NO")
print("DECISION_0095_AUTHORIZATION_VERIFIER_PERMANENTLY_RETIRED=YES")
print("DECISION_0095_AUTHORIZATION_VERIFIER_RERUN_ALLOWED=NO")

print("SAFE_VERIFIER_SELF_REFERENCE_FALSE_POSITIVE=CONFIRMED")
print("RESEARCH_EVIDENCE_DEFECT_IDENTIFIED=NO")
print("RELATION_ROW_DEFECT_IDENTIFIED=NO")
print("SRR04_ERRATUM_DEFECT_IDENTIFIED=NO")

print("AUTHORIZED_RECOVERY_MUTATION_1=SAFE_VERIFIER_ONE_SITE_SELF_REFERENCE_CORRECTION")
print("AUTHORIZED_RECOVERY_MUTATION_2=DEPENDENT_PACKAGE_CHECKSUM_REGENERATION")
print("ALL_OTHER_PARTIAL_PACKAGE_FILES_MUST_REMAIN_BYTE_EXACT=YES")

print("OPERATIONAL_POSITIVE_MAPPING_AUTHORIZED=NO")
print("SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO")
print("CURL_JSON_AUTHORIZED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")

print("DECISION_0096_RECOVERY_AUTHORIZATION=PASS")
print("IMPORTANT=THIS_VERIFIER_IS_PRE_RECOVERY_MUTATION_ONLY")
