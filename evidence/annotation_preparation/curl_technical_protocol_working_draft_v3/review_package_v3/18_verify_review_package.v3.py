#!/usr/bin/env python3

import hashlib
import json
import re
import sys
from pathlib import Path


def fail(msg):
    print("FAIL|" + msg)
    raise SystemExit(1)


base = Path(__file__).resolve().parent

V3_SHA = (
    "2c10317a7a1fa745d64b461bb318ac2aa1e3e23439ca261c8cd746d1ea3f8ac2"
)
V3_SIZE = 41330

V2_SHA = (
    "63c17bbd0a09365fad9d3f0445fdc2115a8a0e945f622a39c745f31e1baf3d31"
)

V2_REVIEW_SHA = (
    "597699068c3ba7bf480204c67d88d940f400c7425442a081a18198908b1e029e"
)

SCOPE_SHA = (
    "ede7e1422b9553f73377432474deb282852b619a5b004cd7c4d00033c0a37abb"
)

AUTHOR_COMMIT = (
    "d4c41e682882f6053fd6657a7f0f82a402697354"
)

AUTHOR_TREE = (
    "d6878d64e639566a5cedaa95891947c23815b989"
)

AUTHOR_PARENT = (
    "15d96d809cb7c9e03ac3baf49500fcb206987fad"
)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_oid(obj_type, data):
    header = (
        obj_type.encode("ascii")
        + b" "
        + str(len(data)).encode("ascii")
        + b"\0"
    )
    return hashlib.sha1(header + data).hexdigest()


def parse_tree(data):
    result = {}
    i = 0

    while i < len(data):
        sp = data.index(b" ", i)
        mode = data[i:sp].decode("ascii")

        nul = data.index(b"\0", sp + 1)
        name = data[sp + 1:nul].decode("utf-8")

        oid_raw = data[nul + 1:nul + 21]

        if len(oid_raw) != 20:
            fail("TRUNCATED_TREE_ENTRY|" + name)

        oid = oid_raw.hex()
        result[name] = (mode, oid)

        i = nul + 21

    return result


# ----------------------------------------------------------
# Package structure and checksums
# ----------------------------------------------------------

files = sorted(
    p for p in base.rglob("*")
    if p.is_file()
)

if len(files) != 47:
    fail("PACKAGE_FILE_COUNT|" + str(len(files)))

sums = base / "19_review_package.v3.SHA256SUMS"

entries = []

for line in sums.read_text(encoding="utf-8").splitlines():
    if not line.strip():
        continue

    m = re.match(r"^([0-9a-f]{64})  (.+)$", line)

    if not m:
        fail("CHECKSUM_LINE_FORMAT|" + line)

    wanted, rel = m.groups()
    p = base / rel

    if not p.is_file():
        fail("CHECKSUM_TARGET_MISSING|" + rel)

    got = sha256(p)

    if got != wanted:
        fail(
            "CHECKSUM_MISMATCH|"
            + rel
            + "|EXPECTED="
            + wanted
            + "|OBSERVED="
            + got
        )

    entries.append(rel)

if len(entries) != 46:
    fail("CHECKSUM_ENTRY_COUNT|" + str(len(entries)))

if "19_review_package.v3.SHA256SUMS" in entries:
    fail("CHECKSUM_FILE_MUST_NOT_HASH_ITSELF")


manifest = json.loads(
    (base / "17_review_package_manifest.v3.json")
    .read_text(encoding="utf-8")
)

if manifest["expected_total_package_file_count"] != 47:
    fail("MANIFEST_FILE_COUNT")

if manifest["expected_checksum_entry_count"] != 46:
    fail("MANIFEST_CHECKSUM_COUNT")


# ----------------------------------------------------------
# Exact target and predecessor
# ----------------------------------------------------------

v3_path = base / "03_curl_technical_protocol_working_draft.v3.json"
v2_path = base / "11_curl_technical_protocol_working_draft.v2.json"

if sha256(v3_path) != V3_SHA:
    fail("V3_SHA")

if v3_path.stat().st_size != V3_SIZE:
    fail("V3_SIZE")

if sha256(v2_path) != V2_SHA:
    fail("V2_SHA")

