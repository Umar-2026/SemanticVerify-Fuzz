#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

here = Path(__file__).resolve().parent

def die(x):
    print("FAIL|" + x)
    raise SystemExit(1)

def oid(kind, data):
    hdr = f"{kind} {len(data)}\0".encode()
    return hashlib.sha1(hdr + data).hexdigest()

def parse_tree(data):
    pos = 0
    out = {}
    while pos < len(data):
        sp = data.index(b" ", pos)
        mode = data[pos:sp].decode()
        nul = data.index(b"\0", sp + 1)
        name = data[sp+1:nul].decode("utf-8", "surrogateescape")
        raw_oid = data[nul+1:nul+21]
        if len(raw_oid) != 20:
            die("TRUNCATED_TREE_ENTRY")
        out[name] = {
            "mode": mode,
            "oid": raw_oid.hex()
        }
        pos = nul + 21
    return out

m = json.loads(
    (here / "06_git_object_proof_manifest.v1.json")
    .read_text(encoding="utf-8")
)

commit = (here / "01_checkpoint_commit.raw").read_bytes()
root = (here / "02_root_tree.raw").read_bytes()
config = (here / "03_config_tree.raw").read_bytes()
annotation = (here / "04_annotation_tree.raw").read_bytes()
blob = (here / "05_v3_blob.raw").read_bytes()

if oid("commit", commit) != m["checkpoint_commit"]:
    die("COMMIT_OBJECT_ID")

if oid("tree", root) != m["root_tree"]:
    die("ROOT_TREE_OBJECT_ID")

commit_text = commit.decode("utf-8", "replace")
first = commit_text.splitlines()[0]

if first != "tree " + m["root_tree"]:
    die("COMMIT_ROOT_TREE_BINDING")

root_entries = parse_tree(root)
config_entries = parse_tree(config)
annotation_entries = parse_tree(annotation)

p1, p2, p3 = m["path_chain"]

if root_entries.get("config", {}).get("oid") != p1["expected_object"]:
    die("ROOT_TO_CONFIG")

if oid("tree", config) != p1["expected_object"]:
    die("CONFIG_TREE_OBJECT_ID")

if config_entries.get("annotation", {}).get("oid") != p2["expected_object"]:
    die("CONFIG_TO_ANNOTATION")

if oid("tree", annotation) != p2["expected_object"]:
    die("ANNOTATION_TREE_OBJECT_ID")

target = "curl_canonical_representation_mapping_contract.v3.json"

if annotation_entries.get(target, {}).get("oid") != p3["expected_object"]:
    die("ANNOTATION_TO_V3_BLOB")

if oid("blob", blob) != m["target_blob"]:
    die("V3_BLOB_OBJECT_ID")

if hashlib.sha256(blob).hexdigest() != m["target_sha256"]:
    die("V3_BLOB_SHA256")

if len(blob) != m["target_size_bytes"]:
    die("V3_BLOB_SIZE")

print("GIT_CHECKPOINT_COMMIT_OBJECT_ID=PASS")
print("GIT_CHECKPOINT_ROOT_TREE_BINDING=PASS")
print("GIT_ROOT_TO_CONFIG_TREE=PASS")
print("GIT_CONFIG_TO_ANNOTATION_TREE=PASS")
print("GIT_ANNOTATION_TO_V3_BLOB=PASS")
print("EXACT_V3_GIT_BLOB_OBJECT_ID=PASS")
print("EXACT_V3_SHA256=PASS")
print("EXACT_V3_SIZE=PASS")
print("MINIMAL_PORTABLE_GIT_OBJECT_PROOF=PASS")
