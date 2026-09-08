#!/usr/bin/env python3
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path


D0269_COMMIT = "9b839b32778b392201240df694d96e54ec8f6bd8"
D0269_TREE = "8f815bd9ab289c89149cd8487e113fc3da216ad4"
D0269_AUTH_SHA = "0f80fd806e384e009b590bab0f2ccd557bbe43aa9b073b038d618adb6df94e1c"

DESIGN_SHA = "1810d0292b49e163fe3975acc1302469aa918f6f264ad3d2ab17b4f802ab7e47"
PROJECTION_SHA = "a87715860953980ae9a39fc89a3c8242683189d79098240566a325c7944cfe85"

SUBJECT = (
    "decision: execute successor result-universe materialization "
    "from frozen resolved components"
)

BASE = Path(
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2"
)

AUTH = (
    BASE
    / "d0269_successor_result_universe_materialization_authorization_v1"
    / "01_successor_result_universe_materialization_authorization.v1.json"
)

PKG = BASE / "d0270_successor_result_universe_materialization_execution_v1"

PRIMARY = PKG / "01_successor_result_universe_materialization_execution.v1.json"
SCOPE = PKG / "02_successor_result_universe_materialization_execution_scope.v1.md"
VERIFIER = PKG / "03_verify_successor_result_universe_materialization_execution.v1.py"
MANIFEST = PKG / "04_successor_result_universe_materialization_execution.v1.SHA256SUMS"

DECISION = Path(
    "documentation/decisions/"
    "0270-execute-successor-result-universe-materialization-"
    "from-frozen-resolved-components.md"
)


def die(msg):
    print("SAFE_D0270_VERIFIER=FAIL")
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

# Publication metadata is mutable. D0269 must remain in the published lineage.
ancestry = git(
    repo,
    "merge-base",
    "--is-ancestor",
    D0269_COMMIT,
    origin,
    check=False,
)
if ancestry.returncode != 0:
    die("published origin/main no longer contains D0269")

tree = git(repo, "rev-parse", f"{D0269_COMMIT}^{{tree}}").stdout.strip()
if tree != D0269_TREE:
    die("D0269 tree mismatch")

auth_path = repo / AUTH
if not auth_path.is_file():
    die("D0269 authorization record missing")

if sha(auth_path) != D0269_AUTH_SHA:
    die("D0269 authorization record SHA mismatch")

for rel in [PRIMARY, SCOPE, VERIFIER, MANIFEST, DECISION]:
    if not (repo / rel).is_file():
        die("required D0270 artifact missing: " + str(rel))

# Verify three-entry package manifest without executing another verifier.
manifest_lines = [
    line.strip()
    for line in (repo / MANIFEST).read_text(encoding="utf-8").splitlines()
    if line.strip()
]

if len(manifest_lines) != 3:
    die("manifest entry count mismatch")

expected_manifest_files = {
    "01_successor_result_universe_materialization_execution.v1.json",
    "02_successor_result_universe_materialization_execution_scope.v1.md",
    "03_verify_successor_result_universe_materialization_execution.v1.py",
}

seen = set()

for line in manifest_lines:
    parts = line.split(None, 1)
    if len(parts) != 2:
        die("malformed manifest entry")

    expected_hash, name = parts
    name = name.lstrip("*")

    if name not in expected_manifest_files:
        die("unexpected manifest filename: " + name)

    target = repo / PKG / name
    if sha(target) != expected_hash:
        die("manifest SHA mismatch: " + name)

    seen.add(name)

if seen != expected_manifest_files:
    die("manifest file set mismatch")

auth = json.loads(auth_path.read_text(encoding="utf-8"))
primary = json.loads((repo / PRIMARY).read_text(encoding="utf-8"))

if primary.get("execution_id") != (
    "D0270-SUCCESSOR-RESULT-UNIVERSE-MATERIALIZATION-EXECUTION-V1"
):
    die("execution_id mismatch")

if primary.get("executing_decision") != "D0270":
    die("executing_decision mismatch")

if primary.get("transaction_design_sha256") != DESIGN_SHA:
    die("transaction design SHA mismatch")

if primary.get("input_projection_sha256") != PROJECTION_SHA:
    die("input projection SHA mismatch")

if primary.get("operation") != (
    "MATERIALIZE_ALREADY_RESOLVED_SUCCESSOR_RESULT_UNIVERSE"
):
    die("operation mismatch")

if primary.get("semantics") != (
    "AGGREGATION_OF_ALREADY_RESOLVED_COMPONENTS_ONLY"
):
    die("semantics mismatch")

binding = primary.get("authorization_binding", {})
if binding != {
    "decision": "D0269",
    "commit": D0269_COMMIT,
    "authorization_record_sha256": D0269_AUTH_SHA,
}:
    die("authorization binding mismatch")

if primary.get("independent_d0269_checkpoint_satisfied") is not True:
    die("independent D0269 checkpoint flag mismatch")

u = auth.get("successor_result_universe_binding", {})

expected_universe = {
    "candidate_count": u.get("candidate_count"),
    "candidate_order": u.get("candidate_order"),
    "candidate_4_included": u.get("candidate_4_included"),
    "candidate_4_exclusion_reason": u.get("candidate_4_exclusion_reason"),
    "candidate_results": u.get("candidate_results"),
    "summary": u.get("summary"),
}

