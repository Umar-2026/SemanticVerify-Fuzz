#!/usr/bin/env python3
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys

EXPECTED_HEAD = "ee7fca936998e437e264dbd86cb1b153b3ed626d"
EXPECTED_TREE = "73fd157ae7b0b1e5b29151ccad749d1adb22cf0e"
EXPECTED_MANIFEST = "0cdcf53caf50c274263923f904c0f0557f2626093ade17fe5fd52ecc605f025a"

EXPECTED_ROOTS = [
    {
        "directory": "evidence/annotation_preparation/protocol_specification_schema_successor_v2/schema_v2_requirement_to_semantic_unit_completed_human_positive_binding_evidence_record_v1",
        "tree": "3ef024e1e892c02bda5882c47dc9bb0c342c64ab",
        "member": "evidence/annotation_preparation/protocol_specification_schema_successor_v2/schema_v2_requirement_to_semantic_unit_completed_human_positive_binding_evidence_record_v1/02_completed_human_positive_binding_evidence_packet.EXACT_COPY.v1.md",
        "sha": "effd2848702219741e3814d2dc283284c92ab07f49980cd799fde351ecb8b685",
        "blob": "7f0ea290e6f49c06fd7102d7b0eef5bd306697a5",
    },
    {
        "directory": "evidence/annotation_preparation/protocol_specification_schema_successor_v2/schema_v2_requirement_to_semantic_unit_bounded_technical_adjudication_completed_human_record_v1",
        "tree": "6efeb7db0bdeb6c04c02bf0eaf7cc19419afcc26",
        "member": "evidence/annotation_preparation/protocol_specification_schema_successor_v2/schema_v2_requirement_to_semantic_unit_bounded_technical_adjudication_completed_human_record_v1/01_returned_human_technical_adjudication.EXACT_COPY.v1.md",
        "sha": "ad35ddfefea1d79db79e36f24ef823407f977a682efcdf23a98a1cbc5ffd7eda",
        "blob": "cc14c8f9424caae4a85660c83a74491651d29c1b",
    },
    {
        "directory": "evidence/annotation_preparation/protocol_specification_schema_successor_v2/schema_v2_requirement_to_semantic_unit_bounded_supported_binding_promotion_successor_v1",
        "tree": "23b71c3ec495321bc0275b24dbd220ec26a70ab8",
        "member": "evidence/annotation_preparation/protocol_specification_schema_successor_v2/schema_v2_requirement_to_semantic_unit_bounded_supported_binding_promotion_successor_v1/01_bounded_supported_binding_successor_matrix.v1.json",
        "sha": "c74240135454c6746b0829306d60c5a818c67d06a4148116de0f21891669a940",
        "blob": "336573866fc84ab4b4379ee4f331fb448252acfb",
    },
]

EXPECTED_TOKENS = [
    "requirement",
    "semantic",
    "unit",
    "crosswalk",
    "binding",
    "mapping",
    "matrix",
    "traceability",
    "adjudication",
    "evidence",
]

repo = Path(
    os.environ.get(
        "SVF_REPO_ROOT",
        "/openbayes/home/semanticverify-fuzz-research",
    )
)

pkg = Path(
    os.environ.get(
        "SVF_PACKAGE_DIR",
        Path(__file__).resolve().parent,
    )
)

record_path = pkg / "01_bounded_crosswalk_locator_discovery_authorization.v1.json"
scope_path = pkg / "02_bounded_crosswalk_locator_discovery_authorization_scope.v1.md"

def run(*args):
    return subprocess.check_output(
        args,
        cwd=repo,
        text=True,
    ).strip()

def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def no_dup(pairs):
    out = {}
    for k, v in pairs:
        if k in out:
            raise ValueError("duplicate JSON key: " + k)
        out[k] = v
    return out

raw = record_path.read_bytes()

if raw.endswith(b"\n"):
    raise AssertionError("authorization record has final LF")

record = json.loads(
    raw.decode("utf-8"),
    object_pairs_hook=no_dup,
)

canonical = json.dumps(
    record,
    ensure_ascii=False,
    sort_keys=True,
    separators=(",", ":"),
).encode("utf-8")

assert raw == canonical

assert run("git", "rev-parse", "HEAD") == EXPECTED_HEAD
assert run("git", "rev-parse", "HEAD^{tree}") == EXPECTED_TREE

pred = record["predecessor"]

