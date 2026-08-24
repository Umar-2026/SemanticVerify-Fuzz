#!/usr/bin/env python3

import hashlib
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]

AUTH = HERE / "01_independent_human_review_package_authorization.v1.json"
SUMS = HERE / "03_independent_human_review_package_authorization.v1.SHA256SUMS"

BASE_REL = "evidence/annotation_preparation/protocol_specification_schema_successor_v2"

STUDY_REL = (
    BASE_REL
    + "/schema_v2_v4_losslessness_requirement_provenance_binding_resolution_study_v1"
)

STUDY = REPO / STUDY_REL

EXPECTED_STUDY_TREE = (
    "ee85980dcff85b5be3f21995f578b3b78cf39aa2"
)

EXPECTED_CANONICAL_SHA = (
    "c869079bfbd395b479e2dd8f2f1bcc31"
    "aabeababe0e24fc1542c6d35d210602e"
)

def fail(msg):
    print("FAIL|" + msg)
    raise SystemExit(1)

def sha(path):
    if not path.is_file():
        fail("MISSING|" + str(path))
    return hashlib.sha256(path.read_bytes()).hexdigest()

def git(args):
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

if git(["rev-parse", "HEAD:" + STUDY_REL]) != EXPECTED_STUDY_TREE:
    fail("STUDY_GIT_TREE")

if git(["status", "--porcelain=v1", "--untracked-files=all"]):
    fail("REPOSITORY_NOT_CLEAN")

auth = json.loads(
    AUTH.read_text(encoding="utf-8")
)

if auth["status"] != "AUTHORIZED_NOT_YET_AUTHORED":
    fail("AUTHORIZATION_STATUS")

if (
    auth["authorization_type"]
    != "PRE_INDEPENDENT_HUMAN_REVIEW_PACKAGE_AUTHORING_ONLY"
):
    fail("AUTHORIZATION_TYPE")

subject = auth["review_subject"]

if subject["status"] != "AUTHOR_CANDIDATE":
    fail("SUBJECT_STATUS")

if subject["requirement_count"] != 17:
    fail("REQUIREMENT_COUNT")

if subject["bound_exact_count"] != 17:
    fail("BOUND_EXACT_COUNT")

if subject["bound_composite_count"] != 0:
    fail("BOUND_COMPOSITE_COUNT")

if subject["unresolved_count"] != 0:
    fail("UNRESOLVED_COUNT")

if subject["study_outcome"] != "REQUIREMENT_PROVENANCE_RESOLVED":
    fail("STUDY_OUTCOME")

if (
    subject["outcome_scope"]
    != "REQUIREMENT_IDENTITY_AND_SOURCE_PROVENANCE_ONLY"
):
    fail("OUTCOME_SCOPE")

if (
    subject["canonical_losslessness_object_sha256"]
    != EXPECTED_CANONICAL_SHA
):
    fail("CANONICAL_LOSSLESSNESS_SHA")

if auth["required_reviewer_role"] != "Spec-Technical-Reviewer-1":
    fail("REVIEWER_ROLE")

expected_items = {
    "RPR01",
    "RPR02",
    "RPR03",
    "RPR04",
    "RPR05",
    "RPR06",
    "RPR07",
    "RPR08",
}

if set(auth["review_items"]) != expected_items:
    fail("REVIEW_ITEM_SET")

if (
    auth["review_package_requirements"][
        "reviewer_decision_must_not_be_synthesized"
    ]
    is not True
):
    fail("NO_SYNTHETIC_REVIEWER_DECISION")

for key, value in auth["explicit_non_authorizations"].items():
    if value is not False:
        fail("UNEXPECTED_AUTHORIZATION|" + key)

if (
    auth["retired_verifier_constraints"][
        "decision_0126_a02_rerun"
    ]
    is not False
):
    fail("DECISION0126_A02_RERUN")

study_safe = (
    STUDY
    / "07_verify_v4_losslessness_requirement_provenance_binding_resolution_study.v1.py"
)

p = subprocess.run(
    ["python3", str(study_safe)],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    check=False,
)

if p.returncode != 0:
    fail(
        "STUDY_SAFE_VERIFIER|"
        + p.stdout
        + p.stderr
    )

if (
    "V4_LOSSLESSNESS_REQUIREMENT_PROVENANCE_BINDING_RESOLUTION_STUDY_V1=PASS"
    not in p.stdout
):
    fail("STUDY_SAFE_PASS_MARKER")

if SUMS.is_file():
    for line in SUMS.read_text(
        encoding="utf-8"
    ).splitlines():

        if not line.strip():
            continue

        digest, rel = line.split(None, 1)
        rel = rel.strip().lstrip("*")

        if sha(HERE / rel) != digest:
            fail("CHECKSUM|" + rel)

print("DECISION_0127_STUDY_BINDING=PASS")
print("REQUIREMENT_COUNT=17")
print("BOUND_EXACT_COUNT=17")
print("BOUND_COMPOSITE_COUNT=0")
print("UNRESOLVED_COUNT=0")
print("STUDY_OUTCOME=REQUIREMENT_PROVENANCE_RESOLVED")
print(
    "OUTCOME_SCOPE="
    "REQUIREMENT_IDENTITY_AND_SOURCE_PROVENANCE_ONLY"
)
print("REVIEW_ITEMS=RPR01|RPR02|RPR03|RPR04|RPR05|RPR06|RPR07|RPR08")
print("REQUIRED_REVIEWER_ROLE=Spec-Technical-Reviewer-1")
print("REVIEWER_DECISION_SYNTHESIS_AUTHORIZED=NO")
print("STUDY_GOVERNANCE_ADOPTION_AUTHORIZED=NO")
print("SEMANTIC_UNIT_CARRIER_PAIR_RECLASSIFICATION_AUTHORIZED=NO")
print("POSITIVE_MAPPING_WITNESS_AUTHORIZED=NO")
print("NEGATIVE_MAPPING_IMPOSSIBILITY_PROOF_AUTHORIZED=NO")
print("WHOLE_V4_EXHAUSTIVENESS_CLAIM_AUTHORIZED=NO")
print("OPERATIONAL_MAPPING_AUTHORIZED=NO")
print("ACTIVE_SCHEMA_V2_MODIFICATION_AUTHORIZED=NO")
print("SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO")
print("SCHEMA_VERSION_PRESELECTED=NO")
print("SCHEMA_V3_CREATED=NO")
print("CURL_JSON_AUTHORIZED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
print("DECISION_0126_A02_STATE=PERMANENTLY_RETIRED")
print("DECISION_0126_A02_EXECUTED_BY_THIS_VERIFIER=NO")
print("RETIRED_A02_VERIFIERS_EXECUTED=NO")
print(
    "INDEPENDENT_HUMAN_REVIEW_PACKAGE_AUTHORING_AUTHORIZATION=PASS"
)
print(
    "VERIFIER_LIFECYCLE="
    "ONE_FINAL_RUN_IMMEDIATELY_BEFORE_REVIEW_PACKAGE_AUTHORING_THEN_PERMANENT_RETIREMENT"
)
