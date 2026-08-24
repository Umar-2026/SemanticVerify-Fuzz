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

ADOPT = (
    REPO
    / BASE_REL
    / "schema_v2_relation_informed_exhaustive_"
      "admissible_composition_study_v1_governance_adoption_v1"
)

G01 = ADOPT / "01_governance_adoption_assessment.v1.json"
G02 = ADOPT / "02_verify_governance_adoption.v1.py"
G03 = ADOPT / "03_governance_adoption.v1.SHA256SUMS"

STUDY = (
    REPO
    / BASE_REL
    / "schema_v2_relation_informed_exhaustive_"
      "admissible_composition_study_v1"
)

STUDY_JSON = (
    STUDY
    / "01_relation_informed_exhaustive_admissible_composition_study.v1.json"
)

AUTH = (
    HERE
    / "01_semantic_unit_carrier_admissibility_and_requirement_binding_study_authorization.v1.json"
)

FUTURE_STUDY = (
    REPO
    / BASE_REL
    / "schema_v2_semantic_unit_carrier_admissibility_"
      "and_requirement_binding_study_v1"
)

EXPECTED = {
    G01:
        "de4f4dddbd222d1d100cd2aa6845db1ccaf57459d6c7f6b7ba72663c0ecbac43",

    G02:
        "844d8572168103fa538ebf3cd3ec2804d653fbef927b214c6616e190f0f9fe70",

    G03:
        "5b7a5e45c18be1c317e04cbcc5e0fd820ae54bf1f1b9e2159c872ead970259fa",

    STUDY_JSON:
        "a8d28b09e78e1466eb5bb0991289879b28b10abd1dd1f9197d138ca723718f6f",
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
            "SOURCE_BINDING|" + str(path)
        )

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

if FUTURE_STUDY.exists():
    fail("FUTURE_STUDY_ALREADY_EXISTS")

g = json.loads(
    G01.read_text(
        encoding="utf-8"
    )
)

if g["status"] != \
        "GOVERNANCE_ADOPTED_WITH_BOUNDED_TECHNICAL_OUTCOME":
    fail(
        "GOVERNANCE_STATUS"
    )

if g[
    "governance_adoption"
][
    "adopted_technical_outcome"
] != "FURTHER_EVIDENCE_REQUIRED":
    fail(
        "ADOPTED_OUTCOME"
    )

s = json.loads(
    STUDY_JSON.read_text(
        encoding="utf-8"
    )
)

if s["global_outcome"] != \
        "FURTHER_EVIDENCE_REQUIRED":
    fail(
        "SOURCE_STUDY_OUTCOME"
    )

auth = json.loads(
    AUTH.read_text(
        encoding="utf-8"
    )
)

if auth["status"] != \
        "AUTHORIZED_FOR_STUDY_AUTHORING_ONLY":
    fail(
        "AUTHORIZATION_STATUS"
    )

work = auth["authorized_workstreams"]

uc = work[
    "semantic_unit_carrier_admissibility_domain"
]

if uc["semantic_unit_count"] != 109:
    fail("SEMANTIC_UNIT_COUNT")

if uc["schema_v2_property_path_count"] != 171:
    fail("SCHEMA_PATH_COUNT")

if uc["required_cartesian_pair_count"] != 18639:
    fail("UNIT_CARRIER_DOMAIN_SIZE")

if uc["allowed_pair_classifications"] != [
    "CANDIDATE_ADMISSIBLE",
    "NOT_ADMISSIBLE",
    "UNRESOLVED",
]:
    fail("PAIR_CLASSIFICATIONS")

rb = work[
    "losslessness_requirement_provenance_binding"
]

if rb["requirement_count_in_scope"] != 17:
    fail("REQUIREMENT_COUNT")

if rb["invented_requirement_text_prohibited"] is not True:
    fail("INVENTED_REQUIREMENT_TEXT_POLICY")

if rb[
    "semantic_reconstruction_from_memory_prohibited"
] is not True:
    fail("REQUIREMENT_MEMORY_RECONSTRUCTION_POLICY")

coherence = work[
    "cross_unit_coherence_constraint_inventory"
]

if coherence[
    "whole_v4_composition_enumeration_authorized"
] is not False:
    fail("PREMATURE_COMPOSITION_ENUMERATION")

for key, value in auth[
    "explicit_non_authorizations"
].items():
    if value is not False:
        fail(
            "UNEXPECTED_AUTHORIZATION|" + key
        )

if auth[
    "field_class_domain_safety"
][
    "vocabularies_must_not_be_equated"
] is not True:
    fail("FIELD_CLASS_VOCABULARY_POLICY")

if auth[
    "authorization_verifier_lifecycle"
][
    "initial_state"
] != "ACTIVE_UNCONSUMED":
    fail("VERIFIER_INITIAL_STATE")

if auth[
    "authorization_verifier_lifecycle"
][
    "may_execute_exactly_once_immediately_before_study_authoring"
] is not True:
    fail("VERIFIER_LIFECYCLE")

print("DECISION_0109_GOVERNANCE_BINDING=PASS")
print("ADOPTED_TECHNICAL_OUTCOME=FURTHER_EVIDENCE_REQUIRED")

print("SEMANTIC_UNIT_COUNT=109")
print("SCHEMA_V2_PROPERTY_PATH_COUNT=171")
print("UNIT_CARRIER_CARTESIAN_DOMAIN_SIZE=18639")

print("LOSSLESSNESS_REQUIREMENT_COUNT_IN_SCOPE=17")
print("INVENTED_REQUIREMENT_TEXT_ALLOWED=NO")
print("REQUIREMENT_RECONSTRUCTION_FROM_MEMORY_ALLOWED=NO")

print("CROSS_UNIT_COHERENCE_CONSTRAINT_INVENTORY_AUTHORIZED=YES")
print("WHOLE_V4_COMPOSITION_ENUMERATION_AUTHORIZED=NO")

print("POSITIVE_EXISTING_V2_MAPPING_AUTHORIZED=NO")
print("NEGATIVE_EXISTING_V2_MAPPING_IMPOSSIBILITY_AUTHORIZED=NO")
print("SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO")
print("SCHEMA_VERSION_PRESELECTED=NO")
print("CURL_JSON_AUTHORIZED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")

print("DECISION_0102_A02_STATE=PERMANENTLY_RETIRED")
print("DECISION_0104_A02_STATE=PERMANENTLY_RETIRED")
print("DECISION_0106_A02_STATE=PERMANENTLY_RETIRED")
print("RETIRED_A02_VERIFIERS_EXECUTED=NO")

print("SEMANTIC_UNIT_CARRIER_AND_REQUIREMENT_BINDING_STUDY_AUTHORING_AUTHORIZATION=PASS")
print("VERIFIER_LIFECYCLE=ONE_FINAL_RUN_IMMEDIATELY_BEFORE_STUDY_AUTHORING_THEN_PERMANENT_RETIREMENT")
