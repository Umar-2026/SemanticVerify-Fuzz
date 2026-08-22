#!/usr/bin/env python3

import hashlib
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent

FILES = {
    "pred_manifest":
        HERE / "01_predecessor_review_package_v1_manifest.EXACT_COPY.json",

    "pred_sums":
        HERE / "02_predecessor_review_package_v1_checksums.EXACT_COPY.SHA256SUMS",

    "proof_json":
        HERE / "03_residual_insufficiency_proof_v1.EXACT_COPY.json",

    "proof_md":
        HERE / "04_residual_insufficiency_proof_v1_summary.EXACT_COPY.md",

    "schema":
        HERE / "05_protocol_specification_v2_schema.EXACT_COPY.json",

    "review":
        HERE / "06_completed_human_review_v1.EXACT_COPY.md",

    "d0056":
        HERE / "07_schema_v2_human_approval_decision_0056.EXACT_COPY.md",

    "d0064":
        HERE / "08_activation_corrective_approval_decision_0064.EXACT_COPY.md",

    "d0065":
        HERE / "09_explicit_activation_authorization_decision_0065.EXACT_COPY.md",

    "d0066":
        HERE / "10_schema_v2_activation_decision_0066.EXACT_COPY.md",

    "activation":
        HERE / "11_schema_v2_activation_execution_record.EXACT_COPY.json",

    "active_hash":
        HERE / "12_active_v2_hash_contract.EXACT_COPY.json",

    "dispatch":
        HERE / "13_active_schema_version_dispatch.EXACT_COPY.json",

    "authorization":
        HERE / "14_decision_0071_corrective_authorization.EXACT_COPY.json",

    "bundle":
        HERE / "15_schema_v2_activation_git_provenance.bundle",

    "evidence":
        HERE / "16_RI01_corrective_activation_provenance_evidence.v1.json",

    "packet":
        HERE / "17_RI01_focused_reviewer_packet.REVIEW_DRAFT.v1.md",

    "manifest":
        HERE / "19_corrective_review_package_v2_manifest.v1.json",
}

EXPECTED = {
    "pred_manifest":
        "be45fdffcd4ce463ba3b78b57ac9594309353deeaa14e2f007f985a171849244",

    "pred_sums":
        "38dc6b809fd1528ebe877adac7da8d3ee05c038479b9267c80b2b02624201f6f",

    "proof_json":
        "400f6806217f50b79d17ec77e41683d9077f64e07c63e5421c8b1922b49aaff0",

    "proof_md":
        "c9eddfbdfc29d3e3409dd4e674499e0712fdd604751e9fe01948cef9e5cff57b",

    "schema":
        "c6ebb5ef2214c4168283f9009d1f7ce6e88d2ff928853fe6a57ed1f7521c6956",

    "review":
        "c169b26960349c4829109493f946d4f7115191a830ec35a28ff7a50e6df8c74d",

    "d0056":
        "7eb9026652651f07d8aa281852b3f057de37f09171e1391c0e416d80f7e3b608",

    "d0064":
        "73e4d29278a5cf4368630210d4dc69c9d0b18b03795b9756e5acf5a563fbc4ad",

    "d0065":
        "ea7dba8c77b6c6ae75e81e68a817b551fb2d138e536a1ea15eab75e2c3c28d63",

    "d0066":
        "6bd97e92f97f77d7e7e36bbc9a334ad115f1ebe8f8a2e9f3d0d2b2c361da65d2",

    "activation":
        "8384e173d6c0cac2e78941e33ea8d4aaf45677fa5a59fb00370d5fd2b564d06a",

    "active_hash":
        "37f035bb617f5598a0e368ba3b60b4bf1e69e4e69ce2f1053d71c0fcc96619e9",

    "dispatch":
        "67a96c3eda8de95fa6c55342d5d33ea725e16cea8af21fcb4f3b8945b9d4eeee",

    "authorization":
        "1428e00abca3cfad285f9cd1f7d6bde7f0dc3f8a0479b9a574a7e2fbab2a078e",
}

ACTIVATION_COMMIT = \
    "7b40f4385c2964edd95c4d90a0a3a1090c1b9ccd"

ACTIVATION_TREE = \
    "82f5faa7a7b9c45a4d9633bf3720da4f09bc8116"

ACTIVATION_PARENT = \
    "aa4b85e74f56adab581faf379a09ee69ce1ec30f"

