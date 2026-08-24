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

ADOPT_REL = (
    BASE_REL
    + "/schema_v2_v4_losslessness_requirement_provenance_binding_resolution_study_v1_governance_adoption_v1"
)

PROV_REL = (
    BASE_REL
    + "/schema_v2_v4_losslessness_requirement_provenance_binding_resolution_study_v1"
)

PRIOR_REL = (
    BASE_REL
    + "/schema_v2_semantic_unit_carrier_admissibility_and_requirement_binding_study_v1"
)

THIS_AUTH_REL = (
    BASE_REL
    + "/schema_v2_requirement_bound_carrier_admissibility_resolution_study_v1_authorization_v1"
)

SCHEMA_REL = (
    "config/schemas/protocol_specification.v2.schema.json"
)

V4_REL = (
    "config/annotation/curl_technical_protocol_working_draft.v4.json"
)

MAPPING_REL = (
    "config/annotation/curl_canonical_representation_mapping_contract.v4.json"
)

ADOPT = REPO / ADOPT_REL

ADOPT_SAFE = (
    ADOPT
    / "07_verify_bounded_requirement_provenance_governance_adoption.v1.py"
)

AUTH = (
    HERE
    / "01_requirement_bound_carrier_admissibility_resolution_study_v1_authorization.v1.json"
)

SUMS = (
    HERE
    / "03_requirement_bound_carrier_admissibility_resolution_study_v1_authorization.v1.SHA256SUMS"
)

EXPECTED_DECISION0136 = (
    "ea07e29b61e2a9d76a852be7acfdd1d942aa367d"
)

EXPECTED_ADOPT_TREE = (
    "9893bd5dc8d7472f1177c373fa89d289de9ca59f"
)

EXPECTED_PROV_TREE = (
    "ee85980dcff85b5be3f21995f578b3b78cf39aa2"
)

