#!/usr/bin/env python3
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

D0270_COMMIT = "f7c0461fd281f443547b79ce89b6a544ea299106"
D0270_TREE = "aab969fa4a2336a6faca559362e58962287c83b4"
D0270_PRIMARY_SHA = "95dd66ab7ff15c6785a70d44dbb930ffe6086de1b83d1baa1e6d261f2eb96f22"

GOVERNANCE_DESIGN_SHA = "68d1d6c4580f1e5683a122810f36d5b83f958de2dcfda2b62e25241d6437eaf1"

SUBJECT = (
    "decision: authorize separate positional inference adjudication "
    "for sufficient branch candidates 6 8 9 without execution"
)

BASE = Path(
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2"
)

D0270_PRIMARY = (
    BASE
    / "d0270_successor_result_universe_materialization_execution_v1"
    / "01_successor_result_universe_materialization_execution.v1.json"
)

PKG = BASE / "d0271_sufficient_branch_positional_inference_adjudication_authorization_v1"

RECORD = PKG / "01_sufficient_branch_positional_inference_adjudication_authorization.v1.json"
SCOPE = PKG / "02_sufficient_branch_positional_inference_adjudication_authorization_scope.v1.md"
VERIFIER = PKG / "03_verify_sufficient_branch_positional_inference_adjudication_authorization.v1.py"
MANIFEST = PKG / "04_sufficient_branch_positional_inference_adjudication_authorization.v1.SHA256SUMS"

DECISION = Path(
    "documentation/decisions/"
    "0271-authorize-separate-positional-inference-adjudication-"
    "for-sufficient-branch-candidates-6-8-9-without-execution.md"
)

def die(msg):
    print("SAFE_D0271_VERIFIER=FAIL")
    print("FAIL_REASON=" + msg)
    sys.exit(1)

def git(repo, *args, check=True):
    p = subprocess.run(
        ["git", *args],
        cwd=repo,
        text=True,
        capture_output=True,
    )
    if check and p.returncode != 0:
        die("git command failed: " + " ".join(args))
    return p

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

parser = argparse.ArgumentParser()
parser.add_argument("--precommit", action="store_true")
args = parser.parse_args()

probe = subprocess.run(
    ["git", "rev-parse", "--show-toplevel"],
    text=True,
    capture_output=True,
)

if probe.returncode != 0:
    die("not inside git repository")

repo = Path(probe.stdout.strip())

head = git(repo, "rev-parse", "HEAD").stdout.strip()
origin = git(repo, "rev-parse", "origin/main").stdout.strip()

# D0270 must remain in the published lineage.
published = git(
    repo,
    "merge-base",
    "--is-ancestor",
    D0270_COMMIT,
    origin,
    check=False,
)

if published.returncode != 0:
    die("origin/main no longer contains frozen D0270")

tree = git(repo, "rev-parse", f"{D0270_COMMIT}^{{tree}}").stdout.strip()

if tree != D0270_TREE:
    die("D0270 tree mismatch")

source_path = repo / D0270_PRIMARY

if not source_path.is_file():
    die("D0270 primary missing")

if sha(source_path) != D0270_PRIMARY_SHA:
    die("D0270 primary SHA mismatch")

for rel in [RECORD, SCOPE, VERIFIER, MANIFEST, DECISION]:
    if not (repo / rel).is_file():
        die("required D0271 artifact missing: " + str(rel))

manifest_lines = [
    line.strip()
    for line in (repo / MANIFEST).read_text(encoding="utf-8").splitlines()
    if line.strip()
]

if len(manifest_lines) != 3:
    die("manifest entry count mismatch")

expected_names = {
    "01_sufficient_branch_positional_inference_adjudication_authorization.v1.json",
    "02_sufficient_branch_positional_inference_adjudication_authorization_scope.v1.md",
    "03_verify_sufficient_branch_positional_inference_adjudication_authorization.v1.py",
}

seen = set()

