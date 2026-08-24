#!/usr/bin/env python3

import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]

BASE_REL = Path(
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2"
)

EXACT = (
    HERE
    / "01_completed_SUCR01_SUCR08_human_review.EXACT_COPY.v1.md"
)

RECORD = (
    HERE
    / "02_completed_human_review_record.v1.json"
)

SUMS = (
    HERE
    / "04_completed_human_review.v1.SHA256SUMS"
)

HANDOFF = (
    REPO
    / BASE_REL
    / "schema_v2_semantic_unit_carrier_admissibility_"
      "and_requirement_binding_study_v1_external_review_handoff_v1"
)

HANDOFF_MANIFEST = (
    HANDOFF
    / "06_external_handoff_manifest.v1.json"
)

HANDOFF_SAFE = (
    HANDOFF
    / "07_verify_external_review_handoff.v1.py"
)

HANDOFF_SUMS = (
    HANDOFF
    / "08_external_review_handoff.v1.SHA256SUMS"
)

DEC0115 = (
    REPO
    / "documentation/decisions/"
      "0115-record-external-independent-human-review-handoff-v1-author-checkpoint.md"
)

STUDY_ACC = (
    REPO
    / BASE_REL
    / "schema_v2_semantic_unit_carrier_admissibility_"
      "and_requirement_binding_study_v1"
    / "04_machine_readable_accounting.v1.json"
)

EXPECTED = {
    EXACT:
        "b41c4f737be70cf3de0f837f0f46b186a4d6ac12e7d49ad5e263bcddfb76f50a",

    HANDOFF_MANIFEST:
        "f3f5cb7f4bf5eb1cf68711c4c7a20bfb96d1df2d7cbd4b1c09cedbad836cd71d",

    HANDOFF_SAFE:
        "b049815f4fdaa11a29a7020e96e7be0ec0d653761f8d108a34146015255b829d",

    HANDOFF_SUMS:
        "961e540cca18976740d8af8c32a78538f48a2f36b399cda8468806a58852e0d9",

    DEC0115:
        "a816839bbb7f511e96ac38a1f0a9c4590f67bc11f5156f4ea56ccb3314a69e21",

    STUDY_ACC:
        "f271db56cdd680f85a14d8fe3d4a4b1e820b1bb5276215bd2ca8cb7486e307db",
}

def fail(msg):
    print(
        "FAIL|" + msg
    )
    raise SystemExit(1)

def sha(path):
    if not path.is_file():
        fail(
            "MISSING|" + str(path)
        )

    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()

for path, expected in EXPECTED.items():

    if sha(path) != expected:
        fail(
            "SOURCE_BINDING|"
            + str(path)
        )

b = EXACT.read_bytes()

if len(b) != 9603:
    fail(
        "COMPLETED_REVIEW_SIZE"
    )

if b.count(b"\r\n") != 81:
    fail(
        "COMPLETED_REVIEW_CRLF"
    )

if len(b.splitlines()) != 82:
    fail(
        "COMPLETED_REVIEW_LINES"
    )

text = b.decode("utf-8")

expected_decisions = {
    "SUCR01":
        "REVISION_REQUIRED",

    "SUCR02":
        "PASS",

    "SUCR03":
        "PASS",

    "SUCR04":
        "PASS",

    "SUCR05":
        "PASS",

    "SUCR06":
        "PASS",

    "SUCR07":
        "PASS",

    "SUCR08":
        "PASS",
}

for rid, expected in expected_decisions.items():

    m = re.search(
        rf"## {rid} —.*?"
        rf"Decision:\s*`([^`]+)`",
        text,
        flags=re.DOTALL,
    )

    if not m:
        fail(
            "MISSING_DECISION|"
            + rid
        )

    actual = m.group(1).strip()

    if actual != expected:
        fail(
            "DECISION|"
            + rid
            + "|"
            + actual
        )

m = re.search(
    r"^Overall decision:\s*`([^`]+)`\s*$",
    text,
    flags=re.MULTILINE,
)

if not m:
    fail(
        "OVERALL_DECISION_MISSING"
    )

if m.group(1).strip() != \
        "REVISION_REQUIRED":
    fail(
        "OVERALL_DECISION"
    )

required_fields = {
    "Human reviewer name":
        "Abdul Raheem Shahzad",

    "Human reviewer signature / recorded confirmation":
        "ARS",

    "Human reviewer date":
        "24 / August / 2026",

    "Reviewer role":
        "Spec-Technical-Reviewer-1",
}

for label, expected in required_fields.items():

    m = re.search(
        rf"^{re.escape(label)}:\s*(.+?)\s*$",
        text,
        flags=re.MULTILINE,
    )

    if not m:
        fail(
            "MISSING_REVIEWER_FIELD|"
            + label
        )

    if m.group(1).strip() != expected:
        fail(
            "REVIEWER_FIELD|"
            + label
        )

record = json.loads(
    RECORD.read_text(
        encoding="utf-8"
    )
)

if record[
    "status"
] != "COMPLETED_HUMAN_REVIEW_RECORDED_REVISION_REQUIRED_NOT_GOVERNANCE_ADOPTED":
    fail(
        "RECORD_STATUS"
    )

review = record[
    "completed_review"
]

