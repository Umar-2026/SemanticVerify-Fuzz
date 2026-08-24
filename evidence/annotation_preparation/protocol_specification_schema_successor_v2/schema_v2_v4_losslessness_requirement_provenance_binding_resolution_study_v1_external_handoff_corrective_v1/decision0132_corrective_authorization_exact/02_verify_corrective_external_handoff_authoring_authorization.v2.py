#!/usr/bin/env python3

import hashlib
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]

BASE_REL = (
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2"
)

PKG_REL = (
    BASE_REL
    + "/schema_v2_v4_losslessness_requirement_provenance_binding_resolution_study_v1_review_package_v1"
)

OLD_AUTH_REL = (
    BASE_REL
    + "/schema_v2_v4_losslessness_requirement_provenance_binding_resolution_study_v1_external_handoff_authorization_v1"
)

THIS_AUTH_REL = (
    BASE_REL
    + "/schema_v2_v4_losslessness_requirement_provenance_binding_resolution_study_v1_external_handoff_corrective_successor_authorization_v2"
)

PKG = REPO / PKG_REL
OLD_AUTH = REPO / OLD_AUTH_REL

AUTH = (
    HERE
    / "01_corrective_external_handoff_authoring_successor_authorization.v2.json"
)

FAILED_OUTPUT = (
    HERE
    / "03_decision0130_a02_failed_final_output.EXACT_COPY.v1.txt"
)

FAILED_SENTINEL = (
    HERE
    / "04_decision0130_a02_consumption_sentinel.EXACT_COPY.v1.txt"
)

SUMS = (
    HERE
    / "05_corrective_external_handoff_authoring_successor_authorization.v2.SHA256SUMS"
)

PKG_SAFE = (
    PKG
    / "09_verify_independent_review_package_v1.py"
)

PKG_SUMS = (
    PKG
    / "10_review_package_v1.SHA256SUMS"
)

OLD_A02 = (
    OLD_AUTH
    / "02_verify_external_independent_human_review_handoff_authoring_authorization.v1.py"
)

EXPECTED_DECISION0130_COMMIT = (
    "acccf40b8636609e7d98fd3a7d9575529777470d"
)

EXPECTED_DECISION0129_COMMIT = (
    "7ddaaa2e24a065053c132700292023dfaca9c428"
)

EXPECTED_PKG_TREE = (
    "35794b450ed9bcde337f4ea4b7de35dd8218cc03"
)

EXPECTED_OLD_AUTH_TREE = (
    "030017ebc1daaa22b4031a1a4b82533652ab7490"
)

EXPECTED_OLD_A02_SHA = (
    "ed9ce5e278f1f2b9b49f7d11715faaf"
    "bbd8e0873b20c961c4173d943e04965f4"
)

EXPECTED_FAILED_OUTPUT_SHA = (
    "4635ef9374bd8edb6278b185635033ce"
    "86fa891f387a821d656f626f71dd5a56"
)

EXPECTED_FAILED_SENTINEL_SHA = (
    "a977c957e4e8fc9177147d257c64014c"
    "faba0cc98bbbcd13ba44e1da7dd35bf0"
)

def fail(msg):
    print("FAIL|" + msg)
    raise SystemExit(1)

def sha(path):
    if not path.is_file():
        fail("MISSING|" + str(path))

    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()

