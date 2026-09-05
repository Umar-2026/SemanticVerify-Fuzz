#!/usr/bin/env python3

from pathlib import Path
from copy import deepcopy
from collections import Counter
import hashlib
import json
import os
import subprocess

ROOT = Path(__file__).resolve().parent

D0238_HEAD = "83e438710db355c70ae9860ad8bb357104decb64"
D0238_TREE = "f3c8063313d06fe6d2c17ecb33797476901e190b"
D0237_HEAD = "3c2bfabbd76ad8e0f5df28fd0cdfc4da7acc47ab"
D0236_HEAD = "98c9f70e41a21cb9d0b10feba5c7b3f92ba0b18d"

D0238_MANIFEST_SHA = (
    "280add229ff56b7fa45d7f75acf2c174b9ea956f91cf1c830584e4052073c525"
)

OLD_TRACE_SHA = (
    "d02d67addc0af427d71da66588ce6e1020017007dbdae76b3ef0c6cb3d5b625d"
)

EXPECTED_TRACE_SHA = (
    "9cee6cb560179386da9104d12d353a581dfe8c6149c5890b19c13b0973efc9f2"
)

EXPECTED_TRACE_SIZE = 486907

CHANGED_PATH_LIST_SHA = (
    "ef514ad0ef6abf25d2c402bad48d805f02892a29e5ea701aea556d00ae66cff4"
)

ENUM_PROFILE_SHA = (
    "4469d1e9040e94c878767f9aa0d1d5439ff1ced70a5792839cfd1b8c1e787bea"
)

TRACE_PROFILE_SHA = (
    "2e8c259ea8cee29d72017225f71480d465e55a4ad062626f7be77a6c2d52b662"
)

ENUM_DOMAIN_SHA = (
    "d7905be1646c53446ad3d28d4329e8098d74b14246d5117aa4b64cfe830e6de8"
)

TARGET1 = "candidate_schema_v2_carrier_families"
TARGET2 = "matrix_unit_analysis_field_classes"

BASE = (
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2"
)

D0238_REL = (
    BASE
    + "/d0238_target_array_corrective_execution_authorization_v1"
)

D0237_REL = (
    BASE
    + "/d0237_target_array_semantic_role_governance_v1"
)

D0236_REL = (
    BASE
    + "/d0236_d0235_b1_canonicalization_role_refinement_corrective_successor_v1"
)

def sha(path):
    return hashlib.sha256(
        Path(path).read_bytes()
    ).hexdigest()

def repo_root():
    explicit = os.environ.get("SVF_REPO_ROOT")

    if explicit:
        return Path(explicit).resolve()

    return Path(
        subprocess.check_output(
            [
                "git",
                "rev-parse",
                "--show-toplevel",
            ],
            text=True,
        ).strip()
    ).resolve()

def emit_string(value):
    parts = ['"']

    for ch in value:
        cp = ord(ch)

        if 0xD800 <= cp <= 0xDFFF:
            raise AssertionError(
                "surrogate code point forbidden"
            )

        if cp == 0x22:
            parts.append('\\"')

        elif cp == 0x5C:
            parts.append('\\\\')

        elif cp <= 0x1F:
            parts.append("\\u" + format(cp, "04x"))

        else:
            parts.append(ch)

    parts.append('"')

    return "".join(parts)

def canonical(value):
    if value is None:
        return "null"

    if value is True:
        return "true"

    if value is False:
        return "false"

    if isinstance(value, int):
        return str(value)

    if isinstance(value, float):
        raise AssertionError(
            "floating-point value forbidden"
        )

    if isinstance(value, str):
        return emit_string(value)

    if isinstance(value, list):
        return (
            "["
            + ",".join(canonical(item) for item in value)
            + "]"
        )

    if isinstance(value, dict):
        keys = sorted(
            value.keys(),
            key=lambda x: x.encode("utf-8"),
        )

        return (
            "{"
            + ",".join(
                emit_string(key)
                + ":"
                + canonical(value[key])
                for key in keys
            )
            + "}"
        )

    raise AssertionError(type(value))

REPO = repo_root()

assert subprocess.check_output(
    [
        "git",
        "-C",
        str(REPO),
        "rev-parse",
        f"{D0238_HEAD}^{{tree}}",
    ],
    text=True,
).strip() == D0238_TREE

assert subprocess.check_output(
    [
        "git",
        "-C",
        str(REPO),
        "rev-parse",
        f"{D0238_HEAD}^",
    ],
    text=True,
).strip() == D0237_HEAD

assert subprocess.check_output(
    [
        "git",
        "-C",
        str(REPO),
        "rev-parse",
        f"{D0237_HEAD}^",
    ],
    text=True,
).strip() == D0236_HEAD

d0238 = REPO / D0238_REL
d0237 = REPO / D0237_REL
d0236 = REPO / D0236_REL

