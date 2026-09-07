#!/usr/bin/env python3

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

REPO = Path("/openbayes/home/semanticverify-fuzz-research")
BASE = Path("evidence/annotation_preparation/protocol_specification_schema_successor_v2")

D0266_COMMIT = "feb8cbc1f75061d98a6f2e816ac9bccc5254a0f1"
D0266_PRIMARY_SHA = "be37688678bf083936a02ad90fa484f09afe9635394195a6c91a9705176a03cb"
D0264_PRIMARY_SHA = "45cfc7e3105120e9ede8eb74d54b987c3a57c0e3010eb4c8e028178d1990bf09"
D0262_PRIMARY_SHA = "542bb55d2405b95120e88b5a8051eda36df6f560e6c8cc854c20dec54b63ea36"

INPUT_UNIVERSE_SHA = "4e3b7b38e0b68b19402e0269aa1cba96c95e6210b1a13d996f22245d54df3f7a"

D0267_SUBJECT = "decision: authorize bounded D0266 validated targeted positive-evidence successor sufficiency resolution without execution"

D0267_PKG_REL = BASE / "d0267_d0266_validated_targeted_positive_evidence_successor_sufficiency_resolution_authorization_v1"
D0267_RECORD_REL = D0267_PKG_REL / "01_d0266_validated_targeted_positive_evidence_successor_sufficiency_resolution_authorization.v1.json"
D0267_SCOPE_REL = D0267_PKG_REL / "02_d0266_validated_targeted_positive_evidence_successor_sufficiency_resolution_authorization_scope.v1.md"
D0267_VERIFIER_REL = D0267_PKG_REL / "03_verify_d0266_validated_targeted_positive_evidence_successor_sufficiency_resolution_authorization.v1.py"
D0267_MANIFEST_REL = D0267_PKG_REL / "04_d0266_validated_targeted_positive_evidence_successor_sufficiency_resolution_authorization.v1.SHA256SUMS"

D0262_PRIMARY = REPO / BASE / "d0262_d0260_mismatch_sufficiency_successor_adjudication_execution_v1/01_d0260_mismatch_sufficiency_successor_adjudication_execution.v1.json"
D0264_PRIMARY = REPO / BASE / "d0264_d0262_unresolved_three_way_discrepancy_basis_characterization_execution_v1/01_d0262_unresolved_three_way_discrepancy_basis_characterization_execution.v1.json"
D0266_PRIMARY = REPO / BASE / "d0266_d0264_multifactor_targeted_cited_evidence_adjudication_execution_v1/01_d0264_multifactor_targeted_cited_evidence_adjudication_execution.v1.json"

RESULT_SUFFICIENT = "FROZEN_SNAPSHOT_EVIDENCE_SUFFICIENT_FOR_SEPARATE_POSITIONAL_ADJUDICATION"
RESULT_INSUFFICIENT = "FROZEN_SNAPSHOT_EVIDENCE_INSUFFICIENT_NEW_BOUNDED_EVIDENCE_REQUIRED"
RESULT_INDETERMINATE = "SUFFICIENCY_REMAINS_INDETERMINATE"

RULE_ID = "D0268-RULE-VALIDATED-TARGETED-POSITIVE-EVIDENCE-V1"

EST = "EXPLICIT_POSITIONAL_ASSOCIATION_SUPPORT_ESTABLISHED"
NOT = "EXPLICIT_POSITIONAL_ASSOCIATION_SUPPORT_NOT_ESTABLISHED"
AMB = "TARGET_EVIDENCE_UNIT_REMAINS_AMBIGUOUS"
VALIDATED = "TARGETED_POSITIVE_EVIDENCE_VALIDATED"
UNRESOLVED = "UNRESOLVED"
MULTI = "MULTI_FACTOR_DIVERGENCE"


def sha256_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args):
    return subprocess.check_output(
        ["git", "-C", str(REPO), *args],
        text=True,
    ).strip()


def load_json_no_duplicates(path):
    data = path.read_bytes()

    def hook(pairs):
        out = {}
        for key, value in pairs:
            assert key not in out
            out[key] = value
        return out

    return json.loads(data.decode("utf-8"), object_pairs_hook=hook), data


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


def contains_value(d, target):
    found = False

    def walk(v):
        nonlocal found
        if found:
            return
        if isinstance(v, dict):
            for x in v.values():
                walk(x)
        elif isinstance(v, list):
            for x in v:
                walk(x)
        elif v == target:
            found = True

    walk(d)
    return found


