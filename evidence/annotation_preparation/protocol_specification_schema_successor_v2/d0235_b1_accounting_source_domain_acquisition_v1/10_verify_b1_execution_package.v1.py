#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).parent

EXPECTED_D0234_MANIFEST_SHA = (
    "bcd12a48d3a67322d8cbb8af42e3fb5e6aa4e021150cda98f86bc19c136ab90c"
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
    "09_d0234_authorization_manifest.EXACT_COPY.v1.SHA256SUMS"
) == EXPECTED_D0234_MANIFEST_SHA

auth = json.loads(
    (
        ROOT /
        "07_d0234_authorization_record.EXACT_COPY.v1.json"
    ).read_text(encoding="utf-8")
)

assert auth["authorization"]["b1_authorized"] is True
assert auth["authorization"]["cross_source_join"] is False
assert auth["authorization"]["create_new_source_unit_carrier_mapping"] is False

record = json.loads(
    (
        ROOT /
        "01_b1_execution_record.v1.json"
    ).read_text(encoding="utf-8")
)

assert record["decision"] == "0235"

assert (
    record["status"]
    == "B1_ACCOUNTING_SOURCE_AND_DOMAIN_ACQUISITION_EXECUTED_SOURCE_LOCAL_ONLY"
)

e = record["execution"]

assert e["b1_authorized"] is True
assert e["b1_executed"] is True
assert e["authorized_source_count"] == 2
assert e["sources_parsed_independently"] is True
assert e["source_scope_expanded"] is False
assert e["cross_source_join_performed"] is False
assert e["concrete_source_unit_carrier_mapping_created"] is False
assert e["domain_freeze_created"] is False
assert e["domain_freeze_commit_created"] is False
assert e["forward_witness_acquired"] is False
assert e["reverse_witness_acquired"] is False
assert e["req06_req14_satisfaction_determined"] is False
assert e["req06_req14_violation_determined"] is False
assert e["pair_reclassification_performed"] is False

sources = record["source_results"]

assert set(sources) == {"ENUMERATION", "TRACEABILITY"}

assert sources["ENUMERATION"]["input_sha256"] == EXPECTED_ENUM_SHA
assert sources["TRACEABILITY"]["input_sha256"] == EXPECTED_TRACE_SHA

for sid, spec in sources.items():
    profile = ROOT / spec["profile_artifact"]
    domain = ROOT / spec["domain_input_artifact"]

    assert profile.is_file()
    assert domain.is_file()

    assert sha(profile) == spec["profile_sha256"]
    assert sha(domain) == spec["domain_input_sha256"]

    d = json.loads(domain.read_text(encoding="utf-8"))

    assert d["source_id"] == sid
    assert d["source_sha256"] == spec["input_sha256"]

    assert (
        d["source_local_record_count"]
        == spec["source_local_domain_record_count"]
    )

    assert d["cross_source_join_performed"] is False
    assert d["concrete_mapping_created"] is False
    assert d["domain_frozen"] is False
    assert d["forward_witness_acquired"] is False
    assert d["reverse_witness_acquired"] is False
    assert d["req06_req14_satisfaction_determined"] is False
    assert d["req06_req14_violation_determined"] is False
    assert d["pair_reclassification_performed"] is False

for value in record["later_phase_authorization"].values():
    assert value is False

for value in record["substantive_results_established"].values():
    assert value is False

manifest = ROOT / "11_b1_execution_package.v1.SHA256SUMS"

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
    p.relative_to(ROOT).as_posix()
    for p in ROOT.rglob("*")
    if p.is_file()
}

assert actual == listed | {
    "11_b1_execution_package.v1.SHA256SUMS"
}

print("D0235_B1_EXECUTION_VERIFIER=PASS")
print("B1_EXECUTED=YES")
print("AUTHORIZED_SOURCE_COUNT=2")
print("SOURCES_PARSED_INDEPENDENTLY=YES")
print("SOURCE_SCOPE_EXPANDED=NO")
print("CROSS_SOURCE_JOIN_PERFORMED=NO")
print("CONCRETE_MAPPING_CREATED=NO")
print("DOMAIN_FREEZE_CREATED=NO")
print("FORWARD_WITNESS_ACQUIRED=NO")
print("REVERSE_WITNESS_ACQUIRED=NO")
print("REQ06_REQ14_DETERMINATION_PERFORMED=NO")
print("PAIR_RECLASSIFICATION_PERFORMED=NO")
