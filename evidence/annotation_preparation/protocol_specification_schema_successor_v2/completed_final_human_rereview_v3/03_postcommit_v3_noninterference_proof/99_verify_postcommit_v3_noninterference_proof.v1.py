#!/usr/bin/env python3

import hashlib
import json
from pathlib import Path

def fail(x):
    print("FAIL|" + x)
    raise SystemExit(1)

def git_oid(kind, raw):
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

        oid = raw[
            nul + 1:
            nul + 21
        ].hex()

        out[name] = {
            "mode": mode,
            "oid": oid,
        }

        i = nul + 21

    return out

def same_except(a, b, ignored):
    aa = {
        k: v
        for k, v in a.items()
        if k not in ignored
    }

    bb = {
        k: v
        for k, v in b.items()
        if k not in ignored
    }

    return aa == bb

here = Path(__file__).resolve().parent

m = json.loads(
    (
        here /
        "00_postcommit_proof_manifest.v1.json"
    ).read_text(
        encoding="utf-8"
    )
)

CHECKPOINT = m["checkpoint_commit"]
PARENT = m["parent_commit"]

cp_commit = (
    here /
    "01_checkpoint_commit.raw"
).read_bytes()

pa_commit = (
    here /
    "02_parent_commit.raw"
).read_bytes()

if git_oid(
    "commit",
    cp_commit
) != CHECKPOINT:
    fail("CHECKPOINT_COMMIT_OID")

if git_oid(
    "commit",
    pa_commit
) != PARENT:
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
    fail(
        "CHECKPOINT_COMMIT_TREE_BINDING"
    )

parents = [
    line.split(" ", 1)[1]
    for line in cp_lines
    if line.startswith("parent ")
]

if parents != [PARENT]:
    fail(
        "CHECKPOINT_PARENT_BINDING"
    )

if pa_lines[0] != \
   "tree " + m["parent_root_tree"]:
    fail(
        "PARENT_COMMIT_TREE_BINDING"
    )

files = {
    "cp_root":
        "03_checkpoint_root_tree.raw",

    "pa_root":
        "04_parent_root_tree.raw",

    "cp_config":
        "05_checkpoint_config_tree.raw",

    "pa_config":
        "06_parent_config_tree.raw",

    "cp_schemas":
        "07_checkpoint_schemas_tree.raw",

    "pa_schemas":
        "08_parent_schemas_tree.raw",

    "cp_protocol":
        "09_checkpoint_protocol_specifications_tree.raw",

    "pa_protocol":
        "10_parent_protocol_specifications_tree.raw",

    "cp_evidence":
        "11_checkpoint_evidence_tree.raw",

    "pa_evidence":
        "12_parent_evidence_tree.raw",

    "cp_annotation":
        "13_checkpoint_annotation_preparation_tree.raw",

    "pa_annotation":
        "14_parent_annotation_preparation_tree.raw",

    "cp_successor":
        "15_checkpoint_schema_successor_root_tree.raw",

    "pa_successor":
        "16_parent_schema_successor_root_tree.raw",

    "cp_package":
        "17_checkpoint_review_package_v3_tree.raw",

    "cp_v2":
        "18_checkpoint_schema_v2_blob.raw",

    "pa_v2":
        "19_parent_schema_v2_blob.raw",

    "cp_zlib":
        "20_checkpoint_zlib_blob.raw",

    "pa_zlib":
        "21_parent_zlib_blob.raw",

    "cp_pcap":
        "22_checkpoint_libpcap_blob.raw",

    "pa_pcap":
        "23_parent_libpcap_blob.raw",

    "changed":
        "24_changed_paths.v1.txt",
}

raw = {}

for key, filename in files.items():
    if key == "changed":
        continue

    raw[key] = (
        here /
        filename
    ).read_bytes()

if git_oid(
    "tree",
    raw["cp_root"]
) != m["checkpoint_root_tree"]:
    fail(
        "CHECKPOINT_ROOT_TREE_OID"
    )

if git_oid(
    "tree",
    raw["pa_root"]
) != m["parent_root_tree"]:
    fail(
        "PARENT_ROOT_TREE_OID"
    )

tree_specs = (
    (
        "cp_config",
        "checkpoint_trees",
        "config"
    ),
    (
        "pa_config",
        "parent_trees",
        "config"
    ),
    (
        "cp_schemas",
        "checkpoint_trees",
        "schemas"
    ),
    (
        "pa_schemas",
        "parent_trees",
        "schemas"
    ),
    (
        "cp_protocol",
        "checkpoint_trees",
        "protocol_specifications"
    ),
    (
        "pa_protocol",
        "parent_trees",
        "protocol_specifications"
    ),
    (
        "cp_evidence",
        "checkpoint_trees",
        "evidence"
    ),
    (
        "pa_evidence",
        "parent_trees",
        "evidence"
    ),
    (
        "cp_annotation",
        "checkpoint_trees",
        "annotation_preparation"
    ),
    (
        "pa_annotation",
        "parent_trees",
        "annotation_preparation"
    ),
    (
        "cp_successor",
        "checkpoint_trees",
        "schema_successor_root"
    ),
    (
        "pa_successor",
        "parent_trees",
        "schema_successor_root"
    ),
)

