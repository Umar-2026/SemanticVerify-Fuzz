#!/usr/bin/env python3

import hashlib
import json
import re
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
    + "/schema_v2_relation_informed_exhaustive_"
      "admissible_composition_study_v1_review_package_v1"
)

PKG = REPO / PKG_REL

HANDOFF = (
    REPO
    / BASE_REL
    / "schema_v2_relation_informed_exhaustive_"
      "admissible_composition_study_v1_external_review_handoff_v1"
)

AUTH = (
    HERE
    / "01_external_independent_review_handoff_authorization.v1.json"
)

P21 = (
    PKG
    / "21_RIAC01_RIAC08_reviewer_packet.MANUAL_REVIEW_COPY.v1.md"
)

P22 = (
    PKG
    / "22_review_package_manifest.v1.json"
)

P23 = (
    PKG
    / "23_verify_relation_informed_study_v1_review_package.v1.py"
)

P24 = (
    PKG
    / "24_review_package.v1.SHA256SUMS"
)

D104_CONSUMPTION = (
    PKG
    / "19_decision0104_a02_consumption_record.v1.json"
)

EXPECTED = {
    P21:
        "a60a89c97292b62303a5a8f9c5fa0c3c2796f964a46cf544232d2d8202124166",

    P22:
        "d2dcaf72e2ebacd79efe1305672065632e11108621910b57ba319b4a9ceed9ae",

    P23:
        "9e0cb169350002ef42ece37e1b23d5f601fa454322a82447f818e29c9b2eefee",

    P24:
        "8bce3796572a48ef3140c34055c251b555d809f404a0a27c9e913d18aceaa606",

    D104_CONSUMPTION:
        "48ea6f98077553df95fbfa36f0e6483a4e5984bbe48a46c3e3328bc5063203bf",
}

def fail(msg):
    print("FAIL|" + msg)
    raise SystemExit(1)

def sha(path):
    if not path.is_file():
        fail("MISSING|" + str(path))

    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()

# Repository must be clean immediately before handoff.
proc = subprocess.run(
    [
        "git",
        "-C",
        str(REPO),
        "status",
        "--porcelain=v1",
        "--untracked-files=all",
    ],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    check=False,
)

if proc.returncode != 0:
    fail("GIT_STATUS")

if proc.stdout.strip():
    fail("REPOSITORY_NOT_CLEAN")

if HANDOFF.exists():
    fail("HANDOFF_ALREADY_EXISTS")

# Immutable package tree.
proc = subprocess.run(
    [
        "git",
        "-C",
        str(REPO),
        "rev-parse",
        "HEAD:" + PKG_REL,
    ],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    check=False,
)

if proc.returncode != 0:
    fail("PACKAGE_GIT_TREE_LOOKUP")

if proc.stdout.strip() != \
        "a43856c2b63941eaf379b4157669bc8590d585d1":
    fail("PACKAGE_GIT_TREE_CHANGED")

for path, expected in EXPECTED.items():
    if sha(path) != expected:
        fail("PACKAGE_BINDING|" + str(path))

# Run only safe package verifier.
proc = subprocess.run(
    [
        "python3",
        str(P23),
    ],
    cwd=str(PKG),
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    check=False,
)

if proc.returncode != 0:
    fail(
        "PACKAGE_SAFE_VERIFIER_RC|"
        + str(proc.returncode)
    )

if (
    b"SELF_CONTAINED_RELATION_INFORMED_STUDY_V1_REVIEW_PACKAGE=PASS"
    not in proc.stdout
):
    fail("PACKAGE_SAFE_VERIFIER_PASS_MARKER")

# Blank reviewer packet remains blank.
text = P21.read_text(
    encoding="utf-8"
)

for rid in (
    "RIAC01",
    "RIAC02",
    "RIAC03",
    "RIAC04",
    "RIAC05",
    "RIAC06",
    "RIAC07",
    "RIAC08",
):
    section = re.search(
        rf"^## {rid} — .*?"
        rf"(?=^## RIAC\d{{2}} —|^# Overall review decision)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )

    if not section:
        fail("REVIEW_ITEM|" + rid)

    if not re.search(
        r"^Decision \(PASS / REVISION_REQUIRED / FAIL\):[ \t]*$",
        section.group(0),
        flags=re.MULTILINE,
    ):
        fail("ITEM_DECISION_NOT_BLANK|" + rid)

if not re.search(
    r"^Overall decision "
    r"\(APPROVE_RELATION_INFORMED_EXHAUSTIVE_ADMISSIBLE_COMPOSITION_STUDY_V1 / "
    r"REVISION_REQUIRED / FAIL\):[ \t]*$",
    text,
    flags=re.MULTILINE,
):
    fail("OVERALL_DECISION_NOT_BLANK")

# Decision-0104 A02 retirement.
cons = json.loads(
    D104_CONSUMPTION.read_text(
        encoding="utf-8"
    )
)

if cons["verifier_state_after_run"] != \
        "PERMANENTLY_RETIRED":
    fail("DECISION0104_A02_NOT_RETIRED")

if cons["must_never_be_rerun"] is not True:
    fail("DECISION0104_A02_RERUN_GUARD")

# New authorization semantics.
auth = json.loads(
    AUTH.read_text(
        encoding="utf-8"
    )
)

if auth["status"] != \
        "AUTHORIZED_FOR_EXTERNAL_HANDOFF_AUTHORING_ONLY":
    fail("AUTH_STATUS")

if auth[
    "review_contract"
][
    "required_reviewer_role"
] != "Spec-Technical-Reviewer-1":
    fail("REVIEWER_ROLE")

if auth[
    "review_contract"
][
    "review_items"
] != [
    "RIAC01",
    "RIAC02",
    "RIAC03",
    "RIAC04",
    "RIAC05",
    "RIAC06",
    "RIAC07",
    "RIAC08",
]:
    fail("REVIEW_ITEM_SET")

for key, value in auth[
    "explicit_non_authorizations"
].items():
    if value is not False:
        fail(
            "UNEXPECTED_AUTHORIZATION|" + key
        )

for key, value in auth[
    "authorization_verifier_lifecycle"
].items():
    if value is not True:
        fail(
            "VERIFIER_LIFECYCLE|" + key
        )

print("DECISION_0105_REVIEW_PACKAGE_BINDING=PASS")
print("REVIEW_PACKAGE_FILE_COUNT=24")
print("REVIEW_PACKAGE_STATE=BLANK_READY_FOR_INDEPENDENT_HUMAN_REVIEW")
print("RIAC01_RIAC08_DECISIONS=BLANK")
print("REVIEWER_IDENTITY_PREPOPULATED=NO")
print("REQUIRED_REVIEWER_ROLE=Spec-Technical-Reviewer-1")

print("DECISION_0102_A02_STATE=PERMANENTLY_RETIRED")
print("DECISION_0104_A02_STATE=PERMANENTLY_RETIRED")
print("RETIRED_VERIFIERS_EXECUTED=NO")

print("EXTERNAL_HANDOFF_AUTHORING_AUTHORIZATION=PASS")
print("AUTHORIZED_SCOPE=HANDOFF_AUTHORING_ONLY")

print("STUDY_GOVERNANCE_ADOPTED=NO")
print("OPERATIONAL_POSITIVE_MAPPING_AUTHORIZED=NO")
print("SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO")
print("CURL_JSON_AUTHORIZED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")

print("VERIFIER_LIFECYCLE=ONE_FINAL_RUN_IMMEDIATELY_BEFORE_HANDOFF_AUTHORING_THEN_PERMANENT_RETIREMENT")
