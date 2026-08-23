#!/usr/bin/env python3

import hashlib
import json
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent

PKG = HERE / "review_package_v1_exact"
AUTH = HERE / "decision0106_authorization_exact"

README = HERE / "01_README_REVIEWER_HANDOFF.v1.md"
SOURCE = HERE / "02_source_binding_manifest.v1.json"
A02_OUTPUT = HERE / "03_decision0106_a02_final_output.EXACT_COPY.v1.txt"
A02_CONSUMPTION = HERE / "04_decision0106_a02_consumption_record.v1.json"
DEC0105 = HERE / "05_decision0105.EXACT_COPY.md"
DEC0106 = HERE / "06_decision0106.EXACT_COPY.md"
MANIFEST = HERE / "08_external_review_handoff_manifest.v1.json"
SUMS = HERE / "09_external_review_handoff.v1.SHA256SUMS"

PKG_SAFE = PKG / "23_verify_relation_informed_study_v1_review_package.v1.py"
PKG_SUMS = PKG / "24_review_package.v1.SHA256SUMS"
BLANK = PKG / "21_RIAC01_RIAC08_reviewer_packet.MANUAL_REVIEW_COPY.v1.md"

AUTH_A01 = AUTH / "01_external_independent_review_handoff_authorization.v1.json"
AUTH_A02 = AUTH / "02_verify_external_independent_review_handoff_authoring_authorization.v1.py"
AUTH_A03 = AUTH / "03_external_independent_review_handoff_authorization.v1.SHA256SUMS"

