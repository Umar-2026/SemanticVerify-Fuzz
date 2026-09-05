#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).parent

EXPECTED_D0232_MANIFEST_SHA = (
    "baf93d156185a9981d471207ad928d711161704295e9a101a3cba0580b1cd998"
)

EXPECTED_D0227_MANIFEST_SHA = (
    "db90747fb8f586992c524e5c541a1414bb12349b874ca4fa8a709c4ae0f17ab8"
)

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

assert sha(
    ROOT /
    "05_d0232_adoption_manifest.EXACT_COPY.v1.SHA256SUMS"
) == EXPECTED_D0232_MANIFEST_SHA

assert sha(
    ROOT /
    "06_d0227_corrective_successor_manifest.EXACT_COPY.v1.SHA256SUMS"
) == EXPECTED_D0227_MANIFEST_SHA

prior = json.loads(
    (
        ROOT /
        "04_d0232_adoption_record.EXACT_COPY.v1.json"
    ).read_text(encoding="utf-8")
)

assert (
    prior["status"]
    == "CORRECTIVE_SUCCESSOR_GOVERNANCE_ADOPTED_NO_OPERATIONAL_AUTHORIZATION"
)

assert prior["adoption"]["governance_adopted"] is True
assert prior["adoption"]["adopted_governed_successor"] is True
assert prior["adoption"]["active_schema_v2_materialized"] is False
assert prior["adoption"]["operational_effect"] is False
assert prior["adoption"]["operational_authorization_created"] is False

record = json.loads(
    (
        ROOT /
        "01_req06_req14_accounting_authorization_design.v1.json"
    ).read_text(encoding="utf-8")
)

assert record["decision"] == "0233"

assert (
    record["status"]
    == "AUTHORIZATION_DESIGN_ONLY_NO_OPERATIONAL_AUTHORIZATION"
)

basis = record["governance_basis"]

assert basis["adopted_successor"] == "D0227"
assert basis["governance_adopted"] is True

track = record["selected_design_track"]

assert track["track_id"] == "B"
assert track["name"] == "REQ06_REQ14_ACCOUNTING_WORK"
assert track["selected_for_design"] is True
assert track["authorized_for_execution"] is False

excluded = record["excluded_track"]

assert excluded["track_id"] == "A"
assert excluded["name"] == "ACTIVE_SCHEMA_V2_MATERIALIZATION"
assert excluded["selected_for_design"] is False
assert excluded["authorized_for_execution"] is False
assert excluded["must_be_separately_authorized"] is True

principles = record["design_principles"]

for key, value in principles.items():
    assert type(value) is bool
    assert value is True, key

phases = record["future_authorization_ladder"]

assert [x["phase_id"] for x in phases] == [
    "B1", "B2", "B3", "B4", "B5", "B6", "B7"
]

for phase in phases:
    assert phase["future_authorization_required"] is True
    assert phase["authorized_by_d0233"] is False

assert phases[0]["name"] == "ACCOUNTING_SOURCE_AND_DOMAIN_ACQUISITION"
assert phases[1]["name"] == "COMPLETE_ACCOUNTING_DOMAIN_FREEZE"
assert phases[2]["name"] == "FORWARD_WITNESS_ACQUISITION"
assert phases[3]["name"] == "REVERSE_WITNESS_ACQUISITION"
assert phases[4]["name"] == "CONCRETE_SOURCE_UNIT_CARRIER_MAPPING"
assert phases[5]["name"] == "REQ06_REQ14_ACCOUNTING_SATISFACTION_DETERMINATION"
assert phases[6]["name"] == "PAIR_RECLASSIFICATION_IF_JUSTIFIED"

assert phases[5]["may_determine_satisfaction"] is True
assert phases[6]["may_reclassify_pairs"] is True

next_auth = record["recommended_next_future_authorization"]

assert next_auth["phase_id"] == "B1"
assert next_auth["name"] == "ACCOUNTING_SOURCE_AND_DOMAIN_ACQUISITION"
assert next_auth["authorization_created_by_d0233"] is False
assert next_auth["execution_created_by_d0233"] is False
assert next_auth["must_be_authored_as_separate_future_governance_decision"] is True

for key, value in record["d0233_does_not_establish"].items():
    assert type(value) is bool
    assert value is True, key

for key, value in record["explicit_nonauthorization"].items():
    assert type(value) is bool
    assert value is False, key

assert record["operational_effect"] is False

manifest = (
    ROOT /
    "08_req06_req14_accounting_authorization_design.v1.SHA256SUMS"
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
    "08_req06_req14_accounting_authorization_design.v1.SHA256SUMS"
}

print("D0233_ACCOUNTING_AUTHORIZATION_DESIGN_VERIFIER=PASS")
print("SELECTED_DESIGN_TRACK=B")
print("TRACK_B=REQ06_REQ14_ACCOUNTING_WORK")
print("TRACK_B_EXECUTION_AUTHORIZED=NO")
print("TRACK_A_ACTIVE_SCHEMA_MATERIALIZATION_SELECTED=NO")
print("ACTIVE_SCHEMA_V2_MATERIALIZATION_AUTHORIZED=NO")

print("FUTURE_PHASE_B1=ACCOUNTING_SOURCE_AND_DOMAIN_ACQUISITION")
print("FUTURE_PHASE_B2=COMPLETE_ACCOUNTING_DOMAIN_FREEZE")
print("FUTURE_PHASE_B3=FORWARD_WITNESS_ACQUISITION")
print("FUTURE_PHASE_B4=REVERSE_WITNESS_ACQUISITION")
print("FUTURE_PHASE_B5=CONCRETE_SOURCE_UNIT_CARRIER_MAPPING")
print("FUTURE_PHASE_B6=REQ06_REQ14_ACCOUNTING_SATISFACTION_DETERMINATION")
print("FUTURE_PHASE_B7=PAIR_RECLASSIFICATION_IF_JUSTIFIED")

print("B1_AUTHORIZED_BY_D0233=NO")
print("B2_AUTHORIZED_BY_D0233=NO")
print("B3_AUTHORIZED_BY_D0233=NO")
print("B4_AUTHORIZED_BY_D0233=NO")
print("B5_AUTHORIZED_BY_D0233=NO")
print("B6_AUTHORIZED_BY_D0233=NO")
print("B7_AUTHORIZED_BY_D0233=NO")

print("REQ06_REQ14_SATISFACTION_ESTABLISHED=NO")
print("REQ06_REQ14_VIOLATION_ESTABLISHED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
print("OPERATIONAL_EFFECT=NO")
