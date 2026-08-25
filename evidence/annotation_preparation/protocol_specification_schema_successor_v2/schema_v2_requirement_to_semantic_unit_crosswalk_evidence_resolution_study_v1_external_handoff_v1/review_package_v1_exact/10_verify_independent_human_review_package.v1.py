#!/usr/bin/env python3

import hashlib
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent

PASS_MARKER = (
    "REQUIREMENT_TO_SEMANTIC_UNIT_CROSSWALK_"
    "EVIDENCE_RESOLUTION_STUDY_V1_REVIEW_PACKAGE_"
    "AUTHORING_AUTHORIZATION=PASS"
)

EXPECTED = {
    "portable_sources/01_canonical_requirement_provenance_matrix.EXACT_COPY.v1.json":
        "a03a1c0d5e43a83d74534ed772503f46b3118cec9351f4324ac03ebeb51ae4ac",

    "portable_sources/02_semantic_unit_inventory.EXACT_COPY.v1.json":
        "2b39f5625658e41aeb906a1db8a4a472d9265dc3654572e60374827f0ce7fa7d",

    "portable_sources/03_semantic_unit_traceability.EXACT_COPY.v1.json":
        "6b4b30c958bc1e1dd0896fe086205e3ff58063583b2042bba962c8c59ba46bd4",

    "portable_sources/04_relation_informed_study_v1.EXACT_COPY.v1.json":
        "a8d28b09e78e1466eb5bb0991289879b28b10abd1dd1f9197d138ca723718f6f",

    "portable_sources/05_decision0108.EXACT_COPY.v1.md":
        "2ef3a1a1d8b73827bbc0c9d419e2db92aaa50cf402bd95a9c907a216ff84fe70",

    "portable_sources/06_decision0109.EXACT_COPY.v1.md":
        "1728f262195cd0f72bc744e566150a94c3fa28f1a6410150c5788bd24a8b5237",

    "portable_sources/07_historical_18639_pair_matrix.EXACT_COPY.v1.json":
        "44a6e8169f8515921a980cb727e106281f47bbe1a6bc9672e16146bab2832a12",

    "06_decision0149.EXACT_COPY.v1.md":
        "eb2a538468325fc17c87240a2542e794fa109a8f7d729079cf5354805f727e83",

    "07_decision0148.EXACT_COPY.v1.md":
        "9a48f45b74351cace9b4f1b2ee06fb037a3e71b5d0f268443270aed1f961adee",

    "08_decision0147.EXACT_COPY.v1.md":
        "6fb765713b1adcbe70b7cd412b0c1d4cec87ee02e615ec04169302acb38f5359",
}

def sha(path):
    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()

def load(name):
    return json.loads(
        (HERE / name).read_text(encoding="utf-8")
    )

manifest = load("01_review_package_manifest.v1.json")
consumption = load("05_decision0149_a02_consumption_record.v1.json")
portable = load("09_portable_source_binding_manifest.v1.json")

assert (
    manifest["status"]
    == "AUTHOR_CANDIDATE_AWAITING_INDEPENDENT_HUMAN_REVIEW"
)

result = manifest["source_study_result"]

assert result["requirement_count"] == 17
assert result["semantic_unit_count"] == 109
assert result["pair_universe_count"] == 1853

assert result["SUPPORTED_BINDING"] == 0
assert result["NOT_SUPPORTED_BINDING"] == 0
assert result["UNRESOLVED_BINDING"] == 1853

assert result["BOUND_SINGLE_UNIT"] == 0
assert result["BOUND_COMPOSITE_UNITS"] == 0
assert result["NO_AUTHORIZED_CROSSWALK_PROVEN"] == 0
assert result["UNRESOLVED_REQUIREMENTS"] == 17

assert result["global_outcome"] == "FURTHER_EVIDENCE_REQUIRED"

review = manifest["review_state"]

assert review["blank_reviewer_packet_present"] is True
assert review["independent_human_review_completed"] is False
assert review["reviewer_identity_recorded"] is False
assert review["reviewer_decisions_recorded"] is False
assert review["overall_review_decision_recorded"] is False

gov = manifest["governance_state"]

assert gov["external_handoff_authorized"] is False
assert gov["study_governance_adopted"] is False

assert all(
    v is False
    for v in manifest["non_authorizations"].values()
)

assert consumption["a02_execution_count"] == 1
assert consumption["a02_return_code"] == 0
assert consumption["a02_pass_marker_present"] is True
assert consumption["lifecycle_after_execution"] == "PERMANENTLY_RETIRED"
assert consumption["rerun_authorized"] is False
assert consumption["decision0147_a02_executed_by_this_transaction"] is False
assert consumption["retired_a02_verifier_execution_performed"] is False

a02_output = (
    HERE /
    "04_decision0149_a02_final_output.EXACT_COPY.v1.txt"
).read_text(encoding="utf-8")

assert PASS_MARKER in a02_output.splitlines()

