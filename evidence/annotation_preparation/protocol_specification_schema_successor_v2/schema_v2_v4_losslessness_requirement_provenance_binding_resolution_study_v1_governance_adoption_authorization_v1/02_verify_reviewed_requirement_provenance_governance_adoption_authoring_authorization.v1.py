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

STUDY_REL = (
    BASE_REL
    + "/schema_v2_v4_losslessness_requirement_provenance_binding_resolution_study_v1"
)

REVIEW_REL = (
    BASE_REL
    + "/schema_v2_v4_losslessness_requirement_provenance_binding_resolution_study_v1_completed_human_review_v1"
)

THIS_AUTH_REL = (
    BASE_REL
    + "/schema_v2_v4_losslessness_requirement_provenance_binding_resolution_study_v1_governance_adoption_authorization_v1"
)

REVIEW = REPO / REVIEW_REL

REVIEW_SAFE = (
    REVIEW
    / "04_verify_repository_completed_RPR01_RPR08_human_review.v1.py"
)

AUTH = (
    HERE
    / "01_reviewed_requirement_provenance_governance_adoption_authorization.v1.json"
)

SUMS = (
    HERE
    / "03_reviewed_requirement_provenance_governance_adoption_authorization.v1.SHA256SUMS"
)

EXPECTED_DECISION0134_COMMIT = (
    "f36cd77ead4ee4f154b4bc7cfa2b88ce963a05d9"
)

EXPECTED_STUDY_TREE = (
    "ee85980dcff85b5be3f21995f578b3b78cf39aa2"
)

EXPECTED_REVIEW_TREE = (
    "d873ef00dceb359a2dc8dc25293ab8ec57518dd2"
)

EXPECTED_COMPLETED_REVIEW_SHA = (
    "f133c13bdaeb71055bd839663332c921"
    "556dc516544e19e655f204032d33af71"
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
# Execution must occur from Decision-0135, whose parent is 0134.
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

if current_head == EXPECTED_DECISION0134_COMMIT:
    fail(
        "GOVERNANCE_ADOPTION_AUTHORIZATION_NOT_COMMITTED"
    )

if current_parent != EXPECTED_DECISION0134_COMMIT:
    fail(
        "CURRENT_HEAD_IS_NOT_IMMEDIATE_SUCCESSOR_OF_DECISION0134"
    )

if (
    git(
        "rev-parse",
        "HEAD:" + STUDY_REL,
    )
    != EXPECTED_STUDY_TREE
):
    fail(
        "STUDY_V1_GIT_TREE"
    )

if (
    git(
        "rev-parse",
        "HEAD:" + REVIEW_REL,
    )
    != EXPECTED_REVIEW_TREE
):
    fail(
        "COMPLETED_HUMAN_REVIEW_GIT_TREE"
    )

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
# Authorization semantics
# ------------------------------------------------------------

auth = json.loads(
    AUTH.read_text(
        encoding="utf-8"
    )
)

if (
    auth["authorization_type"]
    != "PRE_GOVERNANCE_ADOPTION_AUTHORING_ONLY"
):
    fail("AUTHORIZATION_TYPE")

if (
    auth["status"]
    != "AUTHORIZED_NOT_YET_ADOPTED"
):
    fail("AUTHORIZATION_STATUS")

checkpoint = auth[
    "decision_0134_checkpoint"
]

if (
    checkpoint["commit"]
    != EXPECTED_DECISION0134_COMMIT
):
    fail("DECISION0134_BINDING")

if (
    checkpoint["study_v1_git_tree"]
    != EXPECTED_STUDY_TREE
):
    fail("STUDY_TREE_BINDING")

if (
    checkpoint["completed_human_review_v1_git_tree"]
    != EXPECTED_REVIEW_TREE
):
    fail("REVIEW_TREE_BINDING")

if (
    checkpoint["completed_reviewer_packet_sha256"]
    != EXPECTED_COMPLETED_REVIEW_SHA
):
    fail("REVIEW_PACKET_SHA_BINDING")

review_basis = auth[
    "review_basis"
]

if review_basis["human_review_completed"] is not True:
    fail("HUMAN_REVIEW_NOT_COMPLETED")

if review_basis["reviewer_decision_synthesized"] is not False:
    fail("SYNTHETIC_REVIEW_DECISION")

for key in (
    "rpr01",
    "rpr02",
    "rpr03",
    "rpr04",
    "rpr05",
    "rpr06",
    "rpr07",
    "rpr08",
):
    if review_basis[key] != "PASS":
        fail("RPR_DECISION|" + key)

if (
    review_basis["overall_review_decision"]
    != "APPROVE_V4_LOSSLESSNESS_REQUIREMENT_PROVENANCE_BINDING_RESOLUTION_STUDY_V1"
):
    fail("OVERALL_REVIEW_DECISION")

adoption = auth[
    "authorized_governance_adoption"
]

if (
    adoption["adopt_outcome"]
    != "REQUIREMENT_PROVENANCE_RESOLVED"
):
    fail("ADOPTED_OUTCOME")

if (
    adoption["adopt_scope"]
    != "REQUIREMENT_IDENTITY_AND_SOURCE_PROVENANCE_ONLY"
):
    fail("ADOPTED_SCOPE")

if adoption["adoption_is_bounded"] is not True:
    fail("BOUNDED_ADOPTION_POLICY")

for key in (
    "preserve_schema_v2_losslessness_nonclaim",
    "preserve_carrier_admissibility_nonclaim",
    "preserve_positive_mapping_nonclaim",
    "preserve_negative_mapping_impossibility_nonclaim",
    "preserve_whole_v4_exhaustiveness_nonclaim",
):
    if adoption[key] is not True:
        fail(
            "NONCLAIM_PRESERVATION|"
            + key
        )

gov = auth[
    "governance_state_before_adoption"
]

if gov["study_governance_adopted"] is not False:
    fail("PREMATURE_ADOPTION")

if gov["governance_adoption_authorized"] is not True:
    fail("GOVERNANCE_ADOPTION_NOT_AUTHORIZED")

if gov["governance_adoption_completed"] is not False:
    fail("PREMATURE_ADOPTION_COMPLETION")

for key, value in auth[
    "explicit_non_authorizations"
].items():
    if value is not False:
        fail(
            "UNEXPECTED_AUTHORIZATION|"
            + key
        )

for key, value in auth[
    "retired_verifier_policy"
].items():
    if value is not False:
        fail(
            "RETIRED_VERIFIER_RERUN_ALLOWED|"
            + key
        )

# ------------------------------------------------------------
# Reverify completed review through the safe verifier only.
# ------------------------------------------------------------

p = subprocess.run(
    [
        "python3",
        str(REVIEW_SAFE),
    ],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    check=False,
)

if p.returncode != 0:
    fail(
        "COMPLETED_REVIEW_SAFE_VERIFIER|"
        + p.stdout
        + p.stderr
    )

required_markers = [
    "COMPLETED_RPR01_RPR08_HUMAN_REVIEW_RECORD_V1=PASS",
    "HUMAN_REVIEW_COMPLETED=YES",
    "RPR01_RPR08_PASS_COUNT=8",
    "APPROVAL_SCOPE=REQUIREMENT_IDENTITY_AND_SOURCE_PROVENANCE_ONLY",
    "STUDY_GOVERNANCE_ADOPTED=NO",
    "RETIRED_A02_VERIFIERS_EXECUTED=NO",
]

for marker in required_markers:
    if marker not in p.stdout:
        fail(
            "COMPLETED_REVIEW_SAFE_MARKER|"
            + marker
        )

# ------------------------------------------------------------
# Authorization checksum closure when present.
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
                "AUTHORIZATION_CHECKSUM|"
                + rel
            )

