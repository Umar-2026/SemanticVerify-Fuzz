#!/usr/bin/env python3

import hashlib
import json
import subprocess
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent

MANIFEST = HERE / "01_corrective_external_handoff_manifest.v1.json"
MANUAL = HERE / "03_RPR01_RPR08_reviewer_packet.MANUAL_REVIEW_COPY.v1.md"

A02_OUT = HERE / "04_decision0132_a02_final_output.EXACT_COPY.v1.txt"
A02_CONS = HERE / "05_decision0132_a02_consumption_record.v1.json"

RP = HERE / "review_package_v1_exact"

RP_SUBJECT_MANIFEST = RP / "01_review_subject_manifest.v1.json"
RP_SOURCE_MANIFEST = RP / "02_source_binding_manifest.v1.json"
RP_BLANK = RP / "03_RPR01_RPR08_reviewer_packet.BLANK.v1.md"
RP_BUNDLE = RP / "06_repository_checkpoint.bundle"
RP_BUNDLE_MANIFEST = RP / "07_repository_checkpoint_bundle_manifest.v1.json"
RP_SUMS = RP / "10_review_package_v1.SHA256SUMS"

AUTH = HERE / "decision0132_corrective_authorization_exact"

AUTH_JSON = AUTH / "01_corrective_external_handoff_authoring_successor_authorization.v2.json"
FAILED_OLD_A02_OUTPUT = AUTH / "03_decision0130_a02_failed_final_output.EXACT_COPY.v1.txt"
FAILED_OLD_A02_SENTINEL = AUTH / "04_decision0130_a02_consumption_sentinel.EXACT_COPY.v1.txt"
AUTH_SUMS = AUTH / "05_corrective_external_handoff_authoring_successor_authorization.v2.SHA256SUMS"

HANDOFF_SUMS = HERE / "09_corrective_external_handoff_v1.SHA256SUMS"

EXPECTED_BLANK_PACKET_SHA = (
    "1f96825a9d035b256c436b24a39d877f"
    "4983460b0f10323f29847224c891721d"
)

EXPECTED_BUNDLE_CHECKPOINT = (
    "7f13e5569c5d25c9c104a9b1dd68516471b6017a"
)

EXPECTED_BUNDLE_SHA = (
    "ab2aed74d6b082137d8560bd21578323"
    "faf5a543f335ccea45dfc361454ebacf"
)

EXPECTED_FAILED_OLD_A02_OUTPUT_SHA = (
    "4635ef9374bd8edb6278b185635033ce"
    "86fa891f387a821d656f626f71dd5a56"
)

