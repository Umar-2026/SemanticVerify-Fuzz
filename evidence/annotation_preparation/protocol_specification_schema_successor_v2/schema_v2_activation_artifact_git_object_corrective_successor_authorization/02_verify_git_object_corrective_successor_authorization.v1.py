#!/usr/bin/env python3

import hashlib
import json
import subprocess
from pathlib import Path

REPO = Path("/openbayes/home/semanticverify-fuzz-research")

AUTH = REPO / (
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2/"
    "schema_v2_activation_artifact_git_object_corrective_successor_authorization/"
    "01_git_object_corrective_successor_authorization.v1.json"
)

FUTURE_PACKAGE = REPO / (
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2/"
    "schema_v2_activation_artifact_git_object_corrective_successor_package_v1"
)

def fail(x):
    print("FAIL|" + x)
    raise SystemExit(1)

def sha(p):
    return hashlib.sha256(
        p.read_bytes()
    ).hexdigest()

def git(*args):
    return subprocess.run(
        ["git", "-C", str(REPO), *args],
        check=True,
        stdout=subprocess.PIPE
    ).stdout.decode("utf-8").strip()

if not AUTH.is_file():
    fail("AUTH_MISSING")

if sha(AUTH) != "c8725561b71ecc72fb0d5da93b968eed70c4d7948a83baa2dd28eff66d045f8e":
    fail("AUTH_SHA")

if AUTH.stat().st_size != 14809:
    fail("AUTH_SIZE")

if FUTURE_PACKAGE.exists():
    fail("PRE_PACKAGE_AUTHORIZER_USED_AFTER_PACKAGE_CREATION")

a = json.loads(
    AUTH.read_text(
        encoding="utf-8"
    )
)

if a["status"] !=    "AUTHORIZED_TO_AUTHOR_AF04_AF07_AF08_AF09_GIT_OBJECT_CORRECTIVE_SUCCESSOR_PACKAGE_ONLY":
    fail("STATUS")

if a["authorization_scope"] != "EVIDENCE_ONLY":
    fail("SCOPE")

d = a["decision_0062_binding"]

if d["commit"] !=    "72eb427203f73d4ac83606144f434cb70a8255bb":
    fail("DEC0062_COMMIT")

if d["tree"] !=    "47069cbb0750260c08fa34b146b645acc0e58c14":
    fail("DEC0062_TREE")

if d["overall_decision"] != "REVISION_REQUIRED":
    fail("REVIEW_RESULT")

if d["open_items"] != [
    "AF04",
    "AF07",
    "AF08",
    "AF09"
]:
    fail("OPEN_ITEMS")

if d["closed_pass_items_not_reopened"] != [
    "AF01",
    "AF02",
    "AF03",
    "AF05",
    "AF06",
    "AF10"
]:
    fail("CLOSED_ITEMS")

h = a["historical_repository_target"]

checkpoint = h["checkpoint_commit_oid"]
parent = h["parent_commit_oid"]

if checkpoint !=    "fa64f7810443d14cd710600cd48ae9f9fedbb04a":
    fail("CHECKPOINT")

if parent !=    "6eba8a1fc69c0b1146e033b031f5948a245bd84b":
    fail("PARENT")

if git(
    "show",
    "-s",
    "--format=%P",
    checkpoint
) != parent:
    fail("PARENT_RELATION")

if git(
    "rev-parse",
    checkpoint + "^{tree}"
) != h["checkpoint_root_tree_oid"]:
    fail("CHECKPOINT_ROOT_TREE")

if git(
    "rev-parse",
    parent + "^{tree}"
) != h["parent_root_tree_oid"]:
    fail("PARENT_ROOT_TREE")

if git(
    "rev-parse",
    checkpoint + ":config"
) != h["checkpoint_config_tree_oid"]:
    fail("CHECKPOINT_CONFIG_TREE")

if git(
    "rev-parse",
    parent + ":config"
) != h["parent_config_tree_oid"]:
    fail("PARENT_CONFIG_TREE")

if h["checkpoint_config_tree_oid"] !=    h["parent_config_tree_oid"]:
    fail("CONFIG_TREE_NOT_IDENTICAL")

if git(
    "rev-parse",
    checkpoint + ":documentation"
) != h["checkpoint_documentation_tree_oid"]:
    fail("CHECKPOINT_DOCUMENTATION_TREE")

if git(
    "rev-parse",
    parent + ":documentation"
) != h["parent_documentation_tree_oid"]:
    fail("PARENT_DOCUMENTATION_TREE")

if h["checkpoint_documentation_tree_oid"] !=    h["parent_documentation_tree_oid"]:
    fail("DOCUMENTATION_TREE_NOT_IDENTICAL")

