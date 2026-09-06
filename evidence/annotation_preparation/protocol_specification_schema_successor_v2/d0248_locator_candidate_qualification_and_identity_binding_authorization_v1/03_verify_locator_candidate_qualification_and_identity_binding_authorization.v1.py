#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import os
import subprocess

D0247_COMMIT = "cf045868de6ef3e1c61a20bcb5bd57c4e7ffe5ba"
D0247_TREE = "7d63a3cff33d74c154e8a33f102af8fb4ba16592"
D0247_PRIMARY_SHA = "7dd9dab7e402f93950b932ce0ec0e5fb283ca6d9605b8c8662073f9e05802e9d"
D0247_MANIFEST_SHA = "c2ab501cd4e32ea723a8d8b51960607ce01f7d15176d6e1dff1927e62810247a"
D0247_CANDIDATE_ARRAY_SHA = "55c366812f695d23384da9e687da16d729ebc339292f2025f601e5e534f7cf68"

D0246_COMMIT = "512df3091b4aeb76ad0979f1c559a3e59cab756e"
D0246_TREE = "bab06bee08e85ea33260a32cf2f4328f37430b52"
D0246_RECORD_SHA = "d0c31c01f0beb10a42cee7f40e6a09a9301ba3ca7aef9935810a78591a9c96f3"
D0246_ANCHOR_ARRAY_SHA = "43e1b35b45285069f20f21400dbaa98c6b26d33c5f955bdc61aac186811c1614"

D0247_PRIMARY = "evidence/annotation_preparation/protocol_specification_schema_successor_v2/d0247_bounded_crosswalk_locator_discovery_execution_v1/01_bounded_crosswalk_locator_discovery_execution.v1.json"
D0247_MANIFEST = "evidence/annotation_preparation/protocol_specification_schema_successor_v2/d0247_bounded_crosswalk_locator_discovery_execution_v1/04_bounded_crosswalk_locator_discovery_execution.v1.SHA256SUMS"

D0246_RECORD = "evidence/annotation_preparation/protocol_specification_schema_successor_v2/d0246_replacement_bounded_crosswalk_locator_discovery_execution_authorization_v1/01_replacement_bounded_crosswalk_locator_discovery_execution_authorization.v1.json"

EXPECTED_OPERATIONS = [
    "LOAD_EXACT_COMMITTED_D0247_CANDIDATE_ARRAY",
    "LOAD_EXACT_D0246_BOUND_ROOT_ANCHOR_METADATA",
    "COMPARE_ONLY_ROOT_ID_FULL_LOCATOR_AND_GIT_OBJECT_ID_AGAINST_BOUND_ANCHOR_METADATA",
    "ASSIGN_EXACTLY_ONE_OF_TWO_IDENTITY_RELATION_VALUES_TO_EACH_OF_TEN_CANDIDATES",
    "MATERIALIZE_METADATA_ONLY_CANDIDATE_IDENTITY_QUALIFICATION_RECORD",
]

