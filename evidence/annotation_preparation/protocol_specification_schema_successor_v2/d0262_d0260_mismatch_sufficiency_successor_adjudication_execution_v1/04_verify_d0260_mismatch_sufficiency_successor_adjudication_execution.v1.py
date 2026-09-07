#!/usr/bin/env python3
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

REPO = Path("/openbayes/home/semanticverify-fuzz-research")

D0261_COMMIT = "fe8fd6e81aaa843b42ecc91ffafe77b743ff3ce8"
D0261_RECORD_SHA = "61241dbca3cefe324dbe03ce3495966c9ef8441dcb86c144617406dc85e492c0"

D0260_COMMIT = "bf142c026e64ce552f3c33279bf4ce372e6a8614"
D0260_PRIMARY_SHA = "2b643b788509bff45b0a0756f530da4c5da90cd0d523347917d49d83660da807"
MISMATCH_PROFILE_SHA = "522cba1167b05ade62805147efadfd95162b99557c13392d399639aa1deafdd6"
MAPPING_UNIVERSE_SHA = "f138eba3fc731ca52c1cd16047969198498e0c4dabc17bdedbdb5df249d30dc6"

D0258_PRIMARY_SHA = "4aa389ad41c3a532c61c3b38aa397da6dccebb96d3384bb6a22d1e0af6462e60"

BASE = "evidence/annotation_preparation/protocol_specification_schema_successor_v2"

D0261_RECORD = REPO / BASE / "d0261_d0260_mismatch_sufficiency_successor_adjudication_authorization_v1/01_d0260_mismatch_sufficiency_successor_adjudication_authorization.v1.json"
D0260_PRIMARY = REPO / BASE / "d0260_d0258_full_result_independent_content_and_sufficiency_revalidation_execution_v1/01_d0258_full_result_independent_content_and_sufficiency_revalidation_execution.v1.json"
D0258_PRIMARY = REPO / BASE / "d0258_bounded_positional_inference_evidence_sufficiency_assessment_execution_v1/01_bounded_positional_inference_evidence_sufficiency_assessment_execution.v1.json"

PRIMARY_NAME = "01_d0260_mismatch_sufficiency_successor_adjudication_execution.v1.json"
SCOPE_NAME = "02_d0260_mismatch_sufficiency_successor_adjudication_execution_scope.v1.md"
TRACE_NAME = "03_d0260_mismatch_sufficiency_successor_adjudication_execution_trace.v1.jsonl"
SELF_NAME = "04_verify_d0260_mismatch_sufficiency_successor_adjudication_execution.v1.py"
MANIFEST_NAME = "05_d0260_mismatch_sufficiency_successor_adjudication_execution.v1.SHA256SUMS"

EXPECTED_CANDIDATE_FIELDS = {
    "candidate_index",
    "root_id",
    "source_locator",
    "snapshot_path",
    "snapshot_sha256",
    "snapshot_byte_count",
    "snapshot_git_blob_oid",
    "content_decode_status",
    "full_snapshot_blind_review_completed",
    "tie_breaker_sufficiency_result",
    "tie_breaker_evidence_references",
    "tie_breaker_bounded_rationale",
    "recorded_d0258_sufficiency_result",
    "recorded_d0260_sufficiency_result",
    "reconciliation_resolution",
    "successor_sufficiency_result",
    "reconciliation_rationale",
}

SUFFICIENT = "FROZEN_SNAPSHOT_EVIDENCE_SUFFICIENT_FOR_SEPARATE_POSITIONAL_ADJUDICATION"
INSUFFICIENT = "FROZEN_SNAPSHOT_EVIDENCE_INSUFFICIENT_NEW_BOUNDED_EVIDENCE_REQUIRED"
INDETERMINATE = "SUFFICIENCY_REMAINS_INDETERMINATE"

VALID_RESULTS = {SUFFICIENT, INSUFFICIENT, INDETERMINATE}
VALID_RESOLUTIONS = {
    "SUCCESSOR_RESOLVED_TWO_OF_THREE",
    "SUCCESSOR_RECONCILIATION_UNRESOLVED_THREE_WAY",
}

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def canonical_bytes(obj):
    return json.dumps(
        obj,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":")
    ).encode("utf-8")

def git(*args):
    return subprocess.check_output(
        ["git", "-C", str(REPO), *args],
        text=True
    ).strip()

ap = argparse.ArgumentParser()
ap.add_argument("--package-root", default=None)
ap.add_argument("--precommit", action="store_true")
args = ap.parse_args()

if args.package_root:
    pkg = Path(args.package_root)
else:
    pkg = REPO / BASE / "d0262_d0260_mismatch_sufficiency_successor_adjudication_execution_v1"

