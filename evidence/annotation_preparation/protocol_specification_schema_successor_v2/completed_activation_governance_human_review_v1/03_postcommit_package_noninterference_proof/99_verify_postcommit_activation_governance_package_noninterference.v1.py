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
            "oid": obj,
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
    ).read_text(
        encoding="utf-8"
    )
)

cp_commit = (
    here /
    "01_checkpoint_commit.raw"
).read_bytes()

pa_commit = (
    here /
    "02_parent_commit.raw"
).read_bytes()

if oid(
    "commit",
    cp_commit
) != m["checkpoint_commit"]:
    fail("CHECKPOINT_COMMIT_OID")

if oid(
    "commit",
    pa_commit
) != m["parent_commit"]:
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
    line.split(" ", 1)[1]
    for line in cp_lines
    if line.startswith("parent ")
]

if parents != [m["parent_commit"]]:
    fail("CHECKPOINT_PARENT_BINDING")

tree_names = [
    "config",
    "schemas",
    "protocol_specifications",
    "documentation",
    "decisions",
    "evidence",
    "annotation_preparation",
    "schema_successor_root",
]

raw = {}

raw["cp_root"] = (
    here /
    "03_checkpoint_root_tree.raw"
).read_bytes()

raw["pa_root"] = (
    here /
    "04_parent_root_tree.raw"
).read_bytes()

if oid(
    "tree",
    raw["cp_root"]
) != m["checkpoint_root_tree"]:
    fail("CHECKPOINT_ROOT_OID")

if oid(
    "tree",
    raw["pa_root"]
) != m["parent_root_tree"]:
    fail("PARENT_ROOT_OID")

counter = 5

for key in tree_names:
    for side in (
        "checkpoint",
        "parent",
    ):
        filename = (
            f"{counter:02d}_{side}_{key}_tree.raw"
        )

        b = (
            here /
            filename
        ).read_bytes()

        expected = (
            m["checkpoint_trees"][key]
            if side == "checkpoint"
            else m["parent_trees"][key]
        )

        if oid(
            "tree",
            b
        ) != expected:
            fail(
                "TREE_OID|"
                + side
                + "|"
                + key
            )

        raw[
            ("cp_" if side == "checkpoint" else "pa_")
            + key
        ] = b

        counter += 1

package_raw = (
    here /
    f"{counter:02d}_checkpoint_package_tree.raw"
).read_bytes()

if oid(
    "tree",
    package_raw
) != m["package_tree"]:
    fail("PACKAGE_TREE_OID")

counter += 1

blob_keys = (
    "schema_v1",
    "schema_v2",
    "hash_v1",
    "zlib",
    "libpcap",
    "decision_0019",
)

blob_raw = {}

for key in blob_keys:
    for side in (
        "checkpoint",
        "parent",
    ):
        filename = (
            f"{counter:02d}_{side}_{key}_blob.raw"
        )

        b = (
            here /
            filename
        ).read_bytes()

        expected_oid = (
            m["checkpoint_blobs"][key]
            if side == "checkpoint"
            else m["parent_blobs"][key]
        )

        if oid(
            "blob",
            b
        ) != expected_oid:
            fail(
                "BLOB_OID|"
                + side
                + "|"
                + key
            )

        if hashlib.sha256(
            b
        ).hexdigest() != m["expected_sha256"][key]:
            fail(
                "BLOB_SHA|"
                + side
                + "|"
                + key
            )

        blob_raw[
            ("cp_" if side == "checkpoint" else "pa_")
            + key
        ] = b

        counter += 1

changed_file = (
    here /
    f"{counter:02d}_changed_paths.v1.txt"
)

changed = [
    x for x in changed_file.read_text(
        encoding="utf-8"
    ).splitlines()
    if x
]

if changed != m["changed_paths"]:
    fail("CHANGED_PATH_LIST")

if len(changed) != 37:
    fail("CHANGED_PATH_COUNT")

prefix = (
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2/"
    "schema_v2_activation_governance_package_v1/"
)

for path in changed:
    if not path.startswith(prefix):
        fail(
            "OUT_OF_SCOPE_CHANGED_PATH|"
            + path
        )

cp_root = parse_tree(
    raw["cp_root"]
)