def git(*args):
    p = subprocess.run(
        [
            "git",
            "-C",
            str(REPO),
            *args,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )

    if p.returncode != 0:
        fail(
            "GIT|"
            + " ".join(args)
            + "|"
            + p.stderr.strip()
        )

    return p.stdout.strip()

# ------------------------------------------------------------
# Correct checkpoint semantics:
#
# This verifier executes only after Decision 0132 has been committed.
# Therefore current HEAD must be an immediate successor of Decision 0130.
# We intentionally DO NOT require current HEAD == Decision 0129.
# ------------------------------------------------------------

current_head = git(
    "rev-parse",
    "HEAD",
)

current_parent = git(
    "show",
    "-s",
    "--format=%P",
    "HEAD",
)

if current_head == EXPECTED_DECISION0130_COMMIT:
    fail(
        "CORRECTIVE_AUTHORIZATION_NOT_COMMITTED"
    )

if current_head == EXPECTED_DECISION0129_COMMIT:
    fail(
        "INCORRECT_DECISION0129_EXECUTION_CHECKPOINT"
    )

if current_parent != EXPECTED_DECISION0130_COMMIT:
    fail(
        "CURRENT_HEAD_IS_NOT_IMMEDIATE_SUCCESSOR_OF_DECISION0130"
    )

if (
    git(
        "rev-parse",
        "HEAD:" + PKG_REL,
    )
    != EXPECTED_PKG_TREE
):
    fail(
        "REVIEW_PACKAGE_GIT_TREE"
    )

if (
    git(
        "rev-parse",
        "HEAD:" + OLD_AUTH_REL,
    )
    != EXPECTED_OLD_AUTH_TREE
):
    fail(
        "OLD_AUTHORIZATION_GIT_TREE"
    )

# This also proves the corrective authorization itself exists in the
# current committed checkpoint.
git(
    "cat-file",
    "-e",
    "HEAD:" + THIS_AUTH_REL,
)

if git(
    "status",
    "--porcelain=v1",
    "--untracked-files=all",
):
    fail(
        "REPOSITORY_NOT_CLEAN"
    )

# ------------------------------------------------------------
# Verify corrective authorization semantics
# ------------------------------------------------------------

auth = json.loads(
    AUTH.read_text(
        encoding="utf-8"
    )
)

if auth["status"] != "AUTHORIZED_NOT_YET_AUTHORED":
    fail(
        "AUTHORIZATION_STATUS"
    )

if (
    auth["authorization_type"]
    != "PRE_CORRECTIVE_EXTERNAL_HANDOFF_AUTHORING_ONLY"
):
    fail(
        "AUTHORIZATION_TYPE"
    )

pred = auth[
    "predecessor_decision_0130_checkpoint"
]

if pred["commit"] != EXPECTED_DECISION0130_COMMIT:
    fail(
        "PREDECESSOR_DECISION0130_COMMIT"
    )

if pred["parent_decision_0129_commit"] != EXPECTED_DECISION0129_COMMIT:
    fail(
        "PREDECESSOR_DECISION0129_COMMIT"
    )

failure = auth[
    "failed_pre_handoff_verifier"
]

if failure["sha256"] != EXPECTED_OLD_A02_SHA:
    fail(
        "FAILED_A02_SHA_BINDING"
    )

if failure["execution_result"] != "FAIL":
    fail(
        "FAILED_A02_RESULT"
    )

if failure["state"] != "PERMANENTLY_RETIRED":
    fail(
        "FAILED_A02_STATE"
    )

if failure["rerun_authorized"] is not False:
    fail(
        "FAILED_A02_RERUN_AUTHORIZED"
    )

if failure["patch_in_place_authorized"] is not False:
    fail(
        "FAILED_A02_PATCH_AUTHORIZED"
    )

if failure["must_never_be_rerun"] is not True:
    fail(
        "FAILED_A02_RETIREMENT"
    )

# ------------------------------------------------------------
# Verify failed A02 historical evidence byte-exactly
# ------------------------------------------------------------

if sha(OLD_A02) != EXPECTED_OLD_A02_SHA:
    fail(
        "OLD_A02_BYTE_IDENTITY"
    )

if sha(FAILED_OUTPUT) != EXPECTED_FAILED_OUTPUT_SHA:
    fail(
        "FAILED_OUTPUT_SHA"
    )

if sha(FAILED_SENTINEL) != EXPECTED_FAILED_SENTINEL_SHA:
    fail(
        "FAILED_SENTINEL_SHA"
    )

if (
    FAILED_OUTPUT.read_text(
        encoding="utf-8"
    ).strip()
    != "FAIL|DECISION0129_CHECKPOINT"
):
    fail(
        "FAILED_OUTPUT_CONTENT"
    )

sentinel = FAILED_SENTINEL.read_text(
    encoding="utf-8"
)

for marker in (
    "DECISION_0130_A02_EXECUTED=YES",
    "RETURN_CODE=1",
    "STATE=PERMANENTLY_RETIRED",
    "MUST_NEVER_BE_RERUN=YES",
):
    if marker not in sentinel:
        fail(
            "FAILED_SENTINEL_MARKER|"
            + marker
        )

# ------------------------------------------------------------
# Verify Review Package V1 remains valid
# ------------------------------------------------------------

p = subprocess.run(
    [
        "python3",
        str(PKG_SAFE),
    ],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    check=False,
)

if p.returncode != 0:
    fail(
        "REVIEW_PACKAGE_SAFE_VERIFIER|"
        + p.stdout
        + p.stderr
    )

if (
    "INDEPENDENT_HUMAN_REVIEW_PACKAGE_V1=PASS"
    not in p.stdout
):
    fail(
        "REVIEW_PACKAGE_PASS_MARKER"
    )

p = subprocess.run(
    [
        "sha256sum",
        "-c",
        PKG_SUMS.name,
    ],
    cwd=str(PKG),
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    check=False,
)

if p.returncode != 0:
    fail(
        "REVIEW_PACKAGE_CHECKSUM_CLOSURE|"
        + p.stdout
        + p.stderr
    )

# ------------------------------------------------------------
# Verify non-authorizations and retired-verifier constraints
# ------------------------------------------------------------

for key, value in auth[
    "explicit_non_authorizations"
].items():
    if value is not False:
        fail(
            "UNEXPECTED_AUTHORIZATION|"
            + key
        )

retired = auth[
    "retired_verifier_constraints"
]

for key, value in retired.items():
    if value is not False:
        fail(
            "RETIRED_VERIFIER_RERUN_ALLOWED|"
            + key
        )

scope = auth[
    "corrective_successor_scope"
]

if (
    scope[
        "new_verifier_must_require_current_head_parent_equals_decision_0130_commit"
    ]
    is not True
):
    fail(
        "CORRECTIVE_PARENT_BINDING_POLICY"
    )

if (
    scope[
        "new_verifier_must_not_require_current_head_equals_decision_0129_commit"
    ]
    is not True
):
    fail(
        "CORRECTIVE_DECISION0129_ANTI_BINDING_POLICY"
    )

if (
    scope[
        "new_verifier_must_not_execute_failed_a02"
    ]
    is not True
):
    fail(
        "OLD_A02_NONEXECUTION_POLICY"
    )

if (
    auth[
        "review_scope_preserved"
    ][
        "reviewer_decision_must_not_be_synthesized"
    ]
    is not True
):
    fail(
        "REVIEWER_DECISION_SYNTHESIS_POLICY"
    )

# ------------------------------------------------------------
# Verify this authorization checksum closure when present
# ------------------------------------------------------------

if SUMS.is_file():
    for line in SUMS.read_text(
        encoding="utf-8"
    ).splitlines():

        if not line.strip():
            continue

        digest, rel = line.split(
            None,
            1,
        )

        rel = rel.strip().lstrip("*")

        if sha(HERE / rel) != digest:
            fail(
                "CORRECTIVE_AUTH_CHECKSUM|"
                + rel
            )

print(
    "CORRECTIVE_EXTERNAL_HANDOFF_AUTHORING_AUTHORIZATION=PASS"
)

print(
    "CURRENT_CHECKPOINT_ROLE="
    "IMMEDIATE_SUCCESSOR_OF_DECISION0130"
)

print(
    "CURRENT_HEAD_PARENT_DECISION0130_BINDING=PASS"
)

print(
    "CURRENT_HEAD_EQUALS_DECISION0129=NO"
)

print(
    "OLD_DECISION0130_A02_EXECUTED_BY_THIS_VERIFIER=NO"
)

print(
    "OLD_DECISION0130_A02_STATE="
    "PERMANENTLY_RETIRED"
)

print(
    "OLD_DECISION0130_A02_RERUN_AUTHORIZED=NO"
)

print(
    "DECISION0128_A02_RERUN_AUTHORIZED=NO"
)

print(
    "DECISION0126_A02_RERUN_AUTHORIZED=NO"
)

print(
    "REVIEW_PACKAGE_V1_REMAINS_VALID=PASS"
)

print(
    "REVIEW_ITEMS="
    "RPR01|RPR02|RPR03|RPR04|RPR05|RPR06|RPR07|RPR08"
)

print(
    "REQUIRED_REVIEWER_ROLE="
    "Spec-Technical-Reviewer-1"
)

print(
    "HUMAN_REVIEW_PERFORMED=NO"
)

print(
    "REVIEWER_DECISION=NONE"
)

print(
    "STUDY_GOVERNANCE_ADOPTION_AUTHORIZED=NO"
)

print(
    "POSITIVE_MAPPING_WITNESS_AUTHORIZED=NO"
)

print(
    "NEGATIVE_MAPPING_IMPOSSIBILITY_PROOF_AUTHORIZED=NO"
)

print(
    "WHOLE_V4_EXHAUSTIVENESS_CLAIM_AUTHORIZED=NO"
)

print(
    "OPERATIONAL_MAPPING_AUTHORIZED=NO"
)

print(
    "ACTIVE_SCHEMA_V2_MODIFICATION_AUTHORIZED=NO"
)

print(
    "SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO"
)

print(
    "SCHEMA_V3_CREATED=NO"
)

print(
    "CURL_JSON_AUTHORIZED=NO"
)

print(
    "ANALYZER_AUTHORIZED=NO"
)

print(
    "BASELINE_AUTHORIZED=NO"
)

print(
    "REPAIR_AUTHORIZED=NO"
)

print(
    "VERIFIER_LIFECYCLE="
    "ONE_FINAL_RUN_IMMEDIATELY_BEFORE_CORRECTIVE_EXTERNAL_HANDOFF_AUTHORING_THEN_PERMANENT_RETIREMENT"
)
