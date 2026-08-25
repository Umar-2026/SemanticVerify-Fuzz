#!/usr/bin/env python3

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def load(name):
    return json.loads(
        (HERE / name).read_text(encoding="utf-8")
    )

manifest = load("01_study_manifest.v1.json")
req = load("02_canonical_requirement_inventory.EXACT_COPY.v1.json")
unit = load("03_semantic_unit_inventory.EXACT_COPY.v1.json")
pairs = load("04_requirement_semantic_unit_pair_matrix.v1.json")
roll = load("05_requirement_crosswalk_rollup.v1.json")
prov = load("06_evidence_provenance_matrix.v1.json")
acct = load("07_accounting_summary.v1.json")
cons = load("09_decision0147_a02_consumption_record.v1.json")

a02_output = (
    HERE /
    "08_decision0147_a02_final_output.EXACT_COPY.v1.txt"
).read_text(encoding="utf-8")

PASS_MARKER = (
    "REQUIREMENT_TO_SEMANTIC_UNIT_CROSSWALK_"
    "EVIDENCE_RESOLUTION_STUDY_V1_AUTHORING_"
    "AUTHORIZATION=PASS"
)

assert PASS_MARKER in a02_output

requirements = req["records"]
units = unit["semantic_units"]
rows = pairs["pairs"]
rollups = roll["records"]

assert len(requirements) == 17
assert len(units) == 109
assert len(rows) == 1853
assert len(rollups) == 17
assert len(prov["records"]) == 17

req_ids = [x["requirement_id"] for x in requirements]
unit_ids = [x["unit_id"] for x in units]

assert len(set(req_ids)) == 17
assert len(set(unit_ids)) == 109

expected_pairs = {
    (r, u)
    for r in req_ids
    for u in unit_ids
}

actual_pairs = {
    (x["requirement_id"], x["semantic_unit_id"])
    for x in rows
}

assert actual_pairs == expected_pairs

allowed_pairs = {
    "SUPPORTED_BINDING",
    "NOT_SUPPORTED_BINDING",
    "UNRESOLVED_BINDING",
}

assert all(
    x["classification"] in allowed_pairs
    for x in rows
)

supported = [
    x for x in rows
    if x["classification"] == "SUPPORTED_BINDING"
]

not_supported = [
    x for x in rows
    if x["classification"] == "NOT_SUPPORTED_BINDING"
]

unresolved = [
    x for x in rows
    if x["classification"] == "UNRESOLVED_BINDING"
]

# Positive/negative classifications would require explicit evidence
# fields. This author candidate intentionally performs no such
# promotion.
for row in supported + not_supported:
    assert row.get("classification_basis")
    assert row.get("requirement_evidence")
    assert row.get("semantic_unit_evidence")

assert len(supported) == 0
assert len(not_supported) == 0
assert len(unresolved) == 1853

allowed_rollups = {
    "BOUND_SINGLE_UNIT",
    "BOUND_COMPOSITE_UNITS",
    "NO_AUTHORIZED_CROSSWALK_PROVEN",
    "UNRESOLVED",
}

for r in rollups:
    assert r["classification"] in allowed_rollups

    a = r["pair_accounting"]

    assert a["total_pair_count"] == 109
    assert a["all_109_units_accounted"] is True

    if a["unresolved_binding_count"] > 0:
        assert r["classification"] == "UNRESOLVED"

    elif a["supported_binding_count"] == 1:
        assert r["classification"] == "BOUND_SINGLE_UNIT"

    elif a["supported_binding_count"] > 1:
        assert r["classification"] == "BOUND_COMPOSITE_UNITS"

    elif (
        a["supported_binding_count"] == 0
        and a["unresolved_binding_count"] == 0
    ):
        assert (
            r["classification"]
            == "NO_AUTHORIZED_CROSSWALK_PROVEN"
        )

assert all(
    r["classification"] == "UNRESOLVED"
    for r in rollups
)

