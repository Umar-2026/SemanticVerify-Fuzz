#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import os
import subprocess

D0248_COMMIT = "049f04eb47da2c4babcf5ecf4129aaeccae6c2bf"
D0248_TREE = "00bd507e9ad59ef6c68f5829afc785c0eecd91ad"
D0248_RECORD_SHA = "52c6b5d65684af5796c9c1a6d69326493dbc02ec4982d100508f5acebb19933a"
D0248_MANIFEST_SHA = "776acd4eeaa7fed55627d35e1e4cbd7fa113d70328ad61bea19812dc06e6a429"

D0247_COMMIT = "cf045868de6ef3e1c61a20bcb5bd57c4e7ffe5ba"
D0247_TREE = "7d63a3cff33d74c154e8a33f102af8fb4ba16592"
D0247_PRIMARY_SHA = "7dd9dab7e402f93950b932ce0ec0e5fb283ca6d9605b8c8662073f9e05802e9d"
D0247_CANDIDATE_ARRAY_SHA = "55c366812f695d23384da9e687da16d729ebc339292f2025f601e5e534f7cf68"

D0246_COMMIT = "512df3091b4aeb76ad0979f1c559a3e59cab756e"
D0246_TREE = "bab06bee08e85ea33260a32cf2f4328f37430b52"
D0246_RECORD_SHA = "d0c31c01f0beb10a42cee7f40e6a09a9301ba3ca7aef9935810a78591a9c96f3"
D0246_ANCHOR_ARRAY_SHA = "43e1b35b45285069f20f21400dbaa98c6b26d33c5f955bdc61aac186811c1614"

D0248_RECORD = "evidence/annotation_preparation/protocol_specification_schema_successor_v2/d0248_locator_candidate_qualification_and_identity_binding_authorization_v1/01_locator_candidate_qualification_and_identity_binding_authorization.v1.json"
D0248_MANIFEST = "evidence/annotation_preparation/protocol_specification_schema_successor_v2/d0248_locator_candidate_qualification_and_identity_binding_authorization_v1/04_locator_candidate_qualification_and_identity_binding_authorization.v1.SHA256SUMS"

D0247_PRIMARY = "evidence/annotation_preparation/protocol_specification_schema_successor_v2/d0247_bounded_crosswalk_locator_discovery_execution_v1/01_bounded_crosswalk_locator_discovery_execution.v1.json"

D0246_RECORD = "evidence/annotation_preparation/protocol_specification_schema_successor_v2/d0246_replacement_bounded_crosswalk_locator_discovery_execution_authorization_v1/01_replacement_bounded_crosswalk_locator_discovery_execution_authorization.v1.json"

EXPECTED_BOUNDARIES = {
    "candidate_admissibility_adjudication": False,
    "candidate_blob_read": False,
    "candidate_content_open": False,
    "candidate_file_byte_hash": False,
    "candidate_json_parse": False,
    "candidate_manifest_read": False,
    "candidate_markdown_read": False,
    "candidate_python_read": False,
    "concrete_mapping": False,
    "cross_source_join": False,
    "crosswalk_semantic_adjudication": False,
    "external_network_access": False,
    "git_history_search": False,
    "repository_wide_search": False,
    "req06_req14_determination": False,
    "semantic_interpretation": False,
    "source_authority_adjudication": False,
    "source_root_reenumeration": False,
}

EXPECTED_RESULTS = {
    "authoritative_class06_crosswalk_source_instance_bound": False,
    "b2_readiness_established": False,
    "c2_authorization_ready": False,
    "c2_source_instance_allowlist_bound": False,
    "candidate_admissibility_resolved": False,
    "crosswalk_semantics_established": False,
    "evidence_adequacy_established": False,
    "req06_req14_satisfaction_established": False,
    "source_authority_established": False,
}

EXPECTED_NEXT = (
    "SEPARATE_READ_ONLY_DESIGN_FOR_BOUNDED_CANDIDATE_CONTENT_QUALIFICATION_IF_GOVERNANCE_DEEMS_CONTENT_INSPECTION_NECESSARY"
)

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

