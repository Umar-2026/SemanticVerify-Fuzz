#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import os
import re
import subprocess
import sys

REPO = Path(os.environ.get(
    "SVF_REPO_ROOT",
    "/openbayes/home/semanticverify-fuzz-research"
))

BASE = Path(
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2"
)

PKG_REL = BASE / (
    "d0258_bounded_positional_inference_"
    "evidence_sufficiency_assessment_execution_v1"
)

PRIMARY_NAME = (
    "01_bounded_positional_inference_evidence_"
    "sufficiency_assessment_execution.v1.json"
)
SCOPE_NAME = (
    "02_bounded_positional_inference_evidence_"
    "sufficiency_assessment_execution_scope.v1.md"
)
TRACE_NAME = (
    "03_bounded_positional_inference_evidence_"
    "sufficiency_assessment_execution_trace.v1.jsonl"
)
SELF_NAME = (
    "04_verify_bounded_positional_inference_evidence_"
    "sufficiency_assessment_execution.v1.py"
)
MANIFEST_NAME = (
    "05_bounded_positional_inference_evidence_"
    "sufficiency_assessment_execution.v1.SHA256SUMS"
)

D0257_COMMIT = "2667da432cca867a43ca66223c61c73c6bf56e7c"
D0257_TREE = "a6364afd8ecadade7b68062ef33c283d35bddbd8"

D0256_COMMIT = "042a3fdc13936ee1e879bcd077ebe2d8ac2fbc75"
D0256_TREE = "b161bc485f544ed460be15719302b04cee1a126d"

D0254_COMMIT = "5cfbbe57ad4fa5c00174137dd19d003be737d29c"
D0254_TREE = "6e1abfc1bfdb1a405b7e6594c4b77a395387cb19"
D0254_PRIMARY_SHA = "8ee9bf4b84412d1bddf86da60aa2e947e5b7c44ac9d2dfe1d539af126023f3d0"

NINE_BINDING_SHA = "51afc6fda72397cebde135eb8762a1269ffd7acdbe32d5941abbf4db220d23b3"
NINE_STATUS_SHA = "3342ab3e560f3a47290bb83ad93e34f9e834623470e229fad84bcd86a92989eb"
NINE_EVIDENCE_SHA = "a5c534b13dca61719e8dca903ae6fe3214b719d52926b8cfd4620e6a7be9e4ae"

D0254_PRIMARY = REPO / BASE / (
    "d0254_c3_bounded_candidate_content_adjudication_execution_v1/"
    "01_c3_bounded_candidate_content_adjudication_execution.v1.json"
)

preinstall = os.environ.get("SVF_D0258_PREINSTALL") == "1"

if preinstall:
    pkg = Path(os.environ["SVF_D0258_PACKAGE_ROOT"])
else:
    pkg = REPO / PKG_REL

primary_path = pkg / PRIMARY_NAME
scope_path = pkg / SCOPE_NAME
trace_path = pkg / TRACE_NAME
self_path = pkg / SELF_NAME
manifest_path = pkg / MANIFEST_NAME