pa_root = parse_tree(
    raw["pa_root"]
)

if cp_root.get(
    "config",
    {}
).get("oid") != \
   m["checkpoint_trees"]["config"]:
    fail("CHECKPOINT_ROOT_CONFIG")

if pa_root.get(
    "config",
    {}
).get("oid") != \
   m["parent_trees"]["config"]:
    fail("PARENT_ROOT_CONFIG")

if cp_root.get(
    "documentation",
    {}
).get("oid") != \
   m["checkpoint_trees"]["documentation"]:
    fail("CHECKPOINT_ROOT_DOCUMENTATION")

if pa_root.get(
    "documentation",
    {}
).get("oid") != \
   m["parent_trees"]["documentation"]:
    fail("PARENT_ROOT_DOCUMENTATION")

if not same_except(
    cp_root,
    pa_root,
    {"evidence"}
):
    fail("ROOT_CHANGED_OUTSIDE_EVIDENCE")

cp_config = parse_tree(
    raw["cp_config"]
)

pa_config = parse_tree(
    raw["pa_config"]
)

if cp_config != pa_config:
    fail("CONFIG_TREE_CONTENT_IDENTITY")

if m["checkpoint_trees"]["config"] != \
   m["parent_trees"]["config"]:
    fail("CONFIG_TREE_OID_IDENTITY")

if cp_config.get(
    "schemas",
    {}
).get("oid") != \
   m["checkpoint_trees"]["schemas"]:
    fail("CONFIG_SCHEMAS_BINDING")

if cp_config.get(
    "protocol_specifications",
    {}
).get("oid") != \
   m["checkpoint_trees"]["protocol_specifications"]:
    fail("CONFIG_PROTOCOL_BINDING")

if "protocol_content_hash_canonicalization.v2.json" in cp_config:
    fail("ACTIVE_V2_HASH_PRESENT_CHECKPOINT")

if "protocol_content_hash_canonicalization.v2.json" in pa_config:
    fail("ACTIVE_V2_HASH_PRESENT_PARENT")

cp_schemas = parse_tree(
    raw["cp_schemas"]
)

pa_schemas = parse_tree(
    raw["pa_schemas"]
)

if cp_schemas != pa_schemas:
    fail("SCHEMAS_TREE_IDENTITY")

if cp_schemas.get(
    "protocol_specification.v2.schema.json",
    {}
).get("oid") != \
   m["checkpoint_blobs"]["schema_v2"]:
    fail("SCHEMA_V2_PATH_BINDING")

if cp_schemas.get(
    "protocol_specification.schema.json",
    {}
).get("oid") != \
   m["checkpoint_blobs"]["schema_v1"]:
    fail("SCHEMA_V1_PATH_BINDING")

cp_protocol = parse_tree(
    raw["cp_protocol_specifications"]
)

pa_protocol = parse_tree(
    raw["pa_protocol_specifications"]
)

if cp_protocol != pa_protocol:
    fail("PROTOCOL_TREE_IDENTITY")

if cp_protocol.get(
    "zlib.json",
    {}
).get("oid") != \
   m["checkpoint_blobs"]["zlib"]:
    fail("ZLIB_PATH_BINDING")

if cp_protocol.get(
    "libpcap.json",
    {}
).get("oid") != \
   m["checkpoint_blobs"]["libpcap"]:
    fail("LIBPCAP_PATH_BINDING")

if "curl.json" in cp_protocol:
    fail("CURL_JSON_PRESENT_CHECKPOINT")

if "curl.json" in pa_protocol:
    fail("CURL_JSON_PRESENT_PARENT")

cp_doc = parse_tree(
    raw["cp_documentation"]
)

pa_doc = parse_tree(
    raw["pa_documentation"]
)

if cp_doc != pa_doc:
    fail("DOCUMENTATION_TREE_IDENTITY")

cp_decisions = parse_tree(
    raw["cp_decisions"]
)

pa_decisions = parse_tree(
    raw["pa_decisions"]
)

if cp_decisions != pa_decisions:
    fail("DECISIONS_TREE_IDENTITY")

if cp_decisions.get(
    "0019-canonical-library-protocol-specification-path-convention.md",
    {}
).get("oid") != \
   m["checkpoint_blobs"]["decision_0019"]:
    fail("DECISION_0019_PATH_BINDING")

