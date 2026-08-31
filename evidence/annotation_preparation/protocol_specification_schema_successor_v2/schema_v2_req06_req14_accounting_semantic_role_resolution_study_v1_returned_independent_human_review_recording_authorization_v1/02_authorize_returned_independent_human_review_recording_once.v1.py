#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import re
import subprocess

D0197_COMMIT = "cd2c9cf591bd970642b85fbf935a64c68d68ae68"

RETURNED = Path(
    "/openbayes/home/"
    "50_req06_req14_Nadeem_accounting_role_"
    "independent_human_review_form.MANUAL_REVIEW_COPY.v1.md"
)

RETURNED_SHA = (
    "a3a9f38ed79b3fa450d6799677b986b690a02f235ef21acf93cb5b75d2423309"
)

RETURNED_SIZE = 9578

ROOT = Path(
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2"
)

HANDOFF_DIR = ROOT / (
    "schema_v2_req06_req14_accounting_semantic_role_resolution_"
    "study_v1_external_independent_human_review_handoff_v1"
)

H01 = (
    HANDOFF_DIR
    / "01_external_independent_human_review_handoff_manifest.v1.json"
)

AUTH_DIR = ROOT / (
    "schema_v2_req06_req14_accounting_semantic_role_resolution_"
    "study_v1_returned_independent_human_review_recording_authorization_v1"
)

A01 = (
    AUTH_DIR
    / "01_returned_independent_human_review_recording_authorization.v1.json"
)

A02 = (
    AUTH_DIR
    / "02_authorize_returned_independent_human_review_recording_once.v1.py"
)

A03 = (
    AUTH_DIR
    / "03_returned_independent_human_review_recording_contract.v1.json"
)

A04 = (
    AUTH_DIR
    / "04_returned_independent_human_review_recording_authorization_boundary.v1.md"
)

DEC = Path(
    "documentation/decisions/"
    "0198-authorize-recording-returned-independent-human-review-for-"
    "req06-req14-accounting-role-study-v1.md"
)

EXPECTED_D0198_PATHS = {
    str(A01),
    str(A02),
    str(A03),
    str(A04),
    str(DEC),
}

EXPECTED_H01_SHA = (
    "ea1ebda0455ecf699273d8138e8a9af7794cc24a4b63523c1b31dd5fa4001c76"
)


def stop(code, detail=""):
    print(
        "STOP|" + code
        + (("|" + detail) if detail else "")
    )
    raise SystemExit(1)


def git(*args):
    return subprocess.check_output(
        ["git", *args],
        text=True
    ).strip()


def clean(s):
    s = s.strip()

    if (
        len(s) >= 2
        and s.startswith("`")
        and s.endswith("`")
    ):
        return s[1:-1].strip()

    return s


def next_value(lines, label):
    hits = [
        i
        for i, line in enumerate(lines)
        if line.startswith(label)
    ]

    if len(hits) != 1:
        stop(
            "RETURNED_FIELD_COUNT_INVALID",
            label
        )

    i = hits[0]

    inline = clean(
        lines[i][len(label):]
    )

    if inline:
        return inline

    j = i + 1

    while (
        j < len(lines)
        and not lines[j].strip()
    ):
        j += 1

    if j >= len(lines):
        stop(
            "RETURNED_FIELD_BLANK",
            label
        )

    value = clean(lines[j])

    if (
        not value
        or value.startswith("#")
        or value == "---"
    ):
        stop(
            "RETURNED_FIELD_BLANK",
            label
        )

    return value


if git(
    "rev-parse",
    "HEAD^"
) != D0197_COMMIT:
    stop(
        "D0198_PARENT_NOT_D0197"
    )

if subprocess.check_output(
    [
        "git",
        "status",
        "--porcelain=v1",
        "--untracked-files=all"
    ],
    text=True
).strip():
    stop(
        "REPOSITORY_NOT_CLEAN_BEFORE_RETURNED_REVIEW_RECORDING"
    )

changed = {
    p
    for p in subprocess.check_output(
        [
            "git",
            "diff-tree",
            "--no-commit-id",
            "--name-only",
            "-r",
            "HEAD",
        ],
        text=True,
    ).splitlines()
    if p.strip()
}

if changed != EXPECTED_D0198_PATHS:
    stop(
        "D0198_COMMIT_SCOPE_MISMATCH",
        ",".join(sorted(changed))
    )

for path in (
    A01,
    A02,
    A03,
    A04,
    DEC,
    H01,
):
    if not path.is_file():
        stop(
            "REQUIRED_ARTIFACT_MISSING",
            str(path)
        )