EXPECTED_RELATIONS = [
    "EXACT_BOUND_ANCHOR_MEMBER_IDENTITY",
    "NO_BOUND_ANCHOR_IDENTITY_MATCH",
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

record_path = pkg / "01_locator_candidate_qualification_and_identity_binding_authorization.v1.json"
scope_path = pkg / "02_locator_candidate_qualification_and_identity_binding_authorization_scope.v1.md"


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


def no_dup(pairs):
    out = {}

    for k, v in pairs:
        if k in out:
            raise AssertionError(
                "duplicate JSON key: " + k
            )

        out[k] = v

    return out


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


current_head = run_text(
    "git",
    "rev-parse",
    "HEAD",
)

rc = subprocess.run(
    [
        "git",
        "merge-base",
        "--is-ancestor",
        D0247_COMMIT,
        current_head,
    ],
    cwd=repo,
).returncode

assert rc == 0

assert run_text(
    "git",
    "rev-parse",
    f"{D0247_COMMIT}^{{tree}}",
) == D0247_TREE

assert run_text(
    "git",
    "rev-parse",
    f"{D0247_COMMIT}^",
) == D0246_COMMIT

d47_raw = run_bytes(
    "git",
    "show",
    f"{D0247_COMMIT}:{D0247_PRIMARY}",
)

assert sha256_bytes(
    d47_raw
) == D0247_PRIMARY_SHA

manifest_raw = run_bytes(
    "git",
    "show",
    f"{D0247_COMMIT}:{D0247_MANIFEST}",
)

assert sha256_bytes(
    manifest_raw
) == D0247_MANIFEST_SHA

d46_raw = run_bytes(
    "git",
    "show",
    f"{D0246_COMMIT}:{D0246_RECORD}",
)

assert sha256_bytes(
    d46_raw
) == D0246_RECORD_SHA

d47 = json.loads(
    d47_raw.decode("utf-8"),
    object_pairs_hook=no_dup,
)

d46 = json.loads(
    d46_raw.decode("utf-8"),
    object_pairs_hook=no_dup,
)

candidates = d47[
    "lexical_candidate_locators"
]

anchors = [
    {
        "git_blob": root[
            "anchor_member"
        ]["git_blob"],
        "path": root[
            "anchor_member"
        ]["path"],
        "root_id": root["root_id"],
        "sha256": root[
            "anchor_member"
        ]["sha256"],
    }
    for root in d46[
        "authorization"
    ]["roots"]
]

assert len(candidates) == 10
assert len(anchors) == 3

candidate_raw = json.dumps(
    candidates,
    ensure_ascii=False,
    sort_keys=True,
    separators=(",", ":"),
).encode("utf-8")

anchor_raw = json.dumps(
    anchors,
    ensure_ascii=False,
    sort_keys=True,
    separators=(",", ":"),
).encode("utf-8")

assert sha256_bytes(
    candidate_raw
) == D0247_CANDIDATE_ARRAY_SHA

assert sha256_bytes(
    anchor_raw
) == D0246_ANCHOR_ARRAY_SHA

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

assert record["decision"] == "D0248"

assert record["status"] == (
    "METADATA_ONLY_LOCATOR_CANDIDATE_QUALIFICATION_AND_IDENTITY_BINDING_AUTHORIZED_NOT_EXECUTED"
)

auth = record["authorization"]

assert auth["authorized"] is True
assert auth["executed"] is False
assert auth["designated_execution_decision"] == "D0249"
assert auth["operation_set"] == EXPECTED_OPERATIONS
assert auth["qualification_relations"] == EXPECTED_RELATIONS

d47_binding = record[
    "input_bindings"
]["d0247_candidate_inventory"]

assert d47_binding["commit"] == D0247_COMMIT
assert d47_binding["tree"] == D0247_TREE
assert d47_binding["primary_output_sha256"] == D0247_PRIMARY_SHA
assert d47_binding["manifest_sha256"] == D0247_MANIFEST_SHA
assert d47_binding["candidate_array_sha256"] == D0247_CANDIDATE_ARRAY_SHA
assert d47_binding["candidate_count"] == 10

d46_binding = record[
    "input_bindings"
]["d0246_anchor_identity_metadata"]

assert d46_binding["commit"] == D0246_COMMIT
assert d46_binding["tree"] == D0246_TREE
assert d46_binding["record_sha256"] == D0246_RECORD_SHA
assert d46_binding["anchor_identity_array_sha256"] == D0246_ANCHOR_ARRAY_SHA
assert d46_binding["anchor_record_count"] == 3

anchor_by_root = {
    a["root_id"]: a
    for a in anchors
}

exact = 0
no_match = 0

for candidate in candidates:
    anchor = anchor_by_root[
        candidate["root_id"]
    ]

    path_match = (
        candidate["full_locator"]
        == anchor["path"]
    )

    blob_match = (
        candidate["git_object_id"]
        == anchor["git_blob"]
    )

    if path_match and blob_match:
        exact += 1
    else:
        no_match += 1

expected = record[
    "expected_metadata_only_result"
]

assert expected["candidate_count"] == 10
assert expected["exact_bound_anchor_member_identity_count"] == 3
assert expected["no_bound_anchor_identity_match_count"] == 7

assert exact == 3
assert no_match == 7

sem = record[
    "qualification_semantics"
]

exact_sem = sem[
    "exact_bound_anchor_member_identity"
]

assert exact_sem[
    "requires_all_conditions"
] is True

assert exact_sem[
    "establishes_already_governed_anchor_identity_only"
] is True

assert exact_sem[
    "establishes_class06_crosswalk_source"
] is False

assert exact_sem[
    "establishes_source_authority_for_c2"
] is False

assert exact_sem[
    "establishes_crosswalk_semantics"
] is False

assert exact_sem[
    "establishes_c2_readiness"
] is False

no_sem = sem[
    "no_bound_anchor_identity_match"
]

assert no_sem[
    "means_not_authoritative"
] is False

assert no_sem[
    "means_not_crosswalk"
] is False

assert no_sem[
    "means_not_relevant"
] is False

assert no_sem[
    "is_negative_semantic_proof"
] is False

for key, value in record[
    "explicit_nonauthorization"
].items():
    assert value is False, key

for key, value in record[
    "results_not_established"
].items():
    assert value is False, key

scope = scope_path.read_text(
    encoding="utf-8"
)

markers = [
    "AUTHORIZED — NOT EXECUTED",
    "D0249_QUALIFICATION_EXECUTION_AUTHORIZED=YES",
    "D0249_QUALIFICATION_EXECUTED=NO",
    "D0249_EXPECTED_CANDIDATE_COUNT=10",
    "D0249_EXPECTED_EXACT_BOUND_ANCHOR_MEMBER_IDENTITY_COUNT=3",
    "D0249_EXPECTED_NO_BOUND_ANCHOR_IDENTITY_MATCH_COUNT=7",
    "D0249_CANDIDATE_CONTENT_OPEN_AUTHORIZED=NO",
    "D0249_CANDIDATE_BLOB_READ_AUTHORIZED=NO",
    "D0249_CANDIDATE_FILE_BYTE_HASH_AUTHORIZED=NO",
    "D0249_SOURCE_ROOT_REENUMERATION_AUTHORIZED=NO",
    "D0249_REPOSITORY_WIDE_SEARCH_AUTHORIZED=NO",
    "D0249_GIT_HISTORY_SEARCH_AUTHORIZED=NO",
    "D0249_EXTERNAL_NETWORK_ACCESS_AUTHORIZED=NO",
    "C2_AUTHORIZED=NO",
    "C3_AUTHORIZED=NO",
    "B2_AUTHORIZED=NO",
    "INDEPENDENT_READ_ONLY_VERIFY_D0248_BEFORE_ANY_D0249_METADATA_QUALIFICATION_EXECUTION",
]

for marker in markers:
    assert marker in scope, marker

print("D0248_METADATA_ONLY_QUALIFICATION_AUTHORIZATION_VERIFIER=PASS")
print("D0247_VERIFIED_FROZEN_INPUT_BINDING=PASS")
print("D0247_CANDIDATE_ARRAY_SHA256=" + D0247_CANDIDATE_ARRAY_SHA)
print("D0246_ANCHOR_IDENTITY_ARRAY_SHA256=" + D0246_ANCHOR_ARRAY_SHA)
print("D0249_EXPECTED_CANDIDATE_COUNT=10")
print("D0249_EXPECTED_EXACT_BOUND_ANCHOR_MEMBER_IDENTITY_COUNT=3")
print("D0249_EXPECTED_NO_BOUND_ANCHOR_IDENTITY_MATCH_COUNT=7")
print("D0249_QUALIFICATION_EXECUTION_AUTHORIZED=YES")
print("D0249_QUALIFICATION_EXECUTED=NO")
print("CANDIDATE_CONTENT_OPEN_AUTHORIZED=NO")
print("CANDIDATE_BLOB_READ_AUTHORIZED=NO")
print("CANDIDATE_FILE_BYTE_HASH_AUTHORIZED=NO")
print("SOURCE_ROOT_REENUMERATION_AUTHORIZED=NO")
print("C2_AUTHORIZED=NO")
print("C2_EXECUTED=NO")
print("C3_AUTHORIZED=NO")
print("B2_READINESS_ESTABLISHED=NO")
print("B2_AUTHORIZED=NO")
print("B2_EXECUTED=NO")
print("SAFE_D0248_VERIFIER=PASS")