if cp_config.get(
    "protocol_content_hash_canonicalization.v1.json",
    {}
).get("oid") != \
   m["checkpoint_blobs"]["hash_v1"]:
    fail("V1_HASH_PATH_BINDING")

cp_evidence = parse_tree(
    raw["cp_evidence"]
)

pa_evidence = parse_tree(
    raw["pa_evidence"]
)

if not same_except(
    cp_evidence,
    pa_evidence,
    {"annotation_preparation"}
):
    fail("EVIDENCE_CHANGED_OUTSIDE_ANNOTATION_PREPARATION")

cp_annotation = parse_tree(
    raw["cp_annotation_preparation"]
)

pa_annotation = parse_tree(
    raw["pa_annotation_preparation"]
)

target = "protocol_specification_schema_successor_v2"

if not same_except(
    cp_annotation,
    pa_annotation,
    {target}
):
    fail("ANNOTATION_CHANGED_OUTSIDE_SCHEMA_SUCCESSOR")

cp_successor = parse_tree(
    raw["cp_schema_successor_root"]
)

pa_successor = parse_tree(
    raw["pa_schema_successor_root"]
)

if "schema_v2_activation_governance_package_v1" in pa_successor:
    fail("PACKAGE_PRESENT_IN_PARENT")

if cp_successor.get(
    "schema_v2_activation_governance_package_v1",
    {}
).get("oid") != m["package_tree"]:
    fail("PACKAGE_SUBTREE_BINDING")

if not same_except(
    cp_successor,
    pa_successor,
    {"schema_v2_activation_governance_package_v1"}
):
    fail("SUCCESSOR_ROOT_CHANGED_OUTSIDE_PACKAGE")

for key in blob_keys:
    if m["checkpoint_blobs"][key] != \
       m["parent_blobs"][key]:
        fail(
            "CHECKPOINT_PARENT_BLOB_NONIDENTITY|"
            + key
        )

if m[
    "active_v2_hash_contract_absent_at_checkpoint_and_parent"
] is not True:
    fail("ACTIVE_V2_HASH_ABSENCE_CLAIM")

if m[
    "curl_json_absent_at_checkpoint_and_parent"
] is not True:
    fail("CURL_ABSENCE_CLAIM")

for key, value in m["claims"].items():
    if value is not True:
        fail(
            "CLAIM|" + key
        )

print("ACTIVATION_PACKAGE_POSTCOMMIT_CHECKPOINT_COMMIT_OBJECT=PASS")
print("ACTIVATION_PACKAGE_POSTCOMMIT_PARENT_COMMIT_OBJECT=PASS")
print("ACTIVATION_PACKAGE_POSTCOMMIT_ROOT_PATH_CHAIN=PASS")
print("ACTIVATION_PACKAGE_POSTCOMMIT_CONFIG_TREE_IDENTITY=PASS")
print("ACTIVATION_PACKAGE_POSTCOMMIT_SCHEMA_V2_PATH_BLOB_IDENTITY=PASS")
print("ACTIVATION_PACKAGE_POSTCOMMIT_V1_HASH_PATH_BLOB_IDENTITY=PASS")
print("ACTIVATION_PACKAGE_POSTCOMMIT_DECISION_0019_PATH_BLOB_IDENTITY=PASS")
print("ACTIVATION_PACKAGE_POSTCOMMIT_ZLIB_PATH_BLOB_IDENTITY=PASS")
print("ACTIVATION_PACKAGE_POSTCOMMIT_LIBPCAP_PATH_BLOB_IDENTITY=PASS")
print("ACTIVATION_PACKAGE_POSTCOMMIT_ACTIVE_V2_HASH_ABSENT=PASS")
print("ACTIVATION_PACKAGE_POSTCOMMIT_CURL_JSON_ABSENT=PASS")
print("ACTIVATION_PACKAGE_POSTCOMMIT_CHANGED_PATH_SCOPE=PACKAGE_ONLY")
print("PORTABLE_ACTIVATION_GOVERNANCE_PACKAGE_POSTCOMMIT_NONINTERFERENCE_PROOF=PASS")