if sha256(
    base / "10_completed_v2_human_technical_review.v1.md"
) != V2_REVIEW_SHA:
    fail("COMPLETED_V2_REVIEW_SHA")

if sha256(
    base / "13_curl_v3_authoring_scope.v3.json"
) != SCOPE_SHA:
    fail("FROZEN_SCOPE_SHA")


v2 = json.loads(v2_path.read_text(encoding="utf-8"))
v3 = json.loads(v3_path.read_text(encoding="utf-8"))


def rule(rules, rid):
    xs = [
        x for x in rules
        if isinstance(x, dict)
        and x.get("rule_id") == rid
    ]

    if len(xs) != 1:
        fail("RULE_COUNT|" + rid + "|" + str(len(xs)))

    return xs[0]


if v3.get("schema_id") != \
        "curl.technical-protocol-working-draft.v3":
    fail("V3_SCHEMA")

if v3.get("status") != \
        "SOURCE_ONLY_TECHNICAL_WORKING_DRAFT_V3_AUTHOR_CHECKPOINT":
    fail("V3_STATUS")

if v3.get("api_surface") != v2.get("api_surface"):
    fail("API_SURFACE_CHANGED")


# Authorized V3 corrections.
if (
    v3["resources"]
    ["EXPLICIT_GLOBAL_CLEANUP_OBLIGATION"]
    ["missing_at_exit_normative_status"]
    != "MUST"
):
    fail("V3_GLOBAL_CLEANUP_STATUS")

e04 = rule(v3["easy_handle_rules"], "E04")

if e04.get("enforcement") != "SOURCE_GROUNDED":
    fail("E04_ENFORCEMENT")

if "review_item" in e04:
    fail("E04_OPERATIVE_REVIEW_ITEM")

if e04.get("runtime_post_state") != [
    "RUNTIME_UNINITIALIZED",
    "RUNTIME_READY_IMPLICIT_ONLY",
]:
    fail("E04_RUNTIME_POST_STATE")


m10 = rule(v3["multi_handle_rules"], "M10")
m11 = rule(v3["multi_handle_rules"], "M11")

if m10.get("precondition") != \
        "supplied multi is live and valid and easy is live":
    fail("M10_PRECONDITION")

if m11.get("precondition") != \
        "supplied multi is live and valid and easy is live":
    fail("M11_PRECONDITION")

if m11.get("defect") != "D7":
    fail("M11_DEFECT")

if m11.get("verdict") != "VIOLATION-MUST":
    fail("M11_VERDICT")

if "CURLM_BAD_EASY_HANDLE" not in m11.get("effect", ""):
    fail("M11_RETURN")

if "actual original multi" not in m11.get("effect", ""):
    fail("M11_MEMBERSHIP")


expected_new = {
    "M26": ("curl_multi_add_handle", "D1"),
    "M27": ("curl_multi_remove_handle", "D1"),
    "M28": ("curl_multi_add_handle", "D2"),
    "M29": ("curl_multi_remove_handle", "D2"),
}

for rid, (fn, defect) in expected_new.items():
    x = rule(v3["multi_handle_rules"], rid)

    if x.get("function") != fn:
        fail(rid + "|FUNCTION")

    if x.get("argument_scope") != "easy_argument":
        fail(rid + "|ARGUMENT_SCOPE")

    if x.get("defect") != defect:
        fail(rid + "|DEFECT")

    if x.get("enforcement") != "MUST":
        fail(rid + "|ENFORCEMENT")

    if x.get("verdict") != "VIOLATION-MUST":
        fail(rid + "|VERDICT")

    if "CURLM_BAD_EASY_HANDLE" not in \
            x.get("return_behavior", ""):
        fail(rid + "|RETURN")

    if "membership" not in x.get("effect", ""):
        fail(rid + "|MEMBERSHIP")


# Preserve accepted V2 subjects.
for rid in ("M07", "M08", "M09", "M12", "M13", "M24", "M25"):
    if rule(v2["multi_handle_rules"], rid) != \
            rule(v3["multi_handle_rules"], rid):
        fail("PRESERVED_MULTI_RULE_CHANGED|" + rid)

if v2["global_runtime_rules"] != v3["global_runtime_rules"]:
    fail("GLOBAL_RUNTIME_RULES_CHANGED")

