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

S2_REL = (
    BASE_REL
    + "/schema_v2_requirement_to_semantic_unit_crosswalk_"
      "evidence_resolution_study_v1_cwxr07_s2_"
      "narrowed_corrective_successor_v1"
)

AUTH_REL = (
    BASE_REL
    + "/schema_v2_requirement_to_semantic_unit_crosswalk_"
      "evidence_resolution_study_v1_cwxr07_s2_"
      "narrowed_corrective_successor_v1_review_package_"
      "authorization_v1"
)

PACKAGE_REL = (
    BASE_REL
    + "/schema_v2_requirement_to_semantic_unit_crosswalk_"
      "evidence_resolution_study_v1_cwxr07_s2_"
      "narrowed_corrective_successor_v1_review_package_v1"
)

EXPECTED_PARENT = "ca659ec08f2a4d66dfbf315a4bc952dc7bf7c4f4"
EXPECTED_A01_SHA = "64844aa360094bbe8583004eef5eb6000ae5bdfd65619b108b5e658852c6f0ce"
EXPECTED_D0165_SHA = "758110ce920d8049b64406684bd551b059a3d4b5cac4f382a783eb3ab2f20efc"

EXPECTED_S2_TREE = "e3e8b53823c6c1e132eba5c56a97f726a801f753"
EXPECTED_MANIFEST_SHA = "c18a6c8e60b00dc9b67e96a454ba032dc5d8d99d86092f1819b2c9303487f725"
EXPECTED_CRITERION_SHA = "83e204708b4e4b660dcea638fcbb30d886f68ca5fbd398156c2d388702ef10c2"
EXPECTED_PACKET_SHA = "ad5333e4687a285f7fb87ce1ab427e25b4d00c8fa513b1f9ee1ae116c0fad5a2"
EXPECTED_SAFE_VERIFIER_SHA = "9c626b9409e563bae1a283f3819d1fcef2584d2f6608444812a78acd0791a698"
EXPECTED_CHECKSUM_SHA = "d7c7b4b7e9adccc64fd6fc89f6d3afe16ca479337e24ef257fda6dc456462baf"

PASS_MARKER = (
    "CWXR07_S2_INDEPENDENT_HUMAN_REVIEW_"
    "PACKAGE_AUTHORING_AUTHORIZATION=PASS"
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
        "STOP|CURRENT_HEAD_IS_NOT_IMMEDIATE_SUCCESSOR_OF_DECISION0165"
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
    / "01_cwxr07_s2_independent_human_review_package_authorization.v1.json"
)

a03 = (
    auth
    / "03_cwxr07_s2_independent_human_review_package_authorization.v1.SHA256SUMS"
)

