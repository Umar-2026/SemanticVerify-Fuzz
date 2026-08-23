#!/usr/bin/env python3

import hashlib
import json
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]

BASE = (
    REPO
    / "evidence"
    / "annotation_preparation"
    / "protocol_specification_schema_successor_v2"
)

HANDOFF_REL = (
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2/"
    "schema_v2_semantic_role_relation_formalization_v1_"
    "corrective_successor_package_v2_focused_rereview_handoff_v1"
)

HANDOFF = REPO / HANDOFF_REL

COMPLETED = (
    HERE
    / "01_completed_focused_human_review.EXACT_COPY.v1.md"
)

RECORD = (
    HERE
    / "02_completed_focused_human_review_record.v1.json"
)

SELF = (
    HERE
    / "03_verify_repository_completed_focused_human_review.v1.py"
)

SUMS = (
    HERE
    / "04_completed_focused_human_review.v1.SHA256SUMS"
)

BLANK = (
    HANDOFF
    / "02_focused_rereview_packet.MANUAL_REVIEW_COPY.v1.md"
)

HANDOFF_SAFE = (
    HANDOFF
    / "03_verify_external_focused_rereview_handoff.v1.py"
)

HANDOFF_MANIFEST = (
    HANDOFF
    / "01_external_focused_rereview_handoff_manifest.v1.json"
)

EXPECTED = {
    COMPLETED:
        "30973cde36434c4737be4359ba316f579af6a58ca5c0cd9ff1155cab03e902ce",

    BLANK:
        "60185126f93d5a113722545108c4b798563b6088f9b92945ccb7cd16840db75e",

    HANDOFF_SAFE:
        "bd97f7fe457f17d1433e2f189f9a62c1394672371bd1bf3a704025454a3d5f15",

    HANDOFF_MANIFEST:
        "9f422486beac76064b8e6f4fd46300326b088b79b6355e808edbbf0f689af492",
}

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

for path, expected in EXPECTED.items():
    actual = sha(path)

    if actual != expected:
        fail(
            "SHA|"
            + str(path)
            + "|ACTUAL="
            + actual
        )

if COMPLETED.stat().st_size != 4546:
    fail(
        "COMPLETED_REVIEW_SIZE"
    )

# ------------------------------------------------------------
# Immutable handoff Git-tree binding.
# ------------------------------------------------------------

proc = subprocess.run(
    [
        "git",
        "-C",
        str(REPO),
        "rev-parse",
        "HEAD:" + HANDOFF_REL,
    ],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    check=False,
)

if proc.returncode != 0:
    fail(
        "HANDOFF_GIT_TREE_LOOKUP"
    )

if proc.stdout.strip() != \
        "ce4f54ba5b7582988a0bb5e69a63bdf48bdd6f2b":
    fail(
        "HANDOFF_GIT_TREE_CHANGED"
    )

# ------------------------------------------------------------
# Run only safe immutable handoff verifier.
# ------------------------------------------------------------

proc = subprocess.run(
    [
        "python3",
        str(HANDOFF_SAFE),
    ],
    cwd=str(HANDOFF),
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    check=False,
)

if proc.returncode != 0:
    fail(
        "HANDOFF_SAFE_VERIFIER_RC|"
        + str(proc.returncode)
    )

if (
    b"SELF_CONTAINED_EXTERNAL_FOCUSED_REREVIEW_HANDOFF=PASS"
    not in proc.stdout
):
    fail(
        "HANDOFF_SAFE_VERIFIER_PASS_MARKER"
    )

# ------------------------------------------------------------
# Validate completed human-review content.
# ------------------------------------------------------------

text = COMPLETED.read_text(
    encoding="utf-8"
)

required_static = [
    "# Focused Independent Human Rereview — Corrective Successor Package V2",
    "Package state: `BLANK — AWAITING INDEPENDENT HUMAN REREVIEW`",
    "`REVISION_REQUIRED`",
    "`SRR01, SRR03, SRR06, SRR07`",
    "`SRR02-C, SRR04-C, SRR05-C, SRR08-C`",
    "`Spec-Technical-Reviewer-1`",
]

for item in required_static:
    if item not in text:
        fail(
            "STATIC_TEMPLATE|" + item
        )

items = (
    "SRR02-C",
    "SRR04-C",
    "SRR05-C",
    "SRR08-C",
)

decisions = {}