EXPECTED_SCHEMA_SHA = (
    "c6ebb5ef2214c4168283f9009d1f7ce6e88d2ff928853fe6a57ed1f7521c6956"
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

if current_head == EXPECTED_DECISION0136:
    fail(
        "STUDY_AUTHORIZATION_NOT_COMMITTED"
    )

if current_parent != EXPECTED_DECISION0136:
    fail(
        "CURRENT_HEAD_IS_NOT_IMMEDIATE_SUCCESSOR_OF_DECISION0136"
    )

if git(
    "rev-parse",
    "HEAD:" + ADOPT_REL,
) != EXPECTED_ADOPT_TREE:
    fail(
        "ADOPTION_GIT_TREE"
    )

if git(
    "rev-parse",
    "HEAD:" + PROV_REL,
) != EXPECTED_PROV_TREE:
    fail(
        "PROVENANCE_STUDY_GIT_TREE"
    )

git(
    "cat-file",
    "-e",
    "HEAD:" + PRIOR_REL,
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

auth = json.loads(
    AUTH.read_text(
        encoding="utf-8"
    )
)

if (
    auth["authorization_type"]
    != "PRE_REQUIREMENT_BOUND_CARRIER_ADMISSIBILITY_STUDY_AUTHORING_ONLY"
):
    fail(
        "AUTHORIZATION_TYPE"
    )

if (
    auth["status"]
    != "AUTHORIZED_NOT_YET_STUDIED"
):
    fail(
        "AUTHORIZATION_STATUS"
    )

basis = auth[
    "governance_adopted_requirement_basis"
]

if basis["outcome"] != "REQUIREMENT_PROVENANCE_RESOLVED":
    fail(
        "REQUIREMENT_BASIS_OUTCOME"
    )

if (
    basis["scope"]
    != "REQUIREMENT_IDENTITY_AND_SOURCE_PROVENANCE_ONLY"
):
    fail(
        "REQUIREMENT_BASIS_SCOPE"
    )

if basis["requirement_count"] != 17:
    fail(
        "REQUIREMENT_COUNT"
    )

if basis["bound_exact_count"] != 17:
    fail(
        "BOUND_EXACT_COUNT"
    )

if basis["unresolved_count"] != 0:
    fail(
        "REQUIREMENT_PROVENANCE_UNRESOLVED_COUNT"
    )

historical = auth[
    "historical_carrier_study_basis"
]

if historical["historical_semantic_unit_count"] != 109:
    fail(
        "SEMANTIC_UNIT_COUNT"
    )

if historical["historical_schema_path_count"] != 171:
    fail(
        "SCHEMA_PATH_COUNT"
    )

if historical["historical_pair_count"] != 18639:
    fail(
        "PAIR_COUNT"
    )

if (
    historical["historical_pair_state_mutable_by_successor_study"]
    is not False
):
    fail(
        "HISTORICAL_PAIR_MUTABILITY"
    )

if (
    historical["historical_pair_reclassification_authorized"]
    is not False
):
    fail(
        "HISTORICAL_PAIR_RECLASSIFICATION"
    )

if (
    git(
        "rev-parse",
        "HEAD:" + PRIOR_REL,
    )
    != historical["git_tree"]
):
    fail(
        "HISTORICAL_CARRIER_STUDY_TREE"
    )

source = auth[
    "exact_technical_source_basis"
]

if sha(REPO / SCHEMA_REL) != EXPECTED_SCHEMA_SHA:
    fail(
        "ACTIVE_SCHEMA_SHA"
    )

if (
    sha(REPO / SCHEMA_REL)
    != source["active_schema_v2_sha256"]
):
    fail(
        "AUTH_SCHEMA_SHA_BINDING"
    )

if (
    sha(REPO / V4_REL)
    != source["approved_curl_v4_sha256"]
):
    fail(
        "APPROVED_V4_SHA_BINDING"
    )

if (
    sha(REPO / MAPPING_REL)
    != source[
        "canonical_representation_mapping_contract_v4_sha256"
    ]
):
    fail(
        "MAPPING_CONTRACT_SHA_BINDING"
    )

allowed = auth[
    "per_requirement_allowed_classifications"
]

if allowed != [
    "ADMISSIBLE_EXACT",
    "ADMISSIBLE_COMPOSITE",
    "NO_ADMISSIBLE_CARRIER_PROVEN",
    "UNRESOLVED",
]:
    fail(
        "CLASSIFICATION_VOCABULARY"
    )

boundaries = auth[
    "critical_scope_boundaries"
]

for key, value in boundaries.items():
    if value is not True:
        fail(
            "MISSING_SCOPE_BOUNDARY|"
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

for key, value in auth[
    "retired_verifier_policy"
].items():
    if value is not False:
        fail(
            "RETIRED_VERIFIER_RERUN_ALLOWED|"
            + key
        )

# Reverify adopted requirement-provenance governance state only
# through its safe verifier.
p = subprocess.run(
    [
        "python3",
        str(ADOPT_SAFE),
    ],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    check=False,
)

if p.returncode != 0:
    fail(
        "ADOPTION_SAFE_VERIFIER|"
        + p.stdout
        + p.stderr
    )

for marker in (
    "BOUNDED_REQUIREMENT_PROVENANCE_GOVERNANCE_ADOPTION_V1=PASS",
    "STUDY_GOVERNANCE_ADOPTED=YES",
    "ADOPTED_OUTCOME=REQUIREMENT_PROVENANCE_RESOLVED",
    "REQUIREMENT_COUNT=17",
    "CARRIER_ADMISSIBILITY_PROVEN=NO",
    "POSITIVE_MAPPING_PROVEN=NO",
    "NEGATIVE_MAPPING_IMPOSSIBILITY_PROVEN=NO",
    "RETIRED_A02_VERIFIERS_EXECUTED=NO",
):
    if marker not in p.stdout:
        fail(
            "ADOPTION_SAFE_MARKER|"
            + marker
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

        if sha(HERE / rel) != digest:
            fail(
                "AUTHORIZATION_CHECKSUM|"
                + rel
            )

print(
    "REQUIREMENT_BOUND_CARRIER_ADMISSIBILITY_RESOLUTION_STUDY_V1_AUTHORIZATION=PASS"
)

print(
    "CURRENT_CHECKPOINT_ROLE="
    "IMMEDIATE_SUCCESSOR_OF_DECISION0136"
)

print(
    "CURRENT_HEAD_PARENT_DECISION0136_BINDING=PASS"
)

print(
    "GOVERNANCE_ADOPTED_REQUIREMENT_COUNT=17"
)

print(
    "REQUIREMENT_PROVENANCE_STATUS="
    "REQUIREMENT_PROVENANCE_RESOLVED"
)

print(
    "STUDY_SCOPE="
    "REQUIREMENT_BOUND_CARRIER_ADMISSIBILITY_ONLY"
)

print(
    "HISTORICAL_SEMANTIC_UNIT_COUNT=109"
)

print(
    "HISTORICAL_SCHEMA_PATH_COUNT=171"
)

print(
    "HISTORICAL_PAIR_COUNT=18639"
)

print(
    "HISTORICAL_PAIR_RECLASSIFICATION_AUTHORIZED=NO"
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
    "ONE_FINAL_RUN_IMMEDIATELY_BEFORE_REQUIREMENT_BOUND_CARRIER_ADMISSIBILITY_RESOLUTION_STUDY_V1_AUTHORING_THEN_PERMANENT_RETIREMENT"
)
