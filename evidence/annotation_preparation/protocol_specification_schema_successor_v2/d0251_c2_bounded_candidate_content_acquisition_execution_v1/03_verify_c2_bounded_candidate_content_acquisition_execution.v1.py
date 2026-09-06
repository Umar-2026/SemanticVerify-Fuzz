#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import os
import subprocess

D0250_COMMIT = "e6c319ce22a4de68bece34db60829a75597c06e7"
D0250_TREE = "4b67d4fdd0475be8ab3d89f4ccfe54b1e76f0317"
D0250_RECORD_SHA = "27ae3c94601841184bd7149e82d674550c7c2fd7610462d244b049d4663e6d8d"
D0250_MANIFEST_SHA = "265cdec3a551e8214217caf790e2dd8c03037f20096e7da2b2c6dc84576ca803"

D0249_COMMIT = "379ae0663fd9c6dbadd24eb677f16cf3ca12f4be"
D0249_TREE = "1248c121e6d4d53ff7f843ee956e82c007633650"
D0249_PRIMARY_SHA = "1138e6a60d410a138757f7e64335b2f4642134c74cf034db99e0f317a756d9a8"
D0249_MANIFEST_SHA = "bdc59156fc8e9d1e097a36a536e7c0ef4be4506d505525abfa95685e2b01fc60"

CONTENT_UNIVERSE_SHA = "2d57d40ae4106b4b8179278172d462822078626166bef9272b0e91cbe1c00054"
MAPPING_SHA = "2246236e8651b382afdfe34a2ca0ee3ca8081709527634d3b919c7bb02fbe189"

D0250_RECORD = (
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2/"
    "d0250_c2_bounded_candidate_content_acquisition_authorization_v1/"
    "01_c2_bounded_candidate_content_acquisition_authorization.v1.json"
)

D0250_MANIFEST = (
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2/"
    "d0250_c2_bounded_candidate_content_acquisition_authorization_v1/"
    "04_c2_bounded_candidate_content_acquisition_authorization.v1.SHA256SUMS"
)

PKG_REL = (
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2/"
    "d0251_c2_bounded_candidate_content_acquisition_execution_v1"
)

EXPECTED_NEXT = (
    "SEPARATE_READ_ONLY_DESIGN_C3_CANDIDATE_CONTENT_ADJUDICATION_FROM_FROZEN_EXACT_SNAPSHOTS"
)

EXPECTED_BOUNDARIES = {
    "candidate_admissibility_adjudication": False,
    "candidate_content_semantic_interpretation": False,
    "candidate_exact_snapshot_materialization": True,
    "candidate_json_parse": False,
    "candidate_manifest_interpretation": False,
    "candidate_markdown_interpretation": False,
    "candidate_python_interpretation": False,
    "candidate_snapshot_sha256": True,
    "candidate_source_blob_read": True,
    "concrete_mapping": False,
    "cross_source_join": False,
    "crosswalk_semantic_adjudication": False,
    "external_network_access": False,
    "git_history_search": False,
    "repository_wide_search": False,
    "req06_req14_determination": False,
    "source_authority_adjudication": False,
    "source_root_reenumeration": False,
}

EXPECTED_RESULTS = {
    "authoritative_class06_crosswalk_source_instance_bound": False,
    "b2_readiness_established": False,
    "c2_source_instance_allowlist_bound": False,
    "candidate_admissibility_resolved": False,
    "crosswalk_semantics_established": False,
    "evidence_adequacy_established": False,
    "req06_req14_satisfaction_established": False,
    "source_authority_established": False,
    "zero_unresolved_closure_established": False,
}

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

    for key, value in pairs:
        if key in out:
            raise AssertionError(
                "duplicate JSON key: " + key
            )

        out[key] = value

    return out


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
        D0250_COMMIT,
        current_head,
    ],
    cwd=repo,
).returncode

assert rc == 0

assert run_text(
    "git",
    "rev-parse",
    f"{D0250_COMMIT}^{{tree}}",
) == D0250_TREE

d250_raw = run_bytes(
    "git",
    "show",
    f"{D0250_COMMIT}:{D0250_RECORD}",
)