if sha(a01) != EXPECTED_A01_SHA:
    raise SystemExit(
        "STOP|DECISION0166_A01_SHA_MISMATCH"
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

d0165 = (
    REPO
    / "documentation/decisions/"
      "0165-author-cwxr07-s2-narrowed-corrective-successor-v1.md"
)

if sha(d0165) != EXPECTED_D0165_SHA:
    raise SystemExit(
        "STOP|DECISION0165_SHA_MISMATCH"
    )

if run(
    "git",
    "rev-parse",
    f"HEAD:{S2_REL}",
) != EXPECTED_S2_TREE:
    raise SystemExit(
        "STOP|CWXR07_S2_SUCCESSOR_TREE_CHANGED"
    )

s2 = REPO / S2_REL

manifest = (
    s2
    / "01_cwxr07_s2_narrowed_corrective_successor_manifest.v1.json"
)

criterion = (
    s2
    / "05_cwxr07_s2_narrowed_criterion.v1.md"
)

packet = (
    s2
    / "06_CWXR07_S2_reviewer_packet.INITIAL_BLANK.v1.md"
)

safe_verifier = (
    s2
    / "09_verify_cwxr07_s2_narrowed_corrective_successor_v1.py"
)

checksum = (
    s2
    / "10_cwxr07_s2_narrowed_corrective_successor_v1.SHA256SUMS"
)

checks = [
    (manifest, EXPECTED_MANIFEST_SHA),
    (criterion, EXPECTED_CRITERION_SHA),
    (packet, EXPECTED_PACKET_SHA),
    (safe_verifier, EXPECTED_SAFE_VERIFIER_SHA),
    (checksum, EXPECTED_CHECKSUM_SHA),
]

for path, expected in checks:
    if sha(path) != expected:
        raise SystemExit(
            "STOP|CWXR07_S2_SOURCE_SHA_MISMATCH|"
            + path.name
        )

subprocess.check_call(
    [
        "sha256sum",
        "-c",
        checksum.name,
    ],
    cwd=s2,
    stdout=subprocess.DEVNULL,
)

obj = json.loads(
    manifest.read_text(
        encoding="utf-8"
    )
)

if obj["criterion_id"] != "CWXR07-S2":
    raise SystemExit(
        "STOP|UNEXPECTED_SUCCESSOR_CRITERION"
    )

if (
    obj["status"]
    != "AUTHOR_CANDIDATE_AWAITING_INDEPENDENT_HUMAN_REVIEW"
):
    raise SystemExit(
        "STOP|UNEXPECTED_SUCCESSOR_STATUS"
    )

if (
    obj["historical_s1_boundary"]["cwxr07_s1_decision"]
    != "REVISION_REQUIRED"
):
    raise SystemExit(
        "STOP|HISTORICAL_S1_DECISION_CHANGED"
    )

human = obj["human_review"]

if human["human_review_completed"] is not False:
    raise SystemExit(
        "STOP|S2_HUMAN_REVIEW_ALREADY_COMPLETED"
    )

if human["reviewer_identity_recorded"] is not False:
    raise SystemExit(
        "STOP|S2_REVIEWER_IDENTITY_ALREADY_RECORDED"
    )

if human["reviewer_decision_recorded"] is not False:
    raise SystemExit(
        "STOP|S2_REVIEWER_DECISION_ALREADY_RECORDED"
    )

future = REPO / PACKAGE_REL

if future.exists():
    raise SystemExit(
        "STOP|S2_REVIEW_PACKAGE_ALREADY_EXISTS"
    )

print(PASS_MARKER)

print("CURRENT_HEAD=" + head)
print("CURRENT_HEAD_PARENT_DECISION0165_BINDING=PASS")

print("REVIEW_SCOPE=CWXR07-S2_ONLY")
print("HISTORICAL_CWXR07_S1_DECISION=REVISION_REQUIRED")
print("HISTORICAL_CWXR07_S1_MODIFIED=NO")

print("SOURCE_SUCCESSOR_FILE_COUNT=17")
print("SOURCE_SUCCESSOR_CHECKSUM_CLOSURE=PASS")

print("INDEPENDENT_HUMAN_REVIEW_REQUIRED=YES")
print("HUMAN_REVIEW_COMPLETED=NO")

print("REVIEWER_IDENTITY_RECORDED=NO")
print("REVIEWER_DECISION_RECORDED=NO")
print("REVIEWER_IDENTITY_SYNTHESIZED=NO")
print("REVIEWER_DECISION_SYNTHESIZED=NO")

print("EXTERNAL_HANDOFF_AUTHORIZED=NO")
print("EXTERNAL_ZIP_AUTHORIZED=NO")

print("SUCCESSOR_APPROVED=NO")
print("GOVERNANCE_ADOPTION_AUTHORIZED=NO")

print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")

print(
    "VERIFIER_LIFECYCLE="
    "ONE_FINAL_RUN_IMMEDIATELY_BEFORE_CWXR07_S2_"
    "INDEPENDENT_HUMAN_REVIEW_PACKAGE_AUTHORING_"
    "THEN_PERMANENT_RETIREMENT"
)