def recompute_input_universe():
    d262, _ = load_json_no_duplicates(D0262_PRIMARY)
    d264, _ = load_json_no_duplicates(D0264_PRIMARY)
    d266, _ = load_json_no_duplicates(D0266_PRIMARY)

    projections = []

    for idx in (8, 9):
        r262 = candidate_dicts(d262, idx)
        r264 = candidate_dicts(d264, idx)
        r266 = candidate_dicts(d266, idx)

        assert any(contains_value(x, UNRESOLVED) for x in r262)
        assert any(contains_value(x, MULTI) for x in r264)

        target = None
        for x in r266:
            if x.get("targeted_positive_evidence_result") == VALIDATED:
                target = x
                break

        assert target is not None
        locs = target.get("target_locator_records")
        assert isinstance(locs, list)

        established = sum(
            1 for x in locs if x.get("target_evidence_judgment") == EST
        )
        not_established = sum(
            1 for x in locs if x.get("target_evidence_judgment") == NOT
        )
        ambiguous = sum(
            1 for x in locs if x.get("target_evidence_judgment") == AMB
        )

        assert established + not_established + ambiguous == len(locs)
        assert established >= 1

        projections.append(
            {
                "candidate_index": idx,
                "d0262_successor_state": UNRESOLVED,
                "d0264_discrepancy_basis_class": MULTI,
                "d0266_targeted_positive_evidence_result": VALIDATED,
                "d0266_established_locator_count": established,
                "d0266_not_established_locator_count": not_established,
                "d0266_ambiguous_locator_count": ambiguous,
            }
        )

    raw = canonical_bytes(projections)
    return hashlib.sha256(raw).hexdigest(), projections


parser = argparse.ArgumentParser()
parser.add_argument("--package-root")
parser.add_argument("--precommit", action="store_true")
args = parser.parse_args()

assert sha256_file(D0262_PRIMARY) == D0262_PRIMARY_SHA
assert sha256_file(D0264_PRIMARY) == D0264_PRIMARY_SHA
assert sha256_file(D0266_PRIMARY) == D0266_PRIMARY_SHA

input_sha, projections = recompute_input_universe()
assert input_sha == INPUT_UNIVERSE_SHA
assert [x["candidate_index"] for x in projections] == [8, 9]
assert projections[0]["d0266_established_locator_count"] == 3
assert projections[0]["d0266_not_established_locator_count"] == 1
assert projections[0]["d0266_ambiguous_locator_count"] == 0
assert projections[1]["d0266_established_locator_count"] == 1
assert projections[1]["d0266_not_established_locator_count"] == 0
assert projections[1]["d0266_ambiguous_locator_count"] == 0

if args.package_root:
    package_root = Path(args.package_root)
else:
    package_root = REPO / D0267_PKG_REL

record_path = package_root / D0267_RECORD_REL.name
scope_path = package_root / D0267_SCOPE_REL.name
verifier_path = package_root / D0267_VERIFIER_REL.name
manifest_path = package_root / D0267_MANIFEST_REL.name

for p in (record_path, scope_path, verifier_path, manifest_path):
    assert p.is_file()

record, record_bytes = load_json_no_duplicates(record_path)
assert record_bytes == canonical_bytes(record)
assert not record_bytes.endswith(b"\n")

assert record["authorization_id"] == "D0267-BOUNDED-D0266-VALIDATED-TARGETED-POSITIVE-EVIDENCE-SUCCESSOR-SUFFICIENCY-RESOLUTION-AUTHORIZATION-V1"
assert record["authorization_role"] == "AUTHORIZATION_ONLY_FOR_BOUNDED_D0266_VALIDATED_TARGETED_POSITIVE_EVIDENCE_SUCCESSOR_SUFFICIENCY_RESOLUTION"
assert record["authorization_target"] == "D0268_ONLY"
assert record["authorized_candidate_indices"] == [8, 9]

fib = record["frozen_input_binding"]
assert fib["d0262_primary_sha256"] == D0262_PRIMARY_SHA
assert fib["d0264_primary_sha256"] == D0264_PRIMARY_SHA
assert fib["d0266_commit"] == D0266_COMMIT
assert fib["d0266_primary_sha256"] == D0266_PRIMARY_SHA
assert fib["successor_resolution_input_universe_sha256"] == INPUT_UNIVERSE_SHA