d0238_manifest = (
    d0238 /
    "10_target_array_corrective_execution_authorization.v1.SHA256SUMS"
)

assert sha(d0238_manifest) == D0238_MANIFEST_SHA

auth_path = (
    d0238 /
    "01_target_array_corrective_execution_authorization.v1.json"
)

role_path = (
    d0237 /
    "01_target_array_semantic_role_governance.v1.json"
)

predecessor_record_path = (
    d0236 /
    "01_b1_corrective_successor_record.v1.json"
)

old_trace_path = (
    d0236 /
    "05_traceability_source_local_domain_inputs.WHITESPACE_CORRECTED_SUCCESSOR.v1.json"
)

auth = json.loads(
    auth_path.read_text(encoding="utf-8")
)

assert auth["operational_authorization"]["created"] is True
assert auth["operational_authorization"]["execution_performed"] is False

assert (
    auth["operational_authorization"]["authorized_future_execution_id"]
    == "D0239"
)

assert (
    auth["expected_D0239_output"]["traceability_domain_successor_sha256"]
    == EXPECTED_TRACE_SHA
)

assert (
    auth["expected_D0239_output"]["traceability_domain_successor_size_bytes"]
    == EXPECTED_TRACE_SIZE
)

role = json.loads(
    role_path.read_text(encoding="utf-8")
)

for name in [TARGET1, TARGET2]:
    b = role["field_role_bindings"][name]

    assert b["collection_semantic_role"] == "IDENTIFIER_SET_ARRAY"
    assert b["semantic_order"] == "ORDER_IRRELEVANT"

    assert (
        b["canonical_order"]
        == "ASCENDING_LEXICOGRAPHIC_EXACT_UTF8_BYTES"
    )

    assert b["duplicate_values_allowed"] is False

old_raw = old_trace_path.read_bytes()

assert sha(old_trace_path) == OLD_TRACE_SHA
assert not old_raw.endswith(b"\n")

duplicate_keys = []

def hook(pairs):
    out = {}

    for key, value in pairs:
        if key in out:
            duplicate_keys.append(key)

        out[key] = value

    return out

old_obj = json.loads(
    old_raw.decode("utf-8"),
    object_pairs_hook=hook,
)

assert duplicate_keys == []
assert canonical(old_obj).encode("utf-8") == old_raw

new_obj = deepcopy(old_obj)

changed_paths = []

t1_count = 0
t1_changed = 0
t1_dup = 0

t2_count = 0
t2_changed = 0
t2_dup = 0

for index, record in enumerate(new_obj["records"]):
    fields = record["observed_relevant_fields"]

    if TARGET1 in fields:
        values = fields[TARGET1]

        t1_count += 1

        if len(values) != len(set(values)):
            t1_dup += 1

        ordered = sorted(
            values,
            key=lambda x: x.encode("utf-8"),
        )

        assert Counter(values) == Counter(ordered)

        if values != ordered:
            t1_changed += 1

            changed_paths.append(
                f"$.records[{index}].observed_relevant_fields.{TARGET1}"
            )

        fields[TARGET1] = ordered

    if TARGET2 in fields:
        values = fields[TARGET2]

        t2_count += 1

        if len(values) != len(set(values)):
            t2_dup += 1

        ordered = sorted(
            values,
            key=lambda x: x.encode("utf-8"),
        )

        if values != ordered:
            t2_changed += 1

        assert values == ordered

assert (t1_count, t1_changed, t1_dup) == (109, 77, 0)
assert (t2_count, t2_changed, t2_dup) == (109, 0, 0)

assert len(changed_paths) == 77
assert len(set(changed_paths)) == 77

path_sha = hashlib.sha256(
    "\n".join(changed_paths).encode("utf-8")
).hexdigest()

assert path_sha == CHANGED_PATH_LIST_SHA

allowed = set(changed_paths)
seen = []

def verify_only_allowed(a, b, path="$"):
    if path in allowed:
        assert isinstance(a, list)
        assert isinstance(b, list)

        assert a != b
        assert Counter(a) == Counter(b)

        assert (
            b
            == sorted(
                b,
                key=lambda x: x.encode("utf-8"),
            )
        )

        seen.append(path)
        return

    assert type(a) is type(b), path

    if isinstance(a, dict):
        assert list(a.keys()) == list(b.keys()), path

        for key in a:
            verify_only_allowed(
                a[key],
                b[key],
                f"{path}.{key}",
            )

        return

    if isinstance(a, list):
        assert len(a) == len(b), path

        for index, (left, right) in enumerate(zip(a, b)):
            verify_only_allowed(
                left,
                right,
                f"{path}[{index}]",
            )

        return

    assert a == b, path

verify_only_allowed(
    old_obj,
    new_obj,
)

assert set(seen) == allowed
assert len(seen) == 77

