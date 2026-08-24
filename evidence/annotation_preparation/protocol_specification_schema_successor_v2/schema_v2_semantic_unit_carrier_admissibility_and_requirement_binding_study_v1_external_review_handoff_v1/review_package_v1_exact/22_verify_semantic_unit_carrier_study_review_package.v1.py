#!/usr/bin/env python3

import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent

STUDY = HERE / "study_v1_exact"
D0110 = HERE / "decision0110_authorization_exact"
D0112 = HERE / "decision0112_authorization_exact"

DEC0111 = (
    HERE
    / "10_decision0111_author_checkpoint.EXACT_COPY.v1.md"
)

DEC0112 = (
    HERE
    / "17_decision0112_authorization_decision.EXACT_COPY.v1.md"
)

A02_OUT = (
    HERE
    / "18_decision0112_a02_final_output.EXACT_COPY.v1.txt"
)

CONSUMPTION = (
    HERE
    / "19_decision0112_a02_consumption_record.v1.json"
)

PACKET = (
    HERE
    / "20_SUCR01_SUCR08_reviewer_packet.MANUAL_REVIEW_COPY.v1.md"
)

MANIFEST = (
    HERE
    / "21_review_package_manifest.v1.json"
)

SUMS = (
    HERE
    / "23_review_package.v1.SHA256SUMS"
)

EXPECTED = {
    STUDY / "01_semantic_unit_carrier_admissibility_matrix.v1.json":
        "44a6e8169f8515921a980cb727e106281f47bbe1a6bc9672e16146bab2832a12",

    STUDY / "02_losslessness_requirement_binding_assessment.v1.json":
        "c8c6fd120f7046ac7e747124821796d1a3686be3dcf6ea40e712b96cdd851ee5",

    STUDY / "03_cross_unit_coherence_constraint_inventory.v1.json":
        "2b831650ec9d4af78f0a836150e79068846d1c70401251951593f9c9e341eb23",

    STUDY / "04_machine_readable_accounting.v1.json":
        "f271db56cdd680f85a14d8fe3d4a4b1e820b1bb5276215bd2ca8cb7486e307db",

    STUDY / "05_study_report.v1.md":
        "478edaee64ca375743e9d4be454603d1c1dd833742d3b4748626e2130c0f5be5",

    STUDY / "06_decision0110_a02_final_output.EXACT_COPY.v1.txt":
        "ff3be9a0d9b206d64e01a5e1665b203a34a2b89a637e3d4e2148582bfebe9f74",

    STUDY / "07_decision0110_a02_consumption_record.v1.json":
        "ff64213af1d88ba20ec0b95daa84ef8bc2e98818291785f711914d35a400df48",

    STUDY / "08_verify_semantic_unit_carrier_admissibility_and_requirement_binding_study.v1.py":
        "4b8c99000699589bc100fd558b7e64fcb70d40139294eb78faafbb4f10584dde",

    STUDY / "09_semantic_unit_carrier_admissibility_and_requirement_binding_study.v1.SHA256SUMS":
        "4a3120241af95c90f935a01c750c88a5d6eda15c513f15b9b377b25b39710795",

    DEC0111:
        "a9db3f9aff44da0a1dc17d62daa63f4c809c6bc81f531c610b746e08f12de105",

    D0110 / "01_semantic_unit_carrier_admissibility_and_requirement_binding_study_authorization.v1.json":
        "6e7aa96df28de6ae9b7c7b0ed08ff7f543cce6c15336480dade7c67ade8934d1",

    D0110 / "02_verify_semantic_unit_carrier_admissibility_and_requirement_binding_study_authoring_authorization.v1.py":
        "6544c325041e816373a8d5586be90e49223519b070a3df92037aca5738ab4d8e",

    D0110 / "03_semantic_unit_carrier_admissibility_and_requirement_binding_study_authorization.v1.SHA256SUMS":
        "f08f71fa1ba90cbbefb797979694c222a5341b3b76770adda3a0baeb9eda2f9d",

    D0112 / "01_review_package_authorization.v1.json":
        "61b797cf443839e58ae6b3cec0f6eb72c368ea08dc0708bf4be651834706d8b8",

    D0112 / "02_verify_review_package_authoring_authorization.v1.py":
        "1909a3e22aa39a643ed89475228ff0e47394c9b5d7b773e5f3e14e6dd891e5b0",

    D0112 / "03_review_package_authorization.v1.SHA256SUMS":
        "b3b97be6c0c914a52466585dd3c4e26986e3bda70f154d9780485d663257886e",

    DEC0112:
        "d2ba1d8fa2bf8fdc149e674ba7ecfdbb78c155206e3dfc146178e0736e4c9ff3",
}