PATH_EXPECTATIONS = {
    "config/schemas/protocol_specification.v2.schema.json":
        EXPECTED["schema"],

    "config/protocol_content_hash_canonicalization.v2.json":
        EXPECTED["active_hash"],

    "config/protocol_specification_schema_version_dispatch.v1.json":
        EXPECTED["dispatch"],

    "documentation/decisions/0056-record-final-schema-v2-candidate-human-approval.md":
        EXPECTED["d0056"],

    "documentation/decisions/0064-record-AF04-AF07-AF08-AF09-corrective-evidence-human-approval.md":
        EXPECTED["d0064"],

    "documentation/decisions/0065-authorize-explicit-schema-v2-activation-execution.md":
        EXPECTED["d0065"],

    "documentation/decisions/0066-activate-schema-v2-and-adopt-decision-0019-successor.md":
        EXPECTED["d0066"],

    "evidence/annotation_preparation/protocol_specification_schema_successor_v2/schema_v2_activation_execution_v1/01_schema_v2_activation_execution_record.v1.json":
        EXPECTED["activation"],
}

def fail(msg):
    print("FAIL|" + msg)
    raise SystemExit(1)

def sha(path):
    if not path.is_file():
        fail("MISSING|" + path.name)

    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()

for key, expected in EXPECTED.items():
    if sha(FILES[key]) != expected:
        fail(
            "EXACT_COPY_SHA|"
            + key
        )

evidence = json.loads(
    FILES["evidence"].read_text(
        encoding="utf-8"
    )
)

authorization = json.loads(
    FILES["authorization"].read_text(
        encoding="utf-8"
    )
)

if authorization[
    "authorized_corrective_package"
]["evidence_only"] is not True:
    fail("AUTH_NOT_EVIDENCE_ONLY")

if authorization[
    "authorized_corrective_package"
]["RI01_focused_rereview_only"] is not True:
    fail("AUTH_NOT_RI01_ONLY")

if evidence[
    "corrective_scope"
]["evidence_only"] is not True:
    fail("EVIDENCE_SCOPE")

if evidence[
    "corrective_scope"
]["focused_RI01_rereview_only"] is not True:
    fail("EVIDENCE_RI01_SCOPE")

if evidence[
    "corrective_scope"
]["proof_v1_modified"] is not False:
    fail("PROOF_MODIFIED")

if evidence[
    "corrective_scope"
]["predecessor_review_package_v1_modified"] is not False:
    fail("PREDECESSOR_PACKAGE_MODIFIED")

if evidence[
    "corrective_scope"
]["RI02_to_RI08_reopened"] is not False:
    fail("RI02_TO_RI08_REOPENED")

review_text = FILES["review"].read_text(
    encoding="utf-8"
)

expected_decisions = {
    "RI01": "REVISION_REQUIRED",
    "RI02": "PASS",
    "RI03": "PASS",
    "RI04": "PASS",
    "RI05": "PASS",
    "RI06": "PASS",
    "RI07": "PASS",
    "RI08": "PASS",
}

for rid, decision in expected_decisions.items():
    m = re.search(
        rf"^### {rid}\b.*?"
        rf"^Decision \(PASS / REVISION_REQUIRED / FAIL\):\s*"
        rf"(PASS|REVISION_REQUIRED|FAIL)\s*$",
        review_text,
        flags=re.MULTILINE | re.DOTALL,
    )

    if not m or m.group(1) != decision:
        fail(
            "PREDECESSOR_REVIEW_DECISION|"
            + rid
        )

packet = FILES["packet"].read_text(
    encoding="utf-8"
)

decision_line = re.findall(
    r"^Focused RI01 decision \(PASS / REVISION_REQUIRED / FAIL\):(.*)$",
    packet,
    flags=re.MULTILINE,
)

if len(decision_line) != 1:
    fail("FOCUSED_DECISION_LINE_COUNT")

if decision_line[0].strip():
    fail("FOCUSED_DECISION_NOT_BLANK")

for field in (
    "Reviewer role:",
    "Human reviewer name:",
    "Human reviewer signature / recorded confirmation:",
    "Human reviewer date:",
):
    lines = [
        x
        for x in packet.splitlines()
        if x.startswith(field)
    ]

    if len(lines) != 1:
        fail(
            "REVIEWER_FIELD_COUNT|"
            + field
        )

    if lines[0][len(field):].strip():
        fail(
            "REVIEWER_FIELD_NOT_BLANK|"
            + field
        )

tmp = Path(
    tempfile.mkdtemp(
        prefix="svf-ri01-v2-verify-"
    )
)

