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

STUDY = (
    REPO
    / BASE_REL
    / "schema_v2_relation_informed_exhaustive_admissible_composition_study_v1"
)

AUTH = (
    HERE
    / "01_relation_informed_exhaustive_admissible_composition_study_authorization.v1.json"
)

SCHEMA = (
    REPO
    / "config"
    / "schemas"
    / "protocol_specification.v2.schema.json"
)

CLOSURE = (
    REPO
    / BASE_REL
    / "schema_v2_semantic_role_relation_formalization_v1_review_chain_closure_v1"
    / "01_review_chain_closure_assessment.v1.json"
)

EXPECTED_SCHEMA_SHA = (
    "c6ebb5ef2214c4168283f9009d1f7ce6"
    "e88d2ff928853fe6a57ed1f7521c6956"
)

EXPECTED_SCHEMA_BLOB = (
    "245fc02f538c21cff5de25f4a6a3c297e915e40f"
)

EXPECTED_CLOSURE_SHA = (
    "f38d22ad829c11e720f5edbb4c27588f"
    "ea01ec0f829b7c4a70fa866582f6a093"
)

def fail(msg):
    print("FAIL|" + msg)
    raise SystemExit(1)

def sha(path):
    if not path.is_file():
        fail("MISSING|" + str(path))
    return hashlib.sha256(path.read_bytes()).hexdigest()

proc = subprocess.run(
    [
        "git", "-C", str(REPO),
        "status", "--porcelain=v1",
        "--untracked-files=all"
    ],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    check=False
)

if proc.returncode != 0:
    fail("GIT_STATUS")

if proc.stdout.strip():
    fail("REPOSITORY_NOT_CLEAN")

if STUDY.exists():
    fail("STUDY_ALREADY_EXISTS")

if sha(SCHEMA) != EXPECTED_SCHEMA_SHA:
    fail("ACTIVE_SCHEMA_V2_SHA")

if SCHEMA.stat().st_size != 43030:
    fail("ACTIVE_SCHEMA_V2_SIZE")

proc = subprocess.run(
    [
        "git", "-C", str(REPO),
        "rev-parse",
        "HEAD:config/schemas/protocol_specification.v2.schema.json"
    ],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    check=False
)

if proc.returncode != 0:
    fail("ACTIVE_SCHEMA_V2_BLOB_LOOKUP")

if proc.stdout.strip() != EXPECTED_SCHEMA_BLOB:
    fail("ACTIVE_SCHEMA_V2_BLOB")

if sha(CLOSURE) != EXPECTED_CLOSURE_SHA:
    fail("DECISION0101_CLOSURE_SHA")

auth = json.loads(AUTH.read_text(encoding="utf-8"))

if auth["status"] != "AUTHORIZED_FOR_AUTHORING_ONLY":
    fail("AUTHORIZATION_STATUS")

if auth["active_schema"]["sha256"] != EXPECTED_SCHEMA_SHA:
    fail("AUTH_SCHEMA_SHA")

if auth["active_schema"]["git_blob"] != EXPECTED_SCHEMA_BLOB:
    fail("AUTH_SCHEMA_BLOB")

if auth["active_schema"]["modification_authorized"] is not False:
    fail("SCHEMA_MODIFICATION_PREMATURE")

scope = auth["authorized_study_scope"]

for key in (
    "active_schema_v2_only",
    "relation_informed",
    "all_109_semantic_units_in_scope",
    "all_17_v4_losslessness_requirements_in_scope",
    "cross_unit_joint_coherence_required",
    "finite_admissible_composition_universe_required",
    "machine_readable_exhaustiveness_accounting_required",
    "structural_schema_constraints_required",
    "semantic_role_compatibility_required"
):
    if scope[key] is not True:
        fail("SCOPE|" + key)

relations = auth["relation_class_semantics"]

if relations["NOT_SEMANTICALLY_RELATED"] != \
        "EXCLUDED_FROM_ADMISSIBLE_SEMANTIC_STORAGE_COMPOSITIONS":
    fail("NEGATIVE_RELATION_POLICY")

if "MUST_NOT_BE_PROMOTED" not in relations["UNRESOLVED"]:
    fail("UNRESOLVED_POLICY")

domain = auth["required_domain_distinctions"]

if domain["vocabularies_must_not_be_equated_or_merged"] is not True:
    fail("VOCABULARY_DISTINCTION")

if domain["lexical_screening_is_not_semantic_proof"] is not True:
    fail("LEXICAL_SCREENING_POLICY")

for key, value in auth["carrier_semantics_constraints"].items():
    if value is not True:
        fail("CARRIER_CONSTRAINT|" + key)

if set(auth["global_allowed_outcomes"]) != {
    "POSITIVE_EXISTING_V2_MAPPING_WITNESS_IDENTIFIED",
    "NEGATIVE_EXISTING_V2_MAPPING_IMPOSSIBILITY_PROVEN",
    "FURTHER_EVIDENCE_REQUIRED"
}:
    fail("GLOBAL_OUTCOME_SET")

for key, value in auth["explicit_non_authorizations"].items():
    if value is not False:
        fail("UNEXPECTED_AUTHORIZATION|" + key)

expected_prohibited = {
    "generated_driver_source",
    "selected_sample_membership",
    "raw_model_responses",
    "compiler_log_semantic_contents",
    "gold_labels",
    "analyzer_output",
    "baseline_output",
    "llm_review_output",
    "repair_output"
}

if set(auth["prohibited_evidence"]) != expected_prohibited:
    fail("PROHIBITED_EVIDENCE_SET")

for key, value in auth["authorization_verifier_lifecycle"].items():
    if value is not True:
        fail("VERIFIER_LIFECYCLE|" + key)

print("DECISION_0101_REVIEW_CHAIN_BINDING=PASS")
print("ACTIVE_SCHEMA_V2_BINDING=PASS")
print("ACTIVE_SCHEMA_V2_SHA256=" + EXPECTED_SCHEMA_SHA)
print("ACTIVE_SCHEMA_V2_GIT_BLOB=" + EXPECTED_SCHEMA_BLOB)
print("STUDY_PREEXISTENCE=NO")
print("REPOSITORY_CLEAN=YES")
print("AUTHORIZED_SCOPE=AUTHORING_ONLY")
print("ACTIVE_SCHEMA_V2_ONLY=YES")
print("UNRESOLVED_POLICY=NOT_AUTOMATICALLY_POSITIVE")
print("NOT_SEMANTICALLY_RELATED_POLICY=EXCLUDED")
print("OPEN_STRING_STORAGE_IS_AUTOMATIC_LOSSLESSNESS_PROOF=NO")
print("TWO_57_ELEMENT_FIELD_CLASS_VOCABULARIES_EQUATED=NO")
print("OPERATIONAL_POSITIVE_MAPPING_AUTHORIZED=NO")
print("SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO")
print("CURL_JSON_AUTHORIZED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
print("RELATION_INFORMED_EXHAUSTIVE_ADMISSIBLE_COMPOSITION_STUDY_AUTHORING_AUTHORIZATION=PASS")
print("VERIFIER_LIFECYCLE=ONE_FINAL_RUN_IMMEDIATELY_BEFORE_STUDY_AUTHORING_THEN_PERMANENT_RETIREMENT")
