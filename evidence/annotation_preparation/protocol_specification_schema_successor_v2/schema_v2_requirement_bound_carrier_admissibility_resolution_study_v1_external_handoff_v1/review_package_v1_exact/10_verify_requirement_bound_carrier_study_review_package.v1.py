#!/usr/bin/env python3

import hashlib
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent

MANIFEST = HERE / "01_review_subject_manifest.v1.json"
SOURCE_MANIFEST = HERE / "02_portable_source_binding_manifest.v1.json"
PACKET = HERE / "03_RBCA01_RBCA08_reviewer_packet.BLANK.v1.md"
A02_OUT = HERE / "04_decision0139_a02_final_output.EXACT_COPY.v1.txt"
A02_CONS = HERE / "05_decision0139_a02_consumption_record.v1.json"
DEC0139 = HERE / "06_decision0139.EXACT_COPY.md"
DEC0138 = HERE / "07_decision0138.EXACT_COPY.md"
BUNDLE = HERE / "08_sealed_repository_checkpoint.bundle"
BUNDLE_MANIFEST = HERE / "09_sealed_repository_checkpoint_manifest.v1.json"
REPORT = HERE / "11_review_package_report.v1.md"
SUMS = HERE / "12_review_package_v1.SHA256SUMS"

STUDY = HERE / "study_v1_exact"
AUTH = HERE / "authorization_v1_exact"
PORTABLE = HERE / "portable_sources"

EXPECTED_DEC0139 = (
    "c9cf1bf0c9a3b59714e08f966f9c98acbd309fd7"
)

