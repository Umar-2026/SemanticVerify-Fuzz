#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import os
import subprocess

D0245_COMMIT = "17bce507c7e71d3d7571ebb911e839cca88bca6c"
D0245_TREE = "0d225d78d8f4cdee982ba2da322ecaa8e766c6a2"
D0245_MANIFEST_SHA = "1d88bfe50f65bce1ce784196ac0afdfda11c009f3fb7d9be1ff741c07489a141"

D0244_COMMIT = "5f30a418e73f53b9f4cbc9fbf0260249f4f9dc4a"
D0244_TREE = "1739b38b6d43019e04f9324911f63c98c74443fa"
D0244_RECORD_SHA = "a8c51e2614c337e6a265101b6ccb30d43e8a8ebfd76108883cab67d81002039b"
D0244_ROOT_SET_SHA = "4fceb4501bc84b3d43d9b2b7591cc84fc4bebcaaa23218c68ac7bbd6fe8bb3bf"

D0244_RECORD = "evidence/annotation_preparation/protocol_specification_schema_successor_v2/d0244_bounded_crosswalk_locator_discovery_authorization_v1/01_bounded_crosswalk_locator_discovery_authorization.v1.json"

D0245_MANIFEST = "evidence/annotation_preparation/protocol_specification_schema_successor_v2/d0245_d0244_postcommit_verifier_binding_corrective_successor_v1/04_d0244_postcommit_verifier_binding_corrective_successor.v1.SHA256SUMS"

EXPECTED_TOKENS = [
    "requirement",
    "semantic",
    "unit",
    "crosswalk",
    "binding",
    "mapping",
    "matrix",
    "traceability",
    "adjudication",
    "evidence",
]

EXPECTED_OPERATIONS = [
    "ENUMERATE_IMMEDIATE_TRACKED_CHILD_PATH_NAMES_OF_EXACTLY_THE_THREE_D0244_BOUND_GIT_TREE_OBJECTS",
    "RECORD_GIT_MODE_OBJECT_TYPE_AND_OBJECT_ID_FOR_EACH_IMMEDIATE_CHILD",
    "APPLY_ONLY_THE_EXACT_D0244_FIXED_CASE_INSENSITIVE_FILENAME_TOKEN_FILTER",
    "MATERIALIZE_DETACHED_LOCATOR_CANDIDATE_INVENTORY",
]

EXPECTED_STOP = [
    "EACH_OF_THE_THREE_EXACT_BOUND_ROOT_TREE_OBJECTS_ENUMERATED_EXACTLY_ONCE",
    "ONLY_IMMEDIATE_TRACKED_CHILDREN_ENUMERATED",
    "EVERY_CHILD_CLASSIFIED_ONLY_BY_THE_FIXED_D0244_LEXICAL_FILENAME_FILTER",
    "NO_OTHER_ROOT_LOCATOR_HISTORY_OR_NETWORK_RESOURCE_ACCESSED",
]

repo = Path(
    os.environ.get(
        "SVF_REPO_ROOT",
        "/openbayes/home/semanticverify-fuzz-research",
    )
)

pkg = Path(
    os.environ.get(
        "SVF_PACKAGE_DIR",
        Path(__file__).resolve().parent,
    )
)

record_path = pkg / "01_replacement_bounded_crosswalk_locator_discovery_execution_authorization.v1.json"
scope_path = pkg / "02_replacement_bounded_crosswalk_locator_discovery_execution_authorization_scope.v1.md"


def run_text(*args):
    return subprocess.check_output(
        args,
        cwd=repo,
        text=True,
    ).strip()


def run_bytes(*args):
    return subprocess.check_output(
        args,
        cwd=repo,
    )


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def no_dup(pairs):
    out = {}
    for k, v in pairs:
        if k in out:
            raise AssertionError(
                "duplicate JSON key: " + k
            )
        out[k] = v
    return out


# ------------------------------------------------------------
# A. D0245 must be current HEAD or an ancestor.
# ------------------------------------------------------------

current_head = run_text(
    "git",
    "rev-parse",
    "HEAD",
)

ancestor_rc = subprocess.run(
    [
        "git",
        "merge-base",
        "--is-ancestor",
        D0245_COMMIT,
        current_head,
    ],
    cwd=repo,
).returncode

assert ancestor_rc == 0

assert run_text(
    "git",
    "rev-parse",
    f"{D0245_COMMIT}^{{tree}}",
) == D0245_TREE

assert run_text(
    "git",
    "rev-parse",
    f"{D0245_COMMIT}^",
) == D0244_COMMIT

manifest_bytes = run_bytes(
    "git",
    "show",
    f"{D0245_COMMIT}:{D0245_MANIFEST}",
)

assert sha256_bytes(manifest_bytes) == D0245_MANIFEST_SHA

# ------------------------------------------------------------
# B. Load immutable D0244 record directly from D0244 commit.
# ------------------------------------------------------------

