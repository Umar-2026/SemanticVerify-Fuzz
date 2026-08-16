#!/usr/bin/env python3

from pathlib import Path
import hashlib
import subprocess
import sys

AUTHOR_COMMIT = "a2344c4905555388bbecd53834ca6627cdbe808a"
DRAFT_PATH = Path("evidence/annotation_preparation/specification_reconciliation_v1/libpcap_working_draft_v1/libpcap_source_only_working_fsm_draft.v1.json")
PACKAGE_COPY = Path("evidence/annotation_preparation/specification_reconciliation_v1/libpcap_working_draft_v1/review_package/03_libpcap_source_only_working_fsm_draft.v1.json")
EXPECTED_SHA = "2a2723eba8cac78c004b846fc1fe71e786730c9aeecc6800e81ee6f2e318687a"
EXPECTED_BLOB = "de11a08a6737f5a29734d2b41f7fd5c19cca8522"

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def fail(msg):
    print("VERIFY|FAIL|" + msg)
    sys.exit(1)

if not DRAFT_PATH.is_file():
    fail("repository draft missing")

if not PACKAGE_COPY.is_file():
    fail("package copy missing")

if sha(DRAFT_PATH) != EXPECTED_SHA:
    fail("repository draft SHA mismatch")

if sha(PACKAGE_COPY) != EXPECTED_SHA:
    fail("package copy SHA mismatch")

if DRAFT_PATH.read_bytes() != PACKAGE_COPY.read_bytes():
    fail("repository/package bytes differ")

cp = subprocess.run(
    [
        "git",
        "rev-parse",
        AUTHOR_COMMIT + ":" + str(DRAFT_PATH),
    ],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
)

if cp.returncode != 0:
    fail("cannot resolve draft blob at author commit")

if cp.stdout.strip() != EXPECTED_BLOB:
    fail("Git blob mismatch")

cp = subprocess.run(
    [
        "git",
        "show",
        AUTHOR_COMMIT + ":" + str(DRAFT_PATH),
    ],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
)

if cp.returncode != 0:
    fail("cannot read draft bytes from author commit")

if hashlib.sha256(cp.stdout).hexdigest() != EXPECTED_SHA:
    fail("author-commit draft bytes SHA mismatch")

print("VERIFY|PASS|repository target")
print("VERIFY|PASS|package byte identity")
print("VERIFY|PASS|author commit binding")
print("LIBPCAP_V1_REVIEW_PACKAGE_BINDING=PASS")
