#!/usr/bin/env python3
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

REPO = Path("/openbayes/home/semanticverify-fuzz-research")

BASE = Path("evidence/annotation_preparation/protocol_specification_schema_successor_v2")

D0262_COMMIT = "2a48e8798cdb4cfd5648da46791613968b19d8aa"
D0262_TREE = "bf5a87e08298bccdf5ed45395f7aee47cfb803e9"
D0260_COMMIT = "bf142c026e64ce552f3c33279bf4ce372e6a8614"
D0258_COMMIT = "15afca914011851d516a05976e4d2d61c586f9d4"

D0258_PRIMARY = REPO / "evidence/annotation_preparation/protocol_specification_schema_successor_v2/d0258_bounded_positional_inference_evidence_sufficiency_assessment_execution_v1/01_bounded_positional_inference_evidence_sufficiency_assessment_execution.v1.json"
D0260_PRIMARY = REPO / "evidence/annotation_preparation/protocol_specification_schema_successor_v2/d0260_d0258_full_result_independent_content_and_sufficiency_revalidation_execution_v1/01_d0258_full_result_independent_content_and_sufficiency_revalidation_execution.v1.json"
D0262_PRIMARY = REPO / "evidence/annotation_preparation/protocol_specification_schema_successor_v2/d0262_d0260_mismatch_sufficiency_successor_adjudication_execution_v1/01_d0260_mismatch_sufficiency_successor_adjudication_execution.v1.json"

D0258_PRIMARY_SHA = "4aa389ad41c3a532c61c3b38aa397da6dccebb96d3384bb6a22d1e0af6462e60"
D0260_PRIMARY_SHA = "2b643b788509bff45b0a0756f530da4c5da90cd0d523347917d49d83660da807"
D0262_PRIMARY_SHA = "542bb55d2405b95120e88b5a8051eda36df6f560e6c8cc854c20dec54b63ea36"

UNRESOLVED_PROFILE_SHA = "a7b2b5fcc25a2485f4159493c34dad9d23d0859ac5942f91182bd86d451c6e8f"
SOURCE_PROJECTION_SHA = "f9221fa456638031e5981e14804b72f7d52daaf5a46c6f3dec18552a339d6427"
C8_TRIPLET_SHA = "a37b421a4ef7d69d07f2c709272e79f29337a5ce8f996bf313eb931a516ad26e"
C9_TRIPLET_SHA = "91c92c50508ed9e367501ba5a7af7446982b80aac86a722b7e1a4c2daa649902"

PKG_REL = Path("evidence/annotation_preparation/protocol_specification_schema_successor_v2/d0263_d0262_unresolved_three_way_discrepancy_basis_characterization_authorization_v1")
PRIMARY_NAME = "01_d0262_unresolved_three_way_discrepancy_basis_characterization_authorization.v1.json"
SCOPE_NAME = "02_d0262_unresolved_three_way_discrepancy_basis_characterization_authorization_scope.v1.md"
SELF_NAME = "03_verify_d0262_unresolved_three_way_discrepancy_basis_characterization_authorization.v1.py"
MANIFEST_NAME = "04_d0262_unresolved_three_way_discrepancy_basis_characterization_authorization.v1.SHA256SUMS"

RESULT_ENUM = {
    "FROZEN_SNAPSHOT_EVIDENCE_SUFFICIENT_FOR_SEPARATE_POSITIONAL_ADJUDICATION",
    "FROZEN_SNAPSHOT_EVIDENCE_INSUFFICIENT_NEW_BOUNDED_EVIDENCE_REQUIRED",
    "SUFFICIENCY_REMAINS_INDETERMINATE",
}

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def canonical(obj):
    return json.dumps(
        obj,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")

def obj_sha(obj):
    return hashlib.sha256(canonical(obj)).hexdigest()

def git(*args):
    return subprocess.check_output(
        ["git", "-C", str(REPO), *args],
        text=True,
    ).strip()

def load_no_dupes(path):
    def hook(pairs):
        out = {}
        for k, v in pairs:
            assert k not in out
            out[k] = v
        return out

    return json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=hook,
    )

def candidate_rows(doc):
    found = []

    def walk(x):
        if isinstance(x, list):
            if x and all(isinstance(v, dict) for v in x):
                ids = {
                    v.get("candidate_index")
                    for v in x
                    if isinstance(v.get("candidate_index"), int)
                }
                if {8, 9}.issubset(ids):
                    found.append(x)

            for v in x:
                walk(v)

        elif isinstance(x, dict):
            for v in x.values():
                walk(v)

    walk(doc)

    assert found
    found.sort(key=len, reverse=True)

    rows = {
        r["candidate_index"]: r
        for r in found[0]
        if r.get("candidate_index") in (8, 9)
    }

    assert set(rows) == {8, 9}
    return rows