primary_path = pkg / PRIMARY_NAME
scope_path = pkg / SCOPE_NAME
trace_path = pkg / TRACE_NAME
self_path = pkg / SELF_NAME
manifest_path = pkg / MANIFEST_NAME

assert sha(D0261_RECORD) == D0261_RECORD_SHA
assert sha(D0260_PRIMARY) == D0260_PRIMARY_SHA
assert sha(D0258_PRIMARY) == D0258_PRIMARY_SHA

assert git("merge-base", "--is-ancestor", D0260_COMMIT, D0261_COMMIT) == ""

if args.precommit:
    assert git("rev-parse", "HEAD") == D0261_COMMIT
else:
    d0262_rel = str(primary_path.relative_to(REPO))
    d0262_commit = git(
        "log", "--diff-filter=A", "-1", "--format=%H", "--", d0262_rel
    )
    assert d0262_commit
    assert git("rev-parse", f"{d0262_commit}^") == D0261_COMMIT
    assert git("merge-base", "--is-ancestor", d0262_commit, "HEAD") == ""

manifest_lines = [
    x for x in manifest_path.read_text(encoding="utf-8").splitlines()
    if x.strip()
]
assert len(manifest_lines) == 4

expected_names = {PRIMARY_NAME, SCOPE_NAME, TRACE_NAME, SELF_NAME}
manifest_names = set()

for line in manifest_lines:
    parts = line.split("  ", 1)
    assert len(parts) == 2
    digest, name = parts
    assert re.fullmatch(r"[0-9a-f]{64}", digest)
    assert name in expected_names
    assert sha(pkg / name) == digest
    manifest_names.add(name)

assert manifest_names == expected_names
assert MANIFEST_NAME not in manifest_names

primary_raw = primary_path.read_bytes()
primary = json.loads(primary_raw.decode("utf-8"))

assert canonical_bytes(primary) == primary_raw
assert not primary_raw.endswith(b"\n")

assert primary["adjudication_id"] == (
    "D0262-BOUNDED-BLINDED-D0260-MISMATCH-SUFFICIENCY-SUCCESSOR-ADJUDICATION-V1"
)

assert primary["authorization_binding"]["d0261_commit"] == D0261_COMMIT
assert primary["d0260_frozen_mismatch_binding"]["d0260_commit"] == D0260_COMMIT
assert (
    primary["d0260_frozen_mismatch_binding"]["mismatch_profile_sha256"]
    == MISMATCH_PROFILE_SHA
)

u = primary["mismatch_snapshot_input_universe_binding"]
assert u["candidate_count"] == 3
assert u["candidate_indices"] == [5, 8, 9]
assert u["mapping_universe_sha256"] == MAPPING_UNIVERSE_SHA

records = primary["candidate_reconciliations"]
assert len(records) == 3
assert [r["candidate_index"] for r in records] == [5, 8, 9]

for r in records:
    assert set(r.keys()) == EXPECTED_CANDIDATE_FIELDS
    assert r["tie_breaker_sufficiency_result"] in VALID_RESULTS
    assert r["recorded_d0258_sufficiency_result"] in VALID_RESULTS
    assert r["recorded_d0260_sufficiency_result"] in VALID_RESULTS
    assert r["reconciliation_resolution"] in VALID_RESOLUTIONS

    a = r["recorded_d0258_sufficiency_result"]
    b = r["recorded_d0260_sufficiency_result"]
    t = r["tie_breaker_sufficiency_result"]

    assert a != b

    if t == a and t != b:
        assert r["reconciliation_resolution"] == "SUCCESSOR_RESOLVED_TWO_OF_THREE"
        assert r["successor_sufficiency_result"] == a
    elif t == b and t != a:
        assert r["reconciliation_resolution"] == "SUCCESSOR_RESOLVED_TWO_OF_THREE"
        assert r["successor_sufficiency_result"] == b
    else:
        assert len({a, b, t}) == 3
        assert (
            r["reconciliation_resolution"]
            == "SUCCESSOR_RECONCILIATION_UNRESOLVED_THREE_WAY"
        )
        assert r["successor_sufficiency_result"] == "UNRESOLVED"

    for ev in r["tie_breaker_evidence_references"]:
        assert set(ev.keys()) == {
            "evidence_purpose", "locator_kind", "locator_value"
        }
        kind = ev["locator_kind"]
        val = ev["locator_value"]
        assert kind in {"LINE_RANGE", "BYTE_RANGE", "JSON_POINTER"}
        if kind == "LINE_RANGE":
            assert re.fullmatch(r"L[1-9][0-9]*-L[1-9][0-9]*", val)
        elif kind == "BYTE_RANGE":
            assert re.fullmatch(r"[0-9]+:[0-9]+", val)
            a0, b0 = map(int, val.split(":"))
            assert 0 <= a0 < b0
        else:
            assert val.startswith("/") or val == ""