# Reviewer packet must remain genuinely blank.
packet = (
    HERE /
    "03_CWXR01_CWXR08_reviewer_packet.INITIAL_BLANK.v1.md"
).read_text(encoding="utf-8")

blank_fields = [
    "CWXR01 decision:",
    "CWXR01 reviewer notes:",
    "CWXR02 decision:",
    "CWXR02 reviewer notes:",
    "CWXR03 decision:",
    "CWXR03 reviewer notes:",
    "CWXR04 decision:",
    "CWXR04 reviewer notes:",
    "CWXR05 decision:",
    "CWXR05 reviewer notes:",
    "CWXR06 decision:",
    "CWXR06 reviewer notes:",
    "CWXR07 decision:",
    "CWXR07 reviewer notes:",
    "CWXR08 decision:",
    "CWXR08 reviewer notes:",
    "Overall decision:",
    "Reviewer name:",
    "Reviewer role:",
    "Reviewer confirmation/signature:",
    "Review date:",
    "Overall reviewer notes:",
]

packet_lines = packet.splitlines()

for field in blank_fields:
    assert packet_lines.count(field) == 1

# Verify portable source bytes.
for rel, expected in EXPECTED.items():
    p = HERE / rel
    assert p.is_file()
    assert sha(p) == expected

assert portable["portable_source_count"] == 7
assert portable["all_required_source_classes_present"] is True
assert portable["source_semantics_modified"] is False

# Verify copied Study V1 with its repeat-safe verifier.
study = HERE / "study_v1_exact"

study_output = subprocess.check_output(
    [
        "python3",
        str(
            study /
            "10_verify_requirement_to_semantic_unit_crosswalk_"
            "evidence_resolution_study_v1.v1.py"
        ),
    ],
    text=True,
)

required_study_markers = [
    (
        "REQUIREMENT_TO_SEMANTIC_UNIT_CROSSWALK_"
        "EVIDENCE_RESOLUTION_STUDY_V1=PASS"
    ),
    "STUDY_STATUS=AUTHOR_CANDIDATE",
    "PAIR_UNIVERSE_COUNT=1853",
    "UNRESOLVED_BINDING_COUNT=1853",
    "UNRESOLVED_REQUIREMENT_COUNT=17",
    "GLOBAL_OUTCOME=FURTHER_EVIDENCE_REQUIRED",
    "INDEPENDENT_HUMAN_REVIEW_REQUIRED=YES",
    "STUDY_GOVERNANCE_ADOPTED=NO",
    "DECISION_0147_A02_STATE=PERMANENTLY_RETIRED",
]

study_lines = study_output.splitlines()

for marker in required_study_markers:
    assert marker in study_lines

# Verify package checksum closure covers every package file except itself.
sumfile = HERE / "11_review_package_v1.SHA256SUMS"

checksum_entries = {}

for line in sumfile.read_text(
    encoding="utf-8"
).splitlines():

    if not line.strip():
        continue

    expected, name = line.split(None, 1)
    name = name.strip().lstrip("*")

    if name.startswith("./"):
        name = name[2:]

    assert name not in checksum_entries
    checksum_entries[name] = expected

actual_files = {
    str(p.relative_to(HERE))
    for p in HERE.rglob("*")
    if p.is_file()
    and p.name != "11_review_package_v1.SHA256SUMS"
}

assert set(checksum_entries) == actual_files

for name, expected in checksum_entries.items():
    assert sha(HERE / name) == expected

assert len(actual_files) == 28
assert len(checksum_entries) == 28

print(
    "REQUIREMENT_TO_SEMANTIC_UNIT_CROSSWALK_EVIDENCE_"
    "RESOLUTION_STUDY_V1_INDEPENDENT_HUMAN_REVIEW_PACKAGE=PASS"
)

print("PACKAGE_STATUS=AUTHOR_CANDIDATE_AWAITING_INDEPENDENT_HUMAN_REVIEW")
print("REVIEW_ITEM_COUNT=8")
print("BLANK_REVIEWER_PACKET=PASS")
print("PORTABLE_SOURCE_COUNT=7")
print("PACKAGE_CHECKSUM_ENTRY_COUNT=28")
print("SOURCE_STUDY_TREE_COPY_PRESENT=YES")
print("SOURCE_STUDY_REPEAT_SAFE_VERIFICATION=PASS")
print("INDEPENDENT_HUMAN_REVIEW_COMPLETED=NO")
print("REVIEWER_IDENTITY_RECORDED=NO")
print("REVIEWER_DECISIONS_RECORDED=NO")
print("EXTERNAL_HANDOFF_AUTHORIZED=NO")
print("STUDY_GOVERNANCE_ADOPTED=NO")
print("DECISION_0149_A02_STATE=PERMANENTLY_RETIRED")
print("DECISION_0149_A02_RERUN_AUTHORIZED=NO")
print("DECISION_0147_A02_RERUN=NO")
print("PAIR_RECLASSIFICATION=NO")
print("HISTORICAL_18639_PAIR_RECLASSIFICATION=NO")
print("OPERATIONAL_MAPPING_AUTHORIZED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
