#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).parent

EXPECTED_D0233_MANIFEST_SHA = (
    "c608ad15a5a345cb0f525389cb70c9a478057c3e44fa265538ed259a150ccc0b"
)

EXPECTED_D0227_MANIFEST_SHA = (
    "db90747fb8f586992c524e5c541a1414bb12349b874ca4fa8a709c4ae0f17ab8"
)

EXPECTED_ENUM_SHA = (
    "44a6e8169f8515921a980cb727e106281f47bbe1a6bc9672e16146bab2832a12"
)

EXPECTED_TRACE_SHA = (
    "6b4b30c958bc1e1dd0896fe086205e3ff58063583b2042bba962c8c59ba46bd4"
)

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

assert sha(
    ROOT /
    "06_d0233_design_manifest.EXACT_COPY.v1.SHA256SUMS"
) == EXPECTED_D0233_MANIFEST_SHA

assert sha(
    ROOT /
    "07_d0227_corrective_successor_manifest.EXACT_COPY.v1.SHA256SUMS"
) == EXPECTED_D0227_MANIFEST_SHA

prior = json.loads(
    (
        ROOT /
        "05_d0233_design_record.EXACT_COPY.v1.json"
    ).read_text(encoding="utf-8")
)

assert (
    prior["status"]
    == "AUTHORIZATION_DESIGN_ONLY_NO_OPERATIONAL_AUTHORIZATION"
)

assert prior["selected_design_track"]["track_id"] == "B"
assert prior["selected_design_track"]["authorized_for_execution"] is False

next_auth = prior["recommended_next_future_authorization"]

assert next_auth["phase_id"] == "B1"
assert next_auth["name"] == "ACCOUNTING_SOURCE_AND_DOMAIN_ACQUISITION"
assert next_auth["authorization_created_by_d0233"] is False
assert next_auth["execution_created_by_d0233"] is False

binding = json.loads(
    (
        ROOT /
        "03_b1_source_identity_and_spec_binding.v1.json"
    ).read_text(encoding="utf-8")
)

assert binding["authorization_phase"] == "B1"
assert binding["source_scope_closed"] is True
assert binding["additional_source_acquisition_authorized"] is False
assert binding["source_identity_record_is_not_b1_execution"] is True

sources = {
    x["source_id"]: x
    for x in binding["primary_sources"]
}

assert set(sources) == {
    "ENUMERATION",
    "TRACEABILITY",
}

assert sources["ENUMERATION"]["sha256"] == EXPECTED_ENUM_SHA
assert sources["TRACEABILITY"]["sha256"] == EXPECTED_TRACE_SHA

for source in sources.values():
    assert source["canonical_and_d0227_copy_byte_equal"] is True

assert (
    binding["d0227_manifest_sha256"]
    == EXPECTED_D0227_MANIFEST_SHA
)

record = json.loads(
    (
        ROOT /
        "01_b1_accounting_source_domain_acquisition_authorization.v1.json"
    ).read_text(encoding="utf-8")
)

assert record["decision"] == "0234"

assert (
    record["status"]
    == "B1_ACCOUNTING_SOURCE_AND_DOMAIN_ACQUISITION_AUTHORIZED_NOT_EXECUTED"
)

a = record["authorization"]

assert a["b1_authorized"] is True
assert a["b1_execution_performed_by_d0234"] is False

assert (
    a["authorization_scope"]
    == "EXACT_TWO_SOURCE_BOUNDED_ACCOUNTING_SOURCE_AND_DOMAIN_ACQUISITION"
)

assert a["authorized_source_ids"] == [
    "ENUMERATION",
    "TRACEABILITY",
]

assert a["read_exact_checksum_bound_source_bytes"] is True
assert a["record_source_byte_identity_and_provenance"] is True
assert a["parse_each_source_locally"] is True
assert a["derive_source_local_req06_req14_domain_input_records"] is True
assert a["canonicalize_derived_b1_records_under_d0227_rules"] is True
assert a["package_b1_outputs_with_detached_hashes"] is True

assert a["cross_source_join"] is False
assert a["create_new_source_unit_carrier_mapping"] is False
assert a["expand_source_scope"] is False
assert a["use_unlisted_external_sources"] is False

execution = record["execution_constraint"]

assert execution["future_execution_decision_required"] is True
assert execution["d0235_exists_at_d0234_authorization_time"] is False
assert execution["canonical_sources_must_remain_unmodified"] is True
assert execution["d0227_exact_source_copies_must_remain_unmodified"] is True
assert execution["write_scope_limited_to_future_b1_execution_package"] is True
assert execution["additional_execution_package_requires_new_authorization"] is True

boundary = record["b1_output_boundary"]

assert boundary["may_record_source_local_domain_inputs"] is True
assert boundary["may_record_detached_hashes"] is True
assert boundary["may_record_source_local_provenance"] is True

assert boundary["may_join_enumeration_and_traceability_records"] is False
assert boundary["may_assert_domain_frozen"] is False
assert boundary["may_create_domain_freeze_record"] is False
assert boundary["may_create_domain_freeze_commit"] is False
assert boundary["may_acquire_forward_witness"] is False
assert boundary["may_acquire_reverse_witness"] is False
assert boundary["may_create_concrete_source_unit_carrier_mapping"] is False
assert boundary["may_determine_req06_req14_satisfaction"] is False
assert boundary["may_determine_req06_req14_violation"] is False
assert boundary["may_reclassify_pairs"] is False

for value in record["later_phase_authorization"].values():
    assert value is False

for value in record["explicit_nonauthorization"].values():
    assert value is False

for value in record["substantive_results_established_by_d0234"].values():
    assert value is False

assert record["operational_authorization_created"] is True
assert record["operational_execution_performed"] is False

manifest = (
    ROOT /
    "09_b1_accounting_source_domain_acquisition_authorization.v1.SHA256SUMS"
)

lines = [
    line
    for line in manifest.read_text(encoding="utf-8").splitlines()
    if line.strip()
]

listed = set()

for line in lines:
    digest, rel = line.split("  ", 1)
    p = ROOT / rel
    assert p.is_file(), rel
    assert sha(p) == digest, rel
    listed.add(rel)

actual = {
    p.relative_to(ROOT).as_posix()
    for p in ROOT.rglob("*")
    if p.is_file()
}

assert actual == listed | {
    "09_b1_accounting_source_domain_acquisition_authorization.v1.SHA256SUMS"
}

print("D0234_B1_AUTHORIZATION_VERIFIER=PASS")
print("B1_AUTHORIZED=YES")
print("B1_EXECUTED=NO")
print("AUTHORIZED_SOURCE_COUNT=2")
print("SOURCE_SCOPE_CLOSED=YES")
print("CROSS_SOURCE_JOIN_AUTHORIZED=NO")
print("B2_DOMAIN_FREEZE_AUTHORIZED=NO")
print("B3_FORWARD_WITNESS_AUTHORIZED=NO")
print("B4_REVERSE_WITNESS_AUTHORIZED=NO")
print("B5_MAPPING_AUTHORIZED=NO")
print("B6_DETERMINATION_AUTHORIZED=NO")
print("B7_RECLASSIFICATION_AUTHORIZED=NO")
print("ACTIVE_SCHEMA_V2_MATERIALIZATION_AUTHORIZED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
print("OPERATIONAL_AUTHORIZATION_CREATED=YES")
print("OPERATIONAL_EXECUTION_PERFORMED=NO")
