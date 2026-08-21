#!/usr/bin/env python3

import hashlib
import json
from pathlib import Path

def fail(x):
    print("FAIL|" + x)
    raise SystemExit(1)

def oid(kind, raw):
    return hashlib.sha1(
        f"{kind} {len(raw)}\0".encode()
        + raw
    ).hexdigest()

def parse_tree(raw):
    out = {}
    i = 0

    while i < len(raw):
        sp = raw.index(b" ", i)
        mode = raw[i:sp].decode()

        nul = raw.index(
            b"\0",
            sp + 1
        )

        name = raw[
            sp + 1:nul
        ].decode()

        obj = raw[
            nul + 1:
            nul + 21
        ].hex()

        out[name] = {
            "mode": mode,
            "oid": obj
        }

        i = nul + 21

    return out

def same_except(a, b, ignored):
    return {
        k: v
        for k, v in a.items()
        if k not in ignored
    } == {
        k: v
        for k, v in b.items()
        if k not in ignored
    }

here = Path(__file__).resolve().parent

m = json.loads(
    (
        here /
        "00_postcommit_noninterference_manifest.v1.json"
    ).read_text(encoding="utf-8")
)

cp_commit = (
    here /
    "01_checkpoint_commit.raw"
).read_bytes()

pa_commit = (
    here /
    "02_parent_commit.raw"
).read_bytes()

if oid("commit", cp_commit) != m["checkpoint_commit"]:
    fail("CHECKPOINT_COMMIT_OID")

if oid("commit", pa_commit) != m["parent_commit"]:
    fail("PARENT_COMMIT_OID")

cp_lines = cp_commit.decode(
    "utf-8",
    errors="strict"
).splitlines()

pa_lines = pa_commit.decode(
    "utf-8",
    errors="strict"
).splitlines()

if cp_lines[0] != \
   "tree " + m["checkpoint_root_tree"]:
    fail("CHECKPOINT_ROOT_BINDING")

if pa_lines[0] != \
   "tree " + m["parent_root_tree"]:
    fail("PARENT_ROOT_BINDING")

parents = [
    x.split(" ", 1)[1]
    for x in cp_lines
    if x.startswith("parent ")
]

if parents != [m["parent_commit"]]:
    fail("CHECKPOINT_PARENT_BINDING")

cp_root_raw = (
    here /
    "03_checkpoint_root_tree.raw"
).read_bytes()

pa_root_raw = (
    here /
    "04_parent_root_tree.raw"
).read_bytes()

if oid("tree", cp_root_raw) != m["checkpoint_root_tree"]:
    fail("CHECKPOINT_ROOT_OID")

if oid("tree", pa_root_raw) != m["parent_root_tree"]:
    fail("PARENT_ROOT_OID")

tree_names = (
    "config",
    "schemas",
    "protocol_specifications",
    "documentation",
    "decisions",
    "evidence",
    "annotation_preparation",
    "schema_successor_root",
    "activation_governance_package",
    "completed_activation_governance_review",
    "hash_finalization_authorization",
)

trees = {}
counter = 5

for key in tree_names:
    for side in ("checkpoint", "parent"):
        filename = (
            f"{counter:02d}_{side}_{key}_tree.raw"
        )

        raw = (
            here /
            filename
        ).read_bytes()

        expected = (
            m["checkpoint_trees"][key]
            if side == "checkpoint"
            else m["parent_trees"][key]
        )

        if oid("tree", raw) != expected:
            fail(
                "TREE_OID|"
                + side
                + "|"
                + key
            )

        trees[
            ("cp_" if side == "checkpoint" else "pa_")
            + key
        ] = parse_tree(raw)

        counter += 1

package_raw = (
    here /
    f"{counter:02d}_checkpoint_package_tree.raw"
).read_bytes()

if oid("tree", package_raw) != m["package_tree"]:
    fail("PACKAGE_TREE_OID")

counter += 1

blob_names = (
    "source_hash",
    "activation_governance_approval",
    "finalization_authorization",
    "schema_v1",
    "schema_v2",
    "hash_v1",
    "decision_0019",
    "decision_0059",
    "zlib",
    "libpcap",
)

for key in blob_names:
    for side in ("checkpoint", "parent"):
        filename = (
            f"{counter:02d}_{side}_{key}_blob.raw"
        )

        raw = (
            here /
            filename
        ).read_bytes()

        expected_oid = (
            m["checkpoint_blobs"][key]
            if side == "checkpoint"
            else m["parent_blobs"][key]
        )

        if oid("blob", raw) != expected_oid:
            fail(
                "BLOB_OID|"
                + side
                + "|"
                + key
            )

        if key != "decision_0059":
            if hashlib.sha256(raw).hexdigest() != \
               m["expected_sha256"][key]:
                fail(
                    "BLOB_SHA|"
                    + side
                    + "|"
                    + key
                )

        counter += 1

