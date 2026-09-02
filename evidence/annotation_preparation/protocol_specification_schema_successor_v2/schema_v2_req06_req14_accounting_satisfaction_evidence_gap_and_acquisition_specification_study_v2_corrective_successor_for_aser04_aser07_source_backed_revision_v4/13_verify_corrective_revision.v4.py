#!/usr/bin/env python3
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).parent

ENUM_SHA = "44a6e8169f8515921a980cb727e106281f47bbe1a6bc9672e16146bab2832a12"
TRACE_SHA = "6b4b30c958bc1e1dd0896fe086205e3ff58063583b2042bba962c8c59ba46bd4"

def load(name):
    return json.loads(
        (ROOT / name).read_text(encoding="utf-8")
    )

delta = load(
    "01_corrective_revision_delta_response.v4.json"
)

construction = load(
    "02_future_accounting_domain_construction_specification.v4.json"
)

schemas = load(
    "03_future_AEA01_AEA05_artifact_schemas.v4.json"
)

canonical = load(
    "04_accounting_evidence_canonicalization_and_detached_hash_rules.v4.json"
)

lineage = load(
    "05_future_domain_freeze_lineage_and_ordering_control.v4.json"
)

freeze = load(
    "06_complete_domain_freeze_record.schema.v2.json"
)

verifier_schema = load(
    "07_independent_verifier_output_record.schema.v2.json"
)

invariants = load(
    "08_cross_artifact_machine_invariants.v2.json"
)

assert delta["corrective_scope"] == [
    "ASER04",
    "ASER07",
]

assert delta["preserved_pass_items"] == [
    "ASER01",
    "ASER02",
    "ASER03",
    "ASER05",
    "ASER06",
    "ASER08",
    "ASER09",
]

meta = delta["aser04_source_metadata_correction"]

assert meta["previous_rejected_v3_prefix_derivation_used"] is False
assert meta["previous_rejected_v3_constant_kind_used"] is False

aea01 = schemas["AEA01"]
aea02 = schemas["AEA02"]
aea03 = schemas["AEA03"]
aea04 = schemas["AEA04"]
aea05 = schemas["AEA05"]

assert (
    aea01["properties"]
    ["enumeration_source_binding"]
    ["properties"]["sha256"]["const"]
    == ENUM_SHA
)

assert (
    aea01["properties"]
    ["traceability_source_binding"]
    ["properties"]["sha256"]["const"]
    == TRACE_SHA
)

assert (
    aea01["properties"]
    ["traceability_source_binding"]
    ["properties"]["source_container_key"]["const"]
    == "source_container"
)

assert (
    aea01["properties"]
    ["traceability_source_binding"]
    ["properties"]["source_path_key"]["const"]
    == "source_path"
)

assert (
    aea01["properties"]
    ["traceability_source_binding"]
    ["properties"]["source_unit_kind_key"]["const"]
    == "unit_kind"
)

assert (
    aea01["properties"]
    ["traceability_source_binding"]
    ["properties"]["source_provenance_sha256_key"]["const"]
    == "value_sha256"
)

source_props = (
    aea01["properties"]["sources"]
    ["additionalProperties"]["properties"]
)

for required in [
    "source_container",
    "source_path",
    "source_unit_kind",
    "source_provenance_sha256",
]:
    assert required in source_props

assert aea01["properties"]["record_count"]["const"] == 109
assert aea01["properties"]["sources"]["minProperties"] == 109
assert aea01["properties"]["sources"]["maxProperties"] == 109

assert aea02["properties"]["unresolved_count"]["const"] == 0

assert (
    set(
        aea02["properties"]["carrier_candidates"]
        ["additionalProperties"]["properties"]
        ["disposition"]["enum"]
    )
    == {
        "INCLUDED",
        "EXCLUDED",
    }
)

for aid in [
    "AEA01",
    "AEA02",
    "AEA03",
    "AEA04",
    "AEA05",
]:
    props = schemas[aid]["properties"]

    assert "artifact_sha256" not in props
    assert "domain_sha256" not in props
    assert "witness_sha256" not in props