for rid in items:
    section = re.search(
        rf"^## {re.escape(rid)}\b"
        rf"(?P<body>.*?)"
        rf"(?=^## SRR\d{{2}}-C\b|^# Overall focused decision\b)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )

    if not section:
        fail(
            "MISSING_SECTION|" + rid
        )

    d = re.search(
        r"^Decision \(PASS / REVISION_REQUIRED / FAIL\):"
        r"[ \t]*(PASS|REVISION_REQUIRED|FAIL)[ \t]*$",
        section.group("body"),
        flags=re.MULTILINE,
    )

    if not d:
        fail(
            "ITEM_DECISION|" + rid
        )

    note = re.search(
        r"^Reviewer notes:[ \t]*\n"
        r"(?P<note>.*?)(?=\n---|\Z)",
        section.group("body"),
        flags=re.MULTILINE | re.DOTALL,
    )

    if not note or not note.group("note").strip():
        fail(
            "ITEM_NOTES|" + rid
        )

    decisions[rid] = d.group(1)

if list(decisions.values()) != [
    "PASS",
    "PASS",
    "PASS",
    "PASS",
]:
    fail(
        "FOCUSED_DECISION_VECTOR"
    )

overall = re.search(
    r"^Overall decision "
    r"\(APPROVE_CORRECTIVE_SUCCESSOR_PACKAGE_V2 / "
    r"REVISION_REQUIRED / FAIL\):"
    r"[ \t]*(APPROVE_CORRECTIVE_SUCCESSOR_PACKAGE_V2|"
    r"REVISION_REQUIRED|FAIL)[ \t]*$",
    text,
    flags=re.MULTILINE,
)

if not overall:
    fail(
        "OVERALL_DECISION"
    )

if overall.group(1) != \
        "APPROVE_CORRECTIVE_SUCCESSOR_PACKAGE_V2":
    fail(
        "OVERALL_NOT_APPROVED"
    )

expected_identity = {
    "Human reviewer name:":
        "Abdul Raheem Shahzad",

    "Human reviewer signature / recorded confirmation:":
        "ARS",

    "Human reviewer date:":
        "23 / August / 2026",

    "Reviewer role:":
        "Spec-Technical-Reviewer-1",
}

for prefix, expected in expected_identity.items():
    values = [
        line[len(prefix):].strip()
        for line in text.splitlines()
        if line.startswith(prefix)
    ]

    if values != [expected]:
        fail(
            "REVIEWER_IDENTITY|" + prefix
        )

# ------------------------------------------------------------
# Machine-readable record.
# ------------------------------------------------------------

record = json.loads(
    RECORD.read_text(
        encoding="utf-8"
    )
)

if record[
    "status"
] != "COMPLETED_FOCUSED_HUMAN_REVIEW_RECORDED":
    fail(
        "RECORD_STATUS"
    )

if record[
    "overall_focused_decision"
] != "APPROVE_CORRECTIVE_SUCCESSOR_PACKAGE_V2":
    fail(
        "RECORD_OVERALL"
    )

expected_decisions = {
    "SRR02-C": "PASS",
    "SRR04-C": "PASS",
    "SRR05-C": "PASS",
    "SRR08-C": "PASS",
}

if record[
    "focused_item_decisions"
] != expected_decisions:
    fail(
        "RECORD_ITEM_DECISIONS"
    )

review_state = record[
    "review_chain_state"
]

if review_state[
    "original_overall_human_review"
] != "REVISION_REQUIRED":
    fail(
        "ORIGINAL_REVIEW_STATE"
    )

if review_state[
    "focused_items_all_pass"
] is not True:
    fail(
        "FOCUSED_ITEMS_PASS_STATE"
    )

if review_state[
    "focused_human_approval_exists"
] is not True:
    fail(
        "FOCUSED_APPROVAL_STATE"
    )

if review_state[
    "corrective_successor_package_v2_human_approved"
] is not True:
    fail(
        "PACKAGE_HUMAN_APPROVAL"
    )

if review_state[
    "formalization_v1_governance_approval"
] is not False:
    fail(
        "FORMALIZATION_GOVERNANCE_APPROVAL_PREMATURE"
    )

if review_state[
    "revision_chain_governance_closed"
] is not False:
    fail(
        "REVISION_CHAIN_PREMATURELY_CLOSED"
    )

bounded = record[
    "bounded_interpretation"
]

for key in (
    "operational_positive_mapping_authorized",
    "schema_successor_authoring_authorized",
    "schema_version_preselected",
    "schema_v3_authorized",
    "curl_json_authorized",
    "analyzer_implementation_authorized",
    "analyzer_execution_authorized",
    "baseline_execution_authorized",
    "repair_authorized",
):
    if bounded[key] is not False:
        fail(
            "NONAUTH|" + key
        )

# ------------------------------------------------------------
# Evidence checksum closure when present.
# ------------------------------------------------------------

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

    for raw in lines:
        digest, rel = raw.split(
            None,
            1,
        )

        rel = rel.strip()

        if rel.startswith("*"):
            rel = rel[1:]

        if rel.startswith("./"):
            rel = rel[2:]

        target = HERE / rel

        if sha(target) != digest:
            fail(
                "CHECKSUM|" + rel
            )

print("COMPLETED_REVIEW_PACKET_EXACT_BINDING=PASS")
print("IMMUTABLE_BLANK_HANDOFF_PRESERVED=YES")

print("SRR02_C=PASS")
print("SRR04_C=PASS")
print("SRR05_C=PASS")
print("SRR08_C=PASS")

print("OVERALL_FOCUSED_DECISION=APPROVE_CORRECTIVE_SUCCESSOR_PACKAGE_V2")
print("FOCUSED_HUMAN_REVIEW_COMPLETED=YES")
print("FOCUSED_HUMAN_APPROVAL_EXISTS=YES")
print("CORRECTIVE_SUCCESSOR_PACKAGE_V2_HUMAN_APPROVED=YES")

print("ORIGINAL_OVERALL_HUMAN_REVIEW=REVISION_REQUIRED")
print("ORIGINAL_REVIEW_REMAINS_IMMUTABLE=YES")

print("FORMALIZATION_V1_GOVERNANCE_APPROVAL=NO")
print("REVISION_CHAIN_GOVERNANCE_CLOSED=NO")

print("DECISION_0095_VERIFIER_EXECUTED=NO")
print("DECISION_0096_VERIFIER_EXECUTED=NO")
print("DECISION_0098_VERIFIER_EXECUTED=NO")

print("OPERATIONAL_POSITIVE_MAPPING_AUTHORIZED=NO")
print("SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO")
print("CURL_JSON_AUTHORIZED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")

print("REPOSITORY_COMPLETED_FOCUSED_HUMAN_REVIEW=PASS")
