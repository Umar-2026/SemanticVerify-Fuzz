#!/usr/bin/env python3

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

README = ROOT / "00_README_FOCUSED_REREVIEW.v1.md"
MANIFEST = ROOT / "01_external_focused_rereview_handoff_manifest.v1.json"
PACKET = ROOT / "02_focused_rereview_packet.MANUAL_REVIEW_COPY.v1.md"
SELF = ROOT / "03_verify_external_focused_rereview_handoff.v1.py"
CONSUMED = ROOT / "04_decision_0098_authorization_verifier_consumed.v1.json"
SUMS = ROOT / "05_external_focused_rereview_handoff.v1.SHA256SUMS"
BINDINGS = ROOT / "06_source_binding_manifest.v1.json"

SUCCESSOR = ROOT / "corrective_successor_package_v2_exact"
COMP = ROOT / "recovery_completion_v1_exact"
AUTH = ROOT / "decision_0098_authorization_exact"
DEC = ROOT / "governance_decisions_exact"

SOURCE_SAFE = SUCCESSOR / "05_verify_corrective_successor_package_v2.py"
SOURCE_BLANK = SUCCESSOR / "04_focused_rereview_packet.BLANK.v2.md"

A01 = AUTH / "01_focused_rereview_handoff_authorization.v1.json"
A02 = AUTH / "02_verify_focused_rereview_handoff_authorization.v1.py"
A03 = AUTH / "03_focused_rereview_handoff_authorization.v1.SHA256SUMS"
A04 = AUTH / "04_final_allowed_handoff_authorization_verifier_output.v1.txt"

D97 = DEC / "0097-record-recovery-completion-and-corrective-successor-package-v2-author-checkpoint.md"
D98 = DEC / "0098-authorize-external-focused-rereview-handoff-for-corrective-successor-package-v2.md"

EXPECTED_FIXED = {
    A01:
        "45b3963a0a942752b14991445923f834221116fc893e2bc32730caf2811a5fbc",

    A02:
        "c7471c76132ec2a5cd1889eaec4ae6ad549f5b59a694d556bf08be7634ee51d4",

    A03:
        "9cb0cf0fdfe492798891aeb9ab3992d9d5d4a15768ed4a0ffb8dfb3a78984db7",

    D97:
        "0df5e4527dcbc130bd11327d1c3dd5c4f170552a2761ffb61e55fcfe64bc1923",

    D98:
        "41225b0e6f8f0c92c022e5f138f88ed7c39f055b2e4541819a66f4fdc07f6d0c",

    SOURCE_BLANK:
        "60185126f93d5a113722545108c4b798563b6088f9b92945ccb7cd16840db75e",

    SOURCE_SAFE:
        "2c053a69dd183faa896364a61e5a2c337876c59735313c421e2acb63cd13a63a",
}

def fail(msg):
    print("FAIL|" + msg)
    raise SystemExit(1)

def sha(path):
    if not path.is_file():
        fail(
            "MISSING|" + str(path.relative_to(ROOT))
        )

    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()

# ------------------------------------------------------------
# Package-local requirement.
# ------------------------------------------------------------

script_text = SELF.read_text(
    encoding="utf-8"
)

absolute_prefix = "/" + "openbayes" + "/"

if absolute_prefix in script_text:
    fail(
        "HANDOFF_VERIFIER_CONTAINS_OPENBAYES_ABSOLUTE_PATH"
    )

# ------------------------------------------------------------
# Fixed exact bindings.
# ------------------------------------------------------------

for path, expected in EXPECTED_FIXED.items():
    actual = sha(path)

    if actual != expected:
        fail(
            "FIXED_SHA|"
            + str(path.relative_to(ROOT))
            + "|ACTUAL="
            + actual
        )

# Root packet must initially be byte-exact blank packet.
if PACKET.read_bytes() != SOURCE_BLANK.read_bytes():
    fail(
        "MANUAL_REVIEW_PACKET_NOT_EXACT_INITIAL_BLANK_COPY"
    )

# ------------------------------------------------------------
# Source binding manifest.
# ------------------------------------------------------------

bindings = json.loads(
    BINDINGS.read_text(
        encoding="utf-8"
    )
)

if bindings[
    "corrective_successor_package_v2_source_git_tree"
] != "3ac8a4b0d19917a12ea02db208becf87d4b81f8f":
    fail(
        "SUCCESSOR_GIT_TREE_BINDING"
    )

if bindings[
    "recovery_completion_v1_source_git_tree"
] != "b51b921c570a74be310bfc192b15970b4f3b4f83":
    fail(
        "COMPLETION_GIT_TREE_BINDING"
    )

group_roots = {
    "corrective_successor_package_v2_exact":
        SUCCESSOR,

    "recovery_completion_v1_exact":
        COMP,

    "decision_0098_authorization_exact":
        AUTH,

    "governance_decisions_exact":
        DEC,
}

