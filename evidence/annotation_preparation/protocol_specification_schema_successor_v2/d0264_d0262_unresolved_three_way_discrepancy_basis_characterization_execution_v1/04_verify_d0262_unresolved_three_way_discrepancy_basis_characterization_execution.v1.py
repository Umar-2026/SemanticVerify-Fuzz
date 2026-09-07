#!/usr/bin/env python3
import argparse
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path

REPO = Path("/openbayes/home/semanticverify-fuzz-research")
BASE = Path(
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2"
)

D0263_COMMIT = "d290deb09216baee402c14a6e09ee6ed4f3c4df6"
D0263_RECORD_SHA = "10f7d80ea4bfd583d52e88ebaae9fc80a841209cbf65b5c8c2715006649472b0"

D0258_SHA = "4aa389ad41c3a532c61c3b38aa397da6dccebb96d3384bb6a22d1e0af6462e60"
D0260_SHA = "2b643b788509bff45b0a0756f530da4c5da90cd0d523347917d49d83660da807"
D0262_SHA = "542bb55d2405b95120e88b5a8051eda36df6f560e6c8cc854c20dec54b63ea36"

UNRESOLVED_PROFILE_SHA = "a7b2b5fcc25a2485f4159493c34dad9d23d0859ac5942f91182bd86d451c6e8f"
SOURCE_PROJECTION_SHA = "f9221fa456638031e5981e14804b72f7d52daaf5a46c6f3dec18552a339d6427"
C008_TRIPLET_SHA = "a37b421a4ef7d69d07f2c709272e79f29337a5ce8f996bf313eb931a516ad26e"
C009_TRIPLET_SHA = "91c92c50508ed9e367501ba5a7af7446982b80aac86a722b7e1a4c2daa649902"

D0263_RECORD = (
    REPO / BASE /
    "d0263_d0262_unresolved_three_way_discrepancy_basis_characterization_authorization_v1/"
    "01_d0262_unresolved_three_way_discrepancy_basis_characterization_authorization.v1.json"
)

D0258_PRIMARY = (
    REPO / BASE /
    "d0258_bounded_positional_inference_evidence_sufficiency_assessment_execution_v1/"
    "01_bounded_positional_inference_evidence_sufficiency_assessment_execution.v1.json"
)
D0260_PRIMARY = (
    REPO / BASE /
    "d0260_d0258_full_result_independent_content_and_sufficiency_revalidation_execution_v1/"
    "01_d0258_full_result_independent_content_and_sufficiency_revalidation_execution.v1.json"
)
D0262_PRIMARY = (
    REPO / BASE /
    "d0262_d0260_mismatch_sufficiency_successor_adjudication_execution_v1/"
    "01_d0260_mismatch_sufficiency_successor_adjudication_execution.v1.json"
)

PKG_REL = (
    BASE /
    "d0264_d0262_unresolved_three_way_discrepancy_basis_characterization_execution_v1"
)

PRIMARY_NAME = "01_d0262_unresolved_three_way_discrepancy_basis_characterization_execution.v1.json"
SCOPE_NAME = "02_d0262_unresolved_three_way_discrepancy_basis_characterization_execution_scope.v1.md"
TRACE_NAME = "03_d0262_unresolved_three_way_discrepancy_basis_characterization_execution_trace.v1.jsonl"
SELF_NAME = "04_verify_d0262_unresolved_three_way_discrepancy_basis_characterization_execution.v1.py"
MANIFEST_NAME = "05_d0262_unresolved_three_way_discrepancy_basis_characterization_execution.v1.SHA256SUMS"

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def git(*args):
    return subprocess.check_output(
        ["git", "-C", str(REPO), *args],
        text=True,
    ).strip()

def canonical_bytes(obj):
    return json.dumps(
        obj,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")

def load_json_bytes(path):
    data = path.read_bytes()
    def hook(pairs):
        out = {}
        for k, v in pairs:
            assert k not in out
            out[k] = v
        return out
    return json.loads(
        data.decode("utf-8"),
        object_pairs_hook=hook,
    ), data

def same_index(v, idx):
    try:
        return int(v) == idx
    except Exception:
        return str(v).lstrip("0") == str(idx)

def find_exact(root, idx, discriminator):
    hits = []
    def walk(x):
        if isinstance(x, dict):
            if (
                "candidate_index" in x
                and same_index(x["candidate_index"], idx)
                and discriminator in x
            ):
                hits.append(x)
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)
    walk(root)
    assert len(hits) == 1
    return hits[0]

def evidence_profile(refs):
    kinds = Counter(r["locator_kind"] for r in refs)
    return {
        "canonical_reference_sequence_sha256":
            hashlib.sha256(canonical_bytes(refs)).hexdigest(),
        "locator_kind_counts":
            {k: kinds[k] for k in sorted(kinds)},
        "reference_count": len(refs),
    }

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
trace_path = pkg / TRACE_NAME
self_path = pkg / SELF_NAME
manifest_path = pkg / MANIFEST_NAME

