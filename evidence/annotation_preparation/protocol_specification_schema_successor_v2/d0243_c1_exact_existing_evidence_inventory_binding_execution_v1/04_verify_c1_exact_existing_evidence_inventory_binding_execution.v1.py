#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys


D0242_COMMIT = "de713b4b0d74a27ed4d7451644d0d492e05fa6d5"
D0242_TREE = "5369fdd85e2e26fde95df951188aacc5ecc7f0a7"
D0242_MANIFEST_SHA = "814abe0cd08a3cf0fccc7114237781441b95f4de9f5b1720bf3f969017964ab4"

EXPECTED_MEMBER_IDS = {
    "C1-G01",
    "C1-G02",
    "C1-G03",
    "C1-G04",
    "C1-G05",
    "C1-S01",
    "C1-S02",
    "C1-S03",
    "C1-S04",
}

EXPECTED_PROVENANCE_DECISIONS = {
    "D0181",
    "D0189",
    "D0191",
    "D0201",
}


def die(reason):
    print("D0243_C1_EXECUTION_VERIFIER=FAIL")
    print("FAIL_REASON=" + reason)
    sys.exit(1)


def sha256(path):
    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()


def canonical_json_bytes(obj):
    return json.dumps(
        obj,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


repo = Path(
    os.environ.get(
        "SVF_REPO_ROOT",
        subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"],
            text=True,
        ).strip(),
    )
)

pkg = Path(
    os.environ.get(
        "SVF_PACKAGE_DIR",
        Path(__file__).resolve().parent,
    )
)

decision = Path(
    os.environ.get(
        "SVF_DECISION_PATH",
        repo /
        "documentation/decisions/"
        "0243-execute-c1-exact-existing-evidence-inventory-binding.md",
    )
)

authorization_record_path = (
    repo /
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2/"
    "d0242_c1_exact_existing_evidence_inventory_binding_authorization_v1/"
    "01_c1_exact_existing_evidence_inventory_binding_authorization.v1.json"
)

inventory_path = (
    pkg /
    "01_c1_exact_existing_evidence_inventory.v1.json"
)

detached_path = (
    pkg /
    "02_c1_inventory_detached_hash_binding.v1.json"
)

boundary_path = (
    pkg /
    "03_c1_execution_boundary.v1.md"
)

manifest_path = (
    pkg /
    "05_c1_exact_existing_evidence_inventory_binding_execution.v1.SHA256SUMS"
)

for path in [
    authorization_record_path,
    inventory_path,
    detached_path,
    boundary_path,
    manifest_path,
    decision,
]:
    if not path.is_file():
        die("missing:" + str(path))


# ------------------------------------------------------------------
# D0242 authorization binding
# ------------------------------------------------------------------

actual_d0242_tree = subprocess.check_output(
    [
        "git",
        "-C",
        str(repo),
        "rev-parse",
        D0242_COMMIT + "^{tree}",
    ],
    text=True,
).strip()

if actual_d0242_tree != D0242_TREE:
    die("D0242_TREE_BINDING")


auth = json.loads(
    authorization_record_path.read_text(
        encoding="utf-8"
    )
)

if auth["decision"] != "D0242":
    die("AUTH_DECISION")

if auth["status"] != "C1_AUTHORIZED_NOT_EXECUTED":
    die("AUTH_STATUS")

if auth["authorization"]["authorized"] is not True:
    die("C1_NOT_AUTHORIZED")

if auth["authorization"]["executed"] is not False:
    die("AUTH_RECORD_EXECUTION_STATE")

if auth["authorization"]["designated_future_execution"] != "D0243":
    die("DESIGNATED_EXECUTION")

if auth["exact_input_set"]["total_member_count"] != 9:
    die("AUTH_INPUT_COUNT")

if auth["exact_input_set"]["source_expansion_allowed"] is not False:
    die("AUTH_SOURCE_EXPANSION")


# ------------------------------------------------------------------
# Parse canonical D0243 inventory
# ------------------------------------------------------------------

inventory_raw = inventory_path.read_bytes()

duplicate_keys = []


def object_pairs_hook(pairs):
    out = {}

    for key, value in pairs:
        if key in out:
            duplicate_keys.append(key)

        out[key] = value

    return out


