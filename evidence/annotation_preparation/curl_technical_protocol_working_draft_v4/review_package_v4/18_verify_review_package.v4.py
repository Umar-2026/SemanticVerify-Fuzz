#!/usr/bin/env python3

import hashlib
import json
import re
import sys
from pathlib import Path, PurePosixPath


def fail(msg):
    print("FAIL|" + msg)
    raise SystemExit(1)


base = Path(__file__).resolve().parent


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def logical_path(value):
    s = str(value).replace("\\", "/")
    return PurePosixPath(s).as_posix()


def physical_from_logical(root, value):
    logical = logical_path(value)
    return root.joinpath(
        *PurePosixPath(logical).parts
    )


V4_SHA = (
    "e17ae2ea5a70bdd790c946eb4b89ca37368d749cd7463159e69514d88a50cea8"
)

V3_SHA = (
    "2c10317a7a1fa745d64b461bb318ac2aa1e3e23439ca261c8cd746d1ea3f8ac2"
)

V3_REVIEW_SHA = (
    "9a15b13cea29bcbcbfff349c9b9bcb113a9d9a4e01afe03727d7be8dbd87c327"
)

v4p = base / "03_curl_technical_protocol_working_draft.v4.json"
v3p = base / "11_curl_technical_protocol_working_draft.v3.json"
reviewp = base / "10_completed_v3_human_technical_review.v1.md"
packetp = base / "02_curl_technical_v4_reviewer_packet.v1.md"
bindingp = base / "01_repository_binding.v4.json"
tracep = base / "06_v4_metadata_successor_traceability.v1.json"
checkpointp = base / "07_v4_author_checkpoint.v1.json"
authp = base / "08_v4_successor_authorization.v1.json"
source_manifestp = base / "14_approved_source_evidence_manifest.v4.json"
source_root = base / "15_source_evidence"
witness_dir = base / "16_author_checkpoint_git_witness"
package_manifestp = base / "17_review_package_manifest.v4.json"
sumsp = base / "19_review_package.v4.SHA256SUMS"


# ----------------------------------------------------------
# Exact file-set and checksum contract
# ----------------------------------------------------------

source_manifest = json.loads(
    source_manifestp.read_text(encoding="utf-8")
)

expected_source_paths = sorted(
    logical_path(x)
    for x in source_manifest["files"]
)

fixed = {
    "01_repository_binding.v4.json",
    "02_curl_technical_v4_reviewer_packet.v1.md",
    "03_curl_technical_protocol_working_draft.v4.json",
    "04_decision_0036.v1.md",
    "05_v4_successor_author_resolution.v1.json",
    "06_v4_metadata_successor_traceability.v1.json",
    "07_v4_author_checkpoint.v1.json",
    "08_v4_successor_authorization.v1.json",
    "09_decision_0035.v1.md",
    "10_completed_v3_human_technical_review.v1.md",
    "11_curl_technical_protocol_working_draft.v3.json",
    "12_decision_0034.v1.md",
    "13_curl_v3_authoring_scope.v3.json",
    "14_approved_source_evidence_manifest.v4.json",
    "16_author_checkpoint_git_witness/01_author_commit.raw",
    "16_author_checkpoint_git_witness/02_root_tree.raw",
    "16_author_checkpoint_git_witness/03_config_tree.raw",
    "16_author_checkpoint_git_witness/04_annotation_tree.raw",
    "16_author_checkpoint_git_witness/05_documentation_tree.raw",
    "16_author_checkpoint_git_witness/06_decisions_tree.raw",
    "16_author_checkpoint_git_witness/07_v4_blob.raw",
    "16_author_checkpoint_git_witness/08_decision_0036_blob.raw",
    "16_author_checkpoint_git_witness/09_git_witness_manifest.v4.json",
    "17_review_package_manifest.v4.json",
    "18_verify_review_package.v4.py",
    "19_review_package.v4.SHA256SUMS",
}

expected_paths = set(fixed)

for rel in expected_source_paths:
    expected_paths.add(
        "15_source_evidence/" + rel
    )

actual_paths = {
    logical_path(p.relative_to(base).as_posix())
    for p in base.rglob("*")
    if p.is_file()
}

if actual_paths != expected_paths:
    fail(
        "PACKAGE_PATH_SET|"
        f"EXPECTED={len(expected_paths)}|"
        f"OBSERVED={len(actual_paths)}"
    )

if len(actual_paths) != 47:
    fail("PACKAGE_FILE_COUNT|" + str(len(actual_paths)))


