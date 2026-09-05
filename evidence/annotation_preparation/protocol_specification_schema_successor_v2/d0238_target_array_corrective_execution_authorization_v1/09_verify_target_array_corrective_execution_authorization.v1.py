#!/usr/bin/env python3

from pathlib import Path
from copy import deepcopy
from collections import Counter
import hashlib
import json
import os
import subprocess

ROOT = Path(__file__).resolve().parent

D0237_HEAD = (
    "3c2bfabbd76ad8e0f5df28fd0cdfc4da7acc47ab"
)

D0237_TREE = (
    "81f49e82767d992d7b0b69430df6ca9ce39bdab5"
)

D0237_MANIFEST_SHA = (
    "d0d16581d995b6651330dbbd97d5c6cd87c9f761ab457891348786e00085a87e"
)

D0236_HEAD = (
    "98c9f70e41a21cb9d0b10feba5c7b3f92ba0b18d"
)

TRACE_DOMAIN_SHA = (
    "d02d67addc0af427d71da66588ce6e1020017007dbdae76b3ef0c6cb3d5b625d"
)

EXPECTED_SHA = (
    "9cee6cb560179386da9104d12d353a581dfe8c6149c5890b19c13b0973efc9f2"
)

EXPECTED_SIZE = 486907

TARGET1 = "candidate_schema_v2_carrier_families"
TARGET2 = "matrix_unit_analysis_field_classes"

BASE = (
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2"
)

D0237_REL = (
    BASE
    + "/d0237_target_array_semantic_role_governance_v1"
)

D0236_REL = (
    BASE
    + "/d0236_d0235_b1_canonicalization_role_refinement_corrective_successor_v1"
)

D0227_REL = (
    BASE
    + "/schema_v2_req06_req14_accounting_satisfaction_evidence_gap_and_"
      "acquisition_specification_study_v2_corrective_successor_for_"
      "aser04_aser07_remaining_findings_revision_v5"
)

def sha(path):
    return hashlib.sha256(
        Path(path).read_bytes()
    ).hexdigest()

def resolve_repo():
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

REPO = resolve_repo()

assert subprocess.check_output(
    [
        "git",
        "-C",
        str(REPO),
        "rev-parse",
        f"{D0237_HEAD}^{{tree}}",
    ],
    text=True,
).strip() == D0237_TREE

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

D0237 = REPO / D0237_REL
D0236 = REPO / D0236_REL
D0227 = REPO / D0227_REL

d0237_manifest = (
    D0237 /
    "10_target_array_semantic_role_governance.v1.SHA256SUMS"
)

assert sha(d0237_manifest) == D0237_MANIFEST_SHA

assert (
    REPO /
    "documentation/decisions/"
    "0237-govern-target-array-semantic-roles-without-correction-or-b2-authorization.md"
).read_bytes() == (
    ROOT /
    "04_decision0237.EXACT_COPY.md"
).read_bytes()

assert (
    D0237 /
    "01_target_array_semantic_role_governance.v1.json"
).read_bytes() == (
    ROOT /
    "05_d0237_role_governance.EXACT_COPY.v1.json"
).read_bytes()

assert d0237_manifest.read_bytes() == (
    ROOT /
    "06_d0237_manifest.EXACT_COPY.v1.SHA256SUMS"
).read_bytes()

assert (
    D0236 /
    "01_b1_corrective_successor_record.v1.json"
).read_bytes() == (
    ROOT /
    "07_d0236_successor_record.EXACT_COPY.v1.json"
).read_bytes()

assert (
    D0227 /
    "02_accounting_evidence_canonicalization_and_detached_hash_rules.v5.json"
).read_bytes() == (
    ROOT /
    "08_d0227_canonicalization_rules.EXACT_COPY.v5.json"
).read_bytes()

auth = json.loads(
    (
        ROOT /
        "01_target_array_corrective_execution_authorization.v1.json"
    ).read_text(encoding="utf-8")
)

sim = json.loads(
    (
        ROOT /
        "02_exact_correction_simulation_and_hash_binding.v1.json"
    ).read_text(encoding="utf-8")
)

assert auth["decision"] == "0238"

assert (
    auth["status"]
    == "D0239_TARGET_ARRAY_CANONICAL_ORDER_CORRECTIVE_EXECUTION_AUTHORIZED_NOT_EXECUTED"
)

op = auth["operational_authorization"]

assert op["created"] is True
assert op["execution_performed"] is False
assert op["authorized_future_execution_id"] == "D0239"

corr = auth["authorized_correction"]

assert corr["target_field"] == TARGET1
assert corr["collection_role"] == "IDENTIFIER_SET_ARRAY"

assert (
    corr["operation"]
    == "SORT_EACH_TARGET_ARRAY_ASCENDING_BY_EXACT_UTF8_BYTES"
)

assert corr["target_occurrence_count"] == 109
assert corr["exact_expected_reorder_count"] == 77
assert corr["duplicate_array_count"] == 0

assert corr["membership_change_authorized"] is False
assert corr["element_insertion_authorized"] is False
assert corr["element_deletion_authorized"] is False
assert corr["element_value_change_authorized"] is False

unchanged = auth["explicitly_unchanged_target"]

assert unchanged["field"] == TARGET2
assert unchanged["occurrence_count"] == 109
assert unchanged["expected_reorder_count"] == 0
assert unchanged["duplicate_array_count"] == 0
assert unchanged["correction_authorized"] is False

expected = auth["expected_D0239_output"]

