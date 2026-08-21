#!/usr/bin/env python3

import hashlib
import json
import subprocess
from pathlib import Path

def fail(x):
    print("FAIL|" + x)
    raise SystemExit(1)

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def git(*args, binary=False):
    return subprocess.check_output(
        ["git", "-C", str(repo), *args],
        text=not binary
    )

here = Path(__file__).resolve().parent
repo = here

while repo != repo.parent and not (repo / ".git").exists():
    repo = repo.parent

authp = (
    here /
    "01_corrective_review_package_v3_authoring_authorization.v1.json"
)

base = (
    repo /
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2"
)

pkg2 = base / "review_package_v2"
pkg3 = base / "review_package_v3"

rereview = (
    base /
    "completed_corrective_human_rereview_v2/"
    "01_completed_schema_v2_corrective_human_rereview.REVISION_REQUIRED.v2.md"
)

rereview_record = (
    base /
    "completed_corrective_human_rereview_v2/"
    "02_completed_schema_v2_corrective_human_rereview_record.v2.json"
)

v2p = repo / "config/schemas/protocol_specification.v2.schema.json"
v1p = repo / "config/schemas/protocol_specification.schema.json"
zlibp = repo / "config/protocol_specifications/zlib.json"
pcapp = repo / "config/protocol_specifications/libpcap.json"
curlp = repo / "config/protocol_specifications/curl.json"

V2_SHA = "c6ebb5ef2214c4168283f9009d1f7ce6e88d2ff928853fe6a57ed1f7521c6956"
V1_SHA = "7eb17eeb8f49b37420d0d1d71539cf0d7cb08241ecf133e7b4139fd130718b34"
ZLIB_SHA = "f4c94c1c151b893e2e4f1fae7d43b1196432cbcceaa7f9428968d45f2f77b7b1"
PCAP_SHA = "b2877713a3d8c38ecf135544f4cab7a2230e39b4ed73e18a7965497b3901ef73"

REREVIEW_SHA = "80852675eeb63508644e20caa4b7c6fdd5d73cd361bd9b072474e12521c3ac40"
REREVIEW_RECORD_SHA = "01486959b88c17e4f4259d8fd3d6b45177081b6d85aeb83784b6c221b7b514c9"

PKG2_COMMIT = "75dd1d9c5a3d01d72b76f9d76e8abb56113187e5"
PKG2_PARENT = "bf6cf53d54c105353906f02c6fa117668b635eae"
PKG2_TREE = "d2bc2301cea0ef87aeae7b37278ba1d5440aae57"

PKG2_MANIFEST_SHA = "68902be116599ff915b8efadcb58b4fbb3107d4abf35d330d723c42f69922bd4"
PKG2_SUMS_SHA = "de583d227d8869bafda83219bab02c02ca718129d9209626e39dc1ed4f52fdcf"

if sha(v2p) != V2_SHA:
    fail("SCHEMA_V2_SHA")

if v2p.stat().st_size != 43030:
    fail("SCHEMA_V2_SIZE")

if sha(v1p) != V1_SHA:
    fail("SCHEMA_V1_SHA")

if sha(zlibp) != ZLIB_SHA:
    fail("ZLIB_SHA")

if sha(pcapp) != PCAP_SHA:
    fail("LIBPCAP_SHA")

if sha(rereview) != REREVIEW_SHA:
    fail("REREVIEW_SHA")

if sha(rereview_record) != REREVIEW_RECORD_SHA:
    fail("REREVIEW_RECORD_SHA")

if sha(pkg2 / "14_corrective_review_package_manifest.v2.json") != \
   PKG2_MANIFEST_SHA:
    fail("PKG2_MANIFEST_SHA")

if sha(pkg2 / "16_corrective_review_package.v2.SHA256SUMS") != \
   PKG2_SUMS_SHA:
    fail("PKG2_SUMS_SHA")

if pkg3.exists():
    fail("REVIEW_PACKAGE_V3_ALREADY_EXISTS")

if curlp.exists():
    fail("CURL_JSON_EXISTS")

auth = json.loads(
    authp.read_text(encoding="utf-8")
)

if auth["status"] != \
   "AUTHORIZED_FOR_CORRECTIVE_REVIEW_PACKAGE_V3_AUTHORING_SV2_RR09_EVIDENCE_ONLY":
    fail("AUTH_STATUS")

