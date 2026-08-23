#!/usr/bin/env python3

import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]

REVIEW = (
    HERE
    / "04_completed_csr01_csr08_human_review.EXACT_COPY.v1.md"
)

RECORD = (
    HERE
    / "05_completed_csr01_csr08_human_review_record.EXACT_COPY.v1.json"
)

AUTH = (
    REPO
    / "evidence/annotation_preparation/protocol_specification_schema_successor_v2"
    / "schema_v2_capability_study_v1_completed_human_review_repository_record_authorization"
    / "01_completed_capability_study_v1_human_review_repository_record_authorization.v1.json"
)

DEC0087 = (
    REPO
    / "documentation/decisions/0087-authorize-recording-completed-capability-study-v1-human-review.md"
)

EXPECTED_REVIEW_SHA = \
    "355de778d41ab0648ef84150c37c6c162725b41582144cb028525b87e25e2856"

EXPECTED_RECORD_SHA = \
    "72d8482899c160209f5f2f91f1aeb973ed06b8d72c079a424160516c66086442"

EXPECTED_AUTH_SHA = \
    "69a2874299977d294e7e8584431efc766b9e4b73f1e9eede3aff262331c43085"

EXPECTED_DEC0087_SHA = \
    "5f3b9c040d33789b6e70a9db412075e0c16bbd67f9ee29a1c89c8233a84c4768"


def fail(msg):
    print("FAIL|" + msg)
    raise SystemExit(1)


def sha(path):
    if not path.is_file():
        fail(
            "MISSING|" + str(path)
        )

    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()


if sha(REVIEW) != EXPECTED_REVIEW_SHA:
    fail("COMPLETED_REVIEW_SHA")

if sha(RECORD) != EXPECTED_RECORD_SHA:
    fail("COMPLETED_RECORD_SHA")

if sha(AUTH) != EXPECTED_AUTH_SHA:
    fail("AUTHORIZATION_SHA")

if sha(DEC0087) != EXPECTED_DEC0087_SHA:
    fail("DECISION_0087_SHA")

text = REVIEW.read_text(
    encoding="utf-8"
)

required_pre = (
    "Before reviewer editing, the manual-review copy was byte-identical "
    "to the immutable blank packet, as established by the one-time "
    "initial blank-state verification and its consumption marker."
)

required_post = (
    "After reviewer completion, the manual-review copy is expected to "
    "differ from the blank packet because the review decisions, notes, "
    "and reviewer identity fields have been filled in."
)

if required_pre not in text:
    fail("CSR01_PRE_EDIT_WORDING")

if required_post not in text:
    fail("CSR01_POST_EDIT_WORDING")

decisions = re.findall(
    r"^Decision \(PASS / REVISION_REQUIRED / FAIL\):\s*"
    r"(PASS|REVISION_REQUIRED|FAIL)\s*$",
    text,
    flags=re.MULTILINE,
)

if decisions != ["PASS"] * 8:
    fail("CSR_DECISIONS")

overall = re.findall(
    r"^Overall decision "
    r"\(APPROVE_SCHEMA_V2_CAPABILITY_STUDY_V1 / "
    r"REVISION_REQUIRED / FAIL\):\s*"
    r"(APPROVE_SCHEMA_V2_CAPABILITY_STUDY_V1|"
    r"REVISION_REQUIRED|FAIL)\s*$",
    text,
    flags=re.MULTILINE,
)

if overall != [
    "APPROVE_SCHEMA_V2_CAPABILITY_STUDY_V1"
]:
    fail("OVERALL_DECISION")

record = json.loads(
    RECORD.read_text(
        encoding="utf-8"
    )
)

if record[
    "status"
] != "COMPLETED_INDEPENDENT_HUMAN_TECHNICAL_REVIEW_VALIDATED":
    fail("RECORD_STATUS")

d = record[
    "human_review_decisions"
]

for rid in (
    "CSR01",
    "CSR02",
    "CSR03",
    "CSR04",
    "CSR05",
    "CSR06",
    "CSR07",
    "CSR08",
):
    if d[rid] != "PASS":
        fail(rid)

if d[
    "overall"
] != "APPROVE_SCHEMA_V2_CAPABILITY_STUDY_V1":
    fail("RECORD_OVERALL")

identity = record[
    "reviewer_identity"
]

if identity != {
    "human_reviewer_confirmation":
        "ARS",

    "human_reviewer_date":
        "22 / August / 2026",

    "human_reviewer_name":
        "Abdul Raheem Shahzad",

    "reviewer_role":
        "Spec-Technical-Reviewer-1",
}:
    fail("REVIEWER_IDENTITY")

approval = record[
    "bounded_human_approval"
]

if approval[
    "capability_study_v1_human_approved"
] is not True:
    fail("STUDY_APPROVAL")

if approval[
    "further_evidence_required_human_approved"
] is not True:
    fail("FER_APPROVAL")

for key in (
    "positive_existing_v2_mapping_path_human_proven",
    "negative_existing_v2_mapping_impossibility_human_proven",
    "admissible_composition_exhaustiveness_human_established",
    "operational_positive_mapping_contract_authorized",
    "schema_successor_authoring_authorized",
    "schema_version_preselected",
    "schema_v3_created",
    "curl_json_created",
    "analyzer_implementation_authorized",
    "analyzer_execution_authorized",
    "baseline_execution_authorized",
    "repair_authorized",
):
    if approval[key] is not False:
        fail(
            "BOUNDED_APPROVAL|" + key
        )

for forbidden in (
    REPO
    / "config/protocol_specifications/curl.json",

    REPO
    / "config/annotation/curl_positive_v4_to_v2_mapping_contract.v1.json",

    REPO
    / "config/annotation/curl_positive_v4_to_successor_mapping_contract.v1.json",

    REPO
    / "config/schemas/protocol_specification.v3.schema.json",
):
    if forbidden.exists():
        fail(
            "FORBIDDEN_ARTIFACT|"
            + str(forbidden)
        )

print("CSR01=PASS")
print("CSR02=PASS")
print("CSR03=PASS")
print("CSR04=PASS")
print("CSR05=PASS")
print("CSR06=PASS")
print("CSR07=PASS")
print("CSR08=PASS")

print(
    "OVERALL_HUMAN_DECISION="
    "APPROVE_SCHEMA_V2_CAPABILITY_STUDY_V1"
)

print("CAPABILITY_STUDY_V1_HUMAN_APPROVED=YES")
print("FURTHER_EVIDENCE_REQUIRED_HUMAN_APPROVED=YES")

print("POSITIVE_EXISTING_V2_MAPPING_PATH_PROVEN=NO")
print("NEGATIVE_EXISTING_V2_MAPPING_PATH_IMPOSSIBILITY_PROVEN=NO")
print("ADMISSIBLE_COMPOSITION_EXHAUSTIVENESS_ESTABLISHED=NO")

print("OPERATIONAL_POSITIVE_MAPPING_CONTRACT_AUTHORIZED=NO")
print("SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO")
print("SCHEMA_VERSION_PRESELECTED=NO")
print("SCHEMA_V3_CREATED=NO")
print("CURL_JSON_CREATED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")

print(
    "REPOSITORY_COMPLETED_CAPABILITY_STUDY_V1_HUMAN_REVIEW_RECORD=PASS"
)
