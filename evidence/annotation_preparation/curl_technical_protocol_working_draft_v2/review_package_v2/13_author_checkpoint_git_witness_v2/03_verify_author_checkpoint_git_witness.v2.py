#!/usr/bin/env python3

import hashlib
import json
import struct
import tarfile
import tempfile
import zlib
from pathlib import Path


def fail(msg):
    print("FAIL|" + msg)
    raise SystemExit(1)


here = Path(__file__).resolve().parent

manifest_path = (
    here / "01_author_checkpoint_git_witness_manifest.v2.json"
)

archive = (
    here / "02_author_checkpoint_minimal_git_witness.v2.tar.gz"
)

record = json.loads(
    manifest_path.read_text(encoding="utf-8")
)

if hashlib.sha256(archive.read_bytes()).hexdigest() != record["archive_sha256"]:
    fail("AUTHOR_WITNESS_ARCHIVE_SHA256")

tmp = Path(tempfile.mkdtemp(prefix="svf-v2-witness-verify-"))

with tarfile.open(archive, "r:gz") as tf:
    for member in tf.getmembers():
        name = Path(member.name)

        if name.is_absolute() or ".." in name.parts:
            fail("UNSAFE_ARCHIVE_MEMBER|" + member.name)

    tf.extractall(tmp)

files = [
    p for p in (tmp / "objects").rglob("*")
    if p.is_file()
]

if len(files) != 8:
    fail("OBJECT_FILE_COUNT|" + str(len(files)))


def load(oid):
    p = tmp / "objects" / oid[:2] / oid[2:]

    if not p.is_file():
        fail("OBJECT_MISSING|" + oid)

    raw = zlib.decompress(p.read_bytes())

    if hashlib.sha1(raw).hexdigest() != oid:
        fail("OBJECT_SHA1|" + oid)

    header, content = raw.split(b"\0", 1)
    typ, size = header.decode("ascii").split(" ", 1)

    if len(content) != int(size):
        fail("OBJECT_SIZE|" + oid)

    return typ, content


def tree_entries(content):
    out = {}
    i = 0

    while i < len(content):
        sp = content.index(b" ", i)
        mode = content[i:sp].decode("ascii")

        nul = content.index(b"\0", sp + 1)
        name = content[sp + 1:nul].decode(
            "utf-8",
            errors="surrogateescape",
        )

        oid = content[nul + 1:nul + 21].hex()

        out[name] = {
            "mode": mode,
            "oid": oid,
        }

        i = nul + 21

    return out


def resolve_path(root_tree_oid, path):
    parts = path.split("/")
    current = root_tree_oid

    for index, part in enumerate(parts):
        typ, content = load(current)

        if typ != "tree":
            fail("NON_TREE_DURING_PATH|" + current)

        entries = tree_entries(content)

        if part not in entries:
            fail("PATH_COMPONENT_MISSING|" + part)

        current = entries[part]["oid"]

        if index < len(parts) - 1:
            next_typ, _ = load(current)

            if next_typ != "tree":
                fail("EXPECTED_TREE|" + part)

    return current


commit_oid = record["author_commit"]
commit_typ, commit_content = load(commit_oid)

if commit_typ != "commit":
    fail("AUTHOR_OBJECT_NOT_COMMIT")

commit_text = commit_content.decode("utf-8", errors="replace")

tree_lines = [
    line[5:]
    for line in commit_text.splitlines()
    if line.startswith("tree ")
]

if tree_lines != [record["author_tree"]]:
    fail("AUTHOR_COMMIT_TREE")

v2_resolved = resolve_path(
    record["author_tree"],
    record["v2_path"],
)

if v2_resolved != record["v2_blob"]:
    fail("V2_PATH_BLOB")

d30_resolved = resolve_path(
    record["author_tree"],
    record["decision_0030_path"],
)

if d30_resolved != record["decision_0030_blob"]:
    fail("D30_PATH_BLOB")

observed_types = {}

for oid in record["object_oids"]:
    typ, _ = load(oid)
    observed_types[oid] = typ

if observed_types != record["object_types"]:
    fail("OBJECT_TYPE_MAP")

type_counts = {}

for typ in observed_types.values():
    type_counts[typ] = type_counts.get(typ, 0) + 1

if type_counts.get("commit", 0) != 1:
    fail("COMMIT_COUNT")

if type_counts.get("tree", 0) != 5:
    fail("TREE_COUNT")

if type_counts.get("blob", 0) != 2:
    fail("BLOB_COUNT")

parent_oids = [
    line[7:]
    for line in commit_text.splitlines()
    if line.startswith("parent ")
]

for parent in parent_oids:
    if parent in record["object_oids"]:
        fail("PARENT_COMMIT_OBJECT_PRESENT|" + parent)

print("AUTHOR_WITNESS_ARCHIVE_SHA256=PASS")
print("AUTHOR_COMMIT_OBJECT=PASS")
print("AUTHOR_COMMIT_TREE=PASS")
print("AUTHOR_COMMIT_TREE_PATH_V2_BLOB_SHA_CHAIN=PASS")
print("AUTHOR_COMMIT_TREE_PATH_D30_BLOB_SHA_CHAIN=PASS")
print("AUTHOR_WITNESS_EXACT_OBJECT_COUNT=8")
print("AUTHOR_WITNESS_COMMIT_COUNT=1")
print("AUTHOR_WITNESS_TREE_COUNT=5")
print("AUTHOR_WITNESS_BLOB_COUNT=2")
print("ONLY_V2_AND_D30_FILE_BLOBS_PRESENT=YES")
print("PARENT_COMMIT_OBJECTS_PRESENT=NO")
print("CURL_TECHNICAL_V2_AUTHOR_GIT_WITNESS_VERIFICATION=PASS")