if auth["basis"]["closed_item"] != "SV2-RR02":
    fail("CLOSED_ITEM")

if auth["basis"]["remaining_open_item"] != "SV2-RR09":
    fail("OPEN_ITEM")

if auth["basis"]["remaining_scope"] != "SV2-RR09-EVIDENCE-ONLY":
    fail("SCOPE")

if auth["authorized_successor"]["authoring_authorized"] is not True:
    fail("AUTHORING_AUTHORIZED")

if auth["authorized_successor"]["scope"] != "SV2-RR09-EVIDENCE-ONLY":
    fail("SUCCESSOR_SCOPE")

if auth["authorized_successor"][
    "schema_v2_content_change_authorized"
] is not False:
    fail("SCHEMA_CONTENT_CHANGE")

if auth["authorized_successor"]["human_rereview_required"] is not True:
    fail("HUMAN_REREVIEW")

proof = auth["required_package_v2_checkpoint_proof"]

if proof["checkpoint_commit"] != PKG2_COMMIT:
    fail("CHECKPOINT_COMMIT")

if proof["immediate_parent_commit"] != PKG2_PARENT:
    fail("PARENT_COMMIT")

if proof["checkpoint_root_tree"] != PKG2_TREE:
    fail("CHECKPOINT_TREE")

actual_tree = git(
    "rev-parse",
    PKG2_COMMIT + "^{tree}"
).strip()

if actual_tree != proof["checkpoint_root_tree"]:
    fail("CHECKPOINT_TREE_GIT")

actual_parent = git(
    "show",
    "-s",
    "--format=%P",
    PKG2_COMMIT
).strip()

if actual_parent != PKG2_PARENT:
    fail("PARENT_GIT")

parent_tree = git(
    "rev-parse",
    PKG2_PARENT + "^{tree}"
).strip()

if parent_tree != proof["immediate_parent_root_tree"]:
    fail("PARENT_TREE")

def tree(commit, path):
    return git(
        "rev-parse",
        f"{commit}:{path}"
    ).strip()

def blob(commit, path):
    return tree(commit, path)

if tree(PKG2_COMMIT, "config") != \
   proof["checkpoint_config_tree"]:
    fail("CHECKPOINT_CONFIG_TREE")

if tree(PKG2_PARENT, "config") != \
   proof["parent_config_tree"]:
    fail("PARENT_CONFIG_TREE")

if tree(PKG2_COMMIT, "config/schemas") != \
   proof["checkpoint_schemas_tree"]:
    fail("CHECKPOINT_SCHEMAS_TREE")

if tree(PKG2_PARENT, "config/schemas") != \
   proof["parent_schemas_tree"]:
    fail("PARENT_SCHEMAS_TREE")

if tree(PKG2_COMMIT, "config/protocol_specifications") != \
   proof["checkpoint_protocol_specifications_tree"]:
    fail("CHECKPOINT_PROTOCOL_TREE")

if tree(PKG2_PARENT, "config/protocol_specifications") != \
   proof["parent_protocol_specifications_tree"]:
    fail("PARENT_PROTOCOL_TREE")

if blob(
    PKG2_COMMIT,
    "config/schemas/protocol_specification.v2.schema.json"
) != proof["checkpoint_schema_v2_blob"]:
    fail("CHECKPOINT_V2_BLOB")

if blob(
    PKG2_PARENT,
    "config/schemas/protocol_specification.v2.schema.json"
) != proof["parent_schema_v2_blob"]:
    fail("PARENT_V2_BLOB")

if blob(
    PKG2_COMMIT,
    "config/protocol_specifications/zlib.json"
) != proof["checkpoint_zlib_blob"]:
    fail("CHECKPOINT_ZLIB_BLOB")

if blob(
    PKG2_PARENT,
    "config/protocol_specifications/zlib.json"
) != proof["parent_zlib_blob"]:
    fail("PARENT_ZLIB_BLOB")

if blob(
    PKG2_COMMIT,
    "config/protocol_specifications/libpcap.json"
) != proof["checkpoint_libpcap_blob"]:
    fail("CHECKPOINT_LIBPCAP_BLOB")