if primary.get("materialized_universe") != expected_universe:
    die("materialized universe differs from D0269 bound universe")

if expected_universe["candidate_order"] != [1,2,3,5,6,7,8,9,10]:
    die("candidate order mismatch")

summary = expected_universe["summary"]

if summary.get("sufficient_indices") != [6,8,9]:
    die("sufficient indices mismatch")

if summary.get("insufficient_indices") != [3,5,7,10]:
    die("insufficient indices mismatch")

if summary.get("indeterminate_indices") != [1,2]:
    die("indeterminate indices mismatch")

constraints = primary.get("execution_constraints", {})

required_false = [
    "active_schema_v2_materialization",
    "analyzer_authorization",
    "b2_authorization",
    "b2_execution",
    "b2_readiness_established",
    "baseline_authorization",
    "c4_authorization",
    "c5_authorization",
    "c6_authorization",
    "candidate_order_change",
    "candidate_result_change",
    "class06_reclassification",
    "d0251_snapshot_content_read",
    "evidence_rejudgment",
    "historical_result_mutation",
    "new_evidence_acquisition",
    "new_semantic_adjudication",
    "original_source_blob_reopen",
    "positional_status_adjudication",
    "positional_status_assignment",
    "repair_authorization",
    "result_reselection",
    "summary_change",
]

for key in required_false:
    if constraints.get(key) is not False:
        die("execution constraint not false: " + key)

result = primary.get("execution_result", {})

if result.get("successor_result_universe_materialization_executed") is not True:
    die("materialization execution flag mismatch")

if result.get("positional_status_assigned") is not False:
    die("positional status changed")

if result.get("class06_reclassified") is not False:
    die("Class06 changed")

if result.get("downstream_branch_execution_authorized_automatically") is not False:
    die("downstream branch auto-authorization mismatch")

one = primary.get("one_time_execution", {})

if one != {
    "authorized": True,
    "consumed": True,
    "execution_count": 1,
}:
    die("one-time execution contract mismatch")

if primary.get("next_required_checkpoint") != (
    "INDEPENDENT_READ_ONLY_VERIFY_D0270_MATERIALIZATION_EXECUTION"
):
    die("next checkpoint mismatch")

scope_text = (repo / SCOPE).read_text(encoding="utf-8")
decision_text = (repo / DECISION).read_text(encoding="utf-8")

for phrase in [
    DESIGN_SHA,
    PROJECTION_SHA,
    "AGGREGATION_OF_ALREADY_RESOLVED_COMPONENTS_ONLY",
    "execution_count = 1",
    "consumed = true",
    "INDEPENDENT_READ_ONLY_VERIFY_D0270_MATERIALIZATION_EXECUTION",
]:
    if phrase not in scope_text:
        die("required scope phrase missing: " + phrase)

for phrase in [
    "No push is authorized by this decision.",
    "No positional status is assigned by D0270.",
    "No Class06 reclassification is performed by D0270.",
    "D0270 consumes the single authorized materialization execution.",
]:
    if phrase not in decision_text:
        die("required decision phrase missing: " + phrase)

if args.precommit:
    if head != D0269_COMMIT:
        die("precommit HEAD must equal D0269")
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
        die("cannot uniquely identify D0270 decision commit")

    d0270_commit = commits[0]

    parent = git(repo, "rev-parse", f"{d0270_commit}^").stdout.strip()
    subject = git(
        repo,
        "show",
        "-s",
        "--format=%s",
        d0270_commit,
    ).stdout.strip()

    if parent != D0269_COMMIT:
        die("D0270 parent mismatch")

    if subject != SUBJECT:
        die("D0270 subject mismatch")

    desc = git(
        repo,
        "merge-base",
        "--is-ancestor",
        d0270_commit,
        head,
        check=False,
    )

    if desc.returncode != 0:
        die("D0270 commit is not ancestor-or-equal of HEAD")

print("D0270_SUCCESSOR_RESULT_UNIVERSE_MATERIALIZATION_EXECUTION_VERIFIER=PASS")
print("D0269_AUTHORIZATION_BINDING=PASS")
print("D0270_BOUND_TRANSACTION_DESIGN_SHA256=" + DESIGN_SHA)
print("D0270_INPUT_PROJECTION_SHA256=" + PROJECTION_SHA)
print("D0270_MATERIALIZED_CANDIDATE_COUNT=9")
print("D0270_MATERIALIZED_SUFFICIENT_INDICES=6,8,9")
print("D0270_MATERIALIZED_INSUFFICIENT_INDICES=3,5,7,10")
print("D0270_MATERIALIZED_INDETERMINATE_INDICES=1,2")
print("D0270_ONE_TIME_EXECUTION_COUNT=1")
print("D0270_ONE_TIME_EXECUTION_CONSUMED=YES")
print("D0251_SNAPSHOT_CONTENT_READ_BY_D0270_VERIFIER=NO")
print("RESULT_RESELECTION_PERFORMED_BY_D0270_VERIFIER=NO")
print("EVIDENCE_REJUDGED_BY_D0270_VERIFIER=NO")
print("POSITIONAL_STATUS_ASSIGNED=NO")
print("CLASS06_RECLASSIFIED=NO")
print("B2_AUTHORIZED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
print("SAFE_D0270_VERIFIER=PASS")
