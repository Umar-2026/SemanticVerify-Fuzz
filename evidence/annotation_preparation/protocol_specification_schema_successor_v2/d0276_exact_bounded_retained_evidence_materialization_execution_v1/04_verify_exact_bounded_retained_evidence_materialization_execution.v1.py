#!/usr/bin/env python3

import hashlib
import json
from pathlib import Path

PKG = Path(__file__).resolve().parent

PRIMARY = (
    PKG
    / "01_exact_bounded_retained_evidence_materialization_execution.v1.json"
)

TRACE = (
    PKG
    / "03_exact_bounded_retained_evidence_materialization_execution_trace.v1.jsonl"
)

r = json.loads(PRIMARY.read_text(encoding="utf-8"))

trace = [
    json.loads(x)
    for x in TRACE.read_text(encoding="utf-8").splitlines()
    if x.strip()
]

assert r["materialization_id"] == (
    "D0276-EXACT-BOUNDED-RETAINED-EVIDENCE-MATERIALIZATION-EXECUTION-V1"
)

assert r["decision"] == "D0276"

assert r["role"] == (
    "EXACT_BOUNDED_RETAINED_EVIDENCE_MATERIALIZATION_EXECUTION"
)

assert r["status"] == "EXECUTED_SUCCESSFULLY"

assert r["parent_binding"]["decision"] == "D0275"

assert r["parent_binding"]["commit"] == (
    "cc84214771b39ebbd175e945b79ccf1d0156819f"
)

assert r["parent_binding"]["verified_frozen"] is True
assert r["parent_binding"]["github_published"] is True

a = r["authorization_binding"]

assert a["transaction_design_sha256"] == (
    "2b399b91fb2f81b7ec8b1c5a5bb515e9fe6ca7e26aced54a7921a2c9fdeb6f5b"
)

assert a["algorithm_object_sha256"] == (
    "7aa7a4f11ca99ccb1bbe1cbd537b1d0eac6dd2e0019366711cb103620f85d1c1"
)

assert a["authorized_candidate_order"] == [6,8,9]
assert a["authorized_candidate_count"] == 3
assert a["authorized_locator_count"] == 10

s = r["execution_summary"]

assert s["successful_snapshot_filesystem_read_count"] == 3

assert s["snapshot_filesystem_read_count_per_candidate"] == {
    "6":1,
    "8":1,
    "9":1,
}

assert s["materialized_unit_count"] == 10
assert s["candidate_6_materialized_unit_count"] == 5
assert s["candidate_8_materialized_unit_count"] == 4
assert s["candidate_9_materialized_unit_count"] == 1

assert s["historical_compatibility_anchor_count"] == 5
assert s["historical_compatibility_anchor_match_count"] == 5
assert s["historical_compatibility_gate"] == "PASS"

assert (
    s["candidate_6_extracted_only_after_all_five_anchor_matches"]
    is True
)

assert (
    s["candidate_6_second_snapshot_read_performed"]
    is False
)

identity = r["snapshot_identity_verifications"]

assert len(identity) == 3

assert [
    x["candidate_index"]
    for x in identity
] == [6,8,9]

assert all(
    x["snapshot_filesystem_read_count"] == 1
    and x["identity_verified"] is True
    for x in identity
)

anchors = r["compatibility_anchor_verifications"]

assert len(anchors) == 5
assert all(x["match"] is True for x in anchors)

units = r["materialized_units"]

assert len(units) == 10

assert [
    sum(x["candidate_index"] == idx for x in units)
    for idx in [6,8,9]
] == [5,4,1]

expected_fields = {
    "candidate_index",
    "locator_index",
    "locator_kind",
    "locator_value",
    "extracted_target_evidence_unit_text",
    "extracted_unit_sha256",
    "snapshot_sha256",
}

for unit in units:
    assert set(unit.keys()) == expected_fields

    computed = hashlib.sha256(
        unit[
            "extracted_target_evidence_unit_text"
        ].encode("utf-8")
    ).hexdigest()

    assert computed == unit["extracted_unit_sha256"]

assert r["compatibility_result"][
    "candidate_8_9_five_anchor_output_compatibility"
] == "ESTABLISHED"

assert r["compatibility_result"][
    "historical_algorithm_equivalence_claimed"
] is False

assert r["compatibility_result"]["semantic_judgment"] == "NONE"

for key, value in r["execution_boundaries"].items():
    assert value is False, key

assert r["d0277_boundary"]["authorized"] is False
assert r["d0277_boundary"]["executed"] is False

assert r["d0277_boundary"][
    "positional_status_enum_if_later_authorized"
] == [
    "INDETERMINATE",
    "NOT_REQUIRED",
    "REQUIRED",
]

assert r["next_required_checkpoint"] == (
    "INDEPENDENT_READ_ONLY_VERIFY_FREEZE_AND_PUBLISH_D0276_WITHOUT_SNAPSHOT_REREAD_BEFORE_ANY_D0277_POSITIONAL_ADJUDICATION_AUTHORIZATION"
)

assert len(trace) > 0

print("D0276_MATERIALIZATION_SAFE_VERIFIER=PASS")
print("D0276_MATERIALIZED_UNIT_COUNT=10")
print("D0276_SUCCESSFUL_SNAPSHOT_READ_COUNT=3")
print("D0276_COMPATIBILITY_ANCHOR_MATCH_COUNT=5")
print("D0276_POSITIONAL_ADJUDICATION_PERFORMED=NO")
print("D0277_AUTHORIZED=NO")
print("D0251_SNAPSHOT_REREAD_BY_SAFE_VERIFIER=NO")