if v2["cross_resource_rules"] != v3["cross_resource_rules"]:
    fail("CROSS_RESOURCE_RULES_CHANGED")


# Four-verdict contract.
allowed = {
    "VALID",
    "VIOLATION-MUST",
    "VIOLATION-MAY",
    "UNKNOWN",
}

bad = []


def walk(o, path="$"):
    if isinstance(o, dict):
        for k, v in o.items():
            p = path + "." + k

            if k in ("verdict", "missing_cleanup_verdict") \
                    and isinstance(v, str) \
                    and v not in allowed:
                bad.append((p, v))

            walk(v, p)

    elif isinstance(o, list):
        for i, v in enumerate(o):
            walk(v, f"{path}[{i}]")


walk(v3)

if bad:
    fail("UNDECLARED_MACHINE_VERDICT|" + repr(bad))


# ----------------------------------------------------------
# Traceability and approved source evidence
# ----------------------------------------------------------

trace = json.loads(
    (base / "06_v3_successor_rule_source_traceability.v1.json")
    .read_text(encoding="utf-8")
)

if trace["successor_binding"]["sha256"] != V3_SHA:
    fail("TRACE_V3_SHA")

if trace["evidence_class"] != "PREAPPROVED_SOURCE_ONLY":
    fail("TRACE_EVIDENCE_CLASS")

subjects = [
    x["successor_subject"]
    for x in trace["corrected_subject_traceability"]
]

if subjects != [
    "resources.EXPLICIT_GLOBAL_CLEANUP_OBLIGATION."
    "missing_at_exit_normative_status",
    "E04",
    "M10",
    "M11",
    "M26",
    "M27",
    "M28",
    "M29",
]:
    fail("TRACE_SUBJECTS")

for k, v in trace["explicit_quarantine"].items():
    if v is not False:
        fail("PROHIBITED_EVIDENCE_USED|" + k)


source_manifest = json.loads(
    (base / "14_approved_source_evidence_manifest.v3.json")
    .read_text(encoding="utf-8")
)

if source_manifest["evidence_class"] != "PREAPPROVED_SOURCE_ONLY":
    fail("SOURCE_MANIFEST_EVIDENCE_CLASS")

if source_manifest["approved_source_file_count"] != 21:
    fail("SOURCE_MANIFEST_COUNT")

source_root = base / "15_source_evidence"

actual_source_paths = sorted(
    str(p.relative_to(source_root))
    for p in source_root.rglob("*")
    if p.is_file()
)

if actual_source_paths != sorted(source_manifest["files"]):
    fail("SOURCE_PATH_SET")

for rel, wanted in source_manifest["files"].items():
    p = source_root / rel

    if sha256(p) != wanted:
        fail("SOURCE_SHA|" + rel)


# ----------------------------------------------------------
# Minimal independent Git witness verification
# ----------------------------------------------------------

wdir = base / "16_author_checkpoint_git_witness"

wm = json.loads(
    (wdir / "09_git_witness_manifest.v3.json")
    .read_text(encoding="utf-8")
)

objects = wm["objects"]

types = {
    "commit": "commit",
    "root_tree": "tree",
    "config_tree": "tree",
    "annotation_tree": "tree",
    "documentation_tree": "tree",
    "decisions_tree": "tree",
    "v3_blob": "blob",
    "decision_0033_blob": "blob",
}

for key, typ in types.items():
    p = wdir / objects[key]["file"]
    got = git_oid(typ, p.read_bytes())

    if got != objects[key]["oid"]:
        fail(
            "GIT_OBJECT_OID|"
            + key
            + "|EXPECTED="
            + objects[key]["oid"]
            + "|OBSERVED="
            + got
        )


commit_text = (
    wdir / objects["commit"]["file"]
).read_text(encoding="utf-8")

m_tree = re.search(r"^tree ([0-9a-f]{40})$", commit_text, re.M)
m_parent = re.search(r"^parent ([0-9a-f]{40})$", commit_text, re.M)

if not m_tree or m_tree.group(1) != AUTHOR_TREE:
    fail("COMMIT_TREE_BINDING")

if not m_parent or m_parent.group(1) != AUTHOR_PARENT:
    fail("COMMIT_PARENT_BINDING")