rule = record["resolution_rule_contract"]
assert rule["rule_id"] == RULE_ID
assert rule["candidate_rule_applicability"] == [
    {"applies": True, "candidate_index": 8},
    {"applies": True, "candidate_index": 9},
]
assert rule["result_enum"] == [
    RESULT_SUFFICIENT,
    RESULT_INSUFFICIENT,
    RESULT_INDETERMINATE,
]

authorized = record["authorized_operations"]
assert authorized == {
    "deterministic_successor_sufficiency_rule_application": True,
    "read_frozen_d0262_primary": True,
    "read_frozen_d0264_primary": True,
    "read_frozen_d0266_primary": True,
    "successor_sufficiency_selection_for_candidates_8_9": True,
}

prohibited = record["prohibited_operations"]
for key in (
    "c4_authorization",
    "c5_authorization",
    "c6_authorization",
    "b2_authorization",
    "class06_reclassification",
    "d0251_snapshot_content_read",
    "d0266_blind_rejudgment",
    "d0266_part_a_reexecution",
    "git_history_source_search",
    "network_access",
    "new_evidence_acquisition",
    "original_source_blob_reopen",
    "positional_status_assignment",
    "reference_following",
    "repository_source_search",
    "successor_result_universe_materialization",
):
    assert prohibited[key] is True

boundary = record["results_nonestablishment_boundary"]
assert boundary == {
    "class06_reclassification_established_by_d0267": False,
    "d0268_execution_performed_by_d0267": False,
    "global_successor_result_universe_materialized_by_d0267": False,
    "positional_status_established_by_d0267": False,
    "successor_sufficiency_result_selected_by_d0267": False,
}

manifest_lines = manifest_path.read_text(encoding="utf-8").splitlines()
assert len(manifest_lines) == 3

expected_manifest_names = {
    record_path.name,
    scope_path.name,
    verifier_path.name,
}
seen_names = set()

for line in manifest_lines:
    digest, name = line.split("  ", 1)
    assert len(digest) == 64
    assert name in expected_manifest_names
    assert name not in seen_names
    seen_names.add(name)
    assert sha256_file(package_root / name) == digest

assert seen_names == expected_manifest_names
assert manifest_path.name not in seen_names

current_head = git("rev-parse", "HEAD")

if args.precommit:
    assert current_head == D0266_COMMIT
else:
    rows = git(
        "log",
        "--diff-filter=A",
        "--format=%H%x00%P%x00%s",
        "HEAD",
        "--",
        str(D0267_RECORD_REL),
    ).splitlines()

    assert len(rows) == 1
    parts = rows[0].split("\x00")
    assert len(parts) == 3

    d0267_commit, parent_field, subject = parts
    parents = parent_field.split()

    assert parents == [D0266_COMMIT]
    assert subject == D0267_SUBJECT
    assert git("merge-base", "--is-ancestor", d0267_commit, current_head) == ""
    assert git("rev-parse", f"{d0267_commit}^") == D0266_COMMIT

print("D0267_SUCCESSOR_SUFFICIENCY_RESOLUTION_AUTHORIZATION_VERIFIER=PASS")
print("D0266_FROZEN_INPUT_BINDING=PASS")
print("D0267_SUCCESSOR_RESOLUTION_INPUT_UNIVERSE_BINDING=PASS")
print("D0267_AUTHORIZATION_SEMANTICS=PASS")
print("D0267_RESULTS_NONESTABLISHMENT_BOUNDARY=PASS")
print("D0268_SUCCESSOR_SUFFICIENCY_RESOLUTION_AUTHORIZED=YES")
print("D0268_SUCCESSOR_SUFFICIENCY_RESOLUTION_EXECUTED=NO")
print("D0268_EXECUTION_ALLOWED_BEFORE_INDEPENDENT_D0267_CHECKPOINT=NO")
print("D0251_SNAPSHOT_CONTENT_READ_BY_D0267_VERIFIER=NO")
print("D0266_TARGET_EVIDENCE_REJUDGED_BY_D0267_VERIFIER=NO")
print("D0266_SAFE_VERIFIER_EXECUTED_BY_D0267_VERIFIER=NO")
print("POSITIONAL_STATUS_ADJUDICATION_AUTHORIZED=NO")
print("CLASS06_RECLASSIFICATION_AUTHORIZED=NO")
print("SUCCESSOR_RESULT_UNIVERSE_MATERIALIZATION_AUTHORIZED=NO")
print("C4_AUTHORIZED=NO")
print("C5_AUTHORIZED=NO")
print("C6_AUTHORIZED=NO")
print("B2_AUTHORIZED=NO")
print("SAFE_D0267_VERIFIER=PASS")