expected_new_raw = canonical(
    new_obj
).encode("utf-8")

assert hashlib.sha256(
    expected_new_raw
).hexdigest() == EXPECTED_TRACE_SHA

assert len(expected_new_raw) == EXPECTED_TRACE_SIZE
assert not expected_new_raw.endswith(b"\n")

child_path = (
    ROOT /
    "01_traceability_source_local_domain_inputs."
    "TARGET_ARRAY_CANONICAL_ORDER_CORRECTED_SUCCESSOR.v1.json"
)

child_raw = child_path.read_bytes()

assert child_raw == expected_new_raw
assert sha(child_path) == EXPECTED_TRACE_SHA

child_obj = json.loads(
    child_raw.decode("utf-8")
)

assert canonical(child_obj).encode("utf-8") == child_raw

execution_path = (
    ROOT /
    "02_target_array_canonical_order_corrective_execution_record.v1.json"
)

execution_raw = execution_path.read_bytes()

assert not execution_raw.endswith(b"\n")

execution = json.loads(
    execution_raw.decode("utf-8")
)

assert canonical(execution).encode("utf-8") == execution_raw

assert execution["decision"] == "0239"

assert (
    execution["status"]
    == "TARGET_ARRAY_CANONICAL_ORDER_CORRECTIVE_EXECUTION_COMPLETED_WITHOUT_B2"
)

assert execution["authorization_basis"]["D0238_commit"] == D0238_HEAD
assert execution["authorization_basis"]["D0238_tree"] == D0238_TREE

assert (
    execution["authorization_basis"]["D0238_manifest_sha256"]
    == D0238_MANIFEST_SHA
)

assert execution["execution"]["performed"] is True
assert execution["execution"]["target_field"] == TARGET1
assert execution["execution"]["target_occurrence_count"] == 109
assert execution["execution"]["exact_reorder_count"] == 77
assert execution["execution"]["duplicate_array_count"] == 0
assert execution["execution"]["changed_path_count"] == 77

assert (
    execution["execution"]["changed_path_list_sha256"]
    == CHANGED_PATH_LIST_SHA
)

assert execution["execution"]["target_membership_preserved"] is True
assert execution["execution"]["record_order_preserved"] is True
assert execution["execution"]["non_target_parsed_values_preserved"] is True

assert execution["execution"]["target2_field"] == TARGET2
assert execution["execution"]["target2_occurrence_count"] == 109
assert execution["execution"]["target2_reorder_count"] == 0
assert execution["execution"]["target2_correction_performed"] is False

assert (
    execution["execution"]["output_traceability_domain_sha256"]
    == EXPECTED_TRACE_SHA
)

assert (
    execution["execution"]["output_traceability_domain_size_bytes"]
    == EXPECTED_TRACE_SIZE
)

predecessor_record = json.loads(
    predecessor_record_path.read_text(encoding="utf-8")
)

expected_source_results = deepcopy(
    predecessor_record["source_results"]
)

assert (
    expected_source_results["ENUMERATION"]["profile_successor_sha256"]
    == ENUM_PROFILE_SHA
)

assert (
    expected_source_results["ENUMERATION"]["domain_input_successor_sha256"]
    == ENUM_DOMAIN_SHA
)

assert (
    expected_source_results["TRACEABILITY"]["profile_successor_sha256"]
    == TRACE_PROFILE_SHA
)

assert (
    expected_source_results["TRACEABILITY"]["domain_input_successor_sha256"]
    == OLD_TRACE_SHA
)

expected_source_results[
    "TRACEABILITY"
][
    "domain_input_successor_sha256"
] = EXPECTED_TRACE_SHA

assert execution["source_results"] == expected_source_results

assert (
    execution["source_results"]["TRACEABILITY"]["domain_input_successor_sha256"]
    == EXPECTED_TRACE_SHA
)

assert (
    execution["source_results"]["ENUMERATION"]["profile_successor_sha256"]
    == ENUM_PROFILE_SHA
)

assert (
    execution["source_results"]["ENUMERATION"]["domain_input_successor_sha256"]
    == ENUM_DOMAIN_SHA
)

assert (
    execution["source_results"]["TRACEABILITY"]["profile_successor_sha256"]
    == TRACE_PROFILE_SHA
)

for value in execution["later_phase_authorization"].values():
    assert value is False

for value in execution["substantive_results_established"].values():
    assert value is False

for value in execution["preserved_boundaries"].values():
    assert value is False

conformance_path = (
    ROOT /
    "03_target_array_conformance_record.v1.json"
)

conformance_raw = conformance_path.read_bytes()

assert not conformance_raw.endswith(b"\n")

conformance = json.loads(
    conformance_raw.decode("utf-8")
)

assert canonical(conformance).encode("utf-8") == conformance_raw

assert conformance["decision"] == "0239"

