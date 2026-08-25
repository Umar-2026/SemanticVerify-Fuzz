#!/usr/bin/env python3

import hashlib
import json
from pathlib import Path

R = Path(__file__).resolve().parent

def sha(path):
    return hashlib.sha256(
        Path(path).read_bytes()
    ).hexdigest()

def load(path):
    return json.loads(
        Path(path).read_text(
            encoding="utf-8"
        )
    )

manifest = load(
    R / "01_external_handoff_manifest.v1.json"
)

assert (
    manifest["status"]
    == "EXTERNAL_HANDOFF_AUTHORED_AWAITING_GENUINE_INDEPENDENT_HUMAN_REVIEW"
)

assert manifest["review_scope"] == "CWXR07-S2_ONLY"

source = manifest["source_review_package"]

assert source["file_count"] == 24
assert source["exact_copy_included"] is True

copy_root = R / "02_review_package.EXACT_COPY"

actual_files = {
    p.relative_to(copy_root).as_posix(): {
        "sha256": sha(p),
        "size_bytes": p.stat().st_size,
    }
    for p in sorted(copy_root.rglob("*"))
    if p.is_file()
}

assert actual_files == source["exact_copy_files"]
assert len(actual_files) == 24

inner_sums = [
    p
    for p in copy_root.glob("*SHA256SUMS")
    if p.is_file()
]

assert len(inner_sums) == 1

rows = [
    row.strip()
    for row in inner_sums[0].read_text(
        encoding="utf-8"
    ).splitlines()
    if row.strip()
]

assert len(rows) == 23

for row in rows:
    digest, name = row.split(None, 1)
    name = name.strip().lstrip("*")

    p = copy_root / name

    assert p.is_file()
    assert sha(p) == digest

packet = R / "03_CWXR07_S2_reviewer_packet.INITIAL_BLANK.EXACT_COPY.v1.md"

assert sha(packet) == manifest["reviewer_packet"]["sha256"]
assert packet.stat().st_size == manifest["reviewer_packet"]["size_bytes"]

package_packet = (
    copy_root
    / "04_CWXR07_S2_reviewer_packet.INITIAL_BLANK.EXACT_COPY.v1.md"
)

assert package_packet.is_file()
assert sha(package_packet) == sha(packet)
assert package_packet.read_bytes() == packet.read_bytes()

text = packet.read_text(
    encoding="utf-8"
)

labels = [
    "CWXR07-S2 decision",
    "Reviewer notes",
    "Reviewer name",
    "Reviewer role",
    "Reviewer confirmation/signature",
    "Reviewer attestation",
    "Review date",
]

lines = text.splitlines()

for label in labels:
    prefix = label + ":"

    matches = [
        line
        for line in lines
        if line.startswith(prefix)
    ]

    assert len(matches) == 1

    value = matches[0].split(":", 1)[1].strip()

    assert value == ""

reviewer_packet = manifest["reviewer_packet"]

assert reviewer_packet["structurally_blank"] is True

assert (
    reviewer_packet["blank_field_validation_rule"]
    == "VALUE_AFTER_FIRST_COLON_MUST_BE_EMPTY"
)

assert reviewer_packet["reviewer_identity_prepopulated"] is False
assert reviewer_packet["reviewer_decision_prepopulated"] is False

life = manifest["decision0168_a02_lifecycle"]

assert life["executed"] is True
assert life["execution_count_in_handoff_transaction"] == 1
assert life["pass"] is True
assert life["lifecycle_after_execution"] == "PERMANENTLY_RETIRED"
assert life["rerun_authorized"] is False

cons = load(
    R / "07_decision0168_a02_consumption_record.v1.json"
)

assert cons["decision"] == "0168"

assert (
    cons["execution_invocation_count_in_this_controlled_transaction"]
    == 1
)

assert cons["return_code"] == 0
assert cons["pass"] is True
assert cons["lifecycle_after_execution"] == "PERMANENTLY_RETIRED"
assert cons["rerun_authorized"] is False
assert cons["retired_a02_verifiers_executed"] is False

historical = manifest["historical_boundary"]

assert historical["historical_cwxr07_s1_decision"] == "REVISION_REQUIRED"
assert historical["historical_cwxr07_s1_modified"] is False
assert historical["historical_cwxr07_s1_upgraded"] is False

human = manifest["human_review_state"]

assert human["independent_human_review_required"] is True
assert human["human_review_completed"] is False
assert human["reviewer_identity_recorded"] is False
assert human["reviewer_decision_recorded"] is False
assert human["reviewer_identity_synthesized"] is False
assert human["reviewer_decision_synthesized"] is False
assert human["successor_approved"] is False

assert all(
    value is False
    for value in manifest["claim_boundary"].values()
)

assert all(
    value is False
    for value in manifest["explicit_non_authorizations"].values()
)

outer_sums = R / "09_external_handoff_v1.SHA256SUMS"

rows = [
    row.strip()
    for row in outer_sums.read_text(
        encoding="utf-8"
    ).splitlines()
    if row.strip()
]

expected_files = {
    p.relative_to(R).as_posix()
    for p in R.rglob("*")
    if p.is_file()
    and p.name != outer_sums.name
}

actual_sum_files = set()

for row in rows:
    digest, name = row.split(None, 1)
    name = name.strip().lstrip("*")

    p = R / name

    assert p.is_file()
    assert sha(p) == digest

    actual_sum_files.add(name)

assert actual_sum_files == expected_files
assert len(expected_files) == 31

print("CWXR07_S2_EXTERNAL_INDEPENDENT_HUMAN_REVIEW_HANDOFF_V1=PASS")

print("REVIEW_SCOPE=CWXR07-S2_ONLY")

print("HANDOFF_FILE_COUNT=32")
print("HANDOFF_CHECKSUM_ENTRY_COUNT=31")
print("SOURCE_REVIEW_PACKAGE_EXACT_COPY_FILE_COUNT=24")

print("REVIEWER_PACKET_STRUCTURALLY_BLANK=YES")
print("BLANK_FIELD_VALIDATION_RULE=VALUE_AFTER_FIRST_COLON_MUST_BE_EMPTY")
print("REVIEWER_IDENTITY_PREPOPULATED=NO")
print("REVIEWER_DECISION_PREPOPULATED=NO")

print("HISTORICAL_CWXR07_S1_DECISION=REVISION_REQUIRED")
print("HISTORICAL_CWXR07_S1_MODIFIED=NO")
print("HISTORICAL_CWXR07_S1_UPGRADED=NO")

print("DECISION0168_A02_STATE=PERMANENTLY_RETIRED")
print("DECISION0168_A02_RERUN_AUTHORIZED=NO")

print("INDEPENDENT_HUMAN_REVIEW_REQUIRED=YES")
print("HUMAN_REVIEW_COMPLETED=NO")

print("REVIEWER_IDENTITY_RECORDED=NO")
print("REVIEWER_DECISION_RECORDED=NO")
print("REVIEWER_IDENTITY_SYNTHESIZED=NO")
print("REVIEWER_DECISION_SYNTHESIZED=NO")

print("SUCCESSOR_APPROVED=NO")

print("GOVERNANCE_ADOPTION_AUTHORIZED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