for line in manifest_lines:
    parts = line.split(None, 1)
    if len(parts) != 2:
        die("malformed manifest line")

    expected_hash, name = parts
    name = name.lstrip("*")

    if name not in expected_names:
        die("unexpected manifest file: " + name)

    target = repo / PKG / name

    if sha(target) != expected_hash:
        die("manifest SHA mismatch: " + name)

    seen.add(name)

if seen != expected_names:
    die("manifest file set mismatch")

source = json.loads(source_path.read_text(encoding="utf-8"))
record = json.loads((repo / RECORD).read_text(encoding="utf-8"))

if record.get("authorization_id") != (
    "D0271-SUFFICIENT-BRANCH-POSITIONAL-INFERENCE-ADJUDICATION-AUTHORIZATION-V1"
):
    die("authorization_id mismatch")

if record.get("authorizing_decision") != "D0271":
    die("authorizing_decision mismatch")

if record.get("designated_execution_decision") != "D0272":
    die("designated execution decision mismatch")

binding = record.get("source_governance_binding", {})

if binding.get("decision") != "D0270":
    die("source decision mismatch")

if binding.get("commit") != D0270_COMMIT:
    die("source commit mismatch")

if binding.get("tree") != D0270_TREE:
    die("source tree mismatch")

if binding.get("primary_sha256") != D0270_PRIMARY_SHA:
    die("source primary SHA mismatch")

if binding.get(
    "post_d0270_successor_branch_governance_design_sha256"
) != GOVERNANCE_DESIGN_SHA:
    die("branch governance design SHA mismatch")

target = record.get("target_branch", {})

if target != {
    "branch_id": "S1_SUFFICIENT_POSITIONAL_BRANCH",
    "candidate_indices": [6,8,9],
    "frozen_entry_state":
        "FROZEN_SNAPSHOT_EVIDENCE_SUFFICIENT_FOR_SEPARATE_POSITIONAL_ADJUDICATION",
    "authorized_operation":
        "SEPARATE_POSITIONAL_INFERENCE_ADJUDICATION",
}:
    die("target branch binding mismatch")

summary = source.get("materialized_universe", {}).get("summary", {})

if summary.get("sufficient_indices") != [6,8,9]:
    die("D0270 sufficient branch mismatch")

if summary.get("indeterminate_indices") != [1,2]:
    die("D0270 indeterminate branch mismatch")

if summary.get("insufficient_indices") != [3,5,7,10]:
    die("D0270 insufficient branch mismatch")

contract = record.get("authorization_contract", {})

required_true = [
    "bounded_branch_local_positional_inference_adjudication_authorized",
    "candidate_scope_must_equal_6_8_9",
    "adjudication_scope_limited_to_authorized_branch_operation",
]

for key in required_true:
    if contract.get(key) is not True:
        die("required authorization flag not true: " + key)

required_false = [
    "execution_in_d0271",
    "execution_performed",
    "execution_allowed_before_independent_d0271_checkpoint",
    "branch_membership_mutation_authorized",
    "candidate_migration_authorized",
    "cross_branch_backflow_authorized",
    "d0251_snapshot_content_read_authorized",
    "original_source_blob_reopen_authorized",
    "new_evidence_acquisition_authorized",
    "result_reselection_authorized",
    "evidence_rejudgment_authorized",
    "historical_result_mutation_authorized",
    "sufficiency_result_mutation_authorized",
    "general_new_semantic_adjudication_authorized",
    "global_positional_status_assignment_authorized",
    "class06_reclassification_authorized",
    "indeterminate_branch_resolution_authorized",
    "insufficient_branch_evidence_acquisition_authorized",
    "c4_authorized",
    "c5_authorized",
    "c6_authorized",
    "b2_readiness_established",
    "b2_authorized",
    "b2_executed",
    "active_schema_v2_materialization_authorized",
    "analyzer_authorized",
    "baseline_authorized",
    "repair_authorized",
]

for key in required_false:
    if contract.get(key) is not False:
        die("required prohibition not false: " + key)

if contract.get("designated_execution_decision") != "D0272":
    die("contract D0272 binding mismatch")

if record.get("next_required_checkpoint") != (
    "INDEPENDENT_READ_ONLY_VERIFY_D0271_AUTHORIZATION_BEFORE_D0272_EXECUTION"
):
    die("next checkpoint mismatch")