try:
    inventory = json.loads(
        inventory_raw.decode("utf-8"),
        object_pairs_hook=object_pairs_hook,
    )
except Exception as exc:
    die("INVENTORY_JSON:" + repr(exc))

if duplicate_keys:
    die("INVENTORY_DUPLICATE_KEYS")

if inventory_raw != canonical_json_bytes(inventory):
    die("INVENTORY_NOT_CANONICAL_JSON")

if inventory_raw.endswith(b"\n"):
    die("INVENTORY_FINAL_LF")

required_inventory_keys = {
    "artifact_id",
    "decision",
    "status",
    "authorization_binding",
    "inventory_summary",
    "inventory_entries",
    "governing_decision_provenance",
    "execution_boundaries",
    "results_not_established",
    "next_required_checkpoint",
}

if set(inventory) != required_inventory_keys:
    die("INVENTORY_TOP_LEVEL_KEYS")

if inventory["artifact_id"] != \
    "SVF-D0243-C1-EXACT-EXISTING-EVIDENCE-INVENTORY-V1":
    die("INVENTORY_ARTIFACT_ID")

if inventory["decision"] != "D0243":
    die("INVENTORY_DECISION")

if inventory["status"] != \
    "C1_EXECUTED_IDENTITY_PROVENANCE_INVENTORY_ONLY":
    die("INVENTORY_STATUS")


binding = inventory["authorization_binding"]

if binding["decision"] != "D0242":
    die("INVENTORY_AUTH_DECISION")

if binding["commit"] != D0242_COMMIT:
    die("INVENTORY_AUTH_COMMIT")

if binding["tree"] != D0242_TREE:
    die("INVENTORY_AUTH_TREE")

if binding["manifest_sha256"] != D0242_MANIFEST_SHA:
    die("INVENTORY_AUTH_MANIFEST")

if binding["C1_authorized"] is not True:
    die("INVENTORY_AUTH_C1")


# ------------------------------------------------------------------
# Exact 9-member authorization/inventory equivalence
# ------------------------------------------------------------------

authorized_members = {
    m["member_id"]: m
    for m in auth["exact_input_set"]["members"]
}

if set(authorized_members) != EXPECTED_MEMBER_IDS:
    die("AUTHORIZED_MEMBER_SET")

entries = inventory["inventory_entries"]

if len(entries) != 9:
    die("INVENTORY_ENTRY_COUNT")

entry_ids = [
    entry["member_id"]
    for entry in entries
]

expected_order = sorted(
    EXPECTED_MEMBER_IDS,
    key=lambda x: x.encode("utf-8"),
)

if entry_ids != expected_order:
    die("INVENTORY_ENTRY_ORDER")

if len(set(entry_ids)) != 9:
    die("INVENTORY_MEMBER_DUPLICATE")

for entry in entries:
    member_id = entry["member_id"]

    if member_id not in authorized_members:
        die("UNAUTHORIZED_MEMBER:" + member_id)

    authorized = authorized_members[member_id]

    expected_keys = {
        "member_id",
        "class",
        "role",
        "path",
        "authorized_sha256",
        "recomputed_sha256",
        "sha256_match",
        "authorized_git_blob",
        "recomputed_git_blob",
        "git_blob_match",
        "governing_decision_if_present",
    }

    if set(entry) != expected_keys:
        die("ENTRY_KEYS:" + member_id)

    if entry["class"] != authorized["class"]:
        die("ENTRY_CLASS:" + member_id)

    if entry["role"] != authorized["role"]:
        die("ENTRY_ROLE:" + member_id)

    if entry["path"] != authorized["path"]:
        die("ENTRY_PATH:" + member_id)

    if entry["authorized_sha256"] != authorized["sha256"]:
        die("ENTRY_AUTH_SHA:" + member_id)

    if entry["authorized_git_blob"] != authorized["git_blob"]:
        die("ENTRY_AUTH_BLOB:" + member_id)

    expected_governing = authorized.get(
        "governing_decision"
    )

    if entry["governing_decision_if_present"] != expected_governing:
        die("ENTRY_GOVERNING_DECISION:" + member_id)

    source_path = repo / entry["path"]

    if not source_path.is_file():
        die("ENTRY_SOURCE_MISSING:" + member_id)

    actual_sha = sha256(
        source_path
    )

    actual_blob = subprocess.check_output(
        [
            "git",
            "-C",
            str(repo),
            "rev-parse",
            "HEAD:" + entry["path"],
        ],
        text=True,
    ).strip()

    if actual_sha != entry["recomputed_sha256"]:
        die("ENTRY_RECOMPUTED_SHA:" + member_id)

    if actual_sha != entry["authorized_sha256"]:
        die("ENTRY_SHA_MISMATCH:" + member_id)

    if entry["sha256_match"] is not True:
        die("ENTRY_SHA_MATCH_FLAG:" + member_id)

    if actual_blob != entry["recomputed_git_blob"]:
        die("ENTRY_RECOMPUTED_BLOB:" + member_id)

    if actual_blob != entry["authorized_git_blob"]:
        die("ENTRY_BLOB_MISMATCH:" + member_id)

    if entry["git_blob_match"] is not True:
        die("ENTRY_BLOB_MATCH_FLAG:" + member_id)


