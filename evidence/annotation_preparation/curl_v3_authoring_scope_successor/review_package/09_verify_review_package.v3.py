#!/usr/bin/env python3

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[3]

V3_REL = Path("config/annotation/curl_v3_authoring_scope.v3.json")
V2_REL = Path("config/annotation/curl_v2_authoring_scope.v2.json")

V3_SHA = "ede7e1422b9553f73377432474deb282852b619a5b004cd7c4d00033c0a37abb"
V2_SHA = "f8a5a0d360ad68478649a549744e4d13f22aec7d7edcc60116052906424b52df"

V3_COMMIT = "7de6fc01797ae68cbd64406b850a3198f71cc702"
V3_TREE = "c5f96b844e5803cccd04c9f64a55754dc6c77e20"
V3_BLOB = "931c24cc46c99f23ee352455d3e8c93e57e63401"

def fail(msg):
    print("FAIL|" + msg)
    sys.exit(1)

def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def git(*args):
    p = subprocess.run(
        ["git", "-C", str(REPO), *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if p.returncode != 0:
        fail("GIT|" + " ".join(args) + "|" + p.stderr.strip())
    return p.stdout.strip()

repo_v3 = REPO / V3_REL
repo_v2 = REPO / V2_REL

pkg_v3 = ROOT / "03_curl_v3_authoring_scope.v3.json"
pkg_v2 = ROOT / "04_curl_v2_authoring_scope.v2.json"

if sha(repo_v3) != V3_SHA:
    fail("REPOSITORY_V3_SHA")

if sha(pkg_v3) != V3_SHA:
    fail("PACKAGE_V3_SHA")

if repo_v3.read_bytes() != pkg_v3.read_bytes():
    fail("V3_PACKAGE_COPY_BYTE_IDENTITY")

if sha(repo_v2) != V2_SHA:
    fail("REPOSITORY_V2_SHA")

if sha(pkg_v2) != V2_SHA:
    fail("PACKAGE_V2_SHA")

if repo_v2.read_bytes() != pkg_v2.read_bytes():
    fail("V2_PACKAGE_COPY_BYTE_IDENTITY")

if git("rev-parse", V3_COMMIT + "^{tree}") != V3_TREE:
    fail("V3_TREE")

if git("rev-parse", V3_COMMIT + ":" + str(V3_REL)) != V3_BLOB:
    fail("V3_BLOB")

v2 = json.loads(pkg_v2.read_text(encoding="utf-8"))
v3 = json.loads(pkg_v3.read_text(encoding="utf-8"))

critical = [
    "in_scope_functions",
    "library",
    "library_revision",
    "scenario_manifest",
    "source_evidence",
    "primary_resources",
    "global_state_rules",
    "easy_handle_rules",
    "multi_easy_membership_rules",
    "multi_perform_error_rules",
    "defect_category_projection",
    "normative_strength_review_items",
    "option_surface_policy",
    "scope_selection_policy",
    "explicitly_excluded_functions",
]

for key in critical:
    if v2.get(key) != v3.get(key):
        fail("SEMANTIC_PRESERVATION|" + key)

if v3.get("human_review_completed") is not False:
    fail("V3_HUMAN_REVIEW_PRECOMPLETED")

if v3.get("scope_frozen") is not False:
    fail("V3_SCOPE_PREMATURELY_FROZEN")

ac = v3["authoring_constraints"]

if ac.get("scope_freeze_authorized_after_exact_v3_human_approval") is not True:
    fail("SCOPE_FREEZE_BOUNDARY_MISSING")

if ac.get(
    "technical_working_draft_authorized_immediately_after_exact_v3_human_approval"
) is not False:
    fail("DIRECT_HUMAN_APPROVAL_TO_TECHNICAL_DRAFT_NOT_BLOCKED")

if ac.get(
    "technical_working_draft_authorized_only_after_completed_v3_scope_freeze"
) is not True:
    fail("COMPLETED_FREEZE_REQUIREMENT_MISSING")

if ac.get("technical_working_draft_authorized_now") is not False:
    fail("TECHNICAL_DRAFT_PREAUTHORIZED")

manifest = json.loads(
    (ROOT / "08_review_package_manifest.v3.json").read_text(encoding="utf-8")
)

if manifest["human_review_completed"] is not False:
    fail("MANIFEST_HUMAN_REVIEW_COMPLETED")

if manifest["overall_review_decision"] is not None:
    fail("MANIFEST_DECISION_PREPOPULATED")

if manifest["scope_freeze_authorized"] is not False:
    fail("MANIFEST_SCOPE_FREEZE_PREAUTHORIZED")

if manifest["technical_working_draft_authorized"] is not False:
    fail("MANIFEST_TECHNICAL_DRAFT_PREAUTHORIZED")

if any(manifest["quarantine"].values()):
    fail("QUARANTINE_FLAG_TRUE")

print("GIT_BINDING_VERIFICATION=PASS")
print("PACKAGE_BYTE_VERIFICATION=PASS")
print("V2_RR01_THROUGH_RR06_SEMANTICS_PRESERVED=YES")
print("V3_RR07_AUTHORIZATION_BOUNDARY_CORRECTED=YES")
print("HUMAN_REVIEW_COMPLETED=NO")
print("SCOPE_FREEZE_AUTHORIZED=NO")
print("TECHNICAL_WORKING_DRAFT_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
print("CURL_V3_REVIEW_PACKAGE_VERIFICATION=PASS")
