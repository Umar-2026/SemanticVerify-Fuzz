#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import os
import re
import subprocess

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
    "d0260_d0258_full_result_independent_content_and_"
    "sufficiency_revalidation_execution_v1"
)

DECISION_REL=Path(
    "documentation/decisions/"
    "0260-execute-d0258-full-result-independent-content-and-"
    "sufficiency-revalidation.md"
)

D0259_COMMIT="9165778571f8f1f6ad1a6e8888562b6e7374cb62"
D0259_TREE="163c26d30a4a0e82526cca2ba9eae8c5b46a64ee"
D0259_RECORD_SHA="aec7d8e17092ee004411a6dfb43366669c636893efeb3c5294844e6cc0c4ab24"
D0259_MANIFEST_SHA="65be220d9703578e46b3d01de0589170a5f61e4539477b17c4952b85fc3fb800"

D0258_COMMIT="15afca914011851d516a05976e4d2d61c586f9d4"
D0258_TREE="622b95b7c9daba7659ceec08e75c90832d5a4dae"
D0258_PRIMARY_SHA="4aa389ad41c3a532c61c3b38aa397da6dccebb96d3384bb6a22d1e0af6462e60"
D0258_MANIFEST_SHA="7a7f534d54c68aca01784d2a611f7875b674c7d58401c9223c9cc8141fd4f895"

SNAPSHOT_BINDING_SHA="51afc6fda72397cebde135eb8762a1269ffd7acdbe32d5941abbf4db220d23b3"
RESULT_PROFILE_SHA="8a565bebd1a6a26112ccdd9d2b34db56f714d3892441cc9a1632da7662884b73"
EVIDENCE_SHA="d9e1ec6d28a32b7477f472fb91a19c93c60c63b6c23e8ddbe4d467cac5e86a11"
RATIONALE_SHA="abb35982ec168b82b696244c24c6f1d58ad2f3096cc6878478f3e69516f496ce"
FULL_ASSESSMENT_SHA="1767e05713cd6b35c9bb6df8bfad65b97e9c95553cc6da71174cebb62b5e861f"

D0259_PKG=REPO / BASE / (
    "d0259_d0258_full_result_independent_content_and_"
    "sufficiency_revalidation_authorization_v1"
)

D0259_RECORD=D0259_PKG / (
    "01_d0258_full_result_independent_content_and_"
    "sufficiency_revalidation_authorization.v1.json"
)

D0259_MANIFEST=D0259_PKG / (
    "04_d0258_full_result_independent_content_and_"
    "sufficiency_revalidation_authorization.v1.SHA256SUMS"
)

D0258_PKG=REPO / BASE / (
    "d0258_bounded_positional_inference_evidence_sufficiency_"
    "assessment_execution_v1"
)

D0258_PRIMARY=D0258_PKG / (
    "01_bounded_positional_inference_evidence_sufficiency_"
    "assessment_execution.v1.json"
)

D0258_MANIFEST=D0258_PKG / (
    "05_bounded_positional_inference_evidence_sufficiency_"
    "assessment_execution.v1.SHA256SUMS"
)

PRIMARY_NAME=(
    "01_d0258_full_result_independent_content_and_"
    "sufficiency_revalidation_execution.v1.json"
)

SCOPE_NAME=(
    "02_d0258_full_result_independent_content_and_"
    "sufficiency_revalidation_execution_scope.v1.md"
)

TRACE_NAME=(
    "03_d0258_full_result_independent_content_and_"
    "sufficiency_revalidation_execution_trace.v1.jsonl"
)

SELF_NAME=(
    "04_verify_d0258_full_result_independent_content_and_"
    "sufficiency_revalidation_execution.v1.py"
)

MANIFEST_NAME=(
    "05_d0258_full_result_independent_content_and_"
    "sufficiency_revalidation_execution.v1.SHA256SUMS"
)

EXPECTED_MANIFEST_NAMES={
    PRIMARY_NAME,
    SCOPE_NAME,
    TRACE_NAME,
    SELF_NAME,
}

EXPECTED_SUBJECT=(
    "decision: execute D0258 full-result independent content "
    "and sufficiency revalidation"
)

INDICES=[1,2,3,5,6,7,8,9,10]

