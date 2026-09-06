#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import os
import subprocess

D0249_COMMIT = "379ae0663fd9c6dbadd24eb677f16cf3ca12f4be"
D0249_TREE = "1248c121e6d4d53ff7f843ee956e82c007633650"
D0249_PRIMARY_SHA = "1138e6a60d410a138757f7e64335b2f4642134c74cf034db99e0f317a756d9a8"
D0249_MANIFEST_SHA = "bdc59156fc8e9d1e097a36a536e7c0ef4be4506d505525abfa95685e2b01fc60"

D0241_COMMIT = "bfc389580da261786556aa91d127ff5ac053ea2d"
D0241_TREE = "bc13dcabe70167d7f81bba4b9142a7ede0e71b4d"
D0241_RECORD_SHA = "6fd0b9de10cb0acd7c6ab81bdc25874d7cdf7b36aff5b1e24ce3c3e5b1e6202e"

CONTENT_UNIVERSE_SHA = "2d57d40ae4106b4b8179278172d462822078626166bef9272b0e91cbe1c00054"

D0249_PRIMARY = (
    "evidence/annotation_preparation/protocol_specification_schema_successor_v2/"
    "d0249_locator_candidate_metadata_identity_qualification_execution_v1/"
    "01_locator_candidate_metadata_identity_qualification_execution.v1.json"
)

D0249_MANIFEST = (
    "evidence/annotation_preparation/protocol_specification_schema_successor_v2/"
    "d0249_locator_candidate_metadata_identity_qualification_execution_v1/"
    "04_locator_candidate_metadata_identity_qualification_execution.v1.SHA256SUMS"
)

D0241_RECORD = (
    "evidence/annotation_preparation/protocol_specification_schema_successor_v2/"
    "d0241_carrier_admissibility_evidence_closure_design_v1/"
    "01_carrier_admissibility_evidence_closure_design.v1.json"
)

D0251_PKG = (
    "evidence/annotation_preparation/protocol_specification_schema_successor_v2/"
    "d0251_c2_bounded_candidate_content_acquisition_execution_v1"
)

D0251_DECISION = (
    "documentation/decisions/"
    "0251-execute-c2-bounded-candidate-content-acquisition.md"
)

EXPECTED_NEXT = (
    "INDEPENDENT_READ_ONLY_VERIFY_D0250_BEFORE_ANY_D0251_SOURCE_BLOB_READ"
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

record_path = (
    pkg
    / "01_c2_bounded_candidate_content_acquisition_authorization.v1.json"
)

scope_path = (
    pkg
    / "02_c2_bounded_candidate_content_acquisition_authorization_scope.v1.md"
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
        D0249_COMMIT,
        current_head,
    ],
    cwd=repo,
).returncode

assert rc == 0

assert run_text(
    "git",
    "rev-parse",
    f"{D0249_COMMIT}^{{tree}}",
) == D0249_TREE

assert run_text(
    "git",
    "rev-parse",
    f"{D0241_COMMIT}^{{tree}}",
) == D0241_TREE

rc = subprocess.run(
    [
        "git",
        "merge-base",
        "--is-ancestor",
        D0241_COMMIT,
        D0249_COMMIT,
    ],
    cwd=repo,
).returncode

assert rc == 0

d49_raw = run_bytes(
    "git",
    "show",
    f"{D0249_COMMIT}:{D0249_PRIMARY}",
)

assert sha256_bytes(d49_raw) == D0249_PRIMARY_SHA

d49_manifest_raw = run_bytes(
    "git",
    "show",
    f"{D0249_COMMIT}:{D0249_MANIFEST}",
)

assert sha256_bytes(
    d49_manifest_raw
) == D0249_MANIFEST_SHA

d241_raw = run_bytes(
    "git",
    "show",
    f"{D0241_COMMIT}:{D0241_RECORD}",
)

assert sha256_bytes(
    d241_raw
) == D0241_RECORD_SHA

d49 = json.loads(
    d49_raw.decode("utf-8"),
    object_pairs_hook=no_dup,
)

rows = d49[
    "candidate_identity_qualifications"
]

assert len(rows) == 10

candidate_universe = []

for expected_index, row in enumerate(
    rows,
    1,
):
    assert row["candidate_index"] == expected_index
    assert row["git_object_type"] == "blob"
    assert row["git_mode"] == "100644"

    candidate_universe.append(
        {
            "candidate_index": row["candidate_index"],
            "full_locator": row["full_locator"],
            "git_mode": row["git_mode"],
            "git_object_id": row["git_object_id"],
            "git_object_type": row["git_object_type"],
            "root_id": row["root_id"],
        }
    )

candidate_raw = json.dumps(
    candidate_universe,
    ensure_ascii=False,
    sort_keys=True,
    separators=(",", ":"),
).encode("utf-8")

assert sha256_bytes(
    candidate_raw
) == CONTENT_UNIVERSE_SHA

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