if hashlib.sha256(
    H01.read_bytes()
).hexdigest() != EXPECTED_H01_SHA:
    stop(
        "D0197_HANDOFF_MANIFEST_SHA_MISMATCH"
    )

if not RETURNED.is_file():
    stop(
        "AUTHORIZED_RETURNED_REVIEW_FILE_MISSING"
    )

raw = RETURNED.read_bytes()

if hashlib.sha256(
    raw
).hexdigest() != RETURNED_SHA:
    stop(
        "AUTHORIZED_RETURNED_REVIEW_SHA_MISMATCH"
    )

if len(raw) != RETURNED_SIZE:
    stop(
        "AUTHORIZED_RETURNED_REVIEW_SIZE_MISMATCH"
    )

authorization = json.loads(
    A01.read_text(encoding="utf-8")
)

contract = json.loads(
    A03.read_text(encoding="utf-8")
)

text = raw.decode("utf-8")
lines = text.splitlines()

if authorization.get("decision") != "0198":
    stop(
        "D0198_AUTHORIZATION_DECISION_INVALID"
    )

if authorization.get("status") != (
    "AUTHORIZED_TO_RECORD_EXACT_RETURNED_INDEPENDENT_HUMAN_REVIEW_ONLY"
):
    stop(
        "D0198_AUTHORIZATION_STATUS_INVALID"
    )

prior = authorization.get(
    "prior_failed_attempt",
    {}
)

if prior.get("repository_effect") != "NONE":
    stop(
        "PRIOR_FAILED_ATTEMPT_REPOSITORY_EFFECT_INVALID"
    )

if prior.get("decision0198_a02_executed") is not False:
    stop(
        "PRIOR_FAILED_ATTEMPT_A02_STATE_INVALID"
    )

activity = authorization.get(
    "authorized_recording_activity",
    {}
)

for key in (
    "copy_exact_returned_review_into_new_immutable_repository_record",
    "record_exact_returned_review_sha256_and_size",
    "record_review_item_decisions_without_rewriting",
    "record_reviewer_notes_without_rewriting",
    "record_overall_decision_without_rewriting",
    "record_overall_notes_without_rewriting",
    "record_reviewer_identity_as_packet_recorded_fact",
    "record_packet_independence_attestation_as_packet_recorded_fact",
):
    if activity.get(key) is not True:
        stop(
            "AUTHORIZED_RECORDING_ACTIVITY_MISSING",
            key
        )

for key in (
    "perform_new_human_review",
    "alter_returned_review",
    "rewrite_reviewer_notes",
    "synthesize_reviewer_identity",
    "synthesize_reviewer_decision",
    "governance_adopt_role_study",
):
    if activity.get(key) is not False:
        stop(
            "RECORDING_ACTIVITY_BOUNDARY_INVALID",
            key
        )

technical = authorization.get(
    "technical_non_authorizations",
    {}
)

for key in (
    "role_governance_adoption",
    "accounting_satisfaction_establishment",
    "pair_reclassification",
    "supported_binding_creation",
    "not_supported_binding_creation",
    "operational_mapping",
    "schema_v2_modification",
    "schema_successor",
    "curl_json",
    "analyzer_implementation",
    "analyzer_execution",
    "baseline_execution",
    "repair",
):
    if technical.get(key) is not False:
        stop(
            "TECHNICAL_NONAUTHORIZATION_INVALID",
            key
        )

facts = contract.get(
    "required_recorded_review_facts",
    {}
)

if facts.get(
    "review_item_ids"
) != [
    "ASRR01",
    "ASRR02",
    "ASRR03",
    "ASRR04",
    "ASRR05",
    "ASRR06",
]:
    stop(
        "REQUIRED_REVIEW_ITEM_IDS_INVALID"
    )

if facts.get(
    "required_pass_count"
) != 6:
    stop(
        "REQUIRED_PASS_COUNT_INVALID"
    )

if facts.get(
    "required_revision_required_count"
) != 0:
    stop(
        "REQUIRED_REVISION_COUNT_INVALID"
    )

if facts.get(
    "required_overall_decision"
) != "APPROVE_BOUNDED_ROLE_STUDY":
    stop(
        "REQUIRED_OVERALL_DECISION_INVALID"
    )

if next_value(
    lines,
    "Reviewer name:"
) != "Muhammad Nadeem Nadir":
    stop(
        "RETURNED_REVIEWER_NAME_CHANGED"
    )

if next_value(
    lines,
    "Reviewer role:"
) != "Spec-Technical-Adjudicator-1":
    stop(
        "RETURNED_REVIEWER_ROLE_CHANGED"
    )

if next_value(
    lines,
    "Reviewer confirmation/signature:"
) != "MN_Lodhi":
    stop(
        "RETURNED_REVIEWER_CONFIRMATION_CHANGED"
    )

