#!/usr/bin/env python3

import hashlib
import json
import subprocess
import tarfile
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent

MANIFEST = HERE / "01_author_checkpoint_git_witness_manifest.v1.json"
ARCHIVE = HERE / "02_author_checkpoint_minimal_git_witness.v1.tar.gz"

AUTHOR_COMMIT = "06a626c90bd18b6645a66117c5562c200734ccc1"
AUTHOR_TREE = "f86c25370a7b74b493cf22491e925b420ae3d303"

DRAFT_PATH = "config/annotation/curl_technical_protocol_working_draft.v1.json"
DRAFT_SHA = "80498e0c4e021700e2a2c09654a852e67b16df86d61fbb28857d14a12fed44c6"

D27_PATH = (
    "documentation/decisions/"
    "0027-curl-technical-protocol-working-draft-v1-author-checkpoint.md"
)
D27_SHA = "2488407a4e4a5e6f0c6881e446bf9a5f9627bf3fe0187b5417c9885739adc6e6"


def fail(msg):
    print("FAIL|" + msg)
    raise SystemExit(1)


def sha_bytes(data):
    return hashlib.sha256(data).hexdigest()


manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

if sha_bytes(ARCHIVE.read_bytes()) != manifest["archive_sha256"]:
    fail("ARCHIVE_SHA256")

with tempfile.TemporaryDirectory(prefix="svf-curl-tech-witness-") as td:
    td = Path(td)

    with tarfile.open(ARCHIVE, "r:gz") as tf:
        tf.extractall(td)

    gitdir = td / "author-witness.git"

    def git(*args, text=True):
        return subprocess.check_output(
            ["git", "--git-dir", str(gitdir), *args],
            text=text,
        )

    if git("cat-file", "-t", AUTHOR_COMMIT).strip() != "commit":
        fail("AUTHOR_COMMIT_TYPE")

    if git("rev-parse", AUTHOR_COMMIT + "^{tree}").strip() != AUTHOR_TREE:
        fail("AUTHOR_TREE")

    draft_blob = git(
        "rev-parse",
        AUTHOR_COMMIT + ":" + DRAFT_PATH
    ).strip()

    expected_draft_blob = (
        manifest["target_paths"][DRAFT_PATH]["blob"]
    )

    if draft_blob != expected_draft_blob:
        fail("DRAFT_BLOB")

    draft_bytes = git(
        "cat-file",
        "blob",
        draft_blob,
        text=False
    )

    if sha_bytes(draft_bytes) != DRAFT_SHA:
        fail("DRAFT_SHA256")

    d27_blob = git(
        "rev-parse",
        AUTHOR_COMMIT + ":" + D27_PATH
    ).strip()

    expected_d27_blob = (
        manifest["target_paths"][D27_PATH]["blob"]
    )

    if d27_blob != expected_d27_blob:
        fail("D27_BLOB")

    d27_bytes = git(
        "cat-file",
        "blob",
        d27_blob,
        text=False
    )

    if sha_bytes(d27_bytes) != D27_SHA:
        fail("D27_SHA256")

    object_files = [
        p
        for p in (gitdir / "objects").glob("*/*")
        if p.parent.name not in {"info", "pack"}
    ]

    oids = [
        p.parent.name + p.name
        for p in object_files
    ]

    counts = {"commit": 0, "tree": 0, "blob": 0}

    blob_oids = set()

    for oid in oids:
        typ = git("cat-file", "-t", oid).strip()

        if typ not in counts:
            fail("UNEXPECTED_OBJECT_TYPE|" + typ)

        counts[typ] += 1

        if typ == "blob":
            blob_oids.add(oid)

    if len(oids) != 8:
        fail("OBJECT_COUNT")

    if counts != {"commit": 1, "tree": 5, "blob": 2}:
        fail("OBJECT_TYPE_COUNTS|" + repr(counts))

    if blob_oids != {draft_blob, d27_blob}:
        fail("UNRELATED_BLOB_PRESENT")

    parent_line = git(
        "cat-file",
        "commit",
        AUTHOR_COMMIT
    )

    parents = [
        line.split(" ", 1)[1]
        for line in parent_line.splitlines()
        if line.startswith("parent ")
    ]

    for parent in parents:
        cp = subprocess.run(
            [
                "git",
                "--git-dir",
                str(gitdir),
                "cat-file",
                "-e",
                parent,
            ]
        )

        if cp.returncode == 0:
            fail("PARENT_COMMIT_OBJECT_INCLUDED|" + parent)

print("AUTHOR_WITNESS_ARCHIVE_SHA256=PASS")
print("AUTHOR_COMMIT_OBJECT=PASS")
print("AUTHOR_COMMIT_TREE=PASS")
print("AUTHOR_COMMIT_TREE_PATH_DRAFT_BLOB_SHA_CHAIN=PASS")
print("AUTHOR_COMMIT_TREE_PATH_D27_BLOB_SHA_CHAIN=PASS")
print("AUTHOR_WITNESS_EXACT_OBJECT_COUNT=8")
print("AUTHOR_WITNESS_COMMIT_COUNT=1")
print("AUTHOR_WITNESS_TREE_COUNT=5")
print("AUTHOR_WITNESS_BLOB_COUNT=2")
print("ONLY_DRAFT_AND_D27_FILE_BLOBS_PRESENT=YES")
print("PARENT_COMMIT_OBJECTS_PRESENT=NO")
print("CURL_TECHNICAL_V1_AUTHOR_GIT_WITNESS_VERIFICATION=PASS")