SUF="FROZEN_SNAPSHOT_EVIDENCE_SUFFICIENT_FOR_SEPARATE_POSITIONAL_ADJUDICATION"
INS="FROZEN_SNAPSHOT_EVIDENCE_INSUFFICIENT_NEW_BOUNDED_EVIDENCE_REQUIRED"
IND="SUFFICIENCY_REMAINS_INDETERMINATE"

MATCH="REVALIDATION_MATCH"
MISMATCH="REVALIDATION_MISMATCH"
RIND="REVALIDATION_INDETERMINATE"

VALIDATION_ENUM={
    "VALID",
    "INVALID",
    "NOT_APPLICABLE",
    "INDETERMINATE",
}

LINE_RE=re.compile(r"^L([1-9][0-9]*)-L([1-9][0-9]*)$")
BYTE_RE=re.compile(r"^([0-9]+):([0-9]+)$")

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

override=os.environ.get("SVF_D0260_PACKAGE_DIR")

if override:
    pkg=Path(override)
else:
    pkg=REPO / PKG_REL

primary_path=pkg / PRIMARY_NAME
scope_path=pkg / SCOPE_NAME
trace_path=pkg / TRACE_NAME
self_path=pkg / SELF_NAME
manifest_path=pkg / MANIFEST_NAME

for p in (
    primary_path,
    scope_path,
    trace_path,
    self_path,
    manifest_path,
):
    if not p.is_file():
        die("missing D0260 package file: " + str(p))

# ----------------------------------------------------------------------
# Upstream immutable bindings.
# ----------------------------------------------------------------------

if git("rev-parse", f"{D0259_COMMIT}^{{tree}}") != D0259_TREE:
    die("D0259 tree mismatch")

if git("rev-parse", f"{D0258_COMMIT}^{{tree}}") != D0258_TREE:
    die("D0258 tree mismatch")

if sha(D0259_RECORD) != D0259_RECORD_SHA:
    die("D0259 record SHA mismatch")

if sha(D0259_MANIFEST) != D0259_MANIFEST_SHA:
    die("D0259 manifest SHA mismatch")

if sha(D0258_PRIMARY) != D0258_PRIMARY_SHA:
    die("D0258 primary SHA mismatch")

if sha(D0258_MANIFEST) != D0258_MANIFEST_SHA:
    die("D0258 manifest SHA mismatch")

# ----------------------------------------------------------------------
# Recompute D0258 recorded-result metadata domains.
# ----------------------------------------------------------------------

d8=json.loads(
    D0258_PRIMARY.read_text(encoding="utf-8"),
    object_pairs_hook=no_dup,
)

rows=d8["candidate_assessments"]

if [x["candidate_index"] for x in rows] != INDICES:
    die("D0258 candidate order mismatch")

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
    die("snapshot-binding hash mismatch")

if canonical_hash(result_profile) != RESULT_PROFILE_SHA:
    die("D0258 result-profile hash mismatch")

if canonical_hash(evidence_profile) != EVIDENCE_SHA:
    die("D0258 evidence-profile hash mismatch")

if canonical_hash(rationale_profile) != RATIONALE_SHA:
    die("D0258 rationale-profile hash mismatch")

if canonical_hash(rows) != FULL_ASSESSMENT_SHA:
    die("D0258 full-assessment hash mismatch")

recorded_by_idx={x["candidate_index"]:x for x in rows}

# ----------------------------------------------------------------------
# D0260 primary canonicalization.
# ----------------------------------------------------------------------

raw=primary_path.read_bytes()

primary=json.loads(
    raw.decode("utf-8"),
    object_pairs_hook=no_dup,
)

if raw != canonical(primary):
    die("D0260 primary not canonical JSON")

if raw.endswith(b"\n"):
    die("D0260 primary has final LF")

if primary["revalidation_id"] != (
    "D0260-D0258-FULL-RESULT-INDEPENDENT-CONTENT-AND-"
    "SUFFICIENCY-REVALIDATION-V1"
):
    die("revalidation id mismatch")

auth=primary["authorization_binding"]

if auth["d0259_commit"] != D0259_COMMIT:
    die("D0259 commit binding mismatch")

if auth["d0259_tree"] != D0259_TREE:
    die("D0259 tree binding mismatch")

binding=primary["d0258_recorded_result_binding"]

if binding["d0258_commit"] != D0258_COMMIT:
    die("D0258 commit binding mismatch")

if binding["d0258_tree"] != D0258_TREE:
    die("D0258 tree binding mismatch")