for group_name, root in group_roots.items():
    group = bindings[
        "groups"
    ][
        group_name
    ]

    expected_count = bindings[
        "expected_group_file_counts"
    ][
        group_name
    ]

    if group["file_count"] != expected_count:
        fail(
            "BINDING_GROUP_DECLARED_COUNT|"
            + group_name
        )

    expected_paths = set()

    for row in group["files"]:
        rel = row["path"]
        target = root / rel

        expected_paths.add(rel)

        if sha(target) != row["sha256"]:
            fail(
                "BINDING_SHA|"
                + group_name
                + "|"
                + rel
            )

        if target.stat().st_size != row["size_bytes"]:
            fail(
                "BINDING_SIZE|"
                + group_name
                + "|"
                + rel
            )

    actual_paths = {
        str(p.relative_to(root))
        for p in root.rglob("*")
        if p.is_file()
    }

    if actual_paths != expected_paths:
        fail(
            "BINDING_FILE_SET|"
            + group_name
        )

# ------------------------------------------------------------
# Decision-0098 final authorization consumption.
# Do NOT execute A02.
# ------------------------------------------------------------

consumed = json.loads(
    CONSUMED.read_text(
        encoding="utf-8"
    )
)

if consumed[
    "authorization_verifier_sha256"
] != EXPECTED_FIXED[A02]:
    fail(
        "CONSUMED_AUTH_VERIFIER_SHA"
    )

if consumed[
    "final_allowed_run_result"
] != "PASS":
    fail(
        "CONSUMED_FINAL_RESULT"
    )

if consumed[
    "final_allowed_run_performed"
] is not True:
    fail(
        "CONSUMED_FINAL_RUN"
    )

if consumed[
    "handoff_authoring_started_after_final_run"
] is not True:
    fail(
        "CONSUMED_HANDOFF_START"
    )

if consumed[
    "authorization_verifier_permanently_retired"
] is not True:
    fail(
        "CONSUMED_RETIREMENT"
    )

if consumed[
    "authorization_verifier_must_never_be_rerun"
] is not True:
    fail(
        "CONSUMED_NEVER_RERUN"
    )

if sha(A04) != consumed[
    "final_allowed_output_sha256"
]:
    fail(
        "FINAL_AUTH_OUTPUT_SHA"
    )

if A04.stat().st_size != consumed[
    "final_allowed_output_size_bytes"
]:
    fail(
        "FINAL_AUTH_OUTPUT_SIZE"
    )

if (
    "DECISION_0098_FOCUSED_REREVIEW_HANDOFF_AUTHORIZATION=PASS"
    not in A04.read_text(
        encoding="utf-8"
    )
):
    fail(
        "FINAL_AUTH_OUTPUT_PASS_MARKER"
    )

# ------------------------------------------------------------
# Run only copied current successor SAFE verifier.
# ------------------------------------------------------------

proc = subprocess.run(
    [
        sys.executable,
        str(SOURCE_SAFE),
    ],
    cwd=str(SUCCESSOR),
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    check=False,
)

if proc.returncode != 0:
    fail(
        "COPIED_SUCCESSOR_SAFE_VERIFIER_RC|"
        + str(proc.returncode)
    )

if b"CORRECTIVE_SUCCESSOR_PACKAGE_V2=PASS" not in proc.stdout:
    fail(
        "COPIED_SUCCESSOR_SAFE_VERIFIER_PASS_MARKER"
    )

# ------------------------------------------------------------
# Handoff manifest and review scope.
# ------------------------------------------------------------

manifest = json.loads(
    MANIFEST.read_text(
        encoding="utf-8"
    )
)

if manifest[
    "status"
] != "BLANK_EXTERNAL_FOCUSED_REREVIEW_HANDOFF_READY":
    fail(
        "HANDOFF_STATUS"
    )

scope = manifest[
    "review_scope"
]

if scope["focused_items"] != [
    "SRR02-C",
    "SRR04-C",
    "SRR05-C",
    "SRR08-C",
]:
    fail(
        "FOCUSED_ITEM_SET"
    )

if scope[
    "carried_forward_pass_items"
] != [
    "SRR01",
    "SRR03",
    "SRR06",
    "SRR07",
]:
    fail(
        "CARRIED_FORWARD_SET"
    )

if scope[
    "original_overall_human_review"
] != "REVISION_REQUIRED":
    fail(
        "ORIGINAL_REVIEW_STATE"
    )

review_state = manifest[
    "human_review_state"
]

if review_state[
    "focused_rereview_packet"
] != "BLANK":
    fail(
        "FOCUSED_PACKET_STATE"
    )

if review_state[
    "focused_human_decision_exists"
] is not False:
    fail(
        "FOCUSED_DECISION_EXISTS"
    )

if review_state[
    "focused_human_approval_exists"
] is not False:
    fail(
        "FOCUSED_APPROVAL_EXISTS"
    )

