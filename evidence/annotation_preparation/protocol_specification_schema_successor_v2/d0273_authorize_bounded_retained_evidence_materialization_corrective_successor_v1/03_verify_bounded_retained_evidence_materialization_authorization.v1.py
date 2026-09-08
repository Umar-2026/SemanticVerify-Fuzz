#!/usr/bin/env python3

import json
from pathlib import Path

PKG = Path(__file__).resolve().parent
PRIMARY = PKG / "01_bounded_retained_evidence_materialization_authorization.v1.json"

r = json.loads(PRIMARY.read_text(encoding="utf-8"))

assert r["authorization_id"] == (
    "D0273-BOUNDED-RETAINED-EVIDENCE-MATERIALIZATION-AUTHORIZATION-CORRECTIVE-SUCCESSOR-V1"
)

assert r["decision"] == "D0273"

assert r["role"] == (
    "AUTHORIZATION_ONLY_CORRECTIVE_SUCCESSOR_FOR_BOUNDED_RETAINED_EVIDENCE_MATERIALIZATION"
)

assert r["status"] == "AUTHORIZED_NOT_EXECUTED"

assert r["parent_binding"]["decision"] == "D0272"

assert r["parent_binding"]["commit"] == (
    "aab0743ac02a9db708b713449cb0f0171fcb930e"
)

assert r["parent_binding"]["verified_frozen"] is True
assert r["parent_binding"]["github_published"] is True

u = r["authorized_locator_universe"]

assert u["candidate_order"] == [6, 8, 9]
assert u["candidate_6"]["locator_count"] == 5
assert u["candidate_8"]["locator_count"] == 4
assert u["candidate_9"]["locator_count"] == 1
assert u["total_locator_count"] == 10
assert u["locator_kind"] == "LINE_RANGE"

assert u["locator_filtering_authorized"] is False
assert u["locator_reselection_authorized"] is False
assert u["new_locator_discovery_authorized"] is False

e = r["d0274_execution_authorization"]

assert e["authorized"] is True
assert e["designated_execution_decision"] == "D0274"

assert (
    e["execution_allowed_before_independent_d0273_checkpoint"]
    is False
)

assert e["operation"] == "BOUNDED_RETAINED_EVIDENCE_MATERIALIZATION"
assert e["candidate_order"] == [6, 8, 9]
assert e["candidate_count"] == 3
assert e["total_authorized_locator_count"] == 10

assert (
    e["d0251_snapshot_content_read_authorized_for_d0274_only"]
    is True
)

assert (
    e["d0251_snapshot_content_read_purpose"]
    == "EXTRACT_EXACT_TEXT_AT_PREBOUND_LINE_RANGE_LOCATORS_ONLY"
)

assert (
    e["snapshot_identity_verification_required_before_content_extraction"]
    is True
)

assert e["maximum_snapshot_filesystem_read_count_per_candidate"] == 1
assert e["maximum_total_snapshot_filesystem_read_count"] == 3

assert e["materialization_only"] is True

assert e["materialized_unit_fields"] == [
    "candidate_index",
    "locator_index",
    "locator_kind",
    "locator_value",
    "extracted_target_evidence_unit_text",
    "extracted_unit_sha256",
    "snapshot_sha256",
]

required_false = [
    "non_target_snapshot_read_authorized",
    "full_snapshot_semantic_rereview_authorized",
    "semantic_locator_reselection_authorized",
    "locator_filtering_authorized",
    "new_locator_discovery_authorized",
    "reference_following_authorized",
    "original_source_blob_reopen_authorized",
    "original_worktree_candidate_read_authorized",
    "repository_search_authorized",
    "git_history_search_authorized",
    "network_access_authorized",
    "snapshot_python_execution_authorized",
    "target_evidence_rejudgment_authorized",
    "positional_adjudication_authorized",
    "positional_status_assignment_authorized",
    "class06_reclassification_authorized",
    "sufficiency_result_reselection_authorized",
    "sufficiency_result_mutation_authorized",
    "branch_membership_mutation_authorized",
    "cross_branch_backflow_authorized",
    "global_positional_materialization_authorized",
    "b2_authorized",
    "analyzer_authorized",
    "baseline_authorized",
    "repair_authorized",
]

for key in required_false:
    assert e[key] is False, key

d275 = r["d0275_boundary"]

assert d275["authorized_by_d0273"] is False
assert d275["execution_authorized_by_d0273"] is False
assert d275["may_be_authorized_before_d0274_execution"] is False

assert (
    d275["may_be_executed_before_independent_d0274_verification_freeze"]
    is False
)

assert d275["candidate_order_if_later_authorized"] == [6, 8, 9]

assert d275["positional_status_enum_if_later_authorized"] == [
    "INDETERMINATE",
    "NOT_REQUIRED",
    "REQUIRED",
]

boundary = r["d0273_execution_boundary"]

for key, value in boundary.items():
    assert value is False, key

assert r["next_required_checkpoint"] == (
    "INDEPENDENT_READ_ONLY_VERIFY_AND_FREEZE_D0273_BEFORE_ANY_D0274_D0251_SNAPSHOT_CONTENT_READ_OR_RETAINED_EVIDENCE_MATERIALIZATION"
)

print("D0273_BOUNDED_RETAINED_EVIDENCE_MATERIALIZATION_AUTHORIZATION_VERIFIER=PASS")
print("D0273_ROLE=AUTHORIZATION_ONLY")
print("D0273_TARGET_CANDIDATES=6,8,9")
print("D0273_TOTAL_BOUND_LOCATORS=10")
print("D0274_MATERIALIZATION_AUTHORIZED=YES")
print("D0274_EXECUTION_ALLOWED_BEFORE_D0273_FREEZE=NO")
print("D0275_AUTHORIZED=NO")
print("D0273_D0251_SNAPSHOT_CONTENT_READ=NO")
print("D0273_POSITIONAL_ADJUDICATION_PERFORMED=NO")
