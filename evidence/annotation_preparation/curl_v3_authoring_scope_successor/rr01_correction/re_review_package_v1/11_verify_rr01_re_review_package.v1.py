#!/usr/bin/env python3

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[4]

V3_REPO = REPO / "config/annotation/curl_v3_authoring_scope.v3.json"
V2_REPO = REPO / "config/annotation/curl_v2_authoring_scope.v2.json"
D23_REPO = REPO / "documentation/decisions/0023-curl-v3-rr07-authorization-boundary-successor.md"
D24_REPO = REPO / "documentation/decisions/0024-curl-v3-rr01-binding-and-handoff-correction.md"

V3_PACKAGE = ROOT / "03_curl_v3_authoring_scope.v3.json"
V2_PACKAGE = ROOT / "04_curl_v2_authoring_scope.v2.json"
D23_PACKAGE = ROOT / "05_decision_0023.HISTORICAL_IMMUTABLE.md"
D24_PACKAGE = ROOT / "06_decision_0024.RR01_CORRECTION.md"

PRIOR_REVIEW = ROOT / "07_completed_v3_human_review.REVISION_REQUIRED.md"
PRIOR_RECORD = ROOT / "08_prior_v3_human_review_decision_record.json"

PACKET = ROOT / "02_curl_v3_rr01_corrected_reviewer_packet.v1.md"
MANIFEST = ROOT / "09_re_review_package_manifest.v1.json"

WITNESS_VERIFY = (
    ROOT /
    "10_minimal_git_witness_v1" /
    "03_verify_minimal_git_witness.v1.py"
)

V3_SHA = "ede7e1422b9553f73377432474deb282852b619a5b004cd7c4d00033c0a37abb"
V2_SHA = "f8a5a0d360ad68478649a549744e4d13f22aec7d7edcc60116052906424b52df"
D23_SHA = "c774bb667930ef9ceaedc5ca5d25e88d57da3ffefa10de639ef6a20f7d2271d1"
D24_SHA = "df22dc70c572407c1968859f6fd86a20d847062b2130a08484670c06a340915b"
PRIOR_REVIEW_SHA = "3e77a9456d49ccd0001ad839b1e2a32478d45a05cc94b0ba115cdd667a45afb9"


def fail(msg):
    print("FAIL|" + msg)
    raise SystemExit(1)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


for repo_path, pkg_path, expected, label in [
    (V3_REPO, V3_PACKAGE, V3_SHA, "V3"),
    (V2_REPO, V2_PACKAGE, V2_SHA, "V2"),
    (D23_REPO, D23_PACKAGE, D23_SHA, "D23"),
    (D24_REPO, D24_PACKAGE, D24_SHA, "D24"),
]:
    if not repo_path.is_file():
        fail(label + "_REPO_FILE_MISSING")

    if not pkg_path.is_file():
        fail(label + "_PACKAGE_FILE_MISSING")

    if sha(repo_path) != expected:
        fail(label + "_REPO_SHA")

    if sha(pkg_path) != expected:
        fail(label + "_PACKAGE_SHA")

    if repo_path.read_bytes() != pkg_path.read_bytes():
        fail(label + "_BYTE_IDENTITY")

if sha(PRIOR_REVIEW) != PRIOR_REVIEW_SHA:
    fail("PRIOR_REVIEW_SHA")

record = json.loads(PRIOR_RECORD.read_text(encoding="utf-8"))

if record.get("overall_decision") != "REVISION_REQUIRED":
    fail("PRIOR_OVERALL_DECISION")

decisions = record.get("review_item_decisions", {})

expected_decisions = {
    "V3-RR01": "REVISION_REQUIRED",
    "V3-RR02": "PASS",
    "V3-RR03": "PASS",
    "V3-RR04": "PASS",
}

if decisions != expected_decisions:
    fail("PRIOR_REVIEW_DECISIONS|" + repr(decisions))

d23_text = D23_PACKAGE.read_text(encoding="utf-8")

bad_line = (
    '- SHA-256: `$ `config/annotation/'
    'curl_v2_authoring_scope.v2.json`'
)

if bad_line not in d23_text:
    fail("HISTORICAL_D23_DEFECT_NOT_PRESERVED")

d24_text = D24_PACKAGE.read_text(encoding="utf-8")

if bad_line in d24_text:
    fail("D23_MALFORMED_PATTERN_PROPAGATED_TO_D24")

if V2_SHA not in d24_text:
    fail("CORRECT_V2_SHA_NOT_IN_D24")

manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

if manifest.get("human_re_review_completed") is not False:
    fail("RE_REVIEW_PRECOMPLETED")

if manifest.get("overall_re_review_decision") is not None:
    fail("OVERALL_RE_REVIEW_DECISION_PREPOPULATED")

for key, value in manifest.get("authorization_state", {}).items():
    if value is not False:
        fail("PREAUTHORIZED|" + key)

packet = PACKET.read_text(encoding="utf-8").replace("\\_", "_")

for rr in ("RR01-R1", "RR01-R2", "RR01-R3", "RR01-R4"):
    section = re.search(
        rf"^### {re.escape(rr)}\b[^\n]*$"
        rf"(.*?)(?=^### |^## Overall re-review decision|\Z)",
        packet,
        re.M | re.S,
    )

    if not section:
        fail("PACKET_SECTION_MISSING|" + rr)

    m = re.search(
        r"^Decision:[ \t]*(.*)$",
        section.group(1),
        re.M,
    )

    if not m:
        fail("PACKET_DECISION_LINE_MISSING|" + rr)

    if m.group(1).strip():
        fail("PACKET_DECISION_PREPOPULATED|" + rr)

m = re.search(
    r"^Overall decision:[ \t]*(.*)$",
    packet,
    re.M,
)

if not m:
    fail("OVERALL_DECISION_LINE_MISSING")

if m.group(1).strip():
    fail("OVERALL_DECISION_PREPOPULATED")

for label in (
    "Human reviewer name:",
    "Human reviewer signature / recorded confirmation:",
    "Human reviewer date:",
):
    lines = [
        x for x in packet.splitlines()
        if x.startswith(label)
    ]

    if len(lines) != 1:
        fail("REVIEWER_FIELD_COUNT|" + label)

    if lines[0][len(label):].strip():
        fail("REVIEWER_FIELD_PREPOPULATED|" + label)

cp = subprocess.run(
    [sys.executable, str(WITNESS_VERIFY)],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
)

if cp.returncode != 0:
    sys.stdout.write(cp.stdout.decode(errors="replace"))
    sys.stderr.write(cp.stderr.decode(errors="replace"))
    fail("MINIMAL_GIT_WITNESS_VERIFY")

print("EXACT_V3_PACKAGE_BINDING=PASS")
print("EXACT_V2_PREDECESSOR_BINDING=PASS")
print("HISTORICAL_DECISION_0023_PRESERVED=YES")
print("DECISION_0024_CORRECTION_BINDING=PASS")
print("PRIOR_V3_REVIEW_BINDING=PASS")
print("PRIOR_V3_RR02_TO_RR04_PASS_PRESERVED=YES")
print("MINIMAL_GIT_WITNESS_BINDING=PASS")
print("RR01_R1_TO_R4_DECISIONS=BLANK")
print("OVERALL_RE_REVIEW_DECISION=BLANK")
print("REVIEWER_IDENTITY_FIELDS=BLANK")
print("V3_SCOPE_FREEZE_AUTHORIZED=NO")
print("TECHNICAL_WORKING_DRAFT_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
print("CURL_V3_RR01_RE_REVIEW_PACKAGE_VERIFICATION=PASS")
