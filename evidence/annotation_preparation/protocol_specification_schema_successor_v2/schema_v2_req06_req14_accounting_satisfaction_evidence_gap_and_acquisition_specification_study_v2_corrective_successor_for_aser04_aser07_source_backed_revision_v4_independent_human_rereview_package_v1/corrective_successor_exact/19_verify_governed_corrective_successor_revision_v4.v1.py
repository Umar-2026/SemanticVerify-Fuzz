#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import subprocess
import sys

ROOT = Path(__file__).parent

def sha(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def load(name):
    return json.loads(
        (ROOT / name).read_text(encoding="utf-8")
    )

overlay = load(
    "10_governed_author_candidate_status_overlay.v1.json"
)

consumption = load(
    "11_d0221_r03_consumption_record.v1.json"
)

sentinel = load(
    "15_d0221_r03_consumption_sentinel.EXACT_COPY.v1.json"
)

freeze_binding = load(
    "17_corrected_v4_preconsumption_binding.EXACT_COPY.v1.json"
)

assert overlay["decision"] == "0222"

assert (
    overlay["governed_status"]
    == "AUTHOR_CANDIDATE_CORRECTIVE_SUCCESSOR"
)

assert overlay["corrective_scope"] == [
    "ASER04",
    "ASER07",
]

assert overlay["preserved_pass_items"] == [
    "ASER01",
    "ASER02",
    "ASER03",
    "ASER05",
    "ASER06",
    "ASER08",
    "ASER09",
]

review = overlay["review_lifecycle"]

assert review["independent_human_rereview_required"] is True
assert review["rereview_completed"] is False
assert review["governance_adopted"] is False

for value in overlay["explicit_nonauthorization"].values():
    assert value is False

one = consumption["one_time_verifier"]

assert one["execution_attempt_count"] == 1
assert one["exit_code"] == 0
assert one["execution_result"] == "PASS"
assert one["first_attempt_consumed_authorization"] is True
assert one["state_after_execution"] == "PERMANENTLY_RETIRED"
assert one["rerun_authorized"] is False

assert sentinel["execution_attempt_count"] == 1
assert sentinel["execution_result"] == "PASS"
assert sentinel["first_attempt_consumes_authorization"] is True
assert sentinel["rerun_authorized"] is False
assert sentinel["state"] == "PERMANENTLY_RETIRED"

for section, filename in [
    (
        "execution_stdout",
        "12_d0221_r03_execution_stdout.EXACT_COPY.v1.txt",
    ),
    (
        "execution_stderr",
        "14_d0221_r03_execution_stderr.EXACT_COPY.v1.txt",
    ),
    (
        "consumption_sentinel",
        "15_d0221_r03_consumption_sentinel.EXACT_COPY.v1.json",
    ),
]:
    record = consumption[section]
    path = ROOT / filename

    assert path.is_file()
    assert sha(path) == record["sha256"]
    assert path.stat().st_size == record["size_bytes"]

assert (
    sha(
        ROOT /
        "16_corrected_v4_preconsumption_manifest.EXACT_COPY.v1.SHA256SUMS"
    )
    == overlay["preconsumption_freeze"]["manifest_sha256"]
)

assert (
    sha(
        ROOT /
        "17_corrected_v4_preconsumption_binding.EXACT_COPY.v1.json"
    )
    == overlay["preconsumption_freeze"]["binding_sha256"]
)

pre = freeze_binding["preconsumption_assertions"]

assert type(pre["r03_execution_attempt_count"]) is int
assert pre["r03_execution_attempt_count"] == 0
assert pre["r03_executed"] is False

assert (
    freeze_binding["state"]
    == "PRECONSUMPTION_FROZEN_NOT_YET_GOVERNED"
)

manifest = (
    ROOT /
    "18_governed_corrective_successor_revision_v4.SHA256SUMS"
)

lines = [
    line
    for line in manifest.read_text(encoding="utf-8").splitlines()
    if line.strip()
]

listed = set()

for line in lines:
    digest, name = line.split("  ", 1)
    path = ROOT / name

    assert path.is_file()
    assert sha(path) == digest
    listed.add(name)

actual_files = {
    p.name
    for p in ROOT.iterdir()
    if p.is_file()
}

assert (
    actual_files
    == listed | {
        "18_governed_corrective_successor_revision_v4.SHA256SUMS"
    }
)

proc = subprocess.run(
    [
        sys.executable,
        str(ROOT / "13_verify_corrective_revision.v4.py"),
    ],
    text=True,
    capture_output=True,
)

assert proc.returncode == 0
assert "D0222_CORRECTED_V4_SPECIFICATION_VERIFIER=PASS" in proc.stdout

print("D0222_GOVERNED_CORRECTIVE_SUCCESSOR_PACKAGE_VERIFIER=PASS")
print("D0221_R03_CONSUMPTION_RECORD=PASS")
print("D0221_R03_STATE=PERMANENTLY_RETIRED")
print("D0221_R03_RERUN_AUTHORIZED=NO")
print("SOURCE_BACKED_CORRECTIVE_REVISION=PASS")
print("CORRECTIVE_SCOPE=ASER04,ASER07")
print("GOVERNED_STATUS=AUTHOR_CANDIDATE_CORRECTIVE_SUCCESSOR")
print("INDEPENDENT_HUMAN_REREVIEW_REQUIRED=YES")
print("GOVERNANCE_ADOPTED=NO")
print("ACTUAL_ACCOUNTING_EVIDENCE_ACQUISITION_PERFORMED=NO")
print("CONCRETE_MAPPING_CREATED=NO")
print("ACCOUNTING_SATISFACTION_EVALUATED=NO")
print("PAIR_RECLASSIFICATION_PERFORMED=NO")
print("ACTIVE_SCHEMA_V2_MODIFIED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