if review_state[
    "formalization_v1_approved"
] is not False:
    fail(
        "FORMALIZATION_APPROVAL"
    )

for key, value in manifest[
    "bounded_nonclaims"
].items():
    if value is not False:
        fail(
            "NONCLAIM|" + key
        )

# ------------------------------------------------------------
# Reviewer packet MUST remain blank at handoff checkpoint.
# ------------------------------------------------------------

text = PACKET.read_text(
    encoding="utf-8"
)

for rid in (
    "SRR02-C",
    "SRR04-C",
    "SRR05-C",
    "SRR08-C",
):
    section = re.search(
        rf"^## {re.escape(rid)}\b"
        rf"(?P<body>.*?)"
        rf"(?=^## SRR\d{{2}}-C\b|^# Overall focused decision\b)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )

    if not section:
        fail(
            "REVIEW_SECTION|" + rid
        )

    if not re.search(
        r"^Decision \(PASS / REVISION_REQUIRED / FAIL\):[ \t]*$",
        section.group("body"),
        flags=re.MULTILINE,
    ):
        fail(
            "ITEM_DECISION_NOT_BLANK|" + rid
        )

if not re.search(
    r"^Overall decision "
    r"\(APPROVE_CORRECTIVE_SUCCESSOR_PACKAGE_V2 / "
    r"REVISION_REQUIRED / FAIL\):[ \t]*$",
    text,
    flags=re.MULTILINE,
):
    fail(
        "OVERALL_DECISION_NOT_BLANK"
    )

for prefix in (
    "Human reviewer name:",
    "Human reviewer signature / recorded confirmation:",
    "Human reviewer date:",
):
    vals = [
        line[len(prefix):].strip()
        for line in text.splitlines()
        if line.startswith(prefix)
    ]

    if vals != [""]:
        fail(
            "REVIEWER_IDENTITY_NOT_BLANK|"
            + prefix
        )

roles = [
    line[len("Reviewer role:"):].strip()
    for line in text.splitlines()
    if line.startswith("Reviewer role:")
]

if roles != ["Spec-Technical-Reviewer-1"]:
    fail(
        "REVIEWER_ROLE"
    )

# ------------------------------------------------------------
# Handoff checksum closure, when authored.
# ------------------------------------------------------------

if SUMS.is_file():
    lines = [
        line
        for line in SUMS.read_text(
            encoding="utf-8"
        ).splitlines()
        if line.strip()
    ]

    if len(lines) != 64:
        fail(
            "HANDOFF_CHECKSUM_ENTRY_COUNT|"
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

        target = ROOT / rel

        if sha(target) != digest:
            fail(
                "HANDOFF_CHECKSUM|"
                + rel
            )

actual_file_count = sum(
    1
    for p in ROOT.rglob("*")
    if p.is_file()
)

if actual_file_count != 65:
    fail(
        "HANDOFF_FILE_COUNT|"
        + str(actual_file_count)
    )

print("HANDOFF_FILE_COUNT=65")
print("HANDOFF_CHECKSUM_ENTRY_COUNT=64")

print("CORRECTIVE_SUCCESSOR_PACKAGE_V2_EXACT_COPY=PASS")
print("RECOVERY_COMPLETION_V1_EXACT_COPY=PASS")
print("DECISION_0097_EXACT_COPY=PASS")
print("DECISION_0098_EXACT_COPY=PASS")
print("DECISION_0098_AUTHORIZATION_EVIDENCE_EXACT_COPY=PASS")

print("DECISION_0098_AUTHORIZATION_VERIFIER_EXECUTED=NO")
print("DECISION_0098_AUTHORIZATION_VERIFIER_PERMANENTLY_RETIRED=YES")
print("DECISION_0098_AUTHORIZATION_VERIFIER_RERUN_ALLOWED=NO")

print("COPIED_CORRECTIVE_SUCCESSOR_SAFE_VERIFIER=PASS")

print("ORIGINAL_OVERALL_HUMAN_REVIEW=REVISION_REQUIRED")
print("CARRIED_FORWARD_PASS_ITEMS=SRR01,SRR03,SRR06,SRR07")
print("FOCUSED_REREVIEW_ITEMS=SRR02-C,SRR04-C,SRR05-C,SRR08-C")

print("FOCUSED_REREVIEW_PACKET=BLANK")
print("FOCUSED_REVIEWER_IDENTITY_PREPOPULATED=NO")
print("FOCUSED_HUMAN_DECISION_EXISTS=NO")
print("FOCUSED_HUMAN_APPROVAL_EXISTS=NO")
print("FORMALIZATION_V1_APPROVED=NO")

print("OPERATIONAL_POSITIVE_MAPPING_AUTHORIZED=NO")
print("SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO")
print("CURL_JSON_AUTHORIZED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")

print("SELF_CONTAINED_EXTERNAL_FOCUSED_REREVIEW_HANDOFF=PASS")
