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
    + "/schema_v2_requirement_bound_carrier_admissibility_resolution_study_v1_bounded_governance_adoption_v1"
)

THIS_AUTH_REL = (
    BASE_REL
    + "/schema_v2_requirement_to_semantic_unit_crosswalk_evidence_resolution_study_v1_authorization_v1"
)

FUTURE_STUDY_REL = (
    BASE_REL
    + "/schema_v2_requirement_to_semantic_unit_crosswalk_evidence_resolution_study_v1"
)

ADOPT = REPO / ADOPT_REL

SAFE = (
    ADOPT
    / "07_verify_bounded_governance_adoption.v1.py"
)

MANIFEST = (
    ADOPT
    / "01_bounded_governance_adoption_manifest.v1.json"
)

AUTH = (
    HERE
    / "01_requirement_to_semantic_unit_crosswalk_evidence_resolution_study_v1_authorization.v1.json"
)

SCHEMA = (
    REPO
    / "config/schemas/protocol_specification.v2.schema.json"
)

EXPECTED_DECISION0146 = (
    "179f59732d0a68d115e7902794dddb512b5dc4c0"
)

EXPECTED_ADOPT_TREE = (
    "cf3df758ba19115e0cfffe1bf9b452e8520e7680"
)

EXPECTED_SCHEMA_SHA = (
    "c6ebb5ef2214c4168283f9009d1f7ce6e88d2ff928853fe6a57ed1f7521c6956"
)

EXPECTED_REQUIREMENTS = [
    "all_10_v4_semantic_containers_preserved",
    "all_3_exit_obligations_accounted_for",
    "all_64_rule_records_accounted_for",
    "complete_exact_v4_representation_policy_machine_checkably_bound",
    "complete_exact_v4_representation_policy_preserved",
    "forward_accounting_required",
    "four_verdict_contract_preserved",
    "membership_sensitive_semantics_preserved",
    "normative_strength_uncertainty_policy_preserved",
    "ownership_sensitive_semantics_preserved",
    "path_sensitive_semantics_preserved",
    "resource_centered_semantics_preserved",
    "return_sensitive_semantics_preserved",
    "reverse_accounting_required",
    "set_valued_state_reasoning_preserved",
    "synthetic_protocol_events_invented_false_policy_preserved",
    "unknown_first_class_preserved",
]

def fail(msg):
    print("FAIL|" + msg)
    raise SystemExit(1)