assert (
    conformance["predecessor_traceability_domain_sha256"]
    == OLD_TRACE_SHA
)

assert (
    conformance["corrected_traceability_domain_sha256"]
    == EXPECTED_TRACE_SHA
)

assert (
    conformance["corrected_traceability_domain_size_bytes"]
    == EXPECTED_TRACE_SIZE
)

assert conformance["changed_path_count"] == 77

assert (
    conformance["changed_path_list_sha256"]
    == CHANGED_PATH_LIST_SHA
)

t1 = conformance[TARGET1]

assert t1["occurrence_count"] == 109
assert t1["reordered_count"] == 77
assert t1["duplicate_array_count_before"] == 0
assert t1["unsorted_array_count_after"] == 0
assert t1["duplicate_array_count_after"] == 0
assert t1["membership_preserved"] is True

t2 = conformance[TARGET2]

assert t2["occurrence_count"] == 109
assert t2["reordered_count"] == 0
assert t2["duplicate_array_count_before"] == 0
assert t2["unsorted_array_count_after"] == 0
assert t2["duplicate_array_count_after"] == 0
assert t2["value_and_order_preserved"] is True

assert conformance[
    "structural_preservation"
]["record_order_preserved"] is True

assert conformance[
    "structural_preservation"
]["non_target_parsed_values_preserved"] is True

assert conformance[
    "structural_preservation"
]["unexpected_non_target_change_count"] == 0

assert conformance[
    "byte_properties"
]["generic_D0227_json_serialization_verified"] is True

assert conformance[
    "byte_properties"
]["final_lf_present"] is False

# Package must contain exactly the five output types authorized by D0238.
expected_files = {
    "01_traceability_source_local_domain_inputs."
    "TARGET_ARRAY_CANONICAL_ORDER_CORRECTED_SUCCESSOR.v1.json",

    "02_target_array_canonical_order_corrective_execution_record.v1.json",

    "03_target_array_conformance_record.v1.json",

    "04_verify_target_array_canonical_order_corrective_successor.v1.py",

    "05_target_array_canonical_order_corrective_successor.v1.SHA256SUMS",
}

actual_files = {
    p.name
    for p in ROOT.iterdir()
    if p.is_file()
}

assert actual_files == expected_files

manifest_path = (
    ROOT /
    "05_target_array_canonical_order_corrective_successor.v1.SHA256SUMS"
)

manifest_lines = [
    line
    for line in manifest_path.read_text(
        encoding="utf-8"
    ).splitlines()
    if line.strip()
]

assert len(manifest_lines) == 4

listed = set()

for line in manifest_lines:
    digest, name = line.split("  ", 1)

    path = ROOT / name

    assert path.is_file()
    assert sha(path) == digest

    listed.add(name)

assert listed == expected_files - {
    "05_target_array_canonical_order_corrective_successor.v1.SHA256SUMS"
}

print("D0239_TARGET_ARRAY_CORRECTIVE_SUCCESSOR_VERIFIER=PASS")

print("D0238_COMMIT_BINDING=PASS")
print("D0238_TREE_BINDING=PASS")
print("D0238_MANIFEST_BINDING=PASS")

print("D0239_EXECUTION_PERFORMED=YES")

print("TARGET1_OCCURRENCE_COUNT=109")
print("TARGET1_REORDER_COUNT=77")
print("TARGET1_DUPLICATE_COUNT=0")
print("TARGET1_UNSORTED_AFTER=0")

print("TARGET2_OCCURRENCE_COUNT=109")
print("TARGET2_REORDER_COUNT=0")
print("TARGET2_DUPLICATE_COUNT=0")
print("TARGET2_UNSORTED_AFTER=0")

print("CHANGED_PATH_COUNT=77")
print("CHANGED_PATH_LIST_SHA256=" + CHANGED_PATH_LIST_SHA)

print("NON_TARGET_PARSED_VALUE_CHANGE_COUNT=0")
print("RECORD_ORDER_CHANGED=NO")
print("TARGET1_MEMBERSHIP_CHANGED=NO")

print("CORRECTED_TRACE_DOMAIN_SHA256=" + EXPECTED_TRACE_SHA)
print("CORRECTED_TRACE_DOMAIN_SIZE_BYTES=" + str(EXPECTED_TRACE_SIZE))
print("CORRECTED_TRACE_DOMAIN_FINAL_LF=NO")

print("TRACE_DOMAIN_HASH_REBOUND=YES")
print("UNCHANGED_CHILD_HASH_BINDINGS_PRESERVED=YES")

print("B2_AUTHORIZED=NO")
print("B2_READINESS_ESTABLISHED=NO")

print("CROSS_SOURCE_JOIN_PERFORMED=NO")
print("CONCRETE_MAPPING_CREATED=NO")
print("REQ06_REQ14_DETERMINATION_PERFORMED=NO")