if binding["recorded_result_profile_sha256"] != RESULT_PROFILE_SHA:
    die("recorded result hash binding mismatch")

if binding["recorded_evidence_reference_universe_sha256"] != EVIDENCE_SHA:
    die("recorded evidence hash binding mismatch")

if binding["recorded_rationale_profile_sha256"] != RATIONALE_SHA:
    die("recorded rationale hash binding mismatch")

inputs=primary["snapshot_input_universe_binding"]

if inputs["candidate_count"] != 9:
    die("candidate count mismatch")

if inputs["candidate_indices"] != INDICES:
    die("candidate indices mismatch")

if inputs["snapshot_bindings"] != snapshot_binding:
    die("snapshot mapping mismatch")

if inputs["snapshot_binding_universe_sha256"] != SNAPSHOT_BINDING_SHA:
    die("snapshot mapping hash mismatch")

independence=primary["independence_contract"]

if independence["blind_candidate_count"] != 9:
    die("blind count mismatch")

if independence["blind_candidate_order"] != INDICES:
    die("blind candidate order mismatch")

blind_sha=independence["blind_assessment_record_sha256"]

if not re.fullmatch(r"[0-9a-f]{64}", blind_sha):
    die("invalid blind-record SHA")

if independence[
    "recorded_d0258_candidate_result_access_before_all_blind_assessments"
] is not False:
    die("anti-bias result gate mismatch")

if independence[
    "recorded_d0258_evidence_access_before_all_blind_assessments"
] is not False:
    die("anti-bias evidence gate mismatch")

if independence[
    "recorded_d0258_rationale_access_before_all_blind_assessments"
] is not False:
    die("anti-bias rationale gate mismatch")

# ----------------------------------------------------------------------
# Candidate records.
# ----------------------------------------------------------------------

cands=primary["candidate_revalidations"]

if [x["candidate_index"] for x in cands] != INDICES:
    die("D0260 candidate order mismatch")

if len(cands) != 9:
    die("D0260 candidate count mismatch")

expected_fields={
    "candidate_index",
    "root_id",
    "source_locator",
    "snapshot_path",
    "snapshot_sha256",
    "snapshot_byte_count",
    "snapshot_git_blob_oid",
    "content_decode_status",
    "full_snapshot_independent_review_completed",
    "independent_sufficiency_result",
    "independent_evidence_references",
    "independent_bounded_rationale",
    "recorded_d0258_sufficiency_result",
    "recorded_d0258_evidence_reference_count",
    "recorded_d0258_evidence_reference_validation_status",
    "revalidation_comparison_result",
    "comparison_rationale",
}

matches=0
mismatches=0
rinds=0

for rec,mapping in zip(cands,snapshot_binding):
    if set(rec) != expected_fields:
        die("candidate field set mismatch")

    idx=rec["candidate_index"]
    recorded=recorded_by_idx[idx]

    for key in mapping_fields:
        if rec[key] != mapping[key]:
            die(f"candidate {idx} mapping mismatch {key}")

    ind_result=rec["independent_sufficiency_result"]

    if ind_result not in {SUF,INS,IND}:
        die("invalid independent result")

    recorded_result=rec["recorded_d0258_sufficiency_result"]

    if recorded_result != recorded[
        "positional_inference_evidence_sufficiency_result"
    ]:
        die("recorded D0258 result mismatch")

    if rec["recorded_d0258_evidence_reference_count"] != len(
        recorded["evidence_references"]
    ):
        die("recorded evidence-reference count mismatch")

    validation=rec[
        "recorded_d0258_evidence_reference_validation_status"
    ]

    if validation not in VALIDATION_ENUM:
        die("invalid evidence validation enum")

    for ref in rec["independent_evidence_references"]:
        if set(ref) != {
            "evidence_purpose",
            "locator_kind",
            "locator_value",
        }:
            die("invalid independent evidence reference fields")

        kind=ref["locator_kind"]
        value=ref["locator_value"]

        if kind == "LINE_RANGE":
            if LINE_RE.fullmatch(value) is None:
                die("invalid line-range grammar")

        elif kind == "BYTE_RANGE":
            if BYTE_RE.fullmatch(value) is None:
                die("invalid byte-range grammar")

        elif kind == "JSON_POINTER":
            if not (value == "" or value.startswith("/")):
                die("invalid JSON pointer grammar")

        else:
            die("invalid locator kind")

    comparison=rec["revalidation_comparison_result"]

    if ind_result != recorded_result:
        expected=MISMATCH

    elif recorded_result == SUF:
        if validation == "VALID":
            expected=MATCH
        elif validation == "INVALID":
            expected=MISMATCH
        else:
            expected=RIND

    else:
        expected=MATCH

    if comparison != expected:
        die(
            f"comparison formula mismatch candidate {idx}: "
            f"{comparison} != {expected}"
        )

    if comparison == MATCH:
        matches += 1
    elif comparison == MISMATCH:
        mismatches += 1
    elif comparison == RIND:
        rinds += 1
    else:
        die("invalid comparison enum")