def git(*args):
    p = subprocess.run(
        ["git", "-C", str(REPO), *args],
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

def sha(path):
    if not path.is_file():
        fail("MISSING|" + str(path))

    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()

head = git(
    "rev-parse",
    "HEAD",
)

parent = git(
    "show",
    "-s",
    "--format=%P",
    "HEAD",
)

if head == EXPECTED_DECISION0146:
    fail(
        "CROSSWALK_STUDY_AUTHORIZATION_NOT_COMMITTED"
    )

if parent != EXPECTED_DECISION0146:
    fail(
        "CURRENT_HEAD_IS_NOT_IMMEDIATE_SUCCESSOR_OF_DECISION0146"
    )

if (
    git(
        "rev-parse",
        "HEAD:" + ADOPT_REL,
    )
    != EXPECTED_ADOPT_TREE
):
    fail(
        "DECISION0146_ADOPTION_TREE"
    )

git(
    "cat-file",
    "-e",
    "HEAD:" + THIS_AUTH_REL,
)

if (REPO / FUTURE_STUDY_REL).exists():
    fail(
        "CROSSWALK_EVIDENCE_RESOLUTION_STUDY_ALREADY_EXISTS"
    )

if git(
    "status",
    "--porcelain=v1",
    "--untracked-files=all",
):
    fail(
        "REPOSITORY_NOT_CLEAN"
    )

if sha(SCHEMA) != EXPECTED_SCHEMA_SHA:
    fail(
        "ACTIVE_SCHEMA_V2_SHA"
    )

auth = json.loads(
    AUTH.read_text(encoding="utf-8")
)

if auth["authorization_type"] != \
    "PRE_CROSSWALK_EVIDENCE_RESOLUTION_STUDY_AUTHORING_ONLY":
    fail(
        "AUTHORIZATION_TYPE"
    )

if auth["status"] != \
    "AUTHORIZED_NOT_YET_AUTHORED":
    fail(
        "AUTHORIZATION_STATUS"
    )

gov = auth["governance_prerequisite"]

if gov[
    "requirement_bound_carrier_study_v1_governance_adopted"
] is not True:
    fail(
        "GOVERNANCE_ADOPTION_PREREQUISITE"
    )

if gov["adopted_governance_result"] != \
    "FURTHER_EVIDENCE_REQUIRED":
    fail(
        "ADOPTED_RESULT"
    )

if gov["remaining_blocking_gap"] != \
    "NO_AUTHORIZED_REQUIREMENT_TO_SEMANTIC_UNIT_CROSSWALK_IDENTIFIED":
    fail(
        "BLOCKING_GAP"
    )

for key in (
    "carrier_admissibility_resolved",
    "positive_mapping_proven",
    "negative_mapping_impossibility_proven",
    "whole_v4_exhaustiveness_proven",
):
    if gov[key] is not False:
        fail(
            "UNEXPECTED_PRIOR_TECHNICAL_CLAIM|"
            + key
        )

reqs = auth[
    "canonical_requirement_universe"
]

if reqs["count"] != 17:
    fail(
        "REQUIREMENT_COUNT"
    )

if reqs["requirement_ids"] != EXPECTED_REQUIREMENTS:
    fail(
        "REQUIREMENT_IDENTITY_SET"
    )

units = auth[
    "semantic_unit_universe"
]

if units["count"] != 109:
    fail(
        "SEMANTIC_UNIT_COUNT"
    )

goal = auth[
    "authorized_study_goal"
]

if goal["candidate_pair_universe_size"] != 1853:
    fail(
        "CANDIDATE_PAIR_UNIVERSE_SIZE"
    )

if goal[
    "study_must_account_for_every_requirement_semantic_unit_pair"
] is not True:
    fail(
        "PAIR_ACCOUNTING_REQUIREMENT"
    )

if goal[
    "study_may_not_modify_historical_18639_unit_to_schema_path_pairs"
] is not True:
    fail(
        "HISTORICAL_PAIR_PROTECTION"
    )

pair_contract = auth[
    "pair_level_classification_contract"
]

if pair_contract["pair_count_required"] != 1853:
    fail(
        "PAIR_COUNT_REQUIRED"
    )

if pair_contract["allowed_values"] != [
    "SUPPORTED_BINDING",
    "NOT_SUPPORTED_BINDING",
    "UNRESOLVED_BINDING",
]:
    fail(
        "PAIR_CLASSIFICATION_VOCABULARY"
    )

rollup = auth[
    "requirement_level_rollup_contract"
]

if rollup["requirement_count_required"] != 17:
    fail(
        "ROLLUP_REQUIREMENT_COUNT"
    )

if rollup["allowed_values"] != [
    "BOUND_SINGLE_UNIT",
    "BOUND_COMPOSITE_UNITS",
    "NO_AUTHORIZED_CROSSWALK_PROVEN",
    "UNRESOLVED",
]:
    fail(
        "ROLLUP_CLASSIFICATION_VOCABULARY"
    )

if rollup[
    "binding_does_not_equal_carrier_admissibility"
] is not True:
    fail(
        "CARRIER_ADMISSIBILITY_BOUNDARY"
    )

if rollup[
    "binding_does_not_equal_schema_mapping"
] is not True:
    fail(
        "SCHEMA_MAPPING_BOUNDARY"
    )

if auth[
    "historical_state_protection"
][
    "historical_18639_pair_records_read_only"
] is not True:
    fail(
        "HISTORICAL_PAIR_READ_ONLY"
    )

for key, value in auth[
    "explicit_non_authorizations"
].items():
    if value is not False:
        fail(
            "UNEXPECTED_OPERATIONAL_AUTHORIZATION|"
            + key
        )

for key, value in auth[
    "retired_verifier_policy"
].items():
    if value is not False:
        fail(
            "RETIRED_A02_RERUN_ALLOWED|"
            + key
        )

manifest = json.loads(
    MANIFEST.read_text(encoding="utf-8")
)

if (
    manifest["adoption_status"]
    != "ADOPTED_AS_BOUNDED_GOVERNANCE_EVIDENCE"
):
    fail(
        "DECISION0146_ADOPTION_STATUS"
    )

if (
    manifest["governance_state"]["study_governance_adopted"]
    is not True
):
    fail(
        "STUDY_NOT_GOVERNANCE_ADOPTED"
    )

if (
    manifest["governance_state"]["adopted_governance_result"]
    != "FURTHER_EVIDENCE_REQUIRED"
):
    fail(
        "DECISION0146_GOVERNANCE_RESULT"
    )

if (
    manifest["adopted_bounded_result"][
        "requirement_to_semantic_unit_crosswalk_identified"
    ]
    is not False
):
    fail(
        "CROSSWALK_ALREADY_IDENTIFIED"
    )

if (
    manifest["adopted_bounded_result"]["unresolved_count"]
    != 17
):
    fail(
        "PRIOR_UNRESOLVED_COUNT"
    )

p = subprocess.run(
    [
        "python3",
        str(SAFE),
    ],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    check=False,
)

if p.returncode != 0:
    fail(
        "DECISION0146_SAFE_VERIFIER|"
        + p.stdout
        + p.stderr
    )

for marker in (
    "REQUIREMENT_BOUND_CARRIER_STUDY_V1_BOUNDED_GOVERNANCE_ADOPTION=PASS",
    "STUDY_GOVERNANCE_ADOPTED=YES",
    "ADOPTED_GOVERNANCE_RESULT=FURTHER_EVIDENCE_REQUIRED",
    "REQUIREMENT_TO_SEMANTIC_UNIT_CROSSWALK_IDENTIFIED=NO",
    "UNRESOLVED_COUNT=17",
    "CARRIER_ADMISSIBILITY_RESOLVED=NO",
    "OPERATIONAL_MAPPING_AUTHORIZED=NO",
    "SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO",
    "ANALYZER_IMPLEMENTATION_AUTHORIZED=NO",
    "REPAIR_AUTHORIZED=NO",
    "DECISION_0145_A02_STATE=PERMANENTLY_RETIRED",
    "RETIRED_A02_VERIFIERS_EXECUTED=NO",
):
    if marker not in p.stdout:
        fail(
            "DECISION0146_SAFE_MARKER|"
            + marker
        )

print(
    "REQUIREMENT_TO_SEMANTIC_UNIT_CROSSWALK_EVIDENCE_RESOLUTION_STUDY_V1_AUTHORING_AUTHORIZATION=PASS"
)

print(
    "CURRENT_CHECKPOINT_ROLE="
    "IMMEDIATE_SUCCESSOR_OF_DECISION0146"
)

print(
    "CURRENT_HEAD_PARENT_DECISION0146_BINDING=PASS"
)

print(
    "STUDY_GOVERNANCE_ADOPTED=YES"
)

print(
    "ADOPTED_GOVERNANCE_RESULT=FURTHER_EVIDENCE_REQUIRED"
)

print(
    "REQUIREMENT_COUNT=17"
)

print(
    "SEMANTIC_UNIT_COUNT=109"
)

print(
    "CANDIDATE_REQUIREMENT_SEMANTIC_UNIT_PAIR_COUNT=1853"
)

print(
    "PAIR_CLASSIFICATIONS=SUPPORTED_BINDING|NOT_SUPPORTED_BINDING|UNRESOLVED_BINDING"
)

print(
    "REQUIREMENT_ROLLUP_CLASSIFICATIONS=BOUND_SINGLE_UNIT|BOUND_COMPOSITE_UNITS|NO_AUTHORIZED_CROSSWALK_PROVEN|UNRESOLVED"
)

print(
    "HISTORICAL_18639_PAIR_RECLASSIFICATION_AUTHORIZED=NO"
)

print(
    "CARRIER_ADMISSIBILITY_CLASSIFICATION_AUTHORIZED=NO"
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
    "INDEPENDENT_HUMAN_REVIEW_REQUIRED=YES"
)

print(
    "RETIRED_A02_VERIFIERS_EXECUTED=NO"
)

print(
    "VERIFIER_LIFECYCLE="
    "ONE_FINAL_RUN_IMMEDIATELY_BEFORE_REQUIREMENT_TO_SEMANTIC_UNIT_CROSSWALK_EVIDENCE_RESOLUTION_STUDY_V1_AUTHORING_THEN_PERMANENT_RETIREMENT"
)