d0244_record_bytes = run_bytes(
    "git",
    "show",
    f"{D0244_COMMIT}:{D0244_RECORD}",
)

assert sha256_bytes(
    d0244_record_bytes
) == D0244_RECORD_SHA

d0244 = json.loads(
    d0244_record_bytes.decode("utf-8"),
    object_pairs_hook=no_dup,
)

assert d0244["decision"] == "D0244"

assert d0244["authorization"]["authorized"] is True
assert d0244["authorization"]["executed"] is False
assert d0244["authorization"]["designated_execution_decision"] == "D0245"

assert d0244["authorization"]["recursion_depth"] == 1
assert len(d0244["authorization"]["roots"]) == 3

d0244_roots = d0244["authorization"]["roots"]

root_canonical = json.dumps(
    d0244_roots,
    ensure_ascii=False,
    sort_keys=True,
    separators=(",", ":"),
).encode("utf-8")

assert sha256_bytes(
    root_canonical
) == D0244_ROOT_SET_SHA

assert d0244["authorization"]["filename_filter"]["tokens"] == EXPECTED_TOKENS

# ------------------------------------------------------------
# C. Verify complete D0244 root records and core Git bindings.
#    Do not enumerate child contents.
# ------------------------------------------------------------

for root in d0244_roots:
    assert set(root.keys()) == {
        "anchor_member",
        "directory",
        "git_tree_object",
        "root_id",
    }

    assert set(
        root["anchor_member"].keys()
    ) == {
        "git_blob",
        "path",
        "sha256",
    }

    actual_tree = run_text(
        "git",
        "rev-parse",
        f"{D0244_COMMIT}:{root['directory']}",
    )

    assert actual_tree == root["git_tree_object"]

    assert run_text(
        "git",
        "cat-file",
        "-t",
        actual_tree,
    ) == "tree"

    actual_anchor_blob = run_text(
        "git",
        "rev-parse",
        f"{D0244_COMMIT}:{root['anchor_member']['path']}",
    )

    assert actual_anchor_blob == root["anchor_member"]["git_blob"]

# ------------------------------------------------------------
# D. Verify D0246 canonical authorization record.
# ------------------------------------------------------------

raw = record_path.read_bytes()

assert not raw.endswith(b"\n")

record = json.loads(
    raw.decode("utf-8"),
    object_pairs_hook=no_dup,
)

canonical = json.dumps(
    record,
    ensure_ascii=False,
    sort_keys=True,
    separators=(",", ":"),
).encode("utf-8")

assert raw == canonical

assert record["decision"] == "D0246"

assert record["status"] == (
    "REPLACEMENT_BOUNDED_CROSSWALK_LOCATOR_DISCOVERY_EXECUTION_AUTHORIZED_NOT_EXECUTED"
)

auth = record["authorization"]

assert auth["authorized"] is True
assert auth["executed"] is False
assert auth["designated_execution_decision"] == "D0247"

assert auth["recursion_depth"] == 1

# Critical corrected rule:
# complete governed D0244 root records must be inherited exactly.
assert auth["roots"] == d0244_roots

auth_root_canonical = json.dumps(
    auth["roots"],
    ensure_ascii=False,
    sort_keys=True,
    separators=(",", ":"),
).encode("utf-8")

assert sha256_bytes(
    auth_root_canonical
) == D0244_ROOT_SET_SHA

root_binding = auth["root_binding"]

assert root_binding["inheritance_mode"] == (
    "EXACT_COMPLETE_D0244_AUTHORIZATION_ROOT_RECORD_INHERITANCE"
)

assert root_binding["inherited_root_record_count"] == 3
assert root_binding["inherited_root_record_set_sha256"] == D0244_ROOT_SET_SHA

assert auth["filename_filter"]["tokens"] == EXPECTED_TOKENS
assert auth["filename_filter"]["match_mode"] == "CASE_INSENSITIVE_SUBSTRING_OR"

assert auth["operation_set"] == EXPECTED_OPERATIONS
assert auth["stop_conditions"] == EXPECTED_STOP

assert auth["filename_filter"]["establishes_authority"] is False
assert auth["filename_filter"]["establishes_crosswalk_semantics"] is False
assert auth["filename_filter"]["establishes_evidence_adequacy"] is False

assert auth["zero_candidate_result_allowed"] is True
assert auth["zero_candidate_result_is_negative_proof"] is False

# ------------------------------------------------------------
# E. Replacement-decision semantics.
# ------------------------------------------------------------

replacement = record["execution_replacement"]

assert replacement["original_d0244_designated_execution_decision"] == "D0245"

assert replacement["original_d0245_execution_designation_state"] == (
    "SUPERSEDED_UNEXECUTED_BY_CORRECTIVE_SUCCESSOR_NUMBER_CONSUMPTION"
)