summary=primary["revalidation_summary"]

if summary != {
    "candidate_count":9,
    "match_count":matches,
    "mismatch_count":mismatches,
    "indeterminate_count":rinds,
}:
    die("summary mismatch")

if matches + mismatches + rinds != 9:
    die("summary invariant mismatch")

results=primary["results"]

expected_all_match=(
    matches == 9
    and mismatches == 0
    and rinds == 0
)

if results["independent_revalidation_executed"] is not True:
    die("revalidation execution state mismatch")

if results["all_nine_candidates_revalidation_match"] != expected_all_match:
    die("all-match state mismatch")

if results["d0258_primary_results_verified_frozen"] is not False:
    die("D0258 primary freeze state must remain false")

if results["d0258_verified_frozen"] is not False:
    die("D0258 freeze state must remain false")

if results["post_d0258_branch_authorized"] is not False:
    die("post-D0258 branch must remain unauthorized")

for key in (
    "c4_authorized",
    "c5_authorized",
    "c6_authorized",
    "b2_authorized",
):
    if results[key] is not False:
        die("downstream authorization leakage: " + key)

if primary["next_required_checkpoint"] != (
    "INDEPENDENT_READ_ONLY_VERIFY_D0260_REVALIDATION_EXECUTION_"
    "WITHOUT_SNAPSHOT_REREAD"
):
    die("next checkpoint mismatch")

# ----------------------------------------------------------------------
# Exact 45-record trace / anti-bias structure.
# ----------------------------------------------------------------------

trace=[]

for line in trace_path.read_text(encoding="utf-8").splitlines():
    if not line.strip():
        continue

    trace.append(
        json.loads(
            line,
            object_pairs_hook=no_dup,
        )
    )

if len(trace) != 45:
    die("trace record count mismatch")

# First 36 = four blind stages per candidate.
for n,idx in enumerate(INDICES):
    group=trace[n*4:(n+1)*4]

    if len(group) != 4:
        die("blind trace group length mismatch")

    expected_states=[
        (True,False,False,False,False,False),
        (True,True,False,False,False,False),
        (True,True,True,False,False,False),
        (True,True,True,True,False,False),
    ]

    for rec,state in zip(group,expected_states):
        if rec["candidate_index"] != idx:
            die("blind trace candidate order mismatch")

        actual=(
            rec["snapshot_read_completed"],
            rec["snapshot_identity_verified"],
            rec["independent_review_completed"],
            rec["independent_assessment_recorded"],
            rec["recorded_d0258_result_accessed"],
            rec["comparison_recorded"],
        )

        if actual != state:
            die(f"blind trace progression mismatch candidate {idx}")

        if "blind_assessment_record_sha256" in rec:
            die("blind SHA appeared before comparison gate")

# Last nine = comparison stage.
comparison_trace=trace[36:]

if [x["candidate_index"] for x in comparison_trace] != INDICES:
    die("comparison trace order mismatch")

for rec in comparison_trace:
    actual=(
        rec["snapshot_read_completed"],
        rec["snapshot_identity_verified"],
        rec["independent_review_completed"],
        rec["independent_assessment_recorded"],
        rec["recorded_d0258_result_accessed"],
        rec["comparison_recorded"],
    )

    if actual != (True,True,True,True,True,True):
        die("comparison trace state mismatch")

    if rec.get("blind_assessment_record_sha256") != blind_sha:
        die("comparison trace blind SHA mismatch")

# ----------------------------------------------------------------------
# Manifest.
# ----------------------------------------------------------------------

manifest_lines=[
    x for x in manifest_path.read_text(
        encoding="utf-8"
    ).splitlines()
    if x.strip()
]