# ------------------------------------------------------------------
# Summary
# ------------------------------------------------------------------

summary = inventory["inventory_summary"]

expected_summary = {
    "total_member_count": 9,
    "substantive_member_count": 4,
    "governance_support_member_count": 5,
    "all_sha256_matches": True,
    "all_git_blob_matches": True,
    "source_expansion_performed": False,
    "source_content_semantic_parse_performed": False,
    "source_record_arrays_enumerated": False,
    "source_pair_records_enumerated": False,
    "candidate_records_enumerated": False,
    "requirement_records_enumerated": False,
    "identity_only_multi_input_aggregation_performed": True,
    "semantic_cross_source_join_performed": False,
}

if summary != expected_summary:
    die("INVENTORY_SUMMARY")


# ------------------------------------------------------------------
# Governing decision provenance
# ------------------------------------------------------------------

authorized_provenance = {
    p["decision"]: p
    for p in auth["governing_decision_provenance"]
}

if set(authorized_provenance) != EXPECTED_PROVENANCE_DECISIONS:
    die("AUTHORIZED_PROVENANCE_SET")

provenance = inventory["governing_decision_provenance"]

if len(provenance) != 4:
    die("PROVENANCE_COUNT")

provenance_ids = [
    p["decision"]
    for p in provenance
]

expected_provenance_order = sorted(
    EXPECTED_PROVENANCE_DECISIONS,
    key=lambda x: x.encode("utf-8"),
)

if provenance_ids != expected_provenance_order:
    die("PROVENANCE_ORDER")

for p in provenance:
    decision_id = p["decision"]

    authorized = authorized_provenance[
        decision_id
    ]

    expected_keys = {
        "decision",
        "path",
        "authorized_sha256",
        "recomputed_sha256",
        "sha256_match",
        "authorized_git_blob",
        "recomputed_git_blob",
        "git_blob_match",
        "introducing_commit",
        "introducing_tree",
        "recomputed_introducing_tree",
        "commit_tree_match",
    }

    if set(p) != expected_keys:
        die("PROVENANCE_KEYS:" + decision_id)

    if p["path"] != authorized["path"]:
        die("PROVENANCE_PATH:" + decision_id)

    if p["authorized_sha256"] != authorized["sha256"]:
        die("PROVENANCE_AUTH_SHA:" + decision_id)

    if p["authorized_git_blob"] != authorized["git_blob"]:
        die("PROVENANCE_AUTH_BLOB:" + decision_id)

    if p["introducing_commit"] != authorized["introducing_commit"]:
        die("PROVENANCE_COMMIT:" + decision_id)

    if p["introducing_tree"] != authorized["introducing_tree"]:
        die("PROVENANCE_TREE:" + decision_id)

    fp = repo / p["path"]

    if not fp.is_file():
        die("PROVENANCE_FILE_MISSING:" + decision_id)

    actual_sha = sha256(
        fp
    )

    actual_blob = subprocess.check_output(
        [
            "git",
            "-C",
            str(repo),
            "rev-parse",
            "HEAD:" + p["path"],
        ],
        text=True,
    ).strip()

    actual_tree = subprocess.check_output(
        [
            "git",
            "-C",
            str(repo),
            "rev-parse",
            p["introducing_commit"] + "^{tree}",
        ],
        text=True,
    ).strip()

    if actual_sha != p["recomputed_sha256"]:
        die("PROVENANCE_RECOMPUTED_SHA:" + decision_id)

    if actual_sha != p["authorized_sha256"]:
        die("PROVENANCE_SHA_MISMATCH:" + decision_id)

    if p["sha256_match"] is not True:
        die("PROVENANCE_SHA_FLAG:" + decision_id)

    if actual_blob != p["recomputed_git_blob"]:
        die("PROVENANCE_RECOMPUTED_BLOB:" + decision_id)

    if actual_blob != p["authorized_git_blob"]:
        die("PROVENANCE_BLOB_MISMATCH:" + decision_id)

    if p["git_blob_match"] is not True:
        die("PROVENANCE_BLOB_FLAG:" + decision_id)

    if actual_tree != p["recomputed_introducing_tree"]:
        die("PROVENANCE_RECOMPUTED_TREE:" + decision_id)

    if actual_tree != p["introducing_tree"]:
        die("PROVENANCE_TREE_MISMATCH:" + decision_id)

    if p["commit_tree_match"] is not True:
        die("PROVENANCE_TREE_FLAG:" + decision_id)