assert pred["decision"] == "D0243"
assert pred["commit"] == EXPECTED_HEAD
assert pred["tree"] == EXPECTED_TREE
assert pred["manifest_sha256"] == EXPECTED_MANIFEST

auth = record["authorization"]

assert auth["authorized"] is True
assert auth["executed"] is False
assert auth["designated_execution_decision"] == "D0245"
assert auth["recursion_depth"] == 1

assert auth["filename_filter"]["tokens"] == EXPECTED_TOKENS
assert auth["filename_filter"]["match_mode"] == "CASE_INSENSITIVE_SUBSTRING_OR"
assert auth["filename_filter"]["establishes_authority"] is False
assert auth["filename_filter"]["establishes_crosswalk_semantics"] is False
assert auth["filename_filter"]["establishes_evidence_adequacy"] is False

assert len(auth["roots"]) == 3

for expected, actual in zip(EXPECTED_ROOTS, auth["roots"]):
    assert actual["directory"] == expected["directory"]
    assert actual["git_tree_object"] == expected["tree"]

    assert run(
        "git",
        "rev-parse",
        "HEAD:" + expected["directory"],
    ) == expected["tree"]

    assert run(
        "git",
        "cat-file",
        "-t",
        expected["tree"],
    ) == "tree"

    anchor = actual["anchor_member"]

    assert anchor["path"] == expected["member"]
    assert anchor["sha256"] == expected["sha"]
    assert anchor["git_blob"] == expected["blob"]

    assert sha256(repo / expected["member"]) == expected["sha"]

    assert run(
        "git",
        "rev-parse",
        "HEAD:" + expected["member"],
    ) == expected["blob"]

non = record["explicit_nonauthorization"]

required_false = [
    "b2_authorized",
    "b2_executed",
    "c2_additional_evidence_acquisition_authorized",
    "c2_executed",
    "c3_adjudication_authorized",
    "c4_closure_authorized",
    "c5_b2_readiness_reassessment_authorized",
    "c6_b2_authorization_authorized",
    "candidate_admissibility_evaluation_authorized",
    "candidate_disposition_creation_authorized",
    "concrete_mapping_authorized",
    "external_network_access_authorized",
    "file_content_read_authorized",
    "pair_reclassification_authorized",
    "repository_wide_search_authorized",
    "req06_req14_determination_authorized",
    "source_evidence_acquisition_authorized",
    "tree_recursion_authorized",
]

for key in required_false:
    assert non[key] is False, key

results = record["results_not_established"]

for value in results.values():
    assert value is False

assert record["status"] == "BOUNDED_CROSSWALK_LOCATOR_DISCOVERY_AUTHORIZED_NOT_EXECUTED"

scope = scope_path.read_text(encoding="utf-8")

markers = [
    "AUTHORIZED — NOT EXECUTED",
    "LOCATOR_DISCOVERY_AUTHORIZED=YES",
    "LOCATOR_DISCOVERY_EXECUTED=NO",
    "C2_AUTHORIZED=NO",
    "C2_EXECUTED=NO",
    "B2_AUTHORIZED=NO",
    "B2_EXECUTED=NO",
    "INDEPENDENT_READ_ONLY_VERIFY_D0244_BEFORE_ANY_D0245_LOCATOR_DISCOVERY_EXECUTION",
]

for marker in markers:
    assert marker in scope, marker

print("D0244_BOUNDED_LOCATOR_DISCOVERY_AUTHORIZATION_VERIFIER=PASS")
print("D0243_PREDECESSOR_BINDING=PASS")
print("DISCOVERY_ROOT_COUNT=3")
print("DISCOVERY_ROOT_TREE_BINDINGS=PASS")
print("DISCOVERY_RECURSION_DEPTH=1")
print("FIXED_FILENAME_TOKEN_COUNT=10")
print("LOCATOR_DISCOVERY_AUTHORIZED=YES")
print("LOCATOR_DISCOVERY_EXECUTED=NO")
print("FILE_CONTENT_READ_AUTHORIZED=NO")
print("EXTERNAL_NETWORK_ACCESS_AUTHORIZED=NO")
print("C2_AUTHORIZED=NO")
print("C2_EXECUTED=NO")
print("C3_AUTHORIZED=NO")
print("B2_READINESS_ESTABLISHED=NO")
print("B2_AUTHORIZED=NO")
print("B2_EXECUTED=NO")
print("SAFE_D0244_VERIFIER=PASS")
