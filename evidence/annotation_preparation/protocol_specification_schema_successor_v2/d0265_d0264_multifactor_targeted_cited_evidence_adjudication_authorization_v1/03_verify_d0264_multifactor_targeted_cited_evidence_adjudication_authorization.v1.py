#!/usr/bin/env python3

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

REPO = Path("/openbayes/home/semanticverify-fuzz-research")
BASE = Path("evidence/annotation_preparation/protocol_specification_schema_successor_v2")

D0264_COMMIT = "28a2eb573c88bedd8a0f2b527814cfd8ebe8406e"
D0264_PRIMARY = REPO / BASE / "d0264_d0262_unresolved_three_way_discrepancy_basis_characterization_execution_v1" / "01_d0262_unresolved_three_way_discrepancy_basis_characterization_execution.v1.json"
D0264_PRIMARY_SHA = "45cfc7e3105120e9ede8eb74d54b987c3a57c0e3010eb4c8e028178d1990bf09"

TARGET_LOCATOR_SHA = "0be5087f66e27dce13ad2271ea69c8cce58441ef318ceb8c624b9c4ab0d30bea"
TARGET_MAPPING_SHA = "37bf22a6c4367a803802b8d3f66aea50fbf6e6784661d77f1bf7d9fe1534f06f"

PKG_REL = BASE / "d0265_d0264_multifactor_targeted_cited_evidence_adjudication_authorization_v1"

RECORD_NAME = "01_d0264_multifactor_targeted_cited_evidence_adjudication_authorization.v1.json"
SCOPE_NAME = "02_d0264_multifactor_targeted_cited_evidence_adjudication_authorization_scope.v1.md"
SELF_NAME = "03_verify_d0264_multifactor_targeted_cited_evidence_adjudication_authorization.v1.py"
MANIFEST_NAME = "04_d0264_multifactor_targeted_cited_evidence_adjudication_authorization.v1.SHA256SUMS"

AUTH_ID = "D0265-BOUNDED-D0264-MULTIFACTOR-TARGETED-CITED-EVIDENCE-ADJUDICATION-AUTHORIZATION-V1"

EXPECTED_LOCATORS = [
    {"candidate_index":8,"locator_kind":"LINE_RANGE","locator_value":"L50-L50"},
    {"candidate_index":8,"locator_kind":"LINE_RANGE","locator_value":"L51-L51"},
    {"candidate_index":8,"locator_kind":"LINE_RANGE","locator_value":"L61-L61"},
    {"candidate_index":8,"locator_kind":"LINE_RANGE","locator_value":"L84-L84"},
    {"candidate_index":9,"locator_kind":"LINE_RANGE","locator_value":"L195-L195"},
]