lines = [
    x for x in
    sumsp.read_text(encoding="utf-8").splitlines()
    if x.strip()
]

if len(lines) != 46:
    fail("PACKAGE_CHECKSUM_ENTRIES|" + str(len(lines)))

sum_paths = set()

for line in lines:
    parts = line.split(None, 1)

    if len(parts) != 2:
        fail("CHECKSUM_LINE_FORMAT")

    wanted, rel = parts
    rel = logical_path(rel.strip())

    if rel == "19_review_package.v4.SHA256SUMS":
        fail("CHECKSUM_MANIFEST_SELF_REFERENCE")

    p = physical_from_logical(base, rel)

    if not p.is_file():
        fail("CHECKSUM_PATH_MISSING|" + rel)

    if sha256(p) != wanted:
        fail("CHECKSUM_SHA|" + rel)

    sum_paths.add(rel)

if sum_paths != (
    expected_paths
    - {"19_review_package.v4.SHA256SUMS"}
):
    fail("CHECKSUM_PATH_SET")


# ----------------------------------------------------------
# Exact identities
# ----------------------------------------------------------

if sha256(v4p) != V4_SHA:
    fail("V4_SHA")

if v4p.stat().st_size != 41033:
    fail("V4_SIZE")

if sha256(v3p) != V3_SHA:
    fail("V3_SHA")

if v3p.stat().st_size != 41330:
    fail("V3_SIZE")

if sha256(reviewp) != V3_REVIEW_SHA:
    fail("V3_REVIEW_SHA")

if reviewp.stat().st_size != 22983:
    fail("V3_REVIEW_SIZE")


# ----------------------------------------------------------
# V4 metadata and exact protocol preservation
# ----------------------------------------------------------

v4 = json.loads(v4p.read_text(encoding="utf-8"))
v3 = json.loads(v3p.read_text(encoding="utf-8"))

if v4["schema_id"] != \
        "curl.technical-protocol-working-draft.v4":
    fail("V4_SCHEMA")

if v4["status"] != \
        "SOURCE_ONLY_TECHNICAL_WORKING_DRAFT_V4_AUTHOR_CHECKPOINT":
    fail("V4_STATUS")

containers = [
    "api_surface",
    "resources",
    "return_condition_policy",
    "verdict_semantics",
    "defect_taxonomy",
    "global_runtime_rules",
    "easy_handle_rules",
    "multi_handle_rules",
    "cross_resource_rules",
    "exit_obligations",
]

for key in containers:
    if v4[key] != v3[key]:
        fail("PROTOCOL_CONTAINER_CHANGED|" + key)

if len(v4["easy_handle_rules"]) != 21:
    fail("EASY_RULE_COUNT")

if len(v4["multi_handle_rules"]) != 29:
    fail("MULTI_RULE_COUNT")


g = v4["governance"]

required = {
    "working_draft_version": "V4",

    "predecessor_working_draft_version": "V3",

    "predecessor_path":
        "config/annotation/curl_technical_protocol_working_draft.v3.json",

    "predecessor_sha256":
        V3_SHA,

    "predecessor_size_bytes":
        41330,

    "completed_human_review_sha256":
        V3_REVIEW_SHA,

    "completed_human_review_commit":
        "0f6625753452944bbedeab66a77a4098a6e349a9",

    "completed_human_review_tree":
        "a822ec4504071e0edbdc8b77c0eda8ea3974cdbc",

    "completed_human_review_decision":
        "REVISION_REQUIRED",

    "successor_authorization_commit":
        "cee5299cf80b633019ea6c98efc065b46aade1dd",

    "successor_authorization_tree":
        "37528cfdc0379b2e999eb8f8d83c7b036b1bb04e",

    "predecessor_in_place_edit_authorized":
        False,
}

for key, wanted in required.items():
    if g.get(key) != wanted:
        fail(
            "V4_GOVERNANCE|"
            + key
            + "|"
            + repr(g.get(key))
        )

if "v1_in_place_edit_authorized" in g:
    fail("STALE_V1_EDIT_FIELD")


sr = v4["human_review_successor_resolution"]

if sr["source_review_items"] != [
    "V3-RR02",
    "V3-RR12",
]:
    fail("SUCCESSOR_REVIEW_ITEMS")

if sr["implemented_metadata_corrections"] != [
    "V4-C01",
    "V4-C02",
    "V4-C03",
    "V4-C04",
    "V4-C05",
    "V4-C06",
]:
    fail("V4_CORRECTION_SET")

