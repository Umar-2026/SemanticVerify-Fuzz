#!/usr/bin/env python3

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

REPO = Path("/openbayes/home/semanticverify-fuzz-research")
BASE = Path("evidence/annotation_preparation/protocol_specification_schema_successor_v2")

D0267_COMMIT = "71b370ba57220089d5646d9ddbd06f99821f3505"
D0268_SUBJECT = "decision: execute bounded D0266 validated targeted positive-evidence successor sufficiency resolution"

D0267_RECORD = REPO / BASE / "d0267_d0266_validated_targeted_positive_evidence_successor_sufficiency_resolution_authorization_v1/01_d0266_validated_targeted_positive_evidence_successor_sufficiency_resolution_authorization.v1.json"

D0262_PRIMARY = REPO / BASE / "d0262_d0260_mismatch_sufficiency_successor_adjudication_execution_v1/01_d0260_mismatch_sufficiency_successor_adjudication_execution.v1.json"
D0264_PRIMARY = REPO / BASE / "d0264_d0262_unresolved_three_way_discrepancy_basis_characterization_execution_v1/01_d0262_unresolved_three_way_discrepancy_basis_characterization_execution.v1.json"
D0266_PRIMARY = REPO / BASE / "d0266_d0264_multifactor_targeted_cited_evidence_adjudication_execution_v1/01_d0264_multifactor_targeted_cited_evidence_adjudication_execution.v1.json"

D0267_RECORD_SHA = "ce5267cd716ea3a2a8eca9640b398ceb0ac63a259ee7e0435f90dd28080bfd21"
D0262_SHA = "542bb55d2405b95120e88b5a8051eda36df6f560e6c8cc854c20dec54b63ea36"
D0264_SHA = "45cfc7e3105120e9ede8eb74d54b987c3a57c0e3010eb4c8e028178d1990bf09"
D0266_SHA = "be37688678bf083936a02ad90fa484f09afe9635394195a6c91a9705176a03cb"

INPUT_SHA = "4e3b7b38e0b68b19402e0269aa1cba96c95e6210b1a13d996f22245d54df3f7a"
RULE_ID = "D0268-RULE-VALIDATED-TARGETED-POSITIVE-EVIDENCE-V1"
EXPECTED_RESULT = "FROZEN_SNAPSHOT_EVIDENCE_SUFFICIENT_FOR_SEPARATE_POSITIONAL_ADJUDICATION"

UNRESOLVED = "UNRESOLVED"
MULTI = "MULTI_FACTOR_DIVERGENCE"
VALIDATED = "TARGETED_POSITIVE_EVIDENCE_VALIDATED"
EST = "EXPLICIT_POSITIONAL_ASSOCIATION_SUPPORT_ESTABLISHED"
NOT_EST = "EXPLICIT_POSITIONAL_ASSOCIATION_SUPPORT_NOT_ESTABLISHED"
AMB = "TARGET_EVIDENCE_UNIT_REMAINS_AMBIGUOUS"

PACKAGE_DIRNAME = "d0268_d0266_validated_targeted_positive_evidence_successor_sufficiency_resolution_execution_v1"
PRIMARY_NAME = "01_d0266_validated_targeted_positive_evidence_successor_sufficiency_resolution_execution.v1.json"
SCOPE_NAME = "02_d0266_validated_targeted_positive_evidence_successor_sufficiency_resolution_execution_scope.v1.md"
TRACE_NAME = "03_d0266_validated_targeted_positive_evidence_successor_sufficiency_resolution_execution_trace.v1.jsonl"
VERIFIER_NAME = "04_verify_d0266_validated_targeted_positive_evidence_successor_sufficiency_resolution_execution.v1.py"
MANIFEST_NAME = "05_d0266_validated_targeted_positive_evidence_successor_sufficiency_resolution_execution.v1.SHA256SUMS"

REL_PRIMARY = str(BASE / PACKAGE_DIRNAME / PRIMARY_NAME)
REL_SCOPE = str(BASE / PACKAGE_DIRNAME / SCOPE_NAME)
REL_TRACE = str(BASE / PACKAGE_DIRNAME / TRACE_NAME)
REL_VERIFIER = str(BASE / PACKAGE_DIRNAME / VERIFIER_NAME)
REL_MANIFEST = str(BASE / PACKAGE_DIRNAME / MANIFEST_NAME)
REL_DECISION = "documentation/decisions/0268-execute-bounded-d0266-validated-targeted-positive-evidence-successor-sufficiency-resolution.md"

