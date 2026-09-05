#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).parent

EXPECTED_D0231_MANIFEST_SHA = (
    "8fe7172a3dd29646f85f237b3079796efd4bc7dbad578744124795ec3eae6e6d"
)

EXPECTED_D0227_MANIFEST_SHA = (
    "db90747fb8f586992c524e5c541a1414bb12349b874ca4fa8a709c4ae0f17ab8"
)

EXPECTED_RETURNED_REVIEW_SHA = (
    "357e5af3944d6a2ed9b47f28af395e02f2903acd29760fee1f6782f366f46fad"
)

def sha(path):
    return hashlib.sha256(
        Path(path).read_bytes()
    ).hexdigest()

assert sha(
    ROOT /
    "05_d0231_approval_manifest.EXACT_COPY.v1.SHA256SUMS"
) == EXPECTED_D0231_MANIFEST_SHA

assert sha(
    ROOT /
    "07_d0227_corrective_successor_manifest.EXACT_COPY.v1.SHA256SUMS"
) == EXPECTED_D0227_MANIFEST_SHA

approval = json.loads(
    (
        ROOT /
        "04_d0231_approval_record.EXACT_COPY.v1.json"
    ).read_text(encoding="utf-8")
)

assert (
    approval["status"]
    == "CORRECTIVE_SUCCESSOR_APPROVED_NOT_GOVERNANCE_ADOPTED"
)

target = approval["approval_target"]

assert target["decision"] == "0227"
assert target["scope"] == ["ASER04", "ASER07"]
assert (
    target["corrective_successor_manifest_sha256"]
    == EXPECTED_D0227_MANIFEST_SHA
)

basis = approval["approval_basis"]

assert (
    basis["returned_human_rereview_sha256"]
    == EXPECTED_RETURNED_REVIEW_SHA
)

assert basis["ASER04_human_decision"] == "PASS"
assert basis["ASER07_human_decision"] == "PASS"
assert basis["overall_human_decision"] == "PASS"
assert basis["bounded_pass_scope"] == "SPECIFICATION_SUFFICIENCY_ONLY"
assert basis["technical_findings_resolved"] is True

a = approval["approval"]

assert a["corrective_successor_approved"] is True
assert a["approval_does_not_equal_governance_adoption"] is True
assert a["approved_for_later_adoption_consideration"] is True
assert a["active_schema_v2_modified"] is False
assert a["operational_effect"] is False

prior_life = approval["lifecycle_after_d0231"]

assert prior_life["corrective_successor_approved"] is True
assert prior_life["governance_adopted"] is False

record = json.loads(
    (
        ROOT /
        "01_governance_adoption_record.v1.json"
    ).read_text(encoding="utf-8")
)

assert (
    record["status"]
    == "CORRECTIVE_SUCCESSOR_GOVERNANCE_ADOPTED_NO_OPERATIONAL_AUTHORIZATION"
)

adoption_target = record["adoption_target"]

assert adoption_target["decision"] == "0227"
assert adoption_target["scope"] == ["ASER04", "ASER07"]

assert (
    adoption_target["corrective_successor_manifest_sha256"]
    == EXPECTED_D0227_MANIFEST_SHA
)

adoption_basis = record["adoption_basis"]

assert adoption_basis["corrective_successor_approved"] is True
assert adoption_basis["ASER04_resolution_accepted"] is True
assert adoption_basis["ASER07_resolution_accepted"] is True

assert (
    adoption_basis["overall_human_rereview_decision"]
    == "PASS"
)

assert (
    adoption_basis["bounded_pass_scope"]
    == "SPECIFICATION_SUFFICIENCY_ONLY"
)

adoption = record["adoption"]

assert adoption["governance_adopted"] is True
assert adoption["adopted_governed_successor"] is True

assert (
    adoption["adoption_scope"]
    == "D0227_ASER04_ASER07_SPECIFICATION_CORRECTIVE_SUCCESSOR"
)

assert adoption["adoption_accepts_d0231_approval"] is True
assert adoption["active_schema_v2_modified"] is False
assert adoption["active_schema_v2_materialized"] is False
assert adoption["operational_effect"] is False
assert adoption["operational_authorization_created"] is False

assert record["preserved_pass_items"] == [
    "ASER01",
    "ASER02",
    "ASER03",
    "ASER05",
    "ASER06",
    "ASER08",
    "ASER09",
]

life = record["lifecycle_after_d0232"]

assert life["external_handoff_authorized"] is True
assert life["external_handoff_export_prepared"] is True
assert life["external_handoff_performed"] is True
assert life["returned_rereview_received"] is True
assert life["returned_rereview_recorded"] is True
assert life["corrective_successor_approved"] is True
assert life["governance_adopted"] is True

for key, value in record["adoption_does_not_establish"].items():
    assert type(value) is bool
    assert value is True, key

for key, value in record["explicit_nonauthorization"].items():
    assert type(value) is bool
    assert value is False, key

assert (
    "separate explicit authorization"
    in record["next_governance_requirement"]
)

manifest = ROOT / "09_governance_adoption.v1.SHA256SUMS"

lines = [
    line
    for line in manifest.read_text(
        encoding="utf-8"
    ).splitlines()
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
    "09_governance_adoption.v1.SHA256SUMS"
}

print("D0232_GOVERNANCE_ADOPTION_VERIFIER=PASS")
print("CORRECTIVE_SUCCESSOR_APPROVED=YES")
print("GOVERNANCE_ADOPTED=YES")
print("ADOPTED_GOVERNED_SUCCESSOR=D0227")
print("ADOPTION_SCOPE=ASER04_ASER07_SPECIFICATION_CORRECTIVE_SUCCESSOR")
print("ACTIVE_SCHEMA_V2_MODIFIED=NO")
print("ACTIVE_SCHEMA_V2_MATERIALIZED=NO")
print("OPERATIONAL_EFFECT=NO")
print("REQ06_REQ14_SATISFACTION_ESTABLISHED=NO")
print("REQ06_REQ14_VIOLATION_ESTABLISHED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