# ------------------------------------------------------------------
# Execution boundary exact semantics
# ------------------------------------------------------------------

boundaries = inventory["execution_boundaries"]

required_true = {
    "C1_authorized",
    "C1_executed",
    "existing_evidence_inventory_materialized",
}

for key in required_true:
    if boundaries.get(key) is not True:
        die("BOUNDARY_TRUE:" + key)

required_false = {
    "existing_evidence_operational_reuse_performed",
    "new_evidence_acquired",
    "unlisted_source_expansion_performed",
    "candidate_admissibility_evaluated",
    "candidate_disposition_values_created",
    "supported_binding_promoted_to_INCLUDED",
    "unresolved_binding_promoted_to_EXCLUDED",
    "negative_proof_inferred_from_absence",
    "AEA01_constructed",
    "AEA02_constructed",
    "U_domain_constructed",
    "C_domain_constructed",
    "domain_freeze_created",
    "domain_freeze_commit_created",
    "semantic_cross_source_join_performed",
    "concrete_mapping_created",
    "Req06_Req14_determination_performed",
    "pair_reclassification_performed",
    "C2_authorized",
    "C3_authorized",
    "C4_authorized",
    "C5_authorized",
    "C6_authorized",
    "B2_readiness_established",
    "B2_authorized",
    "B2_executed",
    "B3_authorized",
    "B4_authorized",
    "B5_authorized",
    "B6_authorized",
    "B7_authorized",
    "active_schema_v2_materialization_authorized",
    "analyzer_authorized",
    "baseline_authorized",
    "repair_authorized",
}

for key in required_false:
    if boundaries.get(key) is not False:
        die("BOUNDARY_FALSE:" + key)

if set(boundaries) != (required_true | required_false):
    die("BOUNDARY_KEY_SET")


results = inventory["results_not_established"]

if any(
    value is not False
    for value in results.values()
):
    die("RESULT_NONESTABLISHMENT")


if inventory["next_required_checkpoint"] != \
    "INDEPENDENT_READ_ONLY_VERIFY_D0243_BEFORE_ANY_C2_AUTHORIZATION_OR_DOWNSTREAM_WORK":
    die("NEXT_CHECKPOINT")


# ------------------------------------------------------------------
# Detached binding
# ------------------------------------------------------------------

detached_raw = detached_path.read_bytes()

detached_duplicates = []


def detached_hook(pairs):
    out = {}

    for key, value in pairs:
        if key in out:
            detached_duplicates.append(key)

        out[key] = value

    return out


try:
    detached = json.loads(
        detached_raw.decode("utf-8"),
        object_pairs_hook=detached_hook,
    )
except Exception as exc:
    die("DETACHED_JSON:" + repr(exc))

if detached_duplicates:
    die("DETACHED_DUPLICATE_KEYS")

if detached_raw != canonical_json_bytes(detached):
    die("DETACHED_NOT_CANONICAL_JSON")

if detached_raw.endswith(b"\n"):
    die("DETACHED_FINAL_LF")