primary_path = pkg / "01_locator_candidate_metadata_identity_qualification_execution.v1.json"
scope_path = pkg / "02_locator_candidate_metadata_identity_qualification_execution_scope.v1.md"


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
    return hashlib.sha256(
        data
    ).hexdigest()


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
        D0248_COMMIT,
        current_head,
    ],
    cwd=repo,
).returncode

assert rc == 0

assert run_text(
    "git",
    "rev-parse",
    f"{D0248_COMMIT}^{{tree}}",
) == D0248_TREE

d48_raw = run_bytes(
    "git",
    "show",
    f"{D0248_COMMIT}:{D0248_RECORD}",
)

assert sha256_bytes(
    d48_raw
) == D0248_RECORD_SHA

d48_manifest_raw = run_bytes(
    "git",
    "show",
    f"{D0248_COMMIT}:{D0248_MANIFEST}",
)

assert sha256_bytes(
    d48_manifest_raw
) == D0248_MANIFEST_SHA

d47_raw = run_bytes(
    "git",
    "show",
    f"{D0247_COMMIT}:{D0247_PRIMARY}",
)

assert sha256_bytes(
    d47_raw
) == D0247_PRIMARY_SHA

d46_raw = run_bytes(
    "git",
    "show",
    f"{D0246_COMMIT}:{D0246_RECORD}",
)

assert sha256_bytes(
    d46_raw
) == D0246_RECORD_SHA

d48 = json.loads(
    d48_raw.decode("utf-8"),
    object_pairs_hook=no_dup,
)

d47 = json.loads(
    d47_raw.decode("utf-8"),
    object_pairs_hook=no_dup,
)

d46 = json.loads(
    d46_raw.decode("utf-8"),
    object_pairs_hook=no_dup,
)

assert d48["decision"] == "D0248"
assert d48["authorization"]["authorized"] is True
assert d48["authorization"]["executed"] is False
assert d48["authorization"]["designated_execution_decision"] == "D0249"

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
        "root_id": root[
            "root_id"
        ],
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

raw = primary_path.read_bytes()

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

assert record[
    "qualification_id"
] == (
    "D0249-LOCATOR-CANDIDATE-METADATA-IDENTITY-QUALIFICATION-V1"
)

assert record[
    "authorization_binding"
] == {
    "commit": D0248_COMMIT,
    "decision": "D0248",
    "manifest_sha256": D0248_MANIFEST_SHA,
    "record_path": D0248_RECORD,
    "record_sha256": D0248_RECORD_SHA,
    "tree": D0248_TREE,
}

assert record[
    "d0247_candidate_inventory_binding"
] == {
    "candidate_array_sha256": D0247_CANDIDATE_ARRAY_SHA,
    "candidate_count": 10,
    "commit": D0247_COMMIT,
    "primary_output_path": D0247_PRIMARY,
    "primary_output_sha256": D0247_PRIMARY_SHA,
    "tree": D0247_TREE,
}

assert record[
    "d0246_anchor_identity_binding"
] == {
    "anchor_identity_array_sha256": D0246_ANCHOR_ARRAY_SHA,
    "anchor_record_count": 3,
    "commit": D0246_COMMIT,
    "record_path": D0246_RECORD,
    "record_sha256": D0246_RECORD_SHA,
    "tree": D0246_TREE,
}

anchor_by_root = {
    anchor["root_id"]: anchor
    for anchor in anchors
}

expected_qualifications = []

exact_count = 0
no_match_count = 0