scope = (repo / SCOPE).read_text(encoding="utf-8")
decision = (repo / DECISION).read_text(encoding="utf-8")

for phrase in [
    GOVERNANCE_DESIGN_SHA,
    "S1_SUFFICIENT_POSITIONAL_BRANCH",
    "6,8,9",
    "SEPARATE_POSITIONAL_INFERENCE_ADJUDICATION",
    "INDEPENDENT_READ_ONLY_VERIFY_D0271_AUTHORIZATION_BEFORE_D0272_EXECUTION",
]:
    if phrase not in scope:
        die("required scope phrase missing: " + phrase)

for phrase in [
    "D0271 is authorization-only.",
    "D0272 is the designated execution decision.",
    "No positional adjudication is executed by D0271.",
    "No global positional status is assigned by D0271.",
    "No Class06 reclassification is authorized by D0271.",
    "No push is authorized by this decision.",
]:
    if phrase not in decision:
        die("required decision phrase missing: " + phrase)

if args.precommit:
    if head != D0270_COMMIT:
        die("precommit HEAD must equal D0270")

    d0272_decisions = list(
        (repo / "documentation/decisions").glob("0272-*")
    )
    d0272_packages = list(BASE.glob("d0272_*"))

    if d0272_decisions or d0272_packages:
        die("D0272 must not exist before D0271 checkpoint")
else:
    commits = [
        x.strip()
        for x in git(
            repo,
            "log",
            "--diff-filter=A",
            "--format=%H",
            "--",
            str(DECISION),
        ).stdout.splitlines()
        if x.strip()
    ]

    if len(commits) != 1:
        die("cannot uniquely identify D0271 commit")

    decision_commit = commits[0]

    parent = git(
        repo,
        "rev-parse",
        f"{decision_commit}^",
    ).stdout.strip()

    subject = git(
        repo,
        "show",
        "-s",
        "--format=%s",
        decision_commit,
    ).stdout.strip()

    if parent != D0270_COMMIT:
        die("D0271 parent mismatch")

    if subject != SUBJECT:
        die("D0271 subject mismatch")

    descendant = git(
        repo,
        "merge-base",
        "--is-ancestor",
        decision_commit,
        head,
        check=False,
    )

    if descendant.returncode != 0:
        die("D0271 commit is not ancestor-or-equal of HEAD")

print("D0271_SUFFICIENT_BRANCH_POSITIONAL_ADJUDICATION_AUTHORIZATION_VERIFIER=PASS")
print("D0270_SOURCE_GOVERNANCE_BINDING=PASS")
print("POST_D0270_GOVERNANCE_DESIGN_SHA256=" + GOVERNANCE_DESIGN_SHA)
print("D0271_AUTHORIZED_BRANCH=S1_SUFFICIENT_POSITIONAL_BRANCH")
print("D0271_AUTHORIZED_CANDIDATES=6,8,9")
print("D0271_BOUNDED_BRANCH_LOCAL_POSITIONAL_ADJUDICATION_AUTHORIZED=YES")
print("D0272_DESIGNATED_EXECUTION_DECISION=YES")
print("D0272_EXECUTION_ALLOWED_BEFORE_INDEPENDENT_D0271_CHECKPOINT=NO")
print("D0271_POSITIONAL_ADJUDICATION_EXECUTED=NO")
print("GLOBAL_POSITIONAL_STATUS_ASSIGNMENT_AUTHORIZED=NO")
print("CLASS06_RECLASSIFICATION_AUTHORIZED=NO")
print("D0251_SNAPSHOT_CONTENT_READ_AUTHORIZED=NO")
print("NEW_EVIDENCE_ACQUISITION_AUTHORIZED=NO")
print("INDETERMINATE_BRANCH_RESOLUTION_AUTHORIZED=NO")
print("INSUFFICIENT_BRANCH_EVIDENCE_ACQUISITION_AUTHORIZED=NO")
print("B2_AUTHORIZED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
print("SAFE_D0271_VERIFIER=PASS")
