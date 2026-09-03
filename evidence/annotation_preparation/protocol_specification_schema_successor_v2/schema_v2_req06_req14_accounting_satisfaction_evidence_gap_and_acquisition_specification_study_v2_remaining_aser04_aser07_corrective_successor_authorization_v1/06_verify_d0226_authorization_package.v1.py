#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).parent

EXPECTED_D0225_COMMIT = (
    "7ce6da63d791a6e7aa3a5b85695b816ed852857e"
)

EXPECTED_D0225_TREE = (
    "2a6fde07204636d2ba62bbba2baa9a4cabffa07c"
)

EXPECTED_D0225_MANIFEST_SHA = (
    "311d1ff6b6002760db6c0c0b8d2ebd78dfc6416e92194b6ef6ee8fbc6966969c"
)

EXPECTED_RETURNED_REVIEW_SHA = (
    "daf3ac553885e3a8547cb48c9271015434d1b0c8f33cc51a3afd083f4e73627e"
)

def sha(path):
    return hashlib.sha256(
        Path(path).read_bytes()
    ).hexdigest()

record = json.loads(
    (
        ROOT /
        "01_remaining_corrective_authorization.v1.json"
    ).read_text(encoding="utf-8")
)

scope = json.loads(
    (
        ROOT /
        "02_remaining_corrective_scope_contract.v1.json"
    ).read_text(encoding="utf-8")
)

packaging = json.loads(
    (
        ROOT /
        "04_next_rereview_packaging_requirements.v1.json"
    ).read_text(encoding="utf-8")
)

assert record["decision"] == "0226"

assert (
    record["authorization_state"]
    == "AUTHORED_UNCONSUMED"
)

pred = record["predecessor_checkpoint"]

assert pred["decision0225_commit"] == EXPECTED_D0225_COMMIT
assert pred["decision0225_tree"] == EXPECTED_D0225_TREE

assert (
    pred["decision0225_package_manifest_sha256"]
    == EXPECTED_D0225_MANIFEST_SHA
)

assert (
    pred["returned_review_sha256"]
    == EXPECTED_RETURNED_REVIEW_SHA
)

assert record["predecessor_review"] == {
    "ASER04": "REVISION_REQUIRED",
    "ASER07": "REVISION_REQUIRED",
    "overall": "REVISION_REQUIRED",
}

assert record["corrective_scope"] == [
    "ASER04",
    "ASER07",
]

assert record["preserved_pass_items"] == [
    "ASER01",
    "ASER02",
    "ASER03",
    "ASER05",
    "ASER06",
    "ASER08",
    "ASER09",
]

aser04 = record["authorized_remaining_corrections"]["ASER04"]

assert aser04["canonical_json_string_and_member_name_escaping"] is True
assert aser04["canonical_byte_test_vectors"] is True
assert aser04["canonical_sha256_test_vectors"] is True

aser07 = record["authorized_remaining_corrections"]["ASER07"]

assert aser07["strict_freeze_before_witness_ordering"] is True
assert aser07["freeze_and_witness_commits_must_be_distinct"] is True
assert aser07["successful_freeze_commit_ancestry"] is True

assert (
    aser07[
        "checked_commits_bound_to_complete_freeze_record_and_witness_lineage"
    ]
    is True
)

one = record["one_time_authorizer"]

r03 = (
    ROOT /
    "03_authorize_bounded_remaining_corrective_successor_once.v1.py"
)

assert r03.is_file()
assert one["sha256"] == sha(r03)
assert one["execution_attempt_count"] == 0
assert one["executed"] is False
assert one["state"] == "AUTHORED_UNCONSUMED"
assert one["first_execution_authorized"] is True
assert one["first_attempt_consumes_authorization"] is True
assert one["rerun_authorized_after_first_attempt"] is False

for key, value in record["explicit_nonauthorization"].items():
    assert type(value) is bool
    assert value is False, key

assert scope["corrective_scope"] == [
    "ASER04",
    "ASER07",
]

assert (
    scope["ASER04"]["remaining_finding"]
    == "CANONICAL_JSON_STRING_ESCAPING"
)

assert (
    scope["ASER07"]["remaining_finding"]
    == "STRICT_FREEZE_BEFORE_WITNESS_ORDERING"
)

for key, value in scope["successor_boundary"].items():
    assert type(value) is bool
    assert value is False, key

req = packaging["requirements"]

assert req["preserve_source_bytes_exactly"] is True
assert req["bind_each_copy_by_sha256"] is True
assert req["include_in_next_independent_human_rereview_package"] is True
assert req["new_accounting_evidence_acquisition"] is False
assert req["new_domain_acquisition"] is False
assert req["new_mapping_creation"] is False
assert req["source_content_modification"] is False

manifest = (
    ROOT /
    "07_d0226_authorization_package.v1.SHA256SUMS"
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

    assert path.is_file()
    assert sha(path) == digest

    listed.add(rel)

actual = {
    p.name
    for p in ROOT.iterdir()
    if p.is_file()
}

assert (
    actual
    == listed | {
        "07_d0226_authorization_package.v1.SHA256SUMS"
    }
)

print("D0226_AUTHORIZATION_PACKAGE_VERIFIER=PASS")
print("AUTHORIZATION_STATE=AUTHORED_UNCONSUMED")
print("D0226_R03_EXECUTION_ATTEMPT_COUNT=0")
print("D0226_R03_EXECUTED=NO")
print("D0226_R03_FIRST_EXECUTION_AUTHORIZED=YES")
print("D0226_R03_RERUN_AFTER_FIRST_ATTEMPT_AUTHORIZED=NO")
print("CORRECTIVE_SCOPE=ASER04,ASER07")
print("ASER04_SCOPE=CANONICAL_JSON_STRING_ESCAPING_AND_TEST_VECTORS")
print("ASER07_SCOPE=STRICT_FREEZE_BEFORE_WITNESS_ORDERING")
print("NEXT_REREVIEW_EXISTING_SOURCE_COPIES_REQUIRED=YES")
print("ACTUAL_CORRECTIVE_SUCCESSOR_AUTHORED=NO")
print("ACTUAL_ACCOUNTING_EVIDENCE_ACQUISITION_AUTHORIZED=NO")
print("ACTUAL_DOMAIN_ACQUISITION_AUTHORIZED=NO")
print("CONCRETE_MAPPING_AUTHORIZED=NO")
print("ACCOUNTING_SATISFACTION_DETERMINATION_AUTHORIZED=NO")
print("PAIR_RECLASSIFICATION_AUTHORIZED=NO")
print("ACTIVE_SCHEMA_V2_MODIFICATION_AUTHORIZED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