lineage_required = {
    "witness_id",
    "creation_timestamp_utc",
    "creation_commit",
    "creation_commit_parent",
    "domain_freeze_commit",
    "u_domain_sha256",
    "c_domain_sha256",
    "predecessor_hashes",
    "derivation_input_hashes",
}

assert (
    set(aea03["properties"]["lineage"]["required"])
    == lineage_required
)

assert (
    set(aea04["properties"]["lineage"]["required"])
    == lineage_required
)

freeze_required = {
    "freeze_id",
    "freeze_timestamp_utc",
    "freeze_commit",
    "freeze_commit_parent",
    "u_domain_path",
    "u_domain_sha256",
    "c_domain_path",
    "c_domain_sha256",
    "enumeration_source_path",
    "enumeration_source_sha256",
    "traceability_source_path",
    "traceability_source_sha256",
    "carrier_candidate_source_path",
    "carrier_candidate_source_sha256",
    "predecessor_hashes",
    "derivation_input_hashes",
}

assert set(freeze["required"]) == freeze_required

assert (
    set(
        aea05["properties"]
        ["freeze_event_metadata"]["required"]
    )
    == freeze_required
)

required_verifier_fields = {
    "verifier_id",
    "verification_role",
    "verifier_path",
    "verifier_sha256",
    "command_argv",
    "working_directory",
    "evaluated_commits",
    "evaluated_objects",
    "checks",
    "exit_code",
    "stdout_sha256",
    "stderr_sha256",
    "generated_at_utc",
}

assert (
    set(verifier_schema["required"])
    == required_verifier_fields
)

assert (
    canonical["hash_self_reference_rule"]
    ["AEA01_AEA05_may_contain_own_artifact_sha256"]
    is False
)

assert (
    canonical["hash_self_reference_rule"]
    ["self_reference_eliminated"]
    is True
)

assert (
    canonical["numeric_canonicalization"]
    ["floating_point_allowed"]
    is False
)

assert (
    canonical["string_canonicalization"]
    ["unicode_normalization"]
    == "NONE"
)

assert "UTF-8 byte sequences" in (
    canonical["string_canonicalization"]
    ["object_member_order"]
)

required_invariant_ids = {
    "U01", "U02", "U03", "U04", "U05",
    "U06", "U07", "U08", "U09", "U10",
    "C01", "C02", "C03", "C04", "C05", "C06",
    "F01", "F02", "F03", "F04", "F05", "F06",
    "R01", "R02", "R03", "R04",
    "B01", "H01",
    "L01", "L02", "L03", "L04",
    "V01", "V02", "V03",
}

actual_ids = {
    row["id"]
    for row in invariants["invariants"]
}

assert required_invariant_ids <= actual_ids

assert (
    construction["AEA02_governed_schema_carrier_domain"]
    ["UNRESOLVED_allowed_in_finalized_AEA02"]
    is False
)

assert (
    construction["AEA05_provenance_closure"]
    ["self_declared_true_values_are_sufficient_evidence"]
    is False
)

assert lineage["actual_freeze_event_executed"] is False
assert lineage["actual_witness_created"] is False
assert lineage["actual_verifier_evidence_created"] is False
assert lineage["satisfaction_evaluated"] is False

for value in delta["nonclaims"].values():
    assert value is False

print("D0222_CORRECTED_V4_SPECIFICATION_VERIFIER=PASS")
print("SOURCE_BACKED_METADATA_DERIVATION=PASS")
print("ASER04_CORRECTIVE_CONTROLS=PASS")
print("ASER07_CORRECTIVE_CONTROLS=PASS")
print("PRESERVED_PASS_ITEMS_NONREGRESSION=PASS")
print("HASH_SELF_REFERENCE_ELIMINATION=PASS")
print("FREEZE_EVENT_METADATA_COMPLETENESS=PASS")
print("INDEPENDENT_VERIFIER_EVIDENCE_CONTRACT=PASS")
print("ACTUAL_ACCOUNTING_EVIDENCE_ACQUISITION_PERFORMED=NO")
print("ACTUAL_DOMAIN_ACQUISITION_PERFORMED=NO")
print("CONCRETE_MAPPING_CREATED=NO")
print("ACCOUNTING_SATISFACTION_EVALUATED=NO")
