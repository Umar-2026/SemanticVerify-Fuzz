#!/usr/bin/env python3

import hashlib
import json
from pathlib import Path

def fail(x):
    print("FAIL|" + x)
    raise SystemExit(1)

def oid(kind, raw):
    header = f"{kind} {len(raw)}\0".encode()
    return hashlib.sha1(header + raw).hexdigest()

def tree_entries(raw):
    out = {}
    i = 0

    while i < len(raw):
        sp = raw.index(b" ", i)
        mode = raw[i:sp].decode()
        nul = raw.index(b"\0", sp + 1)
        name = raw[sp + 1:nul].decode()
        obj = raw[nul + 1:nul + 21].hex()
        out[name] = (mode, obj)
        i = nul + 21

    return out

here = Path(__file__).resolve().parent

m = json.loads(
    (here / "06_git_object_manifest.v1.json")
    .read_text(encoding="utf-8")
)

commit = (here / "01_checkpoint_commit.raw").read_bytes()
root = (here / "02_checkpoint_root_tree.raw").read_bytes()
config = (here / "03_config_tree.raw").read_bytes()
schemas = (here / "04_schemas_tree.raw").read_bytes()
v2 = (here / "05_schema_v2_blob.raw").read_bytes()

if oid("commit", commit) != m["checkpoint_commit"]:
    fail("COMMIT_OBJECT")

if oid("tree", root) != m["checkpoint_root_tree"]:
    fail("ROOT_TREE_OBJECT")

if oid("tree", config) != m["config_tree"]:
    fail("CONFIG_TREE_OBJECT")

if oid("tree", schemas) != m["schemas_tree"]:
    fail("SCHEMAS_TREE_OBJECT")

if oid("blob", v2) != m["schema_v2_blob"]:
    fail("V2_BLOB_OBJECT")

if commit.decode().splitlines()[0] != \
   "tree " + m["checkpoint_root_tree"]:
    fail("COMMIT_ROOT_BINDING")

r = tree_entries(root)
c = tree_entries(config)
s = tree_entries(schemas)

if r.get("config", ("", ""))[1] != m["config_tree"]:
    fail("ROOT_CONFIG_BINDING")

if c.get("schemas", ("", ""))[1] != m["schemas_tree"]:
    fail("CONFIG_SCHEMAS_BINDING")

if s.get(
    "protocol_specification.v2.schema.json",
    ("", "")
)[1] != m["schema_v2_blob"]:
    fail("SCHEMAS_V2_BINDING")

if hashlib.sha256(v2).hexdigest() != m["schema_v2_sha256"]:
    fail("V2_SHA256")

if len(v2) != m["schema_v2_size_bytes"]:
    fail("V2_SIZE")

print("GIT_CHECKPOINT_COMMIT_OBJECT_ID=PASS")
print("GIT_CHECKPOINT_ROOT_TREE_BINDING=PASS")
print("GIT_ROOT_TO_CONFIG_TREE=PASS")
print("GIT_CONFIG_TO_SCHEMAS_TREE=PASS")
print("GIT_SCHEMAS_TO_SCHEMA_V2_BLOB=PASS")
print("EXACT_SCHEMA_V2_GIT_BLOB_OBJECT_ID=PASS")
print("EXACT_SCHEMA_V2_SHA256=PASS")
print("EXACT_SCHEMA_V2_SIZE=PASS")
print("MINIMAL_PORTABLE_SCHEMA_V2_GIT_OBJECT_PROOF=PASS")