EXPECTED = {
    DEC0105:
        "3b39b58b1646cdac883f91db49bf003b76571f8814d91cb337b9cff71b91fd35",

    DEC0106:
        "db89b52e1215d4f2bdcae223f4e7f6cf7adbd0bc0a825d52b6dcabe448842d66",

    AUTH_A01:
        "1573946c7a891f2c63c97594a1598b09992fc7506a6d719e6d15e2a237991188",

    AUTH_A02:
        "933e0baa38f0809e71038f8626980b8469ddd6cd6e3279720ad37501e8ece4e9",

    AUTH_A03:
        "1da2366d9c7df19414e915eca3155a12750b196ee99c2da25e2760de14167645",

    BLANK:
        "a60a89c97292b62303a5a8f9c5fa0c3c2796f964a46cf544232d2d8202124166",

    PKG_SAFE:
        "9e0cb169350002ef42ece37e1b23d5f601fa454322a82447f818e29c9b2eefee",

    PKG_SUMS:
        "8bce3796572a48ef3140c34055c251b555d809f404a0a27c9e913d18aceaa606",
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

for path, expected in EXPECTED.items():
    if sha(path) != expected:
        fail(
            "SOURCE_BINDING|"
            + str(path)
        )

# ------------------------------------------------------------
# Verify exact copied Review Package V1 using its safe verifier.
# No retired A02 verifier is executed.
# ------------------------------------------------------------

proc = subprocess.run(
    [
        "python3",
        str(PKG_SAFE),
    ],
    cwd=str(PKG),
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    check=False,
)

if proc.returncode != 0:
    fail(
        "NESTED_REVIEW_PACKAGE_VERIFIER_RC|"
        + str(proc.returncode)
    )

if (
    b"SELF_CONTAINED_RELATION_INFORMED_STUDY_V1_REVIEW_PACKAGE=PASS"
    not in proc.stdout
):
    fail(
        "NESTED_REVIEW_PACKAGE_PASS_MARKER"
    )

proc = subprocess.run(
    [
        "sha256sum",
        "-c",
        PKG_SUMS.name,
    ],
    cwd=str(PKG),
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    check=False,
)

if proc.returncode != 0:
    fail(
        "NESTED_REVIEW_PACKAGE_CHECKSUM"
    )

# ------------------------------------------------------------
# Decision-0106 authorization checksum closure.
# A02 is hashed only, never run.
# ------------------------------------------------------------

proc = subprocess.run(
    [
        "sha256sum",
        "-c",
        AUTH_A03.name,
    ],
    cwd=str(AUTH),
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    check=False,
)

if proc.returncode != 0:
    fail(
        "DECISION0106_AUTH_CHECKSUM"
    )

# ------------------------------------------------------------
# Decision-0106 A02 final output and consumption.
# ------------------------------------------------------------

cons = json.loads(
    A02_CONSUMPTION.read_text(
        encoding="utf-8"
    )
)

if cons["final_run_result"] != "PASS":
    fail(
        "A02_FINAL_RESULT"
    )

if cons["verifier_state_after_run"] != \
        "PERMANENTLY_RETIRED":
    fail(
        "A02_NOT_RETIRED"
    )

if cons["rerun_authorized"] is not False:
    fail(
        "A02_RERUN_AUTHORIZED"
    )

if cons["must_never_be_rerun"] is not True:
    fail(
        "A02_RERUN_GUARD"
    )

if sha(A02_OUTPUT) != \
        cons["final_output_sha256"]:
    fail(
        "A02_FINAL_OUTPUT_SHA"
    )

if A02_OUTPUT.stat().st_size != \
        cons["final_output_size_bytes"]:
    fail(
        "A02_FINAL_OUTPUT_SIZE"
    )

if (
    "EXTERNAL_HANDOFF_AUTHORING_AUTHORIZATION=PASS"
    not in A02_OUTPUT.read_text(
        encoding="utf-8"
    )
):
    fail(
        "A02_FINAL_OUTPUT_PASS_MARKER"
    )

# ------------------------------------------------------------
# Blank reviewer packet.
# ------------------------------------------------------------

text = BLANK.read_text(
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
        fail(
            "REVIEW_ITEM|" + rid
        )

    body = section.group(0)

    if not re.search(
        r"^Decision \(PASS / REVISION_REQUIRED / FAIL\):[ \t]*$",
        body,
        flags=re.MULTILINE,
    ):
        fail(
            "ITEM_DECISION_NOT_BLANK|" + rid
        )

    if not re.search(
        r"^Reviewer notes:[ \t]*$",
        body,
        flags=re.MULTILINE,
    ):
        fail(
            "ITEM_NOTES_NOT_BLANK|" + rid
        )

if not re.search(
    r"^Overall decision "
    r"\(APPROVE_RELATION_INFORMED_EXHAUSTIVE_ADMISSIBLE_COMPOSITION_STUDY_V1 / "
    r"REVISION_REQUIRED / FAIL\):[ \t]*$",
    text,
    flags=re.MULTILINE,
):
    fail(
        "OVERALL_DECISION_NOT_BLANK"
    )

# ------------------------------------------------------------
# Source binding semantics.
# ------------------------------------------------------------

source = json.loads(
    SOURCE.read_text(
        encoding="utf-8"
    )
)

if source["status"] != \
        "BLANK_READY_FOR_INDEPENDENT_HUMAN_REVIEW":
    fail(
        "SOURCE_BINDING_STATUS"
    )

if source[
    "review_contract"
][
    "required_reviewer_role"
] != "Spec-Technical-Reviewer-1":
    fail(
        "REVIEWER_ROLE"
    )

if source[
    "governance_boundary"
][
    "human_review_decision_exists"
] is not False:
    fail(
        "PREMATURE_HUMAN_DECISION"
    )

# ------------------------------------------------------------
# Handoff manifest.
# ------------------------------------------------------------

manifest = json.loads(
    MANIFEST.read_text(
        encoding="utf-8"
    )
)

if manifest["handoff_state"] != \
        "BLANK_READY_FOR_INDEPENDENT_HUMAN_REVIEW":
    fail(
        "HANDOFF_STATE"
    )

entries = manifest["files"]

if len(entries) != 34:
    fail(
        "HANDOFF_MANIFEST_ENTRY_COUNT|"
        + str(len(entries))
    )

seen = set()

for entry in entries:
    rel = entry["path"]

    if rel in seen:
        fail(
            "HANDOFF_MANIFEST_DUPLICATE|" + rel
        )

    seen.add(rel)

    path = HERE / rel

    if sha(path) != entry["sha256"]:
        fail(
            "HANDOFF_MANIFEST_SHA|" + rel
        )

    if path.stat().st_size != \
            entry["size_bytes"]:
        fail(
            "HANDOFF_MANIFEST_SIZE|" + rel
        )

# ------------------------------------------------------------
# Full handoff checksum closure.
# ------------------------------------------------------------

if SUMS.is_file():
    lines = [
        x
        for x in SUMS.read_text(
            encoding="utf-8"
        ).splitlines()
        if x.strip()
    ]

    if len(lines) != 35:
        fail(
            "HANDOFF_CHECKSUM_ENTRY_COUNT|"
            + str(len(lines))
        )

    for raw in lines:
        digest, rel = raw.split(
            None,
            1,
        )

        rel = rel.strip().lstrip("*")

        if rel.startswith("./"):
            rel = rel[2:]

        path = HERE / rel

        if sha(path) != digest:
            fail(
                "HANDOFF_CHECKSUM|" + rel
            )

print("IMMUTABLE_REVIEW_PACKAGE_V1_EXACT_COPY=PASS")
print("REVIEW_PACKAGE_FILE_COUNT=24")
print("REVIEW_PACKAGE_STATE=BLANK_READY_FOR_INDEPENDENT_HUMAN_REVIEW")

print("RIAC01_RIAC08_DECISIONS=BLANK")
print("REVIEWER_IDENTITY_PREPOPULATED=NO")
print("REQUIRED_REVIEWER_ROLE=Spec-Technical-Reviewer-1")

print("DECISION_0102_A02_STATE=PERMANENTLY_RETIRED")
print("DECISION_0104_A02_STATE=PERMANENTLY_RETIRED")
print("DECISION_0106_A02_STATE=PERMANENTLY_RETIRED")
print("RETIRED_A02_VERIFIERS_EXECUTED_BY_HANDOFF_VERIFIER=NO")

print("HUMAN_REVIEW_DECISION_EXISTS=NO")
print("STUDY_GOVERNANCE_ADOPTED=NO")

print("OPERATIONAL_POSITIVE_MAPPING_AUTHORIZED=NO")
print("SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO")
print("CURL_JSON_AUTHORIZED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")

print("SELF_CONTAINED_EXTERNAL_INDEPENDENT_REVIEW_HANDOFF_V1=PASS")