assert record["decision"] == "D0250"

assert record["status"] == (
    "C2_BOUNDED_CANDIDATE_CONTENT_ACQUISITION_AUTHORIZED_NOT_EXECUTED"
)

auth = record["authorization"]

assert auth == {
    "authorized": True,
    "c2_authorized": True,
    "designated_execution_decision": "D0251",
    "executed": False,
}

assert record["d0249_binding"] == {
    "commit": D0249_COMMIT,
    "manifest_sha256": D0249_MANIFEST_SHA,
    "primary_output_path": D0249_PRIMARY,
    "primary_output_sha256": D0249_PRIMARY_SHA,
    "tree": D0249_TREE,
}

assert record["c2_governance_binding"] == {
    "commit": D0241_COMMIT,
    "record_path": D0241_RECORD,
    "record_sha256": D0241_RECORD_SHA,
    "role": "BOUNDED_ADDITIONAL_EVIDENCE_ACQUISITION",
    "tree": D0241_TREE,
}

assert record[
    "candidate_content_universe"
] == candidate_universe

assert record[
    "candidate_content_universe_binding"
] == {
    "candidate_count": 10,
    "sha256": CONTENT_UNIVERSE_SHA,
    "source": "D0249_CANDIDATE_IDENTITY_QUALIFICATION_METADATA_ONLY",
}

contract = record[
    "d0251_execution_contract"
]

assert contract[
    "allowed_operations"
] == [
    "LOAD_EXACT_D0249_BOUND_CANDIDATE_BLOB_METADATA",
    "READ_EACH_OF_TEN_EXACT_BOUND_GIT_BLOB_OBJECTS_EXACTLY_ONCE",
    "MATERIALIZE_TEN_BYTE_FOR_BYTE_EXACT_DETACHED_SNAPSHOTS",
    "COMPUTE_SHA256_AND_BYTE_COUNT_FOR_EACH_ACQUIRED_SNAPSHOT",
    "MATERIALIZE_C2_ACQUISITION_RECORD_WITHOUT_SEMANTIC_INTERPRETATION",
]

assert contract["exact_source_blob_read_count"] == 10
assert contract["each_source_blob_read_exactly_once"] is True
assert contract["exact_snapshot_count"] == 10

assert contract["snapshot_paths"] == [
    f"candidate_content_snapshots/{i:03d}.EXACT_BLOB_COPY"
    for i in range(1, 11)
]

assert contract[
    "snapshot_git_blob_oid_must_equal_source_git_object_id"
] is True

assert contract[
    "snapshot_sha256_must_be_computed"
] is True

assert contract[
    "snapshot_byte_count_must_be_recorded"
] is True

for key, value in record[
    "explicit_nonauthorization"
].items():
    assert value is False, key

for key, value in record[
    "results_not_established"
].items():
    assert value is False, key

assert record[
    "next_required_checkpoint"
] == EXPECTED_NEXT

scope = scope_path.read_text(
    encoding="utf-8"
)

markers = [
    "AUTHORIZED — NOT EXECUTED",
    "C2_AUTHORIZED=YES",
    "C2_EXECUTED=NO",
    "D0251_SOURCE_BLOB_READ_EXECUTED=NO",
    "D0251_C2_ACQUISITION_EXECUTED=NO",
    "C3_AUTHORIZED=NO",
    "B2_AUTHORIZED=NO",
    EXPECTED_NEXT,
]

for marker in markers:
    assert marker in scope, marker

for path in (
    D0251_PKG,
    D0251_DECISION,
):
    rc = subprocess.run(
        [
            "git",
            "rev-parse",
            "--verify",
            "--quiet",
            f"HEAD:{path}",
        ],
        cwd=repo,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode

    assert rc != 0

print("D0250_C2_ACQUISITION_AUTHORIZATION_VERIFIER=PASS")
print("D0249_VERIFIED_FROZEN_INPUT_BINDING=PASS")
print("D0241_C2_GOVERNANCE_BINDING=PASS")
print(
    "D0251_EXACT_CANDIDATE_CONTENT_UNIVERSE_SHA256="
    + CONTENT_UNIVERSE_SHA
)
print("D0251_EXACT_CANDIDATE_CONTENT_COUNT=10")
print("D0251_C2_ACQUISITION_AUTHORIZED=YES")
print("D0251_C2_ACQUISITION_EXECUTED=NO")
print("D0251_SOURCE_BLOB_READ_EXECUTED=NO")
print("C2_AUTHORIZED=YES")
print("C2_EXECUTED=NO")
print("C3_AUTHORIZED=NO")
print("C3_EXECUTED=NO")
print("B2_READINESS_ESTABLISHED=NO")
print("B2_AUTHORIZED=NO")
print("B2_EXECUTED=NO")
print("SAFE_D0250_VERIFIER=PASS")