if blob(
    PKG2_PARENT,
    "config/protocol_specifications/libpcap.json"
) != proof["parent_libpcap_blob"]:
    fail("PARENT_LIBPCAP_BLOB")

for key in (
    "checkpoint_parent_config_tree_identical",
    "checkpoint_parent_schemas_tree_identical",
    "checkpoint_parent_protocol_specifications_tree_identical",
    "checkpoint_parent_schema_v2_blob_identical",
    "checkpoint_parent_zlib_blob_identical",
    "checkpoint_parent_libpcap_blob_identical",
    "changed_paths_all_within_review_package_v2",
):
    if proof[key] is not True:
        fail("PROOF_FLAG|" + key)

changed = git(
    "diff-tree",
    "--no-commit-id",
    "--name-only",
    "-r",
    PKG2_PARENT,
    PKG2_COMMIT
).splitlines()

changed = sorted(x for x in changed if x)

if len(changed) != proof["changed_path_count"]:
    fail("CHANGED_PATH_COUNT")

prefix = (
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2/"
    "review_package_v2/"
)

if not changed:
    fail("NO_CHANGED_PATHS")

for path in changed:
    if not path.startswith(prefix):
        fail("OUT_OF_SCOPE_CHANGED_PATH|" + path)

anti = auth["anti_recursion_handoff_requirement"]

if anti["enabled"] is not True:
    fail("ANTI_RECURSION_DISABLED")

if anti[
    "postcommit_proof_must_not_modify_review_package_v3"
] is not True:
    fail("POSTCOMMIT_MUTABILITY")

review = auth["review_semantics"]

if review["sv2_rr02_must_not_be_reopened"] is not True:
    fail("RR02_REOPEN")

if review["sv2_rr02_status"] != "PASS_CLOSED":
    fail("RR02_STATUS")

if review["sv2_rr09_requires_new_human_rereview"] is not True:
    fail("RR09_REREVIEW")

if review["new_human_rereview_scope"] != "SV2-RR09-ONLY":
    fail("REREVIEW_SCOPE")

if review["approval_does_not_activate_schema_v2"] is not True:
    fail("APPROVAL_ACTIVATION")

if review["no_synthetic_human_decision"] is not True:
    fail("SYNTHETIC_DECISION")

for key, value in auth["explicit_non_authorizations"].items():
    if value is not False:
        fail("NONAUTH|" + key)

if auth["next_boundary"] != \
   "AUTHOR_SCHEMA_V2_CORRECTIVE_REVIEW_PACKAGE_V3_FOR_SV2_RR09_ONLY":
    fail("NEXT_BOUNDARY")

print("DECISION_0054_CORRECTIVE_REREVIEW_BINDING=PASS")
print("SV2_RR02_STATUS=PASS_CLOSED")
print("SV2_RR09_STATUS=REVISION_REQUIRED_OPEN")
print("PACKAGE_V2_CHECKPOINT_PARENT_COMMIT_BINDING=PASS")
print("PACKAGE_V2_CHECKPOINT_PARENT_CONFIG_TREE_IDENTITY=PASS")
print("PACKAGE_V2_CHECKPOINT_PARENT_SCHEMA_V2_IDENTITY=PASS")
print("PACKAGE_V2_CHECKPOINT_PARENT_ZLIB_IDENTITY=PASS")
print("PACKAGE_V2_CHECKPOINT_PARENT_LIBPCAP_IDENTITY=PASS")
print("PACKAGE_V2_CHANGED_PATH_SCOPE=REVIEW_PACKAGE_V2_ONLY")
print("ANTI_RECURSION_POSTCOMMIT_HANDOFF_REQUIREMENT=ENABLED")
print("SCHEMA_V2_CANDIDATE_IMMUTABLE=YES")
print("REVIEW_PACKAGE_V2_IMMUTABLE=YES")
print("CORRECTIVE_REVIEW_PACKAGE_V3_AUTHORING_AUTHORIZED=YES")
print("CORRECTIVE_SCOPE=SV2_RR09_EVIDENCE_ONLY")
print("SCHEMA_V2_ACTIVATED=NO")
print("POSITIVE_V4_TO_V2_MAPPING_DEFINED=NO")
print("CURL_JSON_CREATED=NO")
print("CORRECTIVE_REVIEW_PACKAGE_V3_AUTHORING_AUTHORIZATION_VERIFICATION=PASS")
