#!/usr/bin/env python3

import hashlib
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]

AUTH = (
    HERE
    / "01_sucr01_corrective_portable_source_evidence_successor_package_v2_authorization.v1.json"
)

BASE_REL = Path(
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2"
)

COMPLETED = (
    REPO
    / BASE_REL
    / "schema_v2_semantic_unit_carrier_admissibility_"
      "and_requirement_binding_study_v1_completed_human_review_v1"
)

COMPLETED_EXACT = (
    COMPLETED
    / "01_completed_SUCR01_SUCR08_human_review.EXACT_COPY.v1.md"
)

COMPLETED_RECORD = (
    COMPLETED
    / "02_completed_human_review_record.v1.json"
)

FUTURE_PACKAGE = (
    REPO
    / BASE_REL
    / "schema_v2_sucr01_corrective_portable_source_evidence_successor_package_v2"
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

def git_object(rel):
    proc = subprocess.run(
        [
            "git",
            "-C",
            str(REPO),
            "rev-parse",
            "HEAD:" + rel,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )

    if proc.returncode != 0:
        fail(
            "GIT_OBJECT|" + rel
        )

    return proc.stdout.strip()

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

if FUTURE_PACKAGE.exists():
    fail(
        "CORRECTIVE_SUCCESSOR_PACKAGE_V2_ALREADY_EXISTS"
    )

a = json.loads(
    AUTH.read_text(
        encoding="utf-8"
    )
)

if a["status"] != \
        "AUTHORIZED_FOR_SUCR01_CORRECTIVE_SUCCESSOR_PACKAGE_V2_AUTHORING_ONLY":
    fail(
        "AUTHORIZATION_STATUS"
    )

if a["corrective_scope"] != \
        "SUCR01_ONLY_SOURCE_EVIDENCE_PORTABILITY_AND_RESOLVABILITY":
    fail(
        "CORRECTIVE_SCOPE"
    )

review = a["review_state"]

if review["original_sucr01"] != \
        "REVISION_REQUIRED":
    fail(
        "SUCR01_ORIGINAL_DECISION"
    )

for rid in (
    "sucr02",
    "sucr03",
    "sucr04",
    "sucr05",
    "sucr06",
    "sucr07",
    "sucr08",
):
    if review[
        "original_" + rid
    ] != "PASS":
        fail(
            "CARRIED_PASS_STATE|"
            + rid
        )

if review[
    "original_overall_review"
] != "REVISION_REQUIRED":
    fail(
        "ORIGINAL_OVERALL_REVIEW"
    )

if review[
    "review_chain_closed"
] is not False:
    fail(
        "PREMATURE_REVIEW_CHAIN_CLOSURE"
    )

sources = a[
    "required_portable_source_evidence"
]

for name, spec in sources.items():

    rel = spec[
        "repository_relative_path"
    ]

    path = REPO / rel

    if spec["kind"] == "file":

        if not path.is_file():
            fail(
                "SOURCE_FILE_MISSING|"
                + name
            )

        if sha(path) != spec["sha256"]:
            fail(
                "SOURCE_FILE_SHA|"
                + name
            )

        if path.stat().st_size != \
                spec["size_bytes"]:
            fail(
                "SOURCE_FILE_SIZE|"
                + name
            )

        if "git_blob" in spec:

            if git_object(rel) != \
                    spec["git_blob"]:
                fail(
                    "SOURCE_GIT_BLOB|"
                    + name
                )

    elif spec["kind"] == "git_tree":

        if not path.is_dir():
            fail(
                "SOURCE_DIRECTORY_MISSING|"
                + name
            )

        if git_object(rel) != \
                spec["git_tree"]:
            fail(
                "SOURCE_GIT_TREE|"
                + name
            )

    else:
        fail(
            "UNKNOWN_SOURCE_KIND|"
            + name
        )

record = json.loads(
    COMPLETED_RECORD.read_text(
        encoding="utf-8"
    )
)

if record[
    "completed_review"
][
    "overall_decision"
] != "REVISION_REQUIRED":
    fail(
        "COMPLETED_REVIEW_OVERALL_STATE"
    )

if record[
    "completed_review"
][
    "item_decisions"
][
    "SUCR01"
] != "REVISION_REQUIRED":
    fail(
        "COMPLETED_REVIEW_SUCR01_STATE"
    )

if sha(COMPLETED_EXACT) != \
        "b41c4f737be70cf3de0f837f0f46b186a4d6ac12e7d49ad5e263bcddfb76f50a":
    fail(
        "COMPLETED_REVIEW_EXACT_BINDING"
    )

req = a[
    "corrective_successor_package_requirements"
]

required_true = (
    "original_review_package_v1_must_be_preserved_byte_exactly",
    "completed_original_human_review_must_be_preserved_byte_exactly",
    "decision_0116_completed_review_record_must_be_bound",
    "active_schema_v2_must_be_included_byte_exactly",
    "relation_artifact_must_be_included_byte_exactly",
    "traceability_artifact_must_be_included_byte_exactly",
    "prior_relation_informed_study_v1_must_be_included_as_exact_git_tree_copy",
    "governance_adoption_evidence_must_be_included_as_exact_git_tree_copy",
    "decision_0109_must_be_included_byte_exactly",
    "portable_source_binding_manifest_required",
    "portable_resolvability_manifest_required",
    "safe_post_authoring_verifier_required",
    "checksum_closure_required",
    "semantic_content_of_source_artifacts_must_not_be_modified",
    "original_review_must_not_be_modified",
    "original_overall_revision_required_must_not_be_rewritten_as_approval",
    "sucr02_through_sucr08_original_pass_findings_must_be_carried_forward_without_rereview",
    "package_authoring_does_not_itself_authorize_focused_rereview",
    "package_authoring_does_not_close_review_chain",
)

for key in required_true:
    if req[key] is not True:
        fail(
            "PACKAGE_REQUIREMENT|"
            + key
        )

if req[
    "package_status_after_authoring"
] != "AUTHOR_CANDIDATE_AWAITING_FOCUSED_SUCR01_REREVIEW":
    fail(
        "PACKAGE_POST_AUTHORING_STATE"
    )

if a[
    "focused_corrective_target"
][
    "focused_rereview_authorized_by_this_decision"
] is not False:
    fail(
        "PREMATURE_FOCUSED_REREVIEW_AUTHORIZATION"
    )

for key, value in a[
    "technical_nonclaims"
].items():

    if value is not False:
        fail(
            "UNEXPECTED_TECHNICAL_PERMISSION|"
            + key
        )

for key, value in a[
    "retired_verifier_state"
].items():

    if key == \
            "retired_verifiers_must_not_be_executed":

        if value is not True:
            fail(
                "RETIRED_VERIFIER_POLICY"
            )

    elif value != \
            "PERMANENTLY_RETIRED":

        fail(
            "RETIRED_VERIFIER_STATE|"
            + key
        )

life = a[
    "authorization_verifier_lifecycle"
]

if life[
    "initial_state"
] != "ACTIVE_UNCONSUMED":
    fail(
        "A02_INITIAL_STATE"
    )

if life[
    "may_execute_exactly_once_immediately_before_corrective_successor_package_v2_authoring"
] is not True:
    fail(
        "A02_LIFECYCLE"
    )

print("DECISION_0116_COMPLETED_REVIEW_BINDING=PASS")

print("ORIGINAL_SUCR01_DECISION=REVISION_REQUIRED")
print("SUCR02_SUCR08_ORIGINAL_PASS_FINDINGS_PRESERVED=YES")
print("ORIGINAL_OVERALL_REVIEW_REMAINS=REVISION_REQUIRED")

print("CORRECTIVE_SCOPE=SUCR01_ONLY_SOURCE_EVIDENCE_PORTABILITY_AND_RESOLVABILITY")

print("ACTIVE_SCHEMA_V2_PORTABLE_SOURCE=PASS")
print("RELATION_ARTIFACT_PORTABLE_SOURCE=PASS")
print("TRACEABILITY_ARTIFACT_PORTABLE_SOURCE=PASS")
print("PRIOR_STUDY_V1_PORTABLE_SOURCE=PASS")
print("GOVERNANCE_ADOPTION_PORTABLE_SOURCE=PASS")

print("REVIEW_CHAIN_CLOSED=NO")
print("FOCUSED_SUCR01_REREVIEW_AUTHORIZED=NO")
print("STUDY_GOVERNANCE_ADOPTED=NO")

print("DECISION_0102_A02_STATE=PERMANENTLY_RETIRED")
print("DECISION_0104_A02_STATE=PERMANENTLY_RETIRED")
print("DECISION_0106_A02_STATE=PERMANENTLY_RETIRED")
print("DECISION_0110_A02_STATE=PERMANENTLY_RETIRED")
print("DECISION_0112_A02_STATE=PERMANENTLY_RETIRED")
print("DECISION_0114_A02_STATE=PERMANENTLY_RETIRED")
print("RETIRED_A02_VERIFIERS_EXECUTED=NO")

print("OPERATIONAL_MAPPING_AUTHORIZED=NO")
print("SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO")
print("CURL_JSON_AUTHORIZED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")

print("SUCR01_CORRECTIVE_SUCCESSOR_PACKAGE_V2_AUTHORING_AUTHORIZATION=PASS")
print("VERIFIER_LIFECYCLE=ONE_FINAL_RUN_IMMEDIATELY_BEFORE_CORRECTIVE_PACKAGE_AUTHORING_THEN_PERMANENT_RETIREMENT")