for key, side, pathkey in tree_specs:
    if git_oid(
        "tree",
        raw[key]
    ) != m[side][pathkey]:
        fail(
            "TREE_OID|" + key
        )

if git_oid(
    "tree",
    raw["cp_package"]
) != m["review_package_v3_tree"]:
    fail(
        "PACKAGE_V3_TREE_OID"
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
    fail(
        "CHECKPOINT_ROOT_CONFIG_BINDING"
    )

if pa_root.get(
    "config",
    {}
).get("oid") != \
   m["parent_trees"]["config"]:
    fail(
        "PARENT_ROOT_CONFIG_BINDING"
    )

if cp_root.get(
    "evidence",
    {}
).get("oid") != \
   m["checkpoint_trees"]["evidence"]:
    fail(
        "CHECKPOINT_ROOT_EVIDENCE_BINDING"
    )

if pa_root.get(
    "evidence",
    {}
).get("oid") != \
   m["parent_trees"]["evidence"]:
    fail(
        "PARENT_ROOT_EVIDENCE_BINDING"
    )

if not same_except(
    cp_root,
    pa_root,
    {"evidence"}
):
    fail(
        "ROOT_CHANGED_OUTSIDE_EVIDENCE"
    )

cp_config = parse_tree(
    raw["cp_config"]
)

pa_config = parse_tree(
    raw["pa_config"]
)

if m["checkpoint_trees"]["config"] != \
   m["parent_trees"]["config"]:
    fail(
        "CONFIG_TREE_OID_IDENTITY"
    )

if cp_config != pa_config:
    fail(
        "CONFIG_TREE_CONTENT_IDENTITY"
    )

if cp_config.get(
    "schemas",
    {}
).get("oid") != \
   m["checkpoint_trees"]["schemas"]:
    fail(
        "CONFIG_SCHEMAS_BINDING"
    )

if cp_config.get(
    "protocol_specifications",
    {}
).get("oid") != \
   m["checkpoint_trees"]["protocol_specifications"]:
    fail(
        "CONFIG_PROTOCOL_BINDING"
    )

cp_schemas = parse_tree(
    raw["cp_schemas"]
)

pa_schemas = parse_tree(
    raw["pa_schemas"]
)

if cp_schemas != pa_schemas:
    fail(
        "SCHEMAS_TREE_CONTENT_IDENTITY"
    )

cp_protocol = parse_tree(
    raw["cp_protocol"]
)

pa_protocol = parse_tree(
    raw["pa_protocol"]
)

if cp_protocol != pa_protocol:
    fail(
        "PROTOCOL_TREE_CONTENT_IDENTITY"
    )

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
    fail(
        "EVIDENCE_CHANGED_OUTSIDE_ANNOTATION_PREPARATION"
    )

if cp_evidence.get(
    "annotation_preparation",
    {}
).get("oid") != \
   m["checkpoint_trees"]["annotation_preparation"]:
    fail(
        "CHECKPOINT_ANNOTATION_BINDING"
    )

if pa_evidence.get(
    "annotation_preparation",
    {}
).get("oid") != \
   m["parent_trees"]["annotation_preparation"]:
    fail(
        "PARENT_ANNOTATION_BINDING"
    )

cp_annotation = parse_tree(
    raw["cp_annotation"]
)

pa_annotation = parse_tree(
    raw["pa_annotation"]
)

target = (
    "protocol_specification_"
    "schema_successor_v2"
)

if not same_except(
    cp_annotation,
    pa_annotation,
    {target}
):
    fail(
        "ANNOTATION_CHANGED_OUTSIDE_SCHEMA_SUCCESSOR"
    )

if cp_annotation.get(
    target,
    {}
).get("oid") != \
   m["checkpoint_trees"]["schema_successor_root"]:
    fail(
        "CHECKPOINT_SCHEMA_SUCCESSOR_BINDING"
    )

if pa_annotation.get(
    target,
    {}
).get("oid") != \
   m["parent_trees"]["schema_successor_root"]:
    fail(
        "PARENT_SCHEMA_SUCCESSOR_BINDING"
    )

cp_successor = parse_tree(
    raw["cp_successor"]
)

pa_successor = parse_tree(
    raw["pa_successor"]
)

if "review_package_v3" in pa_successor:
    fail(
        "PACKAGE_V3_PRESENT_IN_PARENT"
    )

if cp_successor.get(
    "review_package_v3",
    {}
).get("oid") != \
   m["review_package_v3_tree"]:
    fail(
        "PACKAGE_V3_SUBTREE_BINDING"
    )

if not same_except(
    cp_successor,
    pa_successor,
    {"review_package_v3"}
):
    fail(
        "SCHEMA_SUCCESSOR_ROOT_CHANGED_OUTSIDE_PACKAGE_V3"
    )

blob_specs = (
    (
        "cp_v2",
        m["checkpoint_blobs"]["schema_v2"],
        m["expected_file_sha256"]["v2_sha256"],
    ),
    (
        "pa_v2",
        m["parent_blobs"]["schema_v2"],
        m["expected_file_sha256"]["v2_sha256"],
    ),
    (
        "cp_zlib",
        m["checkpoint_blobs"]["zlib"],
        m["expected_file_sha256"]["zlib_sha256"],
    ),
    (
        "pa_zlib",
        m["parent_blobs"]["zlib"],
        m["expected_file_sha256"]["zlib_sha256"],
    ),
    (
        "cp_pcap",
        m["checkpoint_blobs"]["libpcap"],
        m["expected_file_sha256"]["libpcap_sha256"],
    ),
    (
        "pa_pcap",
        m["parent_blobs"]["libpcap"],
        m["expected_file_sha256"]["libpcap_sha256"],
    ),
)

for key, expected_oid, expected_sha in blob_specs:
    if git_oid(
        "blob",
        raw[key]
    ) != expected_oid:
        fail(
            "BLOB_OID|" + key
        )

    if hashlib.sha256(
        raw[key]
    ).hexdigest() != expected_sha:
        fail(
            "BLOB_SHA|" + key
        )

if m["checkpoint_blobs"]["schema_v2"] != \
   m["parent_blobs"]["schema_v2"]:
    fail(
        "SCHEMA_V2_BLOB_IDENTITY"
    )

if m["checkpoint_blobs"]["zlib"] != \
   m["parent_blobs"]["zlib"]:
    fail(
        "ZLIB_BLOB_IDENTITY"
    )

if m["checkpoint_blobs"]["libpcap"] != \
   m["parent_blobs"]["libpcap"]:
    fail(
        "LIBPCAP_BLOB_IDENTITY"
    )

if cp_schemas.get(
    "protocol_specification.v2.schema.json",
    {}
).get("oid") != \
   m["checkpoint_blobs"]["schema_v2"]:
    fail(
        "SCHEMAS_TO_V2_BLOB_BINDING"
    )

if cp_protocol.get(
    "zlib.json",
    {}
).get("oid") != \
   m["checkpoint_blobs"]["zlib"]:
    fail(
        "PROTOCOL_TO_ZLIB_BLOB_BINDING"
    )

if cp_protocol.get(
    "libpcap.json",
    {}
).get("oid") != \
   m["checkpoint_blobs"]["libpcap"]:
    fail(
        "PROTOCOL_TO_LIBPCAP_BLOB_BINDING"
    )

changed = [
    x
    for x in (
        here /
        files["changed"]
    ).read_text(
        encoding="utf-8"
    ).splitlines()
    if x
]

if changed != m["changed_paths"]:
    fail(
        "CHANGED_PATH_LIST"
    )

if len(changed) != \
   m["changed_path_count"]:
    fail(
        "CHANGED_PATH_COUNT"
    )

prefix = (
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2/"
    "review_package_v3/"
)

for path in changed:
    if not path.startswith(prefix):
        fail(
            "OUT_OF_SCOPE_CHANGED_PATH|"
            + path
        )

for key, value in m["claims"].items():
    if value is not True:
        fail(
            "CLAIM|" + key
        )

print("V3_POSTCOMMIT_CHECKPOINT_COMMIT_OBJECT=PASS")
print("V3_POSTCOMMIT_PARENT_COMMIT_OBJECT=PASS")
print("V3_POSTCOMMIT_ROOT_PATH_CHAIN=PASS")
print("V3_POSTCOMMIT_CONFIG_TREE_IDENTITY=PASS")
print("V3_POSTCOMMIT_SCHEMAS_TREE_IDENTITY=PASS")
print("V3_POSTCOMMIT_PROTOCOL_SPECIFICATIONS_TREE_IDENTITY=PASS")
print("V3_POSTCOMMIT_SCHEMA_V2_PATH_BLOB_IDENTITY=PASS")
print("V3_POSTCOMMIT_ZLIB_PATH_BLOB_IDENTITY=PASS")
print("V3_POSTCOMMIT_LIBPCAP_PATH_BLOB_IDENTITY=PASS")
print("V3_POSTCOMMIT_PACKAGE_V3_ONLY_ADDITION=PASS")
print("V3_POSTCOMMIT_CHANGED_PATH_SCOPE=REVIEW_PACKAGE_V3_ONLY")
print("V3_AUTHORING_DID_NOT_MODIFY_SCHEMA_V2=PASS")
print("V3_AUTHORING_DID_NOT_MODIFY_ZLIB=PASS")
print("V3_AUTHORING_DID_NOT_MODIFY_LIBPCAP=PASS")
print("PORTABLE_V3_POSTCOMMIT_NONINTERFERENCE_PROOF=PASS")
