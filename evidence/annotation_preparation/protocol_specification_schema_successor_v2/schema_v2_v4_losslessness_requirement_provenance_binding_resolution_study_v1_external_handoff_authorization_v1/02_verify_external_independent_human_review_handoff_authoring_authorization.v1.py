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

PKG = REPO / PKG_REL

AUTH = (
    HERE
    / "01_external_independent_human_review_handoff_authorization.v1.json"
)

SUMS = (
    HERE
    / "03_external_independent_human_review_handoff_authorization.v1.SHA256SUMS"
)

PKG_SAFE = (
    PKG
    / "09_verify_independent_review_package_v1.py"
)

PKG_SUMS = (
    PKG
    / "10_review_package_v1.SHA256SUMS"
)

BUNDLE = (
    PKG
    / "06_repository_checkpoint.bundle"
)

BUNDLE_MANIFEST = (
    PKG
    / "07_repository_checkpoint_bundle_manifest.v1.json"
)

EXPECTED_PKG_TREE = (
    "35794b450ed9bcde337f4ea4b7de35dd8218cc03"
)

EXPECTED_DEC0129_HEAD = (
    "7ddaaa2e24a065053c132700292023dfaca9c428"
)

EXPECTED_BUNDLE_CHECKPOINT = (
    "7f13e5569c5d25c9c104a9b1dd68516471b6017a"
)

EXPECTED_BUNDLE_SHA = (
    "ab2aed74d6b082137d8560bd21578323"
    "faf5a543f335ccea45dfc361454ebacf"
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
        "HEAD",
    )
    != EXPECTED_DEC0129_HEAD
):
    fail(
        "DECISION0129_CHECKPOINT"
    )

if git(
    "status",
    "--porcelain=v1",
    "--untracked-files=all",
):
    fail(
        "REPOSITORY_NOT_CLEAN"
    )

auth = json.loads(
    AUTH.read_text(
        encoding="utf-8"
    )
)

if (
    auth["status"]
    != "AUTHORIZED_NOT_YET_AUTHORED"
):
    fail(
        "AUTHORIZATION_STATUS"
    )

if (
    auth["authorization_type"]
    != "PRE_EXTERNAL_INDEPENDENT_HUMAN_REVIEW_HANDOFF_AUTHORING_ONLY"
):
    fail(
        "AUTHORIZATION_TYPE"
    )

bundle_auth = auth[
    "sealed_repository_checkpoint_bundle"
]

if (
    bundle_auth["checkpoint_commit"]
    != EXPECTED_BUNDLE_CHECKPOINT
):
    fail(
        "AUTHORIZED_BUNDLE_CHECKPOINT"
    )

if (
    bundle_auth["checkpoint_role"]
    != "DECISION_0128_PRE_REVIEW_PACKAGE_CHECKPOINT"
):
    fail(
        "BUNDLE_CHECKPOINT_ROLE"
    )

if (
    bundle_auth[
        "intentionally_distinct_from_decision_0129_checkpoint"
    ]
    is not True
):
    fail(
        "BUNDLE_CHECKPOINT_DISTINCTION"
    )

if (
    bundle_auth["bundle_sha256"]
    != EXPECTED_BUNDLE_SHA
):
    fail(
        "AUTHORIZED_BUNDLE_SHA"
    )

bundle_manifest = json.loads(
    BUNDLE_MANIFEST.read_text(
        encoding="utf-8"
    )
)

if (
    bundle_manifest["checkpoint_commit"]
    != EXPECTED_BUNDLE_CHECKPOINT
):
    fail(
        "BUNDLE_MANIFEST_CHECKPOINT"
    )

if (
    bundle_manifest["bundle_sha256"]
    != EXPECTED_BUNDLE_SHA
):
    fail(
        "BUNDLE_MANIFEST_SHA_BINDING"
    )

if sha(BUNDLE) != EXPECTED_BUNDLE_SHA:
    fail(
        "BUNDLE_FILE_SHA"
    )

p = subprocess.run(
    [
        "git",
        "-C",
        str(REPO),
        "bundle",
        "verify",
        str(BUNDLE),
    ],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    check=False,
)

if p.returncode != 0:
    fail(
        "BUNDLE_VERIFY|"
        + p.stdout
        + p.stderr
    )

bound = auth[
    "bound_review_package"
]

if bound[
    "review_item_count"
] != 8:
    fail(
        "REVIEW_ITEM_COUNT"
    )