if len(sr["preserved_pass_review_items"]) != 10:
    fail("PASS_PRESERVATION_COUNT")

if sr["accepted_protocol_rule_semantics_preserved"] is not True:
    fail("PROTOCOL_PRESERVATION")


operative = json.dumps(
    {
        "purpose": v4["purpose"],
        "governance": v4["governance"],
        "human_review_successor_resolution":
            v4["human_review_successor_resolution"],
        "explicit_non_claims":
            v4["explicit_non_claims"],
    },
    sort_keys=True,
    ensure_ascii=False,
)

for stale in (
    "Working Draft V2",
    '"working_draft_version": "V2"',
    '"predecessor_working_draft_version": "V1"',
    "curl_technical_protocol_working_draft.v1.json",
    "e253340d540a06cd24af501c569154869ac0324d677995b7266349ba097973cc",
    "eba1cb67f5a7c6b2ea8348634f397204a2bbb0d3",
    "v1_in_place_edit_authorized",
):
    if stale in operative:
        fail("STALE_OPERATIVE_METADATA|" + stale)


# ----------------------------------------------------------
# Exact four-verdict contract
# ----------------------------------------------------------

allowed_verdicts = {
    "VALID",
    "VIOLATION-MUST",
    "VIOLATION-MAY",
    "UNKNOWN",
}

bad_verdicts = []


def walk(obj, path="$"):
    if isinstance(obj, dict):
        for k, value in obj.items():
            p = path + "." + k

            if k in (
                "verdict",
                "missing_cleanup_verdict",
            ) and isinstance(value, str):
                if value not in allowed_verdicts:
                    bad_verdicts.append((p, value))

            walk(value, p)

    elif isinstance(obj, list):
        for i, value in enumerate(obj):
            walk(value, f"{path}[{i}]")


walk(v4)

if bad_verdicts:
    fail(
        "UNDECLARED_MACHINE_VERDICT|"
        + repr(bad_verdicts)
    )


# ----------------------------------------------------------
# Approved source evidence + V4-P01 portability
# ----------------------------------------------------------

if source_manifest["evidence_class"] != \
        "PREAPPROVED_SOURCE_ONLY":
    fail("SOURCE_EVIDENCE_CLASS")

if source_manifest["approved_source_file_count"] != 21:
    fail("SOURCE_FILE_COUNT")

if source_manifest["logical_path_policy"][
    "platform_independent_comparison"
] is not True:
    fail("SOURCE_PATH_POLICY")

actual_source_paths = sorted(
    logical_path(
        p.relative_to(source_root).as_posix()
    )
    for p in source_root.rglob("*")
    if p.is_file()
)

if actual_source_paths != expected_source_paths:
    fail("SOURCE_PATH_SET")

windows_simulated = sorted(
    logical_path(
        x.replace("/", "\\")
    )
    for x in expected_source_paths
)

if windows_simulated != expected_source_paths:
    fail("WINDOWS_PATH_NORMALIZATION")

for rel, wanted in source_manifest["files"].items():
    logical = logical_path(rel)
    p = physical_from_logical(
        source_root,
        logical,
    )

    if sha256(p) != wanted:
        fail("SOURCE_SHA|" + logical)


# ----------------------------------------------------------
# Traceability / checkpoint / authorization / quarantine
# ----------------------------------------------------------

trace = json.loads(tracep.read_text(encoding="utf-8"))

if trace["successor_binding"]["sha256"] != V4_SHA:
    fail("TRACE_V4_SHA")

if trace["preservation_contract"][
    "protocol_rule_semantic_change"
] is not False:
    fail("TRACE_PROTOCOL_CHANGE")

if trace["preservation_contract"][
    "accepted_v3_protocol_semantics_preserved"
] is not True:
    fail("TRACE_PROTOCOL_PRESERVATION")

for k, v in trace["evidence_boundary"].items():
    if k.endswith("_used") and v is not False:
        fail("PROHIBITED_EVIDENCE|" + k)


checkpoint = json.loads(
    checkpointp.read_text(encoding="utf-8")
)

if checkpoint["final_checkpoint_identity"]["sha256"] != V4_SHA:
    fail("CHECKPOINT_V4_SHA")

if checkpoint["protocol_preservation"][
    "all_protocol_containers_preserved"
] is not True:
    fail("CHECKPOINT_PROTOCOL_PRESERVATION")

