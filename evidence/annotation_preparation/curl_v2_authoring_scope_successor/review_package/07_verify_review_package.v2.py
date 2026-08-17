#!/usr/bin/env python3
from pathlib import Path
import hashlib
import subprocess
import sys

AUTHOR_COMMIT = "fae56e4f5196fd0460046723ef9d6a4e26234612"
AUTHOR_TREE = "0cb044dd10d48908895425512f5a2e7c1e8633b9"
TARGET_PATH = "config/annotation/curl_v2_authoring_scope.v2.json"
TARGET_SHA = "f8a5a0d360ad68478649a549744e4d13f22aec7d7edcc60116052906424b52df"
TARGET_BLOB = "5c88a9e00d9ad2e8e4a59aa41488dec016c58cad"

PREDECESSOR_PATH = "config/annotation/curl_v1_authoring_scope.v1.json"
PREDECESSOR_SHA = "d8e020cc14bd6c8ea9d679ba0f736bdce6098763d9b8ac0c0f95edaf8d9fd9c7"

PACKAGE_TARGET = Path("evidence/annotation_preparation/curl_v2_authoring_scope_successor/review_package/03_curl_v2_authoring_scope.v2.json")
PACKAGE_PREDECESSOR = Path("evidence/annotation_preparation/curl_v2_authoring_scope_successor/review_package/04_curl_v1_authoring_scope.v1.json")
SUMS = Path("evidence/annotation_preparation/curl_v2_authoring_scope_successor/review_package/09_review_package.v2.SHA256SUMS")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def run(args):
    return subprocess.run(
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def fail(msg):
    print("FAIL|" + msg)
    sys.exit(1)


if not PACKAGE_TARGET.is_file():
    fail("package target missing")

if sha(PACKAGE_TARGET) != TARGET_SHA:
    fail("package target SHA mismatch")

if not PACKAGE_PREDECESSOR.is_file():
    fail("predecessor copy missing")

if sha(PACKAGE_PREDECESSOR) != PREDECESSOR_SHA:
    fail("predecessor SHA mismatch")

if not SUMS.is_file():
    fail("checksum package missing")

lines = [
    x for x in SUMS.read_text(
        encoding="utf-8"
    ).splitlines()
    if x.strip()
]

for line in lines:
    digest, path = line.split("  ", 1)
    p = Path(path)

    if not p.is_file():
        fail("checksum target missing: " + path)

    if sha(p) != digest:
        fail("checksum mismatch: " + path)

cp = run([
    "git",
    "cat-file",
    "-e",
    AUTHOR_COMMIT + "^{commit}",
])

if cp.returncode == 0:
    tree = run([
        "git",
        "rev-parse",
        AUTHOR_COMMIT + "^{tree}",
    ])

    if tree.returncode != 0:
        fail("cannot resolve author tree")

    if tree.stdout.decode().strip() != AUTHOR_TREE:
        fail("author tree mismatch")

    blob = run([
        "git",
        "rev-parse",
        AUTHOR_COMMIT + ":" + TARGET_PATH,
    ])

    if blob.returncode != 0:
        fail("cannot resolve target blob")

    if blob.stdout.decode().strip() != TARGET_BLOB:
        fail("target blob mismatch")

    target = run([
        "git",
        "show",
        AUTHOR_COMMIT + ":" + TARGET_PATH,
    ])

    if target.returncode != 0:
        fail("cannot read committed target")

    if hashlib.sha256(target.stdout).hexdigest() != TARGET_SHA:
        fail("committed target SHA mismatch")

    predecessor = run([
        "git",
        "show",
        "9b3a33a358cd9cd0d4837b7221426d2e96d42239:" + PREDECESSOR_PATH,
    ])

    if predecessor.returncode == 0:
        if hashlib.sha256(predecessor.stdout).hexdigest() != PREDECESSOR_SHA:
            fail("committed predecessor SHA mismatch")

    print("GIT_BINDING_VERIFICATION=PASS")
else:
    print(
        "GIT_BINDING_VERIFICATION=UNAVAILABLE_IN_THIS_COPY;"
        "USE_A_CONTROLLED_EXTERNAL_HANDOFF_WITH_INDEPENDENTLY_"
        "RESOLVABLE_AUTHOR_COMMIT_METADATA"
    )

print("PACKAGE_BYTE_VERIFICATION=PASS")
print("HUMAN_REVIEW_COMPLETED=NO")
print("CANONICAL_FREEZE_AUTHORIZED=NO")
