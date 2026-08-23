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
    + "/schema_v2_relation_informed_exhaustive_"
      "admissible_composition_study_v1"
)

STUDY = REPO / STUDY_REL

REVIEW_PACKAGE = (
    REPO
    / BASE_REL
    / "schema_v2_relation_informed_exhaustive_"
      "admissible_composition_study_v1_review_package_v1"
)

AUTH = (
    HERE
    / "01_relation_informed_study_v1_review_package_authorization.v1.json"
)

STUDY_JSON = (
    STUDY
    / "01_relation_informed_exhaustive_admissible_composition_study.v1.json"
)

ACCOUNTING = (
    STUDY
    / "02_exhaustiveness_accounting.v1.json"
)

REPORT = (
    STUDY
    / "03_study_report.v1.md"
)

OLD_A02_OUTPUT = (
    STUDY
    / "04_authorization_verifier_final_output.EXACT_COPY.v1.txt"
)

OLD_A02_CONSUMPTION = (
    STUDY
    / "05_authorization_verifier_consumption_record.v1.json"
)

SAFE_STUDY_VERIFIER = (
    STUDY
    / "06_verify_relation_informed_exhaustive_admissible_composition_study.v1.py"
)

STUDY_SUMS = (
    STUDY
    / "07_relation_informed_exhaustive_admissible_composition_study.v1.SHA256SUMS"
)