EXPECTED_FAILED_OLD_A02_SENTINEL_SHA = (
    "a977c957e4e8fc9177147d257c64014c"
    "faba0cc98bbbcd13ba44e1da7dd35bf0"
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

def verify_sum_file(root, sums):
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

        if sha(root / rel) != digest:
            fail(
                "CHECKSUM|"
                + str(root / rel)
            )

manifest = json.loads(
    MANIFEST.read_text(
        encoding="utf-8"
    )
)

if (
    manifest["handoff_state"]
    != "AWAITING_EXTERNAL_INDEPENDENT_HUMAN_REVIEW"
):
    fail("HANDOFF_STATE")

subject = manifest["review_subject"]

if subject["review_items"] != [
    "RPR01",
    "RPR02",
    "RPR03",
    "RPR04",
    "RPR05",
    "RPR06",
    "RPR07",
    "RPR08",
]:
    fail("REVIEW_ITEMS")

if (
    subject["required_reviewer_role"]
    != "Spec-Technical-Reviewer-1"
):
    fail("REVIEWER_ROLE")

manual = manifest["manual_reviewer_packet"]

for key in (
    "reviewer_decision_present_at_handoff",
    "reviewer_identity_present_at_handoff",
    "human_review_performed_at_handoff",
    "author_prefilled_review_decisions",
    "author_synthesized_reviewer_identity",
    "author_synthesized_reviewer_notes",
    "author_synthesized_overall_decision",
):
    if manual[key] is not False:
        fail(
            "MANUAL_REVIEW_BOUNDARY|"
            + key
        )

if sha(MANUAL) != EXPECTED_BLANK_PACKET_SHA:
    fail("MANUAL_PACKET_SHA")

if sha(RP_BLANK) != EXPECTED_BLANK_PACKET_SHA:
    fail("REVIEW_PACKAGE_BLANK_SHA")

if MANUAL.read_bytes() != RP_BLANK.read_bytes():
    fail("MANUAL_NOT_BYTE_EXACT_TO_BLANK")

# Review Package V1 integrity.
verify_sum_file(
    RP,
    RP_SUMS,
)

subject_manifest = json.loads(
    RP_SUBJECT_MANIFEST.read_text(
        encoding="utf-8"
    )
)

if subject_manifest["reviewer_decision_present"] is not False:
    fail("RP_REVIEWER_DECISION_PRESENT")

if subject_manifest["reviewer_decision_synthesized"] is not False:
    fail("RP_REVIEWER_DECISION_SYNTHESIZED")

source_manifest = json.loads(
    RP_SOURCE_MANIFEST.read_text(
        encoding="utf-8"
    )
)

if source_manifest["source_count"] != 7:
    fail("PORTABLE_SOURCE_COUNT")

if source_manifest["all_sources_portable"] is not True:
    fail("PORTABLE_SOURCE_STATE")

for record in source_manifest["records"]:
    portable = (
        RP
        / record["portable_package_relative_path"]
    )

    if sha(portable) != record["portable_sha256"]:
        fail(
            "PORTABLE_SOURCE_SHA|"
            + record["original_repo_relative_path"]
        )

    if (
        record["source_sha256"]
        != record["portable_sha256"]
    ):
        fail(
            "SOURCE_PORTABLE_SHA_DISAGREEMENT|"
            + record["original_repo_relative_path"]
        )

# Sealed Git bundle.
bundle_manifest = json.loads(
    RP_BUNDLE_MANIFEST.read_text(
        encoding="utf-8"
    )
)

if (
    bundle_manifest["checkpoint_commit"]
    != EXPECTED_BUNDLE_CHECKPOINT
):
    fail("BUNDLE_CHECKPOINT")

if (
    bundle_manifest["bundle_sha256"]
    != EXPECTED_BUNDLE_SHA
):
    fail("BUNDLE_MANIFEST_SHA")

if sha(RP_BUNDLE) != EXPECTED_BUNDLE_SHA:
    fail("BUNDLE_FILE_SHA")

p = subprocess.run(
    [
        "git",
        "bundle",
        "list-heads",
        str(RP_BUNDLE),
    ],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    check=False,
)

if p.returncode != 0:
    fail(
        "BUNDLE_LIST_HEADS|"
        + p.stdout
        + p.stderr
    )

if EXPECTED_BUNDLE_CHECKPOINT not in p.stdout:
    fail("BUNDLE_EXPECTED_HEAD")

with tempfile.TemporaryDirectory() as td:
    p = subprocess.run(
        [
            "git",
            "init",
            "--bare",
            td,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )

    if p.returncode != 0:
        fail("TEMP_GIT_INIT")

    p = subprocess.run(
        [
            "git",
            "-C",
            td,
            "bundle",
            "verify",
            str(RP_BUNDLE),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )

    if p.returncode != 0:
        fail(
            "PORTABLE_BUNDLE_VERIFY|"
            + p.stdout
            + p.stderr
        )

# Corrective authorization V2.
verify_sum_file(
    AUTH,
    AUTH_SUMS,
)

auth = json.loads(
    AUTH_JSON.read_text(
        encoding="utf-8"
    )
)

if (
    auth["authorization_type"]
    != "PRE_CORRECTIVE_EXTERNAL_HANDOFF_AUTHORING_ONLY"
):
    fail("CORRECTIVE_AUTH_TYPE")

if (
    auth["failed_pre_handoff_verifier"]["state"]
    != "PERMANENTLY_RETIRED"
):
    fail("FAILED_OLD_A02_STATE")

if (
    auth["failed_pre_handoff_verifier"]["rerun_authorized"]
    is not False
):
    fail("FAILED_OLD_A02_RERUN")

if (
    auth["failed_pre_handoff_verifier"]["patch_in_place_authorized"]
    is not False
):
    fail("FAILED_OLD_A02_PATCH")

if (
    sha(FAILED_OLD_A02_OUTPUT)
    != EXPECTED_FAILED_OLD_A02_OUTPUT_SHA
):
    fail("FAILED_OLD_A02_OUTPUT_SHA")

if (
    FAILED_OLD_A02_OUTPUT.read_text(
        encoding="utf-8"
    ).strip()
    != "FAIL|DECISION0129_CHECKPOINT"
):
    fail("FAILED_OLD_A02_OUTPUT")

if (
    sha(FAILED_OLD_A02_SENTINEL)
    != EXPECTED_FAILED_OLD_A02_SENTINEL_SHA
):
    fail("FAILED_OLD_A02_SENTINEL_SHA")

sentinel = FAILED_OLD_A02_SENTINEL.read_text(
    encoding="utf-8"
)

for marker in (
    "DECISION_0130_A02_EXECUTED=YES",
    "RETURN_CODE=1",
    "STATE=PERMANENTLY_RETIRED",
    "MUST_NEVER_BE_RERUN=YES",
):
    if marker not in sentinel:
        fail(
            "FAILED_OLD_A02_SENTINEL_MARKER|"
            + marker
        )

# Decision-0132 A02 successful retirement evidence.
cons = json.loads(
    A02_CONS.read_text(
        encoding="utf-8"
    )
)

if cons["final_run_result"] != "PASS":
    fail("DECISION0132_A02_RESULT")

if (
    cons["verifier_state_after_run"]
    != "PERMANENTLY_RETIRED"
):
    fail("DECISION0132_A02_STATE")

if cons["must_never_be_rerun"] is not True:
    fail("DECISION0132_A02_RETIREMENT")

if sha(A02_OUT) != cons["final_output_sha256"]:
    fail("DECISION0132_A02_OUTPUT_SHA")

if (
    "CORRECTIVE_EXTERNAL_HANDOFF_AUTHORING_AUTHORIZATION=PASS"
    not in A02_OUT.read_text(
        encoding="utf-8"
    )
):
    fail("DECISION0132_A02_PASS_MARKER")

# Full handoff checksum closure when present.
if HANDOFF_SUMS.is_file():
    verify_sum_file(
        HERE,
        HANDOFF_SUMS,
    )

for key, value in manifest[
    "operational_non_authorizations"
].items():
    if value is not False:
        fail(
            "UNEXPECTED_OPERATIONAL_AUTHORIZATION|"
            + key
        )

gov = manifest["governance_state"]

if gov["human_review_recorded"] is not False:
    fail("HUMAN_REVIEW_RECORDED")

if gov["study_governance_adopted"] is not False:
    fail("STUDY_GOVERNANCE_ADOPTED")

if gov["positive_mapping_proven"] is not False:
    fail("POSITIVE_MAPPING_PROVEN")

if gov["negative_mapping_impossibility_proven"] is not False:
    fail("NEGATIVE_MAPPING_PROVEN")

if gov["whole_v4_exhaustiveness_proven"] is not False:
    fail("WHOLE_V4_EXHAUSTIVENESS")

print("CORRECTIVE_EXTERNAL_INDEPENDENT_HUMAN_REVIEW_HANDOFF_V1=PASS")
print("HANDOFF_STATE=AWAITING_EXTERNAL_INDEPENDENT_HUMAN_REVIEW")
print("REVIEW_ITEMS=RPR01|RPR02|RPR03|RPR04|RPR05|RPR06|RPR07|RPR08")
print("REQUIRED_REVIEWER_ROLE=Spec-Technical-Reviewer-1")
print("REVIEWER_PACKET_INITIAL_BLANK_STATE=PASS")
print("REVIEWER_DECISION_PRESENT=NO")
print("REVIEWER_DECISION_SYNTHESIZED=NO")
print("HUMAN_REVIEW_PERFORMED=NO")
print("PORTABLE_SOURCE_COUNT=7")
print("PORTABLE_SOURCE_RESOLVABILITY=PASS")
print("SEALED_REPOSITORY_CHECKPOINT_BUNDLE=PASS")
print("SEALED_BUNDLE_CHECKPOINT_COMMIT=" + EXPECTED_BUNDLE_CHECKPOINT)
print("FAILED_DECISION_0130_A02_RESULT=FAIL")
print("FAILED_DECISION_0130_A02_STATE=PERMANENTLY_RETIRED")
print("FAILED_DECISION_0130_A02_EXECUTED_BY_SAFE_VERIFIER=NO")
print("DECISION_0132_A02_STATE=PERMANENTLY_RETIRED")
print("DECISION_0132_A02_EXECUTED_BY_SAFE_VERIFIER=NO")
print("DECISION_0128_A02_STATE=PERMANENTLY_RETIRED")
print("DECISION_0126_A02_STATE=PERMANENTLY_RETIRED")
print("RETIRED_A02_VERIFIERS_EXECUTED=NO")
print("STUDY_OUTCOME_UNDER_REVIEW=REQUIREMENT_PROVENANCE_RESOLVED")
print("STUDY_GOVERNANCE_ADOPTED=NO")
print("POSITIVE_MAPPING_PROVEN=NO")
print("NEGATIVE_MAPPING_IMPOSSIBILITY_PROVEN=NO")
print("WHOLE_V4_EXHAUSTIVENESS_PROVEN=NO")
print("OPERATIONAL_MAPPING_AUTHORIZED=NO")
print("ACTIVE_SCHEMA_V2_MODIFICATION_AUTHORIZED=NO")
print("SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO")
print("SCHEMA_VERSION_PRESELECTED=NO")
print("SCHEMA_V3_CREATED=NO")
print("CURL_JSON_AUTHORIZED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
