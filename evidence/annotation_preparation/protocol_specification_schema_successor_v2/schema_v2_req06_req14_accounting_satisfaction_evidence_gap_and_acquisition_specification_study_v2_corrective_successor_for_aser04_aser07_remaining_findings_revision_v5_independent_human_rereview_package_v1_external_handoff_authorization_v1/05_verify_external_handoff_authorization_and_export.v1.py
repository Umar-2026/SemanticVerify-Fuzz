#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import os
import zipfile

ROOT = Path(__file__).parent

EXPECTED_D0228_MANIFEST_SHA = (
    "f0772bfb024fa6fce885ef35d65d17922f0fd4ca4bac65388063013cc1612a42"
)

EXPECTED_ENUM_SHA = (
    "44a6e8169f8515921a980cb727e106281f47bbe1a6bc9672e16146bab2832a12"
)

EXPECTED_TRACE_SHA = (
    "6b4b30c958bc1e1dd0896fe086205e3ff58063583b2042bba962c8c59ba46bd4"
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

assert (
    record["status"]
    == "EXTERNAL_HANDOFF_AUTHORIZED_EXPORT_PREPARED_NOT_YET_PERFORMED"
)

assert (
    record["review_target"]["review_package_manifest_sha256"]
    == EXPECTED_D0228_MANIFEST_SHA
)

assert record["review_target"]["scope"] == ["ASER04", "ASER07"]

src = record["source_byte_availability"]

assert src["enumeration_source_sha256"] == EXPECTED_ENUM_SHA
assert src["traceability_source_sha256"] == EXPECTED_TRACE_SHA
assert src["both_present_in_export"] is True

for key, value in record["reviewer_content"].items():
    assert type(value) is bool
    assert value is False, key

life = record["lifecycle"]

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

copied_manifest = (
    ROOT /
    "04_d0228_review_package_manifest.EXACT_COPY.v1.SHA256SUMS"
)

assert sha(copied_manifest) == EXPECTED_D0228_MANIFEST_SHA

# Optional local export verification.
export_env = os.environ.get("SVF_D0229_EXPORT_ZIP")

if export_env:
    export_path = Path(export_env)

    assert export_path.is_file()

    assert sha(export_path) == record["export"]["sha256"]

    assert export_path.stat().st_size == record["export"]["size_bytes"]

    expected_root = (
        "D0227_ASER04_ASER07_Independent_Human_Rereview_Package_v1/"
    )

    with zipfile.ZipFile(export_path, "r") as zf:
        infos = zf.infolist()

        assert len(infos) == 30

        names = [
            info.filename
            for info in infos
        ]

        assert all(
            name.startswith(expected_root)
            for name in names
        )

        rels = {
            name[len(expected_root):]
            for name in names
        }

        assert (
            "07_independent_human_rereview_package.v1.SHA256SUMS"
            in rels
        )

        manifest_bytes = zf.read(
            expected_root
            + "07_independent_human_rereview_package.v1.SHA256SUMS"
        )

        assert (
            hashlib.sha256(manifest_bytes).hexdigest()
            == EXPECTED_D0228_MANIFEST_SHA
        )

    print("LOCAL_EXTERNAL_HANDOFF_EXPORT=PASS")
else:
    print("LOCAL_EXTERNAL_HANDOFF_EXPORT=NOT_REQUIRED_FOR_PORTABLE_VERIFICATION")

manifest = (
    ROOT /
    "06_external_handoff_authorization_and_export.v1.SHA256SUMS"
)

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
        "06_external_handoff_authorization_and_export.v1.SHA256SUMS"
    }
)

print("D0229_EXTERNAL_HANDOFF_AUTHORIZATION_AND_EXPORT_VERIFIER=PASS")
print("EXTERNAL_HANDOFF_AUTHORIZED=YES")
print("EXTERNAL_HANDOFF_EXPORT_PREPARED=YES")
print("EXTERNAL_HANDOFF_PERFORMED=NO")
print("REVIEW_SCOPE=ASER04,ASER07")
print("REVIEWER_CONTENT_PREFILLED=NO")
print("RETURNED_REREVIEW_RECEIVED=NO")
print("RETURNED_REREVIEW_RECORDED=NO")
print("CORRECTIVE_SUCCESSOR_APPROVED=NO")
print("GOVERNANCE_ADOPTED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
