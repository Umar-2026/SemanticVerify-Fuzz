#!/usr/bin/env python3
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys

REPO = Path("/openbayes/home/semanticverify-fuzz-research")

BASE = Path(
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2"
)

PKG_REL = BASE / "d0261_d0260_mismatch_sufficiency_successor_adjudication_authorization_v1"
RECORD_NAME = "01_d0260_mismatch_sufficiency_successor_adjudication_authorization.v1.json"
SCOPE_NAME = "02_d0260_mismatch_sufficiency_successor_adjudication_authorization_scope.v1.md"
SELF_NAME = "03_verify_d0260_mismatch_sufficiency_successor_adjudication_authorization.v1.py"
MANIFEST_NAME = "04_d0260_mismatch_sufficiency_successor_adjudication_authorization.v1.SHA256SUMS"

DECISION_REL = Path(
    "documentation/decisions/"
    "0261-authorize-bounded-blinded-d0260-mismatch-sufficiency-successor-adjudication-without-execution.md"
)

D0260_COMMIT = "bf142c026e64ce552f3c33279bf4ce372e6a8614"
D0260_TREE = "00cb6cfeeec51135151ddc38713379b4a38bff1b"
D0260_PRIMARY_SHA = "2b643b788509bff45b0a0756f530da4c5da90cd0d523347917d49d83660da807"
D0260_MANIFEST_SHA = "b2ee751236bb7c83d049a83c1702e470edc800d3f9514f77d6764ccf5c3f6019"

MISMATCH_PROFILE_SHA = "522cba1167b05ade62805147efadfd95162b99557c13392d399639aa1deafdd6"
MAPPING_UNIVERSE_SHA = "f138eba3fc731ca52c1cd16047969198498e0c4dabc17bdedbdb5df249d30dc6"

D0260_PRIMARY = REPO / BASE / (
    "d0260_d0258_full_result_independent_content_and_sufficiency_revalidation_execution_v1/"
    "01_d0258_full_result_independent_content_and_sufficiency_revalidation_execution.v1.json"
)

D0260_MANIFEST = REPO / BASE / (
    "d0260_d0258_full_result_independent_content_and_sufficiency_revalidation_execution_v1/"
    "05_d0258_full_result_independent_content_and_sufficiency_revalidation_execution.v1.SHA256SUMS"
)

EXPECTED_SUBJECT = (
    "decision: authorize bounded blinded D0260 mismatch sufficiency "
    "successor adjudication without execution"
)

PREINSTALL = os.environ.get("D0261_PREINSTALL", "") == "1"

if PREINSTALL:
    pkg = Path(os.environ["D0261_PACKAGE_ROOT"])
    decision_path = Path(os.environ["D0261_DECISION_FILE"])
else:
    pkg = REPO / PKG_REL
    decision_path = REPO / DECISION_REL

record_path = pkg / RECORD_NAME
scope_path = pkg / SCOPE_NAME
self_path = pkg / SELF_NAME
manifest_path = pkg / MANIFEST_NAME

def die(msg):
    print("SAFE_D0261_VERIFIER=FAIL")
    print("REASON=" + msg)
    sys.exit(1)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def no_dup(pairs):
    d={}
    for k,v in pairs:
        if k in d:
            raise ValueError("duplicate object key")
        d[k]=v
    return d

def canonical(obj):
    return json.dumps(
        obj,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",",":")
    ).encode("utf-8")