changed_file = (
    here /
    f"{counter:02d}_changed_paths.v1.txt"
)

changed = [
    x
    for x in changed_file.read_text(
        encoding="utf-8"
    ).splitlines()
    if x
]

if changed != m["changed_paths"]:
    fail("CHANGED_PATH_LIST")

if len(changed) != 39:
    fail("CHANGED_PATH_COUNT")

prefix = (
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2/"
    "schema_v2_hash_contract_finalization_package_v1/"
)

for path in changed:
    if not path.startswith(prefix):
        fail(
            "OUT_OF_SCOPE_CHANGED_PATH|"
            + path
        )

cp_root = parse_tree(cp_root_raw)
pa_root = parse_tree(pa_root_raw)

if not same_except(
    cp_root,
    pa_root,
    {"evidence"}
):
    fail("ROOT_CHANGED_OUTSIDE_EVIDENCE")

if trees["cp_config"] != trees["pa_config"]:
    fail("CONFIG_TREE_IDENTITY")

if trees["cp_documentation"] != \
   trees["pa_documentation"]:
    fail("DOCUMENTATION_TREE_IDENTITY")

if trees["cp_schemas"] != \
   trees["pa_schemas"]:
    fail("SCHEMAS_TREE_IDENTITY")

if trees["cp_protocol_specifications"] != \
   trees["pa_protocol_specifications"]:
    fail("PROTOCOL_TREE_IDENTITY")

if trees["cp_decisions"] != \
   trees["pa_decisions"]:
    fail("DECISIONS_TREE_IDENTITY")

config = trees["cp_config"]

if "protocol_content_hash_canonicalization.v2.json" in config:
    fail("ACTIVE_V2_HASH_PRESENT_CHECKPOINT")

if "protocol_content_hash_canonicalization.v2.json" in \
   trees["pa_config"]:
    fail("ACTIVE_V2_HASH_PRESENT_PARENT")

schemas = trees["cp_schemas"]

if schemas.get(
    "protocol_specification.v2.schema.json",
    {}
).get("oid") != m["checkpoint_blobs"]["schema_v2"]:
    fail("SCHEMA_V2_PATH_BINDING")

if schemas.get(
    "protocol_specification.schema.json",
    {}
).get("oid") != m["checkpoint_blobs"]["schema_v1"]:
    fail("SCHEMA_V1_PATH_BINDING")

protocol = trees["cp_protocol_specifications"]

if protocol.get(
    "zlib.json",
    {}
).get("oid") != m["checkpoint_blobs"]["zlib"]:
    fail("ZLIB_PATH_BINDING")

if protocol.get(
    "libpcap.json",
    {}
).get("oid") != m["checkpoint_blobs"]["libpcap"]:
    fail("LIBPCAP_PATH_BINDING")

if "curl.json" in protocol:
    fail("CURL_JSON_PRESENT_CHECKPOINT")

if "curl.json" in trees["pa_protocol_specifications"]:
    fail("CURL_JSON_PRESENT_PARENT")

decisions = trees["cp_decisions"]

if decisions.get(
    "0019-canonical-library-protocol-specification-path-convention.md",
    {}
).get("oid") != m["checkpoint_blobs"]["decision_0019"]:
    fail("DECISION_0019_PATH_BINDING")

if decisions.get(
    "0059-authorize-active-schema-v2-hash-contract-finalization-governance.md",
    {}
).get("oid") != m["checkpoint_blobs"]["decision_0059"]:
    fail("DECISION_0059_PATH_BINDING")

if config.get(
    "protocol_content_hash_canonicalization.v1.json",
    {}
).get("oid") != m["checkpoint_blobs"]["hash_v1"]:
    fail("V1_HASH_PATH_BINDING")

if trees["cp_activation_governance_package"] != \
   trees["pa_activation_governance_package"]:
    fail("ACTIVATION_GOVERNANCE_PACKAGE_TREE_IDENTITY")

if trees["cp_completed_activation_governance_review"] != \
   trees["pa_completed_activation_governance_review"]:
    fail("ACTIVATION_GOVERNANCE_APPROVAL_TREE_IDENTITY")

if trees["cp_hash_finalization_authorization"] != \
   trees["pa_hash_finalization_authorization"]:
    fail("FINALIZATION_AUTHORIZATION_TREE_IDENTITY")

if trees[
    "cp_activation_governance_package"
].get(
    "07_proposed_v2_hash_contract.REVIEW_CANDIDATE.json",
    {}
).get("oid") != m["checkpoint_blobs"]["source_hash"]:
    fail("SOURCE_HASH_PATH_BINDING")

