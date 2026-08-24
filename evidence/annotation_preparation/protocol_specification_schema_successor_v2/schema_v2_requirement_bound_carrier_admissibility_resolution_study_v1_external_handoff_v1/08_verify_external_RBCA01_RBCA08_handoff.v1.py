#!/usr/bin/env python3

import hashlib
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent

MANIFEST = HERE / "01_external_handoff_manifest.v1.json"
INSTRUCTIONS = HERE / "02_external_reviewer_instructions.v1.md"
PACKET = HERE / "03_RBCA01_RBCA08_reviewer_packet.INITIAL_BLANK_EXACT_COPY.v1.md"
A02_OUT = HERE / "04_decision0141_a02_final_output.EXACT_COPY.v1.txt"
A02_CONS = HERE / "05_decision0141_a02_consumption_record.v1.json"
DEC0141 = HERE / "06_decision0141.EXACT_COPY.md"
DEC0140 = HERE / "07_decision0140.EXACT_COPY.md"
SUMS = HERE / "09_external_handoff_v1.SHA256SUMS"

PACKAGE = HERE / "review_package_v1_exact"
AUTH = HERE / "decision0141_authorization_exact"

PACKAGE_PACKET = (
    PACKAGE
    / "03_RBCA01_RBCA08_reviewer_packet.BLANK.v1.md"
)

PACKAGE_SAFE = (
    PACKAGE
    / "10_verify_requirement_bound_carrier_study_review_package.v1.py"
)

PACKAGE_SUMS = (
    PACKAGE
    / "12_review_package_v1.SHA256SUMS"
)

AUTH_SUMS = (
    AUTH
    / "03_external_independent_human_review_handoff_authorization.v1.SHA256SUMS"
)

EXPECTED_BLANK_SHA = (
    "4b0df835c5bfd59f2d023204f5a1a2ede11a293d7168f862413777ccd846210b"
)

EXPECTED_BLANK_SIZE = 4134

EXPECTED_DEC0141_SHA = (
    "28386d2ca2ef9c36b7f8524cb681f5866bb29ca5e5ee7da85500baf8ff2fe59a"
)

EXPECTED_DEC0140_SHA = (
    "8f63f34ef6c991c6b7332d2bc2d843ca6662da2b92c30e9813bb8f446781aac9"
)

EXPECTED_PACKAGE_SAFE_SHA = (
    "db1f315a2a5c37821007e705bba9d8e2addaee21c49d87c1f837c45067d20397"
)