assert sha256_bytes(
    d250_raw
) == D0250_RECORD_SHA

d250_manifest_raw = run_bytes(
    "git",
    "show",
    f"{D0250_COMMIT}:{D0250_MANIFEST}",
)

assert sha256_bytes(
    d250_manifest_raw
) == D0250_MANIFEST_SHA

d250 = json.loads(
    d250_raw.decode("utf-8"),
    object_pairs_hook=no_dup,
)

assert d250["decision"] == "D0250"
assert d250["authorization"]["authorized"] is True
assert d250["authorization"]["c2_authorized"] is True
assert d250["authorization"]["executed"] is False
assert d250["authorization"]["designated_execution_decision"] == "D0251"

universe = d250[
    "candidate_content_universe"
]

snapshot_paths = d250[
    "d0251_execution_contract"
]["snapshot_paths"]

assert len(universe) == 10
assert len(snapshot_paths) == 10
assert len({x["git_object_id"] for x in universe}) == 10

universe_raw = json.dumps(
    universe,
    ensure_ascii=False,
    sort_keys=True,
    separators=(",", ":"),
).encode("utf-8")

assert sha256_bytes(
    universe_raw
) == CONTENT_UNIVERSE_SHA

mapping = []

for row, snapshot_path in zip(
    universe,
    snapshot_paths,
):
    mapping.append(
        {
            "candidate_index": row["candidate_index"],
            "root_id": row["root_id"],
            "source_locator": row["full_locator"],
            "source_git_mode": row["git_mode"],
            "source_git_object_id": row["git_object_id"],
            "source_git_object_type": row["git_object_type"],
            "snapshot_path": snapshot_path,
        }
    )

mapping_raw = json.dumps(
    mapping,
    ensure_ascii=False,
    sort_keys=True,
    separators=(",", ":"),
).encode("utf-8")

assert sha256_bytes(
    mapping_raw
) == MAPPING_SHA

primary_path = (
    pkg
    / "01_c2_bounded_candidate_content_acquisition_execution.v1.json"
)

scope_path = (
    pkg
    / "02_c2_bounded_candidate_content_acquisition_execution_scope.v1.md"
)

manifest_path = (
    pkg
    / "04_c2_bounded_candidate_content_acquisition_execution.v1.SHA256SUMS"
)

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
    "acquisition_id"
] == (
    "D0251-C2-BOUNDED-CANDIDATE-CONTENT-ACQUISITION-V1"
)

assert record[
    "authorization_binding"
] == {
    "commit": D0250_COMMIT,
    "decision": "D0250",
    "manifest_sha256": D0250_MANIFEST_SHA,
    "record_path": D0250_RECORD,
    "record_sha256": D0250_RECORD_SHA,
    "tree": D0250_TREE,
}

assert record[
    "d0249_candidate_content_universe_binding"
] == {
    "candidate_content_universe_sha256": CONTENT_UNIVERSE_SHA,
    "candidate_count": 10,
    "commit": D0249_COMMIT,
    "manifest_sha256": D0249_MANIFEST_SHA,
    "primary_output_sha256": D0249_PRIMARY_SHA,
    "source_oid_to_snapshot_mapping_sha256": MAPPING_SHA,
    "tree": D0249_TREE,
}

expected_snapshot_records = []

for row, snapshot_rel in zip(
    universe,
    snapshot_paths,
):
    snapshot = pkg / snapshot_rel

    assert snapshot.is_file()

    data = snapshot.read_bytes()

    byte_count = len(data)
    sha256 = hashlib.sha256(data).hexdigest()

    git_oid = hashlib.sha1(
        b"blob "
        + str(byte_count).encode("ascii")
        + b"\0"
        + data
    ).hexdigest()

    assert git_oid == row["git_object_id"]

    expected_snapshot_records.append(
        {
            "candidate_index": row["candidate_index"],
            "root_id": row["root_id"],
            "snapshot_byte_count": byte_count,
            "snapshot_git_blob_oid": git_oid,
            "snapshot_path": snapshot_rel,
            "snapshot_sha256": sha256,
            "source_git_mode": row["git_mode"],
            "source_git_object_id": row["git_object_id"],
            "source_git_object_type": row["git_object_type"],
            "source_locator": row["full_locator"],
        }
    )