changed = sorted(
    x
    for x in git(
        "diff-tree",
        "--no-commit-id",
        "--name-only",
        "-r",
        checkpoint
    ).splitlines()
    if x
)

if changed != h["package_changed_paths"]:
    fail("CHANGED_PATH_BINDING")

if len(changed) != 22:
    fail("CHANGED_PATH_COUNT")

prefix = (
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2/"
    "schema_v2_activation_artifact_finalization_package_v1/"
)

if any(
    not x.startswith(prefix)
    for x in changed
):
    fail("CHANGED_PATH_SCOPE")

package_path = prefix.rstrip("/")

r = subprocess.run(
    [
        "git",
        "-C",
        str(REPO),
        "cat-file",
        "-e",
        parent + ":" + package_path
    ],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)

if r.returncode == 0:
    fail("PACKAGE_PRESENT_IN_PARENT")

if git(
    "rev-parse",
    checkpoint + ":" + package_path
) != h["checkpoint_package_tree_oid"]:
    fail("PACKAGE_TREE_BINDING")

for label, b in a[
    "core_path_blob_bindings"
].items():
    path = b["path"]

    cp = git(
        "rev-parse",
        checkpoint + ":" + path
    )

    pp = git(
        "rev-parse",
        parent + ":" + path
    )

    if cp != b["checkpoint_blob_oid"]:
        fail("CORE_CP|" + label)

    if pp != b["parent_blob_oid"]:
        fail("CORE_PARENT|" + label)

    if cp != pp:
        fail("CORE_NONIDENTITY|" + label)

    if git(
        "cat-file",
        "-t",
        cp
    ) != "blob":
        fail("CORE_NOT_BLOB|" + label)

for item in a["required_absence_proofs"]:
    path = item["path"]

    for commit, key in (
        (checkpoint, "checkpoint_absent"),
        (parent, "parent_absent"),
    ):
        r = subprocess.run(
            [
                "git",
                "-C",
                str(REPO),
                "cat-file",
                "-e",
                commit + ":" + path
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        absent = r.returncode != 0

        if absent is not item[key]:
            fail(
                "ABSENCE|"
                + key
                + "|"
                + path
            )

req = a[
    "authorized_corrective_package_requirements"
]

if set(req) != {
    f"GE{i:02d}"
    for i in range(1, 11)
}:
    fail("GE01_GE10_SET")

contract = a[
    "raw_git_object_export_contract"
]

if contract[
    "portable_verifier_must_not_require_repository_access"
] is not True:
    fail("PORTABLE_REPO_INDEPENDENCE")

if contract[
    "portable_verifier_must_recompute_all_exported_object_ids"
] is not True:
    fail("OID_RECOMPUTATION")

if contract[
    "portable_verifier_must_parse_tree_objects"
] is not True:
    fail("TREE_PARSER")

if contract[
    "portable_verifier_must_resolve_paths_from_exported_trees"
] is not True:
    fail("PATH_RESOLUTION")

if contract[
    "portable_verifier_must_prove_absence_by_tree_entry_nonexistence"
] is not True:
    fail("ABSENCE_BY_TREE")

for key, value in a[
    "explicit_non_authorizations"
].items():
    if value is not False:
        fail("NONAUTH|" + key)

print("DECISION_0062_REVIEW_BINDING=PASS")
print("OPEN_AF_ITEMS=AF04,AF07,AF08,AF09")
print("CLOSED_AF_ITEMS_NOT_REOPENED=AF01,AF02,AF03,AF05,AF06,AF10")
print("CHECKPOINT_PARENT_GIT_OBJECT_RELATION=PASS")
print("CHECKPOINT_ROOT_TREE_BINDING=PASS")
print("PARENT_ROOT_TREE_BINDING=PASS")
print("CONFIG_TREE_IDENTITY=PASS")
print("DOCUMENTATION_TREE_IDENTITY=PASS")
print("PACKAGE_ONLY_CHANGED_PATH_SCOPE=PASS")
print("CORE_ARTIFACT_BLOB_BINDINGS=PASS")
print("ACTIVE_V2_HASH_PATH_ABSENCE=PASS")
print("ACTIVE_VERSION_DISPATCH_PATH_ABSENCE=PASS")
print("CURL_JSON_PATH_ABSENCE=PASS")
print("GE01_TO_GE10_REQUIREMENTS=BOUND")
print("RAW_GIT_OBJECT_CORRECTIVE_SUCCESSOR_PACKAGE_AUTHORING_AUTHORIZED=YES")
print("INDEPENDENT_FOCUSED_AF04_AF07_AF08_AF09_REREVIEW_REQUIRED=YES")
print("SCHEMA_V2_ACTIVATED=NO")
print("RAW_GIT_OBJECT_CORRECTIVE_AUTHORIZATION_VERIFICATION=PASS")