if detached["artifact_id"] != \
    "SVF-D0243-C1-INVENTORY-DETACHED-HASH-BINDING-V1":
    die("DETACHED_ARTIFACT_ID")

if detached["decision"] != "D0243":
    die("DETACHED_DECISION")

if detached["status"] != "DETACHED_BINDING_COMPLETE":
    die("DETACHED_STATUS")

db = detached["authorization_binding"]

if db != {
    "decision": "D0242",
    "commit": D0242_COMMIT,
    "tree": D0242_TREE,
    "manifest_sha256": D0242_MANIFEST_SHA,
}:
    die("DETACHED_AUTH_BINDING")

primary = detached["primary_inventory_binding"]

expected_inventory_sha = hashlib.sha256(
    inventory_raw
).hexdigest()

if primary["sha256"] != expected_inventory_sha:
    die("DETACHED_INVENTORY_SHA")

if primary["size_bytes"] != len(inventory_raw):
    die("DETACHED_INVENTORY_SIZE")

if primary["canonical_inventory_entry_count"] != 9:
    die("DETACHED_ENTRY_COUNT")

expected_inventory_rel = (
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2/"
    "d0243_c1_exact_existing_evidence_inventory_binding_execution_v1/"
    "01_c1_exact_existing_evidence_inventory.v1.json"
)

if primary["path"] != expected_inventory_rel:
    die("DETACHED_INVENTORY_PATH")

if detached["self_hash_included"] is not False:
    die("DETACHED_SELF_HASH")

if detached["execution_commit_declared"] is not False:
    die("DETACHED_EXECUTION_COMMIT")


# ------------------------------------------------------------------
# Human-readable boundary / decision
# ------------------------------------------------------------------

boundary = boundary_path.read_text(
    encoding="utf-8"
)

decision_text = decision.read_text(
    encoding="utf-8"
)

boundary_markers = [
    "C1_AUTHORIZED_AND_EXECUTED_IDENTITY_PROVENANCE_INVENTORY_ONLY",
    "`C1_AUTHORIZED=YES`",
    "`C1_EXECUTED=YES`",
    "`EXISTING_EVIDENCE_INVENTORY_MATERIALIZED=YES`",
    "`EXISTING_EVIDENCE_OPERATIONAL_REUSE_PERFORMED=NO`",
    "`NEW_EVIDENCE_ACQUIRED=NO`",
    "`CANDIDATE_ADMISSIBILITY_EVALUATED=NO`",
    "`CANDIDATE_DISPOSITION_VALUES_CREATED=NO`",
    "`SUPPORTED_BINDING_PROMOTED_TO_INCLUDED=NO`",
    "`UNRESOLVED_BINDING_PROMOTED_TO_EXCLUDED=NO`",
    "`NEGATIVE_PROOF_INFERRED_FROM_ABSENCE=NO`",
    "`SEMANTIC_CROSS_SOURCE_JOIN_PERFORMED=NO`",
    "`CONCRETE_MAPPING_CREATED=NO`",
    "`REQ06_REQ14_DETERMINATION_PERFORMED=NO`",
    "`PAIR_RECLASSIFICATION_PERFORMED=NO`",
    "`C2_AUTHORIZED=NO`",
    "`C3_AUTHORIZED=NO`",
    "`C4_AUTHORIZED=NO`",
    "`C5_AUTHORIZED=NO`",
    "`C6_AUTHORIZED=NO`",
    "`B2_READINESS_ESTABLISHED=NO`",
    "`B2_AUTHORIZED=NO`",
    "`B2_EXECUTED=NO`",
]

for marker in boundary_markers:
    if marker not in boundary:
        die("BOUNDARY_MARKER:" + marker)

decision_markers = [
    "`C1_AUTHORIZED=YES`",
    "`C1_EXECUTED=YES`",
    "`EXISTING_EVIDENCE_INVENTORY_MATERIALIZED=YES`",
    "`EXISTING_EVIDENCE_OPERATIONAL_REUSE_PERFORMED=NO`",
    "`NEW_EVIDENCE_ACQUIRED=NO`",
    "`CANDIDATE_ADMISSIBILITY_EVALUATED=NO`",
    "`CANDIDATE_DISPOSITION_VALUES_CREATED=NO`",
    "`SEMANTIC_CROSS_SOURCE_JOIN_PERFORMED=NO`",
    "`CONCRETE_MAPPING_CREATED=NO`",
    "`REQ06_REQ14_DETERMINATION_PERFORMED=NO`",
    "`PAIR_RECLASSIFICATION_PERFORMED=NO`",
    "`C2_AUTHORIZED=NO`",
    "`B2_READINESS_ESTABLISHED=NO`",
    "`B2_AUTHORIZED=NO`",
    "`B2_EXECUTED=NO`",
]

