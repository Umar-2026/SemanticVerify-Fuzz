#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).parent

EXPECTED_D0230_MANIFEST_SHA = (
    "bd791bd106604f4b5cdb75675b69d6ab3af9bb21e3f8759b6ac7ce06c18bfb16"
)

EXPECTED_D0227_MANIFEST_SHA = (
    "db90747fb8f586992c524e5c541a1414bb12349b874ca4fa8a709c4ae0f17ab8"
)

EXPECTED_RETURNED_SHA = (
    "357e5af3944d6a2ed9b47f28af395e02f2903acd29760fee1f6782f366f46fad"
)

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

assert sha(
    ROOT /
    "05_d0230_returned_pass_manifest.EXACT_COPY.v1.SHA256SUMS"
) == EXPECTED_D0230_MANIFEST_SHA

assert sha(
    ROOT /
    "07_d0227_corrective_successor_manifest.EXACT_COPY.v1.SHA256SUMS"
) == EXPECTED_D0227_MANIFEST_SHA

prior = json.loads(
    (
        ROOT /
        "04_d0230_returned_pass_record.EXACT_COPY.v1.json"
    ).read_text(encoding="utf-8")
)

assert (
    prior["status"]
    == "CONFIRMED_HANDOFF_AND_RETURNED_PASS_REREVIEW_RECORDED_NOT_YET_APPROVED_OR_ADOPTED"
)

rr = prior["returned_rereview"]

assert rr["received"] is True
assert rr["recorded"] is True
assert rr["sha256"] == EXPECTED_RETURNED_SHA
assert rr["review_target"] == "Decision0227"
assert rr["corrective_scope"] == ["ASER04", "ASER07"]
assert rr["decisions"]["ASER04"] == "PASS"
assert rr["decisions"]["ASER07"] == "PASS"
assert rr["decisions"]["overall"] == "PASS"
assert rr["bounded_pass_scope"] == "SPECIFICATION_SUFFICIENCY_ONLY"
assert rr["technical_findings_resolved"] is True

prior_life = prior["lifecycle_after_d0230"]

assert prior_life["corrective_successor_approved"] is False
assert prior_life["governance_adopted"] is False

record = json.loads(
    (
        ROOT /
        "01_corrective_successor_approval_record.v1.json"
    ).read_text(encoding="utf-8")
)

assert (
    record["status"]
    == "CORRECTIVE_SUCCESSOR_APPROVED_NOT_GOVERNANCE_ADOPTED"
)

target = record["approval_target"]

assert target["decision"] == "0227"
assert target["scope"] == ["ASER04", "ASER07"]

assert (
    target["corrective_successor_manifest_sha256"]
    == EXPECTED_D0227_MANIFEST_SHA
)

basis = record["approval_basis"]

assert basis["returned_human_rereview_sha256"] == EXPECTED_RETURNED_SHA
assert basis["ASER04_human_decision"] == "PASS"
assert basis["ASER07_human_decision"] == "PASS"
assert basis["overall_human_decision"] == "PASS"
assert basis["bounded_pass_scope"] == "SPECIFICATION_SUFFICIENCY_ONLY"
assert basis["technical_findings_resolved"] is True

approval = record["approval"]

assert approval["corrective_successor_approved"] is True
assert approval["approval_accepts_ASER04_resolution"] is True
assert approval["approval_accepts_ASER07_resolution"] is True
assert approval["approval_preserves_prior_pass_items"] is True
assert approval["approval_does_not_equal_governance_adoption"] is True
assert approval["approved_for_later_adoption_consideration"] is True
assert approval["active_schema_v2_modified"] is False
assert approval["operational_effect"] is False

assert record["preserved_pass_items"] == [
    "ASER01",
    "ASER02",
    "ASER03",
    "ASER05",
    "ASER06",
    "ASER08",
    "ASER09",
]

life = record["lifecycle_after_d0231"]

assert life["external_handoff_authorized"] is True
assert life["external_handoff_export_prepared"] is True
assert life["external_handoff_performed"] is True
assert life["returned_rereview_received"] is True
assert life["returned_rereview_recorded"] is True
assert life["corrective_successor_approved"] is True
assert life["governance_adopted"] is False

for key, value in record["approval_does_not_establish"].items():
    assert type(value) is bool
    assert value is True, key

for key, value in record["explicit_nonauthorization"].items():
    assert type(value) is bool
    assert value is False, key

assert (
    "separate explicit governance adoption decision"
    in record["next_governance_requirement"]
)

manifest = ROOT / "09_corrective_successor_approval.v1.SHA256SUMS"

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
    "09_corrective_successor_approval.v1.SHA256SUMS"
}

print("D0231_CORRECTIVE_SUCCESSOR_APPROVAL_VERIFIER=PASS")
print("CORRECTIVE_SUCCESSOR_APPROVED=YES")
print("ASER04_RESOLUTION_ACCEPTED=YES")
print("ASER07_RESOLUTION_ACCEPTED=YES")
print("GOVERNANCE_ADOPTED=NO")
print("ACTIVE_SCHEMA_V2_MODIFIED=NO")
print("OPERATIONAL_EFFECT=NO")
print("REQ06_REQ14_SATISFACTION_ESTABLISHED=NO")
print("REQ06_REQ14_VIOLATION_ESTABLISHED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