def run_git(*args):
    cp = subprocess.run(
        ["git", *args],
        cwd=REPO,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert cp.returncode == 0, cp.stderr
    return cp.stdout.strip()

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def no_dup(pairs):
    out={}
    for k,v in pairs:
        assert k not in out
        out[k]=v
    return out

def canonical_bytes(x):
    return json.dumps(
        x,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")

def canon_sha(x):
    return hashlib.sha256(canonical_bytes(x)).hexdigest()

# ------------------------------------------------------------------
# Immutable upstream Git metadata
# ------------------------------------------------------------------

assert run_git("rev-parse", f"{D0257_COMMIT}^{{tree}}") == D0257_TREE
assert run_git("rev-parse", f"{D0256_COMMIT}^{{tree}}") == D0256_TREE
assert run_git("rev-parse", f"{D0254_COMMIT}^{{tree}}") == D0254_TREE

cp=subprocess.run(
    ["git","merge-base","--is-ancestor",D0257_COMMIT,"HEAD"],
    cwd=REPO
)
assert cp.returncode == 0

assert sha(D0254_PRIMARY) == D0254_PRIMARY_SHA

# For committed/postcommit use, identify only the bounded introduction
# commit of this verifier path. This is Git metadata provenance, not
# source-evidence history search.
if not preinstall:
    rel=str(PKG_REL / SELF_NAME)
    intro=run_git("log","--diff-filter=A","-1","--format=%H","--",rel)
    assert intro
    assert run_git("rev-parse",f"{intro}^") == D0257_COMMIT
    assert run_git("log","-1","--format=%s",intro) == (
        "decision: execute bounded positional-inference "
        "evidence-sufficiency assessment from frozen D0251 snapshots"
    )

    cp=subprocess.run(
        ["git","merge-base","--is-ancestor",intro,"HEAD"],
        cwd=REPO
    )
    assert cp.returncode == 0

# ------------------------------------------------------------------
# Package manifest
# ------------------------------------------------------------------

entries={}
for line in manifest_path.read_text(encoding="utf-8").splitlines():
    if not line.strip():
        continue
    digest,name=line.split("  ",1)
    assert name not in entries
    entries[name]=digest

assert set(entries) == {
    PRIMARY_NAME,
    SCOPE_NAME,
    TRACE_NAME,
    SELF_NAME,
}

for name,digest in entries.items():
    assert sha(pkg / name) == digest

# ------------------------------------------------------------------
# D0254 frozen metadata and D0258 input universe
# ------------------------------------------------------------------

d4=json.loads(
    D0254_PRIMARY.read_text(encoding="utf-8"),
    object_pairs_hook=no_dup
)

indices=[1,2,3,5,6,7,8,9,10]

rows=[
    x for x in d4["candidate_adjudications"]
    if x["candidate_index"] in indices
]

assert [x["candidate_index"] for x in rows] == indices

shared=[
    "candidate_index",
    "root_id",
    "source_locator",
    "snapshot_path",
    "snapshot_sha256",
    "snapshot_byte_count",
    "snapshot_git_blob_oid",
]

binding=[{k:r[k] for k in shared} for r in rows]
assert canon_sha(binding) == NINE_BINDING_SHA

required_fields=[
    "requirement_identity_status",
    "semantic_unit_identity_status",
    "explicit_crosswalk_relation_status",
    "version_or_checksum_binding_status",
    "authority_basis_status",
]

status=[]
evmeta=[]

for r in rows:
    neg=[k for k in required_fields if r[k] == "NOT_ESTABLISHED"]
    assert neg

    status.append({
        "candidate_index":r["candidate_index"],
        "positional_inference_status":r["positional_inference_status"],
        "required_not_established_fields":neg,
    })

    evmeta.append({
        "candidate_index":r["candidate_index"],
        "evidence_references":[
            {
                "evidence_purpose":e["evidence_purpose"],
                "locator_kind":e["locator_kind"],
                "locator_value":e["locator_value"],
            }
            for e in r["evidence_references"]
        ],
    })

assert canon_sha(status) == NINE_STATUS_SHA
assert canon_sha(evmeta) == NINE_EVIDENCE_SHA

# ------------------------------------------------------------------
# Primary canonicalization / exact contract
# ------------------------------------------------------------------

raw=primary_path.read_bytes()

obj=json.loads(
    raw.decode("utf-8"),
    object_pairs_hook=no_dup
)

assert raw == canonical_bytes(obj)
assert not raw.endswith(b"\n")

assert obj["assessment_id"] == (
    "D0258-BOUNDED-POSITIONAL-INFERENCE-"
    "EVIDENCE-SUFFICIENCY-ASSESSMENT-V1"
)

assert set(obj) == {
    "assessment_id",
    "authorization_binding",
    "d0254_frozen_result_binding",
    "nine_candidate_input_universe_binding",
    "assessment_contract",
    "candidate_assessments",
    "assessment_summary",
    "execution_boundaries",
    "results",
    "next_required_checkpoint",
}

adjs=obj["candidate_assessments"]

assert len(adjs) == 9
assert [x["candidate_index"] for x in adjs] == indices

expected_fields={
    "candidate_index",
    "root_id",
    "source_locator",
    "snapshot_path",
    "snapshot_sha256",
    "snapshot_byte_count",
    "snapshot_git_blob_oid",
    "frozen_d0254_class06_verdict",
    "frozen_d0254_positional_inference_status",
    "frozen_required_not_established_fields",
    "content_decode_status",
    "full_snapshot_bounded_review_completed",
    "positional_inference_evidence_sufficiency_result",
    "evidence_references",
    "bounded_rationale",
    "new_bounded_evidence_required",
    "later_positional_successor_adjudication_eligible",
}

allowed_results={
    "FROZEN_SNAPSHOT_EVIDENCE_SUFFICIENT_FOR_SEPARATE_POSITIONAL_ADJUDICATION",
    "FROZEN_SNAPSHOT_EVIDENCE_INSUFFICIENT_NEW_BOUNDED_EVIDENCE_REQUIRED",
    "SUFFICIENCY_REMAINS_INDETERMINATE",
}

line_re=re.compile(r"^L([1-9][0-9]*)-L([1-9][0-9]*)$")
byte_re=re.compile(r"^([0-9]+):([0-9]+)$")

for rec, frozen in zip(adjs, rows):
    assert set(rec) == expected_fields

    assert rec["candidate_index"] == frozen["candidate_index"]
    assert rec["root_id"] == frozen["root_id"]
    assert rec["source_locator"] == frozen["source_locator"]
    assert rec["snapshot_path"] == frozen["snapshot_path"]
    assert rec["snapshot_sha256"] == frozen["snapshot_sha256"]
    assert rec["snapshot_byte_count"] == frozen["snapshot_byte_count"]
    assert rec["snapshot_git_blob_oid"] == frozen["snapshot_git_blob_oid"]

    assert rec["frozen_d0254_class06_verdict"] == \
        "INDETERMINATE_UNDER_BOUNDED_EVIDENCE"

    assert rec["frozen_d0254_positional_inference_status"] == "INDETERMINATE"

    expected_neg=[
        k for k in required_fields
        if frozen[k] == "NOT_ESTABLISHED"
    ]
    assert rec["frozen_required_not_established_fields"] == expected_neg

    assert rec["content_decode_status"] in {"DECODED","DECODE_FAILED"}

    result=rec["positional_inference_evidence_sufficiency_result"]
    assert result in allowed_results

    if result == \
        "FROZEN_SNAPSHOT_EVIDENCE_SUFFICIENT_FOR_SEPARATE_POSITIONAL_ADJUDICATION":
        assert rec["new_bounded_evidence_required"] is False
        assert rec["later_positional_successor_adjudication_eligible"] is True
        assert rec["full_snapshot_bounded_review_completed"] is True
        assert len(rec["evidence_references"]) >= 1

    elif result == \
        "FROZEN_SNAPSHOT_EVIDENCE_INSUFFICIENT_NEW_BOUNDED_EVIDENCE_REQUIRED":
        assert rec["new_bounded_evidence_required"] is True
        assert rec["later_positional_successor_adjudication_eligible"] is False
        assert rec["full_snapshot_bounded_review_completed"] is True

    else:
        assert rec["new_bounded_evidence_required"] == "UNRESOLVED"
        assert rec["later_positional_successor_adjudication_eligible"] is False

    for ev in rec["evidence_references"]:
        assert set(ev) == {
            "evidence_purpose",
            "locator_kind",
            "locator_value",
        }

        kind=ev["locator_kind"]
        val=ev["locator_value"]

        assert kind in {"LINE_RANGE","BYTE_RANGE","JSON_POINTER"}

        if kind == "LINE_RANGE":
            m=line_re.match(val)
            assert m
            assert int(m.group(1)) <= int(m.group(2))

        elif kind == "BYTE_RANGE":
            m=byte_re.match(val)
            assert m
            assert int(m.group(1)) < int(m.group(2))

        else:
            assert isinstance(val,str)
            assert val == "" or val.startswith("/")

# ------------------------------------------------------------------
# Summary
# ------------------------------------------------------------------

summary=obj["assessment_summary"]

sufficient=[
    x["candidate_index"] for x in adjs
    if x["positional_inference_evidence_sufficiency_result"] ==
       "FROZEN_SNAPSHOT_EVIDENCE_SUFFICIENT_FOR_SEPARATE_POSITIONAL_ADJUDICATION"
]
insufficient=[
    x["candidate_index"] for x in adjs
    if x["positional_inference_evidence_sufficiency_result"] ==
       "FROZEN_SNAPSHOT_EVIDENCE_INSUFFICIENT_NEW_BOUNDED_EVIDENCE_REQUIRED"
]
indeterminate=[
    x["candidate_index"] for x in adjs
    if x["positional_inference_evidence_sufficiency_result"] ==
       "SUFFICIENCY_REMAINS_INDETERMINATE"
]

assert summary == {
    "candidate_count":9,
    "sufficient_count":len(sufficient),
    "insufficient_count":len(insufficient),
    "indeterminate_count":len(indeterminate),
}

assert obj["results"]["sufficient_candidate_indices"] == sufficient
assert obj["results"]["insufficient_candidate_indices"] == insufficient
assert obj["results"]["indeterminate_candidate_indices"] == indeterminate
assert obj["results"]["post_assessment_branch_authorized"] is False
assert obj["results"]["authoritative_class06_source_instance_operationally_bound"] is False
assert obj["results"]["c2_source_instance_allowlist_bound"] is False
assert obj["results"]["req06_req14_determination_performed"] is False
assert obj["results"]["zero_unresolved_closure_established"] is False

# ------------------------------------------------------------------
# Execution trace: 4 records × 9 candidates
# ------------------------------------------------------------------

trace=[
    json.loads(x)
    for x in trace_path.read_text(encoding="utf-8").splitlines()
    if x.strip()
]

assert len(trace) == 36

for idx in indices:
    subset=[x for x in trace if x["candidate_index"] == idx]
    assert len(subset) == 4

    a,b,c,d=subset

    expected_trace_fields={
        "candidate_index",
        "snapshot_path",
        "snapshot_read_completed",
        "snapshot_identity_verified",
        "bounded_review_completed",
        "sufficiency_assessment_recorded",
    }

    for row in subset:
        assert set(row) == expected_trace_fields

    assert a["snapshot_read_completed"] is True
    assert a["snapshot_identity_verified"] is False
    assert a["bounded_review_completed"] is False
    assert a["sufficiency_assessment_recorded"] is False

    assert b["snapshot_read_completed"] is True
    assert b["snapshot_identity_verified"] is True
    assert b["bounded_review_completed"] is False
    assert b["sufficiency_assessment_recorded"] is False

    assert c["snapshot_read_completed"] is True
    assert c["snapshot_identity_verified"] is True
    assert c["sufficiency_assessment_recorded"] is False

    assert d["snapshot_read_completed"] is True
    assert d["snapshot_identity_verified"] is True
    assert d["sufficiency_assessment_recorded"] is True

print("D0258_EVIDENCE_SUFFICIENCY_EXECUTION_VERIFIER=PASS")
print("D0257_AUTHORIZATION_BINDING=PASS")
print("D0256_D0254_FROZEN_BINDING=PASS")
print("D0258_NINE_CANDIDATE_INPUT_BINDING=PASS")
print("D0258_PRIMARY_JSON_CANONICALIZATION=PASS")
print("D0258_EXACT_NINE_CANDIDATE_RECORDS=PASS")
print("D0258_SUFFICIENCY_RESULT_ENUMS=PASS")
print("D0258_RESULT_DEPENDENCIES=PASS")
print("D0258_SUMMARY_COUNTS=PASS")
print("D0258_EXECUTION_TRACE_STRUCTURE=PASS")
print("D0258_EVIDENCE_LOCATOR_GRAMMAR=PASS")
print("D0251_SNAPSHOT_CONTENT_READ_BY_D0258_SAFE_VERIFIER=NO")
print("D0254_SAFE_VERIFIER_EXECUTED_BY_D0258_SAFE_VERIFIER=NO")
print("D0256_SAFE_VERIFIER_EXECUTED_BY_D0258_SAFE_VERIFIER=NO")
print("D0257_SAFE_VERIFIER_EXECUTED_BY_D0258_SAFE_VERIFIER=NO")
print("D0258_SEMANTIC_SUFFICIENCY_REJUDGED_BY_SAFE_VERIFIER=NO")
print("D0258_POSITIONAL_STATUS_ASSIGNED_BY_SAFE_VERIFIER=NO")
print("D0258_CLASS06_RECLASSIFIED_BY_SAFE_VERIFIER=NO")
print("POST_D0258_BRANCH_AUTHORIZED=NO")
print("C4_AUTHORIZED=NO")
print("C5_AUTHORIZED=NO")
print("C6_AUTHORIZED=NO")
print("B2_AUTHORIZED=NO")
print("SAFE_D0258_VERIFIER=PASS")