print(
    "REVIEWED_REQUIREMENT_PROVENANCE_GOVERNANCE_ADOPTION_AUTHORIZATION=PASS"
)

print(
    "CURRENT_CHECKPOINT_ROLE="
    "IMMEDIATE_SUCCESSOR_OF_DECISION0134"
)

print(
    "CURRENT_HEAD_PARENT_DECISION0134_BINDING=PASS"
)

print(
    "HUMAN_REVIEW_COMPLETED=YES"
)

print(
    "RPR01_RPR08_PASS_COUNT=8"
)

print(
    "REVIEWED_OUTCOME="
    "REQUIREMENT_PROVENANCE_RESOLVED"
)

print(
    "AUTHORIZED_ADOPTION_SCOPE="
    "REQUIREMENT_IDENTITY_AND_SOURCE_PROVENANCE_ONLY"
)

print(
    "STUDY_GOVERNANCE_ADOPTED=NO"
)

print(
    "GOVERNANCE_ADOPTION_AUTHORIZED=YES"
)

print(
    "GOVERNANCE_ADOPTION_COMPLETED=NO"
)

print(
    "SCHEMA_V2_LOSSLESSNESS_PROVEN=NO"
)

print(
    "CARRIER_ADMISSIBILITY_PROVEN=NO"
)

print(
    "POSITIVE_MAPPING_PROVEN=NO"
)

print(
    "NEGATIVE_MAPPING_IMPOSSIBILITY_PROVEN=NO"
)

print(
    "WHOLE_V4_EXHAUSTIVENESS_PROVEN=NO"
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
    "RETIRED_A02_VERIFIERS_EXECUTED=NO"
)

print(
    "VERIFIER_LIFECYCLE="
    "ONE_FINAL_RUN_IMMEDIATELY_BEFORE_BOUNDED_GOVERNANCE_ADOPTION_AUTHORING_THEN_PERMANENT_RETIREMENT"
)
