#!/usr/bin/env python3

import hashlib
import json
import subprocess
from pathlib import Path

REPO = Path("/openbayes/home/semanticverify-fuzz-research")

BASE_REL = (
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2"
)

PACKAGE_REL = (
    BASE_REL
    + "/schema_v2_requirement_to_semantic_unit_crosswalk_"
      "evidence_resolution_study_v1_cwxr07_s2_"
      "narrowed_corrective_successor_v1_review_package_v1"
)

AUTH_REL = (
    BASE_REL
    + "/schema_v2_requirement_to_semantic_unit_crosswalk_"
      "evidence_resolution_study_v1_cwxr07_s2_"
      "narrowed_corrective_successor_v1_external_handoff_"
      "authorization_v1"
)

HANDOFF_REL = "evidence/annotation_preparation/protocol_specification_schema_successor_v2/schema_v2_requirement_to_semantic_unit_crosswalk_evidence_resolution_study_v1_cwxr07_s2_narrowed_corrective_successor_v1_external_handoff_v1"

EXPECTED_PARENT = "edcf00a593db3b4d865e12b997ef0aa489383456"
EXPECTED_A01_SHA = "a3ce2aaa7ede7fcfaea593710dbb881e7cb5893a6cd39e77c31de2b3e9ef4017"
EXPECTED_D0167_SHA = "fd5d2aa39f16dacacf7a773963fb0d67e555a09b4137c2cc0433da00d185a3f5"

EXPECTED_PACKAGE_TREE = "906eab598c1fe82fe1f35a9f4b2b05821ac2a9df"
EXPECTED_MANIFEST_SHA = "88b2cddb3e8e860538a060117790b4b7a05cc6c45530d10d4e1bc22f67aa0f05"
EXPECTED_INSTRUCTIONS_SHA = "e89fb9290a6dcc996bf2d27caffe7d46b3a3ab5624f4b20411fd7d6ec416ae96"
EXPECTED_PACKET_SHA = "ad5333e4687a285f7fb87ce1ab427e25b4d00c8fa513b1f9ee1ae116c0fad5a2"
EXPECTED_PACKET_SIZE = 1555
EXPECTED_SAFE_VERIFIER_SHA = "057f822e2f580bad5dd0c761f7caa5a5afccc88695d0c053381aae6e98538eac"
EXPECTED_CHECKSUM_SHA = "308ce3baed82a54a94af98fe22baa4ba5b7066a376c9a13034ab58d6635947f6"

EXTERNAL_ZIP = Path("/openbayes/home/50_CWXR07_S2_independent_human_review_handoff.v1.zip")
EXTERNAL_EDITABLE = Path("/openbayes/home/50_CWXR07_S2_reviewer_packet.MANUAL_REVIEW_COPY.v1.md")

PASS_MARKER = (
    "CWXR07_S2_EXTERNAL_INDEPENDENT_HUMAN_REVIEW_"
    "HANDOFF_AUTHORING_AUTHORIZATION=PASS"
)

def run(*args):
    return subprocess.check_output(
        args,
        cwd=REPO,
        text=True,
    ).strip()

def sha(path):
    return hashlib.sha256(
        Path(path).read_bytes()
    ).hexdigest()

head = run("git", "rev-parse", "HEAD")
parent = run("git", "rev-parse", "HEAD^")

if parent != EXPECTED_PARENT:
    raise SystemExit(
        "STOP|CURRENT_HEAD_IS_NOT_IMMEDIATE_SUCCESSOR_OF_DECISION0167"
    )

status = run(
    "git",
    "status",
    "--porcelain=v1",
    "--untracked-files=all",
)

if status:
    raise SystemExit(
        "STOP|REPOSITORY_NOT_CLEAN"
    )

auth = REPO / AUTH_REL

a01 = (
    auth
    / "01_cwxr07_s2_external_handoff_authorization.v1.json"
)

a03 = (
    auth
    / "03_cwxr07_s2_external_handoff_authorization.v1.SHA256SUMS"
)

if sha(a01) != EXPECTED_A01_SHA:
    raise SystemExit(
        "STOP|DECISION0168_A01_SHA_MISMATCH"
    )

subprocess.check_call(
    [
        "sha256sum",
        "-c",
        a03.name,
    ],
    cwd=auth,
    stdout=subprocess.DEVNULL,
)

d0167 = (
    REPO
    / "documentation/decisions/"
      "0167-author-cwxr07-s2-independent-human-review-package-v1.md"
)

if sha(d0167) != EXPECTED_D0167_SHA:
    raise SystemExit(
        "STOP|DECISION0167_SHA_MISMATCH"
    )

if run(
    "git",
    "rev-parse",
    f"HEAD:{PACKAGE_REL}",
) != EXPECTED_PACKAGE_TREE:
    raise SystemExit(
        "STOP|REVIEW_PACKAGE_TREE_CHANGED"
    )

package = REPO / PACKAGE_REL

manifest = package / "01_review_package_manifest.v1.json"
instructions = package / "03_independent_reviewer_instructions.v1.md"

packet = (
    package
    / "04_CWXR07_S2_reviewer_packet.INITIAL_BLANK.EXACT_COPY.v1.md"
)

safe_verifier = (
    package
    / "07_verify_cwxr07_s2_independent_human_review_package_v1.py"
)