for marker in decision_markers:
    if marker not in decision_text:
        die("DECISION_MARKER:" + marker)


# ------------------------------------------------------------------
# Package manifest
# ------------------------------------------------------------------

manifest_lines = [
    line
    for line in manifest_path.read_text(
        encoding="utf-8"
    ).splitlines()
    if line.strip()
]

if len(manifest_lines) != 4:
    die("MANIFEST_ENTRY_COUNT")

expected_manifest_files = {
    "01_c1_exact_existing_evidence_inventory.v1.json",
    "02_c1_inventory_detached_hash_binding.v1.json",
    "03_c1_execution_boundary.v1.md",
    "04_verify_c1_exact_existing_evidence_inventory_binding_execution.v1.py",
}

seen_manifest = set()

for line in manifest_lines:
    parts = line.split("  ", 1)

    if len(parts) != 2:
        die("MANIFEST_FORMAT")

    declared_hash, name = parts

    if name not in expected_manifest_files:
        die("MANIFEST_NAME:" + name)

    fp = pkg / name

    if sha256(fp) != declared_hash:
        die("MANIFEST_HASH:" + name)

    seen_manifest.add(name)

if seen_manifest != expected_manifest_files:
    die("MANIFEST_COVERAGE")


print("D0243_C1_EXECUTION_VERIFIER=PASS")
print("D0242_AUTHORIZATION_BINDING=PASS")

print("C1_AUTHORIZED=YES")
print("C1_EXECUTED=YES")

print("C1_EXACT_INVENTORY_MEMBER_COUNT=9")
print("C1_SUBSTANTIVE_MEMBER_COUNT=4")
print("C1_GOVERNANCE_SUPPORT_MEMBER_COUNT=5")

print("C1_ALL_NINE_SHA256_IDENTITIES=PASS")
print("C1_ALL_NINE_GIT_BLOB_IDENTITIES=PASS")

print("C1_GOVERNING_DECISION_PROVENANCE_COUNT=4")
print("C1_GOVERNING_DECISION_PROVENANCE_BINDINGS=PASS")

print("C1_PRIMARY_INVENTORY_CANONICAL_JSON=YES")
print("C1_PRIMARY_INVENTORY_FINAL_LF=NO")
print("C1_DETACHED_BINDING_CANONICAL_JSON=YES")
print("C1_DETACHED_BINDING_FINAL_LF=NO")

print("EXISTING_EVIDENCE_INVENTORY_MATERIALIZED=YES")
print("EXISTING_EVIDENCE_OPERATIONAL_REUSE_PERFORMED=NO")

print("NEW_EVIDENCE_ACQUIRED=NO")
print("SOURCE_EXPANSION_PERFORMED=NO")
print("SOURCE_CONTENT_SEMANTIC_PARSE_PERFORMED=NO")

print("CANDIDATE_ADMISSIBILITY_EVALUATED=NO")
print("CANDIDATE_DISPOSITION_VALUES_CREATED=NO")

print("SEMANTIC_CROSS_SOURCE_JOIN_PERFORMED=NO")
print("CONCRETE_MAPPING_CREATED=NO")

print("REQ06_REQ14_DETERMINATION_PERFORMED=NO")
print("PAIR_RECLASSIFICATION_PERFORMED=NO")

print("C2_AUTHORIZED=NO")
print("C3_AUTHORIZED=NO")
print("C4_AUTHORIZED=NO")
print("C5_AUTHORIZED=NO")
print("C6_AUTHORIZED=NO")

print("B2_READINESS_ESTABLISHED=NO")
print("B2_AUTHORIZED=NO")
print("B2_EXECUTED=NO")

print("SAFE_D0243_VERIFIER=PASS")