if objects["commit"]["oid"] != AUTHOR_COMMIT:
    fail("COMMIT_OID_BINDING")


root_tree = parse_tree(
    (wdir / objects["root_tree"]["file"]).read_bytes()
)

if root_tree.get("config", (None, None))[1] != \
        objects["config_tree"]["oid"]:
    fail("ROOT_TO_CONFIG_TREE")

if root_tree.get("documentation", (None, None))[1] != \
        objects["documentation_tree"]["oid"]:
    fail("ROOT_TO_DOCUMENTATION_TREE")


config_tree = parse_tree(
    (wdir / objects["config_tree"]["file"]).read_bytes()
)

if config_tree.get("annotation", (None, None))[1] != \
        objects["annotation_tree"]["oid"]:
    fail("CONFIG_TO_ANNOTATION_TREE")


annotation_tree = parse_tree(
    (wdir / objects["annotation_tree"]["file"]).read_bytes()
)

if annotation_tree.get(
    "curl_technical_protocol_working_draft.v3.json",
    (None, None),
)[1] != objects["v3_blob"]["oid"]:
    fail("ANNOTATION_TO_V3_BLOB")


documentation_tree = parse_tree(
    (wdir / objects["documentation_tree"]["file"]).read_bytes()
)

if documentation_tree.get("decisions", (None, None))[1] != \
        objects["decisions_tree"]["oid"]:
    fail("DOCUMENTATION_TO_DECISIONS_TREE")


decisions_tree = parse_tree(
    (wdir / objects["decisions_tree"]["file"]).read_bytes()
)

if decisions_tree.get(
    "0033-curl-technical-working-draft-v3-author-checkpoint.md",
    (None, None),
)[1] != objects["decision_0033_blob"]["oid"]:
    fail("DECISIONS_TO_D33_BLOB")


if (
    wdir / objects["v3_blob"]["file"]
).read_bytes() != v3_path.read_bytes():
    fail("V3_BLOB_NOT_BYTE_IDENTICAL")

if (
    wdir / objects["decision_0033_blob"]["file"]
).read_bytes() != (
    base / "04_decision_0033.v1.md"
).read_bytes():
    fail("D33_BLOB_NOT_BYTE_IDENTICAL")


# ----------------------------------------------------------
# Blank independent human-review state
# ----------------------------------------------------------

packet_path = base / "02_curl_technical_v3_reviewer_packet.v1.md"
packet_raw = packet_path.read_text(encoding="utf-8")
packet = packet_raw.replace("\\_", "_")

for i in range(1, 13):
    rr = f"V3-RR{i:02d}"

    hs = list(
        re.finditer(
            rf"^###\s+{re.escape(rr)}\b[^\n]*$",
            packet,
            re.M,
        )
    )

    if len(hs) != 1:
        fail("REVIEW_HEADING_COUNT|" + rr)

    tail = packet[hs[0].end():]

    nxt = re.search(
        r"^###\s+V3-RR\d{2}\b[^\n]*$|"
        r"^##\s+Overall technical review decision\b",
        tail,
        re.M,
    )

    section = tail[:nxt.start()] if nxt else tail

    blank = re.findall(
        r"^Decision:[ \t]*$",
        section,
        re.M,
    )

    populated = re.findall(
        r"^Decision:[ \t]*(PASS|REVISION_REQUIRED|FAIL)[ \t]*$",
        section,
        re.M,
    )

    if len(blank) != 1:
        fail("REVIEW_DECISION_NOT_BLANK|" + rr)

    if populated:
        fail("SYNTHETIC_REVIEW_DECISION|" + rr)


overall_blank = re.findall(
    r"^Overall decision:[ \t]*$",
    packet,
    re.M,
)

overall_populated = re.findall(
    r"^Overall decision:[ \t]*(.+?)[ \t]*$",
    packet,
    re.M,
)

if len(overall_blank) != 1:
    fail("OVERALL_DECISION_NOT_BLANK")

if overall_populated:
    fail("SYNTHETIC_OVERALL_DECISION")


role = re.findall(
    r"^Reviewer role ID:[ \t]*`([^`]+)`[ \t]*$",
    packet,
    re.M,
)

if role != ["Spec-Technical-Reviewer-1"]:
    fail("REVIEWER_ROLE")


