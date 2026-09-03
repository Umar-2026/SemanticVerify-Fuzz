#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).parent

EXPECTED_REVIEW_SHA = (
    "daf3ac553885e3a8547cb48c9271015434d1b0c8f33cc51a3afd083f4e73627e"
)

EXPECTED_REVIEW_SIZE = 12445
EXPECTED_REVIEW_CRLF = 373

EXPECTED_D0224_MANIFEST_SHA = (
    "d9589fb12acb161e48e7600053231eaa64aba14c8970080916eee0b9bc98bfd6"
)

EXPECTED_R03_SHA = (
    "04200a09526bffec25d77702f877b9d21b4ed7da407976c9e4510284e7ee6d08"
)

EXPECTED_R03_SENTINEL_SHA = (
    "cfdbc66438b313b0c3e5924f51544a1b5ada65e70bcdf74a8a6791d0a9e1ed3d"
)

def sha(path):
    return hashlib.sha256(
        Path(path).read_bytes()
    ).hexdigest()

returned = (
    ROOT /
    "01_returned_independent_human_rereview.EXACT_COPY.v1.md"
)

raw = returned.read_bytes()

assert sha(returned) == EXPECTED_REVIEW_SHA
assert len(raw) == EXPECTED_REVIEW_SIZE
assert raw.count(b"\r\n") == EXPECTED_REVIEW_CRLF
assert raw.count(b"\n") == EXPECTED_REVIEW_CRLF
assert raw.count(b"\r") == EXPECTED_REVIEW_CRLF
assert not raw.endswith(b"\n")

text = raw.decode("utf-8").replace("\r\n", "\n")

assert "Reviewer name: Muhammad Nadeem Nadir" in text
assert "Reviewer role: Spec-Tecnical-Adjudicator-1" in text
assert "Review date: 03 / September / 2026" in text
assert "Reviewer confirmation / signature: MN_Lodhi" in text

assert (
    "I confirm that I performed this re-review independently"
    in text
)

assert text.count("[x] REVISION_REQUIRED") == 3
assert text.count("[x] PASS") == 0

assert "deterministic JSON string serialization remains incomplete" in text
assert "does not select an exact JSON escape representation" in text
assert "require distinct freeze and witness commits" in text
assert "does not establish strict freeze-before-witness" in text

assert (
    "Only the supplied ZIP and its included corrective-successor artifacts,"
    in text
)

record = json.loads(
    (
        ROOT /
        "02_confirmed_handoff_and_returned_rereview_record.v1.json"
    ).read_text(encoding="utf-8")
)

assert record["decision"] == "0225"

review = record["returned_review"]

assert review["sha256"] == EXPECTED_REVIEW_SHA
assert review["size_bytes"] == EXPECTED_REVIEW_SIZE
assert review["crlf_count"] == EXPECTED_REVIEW_CRLF
assert review["final_newline"] is False
assert review["review_scope"] == ["ASER04", "ASER07"]

assert review["reviewer_name"] == "Muhammad Nadeem Nadir"
assert review["reviewer_role"] == "Spec-Tecnical-Adjudicator-1"
assert review["review_date"] == "03 / September / 2026"
assert review["reviewer_confirmation"] == "MN_Lodhi"
assert review["independence_attestation_present"] is True

decisions = record["review_decisions"]

assert decisions == {
    "ASER04": "REVISION_REQUIRED",
    "ASER07": "REVISION_REQUIRED",
    "overall": "REVISION_REQUIRED",
}

assert record["preserved_pass_items"] == [
    "ASER01",
    "ASER02",
    "ASER03",
    "ASER05",
    "ASER06",
    "ASER08",
    "ASER09",
]

aser04 = record["remaining_corrective_findings"]["ASER04"]

assert (
    aser04["canonical_json_string_serialization_uniquely_specified"]
    is False
)

assert aser04["exact_string_and_member_name_escaping_required"] is True
assert aser04["canonical_byte_and_hash_test_vectors_required"] is True

aser07 = record["remaining_corrective_findings"]["ASER07"]

assert aser07["strict_freeze_before_witness_ordering_established"] is False
assert aser07["distinct_freeze_and_witness_commits_required"] is True
assert aser07["successful_ancestry_required"] is True

assert (
    aser07[
        "checked_commit_binding_to_freeze_record_and_witness_lineage_required"
    ]
    is True
)

lim = record["next_review_packaging_limitation"]

assert lim["enumeration_source_bytes_were_absent"] is True
assert lim["traceability_source_bytes_were_absent"] is True

assert (
    lim["include_existing_checksum_bound_source_copies_next_review"]
    is True
)

assert lim["new_accounting_evidence_requested"] is False
assert lim["new_domain_acquisition_requested"] is False

life = record["handoff_and_review_lifecycle"]

assert life["external_handoff_authorized"] is True
assert life["external_handoff_export_prepared"] is True
assert life["external_handoff_performed"] is True

assert (
    life["external_handoff_performed_evidence_basis"]
    == "RETURNED_REVIEW_STATES_SUPPLIED_ZIP_WAS_CONSIDERED"
)

assert life["reviewer_identity_recorded_from_returned_review"] is True
assert life["delivery_channel_recorded"] is False
assert life["exact_external_handoff_timestamp_established"] is False
assert life["returned_rereview_received"] is True
assert life["returned_rereview_recorded_by_decision0225"] is True
assert life["corrective_successor_approved"] is False
assert life["governance_adopted"] is False

one = record["one_time_verifier_lifecycle"]

assert one["d0221_r03_sha256"] == EXPECTED_R03_SHA
assert one["d0221_r03_execution_attempt_count"] == 1
assert one["d0221_r03_execution_result"] == "PASS"
assert one["d0221_r03_state"] == "PERMANENTLY_RETIRED"
assert one["d0221_r03_rerun_authorized"] is False

assert (
    one["d0221_r03_sentinel_sha256"]
    == EXPECTED_R03_SENTINEL_SHA
)

assert one["d0220_a02_execution_attempt_count"] == 0
assert one["d0220_a02_state"] == "SUPERSEDED_UNEXECUTED"
assert one["d0220_a02_execution_authorized"] is False

non = record["explicit_nonfindings_and_nonauthorization"]

for key, value in non.items():
    assert type(value) is bool
    assert value is False, key

handoff_manifest_copy = (
    ROOT /
    "04_d0224_handoff_package_manifest.EXACT_COPY.v1.SHA256SUMS"
)

assert sha(handoff_manifest_copy) == EXPECTED_D0224_MANIFEST_SHA

manifest = (
    ROOT /
    "07_returned_revision_required_rereview_record.v1.SHA256SUMS"
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
        "07_returned_revision_required_rereview_record.v1.SHA256SUMS"
    }
)

print("D0225_RETURNED_REREVIEW_RECORD_VERIFIER=PASS")
print("RETURNED_REVIEW_EXACT_BYTES=PASS")
print("EXTERNAL_HANDOFF_PERFORMED=YES")
print("EXACT_EXTERNAL_HANDOFF_TIMESTAMP_ESTABLISHED=NO")
print("RETURNED_REREVIEW_RECEIVED=YES")
print("ASER04=REVISION_REQUIRED")
print("ASER07=REVISION_REQUIRED")
print("OVERALL=REVISION_REQUIRED")
print("CORRECTIVE_SUCCESSOR_APPROVED=NO")
print("GOVERNANCE_ADOPTED=NO")
print("D0221_R03_STATE=PERMANENTLY_RETIRED")
print("D0221_R03_RERUN_AUTHORIZED=NO")
print("D0220_A02_STATE=SUPERSEDED_UNEXECUTED")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