assert record[
    "candidate_content_snapshots"
] == expected_snapshot_records

assert record[
    "acquisition_summary"
] == {
    "exact_snapshot_blob_identity_match_count": 10,
    "snapshot_count": 10,
    "source_blob_read_count": 10,
    "source_candidate_count": 10,
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

manifest_lines = [
    line
    for line in manifest_path.read_text(
        encoding="utf-8"
    ).splitlines()
    if line.strip()
]

assert len(manifest_lines) == 13

expected_manifest_names = [
    "01_c2_bounded_candidate_content_acquisition_execution.v1.json",
    "02_c2_bounded_candidate_content_acquisition_execution_scope.v1.md",
    "03_verify_c2_bounded_candidate_content_acquisition_execution.v1.py",
] + snapshot_paths

actual_manifest_names = []

for line in manifest_lines:
    digest, rel = line.split(None, 1)

    rel = rel.lstrip("*")

    assert len(digest) == 64
    int(digest, 16)

    file_path = pkg / rel

    assert file_path.is_file()

    actual = hashlib.sha256(
        file_path.read_bytes()
    ).hexdigest()

    assert actual == digest

    actual_manifest_names.append(rel)

assert actual_manifest_names == expected_manifest_names

scope = scope_path.read_text(
    encoding="utf-8"
)

for marker in (
    "EXECUTED — C2 ACQUISITION ONLY",
    "SOURCE_CANDIDATE_COUNT=10",
    "SOURCE_BLOB_READ_COUNT=10",
    "SNAPSHOT_COUNT=10",
    "EXACT_SNAPSHOT_BLOB_IDENTITY_MATCH_COUNT=10",
    "C2_AUTHORIZED=YES",
    "C2_EXECUTED=YES",
    "C3_AUTHORIZED=NO",
    "B2_AUTHORIZED=NO",
    EXPECTED_NEXT,
):
    assert marker in scope, marker

# Postcommit/index identity check when package is committed.
probe = subprocess.run(
    [
        "git",
        "rev-parse",
        "--verify",
        "--quiet",
        f"HEAD:{PKG_REL}/01_c2_bounded_candidate_content_acquisition_execution.v1.json",
    ],
    cwd=repo,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
).returncode

if probe == 0:
    for row, snapshot_rel in zip(
        universe,
        snapshot_paths,
    ):
        committed_oid = run_text(
            "git",
            "rev-parse",
            f"HEAD:{PKG_REL}/{snapshot_rel}",
        )

        assert committed_oid == row[
            "git_object_id"
        ]

print("D0251_SAFE_NON_SOURCE_REOPENING_VERIFIER=PASS")
print("D0250_AUTHORIZATION_BINDING=PASS")
print("D0251_CONTENT_UNIVERSE_BINDING=PASS")
print("D0251_EXECUTION_MAPPING_BINDING=PASS")
print("D0251_PRIMARY_JSON_CANONICALIZATION=PASS")
print("D0251_SNAPSHOT_SHA256_RECOMPUTATION=PASS")
print("D0251_SNAPSHOT_BYTE_COUNT_RECOMPUTATION=PASS")
print("D0251_SNAPSHOT_RAW_GIT_BLOB_SHA1_RECOMPUTATION=PASS")
print("D0251_EXACT_SNAPSHOT_BLOB_IDENTITY_MATCH_COUNT=10")
print("D0251_MANIFEST_ENTRY_COUNT=13")
print("D0251_SOURCE_BLOB_REOPENED_BY_VERIFIER=NO")
print("C2_AUTHORIZED=YES")
print("C2_EXECUTED=YES")
print("C3_AUTHORIZED=NO")
print("C3_EXECUTED=NO")
print("B2_READINESS_ESTABLISHED=NO")
print("B2_AUTHORIZED=NO")
print("B2_EXECUTED=NO")
print("D0251_SAFE_VERIFIER=PASS")
