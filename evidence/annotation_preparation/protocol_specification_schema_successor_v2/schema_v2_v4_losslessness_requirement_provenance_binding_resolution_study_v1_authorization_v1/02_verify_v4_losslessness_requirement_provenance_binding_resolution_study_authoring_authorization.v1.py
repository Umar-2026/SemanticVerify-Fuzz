#!/usr/bin/env python3

import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]

BASE = (
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2"
)

AUTH = (
    HERE
    / "01_v4_losslessness_requirement_provenance_binding_resolution_study_authorization.v1.json"
)

GOV_REL = (
    BASE
    + "/schema_v2_sucr_closed_review_chain_and_bounded_study_v1_governance_adoption_v1"
)

STUDY_REL = (
    BASE
    + "/schema_v2_semantic_unit_carrier_admissibility_and_requirement_binding_study_v1"
)

FUTURE = (
    REPO
    / BASE
    / "schema_v2_v4_losslessness_requirement_provenance_binding_resolution_study_v1"
)

def fail(msg):
    print("FAIL|" + msg)
    raise SystemExit(1)

def git_object(rel):
    p = subprocess.run(
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

    if p.returncode != 0:
        fail(
            "GIT_OBJECT|" + rel
        )

    return p.stdout.strip()

p = subprocess.run(
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

if p.returncode != 0:
    fail("GIT_STATUS")

if p.stdout.strip():
    fail(
        "REPOSITORY_NOT_CLEAN"
    )

if FUTURE.exists():
    fail(
        "PROVENANCE_BINDING_RESOLUTION_STUDY_ALREADY_EXISTS"
    )

if git_object(
    GOV_REL
) != "28a768d8dedc6f8614f7f0c23c19674df481a3ac":
    fail(
        "GOVERNANCE_ADOPTION_TREE"
    )

if git_object(
    STUDY_REL
) != "3f04237bdc58c2be56e85628de5923b87578a051":
    fail(
        "GOVERNED_STUDY_V1_TREE"
    )

a = json.loads(
    AUTH.read_text(
        encoding="utf-8"
    )
)

if a[
    "status"
] != "AUTHORIZED_FOR_V4_LOSSLESSNESS_REQUIREMENT_PROVENANCE_BINDING_RESOLUTION_STUDY_V1_AUTHORING_ONLY":
    fail(
        "AUTHORIZATION_STATUS"
    )

gov = a[
    "governance_state"
]

if gov[
    "review_chain_closed"
] is not True:
    fail(
        "REVIEW_CHAIN_NOT_CLOSED"
    )

if gov[
    "review_chain_closure_outcome"
] != "PASS_CLOSED":
    fail(
        "REVIEW_CHAIN_OUTCOME"
    )

if gov[
    "governance_status"
] != "APPROVED_WITH_BOUNDED_TECHNICAL_OUTCOME":
    fail(
        "GOVERNANCE_STATUS"
    )

if gov[
    "adopted_bounded_technical_outcome"
] != "FURTHER_EVIDENCE_REQUIRED":
    fail(
        "BOUNDED_OUTCOME"
    )

if gov[
    "study_governance_adopted"
] is not True:
    fail(
        "STUDY_NOT_GOVERNANCE_ADOPTED"
    )

contract = a[
    "study_contract"
]

if contract[
    "requirement_inventory_size"
] != 17:
    fail(
        "REQUIREMENT_INVENTORY_SIZE"
    )

if contract[
    "allowed_requirement_binding_classifications"
] != [
    "BOUND_EXACT",
    "BOUND_COMPOSITE",
    "UNRESOLVED",
]:
    fail(
        "BINDING_CLASSIFICATIONS"
    )

if contract[
    "allowed_study_outcomes"
] != [
    "REQUIREMENT_PROVENANCE_RESOLVED",
    "FURTHER_EVIDENCE_REQUIRED",
]:
    fail(
        "STUDY_OUTCOMES"
    )

for key in (
    "must_preserve_existing_requirement_ids",
    "must_not_invent_new_losslessness_requirements",
    "must_record_source_artifact_identity",
    "must_record_source_path_or_structural_location",
    "must_record_source_sha256_or_git_identity_where_available",
    "must_record_binding_rationale",
    "must_record_unresolved_reason_when_unresolved",
    "must_distinguish_direct_source_text_from_author_inference",
    "must_not_treat_absence_as_negative_proof",
    "must_not_reclassify_semantic_unit_carrier_pairs",
    "must_not_change_existing_18639_pair_state",
    "must_not_claim_carrier_admissibility",
    "must_not_construct_positive_mapping_witness",
    "must_not_construct_negative_mapping_impossibility_proof",
    "must_not_claim_whole_v4_composition_exhaustiveness",
    "must_not_modify_active_schema_v2",
    "must_not_author_schema_successor",
    "must_not_preselect_schema_version",
    "must_not_create_curl_json",
    "must_not_authorize_analyzer",
    "must_not_authorize_baseline",
    "must_not_authorize_repair",
):
    if contract[key] is not True:
        fail(
            "STUDY_CONTRACT|" + key
        )

pre = a[
    "pre_study_state"
]

if pre[
    "study_authorized"
] is not True:
    fail(
        "STUDY_NOT_AUTHORIZED"
    )

if pre[
    "study_authored"
] is not False:
    fail(
        "STUDY_PREMATURELY_AUTHORED"
    )

if pre[
    "study_outcome"
] is not None:
    fail(
        "PREMATURE_STUDY_OUTCOME"
    )

for key, value in a[
    "technical_nonauthorizations"
].items():

    if value is not False:
        fail(
            "UNEXPECTED_AUTHORITY|" + key
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
    "may_execute_exactly_once_immediately_before_study_authoring"
] is not True:
    fail(
        "A02_LIFECYCLE"
    )

print("GOVERNANCE_ADOPTION_BINDING=PASS")
print("GOVERNED_STUDY_V1_BINDING=PASS")

print("ADOPTED_BOUNDED_TECHNICAL_OUTCOME=FURTHER_EVIDENCE_REQUIRED")

print("REQUIREMENT_INVENTORY_SIZE=17")
print("AUTHORIZED_BINDING_CLASSES=BOUND_EXACT|BOUND_COMPOSITE|UNRESOLVED")

print("SEMANTIC_UNIT_CARRIER_PAIR_RECLASSIFICATION_AUTHORIZED=NO")
print("POSITIVE_MAPPING_WITNESS_AUTHORIZED=NO")
print("NEGATIVE_MAPPING_IMPOSSIBILITY_PROOF_AUTHORIZED=NO")
print("WHOLE_V4_EXHAUSTIVENESS_CLAIM_AUTHORIZED=NO")

print("SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO")
print("CURL_JSON_AUTHORIZED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")

print("PROVENANCE_BINDING_RESOLUTION_STUDY_AUTHORIZED=YES")
print("PROVENANCE_BINDING_RESOLUTION_STUDY_AUTHORED=NO")

print("RETIRED_A02_VERIFIERS_EXECUTED=NO")

print("V4_LOSSLESSNESS_REQUIREMENT_PROVENANCE_BINDING_RESOLUTION_STUDY_AUTHORING_AUTHORIZATION=PASS")
print("VERIFIER_LIFECYCLE=ONE_FINAL_RUN_IMMEDIATELY_BEFORE_STUDY_AUTHORING_THEN_PERMANENT_RETIREMENT")
