#!/usr/bin/env python3

import hashlib
import json
from pathlib import Path

PKG = Path(__file__).resolve().parent
PRIMARY = PKG / "01_positional_assignment_semantics_corrective_successor.v1.json"

EXPECTED_ENUM = [
    "INDETERMINATE",
    "NOT_REQUIRED",
    "REQUIRED",
]

EXPECTED_PARENT = "e51a667426eff940f94da295d398a042fe851c5f"

r = json.loads(PRIMARY.read_text(encoding="utf-8"))

assert r["correction_id"] == (
    "D0272-POSITIONAL-ASSIGNMENT-SEMANTICS-CORRECTIVE-SUCCESSOR-V1"
)

assert r["decision"] == "D0272"

assert r["role"] == (
    "CONTRACT_ONLY_CORRECTIVE_SUCCESSOR_WITHOUT_POSITIONAL_ADJUDICATION"
)

assert r["parent_binding"]["commit"] == EXPECTED_PARENT
assert r["parent_binding"]["authorized_candidate_indices"] == [6, 8, 9]

sem = r["positional_assignment_semantics"]

assert sem["judgment_enum"] == EXPECTED_ENUM
assert sem["candidate_specific_judgment_required"] is True
assert sem["bounded_evidence_only"] is True

assert (
    sem["mere_presence_of_positional_tokens_is_not_sufficient_for_required"]
    is True
)

assert (
    sem["mere_absence_of_an_established_nonpositional_crosswalk_is_not_sufficient_for_required"]
    is True
)

assert sem["not_established_is_not_equivalent_to_proven_absent"] is True

execution = r["d0273_execution_contract"]

assert execution["designated_execution_decision"] == "D0273"

assert (
    execution["execution_allowed_before_independent_d0272_checkpoint"]
    is False
)

assert execution["candidate_order"] == [6, 8, 9]
assert execution["allowed_output_statuses"] == EXPECTED_ENUM

required_false = [
    "d0251_snapshot_content_read",
    "snapshot_reread",
    "original_source_blob_reopen",
    "reference_following",
    "repository_source_search",
    "git_history_source_search",
    "network_access",
    "new_evidence_acquisition",
    "d0254_required_criterion_rejudgment",
    "d0254_historical_positional_status_mutation",
    "sufficiency_result_reselection",
    "sufficiency_result_mutation",
    "historical_result_mutation",
    "candidate_branch_membership_mutation",
    "cross_branch_backflow",
    "global_positional_status_materialization",
    "class06_reclassification",
    "indeterminate_branch_1_2_resolution",
    "insufficient_branch_3_5_7_10_evidence_acquisition",
    "b2_authorization",
    "analyzer_authorization",
    "baseline_authorization",
    "repair_authorization",
]

for key in required_false:
    assert execution[key] is False, key

boundary = r["d0272_execution_boundary"]

for key, value in boundary.items():
    assert value is False, key

assert r["next_required_checkpoint"] == (
    "INDEPENDENT_READ_ONLY_VERIFY_AND_FREEZE_D0272_CORRECTIVE_CONTRACT_BEFORE_ANY_D0273_POSITIONAL_ADJUDICATION_EXECUTION"
)

print("D0272_POSITIONAL_ASSIGNMENT_SEMANTICS_CORRECTIVE_VERIFIER=PASS")
print("D0272_ROLE=CONTRACT_ONLY_CORRECTIVE_SUCCESSOR")
print("D0272_TARGET_CANDIDATES=6,8,9")
print("D0272_POSITIONAL_ENUM=INDETERMINATE,NOT_REQUIRED,REQUIRED")
print("D0272_POSITIONAL_ADJUDICATION_EXECUTED=NO")
print("D0273_DESIGNATED_EXECUTION_DECISION=YES")
print("D0273_EXECUTION_ALLOWED_BEFORE_D0272_FREEZE=NO")
print("D0251_SNAPSHOT_CONTENT_READ=NO")
print("CLASS06_RECLASSIFICATION=NO")