EXPECTED_BUNDLE_CHECKPOINT = (
    "c9cf1bf0c9a3b59714e08f966f9c98acbd309fd7"
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

def verify_sums(root, sums):
    if not sums.is_file():
        fail("MISSING_SUMS|" + str(sums))

    for line in sums.read_text(
        encoding="utf-8"
    ).splitlines():

        if not line.strip():
            continue

        digest, rel = line.split(
            None,
            1,
        )

        rel = rel.strip().lstrip("*")
        target = root / rel

        if sha(target) != digest:
            fail("CHECKSUM|" + str(target))

manifest = json.loads(
    MANIFEST.read_text(
        encoding="utf-8"
    )
)

if (
    manifest["handoff_status"]
    != "AWAITING_EXTERNAL_INDEPENDENT_HUMAN_REVIEW"
):
    fail("HANDOFF_STATUS")

subject = manifest["review_subject"]

if subject["review_items"] != [
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

if (
    subject["required_reviewer_role"]
    != "Spec-Technical-Reviewer-1"
):
    fail("REVIEWER_ROLE")

if (
    subject["author_candidate_outcome"]
    != "FURTHER_EVIDENCE_REQUIRED"
):
    fail("SUBJECT_OUTCOME")

if subject["unresolved_count"] != 17:
    fail("UNRESOLVED_COUNT")

blank = manifest[
    "reviewer_packet_initial_state"
]

if blank["state"] != "BLANK":
    fail("BLANK_PACKET_STATE")

if blank["human_review_performed"] is not False:
    fail("HUMAN_REVIEW_STATE")

if blank["reviewer_decision_present"] is not False:
    fail("REVIEWER_DECISION_STATE")

if blank["reviewer_decision_synthesized"] is not False:
    fail("REVIEWER_DECISION_SYNTHESIS")

if blank["reviewer_identity_present"] is not False:
    fail("REVIEWER_IDENTITY_STATE")

if sha(PACKET) != EXPECTED_BLANK_SHA:
    fail("HANDOFF_PACKET_SHA")

if PACKET.stat().st_size != EXPECTED_BLANK_SIZE:
    fail("HANDOFF_PACKET_SIZE")

if sha(PACKAGE_PACKET) != EXPECTED_BLANK_SHA:
    fail("PACKAGE_PACKET_SHA")

if PACKAGE_PACKET.read_bytes() != PACKET.read_bytes():
    fail("BLANK_PACKET_BYTE_IDENTITY")

text = PACKET.read_text(
    encoding="utf-8"
)

if text.count(
    "Decision: `[PASS / REVISION_REQUIRED / FAIL]`"
) != 8:
    fail("BLANK_DECISION_PLACEHOLDER_COUNT")

for forbidden in (
    "Decision: `PASS`",
    "Decision: `REVISION_REQUIRED`",
    "Decision: `FAIL`",
    "Overall decision: `APPROVE_REQUIREMENT_BOUND_CARRIER_ADMISSIBILITY_RESOLUTION_STUDY_V1`",
):
    if forbidden in text:
        fail("PREFILLED_REVIEW_DECISION")

lines = text.splitlines()

for prefix in (
    "Human reviewer name:",
    "Human reviewer signature / recorded confirmation:",
    "Human reviewer date:",
):
    matches = [
        line
        for line in lines
        if line.startswith(prefix)
    ]

    if matches != [prefix]:
        fail("PREFILLED_REVIEWER_IDENTITY|" + prefix)

if sha(DEC0141) != EXPECTED_DEC0141_SHA:
    fail("DECISION0141_SHA")

if sha(DEC0140) != EXPECTED_DEC0140_SHA:
    fail("DECISION0140_SHA")

cons = json.loads(
    A02_CONS.read_text(
        encoding="utf-8"
    )
)

if cons["final_run_result"] != "PASS":
    fail("A02_RESULT")

if (
    cons["verifier_state_after_run"]
    != "PERMANENTLY_RETIRED"
):
    fail("A02_STATE")

if cons["rerun_authorized"] is not False:
    fail("A02_RERUN")

if cons["must_never_be_rerun"] is not True:
    fail("A02_RETIREMENT")

if (
    cons["previous_retired_a02_verifiers_executed"]
    is not False
):
    fail("PREVIOUS_RETIRED_A02_EXECUTION")

if sha(A02_OUT) != cons["final_output_sha256"]:
    fail("A02_OUTPUT_SHA")

if (
    "EXTERNAL_INDEPENDENT_HUMAN_REVIEW_HANDOFF_AUTHORING_AUTHORIZATION=PASS"
    not in A02_OUT.read_text(
        encoding="utf-8"
    )
):
    fail("A02_PASS_MARKER")

if len(
    [
        p
        for p in PACKAGE.rglob("*")
        if p.is_file()
    ]
) != 33:
    fail("PACKAGE_COPY_FILE_COUNT")

if len(
    [
        p
        for p in AUTH.rglob("*")
        if p.is_file()
    ]
) != 3:
    fail("AUTH_COPY_FILE_COUNT")

verify_sums(
    PACKAGE,
    PACKAGE_SUMS,
)

verify_sums(
    AUTH,
    AUTH_SUMS,
)

if sha(PACKAGE_SAFE) != EXPECTED_PACKAGE_SAFE_SHA:
    fail("PACKAGE_SAFE_SHA")

p = subprocess.run(
    [
        "python3",
        str(PACKAGE_SAFE),
    ],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    check=False,
)

if p.returncode != 0:
    fail(
        "PACKAGE_SAFE_VERIFIER|"
        + p.stdout
        + p.stderr
    )

for marker in (
    "REQUIREMENT_BOUND_CARRIER_STUDY_REVIEW_PACKAGE_V1=PASS",
    "REVIEWER_PACKET_INITIAL_BLANK_STATE=PASS",
    "REVIEWER_DECISION_PRESENT=NO",
    "REVIEWER_DECISION_SYNTHESIZED=NO",
    "HUMAN_REVIEW_PERFORMED=NO",
    "PORTABLE_SOURCE_COUNT=9",
    "PORTABLE_SOURCE_RESOLVABILITY=PASS",
    "SEALED_REPOSITORY_CHECKPOINT_BUNDLE=PASS",
    "SEALED_BUNDLE_CHECKPOINT_COMMIT="
    + EXPECTED_BUNDLE_CHECKPOINT,
    "STUDY_OUTCOME_UNDER_REVIEW=FURTHER_EVIDENCE_REQUIRED",
    "UNRESOLVED_COUNT=17",
    "STUDY_GOVERNANCE_ADOPTED=NO",
    "RETIRED_A02_VERIFIERS_EXECUTED=NO",
):
    if marker not in p.stdout:
        fail("PACKAGE_SAFE_MARKER|" + marker)

bundle = (
    PACKAGE
    / "08_sealed_repository_checkpoint.bundle"
)

p = subprocess.run(
    [
        "git",
        "bundle",
        "list-heads",
        str(bundle),
    ],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    check=False,
)

if p.returncode != 0:
    fail("BUNDLE_LIST_HEADS")

if EXPECTED_BUNDLE_CHECKPOINT not in p.stdout:
    fail("BUNDLE_CHECKPOINT")

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
    verify_sums(
        HERE,
        SUMS,
    )

print("EXTERNAL_RBCA01_RBCA08_HANDOFF_V1=PASS")
print("HANDOFF_STATUS=AWAITING_EXTERNAL_INDEPENDENT_HUMAN_REVIEW")
print("REVIEW_ITEMS=RBCA01|RBCA02|RBCA03|RBCA04|RBCA05|RBCA06|RBCA07|RBCA08")
print("REQUIRED_REVIEWER_ROLE=Spec-Technical-Reviewer-1")
print("REVIEWER_PACKET_INITIAL_BLANK_STATE=PASS")
print("REVIEWER_DECISION_PRESENT=NO")
print("REVIEWER_DECISION_SYNTHESIZED=NO")
print("REVIEWER_IDENTITY_PRESENT=NO")
print("HUMAN_REVIEW_PERFORMED=NO")
print("REVIEW_PACKAGE_V1_EXACT_COPY=PASS")
print("REVIEW_PACKAGE_V1_FILE_COUNT=33")
print("PORTABLE_SOURCE_COUNT=9")
print("PORTABLE_SOURCE_RESOLVABILITY=PASS")
print("SEALED_REPOSITORY_CHECKPOINT_BUNDLE=PASS")
print("SEALED_BUNDLE_CHECKPOINT_COMMIT=" + EXPECTED_BUNDLE_CHECKPOINT)
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
print("DECISION_0141_A02_STATE=PERMANENTLY_RETIRED")
print("DECISION_0141_A02_EXECUTED_BY_SAFE_VERIFIER=NO")
print("RETIRED_A02_VERIFIERS_EXECUTED=NO")