def fail(msg):
    print("FAIL|" + msg)
    raise SystemExit(1)

def sha(path):
    if not path.is_file():
        fail(
            "MISSING|" + str(path)
        )

    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()

for path, expected in EXPECTED.items():
    if sha(path) != expected:
        fail(
            "SOURCE_BINDING|" + str(path)
        )

cons = json.loads(
    CONSUMPTION.read_text(
        encoding="utf-8"
    )
)

if cons["final_run_result"] != "PASS":
    fail(
        "DECISION0112_A02_FINAL_RESULT"
    )

if cons[
    "verifier_state_after_run"
] != "PERMANENTLY_RETIRED":
    fail(
        "DECISION0112_A02_STATE"
    )

if cons["rerun_authorized"] is not False:
    fail(
        "DECISION0112_A02_RERUN"
    )

if cons["must_never_be_rerun"] is not True:
    fail(
        "DECISION0112_A02_RETIREMENT_GUARD"
    )

if sha(A02_OUT) != cons["final_output_sha256"]:
    fail(
        "DECISION0112_A02_OUTPUT_SHA"
    )

if A02_OUT.stat().st_size != \
        cons["final_output_size_bytes"]:
    fail(
        "DECISION0112_A02_OUTPUT_SIZE"
    )

if (
    "REVIEW_PACKAGE_AUTHORING_AUTHORIZATION=PASS"
    not in A02_OUT.read_text(
        encoding="utf-8"
    )
):
    fail(
        "DECISION0112_A02_PASS_MARKER"
    )

manifest = json.loads(
    MANIFEST.read_text(
        encoding="utf-8"
    )
)

if manifest["package_state"] != \
        "BLANK_READY_FOR_INDEPENDENT_HUMAN_REVIEW":
    fail(
        "PACKAGE_STATE"
    )

facts = manifest["study_facts"]

expected_facts = {
    "semantic_unit_count":
        109,

    "schema_v2_property_path_count":
        171,

    "unit_carrier_cartesian_pair_count":
        18639,

    "candidate_admissible_count":
        0,

    "not_admissible_count":
        0,

    "unresolved_count":
        18639,

    "losslessness_requirement_count_in_scope":
        17,

    "requirement_bound_count":
        0,

    "requirement_unresolved_source_binding_count":
        17,

    "cross_unit_coherence_screening_hit_count":
        2,

    "accepted_explicit_cross_unit_constraint_count":
        0,

    "whole_v4_composition_enumeration_performed":
        False,
}

if facts != expected_facts:
    fail(
        "STUDY_FACTS"
    )

contract = manifest["review_contract"]

if contract[
    "required_reviewer_role"
] != "Spec-Technical-Reviewer-1":
    fail(
        "REVIEWER_ROLE"
    )

if contract["review_items"] != [
    "SUCR01",
    "SUCR02",
    "SUCR03",
    "SUCR04",
    "SUCR05",
    "SUCR06",
    "SUCR07",
    "SUCR08",
]:
    fail(
        "REVIEW_ITEMS"
    )

text = PACKET.read_text(
    encoding="utf-8"
)

if "Package state: `BLANK — AWAITING INDEPENDENT HUMAN REVIEW`" not in text:
    fail(
        "PACKET_NOT_BLANK"
    )

for rid in contract["review_items"]:
    if text.count(
        "## " + rid + " —"
    ) != 1:
        fail(
            "PACKET_REVIEW_ITEM|" + rid
        )

if text.count(
    "Decision (PASS / REVISION_REQUIRED / FAIL):"
) != 8:
    fail(
        "PACKET_DECISION_TEMPLATE_COUNT"
    )