if next_value(
    lines,
    "Review date:"
) != "31 / August / 2026":
    stop(
        "RETURNED_REVIEW_DATE_CHANGED"
    )

attestation = next_value(
    lines,
    "Independent-review attestation:"
).lower()

if "independent human reviewer" not in attestation:
    stop(
        "RETURNED_INDEPENDENCE_ATTESTATION_CHANGED"
    )

if "not the author" not in attestation:
    stop(
        "RETURNED_NOT_AUTHOR_ATTESTATION_CHANGED"
    )

observed = []

for item in (
    "ASRR01",
    "ASRR02",
    "ASRR03",
    "ASRR04",
    "ASRR05",
    "ASRR06",
):
    match = re.search(
        rf"^## {item} .*?(?=^## |\Z)",
        text,
        re.MULTILINE | re.DOTALL
    )

    if not match:
        stop(
            "RETURNED_REVIEW_ITEM_MISSING",
            item
        )

    section = match.group(0).splitlines()

    decision = next_value(
        section,
        "Review decision:"
    )

    if decision != "PASS":
        stop(
            "RETURNED_REVIEW_ITEM_DECISION_CHANGED",
            item + ":" + decision
        )

    notes = next_value(
        section,
        "Reviewer notes:"
    )

    if not notes:
        stop(
            "RETURNED_REVIEW_ITEM_NOTES_BLANK",
            item
        )

    observed.append(
        (item, decision)
    )

if observed != [
    ("ASRR01", "PASS"),
    ("ASRR02", "PASS"),
    ("ASRR03", "PASS"),
    ("ASRR04", "PASS"),
    ("ASRR05", "PASS"),
    ("ASRR06", "PASS"),
]:
    stop(
        "RETURNED_REVIEW_ITEM_SEQUENCE_CHANGED"
    )

if next_value(
    lines,
    "Overall review decision:"
) != "APPROVE_BOUNDED_ROLE_STUDY":
    stop(
        "RETURNED_OVERALL_DECISION_CHANGED"
    )

if not next_value(
    lines,
    "Overall reviewer notes:"
):
    stop(
        "RETURNED_OVERALL_NOTES_BLANK"
    )

decision_text = DEC.read_text(
    encoding="utf-8"
)

for marker in (
    "RETURNED_REVIEW_RECORDING_AUTHORIZED=YES",
    "RETURNED_REVIEW_RECORDED=NO",
    "ROLE_GOVERNANCE_ADOPTED=NO",
    "PAIR_RECLASSIFICATION_PERFORMED=NO",
    "ACCOUNTING_SATISFACTION_ESTABLISHED=NO",
    "OPERATIONAL_MAPPING_AUTHORIZED=NO",
    "ANALYZER_AUTHORIZED=NO",
    "BASELINE_AUTHORIZED=NO",
    "REPAIR_AUTHORIZED=NO",
):
    if marker not in decision_text:
        stop(
            "DECISION0198_MARKER_MISSING",
            marker
        )

print(
    "DECISION0198_RETURNED_REVIEW_RECORDING_"
    "AUTHORIZATION_VERIFIER=PASS"
)

print(
    "AUTHORIZED_RETURNED_REVIEW_SHA256="
    + RETURNED_SHA
)

print(
    "AUTHORIZED_RETURNED_REVIEW_SIZE=9578"
)

print("REVIEW_ITEM_COUNT=6")
print("REVIEW_ITEM_PASS_COUNT=6")
print("REVIEW_ITEM_REVISION_REQUIRED_COUNT=0")

print(
    "OVERALL_REVIEW_DECISION="
    "APPROVE_BOUNDED_ROLE_STUDY"
)

print(
    "RETURNED_REVIEW_RECORDING_AUTHORIZED=YES"
)

print(
    "RETURNED_REVIEW_RECORDED_BY_THIS_VERIFIER=NO"
)

print(
    "ROLE_GOVERNANCE_ADOPTED=NO"
)

print(
    "PAIR_RECLASSIFICATION_PERFORMED=NO"
)

print(
    "ACCOUNTING_SATISFACTION_ESTABLISHED=NO"
)

print(
    "HUMAN_IDENTITY_INDEPENDENTLY_VERIFIED=NO"
)

print(
    "HUMAN_AUTHORSHIP_BEYOND_RETURNED_ARTIFACT_"
    "INDEPENDENTLY_PROVEN=NO"
)

print(
    "AUTHORIZATION_EXECUTION_COUNT_FOR_THIS_RUN=1"
)

print(
    "AUTHORIZATION_RERUN_AUTHORIZED=NO"
)
