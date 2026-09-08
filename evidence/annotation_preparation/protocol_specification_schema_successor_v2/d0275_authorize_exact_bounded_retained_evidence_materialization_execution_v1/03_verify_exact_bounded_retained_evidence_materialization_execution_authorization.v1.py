#!/usr/bin/env python3

import hashlib
import json
from pathlib import Path

PKG = Path(__file__).resolve().parent

PRIMARY = (
    PKG
    / "01_exact_bounded_retained_evidence_materialization_execution_authorization.v1.json"
)

r = json.loads(PRIMARY.read_text(encoding="utf-8"))

def canon(obj):
    return json.dumps(
        obj,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")

assert r["authorization_id"] == (
    "D0275-AUTHORIZE-D0276-EXACT-BOUNDED-RETAINED-EVIDENCE-MATERIALIZATION-EXECUTION-V1"
)

assert r["decision"] == "D0275"

assert r["role"] == (
    "AUTHORIZATION_ONLY_CORRECTIVE_SUCCESSOR_FOR_D0276_BOUNDED_RETAINED_EVIDENCE_MATERIALIZATION"
)

assert r["status"] == "AUTHORIZED_NOT_EXECUTED"

assert r["parent_binding"]["decision"] == "D0274"

assert r["parent_binding"]["commit"] == (
    "b6f249c17304e9b9c9af0329acf6a3ef31cffe1e"
)

assert r["parent_binding"]["verified_frozen"] is True
assert r["parent_binding"]["github_published"] is True

binding = r["bound_transaction_design"]

assert binding["canonical_sha256"] == (
    "2b399b91fb2f81b7ec8b1c5a5bb515e9fe6ca7e26aced54a7921a2c9fdeb6f5b"
)

assert binding["algorithm_object_sha256"] == (
    "7aa7a4f11ca99ccb1bbe1cbd537b1d0eac6dd2e0019366711cb103620f85d1c1"
)

assert hashlib.sha256(
    canon(binding["design"])
).hexdigest() == binding["canonical_sha256"]

design = binding["design"]

assert design["design_id"] == (
    "D0275-BOUNDED-RETAINED-EVIDENCE-MATERIALIZATION-TRANSACTION-DESIGN-V1"
)

assert design["input_bindings"]["candidate_order"] == [6,8,9]
assert design["input_bindings"]["candidate_count"] == 3
assert design["input_bindings"]["total_locator_count"] == 10

assert len(design["input_bindings"]["candidates"]) == 3

assert [
    x["candidate_index"]
    for x in design["input_bindings"]["candidates"]
] == [6,8,9]

assert [
    x["locator_count"]
    for x in design["input_bindings"]["candidates"]
] == [5,4,1]

assert len(design["execution_sequence"]) == 5

assert design["fail_closed_result"] == (
    "NO_DURABLE_D0275_MATERIALIZATION_RESULT"
)

e = r["d0276_execution_authorization"]

assert e["authorized"] is True
assert e["designated_execution_decision"] == "D0276"

assert (
    e["execution_allowed_before_independent_d0275_checkpoint"]
    is False
)

assert e["operation"] == (
    "EXACT_BOUNDED_RETAINED_EVIDENCE_MATERIALIZATION"
)

assert e["transaction_design_sha256"] == (
    "2b399b91fb2f81b7ec8b1c5a5bb515e9fe6ca7e26aced54a7921a2c9fdeb6f5b"
)

assert e["algorithm_object_sha256"] == (
    "7aa7a4f11ca99ccb1bbe1cbd537b1d0eac6dd2e0019366711cb103620f85d1c1"
)

assert e["candidate_order"] == [6,8,9]
assert e["candidate_count"] == 3
assert e["total_locator_count"] == 10

assert e["maximum_snapshot_filesystem_read_count_per_candidate"] == 1
assert e["maximum_total_snapshot_filesystem_read_count"] == 3

assert e["candidate_8_9_historical_anchor_count"] == 5

assert (
    e["all_five_candidate_8_9_anchor_matches_required"]
    is True
)

assert (
    e["candidate_8_9_anchor_mismatch_action"]
    == "FAIL_CLOSED_NO_DURABLE_D0276_MATERIALIZATION_RESULT"
)

assert (
    e["candidate_6_extraction_allowed_only_after_all_five_anchor_matches"]
    is True
)

assert (
    e["atomic_durable_output_only_after_all_checks_pass"]
    is True
)

required_false = [
    "locator_filtering_authorized",
    "locator_reselection_authorized",
    "new_locator_discovery_authorized",
    "non_target_snapshot_read_authorized",
    "full_snapshot_semantic_rereview_authorized",
    "target_evidence_rejudgment_authorized",
    "positional_adjudication_authorized",
    "positional_status_assignment_authorized",
    "class06_reclassification_authorized",
    "sufficiency_result_mutation_authorized",
    "branch_membership_mutation_authorized",
    "cross_branch_backflow_authorized",
    "network_access_authorized",
    "snapshot_python_execution_authorized",
    "b2_authorized",
    "analyzer_authorized",
    "baseline_authorized",
    "repair_authorized",
]

for key in required_false:
    assert e[key] is False, key

d277 = r["d0277_boundary"]

assert d277["authorized_by_d0275"] is False
assert d277["execution_authorized_by_d0275"] is False
assert d277["may_be_authorized_before_d0276_execution"] is False

assert (
    d277["may_be_executed_before_independent_d0276_verification_freeze"]
    is False
)

assert d277["candidate_order_if_later_authorized"] == [6,8,9]

assert d277["positional_status_enum_if_later_authorized"] == [
    "INDETERMINATE",
    "NOT_REQUIRED",
    "REQUIRED",
]

for key, value in r["d0275_execution_boundary"].items():
    assert value is False, key

assert r["next_required_checkpoint"] == (
    "INDEPENDENT_READ_ONLY_VERIFY_FREEZE_AND_PUBLISH_D0275_BEFORE_ANY_D0276_SNAPSHOT_CONTENT_READ_OR_MATERIALIZATION"
)

print("D0275_MATERIALIZATION_PREEXECUTION_AUTHORIZATION_VERIFIER=PASS")
print("D0275_ROLE=AUTHORIZATION_ONLY")
print("D0275_TRANSACTION_DESIGN_SHA256=2b399b91fb2f81b7ec8b1c5a5bb515e9fe6ca7e26aced54a7921a2c9fdeb6f5b")
print("D0276_MATERIALIZATION_AUTHORIZED=YES")
print("D0276_EXECUTION_ALLOWED_BEFORE_D0275_FREEZE=NO")
print("D0277_AUTHORIZED=NO")
print("D0275_SNAPSHOT_CONTENT_READ=NO")
print("D0275_MATERIALIZATION_EXECUTED=NO")
print("POSITIONAL_ADJUDICATION_PERFORMED=NO")