if re.search(
    r"^Decision:\s*`?(PASS|REVISION_REQUIRED|FAIL)`?\s*$",
    text,
    flags=re.MULTILINE,
):
    fail(
        "PREPOPULATED_ITEM_DECISION"
    )

if re.search(
    r"^Overall decision:\s*`?(APPROVE_|REVISION_REQUIRED|FAIL)",
    text,
    flags=re.MULTILINE,
):
    fail(
        "PREPOPULATED_OVERALL_DECISION"
    )

for label in (
    "Human reviewer name:",
    "Human reviewer signature / recorded confirmation:",
    "Human reviewer date:",
    "Reviewer role:",
):
    m = re.search(
        rf"^{re.escape(label)}(.*)$",
        text,
        flags=re.MULTILINE,
    )

    if not m:
        fail(
            "MISSING_REVIEWER_FIELD|"
            + label
        )

    if m.group(1).strip():
        fail(
            "PREPOPULATED_REVIEWER_FIELD|"
            + label
        )

if manifest[
    "governance_nonclaims"
][
    "human_review_decision_exists"
] is not False:
    fail(
        "HUMAN_REVIEW_DECISION_EXISTS"
    )

for key, value in manifest[
    "governance_nonclaims"
].items():
    if value is not False:
        fail(
            "UNEXPECTED_PERMISSION|"
            + key
        )

if SUMS.is_file():
    lines = [
        line
        for line in SUMS.read_text(
            encoding="utf-8"
        ).splitlines()
        if line.strip()
    ]

    if len(lines) != 22:
        fail(
            "CHECKSUM_ENTRY_COUNT|"
            + str(len(lines))
        )

    for line in lines:
        digest, rel = line.split(
            None,
            1,
        )

        rel = rel.strip().lstrip("*")
        target = HERE / rel

        if sha(target) != digest:
            fail(
                "CHECKSUM|" + rel
            )

print("REVIEW_PACKAGE_SOURCE_BINDINGS=PASS")
print("STUDY_STATUS=AUTHOR_CANDIDATE")
print("GLOBAL_OUTCOME=FURTHER_EVIDENCE_REQUIRED")

print("SEMANTIC_UNIT_COUNT=109")
print("SCHEMA_V2_PROPERTY_PATH_COUNT=171")
print("UNIT_CARRIER_CARTESIAN_PAIR_COUNT=18639")
print("UNIT_CARRIER_UNRESOLVED_COUNT=18639")

print("LOSSLESSNESS_REQUIREMENT_COUNT_IN_SCOPE=17")
print("REQUIREMENT_BOUND_COUNT=0")
print("REQUIREMENT_UNRESOLVED_SOURCE_BINDING_COUNT=17")

print("CROSS_UNIT_COHERENCE_SCREENING_HIT_COUNT=2")
print("ACCEPTED_EXPLICIT_CROSS_UNIT_CONSTRAINT_COUNT=0")

print("SUCR01_SUCR08_REVIEW_CONTRACT=PASS")
print("REQUIRED_REVIEWER_ROLE=Spec-Technical-Reviewer-1")

print("ITEM_DECISIONS_PREPOPULATED=NO")
print("REVIEWER_NOTES_PREPOPULATED=NO")
print("OVERALL_DECISION_PREPOPULATED=NO")
print("REVIEWER_IDENTITY_PREPOPULATED=NO")

print("HUMAN_REVIEW_DECISION_EXISTS=NO")
print("STUDY_GOVERNANCE_ADOPTED=NO")

print("DECISION_0112_A02_STATE=PERMANENTLY_RETIRED")
print("DECISION_0112_A02_EXECUTED_BY_SAFE_VERIFIER=NO")
print("DECISION_0110_A02_EXECUTED_BY_SAFE_VERIFIER=NO")

print("OPERATIONAL_MAPPING_AUTHORIZED=NO")
print("SCHEMA_SUCCESSOR_AUTHORING_AUTHORIZED=NO")
print("CURL_JSON_AUTHORIZED=NO")
print("ANALYZER_AUTHORIZED=NO")
print("BASELINE_AUTHORIZED=NO")
print("REPAIR_AUTHORIZED=NO")

print("SEMANTIC_UNIT_CARRIER_STUDY_REVIEW_PACKAGE_V1=PASS")
