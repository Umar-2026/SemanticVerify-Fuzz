#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import os
import subprocess

ROOT = Path(__file__).resolve().parent

D0236_HEAD = (
    "98c9f70e41a21cb9d0b10feba5c7b3f92ba0b18d"
)

D0236_TREE = (
    "8af54b9ba52424aa2c54c8938a88b3af0ca22886"
)

D0236_MANIFEST_SHA = (
    "9a8703e59b8869f0b884993f4c7d1e4106596f08dd65033d3e088768b783dcbd"
)

D0236_REL = (
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2/"
    "d0236_d0235_b1_canonicalization_role_refinement_corrective_successor_v1"
)

def sha(path):
    return hashlib.sha256(
        Path(path).read_bytes()
    ).hexdigest()

def resolve_repo():
    explicit = os.environ.get("SVF_REPO_ROOT")

    if explicit:
        repo = Path(explicit).resolve()
    else:
        repo = Path(
            subprocess.check_output(
                [
                    "git",
                    "rev-parse",
                    "--show-toplevel",
                ],
                text=True,
            ).strip()
        ).resolve()

    return repo

REPO = resolve_repo()
D0236 = REPO / D0236_REL

assert D0236.is_dir()

assert subprocess.check_output(
    [
        "git",
        "-C",
        str(REPO),
        "rev-parse",
        f"{D0236_HEAD}^{{tree}}",
    ],
    text=True,
).strip() == D0236_TREE

assert sha(
    D0236 /
    "12_d0235_b1_corrective_successor.v2.SHA256SUMS"
) == D0236_MANIFEST_SHA

assert sha(
    ROOT /
    "07_d0236_manifest.EXACT_COPY.v2.SHA256SUMS"
) == D0236_MANIFEST_SHA

assert (
    D0236 /
    "01_b1_corrective_successor_record.v1.json"
).read_bytes() == (
    ROOT /
    "05_d0236_successor_record.EXACT_COPY.v1.json"
).read_bytes()

assert (
    D0236 /
    "06_source_local_role_refinement.v1.json"
).read_bytes() == (
    ROOT /
    "06_d0236_role_refinement.EXACT_COPY.v1.json"
).read_bytes()

audit = json.loads(
    (
        ROOT /
        "02_preexisting_role_binding_audit_summary.v1.json"
    ).read_text(encoding="utf-8")
)

assert audit[
    "candidate_schema_v2_carrier_families"
]["preexisting_explicit_identifier_set_binding_found"] is False

assert audit[
    "candidate_schema_v2_carrier_families"
]["preexisting_explicit_order_preserving_binding_found"] is False

assert audit[
    "matrix_unit_analysis_field_classes"
]["preexisting_explicit_identifier_set_binding_found"] is False

assert audit[
    "matrix_unit_analysis_field_classes"
]["preexisting_explicit_order_preserving_binding_found"] is False

assert audit[
    "governance_consequence"
]["new_explicit_governance_required"] is True

record = json.loads(
    (
        ROOT /
        "01_target_array_semantic_role_governance.v1.json"
    ).read_text(encoding="utf-8")
)

assert record["decision"] == "0237"

assert (
    record["status"]
    == "TARGET_ARRAY_SEMANTIC_ROLES_GOVERNED_WITHOUT_CORRECTIVE_EXECUTION_OR_B2_AUTHORIZATION"
)

basis = record["governance_basis"]

assert basis["preexisting_explicit_field_role_binding_found"] is False
assert basis["this_is_new_explicit_governance"] is True
assert basis["predecessor_commit"] == D0236_HEAD
assert basis["predecessor_tree"] == D0236_TREE
assert basis["predecessor_manifest_sha256"] == D0236_MANIFEST_SHA

bindings = record["field_role_bindings"]

for name in [
    "candidate_schema_v2_carrier_families",
    "matrix_unit_analysis_field_classes",
]:
    role = bindings[name]

    assert role["collection_semantic_role"] == "IDENTIFIER_SET_ARRAY"
    assert role["semantic_order"] == "ORDER_IRRELEVANT"

    assert (
        role["canonical_order"]
        == "ASCENDING_LEXICOGRAPHIC_EXACT_UTF8_BYTES"
    )

    assert role["duplicate_values_allowed"] is False
    assert role["semantic_interpretation"] == "MEMBERSHIP_ONLY"

    assert (
        role["source_or_observed_order_has_semantic_priority"]
        is False
    )

c = record["d0236_conformance_consequence"]