assert replacement["replacement_execution_decision"] == "D0247"
assert replacement["replacement_execution_authorized"] is True
assert replacement["replacement_execution_performed"] is False

bindings = record["governance_bindings"]

assert bindings["d0244_original_discovery_authorization"]["commit"] == D0244_COMMIT
assert bindings["d0244_original_discovery_authorization"]["tree"] == D0244_TREE
assert bindings["d0244_original_discovery_authorization"]["record_sha256"] == D0244_RECORD_SHA
assert bindings["d0244_original_discovery_authorization"]["root_record_set_sha256"] == D0244_ROOT_SET_SHA

assert bindings["d0245_verified_corrective_checkpoint"]["commit"] == D0245_COMMIT
assert bindings["d0245_verified_corrective_checkpoint"]["tree"] == D0245_TREE
assert bindings["d0245_verified_corrective_checkpoint"]["manifest_sha256"] == D0245_MANIFEST_SHA

# ------------------------------------------------------------
# F. Explicit downstream prohibitions.
# ------------------------------------------------------------

for key, value in record["explicit_nonauthorization"].items():
    assert value is False, key

for key, value in record["results_not_established"].items():
    assert value is False, key

boundary = record["post_execution_boundary"]

assert boundary["candidate_result_authorizes_c2"] is False
assert boundary["candidate_result_establishes_crosswalk_semantics"] is False
assert boundary["candidate_result_establishes_source_authority"] is False
assert boundary["zero_candidate_result_allows_automatic_scope_expansion"] is False

# ------------------------------------------------------------
# G. Human-readable boundary.
# ------------------------------------------------------------

scope = scope_path.read_text(
    encoding="utf-8"
)

markers = [
    "AUTHORIZED — NOT EXECUTED",
    "D0246_ROOT_BINDING_MODE=EXACT_COMPLETE_D0244_AUTHORIZATION_ROOT_RECORD_INHERITANCE",
    "SUPERSEDED_UNEXECUTED_BY_CORRECTIVE_SUCCESSOR_NUMBER_CONSUMPTION",
    "D0247_EXECUTION_AUTHORIZED=YES",
    "D0247_EXECUTION_PERFORMED=NO",
    "LOCATOR_DISCOVERY_EXECUTED=NO",
    "D0247_FILE_CONTENT_READ_AUTHORIZED=NO",
    "D0247_FILE_BYTE_HASH_RECOMPUTATION_AUTHORIZED=NO",
    "D0247_SUBDIRECTORY_RECURSION_AUTHORIZED=NO",
    "D0247_REPOSITORY_WIDE_SEARCH_AUTHORIZED=NO",
    "D0247_GIT_HISTORY_SEARCH_AUTHORIZED=NO",
    "D0247_EXTERNAL_NETWORK_ACCESS_AUTHORIZED=NO",
    "C2_AUTHORIZED=NO",
    "C3_AUTHORIZED=NO",
    "B2_AUTHORIZED=NO",
    "INDEPENDENT_READ_ONLY_VERIFY_D0246_BEFORE_ANY_D0247_LOCATOR_DISCOVERY_EXECUTION",
]

for marker in markers:
    assert marker in scope, marker

print("D0246_REPLACEMENT_EXECUTION_AUTHORIZATION_VERIFIER=PASS")
print("D0245_VERIFIED_CHECKPOINT_BINDING=PASS")
print("D0244_ORIGINAL_DISCOVERY_AUTHORIZATION_BINDING=PASS")

print("D0244_COMPLETE_ROOT_RECORD_SET_SHA256=" + D0244_ROOT_SET_SHA)
print("D0246_COMPLETE_ROOT_RECORDS_EQUAL_D0244=YES")
print("D0246_ROOT_BINDING_MODE=EXACT_COMPLETE_D0244_AUTHORIZATION_ROOT_RECORD_INHERITANCE")

print("D0247_ROOT_COUNT=3")
print("D0247_RECURSION_DEPTH=1")
print("D0247_FILENAME_TOKEN_COUNT=10")

print("D0247_EXECUTION_AUTHORIZED=YES")
print("D0247_EXECUTION_PERFORMED=NO")
print("LOCATOR_DISCOVERY_EXECUTED=NO")

print("FILE_CONTENT_READ_AUTHORIZED=NO")
print("FILE_BYTE_HASH_RECOMPUTATION_AUTHORIZED=NO")
print("REPOSITORY_WIDE_SEARCH_AUTHORIZED=NO")
print("GIT_HISTORY_SEARCH_AUTHORIZED=NO")
print("EXTERNAL_NETWORK_ACCESS_AUTHORIZED=NO")

print("C2_AUTHORIZED=NO")
print("C2_EXECUTED=NO")
print("C3_AUTHORIZED=NO")

print("B2_READINESS_ESTABLISHED=NO")
print("B2_AUTHORIZED=NO")
print("B2_EXECUTED=NO")

print("SAFE_D0246_VERIFIER=PASS")
