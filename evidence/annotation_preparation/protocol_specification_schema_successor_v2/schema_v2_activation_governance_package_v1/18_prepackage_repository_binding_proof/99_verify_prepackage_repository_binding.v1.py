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

here = Path(__file__).resolve().parent

m = json.loads(
    (
        here /
        "00_prepackage_binding_manifest.v1.json"
    ).read_text(
        encoding="utf-8"
    )
)

commit_raw = (
    here /
    "01_basis_commit.raw"
).read_bytes()

root_raw = (
    here /
    "02_basis_root_tree.raw"
).read_bytes()

if oid(
    "commit",
    commit_raw
) != m["basis_commit"]:
    fail("COMMIT_OID")

if oid(
    "tree",
    root_raw
) != m["basis_root_tree"]:
    fail("ROOT_TREE_OID")

lines = commit_raw.decode(
    "utf-8",
    errors="strict"
).splitlines()

if lines[0] != \
   "tree " + m["basis_root_tree"]:
    fail("COMMIT_ROOT_BINDING")

tree_files = {
    "config":
        "03_config_tree.raw",

    "schemas":
        "04_schemas_tree.raw",

    "protocol_specifications":
        "05_protocol_specifications_tree.raw",

    "annotation":
        "06_annotation_tree.raw",
}

blob_files = {
    "schema_v1":
        "07_schema_v1_blob.raw",

    "schema_v2":
        "08_schema_v2_blob.raw",

    "hash_v1":
        "09_hash_v1_blob.raw",

    "path_map":
        "10_path_map_blob.raw",

    "zlib":
        "11_zlib_blob.raw",

    "libpcap":
        "12_libpcap_blob.raw",
}

trees = {}

for key, filename in tree_files.items():
    raw = (
        here /
        filename
    ).read_bytes()

    if oid(
        "tree",
        raw
    ) != m["tree_oids"][key]:
        fail(
            "TREE_OID|" + key
        )

    trees[key] = parse_tree(raw)

root = parse_tree(root_raw)

if root.get(
    "config",
    {}
).get("oid") != m["tree_oids"]["config"]:
    fail("ROOT_CONFIG_BINDING")

config = trees["config"]

if config.get(
    "schemas",
    {}
).get("oid") != m["tree_oids"]["schemas"]:
    fail("CONFIG_SCHEMAS_BINDING")

if config.get(
    "protocol_specifications",
    {}
).get("oid") != m["tree_oids"]["protocol_specifications"]:
    fail("CONFIG_PROTOCOL_BINDING")

if config.get(
    "annotation",
    {}
).get("oid") != m["tree_oids"]["annotation"]:
    fail("CONFIG_ANNOTATION_BINDING")

blobs = {}

for key, filename in blob_files.items():
    raw = (
        here /
        filename
    ).read_bytes()

    if oid(
        "blob",
        raw
    ) != m["blob_oids"][key]:
        fail(
            "BLOB_OID|" + key
        )

    if hashlib.sha256(
        raw
    ).hexdigest() != \
       m["expected_sha256"][key]:
        fail(
            "BLOB_SHA|" + key
        )

    blobs[key] = raw

schemas = trees["schemas"]

if schemas.get(
    "protocol_specification.schema.json",
    {}
).get("oid") != m["blob_oids"]["schema_v1"]:
    fail("V1_SCHEMA_PATH_BINDING")

if schemas.get(
    "protocol_specification.v2.schema.json",
    {}
).get("oid") != m["blob_oids"]["schema_v2"]:
    fail("V2_SCHEMA_PATH_BINDING")

protocol = trees["protocol_specifications"]

if protocol.get(
    "zlib.json",
    {}
).get("oid") != m["blob_oids"]["zlib"]:
    fail("ZLIB_PATH_BINDING")

if protocol.get(
    "libpcap.json",
    {}
).get("oid") != m["blob_oids"]["libpcap"]:
    fail("LIBPCAP_PATH_BINDING")

if config.get(
    "protocol_content_hash_canonicalization.v1.json",
    {}
).get("oid") != m["blob_oids"]["hash_v1"]:
    fail("V1_HASH_PATH_BINDING")

annotation = trees["annotation"]

if annotation.get(
    "canonical_protocol_specification_paths.v1.json",
    {}
).get("oid") != m["blob_oids"]["path_map"]:
    fail("PATH_MAP_BINDING")

for key, value in m["claims"].items():
    if value is not True:
        fail(
            "CLAIM|" + key
        )

print("PREPACKAGE_BASIS_COMMIT_OBJECT=PASS")
print("PREPACKAGE_ROOT_CONFIG_PATH_CHAIN=PASS")
print("PREPACKAGE_SCHEMA_V1_PATH_BLOB_BINDING=PASS")
print("PREPACKAGE_SCHEMA_V2_PATH_BLOB_BINDING=PASS")
print("PREPACKAGE_V1_HASH_PATH_BLOB_BINDING=PASS")
print("PREPACKAGE_PATH_MAP_PATH_BLOB_BINDING=PASS")
print("PREPACKAGE_ZLIB_PATH_BLOB_BINDING=PASS")
print("PREPACKAGE_LIBPCAP_PATH_BLOB_BINDING=PASS")
print("PORTABLE_ACTIVATION_GOVERNANCE_PREPACKAGE_BINDING_PROOF=PASS")