try:
    bare = tmp / "verify.git"
    work = tmp / "work"

    subprocess.run(
        [
            "git",
            "init",
            "--bare",
            "-q",
            str(bare),
        ],
        check=True,
    )

    subprocess.run(
        [
            "git",
            "-C",
            str(bare),
            "bundle",
            "verify",
            str(FILES["bundle"]),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    subprocess.run(
        [
            "git",
            "clone",
            "-q",
            str(FILES["bundle"]),
            str(work),
        ],
        check=True,
    )

    object_type = subprocess.check_output(
        [
            "git",
            "-C",
            str(work),
            "cat-file",
            "-t",
            ACTIVATION_COMMIT,
        ],
        text=True,
    ).strip()

    if object_type != "commit":
        fail("ACTIVATION_COMMIT_OBJECT")

    tree = subprocess.check_output(
        [
            "git",
            "-C",
            str(work),
            "rev-parse",
            ACTIVATION_COMMIT + "^{tree}",
        ],
        text=True,
    ).strip()

    if tree != ACTIVATION_TREE:
        fail("ACTIVATION_TREE")

    parent = subprocess.check_output(
        [
            "git",
            "-C",
            str(work),
            "show",
            "-s",
            "--format=%P",
            ACTIVATION_COMMIT,
        ],
        text=True,
    ).strip()

    if parent != ACTIVATION_PARENT:
        fail("ACTIVATION_PARENT")

    for rel, expected_sha in PATH_EXPECTATIONS.items():
        data = subprocess.check_output(
            [
                "git",
                "-C",
                str(work),
                "show",
                ACTIVATION_COMMIT + ":" + rel,
            ]
        )

        observed = hashlib.sha256(
            data
        ).hexdigest()

        if observed != expected_sha:
            fail(
                "ACTIVATION_PATH_SHA|"
                + rel
            )

    for item in evidence[
        "approval_and_activation_lineage"
    ]:
        history_commit = item.get(
            "history_commit"
        )

        if history_commit:
            rc = subprocess.run(
                [
                    "git",
                    "-C",
                    str(work),
                    "merge-base",
                    "--is-ancestor",
                    history_commit,
                    ACTIVATION_COMMIT,
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            ).returncode

            if rc != 0:
                fail(
                    "APPROVAL_HISTORY_NOT_ANCESTOR|"
                    + item["stage"]
                )

finally:
    shutil.rmtree(
        tmp,
        ignore_errors=True
    )

manifest = json.loads(
    FILES["manifest"].read_text(
        encoding="utf-8"
    )
)

if manifest[
    "human_rereview_state"
]["completed"] is not False:
    fail("HUMAN_REREVIEW_ALREADY_COMPLETED")

if manifest[
    "human_rereview_state"
]["synthetic_decision"] is not False:
    fail("SYNTHETIC_DECISION")

for entry in manifest[
    "package_files"
]:
    path = HERE / entry["filename"]

    if not path.is_file():
        fail(
            "MANIFEST_FILE_MISSING|"
            + entry["filename"]
        )

    if sha(path) != entry["sha256"]:
        fail(
            "MANIFEST_FILE_SHA|"
            + entry["filename"]
        )

print("PREDECESSOR_REVIEW_PACKAGE_V1_BINDING=PASS")
print("PROOF_V1_BYTES_UNCHANGED=YES")
print("COMPLETED_HUMAN_REVIEW_BINDING=PASS")
print("RI01_PREDECESSOR_DECISION=REVISION_REQUIRED")
print("RI02_TO_RI08_PASS_CLOSED=YES")
print("CORRECTIVE_SCOPE=EVIDENCE_ONLY")
print("FOCUSED_RI01_REREVIEW_ONLY=YES")
print("SCHEMA_V2_EXACT_SHA_BINDING=PASS")
print("SCHEMA_V2_HUMAN_APPROVAL_DECISION_0056=BOUND")
print("ACTIVATION_CORRECTIVE_APPROVAL_DECISION_0064=BOUND")
print("EXPLICIT_ACTIVATION_AUTHORIZATION_DECISION_0065=BOUND")
print("SCHEMA_V2_ACTIVATION_DECISION_0066=BOUND")
print("ACTIVATION_EXECUTION_RECORD=BOUND")
print("PORTABLE_GIT_BUNDLE_VERIFICATION=PASS")
print("ACTIVATION_COMMIT_OBJECT=PASS")
print("ACTIVATION_TREE=PASS")
print("ACTIVATION_PARENT=PASS")
print("ACTIVATION_PATH_CONTENT_BINDINGS=PASS")
print("APPROVAL_HISTORY_ANCESTRY=PASS")
print("FOCUSED_RI01_INITIAL_DECISION_BLANK=YES")
print("REVIEWER_IDENTITY_FIELDS_INITIAL_BLANK=YES")
print("INDEPENDENT_FOCUSED_RI01_REREVIEW_COMPLETED=NO")
print("SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO")
print("POSITIVE_V4_TO_V2_MAPPING_AUTHORIZED=NO")
print("CURL_JSON_CREATED=NO")
print("SELF_CONTAINED_CORRECTIVE_REVIEW_PACKAGE_V2=PASS")
