#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).parent

EXPECTED_REVIEW_SHA = (
    "357e5af3944d6a2ed9b47f28af395e02f2903acd29760fee1f6782f366f46fad"
)

EXPECTED_REVIEW_SIZE = 4895

EXPECTED_D0229_MANIFEST_SHA = (
    "b274e05868ef3d0b226c79164354bf31020d34aafd271ade5c2d21cd5909e06c"
)

def sha(path):
    return hashlib.sha256(
        Path(path).read_bytes()
    ).hexdigest()

review = ROOT / "01_returned_independent_human_rereview.EXACT_COPY.v1.md"

assert review.is_file()
assert sha(review) == EXPECTED_REVIEW_SHA
assert review.stat().st_size == EXPECTED_REVIEW_SIZE

raw = review.read_bytes()

assert raw.count(b"\r\n") == 136
assert raw.count(b"\n") == 136
assert raw.count(b"\r") == 136
assert not raw.endswith(b"\n")

text = raw.decode("utf-8").replace("\r\n", "\n")
norm = " ".join(text.split())

assert "Reviewer name: Muhammad Nadeem Nadir" in text
assert "Reviewer role:Spec-Tech-Reviewer-1" in text
assert "Review date: 05/September/2026" in text
assert "Reviewer confirmation / signature: MN_Lodhi" in text

assert (
    "[x] I confirm that I performed this re-review independently"
    in text
)

assert text.count("[x] PASS") == 3
assert text.count("[ ] REVISION_REQUIRED") == 3
assert "[x] REVISION_REQUIRED" not in text

assert (
    "The two remaining D0222 findings are technically resolved."
    in norm
)

assert (
    "This bounded PASS concerns specification sufficiency only."
    in norm
)

assert (
    "This bounded PASS does not itself constitute governance approval "
    "or adoption."
    in norm
)

copied_d0229_manifest = (
    ROOT /
    "05_d0229_handoff_package_manifest.EXACT_COPY.v1.SHA256SUMS"
)

assert sha(copied_d0229_manifest) == EXPECTED_D0229_MANIFEST_SHA

record = json.loads(
    (
        ROOT /
        "02_confirmed_handoff_and_returned_pass_rereview_record.v1.json"
    ).read_text(encoding="utf-8")
)

assert (
    record["status"]
    == "CONFIRMED_HANDOFF_AND_RETURNED_PASS_REREVIEW_RECORDED_NOT_YET_APPROVED_OR_ADOPTED"
)

handoff = record["handoff"]

assert handoff["external_handoff_performed"] is True
assert handoff["exact_handoff_timestamp_known"] is False
assert handoff["handoff_timestamp"] is None
assert handoff["delivery_channel_known"] is False
assert handoff["delivery_channel"] is None
assert handoff["reviewer_identity_recorded_from_returned_review"] is True

rr = record["returned_rereview"]

assert rr["received"] is True
assert rr["recorded"] is True
assert rr["sha256"] == EXPECTED_REVIEW_SHA
assert rr["size_bytes"] == EXPECTED_REVIEW_SIZE
assert rr["review_target"] == "Decision0227"
assert rr["corrective_scope"] == ["ASER04", "ASER07"]

reviewer = rr["reviewer"]

assert reviewer["name"] == "Muhammad Nadeem Nadir"
assert reviewer["role"] == "Spec-Tech-Reviewer-1"
assert reviewer["review_date"] == "05/September/2026"
assert reviewer["review_date_is_handoff_timestamp"] is False
assert reviewer["confirmation_signature"] == "MN_Lodhi"
assert reviewer["independence_attestation_checked"] is True

decisions = rr["decisions"]

assert decisions["ASER04"] == "PASS"
assert decisions["ASER07"] == "PASS"
assert decisions["overall"] == "PASS"

assert rr["bounded_pass_scope"] == "SPECIFICATION_SUFFICIENCY_ONLY"
assert rr["technical_findings_resolved"] is True

life = record["lifecycle_after_d0230"]

assert life["external_handoff_authorized"] is True
assert life["external_handoff_export_prepared"] is True
assert life["external_handoff_performed"] is True
assert life["returned_rereview_received"] is True
assert life["returned_rereview_recorded"] is True

assert life["corrective_successor_approved"] is False
assert life["governance_adopted"] is False

limits = record["review_does_not_establish"]

assert limits["req06_req14_satisfaction"] is True
assert limits["req06_req14_violation"] is True
assert limits["schema_v2_semantic_losslessness"] is True
assert limits["new_accounting_evidence"] is True
assert limits["new_domain_acquisition"] is True

for key, value in record["explicit_nonauthorization"].items():
    assert type(value) is bool
    assert value is False, key

manifest = ROOT / "08_returned_pass_rereview_record.v1.SHA256SUMS"

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

assert (
    actual
    == listed | {
        "08_returned_pass_rereview_record.v1.SHA256SUMS"
    }
)

print("D0230_RETURNED_PASS_REREVIEW_RECORD_VERIFIER=PASS")
print("EXTERNAL_HANDOFF_PERFORMED=YES")
print("EXACT_HANDOFF_TIMESTAMP_KNOWN=NO")
print("DELIVERY_CHANNEL_KNOWN=NO")
print("RETURNED_REREVIEW_RECEIVED=YES")
print("RETURNED_REREVIEW_RECORDED=YES")
print("ASER04_HUMAN_DECISION=PASS")
print("ASER07_HUMAN_DECISION=PASS")
print("OVERALL_HUMAN_REREVIEW_DECISION=PASS")
print("BOUNDED_PASS_SCOPE=SPECIFICATION_SUFFICIENCY_ONLY")
print("CORRECTIVE_SUCCESSOR_APPROVED=NO")
print("GOVERNANCE_ADOPTED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
