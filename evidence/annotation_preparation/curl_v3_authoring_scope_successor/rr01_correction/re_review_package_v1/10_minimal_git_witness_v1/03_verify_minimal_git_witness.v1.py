#!/usr/bin/env python3

import hashlib
import json
import shutil
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent

MANIFEST = ROOT / "01_minimal_git_witness_manifest.v1.json"
ARCHIVE = ROOT / "02_curl_v3_rr01_minimal_git_witness.v1.tar.gz"

V3_COMMIT = "7de6fc01797ae68cbd64406b850a3198f71cc702"
V3_TREE = "c5f96b844e5803cccd04c9f64a55754dc6c77e20"
V3_PATH = "config/annotation/curl_v3_authoring_scope.v3.json"
V3_BLOB = "931c24cc46c99f23ee352455d3e8c93e57e63401"
V3_SHA = "ede7e1422b9553f73377432474deb282852b619a5b004cd7c4d00033c0a37abb"

D24_COMMIT = "36400fa2028df6ccaf176780ba8ff21017a68262"
D24_TREE = "d7afbc0a4c159530f5687c93dca2bad823e55f77"
D24_PATH = (
    "documentation/decisions/"
    "0024-curl-v3-rr01-binding-and-handoff-correction.md"
)
D24_BLOB = "ca72e87d5668c649eb64db8fc04f457eeebc5d0c"
D24_SHA = "df22dc70c572407c1968859f6fd86a20d847062b2130a08484670c06a340915b"

V3_PARENT = "f01c66ca65e08a20114525739a5ed777cb428742"
D24_PARENT = "713587c654f9c24f8fd3e7a3b3ad3638ec81a6fe"

ALLOWED_BLOBS = sorted([V3_BLOB, D24_BLOB])


def fail(msg):
    print("FAIL|" + msg)
    raise SystemExit(1)


def run(gitdir, *args, check=True):
    cp = subprocess.run(
        ["git", "--git-dir=" + str(gitdir), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    if check and cp.returncode != 0:
        fail(
            "GIT_COMMAND|"
            + " ".join(args)
            + "|"
            + cp.stderr.decode(errors="replace").strip()
        )

    return cp


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

actual_archive_sha = sha256_bytes(ARCHIVE.read_bytes())

if actual_archive_sha != manifest["archive"]["sha256"]:
    fail("ARCHIVE_SHA256_MISMATCH")

if ARCHIVE.stat().st_size != manifest["archive"]["size_bytes"]:
    fail("ARCHIVE_SIZE_MISMATCH")

with tempfile.TemporaryDirectory(
    prefix="svf-curl-v3-witness-verify-"
) as td:
    td = Path(td)

    with tarfile.open(ARCHIVE, "r:gz") as tf:
        members = tf.getmembers()

        for m in members:
            target = (td / m.name).resolve()

            if not str(target).startswith(str(td.resolve()) + "/"):
                fail("UNSAFE_ARCHIVE_PATH|" + m.name)

        tf.extractall(td)

    gitdir = td / "curl-v3-rr01-minimal.git"

    if not gitdir.is_dir():
        fail("BARE_GIT_DIRECTORY_MISSING")

    cp = run(
        gitdir,
        "cat-file",
        "--batch-all-objects",
        "--batch-check=%(objectname)|%(objecttype)|%(objectsize)",
    )

    rows = sorted(
        x.strip()
        for x in cp.stdout.decode().splitlines()
        if x.strip()
    )

    if len(rows) != 10:
        fail("OBJECT_COUNT|" + str(len(rows)))

    commits = []
    trees = []
    blobs = []

    for row in rows:
        oid, typ, size = row.split("|")

        if typ == "commit":
            commits.append(oid)
        elif typ == "tree":
            trees.append(oid)
        elif typ == "blob":
            blobs.append(oid)
        else:
            fail("UNEXPECTED_OBJECT_TYPE|" + typ)

    if len(commits) != 2:
        fail("COMMIT_COUNT|" + str(len(commits)))

    if len(trees) != 6:
        fail("TREE_COUNT|" + str(len(trees)))

    if sorted(blobs) != ALLOWED_BLOBS:
        fail("BLOB_INVENTORY|" + repr(sorted(blobs)))

    if run(
        gitdir,
        "cat-file",
        "-e",
        V3_PARENT + "^{commit}",
        check=False,
    ).returncode == 0:
        fail("V3_PARENT_OBJECT_PRESENT")

    if run(
        gitdir,
        "cat-file",
        "-e",
        D24_PARENT + "^{commit}",
        check=False,
    ).returncode == 0:
        fail("D24_PARENT_OBJECT_PRESENT")

    v3_tree = run(
        gitdir,
        "rev-parse",
        V3_COMMIT + "^{tree}",
    ).stdout.decode().strip()

    if v3_tree != V3_TREE:
        fail("V3_TREE_MISMATCH")

    v3_blob = run(
        gitdir,
        "rev-parse",
        V3_COMMIT + ":" + V3_PATH,
    ).stdout.decode().strip()

    if v3_blob != V3_BLOB:
        fail("V3_BLOB_MISMATCH")

    v3_data = run(
        gitdir,
        "cat-file",
        "blob",
        V3_BLOB,
    ).stdout

    if sha256_bytes(v3_data) != V3_SHA:
        fail("V3_CONTENT_SHA256_MISMATCH")

    d24_tree = run(
        gitdir,
        "rev-parse",
        D24_COMMIT + "^{tree}",
    ).stdout.decode().strip()

    if d24_tree != D24_TREE:
        fail("D24_TREE_MISMATCH")

    d24_blob = run(
        gitdir,
        "rev-parse",
        D24_COMMIT + ":" + D24_PATH,
    ).stdout.decode().strip()

    if d24_blob != D24_BLOB:
        fail("D24_BLOB_MISMATCH")

    d24_data = run(
        gitdir,
        "cat-file",
        "blob",
        D24_BLOB,
    ).stdout

    if sha256_bytes(d24_data) != D24_SHA:
        fail("D24_CONTENT_SHA256_MISMATCH")

print("MINIMAL_GIT_WITNESS_ARCHIVE_SHA256=PASS")
print("EXACT_OBJECT_COUNT=10")
print("COMMIT_OBJECT_COUNT=2")
print("TREE_OBJECT_COUNT=6")
print("BLOB_OBJECT_COUNT=2")
print("ONLY_ALLOWED_FILE_BLOBS_PRESENT=YES")
print("PARENT_HISTORY_OBJECTS_PRESENT=NO")
print("V3_COMMIT_TREE_PATH_BLOB_SHA_CHAIN=PASS")
print("DECISION_0024_COMMIT_TREE_PATH_BLOB_SHA_CHAIN=PASS")
print("QUARANTINE_SAFE_MINIMAL_GIT_WITNESS_VERIFICATION=PASS")
