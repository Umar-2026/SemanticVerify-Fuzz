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
    R / "01_review_package_manifest.v1.json"
)

assert (
    manifest["status"]
    == "AUTHOR_REVIEW_PACKAGE_AWAITING_EXTERNAL_HANDOFF"
)

assert manifest["review_scope"] == "CWXR07-S2_ONLY"

source = manifest["source_successor"]

assert source["criterion_id"] == "CWXR07-S2"
assert source["source_file_count"] == 17
assert source["exact_copy_included"] is True

copy_root = R / "02_cwxr07_s2_successor.EXACT_COPY"

actual_files = {
    p.relative_to(copy_root).as_posix(): {
        "sha256": sha(p),
        "size_bytes": p.stat().st_size,
    }
    for p in sorted(copy_root.rglob("*"))
    if p.is_file()
}

assert actual_files == source["exact_copy_files"]
assert len(actual_files) == 17

inner_sums = (
    copy_root
    / "10_cwxr07_s2_narrowed_corrective_successor_v1.SHA256SUMS"
)

rows = [
    row.strip()
    for row in inner_sums.read_text(
        encoding="utf-8"
    ).splitlines()
    if row.strip()
]

assert len(rows) == 16

for row in rows:
    digest, name = row.split(None, 1)
    name = name.strip().lstrip("*")
    path = copy_root / name
    assert path.is_file()
    assert sha(path) == digest

source_manifest = load(
    copy_root
    / "01_cwxr07_s2_narrowed_corrective_successor_manifest.v1.json"
)

assert source_manifest["criterion_id"] == "CWXR07-S2"

assert (
    source_manifest["historical_s1_boundary"]["cwxr07_s1_decision"]
    == "REVISION_REQUIRED"
)

assert source_manifest["human_review"]["human_review_completed"] is False
assert source_manifest["human_review"]["reviewer_identity_recorded"] is False
assert source_manifest["human_review"]["reviewer_decision_recorded"] is False

hist = manifest["historical_boundary"]

assert hist["cwxr07_s1_decision"] == "REVISION_REQUIRED"
assert hist["cwxr07_s1_modified"] is False
assert hist["cwxr07_s1_upgraded"] is False
assert hist["cwxr01_to_cwxr06_and_cwxr08_reopened"] is False

packet = manifest["review_packet"]

assert packet["reviewer_identity_prepopulated"] is False
assert packet["reviewer_decision_prepopulated"] is False
assert packet["human_review_completed"] is False

blank = (
    R
    / "04_CWXR07_S2_reviewer_packet.INITIAL_BLANK.EXACT_COPY.v1.md"
)

assert sha(blank) == packet["initial_blank_exact_copy_sha256"]

blank_text = blank.read_text(
    encoding="utf-8"
)

for marker in [
    "Review only `CWXR07-S2`.",
    "CWXR07-S1 remains `REVISION_REQUIRED`",
    "CWXR07-S2 decision:",
    "Reviewer notes:",
    "Reviewer name:",
    "Reviewer role:",
    "Reviewer confirmation/signature:",
    "Reviewer attestation:",
    "Review date:",
]:
    assert marker in blank_text

instructions = (
    R / "03_independent_reviewer_instructions.v1.md"
).read_text(
    encoding="utf-8"
)

for marker in [
    "Review only `CWXR07-S2`.",
    "Historical CWXR07-S1 remains:",
    "`REVISION_REQUIRED`",
    "supplied-file byte integrity",
    "checksum-closure integrity",
    "internal consistency",
    "bounded-claim language",
    "A PASS does not retroactively change CWXR07-S1",
    "Choose exactly one:",
]:
    assert marker in instructions

life = manifest["decision0166_a02_lifecycle"]

assert life["executed"] is True
assert life["execution_count_in_package_authoring_transaction"] == 1
assert life["pass"] is True
assert life["lifecycle_after_execution"] == "PERMANENTLY_RETIRED"
assert life["rerun_authorized"] is False

cons = load(
    R / "06_decision0166_a02_consumption_record.v1.json"
)

assert cons["decision"] == "0166"
assert cons["execution_invocation_count_in_this_controlled_transaction"] == 1
assert cons["return_code"] == 0
assert cons["pass"] is True
assert cons["lifecycle_after_execution"] == "PERMANENTLY_RETIRED"
assert cons["rerun_authorized"] is False
assert cons["human_review_completed"] is False
assert cons["reviewer_identity_recorded"] is False
assert cons["reviewer_decision_recorded"] is False
assert cons["reviewer_identity_synthesized"] is False
assert cons["reviewer_decision_synthesized"] is False
assert cons["external_handoff_authorized"] is False
assert cons["successor_approved"] is False
assert cons["governance_adoption_authorized"] is False
assert cons["retired_a02_verifiers_executed"] is False

assert all(
    value is False
    for value in manifest["explicit_non_authorizations"].values()
)

sums = (
    R / "08_cwxr07_s2_independent_human_review_package_v1.SHA256SUMS"
)

rows = [
    row.strip()
    for row in sums.read_text(
        encoding="utf-8"
    ).splitlines()
    if row.strip()
]

expected_files = {
    p.relative_to(R).as_posix()
    for p in R.rglob("*")
    if p.is_file()
    and p.name != sums.name
}

actual_sum_files = set()

for row in rows:
    digest, name = row.split(None, 1)
    name = name.strip().lstrip("*")

    path = R / name

    assert path.is_file()
    assert sha(path) == digest

    actual_sum_files.add(name)

assert actual_sum_files == expected_files
assert len(expected_files) == 23

print("CWXR07_S2_INDEPENDENT_HUMAN_REVIEW_PACKAGE_V1=PASS")

print("REVIEW_SCOPE=CWXR07-S2_ONLY")
print("PACKAGE_FILE_COUNT=24")
print("PACKAGE_CHECKSUM_ENTRY_COUNT=23")
print("SOURCE_SUCCESSOR_EXACT_COPY_FILE_COUNT=17")

print("HISTORICAL_CWXR07_S1_DECISION=REVISION_REQUIRED")
print("HISTORICAL_CWXR07_S1_MODIFIED=NO")
print("HISTORICAL_CWXR07_S1_UPGRADED=NO")

print("INDEPENDENT_HUMAN_REVIEW_REQUIRED=YES")
print("HUMAN_REVIEW_COMPLETED=NO")
print("REVIEWER_IDENTITY_RECORDED=NO")
print("REVIEWER_DECISION_RECORDED=NO")
print("REVIEWER_IDENTITY_SYNTHESIZED=NO")
print("REVIEWER_DECISION_SYNTHESIZED=NO")

print("DECISION0166_A02_STATE=PERMANENTLY_RETIRED")
print("DECISION0166_A02_RERUN_AUTHORIZED=NO")

print("EXTERNAL_HANDOFF_AUTHORIZED=NO")
print("EXTERNAL_ZIP_CREATED=NO")
print("EXTERNAL_EDITABLE_REVIEW_COPY_CREATED=NO")

print("SUCCESSOR_APPROVED=NO")
print("GOVERNANCE_ADOPTION_AUTHORIZED=NO")

print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
