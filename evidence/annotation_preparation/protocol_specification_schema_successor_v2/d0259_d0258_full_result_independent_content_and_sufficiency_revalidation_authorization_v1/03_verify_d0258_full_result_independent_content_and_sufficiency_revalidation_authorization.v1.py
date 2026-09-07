#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys

REPO=Path(
    os.environ.get(
        "SVF_REPO_ROOT",
        "/openbayes/home/semanticverify-fuzz-research",
    )
)

BASE=Path(
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2"
)

PKG_REL=BASE / (
    "d0259_d0258_full_result_independent_content_and_"
    "sufficiency_revalidation_authorization_v1"
)

DECISION_REL=Path(
    "documentation/decisions/"
    "0259-authorize-d0258-full-result-independent-content-and-"
    "sufficiency-revalidation-without-execution.md"
)

D0258_COMMIT="15afca914011851d516a05976e4d2d61c586f9d4"
D0258_TREE="622b95b7c9daba7659ceec08e75c90832d5a4dae"
D0258_PRIMARY_SHA="4aa389ad41c3a532c61c3b38aa397da6dccebb96d3384bb6a22d1e0af6462e60"
D0258_MANIFEST_SHA="7a7f534d54c68aca01784d2a611f7875b674c7d58401c9223c9cc8141fd4f895"

SNAPSHOT_BINDING_SHA="51afc6fda72397cebde135eb8762a1269ffd7acdbe32d5941abbf4db220d23b3"
RESULT_PROFILE_SHA="8a565bebd1a6a26112ccdd9d2b34db56f714d3892441cc9a1632da7662884b73"
EVIDENCE_SHA="d9e1ec6d28a32b7477f472fb91a19c93c60c63b6c23e8ddbe4d467cac5e86a11"
RATIONALE_SHA="abb35982ec168b82b696244c24c6f1d58ad2f3096cc6878478f3e69516f496ce"
FULL_ASSESSMENT_SHA="1767e05713cd6b35c9bb6df8bfad65b97e9c95553cc6da71174cebb62b5e861f"

D0254_PRIMARY=REPO / BASE / (
    "d0254_c3_bounded_candidate_content_adjudication_execution_v1/"
    "01_c3_bounded_candidate_content_adjudication_execution.v1.json"
)

D0258_PRIMARY=REPO / BASE / (
    "d0258_bounded_positional_inference_evidence_sufficiency_"
    "assessment_execution_v1/"
    "01_bounded_positional_inference_evidence_sufficiency_"
    "assessment_execution.v1.json"
)

D0258_MANIFEST=REPO / BASE / (
    "d0258_bounded_positional_inference_evidence_sufficiency_"
    "assessment_execution_v1/"
    "05_bounded_positional_inference_evidence_sufficiency_"
    "assessment_execution.v1.SHA256SUMS"
)

PRIMARY_NAME=(
    "01_d0258_full_result_independent_content_and_"
    "sufficiency_revalidation_authorization.v1.json"
)

SCOPE_NAME=(
    "02_d0258_full_result_independent_content_and_"
    "sufficiency_revalidation_authorization_scope.v1.md"
)

SELF_NAME=(
    "03_verify_d0258_full_result_independent_content_and_"
    "sufficiency_revalidation_authorization.v1.py"
)

MANIFEST_NAME=(
    "04_d0258_full_result_independent_content_and_"
    "sufficiency_revalidation_authorization.v1.SHA256SUMS"
)

EXPECTED_MANIFEST_NAMES={
    PRIMARY_NAME,
    SCOPE_NAME,
    SELF_NAME,
}

EXPECTED_SUBJECT=(
    "decision: authorize D0258 full-result independent content "
    "and sufficiency revalidation without execution"
)

INDICES=[1,2,3,5,6,7,8,9,10]

def die(msg):
    raise AssertionError(msg)

def git(*args):
    return subprocess.check_output(
        ["git", *args],
        cwd=REPO,
        text=True,
    ).strip()

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def no_dup(pairs):
    out={}
    for k,v in pairs:
        if k in out:
            die("duplicate JSON key: " + k)
        out[k]=v
    return out