if review[
    "item_decisions"
] != expected_decisions:
    fail(
        "RECORDED_ITEM_DECISIONS"
    )

if review[
    "overall_decision"
] != "REVISION_REQUIRED":
    fail(
        "RECORDED_OVERALL_DECISION"
    )

interp = record[
    "review_interpretation"
]

if interp[
    "review_chain_closed"
] is not False:
    fail(
        "PREMATURE_REVIEW_CHAIN_CLOSURE"
    )

if interp[
    "study_approved"
] is not False:
    fail(
        "PREMATURE_STUDY_APPROVAL"
    )

if interp[
    "governance_adopted"
] is not False:
    fail(
        "PREMATURE_GOVERNANCE_ADOPTION"
    )

if interp[
    "sucr01_corrective_action_required"
] is not True:
    fail(
        "SUCR01_CORRECTIVE_REQUIREMENT"
    )

if interp[
    "sucr01_corrective_scope"
] != "SOURCE_EVIDENCE_PORTABILITY_AND_RESOLVABILITY":
    fail(
        "SUCR01_CORRECTIVE_SCOPE"
    )

if interp[
    "original_overall_review_remains"
] != "REVISION_REQUIRED":
    fail(
        "ORIGINAL_OVERALL_REVIEW_STATE"
    )

if interp[
    "bounded_technical_outcome_remains"
] != "FURTHER_EVIDENCE_REQUIRED":
    fail(
        "BOUNDED_OUTCOME"
    )

corrective = record[
    "corrective_package_state"
]

for key, value in corrective.items():

    if value is not False:
        fail(
            "PREMATURE_CORRECTIVE_STATE|"
            + key
        )

for key, value in record[
    "technical_nonclaims"
].items():

    if value is not False:
        fail(
            "UNEXPECTED_TECHNICAL_PERMISSION|"
            + key
        )

for key, value in record[
    "retired_verifiers"
].items():

    if value != \
            "PERMANENTLY_RETIRED":
        fail(
            "RETIRED_VERIFIER_STATE|"
            + key
        )

study = json.loads(
    STUDY_ACC.read_text(
        encoding="utf-8"
    )
)

if study["status"] != \
        "AUTHOR_CANDIDATE":
    fail(
        "STUDY_STATUS"
    )

if study["global_outcome"] != \
        "FURTHER_EVIDENCE_REQUIRED":
    fail(
        "STUDY_OUTCOME"
    )

if SUMS.is_file():

    lines = [
        line
        for line in SUMS.read_text(
            encoding="utf-8"
        ).splitlines()
        if line.strip()
    ]

    if len(lines) != 3:
        fail(
            "CHECKSUM_ENTRY_COUNT|"
            + str(len(lines))
        )

    for line in lines:

        digest, rel = line.split(
            None,
            1,
        )

        rel = rel.strip().lstrip("*")
        target = HERE / rel

        if sha(target) != digest:
            fail(
                "CHECKSUM|"
                + rel
            )

print("COMPLETED_HUMAN_REVIEW_EXACT_BINDING=PASS")

print("SUCR01_DECISION=REVISION_REQUIRED")
print("SUCR02_DECISION=PASS")
print("SUCR03_DECISION=PASS")
print("SUCR04_DECISION=PASS")
print("SUCR05_DECISION=PASS")
print("SUCR06_DECISION=PASS")
print("SUCR07_DECISION=PASS")
print("SUCR08_DECISION=PASS")

print("OVERALL_REVIEW_DECISION=REVISION_REQUIRED")

print("HUMAN_REVIEWER=Abdul Raheem Shahzad")
print("HUMAN_REVIEWER_CONFIRMATION=ARS")
print("HUMAN_REVIEWER_DATE=24 / August / 2026")
print("HUMAN_REVIEWER_ROLE=Spec-Technical-Reviewer-1")

print("SUCR01_CORRECTIVE_ACTION_REQUIRED=YES")
print("SUCR01_CORRECTIVE_SCOPE=SOURCE_EVIDENCE_PORTABILITY_AND_RESOLVABILITY")
print("SUCR02_SUCR08_ORIGINAL_PASS_FINDINGS_PRESERVED=YES")

print("ORIGINAL_OVERALL_REVIEW_REMAINS=REVISION_REQUIRED")
print("REVIEW_CHAIN_CLOSED=NO")

print("STUDY_STATUS=AUTHOR_CANDIDATE")
print("GLOBAL_OUTCOME=FURTHER_EVIDENCE_REQUIRED")
print("STUDY_GOVERNANCE_ADOPTED=NO")

print("POSITIVE_EXISTING_V2_MAPPING_PROVEN=NO")
print("NEGATIVE_EXISTING_V2_MAPPING_IMPOSSIBILITY_PROVEN=NO")
print("WHOLE_V4_ADMISSIBLE_COMPOSITION_EXHAUSTIVENESS_PROVEN=NO")

print("OPERATIONAL_MAPPING_AUTHORIZED=NO")
print("SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO")
print("CURL_JSON_AUTHORIZED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")

print("RETIRED_A02_VERIFIERS_EXECUTED=NO")

print(
    "REPOSITORY_COMPLETED_SUCR01_SUCR08_HUMAN_REVIEW=PASS"
)