for label in (
    "Human reviewer name",
    "Human reviewer signature / recorded confirmation",
    "Human reviewer date",
):
    vals = re.findall(
        r"^" + re.escape(label) + r":[ \t]*(.*)$",
        packet,
        re.M,
    )

    if len(vals) != 1 or vals[0].strip():
        fail("HUMAN_IDENTITY_NOT_BLANK|" + label)


if "No assistant-generated or synthetic human approval is permitted." \
        not in packet:
    fail("NO_SYNTHETIC_APPROVAL_RULE_MISSING")


# ----------------------------------------------------------
# Binding record and non-authorizations
# ----------------------------------------------------------

binding = json.loads(
    (base / "01_repository_binding.v3.json")
    .read_text(encoding="utf-8")
)

if binding["review_target"]["sha256"] != V3_SHA:
    fail("BINDING_V3_SHA")

if binding["author_checkpoint"]["commit"] != AUTHOR_COMMIT:
    fail("BINDING_AUTHOR_COMMIT")

if binding["author_checkpoint"]["tree"] != AUTHOR_TREE:
    fail("BINDING_AUTHOR_TREE")

if binding["predecessor_v2"]["sha256"] != V2_SHA:
    fail("BINDING_V2_SHA")

if binding["reviewer_state"]["review_item_decisions"] != "BLANK":
    fail("BINDING_REVIEW_DECISIONS")

if binding["reviewer_state"]["overall_decision"] != "BLANK":
    fail("BINDING_OVERALL_DECISION")

if binding["reviewer_state"]["human_identity"] != "BLANK":
    fail("BINDING_HUMAN_IDENTITY")

for k, v in binding["non_authorizations"].items():
    if v is not False:
        fail("NON_AUTHORIZATION_CHANGED|" + k)


print("PACKAGE_FILE_COUNT=47")
print("PACKAGE_CHECKSUM_ENTRIES=46")
print("EXACT_WORKING_DRAFT_V3_SHA256=PASS")
print("EXACT_WORKING_DRAFT_V3_SIZE=PASS")
print("EXACT_WORKING_DRAFT_V2_PREDECESSOR=PASS")
print("COMPLETED_V2_HUMAN_REVIEW_BINDING=PASS")
print("EXACT_FROZEN_V3_SCOPE_BINDING=PASS")
print("V3_C01_TO_V3_C08_STRUCTURAL_CHECK=PASS")
print("PRESERVED_V2_PASS_SUBJECTS=PASS")
print("FOUR_MACHINE_VERDICT_CONTRACT=PASS")
print("APPROVED_SOURCE_EVIDENCE=21_OF_21_PASS")
print("V3_SUCCESSOR_BOUND_TRACEABILITY=PASS")
print("PROHIBITED_EVIDENCE_USED=NO")
print("AUTHOR_CHECKPOINT_GIT_WITNESS_COMMIT=PASS")
print("AUTHOR_CHECKPOINT_GIT_WITNESS_TREE_CHAIN=PASS")
print("AUTHOR_CHECKPOINT_GIT_WITNESS_V3_BLOB=PASS")
print("AUTHOR_CHECKPOINT_GIT_WITNESS_D33_BLOB=PASS")
print("V3_RR01_TO_V3_RR12_DECISIONS=BLANK")
print("OVERALL_TECHNICAL_REVIEW_DECISION=BLANK")
print("HUMAN_REVIEWER_IDENTITY_FIELDS=BLANK")
print("REVIEWER_ROLE_ID=Spec-Technical-Reviewer-1")
print("CANONICAL_CURL_SPECIFICATION_AUTHORIZED=NO")
print("GENERATED_DRIVER_INSPECTION_AUTHORIZED=NO")
print("SELECTED_SAMPLE_MEMBERSHIP_INSPECTION_AUTHORIZED=NO")
print("GOLD_ANNOTATION_AUTHORIZED=NO")
print("ANALYZER_IMPLEMENTATION_AUTHORIZED=NO")
print("ANALYZER_EXECUTION_AUTHORIZED=NO")
print("BASELINE_EXECUTION_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
print("CURL_TECHNICAL_WORKING_DRAFT_V3_REVIEW_PACKAGE_VERIFICATION=PASS")
