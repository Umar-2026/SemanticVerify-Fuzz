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

        nul = raw.index(b"\0", sp + 1)

        name = raw[sp + 1:nul].decode()
        obj = raw[nul + 1:nul + 21].hex()

        out[name] = {
            "mode": mode,
            "oid": obj
        }

        i = nul + 21

    return out

here = Path(__file__).resolve().parent

m = json.loads(
    (
        here /
        "00_prepackage_binding_manifest.v1.json"
    ).read_text(encoding="utf-8")
)

commit_raw = (
    here /
    "01_basis_commit.raw"
).read_bytes()

root_raw = (
    here /
    "02_basis_root_tree.raw"
).read_bytes()

if oid("commit", commit_raw) != m["basis_commit"]:
    fail("COMMIT_OID")

if oid("tree", root_raw) != m["basis_root_tree"]:
    fail("ROOT_TREE_OID")

if commit_raw.decode(
    "utf-8",
    errors="strict"
).splitlines()[0] != \
   "tree " + m["basis_root_tree"]:
    fail("COMMIT_ROOT_BINDING")

tree_names = (
    "config",
    "schemas",
    "protocol_specifications",
    "documentation",
    "decisions",
    "evidence",
    "annotation_preparation",
    "schema_successor_root"
)

trees = {}
counter = 3

for key in tree_names:
    raw = (
        here /
        f"{counter:02d}_{key}_tree.raw"
    ).read_bytes()

    if oid("tree", raw) != m["tree_oids"][key]:
        fail("TREE_OID|" + key)

    trees[key] = parse_tree(raw)
    counter += 1

blob_names = (
    "source_hash",
    "approval",
    "schema_v2",
    "schema_v1",
    "hash_v1",
    "decision_0019",
    "zlib",
    "libpcap"
)

blobs = {}

for key in blob_names:
    raw = (
        here /
        f"{counter:02d}_{key}_blob.raw"
    ).read_bytes()

    if oid("blob", raw) != m["blob_oids"][key]:
        fail("BLOB_OID|" + key)

    if hashlib.sha256(raw).hexdigest() != \
       m["expected_sha256"][key]:
        fail("BLOB_SHA|" + key)

    blobs[key] = raw
    counter += 1

root = parse_tree(root_raw)

if root.get("config", {}).get("oid") != \
   m["tree_oids"]["config"]:
    fail("ROOT_CONFIG")

if root.get("documentation", {}).get("oid") != \
   m["tree_oids"]["documentation"]:
    fail("ROOT_DOCUMENTATION")

config = trees["config"]

if config.get("schemas", {}).get("oid") != \
   m["tree_oids"]["schemas"]:
    fail("CONFIG_SCHEMAS")

if config.get(
    "protocol_specifications",
    {}
).get("oid") != m["tree_oids"]["protocol_specifications"]:
    fail("CONFIG_PROTOCOL")

if "protocol_content_hash_canonicalization.v2.json" in config:
    fail("ACTIVE_V2_HASH_PRESENT")

schemas = trees["schemas"]

if schemas.get(
    "protocol_specification.v2.schema.json",
    {}
).get("oid") != m["blob_oids"]["schema_v2"]:
    fail("SCHEMA_V2_PATH")

if schemas.get(
    "protocol_specification.schema.json",
    {}
).get("oid") != m["blob_oids"]["schema_v1"]:
    fail("SCHEMA_V1_PATH")

protocol = trees["protocol_specifications"]

if protocol.get("zlib.json", {}).get("oid") != \
   m["blob_oids"]["zlib"]:
    fail("ZLIB_PATH")

if protocol.get("libpcap.json", {}).get("oid") != \
   m["blob_oids"]["libpcap"]:
    fail("LIBPCAP_PATH")

if "curl.json" in protocol:
    fail("CURL_JSON_PRESENT")

decisions = trees["decisions"]

if decisions.get(
    "0019-canonical-library-protocol-specification-path-convention.md",
    {}
).get("oid") != m["blob_oids"]["decision_0019"]:
    fail("DEC0019_PATH")

if config.get(
    "protocol_content_hash_canonicalization.v1.json",
    {}
).get("oid") != m["blob_oids"]["hash_v1"]:
    fail("V1_HASH_PATH")

if m["active_v2_hash_absent"] is not True:
    fail("ACTIVE_HASH_CLAIM")

if m["curl_json_absent"] is not True:
    fail("CURL_CLAIM")

if m["finalization_package_absent"] is not True:
    fail("PACKAGE_ABSENCE_CLAIM")

print("HASH_FINALIZATION_PREPACKAGE_COMMIT_OBJECT=PASS")
print("HASH_FINALIZATION_PREPACKAGE_ROOT_PATH_CHAIN=PASS")
print("HASH_FINALIZATION_PREPACKAGE_SCHEMA_V2_PATH_BLOB=PASS")
print("HASH_FINALIZATION_PREPACKAGE_V1_HASH_PATH_BLOB=PASS")
print("HASH_FINALIZATION_PREPACKAGE_ZLIB_LIBPCAP_PATH_BLOB=PASS")
print("HASH_FINALIZATION_PREPACKAGE_ACTIVE_V2_HASH_ABSENT=PASS")
print("HASH_FINALIZATION_PREPACKAGE_CURL_JSON_ABSENT=PASS")
print("PORTABLE_HASH_FINALIZATION_PREPACKAGE_BINDING_PROOF=PASS")