for index, candidate in enumerate(
    candidates,
    1,
):
    root_id = candidate[
        "root_id"
    ]

    assert root_id in anchor_by_root

    anchor = anchor_by_root[
        root_id
    ]

    root_match = (
        candidate["root_id"]
        == anchor["root_id"]
    )

    assert root_match is True

    path_match = (
        candidate["full_locator"]
        == anchor["path"]
    )

    git_blob_match = (
        candidate["git_object_id"]
        == anchor["git_blob"]
    )

    exact_relation = (
        root_match
        and path_match
        and git_blob_match
    )

    no_match_relation = (
        root_match
        and not (
            path_match
            and git_blob_match
        )
    )

    assert exact_relation != no_match_relation

    if exact_relation:
        relation = (
            "EXACT_BOUND_ANCHOR_MEMBER_IDENTITY"
        )
        exact_count += 1
    else:
        relation = (
            "NO_BOUND_ANCHOR_IDENTITY_MATCH"
        )
        no_match_count += 1

    expected_qualifications.append(
        {
            "anchor_identity_relation": relation,
            "bound_anchor_git_blob": anchor["git_blob"],
            "bound_anchor_path": anchor["path"],
            "candidate_index": index,
            "full_locator": candidate["full_locator"],
            "git_blob_match": git_blob_match,
            "git_mode": candidate["git_mode"],
            "git_object_id": candidate["git_object_id"],
            "git_object_type": candidate["git_object_type"],
            "matched_filename_tokens": candidate["matched_filename_tokens"],
            "path_match": path_match,
            "root_id": candidate["root_id"],
        }
    )

assert exact_count == 3
assert no_match_count == 7

assert record[
    "candidate_identity_qualifications"
] == expected_qualifications

assert record[
    "qualification_summary"
] == {
    "candidate_count": 10,
    "exact_bound_anchor_member_identity_count": 3,
    "no_bound_anchor_identity_match_count": 7,
}

assert record[
    "execution_boundaries"
] == EXPECTED_BOUNDARIES

assert record[
    "results_not_established"
] == EXPECTED_RESULTS

assert record[
    "next_required_checkpoint"
] == EXPECTED_NEXT

scope = scope_path.read_text(
    encoding="utf-8"
)

markers = [
    "EXECUTED — METADATA ONLY",
    "D0249_CANDIDATE_COUNT=10",
    "D0249_EXACT_BOUND_ANCHOR_MEMBER_IDENTITY_COUNT=3",
    "D0249_NO_BOUND_ANCHOR_IDENTITY_MATCH_COUNT=7",
    "D0249_CANDIDATE_CONTENT_OPEN=NO",
    "D0249_CANDIDATE_BLOB_READ=NO",
    "D0249_CANDIDATE_FILE_BYTE_HASH=NO",
    "D0249_SOURCE_ROOT_REENUMERATION=NO",
    "D0249_REPOSITORY_WIDE_SEARCH=NO",
    "D0249_GIT_HISTORY_SEARCH=NO",
    "D0249_EXTERNAL_NETWORK_ACCESS=NO",
    "D0249_SEMANTIC_INTERPRETATION=NO",
    "C2_AUTHORIZED=NO",
    "C3_AUTHORIZED=NO",
    "B2_AUTHORIZED=NO",
    EXPECTED_NEXT,
]

for marker in markers:
    assert marker in scope, marker

print("D0249_SAFE_METADATA_ONLY_VERIFIER=PASS")
print("D0248_AUTHORIZATION_BINDING=PASS")
print("D0247_CANDIDATE_ARRAY_BINDING=PASS")
print("D0246_ANCHOR_IDENTITY_ARRAY_BINDING=PASS")
print("D0249_PRIMARY_JSON_CANONICALIZATION=PASS")
print("D0249_RELATION_RECOMPUTATION=PASS")
print("D0249_OUTPUT_ARRAY_RECOMPUTATION=PASS")
print("D0249_CANDIDATE_COUNT=10")
print("D0249_EXACT_BOUND_ANCHOR_MEMBER_IDENTITY_COUNT=3")
print("D0249_NO_BOUND_ANCHOR_IDENTITY_MATCH_COUNT=7")
print("D0249_CANDIDATE_CONTENT_OPEN=NO")
print("D0249_CANDIDATE_FILE_BYTE_HASH=NO")
print("D0249_SOURCE_ROOT_REENUMERATION=NO")
print("C2_AUTHORIZED=NO")
print("C2_EXECUTED=NO")
print("C3_AUTHORIZED=NO")
print("B2_READINESS_ESTABLISHED=NO")
print("B2_AUTHORIZED=NO")
print("B2_EXECUTED=NO")
print("D0249_SAFE_VERIFIER=PASS")
