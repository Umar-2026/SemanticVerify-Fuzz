#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import subprocess
import sys

ROOT = Path(__file__).parent
EXACT = ROOT / "corrective_successor_exact"

EXPECTED_D0222_MANIFEST_SHA = (
    "fc35dc047816da91cb3c664840f640050349662a0badb179839d59cb1035f48c"
)

EXPECTED_PREDECESSOR_REVIEW_SHA = (
    "8613f25eb8c971d6d38774ea7cd0ac97e8171f1e116854a843e3d346432b7618"
)

EXPECTED_PREDECESSOR_REVIEW_SIZE = 12091

def sha(path):
    return hashlib.sha256(
        Path(path).read_bytes()
    ).hexdigest()

def load(path):
    return json.loads(
        Path(path).read_text(encoding="utf-8")
    )

meta = load(
    ROOT /
    "02_independent_human_rereview_package_manifest.v1.json"
)

assert meta["decision"] == "0223"

assert (
    meta["package_status"]
    == "BLANK_INDEPENDENT_HUMAN_REREVIEW_PACKAGE_AUTHORED_NOT_HANDED_OFF"
)

assert meta["corrective_review_scope"] == [
    "ASER04",
    "ASER07",
]

assert meta["preserved_pass_items"] == [
    "ASER01",
    "ASER02",
    "ASER03",
    "ASER05",
    "ASER06",
    "ASER08",
    "ASER09",
]

candidate = meta["governed_candidate"]

assert (
    candidate["status"]
    == "AUTHOR_CANDIDATE_CORRECTIVE_SUCCESSOR"
)

assert (
    candidate["decision0222_package_manifest_sha256"]
    == EXPECTED_D0222_MANIFEST_SHA
)

exact_manifest = (
    EXACT /
    "18_governed_corrective_successor_revision_v4.SHA256SUMS"
)

assert exact_manifest.is_file()

assert (
    sha(exact_manifest)
    == EXPECTED_D0222_MANIFEST_SHA
)

exact_files = {
    p.relative_to(EXACT).as_posix()
    for p in EXACT.rglob("*")
    if p.is_file()
}

assert len(exact_files) == 19

assert (
    set(meta["candidate_exact_copy"]["files"])
    == exact_files
)

assert meta["candidate_exact_copy"]["file_count"] == 19

proc = subprocess.run(
    [
        sys.executable,
        str(
            EXACT /
            "19_verify_governed_corrective_successor_revision_v4.v1.py"
        ),
    ],
    text=True,
    capture_output=True,
)

assert proc.returncode == 0

assert (
    "D0222_GOVERNED_CORRECTIVE_SUCCESSOR_PACKAGE_VERIFIER=PASS"
    in proc.stdout
)

previous = (
    ROOT /
    "04_predecessor_returned_rereview.EXACT_COPY.v1.md"
)

assert previous.is_file()
assert sha(previous) == EXPECTED_PREDECESSOR_REVIEW_SHA
assert previous.stat().st_size == EXPECTED_PREDECESSOR_REVIEW_SIZE

reviewer = meta["reviewer_fields"]

for key, value in reviewer.items():
    assert type(value) is bool
    assert value is False, key

life = meta["review_lifecycle"]

assert life["review_package_authored"] is True
assert life["external_handoff_performed"] is False
assert life["returned_review_received"] is False
assert life["returned_review_recorded"] is False
assert life["corrective_successor_approved"] is False
assert life["governance_adopted"] is False

one = meta["one_time_verifier_lifecycle"]

assert one["execution_attempt_count"] == 1
assert one["execution_result"] == "PASS"
assert one["state"] == "PERMANENTLY_RETIRED"
assert one["rerun_authorized"] is False

assert one["d0220_a02_state"] == "SUPERSEDED_UNEXECUTED"
assert one["d0220_a02_execution_attempt_count"] == 0
assert one["d0220_a02_execution_authorized"] is False

for key, value in meta["explicit_nonauthorization"].items():
    assert type(value) is bool
    assert value is False, key

form = (
    ROOT /
    "01_blank_independent_human_rereview_form.MANUAL_REVIEW_COPY.v1.md"
).read_text(encoding="utf-8")

required_blank_lines = [
    "Reviewer name: ______________________________",
    "Reviewer role: ______________________________",
    "Review date: ______________________________",
    "Reviewer confirmation / signature: ______________________________",
    "[ ] I confirm that I performed this re-review independently",
    "## ASER04 reviewer decision",
    "## ASER07 reviewer decision",
    "# Overall independent human re-review decision",
]

for text in required_blank_lines:
    assert text in form

assert "[x] PASS" not in form.lower()
assert "[x] revision_required" not in form.lower()

manifest = (
    ROOT /
    "07_independent_human_rereview_package.v1.SHA256SUMS"
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
    p.relative_to(ROOT).as_posix()
    for p in ROOT.rglob("*")
    if p.is_file()
}

assert (
    actual
    == listed | {
        "07_independent_human_rereview_package.v1.SHA256SUMS"
    }
)

print("D0223_BLANK_INDEPENDENT_HUMAN_REREVIEW_PACKAGE_VERIFIER=PASS")
print("D0222_EXACT_CORRECTIVE_SUCCESSOR_COPY=PASS")
print("PREDECESSOR_RETURNED_REREVIEW_EXACT_COPY=PASS")
print("REVIEW_SCOPE=ASER04,ASER07")
print("ALL_REVIEWER_FIELDS_BLANK=YES")
print("REVIEWER_DECISIONS_PREFILLED=NO")
print("EXTERNAL_HANDOFF_PERFORMED=NO")
print("RETURNED_REREVIEW_RECEIVED=NO")
print("RETURNED_REREVIEW_RECORDED=NO")
print("CORRECTIVE_SUCCESSOR_APPROVED=NO")
print("GOVERNANCE_ADOPTED=NO")
print("D0221_R03_STATE=PERMANENTLY_RETIRED")
print("D0221_R03_RERUN_AUTHORIZED=NO")
print("D0220_A02_STATE=SUPERSEDED_UNEXECUTED")
print("ACTUAL_ACCOUNTING_EVIDENCE_ACQUISITION_AUTHORIZED=NO")
print("CONCRETE_MAPPING_AUTHORIZED=NO")
print("ACCOUNTING_SATISFACTION_DETERMINATION_AUTHORIZED=NO")
print("PAIR_RECLASSIFICATION_AUTHORIZED=NO")
print("ACTIVE_SCHEMA_V2_MODIFICATION_AUTHORIZED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