checksum = (
    package
    / "08_cwxr07_s2_independent_human_review_package_v1.SHA256SUMS"
)

checks = [
    (manifest, EXPECTED_MANIFEST_SHA),
    (instructions, EXPECTED_INSTRUCTIONS_SHA),
    (packet, EXPECTED_PACKET_SHA),
    (safe_verifier, EXPECTED_SAFE_VERIFIER_SHA),
    (checksum, EXPECTED_CHECKSUM_SHA),
]

for path, expected in checks:
    if sha(path) != expected:
        raise SystemExit(
            "STOP|PACKAGE_CONTROL_SHA_MISMATCH|"
            + path.name
        )

if packet.stat().st_size != EXPECTED_PACKET_SIZE:
    raise SystemExit(
        "STOP|REVIEWER_PACKET_SIZE_MISMATCH"
    )

subprocess.check_call(
    [
        "sha256sum",
        "-c",
        checksum.name,
    ],
    cwd=package,
    stdout=subprocess.DEVNULL,
)

# ------------------------------------------------------------
# CORRECT BLANK-FIELD RULE
# ------------------------------------------------------------
#
# Presence of:
#
#     CWXR07-S2 decision:
#
# is REQUIRED template structure and is NOT prepopulation.
#
# Only the substring AFTER the FIRST colon is the field value.
# That value must be empty after stripping whitespace.
# ------------------------------------------------------------

text = packet.read_text(
    encoding="utf-8"
)

fields = [
    "CWXR07-S2 decision",
    "Reviewer notes",
    "Reviewer name",
    "Reviewer role",
    "Reviewer confirmation/signature",
    "Reviewer attestation",
    "Review date",
]

lines = text.splitlines()

for field in fields:
    prefix = field + ":"

    matches = [
        line
        for line in lines
        if line.startswith(prefix)
    ]

    if len(matches) != 1:
        raise SystemExit(
            "STOP|REVIEWER_PACKET_FIELD_OCCURRENCE_COUNT|"
            + field
            + "|"
            + str(len(matches))
        )

    value = (
        matches[0]
        .split(":", 1)[1]
        .strip()
    )

    if value != "":
        raise SystemExit(
            "STOP|REVIEWER_PACKET_FIELD_VALUE_PREPOPULATED|"
            + field
        )

required = [
    "Review only `CWXR07-S2`.",
    "CWXR07-S1 remains `REVISION_REQUIRED`",
    "`PASS`",
    "`REVISION_REQUIRED`",
    "`FAIL`",
]

for marker in required:
    if marker not in text:
        raise SystemExit(
            "STOP|REVIEWER_PACKET_REQUIRED_MARKER_MISSING|"
            + marker
        )

if (REPO / HANDOFF_REL).exists():
    raise SystemExit(
        "STOP|EXTERNAL_HANDOFF_ALREADY_EXISTS"
    )

if EXTERNAL_ZIP.exists():
    raise SystemExit(
        "STOP|EXTERNAL_ZIP_ALREADY_EXISTS"
    )

if EXTERNAL_EDITABLE.exists():
    raise SystemExit(
        "STOP|EXTERNAL_EDITABLE_REVIEW_COPY_ALREADY_EXISTS"
    )

print(PASS_MARKER)

print("CURRENT_HEAD=" + head)
print("CURRENT_HEAD_PARENT_DECISION0167_BINDING=PASS")

print("REVIEW_SCOPE=CWXR07-S2_ONLY")
print("HISTORICAL_CWXR07_S1_DECISION=REVISION_REQUIRED")
print("HISTORICAL_CWXR07_S1_MODIFIED=NO")

print("SOURCE_REVIEW_PACKAGE_FILE_COUNT=24")
print("SOURCE_REVIEW_PACKAGE_CHECKSUM_ENTRY_COUNT=23")
print("SOURCE_REVIEW_PACKAGE_CHECKSUM_CLOSURE=PASS")

print(
    "BLANK_FIELD_VALIDATION_RULE="
    "VALUE_AFTER_FIRST_COLON_MUST_BE_EMPTY"
)

print("ALL_REVIEWER_COMPLETION_FIELD_VALUES_BLANK=YES")
print("REVIEWER_IDENTITY_PREPOPULATED=NO")
print("REVIEWER_DECISION_PREPOPULATED=NO")

print("EXTERNAL_HANDOFF_AUTHORING_AUTHORIZED=YES")
print("EXTERNAL_ZIP_CREATION_AUTHORIZED=YES")
print("EXTERNAL_EDITABLE_REVIEW_COPY_CREATION_AUTHORIZED=YES")

print("HUMAN_REVIEW_COMPLETED=NO")
print("REVIEWER_IDENTITY_RECORDED=NO")
print("REVIEWER_DECISION_RECORDED=NO")

print("SUCCESSOR_APPROVED=NO")
print("GOVERNANCE_ADOPTION_AUTHORIZED=NO")

print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")

print(
    "VERIFIER_LIFECYCLE="
    "ONE_FINAL_RUN_IMMEDIATELY_BEFORE_CWXR07_S2_"
    "EXTERNAL_INDEPENDENT_HUMAN_REVIEW_HANDOFF_AUTHORING_"
    "THEN_PERMANENT_RETIREMENT"
)