def git(*args):
    p=subprocess.run(
        ["git","-C",str(REPO),*args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    if p.returncode != 0:
        die("git command failed: " + " ".join(args))
    return p.stdout.strip()

for p in [record_path, scope_path, self_path, manifest_path, decision_path]:
    if not p.is_file():
        die("missing required artifact: " + str(p))

if sha(D0260_PRIMARY) != D0260_PRIMARY_SHA:
    die("D0260 primary identity mismatch")

if sha(D0260_MANIFEST) != D0260_MANIFEST_SHA:
    die("D0260 manifest identity mismatch")

if git("rev-parse", D0260_COMMIT + "^{tree}") != D0260_TREE:
    die("D0260 tree mismatch")

raw = record_path.read_bytes()

try:
    rec = json.loads(raw.decode("utf-8"), object_pairs_hook=no_dup)
except Exception as e:
    die("authorization JSON parse failed: " + str(e))

if raw != canonical(rec):
    die("authorization JSON not canonical")

if raw.endswith(b"\n"):
    die("authorization JSON has final LF")

if rec.get("authorization_id") != (
    "D0261-BOUNDED-BLINDED-D0260-MISMATCH-SUFFICIENCY-"
    "SUCCESSOR-ADJUDICATION-AUTHORIZATION-V1"
):
    die("authorization_id mismatch")

if rec.get("authorization_role") != (
    "BOUNDED_BLINDED_D0260_MISMATCH_SUFFICIENCY_"
    "SUCCESSOR_ADJUDICATION_AUTHORIZATION_ONLY"
):
    die("authorization role mismatch")

frozen=rec["frozen_input_binding"]

if frozen != {
    "d0258_verified_frozen":False,
    "d0260_commit":D0260_COMMIT,
    "d0260_manifest_sha256":D0260_MANIFEST_SHA,
    "d0260_primary_results_verified_frozen":True,
    "d0260_primary_sha256":D0260_PRIMARY_SHA,
    "d0260_tree":D0260_TREE,
}:
    die("frozen input binding mismatch")

m=rec["mismatch_input_binding"]

if m != {
    "candidate_count":3,
    "candidate_indices":[5,8,9],
    "mismatch_profile_sha256":MISMATCH_PROFILE_SHA,
    "mismatch_snapshot_mapping_universe_sha256":MAPPING_UNIVERSE_SHA,
}:
    die("mismatch input binding mismatch")

a=rec["authorization_contract"]

required_auth = {
    "authorized_candidate_count":3,
    "authorized_candidate_indices":[5,8,9],
    "authorized_semantic_target":"POSITIONAL_INFERENCE_EVIDENCE_SUFFICIENCY_ONLY",
    "complete_current_bound_snapshot_review_authorized":True,
    "cross_candidate_content_as_evidence_authorized":False,
    "d0258_candidate_evidence_reference_access_before_blind_gate_authorized":False,
    "d0258_candidate_rationale_access_before_blind_gate_authorized":False,
    "d0258_candidate_result_access_before_blind_gate_authorized":False,
    "d0258_mutation_authorized":False,
    "d0260_candidate_evidence_reference_access_before_blind_gate_authorized":False,
    "d0260_candidate_rationale_access_before_blind_gate_authorized":False,
    "d0260_candidate_result_access_before_blind_gate_authorized":False,
    "d0260_mutation_authorized":False,
    "designated_execution_decision":"D0262",
    "each_bound_snapshot_primary_filesystem_read_count":"AT_MOST_1",
    "exact_bound_d0251_snapshot_reads_for_d0262_authorized":True,
    "git_history_search_authorized":False,
    "network_access_authorized":False,
    "original_candidate_worktree_read_authorized":False,
    "original_source_blob_reopen_authorized":False,
    "post_gate_comparison_to_d0258_and_d0260_authorized":True,
    "raw_git_blob_oid_recomputation_from_same_in_memory_bytes_authorized":True,
    "reference_following_authorized":False,
    "repository_search_authorized":False,
    "sha256_recomputation_from_same_in_memory_bytes_authorized":True,
    "snapshot_byte_count_verification_from_same_in_memory_bytes_authorized":True,
    "snapshot_python_execution_or_import_authorized":False,
    "successor_result_universe_materialization_authorized":False,
}

if a != required_auth:
    die("authorization contract mismatch")

d=rec["downstream_non_authorization"]

if any(d.values()):
    die("downstream non-authorization boundary violated")

r=rec["results"]

if r != {
    "d0261_authorization_created":True,
    "d0261_verified_frozen":False,
    "d0262_execution_allowed_before_independent_d0261_checkpoint":False,
    "d0262_reconciliation_authorized_by_d0261":True,
    "d0262_reconciliation_executed":False,
    "post_d0258_branch_authorized":False,
}:
    die("results boundary mismatch")

# Recompute D0260 mismatch profile and exact three-candidate mapping metadata.
d0260_raw=D0260_PRIMARY.read_bytes()

try:
    d0260=json.loads(d0260_raw.decode("utf-8"), object_pairs_hook=no_dup)
except Exception as e:
    die("D0260 primary parse failed: " + str(e))

rows=d0260["candidate_revalidations"]

mismatch=[
    x for x in rows
    if x["revalidation_comparison_result"] == "REVALIDATION_MISMATCH"
]

if [x["candidate_index"] for x in mismatch] != [5,8,9]:
    die("D0260 mismatch indices mismatch")

profile=[
    {
        "candidate_index":x["candidate_index"],
        "independent_sufficiency_result":x["independent_sufficiency_result"],
        "recorded_d0258_sufficiency_result":x["recorded_d0258_sufficiency_result"],
        "recorded_d0258_evidence_reference_validation_status":
            x["recorded_d0258_evidence_reference_validation_status"],
        "revalidation_comparison_result":x["revalidation_comparison_result"],
    }
    for x in mismatch
]

if hashlib.sha256(canonical(profile)).hexdigest() != MISMATCH_PROFILE_SHA:
    die("D0260 mismatch profile hash mismatch")

mapping=[
    {
        "candidate_index":x["candidate_index"],
        "root_id":x["root_id"],
        "source_locator":x["source_locator"],
        "snapshot_path":x["snapshot_path"],
        "snapshot_sha256":x["snapshot_sha256"],
        "snapshot_byte_count":x["snapshot_byte_count"],
        "snapshot_git_blob_oid":x["snapshot_git_blob_oid"],
    }
    for x in mismatch
]

if hashlib.sha256(canonical(mapping)).hexdigest() != MAPPING_UNIVERSE_SHA:
    die("D0260 mismatch snapshot mapping universe mismatch")

# Verify manifest.
manifest_lines=manifest_path.read_text(encoding="utf-8").splitlines()

if len(manifest_lines) != 3:
    die("manifest entry count mismatch")

expected_names=[RECORD_NAME,SCOPE_NAME,SELF_NAME]

for line,name in zip(manifest_lines, expected_names):
    parts=line.split("  ",1)
    if len(parts) != 2:
        die("malformed manifest line")
    expected_hash, observed_name=parts
    if observed_name != name:
        die("manifest filename mismatch")
    if sha(pkg / name) != expected_hash:
        die("manifest member hash mismatch")

if MANIFEST_NAME in manifest_path.read_text(encoding="utf-8"):
    die("manifest self hash present")

# Commit provenance only after installation/commit.
if not PREINSTALL:
    rel_self=str(PKG_REL / SELF_NAME)

    intro=git(
        "log",
        "--diff-filter=A",
        "--format=%H",
        "--",
        rel_self
    ).splitlines()

    if not intro:
        die("cannot locate D0261 introduction commit")

    d0261_commit=intro[0].strip()

    if git("rev-parse", d0261_commit + "^") != D0260_COMMIT:
        die("D0261 direct parent mismatch")

    if git("log","-1","--format=%s",d0261_commit) != EXPECTED_SUBJECT:
        die("D0261 subject mismatch")

    head=git("rev-parse","HEAD")

    p=subprocess.run(
        ["git","-C",str(REPO),"merge-base","--is-ancestor",d0261_commit,head],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    if p.returncode != 0:
        die("D0261 is not ancestor-or-equal of current HEAD")

print("D0261_MISMATCH_SUCCESSOR_ADJUDICATION_AUTHORIZATION_VERIFIER=PASS")
print("D0260_FROZEN_INPUT_BINDING=PASS")
print("D0261_MISMATCH_PROFILE_BINDING=PASS")
print("D0261_MISMATCH_SNAPSHOT_MAPPING_BINDING=PASS")
print("D0261_AUTHORIZATION_SEMANTICS=PASS")
print("D0261_BLINDNESS_GATE=PASS")
print("D0262_RECONCILIATION_AUTHORIZED=YES")
print("D0262_RECONCILIATION_EXECUTED=NO")
print("D0262_EXECUTION_ALLOWED_BEFORE_INDEPENDENT_D0261_CHECKPOINT=NO")
print("D0251_SNAPSHOT_CONTENT_READ_BY_D0261_VERIFIER=NO")
print("D0260_CONTENT_REVALIDATION_EXECUTED_BY_D0261_VERIFIER=NO")
print("D0260_SAFE_VERIFIER_EXECUTED_BY_D0261_VERIFIER=NO")
print("C4_AUTHORIZED=NO")
print("C5_AUTHORIZED=NO")
print("C6_AUTHORIZED=NO")
print("B2_AUTHORIZED=NO")
print("SAFE_D0261_VERIFIER=PASS")