summary = primary["reconciliation_summary"]
assert summary["candidate_count"] == 3

resolved_actual = sum(
    1 for r in records
    if r["reconciliation_resolution"] == "SUCCESSOR_RESOLVED_TWO_OF_THREE"
)
unresolved_actual = sum(
    1 for r in records
    if r["reconciliation_resolution"]
    == "SUCCESSOR_RECONCILIATION_UNRESOLVED_THREE_WAY"
)

assert summary["resolved_two_of_three_count"] == resolved_actual
assert summary["unresolved_three_way_count"] == unresolved_actual
assert resolved_actual + unresolved_actual == 3

trace = [
    json.loads(x)
    for x in trace_path.read_text(encoding="utf-8").splitlines()
    if x.strip()
]
assert len(trace) == 15

assert [r["candidate_index"] for r in trace[:12]] == [
    5,5,5,5,8,8,8,8,9,9,9,9
]
assert [r["candidate_index"] for r in trace[12:]] == [5,8,9]

for r in trace[:12]:
    assert r["prior_results_accessed"] is False
    assert r["reconciliation_recorded"] is False

for r in trace[12:]:
    assert r["prior_results_accessed"] is True
    assert r["reconciliation_recorded"] is True

blind_fields = [
    "candidate_index",
    "snapshot_path",
    "snapshot_identity_verified",
    "content_decode_status",
    "full_snapshot_blind_review_completed",
    "tie_breaker_sufficiency_result",
    "tie_breaker_evidence_references",
    "tie_breaker_bounded_rationale",
]

blind_bytes = b""
for r in records:
    b = {k: r[k] for k in blind_fields if k != "snapshot_identity_verified"}
    _identity_trace_rows = [
        t
        for t in trace
        if t.get("candidate_index") == r["candidate_index"]
        and t.get("snapshot_identity_verified") is True
        and t.get("prior_results_accessed") is False
    ]
    assert _identity_trace_rows
    b["snapshot_identity_verified"] = True
    blind_bytes += canonical_bytes(b) + b"\n"

blind_sha = hashlib.sha256(blind_bytes).hexdigest()

assert trace[11]["blind_record_sha256"] == blind_sha
for r in trace[12:]:
    assert r["blind_record_sha256"] == blind_sha

assert primary["blind_review_contract"]["blind_assessment_record_sha256"] == blind_sha
assert (
    primary["blind_review_contract"]
    ["all_three_blind_results_recorded_before_prior_result_access"]
    is True
)

print("D0262_MISMATCH_SUCCESSOR_ADJUDICATION_EXECUTION_VERIFIER=PASS")
print("D0261_AUTHORIZATION_BINDING=PASS")
print("D0260_FROZEN_MISMATCH_BINDING=PASS")
print("D0262_THREE_SNAPSHOT_MAPPING_UNIVERSE_BINDING=PASS")
print("D0262_PRIMARY_JSON_CANONICALIZATION=PASS")
print("D0262_EXACT_THREE_CANDIDATE_RECORDS=PASS")
print("D0262_TWO_OF_THREE_FORMULA_CONSISTENCY=PASS")
print("D0262_SUMMARY_COUNTS=PASS")
print("D0262_TRACE_RECORD_COUNT_15=PASS")
print("D0262_ANTI_BIAS_BLIND_GATE=PASS")
print("D0262_BLIND_ASSESSMENT_RECORD_BINDING=PASS")
print("D0251_SNAPSHOT_CONTENT_READ_BY_D0262_SAFE_VERIFIER=NO")
print("D0260_CONTENT_REVALIDATION_REEXECUTED_BY_D0262_SAFE_VERIFIER=NO")
print("D0260_SAFE_VERIFIER_EXECUTED_BY_D0262_SAFE_VERIFIER=NO")
print("D0258_SAFE_VERIFIER_EXECUTED_BY_D0262_SAFE_VERIFIER=NO")
print("D0254_SAFE_VERIFIER_EXECUTED_BY_D0262_SAFE_VERIFIER=NO")
print("D0262_SAFE_VERIFIER_REJUDGED_TIE_BREAKER_SUFFICIENCY=NO")
print("D0262_SAFE_VERIFIER_ASSIGNED_POSITIONAL_STATUS=NO")
print("D0262_SAFE_VERIFIER_RECLASSIFIED_CLASS06=NO")
print("SUCCESSOR_RESULT_UNIVERSE_MATERIALIZATION_AUTHORIZED=NO")
print("POST_D0258_BRANCH_AUTHORIZED=NO")
print("C4_AUTHORIZED=NO")
print("C5_AUTHORIZED=NO")
print("C6_AUTHORIZED=NO")
print("B2_AUTHORIZED=NO")
print("SAFE_D0262_VERIFIER=PASS")