if checkpoint["protocol_preservation"][
    "protocol_rule_semantic_change"
] is not False:
    fail("CHECKPOINT_PROTOCOL_CHANGE")


auth = json.loads(authp.read_text(encoding="utf-8"))

if auth["authorized_successor"][
    "protocol_rule_semantic_change_authorized"
] is not False:
    fail("AUTH_PROTOCOL_CHANGE")

if auth["authorized_successor"][
    "canonicalization_authorized"
] is not False:
    fail("AUTH_CANONICALIZATION")


# ----------------------------------------------------------
# Minimal Git witness
# ----------------------------------------------------------

wmanifest = json.loads(
    (
        witness_dir
        / "09_git_witness_manifest.v4.json"
    ).read_text(encoding="utf-8")
)

if wmanifest["author_checkpoint_commit"] != \
        "b98d76536376b21fc6f2e85a060e960e1681453c":
    fail("WITNESS_COMMIT")

if wmanifest["author_checkpoint_tree"] != \
        "e7243cda2f8afd9b6cceff793ab0cfa723fabbe5":
    fail("WITNESS_ROOT_TREE")

if wmanifest["witness_object_counts"] != {
    "commit": 1,
    "tree": 5,
    "blob": 2,
    "total_raw_objects": 8,
}:
    fail("WITNESS_OBJECT_COUNTS")

if wmanifest["parent_commit_objects_present"] is not False:
    fail("WITNESS_PARENT_OBJECT_BOUNDARY")


ids = wmanifest["object_ids"]

commit_raw = (
    witness_dir / "01_author_commit.raw"
).read_text(encoding="utf-8")

root_raw = (
    witness_dir / "02_root_tree.raw"
).read_text(encoding="utf-8")

config_raw = (
    witness_dir / "03_config_tree.raw"
).read_text(encoding="utf-8")

annotation_raw = (
    witness_dir / "04_annotation_tree.raw"
).read_text(encoding="utf-8")

documentation_raw = (
    witness_dir / "05_documentation_tree.raw"
).read_text(encoding="utf-8")

decisions_raw = (
    witness_dir / "06_decisions_tree.raw"
).read_text(encoding="utf-8")


if "tree e7243cda2f8afd9b6cceff793ab0cfa723fabbe5" \
        not in commit_raw:
    fail("WITNESS_COMMIT_TREE_CHAIN")

if f"tree {ids['config_tree']}\tconfig" not in root_raw:
    fail("WITNESS_CONFIG_TREE_CHAIN")

if f"tree {ids['documentation_tree']}\tdocumentation" not in root_raw:
    fail("WITNESS_DOCUMENTATION_TREE_CHAIN")

if f"tree {ids['annotation_tree']}\tannotation" not in config_raw:
    fail("WITNESS_ANNOTATION_TREE_CHAIN")

if f"tree {ids['decisions_tree']}\tdecisions" not in documentation_raw:
    fail("WITNESS_DECISIONS_TREE_CHAIN")

if (
    f"blob {ids['v4_blob']}\t"
    "curl_technical_protocol_working_draft.v4.json"
) not in annotation_raw:
    fail("WITNESS_V4_BLOB_CHAIN")

if (
    f"blob {ids['decision_0036_blob']}\t"
    "0036-curl-technical-working-draft-v4-author-checkpoint.md"
) not in decisions_raw:
    fail("WITNESS_D36_BLOB_CHAIN")

if (
    witness_dir / "07_v4_blob.raw"
).read_bytes() != v4p.read_bytes():
    fail("WITNESS_V4_BLOB_BYTES")

if (
    witness_dir / "08_decision_0036_blob.raw"
).read_bytes() != (
    base / "04_decision_0036.v1.md"
).read_bytes():
    fail("WITNESS_D36_BLOB_BYTES")


# ----------------------------------------------------------
# Blank human-review state
# ----------------------------------------------------------

packet = packetp.read_text(encoding="utf-8")
packet_norm = packet.replace("\\_", "_")

for i in range(1, 13):
    rr = f"V4-RR{i:02d}"

    hs = list(
        re.finditer(
            rf"^###\s+{re.escape(rr)}\b[^\n]*$",
            packet_norm,
            re.M,
        )
    )

    if len(hs) != 1:
        fail(
            "REVIEW_HEADING_COUNT|"
            + rr
            + "|"
            + str(len(hs))
        )

    tail = packet_norm[hs[0].end():]

    nxt = re.search(
        r"^###\s+V4-RR\d{2}\b[^\n]*$|"
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
    packet_norm,
    re.M,
)