assert sha(D0263_RECORD) == D0263_RECORD_SHA

d0263_text = D0263_RECORD.read_text(encoding="utf-8")
for token in (
    UNRESOLVED_PROFILE_SHA,
    SOURCE_PROJECTION_SHA,
    C008_TRIPLET_SHA,
    C009_TRIPLET_SHA,
):
    assert token in d0263_text

if args.precommit:
    assert git("rev-parse", "HEAD") == D0263_COMMIT
else:
    rel = str((REPO / PKG_REL / PRIMARY_NAME).relative_to(REPO))
    d0264_commit = git(
        "log",
        "--diff-filter=A",
        "-1",
        "--format=%H",
        "--",
        rel,
    )
    assert d0264_commit
    assert git("rev-parse", f"{d0264_commit}^") == D0263_COMMIT
    assert git(
        "merge-base",
        "--is-ancestor",
        d0264_commit,
        "HEAD",
    ) == ""

manifest_lines = [
    x
    for x in manifest_path.read_text(encoding="utf-8").splitlines()
    if x.strip()
]
assert len(manifest_lines) == 4

expected_names = {
    PRIMARY_NAME,
    SCOPE_NAME,
    TRACE_NAME,
    SELF_NAME,
}
seen = set()

for line in manifest_lines:
    parts = line.split("  ", 1)
    assert len(parts) == 2
    digest, name = parts
    assert name in expected_names
    assert name not in seen
    seen.add(name)
    assert sha(pkg / name) == digest

assert seen == expected_names
assert MANIFEST_NAME not in seen

primary, primary_bytes = load_json_bytes(primary_path)
assert primary_bytes == canonical_bytes(primary)

expected_primary_fields = {
    "authorization_binding",
    "candidate_characterizations",
    "characterization_contract",
    "characterization_id",
    "characterization_summary",
    "execution_boundaries",
    "frozen_source_record_binding",
    "next_required_checkpoint",
    "results",
    "unresolved_three_way_input_binding",
}
assert set(primary) == expected_primary_fields

assert primary["characterization_id"] == (
    "D0264-BOUNDED-D0262-UNRESOLVED-THREE-WAY-"
    "DISCREPANCY-BASIS-CHARACTERIZATION-V1"
)

assert primary["authorization_binding"] == {
    "d0263_authorization_commit": D0263_COMMIT,
    "d0263_authorization_record_sha256": D0263_RECORD_SHA,
}

assert (
    primary["unresolved_three_way_input_binding"]
    ["unresolved_three_way_profile_sha256"]
    == UNRESOLVED_PROFILE_SHA
)
assert (
    primary["frozen_source_record_binding"]
    ["frozen_source_projection_universe_sha256"]
    == SOURCE_PROJECTION_SHA
)
assert (
    primary["frozen_source_record_binding"]
    ["candidate_008_source_triplet_sha256"]
    == C008_TRIPLET_SHA
)
assert (
    primary["frozen_source_record_binding"]
    ["candidate_009_source_triplet_sha256"]
    == C009_TRIPLET_SHA
)

o58, b58 = load_json_bytes(D0258_PRIMARY)
o60, b60 = load_json_bytes(D0260_PRIMARY)
o62, b62 = load_json_bytes(D0262_PRIMARY)

assert hashlib.sha256(b58).hexdigest() == D0258_SHA
assert hashlib.sha256(b60).hexdigest() == D0260_SHA
assert hashlib.sha256(b62).hexdigest() == D0262_SHA

rows = primary["candidate_characterizations"]
assert len(rows) == 2
assert [r["candidate_index"] for r in rows] == [8, 9]

candidate_fields = {
    "candidate_index",
    "characterization_result",
    "d0258_evidence_profile",
    "d0258_rationale_sha256",
    "d0258_recorded_result",
    "d0260_evidence_profile",
    "d0260_rationale_sha256",
    "d0260_recorded_result",
    "d0262_evidence_profile",
    "d0262_rationale_sha256",
    "d0262_tie_breaker_result",
    "discrepancy_basis_class",
    "discrepancy_basis_rationale",
    "evidence_comparison_profile",
    "follow_on_resolution_question",
    "rationale_difference_profile",
}

allowed_classes = {
    "EVIDENCE_SELECTION_DIVERGENCE",
    "EXPLICITNESS_THRESHOLD_APPLICATION_DIVERGENCE",
    "NEGATIVE_REVIEW_VS_AMBIGUITY_CLASSIFICATION_DIVERGENCE",
    "RUBRIC_INTERPRETATION_DIVERGENCE",
    "MULTI_FACTOR_DIVERGENCE",
    "DISCREPANCY_BASIS_REMAINS_INDETERMINATE",
}
allowed_characterization_results = {
    "DISCREPANCY_BASIS_CHARACTERIZED",
    "DISCREPANCY_BASIS_REMAINS_INDETERMINATE",
}