EXPECTED = {
    STUDY_JSON:
        "a8d28b09e78e1466eb5bb0991289879b28b10abd1dd1f9197d138ca723718f6f",

    ACCOUNTING:
        "ae56e06b6668c301167efdd7e81ba937848446215b49be52d1268c69a2c5d643",

    REPORT:
        "d0de61d7285ae8ba2c3ff2fcf2048f8c8dca145f87929a93262ab26c2e4b2642",

    OLD_A02_OUTPUT:
        "82cd248d4d323b691c8635ba9d1b992dfe4dbe0de7033b7a9eb92f0f4ce4bb50",

    OLD_A02_CONSUMPTION:
        "022a8c1fa5f6630261a91e815c1c9339037188b103ae97634a8b7a48c03a2753",

    SAFE_STUDY_VERIFIER:
        "b0ff1cb58eee830aa97c2759b54c78a96c9190c3c173a59483ee459bce8e8d22",

    STUDY_SUMS:
        "aa58e9221db7fa0c2bc17b2831e051ce6d7574c000d35d4f92c26ae923340140",
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

# ------------------------------------------------------------
# Repository clean and review package absent.
# ------------------------------------------------------------

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

if REVIEW_PACKAGE.exists():
    fail("REVIEW_PACKAGE_ALREADY_EXISTS")

# ------------------------------------------------------------
# Immutable study bindings.
# ------------------------------------------------------------

for path, expected in EXPECTED.items():
    if sha(path) != expected:
        fail(
            "STUDY_SHA|"
            + str(path)
        )

proc = subprocess.run(
    [
        "git",
        "-C",
        str(REPO),
        "rev-parse",
        "HEAD:" + STUDY_REL,
    ],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    check=False,
)

if proc.returncode != 0:
    fail("STUDY_GIT_TREE_LOOKUP")

if proc.stdout.strip() != \
        "bb55744db442f718daa56f8f38733e3ef4819b1a":
    fail("STUDY_GIT_TREE_CHANGED")

# ------------------------------------------------------------
# Run ONLY safe Study V1 verifier.
# Never execute Decision-0102 A02.
# ------------------------------------------------------------

proc = subprocess.run(
    [
        "python3",
        str(SAFE_STUDY_VERIFIER),
    ],
    cwd=str(STUDY),
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    check=False,
)

if proc.returncode != 0:
    fail(
        "STUDY_SAFE_VERIFIER_RC|"
        + str(proc.returncode)
    )

if (
    b"RELATION_INFORMED_EXHAUSTIVE_ADMISSIBLE_COMPOSITION_STUDY_V1=PASS"
    not in proc.stdout
):
    fail("STUDY_SAFE_VERIFIER_PASS_MARKER")

# ------------------------------------------------------------
# Study semantic state.
# ------------------------------------------------------------

study = json.loads(
    STUDY_JSON.read_text(
        encoding="utf-8"
    )
)

if study["status"] != "AUTHOR_CANDIDATE":
    fail("STUDY_STATUS")

if study["global_outcome"] != \
        "FURTHER_EVIDENCE_REQUIRED":
    fail("STUDY_OUTCOME")

if study["relation_classification_totals"] != {
    "SEMANTICALLY_RELATED": 113,
    "NOT_SEMANTICALLY_RELATED": 969,
    "UNRESOLVED": 8665,
}:
    fail("RELATION_TOTALS")

bindings = study["approved_input_bindings"]

if bindings["relation_pair_count"] != 9747:
    fail("RELATION_PAIR_COUNT")

if bindings["semantic_unit_count"] != 109:
    fail("SEMANTIC_UNIT_COUNT")

if bindings["source_leaf_record_count"] != 531:
    fail("LEAF_COUNT")

if len(
    study["losslessness_requirement_results"]
) != 17:
    fail("REQUIREMENT_COUNT")

accounting = study["exhaustiveness_accounting"]

if accounting[
    "whole_v4_admissible_composition_universe_proven_complete"
] is not False:
    fail("WHOLE_V4_EXHAUSTIVENESS_OVERCLAIM")

rules = study["admissibility_rules"]

if rules[
    "matrix_and_unit_field_class_vocabularies_equated"
] is not False:
    fail("FIELD_CLASS_VOCABULARY_MERGE")

if rules["unresolved"] != \
        "NOT_AUTOMATICALLY_POSITIVE":
    fail("UNRESOLVED_POLICY")

technical = study["technical_nonclaims"]

for key in (
    "positive_existing_v2_mapping_witness_identified",
    "negative_existing_v2_mapping_impossibility_proven",
    "whole_v4_admissible_composition_exhaustiveness_established",
    "operational_mapping_authorized",
    "schema_successor_authoring_authorized",
):
    if technical[key] is not False:
        fail(
            "UNSUPPORTED_TECHNICAL_CLAIM|"
            + key
        )

# ------------------------------------------------------------
# Decision-0102 A02 retirement evidence.
# ------------------------------------------------------------

consumption = json.loads(
    OLD_A02_CONSUMPTION.read_text(
        encoding="utf-8"
    )
)

if consumption[
    "verifier_state_after_run"
] != "PERMANENTLY_RETIRED":
    fail("OLD_A02_NOT_RETIRED")

if consumption[
    "must_never_be_rerun"
] is not True:
    fail("OLD_A02_RERUN_GUARD")

# ------------------------------------------------------------
# Review-package authorization semantics.
# ------------------------------------------------------------

auth = json.loads(
    AUTH.read_text(
        encoding="utf-8"
    )
)

if auth["status"] != \
        "AUTHORIZED_FOR_REVIEW_PACKAGE_AUTHORING_ONLY":
    fail("AUTH_STATUS")

if auth["required_reviewer_role"] != \
        "Spec-Technical-Reviewer-1":
    fail("REVIEWER_ROLE")

ids = [
    x["id"]
    for x in auth["required_review_items"]
]

if ids != [
    "RIAC01",
    "RIAC02",
    "RIAC03",
    "RIAC04",
    "RIAC05",
    "RIAC06",
    "RIAC07",
    "RIAC08",
]:
    fail("REVIEW_ITEM_IDS")

if auth["item_decision_values"] != [
    "PASS",
    "REVISION_REQUIRED",
    "FAIL",
]:
    fail("ITEM_DECISION_VALUES")

if auth["overall_decision_values"] != [
    "APPROVE_RELATION_INFORMED_EXHAUSTIVE_ADMISSIBLE_COMPOSITION_STUDY_V1",
    "REVISION_REQUIRED",
    "FAIL",
]:
    fail("OVERALL_DECISION_VALUES")

independence = auth[
    "reviewer_independence_requirements"
]

for key, value in independence.items():
    if value is not True:
        fail(
            "REVIEWER_INDEPENDENCE|" + key
        )

for key, value in auth[
    "explicit_non_authorizations"
].items():
    if value is not False:
        fail(
            "UNEXPECTED_AUTHORIZATION|" + key
        )

expected_prohibited = {
    "generated_driver_source",
    "selected_sample_membership",
    "raw_model_responses",
    "compiler_log_semantic_contents",
    "gold_labels",
    "analyzer_output",
    "baseline_output",
    "llm_review_output",
    "repair_output",
}

if set(auth["prohibited_evidence"]) != \
        expected_prohibited:
    fail("PROHIBITED_EVIDENCE_SET")

life = auth[
    "authorization_verifier_lifecycle"
]

for key, value in life.items():
    if value is not True:
        fail(
            "VERIFIER_LIFECYCLE|" + key
        )

print("DECISION_0103_STUDY_BINDING=PASS")
print("STUDY_STATUS=AUTHOR_CANDIDATE")
print("GLOBAL_OUTCOME=FURTHER_EVIDENCE_REQUIRED")

print("RIAC01_REQUIRED=YES")
print("RIAC02_REQUIRED=YES")
print("RIAC03_REQUIRED=YES")
print("RIAC04_REQUIRED=YES")
print("RIAC05_REQUIRED=YES")
print("RIAC06_REQUIRED=YES")
print("RIAC07_REQUIRED=YES")
print("RIAC08_REQUIRED=YES")

print("REQUIRED_REVIEWER_ROLE=Spec-Technical-Reviewer-1")
print("REVIEWER_DECISIONS_PREPOPULATED=NO")
print("REVIEWER_IDENTITY_PREPOPULATED=NO")

print("DECISION_0102_A02_EXECUTED=NO")
print("DECISION_0102_A02_STATE=PERMANENTLY_RETIRED")

print("STUDY_GOVERNANCE_ADOPTED=NO")
print("OPERATIONAL_POSITIVE_MAPPING_AUTHORIZED=NO")
print("SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO")
print("CURL_JSON_AUTHORIZED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")

print("INDEPENDENT_HUMAN_REVIEW_PACKAGE_AUTHORING_AUTHORIZATION=PASS")
print("VERIFIER_LIFECYCLE=ONE_FINAL_RUN_IMMEDIATELY_BEFORE_REVIEW_PACKAGE_AUTHORING_THEN_PERMANENT_RETIREMENT")