if len(manifest_lines) != 4:
    die("manifest count mismatch")

manifest={}

for line in manifest_lines:
    parts=line.split("  ",1)

    if len(parts) != 2:
        die("invalid manifest line")

    digest,name=parts

    if name in manifest:
        die("duplicate manifest member")

    manifest[name]=digest

if set(manifest) != EXPECTED_MANIFEST_NAMES:
    die("manifest member set mismatch")

for name,digest in manifest.items():
    if sha(pkg / name) != digest:
        die("manifest SHA mismatch: " + name)

# ----------------------------------------------------------------------
# Descendant-rerunnable postcommit provenance.
# ----------------------------------------------------------------------

preinstall=os.environ.get("SVF_D0260_PREINSTALL") == "1"

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
        die("unable to identify unique D0260 introduction commit")

    d0260_commit=commits[0]

    if git("log","-1","--format=%s",d0260_commit) != EXPECTED_SUBJECT:
        die("D0260 subject mismatch")

    if git("rev-parse",f"{d0260_commit}^") != D0259_COMMIT:
        die("D0260 parent mismatch")

    subprocess.check_call(
        [
            "git",
            "merge-base",
            "--is-ancestor",
            d0260_commit,
            "HEAD",
        ],
        cwd=REPO,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    expected_paths=sorted([
        str(PKG_REL / PRIMARY_NAME),
        str(PKG_REL / SCOPE_NAME),
        str(PKG_REL / TRACE_NAME),
        str(PKG_REL / SELF_NAME),
        str(PKG_REL / MANIFEST_NAME),
        str(DECISION_REL),
    ])

    committed_paths=[
        x for x in git(
            "diff-tree",
            "--no-commit-id",
            "--name-only",
            "-r",
            d0260_commit,
        ).splitlines()
        if x.strip()
    ]

    if sorted(committed_paths) != expected_paths:
        die("D0260 committed scope mismatch")

    for rel in expected_paths:
        intro_oid=git("rev-parse",f"{d0260_commit}:{rel}")
        head_oid=git("rev-parse",f"HEAD:{rel}")

        if intro_oid != head_oid:
            die("D0260 artifact changed in descendant: " + rel)

print("D0260_FULL_RESULT_REVALIDATION_EXECUTION_VERIFIER=PASS")
print("D0259_AUTHORIZATION_BINDING=PASS")
print("D0258_RECORDED_RESULT_BINDING=PASS")
print("D0260_SNAPSHOT_MAPPING_UNIVERSE_BINDING=PASS")
print("D0260_RECORDED_RESULT_PROFILE_BINDING=PASS")
print("D0260_RECORDED_EVIDENCE_PROFILE_BINDING=PASS")
print("D0260_RECORDED_RATIONALE_PROFILE_BINDING=PASS")
print("D0260_PRIMARY_JSON_CANONICALIZATION=PASS")
print("D0260_EXACT_NINE_CANDIDATE_RECORDS=PASS")
print("D0260_COMPARISON_FORMULA_CONSISTENCY=PASS")
print("D0260_SUMMARY_COUNTS=PASS")
print("D0260_TRACE_RECORD_COUNT_45=PASS")
print("D0260_ANTI_BIAS_TRACE_GATE=PASS")
print("D0251_SNAPSHOT_CONTENT_READ_BY_D0260_SAFE_VERIFIER=NO")
print("D0258_PRIMARY_ASSESSMENT_REEXECUTED_BY_D0260_SAFE_VERIFIER=NO")
print("D0258_SAFE_VERIFIER_EXECUTED_BY_D0260_SAFE_VERIFIER=NO")
print("D0254_SAFE_VERIFIER_EXECUTED_BY_D0260_SAFE_VERIFIER=NO")
print("D0260_SAFE_VERIFIER_REJUDGED_SUFFICIENCY=NO")
print("D0260_SAFE_VERIFIER_ASSIGNED_POSITIONAL_STATUS=NO")
print("D0260_SAFE_VERIFIER_RECLASSIFIED_CLASS06=NO")
print("D0258_VERIFIED_FROZEN=NO")
print("POST_D0258_BRANCH_AUTHORIZED=NO")
print("C4_AUTHORIZED=NO")
print("C5_AUTHORIZED=NO")
print("C6_AUTHORIZED=NO")
print("B2_AUTHORIZED=NO")
print("SAFE_D0260_VERIFIER=PASS")