assert c[
    "candidate_schema_v2_carrier_families_occurrences"
] == 109

assert c[
    "candidate_schema_v2_carrier_families_utf8_unsorted_occurrences"
] == 77

assert c[
    "candidate_schema_v2_carrier_families_duplicate_value_array_occurrences"
] == 0

assert c[
    "candidate_schema_v2_carrier_families_conforms_to_new_identifier_set_ordering"
] is False

assert c[
    "matrix_unit_analysis_field_classes_occurrences"
] == 109

assert c[
    "matrix_unit_analysis_field_classes_utf8_unsorted_occurrences"
] == 0

assert c[
    "matrix_unit_analysis_field_classes_duplicate_value_array_occurrences"
] == 0

assert c[
    "matrix_unit_analysis_field_classes_conforms_to_new_identifier_set_ordering"
] is True

assert c["d0236_full_target_array_semantics_conformance"] is False
assert c["future_corrective_successor_required"] is True

boundary = record["execution_boundary"]

for key in [
    "d0236_modified",
    "target_array_values_changed",
    "target_arrays_reordered",
    "b1_reexecuted",
    "original_authorized_sources_reparsed",
    "cross_source_join_performed",
    "concrete_mapping_created",
    "domain_freeze_created",
    "req06_req14_determination_performed",
]:
    assert boundary[key] is False, key

for key, value in record["later_phase_authorization"].items():
    assert value is False, key

for key, value in record["substantive_results_established"].items():
    assert value is False, key

rules = json.loads(
    (
        ROOT /
        "08_d0227_canonicalization_rules.EXACT_COPY.v5.json"
    ).read_text(encoding="utf-8")
)

assert (
    rules["array_semantics"]["identifier_set_arrays"]
    == "sort ascending by exact UTF-8 bytes; duplicate values forbidden"
)

assert (
    rules["string_canonicalization"]["identifier_set_array_order"]
    == "ascending lexicographic order of exact UTF-8 byte sequences"
)

manifest = (
    ROOT /
    "10_target_array_semantic_role_governance.v1.SHA256SUMS"
)

lines = [
    line
    for line in manifest.read_text(encoding="utf-8").splitlines()
    if line.strip()
]

listed = set()

for line in lines:
    digest, rel = line.split("  ", 1)

    path = ROOT / rel

    assert path.is_file(), rel
    assert sha(path) == digest, rel

    listed.add(rel)

actual = {
    p.name
    for p in ROOT.iterdir()
    if p.is_file()
}

assert actual == listed | {
    "10_target_array_semantic_role_governance.v1.SHA256SUMS"
}

print("D0237_TARGET_ARRAY_ROLE_GOVERNANCE_VERIFIER=PASS")
print("D0236_COMMIT_BINDING=PASS")
print("D0236_TREE_BINDING=PASS")
print("D0236_MANIFEST_BINDING=PASS")

print("PREEXISTING_EXPLICIT_ROLE_BINDING_FOUND=NO")
print("D0237_CREATES_NEW_EXPLICIT_ROLE_GOVERNANCE=YES")

print("CANDIDATE_SCHEMA_V2_CARRIER_FAMILIES_ROLE=IDENTIFIER_SET_ARRAY")
print("MATRIX_UNIT_ANALYSIS_FIELD_CLASSES_ROLE=IDENTIFIER_SET_ARRAY")

print("SEMANTIC_ORDER=ORDER_IRRELEVANT")
print("CANONICAL_ORDER=ASCENDING_LEXICOGRAPHIC_EXACT_UTF8_BYTES")
print("DUPLICATE_VALUES_ALLOWED=NO")

print("D0236_TARGET1_NONCONFORMING_ARRAY_COUNT=77")
print("D0236_TARGET2_NONCONFORMING_ARRAY_COUNT=0")
print("D0236_FULL_TARGET_ARRAY_SEMANTICS_CONFORMANCE=NO")

print("TARGET_ARRAY_VALUES_CHANGED_BY_D0237=NO")
print("TARGET_ARRAYS_REORDERED_BY_D0237=NO")

print("D0238_CORRECTIVE_EXECUTION_AUTHORIZED=NO")
print("B2_AUTHORIZED=NO")

print("DOMAIN_FREEZE_CREATED=NO")
print("CROSS_SOURCE_JOIN_PERFORMED=NO")
print("CONCRETE_MAPPING_CREATED=NO")
print("REQ06_REQ14_DETERMINATION_PERFORMED=NO")