if len(overall_blank) != 1:
    fail("OVERALL_DECISION_NOT_BLANK")


for label in (
    "Human reviewer name",
    "Human reviewer signature / recorded confirmation",
    "Human reviewer date",
):
    vals = re.findall(
        r"^"
        + re.escape(label)
        + r":[ \t]*(.*)$",
        packet_norm,
        re.M,
    )

    if len(vals) != 1:
        fail("REVIEWER_FIELD_COUNT|" + label)

    if vals[0].strip():
        fail("REVIEWER_FIELD_NOT_BLANK|" + label)


role = re.findall(
    r"^Reviewer role ID:[ \t]*`([^`]+)`[ \t]*$",
    packet_norm,
    re.M,
)

if role != ["Spec-Technical-Reviewer-1"]:
    fail("REVIEWER_ROLE")


# ----------------------------------------------------------
# Package manifest / non-authorization
# ----------------------------------------------------------

pm = json.loads(
    package_manifestp.read_text(encoding="utf-8")
)

if pm["package_file_contract"]["expected_total_file_count"] != 47:
    fail("PACKAGE_MANIFEST_FILE_COUNT")

if pm["v4_p01"][
    "platform_independent_logical_source_path_comparison"
] != "IMPLEMENTED_IN_PACKAGE_VERIFIER":
    fail("PACKAGE_V4_P01")

if pm["v4_p02"][
    "fresh_v4_bound_review_package"
] != "IMPLEMENTED_BY_THIS_PACKAGE":
    fail("PACKAGE_V4_P02")

if pm["v4_p02"]["independent_human_review"] != "PENDING":
    fail("HUMAN_REVIEW_STATE")

for k, v in pm["non_authorizations"].items():
    if v is not False:
        fail("NON_AUTHORIZATION|" + k)


binding = json.loads(
    bindingp.read_text(encoding="utf-8")
)

if binding["review_target"]["sha256"] != V4_SHA:
    fail("BINDING_V4_SHA")

if binding["human_review_state"]["V4_RR01_to_V4_RR12"] != "BLANK":
    fail("BINDING_REVIEW_STATE")


print("PACKAGE_FILE_COUNT=47")
print("PACKAGE_CHECKSUM_ENTRIES=46")
print("EXACT_WORKING_DRAFT_V4_SHA256=PASS")
print("EXACT_WORKING_DRAFT_V4_SIZE=PASS")
print("EXACT_WORKING_DRAFT_V3_PREDECESSOR=PASS")
print("COMPLETED_V3_HUMAN_REVIEW_BINDING=PASS")
print("V4_C01_TO_V4_C06_METADATA_CORRECTIONS=PASS")
print("PROTOCOL_CONTAINERS_PRESERVED=10_OF_10")
print("EASY_HANDLE_RULE_COUNT=21")
print("MULTI_HANDLE_RULE_COUNT=29")
print("NEW_PROTOCOL_RULE_COUNT=0")
print("REMOVED_PROTOCOL_RULE_COUNT=0")
print("PROTOCOL_RULE_SEMANTIC_CHANGE=NONE")
print("STALE_OPERATIVE_V1_V2_SUCCESSOR_METADATA=NONE")
print("FOUR_MACHINE_VERDICT_CONTRACT=PASS")
print("APPROVED_SOURCE_EVIDENCE=21_OF_21_PASS")
print("V4_P01_PLATFORM_INDEPENDENT_PATH_COMPARISON=PASS")
print("WINDOWS_BACKSLASH_NORMALIZATION_SELF_TEST=PASS")
print("V4_P02_FRESH_V4_BOUND_PACKAGE=PASS")
print("V4_SUCCESSOR_BOUND_TRACEABILITY=PASS")
print("PROHIBITED_EVIDENCE_USED=NO")
print("AUTHOR_CHECKPOINT_GIT_WITNESS_COMMIT=PASS")
print("AUTHOR_CHECKPOINT_GIT_WITNESS_TREE_CHAIN=PASS")
print("AUTHOR_CHECKPOINT_GIT_WITNESS_V4_BLOB=PASS")
print("AUTHOR_CHECKPOINT_GIT_WITNESS_D36_BLOB=PASS")
print("V4_RR01_TO_V4_RR12_DECISIONS=BLANK")
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
print("CURL_TECHNICAL_WORKING_DRAFT_V4_REVIEW_PACKAGE_VERIFICATION=PASS")