EXPECTED_STUDY_SAFE_SHA = (
    "cd712c15c80441d94b36c7b9ce84c90"
    "f53c2f4c87f5491c22ceb30932bf74644"
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

manifest = json.loads(
    MANIFEST.read_text(
        encoding="utf-8"
    )
)

if (
    manifest["package_status"]
    != "AUTHOR_CANDIDATE_AWAITING_INDEPENDENT_HUMAN_REVIEW"
):
    fail("PACKAGE_STATUS")

subject = manifest["review_subject"]

if subject["outcome"] != "FURTHER_EVIDENCE_REQUIRED":
    fail("SUBJECT_OUTCOME")

for key, expected in (
    ("requirement_count", 17),
    ("semantic_unit_count", 109),
    ("schema_v2_property_path_count", 171),
    ("historical_pair_count", 18639),
    ("admissible_exact_count", 0),
    ("admissible_composite_count", 0),
    ("no_admissible_carrier_proven_count", 0),
    ("unresolved_count", 17),
):
    if subject[key] != expected:
        fail("SUBJECT_ACCOUNTING|" + key)

if subject["requirement_to_semantic_unit_crosswalk_identified"] is not False:
    fail("CROSSWALK_STATE")

if subject["historical_pair_state_modified"] is not False:
    fail("PAIR_STATE")

if manifest["review_items"] != [
    "RBCA01",
    "RBCA02",
    "RBCA03",
    "RBCA04",
    "RBCA05",
    "RBCA06",
    "RBCA07",
    "RBCA08",
]:
    fail("REVIEW_ITEMS")

packet = PACKET.read_text(
    encoding="utf-8"
)

if packet.count(
    "Decision: `[PASS / REVISION_REQUIRED / FAIL]`"
) != 8:
    fail("BLANK_DECISION_COUNT")

for forbidden in (
    "Decision: `PASS`",
    "Decision: `REVISION_REQUIRED`",
    "Decision: `FAIL`",
    "Overall decision: `APPROVE_REQUIREMENT_BOUND_CARRIER_ADMISSIBILITY_RESOLUTION_STUDY_V1`",
):
    if forbidden in packet:
        fail("PREFILLED_DECISION")

lines = packet.splitlines()

for prefix in (
    "Human reviewer name:",
    "Human reviewer signature / recorded confirmation:",
    "Human reviewer date:",
):
    if [x for x in lines if x.startswith(prefix)] != [prefix]:
        fail("PREFILLED_REVIEWER_IDENTITY|" + prefix)

if manifest["review_packet"]["decision_present"] is not False:
    fail("DECISION_PRESENT_STATE")

if manifest["review_packet"]["human_review_performed"] is not False:
    fail("HUMAN_REVIEW_STATE")

cons = json.loads(
    A02_CONS.read_text(
        encoding="utf-8"
    )
)

if cons["final_run_result"] != "PASS":
    fail("A02_RESULT")

if cons["verifier_state_after_run"] != "PERMANENTLY_RETIRED":
    fail("A02_STATE")

if cons["rerun_authorized"] is not False:
    fail("A02_RERUN")

if cons["must_never_be_rerun"] is not True:
    fail("A02_RETIREMENT")

if sha(A02_OUT) != cons["final_output_sha256"]:
    fail("A02_OUTPUT_SHA")

if (
    "INDEPENDENT_HUMAN_REVIEW_PACKAGE_AUTHORING_AUTHORIZATION=PASS"
    not in A02_OUT.read_text(
        encoding="utf-8"
    )
):
    fail("A02_PASS_MARKER")

source_manifest = json.loads(
    SOURCE_MANIFEST.read_text(
        encoding="utf-8"
    )
)

if source_manifest["portable_source_count"] != 9:
    fail("PORTABLE_SOURCE_COUNT")

for record in source_manifest["records"]:
    rel = record["package_path"]
    path = HERE / rel

    if sha(path) != record["sha256"]:
        fail("PORTABLE_SOURCE_SHA|" + rel)

    if path.stat().st_size != record["size_bytes"]:
        fail("PORTABLE_SOURCE_SIZE|" + rel)

study_safe = (
    STUDY
    / "08_verify_requirement_bound_carrier_admissibility_resolution_study.v1.py"
)

if sha(study_safe) != EXPECTED_STUDY_SAFE_SHA:
    fail("STUDY_SAFE_SHA")

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

for marker in (
    "REQUIREMENT_BOUND_CARRIER_ADMISSIBILITY_RESOLUTION_STUDY_V1=PASS",
    "UNRESOLVED_COUNT=17",
    "STUDY_OUTCOME=FURTHER_EVIDENCE_REQUIRED",
    "CARRIER_ADMISSIBILITY_RESOLVED=NO",
    "POSITIVE_MAPPING_PROVEN=NO",
    "NEGATIVE_MAPPING_IMPOSSIBILITY_PROVEN=NO",
    "INDEPENDENT_HUMAN_REVIEW_REQUIRED=YES",
):
    if marker not in p.stdout:
        fail("STUDY_SAFE_MARKER|" + marker)

bundle_manifest = json.loads(
    BUNDLE_MANIFEST.read_text(
        encoding="utf-8"
    )
)

if (
    bundle_manifest["checkpoint_commit"]
    != EXPECTED_DEC0139
):
    fail("BUNDLE_CHECKPOINT")

if sha(BUNDLE) != bundle_manifest["bundle_sha256"]:
    fail("BUNDLE_SHA")

p = subprocess.run(
    ["git", "bundle", "list-heads", str(BUNDLE)],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    check=False,
)

if p.returncode != 0:
    fail("BUNDLE_LIST_HEADS")

if EXPECTED_DEC0139 not in p.stdout:
    fail("BUNDLE_CHECKPOINT_HEAD")

for key, value in manifest[
    "technical_nonclaims"
].items():
    if value is not False:
        fail("UNEXPECTED_TECHNICAL_CLAIM|" + key)

for key, value in manifest[
    "explicit_non_authorizations"
].items():
    if value is not False:
        fail("UNEXPECTED_AUTHORIZATION|" + key)

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

        path = HERE / rel

        if sha(path) != digest:
            fail("CHECKSUM|" + rel)

print("REQUIREMENT_BOUND_CARRIER_STUDY_REVIEW_PACKAGE_V1=PASS")
print("PACKAGE_STATUS=AUTHOR_CANDIDATE_AWAITING_INDEPENDENT_HUMAN_REVIEW")
print("REVIEW_ITEMS=RBCA01|RBCA02|RBCA03|RBCA04|RBCA05|RBCA06|RBCA07|RBCA08")
print("REQUIRED_REVIEWER_ROLE=Spec-Technical-Reviewer-1")
print("REVIEWER_PACKET_INITIAL_BLANK_STATE=PASS")
print("REVIEWER_DECISION_PRESENT=NO")
print("REVIEWER_DECISION_SYNTHESIZED=NO")
print("HUMAN_REVIEW_PERFORMED=NO")
print("PORTABLE_SOURCE_COUNT=9")
print("PORTABLE_SOURCE_RESOLVABILITY=PASS")
print("SEALED_REPOSITORY_CHECKPOINT_BUNDLE=PASS")
print("SEALED_BUNDLE_CHECKPOINT_COMMIT=" + EXPECTED_DEC0139)
print("SEALED_BUNDLE_CHECKPOINT_ROLE=DECISION_0139_PRE_REVIEW_PACKAGE_CHECKPOINT")
print("STUDY_OUTCOME_UNDER_REVIEW=FURTHER_EVIDENCE_REQUIRED")
print("UNRESOLVED_COUNT=17")
print("CARRIER_ADMISSIBILITY_RESOLVED=NO")
print("POSITIVE_MAPPING_PROVEN=NO")
print("NEGATIVE_MAPPING_IMPOSSIBILITY_PROVEN=NO")
print("WHOLE_V4_EXHAUSTIVENESS_PROVEN=NO")
print("STUDY_GOVERNANCE_ADOPTED=NO")
print("OPERATIONAL_MAPPING_AUTHORIZED=NO")
print("SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO")
print("CURL_JSON_AUTHORIZED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
print("DECISION_0139_A02_STATE=PERMANENTLY_RETIRED")
print("DECISION_0139_A02_EXECUTED_BY_SAFE_VERIFIER=NO")
print("RETIRED_A02_VERIFIERS_EXECUTED=NO")
