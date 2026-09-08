#!/usr/bin/env python3

import json
from pathlib import Path

PKG = Path(__file__).resolve().parent

PRIMARY = (
    PKG
    / "01_exact_line_range_extraction_semantics_corrective_successor.v1.json"
)

r = json.loads(PRIMARY.read_text(encoding="utf-8"))

assert r["contract_id"] == (
    "D0274-EXACT-LINE-RANGE-EXTRACTION-SEMANTICS-CORRECTIVE-SUCCESSOR-V1"
)

assert r["decision"] == "D0274"

assert r["role"] == (
    "CONTRACT_ONLY_CORRECTIVE_SUCCESSOR_FOR_EXACT_LINE_RANGE_EXTRACTION_SEMANTICS"
)

assert r["status"] == "CONTRACT_ESTABLISHED_NOT_EXECUTED"

basis = r["correction_basis"]

assert basis[
    "historical_coherent_exact_line_extraction_algorithm_frozen"
] is False

assert basis[
    "static_recovery_found_explicit_line_range_parser"
] is False

assert basis[
    "static_recovery_found_actual_snapshot_line_index_or_slice"
] is False

assert basis[
    "same_transaction_algorithm_definition_and_materialization_prohibited"
] is True

assert basis["historical_d0273_mutation"] is False
assert basis["d0274_reads_snapshot_content"] is False
assert basis["d0274_materializes_retained_evidence"] is False
assert basis["d0274_performs_positional_adjudication"] is False

parent = r["parent_binding"]

assert parent["decision"] == "D0273"
assert parent["commit"] == (
    "c3246078a05cb755fdb89fa61b0668585f0dedb6"
)
assert parent["verified_frozen"] is True
assert parent["github_published"] is True

inputs = r["frozen_materialization_input_bindings"]

assert inputs["candidate_order"] == [6, 8, 9]
assert inputs["authorized_locator_count"] == 10
assert inputs["candidate_6_locator_count"] == 5
assert inputs["candidate_8_locator_count"] == 4
assert inputs["candidate_9_locator_count"] == 1

alg = r["exact_line_range_extraction_algorithm"]

assert alg["algorithm_id"] == (
    "D0274-LINE-RANGE-UTF8-EXTRACTION-ALGORITHM-V1"
)

assert alg["historical_equivalence_claimed_before_execution"] is False

assert (
    alg["snapshot_read_policy"]["maximum_filesystem_read_count_per_candidate"]
    == 1
)

assert (
    alg["snapshot_read_policy"]["maximum_total_snapshot_filesystem_read_count"]
    == 3
)

assert alg["decode_policy"]["encoding"] == "UTF-8"
assert alg["decode_policy"]["error_policy"] == "STRICT"
assert alg["decode_policy"]["unicode_normalization"] == "NONE"
assert alg["decode_policy"]["whitespace_trimming"] == "NONE"

assert alg["locator_parser"]["locator_kind"] == "LINE_RANGE"

assert alg["locator_parser"]["accepted_grammar_regex"] == (
    "^L([1-9][0-9]*)-L([1-9][0-9]*)$"
)

assert alg["locator_parser"]["line_number_base"] == 1
assert alg["locator_parser"]["end_line_semantics"] == "INCLUSIVE"

assert alg["line_segmentation"]["python_semantics"] == (
    "decoded_text.splitlines()"
)

assert alg["line_segmentation"]["keep_line_terminators"] is False

assert alg["line_segmentation"]["selected_slice_semantics"] == (
    "lines[start_line_minus_1:end_line]"
)

assert alg["unit_construction"]["selected_lines_join_separator"] == "\\n"
assert alg["unit_construction"]["append_terminal_newline"] is False
assert alg["unit_construction"]["strip_or_rstrip"] is False

assert alg["unit_hash"]["algorithm"] == "SHA-256"

assert alg["unit_hash"]["input"] == (
    "UTF8_BYTES_OF_EXTRACTED_TARGET_EVIDENCE_UNIT_TEXT_EXACTLY_AS_CONSTRUCTED"
)

assert alg["unit_hash"]["json_serialization_quotes_included"] is False
assert alg["unit_hash"]["jsonl_record_newline_included"] is False

d275 = r["d0275_materialization_boundary"]

assert d275["authorized_by_d0274"] is False
assert d275["execution_authorized_by_d0274"] is False

assert (
    d275["may_be_authorized_before_independent_d0274_verification_freeze"]
    is False
)

assert d275["candidate_order_if_later_authorized"] == [6, 8, 9]
assert d275["authorized_locator_count_if_later_authorized"] == 10

assert d275["candidate_8_9_historical_hash_anchor_policy"] == (
    "ALL_FIVE_ALREADY_FROZEN_D0266_EXTRACTED_UNIT_HASHES_MUST_MATCH_EXACTLY"
)

assert d275["candidate_8_9_any_anchor_mismatch_action"] == (
    "FAIL_CLOSED_NO_DURABLE_D0275_MATERIALIZATION_RESULT"
)

assert d275["full_snapshot_semantic_rereview"] is False
assert d275["target_evidence_rejudgment"] is False
assert d275["positional_adjudication"] is False
assert d275["positional_status_assignment"] is False
assert d275["class06_reclassification"] is False

d276 = r["d0276_boundary"]

assert d276["authorized_by_d0274"] is False
assert d276["execution_authorized_by_d0274"] is False
assert d276["may_be_authorized_before_d0275_execution"] is False

assert (
    d276["may_be_executed_before_independent_d0275_verification_freeze"]
    is False
)

assert d276["candidate_order_if_later_authorized"] == [6, 8, 9]

assert d276["positional_status_enum_if_later_authorized"] == [
    "INDETERMINATE",
    "NOT_REQUIRED",
    "REQUIRED",
]

for key, value in r["d0274_execution_boundary"].items():
    assert value is False, key

assert r["next_required_checkpoint"] == (
    "INDEPENDENT_READ_ONLY_VERIFY_AND_FREEZE_D0274_EXTRACTION_SEMANTICS_BEFORE_ANY_D0275_SNAPSHOT_CONTENT_READ_OR_MATERIALIZATION"
)

print("D0274_EXTRACTION_SEMANTICS_CORRECTIVE_VERIFIER=PASS")
print("D0274_ROLE=CONTRACT_ONLY")
print("D0274_SNAPSHOT_CONTENT_READ=NO")
print("D0274_MATERIALIZATION_EXECUTED=NO")
print("D0275_AUTHORIZED=NO")
print("D0276_AUTHORIZED=NO")
print("POSITIONAL_ADJUDICATION_PERFORMED=NO")