def canonical(obj):
    return json.dumps(
        obj,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")

def canonical_hash(obj):
    return hashlib.sha256(canonical(obj)).hexdigest()

# ----------------------------------------------------------------------
# Resolve package root.
# ----------------------------------------------------------------------

override=os.environ.get("SVF_D0259_PACKAGE_DIR")

if override:
    pkg=Path(override)
else:
    pkg=REPO / PKG_REL

primary_path=pkg / PRIMARY_NAME
scope_path=pkg / SCOPE_NAME
self_path=pkg / SELF_NAME
manifest_path=pkg / MANIFEST_NAME

for p in (
    primary_path,
    scope_path,
    self_path,
    manifest_path,
):
    if not p.is_file():
        die("missing D0259 package file: " + str(p))

# ----------------------------------------------------------------------
# Frozen D0258 package bindings.
# ----------------------------------------------------------------------

if git("rev-parse", f"{D0258_COMMIT}^{{tree}}") != D0258_TREE:
    die("D0258 tree mismatch")

if sha(D0258_PRIMARY) != D0258_PRIMARY_SHA:
    die("D0258 primary SHA mismatch")

if sha(D0258_MANIFEST) != D0258_MANIFEST_SHA:
    die("D0258 manifest SHA mismatch")

# ----------------------------------------------------------------------
# Parse D0258 / D0254 metadata only.
# ----------------------------------------------------------------------

d8=json.loads(
    D0258_PRIMARY.read_text(encoding="utf-8"),
    object_pairs_hook=no_dup,
)

d4=json.loads(
    D0254_PRIMARY.read_text(encoding="utf-8"),
    object_pairs_hook=no_dup,
)

rows=d8["candidate_assessments"]

if [x["candidate_index"] for x in rows] != INDICES:
    die("D0258 candidate order mismatch")

d4rows=[
    x for x in d4["candidate_adjudications"]
    if x["candidate_index"] in INDICES
]

if [x["candidate_index"] for x in d4rows] != INDICES:
    die("D0254 candidate order mismatch")

mapping_fields=[
    "candidate_index",
    "root_id",
    "source_locator",
    "snapshot_path",
    "snapshot_sha256",
    "snapshot_byte_count",
    "snapshot_git_blob_oid",
]

snapshot_binding=[
    {k:r[k] for k in mapping_fields}
    for r in rows
]

for r8,r4 in zip(rows,d4rows):
    for k in mapping_fields:
        if r8[k] != r4[k]:
            die(
                "D0258/D0254 mapping mismatch candidate "
                + str(r8["candidate_index"])
                + " field "
                + k
            )

result_profile=[
    {
        "candidate_index":
            r["candidate_index"],
        "content_decode_status":
            r["content_decode_status"],
        "full_snapshot_bounded_review_completed":
            r["full_snapshot_bounded_review_completed"],
        "positional_inference_evidence_sufficiency_result":
            r["positional_inference_evidence_sufficiency_result"],
        "new_bounded_evidence_required":
            r["new_bounded_evidence_required"],
        "later_positional_successor_adjudication_eligible":
            r["later_positional_successor_adjudication_eligible"],
    }
    for r in rows
]

evidence_profile=[
    {
        "candidate_index":r["candidate_index"],
        "evidence_references":r["evidence_references"],
    }
    for r in rows
]

rationale_profile=[
    {
        "candidate_index":r["candidate_index"],
        "bounded_rationale":r["bounded_rationale"],
    }
    for r in rows
]

if canonical_hash(snapshot_binding) != SNAPSHOT_BINDING_SHA:
    die("snapshot binding hash mismatch")

if canonical_hash(result_profile) != RESULT_PROFILE_SHA:
    die("recorded result profile hash mismatch")

if canonical_hash(evidence_profile) != EVIDENCE_SHA:
    die("recorded evidence hash mismatch")

if canonical_hash(rationale_profile) != RATIONALE_SHA:
    die("recorded rationale hash mismatch")

if canonical_hash(rows) != FULL_ASSESSMENT_SHA:
    die("full D0258 assessment hash mismatch")

if sum(len(x["evidence_references"]) for x in rows) != 10:
    die("recorded evidence-reference count mismatch")

# ----------------------------------------------------------------------
# D0259 primary canonicalization / semantics.
# ----------------------------------------------------------------------

raw=primary_path.read_bytes()

record=json.loads(
    raw.decode("utf-8"),
    object_pairs_hook=no_dup,
)

if raw != canonical(record):
    die("D0259 primary is not canonical JSON")

if raw.endswith(b"\n"):
    die("D0259 primary has final LF")

if record["authorization_role"] != (
    "D0258_FULL_RESULT_INDEPENDENT_CONTENT_AND_"
    "SUFFICIENCY_REVALIDATION_AUTHORIZATION_ONLY"
):
    die("authorization role mismatch")

if record["authorization_target"] != "D0260":
    die("authorization target mismatch")

binding=record["d0258_binding"]

if binding["commit"] != D0258_COMMIT:
    die("D0258 commit binding mismatch")

if binding["tree"] != D0258_TREE:
    die("D0258 tree binding mismatch")

if binding["primary_sha256"] != D0258_PRIMARY_SHA:
    die("D0258 primary binding mismatch")

if binding["manifest_sha256"] != D0258_MANIFEST_SHA:
    die("D0258 manifest binding mismatch")

if binding["full_result_revalidation_necessity"] != "ESTABLISHED":
    die("revalidation necessity mismatch")

if binding["verified_frozen"] is not False:
    die("D0258 must remain not frozen")

inputs=record["input_universe_binding"]

if inputs["candidate_count"] != 9:
    die("candidate count mismatch")

if inputs["candidate_indices"] != INDICES:
    die("candidate index mismatch")

if inputs["snapshot_bindings"] != snapshot_binding:
    die("snapshot mapping mismatch")

if inputs["snapshot_binding_universe_sha256"] != SNAPSHOT_BINDING_SHA:
    die("snapshot binding SHA mismatch")

if inputs["recorded_d0258_result_profile_sha256"] != RESULT_PROFILE_SHA:
    die("result profile SHA mismatch")

if inputs[
    "recorded_d0258_evidence_reference_universe_sha256"
] != EVIDENCE_SHA:
    die("evidence universe SHA mismatch")

if inputs["recorded_d0258_rationale_profile_sha256"] != RATIONALE_SHA:
    die("rationale profile SHA mismatch")

if inputs[
    "full_d0258_candidate_assessment_universe_sha256"
] != FULL_ASSESSMENT_SHA:
    die("full assessment SHA mismatch")

if inputs["recorded_d0258_evidence_reference_count"] != 10:
    die("evidence-reference count mismatch")

auth=record["authorized_operations"]

if auth["read_exact_bound_frozen_d0251_snapshots"] is not True:
    die("D0260 snapshot read not authorized")

if auth["snapshot_read_authorized_for"] != "D0260_ONLY":
    die("snapshot read target mismatch")

if auth["maximum_primary_read_count_per_candidate"] != 1:
    die("per-candidate read maximum mismatch")

if auth["successful_total_primary_snapshot_read_count"] != 9:
    die("successful read count mismatch")

ind=record["independence_contract"]

if ind[
    "recorded_d0258_candidate_result_access_before_all_9_independent_assessments_recorded"
] is not False:
    die("anti-bias result gate mismatch")

if ind[
    "recorded_d0258_candidate_evidence_reference_access_before_all_9_independent_assessments_recorded"
] is not False:
    die("anti-bias evidence gate mismatch")

if ind[
    "recorded_d0258_candidate_bounded_rationale_access_before_all_9_independent_assessments_recorded"
] is not False:
    die("anti-bias rationale gate mismatch")

if ind["comparison_gate"] != (
    "ALL_9_INDEPENDENT_ASSESSMENTS_DURABLY_RECORDED"
):
    die("comparison gate mismatch")

prohib=record["prohibited_operations"]

required_true=[
    "reexecute_d0258_primary_assessment",
    "mutate_d0258_primary",
    "mutate_d0254_frozen_statuses",
    "assign_positional_required_or_not_required",
    "reclassify_class06",
    "reopen_original_source_blobs",
    "read_original_candidate_worktree_paths",
    "follow_references",
    "search_repository",
    "search_git_history_for_source_evidence",
    "network_access",
    "execute_or_import_snapshot_python",
    "use_other_candidate_content_as_evidence",
    "authorize_c4",
    "authorize_c5",
    "authorize_c6",
    "authorize_b2",
]

for key in required_true:
    if prohib[key] is not True:
        die("prohibition not locked: " + key)

execution=record["execution_contract"]

if execution["designated_execution_decision"] != "D0260":
    die("designated execution mismatch")

if execution["candidate_order"] != INDICES:
    die("execution candidate order mismatch")

if execution["successful_snapshot_read_count"] != 9:
    die("successful snapshot read count mismatch")

if execution["maximum_snapshot_read_count_per_candidate"] != 1:
    die("max snapshot read count mismatch")

if execution["expected_execution_trace_record_count"] != 45:
    die("trace count contract mismatch")

if execution["automatic_reexecution_after_any_snapshot_read"] is not False:
    die("automatic reexecution must be false")

if execution["automatic_snapshot_reread_after_any_snapshot_read"] is not False:
    die("automatic reread must be false")

results=record["results"]

if results["authorization_created"] is not True:
    die("authorization-created state mismatch")

if results["d0260_revalidation_authorized"] is not True:
    die("D0260 authorization state mismatch")

if results["d0260_revalidation_executed"] is not False:
    die("D0260 execution state mismatch")

if results["d0258_verified_frozen"] is not False:
    die("D0258 freeze state mismatch")

if results["post_d0258_branch_authorized"] is not False:
    die("post-D0258 branch state mismatch")

for key in (
    "c4_authorized",
    "c5_authorized",
    "c6_authorized",
    "b2_authorized",
):
    if results[key] is not False:
        die("downstream authorization leakage: " + key)

if record["next_required_checkpoint"] != (
    "INDEPENDENT_READ_ONLY_VERIFY_D0259_BEFORE_ANY_D0260_"
    "SNAPSHOT_CONTENT_READ"
):
    die("next checkpoint mismatch")

# ----------------------------------------------------------------------
# Exact 3-entry manifest.
# ----------------------------------------------------------------------

manifest_lines=[
    x for x in manifest_path.read_text(
        encoding="utf-8"
    ).splitlines()
    if x.strip()
]

if len(manifest_lines) != 3:
    die("manifest entry count mismatch")

manifest={}

for line in manifest_lines:
    parts=line.split("  ", 1)

    if len(parts) != 2:
        die("invalid manifest line")

    digest,name=parts

    if len(digest) != 64:
        die("invalid manifest digest")

    if name in manifest:
        die("duplicate manifest name")

    manifest[name]=digest

if set(manifest) != EXPECTED_MANIFEST_NAMES:
    die("manifest member set mismatch")

for name,digest in manifest.items():
    if sha(pkg / name) != digest:
        die("manifest member SHA mismatch: " + name)

# ----------------------------------------------------------------------
# Postcommit bounded provenance / descendant-rerunnable checks.
# ----------------------------------------------------------------------

preinstall=os.environ.get("SVF_D0259_PREINSTALL") == "1"

if not preinstall:
    record_rel=str(PKG_REL / PRIMARY_NAME)

    commits=[
        x for x in git(
            "log",
            "--diff-filter=A",
            "--format=%H",
            "--",
            record_rel,
        ).splitlines()
        if x.strip()
    ]

    if len(commits) != 1:
        die("unable to uniquely identify D0259 introduction commit")

    d0259_commit=commits[0]

    if git("log", "-1", "--format=%s", d0259_commit) != EXPECTED_SUBJECT:
        die("D0259 subject mismatch")

    if git("rev-parse", f"{d0259_commit}^") != D0258_COMMIT:
        die("D0259 parent mismatch")

    subprocess.check_call(
        [
            "git",
            "merge-base",
            "--is-ancestor",
            d0259_commit,
            "HEAD",
        ],
        cwd=REPO,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    committed_paths=[
        x for x in git(
            "diff-tree",
            "--no-commit-id",
            "--name-only",
            "-r",
            d0259_commit,
        ).splitlines()
        if x.strip()
    ]

    expected_paths=sorted([
        str(PKG_REL / PRIMARY_NAME),
        str(PKG_REL / SCOPE_NAME),
        str(PKG_REL / SELF_NAME),
        str(PKG_REL / MANIFEST_NAME),
        str(DECISION_REL),
    ])

    if sorted(committed_paths) != expected_paths:
        die("D0259 committed scope mismatch")

    # D0259 files must remain byte-identical in descendants.
    for rel in expected_paths:
        intro_oid=git("rev-parse", f"{d0259_commit}:{rel}")
        head_oid=git("rev-parse", f"HEAD:{rel}")

        if intro_oid != head_oid:
            die("D0259 artifact changed in descendant: " + rel)

print("D0259_FULL_RESULT_REVALIDATION_AUTHORIZATION_VERIFIER=PASS")
print("D0258_FROZEN_PROVENANCE_BINDING=PASS")
print("D0259_SNAPSHOT_INPUT_UNIVERSE_BINDING=PASS")
print("D0259_RECORDED_D0258_RESULT_PROFILE_BINDING=PASS")
print("D0259_RECORDED_D0258_EVIDENCE_BINDING=PASS")
print("D0259_RECORDED_D0258_RATIONALE_BINDING=PASS")
print("D0259_AUTHORIZATION_SEMANTICS=PASS")
print("D0259_INDEPENDENCE_GATE=PASS")
print("D0260_REVALIDATION_AUTHORIZED=YES")
print("D0260_REVALIDATION_EXECUTED=NO")
print("D0260_EXECUTION_ALLOWED_BEFORE_INDEPENDENT_D0259_CHECKPOINT=NO")
print("D0251_SNAPSHOT_CONTENT_READ_BY_D0259_VERIFIER=NO")
print("D0258_PRIMARY_ASSESSMENT_EXECUTED_BY_D0259_VERIFIER=NO")
print("D0258_SAFE_VERIFIER_EXECUTED_BY_D0259_VERIFIER=NO")
print("C4_AUTHORIZED=NO")
print("C5_AUTHORIZED=NO")
print("C6_AUTHORIZED=NO")
print("B2_AUTHORIZED=NO")
print("SAFE_D0259_VERIFIER=PASS")