EXPECTED_MAPPINGS = [
    {
        "candidate_index":8,
        "root_id":"DISCOVERY-ROOT-03",
        "snapshot_path":"008.EXACT_BLOB_COPY",
        "snapshot_sha256":"c74240135454c6746b0829306d60c5a818c67d06a4148116de0f21891669a940",
        "snapshot_byte_count":5134601,
        "snapshot_git_blob_oid":"336573866fc84ab4b4379ee4f331fb448252acfb",
    },
    {
        "candidate_index":9,
        "root_id":"DISCOVERY-ROOT-03",
        "snapshot_path":"009.EXACT_BLOB_COPY",
        "snapshot_sha256":"80cebe2423f5e7061012a550c262e7f3ca13898ab40b76c0288c90bc9e4a5b9c",
        "snapshot_byte_count":11346,
        "snapshot_git_blob_oid":"03c709e75cb3ff738175198ad24b8074bbe6e70d",
    },
]

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def canonical_bytes(obj):
    return json.dumps(
        obj,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")

def duplicate_key_hook(pairs):
    out = {}
    for k, v in pairs:
        assert k not in out
        out[k] = v
    return out

def load_json_bytes(path):
    data = path.read_bytes()
    obj = json.loads(
        data.decode("utf-8"),
        object_pairs_hook=duplicate_key_hook,
    )
    return obj, data

def git(*args):
    return subprocess.check_output(
        ["git", "-C", str(REPO), *args],
        text=True,
    ).strip()

def git_ancestor(a, b):
    p = subprocess.run(
        ["git", "-C", str(REPO), "merge-base", "--is-ancestor", a, b],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return p.returncode == 0

ap = argparse.ArgumentParser()
ap.add_argument("--package-root", default=None)
ap.add_argument("--precommit", action="store_true")
args = ap.parse_args()

pkg = Path(args.package_root) if args.package_root else REPO / PKG_REL

record_path = pkg / RECORD_NAME
scope_path = pkg / SCOPE_NAME
self_path = pkg / SELF_NAME
manifest_path = pkg / MANIFEST_NAME

assert sha(D0264_PRIMARY) == D0264_PRIMARY_SHA

if args.precommit:
    assert git("rev-parse", "HEAD") == D0264_COMMIT
else:
    rel = str(record_path.relative_to(REPO))
    d0265_commit = git(
        "log",
        "--diff-filter=A",
        "-1",
        "--format=%H",
        "--",
        rel,
    )
    assert d0265_commit
    assert git("rev-parse", f"{d0265_commit}^") == D0264_COMMIT
    assert git_ancestor(d0265_commit, "HEAD")

manifest_lines = [
    line
    for line in manifest_path.read_text(encoding="utf-8").splitlines()
    if line.strip()
]

assert len(manifest_lines) == 3

expected_manifest_names = {
    RECORD_NAME,
    SCOPE_NAME,
    SELF_NAME,
}
seen_manifest_names = set()

for line in manifest_lines:
    parts = line.split("  ", 1)
    assert len(parts) == 2
    digest, name = parts
    assert name in expected_manifest_names
    assert name not in seen_manifest_names
    assert sha(pkg / name) == digest
    seen_manifest_names.add(name)

assert seen_manifest_names == expected_manifest_names
assert MANIFEST_NAME not in seen_manifest_names

record, record_bytes = load_json_bytes(record_path)

assert record_bytes == canonical_bytes(record)
assert not record_bytes.endswith(b"\n")

assert record["authorization_id"] == AUTH_ID

assert record["authorization_role"] == \
    "AUTHORIZATION_ONLY_FOR_BOUNDED_D0264_MULTIFACTOR_TARGETED_CITED_EVIDENCE_ADJUDICATION"

assert record["authorization_target"] == "D0266_ONLY"

parent = record["parent_binding"]
assert parent["d0264_commit"] == D0264_COMMIT
assert parent["d0264_primary_sha256"] == D0264_PRIMARY_SHA
assert parent["d0264_verified_frozen"] is True

d0264, _ = load_json_bytes(D0264_PRIMARY)
rows = d0264["candidate_characterizations"]

assert len(rows) == 2
assert [int(r["candidate_index"]) for r in rows] == [8, 9]

for row in rows:
    assert row["discrepancy_basis_class"] == "MULTI_FACTOR_DIVERGENCE"
    assert row["characterization_result"] == "DISCREPANCY_BASIS_CHARACTERIZED"

mf = record["d0264_multifactor_input_binding"]
assert mf["candidate_count"] == 2
assert mf["candidate_indices"] == [8, 9]
assert mf["candidate_008_discrepancy_basis_class"] == "MULTI_FACTOR_DIVERGENCE"
assert mf["candidate_009_discrepancy_basis_class"] == "MULTI_FACTOR_DIVERGENCE"

locators = record["targeted_locator_universe"]
mappings = record["targeted_snapshot_mapping_universe"]

assert locators == EXPECTED_LOCATORS
assert mappings == EXPECTED_MAPPINGS

assert hashlib.sha256(canonical_bytes(locators)).hexdigest() == TARGET_LOCATOR_SHA
assert hashlib.sha256(canonical_bytes(mappings)).hexdigest() == TARGET_MAPPING_SHA

assert record["targeted_locator_universe_sha256"] == TARGET_LOCATOR_SHA
assert record["targeted_snapshot_mapping_universe_sha256"] == TARGET_MAPPING_SHA

contract = record["authorized_execution_contract"]

assert contract["authorized_candidate_count"] == 2
assert contract["authorized_candidate_indices"] == [8, 9]
assert contract["d0266_designated_execution"] is True

assert contract["d0251_snapshot_content_read_authorized_for_d0266_only"] is True
assert contract["d0251_snapshot_content_read_requires_independently_frozen_d0265"] is True

assert contract["maximum_snapshot_filesystem_read_count_per_candidate"] == 1
assert contract["successful_total_snapshot_filesystem_read_count"] == 2

assert contract["snapshot_identity_verification_required"] is True
assert contract["target_locator_extraction_from_retained_bytes_authorized"] is True

assert contract["full_snapshot_semantic_rereview_authorized"] is False
assert contract["non_target_snapshot_semantic_inspection_authorized"] is False

assert contract["original_source_blob_reopen_authorized"] is False
assert contract["original_worktree_candidate_read_authorized"] is False
assert contract["reference_following_authorized"] is False
assert contract["repository_search_authorized"] is False
assert contract["git_history_search_authorized"] is False
assert contract["network_access_authorized"] is False

assert contract["final_sufficiency_selection_authorized"] is False
assert contract["positional_status_assignment_authorized"] is False
assert contract["class06_reclassification_authorized"] is False
assert contract["successor_result_universe_materialization_authorized"] is False
assert contract["c4_authorized"] is False
assert contract["c5_authorized"] is False
assert contract["c6_authorized"] is False
assert contract["b2_authorized"] is False

blind = record["blind_anti_bias_contract"]

assert blind["pre_gate_source_record_identity_visible"] is False
assert blind["pre_gate_d0258_result_visible"] is False
assert blind["pre_gate_d0260_result_visible"] is False
assert blind["pre_gate_d0262_result_visible"] is False
assert blind["pre_gate_evidence_purpose_label_visible"] is False
assert blind["pre_gate_prior_rationale_visible"] is False

assert blind["all_locator_judgments_must_be_durable_before_source_attribution_gate"] is True
assert blind["blind_judgment_record_sha256_required_before_gate"] is True
assert blind["post_gate_may_bind_prior_source_provenance"] is True
assert blind["post_gate_may_change_blind_locator_judgment"] is False

boundary = record["results_nonestablishment_boundary"]

assert boundary["d0266_targeted_adjudication_executed"] is False
assert boundary["final_sufficiency_result_selected"] is False
assert boundary["positional_status_assigned"] is False
assert boundary["class06_reclassified"] is False
assert boundary["successor_result_universe_materialized"] is False
assert boundary["post_d0258_branch_authorized"] is False
assert boundary["c4_authorized"] is False
assert boundary["c5_authorized"] is False
assert boundary["c6_authorized"] is False
assert boundary["b2_authorized"] is False

assert record["next_required_checkpoint"] == \
    "INDEPENDENT_READ_ONLY_VERIFY_D0265_BEFORE_ANY_D0266_SNAPSHOT_CONTENT_READ_OR_TARGETED_ADJUDICATION_EXECUTION"

print("D0265_TARGETED_EVIDENCE_ADJUDICATION_AUTHORIZATION_VERIFIER=PASS")
print("D0264_FROZEN_MULTIFACTOR_INPUT_BINDING=PASS")
print("D0265_TARGETED_LOCATOR_UNIVERSE_BINDING=PASS")
print("D0265_TARGETED_SNAPSHOT_MAPPING_BINDING=PASS")
print("D0265_AUTHORIZATION_SEMANTICS=PASS")
print("D0265_RESULTS_NONESTABLISHMENT_BOUNDARY=PASS")

print("D0266_TARGETED_ADJUDICATION_AUTHORIZED=YES")
print("D0266_TARGETED_ADJUDICATION_EXECUTED=NO")
print("D0266_EXECUTION_ALLOWED_BEFORE_INDEPENDENT_D0265_CHECKPOINT=NO")

print("D0251_SNAPSHOT_CONTENT_READ_BY_D0265_VERIFIER=NO")
print("D0264_CHARACTERIZATION_REEXECUTED_BY_D0265_VERIFIER=NO")
print("D0264_SAFE_VERIFIER_EXECUTED_BY_D0265_VERIFIER=NO")

print("FINAL_SUFFICIENCY_RESULT_SELECTION_AUTHORIZED=NO")
print("POSITIONAL_STATUS_ADJUDICATION_AUTHORIZED=NO")
print("CLASS06_RECLASSIFICATION_AUTHORIZED=NO")
print("SUCCESSOR_RESULT_UNIVERSE_MATERIALIZATION_AUTHORIZED=NO")

print("C4_AUTHORIZED=NO")
print("C5_AUTHORIZED=NO")
print("C6_AUTHORIZED=NO")
print("B2_AUTHORIZED=NO")

print("SAFE_D0265_VERIFIER=PASS")