if bound["review_items"] != [
    "RPR01",
    "RPR02",
    "RPR03",
    "RPR04",
    "RPR05",
    "RPR06",
    "RPR07",
    "RPR08",
]:
    fail(
        "REVIEW_ITEMS"
    )

if (
    bound["required_reviewer_role"]
    != "Spec-Technical-Reviewer-1"
):
    fail(
        "REVIEWER_ROLE"
    )

if (
    bound["reviewer_decision_present"]
    is not False
):
    fail(
        "REVIEWER_DECISION_PRESENT"
    )

if (
    bound["human_review_performed"]
    is not False
):
    fail(
        "HUMAN_REVIEW_ALREADY_PERFORMED"
    )

req = auth[
    "external_handoff_requirements"
]

required_true = (
    "handoff_zip_required",
    "zip_must_include_exact_review_package_v1",
    "zip_must_include_sealed_repository_checkpoint_bundle",
    "zip_must_include_portable_source_evidence",
    "zip_must_include_blank_rpr01_rpr08_reviewer_packet",
    "zip_must_include_safe_review_package_verifier",
    "zip_must_include_checksum_closure",
    "editable_manual_reviewer_packet_copy_required",
    "editable_manual_copy_must_start_byte_exactly_from_blank_packet",
    "author_must_not_prefill_reviewer_decisions",
    "author_must_not_synthesize_reviewer_identity",
    "author_must_not_synthesize_reviewer_notes",
    "author_must_not_synthesize_overall_decision",
    "external_reviewer_must_return_completed_packet",
)

for key in required_true:
    if req[key] is not True:
        fail(
            "HANDOFF_REQUIREMENT|"
            + key
        )

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

if (
    retired[
        "decision_0128_a02_rerun"
    ]
    is not False
):
    fail(
        "DECISION0128_A02_RERUN"
    )

if (
    retired[
        "decision_0126_a02_rerun"
    ]
    is not False
):
    fail(
        "DECISION0126_A02_RERUN"
    )

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
        "PACKAGE_SAFE_VERIFIER|"
        + p.stdout
        + p.stderr
    )

if (
    "INDEPENDENT_HUMAN_REVIEW_PACKAGE_V1=PASS"
    not in p.stdout
):
    fail(
        "PACKAGE_SAFE_PASS_MARKER"
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
        "PACKAGE_CHECKSUM_CLOSURE|"
        + p.stdout
        + p.stderr
    )

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

        if (
            sha(HERE / rel)
            != digest
        ):
            fail(
                "AUTH_CHECKSUM|"
                + rel
            )

print(
    "DECISION_0129_REVIEW_PACKAGE_BINDING=PASS"
)

print(
    "SEALED_BUNDLE_CHECKPOINT_COMMIT="
    + EXPECTED_BUNDLE_CHECKPOINT
)

print(
    "SEALED_BUNDLE_CHECKPOINT_ROLE="
    "DECISION_0128_PRE_REVIEW_PACKAGE_CHECKPOINT"
)

print(
    "BUNDLE_CHECKPOINT_DISTINCT_FROM_DECISION_0129_CHECKPOINT=YES"
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
    "REVIEWER_DECISION_PRESENT=NO"
)

print(
    "HUMAN_REVIEW_PERFORMED=NO"
)

print(
    "EXTERNAL_HANDOFF_ZIP_REQUIRED=YES"
)

print(
    "EDITABLE_MANUAL_REVIEWER_PACKET_REQUIRED=YES"
)

print(
    "REVIEWER_DECISION_SYNTHESIS_AUTHORIZED=NO"
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
    "SCHEMA_VERSION_PRESELECTED=NO"
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
    "DECISION_0128_A02_STATE="
    "PERMANENTLY_RETIRED"
)

print(
    "DECISION_0128_A02_EXECUTED_BY_THIS_VERIFIER=NO"
)

print(
    "DECISION_0126_A02_STATE="
    "PERMANENTLY_RETIRED"
)

print(
    "DECISION_0126_A02_EXECUTED_BY_THIS_VERIFIER=NO"
)

print(
    "RETIRED_A02_VERIFIERS_EXECUTED=NO"
)

print(
    "EXTERNAL_INDEPENDENT_HUMAN_REVIEW_HANDOFF_AUTHORING_AUTHORIZATION=PASS"
)

print(
    "VERIFIER_LIFECYCLE="
    "ONE_FINAL_RUN_IMMEDIATELY_BEFORE_EXTERNAL_HANDOFF_AUTHORING_THEN_PERMANENT_RETIREMENT"
)
