#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import os
import subprocess

ROOT = Path(__file__).resolve().parent

D0235_HEAD = (
    "3cda6cf4ea79434b8ed899ff3b5d28a8dc68d205"
)

D0235_TREE = (
    "acb702e968c762d215976a91d25897580722dd3b"
)

D0235_MANIFEST_SHA = (
    "e463755f26608bae56096518e31a2033b6ea3b9821132909350df858708a5c57"
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

TRACE_DOMAIN_SHA = (
    "d02d67addc0af427d71da66588ce6e1020017007dbdae76b3ef0c6cb3d5b625d"
)

D0235_REL = (
    "evidence/annotation_preparation/"
    "protocol_specification_schema_successor_v2/"
    "d0235_b1_accounting_source_domain_acquisition_v1"
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

    assert (
        subprocess.check_output(
            [
                "git",
                "-C",
                str(repo),
                "rev-parse",
                "--is-inside-work-tree",
            ],
            text=True,
        ).strip()
        == "true"
    )

    return repo

REPO = resolve_repo()
D0235 = REPO / D0235_REL

assert D0235.is_dir()

resolved_d0235_tree = subprocess.check_output(
    [
        "git",
        "-C",
        str(REPO),
        "rev-parse",
        f"{D0235_HEAD}^{{tree}}",
    ],
    text=True,
).strip()

assert resolved_d0235_tree == D0235_TREE

assert sha(
    D0235 /
    "11_b1_execution_package.v1.SHA256SUMS"
) == D0235_MANIFEST_SHA

assert sha(
    ROOT /
    "09_d0235_execution_manifest.EXACT_COPY.v1.SHA256SUMS"
) == D0235_MANIFEST_SHA

old_exec = json.loads(
    (
        D0235 /
        "01_b1_execution_record.v1.json"
    ).read_text(encoding="utf-8")
)

copied_exec = json.loads(
    (
        ROOT /
        "08_d0235_execution_record.EXACT_COPY.v1.json"
    ).read_text(encoding="utf-8")
)

assert old_exec == copied_exec

successor = json.loads(
    (
        ROOT /
        "01_b1_corrective_successor_record.v1.json"
    ).read_text(encoding="utf-8")
)

assert successor["decision"] == "0236"

assert (
    successor["status"]
    == "D0235_B1_WHITESPACE_HASH_CORRECTIVE_SUCCESSOR_WITH_ARRAY_ROLE_UNRESOLVED"
)

pred = successor["predecessor_execution"]

assert pred["commit"] == D0235_HEAD
assert pred["tree"] == D0235_TREE
assert pred["manifest_sha256"] == D0235_MANIFEST_SHA
assert pred["historical_b1_execution_preserved"] is True

scope = successor["corrective_scope"]

assert scope["b1_reexecuted"] is False
assert scope["original_authorized_sources_reparsed"] is False
assert scope["d0235_modified"] is False
assert scope["final_lf_removed_from_four_child_successors"] is True
assert scope["child_hashes_rebound_to_successor_bytes"] is True
assert scope["source_local_role_refinement_created"] is True
assert scope["target_array_order_changed"] is False
assert scope["target_array_identifier_set_role_governed"] is False
assert scope["full_d0227_array_semantics_conformance_established"] is False
assert scope["full_d0227_canonical_hash_target_conformance_established"] is False

assert (
    successor["preserved_execution_facts"]
    == old_exec["execution"]
)

pairs = [
    (
        D0235 /
        "02_enumeration_source_local_profile.v1.json",

        ROOT /
        "02_enumeration_source_local_profile.WHITESPACE_CORRECTED_SUCCESSOR.v1.json",

        ENUM_PROFILE_SHA,

        successor["source_results"]["ENUMERATION"][
            "profile_successor_sha256"
        ],
    ),
    (
        D0235 /
        "03_traceability_source_local_profile.v1.json",

        ROOT /
        "03_traceability_source_local_profile.WHITESPACE_CORRECTED_SUCCESSOR.v1.json",

        TRACE_PROFILE_SHA,

        successor["source_results"]["TRACEABILITY"][
            "profile_successor_sha256"
        ],
    ),
    (
        D0235 /
        "04_enumeration_source_local_domain_inputs.v1.json",

        ROOT /
        "04_enumeration_source_local_domain_inputs.WHITESPACE_CORRECTED_SUCCESSOR.v1.json",

        ENUM_DOMAIN_SHA,

        successor["source_results"]["ENUMERATION"][
            "domain_input_successor_sha256"
        ],
    ),
    (
        D0235 /
        "05_traceability_source_local_domain_inputs.v1.json",

        ROOT /
        "05_traceability_source_local_domain_inputs.WHITESPACE_CORRECTED_SUCCESSOR.v1.json",

        TRACE_DOMAIN_SHA,

        successor["source_results"]["TRACEABILITY"][
            "domain_input_successor_sha256"
        ],
    ),
]

for old_path, new_path, expected_sha, declared_sha in pairs:
    old = old_path.read_bytes()
    new = new_path.read_bytes()

    assert old.endswith(b"\n")
    assert old[:-1] == new
    assert not new.endswith(b"\n")

    assert sha(new_path) == expected_sha
    assert declared_sha == expected_sha

    assert (
        json.loads(old.decode("utf-8"))
        == json.loads(new.decode("utf-8"))
    )

role_path = (
    ROOT /
    "06_source_local_role_refinement.v1.json"
)

role_raw = role_path.read_bytes()

assert not role_raw.endswith(b"\n")

role = json.loads(
    role_raw.decode("utf-8")
)

assert (
    successor["role_refinement"]["sha256"]
    == sha(role_path)
)

assert role["derivation_boundary"][
    "original_authorized_sources_reparsed"
] is False

assert role["derivation_boundary"][
    "b1_reexecuted"
] is False

assert role["derivation_boundary"][
    "cross_source_join_performed"
] is False

assert role["derivation_boundary"][
    "observed_source_local_values_changed"
] is False

assert role["enumeration_roles"][
    "PRIMARY_ENUMERATION_PAIR_ROW"
] == 18639

assert role["enumeration_roles"][
    "ENUMERATION_METADATA_OR_AUXILIARY"
] == 5

assert role["traceability_roles"][
    "REVIEWED_LEAF_FIELD"
] == 531

assert role["traceability_roles"][
    "SEMANTIC_UNIT_CONTEXT"
] == 109

assert role["traceability_roles"][
    "NESTED_CANDIDATE_DOMAIN_PATH_CONTEXT"
] == 97

assert role["traceability_roles"][
    "TRACEABILITY_METADATA_OR_AUXILIARY"
] == 3

target = role["target_array_role_audit"]

candidate = target[
    "candidate_schema_v2_carrier_families"
]

assert candidate["occurrences"] == 109
assert candidate["utf8_unsorted_occurrences"] == 77
assert candidate["duplicate_value_array_occurrences"] == 0
assert candidate["identifier_set_role_governed"] is False
assert candidate["order_changed"] is False

matrix = target[
    "matrix_unit_analysis_field_classes"
]

assert matrix["occurrences"] == 109
assert matrix["utf8_unsorted_occurrences"] == 0
assert matrix["duplicate_value_array_occurrences"] == 0
assert matrix["identifier_set_role_governed"] is False
assert matrix["order_changed"] is False

old_trace = json.loads(
    (
        D0235 /
        "05_traceability_source_local_domain_inputs.v1.json"
    ).read_text(encoding="utf-8")
)

new_trace = json.loads(
    (
        ROOT /
        "05_traceability_source_local_domain_inputs.WHITESPACE_CORRECTED_SUCCESSOR.v1.json"
    ).read_text(encoding="utf-8")
)

names = {
    "candidate_schema_v2_carrier_families",
    "matrix_unit_analysis_field_classes",
}

old_targets = []
new_targets = []

for document, sink in [
    (old_trace, old_targets),
    (new_trace, new_targets),
]:
    for record in document["records"]:
        fields = record["observed_relevant_fields"]

        for name in sorted(names):
            if name in fields:
                sink.append(
                    (
                        record["source_local_path"],
                        name,
                        fields[name],
                    )
                )

assert len(old_targets) == 218
assert old_targets == new_targets

candidate_unsorted = 0

for path, name, values in new_targets:
    if name != "candidate_schema_v2_carrier_families":
        continue

    ordered = sorted(
        values,
        key=lambda x: x.encode("utf-8"),
    )

    candidate_unsorted += int(
        values != ordered
    )

assert candidate_unsorted == 77

state = successor["canonicalization_state"]

assert state[
    "target_array_role_binding"
] == "NOT_ESTABLISHED"

assert state[
    "target_array_observed_order_preserved"
] is True

assert state[
    "full_d0227_array_semantics_conformance"
] == "NOT_ESTABLISHED"

assert state[
    "full_d0227_canonical_hash_target_conformance"
] == "NOT_ESTABLISHED"

for value in successor["later_phase_authorization"].values():
    assert value is False

for value in successor["substantive_results_established"].values():
    assert value is False

manifest = (
    ROOT /
    "12_d0235_b1_corrective_successor.v2.SHA256SUMS"
)

lines = [
    x
    for x in manifest.read_text(encoding="utf-8").splitlines()
    if x.strip()
]

listed = set()

for line in lines:
    digest, rel = line.split("  ", 1)

    p = ROOT / rel

    assert p.is_file(), rel
    assert sha(p) == digest, rel

    listed.add(rel)

actual = {
    p.name
    for p in ROOT.iterdir()
    if p.is_file()
}

assert actual == listed | {
    "12_d0235_b1_corrective_successor.v2.SHA256SUMS"
}

print("D0236_CORRECTIVE_SUCCESSOR_VERIFIER_V2=PASS")
print("REPOSITORY_ROOT_RESOLUTION=PASS")
print("D0235_COMMIT_BINDING=PASS")
print("D0235_TREE_BINDING=PASS")
print("D0235_MANIFEST_BINDING=PASS")

print("D0235_HISTORICAL_B1_EXECUTION_PRESERVED=YES")
print("B1_REEXECUTED_BY_D0236=NO")
print("ORIGINAL_AUTHORIZED_SOURCES_REPARSED_BY_D0236=NO")

print("FOUR_WHITESPACE_CORRECTED_CHILD_SUCCESSORS_VALID=YES")
print("FOUR_CHILD_HASHES_REBOUND_TO_SUCCESSOR_BYTES=YES")

print("TARGET_ARRAY_ORDER_PRESERVED=YES")
print("CANDIDATE_SCHEMA_V2_CARRIER_FAMILIES_UNSORTED_PRESERVED_COUNT=77")
print("TARGET_ARRAY_IDENTIFIER_SET_ROLE_GOVERNED=NO")

print("FULL_D0227_ARRAY_SEMANTICS_CONFORMANCE=NOT_ESTABLISHED")
print("FULL_D0227_CANONICAL_HASH_TARGET_CONFORMANCE=NOT_ESTABLISHED")

print("B2_AUTHORIZED=NO")
print("B2_READINESS_ESTABLISHED=NO")

print("CROSS_SOURCE_JOIN_PERFORMED=NO")
print("CONCRETE_MAPPING_CREATED=NO")
print("DOMAIN_FREEZE_CREATED=NO")
print("REQ06_REQ14_DETERMINATION_PERFORMED=NO")
