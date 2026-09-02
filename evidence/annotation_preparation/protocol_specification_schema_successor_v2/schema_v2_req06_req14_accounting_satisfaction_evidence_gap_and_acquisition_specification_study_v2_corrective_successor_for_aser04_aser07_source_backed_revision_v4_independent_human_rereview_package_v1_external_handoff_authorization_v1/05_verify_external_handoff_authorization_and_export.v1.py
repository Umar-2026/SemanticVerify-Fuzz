#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import os
import zipfile

ROOT = Path(__file__).parent

EXPECTED_D0223_MANIFEST_SHA = (
    "f872293903dcbef15d7b190a1ec774b8e700ca1a0816047718d08d27a16c2ead"
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

record = json.loads(
    (
        ROOT /
        "01_external_handoff_authorization_and_export_record.v1.json"
    ).read_text(encoding="utf-8")
)

assert record["decision"] == "0224"

assert (
    record["status"]
    == "EXTERNAL_HANDOFF_AUTHORIZED_EXPORT_PREPARED_NOT_YET_PERFORMED"
)

review = record["review_package"]

assert (
    review["review_package_manifest_sha256"]
    == EXPECTED_D0223_MANIFEST_SHA
)

assert review["review_scope"] == [
    "ASER04",
    "ASER07",
]

assert review["review_package_file_count"] == 26

for key, value in record["reviewer_content"].items():
    assert type(value) is bool
    assert value is False, key

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

life = record["handoff_lifecycle"]

assert life["external_handoff_authorized"] is True
assert life["external_handoff_export_prepared"] is True
assert life["external_handoff_performed"] is False
assert life["reviewer_recipient_recorded"] is False
assert life["handoff_timestamp_recorded"] is False
assert life["returned_rereview_received"] is False
assert life["returned_rereview_recorded"] is False
assert life["corrective_successor_approved"] is False
assert life["governance_adopted"] is False

for key, value in record["explicit_nonauthorization"].items():
    assert type(value) is bool
    assert value is False, key

manifest_copy = (
    ROOT /
    "04_d0223_review_package_manifest.EXACT_COPY.v1.SHA256SUMS"
)

assert sha(manifest_copy) == EXPECTED_D0223_MANIFEST_SHA

# Optional local-export verification.
# Portable repository verification does not require the external archive.
export_env = os.environ.get("SVF_D0224_EXPORT_ZIP")

if export_env:
    archive = Path(export_env)

    assert archive.is_file()
    assert sha(archive) == record["export"]["archive_sha256"]
    assert archive.stat().st_size == record["export"]["archive_size_bytes"]

    root_name = record["export"]["archive_root"]

    with zipfile.ZipFile(archive, "r") as zf:
        names = zf.namelist()

        assert len(names) == 26
        assert all(
            name.startswith(root_name + "/")
            for name in names
        )

        manifest_bytes = zf.read(
            root_name
            + "/07_independent_human_rereview_package.v1.SHA256SUMS"
        )

        assert (
            hashlib.sha256(manifest_bytes).hexdigest()
            == EXPECTED_D0223_MANIFEST_SHA
        )

    print("LOCAL_EXTERNAL_HANDOFF_EXPORT=PASS")
else:
    print("LOCAL_EXTERNAL_HANDOFF_EXPORT=NOT_REQUESTED")

manifest = (
    ROOT /
    "06_external_handoff_authorization_and_export.v1.SHA256SUMS"
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
        "06_external_handoff_authorization_and_export.v1.SHA256SUMS"
    }
)

print("D0224_EXTERNAL_HANDOFF_AUTHORIZATION_AND_EXPORT_VERIFIER=PASS")
print("EXTERNAL_HANDOFF_AUTHORIZED=YES")
print("EXTERNAL_HANDOFF_EXPORT_PREPARED=YES")
print("EXTERNAL_HANDOFF_PERFORMED=NO")
print("REVIEW_SCOPE=ASER04,ASER07")
print("REVIEWER_CONTENT_PREFILLED=NO")
print("RETURNED_REREVIEW_RECEIVED=NO")
print("RETURNED_REREVIEW_RECORDED=NO")
print("CORRECTIVE_SUCCESSOR_APPROVED=NO")
print("GOVERNANCE_ADOPTED=NO")
print("D0221_R03_STATE=PERMANENTLY_RETIRED")
print("D0221_R03_RERUN_AUTHORIZED=NO")
print("D0220_A02_STATE=SUPERSEDED_UNEXECUTED")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