ap = argparse.ArgumentParser()
ap.add_argument("--package-root", default=None)
ap.add_argument("--precommit", action="store_true")
args = ap.parse_args()

if args.package_root:
    pkg = Path(args.package_root)
else:
    pkg = REPO / PKG_REL

primary_path = pkg / PRIMARY_NAME
scope_path = pkg / SCOPE_NAME
self_path = pkg / SELF_NAME
manifest_path = pkg / MANIFEST_NAME

assert sha(D0258_PRIMARY) == D0258_PRIMARY_SHA
assert sha(D0260_PRIMARY) == D0260_PRIMARY_SHA
assert sha(D0262_PRIMARY) == D0262_PRIMARY_SHA

assert git("rev-parse", f"{D0262_COMMIT}^{{tree}}") == D0262_TREE
assert git("merge-base", "--is-ancestor", D0258_COMMIT, D0260_COMMIT) == ""
assert git("merge-base", "--is-ancestor", D0260_COMMIT, D0262_COMMIT) == ""

if args.precommit:
    assert git("rev-parse", "HEAD") == D0262_COMMIT
else:
    d0263_rel = str((REPO / PKG_REL / PRIMARY_NAME).relative_to(REPO))

    d0263_commit = git(
        "log",
        "--diff-filter=A",
        "-1",
        "--format=%H",
        "--",
        d0263_rel,
    )

    assert d0263_commit
    assert git("rev-parse", f"{d0263_commit}^") == D0262_COMMIT
    assert git("merge-base", "--is-ancestor", d0263_commit, "HEAD") == ""

manifest_lines = [
    x
    for x in manifest_path.read_text(encoding="utf-8").splitlines()
    if x.strip()
]

assert len(manifest_lines) == 3

expected_names = {
    PRIMARY_NAME,
    SCOPE_NAME,
    SELF_NAME,
}

seen = set()

for line in manifest_lines:
    parts = line.split("  ", 1)
    assert len(parts) == 2

    digest, name = parts
    assert name in expected_names
    assert name not in seen
    assert sha(pkg / name) == digest

    seen.add(name)

assert seen == expected_names
assert MANIFEST_NAME not in seen

raw = primary_path.read_bytes()
record = load_no_dupes(primary_path)

assert raw == canonical(record)
assert not raw.endswith(b"\n")

assert record["authorization_id"] == (
    "D0263-BOUNDED-D0262-UNRESOLVED-THREE-WAY-"
    "DISCREPANCY-BASIS-CHARACTERIZATION-AUTHORIZATION-V1"
)

assert record["authorization_target"] == "D0264_ONLY"
assert record["authorized_candidate_indices"] == [8, 9]

domain = record["authorized_input_domain"]

assert domain == {
    "d0258_frozen_result_record": True,
    "d0260_frozen_result_record": True,
    "d0262_frozen_result_record": True,
    "d0251_snapshot_content": False,
    "original_source_blob": False,
    "original_worktree_candidate": False,
    "reference_following": False,
    "repository_search": False,
    "git_history_search": False,
    "network_access": False,
}

ops = record["authorized_operations"]

assert ops == {
    "compare_result_values": True,
    "compare_evidence_reference_records": True,
    "compare_evidence_locator_kind_profiles": True,
    "compare_bounded_rationales": True,
    "classify_discrepancy_basis": True,
    "identify_follow_on_resolution_question": True,
}

forbidden = record["forbidden_operations"]

assert all(forbidden.values())
assert set(forbidden) == {
    "fourth_tie_breaker",
    "new_sufficiency_adjudication",
    "final_sufficiency_result_selection",
    "positional_required_or_not_required_assignment",
    "class06_reclassification",
    "successor_result_universe_materialization",
    "d0258_mutation",
    "d0260_mutation",
    "d0262_mutation",
    "c4_authorization",
    "c5_authorization",
    "c6_authorization",
    "b2_authorization",
}

binding = record["frozen_input_binding"]

assert binding["d0258_commit"] == D0258_COMMIT
assert binding["d0258_primary_sha256"] == D0258_PRIMARY_SHA
assert binding["d0260_commit"] == D0260_COMMIT
assert binding["d0260_primary_sha256"] == D0260_PRIMARY_SHA
assert binding["d0262_commit"] == D0262_COMMIT
assert binding["d0262_tree"] == D0262_TREE
assert binding["d0262_primary_sha256"] == D0262_PRIMARY_SHA

assert binding["unresolved_three_way_candidate_count"] == 2
assert binding["unresolved_three_way_candidate_indices"] == [8, 9]
assert binding["unresolved_three_way_profile_sha256"] == UNRESOLVED_PROFILE_SHA

assert (
    binding["candidate_008_frozen_source_triplet_sha256"]
    == C8_TRIPLET_SHA
)