if trees[
    "cp_completed_activation_governance_review"
].get(
    "04_completed_activation_governance_human_approval_record.v1.json",
    {}
).get("oid") != m["checkpoint_blobs"]["activation_governance_approval"]:
    fail("ACTIVATION_APPROVAL_PATH_BINDING")

if trees[
    "cp_hash_finalization_authorization"
].get(
    "01_schema_v2_hash_contract_finalization_authorization.v1.json",
    {}
).get("oid") != m["checkpoint_blobs"]["finalization_authorization"]:
    fail("FINALIZATION_AUTH_PATH_BINDING")

cp_evidence = trees["cp_evidence"]
pa_evidence = trees["pa_evidence"]

if not same_except(
    cp_evidence,
    pa_evidence,
    {"annotation_preparation"}
):
    fail("EVIDENCE_CHANGED_OUTSIDE_ANNOTATION_PREPARATION")

cp_annotation = trees["cp_annotation_preparation"]
pa_annotation = trees["pa_annotation_preparation"]

target = "protocol_specification_schema_successor_v2"

if not same_except(
    cp_annotation,
    pa_annotation,
    {target}
):
    fail("ANNOTATION_CHANGED_OUTSIDE_SCHEMA_SUCCESSOR")

cp_successor = trees["cp_schema_successor_root"]
pa_successor = trees["pa_schema_successor_root"]

pkg_name = "schema_v2_hash_contract_finalization_package_v1"

if pkg_name in pa_successor:
    fail("PACKAGE_PRESENT_IN_PARENT")

if cp_successor.get(
    pkg_name,
    {}
).get("oid") != m["package_tree"]:
    fail("PACKAGE_SUBTREE_BINDING")

if not same_except(
    cp_successor,
    pa_successor,
    {pkg_name}
):
    fail("SCHEMA_SUCCESSOR_CHANGED_OUTSIDE_PACKAGE")

for key in blob_names:
    if m["checkpoint_blobs"][key] != \
       m["parent_blobs"][key]:
        fail(
            "CHECKPOINT_PARENT_BLOB_NONIDENTITY|"
            + key
        )

if m[
    "active_v2_hash_absent_at_checkpoint_and_parent"
] is not True:
    fail("ACTIVE_HASH_ABSENCE_CLAIM")

if m[
    "curl_json_absent_at_checkpoint_and_parent"
] is not True:
    fail("CURL_ABSENCE_CLAIM")

for key, value in m["claims"].items():
    if value is not True:
        fail("CLAIM|" + key)

print("HASH_FINALIZATION_POSTCOMMIT_CHECKPOINT_COMMIT_OBJECT=PASS")
print("HASH_FINALIZATION_POSTCOMMIT_PARENT_COMMIT_OBJECT=PASS")
print("HASH_FINALIZATION_POSTCOMMIT_ROOT_PATH_CHAIN=PASS")
print("HASH_FINALIZATION_POSTCOMMIT_CONFIG_TREE_IDENTITY=PASS")
print("HASH_FINALIZATION_POSTCOMMIT_DOCUMENTATION_TREE_IDENTITY=PASS")
print("HASH_FINALIZATION_POSTCOMMIT_SCHEMA_V2_PATH_BLOB_IDENTITY=PASS")
print("HASH_FINALIZATION_POSTCOMMIT_V1_HASH_PATH_BLOB_IDENTITY=PASS")
print("HASH_FINALIZATION_POSTCOMMIT_SOURCE_HASH_PATH_BLOB_IDENTITY=PASS")
print("HASH_FINALIZATION_POSTCOMMIT_APPROVAL_PATH_BLOB_IDENTITY=PASS")
print("HASH_FINALIZATION_POSTCOMMIT_AUTHORIZATION_PATH_BLOB_IDENTITY=PASS")
print("HASH_FINALIZATION_POSTCOMMIT_DECISION_0019_PATH_BLOB_IDENTITY=PASS")
print("HASH_FINALIZATION_POSTCOMMIT_DECISION_0059_PATH_BLOB_IDENTITY=PASS")
print("HASH_FINALIZATION_POSTCOMMIT_ZLIB_PATH_BLOB_IDENTITY=PASS")
print("HASH_FINALIZATION_POSTCOMMIT_LIBPCAP_PATH_BLOB_IDENTITY=PASS")
print("HASH_FINALIZATION_POSTCOMMIT_ACTIVE_V2_HASH_ABSENT=PASS")
print("HASH_FINALIZATION_POSTCOMMIT_CURL_JSON_ABSENT=PASS")
print("HASH_FINALIZATION_POSTCOMMIT_CHANGED_PATH_SCOPE=PACKAGE_ONLY")
print("PORTABLE_HASH_FINALIZATION_PACKAGE_POSTCOMMIT_NONINTERFERENCE_PROOF=PASS")