for row in rows:
    assert set(row) == candidate_fields
    assert row["discrepancy_basis_class"] in allowed_classes
    assert row["characterization_result"] in allowed_characterization_results

    idx = row["candidate_index"]

    r58 = find_exact(
        o58,
        idx,
        "positional_inference_evidence_sufficiency_result",
    )
    r60 = find_exact(
        o60,
        idx,
        "independent_sufficiency_result",
    )
    r62 = find_exact(
        o62,
        idx,
        "tie_breaker_sufficiency_result",
    )

    assert row["d0258_recorded_result"] == (
        r58["positional_inference_evidence_sufficiency_result"]
    )
    assert row["d0260_recorded_result"] == (
        r60["independent_sufficiency_result"]
    )
    assert row["d0262_tie_breaker_result"] == (
        r62["tie_breaker_sufficiency_result"]
    )

    assert row["d0258_evidence_profile"] == evidence_profile(
        r58["evidence_references"]
    )
    assert row["d0260_evidence_profile"] == evidence_profile(
        r60["independent_evidence_references"]
    )
    assert row["d0262_evidence_profile"] == evidence_profile(
        r62["tie_breaker_evidence_references"]
    )

    assert row["d0258_rationale_sha256"] == hashlib.sha256(
        r58["bounded_rationale"].encode("utf-8")
    ).hexdigest()
    assert row["d0260_rationale_sha256"] == hashlib.sha256(
        r60["independent_bounded_rationale"].encode("utf-8")
    ).hexdigest()
    assert row["d0262_rationale_sha256"] == hashlib.sha256(
        r62["tie_breaker_bounded_rationale"].encode("utf-8")
    ).hexdigest()

summary = primary["characterization_summary"]
assert summary["candidate_count"] == 2
assert (
    summary["candidate_count"]
    ==
    summary["characterized_count"]
    + summary["indeterminate_count"]
)

trace = [
    json.loads(x)
    for x in trace_path.read_text(encoding="utf-8").splitlines()
    if x
]
assert len(trace) == 5

assert [x["stage"] for x in trace[:3]] == [
    "LOAD_AND_BIND_D0258_FROZEN_RESULT_RECORD",
    "LOAD_AND_BIND_D0260_FROZEN_RESULT_RECORD",
    "LOAD_AND_BIND_D0262_FROZEN_RESULT_RECORD",
]
assert trace[3]["candidate_index"] == 8
assert trace[4]["candidate_index"] == 9
assert trace[3]["stage"] == "CHARACTERIZE_CANDIDATE_008_DISCREPANCY_BASIS"
assert trace[4]["stage"] == "CHARACTERIZE_CANDIDATE_009_DISCREPANCY_BASIS"

assert primary["execution_boundaries"]["d0251_snapshot_content_read_count"] == 0
assert primary["execution_boundaries"]["final_sufficiency_result_selected"] is False
assert primary["results"]["final_sufficiency_result_selected"] is False
assert primary["results"]["follow_on_resolution_branch_authorized"] is False
assert (
    primary["results"]
    ["successor_result_universe_materialization_authorized"]
    is False
)

print("D0264_THREE_WAY_DISCREPANCY_CHARACTERIZATION_EXECUTION_VERIFIER=PASS")
print("D0263_AUTHORIZATION_BINDING=PASS")
print("D0264_FROZEN_SOURCE_PROJECTION_BINDING=PASS")
print("D0264_PRIMARY_JSON_CANONICALIZATION=PASS")
print("D0264_EXACT_TWO_CANDIDATE_RECORDS=PASS")
print("D0264_CANDIDATE_ORDER_8_9=PASS")
print("D0264_FROZEN_RESULT_VALUE_DEPENDENCIES=PASS")
print("D0264_EVIDENCE_PROFILE_HASH_DEPENDENCIES=PASS")
print("D0264_RATIONALE_SHA_DEPENDENCIES=PASS")
print("D0264_DISCREPANCY_CLASS_ENUM=PASS")
print("D0264_CHARACTERIZATION_RESULT_ENUM=PASS")
print("D0264_SUMMARY_COUNTS=PASS")
print("D0264_TRACE_RECORD_COUNT_5=PASS")
print("D0251_SNAPSHOT_CONTENT_READ_BY_D0264_SAFE_VERIFIER=NO")
print("D0264_SAFE_VERIFIER_RECHARACTERIZED_SEMANTIC_BASIS=NO")
print("D0264_SAFE_VERIFIER_SELECTED_FINAL_SUFFICIENCY_RESULT=NO")
print("D0264_SAFE_VERIFIER_ASSIGNED_POSITIONAL_STATUS=NO")
print("D0264_SAFE_VERIFIER_RECLASSIFIED_CLASS06=NO")
print("SUCCESSOR_RESULT_UNIVERSE_MATERIALIZATION_AUTHORIZED=NO")
print("POST_D0258_BRANCH_AUTHORIZED=NO")
print("C4_AUTHORIZED=NO")
print("C5_AUTHORIZED=NO")
print("C6_AUTHORIZED=NO")
print("B2_AUTHORIZED=NO")
print("SAFE_D0264_VERIFIER=PASS")