assert (
    binding["candidate_009_frozen_source_triplet_sha256"]
    == C9_TRIPLET_SHA
)

assert (
    binding["frozen_source_projection_universe_sha256"]
    == SOURCE_PROJECTION_SHA
)

d8 = load_no_dupes(D0258_PRIMARY)
d60 = load_no_dupes(D0260_PRIMARY)
d62 = load_no_dupes(D0262_PRIMARY)

r8 = candidate_rows(d8)
r60 = candidate_rows(d60)
r62 = candidate_rows(d62)

projection = []

for idx in (8, 9):
    stages = {
        "D0258": {
            "candidate_index": idx,
            "result":
                r8[idx]["positional_inference_evidence_sufficiency_result"],
            "evidence_references":
                r8[idx]["evidence_references"],
            "bounded_rationale":
                r8[idx]["bounded_rationale"],
        },
        "D0260": {
            "candidate_index": idx,
            "result":
                r60[idx]["independent_sufficiency_result"],
            "evidence_references":
                r60[idx]["independent_evidence_references"],
            "bounded_rationale":
                r60[idx]["independent_bounded_rationale"],
        },
        "D0262": {
            "candidate_index": idx,
            "result":
                r62[idx]["tie_breaker_sufficiency_result"],
            "evidence_references":
                r62[idx]["tie_breaker_evidence_references"],
            "bounded_rationale":
                r62[idx]["tie_breaker_bounded_rationale"],
        },
    }

    assert {v["result"] for v in stages.values()} == RESULT_ENUM

    item = {
        "candidate_index": idx,
        "stages": stages,
    }

    projection.append(item)

    if idx == 8:
        assert obj_sha(item) == C8_TRIPLET_SHA
    else:
        assert obj_sha(item) == C9_TRIPLET_SHA

assert obj_sha(projection) == SOURCE_PROJECTION_SHA

contract = record["characterization_contract"]

assert contract["target"] == (
    "RECORDED_BASIS_OF_THREE_WAY_POSITIONAL_INFERENCE_"
    "EVIDENCE_SUFFICIENCY_DISAGREEMENT"
)

assert contract["may_use_recorded_result_values"] is True
assert contract["may_use_recorded_evidence_references"] is True
assert contract["may_use_recorded_bounded_rationales"] is True
assert contract["may_dereference_recorded_evidence"] is False
assert contract["may_infer_unrecorded_snapshot_content"] is False
assert contract["may_select_winning_sufficiency_result"] is False

boundary = record["execution_boundary"]

assert boundary == {
    "d0264_designated": True,
    "d0264_authorized_by_this_record": True,
    "d0264_execution_allowed_before_independent_d0263_checkpoint": False,
    "d0264_executed": False,
    "d0264_verified_frozen": False,
}

non = record["results_nonestablishment"]

assert non == {
    "d0258_verified_frozen": False,
    "successor_result_universe_materialization_authorized": False,
    "post_d0258_branch_authorized": False,
    "c4_authorized": False,
    "c5_authorized": False,
    "c6_authorized": False,
    "b2_readiness_established": False,
    "b2_authorized": False,
    "b2_executed": False,
}

assert record["next_required_checkpoint"] == (
    "INDEPENDENT_READ_ONLY_VERIFY_D0263_BEFORE_ANY_"
    "D0264_CHARACTERIZATION_EXECUTION"
)

print("D0263_THREE_WAY_DISCREPANCY_CHARACTERIZATION_AUTHORIZATION_VERIFIER=PASS")
print("D0262_FROZEN_INPUT_BINDING=PASS")
print("D0263_FROZEN_SOURCE_PROJECTION_BINDING=PASS")
print("D0263_AUTHORIZATION_SEMANTICS=PASS")
print("D0263_RESULTS_NONESTABLISHMENT_BOUNDARY=PASS")
print("D0264_CHARACTERIZATION_AUTHORIZED=YES")
print("D0264_CHARACTERIZATION_EXECUTED=NO")
print("D0264_EXECUTION_ALLOWED_BEFORE_INDEPENDENT_D0263_CHECKPOINT=NO")
print("D0251_SNAPSHOT_CONTENT_READ_BY_D0263_VERIFIER=NO")
print("D0262_SEMANTIC_EXECUTION_REEXECUTED_BY_D0263_VERIFIER=NO")
print("D0262_SAFE_VERIFIER_EXECUTED_BY_D0263_VERIFIER=NO")
print("SUCCESSOR_RESULT_UNIVERSE_MATERIALIZATION_AUTHORIZED=NO")
print("C4_AUTHORIZED=NO")
print("C5_AUTHORIZED=NO")
print("C6_AUTHORIZED=NO")
print("B2_AUTHORIZED=NO")
print("SAFE_D0263_VERIFIER=PASS")