assert acct["pair_classification_counts"] == {
    "SUPPORTED_BINDING": 0,
    "NOT_SUPPORTED_BINDING": 0,
    "UNRESOLVED_BINDING": 1853,
}

assert acct["requirement_rollup_counts"] == {
    "BOUND_SINGLE_UNIT": 0,
    "BOUND_COMPOSITE_UNITS": 0,
    "NO_AUTHORIZED_CROSSWALK_PROVEN": 0,
    "UNRESOLVED": 17,
}

assert acct["global_outcome"] == "FURTHER_EVIDENCE_REQUIRED"

assert cons["a02_execution_count"] == 1
assert cons["a02_return_code"] == 0
assert cons["a02_pass_marker_present"] is True
assert cons["lifecycle_after_execution"] == "PERMANENTLY_RETIRED"
assert cons["rerun_authorized"] is False

assert manifest["status"] == "AUTHOR_CANDIDATE"
assert manifest["review_state"]["independent_human_review_required"] is True
assert manifest["review_state"]["independent_human_review_completed"] is False
assert manifest["review_state"]["governance_adopted"] is False

assert (
    manifest["result"]["global_outcome"]
    == "FURTHER_EVIDENCE_REQUIRED"
)

for v in manifest["non_authorizations"].values():
    assert v is False

assert (
    pairs["historical_18639_pair_matrix"]
    ["reclassification_performed"]
    is False
)

# Verify checksum closure.
checksum_file = HERE / "11_study_v1.SHA256SUMS"

seen = set()

for line in checksum_file.read_text(
    encoding="utf-8"
).splitlines():

    if not line.strip():
        continue

    expected, name = line.split(None, 1)
    name = name.strip().lstrip("*")

    p = HERE / name

    assert p.is_file()
    assert sha(p) == expected

    seen.add(name)

required_checksum_members = {
    "01_study_manifest.v1.json",
    "02_canonical_requirement_inventory.EXACT_COPY.v1.json",
    "03_semantic_unit_inventory.EXACT_COPY.v1.json",
    "04_requirement_semantic_unit_pair_matrix.v1.json",
    "05_requirement_crosswalk_rollup.v1.json",
    "06_evidence_provenance_matrix.v1.json",
    "07_accounting_summary.v1.json",
    "08_decision0147_a02_final_output.EXACT_COPY.v1.txt",
    "09_decision0147_a02_consumption_record.v1.json",
    "10_verify_requirement_to_semantic_unit_crosswalk_evidence_resolution_study_v1.v1.py",
}

assert seen == required_checksum_members

print(
    "REQUIREMENT_TO_SEMANTIC_UNIT_CROSSWALK_"
    "EVIDENCE_RESOLUTION_STUDY_V1=PASS"
)
print("STUDY_STATUS=AUTHOR_CANDIDATE")
print("REQUIREMENT_COUNT=17")
print("SEMANTIC_UNIT_COUNT=109")
print("PAIR_UNIVERSE_COUNT=1853")
print("SUPPORTED_BINDING_COUNT=0")
print("NOT_SUPPORTED_BINDING_COUNT=0")
print("UNRESOLVED_BINDING_COUNT=1853")
print("BOUND_SINGLE_UNIT_COUNT=0")
print("BOUND_COMPOSITE_UNITS_COUNT=0")
print("NO_AUTHORIZED_CROSSWALK_PROVEN_COUNT=0")
print("UNRESOLVED_REQUIREMENT_COUNT=17")
print("GLOBAL_OUTCOME=FURTHER_EVIDENCE_REQUIRED")
print("HISTORICAL_18639_PAIR_RECLASSIFICATION=NO")
print("CARRIER_ADMISSIBILITY_RECLASSIFICATION=NO")
print("OPERATIONAL_MAPPING_AUTHORIZED=NO")
print("SCHEMA_V2_MODIFICATION_AUTHORIZED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")
print("INDEPENDENT_HUMAN_REVIEW_REQUIRED=YES")
print("STUDY_GOVERNANCE_ADOPTED=NO")
print("DECISION_0147_A02_STATE=PERMANENTLY_RETIRED")