assert expected[
    "traceability_domain_successor_sha256"
] == EXPECTED_SHA

assert expected[
    "traceability_domain_successor_size_bytes"
] == EXPECTED_SIZE

assert expected["exact_changed_json_path_count"] == 77
assert expected["unexpected_non_target_change_count"] == 0

for value in auth["later_phase_authorization"].values():
    assert value is False

trace = (
    D0236 /
    "05_traceability_source_local_domain_inputs.WHITESPACE_CORRECTED_SUCCESSOR.v1.json"
)

raw = trace.read_bytes()

assert sha(trace) == TRACE_DOMAIN_SHA
assert not raw.endswith(b"\n")

duplicate_keys = []

def hook(pairs):
    out = {}

    for key, value in pairs:
        if key in out:
            duplicate_keys.append(key)

        out[key] = value

    return out

original = json.loads(
    raw.decode("utf-8"),
    object_pairs_hook=hook,
)

assert duplicate_keys == []

def emit_string(value):
    out = ['"']

    for ch in value:
        cp = ord(ch)

        assert not (0xD800 <= cp <= 0xDFFF)

        if cp == 0x22:
            out.append('\\"')

        elif cp == 0x5C:
            out.append('\\\\')

        elif cp <= 0x1F:
            out.append(
                "\\u"
                + format(cp, "04x")
            )

        else:
            out.append(ch)

    out.append('"')

    return "".join(out)

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
            "floating point forbidden"
        )

    if isinstance(value, str):
        return emit_string(value)

    if isinstance(value, list):
        return (
            "["
            + ",".join(
                canonical(x)
                for x in value
            )
            + "]"
        )

    if isinstance(value, dict):
        keys = sorted(
            value,
            key=lambda x: x.encode("utf-8"),
        )

        return (
            "{"
            + ",".join(
                emit_string(k)
                + ":"
                + canonical(value[k])
                for k in keys
            )
            + "}"
        )

    raise AssertionError(type(value))

assert canonical(original).encode("utf-8") == raw

corrected = deepcopy(original)

t1_count = 0
t1_changed = 0
t1_dup = 0

t2_count = 0
t2_changed = 0
t2_dup = 0

allowed = []

for index, record in enumerate(corrected["records"]):
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

            allowed.append(
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

assert (
    t1_count,
    t1_changed,
    t1_dup,
) == (
    109,
    77,
    0,
)

assert (
    t2_count,
    t2_changed,
    t2_dup,
) == (
    109,
    0,
    0,
)

allowed = set(allowed)
seen = []

def verify_only_allowed(a, b, path="$"):
    if path in allowed:
        assert isinstance(a, list)
        assert isinstance(b, list)
        assert a != b
        assert Counter(a) == Counter(b)
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

        for i, (left, right) in enumerate(zip(a, b)):
            verify_only_allowed(
                left,
                right,
                f"{path}[{i}]",
            )

        return

    assert a == b, path

verify_only_allowed(
    original,
    corrected,
)

assert set(seen) == allowed
assert len(seen) == 77

corrected_bytes = canonical(corrected).encode("utf-8")

assert hashlib.sha256(
    corrected_bytes
).hexdigest() == EXPECTED_SHA

assert len(corrected_bytes) == EXPECTED_SIZE
assert not corrected_bytes.endswith(b"\n")

assert sim[
    "expected_future_output"
]["sha256"] == EXPECTED_SHA

assert sim[
    "simulation_facts"
]["candidate_schema_v2_carrier_families_exact_reorder_count"] == 77

assert sim[
    "simulation_facts"
]["unexpected_non_target_change_count"] == 0

assert sim[
    "previous_failed_read_only_design"
]["repository_defect_established"] is False

manifest = (
    ROOT /
    "10_target_array_corrective_execution_authorization.v1.SHA256SUMS"
)

lines = [
    x
    for x in manifest.read_text(
        encoding="utf-8"
    ).splitlines()
    if x.strip()
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
    "10_target_array_corrective_execution_authorization.v1.SHA256SUMS"
}

print("D0238_TARGET_ARRAY_CORRECTIVE_EXECUTION_AUTHORIZATION_VERIFIER=PASS")

print("D0237_COMMIT_BINDING=PASS")
print("D0237_TREE_BINDING=PASS")
print("D0237_MANIFEST_BINDING=PASS")

print("D0239_CORRECTIVE_EXECUTION_AUTHORIZED=YES")
print("D0239_EXECUTION_PERFORMED=NO")

print("AUTHORIZED_TARGET_FIELD=" + TARGET1)
print("AUTHORIZED_TARGET_OCCURRENCE_COUNT=109")
print("AUTHORIZED_EXACT_REORDER_COUNT=77")
print("AUTHORIZED_DUPLICATE_ARRAY_COUNT=0")

print("TARGET2_CORRECTION_AUTHORIZED=NO")
print("TARGET2_EXPECTED_REORDER_COUNT=0")

print("EXPECTED_D0239_TRACE_DOMAIN_SHA256=" + EXPECTED_SHA)
print("EXPECTED_D0239_TRACE_DOMAIN_SIZE_BYTES=" + str(EXPECTED_SIZE))

print("B2_AUTHORIZED=NO")
print("B2_READINESS_ESTABLISHED=NO")

print("CROSS_SOURCE_JOIN_AUTHORIZED=NO")
print("CONCRETE_MAPPING_AUTHORIZED=NO")
print("REQ06_REQ14_DETERMINATION_AUTHORIZED=NO")
