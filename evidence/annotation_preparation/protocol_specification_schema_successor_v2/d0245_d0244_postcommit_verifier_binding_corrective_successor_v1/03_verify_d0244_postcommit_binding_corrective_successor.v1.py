#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import os
import re
import subprocess

D0244_COMMIT = "5f30a418e73f53b9f4cbc9fbf0260249f4f9dc4a"
D0244_TREE = "1739b38b6d43019e04f9324911f63c98c74443fa"
D0243_COMMIT = "ee7fca936998e437e264dbd86cb1b153b3ed626d"

D0244_SUBJECT = "decision: authorize bounded crosswalk locator discovery without execution"

D0244_ARTIFACTS = [
    {
        "role": "PRIMARY_AUTHORIZATION_RECORD",
        "path": "evidence/annotation_preparation/protocol_specification_schema_successor_v2/d0244_bounded_crosswalk_locator_discovery_authorization_v1/01_bounded_crosswalk_locator_discovery_authorization.v1.json",
        "sha": "a8c51e2614c337e6a265101b6ccb30d43e8a8ebfd76108883cab67d81002039b",
        "blob": "adfd70e347698e979f050da87c50c5d6ca352a16",
    },
    {
        "role": "HUMAN_READABLE_SCOPE",
        "path": "evidence/annotation_preparation/protocol_specification_schema_successor_v2/d0244_bounded_crosswalk_locator_discovery_authorization_v1/02_bounded_crosswalk_locator_discovery_authorization_scope.v1.md",
        "sha": "ba2c64cb62839028593ed85ee9f163dba3b513aa6ae24b7bc9dc150dc66deed7",
        "blob": "56c59da21c28976e917bb5195b8b3355f99ad1e0",
    },
    {
        "role": "DEFECTIVE_ORIGINAL_VERIFIER",
        "path": "evidence/annotation_preparation/protocol_specification_schema_successor_v2/d0244_bounded_crosswalk_locator_discovery_authorization_v1/03_verify_bounded_crosswalk_locator_discovery_authorization.v1.py",
        "sha": "4a7169f5f6f6adc368a32cde82fc14d6f333027364a973df2d1f8a5d202c4267",
        "blob": "257ff8197e3614538453303fed09526c2914b087",
    },
    {
        "role": "PACKAGE_MANIFEST",
        "path": "evidence/annotation_preparation/protocol_specification_schema_successor_v2/d0244_bounded_crosswalk_locator_discovery_authorization_v1/04_bounded_crosswalk_locator_discovery_authorization.v1.SHA256SUMS",
        "sha": "ca31fd630c6c5cd59e0283264197365cbe9b32ca80152115f1e01542c9914ca7",
        "blob": "4af4a80776f839affa7bb638bb0c91f4120965aa",
    },
    {
        "role": "DECISION_RECORD",
        "path": "documentation/decisions/0244-authorize-bounded-crosswalk-locator-discovery-without-execution.md",
        "sha": "ba82be121a4dc754ca5ac5c785c4b13c8b9a104f8f49a49ffcd5e8d3446ff415",
        "blob": "20177c5994935b1cb74b58b61043f0e65e8d0e04",
    },
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

record_path = pkg / "01_d0244_postcommit_verifier_binding_corrective_successor.v1.json"
scope_path = pkg / "02_d0244_postcommit_verifier_binding_corrective_scope.v1.md"


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


def commit_bytes(commit, path):
    return run_bytes(
        "git",
        "show",
        f"{commit}:{path}",
    )


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def no_dup(pairs):
    out = {}
    for k, v in pairs:
        if k in out:
            raise AssertionError("duplicate JSON key: " + k)
        out[k] = v
    return out


current_head = run_text("git", "rev-parse", "HEAD")

ancestor_rc = subprocess.run(
    [
        "git",
        "merge-base",
        "--is-ancestor",
        D0244_COMMIT,
        current_head,
    ],
    cwd=repo,
).returncode

assert ancestor_rc == 0

assert run_text(
    "git",
    "rev-parse",
    f"{D0244_COMMIT}^{{tree}}",
) == D0244_TREE

assert run_text(
    "git",
    "rev-parse",
    f"{D0244_COMMIT}^",
) == D0243_COMMIT

assert run_text(
    "git",
    "log",
    "-1",
    "--pretty=%s",
    D0244_COMMIT,
) == D0244_SUBJECT

for item in D0244_ARTIFACTS:
    blob = run_text(
        "git",
        "rev-parse",
        f"{D0244_COMMIT}:{item['path']}",
    )

    assert blob == item["blob"]

    data = commit_bytes(
        D0244_COMMIT,
        item["path"],
    )

    assert sha256_bytes(data) == item["sha"]

paths = run_text(
    "git",
    "diff-tree",
    "--no-commit-id",
    "--name-only",
    "-r",
    D0244_COMMIT,
).splitlines()

expected_paths = sorted(
    item["path"]
    for item in D0244_ARTIFACTS
)

assert sorted(paths) == expected_paths
assert len(paths) == 5

orig_record_item = next(
    x for x in D0244_ARTIFACTS
    if x["role"] == "PRIMARY_AUTHORIZATION_RECORD"
)

orig_raw = commit_bytes(
    D0244_COMMIT,
    orig_record_item["path"],
)

assert not orig_raw.endswith(b"\n")

orig = json.loads(
    orig_raw.decode("utf-8"),
    object_pairs_hook=no_dup,
)

orig_canonical = json.dumps(
    orig,
    ensure_ascii=False,
    sort_keys=True,
    separators=(",", ":"),
).encode("utf-8")

assert orig_raw == orig_canonical

assert orig["decision"] == "D0244"
assert orig["status"] == (
    "BOUNDED_CROSSWALK_LOCATOR_DISCOVERY_AUTHORIZED_NOT_EXECUTED"
)

assert orig["authorization"]["authorized"] is True
assert orig["authorization"]["executed"] is False
assert orig["authorization"]["designated_execution_decision"] == "D0245"
assert orig["authorization"]["recursion_depth"] == 1
assert len(orig["authorization"]["roots"]) == 3
assert len(orig["authorization"]["filename_filter"]["tokens"]) == 10

for value in orig["explicit_nonauthorization"].values():
    assert value is False

verifier_item = next(
    x for x in D0244_ARTIFACTS
    if x["role"] == "DEFECTIVE_ORIGINAL_VERIFIER"
)

old_verifier_text = commit_bytes(
    D0244_COMMIT,
    verifier_item["path"],
).decode("utf-8")

expected_heads = re.findall(
    r'EXPECTED_HEAD\s*=\s*["\']([0-9a-f]{40})["\']',
    old_verifier_text,
)

assert expected_heads == [D0243_COMMIT]
assert D0244_COMMIT not in old_verifier_text
assert "== EXPECTED_HEAD" in old_verifier_text

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

assert record["decision"] == "D0245"

assert record["status"] == (
    "D0244_VERIFIER_BINDING_CORRECTIVE_SUCCESSOR_CREATED_NO_LOCATOR_DISCOVERY_EXECUTION"
)

pred = record["predecessor"]

assert pred["decision"] == "D0244"
assert pred["commit"] == D0244_COMMIT
assert pred["tree"] == D0244_TREE
assert pred["parent"] == D0243_COMMIT

corr = record["correction"]

assert corr["defect_scope"] == "VERIFIER_BINDING_ONLY"
assert corr["original_d0244_authorization_semantics_invalidated"] is False

design = corr["corrected_verifier_design"]

assert design["bind_d0244_commit_object_directly"] is True
assert design["bind_d0244_tree_object_directly"] is True
assert design["bind_d0244_parent_directly"] is True
assert design["current_head_may_equal_or_descend_from_d0244"] is True
assert design["execute_original_d0244_verifier"] is False
assert design["require_current_head_equals_d0243"] is False
assert design["require_current_head_equals_d0244"] is False
assert design["verify_d0244_is_ancestor_or_equal_of_current_head"] is True

resolution = record["execution_designation_resolution"]

assert resolution["original_d0244_designated_execution_decision"] == "D0245"
assert resolution["original_d0245_execution_occurred"] is False
assert resolution["original_d0245_execution_designation_state"] == (
    "SUPERSEDED_UNEXECUTED_BY_CORRECTIVE_SUCCESSOR_NUMBER_CONSUMPTION"
)
assert resolution["replacement_execution_decision"] is None
assert resolution["replacement_execution_pre_authorized"] is False
assert resolution["transfer_execution_authorization_to_d0246"] is False

for value in record["explicit_nonauthorization"].values():
    assert value is False

preserved = record["preserved_d0244_authorization_semantics"]

assert preserved["discovery_root_count"] == 3
assert preserved["recursion_depth"] == 1
assert preserved["fixed_filename_token_count"] == 10
assert preserved["metadata_only_discovery_scope"] is True
assert preserved["locator_discovery_authorized_by_d0244"] is True
assert preserved["locator_discovery_executed"] is False

for value in record["results_not_established"].values():
    assert value is False

scope = scope_path.read_text(encoding="utf-8")

markers = [
    "CORRECTIVE SUCCESSOR ONLY — NO LOCATOR DISCOVERY EXECUTION",
    "D0244_DEFECTIVE_VERIFIER_MUST_NOT_BE_RERUN=YES",
    "SUPERSEDED_UNEXECUTED_BY_CORRECTIVE_SUCCESSOR_NUMBER_CONSUMPTION",
    "LOCATOR_DISCOVERY_EXECUTED=NO",
    "REPLACEMENT_LOCATOR_DISCOVERY_EXECUTION_DECISION_AUTHORIZED=NO",
    "C2_AUTHORIZED=NO",
    "C3_AUTHORIZED=NO",
    "B2_AUTHORIZED=NO",
    "INDEPENDENT_READ_ONLY_VERIFY_D0245_CORRECTIVE_SUCCESSOR_AND_D0244_AUTHORIZATION_BINDING",
]

for marker in markers:
    assert marker in scope, marker

print("D0245_D0244_BINDING_CORRECTIVE_SUCCESSOR_VERIFIER=PASS")
print("D0244_COMMIT_OBJECT_BINDING=PASS")
print("D0244_TREE_OBJECT_BINDING=PASS")
print("D0244_PARENT_BINDING=PASS")
print("D0244_IS_ANCESTOR_OR_EQUAL_OF_CURRENT_HEAD=YES")
print("D0244_EXACT_FIVE_PATH_SCOPE=PASS")
print("D0244_ORIGINAL_ARTIFACT_SHA256_BINDINGS=PASS")
print("D0244_ORIGINAL_ARTIFACT_GIT_BLOB_BINDINGS=PASS")
print("D0244_AUTHORIZATION_RECORD_CANONICAL_JSON=YES")
print("D0244_AUTHORIZATION_SUBSTANTIVE_SCOPE_VALID=YES")
print("D0244_DEFECTIVE_VERIFIER_STATIC_DEFECT_CONFIRMED=YES")
print("D0244_DEFECTIVE_VERIFIER_EXECUTED=NO")
print("D0244_DEFECTIVE_VERIFIER_MUST_NOT_BE_RERUN=YES")
print("D0245_ORIGINAL_EXECUTION_DESIGNATION_STATE=SUPERSEDED_UNEXECUTED_BY_CORRECTIVE_SUCCESSOR_NUMBER_CONSUMPTION")
print("REPLACEMENT_EXECUTION_DECISION_AUTHORIZED=NO")
print("LOCATOR_DISCOVERY_EXECUTED=NO")
print("C2_AUTHORIZED=NO")
print("C2_EXECUTED=NO")
print("C3_AUTHORIZED=NO")
print("B2_READINESS_ESTABLISHED=NO")
print("B2_AUTHORIZED=NO")
print("B2_EXECUTED=NO")
print("SAFE_D0245_CORRECTIVE_VERIFIER=PASS")