EXPECTED_CHANGED_PATHS = sorted([
    REL_PRIMARY,
    REL_SCOPE,
    REL_TRACE,
    REL_VERIFIER,
    REL_MANIFEST,
    REL_DECISION,
])

def git(*args):
    return subprocess.check_output(
        ["git", "-C", str(REPO), *args],
        text=True,
    ).strip()

def sha_bytes(data):
    return hashlib.sha256(data).hexdigest()

def sha_path(path):
    return sha_bytes(path.read_bytes())

def no_dupe_hook(pairs):
    out = {}
    for k, v in pairs:
        assert k not in out
        out[k] = v
    return out

def load_json_bytes(path):
    data = path.read_bytes()
    obj = json.loads(
        data.decode("utf-8"),
        object_pairs_hook=no_dupe_hook,
    )
    return obj, data

def canonical_bytes(obj):
    return json.dumps(
        obj,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")

def candidate_dicts(obj, idx):
    out = []
    def walk(v):
        if isinstance(v, dict):
            try:
                same = int(v.get("candidate_index")) == idx
            except Exception:
                same = False
            if same:
                out.append(v)
            for x in v.values():
                walk(x)
        elif isinstance(v, list):
            for x in v:
                walk(x)
    walk(obj)
    return out

def contains_value(v, target):
    if isinstance(v, dict):
        return any(contains_value(x, target) for x in v.values())
    if isinstance(v, list):
        return any(contains_value(x, target) for x in v)
    return v == target

parser = argparse.ArgumentParser()
parser.add_argument("--package-root", default=None)
parser.add_argument("--precommit", action="store_true")
args = parser.parse_args()

if args.package_root is None:
    package_root = Path(__file__).resolve().parent
else:
    package_root = Path(args.package_root).resolve()

primary_path = package_root / PRIMARY_NAME
scope_path = package_root / SCOPE_NAME
trace_path = package_root / TRACE_NAME
verifier_path = package_root / VERIFIER_NAME
manifest_path = package_root / MANIFEST_NAME

assert primary_path.is_file()
assert scope_path.is_file()
assert trace_path.is_file()
assert verifier_path.is_file()
assert manifest_path.is_file()

assert sha_path(D0267_RECORD) == D0267_RECORD_SHA
assert sha_path(D0262_PRIMARY) == D0262_SHA
assert sha_path(D0264_PRIMARY) == D0264_SHA
assert sha_path(D0266_PRIMARY) == D0266_SHA

d0267, _ = load_json_bytes(D0267_RECORD)
assert d0267["authorization_target"] == "D0268_ONLY"
assert d0267["authorized_candidate_indices"] == [8, 9]
assert d0267["frozen_input_binding"]["successor_resolution_input_universe_sha256"] == INPUT_SHA
assert d0267["resolution_rule_contract"]["rule_id"] == RULE_ID

d0262, _ = load_json_bytes(D0262_PRIMARY)
d0264, _ = load_json_bytes(D0264_PRIMARY)
d0266, _ = load_json_bytes(D0266_PRIMARY)

input_rows = []
source_rows = {}

for idx in (8, 9):
    c262 = candidate_dicts(d0262, idx)
    c264 = candidate_dicts(d0264, idx)
    c266 = candidate_dicts(d0266, idx)

    assert any(contains_value(x, UNRESOLVED) for x in c262)
    assert any(contains_value(x, MULTI) for x in c264)

    target = next(
        x for x in c266
        if x.get("targeted_positive_evidence_result") == VALIDATED
    )

    locs = target["target_locator_records"]

    est = sum(1 for x in locs if x.get("target_evidence_judgment") == EST)
    not_est = sum(1 for x in locs if x.get("target_evidence_judgment") == NOT_EST)
    amb = sum(1 for x in locs if x.get("target_evidence_judgment") == AMB)

    assert est + not_est + amb == len(locs)

    row = {
        "candidate_index": idx,
        "d0262_successor_state": UNRESOLVED,
        "d0264_discrepancy_basis_class": MULTI,
        "d0266_targeted_positive_evidence_result": VALIDATED,
        "d0266_established_locator_count": est,
        "d0266_not_established_locator_count": not_est,
        "d0266_ambiguous_locator_count": amb,
    }

    input_rows.append(row)
    source_rows[idx] = row

assert sha_bytes(canonical_bytes(input_rows)) == INPUT_SHA

assert source_rows[8]["d0266_established_locator_count"] == 3
assert source_rows[8]["d0266_not_established_locator_count"] == 1
assert source_rows[8]["d0266_ambiguous_locator_count"] == 0

assert source_rows[9]["d0266_established_locator_count"] == 1
assert source_rows[9]["d0266_not_established_locator_count"] == 0
assert source_rows[9]["d0266_ambiguous_locator_count"] == 0

primary, primary_bytes = load_json_bytes(primary_path)
assert primary_bytes == canonical_bytes(primary)
assert not primary_bytes.endswith(b"\n")

assert set(primary.keys()) == {
    "resolution_id",
    "authorization_binding",
    "frozen_input_binding",
    "resolution_rule_contract",
    "candidate_successor_sufficiency_resolutions",
    "resolution_summary",
    "execution_boundaries",
    "results",
    "next_required_checkpoint",
}

assert primary["authorization_binding"]["authorization_commit"] == D0267_COMMIT
assert primary["authorization_binding"]["resolution_rule_id"] == RULE_ID
assert primary["frozen_input_binding"]["d0262_primary_sha256"] == D0262_SHA
assert primary["frozen_input_binding"]["d0264_primary_sha256"] == D0264_SHA
assert primary["frozen_input_binding"]["d0266_primary_sha256"] == D0266_SHA
assert primary["frozen_input_binding"]["successor_resolution_input_universe_sha256"] == INPUT_SHA

rows = primary["candidate_successor_sufficiency_resolutions"]
assert [x["candidate_index"] for x in rows] == [8, 9]

expected_candidate_fields = {
    "candidate_index",
    "d0262_prior_successor_state",
    "d0264_discrepancy_basis_class",
    "d0266_targeted_positive_evidence_result",
    "d0266_established_locator_count",
    "d0266_not_established_locator_count",
    "d0266_ambiguous_locator_count",
    "resolution_rule_id",
    "successor_sufficiency_result",
    "bounded_resolution_rationale",
}

for row in rows:
    assert set(row.keys()) == expected_candidate_fields
    idx = row["candidate_index"]
    src = source_rows[idx]

    assert row["d0262_prior_successor_state"] == src["d0262_successor_state"]
    assert row["d0264_discrepancy_basis_class"] == src["d0264_discrepancy_basis_class"]
    assert row["d0266_targeted_positive_evidence_result"] == VALIDATED
    assert row["d0266_established_locator_count"] == src["d0266_established_locator_count"]
    assert row["d0266_not_established_locator_count"] == src["d0266_not_established_locator_count"]
    assert row["d0266_ambiguous_locator_count"] == src["d0266_ambiguous_locator_count"]
    assert row["resolution_rule_id"] == RULE_ID

    recomputed = (
        EXPECTED_RESULT
        if (
            src["d0266_targeted_positive_evidence_result"] == VALIDATED
            and src["d0266_established_locator_count"] >= 1
        )
        else None
    )

    assert recomputed == EXPECTED_RESULT
    assert row["successor_sufficiency_result"] == recomputed

assert primary["resolution_summary"] == {
    "candidate_count": 2,
    "remaining_indeterminate_count": 0,
    "resolved_insufficient_count": 0,
    "resolved_sufficient_count": 2,
}

boundaries = primary["execution_boundaries"]
assert boundaries["d0251_snapshot_content_read"] is False
assert boundaries["d0266_target_evidence_rejudgment"] is False
assert boundaries["d0266_part_a_reexecution"] is False
assert boundaries["new_evidence_acquisition"] is False
assert boundaries["positional_status_assignment"] is False
assert boundaries["class06_reclassification"] is False
assert boundaries["successor_result_universe_materialization"] is False
assert boundaries["c4_authorization"] is False
assert boundaries["c5_authorization"] is False
assert boundaries["c6_authorization"] is False
assert boundaries["b2_authorization"] is False

trace_records = [
    json.loads(line, object_pairs_hook=no_dupe_hook)
    for line in trace_path.read_text(encoding="utf-8").splitlines()
    if line
]

assert len(trace_records) == 5

expected_stages = [
    "LOAD_AND_BIND_D0262_FROZEN_SUCCESSOR_STATE_FOR_CANDIDATES_8_9",
    "LOAD_AND_BIND_D0264_FROZEN_MULTI_FACTOR_CHARACTERIZATION_FOR_CANDIDATES_8_9",
    "LOAD_AND_BIND_D0266_FROZEN_TARGETED_POSITIVE_EVIDENCE_RESULTS_FOR_CANDIDATES_8_9",
    "APPLY_LOCKED_SUCCESSOR_SUFFICIENCY_RESOLUTION_RULE_TO_CANDIDATE_008",
    "APPLY_LOCKED_SUCCESSOR_SUFFICIENCY_RESOLUTION_RULE_TO_CANDIDATE_009",
]

assert [x["stage"] for x in trace_records] == expected_stages

manifest_lines = manifest_path.read_text(encoding="utf-8").splitlines()
assert len(manifest_lines) == 4

expected_manifest = {
    PRIMARY_NAME: sha_path(primary_path),
    SCOPE_NAME: sha_path(scope_path),
    TRACE_NAME: sha_path(trace_path),
    VERIFIER_NAME: sha_path(verifier_path),
}

seen = {}
for line in manifest_lines:
    digest, name = line.split("  ", 1)
    assert name not in seen
    seen[name] = digest

assert seen == expected_manifest
assert MANIFEST_NAME not in seen

if args.precommit:
    assert git("rev-parse", "HEAD") == D0267_COMMIT
else:
    commits = git(
        "log",
        "--diff-filter=A",
        "--format=%H",
        "--",
        REL_PRIMARY,
    ).splitlines()

    assert commits
    d0268_commit = commits[-1]

    assert git("rev-parse", f"{d0268_commit}^") == D0267_COMMIT
    assert git("show", "-s", "--format=%s", d0268_commit) == D0268_SUBJECT

    changed = sorted(
        x for x in git(
            "diff-tree",
            "--no-commit-id",
            "--name-only",
            "-r",
            d0268_commit,
        ).splitlines()
        if x
    )
    assert changed == EXPECTED_CHANGED_PATHS

    subprocess.check_output(
        ["git", "-C", str(REPO), "merge-base", "--is-ancestor", d0268_commit, "HEAD"],
        text=True,
    )

print("D0268_SUCCESSOR_SUFFICIENCY_RESOLUTION_EXECUTION_VERIFIER=PASS")
print("D0267_AUTHORIZATION_BINDING=PASS")
print("D0268_FROZEN_INPUT_IDENTITY_BINDING=PASS")
print("D0268_SUCCESSOR_RESOLUTION_INPUT_UNIVERSE_BINDING=PASS")
print("D0268_PRIMARY_JSON_CANONICALIZATION=PASS")
print("D0268_EXACT_CANDIDATE_ORDER_8_9=PASS")
print("D0268_D0266_TARGETED_RESULT_BINDING=PASS")
print("D0268_ESTABLISHED_LOCATOR_COUNT_BINDING=PASS")
print("D0268_DETERMINISTIC_RESOLUTION_RULE_RECOMPUTATION=PASS")
print("D0268_CANDIDATE_008_SUCCESSOR_RESULT=FROZEN_SNAPSHOT_EVIDENCE_SUFFICIENT_FOR_SEPARATE_POSITIONAL_ADJUDICATION")
print("D0268_CANDIDATE_009_SUCCESSOR_RESULT=FROZEN_SNAPSHOT_EVIDENCE_SUFFICIENT_FOR_SEPARATE_POSITIONAL_ADJUDICATION")
print("D0268_SUMMARY_COUNTS=PASS")
print("D0268_TRACE_RECORD_COUNT_5=PASS")
print("D0251_SNAPSHOT_CONTENT_READ_BY_D0268_SAFE_VERIFIER=NO")
print("D0266_TARGET_EVIDENCE_REJUDGED_BY_D0268_SAFE_VERIFIER=NO")
print("D0268_SAFE_VERIFIER_ASSIGNED_POSITIONAL_STATUS=NO")
print("D0268_SAFE_VERIFIER_RECLASSIFIED_CLASS06=NO")
print("SUCCESSOR_RESULT_UNIVERSE_MATERIALIZATION_AUTHORIZED=NO")
print("C4_AUTHORIZED=NO")
print("C5_AUTHORIZED=NO")
print("C6_AUTHORIZED=NO")
print("B2_AUTHORIZED=NO")
print("SAFE_D0268_VERIFIER=PASS")
